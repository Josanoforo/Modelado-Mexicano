"""Protege saltos y diferencias del instrumento ENDIREH 2016."""
import importlib.util
from pathlib import Path


PATH = (Path(__file__).resolve().parents[1] / "data/corrida0" /
        "CALC-ENDIREH-PISOS-2016-RESTANTES-0001/medidor.py")
spec = importlib.util.spec_from_file_location("endireh_2016_restantes", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_c1_omite_actos_conyugales():
    assert "P13_1_23AB" in module._partner_act("emocional_control", "B1")
    assert "P13_1_23AB" not in module._partner_act("emocional_control", "C1")
    assert "P13_1_36AB" not in module._partner_act("economica_patrimonial", "C1")


def test_codigos_2016_por_tipo_de_pregunta():
    assert module.classify_yesno(["2", "2"]) == 0
    assert module.classify_yesno(["2", ""]) is None
    assert module.classify_freq(["4", "4"]) == 0
    assert module.classify_freq(["1", "4"]) == 1


def test_razones_solo_entre_sin_ayuda_ni_denuncia():
    base = {}
    main = {"P13_7_1": "2", "P13_7_2": "2"}
    extra = {"P13_21_1": "1", "P13_21_2": "0"}
    module._service_fields(base, main, extra, "pareja", 1)
    assert base["pareja_razon_01"] == 1
    assert base["pareja_razon_02"] == 0
    main["P13_7_1"] = "1"
    module._service_fields(base, main, extra, "pareja", 1)
    assert base["pareja_razon_01"] is None
