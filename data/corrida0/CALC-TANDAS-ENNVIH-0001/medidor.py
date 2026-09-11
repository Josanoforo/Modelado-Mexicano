"""Medidor congelado de `CALC-TANDAS-ENNVIH-0001`.

Interfaz estable: medir(inputs, contrato) -> {"RESULT-...": escalar}.
No fue ejecutado antes del commit de congelamiento.
"""
from __future__ import annotations

import io
import json
import math
import zipfile

import numpy as np
import pandas as pd


P = "RESULT-TANDAS-ENNVIH-"

WAVES = {
    "2002": {
        "data_id": "ennvih1_2002_hogar_dta",
        "weight_id": "ennvih1_2002_ponderador",
        "cr": "ehh02dta_all/ehh02dta_b3b/iiib_cr.dta",
        "port": "ehh02dta_all/ehh02dta_b3b/iiib_portad.dta",
        "weight": "ehh02w_all/ehh02w_b3b.dta",
        "expected": {1: 2469, 3: 17333},
        "amounts": {
            "APORTADO": ("cr05a_1", "cr05a_2"),
            "RECIBIDO": ("cr05b_1", "cr05b_2"),
            "POR-RECIBIR": ("cr05c_1", "cr05c_2"),
        },
    },
    "2005_06": {
        "data_id": "ennvih2_2005_hogar_dta",
        "weight_id": "ennvih2_2005_ponderador_transversal",
        "cr": "ehh05dta_b3b/iiib_cr.dta",
        "port": "ehh05dta_b3b/iiib_portad.dta",
        "weight": "ehh05w_all/ehh05w_b3b.dta",
        "expected": {1: 1505, 3: 18952},
        "amounts": {
            "APORTADO": ("cr05a_1", "cr05a_2"),
            "RECIBIDO": ("cr05b_1", "cr05b_2"),
            "POR-RECIBIR": ("cr05c_1", "cr05c_2"),
        },
    },
    "2009_12": {
        "data_id": "ennvih3_2009_hogar_dta",
        "weight_id": "ennvih3_2009_ponderador_transversal",
        "cr": "ehh09dta_all/ehh09dta_b3b/iiib_cr.dta",
        "port": "ehh09dta_all/ehh09dta_b3b/iiib_portad.dta",
        "weight": "ehh09w_all/ehh09w_b3b.dta",
        "expected": {1: 2497, 3: 20960},
        "amounts": {"RECIBIDO-O-POR-RECIBIR": ("cr05_1", "cr05_2")},
    },
}


def _read_member(path, member):
    with zipfile.ZipFile(path) as zf:
        df = pd.read_stata(io.BytesIO(zf.read(member)),
                           convert_categoricals=False,
                           preserve_dtypes=False)
    if "folio" in df and "ls" in df:
        def key(value, width):
            if pd.isna(value):
                return ""
            if isinstance(value, (int, float, np.integer, np.floating)):
                if not float(value).is_integer():
                    raise ValueError(f"llave numerica no entera: {value!r}")
                return str(int(value)).zfill(width)
            raw = str(value).strip()
            return raw.zfill(width) if raw.isdigit() else raw
        df["folio"] = df["folio"].map(lambda value: key(value, 8))
        df["ls"] = df["ls"].map(lambda value: key(value, 2))
    if "fac_3b" in df:
        rows = []
        for (folio, ls), group in df.groupby(["folio", "ls"], sort=False):
            positive = sorted(set(_num(group["fac_3b"]).dropna().loc[lambda x: x > 0]))
            if len(positive) > 1:
                raise ValueError(f"ponderadores positivos ambiguos para {(folio, ls)}")
            rows.append({"folio": folio, "ls": ls,
                         "fac_3b": positive[0] if positive else 0.0})
        df = pd.DataFrame(rows, columns=["folio", "ls", "fac_3b"])
    return df


def _num(s):
    return pd.to_numeric(s, errors="coerce")


def _weighted_quantile(values, weights, q):
    order = np.argsort(values, kind="stable")
    v = np.asarray(values, dtype=float)[order]
    w = np.asarray(weights, dtype=float)[order]
    target = q * w.sum()
    return float(v[np.searchsorted(np.cumsum(w), target, side="left")])


def _summarize_value(df, value_col, mask):
    x = _num(df[value_col])
    w = _num(df["fac_3b"])
    bad = mask & (~np.isfinite(x) | (x < 0))
    ok = mask & np.isfinite(x) & (x >= 0) & np.isfinite(w) & (w > 0)
    if not ok.any():
        return {"N": 0, "MASA": 0.0, "MEDIA": None, "MEDIANA": None,
                "N-EXCLUIDO": int(bad.sum())}
    xv = x[ok].to_numpy(dtype=float)
    wv = w[ok].to_numpy(dtype=float)
    return {
        "N": int(ok.sum()),
        "MASA": float(math.fsum(wv)),
        "MEDIA": float(np.average(xv, weights=wv)),
        "MEDIANA": _weighted_quantile(xv, wv, 0.5),
        "N-EXCLUIDO": int(bad.sum()),
    }


