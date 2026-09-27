#!/usr/bin/env python3
"""Verifica cobertura, cifras e IC publicados sin generar un nuevo bootstrap."""
from pathlib import Path
import json
import zipfile
import numpy as np
import pandas as pd

base = Path(__file__).resolve().parent
keys = pd.read_csv(base/'entradas/estimandos.tsv',sep='\t',dtype=str)
r = pd.read_csv(base/'reconstruccion.tsv',sep='\t',keep_default_na=False)
b = pd.read_csv(base/'replicas_publicables.tsv',sep='\t',index_col=0,float_precision='round_trip')
assert list(keys.llave) == list(r.llave) and r.llave.is_unique
assert b.shape == (500,138)
assert set(r.estado) == {'RECONSTRUIDO'}
assert r.motivo.eq('').all()
z = zipfile.ZipFile('/raw/endireh2021_bd_csv_zip.zip')
def read(name, cols):
    return pd.read_csv(z.open('bd_endireh_2021_csv/'+name+'.csv'),usecols=cols,dtype=str,encoding='latin1',keep_default_na=False)
d = read('TB_SEC_XV',['ID_PER','T_INSTRUM','FAC_MUJ','DOMINIO','CVE_ENT','P15_1AB_3','P15_1AB_7'])
d = d[d.T_INSTRUM.isin(['A1','A2'])]
d = d.merge(read('TB_SEC_IV',['ID_PER','P4_11']),on='ID_PER',validate='one_to_one')
d = d.merge(read('TSDem',['ID_PER','EDAD','NIV']),on='ID_PER',validate='one_to_one')
d['age'] = pd.to_numeric(d.EDAD)
d['w'] = pd.to_numeric(d.FAC_MUJ)
d = d[d.age.between(15,120) & d.w.gt(0) & d.ID_PER.ne('')]
maxdiff = 0.
for key, result in zip(keys.to_dict('records'),r.to_dict('records')):
    axis, seg = key['eje'],key['segmento']
    if axis == 'nacional': mask = pd.Series(True,index=d.index)
    elif axis == 'edad':
        lo,hi = {'15-29':(15,29),'30-44':(30,44),'45-59':(45,59),'60+':(60,120)}[seg]
        mask = d.age.between(lo,hi)
    elif axis == 'escolaridad':
        mask = d.NIV.isin({'ninguno':['00'],'basica':['01','02','03','05','06'],'media_superior':['04','07','08'],'superior':['09','10','11']}[seg])
    else: mask = d[{'localidad':'DOMINIO','pareja':'T_INSTRUM','entidad':'CVE_ENT'}[axis]].eq(seg)
    col = {'dinero_libre':'P4_11','decide_sobre_dinero_ella':'P15_1AB_3','decide_gasto_ella':'P15_1AB_7'}[key['conducta']]
    valid_codes = ['1','2'] if col == 'P4_11' else ['1','2','3','4','5']
    yes_codes = ['1'] if col == 'P4_11' else ['1','4','5']
    sub = d[mask & d[col].isin(valid_codes)]
    direct = sub.loc[sub[col].isin(yes_codes),'w'].sum()/sub.w.sum()
    diff = abs(direct-float(result['punto']))
    assert diff < 1e-14
    maxdiff = max(maxdiff,diff)
    sample = b[key['llave']].to_numpy()
    low,high = np.quantile(sample,[.025,.975],method='linear')
    assert abs(low-float(result['ic95_inf'])) < 1e-14
    assert abs(high-float(result['ic95_sup'])) < 1e-14
    assert high-low <= .20
    assert np.std(sample,ddof=1)/direct <= .30
checks = {'llaves_verificadas':len(r),'puntos_con_sumas_directas':len(r),
          'IC_verificados_desde_replicas_congeladas':len(r),
          'max_diferencia_punto':maxdiff,'nuevos_remuestreos':0}
(base/'verificacion.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False))
