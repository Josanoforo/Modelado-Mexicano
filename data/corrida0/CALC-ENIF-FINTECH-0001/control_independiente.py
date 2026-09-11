#!/usr/bin/env python3
"""Control separado para credito/app ENIF 2021; no importa el medidor."""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile

MEMBER = (
    "conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/"
    "conjunto_de_datos_tmodulo_enif_2021.csv"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_2021")
    args = parser.parse_args()
    with zipfile.ZipFile(args.zip_2021) as zf:
        raw = zf.read(MEMBER)
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = []
    for raw_row in reader:
        row = {str(k).lstrip("\ufeff").strip().upper(): str(v).strip()
               for k, v in raw_row.items()}
        try:
            weight = float(row["FAC_ELE"])
        except (KeyError, ValueError):
            continue
        if weight <= 0 or row.get("P6_2_8") != "1" or row.get("P6_7") not in set("123456"):
            continue
        rows.append((row.get("P6_7"), weight))
    denominator = sum(weight for _, weight in rows)
    app = [(channel, weight) for channel, weight in rows if channel == "2"]
    numerator = sum(weight for _, weight in app)
    print(json.dumps({
        "objeto": "credito_2021_app_celular",
        "n_numerador": len(app),
        "masa_numerador": round(numerator, 6),
        "n_denominador": len(rows),
        "masa_denominador": round(denominator, 6),
        "p": round(numerator / denominator, 12),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
