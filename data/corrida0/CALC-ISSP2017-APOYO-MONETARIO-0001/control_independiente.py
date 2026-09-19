#!/usr/bin/env python3
"""Control independiente: no importa medidor.py ni reutiliza sus funciones."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import pandas as pd


COLUMNS = ["country", "c_alphan", "CASEID", "SEX", "WEIGHT", "v26"]
DOMAINS = {"TOTAL": None, "HOMBRES": 1, "MUJERES": 2}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        raw = archive.read("ZA6980_v2-0-0.dta")
    frame = pd.read_stata(io.BytesIO(raw), columns=COLUMNS, convert_categoricals=False)
    frame = frame.loc[frame["c_alphan"].astype(str).eq("MX") & pd.to_numeric(frame["country"], errors="coerce").eq(484)].copy()
    frame["SEX"] = pd.to_numeric(frame["SEX"], errors="coerce")
    frame["WEIGHT"] = pd.to_numeric(frame["WEIGHT"], errors="coerce")
    frame["v26"] = pd.to_numeric(frame["v26"], errors="coerce")
    return frame


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-10)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dta-zip", required=True, type=Path)
    parser.add_argument("--distribution", required=True, type=Path)
    parser.add_argument("--coverage", required=True, type=Path)
    parser.add_argument("--contrast", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    frame = read_source(args.dta_zip)
    published = read_csv(args.distribution)
    coverage = read_csv(args.coverage)
    contrast = read_csv(args.contrast)[0]
    max_point_delta = 0.0
    max_mass_delta = 0.0
    reconstruction = {}
    for domain, sex in DOMAINS.items():
        part = frame if sex is None else frame.loc[frame["SEX"].eq(sex)]
        weight_ok = part["WEIGHT"].notna() & part["WEIGHT"].map(math.isfinite) & part["WEIGHT"].gt(0)
        valid = weight_ok & part["v26"].isin([1, 2, 3, 4, 5, 6, 7])
        denominator = sum(float(w) for w in part.loc[valid, "WEIGHT"])
        rows = [row for row in published if row["dominio_id"] == domain]
        if len(rows) != 7:
            raise SystemExit(f"CONTROL-FALLA:FILAS:{domain}")
        for code in range(1, 8):
            row = next(item for item in rows if int(item["codigo"]) == code)
            mask = valid & part["v26"].eq(code)
            mass = sum(float(w) for w in part.loc[mask, "WEIGHT"])
            point = mass / denominator if denominator else None
            if int(row["n_categoria"]) != int(mask.sum()) or int(row["n_denominador_valido"]) != int(valid.sum()):
                raise SystemExit(f"CONTROL-FALLA:N:{domain}:{code}")
            max_mass_delta = max(max_mass_delta, abs(float(row["masa_categoria"]) - mass))
            if point is not None:
                max_point_delta = max(max_point_delta, abs(float(row["proporcion"]) - point))
        if not close(sum(float(row["proporcion"]) for row in rows), 1.0):
            raise SystemExit(f"CONTROL-FALLA:PARTICION:{domain}")
        crows = [row for row in coverage if row["dominio_id"] == domain]
        if sum(int(row["n"]) for row in crows) != len(part):
            raise SystemExit(f"CONTROL-FALLA:RECONCILIACION:{domain}")
        reconstruction[domain] = {
            "n": len(part),
            "masa_peso_utilizable": sum(float(w) for w in part.loc[weight_ok, "WEIGHT"]),
        }
    other = frame.loc[~frame["SEX"].isin([1, 2])]
    other_ok = other["WEIGHT"].notna() & other["WEIGHT"].map(math.isfinite) & other["WEIGHT"].gt(0)
    if reconstruction["TOTAL"]["n"] != reconstruction["HOMBRES"]["n"] + reconstruction["MUJERES"]["n"] + len(other):
        raise SystemExit("CONTROL-FALLA:RECONSTRUCCION-N")
    rebuilt_mass = reconstruction["HOMBRES"]["masa_peso_utilizable"] + reconstruction["MUJERES"]["masa_peso_utilizable"] + sum(float(w) for w in other.loc[other_ok, "WEIGHT"])
    if not close(rebuilt_mass, reconstruction["TOTAL"]["masa_peso_utilizable"]):
        raise SystemExit("CONTROL-FALLA:RECONSTRUCCION-MASA")
    p_w = next(float(row["proporcion"]) for row in published if row["dominio_id"] == "MUJERES" and row["codigo"] == "1")
    p_m = next(float(row["proporcion"]) for row in published if row["dominio_id"] == "HOMBRES" and row["codigo"] == "1")
    if not close(float(contrast["diferencia_menos_mas"]), p_w - p_m):
        raise SystemExit("CONTROL-FALLA:CONTRASTE")
    result = {
        "estado": "CONTROL-INDEPENDIENTE-OK",
        "no_importa_medidor": True,
        "n_mexico": len(frame),
        "max_delta_masa": max_mass_delta,
        "max_delta_punto": max_point_delta,
        "reconstruccion_total": True,
        "particiones": True,
        "reconciliaciones": True,
        "sha256_input_dta_zip": digest(args.dta_zip),
        "sha256_distribucion": digest(args.distribution),
        "sha256_cobertura": digest(args.coverage),
        "sha256_contraste": digest(args.contrast),
    }
    raw = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(raw, encoding="utf-8")
    print(raw, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
