"""Contrato mínimo del dominio poblacional de CALC-ENIF-0002, sin corpus."""
import csv
import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RUTA = ROOT / "data/corrida0/CALC-ENIF-0002/medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_enif_poblacion", RUTA)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class EnifPoblacionTest(unittest.TestCase):
    def test_saltos_no_confunden_blanco_con_no_trabajador(self):
        no_trabaja = {"P3_8": "5", "P3_9": "7", "P3_13": "b"}
        sin_pago = {"P3_8": "5", "P3_9": "1", "P3_13": "b"}
        directo = {"P3_8": "8", "P3_9": "b", "P3_13": "b"}
        self.assertTrue(M._no_trabaja(no_trabaja))
        self.assertFalse(M._trabaja(no_trabaja))
        self.assertTrue(M._trabaja(sin_pago))
        self.assertFalse(M._no_trabaja(sin_pago))
        self.assertEqual(M._celda({**sin_pago, "P4_10": "5"}),
                         "TRABAJA-RESIDUAL")
        self.assertTrue(M._no_trabaja(directo))

    def test_numeradores_pesos_particion_y_no_respuesta(self):
        cols = M.COLS
        filas = [
            ["1", "b", "1", "1", "1", "1", "001", "00001"],
            ["2", "b", "2", "7", "3", "2", "001", "00002"],
            ["5", "7", "b", "b", "2", "3", "002", "00003"],
            ["5", "1", "6", "b", "5", "4", "002", "00004"],
            ["8", "b", "b", "b", "1", "5", "003", "00005"],
            ["6", "7", "b", "b", "8", "6", "003", "00006"],
        ]
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            zpath = td / "enif.zip"
            sio = io.StringIO()
            w = csv.writer(sio, lineterminator="\n")
            w.writerow(cols)
            w.writerows(filas)
            with zipfile.ZipFile(zpath, "w") as zf:
                zf.writestr("TMODULO.csv", sio.getvalue())
            previo = td / "previo.json"
            previo.write_text(json.dumps({"resultados": M.REUSO_ESPERADO}),
                              encoding="utf-8")
            r = M.medir({
                M.ZIP_ID: {"ruta_absoluta": str(zpath)},
                M.REUSO_ID: {"ruta_absoluta": str(previo)},
            }, {})
        p = M.P
        self.assertEqual(r[p + "G-PARTICION-ACTIVIDAD"],
                         "EXHAUSTIVA-Y-DISJUNTA")
        self.assertEqual(r[p + "M-NO-TRABAJA-N"], 2)
        self.assertEqual(r[p + "M-NO-TRABAJA-PESO"], 8.0)
        self.assertEqual(r[p + "M-TRABAJA-RESIDUAL-N"], 1)
        self.assertEqual(r[p + "M-P410-FALTANTE-N"], 1)
        self.assertEqual(r[p + "M-COBERTURA-P410-VALIDO"], round(15 / 21, 6))
        self.assertEqual(r[p + "P-CORTO-NO-TRABAJA-P"], 1.0)
        self.assertEqual(r[p + "P-CORTO-TRABAJA-RESIDUAL-P"], 0.0)
        self.assertEqual(r[p + "P-CORTO-POBLACION-18MAS-P"], 0.6)
        self.assertEqual(r[p + "G-PARTICION-PESO-DELTA"], 0.0)
        declarados = {x["id"] for x in yaml.safe_load(
            (ROOT / "data/corrida0/CALC-ENIF-0002/spec.yaml").read_text(
                encoding="utf-8"))["resultados"]}
        self.assertEqual(set(r), declarados)


if __name__ == "__main__":
    unittest.main()
