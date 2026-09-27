#!/usr/bin/env python3
"""Deriva tablas y report desde juicios explícitos; verifica errores materiales, no decide dictámenes."""
import argparse, copy, csv, hashlib, io, json, re
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[4]
def read(name): return json.loads((D/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fail(msg):raise ValueError(msg)
def check(decisions,own,external,correspondences,template,dependency_override=None):
    meta=read('contrato.json');original=ROOT/meta['report_original'];catalog=ROOT/'canon/catalogo-del-mexicano-v1_2.tsv'
    if sha(original)!=meta['original_sha256']:fail('original cambió: releer cobertura')
    mapping=list(csv.DictReader((ROOT/meta['mapa']).open(),delimiter='\t'))
    expected={r['id_afirmacion'] for r in mapping if r['report']==meta['report_original']}
    parents={r['id'] for r in decisions if r['mapa_id']==r['id']}
    if parents!=expected:fail('cobertura de mapa incompleta')
    ids={r['id'] for r in decisions}
    if len(ids)!=len(decisions):fail('identidad duplicada')
    source_ids={r['id'] for r in read('fuentes.json')}
    refs=source_ids|{r['id'] for r in own}
    for r in decisions:
        if r['dictamen'] not in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}:fail('dictamen inválido')
        if not r['razon'] or not r.get('revision_manual'):fail('falta juicio/revisión manual')
        if r['dictamen']=='SIN-CIFRA' and not r['sin_cifra_razon']:fail('SIN-CIFRA sin motivo')
        if r['dictamen']=='ROMPE' and not r['evidencia']:fail('ROMPE sin evidencia refutatoria')
        if not set(r['evidencia'])<=refs:fail('evidencia inexistente')
    lines=original.read_text().splitlines()
    expected_lines={str(i) for i,l in enumerate(lines,1) if l.strip() and not l.startswith('#')}
    if set(correspondences)!=expected_lines:fail('pasajes fuera del mapa sin correspondencia')
    for l,rs in correspondences.items():
        if not rs or not set(rs)<=ids:fail('correspondencia no resuelta')
    catalog_rows=list(csv.DictReader(catalog.open(),delimiter='\t'))
    dependencies=read('dependencias.json') if dependency_override is None else dependency_override
    for r in own:
        path=ROOT/r['resultado_path']
        if sha(path)!=r['resultado_sha256']:fail('resultado sellado cambió')
        val=json.loads(path.read_text())
        for s in r['selector']:val=val[s]
        if val!=r['valor']:fail('cifra propia distinta de RESULT')
        matches=[x for x in catalog_rows if x['llave']==r['result_id']]
        if len(matches)!=1 or matches[0]['estado_adopcion']!='ADOPTADO':fail('cifra sin adopción vigente: revisar firma/objeto')
        if matches[0]['calc']!=r['calc'] or float(matches[0]['punto'])!=r['valor']:fail('llave/linaje catalogo incorrecto')
        if r['denominador']!='personas de20–54 años del hogar, alguna vez unidas en EDER2017, primer código no-cero LIBRE/DIRECTO/37, factor_per positivo; primera unión por historia de vida':fail('denominador EDER alterado')
        # Revisar nueva adjudicación material por identidad en recibo C1, no rango de fila.
        p=ROOT/'forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv'
        rows=[x for x in csv.DictReader(p.open(),delimiter='\t') if x['result_id']==r['result_id'] or x['calc']==r['calc']]
        if rows:fail('nueva dependencia C1: requiere adjudicación editorial')
        if any(r['result_id'] in x['llaves'] and x['consumida'] and x['veto'] for x in dependencies):fail('veto material consumido')
    src={r['id']:r for r in read('fuentes.json')}
    captures=read('capturas-numericas.json')
    for r in external:
        capture=captures.get(r['id'],'')
        if hashlib.sha256(capture.encode()).hexdigest()!=r['captura_sha256']:fail('captura externa alterada')
        match=re.search(r['selector_regex'],capture,re.S)
        if match is None or float(match.group(1).replace(' ',''))!=r['valor']:fail('cifra externa diferente del documento')
        if r['fuente'] not in src or not r['localizador'] or not r['selector_regex']:fail('cifra externa sin fuente/selector')
        if len(r['archivo_consulta_sha256'])!=64 or len(src[r['fuente']]['sha256_descarga'])!=64:fail('fuente externa sin hash')
        if r['id']=='E-NOV-TOTAL' and r['denominador']!='solteras15–24 alguna vez con pareja, nunca cohabitantes':fail('generalización de noviazgo')
        if r['id'] in {'E-LGBT-INDIGENA','E-LGBT-AFRO'} and not r['denominador'].startswith('poblaciónLGBTI+'):fail('denominador étnico invertido')
    placeholders=set(re.findall(r'\{\{([^{}]+)\}\}',template))
    if placeholders!={r['id'] for r in own+external if r['id'] not in {'E-NOV-EMOCIONAL','E-NOV-FISICA','E-NOV-SEXUAL'}}:fail('cifra sin placeholder/registro o registro activo sin uso')
    # El texto editorial usa marcadores para todas las cantidades propias/externas que afirma.
    # Detectar valores porcentuales añadidos directamente, no fechas, bibliografía ni cantidades citadas como error.
    if re.search(r'\d+(?:\.\d+)?\s*%|\b0\.\d+|\b(?:registraron|prevalencia|proporción|probabilidad|tasa)\s+(?:es\s+|de\s+)?\d',template):fail('cantidad afirmada sin registro')
    return meta

def render(template,own,external):
    for r in own:
        text=f"{r['valor']:.6f} como proporción ponderada de personas de20–54 años alguna vez unidas cuya primera unión fue libre (`{r['result_id']}`; `{r['calc']}`; ADOPTADO; sin IC consumido)"
        template=template.replace('{{'+r['id']+'}}',text)
    for r in external:
        text=f"{r['valor']:g}"+(' eventos registrados' if r['unidad']=='eventos' else '%')+f" [cifra externa `{r['id']}`]"
        template=template.replace('{{'+r['id']+'}}',text)
    return template

def artifacts():
    ds,own,ext,corr=read('decisiones.json'),read('cifras.json'),read('cifras-externas.json'),read('correspondencias.json')
    template=(D/'report-editorial.md').read_text();meta=check(ds,own,ext,corr,template)
    report=render(template,own,ext)
    buf=io.StringIO();cols=['id','mapa_id','localizador','afirmacion','dictamen','razon','sin_cifra_razon','evidencia','naturaleza','revision_manual'];w=csv.DictWriter(buf,fieldnames=cols,delimiter='\t',lineterminator='\n');w.writeheader()
    for row in ds:w.writerow({k:';'.join(row[k]) if isinstance(row[k],list) else row[k] for k in cols})
    counts=dict(Counter(r['dictamen'] for r in ds))
    summary={'report':meta['report'],'registros':len(ds),'mapa_filas':sum(r['id']==r['mapa_id'] for r in ds),'clausulas_descompuestas':sum(bool(r.get('descompone')) for r in ds),'fuera_mapa':sum(r['mapa_id']=='FUERA-DEL-MAPA' for r in ds),'pasajes':len(corr),'dictamenes':counts,'cifras':len(own),'cifras_externas':len(ext),'fuentes_leidas':len(read('fuentes.json')),'reglas':len(read('reglas.json')),'comando_generar':['python3',str(D.relative_to(ROOT)/'producir.py')],'comando_verificar':['python3',str(D.relative_to(ROOT)/'producir.py'),'--check'],'self_test':['python3',str(D.relative_to(ROOT)/'producir.py'),'--self-test'],'reservas':['sin eficacia aplicada ni causalidad acreditada','no validación independiente EDER en loteC1','cantidades y escalas no cotejadas retiradas por afirmación']}
    index='# Pareja · índice local reproducible\n\n'+f"Report: `{meta['report']}`. {len(ds)} registros editoriales, {summary['mapa_filas']} filas del mapa, {len(corr)} pasajes completos.\n\n"+'\n'.join(f'- {k}: {v}' for k,v in counts.items())+'\n\nLectura/juicio: `decisiones.json`, `correspondencias.json`, `contrato.json`. Evidencia: `fuentes.json`, `cifras.json`, `cifras-externas.json`. Revisión: `revision-dirigida.md`, `dependencias-c1.md`.\n\nRegenerar: `python3 '+str(D.relative_to(ROOT)/'producir.py')+'`; verificar `--check`; autopruebas `--self-test`.\n'
    return {ROOT/meta['report']:report,D/'afirmaciones.tsv':buf.getvalue(),D/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n',D/'indice-local.md':index,D/'coverage.json':json.dumps({'original_sha256':meta['original_sha256'],'pasajes':len(corr),'sin_cobertura':[],'mapa_filas':summary['mapa_filas'],'deduplicacion':'los hijos descomponen y los pasajes reiteran: no son tesis independientes adicionales'},ensure_ascii=False,indent=2)+'\n'}

def self_test():
    ds,own,ext,corr=read('decisiones.json'),read('cifras.json'),read('cifras-externas.json'),read('correspondencias.json');t=(D/'report-editorial.md').read_text();check(ds,own,ext,corr,t)
    cases=[]
    a=copy.deepcopy(ext);a[0]['valor']+=.1;cases.append(('cifra externa inventada',ds,own,a,corr,t))
    a=copy.deepcopy(own);a[0]['valor']+=.1;cases.append(('cifra diferente de sellado',ds,a,ext,corr,t))
    a=copy.deepcopy(own);a[0]['denominador']='población15+ en unión actual';cases.append(('primera unión convertida en actual',ds,a,ext,corr,t))
    a=copy.deepcopy(ext);next(x for x in a if x['id']=='E-NOV-TOTAL')['denominador']='todas las jóvenes';cases.append(('selección juvenil borrada',ds,own,a,corr,t))
    a=copy.deepcopy(ext);next(x for x in a if x['id']=='E-LGBT-INDIGENA')['denominador']='indígenas';cases.append(('condicional étnico invertido',ds,own,a,corr,t))
    a=copy.deepcopy(corr);a.pop(next(iter(a)));cases.append(('pasaje omitido',ds,own,ext,a,t))
    a=copy.deepcopy(ds);a.remove(next(r for r in a if r['id']==r['mapa_id']));cases.append(('fila mapa omitida',a,own,ext,corr,t))
    cases.append(('porcentaje sin registro',ds,own,ext,corr,t+'\nLa prevalencia es 45.5%.'))
    cases.append(('proporción sin registro',ds,own,ext,corr,t+'\nLa proporción es 0.333.'))
    cases.append(('conteo sin registro',ds,own,ext,corr,t+'\nSe registraron 6666 eventos.'))
    for name,a,b,c,d,e in cases:
        try:check(a,b,c,d,e)
        except ValueError:print('RECHAZA:',name)
        else:fail('autoprueba no detecta '+name)
    a=copy.deepcopy(read('dependencias.json'));a[0]['veto']=True
    try:check(ds,own,ext,corr,t,a)
    except ValueError:print('RECHAZA: veto consumido')
    else:fail('autoprueba no detecta veto')
    print('SELF-TEST OK: errores materiales rechazados')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:self_test();return
    files=artifacts()
    if a.check:
        for path,content in files.items():
            if not path.exists() or path.read_text()!=content:fail('artefacto atrasado: '+str(path))
        print('VERIFICA OK: cobertura, cifras, adopción, denominadores y dependencia C1')
    else:
        for path,content in files.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
        print('GENERA OK:',len(files),'artefactos')
if __name__=='__main__':main()
