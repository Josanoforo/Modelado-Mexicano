#!/usr/bin/env python3
"""Medidor de APERTURA de ENSANUT 2025 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Spec humana: `APERTURA-ENSANUT-2025-spec-v1_0.md` (esta carpeta); contrato: `APERTURA-ENSANUT-2025-spec.yaml`. NO SE HA CORRIDO
sobre ENSANUT 2025 y no se corre en este acto: corre sólo en caja, en el commit de
apertura que mesa autorice (receta: `RECETA-APERTURA-ENSANUT-2025.md`).

Qué hace al abrir: R = razón ponderada de cada conducta de
`CALC-ENSANUT-PISOS-SALUD-0001` en ENSANUT 2025, por categoría de UN eje a la vez,
con la recodificación del medidor sellado (importado por bytes, sha fijado); y
adjudica la cobertura del contendiente sellado (piso 2024 con IC calibrado de
persistencia, ICC-LO/ICC-HI de `resultados.json` sellado) con
`guardia_apertura.adjudica_cobertura`. Guardia E.6: auditoría AST de este archivo
antes de leer un byte del payload, y `proporcion_por_grupo` como único agregador.
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
P = "RESULT-APERTURA-ENSANUT-2025"
OLA_R = "2025"
OLA_PISO = "2024"
SELLADO = "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/medidor.py"
SELLADO_SHA = "f334da45a248ccf6d4b812cef2b6108a6dbb3a76825f3af9d5bd9d648e13abe8"
PISO = "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/resultados.json"
PISO_SHA = "a2d6654d84c002179dc40eb1c01999f7351dd27be09c52b414d3151033537434"
RECETA = "tools/dominios/salud/pisos_diseno.py"
RECETA_SHA = "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9"
PAYLOADS = {
    "ADUL": "ensanut_2025__adultos_2025_w_stata_stata_zip",
    "INTE": "ensanut_2025__integrantes_2025_w_stata_stata_zip",
    "UTIL": "ensanut_2025__utilizadores_2025_w_stata_stata_zip",
    "ADOL": "ensanut_2025__adolescentes_2025_w_stata_stata_zip",
}


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
    return (_modulo("m_ensanut_pisos_sellado", _bytes_fijados(SELLADO, SELLADO_SHA)),
            _modulo("receta_pisos_salud", _bytes_fijados(RECETA, RECETA_SHA)),
            json.loads(_bytes_fijados(PISO, PISO_SHA))["resultados"])


def lee_payload_reservado(R, M, arch, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige)."""
    return R.lee_dta(ruta, M.COLS[arch])


def mide_r(M, R, frames):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    out = {}
    inte = frames["INTE"]
    for arch in ("ADUL", "INTE", "UTIL", "ADOL"):
        f, ejes, _diag, edad = M.prepara(arch, frames[arch], None if arch == "INTE" else inte, R)
        w = f["_w"].to_numpy()
        for c, (a, ejes_c) in M.CONDUCTAS.items():
            if a != arch:
                continue
            y = np.asarray(M.conducta_y(c, f, R), dtype=float)
            y[~np.asarray(M.universo_edad(arch, edad))] = np.nan
            grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
            grupos.update({e: np.asarray(ejes[e], dtype=object) for e in M.ejes_de(arch, ejes_c)})
            for eje, g in grupos.items():
                for cat, r in G.proporcion_por_grupo(y, w, g).items():
                    out[(c, eje, cat)] = r["p"]
    return out


def celdas(M, r, piso):
    filas = []
    for c, (arch, ejes_c) in M.CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(M.ejes_de(arch, ejes_c).items()):
            for cat in cats:
                filas.append({"id": f"{c}|{eje}|{cat}", "conglomerado": c,
                              "lo": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-LO")),
                              "hi": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-HI")),
                              "punto": piso.get(M.rid(c, OLA_PISO, eje, cat, "P")),
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
