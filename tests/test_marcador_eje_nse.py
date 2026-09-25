"""GEN2-CLASE-AMAI-2 · P3: el eje NSE entra al marcador sólo por la firma A4.

Guarda el PARO (c) del encargo: NSE fuera de los instrumentos de A4 no entra.
Los valores salen por id de los CALC sellados, nunca tecleados.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import marcador_segmento as M  # noqa: E402


class TestEjeNse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filas = M.filas_eje_nse()

    def test_solo_instrumentos_de_a4(self):
        self.assertEqual({f["instrumento"] for f in self.filas},
                         {"ENIGH 2022", "ENIF 2024", "ENDUTIH 2023"})
        for fuera in ("ENDUTIH 2024", "ENDUTIH 2025", "ENIF 2021", "ENIGH 2024"):
            self.assertFalse(any(f["instrumento"] == fuera for f in self.filas), fuera)

    def test_valores_por_id_del_calc_sellado(self):
        cache = {}
        for f in self.filas:
            calc = f["fuente"].split(" · ")[0]
            v = cache.setdefault(calc, M._valores_calc(calc))
            base = f["resultado_id"][:-2]
            self.assertEqual(f["R"], v[base + "-P"])
            self.assertEqual(f["R_ic95inf"], v[base + "-IC-LO"])
            self.assertEqual(f["R_ic95sup"], v[base + "-IC-HI"])

    def test_endutih_rotulado_aproximacion_y_celdas_unicas(self):
        for f in self.filas:
            if f["instrumento"] == "ENDUTIH 2023" and f["estado"].startswith("MEDIDA"):
                self.assertIn("APROXIMACION", f["estado"])
        ids = [f["celda_id"] for f in self.filas]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_toca_contadores_de_piso(self):
        d = M.deriva()
        for f in d["filas"]:
            if f["tipo"] == "EJE-NSE":
                self.assertEqual(f["piso_tipo"], "NO-APLICA")
                self.assertNotEqual(f["estado"], "SIN-PISO")
                self.assertEqual(f["M"], "")
        self.assertEqual(sum(d["resumen"]["eje_nse"].values()), len(self.filas))


if __name__ == "__main__":
    unittest.main()
