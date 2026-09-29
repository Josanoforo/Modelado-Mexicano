"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENPECYT (expediente ENPECYT-2017).

El esquema es el del medidor sellado del contendiente `CALC-ENPECYT-CONOC-PISOS-0001` (`campos_de("2015")`,
tablas CB1/CB2/CS en DBF dentro de un ZIP), que el medidor de apertura reusa por bytes. Ramas: con soporte;
conducta sin soporte (campo ausente → R None); categoría vacía. Toda salida pasa `corrida0._valida_outputs`
contra `esquema_resultados()` sin no finitos, y el dictamen es del vocabulario. Auditoría AST limpia y cada
mutación de `expediente_apertura.MUTACIONES` detectada.
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

REL = "forense/prereg-aperturas/ENPECYT-2017/medidor_apertura_enpecyt_2017.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


EP = _load(REL, "ap_enpecyt_2017_t")
M, PISO = EP.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": EP.esquema_resultados()}, out) == []
    assert out[f"{EP.P}-DICTAMEN"] in EP.G.VOCABULARIO
    assert out[f"{EP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _tablas(rng, n=1500):
    campos = M.campos_de(EP.OLA_CODIGOS)
    llave = {"CD_A": [f"{c:02d}" for c in rng.integers(1, 30, n)], "PER": ["1"] * n, "CON": [str(i) for i in range(n)],
             "V_SEL": ["1"] * n, "N_HOG": ["1"] * n, "N_REN": ["1"] * n}
    out = {}
    for t, cols in campos.items():
        d = {}
        for c in cols:
            if c in llave:
                d[c] = llave[c]
            elif c == "FAC":
                d[c] = [f"{v:.0f}" for v in rng.uniform(100, 3000, n)]
            elif c.startswith("S4P14_"):
                d[c] = [str(v) for v in rng.integers(1, 12, n)]
            elif c == "S4P1_3":
                d[c] = [str(v) for v in rng.integers(1, 5, n)]
            elif c.startswith("S4P"):
                d[c] = [str(v) for v in rng.integers(1, 6, n)]
            elif c == "SEX":
                d[c] = [str(v) for v in rng.integers(1, 3, n)]
            elif c == "EDA":
                d[c] = [str(v) for v in rng.integers(18, 90, n)]
            elif c == "NIV":
                d[c] = [str(v) for v in rng.integers(0, 11, n)]
            elif c == "EST_DIS":
                d[c] = [str(v) for v in rng.integers(1, 5, n)]
            elif c == "UPM_DIS":
                d[c] = [str(v) for v in rng.integers(1, 200, n)]
        out[t] = pd.DataFrame(d)
    return out


def _sale(tablas):
    return EP.E.salida(EP.P, EP.filas(M, EP.mide_r(M, tablas), PISO))


def test_con_soporte():
    out = _sale(_tablas(np.random.default_rng(17)))
    _ok(out)
    assert out[f"{EP.P}-N"] > 0
    assert out[f"{EP.P}-RESPETA-10-INVENTOR-TOTAL-TODOS-R"] is not None   # R se reporta; no se puntúa (sin ICC)


def test_total_e_inventor_no_se_puntuan():
    fl = EP.filas(M, {}, PISO)
    fuera = [f for f in fl if f["id"].endswith("-TOTAL-TODOS") or f["id"].startswith("RESPETA-10-INVENTOR-")]
    assert len(fuera) == 19 and all(f["lo"] is None and f["hi"] is None for f in fuera)
    assert sum(f["lo"] is not None and f["hi"] is not None for f in fl) == 81


def test_sin_soporte_y_categoria_vacia():
    t = _tablas(np.random.default_rng(18))
    t["cb2"]["S4P31_1_1"] = ""       # conducta sin soporte (campo vacío como lo deja un campo ausente)
    t["cs"]["SEX"] = "1"             # SEXO-MUJER vacía
    out = _sale(t)
    _ok(out)
    assert out[f"{EP.P}-FE-CIENCIA-ACUERDO-TOTAL-TODOS-R"] is None
    assert out[f"{EP.P}-INTERES-GRANDE-O-MAS-SEXO-MUJER-R"] is None
    assert out[f"{EP.P}-INTERES-GRANDE-O-MAS-SEXO-HOMBRE-R"] is not None


# ── extremo a extremo: DBF en ZIP con los nombres de miembro del contendiente ────────────────────
def _dbf(df):
    cols = list(df.columns)
    anchos = [max(1, int(df[c].astype(str).str.len().max())) for c in cols]
    nrec, lcab, lreg = len(df), 32 + 32 * len(cols) + 1, 1 + sum(anchos)
    b = bytearray(struct.pack("<BBBBIHH20x", 3, 126, 9, 29, nrec, lcab, lreg))
    for c, a in zip(cols, anchos):
        b += struct.pack("<11sc4xBB14x", c.encode("ascii"), b"C", a, 0)
    b += b"\x0D"
    for fila in df.astype(str).itertuples(index=False):
        b += b" " + b"".join(str(v).encode("latin-1").ljust(a)[:a] for v, a in zip(fila, anchos))
    return bytes(b + b"\x1A")


def _inputs(tmp_path, tablas, nombre="enpecyt2017_bd_dbf.zip"):
    z = tmp_path / nombre
    with zipfile.ZipFile(z, "w") as zf:
        for t, df in tablas.items():
            zf.writestr(f"ENPECYT2017_{t.upper()}.DBF", _dbf(df))
    inp = {EP.PAYLOAD: {"ruta_absoluta": str(z)}}
    inp.update({k: {} for k, _r, _n in EP.CONTRATO["repo"]})
    return inp


def test_medir_extremo_a_extremo_campo_ausente(tmp_path):
    t = _tablas(np.random.default_rng(19), n=400)
    t["cb2"] = t["cb2"].drop(columns=["S4P25_1"])
    out = EP.medir(_inputs(tmp_path, t), {})
    _ok(out)
    assert out[f"{EP.P}-GOB-INVERTIR-ACUERDO-TOTAL-TODOS-R"] is None
    assert out[f"{EP.P}-FE-CIENCIA-ACUERDO-TOTAL-TODOS-R"] is not None


def test_medir_paro_por_ponderador_ausente(tmp_path):
    t = _tablas(np.random.default_rng(20), n=100)
    t["cb1"] = t["cb1"].drop(columns=["FAC"])
    with pytest.raises(EP.G.ParoDeGuardia):
        EP.medir(_inputs(tmp_path, t), {})


def test_medir_paro_si_no_es_2017(tmp_path):
    t = _tablas(np.random.default_rng(21), n=100)
    with pytest.raises(EP.G.ParoDeGuardia):
        EP.medir(_inputs(tmp_path, t, nombre="enpecyt2015_bd_dbf.zip"), {})


# ── guardia E.6 ─────────────────────────────────────────────────────────────
def test_auditoria_limpia_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert EP.G.auditoria_ast(fuente) == []
    for mut in EP.E.MUTACIONES:
        assert EP.G.auditoria_ast(fuente + "\n\n" + mut), mut
