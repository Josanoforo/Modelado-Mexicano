"""Medidor congelado: atraso y afrontamiento ENSAFI 2023 con diseño.

Calcula trece proporciones descriptivas. La varianza usa linealización de
razón por UPM anidada en estrato sobre la muestra completa; las filas fuera
del dominio aportan cero, no se eliminan antes de construir la varianza.
"""
from __future__ import annotations

import csv
import io
import math
import zipfile
from collections import defaultdict

from scipy.stats import t as student_t


INPUT_ID = "ensafi2023_bd_csv_zip"
PFX = "RESULT-ENSAFI-DIS-"
VALID = {"1", "2"}
DEBT_LEVELS = {"1", "2", "3", "4"}

ESTIMANDS = [
    {
        "code": "HOG-FORMAL",
        "table": "THOGAR.csv",
        "weight": "FAC_HOG",
        "exposure": "P4_7_1",
        "response": "P4_8_1",
    },
    {
        "code": "HOG-CAJA-FAMILIA",
        "table": "THOGAR.csv",
        "weight": "FAC_HOG",
        "exposure": "P4_7_2",
        "response": "P4_8_2",
    },
    {
        "code": "HOG-EMPENO",
        "table": "THOGAR.csv",
        "weight": "FAC_HOG",
        "exposure": "P4_7_3",
        "response": "P4_8_3",
    },
    {
        "code": "HOG-PRESTAMISTA",
        "table": "THOGAR.csv",
        "weight": "FAC_HOG",
        "exposure": "P4_7_4",
        "response": "P4_8_4",
    },
    {
        "code": "PER-ATRASO",
        "table": "TMODULO.csv",
        "weight": "FAC_ELE",
        "exposure": "P6_8",
        "response": "P6_7",
        "exposure_values": DEBT_LEVELS,
    },
] + [
    {
        "code": f"PER-AFR-{i}",
        "table": "TMODULO.csv",
        "weight": "FAC_ELE",
        "exposure": "P6_9",
        "exposure_values": {"2"},
        "response": f"P6_10_{i}",
    }
    for i in range(1, 9)
]

# Puntos publicados por #723; son contraste de identidad/codificación, no
# objetivos de calibración. El cálculo de incertidumbre no aparece aquí.
EXPECTED_723 = {
    "HOG-FORMAL": 0.278268362703,
    "HOG-CAJA-FAMILIA": 0.300837713027,
    "HOG-EMPENO": 0.276593308520,
    "HOG-PRESTAMISTA": 0.328203722622,
    "PER-ATRASO": 0.272627402059,
    "PER-AFR-1": 0.415862666480,
    "PER-AFR-2": 0.319620126195,
    "PER-AFR-3": 0.683069699797,
    "PER-AFR-4": 0.097363421894,
    "PER-AFR-5": 0.104045372303,
    "PER-AFR-6": 0.102792917547,
    "PER-AFR-7": 0.100740949123,
    "PER-AFR-8": 0.021154112843,
}


def _code(value):
    return "" if value is None else str(value).strip()


