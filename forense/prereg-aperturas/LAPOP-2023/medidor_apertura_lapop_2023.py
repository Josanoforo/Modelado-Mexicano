#!/usr/bin/env python3
"""Medidor de APERTURA de LAPOP AmericasBarometer México 2023 (reactivos de capital social) — ACTO
GEN2-APERTURAS-PREREGISTRADAS-1.

Spec humana: `APERTURA-LAPOP-2023-spec-v1_0.md`; contrato: `APERTURA-LAPOP-2023-spec.yaml`;
receta: `RECETA-APERTURA-LAPOP-2023.md`. NO SE HA CORRIDO: corre sólo en caja, en el commit de apertura que
mesa autorice.

Reserva POR ESTIMANDO, no por payload: el .dta de 2023 ya lo abrió CALC-LAPOP-PISOS-2023-0001 para otros
reactivos (b18, b21, pol1, eff1, eff2, d3, d4 + diseño); los reactivos de CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001
quedaron «2023 RESERVADA para estos reactivos (E.6)». Este medidor es el único código autorizado a leerlos.

R = Σw·y/Σw por conducta×eje×categoría en 2023, con la recodificación, el universo y los ejes del contendiente
(sus tablas, importadas por bytes con sha256 fijado); piso = última ola del contendiente con la conducta y P
TOTAL finito (2019 o 2006), intervalo = su IC de diseño IC-LO/IC-HI (sin serie: FIRMAS-15 T, no hay ICC).
Guardia E.6: auditoría AST de este archivo antes de leer un byte; `guardia_apertura.proporcion_por_grupo` es
el único agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "LAPOP-2023"
P = "RESULT-APERTURA-LAPOP-2023"
OLA = "2023"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001/medidor.py",
           "3478170747a8e0e00d6eb836be7bd23a602e2bcbee0c0f9d4271fb01b71fb015")
PISO = ("contendiente_resultados", "data/corrida0/CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001/resultados.json",
        "cc45f30179e78cbbc3a09c0c3b41b3d122170fc393d9be93385638d37baf850c")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAY = "mex_2023_lapop_americasbarometer_v1_0_w"
CONTENDIENTE = "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001"
# Diseño en 2023: el de la ola 2019 del contendiente (peso, estrato, UPM) y sus ejes.
PESO, ESTRATO, UPM = "wt", "estratopri", "upm"
OBLIGATORIAS = (PESO, ESTRATO, UPM, "q2")
EJES_COL = {"SEXO": "q1", "EDAD": "q2", "ESCOLARIDAD": "ed", "UR": "ur"}


def sellados(inputs=None):
    M = E.modulo("motor_pisos_confianza", E.bytes_repo(inputs, *MOTOR))
    L = E.modulo("m_lapop_capital_social_sellado", E.bytes_repo(inputs, *SELLADO))
    return {"M": M, "L": L, "res": E.json_repo(inputs, *PISO)["resultados"]}


def _fin(x):
    return isinstance(x, (int, float)) and x == x and abs(x) != float("inf")


def conductas(L):
    out = []
    for o in L.OLAS:
        out += [c for c in L.OLAS[o][3] if c not in out]
    return out


def ola_piso(S, c):
    """Última ola del contendiente con la conducta y P TOTAL finito en su resultados.json sellado; si ninguna,
    la última ola con la conducta (sus celdas quedan sin intervalo: no se puntúan)."""
    L, M = S["L"], S["M"]
    olas = [o for o in L.OLAS if c in L.OLAS[o][3]]
    con = [o for o in olas if _fin(S["res"].get(M.rid(L.P, c, o, "TOTAL", "TODOS", "P")))]
    return (con or olas)[-1]


def celdas_de(S):
    """[(conducta, ola_piso, eje, cat)] en orden determinista, derivado de las tablas y pisos sellados."""
    L, out = S["L"], []
    for c in conductas(L):
        piso = ola_piso(S, c)
        for eje, cats in [("TOTAL", ("TODOS",))] + list(L.ejes_de(piso).items()):
            out += [(c, piso, eje, cat) for cat in cats]
    return out


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def esquema_resultados():
    return E.esquema(P, [_cid(c, e, k) for c, _o, e, k in celdas_de(sellados())])


def columnas_pedidas(S):
    L = S["L"]
    cols = list(OBLIGATORIAS) + list(EJES_COL.values())
    cols += [L.OLAS[piso][3][c][1].lower() for c, piso in {c: ola_piso(S, c) for c in conductas(L)}.items()]
    return list(dict.fromkeys(cols))


def lee_payload_reservado(M, ruta, pedidas):
    """Única lectura de los reactivos reservados (la auditoría AST lo exige). Primero metadatos del .dta (nombres
    de columna = libro de códigos): si falta una columna de diseño obligatoria, PARO antes de leer una fila.
    Después, sólo las columnas pedidas que existen (el archivo es sólo México: no hay filtro de país)."""
    import pyreadstat

    _, meta = pyreadstat.read_dta(str(ruta), metadataonly=True)
    reales = {c.lower() for c in meta.column_names}
    faltan = [c for c in OBLIGATORIAS if c not in reales]
    if faltan:
        raise G.ParoDeGuardia(f"columnas de diseño ausentes en 2023: {faltan}")
    return M.lee(ruta, [c for c in pedidas if c in reales])


def mide_r(S, frame):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    M, L = S["M"], S["L"]
    faltan = [c for c in OBLIGATORIAS if c not in frame.columns]
    if faltan:
        raise G.ParoDeGuardia(f"columnas de diseño ausentes: {faltan}")
    f, _etiqueta, _n = M.prepara_diseno(frame, peso=PESO, estrato=ESTRATO, upm=UPM)
    w = f["_w"].to_numpy()
    nada = np.full(len(f), None, dtype=object)
    ejes = {"SEXO": M.eje_mapa(f, "q1", {"HOMBRE": [1], "MUJER": [2]}) if "q1" in f.columns else nada,
            "EDAD": M.edad(f, "q2"),
            "ESCOLARIDAD": M.eje_rango(f, "ed", L.ESCOL) if "ed" in f.columns else nada,
            "UR": M.eje_mapa(f, "ur", {"URBANO": [1], "RURAL": [2]}) if "ur" in f.columns else nada}
    universo = M.num(f["q2"]) >= 18
    out = {}
    for c in conductas(L):
        piso = ola_piso(S, c)
        regla = L.OLAS[piso][3][c]
        if regla[1].lower() not in f.columns:
            continue
        y = np.asarray(M.recodifica(f, regla), dtype=float)
        y[~universo] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: ejes[e] for e in L.ejes_de(piso)})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(S, r):
    M, L, res, out = S["M"], S["L"], S["res"], []
    for c, piso, eje, cat in celdas_de(S):
        q = lambda k: res.get(M.rid(L.P, c, piso, eje, cat, k))  # noqa: E731
        out.append({"id": _cid(c, eje, cat), "conglomerado": c,
                    "lo": q("IC-LO"), "hi": q("IC-HI"), "punto": q("P"), "r": r.get((c, eje, cat))})
    return out


def _variables():
    S = sellados()
    out = []
    for c in conductas(S["L"]):
        piso = ola_piso(S, c)
        t, col, uno, cero = S["L"].OLAS[piso][3][c]
        out.append({"nombre": c, "definicion": f"{t}({col}: 1={list(uno)}, 0={list(cero)}; resto fuera); códigos "
                                               f"de la ola del piso {piso} de {CONTENDIENTE}"})
    return out


CONTRATO = {
    "x": X, "programa": "LAPOP", "ola": "2023", "unidad": "PERSONA",
    "contendientes": [CONTENDIENTE],
    "payloads": [(PAY, "LAPOP AmericasBarometer México 2023 (.dta) -- reactivos de CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001 "
                       "RESERVADOS por su spec sellada (reserva por estimando); sólo este medidor los lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: OLAS, BASE, SOLO_*, ESCOL, CATS, ejes_de, P"),
             (PISO[0], PISO[1], "pisos 2004/2006/2019 sellados: P, IC-LO, IC-HI por celda"),
             (MOTOR[0], MOTOR[1], "lee, num, recodifica, eje_mapa, eje_rango, edad, prepara_diseno, rid"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas de LAPOP México 2023 con wt finito > 0, estratopri y upm no vacíos (prepara_diseno del "
                "contendiente, diseño de su ola 2019) y edad q2 >= 18",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD, UR); nunca cruces (guardia E.6)",
    "ponderador": "wt",
    "transformacion": "Recodificación bin del contendiente con los códigos de la ola del piso (2019 o 2006; spec §1); "
                      "columna ausente en 2023 -> NO-ESTIMABLE (sin recodificación ad hoc)",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en LAPOP México 2023; cobertura de R en el IC de diseño "
                 "sellado de la ola del piso del contendiente (IC-LO/IC-HI; sin ICC por FIRMAS-15 T)",
    "variables": _variables(),
    "dependencias": ["numpy", "pandas", "pyreadstat"],
}


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAY} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S = sellados(inputs)
    frame = lee_payload_reservado(S["M"], inputs[PAY]["ruta_absoluta"], columnas_pedidas(S))
    return E.salida(P, filas(S, mide_r(S, frame)))
