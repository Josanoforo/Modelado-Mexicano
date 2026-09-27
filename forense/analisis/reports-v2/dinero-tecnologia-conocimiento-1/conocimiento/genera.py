#!/usr/bin/env python3
"""Deriva tabla y report de juicios explícitos; no adjudica por texto, mapa o rango."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[4]
REPORT=ROOT/'corpus/reports-v2/Report_26__The_Contemporary_Mexican_and_Knowledge__Expertise__Education_and_Information_as_Decision_Behavior.md'
def load(n):return json.loads((P/n).read_text())
def productos():
 rows=load('decisiones.json');sources={x['id']:x for x in load('fuentes.json')};q=load('contratos-cifras.json')
 report=(P/'report.plantilla.md').read_text()
 cifras=[]
 for c in q:
  s=sources[c['fuente']];values={k:s['hechos'][k] for k in c['hechos']}
  sentence=c['plantilla'].format(**values)
  line=sentence+' ['+s['id']+']('+s['url']+'). <!-- '+c['id']+' -->'
  report=report.replace('{{'+c['id']+'}}',line)
  cifras.append(dict(c,sentencia=sentence,valores=values,url=s['url'],localizador=s['localizador'],estado_adopcion='EXTERNA-NO-RESULT-NO-ADOPTA',fuente_registro_sha256=hashlib.sha256(json.dumps(s,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
 return rows,report,cifras
if __name__=='__main__':
 rows,report,cifras=productos()
 with (P/'tabla.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',quoting=csv.QUOTE_ALL,lineterminator='\n');w.writeheader();w.writerows(rows)
 REPORT.write_text(report)
 (P/'cifras.json').write_text(json.dumps(cifras,ensure_ascii=False,indent=2)+'\n')
 mapa=list(csv.DictReader((P/'mapa-leido.tsv').open(),delimiter='\t'))
 summary={'report':str(REPORT.relative_to(ROOT)),'mapa_filas':len(mapa),'afirmaciones':len(rows),'dictamenes':dict(Counter(x['dictamen'] for x in rows)),'cifras':len(cifras),'fuera_mapa':sum(not x['mapa_id'] for x in rows),'resultado':'Report íntegro Bloque B; mecanismos como hipótesis; cifra propia compatible no disponible','comando_generar':['python3',str((P/'genera.py').relative_to(ROOT))],'comando_verificar':['python3',str((P/'verifica.py').relative_to(ROOT))],'comando_self_test':['python3',str((P/'verifica.py').relative_to(ROOT)),'--self-test']}
 (P/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(summary,ensure_ascii=False))
