"""Verifica integridad de la entrega sin volver a estimar ni consultar referencias."""
import collections, csv, hashlib, json
from pathlib import Path
import numpy as np

base=Path(__file__).resolve().parent
read=lambda name:list(csv.DictReader((base/name).open(),delimiter='\t'))
incoming=read('entrada/estimandos.tsv'); result=read('reconstruccion.tsv'); reps=read('replicas.tsv')
assert [r['llave'] for r in incoming]==[r['llave'] for r in result]
assert len({r['llave'] for r in result})==len(result)
repmap={r['llave']:r for r in reps};assert len(repmap)==len(reps)
allowed={'RECONSTRUIDO','NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO','NO-EVALUADO'}
for r in result:
    assert r['estado'] in allowed
    vals=[r[c] for c in ['punto','ic95_inf','ic95_sup']]
    if r['estado']=='RECONSTRUIDO':
        p,lo,hi=map(float,vals);assert 0<=p<=1 and 0<=lo<=hi<=1
        assert not r['motivo'];rr=repmap[r['llave']]
        x=np.array([float(rr[f'replica_{i:03}']) for i in range(1,201)])
        assert np.all(np.isfinite(x)&(x>=0)&(x<=1))
        np.testing.assert_allclose([lo,hi],np.quantile(x,[.025,.975]),rtol=0,atol=1e-15)
        assert hi-lo<=.20 and (p==0 or np.std(x,ddof=1)/p<=.30)
    else:
        assert vals==['','',''] and r['motivo'] and r['llave'] not in repmap
assert len(reps)==sum(r['estado']=='RECONSTRUIDO' for r in result)
receipt=json.loads((base/'recibo.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(base/'entrada/manifiesto.json')==receipt['manifiesto_sha256']
for name,h in receipt['entradas_sha256'].items():assert sha(base/'entrada'/name)==h
for item in receipt['insumos']:assert sha(Path(item['ruta_efectiva']))==item['sha256_calculado']==item['entrada_recibida']['sha256']
print(json.dumps({'llaves':len(result),'estados':dict(collections.Counter(r['estado'] for r in result)), 'replicas_por_llave_publicable':200,'verificacion':'integridad, cobertura, IC, publicación y hashes verificados'},ensure_ascii=False,indent=2))
