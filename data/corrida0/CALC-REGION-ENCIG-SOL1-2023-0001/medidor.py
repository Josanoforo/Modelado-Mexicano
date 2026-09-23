"""Solicitud inicial P8_3_1 ENCIG 2021/23 por entidad de residencia."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, ENTIDADES

ADAPTER = {
    2021: ("conjunto_de_datos_encig2021_01_sec1_A_3_4_5_8_9_10.csv", "ENT"),
    2023: ("encig2023_01_sec1_A_3_4_5_8_9_10.csv", "CVE_ENT"),
}


def desenlace(code):
    c = code.str.strip()
    den = c.isin(["1", "2"])
    return den, den & c.eq("1")


def medir(inputs, contrato):
    par = contrato["parametros"]
    year = int(par["ola"])
    if year not in ADAPTER or par["conducta"] != "paga_mordida_encig2025":
        raise RuntimeError("ola o conducta distinta del freeze")
    member, geo_col = ADAPTER[year]
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    d = _csv_zip(ruta, member, [geo_col, "P8_3_1", "FAC_P18", "EST_DIS", "UPM_DIS"])
    den, y = desenlace(d["P8_3_1"])
    filas, meta = estima_dominios(d, d[geo_col].str.zfill(2), den, y,
        factor="FAC_P18", estrato="EST_DIS", upm="UPM_DIS", dominios=ENTIDADES,
        representativos=set(ENTIDADES), semilla=int(contrato["seed"]["valor"]),
        replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]))
    pref = f"RESULT-REGION-ENCIG-SOL1-{year}"
    out = {pref + "-JSON": json.dumps({"filas": filas, "diseno": meta,
        "unidad": "persona", "reactivo": "P8_3_1 primer inciso de solicitud"},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"))}
    for fila in filas:
        base = pref + "-" + fila["geografia"]
        out.update({base + "-P": fila["punto"], base + "-IC-LO": fila["ic_inf"],
            base + "-IC-HI": fila["ic_sup"], base + "-N": fila["n"],
            base + "-ESTADO": fila["estado"],
            base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return out
