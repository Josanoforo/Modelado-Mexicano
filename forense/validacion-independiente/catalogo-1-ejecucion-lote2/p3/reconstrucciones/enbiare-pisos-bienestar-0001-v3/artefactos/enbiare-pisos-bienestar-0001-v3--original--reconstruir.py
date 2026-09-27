#!/usr/bin/env python3
"""Reconstrucción estricta de razones identificables; no imputa identidades."""
import csv
import hashlib
import json
import platform
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ENTRY = ROOT / 'entradas'
RAW = Path('/raw')
KEY = ['FOLIO', 'VIV_SEL', 'HOGAR', 'N_REN']
IC_REASON = ('metodo.md menciona receta común por sha256 sin identificarla ni adjuntarla; '
             'no define contrato conservador, orden de estratos/UPM, consumo de PCG64, '
             'remuestreo/tamaño por estrato, tratamiento de denominadores cero ni interpolación de percentiles. '
             'Semilla y 2000 réplicas no determinan los extremos a tolerancia 1e-10.')
MEANS = {'satisfaccion-vida':'PA1', 'escalera-cantril':'PA5',
         'confianza-mayoria-gente':'PB1_01', 'confianza-gente-conocida':'PB1_02',
         'confianza-policia-municipal':'PB1_04', 'confianza-partidos':'PB1_11'}
SCHOOL = {'HASTA-PRIMARIA':['00','01','02'], 'SECUNDARIA':['03','04'],
          'MEDIA-SUPERIOR':['05','06','07'], 'SUPERIOR':['08','09','10']}
LOC = {'100MIL-MAS':'1','15MIL-99MIL':'2','2500-14999':'3','MENOS-2500':'4'}
AGE = {'18-29':(18,29),'30-44':(30,44),'45-59':(45,59),'60-MAS':(60,96)}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def num(frame, col):
    return pd.to_numeric(frame[col],errors='coerce')

def responses(frame, behavior):
    """NaN indica respuesta indeterminada; no se codifica como cero."""
    if behavior in MEANS:
        v=num(frame,MEANS[behavior]); return v.where(v.between(0,10))
    if behavior in ('cuenta-apoyo-familia','cuenta-apoyo-amistades'):
        c='PB2_1' if behavior.endswith('familia') else 'PB2_2'
        return frame[c].map({'1':1.,'2':0.,'3':0.})
    if behavior=='tiene-religion': return frame.PG6.map({'1':1.,'2':0.})
    if behavior=='asiste-servicio-religioso':
        v=frame.PG7.map({'1':1.,'2':0.})
        return v.mask(frame.PG6.eq('2'),0.)
    if behavior=='ansiedad-gad2':
        x=frame[['PD3_1','PD3_2']].apply(pd.to_numeric,errors='coerce')
        return (x.sum(axis=1)>=3).astype(float).where(x.isin([0,1,2,3]).all(axis=1))
    if behavior=='depresion-cesd7':
        x=frame[[f'PD2_{i}' for i in range(1,8)]].apply(pd.to_numeric,errors='coerce')
        valid=x.isin([0,1,2,3]).all(axis=1)
        x['PD2_6']=3-x['PD2_6']; score=x.sum(axis=1)
        a=num(frame,'EDAD'); known=a.between(18,96)
        cut=pd.Series(np.where(a.between(60,96),5,9),index=frame.index)
        v=(score>=cut).astype(float).where(known)
        # Adultos 98: sólo clasificar cuando ambos cortes dan el mismo resultado.
        v=v.mask(a.eq(98)&score.lt(5),0.).mask(a.eq(98)&score.ge(9),1.)
        return v.where(valid)
    raise ValueError('Conducta sin identidad explícita: '+behavior)

def domain(frame, axis, segment):
    if axis=='TOTAL' and segment=='TODOS': return pd.Series(True,index=frame.index)
    if axis=='SEXO': return frame.SEXO.eq({'HOMBRE':'1','MUJER':'2'}[segment])
    if axis=='ESCOLARIDAD': return frame.NIVEL.isin(SCHOOL[segment])
    if axis=='TLOC': return frame.TLOC.eq(LOC[segment])
    if axis=='EDAD': return num(frame,'EDAD').between(*AGE[segment])
    raise ValueError('Eje sin identidad explícita: '+axis+'/'+segment)

