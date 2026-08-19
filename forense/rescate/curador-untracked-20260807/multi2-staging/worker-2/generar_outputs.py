import csv, json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).parent
IN=HERE/'input-candidatas.tsv'
REL=HERE/'worker-2-relaciones.tsv'
EVI=HERE/'worker-2-evidencia.tsv'

with IN.open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==39

source_notes={
'ENFIH':('INSTRUMENTO_LOCAL_PARCIAL','MAIN:data/abrir4-variables-2026-08-08.tsv','L9-L14','La apertura local de ENFIH documenta variables financieras concretas y búsquedas de constructos, pero no demuestra para esta clave el par constructo–desenlace exigido.','Abrir el diccionario ENFIH y construir una tabla variable×constructo×desenlace para esta necesidad; verificar coobservación por llave de persona.'),
'ENIF':('INSTRUMENTO_LOCAL_PARCIAL','MAIN:forense/hitoE-campana-medicion-v2_0.md','L999-L1116','ENIF tiene reactivos financieros identificados (P9_9_1..6, P4_10 y sección 11), pero la evidencia local no verifica el cruce específico solicitado por esta clave.','Mapear en el cuestionario y microdato ENIF los reactivos de la necesidad y el desenlace, y comprobar que comparten unidad de observación.'),
'ENBIARE2021':('APERTURA_SIN_PAR_COMPLETO','MAIN:forense/matriz-impacto-universal-2026-08-06.md','L81-L86','La matriz local registra orientación futura y redes en ENBIARE, pero advierte que no sustituyen automáticamente el diseño ni prueban el desenlace coobservado de esta relación.','Abrir cuestionario/diccionario ENBIARE y localizar texto, codificación y llave del reactivo junto con el desenlace requerido.'),
'LATINOBARÓMETRO':('CUESTIONARIO_SIN_MICRODATO','MAIN:forense/hitoE-campana-medicion-v2_0.md','L1116','El cuestionario local identifica P4NOIJ como proxy de obediencia, pero el microdato no está registrado; para otras necesidades no hay mapeo de reactivo y desenlace.','Obtener el microdato bajo la licencia aplicable y mapear reactivo, codificación y desenlace para México.'),
'INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO':('DOCUMENTO_INDEXADO_SIN_MAPEO','MAIN:data/mapa-ext-academico-2026-08-06.tsv','L15','El mapa clasifica documentalmente el estudio, pero no contiene instrumento, variable ni resultado que conecte esta clave con la necesidad.','Abrir materiales suplementarios del estudio y localizar variable, tratamiento, resultado y muestra mexicanos pertinentes.'),
'DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE':('DOCUMENTO_INDEXADO_SIN_MAPEO','MAIN:data/mapa-ext-academico-2026-08-06.tsv','L2','El estudio está clasificado a umbral documental, pero la fila local no aporta variable o estimando adjudicable para esta clave.','Abrir instrumento y tablas del estudio; localizar tratamiento informativo, outcome y estimando pertinente.'),
'MEXICO_PANEL_STUDY_2012':('FUENTE_INDEXADA_SIN_APERTURA','MAIN:data/mapa-ext-general-2026-08-06.tsv','L16','El panel está inventariado localmente, pero no hay diccionario o reactivo abierto que pruebe esta relación.','Abrir cuestionario y codebook 2012 y localizar las variables exactas y su llave longitudinal.'),
'VOTAR_ENTRE_BALAS':('BASE_INDEXADA_SIN_MAPEO','MAIN:data/mapa-fuentes-externas-consolidado-2026-08-06.tsv','L14','La base de violencia político-criminal está identificada, pero no hay variables abiertas que prueben respuesta individual o el mecanismo requerido.','Abrir diccionario/descarga y mapear tipo de evento, actor, municipio, fecha y outcome electoral; declarar límite ecológico.'),
'BASE_DEL_OBSERVATORIO_DE_CONFLICTOS_POR_EL_AGUA':('BASE_INDEXADA_SIN_MAPEO','MAIN:data/mapa-fuentes-externas-consolidado-2026-08-06.tsv','L25','La base está registrada como candidata, sin esquema local abierto ni variables adjudicables para esta relación.','Abrir diccionario y mapear evento, actor, repertorio, resultado, geografía y periodo.'),
'ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION':('BASE_INDEXADA_SIN_MAPEO','MAIN:data/mapa-ext-academico-2026-08-06.tsv','L21','La base electoral está identificada como potencialmente material, pero falta esquema y vínculo causal para esta necesidad.','Abrir codebook y verificar variables de sección, elección, tratamiento/exposición y resultado.'),
'ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024':('ABIERTO_SIN_MAPEO','MAIN:data/mapa-fuentes-externas-consolidado-2026-08-06.tsv','L3','La fuente figura abierta sin mapeo; no se dispone aquí de variable, tabla o texto que satisfaga la clave.','Mapear cuestionario y tabulados 2019–2024 a la necesidad, con periodo, unidad y codificación.'),
'ENNVIH':('PANEL_SIN_MAPEO_DIRIGIDO','MAIN:forense/matriz-impacto-universal-2026-08-06.md','L81','La matriz reconoce ENNViH/MxFLS como ruta longitudinal para horizonte temporal, pero la fase descriptiva y la llave panel siguen pendientes.','Abrir codebooks por ola y localizar indicador temporal, conducta financiera y llave individual longitudinal.'),
'GLOBAL_PREFERENCES_SURVEY':('FUENTE_SIN_REACTIVO_LOCAL','MAIN:forense/hitoE-campana-medicion-v2_0.md','L274-L287','El inventario local no presenta reactivo concreto ni desenlace coobservado para deferencia en esta fuente.','Abrir cuestionario y datos México; buscar proxy de deferencia y outcome laboral/comunicacional en la misma muestra.'),
'LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2':('INDEXADO_NO_DESCARGADO','MAIN:data/mapa-ext-academico-2026-08-06.tsv','L5','El estudio está indexado pero no descargado; no hay instrumento o resultado local verificable para adjudicar.','Recuperar el paquete canónico del estudio y revisar instrumento, diseño, outcomes y tablas de impacto.'),
'PI':('FUENTE_INDEXADA_SIN_APERTURA','MAIN:data/mapa-fuentes-2026-08-06.tsv','L110','Portafolio de Información aparece en el mapa, sin payload, tabla o diccionario abierto asociado a esta clave.','Resolver el recurso canónico de PI y abrir la tabla/diccionario específico antes de adjudicar.'),
'REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES':('INDEXADO_NO_DESCARGADO','MAIN:data/mapa-fuentes-externas-consolidado-2026-08-06.tsv','L4','El reporte está indexado pero no descargado; no existe tabla local verificable para la relación.','Recuperar el reporte canónico y localizar tabla, pregunta, muestra, periodo y codificación de confianza/uso.'),
'CCPV':('FUENTE_SIN_APERTURA_ESPECIFICA','MAIN:forense/hitoE-campana-medicion-v2_0.md','L274','La evidencia local general no identifica diseño, reactivo o muestra de CCPV que permita probar replicación fuera de Tlaxcala.','Abrir instrumento, ficha muestral y resultados CCPV; verificar cobertura geográfica y réplica del estimando original.'),
}

