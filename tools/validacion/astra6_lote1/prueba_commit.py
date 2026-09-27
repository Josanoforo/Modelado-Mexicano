#!/usr/bin/env python3
"""Prueba portable de pertenencia al commit para código y salidas agregadas."""
import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess


def exigir(condition, message):
    if not condition:
        raise ValueError(message)


def permitida(path):
    parts = PurePosixPath(path).parts
    exigir(parts and not path.startswith('/') and '..' not in parts, 'Ruta inválida')
    exigir(not any(p.lower() in {'raw', 'documentacion', 'documentación', 'entrada', 'insumos'} for p in parts), 'Ruta de insumos prohibida')
    exigir(PurePosixPath(path).suffix.lower() in {'.py', '.r', '.sh', '.tsv', '.json'}, 'Solo código, TSV agregado y recibos JSON')
    return parts


def oid(kind, content):
    return hashlib.sha1(kind.encode() + b' ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def encode(content):
    return base64.b64encode(content).decode('ascii')


def decode(content):
    return base64.b64decode(content, validate=True)


def arbol(content):
    entries = {}
    cursor = 0
    while cursor < len(content):
        space = content.index(b' ', cursor)
        null = content.index(b'\0', space)
        mode = content[cursor:space].decode('ascii')
        name = content[space + 1:null].decode('utf-8')
        identifier = content[null + 1:null + 21]
        exigir(len(identifier) == 20 and name not in entries, 'Tree Git inválido')
        entries[name] = (mode, identifier.hex())
        cursor = null + 21
    return entries


def raiz(commit):
    first = commit.split(b'\n', 1)[0]
    exigir(first.startswith(b'tree ') and len(first) == 45, 'Commit Git sin tree SHA1')
    return first[5:].decode('ascii')


def generar(checkout, commit, paths):
    def cat(kind, identifier):
        return subprocess.check_output(['git', 'cat-file', kind, identifier], cwd=checkout)
    commit_content = cat('commit', commit)
    commit_oid = oid('commit', commit_content)
    exigir(commit_oid == subprocess.check_output(['git', 'rev-parse', commit], cwd=checkout).decode().strip(), 'Repositorio no usa SHA1')
    proof = {'commit_oid': commit_oid, 'commit_content_base64': encode(commit_content), 'archivos': []}
    exigir(len(paths) == len(set(paths)), 'Rutas duplicadas')
    for path in paths:
        parts = permitida(path)
        current = raiz(commit_content)
        chain = []
        for index, part in enumerate(parts):
            content = cat('tree', current)
            chain.append({'oid': current, 'content_base64': encode(content)})
            mode, current = arbol(content)[part]
            exigir(mode == '40000' if index < len(parts) - 1 else mode in {'100644', '100755'}, 'Ruta no es archivo regular')
        blob = cat('blob', current)
        proof['archivos'].append({'ruta': path, 'trees': chain, 'blob_oid': current, 'blob_content_base64': encode(blob)})
    verificar(proof)
    return proof


def verificar(proof):
    commit = decode(proof['commit_content_base64'])
    exigir(oid('commit', commit) == proof['commit_oid'], 'Commit adulterado')
    root = raiz(commit)
    files = {}
    for item in proof['archivos']:
        path = item['ruta']
        parts = permitida(path)
        exigir(path not in files, 'Ruta duplicada en prueba')
        exigir(len(item['trees']) == len(parts), 'Cadena incompleta de trees')
        current = root
        for index, (part, tree) in enumerate(zip(parts, item['trees'])):
            content = decode(tree['content_base64'])
            exigir(oid('tree', content) == tree['oid'] == current, 'Tree adulterado o desconectado')
            mode, current = arbol(content)[part]
            exigir(mode == '40000' if index < len(parts) - 1 else mode in {'100644', '100755'}, 'Modo Git inválido')
        blob = decode(item['blob_content_base64'])
        exigir(oid('blob', blob) == item['blob_oid'] == current, 'Blob adulterado o desconectado')
        files[path] = blob
    exigir(bool(files), 'Prueba sin archivos')
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operacion', required=True)
    create = sub.add_parser('generar')
    create.add_argument('--checkout', type=Path, required=True)
    create.add_argument('--commit', required=True)
    create.add_argument('--ruta', action='append', required=True, help='Allowlist explícita de código/TSV agregado/recibo')
    create.add_argument('--salida', type=Path, required=True)
    check = sub.add_parser('verificar')
    check.add_argument('prueba', type=Path)
    args = parser.parse_args()
    try:
        if args.operacion == 'generar':
            exigir(not args.salida.exists(), 'No sobrescribe prueba previa')
            args.salida.write_text(json.dumps(generar(args.checkout, args.commit, args.ruta), indent=2) + '\n')
        else:
            files = verificar(json.loads(args.prueba.read_text()))
            print(json.dumps({p: hashlib.sha256(c).hexdigest() for p, c in files.items()}, indent=2))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'PRUEBA-RECHAZADA: {error}\n')
