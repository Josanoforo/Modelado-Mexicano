"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENOE (tabla SDEMT) para el expediente
de apertura ENOE 2026T2.

El esquema es el del medidor sellado del contendiente (`COLS_CRUDAS`: r_def, c_res, eda, sex, cs_p17, clase1,
clase2, t_loc_tri, niv_ins, ent, fac_tri, est_d_tri, upm). Se fabrica un ZIP con `ENOE_SDEMT226.csv` (y un
miembro ajeno) y se corre la lectura real. Ramas: con soporte; conducta sin soporte (columna ausente → R
None); categoría vacía; diseño ausente → PARO. Toda salida pasa `corrida0._valida_outputs`, sin no finitos,
dictamen del vocabulario; auditoría AST limpia y cada mutación detectada.
"""
from __future__ import annotations

import importlib.util
import io
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

REL = "forense/prereg-aperturas/ENOE-2026T2/medidor_apertura_enoe_2026t2.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AP = _load(REL, "ap_enoe_2026t2_t")


def _ok(out):
    assert corrida0._valida_outputs({"resultados": AP.esquema_resultados()}, out) == []
    assert out[f"{AP.P}-DICTAMEN"] in AP.G.VOCABULARIO
    assert out[f"{AP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _sdemt(rng, n, quitar=(), tloc=None):
    d = {"r_def": rng.choice(["00", "15"], n, p=[0.95, 0.05]), "c_res": rng.choice([1, 2, 3], n, p=[0.9, 0.05, 0.05]),
         "eda": rng.integers(0, 99, n), "sex": rng.integers(1, 3, n), "cs_p17": rng.choice([1, 2, 9], n),
         "clase1": rng.choice([1, 2], n), "clase2": rng.integers(1, 5, n),
         "t_loc_tri": (np.full(n, tloc) if tloc is not None else rng.integers(1, 5, n)),
         "niv_ins": rng.integers(1, 6, n), "ent": rng.integers(1, 33, n),
         "fac_tri": rng.integers(50, 900, n), "est_d_tri": rng.integers(1, 60, n), "upm": rng.integers(1, 800, n)}
    return pd.DataFrame(d).drop(columns=list(quitar))


def _zip(tmp_path, df):
    ruta = tmp_path / "enoe_2026_trim2_csv.zip"
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("ENOE_SDEMT226.csv", buf.getvalue())
        z.writestr("ENOE_VIVT226.csv", "loc,mun\n1,1\n")
    return str(ruta)


def _corre(tmp_path, **kw):
    S, R, M, piso = AP.sellados()
    frame = AP.lee_payload_reservado(S, R, _zip(tmp_path, _sdemt(np.random.default_rng(226), 6000, **kw)))
    return AP.E.salida(AP.P, AP.filas(S, M, AP.mide_r(S, M, frame), piso))


def test_enoe_con_soporte(tmp_path):
    out = _corre(tmp_path)
    _ok(out)
    assert out[f"{AP.P}-N"] > 0
    assert out[f"{AP.P}-PARTICIPA-ECONOMICAMENTE-TOTAL-TODOS-R"] is not None


def test_enoe_sin_soporte_y_categoria_vacia(tmp_path):
    out = _corre(tmp_path, quitar=("cs_p17",), tloc=1)
    _ok(out)
    assert out[f"{AP.P}-NO-ESTUDIA-NI-OCUPADO-18-24-TOTAL-TODOS-R"] is None
    assert out[f"{AP.P}-PARTICIPA-ECONOMICAMENTE-LOCALIDAD-MENOS-2500-R"] is None
    assert out[f"{AP.P}-PARTICIPA-ECONOMICAMENTE-LOCALIDAD-100MIL-MAS-R"] is not None


def test_enoe_diseno_ausente_es_paro(tmp_path):
    S, R, _M, _p = AP.sellados()
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(S, R, _zip(tmp_path, _sdemt(np.random.default_rng(1), 50, quitar=("fac_tri",))))


def test_enoe_auditoria_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert AP.G.auditoria_ast(src) == []
    for mut in AP.E.MUTACIONES:
        assert AP.G.auditoria_ast(src + "\n\n" + mut), mut
