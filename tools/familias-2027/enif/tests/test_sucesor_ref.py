"""Sucesor propuesto: sintéticos y tablas temporales, sin microdatos."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[4]
CID = "CALC-FAMILIA-2027-ENIF-ORO-0002"


def carga(nombre, ruta):
    s = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def entorno(tmp_path, monkeypatch):
    d = tmp_path/"data/corrida0"/CID; d.mkdir(parents=True)
    m = carga("sucesor_ref", ROOT/"data/corrida0"/CID/"medidor.py")
    c = carga("corrida_ref", ROOT/"tools/corrida0.py")
    monkeypatch.setattr(m, "__file__", str(d/"medidor.py"))
    monkeypatch.setattr(c, "RAIZ", tmp_path)
    return d, m, c


def test_algoritmo_congelado_identico():
    viejo = ROOT/"data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0001/medidor.py"
    nuevo = ROOT/"data/corrida0"/CID/"medidor.py"
    def funcs(p):
        return {n.name: ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n, ast.FunctionDef)}
    old, new = funcs(viejo), funcs(nuevo)
    for nombre in old:
        if nombre != "medir":
            assert old[nombre] == new[nombre]
    a = ast.parse(viejo.read_text()); b = ast.parse(nuevo.read_text())
    constantes = lambda arbol: [ast.dump(n) for n in arbol.body if isinstance(n, ast.Assign)]
    assert constantes(a) == constantes(b)


def test_ref_nativa_hash_y_replay_sin_reescribir(tmp_path, monkeypatch):
    d, m, c = entorno(tmp_path, monkeypatch)
    obj = [[0.1, 0.2, 0.01, 0.29]]*2000
    ref = m._tabla("replicas.json", obj)
    assert c._problemas_valor_largo({"RESULT-X":ref},d) == []
    ruta = d/"tablas/replicas.json"
    antes = ruta.stat().st_mtime_ns
    assert m._tabla("replicas.json", obj) == ref
    assert ruta.stat().st_mtime_ns == antes
    assert json.loads(ruta.read_bytes()) == obj
    assert ref.endswith(hashlib.sha256(ruta.read_bytes()).hexdigest())
    with pytest.raises(PermissionError):m._tabla("replicas.json", [[0]])
    assert c._problemas_valor_largo({"RESULT-X":ref.replace(CID,"OTRO")},d)
    assert c._problemas_valor_largo({"RESULT-X":ref[:-1]+"0"},d)
    with pytest.raises(PermissionError):m._tabla("../escape.json",obj)


def test_ref_rechaza_enlaces_no_finitos(tmp_path, monkeypatch):
    d, m, c = entorno(tmp_path, monkeypatch)
    with pytest.raises(ValueError):m._tabla("potencia.json",{"x":float("nan")})
    afuera = tmp_path/"afuera"; afuera.mkdir()
    (d/"tablas/potencia.json").symlink_to(afuera/"x")
    with pytest.raises(PermissionError):m._tabla("potencia.json",{})


def test_medidor_sintetico_conducto_completo(tmp_path, monkeypatch):
    d, m, c = entorno(tmp_path, monkeypatch)
    rows=[]
    for j in range(12):
        r=dict.fromkeys(m.COLS,"2")
        r.update(LLAVEMOD=str(j),FAC_PER="1",EDAD_V="98",EST_DIS="001",UPM_DIS=str(j%3))
        r["P5_6_1"]="1" if j%2 else "b";r["P5_1_1"]="1" if j%3 else "2";rows.append(r)
    monkeypatch.setattr(m,"lee_zip",lambda _:rows)
    ins={"enif_2024_enif_2024_bd_csv":{"ruta_absoluta":"SINTETICO"}}
    out=m.medir(ins,{})
    spec=yaml.safe_load((ROOT/"data/corrida0"/CID/"spec.yaml").read_text())
    assert c._valida_outputs(spec,out) == []
    assert c._problemas_valor_largo(out,d) == []
    assert c._fallas_run(spec,out,0,"",d) == []
    old=carga("oro_anterior_ref",ROOT/"data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0001/medidor.py")
    monkeypatch.setattr(old,"lee_zip",lambda _:rows)
    previo=old.medir(ins,{})
    for rid,v in out.items():
        if isinstance(v,str) and v.startswith("REF:"):
            ruta=v[4:].split("#sha256:")[0]
            assert json.loads((tmp_path/ruta).read_bytes()) == json.loads(previo[rid])
        else:assert v == previo[rid]
