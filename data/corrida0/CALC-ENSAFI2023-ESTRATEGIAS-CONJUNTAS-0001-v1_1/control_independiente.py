"""Control separado: recomputa un punto y su varianza sin importar medidor."""
import csv, hashlib, io, json, math, zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def c(x): return '' if x is None else str(x).strip()
def w(x):
    try: return float(c(x))
    except ValueError: return None
def main():
    raw=ROOT/'data/raw/ensafi2023/ensafi_2023_bd_csv.zip'
    with zipfile.ZipFile(raw) as z:
        n=next(x for x in z.namelist() if x.endswith('TMODULO.csv'))
        rows=list(csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig'))))
    its=[f'P6_10_{i}' for i in range(1,9)]
    ok=lambda r:c(r['P6_9'])=='2' and all(c(r[x]) in {'1','2'} for x in its)
    den=sum(w(r['FAC_ELE']) for r in rows if ok(r)); num=sum(w(r['FAC_ELE']) for r in rows if ok(r) and sum(c(r[x])=='1' for x in its)>=2); p=num/den
    psus=defaultdict(set); z=defaultdict(float)
    for r in rows:
        h,u=c(r['EST_DIS']),c(r['UPM_DIS']); ww=w(r['FAC_ELE'])
        if ww and h and u:
            psus[h].add(u)
            if ok(r): z[h,u]+=ww*(float(sum(c(r[x])=='1' for x in its)>=2)-p)/den
    v=0
    for h,us in psus.items():
        a=[z[h,u] for u in us]
        if len(a)>1:
            m=sum(a)/len(a);v+=len(a)/(len(a)-1)*sum((x-m)**2 for x in a)
    sealed=json.loads((ROOT/'data/corrida0/CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1/resultados.json').read_text())['resultados']
    outdir=ROOT/'forense/analisis/ensafi2023-estrategias-conjuntas-cli-1-v1_1'
    tab=list(csv.DictReader((outdir/'conteos.csv').open()))
    hit=next(x for x in tab if x['conteo']=='>=2')
    hashes={n:hashlib.sha256((outdir/n).read_bytes()).hexdigest() for n in ('cobertura.csv','conteos.csv','parejas.csv','sensibilidad_parejas.csv','limites_faltantes.csv')}
    seal_hashes={'cobertura.csv':sealed['RESULT-ENSAFI-EC2-G-SHA256-COBERTURA'],'conteos.csv':sealed['RESULT-ENSAFI-EC2-G-SHA256-CONTEOS'],'parejas.csv':sealed['RESULT-ENSAFI-EC2-G-SHA256-PAREJAS'],'sensibilidad_parejas.csv':sealed['RESULT-ENSAFI-EC2-G-SHA256-SENSIBILIDAD-PAREJAS'],'limites_faltantes.csv':sealed['RESULT-ENSAFI-EC2-G-SHA256-LIMITES-FALTANTES']}
    out={'control':'COINCIDE' if abs(p-float(hit['p']))<1e-10 and abs(math.sqrt(v)-float(hit['ee']))<1e-10 and hashes==seal_hashes else 'DISCREPA','p_ge2':p,'ee_ge2':math.sqrt(v),'delta_p':abs(p-float(hit['p'])),'delta_ee':abs(math.sqrt(v)-float(hit['ee'])),'hashes_regenerados':hashes,'hashes_sellados':seal_hashes,'replay_tablas':'IDENTICO' if hashes==seal_hashes else 'DISCREPA','implementacion':'separada; no importa medidor.py'}
    print(json.dumps(out,indent=2)); return out
if __name__=='__main__': main()
