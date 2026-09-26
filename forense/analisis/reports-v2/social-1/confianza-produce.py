"""Deriva cobertura y tablas desde juicios explícitos del ejecutor por unidad v1; no mide datos."""
import csv,json,hashlib,re,subprocess
from pathlib import Path
OUT=Path(__file__).parent
REPORT='corpus/reports/Confianza_y_Desconfianza_en_México__Anatomía_Psicológica_de_una_Sociedad_Dual.md'
raw=Path(REPORT).read_bytes(); lines=raw.decode().splitlines(); sha=hashlib.sha256(raw).hexdigest()
# Cada asignación se decidió tras leer la unidad completa, no por búsqueda de palabras.
D={}
def put(nums,dictamen,argumento,evidencia=(),razon=''):
 for n in nums:D[n]=(dictamen,argumento,list(evidencia),razon)
put([3,375],'MATIZA','El gradiente relacional existe en WVS, pero concentración no demuestra transferencia de un stock de confianza ni adaptación óptima; se retira el cierre que descarta todo déficit.', ['CONF-C35','CONF-C42','CONF-OECD25'])
put([9,47,71],'ROMPE','Q57 ponderada 18+ WVS2018 da 10.5%, incompatible con la atribución 22%; Latinobarómetro2023 es otro periodo y diseño. Serie histórica y comparadores no se reconstruyen con una sola ola.',['CONF-C42','CONF-C29'])
put([11],'SIN-CIFRA','Saldo mucha menos ninguna no es porcentaje mucha/algo. Falta ficha completa Research Land2026 y comparadores; no prueba familia como única institución positiva.',razon='adquisición pendiente')
put([13,51,53,73,74,283,312],'MATIZA','WVS/LB sostienen posiciones relativas de iglesias/FFAA frente a partidos, pero no orden universal, estabilidad temporal ni escala homogénea; OCDE usa otro corte y contradice policía siempre baja. ENCIG es urbana y sus valores no son nacionales rurales.',['CONF-C21','CONF-C25','CONF-C33','CONF-C38','CONF-OECD24'])
put([15,63],'SIN-CIFRA','Distinguir objetos de confianza es necesario; un análisis factorial externo no prueba independencia psicológica en toda población mexicana ni que la mayoría adopte prudencia óptima.',razon='instrumento inadecuado')
put([17,77,333],'SIN-CIFRA','ENVIPE permite cifra negra por delito, pero requiere RESULT y denominador específico; no investigar no equivale a impunidad, y resolución positiva entre denuncias tiene otro denominador. No se heredan cifras como mecanismo de confianza.',razon='falta de ejecución en este contraste')
put([19,78,205,328],'SIN-CIFRA','Un contraste de sexo de Ipsos no demuestra unicidad mundial ni mecanismo de solidaridad. Violencia y no denuncia requieren ola, población y denominador propios; no se comparan con confianza sin diseño conjunto.',razon='adquisición pendiente')
put([21,79,193,329],'MATIZA','OCDE permite describir gradientes por educación en muestra urbana, pero diferencia educativa no identifica efecto de populismo, transferencias o clase. Se retira unicidad internacional sin tabla comparable.',['CONF-OECD24'])
put([23,85,235,237,239,320],'MATIZA','Experimentos y encuestas observan conductas/unidades distintas; enviar parte de una dotación no se resta de proporción de respuestas de encuesta. La literatura LAC no prueba que todos los mexicanos cooperen más de lo que declaran.',['CONF-C42'], 'no comparabilidad')
put([25,76,149],'MATIZA','Datos transversales y modelos recíprocos no identifican las dos flechas causales; viñetas aleatorias aportan mecanismo acotado sobre actitudes fiscales, no equilibrio nacional estable.',['CONF-CARBON24'])
put([27,173,175,299],'SIN-CIFRA','Informalidad incluye restricciones de oferta laboral/productividad y no ausencia total de relación estatal. Falta diseño que identifique confianza→informalidad o salud→informalidad; no se romantiza como elección homogénea.',razon='instrumento inadecuado')
put([29,75,155,157,159,319],'MATIZA','Victimización y confianza pueden asociarse, pero conservación de familiares no descarta efectos horizontales en todas comunidades. Autodefensas no se derivan de marginales de confianza; selección territorial y protección rival siguen abiertas.',['CONF-C17','CONF-C19'], 'no comparabilidad')
put([31,199],'SIN-CIFRA','Fundación SM y rangos juveniles no equivalen a adultos18+ de los pisos; falta fuente primaria del gradiente y cifras de legisladores. No deducir cohorte de corte transversal.',razon='adquisición pendiente')
put([33,353],'SIN-CIFRA','82% no tiene año ni denominador reproducible. Proporción de transacciones, personas y valor monetario son diferentes; no atribuye uso a memoria de crisis ni permite afirmar exclusión del mismo porcentaje.',razon='adquisición pendiente')
put([35,265,267],'SIN-CIFRA','Recuentos de clientes, tiendas, tasas y NPS dependen de fecha y geografía; casos supervivientes no identifican éxito por transparencia/puentes físicos frente a precio, cobertura, publicidad o selección.',razon='adquisición pendiente')
put([37,295,327],'SIN-CIFRA','Latinobarómetro2024 reservada: no se abre ni su tabulado para validar récord o serie. CPI es percepción y no calidad objetiva; comparar ambas sin enlace no demuestra independencia psicológica.',razon='restricción del proyecto')
put([45,55,57,59],'MATIZA','Taxonomía sirve como marco conceptual; tipos se solapan y no son siete dimensiones psicométricas verificadas para población mexicana. Relación, transacción y sistema requieren reactivos separados.', ['CONF-OECDLAC25'])
put([49,72,103,311],'MATIZA','Familia WVS es más confiable que vecinos/conocidos/desconocidos, pero no confianza exclusiva ni plena de todos. ENCIG dice familiares en universo urbano; mapa confundía ausencia literal de familia nuclear con ausencia del componente relacional.',['CONF-C35','CONF-C41','CONF-C31','CONF-C32','CONF-E01'])
put([83,111,113,291,316,324],'MATIZA','El v1 identifica diáspora hispana en simpatía: transporte a residentes mexicanos no está validado. Calidez no mide confianza y superficial es juicio no observado; se conserva distinción conceptual sin frecuencia nacional.',razon='no comparabilidad')
put([84],'SIN-CIFRA','Mapa no confirmó escala específica de Mogro-Wilson con esa muestra; personalismo como precondición universal tampoco se prueba aun si una escala de diáspora existe.',razon='adquisición pendiente')
put([86,127],'SIN-CIFRA','Compadrazgo y palanca son hipótesis etnográficas plausibles; faltan referencias completas y población del estudio. No se infiere ausencia de compensación o cobertura de seguro para todos.',razon='adquisición pendiente')
put([87,183,185,187,189,342,356,369],'SIN-CIFRA','Entidad/urbanización son ejes medibles, pero no se ejecutó el contraste que sostenga norte-centro-sur como países psicológicos ni causalidad maya→seguridad. Estereotipos capitalinos no son evidencia; pueblos indígenas no son bloque homogéneo.',razon='falta de ejecución en este contraste')
put([91,92,93,94,95,287,373],'MATIZA','La cautela contra esencia cultural es pertinente; contraejemplos entre países no identifican efecto nulo de cultura/religión/familismo. Bardhan ofrece mecanismo rival, no certificación de racionalidad universal de mordida.', ['CONF-OECDLAC25'])
put([105],'ROMPE','El 27% OCDE citado corresponde a favor político por empleo privado, no a rechazo de soborno por funcionario; cifra negra tampoco significa impunidad. La calibración racional del radio no se observa.',['CONF-E03','CONF-OECD24'])
put([107,131,259,261,314,315,337,344,346,354,357,359],'SIN-CIFRA','Referencias y repetición pueden reducir incertidumbre, pero no se midió requisito universal, superioridad sobre contratos, ROI o tiempo mínimo. Se transforma en propuesta de prueba local con costos/precio/calidad controlados.',razon='instrumento inadecuado')
put([117,119,313,355,365,371],'MATIZA','Adaptación es hipótesis compatible con riesgo observado, no resultado de maximización demostrada. Información incorrecta, exclusión y persistencia de hábitos son rivales; la prudencia puede tener costos.',['CONF-C42','CONF-C35','CONF-CARBON24'])
put([123,125,167,195,318,326],'SIN-CIFRA','Redes pueden complementar o sustituir servicios según acceso, ingreso y obligaciones; el report no identifica cuánto ni efectos netos. No toda persona pobre depende de la misma red ni toda élite tiene seguro privado.',razon='instrumento inadecuado')
put([133,253,341,345,352],'SIN-CIFRA','Encuestas empresariales seleccionan empresas/empleados; razones de permanencia y liderazgo no prueban 2.7x causal. Jerarquía y paternalismo no son requisitos nacionales; rol, salario y condiciones rivales no fueron aislados.',razon='adquisición pendiente')
put([141,143,145,317],'SIN-CIFRA','Cronología política sirve como contexto; duración hegemónica y densidades asociativas no identifican supresión causal ni trayectoria de confianza. Falta serie enlazada y contrafactual para atribuir a Fox o PRI.',razon='instrumento inadecuado')
put([151],'SIN-CIFRA','CPI no mide corrupción objetiva y cambia por edición; los porcentajes de soborno y motivos de desconfianza exigen denominadores distintos. No se usa ranking/record sin tabla primaria cotejada.',razon='adquisición pendiente')
put([161,165,169],'SIN-CIFRA','Conductas defensivas, Gini corregido y clase autopercibida tienen fuentes, años y universos diferentes no trazados en v1. No se usan para cuantificar confianza ni comparar sus escalas.',razon='adquisición pendiente')
put([201,247,249,275,330,339,343],'SIN-CIFRA','Paneles de compradores/usuarios no representan a toda población. No hay diseño que pruebe sustitución de familia, superioridad de microinfluencers o efecto reputacional de queja declarada; publicidad y oferta son rivales.',razon='adquisición pendiente')
put([209,211],'SIN-CIFRA','Retornados y diáspora exigen periodo, selección y referente de confianza propios. Estudios transnacionales no prueban los niveles o la situación homogénea de todos los retornados residentes.',razon='adquisición pendiente')
put([219,221,225,231],'SIN-CIFRA','Comparadores de país mezclan olas, escalas e índices; no se verifican orden ni cifras históricas con México2018 únicamente. Homogeneidad étnica/protestantismo no son identificación causal y no se deduce esencia nacional.',razon='no comparabilidad')
put([227],'MATIZA','Instituciones y condiciones de vida son explicaciones defendibles, pero comparación nórdica observacional no demuestra efecto de cada política ni transportabilidad automática a México.',['CONF-OECDLAC25'])
put([255,350],'SIN-CIFRA','Silencio puede significar rechazo, duda, acuerdo o falta de poder; regla unívoca nacional carece de instrumento. Se propone confirmación explícita y canales confidenciales.',razon='instrumento inadecuado')
put([271],'MATIZA','Separar producto/proveedor/sistema es útil; mensajero comunitario siempre más eficaz y generalización de entrevistas con embarazadas no están identificados sin referencia y contraste local.',['CONF-OECDLAC25'])
put([303,338,340,358],'MATIZA','Accesibilidad, transparencia y canal humano son propuestas útiles; no efectos probados de Nu/OXXO. Un canal físico puede costar más o fallar y transparencia sin buen servicio no basta.', ['CONF-DIG25'])
put([325,351],'MATIZA','Baja confianza declarada no mide falta de confiabilidad moral; tampoco prueba todas personas conocidas confiables/instituciones peligrosas ni cooperación intensa universal.',['CONF-C35','CONF-C42'])
put([331],'SIN-CIFRA','Uso de efectivo y smartphones pueden coexistir por tarifas/cobertura/diseño; el porcentaje no identifica falta de confianza digital.',razon='adquisición pendiente')
put([332],'MATIZA','Confianza en una institución y seguridad percibida son objetos distintos; su coexistencia no contradice por sí sola racionalidad ni permite atribuir seguridad al ejército.',['CONF-C33'])
put([367],'MATIZA','ENCIG cubre localidades100mil+, no México rural; la cifra40% y proporciones indígenas requieren fuente propia. Encuesta nacional WVS/LB evita trasladar exclusivamente universo urbano, sin resolver representación comunal.',['CONF-ENCIG','CONF-OECDLAC25'])
claims=[];included=[];excluded=[]
for n,l in enumerate(lines,1):
 if not l:continue
 if l.startswith(('#','---')):excluded.append({'linea':n,'linea_fin':n,'razon':'título o separador sin afirmación sustantiva'});continue
 assert n in D,('unidad sin juicio',n)
 d,a,e,r=D[n]
 # Una fila por oración material, conservando texto literal completo y repetición.
 number=re.match(r'^(\d+\. )',l)
 body=l[len(number.group(1)):] if number else l
 parts=re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚ¿*])',body)
 if number:parts[0]=number.group(1)+parts[0]
 ids=[]
 for idx,part in enumerate(parts,1):
  ident=f'CONF-V1-L{n:03d}-S{idx:02d}';ids.append(ident)
  claims.append({'id':ident,'origen':'v1','report':REPORT,'report_sha256':sha,'linea':n,'linea_fin':n,'mapa_id':None,'afirmacion':part,'tipo':'descripción/mecanismo/propuesta según texto literal; juicio acota mecanismo','dictamen':d,'razon_sin_cifra':r if d=='SIN-CIFRA' else '', 'argumento':a,'evidencia':e,'estado_adopcion':'No hay adopción del juicio editorial; PROPUESTO-POR-EJECUTOR. Pisos citados adoptados por FP ac7b-01/02/04; fuentes externas publicadas.','vigencia':'Corte inicial main 2c646cba93eebc9189a8135a5369bb45e8d29b89; literatura recuperada 26/sep/2026','cambio_editorial':'Reescribir conservando solo descripción respaldada; límites y propuesta explícitos.'})
 included.append({'linea':n,'linea_fin':n,'afirmaciones':ids})
