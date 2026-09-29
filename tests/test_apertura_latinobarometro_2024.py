"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de Latinobarómetro 2024 (expediente
LATINOBAROMETRO-2024).

Defecto real que atrapa: D-22 (conducto que no acepta una rama terminal; actos perdidos del piloto 3) y NC-0328.
El esquema es el de los dos medidores sellados de 2023 (columnas que `columnas_pedidas` deriva de sus tablas).
Ramas: con soporte; conducta sin soporte (R None); categoría vacía; y el conducto completo `medir()` sobre un zip
sintético con .dta en español e inglés y filas de otro país; PARO si falta el peso o si el .dta español no es único.
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


REL = "forense/prereg-aperturas/LATINOBAROMETRO-2024/medidor_apertura_latinobarometro_2024.py"
LB = _load(REL, "ap_latinobarometro_2024_t")
S = LB.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": LB.esquema_resultados()}, out) == []
    assert out[f"{LB.P}-DICTAMEN"] in LB.G.VOCABULARIO
    assert out[f"{LB.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _frame(n=2400, seed=41):
    rng = np.random.default_rng(seed)
    d = {c: rng.integers(1, 5, n).astype(float) for c in LB.columnas_pedidas(S)}
    d["idenpa"] = np.full(n, 484.0)
    d["wt"] = rng.uniform(0.4, 2.0, n)
    d["edad"] = rng.integers(16, 90, n).astype(float)
    d["reeeduc_1"] = rng.integers(1, 8, n).astype(float)
    d["tamciud"] = rng.integers(1, 9, n).astype(float)
    d["s2"] = rng.integers(1, 6, n).astype(float)
    d["s1"] = rng.choice(list(range(1, 15)) + [96, 97], n).astype(float)
    return pd.DataFrame(d)


def _sale(frame):
    return LB.E.salida(LB.P, LB.filas(S, LB.mide_r(S, frame)))


def test_latinobarometro_con_soporte():
    out = _sale(_frame())
    _ok(out)
    assert out[f"{LB.P}-N"] > 0
    assert out[f"{LB.P}-COLA-SATISFECHO-CON-LA-VIDA-TOTAL-TODOS-R"] is not None
    assert not any("ORO-CONFIA-GOBIERNO" in k for k in out)


def test_latinobarometro_sin_soporte_y_categoria_vacia():
    f = _frame().drop(columns=["p13st_e", "p1st"])   # nombres ausentes en la ola -> NO-ESTIMABLE
    f["tamciud"] = 8.0                                # MENOS-20MIL y 20MIL-100MIL vacías
    f["p20stm"] = np.nan                              # columna presente sin respuesta válida
    out = _sale(f)
    _ok(out)
    assert out[f"{LB.P}-PISOS-CONFIA-GOBIERNO-TOTAL-TODOS-R"] is None
    assert out[f"{LB.P}-COLA-SATISFECHO-CON-LA-VIDA-TOTAL-TODOS-R"] is None
    assert out[f"{LB.P}-PISOS-APOYARIA-GOBIERNO-MILITAR-TOTAL-TODOS-R"] is None
    assert out[f"{LB.P}-PISOS-CONFIA-POLICIA-TAMLOC-MENOS-20MIL-R"] is None
    assert out[f"{LB.P}-PISOS-CONFIA-POLICIA-TAMLOC-100MIL-MAS-R"] is not None


def _zip(tmp_path, frame, esp=True, eng=True, nombre="lb.zip"):
    import pyreadstat
    z = tmp_path / nombre
    with zipfile.ZipFile(z, "w") as zz:
        for marca, poner in (("esp", esp), ("eng", eng)):
            if poner:
                p = tmp_path / f"Latinobarometro_2024_Stata_{marca}_v20250817.dta"
                pyreadstat.write_dta(frame, str(p))
                zz.write(p, p.name)
    return str(z)


def _inputs(ruta):
    d = {LB.PAY: {"ruta_absoluta": ruta}}
    d.update({k: {} for k, _r, _n in LB.CONTRATO["repo"]})
    return d


def test_latinobarometro_medir_conducto_completo(tmp_path):
    mx = _frame(1200, 42)
    otro = _frame(600, 43)
    otro["idenpa"] = 32.0
    otro["p9stgbs"] = 1.0                            # si el filtro fallara, CONFIANZA-INTERPERSONAL se movería
    datos = pd.concat([mx, otro], ignore_index=True)
    datos.columns = [c.upper() if c.startswith("p") else c for c in datos.columns]   # mayúsculas como Stata
    out = LB.medir(_inputs(_zip(tmp_path, datos)), {})
    _ok(out)
    esperado = LB.mide_r(S, mx)[("PISOS", "CONFIANZA-INTERPERSONAL", "TOTAL", "TODOS")]
    assert out[f"{LB.P}-PISOS-CONFIANZA-INTERPERSONAL-TOTAL-TODOS-R"] == pytest.approx(esperado, abs=1e-12)


def test_latinobarometro_paros_de_lectura(tmp_path):
    f = _frame(300, 44)
    with pytest.raises(LB.G.ParoDeGuardia):
        LB.medir(_inputs(_zip(tmp_path, f.drop(columns=["wt"]), nombre="a.zip")), {})
    with pytest.raises(LB.G.ParoDeGuardia):
        LB.medir(_inputs(_zip(tmp_path, f, esp=False, nombre="b.zip")), {})


def test_latinobarometro_guardia_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert LB.G.auditoria_ast(src) == []
    for mut in LB.E.MUTACIONES:
        assert LB.G.auditoria_ast(src + "\n\n" + mut), mut
