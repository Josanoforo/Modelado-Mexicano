#!/usr/bin/env python3
"""Deriva edición y tabla; protege errores materiales: universo, fuente, veto y cifra huérfana."""
import argparse, collections, csv, hashlib, io, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
REL=str(HERE.relative_to(ROOT))

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())
def tsv(path):
    with path.open() as f: return list(csv.DictReader(f,delimiter='\t'))
def inputs():
    decisions=read(HERE/'decisiones.json'); sources=read(HERE/'fuentes.json')
    original=ROOT/decisions['report']
    assert sha(original)==decisions['report_sha256'],'original cambió: relectura editorial requerida'
    mapa=[r for r in tsv(ROOT/'canon/mapa-dominios-v1_1.tsv') if r['report']==decisions['report']]
    covered={r['mapa'] for r in decisions['decisiones'] if r['mapa']}
    assert covered=={r['id_afirmacion'] for r in mapa},'cobertura del mapa faltante/sobrante'
    ids=[r['id'] for r in decisions['decisiones']]; assert len(ids)==len(set(ids))
    for r in decisions['decisiones']:
        assert r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} and r['razon'] and r['evidencia']
        if r['dictamen']=='ROMPE': assert r['evidencia']=='LFT' and 'no obligatorio' in r['afirmacion']
    signatures={r['id']:r for r in tsv(ROOT/'forense/firmas-pendientes.tsv')}
    adoptions=tsv(ROOT/'data/corrida0/decisiones.tsv')
    fp='FP-260923-ASTRA5-U2-ENDIREH-6a2c-01'; ep='FP-260926-GEN2-COLA-COMPLETA-1-0d4a-01'
    assert signatures[fp]['estado']=='FIRMADA','revisar adopción ENDIREH'
    assert any(r['objeto']=='adopcion-astra:'+fp and 'adopta: SI' in r['decision'] for r in adoptions)
    assert signatures[ep]['estado']=='ABIERTA','cambió estado ENDISEG: revisar rótulo provisional'
    for r in adoptions:
        if ('ENDISEG' in str(r) or fp in str(r)) and 'vetar' in str(r).lower(): raise AssertionError('veto material: revisar producto')
    evid={}; values={}
    for key,calc,signature in [('PF','CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004',fp),('ENDISEG','CALC-ENDISEG-PISOS-2021-0001',ep)]:
        base=ROOT/'data/corrida0'/calc; seal=read(base/'sello.json')
        for p,h in seal.items(): assert sha(base/p)==h, f'sello alterado: {calc}/{p}'
        evid[key]={'calc':calc,'resultados_sha256':seal['resultados.json'],'firma':signature,'estado_firma':signatures[signature]['estado'],'adopcion':'ADOPTADO-DESCRIPTIVO' if key=='PF' else 'PROVISIONAL-NO-ADOPTADO','spec_sha256':seal['spec.yaml']}
        values[key]=read(base/'resultados.json')['resultados']
    pf=json.loads(values['PF']['RESULT-ENDIREH2021-PF-TABLA'])
    for q,window in [('PFVIDA','vida'),('PFRECIENTE','desde_octubre_2020')]:
        row=next(r for r in pf if (r['eje'],r['categoria'],r['ventana'])==('nacional','MX',window))
        assert row['estado']=='PUBLICABLE'
        evid[q]={**evid['PF'],'result':'RESULT-ENDIREH2021-PF-TABLA','selector':{'eje':'nacional','categoria':'MX','ventana':window},'denominador':'mujeres de 15+ A1/A2 con pareja actual y respuesta conocida','ventana':window,'p':row['p'],'ic95':row['ic95'],'n':row['n']}
    for q,stem in [('LGBT','LGBT'),('ORIENTACION','ORIENTACION-NO-HETEROSEXUAL'),('IDENTIDAD','IDENTIDAD-NO-CISGENERO')]:
        prefix=f'RESULT-ENDISEG-PISOS-2021-{stem}-2021-TOTAL-TODOS-'
        d=values['ENDISEG']; evid[q]={**evid['ENDISEG'],'result':prefix+'P','ic_results':[prefix+'IC-LO',prefix+'IC-HI'],'denominador':'persona seleccionada de 15+; diseño y respuesta admisibles; ENDISEG 2021','ventana':'2021','p':d[prefix+'P'],'ic95':[d[prefix+'IC-LO'],d[prefix+'IC-HI']],'n':d[prefix+'N']}
    for q,record in sources['cantidades_externas'].items(): evid[q]={**record,'tipo':'FUENTE-PRIMARIA-EXTERNA','fecha_lectura':sources['fecha_lectura']}
    return decisions,sources,mapa,evid

def qtext(q,e):
    if e.get('tipo')=='FUENTE-PRIMARIA-EXTERNA':
        return f"{e['valor']}% [Q:{q}; {e['fuente']}, {e['localizador']}; externa]" if e['unidad']=='porcentaje' else f"{e['valor']} {e['unidad']} [Q:{q}; {e['fuente']}, {e['localizador']}; norma externa]"
    lo,hi=e['ic95']; return f"{100*e['p']:.2f}% (IC95 {100*lo:.2f}–{100*hi:.2f}%) [Q:{q}; {e['result']}; {e['adopcion']}]"

