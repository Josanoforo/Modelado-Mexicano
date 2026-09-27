"""Inventario portable y hoja C2; nunca ejecuta run ni abre una R futura.

Preparar fija archivos del corte Git, verificar compara sin regenerarlos.
--replay ejecuta una sola vez el lote histórico en CAJA y archiva salida cruda.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time

import yaml

ROOT = Path(__file__).resolve().parents[3]
AREA_REL = 'forense/analisis/familias-2027/astra6-cierre-material-1'
AREA = ROOT / AREA_REL
INVENTARIO = AREA / 'inventario-portable.json'
INSTRUMENTOS = ('enif', 'encig', 'envipe')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def json_leer(p):
    return json.loads(p.read_text())


def escribe(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n')


def ruta(root, rel):
    parts = PurePosixPath(rel).parts
    if not parts or rel.startswith('/') or '..' in parts or '\\' in rel:
        raise ValueError('RUTA-AJENA: '+rel)
    p = root / rel
    if any(q.is_symlink() for q in [p, *p.parents] if q != root.parent):
        raise ValueError('ENLACE-AJENO: '+rel)
    if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError('ARCHIVO-AUSENTE-O-AJENO: '+rel)
    return p


def prepara():
    if INVENTARIO.exists():
        raise ValueError('INVENTARIO-YA-FIJADO; no regenerar testigo')
    corte = json_leer(AREA/'arranque.json')['corte']
    tracked = git('ls-tree', '-r', '--name-only', corte).decode().splitlines()
    selected = set()
    for rel in tracked:
        if (rel.startswith('tools/familias-2027/') or
            any(rel.startswith('forense/analisis/familias-2027/astra6-'+i+'/') for i in INSTRUMENTOS) or
            rel.startswith('forense/prereg-caja/FAMILIA-2027-') or
            (rel.startswith('data/corrida0/CALC-') and 'FAMILIA' in rel and '2027' in rel)):
            selected.add(rel)
    # Padres de pisos y sus testigos de ejecución: contenidos concretos, no libros vivos.
    parents = ('CALC-ENIF-0001', 'CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1',
               'CALC-ENCIG-0001', 'CALC-ENVIPE-0001', 'CALC-EVASION-NORMA-0001-v1_1')
    for cid in parents:
        selected.update(p for p in tracked if p.startswith('data/corrida0/'+cid+'/'))
    archivos = {p: sha(git('show', corte+':'+p)) for p in sorted(selected)
                if '__pycache__' not in PurePosixPath(p).parts and not p.endswith('.pyc')}
    manifest = yaml.safe_load((ROOT/'data/manifiesto.yaml').read_text())
    # Solo tres identidades históricas: no se enumeran ni abren olas reservadas.
    ids = {'enif_2024_enif_2024_bd_csv', 'encig25_base_datos_csv', 'envipe2025_csv'}
    raws = {}
    def busca(o):
        if isinstance(o, dict):
            if o.get('id') in ids:
                raws[o['id']] = {k:o[k] for k in ('archivo', 'sha256')}
            for v in o.values():
                busca(v)
        elif isinstance(o, list):
            for v in o:
                busca(v)
    busca(manifest)
    if set(raws) != ids:
        raise ValueError('IDENTIDAD-HISTORICA-AUSENTE')
    inv = {'corte': corte, 'estado':'SELLADO-INTERNAMENTE',
           'comprobante_envio':None, 'comprobante_ots':None,
           'relacion':'Sucesor aditivo; originales conservados. Excluye caches y mtime.',
           'archivos':archivos, 'raw_historicos':raws}
    escribe(INVENTARIO, inv)
    (AREA/'inventario-portable.sha256').write_text(sha(INVENTARIO.read_bytes())+'  inventario-portable.json\n')
    print('INVENTARIO FIJADO:', len(archivos), 'archivos de Git; raws por identidad')


def verifica(root=ROOT, inv=None, esperado=None):
    p = root/AREA_REL/'inventario-portable.json'
    raw = p.read_bytes()
    if esperado is None:
        # Ancla distinta del archivo que audita: blob del inventario entregado en Git.
        esperado = sha(git('show', 'HEAD:'+AREA_REL+'/inventario-portable.json'))
    if sha(raw) != esperado:
        raise ValueError('INVENTARIO-MUTADO')
    inv = json.loads(raw) if inv is None else inv
    for rel, expected in inv['archivos'].items():
        if sha(ruta(root, rel).read_bytes()) != expected:
            raise ValueError('HASH-DISCORDANTE: '+rel)
    # Identidad de la enmienda y drivers contra COMMIT-1, no autocertificación.
    prefix = 'forense/analisis/familias-2027/astra6-encig/'
    amendment = json_leer(root/(prefix+'enmienda-verificacion.json'))
    frozen = json_leer(root/(prefix+'commit-1-hashes.json'))
    for rel, item in amendment['archivos'].items():
        if sha(git('show', amendment['commit_1']+':'+rel)) != item['anterior']:
            raise ValueError('COMMIT-1-DISCORDANTE: '+rel)
        if frozen['archivos'][rel] != item['anterior'] or inv['archivos'][rel] != item['actual']:
            raise ValueError('ENMIENDA-DISCORDANTE: '+rel)
    if inv['comprobante_ots'] is not None or inv['comprobante_envio'] is not None:
        raise ValueError('ATESTACION-NO-ACREDITADA-EN-ESTE-CORTE')
    print('INVENTARIO: VERDE;', len(inv['archivos']), 'archivos efectivos, identidad COMMIT-1/enmienda intacta')
    from auditoria_sucesora import audita
    for rel in ('tools/familias-2027/enif/lector-futuro-serializacion-v2.py',
                'data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0002/medidor.py'):
        audita((root/rel).read_text(), inv['archivos'][rel])
    return inv


def resultados(cid):
    return json_leer(ROOT/'data/corrida0'/cid/'resultados.json')['resultados']


def hoja(inv):
    filas = []
    oro_id = 'CALC-FAMILIA-2027-ENIF-ORO-0002'
    oro = resultados(oro_id)
    soporte = {k: oro['RESULT-FAMILIA-ENIF-ORO-'+k.upper()] for k in ('n', 'estratos', 'upm', 'unicas')}
    support_ok = oro['RESULT-FAMILIA-ENIF-ORO-SOPORTE'] == 'SI'
    contract = 'tools/familias-2027/enif/contrato-futuro-serializacion-v2.yaml'
    for fam in ('AHORRO-FORMAL', 'HORIZONTE-AHORRO'):
        cid = 'CALC-FAMILIA-2027-ENIF-'+fam+'-EMISIONES-0001'
        rid = 'RESULT-FAMILIA-ENIF-'+fam+'-PISO-P'
        filas.append(dict(familia='ENIF-'+fam, instrumento='ENIF', ola='enif_2027',
            unidad='persona18+', p0=resultados(cid)[rid], result_id=rid, emision=cid,
            regla=yaml.safe_load((ROOT/contract).read_text())['parametros'],
            soporte_historico=soporte, soporte_acreditado=support_ok, contrato=contract,
            driver='tools/familias-2027/enif/lector-futuro-serializacion-v2.py',
            fecha=None, ventana='Seguimiento operativo; no ventana oficial de publicación',
            calendario='forense/analisis/familias-2027/astra6-enif/calendario.md',
            estado='CONDICIONAL', pendiente='COMMIT-3 cerrado; comparabilidad, autorización, auditoría sucesora propuesta'))
    prefix = ROOT/'forense/analisis/familias-2027/astra6-encig'
    gold = json_leer(prefix/'oro-evidencia.json')['familias']
    floors = json_leer(prefix/'pisos.json')['familias']
    contract = 'tools/familias-2027/encig/evaluacion-spec.yaml'
    rules = yaml.safe_load((ROOT/'data/corrida0/CALC-ENCIG-AUX-FAMILIAS-2027-0001/spec.yaml').read_text())
    for fam, piso in floors.items():
        f = gold[fam]
        ok = f['dictamen_soporte'] == 'ESTIMABLE'
        calendario = (prefix/'calendario.md').read_text()
        ventana = next(line.split('|')[4].strip() for line in calendario.splitlines()
                       if line.startswith('| ENCIG-'+fam+' |'))
        filas.append(dict(familia='ENCIG-'+fam, instrumento='ENCIG', ola='encig_2027',
            unidad='evento pago luz' if fam=='PAGO-DIGITAL' else 'persona18+ urbana100mil',
            p0=piso['p0'], result_id=piso['result_id'], emision='CALC-FAMILIA-2027-ENCIG-'+fam+'-0001',
            regla={'ruta':'data/corrida0/CALC-ENCIG-AUX-FAMILIAS-2027-0001/spec.yaml', 'parametros':rules.get('parametros')},
            soporte_historico=f['soporte'], soporte_acreditado=ok, contrato=contract,
            driver='tools/familias-2027/encig/evaluar.py', fecha=None,
            ventana={'descripcion':ventana,'fuente':'https://www.snieg.mx/Documentos/Gobierno/Programas/cteig_2025-2030.pdf',
                     'tipo':'VENTANA-ESPERADA-NO-FECHA-OFICIAL'},
            calendario='forense/analisis/familias-2027/astra6-encig/calendario.md',
            estado='CONDICIONAL' if ok else 'SUSPENDIDO/NO-ESTIMABLE',
            pendiente='COMMIT-3 cerrado; autorización de ola, reconocimiento de enmienda; conservar gate vigente'))
    prefix = ROOT/'forense/analisis/familias-2027/astra6-envipe'
    gold = json_leer(prefix/'diagnostico.json')['familias']
    cal = json_leer(prefix/'calendario.json')
    for fam, f in gold.items():
        cid = 'CALC-FAMILIA-2027-ENVIPE-'+fam.replace('_','-')
        e = json_leer(ROOT/'data/corrida0'/cid/'emision.json')
        filas.append(dict(familia='ENVIPE-'+fam.replace('_','-'), instrumento='ENVIPE', ola=e['ola_objetivo'],
            unidad='persona U4' if fam == 'DENUNCIA_U4' else 'delito', p0=e['p0'],
            result_id=e['fuente']['result'], emision=cid,
            regla={'ruta':'forense/analisis/familias-2027/astra6-envipe/auxiliares-spec.yaml',
                   'dictamen':'tools/familias-2027/envipe/medidor.py:dictamen'},
            soporte_historico=f['soporte'], soporte_acreditado=f['estimable'],
            contrato='forense/analisis/familias-2027/astra6-envipe/contrato.md',
            driver='tools/familias-2027/envipe/prospectiva.py', fecha=cal['fecha_confirmada'],
            ventana=cal['ventana_esperada'], calendario='forense/analisis/familias-2027/astra6-envipe/calendario.json',
            estado='CONDICIONAL', pendiente='COMMIT-3 cerrado; adaptar nominalmente y autorizar; precisar singleton contribuyente con firma'))
    for f in filas:
        f.update(estado_emision='SELLADO-INTERNAMENTE', atestacion='SELLADO-INTERNAMENTE',
                 comprobante_ots=inv['comprobante_ots'], contrato_sha256=inv['archivos'][f['contrato']],
                 driver_sha256=inv['archivos'][f['driver']], calendario_sha256=inv['archivos'][f['calendario']],
                 sello_sha256=inv['archivos']['data/corrida0/'+f['emision']+'/sello.json'])
    resumen = {'N':len(filas), 'M':len({f['ola'] for f in filas}),
               'K':sum(f['comprobante_ots'] is not None for f in filas),
               'soporte_historico_acreditado':sum(f['soporte_acreditado'] for f in filas),
               'activables_hoy':sum(f['estado']=='AUTORIZADA' for f in filas),
               'corte':inv['corte'], 'familias':filas}
    escribe(AREA/'hoja-comun.json', resumen)
    with (AREA/'hoja-comun.tsv').open('w') as out:
        fields = ['familia','ola','unidad','p0','result_id','estado','soporte_acreditado',
                  'contrato','contrato_sha256','driver','driver_sha256','calendario','estado_emision','atestacion','pendiente']
        writer = csv.DictWriter(out,fieldnames=fields,delimiter='\t',extrasaction='ignore')
        writer.writeheader();writer.writerows(filas)
    texto = (f"{resumen['N']} familias con emisiones congeladas para {resumen['M']} olas futuras; "
             f"{resumen['K']} con atestación externa verificada; fechas no confirmadas o ventanas esperadas. "
             f"{resumen['soporte_historico_acreditado']} con soporte histórico; "
             f"{resumen['activables_hoy']} autorizadas para apertura hoy.\n")
    (AREA/'producto.txt').write_text(texto)
    print(texto.strip())


def replay(inv):
    import numpy
    if numpy.__version__ != '2.3.5' or yaml.__version__ != '6.0.3':
        raise ValueError('DEPENDENCIAS-DISTINTAS; usar entorno aislado congelado')
    evidence = AREA/'replay-ejecutado.json'
    if evidence.exists():
        raise ValueError('REPLAY-YA-EJECUTADO; conservar primera evidencia')
    valida_raws(ROOT/'data/raw', inv['raw_historicos'])
    logdir = AREA/'logs';logdir.mkdir(exist_ok=True)
    commands = []
    calcs = ['CALC-FAMILIA-2027-ENIF-ORO-0002',
             'CALC-FAMILIA-2027-ENIF-AHORRO-FORMAL-EMISIONES-0001',
             'CALC-FAMILIA-2027-ENIF-HORIZONTE-AHORRO-EMISIONES-0001',
             'CALC-ENCIG-AUX-FAMILIAS-2027-0001',
             'CALC-FAMILIA-2027-ENCIG-PAGO-DIGITAL-0001',
             'CALC-FAMILIA-2027-ENCIG-SOLICITUD-MORDIDA-0001',
             'CALC-FAMILIA-2027-ENVIPE-DENUNCIA-U4',
             'CALC-FAMILIA-2027-ENVIPE-EVASION-NORMA']
    for cid in calcs:
        for action in ('preflight','verify'):
            commands.append(([sys.executable,'tools/corrida0.py',action,cid],
                             action+'-'+cid+'.txt'))
    # El cierre ENIF histórico es ejecutado y conserva su fallo de .pyc;
    # el verificador sucesor responde el cierre portable, sin fabricar caches.
    for inst in INSTRUMENTOS:
        commands.append(([sys.executable,'tools/familias-2027/'+inst+'/cierre.py','--verifica'], 'cierre-'+inst+'.txt'))
    records = []
    for cmd, name in commands:
        start = time.time()
        p = subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        raw = p.stdout+p.stderr
        (logdir/name).write_text(raw)
        rec = {'comando':cmd, 'exit_code':p.returncode, 'segundos':time.time()-start,
               'log':AREA_REL+'/logs/'+name, 'sha256':sha(raw.encode()),
               'alcance':'histórico abierto o emisión; nunca evaluación de R futura'}
        records.append(rec)
        print(name, 'exit='+str(p.returncode), flush=True)
    escribe(evidence, {'estado':'EJECUTADO', 'commit':git('rev-parse','HEAD').decode().strip(),
                       'entorno':'CAJA', 'numpy':numpy.__version__,'yaml':yaml.__version__,
                       'raws_verificados':inv['raw_historicos'], 'comandos':records})


def valida_raws(carpeta, entradas):
    for ident, item in entradas.items():
        if Path(item['archivo']).name != item['archivo']:
            raise ValueError('RUTA-INPUT-AJENA')
        path = carpeta/item['archivo']
        if sha(path.read_bytes()) != item['sha256']:
            raise ValueError('INPUT-HISTORICO-DISCORDANTE: '+ident)


def pruebas():
    proc = subprocess.run([sys.executable,'-m','pytest','-q',
                           'tools/familias-2027/cierre-material-1/test_cierre.py'],cwd=ROOT)
    if proc.returncode:
        raise ValueError('PRUEBAS-MATERIALES-FALLAN')


def preflight_final():
    if git('status','--porcelain').strip():
        raise ValueError('PREFLIGHT-FINAL-REQUIERE-COMMIT-LIMPIO')
    inv = verifica()
    calcs = sorted({PurePosixPath(p).parts[2] for p in inv['archivos']
                    if p.startswith('data/corrida0/') and p.endswith('/sello.json')
                    and '2027' in PurePosixPath(p).parts[2]})
    logs = []
    for cid in calcs:
        cmd = [sys.executable,'tools/corrida0.py','preflight',cid]
        p = subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        raw = p.stdout+p.stderr
        if 'working_tree_dirty' in raw or 'SELLO_COINCIDE' not in raw:
            raise ValueError('PREFLIGHT-NO-ACREDITADO: '+cid)
        logs.append((cid,raw,p.returncode))
    # Solo después de todos los comandos: el propio log no ensucia el siguiente.
    folder = AREA/'preflight-final';folder.mkdir(exist_ok=True)
    for cid,raw,code in logs:
        (folder/(cid+'.txt')).write_text(raw)
    escribe(folder/'resumen.json', {'commit':git('rev-parse','HEAD').decode().strip(),
            'estado':'EJECUTADO-LIMPIO; bloqueos por inmutabilidad o emisión sin ejecución, no preflight VERDE para run',
            'calcs':[{'calc':cid,'exit_code':code,'sha256':sha(raw.encode())} for cid,raw,code in logs]})


def verifica_replay():
    e = json_leer(AREA/'replay-ejecutado.json')
    for item in e['comandos']:
        if sha((ROOT/item['log']).read_bytes()) != item['sha256']:
            raise ValueError('LOG-REPLAY-MUTADO')
    for cid in ('CALC-FAMILIA-2027-ENIF-ORO-0002', 'CALC-ENCIG-AUX-FAMILIAS-2027-0001'):
        text = (AREA/'logs'/('verify-'+cid+'.txt')).read_text()
        if 'CONTEXTO=IDENTICO · RESULTADO=REPRODUCE' not in text:
            raise ValueError('ORO-NO-REPRODUCE: '+cid)
    text = (AREA/'logs/cierre-envipe.txt').read_text()
    if 'ORO-HISTORICO: REPRODUCE' not in text or 'CIERRE: PASS' not in text:
        raise ValueError('CIERRE-ENVIPE-NO-REPRODUCE')
    print('EVIDENCIA-HISTORICA: ACREDITADA; no atestación ni evaluación futura')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepara',action='store_true')
    p.add_argument('--verifica',action='store_true')
    p.add_argument('--hoja',action='store_true')
    p.add_argument('--replay',action='store_true')
    p.add_argument('--pruebas',action='store_true')
    p.add_argument('--preflight-final',action='store_true')
    p.add_argument('--evidencia',action='store_true')
    p.add_argument('--inventario-sha256',help='ancla entregada por mesa para paquete sin Git')
    a = p.parse_args()
    if a.prepara:
        prepara()
    if a.verifica or a.hoja or a.replay:
        inv = verifica(esperado=a.inventario_sha256)
        if a.hoja:
            hoja(inv)
        if a.replay:
            replay(inv)
    if a.pruebas:
        pruebas()
    if a.preflight_final:
        preflight_final()
    if a.evidencia:
        verifica_replay()
