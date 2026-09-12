"""Medidor descriptivo de BNPL y daño en SHED 2025.

El CSV público trae etiquetas textuales aunque el codebook publique códigos
numéricos. Este medidor congela esa traducción y conserva cada universo de
pregunta. No calcula varianza: ``weight`` es un ponderador transversal de
postestratificación, pero el archivo público no acredita aquí todas las
variables del diseño necesarias para una varianza oficial.
"""
from __future__ import annotations

import csv
import io
import math
import zipfile


INPUT_ID = "gen2_federal_reserve_shed_2025_public_csv"
MEMBER = "public2025.csv"
PFX = "RESULT-SHED-BNPL-"
REQUIRED = {
    "shedid", "weight", "weight_pop", "BK1", "BK2_f", "BNPL1",
    "BNPL3", "BNPL3A", "BNPL1A", "BNPL4_e",
}
QUESTION_COLUMNS = tuple(sorted(REQUIRED - {"shedid", "weight", "weight_pop"}))

# Traducción exacta del CSV. Un "1" o "0" textual es un error: mezclaría la
# cara numérica del codebook con la cara etiquetada del archivo analizado.
CODES = {
    "Yes": "SI",
    "No": "NO",
    "Refused": "RECHAZO",
    "Don't know": "NO_SABE",
    "": "VACIO",
}
VALID = {"Yes", "No"}

DEFINITIONS = {
    "USO": (
        "Todas las personas con BNPL1 válido; proporción ponderada que usó "
        "Buy Now, Pay Later en el último año."
    ),
    "ATRASO": (
        "Personas con BNPL1=Yes y BNPL3 válido; proporción ponderada que "
        "reportó haberse atrasado en un pago BNPL en el último año."
    ),
    "CARGO": (
        "Personas con BNPL1=Yes, BNPL3=Yes y BNPL3A válido; proporción "
        "ponderada que reportó cargo extra por el atraso. La ruta de rechazo "
        "en BNPL3 se informa aparte y nunca integra este denominador."
    ),
    "SOBREGIRO": (
        "Personas con BNPL1=Yes, cuenta bancaria vigente (BK1=Yes), "
        "BK2_f=Yes y BNPL1A válido; proporción ponderada cuyo pago BNPL "
        "disparó cargo por sobregiro o fondos insuficientes."
    ),
    "ASEQ-ATRASO": (
        "Personas con BNPL1=Yes, BNPL4_e y BNPL3 válidos; tabla 2x2 "
        "ponderada y diferencia descriptiva P(atraso|asequibilidad=Yes) "
        "menos P(atraso|asequibilidad=No)."
    ),
}


def _round(value):
    return round(float(value), 12)


def _weight(row, column="weight"):
    try:
        value = float(str(row.get(column, "")).strip())
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def _read_rows(path):
    with zipfile.ZipFile(path) as zf:
        if zf.testzip() is not None:
            raise ValueError("ZIP-CORRUPTO")
        members = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if members != [MEMBER]:
            raise ValueError(f"MIEMBRO-CSV-INESPERADO:{members}")
        raw = zf.read(MEMBER).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw, newline=""))
    fields = reader.fieldnames or []
    missing = sorted(REQUIRED - set(fields))
    if missing:
        raise ValueError(f"COLUMNAS-AUSENTES:{missing}")
    return list(reader), len(fields)


def _validate(rows, expected_rows=None):
    if expected_rows is not None and len(rows) != expected_rows:
        raise ValueError(f"N-FILAS-INESPERADO:{len(rows)}!={expected_rows}")
    ids = [str(row.get("shedid", "")).strip() for row in rows]
    if not all(ids) or len(ids) != len(set(ids)):
        raise ValueError("SHEDID-AUSENTE-O-DUPLICADO")
    for column in QUESTION_COLUMNS:
        unexpected = sorted({str(row.get(column, "")).strip() for row in rows} - set(CODES))
        if unexpected:
            raise ValueError(f"CODIFICACION-NO-TEXTUAL:{column}:{unexpected}")
    invalid_weights = sum(
        _weight(row, "weight") is None or _weight(row, "weight_pop") is None
        for row in rows
    )
    if invalid_weights:
        raise ValueError(f"PESOS-NO-POSITIVOS-O-NO-FINITOS:{invalid_weights}")

    # Una respuesta fuera de ruta no se transforma en "No".
    outside_nsf = [
        row for row in rows
        if row["BNPL1"] != "Yes" or row["BK1"] != "Yes" or row["BK2_f"] != "Yes"
    ]
    if any(row["BNPL1A"] != "" for row in outside_nsf):
        raise ValueError("BNPL1A-RESPUESTA-FUERA-DE-RUTA")
    if any(row["BNPL3A"] in VALID and row["BNPL3"] == "No" for row in rows):
        raise ValueError("BNPL3A-RESPUESTA-CON-BNPL3-NO")


def _mass(rows, column="weight"):
    return sum(_weight(row, column) for row in rows)


