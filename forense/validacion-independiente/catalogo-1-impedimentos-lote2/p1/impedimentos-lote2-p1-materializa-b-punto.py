#!/usr/bin/env python3
"""Transporta únicamente el punto histórico B2022; no estima ni compara."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tarfile
import zipfile


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here.parents[3]
    contract_path = here / 'contratos/impedimentos-lote2-p1-b-0001.json'
    if digest(contract_path) != '8ab1b5626f240a11d9ad2d7d2e461b5b07929be1886d57bf08589e27e62d4e10':
        raise ValueError('Contrato puntual no coincide con contenido preparado')
    contract = json.loads(contract_path.read_text())
    if contract['identidad_historica'] != 'b-0001' or contract['firma_de_contenido_pendiente']:
        raise ValueError('Contrato no corresponde al alcance puntual autorizado')
    if contract['estimadores_historicos'] != 1 or contract['ic'] != 'FUERA-DEL-ALCANCE-PARCIAL':
        raise ValueError('No se autoriza ampliación a ensayo B o incertidumbre')
    source = repo / contract['fuente_contenedor']
    if digest(source) != contract['sha256_original']:
        raise ValueError('Contenedor original difiere')
    rawroot = Path('/home/pc0/mm-corpus/raw').resolve(strict=True)
    chosen = [x for x in contract['insumos_fuente']
              if x['id'] in {'enigh2022_nc_csv', 'enigh2022_descripcion_base_pdf'}]
    if {x['id'] for x in chosen} != {'enigh2022_nc_csv', 'enigh2022_descripcion_base_pdf'}:
        raise ValueError('Falta fuente/FD exactos')
    sources = {}
    for item in chosen:
        pinned = {
            'enigh2022_nc_csv': ('enigh2022_nc_csv.zip',
                '3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06'),
            'enigh2022_descripcion_base_pdf': ('enigh2022_descripcion_base_pdf.pdf',
                '7b0c4e6bd36ceb9eae7cc852fce5a38dbcf4f2da6b133d35df6b1443fc76836c'),
        }
        if (item['archivo'], item['sha256']) != pinned[item['id']]:
            raise ValueError('Fuente/bytes fuera de alcance autorizado')
        file = rawroot / item['archivo']
        if file.is_symlink() or file.resolve(strict=True).parent != rawroot:
            raise ValueError('Fuente fuera de custodia física')
        if not stat.S_ISREG(file.stat().st_mode) or not os.access(file, os.R_OK):
            raise ValueError('Fuente no regular/legible')
        if item['estado_acceso'] != 'COINCIDE' or digest(file) != item['sha256']:
            raise ValueError('Fuente no autorizada o hash distinto')
        sources[item['id']] = file
    fd = sources['enigh2022_descripcion_base_pdf'].read_bytes()
    if not fd.startswith(b'%PDF-'):
        raise ValueError('FD no es PDF')
    with zipfile.ZipFile(sources['enigh2022_nc_csv']) as z:
        literal = contract['miembro_literal']
        members = [x for x in z.infolist() if x.filename == literal]
        if len(members) != 1 or members[0].is_dir() or members[0].flag_bits & 1:
            raise ValueError('Miembro CSV ausente/duplicado/cifrado')
        member = z.read(members[0])
    # Documented column and text checks only; no observations or statistics.
    header = member.splitlines()[0].decode('utf-8-sig').lower().replace('"', '')
    if not {'folioviv', 'foliohog', 'factor', 'remesas'} <= set(header.split(',')):
        raise ValueError('Miembro no acredita esquema puntual')
    destination = Path(args.destino)
    if not destination.is_absolute() or '..' in destination.parts:
        raise ValueError('Destino absoluto sin ascensos requerido')
    for ancestor in [destination, *destination.parents]:
        if ancestor.is_symlink():
            raise ValueError('Enlace en destino')
    if destination == repo or repo in destination.parents:
        raise ValueError('Salida debe estar fuera del clon')
    if destination.exists():
        raise ValueError('Destino ya existe; no sobrescribir')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir(mode=0o700)
    with tarfile.open(source, 'r:gz') as archive:
        estimates = archive.extractfile('estimandos.tsv').read()
        tolerance = archive.extractfile('tolerancia.json').read()
    outputs = {
        'impedimentos-lote2-p1-b-concentrado2022.csv': member,
        'impedimentos-lote2-p1-b-fd2022.pdf': fd,
        'impedimentos-lote2-p1-b-estimandos.tsv': estimates,
        'impedimentos-lote2-p1-b-tolerancia.json': tolerance,
        'impedimentos-lote2-p1-b-contrato.json': contract_path.read_bytes(),
        'impedimentos-lote2-p1-b-metodo.md': (
            '# Punto aislado B2022\n\n' + contract['punto'] + '\n\n'
            'Solo RESULT-B-ENIGH-2022-P. No estimar selector, IC, CV ni ensayo B. '
            'No publicar como validación integral. Primera reconstrucción propia '
            'se congela antes de comparación. El PDF es descriptor oficial.\n'
        ).encode(),
    }
    hashes = {}
    for name, data in outputs.items():
        with (destination / name).open('xb') as f:
            f.write(data)
        (destination / name).chmod(0o600)
        hashes[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    receipt = {'estado': 'MATERIALIZADO-PUNTO-PARCIAL', 'identidad': 'b-0001',
               'estimadores': 1, 'validacion': 'NO-EVALUADO',
               'destino': str(destination), 'archivos': hashes,
               'fuentes': [{'ruta': str(sources[x['id']]), 'sha256': x['sha256']}
                           for x in chosen]}
    for name, expected in hashes.items():
        if digest(destination / name) != expected['sha256']:
            raise ValueError('Copia final difiere')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
