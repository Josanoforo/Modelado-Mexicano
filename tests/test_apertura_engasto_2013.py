"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENGASTO (expediente ENGASTO-2013).

El esquema es el del medidor sellado del contendiente `CALC-ENGASTO-CONSUMO-PISOS-0001` (`COLS`,
`LLAVE_HOG`, `LLAVE_VIV`), que el medidor de apertura reusa por bytes. Ramas: con soporte; conducta sin
soporte (LUGAR_COMPRA ausente de la ola → R None; `num_cel` ausente en HOGAR → R None); categoría vacía.
Toda salida pasa `corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el dictamen
es del vocabulario. Auditoría AST limpia y cada mutación de `expediente_apertura.MUTACIONES` detectada.
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

REL = "forense/prereg-aperturas/ENGASTO-2013/medidor_apertura_engasto_2013.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


EG = _load(REL, "ap_engasto_2013_t")
M, R, PISO = EG.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": EG.esquema_resultados()}, out) == []
    assert out[f"{EG.P}-DICTAMEN"] in EG.G.VOCABULARIO
    assert out[f"{EG.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _frames(rng, n=1500):
    folio = [f"{i:06d}" for i in range(n)]
    base = {"anio_reg": ["2013"] * n, "trimestre": [str(t) for t in rng.integers(1, 5, n)], "folio": folio}
    hog = pd.DataFrame(dict(base, hog_ent_1=["1"] * n, hog_ent_2=["0"] * n,
                            num_cel=rng.integers(0, 4, n).astype(float), conex_inte=rng.integers(1, 3, n).astype(float),
                            factor_hog=rng.uniform(50, 900, n)))
    viv = pd.DataFrame(dict(base, tam_loc=rng.integers(1, 5, n).astype(float),
                            est_dis=[str(e) for e in rng.integers(1, 30, n)], upm=[str(u) for u in rng.integers(1, 400, n)]))
    aj = pd.DataFrame(dict(base, hog_ent_1=["1"] * n, hog_ent_2=["0"] * n, sexo_je=rng.integers(1, 3, n).astype(float),
                           edad_je=rng.integers(18, 90, n).astype(float), ned_je=rng.integers(1, 5, n).astype(float)))
    return {"hogar": hog, "vivienda": viv, "ajustado": aj}


def _sale(frames):
    return EG.E.salida(EG.P, EG.filas(M, EG.mide_r(M, R, frames), PISO))


def test_con_soporte_y_tabla_ausente():
    out = _sale(_frames(np.random.default_rng(13)))
    _ok(out)
    assert out[f"{EG.P}-N"] > 0
    assert out[f"{EG.P}-CONEX-INTERNET-TOTAL-TODOS-R"] is not None
    # LUGAR_COMPRA no existe en la ola: toda conducta que la usa sale sin R (NO-ESTIMABLE por construcción)
    assert out[f"{EG.P}-GRAN-COMPRA-MERCADO-TOTAL-TODOS-R"] is None
    assert out[f"{EG.P}-COMPRA-INTERNET-ALGUN-RUBRO-TOTAL-TODOS-R"] is None


def test_sin_soporte_y_categoria_vacia():
    fr = _frames(np.random.default_rng(14))
    fr["hogar"]["num_cel"] = np.nan          # conducta sin soporte
    fr["vivienda"]["tam_loc"] = 1.0          # TLOC con sólo 100MIL-MAS: las otras categorías vacías
    out = _sale(fr)
    _ok(out)
    assert out[f"{EG.P}-TIENE-CELULAR-TOTAL-TODOS-R"] is None
    assert out[f"{EG.P}-CONEX-INTERNET-TLOC-MENOS-2500-R"] is None
    assert out[f"{EG.P}-CONEX-INTERNET-TLOC-100MIL-MAS-R"] is not None


def test_todo_vacio_no_estimable():
    fr = _frames(np.random.default_rng(15))
    fr["hogar"]["factor_hog"] = 0.0
    out = _sale(fr)
    _ok(out)
    assert out[f"{EG.P}-DICTAMEN"] == "NO-ESTIMABLE"


# ── extremo a extremo: .dta en ZIP bajo engasto2013/, columna ausente, PARO estructural ─────────
def _zip_dta(d, nombre, df):
    import pyreadstat
    dta = os.path.join(d, nombre + ".dta")
    pyreadstat.write_dta(df, dta)
    z = os.path.join(d, nombre + "_dta.zip")
    with zipfile.ZipFile(z, "w") as zf:
        zf.write(dta, nombre + ".dta")
    return z


def _inputs(tmp_path, fr, carpeta="engasto2013"):
    d = tmp_path / carpeta
    d.mkdir()
    rutas = {t: _zip_dta(str(d), t, fr[t]) for t in fr}
    inp = {pid: {"ruta_absoluta": rutas[t]} for t, pid in EG.PAYLOADS.items()}
    inp.update({k: {} for k, _r, _n in EG.CONTRATO["repo"]})
    return inp


def test_medir_extremo_a_extremo_columna_ausente(tmp_path):
    fr = _frames(np.random.default_rng(16), n=600)
    fr["hogar"] = fr["hogar"].drop(columns=["num_cel"]).assign(num_cel1=1.0, num_cel2=0.0)  # trazado 2013
    out = EG.medir(_inputs(tmp_path, fr), {})
    _ok(out)
    assert out[f"{EG.P}-TIENE-CELULAR-TOTAL-TODOS-R"] is None
    assert out[f"{EG.P}-CONEX-INTERNET-TOTAL-TODOS-R"] is not None


def test_medir_paro_por_ponderador_ausente(tmp_path):
    fr = _frames(np.random.default_rng(17), n=200)
    fr["hogar"] = fr["hogar"].drop(columns=["factor_hog"])
    with pytest.raises(EG.G.ParoDeGuardia):
        EG.medir(_inputs(tmp_path, fr), {})


def test_medir_paro_si_no_es_la_carpeta_2013(tmp_path):
    fr = _frames(np.random.default_rng(18), n=200)
    with pytest.raises(EG.G.ParoDeGuardia):
        EG.medir(_inputs(tmp_path, fr, carpeta="engasto2012"), {})


# ── guardia E.6 ─────────────────────────────────────────────────────────────
def test_auditoria_limpia_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert EG.G.auditoria_ast(fuente) == []
    for mut in EG.E.MUTACIONES:
        assert EG.G.auditoria_ast(fuente + "\n\n" + mut), mut
