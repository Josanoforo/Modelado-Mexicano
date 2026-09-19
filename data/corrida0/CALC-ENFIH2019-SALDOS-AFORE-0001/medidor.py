"""Saldo Afore de hogares en ENFIH 2019.

Interfaz de corrida0: ``medir(inputs, contrato) -> {RESULT-...: escalar}``.
La especificacion y este medidor se congelan antes de ejecutar la medicion.
"""
from __future__ import annotations

import io
import json
import math
import zipfile

import numpy as np
import pandas as pd


PREFIX = "RESULT-ENFIH2019-SALDOS-AFORE-"
KEY = ["FOLIO", "VIV_SEL", "HOGAR"]
CONC_COLS = KEY + ["C_AFORE", "V_AFORE", "FAC_HOG", "EDIS", "UPM_DIS", "H_PPAL"]
MOD_COLS = KEY + ["N_REN", "P9_10", "P9_11"]
SPECIAL = {"999999888": "NO-RESPONDE", "999999999": "NO-SABE"}


def _member(zf: zipfile.ZipFile, wanted: str) -> str:
    candidates = [n for n in zf.namelist() if n.rsplit("/", 1)[-1].upper() == wanted.upper()]
    if len(candidates) != 1:
        raise ValueError(f"miembro {wanted}: esperados 1, encontrados {len(candidates)}")
    return candidates[0]


def _read(zf: zipfile.ZipFile, member: str, columns: list[str]) -> pd.DataFrame:
    raw = zf.read(_member(zf, member)).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    frame = pd.read_csv(io.BytesIO(raw), encoding="latin-1", dtype=str,
                        keep_default_na=False, low_memory=False)
    frame.columns = [str(c).lstrip("\ufeff").lstrip("ï»¿").strip() for c in frame.columns]
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise ValueError(f"{member}: columnas ausentes {missing}")
    return frame[columns].apply(lambda s: s.astype(str).str.strip())


