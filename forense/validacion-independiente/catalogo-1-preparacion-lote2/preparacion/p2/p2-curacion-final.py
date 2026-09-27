#!/usr/bin/env python3
"""Extracción fiel final humana: no abre raw, no ejecuta productores."""
import gzip,hashlib,io,json,tarfile,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'forense/validacion-independiente/catalogo-1-preparacion-lote2';PREP=BASE/'preparacion/p2'
def sha(b):return hashlib.sha256(b).hexdigest()
def js(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def pack(path,files):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as f,gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:
  with tarfile.open(fileobj=z,mode='w') as t:
   for n,b in sorted(files.items()):
    m=tarfile.TarInfo(n);m.size=len(b);m.mode=0o644;t.addfile(m,io.BytesIO(b))
def lines(rel,a,b):return ''.join((ROOT/rel).read_text().splitlines(keepends=True)[a-1:b])
def run():
 records=json.loads((PREP/'p2-sucesores.json').read_text());changes=[]
 fixed={'endireh-pisos-2016-discriminacion-0001','endireh-pisos-2016-pareja-fisica-0002','endireh-pisos-2016-restantes-0001'}
 for rec in records:
  pid=rec['paquete'];path=BASE/rec['archivo']
  if pid in fixed:continue
  with tarfile.open(path) as t:files={m.name:t.extractfile(m).read() for m in t.getmembers()}
  before={k:sha(v) for k,v in files.items()};sources=[]
  ins=json.loads(files['insumos.json'])
  ins=[i for i in ins if not any(k in i['id'] for k in ['dutih_2022','nota_tecnica','descripcion_calculo_r','diseno_muestral'])]
  files['insumos.json']=js(ins)
  if pid.startswith('enigh'):
   for n in list(files):
    if 'cuestionario-encuci' in n:del files[n]
   rec['revision_semantica']['documentos']=[x for x in rec['revision_semantica'].get('documentos',[]) if x['archivo'] in files]
  if pid=='eder-0003':
   rel='forense/prereg-caja/EDER-UNION-LIBRE-spec-v1_0.md';text=(ROOT/rel).read_text()
   a=lines('data/corrida0/CALC-EDER-0003/spec.md',30,39)
   codes=text[text.index('| rama | códigos |'):text.index('**Lo que no se fuerza:**')]
   codes+=text[text.index('Los códigos se leen **como cadena cruda**'):text.index('## 2 · Qué mide, exactamente')]
   universe=text[text.index('Personas de EDER 2017 (unidad:'):text.index('Referencia del censo de L7')]
   estimator=text[text.index('`A-P-LIBRE` ='):text.index('### 2.3 · Diseño')]
   start=text.index('Bootstrap de `upm`',text.index('### 2.3 · Diseño'))
   design=text[start:text.index('Precedente directo:',start)]
   cohort=text[text.index('`B-*`: cohorte de nacimiento'):text.index('No entra a ningún consumidor:')]
   files['metodo.md']=('# Método humano\n\n'+a+'\n'+codes+'\n'+universe+'\n'+estimator+'\n'+design+'\n'+cohort).encode()
   sources=[{'ruta':rel,'secciones':['catálogo tablas LIBRE/DIRECTO y tipado','2.1 universo sin referencia censo','2.2 estimando','2.3 desde Bootstrap hasta precedente','2.4 sólo definición cohortes'],'supresiones':'censos de L7, historia, controles y precedente singleton'}]
  if pid=='enfih-0001':
   rel='forense/prereg-caja/ENFIH-AFORE-spec-v1_0.md';text=(ROOT/rel).read_text()
   code=lines(rel,111,111).split('**No se adivina**')[0]+text[text.index('`C_AFORE` ya es dicotómica'):text.index('## 2 · Qué mide, exactamente')]
   universe=text[text.index('Hogares: **todas**'):text.index('### 2.3 · Lo que esta spec')]
   method=text[text.index('`EDIS` y `UPM_DIS` **están',text.index('### 2.3 · Lo que esta spec')):text.index('### 2.4 · Lo que NO es construible')]
   method=re.sub(r'   `A-DELTA-IC-VS-GEN1`.*?\n','',method)
   files['metodo.md']=(code+'\n'+universe+'\n'+method).encode()
   sources=[{'ruta':rel,'secciones':['1.4 primera cláusula0/1 y guarda soporte','2.1 universo','2.2 estimando','2.3 desde EDIS/UPM hasta2.4'],'supresiones':'V_AFORE monto observado, controles GEN1 y historia de intervalo previo'}]
  if pid=='envipe-0001':
   rel='data/corrida0/CALC-ENVIPE-0001/spec.md';text=(ROOT/rel).read_text()
   safe=text[text.index('## Qué mide'):text.index('## Control positivo externo')]
   safe=safe.replace('; colapso GEN1 (`máx`)','; colapso (`máx`)').replace('— partición GEN1, añade','— añade')
   safe=safe.replace('## Codificación — dos, la primaria NO es la de GEN1','## Codificación')
   safe=re.sub(r' \(a diferencia de lo\nque `FP-201` declaró para la corrida GEN1\)','',safe)
   files['metodo.md']=safe.encode()
   sources=[{'ruta':rel,'secciones':['Qué mide hasta Control positivo externo excluido'],'supresiones':'identificador GEN1 y cláusula históricaFP201; todas las normas U1/U3/U4/C1/C2 preservadas'}]
  if pid=='encig-0001':
   rel='forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md';text=(ROOT/rel).read_text()
   safe=text[text.index('### 3.1 · Regla general'):text.index('## 4 · Familia X')]
   safe=safe.replace(' **(codificación GEN1)**','').replace('por el codebook, no por GEN1','por el codebook').replace('universo GEN1','universo')
   safe=re.sub(r'\*\*Esto, y no.*?### 3.5', '### 3.5',safe,flags=re.S)
   safe=re.sub(r'— la que\n  \*\*verificó `MAESTRA35-L1`\*\*','',safe)
   safe=safe.replace('la llave de `MAESTRA35-L1`','la llave `(ID_TRA,NT_TIPO)`')
   safe=safe.replace('### 3.7 · Diseño: ponderador, estrato y UPM — **la lección de FP-201**','### 3.7 · Diseño: ponderador, estrato y UPM')
   safe=re.sub(r'  \(lección de `ACTO GEN2-LOTE-ENVIPE-1`.*?normalizarlas habría partido estratos en silencio\)\.', '',safe,flags=re.S)
   safe=re.sub(r'- \*\*Ranura no pre-registrada:.*?\n---', '\n---',safe,flags=re.S)
   rows=[]
   for line in safe.splitlines():
    if line.startswith('|') and ('consumidor' in line or 'RES-00' in line or line.startswith('|---')):line='|'.join(line.split('|')[:3])+'|'
    rows.append(line)
   files['metodo.md']=('\n'.join(rows)+'\n').encode()
   sources=[{'ruta':rel,'secciones':['3.1–3.7'],'supresiones':'columnas consumidores, contexto base/_r2, lecciónFP201 y ranura histórica; normas completas conservadas'}]
  if pid=='encuci-0001':
   rel='data/corrida0/CALC-ENCUCI-0001/spec.md';text=(ROOT/rel).read_text()
   safe=text[text.index('## Qué mide'):text.index('Los `ic95` GEN1')]
   safe=safe.replace(' (la codificación GEN1)','').replace(' — la primaria NO es la de GEN1 (familia A)','').replace('**codificación GEN1 — la única adoptable**','')
   safe=re.sub(r'\*\*`FP-201` es falso también para ENCUCI\n2020\*\*\.', '',safe)
   safe=safe.replace('`_cod()`','')
   files['metodo.md']=safe.encode()
   sources=[{'ruta':rel,'secciones':['Qué mide hasta párrafo comparación GEN1 excluido'],'supresiones':'contexto GEN1/FP201/nombre de función; normas de código/universos/diseño preservadas'}]
  if pid=='enbiare-pisos-bienestar-0001' and 'conductas.md' in files and files['conductas.md'] not in files['metodo.md']:
   files['metodo.md']+=b'\n'+files['conductas.md']
   sources=[{'ruta':'forense/analisis/salud-bienestar/lista-cerrada-P1.md','rangos':[[88,104]],'nota':'tabla incluida en método además documento separado'}]
  if pid=='envipe-denuncia-seguro-0001':
   text=files['metodo.md'].decode()
   text='\n'.join(' | '.join(line.split('|')[:6])+' |' if line.startswith('|') and 'RES-00' in line else line for line in text.splitlines())
   # Proyección Markdown de cuatro columnas: no legado en cabecera o filas.
   result=[]
   for line in text.splitlines():
    if line.lstrip().startswith('|'):
     parts=line.strip().split('|')
     if len(parts)>6:line='|'.join(parts[:5])+'|'
     line=line.replace(' | releva |',' |')
    result.append(line)
   text='\n'.join(result)+'\n'
   text=text.replace('El encargo pidió comprobarlo:','').replace('según\n   `data/inventario-reactivos-v1_2.tsv`','').replace('No hizo falta guardia de renombre. Pero','Pero')
   files['metodo.md']=text.encode()
   sources=[{'ruta':'data/corrida0/CALC-ENVIPE-DENUNCIA-SEGURO-0001/spec.md','supresiones':'columna releva/historia encargo/inventario; normas explícitas permanecen'}]
  if pid=='pisos-envipe2024-ejes-0002' and not any('escolaridad homologada' in f for f in rec['faltantes']):
   rec['faltantes'].append('NO-RECALCULABLE-DESDE-SPEC-PREPARACION: fuente humana de pisos2024 dice escolaridad homologada sin mapa códigos→categorías. Códigos no se inferirán de productor; dictamen de sesión nueva y documento previo por fuente/corte.')
  # Revisión por tipo de fuentes documentales realmente examinadas; permiso
  # de olas recientes se mantiene pendiente cuando no se identificó apertura.
  reviewed={'eder-0003','enbiare-pisos-bienestar-0001','encig-0001','encuci-0001','enfih-0001','enigh-0001','enigh2020-intensidad-remesas-0001','envipe-0001','envipe-denuncia-seguro-0001'}
  if pid in reviewed:
   review=rec['revision_semantica'];review['estado']='REVISADO-SIN-FILTRACIONES';review['metodo']='REVISADO-SIN-FILTRACIONES';review['insumos']=[]
   for item in ins:
    ident=item['id'];kind='cuestionario' if 'cuest' in ident else ('fd' if any(s in ident for s in ['_fd','descripcion_base','estructura_base']) else 'raw')
    recent=pid in {'enbiare-pisos-bienestar-0001','enfih-0001'} and kind=='raw'
    review['insumos'].append({'id':ident,'tipo':kind,'estado_acceso':'POR-VERIFICAR-AUTORIZACION' if recent else 'ABIERTO','autorizacion':None if recent else ('canon/MEMORIA-OPERATIVA.md §1: ENCIG2025/ENVIPE2025 abiertas' if '2025' in ident else 'Misión C1: documentos y olas históricas abiertas')})
  after={k:sha(v) for k,v in files.items()}
  if before==after:continue
  old=path.read_bytes();retired=PREP/'retirados'/path.name;retired.parent.mkdir(exist_ok=True);shutil.copyfile(path,retired)
  version=rec.get('version_entrada',2)+1
  files['manifiesto.json']=js({'paquete':pid,'version_entrada':version,'archivos':{n:sha(b) for n,b in sorted(files.items()) if n!='manifiesto.json'}})
  target=path.with_name(pid+'-entradas-v'+str(version)+'.tar.gz');pack(target,files)
  rec.update(archivo=str(target.relative_to(BASE)),sha256=sha(files['manifiesto.json']),sha256_manifiesto=sha(files['manifiesto.json']),sha256_contenedor=sha(target.read_bytes()),version_entrada=version)
  changes.append({'paquete':pid,'archivo_v2':str(path.relative_to(BASE)),'sha256_v2':sha(old),'archivo_v3':rec['archivo'],'sha256_v3':rec['sha256_contenedor'],'procedencia':sources})
 (PREP/'p2-sucesores.json').write_bytes(js(records));(PREP/'p2-curacion-final-procedencia.json').write_bytes(js(changes));print(js({'sucesores_v3':len(changes),'sin_faltantes':sum(not x['faltantes'] for x in records)}).decode())
if __name__=='__main__':run()
