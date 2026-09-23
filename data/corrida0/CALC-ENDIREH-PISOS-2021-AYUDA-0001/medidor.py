"""ENDIREH 2021, ayuda y denuncia en pareja actual, cuestionario A.

El resultado público contiene sólo agregados. La incertidumbre remuestrea
UPM dentro de estrato y conserva réplicas de proporciones, sin microregistros.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import defaultdict

import numpy as np

PAYLOAD = "endireh2021_bd_csv_zip"
MEMBER = "TB_SEC_XIV.csv"
DEM = "TSDem.csv"
PHYSICAL = tuple(range(1, 10))


def classify(values):
    """1/2/3=ocurrió; 4=no ocurrió; 9, blanco y saltos=desconocido."""
    vals = [str(x).strip() for x in values]
    if any(v in {"1", "2", "3"} for v in vals):
        return 1
    if vals and all(v == "4" for v in vals):
        return 0
    return None


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
    # NIV, FD 2021, TSDem: 00 ninguno, 01-03 hasta secundaria,
    # 04, 07, 08 media superior/técnica; 05-06 técnicos con menor
    # antecedente se agrupan en básica; 09-11 normal/licenciatura/posgrado.
    if level == 0:
        return "ninguno"
    if level in {1, 2, 3, 5, 6}:
        return "basica"
    if level in {4, 7, 8}:
        return "media_superior"
    if level in {9, 10, 11}:
        return "superior"
    return None


def _aggregate(rows, window, axis, category, seed, replicas):
    selected = [r for r in rows if (axis == "nacional" or r.get(axis) == category)
                and r[window] is not None]
    n = len(selected)
    psus = {(r["stratum"], r["psu"]) for r in selected}
    if n < 100 or len(psus) < 5:
        return {"estado": "SUPRIMIDA", "n": n, "upm": len(psus), "causa": "soporte"}
    # Remuestrear el marco completo: una UPM sin respuestas en el dominio
    # contribuye (0, 0), pero sigue en su estrato y afecta la incertidumbre.
    clusters = {(r["stratum"], r["psu"]): [0.0, 0.0] for r in rows}
    for r in selected:
        c = clusters[(r["stratum"], r["psu"])]
        c[0] += r["weight"] * r[window]
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



SPECIAL = {23, 24, 35, 36, 37, 38}
ACTS = [f"P14_1_{i}{'AB' if i in SPECIAL else ''}" for i in range(1, 39)]


def _yesno(value):
    value = str(value or "").strip()
    return 1 if value == "1" else 0 if value == "2" else None


def _reason(value):
    value = str(value or "").strip()
    return 1 if value == "1" else 0 if value == "0" else None


def measure_rows(rows, replicas=500, seed=20260923):
    axes = {"nacional": ["MX"], "edad": ["15-29", "30-44", "45-59", "60+"],
            "escolaridad": ["ninguno", "basica", "media_superior", "superior"],
            "localidad": ["U", "C", "R"], "pareja": ["A1", "A2"],
            "entidad": [f"{i:02d}" for i in range(1, 33)]}
    out = []
    for outcome in ("ayuda", "denuncia"):
        for axis, cats in axes.items():
            for cat in cats:
                x = _aggregate(rows, outcome, axis, cat,
                               seed + sum(map(ord, outcome + axis + cat)), replicas)
                out.append({"resultado": outcome, "eje": axis, "categoria": cat, **x})
    for prefix, count in (("institucion", 10), ("razon", 15)):
        for i in range(1, count + 1):
            outcome = f"{prefix}_{i:02d}"
            x = _aggregate(rows, outcome, "nacional", "MX",
                           seed + sum(map(ord, outcome)), replicas)
            out.append({"resultado": outcome, "eje": "nacional", "categoria": "MX", **x})
    return out


def medir(inputs, contrato):
    with zipfile.ZipFile(inputs[PAYLOAD]["ruta_absoluta"]) as archive:
        with _member(archive, DEM) as stream:
            dem = {r["ID_PER"]: (r["EDAD"], r["NIV"]) for r in csv.DictReader(stream)
                   if r.get("ID_PER")}
        with _member(archive, "TB_SEC_XIV_2.csv") as stream:
            reasons = {r["ID_PER"]: [r.get(f"P14_22_{i}", "") for i in range(1, 16)]
                       for r in csv.DictReader(stream) if r.get("ID_PER")}
        rows = []
        with _member(archive, MEMBER) as stream:
            for r in csv.DictReader(stream):
                if r.get("T_INSTRUM") not in {"A1", "A2"}:
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
                violence = classify([r.get(c, "") for c in ACTS])
                help_ = _yesno(r.get("P14_7_1")) if violence == 1 else None
                report = _yesno(r.get("P14_7_2")) if violence == 1 else None
                row = {"ayuda": help_, "denuncia": report, "weight": weight,
                       "stratum": r["EST_DIS"], "psu": r["UPM_DIS"],
                       "edad": age_group, "escolaridad": _school_group(level),
                       "localidad": r.get("DOMINIO"), "pareja": r["T_INSTRUM"],
                       "entidad": r.get("CVE_ENT")}
                for i in range(1, 11):
                    row[f"institucion_{i:02d}"] = (
                        _yesno(r.get(f"P14_8_{i}")) if help_ == 1 else None)
                vals = reasons.get(r.get("ID_PER"), [])
                for i in range(1, 16):
                    row[f"razon_{i:02d}"] = (
                        _reason(vals[i-1]) if help_ == 0 and report == 0 and len(vals) == 15
                        else None)
                rows.append(row)
    if not rows:
        raise ValueError("sin mujeres elegibles")
    table = measure_rows(rows, int(contrato["parametros"]["bootstrap_replicas"]),
                         int(contrato["seed"]["valor"]))
    return {"RESULT-ENDIREH2021-AYU-TABLA": json.dumps(table, ensure_ascii=False, sort_keys=True),
            "RESULT-ENDIREH2021-AYU-N-ELEGIBLES": len(rows)}
