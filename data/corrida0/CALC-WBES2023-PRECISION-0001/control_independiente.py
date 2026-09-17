"""Cotejo acotado de precisión sin importar el medidor sucesor."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import zipfile
from pathlib import Path

import pandas as pd
from scipy.stats import t as student_t


PAIRS = (("c3", "c5"), ("c12", "c14"), ("g2", "g4"),
         ("j3", "j5"), ("j10", "j12"), ("j13", "j15"))
DOMAINS = (("TOTAL", None), ("PEQUENA", 1), ("MEDIANA", 2),
           ("GRANDE", 3), ("EXTRA-GRANDE", 4))


def composite(row):
    outcomes = []
    for parent, event in PAIRS:
        if row[parent] == 1:
            outcomes.append(row[event])
    if not outcomes:
        return None
    if any(value == 1 for value in outcomes):
        return 1
    if all(value == 2 for value in outcomes):
        return 0
    return None


def independent(frame, size_code, scenario):
    outcome = frame.apply(composite, axis=1)
    in_size = pd.Series(True, index=frame.index) if size_code is None else frame.a6a.eq(size_code)
    x = (in_size & outcome.isin((0, 1))).astype(float)
    y = (in_size & outcome.eq(1)).astype(float)
    yes = y.eq(1)
    no = x.eq(1) & ~yes
    numerator = float(frame.loc[yes, "wmedian"].sum())
    denominator = numerator + float(frame.loc[no, "wmedian"].sum())
    point = numerator / denominator
    z = frame.wmedian * (y - point * x) / denominator
    terms = []
    singleton = 0
    for _, values in z.groupby(frame.strata):
        n_h = len(values)
        if n_h == 1:
            singleton += 1
            continue
        center = float(values.sum()) / n_h
        terms.append(n_h / (n_h - 1) * math.fsum((float(v) - center) ** 2 for v in values))
    variance = math.fsum(terms)
    if scenario == "SINGLETON-AVERAGE":
        variance *= (len(terms) + singleton) / len(terms)
    se = math.sqrt(variance)
    df = len(frame) - frame.strata.nunique()
    critical = float(student_t.ppf(0.975, df))
    logit = math.log(point / (1 - point))
    se_logit = se / (point * (1 - point))
    inverse = lambda value: 1 / (1 + math.exp(-value))
    return point, se, inverse(logit - critical * se_logit), inverse(logit + critical * se_logit)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    zip_path = repo / "data/raw/WBES_Mexico2023_Data.zip"
    columns = {"wmedian", "a6a", "strata", *(name for pair in PAIRS for name in pair)}
    with zipfile.ZipFile(zip_path) as zf:
        frame = pd.read_stata(
            io.BytesIO(zf.read("Mexico-2023-full-data.dta")),
            columns=sorted(columns), convert_categoricals=False,
        )
    csv_path = repo / "forense/analisis/wbes2023-precision-1/wbes2023-precision.csv"
    with csv_path.open(encoding="utf-8", newline="") as handle:
        observed = {(row["dominio_id"], row["escenario_singleton"]): row
                    for row in csv.DictReader(handle)}
    deltas = []
    compared = 0
    for domain, size_code in DOMAINS:
        for scenario in ("SINGLETON-CERTEZA", "SINGLETON-AVERAGE"):
            expected = independent(frame, size_code, scenario)
            row = observed[domain, scenario]
            for field, value in zip(
                ("punto_sucesor", "ee", "ic95_inferior", "ic95_superior"), expected
            ):
                deltas.append(abs(float(row[field]) - value))
                compared += 1
    max_delta = max(deltas)
    result = {
        "control": "VALIDACION-INDEPENDIENTE-COINCIDE" if max_delta <= 1e-10 else "DISCREPA",
        "implementacion": "separada; no importa medidor.py del sucesor",
        "dominios": len(DOMAINS),
        "escenarios": 2,
        "campos_numericos_comparados": compared,
        "tolerancia_abs": 1e-10,
        "max_delta": max_delta,
    }
    raw = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output = args.output or repo / "forense/analisis/wbes2023-precision-1/control-independiente.json"
    output.write_text(raw, encoding="utf-8")
    print(raw, end="")
    raise SystemExit(0 if result["control"].endswith("COINCIDE") else 1)


if __name__ == "__main__":
    main()
