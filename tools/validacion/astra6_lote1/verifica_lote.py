#!/usr/bin/env python3
"""Verifica evidencia y cobertura del lote sin abrir esperados ni productores."""
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path
import re
import subprocess
import tarfile
import importlib.util

_spec = importlib.util.spec_from_file_location("prueba_commit", Path(__file__).with_name("prueba_commit.py"))
_prueba = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prueba)

ROOT = Path(__file__).resolve().parents[3]
CATALOGO = ROOT / 'forense/validacion-independiente/catalogo-1'
ENTREGA = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
ESTADOS = {'COINCIDE', 'DISCREPA', 'NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO', 'NO-EVALUADO'}


def exigir(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def filas(data):
    return list(csv.DictReader(io.StringIO(data.decode('utf-8')), delimiter='\t'))


def llaves(rows):
    keys = [row['llave'] for row in rows]
    exigir(all(keys) and len(keys) == len(set(keys)), 'Llaves vacías o duplicadas')
    return set(keys)


def fecha(value):
    exigir(isinstance(value, str) and bool(value), 'Falta fecha de evidencia')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    exigir(parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0, 'Fecha debe incluir zona UTC')
    return parsed


def ruta(base, value):
    exigir(isinstance(value, str) and value, 'Falta ruta de evidencia')
    path = (base / value).resolve()
    exigir(not Path(value).is_absolute() and path.is_relative_to(base.resolve()), 'Ruta fuera de entrega')
    return path


def comparacion(entrega, base, expected):
    entrada = fecha(entrega.get('entrada_registrada_utc'))
    freeze = fecha(entrega.get('congelacion_recibida_utc'))
    reveal = fecha(entrega.get('revelacion_utc'))
    exigir(entrada <= freeze < reveal, 'Orden inválido: entrada <= congelación < revelación')
    exigir(entrega.get('separacion_efectiva') is True, 'Comparación sin separación efectiva')
    reconstruction = ruta(base, entrega.get('reconstruccion', 'reconstrucciones/' + entrega['paquete'] + '/reconstruccion.tsv'))
    content = reconstruction.read_bytes()
    exigir(sha(content) == entrega.get('reconstruccion_sha256'), 'Hash reconstrucción incorrecto')
    own_rows = filas(content)
    exigir(llaves(own_rows) == expected, 'Cobertura incompleta de reconstrucción')
    own = {row['llave']: row for row in own_rows}
    commit = entrega.get('commit_reconstruccion', '')
    exigir(re.fullmatch(r'[0-9a-f]{40,64}', commit) is not None, 'Falta commit de reconstrucción válido')
    # El checkout permite comprobar el objeto congelado sin leer código productor.
    checkout = entrega.get('checkout_reconstruccion')
    verified_commit = False
    if entrega.get('prueba_commit'):
        proof = json.loads(ruta(base, entrega['prueba_commit']).read_text())
        exigir(proof['commit_oid'] == commit, 'Prueba pertenece a otro commit')
        files = _prueba.verificar(proof)
        relative = entrega.get('ruta_reconstruccion_commit', 'reconstruccion.tsv')
        exigir(files.get(relative) == content, 'Prueba no contiene reconstrucción archivada')
        verified_commit = True
    elif checkout and Path(checkout).is_dir():
        relative = entrega.get('ruta_reconstruccion_commit', 'reconstruccion.tsv')
        exigir(not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'Ruta commit inválida')
        committed = subprocess.check_output(['git', 'show', f'{commit}:{relative}'], cwd=checkout)
        exigir(sha(committed) == entrega['reconstruccion_sha256'], 'Commit no contiene la reconstrucción congelada')
        verified_commit = True
    path = ruta(base, entrega.get('comparacion'))
    raw = path.read_bytes()
    if entrega.get('comparacion_sha256'):
        exigir(sha(raw) == entrega['comparacion_sha256'], 'Hash comparación incorrecto')
    comparison = json.loads(raw)
    receipt = comparison['recibo']
    for field in ('paquete', 'paquete_sha256', 'reconstruccion_sha256', 'commit_reconstruccion'):
        exigir(receipt.get(field) == entrega.get(field), f'Recibo de comparación diverge: {field}')
    exigir(receipt.get('congelado_antes_de_revelacion') is True, 'Recibo sin congelación')
    results = comparison['resultados']
    exigir(llaves(results) == expected, 'Cobertura incompleta de comparación')
    for row in results:
        state = row.get('estado')
        exigir(state in ESTADOS, 'Estado desconocido')
        source = own[row['llave']]
        if state in {'COINCIDE', 'DISCREPA'}:
            exigir(source.get('estado') == 'RECONSTRUIDO' and bool(row.get('campos')), 'Estado numérico sin evidencia')
            exigir('punto' in row['campos'], 'Comparación sin punto')
            exigir(all(isinstance(x.get('dentro'), bool) and isinstance(x.get('delta'), (int, float)) and math.isfinite(x['delta']) for x in row['campos'].values()), 'Campos comparación inválidos')
            exigir((state == 'COINCIDE') == all(x['dentro'] for x in row['campos'].values()), 'Estado contradice comparación')
        else:
            exigir(source.get('estado') == state and bool(source.get('motivo') or source.get('explicacion')), 'Estado pendiente sin evidencia/motivo')
    return Counter(row['estado'] for row in results), verified_commit


def publicabilidad(base, entries, counts):
    """Dictamen de alcance separado del sello y de la comparación mecánica."""
    path = base / 'dictamenes-publicabilidad.tsv'
    adjudicated = counts.copy()
    if not path.exists():
        return 0, adjudicated
    overrides = filas(path.read_bytes())
    llaves(overrides)
    by_package = {entry['paquete']: entry for entry in entries}
    evidence = {}
    for override in overrides:
        package = override['paquete']
        exigir(package in by_package, 'Publicabilidad: paquete ajeno')
        entry = by_package[package]
        exigir(bool(entry.get('comparacion')), 'Publicabilidad sin comparación')
        reconstruction = entry.get('reconstruccion', 'reconstrucciones/' + package + '/reconstruccion.tsv')
        exigir(override.get('evidencia') == reconstruction, 'Publicabilidad: evidencia no corresponde a reconstrucción')
        if package not in evidence:
            own = filas(ruta(base, reconstruction).read_bytes())
            results = json.loads(ruta(base, entry['comparacion']).read_text())['resultados']
            evidence[package] = ({row['llave']: row for row in own}, {row['llave']: row for row in results})
        own, results = evidence[package]
        key = override['llave']
        exigir(key in own and key in results, 'Publicabilidad: identidad sin evidencia')
        source, result = own[key], results[key]
        exigir(override.get('estado_comparador') == result['estado'] == source['estado'] == 'NO-RECALCULABLE-DESDE-SPEC', 'Publicabilidad: estado mecánico incompatible')
        exigir(override.get('estado_dictamen') == 'DISCREPA' and override.get('efecto') == 'alcance: publicabilidad', 'Publicabilidad: solo discrepancia de alcance autorizada')
        reason = source.get('motivo') or source.get('explicacion') or ''
        exigir(reason.startswith(('SUPRIMIDO-POR-SPEC:', 'Estimación suprimida por regla de publicación de spec:')), 'Publicabilidad: fuente no acredita supresión ejecutada')
        exigir(all(not source.get(field) for field in ('punto', 'ic95_inf', 'ic95_sup')), 'Publicabilidad: supresión contiene cifras')
        exigir(bool(override.get('motivo')), 'Publicabilidad: falta motivo de dictamen')
        adjudicated['NO-RECALCULABLE-DESDE-SPEC'] -= 1
        adjudicated['DISCREPA'] += 1
    exigir(adjudicated['NO-RECALCULABLE-DESDE-SPEC'] >= 0, 'Publicabilidad: conteo inconsistente')
    return len(overrides), adjudicated


def verificar(base=ENTREGA, catalogo=CATALOGO):
    lots = json.loads((catalogo / 'lotes.json').read_text())
    ready = {lot['paquete']: lot for lot in lots if lot['estado_preparacion'] == 'DISPONIBLE'}
    entries = json.loads((base / 'entregas.json').read_text())
    exigir(isinstance(entries, list), 'entregas.json debe ser array')
    packages = [entry['paquete'] for entry in entries]
    exigir(len(packages) == len(set(packages)) and set(packages) == set(ready), 'Cobertura exacta de paquetes DISPONIBLE requerida')
    universe = filas((catalogo / 'universo.tsv').read_bytes())
    llaves(universe)
    sessions = set()
    counts, causes = Counter(), Counter()
    missing_commits = []
    denominator = 0
    for entry in entries:
        package = entry['paquete']
        lot = ready[package]
        archive = catalogo / 'paquetes' / package / lot['archivo']
        exigir(sha(archive.read_bytes()) == lot['sha256_contenedor'] == entry.get('sha256_contenedor'), f'{package}: hash contenedor incorrecto')
        with tarfile.open(archive, 'r:gz') as tar:
            manifest = tar.extractfile('manifiesto.json').read()
            exigir(sha(manifest) == lot['sha256'] == entry.get('paquete_sha256'), f'{package}: hash manifiesto incorrecto')
            estimands = tar.extractfile('estimandos.tsv').read()
            exigir(sha(estimands) == json.loads(manifest)['archivos']['estimandos.tsv'], 'Estimandos no corresponden al manifiesto')
            expected = llaves(filas(estimands))
        exigir(len(expected) == lot['estimadores'], 'Conteo lote diverge')
        universe_keys = {row['llave'] for row in universe if row['paquete'] == package}
        exigir(expected == universe_keys, 'Estimandos divergen de identidades del universo')
        denominator += len(expected)
        if entry.get('comparacion'):
            session = entry.get('session_id')
            exigir(isinstance(session, str) and session and session not in sessions, 'Session id vacío o reutilizado')
            sessions.add(session)
            result, verified_commit = comparacion(entry, base, expected)
            counts.update(result)
            for row in filas(ruta(base, entry.get('reconstruccion', 'reconstrucciones/' + package + '/reconstruccion.tsv')).read_bytes()):
                if row.get('estado') != 'RECONSTRUIDO':
                    causes[row.get('motivo') or row.get('explicacion')] += 1
            if not verified_commit:
                missing_commits.append(package)
        else:
            state = entry.get('estado')
            exigir(state in {'BLOQUEADO-POR-ACCESO', 'NO-EVALUADO'} and bool(entry.get('motivo')), f'{package}: pendiente sin estado/motivo')
            exigir(not entry.get('revelacion_utc'), 'Revelación sin comparación')
            counts[state] += len(expected)
            causes[entry['motivo']] += len(expected)
    evaluated = counts['COINCIDE'] + counts['DISCREPA'] + counts['NO-RECALCULABLE-DESDE-SPEC']
    suppressed, adjudicated = publicabilidad(base, entries, counts)
    return {'supresiones_reclasificadas': suppressed, 'estados_dictamen': dict(adjudicated), 'evaluados': evaluated, 'denominador_lote': denominator, 'denominador_universo': len(universe), 'estados': dict(counts), 'causas': dict(causes), 'commit_sin_verificacion_de_objeto': missing_commits}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrega', type=Path, default=ENTREGA)
    parser.add_argument('--catalogo', type=Path, default=CATALOGO)
    args = parser.parse_args()
    try:
        print(json.dumps(verificar(args.entrega, args.catalogo), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'LOTE-RECHAZADO: {error}\n')
