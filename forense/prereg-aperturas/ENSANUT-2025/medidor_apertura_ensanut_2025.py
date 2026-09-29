#!/usr/bin/env python3
"""Medidor de APERTURA de ENSANUT 2025 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Spec humana: `APERTURA-ENSANUT-2025-spec-v1_0.md`; contrato: `APERTURA-ENSANUT-2025-spec.yaml`;
receta: `RECETA-APERTURA-ENSANUT-2025.md`. NO SE HA CORRIDO sobre ENSANUT 2025: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada de cada conducta de `CALC-ENSANUT-PISOS-SALUD-0001` en ENSANUT 2025, por
categoría de UN eje a la vez, con la recodificación del medidor sellado (input `origen: repo`, sha fijado);
adjudica la cobertura del contendiente (piso 2024 con IC calibrado de persistencia, ICC-LO/ICC-HI de su
`resultados.json` sellado). Guardia E.6: auditoría AST de este archivo antes de leer un byte del payload;
`guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENSANUT-2025"
P = "RESULT-APERTURA-ENSANUT-2025"
OLA_PISO = "2024"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/medidor.py",
           "f334da45a248ccf6d4b812cef2b6108a6dbb3a76825f3af9d5bd9d648e13abe8")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/resultados.json",
        "a2d6654d84c002179dc40eb1c01999f7351dd27be09c52b414d3151033537434")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOADS = {
    "ADUL": "ensanut_2025__adultos_2025_w_stata_stata_zip",
    "INTE": "ensanut_2025__integrantes_2025_w_stata_stata_zip",
    "UTIL": "ensanut_2025__utilizadores_2025_w_stata_stata_zip",
    "ADOL": "ensanut_2025__adolescentes_2025_w_stata_stata_zip",
}

CONTRATO = {
    "x": X, "programa": "ENSANUT", "ola": "2025", "unidad": "PERSONA",
    "contendientes": ["CALC-ENSANUT-PISOS-SALUD-0001"],
    "payloads": [(pid, f"ENSANUT 2025 {a} -- ola RESERVADA; sólo este medidor la lee") for a, pid in PAYLOADS.items()],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: prepara/conducta_y/universo_edad/ejes_de"),
             (PISO[0], PISO[1], "piso 2024 sellado: P, ICC-LO, ICC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_dta y num de la receta de pisos"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas de ENSANUT 2025: adultos 20+, integrantes (todas las edades), utilizadores, adolescentes 10-19; "
                "ponde_f > 0 con est_sel y upm no vacíos (prepara() del contendiente)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESTRATO, ESCOLARIDAD 20+); nunca cruces (guardia E.6)",
    "ponderador": "ponde_f",
    "transformacion": "Recodificación del contendiente (forense/analisis/salud-bienestar/lista-cerrada-P1.md §2); "
                      "columna ausente o con texto/códigos distintos en el catálogo 2025 -> NO-ESTIMABLE",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENSANUT 2025; cobertura de R en el ICC del piso 2024",
    "variables": [{"nombre": c, "definicion": "conducta del contendiente (spec SALUD-ENSANUT-PISOS §2)"}
                  for c in ("DEPRESION-CESD7", "IDEACION-SUICIDA-ADULTOS", "DX-DIABETES", "DX-HIPERTENSION",
                            "FUMA-ACTUAL", "ALCOHOL-12M", "ALCOHOL-EXCESIVO-30D", "NECESIDAD-SALUD-3M",
                            "BUSCO-ATENCION", "FUE-ATENDIDO", "ATENCION-CONSULTORIO-FARMACIA",
                            "ATENCION-CURANDERO-HIERBERO", "IDEACION-SUICIDA-ADOLESCENTES")],
}


def sellados(inputs=None):
    M = E.modulo("m_ensanut_pisos_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud", E.bytes_repo(inputs, *RECETA))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return M, R, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(M):
    out = []
    for c, (arch, ejes_c) in M.CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(M.ejes_de(arch, ejes_c).items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    M, _R, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(M)])


def lee_payload_reservado(R, M, arch, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige). Spec §5: una columna de diseño o llave
    ausente es PARO; un reactivo o eje ausente entra vacío y sus celdas salen NO-ESTIMABLE (sin recodificar)."""
    cols = list(M.COLS[arch])
    try:
        return R.lee_dta(ruta, cols)
    except KeyError as exc:
        faltan = [c for c in cols if repr(c) in str(exc)]
    duras = [c for c in faltan if c in M.DISENO]
    if duras or not faltan:
        raise G.ParoDeGuardia(f"columnas de diseño o llave ausentes en {arch}: {duras or faltan}")
    df = R.lee_dta(ruta, [c for c in cols if c not in faltan])
    for c in faltan:
        df[c] = np.nan
    return df


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


def filas(M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-LO")),
             "hi": piso.get(M.rid(c, OLA_PISO, eje, cat, "ICC-HI")),
             "punto": piso.get(M.rid(c, OLA_PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(M)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = set(PAYLOADS.values()) | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    M, R, piso = sellados(inputs)
    frames = {a: lee_payload_reservado(R, M, a, inputs[pid]["ruta_absoluta"]) for a, pid in PAYLOADS.items()}
    return E.salida(P, filas(M, mide_r(M, R, frames), piso))
