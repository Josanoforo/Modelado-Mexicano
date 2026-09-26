"""Extrae procedencia y cifras; los dictámenes son decisiones editoriales explícitas."""
import csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).parent
REPORT='Psicología_del_Consumidor_Mexicano__Patrones__Contradicciones_y_Estrategia.md'
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
v1=(ROOT/'corpus/reports'/REPORT).read_text().splitlines()
with (ROOT/'canon/mapa-dominios-v1_1.tsv').open() as f:
    mapa=[r for r in csv.DictReader(f,delimiter='\t') if r['report']==f'corpus/reports/{REPORT}']
sources=[
 dict(id='RB2024',url='https://www.rolandberger.com/en/Insights/Publications/Inside-the-mind-of-Mexican-consumers.html',autor='Roland Berger',fecha='2024-03',poblacion='Consumidores en México, segmentos de poder de compra de la encuesta comercial',metodo='Encuesta; síntesis pública leída; no se recuperó el cuestionario completo',procedencia='(a)',alcance='Calidad y precio declarados y preferencia física; no identifica elasticidad ni causalidad; consulta 2026-09-26'),
 dict(id='MK2012',url='https://www.mckinsey.com/~/media/McKinsey/Industries/Consumer%20Packaged%20Goods/Our%20Insights/Understanding%20Mexicos%20evolving%20consumers/Understanding%20Mexicos%20evolving%20consumers.pdf',autor='Oscar Garcia, Jorge Lacayo, Anne Martinez',fecha='2012-08',poblacion='Consumidores de CDMX, Monterrey, Puebla y Querétaro; campo noviembre 2011',metodo='Encuesta presencial de gastos, concentrada en bienes de consumo rápido; documento primario leído pp.2-5',procedencia='(a)',alcance='Historia urbana; satisfacción condicional entre quienes cambiaron; no panel ni población nacional actual; consulta 2026-09-26'),
 dict(id='MK2023',url='https://www.mckinsey.com/featured-insights/charts/trading-down',autor='Fernando Hiraoka y colaboradores, McKinsey',fecha='2023-07-24',poblacion='Respondentes Mexico Consumer Sentiment Survey 2023',metodo='Encuesta comercial; resumen y descripción de gráfica leídos',procedencia='(a)',alcance='Trading down declarado; no comparable automáticamente con preguntas de 2011; consulta 2026-09-26'),
 dict(id='MK2025',url='https://www.mckinsey.com/industries/retail/our-insights/the-state-of-grocery-retail-in-mexico-2024',autor='Agustín Gutiérrez, Bruno Furtado, José Ricardo Cota, Julio Rodríguez, Aaron Braiman y Andrea Biancardi; McKinsey/Kantar',fecha='2025-01-22',poblacion='Sector de alimentos minorista mexicano',metodo='Investigación comercial con Kantar; síntesis pública leída, enlace a PDF volvió a página',procedencia='(a)',alcance='Prioridad de valor, crecimiento marca privada y formatos descuento; no cifra nacional de mecanismo, no PDF leído; consulta 2026-09-26'),
 dict(id='MK2026',url='https://www.mckinsey.com/industries/retail/our-insights/the-state-of-grocery-north-america',autor='McKinsey Retail Practice',fecha='2026',poblacion='Encuesta de consumidores de grocery y panel de recibos estadounidense; no encuesta mexicana',metodo='Encuesta marzo 2026 y panel Numerator; sección precios/marca privada leída',procedencia='(c)',alcance='Hipótesis importada: transparencia y calidad de marca privada pueden importar; no transporta frecuencia ni efectos a México; consulta 2026-09-26'),
]
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
cifras=[]
for ident,c,e,k in selected:
    i,r=next((i,r) for i,r in pisos if r['calc']==calc and r['ola']=='2022' and (r['conducta'],r['eje'],r['categoria'])==(c,e,k))
    rid=r['result_id_p']; val=res[rid]
    cifras.append(dict(id='CONS-'+ident,tipo='propia',calc=calc,result_id=rid,tabla='forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv',fila=i,valor=val,unidad='pesos corrientes mensuales por hogar' if c.startswith('MEDIA') else 'proporción de hogares' if c.startswith('HOG') else 'participación del gasto, razón de totales',periodo='2022',denominador=(('hogares con conexión' if 'SI-CONEXION' in c else 'hogares con tarjeta' if 'SI-TIENE' in c else 'hogares del universo con respuesta válida') if c.startswith('HOG') else ('hogares con gasto monetario válido' if c.startswith('MEDIA') else 'gasto directo G1' if 'EFECTIVO' in c else 'gasto alimentario para el hogar' if 'CANAL' in c else 'gasto monetario agregado'))+f'; segmento {e}/{k}',transformacion='identidad',hash_sello=sello['resultados.json'],estado_adopcion='ADOPTADO-CON-RESERVA-DE-ANCHO; FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-01; no consumidor nuevo',ic=[float(r['ic_lo']),float(r['ic_hi'])],ic_calibrado=[float(r['icc_lo']),float(r['icc_hi'])] if r['icc_lo'] else []))
