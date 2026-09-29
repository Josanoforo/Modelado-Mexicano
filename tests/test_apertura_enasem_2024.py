"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENASEM 2024 (expediente ENASEM-2024).

El esquema es el del medidor sellado del contendiente `CALC-ENASEM-ESCOLARIDAD-2021-0001` (`COLS_CRUDAS`, con el
sufijo de ronda `_21` -> `_24`), que el medidor de apertura reusa. Ramas: con soporte; conducta sin soporte
(columna YRSCHOOL ausente -> R None, NO-ESTIMABLE); categoría vacía (sólo hombres -> MUJER None). Toda salida pasa
`corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el dictamen es del vocabulario. `medir`
se ejerce de punta a punta sobre un ZIP sintético (lee_payload_reservado incluido). Sin microdato.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
import zipfile

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REL = "forense/prereg-aperturas/ENASEM-2024/medidor_apertura_enasem_2024.py"
MOD = _load(REL, "ap_enasem_2024_t")


def _ok(out):
    assert corrida0._valida_outputs({"resultados": MOD.esquema_resultados()}, out) == []
    assert out[f"{MOD.P}-DICTAMEN"] in MOD.G.VOCABULARIO
    assert out[f"{MOD.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _frame(n=20000, seed=24):
    S, _M, _p = MOD.sellados()
    rng = np.random.default_rng(seed)
    # YRSCHOOL con la mezcla del piso 2021 (0: ~13 %, 1-6: ~47 %, 7-22: ~40 %): cobertura parcial, 0 < K < N
    ys = rng.choice(3, n, p=[0.133, 0.466, 0.401])
    yr = np.where(ys == 0, 0, np.where(ys == 1, rng.integers(1, 7, n), rng.integers(7, 23, n)))
    d = {"YRSCHOOL": yr, "SEX_24": rng.integers(1, 3, n), "AGE_24": rng.integers(40, 100, n),
         "FACTORI_24": rng.uniform(1, 99, n), "EST_DIS_24": rng.integers(1, 5, n), "UPM_DIS_24": rng.integers(1, 90, n)}
    assert set(d) == set(MOD.columnas(S))
    return pd.DataFrame(d)


def _zip(tmp_path, df, miembro=MOD.MIEMBRO):
    ruta = tmp_path / "enasem_2024_bd_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(miembro, df.to_csv(index=False))
        z.writestr("tr_enasem24_master_follow_up_file.csv", "AGE_24,SEX_24\n60,1\n")
    return str(ruta)


def _inputs(ruta):
    ins = {MOD.PAYLOAD: {"ruta_absoluta": ruta}}
    ins.update({k: {} for k, _r, _n in MOD.CONTRATO["repo"]})
    return ins


def test_con_soporte_de_punta_a_punta(tmp_path):
    out = MOD.medir(_inputs(_zip(tmp_path, _frame())), {})
    _ok(out)
    assert out[f"{MOD.P}-N"] == 14
    assert 0 < out[f"{MOD.P}-K"] < 14
    assert out[f"{MOD.P}-SIN-ESCOLARIDAD-TOTAL-TODOS-R"] is not None


def test_rama_k_cero(tmp_path):
    """K = 0 con N = 14: Wilson sin acotar daba WILSON-LO = -1.4e-17 (rechazado por _valida_outputs)."""
    df = _frame()
    df["YRSCHOOL"] = 22  # nadie sin escolaridad ni con 6 años o menos: R = 0 fuera de todo IC del piso
    out = MOD.medir(_inputs(_zip(tmp_path, df)), {})
    assert out[f"{MOD.P}-K"] == 0
    _ok(out)


def test_conducta_sin_soporte_columna_ausente(tmp_path):
    out = MOD.medir(_inputs(_zip(tmp_path, _frame().drop(columns=["YRSCHOOL"]))), {})
    _ok(out)
    assert out[f"{MOD.P}-SIN-ESCOLARIDAD-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-DICTAMEN"] == "NO-ESTIMABLE"


def test_categoria_vacia(tmp_path):
    df = _frame()
    df["SEX_24"] = 1
    out = MOD.medir(_inputs(_zip(tmp_path, df)), {})
    _ok(out)
    assert out[f"{MOD.P}-SEIS-ANOS-O-MENOS-SEXO-MUJER-R"] is None
    assert out[f"{MOD.P}-SEIS-ANOS-O-MENOS-SEXO-HOMBRE-R"] is not None


def test_universo_50_mas_y_un_eje():
    S, M, _p = MOD.sellados()
    df = _frame()
    df.columns = [c.lower() for c in df.columns]
    df = df.astype(str)
    r = MOD.mide_r(S, M, df)
    f = df.assign(y=(df["yrschool"].astype(int) == 0).astype(float), w=df["factori_24"].astype(float))
    f = f[f["age_24"].astype(int) >= 50]
    assert abs(r[("SIN-ESCOLARIDAD", "TOTAL", "TODOS")] - (f.w * f.y).sum() / f.w.sum()) < 1e-12


def test_miembro_ausente_para(tmp_path):
    with pytest.raises(MOD.G.ParoDeGuardia):
        MOD.medir(_inputs(_zip(tmp_path, _frame(), miembro="otro.csv")), {})


def test_auditoria_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert MOD.G.auditoria_ast(fuente) == []
    for mut in MOD.E.MUTACIONES:
        assert MOD.G.auditoria_ast(fuente + "\n\n" + mut), mut
