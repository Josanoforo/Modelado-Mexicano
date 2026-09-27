#!/usr/bin/env python3
"""⟲ Adaptador estructural v2; congelación verificada antes de abrir referencia."""
import argparse
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path

CONTRACT = Path(__file__).with_name('contrato-v2.json')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'Llave JSON duplicada: ' + key)
        result[key] = value
    return result


def read_json(path):
    def invalid(value):
        raise ValueError('Numero no finito: ' + value)
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=invalid,
                      parse_float=str)


def write_json(path, value):
    with Path(path).open('x') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def number(value):
    require(type(value) in (str, int, float), 'Tipo numerico invalido')
    if isinstance(value, str):
        require(bool(re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?', value)), 'Decimal invalido')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('Decimal invalido') from exc
    require(result.is_finite(), 'Numero no finito')
    return result


def normalize(document, contract=None):
    contract = read_json(CONTRACT) if contract is None else contract
    require(type(document) is dict and set(document) == {'version', 'identidad', 'filas'}, 'Campos de documento invalidos')
    require(type(document['version']) is int and document['version'] == contract['version'] == 2, 'Version invalida')
    identity = document['identidad']
    require(type(identity) is dict and set(identity) == set(contract['identidad']), 'Identidad incompleta/extra')
    require(all(type(v) is str and v for v in identity.values()), 'Tipo de identidad invalido')
    require(bool(re.fullmatch('[0-9a-f]{64}', identity['sha256_entrada'])), 'Hash entrada invalido')
    require(type(document['filas']) is list and document['filas'], 'Filas invalidas')
    aliases = contract['alias']
    allowed = {'llave', 'unidad', 'estado'} | set(contract['campos_opcionales']) | {a for values in aliases.values() for a in values}
    seen, rows, mappings = set(), [], []
    for row in document['filas']:
        require(type(row) is dict and set(row) <= allowed and {'llave','unidad','estado'} <= set(row), 'Campos de fila faltantes/extra')
        require(all(type(row[k]) is str and row[k] for k in ('llave','unidad','estado')), 'Tipos de fila invalidos')
        require(row['llave'] not in seen, 'Llave repetida')
        seen.add(row['llave'])
        require(row['estado'] in contract['estados'], 'Estado invalido')
        out = {k: v for k, v in row.items() if k in {'llave','unidad','estado'} | set(contract['campos_opcionales'])}
        for key in contract['campos_opcionales']:
            if key in row:
                require(type(row[key]) is str and bool(row[key]), 'Tipo opcional invalido')
        if 'estado_ic' in row:
            require(row['estado_ic'] in contract['estados_ic'], 'Estado IC invalido')
        mapping = {}
        for target, names in aliases.items():
            present = [key for key in names if key in row]
            require(len(present) <= 1, 'Colision ambigua: ' + target)
            if present:
                source = present[0]
                value = row[source]
                if value is not None:
                    number(value)
                out[target] = value
                mapping[target] = source
            else:
                mapping[target] = None
        if row['estado'] == 'RECONSTRUIDO':
            require('punto' in out and out['punto'] is not None, 'Falta punto reconstruido')
        if row.get('estado_ic') == 'SIN-IC':
            require('ic95_inf' not in out and 'ic95_sup' not in out, 'SIN-IC exige extremos ausentes')
        else:
            require(('ic95_inf' in out) == ('ic95_sup' in out), 'IC incompleto')
            if 'ic95_inf' in out:
                require((out['ic95_inf'] is None) == (out['ic95_sup'] is None), 'IC null parcial')
                if out['ic95_inf'] is not None:
                    require(number(out['ic95_inf']) <= number(out['ic95_sup']), 'IC invertido')
            if row.get('estado_ic') == 'CALCULADO':
                require(out.get('ic95_inf') is not None and out.get('ic95_sup') is not None, 'IC calculado faltante')
        rows.append(out)
        mappings.append({'llave': row['llave'], 'campos': mapping})
    return {'version': 2, 'identidad': identity.copy(), 'filas': rows, 'mapa_campos': mappings}


def freeze(artifact_dir, original_path, code_paths, entry_path, tolerance_path, contract_path=CONTRACT):
    directory = Path(artifact_dir)
    require(not directory.exists(), 'Directorio de congelacion ya existe')
    contract = read_json(contract_path)
    original = read_json(original_path)
    normalized = normalize(original, contract)
    require(sha(entry_path) == original['identidad']['sha256_entrada'], 'Entrada no corresponde a identidad')
    tolerance = read_json(tolerance_path)
    require(set(tolerance) == {'abs','rel'} and all(number(v) >= 0 for v in tolerance.values()), 'Tolerancia invalida')
    require(bool(code_paths), 'Codigo de reconstruccion faltante')
    require(all(Path(p).is_file() for p in code_paths), 'Codigo inaccesible')
    directory.mkdir(parents=True)
    files = {'original.json': Path(original_path), 'entrada': Path(entry_path), 'tolerancia.json': Path(tolerance_path), 'contrato.json': Path(contract_path), 'adaptador.py': Path(__file__)}
    for i, path in enumerate(code_paths):
        files[f'codigo-{i}'] = Path(path)
    for name, path in files.items():
        (directory / name).write_bytes(path.read_bytes())
    write_json(directory / 'derivada.json', normalized)
    manifest = {'version': 2, 'identidad': original['identidad'], 'archivos': {name: sha(directory / name) for name in list(files) + ['derivada.json']}}
    write_json(directory / 'congelacion.json', manifest)
    return directory / 'congelacion.json'


def verify_freeze(artifact_dir, expected_manifest_sha256):
    directory = Path(artifact_dir)
    require(sha(directory / 'congelacion.json') == expected_manifest_sha256, 'Congelacion alterada')
    manifest = read_json(directory / 'congelacion.json')
    require(set(manifest) == {'version','identidad','archivos'} and manifest['version'] == 2, 'Manifiesto invalido')
    for name, digest in manifest['archivos'].items():
        require(Path(name).name == name and not (directory / name).is_symlink(), 'Ruta congelada invalida')
        require(sha(directory / name) == digest, 'Artefacto alterado: ' + name)
    require(sha(__file__) == manifest['archivos']['adaptador.py'], 'Comparador no coincide con congelado')
    require(sha(CONTRACT) == manifest['archivos']['contrato.json'], 'Contrato activo no coincide con congelado')
    normalized = normalize(read_json(directory / 'original.json'), read_json(directory / 'contrato.json'))
    require(normalized == read_json(directory / 'derivada.json'), 'Derivada no corresponde al original')
    require(normalized['identidad'] == manifest['identidad'] and sha(directory / 'entrada') == manifest['identidad']['sha256_entrada'], 'Identidad congelada invalida')
    return manifest


def compare(artifact_dir, expected_manifest_sha256, reference_path, expected_reference_sha256):
    manifest = verify_freeze(artifact_dir, expected_manifest_sha256)
    directory = Path(artifact_dir)
    require(sha(reference_path) == expected_reference_sha256, 'Referencia alterada')
    reference = normalize(read_json(reference_path), read_json(directory / 'contrato.json'))
    actual = read_json(directory / 'derivada.json')
    require(reference['identidad'] == actual['identidad'], 'Identidad referencia incompatible')
    targets = {r['llave']: r for r in reference['filas']}
    require(set(targets) == {r['llave'] for r in actual['filas']}, 'Llaves referencia incompatibles')
    tolerance = read_json(directory / 'tolerancia.json')
    absolute, relative = number(tolerance['abs']), number(tolerance['rel'])
    results = []
    for row in actual['filas']:
        target = targets[row['llave']]
        require(target['unidad'] == row['unidad'], 'Unidad incompatible')
        fields = {}
        for field in ('punto','ic95_inf','ic95_sup'):
            a, b = row.get(field), target.get(field)
            state_a = 'AUSENTE' if field not in row else 'NULL' if a is None else 'NUMERO'
            state_b = 'AUSENTE' if field not in target else 'NULL' if b is None else 'NUMERO'
            item = {'estado_actual': state_a, 'estado_referencia': state_b, 'dentro': state_a == state_b}
            if state_a == state_b == 'NUMERO':
                da, db = number(a), number(b)
                with localcontext() as ctx:
                    values = (da, db, absolute, relative)
                    ctx.prec = max(64, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in values) + 8)
                    delta = da - db
                    item.update(delta=str(delta), dentro=abs(delta) <= max(absolute, relative * max(abs(da),abs(db))))
            fields[field] = item
        match = all(f['dentro'] for f in fields.values()) and row.get('estado_ic') == target.get('estado_ic')
        status = row['estado'] if row['estado'] != 'RECONSTRUIDO' else 'COINCIDE' if match else 'DISCREPA'
        results.append({'llave':row['llave'],'estado':status,'campos':fields})
    return {'version':2,'identidad':manifest['identidad'],'congelacion_sha256':expected_manifest_sha256,'referencia_sha256':expected_reference_sha256,'contrato_sha256':manifest['archivos']['contrato.json'],'comparador_sha256':manifest['archivos']['adaptador.py'],'tolerancia_sha256':manifest['archivos']['tolerancia.json'],'tolerancia':tolerance,'resultados':results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('normalizar'); p.add_argument('original'); p.add_argument('salida')
    p = sub.add_parser('congelar'); p.add_argument('directorio'); p.add_argument('original'); p.add_argument('entrada'); p.add_argument('tolerancia'); p.add_argument('codigo', nargs='+')
    p = sub.add_parser('verificar'); p.add_argument('directorio'); p.add_argument('sha256')
    p = sub.add_parser('comparar'); p.add_argument('directorio'); p.add_argument('sha256'); p.add_argument('referencia'); p.add_argument('referencia_sha256'); p.add_argument('salida')
    args = parser.parse_args()
    if args.command == 'normalizar': write_json(args.salida, normalize(read_json(args.original)))
    elif args.command == 'congelar':
        path = freeze(args.directorio,args.original,args.codigo,args.entrada,args.tolerancia)
        print(sha(path))
    elif args.command == 'verificar': verify_freeze(args.directorio,args.sha256); print('CONGELACION-VERIFICADA')
    else: write_json(args.salida, compare(args.directorio,args.sha256,args.referencia,args.referencia_sha256))


if __name__ == '__main__':
    main()
