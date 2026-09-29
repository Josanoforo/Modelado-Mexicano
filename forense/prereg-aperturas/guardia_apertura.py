#!/usr/bin/env python3
"""Guardia E.6 de apertura, compartida por los expedientes de `forense/prereg-aperturas/`.

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (28/sep/2026). Qué defecto real atrapa:
NC-0328 (una reserva quemada por un script de scratch que cruzó dos variables) y
el precedente de `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (auditoría AST dentro del
medidor). Aquí la guardia es la misma semántica, en un solo sitio, para que
cada expediente la importe en vez de copiarla.

Tres piezas, ninguna de prosa:

  1. `auditoria_ast(fuente)` — lee el código (no lo ejecuta) y devuelve la lista
     de violaciones: `groupby`/`value_counts` con más de una llave, `crosstab`,
     `pivot`/`pivot_table`/`unstack`, y lecturas `read_*` fuera de la función
     autorizada `lee_payload_reservado`. Cero violaciones = pasa.
  2. `proporcion_por_grupo(y, w, grupo)` — el ÚNICO agregador autorizado sobre
     la ola reservada: razón ponderada Σw·y/Σw por categoría de UNA variable de
     agrupación. Recibir una lista/tupla/matriz de agrupación levanta
     `ParoDeGuardia` (mismo nombre que los medidores sellados).
  3. `adjudica_cobertura(celdas)` — regla fijada antes de abrir: cobertura =
     «R dentro del IC del candidato» (§4 v2.16), con Wilson; dictamen de
     vocabulario cerrado CALIBRADO · SUBCUBRE · SOBRECUBRE · NO-ESTIMABLE.

Nada de este archivo abre dato. Sólo numpy.
"""
from __future__ import annotations

import ast
import math

import numpy as np

Z95 = 1.959964
NOMINAL = 0.95
VOCABULARIO = ("CALIBRADO", "SUBCUBRE", "SOBRECUBRE", "NO-ESTIMABLE")
_PROHIBIDAS = {"crosstab", "pivot", "pivot_table", "unstack"}
_AGRUPADORAS = {"groupby", "value_counts"}
LECTOR_AUTORIZADO = "lee_payload_reservado"


class ParoDeGuardia(RuntimeError):
    pass


# ── 1 · auditoría estática ──────────────────────────────────────────────────
def _n_llaves(nodo: ast.AST) -> int:
    if isinstance(nodo, (ast.List, ast.Tuple, ast.Set)):
        return len(nodo.elts)
    return 1


def auditoria_ast(fuente: str) -> list[str]:
    arbol = ast.parse(fuente)
    padres = {}
    for p in ast.walk(arbol):
        for h in ast.iter_child_nodes(p):
            padres[h] = p
    viol = []
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Call):
            continue
        f = nodo.func
        nombre = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
        if nombre in _PROHIBIDAS:
            viol.append(f"L{nodo.lineno}: {nombre} prohibido sobre ola reservada")
        if nombre in _AGRUPADORAS:
            llaves = [a for a in nodo.args[:1]] + [k.value for k in nodo.keywords if k.arg in ("by", "subset")]
            if any(_n_llaves(a) > 1 for a in llaves):
                viol.append(f"L{nodo.lineno}: {nombre} con más de una variable de agrupación")
        if nombre.startswith("read_") or nombre in ("lee_dta", "lee_csv_zip"):
            dueno = nodo
            while dueno in padres and not isinstance(dueno, ast.FunctionDef):
                dueno = padres[dueno]
            if not (isinstance(dueno, ast.FunctionDef) and dueno.name == LECTOR_AUTORIZADO):
                viol.append(f"L{nodo.lineno}: lectura {nombre} fuera de {LECTOR_AUTORIZADO}")
    return viol


def exige_auditoria(fuente: str) -> None:
    v = auditoria_ast(fuente)
    if v:
        raise ParoDeGuardia("auditoría AST: " + "; ".join(v))


# ── 2 · único agregador autorizado ──────────────────────────────────────────
def proporcion_por_grupo(y, w, grupo) -> dict:
    """{categoría: {"p": float|None, "n": int}} con UNA variable de agrupación.

    `grupo` es un vector 1-D de etiquetas (None/NaN = fuera). Una lista de
    vectores, una tupla o una matriz 2-D es un cruce y levanta ParoDeGuardia.
    """
    if isinstance(grupo, (list, tuple)) and grupo and not np.isscalar(grupo[0]) and grupo[0] is not None:
        raise ParoDeGuardia("más de una variable de agrupación")
    g = np.asarray(grupo, dtype=object)
    if g.ndim != 1:
        raise ParoDeGuardia("agrupación no unidimensional (cruce)")
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    if not (len(y) == len(w) == len(g)):
        raise ParoDeGuardia("longitudes discordantes")
    out = {}
    valido = np.isfinite(y) & np.isfinite(w) & (w > 0)
    cats = sorted({c for c in g.tolist() if c is not None and not (isinstance(c, float) and math.isnan(c))}, key=str)
    for c in cats:
        m = valido & (g == c)
        den = float(w[m].sum())
        out[c] = {"p": (float((w[m] * y[m]).sum()) / den) if den > 0 else None, "n": int(m.sum())}
    return out


# ── 3 · adjudicación fijada antes de abrir ─────────────────────────────────
def wilson(k: int, n: int, z: float = Z95):
    if n == 0:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)  # acotado: el redondeo daba -3e-18 o 1+2e-16 (_valida_outputs lo rechaza)


def adjudica_cobertura(celdas) -> dict:
    """`celdas`: iterable de dicts {"lo","hi","r","punto","conglomerado"}.

    Puntúa sólo celdas con lo, hi, r finitos. Primaria: k/n de R∈[lo,hi] con
    Wilson; CALIBRADO si 0.95 ∈ Wilson, SUBCUBRE si Wilson_hi < 0.95,
    SOBRECUBRE si Wilson_lo > 0.95, NO-ESTIMABLE si n = 0. Secundarias
    (descriptivas, no adjudican): error absoluto medio punto-vs-R y cobertura
    por conglomerado.
    """
    k = n = 0
    errs, por = [], {}
    for c in celdas:
        lo, hi, r = c.get("lo"), c.get("hi"), c.get("r")
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in (lo, hi, r)):
            continue
        dentro = int(lo <= r <= hi)
        k += dentro
        n += 1
        g = por.setdefault(c.get("conglomerado", "-"), [0, 0])
        g[0] += dentro
        g[1] += 1
        pt = c.get("punto")
        if isinstance(pt, (int, float)) and math.isfinite(pt):
            errs.append(abs(pt - r))
    lo_w, hi_w = wilson(k, n)
    if n == 0:
        dic = "NO-ESTIMABLE"
    elif hi_w < NOMINAL:
        dic = "SUBCUBRE"
    elif lo_w > NOMINAL:
        dic = "SOBRECUBRE"
    else:
        dic = "CALIBRADO"
    return {"k": k, "n": n, "wilson_lo": lo_w, "wilson_hi": hi_w, "dictamen": dic,
            "mae_punto": (sum(errs) / len(errs)) if errs else None,
            "por_conglomerado": {g: {"k": a, "n": b} for g, (a, b) in sorted(por.items())}}
