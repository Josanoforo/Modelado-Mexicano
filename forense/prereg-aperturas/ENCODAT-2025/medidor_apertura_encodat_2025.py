#!/usr/bin/env python3
"""Medidor de APERTURA de ENCODAT 2025 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Spec humana: `APERTURA-ENCODAT-2025-spec-v1_0.md`; contrato: `APERTURA-ENCODAT-2025-spec.yaml`;
receta: `RECETA-APERTURA-ENCODAT-2025.md`. NO SE HA CORRIDO sobre ENCODAT 2025: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada de cada conducta de `CALC-ENCODAT-PISOS-SUSTANCIAS-0001` en ENCODAT 2025,
por categoría de UN eje a la vez, con la recodificación del medidor sellado (input `origen: repo`, sha
fijado); adjudica la cobertura del contendiente (piso 2016-17 con su IC de diseño: una sola ola abierta,
sin IC de persistencia). Guardia E.6 idéntica a ENSANUT-2025.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENCODAT-2025"
P = "RESULT-APERTURA-ENCODAT-2025"
OLA_PISO = "2016"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENCODAT-PISOS-SUSTANCIAS-0001/medidor.py",
           "d2123bfb393dba0d770824d04a7ef66118544f6502d9347197b1e292cb882b9b")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENCODAT-PISOS-SUSTANCIAS-0001/resultados.json",
        "a905034448cd3631b5b541c8ebee0e57cff5aa826ef8d859da37fb7dfe54389d")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOADS = {
    "IND": "encodat_2025__encodat_2025_adolescentes_adultos_stata_stata_zip",
    "HOG": "encodat_2025__encodat_2025_hogar_stata_stata_zip",
}
COLS = {"IND": "COLS_IND", "HOG": "COLS_HOG"}

CONTRATO = {
    "x": X, "programa": "ENCODAT", "ola": "2025", "unidad": "PERSONA",
    "contendientes": ["CALC-ENCODAT-PISOS-SUSTANCIAS-0001"],
    "payloads": [(pid, f"ENCODAT 2025 {a} -- ola RESERVADA; sólo este medidor la lee") for a, pid in PAYLOADS.items()],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: prepara/conducta_y/EJES/CONDUCTAS"),
             (PISO[0], PISO[1], "piso 2016-17 sellado: P, IC-LO, IC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_dta y num de la receta de pisos"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas de 12 a 65 años de ENCODAT 2025 (adolescentes_adultos unido a hogar por los 20 primeros "
                "caracteres de id_pers); ponde_ss > 0 con est_var y code_upm no vacíos (prepara() del contendiente)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESTRATO, ESCOLARIDAD 18+); nunca cruces (guardia E.6)",
    "ponderador": "ponde_ss",
    "transformacion": "Recodificación del contendiente (spec SALUD-ENCODAT-PISOS); columna ausente o con "
                      "texto/códigos distintos en el catálogo 2025 -> NO-ESTIMABLE",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENCODAT 2025; cobertura de R en el IC de diseño del piso 2016-17",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec SALUD-ENCODAT-PISOS)"}
                  for c in ("ALCOHOL-12M", "ALCOHOL-30D", "ALCOHOL-EXCESIVO-12M", "FUMA-ACTUAL",
                            "CIGARRO-ELECTRONICO-ALGUNA-VEZ", "DROGA-ILEGAL-ALGUNA-VEZ", "MARIGUANA-ALGUNA-VEZ",
                            "DROGA-MEDICA-SIN-RECETA-ALGUNA-VEZ", "OPIACEOS-SIN-RECETA-ALGUNA-VEZ",
                            "CONSULTO-PROFESIONAL-POR-CONSUMO")],
}


def sellados(inputs=None):
    M = E.modulo("m_encodat_pisos_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud", E.bytes_repo(inputs, *RECETA))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return M, R, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(M):
    return [(c, eje, cat) for c in M.CONDUCTAS
            for eje, cats in [("TOTAL", ("TODOS",))] + list(M.EJES.items()) for cat in cats]


def esquema_resultados():
    M, _R, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M)])


def lee_payload_reservado(R, M, arch, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige)."""
    return R.lee_dta(ruta, getattr(M, COLS[arch]), encoding="UTF-8")


def mide_r(M, R, frames):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    f, ejes, _diag, uni = M.prepara(frames["IND"], frames["HOG"], R)
    w = f["_w"].to_numpy()
    out = {}
    for c in M.CONDUCTAS:
        y = np.asarray(M.conducta_y(c, f, R.num), dtype=float)
        y[~np.asarray(uni)] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(lab, dtype=object) for e, (lab, _cats) in ejes.items()})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(c, eje, cat, "IC-LO")),
             "hi": piso.get(M.rid(c, eje, cat, "IC-HI")),
             "punto": piso.get(M.rid(c, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(M)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, R, piso = sellados(inputs)
    frames = {a: lee_payload_reservado(R, M, a, inputs[pid]["ruta_absoluta"]) for a, pid in PAYLOADS.items()}
    return E.salida(P, filas(M, mide_r(M, R, frames), piso))
