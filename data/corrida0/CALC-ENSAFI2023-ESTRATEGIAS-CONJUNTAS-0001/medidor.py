"""Medición determinista de estrategias conjuntas ENSAFI 2023."""
from __future__ import annotations
import csv, hashlib, io, math, zipfile
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from scipy.stats import t as student_t

CALC = "CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001"
INPUT = "ensafi2023_bd_csv_zip"
ITEMS = [f"P6_10_{i}" for i in range(1, 9)]
VALID = {"1", "2"}
PARENT = [0.415862666480,0.319620126195,0.683069699797,0.097363421894,
          0.104045372303,0.102792917547,0.100740949123,0.021154112843]

def c(x): return "" if x is None else str(x).strip()
def w(x):
    try: x=float(c(x).replace(",",""))
    except ValueError: return None
    return x if math.isfinite(x) and x>0 else None
def r6(x): return None if x is None else round(float(x), 12)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(path):
    with zipfile.ZipFile(path) as z:
        name=next(n for n in z.namelist() if n.rsplit('/',1)[-1]=='TMODULO.csv')
        raw=z.read(name)
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline='')))

def design(rows):
    s=defaultdict(set); missing=0; invalid=0
    for x in rows:
        if w(x.get('FAC_ELE')) is None: invalid+=1; continue
        h,u=c(x.get('EST_DIS')),c(x.get('UPM_DIS'))
        if not h or not u: missing+=1; continue
        s[h].add(u)
    return s, invalid, missing

def ratio(rows, mask, y):
    """Razón y su vector de influencia por UPM; marco completo en varianza."""
    num=den=0.; nv=nn=0
    for x in rows:
        ww=w(x.get('FAC_ELE'))
        if ww is not None and mask(x):
            den+=ww; num+=ww*y(x); nv+=1; nn+=int(bool(y(x)))
    if not den: return {'p':None,'se':None,'lo':None,'hi':None,'den':0,'num':0,'n':0,'nn':0,'z':{}}
    p=num/den; z=defaultdict(float)
    for x in rows:
        ww=w(x.get('FAC_ELE')); h,u=c(x.get('EST_DIS')),c(x.get('UPM_DIS'))
        if ww is not None and h and u and mask(x): z[h,u]+=ww*(y(x)-p)/den
    return {'p':p,'den':den,'num':num,'n':nv,'nn':nn,'z':z}

def variance(z, strata):
    v=0.
    for h,us in strata.items():
        vs=[z.get((h,u),0.) for u in us]; m=len(vs)
        if m>1:
            a=sum(vs)/m; v+=m/(m-1)*sum((q-a)**2 for q in vs)
    return v
def attach(e,strata,df):
    if e['p'] is None: e.update(se=None,lo=None,hi=None,estado='NO-ESTIMABLE:DENOMINADOR-NULO'); return e
    if e['p'] in (0.,1.): e.update(se=None,lo=None,hi=None,estado='NO-DISPONIBLE:FRONTERA'); return e
    se=math.sqrt(variance(e['z'],strata)); q=float(student_t.ppf(.975,df))
    e.update(se=se,lo=max(0,e['p']-q*se),hi=min(1,e['p']+q*se),estado='ESTIMABLE:T95-LINEALIZACION')
    return e
def diff(a,b,strata,df):
    if a['p'] is None or b['p'] is None: return None,None,None,None,'NO-ESTIMABLE'
    d=a['p']-b['p']
    if df<=0: return d,None,None,None,'NO-DISPONIBLE:GL'
    z={k:a['z'].get(k,0)-b['z'].get(k,0) for h,us in strata.items() for k in [(h,u) for u in us]}
    se=math.sqrt(variance(z,strata)); q=float(student_t.ppf(.975,df))
    return d,se,d-q*se,d+q*se,'ESTIMABLE:T95-INFLUENCIA-CONJUNTA'
