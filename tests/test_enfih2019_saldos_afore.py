import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd


PATH = (Path(__file__).parents[1] / "data/corrida0" /
        "CALC-ENFIH2019-SALDOS-AFORE-0001/medidor.py")
SPEC = importlib.util.spec_from_file_location("saldo_afore", PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def _frames():
    conc = pd.DataFrame([
        ["1", "01", "1", "0", "0", "10", "001", "0000001", "1"],
        ["2", "01", "1", "1", "0", "20", "001", "0000002", "1"],
        ["3", "01", "1", "1", "100", "30", "002", "0000003", "1"],
        ["4", "01", "1", "1", "50", "40", "002", "0000004", "0"],
        ["5", "01", "1", "1", "0", "50", "003", "0000005", "1"],
    ], columns=MOD.CONC_COLS)
    module = pd.DataFrame([
        ["1", "01", "1", "1", "2", ""],
        ["2", "01", "1", "1", "1", "000000000"],
        ["3", "01", "1", "1", "1", "000000100"],
        ["4", "01", "1", "1", "1", "000000050"],
        ["4", "01", "1", "2", "1", "999999999"],
        ["5", "01", "1", "1", "1", "999999888"],
    ], columns=MOD.MOD_COLS)
    return conc, module


def test_codigos_especiales_no_son_dinero_y_cero_puede_ser_conocido():
    classified = MOD.classify_households(*_frames())
    assert classified["state"].tolist() == [
        "NO-TENEDOR", "CONOCIDO-CERO", "CONOCIDO-POSITIVO", "PARCIAL",
        "DESCONOCIDO-TOTAL",
    ]
    assert classified.loc[3, "v"] == 50
    assert not classified.loc[3, "complete"]


def test_cuantil_inversa_izquierda_y_monotonia():
    values = np.array([0, 10, 20, 100], dtype=float)
    weights = np.array([1, 2, 1, 1], dtype=float)
    qs = [MOD.weighted_quantile(values, weights, q) for q in (.25, .5, .75, .9)]
    assert qs == [10, 10, 20, 100]
    assert qs == sorted(qs)


def test_top_decil_reparte_empate_y_es_invariante_al_orden_y_escala():
    values = np.array([1, 10, 10, 2], dtype=float)
    weights = np.array([7, 2, 1, 10], dtype=float)
    expected = 20 / 57  # masa superior=2; se toma 2/3 del empate de saldo 10
    assert np.isclose(MOD.top_share_tied(values, weights), expected)
    assert np.isclose(MOD.top_share_tied(values[::-1], weights[::-1]), expected)
    assert np.isclose(MOD.top_share_tied(values * 1000, weights), expected)


def test_proporciones_invariantes_al_escalar_pesos():
    frame = MOD.classify_households(*_frames())
    w = pd.to_numeric(frame["FAC_HOG"]).to_numpy(float)
    a = MOD.calculate_points(frame, w)
    b = MOD.calculate_points(frame, w * 17)
    assert np.isclose(a["coverage"], b["coverage"])
    assert np.isclose(a["concentration"], b["concentration"])
    assert np.isclose(a["principal_mean"], b["principal_mean"])


def test_incoherencia_agregado_personas_es_error_material():
    conc, module = _frames()
    conc.loc[2, "V_AFORE"] = "101"
    try:
        MOD.classify_households(conc, module)
    except ValueError as exc:
        assert "suma" in str(exc)
    else:
        raise AssertionError("debio rechazar agregado incoherente")