def _weight(value):
    try:
        out = float(_code(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) and out > 0 else None


def _read_tables(path):
    out = {}
    with zipfile.ZipFile(path) as zf:
        if zf.testzip() is not None:
            raise ValueError("ZIP-ENSAFI-CORRUPTO")
        for table in ("THOGAR.csv", "TMODULO.csv"):
            matches = [name for name in zf.namelist() if name.rsplit("/", 1)[-1] == table]
            if len(matches) != 1:
                raise ValueError(f"MIEMBRO-NO-UNIVOCO:{table}:{matches}")
            raw = zf.read(matches[0])
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("latin-1")
            reader = csv.DictReader(io.StringIO(text, newline=""))
            if reader.fieldnames is None:
                raise ValueError(f"SIN-CABECERA:{table}")
            out[table] = list(reader), len(reader.fieldnames)
    return out


def _is_exposed(row, cfg):
    allowed = cfg.get("exposure_values", {"1"})
    return _code(row.get(cfg["exposure"])) in allowed


def _design_profile(rows, weight_col):
    strata = defaultdict(set)
    upm_strata = defaultdict(set)
    invalid_weights = 0
    missing_design = 0
    for row in rows:
        weight = _weight(row.get(weight_col))
        if weight is None:
            invalid_weights += 1
            continue
        h, u = _code(row.get("EST_DIS")), _code(row.get("UPM_DIS"))
        if not h or not u:
            missing_design += 1
            continue
        strata[h].add(u)
        upm_strata[u].add(h)
    singletons = sum(len(psus) == 1 for psus in strata.values())
    df = sum(max(0, len(psus) - 1) for psus in strata.values())
    return {
        "n_strata": len(strata),
        "n_psu_nested": sum(len(psus) for psus in strata.values()),
        "n_psu_cross_strata": sum(len(hs) > 1 for hs in upm_strata.values()),
        "n_singleton": singletons,
        "df": df,
        "invalid_weights": invalid_weights,
        "missing_design": missing_design,
    }


def _estimate(rows, cfg):
    exposed = [row for row in rows if _is_exposed(row, cfg)]
    valid = [row for row in exposed if _code(row.get(cfg["response"])) in VALID]
    unknown = [row for row in exposed if _code(row.get(cfg["response"])) not in VALID]
    weighted_valid = [(row, _weight(row.get(cfg["weight"]))) for row in valid]
    invalid_weight = sum(weight is None for _, weight in weighted_valid)
    weighted_valid = [(row, weight) for row, weight in weighted_valid if weight is not None]
    denominator = sum(weight for _, weight in weighted_valid)
    numerator_rows = [(row, weight) for row, weight in weighted_valid
                      if _code(row.get(cfg["response"])) == "1"]
    numerator = sum(weight for _, weight in numerator_rows)
    unknown_mass = sum(weight for row in unknown
                       if (weight := _weight(row.get(cfg["weight"]))) is not None)
    base = {
        "n_exposed": len(exposed),
        "n_valid": len(valid),
        "n_unknown": len(unknown),
        "unknown_mass": unknown_mass,
        "n_numerator": len(numerator_rows),
        "numerator": numerator,
        "denominator": denominator,
        "n_invalid_weight": invalid_weight,
    }
    if denominator <= 0:
        return {**base, "p": None, "se": None, "lo": None, "hi": None,
                "df": 0, "n_domain_missing_design": 0,
                "precision_status": "NO-DISPONIBLE:DENOMINADOR-NULO"}

    p_hat = numerator / denominator
    psu_z = defaultdict(float)
    strata_psu = defaultdict(set)
    domain_missing_design = 0
    full_missing_design = 0
    for row in rows:
        weight = _weight(row.get(cfg["weight"]))
        if weight is None:
            continue
        h, u = _code(row.get("EST_DIS")), _code(row.get("UPM_DIS"))
        in_domain = _is_exposed(row, cfg) and _code(row.get(cfg["response"])) in VALID
        if not h or not u:
            full_missing_design += 1
            if in_domain:
                domain_missing_design += 1
            continue
        key = (h, u)  # anidamiento explícito aun si UPM_DIS resulta globalmente única
        strata_psu[h].add(u)
        if in_domain:
            y = 1.0 if _code(row.get(cfg["response"])) == "1" else 0.0
            psu_z[key] += weight * (y - p_hat) / denominator
        else:
            psu_z[key] += 0.0

    df = sum(max(0, len(psus) - 1) for psus in strata_psu.values())
    if full_missing_design:
        return {**base, "p": p_hat, "se": None, "lo": None, "hi": None,
                "df": df, "n_domain_missing_design": domain_missing_design,
                "precision_status": "NO-DISPONIBLE:DISENO-INCOMPLETO"}
    if p_hat in (0.0, 1.0):
        return {**base, "p": p_hat, "se": None, "lo": None, "hi": None,
                "df": df, "n_domain_missing_design": domain_missing_design,
                "precision_status": "NO-DISPONIBLE:FRONTERA-P-0-O-1"}
    if df <= 0:
        return {**base, "p": p_hat, "se": None, "lo": None, "hi": None,
                "df": df, "n_domain_missing_design": domain_missing_design,
                "precision_status": "NO-DISPONIBLE:GL-NO-POSITIVOS"}

    variance = 0.0
    singleton = 0
    for h, psus in strata_psu.items():
        values = [psu_z[(h, u)] for u in psus]
        m_h = len(values)
        if m_h < 2:
            singleton += 1
            continue
        mean = sum(values) / m_h
        variance += m_h / (m_h - 1) * sum((value - mean) ** 2 for value in values)
    se = math.sqrt(max(0.0, variance))
    critical = float(student_t.ppf(0.975, df))
    return {
        **base,
        "p": p_hat,
        "se": se,
        "lo": max(0.0, p_hat - critical * se),
        "hi": min(1.0, p_hat + critical * se),
        "df": df,
        "n_domain_missing_design": domain_missing_design,
        "precision_status": (
            f"DISPONIBLE:T95-LINEALIZACION-RAZON;SINGLETON={singleton};FPC-NO-APLICADA"
        ),
    }


def medir(inputs, contrato):
    tables = _read_tables(inputs[INPUT_ID]["ruta_absoluta"])
    out = {}

    def put(suffix, value):
        out[PFX + suffix] = value

    put("G-N-ESTIMANDOS", len(ESTIMANDS))
    put("G-METODO-DOMINIO", "MUESTRA-COMPLETA;FUERA-DOMINIO-CERO")
    put("G-ANIDAMIENTO", "EST_DISxUPM_DIS")
    put("G-SINGLETON-REGLA", "SIN-APORTE-A-VARIANZA-NI-GL;SE-REPORTA")
    put("G-FRONTERA-REGLA", "P-0-O-1:PRECISION-NO-DISPONIBLE;NO-SE-CERO")
    put("G-INTERVALO", "T-STUDENT-95-BILATERAL-TRUNCADO-0-1;FPC-NO-APLICADA")

    table_cfg = {
        "THOGAR.csv": ("HOG", "LLAVEHOG", "FAC_HOG"),
        "TMODULO.csv": ("PER", "LLAVEMOD", "FAC_ELE"),
    }
    for table, (short, key, weight) in table_cfg.items():
        rows, width = tables[table]
        required = {key, weight, "EST_DIS", "UPM_DIS"}
        for cfg in ESTIMANDS:
            if cfg["table"] == table:
                required.update((cfg["exposure"], cfg["response"]))
        missing = sorted(required - set(rows[0] if rows else []))
        put(f"{short}-N-FILAS", len(rows))
        put(f"{short}-N-COLUMNAS", width)
        put(f"{short}-COLUMNAS-AUSENTES", ";".join(missing) if missing else "NINGUNA")
        if missing:
            raise ValueError(f"COLUMNAS-AUSENTES:{table}:{missing}")
        put(f"{short}-LLAVE-UNICA", "SI" if len({row[key] for row in rows}) == len(rows) else "NO")
        if len({row[key] for row in rows}) != len(rows):
            raise ValueError(f"LLAVE-DUPLICADA:{table}")
        profile = _design_profile(rows, weight)
        put(f"{short}-PESO-INVALIDO-N", profile["invalid_weights"])
        put(f"{short}-DISENO-FALTANTE-N", profile["missing_design"])
        put(f"{short}-N-ESTRATOS", profile["n_strata"])
        put(f"{short}-N-UPM-ANIDADAS", profile["n_psu_nested"])
        put(f"{short}-N-UPM-CRUZA-ESTRATOS", profile["n_psu_cross_strata"])
        put(f"{short}-N-ESTRATOS-SINGLETON", profile["n_singleton"])
        put(f"{short}-GL", profile["df"])

    estimates = {}
    for cfg in ESTIMANDS:
        rows = tables[cfg["table"]][0]
        est = _estimate(rows, cfg)
        estimates[cfg["code"]] = est
        code = cfg["code"]
        put(f"{code}-N-EXPUESTO", est["n_exposed"])
        put(f"{code}-N-VALIDO", est["n_valid"])
        put(f"{code}-N-DESCONOCIDO", est["n_unknown"])
        put(f"{code}-MASA-DESCONOCIDO", round(est["unknown_mass"], 6))
        put(f"{code}-N-NUMERADOR", est["n_numerator"])
        put(f"{code}-MASA-NUMERADOR", round(est["numerator"], 6))
        put(f"{code}-MASA-DENOMINADOR", round(est["denominator"], 6))
        put(f"{code}-P", None if est["p"] is None else round(est["p"], 12))
        put(f"{code}-EE", None if est["se"] is None else round(est["se"], 12))
        put(f"{code}-IC95-LO", None if est["lo"] is None else round(est["lo"], 12))
        put(f"{code}-IC95-HI", None if est["hi"] is None else round(est["hi"], 12))
        put(f"{code}-GL", est["df"])
        put(f"{code}-N-SIN-DISENO", est["n_domain_missing_design"])
        put(f"{code}-N-PESO-INVALIDO", est["n_invalid_weight"])
        put(f"{code}-PRECISION-ESTADO", est["precision_status"])

    deltas = [abs(estimates[code]["p"] - expected)
              for code, expected in EXPECTED_723.items()
              if estimates[code]["p"] is not None]
    max_delta = max(deltas) if len(deltas) == len(EXPECTED_723) else None
    put("G-CONTRASTE-723-MAX-DELTA", None if max_delta is None else round(max_delta, 12))
    put("G-CONTRASTE-723", "COINCIDE-13-DE-13" if max_delta is not None and max_delta <= 1e-10
        else "DISCREPA")
    p_debt = estimates["PER-ATRASO"]["p"]
    official = None if p_debt is None else round(100 * p_debt, 1)
    put("G-CONTRASTE-OFICIAL-27_3", "COINCIDE" if official == 27.3 else "DISCREPA")
    return out
