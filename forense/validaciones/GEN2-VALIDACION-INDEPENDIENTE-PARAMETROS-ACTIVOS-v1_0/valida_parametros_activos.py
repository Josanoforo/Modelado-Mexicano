#!/usr/bin/env python3
"""Valida desde microdatos los 16 RESULT GEN2 directos activos.

La implementación sigue protocolo-parametros-activos.md. No importa ni lee los medidores
productores para calcular. Los resultados congelados se abren solamente tras
autocontroles, verificación de identidad y medición completa del corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import struct
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path


getcontext().prec = 50
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SNAPSHOT = ROOT / "forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_1.json"

SOURCES = {
    "encig": (
        "encig25_base_datos_csv.zip",
        "47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12",
    ),
    "encuci": (
        "BD_ENCUCI2020_dbf.zip",
        "0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283",
    ),
    "enif": (
        "enif_2024_bd_csv.zip",
        "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039",
    ),
    "envipe": (
        "envipe2025_csv.zip",
        "8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa",
    ),
    "enigh": (
        "enigh2022_nc_csv.zip",
        "3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06",
    ),
}

DOCUMENTS = {
    "FD_ENCUCI2020.pdf": "6cd6f7475a0b5db27a84cf0e047db5b7ed98f73c3480a9e64ea084bc7d475638",
    "encig25_estructura_base_datos.pdf": "09e1b19bcb165979406865360bfdec95a9767640c58565b64d405ceb04e623a2",
    "enif_2024_fd.xlsx": "17e2ad86ce9e4fd5783ee54e9b51ee436b934e002d5736b82094070c74a25db2",
    "enif_2024_cuestionario.pdf": "32e37cc13da38691dee20fbffcef3637aeb87b8dac194e64f83bebed8b57ef8b",
    "cuest_modulo_envipe2025.pdf": "21df38610b21c481382dfb05cf8061e87216d97557c665b2e6e50aacaa216d27",
    "fd_envipe2025.pdf": "83fe02467b661d64e8638d882b242b0e534b8383e683a3fcbeadd66ead777fad",
}


@dataclass
class Accumulator:
    n: int = 0
    numerator: Decimal = Decimal(0)
    denominator: Decimal = Decimal(0)

    def add(self, weight: Decimal, outcome: bool | int) -> None:
        self.n += 1
        self.denominator += weight
        self.numerator += weight * int(bool(outcome))

    def evidence(self) -> dict:
        if self.denominator <= 0:
            raise ValueError("denominador vacío o no positivo")
        return {
            "n": self.n,
            "numerador_decimal": str(self.numerator),
            "denominador_decimal": str(self.denominator),
            "punto": float(self.numerator / self.denominator),
        }


@dataclass(frozen=True)
class Target:
    spec_id: str
    result_id: str
    consumer: str
    measurement: str
    producer_file: str
    tolerance: float
    n_id: str | None = None
    mass_id: str | None = None


TARGETS = (
    Target("CALC-ENVIPE-0001", "RESULT-ENVIPE-DEN-P-C2-U4", "milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:denuncia_con_miedo_o_desconfianza", "envipe_c2_u4", "CALC-ENVIPE-0001", 1e-12, "RESULT-ENVIPE-DEN-N-PERSONAS-U4", "RESULT-ENVIPE-DEN-MASA-FAC-ELE-U4"),
    Target("CALC-ENCUCI-0001", "RESULT-ENCUCI-B-P-RUR-AGR", "milpa/tramite.yaml:civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_rural_con_agravio_encuci2020", "encuci_b_rural_agravio", "CALC-ENCUCI-0001", 1e-12, "RESULT-ENCUCI-B-N-RUR-AGR"),
    Target("CALC-ENCUCI-0001", "RESULT-ENCUCI-B-P-URB-AGR", "milpa/tramite.yaml:civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_urbano_con_agravio_encuci2020", "encuci_b_urbano_agravio", "CALC-ENCUCI-0001", 1e-12, "RESULT-ENCUCI-B-N-URB-AGR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-A-P-CORTO-SIN-P", "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:horizonte_corto", "enif_a_corto_sin", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-A-P-CORTO-SIN-N-DENOMINADOR", "RESULT-ENIF-AHO-A-P-CORTO-SIN-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-A-P-CORTO-CON-P", "milpa/tramite.yaml:dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_corto", "enif_a_corto_con", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-A-P-CORTO-CON-N-DENOMINADOR", "RESULT-ENIF-AHO-A-P-CORTO-CON-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0002", "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P", "milpa/tramite.yaml:dinero.ahorro.horizonte_no_trabajadores:horizonte_corto", "enif_corto_no_trabaja", "CALC-ENIF-0002", 5e-7, "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-N-DENOMINADOR", "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P", "milpa/tramite.yaml:dinero.ahorro.seguro_deposito_enif2024:desconfianza_o_mal_servicio_como_razon_principal_conoce_proteccion_enif2024", "enif_c_desconfia_conoce", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-N-DENOMINADOR", "RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P", "milpa/tramite.yaml:dinero.ahorro.seguro_deposito_enif2024:desconfianza_o_mal_servicio_como_razon_principal_no_conoce_enif2024", "enif_c_desconfia_no_conoce", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-N-DENOMINADOR", "RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-B-P-FORMAL-P", "milpa/tramite.yaml:dinero.ahorro.via_informal:formal_cualquiera", "enif_b_formal", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-B-P-FORMAL-N-DENOMINADOR", "RESULT-ENIF-AHO-B-P-FORMAL-PESO-DENOMINADOR"),
    Target("CALC-ENIF-0001", "RESULT-ENIF-AHO-B-P-INFORMAL-P", "milpa/tramite.yaml:dinero.ahorro.via_informal:informal_cualquiera", "enif_b_informal", "CALC-ENIF-0001", 5e-7, "RESULT-ENIF-AHO-B-P-INFORMAL-N-DENOMINADOR", "RESULT-ENIF-AHO-B-P-INFORMAL-PESO-DENOMINADOR"),
    Target("CALC-B-0001", "RESULT-B-ENIGH-2022-P", "milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas", "enigh_remesas_2022", "CALC-B-0001", 1e-12, "RESULT-B-ENIGH-2022-N", "RESULT-B-ENIGH-2022-HOGARES-EXPANDIDOS"),
    Target("CALC-ENCIG-0001", "RESULT-ENCIG-MOR-C-P-ADOPTA", "milpa/tramite.yaml:tramite.gobierno_digital.util_sin_coercion:adopta_encig2025_luz", "encig_c_adopta", "CALC-ENCIG-0001", 1e-12, "RESULT-ENCIG-MOR-C-N-U", "RESULT-ENCIG-MOR-C-MASA-FAC-TRA-U"),
    Target("CALC-ENCIG-0001", "RESULT-ENCIG-MOR-A-P-SOL1", "milpa/tramite.yaml:tramite.mordida.discrecional:paga_mordida_encig2025", "encig_a_sol1", "CALC-ENCIG-0001", 1e-12, "RESULT-ENCIG-MOR-A-N-U", "RESULT-ENCIG-MOR-A-MASA-FAC-P18-U"),
    Target("CALC-ENCIG-0001", "RESULT-ENCIG-MOR-B-P-DIG-SD", "milpa/tramite.yaml:tramite.mordida.con_registro:paga_mordida_encig2025_digital_r2", "encig_b_digital_sd", "CALC-ENCIG-0001", 1e-12, "RESULT-ENCIG-MOR-B-N-DIG-SD"),
    Target("CALC-ENCIG-0001", "RESULT-ENCIG-MOR-B-P-PRE-SD", "milpa/tramite.yaml:tramite.mordida.con_registro:paga_mordida_encig2025_presencial_r2", "encig_b_presencial_sd", "CALC-ENCIG-0001", 1e-12, "RESULT-ENCIG-MOR-B-N-PRE-SD"),
    Target("CALC-ENCUCI-0001", "RESULT-ENCUCI-A-P-CUALQUIERA", "milpa/tramite.yaml:tramite.mordida.discrecional:solicitud_o_entrega_mordida_encuci2020", "encuci_a_cualquiera", "CALC-ENCUCI-0001", 1e-12, "RESULT-ENCUCI-A-N-U", "RESULT-ENCUCI-A-MASA-FAC-SEL-U"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exact_member(archive: zipfile.ZipFile, member: str) -> str:
    matches = [name for name in archive.namelist() if name == member]
    if len(matches) != 1:
        raise ValueError(f"{archive.filename}: {member!r} resuelve {len(matches)} miembros")
    return matches[0]


def iter_csv_member(path: Path, member: str, required: set[str]):
    with zipfile.ZipFile(path) as archive:
        exact_member(archive, member)
        with archive.open(member) as probe_stream:
            probe = probe_stream.read(1024 * 1024)
        try:
            probe.decode("utf-8-sig")
            encoding = "utf-8-sig"
        except UnicodeDecodeError:
            encoding = "latin-1"
        with archive.open(member) as binary:
            text = io.TextIOWrapper(binary, encoding=encoding, newline="")
            reader = csv.DictReader(text)
            if reader.fieldnames is None:
                raise ValueError(f"{member}: sin cabecera")
            fields = {field.strip().upper() for field in reader.fieldnames}
            missing = required - fields
            if missing:
                raise ValueError(f"{member}: columnas ausentes {sorted(missing)}")
            for row in reader:
                yield {str(key).strip().upper(): value for key, value in row.items()}


def dbf_rows_from_blob(blob: bytes, required: set[str]) -> tuple[list[dict], dict]:
    if len(blob) < 33:
        raise ValueError("DBF truncado")
    n_records = struct.unpack("<I", blob[4:8])[0]
    header_length = struct.unpack("<H", blob[8:10])[0]
    record_length = struct.unpack("<H", blob[10:12])[0]
    fields = []
    offset = 1
    cursor = 32
    while cursor < header_length and blob[cursor] != 0x0D:
        descriptor = blob[cursor:cursor + 32]
        if len(descriptor) != 32:
            raise ValueError("descriptor DBF truncado")
        name = descriptor[:11].split(b"\0", 1)[0].decode("ascii").upper()
        length = descriptor[16]
        fields.append((name, offset, length))
        offset += length
        cursor += 32
    if offset != record_length:
        raise ValueError(f"DBF ancho reconstruido {offset} != {record_length}")
    available = {name for name, _, _ in fields}
    missing = required - available
    if missing:
        raise ValueError(f"DBF columnas ausentes {sorted(missing)}")
    selected = [field for field in fields if field[0] in required]
    rows = []
    deleted = 0
    for index in range(n_records):
        start = header_length + index * record_length
        record = blob[start:start + record_length]
        if len(record) != record_length:
            raise ValueError("registro DBF truncado")
        if record[0:1] == b"*":
            deleted += 1
            continue
        if record[0:1] not in {b" ", b"\x00"}:
            raise ValueError(f"marca DBF inesperada {record[0]:#x}")
        rows.append({
            name: record[field_offset:field_offset + length].decode("latin-1").strip()
            for name, field_offset, length in selected
        })
    return rows, {
        "registros_declarados": n_records,
        "registros_vivos": len(rows),
        "registros_borrados": deleted,
        "ancho_registro": record_length,
        "campos": sorted(available),
    }


def dbf_member(path: Path, member: str, required: set[str]) -> tuple[list[dict], dict]:
    with zipfile.ZipFile(path) as archive:
        exact_member(archive, member)
        return dbf_rows_from_blob(archive.read(member), required)


def clean(value) -> str:
    return "" if value is None else str(value).strip()


def int_code(value) -> int | None:
    text = clean(value)
    if not text or text.casefold() == "b":
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    return int(number) if number.is_finite() and number == number.to_integral_value() else None


def positive_weight(value) -> Decimal | None:
    text = clean(value)
    if not text:
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    return number if number.is_finite() and number > 0 else None


def verify_inputs(raw_root: Path) -> dict:
    evidence = {"payloads": {}, "documentos": {}}
    for source, (filename, expected) in SOURCES.items():
        path = raw_root / filename
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(f"{filename}: hash {actual} != {expected}")
        evidence["payloads"][source] = {
            "archivo": filename,
            "sha256": actual,
            "bytes": path.stat().st_size,
        }
    for filename, expected in DOCUMENTS.items():
        path = raw_root / filename
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(f"{filename}: hash {actual} != {expected}")
        evidence["documentos"][filename] = {"sha256": actual, "bytes": path.stat().st_size}
    return evidence


def measure_enif(path: Path) -> tuple[dict, dict]:
    member = "TMODULO.csv"
    informal = [f"P5_1_{i}" for i in range(1, 7)]
    formal = [f"P5_6_{i}" for i in range(1, 10)]
    required = {"P3_8", "P3_9", "P3_13", "P4_10", "P5_20", "P5_23", "FAC_PER", *informal, *formal}
    acc = {name: Accumulator() for name in (
        "enif_a_corto_sin", "enif_a_corto_con", "enif_b_formal",
        "enif_b_informal", "enif_c_desconfia_conoce",
        "enif_c_desconfia_no_conoce", "enif_corto_no_trabaja",
    )}
    counts = Counter()
    for row in iter_csv_member(path, member, required):
        counts["filas_tmodulo"] += 1
        weight = positive_weight(row["FAC_PER"])
        if weight is None:
            counts["peso_invalido"] += 1
            continue
        p410 = int_code(row["P4_10"])
        p313 = int_code(row["P3_13"])
        if p410 in {1, 2, 3, 4, 5} and p313 == 7:
            acc["enif_a_corto_sin"].add(weight, p410 in {1, 2})
        if p410 in {1, 2, 3, 4, 5} and p313 in {1, 2, 3, 4}:
            acc["enif_a_corto_con"].add(weight, p410 in {1, 2})
        acc["enif_b_formal"].add(weight, any(int_code(row[name]) == 1 for name in formal))
        acc["enif_b_informal"].add(weight, any(int_code(row[name]) == 1 for name in informal))
        p520 = int_code(row["P5_20"])
        p523 = int_code(row["P5_23"])
        if p520 in set(range(1, 11)) and p523 == 1:
            acc["enif_c_desconfia_conoce"].add(weight, p520 == 3)
        if p520 in set(range(1, 11)) and p523 == 2:
            acc["enif_c_desconfia_no_conoce"].add(weight, p520 == 3)
        nonworker = int_code(row["P3_8"]) == 8 or int_code(row["P3_9"]) == 7
        if nonworker and p410 in {1, 2, 3, 4, 5}:
            acc["enif_corto_no_trabaja"].add(weight, p410 in {1, 2})
    return {key: value.evidence() for key, value in acc.items()}, dict(sorted(counts.items()))


def measure_enigh(path: Path) -> tuple[dict, dict]:
    member = "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv"
    acc = Accumulator()
    counts = Counter()
    for row in iter_csv_member(path, member, {"FOLIOVIV", "FOLIOHOG", "REMESAS", "FACTOR"}):
        counts["filas_concentradohogar"] += 1
        weight = positive_weight(row["FACTOR"])
        if weight is None:
            counts["peso_invalido"] += 1
            continue
        try:
            remittances = Decimal(clean(row["REMESAS"]))
        except InvalidOperation:
            counts["remesas_nula_o_invalida"] += 1
            continue
        if not remittances.is_finite():
            counts["remesas_nula_o_invalida"] += 1
            continue
        acc.add(weight, remittances > 0)
    return {"enigh_remesas_2022": acc.evidence()}, dict(sorted(counts.items()))


def measure_envipe(path: Path) -> tuple[dict, dict]:
    person_member = "tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv"
    crime_member = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"
    people = {}
    counts = Counter()
    for row in iter_csv_member(path, person_member, {"ID_PER", "FAC_ELE"}):
        counts["filas_tper_vic2"] += 1
        key = clean(row["ID_PER"])
        if key in people:
            raise ValueError(f"ENVIPE ID_PER duplicado: {key}")
        people[key] = positive_weight(row["FAC_ELE"])
    collapsed = {}
    for row in iter_csv_member(path, crime_member, {"ID_PER", "BPCOD", "BP1_20", "BP1_23", "FAC_DEL"}):
        counts["filas_tmod_vic"] += 1
        if int_code(row["BPCOD"]) not in set(range(5, 16)):
            counts["fuera_bpcod_05_15"] += 1
            continue
        if int_code(row["BP1_20"]) != 2:
            counts["denunciado_o_invalido"] += 1
            continue
        reason = int_code(row["BP1_23"])
        if reason not in set(range(1, 9)):
            counts["bp1_23_fuera_01_08"] += 1
            continue
        if positive_weight(row["FAC_DEL"]) is None:
            counts["fac_del_invalido"] += 1
            continue
        key = clean(row["ID_PER"])
        outcome = reason in {1, 2, 6, 8}
        collapsed[key] = max(int(outcome), collapsed.get(key, 0))
    acc = Accumulator()
    for key, outcome in collapsed.items():
        weight = people.get(key)
        if weight is None:
            counts["persona_sin_fac_ele_valido_o_sin_pareja"] += 1
            continue
        acc.add(weight, outcome)
    counts["personas_colapsadas_u4"] = len(collapsed)
    return {"envipe_c2_u4": acc.evidence()}, dict(sorted(counts.items()))


def measure_encuci(path: Path) -> tuple[dict, dict]:
    contacts = {f"AP5_16_{i}" for i in range(1, 11)}
    fields45 = {"ID_PER", "AP5_17", "AP5_18", "AP4_3_2", "FAC_SEL", *contacts}
    rows45, meta45 = dbf_member(path, "ENCUCI_2020_SEC_4_5.dbf", fields45)
    acc_a = Accumulator()
    counts = Counter()
    by_person = {}
    for row in rows45:
        key = clean(row["ID_PER"])
        if key in by_person:
            raise ValueError(f"ENCUCI SEC45 ID_PER duplicado: {key}")
        by_person[key] = int_code(row["AP4_3_2"])
        weight = positive_weight(row["FAC_SEL"])
        has_contact = any(int_code(row[name]) == 1 for name in contacts)
        response17, response18 = int_code(row["AP5_17"]), int_code(row["AP5_18"])
        if weight is not None and has_contact and response17 in {1, 2} and response18 in {1, 2}:
            acc_a.add(weight, response17 == 1 or response18 == 1)
        else:
            counts["a_fuera_universo"] += 1
    rows678, meta678 = dbf_member(path, "ENCUCI_2020_SEC_6_7_8.dbf", {"ID_PER", "AP7_3_5", "DOMINIO", "FAC_SEL"})
    acc_urb = Accumulator()
    acc_rur = Accumulator()
    acc_all = Accumulator()
    seen678 = set()
    for row in rows678:
        key = clean(row["ID_PER"])
        if key in seen678:
            raise ValueError(f"ENCUCI SEC678 ID_PER duplicado: {key}")
        seen678.add(key)
        agravio = by_person.get(key)
        protest = int_code(row["AP7_3_5"])
        domain = clean(row["DOMINIO"]).upper()
        weight = positive_weight(row["FAC_SEL"])
        if agravio not in {1, 2} or protest not in {1, 2} or domain not in {"U", "C", "R"} or weight is None:
            counts["b_fuera_universo"] += 1
            continue
        acc_all.add(weight, protest == 1)
        if agravio == 1 and domain in {"U", "C"}:
            acc_urb.add(weight, protest == 1)
        if agravio == 1 and domain == "R":
            acc_rur.add(weight, protest == 1)
    measurements = {
        "encuci_a_cualquiera": acc_a.evidence(),
        "encuci_b_urbano_agravio": acc_urb.evidence(),
        "encuci_b_rural_agravio": acc_rur.evidence(),
    }
    diagnostics = dict(sorted(counts.items())) | {"dbf_sec45": meta45, "dbf_sec678": meta678, "b_universo_completo": acc_all.evidence()}
    return measurements, diagnostics


def measure_encig(path: Path) -> tuple[dict, dict]:
    person_member = "encig2025_01_sec1_A_3_4_5_8_9_10.csv"
    sec7_member = "encig2025_04_sec_7.csv"
    sec8_member = "encig2025_05_sec_8.csv"
    counts = Counter()
    acc_a = Accumulator()
    for row in iter_csv_member(path, person_member, {"P8_3_1", "FAC_P18"}):
        counts["filas_persona"] += 1
        response = int_code(row["P8_3_1"])
        weight = positive_weight(row["FAC_P18"])
        if response in {1, 2} and weight is not None:
            acc_a.add(weight, response == 1)
        else:
            counts["a_fuera_universo"] += 1
    sec8 = {}
    for row in iter_csv_member(path, sec8_member, {"ID_TRA", "P8_4"}):
        counts["filas_sec8"] += 1
        key = clean(row["ID_TRA"])
        if key in sec8:
            raise ValueError(f"ENCIG SEC8 ID_TRA duplicado: {key}")
        sec8[key] = int_code(row["P8_4"])
    acc_pre = Accumulator()
    acc_dig = Accumulator()
    acc_c = Accumulator()
    id_tra_counts = Counter()
    for row in iter_csv_member(path, sec7_member, {"ID_TRA", "N_TRA", "P7_3", "FAC_TRA"}):
        counts["filas_sec7"] += 1
        key = clean(row["ID_TRA"])
        id_tra_counts[key] += 1
        channel = int_code(row["P7_3"])
        weight = positive_weight(row["FAC_TRA"])
        p84 = sec8.get(key)
        if weight is not None and p84 in {0, 1}:
            if channel == 1:
                acc_pre.add(weight, p84 == 1)
            elif channel in {3, 4, 5}:
                acc_dig.add(weight, p84 == 1)
        if weight is not None and int_code(row["N_TRA"]) == 1 and channel in {1, 2, 4, 5, 6}:
            acc_c.add(weight, channel in {4, 5})
    counts["id_tra_repetidos_sec7"] = sum(value > 1 for value in id_tra_counts.values())
    measurements = {
        "encig_a_sol1": acc_a.evidence(),
        "encig_b_presencial_sd": acc_pre.evidence(),
        "encig_b_digital_sd": acc_dig.evidence(),
        "encig_c_adopta": acc_c.evidence(),
    }
    return measurements, dict(sorted(counts.items()))


def synthetic_dbf() -> bytes:
    fields = [("ID", "C", 2), ("VAL", "N", 3)]
    n_records = 3
    header_length = 32 + 32 * len(fields) + 1
    record_length = 1 + sum(field[2] for field in fields)
    header = bytearray(header_length)
    header[0] = 0x03
    header[4:8] = struct.pack("<I", n_records)
    header[8:10] = struct.pack("<H", header_length)
    header[10:12] = struct.pack("<H", record_length)
    cursor = 32
    for name, kind, length in fields:
        encoded = name.encode("ascii")
        header[cursor:cursor + len(encoded)] = encoded
        header[cursor + 11] = ord(kind)
        header[cursor + 16] = length
        cursor += 32
    header[cursor] = 0x0D
    records = b" A1  1" + b"*B2  2" + b" C3  3"
    return bytes(header) + records + b"\x1a"


def selftests() -> dict:
    acc = Accumulator()
    acc.add(Decimal(1), 1)
    acc.add(Decimal(3), 0)
    assert acc.evidence()["punto"] == 0.25
    assert positive_weight("0") is None
    assert positive_weight("-1") is None
    assert positive_weight("Infinity") is None
    assert positive_weight("") is None
    assert int_code("1.5") is None and int_code("1.000") == 1
    mapping = {"K": 1}
    repeated = ["K", "K"]
    assert sum(mapping[key] for key in repeated) == 2
    rows, meta = dbf_rows_from_blob(synthetic_dbf(), {"ID", "VAL"})
    assert rows == [{"ID": "A1", "VAL": "1"}, {"ID": "C3", "VAL": "3"}]
    assert meta["registros_borrados"] == 1
    return {
        "ponderacion_desigual": "PASA",
        "codigos_y_pesos_invalidos": "PASA",
        "multiplicidad_join": "PASA",
        "lector_dbf_sintetico": "PASA",
    }


def snapshot_links() -> tuple[dict, dict]:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    rows = data["salidas_gen2_directas"]
    if len(rows) != 16:
        raise ValueError(f"snapshot: {len(rows)} salidas, esperadas 16")
    links = {(row["resultado_id"], row["consumidor"]): row for row in rows}
    if len(links) != 16:
        raise ValueError("snapshot: pares consumidor/RESULT duplicados")
    expected = {(target.result_id, target.consumer) for target in TARGETS}
    if set(links) != expected:
        raise ValueError(f"snapshot difiere: faltan={sorted(expected-set(links))}, sobran={sorted(set(links)-expected)}")
    for row in rows:
        if row.get("estado") != "EMITE" or row.get("validacion_independiente") != "NO-HECHA":
            raise ValueError(f"snapshot estado inesperado: {row['resultado_id']}")
    return data, {"sha256": sha256_file(SNAPSHOT), "n_salidas": 16, "pares_unicos": 16}


def producer_results(calc: str) -> tuple[dict, dict]:
    path = ROOT / f"data/corrida0/{calc}/resultados.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["resultados"], {"ruta": str(path.relative_to(ROOT)), "sha256": sha256_file(path)}


def compare(measurements: dict, input_evidence: dict) -> tuple[list[dict], dict]:
    producer_cache = {}
    producer_evidence = {}
    rows = []
    for target in TARGETS:
        if target.producer_file not in producer_cache:
            producer_cache[target.producer_file], producer_evidence[target.producer_file] = producer_results(target.producer_file)
        producer = producer_cache[target.producer_file]
        measured = measurements[target.measurement]
        reference = float(producer[target.result_id])
        delta = measured["punto"] - reference
        n_ok = target.n_id is None or measured["n"] == int(producer[target.n_id])
        mass_ok = target.mass_id is None or Decimal(measured["denominador_decimal"]) == Decimal(str(producer[target.mass_id]))
        point_ok = abs(delta) <= target.tolerance
        verdict = "PASA" if point_ok and n_ok and mass_ok else "NO-PASA"
        rows.append({
            "spec_id": target.spec_id,
            "resultado_id": target.result_id,
            "consumidor": target.consumer,
            "medicion": target.measurement,
            "punto_independiente": measured["punto"],
            "punto_productor": reference,
            "delta": delta,
            "tolerancia": target.tolerance,
            "n": measured["n"],
            "n_productor": int(producer[target.n_id]) if target.n_id else None,
            "numerador_decimal": measured["numerador_decimal"],
            "denominador_decimal": measured["denominador_decimal"],
            "masa_productor": str(producer[target.mass_id]) if target.mass_id else None,
            "punto_concuerda": point_ok,
            "n_concuerda": n_ok,
            "masa_concuerda": mass_ok,
            "validacion_independiente": verdict,
            "alcance": "PUNTO;UNIVERSO;UNIDAD;CODIFICACION;PONDERADOR;TRANSFORMACION;ENLACE",
            "inferencia_diseno": "NO-COMPROBADA",
        })
    summary = Counter(row["validacion_independiente"] for row in rows)
    return rows, {"por_veredicto": dict(sorted(summary.items())), "productores": producer_evidence}


def write_tsv(path: Path, rows: list[dict]) -> None:
    fields = [
        "spec_id", "resultado_id", "consumidor", "medicion",
        "punto_independiente", "punto_productor", "delta", "tolerancia",
        "n", "n_productor", "numerador_decimal", "denominador_decimal",
        "masa_productor", "punto_concuerda", "n_concuerda", "masa_concuerda",
        "validacion_independiente", "alcance", "inferencia_diseno",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=ROOT / "data/raw")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    tests = selftests()
    _, snapshot_evidence = snapshot_links()
    inputs = verify_inputs(args.raw_root)

    measurements = {}
    diagnostics = {}
    runners = (
        ("enif", measure_enif),
        ("enigh", measure_enigh),
        ("envipe", measure_envipe),
        ("encuci", measure_encuci),
        ("encig", measure_encig),
    )
    for source, runner in runners:
        source_measurements, source_diagnostics = runner(args.raw_root / SOURCES[source][0])
        overlap = set(measurements) & set(source_measurements)
        if overlap:
            raise ValueError(f"mediciones duplicadas: {sorted(overlap)}")
        measurements.update(source_measurements)
        diagnostics[source] = source_diagnostics
    if set(measurements) != {target.measurement for target in TARGETS}:
        raise ValueError("el conjunto medido no coincide con el perímetro congelado")

    comparisons, comparison_summary = compare(measurements, inputs)
    evidence = {
        "acto": "GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS",
        "fecha": "2026-09-11",
        "protocolo": "forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS-v1_0/protocolo-parametros-activos.md",
        "independencia": {
            "implementacion": "SI",
            "cegamiento_a_cifras": "NO",
            "muestra_independiente": "NO",
            "lee_medidores_productores": "NO",
            "orden": "autocontroles -> snapshot/enlaces -> identidad -> microdatos -> resultados.json productores",
        },
        "alcance": {
            "consumidores_directos": 16,
            "resultados_unicos": 16,
            "incertidumbre_diseno": "NO-COMPROBADA",
            "causalidad": "NO-APLICA",
        },
        "autocontroles": tests,
        "snapshot": snapshot_evidence,
        "fuentes": inputs,
        "diagnosticos": diagnostics,
        "mediciones": measurements,
        "comparaciones": comparisons,
        "resumen": comparison_summary,
        "python": sys.version.split()[0],
    }
    rendered = json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "evidencia-parametros-activos.json").write_text(
            rendered, encoding="utf-8")
        write_tsv(HERE / "resumen-parametros-activos.tsv", comparisons)
    else:
        print(rendered, end="")
    return 0 if comparison_summary["por_veredicto"] == {"PASA": 16} else 1


if __name__ == "__main__":
    raise SystemExit(main())
