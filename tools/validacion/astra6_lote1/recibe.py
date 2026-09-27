#!/usr/bin/env python3
"""Recibe una salida congelada; registra su hash antes de comparar."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receive(package, checkout, reconstruction, includes):
    checkout = checkout.resolve()
    launch = json.loads((BASE / 'lanzamientos' / (package + '--lanzamiento.json')).read_text())
    assert launch['estado'] in {'TERMINADO', 'REVISAR-SALIDA'} and launch['session_id']
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    relative = str(reconstruction)
    content = subprocess.check_output(['git', 'show', commit + ':' + relative], cwd=checkout)
    assert content == (checkout / reconstruction).read_bytes(), 'Salida no coincide con commit'
    digest = hashlib.sha256(content).hexdigest()
    destination = BASE / 'reconstrucciones' / package
    assert not destination.exists(), 'No sobrescribe una entrega'
    destination.mkdir(parents=True)
    fields = ['paquete', 'paquete_sha256', 'sha256_contenedor', 'entrada_registrada_utc',
              'separacion_efectiva', 'session_id', 'directorio_aislado', 'prueba_separacion']
    entry = {key: launch[key] for key in fields}
    entry.update(reconstruccion_sha256=digest, commit_reconstruccion=commit,
                 checkout_reconstruccion=str(checkout), ruta_reconstruccion_commit=relative,
                 congelacion_recibida_utc=now(), estado='CONGELADO-SIN-REVELAR')
    receipt = dict(entry, congelado_antes_de_revelacion=True)
    (destination / 'recibo.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    (destination / 'reconstruccion.tsv').write_bytes(content)
    inventory = {}
    for name in includes:
        source = Path(name)
        assert not source.is_absolute() and '..' not in source.parts
        assert not {'raw', 'documentacion', '.git'} & set(source.parts)
        assert source.suffix in {'.py', '.sh', '.md', '.tsv', '.json'}, 'Allowlist de artefactos agregados'
        target = destination / 'artefactos' / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(['git', 'show', commit + ':' + name], cwd=checkout))
        inventory[name] = sha(target)
    (destination / 'artefactos-sha256.json').write_text(json.dumps(inventory, indent=2) + '\n')
    proof = destination / 'prueba-commit.json'
    command = ['python3', str(ROOT / 'tools/validacion/astra6_lote1/prueba_commit.py'), 'generar',
               '--checkout', str(checkout), '--commit', commit, '--ruta', relative]
    for name in includes:
        if Path(name).suffix != '.md' and name != relative:
            command.extend(['--ruta', name])
    command.extend(['--salida', str(proof)])
    subprocess.run(command, check=True)
    entry.update(reconstruccion=str((destination / 'reconstruccion.tsv').relative_to(BASE)),
                 prueba_commit=str(proof.relative_to(BASE)))
    entries = json.loads((BASE / 'entregas.json').read_text())
    index = next(i for i, row in enumerate(entries) if row['paquete'] == package)
    entries[index] = entry
    # Este asiento ocurre ANTES de abrir el esperado.
    (BASE / 'entregas.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
    print('CONGELADO', package, commit, digest, flush=True)
    comparison = BASE / 'comparaciones' / (package + '--comparacion.json')
    reveal = now()
    subprocess.run(['python3', str(ROOT / 'tools/validacion/astra6_catalogo/astra6_compara_catalogo.py'),
                    '--reconstruccion', str(checkout / reconstruction), '--recibo', str(destination / 'recibo.json'),
                    '--sha256-recibido', digest, '--salida', str(comparison)], check=True)
    entry.update(revelacion_utc=reveal, comparacion=str(comparison.relative_to(BASE)),
                 comparacion_sha256=sha(comparison), estado='COMPARADO')
    entries[index] = entry
    (BASE / 'entregas.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
    print('COMPARADO', package, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paquete')
    parser.add_argument('--checkout', required=True, type=Path)
    parser.add_argument('--reconstruccion', required=True, type=Path)
    parser.add_argument('--incluye', action='append', default=[])
    args = parser.parse_args()
    receive(args.paquete, args.checkout, args.reconstruccion, args.incluye)
