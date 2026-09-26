#!/usr/bin/env python3
"""IMOR de consumo por producto (Banxico, banca comercial) en los periodos que
citan las afirmaciones DINERO/BANXICO y DINERO/CNBV de la cola v1.1.

ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1. SERIE-ADMINISTRATIVA: la unidad es
el SALDO de cartera, no la persona; ningun RESULT de aqui se promedia con un
piso de encuesta (§4 v2.16).
"""
from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path

CALC_ID = "CALC-BANXICO-SERIES-IMOR-0001"
INPUT_ID = "IN-BANXICO-IMOR-CONSUMO-MENSUAL"
EXPECTED_SHA256 = "772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9"
PRODUCTOS = {"CON": "Consumo total", "TDC": "Tarjetas de crédito", "ABCD": "ABCD",
             "NOM": "Nómina", "PER": "Personales"}
# Periodos fijados en spec.md §3 antes de correr: ultimo dato y los que citan las afirmaciones.
PUNTOS = ["2026-03", "2025-09", "2024-12", "2024-03", "2024-02", "2023-12"]
ANIO_MEDIA = "2025"
YOY = ("2026-03", "2025-03")


def serie(raw: bytes) -> dict:
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("SHA-256 inesperado del insumo")
    filas = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(filas) != 615:
        raise ValueError(f"filas inesperadas: {len(filas)}")
    s: dict = {}
    for f in filas:
        if f["unidad"] != "porcentaje" or f["indicador"] != "IMOR":
            raise ValueError(f"unidad/indicador inesperado: {f}")
        k = (f["producto"], f["fecha"])
        if k in s:
            raise ValueError(f"duplicado {k}")
        v = float(f["valor"])
        if not 0.0 <= v <= 100.0:
            raise ValueError(f"fuera de rango {k}: {v}")
        s[k] = v
    return s


def medir(inputs: dict, contrato: dict) -> dict:
    e = inputs[INPUT_ID]
    raw = e.get("bytes")
    if raw is None:
        raw = Path(e["ruta_absoluta"]).read_bytes()
    s = serie(raw)
    out = {"RESULT-BANXICO-SERIES-G-INPUT-SHA256": hashlib.sha256(raw).hexdigest(),
           "RESULT-BANXICO-SERIES-G-N-FILAS": len(s),
           "RESULT-BANXICO-SERIES-G-CORTE": f"{min(k[1] for k in s)}..{max(k[1] for k in s)}",
           "RESULT-BANXICO-SERIES-G-UNIDAD": "SERIE-ADMINISTRATIVA; porcentaje de saldo de cartera; "
                                             "no es encuesta ni persona"}
    for cod, prod in PRODUCTOS.items():
        for p in PUNTOS:
            out[f"RESULT-BANXICO-SERIES-{cod}-{p}"] = s[(prod, p)]
        meses = [s[(prod, f"{ANIO_MEDIA}-{m:02d}")] for m in range(1, 13)]
        out[f"RESULT-BANXICO-SERIES-{cod}-MEDIA-{ANIO_MEDIA}"] = round(sum(meses) / 12, 12)
        out[f"RESULT-BANXICO-SERIES-{cod}-YOY-{YOY[0]}-PP"] = round(s[(prod, YOY[0])] - s[(prod, YOY[1])], 12)
    return out


if __name__ == "__main__":
    ruta = Path(__file__).parent / "insumos" / "banxico-imor-consumo-mensual.csv"
    for k, v in medir({INPUT_ID: {"bytes": ruta.read_bytes()}}, {}).items():
        print(k, v, sep="\t")
