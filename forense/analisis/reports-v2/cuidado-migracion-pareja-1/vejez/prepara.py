"""Materializa juicios editoriales explícitos; no infiere veredictos de líneas/rangos."""
import csv, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
REPORT = 'Vejez_y_Cuidado_Intergeneracional_en_México__El_Debilitamiento_del_Seguro_Familiar.md'
original = ROOT/'corpus/reports'/REPORT
with (ROOT/'canon/mapa-dominios-v1_1.tsv').open() as h:
    mapa = [r for r in csv.DictReader(h, delimiter='\t') if r['report']==f'corpus/reports/{REPORT}']
(HERE/'mapa-leido.json').write_text(json.dumps(mapa,ensure_ascii=False,indent=2)+'\n')
# Cada entrada es una decisión editorial escrita después de leer el v1 y el mapa.
# Las listas separan cláusulas materiales; las cifras que no se conservan quedan
# como testimonio literal del v1, nunca como una nueva afirmación firme del v2.
decisiones = [
(1,'SIN-CIFRA','adquisición pendiente','No se verificó una serie primaria que sostenga el año de cruce y TGF; no sustituir natalidad registrada por fecundidad.',[],['Cruce del reemplazo en 2016','TGF 2024 de 1.89 y mínimo histórico']),
(2,'SIN-CIFRA','restricción del proyecto','La conducta PERSONA-60MAS en ENADID2023 está reservada por lista P1; publicación pública no habilita su consumo. La comparación no se adopta.',[],['Proporción60+ 2018 de12.3%','Proporción60+ 2023 de14.7%']),
(3,'SIN-CIFRA','adquisición pendiente','No se leyó proyección primaria y no se mezclan proyección y encuesta; tampoco se acredita el cruce de cohortes.',[],['CONAPO2025 17.1M y12.8%','Proyección2030 de15%','Mayores superan menores15 en2030','Envejecer antes de enriquecerse como comparación']),
(4,'SIN-CIFRA','adquisición pendiente','Esperanza de vida requiere tabla de mortalidad con año y población.',[],['Esperanza vida2024 75.5 y recuperación']),
(5,'SIN-CIFRA','falta de ejecución','No hay RESULT directo del Censo2020 sobre los tres estimandos; el tamaño medio no mide multigeneracionalidad.',[],['82% hogares con mayores nucleares/ampliados','Tamaño medio3.4','28% hogares multigeneracionales']),
(6,'MATIZA','','No equiparar porcentaje de hogares con proporción de personas mayores: explicitar ambos denominadores; valores retirados por falta de tabla directa.',[],['16.8% hogares unipersonales con mayores','Conversión a1.8M personas solas']),
(7,'MATIZA','','Corresidencia y ayuda no identifican preferencia ni seguro eficaz. Oferta y guion son mecanismos rivales, no jerarquía probada.','VEJ-M1'.split(),['Familismo como pilar del cuidado','Ausencia de elección libre','Adaptación ante falla institucional','Seguro familiar como hipótesis']),
(8,'MATIZA','','ENASIC sostiene feminización y parentesco entre receptores con cuidador en hogar; no edad modal ni14h/día ni74% sin apoyo nacional.','R-MUJER R-HIJA R-CONYUGE'.split(),['Cuidadora mayoritariamente mujer','Edad modal mayor50','Hija o cónyuge como parentesco','14h diarias','74% sin terceros']),
(9,'SIN-CIFRA','restricción del proyecto','ENUT2024 reparto_hogar×sexo_edad reservado; total doméstico/cuidados/voluntario no es cuidado de mayores.',[],['67.8% participa cuidados','Mujeres39.7h y hombres18.2h','Brecha21.5h']),
(10,'MATIZA','','La provisión pública es condición a examinar; no hay diseño para ordenar estructura y marianismo causalmente.','VEJ-M1'.split(),['Estructura primaria','Guion asigna cuidado a mujer']),
(11,'SIN-CIFRA','adquisición pendiente','Cuenta satélite valora insumo no remunerado, no pago ni precio del cuidado gerontológico; fuente exacta no leída.',[],['8 billones2024','Aporte mujer82339','Aporte hombre34695']),
(12,'SIN-CIFRA','adquisición pendiente','No hay fuente primaria leída para establecimientos; no equivale a cuidador informal de un mayor.',[],['98.4% mujeres en establecimientos']),
(13,'SIN-CIFRA','adquisición pendiente','No leídos artículos locales originales; heterogeneidad de escala y muestra impide prevalencia nacional. Actualización VEJ-M1 contextual, no sustitución.','VEJ-M1'.split(),['Rango Zarit14.5–66','Obregón48.2 intensa','Guanajuato85.6 sin sobrecarga','Dependencia condiciona carga']),
(14,'SIN-CIFRA','adquisición pendiente','No leída publicación ISSSTE; tres síntomas distintos no son diagnóstico nacional.',[],['ISSSTE52% síndrome','ISSSTE36% depresión','ISSSTE98% ansiedad']),
(15,'SIN-CIFRA','adquisición pendiente','No leídas reglas y padrón2026; no inferir cobertura efectiva de universalidad normativa.',[],['Monto6400 y aumento200','Cobertura14M65+','Universalidad constitucional']),
(16,'MATIZA','','Retirar cifras contributivas sin estudio original; informalidad es vía plausible, no efecto causal exclusivo.',[],['3de10 contributiva','2de10 mujeres','41.5 hombres25.4 mujeres','40% cotiza','Consecuencia directa informalidad']),
(17,'SIN-CIFRA','adquisición pendiente','Estado legislativo temporal no verificado contra texto primario; no prolongar congelamiento por memoria.',[],['Congelamiento Senado desde2020','Reforma marzo2024 sin recursos']),
(18,'SIN-CIFRA','instrumento inadecuado','Demanda potencial no equivale necesidad funcional ni cuidados recibidos; multiplicador sin unidades comparables se retira.',[],['Demanda mayores15veces infancia']),
(19,'SIN-CIFRA','falta de ejecución','Boletín ENASEM2021 leído: población general53+; no localizado88.3 con denominador60+, por tanto no conservar.','VEJ-E1'.split(),['Satisfacción88.3% personas mayores']),
(20,'SIN-CIFRA','no comparabilidad','El porcentaje corresponde a ENASEM2021 y la población CONAPO citada en L12 a2025; no comparten base temporal. El absoluto permanece sin confirmar hasta recuperar población, año y denominador compatibles; esa multiplicación no sostiene ROMPE.','VEJ-E1'.split(),['39.8% soledad60+','Equivalencia10.3M']),
(21,'SIN-CIFRA','adquisición pendiente','No leídos originales etnográficos; contacto/remesa/residencia no sustituyen acompañamiento. Retener como pregunta.',[],['Remesas con soledad rural','Silencio sobre enfermedades','Remesas compran privacidad']),
(22,'SIN-CIFRA','adquisición pendiente','No leído estudio municipal original; inferencia ecológica no identificaría efecto individual.',[],['Vulnerabilidad no concentra en alta migración','Migración no monocausal abandono']),
(23,'SIN-CIFRA','adquisición pendiente','No leer evento como registro vigente del Consejo; cociente nacional no es carga real por médico.',[],['841 médicos2022','15.1M mayores','17mil pacientes por geriatra']),
(24,'SIN-CIFRA','adquisición pendiente','Registro CONACEM y estándar de dotación no leídos; cifras de distinto año no promediables.',[],['850 certificados','Más15mil mayores por geriatra','Meta2770']),
(25,'SIN-CIFRA','adquisición pendiente','ENOE mensual exige documento y universo; participación general no mide sustitución de tiempo de cuidado.',[],['PEA mujer46 hombre74.6 diciembre2024','Brecha28.6']),
(26,'SIN-CIFRA','adquisición pendiente','Sin boletín primario de la ola citada; no usar ola futura para corregir esta cifra.',[],['55.9 informalidad ocupadas marzo2025']),
(27,'MATIZA','','Falta método para participación en PIB. Rechazar su uso como parámetro, sin declarar falsa una cantidad no verificada.',[],['Economía plateada28% PIB','Cautela ante marketing']),
(28,'MATIZA','','Tipología importada útil como pregunta; no hay comparación armonizada que pruebe singularidad mexicana o equivalencia Japón.','VEJ-M1'.split(),['Familismo desprotegido ingreso medio','Semejanza Europa sur y Japón pre2000']),
(29,'SIN-CIFRA','adquisición pendiente','Sin medición primaria65+ pobreza2022 leída; ranking estatal no es tasa de necesidad funcional.',[],['3.9M pobreza2022','49.8% concentra seis entidades','Sur mayor pobreza']),
(30,'SIN-CIFRA','instrumento inadecuado','Batería cognitiva y reporte de familiar fallecido no diagnostican demencia; proyección requiere modelo externo.','VEJ-E1'.split(),['Demencia7–8%60+','1.3M diagnosticados','Triplicación2050']),
(31,'SIN-CIFRA','no comparabilidad','No leídas normas/series armonizadas de Uruguay/Japón; no usar comparación numérica ni temporal como argumento probado.',[],['Uruguay Ley19353','Japón Kaigo2000','Japón1.8%PIB2023','AL20%65+2055','Transición mitad tiempo Europa y mitad PIB']),
(32,'SIN-CIFRA','restricción del proyecto','ENUT2024 reservado; proyección por entidad tampoco verificada. No inferir brecha indígena de muestra electrónica.',[],['Brecha indígena27.3h','Edomex/CDMX21%2030']),
(33,'SIN-CIFRA','adquisición pendiente','No normas estatales primarias ni evaluación de programas leídas; existencia no equivale acceso efectivo.',[],['Jalisco primera ley2024','CDMX/NL/Edomex sistemas','Casa por Casa/Juárez pilotos']),
(34,'SIN-CIFRA','adquisición pendiente','Sin tabulado fuente/denominador ocupacional; costo mensual no es universal.',[],['647mil remunerados','90% mujeres','Cuidadora10121mes']),
(35,'SIN-CIFRA','adquisición pendiente','Sin estimación SHCP leída; no convertir supuesto fiscal en presupuesto recomendado.',[],['SNC1.4%PIB']),
(36,'MATIZA','','Propuestas separadas de eficacia; retirar metas sin base y financiar evaluación de accesibilidad y desenlaces.','R-MUJER'.split(),['Tamizaje/respiro','Formación geriatría100año y duplicación5años','Centros día/domicilio','Ruta0.2–0.3%PIB','Dos ciclos sin presupuesto','Pensión/formalización','Producto/RH/mercado segmentado']),
(37,'SIN-CIFRA','no comparabilidad','Hogares totales y hogares con mayores son universos distintos; no leído estudio chileno.',[],['28% multigeneracional','Chile reducción mitad1982–2017']),
(38,'SIN-CIFRA','restricción del proyecto','ENASEM2024 ola más reciente; actualización pública no levanta reserva. Se elimina cifra.',[],['Escolaridad mujer11.5 hombre8.0']),
]
rows=[]
for n,d,razon,motivo,evidencia,clausulas in decisiones:
    m=next(x for x in mapa if x['id_afirmacion']==f'ASTRA5-U0-VEJEZ-{n:03}')
    for i,c in enumerate(clausulas,1):
        rows.append(dict(id=f'V-{n:03}-{i:02}',mapa_id=m['id_afirmacion'],localizador=m['localizador'],afirmacion=c,dictamen=d,razon_sin_cifra=razon,motivo=motivo,evidencia=evidencia,revision_manual=True))
