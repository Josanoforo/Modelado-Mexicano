"""Contratos documentales de ENIGH 2024 y ENCIG 2025; sin microdatos ni ola ENOE 2026T1 reservada."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Mérito__Movilidad_Social_y_Desigualdad_en_México__Actualización_2025-2026.md"
FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]

ENIGH_DOC = "SIN-ID:enigh2024_reporte_resultados.pdf|6b091e2d640b6682ca568203637d2a327fbcae950ba7ef66c441c5970568903d|reporte 23/25 p.11, gráfica 2; sin registro en main ni rama; copia física local"

REPORT_SHA = hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()

ENIGH = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L18; repetición L4,L47-L48,L55",
    tier_report="sin rótulo explícito",
    clase="cifra publicada y comparación contrafactual contable",
    limite_inferencial="La diferencia descriptiva con/sin transferencias no identifica el efecto causal de programas sociales, pensiones o salario mínimo. La serie 2016/2022 requiere comparabilidad de cuestionario y precios separada.",
    conducta_unidad_universo="Distribución por deciles de hogares del ingreso corriente promedio trimestral; México, ENIGH nueva serie 2024.",
    instrumento_ola="ENIGH 2024 nueva serie, reporte de resultados 23/25 de 30-jul-2025",
    documento_id_hash_pagina=ENIGH_DOC + ";enigh2024_diseno_muestral_pdf|2d2a5c0fd47a92d7c2d044300b47cf15330f9902c8b50975dd1e4eab35395229|main",
    pregunta_textual_codigo_respuestas="Indicador derivado de ingreso corriente trimestral por hogar; no existe reactivo único Gini. La gráfica 2 distingue explícitamente 'Con transferencias' y 'Sin transferencias'.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="El reporte público fija cifra, unidad y método contable; PDF físico verificado y sin registrar en manifiesto. Dato y diseño ENIGH 2024 están en main, pero reporte de cifra no; falta reproducción/RESULT compatible.",
    datos_id_estado="enigh2024_nc_csv|7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d|main, microdato NO ABIERTO",
    reserva="Permiso y apertura en CAJA; U0 no abrió microdato. La atribución causal queda fuera del contrato descriptivo.",
    gen2_existente="ENIGH 2024 en main como corpus; ningún RESULT de Gini 2024 con/sin transferencias identificado al corte.",
    propietario="ASTRA5-MESA-MOVILIDAD",
    prioridad="2",
)

ENCIG = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L26; repetición L5,L48-L49",
    tier_report="sin rótulo explícito",
    clase="cifra publicada y tesis interpretativa",
    limite_inferencial="Percepción de frecuencia y confianza declarada no miden corrupción objetiva ni demuestran que las palancas determinen el éxito. El 15.6% de victimización usa solo personas con trámite/pago/servicio/contacto y requiere derivación separada.",
    conducta_unidad_universo="Persona seleccionada de 18+ en vivienda particular de ciudades de 100 mil habitantes o más; ENCIG 2025, dominio nacional urbano alto, no toda la población de México.",
    instrumento_ola="ENCIG 2025, captación 31-oct a 16-dic-2025",
    documento_id_hash_pagina="encig25_cuestionario_pdf|807196d6aba5ee584fcc3710b6f01c6a43970b91c7f3c380f68109a4bd16bd33|main;encig25_estructura_base_datos_pdf|09e1b19bcb165979406865360bfdec95a9767640c58565b64d405ceb04e623a2|main;SIN-ID:encig2025_diseno_muestral.pdf|de74a89623696e54e2d409a5cb5ae2b41dcd54a73c9deef1102b5793d875175e|sin registro en main ni rama; copia física local",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Cuestionario, descriptor y dato ENCIG 2025 en main con SHA físico coincidente; diseño y tabulado oficial con SHA físico sin registrar en manifiesto. Hasta integrar documentos en main y cotejar denominador, no es MEDIBLE-EN-CORPUS ni RESULT propio.",
    datos_id_estado="encig_2025_encig25_base_datos_dbf|fa92a6ea4119ff1b64986a10b7939ccc1ef02b2af3c127a38c93bed830d6fe59|main, físico COINCIDE SHA, microdato NO ABIERTO",
    reserva="Términos de Libre Uso INEGI; verificar autorización de apertura en CAJA. U0 no abrió ni descargó microdato.",
    gen2_existente="Sin RESULT ENCIG 2025 para P3_2/P11_1_04 identificado en main al corte; no usar ENCIG 2023 ni ENVIPE como misma pregunta.",
    propietario="ASTRA5-U3",
    prioridad="2",
)

CPI = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L26; repetición L5,L48-L49",
    tier_report="sin rótulo explícito",
    clase="índice compuesto publicado",
    limite_inferencial="El IPC agrega percepciones de expertos y empresarios sobre corrupción del sector público. No mide experiencia de víctimas ENCIG, corrupción comprobada ni causalidad de mérito, y el rango depende de los países incluidos.",
    conducta_unidad_universo="México como país, comparado con 182 países y territorios; no muestra individual de mexicanos.",
    instrumento_ola="Transparency International, Índice de Percepción de la Corrupción 2025, publicado 10-feb-2026",
    documento_id_hash_pagina="SIN-ID:transparency_cpi2025_mexico.html|988f7f990613934e5344a1468544cfa6f8af21ffe2d1a16aca66ac6864434977|ficha México, captura física 23-sep-2026; sin registro en main;https://www.transparency.org/en/countries/mexico; metodología https://www.transparency.org/en/news/how-cpi-scores-are-calculated",
    pregunta_textual_codigo_respuestas="No hay reactivo único de ciudadano. IPC: combinación estandarizada de al menos tres fuentes entre trece encuestas/evaluaciones de expertos y empresarios; escala 0 alta corrupción percibida a 100 muy baja.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Ficha primaria México cotejada y captura física con SHA; falta id documental en main. La página es mutable; año 2025 verificado en serie de la ficha. No hay RESULT propio de U0 ni microdato abierto.",
    datos_id_estado="Fuente agregada TI en web; tabla completa no descargada ni registrada; sin microdato U0.",
    reserva="TI permite usar resultados IPC con atribución bajo CC BY-ND 4.0, sin alterar el contenido; conservar enlace y año. Captura local no redistribuida.",
    gen2_existente="Sin RESULT propio; 27/100 y rango 141/182 publicados directamente por TI para México 2025.",
    propietario="ASTRA5-MESA-DOCUMENTAL / ASTRA5-U3",
    prioridad="2",
)

POBREZA = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L16; repetición L4,L47-L48,L54-L55",
    tier_report="sin rótulo explícito",
    clase="medición oficial de pobreza multidimensional publicada",
    limite_inferencial="Pobreza multidimensional combina bienestar económico y derechos; no es Gini, movilidad intergeneracional ni pobreza solo por ingresos. El cambio agregado no identifica por sí solo el efecto causal del salario mínimo o de un programa.",
    conducta_unidad_universo="Personas residentes en México, escala nacional; ENIGH 2024 y metodología de pobreza multidimensional vigente.",
    instrumento_ola="INEGI Pobreza Multidimensional 2024, reporte de resultados 27/25 y nota técnica, 13-ago-2025",
    documento_id_hash_pagina="SIN-ID:pm2024_reporte_resultados.pdf|4da28fe9a3d74633d0275e4c5567576caade48b57aa12b81fecfd9db6781a4f9|reporte 27/25 p.9; SIN-ID:pm2024_nota_tecnica.pdf|aea6eb795d71c40ee8c343fee70302c5637a44a13de9b97b53aca7c67031af16|pp.2-4,18-19; dos copias físicas locales, sin registro en main",
    pregunta_textual_codigo_respuestas="Indicador derivado de ingreso corriente total per cápita y carencias sociales conforme a metodología CONEVAL retomada por INEGI; no hay pregunta única ni es equivalente a Gini ENIGH.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Reporte y nota técnica oficiales leídos y verificados por SHA físico; falta id documental en manifiesto y RESULT de reproducción. Se cierra la atribución del agregado publicado, no el cálculo propio ni su causa.",
    datos_id_estado="enigh2024_nc_csv|7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d|main, microdato NO ABIERTO; indicadores derivados de pobreza no reconstruidos por U0",
    reserva="Términos de Libre Uso INEGI para documentos públicos; registro por MESA-DOCUMENTAL. U0 no abrió microdato ni editó manifiesto.",
    gen2_existente="Sin RESULT propio de pobreza multidimensional 2024 identificado en main.",
    propietario="ASTRA5-MESA-MOVILIDAD / ASTRA5-MESA-DOCUMENTAL",
    prioridad="2",
)

CEEY = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L12; repetición L4,L38,L47-L48",
    tier_report="sin rótulo explícito",
    clase="transición intergeneracional publicada",
    limite_inferencial="La matriz de recursos económicos de origen y destino no mide ingreso monetario o pobreza multidimensional ni sigue toda la vida de cada persona. Son asociaciones observacionales; la educación heredada no prueba efecto causal de escuela o mérito individual.",
    conducta_unidad_universo="Personas de 25–64 años en México, ESRU-EMOVI 2023 básica, representativa nacional y para cinco regiones; 17 843 entrevistas totales, 14 924 observaciones analíticas de Figuras 3/4.",
    instrumento_ola="CEEY ESRU-EMOVI 2023, Informe de movilidad social en México 2025 (comunicado 30-jun-2025)",
    documento_id_hash_pagina="SIN-ID:ceey_movilidad2025.pdf|ba57a707210c2295b5b138fc310ca10b34fbcd1ae19f7f34c57b084f7653c758|pp.17,20-21; PDF local de enlace oficial https://ceey.org.mx/informe-de-movilidad-social-en-mexico-2025/ sin registro en main",
    pregunta_textual_codigo_respuestas="CEEY deriva quintiles del índice de recursos económicos del hogar de origen recordado y del hogar actual; educación máxima de padres frente a educación profesional del entrevistado. Preguntas/códigos y ponderación exacta requieren documentación de ESRU-EMOVI 2023 antes de reproducción.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="El informe primario fija cifra, condicionamiento, población y n analítica, con PDF físico y SHA verificados. Microdato, instrumento/código y RESULT no tienen id/cotejo U0; el cierre es del agregado publicado, no de una reproducción propia.",
    datos_id_estado="ESRU-EMOVI 2023 disponible por enlace CEEY, SIN-ID de manifiesto U0; microdato NO DESCARGADO NI ABIERTO.",
    reserva="Informe D.R. © CEEY 2025 sin licencia explícita para redistribuir PDF; copia local solamente. Apertura de ESRU-EMOVI requiere carril autorizado; U0 no abrió microdato.",
    gen2_existente="Sin RESULT ESRU-EMOVI 2023 compatible identificado en main.",
    propietario="ASTRA5-MESA-MOVILIDAD / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="MESA-DOCUMENTAL registra referencia, condición y SHA sin redistribuir PDF; MESA-MOVILIDAD coteja instrumento, índice/ponderador y reproduce solo con autorización en CAJA.",
    prioridad="2",
)

CEEY_FIN = dict(
    report=REPORT,
    report_sha256=REPORT_SHA,
    localizador="L13; repetición L10-L12",
    tier_report="sin rótulo explícito",
    clase="asociación publicada entre inclusión financiera parental y destino económico",
    limite_inferencial="Son probabilidades descriptivas condicionadas simultáneamente por origen en grupos 1+2 y tenencia financiera parental. No equivalen a la celda Q1→Q5 del informe general, ni demuestran efecto causal de producto financiero sobre movilidad.",
    conducta_unidad_universo="Adultos 25–64 ESRU-EMOVI 2023 cuyo hogar de origen estaba en grupos 1 o 2 (40% inferior) del índice de recursos económicos; Figura 11 usa 16 205 observaciones analíticas del cuestionario básico, no toda la muestra.",
    instrumento_ola="CEEY ESRU-EMOVI 2023, Informe de movilidad social en México 2025: la ruta hacia la inclusión financiera",
    documento_id_hash_pagina="SIN-ID:ceey_inclusion_financiera2025.pdf|9421e24efded34ee752d89c1a80133ab35330d8ebe5961e47f005d7a5ccb4125|p.36 Figura 11 y notas; PDF local de enlace oficial https://ceey.org.mx/informe-movilidad-social-en-mexico-2025-inclusion-financiera/ sin registro en main",
    pregunta_textual_codigo_respuestas="Inclusión parental: al menos cuenta de ahorro, tarjeta de crédito, cuenta/tarjeta de nómina o cuenta de cheques según nota Figura 11; destino grupo 5 del índice de recursos económicos. Reactivo, códigos, construcción y factor exactos por cotejar.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="El segundo informe CEEY publica cifra, grupo de origen, condición parental, población y n analítica con PDF físico/hash; microdato, instrumento y RESULT no cotejados por U0. Se cierra el agregado, no causalidad ni reproducción.",
    datos_id_estado="ESRU-EMOVI 2023 cuestionario básico disponible por CEEY, SIN-ID de manifiesto U0; microdato NO DESCARGADO NI ABIERTO.",
    reserva="Informe D.R. © CEEY 2025 sin licencia de redistribución explícita; copia local solamente. Apertura de microdato requiere carril autorizado.",
    gen2_existente="Sin RESULT ESRU-EMOVI 2023 compatible identificado en main.",
    propietario="ASTRA5-MESA-MOVILIDAD / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="MESA-DOCUMENTAL registra referencia, condiciones y SHA; MESA-MOVILIDAD coteja pregunta parental, grupo 1+2 y ponderación antes de reproducir en CAJA autorizada.",
    prioridad="2",
)

ROWS = [
    ENIGH | dict(id_afirmacion="ASTRA5-U0-MER-004", texto_vigente="El Gini del ingreso corriente por hogar con transferencias fue 0.391 en ENIGH 2024.", componente_contrastable="Gini publicado con transferencias recibidas incluidas: 0.391; 0.402 en 2022 y 0.449 en 2016 se conservan como comparadores, sin dictamen de serie.", siguiente_operacion="Registrar publicación en main, reproducir fórmula del Gini en CAJA y tratar la serie 2016/2022 con su propio contrato de comparabilidad."),
    ENIGH | dict(id_afirmacion="ASTRA5-U0-MER-005", texto_vigente="Sin considerar transferencias, el Gini contable ENIGH 2024 habría sido 0.450.", componente_contrastable="Gini simulado sin transferencias recibidas: 0.450 frente a 0.391 con ellas, misma fuente y año.", siguiente_operacion="Registrar publicación en main y verificar qué rubros se restan en la simulación; no atribuir 0.059 a un programa o salario mínimo causalmente."),
    ENCIG | dict(id_afirmacion="ASTRA5-U0-MER-006", texto_vigente="En ENCIG 2025, 84.1% de la población consideró frecuentes los actos de corrupción.", componente_contrastable="P3_2=1 Muy frecuentes o 2 Frecuentes; proporción publicada 84.1% del dominio urbano alto 18+.", documento_id_hash_pagina=ENCIG["documento_id_hash_pagina"] + ";SIN-ID:encig2025_boletin.pdf|6515cb698a8a7f0821a225827ac2402d06cd6405cabf76208f0d6c529b29eaa4|p.3; registro pendiente", pregunta_textual_codigo_respuestas="P3.2: 'Por lo que usted sabe, en (ESTADO) estas prácticas son:' P3_2 1 Muy frecuentes, 2 Frecuentes, 3 Poco frecuentes, 4 Nunca se dan, 9 No sabe/no responde. FAC_P18; verificar tratamiento publicado de 9.", siguiente_operacion="U3 coteja P3_2=1/2 con FAC_P18 y diseño; no confundir percepción con victimización 15.6% ni generalizar fuera de ciudades 100 mil+."),
    ENCIG | dict(id_afirmacion="ASTRA5-U0-MER-007", texto_vigente="La confianza en gobierno federal fue 46.5% en ENCIG 2025; el report la compara con 59.1% en 2023.", componente_contrastable="P11_1_04=1 Mucha o 2 Algo de confianza en Presidencia de la República y Secretarías de Estado; presentación 2025 p.50 publica 46.5%.", documento_id_hash_pagina=ENCIG["documento_id_hash_pagina"] + ";SIN-ID:encig2025_principales_resultados.pdf|476cf06ee8cb18727f2326c0d80e5f113ca3554a0851f89f3414ab1a03113548|p.50; registro pendiente", pregunta_textual_codigo_respuestas="P11.1 item 04 'Presidencia de la República y Secretarías de Estado': P11_1_04 1 Mucha confianza, 2 Algo, 3 Algo de desconfianza, 4 Mucha desconfianza, 5 No aplica, 9 No sabe/no responde. FAC_P18; cotejar denominador publicado.", siguiente_operacion="U3 reproduce 46.5% con P11_1_04 y diseño; localizar/registrar presentación ENCIG 2023 y verificar mismo reactivo/universo antes de contratar 59.1% o caída de 12.6 puntos."),
    CPI | dict(id_afirmacion="ASTRA5-U0-MER-008", texto_vigente="México obtuvo 27/100 y rango 141/182 en el IPC 2025.", componente_contrastable="Ficha primaria TI México: puntuación 27/100, cambio +1 respecto de 2024 y posición 141/182 en 2025.", siguiente_operacion="MESA-DOCUMENTAL registra referencia, licencia y SHA de captura sin modificar manifiesto desde U0; U3 conserva 27/100 separado de ENCIG 84.1%, 15.6% y de la tesis causal de palancas."),
    ENCIG | dict(id_afirmacion="ASTRA5-U0-MER-009", texto_vigente="En ENCIG 2025, 15.6% de las personas con trámite, pago, solicitud de servicio o contacto con autoridad durante 2025 experimentó corrupción.", clase="prevalencia condicional publicada", componente_contrastable="Boletín p.3: 15.6% entre personas con interacción durante 2025; presentación pp.41-42: 15 642 por 100 mil personas de ese denominador, redondeado a 15.6%.", limite_inferencial="La cifra no es proporción de toda la población, ni frecuencia percibida P3_2, ni incidencia por trámite ponderada con FAC_TRA. No prueba que corrupción determine creencias de mérito. La fórmula exacta para reconstrucción sigue pendiente.", conducta_unidad_universo="Personas de 18+ en viviendas particulares de ciudades de 100 mil habitantes o más que hicieron trámite, pago, solicitud de servicio o contacto con autoridad durante 2025; ENCIG 2025.", documento_id_hash_pagina=ENCIG["documento_id_hash_pagina"] + ";SIN-ID:encig2025_boletin.pdf|6515cb698a8a7f0821a225827ac2402d06cd6405cabf76208f0d6c529b29eaa4|p.3;SIN-ID:encig2025_principales_resultados.pdf|476cf06ee8cb18727f2326c0d80e5f113ca3554a0851f89f3414ab1a03113548|pp.41-42; registro pendiente", pregunta_textual_codigo_respuestas="Sección VI P6.1 registra hasta 23 tipos de interacción; sección VIII P8.3 pregunta solicitud o insinuación de beneficio. Estructura: P8_3_1/2/3 (1 Sí, 2 No, 9 NS/NR), FAC_P18 para personas. Unión exacta, filtros, faltantes y estimación oficial por verificar; FAC_TRA no es peso de persona.", dictamen_razon="Cifra y denominador publicados por INEGI, boletín/presentación físicos con SHA verificado sin id de manifiesto. Contrato de agregado publicado cerrado; reconstrucción en microdato y RESULT siguen pendientes. No se abrió el ZIP.", gen2_existente="Sin RESULT ENCIG 2025 para victimización condicionada; microdato y descriptor en main sin apertura U0.", siguiente_operacion="MESA-DOCUMENTAL registra boletín/presentación; U3 fija fórmula, filtros de interacción, no aplica y no respuesta con FAC_P18 antes de calcular en CAJA; no derivar 15.6 de P3_2 o FAC_TRA."),
    POBREZA | dict(id_afirmacion="ASTRA5-U0-MER-010", texto_vigente="La pobreza multidimensional nacional fue 29.6% en 2024, equivalente a 38.5 millones de personas.", componente_contrastable="Reporte INEGI 27/25 p.9: 29.6% y 38.5 millones, personas, México 2024.", siguiente_operacion="MESA-DOCUMENTAL registra reporte y nota técnica; MESA-MOVILIDAD reproduce indicador en CAJA sólo con permiso y diseño, manteniendo Gini, movilidad y atribución causal separados."),
    POBREZA | dict(id_afirmacion="ASTRA5-U0-MER-011", texto_vigente="La pobreza extrema multidimensional fue 5.3% en 2024, equivalente a 7.0 millones de personas.", componente_contrastable="Reporte INEGI 27/25 p.9: pobreza extrema 5.3% y 7.0 millones; subgrupo de pobreza multidimensional, no suma adicional a 29.6%.", siguiente_operacion="MESA-DOCUMENTAL registra reporte y nota; MESA-MOVILIDAD verifica umbrales de pobreza extrema y reproduce indicador en CAJA sólo con permiso, sin sumarlo a 29.6%."),
    POBREZA | dict(id_afirmacion="ASTRA5-U0-MER-012", texto_vigente="La pobreza multidimensional nacional pasó de 43.2% en 2016 a 29.6% en 2024, una disminución publicada de 13.7 millones de personas.", componente_contrastable="Reporte 27/25 p.9 publica serie 2016-2024 y caída absoluta de 13.7 millones; nota técnica pp.2-4,18-19 documenta la continuidad metodológica declarada por INEGI y cambios de ENIGH 2024.", conducta_unidad_universo="Personas residentes en México; serie bienal nacional 2016-2024 de pobreza multidimensional. Comparación descriptiva de dos cortes, no panel individual.", limite_inferencial="INEGI documenta continuidad y equivalencias, pero hubo cambios de preguntas en ENIGH 2024; la objeción académica citada por el report requiere fuente y evaluación separadas. No atribuir el cambio a salarios o transferencias sin identificación.", documento_id_hash_pagina=POBREZA["documento_id_hash_pagina"].replace("reporte 27/25 p.9", "reporte 27/25 pp.3-4,9"), siguiente_operacion="MESA-DOCUMENTAL registra ambas piezas; MESA-MOVILIDAD coteja nota técnica y objeción IBERO por indicador, no confunde caída agregada con movilidad individual o efecto causal."),
    CEEY | dict(id_afirmacion="ASTRA5-U0-MER-013", texto_vigente="De quienes nacieron en el quintil inferior de recursos económicos, 50% permanecía en ese quintil en la adultez.", componente_contrastable="Informe CEEY 2025 Figura 3 p.20: P(quintil actual 1 | quintil origen 1)=50% entre adultos 25–64 de la base analítica ESRU-EMOVI 2023.", pregunta_textual_codigo_respuestas="Matriz origen/destino del índice de recursos económicos del hogar, cinco grupos de 20%; fila origen grupo 1, columna destino grupo 1. n analítica total 14 924, n de fila/ponderador por cotejar."),
    CEEY | dict(id_afirmacion="ASTRA5-U0-MER-014", texto_vigente="De quienes nacieron en el quintil inferior de recursos económicos, 2% alcanzó el quintil superior en la adultez.", componente_contrastable="Informe CEEY 2025 Figura 3 p.20: P(quintil actual 5 | quintil origen 1)=2% entre adultos 25–64 de la base analítica ESRU-EMOVI 2023.", pregunta_textual_codigo_respuestas="Matriz origen/destino del índice de recursos económicos del hogar, cinco grupos de 20%; fila origen grupo 1, columna destino grupo 5. n analítica total 14 924, n de fila/ponderador por cotejar."),
    CEEY | dict(id_afirmacion="ASTRA5-U0-MER-015", texto_vigente="El 9% de adultos cuyos padres estudiaron hasta primaria o menos alcanzó educación profesional.", clase="transición educativa publicada", componente_contrastable="Informe CEEY 2025 Figura 4 p.21: P(educación profesional | máximo de padres primaria o menos)=9%; no es exactamente 10% aunque el report redondea a 1 de cada 10.", pregunta_textual_codigo_respuestas="Máximo nivel educativo de padres ≤primaria frente a nivel profesional alcanzado por persona entrevistada 25–64; categorías/códigos exactos por cotejar."),
    CEEY | dict(id_afirmacion="ASTRA5-U0-MER-016", texto_vigente="El 63% de adultos con padres de educación profesional alcanzó educación profesional, alrededor de siete veces la probabilidad del grupo con padres hasta primaria.", clase="transición educativa publicada", componente_contrastable="Informe CEEY 2025 Figura 4 p.21: P(profesional | padres profesionales)=63% frente a 9% si padres ≤primaria; cociente descriptivo 7, sin interpretación causal.", pregunta_textual_codigo_respuestas="Máximo nivel educativo de padres profesional frente a nivel profesional alcanzado por persona entrevistada 25–64; categorías/códigos exactos por cotejar."),
    CEEY_FIN | dict(id_afirmacion="ASTRA5-U0-MER-017", texto_vigente="Entre adultos con origen en grupos 1+2 y padres con inclusión financiera, 13% alcanzó el grupo 5 de recursos económicos.", componente_contrastable="CEEY inclusión financiera Figura 11 p.36: P(destino grupo 5 | origen grupos 1+2, padres con producto financiero)=13%; n analítica total 16 205.", siguiente_operacion="Registrar segundo informe; U3/MESA-MOVILIDAD fija pregunta parental y denominador condicionado antes de reproducir. No atribuir 13% a todos los adultos."),
    CEEY_FIN | dict(id_afirmacion="ASTRA5-U0-MER-018", texto_vigente="Entre adultos con origen en grupos 1+2 y padres sin inclusión financiera, 4% alcanzó el grupo 5 de recursos económicos.", componente_contrastable="CEEY inclusión financiera Figura 11 p.36: P(destino grupo 5 | origen grupos 1+2, padres sin producto financiero)=4%; CEEY resume la diferencia como 3.3 veces; 13% y 4% son cifras redondeadas.", siguiente_operacion="Registrar segundo informe; U3/MESA-MOVILIDAD coteja grupo de comparación, reactivo y ponderación; no leer razón 3.3 como efecto causal ni deduplicar con Q1→Q5 2%."),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
