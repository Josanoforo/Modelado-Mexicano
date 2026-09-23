"""Frozen C-ASTRA CALC adapter."""
import hashlib
import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "tools/astra/envipe/model.py"
MODEL_SHA = "47ded83d3e8a9283a2972289240d8fa6b90c440cefb238bca04255e044a11212"
PAIR = "ESCOLARIDADPROXYXSEXO"
def medir(inputs, contrato):
    if hashlib.sha256(MODEL.read_bytes()).hexdigest() != MODEL_SHA:
        raise ValueError("C-ASTRA code changed since freeze")
    spec = importlib.util.spec_from_file_location("astra_envipe_model", MODEL)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    history = [inputs[f"envipe{y}_csv"]["ruta_absoluta"] for y in (2023, 2024)]
    public = inputs["MARGINALES-PUBLICOS"]["bytes"]
    (pred, hyper), meta = model.run(PAIR, history, public)
    result = {}
    a, b = model.PAIRS[PAIR]
    for i, cell in enumerate((x, y) for x in model.ORDER[a] for y in model.ORDER[b]):
        key = f"RESULT-ASTRA-{PAIR}-{i+1:02d}"
        value = pred[cell]
        result[key+"-P"] = None if value is None else value[0]
        result[key+"-LO"] = None if value is None else value[1]
        result[key+"-HI"] = None if value is None else value[2]
        result[key+"-ESTADO"] = "NO-ESTIMABLE: denominador histórico o réplica vacía" if value is None else "ESTIMABLE: INTERVALO-PREDICTIVO-95"
    result[f"RESULT-ASTRA-{PAIR}-TAU2"] = hyper["tau2"]
    result[f"RESULT-ASTRA-{PAIR}-Q"] = hyper["q"]
    return result
