#!/usr/bin/env python3
"""Deriva productos de decisiones explícitas; protege la confusión EDR conteo/tasa y cifras sin fuente."""
import argparse, copy, csv, hashlib, io, json, re
from collections import Counter
from pathlib import Path
B = Path(__file__).resolve().parent
ROOT = B.parents[4]
REPORT = 'corpus/reports-v2/Salud_Mental_en_México__Prevalencia__Estigma_y_la_Brecha_entre_Necesidad_y_Atención.md'

def read(name):
    return json.loads((B/name).read_text())

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def tsv(rows, fields):
    out=io.StringIO(); w=csv.DictWriter(out,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader()
    for row in rows:
        w.writerow({f:(';'.join(row[f]) if isinstance(row.get(f),list) else row.get(f,'NO-APLICA')) for f in fields})
    return out.getvalue()

def validate(rows, q, cov, sources):
    meta=read('metadatos.json')
    assert digest(ROOT/meta['original'])==meta['original_sha256'],'original cambiado'
    assert digest(ROOT/meta['mapa'])==meta['mapa_sha256'],'mapa cambiado: reevaluar correspondencias'
    with (ROOT/meta['mapa']).open() as f:
        mids={r['id_afirmacion'] for r in csv.DictReader(f,delimiter='\t') if r['report']==meta['original']}
    assert {r['mapa_id'] for r in rows if r['mapa_id']}==mids,'mapa sin cobertura'
    ids={r['id'] for r in rows}; assert len(ids)==len(rows),'ids duplicados'
    source_ids={s['id'] for s in sources}
    for r in rows:
        assert r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} and r['razon'],'dictamen sin juicio'
        assert not r['evidencia'] or r['evidencia'] in source_ids,'fuente inexistente'
        if r['dictamen']=='ROMPE':
            assert r['id'] in {'SAL-X47','SAL-X67'} and r['evidencia']=='DEMORA','ROMPE sin contradicción primaria'
    original=(ROOT/meta['original']).read_text().splitlines()
    assert len(cov)==len(original),'línea sin cobertura'
    for i,(line,c) in enumerate(zip(original,cov),1):
        assert c['linea']==i and c['sha256']==hashlib.sha256(line.encode()).hexdigest(),'cobertura distinta del original'
        assert c['razon'] and c['estado'] in {'CORRESPONDENCIA','EXCLUSION-EDITORIAL','ESTRUCTURA'}
        assert all(x in ids for x in c['decisiones']),'cobertura huérfana'
        if c['estado']=='CORRESPONDENCIA':assert c['decisiones'],'afirmación sin decisión'
    contracts=read('contratos-cifras.json')
    assert len(q)==len(contracts),'cantidad sin contrato'
    for c in q:
        assert c==contracts[c['id']],'cifra/unidad/denominador sin evidencia o contrato incompatible'
        assert c['fuente'] in source_ids
        if c['tipo']=='RESULT':
            assert c['unidad']=='conteo defunciones' and c['denominador']=='no aplica: conteo, no tasa poblacional','denominador EDR incompatible'
            assert c['estado']=='PROVISIONAL-NO-ADOPTADO','EDR sin firma no piso adoptado'
            p=ROOT/'data/corrida0'/c['calc']/'resultados.json'
            assert digest(p)==c['hash_resultados'],'sello resultados distinto'
            seal=json.loads((p.parent/'sello.json').read_text()); assert seal['resultados.json']==c['hash_resultados']
            execution=json.loads((p.parent/'ejecucion.json').read_text())
            assert execution['etiquetas']['cuenta_gen2']=='SI' and execution['etiquetas']['adopta']=='NO'
            with (ROOT/'forense/firmas-pendientes.tsv').open() as f:
                fp=next(r for r in csv.DictReader(f,delimiter='\t') if r['id']==meta['firma_edr'])
            assert fp['estado']=='ABIERTA','adopción cambió: revisar report'
            with (ROOT/'data/corrida0/decisiones.tsv').open() as f:
                decisions=[r for r in csv.DictReader(f,delimiter='\t') if c['calc'] in r.get('objeto','')]
            assert not any('vetar' in r.get('decision','').lower() for r in decisions),'RESULT vetado'
            with (ROOT/'canon/catalogo-del-mexicano-v1_2.tsv').open() as f:
                assert not any(c['calc'] in str(r) for r in csv.DictReader(f,delimiter='\t')),'catálogo cambió: revisar autoridad'
        else:
            assert c['tipo']=='EXTERNA-PRIMARIA' and c['estado']=='PUBLICADA-NO-RESULT'
    return meta

