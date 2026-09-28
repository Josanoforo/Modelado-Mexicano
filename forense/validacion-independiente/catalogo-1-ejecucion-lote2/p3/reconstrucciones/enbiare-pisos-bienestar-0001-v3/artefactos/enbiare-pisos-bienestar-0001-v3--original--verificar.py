"""Verifica integridad, bordes de codificación y dos razones por vía independiente."""
import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path
import pandas as pd
from reconstruir import responses

root=Path(__file__).resolve().parent
rows=list(csv.DictReader((root/'reconstruccion.tsv').open(),delimiter='\t'))
original=list(csv.DictReader((root/'entradas/estimandos.tsv').open(),delimiter='\t'))
assert len(rows)==len(original)==180
for row,source in zip(rows,original):
    assert all(row[k]==v for k,v in source.items())
    if row['estado']=='RECONSTRUIDO':
        p=float(row['estimacion']); assert math.isfinite(p)
        assert float(row['denominador'])>0
        assert 0<=p<=(10 if row['unidad_calculada']=='media' else 1)
    else:
        assert row['motivo'] and not any(row[c] for c in ['estimacion','numerador','denominador','n'])
    assert row['estado_ic']=='NO-RECALCULABLE-DESDE-SPEC' and row['motivo_ic']
    assert row['ic95_inf']==row['ic95_sup']==''
receipt=json.loads((root/'recibo.json').read_text())
for name,digest in receipt['artefactos_sha256'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
assert hashlib.sha256(Path('/entrada/manifiesto.json').read_bytes()).hexdigest()==receipt['manifiesto_sha256']
# Puntaje 6: negativo a 59, positivo a 60, indeterminado con edad adulta 98.
frame=pd.DataFrame([{**{f'PD2_{i}':'0' for i in range(1,8)},
                     'PD2_1':'3','PD2_6':'0','EDAD':a} for a in ['59','60','98']])
v=responses(frame,'depresion-cesd7')
assert v.iloc[0]==0 and v.iloc[1]==1 and pd.isna(v.iloc[2])
frame.loc[2,'PD2_1']='0' # puntaje 3: ambos cortes negativos
assert responses(frame,'depresion-cesd7').iloc[2]==0
religion=pd.DataFrame({'PG6':['2','1','1','1'],'PG7':['','1','2','']})
v=responses(religion,'asiste-servicio-religioso')
assert v.iloc[:3].tolist()==[0,1,0] and pd.isna(v.iloc[3])
# Vía csv/int, sin pandas ni funciones del estimador; datos comprobados completos.
with zipfile.ZipFile('/raw/enbiare2021_bd_csv_zip/enbiare_2021_base_de_datos_csv.zip') as z:
    raw=list(csv.DictReader(io.TextIOWrapper(z.open('TENBIARE.csv'),encoding='utf-8-sig')))
    denom=sum(int(r['FAC_ELE']) for r in raw)
    numerators={
        'satisfaccion-vida':sum(int(r['FAC_ELE'])*int(r['PA1']) for r in raw),
        'ansiedad-gad2':sum(int(r['FAC_ELE'])*(int(r['PD3_1'])+int(r['PD3_2'])>=3) for r in raw)}
    for behavior,numerator in numerators.items():
        out=next(r for r in rows if r['conducta']==behavior and r['eje']=='TOTAL')
        assert float(out['numerador'])==numerator and float(out['denominador'])==denom
        assert abs(float(out['estimacion'])-numerator/denom)<=1e-10
print('OK: 180 llaves, estados, hashes, cortes CESD7, secuencia religiosa y dos razones independientes.')
