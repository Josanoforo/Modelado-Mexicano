# Barrido público de 17 condiciones clasificadas "no existe fuente"

*5 de agosto de 2026. Encargo externo (analista de fuentes de datos), sin número de mesa asignado — no es un `ENCARGO` archivado en `forense/encargos/`, es un barrido de descubrimiento de candidatas, mismo género que `cruce-catalogo-fichas-v2_0.md` y `2026-08-05-p3-r8-1-contradiccion-inventario.md`. No adjudica ningún veredicto `RX.Y`, no edita ninguna ficha del pre-registro, no descarga ningún microdato. Produce candidatas con URL para que un acto posterior (con red y perímetro propio) las abra y verifique.*

## 0 · Por qué este acto existe y qué NO hace

La motivación explícita del encargo: cuatro verificaciones recientes de la etiqueta "no existe fuente" resultaron falsas, la última hace horas — el barrido interno del programa (`cruce-catalogo-fichas-v2_0.md:47`) ya reconocía, con reserva declarada, que **nadie había buscado específicamente un padrón de AGROASEMEX/Fondos de Aseguramiento** para R1.1. Este acto reabre las 17 condiciones que el programa tenía clasificadas como "ninguna encontrada" o "dato propietario, no existe", sin heredar ninguna clasificación previa, y busca desde cero en datos.gob.mx, portales de dependencia, transparencia, repositorios académicos, organismos internacionales y datos comerciales/sindicados.

**Método.** Cuatro agentes de investigación en paralelo, cada uno con las fichas completas del pre-registro (`hitoD-preregistro-v2_0.md`: falsador, umbral, confusor a aislar) para no re-derivar el objeto de búsqueda. Cada uno ejecutó entre 46 y 62 búsquedas reales (`WebSearch`).

⚠️ **Limitación real de esta sesión, declarada por los cuatro agentes de forma independiente y verificada contra un dominio de control neutral (`example.com`, Wikipedia): `WebFetch` devolvió `403` (policy denial del proxy del entorno, no de los sitios de destino) en el 100% de los intentos.** Esto significa que ninguna URL de abajo fue abierta y leída byte a byte en esta sesión — todas provienen de `WebSearch`, que sí trae contenido indexado real (texto citable, no inventado) de las páginas fuente, pero es evidencia de segunda mano, no verificación directa de contenido/diccionario de campos. Se marca explícitamente en cada fila donde esto deja un hallazgo sin confirmar al 100%. **Recomendación operativa:** un acto siguiente con `WebFetch` funcional debería abrir directamente las URLs marcadas como pendientes de confirmación antes de que cualquiera de estas candidatas se promueva a ficha o se abra como fuente.

**Convención de columnas**, igual para las 17 tablas: EXISTE (Sí/No/Parcial) · FUENTE (institución, nombre exacto, URL) · GRANULARIDAD · COBERTURA TEMPORAL · ACCESO · FORMATO · QUÉ LE FALTA · CLASIFICACIÓN. La clasificación usa el esquema del encargo, no el esquema A/B/C/D del pre-registro del programa (que es sobre desenlaces de falsador, no sobre existencia de fuente) — para evitar la confusión, aquí se escribe siempre con el nombre completo:

- **EXISTE-SATISFACE** — el dato cubre la condición tal como está escrita.
- **EXISTE-NO-SATISFACE** — existe, falta algo específico (se dice qué).
- **NO-ENCONTRADO** — se buscó y no apareció; no es "no existe". Se dice dónde y con qué términos.
- **NO-ACCESIBLE** — pago, tarjeta, afiliación institucional o restricción legal. El registro gratuito (LAPOP, datos.gob.mx) o aceptar términos de uso **no** cuenta aquí.

---

## Ficha 1 (R1.1) · Padrón de Fondos de Aseguramiento agrícola, por productor y ciclo

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial |
| **FUENTE** | AGROASEMEX / `datos.gob.mx`. Datasets: *Subsidio Seguro Agropecuario* (`datos.gob.mx/dataset/subsidio_seguro_agropecuario`), *Bases de datos del programa de Aseguramiento Agropecuario, componente de subsidio, ramo Agrícola/Ganadero* (`datos.gob.mx/busca/dataset/bases-de-datos-del-programa-de-aseguramiento-agropecuario-componente-de-subsidio-para-el-ramo-g`), *Padrón de integrantes del Sistema Nacional de Aseguramiento Agropecuario* (`datos.gob.mx/busca/dataset/padron-de-integrantes-del-sistema-nacional-de-aseguramiento-agropecuario-que-se-integra-por-los`). Organización completa: `datos.gob.mx/organization/agroasemex` (4 bases, última actualización reportada 9/feb/2026). API CKAN: `datos.gob.mx/api/3/action/package_show?id=subsidio_seguro_agropecuario`. |
| **GRANULARIDAD** | Mixta. El "padrón de integrantes del sistema" es a nivel de **Fondo/asegurador**. Las bases de "subsidio" apuntan, por diseño normativo (CIPA — Cédula de Inscripción al Padrón de Asegurados, anexa a las Reglas de Operación SHCP/DOF), a **productor individual** — no confirmado por lectura directa del archivo si el recurso descargable expone folio/nombre o llega ya agregado. |
| **COBERTURA TEMPORAL** | 1992–2023, con actividad reportada hasta 2025/2026 — registro continuo actualizado por ciclo/año, no corte único. |
| **ACCESO** | Descarga directa, sin registro (CKAN). |
| **FORMATO** | Probablemente CSV/XLSX vía CKAN (no confirmado por fetch). |
| **QUÉ LE FALTA** | Dos cosas puntuales: (1) no está confirmado que el campo temporal sea **ciclo agrícola** (primavera-verano / otoño-invierno) y no año fiscal; (2) no hay evidencia de una columna que distinga **voluntario** de **obligatorio-atado-a-crédito-de-avío** — la CIPA regula el estatus jurídico del Fondo, no necesariamente expone ese campo en el dato abierto. Nota importante: `hitoD-R1.1-veredicto-v1_0.md` (28/jul/2026) ya investigó a fondo este dominio con otras fuentes (ENA 2017, AMUCSS, SADER) y concluyó veredicto **D — inejecutable**, pero por una razón estructural distinta (la población de volatilidad máxima, productores de temporal, está excluida por diseño de mercado — concentración 62-66% en Sonora-Sinaloa-Tamaulipas, riego no temporal) — no porque faltara el padrón. Este barrido no reabre ese veredicto; solo confirma que el padrón por productor sí existe y es descargable, lo cual no estaba verificado antes. |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE.** El padrón existe, por productor y por Fondo, con serie larga — pero sin confirmación de desagregación por ciclo agrícola ni de un campo voluntario/obligatorio. Un acto con `WebFetch` funcional debería abrir el CSV y el diccionario de datos antes de descartar o promover esta candidata. |

