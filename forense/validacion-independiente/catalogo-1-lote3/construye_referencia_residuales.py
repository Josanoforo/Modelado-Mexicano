#!/usr/bin/env python3
"""ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P1. Referencia v3 de un paquete residual desde el CALC
sellado, DESPUÉS de congelar la exportación de la reconstructora (commit 458a3440).

Por llave `<X>-P` del esquema: punto = sellado[<X>-P]; IC = sellado[<X>-IC-LO/HI] si ambos
existen (estado_ic CALCULADO), si no SIN-IC. Números como repr(float), sin redondear.
Guardia que PARA: toda llave del esquema existe en el sellado y es numérica.
Uso: construye_referencia_residuales.py <paq> <salida.json>"""
import csv
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
CALC = {"enbiare-pisos-bienestar-0001": "CALC-ENBIARE-PISOS-BIENESTAR-0001",
        "encodat-pisos-sustancias-0001": "CALC-ENCODAT-PISOS-SUSTANCIAS-0001",
        "encuci-0001": "CALC-ENCUCI-0001", "enigh-0001": "CALC-ENIGH-0001"}
AB = {"enbiare-pisos-bienestar-0001": "enbiare-l3r", "encodat-pisos-sustancias-0001": "encodat-l3r",
      "encuci-0001": "encuci-l3r", "enigh-0001": "enigh-l3r"}  # prefijo T02 de entrada/ (MAPA-NOMBRES-ENTRADA.md)
paq, out = sys.argv[1], sys.argv[2]
ident = json.loads((AQUI / paq / "entrada" / f"{AB[paq]}--identidad.json").read_text())
sell = json.loads((R / "data/corrida0" / CALC[paq] / "resultados.json").read_text())["resultados"]
esq = Path("/home/pc0/c1-sucesores-rec") / paq / "paquete/esquema-identidades.tsv"
filas = []
for r in csv.DictReader(open(esq, encoding="utf-8"), delimiter="\t"):
    k = r["llave"]
    v = sell.get(k)
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise SystemExit(f"PARO · {k} ausente o no numérica en el sellado")
    f = {"llave": k, "unidad": r["unidad"], "estado": "RECONSTRUIDO", "punto": repr(float(v))}
    base = k[:-2] if k.endswith("-P") else None
    lo, hi = (sell.get(f"{base}-IC-LO"), sell.get(f"{base}-IC-HI")) if base else (None, None)
    if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
        f.update(estado_ic="CALCULADO", ic95_inf=repr(float(lo)), ic95_sup=repr(float(hi)))
    else:
        f["estado_ic"] = "SIN-IC"
    filas.append(f)
Path(out).write_text(json.dumps({"version": 3, "identidad": ident, "filas": filas},
                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(paq, len(filas), "filas ·", sum(f["estado_ic"] == "CALCULADO" for f in filas), "con IC")
