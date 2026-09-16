"""Guardias dirigidas para la extracción descriptiva ENCRIGE 2020."""
from __future__ import annotations

import importlib.util
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIDOR = ROOT / "data/corrida0/CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_encrige_descriptiva", MEDIDOR)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class EncrigeDescriptivaTest(unittest.TestCase):
    def test_tasa_por_10000_no_se_confunde_con_porcentaje(self):
        self.assertEqual(
            MODULE.normaliza_tasa_por_10000(Decimal("509.853592479729")),
            Decimal("0.0509853592479729"),
        )
        self.assertNotEqual(
            MODULE.normaliza_tasa_por_10000(Decimal("509.853592479729")),
            Decimal("5.09853592479729"),
        )

    def test_formula_admite_redondeo_publicado_y_rechaza_escala_erronea(self):
        delta = MODULE._assert_rate(
            Decimal("204284.532"),
            Decimal("4006729.2849"),
            Decimal("509.853592479729"),
            "sintetico",
        )
        self.assertLessEqual(delta, MODULE.RATE_TOLERANCE)
        with self.assertRaisesRegex(ValueError, "TASA-INCONSISTENTE"):
            MODULE._assert_rate(
                Decimal("204284.532"),
                Decimal("4006729.2849"),
                Decimal("5.09853592479729"),
                "sintetico-escala-mal",
            )


if __name__ == "__main__":
    unittest.main()
