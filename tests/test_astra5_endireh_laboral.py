import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENDIREH-PISOS-2021-LABORAL-0001/medidor.py'
spec = importlib.util.spec_from_file_location('endireh_esc', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_union_y_salto_escolar():
    assert len(module.ACTS) == 19
    assert module.classify_binary_union(['2'] * 19) == 0
    assert module.classify_binary_union(['2'] * 18 + ['1']) == 1
    assert module.classify_binary_union(['2'] * 18 + ['']) is None
    assert module.classify(['4'] * 18 + ['3']) == 1
