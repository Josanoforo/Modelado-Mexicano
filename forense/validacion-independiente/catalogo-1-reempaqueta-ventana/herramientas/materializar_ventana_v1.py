"""Extrae un contenedor verificado fuera de los worktrees del proyecto.

Protege el defecto real de C1: entrada incompleta o mezclada con expediente.
No lanza sesiones, no abre microdatos y no acredita aislamiento de red.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile


def materializar(tar, esperado, destino):
    tar, destino = Path(tar).resolve(), Path(destino).resolve()
    repo = Path(__file__).resolve().parents[4]
    # El sandbox presenta marcadores .git también en /tmp y en HOME;
    # contrastamos los worktrees reales del proyecto, sin inferir por marcador.
    lista = subprocess.check_output(['git', 'worktree', 'list', '--porcelain'], cwd=repo, text=True)
    clones = [Path(line[9:]).resolve() for line in lista.splitlines() if line.startswith('worktree ')]
    if any(destino == clon or clon in destino.parents for clon in clones):
        raise ValueError('destino dentro de un clon')
    if destino.exists():
        raise ValueError('destino debe ser nuevo')
    if hashlib.sha256(tar.read_bytes()).hexdigest() != esperado:
        raise ValueError('hash de contenedor cambiado')
    with tarfile.open(tar, 'r:gz') as archivo:
        miembros = archivo.getmembers()
        nombres = [m.name for m in miembros]
        if len(nombres) != len(set(nombres)):
            raise ValueError('miembros duplicados')
        if any(not m.isfile() or Path(m.name).name != m.name or m.name in {'.', '..'} for m in miembros):
            raise ValueError('miembro inseguro')
        contenido = {m.name: archivo.extractfile(m).read() for m in miembros}
    manifiesto = json.loads(contenido['manifiesto.json'])
    if set(contenido) != set(manifiesto['archivos']) | {'manifiesto.json'}:
        raise ValueError('miembros fuera de manifiesto')
    for nombre, esperado_miembro in manifiesto['archivos'].items():
        if hashlib.sha256(contenido[nombre]).hexdigest() != esperado_miembro:
            raise ValueError('hash de miembro cambiado')
    destino.mkdir(parents=True)
    for nombre, cuerpo in contenido.items():
        (destino / nombre).write_bytes(cuerpo)
    return {'destino': str(destino), 'miembros': len(contenido),
            'sha256_contenedor': esperado, 'red_aislada': 'NO-ACREDITADA',
            'raw_materializado': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--tar', required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--destino', required=True)
    a = p.parse_args()
    print(json.dumps(materializar(a.tar, a.sha256, a.destino), ensure_ascii=False))
