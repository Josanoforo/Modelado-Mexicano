#!/usr/bin/env python3
"""Medidor de APERTURA de ENPECYT 2017 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENPECYT-2017-spec-v1_0.md`; contrato: `APERTURA-ENPECYT-2017-spec.yaml`;
receta: `RECETA-APERTURA-ENPECYT-2017.md`. NO SE HA CORRIDO sobre ENPECYT 2017: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada (`FAC`) de personas 18+ de cada conducta de `CALC-ENPECYT-CONOC-PISOS-0001`
en ENPECYT 2017, por categoría de UN eje a la vez, con la recodificación del medidor sellado (input
`origen: repo`, sha fijado) y los códigos/campos de la ola del piso 2015 (`ITEMS["2015"]`, ciudad `CD_A`).
Adjudica la cobertura del contendiente: piso 2015 con IC calibrado de persistencia 2011-2015
(ICC-LO/ICC-HI de su `resultados.json` sellado). RESPETA-10-INVENTOR sólo tiene ola 2015 (sin ICC): su
R se reporta y no se puntúa; tampoco se puntúa la celda TOTAL (marginal 2017 ya publicado y citado por los
reports; spec §0). Guardia E.6: auditoría AST de este archivo antes de leer un byte;
`guardia_apertura.proporcion_por_grupo` es el único agregador.

Columna ausente de reactivo o eje → vacío → NO-ESTIMABLE en las celdas que la usan; columna ausente de
ciudad/llave/FAC/EST_DIS/UPM_DIS, o miembro `enpecyt2017_<tabla>.dbf` ausente → ParoDeGuardia.
"""
from __future__ import annotations

import ast
import os
import zipfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENPECYT-2017"
P = "RESULT-APERTURA-ENPECYT-2017"
CALC = "CALC-ENPECYT-CONOC-PISOS-0001"
OLA = "2017"
OLA_CODIGOS = "2015"  # códigos, campos y nombres fijados sobre la ola del piso
# Marginales nacionales 2017 ya publicados y citados por los reports (spec del contendiente §5): la celda
# TOTAL se aparta de la primaria sin abrir (E.6: lo apartado se declara); su R se reporta, no se puntúa.
EJES_APARTADOS = frozenset({"TOTAL"})


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", f"data/corrida0/{CALC}/medidor.py",
           "8e3b450e9ad5da51c97641bb1125fe388161e75a57932ee51cd3e9ec619ac7e5")
PISO = ("contendiente_resultados", f"data/corrida0/{CALC}/resultados.json",
        "233db622abf9af279c94021820a3535cd004cc359648c7093c0432a046453d67")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "enpecyt2017_bd_dbf_zip"

CONTRATO = {
    "x": X, "programa": "ENPECYT", "ola": OLA, "unidad": "PERSONA",
    "contendientes": [CALC],
    "payloads": [(PAYLOAD, "ENPECYT 2017 base DBF (tablas CB1, CB2, CS) -- ola RESERVADA; sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: lee_dbf/miembro/campos_de/prepara/conducta_y/rid/rid_p"),
             (PISO[0], PISO[1], "piso 2015 sellado: P, ICC-LO, ICC-HI por celda"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Persona elegida de 18+ (una fila de CB1) de ENPECYT 2017, áreas urbanas 100 000+; unión CB1-CB2-CS por "
                "CD_A+PER+CON+V_SEL+N_HOG+N_REN con llaves únicas; FAC > 0; EST_DIS y UPM_DIS no vacíos (prepara() del contendiente)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD); nunca cruces (guardia E.6)",
    "ponderador": "FAC (CB1)",
    "transformacion": "Recodificación del contendiente (spec ENPECYT-CONOC-PISOS §2) con los campos de 2015 (ITEMS['2015']); "
                      "campo ausente o con texto/códigos distintos en el FD/cuestionario 2017 -> NO-ESTIMABLE; "
                      "ciudad/llave/FAC/diseño ausente -> PARO",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENPECYT 2017; cobertura de R en el ICC (persistencia) del piso 2015",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec ENPECYT-CONOC-PISOS §0/§2), campos 2015"}
                  for c in ("INTERES-AL-MENOS-MODERADO", "INTERES-GRANDE-O-MAS", "GOB-INVERTIR-ACUERDO",
                            "GOB-INVERTIR-ACUERDO-SIN-NS", "FE-CIENCIA-ACUERDO", "FE-CIENCIA-ACUERDO-SIN-NS",
                            "RESPETA-10-BOMBERO", "RESPETA-10-ENFERMERA", "RESPETA-10-INVESTIGADOR",
                            "RESPETA-10-INVENTOR")],
}


