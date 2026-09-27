#!/usr/bin/env python3
"""Preparación: sucesores por allowlist; no ejecuta recálculos ni abre raw."""
import gzip, hashlib, io, json, re, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'forense/validacion-independiente/catalogo-1'
BASE=ROOT/'forense/validacion-independiente/catalogo-1-preparacion-lote2'
PREP=BASE/'preparacion/p2'
def digest(b): return hashlib.sha256(b).hexdigest()
def js(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def archive(path,files):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as out,gzip.GzipFile(filename='',fileobj=out,mode='wb',mtime=0) as z:
  with tarfile.open(fileobj=z,mode='w') as t:
   for name,b in sorted(files.items()):
    info=tarfile.TarInfo(name);info.size=len(b);info.mode=0o644;t.addfile(info,io.BytesIO(b))
def run():
 original_lots=json.loads((OLD/'lotes.json').read_text())
 lots=[x for x in original_lots if x['estado_preparacion']=='INCOMPLETO']
 docs_by_raw={}
 for archived in original_lots:
  with tarfile.open(OLD/'paquetes'/archived['paquete']/archived['archivo']) as t:ins=json.loads(t.extractfile('insumos.json').read())
  raw=[x for x in ins if str(x.get('archivo','')).endswith(('.zip','.dta','.csv')) and '_fd' not in x['id'].lower() and not any(y in x['id'].lower() for y in ['encargo','descriptor','_der'])]
  for item in raw:
   yrs=set(re.findall(r'(?:19|20)\d{2}',item['id']))
   docs_by_raw.setdefault(item['id'],{})
   for doc in ins:
    ident=doc['id'].lower();dy=set(re.findall(r'(?:19|20)\d{2}',ident))
    if yrs and dy and not dy.issubset(yrs):continue
    if any(y in ident for y in ['cuest','_fd','estructura_base','descripcion_base','descriptor']):docs_by_raw[item['id']][doc['id']]=doc

 pages=(PREP/'endireh2006-original.local.txt').read_text().split('\f')
 # Todo el método de estos documentos mixtos se queda fuera; una extracción
 # sucesora posterior requiere lectura humana de rangos, nunca reconstrucción.
 quarantine={'amai-nse-endutih-2023-0001','amai-nse-enif-2024-0001','amai-nse-enigh-2022-0001',
 'ensanut-0001','enif-persistencia-ic-calibrado-0001','enoe-pisos-0003','evasion-norma-0001-v1_1',
 'horizonte-via-derivados-0001-v1_1','enigh2016-intensidad-remesas-0001',
 'enigh2018-intensidad-remesas-0001','enigh2020-intensidad-remesas-0001'}
 # Fragmentos humanos ya revisados: esquema/códigos/estimación, sin contexto
 # de resultados, historia o código. El mapa de exclusiones queda en PREP.
 from yaml import safe_load
 manifest={e['id']:e for e in safe_load((ROOT/'data/manifiesto.yaml').read_text())}
 records=[]; provenance=[]; cache={}
 docs_path=BASE/'preparacion/p1/p1-resoluciones.json'
 docs={r['paquete']:r for r in json.loads(docs_path.read_text())['resoluciones']} if docs_path.exists() else {}
 for lot in lots:
  pid=lot['paquete'];src=OLD/'paquetes'/pid/lot['archivo']
  with tarfile.open(src) as t: files={m.name:t.extractfile(m).read() for m in t.getmembers()}
  original=files.get('metodo.md',b'').decode()
  missing=list(lot['faltantes']);removed=[]
  if pid in quarantine:
   files.pop('metodo.md',None)
   missing.append('EXTRACCION-HUMANA: documento mixto en cuarentena; falta método completo libre de valores objetivo e historial.')
   removed=[{'todo':True,'razon':'revisión semántica detectó resultados/historial/referencias productores'}]
  else:
   # Excluir por párrafo completo para no dejar continuaciones de historia.
   paras=re.split(r'\n\s*\n',original)
   safe=[]
   bad=re.compile(r'tools/|forense/|milpa/|canon/|GEN1|hist[oó]ri|medidor|sellad|esperad|sucesi[oó]n|intento|KeyError|PR #|FP-\d|CORR-|RESULTADO|replay|reproduce|resultado.*previo|sha256.*declarado',re.I)
   for i,para in enumerate(paras):
    if bad.search(para):removed.append({'parrafo':i+1,'sha256':digest(para.encode()),'razon':'historial, referencia productor o contexto comparativo'})
    else:safe.append(para)
   method='\n\n'.join(safe).strip()+'\n'
   files['metodo.md']=method.encode()

  if pid=='enut-0001':
   mechanical=(ROOT/'data/corrida0/CALC-ENUT-0001/spec.md').read_text().splitlines(keepends=True)
   sealed=(ROOT/'forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md').read_text().splitlines(keepends=True)
   method='# Método: extracción fiel de especificación humana\n\n'+''.join(mechanical[15:28])+ '\n'+''.join(mechanical[42:49])+ '\n'+''.join(sealed[173:182])
   # La guarda es parte del método previo: extraer literalmente sin la historia.
   method+='\n'+''.join(sealed[113:118])
   files['metodo.md']=method.encode()
   missing=[m for m in missing if not m.startswith(('FILTRACION-TEXTUAL:','EXTRACCION-HUMANA:'))]
   provenance.append({'paquete':pid,'ruta':'data/corrida0/CALC-ENUT-0001/spec.md','rangos':[[16,28],[43,49]],'sha256':digest((ROOT/'data/corrida0/CALC-ENUT-0001/spec.md').read_bytes())})
   provenance.append({'paquete':pid,'ruta':'forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md','rangos':[[174,182],[114,118]],'sha256':digest((ROOT/'forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md').read_bytes())})
  if pid=='endireh-pisos-2006-modulos-0002':
   for label,a,b in [('general-mc',153,173),('md',175,190),('ms',191,195)]:
    files['cuestionario-'+label+'.md']=(''.join(pages[a-1:b])).encode()
    provenance.append({'paquete':pid,'id':'endireh2006_tabulados_cuestionarios_pdf','pagina_fisica':[a,b],'salida':'cuestionario-'+label+'.md','tipo':'texto pdftotext -layout','sha256_fuente':'6a3ae3b23f0b0241b536e2fb1ec7de08b25af5d43318ec35a2fa379f6a965a55'})
   inputs=json.loads(files['insumos.json'])
   files['insumos.json']=js([x for x in inputs if x['id']!='endireh2006_tabulados_cuestionarios_pdf'])
   missing=[m for m in missing if not m.startswith('CUESTIONARIOS-MC-MD-MS:')]
   missing.append('DEFECTO-CONCEPTUAL: spec declara P7_4 anual MC/MD; cuestionario MD pregunta después de separación. Dictamen del validador requerido; no corregir contrato congelado.')
  if pid in {'enbiare-pisos-bienestar-0001','encodat-pisos-sustancias-0001'}:
   clause=next(para for para in re.split(r'\n\s*\n',original) if 'Tabla en `forense/analisis/salud-bienestar/lista-cerrada-P1.md`' in para)
   clause=clause[clause.index('spec.')+5:]
   files['metodo.md']+=('\n'+clause+'\n').encode()
  if pid=='ensanut-pisos-salud-0001':
   paragraphs=re.split(r'\n\s*\n',original)
   normative=next(para for para in paragraphs if '**IC de diseño:**' in para)
   normative=normative[:normative.index('Código:')].rstrip()
   files['metodo.md']+=('\n'+normative+'\n').encode()
  if pid in {'ensanut-pisos-salud-0001','encodat-pisos-sustancias-0001','enbiare-pisos-bienestar-0001'}:
   text=(ROOT/'forense/analisis/salud-bienestar/lista-cerrada-P1.md').read_text().splitlines(keepends=True)
   span={'ensanut-pisos-salud-0001':(35,49),'encodat-pisos-sustancias-0001':(68,79),'enbiare-pisos-bienestar-0001':(88,104)}[pid]
   a,b=span;files['conductas.md']=''.join(text[a-1:b]).encode()
   provenance.append({'paquete':pid,'ruta':'forense/analisis/salud-bienestar/lista-cerrada-P1.md','rangos':[[a,b]],'sha256':digest((ROOT/'forense/analisis/salud-bienestar/lista-cerrada-P1.md').read_bytes())})
   missing=[m for m in missing if not m.startswith('LISTA-CERRADA-P1:')]
  if pid=='encig-0001':
   human=ROOT/'data/corrida0/CALC-ENCIG-0001/spec.md';lines=human.read_text().splitlines(keepends=True)
   safe=''.join(lines[18:30])+'\n'+lines[33]+lines[34].split('GEN1')[0]+'\n'+''.join(lines[37:41])+'\n'+''.join(lines[41:43])+''.join(lines[44:46])+'\n'+''.join(lines[49:52]).split('Igual que')[0]+'\n'+''.join(lines[55:62])
   safe=safe.replace('La rama `CD` reproduce la corrida base y','').replace('   tres** y,','').replace('   eventos repetidos del mismo tipo. ','   eventos repetidos del mismo tipo. ')
   files['metodo.md']=safe.encode()
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   provenance.append({'paquete':pid,'ruta':str(human.relative_to(ROOT)),'sha256':digest(human.read_bytes()),'rangos':[[19,30],[34,35],[38,43],[45,46],[50,52],[56,62]],'supresiones':'historial GEN1, precedente llave y comparación ENVIPE; controles y cifras excluidos'})
  if pid.startswith('amai-nse-'):
   human=ROOT/'forense/prereg-caja/AMAI-NSE-spec-v1_0.md'
   lines=human.read_text().splitlines(keepends=True)
   safe=''.join(lines[6:25])+ '\n'+''.join(lines[30:43])
   # Suprimir solo remisiones al implementador en la prosa normativa.
   safe=safe.replace('(el medidor para)','')
   estimation=lines[48];estimation=estimation[estimation.index('con el grupo NSE'):]
   estimation=estimation.replace(', módulo `tools/celda_d/marginales_reproduccion.py`','')
   safe+='\n'+estimation
   if 'enigh-2022' in pid:safe+='\n'+lines[52]
   files['metodo.md']=safe.encode()
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   missing.append('CONTRATO-PARCIAL: referencias de validación publicadas AMAI quedan fuera; falta contrato ciego para esos estimandos. Conductas ENIF/ENDUTIH remiten helpers; no completar desde ellos.')
   provenance.append({'paquete':pid,'ruta':str(human.relative_to(ROOT)),'sha256':digest(human.read_bytes()),'rangos':[[7,25],[31,43],[49,49],[53,53]],'supresiones':'distribución porcentual pública, productor y referencias de validación'})
  if pid.startswith(('enigh2016-intensidad','enigh2018-intensidad','enigh2020-intensidad')):
   human=ROOT/'data/corrida0/CALC-ENIGH2022-INTENSIDAD-REMESAS-0001/spec.md'
   text=human.read_text();safe=text[text.index('## Universo y dominios'):text.index('## Interpretación y límites')]
   safe=safe.replace('de 90,102 hogares ','').replace(', con control contra `CALC-ENIGH-0001`','')
   files['metodo.md']=safe.encode()
   missing=[m for m in missing if not m.startswith(('METODO-MEZCLADO:','EXTRACCION-HUMANA:'))]
   provenance.append({'paquete':pid,'ruta':str(human.relative_to(ROOT)),'sha256':digest(human.read_bytes()),'secciones':['Universo y dominios','Cinco estadísticos principales','Incertidumbre'],'supresiones':['de 90,102 hogares ','control contra CALC-ENIGH-0001']})
  if pid=='ensanut-0001':
   human=ROOT/'data/corrida0/CALC-ENSANUT-0001/spec.md';lines=human.read_text().splitlines(keepends=True)
   files['metodo.md']=(''.join(lines[24:35])+'\n'+lines[37]+''.join(lines[40:42])).encode()
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   missing.append('METODO-PARCIAL: resumen define menciones y ponderación; extraer diseño IC desde S7-L17 humano, sin N observado ni controles publicados.')
  if pid=='evasion-norma-0001-v1_1':
   human=ROOT/'data/corrida0/CALC-EVASION-NORMA-0001-v1_1/spec.md';lines=human.read_text().splitlines(keepends=True)
   safe='| campo | valor |\n|---|---|\n'+''.join(lines[63:68])
   safe=safe.replace('; `n=40 280`, sin pérdida','')
   safe=safe.replace(' — reserva declarada en `milpa/tramite.yaml:513`','')
   safe=safe.replace(' (`wprop_ic_conglomerado`, misma función que `S7-L17`)','')
   files['metodo.md']=safe.encode()
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   missing.append('METODO-PARCIAL: tabla humana previa fija universo, desenlace y plan; algoritmo de IC completo remite a función. No reconstruir desde código.')
  if pid=='enif-persistencia-ic-calibrado-0001':
   human=ROOT/'forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md'
   text=human.read_text();safe=text[text.index('## §4 · Regla del intervalo'):text.index('## §5 · Cobertura')]
   files['metodo.md']=safe.encode()
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   missing.append('METODO-PARCIAL: fórmula calibrado extraída fielmente; faltan reconstrucción independiente de pisos humanos y controles excluidos por valor esperado.')
  if pid=='horizonte-via-derivados-0001-v1_1':
   # Sigue detenido: los inputs derivados son valores objetivos conocidos.
   missing=[m for m in missing if not m.startswith('EXTRACCION-HUMANA:')]
   missing.append('METODO-PARCIAL: complementariedad/inclusión-exclusión requieren padres reconstruidos ciegamente; entregar encadenado tras sus sellos propios, sin leer productores o puntos originales.')
  if pid=='enoe-pisos-0003':
   human=ROOT/'forense/prereg-caja/ENOE-PISOS-spec-v1_2.md'
   lines=human.read_text().splitlines(keepends=True)
   files['metodo.md']=('# Método: extracción fiel de especificación humana\n\n'+''.join(lines[27:107])+ '\n'+ lines[126].split(',')[0]+'.\n'+''.join(lines[142:144])).encode()
   for name in ['enoe-reactivos-olas-v1_0.tsv','enoe-olas-elegibles-preparacion-v1_0.tsv']:
    source=ROOT/'data'/name;files[name]=source.read_bytes()
    provenance.append({'paquete':pid,'ruta':str(source.relative_to(ROOT)),'sha256':digest(source.read_bytes()),'extraccion':'completa: matriz documental previa sin observados'})
   provenance.append({'paquete':pid,'ruta':str(human.relative_to(ROOT)),'sha256':digest(human.read_bytes()),'rangos':[[28,107],[127,127],[143,144]],'supresiones_textuales':['referencia v1.0 omitía y logs de ejecución']})
   inputs=json.loads(files['insumos.json'])
   admin='encargoEG_ruptura_enoe_y_descriptores_pendientes_navegador'
   files['insumos.json']=js([x for x in inputs if x['id']!=admin])
   missing=[m for m in missing if not m.startswith(('METODO-MEZCLADO:','EXTRACCION-HUMANA:')) and admin not in m]
   missing.append('METODO-PARCIAL: semilla PCG64(42+i_ola) no fija explícitamente base del índice i_ola ni orden del marco UPM. Dictamen D-15 por sesión nueva; no completar desde código.')
  inputs=json.loads(files['insumos.json'])
  for item in list(inputs):
   for doc in docs_by_raw.get(item['id'],{}).values():
    if doc['id'] not in {x['id'] for x in inputs}:inputs.append(doc)
  files['insumos.json']=js(inputs)
  # Añadir sólo documentos identificados y exactos por ola, nunca sustitutos.
  inputs=json.loads(files['insumos.json'])
  exact=[]
  for candidate in docs.get(pid,{}).get('documentos_candidatos',[]):
   ident=candidate['id']
   if ident in {x['id'] for x in inputs}:continue
   # P1 puede listar candidatas de otra ola: evitar la ampliación por analogía.
   years=set(re.findall(r'(?:19|20)\d{2}',pid)) or {year for x in inputs if str(x.get('archivo','')).endswith(('.zip','.dta','.csv')) and '_fd' not in x['id'].lower() for year in re.findall(r'(?:19|20)\d{2}',x['id'])}
   identified=set(re.findall(r'(?:19|20)\d{2}',ident))
   if years and identified and not identified.issubset(years):continue
   e=manifest.get(ident,{})
   if not e.get('archivo') or not e.get('sha256'):continue
   source=ROOT/'data/raw'/e['archivo']
   if source.is_file() and digest(source.read_bytes())==e['sha256']:
    inputs.append({'id':ident,'archivo':e['archivo'],'sha256':e['sha256'],'url':e.get('url_origen'),'estado_acceso':'COINCIDE'})
    exact.append(ident)
  files['insumos.json']=js(inputs)
  if any('cuest' in x['id'].lower() for x in inputs):missing=[m for m in missing if not m.startswith('CUESTIONARIO:')]
  if any(any(k in x['id'].lower() for k in ['_fd','descriptor','descripcion_base','estructura_base']) for x in inputs):missing=[m for m in missing if not m.startswith('FD:')]
  provenance.append({'paquete':pid,'documentos_agregados':exact})
  # No se entrega el ZIP ENIF mezclado en ninguna entrada sucesora.
  inputs=json.loads(files['insumos.json']);blocked=[x for x in inputs if x['id']=='enif_2024_enif_2024_bd_csv']
  if blocked:files['insumos.json']=js([x for x in inputs if x not in blocked])
  fragment_map={'endireh-pisos-2021-pareja-fisica-0004':['p1-endireh2021-a-marco-bootstrap.md'],
  'endireh-pisos-2021-pareja-fisica-bc-0001':['p1-endireh2021-bc-diseno.md'],
  'dinero-familiares-vejez-0001-v1_1':['p1-enif2024-dinero-familiares-definiciones.md','p1-enif2024-dinero-familiares-diseno.md'],
  'enif-persistencia-ic-calibrado-0001':['p1-enif2021-piso-contrato.md','p1-enif2021-piso-posicional.md']}
  for name in fragment_map.get(pid,[]):
   source=BASE/'preparacion/p1/fragmentos'/name
   content=source.read_bytes()
   if 'definiciones' in name:content=b'\n'.join(content.splitlines()[:4])+b'\n'
   files.setdefault('metodo.md',b'');files['metodo.md']+=b'\n'+content
   provenance.append({'paquete':pid,'fragmento_p1':str(source.relative_to(ROOT)),'sha256':digest(source.read_bytes()),'revision':'P2 texto humano leído sin datos observados; definiciones vejez sólo primeras4 líneas'})
  recovered={'endireh-pisos-2021-pareja-fisica-0004','endireh-pisos-2021-pareja-fisica-bc-0001'}
  if pid in recovered:missing=[m for m in missing if not m.startswith('METODO-MEZCLADO:')]
  if pid=='dinero-familiares-vejez-0001-v1_1':
   missing=[m for m in missing if not m.startswith('METODO-MEZCLADO:')]
   missing.append('NO-RECALCULABLE-DESDE-SPEC-PREPARACION: dos fuentes humanas previas definen bootstrap ponderado simple10k seed42 sin mecanismo exacto de selección/ponderación. Dictamen D-15 del validador; no leer implementación.')
  parent_map={'encig-0001-complementos-derivado-0001':'encig-0001','encuci-0001-complemento-derivado-0001':'encuci-0001','envipe-res0028-u4-derivado-0001':'envipe-0001'}
  if pid in parent_map:
   parent=parent_map[pid]
   if parent in cache:files['metodo-padre.md']=cache[parent]['metodo.md']
   method=files['metodo.md'].decode()
   method='\n'.join(line for line in method.splitlines() if not re.search(r'legacy|LEGACY|COINCIDE-AL-GRANO|COMPATIBILIDAD-LEGACY',line))+'\n'
   files['metodo.md']=method.encode()
   missing=[m for m in missing if not m.startswith('METODO-MEZCLADO:')]
   missing.append('ENCADENADO-CIEGO: reconstruir y sellar primero los puntos/IC del padre desde metodo-padre.md; aplicar transformación humana al valor propio, nunca al productor original. Dictamen conjunto pendiente.')
  if pid=='eder-0003':
   files['metodo.md']=files['metodo.md'].replace(b'(0 casos); ',b'')
  cache[pid]=files.copy()
  if pid=='enut-0001':
   inputs=json.loads(files['insumos.json'])
   files['insumos.json']=js([x for x in inputs if x['id']!='enut2024_bd_csv'])
   missing.append('BLOQUEADO-POR-ACCESO: ENUT2024 reparto_hogar×sexo_edad sigue reservado; FP-260922-GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1-bda6-02 no autoriza entregar ZIP a nueva sesión. Método limpio disponible para dictamen.')
  embedded=[]
  if pid.startswith('endireh-pisos-2016-'):
   source=BASE/'preparacion/p1/documentos/p1-endireh2016-fd.xlsx';content=source.read_bytes()
   assert digest(content)=='b4b2359806d50922403d50ebc764a1f54b8265c864c37df92e0a6e631dbd35e9'
   files['fd-endireh2016.xlsx']=content
   embedded.append({'archivo':'fd-endireh2016.xlsx','tipo':'fd','estado':'REVISADO-SIN-FILTRACIONES','sha256':digest(content),'revision':'P2 revisión26hojas esquema/códigos; TSDem,TB_SEC_III,TB_SEC_VII,FACTORES,ID_MUJ'})
   missing=[m for m in missing if not m.startswith('FD:')]
   provenance.append({'paquete':pid,'fd_documental':str(source.relative_to(ROOT)),'url':'https://www.inegi.org.mx/contenidos/programas/endireh/2016/doc/fd_endireh2016.xlsx','sha256':digest(content)})
  for document in docs.get(pid,{}).get('documentos_adquiridos',[]):
   source=ROOT/document['ruta']
   if document.get('estado')!='PDF-ADQUIRIDO' or not source.is_file():continue
   content=source.read_bytes()
   if not content.startswith(b'%PDF-') or digest(content)!=document['sha256']:raise ValueError('Documento inválido: '+str(source))
   name=document['nombre'].replace('p1-','cuestionario-')
   files[name]=content;embedded.append({'archivo':name,'tipo':'cuestionario','estado':'REVISADO-SIN-FILTRACIONES','sha256':document['sha256'],'revision':'P1 encabezados/formulario vacío; P2 páginas por tipo e ítems de familia'})
   provenance.append({'paquete':pid,'documento_adquirido':document,'salida':name})
  if any(x['tipo']=='cuestionario' for x in embedded):missing=[m for m in missing if not m.startswith('CUESTIONARIO:')]
  if pid in {'envipe-denuncia-seguro-0001','pisos-envipe2024-ejes-0002'}:
   year='2025' if pid=='envipe-denuncia-seguro-0001' else '2024'
   inputs=json.loads(files['insumos.json'])
   inputs=[x for x in inputs if year in x['id'] and 'diseno_muestral' not in x['id']]
   files['insumos.json']=js(inputs)
   method=files['metodo.md'].decode()
   if pid=='envipe-denuncia-seguro-0001':
    a=method.index('1. **Es la opción A');b=method.index('2. **`EST_DIS`',a);method=method[:a]+method[b:]
   else:
    method='\n'.join(l for l in method.splitlines() if not l.startswith('Prerregistro correctivo'))+'\n'
   files['metodo.md']=method.encode()
  if pid=='enigh2016-intensidad-remesas-0001':missing.append('BLOQUEADO-POR-ACCESO-DOCUMENTAL: cuestionario exacto2016 no obtenido P1; URLs oficiales ensayadas devolvieron HTML2002263bytes. Reintentar índice oficial2016, sin sustituirlo con ola2022.')
  # Faltantes solo en preparación: contienen historia y razones no ciegas.
  files.pop('faltantes.json',None)
  files['encargo.md']=b'# Reconstruccion independiente\n\nSesion nueva sin historial. Lee solo estas entradas y los insumos enumerados. Implementa cada llave de estimandos.tsv desde metodo.md y documentos humanos, con bibliotecas genericas. Si falta metodo, tolerancia o acceso, informa el faltante sin adivinar. Congela codigo propio y numeros antes de pedir revelacion. Conserva hash de manifiesto.json.\n'
  files['manifiesto.json']=js({'paquete':pid,'version_entrada':2,'archivos':{n:digest(b) for n,b in sorted(files.items()) if n!='manifiesto.json'}})
  target=BASE/'entradas'/pid/(pid+'-entradas-v2.tar.gz');archive(target,files)
  review={'estado':'PENDIENTE-P3','documentos':embedded,'metodo':'REVISADO-SIN-FILTRACIONES','insumos':[]}
  if pid in {'envipe-denuncia-seguro-0001','pisos-envipe2024-ejes-0002','endireh-pisos-2016-discriminacion-0001','endireh-pisos-2016-pareja-fisica-0002','endireh-pisos-2016-restantes-0001'}:
   review['estado']='REVISADO-SIN-FILTRACIONES'
   for item in json.loads(files['insumos.json']):
    ident=item['id'];kind='cuestionario' if 'cuest' in ident else ('fd' if '_fd' in ident else 'raw')
    review['insumos'].append({'id':ident,'tipo':kind,'estado_acceso':'ABIERTO','autorizacion':('canon/MEMORIA-OPERATIVA.md §1 ENVIPE2025 abiertas; misión C1 microdato olas abiertas' if '2025' in ident else 'Misión C1: olas históricas abiertas '+('ENDIREH2016' if '2016' in ident else 'ENVIPE2024'))})
  record={**lot,'archivo':str(target.relative_to(BASE)),'sha256_contenedor':digest(target.read_bytes()),'sha256':digest(files['manifiesto.json']),'sha256_manifiesto':digest(files['manifiesto.json']),'faltantes':missing,'estado_preparacion':'PENDIENTE-VERIFICACION-P3','original_sha256_contenedor':lot['sha256_contenedor'],'revision_semantica':review,'acciones':docs.get(pid,{}).get('acciones',[])}
  records.append(record)
  provenance.append({'paquete':pid,'original_contenedor':str(src.relative_to(ROOT)),'sha256_original':digest(src.read_bytes()),'supresiones':removed,'insumo_retendido_en_preparacion':blocked})
 (PREP/'p2-sucesores.json').write_bytes(js(records));(PREP/'p2-procedencia-supresiones.json').write_bytes(js(provenance))
 print(json.dumps({'sucesores':len(records),'sin_faltantes_antes_P3':sum(not x['faltantes'] for x in records)}))
if __name__=='__main__':run()