def _estimate(rows, eligible, variable):
    selected = [row for row in rows if eligible(row)]
    valid = [row for row in selected if row[variable] in VALID]
    positive = [row for row in valid if row[variable] == "Yes"]
    denominator = _mass(valid)
    numerator = _mass(positive)
    if denominator <= 0:
        raise ValueError(f"DENOMINADOR-NULO:{variable}")
    return {
        "n_eligible": len(selected),
        "n_valid": len(valid),
        "n_positive": len(positive),
        "mass_eligible": _round(_mass(selected)),
        "mass_valid": _round(denominator),
        "mass_positive": _round(numerator),
        "point": _round(numerator / denominator),
    }


def _missing_counts(rows):
    users = [row for row in rows if row["BNPL1"] == "Yes"]
    late_yes = [row for row in users if row["BNPL3"] == "Yes"]
    fee_refused = [row for row in users if row["BNPL3"] == "Refused"]
    return {
        "USO": {
            "NO_APLICA": 0,
            "RECHAZO": sum(row["BNPL1"] == "Refused" for row in rows),
            "NO_SABE": sum(row["BNPL1"] == "Don't know" for row in rows),
            "SIN_RESPUESTA": sum(row["BNPL1"] == "" for row in rows),
        },
        "ATRASO": {
            "NO_APLICA_NO_USO_BNPL": len(rows) - len(users),
            "RECHAZO": sum(row["BNPL3"] == "Refused" for row in users),
            "NO_SABE": sum(row["BNPL3"] == "Don't know" for row in users),
            "SIN_RESPUESTA": sum(row["BNPL3"] == "" for row in users),
        },
        "CARGO": {
            "NO_APLICA_NO_ATRASO_AFIRMATIVO": len(rows) - len(late_yes) - len(fee_refused),
            "RUTA_RECHAZO_BNPL3": len(fee_refused),
            "RECHAZO_BNPL3A": sum(row["BNPL3A"] == "Refused" for row in late_yes),
            "NO_SABE_BNPL3A": sum(row["BNPL3A"] == "Don't know" for row in late_yes),
            "SIN_RESPUESTA_BNPL3A": sum(row["BNPL3A"] == "" for row in late_yes),
        },
        "SOBREGIRO": {
            "NO_APLICA_NO_USO_BNPL": sum(row["BNPL1"] != "Yes" for row in rows),
            "NO_APLICA_SIN_CUENTA_BANCARIA": sum(
                row["BNPL1"] == "Yes" and row["BK1"] == "No" for row in rows
            ),
            "NO_APLICA_SIN_SOBREGIRO_PREVIO": sum(
                row["BNPL1"] == "Yes" and row["BK1"] == "Yes" and row["BK2_f"] == "No"
                for row in rows
            ),
            "BK2_F_RECHAZO": sum(row["BNPL1"] == "Yes" and row["BK2_f"] == "Refused" for row in rows),
            "BK2_F_NO_SABE": sum(row["BNPL1"] == "Yes" and row["BK2_f"] == "Don't know" for row in rows),
            "BK2_F_SIN_RESPUESTA": sum(row["BNPL1"] == "Yes" and row["BK1"] == "Yes" and row["BK2_f"] == "" for row in rows),
            "BNPL1A_RECHAZO": sum(row["BNPL1A"] == "Refused" for row in rows),
            "BNPL1A_NO_SABE": sum(row["BNPL1A"] == "Don't know" for row in rows),
            "BNPL1A_SIN_RESPUESTA": sum(
                row["BNPL1"] == "Yes" and row["BK2_f"] == "Yes" and row["BNPL1A"] == ""
                for row in rows
            ),
        },
        "ASEQ-ATRASO": {
            "NO_APLICA_NO_USO_BNPL": len(rows) - len(users),
            "BNPL4_E_RECHAZO": sum(row["BNPL4_e"] == "Refused" for row in users),
            "BNPL4_E_NO_SABE": sum(row["BNPL4_e"] == "Don't know" for row in users),
            "BNPL4_E_SIN_RESPUESTA": sum(row["BNPL4_e"] == "" for row in users),
            "BNPL3_RECHAZO": sum(row["BNPL3"] == "Refused" for row in users),
            "BNPL3_NO_SABE": sum(row["BNPL3"] == "Don't know" for row in users),
            "BNPL3_SIN_RESPUESTA": sum(row["BNPL3"] == "" for row in users),
        },
    }


def _missing_text(values):
    return ";".join(f"{key}={values[key]}" for key in sorted(values))


