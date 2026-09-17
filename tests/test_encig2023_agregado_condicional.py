#!/usr/bin/env python3
"""Fixtures focales del agregado condicional ENCIG 2023."""
from __future__ import annotations

import csv
import importlib.util
import io
import tempfile
import zipfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MEDIDOR = ROOT / "data/corrida0/CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("encig23_agcond", MEDIDOR)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def _csv_bytes(cabecera, filas):
    salida = io.StringIO(newline="")
    escritor = csv.writer(salida)
    escritor.writerow(cabecera)
    escritor.writerows(filas)
    return salida.getvalue().encode("latin-1")


def _crea_zip(ruta: Path, sec7, sec8):
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr(M.M_S7, _csv_bytes(M.COLS_S7, sec7))
        zf.writestr(M.M_S8, _csv_bytes(M.COLS_S8, sec8))


def _s7(id_tra, canal, peso, est="E1", upm="U1"):
    # ID_TRA, NT_TIPO, N_TRA, P7_3, FAC_TRA, EST_DIS, UPM_DIS,
    # CVE_ENT, UPM, V_SEL, R_ELE, ID_VIV, ID_PER
    return [id_tra, "1", "01", canal, str(peso), est, upm,
            "01", "001", "1", "1", "V1", "P1"]


def _s8(id_tra, desenlace):
    # ID_TRA, P8_4, ID_VIV, ID_PER, N_TRA, FAC_P18
    return [id_tra, desenlace, "V1", "P1", "01", "999"]


def _contrato():
    return {
        "parametros": {
            "blanco_literal": ["", "b", "NA"],
            "canal_pre": [1],
            "canal_dig": [3, 4, 5],
            "bootstrap_replicas": 80,
        },
        "seed": {"aplica": True, "valor": 20260915, "rng": "numpy.PCG64"},
    }


class AgregadoCondicionalTest(unittest.TestCase):
    def test_pesos_faltante_residuo_y_q(self):
        sec7 = [
            _s7("A", "1", 1, upm="U1"),       # PRE, y=1
            _s7("B", "3", 9, upm="U2"),       # DIG, y=0
            _s7("C", "2", 2, upm="U3"),       # OTRO, y=1
            _s7("D", "1", 100, upm="U4"),     # P8_4 faltante: fuera
            _s7("E", "NA", 3, upm="U5"),      # canal faltante, y=0
        ]
        sec8 = [_s8("A", "1"), _s8("B", "0"), _s8("C", "1"),
                _s8("D", "NA"), _s8("E", "0")]
        with tempfile.TemporaryDirectory() as td:
            ruta = Path(td) / "fixture.zip"
            _crea_zip(ruta, sec7, sec8)
            resultados = M.medir(
                {M.ZIP_ID: {"ruta_absoluta": str(ruta)}}, _contrato()
            )

        # El promedio simple seria 2/4=.5; el estimando ponderado es 3/15=.2.
        self.assertAlmostEqual(resultados[M.P + "PRIMARIO-P"], 0.2)
        self.assertNotEqual(resultados[M.P + "PRIMARIO-P"], 0.5)
        self.assertAlmostEqual(resultados[M.P + "PRIMARIO-Q"], 0.8)
        self.assertEqual(resultados[M.P + "PRIMARIO-N"], 4)
        self.assertEqual(resultados[M.P + "DESENLACE-N-FALTANTE"], 1)
        self.assertAlmostEqual(resultados[M.P + "DESENLACE-COBERTURA-N"], 4 / 5)
        self.assertAlmostEqual(resultados[M.P + "DESENLACE-COBERTURA-MASA"], 15 / 115)

        # El canal OTRO pertenece al primario, pero no al secundario PRE+DIG.
        self.assertEqual(resultados[M.P + "CANAL-OTRO-N"], 1)
        self.assertEqual(resultados[M.P + "CANAL-FALTANTE-N"], 1)
        self.assertAlmostEqual(resultados[M.P + "PREDIG-P"], 0.1)
        self.assertEqual(resultados[M.P + "PREDIG-N"], 2)

        # La descomposicion reconstruye exactamente las masas agregadas.
        suma_den = sum(resultados[M.P + f"CANAL-{g}-MASA-DEN"] for g in M.GRUPOS)
        suma_num = sum(resultados[M.P + f"CANAL-{g}-MASA-NUM"] for g in M.GRUPOS)
        self.assertEqual(suma_den, resultados[M.P + "PRIMARIO-MASA-DEN"])
        self.assertEqual(suma_num, resultados[M.P + "PRIMARIO-MASA-NUM"])

        # q transforma e invierte los extremos del IC de p.
        self.assertAlmostEqual(
            resultados[M.P + "PRIMARIO-IC-Q-LO"],
            1 - resultados[M.P + "PRIMARIO-IC-P-HI"],
        )
        self.assertAlmostEqual(
            resultados[M.P + "PRIMARIO-IC-Q-HI"],
            1 - resultados[M.P + "PRIMARIO-IC-P-LO"],
        )

    def test_multiplicidad_sec8_para_sin_deduplicar(self):
        sec7 = [_s7("A", "1", 1)]
        sec8 = [_s8("A", "1"), _s8("A", "0")]
        with tempfile.TemporaryDirectory() as td:
            ruta = Path(td) / "fixture-duplicada.zip"
            _crea_zip(ruta, sec7, sec8)
            resultados = M.medir(
                {M.ZIP_ID: {"ruta_absoluta": str(ruta)}}, _contrato()
            )
        self.assertEqual(
            resultados[M.P + "ESTADO"],
            "NO-ESTIMABLE-LLAVE-NO-UNICA:SEC8-ID_TRA",
        )
        self.assertIsNone(resultados[M.P + "PRIMARIO-P"])
        self.assertEqual(resultados[M.P + "PRIMARIO-N"], 0)


if __name__ == "__main__":
    unittest.main()
