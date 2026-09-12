#!/usr/bin/env python3
"""Control independiente de tres hechos de CALC-MOTRAL2015-VALORACION-SS-0001.

Usa dbfread y extracción temporal, no importa el lector ni las funciones del
medidor congelado. Comprueba el cociente P17 total, la clasificación P16 y la
cardinalidad de la unión con ENOE contra el resultado sellado.
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

from dbfread import DBF


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from payload_resolver import resolver_payload  # noqa: E402

KEY = ("CD_A", "ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN")
RANKS = ("P16_1", "P16_2", "P16_3", "P16_4", "P16_5")
RESULT = ROOT / "data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001/resultados.json"


def payload(payload_id: str) -> Path:
    found = resolver_payload(payload_id, root=str(ROOT))
    if found["estado"] != "COINCIDE":
        raise SystemExit(f"{payload_id}: {found['estado']}")
    return Path(found["ruta_absoluta"])


def extract_member(archive: Path, basename: str, destination: Path) -> Path:
    with zipfile.ZipFile(archive) as zipped:
        matches = [name for name in zipped.namelist() if Path(name).name.upper() == basename.upper()]
        if len(matches) != 1:
            raise SystemExit(f"miembro no unívoco {basename}: {matches}")
        target = destination / basename
        with zipped.open(matches[0]) as source, target.open("wb") as output:
            while chunk := source.read(1024 * 1024):
                output.write(chunk)
        return target


def text(row, field: str) -> str:
    value = row[field]
    return "" if value is None else str(value).strip()


def key(row) -> tuple[str, ...]:
    return tuple(text(row, field) for field in KEY)


def eligible(row) -> bool:
    try:
        age = int(text(row, "EDA"))
    except ValueError:
        return False
    return text(row, "R_DEF") == "00" and 18 <= age <= 54 and text(row, "C_TRA") in {"1", "2"}


def ranking(row) -> tuple[str, int | None]:
    values = [text(row, field) for field in RANKS]
    valid = [value for value in values if value in {"1", "2", "3", "4", "5"}]
    first = [index for index, value in enumerate(values) if value == "1"]
    if len(first) > 1 or len(valid) != len(set(valid)):
        return "INCONSISTENTE", None
    if len(first) == 1 and sorted(valid) == ["1", "2", "3", "4", "5"]:
        return "COMPLETO", first[0]
    if len(first) == 1:
        return "INCOMPLETO-CON-PRIMERO", first[0]
    if any(value not in {"", "9"} for value in values):
        return "INCONSISTENTE", None
    return "INCOMPLETO-SIN-PRIMERO", None


def main() -> int:
    sealed = json.loads(RESULT.read_text(encoding="utf-8"))["resultados"]
    estimates = json.loads(sealed["RESULT-MOTRAL15-G-ESTIMANDOS-JSON"])
    expected_diag = json.loads(sealed["RESULT-MOTRAL15-G-DIAGNOSTICOS-JSON"])
    with tempfile.TemporaryDirectory(prefix="control-motral15-") as temporary:
        tmp = Path(temporary)
        module_file = extract_member(payload("motral2015_bases_datos_dbf"), "motral2015_cuestionario.dbf", tmp)
        enoe_file = extract_member(payload("enoe_2015_trim2_dbf"), "SDEMT215.DBF", tmp)
        module = list(DBF(module_file, encoding="latin-1", char_decode_errors="strict", load=True))
        module_keys = [key(row) for row in module]
        wanted = set(module_keys)
        enoe_keys = [key(row) for row in DBF(enoe_file, encoding="latin-1", char_decode_errors="strict", load=False) if key(row) in wanted]

    if len(module_keys) != len(set(module_keys)):
        raise SystemExit("FALLA: llave MOTRAL duplicada")
    counts = Counter(enoe_keys)
    duplicates = sum(count - 1 for count in counts.values() if count > 1)
    matches = len(counts)
    losses = len(module_keys) - matches

    rows = [row for row in module if eligible(row)]
    p17 = [row for row in rows if text(row, "P17") in {"1", "2"}]
    numerator = math.fsum(float(row["FAC_MOTRAL"]) for row in p17 if text(row, "P17") == "1")
    denominator = math.fsum(float(row["FAC_MOTRAL"]) for row in p17)
    statuses: Counter[str] = Counter()
    first: Counter[int] = Counter()
    for row in rows:
        status, choice = ranking(row)
        statuses[status] += 1
        if choice is not None:
            first[choice] += 1

    expected_p17 = estimates["P17-TOTAL"]
    failures = []
    if not math.isclose(numerator / denominator, expected_p17["p"], abs_tol=5e-13):
        failures.append("cociente P17")
    if (numerator, denominator) != (expected_p17["masa_numerador"], expected_p17["masa_denominador"]):
        failures.append("masas P17")
    if dict(statuses) != expected_diag["ranking"]:
        failures.append("clasificación ranking")
    if sum(first.values()) != 5698 or sum(first.values()) != expected_p17["n_expuesto"] - 6:
        failures.append("primer lugar único")
    if (matches, losses, duplicates) != (6564, 436, 0):
        failures.append("cardinalidad ENOE")
    if failures:
        raise SystemExit("FALLA: " + ", ".join(failures))
    print("CONTROL-INDEPENDIENTE: COINCIDE")
    print(f"P17_TOTAL={numerator / denominator:.12f}; MASAS={numerator:.0f}/{denominator:.0f}; N={len(p17)}")
    print(f"RANKING={dict(sorted(statuses.items()))}; PRIMEROS_VALIDOS={sum(first.values())}")
    print(f"JOIN_ENOE=COINCIDENCIAS:{matches}; PERDIDAS:{losses}; DUPLICADOS:{duplicates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
