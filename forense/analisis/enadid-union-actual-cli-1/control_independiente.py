#!/usr/bin/env python3
"""Control de puntos y denominadores; no importa el medidor ni sus helpers."""
import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path


VALID = set("1234567")
AGES = (("15_17", 15, 17), ("18_29", 18, 29), ("30_44", 30, 44),
        ("45_59", 45, 59), ("60_mas", 60, 120), ("15_mas", 15, 120))


def main(zip_path: str, expected_csv: str, output: str) -> None:
    totals = {}
    with zipfile.ZipFile(zip_path) as zf, zf.open("TSDEM.csv") as raw:
        reader = csv.DictReader((line.decode("utf-8-sig") for line in raw))
        for row in reader:
            try:
                age, weight = int(row["EDAD"]), float(row["FAC_VIV"])
            except (ValueError, TypeError):
                continue
            if weight <= 0:
                continue
            status = row["P3_27"].strip()
            for age_id, low, high in AGES:
                if low <= age <= high:
                    cell = totals.setdefault(age_id, {"valid_n": 0, "valid_w": 0.0,
                        "pair_n": 0, "pair_w": 0.0, "libre_n": 0, "libre_w": 0.0})
                    if status in VALID:
                        cell["valid_n"] += 1; cell["valid_w"] += weight
                    if status in {"1", "6"}:
                        cell["pair_n"] += 1; cell["pair_w"] += weight
                    if status == "1":
                        cell["libre_n"] += 1; cell["libre_w"] += weight
    with open(expected_csv, encoding="utf-8", newline="") as handle:
        published = list(csv.DictReader(handle))
    checks = []
    for age_id, values in totals.items():
        gross = next(r for r in published if r["estimando"] == "distribucion_actual_15_mas" and r["categoria"] == "union_libre" and r["edad"] == age_id)
        conditional = next(r for r in published if r["estimando"] == "union_libre_entre_union_o_casada" and r["categoria"] == "union_libre" and r["edad"] == age_id)
        checks.append({"edad": age_id,
            "denominador_bruto_n_ok": int(gross["n_valido"]) == values["valid_n"],
            "denominador_condicional_n_ok": int(conditional["n_valido"]) == values["pair_n"],
            "punto_bruto_ok": abs(float(gross["punto"]) - values["libre_w"] / values["valid_w"]) < 5e-12,
            "punto_condicional_ok": abs(float(conditional["punto"]) - values["libre_w"] / values["pair_w"]) < 5e-12})
    result = {"metodo": "csv-modulo-estandar; sin importar medidor.py", "checks": checks,
              "todos_ok": all(all(v for k, v in item.items() if k != "edad") for item in checks)}
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result["todos_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main(*sys.argv[1:])
