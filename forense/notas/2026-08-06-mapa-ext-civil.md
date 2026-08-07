# MAPA-EXT-CIVIL · sociedad civil, observatorios y fuentes restringidas

Fecha de corte de la búsqueda: 2026-08-06. Este acto documenta puertas; no crea cuentas, no acepta licencias, no descarga microdatos, no mide y no modifica manifiesto ni sellos.

## Resultado que cambia decisiones

Se localizaron diez candidatas prioritarias. Cuatro abren rutas civiles que no estaban resueltas por los antecedentes: LAOMS para protesta con actor y respuesta; Votar entre Balas para violencia político-criminal municipal descargable; OMCA para conflictos con actores y acciones; y plataformas operativas de tandas para incumplimiento/reputación. Cero Desabasto avanzó de “portal conocido” a descarga configurable documentalmente confirmada, pero conserva el estado `INDEXADO-NO-DESCARGADO`: sin abrir la aplicación no se puede afirmar granularidad de unidad, campaña ni denominador.

Las dos coincidencias más directas con huecos del modelo son propietarias: Kantar Worldpanel México declara un panel continuo de 8,500 hogares, 82% de población urbana, seis regiones y siete ciudades; NIQ Homescan declara panel longitudinal a nivel UPC y enlace con encuestas, aunque la página global no confirma por sí sola la muestra mexicana. No se solicitó cotización.

## Método y universo

Se leyó `AGENTS.md`, la matriz universal, el catálogo vigente v2.0 (el v1.0 pedido ya no existe y fue reemplazado), `exploracion-puertas`, y los encargos/notas BARRIDO-1, VERIF-3 y ABRIR-4. El filtro fue: conservar solo una puerta con unidad/campos/acceso suficientes para producir una medición o cambiar la decisión de perseguirla. Se usaron páginas primarias de organizaciones y proveedores; una nota metodológica de UNAM documenta la estructura de LAOMS. No se tomó una cifra periodística aislada como dataset.

Universos de búsqueda negativa delimitados:

- Corrupción/mordida subnacional: MCCI, Transparencia Mexicana, observatorios anticorrupción y resultados visibles. MCCI es duplicada de fuente conocida; no se encontró una fuente civil nueva con conducta de mordida municipal. ENCIG sigue siendo la puerta estatal conocida, fuera del perímetro civil de esta salida.
- Denuncia con seguro: plataformas de denuncia, observatorios de seguridad, AMIS/aseguradoras y búsquedas de coobservación. No se encontró una fuente que observe en la misma unidad seguro vigente y acto de denunciar; Denuncia Digital requiere autenticación y tampoco documenta seguro.
- Tandas/ROSCA: plataformas y estudios México. Se localizaron Tanda+ y Tanda Ahorro MX con calendario, pagos y reputación, pero ninguna publica dataset o tasa de incumplimiento. El SAT declaró que no lleva programa de seguimiento de tandas, cerrando esa puerta administrativa específica.
- Protesta/violencia/actores: LAOMS, Data Cívica, OMCA, OCSA, ODIM y ACLED. LAOMS es la mejor coincidencia conceptual; la base no quedó descargable. ACLED detallado sigue restringido y el payload gratuito mensual ya está mapeado como insuficiente.
- Consumo/marca: Kantar, NIQ e Ipsos. Kantar y NIQ tienen compra observada longitudinal; Ipsos visible es encuesta/informe agregado y no se conservó entre prioridades.
- Clima/desempeño: Mercer, Aon y GPTW. Se confirmó infraestructura propietaria de clima/engagement; no se confirmó todavía un benchmark que enlace estilo de liderazgo con rotación o productividad auditada.
- Cuidado/redes: Observatorio de Cuidados y fuentes civiles visibles. El observatorio agrega oferta territorial, pero no reemplaza ENASIC/ENBIARE para redes familiares individuales.

## Evidencia documental clave

