from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

CONGELADO SIN CORRER (COMMIT-1 de esta pieza). Este módulo es el ÚNICO
código autorizado a tocar la sección de crédito de ENIF 2024 (E.6:
"el único código autorizado a tocar la ola reservada se congela en
COMMIT-1 con guardia de una sola variable de agrupación"). Quien lo
congela NO lo ejecuta (F3 del encargo): el COMMIT-2 (abrir 2024, extraer
los marginales reales) y el COMMIT-3 (adjudicar contra las emisiones ya
selladas de `CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001`, componer
C2 de cruces) corren en OTRA sesión.

**Guardia de una variable** (`abre_conducta_2024`): la única función de
este módulo que toca `enif2024_csv` exige una y sólo una `conducta_id` de
la lista blanca ya congelada (`CONDUCTAS_AUTORIZADAS`, idéntica a
`ENTERING` de -EMISIONES-0001); llamarla con cualquier otra cosa --lista,
`"*"`, una conducta no listada-- lanza `ReservaRota` antes de leer una
sola fila. No hay función que abra "todo" el módulo de 2024 a la vez.

**Códigos desde el descriptor, sin abrir microdato (A.15).** El mapa
`COLUMNA_2024` de abajo se derivó leyendo `diccionario_de_datos_tmodulo_
enif2024.csv` y los catálogos `catalogos/*.csv` dentro de `enif2024_csv`
(estructura y etiquetas, CERO filas de `conjunto_de_datos_tmodulo_
enif2024.csv` abiertas) -- ver spec.md §1 para la cita fila por fila.
2024 renombró varias variables respecto de 2021 (P6_14→P6_13,
P6_15→P6_14, P6_17→P6_16, P6_4_k→P6_3_k, EDAD→edad_v, FAC_ELE→fac_per,
P3_1_1→niv/gra) -- un "nemónico desplazado" que A.15 exige declarar, no
inferir del nombre.

La extracción reusa `_cells`/`_estimate` de `tools/corrida0/CALC-PISOS-
ENIF2021-EJES-0003/medidor.py` (importado por bytes, sha256 -- mismo
input `MEDIDOR-EJES-0003` que -RECORTE1870-0001 y -EMISIONES ya citan
indirectamente) para que el marco de réplicas sea el mismo linaje que el
resto de la serie.

**La REGLA de adjudicación (comparar contra las emisiones, IC, veredicto)
es COMMIT-3, no este archivo** (encargo §3: "C2 no existe hasta abrir los
marginales... se compone dentro del COMMIT-3"; `cruces_familia.py::adjudica`
usa réplicas bootstrap por celda que esta serie de pisos no tiene --
propagación analítica en logit, como el resto de esta pieza-- así que
forzar su contrato aquí sería incoherente con el método ya sellado de
-EMISIONES; la regla de comparación se diseña en COMMIT-3 con las dos
cosas ya abiertas). Este módulo se detiene en: abrir UNA conducta,
construir su tabla de 18 celdas, y devolverla -- comparar es de otro
commit.
"""
import types
from pathlib import Path

import pandas as pd

PREFIJO = "DIN-CREDITO-PREDICCION-2024-ADJ"
EDAD_MIN, EDAD_MAX = 18, 70          # mismo recorte que -RECORTE1870-0001
MIEMBRO_2024 = "conjunto_de_datos_tmodulo_enif2024.csv"

# conducta -> (unidad, columnas de producto 2024, código(s) "tenido")
# Derivado de data/credito-comparabilidad-texto-v1_1.tsv fila ola=2024
# (K1/K2/K3/K5/K6: CAMBIO-MENOR o MISMO-INSTRUMENTO; K4: CAMBIO-MENOR) y
# del diccionario 2024 (spec.md §1). Idéntica lista blanca que ENTERING
# de CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001.
CONDUCTAS_AUTORIZADAS = ("K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ",
                         "K3", "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES")

# Columnas 2021 (medidor sellado de #943) -> columnas 2024 (este descriptor).
# "None" = no aplica a esa conducta.
COLUMNA_2024 = {
    "PRODUCTOS": [f"p6_2_{k}" for k in range(1, 10)],   # mismos códigos 1/2
    "ATRASOS": [f"p6_3_{k}" for k in range(1, 10)],      # 2021 P6_4_k -> 2024 P6_3_k
    "INFORMALES": [f"p6_1_{k}" for k in range(1, 6)],    # mismos códigos 1/2
    "P6_7_EQUIV": None,                                  # K7 no entra (no lo mide -EMISIONES)
    "P6_14_EQUIV": "p6_13",                              # 2021 P6_14 (alguna vez tuvo) -> 2024 P6_13
    "P6_15_EQUIV": "p6_14",                              # 2021 P6_15 (motivo nunca tuvo) -> 2024 P6_14
    "P6_17_EQUIV": "p6_16",                              # 2021 P6_17 (rechazo) -> 2024 P6_16, mismos códigos 1/2/3
    "SEXO": "sexo", "EDAD": "edad_v", "TLOC": "tloc",
    "FAC_ELE": "fac_per", "EST_DIS": "est_dis", "UPM_DIS": "upm_dis",
    "P3_10": "p3_10",                                    # mismos códigos 1..6
}

# niv (2024, 00-11 + 99) -> los mismos cuatro cubos que _school() usaba
# sobre P3_1_1 (2021, 0-9). Derivado comparando catalogos/niv.csv 2024
# contra el mapa de -0003 (spec.md §1): 00-02 -> hasta_primaria (Ninguno/
# Preescolar/Primaria), 03 -> secundaria, 04-07 -> media_superior (Normal
# básica/técnicos/preparatoria), 08-11 -> superior (Licenciatura..Doctorado).
NIV_A_ESCOLARIDAD = {
    "00": "hasta_primaria", "01": "hasta_primaria", "02": "hasta_primaria",
    "03": "secundaria",
    "04": "media_superior", "05": "media_superior", "06": "media_superior", "07": "media_superior",
    "08": "superior", "09": "superior", "10": "superior", "11": "superior",
}


class ReservaRota(Exception):
    """La guardia de una variable rechazó la llamada (E.6)."""


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_0003(inputs):
    src = _bytes(inputs["MEDIDOR-EJES-0003"])
    mod = types.ModuleType("medidor_ejes_0003_adj")
    exec(compile(src, "medidor_ejes_0003_adj", "exec"), mod.__dict__)
    return mod


def _csv_2024(m, ruta_absoluta, cols):
    """Lee EXACTAMENTE las columnas pedidas del TMODULO 2024 (minúsculas,
    A.15) -- nunca el archivo completo en un DataFrame sin acotar."""
    return m._csv(ruta_absoluta, MIEMBRO_2024, cols)


def abre_conducta_2024(inputs: dict, conducta_id: str, contrato: dict) -> dict:
    """ÚNICA función de este módulo que lee `enif2024_csv`. `conducta_id`
    debe ser un str de CONDUCTAS_AUTORIZADAS -- ni lista, ni "*", ni una
    conducta fuera de la lista blanca. PARA con ReservaRota antes de abrir
    el ZIP si la guardia no se cumple."""
    if not isinstance(conducta_id, str) or conducta_id not in CONDUCTAS_AUTORIZADAS:
        raise ReservaRota(
            f"conducta {conducta_id!r} no está en la lista blanca congelada "
            f"en COMMIT-1: {CONDUCTAS_AUTORIZADAS}"
        )
    m = _modulo_0003(inputs)
    C = COLUMNA_2024
    cols_base = [C["SEXO"], C["EDAD"], C["TLOC"], "niv", C["P3_10"],
                 C["FAC_ELE"], C["EST_DIS"], C["UPM_DIS"]]

    if conducta_id == "K1":
        cols = C["PRODUCTOS"] + [C["P6_14_EQUIV"]] + cols_base
    elif conducta_id in ("K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ"):
        idx = {"K2-DEPARTAMENTAL": 0, "K2-NOMINA": 2, "K2-AUTOMOTRIZ": 4}[conducta_id]
        cols = [C["PRODUCTOS"][idx]] + cols_base
    elif conducta_id == "K3":
        cols = C["INFORMALES"] + cols_base
    elif conducta_id in ("K4A-AUTOEXCLUSION", "K4B-OFERTA"):
        cols = C["PRODUCTOS"] + [C["P6_14_EQUIV"], C["P6_15_EQUIV"]] + cols_base
    elif conducta_id == "K5":
        cols = [C["P6_17_EQUIV"]] + cols_base
    elif conducta_id == "K6-P-TENEDORES":
        cols = C["PRODUCTOS"] + C["ATRASOS"] + cols_base
    else:  # inalcanzable: ya lo bloqueó la guardia de arriba
        raise ReservaRota(conducta_id)

    ruta = inputs["enif2024_csv"]["ruta_absoluta"]
    d = _csv_2024(m, ruta, sorted(set(cols)))

    edad = pd.to_numeric(d[C["EDAD"]], errors="coerce")
    d = d.loc[edad.notna() & edad.between(EDAD_MIN, EDAD_MAX)].reset_index(drop=True)

    d["_w"] = pd.to_numeric(d[C["FAC_ELE"]], errors="coerce")
    d["_est"] = d[C["EST_DIS"]].astype(str).str.strip()
    d["_upm"] = d[C["UPM_DIS"]].astype(str).str.strip()
    code = {c: m._code(d[c]) for c in set(cols) if c not in (C["FAC_ELE"], C["EST_DIS"], C["UPM_DIS"])}

    ejes = {
        "sexo": code[C["SEXO"]].where(code[C["SEXO"]].isin(["1", "2"]), pd.NA),
        "edad": m._age(d[C["EDAD"]]),
        "escolaridad": code["niv"].map(NIV_A_ESCOLARIDAD),
        "localidad": code[C["TLOC"]].map({"1": "15 000 y mas", "2": "15 000 y mas",
                                          "3": "menor de 15 000", "4": "menor de 15 000"}),
        "formalidad": pd.Series(pd.NA, index=d.index, dtype="object"),
    }
    ejes["formalidad"].loc[code[C["P3_10"]].isin(list("12345"))] = "con seguridad social"
    ejes["formalidad"].loc[code[C["P3_10"]].eq("6")] = "sin seguridad social"

    return {"marco": d, "codigos": code, "ejes": ejes, "conducta": conducta_id}


def _dicot(code, unos, ceros):
    out = pd.Series(pd.NA, index=code.index, dtype="Float64")
    out.loc[code.isin(list(ceros))] = 0.0
    out.loc[code.isin(list(unos))] = 1.0
    return out


def _desenlace(abierto: dict) -> pd.Series:
    """El mismo código de desenlace que #943 (CALC-DIN-CREDITO-PISOS-
    ENIF2021-0001) y -RECORTE1870-0001, sobre las columnas 2024 ya
    traducidas por COLUMNA_2024 -- misma dicotomización, mismos códigos
    (1/2 en 2024 == 1/2 en 2021 para cada una de estas conductas,
    verificado contra los catálogos del descriptor, spec.md §1)."""
    cid = abierto["conducta"]
    c = abierto["codigos"]
    C = COLUMNA_2024
    if cid == "K1":
        pr = pd.concat([c[col] for col in C["PRODUCTOS"]], axis=1)
        tenedor = pr.eq("1").any(axis=1)
        sin_producto = pr.eq("2").all(axis=1)
        y = pd.Series(pd.NA, index=pr.index, dtype="Float64")
        y.loc[sin_producto] = 0.0
        y.loc[tenedor] = 1.0
        return y
    if cid in ("K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ"):
        idx = {"K2-DEPARTAMENTAL": 0, "K2-NOMINA": 2, "K2-AUTOMOTRIZ": 4}[cid]
        return _dicot(c[C["PRODUCTOS"][idx]], "1", "2")
    if cid == "K3":
        inf = pd.concat([c[col] for col in C["INFORMALES"]], axis=1)
        y = pd.Series(pd.NA, index=inf.index, dtype="Float64")
        y.loc[inf.eq("2").all(axis=1)] = 0.0
        y.loc[inf.eq("1").any(axis=1)] = 1.0
        return y
    if cid in ("K4A-AUTOEXCLUSION", "K4B-OFERTA"):
        pr = pd.concat([c[col] for col in C["PRODUCTOS"]], axis=1)
        sin_producto = pr.eq("2").all(axis=1)
        nunca = sin_producto & c[C["P6_14_EQUIV"]].eq("2")
        p_motivo = c[C["P6_15_EQUIV"]].where(nunca, "")
        unos = {"K4A-AUTOEXCLUSION": "67", "K4B-OFERTA": "123"}[cid]
        ceros = "".join(sorted(set("123456789") - set(unos)))
        return _dicot(p_motivo, unos, ceros)
    if cid == "K5":
        return _dicot(c[C["P6_17_EQUIV"]], "1", "23")
    if cid == "K6-P-TENEDORES":
        pr = pd.concat([c[col] for col in C["PRODUCTOS"]], axis=1)
        at = pd.concat([c[col] for col in C["ATRASOS"]], axis=1)
        tenedor = pr.eq("1").any(axis=1)
        held = pr.eq("1").to_numpy()
        at_held = at.where(held, "")
        y = pd.Series(pd.NA, index=pr.index, dtype="Float64")
        y.loc[tenedor & (at_held.eq("2").to_numpy() | ~held).all(axis=1)] = 0.0
        y.loc[tenedor & at_held.eq("1").any(axis=1)] = 1.0
        return y
    raise ReservaRota(cid)  # inalcanzable: la lista blanca ya lo filtró


def medir(inputs: dict, contrato: dict) -> dict:
    """Recorre las 9 conductas de la lista blanca, UNA llamada guardada a
    `abre_conducta_2024` por conducta (nunca una lectura de todas las
    columnas de golpe), y estima sus 18 celdas con el marco de -0003
    (mismas 10 000 réplicas PCG64(42) que la serie histórica completa,
    A-bis 3: comparable por construcción)."""
    m = _modulo_0003(inputs)
    out = {}
    for cid in CONDUCTAS_AUTORIZADAS:
        abierto = abre_conducta_2024(inputs, cid, contrato)
        d = abierto["marco"]
        ejes = abierto["ejes"]
        y = _desenlace(abierto)

        todos = pd.Series("todos", index=d.index, dtype="object")
        trabaja = pd.Series("universo trabaja", index=d.index, dtype="object").where(
            ejes["formalidad"].notna(), pd.NA)
        axes = {"nacional": (todos, ("todos",)),
                "sexo": (ejes["sexo"], ("1", "2")),
                "edad": (ejes["edad"], ("18-29", "30-44", "45-59", "60+")),
                "escolaridad": (ejes["escolaridad"],
                                ("hasta_primaria", "secundaria", "media_superior", "superior")),
                "localidad": (ejes["localidad"], ("menor de 15 000", "15 000 y mas")),
                "formalidad": (ejes["formalidad"], ("sin seguridad social", "con seguridad social")),
                "universo": (trabaja, ("universo trabaja",))}
        cells = m._cells(f"{PREFIJO}-{cid}", y, axes)
        r = m._estimate(d, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                        int(contrato["seed"]["valor"]))
        out.update(r)
        out[f"RESULT-{PREFIJO}-{cid}-N-UNIVERSO"] = int(y.notna().sum())
        out[f"RESULT-{PREFIJO}-{cid}-FILAS-18-70"] = int(len(d))
    return out
