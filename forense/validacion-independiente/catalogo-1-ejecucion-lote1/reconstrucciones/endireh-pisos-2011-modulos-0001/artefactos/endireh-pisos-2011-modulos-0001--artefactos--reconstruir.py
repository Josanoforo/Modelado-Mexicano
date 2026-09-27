#!/usr/bin/env python3
"""Reconstrucción independiente ENDIREH 2011, sin resultados de referencia."""
import argparse, collections, csv, hashlib, json, platform, re, shutil, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from leer_fd import read_cells

KEY = ['CONTROL', 'VIV_SEL', 'HOGAR', 'R_SEL_M']
DESIGN = ['FAC_PER', 'DOMINIO', 'EST_DIS', 'UPM_DIS', 'CVE_ENT']
SEED = 20260923
B = 200

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, obj): Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def recode(x, yes=(1,), no=(2,)):
    return np.where(np.isin(x, yes), 1., np.where(np.isin(x, no), 0., np.nan))
def union(xs):
    x = np.asarray(xs)
    return np.where(np.any(x == 1, axis=0), 1., np.where(np.all(x == 0, axis=0), 0., np.nan))
def restrict(x, eligible): return np.where(eligible, x, np.nan)
def multiple_codes(xs, positive, valid):
    """Lista de respuestas múltiples: al menos un código válido define respuesta."""
    x = np.asarray(xs)
    return np.where(np.any(np.isin(x, positive), axis=0), 1.,
                    np.where(np.any(np.isin(x, valid), axis=0), 0., np.nan))

def read(z, name, cols):
    d = pd.read_csv(z.open('bd_endireh_2011_csv/'+name+'.csv'), dtype=str,
                    keep_default_na=False, encoding='latin1', usecols=cols)
    return d.apply(lambda x: x.str.strip())

def load(z):
    demo = read(z, 'TSDem', lambda c: c in KEY[:-1]+['N_REN','EDAD','NIV'])
    demo = demo.rename(columns={'N_REN':'R_SEL_M'})
    assert not demo.duplicated(KEY).any(), 'Identidad demográfica no única'
    frames = []; audit = {}
    for letter, stem, parts in [('A','TUnidas',3),('B','TDunida',3),('C','TSolter',2)]:
        # Sólo variables del método, claves y diseño; no otros indicadores.
        def select(c):
            return c in KEY+DESIGN or bool(re.match(letter+r'P(?:2_(?:1$|2$|3_1$|5_|6_|7_|8_|9_|10_|12_)|3_(?:7_|1_)|4_1$|6_(?:1_|3_|4_|5_|7_|8_|11_)|7_1(?:_|$)|8_1$)', c))
        d = None
        for part in range(1,parts+1):
            t = read(z, stem+str(part), select)
            assert not t.duplicated(KEY).any(), 'Identidad de módulo no única'
            assert not (t[KEY]=='').any().any(), 'Clave incompleta'
            if d is None: d=t
            else:
                common = [c for c in t if c not in KEY and c in d]
                check = d[KEY+common].merge(t[KEY+common],on=KEY,how='outer',validate='one_to_one',indicator=True)
                assert (check['_merge']=='both').all(), 'Partes de módulo con claves distintas'
                for c in common: assert (check[c+'_x']==check[c+'_y']).all(), 'Discordancia '+c
                d=d.merge(t.drop(columns=common),on=KEY,how='inner',validate='one_to_one')
        d=d.merge(demo,on=KEY,how='left',validate='one_to_one',indicator=True)
        audit[letter]={'mujeres':len(d),'sin_demografia':int((d['_merge']!='both').sum())}
        # Una falta demográfica no se imputa y sólo excluye los cortes correspondientes.
        d=d.drop(columns='_merge'); d['modulo']=letter
        frames.append(d)
    allkeys=pd.concat([f[KEY] for f in frames],ignore_index=True)
    assert not allkeys.duplicated(KEY).any(), 'Identidad compartida entre A/B/C'
    return frames,audit

