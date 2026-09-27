"""Validaciones de integridad sobre el primer resultado, sin volver a estimar."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

root = Path(__file__).resolve().parent
def read(name):
    with open(root / name) as f:
        return list(csv.DictReader(f, delimiter='\t'))

expected = read('entrada/estimandos.tsv')
actual = read('reconstruccion.tsv')
assert [r['llave'] for r in actual] == [r['llave'] for r in expected]
assert len(set(r['llave'] for r in actual)) == 117
replicas = read('replicas.tsv')
by_key = {}
for r in replicas:
    by_key.setdefault(r['llave'], []).append(r)
for r in actual:
    if r['estado'] == 'RECONSTRUIDO':
        point, lo, hi = [float(r[k]) for k in ['punto', 'ic95_inf', 'ic95_sup']]
        assert 0 <= point <= 1 and 0 <= lo <= hi <= 1
        assert r['motivo'] == ''
        b = by_key.pop(r['llave'])
        assert [int(v['replica']) for v in b] == list(range(1, 501))
        values = np.array([float(v['proporcion']) for v in b])
        assert np.all((values >= 0) & (values <= 1))
        assert np.array_equal(np.quantile(values, [.025, .975], method='linear'), [lo, hi])
        assert hi - lo <= .20
        assert point == 0 or np.std(values, ddof=1) / point <= .30
    else:
        assert r['estado'] in ['NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO', 'NO-EVALUADO']
        assert r['motivo'] and all(r[k] == '' for k in ['punto', 'ic95_inf', 'ic95_sup'])
        assert r['llave'] not in by_key
assert not by_key
receipt = json.loads((root / 'recibo.json').read_text())
assert hashlib.sha256((root / 'entrada/manifiesto.json').read_bytes()).hexdigest() == receipt['manifiesto_sha256']
assert receipt['lista_entradas_manifiesto'] == json.loads((root / 'entrada/manifiesto.json').read_text())['archivos']
print('Verificadas 117 llaves, estados, ausencia de réplicas no publicables, 500 réplicas por celda publicada, IC, filtros y recibo.')
