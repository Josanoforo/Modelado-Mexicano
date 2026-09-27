"""Lector propuesto; oro fijo abierto2025T4, no abre olas futuras."""
import argparse, csv, hashlib, io, json, math, zipfile
from collections import defaultdict
CAMPOS = {'ID_PER','CD','SEXO','EDAD','BP1_1','FAC_SEL','EST_DIS','UPM_DIS'}
SHA_ORO = '317ed14f2f2f43c9f8280e491f7592d0cf95a0392aaa641b66822569444b121c'
def medir(rows, campos):
    if not CAMPOS.issubset(campos): raise ValueError('ESQUEMA: faltan campos')
    grupos = {1: [], 2: []}; vistos = set(); excluidos = defaultdict(int); marco = set()
    for r in rows:
        if r['CD'] != '01': continue
        if not r['ID_PER'] or r['ID_PER'] in vistos: raise ValueError('ID duplicado/nulo')
        vistos.add(r['ID_PER'])
        sexo=int(r['SEXO']); edad=int(r['EDAD']); w=float(r['FAC_SEL'])
        if sexo not in grupos or not 18<=edad<=99: raise ValueError('UNIVERSO')
        if not math.isfinite(w) or w<=0: raise ValueError('PESO')
        if not r['EST_DIS'] or not r['UPM_DIS']: raise ValueError('DISENO')
        b=r['BP1_1'].strip()
        if b and b not in {'1','2','9'}: raise ValueError('CODIGO')
        if not b: excluidos[str(sexo)]+=1
        marco.add((r['EST_DIS'],r['UPM_DIS']))
        grupos[sexo].append((r['EST_DIS'],r['UPM_DIS'],w,None if not b else int(b)==2))
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
    with zipfile.ZipFile(io.BytesIO(payload)) as outer:
        inner=outer.read('ensu_bd_diciembre_2025_csv.zip')
    with zipfile.ZipFile(io.BytesIO(inner)) as z:
        reader=csv.DictReader(io.TextIOWrapper(z.open('ENSU_CB_1225.csv'),encoding='utf-8-sig'))
        return {'estado':'DIAGNOSTICO-HISTORICO-ABIERTO','ola':'2025T4','archivo_sha256':SHA_ORO,'grupos':medir(reader,reader.fieldnames)}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--oro',required=True);ap.add_argument('--salida',required=True);a=ap.parse_args()
    result=oro(a.oro)
    with open(a.salida,'w') as f: json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
