"""PROPUESTO: referencia sintética, sin lector de microdatos/históricos."""
from collections import Counter
from itertools import product
import numpy as np

SEED = 20260923

def prepare(frame, contributions):
    pairs = sorted(set(frame))
    if len(pairs) != len(frame) or any(not h or not u for h,u in pairs):
        raise ValueError('marco duplicado o vacío')
    if set(contributions) - set(pairs):
        raise ValueError('UPM fuera del marco')
    values = np.array([contributions.get(p, (0.,0.)) for p in pairs],dtype=float)
    if np.any(~np.isfinite(values)) or np.any(values[:,1]<0) or np.any(values[:,0]<0) or np.any(values[:,0]>values[:,1]):
        raise ValueError('totales incompatibles con proporción')
    strata = [[i for i,p in enumerate(pairs) if p[0]==h] for h in sorted({p[0] for p in pairs})]
    return pairs, values, strata

def reference(frame, contributions, b=200, seed=SEED):
    if b < 2: raise ValueError('requiere dos réplicas')
    pairs, values, strata = prepare(frame,contributions)
    rng=np.random.Generator(np.random.PCG64(seed))
    reps=[]
    for _ in range(b):
        draw=[i for group in strata for i in rng.choice(group,len(group),replace=True)]
        n,d=values[draw].sum(axis=0)
        reps.append(n/d if d>0 else float('nan'))
    total=values.sum(axis=0); p=total[0]/total[1] if total[1]>0 else float('nan')
    reps=np.array(reps)
    finite=np.isfinite(reps).all() and np.isfinite(p)
    return dict(point=p,replicas=reps,interval=np.quantile(reps,[.025,.975],method='linear') if finite else None,
                se=float(np.std(reps,ddof=1)) if finite else None,
                singleton=sum(len(g)==1 for g in strata),nonestimable=int((~np.isfinite(reps)).sum()))

def exact_law(frame, contributions):
    _,values,strata=prepare(frame,contributions)
    draws=[list(product(g,repeat=len(g))) for g in strata]
    if np.prod([len(x) for x in draws])>100000: raise ValueError('solo sintéticos pequeños')
    counts=Counter()
    for groups in product(*draws):
        idx=[i for g in groups for i in g];n,d=values[idx].sum(axis=0)
        counts[float(n/d) if d>0 else 'NO-ESTIMABLE']+=1
    size=sum(counts.values());return {k:v/size for k,v in counts.items()}

def publicable(n,upm,point,lo,hi,se,nonestimable=0):
    if nonestimable or any(not np.isfinite(v) for v in [point,lo,hi,se]): return False
    if not 0<=lo<=hi<=1 or not 0<=point<=1 or se<0: return False
    return n>=100 and upm>=5 and hi-lo<=.20 and (point==0 or se/point<=.30)
