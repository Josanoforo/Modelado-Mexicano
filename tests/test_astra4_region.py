"""Casos sintéticos que protegen el estimador regional antes del microdato."""
import zipfile

import pandas as pd
import pytest

from tools.astra.region.estadistica import estima_dominios
from tools.astra.region.historia import carga_enif, carga_envipe
from tools.astra.region.historia_v2 import carga_encig
from tools.astra.region.historia_v3 import carga_enif as carga_enif_v3
from tools.astra.region.enif_portafolio import desenlaces
from tools.astra.region.envipe_complemento import complemento
from tools.astra.region.encig2025_consumidores import fuentes as fuentes_encig25, desenlaces as desenlaces_encig25


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
    assert filas[0]["punto"] == pytest.approx(2 / 6)
    assert filas[1]["punto"] == pytest.approx(8 / 10)
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

    enif18 = tmp_path / "enif18.zip"
    cols18 = {f"p5_1_{i}": ["2", "2"] for i in range(1, 7)}
    cols18["p5_1_1"] = ["1", "1"]
    _zip_csv(enif18, {"conjunto_de_datos/tmodulo.csv": pd.DataFrame({
        "region": ["1", "2"], "edad": ["70", "71"], "fac_per": ["2", "3"],
        "est_dis": ["1", "1"], "upm_dis": ["1", "2"], **cols18})})
    d, geo, den, y, fac, dominios = carga_enif_v3(enif18, 2018)
    assert list(geo) == ["1", "2"] and list(den) == [True, False]
    assert list(y) == [True, False] and fac == "FAC_PER" and len(dominios) == 6

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


def test_portafolio_enif_particion_y_complemento():
    cols = {f"P5_1_{i}": ["2"] * 5 for i in range(1, 7)}
    cols.update({f"P5_6_{i}": ["2"] * 5 for i in range(1, 10)})
    cols["P5_1_1"] = ["1", "2", "1", "2", ""]
    cols["P5_6_1"] = ["2", "1", "1", "2", ""]
    for k in cols:
        cols[k][-1] = ""
    den, y = desenlaces(pd.DataFrame(cols))
    assert list(den) == [True, True, True, True, False]
    assert list(y["ahorra_solo_informal"]) == [True, False, False, False, False]
    assert list(y["ahorra_solo_formal"]) == [False, True, False, False, False]
    assert list(y["ahorra_ambas_vias"]) == [False, False, True, False, False]
    assert list(y["no_ahorra"]) == [False, False, False, True, False]
    assert y["no_tiene_ahorros_enif2024"].equals(y["no_ahorra"])
    assert (y["ahorra_solo_informal"] | y["ahorra_solo_formal"] |
            y["ahorra_ambas_vias"] | y["no_ahorra"]).equals(den)


def test_complemento_envipe_invierte_intervalo_y_replicas():
    origen = {"geografia": "01", "n": 240, "n_numerador": 90,
              "punto": .4, "ic_inf": .3, "ic_sup": .5,
              "replicas_p": [.35, .45], "n_efectivo_kish": 200,
              "estado": "PUBLICABLE"}
    fila = complemento(origen)
    assert fila["punto"] == pytest.approx(.6)
    assert (fila["ic_inf"], fila["ic_sup"]) == pytest.approx((.5, .7))
    assert fila["replicas_p"] == pytest.approx([.65, .55])
    assert fila["n_numerador"] == 150 and fila["n"] == 240
    suprimida = {**origen, "estado": "SUPRIMIDA-N", "punto": None,
                 "ic_inf": None, "ic_sup": None, "replicas_p": None}
    assert complemento(suprimida)["punto"] is None


def test_encig2025_unidades_y_join_sin_deduplicar(tmp_path):
    z = tmp_path / "encig25.zip"
    _zip_csv(z, {
        "encig2025_01_sec1_A_3_4_5_8_9_10.csv": pd.DataFrame({
            "CVE_ENT": ["1", "2"], "P8_3_1": ["1", "2"], "FAC_P18": ["2", "3"],
            "EST_DIS": ["1", "1"], "UPM_DIS": ["1", "2"]}),
        "encig2025_04_sec_7.csv": pd.DataFrame({
            "ID_TRA": ["a", "a", "b", "c"], "CVE_ENT": ["1", "1", "2", "2"],
            "N_TRA": ["01", "01", "01", "02"], "P7_3": ["4", "4", "1", "3"],
            "FAC_TRA": ["2", "2", "3", "4"], "EST_DIS": ["1"]*4,
            "UPM_DIS": ["1", "1", "2", "2"]}),
        "encig2025_05_sec_8.csv": pd.DataFrame({
            "ID_TRA": ["a", "b", "c"], "P8_4": ["1", "0", "1"]}),
    })
    per, s7, g = fuentes_encig25(z)
    d = desenlaces_encig25(per, s7)
    assert g["sec7_sin_pareja_sec8"] == 0
    assert list(d["paga_mordida_encig2025"][2]) == [True, True]
    assert list(d["paga_mordida_encig2025"][3]) == [True, False]
    assert list(d["adopta_encig2025_luz"][3]) == [True, True, False, False]
    assert list(d["paga_mordida_encig2025_digital_r2"][3]) == [True, True, False, True]
    assert list(d["paga_mordida_encig2025_presencial_r2"][2]) == [False, False, True, False]


