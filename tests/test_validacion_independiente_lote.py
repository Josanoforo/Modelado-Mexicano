#!/usr/bin/env python3
"""Guardia de `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-LOTE-v1_0/`.

ACTO GEN2-VALIDACION-INDEPENDIENTE-LOTE-1 (22/sep/2026). La validación independiente de
las 44 celdas primarias del lote (`#986`) produjo, a ciegas (commit `97d92016`, antes de
abrir el sellado), R y C2 por celda y los comparó contra
`CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001`. Este test pina que el veredicto archivado
sigue siendo el que el árbol contiene:

  · comparacion-lote.json trae 44 celdas, las 44 `COINCIDE`;
  · `R_p_propio` y `R_p_sellado` de cada celda son iguales a `1e-9`;
  · los `n` (2024) propios y sellados son iguales, celda por celda;
  · el valor «sellado» que la comparación archivó sigue siendo el que hoy trae el
    `resultados.json` del CALC (si alguien re-sella el CALC, este test lo delata: un
    veredicto `COINCIDE` contra un sello que ya no existe es un veredicto vencido, A.10).

Defecto real que atrapa: un `resultados.json` re-generado bajo otro contrato dejaría el
informe afirmando `COINCIDE` sobre cifras que ya no están en el árbol. D-22: primero corre
sobre un caso sintético (una comparación mínima válida y tres mutaciones que deben fallar),
después sobre el archivo real. Cero microdato; no requiere corpus.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "forense", "validaciones", "GEN2-VALIDACION-INDEPENDIENTE-LOTE-v1_0")
COMP = os.path.join(DIR, "comparacion-lote.json")
N_CELDAS_ESPERADO = 44
CALC = "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001"

EDAD_MAP = {"edad:E1": "18-29", "edad:E2": "30-44", "edad:E3": "45-59", "edad:E4": "60"}
SEXO_MAP = {"sexo:H": "1-HOMBRE", "sexo:M": "2-MUJER"}
ESC_MAP = {"escolaridad:HP": "HASTA-PRIMARIA", "escolaridad:SEC": "SECUNDARIA", "escolaridad:MS": "MEDIA-SUPERIOR", "escolaridad:SUP": "SUPERIOR"}
LOC_MAP = {"localidad:L1": "MENOR-DE-15-000", "localidad:L2": "15-000-Y-MAS"}
TOKEN = {**EDAD_MAP, **SEXO_MAP, **ESC_MAP, **LOC_MAP}
PARES = {
    "edadxsexo": ("edad", "sexo", "EDADXSEXO"), "escolaridadxsexo": ("escolaridad", "sexo", "ESCOLARIDADXSEXO"),
    "localidadxsexo": ("localidad", "sexo", "LOCALIDADXSEXO"), "edadxescolaridad": ("edad", "escolaridad", "EDADXESCOLARIDAD"),
    "escolaridadxlocalidad": ("escolaridad", "localidad", "ESCOLARIDADXLOCALIDAD"),
}


def valida(comp: dict, sellados_hoy: dict) -> list[str]:
    """Devuelve la lista de defectos (vacía = VERDE). `sellados_hoy[celda] = R sellado hoy."""
    errores = []
    filas = comp.get("celdas", [])
    if len(filas) != N_CELDAS_ESPERADO:
        errores.append(f"n_celdas {len(filas)}, esperadas {N_CELDAS_ESPERADO}")
    for f in filas:
        celda = f["celda"]
        if f.get("veredicto") != "COINCIDE":
            errores.append(f"{celda}: veredicto {f.get('veredicto')}")
            continue
        if f.get("R_p_propio") is None or f.get("R_p_sellado") is None:
            errores.append(f"{celda}: R ausente")
            continue
        if abs(f["R_p_propio"] - f["R_p_sellado"]) > 1e-9:
            errores.append(f"{celda}: R propio {f['R_p_propio']} != sellado archivado {f['R_p_sellado']}")
        if f.get("n_propio") != f.get("n_sellado"):
            errores.append(f"{celda}: n propio {f.get('n_propio')} != n sellado {f.get('n_sellado')}")
        hoy = sellados_hoy.get(celda)
        if hoy is None or abs(hoy - f["R_p_sellado"]) > 1e-9:
            errores.append(f"{celda}: R sellado archivado {f['R_p_sellado']} != árbol hoy {hoy}")
    return errores


def _fila(celda, r_prop, r_sel, n=300, veredicto="COINCIDE"):
    return {"celda": celda, "R_p_propio": r_prop, "R_p_sellado": r_sel, "n_propio": n, "n_sellado": n, "veredicto": veredicto}


def sintetico() -> None:
    comp = {"celdas": [_fila(f"c{i}", 0.4, 0.4) for i in range(N_CELDAS_ESPERADO)]}
    sel = {f["celda"]: 0.4 for f in comp["celdas"]}
    assert valida(comp, sel) == [], "el caso sintético válido debe pasar"
    # mutación 1: una celda con veredicto DISCREPA
    m = json.loads(json.dumps(comp))
    m["celdas"][0]["veredicto"] = "DISCREPA"
    assert any("veredicto DISCREPA" in e for e in valida(m, sel))
    # mutación 2: n distinto
    m = json.loads(json.dumps(comp))
    m["celdas"][1]["n_sellado"] = 299
    assert any("n propio" in e for e in valida(m, sel))
    # mutación 3: el árbol ya no trae el sello archivado (re-sello simulado)
    s2 = dict(sel)
    s2["c2"] = 0.40001
    assert any("árbol hoy" in e for e in valida(comp, s2))
    # mutación 4: falta una celda
    m = json.loads(json.dumps(comp))
    m["celdas"].pop()
    assert any("n_celdas" in e for e in valida(m, sel))


def sellados_hoy(comp: dict) -> dict:
    p = os.path.join(ROOT, "data", "corrida0", CALC, "resultados.json")
    r = json.load(open(p, encoding="utf-8"))["resultados"]
    out = {}
    for f in comp.get("celdas", []):
        celda = f["celda"]
        par_slug, sufc = celda.split(":")
        entry = PARES.get(par_slug)
        if entry is None:
            continue
        a_slug, b_slug, par = entry
        na, nb = sufc.split("x")
        tok_a = TOKEN.get(f"{a_slug}:{na}")
        tok_b = TOKEN.get(f"{b_slug}:{nb}")
        if tok_a is None or tok_b is None:
            continue
        key = f"RESULT-DIN-LOTE24-ADJ-{par}-R-{tok_a}-X-{tok_b}-P"
        out[celda] = r.get(key)
    return out


def main() -> int:
    sintetico()
    print("sintético: OK (1 válido, 4 mutaciones detectadas)")
    comp = json.load(open(COMP, encoding="utf-8"))
    errores = valida(comp, sellados_hoy(comp))
    for e in errores:
        print("FAIL", e)
    print(f"real: {len(comp.get('celdas', []))} celdas R comparadas, {len(errores)} defectos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
