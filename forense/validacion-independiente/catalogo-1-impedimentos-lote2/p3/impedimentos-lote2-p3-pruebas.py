#!/usr/bin/env python3
"""Controles de proyección con ZIP/CSV/DTA exclusivamente sintéticos."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).absolute().parent
CODE = ROOT / 'impedimentos-lote2-p3-proyecta.py'
spec = importlib.util.spec_from_file_location('proyecta', CODE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
compiler_spec = importlib.util.spec_from_file_location('compila', ROOT / 'impedimentos-lote2-p3-compila.py')
compiler = importlib.util.module_from_spec(compiler_spec)
compiler_spec.loader.exec_module(compiler)
REPO = next(p for p in ROOT.parents if (p / '.git').exists())


class Custodia(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='p3-sintetico-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.custody = self.base / 'custodia'
        self.custody.mkdir(mode=0o700)
        self.src = self.custody / 'fuente.zip'
        self.out = self.base / 'reducido'
        self.contract = self.base / 'contrato'
        self.signature = self.base / 'firma'
        self.key = self.base / 'public.pem'
        self.private = self.base / 'private.pem'
        self.run_ssl('genpkey', '-algorithm', 'Ed25519', '-out', str(self.private))
        self.run_ssl('pkey', '-in', str(self.private), '-pubout', '-out', str(self.key))
        self.trusted = module.sha(self.key.read_bytes())
        self.archive({'tabla.csv': b'ID,EDAD,CREDITO,RESERVADA\n1,33,TRAMPA-CREDITO,SECRETO-XYZ\n'})
        self.c = {'schema': 'custodia-proyeccion-v1', 'approved': True,
                  'operation': 'project', 'signer_key_sha256': self.trusted,
                  'human_signature': {'reference': 'ACTO-SINTETICO', 'literal': 'FIRMA-SINTETICA',
                    'body_sha256': '1' * 64, 'scope': 'project', 'verified_by_custodian': True,
                    'reservation_scopes': []}, 'publication_authorized': False,
                  'code_sha256': module.sha(CODE.read_bytes()), 'source_sha256': module.sha(self.src.read_bytes()),
                  'mode': 'synthetic', 'custodian_uid': os.getuid(), 'analyst_uid': os.getuid(),
                  'purpose': 'control sintético; sin autorización real', 'signer': 'clave efímera sintética',
                  'act': 'P3-CONTROL-SINTETICO', 'max_member_bytes': 10_000_000,
                  'max_archive_bytes': 10_000_000, 'archive_inventory': ['tabla.csv'],
                  'members': {'tabla.csv': {'columns': ['ID', 'EDAD'], 'purpose': 'edad sintética',
                                           'format': 'csv', 'encoding': 'utf-8', 'delimiter': ',',
                                           'output': 'tabla.csv'}}}

    def run_ssl(self, *args):
        subprocess.run(['openssl', *args], check=True, capture_output=True)

    def archive(self, entries):
        with zipfile.ZipFile(self.src, 'w') as z:
            for name, b in entries.items():
                z.writestr(name, b)
        self.src.chmod(0o600)

    def sign(self):
        self.contract.write_text(json.dumps(self.c, ensure_ascii=False), encoding='utf-8')
        self.run_ssl('pkeyutl', '-sign', '-inkey', str(self.private), '-rawin',
                     '-in', str(self.contract), '-out', str(self.signature))

    def project(self, **overrides):
        args = dict(contract=str(self.contract), signature=str(self.signature), public_key=str(self.key),
                    trusted_key_sha256=self.trusted, source=str(self.src), output=str(self.out), clone=str(REPO))
        args.update(overrides)
        return module.proyecta(**args)

    def rejected(self, **overrides):
        self.sign()
        with self.assertRaises((module.Rechazo, OSError, ValueError, KeyError)):
            self.project(**overrides)
        if not self.out.exists():
            self.assertFalse(self.out.exists())

    def test_minimo_no_centanelas_csv(self):
        self.sign()
        r = self.project()
        self.assertEqual((self.out / 'tabla.csv').read_text(), 'ID,EDAD\n1,33\n')
        self.assertEqual(set(p.name for p in self.out.iterdir()), {'tabla.csv', 'recibo.json'})
        for p in self.out.iterdir():
            self.assertNotIn(b'SECRETO-XYZ', p.read_bytes())
            self.assertNotIn(b'TRAMPA-CREDITO', p.read_bytes())
        self.assertEqual(r['outputs']['tabla.csv'], module.sha((self.out / 'tabla.csv').read_bytes()))

    def test_minimo_dta(self):
        import pandas as pd
        b = io.BytesIO()
        pd.DataFrame({'ID': [1], 'EDAD': [33], 'RESERVADA': ['SECRETO-XYZ']}).to_stata(b, write_index=False)
        self.archive({'tabla.dta': b.getvalue()})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.c['archive_inventory'] = ['tabla.dta']
        self.c['members'] = {'tabla.dta': dict(self.c['members']['tabla.csv'], format='dta')}
        self.sign()
        self.project()
        self.assertEqual((self.out / 'tabla.csv').read_text(), 'ID,EDAD\n1,33\n')

    def test_firma_ausente(self):
        self.sign()
        self.signature.unlink()
        with self.assertRaises(OSError): self.project()
        self.assertFalse(self.out.exists())

    def test_firma_erronea(self):
        self.sign()
        self.signature.write_bytes(b'x' * 64)
        with self.assertRaises(module.Rechazo): self.project()
        self.assertFalse(self.out.exists())

    def test_usurpacion_clave(self):
        self.sign()
        self.run_ssl('genpkey', '-algorithm', 'Ed25519', '-out', str(self.private))
        self.run_ssl('pkey', '-in', str(self.private), '-pubout', '-out', str(self.key))
        self.rejected()

    def test_modificacion_despues_firma(self):
        self.sign()
        self.contract.write_text(self.contract.read_text() + ' ')
        with self.assertRaises(module.Rechazo): self.project()
        self.assertFalse(self.out.exists())

    def test_hash_fuente(self):
        self.c['source_sha256'] = '0' * 64
        self.rejected()

    def test_hash_codigo(self):
        self.c['code_sha256'] = '0' * 64
        self.rejected()

    def test_default_reject(self):
        self.c['approved'] = False
        self.rejected()

    def inventory(self):
        self.c['operation'] = 'inventory-only'
        self.c['human_signature']['scope'] = 'inventory-only'
        self.sign()
        with patch.object(zipfile.ZipFile, 'read', side_effect=AssertionError('leyó registros')):
            self.project()
        path = self.out / 'inventario.json'
        self.assertEqual(list(self.out.iterdir()), [path])
        self.run_ssl('pkeyutl', '-sign', '-inkey', str(self.private), '-rawin',
                     '-in', str(path), '-out', str(self.signature))
        return path

    def proposal(self):
        c = copy.deepcopy(self.c)
        c['table_proposals'] = [dict(c['members']['tabla.csv'], documented_filename='tabla.csv')]
        p = self.base / 'propuesta'; p.write_text(json.dumps(c))
        return p

    def test_firma_inventario_no_abre(self):
        self.inventory()
        self.assertNotIn(b'SECRETO-XYZ', (self.out / 'inventario.json').read_bytes())

    def test_compilador_y_etapa2(self):
        i = self.inventory()
        c = compiler.compila(str(self.proposal()), str(i), str(self.signature), str(self.key), self.trusted)
        self.assertFalse(c['approved'])
        self.assertEqual(c['archive_inventory'], ['tabla.csv'])
        self.assertEqual(list(c['members']), ['tabla.csv'])
        self.c = c; self.out = self.base / 'etapa2'
        self.c['human_signature']['scope'] = 'project'
        self.rejected()
        self.c['approved'] = True
        self.c['human_signature'] = {'reference': 'ACTO-SINTETICO', 'literal': 'FIRMA-SINTETICA',
          'body_sha256': '1' * 64, 'scope': 'project', 'verified_by_custodian': True, 'reservation_scopes': []}
        self.sign(); self.project()
        self.assertEqual((self.out / 'tabla.csv').read_text(), 'ID,EDAD\n1,33\n')

    def test_compilador_ambiguedad(self):
        self.archive({'a/tabla.csv': b'ID,EDAD\n1,33\n', 'b/tabla.csv': b'ID,EDAD\n2,34\n'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        i = self.inventory()
        with self.assertRaises(compiler.custodia.Rechazo):
            compiler.compila(str(self.proposal()), str(i), str(self.signature), str(self.key), self.trusted)

    def test_compilador_tabla_ausente(self):
        self.archive({'otra.csv': b'ID,EDAD\n1,33\n'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        i = self.inventory()
        with self.assertRaises(compiler.custodia.Rechazo):
            compiler.compila(str(self.proposal()), str(i), str(self.signature), str(self.key), self.trusted)

    def test_compilador_hash_erroneo(self):
        i = self.inventory()
        self.c['source_sha256'] = '0' * 64
        with self.assertRaises(compiler.custodia.Rechazo):
            compiler.compila(str(self.proposal()), str(i), str(self.signature), str(self.key), self.trusted)

    def test_compilador_firma_erronea(self):
        i = self.inventory()
        self.signature.write_bytes(b'x' * 64)
        with self.assertRaises(compiler.custodia.Rechazo):
            compiler.compila(str(self.proposal()), str(i), str(self.signature), str(self.key), self.trusted)

    def test_symlink_contrato(self):
        self.sign()
        link = self.base / 'contrato-link'; link.symlink_to(self.contract)
        with self.assertRaises(OSError): self.project(contract=str(link))
        self.assertFalse(self.out.exists())

    def test_symlink_clave(self):
        self.sign()
        link = self.base / 'clave-link'; link.symlink_to(self.key)
        with self.assertRaises(OSError): self.project(public_key=str(link))
        self.assertFalse(self.out.exists())

    def test_miembro_inesperado(self):
        self.archive({'tabla.csv': b'ID,EDAD\n1,33\n', 'reserva.csv': b'SECRETO-XYZ'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.rejected()

    def test_miembro_duplicado(self):
        with zipfile.ZipFile(self.src, 'a') as z: z.writestr('tabla.csv', b'ID,EDAD\n1,33\n')
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.rejected()

    def test_ruta_zip_traversal(self):
        self.archive({'tabla.csv': b'ID,EDAD\n1,33\n', '../escape': b'TRAMPA'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.c['archive_inventory'].append('../escape')
        self.rejected()

    def test_symlink_zip(self):
        with zipfile.ZipFile(self.src, 'a') as z:
            m = zipfile.ZipInfo('enlace'); m.create_system = 3; m.external_attr = 0o120777 << 16
            z.writestr(m, 'tabla.csv')
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.c['archive_inventory'].append('enlace')
        self.rejected()

    def test_columna_ausente(self):
        self.c['members']['tabla.csv']['columns'].append('FALTANTE')
        self.rejected()

    def test_header_duplicado(self):
        self.archive({'tabla.csv': b'ID,EDAD,EDAD\n1,33,34\n'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.rejected()

    def test_symlink_fuente(self):
        link = self.custody / 'link.zip'; link.symlink_to(self.src)
        self.rejected(source=str(link))

    def test_symlink_padre_fuente(self):
        link = self.base / 'alias'; link.symlink_to(self.custody, target_is_directory=True)
        self.rejected(source=str(link / self.src.name))

    def test_symlink_padre_salida(self):
        link = self.base / 'alias'; link.symlink_to(self.base, target_is_directory=True)
        self.rejected(output=str(link / 'nueva'))
        self.assertFalse((self.base / 'nueva').exists())

    def test_salida_existente(self):
        self.out.mkdir(); (self.out / 'testigo').write_text('íntegro')
        self.rejected()
        self.assertEqual((self.out / 'testigo').read_text(), 'íntegro')
        self.assertEqual(list(self.out.iterdir()), [self.out / 'testigo'])

    def test_symlink_salida(self):
        self.out.symlink_to(self.base, target_is_directory=True)
        self.rejected()

    def test_fuera_clon(self):
        self.rejected(output=str(REPO / 'rechazar-salida-p3'))

    def test_custodia_privada(self):
        self.custody.chmod(0o755)
        self.rejected()

    def test_real_identidades_separadas(self):
        self.c['mode'] = 'real'
        self.rejected()

    def test_salida_recibo_reservado(self):
        self.c['members']['tabla.csv']['output'] = 'recibo.json'
        self.rejected()

    def test_enut_coentrega_no_firma_generica(self):
        self.archive({'tabla.csv': b'LLAVEHOG,SEXO,EDAD,CUID_ESP_INT_HOG_CON_CP\n1,2,45,12\n'})
        self.c['source_sha256'] = module.sha(self.src.read_bytes())
        self.c['members']['tabla.csv']['columns'] = ['LLAVEHOG','SEXO','EDAD','CUID_ESP_INT_HOG_CON_CP']
        self.c['reservation_overrides'] = {module.RESERVA_ENUT: False}
        with patch.dict(module.SOURCE_REQUIRED_SCOPES, {self.c['source_sha256']: [module.RESERVA_ENUT]}):
            self.rejected()
            self.c['reservation_overrides'] = {}
            self.rejected()  # Cannot remove scope from source policy to bypass reserve.
            self.c['reservation_overrides'] = {module.RESERVA_ENUT: True}
            self.rejected()  # Boolean alone is insufficient; human scope required.
            self.c['human_signature']['reservation_scopes'] = [module.RESERVA_ENUT]
            self.sign(); self.project()
        self.assertEqual((self.out/'tabla.csv').read_text(),
                         'LLAVEHOG,SEXO,EDAD,CUID_ESP_INT_HOG_CON_CP\n1,2,45,12\n')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Custodia)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    evidence = {'mode': 'EXCLUSIVAMENTE-SINTETICO', 'tests_run': result.testsRun,
                'failures': len(result.failures), 'errors': len(result.errors),
                'code_sha256': module.sha(CODE.read_bytes()),
                'tests_sha256': module.sha(Path(__file__).read_bytes()),
                'result': 'PASS' if result.wasSuccessful() else 'FAIL'}
    (ROOT / 'impedimentos-lote2-p3-controles.json').write_text(json.dumps(evidence, indent=2) + '\n')
    raise SystemExit(not result.wasSuccessful())
