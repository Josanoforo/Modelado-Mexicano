#!/usr/bin/env python3
"""Control independiente: no importa el medidor ni sus funciones."""
import io,json,zipfile,hashlib
from pathlib import Path
import numpy as np,pandas as pd
K=['folioviv','foliohog','id_pobla']; L={'1','12','13','14','17','18','126'}
def rd(z,n,c):
 b=z.read([x for x in z.namelist() if x.lower().endswith(n)][0]); d=pd.read_csv(io.BytesIO(b),encoding='latin-1',dtype=str,keep_default_na=False);d.columns=[x.lstrip('ï»¿').lower() for x in d.columns];return d[c]
def coh(x): return '<=1970' if x<=1970 else '1971-1980' if x<=1980 else '1981-1990' if x<=1990 else '1991+'
def main(zipname,out):
 with zipfile.ZipFile(zipname) as z:
  h=rd(z,'historiavida.csv',K+['anio_retro','anio_nac','edo_civil1']);a=rd(z,'antecedentes.csv',K+['factor_per']);p=rd(z,'persona.csv',K+['sexo']);v=rd(z,'vivienda.csv',['folioviv','est_dis','upm'])
 h['t']=pd.to_numeric(h.anio_retro,errors='coerce');h.edo_civil1=h.edo_civil1.str.strip();q=h[(h.edo_civil1!='0')&(h.edo_civil1!='')&h.t.notna()];q=q[q.t.eq(q.groupby(K).t.transform('min'))];q=q[q.groupby(K).edo_civil1.transform('nunique').eq(1)].drop_duplicates(K)
 d=a.merge(p,on=K).merge(v,on='folioviv').merge(q[K+['anio_nac','edo_civil1']],on=K,how='left');d['w']=pd.to_numeric(d.factor_per);d=d[d.w.gt(0)&np.isfinite(d.w)];d['s']=d.sexo.map({'1':'hombre','2':'mujer'});d['c']=pd.to_numeric(d.anio_nac,errors='coerce').map(lambda x:coh(x) if np.isfinite(x) else 'NA');d['dom']=d.edo_civil1.notna();d['free']=d.edo_civil1.isin(L)
 def pt(x): return float((x.w*x.free).sum()/x.w.sum())
 u=d[d.dom]; point={'total_libre':pt(u),'mujer_libre':pt(u[u.s=='mujer']),'cohorte_1991_mujer_menos_hombre':pt(u[(u.s=='mujer')&(u.c=='1991+')])-pt(u[(u.s=='hombre')&(u.c=='1991+')]),'n_marco':int(len(d))}
 # Diseño independiente: marco completo, conglomerados en estrato; dominio no
 # seleccionado conserva cero porque sólo el numerador/denominador del dominio entra.
 d=d[d.est_dis.notna()&d.upm.notna()].copy();d['cl']=d.est_dis+'|'+d.upm;cl=d[['cl','est_dis']].drop_duplicates().sort_values(['est_dis','cl']).reset_index(drop=True);ix={x:i for i,x in enumerate(cl.cl)};A=np.zeros((len(cl),4));
 for r in d.itertuples():
  if r.dom and r.c=='1991+' and r.s in ('mujer','hombre'):
   j=0 if r.s=='mujer' else 2; A[ix[r.cl],j]+=r.w;A[ix[r.cl],j+1]+=r.w*bool(r.free)
 rng=np.random.Generator(np.random.PCG64(20260919));M=np.zeros((2000,len(cl)))
 for _,g in cl.groupby('est_dis'):
  pos=g.index.to_numpy();draw=rng.integers(0,len(pos),(2000,len(pos)))
  for j in range(len(pos)):M[np.arange(2000),pos[draw[:,j]]]+=1
 X=M@A;vrep=X[:,1]/X[:,0]-X[:,3]/X[:,2]; point['contraste_1991_ee']=float(vrep.std(ddof=1));point['contraste_1991_ic95']=[float(np.percentile(vrep,2.5)),float(np.percentile(vrep,97.5))]
 target=pd.read_csv(Path(out).parent/'tablas'/'contrastes.csv');ref=float(target.loc[target.contraste=='mujer-hombre libre 1991+','diferencia'].iloc[0]);ee=float(target.loc[target.contraste=='mujer-hombre libre 1991+','ee'].iloc[0]);point['diferencias_vs_tabla']={'contraste_abs':abs(point['cohorte_1991_mujer_menos_hombre']-ref),'ee_abs':abs(point['contraste_1991_ee']-ee)};Path(out).write_text(json.dumps(point,indent=2)+'\n')
if __name__=='__main__':
 import sys;main(sys.argv[1],sys.argv[2])
