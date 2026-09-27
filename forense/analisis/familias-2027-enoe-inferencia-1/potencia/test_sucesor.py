"""Guardas materiales P5; fixtures no son SE del oro."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sucesor', Path(__file__).with_name('calcula_sucesor.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PowerGuards(unittest.TestCase):
    def evaluate(self, groups):
        return module.evaluate({'grupos': groups}, json.loads(module.GOLD.read_text()))

    def test_missing_group(self):
        result = self.evaluate({'1': {'se_taylor': .0001}})
        self.assertEqual(result['decision'], 'NO-LANZAR-TODAVIA')
        self.assertEqual(len(result['scenarios']), 6)
        self.assertTrue(all(r['mde'] is None for r in result['scenarios']))

    def test_invalid_se(self):
        for se in (None, 0., -.01, float('nan'), float('inf'), True, '.0001'):
            with self.subTest(se=se):
                self.assertFalse(self.evaluate({'1': {'se_taylor': .0001}, '2': {'se_taylor': se}})['inference_identifiable'])

    def test_incomplete_or_duplicate_scenarios(self):
        rows, blocks = module.contract.gold_family({'grupos': {
            '1': {'se_taylor': .0001}, '2': {'se_taylor': .0001}}}, 'ENOE')
        for altered in (rows[:-1], rows[:-1] + [rows[0]]):
            self.assertEqual(module.contract.family_decision(altered, blocks, 'ENOE'), 'NO-LANZAR-TODAVIA')

    def test_methodological_block_and_fixed_p0(self):
        result = self.evaluate({'1': {'se_taylor': .0001, 'razon_bloqueo': 'INSTRUCCION-FALTANTE'},
                                '2': {'se_taylor': .0001}})
        self.assertFalse(result['inference_identifiable'])
        gold = json.loads(module.GOLD.read_text())
        self.assertEqual(result['scenarios'][0]['p0_fijo'], gold['grupos']['1']['p0'])

    def test_complete_fixture_import_identity(self):
        result = self.evaluate({'1': {'se_taylor': .0001}, '2': {'se_taylor': .0002}})
        self.assertTrue(result['inference_identifiable'])
        self.assertEqual(len(result['scenarios']), 6)
        expected = module.contract.calculate('ENOE-SEX-1', .0001, 0., 0.)
        self.assertEqual(result['scenarios'][0]['conditional_fixed_p0_mde'], expected['conditional_fixed_p0_mde'])


if __name__ == '__main__':
    unittest.main()