def validate_report(report,evidence):
    # Cada afirmación cuantitativa publicada se vincula a su registro; fechas/ids no son cantidades.
    for match in re.finditer(r'\d+(?:\.\d+)?(?:%| (?:personas|mujeres|hombres|víctimas|casos|días|puntos|millones|billones|veces)\b)',report):
        end=report.find(']',match.end()); tail=report[match.end():end+1]
        assert end>=0 and end-match.end()<300 and re.search(r'\[Q:[A-Z]+;',tail), 'cifra porcentual sin evidencia'
    for q,e in evidence.items():
        if q in {'PF','ENDISEG'}: continue
        assert qtext(q,e) in report,f'cifra o procedencia alterada: {q}'
    for q in ('PFVIDA','PFRECIENTE'):
        assert evidence[q]['denominador']=='mujeres de 15+ A1/A2 con pareja actual y respuesta conocida','denominador ENDIREH incompatible'
        assert evidence[q]['selector']['ventana']==evidence[q]['ventana']
    for q in ('LGBT','ORIENTACION','IDENTIDAD'):
        assert evidence[q]['denominador']=='persona seleccionada de 15+; diseño y respuesta admisibles; ENDISEG 2021','denominador ENDISEG incompatible'
        assert evidence[q]['adopcion']=='PROVISIONAL-NO-ADOPTADO'
    assert 'no son normas' in report and 'no mide aceptación' in report.lower()
    return True

def products():
    decisions,sources,mapa,evidence=inputs(); rows=decisions['decisiones']; counts=dict(sorted(collections.Counter(r['dictamen'] for r in rows).items()))
    template=(HERE/'report-base.md').read_text()
    report=template.replace('{{CORTE}}',decisions['corte']).replace('{{N}}',str(len(rows))).replace('{{M}}',str(len(mapa)))
    report=report.replace('{{CONTEOS}}','Dictámenes por cláusula editorial (con solapamiento documentado): '+', '.join(f'{k}: {v}' for k,v in counts.items())+'.')
    for q in re.findall(r'\{\{Q:([A-Z]+)\}\}',report): report=report.replace('{{Q:'+q+'}}',qtext(q,evidence[q]))
    assert '{{' not in report; validate_report(report,evidence)
    stream=io.StringIO(); fields=['id','mapa','localizador','afirmacion','dictamen','evidencia','razon','original']; writer=csv.DictWriter(stream,fields,delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(rows)
    summary={'report':decisions['report'].replace('corpus/reports/','corpus/reports-v2/'),'mapa_filas':len(mapa),'afirmaciones':len(rows),'aclaracion':'Cláusulas editoriales; repeticiones y fuera mapa incluidos; no total de tesis independientes.','fuera_mapa':sum(not r['mapa'] for r in rows),'dictamenes':counts,'cifras':sum(1 for q in evidence if q not in {'PF','ENDISEG'}),'fuentes':sum(not r['leido'].startswith('NO:') for r in sources['fuentes']),'reglas':len(re.findall(r'\*\*GEN-R\d',report)),'comando_generar':['python3',REL+'/verifica.py'],'comando_verificar':['python3',REL+'/verifica.py','--check','--self-test'],'reservas':['ENDISEG: sellado no adoptado, firma ABIERTA; cifra provisional.','Coeficientes Nuñez y estudios Arciniega/Castillo/Wheeler no leídos; cantidades retiradas.','No microdatos, reservas, recalculo ni revisión independiente externa.','Mayor velocidad actitudinal, jerarquías demográficas e impactos de intervenciones no identificados.']}
    result={ROOT/summary['report']:report,HERE/'tabla-afirmaciones.tsv':stream.getvalue(),HERE/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n',HERE/'evidencia.json':json.dumps(evidence,ensure_ascii=False,indent=2)+'\n'}
    return result,summary,evidence,report

def self_test(report,evidence):
    from copy import deepcopy
    mutations=[('cifra huérfana',report+'\nLa prevalencia es 99%.\n',evidence),('denominador total por pareja',report,deepcopy(evidence)),('piso provisional adoptado',report,deepcopy(evidence))]
    mutations[1][2]['PFVIDA']['denominador']='todas las mujeres de 15+; cualquier ámbito'
    mutations[2][2]['LGBT']['adopcion']='ADOPTADO'
    mutations.append(('conteo textual sin evidencia',report+'\nSe observaron 777 personas.\n',evidence))
    caught=[]
    for label,text,e in mutations:
        try: validate_report(text,e)
        except AssertionError: caught.append(label)
        else: raise AssertionError('mutación aceptada: '+label)
    return caught

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    result,summary,evidence,report=products()
    for path,content in result.items():
        if args.check: assert path.exists() and path.read_text()==content,'diferencia de regeneración: '+str(path.relative_to(ROOT))
        else: path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    if args.self_test: print('AUTOPRUEBAS:',', '.join(self_test(report,evidence)))
    print(json.dumps({'estado':'VERIFICADO-SIN-DIFERENCIAS' if args.check else 'GENERADO','afirmaciones':summary['afirmaciones'],'mapa_filas':summary['mapa_filas'],'dictamenes':summary['dictamenes'],'cifras':summary['cifras']},ensure_ascii=False))
if __name__=='__main__': main()
