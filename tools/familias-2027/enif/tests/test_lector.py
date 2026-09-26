import importlib.util
import io
import zipfile
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("lector", Path(__file__).parents[1]/"lector.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fila(i, f=False, informal=False, peso=1):
    r = dict.fromkeys(m.COLS, "2")
    r.update(LLAVEMOD=str(i), FAC_PER=str(peso), EST_DIS="001", UPM_DIS=str(i), EDAD_V="98")
    r["P5_6_1"] = "1" if f else "b"
    r["P5_1_1"] = "1" if informal else "2"
    return r


def test_conjuncion_denominador_peso_blancos():
    r = m.estima([fila(1, True, True, 3), fila(2, False, True, 1)], 20)
    assert r["p"] == [.75, 1., .75, 1.]
    assert r["n"] == 2 and r["soporte"] is False
    assert all(abs(x[3]-(x[0]+x[1]-x[2])) < 1e-12 for x in r["replicas"])


@pytest.mark.parametrize("lo,hi,estado", [(-.05,.05,"INDETERMINADO"),(.007,.013,"COMPATIBLE-CON-TOLERANCIA"),(.021,.03,"DESVÍO-MATERIAL"),(-.02,.02,"COMPATIBLE-CON-TOLERANCIA"),(.02,.025,"INDETERMINADO"),(-.025,-.02,"INDETERMINADO"),(.0201,.025,"DESVÍO-MATERIAL")])
def test_fronteras(lo,hi,estado):
    assert m.clasifica(lo,hi) == estado


def test_guardias_mutacion():
    with pytest.raises(PermissionError):
        m.guardia({}, True, False)
    with pytest.raises(ValueError):
        m.guardia({}, agrupacion="sexo")
    with pytest.raises(PermissionError):
        m.medir({"otro_archivo": {}}, {})
    with pytest.raises(ValueError):
        m.estima([fila(1), fila(1)], 20)
    r = fila(1); r["EDAD_V"] = "17"
    with pytest.raises(ValueError):
        m.estima([r], 20)
    with pytest.raises(ValueError):
        m.guardia({"peso": "FAC_HOG"})


def test_lector_proyeccion_sintetica():
    r = fila(1)
    blob = io.BytesIO()
    with zipfile.ZipFile(blob, "w") as z:
        z.writestr("TMODULO.csv", ",".join(m.COLS)+",SECRETO\n"+",".join(r[c] for c in m.COLS)+",no-leer\n")
    blob.seek(0)
    assert m.lee_zip(blob) == [r]


def test_codigo_fuera_descriptor_masa():
    r = fila(1, peso=3); r["P5_6_1"] = "9"
    out = m.estima([r], 20)
    assert out["codigos"] == {"P5_6_1:9": 1}
    assert out["masa_codigos"] == {"P5_6_1:9": 3}


def test_mutacion_codigo_columna_ajena():
    spec = importlib.util.spec_from_file_location("audita", Path(__file__).parents[1]/"auditoria.py")
    a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
    code = (Path(__file__).parents[1]/"lector.py").read_text()
    assert a.audita(code) == []
    assert a.audita(code.replace('r["FAC_PER"]', 'r["SEXO"]'))
    assert not a.finitos({"anidado": [float("nan")]})


def test_d22_terminales_conducto_real():
    root = Path(__file__).resolve().parents[4]
    spec = importlib.util.spec_from_file_location("corrida", root/"tools/corrida0.py")
    c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    declarado = {"resultados": [{"id":"RESULT-ENIF-FUTURO-LO","tipo":"flotante","unidad":"proporción","permite_no_estimable":True}]}
    assert c._valida_outputs(declarado, {"RESULT-ENIF-FUTURO-LO": None}) == []
    assert c._valida_outputs(declarado, {"RESULT-ENIF-FUTURO-LO": float("nan")})
    declarado["resultados"][0]["permite_no_estimable"] = False
    assert c._valida_outputs(declarado, {"RESULT-ENIF-FUTURO-LO": None})
