"""Pruebas sintéticas del descriptivo ISSP; no abre microdatos reales."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-ISSP2017-APOYO-MONETARIO-0001"
SPEC = importlib.util.spec_from_file_location("issp_medidor", CALC / "medidor.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class IsspApoyoMonetarioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = pd.read_csv(CALC / "fixtures/sintetico.csv")
        cls.frame = raw.loc[raw["c_alphan"].eq("MX")].copy()
        for col in ("SEX", "AGE", "WEIGHT", "v26"):
            cls.frame[col] = pd.to_numeric(cls.frame[col], errors="coerce")
        cls.distribution, cls.coverage, cls.contrast, cls.controls = MODULE.calculate(cls.frame)

    def row(self, domain, code):
        return next(row for row in self.distribution if row["dominio_id"] == domain and row["codigo"] == code)

    def test_siete_categorias_por_tres_dominios_incluyen_ceros(self):
        self.assertEqual(len(self.distribution), 21)
        self.assertEqual(self.row("TOTAL", 6)["n_categoria"], 0)

    def test_razon_ponderada_usa_solo_respuestas_validas(self):
        self.assertAlmostEqual(self.row("TOTAL", 1)["proporcion"], 5 / 6)
        self.assertEqual(self.row("TOTAL", 1)["n_denominador_valido"], 3)

    def test_codigo_siete_es_sustantivo(self):
        self.assertAlmostEqual(self.row("HOMBRES", 7)["proporcion"], 1 / 3)

    def test_no_puede_elegir_y_no_respuesta_separados(self):
        rows = {row["clasificacion"]: row for row in self.coverage if row["dominio_id"] == "TOTAL"}
        self.assertEqual(rows["NO_PUEDE_ELEGIR"]["n"], 1)
        self.assertEqual(rows["NO_RESPUESTA"]["n"], 2)

    def test_peso_invalido_tiene_prioridad_y_sin_masa(self):
        row = next(row for row in self.coverage if row["dominio_id"] == "TOTAL" and row["clasificacion"] == "PESO_INVALIDO")
        self.assertEqual(row["n"], 1)
        self.assertIsNone(row["masa"])

    def test_contraste_mujeres_menos_hombres(self):
        self.assertAlmostEqual(self.contrast[0]["diferencia_menos_mas"], 1 - 2 / 3)

    def test_particion_reconciliacion_y_reconstruccion(self):
        self.assertTrue(self.controls["particiones_suman_uno"])
        self.assertTrue(self.controls["reconciliacion_elegibles"])
        self.assertTrue(self.controls["reconstruccion_total_masa"])

    def test_denominador_nulo_permanece_nulo(self):
        frame = self.frame.loc[self.frame["SEX"].eq(2)].copy()
        frame["v26"] = 8
        distribution, _, contrast, _ = MODULE.calculate(frame)
        row = next(item for item in distribution if item["dominio_id"] == "TOTAL" and item["codigo"] == 1)
        self.assertIsNone(row["proporcion"])
        self.assertEqual(row["estado"], "DENOMINADOR-NULO")
        self.assertIsNone(contrast[0]["diferencia_menos_mas"])

    def test_precision_no_se_simula(self):
        self.assertEqual(self.row("TOTAL", 1)["precision"], MODULE.PRECISION)


if __name__ == "__main__":
    unittest.main()
