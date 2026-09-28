"""Regresión del agotamiento de memoria señalado en 00-INPUT-PR1194.md."""
import unittest
from unittest.mock import patch

import protocolo_v2
import test_sinteticos


class SinteticosV2(test_sinteticos.Sinteticos):
    @classmethod
    def setUpClass(cls):
        cls.swap = patch.object(test_sinteticos, 'exact_law', protocolo_v2.exact_law)
        cls.swap.start()

    @classmethod
    def tearDownClass(cls):
        cls.swap.stop()


class GuardaCardinalidad(unittest.TestCase):
    def reject_without_enumeration(self, frame):
        with patch.object(protocolo_v2, 'product', side_effect=AssertionError('enumeró antes de la guarda')) as spy:
            with self.assertRaisesRegex(ValueError, 'solo sintéticos pequeños'):
                protocolo_v2.exact_law(frame, {})
            spy.assert_not_called()

    def test_estrato_doce_upm(self):
        self.reject_without_enumeration([('h', str(i)) for i in range(12)])

    def test_producto_varios_estratos(self):
        # 4**4 * 4**4 * 3**3 excede el límite; cada estrato solo sí cabe.
        self.reject_without_enumeration([(h, str(i)) for h, n in [('a', 4), ('b', 4), ('c', 3)] for i in range(n)])

    def test_cardinalidad_mayor_que_entero_64_bits(self):
        self.reject_without_enumeration([(str(h), str(i)) for h in range(32) for i in range(2)])

    def test_ley_multiestrato_con_multiplicidades(self):
        frame = [(h, str(i)) for h in ['a', 'b'] for i in range(2)]
        contributions = {(h, str(i)): (i, 1) for h, i in frame}
        # Convertir el identificador textual a numerador.
        contributions = {key: (int(value[0]), value[1]) for key, value in contributions.items()}
        self.assertEqual(protocolo_v2.exact_law(frame, contributions),
                         {0.: 1/16, .25: 4/16, .5: 6/16, .75: 4/16, 1.: 1/16})


if __name__ == '__main__':
    unittest.main(verbosity=2)
