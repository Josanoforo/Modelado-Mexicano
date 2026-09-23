import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENDIREH-PISOS-2021-DECISIONES-0001/medidor.py'
spec = importlib.util.spec_from_file_location('endireh_dec', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_codes_and_missing():
    assert module._binary('1', {'1', '4', '5'}, {'2', '3'}) == 1
    assert module._binary('3', {'1', '4', '5'}, {'2', '3'}) == 0
    assert module._binary('6', {'1', '4', '5'}, {'2', '3'}) is None
    assert module._binary('7', {'1', '4', '5'}, {'2', '3'}) is None
    assert module._binary('', {'1', '4', '5'}, {'2', '3'}) is None
