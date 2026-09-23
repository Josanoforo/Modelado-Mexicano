"""Punto ponderado precongelado de P8_3, ENCIG 2023; una tabla de persona."""
from __future__ import annotations

import collections
import csv
import io
import math
import zipfile

ZIP_ID = "encig23_base_datos_csv"
MEMBER = "encig2023_01_sec1_A_3_4_5_8_9_10.csv"
FIELDS = ("P8_3_1", "P8_3_2", "P8_3_3", "FAC_P18", "EST_DIS", "UPM_DIS")
PREFIX = "RESULT-RELEVO-ENCIG23-P83-"


def medir(inputs, contrato):
    counts = [collections.Counter() for _ in range(3)]
    n = n_weight = n_any = n_one = n_design_missing = 0
    w_any = w_any_yes = w_one = w_one_yes = 0.0
    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as archive:
        members = [m for m in archive.namelist() if m.rsplit("/", 1)[-1].lower() == MEMBER]
        if len(members) != 1:
            raise ValueError(f"miembro no único: {MEMBER}: {len(members)}")
        with archive.open(members[0]) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="latin-1", newline=""))
            if reader.fieldnames is None:
                raise ValueError("CSV sin cabecera")
            cols = {s.lstrip("\ufeff").lstrip("ï»¿").strip().upper(): s for s in reader.fieldnames}
            absent = set(FIELDS) - set(cols)
            if absent:
                raise ValueError(f"columnas ausentes: {sorted(absent)}")
            for row in reader:
                n += 1
                vals = tuple(row[cols[f]].strip() for f in FIELDS[:3])
                for counter, value in zip(counts, vals):
                    token = value.upper()
                    if token not in {"1", "2", "9", "NA", "", "B"}:
                        raise ValueError(f"código inesperado en P8_3: {token!r}")
                    counter[token or "BLANCO"] += 1
                raw_weight = row[cols["FAC_P18"]].strip().replace(",", "")
                try:
                    weight = float(raw_weight)
                except ValueError:
                    continue
                if not math.isfinite(weight) or weight <= 0:
                    continue
                n_weight += 1
                if not row[cols["EST_DIS"]].strip() or not row[cols["UPM_DIS"]].strip():
                    n_design_missing += 1
                if vals[0] in {"1", "2"}:
                    n_one += 1
                    w_one += weight
                    if vals[0] == "1":
                        w_one_yes += weight
                if all(x in {"1", "2"} for x in vals):
                    n_any += 1
                    w_any += weight
                    if "1" in vals:
                        w_any_yes += weight
    if not w_any or not w_one:
        raise ValueError("denominador vacío")
    if n_any > n_weight or n_one > n_weight or n_design_missing > n_weight:
        raise AssertionError("conteos no cierran")
    p_any = w_any_yes / w_any
    p_one = w_one_yes / w_one
    out = {
        "N-PERSONAS": n, "N-PESO-VALIDO": n_weight,
        "N-SOLANY": n_any, "N-SOL1": n_one,
        "N-DISENO-FALTANTE": n_design_missing,
        "W-SOLANY-DEN": w_any, "W-SOLANY-NUM": w_any_yes,
        "W-SOL1-DEN": w_one, "W-SOL1-NUM": w_one_yes,
        "P-SOLANY": p_any, "P-NO-SOLANY": 1 - p_any,
        "P-SOL1": p_one, "DELTA-SOLANY-VS-PRIOR-PAGO": p_any - 0.62,
        "DELTA-NO-SOLANY-VS-PRIOR-NORMAL": (1 - p_any) - 0.38,
        "SOPORTE-1": ";".join(f"{k}:{v}" for k, v in sorted(counts[0].items())),
        "SOPORTE-2": ";".join(f"{k}:{v}" for k, v in sorted(counts[1].items())),
        "SOPORTE-3": ";".join(f"{k}:{v}" for k, v in sorted(counts[2].items())),
        "CORRESPONDENCIA-RES-0001": "NO-EQUIVALENTE-PAGO",
        "CORRESPONDENCIA-RES-0002": "NO-EQUIVALENTE-PAGO",
    }
    return {PREFIX + key: value for key, value in out.items()}
