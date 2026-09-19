"""Concentracion de saldos Afore completos, incluyendo ceros validos.

Interfaz de corrida0: ``medir(inputs, contrato) -> {RESULT-...: escalar}``.
Esta unidad es sucesora de CALC-ENFIH2019-SALDOS-AFORE-0001 y no importa ni
modifica su funcion de concentracion, cuyo dominio publicado fue positivo.
"""
from __future__ import annotations

import io
import json
import math
import zipfile

import numpy as np
import pandas as pd


PREFIX = "RESULT-ENFIH2019-SALDOS-AFORE-CONCENTRACION-"
KEY = ["FOLIO", "VIV_SEL", "HOGAR"]
CONC_COLS = KEY + ["C_AFORE", "V_AFORE", "FAC_HOG", "EDIS", "UPM_DIS"]
MOD_COLS = KEY + ["N_REN", "P9_10", "P9_11"]
SPECIAL = {"999999888", "999999999"}


def _member(zf: zipfile.ZipFile, wanted: str) -> str:
    found = [n for n in zf.namelist() if n.rsplit("/", 1)[-1].upper() == wanted.upper()]
    if len(found) != 1:
        raise ValueError(f"miembro {wanted}: esperados 1, encontrados {len(found)}")
    return found[0]


def _read(zf: zipfile.ZipFile, member: str, columns: list[str]) -> pd.DataFrame:
    raw = zf.read(_member(zf, member)).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    frame = pd.read_csv(io.BytesIO(raw), encoding="latin-1", dtype=str,
                        keep_default_na=False, low_memory=False)
    frame.columns = [str(c).lstrip("\ufeff").lstrip("ï»¿").strip() for c in frame.columns]
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise ValueError(f"{member}: columnas ausentes {missing}")
    return frame[columns].apply(lambda s: s.astype(str).str.strip())


def classify_complete(conc: pd.DataFrame, module: pd.DataFrame) -> pd.DataFrame:
    """Clasifica el total completo sin convertir especiales en dinero."""
    if conc.duplicated(KEY).any():
        raise ValueError("llave de hogar no unica")
    if module.duplicated(KEY + ["N_REN"]).any():
        raise ValueError("llave de persona no unica")
    holders = module.loc[module["P9_10"].eq("1"), KEY + ["P9_11"]].copy()
    amount = pd.to_numeric(holders["P9_11"], errors="coerce")
    known = amount.between(0, 108_264_000, inclusive="both")
    special = holders["P9_11"].isin(SPECIAL)
    if (~(known | special)).any():
        bad = sorted(holders.loc[~(known | special), "P9_11"].unique().tolist())
        raise ValueError(f"P9_11 fuera de mapa: {bad}")
    holders["known"] = known
    holders["special"] = special
    holders["known_amount"] = amount.where(known, 0.0)
    agg = holders.groupby(KEY, sort=False).agg(
        n_holders=("P9_11", "size"),
        n_special=("special", "sum"),
        sum_known=("known_amount", "sum"),
    ).reset_index()
    out = conc.merge(agg, on=KEY, how="left", validate="one_to_one")
    for name in ["n_holders", "n_special", "sum_known"]:
        out[name] = out[name].fillna(0)
    out["c"] = pd.to_numeric(out["C_AFORE"], errors="coerce")
    out["v"] = pd.to_numeric(out["V_AFORE"], errors="coerce")
    if out["c"].isna().any() or not set(out["c"].unique()).issubset({0, 1}):
        raise ValueError("C_AFORE fuera de {0,1}")
    if out["v"].isna().any() or out["v"].lt(0).any():
        raise ValueError("V_AFORE no numerico o negativo")
    if not np.array_equal(out["c"].to_numpy(int), out["n_holders"].gt(0).to_numpy(int)):
        raise ValueError("C_AFORE no coincide con P9_10 agregado")
    if not np.allclose(out["v"], out["sum_known"], rtol=0, atol=0):
        raise ValueError("V_AFORE no coincide con suma de P9_11 conocidos")
    out["complete"] = out["c"].eq(1) & out["n_special"].eq(0)
    return out


def top_share_by_mass(values, weights, domain, fraction: float = 0.10) -> float:
    """Saldo del ``fraction`` superior definido por masa del dominio.

    ``domain`` decide la poblacion antes de ordenar. Los ceros permanecen si
    pertenecen al dominio; solo pesos de aporte cero salen del calculo. Un
    empate en el umbral recibe la misma fraccion de inclusion por hogar.
    """
    x = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    d = np.asarray(domain, dtype=bool)
    keep = d & np.isfinite(x) & np.isfinite(w) & (w > 0) & (x >= 0)
    x, w = x[keep], w[keep]
    population_mass = math.fsum(w.tolist())
    money = math.fsum((x * w).tolist())
    if population_mass <= 0 or money <= 0:
        return float("nan")
    remaining = fraction * population_mass
    numerator = 0.0
    for value in np.unique(x)[::-1]:
        group_mass = math.fsum(w[x == value].tolist())
        take = min(group_mass, max(remaining, 0.0))
        numerator += float(value) * take
        remaining -= take
        if remaining <= 1e-12:
            break
    return float(numerator / money)