def write(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        o=csv.DictWriter(f,fieldnames=fields);o.writeheader();o.writerows(rows)

def medir(inputs, contrato):
    rows=read(inputs[INPUT]['ruta_absoluta'])
    need={'LLAVEMOD','P6_9','FAC_ELE','EST_DIS','UPM_DIS',*ITEMS}
    if not rows or need-set(rows[0]): raise ValueError('COLUMNAS-AUSENTES')
    if len({c(x['LLAVEMOD']) for x in rows})!=len(rows): raise ValueError('LLAVEMOD-NO-UNICA')
    strata,bad,miss=design(rows); df=sum(max(0,len(x)-1) for x in strata.values())
    eligible=[x for x in rows if c(x['P6_9'])=='2']; ew=[(x,w(x['FAC_ELE'])) for x in eligible]; mass=sum(q for _,q in ew if q)
    full=lambda x: c(x['P6_9'])=='2' and all(c(x[i]) in VALID for i in ITEMS)
    pair=lambda x,i,j: c(x['P6_9'])=='2' and c(x[i]) in VALID and c(x[j]) in VALID
    outdir=Path(__file__).resolve().parents[3]/contrato['parametros']['directorio_salida']
    cov=[]
    for k in range(9):
        rr=[x for x in eligible if sum(c(x[i]) not in VALID for i in ITEMS)==k]; mm=sum(w(x['FAC_ELE']) or 0 for x in rr)
        cov.append({'respuestas_desconocidas':k,'n':len(rr),'masa':mm,'proporcion_masa':mm/mass if mass else None})
    complete=ratio(rows,full,lambda x:1.); attach(complete,strata,df)
    counts=[]; count_est=[]
    for k in range(9):
        e=ratio(rows,full,lambda x,k=k: float(sum(c(x[i])=='1' for i in ITEMS)==k));attach(e,strata,df);count_est.append(e)
        counts.append({'conteo':k,'n_numerador':e['nn'],'masa_numerador':e['num'],'masa_denominador':e['den'],'p':r6(e['p']),'ee':r6(e['se']),'ic95_lo':r6(e['lo']),'ic95_hi':r6(e['hi']),'estado':e['estado']})
    mean=ratio(rows,full,lambda x:sum(c(x[i])=='1' for i in ITEMS));attach(mean,strata,df)
    for t in (1,2,4):
        e=ratio(rows,full,lambda x,t=t:float(sum(c(x[i])=='1' for i in ITEMS)>=t));attach(e,strata,df)
        counts.append({'conteo':f'>={t}','n_numerador':e['nn'],'masa_numerador':e['num'],'masa_denominador':e['den'],'p':r6(e['p']),'ee':r6(e['se']),'ic95_lo':r6(e['lo']),'ic95_hi':r6(e['hi']),'estado':e['estado']})
    pairs=[]; sens=[]
    for a,b in combinations(ITEMS,2):
        base=ratio(rows,full,lambda x,a=a,b=b:float(c(x[a])=='1' and c(x[b])=='1')); attach(base,strata,df)
        aa=ratio(rows,full,lambda x,a=a:float(c(x[a])=='1')); bb=ratio(rows,full,lambda x,b=b:float(c(x[b])=='1'))
        n11=base['num']; n10=aa['num']-n11; n01=bb['num']-n11; n00=complete['den']-n11-n10-n01
        pab_a=n11/aa['num'] if aa['num'] else None; pab_b=n11/bb['num'] if bb['num'] else None
        pairs.append({'estrategia_a':a,'estrategia_b':b,'n00_masa':n00,'n01_masa':n01,'n10_masa':n10,'n11_masa':n11,'denominador':complete['den'],'p_ambas':r6(base['p']),'p_b_dado_a':r6(pab_a),'p_a_dado_b':r6(pab_b),'ee':r6(base['se']),'ic95_lo':r6(base['lo']),'ic95_hi':r6(base['hi']),'estado':base['estado']})
        two=ratio(rows,lambda x,a=a,b=b:pair(x,a,b),lambda x,a=a,b=b:float(c(x[a])=='1' and c(x[b])=='1'));attach(two,strata,df)
        d,se,lo,hi,state=diff(two,base,strata,df)
        sens.append({'estrategia_a':a,'estrategia_b':b,'n_dos_validas':two['n'],'masa_dos_validas':two['den'],'cobertura_masa':two['den']/mass if mass else None,'p_ambas_dos_validas':r6(two['p']),'p_ambas_vector_completo':r6(base['p']),'diferencia':r6(d),'ee_diferencia':r6(se),'ic95_lo_diferencia':r6(lo),'ic95_hi_diferencia':r6(hi),'estado':state})
    limits=[]
    for t in (1,2,4):
        low=high=0.
        for x,q in ew:
            if not q: continue
            yes=sum(c(x[i])=='1' for i in ITEMS); unk=sum(c(x[i]) not in VALID for i in ITEMS)
            low+=q*(yes>=t);high+=q*(yes+unk>=t)
        limits.append({'umbral':f'>={t}','masa_minima':low,'masa_maxima':high,'p_minima':low/mass if mass else None,'p_maxima':high/mass if mass else None,'estado':'LIMITE-IDENTIFICACION;NO-IC'})
    files={'cobertura.csv':cov,'conteos.csv':counts,'parejas.csv':pairs,'sensibilidad_parejas.csv':sens,'limites_faltantes.csv':limits}
    for fn,data in files.items(): write(outdir/fn,list(data[0]),data)
    marginal=[ratio(rows,full,lambda x,i=i:float(c(x[i])=='1'))['p'] for i in ITEMS]
    partition=sum(x['p'] or 0 for x in count_est)
    control_parent=max(abs(x-y) for x,y in zip(marginal,PARENT))
    return {'RESULT-ENSAFI-EC-G-N-MARCO':len(rows),'RESULT-ENSAFI-EC-G-N-ELEGIBLES':len(eligible),'RESULT-ENSAFI-EC-G-MASA-ELEGIBLES':r6(mass),'RESULT-ENSAFI-EC-G-COBERTURA-VECTOR':r6(complete['den']/mass if mass else None),'RESULT-ENSAFI-EC-G-MEDIA-CONTEO-COMPLETO':r6(mean['p']),'RESULT-ENSAFI-EC-G-CONTROL-PARTICION':'COINCIDE' if abs(partition-1)<1e-10 else 'DISCREPA','RESULT-ENSAFI-EC-G-CONTROL-MEDIA-MARGINALES':'COINCIDE' if abs(mean['p']-sum(marginal))<1e-10 else 'DISCREPA','RESULT-ENSAFI-EC-G-CONTROL-PADRE':'COINCIDE' if control_parent<1e-10 else 'DISCREPA','RESULT-ENSAFI-EC-G-ESTRATOS':len(strata),'RESULT-ENSAFI-EC-G-UPM':sum(map(len,strata.values())),'RESULT-ENSAFI-EC-G-GL':df,'RESULT-ENSAFI-EC-G-SALIDA-COBERTURA':str(outdir.relative_to(Path(__file__).resolve().parents[3])/'cobertura.csv'),'RESULT-ENSAFI-EC-G-SALIDA-CONTEOS':str(outdir.relative_to(Path(__file__).resolve().parents[3])/'conteos.csv'),'RESULT-ENSAFI-EC-G-SALIDA-PAREJAS':str(outdir.relative_to(Path(__file__).resolve().parents[3])/'parejas.csv'),'RESULT-ENSAFI-EC-G-SALIDA-SENSIBILIDAD':str(outdir.relative_to(Path(__file__).resolve().parents[3])/'sensibilidad_parejas.csv'),'RESULT-ENSAFI-EC-G-SALIDA-LIMITES':str(outdir.relative_to(Path(__file__).resolve().parents[3])/'limites_faltantes.csv')}
