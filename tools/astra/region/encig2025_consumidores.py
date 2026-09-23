"""Consumidores ENCIG 2025 por entidad de residencia, con diseño completo."""
from __future__ import annotations

import json

import pandas as pd

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, ENTIDADES

CONDUCTAS = (
    "paga_mordida_encig2025",
    "adopta_encig2025_luz",
    "paga_mordida_encig2025_presencial_r2",
    "paga_mordida_encig2025_digital_r2",
)
M_PER = "encig2025_01_sec1_A_3_4_5_8_9_10.csv"
M_S7 = "encig2025_04_sec_7.csv"
M_S8 = "encig2025_05_sec_8.csv"


def codigos(s):
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype(str)


def prepara(d, factor):
    peso = pd.to_numeric(d[factor], errors="coerce")
    valid = peso.notna() & (peso > 0) & d["EST_DIS"].ne("") & d["UPM_DIS"].ne("")
    return d.loc[valid].reset_index(drop=True), int((~valid).sum())


def fuentes(ruta):
    per = _csv_zip(ruta, M_PER,
                   ["CVE_ENT", "P8_3_1", "FAC_P18", "EST_DIS", "UPM_DIS"])
    s7 = _csv_zip(ruta, M_S7,
                  ["ID_TRA", "CVE_ENT", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"])
    s8 = _csv_zip(ruta, M_S8, ["ID_TRA", "P8_4"])
    if s8["ID_TRA"].duplicated().any() or s8["ID_TRA"].eq("").any():
        raise RuntimeError("SEC8: ID_TRA no única o vacía")
    per, excl_per = prepara(per, "FAC_P18")
    s7, excl_s7 = prepara(s7, "FAC_TRA")
    s7["_P8_4"] = s7["ID_TRA"].map(s8.set_index("ID_TRA")["P8_4"])
    return per, s7, {"excluidos_sin_factor_diseno_persona": excl_per,
                     "excluidos_sin_factor_diseno_sec7": excl_s7,
                     "sec7_sin_pareja_sec8": int(s7["_P8_4"].isna().sum())}


def desenlaces(per, s7):
    a = codigos(per["P8_3_1"])
    canal = codigos(s7["P7_3"])
    ntra = codigos(s7["N_TRA"])
    p84 = codigos(s7["_P8_4"])
    return {
        "paga_mordida_encig2025":
            (per, per["CVE_ENT"].str.zfill(2), a.isin(["1", "2"]), a.eq("1"), "FAC_P18", "persona 18+"),
        "adopta_encig2025_luz":
            (s7, s7["CVE_ENT"].str.zfill(2), ntra.eq("1") & canal.isin(["1", "2", "4", "5", "6"]),
             ntra.eq("1") & canal.isin(["4", "5"]), "FAC_TRA", "trámite de luz"),
        "paga_mordida_encig2025_presencial_r2":
            (s7, s7["CVE_ENT"].str.zfill(2), canal.eq("1") & p84.isin(["0", "1"]),
             canal.eq("1") & p84.eq("1"), "FAC_TRA", "registro de trámite sin deduplicar"),
        "paga_mordida_encig2025_digital_r2":
            (s7, s7["CVE_ENT"].str.zfill(2), canal.isin(["3", "4", "5"]) & p84.isin(["0", "1"]),
             canal.isin(["3", "4", "5"]) & p84.eq("1"), "FAC_TRA", "registro de trámite sin deduplicar"),
    }


def medir(inputs, contrato):
    par = contrato["parametros"]
    if tuple(par["conductas"]) != CONDUCTAS:
        raise RuntimeError("conductas distintas de la spec")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    per, s7, guardias = fuentes(ruta)
    d = desenlaces(per, s7)
    resultados = {}
    for conducta in CONDUCTAS:
        df, geo, den, y, factor, unidad = d[conducta]
        filas, meta = estima_dominios(
            df, geo, den, y, factor=factor, estrato="EST_DIS", upm="UPM_DIS",
            dominios=ENTIDADES, representativos=set(ENTIDADES),
            semilla=int(contrato["seed"]["valor"]), replicas=int(par["bootstrap_replicas"]),
            n_min=int(par["n_min"]),
        )
        pref = f"RESULT-REGION-ENCIG-2025-{conducta}"
        resultados[pref + "-JSON"] = json.dumps(
            {"filas": filas, "diseno": meta, "guardias": guardias, "unidad": unidad,
             "ambito_geografico": "entidad de residencia del informante; marco urbano 100 mil+"},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            resultados.update({base + "-P": fila["punto"],
                               base + "-IC-LO": fila["ic_inf"],
                               base + "-IC-HI": fila["ic_sup"],
                               base + "-N": fila["n"],
                               base + "-ESTADO": fila["estado"],
                               base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return resultados
