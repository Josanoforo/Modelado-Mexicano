"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de LAPOP México 2023 (expediente LAPOP-2023,
reactivos de CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001).

Defecto real que atrapa: D-22 (conducto que no acepta una rama terminal; actos perdidos del piloto 3) y NC-0328.
El esquema es el del medidor sellado (columnas que `columnas_pedidas` deriva de sus tablas, diseño de su ola 2019).
Ramas: con soporte; conducta sin soporte (R None, incluidos los reactivos sólo 2004/2006 ausentes); categoría
vacía; y el conducto completo `medir()` sobre un .dta sintético; PARO si falta una columna de diseño.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

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


REL = "forense/prereg-aperturas/LAPOP-2023/medidor_apertura_lapop_2023.py"
LP = _load(REL, "ap_lapop_2023_t")
S = LP.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": LP.esquema_resultados()}, out) == []
    assert out[f"{LP.P}-DICTAMEN"] in LP.G.VOCABULARIO
    assert out[f"{LP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _frame(n=1600, seed=51):
    rng = np.random.default_rng(seed)
    d = {c: rng.choice([1, 2, 3, 4, 5, 6, 7, 888888], n).astype(float) for c in LP.columnas_pedidas(S)}
    d["wt"] = np.ones(n)
    d["estratopri"] = rng.integers(1, 6, n).astype(float)
    d["upm"] = rng.integers(1, 120, n).astype(float)
    d["q1"] = rng.integers(1, 3, n).astype(float)
    d["q2"] = rng.integers(16, 90, n).astype(float)
    d["ed"] = rng.integers(0, 19, n).astype(float)
    d["ur"] = rng.integers(1, 3, n).astype(float)
    for c in ("d5", "e16"):
        d[c] = rng.integers(1, 11, n).astype(float)
    return pd.DataFrame(d)


def _sale(frame):
    return LP.E.salida(LP.P, LP.filas(S, LP.mide_r(S, frame)))


def test_lapop_con_soporte():
    out = _sale(_frame())
    _ok(out)
    assert out[f"{LP.P}-N"] > 0
    assert out[f"{LP.P}-CONFIANZA-INTERPERSONAL-UR-RURAL-R"] is not None


def test_lapop_sin_soporte_y_categoria_vacia():
    f = _frame().drop(columns=["b10a", "b14", "cp9", "cp5", "aut1", "e16"])   # reactivos sólo 2004/2006
    f["ur"] = 1.0                                                           # RURAL vacía
    f["it1"] = 888888.0                                                     # sólo no respuesta
    out = _sale(f)
    _ok(out)
    assert out[f"{LP.P}-CONFIA-JUSTICIA-TOTAL-TODOS-R"] is None
    assert out[f"{LP.P}-CONFIANZA-INTERPERSONAL-TOTAL-TODOS-R"] is None
    assert out[f"{LP.P}-CONFIA-FFAA-UR-RURAL-R"] is None
    assert out[f"{LP.P}-CONFIA-FFAA-UR-URBANO-R"] is not None


def test_lapop_sin_ejes_opcionales():
    out = _sale(_frame().drop(columns=["q1", "ed", "ur"]))    # como 2021: ejes -> NO-ESTIMABLE, TOTAL sí
    _ok(out)
    assert out[f"{LP.P}-CONFIA-FFAA-SEXO-MUJER-R"] is None
    assert out[f"{LP.P}-CONFIA-FFAA-TOTAL-TODOS-R"] is not None


def _inputs(ruta):
    d = {LP.PAY: {"ruta_absoluta": ruta}}
    d.update({k: {} for k, _r, _n in LP.CONTRATO["repo"]})
    return d


def test_lapop_medir_conducto_completo(tmp_path):
    import pyreadstat
    f = _frame(900, 52)
    ruta = tmp_path / "MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta"
    pyreadstat.write_dta(f, str(ruta))
    out = LP.medir(_inputs(str(ruta)), {})
    _ok(out)
    esperado = LP.mide_r(S, f)[("CONFIA-FFAA", "TOTAL", "TODOS")]
    assert out[f"{LP.P}-CONFIA-FFAA-TOTAL-TODOS-R"] == pytest.approx(esperado, abs=1e-12)
    malo = tmp_path / "sin_upm.dta"
    pyreadstat.write_dta(f.drop(columns=["upm"]), str(malo))
    with pytest.raises(LP.G.ParoDeGuardia):
        LP.medir(_inputs(str(malo)), {})


def test_lapop_guardia_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert LP.G.auditoria_ast(src) == []
    for mut in LP.E.MUTACIONES:
        assert LP.G.auditoria_ast(src + "\n\n" + mut), mut
