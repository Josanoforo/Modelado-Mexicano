"""Regresión del fallo real 2025T3: CVE_ENT."""
import csv
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.dominios.enoe.pisos_v1_2 import medir_ola


class BomYLocalidad(unittest.TestCase):
    def test_entidad_renombrada(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "enoen.zip"
            buf = io.StringIO()
            cols = ["r_def", "c_res", "eda", "sex", "fac_tri", "est_d_tri",
                    "upm", "cve_ent", "t_loc_tri", "niv_ins", "clase1", "clase2",
                    "emp_ppal", "tue_ppal", "sub_o", "busqueda", "pnea_est",
                    "hrsocup", "ingocup", "t_tra", "tip_con", "remune2c"]
            writer = csv.DictWriter(buf, fieldnames=cols)
            writer.writeheader()
            for i in range(400):
                writer.writerow({"r_def": "00", "c_res": "1", "eda": "30", "sex": "2",
                                 "fac_tri": "1", "est_d_tri": "1", "upm": str(i // 50),
                                 "cve_ent": "2", "t_loc_tri": "4", "niv_ins": "3",
                                 "clase1": "1", "clase2": "1", "emp_ppal": "1",
                                 "tue_ppal": "1", "sub_o": "", "busqueda": "2",
                                 "pnea_est": "", "hrsocup": "40", "ingocup": "1000",
                                 "t_tra": "1", "tip_con": "1", "remune2c": "1"})
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("ENOEN_SDEMT222.csv", b"\xef\xbb\xbf" + buf.getvalue().encode())
            filas, base, _ = medir_ola(path, "2025T3", "pos2023", 40, 42)
            self.assertEqual(base, 400)
            rural = [r for r in filas if r["conducta"] == "empleo_informal"
                     and r["eje"] == "localidad"]
            self.assertEqual(len(rural), 1)
            self.assertEqual(rural[0]["segmento"], "MENOS-2K5")
            self.assertEqual(rural[0]["punto"], 1.0)
            ent = [r for r in filas if r["conducta"] == "empleo_informal" and r["eje"] == "entidad"]
            self.assertEqual(ent[0]["segmento"], "02")


if __name__ == "__main__":
    unittest.main()
