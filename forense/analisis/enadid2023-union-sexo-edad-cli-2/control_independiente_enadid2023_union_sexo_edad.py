#!/usr/bin/env python3
"""Control independiente de puntos, reconstrucción y covarianza compartida.

No importa el medidor. Lee TSDEM con csv estándar, vuelve a formar el marco
de UPM y reproduce un contraste representativo y la estandarización.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t


EXPECTED_SHA = "995d448ab298251d441e437fc4a368f84879a8b74fa7bc103dc189434cbfaa18"
AGES = (("15_17", 15, 17), ("18_29", 18, 29), ("30_44", 30, 44),
        ("45_59", 45, 59), ("60_mas", 60, 120))
CATEGORIES = ("union_libre", "separada_union_libre", "separada_matrimonio",
              "divorciada", "viuda", "casada", "soltera")
REPLICATES, SEED, TOL = 800, 20260919, 5e-10
NCELLS = 3 * 6 * 8


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cell_id(sex, age, status):
    return (sex * 6 + age) * 8 + status


def slots(age_text, sex_text, status_text):
    try:
        age = int(age_text)
    except ValueError:
        age = None
    age_slot = 5
    for i, (_, low, high) in enumerate(AGES):
        if age is not None and low <= age <= high:
            age_slot = i
            break
    sex_slot = 0 if sex_text == "1" else 1 if sex_text == "2" else 2
    status_slot = int(status_text) - 1 if status_text in "1234567" and len(status_text) == 1 else 7
    return age, sex_slot, age_slot, status_slot


def load(zip_path):
    point = np.zeros(NCELLS)
    psu_cells = defaultdict(lambda: np.zeros(NCELLS))
    keys = set()
    audit = defaultdict(float)
    with zipfile.ZipFile(zip_path) as archive, archive.open("TSDEM.csv") as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
        for source in reader:
            row = {key.upper(): (value or "").strip() for key, value in source.items()}
            key = row["LLAVE_PER"]
            audit["filas"] += 1
            audit["llaves_duplicadas"] += key in keys
            keys.add(key)
            try:
                weight = float(row["FAC_VIV"])
            except ValueError:
                weight = math.nan
            weight_ok = math.isfinite(weight) and weight > 0
            age, sex_slot, age_slot, status_slot = slots(row["EDAD"], row["SEXO"], row["P3_27"])
            if not weight_ok:
                audit["peso_invalido_n"] += 1
                continue
            audit["masa_total"] += weight
            if age is not None and 0 <= age < 15:
                audit["edad_menor_15_n"] += 1
                audit["edad_menor_15_masa"] += weight
            if age is None or age == 999 or age < 0 or (age > 120 and age != 999):
                audit["edad_999_o_no_numerica_n"] += 1
                audit["edad_999_o_no_numerica_masa"] += weight
            if age_slot < 5 and sex_slot == 2:
                audit["sexo_desconocido_15_mas_n"] += 1
                audit["sexo_desconocido_15_mas_masa"] += weight
            idx = cell_id(sex_slot, age_slot, status_slot)
            point[idx] += weight
            if row["EST_DIS"] and row["UPM_DIS"]:
                psu_cells[(row["EST_DIS"], row["UPM_DIS"])][idx] += weight
            elif age_slot < 5:
                audit["diseno_faltante_15_mas_n"] += 1
    audit["llaves_unicas"] = len(keys)
    return point, psu_cells, dict(audit)


def bootstrap(psu_cells):
    keys = sorted(psu_cells)
    matrix = np.vstack([psu_cells[key] for key in keys])
    by_stratum = defaultdict(list)
    for index, (stratum, _) in enumerate(keys):
        by_stratum[stratum].append(index)
    multipliers = np.ones((REPLICATES, len(keys)))
    rng = np.random.default_rng(SEED)
    singleton = non_singleton = df = 0
    for stratum in sorted(by_stratum):
        indices = by_stratum[stratum]
        m = len(indices)
        if m == 1:
            singleton += 1
            continue
        counts = rng.multinomial(m - 1, np.full(m, 1 / m), size=REPLICATES)
        multipliers[:, indices] = counts * (m / (m - 1))
        non_singleton += 1
        df += m - 1
    return multipliers @ matrix, {
        "estratos": len(by_stratum), "upm_anidadas": len(keys),
        "singleton": singleton, "gl": df,
        "ajuste": (non_singleton + singleton) / non_singleton,
    }


def indices(sexes, ages, statuses):
    return [cell_id(s, a, c) for s in sexes for a in ages for c in statuses]


def mass(point, reps, sexes, ages, statuses):
    idx = indices(sexes, ages, statuses)
    return float(point[idx].sum()), reps[:, idx].sum(axis=1)


def ratio(num, den, num_rep, den_rep):
    return num / den, num_rep / den_rep


def precision(value, replicate_values, design, proportion=False):
    se = float(np.std(replicate_values, ddof=1) * math.sqrt(design["ajuste"]))
    critical = float(student_t.ppf(0.975, design["gl"]))
    if proportion:
        logit = math.log(value / (1 - value))
        se_logit = se / (value * (1 - value))
        inv = lambda x: 1 / (1 + math.exp(-x))
        lo, hi = inv(logit - critical * se_logit), inv(logit + critical * se_logit)
    else:
        lo, hi = value - critical * se, value + critical * se
    return {"punto": value, "ee": se, "ic95_lo": lo, "ic95_hi": hi}


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def number(row, key):
    return float(row[key]) if row.get(key) not in (None, "") else None


def compare(zip_path, output_dir, parent_path):
    point, psu_cells, audit = load(zip_path)
    reps, design = bootstrap(psu_cells)
    output_dir = Path(output_dir)
    distribution = read_csv(output_dir / "distribucion.csv")
    union = read_csv(output_dir / "union_condicional.csv")
    standard = read_csv(output_dir / "estandarizacion.csv")
    parent = read_csv(parent_path)

    # Reconstrucción del padre por NUM/DEN, incluyendo el slot de sexo residual.
    reconstruction = []
    age_map = {name: [i] for i, (name, _, _) in enumerate(AGES)}
    age_map["15_mas"] = list(range(5))
    for age_name, age_slots in age_map.items():
        for status_slot, category in enumerate(CATEGORIES):
            new_rows = [r for r in distribution if r["edad"] == age_name and r["categoria"] == category]
            parent_row = next(r for r in parent if r["estimando"] == "distribucion_actual_15_mas"
                              and r["edad"] == age_name and r["categoria"] == category)
            new_num = sum(number(r, "masa_numerador") for r in new_rows)
            new_den = sum(
                number(next(r for r in new_rows if r["sexo"] == sex), "masa_denominador")
                for sex in ("hombre", "mujer", "sexo_desconocido"))
            reconstruction.append({"producto": "P1", "edad": age_name,
                                   "categoria": category,
                                   "delta_num": new_num - float(parent_row["masa_numerador"]),
                                   "delta_den": new_den - float(parent_row["masa_denominador"])})
        parent_union = next(r for r in parent if r["estimando"] == "union_libre_entre_union_o_casada"
                            and r["edad"] == age_name and r["categoria"] == "union_libre")
        known_rows = [r for r in union if r["tipo"] == "tasa" and r["edad"] == age_name]
        unknown_num, _ = mass(point, reps, [2], age_slots, [0])
        unknown_den, _ = mass(point, reps, [2], age_slots, [0, 5])
        reconstruction.append({"producto": "P2", "edad": age_name,
                               "categoria": "union_libre",
                               "delta_num": sum(number(r, "masa_numerador") for r in known_rows) + unknown_num - float(parent_union["masa_numerador"]),
                               "delta_den": sum(number(r, "masa_denominador") for r in known_rows) + unknown_den - float(parent_union["masa_denominador"])})

    # Contraste 30--44 independiente, con covarianza de las mismas réplicas.
    rates, rate_reps = {}, {}
    for sex_name, sex_slot in (("hombre", 0), ("mujer", 1)):
        den, den_rep = mass(point, reps, [sex_slot], [2], [0, 5])
        num, num_rep = mass(point, reps, [sex_slot], [2], [0])
        rates[sex_name], rate_reps[sex_name] = ratio(num, den, num_rep, den_rep)
    representative = precision(rates["mujer"] - rates["hombre"],
                               rate_reps["mujer"] - rate_reps["hombre"], design)
    published_rep = next(r for r in union if r["tipo"] == "diferencia_mujer_menos_hombre"
                         and r["edad"] == "30_44")
    representative["deltas_publicado"] = {
        key: abs(representative[key] - float(published_rep[key]))
        for key in ("punto", "ee", "ic95_lo", "ic95_hi")
    }

    # Estandarización completa recalculando pesos y tasas en cada réplica.
    total, total_rep = mass(point, reps, [0, 1], range(5), [0, 5])
    weights, weight_reps = {}, {}
    std_rates, std_reps = {}, {}
    for age_slot, (age_name, _, _) in enumerate(AGES):
        den, den_rep = mass(point, reps, [0, 1], [age_slot], [0, 5])
        weights[age_name], weight_reps[age_name] = ratio(den, total, den_rep, total_rep)
    for sex_name, sex_slot in (("hombre", 0), ("mujer", 1)):
        value = np.zeros(REPLICATES)
        point_value = 0.0
        for age_slot, (age_name, _, _) in enumerate(AGES):
            den, den_rep = mass(point, reps, [sex_slot], [age_slot], [0, 5])
            num, num_rep = mass(point, reps, [sex_slot], [age_slot], [0])
            rate, rate_rep = ratio(num, den, num_rep, den_rep)
            point_value += weights[age_name] * rate
            value += weight_reps[age_name] * rate_rep
        std_rates[sex_name], std_reps[sex_name] = point_value, value
    std_diff = precision(std_rates["mujer"] - std_rates["hombre"],
                         std_reps["mujer"] - std_reps["hombre"], design)
    published_std = next(r for r in standard if r["tipo"] == "diferencia_estandarizada")
    std_diff["deltas_publicado"] = {
        key: abs(std_diff[key] - float(published_std[key]))
        for key in ("punto", "ee", "ic95_lo", "ic95_hi")
    }

    exhaustive = []
    for sex in ("hombre", "mujer"):
        for age in age_map:
            rows = [r for r in distribution if r["sexo"] == sex and r["edad"] == age]
            exhaustive.append(abs(sum(float(r["punto"]) for r in rows) - 1.0))
    max_reconstruction = max(abs(r[key]) for r in reconstruction for key in ("delta_num", "delta_den"))
    max_precision = max(*representative["deltas_publicado"].values(),
                        *std_diff["deltas_publicado"].values())
    checks = {
        "hash_input_ok": sha256(zip_path) == EXPECTED_SHA,
        "llave_unica": audit["llaves_duplicadas"] == 0,
        "reconstruccion_padre_max_delta_masa": max_reconstruction,
        "categorias_exhaustivas_max_delta": max(exhaustive),
        "pesos_estandar_suman": sum(weights.values()),
        "precision_representativa_max_delta": max_precision,
        "sexo_desconocido_residuo_n": int(audit.get("sexo_desconocido_15_mas_n", 0)),
    }
    return {
        "metodo": "csv/numpy/scipy independiente; no importa medidor.py",
        "input_sha256": sha256(zip_path), "auditoria_independiente": audit,
        "diseno": design, "reconstruccion": reconstruction,
        "contraste_representativo_30_44": representative,
        "estandarizacion": {"pesos": weights, "tasas": std_rates,
                            "diferencia": std_diff},
        "checks": checks,
        "todos_ok": (checks["hash_input_ok"] and checks["llave_unica"]
                     and max_reconstruction <= TOL and max(exhaustive) <= TOL
                     and abs(checks["pesos_estandar_suman"] - 1) <= TOL
                     and max_precision <= TOL),
    }


def main(argv):
    if len(argv) != 5:
        raise SystemExit(
            "uso: control_independiente_enadid2023_union_sexo_edad.py "
            "ZIP DIR_RESULTADOS PADRE_CSV SALIDA_JSON"
        )
    result = compare(argv[1], argv[2], argv[3])
    Path(argv[4]).write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                        sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result["todos_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
