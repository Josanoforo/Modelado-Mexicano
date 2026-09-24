"""ENDIREH 2016, módulos por estado conyugal de la ola 2006.

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

PAYLOAD = "endireh_2006_bd_endireh_2006_csv"
MEMBER = "TB_SEC_XIII.csv"
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
    # Cuestionario 2006, 2.5: 00 ninguna, 01-03 preescolar/secundaria,
    # 04-06 tecnica y bachillerato, 07-10 normal/posgrado.
    if level == 0:
        return "ninguno"
    if level in {1, 2, 3}:
        return "basica"
    if level in {4, 5, 6}:
        return "media_superior"
    if level in {7, 8, 9, 10}:
        return "superior"
    return None


def _aggregate(rows, window, axis, category, seed, replicas):
    selected = [r for r in rows if (axis == "nacional" or r.get(axis) == category)
                and r.get(window) is not None]
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




KEY = ("N_CON", "V_SEL", "N_REN")
CONJUGAL = {
    "MC": {"labor_elig": "P3_15", "labor": "P3_19_", "disc": "P3_18_",
           "labor_den": "P3_20", "school_elig": "P3_21", "school": "P3_22_",
           "school_help": "P3_23_", "community": "P3_24_", "community_help": "P3_25_"},
    "MD": {"labor_elig": "P3_13", "labor": "P3_17_", "disc": "P3_16_",
           "labor_den": "P3_18", "school_elig": "P3_19", "school": "P3_20_",
           "school_help": "P3_21_", "community": "P3_22_", "community_help": "P3_23_"},
    "MS": {"labor_elig": "P12", "labor": "P16_", "disc": "P15_",
           "labor_den": "P17", "school_elig": "P9", "school": "P10_",
           "school_help": "P11_", "community": "P7_", "community_help": "P8_"},
}


def _key(r):
    return tuple(r.get(k, "") for k in KEY)


def _classify(values, positive, negative):
    vals = [str(x or "").strip() for x in values]
    if any(v in positive for v in vals):
        return 1
    if vals and all(v in negative for v in vals):
        return 0
    return None


def _binary(value):
    v = str(value or "").strip()
    return 1 if v == "1" else 0 if v == "2" else None


def _selected(r, prefix, i):
    v = str(r.get(prefix + str(i), "")).strip()
    return v.lstrip("0") == str(i)


def _help_flags(r, prefix, count):
    if any(_selected(r, prefix, i) for i in range(1, count)):
        return 1
    if _selected(r, prefix, count):
        return 0
    return None


def _base(r, dem, state):
    age, level = dem.get(_key(r), (None, None))
    age_group = _age_group(age)
    try:
        weight = float(r["FAC_PER"])
    except (ValueError, KeyError):
        return None
    if age_group is None or not np.isfinite(weight) or weight <= 0:
        return None
    if not r.get("ZEST") or not r.get("ZUPM"):
        return None
    ent = r.get("CVE_ENT")
    return {"weight": weight, "stratum": (ent, r["ZEST"]),
            "psu": (ent, r["ZUPM"]), "edad": age_group,
            "escolaridad": _school_group(level), "localidad": r.get("DOM"),
            "pareja": state, "entidad": ent}


def _read(archive, name):
    with _member(archive, name) as stream:
        return list(csv.DictReader(stream))


def _outcomes(r, state, cfg, base):
    working = r.get(cfg["labor_elig"]) in {str(i) for i in range(1, 8)}
    school = r.get(cfg["school_elig"]) == "1"
    labor_vals = [r.get(cfg["labor"] + str(i)) for i in range(1, 8)]
    disc_vals = [r.get(cfg["disc"] + str(i)) for i in range(1, 7)]
    school_vals = [r.get(cfg["school"] + str(i)) for i in range(1, 8)]
    community_vals = [r.get(cfg["community"] + str(i)) for i in range(1, 6)]
    base["laboral_anual"] = _classify(labor_vals, {"1"}, {"2"}) if working else None
    base["discriminacion_laboral_anual"] = _classify(disc_vals, {"1"}, {"2"}) if working else None
    base["escolar_vida"] = _classify(school_vals, {"1"}, {"2"}) if school else None
    base["comunitaria_vida"] = _classify(community_vals, {"1"}, {"2"})
    base["familiar_anual"] = _classify([r.get("P18_" + str(i)) for i in range(1, 8)], {"1"}, {"2"}) if state == "MS" else _classify([r.get("P5_11_" + str(i)) for i in range(1, 8)], {"1"}, {"2"})
    labor_any = _classify(labor_vals + disc_vals, {"1"}, {"2"}) if working else None
    base["laboral_denuncia"] = _binary(r.get(cfg["labor_den"])) if labor_any == 1 else None
    school_help_count = 6
    community_help_count = 5
    base["escolar_aviso_o_denuncia"] = _help_flags(r, cfg["school_help"], school_help_count) if base["escolar_vida"] == 1 else None
    base["comunitaria_aviso_o_denuncia"] = _help_flags(r, cfg["community_help"], community_help_count) if base["comunitaria_vida"] == 1 else None
    for i in range(1, 7):
        v = str(r.get(cfg["disc"] + str(i), "")).strip()
        base[f"discriminacion_item_{i:02d}"] = (1 if v == "1" else 0 if v == "2" else None) if working else None


def _partner_ab(r, base):
    acts = [r.get(f"P7_1_{i}") for i in range(1, 31)]
    recent = [("3" if e == "3" else r.get(f"P7_4_{i}")) for i, e in enumerate(acts, 1)]
    groups = {"fisica": range(1, 9), "emocional_control": range(9, 22),
              "economica_patrimonial": range(22, 28), "sexual": range(28, 31),
              "alguna": range(1, 31)}
    for g, nums in groups.items():
        idx = [i - 1 for i in nums]
        life = _classify([acts[i] for i in idx], {"1", "2"}, {"3"})
        annual = _classify([recent[i] for i in idx], {"1", "2"}, {"3"}) if life is not None else None
        base[f"pareja_{g}_vida"] = life
        base[f"pareja_{g}_anual"] = annual
    violence = base["pareja_alguna_vida"]
    help_ = _help_flags(r, "P7_7_", 4) if violence == 1 else None
    base["pareja_ayuda_autoridad"] = help_
    base["pareja_denuncia_en_autoridad"] = (1 if _selected(r, "P7_10_", 1) else
        0 if help_ == 1 and any(_selected(r, "P7_10_", i) for i in range(2, 8)) else None)
    reason_count = 12 if base["pareja"] == "MC" else 11
    any_reason = any(_selected(r, "P7_12_", i) for i in range(1, reason_count + 1))
    for i in range(1, reason_count + 1):
        base[f"pareja_razon_{i:02d}"] = (1 if _selected(r, "P7_12_", i) else 0) if help_ == 0 and any_reason else None


def _partner_c(r, base):
    if r.get("P23") not in {"1", "2"}:
        return
    groups = {"fisica": range(1, 5), "emocional_control": (*range(5, 10), *range(14, 17)),
              "economica_patrimonial": (10,), "sexual": range(11, 14),
              "alguna": range(1, 17)}
    for g, nums in groups.items():
        base[f"pareja_{g}_vida"] = _classify([r.get(f"P28_{i}_1") for i in nums], {"1"}, {"2"})
    positives = [i for i in range(1, 17) if r.get(f"P28_{i}_1") == "1"]
    base["pareja_denuncia_o_aviso_familiar"] = (_classify([r.get(f"P28_{i}_2") for i in positives], {"1"}, {"2"})
                                                      if positives else None)


def _decisions(r, base):
    base["dinero_personal"] = _binary(r.get("P9_3"))
    for i, label in ((3, "decision_su_dinero"), (6, "decision_gasto")):
        v = r.get(f"P8_1_{i}")
        base[label] = 1 if v in {"1", "3"} else 0 if v == "2" else None


def _table(rows, outcomes, replicas, seed):
    axes = {"nacional": ["MX"], "edad": ["15-29", "30-44", "45-59", "60+"],
            "escolaridad": ["ninguno", "basica", "media_superior", "superior"],
            "localidad": sorted({r["localidad"] for r in rows if r["localidad"]}),
            "pareja": ["MC", "MD", "MS"], "entidad": [f"{i:02d}" for i in range(1, 33)]}
    out = []
    for outcome in outcomes:
        categories = {"nacional": ["MX"]} if outcome.startswith("pareja_razon_") else axes
        for axis, cats in categories.items():
            for cat in cats:
                x = _aggregate(rows, outcome, axis, cat, seed + sum(map(ord, outcome + axis + cat)), replicas)
                out.append({"resultado": outcome, "eje": axis, "categoria": cat, **x})
    return out


def medir(inputs, contrato):
    with zipfile.ZipFile(inputs[PAYLOAD]["ruta_absoluta"]) as archive:
        dem = {_key(r): (r.get("EDAD"), r.get("NIV")) for r in _read(archive, "06_DS.csv")}
        rows = []
        for state in ("MC", "MD", "MS"):
            first = _read(archive, f"06_{state}1.csv" if state != "MS" else "06_MS.csv")
            second = {_key(r): r for r in _read(archive, f"06_{state}2.csv")} if state != "MS" else {}
            third = {_key(r): r for r in _read(archive, f"06_{state}3.csv")} if state != "MS" else {}
            for r in first:
                base = _base(r, dem, state)
                if base is None:
                    continue
                _outcomes(r, state, CONJUGAL[state], base)
                if state == "MS":
                    _partner_c(r, base)
                else:
                    partner = second.get(_key(r))
                    if partner:
                        _partner_ab(partner, base)
                    if state == "MC":
                        decisions = third.get(_key(r))
                        if decisions:
                            _decisions(decisions, base)
                rows.append(base)
    outcomes = sorted({key for r in rows for key in r if key not in {"weight", "stratum", "psu", "edad", "escolaridad", "localidad", "pareja", "entidad"}})
    table = _table(rows, outcomes, int(contrato["parametros"]["bootstrap_replicas"]),
                   int(contrato["seed"]["valor"]))
    return {"RESULT-ENDIREH2006-MOD-TABLA": json.dumps(table, ensure_ascii=False, sort_keys=True),
            "RESULT-ENDIREH2006-MOD-SOPORTE": len(rows)}
