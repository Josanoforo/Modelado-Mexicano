#!/usr/bin/env python3
"""Verifica que la salida archivada de la reconstructora casa byte a byte con su SELLO.txt,
resolviendo los dos renombres de MAPA-NOMBRES.md (prefijo endireh2016-pf-l3--)."""
import hashlib, sys
from pathlib import Path
D = Path(__file__).resolve().parent / "endireh-pisos-2016-pareja-fisica-0002/reconstructora/salida"
REN = {"diagnostico.json": "endireh2016-pf-l3--diagnostico.json", "replicas.json": "endireh2016-pf-l3--replicas.json"}
mal = 0
for linea in (D / "SELLO.txt").read_text().splitlines():
    sha, nombre = linea.split(maxsplit=1)
    nombre = nombre.lstrip("*").removeprefix("salida/")
    real = D / REN.get(nombre, nombre)
    ok = real.is_file() and hashlib.sha256(real.read_bytes()).hexdigest() == sha
    mal += not ok
    print("OK " if ok else "MAL", nombre, "->", real.name)
sys.exit(1 if mal else 0)