def variables(d):
    l=d['modulo'].iloc[0]; n=len(d)
    def v(name):
        return pd.to_numeric(d[l+'P'+name],errors='coerce').to_numpy(dtype=float)
    def item(name,yes=(1,),no=(2,)): return recode(v(name),yes,no)
    def items(prefix,rr,yes=(1,),no=(2,)): return [item(prefix+str(i),yes,no) for i in rr]
    eligible=np.isin(v('4_1'),[1,2]) if l=='C' else np.ones(n,dtype=bool)
    ranges=({'alguna':range(1,22),'fisica':range(12,19),'emocional_control':range(1,11),
             'economica_patrimonial':[11],'sexual':range(19,22)} if l=='C' else
            {'alguna':range(1,31),'fisica':range(20,28),'emocional_control':range(1,14),
             'economica_patrimonial':range(14,20),'sexual':range(28,31)})
    out={}
    for group,rr in ranges.items():
        life=[v('6_1_'+str(i)) for i in rr]
        annual=[np.where(x==4,4,v('6_3_'+str(i))) for i,x in zip(rr,life)]
        for period,xx in [('vida',life),('desde_octubre_2010',annual)]:
            out['pareja_'+group+'_'+period]=restrict(union([recode(x,(1,2,3),(4,)) for x in xx]),eligible)
    affected=out['pareja_alguna_vida']==1
    helpq='6_4_' if l=='C' else '6_5_'
    aid=items(helpq,range(1,7))
    out['pareja_ayuda_institucional']=restrict(union(aid),affected)
    for i in range(1,7):out[f'pareja_institucion_{i:02}']=restrict(aid[i-1],affected)
    if l=='C':out['pareja_informo_familia']=restrict(item('6_4_7'),affected)
    else:
        results=[restrict(v(f'6_8_{i}_{j}'),v(helpq+str(i))==1) for i in range(1,7) for j in (1,2)]
        out['pareja_denuncia_ultima_visita']=restrict(multiple_codes(results,[1],range(1,11)),affected & (out['pareja_ayuda_institucional']==1))
    reasonq='6_7_' if l=='C' else '6_11_'
    reasons=[v(reasonq+str(i)) for i in range(1,14)]
    anyreason=np.any([x==i for i,x in enumerate(reasons,1)],axis=0)
    noaid=affected & (out['pareja_ayuda_institucional']==0) & anyreason
    for i,x in enumerate(reasons,1):
        out[f'pareja_razon_{i:02}']=restrict(np.where(x==i,1.,np.where(np.isnan(x),0.,np.nan)),noaid)
    out['despojo_bienes_vida']=union(items('3_1_' if l=='C' else '3_7_',range(1,4)))
    out['prueba_embarazo_vida']=item('2_1')
    out['perjuicio_embarazo_vida']=item('2_2')
    work=v('2_3_1')==1
    discr=[restrict(x,work) for x in items('2_5_',range(1,6))]
    out['discriminacion_laboral_desde_octubre_2010']=union(discr)
    for i,x in enumerate(discr,1):out[f'discriminacion_laboral_item_{i:02}']=x
    if l=='A':
        out['decision_gasto']=item('7_1_6',(1,3),(2,))
        out['decision_su_dinero']=item('7_1_3',(1,3),(2,))
        out['dinero_libre']=item('8_1')
    if l=='B':out['dinero_libre']=item('7_1')
    if l=='C':
        for i in range(1,8):out[f'permiso_{i:02}']=restrict(item('7_1_'+str(i),(1,),(2,3)),eligible)
    domains=[('familiar_agresor','7',range(1,7),range(1,17)),
             ('laboral_agresor','7',[7,8],range(1,17)),
             ('escolar_agresor','7',[9,10,11],range(1,17)),
             ('comunitaria_lugar','8',[1,6,7,8],range(1,10)),
             ('escolar_lugar','8',[2],range(1,10)),
             ('laboral_lugar','8',[3,4],range(1,10))]
    acts=[v('2_6_'+str(i)) for i in range(1,13)]
    for domain,q,codes,valid in domains:
        life=[]; year=[]
        for i,act in enumerate(acts,1):
            a=np.array([v(f'2_{q}_{i}_{j}') for j in (1,2)])
            t=np.array([v(f'2_9_{i}_{j}') for j in (1,2)])
            known=np.isin(a,valid); match=np.isin(a,codes)
            # Segunda casilla opcional vacía no es un agresor/lugar desconocido.
            complete=np.any(known,axis=0)&np.all(known|np.isnan(a),axis=0)
            base=np.where(np.any(match,axis=0),1.,np.where(complete,0.,np.nan))
            current=np.any(match&(t==1),axis=0)
            no_current=complete & np.all(~match|(t==2),axis=0)
            life.append(np.where(act==2,0.,np.where(act==1,base,np.nan)))
            year.append(np.where(act==2,0.,np.where(act==1,np.where(current,1.,np.where(no_current,0.,np.nan)),np.nan)))
        out['externo_'+domain+'_vida']=union(life)
        out['externo_'+domain+'_desde_octubre_2010']=union(year)
    subaffected=union([recode(x) for x in acts[:9]])==1
    requests=[restrict(v(f'2_10_{i}_{j}'),acts[i-1]==1) for i in range(1,10) for j in (1,2)]
    out['externo_ayuda_autoridad']=restrict(multiple_codes(requests,range(1,10),range(1,12)),subaffected)
    out['externo_informo_familia']=restrict(multiple_codes(requests,[10],range(1,12)),subaffected)
    results=[]
    for i in range(1,10):
        for j in (1,2):
            attended=(acts[i-1]==1)&np.isin(v(f'2_10_{i}_{j}'),range(1,10))
            for k in (2*j-1,2*j):results.append(restrict(v(f'2_12_{i}_{k}'),attended))
    out['externo_denuncia_ultima_visita']=restrict(multiple_codes(results,[1],range(1,9)),subaffected & (out['externo_ayuda_autoridad']==1))
    return out

