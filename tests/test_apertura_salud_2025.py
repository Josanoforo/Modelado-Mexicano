"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENSANUT 2025 y ENCODAT 2025.

El esquema es el del medidor sellado del contendiente (`COLS`, `COLS_IND`/`COLS_HOG`), que el medidor
de apertura reusa. Ramas: con soporte, conducta sin soporte (R None), categoría vacía. Toda salida pasa
`corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el dictamen es del vocabulario.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ENS = _load("forense/prereg-aperturas/ENSANUT-2025/medidor_apertura_ensanut_2025.py", "ap_ensanut_2025_t")
ENC = _load("forense/prereg-aperturas/ENCODAT-2025/medidor_apertura_encodat_2025.py", "ap_encodat_2025_t")


def _ok(Mod, out):
    assert corrida0._valida_outputs({"resultados": Mod.esquema_resultados()}, out) == []
    assert out[f"{Mod.P}-DICTAMEN"] in Mod.G.VOCABULARIO
    assert out[f"{Mod.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _fr_ensanut(M, rng, arch, n):
    d = {"folio_i": rng.integers(1, max(2, n // 3), n).astype(str), "folio_int": rng.integers(1, 4, n).astype(str),
         "ponde_f": rng.uniform(50, 500, n), "est_sel": rng.integers(1, 40, n).astype(str),
         "upm": rng.integers(1, 300, n).astype(str), "estrato": rng.integers(1, 4, n)}
    for c in M.COLS[arch]:
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
    return pd.DataFrame(d)


def _ensanut(mutar=None):
    M, R, piso = ENS.sellados()
    rng = np.random.default_rng(28)
    frames = {a: _fr_ensanut(M, rng, a, 6000 if a == "INTE" else 2000) for a in ENS.PAYLOADS}
    if mutar:
        mutar(frames)
    return ENS.E.salida(ENS.P, ENS.filas(M, ENS.mide_r(M, R, frames), piso))


def test_ensanut_con_soporte():
    out = _ensanut()
    _ok(ENS, out)
    assert out[f"{ENS.P}-N"] > 0


def test_ensanut_sin_soporte_y_categoria_vacia():
    def mutar(fr):
        fr["UTIL"]["u0201"] = np.nan          # conductas de utilizadores sin soporte
        fr["ADUL"]["estrato"] = 3             # RURAL y URBANO vacíos en adultos
    out = _ensanut(mutar)
    _ok(ENS, out)
    assert out[f"{ENS.P}-ATENCION-CURANDERO-HIERBERO-TOTAL-TODOS-R"] is None
    assert out[f"{ENS.P}-DEPRESION-CESD7-ESTRATO-RURAL-R"] is None


def _encodat(mutar=None):
    M, R, piso = ENC.sellados()
    rng = np.random.default_rng(29)
    nh = 1200
    hog = pd.DataFrame({"id_hogar": [f"{i:020d}" for i in range(nh)], "estrato": rng.integers(1, 4, nh),
                        "est_var": rng.integers(1, 30, nh), "code_upm": rng.integers(1, 300, nh).astype(str)})
    n = 3000
    hid = rng.integers(0, nh, n)
    ind = pd.DataFrame({"id_pers": [f"{h:020d}{k:02d}" for h, k in zip(hid, rng.integers(1, 5, n))],
                        "ponde_ss": rng.uniform(1, 9, n), "ds2": rng.integers(1, 3, n), "ds3": rng.integers(10, 70, n),
                        "ds9": rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9], n)})
    for c in M.COLS_IND:
        if c not in ind:
            ind[c] = rng.choice([1, 2, 9], n).astype(float)
    if mutar:
        mutar(ind, hog)
    return ENC.E.salida(ENC.P, ENC.filas(M, ENC.mide_r(M, R, {"IND": ind, "HOG": hog}), piso))


def test_encodat_con_soporte():
    out = _encodat()
    _ok(ENC, out)
    assert out[f"{ENC.P}-N"] > 0


def test_encodat_sin_soporte_y_categoria_vacia():
    def mutar(ind, hog):
        ind["tp1"] = np.nan
        hog["estrato"] = 3
    out = _encodat(mutar)
    _ok(ENC, out)
    assert out[f"{ENC.P}-CONSULTO-PROFESIONAL-POR-CONSUMO-TOTAL-TODOS-R"] is None
    assert out[f"{ENC.P}-ALCOHOL-12M-ESTRATO-RURAL-R"] is None


class _RFalso:
    """Imita `lee_dta` de la receta: KeyError con los nombres ausentes, como tools/dominios/salud/pisos_diseno.py."""
    def __init__(self, df):
        self.df = df

    def lee_dta(self, ruta, columnas, encoding=None):
        faltan = [c for c in columnas if c not in self.df.columns]
        if faltan:
            raise KeyError(f"columnas ausentes en m.dta: {faltan}")
        return self.df[list(columnas)].copy()


def test_columna_de_reactivo_ausente_sale_vacia_y_de_diseno_para():
    M, _R, _p = ENS.sellados()
    df = _fr_ensanut(M, np.random.default_rng(3), "ADUL", 50).drop(columns=["a1211"])
    leido = ENS.lee_payload_reservado(_RFalso(df), M, "ADUL", "/x")
    assert leido["a1211"].isna().all() and len(leido) == 50
    try:
        ENS.lee_payload_reservado(_RFalso(df.drop(columns=["ponde_f"])), M, "ADUL", "/x")
    except ENS.G.ParoDeGuardia:
        pass
    else:
        raise AssertionError("diseño ausente debía ser PARO")
