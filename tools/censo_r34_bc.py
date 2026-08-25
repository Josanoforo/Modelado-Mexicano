#!/usr/bin/env python3
"""tools/censo_r34_bc.py -- barrido de instrumentos del corpus para el censo de las
condiciones B (prueba de mecanismo) y C (anti-confusion) del gate de R3.4 (ADR-37).

ACTO R34-BC-MECANISMO, 25/ago/2026. Entorno UBUNTU (exige data/raw montado).

Que hace: recorre data/raw/ completo y, por cada archivo que pueda contener el TEXTO de
un reactivo -- PDF, XLSX, cabecera de CSV, HTML/XML/JSON -- registra si aparece
  DIGITAL  : CoDi / SPEI / DiMo / pago digital-movil-por internet / banca en linea / tramite en linea
  FISCAL   : SAT / impuesto / fiscalizacion / hacienda / fisco / vigilancia / rastreo
  FRICCION : no sabe como / no sabe usar / complicado / requisitos que no tiene / no cuenta con...
  PERSONAL : amistades / personas conocidas / familiares o amigos / parientes como / vecinos

Salida: JSONL incremental, una linea por archivo examinado (reanudable: re-ejecutar
sobre el mismo JSONL salta lo ya registrado). El conteo de lineas ES el numero de
archivos examinados que A.13 exige declarar junto a cualquier veredicto negativo.

LIMITE DECLARADO: un .csv solo aporta NOMBRES DE VARIABLE, no el texto del reactivo.
Este barrido no puede encontrar un item cuya redaccion viva unicamente en un descriptor
ausente del corpus. Por eso el censo NO se cierra con el: cada candidata con senal se
abre y se lee a nivel de reactivo, y es esa lectura la que emite el veredicto A.4.

Uso: python3 tools/censo_r34_bc.py <salida.jsonl>
"""

import os, re, sys, zipfile, io, subprocess, json, tempfile

RAIZ='data/raw'
TMP=os.environ.get('CENSO_TMP','/tmp/claude-1000/-home-pc0/ae17f2ac-d849-48c1-8bb0-1b8303e2d69e/scratchpad/censo/tmp')
os.makedirs(TMP, exist_ok=True)
import json as _j
YA=set()
try:
    for _l in open(sys.argv[1],encoding='utf-8'):
        try: YA.add(_j.loads(_l)['a'])
        except Exception: pass
except FileNotFoundError: pass
SAL=open(sys.argv[1],'a',encoding='utf-8')
print('reanuda: ya registrados',len(YA),flush=True)

FISCAL   = re.compile(r'\bSAT\b|impuest|fiscaliz|hacienda|fisco|vigilanc|rastre[oa]', re.I)
DIGITAL  = re.compile(r'\bCoDi\b|cobro digital|pago(s)? (digital|m[oó]vil|por internet|electr)|transferencia electr|banca (en l[ií]nea|electr|m[oó]vil)|aplicaci[oó]n de celular|\bSPEI\b|\bDiMo\b|tr[aá]mite.{0,20}en l[ií]nea', re.I)
FRICCION = re.compile(r'no sab(e|r[ií]a) c[oó]mo|no sabe usar|no sabe hacerlo|complicad|dif[ií]cil de usar|requisitos que no tiene|no cuenta con (tarjeta|servicios)', re.I)
PERSONAL = re.compile(r'amistades|personas conocidas|familiares o amig|amigos o familiar|parientes como|vecinos\?|recomendaci[oó]n de (amist|conocid|familiar)', re.I)

def t_pdf(p):
    o=[]
    try:
        from pypdf import PdfReader
        o.append("\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages))
    except Exception: pass
    try:
        o.append(subprocess.run(["pdftotext","-layout",p,"-"],capture_output=True,text=True,timeout=180).stdout)
    except Exception: pass
    return "\n".join(o)

def t_xlsx(b):
    try:
        import openpyxl, warnings
        warnings.filterwarnings('ignore')
        wb=openpyxl.load_workbook(io.BytesIO(b) if isinstance(b,(bytes,bytearray)) else b, read_only=True, data_only=True)
    except Exception: return ""
    ps=[]
    for ws in wb.worksheets:
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i>4000: break
            ps.append(' | '.join(str(c) for c in row if c is not None))
    return "\n".join(ps)

def t_csvhdr(b):
    try: return b.decode('latin-1','replace').split('\n')[0]
    except Exception: return ""

def registra(nombre, texto, clase):
    if nombre in YA: return
    d,f,fr,pe = DIGITAL.search(texto or ''), FISCAL.search(texto or ''), FRICCION.search(texto or ''), PERSONAL.search(texto or '')
    SAL.write(json.dumps(dict(a=nombre, clase=clase, chars=len(texto or ''),
        dig=bool(d), fis=bool(f), fri=bool(fr), per=bool(pe),
        fis_ej=(f.group(0) if f else None), dig_ej=(d.group(0) if d else None),
        per_ej=(pe.group(0) if pe else None)), ensure_ascii=False)+"\n")
    SAL.flush()

for dp,_,fs in os.walk(RAIZ):
    for fn in sorted(fs):
        p=os.path.join(dp,fn); low=fn.lower()
        try:
            if p in YA and not low.endswith('.zip'): continue
            if low.endswith('.pdf'): registra(p, t_pdf(p), 'pdf')
            elif low.endswith(('.xlsx','.xls')): registra(p, t_xlsx(p), 'xlsx')
            elif low.endswith('.csv'):
                with open(p,'rb') as fh: registra(p, t_csvhdr(fh.read(400000)), 'csv_hdr')
            elif low.endswith(('.html','.htm','.txt','.xml','.json')):
                with open(p,'rb') as fh: registra(p, fh.read(3000000).decode('utf-8','replace'), 'texto')
            elif low.endswith('.zip'):
                try: z=zipfile.ZipFile(p)
                except Exception: 
                    registra(p,'','zip_ilegible'); continue
                for n in z.namelist():
                    nl=n.lower()
                    try:
                        if nl.endswith(('.xlsx','.xls')): registra(f'{p}::{n}', t_xlsx(z.read(n)), 'zip_xlsx')
                        elif nl.endswith('.pdf'):
                            with tempfile.NamedTemporaryFile(suffix='.pdf',delete=False,dir=TMP) as t:
                                t.write(z.read(n)); tp=t.name
                            registra(f'{p}::{n}', t_pdf(tp), 'zip_pdf'); os.unlink(tp)
                        elif nl.endswith('.csv'):
                            with z.open(n) as fh: registra(f'{p}::{n}', t_csvhdr(fh.read(400000)), 'zip_csv_hdr')
                    except Exception as e:
                        print('ERRZ',p,n,type(e).__name__,e,file=sys.stderr)
        except Exception as e:
            print('ERR',p,type(e).__name__,e,file=sys.stderr)
SAL.close()
print('FIN')