def design(z,frames):
    # Marco completo observado en vivienda, incluso UPM sin mujeres contribuyentes.
    frame=read(z,'TViviend',lambda c:c in ['EST_DIS','UPM_DIS'])
    pairs=sorted(set(map(tuple,frame.to_numpy())))
    assert all(h and u for h,u in pairs)
    idx={p:i for i,p in enumerate(pairs)}
    groups=collections.defaultdict(list)
    for i,(h,u) in enumerate(pairs):groups[h].append(i)
    rng=np.random.Generator(np.random.PCG64(SEED))
    multiplicity=np.zeros((B,len(pairs)),dtype=np.float64)
    # Estratos lexicográficos; dentro, UPM lexicográficas; 200 filas por estrato.
    for h,indices in sorted(groups.items()):
        m=len(indices); samples=rng.integers(0,m,size=(B,m))
        for b in range(B):multiplicity[b,indices]=np.bincount(samples[b],minlength=m)
    woman_idx=np.array([idx[p] for f in frames for p in zip(f.EST_DIS,f.UPM_DIS)])
    module_pairs=set(p for f in frames for p in zip(f.EST_DIS,f.UPM_DIS))
    return multiplicity,woman_idx,{'estratos':len(groups),'upm':len(pairs),'upm_sin_mujeres_modulos':len(set(pairs)-module_pairs),'estratos_una_upm':sum(len(g)==1 for g in groups.values())}

def segments(d):
    age=pd.to_numeric(d.EDAD,errors='coerce').to_numpy()
    s={('nacional','MX'):np.ones(len(d),bool)}
    for name,lo,hi in [('15-29',15,29),('30-44',30,44),('45-59',45,59),('60+',60,97)]:s['edad',name]=(age>=lo)&(age<=hi)
    for name,codes in [('ninguno',['00']),('basica',['01','02','03','05']),('media_superior',['04','06','07']),('superior',['08','09'])]:s['escolaridad',name]=d.NIV.isin(codes).to_numpy()
    for axis,column,values in [('localidad','DOMINIO',['U','R']),('pareja','modulo',['A','B','C']),('entidad','CVE_ENT',[f'{i:02}' for i in range(1,33)])]:
        for value in values:s[axis,value]=(d[column]==value).to_numpy()
    return s

