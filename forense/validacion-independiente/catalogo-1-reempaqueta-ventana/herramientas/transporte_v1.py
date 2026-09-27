"""Transporte documental v1: no calcula ni consulta valores del productor."""
import argparse
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

BASE = Path(__file__).resolve().parents[1]
COLUMNAS = ('llave calc result_id celda instrumento ola conducta eje segmento unidad naturaleza_ic').split()
VERSION = 'c1-ventana-v1'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()


def filas(b, ventana=False):
    lector = csv.DictReader(io.StringIO(b.decode('utf-8')), delimiter='\t')
    if lector.fieldnames != COLUMNAS + (['ventana'] if ventana else []):
        raise ValueError('esquema cerrado: valores, IC o codigo productor no admitidos')
    rows = list(lector)
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise ValueError('fila mal formada')
    keys = [r['llave'] for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('llave duplicada')
    if ventana and any(not r['ventana'] for r in rows):
        raise ValueError('ventana ausente')
    return rows


def transportar(b, mapa, metodo):
    rows = filas(b)
    keys = {r['llave'] for r in rows}
    if set(mapa) - keys:
        raise ValueError('llave inexistente en original')
    allowed = {"2021": {'vida', 'vida_relacion', 'desde_octubre_2020'},
               "2016": {'vida', 'desde_octubre_2015'}}
    for r in rows:
        if r['llave'] not in mapa:
            continue
        w = mapa[r['llave']]
        if w not in allowed.get(r['ola'], set()):
            raise ValueError('contradiccion temporal')
        if w.startswith('desde_octubre_') and w[-4:] not in metodo.decode('utf-8'):
            raise ValueError('ventana contradice metodo historico')
    lines = b.splitlines(keepends=True)
    def append(line, w):
        ending = b'\r\n' if line.endswith(b'\r\n') else b'\n'
        return line.rstrip(b'\r\n') + b'\t' + w.encode() + ending
    out = append(lines[0], 'ventana')
    for row, line in zip(rows, lines[1:], strict=True):
        if row['llave'] in mapa:
            out += append(line, mapa[row['llave']])
    filas(out, True)
    return out


def leer_tar(path):
    with tarfile.open(path) as t:
        members = t.getmembers()
        names = [m.name for m in members]
        if len(names) != len(set(names)) or any('/' in n or n in {'.', '..'} for n in names):
            raise ValueError('miembro inseguro o duplicado')
        if any(not m.isfile() for m in members):
            raise ValueError('solo miembros regulares')
        data = {m.name: t.extractfile(m).read() for m in members}
    manifest = json.loads(data['manifiesto.json'])
    if set(data) != set(manifest['archivos']) | {'manifiesto.json'}:
        raise ValueError('miembro no declarado')
    if any(n.endswith('.py') or 'resultados' in n.lower() or 'medidor' in n.lower() for n in data):
        raise ValueError('codigo productor o resultados no admitidos')
    for name, digest in manifest['archivos'].items():
        if sha(data[name]) != digest:
            raise ValueError('hash cambiado: ' + name)
    return data


def comprobar(original, nuevo):
    for name in ('metodo.md', 'tolerancia.json'):
        if original[name] != nuevo[name]:
            raise ValueError('diferencia no autorizada de metodo/tolerancia')
    old = {r['llave']: r for r in filas(original['estimandos.tsv'])}
    for r in filas(nuevo['estimandos.tsv'], True):
        before = {k: v for k, v in r.items() if k != 'ventana'}
        if old.get(r['llave']) != before:
            raise ValueError('diferencia no autorizada de identidad/metodo')


def escribir_tar(path, data):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w', format=tarfile.USTAR_FORMAT) as t:
        for name, b in sorted(data.items()):
            m = tarfile.TarInfo(name)
            m.size, m.mtime, m.mode = len(b), 0, 0o644
            t.addfile(m, io.BytesIO(b))
    path.write_bytes(gzip.compress(buf.getvalue(), mtime=0))


def crear(original_path, mapa, documentos):
    original = leer_tar(original_path)
    paquete = json.loads(original['manifiesto.json'])['paquete']
    nuevo = {k: original[k] for k in ('metodo.md', 'tolerancia.json', 'encargo.md')}
    if 'faltantes.json' in original:
        nuevo['faltantes.json'] = original['faltantes.json']
    if documentos.get('mantener_fd_xlsx'):
        nuevo['fd-endireh2016.xlsx'] = original['fd-endireh2016.xlsx']
    nuevo['estimandos.tsv'] = transportar(original['estimandos.tsv'], mapa, original['metodo.md'])
    nuevo['esquema.json'] = json_bytes({'version': VERSION, 'columnas': COLUMNAS + ['ventana'],
                                      'campos_adicionales': False})
    # Solo se incorporan documentos revisados por P3, nunca el listado historico completo.
    nuevo['insumos.json'] = json_bytes(documentos['insumos'])
    for name, path in documentos.get('miembros', {}).items():
        if '/' in name or name in nuevo or name == 'manifiesto.json':
            raise ValueError('nombre documental inseguro')
        nuevo[name] = Path(path).read_bytes()
    comprobar(original, nuevo)
    nuevo['manifiesto.json'] = json_bytes({'paquete': paquete, 'version_entrada': VERSION,
                                         'archivos': {k: sha(v) for k, v in sorted(nuevo.items())}})
    folder = BASE / 'entradas' / paquete
    folder.mkdir(parents=True, exist_ok=True)
    tar_path = folder / (paquete + '-entradas-ventana-v1.tar.gz')
    escribir_tar(tar_path, nuevo)
    audit = {'paquete': paquete, 'original': str(original_path), 'sha256_original': sha(original_path.read_bytes()),
             'sucesor': str(tar_path.relative_to(BASE)), 'sha256_sucesor': sha(tar_path.read_bytes()),
             'identidades_originales': len(filas(original['estimandos.tsv'])), 'identidades_sucesoras': len(mapa),
             'excluidas_por_alcance': sorted({r['llave'] for r in filas(original['estimandos.tsv'])} - set(mapa)),
             'miembros': [{'miembro': k, 'sha256_original': sha(original[k]) if k in original else None,
                           'sha256_sucesor': sha(nuevo[k]) if k in nuevo else None,
                           'estado': 'IDENTICO' if original.get(k) == nuevo.get(k) else 'CAMBIO-TRANSPORTE'}
                          for k in sorted(set(original) | set(nuevo))]}
    (BASE / 'paquetes' / (paquete + '-diff.json')).write_bytes(json_bytes(audit))
    return audit


def leer_mapa(path):
    grouped = {}
    with path.open() as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['estado'] != 'DEMOSTRADA-PUBLICADA':
                continue
            group = grouped.setdefault(r['paquete'], {})
            if r['llave'] in group:
                raise ValueError('ventana duplicada')
            group[r['llave']] = r['ventana']
    return grouped


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mapa', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    args = p.parse_args()
    grouped = leer_mapa(args.mapa)
    config = json.loads(args.config.read_text())
    if isinstance(config, dict):
        records = []
        for paquete, content in config.items():
            wave = '2016' if '2016' in paquete else '2021'
            history = BASE.parent / ('catalogo-1-preparacion-lote2/entradas' if wave == '2016' else 'catalogo-1/paquetes') / paquete
            originals = list(history.glob('*.tar.gz'))
            if len(originals) != 1:
                raise ValueError('original ambiguo')
            content = dict(content)
            docs = BASE / 'documentos-revisados'
            content['miembros'] = {**content.get('miembros', {}), **{
                f.name: str(f) for f in docs.glob('endireh' + wave + '*-semantica.json')}}
            if wave == '2016':
                content['miembros'].update({f.name: str(f) for f in docs.glob('fd2016-*.json')})
            content['insumos'] = [r for r in content['insumos'] if 'general_pdf' not in r['id']]
            records.append({'paquete': paquete, 'original': str(originals[0]), **content})
        config = records
    audits = [crear(Path(c['original']), grouped[c['paquete']], c) for c in config]
    (BASE / 'paquetes' / 'transporte-v1.json').write_bytes(json_bytes(audits))
    print(json.dumps({a['paquete']: a['identidades_sucesoras'] for a in audits}))


if __name__ == '__main__':
    main()
