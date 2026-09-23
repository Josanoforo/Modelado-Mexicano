"""ENIF 2012–2021: motivos declarados entre personas sin producto formal.

El primer resultado que produzca este procedimiento es el que se reporta.
Las lecturas DBF/CSV, cortes y bootstrap se importan por bytes de medidores
sellados; esta pieza fija universo, pases, partición y diagnósticos nuevos.
"""
from __future__ import annotations

import types
from pathlib import Path
import numpy as np
import pandas as pd

HIST = "data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2018-0001/medidor.py"
EJES = "data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py"
MAPA = "forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-mapa-v1_1.tsv"

CFG = {
 "2012": {"CUENTA": ("P5_3", "P5_4", 9, None, None),
          "CREDITO": ("P6_4", "P6_5", 8, None, None)},
 "2015": {"CUENTA": ("P5_4", "P5_6", 9, "P5_5", "P5_8"),
          "CREDITO": ("P6_4", "P6_6", 8, "P6_5", "P6_7")},
 "2018": {"CUENTA": ("P5_4", "P5_7", 9, "P5_6", "P5_8"),
          "CREDITO": ("P6_3", "P6_6", 8, "P6_5", "P6_7")},
 "2021": {"CUENTA": ("P5_4_1", "P5_21", 10, "P5_20", "P5_22"),
          "CREDITO": ("P6_2_1", "P6_15", 9, "P6_14", "P6_16")},
}
# Pregunta principal de no tenencia, pregunta de ex usuario. Ambigüedad
# desconfianza/mal servicio -> OTRO por imposibilidad de separar ambos textos.
CLASES = {
 "2012": {"CUENTA": ({3,4,6,8},{2,7},{1:"INGRESO-INSUFICIENTE",5:"DESCONFIANZA-O-SERVICIO",9:"OTRA"}),
          "CREDITO": ({2,4,6,7},{1,5},{3:"DESCONFIANZA-O-SERVICIO",8:"OTRA"})},
 "2015": {"CUENTA": ({3,4,8},{1,5,6},{2:"INGRESO-INSUFICIENTE",7:"DESCONFIANZA-O-SERVICIO",9:"OTRA"}),
          "CREDITO": ({1,2,4,5},{6,7},{3:"DESCONFIANZA-O-SERVICIO",8:"OTRA"})},
 "2018": {"CUENTA": ({1,2,4},{5,6},{3:"DESCONFIANZA-O-SERVICIO",7:"INGRESO-INSUFICIENTE",8:"DESCONOCIMIENTO",9:"OTRA"}),
          "CREDITO": ({1,2,3,5},{6,7},{4:"DESCONFIANZA-O-SERVICIO",8:"OTRA"})},
 "2021": {"CUENTA": ({1,2,4},{5,6},{3:"DESCONFIANZA-O-SERVICIO",7:"INGRESO-INSUFICIENTE",8:"DESCONOCIMIENTO",9:"IMPUESTOS",10:"OTRA"}),
          "CREDITO": ({1,2,3,5},{6,7},{4:"DESCONFIANZA-O-SERVICIO",8:"IMPUESTOS",9:"OTRA"})},
}
EX = {
 "2015": {"CUENTA": ({3,5,6},{2,4},{1:"MALA-EXPERIENCIA",7:"OTRA"}),
          "CREDITO": ({2,4},{3,5,6},{1:"MALA-EXPERIENCIA",7:"OTRA"})},
 "2018": {"CUENTA": ({5,6,7},{1,2,3},{4:"MALA-EXPERIENCIA",8:"FRAUDE",9:"OTRA"}),
          "CREDITO": ({1,5},{2,3,6},{4:"MALA-EXPERIENCIA",7:"OTRA"})},
 "2021": {"CUENTA": ({5,6,7},{1,2,3},{4:"MALA-EXPERIENCIA",8:"FRAUDE",9:"IMPUESTOS",10:"OTRA"}),
          "CREDITO": ({1,5},{2,3,6},{4:"MALA-EXPERIENCIA",7:"IMPUESTOS",8:"OTRA"})},
}
METRICAS = ("OFERTA", "PREFERENCIA", "OTRO-NS", "CUALQUIER-OFERTA",
            "CUALQUIER-PREFERENCIA", "INTERSECCION", "COBERTURA",
            "PASE-ESTRUCTURAL", "NO-RESPUESTA", "MIXTA")

