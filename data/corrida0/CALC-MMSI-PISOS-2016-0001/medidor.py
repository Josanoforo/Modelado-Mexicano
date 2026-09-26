#!/usr/bin/env python3
"""CALC-MMSI-PISOS-2016-0001 · pisos por segmento MMSI 2016 (escolaridad, ocupación directiva, movilidad percibida).

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-MMSI-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar este
archivo sobre MMSI.

Una sola ola del módulo en corpus (2016; se abre, E.6). Proporciones ponderadas (`Factor_Per`) de
las personas de 25 a 64 años entrevistadas, total y por UN eje a la vez, con bootstrap de UPM
(`upm_ENH`) dentro de estrato (`est_dis_ENH`).

El tono de piel (10.2, escala cromática A…K mostrada en tarjeta; la tarjeta del manual del
entrevistador, p. 81, va de A —más oscuro— a K —más claro—) y el origen autoadscrito (10.3) entran
SÓLO como marcador de trato y posición social (estructura), nunca como ascendencia → conducta
(firewall genético, §3 de las instrucciones): las conductas medidas son resultados de
estratificación (escolaridad alcanzada, ocupación, percepción de movilidad), no decisiones
atribuidas a un grupo. INTERPRETACIÓN-DECLARADA, rotulada para ratificación en la hoja de firmas.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-MMSI-PISOS-2016"
OLA = "2016"
PAY = "mmsi2016_bd_csv_zip"
MIEMBRO = "MMSI_2016.csv"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})

CONDUCTAS = {
    "EDUCACION-SUPERIOR": ("bin", "NivEsc_Inf", [7], [1, 2, 3, 4, 5, 6]),
    "EDUCACION-SUPERIOR-MUJER": ("bin", "_sup_mujer", [1], [0]),
    "EDUCACION-SUPERIOR-HOMBRE": ("bin", "_sup_hombre", [1], [0]),
    "OCUPACION-DIRECTIVA": ("bin", "DivOcu_Act", [1], [2, 3, 4, 5, 6, 7, 8, 9]),
    "PERCIBE-MEJORA-SOCIOECONOMICA": ("bin", "Per_SitEco", [1], [2, 3]),
}
TONOS = "ABCDEFGHIJK"
MAPAS = {
    "SEXO": ("P1_1", {"HOMBRE": [1], "MUJER": [2]}),
    "TONO": ("P10_2", {f"TONO-{t}": [i + 1] for i, t in enumerate(TONOS)}),
    "TONO-TRAMO": ("P10_2", {"A-E": [1, 2, 3, 4, 5], "F-G": [6, 7], "H-K": [8, 9, 10, 11]}),
    "ORIGEN-AUTOADSCRITO": ("P10_3", {"NEGRA-MULATA": [1], "INDIGENA": [2], "MESTIZA": [3],
                                      "BLANCA": [4], "OTRA": [5]}),
    "LENGUA-INDIGENA": ("P10_1", {"SI": [1], "NO": [2]}),
    "TAMLOC": ("tam_loc_ENH", {"100MIL-MAS": [1], "15MIL-99MIL": [2], "2500-14999": [3],
                                "MENOS-2500": [4]}),
}
EDAD_COL = "P1_2"
EDADES = (("25-34", 25, 34), ("35-44", 35, 44), ("45-54", 45, 54), ("55-64", 55, 64))
PESO, ESTRATO, UPM = "Factor_Per", "est_dis_ENH", "upm_ENH"
COLS_CRUDAS = ("NivEsc_Inf", "DivOcu_Act", "Per_SitEco", "P1_1", "P1_2", "P10_1", "P10_2", "P10_3",
               "tam_loc_ENH", PESO, ESTRATO, UPM)
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"),
             "EDAD": tuple(c for c, _, _ in EDADES),
             "TONO": tuple(f"TONO-{t}" for t in TONOS),
             "TONO-TRAMO": ("A-E", "F-G", "H-K"),
             "ORIGEN-AUTOADSCRITO": ("NEGRA-MULATA", "INDIGENA", "MESTIZA", "BLANCA", "OTRA"),
             "LENGUA-INDIGENA": ("SI", "NO"),
             "TAMLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500")}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-25-64")


class ParoDeGuardia(RuntimeError):
    pass


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | {PAY}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    if not inputs[PAY].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{PAY}` sin ruta resuelta")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"{k} sin bytes: se exige origen repo")


def columnas():
    return list(COLS_CRUDAS)


def derivadas(frame, M):
    """`_sup_mujer` / `_sup_hombre`: educación superior (NivEsc_Inf 7 vs 1–6) sólo en ese sexo."""
    f = frame.copy()
    sup = M.recodifica(f, CONDUCTAS["EDUCACION-SUPERIOR"])
    sexo = M.num(f["p1_1"])
    f["_sup_mujer"] = np.where(sexo == 2, sup, np.nan)
    f["_sup_hombre"] = np.where(sexo == 1, sup, np.nan)
    return f


def mide(frame, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso=PESO, estrato=ESTRATO, upm=UPM)
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    f = derivadas(f, M)
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.eje_rango(f, EDAD_COL, EDADES), EJES_CATS["EDAD"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    edad = M.num(f[EDAD_COL.lower()])
    universo = (edad >= 25) & (edad <= 64)
    diag["FILAS-25-64"] = int(universo.sum())
    out = {f"{P}-G-{k}": v for k, v in diag.items()}
    out.update(M.mide_ola(R, f, CONDUCTAS, ejes, P, OLA, replicas, semilla, universo=universo))
    out[f"{P}-G-DISENO"] = etiqueta
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    M = _modulo_desde_bytes("motor_pisos_confianza", inputs["motor_pisos_confianza"]["bytes"])
    frame = R.lee_csv_zip(inputs[PAY]["ruta_absoluta"], columnas(), miembro=MIEMBRO)
    out = mide(frame, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-UNICA"] = "MMSI 2016 -- unica ola del modulo en corpus; se abre (E.6), sin IC de persistencia"
    return out


def _motor():
    import importlib.util
    import pathlib
    ruta = pathlib.Path(__file__).resolve().parents[3] / "tools/dominios/confianza/motor_pisos.py"
    spec = importlib.util.spec_from_file_location("motor_pisos_confianza", ruta)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    return M


def esquema_resultados():
    M = _motor()
    f = [M.fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    f += M.esquema_ola(P, OLA, CONDUCTAS, EJES_CATS)
    f += [M.fila(f"{P}-G-DISENO", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-UNICA", "texto", "declaración")]
    return f
