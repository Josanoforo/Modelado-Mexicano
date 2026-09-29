#!/usr/bin/env python3
"""Medidor de APERTURA de ENSU 2026 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENSU-2026-spec-v1_0.md`; contrato: `APERTURA-ENSU-2026-spec.yaml`;
receta: `RECETA-APERTURA-ENSU-2026.md`. NO SE HA CORRIDO sobre ENSU 2026: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada de cada conducta de los contendientes `CALC-ENSU-PISOS-0001` /
`CALC-ENSU-SERIE-0001` en el trimestre siguiente al último abierto de su cadencia (2025T4 → 2026T1
para las 14 trimestrales; 2025T4 → 2026T2 para C15, semestral T2/T4), por categoría de UN eje a la
vez, con el marco y la recodificación del medidor sellado (bytes idénticos en los dos CALC, sha
fijado). Contendiente por celda: el piso 2025T4 de PISOS con el IC calibrado de persistencia que la
regla sellada de SERIE aplica a «piso t−1 cubre a t» (spec SERIE §6; `tools/series/dictamen.py`):
expit(logit p ± z·√(ee² + τ²)), ee del IC de diseño 2025T4, τ² sellado en SERIE por eje y cadencia
(`tau2_para`: eje sin τ² propio → media de los ejes de su cadencia). Guardia E.6: auditoría AST de
este archivo antes de leer un byte del payload; `guardia_apertura.proporcion_por_grupo` es el único
agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENSU-2026"
P = "RESULT-APERTURA-ENSU-2026"
OLA_PISO = "2025T4"
OLA_R = {"T": "2026T1", "S": "2026T2"}          # cadencia de la conducta -> trimestre R


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENSU-PISOS-0001/medidor.py",
           "18026ad104df64a98d25ac1242be1a71899c05b87f3db789984cb8cac934b43a")
PISO = ("contendiente_pisos_resultados", "data/corrida0/CALC-ENSU-PISOS-0001/resultados.json",
        "5b3ae6f7cf40297775e2facb86af61e14d37ec74eebb98ab5a7fefd3b71531a9")
SERIE = ("contendiente_serie_resultados", "data/corrida0/CALC-ENSU-SERIE-0001/resultados.json",
         "cd6de0f16bbda4d017b3de498d3b4aec080ed79d4915d6074507f0ab55b1af70")
RECETA = ("receta_pisos", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
DICTAMEN = ("dictamen_series", "tools/series/dictamen.py",
            "b2b846cacca8dff43a9f662a31b3a0a53afd101462ea3d34d7606405a52dd29f")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "cc1_inegi_ensu_2026__ensu_bd_2026_csv"
PREF_PISO = "RESULT-ENSU-PISOS"
PREF_SERIE = "RESULT-ENSU-SERIE"
COL_EJE = {"SEXO": "_sexo", "EDAD": "_edad", "ENT": "_ent", "CIUDAD": "_cd"}
DISENO = ("_w", "_est", "_upm", "_cd", "_ent", "_sexo", "_edad")

CONTRATO = {
    "x": X, "programa": "ENSU", "ola": "2026", "unidad": "PERSONA",
    "contendientes": ["CALC-ENSU-PISOS-0001", "CALC-ENSU-SERIE-0001"],
    "payloads": [(PAYLOAD, "ENSU 2026 base de datos (marzo y junio: 2026T1, 2026T2) -- ola RESERVADA; sólo "
                           "este medidor la lee; el FD cc1_inegi_ensu_2026__ensu_fd_2026_pdf es documentación, no input")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado de PISOS y SERIE (bytes idénticos): tablas/marco/y_de/celdas_ola"),
             (PISO[0], PISO[1], "piso 2025T4 sellado: P, IC-LO, IC-HI por celda (conducta × eje × categoría)"),
             (SERIE[0], SERIE[1], "τ² de persistencia sellado por eje y cadencia (RESULT-ENSU-DICTAMEN-TAU2-*)"),
             (RECETA[0], RECETA[1], "num e ic_calibrado de la receta de pisos"),
             (DICTAMEN[0], DICTAMEN[1], "tau2_para: regla sellada de SERIE para el eje sin τ² propio"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Persona seleccionada de 18+ de la tabla CB de ENSU 2026T1 (C01-C14) y 2026T2 (C15), FAC_SEL > 0, "
                "EST_DIS y UPM_DIS no vacíos (marco() del contendiente, era 2021T2+); universo de cada conducta en "
                "forense/analisis/seguridad-ensu/lista-cerrada-P1.md §3",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ENT, CIUDAD); nunca cruces (guardia E.6); de 2026T2 sólo se "
               "agrega C15-CORRUPCION-POLICIA",
    "ponderador": "FAC_SEL",
    "transformacion": "Recodificación del contendiente (CONDUCTAS/FILTRO del medidor sellado, lista-cerrada-P1 §3); "
                      "columna ausente en el catálogo 2026 -> NO-ESTIMABLE (R None), sin recodificación ad hoc",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENSU 2026 (trimestre siguiente de su cadencia); cobertura "
                 "de R en el IC calibrado de persistencia del piso 2025T4 (regla sellada de CALC-ENSU-SERIE-0001 §6)",
    "variables": [{"nombre": c, "definicion": f"conducta del contendiente (lista-cerrada-P1 §3), R en {OLA_R[cad]}"}
                  for c, cad in (("C01-INSEG-CIUDAD", "T"), ("C02-INSEG-CALLE", "T"), ("C03-INSEG-CAJERO", "T"),
                                 ("C04-INSEG-TRANSPORTE", "T"), ("C05-EXPECT-EMPEORA", "T"),
                                 ("C06-TESTIGO-ROBOS", "T"), ("C07-TESTIGO-PANDILLAS", "T"),
                                 ("C08-TESTIGO-DISPAROS", "T"), ("C09-HABITO-OBJETOS-VALOR", "T"),
                                 ("C10-HABITO-CAMINAR-NOCHE", "T"), ("C11-HABITO-VISITAR", "T"),
                                 ("C12-HABITO-MENORES", "T"), ("C13-POLICIA-MUN-CONFIANZA", "T"),
                                 ("C14-POLICIA-MUN-EFECTIVA", "T"), ("C15-CORRUPCION-POLICIA", "S"))],
}


def sellados(inputs=None):
    M = E.modulo("m_ensu_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_ensu", E.bytes_repo(inputs, *RECETA))
    D = E.modulo("dictamen_series_ensu", E.bytes_repo(inputs, *DICTAMEN))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    serie = E.json_repo(inputs, *SERIE)["resultados"]
    return M, R, D, piso, serie


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def cadencia(M, c):
    return next(k[5] for k in M.CONDUCTAS if k[0] == c)


def celdas_de(M, piso):
    """Celdas del contendiente: las de `celdas_ola('pisos', c, 2025T4)` con P sellado en 2025T4."""
    out = []
    for c in M.NOMBRES:
        for eje, cats in M.celdas_ola("pisos", c, OLA_PISO):
            out += [(c, eje, cat) for cat in cats
                    if M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "P") in piso]
    return out


def esquema_resultados():
    M, _R, _D, piso, _s = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M, piso)])


def lee_payload_reservado(M, R, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige): {trimestre: marco por persona}.

    Sólo 2026T1 y 2026T2; de 2026T2 se conservan diseño y las columnas de C15 (BP3_5, BP3_6)."""
    with open(ruta, "rb") as fh:
        tabs = M.tablas(fh.read())
    out = {}
    for ola in sorted(set(OLA_R.values())):
        t = tabs.get(ola) or {}
        if "cb" not in t:
            raise G.ParoDeGuardia(f"{ola}: tabla CB ausente en el payload (receta paso 3)")
        f, _diag = M.marco(ola, *t["cb"], None, None, R)
        if ola == OLA_R["S"]:
            quedan = [c for c in M.CONDUCTAS if c[5] == "S"]
            cols = list(DISENO) + [c[1] for c in quedan] + [v for v, _ in M.FILTRO.values()]
            f = f[[c for c in cols if c in f.columns]]
        out[ola] = f
    return out


