"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de Pew GAS Spring 2025 (expediente PEW-2025).

Defecto real que atrapa: los actos perdidos del piloto 3 (D-22: un conducto que no acepta una rama terminal) y
NC-0328 (reserva quemada por un cruce). El esquema es el de los tres medidores sellados (sus columnas, en
minúsculas, las que `columnas_pedidas` deriva de sus tablas). Ramas: con soporte; conducta sin soporte (R None);
categoría vacía; y el conducto completo `medir()` sobre un .sav sintético en zip con filas de otro país, más los
PARO de lectura (sin peso, sin etiqueta «Mexico»). Toda salida pasa `corrida0._valida_outputs`.
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


REL = "forense/prereg-aperturas/PEW-2025/medidor_apertura_pew_2025.py"
PEW = _load(REL, "ap_pew_2025_t")
S = PEW.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": PEW.esquema_resultados()}, out) == []
    assert out[f"{PEW.P}-DICTAMEN"] in PEW.G.VOCABULARIO
    assert out[f"{PEW.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _frame(n=2400, seed=31):
    rng = np.random.default_rng(seed)
    d = {c: rng.integers(1, 5, n).astype(float) for c in PEW.columnas_pedidas(S)}
    d["country"] = np.full(n, 7.0)
    d["weight"] = rng.uniform(0.3, 2.5, n)
    d["age"] = rng.integers(18, 100, n).astype(float)          # 98/99 = no sabe/no responde
    d["gender"] = rng.integers(1, 3, n).astype(float)
    d["d_educ_mexico"] = rng.integers(1, 13, n).astype(float)
    d["religion_combined"] = rng.choice([1, 2, 3, 4, 5, 6, 7, 99], n).astype(float)
    d["religion_christian"] = rng.choice([0, 1, 2], n).astype(float)
    d.pop("sex")
    d.pop("d_educ_mexico_2017")
    return pd.DataFrame(d)


def _sale(frame):
    return PEW.E.salida(PEW.P, PEW.filas(S, PEW.mide_r(S, frame)))


def test_pew_con_soporte():
    out = _sale(_frame())
    _ok(out)
    assert out[f"{PEW.P}-N"] > 0
    assert out[f"{PEW.P}-RELIGION2024-CATOLICO-TOTAL-TODOS-R"] is not None
    # CONFIANZA-INTERPERSONAL no tiene piso con soporte en el contendiente: R existe, la celda no se puntúa
    assert out[f"{PEW.P}-PISOS-CONFIANZA-INTERPERSONAL-TOTAL-TODOS-R"] is not None


def test_pew_sin_soporte_y_categoria_vacia():
    f = _frame()
    f = f.drop(columns=["god", "mex_live_us"])      # conductas sin columna en la ola -> NO-ESTIMABLE
    f["gender"] = 2.0                               # HOMBRE vacío
    f["religion_import"] = np.nan                  # conducta con columna pero sin respuesta válida
    out = _sale(f)
    _ok(out)
    assert out[f"{PEW.P}-RELIGION2024-CREE-EN-DIOS-TOTAL-TODOS-R"] is None
    assert out[f"{PEW.P}-MIGRACION-IRIA-A-VIVIR-A-EEUU-TOTAL-TODOS-R"] is None
    assert out[f"{PEW.P}-MIGRACION-IRIA-SIN-AUTORIZACION-ENTRE-QUIENES-IRIAN-TOTAL-TODOS-R"] is None
    assert out[f"{PEW.P}-PISOS-RELIGION-MUY-IMPORTANTE-TOTAL-TODOS-R"] is None
    assert out[f"{PEW.P}-RELIGION2024-CATOLICO-SEXO-HOMBRE-R"] is None
    assert out[f"{PEW.P}-RELIGION2024-CATOLICO-SEXO-MUJER-R"] is not None


def test_pew_alias_de_sexo_y_escolaridad():
    f = _frame().rename(columns={"gender": "sex", "d_educ_mexico": "d_educ_mexico_2017"})
    out = _sale(f)
    _ok(out)
    assert out[f"{PEW.P}-PISOS-LIDER-FUERTE-BUENO-SEXO-MUJER-R"] is not None
    assert out[f"{PEW.P}-PISOS-LIDER-FUERTE-BUENO-ESCOLARIDAD-SUPERIOR-R"] is not None


def _zip_sav(tmp_path, frame, etiquetas):
    import pyreadstat
    sav = tmp_path / "Pew Research Center Global Attitudes Spring 2025 Dataset.sav"
    pyreadstat.write_sav(frame, str(sav), variable_value_labels={"country": etiquetas})
    z = tmp_path / "pew_gas_spring2025.zip"
    with zipfile.ZipFile(z, "w") as zz:
        zz.write(sav, sav.name)
    return str(z)


def _inputs(ruta):
    d = {PEW.PAY: {"ruta_absoluta": ruta}}
    d.update({k: {} for k, _r, _n in PEW.CONTRATO["repo"]})
    return d


def test_pew_medir_conducto_completo(tmp_path):
    mx = _frame(1500, 32)
    otro = _frame(700, 33)
    otro["country"] = 3.0
    otro["religion_christian"] = 1.0                 # si el filtro fallara, CATOLICO se movería
    ruta = _zip_sav(tmp_path, pd.concat([mx, otro], ignore_index=True), {7.0: "Mexico", 3.0: "Brazil"})
    out = PEW.medir(_inputs(ruta), {})
    _ok(out)
    esperado = PEW.mide_r(S, mx)[("RELIGION2024", "CATOLICO", "TOTAL", "TODOS")]
    assert out[f"{PEW.P}-RELIGION2024-CATOLICO-TOTAL-TODOS-R"] == pytest.approx(esperado, abs=1e-12)


def test_pew_paro_sin_peso_o_sin_mexico(tmp_path):
    f = _frame(300, 34)
    with pytest.raises(PEW.G.ParoDeGuardia):
        PEW.medir(_inputs(_zip_sav(tmp_path, f.drop(columns=["weight"]), {7.0: "Mexico"})), {})
    with pytest.raises(PEW.G.ParoDeGuardia):
        PEW.medir(_inputs(_zip_sav(tmp_path, f, {7.0: "Brazil"})), {})


def test_pew_guardia_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert PEW.G.auditoria_ast(src) == []
    for mut in PEW.E.MUTACIONES:
        assert PEW.G.auditoria_ast(src + "\n\n" + mut), mut
