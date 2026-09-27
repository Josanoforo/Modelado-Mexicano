#!/usr/bin/env python3
"""Juicios humanos -> tablas/report. Controla denominador, sello, veto y cobertura.
Defectos observados: precio confundido con voluntad, resiliencia con metas,
porcentajes de bases distintas y adopción confundida con corroboración (#1184).
No mide datos ni asigna un dictamen por línea, palabra o rango.
"""
import argparse,collections,csv,hashlib,io,json,re,copy
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parents[4]
NAME='Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md'
REPORT='corpus/reports-v2/'+NAME
ORIGINAL='corpus/reports/'+NAME
MAP='canon/mapa-dominios-v1_1.tsv'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def rows(p):
 with p.open() as f:return list(csv.DictReader(f,delimiter='\t'))
PICKS=[
('CALC-ENIF-0001','RESULT-ENIF-AHO-B-P-FORMAL-P','Ahorra por alguna vía formal','RESULT-ENIF-AHO-B-P-FORMAL'),
('CALC-ENIF-0001','RESULT-ENIF-AHO-B-P-INFORMAL-P','Ahorra por alguna vía informal','RESULT-ENIF-AHO-B-P-INFORMAL'),
('CALC-ENIF-0001','RESULT-ENIF-AHO-A-P-CORTO-CON-P','Resiliencia corta con seguridad laboral','RESULT-ENIF-AHO-A-P-CORTO-CON'),
('CALC-ENIF-0001','RESULT-ENIF-AHO-A-P-CORTO-SIN-P','Resiliencia corta sin seguridad laboral','RESULT-ENIF-AHO-A-P-CORTO-SIN'),
('CALC-ENIF-0001','RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P','Razón desconfianza/mal servicio; conoce protección','RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE'),
('CALC-ENIF-0001','RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P','Razón desconfianza/mal servicio; no conoce protección','RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE'),
('CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1','RESULT-HVD-A-AMBAS-VIAS','Ahorra por ambas vías',None),
('CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1','RESULT-HVD-A-SOLO-FORMAL','Ahorra solo formal',None),
('CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1','RESULT-HVD-A-SOLO-INFORMAL','Ahorra solo informal',None),
('CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1','RESULT-HVD-A-NO-AHORRA','No declara ahorro por esas vías',None)]
def evidence(cat=None):
 cat=cat if cat is not None else rows(R/'canon/catalogo-del-mexicano-v1_2.tsv')
 decisions=rows(R/'data/corrida0/decisiones.tsv')
 out=[]
 for calc,rid,label,prefix in PICKS:
  d=R/'data/corrida0'/calc;s=obj(d/'sello.json');v=obj(d/'resultados.json')['resultados']
  for file in ['spec.yaml','resultados.json']:assert sha(d/file)==s[file],f'sello incompatible {calc}/{file}'
  c=[x for x in cat if x['calc']==calc and x['result_id']==rid];assert len(c)==1,'identidad catálogo ausente/ambigua'
  c=c[0];assert c['estado_adopcion'].startswith('ADOPTADO') and not 'VET' in (c['estado_adopcion']+c['reserva']).upper(),'vetado/no adoptado'
  ds=[x for x in decisions if x['objeto']==calc];assert ds and any('cuenta_gen2=SI' in x['decision'] for x in ds),'sin cuenta_gen2'
  x=dict(calc=calc,result=rid,etiqueta=label,punto=v[rid],unidad='proporción ponderada de persona elegida 18+',ola='ENIF2024',temporalidad='RETROSPECTIVA',adopcion=c['estado_adopcion'],firma=c['firma_fp'],reserva=c['reserva'],oferta_exclusion=c['oferta_exclusion'],resultados_sha256=s['resultados.json'],sello_sha256=sha(d/'sello.json'),spec_sha256=s['spec.yaml'],fuente_adopcion=ds,linaje=['CALC-ENIF-0001'] if prefix is None else [calc])
  if prefix:
   x.update(denominador=v[prefix+'-DENOMINADOR'],ic_lo=v[prefix+'-IC-LO'],ic_hi=v[prefix+'-IC-HI'],n=v[prefix+'-N-DENOMINADOR'],metodo_ic=v[prefix+'-METODO-IC'])
  else:x.update(denominador='todas las personas 18+ con FAC_PER válido; mismo universo que familia B CALC-ENIF-0001',ic_lo=None,ic_hi=None,n=None,metodo_ic='derivado determinista; no emitir IC nuevo')
  assert x['denominador'];assert abs(float(c['punto'])-x['punto'])<1e-9,'vista atrasada: dictaminar contra sello'
  out.append(x)
 assert abs(sum(x['punto'] for x in out[6:])-1)<1e-10,'partición inválida'
 assert out[0]['denominador']==out[1]['denominador'],'vías con bases distintas'
 assert out[4]['denominador']!=out[5]['denominador'],'razones con bases confundidas'
 return out

