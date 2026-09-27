#!/usr/bin/env python3
"""CALC-ENASEM-ESCOLARIDAD-2021-0001 · personas de 50+ sin escolaridad por sexo y edad, ENASEM 2021.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-ENASEM-ESCOLARIDAD-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre ENASEM.

Olas en corpus: 2018, 2021, 2024. 2024 es la más reciente y queda RESERVADA (E.6): este código no la
lee ni la nombra como input. Se abre 2021 (sección A-C-D-E-PC-F-H-I). Unidad persona entrevistada con
factor individual transversal 2021 (`FACTORI_21` > 0), 50 años o más (`AGE_21`). Bootstrap de UPM
(`UPM_DIS_21`) dentro de estrato (`EST_DIS_21`).
SIN-ESCOLARIDAD: «Años de Educación» (`YRSCHOOL`) = 0 frente a 1–22; blanco fuera.
"""
from __future__ import annotations

import types

P = "RESULT-ENASEM-ESCOLARIDAD-2021"
OLA = "2021"
PAY = "enasem2021_bd_csv_zip"
MIEMBRO = "SECT_A_C_D_E_PC_F_H_I_2021.csv"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS_PREFIJO = ("enasem2024",)

CONDUCTAS = {
    "SIN-ESCOLARIDAD": ("bin", "YRSCHOOL", [0], list(range(1, 23))),
    "SEIS-ANOS-O-MENOS": ("bin", "YRSCHOOL", list(range(0, 7)), list(range(7, 23))),
}
MAPAS = {"SEXO": ("SEX_21", {"HOMBRE": [1], "MUJER": [2]})}
EDAD_COL = "AGE_21"
EDADES = (("50-59", 50, 59), ("60-69", 60, 69), ("70-79", 70, 79), ("80-MAS", 80, 130))
PESO, ESTRATO, UPM = "FACTORI_21", "EST_DIS_21", "UPM_DIS_21"
COLS_CRUDAS = ("YRSCHOOL", "SEX_21", EDAD_COL, PESO, ESTRATO, UPM)
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": tuple(c for c, _, _ in EDADES)}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-50-MAS")


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


def mide(frame, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso=PESO, estrato=ESTRATO, upm=UPM)
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.eje_rango(f, EDAD_COL, EDADES), EJES_CATS["EDAD"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    edad = M.num(f[EDAD_COL.lower()])
    universo = (edad >= 50) & (edad <= 120)  # 888/999 = no responde/no sabe (FD) quedan fuera
    diag["FILAS-50-MAS"] = int(universo.sum())
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
    out[f"{P}-G-OLA-ABIERTA"] = "ENASEM 2021 -- 2024 RESERVADA (E.6); una ola abierta, sin IC de persistencia"
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
