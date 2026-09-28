#!/usr/bin/env python3
"""PDR1 · pieza ENSU2024 (ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1) · prueba sintética.

Fabrica un payload con la forma del real (zip externo con zips trimestrales; CB con
BOM, comillas y fin de línea `\\r` solo; miembros de otros trimestres que NO deben
leerse), corre `medir()` y exige: ids emitidos == ids del spec.yaml,
`corrida0._valida_outputs(spec, out) == []`, sin no finitos; rama degenerada (sin
«no» en un segmento vacío) también pasa por el validador; el dictamen B-bis sale
mecánico sobre casos construidos.

Defecto real que atrapa: #941/#951 (preflight VERDE y `run` no sella por null no
declarado o id no listado) y CSV INEGI con `\\r` solo + BOM (memoria del proyecto).
"""
from __future__ import annotations

import importlib.util
import io
import math
import os
import sys
import zipfile

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC = os.path.join(ROOT, "data", "corrida0", "CALC-PDR1-ENSU2024-0001")
sys.path.insert(0, os.path.join(ROOT, "tools"))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _load(os.path.join(CALC, "medidor.py"), "medidor_pdr1_ensu2024")


def _cb(n, rng, sin_no=False):
    cols = ["ID_VIV", "ID_PER", "UPM", "CD", "SEXO", "EDAD", "BP1_5_1", "FAC_SEL", "UPM_DIS", "EST_DIS"]
    filas = ['"' + '","'.join(cols) + '"']
    for i in range(n):
        v = int(rng.choice([1, 2, 3, 9], p=[0.45, 0.45, 0.07, 0.03]))
        if sin_no and v == 2:
            v = 1
        edad = int(rng.integers(18, 97))
        filas.append(",".join(str(x) for x in [i, i, 100 + i // 5, f"{1 + i % 3:02d}", 1 + i % 2, edad, v,
                                               int(rng.integers(50, 900)), f"{i // 5:05d}", f"{(i // 20) % 4:04d}"]))
    return ("﻿" + "\r".join(filas) + "\r").encode("utf-8")


def _payload(tmp, sin_no=False):
    rng = np.random.default_rng(7)
    ext = io.BytesIO()
    with zipfile.ZipFile(ext, "w") as z:
        for mes, cb in (("marzo", "0324"), ("junio", "0624")):
            inner = io.BytesIO()
            with zipfile.ZipFile(inner, "w") as zi:
                zi.writestr(f"ENSU_CB_{cb}.csv", _cb(400, rng, sin_no) if mes == "marzo" else b"BASURA")
                zi.writestr(f"ENSU_CS_{cb}.csv", b"x")
            z.writestr(f"ensu_bd_{mes}_2024_csv.zip", inner.getvalue())
    ruta = os.path.join(tmp, "ENSU", "2024", "ensu_bd_2024_csv.zip")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "wb") as fh:
        fh.write(ext.getvalue())
    return ruta


def _spec():
    with open(os.path.join(CALC, "spec.yaml"), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _corre(tmp_path, sin_no=False):
    import corrida0
    spec = _spec()
    ruta = _payload(str(tmp_path), sin_no)
    out = M.medir({M.PAYLOAD_ID: {"ruta_absoluta": ruta}}, spec)
    assert set(out) == {r["id"] for r in spec["resultados"]}
    assert corrida0._valida_outputs(spec, out) == []
    for v in out.values():
        assert not (isinstance(v, float) and not math.isfinite(v))
    return out


def test_sintetico(tmp_path):
    out = _corre(tmp_path)
    assert out[f"{M.PREF}-G-FILAS-CB"] == 400
    assert out[f"{M.PREF}-DICTAMEN"] in {"CONFIRMA", "MATIZA", "ROMPE", "NO-CONSTRUIBLE"}


def test_degenerado(tmp_path):
    out = _corre(tmp_path, sin_no=True)
    assert out[f"{M.PREF}-PRINCIPAL-TOTAL-TODOS-P"] == 1.0


def test_ids_del_esquema():
    assert [r["id"] for r in _spec()["resultados"]] == [r["id"] for r in M.esquema_resultados()]


def test_dictamen_mecanico():
    assert M.dictamen(0.47, 0.46, 0.48, 0.474, 0.03) == "CONFIRMA"
    assert M.dictamen(0.459, 0.450, 0.468, 0.474, 0.03) == "MATIZA"
    assert M.dictamen(0.40, 0.39, 0.41, 0.474, 0.03) == "ROMPE"
    assert M.dictamen(None, None, None, 0.474, 0.03) == "NO-CONSTRUIBLE"
