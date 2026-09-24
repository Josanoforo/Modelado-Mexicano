"""Dictamen de serie por conducta y segmento — DONDE-CAMBIO spec v1.0.

Aplica, sin parámetros libres, `forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md`
(vocabulario y desempate sellados en `9aea5a09`) sobre el mapa de series
(`forense/analisis/donde-cambio/mapa/*.tsv`, sólo ids) y los RESULT sellados
que el mapa cita. No abre microdato. El primer resultado que produzca este
procedimiento es el que se reporta.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

Z = 1.959964
VOCAB = ("SIN-SERIE", "CAMBIO-SOSTENIDO", "SALTO-DE-INSTRUMENTO",
         "SALTO-SIN-EXPLICAR", "ESTABLE")
UNE = ("COMPARABLE", "CAMBIO-DOCUMENTADO")          # estados que unen el tramo
TAU2_SELLADO = {"ENIF", "ENCIG"}                     # spec §3 puntos 1 y 2

# ---------------------------------------------------------------- utilidades

def _logit(x):
    return math.log(x / (1 - x))


def _expit(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    y = math.exp(x)
    return y / (1 + y)


def _abierto(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) \
        and math.isfinite(x) and 0 < x < 1


def lee_mapa(texto):
    """TSV del mapa -> lista de dicts (split por tab; no módulo csv)."""
    lineas = [l for l in texto.splitlines() if l.strip()]
    cab = lineas[0].split("\t")
    filas = []
    for l in lineas[1:]:
        c = l.split("\t")
        c += [""] * (len(cab) - len(c))
        filas.append(dict(zip(cab, c)))
    return filas


def series_de(filas):
    s = defaultdict(list)
    for f in filas:
        s[f["serie_id"]].append(f)
    for k in s:
        s[k].sort(key=lambda f: f["ola"])
    return dict(s)


# ------------------------------------------------------------ tramo y pares

def tramo(olas):
    """Corrida más larga de olas unidas por COMPARABLE/CAMBIO-DOCUMENTADO
    (desempate: la más reciente) con p, lo, hi en (0,1). spec §2."""
    corridas, actual = [], []
    for i, o in enumerate(olas):
        valida = all(_abierto(o.get(x)) for x in ("p", "lo", "hi"))
        une = i > 0 and o["par_con_anterior"] in UNE
        if valida and (une and actual):
            actual.append(o)
        else:
            if actual:
                corridas.append(actual)
            actual = [o] if valida else []
    if actual:
        corridas.append(actual)
    if not corridas:
        return []
    mejor = corridas[0]
    for c in corridas[1:]:
        if len(c) >= len(mejor):
            mejor = c
    return mejor


def pares(tr):
    out = []
    for a, b in zip(tr, tr[1:]):
        ee = (_logit(a["hi"]) - _logit(a["lo"])) / (2 * Z)
        out.append({"a": a, "b": b, "ee": ee,
                    "delta": _logit(b["p"]) - _logit(a["p"]),
                    "estado": b["par_con_anterior"],
                    "marca_2020": b.get("marca_2020", "NO")})
    return out


# -------------------------------------------------------------- tau² (§3.3)

def tau2_por_eje(series_tramos):
    """series_tramos: {serie_id: (eje, [pares])}. Media entre pares de olas
    (peso igual) de la media dentro del par de Δ², sólo pares COMPARABLE."""
    por_eje = defaultdict(lambda: defaultdict(list))
    for eje, prs in series_tramos.values():
        for p in prs:
            if p["estado"] == "COMPARABLE":
                por_eje[eje][(p["a"]["ola"], p["b"]["ola"])].append(p["delta"] ** 2)
    tau = {}
    for eje, d in por_eje.items():
        medias = [sum(v) / len(v) for v in d.values() if v]
        if medias:
            tau[eje] = sum(medias) / len(medias)
    return tau


def tau2_para(eje, tau):
    if eje in tau:
        return tau[eje]
    if tau:
        return sum(tau.values()) / len(tau)
    return None


# ------------------------------------------------------------- dictamen §4

def dictamina(prs, t2, k):
    if k < 3 or t2 is None:
        return {"dictamen": "SIN-SERIE", "direccion": "", "n_fuera": 0,
                "fuera": []}
    fuera = []
    for p in prs:
        s = math.sqrt(p["ee"] ** 2 + t2)
        lo = _expit(_logit(p["a"]["p"]) - Z * s)
        hi = _expit(_logit(p["a"]["p"]) + Z * s)
        p["ic_lo"], p["ic_hi"] = lo, hi
        p["fuera"] = not (lo <= p["b"]["p"] <= hi)
        if p["fuera"]:
            fuera.append(p)
    comp = [p for p in fuera if p["estado"] == "COMPARABLE"]
    sube = sum(1 for p in comp if p["delta"] > 0)
    baja = sum(1 for p in comp if p["delta"] < 0)
    doc = [p for p in fuera if p["estado"] == "CAMBIO-DOCUMENTADO"]
    if max(sube, baja) >= 2 and sube != baja:
        d, dr = "CAMBIO-SOSTENIDO", ("SUBE" if sube > baja else "BAJA")
    elif doc:
        d, dr = "SALTO-DE-INSTRUMENTO", ""
    elif comp:
        d, dr = "SALTO-SIN-EXPLICAR", ""
    else:
        d, dr = "ESTABLE", ""
    return {"dictamen": d, "direccion": dr, "n_fuera": len(fuera),
            "fuera": fuera}


# ----------------------------------------------------------- orquestación

def evalua(filas, valores, tau_sellado=None, instrumento=None):
    """filas: mapa de UN instrumento; valores: {result_id: float};
    tau_sellado: {eje: τ²} si el instrumento es ENIF/ENCIG (spec §3.1-2)."""
    ser = series_de(filas)
    tramos = {}
    for sid, olas in ser.items():
        for o in olas:
            o["p"] = valores.get(o["result_p"])
            o["lo"] = valores.get(o["result_lo"]) if o["result_lo"] else None
            o["hi"] = valores.get(o["result_hi"]) if o["result_hi"] else None
        tr = tramo(olas)
        tramos[sid] = (olas[0]["eje"], tr, pares(tr))
    if tau_sellado is not None:
        tau, fuente = dict(tau_sellado), "SELLADO"
    else:
        tau = tau2_por_eje({s: (e, p) for s, (e, _, p) in tramos.items()})
        fuente = "CALCULADO-AQUI"
    out = {}
    for sid, (eje, tr, prs) in sorted(tramos.items()):
        t2 = tau2_para(eje, tau)
        r = dictamina(prs, t2, len(tr))
        r.update({"k": len(tr), "tau2": t2, "olas": [o["ola"] for o in tr],
                  "delta_pp": (100 * (tr[-1]["p"] - tr[0]["p"]) if len(tr) >= 2 else None),
                  "pares": prs, "eje": eje})
        out[sid] = r
    return out, tau, fuente