def render(q,meta):
    values={'CORTE':meta['corte'],'FIRMA':meta['firma_edr'],'HASH_EDR':next(c['hash_resultados'] for c in q if c['tipo']=='RESULT')}
    resolved=[]
    for c in q:
        c=copy.deepcopy(c)
        if c['tipo']=='RESULT':
            p=ROOT/'data/corrida0'/c['calc']/'resultados.json'
            c['valor']=str(json.loads(p.read_text())['resultados'][c['result']])
        values[c['id']]=c['valor'];resolved.append(c)
    template=(B/'report.base.md').read_text()
    assert not re.search(r'\b\d+(?:[.,]\d+)?%|\$\s*\d',template),'cifra literal en plantilla sin registro de evidencia'
    for key,value in values.items():template=template.replace('{{'+key+'}}',value)
    assert '{{' not in template,'token sin evidencia'
    return template,resolved

def trace_text(candidate,expected,q):
    # Párrafos cuantitativos tienen contrato con fuente/unidad/denominador. Una cifra textual
    # añadida o la sustitución de un denominador no queda autorizada por contener un RESULT.
    known={c.get('valor') for c in q if c.get('valor')}
    for percentage in re.findall(r'\b\d+(?:[.,]\d+)?%',candidate):
        assert percentage in known,'cifra textual sin evidencia: '+percentage
    assert candidate==expected,'afirmación textual o denominador difiere del producto trazado'

def outputs():
    rows,q,cov,sources=(read(x) for x in ['decisiones.json','cifras.json','cobertura.json','fuentes.json'])
    meta=validate(rows,q,cov,sources);report,resolved=render(q,meta);trace_text(report,report,resolved)
    counts=dict(Counter(r['dictamen'] for r in rows))
    command=['python3',str(B.relative_to(ROOT)/'verifica.py')]
    summary={'report':REPORT,'mapa_filas':len({r['mapa_id'] for r in rows if r['mapa_id']}),'afirmaciones':len(rows),'afirmaciones_aclaracion':'Registros editoriales: filas mapa compuestas, cláusulas divididas y fuera mapa; no tesis únicas. Correspondencias de reiteraciones en cobertura.','dictamenes':counts,'cifras':len(q),'fuentes':len(sources),'reglas':3,'comando_generar':command,'comando_verificar':command+['--check','--self-test'],'cobertura_lineas':len(cov),'reservas':['EDR PROVISIONAL firma ABIERTA, vista reciente ausente; no tasa ni contraste tasa original','ENEP resumen primario, no foto actual','DOF mandato y transitorio verificados; no ejecución ni presupuesto futuro total','Migración lectura parcial, no cantidades firmes ni causalidad','Literatura no leída retirada; no adquisición microdato','Revisión editorial POR EJECUTOR; revisión externa solicitada por responsable']}
    generated={ROOT/REPORT:report,B/'tabla.tsv':tsv(rows,['id','mapa_id','localizador','afirmacion','dictamen','evidencia','razon','origen','naturaleza','revision_dirigida']),B/'cobertura.tsv':tsv(cov,['linea','sha256','estado','decisiones','razon']),B/'cifras.tsv':tsv(resolved,['id','tipo','fuente','valor','unidad','denominador','periodo','estado','calc','result','hash_resultados']),B/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
    return generated,report,resolved,(rows,q,cov,sources)

def self_test(report,resolved,state):
    rows,q,cov,sources=state
    cases=[]
    cases.append(('cifra inventada en texto',lambda:trace_text(report+'\nLa prevalencia mexicana es 99.987%.\n',report,resolved)))
    cases.append(('conteo como tasa textual',lambda:trace_text(report.replace('defunciones con causa CIE','casos por cada cien mil habitantes con causa CIE'),report,resolved)))
    bad=copy.deepcopy(q);next(c for c in bad if c['tipo']=='RESULT')['denominador']='población residente total'
    cases.append(('denominador EDR incompatible',lambda:validate(rows,bad,cov,sources)))
    adopted=copy.deepcopy(q);next(c for c in adopted if c['tipo']=='RESULT')['estado']='ADOPTADO'
    cases.append(('piso adoptado sin firma',lambda:validate(rows,adopted,cov,sources)))
    missing=rows[1:];cases.append(('mapa sin cobertura',lambda:validate(missing,q,cov,sources)))
    for name,fn in cases:
        try:fn()
        except AssertionError:print('SELF-TEST atrapado:',name)
        else:raise AssertionError('mutación no detectada: '+name)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');args=p.parse_args()
    generated,report,resolved,state=outputs()
    if args.self_test:self_test(report,resolved,state)
    for path,content in generated.items():
        if args.check:
            assert path.exists() and path.read_text()==content,'regeneración con diferencias: '+str(path)
            if path==ROOT/REPORT:trace_text(path.read_text(),report,resolved)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print(('VERIFICADO SIN DIFERENCIAS' if args.check else 'GENERADO'),len(state[0]),'registros editoriales; cobertura original completa; revisión POR EJECUTOR')
