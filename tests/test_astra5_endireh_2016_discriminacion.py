"""Protege la elegibilidad específica del embarazo en ENDIREH 2016 7.3."""
import importlib.util
from pathlib import Path


PATH = (Path(__file__).resolve().parents[1] / "data/corrida0" /
        "CALC-ENDIREH-PISOS-2016-DISCRIMINACION-0001/medidor.py")
spec = importlib.util.spec_from_file_location("endireh_discriminacion", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_no_estuvo_embarazada_no_es_negativo():
    assert module.classify_pregnancy(["3", "3", "3"]) is None
    assert module.classify_pregnancy(["2", "3", "2"]) is None
    assert module.classify_pregnancy(["2", "2", "2"]) == 0
    assert module.classify_pregnancy(["3", "1", "2"]) == 1


def test_prueba_de_embarazo_tiene_universo_laboral_distinto():
    assert module.classify_binary(["2", "2"]) == 0
    assert module.classify_binary(["1", "2"]) == 1
    assert module.classify_binary(["2", "9"]) is None
