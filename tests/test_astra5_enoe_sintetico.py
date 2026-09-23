"""Oro sintético: empleo informal, sector informal y desaliento son distintos."""
import csv
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.dominios.enoe.pisos import medir_ola


class EnosSintetico(unittest.TestCase):
    def test_terminos_y_denominadores(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "ola.zip"
            campos = ["r_def", "c_res", "eda", "sex", "fac", "est_d", "upm",
                      "ent", "t_loc", "niv_ins", "clase1", "clase2", "emp_ppal",
                      "tue_ppal", "sub_o", "busqueda", "pnea_est", "hrsocup",
                      "ingocup", "t_tra"]
            import io
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=campos)
            w.writeheader()
            for i in range(400):
                ocupado = i < 200
                w.writerow({"r_def": "00", "c_res": "1", "eda": "30", "sex": "1",
                            "fac": "1", "est_d": "1", "upm": str(i // 50 + 1),
                            "ent": "1", "t_loc": "1", "niv_ins": "3",
                            "clase1": "1" if ocupado else "2",
                            "clase2": "1" if ocupado else "3",
                            "emp_ppal": "1" if ocupado and i < 100 else ("2" if ocupado else ""),
                            "tue_ppal": "1" if ocupado and i < 50 else ("2" if ocupado else ""),
                            "sub_o": "1" if ocupado and i < 40 else "",
                            "busqueda": "1" if ocupado and i < 20 else ("2" if ocupado else ""),
                            "pnea_est": "1" if not ocupado and i < 250 else ("4" if not ocupado else ""),
                            "hrsocup": "40" if ocupado else "",
                            "ingocup": "1000" if ocupado else "",
                            "t_tra": "2" if ocupado and i < 10 else ("1" if ocupado else "")})
            with zipfile.ZipFile(ruta, "w") as z:
                z.writestr("SDEMT123.csv", buf.getvalue().encode("latin-1"))
            filas, base, leidas = medir_ola(ruta, "2019T1", "clasica", 60, 42)
            self.assertEqual((base, leidas), (400, 400))
            por = {r["conducta"]: r for r in filas if r["eje"] == "nacional"}
            self.assertAlmostEqual(por["empleo_informal"]["punto"], .5)
            self.assertAlmostEqual(por["sector_informal"]["punto"], .25)
            self.assertAlmostEqual(por["subocupacion"]["punto"], .2)
            self.assertAlmostEqual(por["desaliento_desistio"]["punto"], .25)
            self.assertAlmostEqual(por["no_participacion_obligaciones"]["punto"], .75)
            self.assertEqual(por["horas_ocupado"]["punto"], 40)
            self.assertEqual(por["ingreso_ocupado_nominal"]["punto"], 1000)


if __name__ == "__main__":
    unittest.main()
