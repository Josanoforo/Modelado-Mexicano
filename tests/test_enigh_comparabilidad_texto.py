#!/usr/bin/env python3
"""Test de forma de `data/enigh-comparabilidad-texto-v1_0.tsv`.

ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1, pieza P2. La tabla dice, variable por
variable, si la definición/construcción/catálogo de ENIGH 2022 y ENIGH 2024
son la misma cosa -- leído del diccionario de datos ("Descripción de la
base"), nunca del microdato de 2024 (que sigue RESERVADO). Mismo patrón que
`data/credito-comparabilidad-texto-v1_1.tsv`
(`tests/test_credito_comparabilidad_texto.py`), adaptado: ENIGH documenta
variables por diccionario (tipo/definición/construcción/catálogo), no por
flujo de pase de cuestionario, así que la unidad de fila es `variable` (no
`conducta`×`ola`) y no hay eje NO-VERIFICABLE-AQUÍ (los dos descriptores,
2022 y 2024, ya están en el corpus).

D-22: el punto de entrada corre PRIMERO sobre un caso sintético (una tabla
mínima válida y mutaciones que deben fallar) y sólo después sobre la tabla
real. Sin módulo `csv` (ver [[feedback_csv_module_corrompe_tsv]]): split por
tabulador, como el resto de los TSV del repo. Cero microdato de ENIGH2024.
"""
from __future__ import annotations

import os
import re
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(RAIZ, "data", "enigh-comparabilidad-texto-v1_0.tsv")

VEREDICTOS = {
    "MISMO-INSTRUMENTO",
    "CAMBIO-MENOR",
    "CAMBIO-DE-INSTRUMENTO",
    "NO-ESTIMABLE",
}
POSITIVOS = {"MISMO-INSTRUMENTO", "CAMBIO-MENOR", "CAMBIO-DE-INSTRUMENTO"}

COLUMNAS = [
    "variable", "variable_etiqueta", "comparado_con", "veredicto",
    "alcance_del_veredicto", "reactivo", "texto_literal", "opciones_y_codigos",
    "filtro_y_flujo", "unidad", "poblacion_base", "fuente",
    "secciones_fd_recorridas", "componentes_no_estimables", "texto_buscado",
    "limite_fd", "nota",
]
OBLIGATORIAS = [
    "variable", "variable_etiqueta", "comparado_con", "veredicto",
    "alcance_del_veredicto", "unidad", "poblacion_base", "fuente",
    "secciones_fd_recorridas", "nota",
]
CITA_REACTIVO = ["reactivo", "texto_literal", "opciones_y_codigos", "filtro_y_flujo"]
RE_SHA16 = re.compile(r"sha256/16=[0-9a-f]{16}")
RE_PAGINA = re.compile(r"pdf-p[aá]g")

VARIABLES_ESPERADAS = {
    "folioviv", "foliohog", "parentesco", "edad", "segsoc", "tam_loc",
    "est_socio", "est_dis", "upm", "factor", "celular", "conex_inte",
    "remesas", "ing_cor",
}


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
    vistos = set()
    for i, r in enumerate(filas, start=2):
        v = r["veredicto"]
        var = r["variable"]
        pref = f"línea {i} ({var})"
        if var in vistos:
            defectos.append(f"{pref}: variable duplicada")
        vistos.add(var)
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
        if v == "NO-ESTIMABLE" and not r["texto_buscado"].strip():
            defectos.append(f"{pref}: NO-ESTIMABLE sin texto_buscado (A.15)")
        if r["componentes_no_estimables"].strip() and not r["texto_buscado"].strip():
            defectos.append(f"{pref}: componentes_no_estimables sin texto_buscado")
        fuente = r["fuente"]
        if not RE_SHA16.search(fuente):
            defectos.append(f"{pref}: fuente sin sha256/16: {fuente!r}")
        if not RE_PAGINA.search(fuente):
            defectos.append(f"{pref}: fuente sin cita de página: {fuente!r}")
    return defectos