## Ficha 2 (R1.3) · Canal de alta desagregado, sin programa de referidos que explique el grueso de las altas

| Campo | Detalle |
|---|---|
| **EXISTE** | No, a nivel de cifra desagregada; parcial como declaración cualitativa suelta. |
| **FUENTE** | Ninguna fuente regulatoria (CNBV — bases de datos de inclusión financiera `cnbv.gob.mx/Inclusi%C3%B3n/Paginas/Bases-de-Datos.aspx`, Banxico, CONDUSEF) mide canal de adquisición de clientes; el "Acceso" de CNBV mide infraestructura (sucursales/cajeros/banca móvil), no canal de captación. COFECE, *Estudio de competencia y libre concurrencia en el sector fintech* (`cofece.mx/wp-content/uploads/2024/10/Estudio-Fintech.pdf`), toca costo de adquisición de forma agregada y cualitativa ("puede superar 200 USD en no bancarizados"), sin desglose por canal. Finnovista *Fintech Radar México* (`finnosummit.com`, encuesta anual a ~200 fintechs) es la candidata más prometedora a nivel industria, pero no se confirmó que su cuestionario traiga canal de adquisición desagregado. Prensa (Cronista, La Silla Rota, El Heraldo, marzo-abril 2026) cita a Nu México declarando que su crecimiento de 5 a 15 millones de clientes está "sustentado en el boca a boca" y el "programa de referidos", sin dar porcentaje. |
| **GRANULARIDAD** | N/A — no existe el dato desagregado; lo más cercano es industria (Finnovista) o anecdótico por empresa (Nu, sin cifra). |
| **COBERTURA TEMPORAL** | N/A. |
| **ACCESO** | No público en la forma requerida. |
| **FORMATO** | N/A. |
| **QUÉ LE FALTA** | Un cruce cuantitativo (%) de canal de adquisición (referido/pauta/orgánico/partnership), por empresa o agregado por industria. No existe en ninguna fuente identificada. |
| **CLASIFICACIÓN** | **NO-ENCONTRADO.** Búsquedas en CNBV, Banxico, CONDUSEF, COFECE, Finnovista/Finnosummit, prensa especializada sobre Nu/Kueski/Klar/Konfío. **Límite de clase parcial, no absoluto:** el dato exacto de atribución (de dónde vino cada cliente) es interno de CRM/marketing de cada empresa y no observable desde fuera por un regulador — pero una encuesta a consumidores bien diseñada ("¿cómo conociste tu app financiera?") sí podría producirlo sin acceso a sistemas internos, y esa encuesta simplemente no existe públicamente en México. Es un límite de la vía regulatoria, no un límite absoluto de la clase de dato. |

## Ficha 3 (R1.4) · Prima pagada por marca sobre sustituto funcional equivalente en D/E ≤ la de A/B

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí, el panel existe; el cruce específico es propietario. |
| **FUENTE** | **Kantar Worldpanel / Worldpanel by Numerator México** (`kantar.com/latin-america/latinoamerica/mexico`, `market.worldpanelbynumerator.com/mx`) — panel de 8,500 hogares, 82-84% cobertura urbana, ~100 categorías, sí segmenta por NSE. **NielsenIQ (NIQ) México** publica agregados gratuitos citables sin cruce NSE (`nielseniq.com/global/es/insights/analysis/2025/la-vision-completa-del-consumo-en-mexico-2025`, `.../key-takeaways-mexico-2025`): 69% ve marca propia como opción de calidad, 40% ha sustituido marca comercial por marca propia; el cruce por NSE exige el producto pagado *Full View™* (`nielseniq.com/global/en/insights/report/2025/full-view-measurement`). GfK: sin evidencia de panel independiente activo en México. Buró de Crédito: solo historial crediticio individual, no gasto por marca/NSE. ANTAD/Concanaco: estudios económicos sin cruce marca-NSE. |
| **GRANULARIDAD** | Hogar (panel, tracking semanal de compras). |
| **COBERTURA TEMPORAL** | Continua/semanal; históricos vía suscripción. Resúmenes gratuitos: anuales. |
| **ACCESO** | Panel completo con cruce NSE × marca/genérico: **de pago**, modelo B2B/licencia corporativa, sin tarifa pública listada, se contrata directo con Kantar/NIQ. Resúmenes agregados sin NSE: gratuitos. |
| **FORMATO** | Panel: dashboard/entregables bajo contrato. Resúmenes: PDF/HTML. |
| **QUÉ LE FALTA** | El cruce exacto (prima D/E vs A/B) no aparece en ningún material gratuito — casi con certeza existe dentro del panel pagado (es justo lo que estos paneles producen de rutina), pero no se publica sin comprar. |
| **CLASIFICACIÓN** | **NO-ACCESIBLE** (pago/suscripción corporativa) para el cruce exacto. Los agregados sin NSE están cerca de EXISTE-NO-SATISFACE pero no cubren la condición. No es límite de clase: es un dato que la industria recolecta rutinariamente, detrás de un muro de pago. |

## Ficha 4 (R2.1) · Diferencia <20pp en tasa de reporte voluntario de errores, jerarquía tradicional vs. plana, canal pareado

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial. |
| **FUENTE** | Secretaría de la Función Pública, **Encuesta de Clima y Cultura Organizacional (ECCO)** — anual desde 2002, 287 instituciones de la APF, 1,017,478 respondentes en 2023. Dataset: `datos.gob.mx/dataset/encuesta_clima_cultura-organizacional`; reportes por dependencia, p. ej. `gob.mx/cms/uploads/attachment/file/907022/SE_REPORTE_GENERAL_ECCO_2023.pdf`. Complementaria: **World Bank Enterprise Surveys México 2023** (`microdata.worldbank.org/index.php/catalog/6453`), sección R de "management practices". Great Place to Work México publica un Índice de Confianza agregado (87% favorabilidad, 2026) sin desglose por jerarquía ni canal — dato propietario de GPTW. |
| **GRANULARIDAD** | Individuo, agregable por institución/establecimiento (ECCO); establecimiento (Enterprise Survey). |
| **COBERTURA TEMPORAL** | ECCO: 2002-2023, anual. Enterprise Survey México: 2006, 2010, 2023. |
| **ACCESO** | ECCO: descarga directa (PDF por dependencia). Enterprise Survey: requiere registro gratuito (cuenta como accesible). |
| **FORMATO** | ECCO: PDF agregado. Enterprise Survey: microdato descargable tras registro. |
| **QUÉ LE FALTA** | ECCO cubre solo sector público federal, no representa empresas privadas ni jerarquía tradicional/familiar del sector privado, que es el objeto real de la ficha (`R2.1`: "empresa familiar mexicana de jerarquía tradicional"). Ninguna de las dos trae la métrica pareada (reporte de errores × canal anónimo/no-anónimo × tipo de jerarquía tradicional/plana). |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE**, con **límite de clase declarado explícitamente**: la conducta de reporte de errores ligada a diseño de canal (anónimo/no) y tipo de jerarquía es dato interno de sistema de incidencias de cada empresa privada — ninguna encuesta pública agregada la captura por diseño; ECCO se acerca pero mide sector público, no empresa familiar tradicional. |

