"""ENDIREH 2021, discriminación laboral 8.3; agregados de diseño únicamente."""
from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import defaultdict

import numpy as np

PAYLOAD = "endireh2021_bd_csv_zip"


def _member(archive, basename):
    names = [n for n in archive.namelist() if n.rsplit("/", 1)[-1] == basename]
    if len(names) != 1:
        raise ValueError(f"miembro {basename}: {len(names)} coincidencias")
    return io.TextIOWrapper(archive.open(names[0]), encoding="latin-1", newline="")


def _age_group(value):
    try:
        age = int(value)
    except (ValueError, TypeError):
        return None
    if age < 15 or age > 120:
        return None
    return "15-29" if age < 30 else "30-44" if age < 45 else "45-59" if age < 60 else "60+"


def _school_group(value):
    try:
        level = int(value)
    except (ValueError, TypeError):
        return None
    if level == 0:
        return "ninguno"
    if level in {1, 2, 3, 5, 6}:
        return "basica"
    if level in {4, 7, 8}:
        return "media_superior"
    if level in {9, 10, 11}:
        return "superior"
    return None


def classify_binary(values, no_codes=("2",)):
    vals = [str(v or "").strip() for v in values]
    if any(v == "1" for v in vals):
        return 1
    if vals and all(v in no_codes for v in vals):
        return 0
    return None


def classify_pregnancy(values):
    """3 is structural ineligibility; it never counts as a pregnant negative."""
    vals = [str(v or "").strip() for v in values]
    if all(v == "3" for v in vals):
        return None
    if any(v == "1" for v in vals):
        return 1
    if all(v == "2" for v in vals):
        return 0
    return None


def _aggregate(rows, outcome, axis, category, seed, replicas):
    selected = [r for r in rows if (axis == "nacional" or r.get(axis) == category)
                and r[outcome] is not None]
    n = len(selected)
    psus = {(r["stratum"], r["psu"]) for r in selected}
    if n < 100 or len(psus) < 5:
        return {"estado": "SUPRIMIDA", "n": n, "upm": len(psus), "causa": "soporte"}
    clusters = {(r["stratum"], r["psu"]): [0.0, 0.0] for r in rows}
    for r in selected:
        c = clusters[(r["stratum"], r["psu"])]
        c[0] += r["weight"] * r[outcome]
        c[1] += r["weight"]
    strata = defaultdict(list)
    for (stratum, _), sums in clusters.items():
        strata[stratum].append(sums)
    numerator = sum(v[0] for v in clusters.values())
    denominator = sum(v[1] for v in clusters.values())
    p = numerator / denominator
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(replicas):
        num = den = 0.0
        for cells in strata.values():
            idx = rng.integers(0, len(cells), len(cells))
            for j in idx:
                num += cells[j][0]
                den += cells[j][1]
        draws.append(num / den if den else np.nan)
    valid = np.asarray([x for x in draws if np.isfinite(x)])
    if len(valid) < replicas:
        return {"estado": "SUPRIMIDA", "n": n, "upm": len(psus), "causa": "replicas"}
    lo, hi = np.quantile(valid, [0.025, 0.975])
    se = float(valid.std(ddof=1))
    if hi - lo > 0.20 or (p > 0 and se / p > 0.30):
        return {"estado": "SUPRIMIDA", "n": n, "upm": len(psus), "causa": "precision"}
    return {"estado": "PUBLICABLE", "n": n, "upm": len(psus),
            "p": p, "ic95": [float(lo), float(hi)], "se": se,
            "masa_ponderada": denominator, "replicas": draws}


OUTCOMES = ("prueba_ingreso", "prueba_continuidad", "prueba_alguna",
            "despido_embarazo", "no_renovacion_embarazo", "reduccion_embarazo",
            "perjuicio_embarazo_alguno")


def measure_rows(rows, replicas=200, seed=20260923):
    axes = {"nacional": ["MX"], "edad": ["15-29", "30-44", "45-59", "60+"],
            "escolaridad": ["ninguno", "basica", "media_superior", "superior"],
            "localidad": ["U", "C", "R"], "pareja": ["A1", "A2", "B1", "B2", "C1", "C2"],
            "entidad": [f"{i:02d}" for i in range(1, 33)]}
    out = []
    for outcome in OUTCOMES:
        for axis, categories in axes.items():
            for category in categories:
                x = _aggregate(rows, outcome, axis, category,
                               seed + sum(map(ord, outcome + axis + category)), replicas)
                out.append({"resultado": outcome, "ventana": "octubre_2016_a_entrevista",
                            "eje": axis, "categoria": category, **x})
    return out


def medir(inputs, contrato):
    with zipfile.ZipFile(inputs[PAYLOAD]["ruta_absoluta"]) as archive:
        with _member(archive, "TSDem.csv") as stream:
            dem = {r["ID_PER"]: (r["EDAD"], r["NIV"]) for r in csv.DictReader(stream)
                   if r.get("ID_PER")}
        rows = []
        with _member(archive, "TB_SEC_VIII.csv") as stream:
            for r in csv.DictReader(stream):
                if r.get("P8_2") != "1":
                    continue
                age, level = dem.get(r.get("ID_PER"), (None, None))
                age_group = _age_group(age)
                try:
                    weight = float(r["FAC_MUJ"])
                except (ValueError, KeyError):
                    continue
                if age_group is None or not np.isfinite(weight) or weight <= 0:
                    continue
                if not r.get("EST_DIS") or not r.get("UPM_DIS"):
                    continue
                t1 = classify_binary([r.get("P8_3_1_1")])
                t2 = classify_binary([r.get("P8_3_1_2")])
                pregnancy = [r.get(f"P8_3_2_{i}") for i in range(1, 4)]
                row = {"prueba_ingreso": t1, "prueba_continuidad": t2,
                       "prueba_alguna": classify_binary([r.get("P8_3_1_1"), r.get("P8_3_1_2")]),
                       "despido_embarazo": classify_pregnancy(pregnancy[:1]),
                       "no_renovacion_embarazo": classify_pregnancy(pregnancy[1:2]),
                       "reduccion_embarazo": classify_pregnancy(pregnancy[2:]),
                       "perjuicio_embarazo_alguno": classify_pregnancy(pregnancy),
                       "weight": weight, "stratum": r["EST_DIS"], "psu": r["UPM_DIS"],
                       "edad": age_group, "escolaridad": _school_group(level),
                       "localidad": r.get("DOMINIO"), "pareja": r.get("T_INSTRUM"),
                       "entidad": r.get("CVE_ENT")}
                rows.append(row)
    if not rows:
        raise ValueError("sin trabajadoras elegibles 2016-2021")
    table = measure_rows(rows, int(contrato["parametros"]["bootstrap_replicas"]),
                         int(contrato["seed"]["valor"]))
    return {"RESULT-ENDIREH2021-DIS-TABLA": json.dumps(table, ensure_ascii=False, sort_keys=True),
            "RESULT-ENDIREH2021-DIS-N-ELEGIBLES": len(rows)}
