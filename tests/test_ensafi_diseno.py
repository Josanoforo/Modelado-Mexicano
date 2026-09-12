import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIDOR = ROOT / "data/corrida0/CALC-ENSAFI-DISENO-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("ensafi_diseno_medidor", MEDIDOR)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


def row(h, u, exposure, response, weight=1):
    return {
        "EST_DIS": h,
        "UPM_DIS": u,
        "FAC_HOG": str(weight),
        "X": exposure,
        "Y": response,
    }


CFG = {
    "code": "TEST",
    "table": "THOGAR.csv",
    "weight": "FAC_HOG",
    "exposure": "X",
    "response": "Y",
}


class EnsafiDisenoTest(unittest.TestCase):
    def test_dominio_conserva_psu_fuera_del_dominio(self):
        rows = [
            row("A", "1", "1", "1", 2),
            row("A", "2", "2", "", 4),
            row("B", "1", "1", "2", 1),
            row("B", "2", "2", "", 3),
        ]
        result = MOD._estimate(rows, CFG)
        self.assertEqual(result["n_exposed"], 2)
        self.assertEqual(result["n_valid"], 2)
        self.assertAlmostEqual(result["p"], 2 / 3)
        self.assertEqual(result["df"], 2)
        self.assertIn("DISPONIBLE", result["precision_status"])

    def test_desconocido_sale_del_denominador_y_conserva_masa(self):
        rows = [
            row("A", "1", "1", "1", 2),
            row("A", "2", "1", "9", 5),
            row("B", "1", "1", "2", 1),
            row("B", "2", "2", "", 3),
        ]
        result = MOD._estimate(rows, CFG)
        self.assertEqual(result["n_exposed"], 3)
        self.assertEqual(result["n_valid"], 2)
        self.assertEqual(result["n_unknown"], 1)
        self.assertEqual(result["unknown_mass"], 5)
        self.assertEqual(result["denominator"], 3)

    def test_frontera_no_se_publica_como_precision_cero(self):
        rows = [
            row("A", "1", "1", "1"),
            row("A", "2", "1", "1"),
            row("B", "1", "2", ""),
            row("B", "2", "2", ""),
        ]
        result = MOD._estimate(rows, CFG)
        self.assertEqual(result["p"], 1.0)
        self.assertIsNone(result["se"])
        self.assertEqual(result["precision_status"], "NO-DISPONIBLE:FRONTERA-P-0-O-1")

    def test_denominador_nulo_es_no_estimable(self):
        result = MOD._estimate([row("A", "1", "2", "")], CFG)
        self.assertIsNone(result["p"])
        self.assertIsNone(result["se"])
        self.assertEqual(result["precision_status"], "NO-DISPONIBLE:DENOMINADOR-NULO")

    def test_upm_se_anida_en_estrato(self):
        rows = [
            row("A", "1", "1", "1"), row("A", "2", "1", "2"),
            row("B", "1", "1", "1"), row("B", "3", "1", "2"),
        ]
        profile = MOD._design_profile(rows, "FAC_HOG")
        self.assertEqual(profile["n_strata"], 2)
        self.assertEqual(profile["n_psu_nested"], 4)
        self.assertEqual(profile["n_psu_cross_strata"], 1)
        self.assertEqual(profile["df"], 2)


if __name__ == "__main__":
    unittest.main()
