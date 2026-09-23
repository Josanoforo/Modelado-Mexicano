"""Motivo principal de no denuncia, unidad persona U4, ENVIPE 2025."""
from __future__ import annotations

import json

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.medidor import _csv_zip, ENTIDADES

CONDUCTAS = ("denuncia_con_miedo_o_desconfianza", "denuncia_por_otra_razon")
PERSONALES = {f"{i:02}" for i in range(5, 16)}
U1 = {f"{i:02}" for i in range(1, 9)}
C2 = {"01", "02", "06", "08"}


def universo(mod, per):
    if per["ID_PER"].duplicated().any():
        raise RuntimeError("ID_PER duplicada en TPER_VIC2")
    cod = mod["BP1_23"].str.strip().str.zfill(2)
    bpc = mod["BPCOD"].str.strip().str.zfill(2)
    usa = bpc.isin(PERSONALES) & mod["BP1_20"].str.strip().eq("2") & cod.isin(U1)
    sub = mod.loc[usa, ["ID_PER"]].copy()
    sub["y"] = cod[usa].isin(C2).to_numpy()
    if sub.empty:
        raise RuntimeError("U4 vacío")
    por_persona = sub.groupby("ID_PER", sort=False)["y"].max()
    if not por_persona.index.isin(per["ID_PER"]).all():
        raise RuntimeError("ID_PER de delitos sin TPER_VIC2")
    den = per["ID_PER"].isin(por_persona.index)
    y = per["ID_PER"].map(por_persona).eq(True) & den
    return den, y


def medir(inputs, contrato):
    par = contrato["parametros"]
    if tuple(par["conductas"]) != CONDUCTAS:
        raise RuntimeError("conductas distintas de la spec")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    mod = _csv_zip(ruta, "conjunto_de_datos_tmod_vic_envipe2025.csv",
                   ["ID_PER", "BPCOD", "BP1_20", "BP1_23"])
    per = _csv_zip(ruta, "conjunto_de_datos_tper_vic2_envipe2025.csv",
                   ["ID_PER", "CVE_ENT", "FAC_ELE", "EST_DIS", "UPM_DIS"])
    den, y = universo(mod, per)
    out = {}
    for conducta in CONDUCTAS:
        outcome = y if conducta == CONDUCTAS[0] else den & ~y
        filas, meta = estima_dominios(per, per["CVE_ENT"].str.zfill(2), den, outcome,
            factor="FAC_ELE", estrato="EST_DIS", upm="UPM_DIS", dominios=ENTIDADES,
            representativos=set(ENTIDADES), semilla=int(contrato["seed"]["valor"]),
            replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]))
        pref = f"RESULT-REGION-ENVIPE-2025-{conducta}"
        out[pref + "-JSON"] = json.dumps({"filas": filas, "diseno": meta,
            "unidad": "persona", "denominador": "U4: persona con al menos un delito U1"},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            out.update({base + "-P": fila["punto"], base + "-IC-LO": fila["ic_inf"],
                base + "-IC-HI": fila["ic_sup"], base + "-N": fila["n"],
                base + "-ESTADO": fila["estado"],
                base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return out
