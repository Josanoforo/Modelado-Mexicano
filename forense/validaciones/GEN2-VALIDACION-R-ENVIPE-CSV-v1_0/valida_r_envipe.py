#!/usr/bin/env python3
"""Reconstrucción independiente de CIV-M-10/-12/-13 desde ENVIPE CSV.

No importa los medidores congelados, arbitra, valida_envipe_independiente ni
tests.svystat. La aritmética implementa el PROTOCOLO.md vecino.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path


getcontext().prec = 50
Z_975 = 1.959963984540054
POINT_TOL = 1e-12
SE_CV_TOL = 1e-10
IC_TOL = 2e-10
POSITIVE = frozenset({1, 2, 6})
NEGATIVE = frozenset({3, 4, 5, 7, 8, 9})
VALID_RESPONSE = POSITIVE | NEGATIVE
VALID_CRIME = frozenset(range(1, 16))
FUNNEL_KEYS = (
    "filas_tabla",
    "filas_tabla_sin_diseno",
    "descarta_bpcod_fuera_01_15",
    "pasa_bpcod_01_15",
    "descarta_bp1_23_99",
    "descarta_bp1_23_blanco",
    "descarta_bp1_23_otro",
    "pasa_bp1_23_01_09",
    "descarta_fac_del_no_positivo_o_no_finito",
    "pasa_fac_del",
    "incluida_sin_diseno",
    "n_u_r",
)


@dataclass(frozen=True)
class Wave:
    cell: str
    survey: int
    fact_year: int
    payload_id: str
    archive: str
    archive_sha256: str
    data_member: str
    dictionary_member: str
    catalog_member: str
    dwelling_member: str
    questionnaire: str
    questionnaire_id: str
    questionnaire_sha256: str
    descriptor: str
    descriptor_id: str
    descriptor_sha256: str
    official_sample_dwellings: int
    design_upc: str
    design_pdf_sha256_2026_09_11: str


WAVES = (
    Wave(
        "CIV-M-10",
        2021,
        2020,
        "envipe2021_csv",
        "envipe2021_csv.zip",
        "88153c67ff3666be511dab3f3b483226a0af9f0e8683bd8dbfba8d616ddbfdd1",
        "conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv",
        "conjunto_de_datos_TMod_Vic_ENVIPE_2021/diccionario_de_datos/diccionario_de_datos_TMod_Vic_ENVIPE_2021.csv",
        "conjunto_de_datos_TMod_Vic_ENVIPE_2021/catalogos/BP1_23.csv",
        "conjunto_de_datos_TVivienda_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TVivienda_ENVIPE_2021.csv",
        "cuest_modulo_envipe2021.pdf",
        "envipe2021_cuest_modulo_pdf",
        "390ef00ec15cabb9dcdf86d9fa79e108cea4ef1a2e8fdfcf4f4c409794636e0c",
        "fd_envipe2021.pdf",
        "envipe2021_fd_pdf",
        "d85775241d6f427d6dd6643bce973ed0bdbfca4e0b0d6a9b02265e8327179945",
        102297,
        "889463902454",
        "090da555cfcf132035dc4fedb30c311376ab200439837c9d29068b3eeaefd6a4",
    ),
    Wave(
        "CIV-M-12",
        2023,
        2022,
        "envipe2023_csv",
        "envipe2023_csv.zip",
        "0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404",
        "tmod_vic_envipe2023/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2023.csv",
        "tmod_vic_envipe2023/diccionario_de_datos/diccionario_de_datos_tmod_vic_envipe2023.csv",
        "tmod_vic_envipe2023/catalogos/bp1_23.csv",
        "tvivienda_envipe2023/conjunto_de_datos/conjunto_de_datos_tvivienda_envipe2023.csv",
        "cuest_modulo_envipe2023.pdf",
        "envipe2023_cuest_modulo_pdf",
        "98d3c632cc038c4a9a1ff129efb63f6d1ac786f46e4886aaaf5aff92b4cdf5b4",
        "fd_envipe2023.pdf",
        "envipe2023_fd_pdf",
        "743c260e89a6c5d6f2fcc6eac0f1884c40bc6b437164b34e13ba6fe1caf1be63",
        102362,
        "889463912637",
        "2031d7d5a0999c5356b63fe151c7e049fe5921a133bf6234b0f933dcb166f745",
    ),
    Wave(
        "CIV-M-13",
        2024,
        2023,
        "envipe2024_csv",
        "envipe2024_csv.zip",
        "90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2",
        "tmod_vic_envipe2024/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2024.csv",
        "tmod_vic_envipe2024/diccionario_de_datos/diccionario_de_datos_tmod_vic_envipe2024.csv",
        "tmod_vic_envipe2024/catalogos/bp1_23.csv",
        "tvivienda_envipe2024/conjunto_de_datos/conjunto_de_datos_tvivienda_envipe2024.csv",
        "cuest_modulo_envipe2024.pdf",
        "envipe2024_cuest_modulo_pdf",
        "7628127d5e9bd4424737f7a8cb60bbded28e21c2242d1f412c86367e03836e28",
        "fd_envipe2024.pdf",
        "envipe2024_fd_pdf",
        "f8d72038595746ceac21e5096462b277e757d7501bd3a1b61ac86bf9fc0d57d5",
        102287,
        "889463920014",
        "a366d2a2fdccad18991de5d0a447341267808948018e3f3ec8bbed8d2d6dc6f6",
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_csv(blob: bytes) -> tuple[str, str]:
    try:
        return blob.decode("utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        return blob.decode("latin-1"), "latin-1"


def member_blob(archive: zipfile.ZipFile, expected: str) -> bytes:
    matches = [name for name in archive.namelist() if name == expected]
    if len(matches) != 1:
        raise ValueError(f"{expected!r}: se esperaba un miembro literal y hubo {len(matches)}")
    return archive.read(matches[0])


def rows_from_blob(blob: bytes) -> tuple[list[dict[str, str]], str]:
    text, encoding = decode_csv(blob)
    rows = list(csv.DictReader(io.StringIO(text, newline="")))
    return rows, encoding


def uppercase_row(row: dict[str, str]) -> dict[str, str]:
    return {str(key).upper(): value for key, value in row.items()}


def integer(value: object) -> int | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    return int(number) if number == number.to_integral_value() else None


def positive_weight(value: object) -> Decimal | None:
    if value is None:
        return None
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    return number if number.is_finite() and number > 0 else None


def response_label(value: object) -> str:
    parsed = integer(value)
    if parsed is not None:
        return f"{parsed:02d}"
    text = "" if value is None else str(value)
    return "BLANCO" if not text.strip() or text.strip().casefold() == "b" else f"OTRO:{text.strip()}"


def opaque_key(value: object) -> str:
    return "" if value is None else str(value)


def empty_key(value: object) -> bool:
    return value is None or not str(value).strip()


def measure_rows(rows: list[dict[str, str]]) -> dict:
    funnel = Counter()
    frequencies = Counter()
    bpcod_frequencies = Counter()
    numerator = Decimal(0)
    denominator = Decimal(0)
    included_design: list[tuple[str, str, Decimal, int]] = []
    full_tmod_psus: dict[str, set[str]] = defaultdict(set)
    included_people = Counter()
    included_crimes = Counter()

    for raw in rows:
        row = uppercase_row(raw)
        missing = {name for name in ("ID_PER", "ID_DEL", "BPCOD", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS") if name not in row}
        if missing:
            raise ValueError(f"columnas ausentes: {sorted(missing)}")
        funnel["filas_tabla"] += 1
        frequencies[response_label(row["BP1_23"])] += 1
        bpcod_frequencies[response_label(row["BPCOD"])] += 1

        stratum = opaque_key(row["EST_DIS"])
        psu = opaque_key(row["UPM_DIS"])
        if empty_key(stratum) or empty_key(psu):
            funnel["filas_tabla_sin_diseno"] += 1
        else:
            full_tmod_psus[stratum].add(psu)

        crime = integer(row["BPCOD"])
        if crime not in VALID_CRIME:
            funnel["descarta_bpcod_fuera_01_15"] += 1
            continue
        funnel["pasa_bpcod_01_15"] += 1

        response = integer(row["BP1_23"])
        if response not in VALID_RESPONSE:
            if response == 99:
                funnel["descarta_bp1_23_99"] += 1
            elif response_label(row["BP1_23"]) == "BLANCO":
                funnel["descarta_bp1_23_blanco"] += 1
            else:
                funnel["descarta_bp1_23_otro"] += 1
            continue
        funnel["pasa_bp1_23_01_09"] += 1

        weight = positive_weight(row["FAC_DEL"])
        if weight is None:
            funnel["descarta_fac_del_no_positivo_o_no_finito"] += 1
            continue
        funnel["pasa_fac_del"] += 1

        outcome = 1 if response in POSITIVE else 0
        numerator += weight * outcome
        denominator += weight
        included_design.append((stratum, psu, weight, outcome))
        included_people[opaque_key(row["ID_PER"])] += 1
        included_crimes[opaque_key(row["ID_DEL"])] += 1
        if empty_key(stratum) or empty_key(psu):
            funnel["incluida_sin_diseno"] += 1

    if not denominator:
        raise ValueError("universo U_R vacío o sin masa ponderada")
    point_decimal = numerator / denominator
    point = float(point_decimal)
    funnel["n_u_r"] = len(included_design)
    for key in FUNNEL_KEYS:
        funnel[key] += 0
    return {
        "funnel": dict(sorted(funnel.items())),
        "frequencies": dict(sorted(frequencies.items())),
        "bpcod_frequencies": dict(sorted(bpcod_frequencies.items())),
        "numerator": numerator,
        "denominator": denominator,
        "point_decimal": point_decimal,
        "point": point,
        "included_design": included_design,
        "full_tmod_psus": full_tmod_psus,
        "n_personas": len(included_people),
        "n_personas_con_varios_delitos": sum(count > 1 for count in included_people.values()),
        "max_delitos_por_persona": max(included_people.values(), default=0),
        "n_id_del_distintos": len(included_crimes),
        "n_id_del_repetidos": sum(count > 1 for count in included_crimes.values()),
    }


def psu_scores(design_rows: list[tuple[str, str, Decimal, int]], point: float) -> dict[tuple[str, str], float]:
    terms: dict[tuple[str, str], list[float]] = defaultdict(list)
    for stratum, psu, weight, outcome in design_rows:
        terms[(stratum, psu)].append(float(weight) * (outcome - point))
    return {key: math.fsum(values) for key, values in terms.items()}


def variance_from_frame(
    scores: dict[tuple[str, str], float],
    denominator: Decimal,
    frame: dict[str, set[str]] | None = None,
) -> dict:
    if frame is None:
        frame = defaultdict(set)
        for stratum, psu in scores:
            frame[stratum].add(psu)
    variance_total = 0.0
    singleton = 0
    for stratum in sorted(frame):
        values = [scores.get((stratum, psu), 0.0) for psu in sorted(frame[stratum])]
        size = len(values)
        if size == 1:
            singleton += 1
            continue
        if not size:
            continue
        mean = math.fsum(values) / size
        squared = math.fsum((value - mean) ** 2 for value in values)
        variance_total += size / (size - 1) * squared
    variance = variance_total / float(denominator) ** 2
    return {
        "variance": variance,
        "se": math.sqrt(variance),
        "n_strata": len(frame),
        "n_psu": sum(len(psus) for psus in frame.values()),
        "n_singleton_strata": singleton,
    }


def interval(point: float, se: float) -> tuple[float, float]:
    return max(0.0, point - Z_975 * se), min(1.0, point + Z_975 * se)


def dwelling_scope(rows: list[dict[str, str]]) -> dict:
    scope: dict[str, set[str]] = defaultdict(set)
    ids = Counter()
    missing_design = 0
    for raw in rows:
        row = uppercase_row(raw)
        missing = {name for name in ("ID_VIV", "EST_DIS", "UPM_DIS") if name not in row}
        if missing:
            raise ValueError(f"TVivienda columnas ausentes: {sorted(missing)}")
        ids[opaque_key(row["ID_VIV"])] += 1
        stratum = opaque_key(row["EST_DIS"])
        psu = opaque_key(row["UPM_DIS"])
        if empty_key(stratum) or empty_key(psu):
            missing_design += 1
        else:
            scope[stratum].add(psu)
    return {
        "scope": scope,
        "n_rows": len(rows),
        "n_distinct_id_viv": len(ids),
        "n_repeated_id_viv": sum(count > 1 for count in ids.values()),
        "n_missing_design": missing_design,
    }


def singleton_diagnostics(
    domain_scope: dict[str, set[str]],
    tmod_scope: dict[str, set[str]],
    dwelling: dict,
) -> dict:
    dwelling_scope_map = dwelling["scope"]
    domain_singletons = [stratum for stratum, psus in domain_scope.items() if len(psus) == 1]
    profile = Counter()
    for stratum in domain_singletons:
        tmod_n = len(tmod_scope.get(stratum, set()))
        dwelling_n = len(dwelling_scope_map.get(stratum, set()))
        if dwelling_n > 1:
            classification = "creado_por_restriccion_u_r"
        elif dwelling_n == 1:
            classification = "persiste_en_tvivienda_sin_acreditacion_de_certeza"
        else:
            classification = "estrato_no_encontrado_en_tvivienda"
        profile[(classification, tmod_n, dwelling_n)] += 1

    domain_keys = {(stratum, psu) for stratum, psus in domain_scope.items() for psu in psus}
    tmod_keys = {(stratum, psu) for stratum, psus in tmod_scope.items() for psu in psus}
    dwelling_keys = {(stratum, psu) for stratum, psus in dwelling_scope_map.items() for psu in psus}
    return {
        "n_singletons_u_r": len(domain_singletons),
        "n_singletons_u_r_creados_por_restriccion": sum(
            count for (kind, _, _), count in profile.items() if kind == "creado_por_restriccion_u_r"
        ),
        "n_singletons_u_r_persisten_tvivienda": sum(
            count
            for (kind, _, _), count in profile.items()
            if kind == "persiste_en_tvivienda_sin_acreditacion_de_certeza"
        ),
        "n_singletons_tmod_completo": sum(len(psus) == 1 for psus in tmod_scope.values()),
        "n_singletons_tvivienda": sum(len(psus) == 1 for psus in dwelling_scope_map.values()),
        "n_upm_u_r": len(domain_keys),
        "n_upm_tmod_completo": len(tmod_keys),
        "n_upm_tvivienda": len(dwelling_keys),
        "n_upm_u_r_ausentes_tvivienda": len(domain_keys - dwelling_keys),
        "n_upm_tmod_ausentes_tvivienda": len(tmod_keys - dwelling_keys),
        "n_upm_adicionales_tmod_vs_u_r": len(tmod_keys - domain_keys),
        "n_upm_adicionales_tvivienda_vs_u_r": len(dwelling_keys - domain_keys),
        "perfil_singletons_u_r": [
            {
                "clasificacion": kind,
                "upm_en_tmod_completo": tmod_n,
                "upm_en_tvivienda": dwelling_n,
                "n_estratos": count,
            }
            for (kind, tmod_n, dwelling_n), count in sorted(profile.items())
        ],
    }


def exact_document(path: Path, expected_sha256: str, source_id: str) -> dict:
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError(f"{source_id}: hash {actual} != {expected_sha256}")
    return {"id": source_id, "archivo": path.name, "sha256": actual, "bytes": path.stat().st_size}


def catalog_evidence(blob: bytes) -> tuple[dict, str]:
    rows, encoding = rows_from_blob(blob)
    labels = {}
    for raw in rows:
        row = uppercase_row(raw)
        code_value = integer(row.get("BP1_23"))
        if code_value is not None:
            labels[f"{code_value:02d}"] = str(row.get("DESCRIP", "")).strip()
    expected = {f"{value:02d}" for value in range(1, 10)} | {"99"}
    if set(labels) != expected:
        raise ValueError(f"catálogo BP1_23: códigos {sorted(labels)}, esperados {sorted(expected)}")
    return labels, encoding


def dictionary_evidence(blob: bytes) -> tuple[dict, str]:
    rows, encoding = rows_from_blob(blob)
    selected = {}
    for raw in rows:
        row = uppercase_row(raw)
        mnemonic = str(row.get("NEMONICO", "")).strip().upper()
        if mnemonic in {"ID_PER", "ID_DEL", "BPCOD", "BP1_23", "FAC_DEL", "FAC_DEL_AM", "EST_DIS", "UPM_DIS"}:
            selected[mnemonic] = {
                "nombre": str(row.get("NOMBRE_CAMPO", "")).strip(),
                "tipo": str(row.get("TIPO", "")).strip(),
                "longitud": str(row.get("LONGITUD", "")).strip(),
                "rango": " ".join(str(row.get("RANGO_CLAVES", "")).split()),
            }
    required = {"ID_PER", "ID_DEL", "BPCOD", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS"}
    if required - set(selected):
        raise ValueError(f"diccionario: variables ausentes {sorted(required - set(selected))}")
    return selected, encoding


def reference_values(repo: Path, cell: str) -> dict:
    results_path = repo / f"data/corrida0/CALC-R-{cell}/resultados.json"
    results = json.loads(results_path.read_text(encoding="utf-8"))["resultados"]
    prefix = f"RESULT-R-{cell}"
    return {
        "path": str(results_path.relative_to(repo)),
        "sha256": sha256_file(results_path),
        "n": int(results[f"{prefix}-N"]),
        "denominator": float(results[f"{prefix}-MASA-FAC-DEL"]),
        "point": float(results[f"{prefix}-PUNTO"]),
        "se": float(results[f"{prefix}-EE"]),
        "ic_lo": float(results[f"{prefix}-IC-LO"]),
        "ic_hi": float(results[f"{prefix}-IC-HI"]),
        "cv": float(results[f"{prefix}-CV"]),
        "n_strata": int(results[f"{prefix}-N-ESTRATOS"]),
        "n_psu": int(results[f"{prefix}-N-UPM"]),
        "n_singleton_strata": int(results[f"{prefix}-N-ESTRATOS-UPM-UNICA"]),
    }


def compare_reference(measurement: dict, historical: dict, reference: dict) -> dict:
    hist_lo, hist_hi = interval(measurement["point"], historical["se"])
    cv = historical["se"] / measurement["point"]
    differences = {
        "n": measurement["funnel"]["n_u_r"] - reference["n"],
        "denominator": float(measurement["denominator"]) - reference["denominator"],
        "point": measurement["point"] - reference["point"],
        "se": historical["se"] - reference["se"],
        "ic_lo": hist_lo - reference["ic_lo"],
        "ic_hi": hist_hi - reference["ic_hi"],
        "cv": cv - reference["cv"],
        "n_strata": historical["n_strata"] - reference["n_strata"],
        "n_psu": historical["n_psu"] - reference["n_psu"],
        "n_singleton_strata": historical["n_singleton_strata"] - reference["n_singleton_strata"],
    }
    agrees = (
        differences["n"] == 0
        and differences["denominator"] == 0
        and abs(differences["point"]) <= POINT_TOL
        and abs(differences["se"]) <= SE_CV_TOL
        and abs(differences["ic_lo"]) <= IC_TOL
        and abs(differences["ic_hi"]) <= IC_TOL
        and abs(differences["cv"]) <= SE_CV_TOL
        and differences["n_strata"] == 0
        and differences["n_psu"] == 0
        and differences["n_singleton_strata"] == 0
    )
    return {
        "historical_reconstructed": {
            "se": historical["se"],
            "ic_lo": hist_lo,
            "ic_hi": hist_hi,
            "cv": cv,
            "n_strata": historical["n_strata"],
            "n_psu": historical["n_psu"],
            "n_singleton_strata": historical["n_singleton_strata"],
        },
        "producer": reference,
        "differences_validator_minus_producer": differences,
        "concordancia_numerica": "CONCUERDA" if agrees else "DIFIERE",
    }


def validate_wave(repo: Path, raw_root: Path, wave: Wave) -> dict:
    archive_path = raw_root / wave.archive
    archive_hash = sha256_file(archive_path)
    if archive_hash != wave.archive_sha256:
        raise ValueError(f"{wave.payload_id}: hash {archive_hash} != {wave.archive_sha256}")

    questionnaire = exact_document(raw_root / wave.questionnaire, wave.questionnaire_sha256, wave.questionnaire_id)
    descriptor = exact_document(raw_root / wave.descriptor, wave.descriptor_sha256, wave.descriptor_id)

    with zipfile.ZipFile(archive_path) as archive:
        data_blob = member_blob(archive, wave.data_member)
        dictionary_blob = member_blob(archive, wave.dictionary_member)
        catalog_blob = member_blob(archive, wave.catalog_member)
        dwelling_blob = member_blob(archive, wave.dwelling_member)

    data_rows, data_encoding = rows_from_blob(data_blob)
    dwelling_rows, dwelling_encoding = rows_from_blob(dwelling_blob)
    dictionary, dictionary_encoding = dictionary_evidence(dictionary_blob)
    catalog, catalog_encoding = catalog_evidence(catalog_blob)
    measurement = measure_rows(data_rows)
    dwelling = dwelling_scope(dwelling_rows)

    scores = psu_scores(measurement["included_design"], measurement["point"])
    historical = variance_from_frame(scores, measurement["denominator"])
    domain_scope: dict[str, set[str]] = defaultdict(set)
    for stratum, psu in scores:
        domain_scope[stratum].add(psu)
    diagnostics = singleton_diagnostics(domain_scope, measurement["full_tmod_psus"], dwelling)

    if diagnostics["n_upm_u_r_ausentes_tvivienda"]:
        domain_aware = None
        inferential = "NO-ACREDITADA-UPM-U_R-AUSENTE-DE-TVIVIENDA"
    else:
        domain_aware = variance_from_frame(scores, measurement["denominator"], dwelling["scope"])
        domain_lo, domain_hi = interval(measurement["point"], domain_aware["se"])
        domain_aware.update({"ic_lo": domain_lo, "ic_hi": domain_hi, "cv": domain_aware["se"] / measurement["point"]})
        complete_dwelling_frame = (
            dwelling["n_rows"] == wave.official_sample_dwellings
            and dwelling["n_distinct_id_viv"] == wave.official_sample_dwellings
            and dwelling["n_repeated_id_viv"] == 0
            and dwelling["n_missing_design"] == 0
        )
        if not complete_dwelling_frame:
            inferential = "NO-ACREDITADA-TVIVIENDA-NO-COINCIDE-CON-MUESTRA-OFICIAL"
        elif diagnostics["n_singletons_tvivienda"]:
            inferential = "NO-ACREDITADA-SINGLETON-PERSISTE-SIN-CERTEZA-DOCUMENTADA"
        else:
            inferential = "APTA-CON-SUCESOR-DOMINIO-TVIVIENDA; HISTORICA-SOLO-CONCORDANCIA-NUMERICA"

    reference = reference_values(repo, wave.cell)
    comparison = compare_reference(measurement, historical, reference)
    point_valid = (
        comparison["differences_validator_minus_producer"]["n"] == 0
        and comparison["differences_validator_minus_producer"]["denominator"] == 0
        and abs(comparison["differences_validator_minus_producer"]["point"]) <= POINT_TOL
    )

    return {
        "cell": wave.cell,
        "survey": wave.survey,
        "fact_year": wave.fact_year,
        "source": {
            "payload_id": wave.payload_id,
            "archive": wave.archive,
            "archive_sha256": archive_hash,
            "archive_bytes": archive_path.stat().st_size,
            "data_member": wave.data_member,
            "data_member_sha256": hashlib.sha256(data_blob).hexdigest(),
            "data_encoding": data_encoding,
            "dictionary_member": wave.dictionary_member,
            "dictionary_member_sha256": hashlib.sha256(dictionary_blob).hexdigest(),
            "dictionary_encoding": dictionary_encoding,
            "dictionary_variables": dictionary,
            "catalog_member": wave.catalog_member,
            "catalog_member_sha256": hashlib.sha256(catalog_blob).hexdigest(),
            "catalog_encoding": catalog_encoding,
            "catalog_bp1_23": catalog,
            "dwelling_member": wave.dwelling_member,
            "dwelling_member_sha256": hashlib.sha256(dwelling_blob).hexdigest(),
            "dwelling_encoding": dwelling_encoding,
            "questionnaire": questionnaire,
            "questionnaire_reactive": "pregunta 1.23, página PDF 4; códigos 01..09 y 99 contrastados con catálogo",
            "descriptor": descriptor,
            "official_design": {
                "upc": wave.design_upc,
                "url": f"https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/{wave.design_upc}.pdf",
                "retrieval_sha256_2026_09_11": wave.design_pdf_sha256_2026_09_11,
                "official_sample_dwellings": wave.official_sample_dwellings,
            },
        },
        "measurement": {
            "unit": "DELITO",
            "n": measurement["funnel"]["n_u_r"],
            "weighted_numerator": str(measurement["numerator"]),
            "weighted_denominator": str(measurement["denominator"]),
            "point_decimal": str(measurement["point_decimal"]),
            "point": measurement["point"],
            "funnel": measurement["funnel"],
            "bp1_23_frequencies": measurement["frequencies"],
            "bpcod_frequencies": measurement["bpcod_frequencies"],
            "n_personas": measurement["n_personas"],
            "n_personas_con_varios_delitos": measurement["n_personas_con_varios_delitos"],
            "max_delitos_por_persona": measurement["max_delitos_por_persona"],
            "n_id_del_distintos": measurement["n_id_del_distintos"],
            "n_id_del_repetidos": measurement["n_id_del_repetidos"],
        },
        "comparison": comparison,
        "design_diagnostics": {
            **diagnostics,
            "tvivienda": {key: value for key, value in dwelling.items() if key != "scope"},
            "official_sample_dwellings": wave.official_sample_dwellings,
            "domain_aware_tvivienda": domain_aware,
        },
        "verdicts": {
            "concordancia_numerica": comparison["concordancia_numerica"],
            "validacion_punto": "VALIDADO" if point_valid else "NO-VALIDADO",
            "aptitud_inferencial": inferential,
        },
    }


def self_tests() -> list[dict]:
    def row(person: str, crime_id: str, crime: str, response: str, weight: str, stratum: str, psu: str) -> dict[str, str]:
        return {
            "ID_PER": person,
            "ID_DEL": crime_id,
            "BPCOD": crime,
            "BP1_23": response,
            "FAC_DEL": weight,
            "EST_DIS": stratum,
            "UPM_DIS": psu,
        }

    results = []
    unequal = measure_rows([row("p1", "d1", "01", "01", "1", "A", "1"), row("p2", "d2", "02", "03", "3", "A", "2")])
    assert unequal["numerator"] == Decimal(1)
    assert unequal["denominator"] == Decimal(4)
    assert unequal["point_decimal"] == Decimal("0.25")
    results.append({"case": "pesos_desiguales", "status": "OK", "point": "0.25"})

    exclusions = measure_rows(
        [
            row("p1", "d1", "01", "01", "1", "A", "1"),
            row("p1", "d2", "02", "03", "1", "A", "2"),
            row("p2", "d3", "03", "99", "1", "A", "3"),
            row("p3", "d4", "04", "b", "1", "A", "4"),
            row("p4", "d5", "16", "01", "1", "A", "5"),
            row("p5", "d6", "05", "06", "0", "A", "6"),
        ]
    )
    assert exclusions["funnel"]["descarta_bp1_23_99"] == 1
    assert exclusions["funnel"]["descarta_bp1_23_blanco"] == 1
    assert exclusions["funnel"]["descarta_bpcod_fuera_01_15"] == 1
    assert exclusions["funnel"]["descarta_fac_del_no_positivo_o_no_finito"] == 1
    assert exclusions["funnel"]["n_u_r"] == 2
    assert exclusions["n_personas_con_varios_delitos"] == 1
    results.append({"case": "exclusiones_y_varios_delitos", "status": "OK", "n": 2})

    variance_rows = [
        ("A", "1", Decimal(1), 1),
        ("A", "2", Decimal(1), 0),
        ("B", "3", Decimal(2), 1),
    ]
    scores = psu_scores(variance_rows, 0.75)
    historical = variance_from_frame(scores, Decimal(4))
    assert abs(historical["variance"] - 0.0625) < 1e-15
    assert abs(historical["se"] - 0.25) < 1e-15
    assert historical["n_singleton_strata"] == 1
    results.append({"case": "estratos_upm_y_singleton", "status": "OK", "variance": 0.0625, "se": 0.25})

    two_scores = {("A", "1"): 0.5, ("A", "2"): -0.5}
    two = variance_from_frame(two_scores, Decimal(2), {"A": {"1", "2"}})
    three = variance_from_frame(two_scores, Decimal(2), {"A": {"1", "2", "3"}})
    assert abs(two["se"] - 0.5) < 1e-15
    assert abs(three["variance"] - 0.1875) < 1e-15
    assert abs(three["se"] - math.sqrt(0.1875)) < 1e-15
    results.append({"case": "upm_cero_no_impone_direccion", "status": "OK", "se_2_upm": two["se"], "se_3_upm": three["se"]})
    return results


def json_ready(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"no serializable: {type(value).__name__}")


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, evidence: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evidencia.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True, default=json_ready) + "\n",
        encoding="utf-8",
    )
    summary_rows = []
    frequency_rows = []
    funnel_rows = []
    for wave in evidence["waves"]:
        measurement = wave["measurement"]
        historic = wave["comparison"]["historical_reconstructed"]
        producer = wave["comparison"]["producer"]
        domain = wave["design_diagnostics"]["domain_aware_tvivienda"]
        summary_rows.append(
            {
                "celda": wave["cell"],
                "encuesta": wave["survey"],
                "anio_hechos": wave["fact_year"],
                "payload_id": wave["source"]["payload_id"],
                "sha256_zip": wave["source"]["archive_sha256"],
                "n": measurement["n"],
                "numerador_ponderado": measurement["weighted_numerator"],
                "denominador_ponderado": measurement["weighted_denominator"],
                "punto": measurement["point_decimal"],
                "ee_historico_reconstruido": historic["se"],
                "ic95_lo_historico": historic["ic_lo"],
                "ic95_hi_historico": historic["ic_hi"],
                "cv_historico": historic["cv"],
                "delta_punto_productor": wave["comparison"]["differences_validator_minus_producer"]["point"],
                "delta_ee_productor": wave["comparison"]["differences_validator_minus_producer"]["se"],
                "singletons_u_r": wave["design_diagnostics"]["n_singletons_u_r"],
                "singletons_tvivienda": wave["design_diagnostics"]["n_singletons_tvivienda"],
                "ee_dominio_tvivienda": None if domain is None else domain["se"],
                "ic95_lo_dominio_tvivienda": None if domain is None else domain["ic_lo"],
                "ic95_hi_dominio_tvivienda": None if domain is None else domain["ic_hi"],
                "delta_ee_dominio_menos_historico": None if domain is None else domain["se"] - historic["se"],
                "concordancia_numerica": wave["verdicts"]["concordancia_numerica"],
                "validacion_punto": wave["verdicts"]["validacion_punto"],
                "aptitud_inferencial": wave["verdicts"]["aptitud_inferencial"],
                "ee_productor": producer["se"],
            }
        )
        for variable, frequencies in (
            ("BP1_23", measurement["bp1_23_frequencies"]),
            ("BPCOD", measurement["bpcod_frequencies"]),
        ):
            for code_value, count in frequencies.items():
                frequency_rows.append(
                    {"celda": wave["cell"], "variable": variable, "codigo": code_value, "n": count}
                )
        for stage, count in measurement["funnel"].items():
            funnel_rows.append({"celda": wave["cell"], "etapa": stage, "n": count})
    write_tsv(output_dir / "resumen.tsv", summary_rows)
    write_tsv(output_dir / "frecuencias-codificacion.tsv", frequency_rows)
    write_tsv(output_dir / "embudo.tsv", funnel_rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    tests = self_tests()
    if args.self_test:
        print(json.dumps({"self_tests": tests}, ensure_ascii=False, indent=2))
        return 0

    repo = args.repo.resolve()
    raw_root = (args.raw_root or repo / "data/raw").resolve()
    waves = [validate_wave(repo, raw_root, wave) for wave in WAVES]
    protocol = Path(__file__).with_name("PROTOCOLO.md")
    evidence = {
        "validation_id": "GEN2-VALIDACION-R-ENVIPE-CSV-v1_0",
        "execution_date": "2026-09-11",
        "not_blind": True,
        "protocol_sha256": sha256_file(protocol),
        "script_sha256": sha256_file(Path(__file__)),
        "python": platform.python_version(),
        "self_tests": tests,
        "reused": ["biblioteca estándar de Python para ZIP/CSV/SHA-256"],
        "not_reused": [
            "data/corrida0/CALC-R-CIV-M-{10,12,13}/medidor.py",
            "tools/arbitra.py",
            "tools/valida_envipe_independiente.py",
            "tests/svystat.py:prop_ultimate_cluster",
        ],
        "waves": waves,
        "overall": {
            "all_numeric_concordance": all(wave["verdicts"]["concordancia_numerica"] == "CONCUERDA" for wave in waves),
            "all_points_validated": all(wave["verdicts"]["validacion_punto"] == "VALIDADO" for wave in waves),
            "historical_intervals_inferentially_approved": False,
            "reason": "la concordancia histórica no incorpora UPM con contribución cero fuera de U_R; la aptitud se decide por el diagnóstico TVivienda y se propone como sucesor, no como reescritura",
        },
    }
    if args.write:
        write_outputs(Path(__file__).parent, evidence)
    print(
        "VALIDACION_R_ENVIPE · "
        f"puntos_validados={sum(w['verdicts']['validacion_punto'] == 'VALIDADO' for w in waves)}/3 · "
        f"concordancia_numerica={sum(w['verdicts']['concordancia_numerica'] == 'CONCUERDA' for w in waves)}/3 · "
        f"aptitud_historica=NO-APROBADA"
    )
    return 0 if evidence["overall"]["all_numeric_concordance"] and evidence["overall"]["all_points_validated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
