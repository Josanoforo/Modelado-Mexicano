"""Deriva tablas y report desde decisiones; no decide CONFIRMA/MATIZA/ROMPE."""
import argparse, csv, hashlib, io, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
REPORT='corpus/reports-v2/Vejez_y_Cuidado_Intergeneracional_en_México__El_Debilitamiento_del_Seguro_Familiar.md'
def read_tsv(path):
    with path.open() as h:return list(csv.DictReader((l for l in h if not l.startswith('#')),delimiter='\t'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def tsv(rows):
    s=io.StringIO(); w=csv.DictWriter(s,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows);return s.getvalue()
def outputs():
    d=json.loads((HERE/'decisiones.json').read_text())
    evid=json.loads((HERE/'evidencia.json').read_text())
    m=json.loads((HERE/'mapa-leido.json').read_text())
    r=json.loads((ROOT/evid['calc']/'resultados.json').read_text())['resultados']
    cat={x['llave']:x for x in read_tsv(ROOT/'canon/catalogo-del-mexicano-v1_2.tsv')}
    counts={v:sum(x['dictamen']==v for x in d) for v in ['CONFIRMA','MATIZA','ROMPE','SIN-CIFRA']}
    deps=[]; cifras=[]
    tabla=['| Clave · estimando | Punto · IC95 de diseño · N | Denominador, unidad y estado |','|---|---|---|']
    for x in evid['cifras']:
        k=x['result'];base=k[:-1];c=cat[k]
        value=r[k];lo=r[base+'IC-LO'];hi=r[base+'IC-HI'];n=r[base+'N']
        cifras.append(dict(clave=x['clave'],result=k,punto=value,ic95_inf=lo,ic95_sup=hi,n=n,denominador=x['denominador'],unidad=x['unidad'],ola='2022',estado=c['estado_adopcion'],calc=evid['calc'],sha_resultados=evid['hashes'][evid['calc']+'/resultados.json']))
        tabla.append(f"| {x['clave']} · {x['etiqueta']} | {value*100:.2f}% · [{lo*100:.2f}; {hi*100:.2f}]% · N={n} | {x['denominador']}; {x['unidad']}; {c['estado_adopcion']}. `{k}` |")
        deps.append(dict(llave=k,alias=x['clave'],linaje=evid['calc'],corte='11602de8',defecto_conocido='NINGUNO-MATERIAL-IDENTIFICADO-EN-C1-DISPONIBLE',estado_c1='NO-EVALUADO-EN-RECIBOS-CONSULTADOS',efecto='NO RETIRO POR AUSENCIA DE EVALUACION',conclusiones_afectadas=x['conclusion'],adopcion=c['estado_adopcion'],reserva=c['reserva'],firma=c['firma_fp']))
    claims=[{**x,'evidencia':';'.join(x['evidencia'])} for x in d]
    report=(HERE/'report-template.md').read_text().replace('{{CIFRAS}}','\n'.join(tabla))
    summary=dict(report=REPORT,registros=len(d),mapa_filas=len(m),fuentes_leidas=sum(f['estado']=='LEÍDA' for f in evid['fuentes']),dictamenes=counts,cifras=len(cifras),comando_generar=['python3',str((HERE/'genera.py').relative_to(ROOT))],comando_verificar=['python3',str((HERE/'genera.py').relative_to(ROOT)),'--check'],self_test=['python3',str((HERE/'genera.py').relative_to(ROOT)),'--self-test'])
    review=f'''# Revisión dirigida · vejez

EJECUTADO: juicio editorial manual de todas las cláusulas; el programa solo genera esta vista; no calcula conversiones entre bases temporales incompatibles ni decide dictámenes.

V-020-02: SIN-CIFRA por no comparabilidad. La refutación aritmética anterior se retira: el porcentaje ENASEM2021 y la población CONAPO2025 citada en L12 no constituyen una misma base temporal. El absoluto permanece sin confirmar hasta recuperar población, año y denominador compatibles. V-020-01 también permanece SIN-CIFRA; ninguna de las dos cifras queda confirmada o refutada por esa multiplicación. Vejez ya no tiene dictámenes ROMPE.

Esta corrección no adjudica la exposición a ENADID2023. Migración y pareja pueden recibirse por separado; su recepción no se acredita aquí.

Mecanismos revisados: V-007 y V-010 separan oferta, norma y adaptación; V-008 identifica al proveedor desde receptor condicionado; V-013/V-014 separan muestra clínica, síntomas y diagnóstico; V-016 evita monocausalidad de informalidad; V-036 retira metas sin fuente y presenta propuestas evaluables. Ninguno deriva el veredicto de la medibilidad del mapa.

Cifras principales: las siete llaves se cruzaron con objeto sellado, catálogo, exclusiones, firma FIRMADA y recibos C1 por llave/linaje. Ninguna figura en los recibos C1 consultados: no evaluada allí, no validada independientemente. La vista corrida estaba atrasada; la firma y objeto resuelven por identidad, sin editar derivados.

Reservas: ENASIC una ola, proveedor condicionado y N pequeño; sin localidad utilizable. No diagnóstico nacional de carga ni demencia, no protección efectiva o declive del seguro familiar identificado. La publicación ENADID2023 se abrió durante búsqueda antes de revisar la reserva específica de P1; sus cifras no se consumen ni se usan para concluir y el incidente se declara en evidencia.json. ENASEM2024 solo surgió en snippets de búsqueda, no abrió PDF ni alimentó conclusión; ENUT2024/ENIGH2024 no usados. No se abrió microdato.
'''
    index=f'''# Índice local · vejez

EJECUTADO: report Bloque B completo, {len(d)} decisiones por cláusula ({len(m)} filas de mapa; {sum(not x['mapa_id'] for x in d)} afirmaciones adicionales), siete pisos descriptivos con firma y reserva, tabla de dependencias C1, productor y verificador.

LEÍDO: original completo L1–199, todas las filas de mapa; fuentes primarias y límites en evidencia.json. Fuentes registradas como LEÍDA: {summary['fuentes_leidas']}. Material inaccesible o reservado no sostiene afirmaciones firmes.

PROPUESTO-POR-EJECUTOR: tres reglas de atención/medición con consumidor, condición y falsador en el report. No adoptadas, sin motor.

Objetos: decisiones.json (fuente editorial), mapa-leido.json (lectura del mapa), lectura.json (original/hash/bloques), evidencia.json (contratos/hashes/lecturas), tabla-afirmaciones.tsv, cifras.tsv, dependencias.tsv, revision-dirigida.md y resumen.json. prepara.py materializa los juicios explícitos; genera.py regenera tablas/report y comprueba el soporte material. No sustituye revisión independiente.

Comandos desde raíz: python3 forense/analisis/reports-v2/cuidado-migracion-pareja-1/vejez/genera.py; mismo comando con --check y --self-test. Reservas e incidente de publicación reservada descritos en revision-dirigida.md; sin uso de esos resultados.
'''
    return {ROOT/REPORT:report,HERE/'tabla-afirmaciones.tsv':tsv(claims),HERE/'cifras.tsv':tsv(cifras),HERE/'dependencias.tsv':tsv(deps),HERE/'revision-dirigida.md':review,HERE/'indice.md':index,HERE/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
def validate(decisions=None,evid=None,rendered=None):
    d=decisions if decisions is not None else json.loads((HERE/'decisiones.json').read_text())
    e=evid if evid is not None else json.loads((HERE/'evidencia.json').read_text())
    mapa=json.loads((HERE/'mapa-leido.json').read_text())
    assert len({x['id'] for x in d})==len(d),'ID duplicado'
    assert {x['mapa_id'] for x in d if x['mapa_id']}=={x['id_afirmacion'] for x in mapa},'Cobertura mapa'
    original=ROOT/json.loads((HERE/'lectura.json').read_text())['original']
    assert sha(original)==json.loads((HERE/'lectura.json').read_text())['sha256'],'Original cambió'
    for p,h in e['hashes'].items():assert sha(ROOT/p)==h,f'Hash cambió {p}'
    allowed={f['id'] for f in e['fuentes'] if f['estado']=='LEÍDA'}|{x['clave'] for x in e['cifras']}
    for x in d:
        assert x['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}
        assert x['motivo'] and x['revision_manual'],'Falta juicio explícito'
        if x['dictamen']=='SIN-CIFRA':assert x['razon_sin_cifra'] in {'adquisición pendiente','falta de ejecución','instrumento inadecuado','no comparabilidad','restricción del proyecto','imposibilidad justificada'}
        assert set(x['evidencia'])<=allowed,'Fuente no leída'
    cat={x['llave']:x for x in read_tsv(ROOT/'canon/catalogo-del-mexicano-v1_2.tsv')}
    excluded={x['llave'] for x in read_tsv(ROOT/'forense/analisis/catalogo/v1_2/excluidos-v1_2.tsv')}
    sig={x['id']:x for x in read_tsv(ROOT/'forense/firmas-pendientes.tsv')}
    c1=[]
    for path in e['recibos_c1']:
        c1+=read_tsv(ROOT/path)
    for x in e['cifras']:
        k=x['result'];assert k not in excluded,'Veto/celda sin punto'
        assert k in cat,'Sin catálogo'
        c=cat[k];assert c['estado_adopcion']=='ADOPTADO-CON-RESERVA-DE-ANCHO','Estado material cambió'
        assert sig[c['firma_fp']]['estado']=='FIRMADA','Adopción sin firma'
        assert x['denominador']==e['contrato_denominadores'][x['clave']],'Denominador erróneo'
        assert x['unidad']==e['contrato_unidades'][x['clave']],'Unidad errónea'
        assert c['temporalidad']=='RETROSPECTIVA','Temporalidad'
        assert not any(k in str(row) for row in c1),'Nueva dependencia C1 requiere dictamen humano'
    text=rendered if rendered is not None else outputs()[ROOT/REPORT]
    ids=set(re.findall(r'RESULT-[A-Z0-9-]+',text))
    assert ids=={x['result'] for x in e['cifras']},'Cifra propia sin respaldo'
    for line in text.splitlines():
        prose=re.sub(r'https?://\S+','',line)
        if re.search(r'\d+(?:\.\d+)?%',prose):assert 'RESULT-' in line,'Cantidad porcentual sin RESULT'
    assert '{{' not in text,'Plantilla sin resolver'
    return {'estado':'PASS','registros':len(d),'mapa':len(mapa),'cifras':len(e['cifras']),'microdatos_abiertos':False}
def self_test():
    import copy
    d=json.loads((HERE/'decisiones.json').read_text());e=json.loads((HERE/'evidencia.json').read_text());cases=[]
    bad=copy.deepcopy(d);bad=[x for x in bad if x['mapa_id']!='ASTRA5-U0-VEJEZ-001'];cases.append(('cobertura',bad,e,None))
    bad=copy.deepcopy(e);bad['cifras'][0]['denominador']='todas las personas de México';cases.append(('denominador',d,bad,None))
    bad=copy.deepcopy(e);bad['cifras'][0]['result']='RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR-2022-TAMANO-HOGAR-1-P';cases.append(('veto-sin-punto',d,bad,None))
    cases.append(('cifra-sin-fuente',d,e,outputs()[ROOT/REPORT]+'\nHay 90% sin soporte.'))
    bad=copy.deepcopy(d);bad[0]['evidencia']=['FUENTE-SOLO-BUSCADA'];cases.append(('fuente-no-leida',bad,e,None))
    for label,dd,ee,rr in cases:
        try:validate(dd,ee,rr)
        except AssertionError:continue
        raise AssertionError(f'Mutación no detectada: {label}')
    return {'estado':'PASS','mutaciones_detectadas':[x[0] for x in cases]}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--self-test',action='store_true');a=parser.parse_args()
    status=validate()
    if a.self_test:status=self_test()
    elif a.check:
        for p,content in outputs().items():assert p.read_text()==content,f'Derivado atrasado: {p}'
    else:
        for p,content in outputs().items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    print(json.dumps(status,ensure_ascii=False))
