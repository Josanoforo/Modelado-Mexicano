"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENSU (tabla CB, era 2021T2+) para el
expediente de apertura ENSU 2026.

El esquema es el del medidor sellado del contendiente (`marco`: CD, EST_DIS, UPM_DIS, FAC_SEL, UPM, VIV_SEL,
H_MUD, R_SEL, SEXO, EDAD y los reactivos de CONDUCTAS/FILTRO), que el medidor de apertura reusa por bytes.
Se fabrica un ZIP con `ensu_cb_0326.csv` y `ensu_cb_0626.csv` y se corre la lectura real
(`lee_payload_reservado`). Ramas: con soporte; conducta sin soporte (columna ausente → R None); categoría
vacía. Toda salida pasa `corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, el dictamen
es del vocabulario; la auditoría AST del medidor está limpia y cada mutación se detecta.
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

REL = "forense/prereg-aperturas/ENSU-2026/medidor_apertura_ensu_2026.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AP = _load(REL, "ap_ensu_2026_t")


def _ok(out):
    assert corrida0._valida_outputs({"resultados": AP.esquema_resultados()}, out) == []
    assert out[f"{AP.P}-DICTAMEN"] in AP.G.VOCABULARIO
    assert out[f"{AP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _cb(M, rng, n, quitar=(), edad=None):
    upm = rng.integers(1, 400, n)
    ent = rng.integers(1, 33, n)
    d = {"CD": rng.integers(1, 97, n).astype(str), "EST_DIS": rng.integers(1, 5, n).astype(str),
         "UPM_DIS": upm.astype(str), "FAC_SEL": rng.uniform(100, 900, n).round(2),
         "UPM": [f"{e:02d}{u:05d}" for e, u in zip(ent, upm)], "VIV_SEL": rng.integers(1, 20, n).astype(str),
         "H_MUD": "0", "R_SEL": "1", "SEXO": rng.integers(1, 3, n),
         "EDAD": (np.full(n, edad) if edad is not None else rng.integers(18, 90, n))}
    for c in M.CONDUCTAS:
        d[c[1]] = rng.choice(list(c[4]), n)
    for v, _cods in M.FILTRO.values():
        d[v] = rng.choice([1, 2], n)
    return pd.DataFrame(d).drop(columns=list(quitar))


def _zip(tmp_path, t1, t2):
    ruta = tmp_path / "ensu_bd_2026_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        for nombre, df in (("ensu_cb_0326.csv", t1), ("ensu_cb_0626.csv", t2)):
            buf = io.StringIO()
            df.to_csv(buf, index=False)
            z.writestr(f"ensu_bd_2026_csv/{nombre}", buf.getvalue().replace("\n", "\r\n"))
    return str(ruta)


def _corre(tmp_path, quitar=(), edad=None):
    M, R, D, piso, serie = AP.sellados()
    rng = np.random.default_rng(2026)
    ruta = _zip(tmp_path, _cb(M, rng, 3000, quitar, edad), _cb(M, rng, 3000, quitar, edad))
    marcos = AP.lee_payload_reservado(M, R, ruta)
    return AP.E.salida(AP.P, AP.filas(M, R, D, AP.mide_r(M, R, marcos), piso, serie))


def test_ensu_con_soporte(tmp_path):
    out = _corre(tmp_path)
    _ok(out)
    assert out[f"{AP.P}-N"] > 0
    assert out[f"{AP.P}-C01-INSEG-CIUDAD-TOTAL-TODOS-R"] is not None
    assert out[f"{AP.P}-C15-CORRUPCION-POLICIA-TOTAL-TODOS-R"] is not None   # R de 2026T2


def test_ensu_sin_soporte_y_categoria_vacia(tmp_path):
    out = _corre(tmp_path, quitar=("BP1_2_08",), edad=25)   # C03 sin columna; sólo 18-29
    _ok(out)
    assert out[f"{AP.P}-C03-INSEG-CAJERO-TOTAL-TODOS-R"] is None
    assert out[f"{AP.P}-C01-INSEG-CIUDAD-EDAD-60-MAS-R"] is None
    assert out[f"{AP.P}-C01-INSEG-CIUDAD-EDAD-18-29-R"] is not None


def test_ensu_sin_tabla_cb_es_paro(tmp_path):
    M, R, _D, _p, _s = AP.sellados()
    ruta = tmp_path / "vacio.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("leeme.txt", "nada")
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(M, R, str(ruta))


def test_ensu_auditoria_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert AP.G.auditoria_ast(src) == []
    for mut in AP.E.MUTACIONES:
        assert AP.G.auditoria_ast(src + "\n\n" + mut), mut


def test_ensu_contendiente_ic_calibrado_y_control_cruzado():
    M, R, D, piso, serie = AP.sellados()
    AP.control_cruzado(M, piso, serie)
    fl = AP.filas(M, R, D, {}, piso, serie)
    assert len(fl) == len([r for r in AP.esquema_resultados() if r["id"].endswith("-R")])
    con = [f for f in fl if f["lo"] is not None]
    assert con and all(f["lo"] <= f["punto"] <= f["hi"] for f in con)
