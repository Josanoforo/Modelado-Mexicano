#!/usr/bin/env python3
"""Vocabulario de columnas REALES por paquete (solo encabezados, ninguna fila): lo usa la auditoría
de compara.py para detectar en el código de la reconstructora columnas leídas sin autorización.
Uso: vocabulario.py <REC> → escribe vocabulario-columnas.json junto a este archivo."""
import json, sys
from pathlib import Path
import pyreadstat
from dbfread import DBF

REC = Path(sys.argv[1]); AQUI = Path(__file__).resolve().parent
out = {}
for cfg in sorted((AQUI / "paquetes").glob("*.json")):
    c = json.loads(cfg.read_text()); cols = set()
    for d in c["datos"]:
        p = REC / c["paquete"] / "paquete" / d["dst"]; s = p.suffix.lower()
        if s == ".csv":
            with open(p, "rb") as fh:
                cab = fh.read(65536).replace(b"\r", b"\n").split(b"\n")[0].decode("latin-1")
            cols |= {x.strip().strip('"').lstrip("﻿").lstrip("ï»¿") for x in cab.split(",")}
        elif s == ".dbf":
            cols |= set(DBF(str(p), load=False).field_names)
        elif s in (".dta", ".sav"):
            _, meta = (pyreadstat.read_dta if s == ".dta" else pyreadstat.read_sav)(str(p), metadataonly=True)
            cols |= set(meta.column_names)
    out[c["paquete"]] = sorted(x for x in cols if x)
    print(c["paquete"], len(out[c["paquete"]]))
(AQUI / "vocabulario-columnas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
