import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd


PATH = Path(__file__).parents[1] / "data/corrida0/CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("enutpi", PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def row(key, sex="1", age="30", weight="1", value="0", stratum="0001", psu="00001"):
    out = {"LLAVEMOD": key, "SEXO": sex, "EDAD": age, "FAC_PER": weight,
           "EST_DIS": stratum, "UPM_DIS": psu}
    out.update({col: value for col in M.CON + M.SIN})
    return out


def test_cero_es_valido_y_faltante_no_se_imputa():
    rows = [row("a", value="0"), row("b", value="1", psu="00002"), row("c", value="", psu="00003")]
    valid, incidence, marco = M.prepare_frame(pd.DataFrame(rows))
    assert len(marco) == 3
    assert len(valid) == 2
    assert valid.loc[valid.LLAVEMOD.eq("a"), "h_con_cp"].iat[0] == 0
    assert incidence["filas_fuera_universo_comun"] == 1


def test_fac_per_es_ponderador_de_persona():
    valid, _, marco = M.prepare_frame(pd.DataFrame([
        row("a", sex="1", weight="1", value="0", psu="00001"),
        row("b", sex="1", weight="9", value="1", psu="00002"),
        row("c", sex="2", weight="1", value="1", psu="00003"),
    ]))
    estimates, _, _, error = M.analyse(valid, marco, 20, 7)
    idx = {(r["variante"], r["desglose"], r["grupo"], r["medida"]): r for r in estimates}
    assert np.isclose(idx[("CON_CP", "sexo", "hombre", "participacion")]["estimacion"], .9)
    assert error < 1e-12


def test_grupo_sin_participantes_es_no_estimable_no_cero():
    valid, _, marco = M.prepare_frame(pd.DataFrame([
        row("a", sex="1", value="0", psu="00001"),
        row("b", sex="2", value="1", psu="00002"),
    ]))
    estimates, _, _, _ = M.analyse(valid, marco, 20, 9)
    target = next(r for r in estimates if r["variante"] == "CON_CP" and
                  r["desglose"] == "sexo" and r["grupo"] == "hombre" and
                  r["medida"] == "media_participantes")
    assert target["estimacion"] is None
    assert target["estado"] == "NO-ESTIMABLE"


def test_llave_persona_duplicada_para():
    with np.testing.assert_raises_regex(ValueError, "LLAVEMOD"):
        M.prepare_frame(pd.DataFrame([row("a"), row("a", psu="00002")]))
