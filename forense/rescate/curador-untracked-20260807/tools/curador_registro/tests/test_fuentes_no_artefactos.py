import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curador import is_real_source


class FuentesNoArtefactosTest(unittest.TestCase):
    def test_semillas_prohibidas(self):
        for value in ["SI", "ESPEJO", "PROCEDENCIA_YAML", "VALIDAR_REGISTRO", "202143006"]:
            with self.subTest(value=value):
                self.assertFalse(is_real_source(value, value))

    def test_archivos_no_son_identidad_de_fuente(self):
        for value in ["algo.py", "nota.md", "tabla.tsv", "paquete.zip"]:
            with self.subTest(value=value):
                self.assertFalse(is_real_source(value, value))

    def test_fuente_real(self):
        self.assertTrue(is_real_source("ENCIG", "Encuesta Nacional de Calidad e Impacto Gubernamental"))


if __name__ == "__main__":
    unittest.main()

