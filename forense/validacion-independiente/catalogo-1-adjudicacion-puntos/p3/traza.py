#!/usr/bin/env python3
"""Traza puntos revelados, sin raw ni ejecutar productores. Diagnóstico no adopción."""
import csv, hashlib, json, subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
inputs=set()
def tsv(p):
 p=ROOT/p if not isinstance(p,Path) else p;inputs.add(p)
 with p.open() as f:return list(csv.DictReader((l for l in f if not l.startswith('#')),delimiter='\t'))
def js(p):
 p=ROOT/p if not isinstance(p,Path) else p;inputs.add(p);return json.loads(p.read_text())
def write(name,rows):
 if not rows:return
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
p1path=ROOT/'forense/validacion-independiente/catalogo-1-adjudicacion-puntos/p1/adjudicacion.tsv'
p1={r['identidad_original']:r for r in tsv(p1path)} if p1path.exists() else {}
effects=[r for r in tsv(BASE/'efectos-discrepancias.tsv') if r['componente']=='punto']
meta={r['llave']:r for r in tsv(BASE/'tabla-estimadores.tsv')}
cat={r['llave']:r for r in tsv('canon/catalogo-del-mexicano-v1_2.tsv')}
piso={r['llave']:r for r in tsv('canon/tabla-de-piso-v1_1.tsv')}
recon={}
for pk in {e['paquete'] for e in effects}:
 p=BASE/'reconstrucciones'/pk/(pk+'--reconstruccion.tsv');recon.update({r['llave']:r for r in tsv(p)})
tables={}
for calc in {meta[e['llave']]['calc'] for e in effects}:
 ob=js('data/corrida0/'+calc+'/resultados.json')['resultados']
 for rid,val in ob.items():
  if rid.endswith('TABLA'):tables[rid]=json.loads(val) if isinstance(val,str) else val
exports={}
for rid in tables:
 name='endireh-2011-modulos-tabla.tsv' if '2011' in rid else 'endireh-2021-pareja-nofisica-bc-tabla.tsv'
 exports[rid]=tsv('forense/analisis/dominios/genero/'+name)
series=tsv('forense/analisis/donde-cambio/mapa/resto.tsv')
series_by=defaultdict(list)
for r in series:
 ref=r['result_p'];rid=ref.split('#')[0]
 if rid not in tables:continue
 sel={unquote(k):unquote(v) for k,v in (kv.split('=',1) for kv in ref.split('#',1)[1].rsplit('/',1)[0].split('&'))}
 matches=[i for i,c in enumerate(tables[rid]) if all(str(c.get(k,''))==v for k,v in sel.items())]
 for i in matches:series_by[f'{rid}#{i}'].append(r)
# Descomprime diccionarios: llave vacía se deriva de RESULT y celda en la vista Pages.
pages={}
for ver in ['1_1','1_2']:
 ob=js('docs/data/catalogo-v'+ver+'.json'); entries={}
 for row in ob['filas']:
  rr={k:ob['diccionarios'][k][v] if k in ob['diccionarios'] else v for k,v in zip(ob['columnas'],row)}
  key=rr['llave'] or rr['result_id']+('#'+str(rr['celda']) if str(rr['celda']) else '')
  entries[key]=rr
 pages[ver]=entries
dc=js('data/corrida0/CALC-ENDIREH-SERIE-DICTAMEN-0001/resultados.json')['resultados']; dcrows=json.loads(dc['RESULT-DC-ENDIREH-TABLA']); dcby={r['serie_id']:r for r in dcrows}
inputs.add(ROOT/'data/corrida0/CALC-ENDIREH-SERIE-DICTAMEN-0001/spec.yaml')
inputs.add(ROOT/'canon/donde-cambio-el-mexicano-v1_0.md')
results=tsv('data/corrida0/resultados.tsv');uses=tsv('data/corrida0/usos.tsv')
# Consumidores potenciales del CALC/tablas/series: examina solo texto versionado.
paths=subprocess.check_output(['git','ls-files','*.md','*.tsv','*.yaml'],cwd=ROOT,text=True).splitlines()
texts={}
for path in paths:
 if path.startswith(('forense/validacion-independiente/','data/raw/')):continue
 if path.startswith(('corpus/','canon/','milpa/','forense/analisis/','docs/')):
  try:texts[path]=(ROOT/path).read_text()
  except (UnicodeError,OSError):pass
