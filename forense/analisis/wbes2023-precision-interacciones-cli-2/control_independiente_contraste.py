"""Control independiente, sin importar el medidor sellado."""
import csv, hashlib, io, math, zipfile
from pathlib import Path
import pandas as pd
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[3]
RAW=ROOT/'data/raw/WBES_Mexico2023_Data.zip'
OUT=Path(__file__).with_name('wbes2023-fiscal-operacion-complemento.csv')
with zipfile.ZipFile(RAW) as z:
    f=pd.read_stata(io.BytesIO(z.read('Mexico-2023-full-data.dta')),columns=['idstd','strata','wmedian','j3','j5','j13','j15'],convert_categoricals=False)
def yes(x): return x==1
def valid(x): return x.isin([1,2])
common=yes(f.j3)&yes(f.j13); both=common&valid(f.j5)&valid(f.j15); w=f.wmedian
den=float(w[both].sum()); yf=(both&yes(f.j5)).astype(float); yo=(both&yes(f.j15)).astype(float)
pf=float((w*yf).sum()/den); po=float((w*yo).sum()/den)
af=w*(yf-pf*both.astype(float))/den; ao=w*(yo-po*both.astype(float))/den
def quad(a,b,average):
    vals=[]; single=0
    for _,ix in f.groupby('strata').groups.items():
        x=a.loc[ix]; y=b.loc[ix]; n=len(x)
        if n==1: single+=1; continue
        vals.append(n/(n-1)*float(((x-x.mean())*(y-y.mean())).sum()))
    v=sum(vals)
    return v*(len(vals)+single)/len(vals) if average else v
rows=[]; df=int(sum(len(x)-1 for _,x in f.groupby('strata')))
for name,av in [('SINGLETON-CERTEZA',False),('SINGLETON-AVERAGE',True)]:
    var=quad(af-ao,af-ao,av); cov=quad(af,ao,av); se=math.sqrt(max(0,var)); q=t.ppf(.975,df)
    rows.append({'escenario_singleton':name,'n_doblemente_expuestos':int(common.sum()),'n_doble_valido':int(both.sum()),'masa_doble_expuesta':float(w[common].sum()),'denominador_comun':den,'numerador_fiscal':float((w*yf).sum()),'numerador_operacion':float((w*yo).sum()),'punto_fiscal':pf,'punto_operacion':po,'diferencia_fiscal_menos_operacion':pf-po,'covarianza_diseno':cov,'ee_diferencia':se,'ic95_inferior':pf-po-q*se,'ic95_superior':pf-po+q*se,'grados_libertad':df})
with OUT.open('w',newline='',encoding='utf-8') as h:
    wr=csv.DictWriter(h,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
print(hashlib.sha256(OUT.read_bytes()).hexdigest())
