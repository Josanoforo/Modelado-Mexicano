"""Casos sintéticos que protegen el estimador regional antes del microdato."""
import math

import pandas as pd

from tools.astra.region.estadistica import estima_dominios


def marco():
    # La UPM "1" se repite entre estratos: su llave real es (estrato, UPM).
    return pd.DataFrame({
        "est": ["a"] * 4 + ["b"] * 4,
        "upm": ["1", "1", "2", "2"] * 2,
        "w": [1, 1, 2, 2, 1, 1, 4, 4],
    })


def test_razon_ponderada_y_plan_compartido():
    d = marco()
    geo = pd.Series(["X", "X", "X", "X", "Y", "Y", "Y", "Y"])
    den = pd.Series([True] * 8)
    y = pd.Series([True, True, False, False, False, False, True, True])
    filas, meta = estima_dominios(d, geo, den, y, factor="w", estrato="est",
                                  upm="upm", dominios=["X", "Y"],
                                  representativos={"X", "Y"}, semilla=42,
                                  replicas=256, n_min=1)
    assert meta["upm_marco"] == 4
    assert math.isclose(filas[0]["punto"], 2 / 6)
    assert math.isclose(filas[1]["punto"], 8 / 10)
    assert all(f["estado"] == "PUBLICABLE" for f in filas)
    assert all(f["ic_inf"] <= f["punto"] <= f["ic_sup"] for f in filas)


def test_supresion_y_representatividad_no_se_convierten_en_cero():
    d = marco()
    geo = pd.Series(["X"] * 4 + ["Y"] * 4)
    den = pd.Series([True] * 8)
    y = pd.Series([True, True, False, False] * 2)
    filas, _ = estima_dominios(d, geo, den, y, factor="w", estrato="est",
                               upm="upm", dominios=["X", "Y"],
                               representativos={"X"}, semilla=42,
                               replicas=32, n_min=5)
    assert filas[0]["estado"] == "SUPRIMIDA-N"
    assert filas[1]["estado"] == "NO-REPRESENTATIVA"
    assert all(f["punto"] is None and f["ic_inf"] is None for f in filas)


def test_denominador_vacio_y_varianza_degenerada():
    d = marco()
    geo = pd.Series(["X"] * 8)
    den = pd.Series([False] * 8)
    y = pd.Series([False] * 8)
    filas, _ = estima_dominios(d, geo, den, y, factor="w", estrato="est",
                               upm="upm", dominios=["X"],
                               representativos={"X"}, semilla=42,
                               replicas=32, n_min=1)
    assert filas[0]["estado"] == "SUPRIMIDA-N"
    den[:] = True
    y[:] = True
    filas, _ = estima_dominios(d, geo, den, y, factor="w", estrato="est",
                               upm="upm", dominios=["X"],
                               representativos={"X"}, semilla=42,
                               replicas=32, n_min=1)
    assert filas[0]["estado"] == "VARIANZA-NO-ESTIMABLE"
    assert filas[0]["punto"] is None