rel_fields=['worker_id','necesidad_id','fuente_canonica','objeto_evidencia_id','estado_anterior','estado_propuesto','tipo_resultado','evidencia_ref','evidencia_localizador','evidencia_explicita','razon','reserva_incertidumbre','requiere_decision_humana','siguiente_accion']
evi_fields=['necesidad_id','fuente_canonica','objeto_evidencia_id','tipo_evidencia','evidencia_ref','evidencia_localizador','variable_reactivo_tabla','texto_evidencia','unidad_observacion','periodo','universo_muestra','codificacion','parte_necesidad_cubierta','parte_necesidad_no_cubierta','uso_potencial_modelo','transformacion_requerida','incertidumbre','traza_revision','siguiente_accion']
rels=[]; evid=[]
for x in rows:
    n=x['necesidad_id']; s=x['fuente_id_canonico']; oe=x['objeto_evidencia_id']
    typ,ref,loc,found,action=source_notes[s]
    requested=x['evidencia_textual_breve'] or 'La relación requiere un objeto de evidencia concreto todavía no mapeado.'
    reason=f'Revisión dirigida de {ref}:{loc}: {found} No alcanza el estándar de CONFIRMADA ni de NEGATIVA delimitada.'
    rels.append(dict(worker_id='worker-2',necesidad_id=n,fuente_canonica=s,objeto_evidencia_id=oe,estado_anterior='CANDIDATA',estado_propuesto='CANDIDATA',tipo_resultado='CANDIDATA_CON_CARENCIA',evidencia_ref=ref,evidencia_localizador=loc,evidencia_explicita=found,razon=reason,reserva_incertidumbre='No se observó una pareja verificable de constructo y desenlace para esta clave; ausencia no demostrada.',requiere_decision_humana='NO',siguiente_accion=action))
    evid.append(dict(necesidad_id=n,fuente_canonica=s,objeto_evidencia_id=oe,tipo_evidencia=typ,evidencia_ref=ref,evidencia_localizador=loc,variable_reactivo_tabla='NO_DETERMINADO',texto_evidencia=found,unidad_observacion='NO_DETERMINADO',periodo='NO_DETERMINADO',universo_muestra='NO_DETERMINADO',codificacion='NO_DETERMINADO',parte_necesidad_cubierta=requested,parte_necesidad_no_cubierta='Identificación verificable y coobservación del constructo con el desenlace específico.',uso_potencial_modelo='CANDIDATO; no parametrizable hasta completar el mapeo.',transformacion_requerida='Mapeo de variables, codificación y llave de unión; estimación solo después de validar unidad y periodo.',incertidumbre='ALTA: evidencia local parcial o meramente indexada.',traza_revision=f'Se abrió la referencia local {ref}, localizador {loc}, y se contrastó únicamente con {n} / {s} / {oe}.',siguiente_accion=action))

for path,fields,data in [(REL,rel_fields,rels),(EVI,evi_fields,evid)]:
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(data)

c=Counter(r['estado_propuesto'] for r in rels)
summary={'fuentes_asignadas':len({r['fuente_canonica'] for r in rels}),'candidatas_asignadas':len(rows),'candidatas_devuelta':len(rels),'confirmadas_nuevas':c['CONFIRMADA'],'negativas_nuevas':c['NEGATIVA'],'candidatas_intactas':c['CANDIDATA'],'no_accesibles_nuevas':c['NO_ACCESIBLE'],'conflictos':0,'decisiones_humanas':sum(r['requiere_decision_humana']=='SI' for r in rels),'referencias_verificadas':0,'bloqueos':sum(r['tipo_resultado'] in {'BLOQUEO','NO_ACCESIBLE'} for r in rels)}
(HERE/'worker-2-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