def calculate(rows, width=815, expected_rows=None):
    """Calcula RESULT; se expone para falsadores con fixtures mínimos."""
    _validate(rows, expected_rows=expected_rows)
    out = {}

    def put(suffix, value):
        out[PFX + suffix] = value

    put("G-N-FILAS", len(rows))
    put("G-N-COLUMNAS", width)
    put("G-SHEDID-UNICO", "SI")
    put("G-PESO-INVALIDO-N", 0)
    put("G-MASA-WEIGHT", _round(_mass(rows, "weight")))
    put("G-MASA-WEIGHT-POP", _round(_mass(rows, "weight_pop")))
    put("G-CODIFICACION", "CSV:Yes=1;No=0;Refused=RECHAZO;Don't know=NO_SABE;vacio=NO_APLICA_O_FALTANTE_SEGUN_RUTA;codebook:1=Yes,0=No")
    put("G-PONDERADOR", "weight;TRANSVERSAL;NO-panel_weight;PUNTO-COMO-RAZON-DE-MASAS")
    put("G-PRECISION", "NO-CALCULADA;POSTESTRATIFICACION-SIN-DISENO-COMPLETO-ACREDITADO")

    specs = {
        "USO": (lambda row: True, "BNPL1"),
        "ATRASO": (lambda row: row["BNPL1"] == "Yes", "BNPL3"),
        "CARGO": (lambda row: row["BNPL1"] == "Yes" and row["BNPL3"] == "Yes", "BNPL3A"),
        "SOBREGIRO": (
            lambda row: row["BNPL1"] == "Yes" and row["BK1"] == "Yes" and row["BK2_f"] == "Yes",
            "BNPL1A",
        ),
    }
    missing = _missing_counts(rows)
    for code, (eligible, variable) in specs.items():
        estimate = _estimate(rows, eligible, variable)
        for field, suffix in (
            ("n_eligible", "N-ELEGIBLE"),
            ("n_valid", "N-VALIDO"),
            ("n_positive", "N-POSITIVOS"),
            ("mass_eligible", "MASA-ELEGIBLE"),
            ("mass_valid", "MASA-VALIDA"),
            ("mass_positive", "MASA-POSITIVOS"),
            ("point", "PUNTO"),
        ):
            put(f"{code}-{suffix}", estimate[field])
        put(f"{code}-FALTANTES", _missing_text(missing[code]))
        put(f"{code}-DEFINICION", DEFINITIONS[code])

    refused_route = [row for row in rows if row["BNPL1"] == "Yes" and row["BNPL3"] == "Refused"]
    refused_valid = [row for row in refused_route if row["BNPL3A"] in VALID]
    refused_positive = [row for row in refused_valid if row["BNPL3A"] == "Yes"]
    put("CARGO-RUTA-RECHAZO-N-ELEGIBLE", len(refused_route))
    put("CARGO-RUTA-RECHAZO-N-VALIDO", len(refused_valid))
    put("CARGO-RUTA-RECHAZO-N-POSITIVOS", len(refused_positive))
    put("CARGO-RUTA-RECHAZO-MASA-VALIDA", _round(_mass(refused_valid)))

    association_eligible = [row for row in rows if row["BNPL1"] == "Yes"]
    association_valid = [
        row for row in association_eligible
        if row["BNPL4_e"] in VALID and row["BNPL3"] in VALID
    ]
    put("ASEQ-ATRASO-N-ELEGIBLE", len(association_eligible))
    put("ASEQ-ATRASO-N-VALIDO", len(association_valid))
    put("ASEQ-ATRASO-MASA-ELEGIBLE", _round(_mass(association_eligible)))
    put("ASEQ-ATRASO-MASA-VALIDA", _round(_mass(association_valid)))
    rates = {}
    for afford in ("No", "Yes"):
        group = [row for row in association_valid if row["BNPL4_e"] == afford]
        group_mass = _mass(group)
        for late in ("No", "Yes"):
            cell = [row for row in group if row["BNPL3"] == late]
            put(f"ASEQ-ATRASO-CELDA-AF-{afford.upper()}-ATR-{late.upper()}-N", len(cell))
            put(f"ASEQ-ATRASO-CELDA-AF-{afford.upper()}-ATR-{late.upper()}-MASA", _round(_mass(cell)))
        rates[afford] = _mass([row for row in group if row["BNPL3"] == "Yes"]) / group_mass
        put(f"ASEQ-ATRASO-P-ATRASO-AF-{afford.upper()}", _round(rates[afford]))
    put("ASEQ-ATRASO-DIF-YES-MENOS-NO", _round(rates["Yes"] - rates["No"]))
    put("ASEQ-ATRASO-FALTANTES", _missing_text(missing["ASEQ-ATRASO"]))
    put("ASEQ-ATRASO-DEFINICION", DEFINITIONS["ASEQ-ATRASO"])
    return out


def medir(inputs, contrato):
    rows, width = _read_rows(inputs[INPUT_ID]["ruta_absoluta"])
    params = contrato.get("parametros") or {}
    expected_width = int(params.get("columnas_esperadas", 815))
    if width != expected_width:
        raise ValueError(f"N-COLUMNAS-INESPERADO:{width}!={expected_width}")
    return calculate(rows, width=width, expected_rows=int(params.get("filas_esperadas", 12934)))
