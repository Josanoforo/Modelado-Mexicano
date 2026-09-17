"""Guardias sintéticas del descriptivo WBES México 2023."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001"
MEDIDOR = CALC / "medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_wbes2023_descriptiva", MEDIDOR)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class Wbes2023DescriptivaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = pd.read_csv(CALC / "fixtures/sintetico.csv")
        MODULE.validate_frame(cls.frame)

    def test_un_positivo_con_otro_faltante_es_positivo_y_no_duplica(self):
        eligibility, outcome = MODULE.classify_composite(self.frame.iloc[0])
        self.assertEqual((eligibility, outcome), ("eligible", "yes"))
        row = MODULE.aggregate(self.frame, None, MODULE.DOMAINS[0])
        self.assertEqual(row["n_si"], "1")

    def test_todos_negativos_observados_son_no(self):
        self.assertEqual(MODULE.classify_composite(self.frame.iloc[1]), ("eligible", "no"))

    def test_negativo_y_otro_aplicable_faltante_es_desconocido(self):
        self.assertEqual(MODULE.classify_composite(self.frame.iloc[2]), ("eligible", "unknown"))

    def test_sin_tramite_no_equivale_a_cero(self):
        self.assertEqual(MODULE.classify_composite(self.frame.iloc[3]), ("not_eligible", None))
        row = MODULE.aggregate(self.frame, None, MODULE.DOMAINS[0])
        self.assertEqual(row["n_sin_interaccion"], "2")
        self.assertEqual(row["n_no"], "2")

    def test_elegibilidad_ambigua_se_separa(self):
        self.assertEqual(MODULE.classify_composite(self.frame.iloc[4]), ("eligibility_unknown", None))
        row = MODULE.aggregate(self.frame, None, MODULE.DOMAINS[0])
        self.assertEqual(row["n_elegibilidad_desconocida"], "1")

    def test_codigos_especiales_del_evento_son_desconocidos(self):
        self.assertEqual(MODULE.classify_composite(self.frame.iloc[6]), ("eligible", "unknown"))

    def test_razon_usa_pesos_desiguales_y_limites(self):
        row = MODULE.aggregate(self.frame, None, MODULE.DOMAINS[0])
        self.assertAlmostEqual(float(row["proporcion_observada"]), 0.5)
        self.assertNotAlmostEqual(float(row["proporcion_observada"]), 1 / 3)
        self.assertAlmostEqual(float(row["limite_inferior_faltantes"]), 10 / 26)
        self.assertAlmostEqual(float(row["limite_superior_faltantes"]), 16 / 26)
        self.assertAlmostEqual(float(row["masa_desconocida_entre_expuestos"]), 6 / 26)

    def test_denominador_vacio_no_se_convierte_en_cero(self):
        frame = self.frame.iloc[[3]].copy()
        row = MODULE.aggregate(frame, None, MODULE.DOMAINS[0])
        self.assertEqual(row["estado"], "DENOMINADOR-VACIO")
        self.assertEqual(row["proporcion_observada"], "")

    def test_conversion_proporcion_porcentaje(self):
        self.assertEqual(MODULE.proportion_to_percent(0.125), 12.5)
        self.assertIsNone(MODULE.proportion_to_percent(None))

    def test_identificador_duplicado_falla(self):
        frame = pd.concat([self.frame, self.frame.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "IDSTD-NO-UNICO"):
            MODULE.validate_frame(frame)


if __name__ == "__main__":
    unittest.main()
