"""D22: salidas reales de ramas sintéticas por el conducto de sellado."""
import importlib.util
import json
from pathlib import Path
import pytest
import yaml

ROOT=Path(__file__).resolve().parents[4]
def modulo(nombre,ruta):
    s=importlib.util.spec_from_file_location(nombre,ruta)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=modulo("enif_terminales",ROOT/"tools/familias-2027/enif/lector.py")
c=modulo("corrida_terminales",ROOT/"tools/corrida0.py")
a=modulo("auditoria_terminales",ROOT/"tools/familias-2027/enif/auditoria.py")
SPEC=yaml.safe_load((ROOT/"data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0001/spec.yaml").read_text())

def filas(n=10000,cero=False):
    rows=[]
    for i in range(n):
        r=dict.fromkeys(m.COLS,"2")
        r.update(LLAVEMOD=str(i),FAC_PER="1",EST_DIS=f"{i%150:03d}",UPM_DIS=str(i%1500),EDAD_V="98")
        r["P5_6_1"]="1" if not cero and i%3==0 else "b"
        r["P5_1_1"]="1" if not cero and i%4==0 else "2"
        rows.append(r)
    return rows

@pytest.mark.parametrize("rama",["total","parcial","singleton","cero_outcomes","marginal_cero","peso_cero","sin_diseno"])
def test_salidas_reales_por_conducto(monkeypatch,rama):
    rows=filas(cero=rama=="cero_outcomes")
    if rama=="parcial": rows=rows[:100]
    if rama=="singleton":
        for r in rows:r["UPM_DIS"]=r["EST_DIS"]
    if rama=="marginal_cero":
        for r in rows:r["P5_6_1"]="b"
    if rama=="peso_cero":rows[0]["FAC_PER"]="0"
    if rama=="sin_diseno":
        for r in rows:r["EST_DIS"]=""
    monkeypatch.setattr(m,"lee_zip",lambda _:rows)
    out=m.medir({"enif_2024_enif_2024_bd_csv":{"ruta_absoluta":"sintetico"}}, {})
    assert c._valida_outputs(SPEC,out)==[]
    for key in ("REPLICAS","AUDITORIA","POTENCIA"):
        assert a.finitos(json.loads(out["RESULT-FAMILIA-ENIF-ORO-"+key]))
    assert out["RESULT-FAMILIA-ENIF-ORO-SOPORTE"] == ("SI" if rama in {"total","cero_outcomes","marginal_cero"} else "NO")

def test_denominador_total_vacio():
    rows=filas(2)
    for r in rows:r["FAC_PER"]="0"
    with pytest.raises(ValueError,match="denominador vacío"):m.estima(rows)
