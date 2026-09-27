"""Auxiliar2011 propio no ciego, factorial edad y reglas sin bootstrap."""
import csv,json,zipfile,hashlib,re
from pathlib import Path
from collections import defaultdict
import pandas as pd
B=Path(__file__).resolve().parent
RAW=Path('/home/pc0/astra6-c1-aislado/tanda2-endireh-pisos-2011-modulos-0001/raw/endireh_2011_bd_endireh_2011_csv.zip')
SHA='8ece557b2ac1d78dc0bfdee1d8f9743b2da1e44184be340d22967d60b10d52e5'
KEY=['CONTROL','VIV_SEL','HOGAR','R_SEL_M']
def binary(v):return 1 if v==1 else 0 if v==2 else None
def union(v):return 1 if 1 in v else 0 if v and all(x==0 for x in v) else None
def freq(v):return union([1 if x in [1,2,3] else 0 if x==4 else None for x in v])
def multi(v,positive,valid):return 1 if any(x in positive for x in v) else 0 if any(x in valid for x in v) else None
def outcomes(r,l,new):
 def v(s):
  try:return int(r.get(l+'P'+s,''))
  except (ValueError,TypeError):return None
 o={};eligible=l!='C' or v('4_1') in [1,2]
 ranges={'alguna':range(1,22),'fisica':range(12,19),'emocional_control':range(1,11),'economica_patrimonial':[11],'sexual':range(19,22)} if l=='C' else {'alguna':range(1,31),'fisica':range(20,28),'emocional_control':range(1,14),'economica_patrimonial':range(14,20),'sexual':range(28,31)}
 for group,nums in ranges.items():
  life=[v('6_1_'+str(i)) for i in nums];yl=freq(life) if eligible else None
  recent=freq([4 if x==4 else v('6_3_'+str(i)) for x,i in zip(life,nums)]) if eligible else None
  o['pareja_'+group+'_vida']=yl;o['pareja_'+group+'_desde_octubre_2010']=recent if new or yl is not None else None
 affected=o['pareja_alguna_vida']==1
 aid=[binary(v(('6_4_' if l=='C' else '6_5_')+str(i))) for i in range(1,7)]
 helping=union(aid) if affected else None;o['pareja_ayuda_institucional']=helping
 for i,y in enumerate(aid,1):o[f'pareja_institucion_{i:02}']=y if (affected if new else helping==1) else None
 partnerresults=[v(f'6_8_{i}_{j}') for i in range(1,7) for j in [1,2] if not new or v(f'6_5_{i}')==1]
 if l!='C':o['pareja_denuncia_ultima_visita']=multi(partnerresults,[1],range(1,11)) if helping==1 else None
 for i in range(1,8):o[f'permiso_{i:02}']=(1 if v('7_1_'+str(i))==1 else 0 if v('7_1_'+str(i)) in [2,3] else None) if l=='C' and (eligible or not new) else None
 o['prueba_embarazo_vida']=binary(v('2_1'));o['perjuicio_embarazo_vida']=binary(v('2_2'))
 discr=[binary(v('2_5_'+str(i))) if v('2_3_1')==1 else None for i in range(1,6)]
 o['discriminacion_laboral_desde_octubre_2010']=union(discr)
 for i,y in enumerate(discr,1):o[f'discriminacion_laboral_item_{i:02}']=y
 o['despojo_bienes_vida']=union([binary(v(('3_1_' if l=='C' else '3_7_')+str(i))) for i in range(1,4)])
 o['decision_gasto']=1 if v('7_1_6') in [1,3] else 0 if v('7_1_6')==2 else None
 o['decision_su_dinero']=1 if v('7_1_3') in [1,3] else 0 if v('7_1_3')==2 else None
 if l!='A':o['decision_gasto']=o['decision_su_dinero']=None
 o['dinero_libre']=binary(v('8_1' if l=='A' else '7_1')) if l in ['A','B'] else None
 domains={'familiar_agresor':('7',range(1,7)),'laboral_agresor':('7',[7,8]),'escolar_agresor':('7',[9,10,11]),'comunitaria_lugar':('8',[1,6,7,8]),'escolar_lugar':('8',[2]),'laboral_lugar':('8',[3,4])}
 for domain,(q,codes) in domains.items():
  life=[];recent=[];valid=range(1,17) if q=='7' else range(1,10)
  for i in range(1,13):
   act=v('2_6_'+str(i));cas=[v(f'2_{q}_{i}_{j}') for j in [1,2]];times=[v(f'2_9_{i}_{j}') for j in [1,2]]
   match=[j for j,x in enumerate(cas) if x in codes];known=any(x in valid for x in cas) and (not new or all(x in valid or x is None for x in cas))
   yl=1 if match else 0 if known else None
   yr=1 if any(times[j]==1 for j in match) else 0 if (all(times[j]==2 for j in match) and (bool(match) or known)) else None
   life.append(0 if act==2 else yl if act==1 else None);recent.append(0 if act==2 else yr if act==1 else None)
  o['externo_'+domain+'_vida']=union(life);o['externo_'+domain+'_desde_octubre_2010']=union(recent)
 acts=[v('2_6_'+str(i)) for i in range(1,10)];aff=union([binary(x) for x in acts])==1
 visits=[v(f'2_10_{i}_{j}') for i in range(1,10) for j in [1,2] if not new or acts[i-1]==1]
 help_=multi(visits,range(1,10),range(1,12)) if aff else None
 o['externo_ayuda_autoridad']=help_;o['externo_informo_familia']=multi(visits,[10],range(1,12)) if aff else None
 results=[v(f'2_12_{i}_{k}') for i in range(1,10) for j in [1,2] for k in ([2*j-1,2*j] if new else ([1,5] if j==1 else [])) if not new or (acts[i-1]==1 and v(f'2_10_{i}_{j}') in range(1,10))]
 o['externo_denuncia_ultima_visita']=multi(results,[1],range(1,9)) if help_==1 else None
 return o

