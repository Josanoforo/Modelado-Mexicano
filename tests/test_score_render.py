#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_score_render.py -- prueba de `construir_documento`/
`render_json`/`render_markdown` en `tools/score_marco_m.py`
(`ACTO AUTOMATIZA-2-E5 · SCORE-RENDER`, 7/sep/2026).

Fixture de tres celdas -- constante pequeña dentro del acto, no golden
del scoreboard real -- con `_m_disponible`/`_r_disponible`/`_l_disponible`
parcheados para no tocar el árbol de `corridas-M/R/L`:

  · CEL-A: R+M disponibles, sin marca DD -> puntuable.
  · CEL-B: sin R (aunque M y L estén), sin marca DD -> no puntuable.
  · CEL-C: R+M disponibles pero `VERIFICACION-NO-PUNTUA` -> excluida
    igual, aunque tenga corredores.

Corre sola:
    python3 tests/test_score_render.py
"""
import csv
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import score_marco_m as S  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


FILAS_FIXTURE = [
    {"id": "CEL-A", "grado_DD": "P1 PUNTUA"},
    {"id": "CEL-B", "grado_DD": "P1 PUNTUA"},
    {"id": "CEL-C", "grado_DD": "VERIFICACION-NO-PUNTUA"},
]

DATOS_M = {
    "CEL-A": {"disponible": True, "estado_M": "EMITE", "valor_punto": 0.42},
    "CEL-B": {"disponible": True, "estado_M": "EMITE", "valor_punto": 0.10},
    "CEL-C": {"disponible": True, "estado_M": "EMITE", "valor_punto": 0.99},
}
DATOS_R = {
    "CEL-A": {"disponible": True, "estado": "COMPUTADO", "R": 0.5, "EE_R": 0.02},
    "CEL-B": {"disponible": False, "estado": None, "R": None, "EE_R": None},
    "CEL-C": {"disponible": True, "estado": "COMPUTADO", "R": 0.7, "EE_R": 0.03},
}
DATOS_L = {
    "CEL-A": {"disponible": False, "n_corridas": 0, "archivos": []},
    "CEL-B": {"disponible": True, "n_corridas": 2, "archivos": ["CEL-B__L-solo__01.json", "CEL-B__L-solo__02.json"]},
    "CEL-C": {"disponible": False, "n_corridas": 0, "archivos": []},
}


def _escribe_fixture_tsv(directorio):
    ruta = os.path.join(directorio, "marco-M-sorteado-fixture.tsv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "grado_DD"], delimiter="\t")
        w.writeheader()
        for fila in FILAS_FIXTURE:
            w.writerow(fila)
    return ruta


def _parcha_corredores():
    original_m, original_r, original_l = S._m_disponible, S._r_disponible, S._l_disponible
    S._m_disponible = lambda id_celda: DATOS_M[id_celda]
    S._r_disponible = lambda id_celda: DATOS_R[id_celda]
    S._l_disponible = lambda id_celda: DATOS_L[id_celda]

    def restaura():
        S._m_disponible, S._r_disponible, S._l_disponible = original_m, original_r, original_l

    return restaura


def prueba_construir_documento_igual_al_main_previo():
    """`construir_documento` reproduce exactamente el documento que `main()`
    armaba inline antes de esta extracción -- misma forma, mismas claves,
    recompuesto aquí con los primitivos sin tocar (`censar_universo`,
    `construir_entrada_scoring`) para servir de comparación independiente."""
    restaura = _parcha_corredores()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = _escribe_fixture_tsv(tmp)
            from pathlib import Path

            ruta_marco = Path(ruta)
            filas = S._leer_tsv(ruta_marco)
            censo_esperado = S.censar_universo(filas, schema_dd=True)
            entrada_esperada = S.construir_entrada_scoring(censo_esperado)
            documento_esperado = {
                "marco_censado": ruta_marco.name,
                "n_celdas_universo": len(censo_esperado),
                "n_verificacion_no_puntua": sum(1 for c in censo_esperado if c["verificacion_no_puntua"]),
                "n_puntuables": sum(1 for c in censo_esperado if c["puntuable"]),
                "censo": censo_esperado,
                "entrada_scoring": entrada_esperada,
            }

            documento = S.construir_documento(ruta_marco, schema_dd=True)

            afirma(documento == documento_esperado,
                   f"construir_documento diverge del documento que main() armaba antes:\n{documento!r}\n!=\n{documento_esperado!r}")
            afirma(documento["n_celdas_universo"] == 3, documento["n_celdas_universo"])
            afirma(documento["n_verificacion_no_puntua"] == 1, documento["n_verificacion_no_puntua"])
            afirma(documento["n_puntuables"] == 1, documento["n_puntuables"])
            ids_puntuables = {c["id_celda"] for c in documento["censo"] if c["puntuable"]}
            afirma(ids_puntuables == {"CEL-A"}, ids_puntuables)
            ids_no_puntua_dd = {c["id_celda"] for c in documento["censo"] if c["verificacion_no_puntua"]}
            afirma(ids_no_puntua_dd == {"CEL-C"}, ids_no_puntua_dd)

            return documento
    finally:
        restaura()


def prueba_render_json_es_json_dumps_actual(documento):
    esperado = S.json.dumps(documento, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    afirma(S.render_json(documento) == esperado, "render_json diverge de json.dumps(...) + '\\n'")


def prueba_render_markdown_tres_filas_y_valores_por_fila(documento):
    md = S.render_markdown(documento)
    lineas = md.splitlines()
    filas_tabla = [l for l in lineas if l.startswith("| CEL-")]
    afirma(len(filas_tabla) == 3, f"esperaba exactamente 3 filas de datos, hubo {len(filas_tabla)}: {filas_tabla!r}")

    por_id = {}
    for linea in filas_tabla:
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        por_id[celdas[0]] = celdas

    # id_celda | grado_DD | verificación-no-puntúa | M | R | L | puntuable
    fila_a = por_id["CEL-A"]
    afirma(fila_a[2] == "NO", fila_a)
    afirma(fila_a[3] == "EMITE", fila_a)
    afirma(fila_a[4] == "COMPUTADO (0.5/0.02)", fila_a)
    afirma(fila_a[5] == "0", fila_a)
    afirma(fila_a[6] == "SÍ", fila_a)

    fila_b = por_id["CEL-B"]
    afirma(fila_b[2] == "NO", fila_b)
    afirma(fila_b[3] == "EMITE", fila_b)
    afirma(fila_b[4] == "—", fila_b)
    afirma(fila_b[5] == "2", fila_b)
    afirma(fila_b[6] == "NO", fila_b)

    fila_c = por_id["CEL-C"]
    afirma(fila_c[2] == "SÍ", fila_c)
    afirma(fila_c[3] == "EMITE", fila_c)
    afirma(fila_c[4] == "COMPUTADO (0.7/0.03)", fila_c)
    afirma(fila_c[5] == "0", fila_c)
    afirma(fila_c[6] == "NO", fila_c)

    afirma(f"n_celdas_universo: {documento['n_celdas_universo']}" in md, md)
    afirma(f"n_verificacion_no_puntua: {documento['n_verificacion_no_puntua']}" in md, md)
    afirma(f"n_puntuables: {documento['n_puntuables']}" in md, md)


def prueba_render_markdown_dos_corridas_bytes_identicos(documento):
    primera = S.render_markdown(documento)
    segunda = S.render_markdown(documento)
    afirma(primera == segunda, "dos corridas de render_markdown sobre el mismo documento deben ser byte a byte idénticas")
    afirma(primera.encode("utf-8") == segunda.encode("utf-8"), "divergencia a nivel de bytes utf-8")


def main():
    documento = prueba_construir_documento_igual_al_main_previo()
    prueba_render_json_es_json_dumps_actual(documento)
    prueba_render_markdown_tres_filas_y_valores_por_fila(documento)
    prueba_render_markdown_dos_corridas_bytes_identicos(documento)
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_score_render.py: 4 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
