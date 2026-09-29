"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de EMAT 2024 (expediente EMAT-2024).

El esquema es el del medidor sellado del contendiente `CALC-EMAT-PAREJA-PISOS-0001` (`CAMPOS`), en un DBF sintético
`MATRI24.dbf` dentro de un ZIP. Ramas: con soporte (0 < K < N); conducta sin soporte (GENERO ausente ->
M-MISMO-SEXO None); categoría vacía (toda TAM_LOC_RE = 15 -> MENOS-2500 None). Toda salida pasa
`corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el dictamen es del vocabulario. R coincide
celda por celda con `_celdas` del sellado. Sin microdato.
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


REL = "forense/prereg-aperturas/EMAT-2024/medidor_apertura_emat_2024.py"
MOD = _load(REL, "ap_emat_2024_t")
ANCHO = {"ENT_REGIS": 2, "TAM_LOC_RE": 2, "ANIO_REGIS": 4, "GENERO": 1, "SEXO_CON1": 1, "EDAD_CON1": 2,
         "ESCOL_CON1": 1, "CONACTCON1": 1, "SEXO_CON2": 1, "EDAD_CON2": 2, "ESCOL_CON2": 1, "CONACTCON2": 1}
TRAMOS = ((12, 20, 0.041), (20, 25, 0.197), (25, 30, 0.249), (30, 35, 0.179), (35, 40, 0.104), (40, 90, 0.230))


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


def _edades(rng, n):
    t = rng.choice(len(TRAMOS), n, p=[p for _a, _b, p in TRAMOS] / np.sum([p for _a, _b, p in TRAMOS]))
    lo = np.array([a for a, _b, _p in TRAMOS])[t]
    hi = np.array([b for _a, b, _p in TRAMOS])[t]
    return rng.integers(lo, hi)


def _frame(n=40000, seed=2024):
    rng = np.random.default_rng(seed)
    gen = np.where(rng.random(n) < 0.013, 2, 1)
    k1 = rng.integers(1, 8, n)
    k2 = np.where(rng.random(n) < 0.52, k1, rng.integers(1, 8, n))
    return pd.DataFrame({
        "ENT_REGIS": [f"{i:02d}" for i in rng.integers(1, 33, n)],
        "TAM_LOC_RE": rng.integers(1, 18, n),
        "ANIO_REGIS": 2024,
        "GENERO": gen,
        "SEXO_CON1": np.where(gen == 2, rng.integers(1, 3, n), 1),
        "EDAD_CON1": _edades(rng, n),
        "ESCOL_CON1": k1,
        "CONACTCON1": np.where(rng.random(n) < 0.78, 1, 2),
        "SEXO_CON2": np.where(gen == 2, rng.integers(1, 3, n), 2),
        "EDAD_CON2": _edades(rng, n),
        "ESCOL_CON2": k2,
        "CONACTCON2": np.where(rng.random(n) < 0.78, 1, 2),
    })


def _zip(tmp_path, df, miembro="MATRI24.dbf"):
    ruta = tmp_path / "matrimonios_base_datos_2024_dbf.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(miembro, dbf(df))
        z.writestr("CATEMLMA24.dbf", b"")
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
    assert out[f"{MOD.P}-C-TRABAJA-SEXO-MUJER-R"] is not None
    assert not any(k.startswith(f"{MOD.P}-C-EDAD-MEDIA") for k in out)


def test_conducta_sin_soporte_columna_ausente(tmp_path):
    out = MOD.medir(_inputs(_zip(tmp_path, _frame().drop(columns=["GENERO"]))), {})
    _ok(out)
    assert out[f"{MOD.P}-M-MISMO-SEXO-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-M-AMBOS-TRABAJAN-TOTAL-TODOS-R"] is not None


def test_categoria_vacia(tmp_path):
    df = _frame()
    df["TAM_LOC_RE"] = 15
    out = MOD.medir(_inputs(_zip(tmp_path, df)), {})
    _ok(out)
    assert out[f"{MOD.P}-M-MISMA-ESCOLARIDAD-TLOC-MENOS-2500-R"] is None
    assert out[f"{MOD.P}-C-TRABAJA-TLOC-MENOS-2500-R"] is None
    assert out[f"{MOD.P}-C-TRABAJA-TLOC-100MIL-MAS-R"] is not None


def test_r_coincide_con_celdas_del_sellado(tmp_path):
    S, _p = MOD.sellados()
    df, faltan = MOD.lee_payload_reservado(S, _zip(tmp_path, _frame()), S.CAMPOS)
    assert faltan == []
    r = MOD.mide_r(S, df)
    ym, em, _d = S.matrimonios(df, "2024")
    yc, ec = S.contrayentes(df)
    ref = S._celdas(ym, S.EJES_M, em)
    ref.update(S._celdas(yc, S.EJES_C, ec))
    for c, eje, cat in MOD.celdas_de(S):
        a, b = r.get((c, eje, cat)), ref[(c, eje, cat)][0]
        assert (a is None and b is None) or abs(a - b) < 1e-12, (c, eje, cat)


def test_miembro_ausente_para(tmp_path):
    with pytest.raises(MOD.G.ParoDeGuardia):
        MOD.medir(_inputs(_zip(tmp_path, _frame(), miembro="MATRI23.dbf")), {})


def test_auditoria_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert MOD.G.auditoria_ast(fuente) == []
    for mut in MOD.E.MUTACIONES:
        assert MOD.G.auditoria_ast(fuente + "\n\n" + mut), mut
