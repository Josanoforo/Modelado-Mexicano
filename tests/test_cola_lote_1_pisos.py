"""D-22 de ACTO GEN2-COLA-LOTE-1 (25/sep/2026): pisos de la cola v1.1, lote 1.

Specs: forense/prereg-caja/{CCPV-FAM,EMAT-PAREJA,ENPECYT-CONOC,EDR-SUICIDIO}-PISOS-spec-v1_0.md §5.
Sintético sin microdato: las ramas terminales de cada medidor (con soporte, fuera de universo,
código no especificado, categoría vacía, llave sin jefe o con dos, UPM única de estrato, ola
reservada rechazada por la guardia) pasan el conducto que sella (`corrida0._valida_outputs`)
sin NaN ni inf, y `resultados:` del spec.yaml es exactamente `esquema_resultados()`.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_cola_lote_1_test")
RECETA_BYTES = open(os.path.join(ROOT, "tools/dominios/salud/pisos_diseno.py"), "rb").read()


def _spec(calc):
    with open(os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")) as f:
        return yaml.safe_load(f)


def _sin_no_finitos(out):
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k


def _cierra(M, out, extra):
    for k, v in extra.items():
        out[f"{M.P}-G-{k}"] = v
    assert corrida0._valida_outputs({"resultados": M.esquema_resultados()}, out) == []
    _sin_no_finitos(out)
    return out


# ═══════════════════════════ CCPV ═══════════════════════════

CCPV = _load("data/corrida0/CALC-CCPV-FAM-PISOS-0001/medidor.py", "m_ccpv_fam")


def _ccpv_marco():
    viv, per = [], []
    rng = np.random.default_rng(7)
    for i in range(120):
        ent = f"{1 + i % 5:02d}"
        est = "9" if i == 0 else str(1 + i % 3)  # estrato 9: UPM única (certeza)
        th = (1, 2, 3, 4, 5, 6, 9)[i % 7]
        viv.append({"ent": ent, "id_viv": str(i), "tipohog": th, "numpers": 0 if i == 3 else 1 + i % 6,
                    "factor": 0 if i == 4 else int(rng.integers(10, 90)), "estrato": est,
                    "upm": f"{est}{i % 4}", "tam_loc": 1 + i % 4})
        if i == 5:
            continue  # vivienda sin personas
        miembros = [1] if th == 5 else [1, 2, 3, 4, 6][: 2 + i % 4]
        if i == 6:
            miembros = [2, 3]  # sin jefe
        if i == 7:
            miembros = [1, 1, 3]  # dos jefes
        for j, par in enumerate(miembros):
            edad = (70 if th == 5 and i % 2 else 35 + 3 * j) if par != 4 else 8
            if i == 8 and j == 1:
                edad = 999
            per.append({"ent": ent, "id_viv": str(i), "sexo": (1, 3, 2)[(i + j) % 3] if i == 9 else (1, 3)[(i + j) % 2],
                        "edad": edad, "parent": 99 if (i == 10 and j == 1) else par, "nivacad": (0, 4, 10, 99)[j % 4],
                        "factor": int(rng.integers(10, 90)), "estrato": est, "upm": f"{est}{i % 4}",
                        "tam_loc": 1 + i % 4})
    return pd.DataFrame(viv), pd.DataFrame(per)


def test_ccpv_ramas_terminales_pasan_el_conducto():
    viv, per = _ccpv_marco()
    out = CCPV.mide(viv, per, R, 20, 1)
    out = _cierra(CCPV, out, {"BOOTSTRAP-REPLICAS": 20, "SEED": 1, "INPUT-RECETA-SHA256": "x",
                              "OLA-RESERVADA": "x"})
    assert out[f"{CCPV.P}-G-VIV-SIN-JEFE"] == 1
    assert out[f"{CCPV.P}-G-VIV-JEFE-MULTIPLE"] == 1
    assert out[f"{CCPV.P}-G-VIV-SIN-PERSONAS"] == 1
    assert out[f"{CCPV.P}-G-PER-SEXO-FUERA-CATALOGO"] >= 1
    # la proporción total de tipos de hogar suma 1 sin el 4 (familiar no especificado) ni el 9
    s = sum(out[CCPV.rid(c, "TOTAL", "TODOS", "P")] for c in
            ("HOG-NUCLEAR", "HOG-AMPLIADO", "HOG-COMPUESTO", "HOG-UNIPERSONAL", "HOG-CORRESIDENTES"))
    assert 0.0 < s < 1.0
    assert out[CCPV.rid("HOG-TAMANO-MEDIO", "TOTAL", "TODOS", "P")] > 1.0
    assert out[CCPV.rid("HOG-NUCLEAR", "ENT", "32", "N")] == 0


def test_ccpv_mujer_es_3():
    assert (CCPV.HOMBRE, CCPV.MUJER) == (1, 3)


def test_ccpv_guardia_rechaza_2020():
    inputs = {pid: {"ruta_absoluta": f"/x/ccpv/2010/MC2010_{e}_dta.zip"} for e, pid in CCPV.PAY.items()}
    inputs["receta_pisos"] = {"bytes": RECETA_BYTES}
    CCPV._guardia_inputs(inputs)
    inputs[CCPV.PAY["09"]] = {"ruta_absoluta": "/x/ccpv/2020/MC2010_09_dta.zip"}
    with pytest.raises(CCPV.ParoDeGuardia):
        CCPV._guardia_inputs(inputs)


def test_ccpv_spec_yaml_es_el_esquema():
    assert _spec("CALC-CCPV-FAM-PISOS-0001")["resultados"] == CCPV.esquema_resultados()
