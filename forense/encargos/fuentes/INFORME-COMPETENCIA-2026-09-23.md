# ¿Existe en México un producto como el nuestro? Informe de competencia 2025–2026

**Respuesta corta: no encontramos a nadie que venda, publique o mantenga para México ninguna de las tres propiedades completas.** Nadie tiene validación prospectiva sellada con historial público, ni cobertura de intervalo medida por segmento, ni una prueba publicada contra la persistencia. Los más cercanos se quedan a medio camino en al menos una propiedad. YouGov Parallax y la alianza Gallup–Simile ya validan gemelos contra humanos reales, pero en tiempo real o en EE.UU. y no de forma prospectiva sobre México. Matria AI (Celestial Dynamics) usa microdato INEGI y NSE AMAI, pero no publica ninguna métrica de precisión. La literatura académica de 2026 respalda con fuerza la tesis de la persistencia fuera de México.

*Fecha de consulta de todas las fuentes: 23/sep/2026, salvo indicación. Etiquetas de procedencia: **[afirma]** = lo dice el proveedor de sí mismo · **[tercero]** = lo reporta o verifica alguien ajeno · **[literatura]** = evidencia académica sobre el método en general.*

## TL;DR

- **Ninguna de las tres propiedades existe hoy para México con evidencia pública.** No encontramos un historial "predije X antes de la ola, la ola dijo Y" para México ni una cobertura de intervalo reportada para segmentos mexicanos. Tampoco hallamos un contraste publicado de gemelos digitales contra microdato INEGI. Los proveedores sintéticos con México declarado, como Toluna, ThinkNow y Matria AI, se entrenan con paneles en línea o con modelos geográficos y no publican error.
- **La industria global ya pide exactamente el tipo de benchmark que tenemos, pero lo resuelve en casa.** YouGov admite que los sintéticos "cannot reliably track shifts in public opinion" y vende su propia capa de validación. Gallup valida a Simile "independently", según el blog metodológico de Jenny Marlar y Zacc Ritter (11/may/2026). El preprint arXiv 2608.28615 de Howard Kim y Keun Tae Cho (Corea, jul/2026, contra el KISDI Korea Media Panel Survey) encontró que la ola previa (MAE 3.7 pp) venció al panel sintético incluso ya calibrado (7.0–7.5 pp), y que "the correction did not transfer across time". No hallamos precedente de un tercero independiente que venda calibración.
- **La ventaja defendible es el historial sellado, y es estrecha.** Cualquier actor con acceso a microdato INEGI y un LLM (Matria AI, WoskyLab, ThinkNow MX, Worldpanel by Numerator) puede replicar el catálogo en 6–12 meses. Nadie puede fabricar hacia atrás predicciones selladas antes de olas ya publicadas. Por el calendario de olas (ENIF trienal, ENIGH bienal), un recién llegado tardaría años en igualar seis evaluaciones.

## Key Findings

1. **Validación prospectiva (P1):** nadie la publica para México. En el mundo la aproxima Aaru, que según Replism "predicted the 2024 New York Democratic primary within 371 votes", pero también "predicted a Harris Electoral College win" y falló el resultado general; son eventos electorales en EE.UU. y la fuente es secundaria. WoskyLab (México) la *promete*: "volver en siete días a verificar si acertamos, a la vista de todos". No encontramos evidencia de que ya lo haga.
2. **Cobertura de intervalo (P2):** nadie la reporta. Lo más cercano son el coeficiente de variación muestral que publica INEGI y el "calculable margin of error" que YouGov obtiene de la muestra humana de validación. Ninguno mide la varianza del cambio entre olas.
3. **Persistencia como piso (P3):** ningún proveedor la usa como benchmark. La literatura sí: en Corea (Kim y Cho, arXiv 2608.28615), la ola previa superó a un panel sintético calibrado, y YouGov declara que Parallax no sirve para trackers.
4. **México no es bloque en la oferta actual.** Worldpanel by Numerator cubre la población *urbana*: 8,500 hogares, con 82% u 84% de cobertura según la página. GWI cubre solo a internautas de 16–64 años, y Toluna construye personas con su comunidad en línea. Solo el microdato oficial (INEGI) y LAPOP tienen marcos probabilísticos nacionales con población rural.
5. **Exclusión por oferta (Q5):** INEGI y CNBV publican las razones de no tenencia, como "no cumple con los requisitos (20.7%)" en crédito, pero como tabulado aparte. No encontramos ningún producto comercial que la ponga como columna estándar junto a la conducta.
6. **AMAI NSE (Q8):** sigue siendo el estándar mexicano, con la Regla AMAI 2024 ratificada con ENIGH 2022. Matria AI lo usa. Los gemelos globales (Toluna, YouGov, Simile, Aaru) no lo mencionan en ninguna fuente consultada.

