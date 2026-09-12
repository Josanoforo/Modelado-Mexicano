#!/usr/bin/env python3
"""Control independiente de dos cocientes SHED; no importa el medidor."""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True)
    parser.add_argument("--resultados", required=True)
    parser.add_argument("--salida")
    args = parser.parse_args(argv)
    with zipfile.ZipFile(args.zip) as zf:
        rows = list(csv.DictReader(io.TextIOWrapper(zf.open("public2025.csv"), encoding="utf-8-sig")))
    sealed = json.loads(Path(args.resultados).read_text(encoding="utf-8"))["resultados"]

    def weight(row):
        return float(row["weight"])

    use_den = [row for row in rows if row["BNPL1"] in {"Yes", "No"}]
    use_num = [row for row in use_den if row["BNPL1"] == "Yes"]
    use = sum(map(weight, use_num)) / sum(map(weight, use_den))

    # Fórmula deliberadamente independiente: BK2_f=Yes ya acredita cuenta y
    # sobregiro previo; no reutiliza el predicado del medidor.
    nsf_den = [
        row for row in rows
        if row["BNPL1"] == "Yes" and row["BK2_f"] == "Yes"
        and row["BNPL1A"] in {"Yes", "No"}
    ]
    nsf_num = [row for row in nsf_den if row["BNPL1A"] == "Yes"]
    nsf = sum(map(weight, nsf_num)) / sum(map(weight, nsf_den))
    refused_valid = [
        row for row in rows
        if row["BNPL1"] == "Yes" and row["BNPL3"] == "Refused"
        and row["BNPL3A"] in {"Yes", "No"}
    ]
    checks = {
        "control": "lectura_csv_y_cocientes_directos_sin_importar_medidor",
        "n_filas": len(rows),
        "uso": {"n_denominador": len(use_den), "n_numerador": len(use_num), "p": round(use, 12)},
        "sobregiro": {"n_denominador": len(nsf_den), "n_numerador": len(nsf_num), "p": round(nsf, 12)},
        "cargo_ruta_rechazo_n_valido": len(refused_valid),
    }
    expected = {
        "uso_n": sealed["RESULT-SHED-BNPL-USO-N-VALIDO"],
        "uso_y": sealed["RESULT-SHED-BNPL-USO-N-POSITIVOS"],
        "uso_p": sealed["RESULT-SHED-BNPL-USO-PUNTO"],
        "nsf_n": sealed["RESULT-SHED-BNPL-SOBREGIRO-N-VALIDO"],
        "nsf_y": sealed["RESULT-SHED-BNPL-SOBREGIRO-N-POSITIVOS"],
        "nsf_p": sealed["RESULT-SHED-BNPL-SOBREGIRO-PUNTO"],
        "refused": sealed["RESULT-SHED-BNPL-CARGO-RUTA-RECHAZO-N-VALIDO"],
    }
    checks["coincide_result_sellado"] = (
        (len(use_den), len(use_num), round(use, 12)) == (expected["uso_n"], expected["uso_y"], expected["uso_p"])
        and (len(nsf_den), len(nsf_num), round(nsf, 12)) == (expected["nsf_n"], expected["nsf_y"], expected["nsf_p"])
        and len(refused_valid) == expected["refused"]
    )
    if not checks["coincide_result_sellado"]:
        raise SystemExit("NO-COINCIDE con RESULT sellado")
    rendered = json.dumps(checks, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.salida:
        target = Path(args.salida)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
