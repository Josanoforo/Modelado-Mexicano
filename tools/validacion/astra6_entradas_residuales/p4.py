#!/usr/bin/env python3
"""Materializa y verifica contenedores exclusivamente documentales de residuales C1."""
import argparse
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-entradas-residuales-lote2'
OUT = BASE / 'p4'
ORIGINAL = ROOT / 'forense/validacion-independiente/catalogo-1-preparacion-lote2/entradas'
COHORTES = {
    'ENBIARE': 'enbiare-pisos-bienestar-0001',
    'ENCODAT': 'encodat-pisos-sustancias-0001',
    'ENCUCI': 'encuci-0001',
    'ENIGH': 'enigh-0001',
}
FIELDS = ['entrada_id', 'instrumento', 'ola', 'conducta', 'eje', 'segmento', 'unidad', 'celda']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tsv(rows, fields):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifica', action='store_true')
    args = parser.parse_args()
    config_path = OUT / 'residuales-p4-config.json'
    cfg = json.loads(config_path.read_text())
    affected = list(csv.DictReader((BASE / 'p1/tabla-llave-componente.tsv').open(), delimiter='\t'))
    expected = {r['llave'] for r in affected}
    maps, manifests = [], []
    OUT.mkdir(exist_ok=True)
    for inst, original_id in COHORTES.items():
        group = cfg[inst]
        original_path = next((ORIGINAL / original_id).glob('*.tar.gz'))
        original_hash = sha(original_path.read_bytes())
        selected = {r['llave'] for r in affected if r['instrumento'] == inst}
        members, schemas = {}, []
        successor = original_id + '-residuales-documentales-v1'
        with tarfile.open(original_path) as source:
            estimandos = list(csv.DictReader(io.StringIO(source.extractfile('estimandos.tsv').read().decode()), delimiter='\t'))
            for row in estimandos:
                if row['llave'] not in selected:
                    continue
                entry_id = row['llave'].replace('RESULT-', 'ENTRADA-RESIDUALES-', 1)
                clean = {k: row.get(k, '') for k in FIELDS}
                clean['entrada_id'] = entry_id
                if inst == 'ENCUCI':
                    clean.update(celda='B-P-RUR-AGR', segmento='agravio_rural', unidad='PERSONA')
                elif inst == 'ENIGH':
                    clean.update(celda='A-P-COMPLEMENTO', segmento='TOTAL', unidad='HOGAR')
                schemas.append(clean)
                maps.append(dict(original=row['llave'], entrada_id=entry_id, instrumento=inst,
                                 contenedor_original=str(original_path.relative_to(ROOT)),
                                 original_sha256=original_hash, sucesor=successor,
                                 componentes=','.join(sorted({r['componente'] for r in affected if r['llave'] == row['llave']})),
                                 decision=group['decision'], estado=group['estado']))
            for member in source.getmembers():
                if member.name.startswith(('cuestionario-', 'fd-')):
                    members[member.name] = source.extractfile(member).read()
            inputs = json.loads(source.extractfile('insumos.json').read())
            payloads = [item for item in inputs if item['archivo'].endswith('.zip')]
            access = '# Insumos y separación de la sesión\n\n'
            access += ('Solo una sesión nueva sin historial recibirá estos documentos; este contenedor no '
                       'autoriza ejecución ni apertura de datos por sí mismo. Una misión de recálculo '
                       'debe autorizar las olas abiertas y firmar los contratos propuestos antes de '
                       'iniciar. No abrir resultados, productores, dictámenes ni material exterior; '
                       'retornar únicamente salida propia según esquema y sellarla antes de comparar.\n\n')
            for item in payloads:
                access += f"Payload `{item['id']}`; archivo `{item['archivo']}`; SHA256 `{item['sha256']}`.\n\n"
            members['spec-acceso-insumos.md'] = access.encode()
            if inst == 'ENBIARE':
                members['spec-conductas-base.md'] = source.extractfile('conductas.md').read()
            if inst == 'ENCODAT':
                for name in ('metodo.md', 'conductas.md'):
                    members['spec-base-' + name] = source.extractfile(name).read()
        assert len(schemas) == len(selected), (inst, len(schemas), len(selected))
        members['esquema-identidades.tsv'] = tsv(schemas, FIELDS)
        members['esquema-salida.md'] = (
            '# Esquema de salida documental\n\n'
            'Una fila por entrada_id del esquema-identidades.tsv. Campos: entrada_id, conducta, eje, '
            'segmento, unidad, estimacion, n_valido, peso_denominador, exclusiones_por_causa; '
            'IC95_inf, IC95_sup y metodo_IC solo bajo contrato de incertidumbre adjunto. '
            'No contiene valores de referencia. No ejecutar contratos propuestos sin firma de contenido.\n'
        ).encode()
        for item in group['archivos']:
            path = ROOT / item['ruta']
            data = path.read_bytes()
            assert data, path
            assert item['nombre'] not in members, item['nombre']
            members[item['nombre']] = data
        assert all(data for data in members.values())
        assert all('/' not in name and name.endswith(('.md', '.tsv', '.pdf', '.xlsx')) for name in members)
        # Solo documentos explícitamente permitidos, nunca encargo/insumos/resultados/productores.
        assert not any(name.startswith(('encargo', 'insumos', 'resultados', 'dictamen', 'auditoria')) for name in members)
        archive = OUT / (successor + '.tar.gz')
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as target:
            for name, data in sorted(members.items()):
                info = tarfile.TarInfo(name)
                info.size, info.mtime, info.mode = len(data), 0, 0o644
                info.uid = info.gid = 0
                target.addfile(info, io.BytesIO(data))
        compressed = gzip.compress(buffer.getvalue(), mtime=0)
        if args.verifica:
            assert archive.read_bytes() == compressed, archive
        else:
            archive.write_bytes(compressed)
        with tarfile.open(archive) as check:
            assert set(check.getnames()) == set(members)
            for member in check.getmembers():
                assert member.isfile() and member.size > 0
                assert sha(check.extractfile(member).read()) == sha(members[member.name])
        manifests.append(dict(instrumento=inst, sucesor=successor, archivo=str(archive.relative_to(ROOT)),
                              sha256=sha(compressed), decision=group['decision'], estado=group['estado'],
                              pendientes=group['pendientes'], identidades=len(schemas),
                              miembros={name: dict(sha256=sha(data), bytes=len(data)) for name, data in sorted(members.items())}))
    assert {r['original'] for r in maps} == expected
    assert len(maps) == len(expected) == 312
    manifest_path = OUT / 'residuales-p4-manifestacion.json'
    map_path = OUT / 'residuales-p4-original-sucesor.tsv'
    manifest_data = (json.dumps(manifests, ensure_ascii=False, indent=2) + '\n').encode()
    map_data = tsv(maps, list(maps[0]))
    if args.verifica:
        assert manifest_path.read_bytes() == manifest_data
        assert map_path.read_bytes() == map_data
    else:
        manifest_path.write_bytes(manifest_data)
        map_path.write_bytes(map_data)
    print(json.dumps(dict(contenedores=4, identidades=len(maps), miembros_verificados=sum(len(m['miembros']) for m in manifests),
                          reproducible=True, recalculos=0), ensure_ascii=False))


if __name__ == '__main__':
    main()
