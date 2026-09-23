import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENDIREH-PISOS-2021-AYUDA-0001/medidor.py'
spec = importlib.util.spec_from_file_location('endireh_ayu', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_actos_y_codigos_condicionales():
    assert len(module.ACTS) == len(set(module.ACTS)) == 38
    assert module.classify(['4'] * 37 + ['1']) == 1
    assert module.classify(['4'] * 37 + ['9']) is None
    assert module._yesno('2') == 0
    assert module._yesno('9') is None
    assert module._reason('0') == 0
    assert module._reason('') is None
