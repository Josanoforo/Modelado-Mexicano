#!/usr/bin/env python3
"""Migra data/cola-adquisicion-v1_0.tsv al registro oficial (P2, MAESTRA33-A5).

Lee la cola tal como esta hoy y escribe cola-adquisicion-registro.tsv: una
fila por cada fila de la cola, con fuente_canonica resuelta contra
aliases-fuentes.tsv (discordancias listadas, no forzadas) y una cita de
origen (A.13: numero de fila real de la cola de entrada).

No decide adquisiciones nuevas, no borra la cola de agosto, no toca
manifiesto.yaml. Sin via a mano: correr de nuevo sobre la misma entrada
produce la misma salida (salvo que la propia cola de entrada cambie).
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDS = [
    "fila_origen",
    "fuente_canonica",
    "fuente_canonica_normalizada",
    "discordancia_alias",
    "estado_A4A5",
    "prioridad",
    "url_conocida",
    "ids_manifiesto",
    "origen",
    "nota",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build_alias_index(aliases: list[dict[str, str]]) -> dict[str, str]:
    return {row["alias_fuente"].strip().upper(): row["fuente_canonica_normalizada"].strip() for row in aliases}


def build(cola_path: Path, aliases_path: Path) -> list[dict[str, str]]:
    cola_rows = read_tsv(cola_path)
    alias_index = build_alias_index(read_tsv(aliases_path))
    out: list[dict[str, str]] = []
    for line_no, row in enumerate(cola_rows, start=2):  # +1 header, +1 1-index
        fuente = row["fuente_canonica"].strip()
        normalizada = alias_index.get(fuente.upper())
        discordancia = "" if normalizada else "SIN_ALIAS"
        out.append({
            "fila_origen": f"cola-adquisicion-v1_0.tsv:{line_no}",
            "fuente_canonica": fuente,
            "fuente_canonica_normalizada": normalizada or fuente,
            "discordancia_alias": discordancia,
            "estado_A4A5": row["estado_A4A5"].strip(),
            "prioridad": row["prioridad"].strip(),
            "url_conocida": row["url_conocida"].strip(),
            "ids_manifiesto": row["ids_manifiesto"].strip(),
            "origen": row["origen"].strip(),
            "nota": row["nota"].strip(),
        })
    return out


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cola", type=Path, default=Path("data/cola-adquisicion-v1_0.tsv"))
    parser.add_argument("--aliases", type=Path, default=Path("data/curacion-registro/aliases-fuentes.tsv"))
    parser.add_argument("--output", type=Path, default=Path("data/curacion-registro/cola-adquisicion-registro.tsv"))
    args = parser.parse_args()
    rows = build(args.cola.resolve(), args.aliases.resolve())
    write_tsv(args.output.resolve(), rows)
    con_alias = sum(1 for row in rows if not row["discordancia_alias"])
    print(f"filas={len(rows)} con_alias={con_alias} sin_alias={len(rows) - con_alias}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
