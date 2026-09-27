import csv, json, itertools
from pathlib import Path
from reconstruir import outcome
p=Path(__file__).resolve().parent
cases=0
for n in (1,2,3):
 for x in itertools.product(('1','2','3','9',''),repeat=n):
  expected=1 if any(v=='1' for v in x) else 0 if set(x)=={'2'} else -1
  assert outcome(x)==expected
  cases+=1
r=list(csv.DictReader((p/'reconstruccion.tsv').open(),delimiter='\t'))
k=list(csv.DictReader((p/'entrada/estimandos.tsv').open(),delimiter='\t'))
assert [x['llave'] for x in r]==[x['llave'] for x in k]
for x in r:
 if x['punto']:
  assert x['estado']=='RECONSTRUIDO'
  assert 0<=float(x['punto'])<=1
  assert 0<=float(x['ic95_inf'])<=float(x['ic95_sup'])<=1
 else:assert x['motivo'] and not x['ic95_inf'] and not x['ic95_sup']
s=list(csv.DictReader((p/'soporte.tsv').open(),delimiter='\t'))
assert len(s)==263
for x in s:
 if x['publicable']=='True':
  assert int(x['n_conocido'])>=100 and int(x['upm_con_casos'])>=5
reps=list(csv.DictReader((p/'replicas.tsv').open(),delimiter='\t'))
assert len(reps)==263*200
(p/'validacion.json').write_text(json.dumps(dict(llaves=len(r),clasificaciones_verificadas=cases,replicas_agregadas=len(reps),verificaciones='satisfactorias'),indent=2)+'\n')
print('Verificaciones satisfactorias')
