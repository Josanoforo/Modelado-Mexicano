#!/usr/bin/env python3
"""Medidor de APERTURA de ENADID 2023 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENADID-2023-spec-v1_0.md`; contrato: `APERTURA-ENADID-2023-spec.yaml`;
receta: `RECETA-APERTURA-ENADID-2023.md`. NO SE HA CORRIDO sobre ENADID 2023: corre sólo en caja,
en el commit de apertura que mesa autorice.

Una apertura sirve a los DOS contendientes sellados antes (E.6), con UNA comparación primaria
(cobertura de todas las celdas puntuadas; conglomerado = CALC contendiente):

  · `CALC-ENADID-FAMILIA-HOGARES-0001` (prefijo de celda `FAM-`): piso 2018 con IC calibrado de
    persistencia 2009-2014-2018 (ICC-LO/ICC-HI). HOGAR-CON-MIGRANTE-INTERNACIONAL-5A no tiene ICC (dos
    olas): R se reporta, no se puntúa. PERSONA-15MAS-UNIDA y UNIDO-15MAS-EN-UNION-LIBRE en TOTAL, SEXO y
    EDAD: cruce ya visto de ENADID 2023 (CALC-ENADID-0001, CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004,
    `p3_27` por sexo y edad, anteriores al sello del contendiente) → apartadas de la primaria (lo/hi
    None), R descriptiva (spec §0, §4).
  · `CALC-ENADID-COLA-2018-0001` (prefijo `COLA-`): piso 2018 con IC95 de DISEÑO (IC-LO/IC-HI; una ola
    abierta, sin persistencia).

R = razón ponderada por categoría de UN eje a la vez, con la recodificación de cada medidor sellado
(inputs `origen: repo`, sha fijado) y los códigos de la ola del piso 2018. Único renombre declarado
antes de abrir: la situación conyugal de TSDEM, `p3_21` en 2018, es `p3_27` en 2023 (mismos códigos
1..7; LEÍDO en el spec sellado de CALC-ENADID2023-UNION-SEXO-EDAD-0004 y CALC-ENADID-0001).
Guardia E.6: auditoría AST de este archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo`
es el único agregador. Columna ausente de reactivo o eje → vacío → NO-ESTIMABLE en las celdas que la
usan; llave/ponderador/diseño/parentesco del jefe ausente o miembro CSV ausente → ParoDeGuardia.
"""
from __future__ import annotations

import ast
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENADID-2023"
P = "RESULT-APERTURA-ENADID-2023"
FAM_CALC = "CALC-ENADID-FAMILIA-HOGARES-0001"
COLA_CALC = "CALC-ENADID-COLA-2018-0001"
OLA_CODIGOS = "2018"  # códigos, campos y miembros fijados sobre la ola del piso
CONYU_2023 = "p3_27"  # renombre declarado (spec §5): rol de PER["2018"]["conyu"] = "p3_21"
APARTADAS = {("PERSONA-15MAS-UNIDA", e) for e in ("TOTAL", "SEXO", "EDAD")} | \
            {("UNIDO-15MAS-EN-UNION-LIBRE", e) for e in ("TOTAL", "SEXO", "EDAD")}
DEPENDE_MIG = ("p4_6", "p4_15")  # sin ellas, las dos conductas de jefatura de COLA no tienen universo


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

FAM_MED = ("familia_medidor", f"data/corrida0/{FAM_CALC}/medidor.py",
           "7ff64d94b1a8cb59f0df3a62dd54f256cb4907b5da1d5e6e3cdeff7028dc3863")
FAM_PISO = ("familia_resultados", f"data/corrida0/{FAM_CALC}/resultados.json",
            "51d8ad9fb49a64e53c560316f818567a73d4144230da0fa89fed72f64cee8ee4")
COLA_MED = ("cola_medidor", f"data/corrida0/{COLA_CALC}/medidor.py",
            "d5ed69920078262d1e1e01894f4ee2cfae1e6f9e1cf40120edd86025352d72c3")
COLA_PISO = ("cola_resultados", f"data/corrida0/{COLA_CALC}/resultados.json",
             "ad62e897caf13f2bf7e7bc8e53e9291937a530e0f192cdf405260aefb3eb947a")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
LECTORES = ("lectores_familia", "tools/dominios/familia/lectores.py",
            "4e71238800c2c1a0d9215443dc8aadbb8add35b120c0c0ff1c1e87773e62e331")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "enadid2023_base_datos_csv"

