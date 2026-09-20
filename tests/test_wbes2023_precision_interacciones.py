"""Pruebas dirigidas de seis interacciones y contraste apareado WBES."""
import importlib.util
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/corrida0/CALC-WBES2023-PRECISION-INTERACCIONES-0001/medidor.py'
s=importlib.util.spec_from_file_location('int',p); M=importlib.util.module_from_spec(s); s.loader.exec_module(M)

def frame(rows):
 d={c:2 for c in M.REQUIRED}; d.update({'wmedian':1.,'a6a':1})
 out=[]
 for i,x in enumerate(rows):
  z=d.copy();z.update({'idstd':i+1,'strata':'A' if i<2 else 'B'});z.update(x);out.append(z)
 return pd.DataFrame(out)

def test_unknown_is_identification_not_ic():
 f=frame([{'c3':1,'c5':1},{'c3':1,'c5':2},{'c3':1,'c5':9},{'c3':2}])
 r,_=M._interaction(f,M.PARENT.INTERACTIONS[0])
 assert r['tasa_observada']==.5 and r['limite_inferior_faltantes']==1/3 and r['limite_superior_faltantes']==2/3
 assert r['anchura_identificacion_faltantes']==1/3 and r['ic95_inferior'] is not None

def test_common_universe_and_nonzero_covariance():
 f=frame([{'j3':1,'j5':1,'j13':1,'j15':1},{'j3':1,'j5':2,'j13':1,'j15':2},{'j3':1,'j5':1,'j13':1,'j15':2},{'j3':1,'j5':2,'j13':1,'j15':2}])
 r=M.contrast(f,'SINGLETON-CERTEZA')
 assert r['n_expuestos']==4 and r['cobertura_doble_expuestos']==1 and r['covarianza_diseno'] != 0
 assert r['tasa_observada']==.25

def test_frontier_and_empty_group_are_explicit():
 f=frame([{'c3':1,'c5':1},{'c3':1,'c5':1},{'c3':1,'c5':1},{'c3':1,'c5':1}])
 r,_=M._interaction(f,M.PARENT.INTERACTIONS[0])
 assert r['ic95_inferior'] is None and 'FRONTERA' in r['estado']
 g=frame([{'j3':2,'j13':2} for _ in range(4)])
 assert M.contrast(g,'SINGLETON-CERTEZA')['estado']=='NO-ESTIMABLE-SIN-SOPORTE'
