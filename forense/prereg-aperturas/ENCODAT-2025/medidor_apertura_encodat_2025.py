#!/usr/bin/env python3
"""Medidor de APERTURA de ENCODAT 2025 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Spec humana: `APERTURA-ENCODAT-2025-spec-v1_0.md` (esta carpeta); contrato: `APERTURA-ENCODAT-2025-spec.yaml`. NO SE HA CORRIDO
sobre ENCODAT 2025 y no se corre en este acto: corre sólo en caja, en el commit de
apertura que mesa autorice (receta: `RECETA-APERTURA-ENCODAT-2025.md`).

Qué hace al abrir: R = razón ponderada de cada conducta de
`CALC-ENCODAT-PISOS-SUSTANCIAS-0001` en ENCODAT 2025, por categoría de UN eje a la
vez, con la recodificación del medidor sellado (importado por bytes, sha fijado); y
adjudica la cobertura del contendiente sellado (piso 2016-17 con su IC de diseño:
una sola ola abierta, sin IC de persistencia) con
`guardia_apertura.adjudica_cobertura`. Guardia E.6 idéntica a ENSANUT-2025.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import types

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
P = "RESULT-APERTURA-ENCODAT-2025"
OLA_R = "2025"
OLA_PISO = "2016"
SELLADO = "data/corrida0/CALC-ENCODAT-PISOS-SUSTANCIAS-0001/medidor.py"
SELLADO_SHA = "d2123bfb393dba0d770824d04a7ef66118544f6502d9347197b1e292cb882b9b"
PISO = "data/corrida0/CALC-ENCODAT-PISOS-SUSTANCIAS-0001/resultados.json"
PISO_SHA = "a905034448cd3631b5b541c8ebee0e57cff5aa826ef8d859da37fb7dfe54389d"
RECETA = "tools/dominios/salud/pisos_diseno.py"
RECETA_SHA = "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9"
PAYLOADS = {
    "IND": "encodat_2025__encodat_2025_adolescentes_adultos_stata_stata_zip",
    "HOG": "encodat_2025__encodat_2025_hogar_stata_stata_zip",
}
COLS = {"IND": "COLS_IND", "HOG": "COLS_HOG"}


def _guardia():
    spec = importlib.util.spec_from_file_location("guardia_apertura", os.path.join(os.path.dirname(AQUI), "guardia_apertura.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


G = _guardia()


def _bytes_fijados(rel, sha):
    b = open(os.path.join(RAIZ, rel), "rb").read()
    if hashlib.sha256(b).hexdigest() != sha:
        raise G.ParoDeGuardia(f"sha discordante: {rel}")
    return b


def _modulo(nombre, b):
    m = types.ModuleType(nombre)
    exec(compile(b, f"<{nombre}>", "exec"), m.__dict__)
    return m


def sellados():
    return (_modulo("m_encodat_pisos_sellado", _bytes_fijados(SELLADO, SELLADO_SHA)),
            _modulo("receta_pisos_salud", _bytes_fijados(RECETA, RECETA_SHA)),
            json.loads(_bytes_fijados(PISO, PISO_SHA))["resultados"])


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


def celdas(M, r, piso):
    filas = []
    for c in M.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(M.EJES.items()):
            for cat in cats:
                filas.append({"id": f"{c}|{eje}|{cat}", "conglomerado": c,
                              "lo": piso.get(M.rid(c, eje, cat, "IC-LO")),
                              "hi": piso.get(M.rid(c, eje, cat, "IC-HI")),
                              "punto": piso.get(M.rid(c, eje, cat, "P")),
                              "r": r.get((c, eje, cat))})
    return filas


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    if set(inputs) != set(PAYLOADS.values()):
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ set(PAYLOADS.values()))}")
    M, R, piso = sellados()
    frames = {a: lee_payload_reservado(R, M, a, inputs[pid]["ruta_absoluta"]) for a, pid in PAYLOADS.items()}
    return salida(M, piso, mide_r(M, R, frames))


def salida(M, piso, r):
    fs = celdas(M, r, piso)
    adj = G.adjudica_cobertura(fs)
    out = {f"{P}-{f['id']}-R": f["r"] for f in fs}
    out.update({f"{P}-DICTAMEN": adj["dictamen"], f"{P}-K": adj["k"], f"{P}-N": adj["n"],
                f"{P}-WILSON-LO": adj["wilson_lo"], f"{P}-WILSON-HI": adj["wilson_hi"],
                f"{P}-MAE-PUNTO": adj["mae_punto"], f"{P}-MARCA": "PROSPECTIVA"})
    return out
