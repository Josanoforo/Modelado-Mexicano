"""Las etiquetas del XLSX y los códigos del cuestionario conservan dirección."""
import importlib.util
from pathlib import Path
import pandas as pd


MODULE = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-ENCUP-PISOS-2012-0003/medidor.py"
spec = importlib.util.spec_from_file_location("encup_pisos_v12", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_mucho_poco_nada_y_no_respuesta():
    values = pd.Series(["Mucho"] * 12 + ["Poco"] * 10 + ["Nada"] * 8 + ["No sé", "No contesta"])
    got = mod.summarize(values, (1, 2, 3), (1,))
    assert got["n_validos"] == 30
    assert got["n_seleccionados"] == 12
    assert got["proporcion"] == 0.4
    assert got["n_sin_respuesta_sustantiva"] == 2
