#!/usr/bin/env python3
"""Preparación no ciega C1. Nunca ejecuta productores ni lee registros raw.

El manifiesto de cada paquete es una allowlist: el lanzamiento copia solo
esas entradas. La comprobación textual complementa los hashes, no acredita
independencia cognitiva. Los valores esperados quedan fuera de paquetes/.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import gzip
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1'
CAT = 'canon/catalogo-del-mexicano-v1_1.tsv'
SAFE_FIELDS = ['llave', 'calc', 'result_id', 'celda', 'instrumento', 'ola',
               'conducta', 'eje', 'segmento', 'unidad', 'naturaleza_ic']


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def read_tsv(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def tsv(path, rows, fields):
    with Path(path).open('w', newline='') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def verify_files(folder, manifest):
    assert {p.name for p in folder.iterdir()} == set(manifest['archivos']) | {'manifiesto.json'}
    for name, digest in manifest['archivos'].items():
        assert Path(name).name == name, 'Nombre fuera de allowlist plana'
        path = folder / name
        assert not path.is_symlink() and path.is_file() and sha(path) == digest, f'Hash o enlace inválido: {path}'
        assert path.suffix in {'.md', '.json', '.tsv'}, 'Tipo de archivo no autorizado'
        assert not re.search(r'medidor\.py|resultados\.json|reports/|\.git/|p=0\.\d{4}', path.read_text()), path


def cut_bytes(cut, path):
    return subprocess.check_output(['git', 'show', f'{cut}:{path}'], cwd=ROOT)


def package_id(calc):
    return calc.removeprefix('CALC-').lower()


def locations():
    private = BASE / 'preparacion/ubicaciones.local.json'
    if private.exists():
        return json.loads(private.read_text())
    sys.path.insert(0, str(ROOT / 'tests'))
    from payload_resolver import resolver_payload
    manifest = yaml.safe_load((ROOT / 'data/manifiesto.yaml').read_text())
    ids = {i['id'] for lot in json.loads((BASE / 'lotes.json').read_text())
           for i in json.loads(package_files(lot['paquete'])['insumos.json'])}
    return {i: resolver_payload(i, entradas=manifest, root=str(ROOT)) for i in sorted(ids)}


def package_files(pid):
    archive = BASE / 'paquetes' / pid / (pid + '-entradas.tar.gz')
    with tarfile.open(archive, 'r:gz') as tar:
        members = tar.getmembers()
        assert len({m.name for m in members}) == len(members), 'Miembros duplicados'
        assert all(m.isfile() and Path(m.name).name == m.name for m in members), 'Archivo o ruta no autorizados'
        return {m.name: tar.extractfile(m).read() for m in members}


def resolve_inputs(calc, specs, seen=None):
    """Remonta padres declarados para derivados; jamás importa sus scripts."""
    seen = set() if seen is None else seen
    if calc in seen:
        return set()
    seen.add(calc)
    spec = specs.setdefault(calc, yaml.safe_load((ROOT / 'data/corrida0' / calc / 'spec.yaml').read_text()))
    ids = {i['id'] for i in spec.get('inputs', []) if i.get('origen') == 'manifiesto'}
    ids.update(i['id'] for k in ['payloads', 'codebook'] for i in spec.get(k, []) if 'id' in i)
    for i in spec.get('inputs', []):
        match = re.search(r'data/corrida0/(CALC-[^/]+)/', i.get('ruta', ''))
        if match and match[1] != calc:
            ids.update(resolve_inputs(match[1], specs, seen))
    return ids


def prepare():
    if (BASE / 'corte.json').exists():
        tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', str((BASE / 'corte.json').relative_to(ROOT))],
                                 cwd=ROOT, capture_output=True).returncode == 0
        if tracked:
            raise ValueError('El corte está archivado; no se regenera un paquete congelado.')
    BASE.mkdir(parents=True, exist_ok=True)
    prep = BASE / 'preparacion'
    prep.mkdir(exist_ok=True)
    cut = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    snapshot = prep / 'catalogo-al-corte.tsv.gz'
    catalog_bytes = cut_bytes(cut, CAT)
    snapshot.write_bytes(gzip.compress(catalog_bytes, mtime=0))
    rows = read_tsv(snapshot)
    assert len({r['llave'] for r in rows}) == len(rows), 'Llaves duplicadas'
    manifest = yaml.safe_load((ROOT / 'data/manifiesto.yaml').read_text())
    entries = {e['id']: e for e in manifest}
    sys.path.insert(0, str(ROOT / 'tests'))
    from payload_resolver import resolver_payload
    recipes = json.loads((prep / 'extracciones.json').read_text())
    specs, resolved, all_packages, sources = {}, {}, [], []
    universe = []
    for calc in sorted({r['calc'] for r in rows}):
        own = [r for r in rows if r['calc'] == calc]
        pid = package_id(calc)
        archive_dir = BASE / 'paquetes' / pid
        archive_dir.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='astra6-entradas-')
        dest = Path(temporary.name)
        spec = yaml.safe_load((ROOT / 'data/corrida0' / calc / 'spec.yaml').read_text())
        primary = (ROOT / 'data/corrida0' / calc / spec.get('spec_md', 'spec.md')).resolve()
        sources.append({'paquete': pid, 'original': str(primary.relative_to(ROOT)),
                        'sha256_original': sha(primary), 'entregado': False})
        ids = resolve_inputs(calc, specs)
        # Documentación oficial por identidad instrumento/ola, sin notas del productor.
        instr = {r['instrumento'].lower().split('-')[0] for r in own}
        years = {y for r in own for y in re.findall(r'(?:19|20)\d{2}', str(r['ola']))}
        years.update(y for ident in ids for y in re.findall(r'(?:19|20)\d{2}', ident))
        for e in manifest:
            ident = e['id'].lower()
            year_match = any(y in ident or (y[-2:] in ident and ident.startswith(('encig', 'envipe'))) for y in years)
            generic_doc = 'enoe' in instr and not re.search(r'(?:19|20)\d{2}', ident)
            if any(i in ident for i in instr) and (year_match or generic_doc):
                if any(t in ident for t in ['_fd', 'descriptor', 'cuestionario', 'diseno_muestral', 'estructura_base', 'descripcion_archivos']):
                    ids.add(e['id'])
        inputs = []
        for ident in sorted(ids):
            e = entries.get(ident, {})
            if ident not in resolved:
                resolved[ident] = resolver_payload(ident, entradas=manifest, root=str(ROOT))
            rr = resolved[ident]
            inputs.append({'id': ident, 'archivo': e.get('archivo'), 'sha256': e.get('sha256'),
                           'url': e.get('url_origen'), 'estado_acceso': rr['estado']})
        missing = []
        recipe = recipes.get(calc)
        if recipe:
            sections = []
            for item in recipe['fuentes']:
                src = ROOT / item['ruta']
                lines = src.read_text().splitlines(keepends=True)
                excerpts = [''.join(lines[a-1:b]) for a, b in item['rangos']]
                for omitted in item.get('supresiones', []):
                    assert sum(x.count(omitted) for x in excerpts) == 1, (calc, omitted)
                    excerpts = [x.replace(omitted, '') for x in excerpts]
                sections += excerpts
                sources.append({'paquete': pid, 'ruta': item['ruta'], 'sha256': sha(src),
                                'rangos': item['rangos'], 'supresiones': item.get('supresiones', [])})
            (dest / 'metodo.md').write_text('# Método: extracción fiel de especificación humana\n\n' + '\n\n'.join(sections))
            missing.extend(recipe.get('faltantes', []))
        else:
            missing.append('SPEC-HUMANA: falta extracción libre de resultados; original identificado en preparación.')
        if not any(any(t in x['id'].lower() for t in ['_fd', 'descriptor']) for x in inputs):
            missing.append('FD: no hay descriptor identificado entre las entradas.')
        if not any('cuestionario' in x['id'].lower() for x in inputs):
            missing.append('CUESTIONARIO: no hay cuestionario identificado entre las entradas.')
        for x in inputs:
            if x['estado_acceso'] != 'COINCIDE':
                missing.append(f"ACCESO:{x['id']}:{x['estado_acceso']}")
        if 'enif_2024_enif_2024_bd_csv' in ids:
            missing.append('RESERVA-ENIF2024-CREDITO: el ZIP completo no es entregable; falta proyección de columnas abiertas mediante procedimiento autorizado.')
        if calc == 'CALC-ENUT-0001':
            missing.append('FILTRACION-TEXTUAL: el resumen humano cita N observado; falta extracción sucesora sin ese conteo antes de entrega.')
        if calc == 'CALC-ENDIREH-PISOS-2006-MODULOS-0002':
            missing.append('CUESTIONARIOS-MC-MD-MS: documento identificado mezcla tabulados y cuestionarios; faltan las tres extracciones documentales sin cifras.')
        if not inputs:
            missing.append('RAW: no hay insumo externo declarado ni padre resuelto.')
        tolerance = spec.get('tolerancia', {})
        # Solo contrato numérico previo; las justificaciones pueden filtrar esperados.
        tol = {k: v for k, v in tolerance.items() if k in ['tipo', 'abs', 'rel']}
        if not isinstance(tol.get('abs'), (int, float)):
            missing.append('TOLERANCIA: falta tolerancia absoluta numérica previa; no se inventa al comparar.')
        write_json(dest / 'insumos.json', inputs)
        write_json(dest / 'tolerancia.json', tol)
        tsv(dest / 'estimandos.tsv', own, SAFE_FIELDS)
        (dest / 'encargo.md').write_text(
            '# Reconstrucción independiente\n\n'
            'Sesión nueva sin historial. Recibe únicamente esta carpeta y los insumos enumerados. '
            'Implementa desde metodo.md, cuestionarios y FD, con dependencias estadísticas genéricas. '
            'No uses helpers del productor. Si falta método o acceso, informa el faltante sin adivinar.\n\n'
            'Reconstruye cada llave de estimandos.tsv. Entrega reconstruccion.tsv con columnas '
            'llave, punto, ic95_inf, ic95_sup y estado. No sustituyas un IC aleatorio por el esperado: '
            'conserva semilla y criterio de la spec y documenta diferencias de RNG. '
            'Congela código, entradas y números con SHA-256 y commit ANTES de solicitar revelación. '
            'Adjunta el SHA-256 de manifiesto.json recibido y conserva su lista de entradas.\n\n'
            'El preparador conoce resultados; no ejecuta esta reconstrucción. '
            'Si el entorno permite leer el clon, la comparación u otras reservas, rotula '
            'REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA. Nunca declares COINCIDE en preparación.\n')
        write_json(dest / 'faltantes.json', missing)
        files = {p.name: sha(p) for p in sorted(dest.iterdir()) if p.is_file() and p.name != 'manifiesto.json'}
        write_json(dest / 'manifiesto.json', {'paquete': pid, 'archivos': files})
        archive = archive_dir / (pid + '-entradas.tar.gz')
        with archive.open('wb') as stream, gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode='w') as tar:
                for file in sorted(dest.iterdir()):
                    data = file.read_bytes()
                    info = tarfile.TarInfo(file.name)
                    info.size = len(data)
                    info.mode = 0o644
                    tar.addfile(info, io.BytesIO(data))
        all_packages.append({'paquete': pid, 'calc': calc, 'estimadores': len(own),
                             'estado_preparacion': 'DISPONIBLE' if not missing else 'INCOMPLETO',
                             'faltantes': missing, 'sha256': sha(dest / 'manifiesto.json'),
                             'archivo': archive.name, 'sha256_contenedor': sha(archive)})
        temporary.cleanup()
        universe.extend({**{k: r[k] for k in SAFE_FIELDS}, 'firma_fp': r['firma_fp'],
                         'estado_adopcion': r['estado_adopcion'], 'origen_piso': r['origen_piso'],
                         'paquete': pid, 'estado': 'NO-EVALUADO'} for r in own)
    tsv(BASE / 'universo.tsv', universe, list(universe[0]))
    write_json(prep / 'ubicaciones.local.json', resolved)
    write_json(prep / 'procedencia-metodos.json', sources)
    inventory = read_tsv(ROOT / 'forense/analisis/catalogo/v1_1/calcs.tsv')
    write_json(prep / 'calcs-al-corte.json', [x for x in inventory if x['calc'] in {r['calc'] for r in rows}])
    write_json(BASE / 'lotes.json', all_packages)
    write_json(BASE / 'corte.json', {'commit': cut, 'catalogo': CAT, 'sha256': hashlib.sha256(catalog_bytes).hexdigest(),
                                   'filas': len(rows), 'estimadores_unicos': len({(r['calc'], r['result_id'], r['celda']) for r in rows}),
                                   'calcs': len(all_packages), 'results': len({(r['calc'], r['result_id']) for r in rows}),
                                   'firmas_citadas': len({r['firma_fp'] for r in rows}),
                                   'afirmaciones': 'NO-INTERCAMBIABLE-CON-ESTIMADORES; catálogo sin mapeo por afirmación'})
    print(json.dumps({'corte': cut, 'paquetes': len(all_packages),
                      'disponibles': sum(p['estado_preparacion'] == 'DISPONIBLE' for p in all_packages)}, ensure_ascii=False))


def verify():
    cut = json.loads((BASE / 'corte.json').read_text())
    snapshot = BASE / 'preparacion/catalogo-al-corte.tsv.gz'
    catalog_bytes = gzip.decompress(snapshot.read_bytes())
    assert hashlib.sha256(catalog_bytes).hexdigest() == cut['sha256']
    assert catalog_bytes == cut_bytes(cut['commit'], cut['catalogo'])
    original = read_tsv(snapshot)
    adoptions = json.loads((BASE / 'preparacion/adopciones-al-corte.json').read_text())
    assert {a['referencia'] for a in adoptions} == {r['firma_fp'] for r in original}
    assert all(a['estado'].startswith('FIRMADA') if a['tipo'] == 'FP' else a['estado'] in {'ASENTADA', 'ARCHIVADO'} for a in adoptions)
    producers = json.loads((BASE / 'preparacion/calcs-al-corte.json').read_text())
    assert {s['calc'] for s in producers} == {r['calc'] for r in original}
    for source in producers:
        calcdir = ROOT / 'data/corrida0' / source['calc']
        assert sha(calcdir / 'resultados.json') == source['sha256_resultados']
        assert sha(calcdir / 'sello.json') == source['sha256_sello']
        data = json.loads((calcdir / 'resultados.json').read_text())['resultados']
        tables = {}
        for row in (r for r in original if r['calc'] == source['calc']):
            value = data[row['result_id']]
            if '#' in row['llave']:
                if row['result_id'] not in tables:
                    value = json.loads(value) if isinstance(value, str) else value
                    tables[row['result_id']] = value['celdas'] if isinstance(value, dict) else value
                cells = tables[row['result_id']]
                cell = cells[int(row['celda'])]
                value = cell.get('punto', cell.get('p'))
            assert float(value) == float(row['punto']), row['llave']
    universe = read_tsv(BASE / 'universo.tsv')
    expected = {r['llave']: r for r in original}
    assert len(universe) == len(expected)
    assert {r['llave'] for r in universe} == set(expected)
    seen = []
    for lot in json.loads((BASE / 'lotes.json').read_text()):
        folder = BASE / 'paquetes' / lot['paquete']
        assert {p.name for p in folder.iterdir()} == {lot['archivo']}
        assert sha(folder / lot['archivo']) == lot['sha256_contenedor']
        contents = package_files(lot['paquete'])
        assert hashlib.sha256(contents['manifiesto.json']).hexdigest() == lot['sha256']
        manifest = json.loads(contents['manifiesto.json'])
        with tempfile.TemporaryDirectory(prefix='astra6-verifica-') as tmp:
            for name, content in contents.items():
                (Path(tmp) / name).write_bytes(content)
            verify_files(Path(tmp), manifest)
        own = list(csv.DictReader(io.StringIO(contents['estimandos.tsv'].decode()), delimiter='\t'))
        assert len(own) == lot['estimadores']
        for r in own:
            assert r == {k: expected[r['llave']][k] for k in SAFE_FIELDS}
            seen.append(r['llave'])
        missing = json.loads(contents['faltantes.json'])
        assert missing == lot['faltantes']
        assert (lot['estado_preparacion'] == 'DISPONIBLE') == (not missing)
    assert len(seen) == len(set(seen)) == len(expected) and set(seen) == set(expected)
    for r in universe:
        assert r['estado'] == 'NO-EVALUADO'
        assert all(r[k] == expected[r['llave']][k] for k in SAFE_FIELDS)
    resolved = locations()
    for location in resolved.values():
        if location['estado'] == 'COINCIDE':
            p = Path(location['ruta_absoluta'])
            assert p.is_file() and sha(p) == location['sha256_esperado'], location['id']
    print(f"VERDE: cobertura exacta de {len(seen)} filas; hashes y allowlists de paquetes; cero validaciones declaradas.")


def stage(pid, output):
    verify()
    lot = next(x for x in json.loads((BASE / 'lotes.json').read_text()) if x['paquete'] == pid)
    assert lot['estado_preparacion'] == 'DISPONIBLE', lot['faltantes']
    output = Path(output).resolve()
    assert not output.exists(), 'Destino debe ser nuevo'
    assert not output.is_relative_to(ROOT), 'Destino fuera del clon'
    source = package_files(pid)
    resolved = locations()
    # Verifica identidad antes de copiar; nunca abre miembros de ZIP.
    inputs = json.loads(source['insumos.json'])
    for i in inputs:
        p = Path(resolved[i['id']]['ruta_absoluta'])
        assert p.is_file() and sha(p) == i['sha256'], i['id']
    (output / 'entrada').mkdir(parents=True)
    for name, content in source.items():
        (output / 'entrada' / name).write_bytes(content)
    (output / 'raw').mkdir()
    for i in inputs:
        shutil.copyfile(resolved[i['id']]['ruta_absoluta'], output / 'raw' / (i['id'] + Path(i['archivo']).suffix))
    write_json(output / 'recibo-entrada.json', {'paquete': pid, 'sha256': lot['sha256'],
                                               'rotulo': 'REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA',
                                               'motivo': 'Copia aislada; restricción efectiva de la sesión aún no acreditada.'})
    print(f'Entradas copiadas a {output}; sesión nueva y aislamiento efectivo son requisitos del lanzamiento ciego.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepara', action='store_true')
    p.add_argument('--verifica', action='store_true')
    p.add_argument('--materializa', metavar='PAQUETE')
    p.add_argument('--destino')
    a = p.parse_args()
    try:
        if a.prepara:
            prepare()
        elif a.materializa:
            assert a.destino, '--destino obligatorio'
            stage(a.materializa, a.destino)
        else:
            verify()
    except (AssertionError, ValueError, StopIteration, OSError) as e:
        print(f'ROJO: {e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