for ident,src,val,unit,period,denom in [('CONS-QUAL','RB2024',2,'ratio declarado superior a','2024','importancia declarada de calidad frente a precio, todos los segmentos de poder de compra encuestados'),('CONS-FISICO','RB2024',90,'porcentaje aproximado','2024','consumidores de la encuesta; preferencia por tiendas físicas'),('CONS-TRADE2011','MK2012',4,'porcentaje','2011','respondentes referidos en pasaje alimentario p.2; cambio a marca más barata últimos doce meses'),('CONS-PRIVADA2011','MK2012',5,'porcentaje aproximado de ventas retail','2011-2012','ventas retail, contexto histórico citado p.3; no proporción de consumidores'),('CONS-TRADE2023','MK2023',23,'porcentaje','2023','respondentes que declaran trading down en la canasta, no población nacional ponderada acreditada')]:
    cifras.append(dict(id=ident,tipo='externa',fuente_id=src,valor=val,unidad=unit,periodo=period,denominador=denom))
dump('consumo-cifras.json',cifras)
# Decisiones por afirmación del mapa, elaboradas después de leer el v1, fuentes y sellos.
dec={
1:('MATIZA','RB2024 sostiene importancia declarada superior al precio en segmentos de poder de compra; no significa elasticidad, conducta observada ni que precio no importe.',['RB2024']),
2:('MATIZA','MK2012 localiza la cifra en encuesta urbana de bienes rápidos de 2011 y pasaje alimentario; no es tasa universal actual de cambio por crisis.',['MK2012']),
3:('MATIZA','MK2012 describe expectativas superadas y satisfacción en submuestra pequeña que cambió; la intención de no retornar no es conducta futura observada.',['MK2012']),
4:('SIN-CIFRA','Satisfacción posterior no distingue inercia de disponibilidad, aprendizaje, precio ni afecto; ENIGH no pregunta motivos o marcas.',['MK2012']),
5:('SIN-CIFRA','No se recuperó GWI con definición operacional, población y base del constructo aspiracional.',[]),
6:('SIN-CIFRA','Experimento importado citado en v1 no identifica mecanismo nacional; ENIGH gasto no mide estatus percibido ni motivación.',['CONS-ALIMENTOS']),
7:('SIN-CIFRA','El v1 transporta una relación psicológica sin acreditar muestra mexicana ni pregunta; falta documento primario específico.',[]),
8:('SIN-CIFRA','Estudio cualitativo de élites no leído directamente en este lote; no se mantiene cifra ni generalización a clases medias.',[]),
9:('MATIZA','El gasto efectivo es predominante en ENIGH, pero participación de gasto de hogares no es preferencia personal PCMI.',['CONS-EFECTIVO']),
10:('SIN-CIFRA','La cifra atribuida a ENIF 2025 carece de identidad de ola; la última ola está reservada. No se sustituye por gasto ENIGH.',[]),
11:('MATIZA','Tenencia ENIGH es de hogares, no adultos; el contraste por hogar aclara acceso sin refutar tasa personal no verificada.',['CONS-TARJETA']),
12:('SIN-CIFRA','El dato histórico de confianza interpersonal no equivale a confianza de compra, marca o publicidad; no se publica su porcentaje sin RESULT puntual.',[]),
13:('SIN-CIFRA','Exclusividad relacional y primacía de recomendación exigen medir alternativas de información y compra; los pisos de gasto no identifican canal causal.',[]),
14:('SIN-CIFRA','No recuperado instrumento IZEA, marco muestral ni denominador de compra por recomendación; no tratar como efecto causal.',[]),
15:('SIN-CIFRA','No recuperada fuente primaria AMVO con año y base retail; incidencia ENIGH de hogares no es cuota monetaria retail.',['CONS-INTERNET']),
16:('MATIZA','RB2024 sí expresa preferencia física; ENIGH registra compra en periodo corto. La no compra no prueba preferencia ni falta de acceso.',['RB2024','CONS-INTERNET','CONS-INTERNET-COND','CONS-CONEXION']),
17:('MATIZA','Efectivo y canal conveniencia tienen estimandos distintos; ENIGH no identifica pagos OXXO ni su exclusividad internacional.',['CONS-EFECTIVO','CONS-CONVENIENCIA']),
18:('MATIZA','Cuota y comparadores aparecen en MK2012: son contexto histórico, no Kantar 2024 acreditado. Actualización 2025 describe crecimiento, no cuota homogénea.',['MK2012','MK2025']),
19:('SIN-CIFRA','Penetración y conversión chat usan bases distintas no recuperadas; disponibilidad de celular no valida WhatsApp ni rendimiento.',[]),
20:('SIN-CIFRA','No se recuperó Google con definición de influir y unidades hogar/decisión/persona; cohorte no determina causalmente agencia.',[]),
21:('SIN-CIFRA','No se recuperó corte y cartera Banxico que respalden cuota MSI del v1; saldo no es proporción de consumidores.',[]),
22:('SIN-CIFRA','Umbral universal MSI es recomendación comercial sin ensayo, categorías o costo total; no requisito empírico.',[]),
23:('MATIZA','Piso ENIGH abierto de 2022 sostiene brecha regional en cierre; cifras de 2024 no se reutilizan por reserva, y medias nominales no aíslan cultura.',['CONS-GASTO-CDMX','CONS-GASTO-CHIAPAS']),
24:('SIN-CIFRA','Norte y exposición estadounidense mezclan oferta, ingreso y contacto; no se identificó diseño que los separe.',[]),
25:('SIN-CIFRA','Pronóstico comercial BNPL no recuperado; fiado no es BNPL, ni prueba cobertura a excluidos formales.',['CONS-FIADO']),
26:('SIN-CIFRA','AMVO Buen Fin no recuperada con denominador; desconfianza declarada no demuestra aprendizaje o detección efectiva.',[]),
27:('MATIZA','Se conserva la corrección conceptual del v1: índice agregado (c) no causa individual; no se republican scores sin fuente primaria leída.',[]),
28:('SIN-CIFRA','Estigma no está operacionalizado en instrumentos de gasto; se propone medir selección controlando calidad y precio.',[]),
29:('SIN-CIFRA','No hay encuesta comparable LatAm que permita ranking contemporáneo de lealtad.',[]),
30:('SIN-CIFRA','El ciclo secuencial es esquema hipotético; ni diario de gasto ni índices nacionales observan secuencia o necesidad de cada etapa.',[]),
31:('MATIZA','MK2023 recuperada sostiene trading down; componentes EY y salud siguen sin fuente primaria leída; no se presupone invariancia desde 2011.',['MK2023','MK2025']),
32:('SIN-CIFRA','No recuperados artículo y modelos SPM; varianza explicada de creencias no equivale a efecto causal o cuota de decisión.',[]),
33:('SIN-CIFRA','Escalas de seguridad, fraude, abandono y confianza de durable difieren; no recuperadas fuentes primarias y no se valida motivo con uso de tarjeta.',['CONS-TARJETA-COND']),
34:('SIN-CIFRA','Casos Pix/UPI no son tratamiento comparable México; no se verificaron las tasas y no se transporta causalidad de intervención nacional.',[]),
35:('SIN-CIFRA','Proyecciones sin modelo, intervalos o diseño de evaluación; escenarios de oferta/ingreso se conservan sin fechas y cuotas prometidas.',['MK2025']),
36:('MATIZA','La síntesis repite cifras y mecanismos sin respaldo: se conserva diagnóstico heterogéneo y se reemplazan mandatos universales por reglas a probar.',['CONS-INTERNET','CONS-EFECTIVO','MK2025']),
38:('SIN-CIFRA','Porcentajes ENDUTIH v1 sin corte de ola verificable; encuesta mide personas y no compra. Última ola no se abrió por reserva.',[]),
39:('SIN-CIFRA','ENIF 2024 es última ola reservada; brecha por sexo no se publica aquí desde resultados externos para evitar abrir la reserva.',[]),
}
claims=[]
covered=set()
for m in mapa:
    n=int(m['id_afirmacion'].split('-')[-1]);d,reason,ev=dec[n]
    loc=m['localizador']; nums=set()
    for a,b in re.findall(r'L(\d+)(?:-L?(\d+))?',loc): nums.update(range(int(a),int(b or a)+1))
    covered.update(nums)
    claims.append(dict(id=m['id_afirmacion'],mapa_id=m['id_afirmacion'],localizador=loc,texto_v1=m['texto_vigente'],dictamen=d,razon=reason,evidencia_ids=ev,estado_adopcion='No adopta tesis; pisos usados adoptados por FP-2d37-01, literatura externa no es adopción',vigencia='Corte 2c646cba; descripción histórica, no predicción',cambio_editorial='Reescrito con límites en report v2; porcentaje v1 no recuperado se retira del cuerpo publicable',razon_sin_cifra=('restricción del proyecto' if n in [10,38,39] else 'instrumento' if n in [4,6,13,22,28,30,34,35] else 'adquisición') if d=='SIN-CIFRA' else '',mapa_dictamen=m['dictamen'],report_sha256=m['report_sha256']))
