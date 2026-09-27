#!/usr/bin/env python3
"""Verificación y transporte C1 lote2; nunca recalcula ni revela objetivos."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / 'forense/validacion-independiente/catalogo-1'
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-preparacion-lote2'
SAFE = ['llave', 'calc', 'result_id', 'celda', 'instrumento', 'ola', 'conducta', 'eje', 'segmento', 'unidad', 'naturaleza_ic']
CACHE = {}


def sha(path):
    path = Path(path)
    stat = path.stat()
    key = (str(path.resolve()), stat.st_size, stat.st_mtime_ns)
    if key not in CACHE:
        digest = hashlib.sha256()
        with path.open('rb') as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b''):
                digest.update(chunk)
        CACHE[key] = digest.hexdigest()
    return CACHE[key]


def archive(path, expected_tar, expected_manifest):
    assert not Path(path).is_symlink(), 'Contenedor enlazado'
    assert sha(path) == expected_tar, f'Hash contenedor: {path.name}'
    with tarfile.open(path, 'r:gz') as tar:
        members = tar.getmembers()
        assert len(members) == len({m.name for m in members}), 'Miembro duplicado'
        assert all(m.isfile() and Path(m.name).name == m.name and m.name not in {'.', '..'} for m in members), 'Tar no plano o enlace'
        files = {m.name: tar.extractfile(m).read() for m in members}
    assert hashlib.sha256(files['manifiesto.json']).hexdigest() == expected_manifest, 'Hash manifiesto'
    manifest = json.loads(files['manifiesto.json'])
    assert set(files) == set(manifest['archivos']) | {'manifiesto.json'}, 'Miembros fuera de allowlist'
    for name, digest in manifest['archivos'].items():
        assert name.endswith(('.md', '.tsv', '.json', '.pdf', '.xlsx')), 'Tipo de entrada no autorizado'
        assert not re.search(r'medidor|resultados|esperados|procedencia|historial',name,re.I), 'Miembro prohibido'
        assert hashlib.sha256(files[name]).hexdigest() == digest, f'Hash miembro {name}'
    return files


def identities(files):
    reader = csv.DictReader(io.StringIO(files['estimandos.tsv'].decode()), delimiter='\t')
    assert reader.fieldnames == SAFE, 'Esquema de estimandos no seguro'
    rows = list(reader)
    assert len({r['llave'] for r in rows}) == len(rows), 'Llave repetida'
    return sorted(rows, key=lambda r: r['llave'])


def resolver():
    sys.path.insert(0, str(ROOT / 'tests'))
    import payload_resolver as payload
    payload.M.sha256_de = sha
    _, entries = payload.M.leer_manifiesto(str(ROOT/'data/manifiesto.yaml'))
    return lambda ident: payload.resolver_payload(ident, entradas=entries, root=str(ROOT))


def permission(item, reviewed):
    ident = item['id'].lower()
    if 'enif' in ident and '2024' in ident and 'bd_csv' in ident:
        return 'ZIP-ENIF2024-INTEGRAL-NO-AUTORIZADO'
    if 'endireh' in ident and '2006' in ident and ('cuestionario' in ident or 'tabulado' in ident):
        return 'DOCUMENTO-MIXTO-REQUIERE-EXTRACCION'
    if 'enut' in ident and '2024' in ident and 'bd_csv' in ident:
        return 'ENUT2024-CRUCE-RESERVADO-FP-bda6-02'
    if 'ensanut2024' in ident and 'stata' in ident and not reviewed.get(item['id'],{}).get('firma_apertura_especifica'):
        return 'ENSANUT2024-ULTIMA-OLA-RESERVADA-E6'
    if 'endireh' in ident and '2021' in ident and any(x in ident for x in ['bd_', 'bases_']):
        if not reviewed.get(item['id'],{}).get('firma_apertura_especifica'):
            return 'ENDIREH2021-ULTIMA-OLA-SIN-FIRMA-APERTURA'
    if ident not in reviewed:
        return 'SIN-REVISION-SEMANTICA-POR-INSUMO'
    if reviewed[ident].get('tipo')=='raw':
        if reviewed[ident].get('estado_acceso')!='ABIERTO' or not reviewed[ident].get('autorizacion'):
            return 'RAW-SIN-REFERENCIA-A-APERTURA-O-MISION-HISTORICA'
    if reviewed[ident].get('tipo')=='raw' and any(x in ident for x in ['envipe2026', 'envipe_2026', 'encig2025', 'encig_2025', 'enigh2024', 'enigh_2024', 'enut2024', 'enut_2024', 'enadid2023', 'enadid_2023']):
        if not reviewed[ident].get('autorizacion'):
            return 'OLA-RECIENTE-SIN-REFERENCIA-APERTURA'
    if reviewed[ident].get('tipo')=='raw' and (ident=='enco' or ident.startswith(('enco_', 'enco20'))):
        return 'RESERVA-ENCO'
    return ''


def document_matches(document, label, expected):
    if document.get('instrumento') and document.get('ola'):
        return (document['instrumento'].upper(), str(document['ola'])) in expected
    label = label.lower()
    return any(instrument.lower() in label and (year in label or re.search(re.escape(instrument.lower())+r'[_-]?'+re.escape(year[-2:])+r'[_-]',label)) for instrument,year in expected)


def verify(index, overrides=None):
    lotes = json.loads((ORIGINAL/'lotes.json').read_text())
    original = {r['paquete']: r for r in lotes if r['estado_preparacion']=='INCOMPLETO'}
    successors = index if isinstance(index, list) else index['sucesores']
    assert len(successors)==len(original) and {r.get('paquete_original', r['paquete']) for r in successors}==set(original), 'Partición lote2 incompleta o duplicada'
    assert not ({r.get('paquete_original', r['paquete']) for r in successors} & {r['paquete'] for r in lotes if r['estado_preparacion']=='DISPONIBLE'})
    resolve = resolver()
    report, deliveries = [], {}
    for successor in successors:
        pid = successor.get('paquete_original', successor['paquete'])
        old = original[pid]
        assert successor['calc']==old['calc'] and successor['estimadores']==old['estimadores'], 'Identidad índice cambiada'
        assert successor['original_sha256_contenedor']==old['sha256_contenedor'], 'Referencia original cambiada'
        initial = archive(ORIGINAL/'paquetes'/pid/old['archivo'], old['sha256_contenedor'], old['sha256'])
        path = ROOT/successor['ruta_tar'] if 'ruta_tar' in successor else BASE/successor['archivo']
        assert path.resolve().is_relative_to((BASE/'entradas').resolve()), 'Contenedor fuera del perímetro entradas'
        files = archive(path, successor['sha256_contenedor'], successor['sha256_manifiesto'])
        manifest = json.loads(files['manifiesto.json'])
        version = successor.get('version_entrada',2)
        assert isinstance(version,int) and version>=2
        assert manifest['paquete']==pid and manifest['version_entrada']==version, 'Versión o identidad manifiesto'
        assert identities(files)==identities(initial), f'Identidad cambiada: {pid}'
        assert len(identities(files))==old['estimadores']
        assert files['tolerancia.json']==initial['tolerancia.json'], 'Tolerancia previa modificada'
        reasons = list(successor['faltantes'])
        review = successor.get('revision_semantica', {})
        if overrides and pid in overrides:
            override = overrides[pid]
            assert override['sha256_contenedor']==successor['sha256_contenedor'] and override['sha256_manifiesto']==successor['sha256_manifiesto'], 'Revisión de otra versión'
            review = override['revision_semantica']
        if not isinstance(review, dict):
            review = {}
        reasons.extend(review.get('faltantes', []))
        if review.get('estado')!='REVISADO-SIN-FILTRACIONES':
            reasons.append('REVISION-SEMANTICA-NO-COMPLETA')
        documents = review.get('documentos', [])
        documented = {d['archivo'] for d in documents if d.get('estado')=='REVISADO-SIN-FILTRACIONES'}
        for name in files:
            if name.endswith(('.pdf', '.xlsx')) and name not in documented:
                reasons.append('DOCUMENTO-SIN-REVISION-SEMANTICA:'+name)
            if name.endswith('.pdf') and not files[name].startswith(b'%PDF-'):
                reasons.append('PDF-SIN-FIRMA-DE-FORMATO:'+name)
            if name.endswith('.xlsx') and not any(d.get('archivo')==name and d.get('tipo')=='fd' and d.get('estado')=='REVISADO-SIN-FILTRACIONES' for d in documents):
                reasons.append('XLSX-SOLO-DESCRIPTOR-HUMANO-REVISADO:'+name)
        reviewed = {r['id']:r for r in review.get('insumos', [])}
        for name, content in files.items():
            if name.endswith('.md') and re.search(r'medidor\.py|resultados\.json|N observado|resultados esperados\s*[:=]', content.decode(), re.I):
                reasons.append('FILTRACION-TEXTUAL:'+name)
        tolerance = json.loads(files['tolerancia.json'])
        if not isinstance(tolerance.get('abs'), (int,float)) or not math.isfinite(tolerance['abs']) or tolerance['abs']<0:
            reasons.append('TOLERANCIA-PREVIA-AUSENTE')
        raw = []
        availability = []
        for item in json.loads(files['insumos.json']):
            prohibited = permission(item, reviewed)
            if prohibited:
                reasons.append(item['id']+':'+prohibited)
                if prohibited != 'SIN-REVISION-SEMANTICA-POR-INSUMO':
                    availability.append(dict(id=item['id'], estado='NO-RESUELTO-POR-PERMISO', motivo=prohibited))
                    continue
                # Sin revisión humana no hay entrega; hash de documentos u olas
                # históricas no interpreta filas y sí comprueba disponibilidad.
                if re.search(r'(enif|enut|enigh).*2024|envipe.*2026|encig.*2025|enadid.*2023',item['id'].lower()) and not any(t in item['id'].lower() for t in ['cuestionario','_fd','descriptor','diseno','estructura']):
                    availability.append(dict(id=item['id'], estado='NO-RESUELTO-POR-PERMISO', motivo='RECIENTE-SIN-MAPA-APERTURA'))
                    continue
            rr = resolve(item['id'])
            availability.append(dict(id=item['id'], estado=rr['estado'], sha256_esperado=item['sha256'], sha256_actual=rr['sha256_actual']))
            if rr['estado']!='COINCIDE' or rr['sha256_actual']!=item['sha256']:
                reasons.append(item['id']+':'+rr['estado'])
                continue
            source = Path(rr['ruta_absoluta'])
            if not os.access(source, os.R_OK):
                reasons.append(item['id']+':SIN-PERMISO-LECTURA')
                continue
            raw.append((item, source))
        if not raw:
            reasons.append('SIN-INSUMOS-MATERIALIZABLES')
        available_ids = {item['id'] for item,_ in raw}
        expected = {(r['instrumento'].upper(),r['ola']) for r in identities(files)}
        doc_types = {r.get('tipo') for ident,r in reviewed.items() if ident in available_ids and (r.get('tipo')=='raw' or document_matches(r,ident,expected))}
        if 'raw' not in doc_types:
            reasons.append('MICRODATO-AUTORIZADO-NO-DISPONIBLE')
        doc_types.update(d.get('tipo') for d in documents if d.get('archivo') in documented and document_matches(d,d['archivo'],expected))
        for needed in ['cuestionario', 'fd']:
            if needed not in doc_types:
                reasons.append('DOCUMENTO-REQUERIDO-NO-DISPONIBLE:'+needed)
        ready = not reasons
        row = dict(paquete_original=pid, paquete_sucesor=successor['paquete']+f'-v{version}', version_entrada=version, calc=old['calc'], estimadores=old['estimadores'], estado='LISTO-PARA-SESION-NUEVA' if ready else 'NO-PREPARADO', impedimentos=sorted(set(reasons)), disponibilidad=availability, sha256_contenedor=successor['sha256_contenedor'], sha256_manifiesto=successor['sha256_manifiesto'], original_sha256_contenedor=old['sha256_contenedor'], original_sha256_manifiesto=old['sha256'])
        report.append(row)
        if ready:
            deliveries[pid] = (files, raw, row)
    return report, deliveries


def materialize(pid, destination, report, deliveries):
    assert pid in deliveries, 'Paquete bloqueado: materialización rechazada'
    requested = Path(destination).absolute()
    assert not any(p.is_symlink() for p in [requested, *requested.parents]), 'Destino con ancestro enlace'
    destination = requested.resolve()
    assert not destination.exists(), 'Destino debe ser nuevo'
    assert not destination.resolve().is_relative_to(ROOT.resolve()), 'Destino fuera del clon'
    files, raw, row = deliveries[pid]
    destination.mkdir(parents=True)
    (destination/'entrada').mkdir()
    (destination/'raw').mkdir()
    for name, content in files.items():
        (destination/'entrada'/name).write_bytes(content)
    receipt_inputs = []
    for item, source in raw:
        target = destination/'raw'/item['id']/Path(item['archivo']).name
        target.parent.mkdir()
        shutil.copyfile(source, target)
        assert sha(target)==item['sha256'], 'Copia raw no íntegra'
        receipt_inputs.append(dict(id=item['id'], archivo=str(target.relative_to(destination)), sha256=sha(target)))
    receipt = {**row, 'version':f"v{row.get('version_entrada',2)}", 'insumos':receipt_inputs, 'estado':'MATERIALIZADO-SIN-RECALCULO'}
    (destination/'recibo-entrada.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    assert not any(p.is_symlink() for p in destination.rglob('*')), 'Enlace en destino'
    return receipt


def container_tests(index):
    """Aislamiento por esquema de entrada; raw vacío no acredita entrega."""
    successors = index if isinstance(index,list) else index['sucesores']
    seen, checks = set(), []
    for successor in successors:
        path = ROOT/successor['ruta_tar'] if 'ruta_tar' in successor else BASE/successor['archivo']
        assert path.resolve().is_relative_to((BASE/'entradas').resolve())
        files = archive(path,successor['sha256_contenedor'],successor['sha256_manifiesto'])
        structure = []
        for name, content in files.items():
            suffix = Path(name).suffix
            if suffix=='.tsv':
                header = next(csv.reader(io.StringIO(content.decode()),delimiter='\t'))
                structure.append(name+':'+','.join(header))
            elif suffix=='.json':
                obj = json.loads(content)
                keys = sorted(obj) if isinstance(obj,dict) else sorted({k for row in obj if isinstance(row,dict) for k in row})
                structure.append(name+':'+','.join(keys))
            else:
                structure.append(name)
        schema = tuple(sorted(structure))
        if schema in seen:
            continue
        seen.add(schema)
        with tempfile.TemporaryDirectory(prefix='astra6-p3-aislamiento-esquema-') as tmp:
            folder = Path(tmp)
            (folder/'entrada').mkdir()
            (folder/'raw').mkdir()
            for name, content in files.items():
                (folder/'entrada'/name).write_bytes(content)
            (folder/'recibo-entrada.json').write_text(json.dumps({'paquete':successor['paquete'],'estado':'SOLO-PRUEBA-CONTENEDOR-RAW-VACIO'}))
            check = subprocess.run(['bash',str(ROOT/'tools/validacion/astra6_catalogo/astra6_lanza_catalogo.sh'),'--prueba',str(folder)],text=True,capture_output=True)
            checks.append(dict(paquete=successor['paquete'],esquema=schema,estado='SOLO-AISLAMIENTO-CONTENEDOR-RAW-VACIO',returncode=check.returncode,stdout=check.stdout,stderr=check.stderr))
    return checks


def check_materialized(destination, row):
    destination = Path(destination)
    assert not any(p.is_symlink() for p in [destination,*destination.parents]), 'Copia con ancestro enlace'
    assert not destination.resolve().is_relative_to(ROOT.resolve()), 'Copia dentro del clon'
    assert not any(p.is_symlink() for p in destination.rglob('*')), 'Enlace en copia'
    receipt = json.loads((destination/'recibo-entrada.json').read_text())
    for key in ['paquete_original','calc','sha256_manifiesto','sha256_contenedor','version_entrada']:
        assert receipt[key]==row[key], 'Recibo de otra versión'
    assert sha(destination/'entrada/manifiesto.json')==row['sha256_manifiesto']
    manifest = json.loads((destination/'entrada/manifiesto.json').read_text())
    assert {p.name for p in (destination/'entrada').iterdir()}==set(manifest['archivos'])|{'manifiesto.json'}
    for name,digest in manifest['archivos'].items():
        assert sha(destination/'entrada'/name)==digest
    expected_raw = set()
    inputs = {item['id']:item['sha256'] for item in json.loads((destination/'entrada/insumos.json').read_text())}
    assert len(receipt['insumos'])==len(inputs) and {item['id'] for item in receipt['insumos']}==set(inputs), 'Recibo insumos distinto de allowlist'
    for item in receipt['insumos']:
        path = destination/item['archivo']
        assert path.resolve().is_relative_to((destination/'raw').resolve()), 'Raw fuera de copia'
        assert sha(path)==item['sha256']==inputs[item['id']]
        expected_raw.add(path.resolve())
    assert {p.resolve() for p in (destination/'raw').rglob('*') if p.is_file()}==expected_raw, 'Raw extra'
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--indice', type=Path, default=BASE/'preparacion/p2/p2-sucesores.json')
    parser.add_argument('--salida', type=Path, default=BASE/'preparacion/p3/p3-verificacion.json')
    parser.add_argument('--materializa')
    parser.add_argument('--destino', type=Path)
    parser.add_argument('--materializa-listos', type=Path)
    parser.add_argument('--prueba-aislamiento', action='store_true')
    parser.add_argument('--lanzamientos', type=Path)
    parser.add_argument('--prueba-contenedores', action='store_true')
    parser.add_argument('--revision-p3', type=Path, default=BASE/'preparacion/p3/p3-revision-documentos.json')
    parser.add_argument('--verifica-materializados', type=Path)
    args = parser.parse_args()
    index_bytes = args.indice.read_bytes()
    index_digest = hashlib.sha256(index_bytes).hexdigest()
    index = json.loads(index_bytes)
    overrides = json.loads(args.revision_p3.read_text()) if args.revision_p3.exists() else None
    report, deliveries = verify(index,overrides)
    assert sha(args.indice)==index_digest, 'Índice cambió durante verificación; repetir sobre corte estable'
    output = dict(corte=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(), indice_sha256=index_digest, fuente_lotes_sha256=sha(ORIGINAL/'lotes.json'), paquetes=len(report), estimadores=sum(r['estimadores'] for r in report), listos=len(deliveries), no_preparados=len(report)-len(deliveries), resultados=report)
    if overrides:
        output['revision_p3_sha256'] = sha(args.revision_p3)
    args.salida.parent.mkdir(parents=True,exist_ok=True)
    args.salida.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    if args.materializa:
        assert args.destino, '--destino requerido'
        materialize(args.materializa,args.destino,report,deliveries)
    if args.materializa_listos:
        assert not args.materializa_listos.exists(), 'Raíz materialización debe ser nueva'
        existing = args.materializa_listos.absolute().parent
        while not existing.exists():
            existing = existing.parent
        required_bytes = sum(sum(len(b) for b in files.values())+sum(source.stat().st_size for _,source in raw) for files,raw,_ in deliveries.values())
        free_bytes = shutil.disk_usage(existing).free
        output['espacio'] = dict(bytes_requeridos=required_bytes,bytes_disponibles=free_bytes)
        assert required_bytes < free_bytes, 'Espacio insuficiente para materialización completa'
        checks = []
        schemas = set()
        for pid, (files, raw, row) in deliveries.items():
            dest = args.materializa_listos/pid
            receipt = materialize(pid,dest,report,deliveries)
            schema = tuple(sorted({p.suffix for _,p in raw}))
            if args.prueba_aislamiento and schema not in schemas:
                check = subprocess.run(['bash',str(ROOT/'tools/validacion/astra6_catalogo/astra6_lanza_catalogo.sh'),'--prueba',str(dest)],text=True,capture_output=True)
                checks.append(dict(paquete=pid, esquema=schema, returncode=check.returncode, stdout=check.stdout, stderr=check.stderr))
                schemas.add(schema)
            output.setdefault('materializados',[]).append(receipt)
        for row in report:
            if row['estado']=='NO-PREPARADO':
                try:
                    materialize(row['paquete_original'],args.materializa_listos/row['paquete_original'],report,deliveries)
                except AssertionError as error:
                    checks.append(dict(paquete=row['paquete_original'], rechazo_comprobado=str(error)))
                else:
                    raise AssertionError('Bloqueado materializado')
        output['pruebas'] = checks
        args.salida.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    if args.verifica_materializados:
        checks, schemas = [], set()
        output['materializados'] = []
        for row in report:
            pid = row['paquete_original']
            if pid not in deliveries:
                try:
                    materialize(pid,args.verifica_materializados/pid,report,deliveries)
                except AssertionError as error:
                    checks.append(dict(paquete=pid,rechazo_comprobado=str(error)))
                else:
                    raise AssertionError('Bloqueado materializado')
                continue
            folder = args.verifica_materializados/pid
            receipt = check_materialized(folder,row)
            output['materializados'].append(receipt)
            schema = tuple(sorted({Path(x['archivo']).suffix for x in receipt['insumos']}))
            if args.prueba_aislamiento and schema not in schemas:
                check = subprocess.run(['bash',str(ROOT/'tools/validacion/astra6_catalogo/astra6_lanza_catalogo.sh'),'--prueba',str(folder)],text=True,capture_output=True)
                checks.append(dict(paquete=pid,esquema=schema,returncode=check.returncode,stdout=check.stdout,stderr=check.stderr))
                schemas.add(schema)
        output['pruebas'] = checks
        args.salida.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    if args.lanzamientos:
        lines = ['# Lanzamientos lote2 · preparación no ciega\n',
                 'Generado por `tools/validacion/astra6_paquetes_lote2.py`; los estados acreditan preparación, nunca coincidencia numérica.\n',
                 'Prompt mínimo para un paquete LISTO: «Sesión nueva sin historial. Lee /entrada/encargo.md y manifiesto.json. Implementa únicamente desde las entradas autorizadas; congela código y números antes de revelación. Si falta contrato, informa sin adivinar.»\n',
                 '| Paquete original | Versión | Preparación | Acción concreta |\n|---|---|---|---|\n']
        for row in report:
            pid = row['paquete_original']
            if row['estado']=='LISTO-PARA-SESION-NUEVA':
                folder = args.verifica_materializados or args.materializa_listos
                if folder:
                    action = f'`bash tools/validacion/astra6_catalogo/astra6_lanza_catalogo.sh --prueba {folder/pid}`; sesión nueva con prompt mínimo'
                else:
                    action = f"`python3 tools/validacion/astra6_paquetes_lote2.py --materializa {pid} --destino /tmp/astra6-c1-v{row['version_entrada']}-{pid}`"
            else:
                text = ' '.join(row['impedimentos']).lower()
                if 'identidad' in text or 'ola2025' in text:
                    action = 'Resolver discordancia de ola/identidad por dictamen, preservando corte'
                elif 'reserv' in text or 'apertura' in text or 'bloqueado-por-acceso' in text:
                    action = 'Resolver autorización/proyección específica antes de materializar'
                elif 'tolerancia' in text:
                    action = 'Fijar criterio nuevo antes de comparación y tramitar adopción cuando corresponda'
                elif 'd-15' in text or 'd15' in text or 'metodo' in text or 'methodo' in text or 'no-recalculable' in text or 'spec' in text:
                    action = 'Completar contrato humano previo o dictaminar D-15 sin reconstruir desde código'
                elif 'fd' in text or 'cuestionario' in text or 'documento' in text:
                    action = 'Completar documento propio de instrumento/ola y revisión humana'
                else:
                    action = 'Resolver brecha concreta de preparación antes de sesión nueva'
                action += f' · [detalle](preparacion/p3/p3-verificacion.json) por `{pid}`'
            lines.append(f"| {pid} | v{row['version_entrada']} | {row['estado']} | {action} |\n")
        lines.append('\nNo se lanzaron validadores. Las entradas originales y los nueve paquetes de sesión01 permanecen intactos. El comparador anterior requiere adaptación explícita para las nuevas versiones antes de revelación: nunca sustituir SHA sucesor por SHA original. Los rechazos de materialización quedan comprobados en p3-verificacion.json.\n')
        args.lanzamientos.write_text('\n'.join(lines))
    if args.prueba_contenedores:
        output['aislamiento_contenedores'] = container_tests(index)
        args.salida.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['paquetes','estimadores','listos','no_preparados']},ensure_ascii=False))


if __name__=='__main__':
    main()
