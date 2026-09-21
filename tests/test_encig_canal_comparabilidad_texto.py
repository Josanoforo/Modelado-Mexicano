#!/usr/bin/env python3
"""Test de forma de `data/encig-canal-comparabilidad-texto-v1_0.tsv`.

ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026), pieza P1. La tabla dice,
ola por ola (ENCIG 2015–2025), si el reactivo 7.3 sobre el pago ordinario de
luz (`N_TRA` 01) pregunta lo mismo, con qué opciones, filtro, flujo y unidad.
Misma forma y vocabulario que `data/credito-comparabilidad-texto-v1_0.tsv`
(A.15); reutiliza su verificador con otra rejilla: una conducta × seis olas.

  · 6 filas = 1 conducta × 6 olas, sin duplicados ni huecos;
  · 2021 es el ancla (`comparado_con` = «2021 (ancla)»), las demás se leen
    contra 2021;
  · veredicto en la lista cerrada; toda fila positiva cita reactivo, texto,
    opciones y flujo; la fuente trae sha256/16 y página;
  · 2025 no se abre: su fila sólo puede apoyarse en cuestionario y en la
    nota de NC-0355, nunca en microdato (la nota lo dice).

D-22: verificador probado sobre un sintético mínimo y sobre mutaciones que
deben fallar, antes de la tabla real. Sin módulo `csv`.
"""
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(RAIZ, "data", "encig-canal-comparabilidad-texto-v1_0.tsv")

_spec = importlib.util.spec_from_file_location(
    "credito_comp", os.path.join(RAIZ, "tests", "test_credito_comparabilidad_texto.py"))
CRED = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CRED)

CONDUCTA = "C-LUZ-DIGITAL"
OLAS = ["2015", "2017", "2019", "2021", "2023", "2025"]
ANCLA = "2021"


def verificar(ruta: str) -> list[str]:
    defectos: list[str] = []
    cab, filas = CRED.leer_tsv(ruta)
    if cab != CRED.COLUMNAS:
        return [f"cabecera: {cab} != {CRED.COLUMNAS}"]
    if len(filas) != len(OLAS):
        defectos.append(f"filas de datos: {len(filas)} != {len(OLAS)}")
    vistos = set()
    for i, r in enumerate(filas, start=2):
        ola, v = r["ola"], r["veredicto"]
        pref = f"línea {i} ({ola})"
        if r["conducta"] != CONDUCTA:
            defectos.append(f"{pref}: conducta != {CONDUCTA}")
        if ola not in OLAS:
            defectos.append(f"{pref}: ola fuera de {OLAS}")
        if ola in vistos:
            defectos.append(f"{pref}: ola duplicada")
        vistos.add(ola)
        esperado = f"{ANCLA} (ancla)" if ola == ANCLA else ANCLA
        if r["comparado_con"] != esperado:
            defectos.append(f"{pref}: comparado_con {r['comparado_con']!r} != {esperado!r}")
        for c in CRED.OBLIGATORIAS:
            if not r[c].strip():
                defectos.append(f"{pref}: columna obligatoria vacía: {c}")
        if v not in CRED.VEREDICTOS:
            defectos.append(f"{pref}: veredicto fuera de la lista cerrada: {v!r}")
            continue
        if v in CRED.POSITIVOS:
            for c in CRED.CITA_REACTIVO:
                if not r[c].strip():
                    defectos.append(f"{pref}: veredicto {v} sin {c}")
        if v == "NO-ESTIMABLE" and not r["texto_buscado"].strip():
            defectos.append(f"{pref}: NO-ESTIMABLE sin texto_buscado (A.15)")
        if v == "NO-VERIFICABLE-AQUÍ" and not r["limite_fd"].strip():
            defectos.append(f"{pref}: NO-VERIFICABLE-AQUÍ sin limite_fd")
        if not CRED.RE_SHA16.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin sha256/16")
        if not CRED.RE_PAG_O_FILA.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin página ni fila")
        if ola == "2025" and "no se abre" not in r["nota"]:
            defectos.append(f"{pref}: la fila 2025 debe declarar que la ola no se abre")
    faltan = set(OLAS) - vistos
    if faltan:
        defectos.append(f"olas ausentes: {sorted(faltan)}")
    return defectos


def _fila(ola: str, v: str) -> dict[str, str]:
    r = CRED._fila(CONDUCTA, ola, v)
    r["comparado_con"] = f"{ANCLA} (ancla)" if ola == ANCLA else ANCLA
    if ola == "2025":
        r["nota"] = "fixture; la ola no se abre"
    return r


def tabla_sintetica() -> list[dict[str, str]]:
    return [_fila(ola, "MISMO-INSTRUMENTO" if ola == ANCLA else "CAMBIO-MENOR") for ola in OLAS]


class TestSintetico(unittest.TestCase):
    def _defectos(self, filas):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tsv")
            CRED.escribir(filas, p)
            return verificar(p)

    def test_control_positivo(self):
        self.assertEqual(self._defectos(tabla_sintetica()), [])

    def test_falla_con_cinco_filas(self):
        d = self._defectos(tabla_sintetica()[:-1])
        self.assertTrue(any("5 != 6" in x for x in d), d)
        self.assertTrue(any("ausentes" in x for x in d), d)

    def test_falla_ancla_mal_declarada(self):
        filas = tabla_sintetica(); filas[3]["comparado_con"] = "2021"
        d = self._defectos(filas)
        self.assertTrue(any("comparado_con" in x for x in d), d)

    def test_falla_positivo_sin_reactivo(self):
        filas = tabla_sintetica(); filas[0]["reactivo"] = ""
        d = self._defectos(filas)
        self.assertTrue(any("sin reactivo" in x for x in d), d)

    def test_falla_2025_sin_declarar_reserva(self):
        filas = tabla_sintetica(); filas[5]["nota"] = "fixture"
        d = self._defectos(filas)
        self.assertTrue(any("no se abre" in x for x in d), d)


class TestTablaReal(unittest.TestCase):
    def test_tabla_en_forma(self):
        self.assertTrue(os.path.exists(TABLA), TABLA)
        self.assertEqual(verificar(TABLA), [])

    def test_veredictos_esperados_por_el_acto(self):
        _, filas = CRED.leer_tsv(TABLA)
        v = {r["ola"]: r["veredicto"] for r in filas}
        self.assertEqual(v["2021"], "MISMO-INSTRUMENTO")
        self.assertEqual(v["2017"], "MISMO-INSTRUMENTO")
        self.assertEqual(v["2019"], "MISMO-INSTRUMENTO")
        for ola in ("2015", "2023", "2025"):
            self.assertEqual(v[ola], "CAMBIO-MENOR", ola)


if __name__ == "__main__":
    unittest.main()
