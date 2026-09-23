"""Portafolio de ahorro ENIF 2024 por región oficial, unidad persona 18+."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, REGIONES_ENIF_2024

CONDUCTAS = (
    "no_tiene_ahorros_enif2024",
    "informal_cualquiera",
    "formal_cualquiera",
    "ahorra_solo_informal",
    "ahorra_solo_formal",
    "ahorra_ambas_vias",
    "no_ahorra",
)


def desenlaces(d):
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    formal = [f"P5_6_{i}" for i in range(1, 10)]
    valid = d[inf + formal].isin(["1", "2"]).any(axis=1)
    i = d[inf].eq("1").any(axis=1)
    f = d[formal].eq("1").any(axis=1)
    return valid, {
        "no_tiene_ahorros_enif2024": valid & ~i & ~f,
        "informal_cualquiera": valid & i,
        "formal_cualquiera": valid & f,
        "ahorra_solo_informal": valid & i & ~f,
        "ahorra_solo_formal": valid & f & ~i,
        "ahorra_ambas_vias": valid & i & f,
        "no_ahorra": valid & ~i & ~f,
    }


def medir(inputs, contrato):
    par = contrato["parametros"]
    if tuple(par["conductas"]) != CONDUCTAS:
        raise RuntimeError("lista de conductas distinta de la congelada")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    form = [f"P5_6_{i}" for i in range(1, 10)]
    d = _csv_zip(ruta, "TMODULO.csv",
                 ["REGION", "EDAD_V", "FAC_PER", "EST_DIS", "UPM_DIS"] + inf + form)
    valid, outcomes = desenlaces(d)
    resultados = {}
    for conducta in CONDUCTAS:
        filas, meta = estima_dominios(
            d, d["REGION"], valid, outcomes[conducta], factor="FAC_PER",
            estrato="EST_DIS", upm="UPM_DIS", dominios=REGIONES_ENIF_2024,
            representativos=set(REGIONES_ENIF_2024),
            semilla=int(contrato["seed"]["valor"]), replicas=int(par["bootstrap_replicas"]),
            n_min=int(par["n_min"]),
        )
        pref = f"RESULT-REGION-ENIF-PORT-2024-{conducta}"
        resultados[pref + "-JSON"] = json.dumps({"filas": filas, "diseno": meta},
                                                 ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            resultados.update({base + "-P": fila["punto"],
                               base + "-IC-LO": fila["ic_inf"],
                               base + "-IC-HI": fila["ic_sup"],
                               base + "-N": fila["n"],
                               base + "-ESTADO": fila["estado"],
                               base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return resultados