## Details

### 1 · Tabla comparativa

Leyenda de estado: **ENC** = ENCONTRADO (con cita) · **NO-ENC** = NO-ENCONTRADO (se buscó y no apareció) · **NO-ACC** = NO-ACCESIBLE (muro de pago o login) · **PEND** = no buscado en esta sesión (ver Caveats). Validación prospectiva e IC: SÍ / NO / PARCIAL.

| # | Frente | Proveedor / producto | Qué vende | Fuente de datos | Segmentación | ¿Validación prospectiva? | ¿Cobertura IC? | Cobertura México | Modelo comercial y precio | URL | Estado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | Worldpanel by Numerator (ex Kantar Worldpanel) México | Panel de compras de hogares, ~100 categorías de consumo masivo | Panel propio: 8,500 hogares, compras semanales, 6 regiones | Región, 7 ciudades auto-representadas, perfil del hogar | NO (no publica) | NO | **Urbana** ("82%" / "84% de la población urbana", cifras inconsistentes entre páginas) | Suscripción sindicada; precio no público | kantar.com/latin-america/latinoamerica/mexico · market.worldpanelbynumerator.com/es/countries/worldpanel/Mexico | ENC [afirma] |
| 2 | A | Euromonitor Passport: Consumer Lifestyles in Mexico, Mexico: Consumer Profile, Consumer Types in Mexico | Informes-país (PPT) y plataforma | Encuesta propia Voice of the Consumer: Lifestyles 2026 más estadística socioeconómica | Edad, ingreso, hogar; "Consumer Types" propios | NO | NO | 40 países; universo de la encuesta en México no verificado | Informe individual de pago más suscripción Passport; precio no capturado | euromonitor.com/consumer-lifestyles-in-mexico/report | ENC / precio NO-ACC |
| 3 | A | GWI Core | Plataforma de perfiles de consumidores en línea | Encuesta propia trimestral, cuotas por edad, sexo y escolaridad | Edad, sexo, escolaridad, más segmentaciones GWI | NO | NO | **Internautas 16–64**; 65+ solo en "select markets" desde el T1 2024 | Suscripción a plataforma y API | help.globalwebindex.com/en/articles/5880945-sample-composition | ENC [afirma] |
| 4 | A | De la Riva Group | Estudios sindicados ("México Rifado 2.0", Base de la Pirámide en LatAm), QuickSights con copiloto de IA | Encuesta y cualitativo propios | Por estudio; "Base de la Pirámide" | NO | NO | No declarada | Sindicado más proyecto; precio no público | linkedin.com/company/de-la-riva-group | ENC (solo LinkedIn; sitio no verificado) |
| 5 | A/D | AMAI, Regla NSE AMAI 2024 | Estándar de clasificación socioeconómica y NSE por manzana, AGEB y localidad | ENIGH (INEGI) | 7 niveles; 6 variables más escolaridad del jefe de hogar | PARCIAL: revisión bienal de la regla contra cada ENIGH nueva (retrospectiva, no conductual) | NO (reporta Pseudo-R² 0.4852) | Nacional | Regla pública; desagregados vía AMAI | amai.org/NSE/index.php?queVeo=NSE2024 · amai.org/descargas/NOTA_METODOLOGICA_NSE_AMAI_2024_v6.pdf | ENC |
| 6 | A/B | Ipsos, gemelos digitales con Stanford (Politics and Social Change Lab) | Paneles de gemelos digitales | KnowledgePanel (EE.UU.) | No documentada para MX | PARCIAL (validación con Stanford, EE.UU.) | NO | NO-ENC para México | No público | tecnoempresa.mx/ipsos-y-stanford-impulsan-gemelos-digitales-en-investigacion-de-mercado/ | ENC [tercero] |
| 7 | B | YouGov Parallax | Gemelos 1:1 de panelistas más validación humana configurable | Panel propio: más de 30 millones de miembros | Por audiencia del panel | PARCIAL: validación *contemporánea* contra humanos, no sellada ex ante | PARCIAL: "calculable margin of error" de la muestra humana de validación | Demo solo EE.UU./Reino Unido; enterprise en "49 markets" de YouGov Profiles (México no verificado); internautas | Para suscriptores de YouGov; precio no público | parallax.yougov.com · yougov.com/articles/55129 | ENC [afirma] |
| 8 | B | Toluna HarmonAIze Personas | Personas sintéticas para claims testing y screening | "first-party data" de la comunidad en línea de Toluna (79 millones) | Demográfica y psicográfica | NO | NO | **México "live"** desde oct/2025; internautas | Dentro de la plataforma Toluna Start; precio no público | tolunacorporate.com/tolunas-one-million-synthetic-personas-accelerate-ideas-and-claims-testing-worldwide/ | ENC [afirma] |
| 9 | B | Simile | Gemelos agénticos; "simular 8 mil millones de humanos" | Entrevistas en profundidad (origen: estudio de 1,000 personas de Stanford) | Individual | NO publicada; afirma "85% accuracy" en la General Social Survey | PARCIAL: "trained a confidence model that predicts the accuracy of every simulation" [comunicado vía Pulse 2.0, 30/jul/2026; sin cobertura publicada] | NO-ENC para México | Enterprise, sin precio público; Serie B de US$200M con valuación post-money de US$2B liderada por Greenoaks (30/jul/2026) [tercero: TechCrunch] | valueaddvc.com/blog/simile-valuation-2026-2b-synthetic-user-ai-startup-20x-in-5-months | ENC [afirma]/[tercero] |
| 10 | B | Gallup, programa de validación de Simile | Validación independiente de respuestas sintéticas | Gallup Panel probabilístico, ~1,000 entrevistas | Respondente, encuesta y población | PARCIAL: en curso, resultados "in future articles" | NO publicada | EE.UU.; no aplica a MX | No comercial; no se usará en estimaciones publicadas | news.gallup.com/opinion/methodology/709373/gallup-begins-research-synthetic-responses.aspx | ENC [afirma] |
| 11 | B | Aaru | Simulación de poblaciones para predicción de resultados | "public and proprietary data" | Demografía y geografía | PARCIAL: primaria demócrata de NY "within 371 votes", pero falló el ganador presidencial de 2024 [tercero: Replism]; EY "0.90 median correlation" [afirma] | NO | NO-ENC para México | Enterprise; Serie A (dic/2025) con valuación "headline" de US$1B y valuación combinada inferior; ARR menor a US$10M [tercero] | aaru.com · techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation | ENC |
| 12 | B | Qualtrics Edge Audiences | Panel sintético dentro de Qualtrics | Millones de respuestas históricas de Qualtrics más PureSpectrum | Población general | NO; afirma "12 times better accuracy" que la IA genérica [tercero que cita al proveedor] | NO | **Solo EE.UU., inglés**; expansión "planned for 2026" | Add-on enterprise | fish.dog/news/synthetic-research-platforms-the-2026-market-map | ENC [tercero] |
| 13 | B | Evidenza | "Synthetic CMO" personas, B2B | No documentada | Ejecutivos B2B | NO; "0.87 correlation" [tercero que cita al proveedor] | NO | NO-ENC; no aplica a consumidor MX | Enterprise | valueaddvc.com (mismo artículo) | ENC [tercero] |
| 14 | B | ThinkNow Synthetic y ThinkNow MX | Sample sintético para completar huecos del panel | Panel DigaYGane (más de 1 millón de panelistas hispanos en EE.UU. y LatAm) | Multicultural; LatAm por país | NO | NO | ThinkNow MX incorporada en 2023; panel **en línea**; reconoce que en zonas rurales la participación en línea "still emerging" | Sin PM fees ni mínimo de pedido (dato de Brasil) [tercero] | thinknow.com/synthetic-synthetic-sample-solution/ · thinknow.com/blog/expanding-synthetic-sample-in-latam-balancing-trust-and-accuracy/ | ENC [afirma] |
| 15 | B | Buzzmonitor (Brasil) | Social listening con IA | Redes sociales | No aplica | NO-ENC: réplica de Top of Mind Folha (buscado: "Buzzmonitor Top of Mind Folha IA sintética") | NO | Brasil | Desde R$1,790 al mes | buzzmonitor.com/blog/ | NO-ENC (réplica) / ENC (precio) |
| 16 | B | WoskyLab (México) | "Sociedades simuladas" con agentes de IA sobre OASIS | "datos regionales" sin especificar | Edad, residencia, intereses | NO (solo promesa de verificación semanal pública) | NO | No declarada; dice que sus encuestas marcan "dirección e intensidad —no porcentajes de censo—" | No público | marketing4ecommerce.mx/woskylab-investigacion-de-mercadosl-con-inteligencia-artificial/ | ENC [afirma]; notas con tono de publirreportaje |
| 17 | B | Matria AI / TargetMax AI (Celestial Dynamics, México) | "más de 85 millones de gemelos digitales" a nivel manzana, AGEB, CP y municipio | INEGI/DENUE más NSE AMAI | Geográfica fina más NSE | NO; afirma "una precisión que no habíamos visto antes" sin cifra | NO | Nacional por construcción geográfica; conductas no validadas | No público; alianza con Meta [tercero] | matria.ai · celestialdynamics.io/portfolio-item/targetmax/ | ENC [afirma] |
| 18 | B | Synthetic Users | Encuestados sintéticos autoservicio | LLM | Por prompt | NO-ENC | NO | NO-ENC | US$2–27 por respondente sintético [tercero: Ditto, competidor] | askditto.io/news/simile-ai-review-2026-what-you-need-to-know | ENC (solo precio, fuente sesgada) |
| 19 | B | Artificial Societies | Simulación de audiencias | LLM | Por prompt | NO-ENC | NO | NO-ENC | Gratis a US$40 al mes [tercero: Ditto, competidor] | askditto.io (mismo) | ENC (solo precio, fuente sesgada) |
| 20 | C | LAPOP AmericasBarometer, Data Playground | Herramienta interactiva gratuita | Encuesta probabilística por ronda | Edad, sexo, escolaridad, región, urbano/rural, riqueza (ponderadores) | NO (descriptiva) | NO; microdatos con estratos y UPM para calcular IC | **Nacional** | Gratuito; ronda 2026 cargada desde el 9/sep/2026 | vanderbilt.edu/cgd/data-playground/ | ENC |
| 21 | C | Latinobarómetro, análisis en línea (JDSurvey) | Tabulación en navegador, todas las olas | Encuesta anual | Cortes sociodemográficos en la base (sin cita textual) | NO | NO | Nacional | Gratuito; ola 2025 en licitación (sin confirmar si ya está cargada) | latinobarometro.org/online-analysis | ENC |
| 22 | C | México ¿Cómo Vamos?, Semáforos | Tablero de indicadores contra metas | Datos oficiales | Estado y sector; micrositio de género | NO | NO | Nacional/estatal | Gratuito | mexicocomovamos.mx/semaforos-estatales/ | ENC |
| 23 | C | IMCO, Índice de Competitividad Estatal 2026 | Índices más bases de datos | 53 variables oficiales | Solo geográfica | NO | NO | 32 entidades | Gratuito | indices.imco.org.mx | ENC |
| 24 | C | México Evalúa | Informes y propuestas | Datos oficiales | No hay herramienta demográfica | NO | NO | Nacional | Gratuito | mexicoevalua.org | ENC (tablero propio NO-ENC) |
| 25 | C | Observatorio Nacional Ciudadano | Observatorio interactivo de incidencia delictiva | Registros SESNSP (no encuesta) | Geográfica y por delito | NO | NO | Nacional | Gratuito | delitosmexico.onc.org.mx/mapa | ENC |
| 26 | C | Banamex, "Los valores de los mexicanos" vol. VII (Alejandro Moreno) | Libro (digital gratuito) | WVS desde 1982 más encuesta Banamex 2003 y 2023 | Solo en el análisis del libro | NO | NO | Nacional | Gratuito; presentado en la FIL el 7/dic/2025 | elfinanciero.com.mx/nacional/2025/12/07/fil2025-alejandro-moreno-presenta-libro-en-el-que-explica-la-transformacion-de-la-sociedad-mexicana/ | ENC (estático) |
| 27 | D | INEGI, ENIF 2024 más Laboratorio de Microdatos y Procesamiento Remoto | Tabulados, microdatos y acceso restringido | Encuesta probabilística nacional (5.ª edición) | Sexo, tamaño de localidad, región; microdato completo | NO | NO; publica precisión muestral | **Nacional** | Gratuito; laboratorio con solicitud (sedes CIDE, ITAM) | inegi.org.mx/programas/enif/2024/ · inegi.org.mx/contenidos/app/microdatos/laboratoriodatos/doc/Solicitud_Uso.pdf | ENC |
| 28 | D | INEGI, medición de pobreza (ex CONEVAL) | Tabulados interactivos bienales | ENIGH | Entidad, tamaño de localidad, grupos de población | NO | NO; precisión por CV ("baja: CV ≥30") | Nacional | Gratuito | inegi.org.mx/desarrollosocial/pm/ | ENC |
| 29 | D | DataMéxico (Secretaría de Economía) | Visualizaciones interactivas, más de 50 repositorios | ENOE, Censo, comercio exterior | Estado, municipio, industria, ocupación | NO | NO | Nacional | Gratuito | economia.gob.mx/datamexico/ | ENC |
| 30 | D | CNBV, Reporte de Resultados ENIF 2024 | Informe de inclusión con razones de no tenencia | ENIF | Sexo, localidad | NO | NO | Nacional | Gratuito | cnbv.gob.mx/Inclusión/Anexos Inclusin Financiera/Reporte_ENIF2024.pdf | ENC |
| 31 | E | Behavioural Insights Team (LatAm) | Consultoría y RCT por proyecto | Datos de cada proyecto | Por proyecto | NO (RCT ex post) | NO | Proyectos (p. ej., Prospera) | Por proyecto | bi.team/articles/financial-inclusion/ | ENC |
| 32 | E | ideas42 | Diseño conductual por proyecto | Datos de cada proyecto | Por proyecto | NO | NO | Proyecto (estados de cuenta de afore) | Por proyecto (ONG) | ideas42.org/our-story | ENC |
| 33 | A–E | NIQ/Nielsen MX, GfK, Statista Consumer Insights, Mintel, Netquest/Kantar Profiles, Lexia, Brain, Provokers, Master Research, Mercawise, Feebbo; Semilattice, Electric Twin, CulturePulse, Expected Parrot, Panoplai, Viewpoints.ai, Simsurveys, BluePill, Prior Computers, Constellation Systems, Brox; CIDE, Colmex, ITAM (CESIG, Segmento), UNAM etnopsicología, WVS México; Nudge Lab, Laboratorio de Políticas Públicas CDMX | — | — | — | — | — | — | — | — | **PEND** |

