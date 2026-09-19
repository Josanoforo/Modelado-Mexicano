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
            (dict(regla="DIN", desenlace="ahorro_solo_informal", instrumento="ENIF", periodo="2024", universo="persona", ejes={"localidad":"L1", "edad":"E1"}),
             "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001", "RESULT-DIN-LXE8-C2-P-L1xE1"),
            (dict(regla="TRA", desenlace="evade_norma", instrumento="ENVIPE", periodo="2025", universo="persona", ejes={"escolaridad":"S4", "dominio":"D3"}),
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

    def test_pisos_corregidos_de_cada_instrumento(self):
        casos = [
            (dict(regla="GOB", desenlace="digital_util_sin_coercion", instrumento="ENCIG",
                  periodo="2025", universo="evento_tramite_comparable", ejes={"sexo": "1"}),
             "CALC-PISOS-ENCIG2023-EJES-0002", 0.5780492513486944, 10407),
            (dict(regla="DIN", desenlace="ahorro_solo_informal", instrumento="ENIF",
                  periodo="2024", universo="persona_elegida_18_mas",
                  ejes={"localidad": "menos-15000"}),
             "CALC-PISOS-ENIF2021-EJES-0002", 0.42350079209783514, 4989),
            (dict(regla="TRA", desenlace="evade_norma", instrumento="ENVIPE",
                  periodo="2025", universo="delito_con_bp1_20_valido", ejes={"edad": "60-mas"}),
             "CALC-PISOS-ENVIPE2024-EJES-0002", 0.5480025499040757, 4337),
            (dict(regla="CIV", desenlace="denuncia", instrumento="ENVIPE",
                  periodo="2025", universo="delito_robo_total_vehiculo",
                  ejes={"cobertura_seguro": "asegurado"}),
             "CALC-PISOS-ENVIPE2024-EJES-0002", 0.7740559546028694, 375),
        ]
        for consulta, calc, punto, n in casos:
            recibido = estimar_segmento(**consulta)
            self.assertEqual(recibido["fuente"], calc)
            self.assertEqual(recibido["punto"], punto)
            self.assertEqual(recibido["n"], n)
            self.assertEqual(recibido["estados"]["consumo"], "ACTIVO")

    def test_ausencia_no_cae_a_nacional_ni_a_otro_desenlace_o_universo(self):
        base = dict(regla="DIN", desenlace="ahorro_solo_informal", instrumento="ENIF",
                    periodo="2024", universo="persona_elegida_18_mas")
        self.assertIsNone(estimar_segmento(**base, ejes={"edad":"97-mas"}))
        self.assertIsNone(estimar_segmento(**dict(base, universo="persona"),
                                           ejes={"edad":"18-29"}))
        self.assertIsNone(estimar_segmento(regla="DIN", desenlace="informal_cualquiera",
                          instrumento="ENIF", periodo="2024", universo="persona_elegida_18_mas",
                          ejes={"edad":"18-29"}))

    def test_conteos_derivados_y_guardias_de_result(self):
        mapa = json.loads(json.dumps(__import__("yaml").safe_load(
            (ROOT / "milpa/estimadores-por-segmento.yaml").read_text())))
        estimadores = mapa["estimadores"]
        self.assertEqual(len(estimadores), 59)
        self.assertEqual(len({e["fuente"]["punto"] for e in estimadores}), 59)
        self.assertEqual(sum(e["tipo"] == "cruce" for e in estimadores), 20)
        self.assertEqual(sum(e["tipo"] == "marginal" for e in estimadores), 39)
        for entrada in estimadores:
            punto = entrada["fuente"]["punto"]
            self.assertNotIn("P-REDERIVADO", punto)
            self.assertNotIn("IC95", punto)
            self.assertNotIn("ARBITRO", entrada["fuente"]["calc"])

    def test_derivacion_determinista_y_tsv_sin_cifras_r(self):
        antes = (ROOT / "data/corrida0/marcador-segmento.tsv").read_bytes()
        subprocess.run([sys.executable, "tools/marcador_segmento.py"], cwd=ROOT, check=True)
        self.assertEqual(antes, (ROOT / "data/corrida0/marcador-segmento.tsv").read_bytes())
        self.assertTrue(antes.startswith(b"# DERIVADO"))


if __name__ == "__main__":
    unittest.main()
