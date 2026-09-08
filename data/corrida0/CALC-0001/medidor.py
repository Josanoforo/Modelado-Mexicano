"""`CALC-0001` — falsador S12 sobre CIDE-CSES 2015 (zanahoria/garrote + encuadre).

Interfaz estable del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO EN `ACTO GEN2-E5-0` Y **NO EJECUTADO EN ÉL**: E5-0 termina en el COMMIT-1
y tiene prohibido abrir microdato. Lo corre `ACTO GEN2-E5`. Que el `preflight` de
este CALC salga VERDE certifica la DECLARACION (esquema de la spec, identidad de
los inputs, estado del arbol) — NO certifica el numero que este archivo produzca.
"""
from __future__ import annotations

import numpy as np
import pyreadstat

# Faltantes declarados por el codebook, por variable. Nunca se infieren.
_NS_DICOTOMICA = {9.0, 8.0}


def _dicotomiza(serie, si=1.0, no=2.0):
    """1 / 0 / NaN. Cualquier codigo que no sea `si` ni `no` es faltante y se
    CUENTA: la spec exige publicar los NS/NC, no absorberlos en el cero."""
    out = np.full(len(serie), np.nan)
    v = np.asarray(serie, dtype="float64")
    out[v == si] = 1.0
    out[v == no] = 0.0
    return out


def _alineado(oferente, voto, crosswalk, coaliciones):
    """`ALINEADO=1` si el partido votado es el que ofrecio/amenazo. Sale del
    crosswalk congelado en `spec.yaml`, NUNCA de `oferente == voto`: los dos
    esquemas de codigo coinciden en cinco numeros con partidos distintos."""
    out = np.full(len(oferente), np.nan)
    for i, (o, w) in enumerate(zip(oferente, voto)):
        if not np.isfinite(o) or not np.isfinite(w):
            continue
        esperado = crosswalk.get(int(o))
        if esperado is None:          # 97 Ninguno / 99 NS-NC: faltante del brazo
            continue
        aceptados = {esperado} | {c for c, partes in coaliciones.items()
                                  if esperado in partes}
        out[i] = 1.0 if int(w) in aceptados else 0.0
    return out


def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como la cadena
    "NO-ESTIMABLE": `_valida_outputs` rechaza los dos ultimos y solo acepta
    `None` cuando el output declara `permite_no_estimable: true`."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _prop_ponderada(y, w):
    m = np.isfinite(y) & np.isfinite(w) & (w > 0)
    if not m.any():
        return float("nan"), 0
    return float(np.sum(y[m] * w[m]) / np.sum(w[m])), int(m.sum())


def _boot_ic_delta(y, t, w, upm, estrato, b, semilla, n_min):
    """IC95 percentil por bootstrap de UPM dentro de estrato (spec.md §3).
    `NaN` si alguna celda no alcanza `n_min` — la cota de S12 §4."""
    ok = np.isfinite(y) & np.isfinite(t) & np.isfinite(w) & (w > 0)
    if int(np.sum(ok & (t == 1))) < n_min or int(np.sum(ok & (t == 0))) < n_min:
        return float("nan"), float("nan")
    rng = np.random.Generator(np.random.PCG64(semilla))
    idx_por_upm, orden = {}, []
    for i in np.flatnonzero(ok):
        clave = (estrato[i], upm[i])
        if clave not in idx_por_upm:
            idx_por_upm[clave] = []
            orden.append(clave)
        idx_por_upm[clave].append(i)
    por_estrato = {}
    for e, u in orden:
        por_estrato.setdefault(e, []).append((e, u))
    reps = np.empty(b)
    for r in range(b):
        tomadas = []
        for e, claves in por_estrato.items():
            elegidas = rng.integers(0, len(claves), len(claves))
            for k in elegidas:
                tomadas.extend(idx_por_upm[claves[k]])
        s = np.asarray(tomadas)
        p1, _ = _prop_ponderada(y[s][t[s] == 1], w[s][t[s] == 1])
        p0, _ = _prop_ponderada(y[s][t[s] == 0], w[s][t[s] == 0])
        reps[r] = p1 - p0
    reps = reps[np.isfinite(reps)]
    if reps.size < b // 2:
        return float("nan"), float("nan")
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


def _lee(entrada):
    df, _ = pyreadstat.read_sav(entrada["ruta_absoluta"])
    return df


