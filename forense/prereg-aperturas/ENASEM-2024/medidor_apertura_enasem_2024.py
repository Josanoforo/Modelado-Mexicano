#!/usr/bin/env python3
"""Medidor de APERTURA de ENASEM 2024 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENASEM-2024-spec-v1_0.md`; contrato: `APERTURA-ENASEM-2024-spec.yaml`;
receta: `RECETA-APERTURA-ENASEM-2024.md`. NO SE HA CORRIDO sobre ENASEM 2024: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada (FACTORI_24) de cada conducta de `CALC-ENASEM-ESCOLARIDAD-2021-0001` en
ENASEM 2024, persona entrevistada de 50+, por categoría de UN eje a la vez (TOTAL, SEXO, EDAD), con la
recodificación del medidor sellado (CONDUCTAS, MAPAS, EDADES; importado por bytes con sha fijado) y las
funciones del motor común (`prepara_diseno`, `recodifica`, `eje_mapa`, `eje_rango`). Columnas de 2021 con
sufijo de ronda `_21` se leen como `_24` en 2024 (spec §0, §5). Adjudica la cobertura del contendiente
(piso 2021 con IC95 de DISEÑO IC-LO/IC-HI de su `resultados.json` sellado; una sola ola abierta, sin IC
de persistencia). Guardia E.6: auditoría AST de este archivo antes de leer un byte del payload;
`guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import io
import os
import zipfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENASEM-2024"
P = "RESULT-APERTURA-ENASEM-2024"
OLA = "2024"
OLA_PISO = "2021"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENASEM-ESCOLARIDAD-2021-0001/medidor.py",
           "e99494b009dba74ed0fd79bf80e921f480be8f9a969a452f2817ec43a6b21098")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENASEM-ESCOLARIDAD-2021-0001/resultados.json",
        "f7ab868cba803c459ef8b73cb50345839e973f33e50e1efe92b6c2f8085a0a33")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "enasem2024_bd_csv_zip"
# Miembro de la sección A-C-D-E-PC-F-H-I de 2024: nombre tomado del inventario de cabeceras
# `data/inventario-reactivos-v1_2.tsv` (nombres de columna, sin valores); se compara sin mayúsculas.
MIEMBRO = "tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv"

CONTRATO = {
    "x": X, "programa": "ENASEM", "ola": "2024", "unidad": "PERSONA",
    "contendientes": ["CALC-ENASEM-ESCOLARIDAD-2021-0001"],
    "payloads": [(PAYLOAD, "ENASEM 2024 microdatos CSV (miembro tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv) -- ola "
                           "RESERVADA; sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: CONDUCTAS, MAPAS, EDADES, columnas y diseño"),
             (PISO[0], PISO[1], "piso 2021 sellado: P, IC-LO, IC-HI (IC95 de diseño) por celda"),
             (MOTOR[0], MOTOR[1], "prepara_diseno, recodifica, eje_mapa, eje_rango, num, rid del motor común"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Persona entrevistada de ENASEM 2024 con 50 <= AGE_24 <= 120 (888/999 fuera); FACTORI_24 > 0, "
                "EST_DIS_24 y UPM_DIS_24 no vacíos (prepara_diseno del motor)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD); nunca cruces (guardia E.6)",
    "ponderador": "FACTORI_24 (factor individual 2024; homólogo de FACTORI_21 del piso)",
    "transformacion": "Recodificación del contendiente (spec COLA-ENASEM-ESCOLARIDAD §2) sobre YRSCHOOL; sufijo de "
                      "ronda _21 -> _24 en sexo, edad, factor, estrato y UPM; columna ausente -> NO-ESTIMABLE",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENASEM 2024; cobertura de R en el IC95 de diseño del piso 2021",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec COLA-ENASEM-ESCOLARIDAD §2): YRSCHOOL"}
                  for c in ("SIN-ESCOLARIDAD", "SEIS-ANOS-O-MENOS")]
               + [{"nombre": v, "definicion": d} for v, d in (
                   ("SEX_24", "Sexo 2024 (eje SEXO, 1 HOMBRE / 2 MUJER)"),
                   ("AGE_24", "Edad 2024 (universo 50-120 y eje EDAD 50-59/60-69/70-79/80-MAS)"),
                   ("FACTORI_24", "factor individual 2024 (ponderador)"),
                   ("EST_DIS_24", "estrato de diseño (validez de registro)"),
                   ("UPM_DIS_24", "UPM de diseño (validez de registro)"))],
}


def c24(col: str) -> str:
    """Columna 2021 -> 2024: sólo el sufijo de ronda `_21` cambia (YRSCHOOL no lo lleva)."""
    return col[:-3] + "_24" if col.upper().endswith("_21") else col


def sellados(inputs=None):
    S = E.modulo("m_enasem_escolaridad_sellado", E.bytes_repo(inputs, *SELLADO))
    M = E.modulo("motor_pisos_confianza", E.bytes_repo(inputs, *MOTOR))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, M, piso


def columnas(S):
    return [c24(c) for c in S.COLS_CRUDAS]


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    out = []
    for c in S.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(S.EJES_CATS.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    S, _M, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)],
                     unidad_r="proporción ponderada de personas 50+ en ENASEM 2024")


def lee_payload_reservado(ruta, cols, miembro=MIEMBRO):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Devuelve (frame de texto con las
    columnas en minúsculas, columnas ausentes). Una columna ausente entra vacía (spec §5: NO-ESTIMABLE)."""
    with zipfile.ZipFile(ruta) as z:
        cand = [n for n in z.namelist() if n.rsplit("/", 1)[-1].lower() == miembro.lower()]
        if len(cand) != 1:
            raise G.ParoDeGuardia(f"{miembro}: se esperaba 1 miembro, hay {len(cand)}")
        raw = z.read(cand[0])
    try:
        texto = raw.decode("utf-8")
    except UnicodeDecodeError:
        texto = raw.decode("latin-1")
    quiero = {c.lower() for c in cols}
    df = pd.read_csv(io.StringIO(texto), usecols=lambda c: c.strip().lower() in quiero, dtype=str,
                     keep_default_na=False)
    df.columns = [c.strip().lower() for c in df.columns]
    faltan = sorted(quiero - set(df.columns))
    for c in faltan:
        df[c] = ""
    return df, faltan