### 2 · Respuestas a las preguntas de detalle (§3)

**Q1. ¿Algún producto para México publica "predije X antes de la ola, la ola dijo Y"?** NO-ENCONTRADO. Buscamos en los sitios de Toluna, YouGov Parallax, Aaru, ThinkNow, WoskyLab, Matria AI, Worldpanel, Euromonitor, GWI y en la prensa sobre Simile. Lo más parecido en México es la revisión bienal de la Regla AMAI contra cada ENIGH nueva, que reporta ajuste (Pseudo-R² 0.4852 con ENIGH 2022) y no predicción conductual. WoskyLab promete verificación semanal pública; no encontramos resultados. Fuera de México, Aaru tiene un acierto (primaria de NY "within 371 votes") y un fallo (predijo victoria de Harris) reportados por Replism, y Gallup anuncia que publicará sus resultados de validación de Simile.

**Q2. ¿Alguien reporta cobertura de intervalo para segmentos mexicanos?** NO-ENCONTRADO. INEGI publica coeficientes de variación, que miden solo el error muestral, con umbrales como "Nivel de precisión moderada: CV [15,30)". YouGov promete "a calculable margin of error" que viene de la muestra humana de validación, no del modelo. El preprint arXiv 2609.13148 (Tigre y Souto, jun/2026) propone un estimador AIPW doblemente robusto con muestra de calibración de n = 50–300 para inferencia válida [literatura]. Está validado en simulaciones y en la ANES (EE.UU.), no en México.

