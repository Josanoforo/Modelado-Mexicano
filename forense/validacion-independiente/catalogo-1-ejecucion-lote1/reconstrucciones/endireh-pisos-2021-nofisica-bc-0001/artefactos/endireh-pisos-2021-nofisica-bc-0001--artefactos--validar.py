"""Validación de la entrega congelable, sin recalcular estimaciones."""
import csv
import hashlib
import json
import math
from pathlib import Path
from collections import Counter

root=Path(__file__).resolve().parent

def read(name):
    with (root/name).open() as f:
        return list(csv.DictReader(f,delimiter='\t'))

spec=read('entrada/estimandos.tsv'); out=read('reconstruccion.tsv'); reps=read('replicas.tsv')
assert [r['llave'] for r in spec]==[r['llave'] for r in out]
assert len({r['llave'] for r in out})==len(out)
allowed={'RECONSTRUIDO','NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO','NO-EVALUADO'}
published=set()
for r in out:
    assert r['estado'] in allowed
    if r['estado']=='RECONSTRUIDO':
        published.add(r['llave'])
        p,lo,hi=[float(r[k]) for k in ('punto','ic95_inf','ic95_sup')]
        assert all(math.isfinite(x) for x in [p,lo,hi])
        assert 0<=p<=1 and 0<=lo<=hi<=1 and hi-lo<=.20
        assert not r['motivo']
    else:
        assert r['motivo'] and all(r[k]=='' for k in ('punto','ic95_inf','ic95_sup'))
assert set(r['llave'] for r in reps)==published
assert Counter(r['llave'] for r in reps)==Counter({k:200 for k in published})
assert len({(r['llave'],r['replica']) for r in reps})==len(reps)
assert all(1<=int(r['replica'])<=200 and 0<=float(r['proporcion'])<=1 for r in reps)
for r in read('diagnostico.tsv'):
    if r['llave'] in published:
        assert int(r['n_conocido'])>=100 and int(r['upm_con_casos'])>=5
receipt=json.loads((root/'recibo.json').read_text())
assert receipt['manifiesto_sha256']==hashlib.sha256(Path('/entrada/manifiesto.json').read_bytes()).hexdigest()
assert not list(root.rglob('*.pdf')) and not list(root.rglob('*.zip'))
print(json.dumps({'validacion':'APROBADA','llaves':len(out),'con_cifras':len(published),
                  'replicas':len(reps),'manifiesto_sha256':receipt['manifiesto_sha256']},ensure_ascii=False,indent=2))
