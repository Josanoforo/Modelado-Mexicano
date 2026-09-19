#!/usr/bin/env python3
"""ENADID 2023: situacion conyugal actual, total y por edad.

La unidad es la persona residente en TSDEM. Los dominios se linealizan sobre
la muestra completa; filtrar una edad antes de construir la varianza seria un
estimador distinto. No se usa P3_27_AG ni se interpreta situacion actual como
tipo de primera union.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import pandas as pd
from scipy.stats import t as student_t


CALC_ID = "CALC-ENADID-0001"
INPUT_DATA = "enadid2023_base_datos_csv"
INPUT_FD = "enadid2023_fd_xlsx"
INPUT_QUESTIONNAIRE = "enadid2023_hogar_cuestionario_pdf"
EXPECTED_SHA256 = {
    INPUT_DATA: "995d448ab298251d441e437fc4a368f84879a8b74fa7bc103dc189434cbfaa18",
    INPUT_FD: "d56582b7ace04e2c13a1b9ea22aeea458d7b9cc02a21241e5fda29fe12b4f34c",
    INPUT_QUESTIONNAIRE: "8b046a68dc19e292522557e05d81952e8fb04c2d3a1375c93fa7192e857e3270",
}
MEMBER = "TSDEM.csv"
KEY = "LLAVE_PER"
AGE = "EDAD"
STATUS = "P3_27"
WEIGHT = "FAC_VIV"
STRATUM = "EST_DIS"
PSU = "UPM_DIS"
REQUIRED = {KEY, AGE, STATUS, WEIGHT, STRATUM, PSU}

CATEGORIES = {
    "1": "union_libre",
    "2": "separada_union_libre",
    "3": "separada_matrimonio",
    "4": "divorciada",
    "5": "viuda",
    "6": "casada",
    "7": "soltera",
}
AGES = (
    ("15_17", 15, 17),
    ("18_29", 18, 29),
    ("30_44", 30, 44),
    ("45_59", 45, 59),
    ("60_mas", 60, 120),
    ("15_mas", 15, 120),
)
OUTPUT_COLUMNS = [
    "estimando", "categoria", "edad", "n_expuesto", "n_valido",
    "n_desconocido", "masa_desconocido", "n_numerador",
    "masa_numerador", "masa_denominador", "punto", "ee", "ic95_lo",
    "ic95_hi", "gl", "precision_estado",
]


def _raw(entry: dict) -> bytes:
    value = entry.get("bytes")
    return value if value is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_frame(raw_zip: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
        if zf.testzip() is not None:
            raise ValueError("ZIP-CORRUPTO")
        names = [item.filename for item in zf.infolist() if not item.is_dir()]
        if MEMBER not in names:
            raise ValueError(f"MIEMBRO-AUSENTE:{MEMBER}")
        frame = pd.read_csv(
            zf.open(MEMBER), dtype=str, encoding="utf-8-sig",
            low_memory=False, usecols=lambda name: name.upper() in REQUIRED,
        )
    frame.columns = [name.upper() for name in frame.columns]
    return frame


def validate(frame: pd.DataFrame) -> None:
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        raise ValueError(f"COLUMNAS-AUSENTES:{','.join(missing)}")
    if frame[KEY].isna().any() or frame[KEY].astype(str).str.strip().eq("").any():
        raise ValueError("LLAVE-VACIA")
    if frame[KEY].duplicated().any():
        raise ValueError("LLAVE-NO-UNICA")


def prepare(frame: pd.DataFrame) -> pd.DataFrame:
    validate(frame)
    out = frame.copy()
    for column in (KEY, STATUS, STRATUM, PSU):
        out[column] = out[column].fillna("").astype(str).str.strip()
    out["_age"] = pd.to_numeric(out[AGE], errors="coerce")
    out["_weight"] = pd.to_numeric(out[WEIGHT], errors="coerce")
    out["_weight_ok"] = out["_weight"].map(lambda x: bool(math.isfinite(x) and x > 0) if pd.notna(x) else False)
    out["_design_ok"] = out[STRATUM].ne("") & out[PSU].ne("")
    out["_status_ok"] = out[STATUS].isin(CATEGORIES)
    out["_age_known"] = out["_age"].between(0, 120, inclusive="both")
    return out


def _age_mask(frame: pd.DataFrame, low: int, high: int) -> pd.Series:
    return frame["_age"].between(low, high, inclusive="both")


def _precision(
    frame: pd.DataFrame, denominator_mask: pd.Series,
    numerator_mask: pd.Series, point: float, denominator: float,
) -> tuple[float | None, float | None, float | None, int, str]:
    base = frame[frame["_weight_ok"] & frame["_design_ok"]].copy()
    if int((denominator_mask & frame["_weight_ok"] & ~frame["_design_ok"]).sum()):
        return None, None, None, 0, "NO-DISPONIBLE:DISENO-FALTANTE-EN-DOMINIO"
    x = denominator_mask.reindex(base.index).fillna(False).astype(float)
    y = numerator_mask.reindex(base.index).fillna(False).astype(float)
    influence = base["_weight"] * (y - point * x) / denominator
    psu = (
        pd.DataFrame({"stratum": base[STRATUM], "psu": base[PSU], "z": influence})
        .groupby(["stratum", "psu"], sort=True, as_index=False)["z"].sum()
    )
    variance_terms = []
    df = 0
    singletons = 0
    for _, group in psu.groupby("stratum", sort=True):
        values = group["z"].astype(float).tolist()
        m = len(values)
        if m == 1:
            singletons += 1
            continue
        mean = math.fsum(values) / m
        variance_terms.append(m / (m - 1) * math.fsum((v - mean) ** 2 for v in values))
        df += m - 1
    if df <= 0 or not variance_terms:
        return None, None, None, df, "NO-DISPONIBLE:SIN-GL-DE-DISENO"
    ee = math.sqrt(max(0.0, math.fsum(variance_terms)))
    if not (0 < point < 1):
        return ee, None, None, df, "NO-DISPONIBLE:PROPORCION-FRONTERA"
    critical = float(student_t.ppf(0.975, df))
    logit = math.log(point / (1 - point))
    se_logit = ee / (point * (1 - point))
    inv = lambda value: 1 / (1 + math.exp(-value))
    state = "DISPONIBLE:TAYLOR-RATIO-LOGIT-T95"
    if singletons:
        state += f":SINGLETON-SIN-APORTE={singletons}"
    return ee, inv(logit - critical * se_logit), inv(logit + critical * se_logit), df, state


def _row(
    frame: pd.DataFrame, estimand: str, category: str, age_id: str,
    exposed: pd.Series, valid: pd.Series, numerator: pd.Series,
) -> dict:
    weight_ok = frame["_weight_ok"]
    denominator_mask = exposed & valid & weight_ok
    numerator_mask = denominator_mask & numerator
    unknown = exposed & ~valid & weight_ok
    denominator = float(frame.loc[denominator_mask, "_weight"].sum())
    numerator_mass = float(frame.loc[numerator_mask, "_weight"].sum())
    point = numerator_mass / denominator if denominator > 0 else None
    if point is None:
        ee = lo = hi = None
        df, state = 0, "NO-DISPONIBLE:DENOMINADOR-NULO"
    else:
        ee, lo, hi, df, state = _precision(frame, denominator_mask, numerator_mask, point, denominator)
    return {
        "estimando": estimand, "categoria": category, "edad": age_id,
        "n_expuesto": int(exposed.sum()), "n_valido": int(denominator_mask.sum()),
        "n_desconocido": int(unknown.sum()),
        "masa_desconocido": float(frame.loc[unknown, "_weight"].sum()),
        "n_numerador": int(numerator_mask.sum()), "masa_numerador": numerator_mass,
        "masa_denominador": denominator, "punto": point, "ee": ee,
        "ic95_lo": lo, "ic95_hi": hi, "gl": df, "precision_estado": state,
    }


def calculate(frame: pd.DataFrame) -> tuple[list[dict], dict]:
    data = prepare(frame)
    rows = []
    for age_id, low, high in AGES:
        exposed = _age_mask(data, low, high)
        valid_status = data["_status_ok"]
        for code, label in CATEGORIES.items():
            rows.append(_row(data, "distribucion_actual_15_mas", label, age_id,
                             exposed, valid_status, data[STATUS].eq(code)))
        pair = data[STATUS].isin(("1", "6"))
        rows.append(_row(data, "union_libre_entre_union_o_casada", "union_libre", age_id,
                         exposed, pair, data[STATUS].eq("1")))
        rows.append(_row(data, "union_libre_entre_union_o_casada", "actualmente_casada", age_id,
                         exposed, pair, data[STATUS].eq("6")))

    valid_weight = data["_weight_ok"]
    age_unknown = ~data["_age_known"] & valid_weight
    status_unknown_15 = _age_mask(data, 15, 120) & ~data["_status_ok"] & valid_weight
    audit = {
        "n_filas": int(len(data)), "llave_unica": True, "perdida_enlace_n": 0,
        "peso_invalido_n": int((~valid_weight).sum()),
        "edad_no_especificada_n": int(age_unknown.sum()),
        "edad_no_especificada_masa": float(data.loc[age_unknown, "_weight"].sum()),
        "situacion_no_especificada_15_mas_n": int(status_unknown_15.sum()),
        "situacion_no_especificada_15_mas_masa": float(data.loc[status_unknown_15, "_weight"].sum()),
        "diseno_faltante_15_mas_n": int((_age_mask(data, 15, 120) & valid_weight & ~data["_design_ok"]).sum()),
        "estratos": int(data.loc[valid_weight & data["_design_ok"], STRATUM].nunique()),
        "upm_anidadas": int(data.loc[valid_weight & data["_design_ok"], [STRATUM, PSU]].drop_duplicates().shape[0]),
        "upm_cruza_estratos": int((data.loc[valid_weight & data["_design_ok"]].groupby(PSU)[STRATUM].nunique() > 1).sum()),
        "fpc": "NO-APLICADA:NO-ACREDITADA",
    }
    return rows, audit


def _fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12f}"
    return value


def serialize(rows: list[dict]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: _fmt(row[key]) for key in OUTPUT_COLUMNS} for row in rows)
    return output.getvalue().encode("utf-8")


def medir(inputs: dict, contrato: dict) -> dict:
    raw = {key: _raw(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        actual = _sha(raw[key])
        if actual != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{actual}")
    if not raw[INPUT_FD].startswith(b"PK") or not raw[INPUT_QUESTIONNAIRE].startswith(b"%PDF"):
        raise ValueError("DOCUMENTACION-INVALIDA")
    rows, audit = calculate(read_frame(raw[INPUT_DATA]))
    table = serialize(rows)
    repo = Path(__file__).resolve().parents[3]
    destination = repo / "forense/analisis/enadid-union-actual-cli-1"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "resultados.csv").write_bytes(table)
    (destination / "auditoria.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    index = {(r["estimando"], r["categoria"], r["edad"]): r for r in rows}
    gross = index[("distribucion_actual_15_mas", "union_libre", "15_mas")]
    conditional = index[("union_libre_entre_union_o_casada", "union_libre", "15_mas")]
    return {
        "RESULT-ENADID-UA-G-P-BRUTA": gross["punto"],
        "RESULT-ENADID-UA-G-P-CONDICIONAL": conditional["punto"],
        "RESULT-ENADID-UA-G-P-CASADA-CONDICIONAL": 1.0 - conditional["punto"],
        "RESULT-ENADID-UA-G-N-VALIDO-BRUTA": gross["n_valido"],
        "RESULT-ENADID-UA-G-N-VALIDO-CONDICIONAL": conditional["n_valido"],
        "RESULT-ENADID-UA-G-TABLA-SHA256": _sha(table),
        "RESULT-ENADID-UA-G-LLAVE-UNICA": "SI",
        "RESULT-ENADID-UA-G-PERDIDA-ENLACE-N": audit["perdida_enlace_n"],
        "RESULT-ENADID-UA-G-PESO-INVALIDO-N": audit["peso_invalido_n"],
        "RESULT-ENADID-UA-G-EDAD-NE-N": audit["edad_no_especificada_n"],
        "RESULT-ENADID-UA-G-SITUACION-NE-N": audit["situacion_no_especificada_15_mas_n"],
        "RESULT-ENADID-UA-G-FPC": audit["fpc"],
        "RESULT-ENADID-UA-G-SALIDA": "forense/analisis/enadid-union-actual-cli-1/resultados.csv",
    }
