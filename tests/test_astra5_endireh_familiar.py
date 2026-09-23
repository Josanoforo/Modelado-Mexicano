import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENDIREH-PISOS-2021-FAMILIAR-0001/medidor.py'
spec = importlib.util.spec_from_file_location('endireh_fam', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_union_reciente():
    assert len(module.ACTS) == 20
    assert module.classify(['4'] * 20) == 0
    assert module.classify(['4'] * 19 + ['2']) == 1
    assert module.classify(['4'] * 19 + ['']) is None
