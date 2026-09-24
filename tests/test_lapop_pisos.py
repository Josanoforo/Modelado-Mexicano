"""Verifica universo, ponderación y réplicas estratificadas del piso LAPOP."""
import importlib.util
from pathlib import Path
import pandas as pd


MODULE = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-LAPOP-PISOS-2019-0001/medidor.py"
spec = importlib.util.spec_from_file_location("lapop_pisos", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_tasa_ponderada_y_faltantes():
    df = pd.DataFrame({
        "clien1na": [1] * 16 + [2] * 16 + [float("nan")],
        "wt": [2] * 16 + [1] * 16 + [1],
        "estratopri": [1] * 16 + [2] * 17,
        "upm": [1] * 8 + [2] * 8 + [3] * 8 + [4] * 9,
    })
    got = mod.estimate(df, "clien1na", (1, 2), (1,), 42, 100)
    assert got["n"] == 32
    assert got["n_si"] == 16
    assert got["p"] == 2 / 3
    assert got["n_estratos"] == 2
    assert got["replicas_validas"] == 100