**Q3. ¿Qué gemelos tienen datos de entrenamiento con representatividad nacional mexicana?** Ninguno de los que declaran México lo documenta. Toluna usa "first-party data" de su comunidad *en línea*. ThinkNow MX usa el panel en línea DigaYGane y reconoce que en las zonas rurales la investigación en línea está "still emerging". Su respuesta es modelar sintéticamente a esos grupos a partir de "seed data" del panel [afirma]; es decir, extrapola a los desconectados desde los conectados. Matria AI parte de INEGI/DENUE y NSE AMAI, lo que da cobertura geográfica nacional, pero no publica validación conductual. YouGov y Simile no documentan México.

**Q4. ¿Cómo se comercializa el conocimiento del consumidor en México?**
- **Suscripción sindicada:** Worldpanel, Euromonitor Passport, GWI.
- **Informe individual de pago:** los informes-país de Euromonitor, en PPT.
- **Plataforma más add-on sintético:** Toluna Start y YouGov Parallax, que se ofrece a suscriptores.
- **Enterprise sin precio público:** Simile y Aaru.
- **Autoservicio barato:** Synthetic Users, de US$2 a 27 por respondente, y Artificial Societies, de gratis a US$40 al mes. Ambos precios vienen de una reseña de Ditto, competidor directo.
- **Por proyecto:** BIT, ideas42 y las agencias locales.
- **Gratuito:** INEGI, LAPOP, Latinobarómetro, DataMéxico.

