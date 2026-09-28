#!/usr/bin/env python3
"""PDR1 · pieza ENVIPE2025 (ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1) · prueba sintética.

Fabrica un zip con la forma del real (miembro tper_vic1 bajo carpeta, cabecera con
comillas, BOM, fin de línea `\\r` solo, columnas extra), con TODAS las categorías reales
(ESTRATO 1-4, AP4_3_1 1/2/9, DOMINIO U/C/R, 4 grupos de edad), corre `medir()` y exige:
ids emitidos == ids del spec.yaml, `corrida0._valida_outputs(spec, out) == []`,
ningún str > 1024 bytes (VALOR-LARGO), y el dictamen B-bis mecánico.
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
CALC = os.path.join(ROOT, "data", "corrida0", "CALC-PDR1-ENVIPE2025-0001")
sys.path.insert(0, os.path.join(ROOT, "tools"))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _load(os.path.join(CALC, "medidor.py"), "medidor_pdr1_envipe2025")


def _csv(n, seed=7, vacio_e1=False):
    rng = np.random.default_rng(seed)
    cols = ["ID_VIV", "ID_PER", "UPM", "SEXO", "EDAD", "AP4_1", "AP4_3_1", "AP4_8_5", "AP4_9_5",
            "AP4_11_06", "FAC_HOG", "FAC_ELE", "DOMINIO", "ESTRATO", "EST_DIS", "UPM_DIS"]
    filas = ['"' + '","'.join(cols) + '"']
    for i in range(n):
        est = 1 + i % 4
        if vacio_e1 and est == 1:
            est = 2
        r5 = int(rng.choice([1, 2, 3, 9]))
        y2 = int(rng.choice([1, 2, 9])) if r5 == 1 else ""
        filas.append(",".join(str(x) for x in [
            f"{i:07d}", f"{i:07d}.01", i // 5, 1 + i % 2, int(rng.integers(18, 99)), 1,
            int(rng.choice([1, 2, 9])), r5, y2, int(rng.choice([1, 2, 9])), 100,
            int(rng.integers(50, 900)), "UCR"[i % 3], est, f"{(i // 40) % 6:03d}", f"{i // 5:05d}"]))
    return ("﻿" + "\r".join(filas) + "\r").encode("utf-8")


def _payload(tmp, **kw):
    ruta = os.path.join(tmp, "envipe2025_csv.zip")
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv",
                   _csv(2400, **kw))
        z.writestr("tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv", b"x")
    return ruta


def _spec():
    with open(os.path.join(CALC, "spec.yaml"), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _corre(tmp, **kw):
    import corrida0
    spec = _spec()
    out = M.medir({M.PAYLOAD_ID: {"ruta_absoluta": _payload(str(tmp), **kw)}}, spec)
    assert set(out) == {r["id"] for r in spec["resultados"]}
    assert corrida0._valida_outputs(spec, out) == []
    for v in out.values():
        assert not (isinstance(v, float) and not math.isfinite(v))
        if isinstance(v, str):
            assert len(v.encode("utf-8")) <= 1024
    return out


def test_sintetico(tmp_path):
    out = _corre(tmp_path)
    assert out["RESULT-PDR1-ENVIPE2025-RGB913-N-FILAS"] == 2400
    assert out["RESULT-PDR1-ENVIPE2025-RGB913-DICTAMEN"] in ("CONFIRMA", "MATIZA", "ROMPE")


def test_degenerado_sin_estrato_bajo(tmp_path):
    out = _corre(tmp_path, vacio_e1=True)
    assert out["RESULT-PDR1-ENVIPE2025-RGB913-DICTAMEN"] == "NO-ESTIMABLE"


def test_dictamen_mecanico():
    assert M.dictamen(3.0, 0.1, 5.0, 3.0) == "CONFIRMA"
    assert M.dictamen(2.9, 0.1, 5.0, 3.0) == "MATIZA"
    assert M.dictamen(4.0, -0.1, 8.0, 3.0) == "MATIZA"
    assert M.dictamen(-1.0, -2.0, -0.1, 3.0) == "ROMPE"
    assert M.dictamen(-1.0, -2.0, 0.1, 3.0) == "MATIZA"
    assert M.dictamen(None, None, None, 3.0) == "NO-ESTIMABLE"
