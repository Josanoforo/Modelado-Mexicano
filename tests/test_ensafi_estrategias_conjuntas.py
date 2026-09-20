import importlib.util
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'data/corrida0/CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001/medidor.py'
S = importlib.util.spec_from_file_location('ec', P); M = importlib.util.module_from_spec(S); S.loader.exec_module(M)

def row(h,u,a,b,weight=1):
    r={'EST_DIS':h,'UPM_DIS':u,'FAC_ELE':str(weight),'P6_9':'2'}
    for i in M.ITEMS:r[i]='2'
    r['P6_10_1']=a;r['P6_10_2']=b
    return r

class EstrategiasConjuntasTest(unittest.TestCase):
    def test_diferencia_pareada_no_suma_varianzas_independientes(self):
        rows=[row('A','1','1','1'),row('A','2','1','2'),row('B','1','2','1'),row('B','2','2','2')]
        strata,_,_=M.design(rows); df=2
        full=lambda x: all(M.c(x[i]) in M.VALID for i in M.ITEMS)
        a=M.ratio(rows,full,lambda x:float(M.c(x['P6_10_1'])=='1')); b=M.ratio(rows,full,lambda x:float(M.c(x['P6_10_2'])=='1'))
        d,se,_,_,state=M.diff(a,b,strata,df)
        self.assertEqual(d,0.0); self.assertEqual(state,'ESTIMABLE:T95-INFLUENCIA-CONJUNTA')
        self.assertIsNotNone(se)

    def test_desconocido_no_se_convierte_en_no(self):
        x=row('A','1','9','2')
        self.assertNotIn(M.c(x['P6_10_1']),M.VALID)

if __name__ == '__main__': unittest.main()
