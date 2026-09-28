#!/usr/bin/env python3
"""Reconstrucción independiente: sólo /entrada e insumos enumerados en /raw."""
import csv
import hashlib
import io
import json
import platform
import shutil
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def save(name, obj):
    (ROOT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def read_data(path, columns):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith('.dta')]
        if len(names) != 1: raise ValueError('No hay un único DTA: '+str(path))
        with z.open(names[0]) as f:
            return pd.read_stata(f, columns=columns, convert_categoricals=False)

def conductas(d):
    def binary(c): return d[c].map({1:1., 2:0.})
    def any_yes(cols):
        v = d[cols]
        return pd.Series(np.where(v.eq(1).any(axis=1), 1., np.where(v.eq(2).all(axis=1),0.,np.nan)), index=d.index)
    never = d.al1.eq(2)
    no12 = never | d.al4.eq(2)
    excessive = pd.Series(np.nan, index=d.index)
    valid = d.al11.isin(range(1,7)) & d.ds2.isin([1,2])
    excessive.loc[valid] = ((d.ds2.eq(1) & d.al11.isin([1,2,3,4])) | (d.ds2.eq(2) & d.al11.isin([1,2,3,4,5]))).loc[valid].astype(float)
    excessive.loc[no12] = 0.
    smoke = d.tb02.map({1:1.,2:1.,3:0.})
    smoke.loc[smoke.isna() & d.tb05.eq(2)] = 0.
    return {
        'alcohol-12m':binary('al4').mask(never,0.),
        'alcohol-30d':binary('al9').mask(no12,0.),
        'alcohol-excesivo-12m':excessive,
        'fuma-actual':smoke,
        'cigarro-electronico-alguna-vez':binary('tb50'),
        'droga-ilegal-alguna-vez':any_yes(['di1'+c for c in 'abcdefghi']),
        'mariguana-alguna-vez':binary('di1a'),
        'droga-medica-sin-receta-alguna-vez':any_yes(['dm1'+c for c in 'abcd']),
        'opiaceos-sin-receta-alguna-vez':binary('dm1a'),
        'consulto-profesional-por-consumo':binary('tp1'),
    }

def segment(d, eje, s):
    if eje=='TOTAL' and s=='TODOS': return pd.Series(True,index=d.index)
    if eje=='EDAD':
        lo, hi = map(int,s.split('-')); return d.ds3.between(lo,hi)
    if eje=='SEXO': return d.ds2.eq({'HOMBRE':1,'MUJER':2}[s])
    if eje=='ESTRATO': return d.estrato.eq({'RURAL':1,'URBANO':2,'METROPOLITANO':3}[s])
    if eje=='ESCOLARIDAD': return d.ds3.ge(18) & d.ds9.isin({'HASTA-PRIMARIA':[1,2],'SECUNDARIA':[3,4],'MEDIA-SUPERIOR':[5,6],'SUPERIOR':[7,8,9]}[s])
    raise ValueError('Segmento sin especificación')