def estimate(y,mask,w,upm,mult):
    ok=mask & np.isfinite(y); n=int(ok.sum()); nupm=len(np.unique(upm[ok]))
    # No persiste puntos ni réplicas si no supera publicación.
    if n<100 or nupm<5:return None, f'SUPRIMIDO-POR-SPEC: n_conocido={n}; UPM_contribuyentes={nupm}; exige n>=100 y UPM>=5'
    den=np.bincount(upm[ok],weights=w[ok],minlength=mult.shape[1])
    num=np.bincount(upm[ok],weights=w[ok]*y[ok],minlength=mult.shape[1])
    p=num.sum()/den.sum(); rd=mult@den
    if np.any(rd<=0):return None,'Método insuficiente: réplica con denominador cero; spec no define su tratamiento'
    reps=(mult@num)/rd
    lo,hi=np.quantile(reps,[.025,.975],method='linear')
    cv=np.std(reps,ddof=1)/p if p>0 else 0.
    if hi-lo>.20 or (p>0 and cv>.30):
        return None,'SUPRIMIDO-POR-SPEC: incumple ancho IC<=0.20 o CV<=0.30; punto y réplicas no publicados'
    return (float(p),float(lo),float(hi),reps),''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--entrada',type=Path,default=Path('/entrada'));ap.add_argument('--raw',type=Path,default=Path('/raw'));ap.add_argument('--salida',type=Path,default=Path(__file__).parent)
    args=ap.parse_args(); out=args.salida;out.mkdir(exist_ok=True,parents=True)
    assert not (out/'reconstruccion.tsv').exists(), 'No sobrescribir primer resultado'
    manifest=json.loads((args.entrada/'manifiesto.json').read_text())
    hashes={p.name:sha(p) for p in sorted(args.entrada.iterdir()) if p.is_file()}
    for name,digest in manifest['archivos'].items():assert hashes[name]==digest,'Hash de entrada distinto: '+name
    receipt={'manifiesto_sha256':hashes['manifiesto.json'],'manifiesto_recibido':manifest,'entradas_sha256':hashes,'insumos':[],'resultados_esperados_consultados':False,'revelacion_solicitada':False}
    for spec in json.loads((args.entrada/'insumos.json').read_text()):
        candidates=list(args.raw.glob(spec['id']+'.*'));assert len(candidates)==1,'Acceso/identidad insumo: '+spec['id']
        p=candidates[0]; digest=sha(p);assert digest==spec['sha256'],'Hash insumo distinto'
        receipt['insumos'].append({'entrada_recibida':spec,'ruta_efectiva':str(p),'sha256_calculado':digest,'hash_verificado':True})
    ecopy=out/'entrada';ecopy.mkdir(exist_ok=True)
    for p in args.entrada.iterdir():
        if p.is_file():shutil.copyfile(p,ecopy/p.name)
    dump(out/'recibo.json',receipt)
    # Verifica presencia de las variables clave en el FD sin guardar la documentación.
    fd=read_cells(args.raw/'endireh_2011_fd_endireh11.xls')
    fdvars={v for s,r,c,v in fd if c==4}
    assert set(KEY+['N_REN','EDAD','NIV']+[c for c in DESIGN if c!='CVE_ENT'])<=fdvars
    # CVE_ENT es columna explícita del CSV; no aparece en este FD.
    estimands=list(csv.DictReader((args.entrada/'estimandos.tsv').open(),delimiter='\t'))
    assert len({e['llave'] for e in estimands})==len(estimands)
    with zipfile.ZipFile(args.raw/'endireh_2011_bd_endireh_2011_csv.zip') as z:
        inventory=[]
        for info in z.infolist():
            with z.open(info) as f:
                h=hashlib.sha256()
                for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
            inventory.append({'entrada':info.filename,'bytes':info.file_size,'sha256':h.hexdigest()})
        dump(out/'inventario_zip.json',inventory)
        frames,audit=load(z);print('Uniones verificadas',audit,flush=True)
        vv=[variables(f) for f in frames]
        m,ui,da=design(z,frames)
    d=pd.concat([f[KEY+DESIGN+['EDAD','NIV','modulo']] for f in frames],ignore_index=True)
    w=pd.to_numeric(d.FAC_PER,errors='raise').to_numpy(dtype=float);assert np.all(np.isfinite(w)&(w>0))
    masks=segments(d); names=set().union(*(v.keys() for v in vv))
    y={name:np.concatenate([v.get(name,np.full(len(f),np.nan)) for v,f in zip(vv,frames)]) for name in names}
    dump(out/'ejecucion.json',{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'semilla':SEED,'replicas':B,'rng':'Generator(PCG64)','uniones':audit,'diseno':da,'llaves':len(estimands),'fuente_marco_upm':'TViviend: todas las UPM observadas'})
    counts=collections.Counter()
    with (out/'reconstruccion.tsv').open('w') as f,(out/'replicas.tsv').open('w') as g:
        writer=csv.writer(f,delimiter='\t',lineterminator='\n');writer.writerow(['llave','punto','ic95_inf','ic95_sup','estado','motivo'])
        rw=csv.writer(g,delimiter='\t',lineterminator='\n');rw.writerow(['llave']+[f'replica_{i:03}' for i in range(1,B+1)])
        for j,e in enumerate(estimands):
            reason=''; ans=None
            if e['conducta'] not in y:reason='Identidad de conducta no definida en implementación desde spec'
            elif (e['eje'],e['segmento']) not in masks:reason='Identidad de corte no definida por spec'
            else:ans,reason=estimate(y[e['conducta']],masks[e['eje'],e['segmento']],w,ui,m)
            if ans is None:
                state='NO-RECALCULABLE-DESDE-SPEC'; writer.writerow([e['llave'],'','','',state,reason])
            else:
                state='RECONSTRUIDO';p,lo,hi,reps=ans
                writer.writerow([e['llave'],format(p,'.17g'),format(lo,'.17g'),format(hi,'.17g'),state,''])
                rw.writerow([e['llave']]+[format(x,'.17g') for x in reps])
            counts[state]+=1
            if (j+1)%250==0:print('Llaves procesadas',j+1,flush=True)
    dump(out/'resumen.json',dict(counts));print(dict(counts),flush=True)

if __name__=='__main__':main()
