#!/usr/bin/env python3
"""CALC-LATINOBAROMETRO-PISOS-2023-0001 · pisos por segmento Latinobarómetro 2023, México.

ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONFIANZA-LATINOBAROMETRO-PISOS-spec-v1_0.md, congelado en el COMMIT-1
antes de ejecutar este archivo sobre Latinobarómetro.

Olas en corpus: 2023 y 2024. 2024 es la más reciente y queda RESERVADA (E.6): este código
no la lee ni la nombra como input. Se abre 2023, filas `idenpa = 484` (México) — el resto de
países nunca sale del lector. El archivo no trae estrato ni UPM: IC por bootstrap ponderado
de entrevistas («MAS-PONDERADO»), declarado como cota inferior de la varianza de diseño.
"""
from __future__ import annotations

import types

P = "RESULT-LATINOBAROMETRO-PISOS-2023"
OLA = "2023"
PAY = "latinobarometro2023_bd_stata_zip"
MIEMBRO = "Latinobarometro_2023_Esp_Stata_v1_0.dta"
PAIS = ("idenpa", 484)
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})

C4 = ([1, 2], [3, 4])  # mucha/algo vs. poca/ninguna
RELIGIONES = list(range(1, 15)) + [96, 97]
CONDUCTAS = {
    "CONFIANZA-INTERPERSONAL": ("bin", "P9STGBS", [1], [2]),
    "CONFIA-FFAA": ("bin", "P13STGBS_A", *C4),
    "CONFIA-POLICIA": ("bin", "P13STGBS_B", *C4),
    "CONFIA-IGLESIA": ("bin", "P13ST_C", *C4),
    "CONFIA-CONGRESO": ("bin", "P13ST_D", *C4),
    "CONFIA-GOBIERNO": ("bin", "P13ST_E", *C4),
    "CONFIA-PODER-JUDICIAL": ("bin", "P13ST_F", *C4),
    "CONFIA-PARTIDOS": ("bin", "P13ST_G", *C4),
    "CONFIA-INSTITUCION-ELECTORAL": ("bin", "P13ST_H", *C4),
    "CONFIA-PRESIDENTE": ("bin", "P13ST_I", *C4),
    "CATOLICO": ("bin", "S1", [1], [c for c in RELIGIONES if c != 1]),
    "SIN-RELIGION": ("bin", "S1", [13, 14, 97], [c for c in RELIGIONES if c not in (13, 14, 97)]),
    "PRACTICANTE": ("bin", "S1A", [1, 2], [3, 4]),
    "DEMOCRACIA-PREFERIBLE": ("bin", "P10STGBS", [1], [2, 3]),
    "AUTORITARISMO-A-VECES-PREFERIBLE": ("bin", "P10STGBS", [2], [1, 3]),
    "NO-IMPORTA-GOBIERNO-NO-DEMOCRATICO": ("bin", "P18STM_B", [1, 2], [3, 4]),
    "APOYARIA-GOBIERNO-MILITAR": ("bin", "P20STM", [1], [2]),
    "PREFIERE-SOCIEDAD-DE-COSTUMBRES": ("bin", "P19N", [1], [2]),
    "TRABAJA-POR-COMUNIDAD": ("bin", "P44ST_B", [1, 2], [3, 4]),
    "FIRMO-PETICION": ("bin", "P45ST_A", [1], [2, 3]),
    "ASISTIO-MANIFESTACION": ("bin", "P45S_B", [1], [2, 3]),
}
MAPAS = {
    "SEXO": ("sexo", {"HOMBRE": [1], "MUJER": [2]}),
    "ESCOLARIDAD": ("REEEDUC_1", {"HASTA-BASICA": [1, 2, 3], "MEDIA": [4, 5], "SUPERIOR": [6, 7]}),
    "TAMLOC": ("tamciud", {"MENOS-20MIL": [1, 2, 3], "20MIL-100MIL": [4, 5, 6], "100MIL-MAS": [7, 8]}),
    "CLASE-SUBJETIVA": ("S2", {"ALTA-MEDIA-ALTA": [1, 2], "MEDIA": [3], "MEDIA-BAJA": [4], "BAJA": [5]}),
}
EDAD_COL = "edad"
PESO, UPM = "wt", None
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
             "ESCOLARIDAD": ("HASTA-BASICA", "MEDIA", "SUPERIOR"),
             "TAMLOC": ("MENOS-20MIL", "20MIL-100MIL", "100MIL-MAS"),
             "CLASE-SUBJETIVA": ("ALTA-MEDIA-ALTA", "MEDIA", "MEDIA-BAJA", "BAJA")}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-18-MAS")


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
    return list(dict.fromkeys([r[1] for r in CONDUCTAS.values()] + [c for c, _ in MAPAS.values()]
                              + [c for c in (EDAD_COL, PESO, UPM) if c]))


def mide(frame, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso=PESO, estrato=None, upm=UPM)
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.edad(f, EDAD_COL), EJES_CATS["EDAD"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    universo = M.num(f[EDAD_COL.lower()]) >= 18
    diag["FILAS-18-MAS"] = int(universo.sum())
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
    frame = M.lee(inputs[PAY]["ruta_absoluta"], columnas(), miembro=MIEMBRO, pais=PAIS)
    out = mide(frame, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-ABIERTA"] = "Latinobarometro 2023 -- 2024 RESERVADA (E.6); una ola abierta, sin IC de persistencia"
    return out


def esquema_resultados():
    import importlib.util
    import pathlib
    ruta = pathlib.Path(__file__).resolve().parents[3] / "tools/dominios/confianza/motor_pisos.py"
    spec = importlib.util.spec_from_file_location("motor_pisos_confianza", ruta)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    f = [M.fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    f += M.esquema_ola(P, OLA, CONDUCTAS, EJES_CATS)
    f += [M.fila(f"{P}-G-DISENO", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-ABIERTA", "texto", "declaración")]
    return f
