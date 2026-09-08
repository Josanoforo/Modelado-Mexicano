#!/usr/bin/env python3
"""Medidor de CALC-AGG-marco-M-sorteado-v1_3 -- agregado SUCESOR, derivado.

ACTO GEN2-E7 · READINESS-2 · Pieza A, A4.

## Corrida DERIVADA

Este agregado no vuelve a medir nada. Sus insumos son los `resultados.json`
de otros CALC del mismo arbol -- archivos **versionados**, con SHA declarado
en la spec y verificados por `preflight` como cualquier otro input
`origen: repo`. Por eso `ci_replayable: true`: cualquiera con el arbol puede
reproducir esta corrida sin corpus, sin red y sin claves.

## Qué lo separa de `agregado_v1_3.py` (LEGACY)

`agregado_v1_3.py` resuelve sus insumos por **convencion de nombre de
archivo** sobre el legado GEN1: `ORDEN_RESOLUCION_M = ("M-{id}__v1_3.json",
"M-{id}.json", "M-{id}__v1_2.json")`, listando `corridas-M/`, `corridas-R/` y
`corridas-L/` en disco. Un archivo suelto en cualquiera de esos tres
directorios entra a la cifra sin que nada lo declare.

Este sucesor consume **solo** `RESULT-R/M/L` por celda, y solo los que una
spec declara. Lo que no esta declarado no entra. `agregado_v1_3.py` queda
LEGACY y vive como smoke (`CALC-SMOKE-0001`), no como productor.

## Los ejes que HOY no se pueden estimar

R y L todavia no tienen corrida GEN2: la de R necesita corpus y va a caja
(E5 o despues); la de L necesita al modelo y su corredor sucesor esta en
readiness, CONTADOR cero. Este agregado **no rellena ese hueco**: reporta
`n_con_R = 0`, `n_con_L = 0` y deja los ejes M-vs-R y M-vs-L en
NO-ESTIMABLE con el motivo dicho. Lo que puede afirmar de M lo afirma; lo
que no, lo declara.

El delta contra la cifra GEN1 de `agregado-v1_3-resultado.json` NO se calcula
aqui: mientras R y L no tengan corrida GEN2, un delta contra el agregado
legado compararia dos cosas distintas. Cuando exista, el encargo lo permite
como `valor_legacy` -- una lectura declarada, no un insumo.
"""
from __future__ import annotations

import csv
import io
import json
import statistics

MARCO_VIGENTE = "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv"
COLUMNA_ELEGIBLE = "elegible_v1_1"

MOTIVO_SIN_R = ("NO-ESTIMABLE -- ninguna celda tiene RESULT-R GEN2: la corrida "
                "de R necesita corpus (data/raw/) y va a caja, E5 o despues")
MOTIVO_SIN_L = ("NO-ESTIMABLE -- ninguna celda tiene RESULT-L GEN2: el corredor "
                "L sucesor esta en readiness, CONTADOR cero (no se llamo al modelo)")


def _texto(entrada: dict) -> str:
    crudo = entrada.get("bytes")
    if crudo is None:
        raise RuntimeError(
            f"input {entrada.get('id')!r} llego sin `bytes` -- este agregado "
            f"solo consume insumos `origen: repo` del snapshot resuelto")
    return crudo.decode("utf-8")


def _results_de(entrada: dict) -> dict:
    """El bloque `resultados` de un `resultados.json` de otro CALC. Se leen los
    MISMOS bytes que el SHA de la spec identifica -- no una relectura de disco."""
    return json.loads(_texto(entrada))["resultados"]


def medir(inputs: dict, contrato: dict) -> dict:
    marco = list(csv.DictReader(
        io.StringIO(_texto(inputs["IN-MARCO-M-SORTEADO-V1-3"])), delimiter="\t"))
    ids = [f["id"] for f in marco
           if (f.get(COLUMNA_ELEGIBLE) or "").strip().upper() == "SI"]

    res_m = _results_de(inputs["IN-CALC-M-RESULTADOS"])

    # Los insumos R y L GEN2 son OPCIONALES por declaracion: la spec no los
    # trae hoy porque no existen. El dia que existan, entran por aqui sin
    # tocar este medidor -- se agregan a la spec y su sha los identifica.
    res_r = _results_de(inputs["IN-CALC-R-RESULTADOS"]) if "IN-CALC-R-RESULTADOS" in inputs else {}
    res_l = _results_de(inputs["IN-CALC-L-RESULTADOS"]) if "IN-CALC-L-RESULTADOS" in inputs else {}

    puntos_m, con_r, con_l = [], 0, 0
    for id_celda in ids:
        p = res_m.get(f"RESULT-M-{id_celda}-P")
        if p is not None:
            puntos_m.append(float(p))
        if res_r.get(f"RESULT-R-{id_celda}-PUNTO") is not None:
            con_r += 1
        if res_l.get(f"RESULT-L-{id_celda}-PUNTO") is not None:
            con_l += 1

    return {
        "RESULT-AGG-N-CELDAS": len(ids),
        "RESULT-AGG-N-CON-M": len(puntos_m),
        "RESULT-AGG-N-CON-R": con_r,
        "RESULT-AGG-N-CON-L": con_l,
        "RESULT-AGG-M-P-MEDIANA": statistics.median(puntos_m) if puntos_m else None,
        "RESULT-AGG-M-P-MIN": min(puntos_m) if puntos_m else None,
        "RESULT-AGG-M-P-MAX": max(puntos_m) if puntos_m else None,
        # El mismo dato del paso 3 que CALC-M mide, re-derivado aqui desde los
        # RESULT-M: si el agregado y el corredor no coinciden, algo se movio
        # entre las dos corridas y el `verify` de ambos lo va a decir.
        "RESULT-AGG-M-P-DISTINTOS": len({round(p, 12) for p in puntos_m}),
        "RESULT-AGG-EJE-M-VS-R": MOTIVO_SIN_R if con_r == 0 else "ESTIMABLE",
        "RESULT-AGG-EJE-M-VS-L": MOTIVO_SIN_L if con_l == 0 else "ESTIMABLE",
        "RESULT-AGG-CI-REPLAYABLE": (
            "true -- todos los insumos son archivos versionados del arbol "
            "(resultados.json de otros CALC + el marco vigente), con sha "
            "declarado en la spec; no hay corpus, red ni clave en el camino"),
        "RESULT-AGG-FUENTES": " | ".join(
            f"{e['id']}={e.get('ruta', e.get('origen'))}"
            for e in sorted(inputs.values(), key=lambda x: x["id"])),
    }