## Ficha 5 (R2.2) · Rotación y productividad ±10pp, liderazgo autoritario no-benévolo vs. benévolo

| Campo | Detalle |
|---|---|
| **EXISTE** | No, a nivel de fuente pública representativa. |
| **FUENTE** | Estudios académicos puntuales, Redalyc/Scielo: *Antecedentes de la rotación voluntaria de personal* (institución financiera mexicana, n=142, `scielo.org.mx/scielo.php?script=sci_arttext&pid=S2448-76782006000100007`); *Rotación de personal en la industria hotelera de Guanajuato* (`redalyc.org/journal/3312/331267304006`). STPS/IMSS: altas-bajas agregadas, sin variable de liderazgo. ENOE-INEGI: panel de transiciones de empleo individual, sin módulo de estilo de liderazgo. AMEDIRH publica tasa nacional de rotación (17% en 2025) sin variable de liderazgo. |
| **GRANULARIDAD** | Empresa individual (estudios de caso, n=67-253). |
| **COBERTURA TEMPORAL** | Estudios puntuales 2006-2021, sin serie nacional. |
| **ACCESO** | Académico abierto y gratuito. |
| **FORMATO** | Artículos PDF. |
| **QUÉ LE FALTA** | (1) dato objetivo de rotación real, no intención autoreportada; (2) tipología validada de liderazgo autoritario-benévolo vs. no-benévolo; (3) control por sector/salario/prestaciones; (4) muestra multi-empresa representativa nacional. |
| **CLASIFICACIÓN** | **NO-ENCONTRADO.** Búsquedas en STPS/datos.gob.mx, IMSS, ENOE, AMEDIRH, Redalyc, Scielo. **Límite de clase declarado explícitamente:** cruzar rotación/productividad objetiva de nómina interna con un instrumento psicométrico de liderazgo aplicado a los mismos supervisores, controlando sector-salario-prestaciones, exige combinar datos propietarios de cada empresa — ninguna estadística pública mexicana está diseñada para vincularlos a ese nivel. |

## Ficha 6 (R4.1, primera fila) · Reducción <25% en uso de farmacia-con-consultorio tras mejora de acceso público, diseño panel/evento fechado

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial. |
| **FUENTE** | DGIS/Secretaría de Salud. Catálogo **CLUES**: `dgis.salud.gob.mx/contenidos/sinais/s_clues.html`; descarga directa `dgis.salud.gob.mx/descargas/datosabiertos/recursosSalud/CLUES_2015.csv`; en `datos.gob.mx`: `datos.gob.mx/dataset/?q=catalogo-de-clave-unica-de-establecimientos-de-salud-clues`. Subsistema **SINERHIAS**: `dgis.salud.gob.mx/contenidos/sinais/s_sinerhias.html`. Snapshots históricos fechados: `gobi.salud.gob.mx/Bases_Clues.html`. Manual de registro: `dgis.salud.gob.mx/descargas/clues/pdf/Manual_registro_informacion_catalogo_CLUES_202506.pdf`. |
| **GRANULARIDAD** | Establecimiento (clave CLUES individual). |
| **COBERTURA TEMPORAL** | Registro administrativo continuo; catálogo CLUES actualizado diariamente con cortes mensuales (según resumen de `datos.gob.mx`); SINERHIAS con revisión semestral; snapshots históricos fechados por año disponibles en GOBI Salud. |
| **ACCESO** | Descarga directa, sin registro (CSV/KMZ). |
| **FORMATO** | CSV, KMZ, PDF. |
| **QUÉ LE FALTA** | El trámite de alta de CLUES sí captura una "fecha de inicio de operaciones" (confirmado por snippets del trámite), pero **no se confirmó si esa fecha es columna del catálogo público descargable** o solo vive en el sistema interno de captura (AppClues). Alternativa viable no confirmada como automática: diferenciar (`diff`) dos snapshots fechados de CLUES para inferir aparición de un establecimiento entre fecha A y B — proxy de apertura sin fecha exacta de día, requiere trabajo de reconstrucción. |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE.** La infraestructura de datos (catálogo + históricos + SINERHIAS) existe; la columna de fecha de apertura explícita en el archivo descargable no quedó verificada — pendiente de un acto con `WebFetch` funcional que abra el CSV real y el manual. |

## Ficha 7 (R4.1, segunda fila) · Trato medido (confusor a aislar) — declarado hasta hoy como ESTAD / "ENSATD"

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí — corrección de nombre: el instrumento real es **ESTAD / SESTAD**, no "ENSATD". |
| **FUENTE** | Secretaría de Salud, Dirección General de Calidad y Educación en Salud (DGCES), con INSP, desde 2015. **Encuesta de Satisfacción, Trato Adecuado y Digno (ESTAD)**, operada vía el **Sistema de la Encuesta de Satisfacción, Trato Adecuado y Digno (SESTAD)**. Portal: `calidad.salud.gob.mx/site/calidad/encuesta_satisfaccion_trato_digno.html`; sistema de captura: `desdgces.salud.gob.mx/sestad/index.php`; reportes anuales: `calidad.salud.gob.mx/site/calidad/docs/2023/SESTAD_reporte_2021.pdf`, `.../2024/SESTAD_reporte_2023.pdf`; instructivo: `calidad.salud.gob.mx/site/calidad/docs/instructivo_estad_c_externa.pdf`. |
| **GRANULARIDAD** | Individuo (encuestado), agregable por establecimiento (CLUES). |
| **COBERTURA TEMPORAL** | **No es transversal única vez** — levantamiento continuo con cortes **cuatrimestrales** por establecimiento, activo desde 2015 (reportes confirmados 2021 y 2023). Esto en principio permite un diseño antes/después pareado con un evento de apertura/mejora de unidad (Ficha 6), si el microdato desagregado es accesible. |
| **ACCESO** | Reportes agregados nacionales/estatales: descarga directa, sin registro. **No confirmado** si el microdato individual (respuesta por respuesta, por establecimiento y corte) es descargable públicamente o restringido a "coordinadores de calidad" institucionales dentro de SESTAD. |
| **FORMATO** | PDF (agregado); sistema de captura web (exportación de microdato no confirmada). |
| **QUÉ LE FALTA** | Confirmar si el microdato cuatrimestral por establecimiento es público o requiere credencial institucional — es la única pieza útil para parear con Ficha 6. No se encontró evidencia de que ENSANUT mida "trato" en el mismo módulo que uso de farmacia-con-consultorio (hay estudios de "percepción de calidad de la atención" en ENSANUT, p. ej. `scielo.org.mx/pdf/spm/v55s2/v55s2a5.pdf`, pero no confirmado que compartan módulo). |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE**, con posible componente **NO-ACCESIBLE** si el microdato resulta restringido a personal del sector salud — pendiente de confirmar. El diseño del instrumento (por establecimiento, cuatrimestral) sí cumpliría la condición si el microdato es abierto. |

