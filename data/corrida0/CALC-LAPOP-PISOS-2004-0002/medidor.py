"""Pisos LAPOP México por ola: proporciones con IC bootstrap de UPM en estrato.

Gobernado por forense/prereg-caja/LAPOP-PISOS-OLAS-spec-v1_0.md y su
sucesor v1_1 (diagnóstico de peso vacío emite null). El mismo
código, autocontenido, se congela en cada CALC de la familia; lo que cambia
por ola (payload, diseño, reactivos, códigos) viene en `parametros`.
"""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
import pyreadstat


def _clave(df, columnas):
    partes = [df[c].astype("string") for c in columnas]
    clave = partes[0]
    for p in partes[1:]:
        clave = clave + "|" + p
    return clave


def estimate(x, w, estrato, upm, validos, evento, faltantes, seed, reps, n_min):
    """Proporción ponderada de `evento` entre `validos` con IC de diseño."""
    x = pd.to_numeric(x, errors="coerce")
    w = pd.to_numeric(w, errors="coerce")
    sustantivo = x.isin(validos)
    no_resp = x.isna() | x.isin(faltantes)
    fuera = int((~sustantivo & ~no_resp).sum())
    base = {"n_filas": int(len(x)), "n_no_sustantivo": int(no_resp.sum()),
            "n_fuera_de_escala": fuera}
    if fuera:
        return {**base, "estado": "ESCALA-DISCREPANTE", "n": None, "p": None, "ic95": None}
    mask = sustantivo & w.notna() & np.isfinite(w) & (w > 0) & estrato.notna() & upm.notna()
    n = int(mask.sum())
    if n < n_min:
        return {**base, "estado": "NO-ESTIMABLE", "n": n, "p": None, "ic95": None}
    pesos = w[mask].to_numpy(float)
    si = x[mask].isin(evento).to_numpy(bool)
    den = float(pesos.sum())
    p = float(pesos[si].sum()) / den
    grupos = {}
    for e, u, pw, s in zip(estrato[mask].astype(str), upm[mask].astype(str), pesos, si):
        g = grupos.setdefault((e, u), [0.0, 0.0])
        g[0] += pw * s
        g[1] += pw
    estratos = {}
    for (e, _u), par in sorted(grupos.items()):
        estratos.setdefault(e, []).append(par)
    mats = [np.asarray(v) for _k, v in sorted(estratos.items())]
    rng = np.random.Generator(np.random.PCG64(seed))
    draws = []
    for _ in range(reps):
        num = dd = 0.0
        for m in mats:
            idx = rng.integers(0, len(m), len(m)) if len(m) > 1 else np.zeros(1, dtype=int)
            tot = m[idx].sum(axis=0)
            num += float(tot[0])
            dd += float(tot[1])
        draws.append(num / dd if dd else math.nan)
    fin = np.asarray(draws)[np.isfinite(draws)]
    ic = [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))] if len(fin) else None
    return {**base, "estado": "ESTIMADA", "n": n, "n_evento": int(si.sum()), "p": p,
            "ic95": ic, "masa_ponderada": den, "n_estratos": len(mats),
            "n_upm": len(grupos), "replicas_validas": int(len(fin))}


def medir(inputs, contrato):
    par = contrato["parametros"]
    ruta = inputs[par["payload_id"]]["ruta_absoluta"]
    df, _ = pyreadstat.read_dta(ruta)
    dis = par["diseno"]
    necesarias = {dis["estrato"], *dis["upm"], *(it["variable"] for it in par["items"])}
    if dis.get("peso"):
        necesarias.add(dis["peso"])
    faltan = sorted(necesarias - set(df.columns))
    if faltan:
        raise ValueError(f"faltan variables: {faltan}")
    estrato = df[dis["estrato"]]
    upm = _clave(df, dis["upm"])
    w = df[dis["peso"]] if dis.get("peso") else pd.Series(1.0, index=df.index)
    seed = int(contrato["seed"]["valor"])
    reps = int(par["bootstrap_replicas"])
    n_min = int(par["n_minimo"])
    tabla = {}
    for it in par["items"]:
        tabla[it["clave"]] = {
            "variable": it["variable"], "evento": list(it["evento"]),
            **estimate(df[it["variable"]], w, estrato, upm, tuple(it["validos"]),
                       tuple(it["evento"]), tuple(it["faltantes"]),
                       seed + int(it["semilla_desplazamiento"]), reps, n_min)}
    diag = {}
    if dis.get("peso_diagnostico"):
        v = pd.to_numeric(df[dis["peso_diagnostico"]], errors="coerce")
        llenos = v.dropna()
        diag = {"variable": dis["peso_diagnostico"],
                "min": float(llenos.min()) if len(llenos) else None,
                "max": float(llenos.max()) if len(llenos) else None,
                "n_vacios": int(v.isna().sum())}
    salida = {par["result_filas"]: int(len(df))}
    for rid, claves in par["result_tablas"].items():
        cuerpo = {k: tabla[k] for k in claves}
        if diag:
            cuerpo["_diagnostico_peso"] = diag
        salida[rid] = json.dumps(cuerpo, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":"), allow_nan=False)
    return salida
