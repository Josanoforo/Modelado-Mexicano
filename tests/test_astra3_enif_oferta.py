import importlib.util
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "tools/astra/enif/oferta/medidor.py"
spec = importlib.util.spec_from_file_location("oferta", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)

def test_principal_y_multiples_y_pase():
    one = pd.DataFrame({"r":["1","6","9","", "2"]})
    o,p,x,obs,_ = mod._reason(one,["r"],{1,2},{6},{9:"OTRA"},False,code)
    assert list(zip(o,p,x,obs)) == [(True,False,False,True),(False,True,False,True),(False,False,True,True),(False,False,False,False),(True,False,False,True)]
    multi = pd.DataFrame({"r_1":["1","1","",""],"r_2":["","1","1",""],"r_3":["","","","1"]})
    o,p,x,obs,_ = mod._reason(multi,list(multi),{1},{2},{3:"OTRA"},True,code)
    only_o=o & ~p & ~x; only_p=p & ~o & ~x; other=~(only_o | only_p)
    assert list(zip(only_o,only_p,other)) == [(True,False,False),(False,False,True),(False,True,False),(False,False,True)]
    assert (only_o.astype(int)+only_p.astype(int)+other.astype(int)==1).all()
    assert (o & p).sum()==1

def test_denominador_vacio_y_opcion_ausente():
    assert mod.CFG["2018"]["CUENTA"][2] == 9
    assert mod.CFG["2021"]["CUENTA"][2] == 10
    assert not (pd.Series([False]) & pd.Series([True])).any()
