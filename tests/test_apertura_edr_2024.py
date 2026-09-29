"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de EDR 2024 (expediente EDR-2024).

El esquema es el del medidor sellado del contendiente `CALC-EDR-SUICIDIO-PISOS-0001` (`CAMPOS_BASE` + la variable
de presunto `TIPO_DEFUN`), en un DBF sintético `DEFUN24.dbf` dentro de un ZIP. Ramas: con soporte (0 < K < N);
conducta sin soporte (TIPO_DEFUN ausente -> SUICIDIO-PRESUNTO None); categoría vacía (toda TLOC_RESID = 15 ->
MENOS-2500 None). Toda salida pasa `corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el
dictamen es del vocabulario. R coincide celda por celda con `_celdas` del sellado. Sin microdato.
"""
from __future__ import annotations

import importlib.util
import math
import os
import struct
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


REL = "forense/prereg-aperturas/EDR-2024/medidor_apertura_edr_2024.py"
MOD = _load(REL, "ap_edr_2024_t")
ANCHO = {"ENT_RESID": 2, "TLOC_RESID": 2, "CAUSA_DEF": 4, "SEXO": 1, "EDAD": 4, "ANIO_OCUR": 4,
         "ANIO_REGIS": 4, "ESCOLARIDA": 2, "TIPO_DEFUN": 1}


def dbf(df: pd.DataFrame) -> bytes:
    """dBase III mínimo (campos C de ancho fijo) con las columnas de `df`."""
    n = len(df)
    cols = list(df.columns)
    anchos = [ANCHO[c] for c in cols]
    lcab = 32 + 32 * len(cols) + 1
    lreg = 1 + sum(anchos)
    cab = struct.pack("<B3BIHH20x", 3, 126, 9, 29, n, lcab, lreg)
    campos = b"".join(struct.pack("<11sc4xBB14x", c.encode("ascii"), b"C", a, 0) for c, a in zip(cols, anchos))
    partes = [np.full((n, 1), ord(" "), dtype=np.uint8)]
    for c, a in zip(cols, anchos):
        v = np.array([str(x).ljust(a)[:a] for x in df[c]], dtype=f"S{a}")
        partes.append(v.view(np.uint8).reshape(n, a))
    return cab + campos + b"\r" + np.hstack(partes).tobytes() + b"\x1a"


def _frame(n=60000, seed=2024):
    rng = np.random.default_rng(seed)
    sui = rng.random(n) < 0.0113
    e = np.where(sui, np.where(rng.random(n) < 0.397, rng.integers(15, 30, n),
                               np.where(rng.random(n) < 0.55, rng.integers(30, 45, n), rng.integers(45, 90, n))),
                 rng.integers(0, 100, n))
    return pd.DataFrame({
        "ENT_RESID": [f"{i:02d}" for i in rng.integers(1, 33, n)],
        "TLOC_RESID": rng.integers(1, 18, n),
        "CAUSA_DEF": np.where(sui, [f"X7{i}" for i in rng.integers(0, 10, n)], "I219"),
        "SEXO": np.where(sui, np.where(rng.random(n) < 0.806, 1, 2), rng.integers(1, 3, n)),
        "EDAD": 4000 + e,
        "ANIO_OCUR": np.where(rng.random(n) < 0.989, 2024, 2023),
        "ANIO_REGIS": 2024,
        "ESCOLARIDA": rng.integers(1, 11, n),
        "TIPO_DEFUN": np.where(sui, 3, 1),
    })


def _zip(tmp_path, df, miembro="DEFUN24.dbf"):
    ruta = tmp_path / "defunciones_base_datos_2024_dbf.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(miembro, dbf(df))
        z.writestr("CATMINDE.dbf", b"")
    return str(ruta)


def _inputs(ruta):
    ins = {MOD.PAYLOAD: {"ruta_absoluta": ruta}}
    ins.update({k: {} for k, _r, _n in MOD.CONTRATO["repo"]})
    return ins


def _ok(out):
    assert corrida0._valida_outputs({"resultados": MOD.esquema_resultados()}, out) == []
    assert out[f"{MOD.P}-DICTAMEN"] in MOD.G.VOCABULARIO
    assert out[f"{MOD.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def test_con_soporte_de_punta_a_punta(tmp_path):
    out = MOD.medir(_inputs(_zip(tmp_path, _frame())), {})
    _ok(out)
    assert 0 < out[f"{MOD.P}-K"] < out[f"{MOD.P}-N"]
    assert out[f"{MOD.P}-SUICIDIO-PRESUNTO-TOTAL-TODOS-R"] is not None


def test_conducta_sin_soporte_columna_ausente(tmp_path):
    out = MOD.medir(_inputs(_zip(tmp_path, _frame().drop(columns=["TIPO_DEFUN"]))), {})
    _ok(out)
    assert out[f"{MOD.P}-SUICIDIO-PRESUNTO-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-SUICIDIO-CIE-TOTAL-TODOS-R"] is not None


def test_categoria_vacia(tmp_path):
    df = _frame()
    df["TLOC_RESID"] = 15
    out = MOD.medir(_inputs(_zip(tmp_path, df)), {})
    _ok(out)
    assert out[f"{MOD.P}-SUICIDIO-CIE-TLOC-MENOS-2500-R"] is None
    assert out[f"{MOD.P}-SUICIDIO-CIE-TLOC-100MIL-MAS-R"] is not None


def test_r_coincide_con_celdas_del_sellado(tmp_path):
    S, _p = MOD.sellados()
    df, faltan = MOD.lee_payload_reservado(S, _zip(tmp_path, _frame()), MOD.campos(S))
    assert faltan == []
    r = MOD.mide_r(S, df)
    ys, ejes, _d = S.prepara(df, "2024")
    ref = S._celdas(ys, ejes)
    for c, eje, cat in MOD.celdas_de(S):
        a, b = r.get((c, eje, cat)), ref[(c, eje, cat)][0]
        assert (a is None and b is None) or abs(a - b) < 1e-12, (c, eje, cat)


def test_miembro_ausente_para(tmp_path):
    with pytest.raises(MOD.G.ParoDeGuardia):
        MOD.medir(_inputs(_zip(tmp_path, _frame(), miembro="DEFUN23.dbf")), {})


def test_auditoria_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert MOD.G.auditoria_ast(fuente) == []
    for mut in MOD.E.MUTACIONES:
        assert MOD.G.auditoria_ast(fuente + "\n\n" + mut), mut
