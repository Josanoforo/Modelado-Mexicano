#!/usr/bin/env python3
"""CALC-ENOE-PARTICIPACION-2024T4-0001 · participación económica por sexo y jóvenes que no estudian ni están ocupados, ENOE 2024T4.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-ENOE-PARTICIPACION-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre ENOE 2024T4.

ENOE: 2026T2 RESERVADA (tabla final de CORPUS-COMPLETO) y el boletín 2026T1 consumido para
informalidad (C4 de FIRMAS-16); este código lee SÓLO la tabla sociodemográfica de 2024T4 (trimestre
que el report cita, «diciembre 2024») y no mide informalidad. Universo ENOE estándar (el de
`tools/dominios/enoe/pisos_v1_2.py`): entrevista completa (`r_def` = 0), residente habitual o nuevo
residente (`c_res` ∈ {1, 3}). Peso `fac_tri`; bootstrap de UPM (`upm`) dentro de estrato (`est_d_tri`).

  PARTICIPA-ECONOMICAMENTE  15+: `clase1` = 1 (PEA) frente a 2 (PNEA).
  NO-ESTUDIA-NI-OCUPADO-18-24  18–24: no asiste a la escuela (`cs_p17` = 2) y no ocupado (`clase2` ≠ 1)
                              frente a asiste o está ocupado; `cs_p17` = 9 fuera.
  MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24  entre quienes cumplen lo anterior: `sex` = 2 frente a 1.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-ENOE-PARTICIPACION-2024T4"
OLA = "2024T4"
PAY = "enoe_2024_4t_microdatos"
MIEMBRO = "ENOE_SDEMT424.csv"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS_PREFIJO = ("enoe_2026",)

CONDUCTAS = {
    "PARTICIPA-ECONOMICAMENTE": ("bin", "_pea", [1], [0]),
    "NO-ESTUDIA-NI-OCUPADO-18-24": ("bin", "_nini", [1], [0]),
    "MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24": ("bin", "_mujer_nini", [1], [0]),
}
MAPAS = {
    "SEXO": ("sex", {"HOMBRE": [1], "MUJER": [2]}),
    "LOCALIDAD": ("t_loc_tri", {"100MIL-MAS": [1], "15MIL-99MIL": [2], "2500-14999": [3],
                                "MENOS-2500": [4]}),
    "ESCOLARIDAD": ("niv_ins", {"PRIMARIA-INCOMPLETA": [1], "PRIMARIA-COMPLETA": [2],
                                "SECUNDARIA-COMPLETA": [3], "MEDIA-SUPERIOR-Y-SUPERIOR": [4]}),
    "ENTIDAD": ("ent", {f"{e:02d}": [e] for e in range(1, 33)}),
}
EDADES = (("15-17", 15, 17), ("18-24", 18, 24), ("25-44", 25, 44), ("45-64", 45, 64), ("65-MAS", 65, 98))
COLS_CRUDAS = ("r_def", "c_res", "eda", "sex", "cs_p17", "clase1", "clase2", "t_loc_tri", "niv_ins",
               "ent", "fac_tri", "est_d_tri", "upm")
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": tuple(c for c, _, _ in EDADES),
             "LOCALIDAD": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
             "ESCOLARIDAD": ("PRIMARIA-INCOMPLETA", "PRIMARIA-COMPLETA", "SECUNDARIA-COMPLETA",
                             "MEDIA-SUPERIOR-Y-SUPERIOR"),
             "ENTIDAD": tuple(f"{e:02d}" for e in range(1, 33))}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-UNIVERSO-15-MAS")


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
    f = frame.copy()
    c1 = M.num(f["clase1"])
    c2 = M.num(f["clase2"])
    asiste = M.num(f["cs_p17"])
    edad = M.num(f["eda"])
    sexo = M.num(f["sex"])
    pea = np.full(len(f), np.nan)
    pea[c1 == 1] = 1.0
    pea[c1 == 2] = 0.0
    joven = (edad >= 18) & (edad <= 24)
    conocido = np.isin(asiste, [1, 2]) & np.isfinite(c2)
    nini = np.full(len(f), np.nan)
    nini[joven & conocido] = 0.0
    nini[joven & conocido & (asiste == 2) & (c2 != 1)] = 1.0
    mn = np.full(len(f), np.nan)
    es_nini = nini == 1
    mn[es_nini & (sexo == 1)] = 0.0
    mn[es_nini & (sexo == 2)] = 1.0
    f["_pea"], f["_nini"], f["_mujer_nini"] = pea, nini, mn
    return f


def mide(frame, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso="fac_tri", estrato="est_d_tri", upm="upm")
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    f = derivadas(f, M)
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.eje_rango(f, "eda", EDADES), EJES_CATS["EDAD"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    edad = M.num(f["eda"])
    universo = ((M.num(f["r_def"]) == 0) & np.isin(M.num(f["c_res"]), [1, 3])
                & (edad >= 15) & (edad <= 98))
    diag["FILAS-UNIVERSO-15-MAS"] = int(universo.sum())
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
    frame = R.lee_csv_zip(inputs[PAY]["ruta_absoluta"], columnas(), miembro=MIEMBRO, encoding="latin-1")
    out = mide(frame, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-ABIERTA"] = ("ENOE 2024T4 -- abierta; 2026T2 RESERVADA y boletin 2026T1 consumido (C4), "
                                 "no son input; un trimestre, sin IC de persistencia")
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
