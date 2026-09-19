import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd


PATH = Path(__file__).parents[1] / "data/corrida0/CALC-ENUT2024-DISTRIBUCION-HORAS-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("enutdh", PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def row(key, sex="1", age="30", weight="1", value="0", stratum="0001", psu="00001"):
    out = {"LLAVEMOD": key, "SEXO": sex, "EDAD": age, "FAC_PER": weight,
           "EST_DIS": stratum, "UPM_DIS": psu}
    out.update({col: value for col in M.CON + M.SIN})
    return out


def test_ceros_validos_y_desconocidos_excluidos():
    valid, incidence, universe, design = M.prepare_frame(pd.DataFrame([
        row("a", value="0"), row("b", value="1", psu="00002"),
        row("c", value="", psu="00003"),
    ]))
    assert (len(valid), len(universe), len(design)) == (2, 3, 3)
    assert valid.loc[valid.LLAVEMOD.eq("a"), "h_con_cp"].iat[0] == 0
    assert incidence["filas_fuera_universo_comun"] == 1


def test_cuantiles_ponderados_monotonos_y_sin_interpolacion():
    result = M.distribution_measures(np.array([0., 5., 20.]), np.array([6., 3., 1.]))
    assert [result[q] for q in ("p25", "p50", "p75", "p90")] == [0., 0., 5., 5.]


def test_empates_e_invariancia_al_orden():
    values = np.array([10., 10., 0., 2.])
    weights = np.array([1., 3., 4., 2.])
    expected = M.top_mass_hour_share(values, weights)
    for order in (np.array([3, 2, 1, 0]), np.array([1, 0, 3, 2])):
        assert np.isclose(M.top_mass_hour_share(values[order], weights[order]), expected)


def test_concentracion_acotada_y_caso_dos_personas():
    all_people = M.top_mass_hour_share(np.array([0., 10.]), np.ones(2))
    participants = M.top_mass_hour_share(np.array([10.]), np.ones(1))
    assert np.isclose(all_people, .20)
    assert np.isclose(participants, .10)
    assert 0 <= all_people <= 1 and 0 <= participants <= 1


def test_escalamiento_de_pesos_y_horas():
    values, weights = np.array([0., 2., 7.]), np.array([1., 4., 2.])
    base = M.distribution_measures(values, weights)
    weight_scaled = M.distribution_measures(values, 11 * weights)
    hour_scaled = M.distribution_measures(3 * values, weights)
    for measure in M.MEASURES:
        assert np.isclose(base[measure], weight_scaled[measure])
    assert np.isclose(base["concentracion_decil_superior"], hour_scaled["concentracion_decil_superior"])
    for q in ("p25", "p50", "p75", "p90"):
        assert np.isclose(3 * base[q], hour_scaled[q])


def test_mediana_y_concentracion_son_controles_separados():
    a = M.distribution_measures(np.array([0., 1., 1.]), np.ones(3))
    b = M.distribution_measures(np.array([0., 1., 100.]), np.ones(3))
    assert a["p50"] == b["p50"] == 1
    assert not np.isclose(a["concentracion_decil_superior"], b["concentracion_decil_superior"])


def test_replicas_focales_deterministas_y_pareadas():
    frame = pd.DataFrame([
        row("a", sex="1", value="0", psu="01"),
        row("b", sex="1", value="2", psu="02"),
        row("c", sex="2", value="4", psu="03"),
        row("d", sex="2", value="8", psu="04"),
    ])
    valid, _, universe, design = M.prepare_frame(frame)
    first = M.analyse(valid, universe, design, 25, 77)
    second = M.analyse(valid, universe, design, 25, 77)
    assert first == second
    estimates, contrasts, _ = first
    target = next(r for r in contrasts if r["tipo"] == "mujer_menos_hombre" and
                  r["dominio"] == "todas_validas" and r["medida"] == "p90")
    assert target["estimacion"] == 24.0  # four identical components per row
    assert target["replicas_validas"] > 0