No hay en México un mercado visible de API conductual con precio público.

**Q5. ¿Alguien publica la exclusión por oferta al lado de la conducta financiera?** PARCIAL, y solo en fuentes oficiales. El boletín ENIF 2024 de INEGI reporta que, entre quienes nunca han tenido crédito formal, las razones fueron "no le gusta endeudarse (38.4 %), no le interesa o no lo necesita (25.8 %), no cumple con los requisitos (20.7 %) y los intereses o comisiones son altas (7.8 %)". También incluye categorías como "la sucursal le queda lejos o no hay" y "cree que le van a rechazar". Para las cuentas, la CNBV reporta que 26% nunca ha tenido una. Las razones son no necesitarla (36%), ingresos insuficientes (30%), no saber usarla (9%) y no cumplir requisitos (8%). En el lado empresarial, la ENAFIN 2024 reporta un rechazo de 6.3% de las solicitudes de crédito, según La Silla Rota. Todo esto se publica como tabulado aparte. No encontramos un producto comercial que lo ponga como columna estándar por segmento.

**Q6. ¿Hay reclamaciones de "predicción del cambio entre olas" para México contrastadas contra INEGI?** NO-ENCONTRADO un contraste. Sí hay afirmaciones de predicción sin métrica. Matria AI dice "no solo predice comportamientos, los simula… con una precisión que no habíamos visto antes", según ITSitio. Su propio producto TargetMax aclara que "los resultados son herramientas de soporte a la decisión, no garantías". Esto no documenta "humo": documenta una afirmación sin evidencia pública, que es distinto.

