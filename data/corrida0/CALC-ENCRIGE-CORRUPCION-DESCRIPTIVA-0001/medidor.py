#!/usr/bin/env python3
"""Extrae tasas oficiales ENCRIGE 2020 por tamaño desde tabulados CSV."""
from __future__ import annotations

import csv
import hashlib
import io
import zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path


CALC_ID = "CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001"
INPUT_TABULADOS = "conjunto_de_datos_encrige_2020_csv"
INPUT_CUESTIONARIO = "encrige2020_cuestionario"
INPUT_DISENO = "gen2_encrige2020_diseno_muestral"
EXPECTED_SHA256 = {
    INPUT_TABULADOS: "06864904426a6b2c18cdad63a8b7bcb995fd35333c44448ba3fb5a973b822c5a",
    INPUT_CUESTIONARIO: "f410156bf5131921f6699b47f07fba302b168de187ea638a5f601732097cd8c1",
    INPUT_DISENO: "3f314258dc4ad0ddc5a4b94b327c763f3ff8c2abacf0bcac0a171519ce479961",
}
DOMAINS = ["Estados Unidos Mexicanos", "Micro", "Pequeña", "Mediana", "Grande"]
TABLE_DIR_MARKER = "/conjunto_de_datos_VI_Entorno_del_establecimiento_2020/"
RATE_TOLERANCE = Decimal("1e-9")
OUTPUT_COLUMNS = [
    "indicador_id", "indicador_nombre", "dominio_tipo", "dominio",
    "valor_original", "unidad_original", "transformacion",
    "valor_normalizado", "unidad_normalizada", "porcentaje_derivado",
    "numerador_publicado", "denominador_publicado",
    "unidad_numerador_denominador", "n_muestral",
    "incertidumbre_tipo", "incertidumbre_valor", "periodo",
    "cuadro", "localizador", "estado_celda", "nota_supresion",
    "procedencia", "uso",
]


def _read_input(entry: dict) -> bytes:
    raw = entry.get("bytes")
    if raw is not None:
        return raw
    return Path(entry["ruta_absoluta"]).read_bytes()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _collapse(value: str | None) -> str:
    return " ".join((value or "").replace("\xa0", " ").split())


def _member(zf: zipfile.ZipFile, basename: str) -> str:
    matches = [
        name for name in zf.namelist()
        if TABLE_DIR_MARKER in name and name.rsplit("/", 1)[-1] == basename
    ]
    if len(matches) != 1:
        raise ValueError(f"MIEMBRO-NO-UNIVOCO:{basename}:{matches}")
    return matches[0]


def _table(zf: zipfile.ZipFile, basename: str) -> tuple[list[dict[str, str]], list[str]]:
    raw = zf.read(_member(zf, basename))
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames:
        raise ValueError(f"SIN-CABECERA:{basename}")
    fields = [_collapse(field) for field in reader.fieldnames]
    rows = []
    for source in reader:
        rows.append({_collapse(key): _collapse(value) for key, value in source.items()})
    return rows, fields


def _find_field(fields: list[str], *needles: str) -> str:
    matches = [field for field in fields if all(needle in field for needle in needles)]
    if len(matches) != 1:
        raise ValueError(f"CAMPO-NO-UNIVOCO:{needles}:{matches}")
    return matches[0]


