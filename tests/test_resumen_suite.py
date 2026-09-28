#!/usr/bin/env python3
"""ACTO GEN2-TUBERIA-RESUMEN-SUITE-1 — guardias de las tres piezas.

P1: `tools/resumen_suite.py` lee VERDE / ROJO / NO-TERMINÓ del log real de
`tests/check.py --baseline` y el tablero dice cuándo el resumen es viejo.
P2: T03 indexa `.claude/` (caso del encargo: `tramite.md`).
P3: `status` publica `dependencias_numericas_legacy_definicion_desde`
derivada del historial, no tecleada.
Corre como huérfano (`tools/ci_guardias.py --ejecuta-huerfanos`).
"""
import datetime as dt
import importlib.util
import os
import re
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import resumen_suite as RS  # noqa: E402

LOG_VERDE = """
════════════════════════════════════════════════════════════════════════
  0 FAIL · 131 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado abc)
  WARN NUEVOS (estado, no adjudican): 2
  · T03: forense/x.md cita `y.md`, que no existe
  · T10: algo
────────────────────────────────────────────────────────────────────────
"""
LOG_ROJO = """
  2 FAIL · 5 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: ROJO — 1 FAIL nuevos frente a tests/baseline.json (HEAD congelado abc)
  · T06: se rompió
────────────────────────────────────────────────────────────────────────
"""


def _tabla(texto):
    return [l.split("\t") for l in texto.splitlines() if l and not l.startswith("#")]


class P1Resumen(unittest.TestCase):
    def test_verde_con_warn_nuevos(self):
        r = RS.parsea(LOG_VERDE)
        self.assertEqual((r["resultado"], r["fail_total"], r["warn_total"]), ("VERDE", "0", "131"))
        self.assertEqual(r["warn_nuevos"], 2)
        self.assertEqual(r["fail_nuevo"], [])
        self.assertTrue(r["warn_nuevo"][0].startswith("T03:"))

    def test_rojo_lista_fail(self):
        r = RS.parsea(LOG_ROJO)
        self.assertEqual(r["resultado"], "ROJO")
        self.assertEqual(r["fail_nuevo"], ["T06: se rompió"])

    def test_log_truncado_no_termino(self):
        self.assertEqual(RS.parsea("  12 FAIL")["resultado"], "NO-TERMINÓ")
        self.assertEqual(RS.parsea("")["resultado"], "NO-TERMINÓ")

    def test_ida_y_vuelta_y_viejo(self):
        import tempfile
        tsv = RS.construye(LOG_VERDE, "deadbeefcafe", "190", "42", "2026-09-20T09:00:00Z")
        self.assertIn(["commit", "deadbeefcafe"], _tabla(tsv))
        with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
            f.write(tsv)
        try:
            d = RS.lee(f.name)
        finally:
            os.unlink(f.name)
        self.assertEqual(d["resultado"], "VERDE")
        self.assertEqual(len(d["warn_nuevo"]), 2)
        hoy = dt.datetime(2026, 9, 21, 12, tzinfo=dt.timezone.utc)
        self.assertTrue(RS.linea(d, hoy).startswith("suite VERDE @ deadbeef"))
        tarde = dt.datetime(2026, 9, 27, 12, tzinfo=dt.timezone.utc)
        self.assertIn("sin corrida nocturna desde 2026-09-20", RS.linea(d, tarde))
        self.assertIn("ausente", RS.linea(None))


class P2T03Ocultos(unittest.TestCase):
    def test_tramite_md_bajo_claude_no_es_colgante(self):
        self.assertTrue(os.path.exists(os.path.join(RAIZ, ".claude", "commands", "tramite.md")))
        spec = importlib.util.spec_from_file_location("check_t03", os.path.join(RAIZ, "tests", "check.py"))
        m = importlib.util.module_from_spec(spec)
        argv = sys.argv
        sys.argv = ["check.py"]
        try:
            spec.loader.exec_module(m)
        finally:
            sys.argv = argv
        self.assertNotIn("tramite.md", m.HISTORICOS)
        self.assertNotIn("revisa.md", m.HISTORICOS)
        avisos = []
        m.warn = lambda t, msg: avisos.append(msg)
        m.t03_dangling_refs()
        ocultos = {os.path.basename(p) for d, _, fs in os.walk(os.path.join(RAIZ, ".claude")) for p in fs}
        colgantes_ocultos = [a for a in avisos if re.search(r"cita `([^`]+)`", a).group(1) in ocultos]
        self.assertEqual(colgantes_ocultos, [])


class P3DefinicionLegacy(unittest.TestCase):
    def test_clave_derivada(self):
        sys.argv, argv = ["corrida0.py"], sys.argv
        try:
            import corrida0
        finally:
            sys.argv = argv
        v = corrida0._legacy_definicion_desde()
        self.assertTrue(re.fullmatch(r"[0-9a-f]{7}|NO-VERIFICABLE-[A-Z\-]+", v), v)


if __name__ == "__main__":
    unittest.main()
