from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001 · ACTO GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1.
Spec humana: forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md.

Un intervalo de persistencia por celda para las 32 celdas marginales de ENIF
que el árbitro evaluó (`ARBITRO-MARGINALES-metadatos-v1_0.tsv`, instrumento
ENIF), que suma al error muestral del piso 2021 la variación empírica del
cambio trienal entre olas, y su cobertura de R 2024 — rotulada
RETROSPECTIVA-MECÁNICA (R 2024 ya vista; una sola regla, sin variantes).

  · Piso (centro y error muestral): los sellados de
    `CALC-PISOS-ENIF2021-EJES-0003` y `-FORMALIDAD-0001` (se CITAN).
  · R 2024: el sellado de `CALC-ARBITRO-MARGINALES-ENIF2024-0001` (se CITA;
    ENIF 2024 no se abre).
  · Cambio entre olas: ENIF 2018 y ENIF 2021 armonizadas (persona elegida
    18-70, mismo constructo en las dos olas), medidas aquí con el estimador
    sellado de -0003 IMPORTADO por bytes (input `MEDIDOR-EJES-0003`); los
    lectores de CSV en minúsculas y de DBF se importan del medidor sellado
    del carril histórico de crédito (input `MEDIDOR-CREDITO-HISTORIA`).
    ENIF 2015 se mide sólo donde el texto es comparable y sólo DESCRIBE
    (no entra al intervalo): firma pendiente de mesa, spec §3.

Regla congelada (spec §4), por celda c del grupo g = (desenlace, eje):
    Δ_c   = logit h2021(c) − logit h2018(c)
    τ²_g  = media de Δ_c² sobre las celdas de g con Δ definido (sin centrar,
            sin restar ruido: la persistencia predice Δ = 0)
    ee_m  = (logit IC-HI − logit IC-LO) / (2·1.959964) del piso sellado
    IC    = expit( logit p2021 ± 1.959964·√(ee_m² + τ²_g) )
    DENTRO si IC-INF ≤ R2024 ≤ IC-SUP.
