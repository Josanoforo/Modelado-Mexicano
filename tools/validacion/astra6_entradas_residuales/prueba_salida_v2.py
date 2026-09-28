#!/usr/bin/env python3
"""Prueba sintética paquete→congelación→comparación con el adaptador exacto de #1221.

No abre microdatos, resultados ni referencias históricas. --adapter-dir contiene
adaptador.py y contrato-v2.json del mismo commit de #1221.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-entradas-residuales-lote2'
MANIFEST = BASE / 'p4/residuales-p4-manifestacion.json'
CASES = ('punto_sin_ic', 'ic_calculado', 'no_estimable')
ADAPTER_HEAD = 'd8ef9f56ef80ec1cd7867779489beb0ce7e4cfe9'
ADAPTER_SHA = '228d2897b0e2a85f3a64c107e4f0691ef26ff44086fbb87f9e03a92d14593fd2'
CONTRACT_SHA = '78a44e2ab1b8cb07c8374e3e3ef265fa827d0b3af291f0cf06089a4402c6f19d'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def load_adapter(directory):
    script = directory / 'adaptador.py'
    contract = directory / 'contrato-v2.json'
    assert script.is_file() and contract.is_file()
    spec = importlib.util.spec_from_file_location('adaptador_1221', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.CONTRACT.resolve() == contract.resolve()
    return module


def synthetic_row(schema, case):
    base = {'llave': schema['llave'], 'unidad': schema['unidad']}
    if case == 'punto_sin_ic':
        return base | {'estado': 'RECONSTRUIDO', 'punto': '0.5', 'estado_ic': 'SIN-IC'}
    if case == 'ic_calculado':
        return base | {'estado': 'RECONSTRUIDO', 'punto': '0.5',
                       'estado_ic': 'CALCULADO', 'ic95_inf': '0.4', 'ic95_sup': '0.6'}
    return base | {'estado': 'NO-RECALCULABLE-DESDE-SPEC',
                   'motivo': 'SINTETICO-DISENO-NO-IDENTIFICADO', 'estado_ic': 'SIN-IC'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--adapter-dir', type=Path)
    source.add_argument('--adapter-ref', help='Ref local cuyo commit debe ser HEAD exacto de #1221')
    args = parser.parse_args()
    manifests = json.loads(MANIFEST.read_text())
    assert len(manifests) == 4
    with tempfile.TemporaryDirectory(prefix='residuales-salida-v2-') as temp:
        root = Path(temp)
        adapter_dir = args.adapter_dir.resolve() if args.adapter_dir else root / 'adaptador-1221'
        if args.adapter_ref:
            head = subprocess.check_output(['git', 'rev-parse', args.adapter_ref], cwd=ROOT,
                                           text=True).strip()
            assert head == ADAPTER_HEAD, ('HEAD #1221 cambió; revisar contrato antes de probar', head)
            adapter_dir.mkdir()
            for name in ('adaptador.py', 'contrato-v2.json'):
                data = subprocess.check_output(['git', 'show',
                                                f'{head}:tools/validacion/astra6_aislamiento_v2/{name}'],
                                               cwd=ROOT)
                (adapter_dir / name).write_bytes(data)
        adapter_sha = digest(adapter_dir / 'adaptador.py')
        contract_sha = digest(adapter_dir / 'contrato-v2.json')
        assert (adapter_sha, contract_sha) == (ADAPTER_SHA, CONTRACT_SHA)
        adapter = load_adapter(adapter_dir)
        report = {'tipo': 'SINTETICO-NO-CIEGO', 'pr_1221_head': ADAPTER_HEAD,
                  'adaptador_sha256': adapter_sha, 'contrato_sha256': contract_sha,
                  'escenarios': []}
        for item in manifests:
            package = ROOT / item['archivo']
            assert digest(package) == item['sha256']
            with tarfile.open(package) as tar:
                members = tar.getnames()
                assert 'esquema-salida-v2.md' in members and 'esquema-salida.md' not in members
                rows = list(csv.DictReader(io.TextIOWrapper(tar.extractfile('esquema-identidades.tsv')),
                                           delimiter='\t'))
            assert len(rows) == item['identidades']
            assert len({row['llave'] for row in rows}) == len(rows)
            assert all(row['llave'] and row['unidad'] and row['entrada_id'] for row in rows)
            identity = {'paquete': item['sucesor'], 'version_entrada': 'residuales-documentales-v2',
                        'sha256_entrada': item['sha256']}
            for case in CASES:
                directory = root / (item['instrumento'] + '-' + case)
                directory.mkdir()
                original = directory / 'original.json'
                document = {'version': 2, 'identidad': identity,
                            'filas': [synthetic_row(row, case) for row in rows]}
                save(original, document)
                normalized = adapter.normalize(adapter.read_json(original))
                assert len(normalized['filas']) == len(rows)
                assert all(a['llave'] == b['llave'] and a['unidad'] == b['unidad']
                           for a, b in zip(normalized['filas'], rows))
                tolerance = directory / 'tolerancia-sintetica.json'
                save(tolerance, {'abs': '0', 'rel': '0'})
                frozen = directory / 'congelado'
                seal = adapter.freeze(frozen, original, [Path(__file__)], package, tolerance)
                seal_sha = digest(seal)  # Ancla exterior al directorio congelado.
                adapter.verify_freeze(frozen, seal_sha)
                reference = directory / 'referencia-sintetica.json'
                save(reference, document)  # Se crea solo después de congelar/verificar.
                compared = adapter.compare(frozen, seal_sha, reference, digest(reference))
                expected = ('NO-RECALCULABLE-DESDE-SPEC' if case == 'no_estimable' else 'COINCIDE')
                assert len(compared['resultados']) == len(rows)
                assert all(result['estado'] == expected for result in compared['resultados'])
                assert compared['identidad'] == identity
                report['escenarios'].append({'cohorte': item['instrumento'], 'caso': case,
                                             'filas': len(rows),
                                             'estado': expected, 'congelacion_verificada': True,
                                             'comparacion_verificada': True})
            bad = {'version': 2, 'identidad': identity,
                   'filas': [synthetic_row(rows[0], 'ic_calculado') | {'ic_lo': '0.4'}]}
            try:
                adapter.normalize(bad)
            except ValueError:
                pass
            else:
                raise AssertionError('El adaptador aceptó un campo IC auxiliar en la fila')
    assert len(report['escenarios']) == 12
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
