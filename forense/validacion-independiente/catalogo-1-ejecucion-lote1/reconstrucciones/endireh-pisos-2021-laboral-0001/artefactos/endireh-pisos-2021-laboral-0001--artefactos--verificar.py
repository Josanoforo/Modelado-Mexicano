"""Comprobaciones semánticas y del contrato de entrega, sin referencias esperadas."""
import csv
from pathlib import Path
import numpy as np
from reconstruir import unions

# Negativo completo, desconocido, positivo con desconocidos y salto reciente.
a = np.full((7,19),2.)
a[1,0] = np.nan
a[2,0] = 1; a[2,1] = np.nan
a[3,0] = 1
a[4,0] = 1
a[6,0] = 1
b = np.full_like(a,np.nan)
b[2,0] = 3; b[3,0] = 4
b[6,0] = 1
v,r = unions(a,b,np.array([1,1,1,1,1,0,1],bool),np.array([1,1,1,1,1,0,0],bool))
np.testing.assert_allclose(v,[0,np.nan,1,1,1,np.nan,1],equal_nan=True)
np.testing.assert_allclose(r,[0,np.nan,1,0,np.nan,np.nan,np.nan],equal_nan=True)
root=Path(__file__).resolve().parent
read=lambda p:list(csv.DictReader((root/p).open(),delimiter='\t'))
expected=read('entrada/estimandos.tsv'); actual=read('reconstruccion.tsv')
assert [x['llave'] for x in actual] == [x['llave'] for x in expected]
assert all(x['estado']=='NO-RECALCULABLE-DESDE-SPEC' and x['motivo'] and
           not any(x[k] for k in ['punto','ic95_inf','ic95_sup']) for x in actual)
semantic=read('resultados_semanticos.tsv'); replicas=read('replicas_agregadas.tsv')
assert len(semantic)==100
for row in semantic:
    vals=[float(x['punto']) for x in replicas if all(x[k]==row[k] for k in ['ventana','eje','segmento'])]
    if row['publicable']=='SI':
        assert len(vals)==200
        lo,hi=np.quantile(vals,[.025,.975],method='linear')
        assert float(row['ic95_inf'])==lo and float(row['ic95_sup'])==hi
        assert 0<=float(row['punto'])<=1 and 0<=lo<=hi<=1
        assert int(row['n_conocido'])>=100 and int(row['upm_con_casos'])>=5
        assert hi-lo<=.20
        assert float(row['cv'])<=.30 or float(row['punto'])==0
    else:
        assert not vals and row['motivo'] and not row['punto']
print('Verificación satisfactoria: uniones, elegibilidad, llaves, supresión y percentiles.')
