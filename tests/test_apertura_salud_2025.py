"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENSANUT 2025 y ENCODAT 2025.

El esquema es el del medidor sellado del contendiente (`COLS`, `COLS_IND`/`COLS_HOG`), que el medidor
de apertura reusa; en ENSANUT 2025, la unión con `COLS_INTE`/`COLS_ADUL` del segundo contendiente
(`CALC-MC2-ENSANUT2024-0001`, celdas `MC2-*`). Ramas: con soporte, conducta sin soporte (R None), categoría vacía. Toda salida pasa
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
    if arch == "INTE":                        # esquema de MC2 (integrantes): necesidad, búsqueda, motivos
        d["h0401"] = rng.choice([1, 2], n).astype(float)
        d["h0402"] = rng.choice([1, 5, 47, 48, 50, 59], n).astype(float)
        d["h0404"] = rng.choice([1, 2], n).astype(float)
        for c in ("h0405a", "h0405b", "h0405c"):
            d[c] = rng.choice([1, 2, 3, 4, 8, 13, 99, np.nan], n)
    if arch == "ADUL":                        # esquema de MC2 (adultos): diabetes, tratamiento, gasto, suspensión
        d["a0301"] = rng.choice([1, 2], n).astype(float)
        d["a0307"] = rng.choice([1, 2, 3, 4], n).astype(float)
        d["a0310a"] = rng.choice([0, 0, 350, 1200, 99999], n).astype(float)
        d["a0313"] = rng.choice([1, 2, 9], n).astype(float)
        d["a0314"] = rng.choice([1, 2, 3, 5, 6, 7, 10], n).astype(float)
    return pd.DataFrame(d)


def _ensanut(mutar=None):
    M, R, piso = ENS.sellados()
    rng = np.random.default_rng(28)
    frames = {a: _fr_ensanut(M, rng, a, 6000 if a == "INTE" else 2000) for a in ENS.PAYLOADS}
    if mutar:
        mutar(frames)
    M2, piso2 = ENS.sellados_mc2()
    return ENS.E.salida(ENS.P, ENS.todas_las_filas(M, R, piso, M2, piso2, frames))


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
        faltan = [c for c in columnas if c.lower() not in self.df.columns]
        if faltan:
            raise KeyError(f"columnas ausentes en m.dta: {faltan}")
        return self.df[[c.lower() for c in columnas]].copy()


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


# ── segundo contendiente: CALC-MC2-ENSANUT2024-0001 (celdas MC2-*) ──────────

def _mc2(out):
    return {k: v for k, v in out.items() if k.startswith(f"{ENS.P}-MC2-")}


def test_mc2_celdas_y_apartadas():
    M2, piso2 = ENS.sellados_mc2()
    C, F = ENS._celdas_y_difs_mc2(M2)
    ids = {r["id"] for r in ENS.esquema_resultados()}
    assert set(ENS.DUPLICADAS_MC2) <= set(C) and len(F) == 7
    assert {f"{ENS.P}-{c}-R" for c in ENS.DUPLICADAS_MC2.values()} <= ids        # su R la da PISOS-SALUD
    for c in list(ENS.DUPLICADAS_MC2) + F:                                         # apartadas sin abrir
        assert f"{ENS.P}-MC2-{c}-R" not in ids
    for c in ENS.celdas_mc2(M2):                                                   # IC publicado por MC2
        assert all(isinstance(piso2[f"{ENS.PFX_MC2}-{c}-{q}"], float) for q in ("P", "IC95-INF", "IC95-SUP")), c
    assert ENS.CALC_MC2 in ENS.CONTRATO["contendientes"]


def test_mc2_con_soporte():
    out = _ensanut()
    _ok(ENS, out)
    m = _mc2(out)
    assert len(m) == len(ENS.celdas_mc2(ENS.sellados_mc2()[0])) and all(v is not None for v in m.values())
    assert 0.0 <= out[f"{ENS.P}-MC2-DM-SUSPENDE-NAC-R"] <= 1.0


def test_mc2_sin_soporte_y_categoria_vacia():
    def mutar(fr):
        for c in ("h0405a", "h0405b", "h0405c"):
            fr["INTE"][c] = np.nan            # motivos de no búsqueda sin soporte
        fr["ADUL"]["a0313"] = np.nan          # suspensión sin soporte
        fr["INTE"]["estrato"] = 3             # RURAL y URBANO vacíos en integrantes
    out = _ensanut(mutar)
    _ok(ENS, out)
    assert out[f"{ENS.P}-MC2-ACCESO-NAC-R"] is None and out[f"{ENS.P}-MC2-NO-GRAVE-MUJER-R"] is None
    assert out[f"{ENS.P}-MC2-DM-SUSPENDE-NAC-R"] is None and out[f"{ENS.P}-MC2-DM-ECON-ACCESO-NAC-R"] is None
    assert out[f"{ENS.P}-MC2-BUSCO-MENTAL-RURAL-R"] is None
    assert out[f"{ENS.P}-MC2-BUSCO-NORURAL-R"] is not None
    assert out[f"{ENS.P}-MC2-DM-PAGA-NAC-R"] is not None


def test_mc2_columna_de_reactivo_ausente_sale_vacia_y_de_diseno_para():
    M, _R, _p = ENS.sellados()
    M2, _p2 = ENS.sellados_mc2()
    df = _fr_ensanut(M, np.random.default_rng(4), "INTE", 60).drop(columns=["h0405b"])
    leido = ENS.lee_payload_reservado(_RFalso(df), M, "INTE", "/x", M2)
    assert leido["h0405b"].isna().all() and len(leido) == 60 and "h0402" in leido
    try:
        ENS.lee_payload_reservado(_RFalso(df.drop(columns=["est_sel"])), M, "INTE", "/x", M2)
    except ENS.G.ParoDeGuardia:
        pass
    else:
        raise AssertionError("diseño ausente debía ser PARO")


def test_mc2_r_iguala_la_razon_del_medidor_sellado():
    """La R de una celda MC2 = Σw·y/Σw de `_estima` (punto) del medidor sellado, sobre el mismo sintético."""
    M, _R, _p = ENS.sellados()
    M2, _p2 = ENS.sellados_mc2()
    rng = np.random.default_rng(31)
    frames = {"INTE": _fr_ensanut(M, rng, "INTE", 3000), "ADUL": _fr_ensanut(M, rng, "ADUL", 2000)}
    r = ENS.mide_r_mc2(M2, frames)
    for a, (fr, ce, _c) in ENS.ARCH_MC2.items():
        d, _ = getattr(M2, fr)(a)
        C, _F = getattr(M2, ce)(d)
        est, _dis = M2._estima(d, C, [], 2, 1)
        for rid, _m, _y in C:
            c = rid[len(ENS.PFX_MC2) + 1:]
            if c in r:
                assert abs(r[c] - est[f"{rid}-P"]) < 1e-12, c
