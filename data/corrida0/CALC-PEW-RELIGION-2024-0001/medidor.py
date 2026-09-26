#!/usr/bin/env python3
"""CALC-PEW-RELIGION-2024-0001 · afiliación religiosa, cambio de religión y creencia en Dios, PEW Global Attitudes 2024, México.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-PEW-RELIGION-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar este
archivo sobre PEW 2024.

Olas en corpus: 2013–2025; 2025 es la más reciente y queda RESERVADA (E.6): este código no la lee ni
la nombra como input. Se abre 2024, filas `country` = 35 (México). Diseño: el archivo público no trae
estrato ni UPM para 2024 (mismo tratamiento que CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001): bootstrap
ponderado de entrevistas («MAS-PONDERADO»), peso `weight`. Ejes y lectura: los de aquel medidor.

Pew rotula `religion_christian` y `religion_none` «NOT FOR POINT ESTIMATES» porque sólo puebla los grupos
con muestra suficiente; en México el grupo católico está poblado. Se estima y se declara la advertencia
en la spec (§1): la cifra es de este archivo, no la publicada por Pew.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-PEW-RELIGION-2024"
OLA = "2024"
PAY = "pew_gas_spring2024"
PAIS = ("country", 35)
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS_PREFIJO = ("pew_gas_spring2025",)

CONDUCTAS = {
    "CATOLICO": ("bin", "_catolico", [1], [0]),
    "SIN-RELIGION": ("bin", "_sinrel", [1], [0]),
    "CAMBIO-DE-RELIGION": ("bin", "religion_switch", [1], [2]),
    "CREE-EN-DIOS": ("bin", "god", [1], [2]),
}
ESCOL = {"HASTA-PRIMARIA": [1, 2, 3], "SECUNDARIA": [4, 5], "MEDIA-SUPERIOR": [6, 7, 8, 9],
         "SUPERIOR": [10, 11, 12]}
MAPAS = {"SEXO": ("gender", {"HOMBRE": [1], "MUJER": [2]}),
         "ESCOLARIDAD": ("d_educ_mexico", ESCOL)}
EDAD_COL = "age"
PESO = "weight"
COLS_CRUDAS = ("religion_combined", "religion_christian", "religion_none", "religion_switch", "god",
               "gender", "age", "d_educ_mexico", PESO)
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
             "ESCOLARIDAD": tuple(ESCOL)}
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
    malos = {k for k in inputs if k.startswith(EXCLUIDOS_PREFIJO)}
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
    """CATOLICO: religion_christian = 1 frente a toda otra afiliación con código válido de
    religion_combined (1–7, 99); SIN-RELIGION: religion_combined = 7 frente a 1–6, 99."""
    f = frame.copy()
    comb = M.num(f["religion_combined"])
    chri = M.num(f["religion_christian"])
    valido = np.isin(comb, [1, 2, 3, 4, 5, 6, 7, 99])
    cat = np.full(len(f), np.nan)
    cat[valido] = 0.0
    cat[valido & (chri == 1)] = 1.0
    sr = np.full(len(f), np.nan)
    sr[valido] = 0.0
    sr[comb == 7] = 1.0
    f["_catolico"], f["_sinrel"] = cat, sr
    return f


def mide(frame, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso=PESO, estrato=None, upm=None)
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    f = derivadas(f, M)
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.edad(f, EDAD_COL), EJES_CATS["EDAD"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    edad = M.num(f[EDAD_COL.lower()])
    universo = (edad >= 18) & (edad <= 97)  # 98 Don't know / 99 Refused (Q109a) quedan fuera
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
    frame = M.lee(inputs[PAY]["ruta_absoluta"], columnas(), miembro_sufijo=".sav", pais=PAIS)
    out = mide(frame, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-ABIERTA"] = "PEW 2024 -- 2025 RESERVADA (E.6); una ola abierta, sin IC de persistencia"
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
    f += [M.fila(f"{P}-G-OLA-ABIERTA", "texto", "declaración")]
    return f
