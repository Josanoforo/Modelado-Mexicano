"""Propuesta futura v2: conducto real con R sintética y tabla temporal."""
import ast
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
CID = "CALC-FAMILIA-2027-ENIF-EVALUACION-0001"


def carga(nombre, ruta):
    s=importlib.util.spec_from_file_location(nombre,ruta)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def test_futuro_v2_conducto_ref(tmp_path, monkeypatch):
    m=carga("futuro_ref", ROOT/"tools/familias-2027/enif/lector-futuro-serializacion-v2.py")
    c=carga("corrida_futuro_ref",ROOT/"tools/corrida0.py")
    d=tmp_path/"data/corrida0"/CID;d.mkdir(parents=True)
    monkeypatch.setattr(m,"__file__",str(d/"medidor.py"));monkeypatch.setattr(c,"RAIZ",tmp_path)
    rows=[]
    for j in range(10080):
        r=dict.fromkeys(m.COLS,"2")
        r.update(LLAVEMOD=str(j),FAC_PER="1",EDAD_V="98",EST_DIS=str(j%180),UPM_DIS=str((j//180)%6))
        r["P5_6_1"]="1" if j%2 else "b";r["P5_1_1"]="1" if j%3 else "2";rows.append(r)
    monkeypatch.setattr(m,"lee_zip",lambda _:rows)
    ins={k:{"bytes":(ROOT/"data/corrida0"/k/"resultados.json").read_bytes()} for k in m.PISOS_HASH}
    ins["enif_2027"]={"ruta_absoluta":"SINTETICO"}
    contrato={"estado":"RESERVADA","autoridad_ola":"AUTORIZACION-SINTETICA","comparabilidad_cotejada":True,
              "metadatos":{"unidad":"persona18+","peso":"FAC_PER","formal":list(m.FORMAL),"informal":list(m.INFORMAL),"periodo":"ultimos12meses"}}
    out=m.medir_futuro(ins,contrato)
    schema=yaml.safe_load((ROOT/"tools/familias-2027/enif/contrato-futuro-serializacion-v2.yaml").read_text())
    assert c._fallas_run(schema,out,0,"",d) == []
    assert all(out["RESULT-FAMILIA-ENIF-FUTURO-"+fam+"-D-K"].startswith("REF:") for fam in ("AHORRO-FORMAL","HORIZONTE-AHORRO"))


def test_algoritmo_guardias_futuro_intactos():
    base=ROOT/"tools/familias-2027/enif"
    funcs=lambda p:{n.name:ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
    old,new=funcs(base/"lector.py"),funcs(base/"lector-futuro-serializacion-v2.py")
    for nombre in old:
        if nombre != "medir_futuro":assert old[nombre]==new[nombre]