## Ficha 8 (R7.3) · RDD sobre Pensión del Bienestar con efecto electoral independiente de aprobación presidencial

**Nota:** no se busca el diseño ya construido (el pre-registro ya declara que "el diseño es concebible, solo no se ha hecho"). Se buscan los dos insumos que lo harían posible.

### (a) Padrón Único de Beneficiarios (PUB), Pensión del Bienestar

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí, con granularidad pública limitada. |
| **FUENTE** | Secretaría de Bienestar, Dirección General de Geoestadística y Padrones de Beneficiarios. `pub.bienestar.gob.mx` (submódulo "Padrones de personas físicas": `pub.bienestar.gob.mx/pub/personas`; consulta de Pensión del Bienestar en `pub.bienestar.gob.mx/pub/programasIntegrales`). Dataset en `datos.gob.mx/dataset/padron_unico_beneficiarios_bienestar`. |
| **GRANULARIDAD** | Nominal (incluye nombre), desagregado por periodo/entidad/municipio y monto. Sin evidencia de coordenadas/domicilio/localidad fina en la versión pública — la desagregación geográfica "puede variar entre nivel estatal y municipal según disponibilidad". |
| **COBERTURA TEMPORAL** | Registro continuo/actualizado por periodo; no confirmado si la fecha de alta individual (variable clave para un RDD de exposición al tratamiento) está expuesta públicamente. |
| **ACCESO** | Consulta pública en línea sin registro aparente para el agregado/nominal básico. Historial relevante: el INAI ha **ordenado** a Bienestar entregar desagregaciones adicionales (tipo de discapacidad, casos Sembrando Vida por municipio/hectáreas) ante negativas iniciales — el patrón sugiere que variables finas (geolocalización, fecha de alta exacta) requieren **solicitud de transparencia**, posiblemente con recurso ante INAI. |
| **FORMATO** | Portal de consulta web; no confirmada descarga masiva CSV/API desde `pub.bienestar.gob.mx` (el dataset en `datos.gob.mx` probablemente sí la ofrece). |
| **QUÉ LE FALTA** | Geolocalización fina (coordenadas o al menos sección electoral) y fecha de alta a nivel de beneficiario individual — no confirmadas como públicas por defecto; el historial de resoluciones INAI sugiere que son obtenibles por la vía de transparencia. |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE** en su forma de descarga directa; probablemente resoluble como **NO-ACCESIBLE → accesible por transparencia** (que sí cuenta como vía válida, no como descarte). |

### (b) Resultados electorales del INE a nivel de sección electoral

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí. |
| **FUENTE** | INE, **Sistema de Consulta de la Estadística de las Elecciones (SICEE)**: `sicee.ine.mx` (proceso 2023-2024), `siceen21.ine.mx` (2020-2024). Portal de datos abiertos: `ine.mx/transparencia/datos-abiertos`; resultados: `ine.mx/voto-y-elecciones/resultados-electorales`. Cómputos distritales por elección: `computos2024.ine.mx`, `computos2021.ine.mx/base-de-datos`. |
| **GRANULARIDAD** | **Sección electoral**, confirmado explícitamente — el SICEE cubre 70,504 secciones, con resultados de presidencia, senaduría, diputación federal y local, y presidencias municipales, por sección/municipio/distrito/entidad/circunscripción. |
| **COBERTURA TEMPORAL** | Más de tres décadas de datos, diseñado explícitamente para comparaciones históricas entre procesos electorales — condición necesaria para parear la misma sección entre dos elecciones. |
| **ACCESO** | Descarga directa, sin registro. |
| **FORMATO** | `.zip` con bases por tipo de elección (Cómputos Distritales); SICEE ofrece descargas para análisis académico/periodístico/ciudadano (formato exacto no confirmado por fetch, probablemente CSV). |
| **QUÉ LE FALTA** | Nada estructural evidente para este insumo. Riesgo técnico conocido y no verificado en este acto: la renumeración de secciones tras redistritación complica el pareo de la misma sección en ventanas largas; manejable en ventanas de elecciones consecutivas cercanas. |
| **CLASIFICACIÓN** | **EXISTE-SATISFACE.** |

**Síntesis Ficha 8:** el insumo (b) satisface completamente. El insumo (a) existe y es nominal, pero su forma pública por defecto no trae la geolocalización/fecha de alta finas que el RDD necesita — la vía de transparencia tiene precedente favorable (resoluciones INAI). **Esto mueve la ficha de "NO EXISTE el diseño" a "el diseño tiene un insumo completo (b) y un insumo a un paso de completarse por transparencia (a)"** — cambio sustantivo respecto a la clasificación previa, sin llegar a EXISTE-SATISFACE conjunto.

## Ficha 9 (R7.4/R7.5) · ≥25% de casos documentados de respuesta colectiva ante agravio que crucen la predicción ambiental

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí. |
| **FUENTE** | **ACLED (Armed Conflict Location & Event Data Project)**, cobertura sistemática y continua de México. `acleddata.com/conflict-data/download-data` (Data Export Tool + API); agregados/semanales vía Humanitarian Data Exchange: `data.humdata.org/dataset/mexico-acled-conflict-data`, `data.humdata.org/dataset/acled-data-for-mexico`; metodología México: `acleddata.com/methodology/mexico`. |
| **GRANULARIDAD** | Evento individual, georreferenciado (coordenadas, código de precisión espacial 1-3), con tipo de actor, tipo de evento ("Protests", "Riots", "Violence against civilians", "Battles"), fecha, actores, fatalidades y nota descriptiva. **Codifica explícitamente autodefensas/policías comunitarias** bajo "Identity Militias" (código de interacción 4) — distingue el fenómeno de autodefensa rural de la protesta urbana genérica. |
| **COBERTURA TEMPORAL** | Registro continuo, actualizado semanalmente, cobertura mexicana activa por más de una década. |
| **ACCESO** | Registro gratuito requerido para exportación completa (cuenta como accesible); agregados semanales sin registro vía HDX. |
| **FORMATO** | CSV/API; HDX en CSV/XLSX. |
| **QUÉ LE FALTA** | No hay variable binaria "urbano/rural" pre-codificada — debe derivarse de admin1/admin2/tipo de localidad. La pregunta específica de la ficha (¿≥25% de casos donde el entorno no predice la forma?) **no es verificable sin descargar y procesar el dataset** — está fuera del alcance de un barrido de existencia y requiere análisis posterior. Nota: "Semáforo del Silencio" (buscado como posible fuente de Data Cívica) no se encontró — el proyecto real más cercano de Data Cívica es *Votar entre Balas* (`votar-entre-balas.datacivica.org`, con México Evalúa/Animal Político), que cubre violencia político-criminal, no protesta/autodefensa en general. UCDP (Uppsala) también cubre México vía HDX como fuente complementaria/alternativa. CIDE tiene bases más acotadas por tema (conflictos por agua 1990-2002, "guerra contra las drogas" 2006-2011). Observatorio Nacional Ciudadano cubre delitos del fuero común, no protesta/autodefensa específicamente. |
| **CLASIFICACIÓN** | **EXISTE-SATISFACE** en existencia, accesibilidad y granularidad (evento georreferenciado con tipificación que distingue autodefensa de protesta). La variable urbano/rural requiere derivarse y el umbral del 25% requiere análisis del dato ya descargado — trabajo de análisis, no de búsqueda de fuente. |