**Q7. ¿Qué dice la literatura 2025–2026?**
- **NIM (2025–2026) [literatura]:** con la elicitación por similitud semántica, los sintéticos todavía "overestimates brand attitudes and exhibits less variation than real respondents". NIM los considera aptos sobre todo para "early-stage concept testing or lower-stakes applications" y recomienda benchmarking contra datos humanos, tanto por respondente como por muestra.
- **Tigre y Souto (arXiv 2609.13148) [literatura]:** documentan "subgroup error balloons of 10–30 percentage points" y correcciones globales que empeoran el sesgo demográfico. Citan que la rectificación PPI++ aumentó el sesgo en mujeres en 58.5% (Krsteski et al., 2025).
- **Taday Morocho et al. (WWW Companion 2026) [literatura]:** con microdato WVS de EE.UU. y más de 70,000 instancias respondente-ítem, el persona prompting "does not yield a clear aggregate improvement… and, in many cases, significantly degrades performance".
- **Auditoría psicométrica (arXiv 2608.14606) [literatura]:** encuentra aquiescencia de +0.84 DE en promedio. Además, los modelos entrenados con datos sintéticos predicen peor que la media (R² = −0.18).
- **Maier et al. (2025), PyMC Labs con Colgate [literatura]:** en 57 encuestas con 9,300 respuestas humanas, lograron 90% de la confiabilidad test-retest humana en intención de compra.
- **HBR (nov/2025) [literatura/divulgación]:** recomienda estudios paralelos periódicos sobre las personas reales detrás del panel de gemelos.

Sobre **mercados emergentes o en español** no encontramos ningún estudio de validez específico de México ni en español. El estudio más cercano no angloparlante es el coreano (arXiv 2608.28615). No verificamos el special issue del IJRM ni la pieza de MIT Sloan (PEND).

**Q8. ¿Qué pasó con AMAI NSE?** Sigue vigente la Regla AMAI 2024: siete niveles, seis características del hogar y la escolaridad del jefe de hogar. El Comité la revisa cada dos años con cada ENIGH. Con ENIGH 2022, AMAI concluyó: "Los Niveles Socioeconómicos cambiaron su distribución, sin embargo, la Regla AMAI 2024 permanece igual". La nomenclatura indica el año de vigencia, dos años después de la ENIGH que la valida. No encontramos si ya se publicó una revisión con ENIGH 2024. En la práctica, Matria AI usa NSE AMAI y GWI usa cuotas propias de edad, sexo y escolaridad. Los gemelos globales no mencionan AMAI: cada quien usa la segmentación de su panel.

### 3 · Veredicto por propiedad

| Propiedad | Quién la tiene | Quién la aproxima | Quién la afirma sin evidencia |
|---|---|---|---|
| **P1. Validación prospectiva sellada con historial público** | Nadie, para México ni, en lo encontrado, en el mundo | Aaru (un acierto y un fallo electorales en EE.UU. [tercero: Replism]); Gallup–Simile (validación en curso, resultados pendientes); YouGov Parallax (validación humana *contemporánea*, no ex ante); AMAI (revisión retrospectiva bienal de la regla NSE) | WoskyLab (promete verificación pública semanal); Matria AI ("predice"); Toluna ("enhances predictive accuracy") |
| **P2. Incertidumbre calibrada con cobertura medida** | Nadie | INEGI (CV muestral); YouGov (margen de error de la muestra de validación); Simile ("confidence model that predicts the accuracy of every simulation", comunicado vía Pulse 2.0); literatura: AIPW de Tigre y Souto, held-out de 200 particiones en el estudio coreano | Ninguno afirma cobertura; varios afirman "precisión" sin universo (Simile 85% GSS, Aaru 0.90, Evidenza 0.87, Qualtrics "12 times") |
| **P3. Persistencia como piso que ningún retador vence** | Nadie como producto | Literatura: la ola previa (3.7 pp) venció al sintético calibrado (7.0–7.5 pp) en Corea (Kim y Cho, arXiv 2608.28615); YouGov: los sintéticos "cannot reliably track shifts" y Parallax no reemplaza trackers | — (nadie afirma lo contrario con datos para México) |

