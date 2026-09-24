"""Pisos nacionales LAPOP México 2019, diseño estratificado por UPM."""
from __future__ import annotations

import json
import numpy as np
import pandas as pd
import pyreadstat

PID = "mexico_lapop_americasbarometer_2019_v1_0_w"


def estimate(df, variable, valid, selected, seed, reps):
    x = pd.to_numeric(df[variable], errors="coerce")
    w = pd.to_numeric(df["wt"], errors="coerce")
    mask = x.isin(valid) & w.notna() & (w > 0) & df["estratopri"].notna() & df["upm"].notna()
    d = df.loc[mask]
    if len(d) < 30:
        return {"estado": "NO-ESTIMABLE", "n": int(len(d)), "p": None,
                "ic95": None}
    weights = w[mask].to_numpy(float)
    yes = x[mask].isin(selected).to_numpy(bool)
    numerator = float(weights[yes].sum())
    denominator = float(weights.sum())
    p = numerator / denominator
    keys = list(zip(d["estratopri"].astype(str), d["upm"].astype(str)))
    groups = {}
    for i, key in enumerate(keys):
        groups.setdefault(key, [0.0, 0.0])
        groups[key][0] += weights[i] * yes[i]
        groups[key][1] += weights[i]
    strata = {}
    for (stratum, upm), pair in groups.items():
        strata.setdefault(stratum, []).append(pair)
    rng = np.random.Generator(np.random.PCG64(seed))
    draws = []
    for _ in range(reps):
        num = den = 0.0
        for pairs in strata.values():
            matrix = np.asarray(pairs)
            indexes = rng.integers(0, len(matrix), len(matrix)) if len(matrix) > 1 else [0]
            total = matrix[indexes].sum(axis=0)
            num += float(total[0])
            den += float(total[1])
        draws.append(num / den if den else np.nan)
    finite = np.asarray(draws)[np.isfinite(draws)]
    ci = [float(np.quantile(finite, 0.025)), float(np.quantile(finite, 0.975))] if len(finite) else None
    return {"estado": "ESTIMADA", "n": int(len(d)), "n_si": int(yes.sum()),
            "p": p, "ic95": ci, "n_estratos": len(strata), "n_upm": len(groups),
            "replicas_validas": int(len(finite)), "masa_ponderada": denominator}


def medir(inputs, contrato):
    df, _ = pyreadstat.read_dta(inputs[PID]["ruta_absoluta"])
    required = {"clien1na", "b18", "wt", "estratopri", "upm"}
    if not required.issubset(df.columns):
        raise ValueError(f"faltan variables: {sorted(required - set(df.columns))}")
    seed = int(contrato["seed"]["valor"])
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    table = {
        "oferta_beneficio_voto": estimate(df, "clien1na", (1, 2), (1,), seed, reps),
        "confianza_policia_alta": estimate(df, "b18", tuple(range(1, 8)), (6, 7), seed + 1, reps),
    }
    return {"RESULT-LAPOP-PISOS-2019-FILAS": int(len(df)),
            "RESULT-LAPOP-PISOS-2019-TABLA": json.dumps(
                table, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)}
