"""Pruebas sintéticas: no abre respuestas reales."""
from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/corrida0/CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001/medidor.py"
S=importlib.util.spec_from_file_location("m",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)

class ConsistenciaFamiliaTest(unittest.TestCase):
    def setUp(self):
        self.f=pd.DataFrame({"SEX":[1,2,9,1],"WEIGHT":[1,1,1,1],"v21":[1,3,2,8],"v22":[2,3,2,1],"v23":[1,4,7,1],"v24":[2,5,6,1],"v25":[1,6,3,1]})
        self.r=M.calculate(self.f)
    def test_conteo_particion_y_residuo(self):
        count,_,_,_,_,_,control=self.r
        self.assertEqual(sum(x["n_numerador"] for x in count if x["dominio_id"]=="TOTAL"),3)
        self.assertEqual(control["sexo_residuo_n"],1)
    def test_matrices_nativas_tienen_ceros_y_sensibilidad(self):
        native,sens=self.r[2:4]
        self.assertEqual(len(native),490); self.assertEqual(len(sens),490)
        self.assertTrue(any(x["n_numerador"]==0 for x in native))
    def test_ocho_no_es_no_familia(self):
        two=self.r[4]
        pair=[x for x in two if x["universo_matriz"]=="CINCO-RESPUESTAS-VALIDAS" and x["variable_a"]=="v21" and x["variable_b"]=="v22"]
        self.assertEqual(pair[0]["n_denominador"],3)
    def test_2x2_se_reconstruye_de_matriz(self):
        native,two=self.r[2],self.r[4]
        p=[x for x in native if x["universo_matriz"]=="CINCO-RESPUESTAS-VALIDAS" and x["variable_a"]=="v21" and x["variable_b"]=="v22" and x["codigo_a"] in (1,2) and x["codigo_b"] in (1,2)]
        cell=next(x for x in two if x["universo_matriz"]=="CINCO-RESPUESTAS-VALIDAS" and x["variable_a"]=="v21" and x["variable_b"]=="v22" and x["familia_a"]=="FAMILIA" and x["familia_b"]=="FAMILIA")
        self.assertEqual(cell["n_numerador"],sum(x["n_numerador"] for x in p))
    def test_condicional_nula_se_rotula(self):
        f=pd.DataFrame({"SEX":[1],"WEIGHT":[1],**{v:[3] for v,_,_ in M.VARS}})
        assoc=M.calculate(f)[5]
        self.assertTrue(any(x["estado"]=="CONDICIONAL-NO-ESTIMABLE" for x in assoc))

if __name__=="__main__": unittest.main()