## Ficha 10 (R8.1) · Contribución ≥60% sostenida ≥2 años sin sanción/monitoreo, fuera de usos y costumbres

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial. |
| **FUENTE** | Secretaría de la Función Pública / datos.gob.mx: *Promoción de Contraloría Social* (`datos.gob.mx/dataset/promocion_contraloria_social`), *Programas y Proyectos de Contraloría Social* (`datos.gob.mx/busca/dataset/programas-y-proyectos-de-contraloria-social`, concentrado 2014-2018). Sistema operativo fuente: **SICS — Sistema Informático de Contraloría Social** (`sics.funcionpublica.gob.mx`, `consultasics.buengobierno.gob.mx`), donde cada comité llena una **Cédula de Vigilancia**. |
| **GRANULARIDAD** | El dataset abierto parece agregado por programa/estado/año (no confirmado = comité individual). El SICS sí captura a nivel de **comité individual** (Cédula de Vigilancia por comité, con CURP), pero es sistema operativo de captura, no un microdato abierto descargable en bloque. |
| **COBERTURA TEMPORAL** | Dataset abierto: desde 2019 (o 2014-2018 en el concentrado). SICS: registro continuo desde ~2013. |
| **ACCESO** | Dataset agregado: descarga directa. SICS a nivel comité: requiere credenciales institucionales (CURP + rol de Instancia Ejecutora/Normativa) — no es portal de datos abiertos; el acceso a microdatos de comités individuales probablemente requiere **solicitud de transparencia**. |
| **FORMATO** | CKAN (CSV/XLSX probable, no confirmado). SICS: sistema web transaccional. |
| **QUÉ LE FALTA** | (1) unidad = comité individual con identificador único en el dato **abierto** (existe en SICS pero no público en bloque); (2) variable explícita de "mecanismo de sanción/monitoreo interno" por comité — la Cédula de Vigilancia registra evaluación de beneficiarios sobre el programa, no necesariamente si el comité mismo tiene mecanismo sancionador; (3) panel de participación ≥2 años a nivel de comité individual, accesible sin solicitud de transparencia. **Hallazgo normativo clave, coincide con el análisis interno previo del programa** (`2026-08-05-p3-r8-1-contradiccion-inventario.md`): "Contraloría Social" está definida por ley (Ley General de Desarrollo Social / Lineamientos SFP) como conjunto de acciones de **vigilancia** sobre el ejercicio de recursos públicos — es decir, **sí** es, por definición, un mecanismo de vigilancia (no un comité vecinal neutral con posible free-riding puro), lo cual confirma que "comité de contraloría social" mide el fenómeno correcto pero es una categoría más estrecha que "comité de obra" en sentido genérico (un comité que administra un tanque de agua comunitario sin vigilar gasto público formal no cae aquí). |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE.** El marco normativo y el sistema (SICS) existen y capturan a nivel de comité, pero el dato abierto público está agregado y no trae variable de sanción/monitoreo ni panel accesible sin solicitud de transparencia. Coincide con y extiende el hallazgo interno previo (clasificación "gap de tercer tipo", `P3`): aquí se confirma que el candidato (SICS) sí existe operativamente, con nombre y URLs concretas, más allá de la sección "sospechada" del inventario donde vivía antes. |

## Ficha 11 (R8.2) · Participación sostenida ≥2 ciclos, incumplimiento <10%, tandas digitales entre desconocidos

| Campo | Detalle |
|---|---|
| **EXISTE** | No encontrado para el cruce específico. |
| **FUENTE** | **ENIF 2024** (INEGI/CNBV) mide tandas en general: 20% de la población participa (subió de 18% en 2021), 36.6% ahorra informalmente — es la fuente pública más sólida sobre tandas, pero mide tandas tradicionales en general, no digitales ni específicamente entre desconocidos, sin ciclos completados ni tasa de incumplimiento. Apps mexicanas de tandas digitalizadas: **Tanda+/Tanda Más** (`tandamas.mx`) y **MINES** (`mines.lat`). Tanda+ menciona un "score de confianza" interno basado en historial de tandas completadas, pagos a tiempo y cero cancelaciones — la app **genera** internamente el dato pedido, pero no se encontró que lo haya publicado como cifra agregada en reporte, ronda de inversión o nota de prensa. Sin evidencia de rondas de inversión o casos de estudio de aceleradoras (Endeavor México, 500 Startups LatAm) con estas cifras. |
| **GRANULARIDAD** | ENIF: individuo/hogar, nacional — no captura lo digital ni "entre desconocidos". |
| **COBERTURA TEMPORAL** | ENIF: trienal (2018, 2021, 2024). |
| **ACCESO** | ENIF: descarga directa y gratuita. El dato específico de apps de tandas: no publicado en ningún formato. |
| **FORMATO** | N/A para el dato específico. |
| **QUÉ LE FALTA** | Todo el cruce: (a) digital vs. tradicional, (b) entre desconocidos vs. familia/amigos (la norma reportada), (c) retención ≥2 ciclos, (d) tasa de incumplimiento — para ninguna app mexicana está publicado. |
| **CLASIFICACIÓN** | **NO-ENCONTRADO.** Búsquedas en descripciones de Google Play/App Store, prensa fintech mexicana, CGAP, BID, sitios de Tanda+/MINES, Endeavor México, 500 Startups LatAm, European Microfinance Platform. **No es límite de clase**: el dato existe y se genera dentro de cada app (ellas mismas calculan el "score de confianza"); es falta de divulgación voluntaria de startups pequeñas y privadas, sin obligación de reporte ni cobertura de prensa financiera especializada profunda — distinto en naturaleza de un límite estructural. |

## Ficha 12 (R8.3) · Diferencia <10pp disposición a transar con desconocidos, enforcement alto vs. bajo

