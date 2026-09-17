#!/usr/bin/env python3
"""Fixtures focales de intensidad contable de remesas ENIGH 2022."""
from __future__ import annotations

import csv
import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIDOR = ROOT / "data/corrida0/CALC-ENIGH2022-INTENSIDAD-REMESAS-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("enigh22_remint", MEDIDOR)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def _crea_zip(ruta: Path, filas):
    salida = io.StringIO(newline="")
    escritor = csv.writer(salida)
    escritor.writerow(M.COLUMNAS)
    escritor.writerows(filas)
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr(M.MIEMBRO, salida.getvalue().encode("latin-1"))


def _fila(viv, hog, peso, remesa, ingreso, est="E1", upm="U1"):
    return [viv, hog, peso, remesa, ingreso, est, upm]


def _contrato(prevalencia=0.75):
    return {
        "parametros": {
            "bootstrap_replicas": 80,
            "tolerancia_componente_pesos": 0.01,
            "prevalencia_padre": prevalencia,
            "tolerancia_prevalencia": 1e-12,
        },
        "seed": {"aplica": True, "valor": 20260916, "rng": "numpy.PCG64"},
    }


class IntensidadRemesasTest(unittest.TestCase):
    def _mide(self, filas, contrato=None):
        with tempfile.TemporaryDirectory() as td:
            ruta = Path(td) / "fixture.zip"
            _crea_zip(ruta, filas)
            return M.medir(
                {M.ZIP_ID: {"ruta_absoluta": str(ruta)}},
                contrato or _contrato(),
            )

    def test_estimandos_dominios_y_pesos_desiguales(self):
        filas = [
            _fila("V1", "1", 1, 10, 10, upm="U1"),    # razon 1
            _fila("V2", "1", 9, 10, 100, upm="U2"),   # razon .1
            _fila("V3", "1", 5, 0, 50, upm="U3"),     # no receptor
            _fila("V4", "1", 2, 5, 0, upm="U4"),      # y=0, excluido
            _fila("V5", "1", 3, 5, "", upm="U5"),     # y faltante, excluido
        ]
        r = self._mide(filas)

        self.assertEqual(r[M.P + "ESTADO"], "REPORTADO-CON-EXCLUSIONES")
        self.assertEqual(r[M.P + "RECEPTORES-N"], 4)
        self.assertEqual(r[M.P + "RECEPTORES-MASA"], 15.0)
        self.assertAlmostEqual(r[M.P + "PREVALENCIA"], 0.75)
        self.assertEqual(r[M.P + "PREVALENCIA-CONTROL-PADRE"], "REPLICA-RESULTADO")
        self.assertAlmostEqual(r[M.P + "REMESAS-MEDIA"], 125 / 15)
        self.assertEqual(r[M.P + "REMESAS-MEDIANA"], 10.0)

        self.assertEqual(r[M.P + "PARTICIPACION-N"], 2)
        self.assertEqual(r[M.P + "PARTICIPACION-MASA"], 10.0)
        self.assertEqual(r[M.P + "EXCL-INGCOR-CERO-N"], 1)
        self.assertEqual(r[M.P + "EXCL-INGCOR-CERO-MASA"], 2.0)
        self.assertEqual(r[M.P + "EXCL-INGCOR-AUSENTE-NOFINITA-N"], 1)
        self.assertEqual(r[M.P + "EXCL-INGCOR-AUSENTE-NOFINITA-MASA"], 3.0)

        media_razones = (1 * 1.0 + 9 * 0.1) / 10
        razon_masas = (1 * 10 + 9 * 10) / (1 * 10 + 9 * 100)
        self.assertAlmostEqual(r[M.P + "PARTICIPACION-MEDIA-HOGAR"], media_razones)
        self.assertAlmostEqual(r[M.P + "PARTICIPACION-AGREGADA"], razon_masas)
        self.assertNotAlmostEqual(media_razones, razon_masas)
        self.assertAlmostEqual(r[M.P + "PARTICIPACION-GE50"], 0.1)

        # El bootstrap ve las cinco filas/UPM; tres aportan ceros al dominio.
        self.assertEqual(r[M.P + "DISENO-N-FILAS-MARCO"], 5)
        self.assertEqual(r[M.P + "DISENO-N-UPM"], 5)
        self.assertEqual(r[M.P + "DISENO-N-ESTRATOS"], 1)
        self.assertIsNotNone(r[M.P + "PARTICIPACION-MEDIA-HOGAR-IC-LO"])

    def test_mediana_inversa_izquierda_sin_interpolacion(self):
        self.assertEqual(M.mediana_ponderada([20, 10, 30], [1, 1, 2]), 20.0)
        self.assertEqual(M.mediana_ponderada([5, 5, 10], [1, 2, 3]), 5.0)

    def test_llave_de_hogar_duplicada_se_rechaza(self):
        filas = [
            _fila("V1", "1", 1, 10, 20, upm="U1"),
            _fila("V1", "1", 1, 0, 20, upm="U2"),
        ]
        r = self._mide(filas)
        self.assertEqual(r[M.P + "ESTADO"], "NO-ESTIMABLE-LLAVE-NO-UNICA")
        self.assertIsNone(r[M.P + "REMESAS-MEDIA"])

    def test_diseno_incompleto_conserva_puntos_sin_fabricar_ic(self):
        filas = [
            _fila("V1", "1", 1, 10, 20, est="", upm=""),
            _fila("V2", "1", 3, 0, 30, est="E1", upm="U1"),
        ]
        r = self._mide(filas, _contrato(prevalencia=0.25))
        self.assertAlmostEqual(r[M.P + "PARTICIPACION-MEDIA-HOGAR"], 0.5)
        self.assertIsNone(r[M.P + "PARTICIPACION-MEDIA-HOGAR-IC-LO"])
        self.assertEqual(r[M.P + "METODO-IC"], "NO-ESTIMABLE-DISENO-INCOMPLETO")
        self.assertEqual(r[M.P + "DISENO-N-FILAS-MARCO"], 2)
        self.assertEqual(r[M.P + "DISENO-N-SIN-DISENO"], 1)

    def test_nulos_y_negativos_no_se_convierten_en_cero(self):
        filas = [
            _fila("V1", "1", 1, "", 20, upm="U1"),
            _fila("V2", "1", 2, -4, 20, upm="U2"),
            _fila("V3", "1", 3, 0, 20, upm="U3"),
            _fila("V4", "1", 4, 5, 20, upm="U4"),
        ]
        r = self._mide(filas, _contrato(prevalencia=4 / 7))
        self.assertEqual(r[M.P + "N-REMESAS-AUSENTE-NOFINITA"], 1)
        self.assertEqual(r[M.P + "N-REMESAS-NEGATIVA"], 1)
        self.assertEqual(r[M.P + "UNIVERSO-VALIDO-N"], 2)
        self.assertEqual(r[M.P + "RECEPTORES-N"], 1)
        self.assertAlmostEqual(r[M.P + "PREVALENCIA"], 4 / 7)


if __name__ == "__main__":
    unittest.main()