def medir(inputs, contrato):
    p = contrato["parametros"]
    cw = {int(k): int(v) for k, v in p["crosswalk_partido"].items()}
    coal = {int(k): {int(x) for x in v} for k, v in p["coaliciones"].items()}
    n_min, b = int(p["n_minimo_celda"]), int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    pond, upm_v, est_v = p["ponderador"], p["upm"], p["estrato"]
    out: dict[str, object] = {}

    # ── §1 · brazos zanahoria y garrote, por levantamiento y por separado ──
    for etiqueta, pid, desenlace in p["brazos_principales"]:
        df = _lee(inputs[pid])
        w = np.asarray(df[pond], dtype="float64")
        upm = np.asarray(df[upm_v], dtype="float64")
        est = np.asarray(df[est_v], dtype="float64")
        voto = np.asarray(df[desenlace], dtype="float64")
        for brazo, disparador, quien in p["pares_disparador"]:
            t = _dicotomiza(df[disparador])
            y = _alineado(np.asarray(df[quien], dtype="float64"), voto, cw, coal)
            p1, n1 = _prop_ponderada(y[t == 1], w[t == 1])
            p0, n0 = _prop_ponderada(y[t == 0], w[t == 0])
            lo, hi = _boot_ic_delta(y, t, w, upm, est, b, semilla, n_min)
            pre = f"RESULT-C1-{etiqueta}-{brazo}"
            out[f"{pre}-P-T1"] = _num(p1)
            out[f"{pre}-P-T0"] = _num(p0)
            out[f"{pre}-DELTA"] = _num(p1 - p0)
            out[f"{pre}-IC-LO"] = _num(lo)
            out[f"{pre}-IC-HI"] = _num(hi)
            out[f"{pre}-N-T1"] = n1
            out[f"{pre}-N-T0"] = n0
            out[f"{pre}-N-NSNC"] = int(np.sum(~np.isfinite(_dicotomiza(df[disparador]))))
            out[f"{pre}-VEREDICTO"] = _veredicto(p1 - p0, lo, hi)
            out[f"{pre}-DESENLACE"] = desenlace

    # ── §2-bis · encuadre de secreto del voto, con su guardia de diseño ──
    df = _lee(inputs[p["archivo_encuadre"]])
    w = np.asarray(df[pond], dtype="float64")
    cobertura = {}
    for v in p["variables_encuadre"]:
        y = _dicotomiza(df[v])
        cobertura[v] = float(np.mean(np.isfinite(y)))
        pv, nv = _prop_ponderada(y, w)
        out[f"RESULT-C2BIS-{v.upper()}-P"] = _num(pv)
        out[f"RESULT-C2BIS-{v.upper()}-N"] = nv
    split = all(p["cobertura_split_min"] <= c <= p["cobertura_split_max"]
                for c in cobertura.values())
    out["RESULT-C2BIS-DISENO"] = "SPLIT-BALLOT" if split else \
        "NO-ESTIMABLE-DISENO-NO-EXPERIMENTAL"
    out["RESULT-C2BIS-COBERTURA"] = "; ".join(f"{k}={v:.4f}" for k, v in cobertura.items())
    for v in p["variables_encuadre"][:2]:
        pre = f"RESULT-C2BIS-{v.upper()}-VS-NEUTRAL"
        if not split:
            out[f"{pre}-DELTA"] = None
            out[f"{pre}-IC-LO"] = None
            out[f"{pre}-IC-HI"] = None
            continue
        neutral = p["variables_encuadre"][2]
        yv, yn = _dicotomiza(df[v]), _dicotomiza(df[neutral])
        t = np.where(np.isfinite(yv), 1.0, np.where(np.isfinite(yn), 0.0, np.nan))
        y = np.where(np.isfinite(yv), yv, yn)
        lo, hi = _boot_ic_delta(y, t, w,
                                np.asarray(df[upm_v], dtype="float64"),
                                np.asarray(df[est_v], dtype="float64"),
                                b, semilla, n_min)
        pv, _ = _prop_ponderada(yv, w)
        pn, _ = _prop_ponderada(yn, w)
        out[f"{pre}-DELTA"] = _num(pv - pn)
        out[f"{pre}-IC-LO"] = _num(lo)
        out[f"{pre}-IC-HI"] = _num(hi)
    return out


def _veredicto(delta, lo, hi):
    if not np.isfinite(delta) or not np.isfinite(lo) or not np.isfinite(hi):
        return "NO-ESTIMABLE"
    if lo > 0:
        return "CORROBORADA"
    if hi < 0:
        return "CONTRARIA"
    return "NO-DISCRIMINA"
