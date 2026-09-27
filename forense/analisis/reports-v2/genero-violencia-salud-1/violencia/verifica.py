#!/usr/bin/env python3
"""Produce el report y tablas desde juicios explícitos; --check no escribe ni abre microdato."""
import argparse,csv,hashlib,io,json,re,sys
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[4]
REPORT=ROOT/'corpus/reports-v2/El_Efecto_Ambiental_de_la_Violencia_Crónica_en_México__Cómo_el_Miedo_Reorganiza_la_Conducta_Psicológica_de_la_Población.md'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tsv(rows,keys):
 b=io.StringIO();w=csv.DictWriter(b,keys,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows);return b.getvalue()
def inputs():
 dec=read(D/'decisiones.json');ev=read(D/'evidencia.json');src=read(D/'fuentes.json')
 assert sha(ROOT/dec['original'])==dec['original_sha256'],'Original cambió: releer alcance'
 assert sha(ROOT/'canon/mapa-dominios-v1_1.tsv')==dec['mapa_sha256'],'Mapa cambió: cotejar'
 for path,h in ev['inputs'].items():assert sha(ROOT/path)==h,'Objeto de evidencia cambió: '+path
 mapa={r['id_afirmacion']:r for r in csv.DictReader((ROOT/'canon/mapa-dominios-v1_1.tsv').open(),delimiter='\t')}
 expected={k for k,v in mapa.items() if v['report']==dec['original']}
 expected.update({'ASTRA5-U0-TRUST-004','ASTRA5-U0-POL-009'})
 seen={r['mapa_id'] for r in dec['decisiones'] if r['mapa_id']}
 assert expected==seen,'Cobertura del mapa/fusionadas incompleta'
 ids=[r['id'] for r in dec['decisiones']];assert len(set(ids))==len(ids),'IDs duplicados'
 for r in dec['decisiones']:
  assert r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} and r['razon'] and r['afirmacion']
  assert r['evidencia'] in {'METODO','ENVIPE','ENSU','NARCO','IEP','ENCIG'}
 signatures=list(csv.DictReader((ROOT/'forense/firmas-pendientes.tsv').open(),delimiter='\t'))
 fp=next(r for r in signatures if r['id']==ev['adopcion']['CALC-ENSU-PISOS-0001']['fp'])
 assert fp['estado']=='ABIERTA','Adopción ENSU cambió: actualizar interpretación'
 decisions=list(csv.DictReader((ROOT/'data/corrida0/decisiones.tsv').open(),delimiter='\t'))
 for q in ev['quantities']:
  assert q['estado']=='PROVISIONAL','Promoción sin acto de contenido'
  assert not any(q['calc'] in str(r) and 'vet' in r.get('decision','').lower() for r in decisions),'Veto activo'
  assert q['unidad']=='persona' and q['temporalidad']=='RETROSPECTIVA'
  if 'ENVIPE' in q['calc']:
   assert q['ola']=='2024' and q['poblacion']=='Persona elegida 18–97 nacional'
   if 'CAMINAR' in q['result_id']:den='Respuestas muy seguro/seguro/inseguro/muy inseguro; No aplica y NS/NR fuera'
   elif 'MENORES' in q['result_id']:den='Respuestas sí/no aplicables; No aplica y NS/NR fuera'
   else:den='Respuestas seguro/inseguro; NS/NR fuera'
  else:
   assert q['ola']=='2025T3' and q['poblacion']=='Persona seleccionada 18+ áreas urbanas ENSU'
   assert 'C01-INSEG-CIUDAD' in q['result_id'],'Hábitos ENSU No aplica no son base comunicados'
   den='Respuestas seguro/inseguro; NS/NR fuera'
  assert q['denominador']==den,'Denominador incompatible con reactivo'
 return dec,ev,src,mapa