| Campo | Detalle |
|---|---|
| **EXISTE** | Sí, con matiz semántico. |
| **FUENTE** | **LAPOP AmericasBarometer México** (`vanderbilt.edu/lapop/about-americasbarometer.php`; acceso: `vanderbilt.edu/lapop/free-access.php`, `request-datasets.php`). Preguntas confirmadas en el mismo cuestionario/mismo respondente: **IT1** (confianza interpersonal: "¿la gente de su comunidad es muy/algo/poco/nada confiable?", escala 1-4), **AOJ12** (percepción de que el sistema judicial castigaría al culpable de un robo/asalto), **B18** (confianza en la policía nacional, escala 1-7), **AOJ11** (percepción de inseguridad en el barrio, complementaria). **Latinobarómetro** (`latinobarometro.org/documentacion-datos`) tiene el equivalente clásico (código varía por año: p14st/P29STGBS/p12) más confianza en policía en el mismo respondente — cruce análogo. |
| **GRANULARIDAD** | Individuo (microdato de encuesta). |
| **COBERTURA TEMPORAL** | LAPOP México: bianual desde 2004 (2004-2023...). Latinobarómetro: anual desde 1995, +25 rondas. |
| **ACCESO** | LAPOP: microdato SPSS/Stata, **acceso sin restricción tras registro gratuito** ("free user", licencia de clic) — cuenta como accesible. Latinobarómetro: descarga directa de microdatos (R/SAS/SPSS/Stata) para todos los años excepto embargo temporal en los más recientes. |
| **FORMATO** | `.sav`, `.dta`; Latinobarómetro también `.RData`, `.sas7bdat`. |
| **QUÉ LE FALTA** | Nada estructural — el cruce es técnicamente posible hoy descargando el microdato. Matiz: IT1 mide confianza generalizada en "la gente de su comunidad", no una pregunta conductual específica de "disposición a transar económicamente con un desconocido" (tipo juego de confianza económico) — es la aproximación estándar de la literatura de capital social, razonable pero no idéntica semánticamente. No se encontró evidencia de un módulo país-específico de LAPOP México con pregunta de confianza económica más conductual. |
| **CLASIFICACIÓN** | **EXISTE-SATISFACE**, con la salvedad semántica anotada. Es la respuesta más limpia de las 17: permite el cruce microdato-a-microdato sin reconciliar cifras agregadas de fuentes distintas, que era exactamente el problema declarado en el pre-registro interno (`conf.06`: cinco/seis cifras de confianza en conflicto). **Importante:** el análisis interno previo (`ADR-64`, sello de `conf.06`) reconcilió las cifras de ENCUCI pero dejó la condición A de R8.3 bloqueada por circularidad (el dato candidato de ENCUCI, `radio_confianza`, comparte reactivo con la regla que se prueba). LAPOP/Latinobarómetro son fuentes **independientes** de esa circularidad — no comparten instrumento con la regla `cooperacion.confianza.puente_personal` del modelo — y por tanto no heredan la marca C3. Esto no adjudica el veredicto `R8.3`, pero identifica una vía de salida al bloqueo que no dependía de reconciliar `conf.06`. |

## Ficha 13 (R9.1, primera fila) · Tasa de consulta a experto <50%, población con acceso documentado (<2km, sin costo, espera <1 día)

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial, con hallazgo negativo relevante. |
| **FUENTE** | Catálogo **CLUES** (DGIS, ver Ficha 6) para georreferenciación de establecimientos; **ENSANUT** (INSP, `ensanut.insp.mx`) para conducta de consulta; diccionario de datos ENSANUT 2018 en el Repositorio Nacional de Metadatos de INEGI: `inegi.org.mx/rnm/index.php/catalog/590/data-dictionary/F42`. |
| **GRANULARIDAD** | (a) ¿CLUES trae coordenadas GPS? Evidencia mixta — el manual documentado describe domicilio como texto (entidad/municipio/localidad/calle), sin campo nativo lat/long confirmado en el CSV oficial; existe al menos un recurso derivado en formato **KMZ** (`datos.gob.mx/busca/dataset/catalogo-de-clave-unica-de-establecimientos-de-salud-clues/resource/6fe85fea-4845-4bff-a273-dfa74a21f076`), que implica geolocalización en algún subconjunto, no confirmado como sistemático para todo el universo. (b) **Hallazgo relativamente firme: el microdato PÚBLICO de ENSANUT no trae llave de establecimiento ni domicilio preciso** — usa las claves geoestadísticas estándar de INEGI (CVE_ENT, CVE_MUN), es decir, llega hasta **municipio**, práctica habitual de anonimización de encuestas de hogar. |
| **COBERTURA TEMPORAL** | ENSANUT: cortes transversales repetidos (2018, 2020, 2021-2024 Continua). CLUES: registro continuo. |
| **ACCESO** | ENSANUT: descarga directa/registro simple en `ensanut.insp.mx`. CLUES: descarga directa. |
| **FORMATO** | ENSANUT: SPSS/CSV + diccionarios PDF. CLUES: CSV/KMZ/PDF. |
| **QUÉ LE FALTA** | La llave que vincule a la persona entrevistada con el establecimiento consultado, o al menos una localidad con precisión suficiente para calcular distancia real <2km, **no está en el microdato público** de ENSANUT — el máximo nivel liberado es municipio. Línea de seguimiento no confirmada en este barrido: si el INSP tiene un mecanismo de acceso restringido a microdatos geolocalizados más precisos para investigadores autorizados ("laboratorio de datos" confidencial). |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE.** Ambas piezas existen por separado; el enlace persona↔establecimiento con precisión <2km no es posible con los microdatos públicos tal como están. Coincide con y confirma con mayor precisión el hallazgo interno previo (`cruce-catalogo-fichas-v2_0.md:99`, "NO ENLAZA") — aquí se agrega la confirmación específica de que ENSANUT público topa en municipio. |