class SintenticoAntesQueReal(unittest.TestCase):
    """D-22: el conducto se ejercita sobre casos fabricados primero."""

    def _tabla(self, filas_extra_texto: str) -> str:
        cab = "\t".join(COLUMNAS)
        fila_valida = "\t".join([
            "x_var", "Etiqueta X", "2022", "MISMO-INSTRUMENTO", "todo",
            "x_var", "Texto literal.", "1=Sí, 2=No", "Sin filtro.",
            "hogar", "Todos los hogares", "doc_pdf sha256/16=0123456789abcdef pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        return cab + "\n" + fila_valida + (("\n" + filas_extra_texto) if filas_extra_texto else "") + "\n"

    def _escribe_y_verifica(self, texto: str) -> list[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
            f.write(texto)
            ruta = f.name
        try:
            return verificar(ruta)
        finally:
            os.unlink(ruta)

    def test_tabla_minima_valida_pasa(self):
        self.assertEqual(self._escribe_y_verifica(self._tabla("")), [])

    def test_veredicto_fuera_de_lista_falla(self):
        cab = "\t".join(COLUMNAS)
        fila_mala = "\t".join([
            "x_var", "Etiqueta X", "2022", "QUIZAS", "todo",
            "x_var", "Texto literal.", "1=Sí, 2=No", "Sin filtro.",
            "hogar", "Todos los hogares", "doc_pdf sha256/16=0123456789abcdef pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        defectos = self._escribe_y_verifica(cab + "\n" + fila_mala + "\n")
        self.assertTrue(any("lista cerrada" in d for d in defectos))

    def test_columna_obligatoria_vacia_falla(self):
        cab = "\t".join(COLUMNAS)
        fila_mala = "\t".join([
            "x_var", "", "2022", "MISMO-INSTRUMENTO", "todo",
            "x_var", "Texto literal.", "1=Sí, 2=No", "Sin filtro.",
            "hogar", "Todos los hogares", "doc_pdf sha256/16=0123456789abcdef pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        defectos = self._escribe_y_verifica(cab + "\n" + fila_mala + "\n")
        self.assertTrue(any("vacía" in d for d in defectos))

    def test_positivo_sin_cita_falla(self):
        cab = "\t".join(COLUMNAS)
        fila_mala = "\t".join([
            "x_var", "Etiqueta X", "2022", "MISMO-INSTRUMENTO", "todo",
            "", "", "", "",
            "hogar", "Todos los hogares", "doc_pdf sha256/16=0123456789abcdef pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        defectos = self._escribe_y_verifica(cab + "\n" + fila_mala + "\n")
        self.assertTrue(any("sin reactivo" in d for d in defectos))

    def test_fuente_sin_sha_falla(self):
        cab = "\t".join(COLUMNAS)
        fila_mala = "\t".join([
            "x_var", "Etiqueta X", "2022", "MISMO-INSTRUMENTO", "todo",
            "x_var", "Texto literal.", "1=Sí, 2=No", "Sin filtro.",
            "hogar", "Todos los hogares", "doc_pdf pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        defectos = self._escribe_y_verifica(cab + "\n" + fila_mala + "\n")
        self.assertTrue(any("sin sha256/16" in d for d in defectos))

    def test_duplicado_de_variable_falla(self):
        cab = "\t".join(COLUMNAS)
        fila = "\t".join([
            "x_var", "Etiqueta X", "2022", "MISMO-INSTRUMENTO", "todo",
            "x_var", "Texto literal.", "1=Sí, 2=No", "Sin filtro.",
            "hogar", "Todos los hogares", "doc_pdf sha256/16=0123456789abcdef pdf-pág 1",
            "Tabla X (p. 1)", "", "", "", "Nota.",
        ])
        defectos = self._escribe_y_verifica(cab + "\n" + fila + "\n" + fila + "\n")
        self.assertTrue(any("duplicada" in d for d in defectos))


class TablaReal(unittest.TestCase):
    def test_tabla_real_en_forma(self):
        defectos = verificar(TABLA)
        self.assertEqual(defectos, [], "\n".join(defectos))

    def test_cubre_las_variables_de_p1(self):
        _cab, filas = leer_tsv(TABLA)
        presentes = {r["variable"] for r in filas}
        faltan = VARIABLES_ESPERADAS - presentes
        self.assertEqual(faltan, set(), f"variables sin fila: {faltan}")


if __name__ == "__main__":
    unittest.main()
