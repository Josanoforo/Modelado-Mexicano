#!/usr/bin/env python3
"""Publica la tabla larga de estimandos sellados de MOTRAL 2015."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001/resultados.json"
TARGET = ROOT / "data/motral2015-valoracion-ss/estimandos-motral2015.csv"
METRICS = (
    "n_expuesto", "n_valido", "n_desconocido", "masa_desconocido",
    "n_numerador", "masa_numerador", "masa_denominador", "p", "ee",
    "ic95_lo", "ic95_hi", "gl", "precision_estado",
)


def dimensions(name: str) -> tuple[str, str, str]:
    if name.startswith("P16-FIRST-"):
        remainder = name.removeprefix("P16-FIRST-")
        segment, category = remainder.rsplit("-", 1)
        return "P16_PRIMER_LUGAR", segment, category
    if name.startswith("P17-"):
        return "P17_AFIRMATIVA", name.removeprefix("P17-"), "SI"
    if name.startswith("ENOE-P17-"):
        return "P17_AFIRMATIVA_POR_SS_EMPLEO_ACTUAL", name.removeprefix("ENOE-P17-"), "SI"
    raise ValueError(f"estimando no reconocido: {name}")


def main() -> int:
    result = json.loads(SOURCE.read_text(encoding="utf-8"))["resultados"]
    estimates = json.loads(result["RESULT-MOTRAL15-G-ESTIMANDOS-JSON"])
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("estimando", "tipo", "segmento", "categoria", *METRICS))
        writer.writeheader()
        for name, values in sorted(estimates.items()):
            kind, segment, category = dimensions(name)
            writer.writerow({"estimando": name, "tipo": kind, "segmento": segment,
                             "categoria": category, **{metric: values[metric] for metric in METRICS}})
    print(f"PUBLICADOS {len(estimates)} estimandos en {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
