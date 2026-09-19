#!/usr/bin/env python3
"""Recalcula puntos y denominadores sin importar medidor.py."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import zipfile
from pathlib import Path

import pandas as pd


VARS = ["v21", "v22", "v23", "v24", "v25"]
DOMAINS = {"TOTAL": None, "HOMBRES": 1, "MUJERES": 2}


def rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=0, abs_tol=1e-10)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dta-zip", required=True, type=Path)
    parser.add_argument("--distribution", required=True, type=Path)
    parser.add_argument("--family", required=True, type=Path)
    parser.add_argument("--counts", required=True, type=Path)
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.dta_zip) as archive:
        raw = archive.read("ZA6980_v2-0-0.dta")
    cols = ["country", "c_alphan", "CASEID", "SEX", "WEIGHT", *VARS]
    frame = pd.read_stata(io.BytesIO(raw), columns=cols, convert_categoricals=False)
    frame = frame.loc[frame["c_alphan"].astype(str).eq("MX") & pd.to_numeric(frame["country"], errors="coerce").eq(484)].copy()
    for col in ["SEX", "WEIGHT", *VARS]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    published, family, counts, matrix = rows(args.distribution), rows(args.family), rows(args.counts), rows(args.matrix)
    max_delta = 0.0
    for variable in VARS:
        for domain, sex in DOMAINS.items():
            part = frame if sex is None else frame.loc[frame["SEX"].eq(sex)]
            wok = part["WEIGHT"].notna() & part["WEIGHT"].map(math.isfinite) & part["WEIGHT"].gt(0)
            valid = wok & part[variable].isin(range(1, 8))
            dm = float(part.loc[valid, "WEIGHT"].sum())
            subset = [r for r in published if r["variable"] == variable and r["dominio_id"] == domain]
            if len(subset) != 7 or not close(sum(float(r["proporcion"]) for r in subset), 1):
                raise SystemExit(f"CONTROL-FALLA:PARTICION:{variable}:{domain}")
            for code in range(1, 8):
                mask = valid & part[variable].eq(code)
                row = next(r for r in subset if int(r["codigo"]) == code)
                point = float(part.loc[mask, "WEIGHT"].sum()) / dm
                max_delta = max(max_delta, abs(float(row["proporcion"]) - point))
                if int(row["n_denominador"]) != int(valid.sum()) or int(row["n_numerador"]) != int(mask.sum()):
                    raise SystemExit(f"CONTROL-FALLA:N:{variable}:{domain}:{code}")
            frow = next(r for r in family if r["variable"] == variable and r["dominio_id"] == domain)
            fmask = valid & part[variable].isin([1, 2])
            if not close(frow["proporcion"], float(part.loc[fmask, "WEIGHT"].sum()) / dm):
                raise SystemExit(f"CONTROL-FALLA:FAMILIA:{variable}:{domain}")
    wok = frame["WEIGHT"].notna() & frame["WEIGHT"].map(math.isfinite) & frame["WEIGHT"].gt(0)
    complete = wok.copy()
    for variable in VARS:
        complete &= frame[variable].isin(range(1, 8))
    comp = frame.loc[complete].copy()
    comp["count"] = sum(comp[v].eq(7).astype(int) for v in VARS)
    if sum(int(r["n_numerador"]) for r in counts) != len(comp):
        raise SystemExit("CONTROL-FALLA:CONTEO")
    for r in matrix:
        expected = int((comp[r["variable_fila"]].eq(7) & comp[r["variable_columna"]].eq(7)).sum())
        if int(r["n_numerador"]) != expected or int(r["n_denominador"]) != len(comp):
            raise SystemExit("CONTROL-FALLA:MATRIZ")
    result = {"control_id": "CONTROL-INDEPENDIENTE-ISSP-REDES-0001", "estado": "CONTROL-INDEPENDIENTE-OK", "no_importa_medidor": True, "n_mexico": len(frame), "n_casos_completos": len(comp), "max_delta_punto": max_delta, "particiones": True, "agregado_familia": True, "conteo": True, "matriz": True}
    raw_out = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(raw_out, encoding="utf-8")
    print(raw_out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
