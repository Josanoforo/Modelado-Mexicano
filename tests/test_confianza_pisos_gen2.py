"""D-22 de ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 (25/sep/2026): pisos por
segmento WVS 2018, Latinobarómetro 2023, PEW 2013–2024 y LAPOP 2004/2006/2019.

Specs: forense/prereg-caja/CONFIANZA-{WVS,LATINOBAROMETRO,PEW,LAPOP}-PISOS-spec-v1_0.md §5.
Sintético sin microdato: todas las ramas terminales (con soporte, conducta sin soporte,
categoría vacía, fuera de universo, código de no respuesta, peso faltante, UPM con faltantes
→ sin conglomerados, serie sin Δ de persistencia) pasan el conducto que sella
(`corrida0._valida_outputs`) sin NaN ni inf, y `resultados:` del spec.yaml es exactamente
`esquema_resultados()`. Guardias: una ola reservada o excluida entre los inputs PARA.
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


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_salud_conf_test")
M = _load("tools/dominios/confianza/motor_pisos.py", "motor_pisos_confianza_test")
WVS = _load("data/corrida0/CALC-WVS-PISOS-2018-0001/medidor.py", "m_wvs_pisos")
LB = _load("data/corrida0/CALC-LATINOBAROMETRO-PISOS-2023-0001/medidor.py", "m_lb_pisos")
PEW = _load("data/corrida0/CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001/medidor.py", "m_pew_pisos")
LAPOP = _load("data/corrida0/CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001/medidor.py", "m_lapop_pisos")
CALCS = {WVS: "CALC-WVS-PISOS-2018-0001", LB: "CALC-LATINOBAROMETRO-PISOS-2023-0001",
         PEW: "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001", LAPOP: "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001"}
REPS = 20


def _extras(mod):
    out = {f"{mod.P}-G-BOOTSTRAP-REPLICAS": REPS, f"{mod.P}-G-SEED": 1}
    for k in sorted(mod.INPUTS_REPO):
        out[f"{mod.P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = "0" * 64
    return out


def _cierra(mod, out, extra):
    out.update(_extras(mod))
    out.update(extra)
    assert corrida0._valida_outputs({"resultados": mod.esquema_resultados()}, out) == []
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k
    return out


def _frame(rng, n, cols, rangos):
    d = {}
    for c in cols:
        lo, hi = rangos.get(c.lower(), (0, 8))
        d[c.lower()] = rng.integers(lo, hi + 1, n).astype(float)
    f = pd.DataFrame(d)
    f.iloc[:3, :] = np.nan  # faltantes extendidos / no respuesta
    return f


def _wvs_frame(rng, n):
    r = {"w_weight": (1, 3), "i_psu": (1, 60), "q262": (15, 90), "q260": (1, 2)}
    return _frame(rng, n, WVS.columnas(), r)


def test_wvs_conducto_y_rama_sin_soporte():
    rng = np.random.default_rng(1)
    f = _wvs_frame(rng, 400)
    f["q57"] = 9.0  # conducta sin soporte (todo fuera de uno ∪ cero)
    f.loc[f["q260"] == 2, "g_townsize2"] = np.nan  # categoría vacía en un eje
    out = WVS.mide(f, R, M, REPS, 7)
    assert out[M.rid(WVS.P, "CONFIANZA-INTERPERSONAL", "2018", "TOTAL", "TODOS", "P")] is None
    _cierra(WVS, out, {f"{WVS.P}-G-OLA-UNICA": "x"})


def test_lb_conducto_mas_ponderado():
    rng = np.random.default_rng(2)
    r = {"wt": (1, 3), "edad": (15, 90), "sexo": (1, 2), "s1": (1, 14)}
    f = _frame(rng, 500, LB.columnas(), r)
    out = LB.mide(f, R, M, REPS, 7)
    assert out[f"{LB.P}-G-DISENO"] == "MAS-PONDERADO-SIN-ESTRATO"
    _cierra(LB, out, {f"{LB.P}-G-OLA-ABIERTA": "x"})


def _pew_frames(rng, upm_faltante=False):
    frames = {}
    for ola, (pais, peso, est, upm, sexo, edad, educ, conductas) in PEW.OLAS.items():
        cols = [r[1] for r in conductas.values()] + [c for c in (peso, est, upm, sexo, edad, educ) if c]
        r = {(peso or "").lower(): (1, 3), (sexo or "").lower(): (1, 2), (edad or "").lower(): (15, 99),
             (est or "x").lower(): (1, 5), (upm or "y").lower(): (1, 40), (educ or "z").lower(): (1, 12)}
        f = _frame(rng, 300, cols, r)
        f.iloc[:3, :] = 1.0  # sin faltantes de diseño salvo lo que pide el caso
        if upm and upm_faltante:
            f.loc[5, upm.lower()] = np.nan
        frames[ola] = f
    return frames


@pytest.mark.parametrize("upm_faltante", [False, True])
def test_pew_conducto_persistencia_y_upm_faltante(upm_faltante):
    rng = np.random.default_rng(3)
    frames = _pew_frames(rng, upm_faltante)
    frames["2023"]["polsys_junta"] = 9.0  # serie con una ola sin soporte → menos Δ
    out = PEW.compone(frames, R, M, REPS, 7)
    etiqueta = out[f"{PEW.P}-2017-G-DISENO"]
    assert etiqueta == ("MAS-PONDERADO-ESTRATIFICADO" if upm_faltante else "CONGLOMERADOS-ESTRATIFICADO")
    assert out[f"{PEW.P}-2013-G-DISENO"] == "MAS-PONDERADO-SIN-ESTRATO"
    assert out[f"{PEW.P}-RELIGION-MUY-IMPORTANTE-PERSISTENCIA-TOTAL-NDELTAS"] == 5
    _cierra(PEW, out, {f"{PEW.P}-G-OLA-RESERVADA": "x"})


def test_lapop_conducto_upm_compuesta():
    rng = np.random.default_rng(4)
    frames = {}
    for ola, (peso, est, upm, conductas) in LAPOP.OLAS.items():
        ups = (upm,) if isinstance(upm, str) else tuple(upm)
        cols = [r[1] for r in conductas.values()] + [c for c in (peso, est) if c] + list(ups) + ["q1", "q2", "ed", "ur"]
        r = {"q1": (1, 2), "q2": (15, 90), "ed": (0, 18), "ur": (1, 2), "wt": (1, 2), "mestrat": (1, 4),
             "estratopri": (101, 104), "mprov": (1, 32), "msec": (1, 5), "upm": (1, 60), "d5": (1, 10), "e16": (1, 10)}
        f = _frame(rng, 300, cols, r)
        f.iloc[:3, :] = 1.0
        frames[ola] = f
    out = LAPOP.compone(frames, R, M, REPS, 7)
    assert out[f"{LAPOP.P}-2004-G-DISENO"] == "MAS-PONDERADO-ESTRATIFICADO" or \
        out[f"{LAPOP.P}-2004-G-DISENO"] == "CONGLOMERADOS-ESTRATIFICADO"
    assert out[f"{LAPOP.P}-2004-G-DISENO"] == "CONGLOMERADOS-ESTRATIFICADO"
    _cierra(LAPOP, out, {f"{LAPOP.P}-G-OLA-RESERVADA": "x"})


def test_recodifica_fuera_de_codigos_es_nan():
    f = pd.DataFrame({"x": [1.0, 2.0, 8.0, np.nan, 88.0]})
    y = M.recodifica(f, ("bin", "x", [1], [2]))
    assert y[0] == 1.0 and y[1] == 0.0 and np.isnan(y[2:]).all()
    z = M.recodifica(pd.DataFrame({"x": [0.0, 1.0, 10.0, 88.0]}), ("media", "x", 1, 10))
    assert np.isnan(z[0]) and z[1] == 1.0 and z[2] == 10.0 and np.isnan(z[3])


@pytest.mark.parametrize("mod,mala", [(PEW, "pew_gas_spring2025"), (LAPOP, "mex_2023_lapop_americasbarometer_v1_0_w")])
def test_guardia_ola_reservada_para(mod, mala):
    inputs = {k: {"ruta_absoluta": "/x"} for k in mod.PAYS.values()}
    inputs.update({k: {"bytes": b""} for k in mod.INPUTS_REPO})
    inputs[mala] = {"ruta_absoluta": "/x"}
    with pytest.raises(mod.ParoDeGuardia):
        mod._guardia_inputs(inputs)


@pytest.mark.parametrize("mod", list(CALCS))
def test_spec_yaml_resultados_es_el_esquema(mod):
    ruta = os.path.join(ROOT, "data", "corrida0", CALCS[mod], "spec.yaml")
    with open(ruta) as fh:
        spec = yaml.safe_load(fh)
    assert spec["resultados"] == mod.esquema_resultados()
