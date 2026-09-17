#!/usr/bin/env python3
"""Mide solicitudes/expectativas de pagos informales en WBES México 2023."""
from __future__ import annotations

import csv
import hashlib
import io
import math
import zipfile
from pathlib import Path

import pandas as pd


CALC_ID = "CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001"
INPUT_DDI_XML = "wbes_mexico_2023_ddi_xml"
INPUT_DDI_PDF = "wbes_mexico_2023_ddi_pdf"
INPUT_MICRODATA = "wbes_mexico_2023_microdato_dta_zip"
INPUT_DOCUMENTATION = "wbes_mexico_2023_documentacion_zip"
EXPECTED_SHA256 = {
    INPUT_DDI_XML: "1d5cded32bef39cc2f129ef63c122d59e4e37b1257b36fc98bc0cc8daccad54c",
    INPUT_DDI_PDF: "069fe4981e1e5d3b2d765009462fc51d24892d6593724f46a8985561b69ae603",
    INPUT_MICRODATA: "bc09225244f1e1274d9c9e58221acf8884512a1ab600551f98fbc0466f479f3f",
    INPUT_DOCUMENTATION: "2b3b0db77f12b841814a37265db279cfcb1778c4377876b77e0a4b725a76c0f7",
}
MICRODATA_MEMBER = "Mexico-2023-full-data.dta"
WEIGHT = "wmedian"
SIZE = "a6a"
IDENTIFIER = "idstd"
UNCERTAINTY = "IC-DE-DISEÑO-NO-ESTIMABLE-CON-INSUMOS-DISPONIBLES"
USE = "CONTEXTO-INFORME-NO-CALIBRA;UNIDAD-DISTINTA-NO-TRANSFERENCIA"

INTERACTIONS = (
    ("ELECTRICIDAD", "Conexión eléctrica", "c3", "c5", "últimos dos años"),
    ("AGUA", "Conexión de agua", "c12", "c14", "últimos dos años"),
    ("CONSTRUCCION", "Permiso de construcción", "g2", "g4", "últimos dos años"),
    ("FISCAL", "Inspección o reunión fiscal", "j3", "j5", "último año"),
    ("IMPORTACION", "Licencia de importación", "j10", "j12", "últimos dos años"),
    ("OPERACION", "Licencia de operación", "j13", "j15", "últimos dos años"),
)
DOMAINS = (
    ("TOTAL", "Total nacional cubierto", None),
    ("PEQUENA", "Pequeña (5-19)", 1),
    ("MEDIANA", "Mediana (20-99)", 2),
    ("GRANDE", "Grande (100-250)", 3),
    ("EXTRA-GRANDE", "Extra grande (251+)", 4),
)
REQUIRED_COLUMNS = {
    IDENTIFIER, WEIGHT, SIZE,
    *(parent for _, _, parent, _, _ in INTERACTIONS),
    *(event for _, _, _, event, _ in INTERACTIONS),
}
OUTPUT_COLUMNS = [
    "indicador_id", "indicador_tipo", "interaccion", "ventana_referencia",
    "dominio_id", "dominio", "n_entrevistados", "peso_entrevistados",
    "n_expuestos", "peso_expuestos", "n_si", "peso_si", "n_no", "peso_no",
    "n_desconocido", "peso_desconocido", "n_elegibilidad_desconocida",
    "peso_elegibilidad_desconocida", "n_sin_interaccion", "peso_sin_interaccion",
    "n_denominador_observado", "peso_denominador_observado",
    "proporcion_observada", "porcentaje_observado",
    "masa_desconocida_entre_expuestos", "limite_inferior_faltantes",
    "limite_superior_faltantes", "incertidumbre_muestral", "estado",
    "ponderador", "unidad", "uso",
]


def _read_input(entry: dict) -> bytes:
    raw = entry.get("bytes")
    if raw is not None:
        return raw
    return Path(entry["ruta_absoluta"]).read_bytes()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _is_code(value, code: int) -> bool:
    if pd.isna(value):
        return False
    try:
        return float(value) == float(code)
    except (TypeError, ValueError):
        return False


def _parent_state(value) -> str:
    if _is_code(value, 1):
        return "eligible"
    if _is_code(value, 2):
        return "not_eligible"
    return "eligibility_unknown"


def _event_state(value) -> str:
    if _is_code(value, 1):
        return "yes"
    if _is_code(value, 2):
        return "no"
    return "unknown"


def classify_interaction(row: pd.Series, parent: str, event: str) -> tuple[str, str | None]:
    """Devuelve estado de elegibilidad y, si aplica, estado del evento."""
    eligibility = _parent_state(row[parent])
    if eligibility != "eligible":
        return eligibility, None
    return eligibility, _event_state(row[event])


