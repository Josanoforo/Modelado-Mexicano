"""ENDIREH 2006 usa códigos y módulos conyugales propios."""
import importlib.util
from pathlib import Path


PATH = (Path(__file__).resolve().parents[1] / "data/corrida0" /
        "CALC-ENDIREH-PISOS-2006-MODULOS-0002/medidor.py")
spec = importlib.util.spec_from_file_location("endireh_2006_modulos", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_pareja_unida_2006_dos_es_violencia_tres_no():
    assert module._classify(["2", "3"], {"1", "2"}, {"3"}) == 1
    assert module._classify(["3", "3"], {"1", "2"}, {"3"}) == 0
    assert module._classify(["3", ""], {"1", "2"}, {"3"}) is None


def test_soltera_sin_pareja_no_entra_en_bloque_28():
    row = {"P23": "3", "P28_1_1": ""}
    out = {}
    module._partner_c(row, out)
    assert out == {}


def test_flags_ayuda_no_imputan_blanco_como_no():
    assert module._help_flags({"P7_7_1": "1"}, "P7_7_", 4) == 1
    assert module._help_flags({"P7_7_4": "4"}, "P7_7_", 4) == 0
    assert module._help_flags({}, "P7_7_", 4) is None
