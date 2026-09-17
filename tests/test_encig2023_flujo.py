import csv
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "data/corrida0/CALC-ENCIG2023-FLUJO-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("encig_flujo", SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
P = M.P


def _csv_bytes(header, rows):
    import io
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue().encode("latin-1")


def _zip(s7, s8, personas):
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    with zipfile.ZipFile(tmp.name, "w") as zf:
        zf.writestr(M.M_S7, _csv_bytes(M.COLS_S7, s7))
        zf.writestr(M.M_S8, _csv_bytes(M.COLS_S8, s8))
        zf.writestr(M.M_PERSONA, _csv_bytes(M.COLS_PERSONA, personas))
    return Path(tmp.name)


class FlujoTest(unittest.TestCase):
    def setUp(self):
        self.personas = [
            ["v1", "p1", 1, 2, 2],
            ["v2", "p2", 2, 2, 2],
            ["v3", "p3", 2, 9, 2],
            ["v4", "p4", 1, 2, 2],
            ["v5", "p5", 2, 2, 2],
        ]
        self.s8 = [
            ["v1", "p1", "t1", "01", 1],
            ["v2", "p2", "t2", "02", ""],
            ["v3", "p3", "t3", "03", ""],
            ["v4", "p4", "t4", "04", ""],
            ["v5", "p5", "t5", "05", 0],
        ]
        self.s7 = [
            ["v1", "p1", "t1", "01", 1, 2],
            ["v1", "p1", "t1", "01", 1, 3],
            ["v2", "p2", "t2", "02", 3, 5],
            ["v3", "p3", "t3", "03", 2, 7],
            ["v4", "p4", "t4", "04", "", 11],
            ["v5", "p5", "t5", "05", 6, 13],
        ]

    def medir(self, s7=None, s8=None, personas=None):
        path = _zip(s7 or self.s7, s8 or self.s8, personas or self.personas)
        self.addCleanup(path.unlink)
        contrato = {"parametros": {"blanco_literal": ["", "b", "NA"]}}
        return M.medir({M.ZIP_ID: {"ruta_absoluta": str(path)}}, contrato)

    def tabla(self, r):
        return {
            (x["grupo"], x["categoria"]): (x["n"], x["masa_fac_tra"])
            for x in json.loads(r[P + "TABLA-CATEGORIAS-JSON"])
        }

    def test_salto_no_es_missing_y_blanco_no_es_cero(self):
        r = self.medir()
        t = self.tabla(r)
        self.assertEqual(t[("TOTAL", "SALTO_NEGATIVO_LOGICO")], (1, 5.0))
        self.assertEqual(t[("TOTAL", "ELEGIBILIDAD_NO_DETERMINABLE")], (1, 7.0))
        self.assertEqual(t[("TOTAL", "RESPUESTA_FALTANTE_APLICABLE")], (1, 11.0))
        self.assertEqual(t[("TOTAL", "CONTRADICCION")], (1, 13.0))
        self.assertEqual(r[P + "PADRE-N-OBSERVADO"], 3)
        self.assertEqual(r[P + "PADRE-N-P84-FALTANTE"], 3)

    def test_respuesta_de_tipo_no_se_repite_como_evento_positivo(self):
        r = self.medir()
        self.assertEqual(r[P + "PADRE-N-TIPOS-POSITIVOS"], 1)
        self.assertEqual(r[P + "PADRE-N-TIPOS-POSITIVOS-REPETIDOS"], 1)
        self.assertEqual(r[P + "N-POSITIVO-CONOCIDO"], 0)
        self.assertEqual(r[P + "N-POSITIVO-LIM-INF"], 1)
        self.assertEqual(r[P + "W-POSITIVO-LIM-INF"], 2.0)
        self.assertEqual(r[P + "W-POSITIVO-LIM-SUP"], 36.0)

    def test_categorias_y_canales_cierran(self):
        r = self.medir()
        t = self.tabla(r)
        self.assertEqual(r[P + "CATEGORIAS-CIERRE-N"], "CIERRA")
        self.assertEqual(r[P + "CATEGORIAS-CIERRE-MASA"], "CIERRA")
        self.assertEqual(sum(t[("TOTAL", c)][0] for c in M.CATEGORIAS), 6)
        for grupo in M.GRUPOS[1:]:
            esperado = sum(1 for x in self.s7 if M._canal(M._codigo(x[4], {"", "b", "NA"})) == grupo)
            self.assertEqual(sum(t[(grupo, c)][0] for c in M.CATEGORIAS), esperado)

    def test_limites_contienen_asignaciones_extremas_y_no_son_ic(self):
        r = self.medir()
        self.assertLessEqual(r[P + "P-LIM-INF"], r[P + "P-LIM-SUP"])
        self.assertEqual(r[P + "W-POSITIVO-LIM-INF"], 2.0)
        self.assertEqual(r[P + "W-POSITIVO-LIM-SUP"], r[P + "W-UNIVERSO"] - r[P + "W-NEGATIVO-CONOCIDO"])
        self.assertEqual(r[P + "PRECISION-MUESTRAL"], "NO-CALCULADA")

    def test_union_persona_muchos_a_uno_sin_multiplicacion(self):
        r = self.medir()
        self.assertEqual(r[P + "JOIN-ESTADO"], "JOIN-EXACTO-SIN-MULTIPLICACION")
        self.assertEqual(r[P + "JOIN-N-EVENTOS-PERSONA"], len(self.s7))
        duplicadas = self.personas + [self.personas[0]]
        r2 = self.medir(personas=duplicadas)
        self.assertEqual(r2[P + "ESTADO"], "NO-ESTIMABLE-PERSONA-NO-UNICA")

    def test_fuera_universo_permanece_cero(self):
        r = self.medir()
        self.assertEqual(self.tabla(r)[("TOTAL", "FUERA_UNIVERSO_NO_APLICA")], (0, 0.0))


if __name__ == "__main__":
    unittest.main()
