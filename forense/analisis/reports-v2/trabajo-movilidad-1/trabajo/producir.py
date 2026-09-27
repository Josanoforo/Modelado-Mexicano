#!/usr/bin/env python3
"""Regenera/valida solo Trabajo: juicio en decisiones.json, prosa en editorial.md.

Protege defectos observados: agregado global trasladado a México, contrato
confundido con informalidad y cifra sin denominador. No mide microdato,
no convierte medibilidad del mapa en dictamen ni concede recibos humanos.
"""
import argparse
import collections
import copy
import csv
import hashlib
import io
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
REPORT = ROOT / 'corpus/reports-v2/Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md'
MAP = ROOT / 'canon/mapa-dominios-v1_1.tsv'
ORIGINAL = ROOT / 'corpus/reports/Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md'
PISO = 'CALC-ENOE-PISOS-0003'
PART = 'CALC-ENOE-PARTICIPACION-2024T4-0001'
FP_PISO = 'FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01'
FP_PART = 'FP-260926-GEN2-COLA-COMPLETA-1-0d4a-01'
RID = 'RESULT-ENOE-PISOS-TABLA'
PREFIX = 'RESULT-ENOE-PARTICIPACION-2024T4-PARTICIPA-ECONOMICAMENTE-2024T4-SEXO-'
CONTRACTS = {
    'INFORMAL': ('empleo_informal', 'ocupados EMP_PPAL válido; persona 15–98 elegible SDEM'),
    'CONTRATO': ('sin_contrato_escrito', 'subordinados REMUNE2C válido y TIP_CON 1–5; persona 15–98 elegible SDEM'),
    'JORNADA': ('jornada_mas_50_horas', 'ocupados HRSOCUP 1–168 válido; persona 15–98 elegible SDEM'),
    'MUJER': ('MUJER', 'mujeres 15+ residentes habituales/nuevas con entrevista completa y diseño válido; clase1 válido'),
    'HOMBRE': ('HOMBRE', 'hombres 15+ residentes habituales/nuevos con entrevista completa y diseño válido; clase1 válido'),
}
# Correspondencias editoriales explícitas por párrafo del original, no reglas de dictamen por línea.
PARAGRAPHS = {
 3:['ENOE-002','TRAB-001','TRAB-002','TRAB-003','X01','X28'],5:['X02'],
 11:['TRAB-004'],13:['TRAB-005'],15:['TRAB-006','X03','X29'],17:['TRAB-007'],
 25:['TRAB-008'],27:['TRAB-008','TRAB-009','TRAB-010','X04','X30'],29:['TRAB-011','TRAB-047'],
 33:['TRAB-012'],35:['TRAB-013','TRAB-038','X05'],37:['TRAB-014','X03','X06'],
 41:['TRAB-015'],43:['TRAB-015'],45:['X07'],49:['TRAB-016'],51:['X08'],53:['X09'],
 57:['TRAB-003','TRAB-017','TRAB-018'],59:['ENOE-003','TRAB-019','X10','X11'],
 67:['TRAB-020','TRAB-021'],71:['TRAB-022','TRAB-023','X12'],
 75:['TRAB-024','TRAB-025','TRAB-026','TRAB-027','TRAB-028','X13','X14'],
 79:['TRAB-029','TRAB-030','TRAB-031','TRAB-032','X15','X31'],
 85:['TRAB-033','X16'],87:['TRAB-033','X16'],89:['X16'],91:['TRAB-033','X16'],
 99:['TRAB-034','TRAB-035'],103:['TRAB-036','TRAB-037','X17'],
 107:['TRAB-038','TRAB-039','TRAB-040','X18'],111:['TRAB-041','TRAB-042','X19'],
 115:['TRAB-043','TRAB-044','TRAB-045','TRAB-046','X20'],
 121:['TRAB-001','TRAB-046','X21'],123:['TRAB-047'],125:['TRAB-015','X22'],
 127:['TRAB-048'],129:['TRAB-049','X27'],131:['TRAB-041','X23'],133:['X24'],135:['TRAB-050'],137:['X25'],
 143:['TRAB-051'],145:['TRAB-051'],146:['TRAB-051'],147:['TRAB-051'],
 153:['TRAB-052','X26'],155:['TRAB-003','TRAB-001','TRAB-017','TRAB-046','X10','X26'],
 157:['TRAB-053','X26'],159:['TRAB-054','X26'],161:['TRAB-055','X26'],
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(p):
    return json.loads(p.read_text())

def encoded(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'

def seal(calc):
    d = ROOT / 'data/corrida0' / calc
    s = load(d / 'sello.json')
    assert sha((d/'resultados.json').read_bytes()) == s['resultados.json'], 'sello resultados incompatible'
    assert sha((d/'spec.yaml').read_bytes()) == s['spec.yaml'], 'sello spec incompatible'
    return load(d/'resultados.json')['resultados'], s['resultados.json'], sha((d/'sello.json').read_bytes())

def firmas():
    with (ROOT/'forense/firmas-pendientes.tsv').open() as f:
        rows={r['id']:r for r in csv.DictReader(f, delimiter='\t') if r['id'] in (FP_PISO,FP_PART)}
    assert rows[FP_PISO]['estado']=='FIRMADA', 'piso no adoptado: revisar conclusión'
    assert rows[FP_PART]['estado']=='ABIERTA', 'estado participación cambió: revisar editorial'
    return rows

def evidence():
    assert sha((BASE/'fuentes.json').read_bytes()) == 'b96543506677989e2cb8cd206d890e87dc3421b154c395b554743dce91292803', 'fuente externa cambió: revisión de país/denominador requerida'
    r,h,s=seal(PISO);tab=json.loads(r[RID]);a,ah,aseal=seal(PART)
    f=firmas();out=[]
    for key in ['INFORMAL','CONTRATO','JORNADA']:
        conducta,den=CONTRACTS[key]
        row=[x for x in tab if x['ola']=='2024T3' and x['conducta']==conducta and x['eje']=='nacional' and x['segmento']=='NAC']
        assert len(row)==1
        x=row[0]
        out.append(dict(id=key,calc=PISO,result=RID,selector={'ola':'2024T3','conducta':conducta,'eje':'nacional','segmento':'NAC'},
                        denominador=den,unidad='proporción ponderada de personas; n sin ponderar',ola='2024T3',
                        punto=x['punto'],ic95_lo=x['ic95_lo'],ic95_hi=x['ic95_hi'],n=x['n'],
                        resultados_sha256=h,sello_sha256=s,adopcion='FIRMADA; piso descriptivo retrospectivo',firma=FP_PISO,firma_sha256=sha(encoded(f[FP_PISO]).encode()),marca='RETROSPECTIVA'))
    for key in ['MUJER','HOMBRE']:
        sex,den=CONTRACTS[key];rid=PREFIX+sex
        out.append(dict(id=key,calc=PART,result=rid+'-P',result_ic_lo=rid+'-IC-LO',result_ic_hi=rid+'-IC-HI',result_n=rid+'-N',
                        selector={'ola':'2024T4','conducta':'participa_economicamente','eje':'sexo','segmento':sex},denominador=den,
                        unidad='proporción ponderada de personas; n sin ponderar',ola='2024T4',punto=a[rid+'-P'],ic95_lo=a[rid+'-IC-LO'],ic95_hi=a[rid+'-IC-HI'],n=a[rid+'-N'],
                        resultados_sha256=ah,sello_sha256=aseal,adopcion='PROVISIONAL NO ADOPTADA; firma ABIERTA',firma=FP_PART,firma_sha256=sha(encoded(f[FP_PART]).encode()),marca='RETROSPECTIVA'))
    source=load(BASE/'fuentes.json')[0]
    assert source['id']=='RAND2025' and source['url'].startswith('https://www.randstad.com.mx/')
    assert source['salario']>source['balance'], 'ROMPE requiere orden contrario para México'
    for key,field in [('RAND_SALARIO','salario'),('RAND_BALANCE','balance')]:
        out.append(dict(id=key,fuente=source['id'],url=source['url'],localizador=source['localizador'],fecha=source['fecha_publicacion'],
                        denominador=source['denominador'],unidad='porcentaje de respuestas importancia; factores no excluyentes',punto=source[field],
                        adopcion='EXTERNA, no RESULT, muestra privada no representatividad nacional acreditada',hash_archivo_leido=source['hash_archivo_leido'],marca='RETROSPECTIVA'))
    return out

def validate_evidence(es):
    assert len(es)==7 and len({x['id'] for x in es})==7
    for e in es:
        if e['id'] in CONTRACTS:
            assert e['denominador']==CONTRACTS[e['id']][1], 'denominador incompatible'
            assert e['result'] and e['calc'], 'cantidad sin RESULT'
            assert e['marca']=='RETROSPECTIVA'
        else:
            assert e['fuente']=='RAND2025' and 'México' in e['denominador'], 'cantidad externa sin país/denominador'

def validate_template(t):
    # Años, ids, número de norma y umbral verbal del estimando no son prevalencias.
    assert not re.search(r'\b\d+(?:[.,]\d+)?\s*%|\b\d+(?:[.,]\d+)?\s+(?:millones|horas|pesos|dólares)\b',t), 'cantidad material literal sin evidencia/token'

def decisions_and_coverage():
    d=load(BASE/'decisiones.json');rs=d['afirmaciones']
    assert d['original_sha256']==sha(ORIGINAL.read_bytes()), 'original cambió, revisión material requerida'
    with MAP.open() as f:
        mapa={r['id_afirmacion']:r for r in csv.DictReader(f,delimiter='\t') if r['report']==str(ORIGINAL.relative_to(ROOT))}
    assert {r['mapa_id'] for r in rs if r['mapa_id']}==set(mapa), 'cobertura mapa faltante/ajena'
    assert all(r['report_sha256']==d['original_sha256'] for r in mapa.values()), 'mapa corresponde a otro original'
    assert len({r['id'] for r in rs})==len(rs)
    for r in rs:
        assert r['dictamen'] in ('CONFIRMA','MATIZA','ROMPE','SIN-CIFRA') and r['razon'] and r['evidencia']
        if r['dictamen']=='ROMPE':
            assert r['evidencia']=='RAND2025' and r['id'] in ('ASTRA5-U0-TRAB-023','ASTRA5-U0-TRAB-053-C2'), 'ROMPE sin contradicción primaria'
        if r['dictamen']=='SIN-CIFRA':assert r['evidencia'] in ('adquisición pendiente','falta de ejecución','instrumento inadecuado','no comparabilidad','restricción del proyecto','imposibilidad justificada'), 'SIN-CIFRA sin razón diferenciada'
    lines=ORIGINAL.read_text().splitlines()
    material={i for i,t in enumerate(lines,1) if t and not t.startswith(('#','---'))}
    assert material==set(PARAGRAPHS), 'párrafo material fuera de cobertura'
    coverage=[]
    for i,shorts in PARAGRAPHS.items():
        ids=[]
        for short in shorts:
            prefix=('TRABAJO-'+short) if short.startswith('X') else 'ASTRA5-U0-'+short
            found=[r['id'] for r in rs if r['id']==prefix or r['id'].startswith(prefix+'-')]
            assert found, 'correspondencia editorial ausente'
            ids.extend(found)
        coverage.append(dict(parrafo_original='L'+str(i),sha256=sha(lines[i-1].encode()),decisiones=list(dict.fromkeys(ids)),tipo='correspondencia; no tesis adicional'))
    return d,rs,mapa,coverage

def proposals():
    return [
      dict(id='TRABAJO-R1',estado='PROPUESTO-POR-EJECUTOR',si='analista compara contrato e informalidad',entonces='mantener cantidades y denominadores separados',porque='subordinados elegibles no equivalen a todos los ocupados',tier_frecuencia='(a) ENOE nacional retrospectiva adoptada',tier_mecanismo='regla de medición, no efecto psicológico',consumidor='lector de reports/analista laboral',aplicabilidad='mismas definiciones, ola y población del registro',falsador='un contrato armonizado que defina exactamente el mismo universo y variable para ambas categorías',si_no_refuta='alcance conservado, no causalidad acreditada',limite='no determina preferencias'),
      dict(id='TRABAJO-R2',estado='PROPUESTO-POR-EJECUTOR',si='se interpreta participación por sexo',entonces='describir cuidado, horarios y oferta antes de atribuir preferencia',porque='participación no identifica motivo',tier_frecuencia='(a) ENOE 2024T4 PROVISIONAL NO ADOPTADA',tier_mecanismo='no identificado',consumidor='analista/planificación de empleos',aplicabilidad='población 15+ y disponibilidad real',falsador='diseño que varíe oportunidad y mida preferencias en la misma persona separando alternativas',si_no_refuta='mecanismo sigue indeterminado',limite='no fija cuánto corresponde a cada causa'),
      dict(id='TRABAJO-R3',estado='PROPUESTO-POR-EJECUTOR',si='centro reporta horas largas y baja autonomía',entonces='evaluar cargas, control y organización del trabajo antes de diagnosticar personalidad',porque='son categorías de riesgo distintas de diagnóstico',tier_frecuencia='(a) ENOE nacional; norma primaria sin prevalencia',tier_mecanismo='propuesta evaluable; efecto no identificado',consumidor='responsable del centro/analista de organización',aplicabilidad='solo con medición pertinente dentro del centro',falsador='comparación que cambie carga/control y mida exposición y resultados sin cambios atribuibles, con precisión suficiente',si_no_refuta='acotada al centro; falsador débil si precisión insuficiente',limite='no diagnostica salud ni promete reducción causal de burnout')]

def render():
    d,rs,mapa,coverage=decisions_and_coverage();es=evidence();validate_evidence(es)
    template=(BASE/'editorial.md').read_text();validate_template(template)
    values={'CORTE':d['corte']}
    for e in es:
        if e['id'] in CONTRACTS:
            for field,suffix in [('punto','P'),('ic95_lo','LO'),('ic95_hi','HI')]:values[e['id']+'_'+suffix]=f'{e[field]*100:.2f}'
        else:values[e['id']]=str(e['punto'])
    table=['|Cantidad / unidad|Ola y denominador|Estado / fuente|','|---|---|---|']
    for e in es:
        if e['id'] in CONTRACTS:
            measure=f"{e['punto']*100:.2f}% (IC95 {e['ic95_lo']*100:.2f}–{e['ic95_hi']*100:.2f}%; n={e['n']})"
            src=f"`{e['result']}`; `{e['calc']}`"
        else:measure=f"{e['punto']}%";src=f"[{e['fuente']}]({e['url']})"
        table.append(f"|{e['id']}: {measure}|{e.get('ola',e.get('fecha'))}; {e['denominador']}|{e['adopcion']}; {src}|")
    values['TABLA_CIFRAS']='\n'.join(table)
    rules=proposals()
    values['REGLAS']='\n\n'.join(f"**{r['id']} · {r['estado']}**. SI {r['si']}, ENTONCES {r['entonces']}, PORQUE {r['porque']}. Consumidor: {r['consumidor']}. Aplicabilidad: {r['aplicabilidad']}. Frecuencia: {r['tier_frecuencia']}; mecanismo: {r['tier_mecanismo']}. Falsador: {r['falsador']}. Si no refuta: {r['si_no_refuta']}. Límite: {r['limite']}." for r in rules)
    counts={'filas_mapa':len(mapa),'registros_editoriales':len(rs),'tesis_distintas':len({r['tesis_id'] for r in rs if r['tesis_id']}),'parrafos_originales_cubiertos':len(coverage),'registros_meta_excluidos_tesis':sum(not r['tesis_id'] for r in rs),'repeticiones_semanticas':sum(bool(r['tesis_id']) for r in rs)-len({r['tesis_id'] for r in rs if r['tesis_id']}),'cantidades_trazadas':len(es),'reglas_propuestas':len(rules),'por_dictamen_registros':dict(collections.Counter(r['dictamen'] for r in rs))}
    values['CIERRE']=f"Regeneración y verificación: `python3 {Path(__file__).relative_to(ROOT)} --verificar --autoprueba`. Tabla: [afirmaciones.tsv](../../forense/analisis/reports-v2/trabajo-movilidad-1/trabajo/afirmaciones.tsv); decisiones/fuentes/cifras/coverage.json contienen contratos y exclusiones. Conteos derivados: {encoded(counts).strip()}. Cobertura de párrafos es un control de integridad, no conteo de tesis únicas. Cero revisiones humanas concedidas; recibo solicitado por integración."
    def replacement(m):
        assert m[1] in values,'token sin fuente '+m[1]
        return values[m[1]]
    text=re.sub(r'\{\{([A-Z_]+)\}\}',replacement,template)
    assert '{{' not in text
    tsv=io.StringIO();keys=['id','tesis_id','mapa_id','localizador','afirmacion','dictamen','evidencia','razon','decision']
    writer=csv.DictWriter(tsv,fieldnames=keys,delimiter='\t',lineterminator='\n',extrasaction='ignore');writer.writeheader();writer.writerows(rs)
    summary=dict(pieza='trabajo',report=str(REPORT.relative_to(ROOT)),decisiones=str((BASE/'decisiones.json').relative_to(ROOT)),cifras=str((BASE/'cifras.json').relative_to(ROOT)),reglas=str((BASE/'reglas.json').relative_to(ROOT)),comando_verificar=['python3',str(Path(__file__).relative_to(ROOT)),'--verificar','--autoprueba'],comando_producir=['python3',str(Path(__file__).relative_to(ROOT))],conteos=counts)
    outputs={REPORT:text,BASE/'afirmaciones.tsv':tsv.getvalue(),BASE/'coverage.json':encoded(coverage),BASE/'cifras.json':encoded(es),BASE/'reglas.json':encoded(rules),BASE/'resumen.json':encoded(summary)}
    inputs=['decisiones.json','editorial.md','fuentes.json','producir.py']
    manifest={'corte':d['corte'],'inputs':{name:sha((BASE/name).read_bytes()) for name in inputs},'original_sha256':d['original_sha256'],'mapa_sha256':sha(MAP.read_bytes()),'outputs':{str(p.relative_to(ROOT)):sha(t.encode()) for p,t in outputs.items()},'alcance':'reproducción editorial y trazabilidad de sellos; no recalcula microdato ni concede revisión humana'}
    outputs[BASE/'manifest.json']=encoded(manifest)
    return outputs,counts,es

def selftest(es):
    bad=copy.deepcopy(es);bad[1]['denominador']=bad[0]['denominador']
    try:validate_evidence(bad)
    except AssertionError:pass
    else:raise AssertionError('no detecta contrato/ocupados confundidos')
    bad=copy.deepcopy(es);bad[0]['result']=''
    try:validate_evidence(bad)
    except AssertionError:pass
    else:raise AssertionError('no detecta cantidad sin RESULT')
    try:validate_template('Una prevalencia inventada es 92.7%.')
    except AssertionError:pass
    else:raise AssertionError('no detecta cantidad editorial sin respaldo')
    print('AUTOPRUEBA: rechaza cantidad literal sin respaldo, RESULT vacío y denominador incompatible')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verificar',action='store_true');parser.add_argument('--autoprueba',action='store_true');args=parser.parse_args()
    outputs,counts,es=render()
    if args.autoprueba:selftest(es)
    for p,t in outputs.items():
        if args.verificar:assert p.exists() and p.read_text()==t,'regeneración difiere: '+str(p)
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
    print(('VERIFICA SIN DIFERENCIAS' if args.verificar else 'PRODUCIDO')+' '+json.dumps(counts,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