def main():
 h=hashlib.sha256()
 with RAW.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 assert h.hexdigest()==SHA
 identities=[r for r in csv.DictReader((B/'cobertura-685.tsv').open(),delimiter='\t') if '2011' in r['llave']]
 needed=defaultdict(set)
 for r in identities:needed[r['conducta']].add((r['eje'],r['segmento']))
 totals=defaultdict(lambda:[0,0.,0.])
 with zipfile.ZipFile(RAW) as z:
  def read(name,selector):return pd.read_csv(z.open('bd_endireh_2011_csv/'+name+'.csv'),encoding='latin1',dtype=str,keep_default_na=False,usecols=selector).apply(lambda s:s.str.strip())
  dem=read('TSDem',lambda c:c in KEY[:-1]+['N_REN','EDAD','NIV']).rename(columns={'N_REN':'R_SEL_M'})
  for l,stem,parts in [('A','TUnidas',3),('B','TDunida',3),('C','TSolter',2)]:
   d=None
   for part in range(1,parts+1):
    t=read(stem+str(part),lambda c:c in KEY+['FAC_PER','DOMINIO','CVE_ENT'] or bool(re.match(l+r'P(?:2_(?:1$|2$|3_1$|5_|6_|7_|8_|9_|10_|12_)|3_(?:7_|1_)|4_1$|6_(?:1_|3_|4_|5_|8_)|7_1(?:_|$)|8_1$)',c)))
    d=t if d is None else d.merge(t.drop(columns=[c for c in t if c in d and c not in KEY]),on=KEY,validate='one_to_one')
   d=d.merge(dem,on=KEY,how='left',validate='one_to_one')
   for r in d.to_dict('records'):
    try:age=int(r['EDAD']);weight=float(r['FAC_PER'])
    except (ValueError,TypeError):continue
    if not 15<=age<=120 or weight<=0:continue
    variants=[outcomes(r,l,new) for new in [0,1]]
    for name,segments in needed.items():
     for axis,segment in segments:
      fixed=(axis=='nacional' or axis=='pareja' and l==segment or axis=='localidad' and r['DOMINIO']==segment or axis=='entidad' and r['CVE_ENT']==segment or axis=='escolaridad' and r['NIV'] in {'ninguno':['00'],'basica':['01','02','03','05'],'media_superior':['04','06','07'],'superior':['08','09']}.get(segment,[]))
      for agefix in [0,1]:
       included=fixed or axis=='edad' and ({'15-29':15<=age<=29,'30-44':30<=age<=44,'45-59':45<=age<=59,'60+':60<=age<=(97 if agefix else 120)}.get(segment,False))
       if not included:continue
       for new in [0,1]:
        y=variants[new].get(name)
        if y is not None:
         a=totals[name,axis,segment,agefix,new];a[0]+=1;a[1]+=weight;a[2]+=weight*y
 rows=[]
 for r in identities:
  for agefix in [0,1]:
   for new in [0,1]:
    a=totals[r['conducta'],r['eje'],r['segmento'],agefix,new]
    rows.append({'llave':r['llave'],'conducta':r['conducta'],'eje':r['eje'],'segmento':r['segmento'],'edad_corregida':agefix,'regla_corregida':new,'n':a[0],'masa':a[1],'numerador':a[2],'punto':a[2]/a[1] if a[1] else '', 'estado':'DIAGNOSTICO-AUXILIAR-NO-ADOPTADO'})
 with (B/'contrastes-raw2011.tsv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
 (B/'raw2011-ejecucion.json').write_text(json.dumps({'sha256_raw':SHA,'sha256_codigo':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sha256_plan':hashlib.sha256((B/'plan2011.md').read_bytes()).hexdigest(),'identidades':len(identities),'filas_factoriales':len(rows),'ic':'NO-RECALCULADO'},indent=2)+'\n')
 print('raw2011',len(rows))
if __name__=='__main__':main()
