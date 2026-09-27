"""Verificación de reglas y salidas, sin producir una segunda estimación."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from reconstruir import union, sha

root = Path(__file__).resolve().parent
values = np.full((5,20), '4')
values[1,0] = '1'
values[2,0] = '9'
values[3,0] = ''
values[4,0] = '9'; values[4,1] = '3'
p,k = union(values)
assert p.tolist() == [False,True,False,False,True]
assert k.tolist() == [True,True,False,False,True]
keys = pd.read_csv(root/'entrada/estimandos.tsv', sep='\t')
out = pd.read_csv(root/'reconstruccion.tsv', sep='\t')
diag = pd.read_csv(root/'diagnosticos.tsv', sep='\t')
rep = pd.read_csv(root/'replicas.tsv', sep='\t', index_col='replica')
assert out.llave.tolist() == keys.llave.tolist()
assert out.llave.is_unique and len(out) == 50 and len(rep) == 200
assert set(out.estado) <= {'RECONSTRUIDO','NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO','NO-EVALUADO'}
for i,r in out.iterrows():
    if r.estado != 'RECONSTRUIDO':
        assert isinstance(r.motivo,str) and r.motivo
        assert pd.isna([r.punto,r.ic95_inf,r.ic95_sup]).all()
        continue
    assert 0 <= r.punto <= 1 and 0 <= r.ic95_inf <= r.ic95_sup <= 1
    assert diag.iloc[i].n_conocido >= 100 and diag.iloc[i].upm_con_casos >= 5
    assert r.ic95_sup-r.ic95_inf <= .20
    if r.punto > 0: assert diag.iloc[i].cv <= .30
    np.testing.assert_allclose(np.quantile(rep[r.llave],[.025,.975],method='linear'),
                               [r.ic95_inf,r.ic95_sup],rtol=0,atol=1e-14)
    np.testing.assert_allclose(rep[r.llave].std(ddof=1)/r.punto,diag.iloc[i].cv,rtol=0,atol=1e-14)
receipt = json.loads((root/'recibo.json').read_text())
assert receipt['manifiesto_sha256_recibido'] == sha(root/'entrada/manifiesto.json')
for name,h in receipt['entradas'].items(): assert sha(root/'entrada'/name) == h
print('Verificación correcta: unión ternaria, 50 llaves, criterios, réplicas, IC y hashes de entradas.')