def validate(ds,text):
 ms=rows(R/MAP);ms=[x for x in ms if x['report']==ORIGINAL]
 assert {x['id_afirmacion'] for x in ms}=={x['mapa_id'] for x in ds if x['mapa_id']},'mapa incompleto'
 assert len({x['id'] for x in ds})==len(ds),'duplicado'
 for x in ds:
  assert x['dictamen'] in ['CONFIRMA','MATIZA','ROMPE','SIN-CIFRA']
  assert all(x[k] for k in ['razon','evidencia','falsador','unidad','localizador'])
  assert x['revision_manual'] is True
  if x['dictamen']=='SIN-CIFRA':assert x['razon_sin_cifra'] in ['adquisición pendiente','falta de ejecución','instrumento inadecuado','no comparabilidad','restricción del proyecto','imposibilidad justificada']
 # solo tabla trazada puede contener porcentajes propios; otras cantidades deben ser declaradas externas.
 for line in text.splitlines():
  if re.search(r'\d[\d.,]*\s*%',line):assert '| RESULT-' in line,'afirmación cuantitativa sin traza'
 assert '{{' not in text,'placeholder pendiente'
 for title in ['Resumen ejecutivo','Marco conceptual','Mapa de evidencia','Patrones principales','Causas:','Segmentación explícita','Comparación internacional','Implicaciones aplicadas','Mitos','Síntesis','Módulo de auditoría']:assert title in text
 return len(ms)