- Cero Desabasto: el portal declara más de 14 mil reportes y una sección de datos abiertos; su comunicado de lanzamiento especifica tablero en tiempo real y descarga según variables. La captación es ciudadana y no probabilística. No debe usarse como tasa sin denominador.
- LAOMS: su metodología define una fila por evento y diez campos: fecha, lugar, actor, campo, demanda, repertorio, demandado, origen del agravio, alcance y respuesta. Es exactamente la estructura ausente del archivo ACLED mensual ya abierto.
- Votar entre Balas: la portada ofrece base descargable y consulta por estado/municipio de víctimas de violencia político-criminal. Falta abrir diccionario antes de afirmar años o exhaustividad.
- OMCA: declara rastreo hemerográfico desde 2010, más de 5,000 registros y ubicación/evolución con actores y acciones.
- Tanda+: registra pagos, rondas y reputación por incumplimiento repetido; Tanda Ahorro documenta monto, frecuencia, rondas, fecha límite y reputación. Son registros operativos potenciales, no datos publicados.
- Kantar: la página México documenta 8,500 hogares y cobertura; sus productos distinguen marca, gasto, frecuencia, canal y marca propia. Esto permite especificar una tabulación mínima para prima de marca, sin comprar todavía.
- NIQ: Homescan documenta panel estático longitudinal, UPC, seguimiento de compradores y encuestas/segmentación; la cobertura México requiere confirmación comercial.
- El estudio Kellogg 2026 usa cuenta×mes de una fintech mexicana, transacciones de app, solicitantes sin historial y default/rentabilidad. Es evidencia de que el dato existe, pero sigue propietario y la fintech no está identificada públicamente en la ficha.

## Puertas rotas, restringidas y duplicados

Puertas rotas o incompletas:

- `cerodesabasto.org/open-data` carga como aplicación JavaScript sin esquema visible en el HTML indexado; la descarga existe documentalmente, pero no se obtuvo el enlace de exportación.
- LAOMS expone metodología, publicaciones e infografías; no se localizó descarga actual de la base ni codebook.
- OCSA anuncia plataforma y campos conceptuales, pero la URL de prensa no entrega por sí sola el sistema ni descarga.
- Tanda Ahorro muestra contadores públicos en cero; puede ser producto incipiente. Validar tracción antes de cualquier solicitud.

Restringidas: Kantar Worldpanel, NIQ Homescan/Discover, Mercer, GPTW, Aon, ACLED detallado, registros internos de Tanda+/Tanda Ahorro y datos de la fintech del estudio Kellogg. “Restringida” significa que existe y documenta variables plausibles; no implica autorización ni recomendación de compra.

Duplicados: Encuesta MCCI ya estaba en BARRIDO-1/catalogada; ACLED ya fue abierto por VERIF-3 en su versión gratuita agregada; Denuncia Digital no aporta la condicional con seguro; Observatorio de Cuidados deriva principalmente de fuentes oficiales ya conocidas y solo añade una capa territorial.

## Cinco oportunidades principales y acción mínima

1. **Cero Desabasto / R9.2.** Abrir humanamente el exportador y conservar solo esquema o tabla agregada. Decisión: si hay campaña×entidad×periodo y denominador defendible, diseñar ruta ecológica; si no, mantener no satisfacción.
2. **LAOMS / R7.4-R7.5.** Localizar el XLSX/codebook institucional o pedir ficha técnica. Decisión: sustituir ACLED restringido con evento+actor+respuesta mexicano, o cerrar por acceso/cobertura.
3. **Tanda+ / R8.2.** Mesa decide si pedir una ficha agregada anonimizada con número de tandas, pagos esperados/realizados, mora y relación del grupo. No pedir microdato. Decisión: si existe n útil, preespecificar medición; si no, cerrar ruta propietaria.
4. **Kantar Worldpanel / R1.4.** Solicitar solo factibilidad/cotización de una tabulación mínima D/E: marca frente a sustituto, precio por unidad, recompra y panel. Decisión: comprar/no comprar con costo conocido; comparar una vez con NIQ.
5. **Votar entre Balas / violencia electoral.** Abrir metodología y encabezados de la descarga pública en un acto autorizado. Decisión: construir municipio×elección o descartar si la codificación no identifica actor/fecha suficientemente.

## Reservas materiales y parada

Ninguna candidata se eleva a `SATISFACE-UMBRAL-DOCUMENTAL`: no se abrieron exportaciones ni diccionarios y varias rutas son propietarias. Cero Desabasto no tiene denominador poblacional; LAOMS/OMCA dependen de cobertura hemerográfica; plataformas de tandas tienen selección de usuario y conflicto de interés del proveedor; paneles comerciales necesitan licencia y confirmar estrato/geografía; fuentes de clima no demuestran todavía desempeño auditado. El barrido se detiene porque ya produjo cinco acciones decisionales de mayor rendimiento y profundizar exigiría registro, contacto, licencia o descarga, todos fuera del encargo.
