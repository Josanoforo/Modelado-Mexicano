#!/usr/bin/env python3
"""Test de forma de `data/ahorro-comparabilidad-texto-v1_0.tsv`.

ACTO GEN2-DIN-LOTE-ENIF2024-A (21/sep/2026), pieza P1. Hermano del de credito
(`tests/test_credito_comparabilidad_texto.py`): misma forma, mismo vocabulario
de veredictos. La tabla dice, objeto por objeto (los dos componentes del
desenlace `ahorra_solo_informal` y los seis ejes) y ola por ola (ENIF
2012-2024), si la pregunta es la misma y con que universo. Lo que este test
pina es la forma que el COMMIT-1 del lote necesita para no volver a leer el
texto de ningun reactivo:

  * 40 filas de datos = 8 objetos x 5 olas, sin duplicados ni huecos;
  * columnas obligatorias sin celda vacia;
  * veredicto dentro de la lista cerrada del encargo;
  * toda fila positiva (MISMO-INSTRUMENTO / CAMBIO-MENOR /
    CAMBIO-DE-INSTRUMENTO) trae reactivo, texto literal, opciones y flujo;
  * toda fila con `componentes_no_estimables` trae `texto_buscado` (A.15:
    "no existe la variable" no vale; se cita el texto buscado y donde);
  * toda fila NO-ESTIMABLE trae `texto_buscado`;
  * toda fila NO-VERIFICABLE-AQUI trae `limite_fd` (hoy no hay ninguna: los
    cuestionarios de 2012 y 2015 entraron al corpus en #960, y por eso este
    acto pudo cerrar las diez filas que el de credito dejo abiertas);
  * la fuente cita archivo + sha256/16 + fila o pagina;
  * unidad, poblacion base y ponderador nunca vacios;
  * la ola ancla es 2021 y cada objeto tiene exactamente una fila por ola.

D-22: el punto de entrada corre PRIMERO sobre un caso sintetico (una tabla
minima valida y cinco mutaciones que deben fallar) y solo despues sobre la
tabla real. Sin modulo `csv` (despoja comillas; ver hallazgos): split por
tabulador, como el resto de los TSV del repo. Cero microdato.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(RAIZ, "data", "ahorro-comparabilidad-texto-v1_0.tsv")

OBJETOS = ["D-INF", "D-FOR", "E-SEX", "E-EDA", "E-ESC", "E-LOC", "E-FOR", "E-CTA"]
OLAS = ["2012", "2015", "2018", "2021", "2024"]
ANCLA = "2021"

VEREDICTOS = {
    "MISMO-INSTRUMENTO",
    "CAMBIO-MENOR",
    "CAMBIO-DE-INSTRUMENTO",
    "NO-ESTIMABLE",
    "NO-VERIFICABLE-AQUÍ",
}
POSITIVOS = {"MISMO-INSTRUMENTO", "CAMBIO-MENOR", "CAMBIO-DE-INSTRUMENTO"}

COLUMNAS = [
    "objeto", "objeto_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "reactivo", "texto_literal", "opciones_y_codigos",
    "filtro_y_flujo", "unidad", "poblacion_base", "ponderador_y_diseno",
    "fuente", "secciones_fd_recorridas", "componentes_no_estimables",
    "texto_buscado", "limite_fd", "nota",
]
OBLIGATORIAS = [
    "objeto", "objeto_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "unidad", "poblacion_base", "ponderador_y_diseno",
    "fuente", "secciones_fd_recorridas", "nota",
]
CITA_REACTIVO = ["reactivo", "texto_literal", "opciones_y_codigos", "filtro_y_flujo"]

RE_SHA16 = re.compile(r"sha256/16(?:\(zip\))?=[0-9a-f]{16}")
RE_PAG_O_FILA = re.compile(r"(filas?\s+\d+|p[aá]gs?\.?\s+\d+|l[ií]neas?\s+\d+|secci[oó]n\s+\d+)")


def lee(ruta):
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip()]
    cab = lineas[0].split("\t")
    return cab, [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def revisa(ruta, objetos=OBJETOS, olas=OLAS):
    """Devuelve la lista de problemas. Vacia = la tabla pasa."""
    mal = []
    cab, filas = lee(ruta)
    if cab != COLUMNAS:
        mal.append(f"cabecera distinta: {cab}")
        return mal

    vistos = set()
    for i, f in enumerate(filas, start=2):
        if len(f) != len(COLUMNAS):
            mal.append(f"fila {i}: {len(f)} columnas")
            continue
        clave = (f["objeto"], f["ola"])
        if clave in vistos:
            mal.append(f"fila {i}: duplicado {clave}")
        vistos.add(clave)
        if f["objeto"] not in objetos:
            mal.append(f"fila {i}: objeto desconocido {f['objeto']!r}")
        if f["ola"] not in olas:
            mal.append(f"fila {i}: ola desconocida {f['ola']!r}")
        if f["veredicto"] not in VEREDICTOS:
            mal.append(f"fila {i}: veredicto fuera de la lista cerrada {f['veredicto']!r}")
        for c in OBLIGATORIAS:
            if not f[c].strip():
                mal.append(f"fila {i}: columna obligatoria vacia {c}")
        if f["veredicto"] in POSITIVOS:
            for c in CITA_REACTIVO:
                if not f[c].strip():
                    mal.append(f"fila {i}: veredicto positivo sin {c}")
        if f["veredicto"] == "NO-ESTIMABLE" and not f["texto_buscado"].strip():
            mal.append(f"fila {i}: NO-ESTIMABLE sin texto_buscado (A.15)")
        if f["veredicto"] == "NO-VERIFICABLE-AQUÍ" and not f["limite_fd"].strip():
            mal.append(f"fila {i}: NO-VERIFICABLE-AQUI sin limite_fd")
        if f["componentes_no_estimables"].strip() and not f["texto_buscado"].strip():
            mal.append(f"fila {i}: componentes no estimables sin texto_buscado (A.15)")
        if f["ola"] != ANCLA and ANCLA not in f["comparado_con"]:
            mal.append(f"fila {i}: comparado_con no cita el ancla {ANCLA}")
        if not RE_SHA16.search(f["fuente"]):
            mal.append(f"fila {i}: fuente sin sha256/16")
        if not RE_PAG_O_FILA.search(f["fuente"]):
            mal.append(f"fila {i}: fuente sin fila/pagina/linea")

    faltan = {(o, w) for o in objetos for w in olas} - vistos
    if faltan:
        mal.append(f"faltan {len(faltan)} pares objeto x ola: {sorted(faltan)[:5]}")
    return mal


# --------------------------------------------------------------- sintetico
_OK = {
    "objeto": "D-INF", "objeto_texto": "x", "ola": "2021",
    "comparado_con": "2021 (ancla)", "veredicto": "MISMO-INSTRUMENTO",
    "alcance_del_veredicto": "x", "reactivo": "P5_1_1", "texto_literal": "x",
    "opciones_y_codigos": "1 Si", "filtro_y_flujo": "x", "unidad": "x",
    "poblacion_base": "x", "ponderador_y_diseno": "x",
    "fuente": "a.xlsx sha256/16=0123456789abcdef :: fila 10",
    "secciones_fd_recorridas": "x", "componentes_no_estimables": "",
    "texto_buscado": "", "limite_fd": "", "nota": "x",
}


def _escribe(filas):
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8")
    fh.write("\t".join(COLUMNAS) + "\n")
    for f in filas:
        fh.write("\t".join(f[c] for c in COLUMNAS) + "\n")
    fh.close()
    return fh.name


class TestSintetico(unittest.TestCase):
    """D-22: el verificador se ejercita antes de mirar la tabla real."""

    def _tabla(self, muta=None):
        filas = []
        for o in ["D-INF", "D-FOR"]:
            for w in OLAS:
                f = dict(_OK)
                f["objeto"] = o
                f["ola"] = w
                filas.append(f)
        if muta:
            muta(filas)
        return _escribe(filas)

    def test_00_minima_valida_pasa(self):
        r = self._tabla()
        self.assertEqual(revisa(r, objetos=["D-INF", "D-FOR"]), [])

    def test_01_veredicto_inventado_falla(self):
        def m(filas):
            filas[0]["veredicto"] = "MAS-O-MENOS"
        mal = revisa(self._tabla(m), objetos=["D-INF", "D-FOR"])
        self.assertTrue(any("lista cerrada" in x for x in mal), mal)

    def test_02_obligatoria_vacia_falla(self):
        def m(filas):
            filas[1]["unidad"] = ""
        mal = revisa(self._tabla(m), objetos=["D-INF", "D-FOR"])
        self.assertTrue(any("obligatoria vacia" in x for x in mal), mal)

    def test_03_componentes_sin_texto_buscado_falla(self):
        def m(filas):
            filas[2]["componentes_no_estimables"] = "la vía 8"
        mal = revisa(self._tabla(m), objetos=["D-INF", "D-FOR"])
        self.assertTrue(any("sin texto_buscado" in x for x in mal), mal)

    def test_04_fuente_sin_sha_falla(self):
        def m(filas):
            filas[3]["fuente"] = "a.xlsx :: fila 10"
        mal = revisa(self._tabla(m), objetos=["D-INF", "D-FOR"])
        self.assertTrue(any("sin sha256/16" in x for x in mal), mal)

    def test_05_hueco_falla(self):
        def m(filas):
            filas.pop()
        mal = revisa(self._tabla(m), objetos=["D-INF", "D-FOR"])
        self.assertTrue(any("faltan" in x for x in mal), mal)


class TestTablaReal(unittest.TestCase):
    def test_10_existe(self):
        self.assertTrue(os.path.exists(TABLA), TABLA)

    def test_11_forma(self):
        mal = revisa(TABLA)
        self.assertEqual(mal, [], "\n".join(mal))

    def test_12_cuarenta_filas(self):
        _, filas = lee(TABLA)
        self.assertEqual(len(filas), len(OBJETOS) * len(OLAS))

    def test_13_ancla_siempre_positiva(self):
        """Una fila ancla con veredicto negativo seria una contradiccion."""
        _, filas = lee(TABLA)
        for f in filas:
            if f["ola"] == ANCLA:
                self.assertEqual(f["veredicto"], "MISMO-INSTRUMENTO", f["objeto"])


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False, verbosity=2).result.wasSuccessful() else 1)
