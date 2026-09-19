"""Pruebas sintéticas materiales; no abre respuestas reales."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001"
SPEC = importlib.util.spec_from_file_location("issp_redes_medidor", CALC / "medidor.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class IsspRedesApoyoCotidianoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = pd.read_csv(CALC / "fixtures/sintetico.csv")
        cls.result = MODULE.calculate(cls.frame)

    def test_conserva_ceros_y_catalogo_completo(self):
        distribution = self.result[0]
        self.assertEqual(len(distribution), 5 * 3 * 7)
        row = next(r for r in distribution if r["variable"] == "v21" and r["dominio_id"] == "TOTAL" and r["codigo"] == 4)
        self.assertEqual(row["n_numerador"], 0)

    def test_no_puedo_elegir_no_es_ninguno(self):
        coverage = self.result[1]
        row = next(r for r in coverage if r["variable"] == "v21" and r["dominio_id"] == "TOTAL" and r["clasificacion"] == "NO_PUEDE_ELEGIR")
        self.assertEqual(row["n_numerador"], 1)
        none = next(r for r in self.result[0] if r["variable"] == "v21" and r["dominio_id"] == "TOTAL" and r["codigo"] == 7)
        self.assertEqual(none["n_numerador"], 1)

    def test_familia_suma_solo_codigos_uno_y_dos(self):
        distribution, _, families = self.result[:3]
        family = next(r for r in families if r["variable"] == "v21" and r["dominio_id"] == "TOTAL")
        native = sum(r["masa_numerador"] for r in distribution if r["variable"] == "v21" and r["dominio_id"] == "TOTAL" and r["codigo"] in (1, 2))
        self.assertEqual(family["masa_numerador"], native)

    def test_sexo_faltante_permanece_en_total(self):
        controls = self.result[7]
        self.assertEqual(controls["sexo_no_clasificable_n"], 2)
        self.assertTrue(controls["reconstruccion_total_n"])
        self.assertTrue(controls["reconstruccion_total_masa"])

    def test_conteo_casos_completos_y_matriz(self):
        counts, matrix, controls = self.result[4], self.result[6], self.result[7]
        self.assertEqual(sum(r["n_numerador"] for r in counts), controls["n_casos_completos"])
        self.assertEqual(len(matrix), 25)
        self.assertTrue(controls["matriz_simetrica"])
        self.assertTrue(controls["diagonal_marginal"])

    def test_todos_desconocidos_da_denominadores_nulos(self):
        frame = pd.DataFrame({"SEX": [1, 2], "WEIGHT": [1, 1], **{v: [9, None] for v, *_ in MODULE.ITEMS}})
        result = MODULE.calculate(frame)
        self.assertTrue(all(r["proporcion"] is None for r in result[0]))
        self.assertTrue(all(r["n_denominador"] == 0 for r in result[4]))
        self.assertEqual(next(r for r in result[5] if r["indicador"] == "COBERTURA_CASOS_COMPLETOS")["proporcion"], 0)

    def test_precision_no_se_simula(self):
        self.assertEqual(self.result[0][0]["precision"], MODULE.PRECISION)


if __name__ == "__main__":
    unittest.main()
