#!/usr/bin/env python3
"""CALC-PDR1-LATINOBAROMETRO-0001 · piso RETROSPECTIVO Latinobarómetro 2024, México: satisfacción con el
funcionamiento de la democracia (P12STGBS.A), por segmento.

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-LATINOBAROMETRO (28/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/PDR1-LATINOBAROMETRO-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre el microdato.

Un solo input de dato: latinobarometro2024_bd_stata (LIBRE por id en el manifiesto). La ola 2023 NO se
re-mide (E.5): se citan CALC-LATINOBAROMETRO-COLA-2023-0001 (satisfacción con la democracia 2023) y
CALC-LATINOBAROMETRO-PISOS-2023-0001 (confianza institucional/interpersonal 2023). Filas IDENPA = 484
(México). El archivo no trae estrato ni UPM: bootstrap ponderado de entrevistas («MAS-PONDERADO»).
Lectura, ejes y estimación: motor y receta sellados, cargados por sha256 desde sus bytes.
"""
from __future__ import annotations

import types

P = "RESULT-PDR1-LATINOBAROMETRO"
OLA = "2024"
PAY = "latinobarometro2024_bd_stata"
MIEMBRO = "Latinobarometro_2024_Stata_esp_v20250817.dta"
PAIS = ("IDENPA", 484)
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})

CONDUCTAS = {
    "SATISFECHO-CON-LA-DEMOCRACIA": ("bin", "P12STGBS.A", [1, 2], [3, 4]),
}
MAPAS = {
    "SEXO": ("SEXO", {"HOMBRE": [1], "MUJER": [2]}),
    "ESCOLARIDAD": ("REEDUC.1", {"HASTA-BASICA": [1, 2, 3], "MEDIA": [4, 5], "SUPERIOR": [6, 7]}),
    "TAMLOC": ("TAMCIUD", {"MENOS-20MIL": [1, 2, 3], "20MIL-100MIL": [4, 5, 6], "100MIL-MAS": [7, 8]}),
    "CLASE-SUBJETIVA": ("S2", {"ALTA-MEDIA-ALTA": [1, 2], "MEDIA": [3], "MEDIA-BAJA": [4], "BAJA": [5]}),
}
EDAD_COL = "EDAD"
PESO, UPM = "WT", None
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
    out[f"{P}-G-OLA-ABIERTA"] = "Latinobarometro 2024 (LIBRE por id); 2023 se cita sellada (E.5), no se re-mide"
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