def sellados(inputs=None):
    M = E.modulo("m_enpecyt_pisos_sellado", E.bytes_repo(inputs, *SELLADO))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return M, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(M):
    return [(c, eje, cat) for c in M.CONDUCTAS for eje, cat in M._todas()]


def esquema_resultados():
    M, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M)])


def _estructurales(M):
    llave = {M.CIUDAD[OLA_CODIGOS], *M.LLAVE}
    return {"cb1": llave | {"FAC"}, "cb2": llave, "cs": llave | {"EST_DIS", "UPM_DIS"}}


def _faltantes(err, pedidas, estructurales, tabla):
    """Campos pedidos que el KeyError del lector declara ausentes; uno estructural → PARO."""
    msg = str(err.args[0]) if err.args else ""
    try:
        dichas = {str(c).upper() for c in ast.literal_eval(msg[msg.rindex(": [") + 2:])}
    except (ValueError, SyntaxError) as e:
        raise G.ParoDeGuardia(f"{tabla}: KeyError ilegible del lector: {msg}") from e
    faltan = [c for c in pedidas if c.upper() in dichas]
    duras = sorted(c for c in faltan if c in estructurales)
    if duras or not faltan:
        raise G.ParoDeGuardia(f"{tabla}: campos de ciudad/llave/FAC/diseño ausentes {duras or msg}: PARO")
    return faltan


def lee_payload_reservado(M, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Devuelve ({tabla: frame}, faltantes)."""
    if f"enpecyt{OLA}" not in os.path.basename(str(ruta)).lower():
        raise G.ParoDeGuardia(f"`{PAYLOAD}` no resuelve a la ola {OLA}: {ruta}")
    tablas, faltan = {}, {}
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        for t, cols in M.campos_de(OLA_CODIGOS).items():
            datos = z.read(M.miembro(nombres, OLA, t))
            cols = list(dict.fromkeys(cols))
            try:
                tablas[t], faltan[t] = M.lee_dbf(datos, cols), []
                continue
            except KeyError as err:
                faltan[t] = _faltantes(err, cols, _estructurales(M)[t], t)
            df = M.lee_dbf(datos, [c for c in cols if c not in faltan[t]])
            for c in faltan[t]:
                df[c] = ""
            tablas[t] = df
    return tablas, faltan


def mide_r(M, tablas):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    f, ejes, _diag = M.prepara(tablas, OLA_CODIGOS)
    w = f["_w"].to_numpy(dtype=float)
    out = {}
    for c in M.CONDUCTAS:
        y = np.asarray(M.conducta_y(c, f, OLA_CODIGOS), dtype=float)
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e][0], dtype=object) for e in M.EJES})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(M, r, piso):
    out = []
    for c, eje, cat in celdas_de(M):
        con_icc = c not in M.SOLO_2015 and eje not in EJES_APARTADOS
        out.append({"id": _cid(c, eje, cat), "conglomerado": c,
                    "lo": piso.get(M.rid_p(c, eje, cat, "ICC-LO")) if con_icc else None,
                    "hi": piso.get(M.rid_p(c, eje, cat, "ICC-HI")) if con_icc else None,
                    "punto": piso.get(M.rid(c, OLA_CODIGOS, eje, cat, "P")),
                    "r": r.get((c, eje, cat))})
    return out


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, piso = sellados(inputs)
    tablas, _faltan = lee_payload_reservado(M, inputs[PAYLOAD]["ruta_absoluta"])
    return E.salida(P, filas(M, mide_r(M, tablas), piso))
