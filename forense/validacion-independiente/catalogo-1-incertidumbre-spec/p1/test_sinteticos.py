import unittest
import numpy as np
from protocolo import exact_law, reference, publicable, prepare

class Sinteticos(unittest.TestCase):
    def setUp(self):
        self.f=[('h','a'),('h','b')];self.c={self.f[0]:(0,1),self.f[1]:(1,1)}
    def test_ley_binomial(self): self.assertEqual(exact_law(self.f,self.c),{0:.25,.5:.5,1:.25})
    def test_orden(self):
        np.testing.assert_array_equal(reference(self.f,self.c)['replicas'],reference(self.f[::-1],self.c)['replicas'])
    def test_pesos(self): self.assertAlmostEqual(reference(self.f,{self.f[0]:(0,1),self.f[1]:(3,3)})['point'],.75)
    def test_semilla_fija(self):
        np.testing.assert_array_equal(reference(self.f,self.c)['replicas'],reference(self.f,self.c)['replicas'])
    def test_singleton(self):
        r=reference([('h','a')],{('h','a'):(1,2)})
        self.assertEqual(r['singleton'],1);self.assertEqual(r['se'],0)
    def test_dominio_cero_es_marco(self):
        c={self.f[0]:(1,1)};law=exact_law(self.f,c)
        self.assertEqual(law, {1.:.75,'NO-ESTIMABLE':.25})
        self.assertEqual(exact_law([self.f[0]],c),{1.:1.})
    def test_marco_extra_cambia_ley(self):
        f=self.f+[('h','c')];self.assertNotEqual(exact_law(f,self.c),exact_law(self.f,self.c))
    def test_denominador_cero(self):
        r=reference(self.f,{});self.assertIsNone(r['interval']);self.assertEqual(r['nonestimable'],200)
    def test_percentil_lineal(self):
        r=reference(self.f,self.c);np.testing.assert_equal(r['interval'],np.quantile(r['replicas'],[.025,.975],method='linear'))
    def test_frontera_cv(self):
        self.assertTrue(publicable(100,5,.1,0,.1,.03));self.assertFalse(publicable(100,5,.1,0,.1,.030001))
    def test_frontera_ancho(self):
        self.assertTrue(publicable(100,5,.5,0,.2,.01));self.assertFalse(publicable(100,5,.5,0,.200001,.01))
    def test_soporte_y_noestimable(self):
        self.assertFalse(publicable(99,5,.5,0,.1,.01));self.assertFalse(publicable(100,4,.5,0,.1,.01));self.assertFalse(publicable(100,5,.5,0,.1,.01,1))
    def test_cero(self): self.assertTrue(publicable(100,5,0,0,0,0))
    def test_guardias(self):
        for frame,c in [(self.f*2,self.c),(self.f,{('h','x'):(1,1)}),(self.f,{self.f[0]:(2,1)})]:
            with self.assertRaises(ValueError): prepare(frame,c)

if __name__=='__main__':unittest.main(verbosity=2)
