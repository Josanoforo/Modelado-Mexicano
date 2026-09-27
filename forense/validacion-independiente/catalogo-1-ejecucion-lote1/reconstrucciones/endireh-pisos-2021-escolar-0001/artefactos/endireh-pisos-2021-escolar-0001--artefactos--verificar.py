"""Controles de lógica y de integridad; no usan resultados esperados externos."""
import unittest
import numpy as np
import pandas as pd
from reconstruir import BASE, unions

class Verificacion(unittest.TestCase):
    def test_uniones_y_saltos(self):
        a = np.full((7,18),2.)
        b = np.full((7,18),np.nan)
        a[1,0] = 1; b[1,0] = 3
        a[2,0] = np.nan
        a[3,0] = 1  # respuesta reciente faltante
        a[4,0] = 1; b[4,0] = 4
        a[5,0] = 1; b[5,0] = 1
        a[6,0] = 1; b[6,0] = 1; a[6,1] = np.nan
        life, recent = unions(a,b,np.array([1,1,1,1,1,0,1],bool),
                                    np.array([1,1,1,1,0,0,1],bool))
        np.testing.assert_equal(life,[0,1,np.nan,1,1,np.nan,1])
        np.testing.assert_equal(recent,[0,1,np.nan,np.nan,np.nan,np.nan,1])

    def test_cobertura_y_no_asignacion(self):
        wanted = pd.read_csv(BASE/'entrada/estimandos.tsv',sep='\t')
        got = pd.read_csv(BASE/'reconstruccion.tsv',sep='\t')
        self.assertEqual(wanted.llave.tolist(),got.llave.tolist())
        self.assertTrue(got[['punto','ic95_inf','ic95_sup']].isna().all().all())
        self.assertTrue(got.estado.eq('NO-RECALCULABLE-DESDE-SPEC').all())
        self.assertTrue(got.motivo.notna().all())

    def test_publicacion_y_replicas(self):
        results = pd.read_csv(BASE/'calculos_sin_asignar.tsv',sep='\t',dtype={'segmento':str})
        reps = pd.read_csv(BASE/'replicas_publicables.tsv',sep='\t',dtype={'segmento':str})
        keys = ['periodo','eje','segmento']
        self.assertFalse(results.duplicated(keys).any())
        for row in results.itertuples():
            sample = reps[(reps.periodo==row.periodo)&(reps.eje==row.eje)&(reps.segmento==row.segmento)]
            if row.publicable:
                self.assertEqual(len(sample),200)
                self.assertGreaterEqual(row.n_conocido,100)
                self.assertGreaterEqual(row.upm_con_casos,5)
                self.assertTrue(0<=row.punto<=1)
                self.assertTrue(0<=row.ic95_inf<=row.ic95_sup<=1)
                self.assertLessEqual(row.ic95_sup-row.ic95_inf,.20)
                np.testing.assert_allclose(np.quantile(sample.punto,[.025,.975]),
                                           [row.ic95_inf,row.ic95_sup],atol=1e-15)
                if row.punto>0:
                    self.assertLessEqual(sample.punto.std(ddof=1)/row.punto,.30)
            else:
                self.assertEqual(len(sample),0)
                self.assertTrue(pd.isna(row.punto))
                self.assertTrue(pd.notna(row.motivo))

if __name__=='__main__': unittest.main(verbosity=2)