p2dir=ROOT/'forense/validacion-independiente/catalogo-1-adjudicacion-puntos/p2'
p22021={(r['conducta'],r['universo']):r for r in tsv(p2dir/'contrastes-raw2021-v4.tsv')} if (p2dir/'contrastes-raw2021-v4.tsv').exists() else {}
p22011={r['llave']:r for r in tsv(p2dir/'cotejo-final2011.tsv')} if (p2dir/'cotejo-final2011.tsv').exists() else {}
rows=[];edges=[];patches=[]
for e in effects:
 key=e['llave'];m=meta[key];rid=m['result_id'];i=int(m['celda']);c=tables[rid][i];cr=recon[key];delta=float(cr['punto'])-float(c['p']);cc=cat.get(key,{});pp=piso.get(key,{})
 group=[(j,v) for j,v in enumerate(tables[rid]) if v.get('resultado')==c.get('resultado') and v.get('ventana','')==c.get('ventana','') and v['eje']==c['eje'] and v.get('p') is not None]
 before=1+sum(v['p']>c['p'] for j,v in group)
 after=1+sum(float((recon.get(f'{rid}#{j}',{}).get('punto') or v['p']))>float(cr['punto']) for j,v in group)
 aliases=series_by[key]
 refs=[]
 for path,txt in texts.items():
  if path.startswith(('corpus/reports','forense/analisis/reports-v2')) and (key in txt or any(a['serie_id'] in txt for a in aliases)):refs.append(path)
 # No inferir selector de la sola mención a la tabla.
 generic=[p for p,t in texts.items() if p.startswith(('corpus/reports','forense/analisis/reports-v2')) and (rid in t or m['calc'] in t)]
 directuses=[u for u in uses if u.get('resultado_id') in [key,rid] or u.get('corrida0_resultado_id') in [key,rid]]
 row={'identidad_original':key,'calc':m['calc'],'result_id':rid,'registro_tabla':i,'conducta':c['resultado'],'ventana':c.get('ventana',''),'eje':c['eje'],'segmento':c['categoria'],'p_productor':c['p'],'p_reimplementacion':cr['punto'],'delta_nativo':delta,'delta_pp':delta*100,'sentido':'reimplementacion_menos_productor','denominador_n_productor':c.get('n',''),'denominador_masa_productor':c.get('masa_ponderada',''),'denominador_reimplementacion':'NO-DISPONIBLE en reconstruccion.tsv; requiere P2','denominador_definicion_ref':f"data/corrida0/{m['calc']}/spec.yaml; resultado={c['resultado']}; ventana={c.get('ventana','')}",'registro_exportado':f"forense/analisis/dominios/genero/{'endireh-2011-modulos-tabla.tsv' if '2011' in rid else 'endireh-2021-pareja-nofisica-bc-tabla.tsv'}:fila={i}",'exportado_coincide_p':str(float(exports[rid][i]['p'])==c['p']),'catalogo_actual':str(key in cat),'piso_actual':str(key in piso),'pages_v1_1':str(key in pages['1_1']),'pages_v1_2':str(key in pages['1_2']),'adopcion':cc.get('estado_adopcion','NO-EN-CATALOGO'),'firma':cc.get('firma_fp',''),'series_alias':'|'.join(a['serie_id'] for a in aliases),'series_par_estado':'|'.join(sorted({a['par_con_anterior'] for a in aliases})),'rango_desc_productor':before,'rango_desc_reimplementacion':after,'rango_grupo_n':len(group),'rango_interpretacion':'COMPARACION-DIAGNOSTICA; sin punto reimplementado se conserva productor; no adopta cifras ni asegura mismo universo','dictamen_serie':'|'.join(sorted({dcby.get(a['serie_id'],{}).get('dictamen','NO-LOCALIZADO') for a in aliases})), 'consumidor_serie':'CALC-ENDIREH-SERIE-DICTAMEN-0001→RESULT-DC-ENDIREH-TABLA→canon/donde-cambio-el-mexicano-v1_0.md', 'umbral_efectivo':'DICTAMEN-SERIE: al menos 2 olas comparables; actuales SIN-SERIE no dependen del nivel puntual. Cobertura z=1.959964 no activa sin tramo. Publicabilidad: sesion02','cruce_mitad_diagnostico':str((c['p']>=.5)!=(float(cr['punto'])>=.5)),'regla_mitad':'EXPLORATORIO; no umbral adoptado','afirmacion_report_consumo_exacto':'|'.join(refs) or 'NO-IDENTIFICADA','mencion_tabla_sin_selector':'|'.join(generic) or 'NINGUNA','consumidor_numerico':'CATALOGO/PISO/PAGES/SERIES/DICTAMEN-TEMPORAL; vistas resultado/usos no cubren tablas','usos_vista_n':len(directuses),'conclusion':'Punto de producto discrepante; dictamen documental P1 incorporado por identidad; atribución exhaustiva y cambio de universo sujetos a contrastes P2. SIN-SERIE temporal conserva su conclusión ante cambio solo del punto con mapa/comparabilidad fijos. Cambio narrativo específico no acreditado. No acredita retiro ni sustitución automática.'}
 aux=p22021.get((c['resultado'],'60+_observada')) if '2021' in rid else None
 if aux:
  row.update({'denominador_n_variante_P2':aux['n'],'denominador_masa_variante_P2':aux['masa'],'delta_denominador_n_P2':int(aux['n'])-int(c['n']),'delta_denominador_masa_P2':float(aux['masa'])-float(c['masa_ponderada']),'denominador_P2_ref':'p2/contrastes-raw2021-v4.tsv;60+_observada','punto_variante_P2':aux['punto'],'punto_P2_reimplementacion_coincide':str(abs(float(aux['punto'])-float(cr['punto']))<=1e-10),'denominador_reimplementacion':'Variante P2 final 60+_observada coincide en punto con primera reconstrucción; n/masa propios de variante, no publicados por primera sesión'})
 elif key in p22011:
  a=p22011[key]
  row.update({'denominador_n_variante_P2':a['n_propuesto'],'denominador_masa_variante_P2':a['masa_propuesta'],'delta_denominador_n_P2':int(a['n_propuesto'])-int(c['n']),'delta_denominador_masa_P2':float(a['masa_propuesta'])-float(c['masa_ponderada']),'denominador_P2_ref':'p2/cotejo-final2011.tsv;edad_corregida=1;regla_corregida=1;'+a['limite'],'punto_variante_P2':a['punto_propuesto'],'punto_P2_reimplementacion_coincide':str(abs(float(a['punto_propuesto'])-float(cr['punto']))<=1e-10),'denominador_reimplementacion':'Variante P2 final coincide en punto con primera reconstrucción; n/masa propios de variante, no publicados por primera sesión'})
 else:
  row.update({'denominador_n_variante_P2':'','denominador_masa_variante_P2':'','delta_denominador_n_P2':'','delta_denominador_masa_P2':'','denominador_P2_ref':'2011-v2 en ejecución; no consumir primer intento','punto_variante_P2':'','punto_P2_reimplementacion_coincide':''})
 ad=p1.get(key,{})
 row.update({'dictamen_documental_P1':ad.get('dictamen_documental','NO-DISPONIBLE'),'familia_P1':ad.get('familia',''),'evidencia_ref_P1':ad.get('evidencia_ref',''),'limite_atribucion_P1':ad.get('limite_atribucion',''),'propuesta_P1':ad.get('propuesta','')})
 rows.append(row)
 for target,kind in [(row['registro_exportado'],'exportacion_tabla'),('canon/catalogo-del-mexicano-v1_2.tsv#'+key,'catalogo'),('canon/tabla-de-piso-v1_1.tsv#'+key,'piso')]+[(f'docs/data/catalogo-v{v}.json#{key}','pages') for v in pages if key in pages[v]]+[(a['result_p'],'alias_selector_serie') for a in aliases]+[(f"RESULT-DC-ENDIREH-TABLA#serie_id={a['serie_id']}",'dictamen_temporal') for a in aliases]+[('canon/donde-cambio-el-mexicano-v1_0.md','informe_temporal_agregado')]:edges.append({'identidad_original':key,'origen':key,'destino':target,'tipo':kind})
 patches.append({'id_afirmacion':'PRODUCTO:'+key,'objeto':'catalogo/piso/Pages/series (consumidor descriptivo)','identidad_original':key,'estado':'PROPUESTO-POR-EJECUTOR','operacion':'Añadir reserva por identidad; mantener punto sellado hasta acto sucesor firmado','texto_propuesto':f"{key}: DISCREPA-PUNTO, diagnóstico posterior a revelación; delta={delta:.17g} proporción ({delta*100:.17g} pp) frente a reimplementación. No sustitución ni conclusión causal; dictamen documental P1 y contraste final P2 disponibles por identidad, sucesor pendiente de firma.",'razon':'Evitar presentar adopción como coincidencia independiente; derivar reserva desde fuente tras firma, no parchear vistas.'})