def main():
    manifest=json.loads((ENTRY/'manifiesto.json').read_text())
    inventory=[]
    for name,expected in manifest['archivos'].items():
        path=Path('/entrada')/name
        actual=sha(path)
        assert actual==expected, ('Hash de entrada diferente',name)
        if path.suffix!='.pdf': assert sha(ENTRY/name)==actual
        inventory.append({'ruta':str(path),'sha256':actual,'bytes':path.stat().st_size,
                          'incluido_en_commit':path.suffix!='.pdf'})
    inputs=json.loads((ENTRY/'insumos.json').read_text())
    paths={}
    for item in inputs:
        path=RAW/item['id']/Path(item['archivo']).name
        actual=sha(path); assert actual==item['sha256'], ('Hash raw diferente',str(path))
        paths[item['id']]=path
        inventory.append({'ruta':str(path),'sha256':actual,'bytes':path.stat().st_size,
                          'incluido_en_commit':False,'entrada':item})
    with zipfile.ZipFile(paths['enbiare2021_bd_csv_zip']) as archive:
        members=[]
        for info in archive.infolist():
            members.append({'entrada':info.filename,'bytes':info.file_size,
                            'sha256':hashlib.sha256(archive.read(info)).hexdigest()})
        def read(name): return pd.read_csv(archive.open(name),dtype=str,keep_default_na=False)
        chosen=read('TENBIARE.csv'); socio=read('TSDEM.csv')
    duplicate=socio.duplicated(KEY,keep=False)
    joined=chosen.merge(socio.loc[~duplicate,KEY+['SEXO','EDAD','NIVEL']],
                        how='left',on=KEY,indicator=True,validate='many_to_one')
    weight=num(joined,'FAC_ELE')
    design=weight.gt(0)&joined.EST_DIS.ne('')&joined.UPM_DIS.ne('')
    paired=joined['_merge'].eq('both')
    age=num(joined,'EDAD')
    # El diccionario distingue 96=96+, 97=menor no especificado,
    # 98=adulto no especificado, 99=edad no especificada.
    adult=age.between(18,96)|age.eq(98)
    frame=joined.loc[design&paired&adult].copy()
    w=num(frame,'FAC_ELE')
    audit={'tenbiare_filas':len(chosen),'tsdem_filas':len(socio),
           'tsdem_filas_llave_no_unica':int(duplicate.sum()),
           'tenbiare_llaves_duplicadas':int(chosen.duplicated(KEY,keep=False).sum()),
           'G-JOIN-SIN-SOCIODEMOGRAFICO':int((~paired).sum()),
           'diseno_invalido':int((~design).sum()),'adultos_validos':len(frame),
           'edad_98_adulto_sin_tramo':int(frame.EDAD.eq('98').sum()),
           'estratos':frame.EST_DIS.nunique(),
           'pares_estrato_upm':len(frame[['EST_DIS','UPM_DIS']].drop_duplicates())}
    estimands=list(csv.DictReader((ENTRY/'estimandos.tsv').open(),delimiter='\t'))
    assert len({r['llave'] for r in estimands})==len(estimands)
    values={b:responses(frame,b) for b in {r['conducta'] for r in estimands}}
    result=[]
    for row in estimands:
        out=dict(row); behavior=row['conducta']; axis=row['eje']; segment=row['segmento']
        out.update(estado='',motivo='',estimacion='',numerador='',denominador='',n='',
                   unidad_calculada='media' if behavior in MEANS else 'proporcion',
                   ic95_inf='',ic95_sup='',estado_ic='NO-RECALCULABLE-DESDE-SPEC',motivo_ic=IC_REASON,
                   observacion=('unidad de entrada=proporcion; metodo.md exige media 0–10' if behavior in MEANS else ''))
        mask=domain(frame,axis,segment); v=values[behavior]
        reasons=[]
        if axis=='EDAD' and frame.EDAD.eq('98').any():
            reasons.append(f'Hay {int(frame.EDAD.eq("98").sum())} adultos con EDAD=98 (edad no especificada); su pertenencia a este tramo no está determinada y no se especifica excluirlos del estimando. No se imputa tramo.')
        unknown=mask&v.isna()
        if unknown.any():
            reasons.append(f'{int(unknown.sum())} respuestas del dominio no determinadas por la especificación; no se cambia el denominador sin regla. Para CESD7, edad 98 y puntaje 5–8 requieren un corte etario no identificable.')
        if reasons:
            out.update(estado='NO-RECALCULABLE-DESDE-SPEC',motivo=' '.join(reasons))
        else:
            numerator=float((w[mask]*v[mask]).sum()); denominator=float(w[mask].sum())
            if denominator<=0:
                out.update(estado='NO-RECALCULABLE-DESDE-SPEC',motivo='Dominio sin denominador positivo.')
            else:
                out.update(estado='RECONSTRUIDO',estimacion=format(numerator/denominator,'.17g'),
                           numerador=format(numerator,'.17g'),denominador=format(denominator,'.17g'),n=int(mask.sum()))
        result.append(out)
    with (ROOT/'reconstruccion.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(result[0]),delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(result)
    audit['estados']=dict(pd.Series([r['estado'] for r in result]).value_counts().items())
    audit['estados']={k:int(v) for k,v in audit['estados'].items()}
    dump('auditoria.json',audit)
    dump('inventario.json',{'archivos':inventory,'entradas_zip':members})
    receipt={'manifiesto_ruta':'/entrada/manifiesto.json','manifiesto_sha256':sha(ENTRY/'manifiesto.json'),
             'fuentes_permitidas':['/entrada','/raw'],'resultados_esperados_consultados':False,
             'revelacion_solicitada':False,'tolerancia':json.loads((ENTRY/'tolerancia.json').read_text()),
             'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
             'estados':audit['estados'],'alcance':'Razones puntuales identificadas; IC no determinados por la receta suministrada.',
             'artefactos_sha256':{n:sha(ROOT/n) for n in ['reconstruir.py','reconstruccion.tsv','auditoria.json','inventario.json']}}
    dump('recibo.json',receipt)
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
