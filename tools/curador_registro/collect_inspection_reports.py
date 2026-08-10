#!/usr/bin/env python3
"""Integra reportes operativos válidos sin alterar su contenido semántico."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


FIELDS = [
    "reporte_id", "tarea_observacion_id", "activo_id", "objeto_logico_id",
    "afirmacion_tipo", "objeto_inspeccionado", "universo_inspeccionado",
    "metodo", "valor_o_descripcion", "evidencia_ref", "localizador",
    "limitacion", "bloqueo", "siguiente_objeto_no_inspeccionado",
]
ALLOWED = {
    "HECHO_OBSERVADO", "NO_OBSERVADO_EN_UNIVERSO_INSPECCIONADO",
    "NO_DETERMINADO", "NO_INSPECCIONADO", "NO_ACCESIBLE",
    "CALCULO_REPRODUCIBLE", "INFERENCIA_PROPUESTA",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_worker(directory: Path) -> Path:
    hashes_path = directory / "hashes.json"
    if not hashes_path.is_file():
        raise ValueError(f"worker sin hashes: {directory}")
    payload = json.loads(hashes_path.read_text(encoding="utf-8"))
    hashes = payload.get("salidas") or payload.get("salidas_sha256") or payload
    if not isinstance(hashes, dict):
        raise ValueError(f"mapa de hashes de salida inválido: {directory}")
    for name, expected in hashes.items():
        path = directory / name
        if not path.is_file() or sha256(path) != expected:
            raise ValueError(f"hash inválido: {path}")
    report = directory / "reporte-inspeccion.tsv"
    if report.name not in hashes:
        raise ValueError(f"reporte no cubierto por hashes: {directory}")
    return report


def collect(base_path: Path, worker_dirs: list[Path]) -> list[dict[str, str]]:
    rows = [{field: row.get(field, "") for field in FIELDS} for row in read_tsv(base_path)]
    seen = {tuple(row[field] for field in FIELDS) for row in rows}
    for directory in worker_dirs:
        for source in read_tsv(validate_worker(directory)):
            row = {field: source.get(field, "") for field in FIELDS}
            if row["afirmacion_tipo"] not in ALLOWED:
                raise ValueError(f"afirmación no permitida: {row['afirmacion_tipo']}")
            if row["afirmacion_tipo"] == "NO_OBSERVADO_EN_UNIVERSO_INSPECCIONADO":
                if not row["universo_inspeccionado"] or not row["metodo"] or not row["limitacion"]:
                    raise ValueError("NO_OBSERVADO sin universo, método o frontera")
            key = tuple(row[field] for field in FIELDS)
            if key not in seen:
                rows.append(row)
                seen.add(key)
    return sorted(rows, key=lambda row: tuple(row[field] for field in FIELDS))


def write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--worker", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = collect(args.base.resolve(), [path.resolve() for path in args.worker])
    write(args.output.resolve(), rows)
    print(json.dumps({"ok": True, "afirmaciones": len(rows), "reportes": len({row['reporte_id'] for row in rows})}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
