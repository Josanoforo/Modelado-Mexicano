#!/usr/bin/env python3
"""Control material: mapa/cláusulas, fuentes y denominadores; no decide veredictos."""
import copy,csv,hashlib,json,re,sys
from pathlib import Path
from genera import P,ROOT,REPORT,load,productos
ORIG=ROOT/'corpus/reports/Report_26__The_Contemporary_Mexican_and_Knowledge__Expertise__Education_and_Information_as_Decision_Behavior.md'
MAPA=ROOT/'canon/mapa-dominios-v1_1.tsv'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validar(rows,report,cifras,coverage):
 errors=[];ids={x['id'] for x in rows};m=load('metadatos.json')
 if len(ids)!=len(rows):errors.append('ID-DUPLICADO')
 expected={x['id_afirmacion'] for x in csv.DictReader((P/'mapa-leido.tsv').open(),delimiter='\t')}
 if expected!={x['mapa_id'] for x in rows if x['mapa_id']}:errors.append('COBERTURA-MAPA')
 for x in rows:
  if x['dictamen'] not in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} or not x['razon'] or not x['revision_material']:errors.append('JUICIO-INCOMPLETO')
  if x['dictamen']=='SIN-CIFRA' and not x['razon_sin_cifra']:errors.append('SIN-CIFRA-SIN-RAZON')
  if x['resultado']:errors.append('RESULT-NO-AUTORIZADO')
 lines=ORIG.read_text().splitlines();org={53,63,69,73,190,197,204,211,214,217}
 material={n for n,l in enumerate(lines,1) if l.strip() and not l.startswith('#') and l!='---' and n not in org}
 if material!={x['linea'] for x in coverage}:errors.append('COBERTURA-ORIGINAL')
 for c in coverage:
  if c['literal']!=lines[c['linea']-1] or not c['decisiones'] or not set(c['decisiones'])<=ids:errors.append('CORRESPONDENCIA-ROTA')
 sources={x['id']:x for x in load('fuentes.json')}
 for c in cifras:
  s=sources.get(c['fuente'])
  if not s or not s['estado'].startswith('LEÍDO-WEB') or not s['localizador'] or not s['fecha_lectura']:errors.append('CIFRA-SIN-FUENTE')
  if c['tipo']!='EXTERNA' or not c['denominador'] or not c['escala'] or c['marca']!='RETROSPECTIVA':errors.append('DENOMINADOR-O-ESTADO')
  if c['sentencia']+' ['+c['fuente']+']('+c['url']+'). <!-- '+c['id']+' -->' not in report:errors.append('CIFRA-VALOR-O-DENOMINADOR-CAMBIADO')
 for line in report.splitlines():
  if re.search(r'\d+(?:[.,]\d+)?\s*(?:%|puntos\b|pp\b)',line) and not re.search(r'<!-- Q\d+ -->',line):errors.append('CIFRA-SIN-TRAZA')
 for k,path in [('original_sha256',ORIG),('mapa_fuente_sha256',MAPA),('fuentes_sha256',P/'fuentes.json'),('contratos_sha256',P/'contratos-cifras.json')]:
  if h(path)!=m[k]:errors.append('HASH-'+k)
 for n in range(1,14):
  if not re.search(r'^## '+str(n)+r'\.',report,re.M):errors.append('BLOQUE-B-INCOMPLETO')
 if m['RESULT_usados']:errors.append('DEPENDENCIA-RESULT-NO-REVISADA')
 return sorted(set(errors))
def main():
 rows,expected,cifras=productos();coverage=load('cobertura-original.json');report=REPORT.read_text()
 errors=validar(rows,report,cifras,coverage)
 if report!=expected:errors.append('REPORT-NO-REGENERADO')
 table=list(csv.DictReader((P/'tabla.tsv').open(),delimiter='\t'))
 if table!=rows:errors.append('TABLA-NO-REGENERADA')
 if load('cifras.json')!=cifras:errors.append('CIFRAS-NO-REGENERADAS')
 if '--self-test' in sys.argv:
  tests=[]
  reduced=[x for x in rows if x['mapa_id']!='ASTRA5-U0-CONOC-001'];tests.append(('mapa faltante','COBERTURA-MAPA' in validar(reduced,report,cifras,coverage)))
  tests.append(('original faltante','COBERTURA-ORIGINAL' in validar(rows,report,cifras,coverage[:-1])))
  tests.append(('cifra agregada sin fuente','CIFRA-SIN-TRAZA' in validar(rows,report+'\nFrecuencia 99%.',cifras,coverage)))
  tests.append(('valor cambiado','CIFRA-VALOR-O-DENOMINADOR-CAMBIADO' in validar(rows,report.replace('395 puntos','396 puntos'),cifras,coverage)))
  tests.append(('denominador cambiado','CIFRA-VALOR-O-DENOMINADOR-CAMBIADO' in validar(rows,report.replace('activos de 25–34 años','habitantes de 25–34 años'),cifras,coverage)))
  cc=copy.deepcopy(cifras);cc[0]['fuente']='NO-LEIDA';tests.append(('fuente retirada','CIFRA-SIN-FUENTE' in validar(rows,report,cc,coverage)))
  print(json.dumps({'mutaciones':tests},ensure_ascii=False));errors.extend('MUTACION-NO-DETECTADA:'+name for name,ok in tests if not ok)
 print(json.dumps({'estado':'PASS' if not errors else 'FAIL','errores':errors,'mapa_filas':len({x['mapa_id'] for x in rows if x['mapa_id']}),'clausulas':len(rows),'lineas_materiales_original':len(coverage),'cifras_externas':len(cifras),'RESULT_usados':0},ensure_ascii=False))
 return bool(errors)
if __name__=='__main__':sys.exit(main())
