"""Verificación independiente de puntos con Decimal y lector CSV estándar."""
import csv,io,json,zipfile,hashlib
from decimal import Decimal as D
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
receipt=json.loads((P/'recibo.json').read_text())
for n,h in receipt['archivos_congelados'].items():
    assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h
src=receipt['miembro_utilizado']
with zipfile.ZipFile(src['archivo']) as z:
    rows=list(csv.DictReader(io.TextIOWrapper(z.open(src['entrada']),encoding='utf-8-sig')))
wtotal=D(0); wrec=D(0); wr=D(0); wy=D(0); meanrat=D(0); ge=D(0); values=[]
for row in rows:
    w,r,y=(D(row[k]) for k in ['factor','remesas','ing_cor'])
    assert w.is_finite() and w>0 and r.is_finite() and r>=0
    wtotal+=w
    if r>0:
        assert y.is_finite() and y>0 and r<=y+D('.01')
        wrec+=w; wr+=w*r; wy+=w*y; meanrat+=w*r/y
        if r/y>=D('.5'): ge+=w
        values.append((r,w))
cum=D(0)
for r,w in sorted(values):
    cum+=w
    if cum>=wrec/2: median=r; break
expected=dict(prevalencia_remesas=wrec/wtotal,remesas_media_remesas=wr/wrec,
 remesas_mediana_remesas=median,participacion_agregada_remesas=wr/wy,
 participacion_media_hogar_remesas=meanrat/wrec,participacion_ge50_remesas=ge/wrec)
out=list(csv.DictReader((P/'reconstruccion.tsv').open(),delimiter='\t'))
assert len(out)==6 and len({r['llave'] for r in out})==6
for row in out:
    assert row['estado']=='RECONSTRUIDO'
    assert abs(float(expected[row['conducta']])-float(row['valor']))<=1e-10
b=np.loadtxt(P/'replicas.tsv',skiprows=1)
assert b.shape==(2000,3) and np.isfinite(b).all()
lim=np.percentile(b,[2.5,97.5],axis=0,method='linear')
for j,k in enumerate(['participacion_media_hogar_remesas','participacion_agregada_remesas','participacion_ge50_remesas']):
    row=next(x for x in out if x['conducta']==k)
    assert float(row['ic95_inf'])==lim[0,j] and float(row['ic95_sup'])==lim[1,j]
report=dict(resultado='PASS',filas=len(rows),receptores=len(values),
 verificaciones=['Hashes del código y números contra recibo','Seis llaves únicas reconstruidas',
 'Puntos por CSV estándar y Decimal: diferencia absoluta <= 1e-10 (control numérico interno, no tolerancia de revelación)',
 'Ausencia de exclusiones e incompatibilidades verificada fila por fila',
 '2000 réplicas finitas y percentiles idénticos al TSV'],
 tolerancia_revelacion=json.loads((P/'entradas/tolerancia.json').read_text()),
 comparacion_con_resultados_esperados='NO REALIZADA')
(P/'verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