def _by_domain(rows: list[dict[str, str]], domain_field: str, table: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        domain = row.get(domain_field, "")
        if domain in DOMAINS:
            if domain in out:
                raise ValueError(f"DOMINIO-DUPLICADO:{table}:{domain}")
            out[domain] = row
    missing = [domain for domain in DOMAINS if domain not in out]
    if missing:
        raise ValueError(f"DOMINIOS-AUSENTES:{table}:{missing}")
    return out


def _decimal(value: str, locator: str) -> Decimal:
    if value == "":
        raise ValueError(f"CELDA-NO-DISPONIBLE:{locator}")
    try:
        result = Decimal(value.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"CELDA-NO-NUMERICA:{locator}:{value}") from exc
    if not result.is_finite():
        raise ValueError(f"CELDA-NO-FINITA:{locator}:{value}")
    return result


def normaliza_tasa_por_10000(value: Decimal) -> Decimal:
    """Convierte una tasa por 10 000 a razón por una unidad."""
    return value / Decimal(10_000)


def _fmt(value: Decimal) -> str:
    return f"{value:.12f}"


def _assert_rate(numerator: Decimal, denominator: Decimal, rate: Decimal, locator: str) -> Decimal:
    if denominator <= 0 or numerator < 0:
        raise ValueError(f"NUMERADOR-DENOMINADOR-INVALIDO:{locator}")
    delta = abs(numerator / denominator * Decimal(10_000) - rate)
    if delta > RATE_TOLERANCE:
        raise ValueError(f"TASA-INCONSISTENTE:{locator}:delta={delta}")
    return delta


def _base_row(indicator_id: str, indicator_name: str, domain: str) -> dict[str, str]:
    return {
        "indicador_id": indicator_id,
        "indicador_nombre": indicator_name,
        "dominio_tipo": "nacional" if domain == DOMAINS[0] else "tamaño oficial",
        "dominio": domain,
        "unidad_numerador_denominador": "unidades expandidas",
        "n_muestral": "NO-PUBLICADO",
        "incertidumbre_tipo": "NO-DISPONIBLE-EN-REPRESENTACION-CSV",
        "incertidumbre_valor": "",
        "periodo": "Durante 2020 (enero a la fecha de entrevista)",
        "estado_celda": "PUBLICADA-NUMERICA",
        "nota_supresion": "Sin símbolo de supresión; una celda vacía no se convertiría en cero.",
        "procedencia": "INEGI, ENCRIGE 2020, tabulados oficiales CSV",
        "uso": "CONTEXTO-INFORME-NO-CALIBRA;UNIDAD-DISTINTA-NO-TRANSFERENCIA",
    }


def extraer(raw_zip: bytes) -> tuple[list[dict[str, str]], dict[str, Decimal]]:
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
        corrupt = zf.testzip()
        if corrupt is not None:
            raise ValueError(f"ZIP-CORRUPTO:{corrupt}")
        rows33, fields33 = _table(zf, "t6_33.csv")
        rows36, fields36 = _table(zf, "t6_36.csv")
        rows41, fields41 = _table(zf, "t6_41.csv")

    domain33 = _find_field(fields33, "Tamaño")
    den33 = _find_field(fields33, "Total de unidades económicas", "trámite", "inspección")
    num33 = _find_field(fields33, "Participación en al menos un acto de corrupción", "Absolutos")
    rate33 = _find_field(fields33, "Participación en al menos un acto de corrupción", "Tasa de prevalencia")
    domain36 = _find_field(fields36, "Tamaño")
    check36 = _find_field(fields36, "Tasa de prevalencia", "a nivel nacional")
    domain41 = _find_field(fields41, "Tamaño")
    den41 = _find_field(fields41, "Total de unidades económicas", "trámite", "inspección")
    num41 = _find_field(fields41, "Total de trámites o inspecciones con experiencia de corrupción")
    rate41 = _find_field(fields41, "Tasa de incidencia")

    by33 = _by_domain(rows33, domain33, "t6_33.csv")
    by36 = _by_domain(rows36, domain36, "t6_36.csv")
    by41 = _by_domain(rows41, domain41, "t6_41.csv")
    output: list[dict[str, str]] = []
    formula_deltas: list[Decimal] = []
    cross_deltas: list[Decimal] = []

    for domain in DOMAINS:
        denominator = _decimal(by33[domain][den33], f"t6_33:{domain}:denominador")
        numerator = _decimal(by33[domain][num33], f"t6_33:{domain}:numerador")
        rate = _decimal(by33[domain][rate33], f"t6_33:{domain}:tasa")
        formula_deltas.append(_assert_rate(numerator, denominator, rate, f"t6_33:{domain}"))
        check_rate = _decimal(by36[domain][check36], f"t6_36:{domain}:tasa")
        cross_delta = abs(check_rate - rate)
        if cross_delta > RATE_TOLERANCE:
            raise ValueError(f"LECTURA-DOBLE-DISCREPA:{domain}:delta={cross_delta}")
        cross_deltas.append(cross_delta)
        normalized = normaliza_tasa_por_10000(rate)
        row = _base_row(
            "PREVALENCIA-EXPERIENCIA-CORRUPCION",
            "Tasa de prevalencia de unidades económicas que experimentaron al menos un acto de corrupción",
            domain,
        )
        row.update({
            "valor_original": by33[domain][rate33],
            "unidad_original": "por 10 000 unidades económicas expuestas",
            "transformacion": "valor_original / 10000",
            "valor_normalizado": _fmt(normalized),
            "unidad_normalizada": "proporción de unidades económicas expuestas",
            "porcentaje_derivado": _fmt(normalized * Decimal(100)),
            "numerador_publicado": by33[domain][num33],
            "denominador_publicado": by33[domain][den33],
            "cuadro": "t6_33 (contraste de tasa: t6_36)",
            "localizador": f"t6_33.csv; fila={domain}; columnas=Participación...Absolutos/Tasa de prevalencia",
        })
        output.append(row)

    for domain in DOMAINS:
        denominator = _decimal(by41[domain][den41], f"t6_41:{domain}:denominador")
        numerator = _decimal(by41[domain][num41], f"t6_41:{domain}:numerador")
        rate = _decimal(by41[domain][rate41], f"t6_41:{domain}:tasa")
        formula_deltas.append(_assert_rate(numerator, denominator, rate, f"t6_41:{domain}"))
        normalized = normaliza_tasa_por_10000(rate)
        row = _base_row(
            "INCIDENCIA-EXPERIENCIAS-CORRUPCION",
            "Tasa de incidencia de trámites o inspecciones con experiencia de corrupción",
            domain,
        )
        row.update({
            "valor_original": by41[domain][rate41],
            "unidad_original": "experiencias por 10 000 unidades económicas expuestas",
            "transformacion": "valor_original / 10000",
            "valor_normalizado": _fmt(normalized),
            "unidad_normalizada": "experiencias por unidad económica expuesta",
            "porcentaje_derivado": "NO-APLICA",
            "numerador_publicado": by41[domain][num41],
            "denominador_publicado": by41[domain][den41],
            "cuadro": "t6_41",
            "localizador": f"t6_41.csv; fila={domain}; columnas=Total de trámites.../Tasa de incidencia",
        })
        output.append(row)

    metrics = {
        "max_formula_delta": max(formula_deltas),
        "max_cross_read_delta": max(cross_deltas),
    }
    return output, metrics


def _serialize(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def _write_output(raw: bytes) -> Path:
    repo = Path(__file__).resolve().parents[3]
    output = repo / "forense" / "analisis" / "encrige-descriptiva-1" / "encrige-corrupcion-por-tamano.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    return output


def medir(inputs: dict, contrato: dict) -> dict:
    raw_inputs = {key: _read_input(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        actual = _sha256(raw_inputs[key])
        if actual != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{actual}")
    if not raw_inputs[INPUT_CUESTIONARIO].startswith(b"%PDF"):
        raise ValueError("CUESTIONARIO-NO-PDF")
    if not raw_inputs[INPUT_DISENO].startswith(b"%PDF"):
        raise ValueError("DISENO-NO-PDF")

    rows, metrics = extraer(raw_inputs[INPUT_TABULADOS])
    serialized = _serialize(rows)
    output = _write_output(serialized)
    prevalence = [row for row in rows if row["indicador_id"].startswith("PREVALENCIA")]
    incidence = [row for row in rows if row["indicador_id"].startswith("INCIDENCIA")]
    return {
        "RESULT-ENCRIGE-DES-G-INPUT-TABULADOS-SHA256": _sha256(raw_inputs[INPUT_TABULADOS]),
        "RESULT-ENCRIGE-DES-G-INPUT-CUESTIONARIO-SHA256": _sha256(raw_inputs[INPUT_CUESTIONARIO]),
        "RESULT-ENCRIGE-DES-G-INPUT-DISENO-SHA256": _sha256(raw_inputs[INPUT_DISENO]),
        "RESULT-ENCRIGE-DES-G-N-INDICADORES": 2,
        "RESULT-ENCRIGE-DES-G-N-DOMINIOS": len(DOMAINS),
        "RESULT-ENCRIGE-DES-G-N-FILAS-SALIDA": len(rows),
        "RESULT-ENCRIGE-DES-G-MAX-DELTA-FORMULA": float(metrics["max_formula_delta"]),
        "RESULT-ENCRIGE-DES-G-MAX-DELTA-DOBLE-LECTURA": float(metrics["max_cross_read_delta"]),
        "RESULT-ENCRIGE-DES-G-CSV-SHA256": _sha256(serialized),
        "RESULT-ENCRIGE-DES-PREVALENCIA-TOTAL-PROPORCION": float(Decimal(prevalence[0]["valor_normalizado"])),
        "RESULT-ENCRIGE-DES-INCIDENCIA-TOTAL-POR-UNIDAD": float(Decimal(incidence[0]["valor_normalizado"])),
        "RESULT-ENCRIGE-DES-G-N-MUESTRAL": "NO-PUBLICADO",
        "RESULT-ENCRIGE-DES-G-INCERTIDUMBRE": "NO-DISPONIBLE-EN-REPRESENTACION-CSV",
        "RESULT-ENCRIGE-DES-G-USO": "CONTEXTO-INFORME-NO-CALIBRA;UNIDAD-DISTINTA-NO-TRANSFERENCIA",
        "RESULT-ENCRIGE-DES-G-SALIDA": str(output.relative_to(Path(__file__).resolve().parents[3])),
    }