### 4 · Los tres más cercanos

**1. YouGov Parallax.** Es lo más cercano en espíritu: "Every other simulated research product asks you to trust the AI and hope for the best. YouGov Parallax keeps the receipts."
- *Le falta:* no sella predicciones antes de la ola; valida contra humanos al mismo tiempo. No publica cobertura de intervalo. Su México, si está dentro de los 49 mercados, sería de internautas. Ellos mismos dicen que no sirve para medir cambio en el tiempo.
- *Dónde gana:* responde cualquier pregunta nueva (nosotros solo las que INEGI ya hizo). Entrega en 30 minutos, con un panel vivo de más de 30 millones y la marca de un encuestador con historial electoral.

**2. Gallup–Simile.** Es la validación más seria del mercado: Gallup compara contra estimaciones probabilísticas de su propio panel, a respondente, encuesta y población.
- *Le falta:* es solo EE.UU., sus resultados siguen sin publicarse y no es prospectiva por olas.
- *Dónde gana:* capital (Serie B de US$200M con valuación de US$2B liderada por Greenoaks [TechCrunch, 30/jul/2026]), pedigrí académico, un panel probabilístico y un validador institucional con 90 años de marca.

**3. Matria AI (Celestial Dynamics).** Es lo más cercano en *datos*: INEGI/DENUE más NSE AMAI, con cobertura nacional por manzana.
- *Le falta:* toda validación publicada, intervalos y dominios conductuales fuera de consumo.
- *Dónde gana:* granularidad geográfica (manzana y AGEB, frente a nuestros segmentos sociodemográficos), producto comercial vivo para pymes, la alianza reportada con Meta y un discurso de venta simple.

**Mención pública:** LAPOP Data Playground es gratuito, nacional, se actualiza por ola (la 2026 desde el 9/sep/2026) y tiene cortes por edad, sexo, escolaridad y región. No predice ni calibra, pero es el mejor "catálogo por segmento" público y un competidor natural en el dominio Estado y corrupción.

**Lo que nos falta a nosotros frente a todos:**
- Solo contestamos preguntas que alguna encuesta oficial ya hizo, con la cadencia de sus olas.
- Medimos conducta *reportada*, no observada; Worldpanel mide compras reales.
- Seis evaluaciones en cinco dominios es una n pequeña para afirmar calibración.
- No tenemos cobertura de marcas ni de categorías de consumo, que es lo que compran los equipos de marketing.

### 5 · Oportunidad de posicionamiento: "nuestro piso calibrado como benchmark del gemelo digital del mexicano"

**Evidencia a favor:**
- La demanda del benchmark es explícita. NIM pide "benchmarking against human-generated data" [literatura]. HBR recomienda estudios paralelos periódicos. Gallup construye un programa de validación y YouGov basa todo su argumento de venta en la validación.
- El estudio coreano demuestra que la persistencia es el rival correcto y que el sintético sin corregir (13.7/14.4 pp) pierde incluso contra la media general (11.1 pp) [literatura].
- Toluna y ThinkNow ya venden sintéticos para México sin métrica pública. Eso deja un hueco para un árbitro con marco probabilístico nacional, que incluya población rural e informal.
- Tigre y Souto muestran que basta una muestra de calibración chica (n = 50–300) para corregir. Un piso INEGI por segmento podría ser esa referencia.

**Evidencia en contra:**
- El mercado resuelve la validación de forma vertical: YouGov valida con su propio panel y Simile con su socio Gallup. No encontramos precedente de un tercero independiente que venda calibración de gemelos (NO-ENCONTRADO).
- Nuestros benchmarks cubren dominios cívicos y financieros; los gemelos se usan sobre todo en claims testing, conceptos y precios, donde INEGI no pregunta.
- Las olas oficiales son lentas: ENIF 2018, 2021 y 2024; ENIGH bienal. Un benchmark que se actualiza cada 2–3 años no sirve para validación rápida.
- La propia industria ya lo concede: el informe del AAPOR Task Force on Responsible AI Integration in Survey Research (mayo/2026), copresidido por David M. Rothschild (Microsoft Research) y Jenny Marlar (Gallup), dice que el uso "is more directed at augmentation than full automating", y YouGov declara que Parallax no reemplaza trackers. Nuestra tesis central puede leerse como algo que el mercado ya concede.

