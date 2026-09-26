#!/usr/bin/env python3
"""CALC-ENADID-COLA-2018-0001 · ENADID 2018: disolución según tipo de unión y jefatura en hogares con migrante varón.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-ENADID-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar este
archivo sobre ENADID.

Olas en corpus: 1992, 1997, 2009, 2014, 2018, 2023. 2023 es la más reciente y queda RESERVADA para
estas conductas (E.6): este código no la lee ni la nombra como input. Se abre 2018. Dos marcos, cada
uno con su bootstrap de UPM (`upm_dis`) dentro de estrato (`est_dis`):

  MUJERES (TMujer2, mujeres elegibles de 15–54, `fac_per`), por la situación conyugal ACTUAL (10.1,
  `p10_1`): entre las que su unión actual o última fue UNIÓN LIBRE (1 vive en unión libre, 2 separada
  de unión libre, 5 viuda de unión libre), la proporción SEPARADA (2); entre las de MATRIMONIO (7
  casada, 3 separada de matrimonio, 4 divorciada, 6 viuda de matrimonio), la proporción SEPARADA O
  DIVORCIADA (3, 4). Es prevalencia de disolución en el stock de uniones, no un riesgo por duración:
  la razón entre las dos se compara con el «3.4 veces» del report como orden, no como el mismo
  estimando.
  HOGARES (TSdem, renglón de la jefatura `paren` = 1, `fac_viv`): JEFATURA-FEMENINA (`sexo` 2 vs 1)
  entre hogares con al menos un emigrante internacional varón que hoy vive fuera de México (TMigrante:
  `p4_6` = 1 y `p4_15` ∈ {1, 3}), y la misma proporción entre hogares sin él.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-ENADID-COLA-2018"
OLA = "2018"
PAY = "enadid2018_bd_csv_zip"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS_PREFIJO = ("enadid2023", "cc1_inegi_enadid_2023")

COND_MUJ = {
    "SEPARADA-ENTRE-UNION-LIBRE": ("bin", "_sep_ul", [1], [0]),
    "SEPARADA-O-DIVORCIADA-ENTRE-MATRIMONIO": ("bin", "_sep_mat", [1], [0]),
}
COND_HOG = {
    "JEFATURA-FEMENINA-CON-MIGRANTE-VARON": ("bin", "_jf_con", [1], [0]),
    "JEFATURA-FEMENINA-SIN-MIGRANTE-VARON": ("bin", "_jf_sin", [1], [0]),
}
TAMLOC = ("tam_loc", {"100MIL-MAS": [1], "15MIL-99MIL": [2], "2500-14999": [3], "MENOS-2500": [4]})
MAPAS_MUJ = {"TAMLOC": TAMLOC,
             "ESCOLARIDAD": ("niv", {"HASTA-PRIMARIA": [0, 1, 2], "SECUNDARIA": [3, 4, 5],
                                     "MEDIA-SUPERIOR": [6, 7], "SUPERIOR": [8, 9, 10, 11]})}
MAPAS_HOG = {"TAMLOC": TAMLOC, "ENTIDAD": ("ent", {f"{e:02d}": [e] for e in range(1, 33)})}
EDADES = (("15-24", 15, 24), ("25-34", 25, 34), ("35-44", 35, 44), ("45-54", 45, 54))
EJES_MUJ = {"EDAD": tuple(c for c, _, _ in EDADES),
            "TAMLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
            "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR")}
EJES_HOG = {"TAMLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
            "ENTIDAD": tuple(f"{e:02d}" for e in range(1, 33))}
COLS_MUJ = ("p10_1", "edad_muj", "tam_loc", "niv", "fac_per", "est_dis", "upm_dis")
COLS_HOG = ("llave_hog", "paren", "sexo", "ent", "tam_loc", "fac_viv", "est_dis", "upm_dis")
COLS_MIG = ("llave_hog", "p4_6", "p4_15")
MIEMBROS = {"MUJ": "TMujer2.csv", "HOG": "TSdem.csv", "MIG": "TMigrante.csv"}
_DIAG = ("MUJ-FILAS-LEIDAS", "MUJ-FILAS-DISENO-VALIDO", "MUJ-FILAS-15-54",
         "HOG-FILAS-JEFATURA", "HOG-FILAS-DISENO-VALIDO", "HOG-CON-MIGRANTE-VARON")


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
    return list(dict.fromkeys(COLS_MUJ + COLS_HOG + COLS_MIG))


def derivadas_mujeres(f, M):
    f = f.copy()
    c = M.num(f["p10_1"])
    ul = np.full(len(f), np.nan)
    ul[np.isin(c, [2])] = 1.0
    ul[np.isin(c, [1, 5])] = 0.0
    ma = np.full(len(f), np.nan)
    ma[np.isin(c, [3, 4])] = 1.0
    ma[np.isin(c, [6, 7])] = 0.0
    f["_sep_ul"], f["_sep_mat"] = ul, ma
    return f


def derivadas_hogares(jefes, mig, M):
    """`_jf_con` / `_jf_sin`: jefatura femenina (sexo 2 vs 1) en hogares con / sin emigrante varón fuera."""
    f = jefes.copy()
    m = mig.copy()
    varon_fuera = (M.num(m["p4_6"]) == 1) & np.isin(M.num(m["p4_15"]), [1, 3])
    con = set(m.loc[varon_fuera, "llave_hog"].astype(str).str.strip())
    tiene = f["llave_hog"].astype(str).str.strip().isin(con).to_numpy()
    s = M.num(f["sexo"])
    jf = np.where(s == 2, 1.0, np.where(s == 1, 0.0, np.nan))
    f["_jf_con"] = np.where(tiene, jf, np.nan)
    f["_jf_sin"] = np.where(~tiene, jf, np.nan)
    f["_tiene"] = tiene
    return f


def mide(frames, R, M, replicas, semilla):
    muj, hog, mig = frames["MUJ"], frames["HOG"], frames["MIG"]
    diag = {"MUJ-FILAS-LEIDAS": int(len(muj))}
    fm, et_m, _ = M.prepara_diseno(muj, peso="fac_per", estrato="est_dis", upm="upm_dis")
    diag["MUJ-FILAS-DISENO-VALIDO"] = int(len(fm))
    fm = derivadas_mujeres(fm, M)
    ejes_m = {e: (M.eje_mapa(fm, col, mapa), EJES_MUJ[e]) for e, (col, mapa) in MAPAS_MUJ.items()}
    ejes_m["EDAD"] = (M.eje_rango(fm, "edad_muj", EDADES), EJES_MUJ["EDAD"])
    ejes_m = {e: ejes_m[e] for e in EJES_MUJ}
    edad = M.num(fm["edad_muj"])
    um = (edad >= 15) & (edad <= 54)
    diag["MUJ-FILAS-15-54"] = int(um.sum())
    jefes = hog[M.num(hog["paren"]) == 1].reset_index(drop=True)
    diag["HOG-FILAS-JEFATURA"] = int(len(jefes))
    fh, et_h, _ = M.prepara_diseno(jefes, peso="fac_viv", estrato="est_dis", upm="upm_dis")
    diag["HOG-FILAS-DISENO-VALIDO"] = int(len(fh))
    fh = derivadas_hogares(fh, mig, M)
    diag["HOG-CON-MIGRANTE-VARON"] = int(fh["_tiene"].sum())
    ejes_h = {e: (M.eje_mapa(fh, col, mapa), EJES_HOG[e]) for e, (col, mapa) in MAPAS_HOG.items()}
    out = {f"{P}-G-{k}": v for k, v in diag.items()}
    out.update(M.mide_ola(R, fm, COND_MUJ, ejes_m, P, OLA, replicas, semilla, universo=um))
    out.update(M.mide_ola(R, fh, COND_HOG, ejes_h, P, OLA, replicas, semilla, universo=None))
    out[f"{P}-G-DISENO-MUJERES"] = et_m
    out[f"{P}-G-DISENO-HOGARES"] = et_h
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    M = _modulo_desde_bytes("motor_pisos_confianza", inputs["motor_pisos_confianza"]["bytes"])
    ruta = inputs[PAY]["ruta_absoluta"]
    frames = {"MUJ": R.lee_csv_zip(ruta, list(COLS_MUJ), miembro=MIEMBROS["MUJ"]),
              "HOG": R.lee_csv_zip(ruta, list(COLS_HOG), miembro=MIEMBROS["HOG"]),
              "MIG": R.lee_csv_zip(ruta, list(COLS_MIG), miembro=MIEMBROS["MIG"])}
    out = mide(frames, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-ABIERTA"] = "ENADID 2018 -- 2023 RESERVADA para estas conductas (E.6); sin IC de persistencia"
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
    f += M.esquema_ola(P, OLA, COND_MUJ, EJES_MUJ)
    hog = M.esquema_ola(P, OLA, COND_HOG, EJES_HOG)
    for x in hog:
        if x["unidad"] == "personas sin ponderar":
            x["unidad"] = "hogares sin ponderar"
    f += hog
    f += [M.fila(f"{P}-G-DISENO-MUJERES", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-DISENO-HOGARES", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-ABIERTA", "texto", "declaración")]
    return f
