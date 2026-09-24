"""Hitos documentales del procedimiento CED art. 34; sin inferencia penal."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Ausencia_sin_certeza__duelo_y_pérdida_ambigua_en_familias_de_personas_desaparecidas_en_México.md"
FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]
SHA = hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()
BASE = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L18; desarrollo del procedimiento art. 34",
    tier_report="sin rótulo explícito",
    clase="acto institucional documentado",
    limite_inferencial="Documento del Comité contra la Desaparición Forzada, no sentencia penal ni decisión de la Asamblea General. La decisión de remitir la cuestión no prueba por sí sola un delito concreto, la culpabilidad de funcionarios o un efecto psicológico individual. El anuncio del presidente del 4/abr/2025 requiere pieza propia.",
    conducta_unidad_universo="Expediente México ante Comité CED en aplicación de artículo 34 de la Convención; unidad acto procesal, no encuesta ni persona desaparecida.",
    instrumento_ola="CED/C/MEX/A.34/D/1, decisión adoptada en 30º período 9-19/mar/2026, distribuida 17/abr/2026; párrafos 33-37 y 122-123",
    documento_id_hash_pagina="SIN-ID:ced_mex_a34_2026.pdf|39fe6ee50aba61739e3f9ff856498f2b05b67f9675c4afcb66b080cc1fa8a6db|pp.6,20 §III y §V;https://docstore.ohchr.org/SelfServices/FilesHandler.ashx?enc=%2BSInD1MGWlfLOwSnMLOch2VA6hZ%2Fe7GNMdQpcCejvaExNjNVcpZGWD0vB0cdB4VOcsB4aXawakh1Za19rldXZA%3D%3D;HTML-oficial:6bbabd7da0a84eae71351bf49e50646f973f0e866f78b7f21aa36e6e99074a66",
    pregunta_textual_codigo_respuestas="No cuestionario: lectura de párrafos de decisión ONU y fecha de distribución. Los actos de solicitud, respuesta, examen y remisión son etapas separadas.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Documento primario ONU completo PDF físico con símbolo, fecha, párrafo y SHA; copia HTML oficial previa con SHA distinta. No id en manifiesto por perímetro U0 ni RESULT analítico.",
    datos_id_estado="Documento público agregado; ningún microdato abierto ni RESULT compatible.",
    reserva="PDF/HTML oficiales conservados para lectura local; condiciones de redistribución por MESA-DOCUMENTAL. No convertir activación/remisión en condena, ni afirmar decisión posterior de Asamblea sin acto específico.",
    gen2_existente="No existe RESULT; afirmación es acto documental.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar PDF/HTML, versión/condiciones/SHA; localizar anuncio 4/abr/2025 y eventual acto de Asamblea por símbolo y fecha antes de actualizar estado procesal.",
    prioridad="3",
)
HEEKE = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L11-L12; comparación colombiana",
    tier_report="sin rótulo explícito",
    clase="estudio transversal de síntomas de duelo prolongado",
    limite_inferencial="Muestra colombiana de desplazados vinculados a la ONG Tierra y Vida, no México ni muestra probabilística de todos los familiares de desaparecidos. El comparador es muerte en conflicto, 92.8% homicidio, no homicidio exclusivamente. PG-13 estudia criterio de síntomas en 2012, no diagnóstico DSM-5-TR actual. Asociación de esperanza y severidad no identifica efecto causal ni interviene sobre esperanza; medias por cinco categorías no son monótonas y celdas moderada/mucha esperanza tienen n=4/n=6.",
    conducta_unidad_universo="Entrevistas estructuradas cara a cara sep-dic/2012 en cuatro distritos colombianos: 295 personas analíticas, 73 pérdida por desaparición forzada y 222 por muerte relacionada con conflicto, de listado de ONG Tierra y Vida.",
    instrumento_ola="Heeke, Stammel y Knaevelsrud, J Affect Disord 173:59–64 (2015), DOI 10.1016/j.jad.2014.10.038; reproducción íntegra como artículo IV de tesis Heeke 2018, Freie Universität Berlin",
    documento_id_hash_pagina="SIN-ID:heeke_dissertation_2018.pdf|9ec6104d4911021e2e4f086fa6273f62f656a910febb413a11e3c0f0a8754d98|Article IV pp.90-97 Tablas 9-12/Figura5;https://refubium.fu-berlin.de/bitstream/handle/fub188/22553/Dissertation_Heeke.pdf?isAllowed=y&save=y&sequence=3;PMID:25462397",
    pregunta_textual_codigo_respuestas="PG-13 entrevista estructurada: síntomas separación y cognitivo-emocionales, duración ≥6 meses, deterioro funcional; esperanza de vida del desaparecido pregunta 0 nada a 4 mucho, solo grupo desaparecido. Depression HSCL y PTSD PCL-C son medidas distintas.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo IV íntegro en tesis primaria de autora con PDF/SHA físicos; muestra, instrumento, tabla y contraste leídos. Falta id documental/condiciones específicas y RESULT propio.",
    datos_id_estado="Entrevistas individuales no abiertas/descargadas U0; no RESULT propio.",
    reserva="Tesis institucional para lectura local; condiciones de redistribución por MESA-DOCUMENTAL. No usar tasa colombiana como prevalencia mexicana, ni asociación de esperanza como tratamiento psicológico.",
    gen2_existente="Sin RESULT PG-13/esperanza compatible en main.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar tesis, artículo final, DOI, condiciones y SHA; cotejar instrumento PG-13/selección, buscar evidencia mexicana específica antes de extrapolar o recomendar atención.",
    prioridad="3",
)
ALMANZA = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L9; evidencia cualitativa Tamaulipas",
    tier_report="sin rótulo explícito",
    clase="entrevistas cualitativas fenomenológico-interpretativas",
    limite_inferencial="Cinco madres contactadas por una asociación de familiares en Ciudad Victoria, selección propositiva y al menos un año desde desaparición. No prevalencia, representatividad de Tamaulipas/México ni prueba causal de corrupción, tratamiento o eficacia de búsqueda. No incluye madres fuera de organizaciones, otros familiares ni comparación sin desaparición.",
    conducta_unidad_universo="Cinco madres con hijo/a desaparecido/a entrevistadas en Ciudad Victoria, Tamaulipas; una entrevista en profundidad por persona de 1–2 horas, muestra propositiva vía asociación local.",
    instrumento_ola="Almanza-Avendaño, Hernández-Brussolo y Gómez-San Luis, Pérdida ambigua: madres de personas desaparecidas en Tamaulipas, México, Región y Sociedad (2020), DOI 10.22198/rys2020/32/1396, artículo cualitativo",
    documento_id_hash_pagina="SIN-ID:almanza2020_perdida_ambigua.html|a953e1b09d5f304696401ac642436c47f4232b77994768afb865b29f38991ca8|Método/Resultados/Conclusiones;https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1870-39252020000100136&lng=es",
    pregunta_textual_codigo_respuestas="Guía de entrevista: desaparición, autoridades, relación previa con hijo/a, vida cotidiana y consecuencias psicosociales; análisis fenomenológico interpretativo de transcripciones. Sin escala de prevalencia ni grupo control.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo primario Scielo capturado físicamente con SHA/licencia CC BY-NC 4.0 y método/limitaciones leídos; cierre cualitativo situado. Falta id documental, no hay RESULT cuantitativo.",
    datos_id_estado="Transcripciones individuales no abiertas/descargadas U0; sin RESULT cuantitativo propio.",
    reserva="CC BY-NC 4.0; captura HTML local, registro documental pendiente. No reproducir citas de participantes fuera de condiciones/licencia; no generalizar n5 a México.",
    gen2_existente="Sin RESULT cuantitativo compatible; hallazgo cualitativo situado.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar DOI/URL/captura/licencia/SHA; conservar selección y contexto en toda cita, buscar estudios comparativos antes de afirmar mecanismo general o intervención.",
    prioridad="3",
)
BOSS = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L9-L10,L27,L31; marco de pérdida ambigua y cierre",
    tier_report="sin rótulo explícito",
    clase="ensayo teórico y reflexión clínica",
    limite_inferencial="Boss y Carnes integran teoría, reflexión personal y poesía; no reportan muestra mexicana, grupo comparador, estimador de daño por buscar cierre ni ensayo de eficacia terapéutica. Su argumento clínico no prueba que toda persona desaparecida en México tenga duelo prolongado ni contraindica por sí solo toda evaluación clínica.",
    conducta_unidad_universo="Ensayo de teoría sobre pérdida ambigua, ejemplificado por ausencia física o psicológica de familiares; no universo muestral ni personas mexicanas observadas.",
    instrumento_ola="Boss y Carnes, The Myth of Closure, Family Process 51(4):456–469 (2012), DOI 10.1111/famp.12005",
    documento_id_hash_pagina="SIN-ID:astra5_boss_carnes2012_myth_closure.pdf|c6fb5f8e1ba925b2c6e41fd6c456a55aa75f995f7ff48903cbbffc38972bac6d|pp.456-457,463-467;https://news.cehd.umn.edu/wp-content/uploads/2020/03/TheMythofClosure-Boss.pdf",
    pregunta_textual_codigo_respuestas="No encuesta: lectura textual de distinción desaparición física/demencia y propuesta clínica de sentido y tolerancia a incertidumbre; sin métrica de efecto.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Ensayo final íntegro en PDF institucional de autora con DOI/páginas/SHA físicos; contrato cierra atribución teórica, no efectividad o traslado clínico a México. Registro documental pendiente.",
    datos_id_estado="Sin datos individuales ni RESULT cuantitativo.",
    reserva="PDF institucional para lectura local; condiciones de reproducción/redistribución por MESA-DOCUMENTAL. No interpretar recomendación del ensayo como contraindicación universal o ensayo clínico.",
    gen2_existente="Sin RESULT compatible; fuente teórica.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar DOI/PDF/SHA/condiciones; contrastar crítica clínica con guías y estudios mexicanos antes de recomendar intervención universal.",
    prioridad="3",
)
SMID = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L98-L102,L171-L178; estudio México n29",
    tier_report="sin rótulo explícito",
    clase="entrevistas y grupos focales cualitativos sobre apoyo psicosocial",
    limite_inferencial="Selección práctica de familiares vinculados a grupos de autoayuda/ONG, hispanohablantes; cinco entrevistas individuales y cuatro grupos con 24 personas. Datos recolectados 2–13/oct/2016 y publicados 2020. La valoración de distrés por entrevistadores clínicos no es un diagnóstico por escala ni prevalencia nacional. Por diseño bilingüe no se transcribió íntegramente; organizaciones mapeadas por área parcial.",
    conducta_unidad_universo="29 familiares mexicanos (5 entrevistas individuales y 24 personas en cuatro grupos focales), reclutados vía colectivos/ONG; siete entrevistas a profesionales proveedores según texto final.",
    instrumento_ola="Smid, Blaauw y Lenferink, Intervention 18(2):139–149 (2020), DOI 10.4103/INTV.INTV_55_19; campo octubre 2016",
    documento_id_hash_pagina="SIN-ID:astra5_smid2020_mexico_relatives.pdf|4c641dd64eb0c5e4509ef0c90a3e169882315b23d2c56550b33394fc64c609be|pp.139,141,143,146-147;https://pure.rug.nl/ws/portalfiles/portal/147451347/Smid_et_al._2020_Disappearances_Mexico.pdf",
    pregunta_textual_codigo_respuestas="Entrevista abierta sobre experiencia, necesidad/apoyo y barreras; esperanza vivo en cinco niveles. Dos clínicos valoraron distrés sin escala reportada; análisis de contenido inmediato de grabaciones, sin transcripción completa.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo final PDF físico con DOI, páginas, método y límites leídos; cierra afirmaciones situadas, no prevalencia/eficacia. Falta id documental, sin RESULT cuantitativo.",
    datos_id_estado="Audio/entrevistas individuales no abiertos ni descargados; sin RESULT compatible.",
    reserva="PDF universitario para lectura local; portada restringe redistribución salvo permiso/licencia. El artículo imprime CC BY-NC-SA 4.0; MESA-DOCUMENTAL debe resolver condiciones aplicables a esta copia antes de circularla.",
    gen2_existente="Sin RESULT clínico compatible en main.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar PDF/DOI/SHA y resolver condiciones de portada/versión editorial; conservar selección, método clínico sin escala y fecha 2016; cotejar muestras externas antes de generalizar.",
    prioridad="3",
)
ROWS = [
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-001",
        texto_vigente="El CED decidió pedir información a México en su 28º período y presentó la solicitud conforme al artículo 34 el 24 de junio de 2025.",
        componente_contrastable="CED/C/MEX/A.34/D/1 párrs.33-34: documentación recibida febrero-abril 2025; Comité decidió solicitar información en 28º período y transmitió solicitud 24/jun/2025. No documenta en ese párrafo la frase de activación presidencial 4/abr.",
        localizador="L18, componente abril-junio 2025",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-002",
        texto_vigente="En decisión adoptada en marzo y distribuida el 17 de abril de 2026, el CED decidió llevar la situación de México a consideración de la Asamblea General y pidió transmitir la decisión.",
        componente_contrastable="CED/C/MEX/A.34/D/1 encabezado y párr.122: decisión de remisión a Asamblea General mediante Secretario General; el párr.123 plantea posibles medidas, no consigna que la Asamblea ya actuó.",
        localizador="L18, componente marzo-abril 2026",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-003",
        texto_vigente="El CED concluyó en el párr.121 que había indicios fundados de desapariciones forzadas en varios ataques generalizados o sistemáticos en México, con la calificación señalada en su decisión.",
        componente_contrastable="CED/C/MEX/A.34/D/1 párr.121: juicio de indicios fundados del Comité en procedimiento artículo 34; no es condena penal ni determinación de responsabilidad individual.",
        localizador="L18, componente indicios y calificación",
        siguiente_operacion="Registrar decisión y separar estándar de indicios del Comité de condena judicial; examinar eventual respuesta de Asamblea solo cuando exista acto propio.",
    ),
    HEEKE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-004",
        texto_vigente="En la muestra colombiana de Heeke et al., 17 de 73 familiares de desaparecidos (23.29%) cumplieron criterios PG-13 de duelo prolongado.",
        componente_contrastable="Artículo IV Tabla 10: 17/73, 23.29%, grupo pérdida por desaparición forzada; estudio transversal de desplazados afiliados a ONG.",
    ),
    HEEKE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-005",
        texto_vigente="En el grupo colombiano comparador de muerte ligada al conflicto, 70 de 222 (31.50%) cumplieron criterios PG-13; la diferencia con 23.29% no fue significativa en Tabla 10.",
        componente_contrastable="Artículo IV Tabla 10: 70/222, 31.50%, contraste χ²=1.67 no significativo; 92.8% de muertes de comparador fueron homicidios, no totalidad.",
    ),
    HEEKE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-006",
        texto_vigente="Entre 73 familiares colombianos de desaparecidos, mayor esperanza declarada de que la persona siguiera viva se asoció con mayor severidad PG-13 (β estandarizada 0.41 en modelo final).",
        componente_contrastable="Artículo IV Tablas 11-12: Spearman ρ=0.30 (p<.01); regresión jerárquica con depresión, PTSD, trauma, tiempo y sexo, β esperanza=0.41 (p<.05), ΔR² ajustada 0.05 en paso 4; esperanza² no significativa.",
        localizador="L11; asociación esperanza y duelo",
    ),
    ALMANZA | dict(
        id_afirmacion="ASTRA5-U0-DUEL-007",
        texto_vigente="Almanza-Avendaño et al. analizaron entrevistas en profundidad a cinco madres de personas desaparecidas de Ciudad Victoria, contactadas por una asociación de familiares.",
        componente_contrastable="Método del artículo: cinco mujeres con hijo/a desaparecido/a desde ≥1 año, selección propositiva mediante asociación local y una entrevista individual de 1–2 horas.",
    ),
    ALMANZA | dict(
        id_afirmacion="ASTRA5-U0-DUEL-008",
        texto_vigente="En esas cinco entrevistas las autoras interpretaron la ausencia física del hijo/a junto con prácticas para mantener su presencia psicológica y la incertidumbre sobre su destino.",
        componente_contrastable="Resultados/conclusiones del artículo: imagen positiva del pasado, actos y lenguaje del presente, esperanza futura; experiencia y contexto de cinco casos, no frecuencia poblacional ni efecto terapéutico.",
    ),
    BOSS | dict(
        id_afirmacion="ASTRA5-U0-DUEL-009",
        texto_vigente="Boss y Carnes distinguen pérdida por desaparición física sin destino verificado de ausencia psicológica en una persona físicamente presente.",
        componente_contrastable="Family Process 2012 p.456: desaparición corporal sin verificación de paradero/muerte y desvanecimiento psicológico por demencia u otras condiciones. Clasificación conceptual, no prevalencia ni causa institucional mexicana.",
        localizador="L9,L27; tipología",
    ),
    BOSS | dict(
        id_afirmacion="ASTRA5-U0-DUEL-010",
        texto_vigente="Boss y Carnes proponen en su ensayo sustituir la meta clínica de cierre definitivo por búsqueda de sentido y mayor tolerancia a la ambigüedad cuando el destino del ser querido sigue incierto.",
        componente_contrastable="Family Process 2012 pp.456-457,463-467: propuesta clínica argumentada con reflexión y narración; no estudio de eficacia ni demostración de daño universal por buscar cierre.",
        localizador="L10,L31; crítica de closure",
    ),
    ALMANZA | dict(
        id_afirmacion="ASTRA5-U0-DUEL-011",
        texto_vigente="Una madre entrevistada en Ciudad Victoria describió papeleo de autoridades sin resultado de localización al momento de la entrevista.",
        componente_contrastable="Resultados/Incertidumbre, ruptura y ausencia, Caso 2: testimonio de trámite sin resultado y falta de noticias. Es experiencia de un caso en muestra n5; no estima tasa de omisión, colusión o regla de espera de 72 horas.",
        localizador="L16,L72-L79; experiencia institucional situada",
    ),
    ALMANZA | dict(
        id_afirmacion="ASTRA5-U0-DUEL-012",
        texto_vigente="En las entrevistas de Almanza et al. aparecen alejamiento social y estigmatización por sospecha de vínculo de la víctima con el crimen, junto con relatos de solidaridad en algunos casos.",
        componente_contrastable="Resultados/El alejamiento de los otros: Caso 1 refiere pérdida de amistades y sospecha; Caso 4, juicio por volver al trabajo; autoras señalan apoyo en algunos casos. No frecuencia poblacional ni prueba de que toda narrativa procede del Estado.",
        localizador="L20,L90-L96; estigma y apoyo situados",
    ),
    SMID | dict(
        id_afirmacion="ASTRA5-U0-DUEL-013",
        texto_vigente="Smid et al. entrevistaron a 29 familiares de personas desaparecidas en México durante octubre de 2016: cinco individualmente y 24 en cuatro grupos focales.",
        componente_contrastable="Método pp.141-143: 29 familiares de colectivos/ONG, cinco entrevistas y cuatro grupos de cuatro a nueve integrantes (24 total); siete entrevistas a profesionales proveedores en artículo final. No muestra representativa; portal Utrecht resume ocho organizaciones, unidad distinta y discrepancia por cotejar.",
    ),
    SMID | dict(
        id_afirmacion="ASTRA5-U0-DUEL-014",
        texto_vigente="En la muestra de 29 familiares entrevistados por Smid et al., todos reportaron y mostraron señales de distrés emocional severo según la valoración de los entrevistadores clínicos.",
        componente_contrastable="Resumen y Resultados p.143: valoración clínica de psiquiatra y médico en n29; no escala, umbral diagnóstico ni denominador de población de familiares en México. Sesgo de reclutamiento reconocido pp.146-147.",
    ),
    SMID | dict(
        id_afirmacion="ASTRA5-U0-DUEL-015",
        texto_vigente="En las entrevistas de Smid et al. se mencionaron ideación suicida, insomnio, ansiedad, cambios de apetito, recuerdos intrusivos, irritabilidad y afectación de funciones cotidianas.",
        componente_contrastable="Resumen y Resultados p.143 enumeran síntomas frecuentes sin n por síntoma ni escala de tamizaje. No equivalen a diagnósticos ni a prevalencias mexicanas de cada síntoma.",
    ),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
