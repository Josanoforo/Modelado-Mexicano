#!/usr/bin/env python3
"""ENADID 2023: unión actual por sexo/edad y estandarización común.

El bootstrap se arma sobre el marco completo de UPM/estratos. Los dominios
entran como indicadores; nunca se filtra el marco antes del remuestreo.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t


CALC_ID = "CALC-ENADID2023-UNION-SEXO-EDAD-0003"
INPUT_DATA = "enadid2023_base_datos_csv"
INPUT_FD = "enadid2023_fd_xlsx"
INPUT_QUESTIONNAIRE = "enadid2023_hogar_cuestionario_pdf"
EXPECTED_SHA256 = {
    INPUT_DATA: "995d448ab298251d441e437fc4a368f84879a8b74fa7bc103dc189434cbfaa18",
    INPUT_FD: "d56582b7ace04e2c13a1b9ea22aeea458d7b9cc02a21241e5fda29fe12b4f34c",
    INPUT_QUESTIONNAIRE: "8b046a68dc19e292522557e05d81952e8fb04c2d3a1375c93fa7192e857e3270",
}
MEMBER = "TSDEM.csv"
KEY, SEX, AGE, STATUS = "LLAVE_PER", "SEXO", "EDAD", "P3_27"
WEIGHT, STRATUM, PSU = "FAC_VIV", "EST_DIS", "UPM_DIS"
REQUIRED = {KEY, SEX, AGE, STATUS, WEIGHT, STRATUM, PSU}
REPLICATES = 800
SEED = 20260919

CATEGORIES = {
    "1": "union_libre", "2": "separada_union_libre",
    "3": "separada_matrimonio", "4": "divorciada", "5": "viuda",
    "6": "casada", "7": "soltera",
}
AGES = (
    ("15_17", 15, 17), ("18_29", 18, 29), ("30_44", 30, 44),
    ("45_59", 45, 59), ("60_mas", 60, 120),
)
SEXES = (("hombre", "1", 0), ("mujer", "2", 1),
         ("sexo_desconocido", None, 2))
NCELLS = 3 * 6 * 8  # sexo conocido/desconocido × cinco edades/residuo × 7/residuo


def _raw(entry: dict) -> bytes:
    value = entry.get("bytes")
    return value if value is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_frame(raw_zip: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP-CORRUPTO")
        if MEMBER not in {item.filename for item in archive.infolist()}:
            raise ValueError(f"MIEMBRO-AUSENTE:{MEMBER}")
        frame = pd.read_csv(
            archive.open(MEMBER), dtype=str, encoding="utf-8-sig",
            low_memory=False, usecols=lambda name: name.upper() in REQUIRED,
        )
    frame.columns = [name.upper() for name in frame.columns]
    return frame


def prepare(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        raise ValueError(f"COLUMNAS-AUSENTES:{','.join(missing)}")
    out = frame.copy()
    for column in (KEY, SEX, STATUS, STRATUM, PSU):
        out[column] = out[column].fillna("").astype(str).str.strip()
    if out[KEY].eq("").any():
        raise ValueError("LLAVE-VACIA")
    if out[KEY].duplicated().any():
        raise ValueError("LLAVE-NO-UNICA")
    out["_age"] = pd.to_numeric(out[AGE], errors="coerce")
    out["_weight"] = pd.to_numeric(out[WEIGHT], errors="coerce")
    out["_weight_ok"] = np.isfinite(out["_weight"]) & out["_weight"].gt(0)
    out["_design_ok"] = out[STRATUM].ne("") & out[PSU].ne("")
    out["_status_ok"] = out[STATUS].isin(CATEGORIES)
    out["_sex_ok"] = out[SEX].isin(("1", "2"))
    out["_age_slot"] = 5
    for slot, (_, low, high) in enumerate(AGES):
        out.loc[out["_age"].between(low, high, inclusive="both"), "_age_slot"] = slot
    out["_sex_slot"] = np.where(out[SEX].eq("1"), 0, np.where(out[SEX].eq("2"), 1, 2))
    status_number = pd.to_numeric(out[STATUS], errors="coerce")
    out["_status_slot"] = np.where(out["_status_ok"], status_number - 1, 7).astype(int)
    out["_cell"] = ((out["_sex_slot"] * 6 + out["_age_slot"]) * 8 + out["_status_slot"]).astype(int)
    return out


def _age_mask(data: pd.DataFrame, age_id: str) -> pd.Series:
    if age_id == "15_mas":
        return data["_age_slot"].between(0, 4)
    slot = next(i for i, item in enumerate(AGES) if item[0] == age_id)
    return data["_age_slot"].eq(slot)


def _sex_mask(data: pd.DataFrame, code: str | None) -> pd.Series:
    return ~data["_sex_ok"] if code is None else data[SEX].eq(code)


def _cell_id(sex_slot: int, age_slot: int, status_slot: int) -> int:
    return (sex_slot * 6 + age_slot) * 8 + status_slot


class ReplicateEngine:
    def __init__(self, data: pd.DataFrame, replicates: int, seed: int):
        design = data.loc[data["_weight_ok"] & data["_design_ok"],
                          [STRATUM, PSU, "_cell", "_weight"]].copy()
        psus = design[[STRATUM, PSU]].drop_duplicates().sort_values([STRATUM, PSU]).reset_index(drop=True)
        psus["_psu_index"] = np.arange(len(psus))
        design = design.merge(psus, on=[STRATUM, PSU], how="left", validate="many_to_one")
        grouped = design.groupby(["_psu_index", "_cell"], sort=False)["_weight"].sum().reset_index()
        matrix = np.zeros((len(psus), NCELLS), dtype=float)
        np.add.at(matrix, (grouped["_psu_index"].to_numpy(int), grouped["_cell"].to_numpy(int)),
                  grouped["_weight"].to_numpy(float))
        multipliers = np.ones((replicates, len(psus)), dtype=float)
        rng = np.random.default_rng(seed)
        self.singleton = 0
        self.non_singleton = 0
        self.df = 0
        for _, group in psus.groupby(STRATUM, sort=True):
            indices = group["_psu_index"].to_numpy(int)
            m = len(indices)
            if m == 1:
                self.singleton += 1
                continue
            counts = rng.multinomial(m - 1, np.full(m, 1 / m), size=replicates)
            multipliers[:, indices] = counts * (m / (m - 1))
            self.non_singleton += 1
            self.df += m - 1
        if self.non_singleton == 0 or self.df == 0:
            raise ValueError("DISENO-SIN-ESTRATOS-NO-SINGLETON")
        self.adjustment = (self.non_singleton + self.singleton) / self.non_singleton
        self.point_cells = np.bincount(
            data.loc[data["_weight_ok"], "_cell"].to_numpy(int),
            weights=data.loc[data["_weight_ok"], "_weight"].to_numpy(float),
            minlength=NCELLS,
        )
        self.rep_cells = multipliers @ matrix
        self.strata = self.non_singleton + self.singleton
        self.psus = len(psus)
        self.replicates = replicates
        self.seed = seed

    @staticmethod
    def indices(sex_slots, age_slots, status_slots) -> list[int]:
        return [_cell_id(s, a, c) for s in sex_slots for a in age_slots for c in status_slots]

    def mass(self, sex_slots, age_slots, status_slots) -> tuple[float, np.ndarray]:
        idx = self.indices(sex_slots, age_slots, status_slots)
        return float(self.point_cells[idx].sum()), self.rep_cells[:, idx].sum(axis=1)


def _ratio(numerator: float, denominator: float, num_rep: np.ndarray,
           den_rep: np.ndarray) -> tuple[float | None, np.ndarray | None, str]:
    if denominator <= 0:
        return None, None, "NO-ESTIMABLE:DENOMINADOR-NULO"
    if np.any(den_rep <= 0):
        return numerator / denominator, None, "NO-DISPONIBLE:REPLICA-DEGENERADA"
    return numerator / denominator, num_rep / den_rep, "ESTIMABLE"


def _precision(point: float | None, reps: np.ndarray | None, engine: ReplicateEngine,
               proportion: bool) -> dict:
    if point is None:
        return {"ee": None, "ic95_lo": None, "ic95_hi": None,
                "gl": engine.df, "precision_estado": "NO-ESTIMABLE:DENOMINADOR-NULO"}
    if reps is None or not np.isfinite(reps).all():
        return {"ee": None, "ic95_lo": None, "ic95_hi": None,
                "gl": engine.df, "precision_estado": "NO-DISPONIBLE:REPLICA-DEGENERADA"}
    ee = float(np.std(reps, ddof=1) * math.sqrt(engine.adjustment))
    critical = float(student_t.ppf(0.975, engine.df))
    if proportion:
        if not 0 < point < 1:
            return {"ee": ee, "ic95_lo": None, "ic95_hi": None,
                    "gl": engine.df, "precision_estado": "NO-DISPONIBLE:FRONTERA-LOGIT"}
        logit = math.log(point / (1 - point))
        se_logit = ee / (point * (1 - point))
        inverse = lambda value: 1 / (1 + math.exp(-value))
        lo, hi = inverse(logit - critical * se_logit), inverse(logit + critical * se_logit)
        state = "DISPONIBLE:RAO-WU-COMPARTIDO-LOGIT-T95"
    else:
        lo, hi = point - critical * ee, point + critical * ee
        state = "DISPONIBLE:RAO-WU-COMPARTIDO-T95"
    if engine.singleton:
        state += f":SINGLETON-APORTE-PROMEDIO={engine.singleton}"
    return {"ee": ee, "ic95_lo": lo, "ic95_hi": hi,
            "gl": engine.df, "precision_estado": state}


def _counts(data: pd.DataFrame, mask: pd.Series) -> tuple[int, float]:
    eligible = mask & data["_weight_ok"]
    return int(eligible.sum()), float(data.loc[eligible, "_weight"].sum())


def _ratio_row(data, engine, sex_label, sex_code, sex_slot, age_id,
               denominator_statuses, numerator_status="1") -> dict:
    age_slots = list(range(5)) if age_id == "15_mas" else [next(i for i, x in enumerate(AGES) if x[0] == age_id)]
    statuses = [int(code) - 1 for code in denominator_statuses]
    denominator, den_rep = engine.mass([sex_slot], age_slots, statuses)
    numerator, num_rep = engine.mass([sex_slot], age_slots, [int(numerator_status) - 1])
    point, reps, _ = _ratio(numerator, denominator, num_rep, den_rep)
    exposed = _sex_mask(data, sex_code) & _age_mask(data, age_id)
    valid = exposed & data["_status_ok"]
    denominator_mask = exposed & data[STATUS].isin(denominator_statuses)
    unknown = exposed & ~data["_status_ok"]
    outside = valid & ~data[STATUS].isin(denominator_statuses)
    n_exp, m_exp = _counts(data, exposed)
    n_valid, m_valid = _counts(data, valid)
    n_unknown, m_unknown = _counts(data, unknown)
    n_out, m_out = _counts(data, outside)
    n_den, _ = _counts(data, denominator_mask)
    n_num, _ = _counts(data, denominator_mask & data[STATUS].eq(numerator_status))
    row = {
        "sexo": sex_label, "edad": age_id, "n_expuesto": n_exp,
        "masa_expuesto": m_exp, "n_status_valido": n_valid,
        "masa_status_valido": m_valid, "n_desconocido": n_unknown,
        "masa_desconocido": m_unknown, "n_fuera_denominador": n_out,
        "masa_fuera_denominador": m_out, "n_denominador": n_den,
        "masa_denominador": denominator, "n_numerador": n_num,
        "masa_numerador": numerator, "punto": point, "_reps": reps,
    }
    row.update(_precision(point, reps, engine, True))
    return row


def calculate(frame: pd.DataFrame, replicates: int = REPLICATES, seed: int = SEED) -> dict:
    data = prepare(frame)
    engine = ReplicateEngine(data, replicates, seed)
    age_ids = [item[0] for item in AGES] + ["15_mas"]

    distribution = []
    for sex_label, sex_code, sex_slot in SEXES:
        for age_id in age_ids:
            base = _ratio_row(data, engine, sex_label, sex_code, sex_slot, age_id, tuple(CATEGORIES))
            for code, category in CATEGORIES.items():
                age_slots = list(range(5)) if age_id == "15_mas" else [next(i for i, x in enumerate(AGES) if x[0] == age_id)]
                numerator, num_rep = engine.mass([sex_slot], age_slots, [int(code) - 1])
                point, reps, _ = _ratio(numerator, base["masa_denominador"], num_rep,
                                         engine.mass([sex_slot], age_slots, list(range(7)))[1])
                row = {key: value for key, value in base.items() if key != "_reps"}
                row.update({"categoria": category, "n_numerador": int((
                    _sex_mask(data, sex_code) & _age_mask(data, age_id) &
                    data[STATUS].eq(code) & data["_weight_ok"]).sum()),
                    "masa_numerador": numerator, "punto": point})
                row.update(_precision(point, reps, engine, True))
                distribution.append(row)

    union = []
    union_reps = {}
    for sex_label, sex_code, sex_slot in SEXES[:2]:
        for age_id in age_ids:
            row = _ratio_row(data, engine, sex_label, sex_code, sex_slot, age_id, ("1", "6"))
            union_reps[(sex_label, age_id)] = row.pop("_reps")
            row.update({"tipo": "tasa", "definicion": "P3_27=1 / P3_27 en {1,6}"})
            union.append(row)
    for age_id in age_ids:
        women = next(r for r in union if r["tipo"] == "tasa" and r["sexo"] == "mujer" and r["edad"] == age_id)
        men = next(r for r in union if r["tipo"] == "tasa" and r["sexo"] == "hombre" and r["edad"] == age_id)
        point = None if women["punto"] is None or men["punto"] is None else women["punto"] - men["punto"]
        wr, mr = union_reps[("mujer", age_id)], union_reps[("hombre", age_id)]
        reps_diff = None if wr is None or mr is None else wr - mr
        row = {key: None for key in women}
        row.update({"tipo": "diferencia_mujer_menos_hombre", "sexo": "mujer-hombre",
                    "edad": age_id, "punto": point,
                    "definicion": "tasa mujer menos tasa hombre; covarianza compartida"})
        row.update(_precision(point, reps_diff, engine, False))
        union.append(row)

    # P3: estándar común y tasas recalculadas dentro de cada réplica.
    standard = []
    age_point, age_rep, rate_point, rate_rep = {}, {}, {}, {}
    all_den, all_den_rep = engine.mass([0, 1], list(range(5)), [0, 5])
    all_n, _ = _counts(
        data,
        data["_sex_ok"] & data["_age_slot"].between(0, 4)
        & data[STATUS].isin(("1", "6")),
    )
    for age_slot, (age_id, _, _) in enumerate(AGES):
        den, den_rep = engine.mass([0, 1], [age_slot], [0, 5])
        point, reps, _ = _ratio(den, all_den, den_rep, all_den_rep)
        age_point[age_id], age_rep[age_id] = point, reps
        n, _ = _counts(data, data["_sex_ok"] & data["_age_slot"].eq(age_slot) & data[STATUS].isin(("1", "6")))
        row = {"tipo": "peso_estandar_edad", "sexo": "ambos", "edad": age_id,
               "n_denominador": all_n, "masa_denominador": all_den,
               "n_numerador": n, "masa_numerador": den, "punto": point,
               "definicion": "masa conjunta del tramo / masa conjunta de cinco tramos"}
        row.update(_precision(point, reps, engine, True))
        standard.append(row)
        for sex_label, _, sex_slot in SEXES[:2]:
            denom, denom_rep = engine.mass([sex_slot], [age_slot], [0, 5])
            numer, numer_rep = engine.mass([sex_slot], [age_slot], [0])
            rate, reps_rate, _ = _ratio(numer, denom, numer_rep, denom_rep)
            rate_point[(sex_label, age_id)] = rate
            rate_rep[(sex_label, age_id)] = reps_rate
            nden, _ = _counts(data, data[SEX].eq("1" if sex_label == "hombre" else "2") &
                              data["_age_slot"].eq(age_slot) & data[STATUS].isin(("1", "6")))
            r = {"tipo": "tasa_sexo_edad", "sexo": sex_label, "edad": age_id,
                 "n_denominador": nden, "masa_denominador": denom,
                 "masa_numerador": numer, "punto": rate,
                 "definicion": "P3_27=1 / P3_27 en {1,6}, tramo y sexo"}
            r.update(_precision(rate, reps_rate, engine, True))
            standard.append(r)

    standardized = {}
    standardized_rep = {}
    for sex_label, _, _ in SEXES[:2]:
        missing = [age for age, _, _ in AGES if age_point[age] and rate_point[(sex_label, age)] is None]
        if missing:
            point, reps = None, None
        else:
            point = sum(age_point[age] * rate_point[(sex_label, age)] for age, _, _ in AGES)
            if any(age_rep[age] is None or rate_rep[(sex_label, age)] is None for age, _, _ in AGES):
                reps = None
            else:
                reps = sum(age_rep[age] * rate_rep[(sex_label, age)] for age, _, _ in AGES)
        standardized[sex_label], standardized_rep[sex_label] = point, reps
        row = {"tipo": "tasa_estandarizada", "sexo": sex_label, "edad": "estandar_cinco_tramos",
               "n_denominador": int((data["_sex_ok"] & data[STATUS].isin(("1", "6")) &
                                      data["_age_slot"].between(0, 4) &
                                      data[SEX].eq("1" if sex_label == "hombre" else "2")).sum()),
               "masa_denominador": None, "masa_numerador": None, "punto": point,
               "definicion": "suma de peso estándar común por tasa sexo×edad; sin redistribución"}
        row.update(_precision(point, reps, engine, True))
        standard.append(row)

    std_diff = None if any(standardized[s] is None for s in ("mujer", "hombre")) else standardized["mujer"] - standardized["hombre"]
    std_diff_rep = None if any(standardized_rep[s] is None for s in ("mujer", "hombre")) else standardized_rep["mujer"] - standardized_rep["hombre"]
    gross_rows = {s: next(r for r in union if r["tipo"] == "tasa" and r["sexo"] == s and r["edad"] == "15_mas") for s in ("hombre", "mujer")}
    gross_diff = gross_rows["mujer"]["punto"] - gross_rows["hombre"]["punto"]
    gross_diff_rep = union_reps[("mujer", "15_mas")] - union_reps[("hombre", "15_mas")]
    for kind, point, reps, definition in (
        ("diferencia_bruta", gross_diff, gross_diff_rep, "mujer-hombre sin fijar composición de edad"),
        ("diferencia_estandarizada", std_diff, std_diff_rep, "mujer-hombre con estándar común estimado"),
        ("bruta_menos_estandarizada", None if std_diff is None else gross_diff - std_diff,
         None if std_diff_rep is None else gross_diff_rep - std_diff_rep,
         "diferencia bruta menos estandarizada; descomposición descriptiva, no causal"),
    ):
        row = {"tipo": kind, "sexo": "mujer-hombre", "edad": "15_mas",
               "n_denominador": None, "masa_denominador": all_den,
               "masa_numerador": None, "punto": point, "definicion": definition}
        row.update(_precision(point, reps, engine, False))
        standard.append(row)

    weight_ok = data["_weight_ok"]
    flow_masks = [
        ("filas_tsdem", pd.Series(True, index=data.index)),
        ("peso_valido", weight_ok),
        ("edad_15_mas_valida", weight_ok & data["_age_slot"].between(0, 4)),
        ("sexo_conocido", weight_ok & data["_age_slot"].between(0, 4) & data["_sex_ok"]),
        ("p3_27_valida", weight_ok & data["_age_slot"].between(0, 4) & data["_sex_ok"] & data["_status_ok"]),
        ("union_actual_1_o_6", weight_ok & data["_age_slot"].between(0, 4) & data["_sex_ok"] & data[STATUS].isin(("1", "6"))),
    ]
    flow = [{"paso": name, "n": int(mask.sum()),
             "masa": float(data.loc[mask & weight_ok, "_weight"].sum())} for name, mask in flow_masks]
    audit = {
        "n_filas": len(data), "llave_unica": True,
        "peso_invalido_n": int((~weight_ok).sum()),
        "edad_999_o_no_valida_n": int((weight_ok & data["_age_slot"].eq(5)).sum()),
        "sexo_desconocido_15_mas_n": int((weight_ok & data["_age_slot"].between(0, 4) & ~data["_sex_ok"]).sum()),
        "status_desconocido_15_mas_n": int((weight_ok & data["_age_slot"].between(0, 4) & ~data["_status_ok"]).sum()),
        "diseno_faltante_15_mas_n": int((weight_ok & data["_age_slot"].between(0, 4) & ~data["_design_ok"]).sum()),
        "estratos": engine.strata, "upm_anidadas": engine.psus,
        "estratos_singleton": engine.singleton, "gl": engine.df,
        "replicas": engine.replicates, "semilla": engine.seed,
        "singleton_ajuste_covarianza": engine.adjustment,
        "fpc": "NO-APLICADA:NO-ACREDITADA",
        "reconstruccion_padre_por_masas": "SE-EVALUA-EN-CONTROL-POST-EJECUCION",
    }
    return {"distribucion": distribution, "union": union,
            "estandarizacion": standard, "flujo": flow, "auditoria": audit}


def _fmt(value):
    if value is None:
        return ""
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.12f}"
    return value


def _serialize(rows: list[dict], columns: list[str]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows({key: _fmt(row.get(key)) for key in columns} for row in rows)
    return output.getvalue().encode("utf-8")


DIST_COLUMNS = ["sexo", "edad", "categoria", "n_expuesto", "masa_expuesto",
                "n_status_valido", "masa_status_valido", "n_desconocido",
                "masa_desconocido", "n_fuera_denominador", "masa_fuera_denominador",
                "n_denominador", "masa_denominador", "n_numerador", "masa_numerador",
                "punto", "ee", "ic95_lo", "ic95_hi", "gl", "precision_estado"]
UNION_COLUMNS = ["tipo", "sexo", "edad"] + DIST_COLUMNS[3:] + ["definicion"]
STD_COLUMNS = ["tipo", "sexo", "edad", "n_denominador", "masa_denominador",
               "masa_numerador", "punto", "ee", "ic95_lo", "ic95_hi", "gl",
               "precision_estado", "definicion"]


def medir(inputs: dict, contrato: dict) -> dict:
    raw = {key: _raw(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        actual = _sha(raw[key])
        if actual != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{actual}")
    if not raw[INPUT_FD].startswith(b"PK") or not raw[INPUT_QUESTIONNAIRE].startswith(b"%PDF"):
        raise ValueError("DOCUMENTACION-INVALIDA")
    result = calculate(read_frame(raw[INPUT_DATA]))
    outputs = {
        "distribucion.csv": _serialize(result["distribucion"], DIST_COLUMNS),
        "union_condicional.csv": _serialize(result["union"], UNION_COLUMNS),
        "estandarizacion.csv": _serialize(result["estandarizacion"], STD_COLUMNS),
        "flujo.csv": _serialize(result["flujo"], ["paso", "n", "masa"]),
        "auditoria.json": (json.dumps(result["auditoria"], ensure_ascii=False,
                                       indent=2, sort_keys=True) + "\n").encode(),
    }
    repo = Path(__file__).resolve().parents[3]
    destination = repo / "forense/analisis/enadid2023-union-sexo-edad-cli-2"
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (destination / name).write_bytes(content)
    std = {row["tipo"]: row for row in result["estandarizacion"]
           if row["tipo"] in {"diferencia_bruta", "diferencia_estandarizada", "bruta_menos_estandarizada"}}
    return {
        "RESULT-ENADID-USE3-P1-TABLA-SHA256": _sha(outputs["distribucion.csv"]),
        "RESULT-ENADID-USE3-P2-TABLA-SHA256": _sha(outputs["union_condicional.csv"]),
        "RESULT-ENADID-USE3-P3-TABLA-SHA256": _sha(outputs["estandarizacion.csv"]),
        "RESULT-ENADID-USE3-FLUJO-SHA256": _sha(outputs["flujo.csv"]),
        "RESULT-ENADID-USE3-AUDITORIA-SHA256": _sha(outputs["auditoria.json"]),
        "RESULT-ENADID-USE3-DIF-BRUTA-MH": std["diferencia_bruta"]["punto"],
        "RESULT-ENADID-USE3-DIF-ESTANDAR-MH": std["diferencia_estandarizada"]["punto"],
        "RESULT-ENADID-USE3-BRUTA-MENOS-ESTANDAR": std["bruta_menos_estandarizada"]["punto"],
        "RESULT-ENADID-USE3-REPLICAS": REPLICATES,
        "RESULT-ENADID-USE3-SEMILLA": SEED,
        "RESULT-ENADID-USE3-SALIDA": "forense/analisis/enadid2023-union-sexo-edad-cli-2",
    }
