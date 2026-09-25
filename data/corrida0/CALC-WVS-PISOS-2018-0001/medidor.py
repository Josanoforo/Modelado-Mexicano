#!/usr/bin/env python3
"""CALC-WVS-PISOS-2018-0001 · pisos por segmento WVS ola 7 México 2018 con IC de conglomerados.

ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONFIANZA-WVS-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre WVS.

Una sola ola de WVS en corpus (2018; E.6: no hay historia que reservar, se abre y se declara).
Proporciones y medias ponderadas (`W_WEIGHT`) de adultos 18+, total y por UN eje a la vez.
El archivo público no trae estrato: bootstrap de UPM (`I_PSU`) con estrato único.
Lo heredado se ejecuta desde los bytes hasheados de la receta de pisos (`receta_pisos_salud`)
y del motor del acto (`motor_pisos_confianza`).
"""
from __future__ import annotations

import types

P = "RESULT-WVS-PISOS-2018"
OLA = "2018"
PAY = "f00013084_wvs_wave_7_mexico_stata_v5_1"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})

# Recodificación por texto de pregunta (lista-cerrada-P1 §2 WVS). Todo código fuera de
# uno ∪ cero (no sabe, no contestó, faltantes extendidos) queda fuera.
C4 = ([1, 2], [3, 4])  # confianza 1–4: completa/algo (mucha/algo) vs. poca/nada
CONDUCTAS = {
    "CONFIANZA-INTERPERSONAL": ("bin", "Q57", [1], [2]),
    "CONFIA-FAMILIA": ("bin", "Q58", *C4),
    "CONFIA-VECINOS": ("bin", "Q59", *C4),
    "CONFIA-CONOCIDOS": ("bin", "Q60", *C4),
    "CONFIA-DESCONOCIDOS": ("bin", "Q61", *C4),
    "CONFIA-IGLESIAS": ("bin", "Q64", *C4),
    "CONFIA-EJERCITO": ("bin", "Q65", *C4),
    "CONFIA-POLICIA": ("bin", "Q69", *C4),
    "CONFIA-TRIBUNALES": ("bin", "Q70", *C4),
    "CONFIA-GOBIERNO": ("bin", "Q71", *C4),
    "CONFIA-PARTIDOS": ("bin", "Q72", *C4),
    "CONFIA-CONGRESO": ("bin", "Q73", *C4),
    "CONFIA-ELECCIONES": ("bin", "Q76", *C4),
    "MIEMBRO-ORG-RELIGIOSA": ("bin", "Q94", [1, 2], [0]),
    "MIEMBRO-ACTIVO-ORG-RELIGIOSA": ("bin", "Q94", [2], [0, 1]),
    "MIEMBRO-ACTIVO-ORG-DEPORTIVA": ("bin", "Q95", [2], [0, 1]),
    "MIEMBRO-ACTIVO-PARTIDO": ("bin", "Q98", [2], [0, 1]),
    "MIEMBRO-ACTIVO-AYUDA-MUTUA": ("bin", "Q103", [2], [0, 1]),
    "RELIGION-MUY-IMPORTANTE": ("bin", "Q6", [1], [2, 3, 4]),
    "IMPORTANCIA-DE-DIOS": ("media", "Q164", 1, 10),
    "ASISTE-SERVICIO-MENSUAL": ("bin", "Q171", [1, 2, 3], [4, 5, 6, 7]),
    "PERSONA-RELIGIOSA": ("bin", "Q173", [1], [2, 3]),
    "PERTENECE-DENOMINACION": ("bin", "Q289", [1, 2, 3, 4, 5, 6, 7], [0]),
    "CATOLICO": ("bin", "Q289", [1], [0, 2, 3, 4, 5, 6, 7]),
    "OBEDIENCIA-CUALIDAD-INFANTIL": ("bin", "Q17", [1], [2]),
    "MAS-RESPETO-AUTORIDAD-BUENO": ("bin", "Q45", [1], [2, 3]),
    "LIDER-FUERTE-BUENO": ("bin", "Q235", [1, 2], [3, 4]),
    "GOBIERNO-MILITAR-BUENO": ("bin", "Q237", [1, 2], [3, 4]),
    "RECHAZA-VECINO-HOMOSEXUAL": ("bin", "Q22", [1], [2]),
    "HOMOSEXUALIDAD-JUSTIFICABLE": ("media", "Q182", 1, 10),
    "FIRMO-PETICION": ("bin", "Q209", [1], [2, 3]),
    "ASISTIO-MANIFESTACION": ("bin", "Q211", [1], [2, 3]),
}
MAPAS = {
    "SEXO": ("Q260", {"HOMBRE": [1], "MUJER": [2]}),
    "ESCOLARIDAD": ("Q275", {"HASTA-PRIMARIA": [0, 1], "SECUNDARIA": [2], "MEDIA-SUPERIOR": [3, 4],
                             "SUPERIOR": [5, 6, 7, 8]}),
    "TAMLOC": ("G_TOWNSIZE2", {"MENOS-5MIL": [1], "5MIL-20MIL": [2], "20MIL-100MIL": [3],
                               "100MIL-500MIL": [4], "500MIL-MAS": [5]}),
    "INGRESO-SUBJETIVO": ("Q288R", {"BAJO": [1], "MEDIO": [2], "ALTO": [3]}),
}
EDAD_COL = "Q262"
PESO, UPM = "W_WEIGHT", "I_PSU"
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
             "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
             "TAMLOC": ("MENOS-5MIL", "5MIL-20MIL", "20MIL-100MIL", "100MIL-500MIL", "500MIL-MAS"),
             "INGRESO-SUBJETIVO": ("BAJO", "MEDIO", "ALTO")}
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
    frame = M.lee(inputs[PAY]["ruta_absoluta"], columnas(), miembro_sufijo=".dta")
    out = mide(frame, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-UNICA"] = "WVS 2018 -- unica ola en corpus; se abre (E.6), sin IC de persistencia"
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
    f += [M.fila(f"{P}-G-OLA-UNICA", "texto", "declaración")]
    return f