## Ficha 14 (R9.1, segunda fila) · Población que no consultó a nadie, excluida del Cuestionario de Utilizadores

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial — el instrumento existe y es descargable; el texto exacto de la categoría pedida no se pudo confirmar en esta sesión. |
| **FUENTE** | INSP/INEGI, **Cuestionario de Utilizadores de Servicios de Salud, ENSANUT 2018**, Sección IV "Accesibilidad y Calidad": `inegi.org.mx/contenidos/programas/ensanut/2018/doc/ensanut_2018_utilizadores_servicios_salud.pdf` (existencia y estructura confirmadas por múltiples resultados de búsqueda que citan su contenido). Ediciones posteriores con módulo similar: ENSANUT Continua 2021-2024. |
| **GRANULARIDAD** | Individuo. |
| **COBERTURA TEMPORAL** | Corte transversal por ronda (2018; luego ENSANUT Continua anual). |
| **ACCESO** | Descarga directa del cuestionario (PDF) y de microdatos (`ensanut.insp.mx`/INEGI), sin registro obligatorio. |
| **FORMATO** | PDF (cuestionario), SPSS/CSV (microdato). |
| **QUÉ LE FALTA** | Un artículo que analiza ENSANUT Continua 2023 (`ensanut.insp.mx/encuestas/ensanutcontinua2023/doctos/analiticos/16199-Texto%20del%20art%C3%ADculo-82516-2-10-20240821.pdf`) reporta razones de no atención: "no lo consideró necesario" (~55%), "caro/no tenía dinero" (~13-16%), "no tenía tiempo" (~8%), "cita en otro lugar" (~3.5%) — **no suman 100%**, lo que sugiere fuertemente categorías adicionales no capturadas en los resúmenes consultados, muy probablemente incluida automedicación o consejo de un conocido. **No se pudo verificar el texto exacto de esa opción de respuesta** porque `WebFetch` falló en todos los intentos (5 variantes de búsqueda distintas probadas, incluidos términos literales "se automedicó", "prefirió consejo de", "recomendación de alguien", "remedio casero" — sin resultado concluyente). |
| **CLASIFICACIÓN** | **NO-ENCONTRADO de forma concluyente para el texto exacto**, aunque el instrumento SÍ EXISTE y ES DESCARGABLE. Términos de búsqueda usados, documentados para que el siguiente acto no los repita: `ENSANUT 2018 utilizadores servicios salud "no buscó" OR "no consultó" razones opciones respuesta cuestionario`; `ENSANUT "razones para no buscar atención" "no fue necesario" "no tenía dinero" "no tenía tiempo"`; `ENSANUT automedicación "recomendación de" familiar OR conocido OR farmacéutico`; `ENSANUT "se automedicó" OR "prefirió automedicarse" OR "consejo de"`; `ENSANUT barrera personal "prefirió" remedio casero OR automedicarse OR "recomendación de alguien"`. **Acción recomendada, de bajo costo:** abrir directamente el PDF del cuestionario (URL arriba) en un acto con `WebFetch` funcional — es casi seguro el paso que cierra esta ficha en un sentido u otro. |

## Ficha 15 (R10.1) · Diferencia <15pp rechazo indirecto, interlocutor superior vs. inferior, muestra no universitaria

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial — existe la materia prima (corpus con hablantes no universitarios), no el análisis específico. |
| **FUENTE** | **PRESEEA** (Proyecto para el Estudio Sociolingüístico del Español de España y América), equipo México/PRESEEA-Puebla, El Colegio de México — corpus estratificado por cuotas de instrucción educativa baja/media/superior (108 entrevistas en Puebla). Repositorio del proyecto: `preseea.linguas.net/corpus.aspx`; volúmenes publicados vía `libros.colmex.mx` (*Corpus sociolingüístico de la ciudad de Puebla, PRESEEA-Puebla. Hablantes de instrucción media/baja*). Estudio de atenuación con hablantes de instrucción baja en PRESEEA-Puebla: `revistas-filologicas.unam.mx/anuario-letras`. |
| **GRANULARIDAD** | Individuo (transcripciones de entrevistas sociolingüísticas). |
| **COBERTURA TEMPORAL** | Recolección ~2014-2018, volúmenes publicados 2018-2023. |
| **ACCESO** | Mixto: el corpus PRESEEA en general es de acceso gratuito para investigación vía contacto con el equipo coordinador; los volúmenes editados de PRESEEA-Puebla están comercializados como libros en la tienda de Colmex (pago, no descarga directa gratuita). |
| **FORMATO** | Transcripciones textuales. |
| **QUÉ LE FALTA** | El corpus consiste en entrevistas sociolingüísticas biográficas semiestructuradas, **no** en tareas elicitadas de actos de rechazo tipo role-play (metodología Félix-Brasdefer, el ancla actual de la ficha). Los rechazos existirían de forma incidental en el habla natural, no codificados sistemáticamente por estatus del interlocutor. No se encontró ningún estudio ya publicado que haya extraído y codificado actos de rechazo por estatus superior/inferior en población mexicana no universitaria — ni en Redalyc, Scielo México, ni en revistas específicas (Signos, Lingüística Mexicana, ELA-UNAM). |
| **CLASIFICACIÓN** | **NO-ENCONTRADO** como estudio que satisfaga la condición directamente. La materia prima (corpus con hablantes no universitarios) EXISTE, con componente **NO-ACCESIBLE** (pago) para los volúmenes editados específicos. Cerrar esta ficha exigiría investigación primaria de re-análisis del corpus (codificar actos de rechazo por estatus del interlocutor en transcripciones ya existentes), no meramente acceso a un dato ya tabulado — es un proyecto de análisis, no una descarga. |

## Ficha 16 (R10.2) · Diferencia <10% rotación/desempeño, retro pública vs. privada, controlando sector

| Campo | Detalle |
|---|---|
| **EXISTE** | No, a nivel de fuente pública mexicana representativa. |
| **FUENTE** | Mismas fuentes revisadas que Ficha 4 (ECCO, Enterprise Surveys, GPTW) — ninguna desagrega retroalimentación pública vs. privada. Cifras tipo "14% más productividad" / "15% menos rotación" citadas en blogs mexicanos de RRHH provienen de estudios de Gallup/Harvard de contexto global/estadounidense, republicados sin metodología mexicana propia ni comparación público/privado. |
| **GRANULARIDAD** | N/A — no localizada. |
| **COBERTURA TEMPORAL** | N/A. |
| **ACCESO** | N/A. |
| **FORMATO** | N/A. |
| **QUÉ LE FALTA** | Todo: no hay fuente mexicana que mida diferencial de rotación/desempeño (<10%) entre retroalimentación en público vs. privado, controlando sector. |
| **CLASIFICACIÓN** | **NO-ENCONTRADO.** Búsquedas en STPS, ECCO, Enterprise Surveys, GPTW, Redalyc/Scielo (psicología organizacional mexicana sobre feedback). **Límite de clase declarado explícitamente**: si la retroalimentación se da en público o en privado es una práctica gerencial cotidiana interna que ninguna encuesta pública agregada registra por diseño — solo la propia empresa observa cómo y dónde retroalimenta a cada empleado. |

## Ficha 17 (R10.3) · Aumento <15pp disposición a testificar tras protección a testigos