# Dictámenes del mapa son de medibilidad, no se copian como veredicto sustantivo.
m=list(csv.DictReader(open('canon/mapa-dominios-v1_1.tsv'),delimiter='\t'))
for r in m:
 if r['report']!=REPORT:continue
 num=int(r['id_afirmacion'].rsplit('-',1)[1]);ln=int(re.search(r'L(\d+)',r['localizador']).group(1))
 d,a,e,reason=D.get(ln,D[3])
 if num==3:d,a,e,reason=('SIN-CIFRA','Comparadores internacionales y serie WVS histórica no se verifican con ola mexicana2018; ausencia no refuta los valores.',[],'no comparabilidad')
 if num==6:d,a,e,reason=D[49]
 if num==10:d,a,e,reason=D[105]
 if num==19:d,a,e,reason=('SIN-CIFRA','ENIF uso/razón de no tener cuenta es unidad persona y no prueba82% de transacciones ni efecto de crisis; RESULT específicos no consumidos en este report.',[],'falta de ejecución en este contraste')
 if num==24:d,a,e,reason=D[37]
 claims.append({'id':'CONF-M-'+r['id_afirmacion'],'origen':'mapa','report':REPORT,'report_sha256':sha,'linea':ln,'linea_fin':ln,'mapa_id':r['id_afirmacion'],'afirmacion':r['texto_vigente'],'tipo':r['clase'],'dictamen':d,'razon_sin_cifra':reason if d=='SIN-CIFRA' else '', 'argumento':a+' Contexto del mapa: '+r['limite_inferencial'],'evidencia':e,'estado_adopcion':'Juicio editorial PROPUESTO-POR-EJECUTOR; cifras citadas según estados estructurados.','vigencia':'Mapa v1.1 al corte2c646cba; estados reservas/adopción actualizados desde firmas vigentes','cambio_editorial':'Sustituye dictamen de medibilidad por juicio sustantivo con alcance; mapa ajeno intacto.','dictamen_mapa_previo':r['dictamen']})
