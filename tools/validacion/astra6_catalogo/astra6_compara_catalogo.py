#!/usr/bin/env python3
"""Comparación posterior a congelación; no modifica registros del proyecto."""
import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1'


def load_tsv(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def compare(reconstruction, receipt, digest, output):
    reconstruction = Path(reconstruction).resolve()
    # El SHA debe haber llegado del responsable ANTES de abrir el esperado.
    assert len(digest) == 64 and all(c in '0123456789abcdef' for c in digest)
    assert hashlib.sha256(reconstruction.read_bytes()).hexdigest() == digest
    received = json.loads(Path(receipt).read_text())
    assert received['reconstruccion_sha256'] == digest
    assert received['congelado_antes_de_revelacion'] is True
    assert received['commit_reconstruccion'], 'Se requiere commit inmutable del validador'
    # Verifica que el archivo pertenece a ese commit, no solo una afirmación textual.
    checkout = Path(received['checkout_reconstruccion']).resolve()
    relative = reconstruction.relative_to(checkout)
    committed = subprocess.check_output(['git', 'show', f"{received['commit_reconstruccion']}:{relative}"], cwd=checkout)
    assert hashlib.sha256(committed).hexdigest() == digest
    lot = next(x for x in json.loads((BASE / 'lotes.json').read_text()) if x['paquete'] == received['paquete'])
    assert received['paquete_sha256'] == lot['sha256']
    assert lot['estado_preparacion'] == 'DISPONIBLE'
    original = load_tsv(BASE / 'preparacion/catalogo-al-corte.tsv.gz')
    expected = {r['llave']: r for r in original if r['calc'] == lot['calc']}
    own_rows = load_tsv(reconstruction)
    own = {r['llave']: r for r in own_rows}
    assert len(own) == len(own_rows), 'Llaves repetidas'
    assert set(own) == set(expected), 'Cobertura debe ser exacta, sin recortar discrepancias'
    archive = BASE / 'paquetes' / received['paquete'] / lot['archivo']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == lot['sha256_contenedor']
    with tarfile.open(archive, 'r:gz') as tar:
        tolerance = json.loads(tar.extractfile('tolerancia.json').read())
    absolute = tolerance['abs']
    relative_tol = tolerance.get('rel', 0)
    assert isinstance(absolute, (int, float)) and absolute >= 0
    results = []
    allowed = {'NO-EVALUADO', 'NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO'}
    for key, reference in expected.items():
        row = own[key]
        status = row.get('estado', '')
        if status in allowed:
            results.append({'llave': key, 'estado': status, 'efecto': 'NO-DETERMINADO'})
            continue
        assert status == 'RECONSTRUIDO', 'El validador no adjudica COINCIDE antes de revelación'
        deltas = {}
        for field in ['punto', 'ic95_inf', 'ic95_sup']:
            actual, target = row.get(field, ''), reference[field]
            if not target:
                assert not actual, f'{key}: IC no declarado en catálogo'
                continue
            a, b = float(actual), float(target)
            assert math.isfinite(a) and math.isfinite(b)
            deltas[field] = {'delta': a - b, 'dentro': math.isclose(a, b, abs_tol=absolute, rel_tol=relative_tol)}
        match = all(x['dentro'] for x in deltas.values())
        results.append({'llave': key, 'estado': 'COINCIDE' if match else 'DISCREPA',
                        'efecto': 'ninguno material' if match else ('cifra' if not deltas['punto']['dentro'] else 'incertidumbre'),
                        'campos': deltas})
    destination = Path(output)
    assert not destination.exists(), 'No sobrescribe una comparación previa'
    destination.write_text(json.dumps({'recibo': received, 'tolerancia': tolerance,
                                      'alcance': 'Coincidencia numérica; no acredita validez del estimando ni adopción.',
                                      'resultados': results}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reconstruccion', required=True)
    parser.add_argument('--recibo', required=True)
    parser.add_argument('--sha256-recibido', required=True)
    parser.add_argument('--salida', required=True)
    args = parser.parse_args()
    try:
        compare(args.reconstruccion, args.recibo, args.sha256_recibido, args.salida)
    except (AssertionError, ValueError, KeyError, OSError, StopIteration, subprocess.CalledProcessError) as e:
        sys.exit(f'COMPARACION-RECHAZADA: {e}')
