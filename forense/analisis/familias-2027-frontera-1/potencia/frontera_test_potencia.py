"""Regresiones: una familia parcial nunca recomienda lanzamiento (#1195)."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).with_name('calcula.py')
spec = importlib.util.spec_from_file_location('frontera_potencia', SOURCE)
calcula = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calcula)


class LaunchCoverage(unittest.TestCase):
    def run_cli(self, family, groups):
        # Aislamiento de salidas: jamás sobreescribir evidencia histórica real.
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copy(SOURCE, root / 'calcula.py')
            shutil.copy(SOURCE.with_name('criterios-previos.md'), root / 'criterios-previos.md')
            gold = root / 'fixture.json'
            gold.write_text(json.dumps({'grupos': groups}))
            flag = '--gold-se' if family == 'ENSU' else '--enoe-gold-se'
            subprocess.run([sys.executable, str(root / 'calcula.py'), flag, str(gold)],
                           check=True, capture_output=True, text=True)
            return json.loads((root / 'frontera-potencia-resultados.json').read_text())

    def assert_partial_refused(self, family, groups, reason):
        result = self.run_cli(family, groups)
        # El grupo restante sí supera potencia: reproduce el falso positivo reportado.
        rows = [r for r in result['gold_scenarios'] if r['group'].startswith(family + '-')]
        self.assertTrue(rows)
        self.assertTrue(all(r['meets_per_group_target'] for r in rows))
        self.assertEqual(result['decision_by_family'][family], 'NO-LANZAR-TODAVIA')
        blocks = [b for b in result['gold_inference_blocks'] if b['family'] == family]
        self.assertIn(reason, [b['reason'] for b in blocks])
        self.assertTrue(all(r['joint_lower_bound_stability'] is None for r in rows))

    def test_one_group_blocked(self):
        for family in ('ENSU', 'ENOE'):
            with self.subTest(family=family):
                self.assert_partial_refused(family, {
                    '1': {'se_taylor': .0001},
                    '2': {'se_taylor': None, 'singleton': ['fixture']}},
                    'SE-TAYLOR-NULA-SINGLETON')

    def test_one_group_absent(self):
        for family in ('ENSU', 'ENOE'):
            with self.subTest(family=family):
                self.assert_partial_refused(family, {'1': {'se_taylor': .0001}}, 'GRUPO-AUSENTE')

    def test_invalid_se(self):
        for value in (0., -.01, float('nan'), float('inf'), True, '0.0001'):
            with self.subTest(se=value):
                self.assert_partial_refused('ENOE', {
                    '1': {'se_taylor': .0001}, '2': {'se_taylor': value}},
                    'SE-TAYLOR-INVALIDA')

    def test_complete_family_can_pass(self):
        for family in ('ENSU', 'ENOE'):
            with self.subTest(family=family):
                result = self.run_cli(family, {
                    '1': {'se_taylor': .0001}, '2': {'se_taylor': .0001}})
                self.assertEqual(result['decision_by_family'][family],
                                 'PREPARAR-LANZAMIENTO-CONDICIONAL')
                rows = [r for r in result['gold_scenarios'] if r['group'].startswith(family + '-')]
                self.assertEqual(len(rows), 6)
                self.assertTrue(all(r['joint_lower_bound_stability'] is not None for r in rows))

    def test_missing_or_duplicate_scenario(self):
        rows, blocks = calcula.gold_family({'grupos': {
            '1': {'se_taylor': .0001}, '2': {'se_taylor': .0001}}}, 'ENOE')
        for altered in (rows[:-1], rows[:-1] + [rows[0]]):
            with self.subTest(keys=[r['group'] for r in altered]):
                self.assertEqual(calcula.family_decision(altered, blocks, 'ENOE'),
                                 'NO-LANZAR-TODAVIA')

    def test_block_with_complete_rows(self):
        rows, blocks = calcula.gold_family({'grupos': {
            '1': {'se_taylor': .0001}, '2': {'se_taylor': .0001}}}, 'ENOE')
        blocks.append({'family': 'ENOE', 'reason': 'fixture'})
        self.assertEqual(calcula.family_decision(rows, blocks, 'ENOE'), 'NO-LANZAR-TODAVIA')


if __name__ == '__main__':
    unittest.main()
