#!/usr/bin/env python3
"""Test de forma de `data/enut-comparabilidad-texto-v1_0.tsv`.

ACTO GEN2-ENUT-PISOS-Y-SERIE-1 (21/sep/2026), pieza P1. La tabla dice, objeto
por objeto (C1..C5, E) y ola por ola (ENUT 2009-2024), qué ítems forman cada
variante de «cuidado», con qué filtros, ponderador y diseño, y si el
instrumento es el mismo. Este test pina la FORMA que P2-P4 consumen:

  · 24 filas de datos = 6 objetos × 4 olas, sin duplicados ni huecos;
  · columnas obligatorias sin celda vacía (incluye periodo, unidad, población,
    ponderador y diseño: lo que el encargo pide fila por fila);
  · veredicto dentro de la lista cerrada;
  · toda fila positiva trae reactivo, texto literal, códigos y flujo;
  · toda fila NO-ESTIMABLE o CAMBIO-DE-INSTRUMENTO trae el texto buscado (A.15);
  · la fuente cita archivo + sha256/16 + página o fila.

D-22: el punto de entrada corre PRIMERO sobre un caso sintético (tabla mínima
válida y cuatro mutaciones que deben fallar) y sólo después sobre la tabla
real. Sin módulo `csv` (despoja comillas): split por tabulador. Cero microdato.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(RAIZ, "data", "enut-comparabilidad-texto-v1_0.tsv")

OBJETOS = ["C1", "C2", "C3", "C4", "C5", "E"]
OLAS = ["2009", "2014", "2019", "2024"]
N_FILAS = len(OBJETOS) * len(OLAS)

VEREDICTOS = {"MISMO-INSTRUMENTO", "CAMBIO-MENOR", "CAMBIO-DE-INSTRUMENTO", "NO-ESTIMABLE"}
POSITIVOS = {"MISMO-INSTRUMENTO", "CAMBIO-MENOR", "CAMBIO-DE-INSTRUMENTO"}
EXIGEN_TEXTO_BUSCADO = {"NO-ESTIMABLE", "CAMBIO-DE-INSTRUMENTO"}

COLUMNAS = [
    "conducta", "conducta_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "reactivo", "texto_literal", "opciones_y_codigos",
    "filtro_y_flujo", "periodo_referencia", "unidad", "poblacion_base",
    "ponderador_y_diseno", "fuente", "secciones_fd_recorridas", "texto_buscado", "nota",
]
OBLIGATORIAS = [
    "conducta", "conducta_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "periodo_referencia", "unidad", "poblacion_base",
    "ponderador_y_diseno", "fuente", "secciones_fd_recorridas", "nota",
]
CITA_REACTIVO = ["reactivo", "texto_literal", "opciones_y_codigos", "filtro_y_flujo"]

RE_SHA16 = re.compile(r"sha256/16(?:\(zip\))?=[0-9a-f]{16}")
RE_PAG_O_FILA = re.compile(r"(pdf-p[aá]gs?\s+\d+|filas?\s+\d+)")


def leer_tsv(ruta: str) -> tuple[list[str], list[dict[str, str]]]:
    with open(ruta, encoding="utf-8") as f:
        lineas = f.read().split("\n")
    if lineas and lineas[-1] == "":
        lineas.pop()
    cab = lineas[0].split("\t")
    filas = []
    for n, l in enumerate(lineas[1:], start=2):
        celdas = l.split("\t")
        if len(celdas) != len(cab):
            raise AssertionError(f"línea {n}: {len(celdas)} celdas, cabecera {len(cab)}")
        filas.append(dict(zip(cab, celdas)))
    return cab, filas


def verificar(ruta: str) -> list[str]:
    """Devuelve la lista de defectos (vacía = tabla en forma)."""
    defectos: list[str] = []
    cab, filas = leer_tsv(ruta)
    if cab != COLUMNAS:
        defectos.append(f"cabecera: {cab} != {COLUMNAS}")
        return defectos
    if len(filas) != N_FILAS:
        defectos.append(f"filas de datos: {len(filas)} != {N_FILAS}")
    vistos = set()
    for i, r in enumerate(filas, start=2):
        k, ola, v = r["conducta"], r["ola"], r["veredicto"]
        pref = f"línea {i} ({k}×{ola})"
        if k not in OBJETOS:
            defectos.append(f"{pref}: objeto fuera de {OBJETOS}")
        if ola not in OLAS:
            defectos.append(f"{pref}: ola fuera de {OLAS}")
        if (k, ola) in vistos:
            defectos.append(f"{pref}: par objeto×ola duplicado")
        vistos.add((k, ola))
        for c in OBLIGATORIAS:
            if not r[c].strip():
                defectos.append(f"{pref}: columna obligatoria vacía: {c}")
        if v not in VEREDICTOS:
            defectos.append(f"{pref}: veredicto fuera de la lista cerrada: {v!r}")
            continue
        if ola == "2024" and r["comparado_con"] != "2024 (ancla)":
            defectos.append(f"{pref}: la fila 2024 debe ser ancla")
        if ola == "2024" and v != "MISMO-INSTRUMENTO":
            defectos.append(f"{pref}: la fila ancla se compara consigo misma")
        if v in POSITIVOS:
            for c in CITA_REACTIVO:
                if not r[c].strip():
                    defectos.append(f"{pref}: veredicto {v} sin {c}")
        if v in EXIGEN_TEXTO_BUSCADO and not r["texto_buscado"].strip():
            defectos.append(f"{pref}: {v} sin texto_buscado (A.15)")
        if not RE_SHA16.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin sha256/16")
        if not RE_PAG_O_FILA.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin página ni fila")
    faltan = {(k, o) for k in OBJETOS for o in OLAS} - vistos
    if faltan:
        defectos.append(f"pares objeto×ola ausentes: {sorted(faltan)}")
    return defectos


# ----------------------------------------------------------------- sintético
def _fila(k: str, ola: str, v: str) -> dict[str, str]:
    r = {c: "" for c in COLUMNAS}
    r.update(conducta=k, conducta_texto=f"objeto {k}", ola=ola,
             comparado_con="2024 (ancla)" if ola == "2024" else "2024",
             veredicto=v, alcance_del_veredicto="sintético", periodo_referencia="semana pasada",
             unidad="persona", poblacion_base="sintética", ponderador_y_diseno="FAC × EST × UPM",
             fuente="x.pdf sha256/16=0123456789abcdef pdf-pág 1",
             secciones_fd_recorridas="sección 6", nota="fixture")
    if v in POSITIVOS:
        r.update(reactivo="PX_1", texto_literal="¿...?", opciones_y_codigos="1 Sí / 2 No",
                 filtro_y_flujo="universal")
    if v in EXIGEN_TEXTO_BUSCADO:
        r["texto_buscado"] = "«término» en sección 6: 0 de 10 filas"
    return r


def tabla_sintetica() -> list[dict[str, str]]:
    return [_fila(k, ola, "MISMO-INSTRUMENTO" if ola == "2024" else "CAMBIO-MENOR")
            for k in OBJETOS for ola in OLAS]


def escribir(filas: list[dict[str, str]], ruta: str) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\t".join(COLUMNAS) + "\n")
        for r in filas:
            f.write("\t".join(r[c] for c in COLUMNAS) + "\n")


class TestSintetico(unittest.TestCase):
    """D-22: el verificador corre sobre un caso sintético antes que sobre la tabla real."""

    def _defectos(self, filas):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.tsv")
            escribir(filas, p)
            return verificar(p)

    def test_control_positivo_tabla_minima_valida(self):
        self.assertEqual(self._defectos(tabla_sintetica()), [])

    def test_falla_con_23_filas(self):
        d = self._defectos(tabla_sintetica()[:-1])
        self.assertTrue(any("23 != 24" in x for x in d), d)
        self.assertTrue(any("ausentes" in x for x in d), d)

    def test_falla_veredicto_fuera_de_lista(self):
        filas = tabla_sintetica()
        filas[1]["veredicto"] = "NO-CONSTRUIBLE"
        d = self._defectos(filas)
        self.assertTrue(any("lista cerrada" in x for x in d), d)

    def test_falla_cambio_de_instrumento_sin_texto_buscado(self):
        filas = tabla_sintetica()
        filas[1]["veredicto"] = "CAMBIO-DE-INSTRUMENTO"  # C1×2014
        d = self._defectos(filas)
        self.assertTrue(any("sin texto_buscado" in x for x in d), d)

    def test_falla_ancla_2024_con_otro_veredicto(self):
        filas = tabla_sintetica()
        filas[3]["veredicto"] = "CAMBIO-MENOR"  # C1×2024
        d = self._defectos(filas)
        self.assertTrue(any("ancla" in x for x in d), d)


class TestTablaReal(unittest.TestCase):
    def test_tabla_real_en_forma(self):
        self.assertTrue(os.path.exists(TABLA), TABLA)
        self.assertEqual(verificar(TABLA), [])

    def test_veredictos_fijados_por_el_dictamen(self):
        """ADR-557 + P1: C1 sólo es construible en 2024; 2014 ≡ 2019 para C2."""
        _, filas = leer_tsv(TABLA)
        v = {(r["conducta"], r["ola"]): r["veredicto"] for r in filas}
        for ola in ("2009", "2014", "2019"):
            self.assertEqual(v[("C1", ola)], "CAMBIO-DE-INSTRUMENTO", ola)
        self.assertEqual(v[("C2", "2019")], v[("C2", "2014")])
        self.assertEqual(v[("C2", "2009")], "CAMBIO-DE-INSTRUMENTO")
        self.assertEqual(v[("C3", "2009")], "CAMBIO-MENOR")


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], verbosity=2)
