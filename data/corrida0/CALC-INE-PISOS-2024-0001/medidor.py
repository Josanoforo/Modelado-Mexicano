"""Conteo administrativo INE 2024, sin inferencia individual ni muestral."""
from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import defaultdict
from itertools import chain

PID = "ine_conteos_censales_participacion_2024"
REQUIRED = {"AELEC", "EDOCVE", "SEXO", "LN", "SV", "NV", "NS"}


def _integer(value):
    v = str(value).strip()
    if not v or not v.isdigit():
        raise ValueError(f"conteo administrativo no entero: {v[:30]}")
    return int(v)


def _rows(handle):
    stream = io.TextIOWrapper(handle, encoding="utf-8-sig", errors="replace", newline="")
    header = stream.readline()
    delimiter = max((",", ";", "\t"), key=header.count)
    if header.count(delimiter) < 2:
        raise ValueError("delimitador no identificable")
    reader = csv.DictReader(chain((header,), stream), delimiter=delimiter)
    names = {x.strip().upper(): x for x in reader.fieldnames or []}
    if not REQUIRED.issubset(names):
        raise ValueError(f"columnas faltantes: {sorted(REQUIRED - set(names))}")
    for row in reader:
        yield {k: row[v] for k, v in names.items() if k in REQUIRED}


def medir(inputs, contrato):
    counts = defaultdict(lambda: [0, 0, 0, 0])  # LN, SV, NV, NS
    anomalous = 0
    rows2024 = 0
    path = inputs[PID]["ruta_absoluta"]
    with zipfile.ZipFile(path) as archive:
        members = sorted(n for n in archive.namelist() if n.lower().endswith(".csv"))
        if len(members) != 32:
            raise ValueError(f"se esperaban 32 archivos estatales: {len(members)}")
        for member in members:
            with archive.open(member) as raw:
                for row in _rows(raw):
                    if str(row["AELEC"]).strip() != "2024":
                        continue
                    rows2024 += 1
                    state = str(row["EDOCVE"]).strip().zfill(2)
                    sex = str(row["SEXO"]).strip()
                    if state not in {f"{i:02d}" for i in range(1, 33)} or sex not in {"0", "1", "2"}:
                        raise ValueError(f"código entidad/sexo fuera de contrato: {state}/{sex}")
                    vals = [_integer(row[k]) for k in ("LN", "SV", "NV", "NS")]
                    if vals[0] != sum(vals[1:]):
                        anomalous += 1
                    for key in (("nacional", "total"), ("nacional", sex), (state, "total"), (state, sex)):
                        for j, value in enumerate(vals):
                            counts[key][j] += value
    if rows2024 == 0:
        raise ValueError("sin filas 2024")
    cells = []
    for (geo, sex), (ln, sv, nv, ns) in sorted(counts.items()):
        if ln < 30:
            cells.append({"geo": geo, "sexo": sex, "estado": "SUPRIMIDA", "ln": ln})
        else:
            cells.append({"geo": geo, "sexo": sex, "ln": ln, "sv": sv, "nv": nv,
                          "ns": ns, "tasa_ln": sv / ln,
                          "tasa_marca_conocida": sv / (sv + nv) if sv + nv else None})
    return {
        "RESULT-INE-PISOS-2024-FILAS": rows2024,
        "RESULT-INE-PISOS-2024-DESCUADRES": anomalous,
        "RESULT-INE-PISOS-2024-TABLA": json.dumps(cells, ensure_ascii=False,
                                                sort_keys=True, separators=(",", ":")),
    }
