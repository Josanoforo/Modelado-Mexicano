#!/usr/bin/env python3
"""Medidor de APERTURA de EDR 2024 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-EDR-2024-spec-v1_0.md`; contrato: `APERTURA-EDR-2024-spec.yaml`;
receta: `RECETA-APERTURA-EDR-2024.md`. NO SE HA CORRIDO sobre EDR 2024: corre sólo en caja, en el
commit de apertura que mesa autorice.

EDR es REGISTRO ADMINISTRATIVO: unidad DEFUNCIÓN REGISTRADA (una fila de DEFUN24.dbf), conteo completo,
sin diseño ni ponderador (w = 1). Al abrir: R = proporción exacta de cada conducta de
`CALC-EDR-SUICIDIO-PISOS-0001` en el año de registro 2024, por categoría de UN eje a la vez, con la
recodificación del medidor sellado (`prepara`, `_ejes_de`, `miembro_ola`, `lee_dbf`; importado por bytes
con sha fijado). Adjudica la cobertura del contendiente (piso 2023 con IC calibrado de persistencia
ICC-LO/ICC-HI de su `resultados.json` sellado). Guardia E.6: auditoría AST de este archivo antes de leer
un byte del payload; `guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os
import zipfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "EDR-2024"
P = "RESULT-APERTURA-EDR-2024"
OLA = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-EDR-SUICIDIO-PISOS-0001/medidor.py",
           "148ccb1abfeb29c6802ce2069aa64555054a6a4d8452fb8c91bd8f18be19e6e1")
PISO = ("contendiente_resultados", "data/corrida0/CALC-EDR-SUICIDIO-PISOS-0001/resultados.json",
        "c39a931e574edb63032663479ff00a9aa4db4d0e10b03b4e953fb716ce977b74")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "edr2024_bd_dbf_zip"
# Variable de «presunto suicidio» en 2024: la misma de 2022-2023 (el sellado usa TIPO_DEFUN desde 2022).
PRESUNTO_2024 = "TIPO_DEFUN"
# Columnas crudas de las que depende cada conducta (spec §2): si falta una, la conducta sale NO-ESTIMABLE.
DEPENDE = {
    "SUICIDIO-CIE": ("CAUSA_DEF",),
    "SUICIDIO-PRESUNTO": (PRESUNTO_2024,),
    "SUIC-HOMBRE": ("CAUSA_DEF", "SEXO"),
    "SUIC-15-44": ("CAUSA_DEF", "EDAD"),
    "SUIC-15-29": ("CAUSA_DEF", "EDAD"),
    "SUIC-OCURRIDO-EN-OLA": ("CAUSA_DEF", "ANIO_OCUR"),
}

CONTRATO = {
    "x": X, "programa": "EDR", "ola": "2024", "unidad": "DEFUNCION-REGISTRADA",
    "contendientes": ["CALC-EDR-SUICIDIO-PISOS-0001"],
    "payloads": [(PAYLOAD, "EDR 2024 defunciones registradas, DBF (miembro DEFUN24.dbf) -- ola RESERVADA; "
                           "sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: prepara/_ejes_de/_todas/miembro_ola/lee_dbf"),
             (PISO[0], PISO[1], "piso 2023 sellado: P, ICC-LO, ICC-HI por celda"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Defunciones registradas en 2024 (todas las filas vivas de DEFUN24.dbf); universo por conducta "
                "según prepara() del contendiente (causa no vacía, suicidio CIE X60-X84, edad o sexo válidos)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ENT de residencia, TLOC de residencia, ESCOLARIDAD); "
               "SUIC-HOMBRE sin eje SEXO y SUIC-15-* sin eje EDAD; nunca cruces (guardia E.6)",
    "ponderador": "ninguno (registro completo: w = 1 por defunción)",
    "transformacion": "Recodificación del contendiente (spec EDR-SUICIDIO-PISOS §2); presunto suicidio = "
                      "TIPO_DEFUN == 3 (como 2022-2023); columna ausente -> NO-ESTIMABLE",
    "estimando": "R = proporción exacta de defunciones registradas en 2024 con la conducta, por conducta×eje×categoría; "
                 "cobertura de R en el ICC del piso 2023",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec EDR-SUICIDIO-PISOS §2): "
                                             + ", ".join(DEPENDE[c])} for c in DEPENDE]
               + [{"nombre": v, "definicion": d} for v, d in (
                   ("ENT_RESID", "entidad de residencia (eje ENT 01-32)"),
                   ("TLOC_RESID", "tamaño de localidad de residencia (eje TLOC)"),
                   ("ESCOLARIDA", "escolaridad del fallecido (eje ESCOLARIDAD)"))],
}


def sellados(inputs=None):
    S = E.modulo("m_edr_suicidio_sellado", E.bytes_repo(inputs, *SELLADO))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, piso


def campos(S):
    return tuple(S.CAMPOS_BASE) + (PRESUNTO_2024,)


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    return list(S._todas())


def esquema_resultados():
    S, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)],
                     unidad_r="proporción exacta de defunciones registradas en 2024")


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
    S.PRESUNTO[OLA] = PRESUNTO_2024  # extiende en memoria el mapa ola -> variable del sellado (spec §5)
    ys, ejes, _diag = S.prepara(frame, OLA)
    w = np.ones(len(frame))
    out = {}
    for c in S.CONDUCTAS:
        if faltan & set(DEPENDE[c]):
            continue
        y = np.asarray(ys[c], dtype=float)
        grupos = {"TOTAL": np.full(len(frame), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e], dtype=object) for e in S._ejes_de(c)})
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
    frame, faltan = lee_payload_reservado(S, inputs[PAYLOAD]["ruta_absoluta"], campos(S))
    return E.salida(P, filas(S, mide_r(S, frame, faltan), piso))
