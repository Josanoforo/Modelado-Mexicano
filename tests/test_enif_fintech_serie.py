"""Pruebas sin corpus del estimador ENIF fintech."""
import csv
import importlib.util
import json
import math
import unittest
import xml.etree.ElementTree as ET
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

    def test_tabla_derivada_conserva_resultados_y_rupturas(self):
        result_path = ROOT / "data/corrida0/CALC-ENIF-FINTECH-0001/resultados.json"
        table_path = ROOT / "data/corrida0/enif-fintech-serie-v1_0.tsv"
        results = json.loads(result_path.read_text())["resultados"]
        with table_path.open(newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter="\t"))
        self.assertEqual(len(rows), 29)
        self.assertTrue(all(r["estado"].startswith("NO-ESTIMABLE")
                            for r in rows if r["ola"] == "2018"))
        for row in rows:
            if row["ola"] != "2021":
                continue
            family = row["familia"].upper()
            channel = row["canal"].upper().replace("_", "-")
            prefix = f"RESULT-ENIF-FINTECH-2021-{family}-CANAL-{channel}"
            self.assertEqual(int(row["n_canal"]), results[prefix + "-N"])
            self.assertTrue(math.isclose(float(row["p"]),
                                         results[prefix + "-P"], abs_tol=1e-12))
        account = [r for r in rows if r["familia"] == "cuenta"]
        self.assertTrue(all(r["delta_2024_menos_2021_pp"] == "NO-CALCULAR"
                            for r in account if r["ola"] in {"2021", "2024"}))
        for row21 in (r for r in rows if r["ola"] == "2021" and
                      r["familia"] == "credito"):
            row24 = next(r for r in rows if r["ola"] == "2024" and
                         r["familia"] == "credito" and
                         r["canal"] == row21["canal"])
            expected = (float(row24["p"]) - float(row21["p"])) * 100
            self.assertTrue(math.isclose(
                float(row21["delta_2024_menos_2021_pp"]), expected,
                abs_tol=1e-10))

    def test_figura_es_svg_y_declara_objeto(self):
        figure = ROOT / "data/corrida0/enif-fintech-serie-v1_0.svg"
        root = ET.parse(figure).getroot()
        text = " ".join("".join(node.itertext()) for node in root.iter())
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("2018: NO-ESTIMABLE", text)
        self.assertIn("no canal del producto fintech exacto", text)


if __name__ == "__main__":
    unittest.main()
