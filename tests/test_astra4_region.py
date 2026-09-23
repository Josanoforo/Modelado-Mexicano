"""Casos sintéticos que protegen el estimador regional antes del microdato."""
import math
import zipfile

import pandas as pd

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.historia import carga_enif, carga_envipe
from tools.astra.region.historia_v2 import carga_encig


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


def _zip_csv(path, miembros):
    with zipfile.ZipFile(path, "w") as z:
        for nombre, df in miembros.items():
            z.writestr(nombre, df.to_csv(index=False))


def test_adaptadores_conservan_geografia_y_unidad(tmp_path):
    encig = tmp_path / "encig.zip"
    _zip_csv(encig, {"encig2017_04_sec_7/conjunto_de_datos/encig2017_04_sec_7.csv": pd.DataFrame({
        "ENT": ["01", "02"], "N_TRA": ["01", "02"], "P7_3": ["4", "5"],
        "FAC_TRA": ["2", "3"], "EST_DIS": ["1", "1"], "UPM_DIS": ["1", "2"]})})
    d, geo, den, y, fac, dominios = carga_encig(encig, 2017)
    assert list(geo) == ["01", "02"] and list(den) == [True, False]
    assert list(y) == [True, False] and fac == "FAC_TRA" and len(dominios) == 32

    enif = tmp_path / "enif.zip"
    cols = {f"P5_1_{i}": ["2", "2"] for i in range(1, 7)}
    cols["P5_1_1"] = ["1", "1"]
    _zip_csv(enif, {"conjunto_de_datos_tmodulo_enif_2021.csv": pd.DataFrame({
        "REGION": ["1", "2"], "EDAD": ["70", "71"], "FAC_ELE": ["2", "3"],
        "EST_DIS": ["1", "1"], "UPM_DIS": ["1", "2"], **cols})})
    d, geo, den, y, fac, dominios = carga_enif(enif, 2021)
    assert list(geo) == ["1", "2"] and list(den) == [True, False]
    assert list(y) == [True, False] and fac == "FAC_ELE" and len(dominios) == 6

    envipe = tmp_path / "envipe.zip"
    _zip_csv(envipe, {
        "conjunto_de_datos_tmod_vic_envipe2023.csv": pd.DataFrame({
            "ID_PER": ["a", "b"], "BP1_20": ["2", "1"], "BP1_23": ["04", ""],
            "FAC_DEL": ["2", "3"], "EST_DIS": ["1", "1"], "UPM_DIS": ["1", "2"]}),
        "conjunto_de_datos_tsdem_envipe2023.csv": pd.DataFrame({
            "ID_PER": ["a", "b"], "CVE_ENT": ["01", "02"]}),
    })
    d, geo, den, y, fac, dominios = carga_envipe(envipe, 2023)
    assert list(geo) == ["01", "02"] and list(den) == [True, True]
    assert list(y) == [True, False] and fac == "FAC_DEL" and len(dominios) == 32
