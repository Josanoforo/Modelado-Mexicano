import importlib.util
from pathlib import Path

import pandas as pd
import pytest


PATH = Path(__file__).parents[1] / "data/corrida0/CALC-ENADID-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("enadid_union", PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def fixture():
    rows = []
    statuses = ["1", "6", "2", "3", "4", "5", "7"]
    ages = [16, 20, 35, 50, 70]
    i = 0
    for stratum in ("001", "002"):
        for psu in ("00001", "00002"):
            for age in ages:
                for status in statuses:
                    i += 1
                    rows.append({
                        "LLAVE_PER": f"K{i:05d}", "EDAD": str(age),
                        "P3_27": status, "FAC_VIV": str(1 + (status == "1")),
                        "EST_DIS": stratum, "UPM_DIS": psu,
                    })
    return pd.DataFrame(rows)


def test_particiones_y_condicional_separados():
    rows, audit = MOD.calculate(fixture())
    total = [r for r in rows if r["estimando"] == "distribucion_actual_15_mas" and r["edad"] == "15_mas"]
    assert sum(r["punto"] for r in total) == pytest.approx(1.0)
    cond = [r for r in rows if r["estimando"] == "union_libre_entre_union_o_casada" and r["edad"] == "15_mas"]
    assert sum(r["punto"] for r in cond) == pytest.approx(1.0)
    assert cond[0]["punto"] != total[0]["punto"]
    assert cond[0]["n_desconocido"] == 0
    assert cond[0]["n_fuera_denominador"] > 0
    assert audit["perdida_enlace_n"] == 0


def test_llave_duplicada_aborta():
    frame = fixture()
    frame.loc[1, "LLAVE_PER"] = frame.loc[0, "LLAVE_PER"]
    with pytest.raises(ValueError, match="LLAVE-NO-UNICA"):
        MOD.calculate(frame)


def test_desconocidos_no_entran_como_negativos():
    frame = fixture()
    frame.loc[0, "P3_27"] = "9"
    rows, _ = MOD.calculate(frame)
    union = next(r for r in rows if r["estimando"] == "distribucion_actual_15_mas" and r["categoria"] == "union_libre" and r["edad"] == "15_17")
    assert union["n_desconocido"] == 1
    assert union["n_valido"] < union["n_expuesto"]
