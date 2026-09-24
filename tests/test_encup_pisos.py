"""Protege códigos ordinales y supresión de ENCUP."""
import importlib.util
from pathlib import Path
import pandas as pd


MODULE = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-ENCUP-PISOS-2012-0001/medidor.py"
spec = importlib.util.spec_from_file_location("encup_pisos", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_no_respuesta_fuera_del_denominador_y_n_minimo():
    data = pd.Series([1] * 20 + [2] * 10 + [98] * 5 + [99] * 5)
    result = mod.summarize(data, (1, 2, 3), (1,))
    assert result["n_validos"] == 30
    assert result["n_sin_respuesta_sustantiva"] == 10
    assert result["proporcion"] == 2 / 3
    assert mod.summarize(data[:29], (1, 2, 3), (1,))["estado"] == "NO-ESTIMABLE"
