#!/usr/bin/env python3
"""Transporte sucesor v1: compara únicamente después de congelación verificada."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
P1 = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2/p1'
CONTRACT = P1 / 'contrato-adaptador-v1.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def validate_receipt(received, entry, digest):
    for field in ['paquete', 'paquete_original', 'version_entrada', 'sha256_contenedor', 'sha256_manifiesto']:
        require(received.get(field) == entry[field], 'Identidad/hash/version incorrecta: ' + field)
    require(received.get('reconstruccion_sha256') == digest, 'Hash reconstruccion incorrecto')
    require(received.get('congelado_antes_de_revelacion') is True, 'Salida sin congelacion')
    require(bool(received.get('commit_reconstruccion')), 'Falta commit congelado')


def exact_keys(own_rows, entry):
    own = {r['llave']: r for r in own_rows}
    require(len(own) == len(own_rows), 'Llaves repetidas')
    require(set(own) == {r['llave_sucesor'] for r in entry['correspondencia']}, 'Llaves ausentes o extras')
    return own


def compare(reconstruction, receipt, digest, output):
    freeze = json.loads((P1 / 'congelacion-adaptador-v1.json').read_text())
    require(sha(__file__) == freeze['adaptador_sha256'], 'Adaptador no congelado')
    require(sha(CONTRACT) == freeze['contrato_sha256'], 'Contrato no congelado')
    contract = json.loads(CONTRACT.read_text())
    require(contract['version_adaptador'] == 1, 'Version de adaptador desconocida')
    received = json.loads(Path(receipt).read_text())
    candidates = [r for r in contract['entradas'] if r['paquete'] == received.get('paquete')]
    require(len(candidates) == 1, 'Paquete/version desconocida')
    entry = candidates[0]
    validate_receipt(received, entry, digest)
    reconstruction = Path(reconstruction).resolve()
    require(sha(reconstruction) == digest, 'Reconstruccion alterada')
    checkout = Path(received['checkout_reconstruccion']).resolve()
    relative = reconstruction.relative_to(checkout)
    committed = subprocess.check_output(['git', 'show', f"{received['commit_reconstruccion']}:{relative}"], cwd=checkout)
    require(hashlib.sha256(committed).hexdigest() == digest, 'Archivo no pertenece al commit congelado')
    own = exact_keys(rows(reconstruction), entry)
    archive = ROOT / entry['ruta_tar']
    require(sha(archive) == entry['sha256_contenedor'], 'Tar alterado')
    with tarfile.open(archive, 'r:gz') as tar:
        manifest = tar.extractfile('manifiesto.json').read()
        tolerance_bytes = tar.extractfile('tolerancia.json').read()
    require(hashlib.sha256(manifest).hexdigest() == entry['sha256_manifiesto'], 'Manifiesto alterado')
    require(hashlib.sha256(tolerance_bytes).hexdigest() == entry['tolerancia_sha256'], 'Tolerancia alterada')
    tolerance = json.loads(tolerance_bytes)
    expected_path = ROOT / contract['esperados_ruta']
    require(sha(expected_path) == contract['esperados_sha256'], 'Esperados alterados')
    # La primera lectura de valores ocurre despues de todas las guardias anteriores.
    selected = [r for r in rows(expected_path) if r['calc'] == entry['calc']]
    expected = {r['llave']: r for r in selected}
    require(len(expected) == len(selected), 'Llaves esperadas repetidas')
    require(set(expected) == {r['llave_original'] for r in entry['correspondencia']}, 'Correspondencia incompleta')
    results = []
    allowed = {'NO-EVALUADO', 'NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO'}
    for mapping in entry['correspondencia']:
        key = mapping['llave_sucesor']
        reference, row = expected[mapping['llave_original']], own[key]
        status = row.get('estado', '')
        if status in allowed:
            results.append({'llave': key, 'estado': status, 'efecto': 'NO-DETERMINADO'})
            continue
        require(status == 'RECONSTRUIDO', 'Estado no autorizado antes de revelacion')
        deltas = {}
        for field in ['punto', 'ic95_inf', 'ic95_sup']:
            actual, target = row.get(field, ''), reference[field]
            if not target:
                require(not actual, key + ': campo no declarado en catalogo')
                continue
            a, b = float(actual), float(target)
            require(math.isfinite(a) and math.isfinite(b), 'Numero no finito')
            deltas[field] = {'delta': a-b, 'dentro': math.isclose(a, b, abs_tol=tolerance['abs'], rel_tol=tolerance.get('rel', 0))}
        match = all(x['dentro'] for x in deltas.values())
        results.append({'llave': key, 'estado': 'COINCIDE' if match else 'DISCREPA',
                        'efecto': 'ninguno material' if match else ('cifra' if not deltas.get('punto', {}).get('dentro', True) else 'incertidumbre'),
                        'campos': deltas})
    with Path(output).open('x') as handle:
        json.dump({'recibo': received, 'tolerancia': tolerance, 'contrato_sha256': freeze['contrato_sha256'],
                   'alcance': 'Coincidencia numerica; publicabilidad, defecto conceptual y adopcion requieren adjudicacion separada.',
                   'resultados': results}, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reconstruccion', required=True)
    parser.add_argument('--recibo', required=True)
    parser.add_argument('--sha256-recibido', required=True)
    parser.add_argument('--salida', required=True)
    args = parser.parse_args()
    compare(args.reconstruccion, args.recibo, args.sha256_recibido, args.salida)
