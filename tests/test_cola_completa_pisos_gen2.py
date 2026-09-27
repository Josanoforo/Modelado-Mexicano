"""D-22 de ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026): pisos por segmento de nueve CALC (ENDISEG 2021,
MMSI 2016, Latinobarómetro 2023 complemento, Intercensal 2015, ENASEM 2021, ENADID 2018, PEW 2024,
ENVIPE 2024, ENOE 2024T4).

Specs: forense/prereg-caja/COLA-*-spec-v1_0.md §5. Sintético sin microdato: todas las ramas
terminales (con soporte, conducta sin soporte, categoría vacía, fuera de universo, código de no
respuesta, peso faltante, derivadas con faltantes) pasan el conducto que sella
(`corrida0._valida_outputs`) sin NaN ni inf, y `resultados:` del spec.yaml es exactamente
`esquema_resultados()`. Guardias: una ola reservada o un instrumento excluido entre los inputs PARA.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_salud_cola_test")
M = _load("tools/dominios/confianza/motor_pisos.py", "motor_pisos_confianza_cola_test")
CALCS = ("CALC-ENDISEG-PISOS-2021-0001", "CALC-MMSI-PISOS-2016-0001", "CALC-LATINOBAROMETRO-COLA-2023-0001",
         "CALC-EIC-HOGARES-2015-0001", "CALC-ENASEM-ESCOLARIDAD-2021-0001", "CALC-ENADID-COLA-2018-0001",
         "CALC-PEW-RELIGION-2024-0001", "CALC-ENVIPE-PERCEPCION-2024-0001", "CALC-ENOE-PARTICIPACION-2024T4-0001")
MOD = {c: _load(f"data/corrida0/{c}/medidor.py", "m_" + c.replace("-", "_")) for c in CALCS}
REPS = 20


def _cierra(mod, out, extra):
    out.update({f"{mod.P}-G-BOOTSTRAP-REPLICAS": REPS, f"{mod.P}-G-SEED": 1})
    for k in sorted(mod.INPUTS_REPO):
        out[f"{mod.P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = "0" * 64
    out.update(extra)
    assert corrida0._valida_outputs({"resultados": mod.esquema_resultados()}, out) == []
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k
    return out


def _frame(rng, n, cols, rangos):
    d = {}
    for c in cols:
        lo, hi = rangos.get(c.lower(), (0, 9))
        d[c.lower()] = rng.integers(lo, hi + 1, n).astype(float)
    f = pd.DataFrame(d)
    f.iloc[:3, :] = np.nan  # no respuesta / blanco
    return f


def _diseno(extra=None):
    r = {"factor": (1, 50), "est_dis": (1, 6), "upm_dis": (1, 60)}
    r.update(extra or {})
    return r


def test_endiseg_derivadas_y_conducto():
    m = MOD["CALC-ENDISEG-PISOS-2021-0001"]
    rng = np.random.default_rng(1)
    r = _diseno({"p4_1": (12, 96), "p8_1": (1, 6), "p9_1": (1, 5), "p7_1": (1, 2), "p7_1a": (1, 3),
                 "niv": (0, 10), "p4_2": (1, 6), "p4_7": (1, 2), "p4_4": (1, 2), "ent": (1, 32)})
    f = _frame(rng, 600, m.columnas(), r)
    f.loc[f["ent"] == 7, "ent"] = np.nan  # entidad sin casos → categoría vacía
    d = m.derivadas(f.assign(p8_1=[4, 1, 5, 4] + [4] * 596, p9_1=[1, 1, 3, 2] + [1] * 596,
                             p7_1=[1, 1, 2, 1] + [1] * 596), M)
    assert list(d["_lgbt"][:4]) == [0.0, 1.0, 1.0, 1.0]  # cis hetero · no hetero · no binario · trans
    out = m.mide(f, R, M, REPS, 7)
    assert out[M.rid(m.P, "LGBT", "2021", "ENTIDAD", "07", "N")] == 0
    _cierra(m, out, {f"{m.P}-G-OLA-UNICA": "x"})


def test_mmsi_conducto_y_tono():
    m = MOD["CALC-MMSI-PISOS-2016-0001"]
    rng = np.random.default_rng(2)
    r = {"nivesc_inf": (1, 9), "divocu_act": (1, 99), "per_siteco": (1, 3), "p1_1": (1, 2), "p1_2": (20, 70),
         "p10_1": (1, 2), "p10_2": (1, 11), "p10_3": (1, 9), "tam_loc_enh": (1, 4), "factor_per": (1, 40),
         "est_dis_enh": (1, 5), "upm_enh": (1, 50)}
    f = _frame(rng, 600, m.columnas(), r)
    f["divocu_act"] = 99.0  # conducta sin soporte (todo «no especificada»)
    out = m.mide(f, R, M, REPS, 7)
    assert out[M.rid(m.P, "OCUPACION-DIRECTIVA", "2016", "TOTAL", "TODOS", "P")] is None
    _cierra(m, out, {f"{m.P}-G-OLA-UNICA": "x"})


def test_lb_cola_mas_ponderado():
    m = MOD["CALC-LATINOBAROMETRO-COLA-2023-0001"]
    rng = np.random.default_rng(3)
    r = {"wt": (1, 3), "edad": (15, 90), "sexo": (1, 2), "p1st": (1, 4), "p11stgbs_a": (-5, 4),
         "p15stgbs": (1, 2), "p13st_e": (1, 4), "reeeduc_1": (1, 7), "tamciud": (1, 8), "s2": (1, 5)}
    f = _frame(rng, 500, m.columnas(), r)
    out = m.mide(f, R, M, REPS, 7)
    assert out[f"{m.P}-G-DISENO"] == "MAS-PONDERADO-SIN-ESTRATO"
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def test_eic_hogares_conducto():
    m = MOD["CALC-EIC-HOGARES-2015-0001"]
    rng = np.random.default_rng(4)
    r = {"tipohog": (1, 9), "jefe_sexo": (1, 3), "tamloc": (1, 5), "ent": (1, 32), "factor": (1, 30),
         "estrato": (1, 8), "upm": (1, 80)}
    f = _frame(rng, 800, m.columnas(), r)
    out = m.mide(f, R, M, REPS, 7)
    assert out[M.rid(m.P, "HOGAR-AMPLIADO", "2015", "JEFATURA", "MUJER", "N")] > 0
    _cierra(m, out, {f"{m.P}-G-OLA-UNICA": "x"})


def test_enasem_conducto():
    m = MOD["CALC-ENASEM-ESCOLARIDAD-2021-0001"]
    rng = np.random.default_rng(5)
    r = {"yrschool": (0, 22), "sex_21": (1, 2), "age_21": (30, 100), "factori_21": (1, 99),
         "est_dis_21": (1, 4), "upm_dis_21": (1, 70)}
    f = _frame(rng, 500, m.columnas(), r)
    out = m.mide(f, R, M, REPS, 7)
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def _enadid_frames(rng):
    m = MOD["CALC-ENADID-COLA-2018-0001"]
    muj = _frame(rng, 500, list(m.COLS_MUJ), {"p10_1": (1, 8), "edad_muj": (12, 60), "tam_loc": (1, 4),
                                               "niv": (0, 11), "fac_per": (1, 50), "est_dis": (1, 5),
                                               "upm_dis": (1, 40)})
    hog = _frame(rng, 900, list(m.COLS_HOG), {"llave_hog": (1, 300), "paren": (1, 3), "sexo": (1, 2),
                                              "ent": (1, 32), "tam_loc": (1, 4), "fac_viv": (1, 50),
                                              "est_dis": (1, 5), "upm_dis": (1, 40)})
    mig = _frame(rng, 60, list(m.COLS_MIG), {"llave_hog": (1, 300), "p4_6": (1, 2), "p4_15": (1, 3)})
    return {"MUJ": muj, "HOG": hog, "MIG": mig}


def test_enadid_dos_marcos():
    m = MOD["CALC-ENADID-COLA-2018-0001"]
    rng = np.random.default_rng(6)
    frames = _enadid_frames(rng)
    out = m.mide(frames, R, M, REPS, 7)
    assert out[f"{m.P}-G-HOG-CON-MIGRANTE-VARON"] >= 0
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def test_enadid_sin_migrantes_rama_vacia():
    m = MOD["CALC-ENADID-COLA-2018-0001"]
    rng = np.random.default_rng(7)
    frames = _enadid_frames(rng)
    frames["MIG"]["p4_6"] = 2.0  # ningún varón → conducta «con migrante» sin soporte
    out = m.mide(frames, R, M, REPS, 7)
    assert out[M.rid(m.P, "JEFATURA-FEMENINA-CON-MIGRANTE-VARON", "2018", "TOTAL", "TODOS", "P")] is None
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def test_pew_religion_derivadas_y_conducto():
    m = MOD["CALC-PEW-RELIGION-2024-0001"]
    rng = np.random.default_rng(8)
    r = {"religion_combined": (1, 8), "religion_christian": (1, 3), "religion_none": (1, 3),
         "religion_switch": (1, 2), "god": (1, 9), "gender": (1, 2), "age": (15, 90), "d_educ_mexico": (1, 12),
         "weight": (1, 3)}
    f = _frame(rng, 400, m.columnas(), r)
    out = m.mide(f, R, M, REPS, 7)
    assert out[f"{m.P}-G-DISENO"] == "MAS-PONDERADO-SIN-ESTRATO"
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def test_envipe_union_y_conducto():
    m = MOD["CALC-ENVIPE-PERCEPCION-2024-0001"]
    rng = np.random.default_rng(9)
    r = {"id_per": (1, 400), "ap4_3_3": (1, 9), "ap4_4_a": (1, 9), "ap4_10_02": (1, 9), "sexo": (1, 2),
         "edad": (18, 98), "cve_ent": (1, 32), "fac_ele": (1, 90), "est_dis": (1, 6), "upm_dis": (1, 60)}
    per = _frame(rng, 400, list(m.COLS_PER), r)
    per["id_per"] = np.arange(400).astype(str)
    per["dominio"] = rng.choice(["U", "C", "R", ""], 400)
    sdem = pd.DataFrame({"id_per": np.arange(0, 800, 2).astype(str), "niv": rng.integers(0, 10, 400).astype(float)})
    out = m.mide(per, sdem, R, M, REPS, 7)
    assert out[f"{m.P}-G-FILAS-CON-NIV"] < out[f"{m.P}-G-FILAS-DISENO-VALIDO"]
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


def test_enoe_participacion_conducto():
    m = MOD["CALC-ENOE-PARTICIPACION-2024T4-0001"]
    rng = np.random.default_rng(10)
    r = {"r_def": (0, 1), "c_res": (1, 3), "eda": (10, 99), "sex": (1, 2), "cs_p17": (1, 2), "clase1": (0, 2),
         "clase2": (0, 4), "t_loc_tri": (1, 4), "niv_ins": (0, 5), "ent": (1, 32), "fac_tri": (1, 90),
         "est_d_tri": (1, 6), "upm": (1, 60)}
    f = _frame(rng, 900, m.columnas(), r)
    out = m.mide(f, R, M, REPS, 7)
    assert out[M.rid(m.P, "NO-ESTUDIA-NI-OCUPADO-18-24", "2024T4", "EDAD", "45-64", "P")] is None
    _cierra(m, out, {f"{m.P}-G-OLA-ABIERTA": "x"})


@pytest.mark.parametrize("calc,malo", [
    ("CALC-LATINOBAROMETRO-COLA-2023-0001", "latinobarometro2024_bd_stata"),
    ("CALC-ENASEM-ESCOLARIDAD-2021-0001", "enasem2024_bd_csv_zip"),
    ("CALC-ENADID-COLA-2018-0001", "enadid2023_base_datos_csv"),
    ("CALC-PEW-RELIGION-2024-0001", "pew_gas_spring2025"),
    ("CALC-ENVIPE-PERCEPCION-2024-0001", "envipe2026_csv"),
    ("CALC-ENOE-PARTICIPACION-2024T4-0001", "enoe_2026_2t_csv"),
    ("CALC-EIC-HOGARES-2015-0001", "cc1_inegi_ccpv_2020__cpv2020_personas"),
    ("CALC-ENDISEG-PISOS-2021-0001", "cc1_inegi_investigacion_2022__endiseg_web_2022_bd_csv"),
])
def test_guardia_ola_reservada_o_excluida_para(calc, malo):
    m = MOD[calc]
    inputs = {m.PAY: {"ruta_absoluta": "/x"}}
    inputs.update({k: {"bytes": b""} for k in m.INPUTS_REPO})
    inputs[malo] = {"ruta_absoluta": "/x"}
    with pytest.raises(m.ParoDeGuardia):
        m._guardia_inputs(inputs)


@pytest.mark.parametrize("calc", CALCS)
def test_spec_yaml_resultados_es_el_esquema(calc):
    with open(os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")) as fh:
        spec = yaml.safe_load(fh)
    assert spec["resultados"] == MOD[calc].esquema_resultados()
