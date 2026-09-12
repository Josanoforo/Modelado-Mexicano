"""Pruebas dirigidas de B-7: identidad, cero, faltantes y rupturas."""

from __future__ import annotations

import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import corrida0 as C  # noqa: E402
import delta_comparacion as D  # noqa: E402


ENTRADA = ROOT / "forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA/pares-v1_0.yaml"


class DeltaComparacionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.informe = D.ejecuta(ENTRADA, C)
        cls.por_id = {p["id"]: p for p in cls.informe["pares"]}
        cls.contrato = C._yaml_safe_load(ENTRADA.read_text(encoding="utf-8"))

    def test_caso_647_usa_fuente_congelada_y_result_sellado(self):
        par = self.por_id["DELTA-REMESAS-ENIGH2022-GRANO"]
        self.assertEqual(par["reproducibilidad_referencias"], "ACREDITADA")
        self.assertEqual(par["referencias"]["a"]["valor"], 0.045694)
        self.assertEqual(par["referencias"]["b"]["valor"], 0.04569409956405095)
        self.assertAlmostEqual(
            par["diferencia"]["delta"], 9.956405094824206e-08, places=20)
        self.assertAlmostEqual(
            par["diferencia"]["puntos_porcentuales"],
            9.956405094824206e-06, places=18)
        self.assertEqual(par["representacion"]["estado"], "IGUAL-AL-GRANO")
        self.assertIn("6 decimales", par["representacion"]["modo"])
        self.assertEqual(par["materialidad"]["estado"], "NO-DETERMINABLE")

    def test_credito_temporal_admite_periodos_distintos(self):
        par = self.por_id["DELTA-ENIF-CREDITO-APP-2024-MENOS-2021"]
        self.assertEqual(par["comparabilidad"]["estado"], "DEMOSTRADA")
        self.assertEqual(
            par["comparabilidad"]["dimensiones"]["periodo"]["estado"],
            "DISTINTO-INTENCIONAL")
        self.assertAlmostEqual(par["diferencia"]["puntos_porcentuales"],
                               -12.303002012, places=10)
        self.assertEqual(par["representacion"]["estado"], "DISTINTO-AL-GRANO")
        self.assertEqual(par["materialidad"]["estado"], "NO-DETERMINABLE")

    def test_cuenta_con_ruptura_rechaza_delta_sustantivo(self):
        par = self.por_id["RECHAZO-ENIF-CUENTA-APP-2024-2021"]
        self.assertEqual(par["comparabilidad"]["estado"], "INCOMPATIBILIDAD")
        self.assertEqual(par["diferencia"]["estado"],
                         "NO-CALCULADO-COMPARABILIDAD")
        self.assertIsNone(par["diferencia"]["delta"])
        self.assertEqual(par["resultado"],
                         "DELTA-SUSTANTIVO-RECHAZADO-INCOMPATIBILIDAD")

    def test_base_cero_no_fabrica_cambio_relativo(self):
        delta = D.calcula_diferencia(
            0.0, 0.25, escala="proporcion", relativo_permitido=True)
        self.assertEqual(delta["estado"], "CALCULADO")
        self.assertEqual(delta["delta"], 0.25)
        self.assertEqual(delta["puntos_porcentuales"], 25.0)
        self.assertIsNone(delta["cambio_relativo"])
        self.assertEqual(delta["estado_relativo"], "NO-APLICA-BASE-CERO")

    def test_valor_ausente_conserva_estado(self):
        delta = D.calcula_diferencia(
            None, 0.25, escala="proporcion", relativo_permitido=True)
        self.assertEqual(delta["estado"], "NO-CALCULABLE-VALOR-AUSENTE")
        self.assertIsNone(delta["delta"])

    def test_result_ausente_no_se_resuelve_por_nombre_parecido(self):
        par = copy.deepcopy(self.contrato["pares"][0])
        par["id"] = "FALTANTE-DIRIGIDO"
        par["b"]["resultado_id"] = "RESULT-B-ENIGH-2022-P-AUSENTE"
        salida = D.compara_par(par, C)
        self.assertEqual(salida["referencias"]["b"]["estado"], "NO-RESUELTA")
        self.assertIn("aparece 0 veces en spec", salida["referencias"]["b"]["razon"])
        self.assertEqual(salida["diferencia"]["estado"],
                         "NO-CALCULABLE-REFERENCIA")

    def test_selector_ambiguo_no_elige_ultima_fila(self):
        ref = copy.deepcopy(self.contrato["pares"][1]["b"])
        ref["selector"]["clave"] = {"ola": "2024", "familia": "credito"}
        with self.assertRaisesRegex(D.ReferenciaNoResuelta, "resolvio 6 filas"):
            D.resuelve_referencia(ref, C)

    def test_hash_incorrecto_detiene_la_referencia(self):
        ref = copy.deepcopy(self.contrato["pares"][1]["b"])
        ref["sha256"] = "0" * 64
        with self.assertRaisesRegex(D.ReferenciaNoResuelta, "HASH-NO-COINCIDE"):
            D.resuelve_referencia(ref, C)

    def test_totales_no_presentan_cero_materiales_como_coincidencia(self):
        t = self.informe["totales"]
        self.assertEqual(t["pares_examinados"], 3)
        self.assertEqual(t["comparables"], 2)
        self.assertEqual(t["incompatibles"], 1)
        self.assertEqual(t["materiales"], 0)
        self.assertEqual(t["materialidad_no_determinable"], 3)
        self.assertIn("no demuestra coincidencia general",
                      self.informe["lectura_global"].lower())

    def test_salidas_json_tsv_y_humana(self):
        json.loads(json.dumps(self.informe, ensure_ascii=False))
        filas = list(csv.DictReader(io.StringIO(D.como_tsv(self.informe)),
                                   delimiter="\t"))
        self.assertEqual(len(filas), 3)
        self.assertIn("DELTA-REMESAS", D.como_humano(self.informe))
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            rutas = D.escribe_salidas(self.informe, Path(tmp), C)
            self.assertEqual(len(rutas), 3)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},
                             {"delta.json", "delta.tsv", "delta.md"})

    def test_cli_sustituye_stub_y_modo_defecto_no_escribe(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools/corrida0.py"), "delta",
             "--entrada", str(ENTRADA.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Informe de delta explicito", proc.stdout)
        self.assertNotIn("NO-IMPLEMENTADO", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