# Inventario fuera del mapa: materialidad se decide aquí, no por parser.
extras=[
('L81','Urbanidad causa más corresidencia por vivienda','MATIZA','Costo de vivienda es rival plausible; no hay identificación ni comparación urbano/rural aquí.'),
('L81','Discapacidad rural no aumenta corresidencia como urbano','SIN-CIFRA','falta de ejecución: falta estudio original y universo comparable.'),
('L91','Ranking brechas Chiapas/Veracruz/Oaxaca/Guerrero/Michoacán/CDMX','SIN-CIFRA','restricción del proyecto: ENUT2024 no consumida.'),
('L101','Bajo NSE y múltiples dependientes aumentan riesgo','MATIZA','Priorizar evaluación de carga, sin atribuir tasa o efecto causal nacional.'),
('L124','Historia corporativa de seguridad social','SIN-CIFRA','adquisición pendiente: no fuente histórica primaria leída.'),
('L128','Educación/urbanización asociados menor soledad','SIN-CIFRA','falta de ejecución: asociación no calculada en universo declarado.'),
('L133','Pobres familia/pensión; ricos compran cuidado','MATIZA','No fijar conducta por clase; medir capacidad, oferta y elección por separado.'),
('L134','60–74 activos;75+ dependientes','MATIZA','Edad es segmento, no criterio diagnóstico individual; medir capacidad funcional.'),
('L135','Mujeres más pobres/dependientes/cuidadoras','MATIZA','ENASIC sostiene cuidadora mujer entre receptores elegibles; no prueba pobreza o dependencia por sexo.'),
('L137','Rural mayor soledad efectiva','SIN-CIFRA','falta de ejecución: ENASIC no tiene localidad utilizable en este CALC.'),
('L138','Religiosidad sin evidencia segmentada','SIN-CIFRA','falta de ejecución: espiritualidad en conveniencia2025 no identifica religiosidad nacional.'),
('L140','Exposición global y apps aplican minoría urbana','MATIZA','Muestra electrónica no permite determinar tamaño nacional de exclusión digital.'),
('L142','Pensión como rasgo distintivo mexicano','MATIZA','No declarar exclusiva sin comparación armonizada.'),
('L147','Independencia puede patologizar corresidencia','MATIZA','Evaluar autonomía decisional y suficiencia del cuidado, no ideal residencial importado.'),
('L159','Formación geriátrica garantiza alto impacto bajo costo','MATIZA','Eficacia y costo no establecidos; recomendación con evaluación.'),
('L164','5R como intervención eficaz','MATIZA','Es marco de organización, no estimación de beneficio.'),
('L173','Licencias/conciliación laboral','MATIZA','Propuesta evaluable, no efecto probado ni estado legal actualizado.'),
('L185','Zarit/CESD no validadas rural/indígena','SIN-CIFRA','adquisición pendiente: no estudios de validación leídos; no afirmar invalidez general.'),
('L188','Hijos cuidan menos que antes','SIN-CIFRA','falta de ejecución: requerir panel comparable, no cortes residenciales.'),
('L191','Dar dinero basta o familia elimina necesidad estatal','MATIZA','No son conclusiones justificadas por observables financieros y familiares.'),
('L26','Soledad/aislamiento se asocian depresión y deterioro cognitivo','SIN-CIFRA','adquisición pendiente: falta estudio específico longitudinal y definición de los tres desenlaces.'),
('L80','Hogares unipersonales de mayores crecen','SIN-CIFRA','no comparabilidad: un corte no identifica tendencia comparable.'),
('L96','Cuidado informal produce estrés crónico','MATIZA','Se conserva como mecanismo compatible; no daño causal universal identificado.'),
('L125','Cuidado persiste con recursos y matiza adaptación','SIN-CIFRA','falta de ejecución: requiere recursos/oferta comparables y cuidado observado.'),
('L147','Japón Meiji hijo mayor responsable y encuestas tensión causaron reforma','SIN-CIFRA','adquisición pendiente: no texto legal ni evaluación histórica primaria leídos.'),
('L147','Seguro japonés transfirió deber hijas/nueras a servicios','SIN-CIFRA','adquisición pendiente: no evaluación de sustitución y distribución leída.'),
('L160','Médicos familiares/enfermería como alternativa de atención','MATIZA','Propuesta evaluable; no equivalencia de eficacia ni dotación garantizada.'),
('L167','Mujeres acceden a pensión solo por viudez','SIN-CIFRA','falta de ejecución: no distribución de fuente/derecho propio/derivado calculada.'),
]
for i,(l,c,d,m) in enumerate(extras,1):rows.append(dict(id=f'V-EX-{i:02}',mapa_id='',localizador=l,afirmacion=c,dictamen=d,razon_sin_cifra=m.split(':')[0] if d=='SIN-CIFRA' else '',motivo=m,evidencia=[],revision_manual=True))
# Revisión manual: porcentaje y absoluto no confirmados; no se cruzan bases temporales.
porcentaje=next(x for x in rows if x['id']=='V-020-01')
porcentaje.update(dictamen='SIN-CIFRA',razon_sin_cifra='falta de ejecución',motivo='No localizado tabulado/reactivo60+ que confirme39.8%; ausencia no refuta el porcentaje.')
feminizacion=next(x for x in rows if x['id']=='V-008-01')
feminizacion.update(dictamen='CONFIRMA',motivo='R-MUJER confirma mayoría femenina del proveedor principal entre receptores60+ con cuidador del hogar pareado; confirma solo esta descripción condicionada, no un perfil modal nacional completo.')
(HERE/'decisiones.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(HERE/'lectura.json').write_text(json.dumps(dict(original=str(original.relative_to(ROOT)),sha256=hashlib.sha256(original.read_bytes()).hexdigest(),bloques_leidos=['L1–36 resumen','L37–75 marco/evidencia','L76–120 patrones','L121–150 causas/segmentación/comparación','L151–199 recomendaciones/auditoría'],mapa_filas=len(mapa),inventario_fuera_mapa=len(extras),criterio_dedup='Repeticiones del TLDR, patrones y síntesis se vinculan a la misma tesis; cláusulas independientes se separan.',corte='11602de8',estado='LEÍDO COMPLETO, decisiones editoriales explícitas'),ensure_ascii=False,indent=2)+'\n')