# Cobertura adicional conservadora: cada línea de contenido fuera de localizadores mapa
# recibe fila propia (puede contener afirmaciones hermanas; ninguna desaparece por inventario).
exclusions=[]
for i,line in enumerate(v1,1):
    if not line.strip() or line.startswith('#') or line.strip()=='---' or line.startswith('|---'):
        exclusions.append(dict(linea=i,razon='línea vacía, título o separador; no afirmación')); continue
    if i<21:
        reason='Nota histórica de corrección y procedencia: se conserva como antecedente, sin adoptar sus cifras ni reescribir sello; el alcance conceptual coincide con CONS-027.'
        d='MATIZA'; ev=[]; cat=''
    elif 342<=i<=355:
        reason='Pronóstico o escenario de esta línea: no dispone de modelo prospectivo ni intervalo calibrado; ingreso, regulación y oferta pueden invertir la trayectoria. Se retira promesa y se conserva escenario condicional.'
        d='SIN-CIFRA'; ev=['MK2025']; cat='falta de ejecución'
    elif 356<=i<=371:
        reason='Autocrítica del v1: se conserva la advertencia de sesgo, transporte y causalidad como límite editorial, sin convertir sus cantidades incidentales en evidencia validada.'
        d='MATIZA';ev=[];cat=''
    elif i in covered:
        matches=[]
        for m in mapa:
            for a,b in re.findall(r'L(\d+)(?:-L?(\d+))?',m['localizador']):
                if int(a)<=i<=int(b or a): matches.append(int(m['id_afirmacion'].split('-')[-1])); break
        # Las afirmaciones agrupadas conservan todas las decisiones de sus componentes.
        decisions=[dec[n] for n in matches]
        reason='Desglose de línea, incluido en mapa: '+'; '.join(f'CONS-{n:03}: {dec[n][1]}' for n in matches)
        d=dec[matches[0]][0] if len(set(t[0] for t in decisions))==1 else 'MATIZA'
        ev=sorted(set(e for t in decisions for e in t[2])); cat='instrumento' if d=='SIN-CIFRA' else ''
    else:
        theme=('Segmentación' if 166<=i<=209 else 'Comparación internacional' if 250<=i<=272 else 'Recomendación estratégica' if 273<=i<=337 else 'Mecanismo psicológico' if 74<=i<=165 else 'Generalización de mercado')
        reason=theme+' adicional: '+('la línea mezcla cohortes, AMAI, ingreso, región o género; atributos y normas no se identifican por composición de hogar y no hay fuente primaria específica recuperada.' if theme=='Segmentación' else 'se requiere igualdad de pregunta, periodo y denominador entre países; índices nacionales y cifras sin fuente actual no prueban excepcionalidad.' if theme=='Comparación internacional' else 'el mandato se reformula como PROPUESTO-POR-EJECUTOR, sin promesa de eficacia: requiere prueba con margen, devolución, costo y acceso por categoría.' if theme=='Recomendación estratégica' else 'la secuencia, motivo o primacía de esta línea no se observa en gasto; covariación, satisfacción o penetración no identifica la explicación frente a oferta, ingreso y aprendizaje.' if theme=='Mecanismo psicológico' else 'la fuente específica y el denominador de esta línea no se recuperaron; se retira cifra o ranking del cuerpo sin interpretar ausencia de evidencia como refutación.')
        d='SIN-CIFRA';ev=[];cat='instrumento' if (i>=273 or 74<=i<=90 or 210<=i<=249) else 'adquisición'
    claims.append(dict(id=f'CONS-V1-L{i:03}',mapa_id=None,localizador=f'L{i}',texto_v1=line,dictamen=d,razon=reason,evidencia_ids=ev,estado_adopcion='Sin adopción de la afirmación; propuesta editorial',vigencia='Corte 2c646cba; v1 conservado íntegro',cambio_editorial='Retirada del cuerpo como afirmación estable; reconvertida en límite o hipótesis; texto íntegro conservado en esta fila',razon_sin_cifra=cat))
