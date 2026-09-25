"""D-22 de ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1 (25/sep/2026): pisos de consumo y gasto ENIGH
2016-2022 y ENGASTO 2012.

Specs: forense/prereg-caja/CONSUMO-{ENIGH,ENGASTO}-PISOS-spec-v1_0.md §5. Sintético sin
microdato: todas las ramas terminales (con soporte, hogar sin partidas de gasto, denominador
cero, categoría vacía, fuera de universo, entidad fuera de rango, llave no pareada, jefe
inconsistente, UPM única de estrato, ola sin Δ de persistencia) pasan el conducto que sella
(`corrida0._valida_outputs`) sin NaN ni inf; `resultados:` del spec.yaml es exactamente
`esquema_resultados()`; y la participación por peso w·den es la razón de totales.
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


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_consumo_test")
ENIGH = _load("data/corrida0/CALC-ENIGH-CONSUMO-PISOS-0001/medidor.py", "m_enigh_consumo")
ENGASTO = _load("data/corrida0/CALC-ENGASTO-CONSUMO-PISOS-0001/medidor.py", "m_engasto_consumo")


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


# ═══════════════════════════ ENIGH ═══════════════════════════

def _enigh_ola(seed, sin_mujeres=False):
    rng = np.random.default_rng(seed)
    n = 240
    folioviv = [f"{(i % 30) + 1:02d}{i:08d}" for i in range(n)]
    folioviv[0] = "99" + folioviv[0][2:]  # entidad fuera de rango
    folioviv[1] = folioviv[1][1:]  # cero a la izquierda perdido: zfill lo repara
    est = [str(1 + (i % 6)) if i != 5 else "77" for i in range(n)]  # estrato 77: UPM única (certeza)
    upm = [f"{int(e) * 100 + (i % 4)}" if e != "77" else "7700" for i, e in enumerate(est)]
    gasto = rng.uniform(1000, 30000, n)
    rub = rng.dirichlet(np.ones(9), n) * gasto[:, None]
    conc = pd.DataFrame({
        "folioviv": folioviv, "foliohog": ["1"] * n, "tam_loc": [str(1 + i % 4) for i in range(n)],
        "est_dis": est, "upm": upm, "factor": [str(int(x)) for x in rng.integers(50, 500, n)],
        "sexo_jefe": ["1" if (sin_mujeres or i % 3) else "2" for i in range(n)],
        "edad_jefe": [str(18 + i % 70) for i in range(n)],
        "educa_jefe": [str(1 + i % 11) for i in range(n)],
        "ing_cor": [f"{x:.2f}" for x in rng.uniform(2000, 60000, n)],
        "gasto_mon": [f"{x:.2f}" for x in gasto],
        "ali_fuera": [f"{x:.2f}" if i % 4 else "0" for i, x in enumerate(rub[:, 0] * 0.2)],
        "bebidas": [f"{x:.2f}" for x in rub[:, 0] * 0.1],
        "comunica": [f"{x:.2f}" if i % 5 else "0" for i, x in enumerate(rub[:, 5] * 0.3)],
        "prestamos": ["0" if i % 7 else "1500" for i in range(n)],
        "pago_tarje": ["0" if i % 6 else "800" for i in range(n)],
        "deudas": ["0" if i % 8 else "600" for i in range(n)],
        **{r: [f"{x:.2f}" for x in rub[:, j]] for j, r in enumerate(ENIGH.RUBROS)},
    })
    conc.loc[2, "gasto_mon"] = "0"  # denominador cero: fuera de PART-*
    conc.loc[3, "alimentos"] = "0"
    conc.loc[4, "factor"] = "0"  # diseño inválido
    hog = pd.DataFrame({"folioviv": conc["folioviv"], "foliohog": "1",
                        "celular": [["1", "2", ""][i % 3] for i in range(n)],
                        "conex_inte": [["1", "2"][i % 2] for i in range(n)],
                        "tarjeta": [["1", "2", "2"][i % 3] for i in range(n)],
                        "pagotarjet": [["1", "2", ""][i % 3] for i in range(n)]})
    hog = hog.drop(index=[6])  # hogar sin fila en HOGARES
    filas = []
    for i in range(n):
        if i % 9 == 0:
            continue  # hogar sin partidas: sumas 0
        for k in range(3):
            filas.append({"folioviv": folioviv[i], "foliohog": "1", "clave": f"A{1 + (i + k) % 247:03d}",
                          "tipo_gasto": "G1" if k < 2 else "G3", "forma_pag1": str([1, 2, 5, 1][(i + k) % 4]),
                          "forma_pag2": "", "forma_pag3": "", "lugar_comp": f"{1 + (i * 3 + k) % 18:02d}",
                          "gasto_tri": f"{rng.uniform(10, 900):.2f}"})
    filas.append({"folioviv": "0100000000X", "foliohog": "1", "clave": "A001", "tipo_gasto": "G1",
                  "forma_pag1": "1", "forma_pag2": "", "forma_pag3": "", "lugar_comp": "06", "gasto_tri": "10"})
    return {"conc": conc, "hog": hog, "gas": pd.DataFrame(filas)}


def test_enigh_ramas_terminales_pasan_el_conducto():
    por_ola, diags = {}, {}
    for j, ola in enumerate(ENIGH.OLAS):
        por_ola[ola], diags[ola] = ENIGH.mide_ola(_enigh_ola(10 + j, sin_mujeres=(ola == "2018")), R, 20, 7)
    out = ENIGH.calcula(por_ola, diags, R)
    assert diags["2016"]["ENTIDAD-FUERA-DE-RANGO"] == 1
    assert diags["2016"]["JOIN-SIN-HOGARES"] == 1
    assert diags["2016"]["FILAS-GASTO-SIN-HOGAR"] >= 1
    assert out[ENIGH.rid("HOG-TIENE-CELULAR", "2018", "SEXO-JEFE", "MUJER", "N")] == 0
    assert out[ENIGH.rid("HOG-TIENE-CELULAR", "2018", "SEXO-JEFE", "MUJER", "P")] is None
    assert out[f"{ENIGH.P}-PART-ALIMENTOS-TOTAL-TAU2"] is not None
    _cierra(ENIGH, out, {"BOOTSTRAP-REPLICAS": 20, "SEED": 7, "INPUT-RECETA-SHA256": "x",
                         "OLA-RESERVADA": "ENIGH 2024"})


def test_enigh_participacion_es_razon_de_totales():
    fr = _enigh_ola(3)
    f, ejes, _ = ENIGH.prepara(fr["conc"], fr["hog"], fr["gas"], R)
    y, mult = ENIGH.conducta("PART-ALIMENTOS", f, R)
    w = f["_w"].to_numpy()
    res = R.marginales(f, {"X": y}, {}, w * mult, "_est", "_upm", 10, 1)
    num, den = R.num(f["alimentos"]).to_numpy(), R.num(f["gasto_mon"]).to_numpy()
    ok = den > 0
    esperado = (w[ok] * num[ok]).sum() / (w[ok] * den[ok]).sum()
    assert abs(res[("X", "TOTAL", "TODOS")]["p"] - esperado) < 1e-12


def test_enigh_deciles_equilibrados():
    w = np.ones(1000)
    d = ENIGH.deciles(np.arange(1000.0), w)
    assert all((d == c).sum() == 100 for c in ENIGH.DECILES)


def test_enigh_guardia_rechaza_2024():
    ins = {pid: {"ruta_absoluta": "/x"} for pid in ENIGH.PAYLOADS.values()}
    ins["receta_pisos"] = {"bytes": b""}
    ins["enigh2024_nc_csv"] = {"ruta_absoluta": "/x"}
    try:
        ENIGH._guardia_inputs(ins)
    except ENIGH.ParoDeGuardia:
        return
    raise AssertionError("la guardia no paró")


def test_enigh_resultados_del_spec_son_el_esquema():
    assert _spec("CALC-ENIGH-CONSUMO-PISOS-0001")["resultados"] == ENIGH.esquema_resultados()


# ═══════════════════════════ ENGASTO ═══════════════════════════

def _engasto(seed):
    rng = np.random.default_rng(seed)
    n = 200
    llave = {"anio_reg": ["2012"] * n, "trimestre": [str(1 + i % 4) for i in range(n)],
             "folio": [f"{i:010d}" for i in range(n)], "hog_ent_1": "1", "hog_ent_2": "1"}
    hog = pd.DataFrame({**llave, "num_cel": [i % 4 if i % 13 else 99 for i in range(n)],
                        "conex_inte": [["1", "2", ""][i % 3] for i in range(n)],
                        "factor_hog": rng.integers(0 + 1, 300, n)})
    hog.loc[0, "factor_hog"] = 0
    viv = pd.DataFrame({k: llave[k] for k in ("anio_reg", "trimestre", "folio")})
    viv["tam_loc"] = [str(1 + i % 4) for i in range(n)]
    viv["est_dis"] = [str(1 + i % 5) if i != 7 else "99" for i in range(n)]
    viv["upm"] = [f"{i % 5}{i % 3}" if i != 7 else "990" for i in range(n)]
    viv = viv.drop(index=[8])
    lug = pd.DataFrame(llave)
    for j, c in enumerate(ENGASTO.LC):
        lug[c] = [["", "97"][i % 2] if (i + j) % 11 == 0 else f"{1 + (i + j) % 18:02d}" for i in range(n)]
    lug = lug.drop(index=[9])
    aj = pd.DataFrame({**{k: v * 2 if isinstance(v, list) else v for k, v in llave.items()},
                       "sexo_je": [str(1 + i % 2) for i in range(n)] * 2,
                       "edad_je": [18 + i % 70 for i in range(n)] * 2,
                       "ned_je": [str(1 + i % 4) for i in range(n)] * 2})
    aj.loc[n + 10, "ned_je"] = "9"  # jefe inconsistente entre filas
    return {"hogar": hog, "vivienda": viv, "lugar": lug, "ajustado": aj}


def test_engasto_ramas_terminales_pasan_el_conducto():
    fr = _engasto(5)
    f, ejes, diag = ENGASTO.prepara(fr, R)
    assert diag["JOIN-SIN-VIVIENDA"] == 1 and diag["JOIN-SIN-LUGAR-COMPRA"] == 1
    assert diag["JEFE-INCONSISTENTE"] == 1
    out = ENGASTO.mide(fr, R, 20, 7)
    _cierra(ENGASTO, out, {"BOOTSTRAP-REPLICAS": 20, "SEED": 7, "INPUT-RECETA-SHA256": "x",
                           "OLA-RESERVADA": "ENGASTO 2013"})


def test_engasto_guardia_rechaza_2013():
    ins = {pid: {"ruta_absoluta": "/raw/engasto2012/x.zip"} for pid in ENGASTO.PAY.values()}
    ins["receta_pisos"] = {"bytes": b""}
    ins["engasto2012_hogar_dta"] = {"ruta_absoluta": "/raw/engasto2013/hogar_dta.zip"}
    try:
        ENGASTO._guardia_inputs(ins)
    except ENGASTO.ParoDeGuardia:
        return
    raise AssertionError("la guardia no paró")


def test_engasto_resultados_del_spec_son_el_esquema():
    assert _spec("CALC-ENGASTO-CONSUMO-PISOS-0001")["resultados"] == ENGASTO.esquema_resultados()
