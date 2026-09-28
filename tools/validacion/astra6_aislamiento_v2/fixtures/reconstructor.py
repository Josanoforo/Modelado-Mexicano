"""Ejemplo exclusivamente sintético; no abre insumos del proyecto."""
import csv
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path
entrada = Path(sys.argv[1])
rows = list(csv.DictReader(entrada.open()))
value = sum(Decimal(r["valor"]) * Decimal(r["peso"]) for r in rows) / sum(Decimal(r["peso"]) for r in rows)
output = {"version": 2, "identidad": {"paquete": "SINTETICO-1", "version_entrada": "1", "sha256_entrada": hashlib.sha256(entrada.read_bytes()).hexdigest()}, "filas": [{"llave": "media", "unidad": "proporcion", "estado": "RECONSTRUIDO", "punto": str(value), "estado_ic": "SIN-IC"}]}
Path(sys.argv[2]).write_text(json.dumps(output, indent=2) + "\n")
