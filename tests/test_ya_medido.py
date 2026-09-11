"""Regresiones dirigidas para tools/ya_medido.py (NC-0109/NC-0129)."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools import ya_medido


class YaMedidoEvidencia(unittest.TestCase):
    def _yaml(self, raiz: Path, texto: str) -> Path:
        ruta = raiz / "fixture.yaml"
        ruta.write_text(texto, encoding="utf-8")
        return ruta

    def _corrida(self, raiz: Path, ref: str, valor=0.25) -> Path:
        corrida = raiz / "corrida0" / "CALC-FIXTURE"
        corrida.mkdir(parents=True)
        resultados = corrida / "resultados.json"
        ejecucion = corrida / "ejecucion.json"
        sello = corrida / "sello.json"
        resultados.write_text(
            json.dumps(
                {"spec_id": "CALC-FIXTURE", "resultados": {ref: valor}},
                indent=1,
            )
            + "\n",
            encoding="utf-8",
        )
        ejecucion.write_text(
            json.dumps({"exit_code": 0, "resultado_ids": [ref]}, indent=1)
            + "\n",
            encoding="utf-8",
        )
        hashes = {
            ruta.name: hashlib.sha256(ruta.read_bytes()).hexdigest()
            for ruta in (resultados, ejecucion)
        }
        sello.write_text(json.dumps(hashes, indent=1) + "\n", encoding="utf-8")
        (corrida / "sello.sha256").write_text(
            f"{hashlib.sha256(sello.read_bytes()).hexdigest()}  sello.json\n",
            encoding="utf-8",
        )
        return raiz / "corrida0"

    def test_tasa_ejecutada_resuelve_result_ejecucion_y_sello(self):
        with tempfile.TemporaryDirectory() as td:
            raiz = Path(td)
            ref = "RESULT-FIXTURE-TASA-P"
            ruta = self._yaml(
                raiz,
                f"""reglas:
  - id: regla.tasa
    entonces:
      - {{conducta: si, p: 0.25, clase: \"MEDIDO·p(tasa)\", corrida0_resultado_id: {ref}}}
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(str(ruta), ["regla.tasa"])
            corrida = ya_medido.busca_referencias_corrida(
                {ref}, str(self._corrida(raiz, ref))
            )
            ya_medido.vincula_evidencia_corrida(ocurrencias, corrida)
            self.assertEqual("TASA-EJECUTADA", ocurrencias[0]["veredicto_real"])
            self.assertEqual("TASA-EJECUTADA", corrida[0]["veredicto_real"])
            self.assertEqual("VALIDO", corrida[0]["campos"]["sello"])

    def test_propuesta_con_p_y_result_declarado_no_es_ejecucion(self):
        with tempfile.TemporaryDirectory() as td:
            ruta = self._yaml(
                Path(td),
                """reglas:
  - id: regla.propuesta
    p: 0.42
    clase: \"MEDIDO·p(tasa propuesta)\"
    nota: \"MEDIDO en prosa; RESULT-FUTURO se correra despues\"
    corrida0_resultado_id: RESULT-FUTURO
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(
                str(ruta), ["regla.propuesta"]
            )
            corrida = ya_medido.busca_referencias_corrida(
                {"RESULT-FUTURO"}, str(Path(td) / "sin-corridas")
            )
            ya_medido.vincula_evidencia_corrida(ocurrencias, corrida)
            self.assertIsNone(ocurrencias[0]["veredicto_real"])
            self.assertEqual([], corrida)

    def test_reglas_vecinas_no_comparten_veredicto(self):
        with tempfile.TemporaryDirectory() as td:
            ruta = self._yaml(
                Path(td),
                """reglas:
  - id: regla.objetivo
    veredicto_Bbis: NO-DISCRIMINA
    n: 40
    sha256_payload: propio
  - id: regla.vecina
    veredicto_Bbis: CONTRARIA
    n: 50
    sha256_payload: abc123
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(
                str(ruta), ["regla.objetivo"]
            )
            self.assertEqual(["id: regla.objetivo"], [o["contexto"] for o in ocurrencias])
            self.assertEqual("NO-DISCRIMINA", ocurrencias[0]["veredicto_real"])

    def test_evidencia_mas_alla_de_260_caracteres_sigue_en_su_bloque(self):
        with tempfile.TemporaryDirectory() as td:
            relleno = "x" * 600
            ruta = self._yaml(
                Path(td),
                f"""reglas:
  - id: regla.larga
    nota: {relleno}
    veredicto_Bbis: NO-DISCRIMINA
    n: 125
    sha256_payload: abc123
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(str(ruta), ["regla.larga"])
            self.assertEqual("NO-DISCRIMINA", ocurrencias[0]["veredicto_real"])

    def test_alias_declarado_es_identidad_y_no_parecido(self):
        with tempfile.TemporaryDirectory() as td:
            ruta = self._yaml(
                Path(td),
                """reglas:
  - id: regla.base_extension_no_alias
    veredicto_Bbis: CONTRARIA
    n: 20
    sha256_payload: vecino
  - id: regla.variante
    referida_a: >
      misma regla regla.base, declarada expresamente
    clase: \"MEDIDO·p(tasa)\"
    n: 30
    sha256_payload: propio
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(str(ruta), ["regla.base"])
            self.assertEqual(["id: regla.variante"], [o["contexto"] for o in ocurrencias])
            self.assertEqual("TASA-EJECUTADA", ocurrencias[0]["veredicto_real"])

    def test_no_estimable_acredita_intento_sin_inventar_p(self):
        with tempfile.TemporaryDirectory() as td:
            ruta = self._yaml(
                Path(td),
                """reglas:
  - id: regla.no_estimable
    situacion: NO-ESTIMABLE
    veredicto_Bbis: NO-ESTIMABLE
    medido_en: \"ACTO FIXTURE; salida ejecutada\"
""",
            )
            ocurrencias = ya_medido.busca_en_yaml(
                str(ruta), ["regla.no_estimable"]
            )
            self.assertEqual(
                "INTENTO-NO-ESTIMABLE", ocurrencias[0]["veredicto_real"]
            )
            self.assertNotIn("p", ocurrencias[0]["campos"])


class YaMedidoIntegracion(unittest.TestCase):
    def _salida(self, token: str) -> str:
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            self.assertEqual(0, ya_medido.main(["ya_medido.py", token]))
        return salida.getvalue()

    def test_dos_tasas_reales_citan_corrida_sustantiva(self):
        casos = {
            "tramite.mordida.con_registro": "CALC-ENCIG-0001",
            "dinero.ahorro.horizonte_no_corto_con_seguridad_social":
                "CALC-ENIF-0001",
        }
        for regla, calc in casos.items():
            with self.subTest(regla=regla):
                salida = self._salida(regla)
                self.assertIn(f"data/corrida0/{calc}/resultados.json", salida)
                self.assertIn("ejecutado=SI sello=VALIDO", salida)
                self.assertTrue(salida.rstrip().splitlines()[-1].startswith("MEDIDA-EN:"))

    def test_controles_historicos_positivo_y_negativo(self):
        positivo = self._salida("civico.voto.clientelar_si_observable")
        negativo = self._salida("familia.cortejo.urbano_joven_apps")
        self.assertTrue(positivo.rstrip().splitlines()[-1].startswith("MEDIDA-EN:"))
        self.assertEqual("NUNCA-MEDIDA", negativo.rstrip().splitlines()[-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
