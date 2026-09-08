#!/usr/bin/env python3
"""Medidor de CALC-MOTOR-celdas-semilla -- el MOTOR MATRICIAL, con cadena.

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, P3(e).

## Por qué existe

`ADR-91` (17/ago/2026, `PR #246`) selló, verbatim de mesa, «M1 cómputo
matricial como definición del ejecutable». `D11` de `ACTO GEN2-E3-1`
(`ADR-396`) declaró ese mismo ejecutable «scaffold histórico». Esta corrida
es la demostración de que la ruta matricial también nace con cadena
SPEC->CALC->INPUTS/HASHES->CÓDIGO FIJADO->ENTORNO->EJECUCIÓN->RESULT: no
mide nada de México, y por eso `cuenta_gen2: NO` (D-1, regla E.1).

## Qué corre de verdad, y qué no

Se ejerce lo que el árbol de hoy permite ejercer, y lo que no, se DECLARA
con su razón medida -- no se rellena:

  · `momentos.cargar_catalogo()` -> corre. 22 momentos, roles sellados.
  · `motor.celdas_semilla()` -> corre. Las tres celdas-D del disco.
  · el muro `AJUSTE`/`HOLDOUT` -> se ejerce de verdad: se toca cada HOLDOUT
    por el único camino permitido y se comprueba que `valor_de` LANZA.
  · `procedencia.cargar()` -> **LANZA** `ClaseDesconocida` sobre
    `milpa/procedencia.yaml` (dos valores de `clase:` que
    `milpa/src/clases.py` no conoce). Sin `Procedencia` no hay `B`, y sin
    `B` no hay `matriz.g(B, θ(x))` ni `motor.evaluar()`.

Ese último punto es el HALLAZGO de esta corrida, y es exactamente la
consecuencia de haber declarado el motor «scaffold»: el ejecutable sellado
por `ADR-91` no arranca hoy, y nadie lo notó porque nada lo corría. Se mide
y se reporta; NO se parchea -- `milpa/src/**` está fuera del perímetro de
`ACTO GEN2-T9` (el motor se corre, no se edita).

A.13: todo negativo declara cuántos archivos examinó el comando que lo
produjo. `RESULT-MOTOR-ARCHIVOS-EXAMINADOS` lo lleva.
"""
from __future__ import annotations

import io
import os
import sys

# CUATRO `dirname`, no tres: este archivo vive en
# `data/corrida0/<CALC>/medidor.py`, asi que tres niveles llegan a `data/`
# y no a la raiz. Con tres funcionaba solo por accidente -- `corrida0` se
# invoca desde la raiz y el CWD ya estaba en `sys.path`; el dia que se
# invocara desde otro sitio, el import del motor habria reventado.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


def medir(inputs: dict, contrato: dict) -> dict:
    from milpa.src import celdas as _celdas
    from milpa.src import clases as _clases
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

    # ── 5 · B y θ: hasta dónde llega el ejecutable HOY ────────────────────
    #
    # No se envuelve en un `except Exception` genérico: se nombra la clase de
    # falla que se está midiendo. Cualquier otra reventaría la corrida, que
    # es lo correcto -- un medidor que se traga lo que no esperaba convierte
    # un defecto nuevo en un RESULT tranquilizador.
    try:
        proc = _procedencia.cargar()
        examinados += 1
        matriz_B = __import__("milpa.src.matriz", fromlist=["cargar_B"]).cargar_B(proc)
        estado_b = "CARGA"
        detalle_b = (f"B carga con {matriz_B.no_cero} celdas no-cero, "
                     f"{len(matriz_B.puntuales)} puntuales y "
                     f"{len(matriz_B.sin_magnitud)} sin magnitud")
        veredictos = ";".join(
            f"{r.celda_id}={r.veredicto}"
            for r in (_motor.evaluar(c, catalogo, matriz_B) for _, c in semillas))
    except _clases.ClaseDesconocida as exc:
        examinados += 1
        estado_b = "NO-EJECUTABLE"
        detalle_b = (
            f"`procedencia.cargar()` LANZA ClaseDesconocida sobre "
            f"milpa/procedencia.yaml: {exc}. Sin Procedencia no hay B, sin B "
            f"no hay g(B, theta(x)) ni motor.evaluar(). El ejecutable sellado "
            f"por ADR-91 no arranca hoy.")
        veredictos = "NO-EVALUABLE-SIN-B"

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
        "RESULT-MOTOR-ARCHIVOS-EXAMINADOS": examinados,
    }
