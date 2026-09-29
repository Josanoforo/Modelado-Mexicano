"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENIGH 2024 (expediente ENIGH-2024).

El esquema es el de los medidores sellados de los contendientes `CALC-ENIGH-CONSUMO-PISOS-0002` (`COLS_CONC`,
`COLS_HOG`, `COLS_GAS`) y `CALC-PDR1-ENIGH2022-0001` (`COLS_POB`, `COLS_GP`), en cinco ZIP sintéticos por tabla
(un miembro .csv cada uno). Ramas: con soporte (0 < K < N); conducta sin soporte (gastospersona sin `inscrip` ->
PDR1-PRIV y PDR1-CARGA None; gastoshogar sin `forma_pag1` -> PART-EFECTIVO None); categoría vacía (todo
`tam_loc` = 1 -> TLOC MENOS-2500 y ámbito RURAL None). Toda salida pasa `corrida0._valida_outputs` contra
`esquema_resultados()` sin no finitos, y el dictamen es del vocabulario. R coincide celda por celda con el punto
de los procedimientos sellados (`mide_ola` de CONSUMO y `mide` de PDR1 con 2 réplicas). Sin microdato.
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


REL = "forense/prereg-aperturas/ENIGH-2024/medidor_apertura_enigh_2024.py"
MOD = _load(REL, "ap_enigh_2024_t")
C, D, R, PC, PD_ = MOD.sellados()


def _tablas(nh=5000, seed=2024):
    rng = np.random.default_rng(seed)
    fv = np.array([f"{e:02d}{i:08d}" for e, i in zip(rng.integers(1, 33, nh), range(nh))])
    fh = np.ones(nh, dtype=int)
    rub = rng.gamma(2.0, 1.0, (nh, len(C.RUBROS))) * rng.uniform(2000, 20000, (nh, 1))
    conc = pd.DataFrame({"folioviv": fv, "foliohog": fh, "tam_loc": rng.integers(1, 5, nh),
                         "est_dis": rng.integers(1, 40, nh), "upm": rng.integers(1, 400, nh),
                         "factor": rng.integers(50, 900, nh), "sexo_jefe": rng.integers(1, 3, nh),
                         "edad_jefe": rng.integers(18, 95, nh), "educa_jefe": rng.integers(1, 12, nh),
                         "ing_cor": rng.uniform(5000, 150000, nh)})
    for j, r in enumerate(C.RUBROS):
        conc[r] = rub[:, j]
    conc["gasto_mon"] = rub.sum(axis=1)
    conc["ali_fuera"] = conc["alimentos"] * rng.uniform(0, 0.4, nh) * (rng.random(nh) < 0.6)
    conc["bebidas"] = conc["alimentos"] * rng.uniform(0, 0.1, nh)
    for c in ("comunica", "prestamos", "pago_tarje", "deudas"):
        conc[c] = rng.uniform(0, 3000, nh) * (rng.random(nh) < 0.5)
    hog = pd.DataFrame({"folioviv": fv, "foliohog": fh, "celular": rng.choice([1, 2], nh, p=[0.9, 0.1]),
                        "conex_inte": rng.choice([1, 2], nh, p=[0.6, 0.4]),
                        "tarjeta": rng.choice([1, 2], nh, p=[0.2, 0.8]), "pagotarjet": rng.choice([1, 2, 0], nh)})
    ng = nh * 8
    hg = rng.integers(0, nh, ng)
    gas = pd.DataFrame({"folioviv": fv[hg], "foliohog": 1,
                        "clave": [f"A{i:03d}" for i in rng.integers(1, 260, ng)],
                        "tipo_gasto": rng.choice(["G1", "G2", "G3"], ng, p=[0.8, 0.1, 0.1]),
                        "forma_pag1": rng.choice([1, 2, 4, 5], ng, p=[0.8, 0.05, 0.1, 0.05]),
                        "forma_pag2": "", "forma_pag3": "",
                        "lugar_comp": rng.integers(1, 19, ng), "gasto_tri": rng.uniform(10, 3000, ng)})
    npers = nh * 3
    hp = np.repeat(np.arange(nh), 3)
    asis = rng.choice([1, 2], npers, p=[0.35, 0.65])
    pob = pd.DataFrame({"folioviv": fv[hp], "foliohog": 1, "numren": np.tile([1, 2, 3], nh),
                        "asis_esc": asis, "tipoesc": np.where(asis == 1, rng.choice([1, 2], npers, p=[0.85, 0.15]), "")})
    pr = pob[pob["tipoesc"].astype(str) == "2"].sample(frac=0.8, random_state=1)
    gp = pd.DataFrame({"folioviv": pr["folioviv"].to_numpy(), "foliohog": 1, "numren": pr["numren"].to_numpy(),
                       "clave": rng.choice(["E001", "E003", "E006"], len(pr)), "tipo_gasto": "G1",
                       "inscrip": rng.uniform(0, 3000, len(pr)), "colegia": rng.uniform(500, 9000, len(pr)),
                       "gasto_tri": rng.uniform(1000, 20000, len(pr))})
    ruido = pd.DataFrame({"folioviv": fv[:50], "foliohog": 1, "numren": 1, "clave": "J010", "tipo_gasto": "G1",
                          "inscrip": 0, "colegia": 0, "gasto_tri": 100.0})
    return {"conc": conc, "hog": hog, "gas": gas, "pob": pob, "gp": pd.concat([gp, ruido], ignore_index=True)}


