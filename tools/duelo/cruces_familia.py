#!/usr/bin/env python3
"""Familia de contendientes a nivel CRUCE, genérica sobre (instrumento, par).

ACTO `GEN2-DUELO-ENVIPE2026-COMMIT-1` (21/sep/2026). Firma de mesa F7(B),
verbatim: «A nivel cruce entra la misma familia del lote ENIF —C2,
persistencia, interacción cruda, interacción encogida, ajuste proporcional—
sobre los dos pares cuyo cruce de 2025 ya está abierto». Este archivo es la
IMPLEMENTACIÓN DE REFERENCIA que el lote ENIF 2024 reutiliza: no sabe qué es
ENVIPE, ENIF ni una ola; recibe celdas ya estimadas (punto, IC95 del árbitro,
réplicas bootstrap, n) y devuelve candidatos y adjudicación. El cableado a un
instrumento vive fuera (`tools/duelo/envipe_duelo.py` para ENVIPE).

QUÉ NO HACE
-----------
  · No abre archivos. No conoce columnas, ponderadores ni universos.
  · No cruza nada: los cruces de olas ANTERIORES llegan hechos (por el
    guardián del instrumento, que es quien decide si puede cruzar).
  · No elige candidato: `adjudica()` aplica la regla declarada y devuelve el
    veredicto de cada retador contra el piso, sin ordenar ni escoger.

CONTENDIENTES (escala: proporción; toda combinación en LOGIT)
-------------------------------------------------------------
  C2   piso log-aditivo sobre los marginales de la ola NUEVA t:
       expit(logit m_t(a) + logit m_t(b) − logit m_t)            [réplica k]
  P    persistencia: el cruce de la ola anterior t' tal cual: x_t'(a,b)
  S1   interacción cruda: expit(logit C2_t + Ī(a,b)),
       Ī = media sobre las olas anteriores disponibles de
       I_w(a,b) = logit x_w(a,b) − [logit m_w(a) + logit m_w(b) − logit m_w]
  Sλ   interacción encogida: expit(logit C2_t + λ·Ī(a,b)),
       λ = τ̂²/(τ̂² + σ̄²), τ̂² = max(0, Var_entre(Ī) − σ̄²), Var_entre con
       ddof=1 sobre las celdas con Ī finito, σ̄² = media de Var(Ī_réplicas)
       por celda — método de momentos, el mismo que el piloto 3 selló
       (`GOB-gobierno-digital-exe15-spec-v1_1.md` §3.1).
  AP   ajuste proporcional: la persistencia desplazada por el cambio del
       nacional, en logit: expit(logit x_t'(a,b) + logit m_t − logit m_t').
       Es el análogo de celda de E+ (diseño §2); se llama así por F7(B) y se
       hace en logit por la primera línea del diseño («toda combinación de
       niveles se hace en logit»). NO es un cociente de proporciones.

Las réplicas se combinan índice a índice (réplica k de la ola t con réplica
k de la ola t'): muestras independientes entre olas, sin covarianzas
inventadas — la convención del piloto 2 (`CALC-TRA-EVADE-NORMA-SXD-
EMISIONES-0001`). Un término fuera de (0,1) deja la réplica en NaN
(SIN-DEFINIR), nunca se recorta.

ADJUDICACIÓN (regla del lote ENIF v0.3, propuesta de dirección 21/sep/2026)
---------------------------------------------------------------------------
«diferencia de error medio entre C2 y la interacción encogida sobre las
celdas puntuadas, con IC95 por réplica; vence si despeja 0.5 pp; propuesta
con reserva si despeja 0 y no 0.5; nadie vence si incluye 0.»
  ΔMAE(j) = MAE(C2) − MAE(j) en pp sobre las PUNTUADAS; IC95 = percentiles
  2.5/97.5 de ΔMAE_k, con R_k, C2_k y j_k de la MISMA réplica k.
  VENCE-RETADOR si IC95inf > 0.5 · PROPUESTA-CON-RESERVA si 0 < IC95inf ≤ 0.5
  · NADIE-VENCE en otro caso (incluye IC95sup < 0: el piso se sostiene, y
  se dice con el signo). Retador primario: Sλ. Los demás se adjudican con la
  misma regla, rotulados SECUNDARIA.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

CANDIDATOS = ("C2", "P", "S1", "SL", "AP")
ROTULO = {"C2": "piso log-aditivo (marginales de la ola nueva)",
          "P": "persistencia (cruce de la ola anterior)",
          "S1": "interaccion cruda (C2 + I media de olas anteriores)",
          "SL": "interaccion encogida (C2 + lambda * I media)",
          "AP": "ajuste proporcional (persistencia + desplazamiento nacional, logit)"}
PISO = "C2"
RETADOR_PRIMARIO = "SL"
VEREDICTOS = ("VENCE-RETADOR", "PROPUESTA-CON-RESERVA", "NADIE-VENCE",
              "NO-ADJUDICABLE")


class FamiliaError(ValueError):
    """Entrada mal formada: no se rellena, se levanta."""


@dataclass(frozen=True)
class Celda:
    """Una celda estimada por el instrumento. `replicas` es un vector de
    réplicas bootstrap (NaN donde la réplica no está definida) o None.
    `ic95` es el IC del árbitro del instrumento (no se recalcula aquí)."""
    p: float | None
    ic95: tuple | None = None
    replicas: np.ndarray | None = field(default=None, repr=False, compare=False)
    n: int | None = None


@dataclass(frozen=True)
class Marginales:
    """Marginales de UNA ola: `a` y `b` son {categoria: Celda}; `nac` es la
    celda nacional. `orden_a`/`orden_b` fijan el orden de las celdas del par."""
    a: dict
    b: dict
    nac: Celda
    orden_a: tuple
    orden_b: tuple


@dataclass(frozen=True)
class OlaAnterior:
    """Cruce y marginales de una ola anterior, ya derivados por el
    instrumento. `rotulo` identifica la ola (p. ej. '2024')."""
    rotulo: str
    cruce: dict          # {(ka, kb): Celda}
    marginales: Marginales


# ══ aritmética en logit, réplica a réplica ═══════════════════════════════

def _logit(p: float | None) -> float | None:
    if p is None or not np.isfinite(p) or not (0.0 < p < 1.0):
        return None
    return math.log(p / (1.0 - p))


def _expit(z: float | None) -> float | None:
    if z is None or not np.isfinite(z):
        return None
    return 1.0 / (1.0 + math.exp(-z))


def _logit_arr(r: np.ndarray | None) -> np.ndarray | None:
    if r is None:
        return None
    r = np.asarray(r, dtype=float)
    ok = np.isfinite(r) & (r > 0.0) & (r < 1.0)
    with np.errstate(all="ignore"):
        return np.where(ok, np.log(r / (1.0 - r)), np.nan)


def _expit_arr(z: np.ndarray | None) -> np.ndarray | None:
    if z is None:
        return None
    with np.errstate(all="ignore"):
        return np.where(np.isfinite(z), 1.0 / (1.0 + np.exp(-z)), np.nan)


def _suma(*partes):
    """Suma de puntos: None si alguno falta."""
    if any(x is None for x in partes):
        return None
    return float(sum(partes))


def _suma_arr(*partes):
    if any(x is None for x in partes):
        return None
    largos = {len(x) for x in partes}
    if len(largos) != 1:
        raise FamiliaError(f"réplicas de largos distintos: {sorted(largos)}")
    return np.sum(np.vstack(partes), axis=0)   # NaN se propaga


def _celdas_del_par(m: Marginales):
    return [(ka, kb) for ka in m.orden_a for kb in m.orden_b]


# ══ contendientes ═════════════════════════════════════════════════════════

def c2(m: Marginales) -> dict:
    """C2 por celda del par: punto y réplicas. Punto None si algún marginal
    es degenerado (0, 1 o ausente): NO-CONSTRUIBLE, sin recorte."""
    out = {}
    ln = _logit(m.nac.p)
    lnr = _logit_arr(m.nac.replicas)
    for ka, kb in _celdas_del_par(m):
        ca, cb = m.a[ka], m.b[kb]
        z = _suma(_logit(ca.p), _logit(cb.p), None if ln is None else -ln)
        zr = None
        if ca.replicas is not None and cb.replicas is not None and lnr is not None:
            zr = _suma_arr(_logit_arr(ca.replicas), _logit_arr(cb.replicas), -lnr)
        out[(ka, kb)] = Celda(p=_expit(z), replicas=_expit_arr(zr))
    return out


def interaccion(o: OlaAnterior) -> dict:
    """I_w(a,b) = logit x_w(a,b) − [logit m_w(a) + logit m_w(b) − logit m_w]
    en la escala LOGIT (no se devuelve a proporción). {celda: (punto, reps)}."""
    m = o.marginales
    ln, lnr = _logit(m.nac.p), _logit_arr(m.nac.replicas)
    out = {}
    for ka, kb in _celdas_del_par(m):
        x = o.cruce.get((ka, kb))
        if x is None:
            raise FamiliaError(f"la ola {o.rotulo} no trae la celda {(ka, kb)}")
        ca, cb = m.a[ka], m.b[kb]
        punto = _suma(_logit(x.p), None if _logit(ca.p) is None else -_logit(ca.p),
                      None if _logit(cb.p) is None else -_logit(cb.p), ln)
        reps = None
        if all(v is not None for v in (x.replicas, ca.replicas, cb.replicas, lnr)):
            reps = _suma_arr(_logit_arr(x.replicas), -_logit_arr(ca.replicas),
                             -_logit_arr(cb.replicas), lnr)
        out[(ka, kb)] = (punto, reps)
    return out


def interaccion_media(interacciones: list[dict]) -> dict:
    """Ī por celda: media aritmética de las olas dadas, punto y réplica a
    réplica. None/NaN si alguna ola no la define."""
    if not interacciones:
        raise FamiliaError("se necesita al menos una ola anterior para Ī")
    celdas = list(interacciones[0])
    out = {}
    for c in celdas:
        puntos = [i[c][0] for i in interacciones]
        reps = [i[c][1] for i in interacciones]
        punto = None if any(p is None for p in puntos) else float(np.mean(puntos))
        r = None if any(x is None for x in reps) else np.mean(np.vstack(reps), axis=0)
        out[c] = (punto, r)
    return out


def lambda_encogimiento(ibar: dict) -> dict:
    """λ por método de momentos sobre las celdas con Ī y varianza finitas.
    Devuelve {lambda, tau2, sigma2_medio, var_entre, k}; λ None si k < 2 o
    si la varianza total es 0 (no se inventa)."""
    puntos, s2 = [], []
    for punto, reps in ibar.values():
        if punto is None or reps is None:
            continue
        ok = reps[np.isfinite(reps)]
        if len(ok) < 2:
            continue
        puntos.append(punto)
        s2.append(float(np.var(ok, ddof=1)))
    k = len(puntos)
    if k < 2:
        return {"lambda": None, "tau2": None, "sigma2_medio": None,
                "var_entre": None, "k": k}
    var_entre = float(np.var(puntos, ddof=1))
    sigma2 = float(np.mean(s2))
    tau2 = max(0.0, var_entre - sigma2)
    den = tau2 + sigma2
    lam = (tau2 / den) if den > 0 else None
    return {"lambda": lam, "tau2": tau2, "sigma2_medio": sigma2,
            "var_entre": var_entre, "k": k}


def desplazada(c2_celdas: dict, ibar: dict, factor: float | None) -> dict:
    """expit(logit C2 + factor·Ī) por celda (S1 con factor 1, Sλ con λ)."""
    out = {}
    for c, base in c2_celdas.items():
        punto, reps = ibar[c]
        if factor is None or punto is None:
            z, zr = None, None
        else:
            z = _suma(_logit(base.p), factor * punto)
            zr = None
            if base.replicas is not None and reps is not None:
                zr = _suma_arr(_logit_arr(base.replicas), factor * reps)
        out[c] = Celda(p=_expit(z), replicas=_expit_arr(zr))
    return out


def persistencia(o: OlaAnterior) -> dict:
    """El cruce de la ola anterior, tal cual (punto, IC95 del árbitro,
    réplicas, n)."""
    return {c: o.cruce[c] for c in _celdas_del_par(o.marginales)}


def ajuste_proporcional(o: OlaAnterior, nac_t: Celda) -> dict:
    """expit(logit x_t'(a,b) + logit m_t − logit m_t'), réplica k con k."""
    ln_t, ln_p = _logit(nac_t.p), _logit(o.marginales.nac.p)
    lr_t, lr_p = _logit_arr(nac_t.replicas), _logit_arr(o.marginales.nac.replicas)
    out = {}
    for c in _celdas_del_par(o.marginales):
        x = o.cruce[c]
        z = _suma(_logit(x.p), ln_t, None if ln_p is None else -ln_p)
        zr = None
        if x.replicas is not None and lr_t is not None and lr_p is not None:
            zr = _suma_arr(_logit_arr(x.replicas), lr_t, -lr_p)
        out[c] = Celda(p=_expit(z), replicas=_expit_arr(zr))
    return out


def familia(m_t: Marginales, anteriores: list[OlaAnterior]) -> dict:
    """Los cinco contendientes sobre (instrumento, par), de golpe y sin
    selección. `anteriores` va de la más antigua a la más reciente; P y AP
    usan la MÁS RECIENTE, S1/Sλ la media de todas. Devuelve
    {"candidatos": {id: {celda: Celda}}, "meta": {...}}."""
    if not anteriores:
        raise FamiliaError("la familia exige al menos una ola anterior")
    celdas = _celdas_del_par(m_t)
    for o in anteriores:
        if _celdas_del_par(o.marginales) != celdas:
            raise FamiliaError(f"la ola {o.rotulo} no comparte el par/orden de la ola nueva")
    ultima = anteriores[-1]
    inter = [interaccion(o) for o in anteriores]
    ibar = interaccion_media(inter)
    lam = lambda_encogimiento(ibar)
    c2_ = c2(m_t)
    cand = {"C2": c2_,
            "P": persistencia(ultima),
            "S1": desplazada(c2_, ibar, 1.0),
            "SL": desplazada(c2_, ibar, lam["lambda"]),
            "AP": ajuste_proporcional(ultima, m_t.nac)}
    meta = {"olas_anteriores": [o.rotulo for o in anteriores],
            "ola_persistencia": ultima.rotulo,
            "lambda": lam, "interaccion_media": ibar,
            "interacciones": dict(zip([o.rotulo for o in anteriores], inter)),
            "celdas": celdas}
    return {"candidatos": cand, "meta": meta}


# ══ soporte y adjudicación ════════════════════════════════════════════════

def puntuadas(n_por_ola: dict, umbral: int) -> dict:
    """{celda: True} si n ≥ umbral en TODAS las olas dadas ({rotulo: {celda:
    n}}); n None cuenta como no puntuada."""
    celdas = None
    for rot, ns in n_por_ola.items():
        celdas = set(ns) if celdas is None else celdas & set(ns)
    out = {}
    for c in sorted(celdas or []):
        out[c] = all((ns.get(c) is not None) and ns[c] >= umbral
                     for ns in n_por_ola.values())
    return out


def ic95_de(celda: Celda) -> tuple | None:
    """IC95 percentil 2.5/97.5 de las réplicas finitas; None si no hay."""
    if celda.replicas is None:
        return None
    ok = celda.replicas[np.isfinite(celda.replicas)]
    if len(ok) == 0:
        return None
    return (float(np.percentile(ok, 2.5)), float(np.percentile(ok, 97.5)))


def _dentro(p, ic):
    if p is None or ic is None:
        return None
    return bool(ic[0] <= p <= ic[1])


def adjudica(R: dict, candidatos: dict, puntuada: dict, *,
             piso: str = PISO, retador: str = RETADOR_PRIMARIO,
             umbral_vence_pp: float = 0.5, umbral_reserva_pp: float = 0.0) -> dict:
    """Regla v0.3. `R` = {celda: Celda} del árbitro (ola nueva, con IC95 del
    árbitro y réplicas); `candidatos` = salida de `familia()["candidatos"]`.
    Devuelve por candidato: error por celda (pp), dentro-IC-R, MAE, y ΔMAE
    contra el piso con IC95 por réplica y veredicto. No ordena, no escoge."""
    if piso not in candidatos:
        raise FamiliaError(f"piso {piso!r} no está entre los candidatos")
    celdas_p = [c for c, ok in puntuada.items() if ok]
    out = {"piso": piso, "retador_primario": retador,
           "celdas_puntuadas": len(celdas_p), "umbral_vence_pp": umbral_vence_pp,
           "umbral_reserva_pp": umbral_reserva_pp, "candidatos": {}}

    def _err_reps(cand_c: Celda, r_c: Celda):
        if cand_c.replicas is None or r_c.replicas is None:
            return None
        return 100.0 * np.abs(np.asarray(cand_c.replicas) - np.asarray(r_c.replicas))

    for cid, celdas in candidatos.items():
        filas, errores, err_reps = {}, [], []
        for c, r_c in R.items():
            k = celdas.get(c)
            e = (None if (k is None or k.p is None or r_c.p is None)
                 else 100.0 * abs(k.p - r_c.p))
            ic_k = ic95_de(k) if k is not None else None
            filas[c] = {"p": None if k is None else k.p, "ic95": ic_k,
                        "error_pp": e,
                        "dentro_ic_R": _dentro(None if k is None else k.p, r_c.ic95),
                        "R_dentro_ic_cand": _dentro(r_c.p, ic_k),
                        "puntuada": bool(puntuada.get(c, False))}
            if puntuada.get(c, False):
                errores.append(e)
                err_reps.append(None if k is None else _err_reps(k, r_c))
        mae = (None if (not errores or any(e is None for e in errores))
               else float(np.mean(errores)))
        mae_reps = (None if (not err_reps or any(x is None for x in err_reps))
                    else np.mean(np.vstack(err_reps), axis=0))
        out["candidatos"][cid] = {"celdas": filas, "mae_pp": mae,
                                  "_mae_reps": mae_reps}

    base = out["candidatos"][piso]
    for cid, r in out["candidatos"].items():
        if cid == piso:
            r.update({"delta_mae_pp": None, "delta_ic95": None,
                      "veredicto": "PISO", "rol": "PISO"})
            continue
        d = (None if (base["mae_pp"] is None or r["mae_pp"] is None)
             else base["mae_pp"] - r["mae_pp"])
        ic = None
        if base["_mae_reps"] is not None and r["_mae_reps"] is not None:
            dr = base["_mae_reps"] - r["_mae_reps"]
            ok = dr[np.isfinite(dr)]
            if len(ok):
                ic = (float(np.percentile(ok, 2.5)), float(np.percentile(ok, 97.5)))
        if d is None or ic is None:
            v = "NO-ADJUDICABLE"
        elif ic[0] > umbral_vence_pp:
            v = "VENCE-RETADOR"
        elif ic[0] > umbral_reserva_pp:
            v = "PROPUESTA-CON-RESERVA"
        else:
            v = "NADIE-VENCE"
        r.update({"delta_mae_pp": d, "delta_ic95": ic, "veredicto": v,
                  "rol": "PRIMARIA" if cid == retador else "SECUNDARIA",
                  "piso_se_sostiene": (None if ic is None else bool(ic[1] < 0))})
    for r in out["candidatos"].values():
        r.pop("_mae_reps", None)
    return out
