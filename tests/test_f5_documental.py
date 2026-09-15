import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ROOT / ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mcp = cargar("f5_documental_mcp", "tools/f5_documental_mcp.py")
runner = cargar("f5_documental", "tools/f5_documental.py")


class TestMcpAislado(unittest.TestCase):
    def test_distribucion_y_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            p = root / "analysis.tsv"
            p.write_text("respuesta\tpeso\n1\t2\n2\t3\n1\t5\n", encoding="utf-8")
            out = mcp.distribucion_ponderada(root, {
                "path": "analysis.tsv", "value_column": "respuesta", "weight_column": "peso"})
            self.assertEqual(out["rows_read"], 3)
            self.assertEqual(out["weighted_total_nonmissing"], 10)
            self.assertEqual(out["distribution"][0]["weighted_share_of_nonmissing"], .7)

    def test_ruta_fuera_rechazada(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                mcp.distribucion_ponderada(pathlib.Path(td), {
                    "path": "../fuera.tsv", "value_column": "x", "weight_column": "w"})


class TestPresupuesto(unittest.TestCase):
    def test_cargo_real_sin_recorte(self):
        # v1_1 (c): sin sobre se conserva la reserva; num_turns real se carga tal cual, nunca recortado hacia abajo.
        self.assertEqual(runner.cargo_solicitudes(None), runner.CARGO_RESERVA)
        self.assertEqual(runner.cargo_solicitudes({"num_turns": 1}), 1)
        self.assertEqual(runner.cargo_solicitudes({"num_turns": 3}), 3)
        self.assertEqual(runner.cargo_solicitudes({"num_turns": 99}), 99)
        self.assertEqual(runner.cargo_solicitudes({"num_turns": 0}), 1)
        self.assertEqual(runner.cargo_solicitudes({}), 1)

    def test_comando_sin_max_turns_con_permiso_y_presupuesto(self):
        cmd = runner.comando_mcp(pathlib.Path("/tmp/x"))
        self.assertNotIn("--max-turns", cmd)
        self.assertIn("--allowedTools", cmd)
        self.assertEqual(cmd[cmd.index("--allowedTools") + 1], runner.HERRAMIENTA)
        self.assertEqual(cmd[cmd.index("--max-budget-usd") + 1], "2.00")
        self.assertIn("--permission-prompts", cmd)
        self.assertIn("--restricted", cmd)

    def test_identidad_modelo_regla_a(self):
        opus = {"canonicalModel": "claude-opus-5", "inputTokens": 4, "outputTokens": 867,
                "cacheCreationInputTokens": 118212, "cacheReadInputTokens": 117745}
        usage = {"input_tokens": 4, "output_tokens": 867, "cache_creation_input_tokens": 118212,
                 "cache_read_input_tokens": 117745}
        haiku = {"canonicalModel": "claude-haiku-4-5", "inputTokens": 91703, "outputTokens": 22,
                 "cacheCreationInputTokens": 0, "cacheReadInputTokens": 0}
        ok = runner.identidad_modelo({"usage": usage, "modelUsage": {"claude-opus-5": opus, "claude-haiku-4-5-20251001": haiku}})
        self.assertTrue(ok["ok"]); self.assertTrue(ok["reconciliacion_usage_modelo"]["ok"])
        self.assertEqual(ok["modelos_auxiliares"][0]["modelo"], "claude-haiku-4-5")
        gordo = runner.identidad_modelo({"usage": usage, "modelUsage": {"claude-opus-5": opus,
                                          "h": {**haiku, "outputTokens": runner.AUX_TOPE_SALIDA + 1}}})
        self.assertFalse(gordo["ok"])
        desajuste = runner.identidad_modelo({"usage": {**usage, "output_tokens": 1}, "modelUsage": {"claude-opus-5": opus}})
        self.assertFalse(desajuste["ok"])
        self.assertFalse(runner.identidad_modelo(None)["ok"])

    def test_reserva_previa_es_conservadora(self):
        with tempfile.TemporaryDirectory() as td:
            anterior = runner.LEDGER
            runner.LEDGER = pathlib.Path(td) / "ledger.json"
            try:
                ledger = {"techo": 96, "consumidas_conservadoras": 0, "eventos": []}
                i = runner.reservar_invocacion(ledger, "TEST", "x")
                self.assertEqual(ledger["consumidas_conservadoras"], runner.CARGO_RESERVA)
                runner.cerrar_reserva(ledger, i, {"num_turns": 1})
                self.assertEqual(ledger["consumidas_conservadoras"], 1)
                # un num_turns real por encima de la reserva se carga entero (nunca menos de lo usado)
                j = runner.reservar_invocacion(ledger, "TEST", "y")
                runner.cerrar_reserva(ledger, j, {"num_turns": runner.CARGO_RESERVA + 2})
                self.assertEqual(ledger["consumidas_conservadoras"], 1 + runner.CARGO_RESERVA + 2)
            finally:
                runner.LEDGER = anterior

    def test_modelo_exacto(self):
        sobre = {"modelUsage": {"opus": {"canonicalModel": "claude-opus-5"}}}
        self.assertEqual(runner.modelos(sobre), {"claude-opus-5"})


class TestFirma(unittest.TestCase):
    def test_cola_no_es_firma(self):
        cola = ROOT / "forense/encargos/cola/2026-09-11-GEN2-F5-DOCUMENTAL-EJECUCION-PENDIENTE.md"
        with self.assertRaisesRegex(RuntimeError, "no constituye firma"):
            runner.verificar_autorizacion(cola)


class TestPrompt(unittest.TestCase):
    def test_esquema_exige_traza_y_sustitucion(self):
        req = set(runner.ESQUEMA["required"])
        self.assertTrue({"fuente_documental", "derivacion", "sustitucion_semantica"} <= req)

    def test_32_posiciones(self):
        if not runner.MANIFIESTO_TRANSPORTE.exists():
            self.skipTest("materializacion aun no generada")
        manifest = json.loads(runner.MANIFIESTO_TRANSPORTE.read_text(encoding="utf-8"))
        ps = runner.posiciones("cliente-prueba", runner.PAQUETE_PREDETERMINADO, manifest)
        self.assertEqual(len(ps), 32)
        self.assertEqual(len({p["identidad"] for p in ps}), 32)

    def test_control_no_contiene_tabla_dirigida(self):
        for cid in runner.CELDAS:
            control = runner.PAQUETE_PREDETERMINADO / cid / "CONTEXTUAL-v2"
            self.assertFalse((control / "analysis.tsv").exists())
            self.assertEqual([p.name for p in control.iterdir()], ["contextual.txt"])


if __name__ == "__main__":
    unittest.main()
