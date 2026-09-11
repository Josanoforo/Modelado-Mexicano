"""Pruebas sin corpus del estimador ENIF fintech."""
import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/corrida0/CALC-ENIF-FINTECH-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_enif_fintech", PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class EnifFintechSerieTest(unittest.TestCase):
    def test_mapas_de_canal_no_reutilizan_codigos_2024(self):
        self.assertEqual(M.CATEGORIAS["CUENTA"]["mapa"]["2"], "APP-CELULAR")
        self.assertEqual(M.CATEGORIAS["CUENTA"]["mapa"]["6"], "EMPLEADOR")
        self.assertEqual(M.CATEGORIAS["CREDITO"]["mapa"]["5"], "PROMOTOR")
        self.assertNotIn("7", M.CATEGORIAS["CREDITO"]["mapa"])

    def test_linealizacion_de_dominio_y_especiales(self):
        rows = []
        channels = ["1", "2", "2", "9", ""]
        weights = [1.0, 2.0, 3.0, 4.0, 5.0]
        for i, (channel, weight) in enumerate(zip(channels, weights), start=1):
            rows.append(({
                "P5_4_8": "1", "P5_17": channel,
                "P6_2_8": "2", "P6_7": "",
                "FAC_ELE": str(weight), "EST_DIS": "001",
                "UPM_DIS": f"{i:07d}", "EDAD": "30",
            }, weight))
        domain = lambda row: row["P5_4_8"] == "1" and row["P5_17"] in set("1234567")
        result = M._prop_dominio(rows, domain, lambda row: row["P5_17"] == "2")
        self.assertEqual(result["n_den"], 3)
        self.assertEqual(result["n_num"], 2)
        self.assertEqual(result["mass_den"], 6.0)
        self.assertEqual(result["mass_num"], 5.0)
        self.assertTrue(math.isclose(result["p"], 5 / 6))
        self.assertEqual(result["n_strata"], 1)
        self.assertEqual(result["n_psu"], 5)

    def test_estimador_srs_reproduce_formula(self):
        rows = []
        ys = [0, 0, 1, 1]
        for i, y in enumerate(ys, start=1):
            rows.append(({
                "EST_DIS": "001", "UPM_DIS": str(i), "d": str(y)
            }, 1.0))
        result = M._prop_dominio(rows, lambda row: True,
                                  lambda row: row["d"] == "1")
        self.assertTrue(math.isclose(result["p"], 0.5))
        self.assertTrue(math.isclose(result["se"], math.sqrt(0.25 / 3)))


if __name__ == "__main__":
    unittest.main()
