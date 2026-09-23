import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001/medidor.py'
spec = importlib.util.spec_from_file_location('endireh_com', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_union_vida_y_salto():
    assert module.classify_binary_union(['2'] * 16) == 0
    assert module.classify_binary_union(['2'] * 15 + ['1']) == 1
    assert module.classify_binary_union(['2'] * 15 + ['']) is None
    assert module.classify(['4'] * 16) == 0
    assert module.classify(['4'] * 15 + ['3']) == 1