def _module(path):
    m = types.ModuleType(Path(path).stem)
    exec(compile(Path(path).read_bytes(), path, "exec"), m.__dict__)
    return m

def _reason(d, cols, yes, no, other, multi, code):
    """Vector de indicadores, conservando ausencia total de motivo."""
    n = len(d)
    o = np.zeros(n, bool); p = np.zeros(n, bool); x = np.zeros(n, bool)
    sub = {v: np.zeros(n, bool) for v in set(other.values())}
    if multi:
        for k, col in enumerate(cols, 1):
            hit = code(d[col]).eq("1").to_numpy()
            if k in yes: o |= hit
            elif k in no: p |= hit
            else:
                x |= hit
                sub[other[k]] |= hit
        observed = o | p | x
    else:
        c = code(d[cols[0]])
        observed = c.isin([str(i) for i in yes | no | set(other)]).to_numpy()
        o = c.isin([str(i) for i in yes]).to_numpy()
        p = c.isin([str(i) for i in no]).to_numpy()
        x = c.isin([str(i) for i in other]).to_numpy()
        for k, name in other.items(): sub[name] |= c.eq(str(k)).to_numpy()
    return o, p, x, observed, sub

def medir(inputs, contrato):
    ola = str(contrato["parametros"]["ola"])
    hist = _module(HIST); eje = _module(EJES)
    mapa = hist._mapa({"MAPA": inputs["MAPA"]}, ola)
    # El mapa histórico tiene las columnas y uniones de los pisos sellados.
    for conducta, (estado, razon, k, pasado, exrazon) in CFG[ola].items():
        cols = [razon] if ola not in ("2012", "2015") or (ola == "2015" and conducta == "CUENTA") else [f"{razon}_{i}" for i in range(1, k+1)]
        plus = [estado] + cols + ([pasado] if pasado else [])
        plus += ([exrazon] if exrazon and ola != "2015" else [f"{exrazon}_{i}" for i in range(1, 8)] if exrazon else [])
        if ola == "2021" and conducta == "CUENTA": plus += [f"P5_4_{i}" for i in range(2, 10)]
        if ola == "2021" and conducta == "CREDITO": plus += [f"P6_2_{i}" for i in range(2, 10)]
        if ola == "2018" and conducta == "CUENTA": plus += ["P5_5"]
        if ola == "2018" and conducta == "CREDITO": plus += ["P6_4"]
        member = {"2012":"stmodulo1_e2.dbf", "2015":"tmodulo1.DBF", "2018":"conjunto_de_datos/tmodulo.csv", "2021":"conjunto_de_datos_tmodulo_enif_2021.csv"}[ola]
        for col in plus:
            if col in {v for row in mapa.values() for v in hist._lista(row["variables"])}: continue
            which = "tmodulo2.DBF" if ola == "2015" and conducta == "CREDITO" and col.startswith(("P6_6_", "P6_7_")) else member
            mapa[f"oferta_{conducta}_{col}"] = {"variables": col, "miembro": which}
    d, _, diag = hist._carga(inputs, ola, mapa)
    age = pd.to_numeric(d[mapa["edad"]["variables"]], errors="coerce")
    d = d.loc[age.between(18,70)].copy().reset_index(drop=True)
    d["_w"] = pd.to_numeric(d[mapa["ponderador"]["variables"]], errors="coerce")
    design = [v.strip() for v in mapa["diseno"]["variables"].split(",")]
    d["_est"] = d[design[0]].str.strip(); d["_upm"] = d[design[1]].str.strip()
    code = eje._code
    axes = {
      "SEXO": (code(d[mapa["sexo"]["variables"]]), ("1","2")),
      "EDAD": (eje._age(d[mapa["edad"]["variables"]]), eje.EDADES),
      "ESCOLARIDAD": (eje._school(d[mapa["escolaridad"]["variables"]]), eje.ESCOLARIDAD),
      "LOCALIDAD": (code(d[mapa["localidad"]["variables"]]).map({"1":"15 000 y mas","2":"15 000 y mas","3":"menor de 15 000","4":"menor de 15 000"}), ("15 000 y mas","menor de 15 000")),
    }
    if mapa["formalidad"]["variables"]:
        f = code(d[mapa["formalidad"]["variables"]])
        axes["FORMALIDAD"] = (f.map({"1":"con seguridad social","2":"con seguridad social","3":"con seguridad social","4":"con seguridad social","5":"con seguridad social","6":"sin seguridad social"}), ("con seguridad social","sin seguridad social"))
    valid = d["_w"].gt(0) & d["_est"].ne("") & d["_upm"].ne("")
    cells=[]; extra={}
    for conducta, (estado, razon, k, pasado, exrazon) in CFG[ola].items():
        if conducta == "CUENTA":
            if ola == "2021":
                a = d[[f"P5_4_{i}" for i in range(1,10)]].apply(code)
                no_user = a.eq("2").all(axis=1).to_numpy()
            elif ola == "2018": no_user = (code(d["P5_4"]).eq("2") & code(d["P5_5"]).eq("2")).to_numpy()
            else: no_user = code(d[estado]).eq("2").to_numpy()
        else:
            if ola == "2021": no_user = d[[f"P6_2_{i}" for i in range(1,10)]].apply(code).eq("2").all(axis=1).to_numpy()
            elif ola == "2018": no_user = (code(d["P6_3"]).eq("2") & code(d["P6_4"]).eq("2")).to_numpy()
            else: no_user = code(d[estado]).eq("2").to_numpy()
        never = no_user & (code(d[pasado]).eq("2").to_numpy() if pasado else True)
        former = no_user & code(d[pasado]).eq("1").to_numpy() if pasado else np.zeros(len(d), bool)
        main_multi = ola == "2012" or (ola == "2015" and conducta == "CREDITO")
        main_cols = [f"{razon}_{i}" for i in range(1,k+1)] if main_multi else [razon]
        yes,no,other = CLASES[ola][conducta]
        o,p,x,obs,sub = _reason(d, main_cols, yes,no,other,main_multi,code)
        o &= never; p &= never; x &= never; obs &= never
        for v in sub: sub[v] &= never
        if exrazon:
            ex_multi = ola == "2015"
            ex_cols = [f"{exrazon}_{i}" for i in range(1,8)] if ex_multi else [exrazon]
            ey,en,eo = EX[ola][conducta]
            a,b,c,s,ss = _reason(d, ex_cols, ey,en,eo,ex_multi,code)
            o |= a & former; p |= b & former; x |= c & former; obs |= s & former
            for v in ss: sub.setdefault(v,np.zeros(len(d),bool)); sub[v] |= ss[v] & former
        cohort = valid.to_numpy() & no_user
        # La partición cubre todo no usuario, incluidos pases sin motivo.
        clase_o = o & ~p & ~x & obs
        clase_p = p & ~o & ~x & obs
        clase_x = cohort & ~(clase_o | clase_p)
        mixed = o & p
        y = {"OFERTA":clase_o,"PREFERENCIA":clase_p,"OTRO-NS":clase_x,
             "CUALQUIER-OFERTA":o,"CUALQUIER-PREFERENCIA":p,
             "INTERSECCION":mixed,"COBERTURA":obs,
             "PASE-ESTRUCTURAL":cohort & ~(never | former),
             "NO-RESPUESTA":cohort & (never | former) & ~obs,
             "MIXTA":mixed}
        y.update({"SUB-"+v: a for v,a in sub.items()})
        extra[f"RESULT-DIN-OFERTA-EXCLUSION-ENIF{ola}-{conducta}-NO-USUARIOS-N"] = int(cohort.sum())
        extra[f"RESULT-DIN-OFERTA-EXCLUSION-ENIF{ola}-{conducta}-BATERIA-OBS-N"] = int((cohort & obs).sum())
        extra[f"RESULT-DIN-OFERTA-EXCLUSION-ENIF{ola}-{conducta}-ESTADO"] = "CONSTRUIBLE"
        for axis,(group,cats) in [("NACIONAL",(pd.Series("TODOS",index=d.index),("TODOS",)))] + list(axes.items()):
            for cat in cats:
                base_mask = pd.Series(cohort & group.eq(cat).fillna(False).to_numpy(), index=d.index)
                for met, arr in y.items():
                    base = f"RESULT-DIN-OFERTA-EXCLUSION-ENIF{ola}-{conducta}-{axis}-{eje._slug(cat)}-{met}"
                    cells.append({"base":base,"mask":base_mask,"y":pd.Series(arr.astype(float),index=d.index)})
    out = eje._estimate(d,cells,int(contrato["parametros"]["bootstrap_replicas"]),int(contrato["seed"]["valor"]))
    out.update(extra)
    out[f"RESULT-DIN-OFERTA-EXCLUSION-ENIF{ola}-DIAGNOSTICO-DBF"] = str(diag)
    return out
