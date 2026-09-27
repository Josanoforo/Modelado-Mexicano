"""Lector propuesto; oro fijo abierto2024T4, no abre olas futuras."""
import argparse, csv, hashlib, io, json, math, zipfile
from collections import defaultdict
CAMPOS = {'R_DEF','C_RES','EDA','SEX','EMP_PPAL','CLASE2','FAC_TRI','EST_D_TRI','UPM','ENT','CON','V_SEL','N_HOG','H_MUD','N_REN','N_PRO_VIV'}
SHA_ORO = '817f28d20a43fa4fed08195e62df58bf320b31c323a3049fe09b5194a1677305'
def medir(rows, campos):
    if not CAMPOS.issubset(campos): raise ValueError('ESQUEMA: faltan campos')
    grupos = {1: [], 2: []}; vistos=set(); excluidos=defaultdict(int);marco=set()
    for r in rows:
        if r['R_DEF'].strip() not in {'0','00'} or r['C_RES'] not in {'1','3'}: continue
        if not r['EST_D_TRI'].strip() or not r['UPM'].strip(): raise ValueError('DISENO')
        marco.add((r['EST_D_TRI'],r['UPM']))
        edad=int(r['EDA'])
        if not 15<=edad<=98: continue
        llave=tuple(r[k] for k in ['ENT','UPM','CON','N_PRO_VIV','V_SEL','N_HOG','H_MUD','N_REN'])
        if any(not v for v in llave) or llave in vistos: raise ValueError('ID duplicado/nulo')
        vistos.add(llave)
        sexo=int(r['SEX']);w=float(r['FAC_TRI'])
        if sexo not in grupos: raise ValueError('SEXO')
        if not math.isfinite(w) or w<=0: raise ValueError('PESO')
        if not r['EST_D_TRI'] or not r['UPM']: raise ValueError('DISENO')
        marco.add((r['EST_D_TRI'],r['UPM']))
        if r['CLASE2'] not in {'1','2','3','4'}: raise ValueError('CLASE2')
        if r['CLASE2']!='1': continue
        b=r['EMP_PPAL'].strip()
        if b and b not in {'1','2'}: raise ValueError('CODIGO')
        if not b: excluidos[str(sexo)]+=1
        grupos[sexo].append((r['EST_D_TRI'],r['UPM'],w,None if not b else int(b)==1))
    salida={}
    for sexo, rr in grupos.items():
        validos=[r for r in rr if r[3] is not None]
        sw=sum(r[2] for r in validos)
        if not sw: raise ValueError('DENOMINADOR VACIO')
        num=sum(r[2]*r[3] for r in validos); phat=num/sw
        estratos=defaultdict(lambda:defaultdict(float))
        for est,upm in sorted(marco): estratos[est][upm]+=0
        for est,upm,w,y in rr: estratos[est][upm]+=0 if y is None else w*(y-phat)/sw
        singleton=[]; var=0
        for est,pp in estratos.items():
            m=len(pp)
            if m<2: singleton.append(est); continue
            media=sum(pp.values())/m
            var+=m/(m-1)*sum((v-media)**2 for v in pp.values())
        salida[str(sexo)]={'p0':phat,'numerador_ponderado':num,'denominador_ponderado':sw,'n':len(validos),'n_eff_kish':sw**2/sum(r[2]**2 for r in validos),'se_taylor':None if singleton else math.sqrt(var),'estratos':len(estratos),'upm':sum(len(v) for v in estratos.values()),'singleton':singleton,'excluidos_blanco':excluidos[str(sexo)],'banda':[max(0,phat-.05),min(1,phat+.05)]}
    return salida

def oro(path):
    payload=open(path,'rb').read()
    if hashlib.sha256(payload).hexdigest()!=SHA_ORO: raise ValueError('IDENTIDAD ORO')
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        reader=csv.DictReader(io.TextIOWrapper(z.open('ENOE_SDEMT424.csv'),encoding='latin1'))
        campos=[k.upper() for k in reader.fieldnames]
        rows=({k.upper():v for k,v in r.items()} for r in reader)
        return {'estado':'DIAGNOSTICO-HISTORICO-ABIERTO','ola':'2024T4','archivo_sha256':SHA_ORO,'grupos':medir(rows,campos)}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--oro',required=True);ap.add_argument('--salida',required=True);a=ap.parse_args()
    result=oro(a.oro)
    with open(a.salida,'w') as f: json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
