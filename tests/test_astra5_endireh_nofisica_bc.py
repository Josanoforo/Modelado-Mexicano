"""Cuestionario C omite seis reactivos conyugales del bloque 14.1."""
import importlib.util
from pathlib import Path


PATH = (Path(__file__).resolve().parents[1] / "data/corrida0" /
        "CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001/medidor.py")
spec = importlib.util.spec_from_file_location("endireh_nofisica_bc", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_c_no_incluye_reactivos_ausentes():
    assert "P14_1_23AB" in module.acts_for("emocional_control", "B1")
    assert "P14_1_23AB" not in module.acts_for("emocional_control", "C1")
    assert "P14_1_38AB" in module.acts_for("economica_patrimonial", "A1")
    assert "P14_1_38AB" not in module.acts_for("economica_patrimonial", "C1")
    assert len(module.acts_for("no_fisica_alguna", "C1")) == 23


def test_union_no_suma_ni_imputa_silencio():
    assert module.classify(["1", "4"]) == 1
    assert module.classify(["4", "4"]) == 0
    assert module.classify(["4", ""]) is None
