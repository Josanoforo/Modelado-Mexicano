"""Horizonte y desconfianza ENIF 2024 por las seis regiones oficiales."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, REGIONES_ENIF_2024

CONDUCTAS = (
    "horizonte_corto_sin_ss", "horizonte_no_corto_sin_ss",
    "horizonte_corto_con_ss", "horizonte_no_corto_con_ss",
    "desconfia_conoce_proteccion", "desconfia_no_conoce_proteccion",
)
VALIDOS_P520 = {f"{i:02}" for i in range(1, 11)}


def dominios_condicionales(d):
    edad = d["EDAD_V"].str.strip()
    adulto = edad.str.isdigit() & edad.astype(str).str.len().le(3)
    adulto &= edad.where(adulto, "0").astype(int).ge(18)
    p410 = d["P4_10"].str.strip()
    p313 = d["P3_13"].str.strip()
    p520 = d["P5_20"].str.strip().str.zfill(2)
    p523 = d["P5_23"].str.strip()
    if p523.isin(["", "b"]).any():
        raise RuntimeError("P5_23 no particiona el universo; G-C1")
    bad520 = set(p520.unique()) - VALIDOS_P520 - {"0b", "00"}
    if bad520:
        raise RuntimeError(f"P5_20 fuera del codebook: {bad520}")
    cuenta = d[[f"P5_4_{i}" for i in range(1, 10)]].eq("1").any(axis=1)
    if (p520.isin(VALIDOS_P520) & cuenta).any():
        raise RuntimeError("P5_20 contestada con cuenta declarada; G-C2")
    valido_h = adulto & p410.isin(["1", "2", "3", "4", "5"])
    sin = valido_h & p313.eq("7")
    con = valido_h & p313.isin(["1", "2", "3", "4"])
    c = adulto & p520.isin(VALIDOS_P520) & p523.eq("1")
    nc = adulto & p520.isin(VALIDOS_P520) & p523.eq("2")
    corto = p410.isin(["1", "2"])
    desc = p520.eq("03")
    return {
        "horizonte_corto_sin_ss": (sin, corto),
        "horizonte_no_corto_sin_ss": (sin, ~corto),
        "horizonte_corto_con_ss": (con, corto),
        "horizonte_no_corto_con_ss": (con, ~corto),
        "desconfia_conoce_proteccion": (c, desc),
        "desconfia_no_conoce_proteccion": (nc, desc),
    }


def medir(inputs, contrato):
    par = contrato["parametros"]
    if tuple(par["conductas"]) != CONDUCTAS:
        raise RuntimeError("conductas diferentes de la spec")
    cols = ["REGION", "EDAD_V", "FAC_PER", "EST_DIS", "UPM_DIS", "P4_10",
            "P3_13", "P5_20", "P5_23"] + [f"P5_4_{i}" for i in range(1, 10)]
    d = _csv_zip(inputs[par["input_id"]]["ruta_absoluta"], "TMODULO.csv", cols)
    definiciones = dominios_condicionales(d)
    out = {}
    for conducta, (den, y) in definiciones.items():
        filas, meta = estima_dominios(d, d["REGION"], den, y, factor="FAC_PER",
            estrato="EST_DIS", upm="UPM_DIS", dominios=REGIONES_ENIF_2024,
            representativos=set(REGIONES_ENIF_2024),
            semilla=int(contrato["seed"]["valor"]), replicas=int(par["bootstrap_replicas"]),
            n_min=int(par["n_min"]))
        pref = f"RESULT-REGION-ENIF-COND-2024-{conducta}"
        out[pref + "-JSON"] = json.dumps({"filas": filas, "diseno": meta},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            out.update({base + "-P": fila["punto"], base + "-IC-LO": fila["ic_inf"],
                base + "-IC-HI": fila["ic_sup"], base + "-N": fila["n"],
                base + "-ESTADO": fila["estado"],
                base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return out
