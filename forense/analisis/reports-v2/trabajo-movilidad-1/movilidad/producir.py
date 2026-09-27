#!/usr/bin/env python3
"""Regeneración mecánica: no infiere dictámenes ni clasifica líneas por medibilidad.
Defectos materiales protegidos: firma abierta como adopción, Gini como movilidad,
condicional CEEY invertida, marginal MMSI como transición y cifra sin fuente.
"""
import argparse, copy, csv, hashlib, io, json, re, subprocess
from collections import Counter
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[4]
OUT=ROOT/'corpus/reports-v2/Mérito__Movilidad_Social_y_Desigualdad_en_México__Actualización_2025-2026.md'
CALC=ROOT/'data/corrida0/CALC-MMSI-PISOS-2016-0001'
SELECT=[
 ('Escolaridad superior · tonos A–E','EDUCACION-SUPERIOR-2016-TONO-TRAMO-A-E'),
 ('Escolaridad superior · tonos F–G','EDUCACION-SUPERIOR-2016-TONO-TRAMO-F-G'),
 ('Escolaridad superior · tonos H–K','EDUCACION-SUPERIOR-2016-TONO-TRAMO-H-K'),
 ('Escolaridad superior · autoadscripción indígena','EDUCACION-SUPERIOR-2016-ORIGEN-AUTOADSCRITO-INDIGENA'),
 ('Escolaridad superior · autoadscripción mestiza','EDUCACION-SUPERIOR-2016-ORIGEN-AUTOADSCRITO-MESTIZA'),
 ('Escolaridad superior · autoadscripción blanca','EDUCACION-SUPERIOR-2016-ORIGEN-AUTOADSCRITO-BLANCA'),
 ('Percibe mejora · tonos A–E','PERCIBE-MEJORA-SOCIOECONOMICA-2016-TONO-TRAMO-A-E'),
 ('Percibe mejora · tonos H–K','PERCIBE-MEJORA-SOCIOECONOMICA-2016-TONO-TRAMO-H-K'),
]
def read(name): return json.loads((BASE/name).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(d): return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def tab(rows):
 b=io.StringIO(); w=csv.DictWriter(b,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows); return b.getvalue()
def validate(editorial,coverage,ledger,ext,contract):
 assert sha(ROOT/contract['original'])==contract['original_sha256'], 'original cambiado'
 assert sha(ROOT/contract['mapa'])==contract['mapa_sha256'], 'mapa cambiado'
 maps={r['id_afirmacion'] for r in csv.DictReader(open(ROOT/contract['mapa']),delimiter='\t') if r['report']==contract['original']}
 assert {r['mapa_id'] for r in editorial if r['mapa_id']}==maps,'cobertura mapa incompleta'
 ids={r['id'] for r in editorial}; assert len(ids)==len(editorial),'id duplicado'
 assert all(r['dictamen'] in ['CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'] and r['razon'] and r['evidencia'] for r in editorial),'juicio incompleto'
 lines=(ROOT/contract['original']).read_text().splitlines()
 material={i for i,t in enumerate(lines,1) if t.strip() and not t.startswith('#')}
 assert {r['linea'] for r in coverage}==material,'cobertura original incompleta'
 for r in coverage:
  assert r['texto']==lines[r['linea']-1] and set(r['decisiones'])<=ids and r['decisiones'],'correspondencia sin respaldo'
 assert ids <= {v for r in coverage for v in r['decisiones']},'tesis sin localizador original'
 disputed=[r for r in editorial if r['mapa_id']=='ASTRA5-U0-MER-037']
 assert len(disputed)==1 and disputed[0]['dictamen']=='SIN-CIFRA' and 'discordantes' in disputed[0]['razon'],'condicionamiento disputado vendido firme'
 assert all(r['estimando'] not in ['P(pobreza|origenQ1)','P(origenQ1|pobreza)'] for r in ext),'condicional disputada en ledger'
 sources={r['id'] for r in read('fuentes.json') if not r.get('estado','').startswith('EXCLUIDA-RESERVA')}
 assert not any(r['evidencia']=='INEGI2025' for r in editorial),'fuente reservada como soporte'
 for r in ext:
  assert r['fuente'] in sources and r['universo'] and r['localizador'],'externa sin fuente/denominador'
  if r['clave'].startswith('q1_'): assert r['universo']=='origen quintil inferior recursos económicos' and r['unidad']=='personas25-64','transición con denominador incompatible'
  if r['clave'].startswith('gini_'): assert 'hogares' in r['universo'] and r['unidad']=='coeficiente Gini, escala0-1','Gini con denominador incompatible'
 for r in ledger:
  expected='NivEsc_Inf ∈1–7 válidos' if 'EDUCACION' in r['result_id'] else 'Per_SitEco ∈1,2,3 válidos'
  assert r['denominador']==expected,'denominador incompatible'
  assert r['estado']=='PROVISIONAL-NO-ADOPTADO' and r['firma_estado']=='ABIERTA','adopción sin firma'
  assert 'PERCIBE' not in r['result_id'] or r['estimando']=='mejora percibida, no transición quintil','marginal como movilidad quintil'
  assert 0<=r['valor']<=1 and 0<=r['ic_lo']<=r['ic_hi']<=1 and r['n']>0,'cantidad inválida'

def produce():
 contract=read('contrato.json'); ed=read('decisiones.json'); cover=read('cobertura.json'); ext=read('cifras-externas.json')
 seal=json.loads((CALC/'sello.json').read_text())
 for name,value in seal.items(): assert sha(CALC/name)==value,'sello no coincide: '+name
 fp=subprocess.run(['python3','tools/consulta.py','fp',contract['firma']],cwd=ROOT,text=True,capture_output=True)
 assert fp.returncode==0 and 'estado=ABIERTA' in fp.stdout,'firma MMSI cambió: actualizar juicio de adopción'
 # consulta.py primero; fallback por RESULT exacto solo si la vista carece de él.
 results=json.loads((CALC/'resultados.json').read_text())['resultados']
 own=[]; trace=[dict(tipo='fp',id=contract['firma'],salida=fp.stdout.strip(),codigo=fp.returncode)]
 calcquery=subprocess.run(['python3','tools/consulta.py','corrida',contract['calc']],cwd=ROOT,text=True,capture_output=True)
 trace.append(dict(tipo='corrida',id=contract['calc'],salida=calcquery.stdout.strip(),codigo=calcquery.returncode))
 for label,suffix in SELECT:
  stem='RESULT-MMSI-PISOS-2016-'+suffix
  rid=stem+'-P'; q=subprocess.run(['python3','tools/consulta.py','result',rid],cwd=ROOT,text=True,capture_output=True)
  trace.append(dict(tipo='result',id=rid,salida=q.stdout.strip(),codigo=q.returncode))
  assert q.returncode in (0,1),'consulta fallida'
  rr={kind:results[stem+'-'+kind] for kind in ['P','IC-LO','IC-HI','N']}
  own.append(dict(etiqueta=label,result_id=rid,calc=contract['calc'],valor=rr['P'],ic_lo=rr['IC-LO'],ic_hi=rr['IC-HI'],n=rr['N'],result_ic_lo=stem+'-IC-LO',result_ic_hi=stem+'-IC-HI',result_n=stem+'-N',unidad='proporción ponderada persona25-64',denominador='NivEsc_Inf ∈1–7 válidos' if 'EDUCACION' in suffix else 'Per_SitEco ∈1,2,3 válidos',estimando='educación superior NivEsc_Inf=7' if 'EDUCACION' in suffix else 'mejora percibida, no transición quintil',ola='MMSI2016',fuente='(a) primaria México',estado=contract['estado'],firma=contract['firma'],firma_estado='ABIERTA',hash_resultados=seal['resultados.json'],hash_spec=seal['spec.yaml'],registro='consulta.py + objeto sellado por identidad' if q.returncode==1 else 'consulta.py + cotejo sello',prospectividad='RETROSPECTIVA descriptiva'))
 validate(ed,cover,own,ext,contract)
 count=Counter(r['dictamen'] for r in ed)
 counts=dict(registros_editoriales=len(ed),filas_mapa=len({r['mapa_id'] for r in ed if r['mapa_id']}),registros_fuera_mapa=sum(not r['mapa_id'] for r in ed),lineas_materiales_cubiertas=len(cover),tesis_editoriales_por_clausula=len(ed),resultados_punto_usados=len(own),resultados_con_ic_n=len(own)*4,cifras_externas=len(ext),reglas=len(read('reglas.json')),**count)
 template=(BASE/'report-editorial.md').read_text()
 assert not re.search(r'\d+(?:[.,]\d+)?\s*(?:%|pesos|millones|centavos)',template),'cifra factual cruda: usar ledger'
 lookup={r['clave']:r for r in ext}
 def replace(m):
  assert m.group(1) in lookup,'cifra sin evidencia'; return lookup[m.group(1)]['valor']
 report=re.sub(r'\|CIFRA:([^|]+)\|',replace,template)
 head='| Segmento y estimando | Punto | IC de diseño | n válido | Estado |\n|---|---:|---:|---:|---|\n'
 body=''.join(f"| {r['etiqueta']} | {100*r['valor']:.2f}% | [{100*r['ic_lo']:.2f}, {100*r['ic_hi']:.2f}]% | {r['n']} | PROVISIONAL |\n" for r in own)
 report=report.replace('|TABLA_MMSI|',head+body)
 rules='| Regla | SI → ENTONCES y driver | Aplicación, falsador y límite |\n|---|---|---|\n'
 for r in read('reglas.json'):
  rules+=f"| {r['id']} · {r['estado']} | {r['si']} → {r['entonces']}. Porque: {r['porque']}. Tier descriptivo: {r['tier_frecuencia']}; mecanismo: {r['tier_mecanismo']}. | Consumidor: {r['consumidor']}. Condición: {r['aplicabilidad']}. Falsador: {r['falsador']}. Límite: {r['limitacion']}. |\n"
 report=report.replace('|REGLAS|',rules)
 c='; '.join(f'{k}: {v}' for k,v in counts.items())
 report=report.replace('|CONTEOS|',c+'. Estos son registros de cláusulas/coverage; no un censo de tesis universales independientes.')
 assert '|CIFRA:' not in report,'placeholder no resuelto'
 summary=dict(pieza='movilidad',report=str(OUT.relative_to(ROOT)),decisiones=str((BASE/'decisiones.json').relative_to(ROOT)),cifras=str((BASE/'cifras.json').relative_to(ROOT)),reglas=str((BASE/'reglas.json').relative_to(ROOT)),comando_verificar=['python3',str((BASE/'producir.py').relative_to(ROOT)),'--check','--self-test'],comando_producir=['python3',str((BASE/'producir.py').relative_to(ROOT)),'--write'],conteos=counts,revision_humana='SOLICITADA, NO CONCEDIDA',exposicion_reserva=contract.get('exposicion_reserva'),reservas=['MMSI provisional sin adopción','condicionamiento CEEY pobreza disputado; sin cifra en ambas direcciones','Exposición pública ENIGH2024 declarada, fuente excluida, adjudicación pendiente'])
 generated={OUT:report,BASE/'decisiones.tsv':tab(ed),BASE/'cifras.json':dump(own),BASE/'trazas-consulta.json':dump(trace),BASE/'conteos.json':dump(counts),BASE/'resumen.json':dump(summary)}
 return generated,(ed,cover,own,ext,contract)

def selftest(args):
 ed,cover,own,ext,contract=args
 cases=[]
 # Errores de evidencia, denominador, cobertura y condicional con impacto real.
 bad=copy.deepcopy(own); bad[0]['denominador']='personas ocupadas';cases.append((ed,cover,bad,ext,contract))
 bad=copy.deepcopy(own); bad[0]['estado']='ADOPTADO';cases.append((ed,cover,bad,ext,contract))
 bad=copy.deepcopy(ed); next(r for r in bad if r['mapa_id']=='ASTRA5-U0-MER-037')['dictamen']='CONFIRMA';cases.append((bad,cover,own,ext,contract))
 cases.append((ed,cover[:-1],own,ext,contract))
 for direction in ['P(pobreza|origenQ1)','P(origenQ1|pobreza)']:
  bad=copy.deepcopy(ext);bad[0]['estimando']=direction;cases.append((ed,cover,own,bad,contract))
 bad=copy.deepcopy(ext);bad[0]['fuente']='SIN-FUENTE';cases.append((ed,cover,own,bad,contract))
 bad=copy.deepcopy(ext);bad[0]['fuente']='INEGI2025';cases.append((ed,cover,own,bad,contract))
 bad=copy.deepcopy(ext);bad[0]['universo']='pobreza actual';cases.append((ed,cover,own,bad,contract))
 for case in cases:
  try: validate(*case)
  except AssertionError: pass
  else: raise AssertionError('mutación material no detectada')
 print('AUTOPRUEBAS materiales:',len(cases),'rechazadas; no validación independiente')

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 assert a.write != a.check,'elegir --write o --check'
 generated,args=produce()
 if a.self_test: selftest(args)
 for path,content in generated.items():
  if a.write: path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
  else: assert path.exists() and path.read_text()==content,'diferencia regeneración '+str(path)
 print('REGENERA-SIN-DIFERENCIAS' if a.check else 'PRODUCIDO',len(generated),'artefactos; juicios explícitos, no concedidos por humano')
if __name__=='__main__':main()
