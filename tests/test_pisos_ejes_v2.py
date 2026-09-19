"""Controles unitarios de las correspondencias corregidas de los pisos."""
import unittest

import pandas as pd

from tools.pisos_ejes_v2 import _edad, _escolaridad


class PisosEjesV2Test(unittest.TestCase):
    def test_edad_excluye_sentinelas_y_limita_60_mas_a_96(self):
        valores = pd.Series([17, 18, 29, 30, 44, 45, 59, 60, 96, 97, 98, 99, ""])
        recibido = _edad(valores).astype("string").fillna("AUSENTE").tolist()
        self.assertEqual(recibido, [
            "AUSENTE", "18-29", "18-29", "30-44", "30-44", "45-59",
            "45-59", "60+", "60+", "AUSENTE", "AUSENTE", "AUSENTE",
            "AUSENTE",
        ])
        self.assertNotIn("nan", recibido)

    def test_escolaridad_usa_las_cuatro_categorias_selladas(self):
        valores = pd.Series(["00", "1", "2", "3", "4", "5", "6", "7",
                             "8", "9", "10", "11", "12", "99", ""])
        recibido = _escolaridad(valores).astype("string").fillna("AUSENTE").tolist()
        self.assertEqual(recibido, [
            "hasta_primaria", "hasta_primaria", "hasta_primaria", "secundaria",
            "media_superior", "media_superior", "media_superior", "media_superior",
            "superior", "superior", "superior", "superior", "AUSENTE",
            "AUSENTE", "AUSENTE",
        ])


if __name__ == "__main__":
    unittest.main()
