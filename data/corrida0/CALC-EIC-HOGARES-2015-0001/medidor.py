#!/usr/bin/env python3
"""CALC-EIC-HOGARES-2015-0001 · tipo de hogar por sexo de la jefatura, Encuesta Intercensal 2015.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-EIC-HOGARES-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar este
archivo sobre la Intercensal.

Unidad: HOGAR (vivienda particular habitada con tipo de hogar registrado; la tabla de viviendas trae
el tipo de hogar `TIPOHOG` y el sexo de la jefatura `JEFE_SEXO` ya construidos por INEGI). Peso
`FACTOR` (vivienda), bootstrap de UPM (`UPM`) dentro de estrato (`ESTRATO`). La Intercensal es la
única ola del instrumento; el Censo 2020 (instrumento hermano, ola más reciente del CCPV) queda
RESERVADO y no es input.
Dos denominadores, declarados: (a) todo hogar con tipo conocido (1, 2, 3, 5, 6); (b) sólo hogares
familiares (1, 2, 3). 4 («familiar no especificado») y 9 («no se sabe») quedan fuera de ambos.
"""
from __future__ import annotations

import types

P = "RESULT-EIC-HOGARES-2015"
OLA = "2015"
PAY = "eic2015_nacional_csv"
MIEMBRO = "TR_VIVIENDA15.CSV"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})

CONDUCTAS = {
    "HOGAR-AMPLIADO": ("bin", "TIPOHOG", [2], [1, 3, 5, 6]),
    "HOGAR-NUCLEAR": ("bin", "TIPOHOG", [1], [2, 3, 5, 6]),
    "HOGAR-UNIPERSONAL": ("bin", "TIPOHOG", [5], [1, 2, 3, 6]),
    "HOGAR-AMPLIADO-ENTRE-FAMILIARES": ("bin", "TIPOHOG", [2], [1, 3]),
}
MAPAS = {
    "JEFATURA": ("JEFE_SEXO", {"HOMBRE": [1], "MUJER": [3]}),
    "TAMLOC": ("TAMLOC", {"MENOS-2500": [1], "2500-14999": [2], "15MIL-49999": [3],
                          "50MIL-99999": [4], "100MIL-MAS": [5]}),
    "ENTIDAD": ("ENT", {f"{e:02d}": [e] for e in range(1, 33)}),
}
PESO, ESTRATO, UPM = "FACTOR", "ESTRATO", "UPM"
COLS_CRUDAS = ("TIPOHOG", "JEFE_SEXO", "TAMLOC", "ENT", PESO, ESTRATO, UPM)
EJES_CATS = {"JEFATURA": ("HOMBRE", "MUJER"),
             "TAMLOC": ("MENOS-2500", "2500-14999", "15MIL-49999", "50MIL-99999", "100MIL-MAS"),
             "ENTIDAD": tuple(f"{e:02d}" for e in range(1, 33))}
EXCLUIDOS_PREFIJO = ("cc1_inegi_ccpv_2020",)
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-TIPOHOG-CONOCIDO")


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
    ejes = {e: ejes[e] for e in EJES_CATS}
    tipo = M.num(f["tipohog"])
    universo = (tipo == 1) | (tipo == 2) | (tipo == 3) | (tipo == 5) | (tipo == 6)
    diag["FILAS-TIPOHOG-CONOCIDO"] = int(universo.sum())
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
    out[f"{P}-G-OLA-UNICA"] = ("Intercensal 2015 -- unica ola del instrumento; Censo 2020 RESERVADO (E.6), "
                               "no es input; sin IC de persistencia")
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
    for x in f:
        if x["id"].endswith("-N") and x["unidad"] == "personas sin ponderar":
            x["unidad"] = "hogares sin ponderar"
    f += [M.fila(f"{P}-G-DISENO", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-UNICA", "texto", "declaración")]
    return f
