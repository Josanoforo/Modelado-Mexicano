#!/usr/bin/env python3
"""Reproduce el código independiente congelado; no constituye otro intento ciego."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'


def replay(package, destination, staged=None):
    destination = destination.resolve()
    assert not destination.exists() and not destination.is_relative_to(ROOT)
    destination.mkdir(parents=True)
    if staged is None:
        staged = destination / 'insumos'
        subprocess.run(['python3', str(ROOT / 'tools/validacion/astra6_paquetes.py'),
                        '--materializa', package, '--destino', str(staged)], check=True)
    staged = staged.resolve()
    entry = next(x for x in json.loads((BASE / 'entregas.json').read_text()) if x['paquete'] == package)
    assert hashlib.sha256((staged / 'entrada/manifiesto.json').read_bytes()).hexdigest() == entry['paquete_sha256']
    archived = BASE / 'reconstrucciones' / package
    mapping = json.loads((archived / (package + '--rutas-originales.json')).read_text())
    work = destination / 'work'
    work.mkdir()
    for original, physical in mapping.items():
        if Path(original).suffix == '.py':
            shutil.copyfile(archived / physical, work / Path(original).name)
    # Los calculadores recibidos usaron ambos nombres para la misma entrada.
    shutil.copytree(staged / 'entrada', work / 'entrada')
    shutil.copytree(staged / 'entrada', work / 'entradas')
    (work / 'raw').mkdir()
    command = ['bwrap', '--unshare-user', '--unshare-pid', '--unshare-ipc', '--unshare-uts',
               '--unshare-net', '--die-with-parent', '--clearenv',
               '--setenv', 'PATH', '/usr/bin:/bin', '--setenv', 'LANG', 'C.UTF-8',
               '--setenv', 'LD_LIBRARY_PATH', '/usr/lib/x86_64-linux-gnu/blas:/usr/lib/x86_64-linux-gnu/lapack',
               '--ro-bind', '/usr', '/usr', '--ro-bind', '/bin', '/bin', '--ro-bind', '/lib', '/lib',
               '--ro-bind', '/lib64', '/lib64', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
               '--ro-bind', str(staged / 'entrada'), '/entrada', '--ro-bind', str(staged / 'raw'), '/raw',
               '--bind', str(work), '/work/reconstruccion',
               '--ro-bind', str(staged / 'raw'), '/work/reconstruccion/raw',
               '--chdir', '/work/reconstruccion', '/usr/bin/python3', 'reconstruir.py']
    with (destination / 'replay.log').open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    assert result.returncode == 0, 'Revisar replay.log; no altera el código congelado'
    generated = work / ('salida/reconstruccion.tsv' if 'comunitaria' in package else 'reconstruccion.tsv')
    original = archived / mapping['salida/reconstruccion.tsv' if 'comunitaria' in package else 'reconstruccion.tsv']
    actual, expected = generated.read_bytes(), original.read_bytes()
    record = {'paquete': package, 'alcance': 'Replay de código independiente congelado; no nuevo recálculo ciego',
              'sha256_generado': hashlib.sha256(actual).hexdigest(),
              'sha256_original': hashlib.sha256(expected).hexdigest(), 'identico': actual == expected,
              'log_local': str(destination / 'replay.log')}
    (destination / 'replay.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(record, ensure_ascii=False))
    assert actual == expected, 'Replay diferente; conservar evidencia sin sustituir salida original'
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paquete')
    parser.add_argument('--destino', required=True, type=Path)
    parser.add_argument('--materializado', type=Path)
    args = parser.parse_args()
    replay(args.paquete, args.destino, args.materializado)
