#!/usr/bin/env python3
"""Medidor de APERTURA de ENOE 2026T2 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENOE-2026T2-spec-v1_0.md`; contrato: `APERTURA-ENOE-2026T2-spec.yaml`;
receta: `RECETA-APERTURA-ENOE-2026T2.md`. NO SE HA CORRIDO sobre ENOE 2026T2: corre sólo en caja,
en el commit de apertura que mesa autorice.

Al abrir: R = razón ponderada de cada conducta de `CALC-ENOE-PARTICIPACION-2024T4-0001` en la tabla
sociodemográfica (SDEMT) de ENOE 2026T2, por categoría de UN eje a la vez, con la recodificación y el
universo del medidor sellado (`derivadas`, CONDUCTAS, MAPAS, EDADES; importado por bytes con sha
fijado) y el motor de pisos (`prepara_diseno`, `recodifica`, `eje_mapa`, `eje_rango`). Contendiente por
celda: piso 2024T4 con su IC de diseño (IC-LO/IC-HI sellados; el contendiente no publica IC de
persistencia). Guardia E.6: auditoría AST de este archivo antes de leer un byte del payload;
`guardia_apertura.proporcion_por_grupo` es el único agregador.
"""
from __future__ import annotations

import os
import re

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENOE-2026T2"
P = "RESULT-APERTURA-ENOE-2026T2"
OLA_PISO = "2024T4"
PREF_PISO = "RESULT-ENOE-PARTICIPACION-2024T4"


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

SELLADO = ("contendiente_medidor", "data/corrida0/CALC-ENOE-PARTICIPACION-2024T4-0001/medidor.py",
           "ba28dfa911966774e3bf8066dd819ba7d75349b0b2ec3f8a290019a1d7bcfaa2")
PISO = ("contendiente_resultados", "data/corrida0/CALC-ENOE-PARTICIPACION-2024T4-0001/resultados.json",
        "4cb128dd64510fffee781568f61712d3086a84d117eb34f3a8a3bc7e61934c6d")
RECETA = ("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py",
          "b82a4fefbf073f247033f376b8bc34183a32db27de48f5d5cafd0d30bbc000c9")
MOTOR = ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py",
         "7d0494f43052e0ea39ce0baf5f6505ccf889b386cfa3c0775b0dbdfb56ef958e")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "cc1_inegi_enoe_2026t2__enoe_2026_trim2_csv"
# Tabla SDEMT del trimestre: en 2024T4 el miembro es ENOE_SDEMT424.csv; aquí se resuelve por patrón
# (SDEMT + trimestre 2 + año 26), sin distinguir mayúsculas ni carpeta. Cero o más de uno -> PARO.
RX_MIEMBRO = re.compile(r"(?i)(^|/)(enoe_)?sdemt226\.csv$")
DISENO = ("fac_tri", "est_d_tri", "upm", "r_def", "c_res", "eda")   # diseño y universo: ausente -> PARO

