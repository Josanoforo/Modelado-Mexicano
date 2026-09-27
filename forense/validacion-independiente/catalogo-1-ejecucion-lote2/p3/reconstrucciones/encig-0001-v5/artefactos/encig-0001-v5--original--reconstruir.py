#!/usr/bin/env python3
"""Reconstrucción independiente; sólo lee entradas declaradas y archivo ZIP local."""
import csv, hashlib, io, json, math, platform, zipfile
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
ENT = ROOT / 'entrada'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
manifest = json.loads((ENT/'manifiesto.json').read_text())
for name, expected in manifest['archivos'].items():
    assert sha(ENT/name) == expected, name
inventory=[]
for item in json.loads((ENT/'insumos.json').read_text()):
    p=Path('/raw')/item['id']/Path(item['archivo']).name
    actual=sha(p)
    assert actual == item['sha256'], str(p)
    inventory.append(dict(item, ruta_local=str(p), sha256_observado=actual, bytes=p.stat().st_size))
zip_path=Path(inventory[0]['ruta_local'])
cols={
 'A': 'P8_3_1 P8_3_2 P8_3_3 FAC_P18 EST_DIS UPM_DIS'.split(),
 '7': 'CVE_ENT UPM V_SEL R_ELE N_TRA ID_TRA NT_TIPO P7_3 FAC_TRA EST_DIS UPM_DIS'.split(),
 '8': 'ID_TRA P8_4 EST_DIS UPM_DIS'.split()}
names={'A':'encig2025_01_sec1_A_3_4_5_8_9_10.csv','7':'encig2025_04_sec_7.csv','8':'encig2025_05_sec_8.csv'}
tables={}; members=[]; guards={}
with zipfile.ZipFile(zip_path) as z:
    for info in z.infolist():
        h=hashlib.sha256()
        with z.open(info) as f:
            for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
        members.append({'entrada':info.filename,'bytes':info.file_size,'sha256':h.hexdigest()})
    for key,name in names.items():
        with z.open(name) as f:
            reader=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig'))
            missing=set(cols[key])-set(reader.fieldnames)
            guards['G-1-'+key]='PRESENTES' if not missing else 'NO-ESTIMABLE-COLUMNA-AUSENTE:'+','.join(sorted(missing))
            assert not missing, guards['G-1-'+key]
            tables[key]=[{c:r[c] for c in cols[key]} for r in reader]
def unique(rows, keys):
    c=Counter(tuple(r[k] for k in keys) for r in rows)
    duplicates=[v for v in c.values() if v>1]
    return 'UNICA' if not duplicates else f'NO-UNICA:{len(duplicates)}/{sum(duplicates)}'
a,s7,s8=(tables[k] for k in ['A','7','8'])
guards['G-LLAVE-SEC7-DECLARADA-UNICA']=unique(s7,['CVE_ENT','UPM','V_SEL','R_ELE','N_TRA'])
guards['G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA']=unique(s7,['ID_TRA','NT_TIPO'])
guards['G-LLAVE-SEC8-IDTRA-UNICA']=unique(s8,['ID_TRA'])
def num(x):
    try: return float(x)
    except (ValueError,TypeError): return float('nan')
def weight(r,c):
    w=num(r[c]); return w if math.isfinite(w) and w>0 else None

diag={}; estimates={}
for table, wc in [('A','FAC_P18'),('7','FAC_TRA')]:
    diag[table+'-N-PESO-INVALIDO']=sum(weight(r,wc) is None for r in tables[table])
for table, columns in [('A',['P8_3_1','P8_3_2','P8_3_3']),('7',['P7_3']),('8',['P8_4'])]:
    for col in columns:
        diag[table+'-FRECUENCIAS-'+col]=dict(sorted(Counter(r[col] for r in tables[table]).items()))
