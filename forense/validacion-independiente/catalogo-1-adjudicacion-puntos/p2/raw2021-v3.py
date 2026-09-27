"""Auxiliar2021 no ciego: solo campos listados en plan, sin réplicas."""
import csv,io,zipfile,hashlib,json
from pathlib import Path
from collections import defaultdict
BASE=Path(__file__).resolve().parent
RAW=Path('/home/pc0/astra6-c1-aislado/tanda2-endireh-pisos-2021-nofisica-bc-0001/raw/endireh2021_bd_csv_zip.zip')
HASH='e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e'
AB={23,24,35,36,37,38}
def rows(z,name):
    members=[n for n in z.namelist() if n.split('/')[-1]==name]
    assert len(members)==1
    with z.open(members[0]) as f:yield from csv.DictReader(io.TextIOWrapper(f,encoding='latin1'))
def union(r,acts,window):
    values=[]
    for i in acts:
        if r['T_INSTRUM'].startswith('C') and i in AB:continue
        suffix=str(i)+('AB' if i in AB else '')
        life=r.get('P14_1_'+suffix,'')
        value=life if window=='vida' else '4' if life=='4' else r.get('P14_3_'+suffix,'')
        values.append(value)
    return 1 if any(v in {'1','2','3'} for v in values) else 0 if values and all(v=='4' for v in values) else None
def main():
    h=hashlib.sha256()
    with RAW.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    assert h.hexdigest()==HASH
    totals=defaultdict(lambda:[0,0.,0.]); ages=defaultdict(lambda:[0,0.])
    with zipfile.ZipFile(RAW) as z:
        dem={r['ID_PER']:r['EDAD'] for r in rows(z,'TSDem.csv')}
        reasons={r['ID_PER']:{f'P14_22_{i}':r.get(f'P14_22_{i}','') for i in range(1,16)} for r in rows(z,'TB_SEC_XIV_2.csv')}
        for r in rows(z,'TB_SEC_XIV.csv'):
            if r['T_INSTRUM'] not in {'A1','A2','B1','B2','C1'}:continue
            try:a=int(dem.get(r['ID_PER'],''));w=float(r['FAC_MUJ'])
            except ValueError:continue
            if w<=0 or not r.get('EST_DIS') or not r.get('UPM_DIS'):continue
            if not 15<=a<=120:continue
            outcomes={}
            for name,acts in {'emocional_control':range(10,25),'sexual':range(25,30),'digital':range(30,32),'economica_patrimonial':range(32,39),'no_fisica_alguna':range(10,39)}.items():
                for window in ['vida','reciente']:outcomes[name+'_'+window]=union(r,acts,window)
            if r['T_INSTRUM'] in {'B1','B2','C1'} and union(r,range(1,39),'vida')==1:
                for name,col in [('ayuda_bc','P14_7_1'),('denuncia_bc','P14_7_2')]:
                    outcomes[name]=1 if r.get(col)=='1' else 0 if r.get(col)=='2' else None
            if r['T_INSTRUM'] in {'B1','B2','C1'} and union(r,range(1,39),'vida')==1:
                if r.get('P14_7_1')=='1':
                    for i in range(1,11):
                        value=r.get(f'P14_8_{i}','');outcomes[f'institucion_bc_{i:02}']=1 if value=='1' else 0 if value in {'0','2'} else None
                if r.get('P14_7_1')=='2' and r.get('P14_7_2')=='2':
                    for i in range(1,16):
                        value=reasons.get(r['ID_PER'],{}).get(f'P14_22_{i}','');outcomes[f'razon_bc_{i:02}']=1 if value=='1' else 0 if value=='0' else None
            agecat=str(a) if a>=98 else 'observada'
            ages[agecat][0]+=1;ages[agecat][1]+=w
            for name,y in outcomes.items():
                if y is None:continue
                for universe,include in {'nacional_productor':True,'nacional_hasta98':a<=98,'nacional_observada':a<=97,'60+_productor':a>=60,'60+_observada':60<=a<=97,'edad98':a==98,'edad99':a==99}.items():
                    if include:
                        t=totals[name,universe];t[0]+=1;t[1]+=w;t[2]+=w*y
    for name in list({k[0] for k in totals}):
        for u in ['edad98','edad99','nacional_productor','nacional_hasta98','nacional_observada','60+_productor','60+_observada']:totals[name,u]
    for a in ['98','99']:ages[a]
    data=[{'conducta':name,'universo':u,'n':v[0],'masa':v[1],'numerador':v[2],'punto':v[2]/v[1] if v[1] else '', 'estado':'DIAGNOSTICO-AUXILIAR-NO-ADOPTADO'} for (name,u),v in sorted(totals.items())]
    with (BASE/'contrastes-raw2021-v3.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t');w.writeheader();w.writerows(data)
    (BASE/'raw2021-v3-ejecucion.json').write_text(json.dumps({'raw_sha256':HASH,'codigo_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'plan_sha256':hashlib.sha256((BASE/'plan-contrastes.md').read_bytes()).hexdigest(),'miembros':['TSDem.csv','TB_SEC_XIV.csv','TB_SEC_XIV_2.csv'],'casos_por_edad':dict(ages),'filas_agregadas':len(data),'ic':'NO-RECALCULADO'},indent=2)+'\n')
    print('raw2021 filas agregadas',len(data))
if __name__=='__main__':main()
