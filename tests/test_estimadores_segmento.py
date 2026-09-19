"""Contratos mínimos del consumidor segmentado autorizado."""
import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from milpa.src.motor import estimar_segmento


class EstimadoresSegmentoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "tools/marcador_segmento.py"], cwd=ROOT, check=True)

    def test_c2_de_ambos_pilotos_conservan_result_e_ic(self):
        casos = [
            (dict(regla="DIN", desenlace="ahorro_solo_informal", instrumento="ENIF", periodo="2024", ejes={"localidad":"L1", "edad":"E1"}),
             "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001", "RESULT-DIN-LXE8-C2-P-L1xE1"),
            (dict(regla="TRA", desenlace="evade_norma", instrumento="ENVIPE", periodo="2025", ejes={"escolaridad":"S4", "dominio":"D3"}),
             "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001", "RESULT-TRA-SXD12-C2-P-S4xD3"),
        ]
        for consulta, calc, result in casos:
            recibido = estimar_segmento(**consulta)
            fuente = json.loads((ROOT / "data/corrida0" / calc / "resultados.json").read_text())["resultados"]
            self.assertEqual(recibido["fuente"], calc)
            self.assertEqual(recibido["resultado"], result)
            self.assertEqual(recibido["punto"], fuente[result])
            self.assertLess(recibido["ic95"][0], recibido["punto"])
            self.assertGreater(recibido["ic95"][1], recibido["punto"])

    def test_pisos_de_los_tres_instrumentos_y_ausencia(self):
        for consulta in (
            dict(regla="TRA", desenlace="evade_norma", instrumento="ENVIPE", periodo="2025", ejes={"edad":"18-29"}),
            dict(regla="GOB", desenlace="digital_util_sin_coercion", instrumento="ENCIG", periodo="2025", ejes={"sexo":"1"}),
            dict(regla="DIN", desenlace="ahorro_solo_informal", instrumento="ENIF", periodo="2024", ejes={"edad":"18-29"}),
        ):
            recibido = estimar_segmento(**consulta)
            self.assertIsNotNone(recibido)
            self.assertEqual(recibido["incertidumbre"], "IC95-muestral-t-1-no-predictiva")
        self.assertIsNone(estimar_segmento(regla="DIN", desenlace="informal_cualquiera",
                          instrumento="ENIF", periodo="2024", ejes={"edad":"18-29"}))

    def test_derivacion_determinista_y_tsv_sin_cifras_r(self):
        antes = (ROOT / "data/corrida0/marcador-segmento.tsv").read_bytes()
        subprocess.run([sys.executable, "tools/marcador_segmento.py"], cwd=ROOT, check=True)
        self.assertEqual(antes, (ROOT / "data/corrida0/marcador-segmento.tsv").read_bytes())
        self.assertTrue(antes.startswith(b"# DERIVADO"))


if __name__ == "__main__":
    unittest.main()
