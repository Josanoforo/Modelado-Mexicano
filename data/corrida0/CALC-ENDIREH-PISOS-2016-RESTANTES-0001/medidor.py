"""ENDIREH 2016, ámbitos, ayuda y economía de la ola 2016.

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

PAYLOAD = "endireh_2016_bd_mujeres_endireh2016_sitioinegi_csv"
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



MODULES = {
    "escolar": ("TB_SEC_VI.csv", "P6_1", "P6_2", "P6_6_", "P6_8_", 17, "P6_13_"),
    "laboral": ("TB_SEC_VII.csv", "P7_1", "P7_4", "P7_9_", "P7_11_", 18, "P7_16_"),
    "comunitaria": ("TB_SEC_VIII.csv", None, None, "P8_1_", "P8_3_", 15, "P8_8_"),
    "familiar": ("TB_SEC_X.csv", None, None, "P10_1_", None, 18, "P10_6_"),
}
SERVICE = {
    "escolar": ("P6_14_", 10, "P6_24_", 11),
    "laboral": ("P7_17_", 10, "P7_27_", 11),
    "comunitaria": ("P8_9_", 10, "P8_19_", 11),
    "familiar": ("P10_7_", 11, "P10_15_", 11),
    "pareja": ("P13_8_", 11, "P13_21_", 15),
}
SPECIAL = {23, 24, 33, 34, 35, 36}
PARTNER_GROUPS = {
    "fisica_bc": tuple(range(1, 10)),
    "emocional_control": tuple(range(10, 25)),
    "sexual": tuple(range(25, 30)),
    "digital": (30, 31),
    "economica_patrimonial": tuple(range(32, 37)),
    "no_fisica_alguna": tuple(range(10, 37)),
}


def _binary(v):
    v = str(v or "").strip()
    return 1 if v == "1" else 0 if v == "2" else None


def classify_yesno(values):
    vals = [str(v or "").strip() for v in values]
    if any(v == "1" for v in vals):
        return 1
    if vals and all(v == "2" for v in vals):
        return 0
    return None


def classify_freq(values):
    vals = [str(v or "").strip() for v in values]
    if any(v in {"1", "2", "3"} for v in vals):
        return 1
    if vals and all(v == "4" for v in vals):
        return 0
    return None


def _axes(rows):
    return {"nacional": ["MX"], "edad": ["15-29", "30-44", "45-59", "60+"],
            "escolaridad": ["ninguno", "basica", "media_superior", "superior"],
            "localidad": ["U", "C", "R"],
            "pareja": sorted({r["pareja"] for r in rows if r["pareja"]}),
            "entidad": [f"{i:02d}" for i in range(1, 33)]}


def _table(rows, outcomes, replicas, seed):
    out = []
    axes = _axes(rows)
    for outcome in outcomes:
        for axis, categories in axes.items():
            for category in categories:
                x = _aggregate(rows, outcome, axis, category,
                               seed + sum(map(ord, outcome + axis + category)), replicas)
                out.append({"resultado": outcome, "eje": axis, "categoria": category, **x})
    return out


def _national(rows, outcomes, replicas, seed):
    return [{"resultado": outcome, "eje": "nacional", "categoria": "MX",
             **_aggregate(rows, outcome, "nacional", "MX",
                          seed + sum(map(ord, outcome)), replicas)}
            for outcome in outcomes]


def _service_fields(base, main, extra, name, violence):
    """Help/complaint, institutions and multiple reasons in their own universe."""
    help_prefix = MODULES[name][-1] if name in MODULES else "P13_7_"
    h = _binary((main if name in {"escolar", "pareja"} else extra).get(help_prefix + "1")) if violence == 1 else None
    d = _binary((main if name in {"escolar", "pareja"} else extra).get(help_prefix + "2")) if violence == 1 else None
    base[name + "_ayuda"] = h
    base[name + "_denuncia"] = d
    institution, n_inst, reason, n_reason = SERVICE[name]
    for i in range(1, n_inst + 1):
        base[f"{name}_institucion_{i:02d}"] = _binary((main if name == "pareja" else extra).get(institution + str(i))) if h == 1 else None
    for i in range(1, n_reason + 1):
        v = str(extra.get(reason + str(i), "")).strip()
        base[f"{name}_razon_{i:02d}"] = (1 if v == "1" else 0 if v == "0" else None) if h == 0 and d == 0 else None


def _service_outcomes(name):
    _, n_inst, _, n_reason = SERVICE[name]
    return ([f"{name}_institucion_{i:02d}" for i in range(1, n_inst + 1)] +
            [f"{name}_razon_{i:02d}" for i in range(1, n_reason + 1)])


def _base(r, dem):
    age, level = dem.get(r.get("ID_MUJ"), (None, None))
    age_group = _age_group(age)
    try:
        weight = float(r["FAC_MUJ"])
    except (ValueError, KeyError):
        return None
    if age_group is None or not np.isfinite(weight) or weight <= 0:
        return None
    if not r.get("EST_DIS") or not r.get("UPM_DIS"):
        return None
    return {"weight": weight, "stratum": r["EST_DIS"], "psu": r["UPM_DIS"],
            "edad": age_group, "escolaridad": _school_group(level),
            "localidad": r.get("DOMINIO"), "pareja": r.get("T_INSTRUM"),
            "entidad": r.get("CVE_ENT")}


def _measure_module(archive, name, cfg, dem, replicas, seed):
    member, eligibility, recent_eligibility, ever_prefix, recent_prefix, count, help_prefix = cfg
    aux_member = member.replace(".csv", "_2.csv")
    with _member(archive, aux_member) as stream:
        aux = {r["ID_MUJ"]: r for r in csv.DictReader(stream) if r.get("ID_MUJ")}
    rows = []
    with _member(archive, member) as stream:
        for r in csv.DictReader(stream):
            if eligibility and r.get(eligibility) != "1":
                continue
            base = _base(r, dem)
            if base is None:
                continue
            extra = aux.get(r.get("ID_MUJ"), {})
            ever_values = [r.get(f"{ever_prefix}{i}", "") for i in range(1, count + 1)]
            if name == "familiar":
                ever = classify_freq(ever_values)
                recent = None
            else:
                ever = classify_yesno(ever_values)
                recent_values = [("4" if e == "2" else (extra if name == "laboral" and i == 18 else r).get(f"{recent_prefix}{i}", ""))
                                 for i, e in enumerate(ever_values, 1)]
                recent = (classify_freq(recent_values) if ever is not None and
                          (recent_eligibility is None or r.get(recent_eligibility) == "1")
                          else None)
            base[name + "_vida" if name != "familiar" else name + "_anual"] = ever
            if name != "familiar":
                base[name + "_reciente"] = recent
            _service_fields(base, r, extra, name, ever)
            rows.append(base)
    outcomes = [name + ("_anual" if name == "familiar" else "_vida")]
    if name != "familiar":
        outcomes.append(name + "_reciente")
    outcomes += [name + "_ayuda", name + "_denuncia"]
    table = _table(rows, outcomes, replicas, seed)
    return rows, table + _national(rows, _service_outcomes(name), replicas, seed)


def _partner_act(group, instrument):
    numbers = PARTNER_GROUPS[group]
    if instrument == "C1":
        numbers = tuple(i for i in numbers if i not in SPECIAL)
    return [f"P13_1_{i}{'AB' if i in SPECIAL else ''}" for i in numbers]


def _measure_partner(archive, dem, replicas, seed):
    with _member(archive, "TB_SEC_XIII_2.csv") as stream:
        aux = {r["ID_MUJ"]: r for r in csv.DictReader(stream) if r.get("ID_MUJ")}
    rows = []
    with _member(archive, "TB_SEC_XIII.csv") as stream:
        for r in csv.DictReader(stream):
            instrument = r.get("T_INSTRUM")
            if instrument not in {"A1", "A2", "B1", "B2", "C1"}:
                continue
            base = _base(r, dem)
            if base is None:
                continue
            for group in PARTNER_GROUPS:
                if group == "fisica_bc" and instrument in {"A1", "A2"}:
                    base[group + "_vida"] = base[group + "_reciente"] = None
                    continue
                acts = _partner_act(group, instrument)
                life = classify_freq([r.get(a, "") for a in acts])
                recent_values = []
                for a in acts:
                    ever = r.get(a, "").strip()
                    recent_values.append("4" if ever == "4" else r.get(a.replace("P13_1_", "P13_3_"), ""))
                base[group + "_vida"] = life
                base[group + "_reciente"] = classify_freq(recent_values) if life is not None else None
            all_acts = [f"P13_1_{i}{'AB' if i in SPECIAL else ''}" for i in range(1, 37)
                        if instrument != "C1" or i not in SPECIAL]
            violence = classify_freq([r.get(a, "") for a in all_acts])
            _service_fields(base, r, aux.get(r.get("ID_MUJ"), {}), "pareja", violence)
            rows.append(base)
    outcomes = [g + "_" + w for g in PARTNER_GROUPS for w in ("vida", "reciente")]
    outcomes += ["pareja_ayuda", "pareja_denuncia"]
    table = _table(rows, outcomes, replicas, seed)
    return rows, table + _national(rows, _service_outcomes("pareja"), replicas, seed)


def _measure_decisions(archive, dem, replicas, seed):
    with _member(archive, "TB_SEC_IV.csv") as stream:
        money = {r["ID_MUJ"]: r.get("P4_11") for r in csv.DictReader(stream) if r.get("ID_MUJ")}
    rows = []
    with _member(archive, "TB_SEC_XIV.csv") as stream:
        for r in csv.DictReader(stream):
            if r.get("T_INSTRUM") not in {"A1", "A2"}:
                continue
            base = _base(r, dem)
            if base is None:
                continue
            base["dinero_libre"] = _binary(money.get(r.get("ID_MUJ")))
            for suffix, label in ((3, "decision_su_dinero"), (6, "decision_gasto"),
                                  (7, "decision_ahorro")):
                v = r.get(f"P14_1AB_{suffix}")
                base[label] = 1 if v in {"1", "4", "5"} else 0 if v in {"2", "3"} else None
            rows.append(base)
    return rows, _table(rows, ["dinero_libre", "decision_su_dinero", "decision_gasto",
                               "decision_ahorro"], replicas, seed)


def medir(inputs, contrato):
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    out = []
    counts = {}
    with zipfile.ZipFile(inputs[PAYLOAD]["ruta_absoluta"]) as archive:
        with _member(archive, DEM) as stream:
            dem = {r["ID_MUJ"]: (r["EDAD"], r["NIV"]) for r in csv.DictReader(stream)
                   if r.get("ID_MUJ")}
        for name, cfg in MODULES.items():
            rows, table = _measure_module(archive, name, cfg, dem, replicas, seed)
            counts[name] = len(rows)
            out.extend(table)
        rows, table = _measure_partner(archive, dem, replicas, seed)
        counts["pareja"] = len(rows)
        out.extend(table)
        rows, table = _measure_decisions(archive, dem, replicas, seed)
        counts["decisiones"] = len(rows)
        out.extend(table)
    return {"RESULT-ENDIREH2016-REST-TABLA": json.dumps(out, ensure_ascii=False, sort_keys=True),
            "RESULT-ENDIREH2016-REST-SOPORTE": json.dumps(counts, sort_keys=True)}
