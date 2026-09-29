#!/usr/bin/env python3
"""Medidor de APERTURA de EMAT 2024 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-EMAT-2024-spec-v1_0.md`; contrato: `APERTURA-EMAT-2024-spec.yaml`;
receta: `RECETA-APERTURA-EMAT-2024.md`. NO SE HA CORRIDO sobre EMAT 2024: corre sólo en caja, en el
commit de apertura que mesa autorice.

EMAT es REGISTRO ADMINISTRATIVO: unidad MATRIMONIO REGISTRADO (conductas M-*) y CONTRAYENTE (conductas
C-*: cada matrimonio aporta dos), conteo completo, sin diseño ni ponderador (w = 1). Al abrir: R =
proporción exacta de cada conducta de `CALC-EMAT-PAREJA-PISOS-0001` en el año de registro 2024, por
categoría de UN eje a la vez, con la recodificación del medidor sellado (`matrimonios`, `contrayentes`,
`miembro_ola`, `lee_dbf`; importado por bytes con sha fijado). C-EDAD-MEDIA queda fuera (media en años sin
IC en el contendiente: spec §1). Adjudica la cobertura del contendiente (piso 2023 con IC calibrado de
persistencia ICC-LO/ICC-HI de su `resultados.json` sellado). Guardia E.6: auditoría AST de este archivo
antes de leer un byte del payload; `guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os
import zipfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "EMAT-2024"
P = "RESULT-APERTURA-EMAT-2024"
OLA = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-EMAT-PAREJA-PISOS-0001/medidor.py",
           "39e21cd28db9a9a2e6b3e9e5d564cbf4127f93f6ee21cf7ff59dec1fe2bbc1f1")
PISO = ("contendiente_resultados", "data/corrida0/CALC-EMAT-PAREJA-PISOS-0001/resultados.json",
        "3e3a908a66047ef7abc63c7ecd414d345a66712cd4786c072e83f64747d8359d")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "cc1_inegi_emat_2024__matrimonios_base_datos_2024_dbf"
_EDADES_C = ("EDAD_CON1", "EDAD_CON2")
# Columnas crudas de las que depende cada conducta (spec §2): si falta una, la conducta sale NO-ESTIMABLE.
DEPENDE = {
    "M-MISMO-SEXO": ("GENERO",),
    "M-CON-MENOR-18": _EDADES_C,
    "M-AMBOS-TRABAJAN": ("CONACTCON1", "CONACTCON2"),
    "M-MISMA-ESCOLARIDAD": ("ESCOL_CON1", "ESCOL_CON2"),
    "C-TRABAJA": ("CONACTCON1", "CONACTCON2"),
}

CONTRATO = {
    "x": X, "programa": "EMAT", "ola": "2024", "unidad": "MATRIMONIO-REGISTRADO y CONTRAYENTE",
    "contendientes": ["CALC-EMAT-PAREJA-PISOS-0001"],
    "payloads": [(PAYLOAD, "EMAT 2024 matrimonios registrados, DBF (miembro MATRI24.dbf) -- ola RESERVADA "
                           "(RESERVADA-NO-ABIERTA-NO-INDEXAR-L); sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: matrimonios/contrayentes/_todas/miembro_ola/lee_dbf"),
             (PISO[0], PISO[1], "piso 2023 sellado: P, ICC-LO, ICC-HI por celda"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Matrimonios registrados en 2024 (filas vivas de MATRI24.dbf) y sus dos contrayentes; universo por "
                "conducta según matrimonios()/contrayentes() del contendiente (edad 12-98, códigos válidos)",
    "filtros": "Un eje a la vez: M-* por TOTAL, ENT de registro, TLOC; C-* por TOTAL, SEXO, ESCOLARIDAD, TLOC; "
               "nunca cruces (guardia E.6)",
    "ponderador": "ninguno (registro completo: w = 1 por matrimonio o por contrayente)",
    "transformacion": "Recodificación del contendiente (spec EMAT-PAREJA-PISOS §2); C-EDAD-MEDIA fuera (media sin IC); "
                      "columna ausente -> NO-ESTIMABLE",
    "estimando": "R = proporción exacta del registro 2024 por conducta×eje×categoría; cobertura de R en el ICC del piso 2023",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec EMAT-PAREJA-PISOS §2): "
                                             + ", ".join(d)} for c, d in DEPENDE.items()]
               + [{"nombre": "C-EDAD-<tramo>", "definicion": "contrayente en el tramo de edad: EDAD_CON1, EDAD_CON2"}]
               + [{"nombre": v, "definicion": d} for v, d in (
                   ("ENT_REGIS", "entidad de registro (eje ENT 01-32)"),
                   ("TAM_LOC_RE", "tamaño de localidad de registro (eje TLOC)"),
                   ("SEXO_CON1/SEXO_CON2", "sexo del contrayente (eje SEXO)"))],
}


def sellados(inputs=None):
    S = E.modulo("m_emat_pareja_sellado", E.bytes_repo(inputs, *SELLADO))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, piso


def depende(c):
    return DEPENDE.get(c, _EDADES_C if c.startswith("C-EDAD-") else ())


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    c_conds = tuple(c for c in S.C_CONDUCTAS if c not in S.MEDIAS)
    return list(S._todas(S.M_CONDUCTAS, S.EJES_M)) + list(S._todas(c_conds, S.EJES_C))


def esquema_resultados():
    S, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)],
                     unidad_r="proporción exacta del registro EMAT 2024 (matrimonio o contrayente según la conducta)")


def lee_payload_reservado(S, ruta, cols):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Devuelve (frame de texto, campos
    ausentes); un campo ausente entra vacío (spec §5: NO-ESTIMABLE)."""
    with zipfile.ZipFile(ruta) as z:
        try:
            miembro = S.miembro_ola(z.namelist(), OLA)
        except S.ParoDeGuardia as e:  # el PARO del sellado se reporta con la clase de la guardia común
            raise G.ParoDeGuardia(str(e)) from e
        datos = z.read(miembro)
    presentes, faltan = {}, []
    for c in cols:
        try:
            presentes[c] = S.lee_dbf(datos, (c,))[c].to_numpy(dtype=object)
        except KeyError:
            faltan.append(c)
    n = len(next(iter(presentes.values()))) if presentes else 0
    df = pd.DataFrame(presentes) if presentes else pd.DataFrame(index=range(0))
    for c in faltan:
        df[c] = np.full(n, "", dtype=object)
    return df, faltan


