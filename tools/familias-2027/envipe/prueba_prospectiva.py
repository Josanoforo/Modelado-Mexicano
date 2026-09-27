"""Prueba del evaluador puro futuro solamente con filas sintéticas."""
import copy
import unittest

from medidor import FAMILIAS
from prospectiva import evaluar
from pruebas import Pruebas


class Prospectiva(Pruebas):
    def test_sin_metadatos_no_evaluacion(self):
        self.assertEqual(evaluar(None, None, None, {})['estado'], 'NO-COMPARABLE')

    def test_diferencia_p0_fijo_sin_sustituir_peso(self):
        meta = dict(id='envipe_2027', estado='RESERVADA', instrumento='ENVIPE',
                    familias=list(FAMILIAS), aperturas=1, comparabilidad='VERIFICADA',
                    autorizacion_ola='FIRMADA', descriptor_sha256='a'*64,
                    cuestionario_sha256='b'*64, commit2_sha256='c'*64)
        emisiones = {k: {'p0': .25, 'R_futura': None, 'retadores': []} for k in FAMILIAS}
        out = evaluar(self.tablas, self.s, emisiones, meta)
        for name in FAMILIAS:
            self.assertTrue((out['d_k'][name] == out['R_k'][name] - .25).all() or
                            # Algunas réplicas del dominio sintético tienen masa cero.
                            __import__('numpy').allclose(out['d_k'][name], out['R_k'][name] - .25, equal_nan=True))
            self.assertEqual(out['resultados'][name]['dictamen'], 'NO-ESTIMABLE')
        emisiones['DENUNCIA_U4']['retadores'] = ['intruso']
        with self.assertRaises(ValueError): evaluar(self.tablas, self.s, emisiones, meta)


if __name__ == '__main__':
    unittest.main()