def mide_r(S, M, frame, faltan=()):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    faltan = {c.lower() for c in faltan}
    f, _et, _n = M.prepara_diseno(frame, peso=c24(S.PESO), estrato=c24(S.ESTRATO), upm=c24(S.UPM))
    w = f["_w"].to_numpy()
    edad = np.asarray(M.num(f[c24(S.EDAD_COL).lower()]), dtype=float)
    universo = (edad >= 50) & (edad <= 120)  # como mide() del sellado: 888/999 fuera
    grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
    for eje, (col, mapa) in S.MAPAS.items():
        grupos[eje] = M.eje_mapa(f, c24(col), mapa)
    grupos["EDAD"] = M.eje_rango(f, c24(S.EDAD_COL), S.EDADES)
    out = {}
    for c, regla in S.CONDUCTAS.items():
        col = c24(regla[1])
        if col.lower() in faltan:
            continue
        y = np.asarray(M.recodifica(f, (regla[0], col) + tuple(regla[2:])), dtype=float)
        y[~universo] = np.nan
        for eje in ["TOTAL"] + list(S.EJES_CATS):
            for cat, r in G.proporcion_por_grupo(y, w, grupos[eje]).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(S, M, r, piso):
    q = lambda c, eje, cat, k: piso.get(M.rid(S.P, c, OLA_PISO, eje, cat, k))  # noqa: E731
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": q(c, eje, cat, "IC-LO"), "hi": q(c, eje, cat, "IC-HI"), "punto": q(c, eje, cat, "P"),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(S)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S, M, piso = sellados(inputs)
    frame, faltan = lee_payload_reservado(inputs[PAYLOAD]["ruta_absoluta"], columnas(S))
    return E.salida(P, filas(S, M, mide_r(S, M, frame, faltan), piso))
