#!/usr/bin/env python3
"""Medidor de CALC-MOTOR-celdas-semilla-v2 -- el MOTOR MATRICIAL, ejercido.

`ACTO AUTO-MOTOR-1 · RECUPERA-Y-EJERCITA`, sucesor de
`CALC-MOTOR-celdas-semilla` (`ACTO GEN2-T9`, `NC-0023`).

## Qué cambió respecto al predecesor

El predecesor midió que `procedencia.cargar()` LANZABA `ClaseDesconocida`
sobre dos valores de `clase:` sin prefijo reconocido
(`REFUTADO-POR-COTA`, `EVIDENCIA_EXPERIMENTAL_TERCEROS`). Este acto les da
prefijo propio (`milpa/src/clases.py`) y corrige la ambigüedad que dejaba
reingresar el prior refutado como `ASIGNADO` del bloque que lo contiene
(`milpa/src/procedencia.py`). Esta corrida ejerce la ruta completa que el
predecesor no pudo alcanzar: `procedencia.cargar()` -> `matriz.cargar_B()`
-> `motor.evaluar()` sobre las tres celdas-D semilla.

## Qué sigue sin ser (y por qué eso no es un defecto)

`motor.evaluar()` no calcula ninguna cifra de México: E0 se detiene en un
veredicto de ESTADO antes de calibrar (`universo_candidatos` está POR
DECLARAR, calibración E1+ tras el cierre de BARRIDO-2). Esta corrida no
cambia eso -- ejercita el camino, no adelanta la calibración. Un veredicto
`EXISTE-NO-VERIFICADO` o `EXISTE-NO-SATISFACE` aquí es un resultado nativo
correcto, no una falla del medidor.

## cuenta_gen2: NO

Regla E.1 (`ACTO GEN2-T9`, D-1, verbatim: «decisión 1 no cuentan como
Gen2»): el motor consume `milpa/procedencia.yaml` entre sus inputs, así
que esta corrida no cuenta como GEN2 por completa que sea su cadena --
misma regla, misma razón que el predecesor.

## Sin `except` genérico

Ninguna de las cinco llamadas de abajo está envuelta en `except Exception`:
si `procedencia.cargar()` volviera a lanzar (una clase nueva sin prefijo,
por ejemplo), esta corrida debe reventar, no reportar un `RESULT`
tranquilizador. Sustituir la excepción por un resultado calmado es
exactamente el defecto que el encargo prohíbe.

A.13: todo negativo declara cuántos archivos examinó el comando que lo
produjo. `RESULT-MOTOR-ARCHIVOS-EXAMINADOS` lo lleva.
"""
from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


def medir(inputs: dict, contrato: dict) -> dict:
    from milpa.src import celdas as _celdas
    from milpa.src import clases as _clases
    from milpa.src import matriz as _matriz
    from milpa.src import momentos as _momentos
    from milpa.src import motor as _motor
    from milpa.src import procedencia as _procedencia

    examinados = 0

    # ── 1 · el catálogo de momentos, sellado ──────────────────────────────
    catalogo = _momentos.cargar_catalogo()
    examinados += 1
    ajuste = _momentos.momentos_ajuste(catalogo)
    holdout = _momentos.momentos_holdout(catalogo)

    # ── 2 · el muro, EJERCIDO -- no declarado ─────────────────────────────
    intocados = 0
    for m in holdout:
        try:
            _momentos.valor_de(m)
        except _momentos.HoldoutTocado:
            intocados += 1
        else:
            raise AssertionError(
                f"`{m.id_momento}` devolvió valor siendo HOLDOUT: el muro de "
                f"pre-registro no está puesto")

    # ── 3 · las celdas-D del disco ────────────────────────────────────────
    semillas = _motor.celdas_semilla()
    examinados += len(semillas)
    ids_celdas = ";".join(sorted(str(c.get("id")) for _, c in semillas))

    # ── 4 · la malla declarada de π ───────────────────────────────────────
    cortes = _celdas.CORTES_C1
    examinados += 1

    # ── 5 · procedencia -> B -> evaluar(), de punta a punta ───────────────
    proc = _procedencia.cargar()
    examinados += 1
    matriz_B = _matriz.cargar_B(proc)
    estado_b = "CARGA"
    detalle_b = (f"B carga con {matriz_B.no_cero} celdas no-cero, "
                 f"{len(matriz_B.puntuales)} puntuales y "
                 f"{len(matriz_B.sin_magnitud)} sin magnitud")
    resultados_celda = [
        _motor.evaluar(c, catalogo, matriz_B) for _, c in semillas
    ]
    veredictos = ";".join(
        f"{r.celda_id}={r.veredicto}" for r in resultados_celda)

    # ── 6 · el contrato de las dos clases nuevas, medido sobre lo que
    #    `cargar()` de verdad produjo -- no declarado.
    refutadas = proc.por_clase(_clases.Clase.REFUTADO_POR_COTA)
    evidencia_terceros = proc.por_clase(
        _clases.Clase.EVIDENCIA_EXPERIMENTAL_TERCEROS)
    consumibles_llaves = {e.llave for e in proc.consumibles()}
    refutadas_en_consumibles = sum(
        1 for e in refutadas if e.llave in consumibles_llaves)
    examinados += 1

    return {
        "RESULT-MOTOR-MOMENTOS-TOTAL": len(catalogo),
        "RESULT-MOTOR-MOMENTOS-AJUSTE": len(ajuste),
        "RESULT-MOTOR-MOMENTOS-HOLDOUT": len(holdout),
        "RESULT-MOTOR-HOLDOUT-INTOCADOS": intocados,
        "RESULT-MOTOR-CELDAS-SEMILLA": len(semillas),
        "RESULT-MOTOR-CELDAS-IDS": ids_celdas,
        "RESULT-MOTOR-CORTES-SELLADOS": len(cortes.sellados),
        "RESULT-MOTOR-CORTES-PENDIENTES": len(cortes.pendientes),
        "RESULT-MOTOR-ESTADO-B": estado_b,
        "RESULT-MOTOR-DETALLE-B": detalle_b,
        "RESULT-MOTOR-VEREDICTOS": veredictos,
        "RESULT-MOTOR-REFUTADO-POR-COTA-N": len(refutadas),
        "RESULT-MOTOR-REFUTADO-POR-COTA-CONSUMIBLE": refutadas_en_consumibles,
        "RESULT-MOTOR-EVIDENCIA-TERCEROS-N": len(evidencia_terceros),
        "RESULT-MOTOR-ARCHIVOS-EXAMINADOS": examinados,
    }
