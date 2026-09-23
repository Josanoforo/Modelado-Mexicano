"""Controles de integridad del inventario de fuentes del catálogo."""

import csv
import hashlib
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "forense/analisis/catalogo/genera.py"
TABLE = ROOT / "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
PUBLISHER = ROOT / "forense/analisis/catalogo/publica.py"
PRODUCTS = [ROOT / "canon/catalogo-del-mexicano-v1_0.md", ROOT / "canon/catalogo-del-mexicano-v1_0.tsv"]


class CatalogoInventario(unittest.TestCase):
    def test_regeneracion_y_fuentes(self):
        before = hashlib.sha256(TABLE.read_bytes()).digest()
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
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
        self.assertEqual(TABLE.read_bytes(), PRODUCTS[1].read_bytes())
        cover = PRODUCTS[0].read_text()
        self.assertIn("benchmark auditable", cover.lower())
        self.assertIn("consumo pendiente", cover.lower())


if __name__ == "__main__":
    unittest.main()
