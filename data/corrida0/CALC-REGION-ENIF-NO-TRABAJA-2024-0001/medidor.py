"""Horizonte corto ENIF 2024 entre personas que no trabajan, por región."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, REGIONES_ENIF_2024


def dominio(d):
    p38, p39, p410 = (d[c].str.strip() for c in ("P3_8", "P3_9", "P4_10"))
    trabaja = p38.isin(["1", "2"]) | p39.isin(["1", "2", "3", "4", "5", "6"])
    no_trabaja = p38.eq("8") | p39.eq("7")
    valido = p410.isin(["1", "2", "3", "4", "5"])
    if (valido & trabaja.eq(no_trabaja)).any():
        raise RuntimeError("P3_8/P3_9 no particionan P4_10 válido como CALC-ENIF-0002")
    den = valido & no_trabaja
    return den, den & p410.isin(["1", "2"])


def medir(inputs, contrato):
    par = contrato["parametros"]
    if par["conducta"] != "horizonte_corto_no_trabaja":
        raise RuntimeError("conducta diferente de la congelada")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    cols = ["REGION", "P3_8", "P3_9", "P4_10", "FAC_PER", "EST_DIS", "UPM_DIS"]
    d = _csv_zip(ruta, "TMODULO.csv", cols)
    den, y = dominio(d)
    filas, meta = estima_dominios(d, d["REGION"], den, y, factor="FAC_PER",
        estrato="EST_DIS", upm="UPM_DIS", dominios=REGIONES_ENIF_2024,
        representativos=set(REGIONES_ENIF_2024), semilla=int(contrato["seed"]["valor"]),
        replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]))
    pref = "RESULT-REGION-ENIF-2024-horizonte_corto_no_trabaja"
    out = {pref + "-JSON": json.dumps({"filas": filas, "diseno": meta},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"))}
    for fila in filas:
        base = pref + "-" + fila["geografia"]
        out.update({base + "-P": fila["punto"], base + "-IC-LO": fila["ic_inf"],
            base + "-IC-HI": fila["ic_sup"], base + "-N": fila["n"],
            base + "-ESTADO": fila["estado"],
            base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return out