# Revisiones humanas por oración: no extender una refutación numérica a conceptos o series distintas.
for c in claims:
 if c['origen']!='v1':continue
 ln=c['linea']; ss=int(c['id'].rsplit('S',1)[1])
 if (ln==9 and ss==2) or (ln==71 and ss==2):
  c.update(dictamen='SIN-CIFRA',razon_sin_cifra='adquisición pendiente',argumento='Serie histórica y convergencia de fuentes requieren olas, fichas y tabulados independientes; no se derivan ni se refutan por corregir WVS2018.',evidencia=[])
 if (ln==47 and ss in (1,2,4)) or (ln==105 and ss in (1,3)) or (ln==71 and ss==3):
  c.update(dictamen='MATIZA',razon_sin_cifra='',argumento='La distinción conceptual o el diseño no quedan refutados por una cifra incorrecta. La generalización a una disposición/racionalidad nacional sigue sin identificación; mantener referente y alcance explícitos.')
 if 337<=ln<=359:c['tipo']='propuesta'
 elif ln in (25,27,29,105,117,119,123,125,127,131,133,141,143,145,149,155,157,159,167,173,175,193,195,205,227,239):c['tipo']='mecanismo'
 elif ln in (9,11,13,17,19,21,23,31,33,35,37,49,71,72,73,74,77,78,79,85,87,151,161,165,169,183,185,187,189,199,201,209,211,219,221,225,231,235,237,247,249,265,267,275):c['tipo']='hecho descriptivo y componentes interpretativos acotados en argumento'
 else:c['tipo']='generalización o marco conceptual'
(OUT/'confianza-afirmaciones.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
with (OUT/'confianza-afirmaciones.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(claims[0])+['dictamen_mapa_previo'],delimiter='\t',quoting=csv.QUOTE_ALL,lineterminator='\n');w.writeheader()
 for c in claims:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in c.items()})
(OUT/'confianza-cobertura.json').write_text(json.dumps({'incluidas':included,'excluidas':excluded},ensure_ascii=False,indent=2)+'\n')
print('afirmaciones',len(claims),'unidades materiales',len(included),'mapa',sum(c['origen']=='mapa' for c in claims))
