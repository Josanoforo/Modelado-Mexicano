import importlib.util
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002/medidor.py"
spec = importlib.util.spec_from_file_location("endireh_pf", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_union_y_desconocidos():
    assert module.classify(["4"] * 9) == 0
    assert module.classify(["4", "2"] + ["4"] * 7) == 1
    assert module.classify(["4", "9"] + ["4"] * 7) is None
    assert module.classify([""] * 9) is None


def test_suppression_and_determinism():
    rows = [{"vida": i % 4 == 0, "desde_octubre_2015": i % 6 == 0,
             "weight": 1.0, "stratum": str(i % 2), "psu": str(i % 10),
             "edad": "15-29", "escolaridad": "basica", "localidad": "U",
             "pareja": "A1", "entidad": "01"} for i in range(120)]
    a = module.measure_rows(rows, 100, 4)
    b = module.measure_rows(rows, 100, 4)
    assert a == b
    assert next(x for x in a if x["eje"] == "nacional" and x["ventana"] == "vida")["estado"] == "PUBLICABLE"
    assert next(x for x in a if x["eje"] == "pareja" and x["categoria"] == "A2")["estado"] == "SUPRIMIDA"


def test_dominio_incluye_upm_sin_casos():
    rows = [{"vida": int(i % 3 == 0), "weight": 1.0, "stratum": "1",
             "psu": str(i % 10), "edad": "15-29" if i % 10 < 8 else "30-44"}
            for i in range(200)]
    full = module._aggregate(rows, "vida", "edad", "15-29", 4, 200)
    only = module._aggregate([r for r in rows if r["edad"] == "15-29"],
                             "vida", "edad", "15-29", 4, 200)
    assert full["estado"] == only["estado"] == "PUBLICABLE"
    assert full["p"] == only["p"]
    assert full["replicas"] != only["replicas"]
