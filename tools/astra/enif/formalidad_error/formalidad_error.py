"""Mide el error de seis pisos ENIF de formalidad a partir de RESULT sellados.

El módulo no lee archivos al importarse. La tabla de identidad manda el enlace;
ninguna fila se empareja por orden. Borrador hasta inputs 18–70 y freeze.
"""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
import math
from pathlib import Path

Z95 = 1.959964
OUTCOMES = {"ahorra_solo_informal", "informal_cualquiera", "horizonte_corto"}
CATEGORIES = {"sin seguridad social", "con seguridad social"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_sealed(path: Path, expected_hash: str) -> dict:
    if sha256(path) != expected_hash:
        raise ValueError(f"hash discrepante: {path}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc.get("resultados"), dict):
        raise ValueError(f"sin mapa RESULT: {path}")
    return doc["resultados"]


def read_identity(path: Path, expected_hash: str) -> list[dict]:
    if sha256(path) != expected_hash:
        raise ValueError(f"hash discrepante: {path}")
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 6:
        raise ValueError("la tabla debe tener seis identidades")
    seen = set()
    for row in rows:
        key = (row["outcome"], row["category"])
        if key in seen or key[0] not in OUTCOMES or key[1] not in CATEGORIES:
            raise ValueError(f"llave duplicada o fuera de alcance: {key}")
        seen.add(key)
        if row["source_universe"] != row["target_universe"]:
            raise ValueError(f"universos despareados: {key}")
        if row["source_universe"] != "PERSONA ELEGIDA 18-70":
            raise ValueError(f"universo no autorizado en tabla: {key}")
    if seen != {(o, c) for o in OUTCOMES for c in CATEGORIES}:
        raise ValueError("faltan llaves de la rejilla")
    return rows


def _triple(results: dict, result_id: str):
    """Devuelve (P, LO, HI) o None si no hay estimación íntegra."""
    ids = (result_id, result_id[:-2] + "-IC-LO", result_id[:-2] + "-IC-HI")
    if len(set(ids)) != 3 or not result_id.endswith("-P"):
        raise ValueError(f"id P inválido: {result_id}")
    values = [results.get(key) for key in ids]
    if any(value is None for value in values):
        return None
    if any(isinstance(value, bool) or not isinstance(value, (int, float))
           or not math.isfinite(value) for value in values):
        raise ValueError(f"P/IC inválido: {result_id}")
    p, lo, hi = values
    if not 0 <= lo <= p <= hi <= 1:
        raise ValueError(f"P/IC fuera de rango u orden: {result_id}")
    return p, lo, hi


def measure(rows: list[dict], source: dict, target: dict) -> dict:
    if len(rows) != 6:
        raise ValueError("se requieren seis identidades")
    result = {}
    source_ids, target_ids = set(), set()
    for row in rows:
        key = row["input_id"]
        if key in result:
            raise ValueError(f"input_id duplicado: {key}")
        if row["source_universe"] != row["target_universe"] or row["source_universe"] != "PERSONA ELEGIDA 18-70":
            raise ValueError(f"universo discrepante: {key}")
        if row["source_id"] in source_ids or (row["target_id"] and row["target_id"] in target_ids):
            raise ValueError(f"RESULT duplicado: {key}")
        source_ids.add(row["source_id"])
        target_ids.add(row["target_id"])
        if key != f'{row["outcome"]}::formalidad::{row["category"]}':
            raise ValueError(f"identidad despareada: {key}")
        base = {"input_id": key, "source_id": row["source_id"],
                "target_id": row["target_id"], "universe": row["source_universe"]}
        a = _triple(source, row["source_id"])
        b = _triple(target, row["target_id"]) if row["target_id"] else None
        if a is None or b is None:
            result[key] = {**base, "estado": "NO-COMPARABLE",
                           "clase": "NO-COMPARABLE", "d_pp": None,
                           "ic95_lo_pp": None, "ic95_hi_pp": None,
                           "causa": "FALTA-P-O-IC-SELLADO"}
            continue
        d = 100 * (b[0] - a[0])
        se_a = (a[2] - a[1]) / (2 * Z95)
        se_b = (b[2] - b[1]) / (2 * Z95)
        half_width = 100 * Z95 * math.sqrt(se_a**2 + se_b**2)
        lo, hi = d - half_width, d + half_width
        result[key] = {**base, "estado": "COMPARABLE",
                       "clase": "PERSISTE" if lo <= 0 <= hi else "CAMBIA",
                       "d_pp": d, "ic95_lo_pp": lo, "ic95_hi_pp": hi,
                       "causa": ""}
    if len(result) != 6:
        raise ValueError("salida incompleta")
    return result


def measure_sealed(identity_path: Path, identity_hash: str,
                   source_path: Path, source_hash: str,
                   target_path: Path, target_hash: str) -> dict:
    rows = read_identity(identity_path, identity_hash)
    source = read_sealed(source_path, source_hash)
    target = read_sealed(target_path, target_hash)
    return measure(rows, source, target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("identity", "source", "target"):
        parser.add_argument(f"--{name}", type=Path, required=True)
        parser.add_argument(f"--{name}-sha256", required=True)
    args = parser.parse_args()
    values = measure_sealed(args.identity, args.identity_sha256,
                            args.source, args.source_sha256,
                            args.target, args.target_sha256)
    print(json.dumps(values, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