| Campo | Detalle |
|---|---|
| **EXISTE** | Parcial — proxies agregados sí existen y son públicos; el dato individualizado en zona insegura, no, y no debe existir. |
| **FUENTE A** | INEGI, **ENVIPE**, serie anual 2011-2025 (`inegi.org.mx/programas/envipe/2025`). Granularidad: entidad federativa/nacional; microdatos individuales anonimizados disponibles, sin marcador de "persona bajo protección de testigos". Cobertura: 2011-2025 anual. Acceso: descarga directa gratuita (microdatos + boletines). Formato: CSV/DBF/SPSS, PDF. Dato relevante: cifra negra ~92-93% (2019-2024), "desconfianza en la autoridad" como razón de no denuncia estable en ~12.7-14% (2023-2024) — proxy agregado válido de disposición a denunciar por confianza en autoridad, por entidad. |
| **FUENTE B** | Secretaría de Gobernación, **Mecanismo de Protección para Personas Defensoras de Derechos Humanos y Periodistas**, Informes Estadísticos Mensuales: `gob.mx/defensorasyperiodistas/documentos/informes-estadisticos-mensuales` (desde ~2019 hasta mayo 2026 localizado). Granularidad: entidad/nacional, estrictamente agregado (conteos de beneficiarios por tipo y entidad, sin identificar personas). Acceso: descarga directa gratuita, PDF. Qué le falta: reporta número de beneficiarios y medidas, pero no cruza con tasas de denuncia/testimonio de la población en esas zonas — ese enlace causal no está publicado. |
| **FUENTE C** | CEAV — registros agregados (REFEVI) de víctimas inscritas, sin desglose de testigos protegidos vs. disposición a testificar. |
| **GRANULARIDAD** | Entidad/nacional (los tres). |
| **COBERTURA TEMPORAL** | ENVIPE: anual 2011-2025. Mecanismo: mensual desde ~2019. |
| **ACCESO** | Descarga directa gratuita, los tres. |
| **FORMATO** | CSV/DBF/SPSS/PDF. |
| **QUÉ LE FALTA** | Un vínculo publicado, agregado, entre "efectividad de la protección a testigos" y "aumento en disposición a testificar/denunciar" en zonas de alta inseguridad. Podría construirse combinando ENVIPE (entidad-año) con los informes del Mecanismo (entidad-año), pero nadie lo ha publicado ya hecho. |
| **CLASIFICACIÓN** | **EXISTE-NO-SATISFACE** completamente (los proxies agregados existen, no dan la relación causal específica ya construida). **Declaración ética explícita, confirmando la clasificación previa del programa, no refutándola:** ninguna fuente pública mexicana ofrece —ni debería ofrecer— datos individualizados de personas bajo protección de testigos en zona de inseguridad activa correlacionados con su disposición a testificar. Tanto el Mecanismo como CEAV publican deliberadamente solo conteos agregados/anonimizados porque identificar a personas protegidas junto con su conducta de denuncia en zona de violencia activa las expondría a represalia. El bloqueo ético declarado por el programa original es correcto y se sostiene: el dato secundario agregado ya publicado (ENVIPE + Mecanismo) es lo único válido — esto **es** el límite ético, no un límite de búsqueda. |

---

## Resumen ejecutivo

### Reparto

| Clasificación | Fichas | Cuenta |
|---|---|---|
| **EXISTE-SATISFACE** | 9 (R7.4/R7.5, ACLED), 12 (R8.3, LAPOP) | 2 |
| **EXISTE-NO-SATISFACE** | 1 (R1.1), 4 (R2.1), 6 (R4.1 panel), 7 (R4.1 trato), 8 (R7.3), 10 (R8.1), 13 (R9.1 distancia), 17 (R10.3) | 8 |
| **NO-ENCONTRADO** | 2 (R1.3), 5 (R2.2), 11 (R8.2), 14 (R9.1 cuestionario), 15 (R10.1), 16 (R10.2) | 6 |
| **NO-ACCESIBLE** | 3 (R1.4) | 1 |

**17 de 17.** Cero fichas se sostienen como "no existe fuente" sin matiz — cada una de las 17 tiene, como mínimo, una candidata con nombre y URL, aunque en 6 casos (NO-ENCONTRADO) esa candidata no apareció y hay que decirlo con las fichas de dónde se buscó, y en varios de los EXISTE-NO-SATISFACE la brecha específica es precisa, no genérica.

**Límite de clase declarado explícitamente** (ninguna encuesta o registro puede darlo por naturaleza, con independencia de cuánto se busque): Ficha 2 (canal de alta fintech, parcial — la vía regulatoria sí es límite de clase, la vía de encuesta a consumidores no), Ficha 4 (reporte de errores por jerarquía), Ficha 5 (rotación/liderazgo), Ficha 16 (retro pública/privada). **Límite ético, no de búsqueda:** Ficha 17 (testificar tras protección a testigos) — confirmado, no refutado.

### Las tres que más rendimiento darían si se persiguieran

1. **Ficha 12 (R8.3, LAPOP/Latinobarómetro).** Ya está en EXISTE-SATISFACE, con acceso vía registro gratuito. Descargar el microdato y correr el cruce IT1×AOJ12/B18 cerraría una ficha que llevaba bloqueada desde `conf.06` — y la cierra por una vía que **no depende de reconciliar las cinco/seis cifras de confianza en conflicto** que bloqueaban la ruta interna (ENCUCI). Es la ganancia de menor esfuerzo y mayor certeza de las 17.

2. **Ficha 9 (R7.4/R7.5, ACLED).** También en EXISTE-SATISFACE, con acceso vía registro gratuito, y cierra **dos** reglas del modelo a la vez (comparten falsador). Lo único que falta es procesamiento (derivar urbano/rural, calcular el 25%) — no hay obstáculo de acceso ni de existencia.

3. **Ficha 8 (R7.3, RDD Pensión del Bienestar).** Era la ficha con el diseño declarado "no existe en absoluto" (`D` no aplicaba: "el diseño es concebible, solo no se ha hecho"). Este barrido encuentra el insumo (b) completamente resuelto (INE por sección electoral, descarga directa) y el insumo (a) a un paso de resolverse por la vía de transparencia, con precedente favorable de INAI. Es la ficha de mayor valor estratégico del lote — no por ser la más fácil, sino porque el programa la describía como la más lejana, y resulta ser la que menos lejos está.

**Mención aparte, porque fue el disparador de todo el acto:** Ficha 1 (R1.1, AGROASEMEX) confirma que el padrón por productor sí existe y es descargable — la premisa del encargo (que se había declarado inexistente algo que sí se publica) se sostiene. No llega a EXISTE-SATISFACE porque falta confirmar la desagregación por ciclo agrícola y la distinción voluntario/obligatorio, y porque el veredicto interno `D` de `hitoD-R1.1-veredicto-v1_0.md` ya resolvió el dominio por una razón estructural distinta (exclusión de mercado del productor de temporal) que este barrido no reabre ni contradice.

---

## Lo que este documento no hace

No adjudica ningún veredicto `RX.Y`. No edita `hitoD-preregistro-v2_0.md` ni `cruce-catalogo-fichas-v2_0.md` (ambos append-only). No descarga ningún microdato ni abre ningún instrumento — todas las URLs de arriba están pendientes de verificación directa por `WebFetch` o descarga manual, bloqueado en esta sesión por política de red del entorno (confirmado contra dominio de control neutral, no es un bloqueo específico de sitios mexicanos). No afirma que la búsqueda de ninguna ficha `NO-ENCONTRADO` sea exhaustiva más allá de los términos y portales listados en cada fila — es la garantía mínima que exige no repetir el error que motivó este acto.
