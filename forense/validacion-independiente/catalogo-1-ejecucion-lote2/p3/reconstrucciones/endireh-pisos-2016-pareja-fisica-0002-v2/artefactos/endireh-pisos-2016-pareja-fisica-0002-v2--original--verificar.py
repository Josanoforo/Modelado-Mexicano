#!/usr/bin/env python3
"""Pruebas de reglas de respuesta e integridad de los artefactos congelables."""
import json
import unittest
import numpy as np
import pandas as pd
from reconstruir import BASE, responses, sha_file


class Verificacion(unittest.TestCase):
    def test_reglas_y_saltos(self):
        life = np.full((6, 9), 4.)
        recent = np.full((6, 9), np.nan)
        life[1, 0] = 1; recent[1, 0] = 3
        life[2, 0] = 9
        life[3, 0] = 2; life[3, 1] = 9; recent[3, 0] = 4
        life[4, 0] = np.nan; recent[4, 1] = 1
        life[5, 0] = 3; recent[5, 0] = 4
        a, b = responses(life, recent)
        np.testing.assert_equal(a, [0, 1, np.nan, 1, np.nan, 1])
        np.testing.assert_equal(b, [0, 1, np.nan, np.nan, np.nan, 0])

    def test_llaves_sin_asignacion(self):
        source = pd.read_csv(BASE/'entrada/estimandos.tsv', sep='\t', dtype=str)
        out = pd.read_csv(BASE/'reconstruccion.tsv', sep='\t', dtype=str)
        pd.testing.assert_frame_equal(source, out[source.columns])
        self.assertTrue((out.estado == 'NO-RECALCULABLE-DESDE-SPEC').all())
        self.assertTrue(out.motivo.notna().all())
        self.assertTrue(out[['proporcion','ic95_inf','ic95_sup']].isna().all().all())

    def test_agregados(self):
        calc = pd.read_csv(BASE/'calculos_por_ventana.tsv', sep='\t')
        rep = pd.read_csv(BASE/'replicas_agregadas.tsv', sep='\t')
        self.assertEqual(len(calc), 92)
        self.assertEqual(len(rep), 46000)
        self.assertFalse({'ID_MUJ','UPM_DIS','EST_DIS'} & set(rep.columns))
        for _, g in rep.groupby(['ventana','eje','segmento']):
            self.assertEqual(set(g.replica), set(range(1,501)))
        self.assertTrue((rep.denominador > 0).all())
        np.testing.assert_allclose(rep.proporcion, rep.numerador / rep.denominador, atol=1e-15)
        pub = calc[calc.publicable]
        self.assertTrue(pub.proporcion.between(0,1).all())
        self.assertTrue((pub.ic95_inf <= pub.ic95_sup).all())
        self.assertTrue((pub.ic95_sup - pub.ic95_inf <= .20).all())
        self.assertTrue((pub.n_conocida >= 100).all())
        self.assertTrue((pub.upm_con_respuesta >= 5).all())
        self.assertTrue((pub.loc[pub.proporcion > 0, 'cv'] <= .30).all())

    def test_hashes(self):
        r = json.loads((BASE/'recibo.json').read_text())
        self.assertEqual(r['manifiesto_sha256'], sha_file(BASE/'entrada/manifiesto.json'))
        for name, digest in r['salidas_sha256'].items():
            self.assertEqual(digest, sha_file(BASE/name), name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
