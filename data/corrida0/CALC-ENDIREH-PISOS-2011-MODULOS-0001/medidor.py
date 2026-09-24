"""ENDIREH 2016, módulos por situación conyugal de la ola 2011.

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

PAYLOAD = "endireh_2011_bd_endireh_2011_csv"
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
    # FD 2011: 00 ninguna, 01-03 y 05 basica, 04/06/07 media, 08/09 superior.
    if level == 0:
        return "ninguno"
    if level in {1, 2, 3, 5}:
        return "basica"
    if level in {4, 6, 7}:
        return "media_superior"
    if level in {8, 9}:
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




KEY = ("CONTROL", "VIV_SEL", "HOGAR", "R_SEL_M")
STATES = {"A": ("TUnidas1.csv", "TUnidas2.csv", "TUnidas3.csv"),
          "B": ("TDunida1.csv", "TDunida2.csv", "TDunida3.csv"),
          "C": ("TSolter1.csv", "TSolter2.csv", None)}
ACTOR_DOMAINS = {"familiar_agresor": {"01", "02", "03", "04", "05", "06"},
                 "laboral_agresor": {"07", "08"},
                 "escolar_agresor": {"09", "10", "11"}}
PLACE_DOMAINS = {"comunitaria_lugar": {"01", "06", "07", "08"},
                 "escolar_lugar": {"02"}, "laboral_lugar": {"03", "04"}}


def _key(r):
    return tuple(r.get(k, "") for k in KEY)


def _dem_key(r):
    return (r.get("CONTROL", ""), r.get("VIV_SEL", ""), r.get("HOGAR", ""), r.get("N_REN", ""))


def _read(archive, name):
    with _member(archive, name) as stream:
        return list(csv.DictReader(stream))


def _base(r, dem, state):
    age, level = dem.get(_key(r), (None, None))
    age_group = _age_group(age)
    try:
        weight = float(r["FAC_PER"])
    except (ValueError, KeyError):
        return None
    if age_group is None or not np.isfinite(weight) or weight <= 0:
        return None
    if not r.get("EST_DIS") or not r.get("UPM_DIS"):
        return None
    return {"weight": weight, "stratum": r["EST_DIS"], "psu": r["UPM_DIS"],
            "edad": age_group, "escolaridad": _school_group(level),
            "localidad": r.get("DOMINIO"), "pareja": state, "entidad": r.get("CVE_ENT")}


def _freq(values):
    vals = [str(v or "").strip() for v in values]
    if any(v in {"1", "2", "3"} for v in vals):
        return 1
    if vals and all(v == "4" for v in vals):
        return 0
    return None


def _binary(value):
    v = str(value or "").strip()
    return 1 if v == "1" else 0 if v == "2" else None


def _union_binary(values):
    vals = [str(v or "").strip() for v in values]
    if any(v == "1" for v in vals):
        return 1
    if vals and all(v == "2" for v in vals):
        return 0
    return None


def _domain_act(r, prefix, i, codes, field):
    act = r.get(f"{prefix}2_6_{i}")
    if act == "2":
        return 0, 0
    if act != "1":
        return None, None
    paired = [(r.get(f"{prefix}{field}_{i}_{j}", "").strip(),
               r.get(f"{prefix}2_9_{i}_{j}", "").strip()) for j in (1, 2)]
    matched = [recent for value, recent in paired if value in codes]
    if matched:
        return 1, _union_binary(matched)
    valid = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"} if field == "2_7" else {"01", "02", "03", "04", "05", "06", "07", "08", "09"}
    if any(value in valid for value, _ in paired):
        return 0, 0
    return None, None


def _external(r, state, base):
    prefix = state + "P"
    base["prueba_embarazo_vida"] = _binary(r.get(prefix + "2_1"))
    base["perjuicio_embarazo_vida"] = _binary(r.get(prefix + "2_2"))
    if r.get(prefix + "2_3_1") == "1":
        base["discriminacion_laboral_desde_octubre_2010"] = _union_binary(
            [r.get(f"{prefix}2_5_{i}") for i in range(1, 6)])
        for i in range(1, 6):
            base[f"discriminacion_laboral_item_{i:02d}"] = _binary(r.get(f"{prefix}2_5_{i}"))
    else:
        base["discriminacion_laboral_desde_octubre_2010"] = None
        for i in range(1, 6):
            base[f"discriminacion_laboral_item_{i:02d}"] = None
    for label, codes in {**ACTOR_DOMAINS, **PLACE_DOMAINS}.items():
        vals = [_domain_act(r, prefix, i, codes, "2_7" if label in ACTOR_DOMAINS else "2_8")
                for i in range(1, 13)]
        for w, ix in (("vida", 0), ("desde_octubre_2010", 1)):
            known = [v[ix] for v in vals]
            base[f"externo_{label}_{w}"] = (1 if 1 in known else 0 if all(x == 0 for x in known) else None)
    # 2.10/2.12 were collected for situations 1-9 only; 10-12 have no
    # institutional follow-up in the released questionnaire.
    any_act = _union_binary([r.get(f"{prefix}2_6_{i}") for i in range(1, 10)])
    visits = [r.get(f"{prefix}2_10_{i}_{j}", "").strip() for i in range(1, 10) for j in (1, 2)]
    authority = {f"{i:02d}" for i in range(1, 10)}
    base["externo_ayuda_autoridad"] = (1 if any(v in authority for v in visits) else
        0 if any(v in {"10", "11"} for v in visits) else None) if any_act == 1 else None
    base["externo_informo_familia"] = (1 if "10" in visits else
        0 if any(v in authority | {"11"} for v in visits) else None) if any_act == 1 else None
    outcomes = [r.get(f"{prefix}2_12_{i}_{j}", "").strip() for i in range(1, 10) for j in (1, 4 + 1)]
    base["externo_denuncia_ultima_visita"] = (1 if "1" in outcomes else
        0 if any(v in {"2", "3", "4", "5", "6", "7", "8"} for v in outcomes) else None) if base["externo_ayuda_autoridad"] == 1 else None
    property_prefix = "CP3_1_" if state == "C" else prefix + "3_7_"
    base["despojo_bienes_vida"] = _union_binary([r.get(property_prefix + str(i)) for i in range(1, 4)])


def _partner_groups(state):
    if state == "C":
        return {"fisica": range(12, 19), "emocional_control": range(1, 11),
                "economica_patrimonial": (11,), "sexual": range(19, 22),
                "alguna": range(1, 22)}
    return {"fisica": range(20, 28), "emocional_control": range(1, 14),
            "economica_patrimonial": range(14, 20), "sexual": range(28, 31),
            "alguna": range(1, 31)}


def _reason(r, prefix, number, count, eligible):
    marked = any(str(r.get(f"{prefix}{i}", "")).strip().lstrip("0") == str(i)
                 for i in range(1, count + 1))
    if not eligible or not marked:
        return None
    return 1 if str(r.get(f"{prefix}{number}", "")).strip().lstrip("0") == str(number) else 0


def _partner(first, second, third, state, base):
    if state == "C" and first.get("CP4_1") not in {"1", "2"}:
        return
    prefix = state + "P"
    for group, nums in _partner_groups(state).items():
        life_vals = [second.get(f"{prefix}6_1_{i}") for i in nums]
        life = _freq(life_vals)
        recent = [("4" if v == "4" else second.get(f"{prefix}6_3_{i}")) for i, v in zip(nums, life_vals)]
        base[f"pareja_{group}_vida"] = life
        base[f"pareja_{group}_desde_octubre_2010"] = _freq(recent) if life is not None else None
    violence = base["pareja_alguna_vida"]
    help_prefix, count = ("CP6_4_", 6) if state == "C" else (prefix + "6_5_", 6)
    institution = [second.get(help_prefix + str(i)) for i in range(1, count + 1)]
    help_ = _union_binary(institution) if violence == 1 else None
    base["pareja_ayuda_institucional"] = help_
    for i in range(1, count + 1):
        base[f"pareja_institucion_{i:02d}"] = _binary(second.get(help_prefix + str(i))) if help_ == 1 else None
    if state == "C":
        base["pareja_informo_familia"] = _binary(second.get("CP6_4_7")) if violence == 1 else None
        reason_source, reason_prefix = second, "CP6_7_"
    else:
        values = [second.get(f"{prefix}6_8_{i}_{j}", "").strip() for i in range(1, 7) for j in (1, 2)]
        base["pareja_denuncia_ultima_visita"] = (1 if "01" in values else
            0 if any(v in {f"{i:02d}" for i in range(2, 11)} for v in values) else None) if help_ == 1 else None
        reason_source, reason_prefix = (second if state == "A" else third), prefix + "6_11_"
    for i in range(1, 14):
        base[f"pareja_razon_{i:02d}"] = _reason(reason_source, reason_prefix, i, 13, help_ == 0)


def _decisions(second, third, state, base):
    if state == "A":
        base["dinero_libre"] = _binary(third.get("AP8_1"))
        for i, label in ((3, "decision_su_dinero"), (6, "decision_gasto")):
            v = third.get(f"AP7_1_{i}")
            base[label] = 1 if v in {"1", "3"} else 0 if v == "2" else None
    elif state == "B":
        base["dinero_libre"] = _binary(third.get("BP7_1"))
    else:
        for i in range(1, 8):
            v = second.get(f"CP7_1_{i}")
            base[f"permiso_{i:02d}"] = 1 if v == "1" else 0 if v in {"2", "3"} else None


def _table(rows, outcomes, replicas, seed):
    axes = {"nacional": ["MX"], "edad": ["15-29", "30-44", "45-59", "60+"],
            "escolaridad": ["ninguno", "basica", "media_superior", "superior"],
            "localidad": ["U", "R"], "pareja": ["A", "B", "C"],
            "entidad": [f"{i:02d}" for i in range(1, 33)]}
    out = []
    for outcome in outcomes:
        categories = {"nacional": ["MX"]} if outcome.startswith("pareja_razon_") or outcome.startswith("pareja_institucion_") else axes
        for axis, cats in categories.items():
            for cat in cats:
                x = _aggregate(rows, outcome, axis, cat, seed + sum(map(ord, outcome + axis + cat)), replicas)
                out.append({"resultado": outcome, "eje": axis, "categoria": cat, **x})
    return out


def medir(inputs, contrato):
    with zipfile.ZipFile(inputs[PAYLOAD]["ruta_absoluta"]) as archive:
        dem = {_dem_key(r): (r.get("EDAD"), r.get("NIV")) for r in _read(archive, "TSDem.csv")}
        rows = []
        for state, (f1, f2, f3) in STATES.items():
            second = {_key(r): r for r in _read(archive, f2)}
            third = {_key(r): r for r in _read(archive, f3)} if f3 else {}
            for r in _read(archive, f1):
                base = _base(r, dem, state)
                if base is None:
                    continue
                s = second.get(_key(r), {})
                t = third.get(_key(r), {})
                _external(r, state, base)
                _partner(r, s, t, state, base)
                _decisions(s, t, state, base)
                rows.append(base)
    excluded = {"weight", "stratum", "psu", "edad", "escolaridad", "localidad", "pareja", "entidad"}
    outcomes = sorted({k for r in rows for k in r if k not in excluded})
    table = _table(rows, outcomes, int(contrato["parametros"]["bootstrap_replicas"]),
                   int(contrato["seed"]["valor"]))
    return {"RESULT-ENDIREH2011-MOD-TABLA": json.dumps(table, ensure_ascii=False, sort_keys=True),
            "RESULT-ENDIREH2011-MOD-SOPORTE": len(rows)}