def main():
    manifest = json.loads((ENTRADA/'manifiesto.json').read_text())
    receipt = {'manifiesto_sha256':sha(ENTRADA/'manifiesto.json'), 'entrada':[], 'insumos':[], 'sin_revelacion':True, 'entorno':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__}}
    (ROOT/'entrada').mkdir(exist_ok=True)
    for name, expected in manifest['archivos'].items():
        p=ENTRADA/name
        actual=sha(p)
        if actual != expected: raise ValueError('Hash de entrada no coincide: '+name)
        receipt['entrada'].append({'archivo':name,'sha256':actual})
        if p.suffix.lower() != '.pdf': shutil.copyfile(p,ROOT/'entrada'/name)
    shutil.copyfile(ENTRADA/'manifiesto.json',ROOT/'entrada/manifiesto.json')
    paths={}
    for spec in json.loads((ENTRADA/'insumos.json').read_text()):
        p=RAW/spec['id']/Path(spec['archivo']).name
        actual=sha(p)
        if actual != spec['sha256']: raise ValueError('Hash de insumo no coincide: '+str(p))
        item={**spec,'ruta_local':str(p),'sha256_observado':actual}
        if p.suffix=='.zip':
            with zipfile.ZipFile(p) as z:
                item['entradas_zip']=[]
                for n in z.namelist():
                    h=hashlib.sha256()
                    with z.open(n) as f:
                        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
                    item['entradas_zip'].append({'nombre':n,'sha256':h.hexdigest(),'bytes':z.getinfo(n).file_size})
        receipt['insumos'].append(item)
        if 'Hogar.stata' in p.name: paths['hogar']=p
        if 'Individual.stata' in p.name: paths['individual']=p
    h=read_data(paths['hogar'],['id_hogar','est_var','code_upm','estrato'])
    cols=['id_pers','ds2','ds3','ds9','ponde_ss','al1','al4','al9','al11','tb02','tb05','tb50','tp1']+['di1'+c for c in 'abcdefghi']+['dm1'+c for c in 'abcd']
    d=read_data(paths['individual'],cols)
    audit={'G-FILAS-INDIVIDUAL':len(d),'G-FILAS-HOGAR':len(h),'longitud_id_pers':d.id_pers.str.len().value_counts().to_dict(),'longitud_id_hogar':h.id_hogar.str.len().value_counts().to_dict()}
    unique=~h.id_hogar.duplicated(keep=False) & h.id_hogar.notna()
    audit['G-HOGARES-EXCLUIDOS-NO-UNICOS']=int((~unique).sum())
    # Literal: no strip, coerción numérica, relleno ni llave alternativa.
    d['id_hogar']=d.id_pers.str[:20]
    d=d.merge(h.loc[unique],on='id_hogar',how='left',validate='many_to_one',indicator=True,sort=False)
    audit['G-JOIN-SIN-HOGAR']=int(d._merge.ne('both').sum())
    universe=d.ds3.between(12,65)
    design=d._merge.eq('both') & d.est_var.notna() & d.code_upm.notna() & d.code_upm.ne('') & d.estrato.isin([1,2,3]) & np.isfinite(d.ponde_ss) & d.ponde_ss.gt(0)
    audit['G-FILAS-UNIVERSO']=int(universe.sum())
    audit['G-FILAS-DISENO-VALIDO']=int((universe & design).sum())
    values=conductas(d)
    rows=list(csv.DictReader((ENTRADA/'estimandos.tsv').open(),delimiter='\t'))
    assert len({r['llave'] for r in rows})==len(rows)
    ic_reason='No se entregó ENSANUT §4 ni receta común por sha256: faltan contrato conservador y detalles de remuestreo/orden para reproducción exacta.'
    out=[]
    for r in rows:
        y=values[r['conducta']]
        keep=universe & design & segment(d,r['eje'],r['segmento']) & y.notna()
        n=int(keep.sum()); w=d.loc[keep,'ponde_ss'].to_numpy(dtype=float); yy=y[keep].to_numpy(dtype=float)
        den=float(w.sum()); num=float(np.dot(w,yy))
        possible=n>0 and den>0
        out.append({**r,'estado':'RECONSTRUIDO' if possible else 'NO-RECALCULABLE-DESDE-SPEC','valor':format(num/den,'.17g') if possible else '', 'n':n if possible else '', 'numerador_ponderado':format(num,'.17g') if possible else '', 'denominador_ponderado':format(den,'.17g') if possible else '', 'motivo':'' if possible else 'La llave, universo y diseño declarados no dejan un denominador válido.', 'ic95_inferior':'','ic95_superior':'','estado_ic':'NO-RECALCULABLE-DESDE-SPEC','motivo_ic':ic_reason})
    with (ROOT/'reconstruccion.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(out[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(out)
    audit['estimandos']=len(out)
    audit['estados']=pd.Series([r['estado'] for r in out]).value_counts().to_dict()
    receipt['salidas_sha256']={'reconstruccion.tsv':sha(ROOT/'reconstruccion.tsv'),'reconstruir.py':sha(Path(__file__))}
    save('auditoria.json',audit)
    receipt['salidas_sha256']['auditoria.json']=sha(ROOT/'auditoria.json')
    save('recibo.json',receipt)
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