Cobertura con IC binomial de Wilson por celda (n = celdas calibrables) y por
conglomerado (n efectivo = número de grupos desenlace × eje con celdas).
"""
import math
import types
from pathlib import Path

import numpy as np
import pandas as pd

Z95 = 1.959964
PREF = "RESULT-ENIFPIC"
ROTULO = "RETROSPECTIVA-MECÁNICA"
TIPO_INCERTIDUMBRE = "muestral + cambio-entre-olas"
TOL_ORO = 1e-10
CONTROL_MUESTRAL_N_DENTRO = 6        # FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02: 6/32
UMBRAL_X = 0.80                      # spec §6 (propuesta de FP, fijada antes del dato)
UMBRAL_PISO = 0.50                   # spec §6: por debajo, la persistencia trienal no es piso
POSITIVOS = ("MISMO-INSTRUMENTO", "CAMBIO-MENOR")
N_CELDAS_ENIF = 32

DES_DE_OUTCOME = {"ahorra_solo_informal": "D9", "informal_cualquiera": "INFORMAL-CUALQUIERA"}
OBJ_DES = {"D9": ("D-INF", "D-FOR"), "INFORMAL-CUALQUIERA": ("D-INF",)}
OBJ_EJE = {"sexo": "E-SEX", "edad": "E-EDA", "escolaridad": "E-ESC",
           "localidad": "E-LOC", "formalidad": "E-FOR", "cuenta": "E-CTA"}
# spec §2: veredictos de `data/ahorro-comparabilidad-texto-v1_0.tsv` sobre los
# que se congeló la regla. Si la tabla dice otra cosa, el medidor PARA.
VEREDICTOS_CONGELADOS = {
    ("D-INF", "2015"): "CAMBIO-MENOR", ("D-INF", "2018"): "MISMO-INSTRUMENTO",
    ("D-FOR", "2015"): "CAMBIO-DE-INSTRUMENTO", ("D-FOR", "2018"): "CAMBIO-MENOR",
    ("E-SEX", "2015"): "MISMO-INSTRUMENTO", ("E-SEX", "2018"): "MISMO-INSTRUMENTO",
    ("E-EDA", "2015"): "CAMBIO-MENOR", ("E-EDA", "2018"): "CAMBIO-MENOR",
    ("E-ESC", "2015"): "CAMBIO-MENOR", ("E-ESC", "2018"): "MISMO-INSTRUMENTO",
    ("E-LOC", "2015"): "MISMO-INSTRUMENTO", ("E-LOC", "2018"): "MISMO-INSTRUMENTO",
    ("E-FOR", "2015"): "CAMBIO-DE-INSTRUMENTO", ("E-FOR", "2018"): "MISMO-INSTRUMENTO",
    ("E-CTA", "2015"): "CAMBIO-DE-INSTRUMENTO", ("E-CTA", "2018"): "CAMBIO-MENOR",
}
CONSTRUCTO = {
    "D9": "D8: ahorra sólo informal sin la vía formal 8 («cuenta contratada por Internet o "
          "aplicación»), armonizado en 2018 (P5_9/P5_13 1-8) y 2021 (P5_4/P5_7 1-7 y 9)",
    "INFORMAL-CUALQUIERA": "informal cualquiera: alguna de las seis vías P5_1_1..P5_1_6 = 1",
}
CON = "con seguridad social"
SIN = "sin seguridad social"
INF_COLS = [f"P5_1_{i}" for i in range(1, 7)]
ACC21 = [f"P5_4_{i}" for i in range(1, 10)]
SAV21 = [f"P5_7_{i}" for i in range(1, 10)]
ACC21_8 = [c for c in ACC21 if c != "P5_4_8"]
SAV21_8 = [c for c in SAV21 if c != "P5_7_8"]
ACC18 = [f"P5_9_{i}" for i in range(1, 9)]
SAV18 = [f"P5_13_{i}" for i in range(1, 9)]


# ------------------------------------------------------------------ insumos
def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo(inputs, iid, nombre):
    mod = types.ModuleType(nombre)
    exec(compile(_bytes(inputs[iid]), nombre, "exec"), mod.__dict__)
    return mod


def _tsv(ent):
    lineas = [l for l in _bytes(ent).decode("utf-8").split("\n") if l.strip() and not l.startswith("#")]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def _json_resultados(inputs, iid):
    import json
    return json.loads(_bytes(inputs[iid]).decode("utf-8"))["resultados"]


def _slug(v):
    return (str(v).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
            .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
            .replace("_", "-").replace(" ", "-"))


def celdas_arbitro(inputs):
    """Las 32 celdas ENIF del árbitro, leídas de la tabla (E.5: la rejilla
    se lee, no se teclea)."""
    out = []
    for f in _tsv(inputs["ARBITRO-MARGINALES-METADATOS"]):
        if f["instrumento"] != "ENIF":
            continue
        rid = f["cell_id_R"]
        pref = "RESULT-ARBITRO-ENIF2024-"
        if not (rid.startswith(pref) and rid.endswith("-P")):
            raise RuntimeError(f"id de R inesperado: {rid}")
        des = DES_DE_OUTCOME[f["outcome"]]
        out.append({"clave": rid[len(pref):-2], "des": des, "eje": f["axis"], "cat": f["category"],
                    "rid": rid, "pid": f["cell_id_piso"], "calc_piso": f["calc_piso"],
                    "grupo": f"{des}-{_slug(f['axis'])}"})
    if len(out) != N_CELDAS_ENIF:
        raise RuntimeError(f"la tabla del árbitro trae {len(out)} celdas ENIF, no {N_CELDAS_ENIF}")
    return out


def _comparabilidad(inputs):
    tabla = {}
    for f in _tsv(inputs["AHORRO-COMPARABILIDAD-TEXTO"]):
        tabla[(f["objeto"], f["ola"])] = f["veredicto"]
    for k, v in VEREDICTOS_CONGELADOS.items():
        if tabla.get(k) != v:
            raise RuntimeError(f"comparabilidad por texto distinta de la congelada en {k}: "
                               f"tabla={tabla.get(k)!r}, spec={v!r}")
    return tabla


def usable(des, eje, ola):
    objs = OBJ_DES[des] + (OBJ_EJE[eje],)
    return all(VEREDICTOS_CONGELADOS[(o, ola)] in POSITIVOS for o in objs)


# ------------------------------------------------------------ constructos
def _grupos_2021(m, d, cuentas):
    a = d[cuentas].apply(m._code)
    account = pd.Series(pd.NA, index=d.index, dtype="object")
    account.loc[a.eq("1").any(axis=1)] = "con cuenta"
    account.loc[a.eq("2").all(axis=1)] = "sin cuenta"
    p310 = m._code(d["P3_10"])
    form = pd.Series(pd.NA, index=d.index, dtype="object")
    form.loc[p310.isin(list("12345"))] = CON
    form.loc[p310.eq("6")] = SIN
    return {"sexo": m._code(d["SEXO"]), "edad": m._age(d["EDAD"]),
            "escolaridad": m._school(d["P3_1_1"]),
            "localidad": m._code(d["TLOC"]).map({"1": "15 000 y mas", "2": "15 000 y mas",
                                                 "3": "menor de 15 000", "4": "menor de 15 000"}),
            "cuenta": account, "formalidad": form}


def _solo_informal(informal, formal):
    only = pd.Series(pd.NA, index=informal.index, dtype="Float64")
    only.loc[informal.eq(False) | formal.eq(True)] = 0.0
    only.loc[informal.eq(True) & formal.eq(False)] = 1.0
    return only


def _cells(celdas, prefijo, y_de, grupos, restringe=None):
    out = []
    for c in celdas:
        y = y_de[c["des"]]
        mask = grupos[c["eje"]].eq(c["cat"]) & y.notna()
        if restringe is not None:
            mask = mask & restringe
        out.append({"base": f"RESULT-{prefijo}-{c['clave']}", "mask": mask.fillna(False).astype(bool), "y": y})
    return out


def _diseno(d, pond):
    d["_w"] = pd.to_numeric(d[pond].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip()
    d["_upm"] = d["UPM_DIS"].str.strip()


def mide_2021(m, inputs, celdas, reps, seed, armonizada=True):
    """ORO (18+, nueve vías: reproduce los pisos sellados) y, si
    `armonizada`, la ola 2021 armonizada al marco del cambio (18-70, D8,
    cuenta sin la vía 8). Un solo plan de réplicas sobre el marco entero:
    el 18-70 es un dominio (máscara), no un recorte del marco."""
    cols = INF_COLS + ACC21 + SAV21 + ["SEXO", "EDAD", "TLOC", "P3_1_1", "P3_10",
                                       "FAC_ELE", "EST_DIS", "UPM_DIS"]
    d = m._csv(inputs["enif2021_csv"]["ruta_absoluta"], "conjunto_de_datos_tmodulo_enif_2021.csv", cols)
    _diseno(d, "FAC_ELE")
    informal = m._known_any(d, INF_COLS)
    y9 = {"D9": _solo_informal(informal, m._formal(d, ACC21, SAV21)),
          "INFORMAL-CUALQUIERA": informal.astype("Float64")}
    cells = _cells(celdas, "ORO2021", y9, _grupos_2021(m, d, ACC21))
    edad = pd.to_numeric(d["EDAD"], errors="coerce")
    en_1870 = (edad >= 18) & (edad <= 70)
    diag = {"FILAS": int(len(d)), "EN-18-70": int(en_1870.sum())}
    if armonizada:
        y8 = {"D9": _solo_informal(informal, m._formal(d, ACC21_8, SAV21_8)),
              "INFORMAL-CUALQUIERA": informal.astype("Float64")}
        cells += _cells(celdas, "H2021", y8, _grupos_2021(m, d, ACC21_8), restringe=en_1870)
        diag["D8-N-UNIVERSO-18-70"] = int((y8["D9"].notna() & en_1870).sum())
        diag["INFORMAL-N-UNIVERSO-18-70"] = int((y8["INFORMAL-CUALQUIERA"].notna() & en_1870).sum())
    return m._estimate(d, cells, reps, seed), diag


def mide_2018(m, h, inputs, celdas, reps, seed):
    cols = (INF_COLS + ["P5_4", "P5_5"] + ACC18 + SAV18
            + ["SEXO", "EDAD", "NIV", "TLOC", "P3_11", "FAC_PER", "EST_DIS", "UPM_DIS"])
    d = h._csv_zip(inputs["enif2018_csv"]["ruta_absoluta"], "conjunto_de_datos/tmodulo.csv", cols)
    _diseno(d, "FAC_PER")
    p54, p55 = m._code(d["P5_4"]), m._code(d["P5_5"])
    sin_filtro = p54.eq("2") & p55.eq("2")
    acc = d[ACC18].apply(m._code)
    blanco_por_pase = acc.eq("") & sin_filtro.to_numpy()[:, None]
    acc = acc.mask(blanco_por_pase, "2")           # spec §2: blanco por pase = No
    sav = d[SAV18].apply(m._code)
    informal = m._known_any(d, INF_COLS)
    formal8 = m._formal(pd.concat([acc, sav], axis=1), ACC18, SAV18)
    y = {"D9": _solo_informal(informal, formal8), "INFORMAL-CUALQUIERA": informal.astype("Float64")}
    account = pd.Series(pd.NA, index=d.index, dtype="object")
    account.loc[p54.eq("1") | p55.eq("1")] = "con cuenta"
    account.loc[sin_filtro] = "sin cuenta"
    p311 = m._code(d["P3_11"])
    form = pd.Series(pd.NA, index=d.index, dtype="object")
    form.loc[p311.isin(list("12345"))] = CON
    form.loc[p311.eq("6")] = SIN
    grupos = {"sexo": m._code(d["SEXO"]), "edad": m._age(d["EDAD"].str.strip()),
              "escolaridad": m._school(d["NIV"]),
              "localidad": m._code(d["TLOC"]).map({"1": "15 000 y mas", "2": "15 000 y mas",
                                                   "3": "menor de 15 000", "4": "menor de 15 000"}),
              "cuenta": account, "formalidad": form}
    usa = [c for c in celdas if usable(c["des"], c["eje"], "2018")]
    est = m._estimate(d, _cells(usa, "H2018", y, grupos), reps, seed)
    diag = {"FILAS": int(len(d)),
            "D8-N-UNIVERSO": int(y["D9"].notna().sum()),
            "INFORMAL-N-UNIVERSO": int(y["INFORMAL-CUALQUIERA"].notna().sum()),
            "SIN-FILTRO-CUENTA-N": int(sin_filtro.sum()),
            "P5-9-BLANCO-POR-PASE-N": int(blanco_por_pase.to_numpy().sum()),
            "CUENTA-FILTRO-SI-BATERIA-NO-N": int(((p54.eq("1") | p55.eq("1"))
                                                   & acc.eq("2").all(axis=1)).sum())}
    return est, diag


def mide_2015(m, h, inputs, celdas, reps, seed):
    """Sólo descriptivo (spec §3): informal cualquiera × ejes comparables."""
    cols = INF_COLS + ["SEXO", "EDAD", "NIV", "TLOC", "FAC_PER", "EST_DIS", "UPM_DIS"]
    d = h._dbf_zip(inputs["enif_2015_enif_2015_bd_dbf"]["ruta_absoluta"], "tmodulo1.DBF", cols)
    borrados = int(d.attrs.get("registros_borrados", 0))
    _diseno(d, "FAC_PER")
    y = {"INFORMAL-CUALQUIERA": m._known_any(d, INF_COLS).astype("Float64")}
    grupos = {"sexo": m._code(d["SEXO"]), "edad": m._age(d["EDAD"].str.strip()),
              "escolaridad": m._school(d["NIV"]),
              "localidad": m._code(d["TLOC"]).map({"1": "15 000 y mas", "2": "15 000 y mas",
                                                   "3": "menor de 15 000", "4": "menor de 15 000"})}
    usa = [c for c in celdas if c["des"] == "INFORMAL-CUALQUIERA" and usable(c["des"], c["eje"], "2015")]
    est = m._estimate(d, _cells(usa, "H2015", y, grupos), reps, seed)
    return est, {"FILAS": int(len(d)), "REGISTROS-DBF-BORRADOS": borrados,
                 "INFORMAL-N-UNIVERSO": int(y["INFORMAL-CUALQUIERA"].notna().sum())}


# ------------------------------------------------------------- aritmética
def _logit(p):
    if p is None:
        return None
    p = float(p)
    if not (0.0 < p < 1.0):
        return None
    return math.log(p / (1.0 - p))


def _expit(x):
    return 1.0 / (1.0 + math.exp(-x))


def _ee_logit(lo, hi):
    a, b = _logit(lo), _logit(hi)
    if a is None or b is None or not b > a:
        return None
    return (b - a) / (2.0 * Z95)


def _wilson(k, n):
    if n <= 0:
        return (None, None)
    p = k / n
    z2 = Z95 * Z95
    den = 1 + z2 / n
    centro = (p + z2 / (2 * n)) / den
    semi = Z95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return (max(0.0, centro - semi), min(1.0, centro + semi))


def _lectura_x(cob, lo_cong):
    if cob is None:
        return "NO-EVALUABLE"
    if cob < UMBRAL_PISO:
        return "NO-CUMPLE-PERSISTENCIA-TRIENAL-NO-ES-PISO"
    if cob < UMBRAL_X:
        return "NO-CUMPLE"
    return "CUMPLE" if (lo_cong is not None and lo_cong >= UMBRAL_PISO) else "CUMPLE-CON-RESERVA"


def calibra(celdas, piso, R, h18, h21, h15=None):
    """La regla congelada (spec §4), pura: no lee nada."""
    out = {}
    grupos = {}
    filas = []
    for c in celdas:
        k = c["clave"]; b = f"{PREF}-{k}"
        base_p = c["pid"][:-2]
        p21, lo21, hi21 = piso[c["pid"]], piso[base_p + "-IC-LO"], piso[base_p + "-IC-HI"]
        r = R[c["rid"]]
        e18, e21 = h18.get(k), h21.get(k)
        d = None
        if e18 is not None and e21 is not None:
            l18, l21 = _logit(e18["P"]), _logit(e21["P"])
            if l18 is not None and l21 is not None:
                d = l21 - l18
        ruido = None
        if e18 is not None and e21 is not None:
            s18, s21 = _ee_logit(e18["LO"], e18["HI"]), _ee_logit(e21["LO"], e21["HI"])
            if s18 is not None and s21 is not None:
                ruido = s18 * s18 + s21 * s21
        d15 = None
        e15 = (h15 or {}).get(k)
        if e15 is not None and e18 is not None:
            l15, l18 = _logit(e15["P"]), _logit(e18["P"])
            if l15 is not None and l18 is not None:
                d15 = l18 - l15
        g = grupos.setdefault(c["grupo"], {"d": [], "ruido": [], "d15": [], "celdas": []})
        g["celdas"].append(k)
        if d is not None:
            g["d"].append(d)
        if ruido is not None:
            g["ruido"].append(ruido)
        if d15 is not None:
            g["d15"].append(d15)
        filas.append((c, b, p21, lo21, hi21, r, e18, e21, e15, d, d15))

    for gk, g in grupos.items():
        gb = f"{PREF}-G-{gk}"
        n = len(g["d"])
        tau2 = sum(x * x for x in g["d"]) / n if n else None
        g["tau2"] = tau2
        out[f"{gb}-N-CELDAS"] = len(g["celdas"])
        out[f"{gb}-N-DELTAS"] = n
        out[f"{gb}-TAU2-LOGIT"] = tau2
        out[f"{gb}-TAU-LOGIT"] = math.sqrt(tau2) if tau2 is not None else None
        out[f"{gb}-DELTA-MEDIO-LOGIT"] = sum(g["d"]) / n if n else None
        out[f"{gb}-RUIDO-MEDIO-LOGIT"] = (sum(g["ruido"]) / len(g["ruido"])) if g["ruido"] else None
        out[f"{gb}-OLAS-DEL-CAMBIO"] = "2018→2021"
        todas = g["d"] + g["d15"]
        out[f"{gb}-DESCRIPTIVO-N-DELTAS-CON-2015"] = len(todas)
        out[f"{gb}-DESCRIPTIVO-TAU2-LOGIT-CON-2015"] = (sum(x * x for x in todas) / len(todas)
                                                         if g["d15"] else None)

    agregados = {}
    for (c, b, p21, lo21, hi21, r, e18, e21, e15, d, d15) in filas:
        tau2 = grupos[c["grupo"]]["tau2"]
        ee_m = _ee_logit(lo21, hi21)
        lp = _logit(p21)
        ok = tau2 is not None and ee_m is not None and lp is not None
        if ok:
            ee_c = math.sqrt(ee_m * ee_m + tau2)
            ic_inf, ic_sup = _expit(lp - Z95 * ee_c), _expit(lp + Z95 * ee_c)
            dentro = "DENTRO" if ic_inf <= float(r) <= ic_sup else "FUERA"
        else:
            ee_c = ic_inf = ic_sup = None
            dentro = "NO-CALIBRABLE"
        muestral = "DENTRO" if float(lo21) <= float(r) <= float(hi21) else "FUERA"
        out.update({
            f"{b}-PISO-P": float(p21), f"{b}-PISO-IC-LO": float(lo21), f"{b}-PISO-IC-HI": float(hi21),
            f"{b}-R2024-P": float(r),
            f"{b}-EE-LOGIT-MUESTRAL": ee_m, f"{b}-TAU2-LOGIT-GRUPO": tau2,
            f"{b}-EE-LOGIT-CALIBRADO": ee_c,
            f"{b}-IC-CALIBRADO-INF": ic_inf, f"{b}-IC-CALIBRADO-SUP": ic_sup,
            f"{b}-TIPO-INCERTIDUMBRE": TIPO_INCERTIDUMBRE, f"{b}-ROTULO": ROTULO,
            f"{b}-R-EN-IC-CALIBRADO": dentro, f"{b}-R-EN-IC-MUESTRAL": muestral,
            f"{b}-GRUPO-DE-POOLING": c["grupo"], f"{b}-CONSTRUCTO-DEL-CAMBIO": CONSTRUCTO[c["des"]],
            f"{b}-DELTA-LOGIT-2018-2021": d,
        })
        for ola, e in (("2018", e18), ("2021", e21)):
            out[f"{b}-H{ola}-P"] = e["P"] if e else None
            out[f"{b}-H{ola}-IC-LO"] = e["LO"] if e else None
            out[f"{b}-H{ola}-IC-HI"] = e["HI"] if e else None
            out[f"{b}-H{ola}-N"] = e["N"] if e else 0
        if h15 is not None and c["des"] == "INFORMAL-CUALQUIERA" and usable(c["des"], c["eje"], "2015"):
            out[f"{b}-DESCRIPTIVO-H2015-P"] = e15["P"] if e15 else None
            out[f"{b}-DESCRIPTIVO-H2015-N"] = e15["N"] if e15 else 0
            out[f"{b}-DESCRIPTIVO-DELTA-LOGIT-2015-2018"] = d15
        for ag in ("GLOBAL", f"DESENLACE-{c['des']}", f"EJE-{_slug(c['eje'])}", f"CONGLOMERADO-{c['grupo']}"):
            a = agregados.setdefault(ag, {"n": 0, "k": 0, "nc": 0, "km": 0, "nm": 0, "grupos": set()})
            a["nm"] += 1
            a["km"] += muestral == "DENTRO"
            if dentro == "NO-CALIBRABLE":
                a["nc"] += 1
            else:
                a["n"] += 1
                a["k"] += dentro == "DENTRO"
                a["grupos"].add(c["grupo"])

    for ag, a in agregados.items():
        ab = f"{PREF}-AGG-{ag}"
        n, k = a["n"], a["k"]
        cob = k / n if n else None
        lo, hi = _wilson(k, n)
        out.update({f"{ab}-N": n, f"{ab}-N-DENTRO": k, f"{ab}-N-NO-CALIBRABLE": a["nc"],
                    f"{ab}-COBERTURA": cob, f"{ab}-COBERTURA-IC-LO": lo, f"{ab}-COBERTURA-IC-HI": hi,
                    f"{ab}-CONTROL-MUESTRAL-N-DENTRO": a["km"],
                    f"{ab}-CONTROL-MUESTRAL-COBERTURA": a["km"] / a["nm"] if a["nm"] else None,
                    f"{ab}-ROTULO": ROTULO})
        if ag == "GLOBAL":
            ng = len(a["grupos"])
            if n and ng:
                p = k / n; z2 = Z95 * Z95; den = 1 + z2 / ng
                centro = (p + z2 / (2 * ng)) / den
                semi = Z95 * math.sqrt(p * (1 - p) / ng + z2 / (4 * ng * ng)) / den
                clo, chi = max(0.0, centro - semi), min(1.0, centro + semi)
            else:
                clo = chi = None
            out[f"{ab}-N-CONGLOMERADOS"] = ng
            out[f"{ab}-COBERTURA-IC-CONGLOMERADO-LO"] = clo
            out[f"{ab}-COBERTURA-IC-CONGLOMERADO-HI"] = chi
            out[f"{ab}-CONTROL-MUESTRAL-COTEJO"] = ("COINCIDE" if a["km"] == CONTROL_MUESTRAL_N_DENTRO
                                                    else "DISCREPA")
            out[f"{PREF}-REGLA-X-LECTURA-MECANICA"] = _lectura_x(cob, clo)
    return out


def _extrae(est, prefijo, celdas):
    """{clave: {P, LO, HI, N}} desde la salida de `_estimate` (None si la
    celda no se midió)."""
    out = {}
    for c in celdas:
        b = f"RESULT-{prefijo}-{c['clave']}"
        if b + "-P" in est:
            out[c["clave"]] = {"P": est[b + "-P"], "LO": est[b + "-IC-LO"],
                               "HI": est[b + "-IC-HI"], "N": int(est[b + "-N"])}
    return out


def oro(celdas, est21, piso):
    """|recalculado 18+ − piso sellado| sobre P, IC-LO, IC-HI; N exacto."""
    maxd, discordes = 0.0, 0
    for c in celdas:
        b = f"RESULT-ORO2021-{c['clave']}"
        base_p = c["pid"][:-2]
        for suf in ("-P", "-IC-LO", "-IC-HI"):
            v, s = est21.get(b + suf), piso.get(base_p + suf)
            if v is None or s is None:
                discordes += 1
                continue
            dd = abs(float(v) - float(s)); maxd = max(maxd, dd)
            discordes += dd > TOL_ORO
        if est21.get(b + "-N") != piso.get(base_p + "-N"):
            discordes += 1
    return maxd, discordes


def medir(inputs, contrato):
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    m = _modulo(inputs, "MEDIDOR-EJES-0003", "medidor_ejes_0003")
    h = _modulo(inputs, "MEDIDOR-CREDITO-HISTORIA", "medidor_credito_historia")
    _comparabilidad(inputs)
    celdas = celdas_arbitro(inputs)
    piso = dict(_json_resultados(inputs, "PISO-ENIF2021-EJES"))
    piso.update(_json_resultados(inputs, "PISO-ENIF2021-FORMALIDAD"))
    R = _json_resultados(inputs, "R-ENIF2024")

    est21, diag21 = mide_2021(m, inputs, celdas, reps, seed, armonizada=True)
    est18, diag18 = mide_2018(m, h, inputs, celdas, reps, seed)
    est15, diag15 = mide_2015(m, h, inputs, celdas, reps, seed)
    h21 = _extrae(est21, "H2021", celdas)
    h18 = _extrae(est18, "H2018", celdas)
    h15 = _extrae(est15, "H2015", celdas)

    out = calibra(celdas, piso, R, h18, h21, h15)
    maxd, discordes = oro(celdas, est21, piso)
    out[f"{PREF}-ORO-2021-MAX-ABS"] = maxd
    out[f"{PREF}-ORO-2021-N-DISCORDES"] = discordes
    out[f"{PREF}-ORO-2021-VEREDICTO"] = "REPRODUCE" if discordes == 0 else "NO-REPRODUCE"
    for ola, dg in (("2021", diag21), ("2018", diag18), ("2015", diag15)):
        for k, v in dg.items():
            out[f"{PREF}-DIAG-{ola}-{k}"] = v
    out[f"{PREF}-N-CELDAS"] = len(celdas)
    out[f"{PREF}-ROTULO"] = ROTULO
    out[f"{PREF}-TIPO-INCERTIDUMBRE"] = TIPO_INCERTIDUMBRE
    return out
