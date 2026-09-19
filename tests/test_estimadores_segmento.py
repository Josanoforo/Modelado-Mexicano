#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `milpa/src/estimadores_segmento.py` / `motor.estimar_segmento`.

ACTO GEN2-MARCADOR-REDISENO-1 (adenda, P2). Dos casos, verbatim del
encargo: pedir una celda adoptada devuelve punto+IC+unidad_dato; pedir una
celda marginal SIN-PISO devuelve `None`.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from milpa.src import estimadores_segmento as ES  # noqa: E402
from milpa.src import motor as MOTOR  # noqa: E402

FALLOS: list[str] = []


def _falla(caso, msg):
    FALLOS.append(f"{caso}: {msg}")


def t_celda_adoptada_devuelve_punto_ic_unidad():
    r = ES.estimador_de_celda(
        "CRUCE::TRA.evade_norma.envipe2025.escolaridad_x_dominio::S1xD1")
    if r is None:
        _falla("T-ADOPTADA", "celda C2 conocida devolvió None")
        return
    for campo in ("punto", "ic95_inf", "ic95_sup", "unidad_dato"):
        if campo not in r or r[campo] in (None, ""):
            _falla("T-ADOPTADA", f"falta o vacío el campo {campo!r} en {r}")
    if r.get("unidad_dato") != "delito":
        _falla("T-ADOPTADA", f"TRA debía traer unidad_dato=delito, trajo {r.get('unidad_dato')!r}")


def t_celda_marginal_sin_piso_devuelve_none():
    r = ES.estimador_de_celda(
        "MARG::tramite.evasion_norma_ejes_envipe2025::sexo::1 Hombre")
    if r is not None:
        _falla("T-SIN-PISO", f"celda marginal SIN-PISO debía devolver None, devolvió {r}")


def t_motor_expone_el_punto_de_entrada():
    if not hasattr(MOTOR, "estimar_segmento"):
        _falla("T-MOTOR-ENTRYPOINT", "milpa.src.motor no expone estimar_segmento")
        return
    if "estimar_segmento" not in MOTOR.__all__:
        _falla("T-MOTOR-ENTRYPOINT", "estimar_segmento no está en motor.__all__")
    r = MOTOR.estimar_segmento("NO-EXISTE-NUNCA")
    if r is not None:
        _falla("T-MOTOR-ENTRYPOINT", "id inexistente debía devolver None")


CASOS = (t_celda_adoptada_devuelve_punto_ic_unidad,
         t_celda_marginal_sin_piso_devuelve_none,
         t_motor_expone_el_punto_de_entrada)


def corre() -> list[str]:
    FALLOS.clear()
    for caso in CASOS:
        caso()
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    if fallos:
        print(f"FALLA -- {len(fallos)} caso(s):")
        for f in fallos:
            print(f"  - {f}")
        return 1
    print(f"PASA -- {len(CASOS)} casos de tests/test_estimadores_segmento.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
