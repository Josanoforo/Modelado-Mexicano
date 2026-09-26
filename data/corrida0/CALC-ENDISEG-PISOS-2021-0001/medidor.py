#!/usr/bin/env python3
"""CALC-ENDISEG-PISOS-2021-0001 · pisos por segmento ENDISEG 2021 (orientación sexual e identidad de género).

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-ENDISEG-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre ENDISEG.

Una sola ola de ENDISEG en corpus (2021; la ENDISEG web 2022 es otro instrumento, no probabilístico,
y no es input). Proporciones ponderadas (`FACTOR` de TMODULO: persona seleccionada de 15+), total y
por UN eje a la vez, con bootstrap de UPM (`UPM_DIS`) dentro de estrato (`EST_DIS`).
Lo heredado se ejecuta desde los bytes hasheados de la receta de pisos (`receta_pisos_salud`) y del
motor de pisos (`motor_pisos_confianza`).

Derivadas por texto de pregunta (spec §2), antes de la recodificación binaria:
  NOHETERO  8.1 (P8_1): 1,2,3,6 → 1 · 4,5 → 0 · otro → fuera.
  NOCIS     9.1 (P9_1) contra 7.1 (P7_1): P9_1 ∈ {3,4,5} → 1; P9_1 ∈ {1,2} y P7_1 ∈ {1,2}:
            distinto → 1, igual → 0; otro → fuera.
  LGBT      1 si NOHETERO = 1 o NOCIS = 1; 0 si ambas son 0; fuera en otro caso.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-ENDISEG-PISOS-2021"
OLA = "2021"
PAY = "endiseg2021_bd_csv_zip"
MIEMBRO = "TMODULO.csv"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS = frozenset({"cc1_inegi_investigacion_2022__endiseg_web_2022_bd_csv"})

CONDUCTAS = {
    "LGBT": ("bin", "_lgbt", [1], [0]),
    "ORIENTACION-NO-HETEROSEXUAL": ("bin", "_nohetero", [1], [0]),
    "IDENTIDAD-NO-CISGENERO": ("bin", "_nocis", [1], [0]),
    "VARIACION-INTERSEXUAL": ("bin", "P7_1A", [1], [2]),
    "MEDIA-SUPERIOR-O-MAS": ("bin", "NIV", [6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5]),
    "SOLTERO": ("bin", "P4_2", [6], [1, 2, 3, 4, 5]),
    "UNION-LIBRE": ("bin", "P4_2", [1], [2, 3, 4, 5, 6]),
    "CASADO": ("bin", "P4_2", [2], [1, 3, 4, 5, 6]),
}
MAPAS = {
    "SEXO-AL-NACER": ("P7_1", {"HOMBRE": [1], "MUJER": [2]}),
    "ESCOLARIDAD": ("NIV", {"HASTA-PRIMARIA": [0, 1, 2], "SECUNDARIA": [3, 4, 5],
                            "MEDIA-SUPERIOR": [6, 7], "SUPERIOR": [8, 9, 10]}),
    "CONYUGAL": ("P4_2", {"UNIDO": [1, 2], "ALGUNA-VEZ-UNIDO": [3, 4, 5], "SOLTERO": [6]}),
    "INDIGENA-AUTOADSCRITO": ("P4_7", {"SI": [1], "NO": [2]}),
    "AFRO-AUTOADSCRITO": ("P4_4", {"SI": [1], "NO": [2]}),
    "LGBT": ("_lgbt", {"SI": [1], "NO": [0]}),
    "ENTIDAD": ("ENT", {f"{e:02d}": [e] for e in range(1, 33)}),
}
EDAD_COL = "P4_1"
EDADES = (("15-19", 15, 19), ("20-29", 20, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 96))
PESO, ESTRATO, UPM = "FACTOR", "EST_DIS", "UPM_DIS"
COLS_CRUDAS = ("P8_1", "P9_1", "P7_1", "P7_1A", "NIV", "P4_2", "P4_7", "P4_4", "ENT", EDAD_COL,
               PESO, ESTRATO, UPM)
EJES_CATS = {"SEXO-AL-NACER": ("HOMBRE", "MUJER"),
             "EDAD": tuple(c for c, _, _ in EDADES),
             "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
             "CONYUGAL": ("UNIDO", "ALGUNA-VEZ-UNIDO", "SOLTERO"),
             "INDIGENA-AUTOADSCRITO": ("SI", "NO"),
             "AFRO-AUTOADSCRITO": ("SI", "NO"),
             "LGBT": ("SI", "NO"),
             "ENTIDAD": tuple(f"{e:02d}" for e in range(1, 33))}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-15-MAS")


class ParoDeGuardia(RuntimeError):
    pass


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | {PAY}
    malos = set(inputs) & EXCLUIDOS
    if malos or set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted((set(inputs) ^ esperados) | malos)}")
    if not inputs[PAY].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{PAY}` sin ruta resuelta")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"{k} sin bytes: se exige origen repo")


def columnas():
    return list(COLS_CRUDAS)


def derivadas(frame, M):
    """Añade `_nohetero`, `_nocis`, `_lgbt` (1/0/NaN) según el docstring del módulo."""
    f = frame.copy()
    o = M.num(f["p8_1"])
    ident = M.num(f["p9_1"])
    nacer = M.num(f["p7_1"])
    noh = np.full(len(f), np.nan)
    noh[np.isin(o, [1, 2, 3, 6])] = 1.0
    noh[np.isin(o, [4, 5])] = 0.0
    noc = np.full(len(f), np.nan)
    noc[np.isin(ident, [3, 4, 5])] = 1.0
    binario = np.isin(ident, [1, 2]) & np.isin(nacer, [1, 2])
    noc[binario & (ident != nacer)] = 1.0
    noc[binario & (ident == nacer)] = 0.0
    lg = np.full(len(f), np.nan)
    lg[(noh == 0) & (noc == 0)] = 0.0
    lg[(noh == 1) | (noc == 1)] = 1.0
    f["_nohetero"], f["_nocis"], f["_lgbt"] = noh, noc, lg
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
    universo = (edad >= 15) & (edad <= 96)
    diag["FILAS-15-MAS"] = int(universo.sum())
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
    out[f"{P}-G-OLA-UNICA"] = "ENDISEG 2021 -- unica ola del instrumento en corpus; se abre (E.6), sin IC de persistencia"
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