dump('consumo-afirmaciones.json',claims)
dump('consumo-cobertura-v1.json',exclusions)
dump('consumo-corte.json',dict(commit='2c646cba93eebc9189a8135a5369bb45e8d29b89',v1=f'corpus/reports/{REPORT}',v1_sha256=hashlib.sha256((ROOT/'corpus/reports'/REPORT).read_bytes()).hexdigest(),mapa='canon/mapa-dominios-v1_1.tsv',mapa_sha256=hashlib.sha256((ROOT/'canon/mapa-dominios-v1_1.tsv').read_bytes()).hexdigest(),tabla_sha256=hashlib.sha256((ROOT/'forense/analisis/consumo-gasto/tabla-pisos-consumo-v1_0.tsv').read_bytes()).hexdigest(),derivado_consulta='consulta.py result no encontró RESULT; recuperado por llave desde CALC sellado con hash comprobado',lectura='v1 completo por bloques; ningún microdato; no ola reservada; ENDUTIH 2024 apareció en búsqueda web pero no se abrió documento ni se usa dato'))
print('consumo',len(mapa),'mapa',len(claims),'filas',len(cifras),'cifras')

body=(OUT/'report-template.md').read_text()
for c in cifras:
    if c['tipo']=='propia':
        value=c['valor'] if c['id'].startswith('CONS-GASTO-') else c['valor']*100
        body=body.replace('{'+c['id'].removeprefix('CONS-')+'}',f"{value:.1f}")
(ROOT/'corpus/reports-v2'/REPORT).write_text(body)
