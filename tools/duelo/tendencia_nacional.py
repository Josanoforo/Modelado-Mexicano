#!/usr/bin/env python3
"""Contendientes mecánicos a nivel NACIONAL y validación de origen móvil,
genéricos sobre una serie de puntos sellados (ola, p, IC95).

ACTO `GEN2-DUELO-ENVIPE2026-COMMIT-1` (21/sep/2026). Diseño v1.0 de MOTOR
(`forense/prereg-caja/DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` §2) y
enmienda F7(A): «El COMMIT-1 corre, como ensayo de punta a punta, la
validación de origen móvil de K, T3, T5 y TC sobre la serie sellada (cada
ola predicha solo con las anteriores), rotulada RETROSPECTIVA-MECÁNICA».

Este módulo no sabe qué instrumento produjo la serie ni qué estimando es:
recibe `Punto(ola, p, lo, hi, comparable)` y devuelve predicciones. No
selecciona variante: las cuatro se emiten siempre, construibles o no.

CONTENDIENTES (escala: proporción; todo ajuste en LOGIT)
--------------------------------------------------------
  K    persistencia t−1: el último punto anterior a t, con su IC95 sellado.
  T3   tendencia lineal en logit sobre las ÚLTIMAS 3 olas anteriores a t.
  T5   ídem, últimas 5.
  TC   ídem, todas las olas anteriores comparables; exige ≥ 6 (con ≤ 5
       coincidiría con T3 o T5 y no sería una variante: el diseño §2 asienta
       TC NO-CONSTRUIBLE para una serie de 3 puntos).
  Una variante con menos puntos de los que su ventana exige es
  NO-CONSTRUIBLE (p = None, estado dicho), nunca se rellena con otra.
  Sólo entran al ajuste los puntos con `comparable=True`; el punto
  predicho también tiene que serlo.

  IC95 de T*: la predicción OLS es lineal en los logits de los puntos,
  ŷ_t = Σ c_i·y_i con c_i = 1/n + (t − x̄)(x_i − x̄)/Sxx; con EE_i del punto
  i en proporción (EE = (hi − lo)/3.92) llevado a logit por delta
  (EE_logit = EE/(p(1−p))) y puntos independientes entre olas,
  Var(ŷ_t) = Σ c_i²·EE_logit_i². IC95 = expit(ŷ_t ± 1.96·√Var). Cubre la
  incertidumbre muestral de los puntos que alimentan la recta, NO el error
  de especificación de la tendencia — y se dice así en la spec.

  E+ (marginal por eje): logit(p_eje,t) = logit(p_eje,t') + [logit(T*_t) −
  logit(p_nac,t')]; `e_mas()` da el punto; `e_mas_replicas()` propaga la
  ola t' réplica a réplica (covarianza eje/nacional respetada por réplicas
  compartidas) y el término T* como normal en logit con su EE, sorteo
  independiente (las olas anteriores a t' son muestras independientes).

ORIGEN MÓVIL
------------
  Para cada ola t comparable (desde la primera en que algún contendiente
  es construible), cada contendiente predice t sólo con olas < t. Se emite,
  por (contendiente, t): predicción, error en pp con signo, |error|, si R
  cae dentro del IC95 del candidato, si el punto del candidato cae dentro
  del IC95 de R. Resumen por contendiente: MAE, n de olas, cobertura con
  intervalo de Wilson al 95 %, sobre TODAS sus olas construibles y sobre la
  VENTANA COMÚN (olas donde los cuatro son construibles). Sin selección.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

CONTENDIENTES = ("K", "T3", "T5", "TC")
VENTANA = {"T3": 3, "T5": 5, "TC": None}
MINIMO = {"K": 1, "T3": 3, "T5": 5, "TC": 6}
Z95 = 1.959963984540054


class SerieError(ValueError):
    pass


@dataclass(frozen=True)
class Punto:
    ola: int
    p: float
    lo: float | None = None
    hi: float | None = None
    comparable: bool = True

    def ee(self) -> float | None:
        if self.lo is None or self.hi is None:
            return None
        return (self.hi - self.lo) / 3.92


@dataclass(frozen=True)
class Prediccion:
    contendiente: str
    ola_objetivo: int
    p: float | None
    ic95: tuple | None
    estado: str                 # CONSTRUIBLE · NO-CONSTRUIBLE-<razón>
    olas_usadas: tuple
    pendiente_logit: float | None = None


def _logit(p):
    if p is None or not (0.0 < p < 1.0):
        return None
    return math.log(p / (1.0 - p))


def _expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def _ordenada(serie: list[Punto]) -> list[Punto]:
    olas = [q.ola for q in serie]
    if len(set(olas)) != len(olas):
        raise SerieError(f"olas repetidas en la serie: {olas}")
    return sorted(serie, key=lambda q: q.ola)


def anteriores(serie: list[Punto], t: int) -> list[Punto]:
    """Puntos comparables con ola < t, en orden."""
    return [q for q in _ordenada(serie) if q.ola < t and q.comparable]


def predice(serie: list[Punto], t: int, contendiente: str) -> Prediccion:
    if contendiente not in CONTENDIENTES:
        raise SerieError(f"contendiente {contendiente!r} no es uno de {CONTENDIENTES}")
    prev = anteriores(serie, t)
    if contendiente == "K":
        if not prev:
            return Prediccion("K", t, None, None, "NO-CONSTRUIBLE-SIN-OLA-ANTERIOR", ())
        q = prev[-1]
        ic = None if q.lo is None or q.hi is None else (float(q.lo), float(q.hi))
        return Prediccion("K", t, float(q.p), ic, "CONSTRUIBLE", (q.ola,))
    w = VENTANA[contendiente]
    usados = prev if w is None else prev[-w:]
    if len(usados) < MINIMO[contendiente]:
        return Prediccion(contendiente, t, None, None,
                          f"NO-CONSTRUIBLE-SERIE-INSUFICIENTE({len(usados)}<{MINIMO[contendiente]})",
                          tuple(q.ola for q in usados))
    y = [_logit(q.p) for q in usados]
    if any(v is None for v in y):
        return Prediccion(contendiente, t, None, None, "NO-CONSTRUIBLE-PUNTO-DEGENERADO",
                          tuple(q.ola for q in usados))
    x = np.array([q.ola for q in usados], dtype=float)
    y = np.array(y, dtype=float)
    xb, yb = x.mean(), y.mean()
    sxx = float(((x - xb) ** 2).sum())
    b = float(((x - xb) * (y - yb)).sum() / sxx)
    yhat = yb + b * (t - xb)
    c = 1.0 / len(x) + (t - xb) * (x - xb) / sxx
    ee = [q.ee() for q in usados]
    ic = None
    if all(e is not None for e in ee):
        ee_logit = np.array([e / (q.p * (1.0 - q.p)) for e, q in zip(ee, usados)])
        var = float((c ** 2 * ee_logit ** 2).sum())
        ic = (_expit(yhat - Z95 * math.sqrt(var)), _expit(yhat + Z95 * math.sqrt(var)))
    return Prediccion(contendiente, t, _expit(yhat), ic, "CONSTRUIBLE",
                      tuple(q.ola for q in usados), pendiente_logit=b)


def e_mas(p_eje_prev: float, p_nac_prev: float, t_star: float) -> float | None:
    """Punto de E+ para un eje: expit(logit p_eje,t' + logit T* − logit p_nac,t')."""
    a, b, c = _logit(p_eje_prev), _logit(p_nac_prev), _logit(t_star)
    if a is None or b is None or c is None:
        return None
    return _expit(a + c - b)


def e_mas_replicas(reps_eje: np.ndarray, reps_nac: np.ndarray,
                   t_star: float, ee_t_star: float | None,
                   rng: np.random.Generator) -> np.ndarray:
    """Réplicas de E+: réplica k del eje y del nacional (misma ola, mismo
    remuestreo) + T* como normal en logit con EE_logit = EE/(T*(1−T*)),
    sorteo independiente. NaN donde algún término no está definido."""
    a, b = np.asarray(reps_eje, float), np.asarray(reps_nac, float)
    ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (a < 1) & (b > 0) & (b < 1)
    lt = _logit(t_star)
    if lt is None:
        return np.full(len(a), np.nan)
    z = np.zeros(len(a)) if ee_t_star is None else rng.standard_normal(len(a))
    ee_logit = 0.0 if ee_t_star is None else ee_t_star / (t_star * (1.0 - t_star))
    with np.errstate(all="ignore"):
        out = np.log(a / (1 - a)) - np.log(b / (1 - b)) + lt + z * ee_logit
        return np.where(ok, 1.0 / (1.0 + np.exp(-out)), np.nan)


# ══ origen móvil ══════════════════════════════════════════════════════════

def wilson(k: int, n: int) -> tuple | None:
    if n <= 0:
        return None
    p = k / n
    den = 1 + Z95 ** 2 / n
    centro = (p + Z95 ** 2 / (2 * n)) / den
    semi = Z95 * math.sqrt(p * (1 - p) / n + Z95 ** 2 / (4 * n * n)) / den
    return (max(0.0, centro - semi), min(1.0, centro + semi))


def origen_movil(serie: list[Punto], contendientes=CONTENDIENTES) -> dict:
    """RETROSPECTIVA-MECÁNICA: cada ola comparable predicha sólo con las
    anteriores. Devuelve {"por_ola": {t: {cont: {...}}}, "resumen": {cont:
    {...}}, "ventana_comun": [olas]}. No selecciona nada."""
    serie = _ordenada(serie)
    objetivos = [q for q in serie if q.comparable]
    por_ola: dict = {}
    for q in objetivos:
        t = q.ola
        fila = {}
        for cid in contendientes:
            pr = predice(serie, t, cid)
            r_ic = None if q.lo is None or q.hi is None else (float(q.lo), float(q.hi))
            if pr.p is None:
                fila[cid] = {"estado": pr.estado, "pred": None, "ic95": None,
                             "error_pp": None, "abs_error_pp": None,
                             "R_en_ic_cand": None, "cand_en_ic_R": None,
                             "olas_usadas": pr.olas_usadas, "pendiente_logit": None}
                continue
            err = 100.0 * (pr.p - q.p)
            fila[cid] = {
                "estado": pr.estado, "pred": pr.p, "ic95": pr.ic95,
                "error_pp": err, "abs_error_pp": abs(err),
                "R_en_ic_cand": (None if pr.ic95 is None
                                 else bool(pr.ic95[0] <= q.p <= pr.ic95[1])),
                "cand_en_ic_R": (None if r_ic is None
                                 else bool(r_ic[0] <= pr.p <= r_ic[1])),
                "olas_usadas": pr.olas_usadas, "pendiente_logit": pr.pendiente_logit}
        if any(f["pred"] is not None for f in fila.values()):
            por_ola[t] = fila
    comun = [t for t, fila in por_ola.items()
             if all(fila[c]["pred"] is not None for c in contendientes)]

    def _resumen(cid, olas):
        filas = [por_ola[t][cid] for t in olas if por_ola[t][cid]["pred"] is not None]
        n = len(filas)
        if n == 0:
            return {"n_olas": 0, "mae_pp": None, "sesgo_pp": None,
                    "cobertura_R_en_ic_cand": None, "cobertura_ic95": None,
                    "n_cobertura": 0, "cand_en_ic_R_frac": None}
        cob = [f["R_en_ic_cand"] for f in filas if f["R_en_ic_cand"] is not None]
        cir = [f["cand_en_ic_R"] for f in filas if f["cand_en_ic_R"] is not None]
        return {"n_olas": n,
                "mae_pp": float(np.mean([f["abs_error_pp"] for f in filas])),
                "sesgo_pp": float(np.mean([f["error_pp"] for f in filas])),
                "cobertura_R_en_ic_cand": (sum(cob) / len(cob)) if cob else None,
                "cobertura_ic95": wilson(sum(cob), len(cob)) if cob else None,
                "n_cobertura": len(cob),
                "cand_en_ic_R_frac": (sum(cir) / len(cir)) if cir else None,
                "olas": [t for t in olas if por_ola[t][cid]["pred"] is not None]}

    resumen = {cid: {"todas": _resumen(cid, list(por_ola)),
                     "ventana_comun": _resumen(cid, comun)} for cid in contendientes}
    return {"rotulo": "RETROSPECTIVA-MECANICA", "por_ola": por_ola,
            "resumen": resumen, "ventana_comun": comun,
            "olas_no_comparables": [q.ola for q in serie if not q.comparable]}
