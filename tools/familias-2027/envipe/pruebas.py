"""Pruebas de fronteras, universo, peso y mutación del lector cerrado."""
import copy
import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np
import yaml

from medidor import COLUMNAS, activacion, construir, dictamen, leer, medir
from ejecuta import SPEC
from audita import auditar


def sintetico(spec, path):
    per = [dict(zip(COLUMNAS['persona'], [str(i), str(10*i), '1', str(i)])) for i in range(1, 5)]
    # Duplicar delitos positivos no duplica personas. Blanco/99 excluye U1,
    # pero queda cero en evasión y conserva el denominador delito.
    rows = [('1','a','5','2','1','1','1','1'),
            ('1','b','5','2','8','1','1','1'),
            ('2','c','5','2','3','8','1','2'),
            ('3','d','5','2','99','1','1','3'),
            ('4','e','5','1','','1','1','4')]
    mod = [dict(zip(COLUMNAS['modulo'], r)) for r in rows]
    with zipfile.ZipFile(path, 'w') as z:
        for name, data in [('persona', per), ('modulo', mod)]:
            text = io.StringIO()
            w = csv.DictWriter(text, fieldnames=COLUMNAS[name]); w.writeheader(); w.writerows(data)
            z.writestr(spec['tablas'][name], text.getvalue())
        z.writestr('prohibido.csv', 'SEXO,EDAD\n1,30\n')
    return {'persona': per, 'modulo': mod}


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.s = yaml.safe_load(SPEC.read_text())
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'sintetico.zip'
        self.tablas = sintetico(self.s, self.path)

    def test_mutacion_codigo(self):
        code = Path(__file__).with_name("medidor.py").read_text()
        self.assertTrue(auditar(code))
        for mutation in ["\nimport pandas\n", "\nexec(\"x=1\")\n", "\nnp.read_csv(\"otro\")\n"]:
            with self.assertRaises(ValueError): auditar(code + mutation)

    def test_unidad_ponderador_colapso(self):
        diag, reps = medir(leer(self.path, self.s, 'sintetico'), self.s)
        self.assertAlmostEqual(diag['familias']['DENUNCIA_U4']['punto'], 1/3)
        self.assertEqual(diag['familias']['DENUNCIA_U4']['n'], 2)
        self.assertAlmostEqual(diag['familias']['EVASION_NORMA']['punto'], 1/12)
        self.assertEqual(diag['familias']['EVASION_NORMA']['n'], 5)
        self.assertEqual(diag['exclusiones']['u1_ns_nr'], 1)
        self.assertEqual(diag['exclusiones']['personas_sin_u1_por_exclusion'], 1)
        self.assertEqual(reps['DENUNCIA_U4'].shape, (2000,))

    def test_fronteras_y_compuertas(self):
        casos = [(-.05,.05,'INDETERMINADO'),(.007,.013,'COMPATIBLE-CON-TOLERANCIA'),
                 (.021,.03,'DESVÍO-MATERIAL'),(-.02,.02,'COMPATIBLE-CON-TOLERANCIA'),
                 (.02,.025,'INDETERMINADO'),(-.025,-.02,'INDETERMINADO'),
                 (.0201,.025,'DESVÍO-MATERIAL')]
        for lo, hi, esperado in casos:
            self.assertEqual(dictamen(lo,hi), esperado)
        self.assertEqual(dictamen(0, 0, comparable=False), 'NO-COMPARABLE')
        for lo, hi in [(np.nan, 0), (1, 0), (0, np.inf)]:
            self.assertEqual(dictamen(lo, hi), 'NO-ESTIMABLE')

    def test_mutacion_columnas_agrupacion_identidad_futuro(self):
        for change in ('columna', 'agrupacion'):
            s = copy.deepcopy(self.s)
            if change == 'columna': s['columnas']['persona'].append('SEXO')
            else: s['agrupacion'].append('EDAD')
            with self.assertRaises(ValueError): leer(self.path, s, 'sintetico')
        with self.assertRaises(ValueError): leer(self.path, self.s, 'historico')
        with self.assertRaises(ValueError): leer(self.path, self.s, 'futuro')

    def test_mutacion_uniones_pesos_diseno(self):
        for campo, valor in [('ID_PER','desconocida'), ('FAC_DEL','0'), ('EST_DIS','2')]:
            t = copy.deepcopy(self.tablas); t['modulo'][0][campo] = valor
            with self.assertRaises(ValueError): construir(t)
        t = copy.deepcopy(self.tablas); t['persona'].append(t['persona'][0])
        with self.assertRaises(ValueError): construir(t)

    def test_singleton_y_dependencia(self):
        t = copy.deepcopy(self.tablas)
        for p in t['persona']: p['UPM_DIS'] = '1'
        for f in t['modulo']: f['UPM_DIS'] = '1'
        d, r = medir(t, self.s)
        self.assertEqual(d['diseno']['singleton_marco'], 1)
        self.assertTrue(all(not x['estimable'] for x in d['familias'].values()))
        for name in r: self.assertTrue(np.all(r[name] == r[name][0]))

    def test_preflight_metadatos_no_autoriza_apertura(self):
        self.assertFalse(activacion({}))
        m = dict(id='envipe_2027', estado='RESERVADA', instrumento='ENVIPE',
                 familias=['DENUNCIA_U4','EVASION_NORMA'], aperturas=1,
                 comparabilidad='VERIFICADA', autorizacion_ola='FIRMADA',
                 descriptor_sha256='a'*64, cuestionario_sha256='b'*64, commit2_sha256='c'*64)
        self.assertTrue(activacion(m))
        m['aperturas'] = 2; self.assertFalse(activacion(m))


if __name__ == '__main__':
    unittest.main()
