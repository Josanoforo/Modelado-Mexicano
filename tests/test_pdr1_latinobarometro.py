"""Prueba sintética de CALC-PDR1-LATINOBAROMETRO-0001 (acto GEN2-PISOS-DOMINIOS-Y-REGLAS-1).

Fabrica un ZIP falso con la misma forma que `latinobarometro2024_bd_stata` (miembro
`Latinobarometro_2024_Stata_esp_v20250817.dta`, columnas con punto como en el real: los nombres
se escriben con `_` y se parchean a `.` en bytes, porque el escritor de Stata no admite `.`), corre
`medir()` completo y exige `corrida0._valida_outputs(spec, out) == []` y que `resultados:` del
spec.yaml sea exactamente el esquema que deriva el medidor. No abre el microdato real.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
import corrida0  # noqa: E402

CALC = RAIZ / "data/corrida0/CALC-PDR1-LATINOBAROMETRO-0001"
MIEMBRO = "Latinobarometro_2024_Stata_esp_v20250817.dta"
RENOMBRE = {"P12STGBS_A": "P12STGBS.A", "REEDUC_1": "REEDUC.1"}


def _load():
    spec = importlib.util.spec_from_file_location("medidor_pdr1_lb", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _zip_sintetico(tmp: Path, n=900, seed=7) -> Path:
    import pyreadstat

    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "IDENPA": rng.choice([484, 32, 76], n).astype(float),
        "SEXO": rng.choice([1, 2], n).astype(float),
        "EDAD": rng.integers(16, 90, n).astype(float),
        "TAMCIUD": rng.integers(1, 9, n).astype(float),
        "REEDUC_1": rng.integers(1, 8, n).astype(float),
        "S2": rng.choice([1, 2, 3, 4, 5, np.nan], n).astype(float),
        "P12STGBS_A": rng.choice([1, 2, 3, 4, np.nan], n).astype(float),
        "WT": rng.uniform(0.3, 2.5, n),
    })
    dta = tmp / "s.dta"
    pyreadstat.write_dta(df, str(dta), version=14)
    b = dta.read_bytes()
    for a, c in RENOMBRE.items():
        assert len(a) == len(c) and a.encode() in b
        b = b.replace(a.encode(), c.encode())
    z = tmp / "latinobarometro2024_bd_stata.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(MIEMBRO, b)
        zf.writestr("Latinobarometro_2024_Cuestionario_esp.pdf", b"%PDF-1.4 sintetico")
    return z


def _inputs(zpath: Path):
    out = {"latinobarometro2024_bd_stata": {"ruta_absoluta": str(zpath)}}
    for k, r in (("receta_pisos_salud", "tools/dominios/salud/pisos_diseno.py"),
                 ("motor_pisos_confianza", "tools/dominios/confianza/motor_pisos.py")):
        by = (RAIZ / r).read_bytes()
        out[k] = {"bytes": by, "sha256": hashlib.sha256(by).hexdigest()}
    return out


def test_medir_sintetico_valida():
    mod = _load()
    _, spec = corrida0._carga_spec("CALC-PDR1-LATINOBAROMETRO-0001")
    contrato = dict(spec)
    contrato["parametros"] = dict(spec["parametros"], bootstrap_replicas=50)
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as t:
        out = mod.medir(_inputs(_zip_sintetico(Path(t))), contrato)
    assert corrida0._valida_outputs(spec, out) == []
    p = out["RESULT-PDR1-LATINOBAROMETRO-SATISFECHO-CON-LA-DEMOCRACIA-2024-TOTAL-TODOS-P"]
    assert 0.0 < p < 1.0


def test_spec_yaml_resultados_es_el_esquema():
    mod = _load()
    _, spec = corrida0._carga_spec("CALC-PDR1-LATINOBAROMETRO-0001")
    assert [r["id"] for r in spec["resultados"]] == [r["id"] for r in mod.esquema_resultados()]


def test_guardia_inputs_para():
    mod = _load()
    with pytest.raises(mod.ParoDeGuardia):
        mod._guardia_inputs({"latinobarometro2023_bd_stata_zip": {"ruta_absoluta": "x"}})
