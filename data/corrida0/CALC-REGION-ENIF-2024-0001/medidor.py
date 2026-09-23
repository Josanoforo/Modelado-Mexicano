"""Medidor regional inicial. El primer resultado que produzca este procedimiento es el que se reporta.

Cada entrada mide la conducta definida en su spec, sin abrir otras olas.
El catálogo completo se cierra mediante piezas adicionales del mismo acto.
"""
from __future__ import annotations

import io
import json
import zipfile

import pandas as pd

from tools.astra.region.estadistica import estima_dominios

ENTIDADES = [f"{i:02d}" for i in range(1, 33)]
REGIONES_ENIF_2024 = [str(i) for i in range(1, 7)]
INUTIL = {"04", "05", "06", "08"}


def _csv_zip(ruta, sufijo, columnas):
    with zipfile.ZipFile(ruta) as z:
        nombres = [n for n in z.namelist() if n.lower().endswith(sufijo.lower())]
        if len(nombres) != 1:
            raise RuntimeError(f"{sufijo}: {len(nombres)} miembros")
        payload = z.read(nombres[0])
    ultimo = None
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            texto = payload.decode(encoding)
            break
        except UnicodeDecodeError as exc:
            ultimo = exc
    else:
        raise RuntimeError("codificación del CSV") from ultimo
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False,
                     na_filter=False, low_memory=False)
    df.columns = [c.strip().strip('"').lstrip("\ufeff") for c in df.columns]
    faltan = set(columnas) - set(df.columns)
    if faltan:
        raise RuntimeError(f"{nombres[0]}: faltan {sorted(faltan)}")
    return df[list(columnas)].apply(lambda s: s.astype(str).str.strip().str.strip('"'))


def _codigos(s):
    return s.astype(str).str.strip().str.strip('"')


def _comun(df, geo, den, y, *, factor, dominios, semilla, replicas, n_min):
    filas, meta = estima_dominios(
        df, geo, den, y, factor=factor, estrato="EST_DIS", upm="UPM_DIS",
        dominios=dominios, representativos=set(dominios), semilla=semilla,
        replicas=replicas, n_min=n_min,
    )
    return {"filas": filas, "diseno": meta}


def _envipe(ruta, semilla, replicas, n_min):
    tmod = _csv_zip(ruta, "conjunto_de_datos_tmod_vic_envipe2024.csv",
                    ["ID_PER", "BP1_20", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS"])
    tsdem = _csv_zip(ruta, "conjunto_de_datos_tsdem_envipe2024.csv",
                     ["ID_PER", "CVE_ENT"])
    if tsdem["ID_PER"].duplicated().any():
        raise RuntimeError("ID_PER no es única en TSDEM")
    geo = tmod["ID_PER"].map(tsdem.set_index("ID_PER")["CVE_ENT"])
    if geo.isna().any():
        raise RuntimeError("delitos sin persona enlazada a TSDEM")
    geo = geo.str.zfill(2)
    bp = _codigos(tmod["BP1_20"])
    motivo = _codigos(tmod["BP1_23"]).str.zfill(2)
    den = bp.isin(["1", "2"])
    y = bp.eq("2") & motivo.isin(INUTIL)
    out = _comun(tmod, geo, den, y, factor="FAC_DEL", dominios=ENTIDADES,
                 semilla=semilla, replicas=replicas, n_min=n_min)
    out["unidad"] = "delito"
    out["ambito_geografico"] = "entidad de residencia de la víctima; no entidad de ocurrencia"
    return out


def _encig(ruta, semilla, replicas, n_min):
    d = _csv_zip(ruta, "encig2023_04_sec_7.csv",
                 ["CVE_ENT", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"])
    canal = _codigos(d["P7_3"])
    den = _codigos(d["N_TRA"]).str.zfill(2).eq("01") & canal.isin(["1", "2", "4", "5", "6"])
    y = den & canal.isin(["4", "5"])
    out = _comun(d, d["CVE_ENT"].str.zfill(2), den, y, factor="FAC_TRA",
                 dominios=ENTIDADES, semilla=semilla, replicas=replicas, n_min=n_min)
    out["unidad"] = "trámite"
    out["ambito_geografico"] = "entidad de residencia de la persona informante; no ubicación del trámite"
    return out


def _enif(ruta, semilla, replicas, n_min):
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    form = [f"P5_6_{i}" for i in range(1, 10)]
    d = _csv_zip(ruta, "TMODULO.csv",
                 ["REGION", "EDAD_V", "FAC_PER", "EST_DIS", "UPM_DIS"] + inf + form)
    edad = pd.to_numeric(d["EDAD_V"], errors="coerce")
    if edad.isna().any() or (edad < 18).any():
        raise RuntimeError("edad fuera del marco ENIF 2024")
    vals = d[inf + form]
    den = vals.isin(["1", "2"]).any(axis=1)
    y = vals.eq("1").any(axis=1) & den
    out = _comun(d, d["REGION"], den, y, factor="FAC_PER",
                 dominios=REGIONES_ENIF_2024, semilla=semilla,
                 replicas=replicas, n_min=n_min)
    out["unidad"] = "persona elegida de 18 años o más"
    out["ambito_geografico"] = "región oficial de diseño ENIF 2024; no entidad"
    return out


MEDIDORES = {"ENVIPE": _envipe, "ENCIG": _encig, "ENIF": _enif}


def medir(inputs, contrato):
    par = contrato["parametros"]
    instrumento = par["instrumento"]
    entrada = inputs[par["input_id"]]["ruta_absoluta"]
    resultado = MEDIDORES[instrumento](entrada, int(contrato["seed"]["valor"]),
                                      int(par["bootstrap_replicas"]), int(par["n_min"]))
    ola = "2023" if instrumento == "ENCIG" else "2024"
    prefijo = f"RESULT-REGION-{instrumento}-{ola}"
    out = {prefijo + "-JSON": json.dumps(resultado, ensure_ascii=False,
                                          sort_keys=True, separators=(",", ":"))}
    for fila in resultado["filas"]:
        base = prefijo + "-" + fila["geografia"]
        out[base + "-P"] = fila["punto"]
        out[base + "-IC-LO"] = fila["ic_inf"]
        out[base + "-IC-HI"] = fila["ic_sup"]
        out[base + "-N"] = fila["n"]
        out[base + "-ESTADO"] = fila["estado"]
        out[base + "-N-EFECTIVO-KISH"] = fila["n_efectivo_kish"]
    return out
