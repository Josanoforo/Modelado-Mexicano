#!/usr/bin/env python3
"""TENDENCIA-SERIE: mínimos cuadrados en logit sobre TODAS las olas
anteriores comparables (>= 2), sin ningún parámetro que alguien elija.

Extraído de `tools/encig_origen_movil.py` (piso homónimo de
`ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1`), el único que FP-852f (b)
(`ADR-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01`) manda al duelo
como RETADOR. `tests/test_tendencia_serie.py` la reproduce byte a byte
contra ese CALC sellado.
"""
from __future__ import annotations

import math

Z95 = 1.959964


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _expit(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def tendencia_serie(olas: list[tuple[float, float, float, float]], objetivo: float) -> dict | None:
    """`olas`: [(año, p, ic95_lo, ic95_hi), ...] anteriores a `objetivo`,
    todas comparables. None si hay menos de 2 olas o los años no varían."""
    if len(olas) < 2:
        return None
    anios = [a for a, *_ in olas]
    xbar = sum(anios) / len(anios)
    sxx = sum((x - xbar) ** 2 for x in anios)
    if sxx <= 0:
        return None
    w = [1.0 / len(anios) + (objetivo - xbar) * (x - xbar) / sxx for x in anios]
    logits = [_logit(p) for _, p, _, _ in olas]
    ees = [(_logit(hi) - _logit(lo)) / (2.0 * Z95) for _, _, lo, hi in olas]
    L = sum(wi * li for wi, li in zip(w, logits))
    ee = math.sqrt(sum((wi * ei) ** 2 for wi, ei in zip(w, ees)))
    return {"p": _expit(L), "lo": _expit(L - Z95 * ee), "hi": _expit(L + Z95 * ee)}