write('efectos-producto.tsv',rows);write('linaje-consumidores.tsv',edges)
maprows=tsv('canon/mapa-dominios-v1_1.tsv')
for mr in maprows:
 if 'RESULT-ENDIREH2021-NF-BC-TABLA' not in mr['gen2_existente']:continue
 patches.append({'id_afirmacion':mr['id_afirmacion'],'objeto':mr['report']+'@'+mr['localizador'],'identidad_original':'RESULT-ENDIREH2021-NF-BC-TABLA#494|RESULT-ENDIREH2021-NF-BC-TABLA#543','estado':'PROPUESTO-POR-EJECUTOR','operacion':'Conservar afirmación externa; acotar referencia auxiliar por población y ventana','texto_propuesto':'La referencia auxiliar de no física A/B/C nacional no valida este agregado ni su población. La adjudicación encuentra discrepancias de punto en ayuda_bc/denuncia_bc de 60+ desde inicio de relación; no afecta por identidad la cifra nacional de violencia no física aquí citada. No sumar física y no física ni trasladar cortes de edad a población nacional.','razon':'Linaje indirecto por mapa, sin consumo numérico de celdas 494/543; no adjudicar 38.27% usando deltas de ayuda/denuncia.'})
write('parches-propuestos.tsv',patches)
summary={'commit_corte':'11602de8e375c10b90807d1b74e088f6b9e99c8b','HEAD_ejecucion':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'identidades':len(rows),'identidades_unicas':len({r['identidad_original'] for r in rows}),'catalogo':sum(r['catalogo_actual']=='True' for r in rows),'piso':sum(r['piso_actual']=='True' for r in rows),'pages_v1_2':sum(r['pages_v1_2']=='True' for r in rows),'series':sum(bool(r['series_alias']) for r in rows),'rango_cambia_diagnostico':sum(r['rango_desc_productor']!=r['rango_desc_reimplementacion'] for r in rows),'denominadores_P2_disponibles':sum(bool(r['denominador_n_variante_P2']) for r in rows),'puntos_P2_reimplementacion_coinciden':sum(r['punto_P2_reimplementacion_coincide']=='True' for r in rows),'cruce_mitad_diagnostico':sum(r['cruce_mitad_diagnostico']=='True' for r in rows),'consumo_exacto_report':sum(r['afirmacion_report_consumo_exacto']!='NO-IDENTIFICADA' for r in rows),'max_abs_pp':max(abs(r['delta_pp']) for r in rows),'aristas':len(edges),'parches':len(patches),'fuentes_hash':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)}}
(OUT/'c1-puntos-p3-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='fuentes_hash'},ensure_ascii=False))
