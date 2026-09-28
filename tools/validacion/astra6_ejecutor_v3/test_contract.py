#!/usr/bin/env python3
"""Compatibilidad sintética de los cuatro formatos residuales v2 y estados v3."""

import unittest

from tools.validacion.astra6_ejecutor_v3.contract import from_v2, validate


IDENTITY = {'paquete': 'SINTETICO', 'version_entrada': 'residuales-documentales-v2',
            'sha256_entrada': 'a' * 64}
COHORTS = {
    'ENBIARE': ('estimacion', 'ic95_inf', 'ic95_sup'),
    'ENCODAT': ('valor', 'ic95_inferior', 'ic95_superior'),
    'ENCUCI': ('estimacion', 'ic95_inf', 'ic95_sup'),
    'ENIGH': ('valor', 'ic_inferior', 'ic_superior'),
}


def doc(version, row):
    return {'version': version, 'identidad': IDENTITY.copy(), 'filas': [row]}


class ContractTest(unittest.TestCase):
    def test_four_v2_cohorts_preserve_numbers_and_aliases(self):
        for cohort, (point, lower, upper) in COHORTS.items():
            with self.subTest(cohort=cohort):
                row = {'llave': cohort, 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
                       'estado_ic': 'CALCULADO', point: '0.500', lower: '0.400', upper: '0.600'}
                result = from_v2(doc(2, row))
                self.assertEqual(result['filas'][0]['punto'], '0.500')
                self.assertEqual(result['filas'][0]['ic95_inf'], '0.400')
                self.assertEqual(result['filas'][0]['ic95_sup'], '0.600')
                self.assertEqual(result['mapa_campos'][0]['campos'], {
                    'punto': point, 'ic95_inf': lower, 'ic95_sup': upper})
                self.assertEqual(result['version'], 3)

    def test_v2_explicit_sin_ic_and_non_reconstructed_states(self):
        for state in ('NO-EVALUADO', 'NO-RECALCULABLE-DESDE-SPEC',
                      'BLOQUEADO-POR-ACCESO'):
            with self.subTest(state=state):
                row = {'llave': 'x', 'unidad': 'media', 'estado': state, 'estado_ic': 'SIN-IC'}
                if state != 'NO-EVALUADO':
                    row['motivo'] = 'causa declarada'
                self.assertEqual(from_v2(doc(2, row))['filas'][0]['estado'], state)
        row = {'llave': 'x', 'unidad': 'media', 'estado': 'RECONSTRUIDO',
               'punto': '0', 'estado_ic': 'SIN-IC'}
        self.assertEqual(from_v2(doc(2, row))['filas'][0]['punto'], '0')

    def test_v3_genuine_states(self):
        for state in ('DENOMINADOR-CERO', 'NO-ESTIMABLE'):
            with self.subTest(state=state):
                row = {'llave': 'x', 'unidad': 'proporcion', 'estado': state,
                       'motivo': 'spec suficiente; condición observada'}
                self.assertEqual(validate(doc(3, row))['filas'][0]['estado'], state)
        point = {'llave': 'x', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
                 'punto': '0.25', 'estado_ic': 'NO-IDENTIFICADA',
                 'motivo_ic': 'varianza sin identificación'}
        self.assertEqual(validate(doc(3, point))['filas'][0]['punto'], '0.25')

    def test_ambiguity_and_false_zero_rejected(self):
        base = {'llave': 'x', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO', 'punto': '0.2'}
        with self.assertRaises(ValueError):
            from_v2(doc(2, base))  # IC ausente, no declaración SIN-IC
        with self.assertRaises(ValueError):
            from_v2(doc(2, base | {'ic95_inf': None, 'ic95_sup': None}))
        with self.assertRaises(ValueError):
            validate(doc(3, {'llave': 'x', 'unidad': 'proporcion',
                             'estado': 'DENOMINADOR-CERO', 'motivo': 'n=0', 'punto': 0}))
        with self.assertRaises(ValueError):
            validate(doc(3, base | {'estado_ic': 'NO-IDENTIFICADA'}))
        with self.assertRaises(ValueError):
            validate(doc(3, base | {'estado_ic': 'CALCULADO',
                                    'ic95_inf': '0.1', 'ic95_sup': None}))
        with self.assertRaises(ValueError):
            validate(doc(3, base | {'estado_ic': 'SIN-IC', 'ic95_inf': None,
                                    'ic95_sup': None}))


if __name__ == '__main__':
    unittest.main()
