from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Piso t-1 (ENIF 2021) del eje `formalidad` para tres desenlaces. Los dos
desenlaces de ahorro y el estimador bootstrap se IMPORTAN del medidor
sellado de CALC-PISOS-ENIF2021-EJES-0003 (input `MEDIDOR-EJES-0003`,
bytes verificados por sha256); la rejilla se LEE del yaml del árbitro
(input `ARBITRO-OLA5-YAML`). Spec: PISOS-ENIF2021-formalidad-spec-v1_0.md.
"""
import types
from pathlib import Path
import pandas as pd
import yaml

PREFIJO = "PISOS-ENIF2021-FORMALIDAD"
CON = "con seguridad social"
SIN = "sin seguridad social"
REGLAS = {  # desenlace -> (id de regla del árbitro, nombre del bloque `desenlaces`, o None)
    "D9": ("dinero.ahorro.via_informal_ejes_enif2024", "ahorra_solo_informal"),
    "INFORMAL-CUALQUIERA": ("dinero.ahorro.via_informal_ejes_enif2024", "informal_cualquiera"),
    "HORIZONTE-CORTO": ("dinero.ahorro.horizonte_corto_ejes_enif2024", None),
}


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_0003(inputs):
    src = _bytes(inputs["MEDIDOR-EJES-0003"])
    mod = types.ModuleType("medidor_ejes_0003")
    exec(compile(src, "medidor_ejes_0003", "exec"), mod.__dict__)
    return mod


def _rejilla(inputs):
    """Categorías del eje `formalidad` por desenlace, leídas del árbitro.
    Falla si alguna entrada no trae exactamente dos celdas."""
    d = yaml.safe_load(_bytes(inputs["ARBITRO-OLA5-YAML"]).decode("utf-8"))
    reglas = {r["id"]: r for r in d["reglas_propuestas"]}
    out = {}
    for des, (rid, bloque) in REGLAS.items():
        r = reglas[rid]
        ejes = r["ejes"] if bloque is None else next(
            v["ejes"] for v in r["desenlaces"].values() if v.get("nombre") == bloque)
        eje = next(e for e in ejes if e["eje"] == "formalidad")
        cats = [c["celda"] for c in eje["celdas"]]
        if sorted(cats) != sorted([SIN, CON]):
            raise RuntimeError(f"rejilla del árbitro inesperada para {des}: {cats}")
        out[des] = cats
    return out


def medir(inputs, contrato):
    m = _modulo_0003(inputs)
    rejilla = _rejilla(inputs)
    z = inputs["enif2021_csv"]["ruta_absoluta"]
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    accounts = [f"P5_4_{i}" for i in range(1, 10)]
    savings = [f"P5_7_{i}" for i in range(1, 10)]
    cols = inf + accounts + savings + ["P3_5", "P3_6", "P3_7", "P3_10", "P4_10",
                                       "FAC_ELE", "EST_DIS", "UPM_DIS"]
    d = m._csv(z, "conjunto_de_datos_tmodulo_enif_2021.csv", cols)
    d["_w"] = pd.to_numeric(d["FAC_ELE"], errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip(); d["_upm"] = d["UPM_DIS"].str.strip()

    # Eje: mapa congelado (spec §1).
    p310 = m._code(d["P3_10"])
    formalidad = pd.Series(pd.NA, index=d.index, dtype="object")
    formalidad.loc[p310.isin(list("12345"))] = CON
    formalidad.loc[p310.eq("6")] = SIN
    en_universo = formalidad.notna()

    # Desenlaces: los dos de ahorro importados; horizonte_corto por spec §4.
    informal = m._known_any(d, inf); formal = m._formal(d, accounts, savings)
    any_inf = informal.astype("Float64")
    only = pd.Series(pd.NA, index=d.index, dtype="Float64")
    only.loc[informal.eq(False) | formal.eq(True)] = 0.0
    only.loc[informal.eq(True) & formal.eq(False)] = 1.0
    p410 = m._code(d["P4_10"])
    horiz = pd.Series(pd.NA, index=d.index, dtype="Float64")
    horiz.loc[p410.isin(list("2345"))] = 0.0
    horiz.loc[p410.eq("1")] = 1.0
    desenlaces = {"D9": only, "INFORMAL-CUALQUIERA": any_inf, "HORIZONTE-CORTO": horiz}

    # Celdas: por desenlace, las dos del árbitro + el total del universo.
    todo = pd.Series("universo trabaja", index=d.index, dtype="object").where(en_universo, pd.NA)
    cells = []
    for des, y in desenlaces.items():
        cells += m._cells(f"{PREFIJO}-{des}", y,
                          {"formalidad": (formalidad, tuple(rejilla[des])),
                           "universo": (todo, ("universo trabaja",))})
    out = m._estimate(d, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]))

    # Control de coherencia (A-bis 4): numeradores ponderados suman.
    for des in desenlaces:
        b = f"RESULT-{PREFIJO}-{des}"
        num = lambda s: out[f"{b}-{s}-P"] * out[f"{b}-{s}-DEN-W"]
        out[f"{b}-COHERENCIA-DELTA-NUM-W"] = abs(
            num("UNIVERSO-UNIVERSO-TRABAJA") - num("FORMALIDAD-SIN-SEGURIDAD-SOCIAL")
            - num("FORMALIDAD-CON-SEGURIDAD-SOCIAL"))
        out[f"{b}-DESENLACE-INDEFINIDO-EN-UNIVERSO"] = int(
            (en_universo & desenlaces[des].isna()).sum())

    # Excluidos del eje y diagnóstico de flujo (spec §1, §4).
    p35 = m._code(d["P3_5"]); p36 = m._code(d["P3_6"]); p37 = m._code(d["P3_7"])
    flujo = (p35.isin(["1", "2"]) | p36.isin(list("12345"))) & p37.isin(list("2345"))
    out.update({
        f"RESULT-{PREFIJO}-FILAS-PERSONAS": int(len(d)),
        f"RESULT-{PREFIJO}-N-UNIVERSO": int(en_universo.sum()),
        f"RESULT-{PREFIJO}-EXCLUIDOS-P3-10-NO-SABE": int(p310.eq("9").sum()),
        f"RESULT-{PREFIJO}-EXCLUIDOS-P3-10-BLANCO": int(p310.eq("").sum()),
        f"RESULT-{PREFIJO}-EXCLUIDOS-P3-10-FUERA-DE-CATALOGO": int(
            (~p310.isin(list("1234569") + [""])).sum()),
        f"RESULT-{PREFIJO}-FLUJO-TRABAJA-N": int(flujo.sum()),
        f"RESULT-{PREFIJO}-FLUJO-DISCORDANCIA-N": int((flujo != p310.ne("")).sum()),
    })
    return out
