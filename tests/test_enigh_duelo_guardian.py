#!/usr/bin/env python3
"""Prueba del guardián de ENIGH 2024 (`tools/enigh_duelo_guardian.py`),
único código autorizado a tocar la ola reservada antes de COMMIT-3 (E.6).

D-22: corre sobre un ZIP SINTÉTICO fabricado en memoria -- cero microdato de
ENIGH 2024, cero lectura del zip real (ni siquiera para hashear: eso lo
prueba el propio `run` de `corrida0.py` con el input declarado). Verifica
que la guardia realmente bloquea, no solo que el cálculo da un número
razonable: si `nacional()` no lanzara `ReservaRota` sobre `reservada=True`,
este test lo atraparía y no la lectura de la spec.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import os
import sys
import tempfile
import unittest
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _carga(path):
    spec = importlib.util.spec_from_file_location("enigh_duelo_guardian", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


G = _carga(os.path.join(RAIZ, "tools", "enigh_duelo_guardian.py"))

MIEMBRO = "sintetico/concentradohogar.csv"


def _zip_sintetico(ruta, filas, columnas_extra=()):
    """filas: lista de (folioviv, foliohog, factor, remesas, est_dis, upm)."""
    buf = io.StringIO()
    cab = list(G.COLUMNAS) + list(columnas_extra)
    w = csv.writer(buf)
    w.writerow(cab)
    for f in filas:
        fila = list(f) + ["x"] * len(columnas_extra)
        w.writerow(fila)
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr(MIEMBRO, buf.getvalue())


class GuardianSintetico(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        self.tmp.close()
        # 10 hogares, 2 UPM x 2 estratos; 3 receptores (factor 100 c/u),
        # 7 no receptores (factor 100 c/u) -> p = 300/1000 = 0.3
        filas = []
        for i in range(10):
            est = "001" if i < 5 else "002"
            upm = "A" if i % 2 == 0 else "B"
            remesa = "500" if i < 3 else "0"
            filas.append((f"{i:010d}", "1", "100", remesa, est, upm))
        _zip_sintetico(self.tmp.name, filas)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_carga_solo_columnas_declaradas(self):
        m = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=False)
        self.assertEqual(len(m.filas), 10)
        self.assertEqual(set(m.filas[0]), set(G.COLUMNAS))

    def test_nacional_da_la_proporcion_correcta(self):
        m = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=False)
        r = G.nacional(m)
        self.assertEqual(r["estado"], "REPORTADO")
        self.assertAlmostEqual(r["p"], 0.3, places=9)
        self.assertEqual(r["n_validos"], 10)

    def test_nacional_bloquea_marco_reservado(self):
        m = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=True)
        with self.assertRaises(G.ReservaRota):
            G.nacional(m)

    def test_emite_bajo_reserva_exige_ambos(self):
        m_reservado = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=True)
        m_libre = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=False)

        # reservada=True + autoriza=True -> funciona
        r = G.emite_bajo_reserva(m_reservado, autoriza=True)
        self.assertEqual(r["estado"], "REPORTADO")

        # reservada=True + autoriza=False -> ReservaRota
        with self.assertRaises(G.ReservaRota):
            G.emite_bajo_reserva(m_reservado, autoriza=False)

        # reservada=False + autoriza=True -> ValueError (no hace falta autorizar)
        with self.assertRaises(ValueError):
            G.emite_bajo_reserva(m_libre, autoriza=True)

    def test_huella_detecta_marco_alterado(self):
        m = G.carga_hogares(self.tmp.name, MIEMBRO, reservada=False)
        alterado = G.MarcoHogares(
            filas=m.filas[:-1],  # se quita una fila -- "filtrar" el marco
            reservada=m.reservada, huella=m.huella)  # huella VIEJA, no recalculada
        with self.assertRaises(G.ReservaRota):
            G._calcula_nacional(alterado)

    def test_columna_ausente_falla_alto(self):
        buf_ruta = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        buf_ruta.close()
        try:
            with zipfile.ZipFile(buf_ruta.name, "w") as zf:
                zf.writestr(MIEMBRO, "folioviv,foliohog\n0000000001,1\n")
            with self.assertRaises(ValueError):
                G.carga_hogares(buf_ruta.name, MIEMBRO, reservada=False)
        finally:
            os.unlink(buf_ruta.name)


if __name__ == "__main__":
    unittest.main()
