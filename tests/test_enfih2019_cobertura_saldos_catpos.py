import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

P = Path(__file__).parents[1] / "data/corrida0/CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001/medidor.py"
S = importlib.util.spec_from_file_location("catpos", P); M = importlib.util.module_from_spec(S); S.loader.exec_module(M)

def _frames():
    c = pd.DataFrame([
        ["1","1","1","1","0","2","1","u1","1"],["2","1","1","1","100","3","1","u1","1"],
        ["3","1","1","1","0","5","2","u2","2"],["4","1","1","1","50","7","2","u2",""],
    ], columns=M.CONC)
    q = pd.DataFrame([
        ["1","1","1","1","1","000000000"],["2","1","1","1","1","000000100"],
        ["3","1","1","1","1","999999999"],["4","1","1","1","1","000000050"],
        ["4","1","1","2","1","999999888"],
    ], columns=M.MOD)
    return c,q

def test_estados_cero_parcial_y_residuo():
    d=M.classify(*_frames()); assert d.state.tolist()==["COMPLETO-CERO","COMPLETO-POSITIVO","DESCONOCIDO-TOTAL","PARCIAL"]
    assert d.cat.tolist()==["1","1","2","DESCONOCIDO"]

def test_resto_no_solapa_y_media_es_invariante_a_escala_de_pesos():
    d=M.classify(*_frames()); w=pd.to_numeric(d.FAC_HOG).to_numpy(float)
    a,b=M.point_table(d,w),M.point_table(d,w*13); con=M.contrasts(d,w)
    assert np.isclose(a["1"]["media"],b["1"]["media"])
    assert con["1"]["sin_solapamiento"]
    assert M.weighted_quantile([0,10,20],[1,2,1],.5)==10
