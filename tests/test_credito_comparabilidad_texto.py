#!/usr/bin/env python3
"""Test de forma de `data/credito-comparabilidad-texto-v1_0.tsv`.

ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1 (20/sep/2026), pieza P7. La tabla
dice, conducta por conducta (K1-K8) y ola por ola (ENIF 2012-2024), si la
sección de crédito pregunta lo mismo y con qué unidad. Este test pina la FORMA
que el sucesor (marginales de crédito 2021) necesita para no volver a leer el
texto de ningún reactivo:

  · 40 filas de datos = 8 conductas × 5 olas, sin duplicados ni huecos;
  · columnas obligatorias sin celda vacía;
  · veredicto dentro de la lista cerrada de §5 del encargo;
  · toda fila con veredicto positivo (MISMO-INSTRUMENTO / CAMBIO-MENOR /
    CAMBIO-DE-INSTRUMENTO) trae reactivo, texto literal, opciones y flujo;
  · toda fila NO-ESTIMABLE trae el texto buscado y las secciones recorridas
    (A.15: «no existe la variable» no vale);
  · toda fila NO-VERIFICABLE-AQUÍ trae el límite del FD declarado, y sólo
    puede serlo en 2012 y 2015 (las olas sin cuestionario en el corpus);
  · toda fila con componentes no estimables trae el texto buscado;
  · la fuente cita archivo + sha256/16 + página o fila;
  · unidad y población base nunca vacías.

D-22: el punto de entrada corre PRIMERO sobre un caso sintético (una tabla
mínima válida y cuatro mutaciones que deben fallar) y sólo después sobre la
tabla real. Sin módulo `csv` (despoja comillas; ver hallazgos): split por
tabulador, como el resto de los TSV del repo. Cero microdato.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(RAIZ, "data", "credito-comparabilidad-texto-v1_0.tsv")

CONDUCTAS = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
OLAS = ["2012", "2015", "2018", "2021", "2024"]
OLAS_SIN_CUESTIONARIO = {"2012", "2015"}

VEREDICTOS = {
    "MISMO-INSTRUMENTO",
    "CAMBIO-MENOR",
    "CAMBIO-DE-INSTRUMENTO",
    "NO-ESTIMABLE",
    "NO-VERIFICABLE-AQUÍ",
}
POSITIVOS = {"MISMO-INSTRUMENTO", "CAMBIO-MENOR", "CAMBIO-DE-INSTRUMENTO"}

COLUMNAS = [
    "conducta", "conducta_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "reactivo", "texto_literal", "opciones_y_codigos",
    "filtro_y_flujo", "unidad", "poblacion_base", "fuente",
    "secciones_fd_recorridas", "componentes_no_estimables", "texto_buscado",
    "limite_fd", "nota",
]
# Nunca vacías, en ninguna fila.
OBLIGATORIAS = [
    "conducta", "conducta_texto", "ola", "comparado_con", "veredicto",
    "alcance_del_veredicto", "unidad", "poblacion_base", "fuente",
    "secciones_fd_recorridas", "nota",
]
# Obligatorias sólo cuando el veredicto es positivo (hay un reactivo que citar).
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
    if len(filas) != 40:
        defectos.append(f"filas de datos: {len(filas)} != 40")
    vistos = set()
    for i, r in enumerate(filas, start=2):
        k, ola, v = r["conducta"], r["ola"], r["veredicto"]
        pref = f"línea {i} ({k}×{ola})"
        if k not in CONDUCTAS:
            defectos.append(f"{pref}: conducta fuera de K1..K8")
        if ola not in OLAS:
            defectos.append(f"{pref}: ola fuera de {OLAS}")
        if (k, ola) in vistos:
            defectos.append(f"{pref}: par conducta×ola duplicado")
        vistos.add((k, ola))
        for c in OBLIGATORIAS:
            if not r[c].strip():
                defectos.append(f"{pref}: columna obligatoria vacía: {c}")
        if v not in VEREDICTOS:
            defectos.append(f"{pref}: veredicto fuera de la lista cerrada: {v!r}")
            continue
        if v in POSITIVOS:
            for c in CITA_REACTIVO:
                if not r[c].strip():
                    defectos.append(f"{pref}: veredicto {v} sin {c}")
        if v == "NO-ESTIMABLE":
            if not r["texto_buscado"].strip():
                defectos.append(f"{pref}: NO-ESTIMABLE sin texto_buscado (A.15)")
            if ola in OLAS_SIN_CUESTIONARIO:
                defectos.append(f"{pref}: NO-ESTIMABLE en ola sin cuestionario; debe ser NO-VERIFICABLE-AQUÍ")
        if v == "NO-VERIFICABLE-AQUÍ":
            if ola not in OLAS_SIN_CUESTIONARIO:
                defectos.append(f"{pref}: NO-VERIFICABLE-AQUÍ sólo cabe en 2012/2015")
            if not r["limite_fd"].strip():
                defectos.append(f"{pref}: NO-VERIFICABLE-AQUÍ sin limite_fd")
        if r["componentes_no_estimables"].strip() and not r["texto_buscado"].strip():
            defectos.append(f"{pref}: componentes_no_estimables sin texto_buscado")
        if not RE_SHA16.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin sha256/16")
        if not RE_PAG_O_FILA.search(r["fuente"]):
            defectos.append(f"{pref}: fuente sin página ni fila")
    faltan = {(k, o) for k in CONDUCTAS for o in OLAS} - vistos
    if faltan:
        defectos.append(f"pares conducta×ola ausentes: {sorted(faltan)}")
    return defectos


# ----------------------------------------------------------------- sintético
def _fila(k: str, ola: str, v: str) -> dict[str, str]:
    r = {c: "" for c in COLUMNAS}
    r.update(conducta=k, conducta_texto=f"conducta {k}", ola=ola, comparado_con="2021",
             veredicto=v, alcance_del_veredicto="sintético", unidad="P",
             poblacion_base="sintética", fuente="x.pdf sha256/16=0123456789abcdef pdf-pág 1",
             secciones_fd_recorridas="sección 6", nota="fixture")
    if v in POSITIVOS:
        r.update(reactivo="PX_1", texto_literal="¿...?", opciones_y_codigos="1 Sí / 2 No",
                 filtro_y_flujo="universal")
    if v == "NO-ESTIMABLE":
        r["texto_buscado"] = "«término» en sección 6: 0"
    if v == "NO-VERIFICABLE-AQUÍ":
        r["limite_fd"] = "sin cuestionario"
    return r


def tabla_sintetica() -> list[dict[str, str]]:
    filas = []
    for k in CONDUCTAS:
        for ola in OLAS:
            v = "NO-VERIFICABLE-AQUÍ" if ola in OLAS_SIN_CUESTIONARIO else "CAMBIO-MENOR"
            filas.append(_fila(k, ola, v))
    return filas


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

    def test_falla_con_39_filas(self):
        filas = tabla_sintetica()[:-1]
        d = self._defectos(filas)
        self.assertTrue(any("39 != 40" in x for x in d), d)
        self.assertTrue(any("ausentes" in x for x in d), d)

    def test_falla_veredicto_fuera_de_lista(self):
        filas = tabla_sintetica()
        filas[0]["veredicto"] = "NO-CONSTRUIBLE"
        d = self._defectos(filas)
        self.assertTrue(any("lista cerrada" in x for x in d), d)

    def test_falla_no_estimable_sin_texto_buscado(self):
        filas = tabla_sintetica()
        filas[2]["veredicto"] = "NO-ESTIMABLE"  # K1×2018
        d = self._defectos(filas)
        self.assertTrue(any("sin texto_buscado" in x for x in d), d)

    def test_falla_no_verificable_en_ola_con_cuestionario(self):
        filas = tabla_sintetica()
        filas[3]["veredicto"] = "NO-VERIFICABLE-AQUÍ"  # K1×2021
        filas[3]["limite_fd"] = "x"
        d = self._defectos(filas)
        self.assertTrue(any("sólo cabe en 2012/2015" in x for x in d), d)

    def test_falla_obligatoria_vacia_y_positivo_sin_reactivo(self):
        filas = tabla_sintetica()
        filas[4]["unidad"] = ""
        filas[4]["reactivo"] = ""
        d = self._defectos(filas)
        self.assertTrue(any("vacía: unidad" in x for x in d), d)
        self.assertTrue(any("sin reactivo" in x for x in d), d)


class TestTablaReal(unittest.TestCase):
    def test_tabla_real_en_forma(self):
        self.assertTrue(os.path.exists(TABLA), TABLA)
        d = verificar(TABLA)
        self.assertEqual(d, [], "\n".join(d))

    def test_conteo_por_veredicto_es_el_declarado(self):
        # Pinado al cierre del acto (20/sep/2026); cambiar la tabla exige tocar
        # esta línea a la vista, no en silencio.
        _, filas = leer_tsv(TABLA)
        conteo = {}
        for r in filas:
            conteo[r["veredicto"]] = conteo.get(r["veredicto"], 0) + 1
        self.assertEqual(conteo, {
            "MISMO-INSTRUMENTO": 8,
            "CAMBIO-MENOR": 11,
            "CAMBIO-DE-INSTRUMENTO": 2,
            "NO-ESTIMABLE": 3,
            "NO-VERIFICABLE-AQUÍ": 16,
        })


if __name__ == "__main__":
    unittest.main(verbosity=2)
