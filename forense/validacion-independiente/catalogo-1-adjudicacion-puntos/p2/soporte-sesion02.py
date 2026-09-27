"""Seis2011 soporte de universo, sin persistir punto ni IC suprimidos."""
import csv,json,zipfile,hashlib,math
from pathlib import Path
import pandas as pd
B=Path(__file__).resolve().parent
RAW=Path('/home/pc0/astra6-c1-aislado/tanda2-endireh-pisos-2011-modulos-0001/raw/endireh_2011_bd_endireh_2011_csv.zip')
SHA='8ece557b2ac1d78dc0bfdee1d8f9743b2da1e44184be340d22967d60b10d52e5'
KEY=['CONTROL','VIV_SEL','HOGAR','R_SEL_M']
TARGET=[('1919','permiso_03','entidad','01'),('1993','permiso_04','entidad','29'),('2039','permiso_05','entidad','29'),('2067','permiso_06','entidad','11'),('2082','permiso_06','entidad','26'),('606','externo_denuncia_ultima_visita','escolaridad','superior')]
def main():
 h=hashlib.sha256()
 with RAW.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 assert h.hexdigest()==SHA
 totals={(key,new):[0,0.] for key,_,_,_ in TARGET for new in [0,1]}
 with zipfile.ZipFile(RAW) as z:
  def read(name,cols):return pd.read_csv(z.open('bd_endireh_2011_csv/'+name+'.csv'),encoding='latin1',dtype=str,keep_default_na=False,usecols=lambda c:c in cols).apply(lambda s:s.str.strip())
  dem=read('TSDem',KEY[:-1]+['N_REN','EDAD','NIV']).rename(columns={'N_REN':'R_SEL_M'})
  for l,stem,parts in [('A','TUnidas',3),('B','TDunida',3),('C','TSolter',2)]:
   cols=KEY+['FAC_PER','EST_DIS','UPM_DIS','CVE_ENT']+[l+'P'+s for s in ['4_1']+[f'7_1_{i}' for i in [3,4,5,6]]+[f'2_6_{i}' for i in range(1,10)]+[f'2_10_{i}_{j}' for i in range(1,10) for j in [1,2]]+[f'2_12_{i}_{k}' for i in range(1,10) for k in range(1,6)]]
   d=None
   for part in range(1,parts+1):
    t=read(stem+str(part),cols);d=t if d is None else d.merge(t.drop(columns=[c for c in t if c in d and c not in KEY]),on=KEY,validate='one_to_one')
   d=d.merge(dem,on=KEY,how='left',validate='one_to_one')
   for r in d.to_dict('records'):
    try:age=int(r['EDAD']);w=float(r['FAC_PER'])
    except (ValueError,TypeError):continue
    if not 15<=age<=120 or not math.isfinite(w) or w<=0 or not r['EST_DIS'] or not r['UPM_DIS']:continue
    def v(s):
     try:return int(r.get(l+'P'+s,''))
     except (ValueError,TypeError):return None
    for key,name,axis,segment in TARGET:
     if name.startswith('permiso'):
      if l!='C' or r['CVE_ENT']!=segment:continue
      value=v('7_1_'+str(int(name[-2:])));old=value in [1,2,3];new=old and v('4_1') in [1,2]
     else:
      if r['NIV'] not in ['08','09']:continue
      acts=[v(f'2_6_{i}') for i in range(1,10)]
      if 1 not in acts:continue
      visits=[v(f'2_10_{i}_{j}') for i in range(1,10) for j in [1,2]]
      if not any(x in range(1,10) for x in visits):continue
      old=any(v(f'2_12_{i}_{k}') in range(1,9) for i in range(1,10) for k in [1,5])
      new=any(v(f'2_12_{i}_{k}') in range(1,9) for i in range(1,10) for j in [1,2] for k in [2*j-1,2*j] if acts[i-1]==1 and v(f'2_10_{i}_{j}') in range(1,10))
     for n,known in enumerate([old,new]):
      if known:totals[key,n][0]+=1;totals[key,n][1]+=w
 rows=[]
 for key,name,axis,segment in TARGET:
  old=totals[key,0];new=totals[key,1];rows.append({'llave':'RESULT-ENDIREH2011-MOD-TABLA#'+key,'conducta':name,'n_antiguo':old[0],'masa_antigua':old[1],'n_nuevo':new[0],'masa_nueva':new[1],'delta_n':new[0]-old[0],'delta_masa':new[1]-old[1],'punto':'NO-PERSISTIDO','ic':'NO-RECALCULADO','decision':'COMPETE-A-SESION02'})
 with (B/'soporte-sesion02-2011.tsv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
 print('sesion02 soporte',len(rows))
if __name__=='__main__':main()
