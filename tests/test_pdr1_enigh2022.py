"""Prueba sintética D-22 de CALC-PDR1-ENIGH2022-0001 (ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza
P-ENIGH2022). Sin microdato: fabrica un ZIP con la misma forma que `enigh2022_nc_csv` (miembros en
subcarpeta, BOM UTF-8, CRLF, columnas del descriptor) y corre `medir()` completo. Exige
`corrida0._valida_outputs(spec, out) == []`, que `resultados:` del spec.yaml sea exactamente
`esquema_resultados()`, que ningún texto pase de 1024 bytes (límite VALOR-LARGO de `run`) y que las
ramas degeneradas (sin hogares privados; bloque vacío) salgan null declarado, no NaN.
Defecto que atrapa: dos piezas del acto perdidas por VALOR-LARGO y ids tecleados.
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
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402

CALC = "CALC-PDR1-ENIGH2022-0001"


def _load(path, name):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = _load(f"data/corrida0/{CALC}/medidor.py", "m_pdr1_enigh2022")
RECETA = os.path.join(ROOT, "tools/dominios/salud/pisos_diseno.py")


def _csv(df):
    return ("﻿" + df.to_csv(index=False, lineterminator="\r\n")).encode("utf-8")


def _zip(tmp, sin_privados=False, n=600, seed=7):
    rng = np.random.default_rng(seed)
    fv = [f"{(i % 32) + 1:02d}{i:08d}" for i in range(n)]
    est = [str(1 + i % 8) for i in range(n)]
    est[3] = "99"  # estrato con UPM única
    upm = [f"{e}{i % 5}" if e != "99" else "990" for i, e in enumerate(est)]
    conc = pd.DataFrame({
        "folioviv": fv, "foliohog": "1", "ubica_geo": "01001", "tam_loc": [str(1 + i % 4) for i in range(n)],
        "est_socio": "2", "est_dis": est, "upm": upm, "factor": [str(x) for x in rng.integers(50, 900, n)],
        "sexo_jefe": [str(1 + i % 2) for i in range(n)], "edad_jefe": [str(18 + i % 70) for i in range(n)],
        "ing_cor": [f"{x:.2f}" for x in rng.uniform(3000, 200000, n)], "gasto_mon": "100"})
    conc.loc[7, "ing_cor"] = "0"  # carga con ingreso cero: fuera de CARGA
    pob, gp = [], []
    for i in range(n):
        for r in range(1, 4):
            asis = "1" if (i + r) % 3 else "2"
            tipo = "2" if (not sin_privados and asis == "1" and (i * r) % 4 == 0) else ("1" if asis == "1" else "")
            pob.append({"folioviv": fv[i], "foliohog": "1", "numren": f"{r:02d}", "sexo": "1", "edad": "10",
                        "asis_esc": asis, "nivel": "06", "tipoesc": tipo})
            if asis == "1":
                pag = tipo == "2" or (i % 7 == 0)
                gp.append({"folioviv": fv[i], "foliohog": "1", "numren": f"{r:02d}",
                           "clave": f"E00{1 + r}", "tipo_gasto": "G1" if i % 11 else "G4",
                           "inscrip": "500" if pag else "", "colegia": "1500" if pag else "0",
                           "material": "10", "gasto_tri": f"{rng.uniform(100, 20000):.2f}", "factor": "1"})
        gp.append({"folioviv": fv[i], "foliohog": "1", "numren": "01", "clave": "A001", "tipo_gasto": "G1",
                   "inscrip": "", "colegia": "", "material": "", "gasto_tri": "5", "factor": "1"})
    gp.append({"folioviv": "0100000000", "foliohog": "9", "numren": "05", "clave": "E001", "tipo_gasto": "G1",
               "inscrip": "1", "colegia": "1", "material": "", "gasto_tri": "5", "factor": "1"})  # sin persona
    ruta = os.path.join(tmp, "enigh2022_nc_csv.zip")
    with zipfile.ZipFile(ruta, "w") as z:
        for t, df in (("concentradohogar", conc), ("poblacion", pd.DataFrame(pob)),
                      ("gastospersona", pd.DataFrame(gp))):
            base = f"conjunto_de_datos_{t}_enigh2022_ns"
            z.writestr(f"{base}/conjunto_de_datos/{base}.csv", _csv(df))
    return ruta


def _corre(tmp, **kw):
    inputs = {"enigh2022_nc_csv": {"ruta_absoluta": _zip(tmp, **kw)},
              "receta_pisos": {"bytes": open(RECETA, "rb").read(), "sha256": "x"}}
    return M.medir(inputs, {"parametros": {"bootstrap_replicas": 60}, "seed": {"valor": 42}})


def _valida(out):
    esq = M.esquema_resultados()
    assert corrida0._valida_outputs({"resultados": esq}, out) == []
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k
        if isinstance(v, str):
            assert len(v.encode("utf-8")) <= 1024, k


def test_con_soporte(tmp_path):
    out = _corre(str(tmp_path))
    _valida(out)
    assert out[f"{M.P}-DICTAMEN-RG-cc1c9ab8f1"] in M.DICTAMENES
    assert out[f"{M.P}-G-FILAS-GP-SIN-PERSONA"] == 1
    for d in M.DECILES:
        assert out[M.rid("PRIV", "TOTAL", d, "N")] > 0
    p = out[M.rid("PRIV", "URBANO", "B2-VIII", "P")]
    assert p is not None and 0 <= p <= 1


def test_sin_privados_degenera_en_null(tmp_path):
    out = _corre(str(tmp_path), sin_privados=True)
    _valida(out)
    assert out[M.rid("CARGA", "URBANO", "TODOS", "P")] is None
    assert out[f"{M.P}-DICTAMEN-RG-cc1c9ab8f1"] in ("ROMPE", "NO-CONSTRUIBLE")


def test_dictamen_mecanico():
    assert M.dictamen(None, 0.1) == "NO-CONSTRUIBLE"
    assert M.dictamen(0.0, 0.1) == "ROMPE"
    assert M.dictamen(-0.01, 0.1) == "ROMPE"
    assert M.dictamen(0.01, 0.0) == "CONFIRMA"
    assert M.dictamen(0.01, -0.001) == "MATIZA"


def test_spec_yaml_es_el_esquema():
    with open(os.path.join(ROOT, "data", "corrida0", CALC, "spec.yaml")) as f:
        spec = yaml.safe_load(f)
    assert spec["resultados"] == M.esquema_resultados()
