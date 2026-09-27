"""Diagnóstico propio auxiliar: solo evidencia agregada y sintéticos; no lee raw."""
import csv, json, hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
SOURCE=REPO/'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
def table(name, rows):
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
def mean(rows):
    selected=[r for r in rows if r['known'] and r['eligible']]
    mass=sum(r['w'] for r in selected)
    return {'n':len(selected),'masa':mass,'p':sum(r['w']*r['y'] for r in selected)/mass if mass else None}
def factorial(rows):
    out=[]
    for a in [0,1]:
        for b in [0,1]:
            chosen=[dict(r, eligible=(r['age']<=97 if a else r['age']<=120), known=(r['complete'] if b else r['partial'])) for r in rows]
            out.append(dict(A=a,B=b,**mean(chosen)))
    p={(r['A'],r['B']):r['p'] for r in out}
    return out, p[1,1]-p[1,0]-p[0,1]+p[0,0]
def execute():
    historical=list(csv.DictReader((SOURCE/'efectos-discrepancias.tsv').open(),delimiter='\t'))
    points=[r for r in historical if r['componente']=='punto']
    assert len(points)==len({r['llave'] for r in points})==685
    coverage=[]
    for r in points:
        coverage.append({k:r[k] for k in ['llave','paquete','conducta','eje','segmento','delta_punto','causa_o_hipotesis']}|{'delta_pp_leido':100*float(r['delta_punto']),'estado_contraste_raw':'EJECUTADO-AUXILIAR; ver cotejo-final2011/2021','atribucion':'HIPOTESIS-HEREDADA; clasificación priorizada no causal'})
    table('cobertura-685.tsv',coverage)
    groups=Counter(r['causa_o_hipotesis'] for r in points)
    table('grupos.tsv',[{'grupo':g,'n':n,'estado':'LEIDO; contribución contrafactual no comprobada'} for g,n in groups.items()])
    pub=list(csv.DictReader((SOURCE/'dictamenes-publicabilidad.tsv').open(),delimiter='\t'))
    assert len(pub)==len({r['llave'] for r in pub})==11
    lookup={r['llave']:r for r in historical}
    table('enlace-sesion02.tsv',[{'llave':r['llave'],'paquete':r['paquete'],'delta_punto_leido':lookup.get(r['llave'],{}).get('delta_punto',''),'cambio_universo':'CP4_1 y permisos' if '2011' in r['llave'] and r['llave'].split('#')[-1]!='606' else 'columnas y elegibilidad denuncia externa' if r['llave'].endswith('#606') else 'sin atribución de punto demostrada; revisar elegibilidad por llave','magnitud_contrafactual':'soporte2011 n/masa en soporte-sesion02-2011.tsv; puntos suprimidos no persistidos' if '2011' in r['llave'] else 'FUERA-DE-ALCANCE-RAW: sesión02 DIS2021','ic':'NO-RECALCULADO','decision_publicabilidad':'COMPETE-A-SESION02'} for r in pub])
    synth=[{'age':65,'w':1,'y':1,'complete':True,'partial':True},{'age':70,'w':2,'y':0,'complete':True,'partial':True},{'age':98,'w':5,'y':0,'complete':False,'partial':True},{'age':80,'w':3,'y':0,'complete':False,'partial':True}]
    cells,interaction=factorial(synth)
    table('sintetico-interacciones.tsv',[{'tipo':'SINTETICO-NO-MEDICION',**r,'diferencia_de_diferencias':interaction} for r in cells])
    assert interaction!=0
    agecases=[]
    for age in [14,15,59,60,97,98,99,120]:
        agecases.append({'EDAD':age,'grupo_productor':'60+' if 60<=age<=120 else 'otro' if 15<=age<60 else '', 'grupo_propuesto':'60+' if 60<=age<=97 else 'otro' if 15<=age<60 else '', 'nacional_observado_o98':15<=age<=98,'nacional_observado':15<=age<=97,'requiere_elegibilidad_externa':age==99,'tipo':'SINTETICO-NO-MEDICION'})
    table('sintetico-edad-nacional2021.tsv',agecases)
    summary={'cobertura_leida':len(points),'grupos':dict(groups),'publicabilidad_enlace':len(pub),'contrastes_raw':'ver c1-puntos-p2-final.json','interaccion_sintetica':interaction,'nacionales2021':'ver contrastes-raw2021-v4.tsv','hashes_fuentes':{n:hashlib.sha256((SOURCE/n).read_bytes()).hexdigest() for n in ['efectos-discrepancias.tsv','dictamenes-publicabilidad.tsv','discrepancias-2011.md','discrepancias-nofisica.md']}}
    (ROOT/'c1-puntos-p2-resumen.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':execute()