def estimate(label, rows):
    # rows: (fila, peso, indicador), en orden de archivo.
    den=0.; numerator=0.; clusters={}; missing=0
    for r,w,d in rows:
        den+=w; numerator+=w*d
        st,psu=r['EST_DIS'],r['UPM_DIS']
        if not st.strip() or not psu.strip(): missing+=1; continue
        pair=clusters.setdefault(st,{}).setdefault(psu,[0.,0.])
        pair[0]+=w*d; pair[1]+=w
    diag[label+'-N']=len(rows); diag[label+'-N-SIN-DISENO']=missing
    if not den:
        estimates[label]={'motivo':'NO-ESTIMABLE-UNIVERSO-VACIO'}; return
    result={'p':numerator/den,'numerador':numerator,'denominador':den}
    # Convenciones explícitas: dominios elegibles, orden de primera aparición,
    # RNG reiniciado por estimando, estrato exterior y matriz (2000,n_UPM).
    rng=np.random.Generator(np.random.PCG64(20260909))
    totals=np.zeros((2000,2)); single=0
    for psus in clusters.values():
        values=np.array(list(psus.values()),dtype=float); n=len(values)
        single+=n==1
        idx=rng.integers(0,n,size=(2000,n))
        totals+=values[idx].sum(axis=1)
    diag[label+'-N-ESTRATOS-UPM-UNICA']=single
    diag[label+'-N-ESTRATOS']=len(clusters)
    diag[label+'-N-UPM']=sum(map(len,clusters.values()))
    if clusters and np.all(totals[:,1]>0):
        lo,hi=np.percentile(totals[:,0]/totals[:,1],[2.5,97.5],method='linear')
        result.update(ic95_inf=float(lo),ic95_sup=float(hi),metodo_ic='IC-CON-ESTRATOS-DE-UPM-UNICA' if single else 'BOOTSTRAP-UPM-ESTRATIFICADO')
    else: result['motivo_ic']='NO-ESTIMABLE-UNIVERSO-DISENO-VACIO'
    estimates[label]=result

diag['A-N-P831-NSNR']=sum(num(r['P8_3_1'])==9 for r in a)
diag['A-N-P831-BLANCO']=sum(not math.isfinite(num(r['P8_3_1'])) for r in a)
diag['A-N-P831-OTRO']=sum(math.isfinite(num(r['P8_3_1'])) and num(r['P8_3_1']) not in (1,2,9) for r in a)
ua=[(r,weight(r,'FAC_P18')) for r in a if num(r['P8_3_1']) in (1,2) and weight(r,'FAC_P18') is not None]
estimate('A-P-SOL1',[(r,w,int(num(r['P8_3_1'])==1)) for r,w in ua])
solany=[]; partial=0; excluded=0
for r,w in ua:
    v=[num(r[c]) for c in ('P8_3_1','P8_3_2','P8_3_3')]
    partial+=any(x not in (1,2) for x in v[1:])
    if 1 in v: solany.append((r,w,1))
    elif all(x==2 for x in v): solany.append((r,w,0))
    else: excluded+=1
diag['A-N-SOLANY-PARCIAL']=partial; diag['A-N-SOLANY-EXCLUIDAS']=excluded
estimate('A-P-SOLANY',solany)
seen=set(); cd=[]
for r in s7:
    if r['ID_TRA'] not in seen: cd.append(r); seen.add(r['ID_TRA'])
