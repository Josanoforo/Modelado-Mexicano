import importlib.util
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0002/medidor.py"
spec = importlib.util.spec_from_file_location("endireh_pf", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_union_y_desconocidos():
    assert module.classify(["4"] * 9) == 0
    assert module.classify(["4", "2"] + ["4"] * 7) == 1
    assert module.classify(["4", "9"] + ["4"] * 7) is None
    assert module.classify([""] * 9) is None


def test_suppression_and_determinism():
    rows = [{"vida": i % 4 == 0, "desde_octubre_2020": i % 6 == 0,
             "weight": 1.0, "stratum": str(i % 2), "psu": str(i % 10),
             "edad": "15-29", "escolaridad": "basica", "localidad": "U",
             "pareja": "A1", "entidad": "01"} for i in range(120)]
    a = module.measure_rows(rows, 100, 4)
    b = module.measure_rows(rows, 100, 4)
    assert a == b
    assert next(x for x in a if x["eje"] == "nacional" and x["ventana"] == "vida")["estado"] == "PUBLICABLE"
    assert next(x for x in a if x["eje"] == "pareja" and x["categoria"] == "A2")["estado"] == "SUPRIMIDA"