def _zips(tmp_path, tablas):
    rutas = {}
    for t, df in tablas.items():
        ruta = tmp_path / f"{t}.zip"
        with zipfile.ZipFile(ruta, "w") as z:
            z.writestr(f"conjunto_de_datos/{t}.csv", df.to_csv(index=False))
        rutas[t] = str(ruta)
    return rutas


def _inputs(rutas):
    ins = {MOD.PAYLOADS[t]: {"ruta_absoluta": r} for t, r in rutas.items()}
    ins.update({k: {} for k, _r, _n in MOD.CONTRATO["repo"]})
    return ins


def _ok(out):
    assert corrida0._valida_outputs({"resultados": MOD.esquema_resultados()}, out) == []
    assert out[f"{MOD.P}-DICTAMEN"] in MOD.G.VOCABULARIO
    assert out[f"{MOD.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


@pytest.fixture(scope="module")
def base():
    return _tablas()


def test_con_soporte_de_punta_a_punta(tmp_path, base):
    out = MOD.medir(_inputs(_zips(tmp_path, base)), {})
    _ok(out)
    assert 0 < out[f"{MOD.P}-K"] < out[f"{MOD.P}-N"]
    for c in ("CONSUMO-HOG-TIENE-CELULAR-TOTAL-TODOS", "PDR1-PRIV-URBANO-D05", "PDR1-CARGA-TOTAL-B2-VIII",
              "PDR1-PRIV-SEXO-JEFE-MUJER", "CONSUMO-PART-ALIMENTOS-ENTIDAD-09"):
        assert out[f"{MOD.P}-{c}-R"] is not None, c
    assert not any("MEDIA-GASTO" in k or "-DIF-" in k for k in out)


def test_conducta_sin_soporte_columna_ausente(tmp_path, base):
    t = dict(base)
    t["gp"] = base["gp"].drop(columns=["inscrip"])
    t["gas"] = base["gas"].drop(columns=["forma_pag1"])
    out = MOD.medir(_inputs(_zips(tmp_path, t)), {})
    _ok(out)
    assert out[f"{MOD.P}-PDR1-PRIV-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-PDR1-CARGA-URBANO-TODOS-R"] is None
    assert out[f"{MOD.P}-PDR1-ASIPRIV-TOTAL-TODOS-R"] is not None
    assert out[f"{MOD.P}-CONSUMO-PART-EFECTIVO-EN-GASTO-DIRECTO-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-CONSUMO-HOG-COMPRA-FIADO-TOTAL-TODOS-R"] is None
    assert out[f"{MOD.P}-CONSUMO-PART-SALUD-TOTAL-TODOS-R"] is not None


def test_categoria_vacia(tmp_path, base):
    t = dict(base)
    t["conc"] = base["conc"].assign(tam_loc=1)
    out = MOD.medir(_inputs(_zips(tmp_path, t)), {})
    _ok(out)
    assert out[f"{MOD.P}-CONSUMO-HOG-TIENE-CELULAR-TLOC-MENOS-2500-R"] is None
    assert out[f"{MOD.P}-PDR1-ASIPRIV-RURAL-TODOS-R"] is None
    assert out[f"{MOD.P}-PDR1-ASIPRIV-URBANO-TODOS-R"] is not None


def test_r_coincide_con_el_punto_sellado(tmp_path, base):
    rutas = _zips(tmp_path, base)
    cols = MOD.columnas(C, D)
    fr = {}
    for t, ruta in rutas.items():
        fr[t], faltan = MOD.lee_payload_reservado(ruta, cols[t], ("clave", tuple(D.CLAVES_COLEG)) if t == "gp" else None)
        assert faltan == []
    r = MOD.mide_r(C, D, R, fr)
    ref_c, _d = C.mide_ola({"conc": fr["conc"], "hog": fr["hog"], "gas": fr["gas"]}, R, 2, 7)
    f, amb, seg, _d = D.prepara({"conc": fr["conc"][list(D.COLS_CONC)], "pob": fr["pob"], "gp": fr["gp"]}, R)
    ref_d = D.mide(f, amb, seg, R, 2, 7)
    for _cid, cont, c, eje, cat in MOD.celdas_de(C, D):
        a = r.get((cont, c, eje, cat))
        if cont == "CONSUMO":
            b = (ref_c.get((c, eje, cat)) or {}).get("p")
        elif c == "PRIV-SEG":
            b = ref_d["PRIV-SEG"][(cat, eje)][0]
        else:
            b = ref_d[c][(cat, eje)][0]
        b = None if b is None or not math.isfinite(b) else b
        assert (a is None and b is None) or abs(a - b) < 1e-9, (cont, c, eje, cat, a, b)


def test_auditoria_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert MOD.G.auditoria_ast(fuente) == []
    for mut in MOD.E.MUTACIONES:
        assert MOD.G.auditoria_ast(fuente + "\n\n" + mut), mut
