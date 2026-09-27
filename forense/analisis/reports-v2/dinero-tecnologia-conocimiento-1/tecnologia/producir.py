#!/usr/bin/env python3
"""Produce y comprueba Tecnología desde decisiones explícitas; no dicta veredictos.

Atrapa defectos materiales observados: denominador no usuarios/total,
TLOC confundido con urbano/rural, tabla o cifra sin firma/traza, párrafo
fuera de cobertura, agregado fintech usado como refutación de aceptación IA.
No lee microdatos, corre medidores ni modifica derivados o sellos.
"""
import argparse, collections, copy, csv, hashlib, io, json, re
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[4]
ORIGINAL=ROOT/'corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md'
REPORT=ROOT/'corpus/reports-v2'/ORIGINAL.name
CALC='CALC-ENDUTIH-PISOS-2024-0001'
RID='RESULT-ENDUTIH-PISOS-2024-TABLA'
FP='FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01'
SELECTION={'INTERNET':('TOTAL',46),'HOMBRE':('SEXO_1',40),'MUJER':('SEXO_2',41)}
DEN={k:'persona elegida 6+; P7_1 válido 1/2, FAC_PER>0, EST_DIS/UPM_DIS presentes; últimos tres meses; '+v[0] for k,v in SELECTION.items()}
REASONS={'adquisición pendiente','falta de ejecución','instrumento inadecuado','no comparabilidad','restricción del proyecto','imposibilidad justificada'}
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text())
def enc(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def validate_claims(d):
    a=d['afirmaciones'];assert len({x['id'] for x in a})==len(a)
    for x in a:
        assert x['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}
        assert all(x.get(k) for k in ['afirmacion','razon','evidencia','localizador'])
        if x['dictamen']=='SIN-CIFRA':assert x['evidencia'] in REASONS
        if x['dictamen']=='ROMPE':assert x['id'] in {'ASTRA5-U0-TEC-002','ASTRA5-U0-TEC-042','TEC-038-CONTRAFACTUAL','TEC-X21','TEC-X30','TEC-X31','TEC-X42'}
    return a

def decisions():
    d=load(BASE/'decisiones.json');assert d['original_sha256']==sha(ORIGINAL.read_bytes())
    a=validate_claims(d)
    with (ROOT/'canon/mapa-dominios-v1_1.tsv').open() as f:
        m=[r for r in csv.DictReader(f,delimiter='\t') if r['report']==str(ORIGINAL.relative_to(ROOT))]
    assert {r['id_afirmacion'] for r in m}=={r['mapa_id'] for r in a if r['mapa_id']},'mapa incompleto'
    assert all(r['report_sha256']==d['original_sha256'] for r in m)
    lines=ORIGINAL.read_text().splitlines();cov=load(BASE/'correspondencias.json')
    material={str(i) for i,t in enumerate(lines,1) if t and not t.startswith('#')}
    assert set(cov)==material,'párrafo omitido o ajeno'
    ids={r['id'] for r in a}
    assert all(set(v)<=ids for v in cov.values())
    # Párrafos sin juicio deben ser rótulos sin tesis: lista editorial explícita.
    labels={11,61,70,76,80,135,144,148,153,161,168}
    assert {int(k) for k,v in cov.items() if not v}==labels
    cs=[{'linea':int(k),'sha256':sha(lines[int(k)-1].encode()),'decisiones':v,'clase':'rótulo sin tesis' if not v else 'correspondencia editorial; repeticiones no se cuentan como tesis nuevas'} for k,v in cov.items()]
    return d,a,m,cs

def evidence():
    folder=ROOT/'data/corrida0'/CALC;s=load(folder/'sello.json')
    for name in ['resultados.json','spec.yaml']:
        assert sha((folder/name).read_bytes())==s[name],'objeto sellado cambió'
    raw=json.loads(load(folder/'resultados.json')['resultados'][RID])['celdas']
    with (ROOT/'forense/firmas-pendientes.tsv').open() as f:
        fp=[r for r in csv.DictReader(f,delimiter='\t') if r['id']==FP]
    assert len(fp)==1 and fp[0]['estado']=='FIRMADA','firma no vigente'
    with (ROOT/'canon/catalogo-del-mexicano-v1_2.tsv').open() as f:
        cat={r['llave']:r for r in csv.DictReader(f,delimiter='\t') if r['calc']==CALC}
    out=[]
    for key,(domain,idx) in SELECTION.items():
        x=raw[idx];identity=RID+'#'+str(idx);c=cat[identity]
        assert x['dominio']==domain and x['medida']=='internet' and x['estado']=='ESTIMABLE'
        assert c['estado_adopcion']=='ADOPTADO' and c['firma_fp']==FP and c['conducta']=='internet' and c['segmento']==domain
        assert float(c['punto'])==x['punto'],'vista/objeto discrepante'
        out.append(dict(id=key,calc=CALC,result=RID,llave=identity,selector={'medida':'internet','dominio':domain},denominador=DEN[key],punto=x['punto']*100,ic95=[v*100 for v in x['ic95']],n=x['n'],unidad='porcentaje ponderado de personas; n sin ponderar',ola='2024',temporalidad='RETROSPECTIVA',adopcion='ADOPTADO piso descriptivo; no validación independiente ni predicción',firma=FP,resultados_sha256=s['resultados.json'],sello_sha256=sha((folder/'sello.json').read_bytes()),firma_sha256=sha(enc(fp[0]).encode()),veto='No consume actividad_empleo original excluida; no nuevos usos'))
    ext=load(BASE/'cifras-externas.json')
    out.extend(ext);validate_evidence(out)
    return out

def validate_evidence(es):
    assert len(es)==9 and len({x['id'] for x in es})==9
    for x in es:
        assert x['temporalidad']=='RETROSPECTIVA' and x['denominador']
        if x['id'] in DEN:assert x['denominador']==DEN[x['id']] and x['result']==RID
        else:assert x['fuente']=='INEGI2025' and x['pdf_sha256']==load(BASE/'manifest.json')['pdf_sha256']
    e={x['id']:x for x in es};assert e['EXT_NOSABE']['denominador']=='personas 6+ total','denominador motivo alterado'
    assert e['EXT_NOUSO']['denominador']=='personas 6+ total'
    assert e['EXT_HOG_ALTO']['denominador']=='hogares por entidad'

def dependency():
    # #1184: solo metadata publicada de dictamen y resumen; no reconstrucciones ciegas.
    p=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
    summary=load(p/'resumen-lote1.json')
    with (p/'dictamenes-publicabilidad.tsv').open() as f:r=list(csv.DictReader(f,delimiter='\t'))
    needles=[CALC,RID,'endutih-pisos-2024-0001','ENDUTIH','FP-260923-ASTRA5-U4-TECNOLOGIA']
    intersects=[x for x in r if any(n.lower() in str(x).lower() for n in needles)]
    packs=[x['paquete'] for x in summary['paquetes']]
    assert not intersects and not any('endutih' in x.lower() for x in packs),'hallazgo #1184 intersecta: requiere revisión'
    return dict(pr=1184,fuentes=[str((p/'dictamenes-publicabilidad.tsv').relative_to(ROOT)),str((p/'resumen-lote1.json').relative_to(ROOT))],dictamen_sha256=sha((p/'dictamenes-publicabilidad.tsv').read_bytes()),paquetes=packs,llaves_alias_linaje=needles,interseccion=[],reserva='No intersección en lote #1184 examinado. ENDUTIH no queda validada independientemente por ausencia de hallazgo. Adopción, integridad y precisión no se colapsan.')

def validate_template(t):
    assert not re.search(r'\b\d+(?:[.,]\d+)?\s*%|\b\d+(?:[.,]\d+)?\s+(?:millones|USD|pesos)\b',t),'cantidad material sin token'
    assert '## Auditoría de rigor extremo' in t and '## Síntesis' in t
    parts=re.split(r'(?m)^## .+$',t)
    assert all(p.strip() for p in parts),'apartado vacío'

def build():
    manifest=load(BASE/'manifest.json')
    for name,digest in manifest['insumos_editoriales'].items():assert sha((BASE/name).read_bytes())==digest,'insumo editorial cambió sin revisión: '+name
    d,a,m,cov=decisions();es=evidence();dep=dependency();t=(BASE/'editorial.md').read_text();validate_template(t)
    t=t.replace('{{CORTE}}',d['corte'])
    for e in es:
        if 'result' in e:
            fmt=f"{e['punto']:.3f}% [IC95 de diseño {e['ic95'][0]:.3f}–{e['ic95'][1]:.3f}], n={e['n']:,}; `{e['llave']}` / `{CALC}`, {FP} FIRMADA, ADOPTADO RETROSPECTIVO"
        else:fmt=f"{e['punto']:.1f}% [EXTERNA {e['fuente']}, {e['localizador']}; {e['denominador']}; no RESULT]"
        t=t.replace('{{'+e['id']+'}}',fmt)
    sources=load(BASE/'fuentes.json')
    t=t.replace('{{FUENTES}}','\n\n'.join(f"- [{s['id']}]({s['url']}) · {s['tier']} · publicación {s['fecha_publicacion']}; lectura {s['fecha_lectura']}; {s['localizador']}. {s['leido']}. Límite: {s['alcance']}." for s in sources))
    assert '{{' not in t
    fields=['id','mapa_id','localizador','afirmacion','dictamen','evidencia','razon'];buf=io.StringIO();w=csv.DictWriter(buf,fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(a)
    cmd=str((BASE/'producir.py').relative_to(ROOT))
    summary=dict(report=str(REPORT.relative_to(ROOT)),mapa_filas=len(m),afirmaciones=len(a),dictamenes=dict(collections.Counter(x['dictamen'] for x in a)),cifras=len(es),original_parrafos=len(cov),rotulos_sin_tesis=sum(not x['decisiones'] for x in cov),registros_sin_mapa_id=sum(not x['mapa_id'] for x in a),extras_editoriales=sum(x['id'].startswith('TEC-X') for x in a),clausulas_separadas=sum(not x['mapa_id'] and not x['id'].startswith('TEC-X') for x in a),unidad_conteo='Registros editoriales; mapa compuesto, cláusulas y correspondencias pueden solaparse. No se anuncian como tesis únicas.',comando_generar=['python3',cmd],comando_verificar=['python3',cmd,'--check'],comando_self_test=['python3',cmd,'--self-test'])
    return {REPORT:t,BASE/'afirmaciones.tsv':buf.getvalue(),BASE/'coverage.json':enc(cov),BASE/'cifras.json':enc(es),BASE/'dependencia-1184.json':enc(dep),BASE/'resumen.json':enc(summary)}

def self_test():
    d=load(BASE/'decisiones.json');bad=copy.deepcopy(d);bad['afirmaciones'][0]['dictamen']='CONFIRMA-POR-RANGO'
    try:validate_claims(bad)
    except AssertionError:pass
    else:raise AssertionError('aceptó juicio automático')
    e=evidence();bad=copy.deepcopy(e);next(x for x in bad if x['id']=='EXT_NOSABE')['denominador']='solo no usuarios'
    try:validate_evidence(bad)
    except AssertionError:pass
    else:raise AssertionError('aceptó denominador errado')
    try:validate_template((BASE/'editorial.md').read_text()+'\nAdopción 99%.')
    except AssertionError:pass
    else:raise AssertionError('aceptó cifra sin traza')
    # Regla del producto: los registros vetados de empleo no aparecen en evidencia.
    assert all(x.get('selector',{}).get('medida')!='actividad_empleo' for x in e)
    print('SELF-TEST VERDE: dictamen inválido, denominador alterado, cantidad sin traza rechazados; veto empleo respetado')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:self_test();return
    products=build()
    for path,text in products.items():
        if a.check:assert path.exists() and path.read_text()==text,'derivado propio desactualizado: '+str(path)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    print('VERDE: cobertura original/mapa, decisiones explícitas, trazabilidad, denominadores, adopción, vetos, #1184; '+('CHECK' if a.check else 'GENERADO'))
if __name__=='__main__':main()
