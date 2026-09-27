"""Proyecta identidades y metadatos; no abre esperados ni recalcula estimadores."""
import collections
import csv
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PREP = 'forense/validacion-independiente/catalogo-1-preparacion-lote2'
csv.field_size_limit(10000000)


def read(name, fields):
    with (ROOT / name).open() as source:
        reader = csv.DictReader((line for line in source if not line.startswith('#')), delimiter='\t')
        return [{key: row.get(key, '') for key in fields} for row in reader]


def write(name, fields, rows):
    with (OUT / name).open('w') as target:
        writer = csv.DictWriter(target, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    deliveries = read(PREP + '/astra6-c1-lote2-entrega-59.tsv', ['paquete_original', 'paquete_sucesor', 'calc', 'estimadores', 'estado_preparacion', 'sha256_contenedor', 'sha256_manifiesto'])
    deliveries = [row for row in deliveries if row['estado_preparacion'] == 'LISTO-PARA-SESION-NUEVA']
    historical = read('forense/validacion-independiente/catalogo-1/universo.tsv', ['llave','calc','result_id','instrumento','ola','firma_fp','estado_adopcion','paquete'])
    current = read('canon/catalogo-del-mexicano-v1_2.tsv', ['llave','calc','result_id','instrumento','ola','firma_fp','estado_adopcion','reserva'])
    assert len(historical) == 36143
    assert len({row['llave'] for row in historical}) == len(historical)
    assert len({row['llave'] for row in current}) == len(current)
    overlay = {row['llave']: row for row in current}
    excluded = {row['llave']:row for row in read('forense/analisis/catalogo/v1_2/excluidos-v1_2.tsv',['llave','calc','causa','firma','nota'])}
    uses = read('data/corrida0/usos.tsv', ['resultado_id','consumidor','tipo_uso','activo','aptitud_uso','motivo_aptitud','camino_linaje','corrida0_resultado_id'])
    groups, identities, inputs, consumers = [], [], [], []
    for entry in deliveries:
        package, calc = entry['paquete_original'], entry['calc']
        selected = [row for row in historical if row['calc'] == calc]
        assert len(selected) == int(entry['estimadores'])
        version = entry['paquete_sucesor'].rsplit('-', 1)[1]
        tar = ROOT / PREP / 'entradas' / package / f'{package}-entradas-{version}.tar.gz'
        assert hashlib.sha256(tar.read_bytes()).hexdigest() == entry['sha256_contenedor']
        with tarfile.open(tar) as archive:
            minimal = list(csv.DictReader(archive.extractfile('estimandos.tsv').read().decode().splitlines(),delimiter='\t'))
            manifest_bytes = archive.extractfile('manifiesto.json').read()
            assert hashlib.sha256(manifest_bytes).hexdigest() == entry['sha256_manifiesto']
            authorized = json.load(archive.extractfile('insumos.json'))
        assert {row['llave'] for row in minimal} == {row['llave'] for row in selected}
        for item in authorized:
            inputs.append(dict(paquete=package, insumo=item['id'], sha256=item['sha256'], archivo=item['archivo'], tipo='MICRODATO' if item['archivo'].endswith('.zip') else 'DOCUMENTO'))
        result_ids = {row['result_id'] for row in selected}
        matched = [row for row in uses if row['resultado_id'] in result_ids or row['corrida0_resultado_id'] in result_ids or any(result in row['camino_linaje'] for result in result_ids)]
        for use in matched:
            consumers.append(dict(paquete=package, **use))
        groups.append(dict(paquete=package, sucesor=entry['paquete_sucesor'],calc=calc,identidades=len(selected),vigentes=sum(row['llave'] in overlay for row in selected),excluidas=sum(row['llave'] in excluded for row in selected),instrumentos=';'.join(sorted({row['instrumento'] for row in selected})),olas=';'.join(sorted({row['ola'] for row in selected})),consumidores=len(matched),estado='NO-EVALUADO'))
        for row in selected:
            excluded_row = excluded.get(row['llave'], {})
            identities.append(dict(**row, sucesor=entry['paquete_sucesor'], vigente=str(row['llave'] in overlay),causa_exclusion=excluded_row.get('causa',''),firma_exclusion=excluded_row.get('firma',''),estado='NO-EVALUADO',comparacion_punto='PENDIENTE',comparacion_ic='PENDIENTE',publicabilidad='PENDIENTE',spec='PENDIENTE'))
    assert len(deliveries)==11 and len(identities)==425
    assert len({row['llave'] for row in identities})==425
    write('paquetes-base.tsv', list(groups[0]), groups)
    write('identidades-base.tsv', list(identities[0]), identities)
    write('insumos-dependencia.tsv', list(inputs[0]), inputs)
    write('consumidores-linaje.tsv', ['paquete','resultado_id','consumidor','tipo_uso','activo','aptitud_uso','motivo_aptitud','camino_linaje','corrida0_resultado_id'], consumers)
    shared = []
    by_hash = collections.defaultdict(set)
    for item in inputs:
        if item['tipo']=='MICRODATO': by_hash[item['sha256']].add(item['paquete'])
    for digest, packages in sorted(by_hash.items()):
        shared.append(dict(sha256=digest,paquetes=';'.join(sorted(packages)),n_paquetes=len(packages),interpretacion='MUESTRA-COMPARTIDA' if len(packages)>1 else 'FUENTE-UNICA-EN-LOTE'))
    write('olas-fuentes.tsv',list(shared[0]),shared)
    selected_keys={row['llave'] for row in identities}
    summary=dict(corte=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),estado='PREPARACION-NO-CIEGA; SIN-RECALCULO',historico_denominador=len(historical),overlay_denominador=len(current),seleccion_denominador=len(identities),seleccion_en_overlay=len(selected_keys & overlay.keys()),seleccion_fuera_overlay=len(selected_keys-overlay.keys()),overlay_nuevas=len(overlay.keys()-{row['llave'] for row in historical}),paquetes=len(deliveries),raw_distintos=len(shared),grupos_raw_compartidos=sum(row['n_paquetes']>1 for row in shared),validacion_ciega_lote2=0,consumidores_filas=len(consumers),catalogo='canon/catalogo-del-mexicano-v1_2.tsv',fuentes_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['forense/validacion-independiente/catalogo-1/universo.tsv','canon/catalogo-del-mexicano-v1_2.tsv',PREP+'/astra6-c1-lote2-entrega-59.tsv','data/corrida0/usos.tsv']})
    (OUT/'cobertura-base.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__': main()