CONTRATO = {
    "x": X, "programa": "ENOE", "ola": "2026T2", "unidad": "PERSONA",
    "contendientes": ["CALC-ENOE-PARTICIPACION-2024T4-0001"],
    "payloads": [(PAYLOAD, "ENOE 2026T2 base de datos CSV (tabla SDEMT) -- ola RESERVADA; sólo este medidor la lee")],
    "repo": [(SELLADO[0], SELLADO[1], "medidor sellado del contendiente: CONDUCTAS, MAPAS, EDADES, EJES_CATS, derivadas"),
             (PISO[0], PISO[1], "piso 2024T4 sellado: P, IC-LO, IC-HI por celda"),
             (RECETA[0], RECETA[1], "lee_csv_zip y num de la receta de pisos"),
             (MOTOR[0], MOTOR[1], "prepara_diseno, recodifica, eje_mapa, eje_rango del motor de pisos"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Residente habitual o nuevo (c_res 1,3) con entrevista completa (r_def 0), 15-98 años, ENOE 2026T2 "
                "(SDEMT); fac_tri > 0, est_d_tri y upm no vacíos (el universo del contendiente)",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, LOCALIDAD, ESCOLARIDAD, ENTIDAD); nunca cruces (guardia E.6)",
    "ponderador": "fac_tri",
    "transformacion": "Recodificación del contendiente (spec COLA-ENOE-PARTICIPACION §2, derivadas() del medidor sellado); "
                      "columna ausente en el catálogo 2026T2 -> NO-ESTIMABLE (R None), sin recodificación ad hoc",
    "estimando": "R = Σw·y/Σw por conducta×eje×categoría en ENOE 2026T2; cobertura de R en el IC de diseño del piso 2024T4",
    "variables": [{"nombre": "PARTICIPA-ECONOMICAMENTE", "definicion": "clase1 = 1 frente a 2, 15+ (spec contendiente §2)"},
                  {"nombre": "NO-ESTUDIA-NI-OCUPADO-18-24",
                   "definicion": "18-24: cs_p17 = 2 y clase2 != 1 frente a asiste u ocupado (spec contendiente §2)"},
                  {"nombre": "MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24",
                   "definicion": "entre quienes cumplen la anterior: sex = 2 frente a 1 (spec contendiente §2)"}],
}


def sellados(inputs=None):
    S = E.modulo("m_enoe_participacion_sellado", E.bytes_repo(inputs, *SELLADO))
    R = E.modulo("receta_pisos_salud_enoe", E.bytes_repo(inputs, *RECETA))
    M = E.modulo("motor_pisos_confianza_enoe", E.bytes_repo(inputs, *MOTOR))
    piso = E.json_repo(inputs, *PISO)["resultados"]
    return S, R, M, piso


def _cid(c, eje, cat):
    return f"{c}-{eje}-{cat}"


def celdas_de(S):
    out = []
    for c in S.CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(S.EJES_CATS.items()):
            out += [(c, eje, cat) for cat in cats]
    return out


def esquema_resultados():
    S, _R, _M, _p = sellados()
    return E.esquema(P, [_cid(*k) for k in celdas_de(S)])


def lee_payload_reservado(S, R, ruta):
    """Única lectura de la ola reservada (la auditoría AST lo exige): la tabla SDEMT de 2026T2 con las
    columnas del contendiente que existan; una columna de diseño o de universo ausente es PARO, una de
    conducta o eje ausente queda vacía (-> NO-ESTIMABLE)."""
    import zipfile

    with zipfile.ZipFile(ruta) as z:
        cands = [n for n in z.namelist() if RX_MIEMBRO.search(n) and not n.startswith("__MACOSX")]
        if len(cands) != 1:
            raise G.ParoDeGuardia(f"tabla SDEMT 2026T2: {len(cands)} miembros ({cands})")
        with z.open(cands[0]) as fh:
            cab = fh.readline().decode("latin-1")
    reales = {c.strip().strip('"').lower() for c in cab.strip().split(",")}
    faltan_diseno = [c for c in DISENO if c not in reales]
    if faltan_diseno:
        raise G.ParoDeGuardia(f"columnas de diseño/universo ausentes en {cands[0]}: {faltan_diseno}")
    hay = [c for c in S.columnas() if c in reales]
    f = R.lee_csv_zip(ruta, hay, miembro=cands[0], encoding="latin-1")
    for c in S.columnas():
        if c not in f.columns:
            f[c] = ""
    return f


def mide_r(S, M, frame):
    """{(conducta, eje, cat): p} con UNA variable de agrupación por llamada."""
    f, _etiqueta, _descartadas = M.prepara_diseno(frame, peso="fac_tri", estrato="est_d_tri", upm="upm")
    f = S.derivadas(f, M)
    ejes = {e: M.eje_mapa(f, col, mapa) for e, (col, mapa) in S.MAPAS.items()}
    ejes["EDAD"] = M.eje_rango(f, "eda", S.EDADES)
    edad = M.num(f["eda"])
    universo = ((M.num(f["r_def"]) == 0) & np.isin(M.num(f["c_res"]), [1, 3]) & (edad >= 15) & (edad <= 98))
    w = f["_w"].to_numpy(dtype=float)
    out = {}
    for c, regla in S.CONDUCTAS.items():
        y = np.asarray(M.recodifica(f, regla), dtype=float)
        y[~universo] = np.nan
        grupos = {"TOTAL": np.full(len(f), "TODOS", dtype=object)}
        grupos.update({e: np.asarray(ejes[e], dtype=object) for e in S.EJES_CATS})
        for eje, g in grupos.items():
            for cat, r in G.proporcion_por_grupo(y, w, g).items():
                out[(c, eje, cat)] = r["p"]
    return out


def filas(S, M, r, piso):
    return [{"id": _cid(c, eje, cat), "conglomerado": c,
             "lo": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-LO")),
             "hi": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "IC-HI")),
             "punto": piso.get(M.rid(PREF_PISO, c, OLA_PISO, eje, cat, "P")),
             "r": r.get((c, eje, cat))} for c, eje, cat in celdas_de(S)]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    S, R, M, piso = sellados(inputs)
    frame = lee_payload_reservado(S, R, inputs[PAYLOAD]["ruta_absoluta"])
    return E.salida(P, filas(S, M, mide_r(S, M, frame), piso))
