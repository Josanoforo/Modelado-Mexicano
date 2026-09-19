import importlib.util
from pathlib import Path

import numpy as np


PATH = (Path(__file__).parents[1] / "data/corrida0" /
        "CALC-ENFIH2019-SALDOS-AFORE-CONCENTRACION-0001/medidor.py")
SPEC = importlib.util.spec_from_file_location("saldo_afore_concentracion", PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_control_minimo_cero_define_masa_del_decil():
    x = np.array([0.0, 10.0])
    w = np.array([1.0, 1.0])
    todos = np.array([True, True])
    positivos = x > 0
    assert np.isclose(MOD.top_share_by_mass(x, w, todos), 0.20)
    assert np.isclose(MOD.top_share_by_mass(x, w, positivos), 0.10)


def test_empates_e_invariancia_al_orden():
    x = np.array([0.0, 10.0, 10.0, 2.0])
    w = np.array([5.0, 2.0, 1.0, 12.0])
    domain = np.ones(4, dtype=bool)
    expected = 20.0 / 54.0
    assert np.isclose(MOD.top_share_by_mass(x, w, domain), expected)
    assert np.isclose(MOD.top_share_by_mass(x[::-1], w[::-1], domain), expected)


def test_invariancia_de_pesos_y_moneda():
    x = np.array([0.0, 4.0, 10.0, 100.0])
    w = np.array([3.0, 5.0, 2.0, 1.0])
    domain = np.ones(4, dtype=bool)
    base = MOD.top_share_by_mass(x, w, domain)
    assert np.isclose(MOD.top_share_by_mass(x, w * 17, domain), base)
    assert np.isclose(MOD.top_share_by_mass(x * 1000, w, domain), base)


def test_peso_de_aporte_cero_no_entra_al_dominio_efectivo():
    x = np.array([0.0, 10.0, 1_000_000.0])
    w = np.array([1.0, 1.0, 0.0])
    domain = np.ones(3, dtype=bool)
    assert np.isclose(MOD.top_share_by_mass(x, w, domain), 0.20)


def test_saldo_agregado_cero_no_es_estimable():
    x = np.array([0.0, 0.0])
    w = np.array([1.0, 2.0])
    domain = np.ones(2, dtype=bool)
    assert np.isnan(MOD.top_share_by_mass(x, w, domain))
