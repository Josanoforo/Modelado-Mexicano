#!/usr/bin/env python3
"""Cotejo posterior portable de allowlist, hashes y enlaces; no archiva raw."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2/p2'

def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def inventory(folder):
    receipt = json.loads((folder / 'recibo-entrada.json').read_text())
    manifest = json.loads((folder / 'entrada/manifiesto.json').read_text())
    expected = {'entrada/manifiesto.json': receipt['sha256_manifiesto']}
    expected.update({'entrada/' + name: digest for name, digest in manifest['archivos'].items()})
    expected.update({r['archivo']: r['sha256'] for r in receipt['insumos']})
    observed = {}
    for name in ('entrada', 'raw'):
        directory = folder / name
        assert not any(p.is_symlink() for p in (directory, *directory.parents)), 'Ancestro enlazado'
        for path in directory.rglob('*'):
            assert not path.is_symlink(), 'Enlace dentro entrada'
            if path.is_file():
                observed[str(path.relative_to(folder))] = sha(path)
    assert observed == expected, 'Allowlist o hash cambiado'
    return dict(directorio=str(folder), archivos=observed, enlaces=0,
                allowlist_exacta=True, sha256_recibo=sha(folder / 'recibo-entrada.json'))

if __name__ == '__main__':
    records = []
    for path in sorted((BASE / 'lanzamientos').glob('*.json')):
        record = json.loads(path.read_text())
        item = inventory(Path(record['directorio_aislado']))
        item.update(paquete=record['paquete'], intento=record['intento'],
                    lanzamiento_sha256=sha(path), entrada_registrada_utc=record['entrada_registrada_utc'])
        records.append(item)
    output = dict(cotejo_utc=datetime.now(timezone.utc).isoformat(),
                  naturaleza='COTEJO-POSTERIOR-NO-ATESTACION-PREVIA',
                  pre_entrega='materializaciones.json contiene los hashes y prueba de separación previos',
                  red='Sin monitor de egreso ni allowlist de hosts; no bloqueo de red', lanzamientos=records)
    (BASE / 'inventario-materializado-posterior.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print('ALLOWLIST-INTEGRA', len(records))
