"""D-22 de ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 (24/sep/2026): pisos por segmento ENSANUT,
ENCODAT y ENBIARE.

Specs: forense/prereg-caja/SALUD-{ENSANUT,ENCODAT,ENBIARE}-PISOS-spec-v1_0.md §5. Sintético
sin microdato: todas las ramas terminales (con soporte, conducta sin soporte, categoría
vacía, fuera de universo, llave no pareada, sin Δ de persistencia) pasan el conducto que
sella (`corrida0._valida_outputs`) sin NaN ni inf, y `resultados:` del spec.yaml es
exactamente `esquema_resultados()`.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_salud_test")
ENSANUT = _load("data/corrida0/CALC-ENSANUT-PISOS-SALUD-0001/medidor.py", "m_ensanut_pisos")
ENCODAT = _load("data/corrida0/CALC-ENCODAT-PISOS-SUSTANCIAS-0001/medidor.py", "m_encodat_pisos")
ENBIARE = _load("data/corrida0/CALC-ENBIARE-PISOS-BIENESTAR-0001/medidor.py", "m_enbiare_pisos")


def _spec(calc):
    with open(os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")) as f:
        return yaml.safe_load(f)


def _sin_no_finitos(out):
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k


def _cierra(M, out, extra):
    for k, v in extra.items():
        out[f"{M.P}-G-{k}"] = v
    esq = M.esquema_resultados()
    assert corrida0._valida_outputs({"resultados": esq}, out) == []
    _sin_no_finitos(out)
    return out


# ═══════════════════════════ ENSANUT ═══════════════════════════

def _fr_ensanut(rng, arch, n):
    d = {"folio_i": rng.integers(1, max(2, n // 3), n).astype(str), "folio_int": rng.integers(1, 4, n).astype(str),
         "ponde_f": rng.uniform(50, 500, n), "est_sel": rng.integers(1, 40, n).astype(str),
         "upm": rng.integers(1, 300, n).astype(str), "estrato": rng.integers(1, 4, n)}
    for c in ENSANUT.COLS[arch]:
        if c not in d:
            d[c] = rng.integers(1, 5, n).astype(float)
    if "edad" in d:
        d["edad"] = rng.integers(10, 20, n) if arch == "ADOL" else rng.integers(20, 90, n)
    if "h0303" in d:
        d["h0303"] = rng.integers(0, 90, n)
    if "h0317a" in d:
        d["h0317a"] = rng.integers(1, 13, n).astype(float)
    if "u0201" in d:
        d["u0201"] = rng.integers(1, 27, n).astype(float)
    d["upm"] = np.char.add(d["est_sel"].astype(str), np.char.add("-", d["upm"].astype(str)))
    f = pd.DataFrame(d)
    f.loc[:5, "ponde_f"] = np.nan
    return f


def _corre_ensanut(mutar=None):
    rng = np.random.default_rng(11)
    por, diag = {}, {}
    for ola in ENSANUT.OLAS:
        frames = {a: _fr_ensanut(rng, a, 9000 if a == "INTE" else 2500) for a in ("ADUL", "INTE", "UTIL", "ADOL")}
        if mutar:
            mutar(ola, frames)
        por[ola], diag[ola] = ENSANUT.mide_ola(ola, frames, R, 60, 7)
    out = ENSANUT.calcula(por, diag, R)
    return _cierra(ENSANUT, out, {"BOOTSTRAP-REPLICAS": 60, "SEED": 7, "INPUT-RECETA-SHA256": "x",
                                  "OLA-RESERVADA": "x"})


def test_ensanut_todas_las_ramas():
    def mutar(ola, fr):
        if ola == "2023":
            fr["UTIL"]["u0201"] = 99.0          # conducta sin soporte en una ola
        if ola == "2022":
            fr["ADUL"]["a1308"] = 1.0           # ALCOHOL-12M = 1 en todos: p fuera de (0,1), sin Δ
        fr["ADOL"]["estrato"] = 1               # categorías de ESTRATO vacías
    out = _corre_ensanut(mutar)
    P = ENSANUT.P
    assert out[f"{P}-ATENCION-CONSULTORIO-FARMACIA-2023-TOTAL-TODOS-P"] is None
    assert out[f"{P}-ATENCION-CONSULTORIO-FARMACIA-2023-TOTAL-TODOS-N"] == 0
    assert out[f"{P}-IDEACION-SUICIDA-ADOLESCENTES-2024-ESTRATO-URBANO-P"] is None
    assert out[f"{P}-DEPRESION-CESD7-TOTAL-TAU2"] is not None
    assert out[f"{P}-DEPRESION-CESD7-2024-TOTAL-TODOS-ICC-LO"] <= out[f"{P}-DEPRESION-CESD7-2024-TOTAL-TODOS-IC-LO"]


def test_ensanut_sin_2025_y_guardia():
    assert not any("ensanut_2025" in p for p in ENSANUT.PAYLOADS.values())
    inputs = {p: {"ruta_absoluta": "/x"} for p in ENSANUT.PAYLOADS.values()}
    inputs["receta_pisos_salud"] = {"bytes": b""}
    ENSANUT._guardia_inputs(inputs)
    inputs["ensanut_2025__adultos_2025_w_stata_stata_zip"] = {"ruta_absoluta": "/x"}
    try:
        ENSANUT._guardia_inputs(inputs)
        raise AssertionError("la guardia debió parar")
    except ENSANUT.ParoDeGuardia:
        pass


def test_cesd7_regla():
    f = pd.DataFrame({c: [1.0, 4.0, 2.0, 1.0] for c in ENSANUT.CESD})
    f["a0216"] = [4.0, 1.0, 3.0, 9.0]  # invertido; 9 = fuera
    f["edad"] = [30, 30, 70, 30]
    y = ENSANUT.conducta_y("DEPRESION-CESD7", f, R)
    # fila 0: 0*6 + (3-3)=0 → 0; fila 1: 3*6+3=21 → 1; fila 2: 1*6+(3-2)=7 ≥ 5 (60+) → 1; fila 3 fuera
    assert list(y[:3]) == [0.0, 1.0, 1.0] and np.isnan(y[3])


# ═══════════════════════════ ENCODAT ═══════════════════════════

def _corre_encodat(mutar=None):
    rng = np.random.default_rng(3)
    nh = 1500
    hog = pd.DataFrame({"id_hogar": [f"{i:020d}" for i in range(nh)], "estrato": rng.integers(1, 4, nh),
                        "est_var": rng.integers(1, 30, nh), "code_upm": rng.integers(1, 300, nh).astype(str)})
    n = 4000
    hid = rng.integers(0, nh + 40, n)  # algunos no parean
    ind = pd.DataFrame({"id_pers": [f"{h:020d}{k:02d}" for h, k in zip(hid, rng.integers(1, 5, n))],
                        "ponde_ss": rng.uniform(1, 9, n), "ds2": rng.integers(1, 3, n), "ds3": rng.integers(10, 70, n),
                        "ds9": rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 99], n)})
    for c in ENCODAT.COLS_IND:
        if c not in ind:
            ind[c] = rng.choice([1, 2, 9], n).astype(float)
    ind["al11"] = rng.integers(1, 7, n).astype(float)
    ind["tb02"] = rng.choice([1, 2, 3, np.nan], n)
    if mutar:
        mutar(ind, hog)
    out = ENCODAT.mide(ind, hog, R, 60, 5)
    return _cierra(ENCODAT, out, {"BOOTSTRAP-REPLICAS": 60, "SEED": 5, "INPUT-RECETA-SHA256": "x",
                                  "OLA-RESERVADA": "x"})


def test_encodat_todas_las_ramas():
    def mutar(ind, hog):
        ind["tp1"] = np.nan          # sin soporte
        hog["estrato"] = 3           # RURAL y URBANO vacíos
    out = _corre_encodat(mutar)
    P = ENCODAT.P
    assert out[f"{P}-CONSULTO-PROFESIONAL-POR-CONSUMO-2016-TOTAL-TODOS-P"] is None
    assert out[f"{P}-ALCOHOL-12M-2016-ESTRATO-RURAL-N"] == 0
    assert out[f"{P}-G-JOIN-SIN-HOGAR"] > 0
    assert not any("encodat_2025" in p for p in (ENCODAT.PAY_IND, ENCODAT.PAY_HOG))


# ═══════════════════════════ ENBIARE ═══════════════════════════

def _corre_enbiare(mutar=None):
    rng = np.random.default_rng(4)
    n = 3000
    key = pd.DataFrame({"folio": rng.integers(1, 99999, n).astype(str), "viv_sel": "1", "hogar": "1",
                        "n_ren": rng.integers(1, 5, n).astype(str)}).drop_duplicates()
    n = len(key)
    ele = key.copy()
    for c in ENBIARE.COLS_ELE[4:]:
        ele[c] = rng.integers(0, 11, n).astype(str)
    for c in ENBIARE.PD2 + ["pd3_1", "pd3_2"]:
        ele[c] = rng.integers(0, 4, n).astype(str)
    for c in ("pb2_1", "pb2_2", "pg6", "pg7"):
        ele[c] = rng.choice(["1", "2", "3", ""], n)
    ele["fac_ele"] = rng.uniform(100, 900, n).astype(str)
    ele["est_dis"] = rng.integers(1, 60, n).astype(str)
    ele["upm_dis"] = rng.integers(1, 700, n).astype(str)
    ele["tloc"] = rng.integers(1, 5, n).astype(str)
    sdem = key.copy()
    sdem["sexo"] = rng.integers(1, 3, n).astype(str)
    sdem["edad"] = rng.integers(15, 95, n).astype(str)
    sdem["nivel"] = rng.choice(["00", "03", "06", "08", "99", "b"], n)
    if mutar:
        mutar(ele, sdem)
    out = ENBIARE.mide(ele, sdem, R, 60, 5)
    return _cierra(ENBIARE, out, {"BOOTSTRAP-REPLICAS": 60, "SEED": 5, "INPUT-RECETA-SHA256": "x",
                                  "OLA-UNICA": "x"})


def test_enbiare_todas_las_ramas():
    def mutar(ele, sdem):
        ele["pb1_11"] = "99"          # escala sin dato válido
        ele["tloc"] = "1"             # TLOC 2–4 vacíos
    out = _corre_enbiare(mutar)
    P = ENBIARE.P
    assert out[f"{P}-CONFIANZA-PARTIDOS-2021-TOTAL-TODOS-P"] is None
    assert out[f"{P}-TIENE-RELIGION-2021-TLOC-MENOS-2500-N"] == 0
    assert 0 <= out[f"{P}-SATISFACCION-VIDA-2021-TOTAL-TODOS-P"] <= 10


# ═══════════════════════════ contrato ═══════════════════════════

def test_resultados_del_spec_igual_a_esquema():
    for calc, M in (("CALC-ENSANUT-PISOS-SALUD-0001", ENSANUT), ("CALC-ENCODAT-PISOS-SUSTANCIAS-0001", ENCODAT),
                    ("CALC-ENBIARE-PISOS-BIENESTAR-0001", ENBIARE)):
        assert _spec(calc)["resultados"] == M.esquema_resultados(), calc


def test_persistencia_y_ic_calibrado():
    t2, n = R.persistencia({"a": {"x": 0.2}, "b": {"x": 0.3}, "c": {"x": 0.25}}, ["a", "b", "c"], ["x"])
    d1 = math.log(0.3 / 0.7) - math.log(0.2 / 0.8)
    d2 = math.log(0.25 / 0.75) - math.log(0.3 / 0.7)
    assert n == 2 and abs(t2 - (d1 * d1 + d2 * d2) / 2) < 1e-12
    assert R.ic_calibrado(0.3, 0.25, 0.35, None) == (None, None)
    lo, hi = R.ic_calibrado(0.3, 0.25, 0.35, t2)
    assert lo < 0.25 and hi > 0.35
