"""Synthetic end-to-end checks for the v3 isolated executor.

The data, code, fake secret, reference and expected values here are synthetic.
The candidate process itself writes the boundary canaries; host-side assertions
never stand in for a successful isolated run.
"""

import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime.py"
CONTRACT = ROOT / "contract.py"
CSV = b"group,value,weight\nA,1,1\nA,0,1\nA,1,2\nB,0,1\n"
RECONSTRUCTOR = r'''import csv
import hashlib
import json
import os
from pathlib import Path
import socket
import numpy as np

source = Path('/entrada/entrada.csv')
rows = list(csv.DictReader(source.open()))
values = np.array([float(r['value']) for r in rows if r['group'] == 'A'])
weights = np.array([float(r['weight']) for r in rows if r['group'] == 'A'])
point = float(np.average(values, weights=weights))
# This CI is a synthetic demonstration of a NumPy runtime, not a survey CI.
standard_error = float(np.std(values, ddof=1) / np.sqrt(values.size))
lower, upper = point - 1.96 * standard_error, point + 1.96 * standard_error
canaries = {'allowed_read': source.read_bytes().startswith(b'group,value,weight')}
try:
    source.write_bytes(b'CHANGED')
    canaries['input_write_denied'] = False
except OSError:
    canaries['input_write_denied'] = True
try:
    Path('OUTSIDE_SECRET_PATH').read_bytes()
    canaries['outside_secret_denied'] = False
except OSError:
    canaries['outside_secret_denied'] = True
for name, kind, address in (
    ('tcp_denied', socket.SOCK_STREAM, ('127.0.0.1', HOST_TCP_PORT)),
    ('udp_denied', socket.SOCK_DGRAM, ('192.0.2.1', 9)),
):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, kind)
        sock.settimeout(0.2)
        if kind == socket.SOCK_STREAM:
            sock.connect(address)
        else:
            sock.sendto(b'synthetic', address)
        canaries[name] = False
    except OSError:
        canaries[name] = True
    finally:
        if sock is not None:
            sock.close()
try:
    Path('/salida/no-autorizado.txt').write_text('must not export')
    canaries['extra_output_written'] = True
except OSError:
    canaries['extra_output_written'] = False
identity = {'paquete': 'SINTETICO-V3', 'version_entrada': '1',
            'sha256_entrada': hashlib.sha256(source.read_bytes()).hexdigest()}
result = {'version': 3, 'identidad': identity, 'filas': [
    {'llave': 'proporcion_A', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
     'punto': str(point), 'estado_ic': 'CALCULADO',
     'ic95_inf': str(lower), 'ic95_sup': str(upper)},
    {'llave': 'dominio_vacio', 'unidad': 'proporcion', 'estado': 'DENOMINADOR-CERO',
     'motivo': 'El dominio Z tiene cero observaciones en el sintético'},
    {'llave': 'punto_sin_ic', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
     'punto': str(point), 'estado_ic': 'NO-IDENTIFICADA',
     'motivo_ic': 'No hay diseño de réplicas en el sintético'},
]}
out = Path('/salida')
(out / 'resultado.json').write_text(json.dumps(result, sort_keys=True) + '\n')
(out / 'canarios.json').write_text(json.dumps(canaries, sort_keys=True) + '\n')
(out / 'diagnostico.json').write_text(json.dumps({'numpy': np.__version__,
    'n': len(rows), 'point': point}, sort_keys=True) + '\n')
(out / 'codigo.py').write_bytes(Path('/entrada/reconstructor.py').read_bytes())
with (out / 'auxiliar.tsv').open('w') as stream:
    stream.write('id\tvalor\n')
    for i in range(120000):
        stream.write(f'{i}\t{point}\n')
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def anchor_export(runtime, export, manifest_path, identity, anchor_path):
    manifest = json.loads(Path(manifest_path).read_text())
    expected = digest(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode())
    return runtime.freeze_export(export, anchor_path, package_identity=identity,
                                 expected_input_manifest_sha256=expected)


def fixture(base, extra_members=(), outside_secret=None, host_tcp_port=9):
    """A valid nonempty allowlist accompanies every TAR, including attacks."""
    script = RECONSTRUCTOR.replace('OUTSIDE_SECRET_PATH',
        str(outside_secret or base / 'secreto-ficticio-externo')).replace(
        'HOST_TCP_PORT', str(host_tcp_port))
    source = {'reconstructor.py': script.encode(), 'entrada.csv': CSV}
    archive = base / 'input.tar'
    with tarfile.open(archive, 'w') as tar:
        for name, data in source.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            tar.addfile(member, io.BytesIO(data))
        for name, kind in extra_members:
            member = tarfile.TarInfo(name)
            if kind == 'symlink':
                member.type = tarfile.SYMTYPE
                member.linkname = '../outside'
                tar.addfile(member)
            else:
                member.size = 1
                tar.addfile(member, io.BytesIO(b'x'))
    manifest = {'version': 1, 'entrypoint': 'reconstructor.py',
                'input_files': [{'path': name, 'sha256': digest(data)}
                                for name, data in source.items()],
                'output_files': [{'path': name, 'max_bytes': limit} for name, limit in (
                    ('resultado.json', 1048576), ('canarios.json', 4096),
                    ('diagnostico.json', 4096), ('codigo.py', 65536),
                    ('auxiliar.tsv', 4194304))],
                'max_total_output_bytes': 6291456}
    manifest_path = base / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, sort_keys=True) + '\n')
    return archive, manifest_path


def cli(*args):
    return subprocess.run([sys.executable, str(RUNTIME), *map(str, args)],
                          text=True, capture_output=True, timeout=90)


def write_evidence(target):
    """Run the synthetic candidate and preserve compact, checkable evidence."""
    spec = importlib.util.spec_from_file_location('runtime_v3_evidence', RUNTIME)
    runtime = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runtime)
    with tempfile.TemporaryDirectory(prefix='astra6-v3-evidence-') as temp:
        base = Path(temp)
        secret = base / 'secreto-ficticio-externo'
        secret.write_text('SYNTHETIC-SECRET')
        archive, manifest = fixture(base, outside_secret=secret)
        build_args = ('build', '--archive', archive, '--manifest', manifest,
                      '--output', base / 'bundle')
        built = cli(*build_args)
        if built.returncode:
            raise RuntimeError(built.stderr)
        run_args = ('run', '--bundle', base / 'bundle', '--output', base / 'export',
                    '--backend', 'namespace')
        launched = cli(*run_args)
        if launched.returncode:
            raise RuntimeError(launched.stderr)
        export_dir = base / 'export'
        output = json.loads((export_dir / 'resultado.json').read_text())
        anchor_path = base / 'export-anchor.json'
        anchor_export(runtime, export_dir, manifest, output['identidad'], anchor_path)
        runtime.verify_export(export_dir, anchor_path)
        export_manifest = json.loads((export_dir / 'export-manifest.json').read_text())
        canaries = json.loads((export_dir / 'canarios.json').read_text())
        if not all(canaries.values()):
            raise AssertionError(canaries)
        spec = importlib.util.spec_from_file_location('contract_v3_evidence', CONTRACT)
        contract = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(contract)
        contract.validate(output)
        # Expected values come from the synthetic fixture, independently of
        # the candidate's output. The reference is written only after freeze.
        standard_error = math.sqrt(1 / 3) / math.sqrt(3)
        reference = {'version': 3, 'identidad': output['identidad'], 'filas': [
            {'llave': 'proporcion_A', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
             'punto': '0.75', 'estado_ic': 'CALCULADO',
             'ic95_inf': str(0.75 - 1.96 * standard_error),
             'ic95_sup': str(0.75 + 1.96 * standard_error)},
            {'llave': 'dominio_vacio', 'unidad': 'proporcion', 'estado': 'DENOMINADOR-CERO',
             'motivo': 'Dominio vacío bajo spec suficiente'},
            {'llave': 'punto_sin_ic', 'unidad': 'proporcion', 'estado': 'RECONSTRUIDO',
             'punto': '0.75', 'estado_ic': 'NO-IDENTIFICADA',
             'motivo_ic': 'Diseño de réplicas no identificado'},
        ]}
        tolerance = base / 'tolerancia.json'
        tolerance.write_text('{"abs":"1e-12","rel":"0"}\n')
        if str(ROOT.parents[2]) not in sys.path:
            sys.path.insert(0, str(ROOT.parents[2]))
        from tools.validacion.astra6_ejecutor_v3 import compare_v3
        frozen_sha = compare_v3.freeze(export_dir, anchor_path, tolerance, base / 'congelado')
        reference_bytes = (json.dumps(reference, sort_keys=True) + '\n').encode()
        reference_path = base / 'referencia.json'
        reference_path.write_bytes(reference_bytes)
        comparison = compare_v3.compare(base / 'congelado', frozen_sha,
                                        reference_path, digest(reference_bytes))
        if comparison['estado'] != 'COINCIDE' or any(
                not all(item['dentro'] for item in row['campos'].values())
                for row in comparison['resultados']):
            raise AssertionError('full synthetic comparison differs')
        if (export_dir / 'no-autorizado.txt').exists():
            raise AssertionError('unlisted output was exported')
        original = export_dir / 'resultado.json'
        saved = original.read_bytes()
        original.chmod(0o644)
        original.write_bytes(saved + b'altered')
        tamper_rejected = False
        try:
            runtime.verify_export(export_dir, anchor_path)
        except (ValueError, RuntimeError):
            tamper_rejected = True
        finally:
            original.write_bytes(saved)
            original.chmod(0o444)
        if not tamper_rejected:
            raise AssertionError('post-seal alteration accepted')
        runtime.verify_export(export_dir, anchor_path)
        payload = io.BytesIO()
        with tarfile.open(fileobj=payload, mode='w') as tar:
            for row in export_manifest['files']:
                data = (export_dir / row['path']).read_bytes()
                member = tarfile.TarInfo(row['path'])
                member.size = len(data)
                tar.addfile(member, io.BytesIO(data))
        truncated_rejected = False
        try:
            runtime._extract(payload.getvalue()[:513], json.loads(manifest.read_text()),
                             base / 'truncated')
        except (ValueError, RuntimeError, tarfile.TarError, EOFError):
            truncated_rejected = True
        if not truncated_rejected:
            raise AssertionError('truncated output TAR accepted')
        evidence = {
            'tipo': 'EJECUTADO-SINTETICO',
            'run_id': digest(archive.read_bytes() + manifest.read_bytes())[:16],
            'contrato_sha256': digest(CONTRACT.read_bytes()),
            'runtime_sha256': digest(RUNTIME.read_bytes()),
            'input_tar_sha256': digest(archive.read_bytes()),
            'input_manifest_sha256': digest(manifest.read_bytes()),
            'backend': 'namespace',
            'comandos': [
                'python3 tools/validacion/astra6_ejecutor_v3/runtime.py build --archive <synthetic.tar> --manifest <synthetic.json> --output <bundle>',
                'python3 tools/validacion/astra6_ejecutor_v3/runtime.py run --bundle <bundle> --output <export> --backend namespace',
                'python3 tools/validacion/astra6_ejecutor_v3/test_e2e.py --evidence <target>',
            ],
            'export_verificado_antes_de_referencia': True,
            'resultado_original_validado_con_contrato_v3': True,
            'referencia_sintetica_sha256': digest(reference_bytes),
            'comparacion_referencia_sintetica': 'COINCIDE',
            'congelacion_sha256': frozen_sha,
            'ancla_exportacion_sha256': digest(anchor_path.read_bytes()),
            'comparacion_componentes': comparison['resultados'],
            'alteracion_posterior_al_sello_rechazada': tamper_rejected,
            'tar_salida_truncado_rechazado': truncated_rejected,
            'canarios_desde_proceso_aislado': canaries,
            'archivos_exportados': export_manifest['files'],
            'export_manifest_sha256': digest((export_dir / 'export-manifest.json').read_bytes()),
            'resultado': [{key: row[key] for key in
                           ('llave', 'estado', 'estado_ic', 'punto') if key in row}
                          for row in output['filas']],
            'auxiliar_bytes': (export_dir / 'auxiliar.tsv').stat().st_size,
            'archivo_no_listado_exportado': False,
            'version_numpy': json.loads((export_dir / 'diagnostico.json').read_text())['numpy'],
        }
    destination = Path(target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(evidence, indent=2, ensure_ascii=False,
                                      sort_keys=True) + '\n')
    return evidence


class ExecutorE2E(unittest.TestCase):
    def test_export_integrity_tamper_and_truncation(self):
        spec = importlib.util.spec_from_file_location('runtime_v3', RUNTIME)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix='astra6-v3-export-') as temp:
            base = Path(temp)
            _, manifest_path = fixture(base)
            manifest = json.loads(manifest_path.read_text())
            files = {item['path']: (item['path'] + '\n').encode()
                     for item in manifest['output_files']}

            def archive(selected):
                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode='w') as tar:
                    for name, data in selected.items():
                        member = tarfile.TarInfo(name)
                        member.size = len(data)
                        tar.addfile(member, io.BytesIO(data))
                return buffer.getvalue()

            good = archive(files)
            module._extract(good, manifest, base / 'complete')
            self.assertTrue(module.verify_export_consistency(base / 'complete'))
            target = base / 'complete' / 'resultado.json'
            target.chmod(0o644)
            target.write_bytes(target.read_bytes() + b'altered')
            with self.assertRaises((ValueError, RuntimeError)):
                module.verify_export_consistency(base / 'complete')
            with self.assertRaises((ValueError, RuntimeError, tarfile.TarError, EOFError)):
                module._extract(archive({'resultado.json': files['resultado.json']}),
                                manifest, base / 'missing')
            with self.assertRaises((ValueError, RuntimeError, tarfile.TarError, EOFError)):
                module._extract(good[:513], manifest, base / 'truncated')

    def test_v2_cohort_formats_map_to_v3_without_changing_numbers(self):
        spec = importlib.util.spec_from_file_location('contract_v3', CONTRACT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        forms = {
            'ENBIARE': ('estimacion', 'ic95_inf', 'ic95_sup'),
            'ENCODAT': ('valor', 'ic95_inferior', 'ic95_superior'),
            'ENCUCI': ('estimacion', 'ic95_inf', 'ic95_sup'),
            'ENIGH': ('valor', 'ic_inferior', 'ic_superior'),
        }
        for cohort, aliases in forms.items():
            with self.subTest(cohort=cohort):
                row = {'llave': cohort, 'unidad': 'proporcion',
                       'estado': 'RECONSTRUIDO', 'estado_ic': 'CALCULADO',
                       aliases[0]: '0.625', aliases[1]: '0.500',
                       aliases[2]: '0.750'}
                v2 = {'version': 2, 'identidad': {'paquete': 'SINTETICO-' + cohort,
                    'version_entrada': '1', 'sha256_entrada': '0' * 64},
                    'filas': [row]}
                v3 = module.from_v2(v2)
                self.assertEqual(v3['version'], 3)
                got = v3['filas'][0]
                self.assertEqual((got['punto'], got['ic95_inf'], got['ic95_sup']),
                                 ('0.625', '0.500', '0.750'))
                self.assertEqual(v3['mapa_campos'][0]['campos']['punto'], aliases[0])

    def test_valid_tar_and_attacks_with_nonempty_allowlist(self):
        with tempfile.TemporaryDirectory(prefix='astra6-v3-test-') as temp:
            base = Path(temp)
            archive, manifest = fixture(base)
            built = cli('build', '--archive', archive, '--manifest', manifest,
                        '--output', base / 'bundle')
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertTrue((base / 'bundle' / 'input' / 'entrada.csv').is_file())
        for case, members in (
            ('traversal', [('../escape', 'file')]),
            ('symlink', [('evil', 'symlink')]),
            ('duplicate', [('entrada.csv', 'file')]),
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory(prefix='astra6-v3-tar-') as temp:
                base = Path(temp)
                archive, manifest = fixture(base, members)
                rejected = cli('build', '--archive', archive, '--manifest', manifest,
                               '--output', base / 'bundle')
                self.assertNotEqual(rejected.returncode, 0, case)
                self.assertFalse((base / 'bundle' / 'input').exists(), case)

    def test_namespace_science_boundary_and_export(self):
        with tempfile.TemporaryDirectory(prefix='astra6-v3-e2e-') as temp:
            base = Path(temp)
            spec_runtime = importlib.util.spec_from_file_location('runtime_v3_e2e', RUNTIME)
            runtime = importlib.util.module_from_spec(spec_runtime)
            spec_runtime.loader.exec_module(runtime)
            secret = base / 'secreto-ficticio-externo'
            secret.write_text('SYNTHETIC-SECRET')
            archive, manifest = fixture(base, outside_secret=secret)
            built = cli('build', '--archive', archive, '--manifest', manifest,
                        '--output', base / 'bundle')
            self.assertEqual(built.returncode, 0, built.stderr)
            result = cli('run', '--bundle', base / 'bundle', '--output', base / 'export',
                         '--backend', 'namespace')
            self.assertEqual(result.returncode, 0, result.stderr)
            export = base / 'export'
            canaries = json.loads((export / 'canarios.json').read_text())
            self.assertTrue(all(canaries.values()), canaries)
            self.assertEqual(set(canaries), {'allowed_read', 'input_write_denied',
                'outside_secret_denied', 'tcp_denied', 'udp_denied',
                'extra_output_written'})
            output = json.loads((export / 'resultado.json').read_text())
            anchor = base / 'export-anchor.json'
            anchor_export(runtime, export, manifest, output['identidad'], anchor)
            self.assertTrue(runtime.verify_export(export, anchor))
            spec = importlib.util.spec_from_file_location('contract_v3_e2e', CONTRACT)
            contract = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(contract)
            contract.validate(output)
            self.assertEqual(output['version'], 3)
            self.assertEqual({r['llave'] for r in output['filas']},
                             {'proporcion_A', 'dominio_vacio', 'punto_sin_ic'})
            self.assertAlmostEqual(float(output['filas'][0]['punto']), 0.75)
            self.assertGreater((export / 'auxiliar.tsv').stat().st_size, 1048576)
            self.assertEqual((export / 'codigo.py').read_bytes(),
                             (base / 'bundle' / 'input' / 'reconstructor.py').read_bytes())
            self.assertFalse((export / 'no-autorizado.txt').exists())
            index = json.loads((export / 'export-manifest.json').read_text())
            self.assertTrue(index)


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--evidence':
        print(json.dumps({'run_id': write_evidence(sys.argv[2])['run_id']},
                         sort_keys=True))
    else:
        unittest.main()
