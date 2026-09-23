"""Denuncia condicionada a seguro ENVIPE 2025, unidad delito BPCOD=01."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, ENTIDADES

CONDUCTAS = (
    "denuncia_con_seguro", "no_denuncia_con_seguro",
    "denuncia_sin_seguro", "no_denuncia_sin_seguro",
)


def dominios(mod):
    robo = mod["BPCOD"].str.strip().str.zfill(2).eq("01")
    cobertura = mod["BP2_1"].str.strip()
    denuncia = mod["BP1_20"].str.strip()
    base = robo & denuncia.isin(["1", "2"])
    con = base & cobertura.eq("1")
    sin = base & cobertura.eq("2")
    return {
        "denuncia_con_seguro": (con, con & denuncia.eq("1")),
        "no_denuncia_con_seguro": (con, con & denuncia.eq("2")),
        "denuncia_sin_seguro": (sin, sin & denuncia.eq("1")),
        "no_denuncia_sin_seguro": (sin, sin & denuncia.eq("2")),
    }


def medir(inputs, contrato):
    par = contrato["parametros"]
    if tuple(par["conductas"]) != CONDUCTAS:
        raise RuntimeError("conductas distintas de la spec")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    mod = _csv_zip(ruta, "conjunto_de_datos_tmod_vic_envipe2025.csv",
        ["ID_PER", "BPCOD", "BP2_1", "BP1_20", "FAC_DEL", "EST_DIS", "UPM_DIS"])
    dem = _csv_zip(ruta, "conjunto_de_datos_tsdem_envipe2025.csv",
        ["ID_PER", "CVE_ENT"])
    if dem["ID_PER"].duplicated().any():
        raise RuntimeError("ID_PER duplicada en TSDEM")
    geo = mod["ID_PER"].map(dem.set_index("ID_PER")["CVE_ENT"])
    if geo.isna().any():
        raise RuntimeError("delito sin residencia de víctima")
    out = {}
    for conducta, (den, y) in dominios(mod).items():
        filas, meta = estima_dominios(mod, geo.str.zfill(2), den, y,
            factor="FAC_DEL", estrato="EST_DIS", upm="UPM_DIS", dominios=ENTIDADES,
            representativos=set(ENTIDADES), semilla=int(contrato["seed"]["valor"]),
            replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]))
        pref = f"RESULT-REGION-ENVIPE-SEG-2025-{conducta}"
        out[pref + "-JSON"] = json.dumps({"filas": filas, "diseno": meta,
            "unidad": "delito", "ambito_geografico": "entidad de residencia"},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            out.update({base + "-P": fila["punto"], base + "-IC-LO": fila["ic_inf"],
                base + "-IC-HI": fila["ic_sup"], base + "-N": fila["n"],
                base + "-ESTADO": fila["estado"],
                base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return out
