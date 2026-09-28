# Psicología de la juventud mexicana contemporánea: trayectorias, restricciones y diferencias

*Report v2 del [original](../reports/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md). Corte editorial: `7748208614570a50a97c1ba830aee72a972185f9`. Una cifra de literatura externa no es un RESULT del programa. Tabla de [afirmaciones](../../forense/analisis/reports-v2/salud-juventud-tiempo-1/juventud/tabla.tsv).*

**Contadores movidos por esta pieza: cero.** Editorial, sin nueva corrida, adjudicación ni adopción.

## Resumen ejecutivo

**Hallazgo sólido, con alcance acotado.** La juventud no es una unidad psicológica uniforme. Estudiar, buscar empleo, estar ocupado, cuidar y residir con la familia son estados distintos. Los resultados y publicaciones disponibles justifican segmentar por edad, sexo, localidad, escolaridad y condiciones materiales antes de atribuir un rasgo a «Gen Z». ENDUTIH documenta acceso digital desigual en la población de seis años o más; ese resultado **no** estima la desigualdad digital específicamente juvenil. La literatura primaria ENSANUT documenta conducta suicida con definiciones y ventanas temporales explícitas; no prueba una «explosión» de trastornos de una cohorte.

**Lo malinterpretado.** El original llamó «efecto de cohorte, no edad» a diferencias entre edades o generaciones observadas en un corte. Eso no identifica por separado edad, periodo y cohorte. También presentó como efectos de estructura afirmaciones para las que solo hay asociaciones o hipótesis. La residencia con padres no mide dependencia económica; «nini» no mide ocio ni cuidados; abstención no mide desafección; autoidentificación LGBTI+ no mide prevalencia latente constante entre periodos. Las frases electorales que convierten una proporción *entre los votos de una coalición* en una proporción *entre los jóvenes* quedan retiradas.

**Utilidad práctica.** Una intervención juvenil debe declarar población, edad, actividad y desenlace. La próxima medición útil distingue las restricciones observables de las preferencias declaradas y separa por diseño el efecto de una política del cambio agregado de periodo. Mientras eso falta, se puede diseñar evaluación de vivienda, cuidados, conectividad y empleo sin afirmar que cada mecanismo ya fue identificado.

**Hallazgos y decisiones para lectura rápida:**

1. **Sólido descriptivo:** la brecha digital por localidad existe en el universo general ENDUTIH; su magnitud juvenil requiere cálculo propio.
2. **Sólido descriptivo:** la ENSANUT distingue ideación, intento y periodos de referencia; no se reemplazan entre sí.
3. **Malinterpretado:** salida del hogar, unión y fecundidad son transiciones diferentes.
4. **Malinterpretado:** residencia con padres no mide dependencia económica.
5. **Malinterpretado:** una diferencia entre cohortes retrospectivas no identifica por sí sola un efecto de cohorte psicológico.
6. **Útil:** separar estudio, ocupación, búsqueda y cuidados antes de interpretar NEET.
7. **Útil:** usar informalidad solo con el grupo de ocupados y la edad del estimando.
8. **Malinterpretado:** autoidentificación de una edad en un corte no mide cambio intergeneracional persistente.
9. **Malinterpretado:** proporción de jóvenes dentro del voto de una coalición no es proporción de votos por esa coalición entre jóvenes.
10. **Útil:** exigencia de justificación de la autoridad es pregunta para medición mexicana, no conclusión importable de EU.
11. **Útil:** tendencia nacional NEET no identifica efecto de Jóvenes Construyendo el Futuro.
12. **Sólido metodológico:** mecanismos de estructura, cultura y adaptación se prueban con variables y comparadores, no se adjudican por plausibilidad.

## Marco y mapa de evidencia por tier

