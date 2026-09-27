"""Deriva cifras y prosa desde juicios humanos explícitos; no decide dictámenes."""
import argparse, csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).parent
SOURCE=ROOT/'forense/analisis/reports-v2/consumo-familia-2/consumo'
REPORT='Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md'
outputs={}
def dump(name,obj):
    outputs[OUT/name]=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
claims=json.loads((SOURCE/'consumo-juicios.json').read_text())['juicios']
assert len({r['id'] for r in claims})==len(claims)
sources=json.loads((SOURCE/'consumo-fuentes-leidas.json').read_text())['fuentes']
dump('consumo-fuentes.json',sources)
calc='CALC-ENIGH-CONSUMO-PISOS-0002'
rp=ROOT/'data/corrida0'/calc/'resultados.json'
res=json.loads(rp.read_text())['resultados']
sello=json.loads((rp.parent/'sello.json').read_text())
assert hashlib.sha256(rp.read_bytes()).hexdigest()==sello['resultados.json']
with (ROOT/'forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv').open() as f:
    pisos=[(i,r) for i,r in enumerate(csv.DictReader(f,delimiter='\t'),2)]
selected=[('INTERNET','HOG-COMPRA-INTERNET','TOTAL','TODOS'),('CONEXION','HOG-CONEX-INTERNET','TOTAL','TODOS'),('INTERNET-COND','HOG-COMPRA-INTERNET-SI-CONEXION','TOTAL','TODOS'),('EFECTIVO','PART-EFECTIVO-EN-GASTO-DIRECTO','TOTAL','TODOS'),('ALIMENTOS','PART-ALIMENTOS','TOTAL','TODOS'),('CONVENIENCIA','PART-CANAL-CONVENIENCIA','TOTAL','TODOS'),('ABARROTES','PART-CANAL-ABARROTES','TOTAL','TODOS'),('SUPER','PART-CANAL-SUPER-MEMBRESIA','TOTAL','TODOS'),('TARJETA','HOG-TIENE-TARJETA-CREDITO','TOTAL','TODOS'),('TARJETA-COND','HOG-USA-TARJETA-ALIMENTOS-SI-TIENE','TOTAL','TODOS'),('FIADO','HOG-COMPRA-FIADO','TOTAL','TODOS'),('INTERNET-D01','HOG-COMPRA-INTERNET','DECIL','D01'),('INTERNET-D10','HOG-COMPRA-INTERNET','DECIL','D10'),('ALIMENTOS-D01','PART-ALIMENTOS','DECIL','D01'),('ALIMENTOS-D10','PART-ALIMENTOS','DECIL','D10')]
selected += [('GASTO-CDMX','MEDIA-GASTO-MON-MENSUAL','ENTIDAD','09'),('GASTO-CHIAPAS','MEDIA-GASTO-MON-MENSUAL','ENTIDAD','07')]
selected += [('GASTO-TOTAL','MEDIA-GASTO-MON-MENSUAL','TOTAL','TODOS'),('INTERNET-NL','HOG-COMPRA-INTERNET','ENTIDAD','19'),('INTERNET-BC','HOG-COMPRA-INTERNET','ENTIDAD','02'),('INTERNET-CHIH','HOG-COMPRA-INTERNET','ENTIDAD','08'),('INTERNET-CDMX','HOG-COMPRA-INTERNET','ENTIDAD','09'),('INTERNET-CHIAPAS','HOG-COMPRA-INTERNET','ENTIDAD','07')]
cifras=[]
for ident,c,e,k in selected:
    i,r=next((i,r) for i,r in pisos if r['calc']==calc and r['ola']=='2022' and (r['conducta'],r['eje'],r['categoria'])==(c,e,k))
    rid=r['result_id_p']; val=res[rid]
    cifras.append(dict(id='CONS-'+ident,tipo='propia',calc=calc,result_id=rid,tabla='forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv',fila=i,valor=val,unidad='pesos corrientes mensuales por hogar' if c.startswith('MEDIA') else 'proporción de hogares' if c.startswith('HOG') else 'participación del gasto, razón de totales',periodo='2022',denominador=(('hogares con conexión' if 'SI-CONEXION' in c else 'hogares con tarjeta' if 'SI-TIENE' in c else 'hogares del universo con respuesta válida') if c.startswith('HOG') else ('hogares con gasto monetario válido' if c.startswith('MEDIA') else 'gasto directo G1' if 'EFECTIVO' in c else 'gasto alimentario para el hogar' if 'CANAL' in c else 'gasto monetario agregado'))+f'; segmento {e}/{k}',transformacion='identidad',hash_sello=sello['resultados.json'],estado_adopcion='ADOPTADO-CON-RESERVA-DE-ANCHO; FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-01; no consumidor nuevo',ic=[float(r['ic_lo']),float(r['ic_hi'])],ic_calibrado=[float(r['icc_lo']),float(r['icc_hi'])] if r['icc_lo'] else []))