**Posición recomendada:** no venderse como "competidor de gemelos", sino como **estándar de referencia auditable para México**. Eso significa publicar el piso de persistencia por segmento y dominio, con la cobertura medida, e invitar a Toluna, ThinkNow, Matria y YouGov a medirse contra él. El precedente más cercano es la función de AMAI con el NSE: un estándar industrial revisado contra cada ENIGH. Buscar el aval de AMAI o de un grupo académico (CIDE o ITAM, que ya tienen acceso al laboratorio de microdatos) daría la neutralidad que un vendedor no tiene.

### 6 · Riesgos: quién puede replicar en 6–12 meses

| Actor | Qué ya tiene | Qué le falta | Probabilidad |
|---|---|---|---|
| Matria AI / Celestial Dynamics | INEGI más NSE AMAI, producto vivo, alianza con Meta | Cultura de validación publicada | Alta en catálogo; baja en historial |
| ThinkNow MX | Entidad en México (2023), panel LatAm, sintético | Marco probabilístico | Media |
| WoskyLab | Discurso de verificación pública | Datos declarados | Media en narrativa, baja en rigor |
| Worldpanel by Numerator / Kantar | Panel de compras real, marca | Interés en dominios cívicos | Baja |
| Academia (CIDE, ITAM) | Laboratorio de microdatos INEGI | Producto y distribución | Media, y además es aliado potencial |
| YouGov / Toluna | Capital, infraestructura sintética, México en catálogo | Microdato oficial | Media si deciden entrar |

**Lo que protege:** un historial sellado no se puede fabricar hacia atrás. Un recién llegado podría hacer backtesting "pseudoprospectivo" con olas viejas, pero no puede demostrar que no vio la ola. Solo con predicciones selladas de forma verificable por terceros (sello de tiempo o hash público) el foso es real. Con el calendario de olas, igualar seis evaluaciones tomaría años.

**Lo que no protege:** el catálogo, las reglas SI–ENTONCES y el motor de consulta se pueden replicar con microdato público y un LLM. La ventaja depende de publicar ya y de forma verificable, antes de que alguien haga pasar backtesting por predicción.

## Recommendations

1. **Hacer público y verificable el sellado** (hash o sello de tiempo de terceros) de cada estimador antes de la próxima ola: ENVIPE, ENIGH 2026 o ENIF. Es el único activo que no se puede copiar.
2. **Publicar una "tabla de piso" por segmento** (persistencia más intervalo con cobertura medida) y retar por escrito a Toluna, ThinkNow, Matria y YouGov Parallax a medirse contra ella en México, citando la advertencia de YouGov sobre el cambio en el tiempo.
3. **Adoptar la Regla AMAI 2024 como corte adicional** para que los compradores de la industria reconozcan la segmentación, y proponer a AMAI un rol de arbitraje.
4. **Mantener la columna de exclusión por oferta** como diferenciador: nadie la pone junto a la conducta, aunque INEGI ya ofrece la materia prima (p. ej., 20.7% "no cumple con los requisitos").
5. **No competir en velocidad ni en preguntas arbitrarias**: ahí ganan YouGov y Toluna. Competir en credibilidad auditada.

## Caveats

- **Cobertura incompleta:** por el límite de búsqueda de esta sesión, 30 proveedores de la lista del brief quedaron **PEND** (fila 33). Son NIQ, GfK, Statista, Mintel, Netquest, varias agencias mexicanas, varios sintéticos (Semilattice, Electric Twin, CulturePulse, Expected Parrot, Panoplai y otros) y la academia (CIDE, Colmex, ITAM, UNAM). No es lo mismo que NO-ENCONTRADO: no se buscaron. Conviene una segunda pasada antes de afirmar que "nadie" tiene P1–P3.
- **Fuentes secundarias y sesgadas:** la valuación de Simile (US$2B) está confirmada por TechCrunch (30/jul/2026); las cifras de Evidenza y Qualtrics vienen de blogs de industria (valueaddvc, fish.dog, Replism), no de comunicados primarios. Los precios de Synthetic Users y Artificial Societies vienen de Ditto, que es competidor. Las notas sobre WoskyLab y Matria tienen tono de publirreportaje.
- **Inconsistencia:** Worldpanel reporta 82% y 84% de cobertura urbana en páginas distintas.
- **Sin datos de precio:** Worldpanel, Euromonitor, GWI, YouGov, Toluna y Simile no publican precios (NO-ACCESIBLE sin contacto comercial).
- **Lista de fuentes:** la columna URL de la tabla y las URL citadas en el texto forman el registro de procedencia. Todas se consultaron el 23/sep/2026. Las de pago o con acceso restringido están marcadas en la tabla: Euromonitor, Worldpanel, GWI, YouGov Parallax enterprise, Toluna Start y el Laboratorio de Microdatos INEGI (por solicitud).
- Este informe no evalúa la calidad de nuestro método (§6 del brief). Las comparaciones de propiedades se basan solo en lo que cada actor publica.