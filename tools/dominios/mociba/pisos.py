"""Pisos MOCIBA 2015-2017 de ASTRA5 U4; véase la spec humana.

El primer resultado real que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from tools.dominios.endutih.pisos import _load, _replicate_weights

FILES = {"2015": "tciberacoso.dbf", "2016": "MOD_2016_CIBERACOSO.DBF",
         "2017": "mod_2017_ciberacoso.dbf"}
FIELDS_BASE = ("EDAD", "SEXO", "NIVEL", "FAC_MOCIBA")


def _fields(year: str) -> tuple[str, ...]:
    if year == "2015":
        return FIELDS_BASE + ("UPM",) + tuple(f"P3_{i}" for i in range(1, 11)) + tuple(
            f"P7_{i}_{j}" for i in range(1, 11) for j in (1, 5))
    if year == "2016":
        return FIELDS_BASE + ("UPM_DIS", "EST_DIS", "ENT") + tuple(
            f"P1_{i}" for i in range(1, 11)) + tuple(
            f"P7_{i}_{j}" for i in range(1, 11) for j in ("1", "6A"))
    return FIELDS_BASE + ("UPM_DIS", "EST_DIS", "ENT") + tuple(
        f"P4_{i:02d}" for i in range(1, 11)) + ("P10_1", "P10_5")


def _domains(row: dict[str, str], year: str) -> list[str]:
    out = ["TOTAL"]
    if row["SEXO"] in ("1", "2"):
        out.append("SEXO_" + row["SEXO"])
    age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
    for lo, hi, name in ((12, 17, "EDAD_12_17"), (18, 29, "EDAD_18_29"),
                         (30, 59, "EDAD_30_59"), (60, 97, "EDAD_60_MAS")):
        if lo <= age <= hi:
            out.append(name)
    school = row["NIVEL"].zfill(2)
    if school in ("00", "01", "02"):
        out.append("ESC_0_2")
    elif school in ("03", "04", "05"):
        out.append("ESC_3_5")
    elif school in ("06", "07", "08", "09", "10", "11"):
        out.append("ESC_6_11")
    if year != "2015" and row["ENT"].isdigit() and 1 <= int(row["ENT"]) <= 32:
        out.append("ENT_" + row["ENT"].zfill(2))
    return out


def _victim(row: dict[str, str], year: str) -> str:
    if year == "2015":
        fields = [f"P3_{i}" for i in range(1, 11)]
    elif year == "2016":
        fields = [f"P1_{i}" for i in range(1, 11)]
    else:
        fields = [f"P4_{i:02d}" for i in range(1, 11)]
    values = [row[x] for x in fields]
    if "1" in values:
        return "SI"
    if all(x == "2" for x in values):
        return "NO"
    if all(x in ("2", "9") for x in values):
        return "NS"
    return "NR"


def _response(row: dict[str, str], year: str, response: str) -> str:
    victim = _victim(row, year)
    if victim == "NO" or victim == "NS":
        return "SALTO"
    if victim != "SI":
        return "NR"
    if year == "2017":
        value = row["P10_1" if response == "bloqueo" else "P10_5"]
        return {"1": "SI", "2": "NO"}.get(value, "NR")
    if year == "2015":
        stem = "P3_"
        suffix = "1" if response == "bloqueo" else "5"
    else:
        stem = "P1_"
        suffix = "1" if response == "bloqueo" else "6A"
    yes_incidents = [i for i in range(1, 11) if row[stem + str(i)] == "1"]
    vals = [row[f"P7_{i}_{suffix}"] for i in yes_incidents]
    if "1" in vals:
        return "SI"
    if vals and all(x == "2" for x in vals):
        return "NO"
    return "NR"


def _measure(rows: list[dict[str, str]], year: str) -> dict:
    entries = []
    for row in rows:
        age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
        try:
            weight = float(row["FAC_MOCIBA"])
        except ValueError:
            weight = -1
        maxage = 59 if year == "2017" else 97
        if 12 <= age <= maxage and weight > 0 and math.isfinite(weight):
            if year == "2015" or (row["EST_DIS"] and row["UPM_DIS"]):
                entries.append((row, weight))
    groups = sorted({d for row, _ in entries for d in _domains(row, year)})
    cluster_keys = sorted({(row["EST_DIS"], row["UPM_DIS"]) for row, _ in entries}) if year != "2015" else []
    index = {key: i for i, key in enumerate(cluster_keys)}
    draws = (_replicate_weights(np.array([s for s, _ in cluster_keys]),
                                np.array([p for _, p in cluster_keys]))
             if year != "2015" else None)
    domain_sets = [set(_domains(row, year)) for row, _ in entries]
    states = {
        "ciberacoso": [_victim(row, year) for row, _ in entries],
        "bloqueo": [_response(row, year, "bloqueo") for row, _ in entries],
        "denuncia": [_response(row, year, "denuncia") for row, _ in entries],
    }
    cells = []
    total_reps = {}
    for measure, values in states.items():
        for domain in groups:
            counts = Counter(values[i] for i, ds in enumerate(domain_sets) if domain in ds)
            eligible = [i for i, ds in enumerate(domain_sets)
                        if domain in ds and values[i] in ("SI", "NO")]
            cell = {"medida": measure, "dominio": domain, "n": len(eligible),
                    "estados": {k: int(counts[k]) for k in ("SI", "NO", "NS", "NR", "SALTO")}}
            if len(eligible) < 100:
                cell["estado"] = "SUPRIMIDA-N-MENOR-100"
                cells.append(cell)
                continue
            if year == "2015":
                # FD 2015 sólo publica UPM y peso; no publica estrato de diseño.
                cell["estado"] = "NO-ESTIMABLE-SIN-EST_DIS"
                cells.append(cell)
                continue
            den = np.zeros(len(cluster_keys))
            num = np.zeros(len(cluster_keys))
            for i in eligible:
                row, weight = entries[i]
                j = index[(row["EST_DIS"], row["UPM_DIS"])]
                den[j] += weight
                if values[i] == "SI":
                    num[j] += weight
            point = float(num.sum() / den.sum())
            rep_den = draws @ den
            rep_num = draws @ num
            reps = np.divide(rep_num, rep_den, out=np.full(len(draws), np.nan), where=rep_den > 0)
            good = reps[np.isfinite(reps)]
            if len(good) < 380:
                cell["estado"] = "NO-ESTIMABLE-REPLICAS"
            else:
                lo, hi = np.quantile(good, [0.025, 0.975])
                cell.update(estado="ESTIMABLE", punto=point, ic95=[float(lo), float(hi)],
                            peso_denominador=float(den.sum()), n_upm=int(np.count_nonzero(den)))
                if domain == "TOTAL":
                    total_reps[measure] = [round(float(x), 9) for x in good]
            cells.append(cell)
    return {"n_tabla": len(rows), "n_universo": len(entries),
            "n_estratos": len({s for s, _ in cluster_keys}), "n_upm": len(cluster_keys),
            "replicas": {"B": 399 if draws is not None else 0,
            "semilla": 20260923, "total_por_medida": total_reps}, "celdas": cells}


def medir(inputs: dict, contrato: dict) -> dict:
    year = str(contrato["parametros"]["ola"])
    path = next(Path(item["ruta_absoluta"]) for item in inputs.values()
                if str(item["ruta_absoluta"]).lower().endswith("bd_dbf.zip"))
    rows = _load(path, FILES[year], _fields(year))
    result = _measure(rows, year)
    return {f"RESULT-MOCIBA-PISOS-{year}-TABLA": json.dumps(result, ensure_ascii=False, sort_keys=True)}