def weighted_quantile(values, weights, q: float) -> float:
    """Inversa izquierda de la CDF: primer valor con acumulado >= q*masa."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not keep.any():
        return float("nan")
    order = np.argsort(values[keep], kind="stable")
    x, w = values[keep][order], weights[keep][order]
    target = q * math.fsum(w.tolist())
    return float(x[np.searchsorted(np.cumsum(w), target, side="left")])


def top_share_tied(values, weights, fraction: float = 0.10) -> float:
    """Fraccion del saldo del ``fraction`` superior por masa de hogares.

    Si el umbral corta un empate, todos los hogares con ese mismo saldo reciben
    la misma fraccion de inclusion. Asi el resultado no depende del orden de fila.
    """
    x = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    keep = np.isfinite(x) & np.isfinite(w) & (w > 0) & (x > 0)
    x, w = x[keep], w[keep]
    if not len(x):
        return float("nan")
    total_balance = math.fsum((x * w).tolist())
    if total_balance <= 0:
        return float("nan")
    target = fraction * math.fsum(w.tolist())
    numerator = 0.0
    remaining = target
    for value in np.unique(x)[::-1]:
        group_weight = math.fsum(w[x == value].tolist())
        take = min(group_weight, max(remaining, 0.0))
        numerator += float(value) * take
        remaining -= take
        if remaining <= 1e-12:
            break
    return float(numerator / total_balance)


def classify_households(conc: pd.DataFrame, module: pd.DataFrame) -> pd.DataFrame:
    """Une el agregado oficial con respuestas personales y clasifica cobertura."""
    if conc.duplicated(KEY).any():
        raise ValueError("llave FOLIO+VIV_SEL+HOGAR no unica en TCONCENTRADORA")
    if module.duplicated(KEY + ["N_REN"]).any():
        raise ValueError("llave de persona no unica en TMODULO")

    holders = module.loc[module["P9_10"] == "1", KEY + ["P9_11"]].copy()
    raw = holders["P9_11"]
    amount = pd.to_numeric(raw, errors="coerce")
    known = amount.between(0, 108_264_000, inclusive="both")
    special = raw.isin(SPECIAL)
    invalid = ~(known | special)
    if invalid.any():
        values = sorted(raw[invalid].unique().tolist())
        raise ValueError(f"P9_11 de tenedor fuera de mapa: {values}")
    holders["known"] = known
    holders["special"] = special
    holders["no_response"] = raw.eq("999999888")
    holders["dont_know"] = raw.eq("999999999")
    holders["known_amount"] = amount.where(known, 0.0)

    agg = holders.groupby(KEY, sort=False).agg(
        n_holders=("P9_11", "size"),
        n_known=("known", "sum"),
        n_special=("special", "sum"),
        n_no_response=("no_response", "sum"),
        n_dont_know=("dont_know", "sum"),
        sum_known=("known_amount", "sum"),
    ).reset_index()
    out = conc.merge(agg, on=KEY, how="left", validate="one_to_one")
    for c in ["n_holders", "n_known", "n_special", "n_no_response", "n_dont_know", "sum_known"]:
        out[c] = out[c].fillna(0)
    out["c"] = pd.to_numeric(out["C_AFORE"], errors="coerce")
    out["v"] = pd.to_numeric(out["V_AFORE"], errors="coerce")
    if out["c"].isna().any() or not set(out["c"].unique()).issubset({0, 1}):
        raise ValueError("C_AFORE fuera de {0,1}")
    if out["v"].isna().any() or (out["v"] < 0).any():
        raise ValueError("V_AFORE no numerico o negativo")
    if not np.array_equal(out["c"].to_numpy(dtype=int), (out["n_holders"] > 0).to_numpy(dtype=int)):
        raise ValueError("C_AFORE no coincide con tenencia personal agregada")
    if not np.allclose(out["v"], out["sum_known"], rtol=0, atol=0):
        raise ValueError("V_AFORE no coincide con suma de montos personales conocidos")

    holder = out["c"].eq(1)
    complete = holder & out["n_special"].eq(0)
    out["state"] = "NO-TENEDOR"
    out.loc[complete & out["v"].eq(0), "state"] = "CONOCIDO-CERO"
    out.loc[complete & out["v"].gt(0), "state"] = "CONOCIDO-POSITIVO"
    out.loc[holder & out["n_special"].gt(0) & out["n_known"].eq(0), "state"] = "DESCONOCIDO-TOTAL"
    out.loc[holder & out["n_special"].gt(0) & out["n_known"].gt(0), "state"] = "PARCIAL"
    out["complete"] = complete
    return out


def _weighted_mean(x, w) -> float:
    x, w = np.asarray(x, float), np.asarray(w, float)
    keep = np.isfinite(x) & np.isfinite(w) & (w > 0)
    den = math.fsum(w[keep].tolist())
    return float(math.fsum((x[keep] * w[keep]).tolist()) / den) if den > 0 else float("nan")


def _domain_stats(df: pd.DataFrame, weights: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    x = df["v"].to_numpy(float)[mask]
    w = weights[mask]
    return {
        "mean": _weighted_mean(x, w),
        "p25": weighted_quantile(x, w, 0.25),
        "p50": weighted_quantile(x, w, 0.50),
        "p75": weighted_quantile(x, w, 0.75),
        "p90": weighted_quantile(x, w, 0.90),
    }


def calculate_points(df: pd.DataFrame, weights: np.ndarray) -> dict[str, float]:
    holder = df["c"].eq(1).to_numpy()
    complete = df["complete"].to_numpy(bool)
    valid = holder & complete
    positive = valid & df["v"].gt(0).to_numpy()
    principal = _domain_stats(df, weights, valid)
    pos = _domain_stats(df, weights, positive)
    holder_mass = math.fsum(weights[holder].tolist())
    coverage = math.fsum(weights[valid].tolist()) / holder_mass if holder_mass else float("nan")
    covered_universe = (~holder) | valid
    universe_mean = _weighted_mean(df["v"].to_numpy(float)[covered_universe], weights[covered_universe])
    concentration = top_share_tied(df["v"].to_numpy(float)[positive], weights[positive], 0.10)

    hp = df["H_PPAL"].eq("1").to_numpy()
    hp_valid = valid & hp
    hp_holder = holder & hp
    hp_stats = _domain_stats(df, weights, hp_valid)
    hp_mass = math.fsum(weights[hp_holder].tolist())
    hp_coverage = math.fsum(weights[hp_valid].tolist()) / hp_mass if hp_mass else float("nan")
    return {
        **{f"principal_{k}": v for k, v in principal.items()},
        **{f"positive_{k}": v for k, v in pos.items()},
        "coverage": coverage,
        "universe_mean": universe_mean,
        "concentration": concentration,
        "hp_coverage": hp_coverage,
        "hp_mean": hp_stats["mean"],
        "hp_p50": hp_stats["p50"],
        "delta_coverage": hp_coverage - coverage,
        "delta_mean": hp_stats["mean"] - principal["mean"],
        "delta_p50": hp_stats["p50"] - principal["p50"],
    }


def _replicate_multipliers(df: pd.DataFrame, replicas: int, seed: int):
    cluster = (df["EDIS"] + "\x1f" + df["UPM_DIS"]).to_numpy()
    unique, inverse = np.unique(cluster, return_inverse=True)
    strata = np.array([x.split("\x1f", 1)[0] for x in unique])
    rng = np.random.Generator(np.random.PCG64(seed))
    positions = [np.flatnonzero(strata == s) for s in np.unique(strata)]
    for _ in range(replicas):
        counts = np.zeros(len(unique), dtype=float)
        for pos in positions:
            selected = rng.choice(pos, size=len(pos), replace=True)
            counts += np.bincount(selected, minlength=len(unique))
        yield counts[inverse]


def bootstrap(df: pd.DataFrame, replicas: int, seed: int) -> dict[str, np.ndarray]:
    names = list(calculate_points(df, df["w"].to_numpy(float)))
    samples = {name: np.full(replicas, np.nan) for name in names}
    base = df["w"].to_numpy(float)
    for r, multiplier in enumerate(_replicate_multipliers(df, replicas, seed)):
        result = calculate_points(df, base * multiplier)
        for name, value in result.items():
            samples[name][r] = value
    return samples


def _ci(values: np.ndarray) -> tuple[float | None, float | None, int]:
    valid = values[np.isfinite(values)]
    if not len(valid):
        return None, None, 0
    lo, hi = np.percentile(valid, [2.5, 97.5])
    return float(lo), float(hi), int(len(valid))


def _mass(weights: np.ndarray, mask: np.ndarray) -> float:
    return float(math.fsum(weights[mask].tolist()))


def medir(inputs, contrato):
    params = contrato["parametros"]
    replicas = int(params["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    path = inputs["enfih2019_bd_csv_zip"]["ruta_absoluta"]
    with zipfile.ZipFile(path) as zf:
        conc = _read(zf, params["tabla_concentradora"], CONC_COLS)
        module = _read(zf, params["tabla_modulo"], MOD_COLS)
    df = classify_households(conc, module).sort_values(KEY, kind="stable").reset_index(drop=True)
    df["w"] = pd.to_numeric(df["FAC_HOG"], errors="coerce")
    valid_weight = np.isfinite(df["w"]) & df["w"].gt(0)
    excluded_weight = int((~valid_weight).sum())
    df = df.loc[valid_weight].copy().reset_index(drop=True)
    if df.empty:
        raise ValueError("universo vacio tras validar FAC_HOG")
    if (df["EDIS"].eq("") | df["UPM_DIS"].eq("")).any():
        raise ValueError("diseno incompleto: IC no defendible")

    w = df["w"].to_numpy(float)
    holder = df["c"].eq(1).to_numpy()
    complete = df["complete"].to_numpy(bool)
    valid = holder & complete
    positive = valid & df["v"].gt(0).to_numpy()
    points = calculate_points(df, w)
    reps = bootstrap(df, replicas, seed)

    out: dict[str, object] = {}
    put = lambda name, value: out.__setitem__(PREFIX + name, value)
    put("N-UNIVERSO", int(len(df)))
    put("N-PESO-INVALIDO", excluded_weight)
    put("MASA-UNIVERSO", _mass(w, np.ones(len(df), dtype=bool)))
    put("P-TENEDOR", _mass(w, holder) / _mass(w, np.ones(len(df), dtype=bool)))
    put("P-NO-TENEDOR", _mass(w, ~holder) / _mass(w, np.ones(len(df), dtype=bool)))
    put("P-TENENCIA-DESCONOCIDA", 0.0)
    put("DELTA-TENENCIA-VS-CALC-ENFIH-0001", out[PREFIX + "P-TENEDOR"] - float(params["tenencia_control"]))

    states = {}
    for state in ["NO-TENEDOR", "CONOCIDO-CERO", "CONOCIDO-POSITIVO", "DESCONOCIDO-TOTAL", "PARCIAL"]:
        mask = df["state"].eq(state).to_numpy()
        states[state] = {"n": int(mask.sum()), "masa": _mass(w, mask),
                         "proporcion_universo": _mass(w, mask) / _mass(w, np.ones(len(df), dtype=bool))}
    put("ESTADOS-JSON", json.dumps(states, sort_keys=True, separators=(",", ":")))
    put("COHERENCIA-JSON", json.dumps({
        "no_tenencia_con_saldo_positivo": int(((df["c"] == 0) & (df["v"] > 0)).sum()),
        "tenencia_con_agregado_cero": int(((df["c"] == 1) & (df["v"] == 0)).sum()),
        "tenencia_con_especial_no_responde": int(((df["c"] == 1) & (df["n_no_response"] > 0)).sum()),
        "tenencia_con_especial_no_sabe": int(((df["c"] == 1) & (df["n_dont_know"] > 0)).sum()),
    }, sort_keys=True, separators=(",", ":")))

    put("COBERTURA-MONTO", points["coverage"])
    put("N-MONTO-VALIDO", int(valid.sum()))
    put("MASA-MONTO-VALIDO", _mass(w, valid))
    put("N-MONTO-POSITIVO", int(positive.sum()))
    put("MASA-MONTO-POSITIVO", _mass(w, positive))
    for label, key in [("MEDIA", "principal_mean"), ("P25", "principal_p25"),
                       ("MEDIANA", "principal_p50"), ("P75", "principal_p75"),
                       ("P90", "principal_p90"), ("POSITIVO-MEDIA", "positive_mean"),
                       ("POSITIVO-MEDIANA", "positive_p50"),
                       ("MEDIA-UNIVERSO-CUBIERTO", "universe_mean"),
                       ("TOP10-FRACCION-SALDO", "concentration"),
                       ("HPPAL-COBERTURA", "hp_coverage"), ("HPPAL-MEDIA", "hp_mean"),
                       ("HPPAL-MEDIANA", "hp_p50"),
                       ("DELTA-HPPAL-COBERTURA", "delta_coverage"),
                       ("DELTA-HPPAL-MEDIA", "delta_mean"),
                       ("DELTA-HPPAL-MEDIANA", "delta_p50")]:
        put(label, points[key])
        lo, hi, _ = _ci(reps[key])
        put(label + "-IC95-LO", lo)
        put(label + "-IC95-HI", hi)

    cov_lo, cov_hi, _ = _ci(reps["coverage"])
    put("COBERTURA-MONTO-IC95-LO", cov_lo)
    put("COBERTURA-MONTO-IC95-HI", cov_hi)
    valid_reps = {name: int(np.isfinite(values).sum()) for name, values in reps.items()}
    put("REPLICAS-VALIDAS-JSON", json.dumps(valid_reps, sort_keys=True, separators=(",", ":")))
    put("METODO-IC", "BOOTSTRAP-UPM-EN-EDIS-PERCENTIL;EMPATES-UMBRAL-FRACCION-UNIFORME")
    put("CONTROL-CUANTILES-MONOTONOS", "SI" if points["principal_p25"] <= points["principal_p50"] <= points["principal_p75"] <= points["principal_p90"] else "NO")
    put("CONTROL-CONCENTRACION-01", "SI" if 0 <= points["concentration"] <= 1 else "NO")
    return out
