#!/usr/bin/env python3
"""Comprueba cobertura y trazas de esta edición; la semántica se revisa a mano."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[5]
report=root/'corpus/reports-v2/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md'
table=Path(__file__).with_name('afirmaciones.tsv')
with table.open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==45 and len({r['id'] for r in rows})==45
assert {r['dictamen_v2'] for r in rows}=={'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}
assert all(r['razon_editorial'] and r['ancla'] for r in rows)
with (root/'canon/mapa-dominios-v1_1.tsv').open(newline='') as f:
 ids={r['id_afirmacion'] for r in csv.DictReader(f,delimiter='\t') if 'El_Mexicano_y_el_Tiempo__' in r['report'] or r['id_afirmacion']=='ASTRA5-U0-ENOE-001'}
assert ids=={r['id'] for r in rows if r['id'].startswith('ASTRA5-')}
body=report.read_text()
assert 'ENUT' not in body and 'ENSU' not in body
assert 'ENIF2024_RR.pdf' not in body and '889463923121.pdf' not in body
for key in ('TIME-001','TIME-002','TIME-003','TIME-004','TIME-005','TIME-006','TIME-016','TIME-019','TIME-020','TIME-032'):
 row=next(r for r in rows if r['id']=='ASTRA5-U0-'+key)
 assert 'extracto reservado omitido' in row['afirmacion_v1']
for id_ in ('RESULT-ENIF-AHO-B-P-FORMAL-P','RESULT-ENIF-AHO-B-P-INFORMAL-P','RESULT-ENIF-AHO-A-P-CORTO-CON-P','RESULT-ENIF-AHO-A-P-CORTO-SIN-P'):
 assert id_ in body
 p=subprocess.run(['python3','tools/consulta.py','result',id_],cwd=root,text=True,capture_output=True)
 assert p.returncode==0 and 'cuenta_gen2=SI' in p.stdout and 'estado=SELLADA' in p.stdout, id_
for forbidden in ('66.0%','58.1%','51.6%','55.7%','55.2%','72% llega','74% de los jóvenes'):
 assert forbidden not in body, forbidden
assert 'RETROSPECTIVA' in body and 'PROSPECTIVA' in body
calc=root/'data/corrida0/CALC-ENIF-0001/resultados.json'
raw=calc.read_bytes(); data=json.loads(raw)['resultados']
sha=hashlib.sha256(raw).hexdigest()
assert json.loads((calc.parent/'sello.json').read_text())['resultados.json']==sha
with Path(__file__).with_name('trazas-result.tsv').open(newline='') as f:
 traces=list(csv.DictReader(f,delimiter='\t'))
assert len(traces)==4 and len({t['result_id'] for t in traces})==4
assert 'trazas-result.tsv' in body
catalog={}
with (root/'canon/catalogo-del-mexicano-v1_3.tsv').open(newline='') as f:
 for x in csv.DictReader(f,delimiter='\t'):
  if x['result_id'] in {t['result_id'] for t in traces}: catalog[x['result_id']]=x
for t in traces:
 rid=t['result_id']; stem=rid[:-2]; c=catalog[rid]
 assert t['fila_json']==f'/resultados/{rid}' and t['sha256_resultados_json']==sha
 assert float(t['valor_p'])==data[rid]
 assert t['denominador']==data[stem+'-DENOMINADOR']
 assert int(t['n_denominador'])==data[stem+'-N-DENOMINADOR']
 assert t['metodo_ic']==data[stem+'-METODO-IC']
 assert t['calc']==c['calc']=='CALC-ENIF-0001'
 assert t['estado_adopcion']==c['estado_adopcion']=='ADOPTADO'
 assert t['firma_fp']==c['firma_fp']=='FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01'
 assert t['unidad']=='proporción ponderada (p)' and t['poblacion']=='persona elegida ENIF 18+' and t['ola']=='ENIF 2024'
by_id={t['result_id']:t for t in traces}
con=by_id['RESULT-ENIF-AHO-A-P-CORTO-CON-P']
sin=by_id['RESULT-ENIF-AHO-A-P-CORTO-SIN-P']
assert float(con['valor_p']) < float(sin['valor_p'])
assert int(con['n_denominador']) == 3969 and int(sin['n_denominador']) == 4973
assert 'CON seguridad social' in con['denominador'] and 'SIN seguridad social' in sin['denominador']
# Juicio editorial explícito: P4_10 {1,2} es menos de un mes según spec.
# Por tanto, mayor p(SIN) significa menor resiliencia descriptiva en ese grupo.
time_006=next(r for r in rows if r['id']=='ASTRA5-U0-TIME-006')
assert time_006['dictamen_v2']=='MATIZA'
assert time_006['ancla']=='RESULT-ENIF-AHO-A-P-CORTO-CON-P;RESULT-ENIF-AHO-A-P-CORTO-SIN-P'
p=subprocess.run(['python3','tools/consulta.py','fp','FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01'],cwd=root,text=True,capture_output=True)
assert p.returncode==0 and 'estado=FIRMADA' in p.stdout
print('VERDE: 38 filas del mapa + 7 materiales ausentes; 4 RESULT ENIF con fila/hash/denominador/adopción cotejados; cifras restringidas y vetadas ausentes')