«Juventud», «Gen Z» y «millennials jóvenes» tienen fronteras distintas. La clasificación por año de nacimiento no sustituye el rango de edad de cada encuesta. En una encuesta transversal, edad = periodo de observación − año de nacimiento. La identidad genera colinealidad exacta: incorporar más cortes repetidos ayuda a describir trayectorias, pero **por sí solo** no identifica los tres efectos. Hacen falta restricciones identificadoras justificadas, un diseño de panel o contrastes externos. EDER retrospectiva puede comparar eventos a la misma edad entre cohortes observadas, pero quedan historia, recuerdo, supervivencia, composición y contexto; la comparación no prueba una esencia generacional.

**Tier fuerte descriptivo, mecanismo no identificado (a, México).** [ENDUTIH 2024, INEGI](https://www.inegi.org.mx/programas/endutih/2024/) mide uso individual de internet en residentes de seis años y más. Las celdas siguientes proceden del objeto `CALC-ENDUTIH-PISOS-2024-0001/resultados.json`, clave `RESULT-ENDUTIH-PISOS-2024-TABLA`, arreglo `celdas`, índices base cero; SHA-256 del JSON `4c0a3b05b6ecef3e9d7e760163cc6a6691ceaf384fa522e620bbe9b663088c25` y del sello `17dd31ae136a795824b49d90515159e0f111be47550dbf86833ba775105aa5b8`. La firma `FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01` consta **FIRMADA** en [firmas-pendientes.tsv](../../forense/firmas-pendientes.tsv), fila de esa identidad; el [catálogo v1.2](../../canon/catalogo-del-mexicano-v1_2.md) §pisos por instrumento la incorpora como piso descriptivo retrospectivo, sin uso predictivo.

| Celda, medida y dominio | Punto e IC95 de diseño | Unidad, denominador y ola |
|---|---|---|
| `RESULT-ENDUTIH-PISOS-2024-TABLA#46`, `internet`, `TOTAL` | 83.122% [82.657, 83.589] | Personas elegidas de seis años y más, P7_1 válido 1/2, FAC_PER positivo, EST_DIS/UPM_DIS presentes; últimos tres meses; n sin ponderar 58 080; peso denominador 120 604 797; ENDUTIH 2024 |
| `RESULT-ENDUTIH-PISOS-2024-TABLA#42`, `internet`, `TLOC_1` | 88.902% [88.309, 89.443] | Mismo universo y filtro, localidad de cien mil habitantes o más; n 27 695; peso denominador 56 847 622; ENDUTIH 2024 |
| `RESULT-ENDUTIH-PISOS-2024-TABLA#45`, `internet`, `TLOC_4` | 69.964% [68.751, 71.178] | Mismo universo y filtro, localidad menor de dos mil quinientos habitantes; n 12 823; peso denominador 27 273 422; ENDUTIH 2024 |

Las tres proporciones son de *personas*, con pesos expandidos, no de hogares; el IC procede del objeto sellado y no tiene validación independiente acreditada aquí. Los extremos de tamaño de localidad no equivalen a todo urbano frente a todo rural. El contraste general respalda desigualdad de uso, pero no destreza digital ni la magnitud del grupo de dieciocho a veinticuatro. [Valdez-Santiago y colegas, ENSANUT 2022](https://ensanut.insp.mx/encuestas/ensanutcontinua2022/doctos/analiticos/15-Conducta.suicida-ENSANUT2022-14815-72580-2-10-20230619.pdf), métodos y resultados, muestra nacional de adolescentes y adultos, distingue ideación e intento alguna vez y en los últimos doce meses. La fuente fue publicada en 2023 y leída en su PDF; la conclusión no debe cambiar de ventana temporal ni de desenlace.

**Tier medio descriptivo, mecanismo no identificado (a).** Los resultados públicos de EDER 2025 y ENADID 2023 serían pertinentes para transiciones familiares y fecundidad; **no se emplean sus cifras** porque las reservas vigentes del proyecto cubren estas olas o módulos. Su existencia no autoriza trasladar resultados al report. La ENDISEG 2021 describe autoidentificación por edad en una muestra nacional de personas de quince años y más, pero se omiten cifras hasta cotejar su reserva exacta y, en cualquier caso, el corte único no identifica cambio de cohorte. Las afirmaciones sobre trabajo de cuidados necesitan cotejo del documento primario de Oxfam y de la clasificación de estudio, empleo, cuidado y búsqueda.

**Tier de mecanismo: hipótesis.** Precios de vivienda, ingreso laboral, oferta de cuidados, infraestructura, violencia, normas de género y acceso a servicios pueden modificar las decisiones. La evidencia aquí no mide su contribución relativa, sus efectos causales ni su predominio frente a preferencias. La referencia agregada a un piso ENOE para *todos los ocupados* que figura en el mapa previo no se usa como RESULT individual: el alias `RESULT-ENOE-PISOS-TABLA` no resolvió por `tools/consulta.py result` en este corte. Tampoco estimaría informalidad de ocupados de veinte a treinta años; además, la candidata de inferencia ENOE afectada por el bloqueo de estratos singleton de #1222 no autoriza usar su intervalo como validación de este corte. Una cifra de informalidad no mide por sí sola aspiraciones ni NEET.

**Tier de marco (c) y diáspora (b).** Las «cuatro íes», Hofstede, GLOBE y tipologías de consultoría son marcos importados, no escalas nacionales validadas de personas jóvenes mexicanas. La encuesta estadounidense sobre jerarquía política no se transporta a una organización mexicana; el dato laboral multinacional de Deloitte tiene su propio marco de selección. No se identificó aquí evidencia de diáspora para los mecanismos centrales; tampoco se usa un contraste migratorio como prueba de socialización mexicana.

La [tabla dirigida](../../forense/analisis/reports-v2/salud-juventud-tiempo-1/juventud/tabla.tsv) evalúa explícitamente las afirmaciones del mapa y las tesis materiales adicionales. **CONFIRMA** exige contraste directo del estimando; **MATIZA** conserva solo una parte con su universo; **ROMPE** retira una inferencia incompatible con el diseño o el denominador; **SIN-CIFRA** conserva la pregunta con su causa concreta de no contraste. Un ROMPE de causalidad no declara falso el fenómeno descrito. La tabla no adopta ningún RESULT ni modifica el mapa.

## Patrones principales y segmentos

### Transiciones a la adultez y vivienda

**A favor:** la pregunta por salida del hogar, primera unión y nacimiento permite estudiar transiciones distintas. **Matiz:** el original sumó residencia parental, independencia antes de cierta edad, nupcialidad y fecundidad como si midieran un único «aplazamiento». La salida del hogar puede ocurrir sin solvencia propia; quedarse puede combinar restricción y preferencia. EDER 2025 y ENADID 2023 permanecen fuera del soporte numérico de esta pieza por reserva. **Segmentos:** comparar mujeres y hombres, rural y urbano, estudio y empleo, pero con estimandos y edades comunes. **Causas rivales:** costos de vivienda, trabajo, escuela, cuidados, unión y preferencia de corresidencia. **Riesgo:** diagnosticar inmadurez o llamar adaptación racional identificada a una correlación. **Implicación:** en evaluación, medir ingreso, costo y oportunidad residencial al mismo tiempo que preferencia y transición observada.

### Conectividad y capacidad digital

**A favor:** el resultado ENDUTIH de población general y su desglose por localidad acreditan desigualdad de uso. **En contra/matiz:** ni el uso frecuente ni el teléfono acreditan habilidades de banca, estudio, producción o seguridad. La frase «nativos digitales» es una hipótesis de competencia uniforme que no se desprende de acceso. **Segmentos:** edad específica, localidad, escolaridad, ingreso y calidad de conexión; una brecha general no equivale a una brecha de jóvenes. **Causas rivales:** cobertura, costo, dispositivo y formación. **Riesgo:** sustituir destreza por posesión. **Implicación:** probar tareas instrumentales concretas y desempeño, además de conectividad.

### Salud mental, ideación, intento y muerte

**A favor:** ENSANUT 2022 permite distinguir ideación e intento en adolescentes y adultos, con prevalencia diferenciada por sexo. **Matiz:** ideación alguna vez no fue mayor en adolescentes en la fuente primaria leída; intento e ideación no comparten necesariamente dirección ni ventana. Diagnóstico, malestar, conducta suicida y mortalidad son desenlaces separados. ENCODAT 2025 y tasas de defunción citadas originalmente no se incorporan como cifras firmes. **Segmentos:** edad, sexo, contexto, atención y población LGBT+ si hay medición adecuada. **Causas rivales:** exposición a violencia, apoyo, servicios, disposición a declarar y cambios de periodo. **Riesgo:** «generación de cristal» patologiza; «las redes causaron la crisis» atribuye causalidad no identificada. **Implicación:** evaluar prevención y acceso con sus propios indicadores, sin inferir tratamiento individual de este report.

### Estudio, empleo, cuidados e informalidad

**A favor:** las categorías laborales y de cuidados hacen plausible que «no estudiar ni estar ocupado» oculte actividad valiosa. **Matiz:** no se verificaron aquí las proporciones de Oxfam ni la definición exacta de su denominador. «No ocupado», «desocupado buscando», «fuera de la fuerza de trabajo», «trabajando en cuidados» y «nini» no son intercambiables. El piso ENOE agregado mencionado en el mapa no respalda un porcentaje juvenil y su alias no se consume en esta pieza. **Segmentos:** sexo, maternidad/paternidad, edad, horas de cuidados, matrícula y búsqueda laboral. **Causas rivales:** oferta de empleo, reglas familiares, salarios, cuidados y preferencias. **Riesgo:** convertir una ausencia de empleo de mercado en ocio o afirmar que un programa falló por tendencia nacional. **Implicación:** evaluar por estados de actividad y trayectorias; para Jóvenes Construyendo el Futuro, comparar elegibles y expuestos con controles plausibles.

### Afiliación, derechos y autoidentificación

**A favor:** censo y ENDISEG ofrecen preguntas descriptivas sobre religión e identidad; actos legales describen cambios institucionales. **Matiz:** un corte de edad no prueba secularización de cohorte; autoidentificación no equivale a orientación latente invariable; cambio legal no equivale a acceso efectivo; movilización visible no significa mayoría nacional. **Segmentos:** localidad, escolaridad, región, sexo y condiciones de reporte. **Causas rivales:** periodo, composición, apertura, experiencia y norma. **Riesgo:** atribuir feminismo, ateísmo, afiliación o identidad a toda una etiqueta generacional. **Implicación:** repetir ítems y observar oferta/uso institucional con denominadores explícitos.

### Autoridad y política

**A favor:** la hipótesis de exigir razones a la autoridad es útil para diseñar una prueba. **Matiz:** jerarquía cultural estadounidense, intención laboral multinacional, preferencia electoral y confianza institucional son constructos distintos. El original carece de fuente electoral identificada para varios porcentajes; la «decisividad» del voto joven no se deduce de composición de los votos de una coalición. **Segmentos:** empleo formal/informal, escolaridad y participación política, nunca un joven genérico. **Causas rivales:** edad, ocupación, periodo electoral, cultura organizacional y competencia percibida. **Riesgo:** «anti jerarquía» y «pro partido» son dos simplificaciones opuestas. **Implicación:** medir conducta y actitudes en la misma población; el rechazo a una figura no demuestra rechazo al sistema.

## Causas, estructura y adaptación

La vivienda, el ingreso, la oferta de trabajo, la red de cuidados y la conectividad son restricciones materiales que pueden ordenar oportunidades. Una decisión compatible con una restricción no demuestra que esa restricción sea su causa dominante. Para distinguirla de preferencia se requiere observar ambas, comparar oportunidades reales y seguir transiciones a igual edad. La unidad correcta para una política juvenil suele ser la persona en un estado de actividad y entorno determinado; la cohorte de nacimiento sirve para comparar trayectorias, no para asignar psicología.

Los papeles de género y la familia son contextos sociales, medibles por distribución de tiempo y decisiones, no explicaciones automáticas de cada caso. Violencia, pandemia, inflación y acceso digital afectan varios grupos de edad en un periodo: etiquetarlos como «cohorte joven» exige demostrar efecto diferencial persistente. La parte causal del original que declaraba predominio de estructura, o efecto de programa por una serie agregada, se retira hasta disponer de diseños comparativos.

## Segmentación explícita

| Eje | Unidad y lectura admisible | Límite |
|---|---|---|
| Edad | Persona y edad exacta o rango de cada instrumento | Un rango juvenil no equivale a Gen Z por nacimiento |
| Cohorte | Año de nacimiento y evento observado a edad comparable | Periodo y selección quedan mezclados |
| Sexo y género | Variable tal como la recoge cada fuente | No atribuir identidad o norma desde sexo administrativo |
| Actividad | Estudio, ocupación, búsqueda y horas de cuidados por persona | NEET no es desocupación ni ociosidad |
| Localidad | ENDUTIH distingue tamaños de localidad | Ruralidad no equivale a identidad indígena |
| Escolaridad e ingreso | Condiciones medidas de la persona o su hogar | No son preferencias ni clase latente automáticamente |
| Región, religión y migración | Ejes para diseños específicos | Sin cifras propias comparables en esta pieza |
| Exposición digital | Uso, dispositivo, calidad y destreza son variables distintas | Uso no demuestra competencia ni causa malestar |

## Comparación internacional útil

Las encuestas comparables pueden preguntar si la misma asociación aparece en contextos de vivienda, cuidados e informalidad diferentes. El [informe OCDE *Society at a Glance 2024*](https://www.oecd.org/en/publications/society-at-a-glance-2024_918d8db3-en.html) ofrece marco comparativo de familias y juventud, pero su porcentaje residencial citado en el original no fue verificado aquí con tabla, año y denominador y no se reproduce. Deloitte 2025 informa sobre una muestra multinacional de Gen Z y millennials; es evidencia (c) para hipótesis laborales, no una tasa mexicana. Ningún contraste internacional mostrado identifica que la causa mexicana sea cultura, estructura o cohorte. No se transporta una brecha política estadounidense por género ni la tipología «cuatro íes» como psicometría mexicana.

## Implicaciones y mitos

Para política de vivienda y empleo, medir primero elegibilidad, ingreso, costo, oferta, búsqueda y decisión residencial; evaluar expansión con comparador. Para cuidados, publicar estado de estudio/empleo junto a horas, relación de parentesco y disponibilidad de servicios. Para inclusión digital, añadir tareas instrumentales y calidad de conexión. Para salud mental, separar tamizaje, intento, atención y mortalidad, y ofrecer servicios pertinentes sin asignar diagnósticos generacionales.

Se retiran los universales «todos los jóvenes dominan tecnología», «no quieren trabajar», «son frágiles», «rechazan toda autoridad» y «votan como bloque». El rechazo de esos universales no demuestra la tesis opuesta en todos los segmentos. «Nini» puede ser una etiqueta administrativa si se define exactamente; su uso moral como ociosidad queda injustificado. La independencia tardía, cuando se mida en una cohorte permitida, deberá interpretarse como transición residencial, no como prueba de voluntad o autosuficiencia.

## Síntesis y reglas SI–ENTONCES propuestas

La explicación defendible es una matriz de oportunidades, actividades, normas y edad; todavía no una personalidad de Gen Z. Las fuentes primarias dan descripciones parciales. El cambio editorial principal es bajar de categoría las atribuciones de cohorte y mecanismos causales que el diseño no separa, y conservar preguntas concretas para un sucesor medible.

| Regla PROPUESTO-POR-EJECUTOR | Consumidor posible; condición | Tier de frecuencia / mecanismo | Falsador |
|---|---|---|---|
| SI una fuente entrega un corte de edad, ENTONCES reportarlo como diferencia por edad y periodo medidos, sin llamarlo efecto de cohorte | Editor de reports; edad, ola y pregunta explícitas | Descriptivo / mecanismo no identificado | Panel o series con supuestos APC transparentes y prueba de robustez que sostengan efecto de cohorte |
| SI se clasifica a alguien fuera de estudio y empleo, ENTONCES medir cuidados y búsqueda antes de interpretarlo | Diseño de empleo y cuidados; persona y ventana comunes | Hipótesis de segmentación / mecanismo no identificado | Encuesta representativa con tiempo y actividad que descarte carga de cuidados en el segmento |
| SI se usa ENDUTIH para una decisión juvenil, ENTONCES exigir corte etario y medir destreza aparte del acceso | Editor de inclusión digital; misma ola y población | RESULT agregado adoptado / destreza sin medición | Desempeño instrumental comparable que muestre equivalencia con simple uso |
| SI se atribuye cambio a Jóvenes Construyendo el Futuro, ENTONCES exigir grupo comparable, exposición y rezagos | Evaluador del programa; estimando causal definido | Serie agregada insuficiente / mecanismo no identificado | Evaluación válida que encuentre efecto con magnitud e incertidumbre |

No se incorporan estas reglas al motor. Las tres primeras disciplinan lenguaje y adquisición; la última fija un criterio de evaluación. Ninguna asigna un coeficiente a una persona.

## Auditoría de rigor extremo

**¿Se confundió pobreza, violencia, informalidad o cuidado con «cultura»?** El original sí las usó como causa predominante de emancipación, fecundidad y aspiraciones sin descomponer efectos. Esta versión las trata como condiciones y mecanismos rivales que requieren contraste. Familia extendida no prueba preferencia ni explica por sí sola la permanencia.

**¿Se generalizó desde clase media urbana?** Jerarquía laboral, apps, activismo y publicidad de Gen Z suelen observar a personas conectadas o escolarizadas. Se acotó su transporte; tampoco se asume que rural equivale a indígena o a baja escolaridad. Los segmentos requieren muestra y tamaño suficiente.

**¿Se importaron marcos anglosajones?** «Nativos digitales», «generación de cristal», las «cuatro íes», Hofstede, GLOBE y la encuesta Berkeley no definen parámetros mexicanos. Se usan como preguntas, no como resultados locales. No hay prueba de diáspora transportable en esta pieza.

**¿Qué cambia con foco rural, indígena o popular?** Cobertura y costo digital, trabajo informal, cuidados, lengua, distancia a servicios y formación del hogar pueden reordenar asociaciones. No hay aquí estimación completa de esos mecanismos ni certeza de que la dirección sea la misma en cada subgrupo.

**¿Qué parece psicológico y puede ser incentivo?** Corresidencia, movilidad de empleo y uso de canales digitales podrían responder a opciones disponibles. Para afirmar adaptación óptima hay que observar el conjunto de alternativas y resultados; de lo contrario queda como hipótesis.

**¿Dónde hay evidencia débil e intuición fuerte?** Efecto de redes en salud mental, causalidad de vivienda sobre fecundidad, jerarquía laboral mexicana, desafección de abstencionistas, «cuatro íes» y evaluación causal de programa. Para cada una la [tabla](../../forense/analisis/reports-v2/salud-juventud-tiempo-1/juventud/tabla.tsv) especifica qué observación movería el dictamen.

**¿Qué conclusión sería dañina si se simplifica?** Inferir ocio de NEET, incompetencia de falta de conexión, inmadurez de corresidencia o patología de una etiqueta generacional puede orientar mal servicios y recursos. También sería dañino deducir causalidad de una mejora o deterioro agregado sin comparador.

**Estado de rigor:** lectura completa del original y del mapa local; juicios explícitos por afirmación; ningún microdato reservado abierto o recalculado y ninguna cifra reservada trasladada a este reporte; sin estimación propia nueva ni validación independiente de RESULT. Una búsqueda web mostró extractos públicos de EDER y ENADID antes del cotejo fino de reserva; se excluyeron sus valores y no se consultaron sus tablas para este producto. La consistencia puntual de un RESULT no acredita automáticamente su incertidumbre o validez inferencial. El report aporta narrativa utilizable y un plan de falsación, con los límites indicados.

**Estado del corpus y deuda:** «casi toda la literatura» urbana de clase media es un juicio heredado escrito a mano, no un conteo derivado; se retiró como proporción en espera de un censo metodológico. La deuda de separar edad, periodo y cohorte ya no puede quedar implícita al usar estos reports como producto: se aplica a cada tesis. La deuda de cifras de olas reservadas se mantiene por objeto y no autoriza actualizar el report con un comunicado público.

**Escala, comparación y temporalidad:** las tres celdas ENDUTIH son proporciones ponderadas de *personas* de seis años y más, comparadas solo con personas del mismo universo en cortes de tamaño de localidad; no se promedian con hogares, jóvenes u horas. La referencia documental ENOE trata *personas ocupadas*, no toda la juventud, y no se consume como RESULT aquí. ENSANUT compara proporciones de *personas* por edad/sexo y periodo de recuerdo, no tasas de muertes. Los RESULT ENDUTIH citados son mediciones **RETROSPECTIVAS** de una ola conocida; esta pieza no contiene cifra **PROSPECTIVA** ni mezcla ambos rótulos en una conclusión. La validez puntual, la incertidumbre y la inferencia causal son preguntas separadas.

## Fuentes primarias y límites de lectura

- (a) [INEGI, ENDUTIH 2024](https://www.inegi.org.mx/programas/endutih/2024/), levantamiento 2024, personas de seis años y más; método probabilístico, ficha y síntesis metodológica; consulta 27/sep/2026. El corte etario de la tesis original no se reconstruyó aquí. RESULT adoptado citado arriba y sus denominadores están en `CALC-ENDUTIH-PISOS-2024-0001`.
- (a) [Valdez-Santiago y colegas, ENSANUT continua 2022](https://ensanut.insp.mx/encuestas/ensanutcontinua2022/doctos/analiticos/15-Conducta.suicida-ENSANUT2022-14815-72580-2-10-20230619.pdf), publicado 2023; adolescentes y adultos residentes en México; análisis transversal de ideación e intento; resumen, métodos y resultados del PDF consultados 27/sep/2026. No identifica redes sociales ni cohorte.
- (a) [INEGI, ENDISEG 2021](https://www.inegi.org.mx/programas/endiseg/2021/), levantamiento 2021–2022, personas de quince años y más; ficha metodológica consultada 27/sep/2026. Sin cifras trasladadas por cotejo de reserva pendiente; una entrevista transversal no identifica efecto generacional.
- (a) [INEGI, EDER 2025](https://www.inegi.org.mx/programas/eder/2025/) y [ENADID 2023](https://www.inegi.org.mx/programas/enadid/2023/): referencias de instrumento; cifras y cuadros deliberadamente excluidos por reserva del proyecto. No se usaron resultados de sus olas como evidencia numérica.
- (c) [OCDE, *Society at a Glance 2024*](https://www.oecd.org/en/publications/society-at-a-glance-2024_918d8db3-en.html), comparación internacional; ficha, sin cifra residencial trasladada. Deloitte, Berkeley y las «cuatro íes» se mencionan como fuentes o marcos originales pendientes de contraste mexicano, sin atribuirles una estimación de México.

El [expediente local](../../forense/analisis/reports-v2/salud-juventud-tiempo-1/juventud/) conserva tabla, productor y revisión dirigida. **B)** evidencia de diáspora: ninguna usada. **C)** marcos importados: solo para formular hipótesis, sin parámetros mexicanos.
