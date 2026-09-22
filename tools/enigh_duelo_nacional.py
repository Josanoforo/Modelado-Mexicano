#!/usr/bin/env python3
"""Contendientes mecánicos a nivel NACIONAL para el duelo prospectivo ENIGH
2024, y validación de origen móvil sobre la serie ya sellada de `remesas>0`.

ACTO `GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P4. Molde declarado en
`forense/prereg-caja/DISENO-duelo-prospectivo-ENIGH2024-v1_0.md` §4
(contendientes) y §5 (origen móvil, rotulado RETROSPECTIVA-MECÁNICA).

**No es `tools/duelo/tendencia_nacional.py`, aunque comparte el mismo diseño
matemático (regresión OLS en logit, IC por método delta).** Ese módulo está
`ajeno` al perímetro de este acto (declarado en la cabecera del encargo:
«Perímetro: ... ajeno: `tools/duelo/`, sellos, celdas-D») — este archivo se
escribe entero, propio, en vez de editarlo o importarlo. El conjunto de
contendientes también difiere: ENIGH tiene 4 olas máximo en su ventana
(2016-2022), así que `TC` (mínimo 6 olas del molde de ENVIPE) siempre saldría
NO-CONSTRUIBLE aquí y no es una variante útil; el diseño ENIGH pide en su
lugar `C-T2` (tendencia de 2, no existe en el molde de ENVIPE) y `C-MEDIA`
(media de la serie en logit, tampoco existe allá).

CONTENDIENTES (escala: proporción; todo ajuste en LOGIT, DISEÑO §4.1)
-----------------------------------------------------------------------
  C-PISO   persistencia t−1: el último punto anterior a t, con su IC95 sellado.
  C-T2     tendencia lineal en logit sobre las ÚLTIMAS 2 olas anteriores a t.
  C-T3     ídem, últimas 3.
  C-TS     ídem, TODAS las olas anteriores comparables (mínimo 2 -- con la
           ventana de 4 olas de ENIGH, "toda la serie" nunca excede 3 puntos
           de historia antes del punto nuevo).
  C-MEDIA  media en logit de todas las olas anteriores comparables (mínimo 1).
  Una variante con menos puntos de los que exige es NO-CONSTRUIBLE
  (p = None, estado dicho), nunca se rellena con otra.

  IC95 de C-T2/C-T3/C-TS: igual método que el molde de ENVIPE (delta desde
  el EE en proporción de cada punto, llevado a logit, propagado por los
  pesos de la predicción OLS). C-MEDIA usa el mismo método con pesos
  uniformes 1/n. C-PISO usa el IC95 sellado del punto que persiste.

ORIGEN MÓVIL (RETROSPECTIVA-MECÁNICA, DISEÑO §5.2)
-----------------------------------------------------------------------
  Para cada ola t de la serie sellada, cada contendiente predice t sólo con
  olas < t de la misma serie. Se emite, por (contendiente, t): predicción,
  error en pp con signo, |error|, si R cae dentro del IC95 del candidato, si
  el punto del candidato cae dentro del IC95 de R. Resumen por contendiente:
  MAE, sesgo, n de olas, cobertura de Wilson. Corre ANTES de que exista el
  dato de 2024 -- no lo toca, no lo necesita.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

CONTENDIENTES = ("C-PISO", "C-T2", "C-T3", "C-TS", "C-MEDIA")
VENTANA = {"C-T2": 2, "C-T3": 3, "C-TS": None}
MINIMO = {"C-PISO": 1, "C-T2": 2, "C-T3": 3, "C-TS": 2, "C-MEDIA": 1}
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
    estado: str
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
    return [q for q in _ordenada(serie) if q.ola < t and q.comparable]


def _ic_ols(t, usados, yhat, c):
    ee = [q.ee() for q in usados]
    if not all(e is not None for e in ee):
        return None
    ee_logit = np.array([e / (q.p * (1.0 - q.p)) for e, q in zip(ee, usados)])
    var = float((c ** 2 * ee_logit ** 2).sum())
    return (_expit(yhat - Z95 * math.sqrt(var)), _expit(yhat + Z95 * math.sqrt(var)))


def predice(serie: list[Punto], t: int, contendiente: str) -> Prediccion:
    if contendiente not in CONTENDIENTES:
        raise SerieError(f"contendiente {contendiente!r} no es uno de {CONTENDIENTES}")
    prev = anteriores(serie, t)

    if contendiente == "C-PISO":
        if not prev:
            return Prediccion("C-PISO", t, None, None, "NO-CONSTRUIBLE-SIN-OLA-ANTERIOR", ())
        q = prev[-1]
        ic = None if q.lo is None or q.hi is None else (float(q.lo), float(q.hi))
        return Prediccion("C-PISO", t, float(q.p), ic, "CONSTRUIBLE", (q.ola,))

    if contendiente == "C-MEDIA":
        if len(prev) < MINIMO["C-MEDIA"]:
            return Prediccion("C-MEDIA", t, None, None,
                              f"NO-CONSTRUIBLE-SERIE-INSUFICIENTE({len(prev)}<{MINIMO['C-MEDIA']})",
                              tuple(q.ola for q in prev))
        y = [_logit(q.p) for q in prev]
        if any(v is None for v in y):
            return Prediccion("C-MEDIA", t, None, None, "NO-CONSTRUIBLE-PUNTO-DEGENERADO",
                              tuple(q.ola for q in prev))
        yhat = float(np.mean(y))
        c = np.full(len(prev), 1.0 / len(prev))
        ic = _ic_ols(t, prev, yhat, c)
        return Prediccion("C-MEDIA", t, _expit(yhat), ic, "CONSTRUIBLE",
                          tuple(q.ola for q in prev))

    # C-T2 / C-T3 / C-TS: regresion OLS en logit sobre la ventana declarada.
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
    if sxx == 0.0:
        # Dos puntos con la misma "ola" no pueden ocurrir (llaves unicas),
        # pero una ventana de 1 punto util (p.ej. C-T2 con un solo punto
        # comparable tras filtrar) cae aqui: no hay pendiente que ajustar.
        return Prediccion(contendiente, t, None, None,
                          "NO-CONSTRUIBLE-SIN-VARIANZA-EN-X",
                          tuple(q.ola for q in usados))
    b = float(((x - xb) * (y - yb)).sum() / sxx)
    yhat = yb + b * (t - xb)
    c = 1.0 / len(x) + (t - xb) * (x - xb) / sxx
    ic = _ic_ols(t, usados, yhat, c)
    return Prediccion(contendiente, t, _expit(yhat), ic, "CONSTRUIBLE",
                      tuple(q.ola for q in usados), pendiente_logit=b)


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
    anteriores de la misma serie sellada. No toca ENIGH2024."""
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
                    "n_cobertura": 0, "cand_en_ic_R_frac": None, "olas": []}
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


def coincidencias(serie: list[Punto], t: int) -> dict:
    """Comprueba por comando (DISEÑO §4.2, «se comprueba por comando antes
    de congelar») si dos contendientes dan el MISMO número para la ola t --
    p.ej. C-T3 y C-TS coinciden exactamente cuando hay exactamente 3 olas
    anteriores disponibles, porque usan la misma ventana."""
    preds = {cid: predice(serie, t, cid) for cid in CONTENDIENTES}
    pares = []
    ids = list(CONTENDIENTES)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = preds[ids[i]], preds[ids[j]]
            if a.p is not None and b.p is not None and a.p == b.p:
                pares.append((ids[i], ids[j], a.p))
    return {"ola": t, "coincidencias_exactas": pares,
            "predicciones": {cid: pr.p for cid, pr in preds.items()}}
