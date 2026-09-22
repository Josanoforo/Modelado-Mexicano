from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Recorte 18-70 del piso t-1 (ENIF 2021) de las conductas de crédito K1-K7.
Reusa el medidor SELLADO de #943 (CALC-DIN-CREDITO-PISOS-ENIF2021-0001)
BYTE A BYTE -- import por sha256, input `MEDIDOR-PISOS-ENIF2021-0001` --
y sólo envuelve dos puntos de extensión que ese medidor expone vía nombres
de módulo:

  - `_modulo_0003`: se sustituye por una versión que, tras cargar el marco
    con el medidor sellado de -0003 (también importado por bytes, sin
    cambio), filtra las filas a `EDAD` numérica en `[EDAD_MIN, EDAD_MAX]`
    ANTES de que ninguna otra parte del procedimiento la lea -- ni ejes, ni
    desenlaces, ni el marco de diseño se construyen sobre una fila fuera
    del recorte.
  - `PREFIJO`: se sustituye por un nombre propio para que los `RESULT-` de
    esta corrida no colisionen con los ya sellados de `#943` (que son otra
    medición, sobre universo 18+, no 18-70).

Ningún otro renglón de la lógica de conducta se reescribe ni se copia: es
literalmente el mismo código de `#943`, ejecutado con un marco más chico.
Spec: DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-spec-v1_0.md (§0: delta contra
la spec madre de `#943`).
"""
import types
from pathlib import Path
import pandas as pd

PREFIJO = "DIN-CREDITO-PISOS-ENIF2021-RECORTE1870"
EDAD_MIN = 18
EDAD_MAX = 70


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_p943(inputs):
    src = _bytes(inputs["MEDIDOR-PISOS-ENIF2021-0001"])
    mod = types.ModuleType("medidor_pisos_enif2021_0001")
    exec(compile(src, "medidor_pisos_enif2021_0001", "exec"), mod.__dict__)
    return mod


def _envolver_modulo_0003(modulo_0003_original, edad_min, edad_max):
    """Devuelve una versión de `_modulo_0003` que filtra EDAD en
    [edad_min, edad_max] justo después de leer el CSV, antes de que
    cualquier otra cosa (ejes, desenlaces, marco de diseño) vea la fila."""

    def _modulo_0003_recortado(inputs):
        m = modulo_0003_original(inputs)
        csv_original = m._csv

        def _csv_recortado(path, miembro, cols):
            d = csv_original(path, miembro, cols)
            edad = pd.to_numeric(d["EDAD"], errors="coerce")
            en_recorte = edad.notna() & edad.between(edad_min, edad_max)
            return d.loc[en_recorte].reset_index(drop=True)

        m._csv = _csv_recortado
        return m

    return _modulo_0003_recortado


def medir(inputs, contrato):
    p943 = _modulo_p943(inputs)
    p943._modulo_0003 = _envolver_modulo_0003(p943._modulo_0003, EDAD_MIN, EDAD_MAX)
    p943.PREFIJO = PREFIJO
    out = p943.medir(inputs, contrato)
    out[f"RESULT-{PREFIJO}-EDAD-RECORTE-MIN"] = EDAD_MIN
    out[f"RESULT-{PREFIJO}-EDAD-RECORTE-MAX"] = EDAD_MAX
    return out