def calculate_points(frame: pd.DataFrame, weights: np.ndarray,
                     fraction: float = 0.10) -> dict[str, float]:
    holder = frame["c"].eq(1).to_numpy()
    valid_all = frame["complete"].to_numpy(bool)
    valid_positive = valid_all & frame["v"].gt(0).to_numpy()
    values = frame["v"].to_numpy(float)
    holder_mass = math.fsum(weights[holder].tolist())
    valid_mass = math.fsum(weights[valid_all].tolist())
    all_share = top_share_by_mass(values, weights, valid_all, fraction)
    positive_share = top_share_by_mass(values, weights, valid_positive, fraction)
    return {
        "coverage": valid_mass / holder_mass if holder_mass > 0 else float("nan"),
        "all_share": all_share,
        "positive_share": positive_share,
        "delta": all_share - positive_share,
    }


def _replicate_multipliers(frame: pd.DataFrame, replicas: int, seed: int):
    cluster = (frame["EDIS"] + "\x1f" + frame["UPM_DIS"]).to_numpy()
    unique, inverse = np.unique(cluster, return_inverse=True)
    strata = np.array([value.split("\x1f", 1)[0] for value in unique])
    rng = np.random.Generator(np.random.PCG64(seed))
    positions = [np.flatnonzero(strata == s) for s in np.unique(strata)]
    for _ in range(replicas):
        counts = np.zeros(len(unique), dtype=float)
        for pos in positions:
            selected = rng.choice(pos, size=len(pos), replace=True)
            counts += np.bincount(selected, minlength=len(unique))
        yield counts[inverse]


def bootstrap(frame: pd.DataFrame, replicas: int, seed: int,
              fraction: float = 0.10) -> dict[str, np.ndarray]:
    samples = {name: np.full(replicas, np.nan) for name in
               ["all_share", "positive_share", "delta"]}
    base = frame["w"].to_numpy(float)
    for index, multiplier in enumerate(_replicate_multipliers(frame, replicas, seed)):
        points = calculate_points(frame, base * multiplier, fraction)
        for name in samples:
            samples[name][index] = points[name]
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
    fraction = float(params["fraccion_superior"])
    seed = int(contrato["seed"]["valor"])
    with zipfile.ZipFile(inputs["enfih2019_bd_csv_zip"]["ruta_absoluta"]) as zf:
        conc = _read(zf, params["tabla_concentradora"], CONC_COLS)
        module = _read(zf, params["tabla_modulo"], MOD_COLS)
    frame = classify_complete(conc, module).sort_values(KEY, kind="stable").reset_index(drop=True)
    frame["w"] = pd.to_numeric(frame["FAC_HOG"], errors="coerce")
    frame = frame.loc[np.isfinite(frame["w"]) & frame["w"].gt(0)].copy().reset_index(drop=True)
    if frame.empty or frame["EDIS"].eq("").any() or frame["UPM_DIS"].eq("").any():
        raise ValueError("marco vacio o diseno incompleto")
    weights = frame["w"].to_numpy(float)
    valid_all = frame["complete"].to_numpy(bool)
    valid_positive = valid_all & frame["v"].gt(0).to_numpy()
    money = math.fsum((frame.loc[valid_all, "v"].to_numpy(float) * weights[valid_all]).tolist())
    if money <= 0:
        raise ValueError("saldo ponderado agregado no positivo: concentracion no estimable")
    points = calculate_points(frame, weights, fraction)
    samples = bootstrap(frame, replicas, seed, fraction)

    out = {}
    put = lambda name, value: out.__setitem__(PREFIX + name, value)
    put("N-VALIDO-TODOS", int(valid_all.sum()))
    put("MASA-VALIDO-TODOS", _mass(weights, valid_all))
    put("N-VALIDO-POSITIVOS", int(valid_positive.sum()))
    put("MASA-VALIDO-POSITIVOS", _mass(weights, valid_positive))
    put("COBERTURA-VALIDO-ENTRE-TENEDORES", points["coverage"])
    for label, name in [("TODOS-TOP10-FRACCION-SALDO", "all_share"),
                        ("POSITIVOS-TOP10-FRACCION-SALDO", "positive_share"),
                        ("DELTA-TODOS-MENOS-POSITIVOS", "delta")]:
        put(label, points[name])
        lo, hi, _ = _ci(samples[name])
        put(label + "-IC95-LO", lo)
        put(label + "-IC95-HI", hi)
    put("REPLICAS-VALIDAS-JSON", json.dumps(
        {name: int(np.isfinite(values).sum()) for name, values in samples.items()},
        sort_keys=True, separators=(",", ":")))
    put("METODO-IC", "BOOTSTRAP-UPM-EN-EDIS-PERCENTIL;REPLICAS-COMPARTIDAS;EMPATES-FRACCION-UNIFORME")
    put("CONTROL-DENOMINADOR-MONETARIO-POSITIVO", "SI")
    put("CONTROL-DOMINIOS", "SI" if valid_positive.sum() <= valid_all.sum() else "NO")
    return out