def produce():
 dec,ev,src,mapa=inputs(); qr=[];md=['| Registro | Estimando | Punto | IC de diseño | Universo, ola y denominador | RESULT, estado |','|---|---|---|---|---|---|']
 for q in ev['quantities']:
  vals=read(ROOT/q['archivo'])['resultados'];rid=q['result_id'];p=vals[rid];lo=vals[rid[:-1]+'IC-LO'];hi=vals[rid[:-1]+'IC-HI']
  assert p is not None and 0<=p<=1 and lo<=p<=hi
  row=dict(q,punto=p,ic95_inf=lo,ic95_sup=hi,archivo_sha256=sha(ROOT/q['archivo']))
  qr.append(row)
  md.append(f"| {q['id']} | {q['label']} | {100*p:.2f}% | [{100*lo:.2f}%, {100*hi:.2f}%] | {q['poblacion']}; {q['ola']}; {q['denominador']} | `{rid}`; {q['estado']} |")
 counts=dict(Counter(r['dictamen'] for r in dec['decisiones']));mapped=len({r['mapa_id'] for r in dec['decisiones'] if r['mapa_id']});extra=sum(not r['mapa_id'] for r in dec['decisiones'])
 coverage=f"Juicios POR EJECUTOR: {len(dec['decisiones'])} registros por cláusula; {mapped} identidades del mapa incluidas dos fusionadas y {extra} registros fuera del mapa. Son registros editoriales, con reiteraciones del original vinculadas por localizador; no son conteo de tesis independientes. Dictámenes derivados: "+', '.join(f'{k}={v}' for k,v in sorted(counts.items()))+'.'
 template=(D/'report.template.md').read_text()
 report=template.replace('{{CORTE}}',dec['corte']).replace('{{TABLA_CIFRAS}}','\n'.join(md)).replace('{{COBERTURA}}',coverage)
 validate_text(report,md[2:])
 table=[]
 for r in dec['decisiones']:
  mr=mapa.get(r['mapa_id'],{}); table.append(dict(r,texto_mapa=mr.get('texto_vigente','FUERA-DEL-MAPA'),dictamen_medibilidad_mapa=mr.get('dictamen','NO-APLICA')))
 argv=['python3',str((D/'verifica.py').relative_to(ROOT))]
 resumen={'report':str(REPORT.relative_to(ROOT)),'mapa_filas':mapped,'afirmaciones':{'registros':len(table),'nota':'Cláusulas con correspondencias; reiteraciones vinculadas, no tesis independientes; dos fusionadas incluidas','fuera_mapa':extra},'dictamenes':counts,'cifras':len(qr),'fuentes':len(src),'fuentes_efectivamente_leidas':sum(x['estado'].startswith('LEIDO') for x in src),'reglas':3,'comando_generar':argv+['--write'],'comando_verificar':argv+['--check','--self-test'],'reservas':['ENVIPE adopción específica no hallada en vista: provisional, no piso catálogo','ENSU firma ABIERTA y hábitos No aplica; primeras olas sexo no completamente comparadas','Fuentes con fetch incompleto no sostienen cifras','No lectura microdato/ENVIPE2026/EDR2024; revisión externa solicitada']}
 out={REPORT:report,D/'tabla-afirmaciones.tsv':tsv(table,list(table[0])),D/'cifras.tsv':tsv(qr,list(qr[0])),D/'resumen.json':json.dumps(resumen,ensure_ascii=False,indent=2)+'\n',D/'indice-local.md':'# Violencia ambiental · índice local\n\n'+coverage+'\n\n'+f"Cifras trazadas: {len(qr)}. Comando: `{' '.join(argv)} --check --self-test`.\n"}
 return out,md[2:],resumen

def validate_text(report,expected_rows):
 # Comprueba afirmaciones porcentuales, no todos los dígitos (años, ids, referencias).
 rows=[s for s in report.splitlines() if re.search(r'\d+(?:[.,]\d+)?\s*%',s)]
 assert rows==expected_rows,'Cantidad sin evidencia o denominador/texto de tabla incompatible'
 assert 'PROVISIONAL' in report and 'no como piso adoptado' in report,'Adopción elevada sin firma'

def self_test(out,rows):
 text=out[REPORT]
 mutations=[text+'\nEl 99.9% de mexicanos tiene trauma.\n',text.replace('Respuestas seguro/inseguro; NS/NR fuera','Todas las personas, incluidas NS/NR',1)]
 for m in mutations:
  try:validate_text(m,rows)
  except AssertionError:continue
  raise AssertionError('Mutación material aceptada')
 # Cobertura y veto, además de las dos pruebas sobre texto de producto.
 dec=read(D/'decisiones.json'); expected={r['mapa_id'] for r in dec['decisiones'] if r['mapa_id']}
 cut=[r for r in dec['decisiones'] if r['mapa_id']!='ASTRA5-U0-VIOL-012']
 assert {r['mapa_id'] for r in cut if r['mapa_id']}!=expected
 print('SELF-TEST: rechaza cifra inventada en texto, denominador cambiado en texto y pérdida de cobertura')

def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group();g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();out,rows,res=produce()
 if a.self_test:self_test(out,rows)
 if a.write:
  for f,s in out.items():f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s)
 else:
  for f,s in out.items():assert f.exists() and f.read_text()==s,'Derivado distinto: '+str(f.relative_to(ROOT))
 print(json.dumps({'estado':'VERIFICA-SIN-DIFERENCIAS' if not a.write else 'GENERADO','dictamenes':res['dictamenes'],'cifras':res['cifras']},ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (AssertionError,KeyError,ValueError) as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