def mide_r(S, frame, faltan=()):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada (w = 1)."""
    faltan = set(faltan)
    ym, em, _diag = S.matrimonios(frame, OLA)
    yc, ec = S.contrayentes(frame)
    out = {}
    for ys, ejes_def, ejes in ((ym, S.EJES_M, em), (yc, S.EJES_C, ec)):
        for c, y in ys.items():
            if c in S.MEDIAS or faltan & set(depende(c)):
                continue
            y = np.asarray(y, dtype=float)
            grupos = {"TOTAL": np.full(len(y), "TODOS", dtype=object)}
            grupos.update({e: np.asarray(ejes[e], dtype=object) for e in ejes_def})
            w = np.ones(len(y))
            for eje, g in grupos.items():
                for cat, r in G.proporcion_por_grupo(y, w, g).items():
                    out[(c, eje, cat)] = r["p"]
    return out


def filas(S, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(S.rid_p(c, eje, cat, "ICC-LO")),
             "hi": piso.get(S.rid_p(c, eje, cat, "ICC-HI")),
             "punto": piso.get(S.rid(c, S.PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(S)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S, piso = sellados(inputs)
    frame, faltan = lee_payload_reservado(S, inputs[PAYLOAD]["ruta_absoluta"], S.CAMPOS)
    return E.salida(P, filas(S, mide_r(S, frame, faltan), piso))
