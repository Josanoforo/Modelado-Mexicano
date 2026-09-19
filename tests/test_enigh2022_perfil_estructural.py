#!/usr/bin/env python3
"""Pruebas sintéticas de riesgos materiales del perfil ENIGH 2022."""
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "data/corrida0/CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003/medidor.py"
spec = importlib.util.spec_from_file_location("perfil", MOD)
perfil = importlib.util.module_from_spec(spec)
spec.loader.exec_module(perfil)


def persona(viv, ren, edad, seg="1", factor="10", par="101", est="001", upm="0000001"):
    return {"folioviv": viv, "foliohog": "1", "numren": ren, "parentesco": par,
            "edad": str(edad), "segsoc": seg, "factor": factor, "est_dis": est, "upm": upm}


def conc(viv, tam="1", est="1"):
    return {"folioviv": viv, "foliohog": "1", "tam_loc": tam, "est_socio": est}


def hogar(viv, cel="1", inte="2"):
    return {"folioviv": viv, "foliohog": "1", "celular": cel, "conex_inte": inte}


def assert_raises(f, texto):
    try:
        f()
    except ValueError as e:
        assert texto in str(e)
    else:
        raise AssertionError("se esperaba ValueError")


def test_join_persona_y_malla():
    pob = [persona("1", "01", 25, factor="10"), persona("1", "02", 40, seg="2", factor="20")]
    r = perfil.calcular(pob, [conc("1")], [hogar("1")], replicas=20, seed=7)
    assert r["universo_n"] == 2
    # El atributo hogar se hereda a dos personas, pero cada una conserva peso persona.
    cel = next(x for x in r["marginales"] if x["variable"] == "celular" and x["codigo"] == "1")
    assert cel["n"] == 2 and cel["numerador_ponderado"] == 30.0
    assert len(r["conjunta"]) == 128
    assert any(x["estado"] == "CERO-MUESTRAL" and x["ee"] is None for x in r["conjunta"])


def test_faltante_no_imputado_y_pertenencia():
    pob = [persona("1", "01", 25, seg=""), persona("1", "02", 30, par="401"), persona("1", "03", 30, par="701")]
    r = perfil.calcular(pob, [conc("1")], [hogar("1")], replicas=20, seed=7)
    assert r["universo_n"] == 1
    assert r["embudo"]["excl_domesticos"]["n"] == 1
    assert r["embudo"]["excl_huespedes"]["n"] == 1
    filas = [x for x in r["marginales"] if x["variable"] == "segsoc"]
    assert all(x["valid_n"] == 0 and x["missing_n"] == 1 for x in filas)
    assert r["completo_n"] == 0


def test_duplicados_detienen():
    p = persona("1", "01", 25)
    assert_raises(lambda: perfil.calcular([p, dict(p)], [conc("1")], [hogar("1")], 5, 1), "llave persona duplicada")
    assert_raises(lambda: perfil.calcular([p], [conc("1"), conc("1")], [hogar("1")], 5, 1), "llave hogar duplicada")


def test_edad_fuera_es_exclusion_no_faltante():
    pob = [persona("1", "01", 17), persona("1", "02", 97), persona("1", "03", 50)]
    r = perfil.calcular(pob, [conc("1")], [hogar("1")], replicas=10, seed=1)
    assert r["universo_n"] == 1
    assert r["embudo"]["excl_menor_18"]["n"] == 1
    assert r["embudo"]["excl_mayor_96"]["n"] == 1
    assert r["embudo"]["excl_edad_invalida"]["n"] == 0


def test_bom_unicode_y_mojibake():
    assert perfil._texto("\ufefffolioviv") == "folioviv"
    assert perfil._texto("ï»¿folioviv") == "folioviv"


if __name__ == "__main__":
    for f in (test_join_persona_y_malla, test_faltante_no_imputado_y_pertenencia,
              test_duplicados_detienen, test_edad_fuera_es_exclusion_no_faltante,
              test_bom_unicode_y_mojibake):
        f()
    print("OK: 5 pruebas sintéticas")
