#!/usr/bin/env python3
"""IMOR de consumo por tipo de cartera, Total Banca Multiple, CNBV 040-1A-R16
(foto 2021-12), para las afirmaciones DINERO/CNBV de la cola v1.1.

ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1. SERIE-ADMINISTRATIVA: la unidad es
el SALDO de cartera, no la persona; ningun RESULT de aqui se promedia con un
piso de encuesta (§4 v2.16).
"""
from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path

CALC_ID = "CALC-CNBV-SERIES-IMOR-R16-0001"
INPUT_ID = "IN-CNBV-R16-IMOR-CONSUMO-202112"
EXPECTED_SHA256 = "e61c97a3acd6634e2c0cabdad18a9fbde06ff58f1c2363a3e290c3cc40e23400"
PRODUCTOS = {"CON": "Cartera total de consumo", "TDC": "Tarjeta de Crédito", "PER": "Personales",
             "NOM": "Nómina", "ABCD": "ABCD", "AUT": "Automotriz", "BM": "Adq. de Bienes Muebles",
             "OTR": "Otros Créditos de Consumo"}
VACIO_DECLARADO = "Ops de Arrendamiento Capitalizable"
FECHA = "2021-12"


def medir(inputs: dict, contrato: dict) -> dict:
    e = inputs[INPUT_ID]
    raw = e.get("bytes")
    if raw is None:
        raw = Path(e["ruta_absoluta"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("SHA-256 inesperado del insumo")
    filas = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    s, vacios = {}, []
    for f in filas:
        if f["fecha"] != FECHA or f["unidad"] != "porcentaje":
            raise ValueError(f"fila inesperada: {f}")
        if f["valor"] == "":
            vacios.append(f["producto_universo"])
            continue
        v = float(f["valor"])
        if not 0.0 <= v <= 100.0:
            raise ValueError(f"fuera de rango: {f}")
        s[f["producto_universo"]] = v
    if vacios != [VACIO_DECLARADO] or set(s) != set(PRODUCTOS.values()):
        raise ValueError(f"universo de productos inesperado: {sorted(s)} vacios={vacios}")
    out = {"RESULT-CNBV-SERIES-G-INPUT-SHA256": hashlib.sha256(raw).hexdigest(),
           "RESULT-CNBV-SERIES-G-N-PRODUCTOS": len(s),
           "RESULT-CNBV-SERIES-G-N-VACIOS": len(vacios),
           "RESULT-CNBV-SERIES-G-UNIDAD": "SERIE-ADMINISTRATIVA; porcentaje de saldo de cartera; "
                                          "Total Banca Multiple; no es encuesta ni persona"}
    for cod, prod in PRODUCTOS.items():
        out[f"RESULT-CNBV-SERIES-{cod}-{FECHA}"] = s[prod]
    return out


if __name__ == "__main__":
    ruta = Path(__file__).parent / "insumos" / "cnbv-imor-consumo.csv"
    for k, v in medir({INPUT_ID: {"bytes": ruta.read_bytes()}}, {}).items():
        print(k, v, sep="\t")