def classify_composite(row: pd.Series) -> tuple[str, str | None]:
    """Clasifica una vez al establecimiento en el compuesto de seis interacciones."""
    applicable = []
    parent_states = []
    for _, _, parent, event, _ in INTERACTIONS:
        eligibility, outcome = classify_interaction(row, parent, event)
        parent_states.append(eligibility)
        if eligibility == "eligible":
            applicable.append(outcome)
    if not applicable:
        if "eligibility_unknown" in parent_states:
            return "eligibility_unknown", None
        return "not_eligible", None
    if "yes" in applicable:
        return "eligible", "yes"
    if all(value == "no" for value in applicable):
        return "eligible", "no"
    return "eligible", "unknown"


def proportion_to_percent(value: float | None) -> float | None:
    return None if value is None else value * 100.0


def _weighted_total(frame: pd.DataFrame, mask: pd.Series) -> float:
    return float(frame.loc[mask, WEIGHT].sum())


def _ratio(numerator: float, denominator: float) -> float | None:
    return None if denominator <= 0 else numerator / denominator


def _fmt_number(value: float | int | None) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    return f"{value:.12f}"


def _classifications(frame: pd.DataFrame, interaction: tuple | None) -> tuple[pd.Series, pd.Series]:
    if interaction is None:
        states = frame.apply(classify_composite, axis=1)
    else:
        _, _, parent, event, _ = interaction
        states = frame.apply(lambda row: classify_interaction(row, parent, event), axis=1)
    eligibility = states.map(lambda pair: pair[0])
    outcome = states.map(lambda pair: pair[1])
    return eligibility, outcome


def aggregate(frame: pd.DataFrame, interaction: tuple | None, domain: tuple) -> dict[str, str]:
    domain_id, domain_label, size_code = domain
    subset = frame if size_code is None else frame.loc[frame[SIZE].map(lambda x: _is_code(x, size_code))]
    eligibility, outcome = _classifications(subset, interaction)
    eligible = eligibility.eq("eligible")
    eligibility_unknown = eligibility.eq("eligibility_unknown")
    not_eligible = eligibility.eq("not_eligible")
    yes = eligible & outcome.eq("yes")
    no = eligible & outcome.eq("no")
    unknown = eligible & outcome.eq("unknown")

    weight_yes = _weighted_total(subset, yes)
    weight_no = _weighted_total(subset, no)
    weight_unknown = _weighted_total(subset, unknown)
    weight_exposed = weight_yes + weight_no + weight_unknown
    weight_observed = weight_yes + weight_no
    point = _ratio(weight_yes, weight_observed)
    missing_mass = _ratio(weight_unknown, weight_exposed)
    lower = _ratio(weight_yes, weight_exposed)
    upper = _ratio(weight_yes + weight_unknown, weight_exposed)
    status = "OK" if point is not None else "DENOMINADOR-VACIO"

    if interaction is None:
        indicator_id = "COMPUESTO-SEIS-INTERACCIONES"
        indicator_type = "compuesto descriptivo propio"
        interaction_label = "Al menos una de seis interacciones"
        window = "ventana propia de cada interacción (una o dos años)"
    else:
        short_id, interaction_label, _, _, window = interaction
        indicator_id = f"INTERACCION-{short_id}"
        indicator_type = "tasa separada documentada"

    values = {
        "indicador_id": indicator_id,
        "indicador_tipo": indicator_type,
        "interaccion": interaction_label,
        "ventana_referencia": window,
        "dominio_id": domain_id,
        "dominio": domain_label,
        "n_entrevistados": int(len(subset)),
        "peso_entrevistados": float(subset[WEIGHT].sum()),
        "n_expuestos": int(eligible.sum()),
        "peso_expuestos": weight_exposed,
        "n_si": int(yes.sum()),
        "peso_si": weight_yes,
        "n_no": int(no.sum()),
        "peso_no": weight_no,
        "n_desconocido": int(unknown.sum()),
        "peso_desconocido": weight_unknown,
        "n_elegibilidad_desconocida": int(eligibility_unknown.sum()),
        "peso_elegibilidad_desconocida": _weighted_total(subset, eligibility_unknown),
        "n_sin_interaccion": int(not_eligible.sum()),
        "peso_sin_interaccion": _weighted_total(subset, not_eligible),
        "n_denominador_observado": int(yes.sum() + no.sum()),
        "peso_denominador_observado": weight_observed,
        "proporcion_observada": point,
        "porcentaje_observado": proportion_to_percent(point),
        "masa_desconocida_entre_expuestos": missing_mass,
        "limite_inferior_faltantes": lower,
        "limite_superior_faltantes": upper,
        "incertidumbre_muestral": UNCERTAINTY,
        "estado": status,
        "ponderador": WEIGHT,
        "unidad": "establecimientos expuestos",
        "uso": USE,
    }
    return {
        key: _fmt_number(value) if value is None or isinstance(value, (int, float)) else value
        for key, value in values.items()
    }


