"""Control post-sello de ENSAFI sin importar el medidor primario."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import zipfile
from collections import defaultdict
from pathlib import Path

from scipy.stats import t as student_t


CONFIG = [
    ("HOG-FORMAL", "THOGAR.csv", "FAC_HOG", "P4_7_1", {"1"}, "P4_8_1"),
    ("HOG-CAJA-FAMILIA", "THOGAR.csv", "FAC_HOG", "P4_7_2", {"1"}, "P4_8_2"),
    ("HOG-EMPENO", "THOGAR.csv", "FAC_HOG", "P4_7_3", {"1"}, "P4_8_3"),
    ("HOG-PRESTAMISTA", "THOGAR.csv", "FAC_HOG", "P4_7_4", {"1"}, "P4_8_4"),
    ("PER-ATRASO", "TMODULO.csv", "FAC_ELE", "P6_8", {"1", "2", "3", "4"}, "P6_7"),
] + [
    (f"PER-AFR-{i}", "TMODULO.csv", "FAC_ELE", "P6_9", {"2"}, f"P6_10_{i}")
    for i in range(1, 9)
]
PREFIX = "RESULT-ENSAFI-DIS-"


def code(value):
    return "" if value is None else str(value).strip()


def weight(value):
    try:
        result = float(code(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) and result > 0 else None


def read_tables(path):
    tables = {}
    with zipfile.ZipFile(path) as zf:
        for table in ("THOGAR.csv", "TMODULO.csv"):
            member = next(name for name in zf.namelist() if name.rsplit("/", 1)[-1] == table)
            raw = zf.read(member)
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("latin-1")
            tables[table] = list(csv.DictReader(io.StringIO(text, newline="")))
    return tables


def independent(rows, weight_col, exposure_col, exposure_values, response_col):
    exposed = [r for r in rows if code(r[exposure_col]) in exposure_values]
    valid = [r for r in exposed if code(r[response_col]) in {"1", "2"}]
    unknown = [r for r in exposed if code(r[response_col]) not in {"1", "2"}]
    domain = [(r, weight(r[weight_col])) for r in valid]
    domain = [(r, w) for r, w in domain if w is not None]
    denominator = math.fsum(w for _, w in domain)
    numerator_rows = [(r, w) for r, w in domain if code(r[response_col]) == "1"]
    numerator = math.fsum(w for _, w in numerator_rows)
    p_hat = numerator / denominator

    clusters = defaultdict(float)
    psus_by_stratum = defaultdict(set)
    for r in rows:
        w = weight(r[weight_col])
        if w is None:
            continue
        h, u = code(r["EST_DIS"]), code(r["UPM_DIS"])
        if not h or not u:
            continue
        psus_by_stratum[h].add(u)
        if code(r[exposure_col]) in exposure_values and code(r[response_col]) in {"1", "2"}:
            y = 1.0 if code(r[response_col]) == "1" else 0.0
            clusters[h, u] += w * (y - p_hat) / denominator
        else:
            clusters[h, u] += 0.0
    variance_terms = []
    for h, psus in psus_by_stratum.items():
        values = [clusters[h, u] for u in psus]
        if len(values) < 2:
            continue
        center = math.fsum(values) / len(values)
        variance_terms.append(
            len(values) / (len(values) - 1) * math.fsum((v - center) ** 2 for v in values)
        )
    se = math.sqrt(math.fsum(variance_terms))
    df = sum(max(0, len(psus) - 1) for psus in psus_by_stratum.values())
    critical = float(student_t.ppf(0.975, df))
    return {
        "N-EXPUESTO": len(exposed),
        "N-VALIDO": len(valid),
        "N-DESCONOCIDO": len(unknown),
        "MASA-DESCONOCIDO": math.fsum(weight(r[weight_col]) or 0 for r in unknown),
        "N-NUMERADOR": len(numerator_rows),
        "MASA-NUMERADOR": numerator,
        "MASA-DENOMINADOR": denominator,
        "P": p_hat,
        "EE": se,
        "IC95-LO": max(0.0, p_hat - critical * se),
        "IC95-HI": min(1.0, p_hat + critical * se),
        "GL": df,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    raw = repo / "data/raw/ensafi2023/ensafi_2023_bd_csv.zip"
    sealed_path = repo / "data/corrida0/CALC-ENSAFI-DISENO-0001/resultados.json"
    sealed = json.loads(sealed_path.read_text(encoding="utf-8"))["resultados"]
    tables = read_tables(raw)

    max_numeric_delta = 0.0
    compared = 0
    per_estimate = {}
    for name, table, wcol, xcol, xvalues, ycol in CONFIG:
        got = independent(tables[table], wcol, xcol, xvalues, ycol)
        deltas = {}
        for suffix, value in got.items():
            observed = sealed[PREFIX + name + "-" + suffix]
            delta = abs(float(observed) - float(value))
            deltas[suffix] = delta
            max_numeric_delta = max(max_numeric_delta, delta)
            compared += 1
        per_estimate[name] = {"max_delta": max(deltas.values()), "campos": len(deltas)}

    result = {
        "control": "VALIDACION-INDEPENDIENTE-COINCIDE" if max_numeric_delta <= 1e-10 else "DISCREPA",
        "implementacion": "separada; no importa medidor.py",
        "estimandos": len(CONFIG),
        "campos_numericos_comparados": compared,
        "tolerancia_abs": 1e-10,
        "max_delta": max_numeric_delta,
        "diseno": {
            "estratos": sealed[PREFIX + "PER-N-ESTRATOS"],
            "upm_anidadas": sealed[PREFIX + "PER-N-UPM-ANIDADAS"],
            "grados_libertad": sealed[PREFIX + "PER-GL"],
            "singleton": sealed[PREFIX + "PER-N-ESTRATOS-SINGLETON"],
        },
        "por_estimando": per_estimate,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    raise SystemExit(0 if result["control"].endswith("COINCIDE") else 1)


if __name__ == "__main__":
    main()