def medir(inputs, contrato):
    out = {}
    for wave, cfg in WAVES.items():
        data_path = inputs[cfg["data_id"]]["ruta_absoluta"]
        weight_path = inputs[cfg["weight_id"]]["ruta_absoluta"]
        cr = _read_member(data_path, cfg["cr"])
        port = _read_member(data_path, cfg["port"])
        weights = _read_member(weight_path, cfg["weight"])

        keys = ["folio", "ls"]
        if port.duplicated(keys).any() or weights.duplicated(keys).any() or cr.duplicated(keys).any():
            raise ValueError(f"{wave}: identidad folio+ls no es unica")
        df = cr.merge(port[keys + ["edad"]], on=keys, how="left", validate="one_to_one")
        df = df.merge(weights[keys + ["fac_3b"]], on=keys, how="left", validate="one_to_one")
        cr04 = _num(df["cr04"])
        observed = {1: int((cr04 == 1).sum()), 3: int((cr04 == 3).sum())}
        if observed != cfg["expected"]:
            raise ValueError(f"{wave}: control codebook falla: {observed} != {cfg['expected']}")
        w = _num(df["fac_3b"])
        valid_response = cr04.isin([1, 3])
        valid_weight = np.isfinite(w) & (w > 0)
        universe = valid_response & valid_weight
        yes = universe & (cr04 == 1)
        mass = float(math.fsum(w[universe].to_numpy(dtype=float)))
        yes_mass = float(math.fsum(w[yes].to_numpy(dtype=float)))

        base = P + wave + "-"
        out[base + "N-FILAS"] = int(len(df))
        out[base + "N-VALIDO"] = int(universe.sum())
        out[base + "N-SI"] = int(yes.sum())
        out[base + "N-RESPUESTA-FALTANTE"] = int((~valid_response).sum())
        out[base + "N-PONDERADOR-INVALIDO"] = int((valid_response & ~valid_weight).sum())
        out[base + "MASA"] = mass
        out[base + "P-PARTICIPA"] = yes_mass / mass
        out[base + "P-PARTICIPA-NO-PONDERADA"] = float(yes.sum() / universe.sum())
        out[base + "CONTROL-CODEBOOK"] = "REPRODUCE"
        out[base + "METODO-IC"] = "NO-ESTIMABLE-SIN-UPM-ESTRATO-REPLICAS"

        age = _num(df["edad"])
        age_valid = age.between(15, 120, inclusive="both")
        out[base + "N-EDAD-FUERA-O-FALTANTE"] = int((~age_valid).sum())
        groups = {
            "EDAD-15-29": age.between(15, 29, inclusive="both"),
            "EDAD-30-49": age.between(30, 49, inclusive="both"),
            "EDAD-50-MAS": age.between(50, 120, inclusive="both"),
        }
        cuts = {}
        for label, group in groups.items():
            den = universe & group
            num = den & (cr04 == 1)
            den_mass = float(math.fsum(w[den].to_numpy(dtype=float)))
            cuts[label] = {
                "n": int(den.sum()),
                "masa": den_mass,
                "p_participa": (
                    float(math.fsum(w[num].to_numpy(dtype=float))) / den_mass
                    if den_mass > 0 else None
                ),
            }
        out[base + "CORTES-EDAD-JSON"] = json.dumps(
            cuts, ensure_ascii=True, sort_keys=True, separators=(",", ":"))

        participant = cr04 == 1
        secondary = {"montos_pesos_nominales": {}}
        for label, (indicator, value) in cfg["amounts"].items():
            eligible = participant & (_num(df[indicator]) == 1)
            secondary["montos_pesos_nominales"][label] = _summarize_value(
                df, value, eligible)

        if wave == "2009_12":
            unit = _num(df["cr05a_1"])
            duration = pd.Series(np.nan, index=df.index, dtype=float)
            duration.loc[unit == 1] = _num(df.loc[unit == 1, "cr05a_21"])
            duration.loc[unit == 2] = _num(df.loc[unit == 2, "cr05a_22"]) * 7.0
            duration.loc[unit == 3] = _num(df.loc[unit == 3, "cr05a_23"]) * (365.25 / 12.0)
            df = df.assign(_duration_days=duration)
            eligible = participant & unit.isin([1, 2, 3])
            secondary["duracion_dias_homologada"] = _summarize_value(
                df, "_duration_days", eligible)
            secondary["duracion_unidad_original_n"] = {}
            for code, label in [(1, "DIAS"), (2, "SEMANAS"), (3, "MESES")]:
                secondary["duracion_unidad_original_n"][label] = int(
                    (participant & (unit == code)).sum())
        out[base + "SECUNDARIOS-JSON"] = json.dumps(
            secondary, ensure_ascii=True, sort_keys=True, separators=(",", ":"))

    return out
