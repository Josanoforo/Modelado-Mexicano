"""Controles de integridad del inventario de fuentes del catálogo."""

import csv
import hashlib
import os
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "forense/analisis/catalogo/genera_catalogo.py"
TABLE = ROOT / "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
PUBLISHER = ROOT / "forense/analisis/catalogo/publica.py"
# Vista con que se congeló v1_0 (último commit de main que tocó las vistas
# antes del primer `[deriva]` posterior al congelamiento). El canal de
# derivados reemplaza la vista; v1_0 no se regenera con ella.
VISTA_CONGELADA = "3e3a85a6a1339944f28f03b27d0c67576cff671b"
ENV = {**os.environ, "CATALOGO_VISTA_REF": VISTA_CONGELADA}
PRODUCTS = [ROOT / "canon/catalogo-del-mexicano-v1_0.md", ROOT / "canon/catalogo-del-mexicano-v1_0.tsv"]


class CatalogoInventario(unittest.TestCase):
    def test_regeneracion_y_fuentes(self):
        before = hashlib.sha256(TABLE.read_bytes()).digest()
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, env=ENV)
        self.assertEqual(before, hashlib.sha256(TABLE.read_bytes()).digest())
        with TABLE.open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(rows), len({row["llave"] for row in rows}))
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["llave"], row["result_punto"])
            self.assertTrue(row["calc"].startswith("CALC-"))
            self.assertEqual(len(row["sha256_resultados"]), 64)
            self.assertEqual(bool(row["result_inf"]), bool(row["result_sup"]))
            if row["oferta_compatible"].startswith("RESULT-"):
                self.assertTrue(row["oferta_valor_ic"])
            if row["naturaleza_ic"] == "SIN-IC-IDENTIFICADO":
                self.assertFalse(row["ic95_inf"] or row["ic95_sup"])

    def test_producto_regenera_y_no_sobredeclara_adopcion(self):
        before = [hashlib.sha256(path.read_bytes()).digest() for path in PRODUCTS]
        subprocess.run([sys.executable, str(PUBLISHER)], cwd=ROOT, check=True)
        self.assertEqual(before, [hashlib.sha256(path.read_bytes()).digest() for path in PRODUCTS])
        with TABLE.open(newline="") as source, PRODUCTS[1].open(newline="") as product:
            src_rows = list(csv.DictReader(source, delimiter="\t"))
            dst_rows = list(csv.DictReader(product, delimiter="\t"))
        self.assertEqual(len(src_rows), len(dst_rows))
        self.assertEqual(
            src_rows,
            [{k: v for k, v in row.items() if k != "area_consulta"} for row in dst_rows],
        )
        self.assertTrue(all(row["area_consulta"] for row in dst_rows))
        cover = PRODUCTS[0].read_text()
        self.assertIn("benchmark auditable", cover.lower())
        self.assertIn("consumo pendiente", cover.lower())


if __name__ == "__main__":
    unittest.main()
