"""Precisión del compuesto descriptivo WBES México 2023.

Extiende el CALC padre sin redefinir el estimando. La unidad de muestreo es
el establecimiento y ``strata`` identifica los estratos de selección. La
varianza de Taylor se construye sobre las 1,322 unidades de la muestra: las
unidades fuera del dominio aportan cero en lugar de desaparecer por filtro.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import math
import zipfile
from pathlib import Path

import pandas as pd
from scipy.stats import t as student_t


CALC_ID = "CALC-WBES2023-PRECISION-0001"
PARENT_ID = "CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001"
INPUT_DDI_XML = "wbes_mexico_2023_ddi_xml"
INPUT_DDI_PDF = "wbes_mexico_2023_ddi_pdf"
INPUT_MICRODATA = "wbes_mexico_2023_microdato_dta_zip"
INPUT_DOCUMENTATION = "wbes_mexico_2023_documentacion_zip"
INPUT_SAMPLING_NOTE = "wbes_sampling_note_consolidated_2022_pdf"
EXPECTED_SHA256 = {
    INPUT_DDI_XML: "1d5cded32bef39cc2f129ef63c122d59e4e37b1257b36fc98bc0cc8daccad54c",
    INPUT_DDI_PDF: "069fe4981e1e5d3b2d765009462fc51d24892d6593724f46a8985561b69ae603",
    INPUT_MICRODATA: "bc09225244f1e1274d9c9e58221acf8884512a1ab600551f98fbc0466f479f3f",
    INPUT_DOCUMENTATION: "2b3b0db77f12b841814a37265db279cfcb1778c4377876b77e0a4b725a76c0f7",
    INPUT_SAMPLING_NOTE: "199b37eac44a700146e2f75ec84e2afc79eda52fb48fd2a2059e50ac9df8fa74",
}
MICRODATA_MEMBER = "Mexico-2023-full-data.dta"
STRATUM = "strata"
PRECISION_TYPE = "IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS"
SCENARIOS = ("SINGLETON-CERTEZA", "SINGLETON-AVERAGE")
OUTPUT_COLUMNS = [
    "dominio_id", "dominio", "escenario_singleton", "precision_tipo",
    "n_entrevistados_dominio", "n_expuestos", "n_clasificables",
    "masa_clasificable", "n_si", "punto_padre", "punto_sucesor",
    "delta_punto", "ee", "ic95_inferior", "ic95_superior",
    "limite_inferior_faltantes", "limite_superior_faltantes",
    "n_unidades_muestreo_diseno", "n_estratos_diseno",
    "n_estratos_singleton_diseno",
    "n_singleton_diseno_con_dominio_clasificable",
    "n_estratos_que_serian_singleton_tras_filtro", "grados_libertad",
    "fpc", "transformacion_ic", "estado", "ponderador",
]


def _load_parent():
    path = Path(__file__).resolve().parents[1] / PARENT_ID / "medidor.py"
    spec = importlib.util.spec_from_file_location("wbes2023_parent_medidor", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"PADRE-NO-IMPORTABLE:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PARENT = _load_parent()
REQUIRED_COLUMNS = set(PARENT.REQUIRED_COLUMNS) | {STRATUM}


def _read_input(entry: dict) -> bytes:
    raw = entry.get("bytes")
    return raw if raw is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_microdata(raw_zip: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
        if zf.testzip() is not None:
            raise ValueError("ZIP-MICRODATO-CORRUPTO")
        members = [info.filename for info in zf.infolist() if not info.is_dir()]
        if members != [MICRODATA_MEMBER]:
            raise ValueError(f"MIEMBROS-MICRODATO-INESPERADOS:{members}")
        raw_dta = zf.read(MICRODATA_MEMBER)
    return pd.read_stata(
        io.BytesIO(raw_dta), columns=sorted(REQUIRED_COLUMNS),
        convert_categoricals=False,
    )


def validate_design(frame: pd.DataFrame) -> None:
    """Rechaza la ausencia del estrato acreditado; no fabrica UPM ni estrato."""
    PARENT.validate_frame(frame)
    if STRATUM not in frame:
        raise ValueError(f"CAMPO-DISENO-AUSENTE:{STRATUM}")
    if frame[STRATUM].isna().any():
        raise ValueError(f"CAMPO-DISENO-INCOMPLETO:{STRATUM}")
    if frame[STRATUM].nunique() < 2:
        raise ValueError("DISENO-SIN-ESTRATIFICACION-OPERATIVA")


def _domain_mask(frame: pd.DataFrame, size_code: int | None) -> pd.Series:
    if size_code is None:
        return pd.Series(True, index=frame.index)
    return frame[PARENT.SIZE].map(lambda value: PARENT._is_code(value, size_code))


def _domain_vectors(frame: pd.DataFrame, size_code: int | None):
    eligibility, outcome = PARENT._classifications(frame, None)
    in_size = _domain_mask(frame, size_code)
    classified = in_size & eligibility.eq("eligible") & outcome.isin(("yes", "no"))
    yes = classified & outcome.eq("yes")
    return classified.astype(float), yes.astype(float), classified, yes


def _stratum_profile(frame: pd.DataFrame, classified: pd.Series) -> dict[str, int]:
    full_counts = frame.groupby(STRATUM, dropna=False).size()
    domain_counts = classified.groupby(frame[STRATUM], dropna=False).sum().astype(int)
    return {
        "n_units": int(len(frame)),
        "n_strata": int(len(full_counts)),
        "n_singleton": int((full_counts == 1).sum()),
        "df": int((full_counts - 1).clip(lower=0).sum()),
        "n_singleton_with_domain": int(((full_counts == 1) & (domain_counts == 1)).sum()),
        "n_filter_created_singleton": int(((full_counts > 1) & (domain_counts == 1)).sum()),
    }


def linearized_variance(
    frame: pd.DataFrame,
    x: pd.Series,
    y: pd.Series,
    point: float,
    denominator: float,
    scenario: str,
) -> tuple[float, dict[str, int]]:
    """Varianza WR de razón por estrato, con dos políticas singleton fijadas."""
    if scenario not in SCENARIOS:
        raise ValueError(f"ESCENARIO-SINGLETON-DESCONOCIDO:{scenario}")
    if denominator <= 0:
        raise ValueError("DENOMINADOR-NO-POSITIVO")
    influence = frame[PARENT.WEIGHT] * (y - point * x) / denominator
    contributions = []
    singleton = 0
    for _, indexes in frame.groupby(STRATUM, dropna=False, sort=True).groups.items():
        values = [float(influence.loc[index]) for index in indexes]
        n_h = len(values)
        if n_h == 1:
            singleton += 1
            continue
        mean = math.fsum(values) / n_h
        contributions.append(
            n_h / (n_h - 1) * math.fsum((value - mean) ** 2 for value in values)
        )
    variance = math.fsum(contributions)
    if scenario == "SINGLETON-AVERAGE":
        if not contributions:
            raise ValueError("SIN-ESTRATOS-NO-SINGLETON")
        variance *= (len(contributions) + singleton) / len(contributions)
    profile = _stratum_profile(frame, x.astype(bool))
    if singleton != profile["n_singleton"]:
        raise AssertionError("CONTEO-SINGLETON-INCONSISTENTE")
    return variance, profile


def logit_interval(point: float, se: float, df: int) -> tuple[float | None, float | None, str]:
    """IC95 logit-t; una proporción frontera queda explícitamente no estimable."""
    if point <= 0.0 or point >= 1.0:
        return None, None, "PRECISION-NO-ESTIMABLE-FRONTERA"
    if not math.isfinite(se) or se < 0 or df <= 0:
        return None, None, "PRECISION-NO-ESTIMABLE-VARIANZA-O-GL"
    critical = float(student_t.ppf(0.975, df))
    logit = math.log(point / (1.0 - point))
    se_logit = se / (point * (1.0 - point))
    inverse = lambda value: 1.0 / (1.0 + math.exp(-value))
    return (
        inverse(logit - critical * se_logit),
        inverse(logit + critical * se_logit),
        "OK",
    )


def estimate_domain(frame: pd.DataFrame, domain: tuple, scenario: str) -> dict:
    domain_id, domain_label, size_code = domain
    parent_row = PARENT.aggregate(frame, None, domain)
    x, y, classified, yes = _domain_vectors(frame, size_code)
    weights = frame[PARENT.WEIGHT]
    numerator = float(weights.loc[yes].sum())
    # El padre suma sí y no por separado. Con ``wmedian`` float32, sumar la
    # máscara conjunta cambia los últimos bits por el orden de reducción.
    # Reproducir su orden es parte del contrato de identidad del punto.
    negative = classified & ~yes
    denominator = numerator + float(weights.loc[negative].sum())
    point = numerator / denominator
    parent_point = float(parent_row["proporcion_observada"])
    delta = abs(point - parent_point)
    if delta > 5e-12:
        raise ValueError(f"PUNTO-NO-REPRODUCE-PADRE:{domain_id}:{delta}")
    if int(parent_row["n_denominador_observado"]) != int(classified.sum()):
        raise ValueError(f"DENOMINADOR-NO-REPRODUCE-PADRE:{domain_id}")

    variance, profile = linearized_variance(frame, x, y, point, denominator, scenario)
    se = math.sqrt(max(0.0, variance))
    lo, hi, interval_status = logit_interval(point, se, profile["df"])
    status = interval_status if interval_status != "OK" else PRECISION_TYPE
    return {
        "dominio_id": domain_id,
        "dominio": domain_label,
        "escenario_singleton": scenario,
        "precision_tipo": PRECISION_TYPE,
        "n_entrevistados_dominio": int(parent_row["n_entrevistados"]),
        "n_expuestos": int(parent_row["n_expuestos"]),
        "n_clasificables": int(parent_row["n_denominador_observado"]),
        "masa_clasificable": denominator,
        "n_si": int(parent_row["n_si"]),
        "punto_padre": parent_point,
        "punto_sucesor": point,
        "delta_punto": delta,
        "ee": se,
        "ic95_inferior": lo,
        "ic95_superior": hi,
        "limite_inferior_faltantes": float(parent_row["limite_inferior_faltantes"]),
        "limite_superior_faltantes": float(parent_row["limite_superior_faltantes"]),
        "n_unidades_muestreo_diseno": profile["n_units"],
        "n_estratos_diseno": profile["n_strata"],
        "n_estratos_singleton_diseno": profile["n_singleton"],
        "n_singleton_diseno_con_dominio_clasificable": profile["n_singleton_with_domain"],
        "n_estratos_que_serian_singleton_tras_filtro": profile["n_filter_created_singleton"],
        "grados_libertad": profile["df"],
        "fpc": "NO-APLICADA;NO-DISPONIBLE-POR-ESTRATO-PANEL-FRESH",
        "transformacion_ic": "LOGIT-T-95",
        "estado": status,
        "ponderador": PARENT.WEIGHT,
    }


def calculate(frame: pd.DataFrame) -> list[dict]:
    validate_design(frame)
    return [
        estimate_domain(frame, domain, scenario)
        for domain in PARENT.DOMAINS
        for scenario in SCENARIOS
    ]


def _fmt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12f}"
    return str(value)


def _serialize(rows: list[dict]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: _fmt(row[key]) for key in OUTPUT_COLUMNS} for row in rows)
    return buffer.getvalue().encode("utf-8")


def _write_output(raw: bytes) -> Path:
    repo = Path(__file__).resolve().parents[3]
    output = repo / "forense/analisis/wbes2023-precision-1/wbes2023-precision.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    return output


def medir(inputs: dict, contrato: dict) -> dict:
    raw_inputs = {key: _read_input(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        actual = _sha256(raw_inputs[key])
        if actual != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{actual}")
    if not raw_inputs[INPUT_DDI_XML].lstrip().startswith(b"<?xml"):
        raise ValueError("DDI-XML-INVALIDO")
    for key in (INPUT_DDI_PDF, INPUT_SAMPLING_NOTE):
        if not raw_inputs[key].startswith(b"%PDF"):
            raise ValueError(f"PDF-INVALIDO:{key}")
    if not zipfile.is_zipfile(io.BytesIO(raw_inputs[INPUT_DOCUMENTATION])):
        raise ValueError("DOCUMENTACION-ZIP-INVALIDA")

    frame = _read_microdata(raw_inputs[INPUT_MICRODATA])
    rows = calculate(frame)
    serialized = _serialize(rows)
    output = _write_output(serialized)
    by_key = {(row["dominio_id"], row["escenario_singleton"]): row for row in rows}
    result = {
        "RESULT-WBES2023-PREC-G-TIPO": PRECISION_TYPE,
        "RESULT-WBES2023-PREC-G-N-UNIDADES": rows[0]["n_unidades_muestreo_diseno"],
        "RESULT-WBES2023-PREC-G-N-ESTRATOS": rows[0]["n_estratos_diseno"],
        "RESULT-WBES2023-PREC-G-N-SINGLETON": rows[0]["n_estratos_singleton_diseno"],
        "RESULT-WBES2023-PREC-G-GL": rows[0]["grados_libertad"],
        "RESULT-WBES2023-PREC-G-FPC": rows[0]["fpc"],
        "RESULT-WBES2023-PREC-G-CSV-SHA256": _sha256(serialized),
        "RESULT-WBES2023-PREC-G-SALIDA": str(output.relative_to(Path(__file__).resolve().parents[3])),
        "RESULT-WBES2023-PREC-G-MAX-DELTA-PADRE": max(row["delta_punto"] for row in rows),
    }
    for domain_id, _, _ in PARENT.DOMAINS:
        short = domain_id.replace("-", "_")
        base = by_key[(domain_id, SCENARIOS[0])]
        result[f"RESULT-WBES2023-PREC-{short}-PUNTO"] = base["punto_sucesor"]
        result[f"RESULT-WBES2023-PREC-{short}-N-CLASIFICABLE"] = base["n_clasificables"]
        for scenario in SCENARIOS:
            suffix = "CERTEZA" if scenario.endswith("CERTEZA") else "AVERAGE"
            row = by_key[(domain_id, scenario)]
            result[f"RESULT-WBES2023-PREC-{short}-{suffix}-EE"] = row["ee"]
            result[f"RESULT-WBES2023-PREC-{short}-{suffix}-IC95-LO"] = row["ic95_inferior"]
            result[f"RESULT-WBES2023-PREC-{short}-{suffix}-IC95-HI"] = row["ic95_superior"]
    return result
