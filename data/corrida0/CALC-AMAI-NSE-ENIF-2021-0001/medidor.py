"""NSE AMAI por instrumento, validación contra AMAI y pisos por grupo de NSE.

Contrato: `forense/prereg-caja/AMAI-NSE-spec-v1_0.md`. El primer resultado que
produzca este procedimiento es el que se reporta. Un medidor, seis CALC:
`parametros.instrumento` ∈ {ENIGH, ENIF, ENDUTIH} y `parametros.ola` eligen
adaptador y conductas; nada más cambia entre CALC.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from tools.dominios.amai import componentes as C
from tools.dominios.amai import imputacion as I
from tools.dominios.amai import regla as R

GRUPOS = list(R.ORDEN_GRUPOS)

CONDUCTAS = {
    ("ENIGH", "2022"): ("recibe_remesas",),
    ("ENIF", "2021"): (),
    ("ENIF", "2024"): (
        "tiene_ahorros_enif2024", "no_tiene_ahorros_enif2024",
        "informal_cualquiera", "formal_cualquiera", "ahorra_solo_informal",
        "ahorra_solo_formal", "ahorra_ambas_vias", "no_ahorra",
        "horizonte_corto_sin_ss", "horizonte_no_corto_sin_ss",
        "horizonte_corto_con_ss", "horizonte_no_corto_con_ss",
        "desconfia_conoce_proteccion", "desconfia_no_conoce_proteccion",
        "horizonte_corto_no_trabaja",
        "recibe_dinero_familiares_para_vejez", "no_recibe_dinero_familiares_para_vejez",
    ),
    ("ENDUTIH", "2023"): None, ("ENDUTIH", "2024"): None, ("ENDUTIH", "2025"): None,
}
MEDIDAS_ENDUTIH = (
    "internet", "celular", "actividad_mensajes", "actividad_tramite",
    "no_internet_acceso", "no_internet_costo", "no_internet_preferencia",
    "no_celular_costo", "no_celular_preferencia", "no_celular_cobertura",
)
for _o in ("2023", "2024", "2025"):
    CONDUCTAS[("ENDUTIH", _o)] = MEDIDAS_ENDUTIH


def _sha(modulo) -> str:
    return hashlib.sha256(Path(modulo.__file__).read_bytes()).hexdigest()


# ------------------------------------------------------------------ NSE

def nse_hogares(inst: str, ola: str, ruta: str, ruta_donante: str | None) -> tuple[pd.DataFrame, dict]:
    """Una fila por hogar con puntaje, nivel y grupo (NaN si falta un
    componente) y un diagnóstico de construcción."""
    diag = {}
    if inst == "ENIGH":
        comp = C.enigh2022(ruta)
    elif inst == "ENIF":
        comp = C.enif(ruta, ola)
    elif inst == "ENDUTIH":
        comp = C.endutih(ruta, ola)
    else:
        raise ValueError(inst)
    if inst == "ENDUTIH":
        donante = I.tabla_donante(C.enigh2022(ruta_donante))
        imp, usado = I.imputa(comp, donante)
        puntaje = I.puntos_observados_endutih(comp) + imp
        diag["imputacion_n_donantes"] = donante["n_donantes"]
        diag["imputacion_nivel_celda"] = {str(k): int(v) for k, v in
                                          usado.value_counts().sort_index().items()}
    else:
        pts = R.puntos(comp[list(R.COMPONENTES)])
        puntaje = pts.sum(axis=1, min_count=len(R.COMPONENTES))
        puntaje[pts.isna().any(axis=1)] = np.nan
    comp = comp.assign(puntaje=puntaje)
    comp["nivel"] = R.nivel(comp["puntaje"])
    comp["grupo"] = R.grupo(comp["nivel"])
    diag["componentes_faltantes"] = {c: int(comp[c].isna().sum()) for c in R.COMPONENTES}
    return comp, diag


def distribucion(comp: pd.DataFrame) -> dict:
    ok = comp["nivel"].notna() & comp["factor"].gt(0)
    w = comp.loc[ok, "factor"].astype(float)
    tot = float(w.sum())
    base = {"n_hogares": int(len(comp)), "n_hogares_con_nse": int(ok.sum()),
            "n_hogares_sin_nse": int((~ok).sum())}
    if tot <= 0:
        return {**base, "niveles": {n: None for n in R.NIVELES},
                "grupos": {g: None for g in GRUPOS}, "masa_puntaje_cero": None}
    niv = {n: float(w[comp.loc[ok, "nivel"].eq(n)].sum() / tot) for n in R.NIVELES}
    gru = {g: float(w[comp.loc[ok, "grupo"].eq(g)].sum() / tot) for g in GRUPOS}
    return {**base, "niveles": niv, "grupos": gru,
            "masa_puntaje_cero": float(w[comp.loc[ok, "puntaje"].eq(0)].sum() / tot)}


def validacion(inst: str, dist: dict, par: dict) -> dict:
    if dist["n_hogares_con_nse"] == 0:
        return {"estado": "SIN-HOGARES-CON-NSE", "desvio_max_grupo_pp": None,
                "desvio_max_nivel_pp": None, "desvio_grupo": None, "desvio_nivel": None,
                "referencia_grupo": None,
                "referencia": "nota AMAI 2024 p.4 Figura 1 (ENIGH 2022)"}
    ref_niv = {k: v / 100 for k, v in R.AMAI_2022_PCT.items()}
    ref_gru = {g: sum(ref_niv[n] for n in R.NIVELES if R.GRUPOS[n] == g) for g in GRUPOS}
    dn = {n: dist["niveles"][n] - ref_niv[n] for n in R.NIVELES}
    dg = {g: dist["grupos"][g] - ref_gru[g] for g in GRUPOS}
    max_g = max(abs(v) for v in dg.values()) * 100
    max_n = max(abs(v) for v in dn.values()) * 100
    if inst == "ENIGH":
        estado = ("CALCULABLE-REPRODUCE-AMAI" if max_n <= float(par["tolerancia_reproduce_pp"])
                  else "CALCULABLE-NO-REPRODUCE-AMAI")
    else:
        estado = ("APROXIMACION-CONFORME" if max_g <= float(par["umbral_desvio_pp"])
                  else "APROXIMACION-DESVIADA")
    return {"estado": estado, "desvio_max_grupo_pp": max_g, "desvio_max_nivel_pp": max_n,
            "desvio_grupo": dg, "desvio_nivel": dn, "referencia_grupo": ref_gru,
            "referencia": "nota AMAI 2024 p.4 Figura 1 (ENIGH 2022)"}


def concordancia_proxy_endutih(comp_enigh: pd.DataFrame) -> dict:
    """Diagnóstico en ENIGH 2022: la aproximación ENDUTIH (autos a sí/no,
    baños y dormitorios imputados) contra la regla exacta, mismo hogar."""
    donante = I.tabla_donante(comp_enigh)
    base = comp_enigh.copy()
    base["autos"] = (base["autos"] > 0).astype(float).where(base["autos"].notna())
    imp, _ = I.imputa(base, donante)
    prox = I.puntos_observados_endutih(base) + imp
    niv_p = R.nivel(prox)
    ok = comp_enigh["nivel"].notna() & niv_p.notna()
    w = comp_enigh.loc[ok, "factor"].astype(float)
    if float(w.sum()) <= 0:
        return {"concordancia_nivel": None, "concordancia_grupo": None, "n_hogares": 0}
    same_n = float(w[comp_enigh.loc[ok, "nivel"].eq(niv_p[ok])].sum() / w.sum())
    same_g = float(w[comp_enigh.loc[ok, "grupo"].eq(R.grupo(niv_p)[ok])].sum() / w.sum())
    return {"concordancia_nivel": same_n, "concordancia_grupo": same_g,
            "n_hogares": int(ok.sum())}


# ---------------------------------------------------------------- conductas

def _conductas_enif2024(ruta: str) -> tuple[pd.DataFrame, dict]:
    from tools.astra.region import enif_condicionales, enif_no_trabaja, enif_portafolio
    inf = [f"P5_1_{i}" for i in range(1, 7)]
    form = [f"P5_6_{i}" for i in range(1, 10)]
    cols = (["LLAVEHOG", "EDAD_V", "FAC_PER", "EST_DIS", "UPM_DIS", "P3_8", "P3_9",
             "P4_10", "P3_13", "P5_20", "P5_23", "FILTRO_S9_1", "P9_9_4"]
            + inf + form + [f"P5_4_{i}" for i in range(1, 10)])
    d = C.csv_zip(ruta, "TMODULO.csv", cols)
    valid, port = enif_portafolio.desenlaces(d)
    defs = {"tiene_ahorros_enif2024": (valid, valid & ~port["no_tiene_ahorros_enif2024"])}
    defs.update({k: (valid, v) for k, v in port.items()})
    defs.update(enif_condicionales.dominios_condicionales(d))
    defs["horizonte_corto_no_trabaja"] = enif_no_trabaja.dominio(d)
    # Vejez: universo de CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1 (spec humana
    # ENIF-DINERO-FAMILIARES-VEJEZ): FILTRO_S9_1=2, EDAD_V<71, P9_9_4 ∈ {1,2}.
    f9 = C._num(d["FILTRO_S9_1"])
    edad = C._num(d["EDAD_V"])
    p994 = C._num(d["P9_9_4"])
    den_v = f9.eq(2) & edad.lt(71) & p994.isin([1, 2])
    defs["recibe_dinero_familiares_para_vejez"] = (den_v, den_v & p994.eq(1))
    defs["no_recibe_dinero_familiares_para_vejez"] = (den_v, den_v & p994.eq(2))
    d = d.assign(_llave=d["LLAVEHOG"])
    return d.rename(columns={"FAC_PER": "_w"}), defs


def _conductas_endutih(ruta: str, ola: str) -> tuple[pd.DataFrame, dict]:
    from tools.dominios.endutih import pisos as P
    first, second, entity = P.FILES[ola]
    rows = P._merge(P._load(Path(ruta), first, P.MAIN + (entity,)),
                    P._load(Path(ruta), second, P.SECOND))
    d = pd.DataFrame(rows)
    edad = C._num(d["EDAD"])
    w = C._num(d["FAC_PER"])
    keep = edad.ge(6) & w.gt(0) & np.isfinite(w) & d["EST_DIS"].ne("") & d["UPM_DIS"].ne("")
    d = d[keep].reset_index(drop=True)
    defs = {}
    for m in MEDIDAS_ENDUTIH:
        st = pd.Series([P._status(r, m) for r in d.to_dict("records")])
        den = st.isin(["SI", "NO"])
        defs[m] = (den, den & st.eq("SI"))
    d = d.assign(_llave=d[C.LLAVE_HOG_ENDUTIH].agg("|".join, axis=1), _w=C._num(d["FAC_PER"]))
    return d, defs


def _conductas_enigh(comp: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    d = comp.copy()
    den = d["remesas"].notna()
    return d.assign(_llave=d["llave"], _w=d["factor"]), {
        "recibe_remesas": (den, den & d["remesas"].gt(0))}


def pisos(personas: pd.DataFrame, defs: dict, comp: pd.DataFrame, orden: tuple,
          par: dict, semilla: int) -> dict:
    from tools.astra.region.estadistica import estima_dominios
    grupo = personas["_llave"].map(comp.set_index("llave")["grupo"])
    geo = grupo.fillna("SIN-NSE").astype(str)
    base = personas.assign(_fac=personas["_w"].astype(float))
    out = {}
    for conducta in orden:
        den, y = defs[conducta]
        filas, meta = estima_dominios(
            base, geo, den.reset_index(drop=True), y.reset_index(drop=True),
            factor="_fac", estrato="EST_DIS", upm="UPM_DIS", dominios=GRUPOS,
            representativos=set(GRUPOS), semilla=semilla,
            replicas=int(par["bootstrap_replicas"]), n_min=int(par["n_min"]))
        out[conducta] = {"filas": filas, "diseno": meta,
                         "n_denominador_sin_nse": int((den & geo.eq("SIN-NSE")).sum())}
    return out


# ------------------------------------------------------------------ medir

def medir(inputs: dict, contrato: dict) -> dict:
    par = contrato["parametros"]
    inst, ola = par["instrumento"], str(par["ola"])
    orden = CONDUCTAS[(inst, ola)]
    if tuple(par["conductas"]) != tuple(orden):
        raise RuntimeError("lista de conductas distinta de la congelada")
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    donante = inputs[par["input_donante"]]["ruta_absoluta"] if par.get("input_donante") else None
    semilla = int(contrato["seed"]["valor"])
    comp, diag = nse_hogares(inst, ola, ruta, donante)
    dist = distribucion(comp)
    val = validacion(inst, dist, par)
    extra = {}
    if inst == "ENIGH":
        extra["concordancia_proxy_endutih"] = concordancia_proxy_endutih(comp)
    if inst == "ENIGH":
        personas, defs = _conductas_enigh(comp)
    elif inst == "ENIF" and orden:
        personas, defs = _conductas_enif2024(ruta)
    elif inst == "ENDUTIH":
        personas, defs = _conductas_endutih(ruta, ola)
    else:
        personas, defs = None, {}
    tabla = pisos(personas, defs, comp, orden, par, semilla) if orden else {}
    from tools.astra.region import estadistica
    modulos = {"regla": _sha(R), "componentes": _sha(C), "imputacion": _sha(I),
               "estimador_u5": _sha(estadistica)}
    pref = f"RESULT-AMAI-NSE-{inst}-{ola}"
    doc = {"instrumento": inst, "ola": ola, "construccion": diag, "distribucion": dist,
           "validacion": val, "pisos": tabla, "modulos_sha256": modulos, **extra}
    out = {pref + "-JSON": json.dumps(doc, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":"), allow_nan=False)}
    for n in R.NIVELES:
        out[f"{pref}-DIST-{n}-P"] = dist["niveles"][n]
    for g in GRUPOS:
        out[f"{pref}-DIST-{g}-P"] = dist["grupos"][g]
    out[pref + "-N-HOGARES-CON-NSE"] = dist["n_hogares_con_nse"]
    out[pref + "-N-HOGARES-SIN-NSE"] = dist["n_hogares_sin_nse"]
    out[pref + "-VALIDACION-ESTADO"] = val["estado"]
    out[pref + "-DESVIO-MAX-GRUPO-PP"] = val["desvio_max_grupo_pp"]
    out[pref + "-DESVIO-MAX-NIVEL-PP"] = val["desvio_max_nivel_pp"]
    if inst == "ENIGH":
        c = extra["concordancia_proxy_endutih"]
        out[pref + "-PROXY-ENDUTIH-CONCORDANCIA-GRUPO"] = c["concordancia_grupo"]
        out[pref + "-PROXY-ENDUTIH-CONCORDANCIA-NIVEL"] = c["concordancia_nivel"]
    for conducta in orden:
        for f in tabla[conducta]["filas"]:
            b = f"{pref}-{conducta}-{f['geografia']}"
            out[b + "-P"] = f["punto"]
            out[b + "-IC-LO"] = f["ic_inf"]
            out[b + "-IC-HI"] = f["ic_sup"]
            out[b + "-N"] = f["n"]
            out[b + "-ESTADO"] = f["estado"]
    return out