for ident,src,val,unit,period,denom in [('CONS-QUAL','RB2024',2,'ratio declarado superior a','2024','importancia declarada de calidad frente a precio, todos los segmentos de poder de compra encuestados'),('CONS-FISICO','RB2024',90,'porcentaje aproximado','2024','consumidores de la encuesta; preferencia por tiendas físicas'),('CONS-TRADE2011','MK2012',4,'porcentaje','2011','respondentes referidos en pasaje alimentario p.2; cambio a marca más barata últimos doce meses'),('CONS-PRIVADA2011','MK2012',5,'porcentaje aproximado de ventas retail','2011-2012','ventas retail, contexto histórico citado p.3; no proporción de consumidores'),('CONS-TRADE2023','MK2023',23,'porcentaje','2023','respondentes que declaran trading down en la canasta, no población nacional ponderada acreditada')]:
    cifras.append(dict(id=ident,tipo='externa',fuente_id=src,valor=val,unidad=unit,periodo=period,denominador=denom))
for c in cifras:
    if c['tipo']=='externa':
        source=next(s for s in sources if s['id']==c['fuente_id'])
        c.update(estado_verificacion='LEÍDO EN FUENTE PRIMARIA',localizador=source['localizador'],fecha_consulta=source['consulta'],alcance='Cifra externa histórica en universo de la fuente; no RESULT ni medición nueva del proyecto')
dump('consumo-cifras.json',cifras)
# Cobertura comprueba identidades; el mapa no es fuente de dictámenes.
v1=(ROOT/'corpus/reports'/REPORT).read_text().splitlines()
with (ROOT/'canon/mapa-dominios-v1_1.tsv').open() as f:
    mapa=[r for r in csv.DictReader(f,delimiter='\t') if r['report']==f'corpus/reports/{REPORT}']
assert {r['mapa_id'] for r in claims if r.get('mapa_id')}=={r['id_afirmacion'] for r in mapa}
for m in mapa:
    r=next(r for r in claims if r['id']==m['id_afirmacion'])
    assert r['texto_v1']==m['texto_vigente'] and r['localizador']==m['localizador']
covered=set()
for r in claims:
    assert r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}
    assert r['razon'] and r['revision_analista']
    assert r['dictamen']!='SIN-CIFRA' or r['razon_sin_cifra']
    if r['id'].startswith('CONS-V1-L'):
        n=int(r['id'].removeprefix('CONS-V1-L')); assert r['texto_v1']==v1[n-1]; covered.add(n)
    for c in r.get('clausulas',[]):
        assert c['razon'] and (c['dictamen']!='SIN-CIFRA' or c['razon_sin_cifra'])
ev={c['id'] for c in cifras}|{s['id'] for s in sources}
for r in claims:
    assert set(r['evidencia_ids'])<=ev
    for c in r.get('clausulas',[]): assert set(c['evidencia_ids'])<=ev
exclusions=[]
for n,line in enumerate(v1,1):
    if n in covered: continue
    assert not line.strip() or line.startswith('#') or line.strip()=='---' or line.startswith('|---'), f'afirmación v1 omitida L{n}'
    exclusions.append(dict(linea=n,razon='línea vacía, título o separador; no afirmación'))
dump('consumo-afirmaciones.json',claims)
dump('consumo-cobertura-v1.json',exclusions)
old_corte=dict(v1=f'corpus/reports/{REPORT}',v1_sha256=hashlib.sha256((ROOT/'corpus/reports'/REPORT).read_bytes()).hexdigest(),mapa='canon/mapa-dominios-v1_1.tsv',mapa_sha256=hashlib.sha256((ROOT/'canon/mapa-dominios-v1_1.tsv').read_bytes()).hexdigest(),tabla_sha256=hashlib.sha256((ROOT/'forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv').read_bytes()).hexdigest(),derivado_consulta='consulta.py result no encontró RESULT; recuperado por llave desde CALC sellado con hash comprobado')
old_corte.update(commit='1eeb855272b933642177e3f32d51adc89f1009a0',tabla_fuente=str((SOURCE/'consumo-juicios.json').relative_to(ROOT)),tabla_fuente_sha256=hashlib.sha256((SOURCE/'consumo-juicios.json').read_bytes()).hexdigest(),fuentes_leidas=str((SOURCE/'consumo-fuentes-leidas.json').relative_to(ROOT)),lectura='Cada fila revisada por identidad; fuentes primarias públicas efectivamente abiertas; sin microdatos ni nuevas reservas')
dump('consumo-corte.json',old_corte)
body=(OUT/'report-template.md').read_text()
for c in cifras:
    if c['tipo']=='propia':
        value=c['valor'] if c['id'].startswith('CONS-GASTO-') else c['valor']*100
        body=body.replace('{'+c['id'].removeprefix('CONS-')+'}',f"{value:.1f}")
        for kind,values in [('IC',c['ic']),('ICC',c.get('ic_calibrado',[]))]:
            for side,value in zip(['LO','HI'],values):
                body=body.replace('{'+c['id'].removeprefix('CONS-')+'-'+kind+'-'+side+'}',f"{value if c['id'].startswith('CONS-GASTO-') else value*100:.1f}")
assert not re.search(r'\{[A-Z][A-Z0-9-]+\}',body), 'placeholder sin resolver'
outputs[ROOT/'corpus/reports-v2'/REPORT]=body
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
if args.check:
    errors=[str(path.relative_to(ROOT)) for path,text in outputs.items() if not path.exists() or path.read_text()!=text]
    if errors: raise SystemExit('NO-REPRODUCE '+', '.join(errors))
else:
    for path,text in outputs.items():path.write_text(text)
print(('REPRODUCE' if args.check else 'GENERADO')+f' consumo: {len(claims)} registros, {len(mapa)} filas mapa, {len(cifras)} cifras; dictámenes leídos de tabla fuente')