def validate_frame(frame: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"VARIABLES-AUSENTES:{missing}")
    if frame[IDENTIFIER].isna().any() or frame[IDENTIFIER].duplicated().any():
        raise ValueError("IDSTD-NO-UNICO-O-FALTANTE")
    weights = pd.to_numeric(frame[WEIGHT], errors="coerce")
    if weights.isna().any() or (~weights.map(math.isfinite)).any() or (weights <= 0).any():
        raise ValueError("PONDERADOR-NO-POSITIVO-O-NO-FINITO")
    frame[WEIGHT] = weights
    invalid_sizes = [value for value in frame[SIZE].dropna().unique() if not any(_is_code(value, code) for code in (1, 2, 3, 4))]
    if invalid_sizes:
        raise ValueError(f"TAMANO-FUERA-DE-CATALOGO:{invalid_sizes}")


def calculate(frame: pd.DataFrame) -> list[dict[str, str]]:
    validate_frame(frame)
    rows = []
    for interaction in (None, *INTERACTIONS):
        for domain in DOMAINS:
            rows.append(aggregate(frame, interaction, domain))
    return rows


def _serialize(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def _read_microdata(raw_zip: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
        if zf.testzip() is not None:
            raise ValueError("ZIP-MICRODATO-CORRUPTO")
        members = [info.filename for info in zf.infolist() if not info.is_dir()]
        if members != [MICRODATA_MEMBER]:
            raise ValueError(f"MIEMBROS-MICRODATO-INESPERADOS:{members}")
        raw_dta = zf.read(MICRODATA_MEMBER)
    return pd.read_stata(io.BytesIO(raw_dta), columns=sorted(REQUIRED_COLUMNS), convert_categoricals=False)


def _write_output(raw: bytes) -> Path:
    repo = Path(__file__).resolve().parents[3]
    output = repo / "forense/analisis/wbes2023-descriptiva-1/wbes2023-solicitud-expectativa-pago-informal.csv"
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
    if not raw_inputs[INPUT_DDI_PDF].startswith(b"%PDF"):
        raise ValueError("DDI-PDF-INVALIDO")
    if not zipfile.is_zipfile(io.BytesIO(raw_inputs[INPUT_DOCUMENTATION])):
        raise ValueError("DOCUMENTACION-ZIP-INVALIDA")

    frame = _read_microdata(raw_inputs[INPUT_MICRODATA])
    rows = calculate(frame)
    serialized = _serialize(rows)
    output = _write_output(serialized)
    primary = next(row for row in rows if row["indicador_id"] == "COMPUESTO-SEIS-INTERACCIONES" and row["dominio_id"] == "TOTAL")
    if primary["estado"] != "OK":
        raise ValueError("PRIMARIO-SIN-DENOMINADOR")
    return {
        "RESULT-WBES2023-DES-G-INPUT-DDI-XML-SHA256": _sha256(raw_inputs[INPUT_DDI_XML]),
        "RESULT-WBES2023-DES-G-INPUT-DDI-PDF-SHA256": _sha256(raw_inputs[INPUT_DDI_PDF]),
        "RESULT-WBES2023-DES-G-INPUT-MICRODATO-SHA256": _sha256(raw_inputs[INPUT_MICRODATA]),
        "RESULT-WBES2023-DES-G-INPUT-DOCUMENTACION-SHA256": _sha256(raw_inputs[INPUT_DOCUMENTATION]),
        "RESULT-WBES2023-DES-G-N-ENTREVISTADOS": len(frame),
        "RESULT-WBES2023-DES-G-N-EXPUESTOS-TOTAL": int(primary["n_expuestos"]),
        "RESULT-WBES2023-DES-G-N-CLASIFICADOS-TOTAL": int(primary["n_denominador_observado"]),
        "RESULT-WBES2023-DES-G-PESO-EXPUESTOS-TOTAL": float(primary["peso_expuestos"]),
        "RESULT-WBES2023-DES-PUNTO-TOTAL": float(primary["proporcion_observada"]),
        "RESULT-WBES2023-DES-MASA-DESCONOCIDA-TOTAL": float(primary["masa_desconocida_entre_expuestos"]),
        "RESULT-WBES2023-DES-LIMITE-INFERIOR-TOTAL": float(primary["limite_inferior_faltantes"]),
        "RESULT-WBES2023-DES-LIMITE-SUPERIOR-TOTAL": float(primary["limite_superior_faltantes"]),
        "RESULT-WBES2023-DES-G-N-FILAS-SALIDA": len(rows),
        "RESULT-WBES2023-DES-G-CSV-SHA256": _sha256(serialized),
        "RESULT-WBES2023-DES-G-INCERTIDUMBRE": UNCERTAINTY,
        "RESULT-WBES2023-DES-G-USO": USE,
        "RESULT-WBES2023-DES-G-SALIDA": str(output.relative_to(Path(__file__).resolve().parents[3])),
    }