diag['B-N-EVENTOS-DESCARTADOS-POR-DEDUP']=len(s7)-len(cd)
diag['B-N-SEC7-FILAS']=len(s7); diag['B-N-SEC8-FILAS']=len(s8)
exact=all(guards[k]=='UNICA' for k in ('G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA','G-LLAVE-SEC8-IDTRA-UNICA'))
guards['JOIN']='EXACTO' if exact else 'JOIN-NO-EXACTO'
if exact:
    lookup={r['ID_TRA']:r for r in s8}
    for branch,rows in [('SD',s7),('CD',cd)]:
        pairs=[(r,lookup[r['ID_TRA']]) for r in rows if r['ID_TRA'] in lookup]
        prefix='B-'+branch
        diag[prefix+'-N-EMPAREJADAS']=len(pairs)
        diag[prefix+'-N-SEC7-SIN-PAREJA']=len(rows)-len(pairs)
        diag[prefix+'-COBERTURA']=len(pairs)/len(rows) if rows else None
        diag[prefix+'-N-P84-BLANCO']=sum(not t['P8_4'].strip() for r,t in pairs)
        diag[prefix+'-N-P84-FUERA']=sum(num(t['P8_4']) not in (0,1) for r,t in pairs)
        ub=[(r,weight(r,'FAC_TRA'),int(num(t['P8_4']))) for r,t in pairs if num(t['P8_4']) in (0,1) and weight(r,'FAC_TRA') is not None]
        residue=[(r,w,d) for r,w,d in ub if num(r['P7_3']) not in (1,3,4,5)]
        diag[prefix+'-N-RESIDUO-CANAL']=len(residue)
        diag[prefix+'-P-RESIDUO-CANAL']=sum(w for r,w,d in residue)/sum(w for r,w,d in ub) if ub else None
        for channel,codes in [('DIG',(3,4,5)),('PRE',(1,))]:
            estimate('B-P-'+channel+'-'+branch,[(r,w,d) for r,w,d in ub if num(r['P7_3']) in codes])
    for metric in ('N-EMPAREJADAS','N-SEC7-SIN-PAREJA','COBERTURA','N-RESIDUO-CANAL','P-RESIDUO-CANAL'):
        diag['B-'+metric]=diag['B-SD-'+metric]
else:
    for branch in ('SD','CD'):
        for channel in ('DIG','PRE'): estimates['B-P-'+channel+'-'+branch]={'motivo':'NO-ESTIMABLE-LLAVE-NO-UNICA'}
uc0=[(r,weight(r,'FAC_TRA')) for r in s7 if num(r['N_TRA'])==1 and weight(r,'FAC_TRA') is not None]
uc=[(r,w,int(num(r['P7_3']) in (4,5))) for r,w in uc0 if num(r['P7_3']) in (1,2,4,5,6)]
residue=[(r,w) for r,w in uc0 if num(r['P7_3']) not in (1,2,4,5,6)]
diag['C-N-RESIDUO']=len(residue)
diag['C-P-RESIDUO']=sum(w for r,w in residue)/sum(w for r,w in uc0) if uc0 else None
estimate('C-P-ADOPTA',uc)
requests=list(csv.DictReader((ENT/'estimandos.tsv').open(),delimiter='\t'))
fields=list(requests[0])+['estado','p','ic95_inf','ic95_sup','metodo_ic','motivo']
with (ROOT/'reconstruccion.tsv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); writer.writeheader()
    for row in requests:
        key=row['llave'].removeprefix('RESULT-ENCIG-MOR-')
        result=estimates.get(key,{'motivo':'Identidad sin correspondencia explícita en el método'})
        row.update({k:result[k] for k in ('p','ic95_inf','ic95_sup','metodo_ic','motivo') if k in result})
        row['estado']='RECONSTRUIDO' if 'p' in result else 'NO-RECALCULABLE-DESDE-SPEC'
        writer.writerow(row)
dump('diagnosticos.json',{'guardias':guards,'conteos':diag,'estimaciones':estimates})
dump('recibo.json',{'paquete':manifest['paquete'],'manifiesto_sha256':sha(ENT/'manifiesto.json'),'entradas':{p.name:sha(p) for p in sorted(ENT.iterdir())},'insumos':inventory,'miembros_zip':members,'entorno':{'python':platform.python_version(),'numpy':np.__version__},'resultados_esperados_consultados':False,'revelacion_solicitada':False})
print(json.dumps({'guardias':guards,'estimaciones_solicitadas':{r['llave']:estimates.get(r['llave'].removeprefix('RESULT-ENCIG-MOR-')) for r in requests}},indent=2))
