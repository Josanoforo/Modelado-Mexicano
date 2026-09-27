"""Verificación de reglas de desconocidos y de la entrega, sin referencias externas."""
import csv
from pathlib import Path
import numpy as np
from reconstruir import unions

life = np.full((5,16),'2',dtype='<U1')
recent = np.full((5,16),'',dtype='<U1')
life[1,0] = '1'; recent[1,0] = '9'
life[2,0] = ''; recent[2,1] = '1'
life[3,:2] = ['1','']; recent[3,0] = '3'
life[4,:2] = ['1','']; recent[4,0] = '4'
a,b = unions(life,recent)
np.testing.assert_equal(a, [0,1,np.nan,1,1])
np.testing.assert_equal(b, [0,np.nan,np.nan,1,np.nan])
p = Path(__file__).resolve().parent
with (p/'entrada/estimandos.tsv').open() as f:
    keys = [r['llave'] for r in csv.DictReader(f,delimiter='\t')]
with (p/'salida/reconstruccion.tsv').open() as f:
    rows = list(csv.DictReader(f,delimiter='\t'))
assert [r['llave'] for r in rows] == keys
assert len(rows) == len(set(keys)) == 100
assert all(r['estado']=='FALTANTE_HORIZONTE_EN_LLAVE' and
           all(r[c]=='' for c in ['punto','ic95_inf','ic95_sup']) for r in rows)
with (p/'salida/estimaciones_por_horizonte.tsv').open() as f:
    estimates = list(csv.DictReader(f,delimiter='\t'))
assert len(estimates)==100
published = set()
for r in estimates:
    if r['estado']=='PUBLICABLE':
        assert 0 <= float(r['punto']) <= 1
        assert 0 <= float(r['ic95_inf']) <= float(r['ic95_sup']) <= 1
        assert float(r['ic95_sup']) - float(r['ic95_inf']) <= .20
        published.add((r['horizonte'],r['eje'],r['segmento']))
    else:
        assert all(r[c]=='' for c in ['punto','ic95_inf','ic95_sup'])
counts = dict.fromkeys(published,0)
with (p/'salida/replicas_publicables.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):
        key = (r['horizonte'],r['eje'],r['segmento'])
        assert key in published
        assert 0 <= float(r['proporcion']) <= 1
        counts[key] += 1
assert all(v==200 for v in counts.values())
print('VERIFICADO: uniones, 100 llaves, intervalos, supresión y 200 réplicas por celda publicable.')
