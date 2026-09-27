"""Reconstrucción independiente a partir exclusivamente de entrada y raw."""
import csv, io, json, zipfile, hashlib, sys
from pathlib import Path
from collections import Counter
import numpy as np
BASE = Path(__file__).resolve().parent
RAW = Path(sys.argv[1]) if len(sys.argv)>1 else Path('/raw')
def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def dump(name, obj):
    (BASE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def tsv(name, rows, fields):
    with (BASE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def outcome(values):
    return 1 if '1' in values else 0 if all(v=='2' for v in values) else -1

def main():
    assert np.__version__=='2.3.5'
    manifest=json.loads((BASE/'entrada/manifiesto.json').read_text())
    for name,digest in manifest['archivos'].items(): assert sha(BASE/'entrada'/name)==digest, name
    inputs=json.loads((BASE/'entrada/insumos.json').read_text())
    inventory=[]
    for item in inputs:
        p=RAW/(item['id']+('.zip' if item['id'].endswith('zip') else '.pdf'))
        digest=sha(p);assert digest==item['sha256'],p
        inventory.append(dict(entrada=item,ruta=str(p),sha256_observado=digest,bytes=p.stat().st_size))
    z=zipfile.ZipFile(RAW/'endireh2021_bd_csv_zip.zip')
    entries=[]
    for n in z.namelist():
        with z.open(n) as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
        entries.append(dict(entrada=n,bytes=z.getinfo(n).file_size,sha256=digest))
    dump('recibo.json',dict(manifiesto_sha256=sha(BASE/'entrada/manifiesto.json'),manifiesto_recibido=manifest,insumos=inventory,entradas_zip=entries,acceso='Solo se leyeron /entrada y /raw como fuentes; sin revelación ni consulta al preparador. No se inspeccionaron reservas externas.',rotulo='REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA',nota_rotulo='Rótulo conservador: no se certifica aislamiento de otras reservas por el entorno; no se accedió a ellas.'))
    def rows(name):return csv.DictReader(io.TextIOWrapper(z.open('bd_endireh_2021_csv/'+name),encoding='latin1'))
    demo={}
    for r in rows('TSDem.csv'):
        assert r['ID_PER'] not in demo
        demo[r['ID_PER']]=(r['EDAD'],r['NIV'],r['SEXO'])
    cols=['ID_PER','EST_DIS','UPM_DIS','FAC_MUJ','P8_2','DOMINIO','CVE_ENT','T_INSTRUM','P8_3_1_1','P8_3_1_2','P8_3_2_1','P8_3_2_2','P8_3_2_3']
    data=[{k:r[k] for k in cols} for r in rows('TB_SEC_VIII.csv')]
    assert len(set(r['ID_PER'] for r in data))==len(data)
    assert all(r['ID_PER'] in demo for r in data)
    design=sorted(set((r['EST_DIS'],r['UPM_DIS']) for r in data));index={v:i for i,v in enumerate(design)}
    psu=np.array([index[(r['EST_DIS'],r['UPM_DIS'])] for r in data]); weights=np.array([float(r['FAC_MUJ']) for r in data])
    assert np.all(weights>0)
    eligible=np.array([r['P8_2']=='1' for r in data])
    ages=np.array([int(demo[r['ID_PER']][0]) for r in data])
    assert all(demo[r['ID_PER']][2]=='2' for r in data)
    assert np.all((ages[eligible]>=15)&(ages[eligible]<=98))
    variables={
        'prueba_ingreso':['P8_3_1_1'],'prueba_continuidad':['P8_3_1_2'],
        'prueba_alguna':['P8_3_1_1','P8_3_1_2'],
        'despido_embarazo':['P8_3_2_1'],'no_renovacion_embarazo':['P8_3_2_2'],
        'reduccion_embarazo':['P8_3_2_3'],'perjuicio_embarazo_alguno':['P8_3_2_1','P8_3_2_2','P8_3_2_3']}
    outcomes={k:np.array([outcome([r[c] for c in v]) for r in data]) for k,v in variables.items()}
    # Marco completo antes de restringir elegibilidad o dominio.
    rng=np.random.Generator(np.random.PCG64(20260923))
    mult=np.zeros((200,len(design)),dtype=np.int32)
    strata=sorted(set(s for s,u in design))
    for s in strata:
        idx=np.array([i for i,(t,u) in enumerate(design) if t==s]);n=len(idx)
        draws=rng.integers(0,n,size=(200,n))
        for b in range(200): mult[b,idx]=np.bincount(draws[b],minlength=n)
    keys=list(csv.DictReader((BASE/'entrada/estimandos.tsv').open(),delimiter='\t'))
    results=[];support=[];replicas=[]
    for k in keys:
        out=dict(llave=k['llave'],punto='',ic95_inf='',ic95_sup='',estado='NO-RECALCULABLE-DESDE-SPEC',motivo='')
        axis,seg=k['eje'],k['segmento']
        if axis=='escolaridad':
            out['motivo']='Falta correspondencia explícita NIV -> ninguno/basica/media_superior/superior; no se adivina recodificación.'
            results.append(out);continue
        if axis=='nacional':
            assert seg=='MX';domain=np.ones(len(data),dtype=bool)
        elif axis=='edad':
            lo,hi={'15-29':(15,29),'30-44':(30,44),'45-59':(45,59),'60+':(60,98)}[seg];domain=(ages>=lo)&(ages<=hi)
        elif axis in ('localidad','entidad','pareja'):
            col={'localidad':'DOMINIO','entidad':'CVE_ENT','pareja':'T_INSTRUM'}[axis]
            domain=np.array([r[col]==seg for r in data])
        else: raise ValueError(axis)
        y=outcomes[k['conducta']];known=eligible&domain&(y>=0)
        den=np.bincount(psu[known],weights=weights[known],minlength=len(design))
        num=np.bincount(psu[known],weights=weights[known]*y[known],minlength=len(design))
        rd=mult@den;rn=mult@num
        n=int(known.sum());upm=int(np.count_nonzero(den));fail=[]
        if n<100:fail.append('n conocido <100')
        if upm<5:fail.append('UPM con casos conocidos <5')
        if den.sum()==0 or np.any(rd==0):fail.append('denominador cero')
        if den.sum()>0 and np.all(rd>0):
            p=float(num.sum()/den.sum());reps=rn/rd
            low,high=np.quantile(reps,[.025,.975],method='linear');cv=float(np.std(reps,ddof=1)/p) if p>0 else None
            if high-low>.20:fail.append('ancho IC >0.20')
            if p>0 and cv>.30:fail.append('CV >0.30')
            for b,v in enumerate(reps):replicas.append(dict(llave=k['llave'],replica=b+1,proporcion=float(v)))
            if not fail:out.update(punto=p,ic95_inf=float(low),ic95_sup=float(high),estado='RECONSTRUIDO')
        else:cv=None
        out['motivo']='; '.join(fail)
        if fail:out['motivo']='Estimación suprimida por regla de publicación de spec: '+out['motivo']
        results.append(out)
        support.append(dict(llave=k['llave'],n_conocido=n,upm_con_casos=upm,denominador_ponderado=float(den.sum()),cv=cv,publicable=not fail,motivo=out['motivo']))
    assert len(results)==len(keys)==len(set(r['llave'] for r in results))
    for r in results:
        assert (r['estado']=='RECONSTRUIDO')==(r['punto']!='')
        assert r['punto']!='' or r['motivo']
    tsv('reconstruccion.tsv',results,['llave','punto','ic95_inf','ic95_sup','estado','motivo'])
    tsv('soporte.tsv',support,['llave','n_conocido','upm_con_casos','denominador_ponderado','cv','publicable','motivo'])
    tsv('replicas.tsv',replicas,['llave','replica','proporcion'])
    dump('ejecucion.json',dict(python=sys.version,numpy=np.__version__,semilla=20260923,rng='PCG64; Generator.integers',replicas=200,filas_modulo=len(data),elegibles=int(eligible.sum()),estratos=len(strata),upm=len(design),estados=dict(Counter(r['estado'] for r in results))))
    print(json.dumps(Counter(r['estado'] for r in results)))
if __name__=='__main__':main()
