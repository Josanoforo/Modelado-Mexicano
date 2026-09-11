"""Medidor de S12 v1.2: composición alineado/no-alineado entre receptores."""
from __future__ import annotations

import numpy as np
import pyreadstat


def _alineado(oferente, voto, crosswalk, coaliciones):
    out = np.full(len(oferente), np.nan)
    for i, (o, v) in enumerate(zip(oferente, voto)):
        if not np.isfinite(o) or not np.isfinite(v):
            continue
        esperado = crosswalk.get(int(o))
        if esperado is None:
            continue
        aceptados = {esperado} | {c for c, partes in coaliciones.items() if esperado in partes}
        out[i] = 1.0 if int(v) in aceptados else 0.0
    return out


def _prop(y, w):
    return float(np.sum(y * w) / np.sum(w))


def _bootstrap(y, w, upm, estrato, replicas, semilla):
    rng = np.random.Generator(np.random.PCG64(semilla))
    indices = {}
    por_estrato = {}
    for i, (e, u) in enumerate(zip(estrato, upm)):
        clave = (e, u)
        indices.setdefault(clave, []).append(i)
        por_estrato.setdefault(e, [])
        if clave not in por_estrato[e]:
            por_estrato[e].append(clave)
    ps = np.empty(replicas)
    for r in range(replicas):
        muestra = []
        for claves in por_estrato.values():
            for j in rng.integers(0, len(claves), len(claves)):
                muestra.extend(indices[claves[j]])
        idx = np.asarray(muestra, dtype=int)
        ps[r] = _prop(y[idx], w[idx])
    return tuple(float(x) for x in np.percentile(ps, [2.5, 97.5]))


def medir(inputs, contrato):
    p = contrato["parametros"]
    df, _ = pyreadstat.read_sav(inputs[p["input_id"]]["ruta_absoluta"])
    cw = {int(k): int(v) for k, v in p["crosswalk_partido"].items()}
    coal = {int(k): {int(x) for x in xs} for k, xs in p["coaliciones"].items()}
    w_all = np.asarray(df[p["ponderador"]], dtype=float)
    upm_all = np.asarray(df[p["upm"]], dtype=float)
    est_all = np.asarray(df[p["estrato"]], dtype=float)
    voto = np.asarray(df[p["desenlace"]], dtype=float)
    out = {}
    for rama, receptor_var, partido_var in p["ramas"]:
        receptor = np.asarray(df[receptor_var], dtype=float) == 1
        y_all = _alineado(np.asarray(df[partido_var], dtype=float), voto, cw, coal)
        valido = receptor & np.isfinite(y_all) & np.isfinite(w_all) & (w_all > 0) & np.isfinite(upm_all) & np.isfinite(est_all)
        y, w, upm, est = y_all[valido], w_all[valido], upm_all[valido], est_all[valido]
        n_a, n_n = int(np.sum(y == 1)), int(np.sum(y == 0))
        w_a, w_n = float(np.sum(w[y == 1])), float(np.sum(w[y == 0]))
        pa = _prop(y, w)
        lo, hi = _bootstrap(y, w, upm, est, int(p["bootstrap_replicas"]), int(contrato["seed"]["valor"]))
        pre = f"RESULT-{rama}"
        out[f"{pre}-N-RECEPTORES"] = int(np.sum(receptor))
        out[f"{pre}-N-ANALITICO"] = int(np.sum(valido))
        out[f"{pre}-N-EXCLUIDOS"] = int(np.sum(receptor) - np.sum(valido))
        out[f"{pre}-N-ALINEADO"] = n_a
        out[f"{pre}-N-NO-ALINEADO"] = n_n
        out[f"{pre}-W-ALINEADO"] = w_a
        out[f"{pre}-W-NO-ALINEADO"] = w_n
        out[f"{pre}-P-ALINEADO"] = pa
        out[f"{pre}-P-NO-ALINEADO"] = 1.0 - pa
        out[f"{pre}-IC-ALINEADO-LO"] = lo
        out[f"{pre}-IC-ALINEADO-HI"] = hi
        out[f"{pre}-IC-NO-ALINEADO-LO"] = 1.0 - hi
        out[f"{pre}-IC-NO-ALINEADO-HI"] = 1.0 - lo
        out[f"{pre}-DELTA-COMP"] = 2.0 * pa - 1.0
        out[f"{pre}-IC-DELTA-LO"] = 2.0 * lo - 1.0
        out[f"{pre}-IC-DELTA-HI"] = 2.0 * hi - 1.0
        out[f"{pre}-N-UPM"] = int(len(set(zip(est.tolist(), upm.tolist()))))
        out[f"{pre}-N-ESTRATOS"] = int(len(set(est.tolist())))
        out[f"{pre}-LIMITACION"] = "LIMITADA-N-MENOR-10" if min(n_a, n_n) < 10 else "SOPORTE-N-MAYOR-O-IGUAL-10"
    return out
