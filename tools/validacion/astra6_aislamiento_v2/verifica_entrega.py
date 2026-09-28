#!/usr/bin/env python3
"""Verifica objetos entregados y circuito conservado contra anclas externas."""
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile

import adaptador

BASE = Path(__file__).resolve().parents[3]
PRODUCT = BASE / 'forense/validacion-independiente/catalogo-1-aislamiento-v2'


def verify():
    hashes = json.loads((PRODUCT / 'aislamiento-v2-objetos-sha256.json').read_text())
    for relative, expected in hashes['objetos'].items():
        actual = hashlib.sha256((BASE / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('Objeto alterado: ' + relative)
    evidence = json.loads((PRODUCT / 'aislamiento-v2-evidencia-circuito.json').read_text())
    with tempfile.TemporaryDirectory(prefix='astra6-verifica-entrega-') as directory:
        with tarfile.open(PRODUCT / 'aislamiento-v2-circuito-congelado.tar.gz') as archive:
            archive.extractall(directory, filter='data')
        artifact = Path(directory) / 'evidencia-sintetica-portable/congelado'
        adaptador.verify_freeze(artifact, evidence['manifest_sha256'])
    return {'objetos': len(hashes['objetos']), 'integridad': 'PASS',
            'circuito_portable': 'PASS', 'ceguera': 'NO-ACREDITADA-EN-ESTE-ENTORNO'}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))
