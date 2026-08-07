#!/usr/bin/env python3
"""Deriva la cola de relaciones candidatas sin crear otra fuente de verdad."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

try:
    from .baseline import leer_tsv
except ImportError:  # ejecución directa
    from baseline import leer_tsv


def derivar(baseline: Path) -> list[dict[str, str]]:
    filas = leer_tsv(baseline / "relaciones.tsv")
    candidatas = [f for f in filas if f.get("clasificacion_relacion") == "CANDIDATA"]
    return sorted(candidatas, key=lambda f: f["relacion_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    filas = derivar(args.baseline.resolve())
    campos = list(filas[0]) if filas else ["relacion_id"]
    handle = args.output.open("w", encoding="utf-8", newline="") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(handle, fieldnames=campos, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(filas)
    finally:
        if args.output:
            handle.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
