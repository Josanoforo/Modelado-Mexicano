import importlib.util
from pathlib import Path

import pandas as pd
import pytest


PATH = Path(__file__).parents[1] / "data/corrida0/CALC-ENADID2023-UNION-SEXO-EDAD-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("enadid_union_sexo_edad", PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def fixture():
    rows = []
    i = 0
    for stratum in ("001", "002", "003"):
        for psu in ("00001", "00002", "00003"):
            for sex in ("1", "2"):
                for age in (16, 22, 36, 51, 70):
                    for status in ("1", "6", "2", "3", "4", "5", "7"):
                        i += 1
                        rows.append({"LLAVE_PER": f"K{i:06d}", "SEXO": sex,
                                     "EDAD": str(age), "P3_27": status,
                                     "FAC_VIV": str(1 + (sex == "2") + (status == "1")),
                                     "EST_DIS": stratum, "UPM_DIS": psu})
    return pd.DataFrame(rows)


def calculate(frame=None):
    return MOD.calculate(fixture() if frame is None else frame, replicates=120, seed=17)


def test_categorias_exhaustivas_y_reconstruccion_con_residuo():
    frame = fixture()
    extra = frame.iloc[[0]].copy()
    extra["LLAVE_PER"] = "RESIDUO"
    extra["SEXO"] = "9"
    result = calculate(pd.concat([frame, extra], ignore_index=True))
    rows = [r for r in result["distribucion"] if r["sexo"] == "mujer" and r["edad"] == "15_mas"]
    assert sum(r["punto"] for r in rows) == pytest.approx(1.0)
    total_num = sum(r["masa_numerador"] for r in result["distribucion"]
                    if r["edad"] == "15_mas")
    parent_den = sum(r["masa_numerador"] for r in result["distribucion"]
                     if r["sexo"] in ("hombre", "mujer", "sexo_desconocido")
                     and r["edad"] == "15_mas")
    assert total_num == pytest.approx(parent_den)
    residue = [r for r in result["distribucion"] if r["sexo"] == "sexo_desconocido"]
    assert any(r["n_numerador"] == 1 for r in residue)


def test_desconocido_no_es_fuera_denominador():
    frame = fixture()
    frame.loc[0, "P3_27"] = "9"
    result = calculate(frame)
    row = next(r for r in result["union"] if r["tipo"] == "tasa" and
               r["sexo"] == "hombre" and r["edad"] == "15_17")
    assert row["n_desconocido"] == 1
    assert row["n_fuera_denominador"] > 0
    assert row["n_denominador"] + row["n_fuera_denominador"] + row["n_desconocido"] == row["n_expuesto"]


def test_denominador_vacio_permanece_no_estimable():
    frame = fixture()
    mask = (frame["SEXO"] == "1") & (frame["EDAD"] == "16")
    frame.loc[mask, "P3_27"] = "7"
    result = calculate(frame)
    row = next(r for r in result["union"] if r["tipo"] == "tasa" and
               r["sexo"] == "hombre" and r["edad"] == "15_17")
    assert row["punto"] is None
    assert row["precision_estado"] == "NO-ESTIMABLE:DENOMINADOR-NULO"


def test_estandar_comun_y_bruta_distinta_de_estandarizada():
    frame = fixture()
    # Composición extrema por sexo sin eliminar soporte: mujeres pesan más en
    # edades mayores y hombres en jóvenes; las tasas por edad siguen definidas.
    age = pd.to_numeric(frame["EDAD"])
    frame.loc[(frame["SEXO"] == "1") & (age < 30), "FAC_VIV"] = "20"
    frame.loc[(frame["SEXO"] == "2") & (age >= 60), "FAC_VIV"] = "20"
    result = calculate(frame)
    weights = [r for r in result["estandarizacion"] if r["tipo"] == "peso_estandar_edad"]
    assert sum(r["punto"] for r in weights) == pytest.approx(1.0)
    gross = next(r for r in result["estandarizacion"] if r["tipo"] == "diferencia_bruta")
    standardized = next(r for r in result["estandarizacion"] if r["tipo"] == "diferencia_estandarizada")
    assert gross["punto"] != pytest.approx(standardized["punto"])


def test_llave_duplicada_aborta():
    frame = fixture()
    frame.loc[1, "LLAVE_PER"] = frame.loc[0, "LLAVE_PER"]
    with pytest.raises(ValueError, match="LLAVE-NO-UNICA"):
        calculate(frame)