def build():
 ds=obj(B/'decisiones.json');es=evidence();ss=obj(B/'fuentes.json');f=ss[1]
 lines=['| Conducta | Valor / IC | Denominador y n | Objeto | Estado |','|---|---|---|---|---|']
 for x in es:
  val=f"{100*x['punto']:.2f}%";ci=f"; IC95 [{100*x['ic_lo']:.2f}, {100*x['ic_hi']:.2f}]%" if x['ic_lo'] is not None else '; sin IC propio'
  lines.append(f"| {x['etiqueta']} | {val}{ci} | {x['denominador']}; n={x['n'] if x['n'] is not None else 'ver padre'} | {x['result']} · `{x['calc']}` | {x['adopcion']}; RETROSPECTIVA |")
 used={z for x in es for z in [x['calc'],x['result'],*x['linaje']]}
 used.update(['CORR-0009','CORR-0015','RES-0046','RES-0048','RES-0057','RES-0058','RES-0059','RES-0060','RES-0053','RES-0054','RES-0055','RES-0056'])
 path=R/'forense/validacion-independiente/catalogo-1-ejecucion-lote1/efectos-discrepancias.tsv'
 cr=rows(path);affected=[x for x in cr if any(z in str(x) for z in used)]
 assert not affected,'#1184 intersecta objetos usados: dictaminar efecto antes de publicar'
 # CALC->RESULT/tabla/alias: todas las columnas de efectos, y comparación con catálogo vigente.
 dep=dict(pr=1184,archivo=str(path.relative_to(R)),sha256=sha(path),universo_examinado=len(cr),calcs_uso=sorted({x['calc'] for x in es}),linaje_examinado=sorted(used),intersecciones=affected,conclusion='No hay intersección de estas llaves, CALC ni padre ENIF en efectos del lote ENDIREH. No acredita validación independiente de ENIF. Mantener adopción separada de validez y precisión; no retirar por extrapolación del diagnóstico.')
 cnt=dict(collections.Counter(x['dictamen'] for x in ds))
 txt=(B/'editorial.md').read_text().replace('{{CIFRAS}}','\n'.join(lines)).replace('{{EXTERNA}}',f"FEMSA declara {f['valor']} {f['unidad']} en 3T2025. Fuente externa `FEMSA`; cantidad tomada del comunicado, sin equivalencia a prevalencia nacional.")
 txt=txt.replace('{{COBERTURA}}',f"Cobertura derivada: {len(ds)} decisiones explícitas, {len([x for x in ds if x['mapa_id']])} filas del mapa y {len([x for x in ds if not x['mapa_id']])} afirmaciones adicionales o cláusulas separadas. Conteos: "+', '.join(f'{k}={v}' for k,v in sorted(cnt.items()))+'. Tabla local: `afirmaciones.tsv`; juicio fuente: `decisiones.json`. Los rótulos de medibilidad del mapa no se usaron como veredictos editoriales.')
 txt=txt.replace('{{DEPENDENCIAS}}','Dependencia #1184 comprobada por identidad, CALC y linaje: '+dep['conclusion']+' `dependencia-1184.json` conserva llaves, archivo y hash del cotejo. Veto/adopción se comprueba en catálogo y decisiones por objeto al regenerar; ningún valor vetado se usa como piso. La ausencia de precisión independiente puede cambiar un uso futuro: no se fija tolerancia ni parámetro predictivo con estas cifras.')
 n=validate(ds,txt)
 buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=list(ds[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(ds)
 cmd=['python3',str((B/'producir.py').relative_to(R))]
 summary=dict(report=REPORT,mapa_filas=n,afirmaciones=len(ds),dictamenes=cnt,cifras=len(es)+1,comando_generar=cmd,comando_verificar=cmd+['--check'],comando_self_test=cmd+['--self-test'])
 artifacts={B/'afirmaciones.tsv':buf.getvalue(),R/REPORT:txt,B/'cifras.json':json.dumps(es,ensure_ascii=False,indent=2)+'\n',B/'dependencia-1184.json':json.dumps(dep,ensure_ascii=False,indent=2)+'\n',B/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n',B/'manifest.json':json.dumps(dict(corte='11602de8e375c10b90807d1b74e088f6b9e99c8b',original_sha256=sha(R/ORIGINAL),mapa_sha256=sha(R/MAP),decisiones_sha256=sha(B/'decisiones.json'),fuentes_sha256=sha(B/'fuentes.json'),catalogo_sha256=sha(R/'canon/catalogo-del-mexicano-v1_2.tsv')),indent=2)+'\n'}
 return artifacts,summary,ds,txt

def self_test(ds,txt):
 trials=[]
 bad=copy.deepcopy(ds);bad.pop(0);trials.append(('fila mapa omitida',lambda:validate(bad,txt)))
 bad2=copy.deepcopy(ds);bad2[0]['razon']='';trials.append(('razón vacía',lambda:validate(bad2,txt)))
 trials.append(('porcentaje sin trazabilidad',lambda:validate(ds,txt+'\nAdopción 99%.\n')))
 cat=rows(R/'canon/catalogo-del-mexicano-v1_2.tsv');hit=next(x for x in cat if x['result_id']==PICKS[0][1]);hit['estado_adopcion']='VETADO';trials.append(('veto',lambda:evidence(cat)))
 for label,fn in trials:
  try:fn()
  except AssertionError:continue
  raise AssertionError('mutación no detectada: '+label)
 return [x[0] for x in trials]

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();files,s,ds,t=build()
 if a.self_test:print(json.dumps({'self_test':'PASS','mutaciones':self_test(ds,t)},ensure_ascii=False));return
 for path,content in files.items():
  if a.check:assert path.exists() and path.read_text()==content,f'derivado obsoleto {path}'
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
 print(json.dumps(dict(estado='VERIFICADO' if a.check else 'GENERADO',**s),ensure_ascii=False))
if __name__=='__main__':main()
