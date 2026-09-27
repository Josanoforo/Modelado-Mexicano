"""Verificación de los cuatro puntos con sumas Decimal y lectura independiente."""
import csv, io, json, zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path
R=Path(__file__).resolve().parent
out=list(csv.DictReader((R/'reconstruccion.tsv').open(),delimiter='\t'))
assert len(out)==4 and len({r['llave'] for r in out})==4
D=Decimal
def number(s):
    try: return D(s)
    except InvalidOperation: return D('NaN')
totals={k:[D(0),D(0)] for k in ['A-P-SOL1','B-P-DIG-SD','B-P-PRE-SD','C-P-ADOPTA']}
def add(k,w,d):
    if w.is_finite() and w>0:
        totals[k][0]+=w*d; totals[k][1]+=w
with zipfile.ZipFile('/raw/encig25_base_datos_csv/encig25_base_datos_csv.zip') as z:
    def rows(name):
        with z.open(name) as f:
            yield from csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig'))
    for r in rows('encig2025_01_sec1_A_3_4_5_8_9_10.csv'):
        x=number(r['P8_3_1'])
        if x in (1,2): add('A-P-SOL1',number(r['FAC_P18']),int(x==1))
    valid={r['ID_TRA']:number(r['P8_4']) for r in rows('encig2025_05_sec_8.csv') if number(r['P8_4']) in (0,1)}
    for r in rows('encig2025_04_sec_7.csv'):
        c=number(r['P7_3']); w=number(r['FAC_TRA'])
        if r['ID_TRA'] in valid:
            if c==1: add('B-P-PRE-SD',w,valid[r['ID_TRA']])
            elif c in (3,4,5): add('B-P-DIG-SD',w,valid[r['ID_TRA']])
        if number(r['N_TRA'])==1 and c in (1,2,4,5,6): add('C-P-ADOPTA',w,int(c in (4,5)))
checks={}
for r in out:
    key=r['llave'].removeprefix('RESULT-ENCIG-MOR-')
    n,d=totals[key]; exact=n/d
    err=abs(D(r['p'])-exact)
    assert err<=D('1e-10')
    assert r['estado']=='RECONSTRUIDO'
    assert 0<=float(r['ic95_inf'])<=float(r['ic95_sup'])<=1
    checks[key]={'numerador_decimal':str(n),'denominador_decimal':str(d),'p_decimal':str(exact),'error_absoluto':str(err)}
(R/'verificacion.json').write_text(json.dumps({'puntos_verificados':checks,'resultado':'CORRECTO'},indent=2)+'\n')
print('Cuatro puntos verificados mediante sumas Decimal; IC dentro de [0,1].')
