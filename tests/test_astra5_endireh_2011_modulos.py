"""ENDIREH 2011 separa cuestionarios A/B/C y códigos de actor/lugar."""
import importlib.util
from pathlib import Path


PATH = (Path(__file__).resolve().parents[1] / "data/corrida0" /
        "CALC-ENDIREH-PISOS-2011-MODULOS-0001/medidor.py")
spec = importlib.util.spec_from_file_location("endireh_2011_modulos", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_actos_por_situacion_conyugal():
    assert len(module._partner_groups("A")["fisica"]) == 8
    assert len(module._partner_groups("C")["fisica"]) == 7
    assert module._freq(["4", "4"]) == 0
    assert module._freq(["4", "8"]) is None


def test_ambito_externo_depende_de_actor_y_lugar():
    row = {"AP2_6_1": "1", "AP2_7_1_1": "09", "AP2_8_1_1": "02",
           "AP2_9_1_1": "1"}
    assert module._domain_act(row, "AP", 1, {"09", "10", "11"}, "2_7") == (1, 1)
    assert module._domain_act(row, "AP", 1, {"07", "08"}, "2_7") == (0, 0)
    assert module._domain_act(row, "AP", 1, {"02"}, "2_8") == (1, 1)


def test_sin_pareja_no_imputa_ausencia_de_violencia():
    base = {}
    module._partner({"CP4_1": "3"}, {}, {}, "C", base)
    assert base == {}