def mide_r(M, R, marcos):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    out = {}
    for c in M.NOMBRES:
        ola = OLA_R[cadencia(M, c)]
        f = marcos[ola]
        y = np.asarray(M.y_de(c, f, ola), dtype=float)
        w = f["_w"].to_numpy(dtype=float)
        for eje, _cats in M.celdas_ola("pisos", c, OLA_PISO):
            g = (np.full(len(f), "TODOS", dtype=object) if eje == "TOTAL"
                 else f[COL_EJE[eje]].to_numpy(dtype=object))
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def tau_de(serie, cad):
    nom = {"T": "TRIMESTRAL", "S": "SEMESTRAL"}[cad]
    tau = {}
    for eje in ("TOTAL", "SEXO", "EDAD", "CIUDAD"):
        v = serie.get(f"RESULT-ENSU-DICTAMEN-TAU2-{nom}-{eje}")
        if v is not None:
            tau[eje] = float(v)
    return tau


def filas(M, R, D, r, piso, serie):
    taus = {cad: tau_de(serie, cad) for cad in OLA_R}
    out = []
    for c, eje, cat in celdas_de(M, piso):
        q = {k: piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, k)) for k in ("P", "IC-LO", "IC-HI")}
        t2 = D.tau2_para(eje, taus[cadencia(M, c)])
        lo, hi = R.ic_calibrado(q["P"], q["IC-LO"], q["IC-HI"], t2)
        out.append({"id": _cid(c, eje, cat), "conglomerado": c, "lo": lo, "hi": hi,
                    "punto": q["P"], "r": r.get((c, eje, cat))})
    return out


def control_cruzado(M, piso, serie):
    """Spec SERIE §8.2: toda celda 2025T4 común PISOS/SERIE es idéntica; si no, PARO (contendiente mal leído)."""
    for c in M.NOMBRES:
        for eje, cats in M.celdas_ola("serie", c, OLA_PISO):
            for cat in cats:
                for k in ("P", "IC-LO", "IC-HI"):
                    a = piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, k))
                    b = serie.get(M.rid(PREF_SERIE, c, OLA_PISO, eje, cat, k))
                    if a != b:
                        raise G.ParoDeGuardia(f"control cruzado PISOS/SERIE discordante: {c}-{eje}-{cat}-{k}")


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, R, D, piso, serie = sellados(inputs)
    control_cruzado(M, piso, serie)
    marcos = lee_payload_reservado(M, R, inputs[PAYLOAD]["ruta_absoluta"])
    return E.salida(P, filas(M, R, D, mide_r(M, R, marcos), piso, serie))