def test_ic_predictivo_usa_solo_ajuste_anterior_y_extremos():
    from tools.astra.region.ic_calibrado import _interval, _tau
    def fila(p, estado="PUBLICABLE"):
        return {"punto": p, "ic_inf": p - .05 if p is not None else None,
                "ic_sup": p + .05 if p is not None else None, "estado": estado}
    a = {"01": fila(.3), "02": fila(.4)}
    b = {"01": fila(.4), "02": fila(.5)}
    tau, counts = _tau([a, b])
    assert counts == [2] and tau > 0
    lo, hi = _interval(b["01"], tau)
    assert lo < .4 < hi and hi - lo > .1
    assert _interval(fila(0), tau) is None
    assert _interval(fila(.4, "SUPRIMIDA-N"), tau) is None
    # Una evaluación futura no se pasa a _tau; cambiarla no cambia el intervalo.
    assert _tau([a, b])[0] == tau


def test_enif_condicionales_separan_denominadores_y_guardias():
    from tools.astra.region.enif_condicionales import dominios_condicionales
    cols = {f"P5_4_{i}": ["2"] * 4 for i in range(1, 10)}
    d = pd.DataFrame({"EDAD_V": ["30"] * 4, "P4_10": ["1", "3", "2", "5"],
                      "P3_13": ["7", "7", "1", "1"],
                      "P5_20": ["03", "10", "03", "02"],
                      "P5_23": ["1", "1", "2", "2"], **cols})
    found = dominios_condicionales(d)
    assert list(found["horizonte_corto_sin_ss"][0]) == [True, True, False, False]
    assert list(found["horizonte_corto_sin_ss"][1]) == [True, False, False, False]
    assert list(found["desconfia_conoce_proteccion"][0]) == [True, True, False, False]
    assert list(found["desconfia_conoce_proteccion"][1]) == [True, False, False, False]
    d.loc[0, "P5_23"] = "b"
    with pytest.raises(RuntimeError, match="G-C1"):
        dominios_condicionales(d)


def test_enif_no_trabaja_aplica_particion_y_corte():
    from tools.astra.region.enif_no_trabaja import dominio
    d = pd.DataFrame({"P3_8": ["8", "8", "1"], "P3_9": ["7", "7", "1"],
                      "P4_10": ["1", "3", "2"]})
    den, y = dominio(d)
    assert list(den) == [True, True, False]
    assert list(y) == [True, False, False]
    d.loc[0, "P3_8"] = "1"
    with pytest.raises(RuntimeError, match="no particionan"):
        dominio(d)


def test_envipe_u4_colapsa_delitos_en_personas():
    from tools.astra.region.envipe_denuncia_persona import universo
    mod = pd.DataFrame({"ID_PER": ["a", "a", "b", "c"],
        "BPCOD": ["05", "06", "15", "04"],
        "BP1_20": ["2", "2", "2", "2"],
        "BP1_23": ["03", "08", "04", "01"]})
    per = pd.DataFrame({"ID_PER": ["a", "b", "c"]})
    den, y = universo(mod, per)
    assert list(den) == [True, True, False]
    assert list(y) == [True, False, False]


def test_envipe_seguro_separa_estratos_y_complementos_contados():
    from tools.astra.region.envipe_seguro import dominios
    d = pd.DataFrame({"BPCOD": ["01", "01", "01", "01", "05"],
                      "BP2_1": ["1", "1", "2", "2", "1"],
                      "BP1_20": ["1", "2", "1", "2", "1"]})
    cells = dominios(d)
    assert list(cells["denuncia_con_seguro"][0]) == [True, True, False, False, False]
    assert list(cells["denuncia_con_seguro"][1]) == [True, False, False, False, False]
    assert list(cells["no_denuncia_con_seguro"][1]) == [False, True, False, False, False]
    assert list(cells["denuncia_sin_seguro"][1]) == [False, False, True, False, False]
