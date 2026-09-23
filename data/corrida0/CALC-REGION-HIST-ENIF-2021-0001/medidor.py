"""Serie regional de tres conductas comparables; cada ola corre en un CALC.

El primer resultado que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import json

import pandas as pd

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, _codigos, ENTIDADES, REGIONES_ENIF_2024, INUTIL


def carga_envipe(ruta, ola):
    tmod = _csv_zip(ruta, f"conjunto_de_datos_tmod_vic_envipe{ola}.csv",
                    ["ID_PER", "BP1_20", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS"])
    tsdem = _csv_zip(ruta, f"conjunto_de_datos_tsdem_envipe{ola}.csv",
                     ["ID_PER", "CVE_ENT"])
    if tsdem["ID_PER"].duplicated().any():
        raise RuntimeError(f"ENVIPE {ola}: ID_PER no única")
    geo = tmod["ID_PER"].map(tsdem.set_index("ID_PER")["CVE_ENT"])
    if geo.isna().any():
        raise RuntimeError(f"ENVIPE {ola}: delito sin persona")
    bp = _codigos(tmod["BP1_20"])
    den = bp.isin(["1", "2"])
    y = bp.eq("2") & _codigos(tmod["BP1_23"]).str.zfill(2).isin(INUTIL)
    return tmod, geo.str.zfill(2), den, y, "FAC_DEL", ENTIDADES


def carga_encig(ruta, ola):
    clave = "CVE_ENT" if ola == 2023 else "ENT"
    miembro = (f"/conjunto_de_datos/encig{ola}_04_sec_7.csv" if ola == 2017
               else f"/conjunto_de_datos/conjunto_de_datos_encig{ola}_04_sec_7.csv")
    d = _csv_zip(ruta, miembro,
                 [clave, "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"])
    canal = _codigos(d["P7_3"])
    den = _codigos(d["N_TRA"]).str.zfill(2).eq("01") & canal.isin(["1", "2", "4", "5", "6"])
    y = den & canal.isin(["4", "5"])
    return d, _codigos(d[clave]).str.zfill(2), den, y, "FAC_TRA", ENTIDADES


def carga_enif(ruta, ola):
    miembro = {2018: "conjunto_de_datos/tmodulo.csv",
               2021: "conjunto_de_datos_tmodulo_enif_2021.csv",
               2024: "TMODULO.csv"}[ola]
    fac = "FAC_ELE" if ola == 2021 else "FAC_PER"
    edad_col = "EDAD_V" if ola == 2024 else "EDAD"
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    d = _csv_zip(ruta, miembro, ["REGION", edad_col, fac, "EST_DIS", "UPM_DIS"] + inf)
    respuestas = d[inf]
    edad = pd.to_numeric(d[edad_col], errors="coerce")
    den = respuestas.isin(["1", "2"]).any(axis=1) & edad.between(18, 70)
    y = respuestas.eq("1").any(axis=1) & den
    return d, _codigos(d["REGION"]), den, y, fac, REGIONES_ENIF_2024


CARGADORES = {"ENVIPE": carga_envipe, "ENCIG": carga_encig, "ENIF": carga_enif}


def medir(inputs, contrato):
    par = contrato["parametros"]
    inst, ola = par["instrumento"], int(par["ola"])
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    d, geo, den, y, fac, geografias = CARGADORES[inst](ruta, ola)
    filas, meta = estima_dominios(
        d, geo, den, y, factor=fac, estrato="EST_DIS", upm="UPM_DIS",
        dominios=geografias, representativos=set(geografias),
        semilla=int(contrato["seed"]["valor"]),
        replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]),
    )
    pref = f"RESULT-REGION-HIST-{inst}-{ola}"
    out = {pref + "-JSON": json.dumps({"filas": filas, "diseno": meta},
                                       ensure_ascii=False, sort_keys=True,
                                       separators=(",", ":"))}
    for f in filas:
        base = pref + "-" + f["geografia"]
        out[base + "-P"] = f["punto"]
        out[base + "-IC-LO"] = f["ic_inf"]
        out[base + "-IC-HI"] = f["ic_sup"]
        out[base + "-N"] = f["n"]
        out[base + "-ESTADO"] = f["estado"]
        out[base + "-N-EFECTIVO-KISH"] = f["n_efectivo_kish"]
    return out