CONTRATO = {
    "x": X, "programa": "ENADID", "ola": "2023", "unidad": "HOGAR y PERSONA (por celda; nunca promediadas entre sí)",
    "contendientes": [FAM_CALC, COLA_CALC],
    "payloads": [(PAYLOAD, "ENADID 2023 base CSV (THOGAR, TSDEM, TMUJER2, TMIGRANTE) -- ola RESERVADA para estas "
                           "conductas; sólo este medidor la lee")],
    "repo": [(FAM_MED[0], FAM_MED[1], "medidor sellado FAMILIA: HOG/PER/columnas_*/prepara_*/conductas_*/rid"),
             (FAM_PISO[0], FAM_PISO[1], "piso 2018 sellado FAMILIA: P, ICC-LO, ICC-HI por celda"),
             (COLA_MED[0], COLA_MED[1], "medidor sellado COLA: COND_*/MAPAS_*/EJES_*/EDADES/COLS_*/MIEMBROS/derivadas_*"),
             (COLA_PISO[0], COLA_PISO[1], "piso 2018 sellado COLA: P, IC-LO, IC-HI (diseño) por celda"),
             (RECETA[0], RECETA[1], "num de la receta de pisos (FAMILIA)"),
             (LECTORES[0], LECTORES[1], "lee_csv_zip (miembro sin distinguir mayúsculas)"),
             (MOTOR[0], MOTOR[1], "prepara_diseno/recodifica/eje_mapa/eje_rango/num/rid (COLA)"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "FAMILIA: hogares de THOGAR con fac_viv > 0, est_dis y upm_dis no vacíos, y residentes de TSDEM enlazados por "
                "llave_hog; COLA: mujeres de TMUJER2 15-54 con fac_per > 0 y diseño válido, y jefaturas (paren = 1) de TSDEM "
                "con fac_viv > 0 y diseño válido, emigrante varón fuera por TMIGRANTE (p4_6 = 1, p4_15 en {1, 3})",
    "filtros": "Un eje a la vez (los de cada contendiente); nunca cruces (guardia E.6)",
    "ponderador": "fac_viv (hogares y residentes), fac_per (mujeres)",
    "transformacion": "Recodificación de cada contendiente (specs FAMILIA-ENADID-PISOS §2 y COLA-ENADID-PISOS) con códigos 2018; "
                      "renombre declarado p3_21 -> p3_27 (situación conyugal TSDEM 2023); columna ausente o con texto/códigos "
                      "distintos -> NO-ESTIMABLE; llave/ponderador/diseño ausente -> PARO",
    "estimando": "R = Σw·y/Σw por contendiente×conducta×eje×categoría en ENADID 2023; cobertura de R en el ICC 2018 "
                 "(FAMILIA) o en el IC95 de diseño 2018 (COLA)",
    "variables": ([{"nombre": f"FAM-{c}", "definicion": f"conducta de {FAM_CALC} (unidad {u})"} for c, u in (
        ("HOGAR-UNIPERSONAL", "HOGAR"), ("HOGAR-NUCLEAR", "HOGAR"), ("HOGAR-AMPLIADO", "HOGAR"),
        ("HOGAR-JEFATURA-FEMENINA", "HOGAR"), ("HOGAR-CON-MIGRANTE-INTERNACIONAL-5A", "HOGAR"),
        ("PERSONA-60MAS", "PERSONA"), ("AM60-VIVE-SOLO", "PERSONA"), ("AM60-EN-HOGAR-AMPLIADO", "PERSONA"),
        ("JOVEN-25-34-HIJO-DEL-JEFE", "PERSONA"), ("PERSONA-15MAS-UNIDA", "PERSONA"),
        ("UNIDO-15MAS-EN-UNION-LIBRE", "PERSONA"))]
        + [{"nombre": f"COLA-{c}", "definicion": f"conducta de {COLA_CALC} (unidad {u})"} for c, u in (
            ("SEPARADA-ENTRE-UNION-LIBRE", "PERSONA (mujer 15-54)"),
            ("SEPARADA-O-DIVORCIADA-ENTRE-MATRIMONIO", "PERSONA (mujer 15-54)"),
            ("JEFATURA-FEMENINA-CON-MIGRANTE-VARON", "HOGAR"), ("JEFATURA-FEMENINA-SIN-MIGRANTE-VARON", "HOGAR"))]),
}


def sellados(inputs=None):
    F = E.modulo("m_enadid_familia_sellado", E.bytes_repo(inputs, *FAM_MED))
    C = E.modulo("m_enadid_cola_sellado", E.bytes_repo(inputs, *COLA_MED))
    R = E.modulo("receta_pisos_enadid", E.bytes_repo(inputs, *RECETA))
    L = E.modulo("lectores_familia_enadid", E.bytes_repo(inputs, *LECTORES))
    Mo = E.modulo("motor_pisos_enadid", E.bytes_repo(inputs, *MOTOR))
    pisos = {"FAM": E.json_repo(inputs, *FAM_PISO)["resultados"], "COLA": E.json_repo(inputs, *COLA_PISO)["resultados"]}
    return F, C, R, L, Mo, pisos


def _cid(pref, c, eje, cat):
    return f"{pref}-{c}-{eje}-{cat}"


def celdas_de(F, C):
    out = []
    for c, unidad in F.CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(F.ejes_de(unidad).items()):
            out += [("FAM", c, eje, cat) for cat in cats]
    for conds, ejes in ((C.COND_MUJ, C.EJES_MUJ), (C.COND_HOG, C.EJES_HOG)):
        for c in conds:
            for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes.items()):
                out += [("COLA", c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    F, C, _R, _L, _Mo, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(F, C)])


def lecturas(F, C):
    """[(clave, miembro, columnas, estructurales, renombre)] — qué se lee de cada miembro, fijado antes de abrir."""
    per = [CONYU_2023 if c == F.PER[OLA_CODIGOS]["conyu"] else c for c in F.columnas_per(OLA_CODIGOS)]
    h = F.HOG[OLA_CODIGOS]
    return [
        ("FAM-HOG", h["miembro"], F.columnas_hog(OLA_CODIGOS), {*h["llave"], h["fac"], h["est"], h["upm"]}, {}),
        ("FAM-PER", F.PER[OLA_CODIGOS]["miembro"], per, set(F.PER[OLA_CODIGOS]["llave"]),
         {CONYU_2023: F.PER[OLA_CODIGOS]["conyu"]}),
        ("COLA-MUJ", C.MIEMBROS["MUJ"], list(C.COLS_MUJ), {"fac_per", "est_dis", "upm_dis"}, {}),
        ("COLA-HOG", C.MIEMBROS["HOG"], list(C.COLS_HOG), {"llave_hog", "paren", "fac_viv", "est_dis", "upm_dis"}, {}),
        ("COLA-MIG", C.MIEMBROS["MIG"], list(C.COLS_MIG), {"llave_hog"}, {}),
    ]


def _faltantes(err, pedidas, estructurales, clave):
    """Columnas pedidas que el KeyError del lector declara ausentes; una estructural → PARO."""
    msg = str(err.args[0]) if err.args else ""
    try:
        dichas = {str(c).lower() for c in ast.literal_eval(msg[msg.rindex(": [") + 2:])}
    except (ValueError, SyntaxError) as e:
        raise G.ParoDeGuardia(f"{clave}: KeyError ilegible del lector: {msg}") from e
    faltan = [c for c in pedidas if c.lower() in dichas]
    duras = sorted(c for c in faltan if c in estructurales)
    if duras or not faltan:
        raise G.ParoDeGuardia(f"{clave}: columnas de llave/ponderador/diseño ausentes {duras or msg}: PARO")
    return faltan


def lee_payload_reservado(L, ruta, miembro, cols, estructurales, clave):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Devuelve (frame, faltantes)."""
    if "enadid23" not in os.path.basename(str(ruta)).lower():
        raise G.ParoDeGuardia(f"`{PAYLOAD}` no resuelve a la ola 2023: {ruta}")
    try:
        return L.lee_csv_zip(ruta, miembro, cols), []
    except KeyError as err:
        faltan = _faltantes(err, cols, estructurales, clave)
    df = L.lee_csv_zip(ruta, miembro, [c for c in cols if c not in faltan])
    for c in faltan:
        df[c] = ""
    return df, faltan


def _agrega(out, clave, y, w, grupos):
    for eje, g in grupos.items():
        for cat, r in G.proporcion_por_grupo(y, w, g).items():
            out[clave + (eje, cat)] = r["p"]


def _todos(n):
    return {"TOTAL": np.full(n, "TODOS", dtype=object)}


def mide_r(F, C, R, Mo, frames, faltan=None):
    """{(pref, conducta, eje, cat): p} con UNA variable de agrupación por llamada.

    `frames`: {"FAM-HOG", "FAM-PER", "COLA-MUJ", "COLA-HOG", "COLA-MIG"} ya renombrados a los nombres 2018.
    `faltan`: {clave: [columnas ausentes]} de `lee_payload_reservado`.
    """
    faltan = faltan or {}
    out = {}
    ola = OLA_CODIGOS
    # FAMILIA: hogares y residentes (prepara_* y conductas_* del contendiente, códigos 2018)
    fh, diag = F.prepara_hogar(ola, frames["FAM-HOG"], R)
    yh, eh = F.conductas_hogar(ola, fh, R)
    wh = fh["_w"].to_numpy(dtype=float)
    for c, y in yh.items():
        g = _todos(len(fh))
        g.update({e: np.asarray(eh[e][0], dtype=object) for e in F.EJES_HOG})
        _agrega(out, ("FAM", c), np.asarray(y, dtype=float), wh, g)
    fp = F.prepara_persona(ola, frames["FAM-PER"], fh, R, diag)
    yp, ep = F.conductas_persona(ola, fp, R)
    wp = fp["_w"].to_numpy(dtype=float)
    for c, y in yp.items():
        g = _todos(len(fp))
        g.update({e: np.asarray(ep[e][0], dtype=object) for e in F.EJES_PER})
        _agrega(out, ("FAM", c), np.asarray(y, dtype=float), wp, g)
    # COLA: mujeres 15-54 (TMUJER2) y jefaturas con/sin emigrante varón (TSDEM + TMIGRANTE)
    fm, _et, _n = Mo.prepara_diseno(frames["COLA-MUJ"], peso="fac_per", estrato="est_dis", upm="upm_dis")
    fm = C.derivadas_mujeres(fm, Mo)
    em = {e: np.asarray(Mo.eje_mapa(fm, col, mapa), dtype=object) for e, (col, mapa) in C.MAPAS_MUJ.items()}
    em["EDAD"] = np.asarray(Mo.eje_rango(fm, "edad_muj", C.EDADES), dtype=object)
    edad = Mo.num(fm["edad_muj"])
    um = (edad >= 15) & (edad <= 54)
    wm = fm["_w"].to_numpy(dtype=float)
    for c, regla in C.COND_MUJ.items():
        y = Mo.recodifica(fm, regla)
        y[~um] = np.nan
        g = _todos(len(fm))
        g.update({e: em[e] for e in C.EJES_MUJ})
        _agrega(out, ("COLA", c), y, wm, g)
    hog = frames["COLA-HOG"]
    jefes = hog[Mo.num(hog["paren"]) == 1].reset_index(drop=True)
    fj, _et, _n = Mo.prepara_diseno(jefes, peso="fac_viv", estrato="est_dis", upm="upm_dis")
    fj = C.derivadas_hogares(fj, frames["COLA-MIG"], Mo)
    sin_mig = any(c in faltan.get("COLA-MIG", ()) for c in DEPENDE_MIG)
    ej = {e: np.asarray(Mo.eje_mapa(fj, col, mapa), dtype=object) for e, (col, mapa) in C.MAPAS_HOG.items()}
    wj = fj["_w"].to_numpy(dtype=float)
    for c, regla in C.COND_HOG.items():
        y = Mo.recodifica(fj, regla)
        if sin_mig:
            y[:] = np.nan
        g = _todos(len(fj))
        g.update({e: ej[e] for e in C.EJES_HOG})
        _agrega(out, ("COLA", c), y, wj, g)
    return out


def filas(F, C, Mo, r, pisos):
    out = []
    for pref, c, eje, cat in celdas_de(F, C):
        if pref == "FAM":
            p = pisos["FAM"]
            puntua = c not in F.MENOS_DE_3_OLAS and (c, eje) not in APARTADAS
            lo = p.get(F.rid(c, OLA_CODIGOS, eje, cat, "ICC-LO")) if puntua else None
            hi = p.get(F.rid(c, OLA_CODIGOS, eje, cat, "ICC-HI")) if puntua else None
            punto = p.get(F.rid(c, OLA_CODIGOS, eje, cat, "P"))
            cong = FAM_CALC
        else:
            p = pisos["COLA"]
            lo = p.get(Mo.rid(C.P, c, OLA_CODIGOS, eje, cat, "IC-LO"))
            hi = p.get(Mo.rid(C.P, c, OLA_CODIGOS, eje, cat, "IC-HI"))
            punto = p.get(Mo.rid(C.P, c, OLA_CODIGOS, eje, cat, "P"))
            cong = COLA_CALC
        out.append({"id": _cid(pref, c, eje, cat), "conglomerado": cong, "lo": lo, "hi": hi, "punto": punto,
                    "r": r.get((pref, c, eje, cat))})
    return out


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    F, C, R, L, Mo, pisos = sellados(inputs)
    ruta = inputs[PAYLOAD]["ruta_absoluta"]
    frames, faltan = {}, {}
    for clave, miembro, cols, estructurales, renombre in lecturas(F, C):
        df, faltan[clave] = lee_payload_reservado(L, ruta, miembro, cols, estructurales, clave)
        frames[clave] = df.rename(columns=renombre)
    return E.salida(P, filas(F, C, Mo, mide_r(F, C, R, Mo, frames, faltan), pisos))
