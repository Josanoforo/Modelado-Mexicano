#!/usr/bin/env python3
"""Invariantes de los agregados publicados de MOTRAL 2015."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001/resultados.json"
CSV = ROOT / "data/motral2015-valoracion-ss/estimandos.csv"


def main() -> int:
    values = json.loads(RESULT.read_text(encoding="utf-8"))["resultados"]
    estimates = json.loads(values["RESULT-MOTRAL15-G-ESTIMANDOS-JSON"])
    with CSV.open(encoding="utf-8", newline="") as stream:
        published = {row["estimando"]: row for row in csv.DictReader(stream)}
    assert len(estimates) == len(published) == 32
    for name, estimate in estimates.items():
        assert math.isclose(float(published[name]["p"]), estimate["p"], abs_tol=1e-12)
        assert int(published[name]["n_valido"]) == estimate["n_valido"]
    for segment in ("TOTAL", "HOMBRE", "MUJER", "EDAD18_34", "EDAD35_54"):
        shares = [estimate["p"] for name, estimate in estimates.items()
                  if name.startswith(f"P16-FIRST-{segment}-")]
        assert len(shares) == 5
        assert math.isclose(sum(shares), 1.0, abs_tol=3e-12)
    assert estimates["P17-TOTAL"]["n_valido"] == 5704
    assert values["RESULT-MOTRAL15-G-JOIN-DUPLICADOS"] == 0
    print("OK: 32 estimandos publicados e invariantes P16/P17/cruce")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
