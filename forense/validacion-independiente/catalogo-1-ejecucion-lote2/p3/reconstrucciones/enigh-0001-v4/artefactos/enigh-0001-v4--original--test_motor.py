"""Pruebas sintéticas propias, sin resultados esperados externos."""
import unittest
from reconstruir import calcular_familia_a


class MotorTest(unittest.TestCase):
    def test_pesos_y_estratos_unicos(self):
        result = calcular_familia_a({'001': {'0000001': [3., 4.]},
                                    '01': {'1': [0., 2.]}})
        self.assertEqual(result['estimacion'], .5)
        self.assertEqual(result['ic_inferior'], .5)
        self.assertEqual(result['ic_superior'], .5)
        self.assertEqual(result['naturaleza_ic'], 'IC-CON-ESTRATOS-DE-UPM-UNICA')

    def test_remuestrea_upm_y_reproduce(self):
        groups = {'001': {'01': [1., 1.], '1': [0., 3.]}}
        result = calcular_familia_a(groups)
        self.assertEqual(result, calcular_familia_a(groups))
        self.assertEqual(result['estimacion'], .25)
        self.assertEqual(result['ic_inferior'], 0.)
        self.assertEqual(result['ic_superior'], 1.)


if __name__ == '__main__':
    unittest.main()
