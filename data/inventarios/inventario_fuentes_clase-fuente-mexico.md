# Inventario de fuentes de datos — Clase de fuente (México)

**Dominio:** no es un dominio temático — es la dimensión de **clase de fuente** que faltaba en
los 10 inventarios originales (todos construidos sobre encuestas). Registro administrativo,
padrón de programa, transparencia/sociedad civil, regulador o sectorial no-INEGI, encuesta
institucional no de hogares, e internacional con dato de México. Compilado por Encargo AA,
mesa #19, 4/ago/2026, contra el punto ciego estructural documentado en
`forense/notas/2026-08-04-aa-taxonomia-clase-fuente.md`.

**Naturaleza del documento:** catálogo. No contiene resultados, nombres de variables, reactivos
de cuestionario, juicios de calidad ni recomendaciones de uso — misma disciplina que
`README-inventarios.md` fija para los 10 inventarios originales.

**Convención de marcado:**
- `[verificado]` = confirmado por consulta web en esta sesión (WebSearch/WebFetch + sondeo de host).
- `[no verificado]` = la fuente existe, pero el dato específico no se confirmó aquí.
- `[ambiguo]` = no se pudo confirmar ni descartar con la búsqueda hecha en esta sesión — se
  registra así explícitamente, no se rellena a favor de ninguna lectura.

**Tres campos nuevos, presentes en cada entrada, que este defecto justifica (Tarea A del
encargo):** `Granularidad`, `Enlazable con encuesta`, `Independiente del prestador`.

**Nota de honestidad metodológica:** varias entradas de este inventario ya existen en el
catálogo v1.0 bajo un dominio temático (SAEH, Global Findex, LAPOP, Latinobarómetro) — se
listan aquí también, marcadas explícitamente `[ya en catálogo v1.0]`, únicamente para que la
dimensión de clase quede etiquetada sobre ellas; no cuentan como fuente nueva y `dedup.py` las
fusiona por acrónimo, no infla el conteo de fuentes únicas.

Orden: por clase, luego alfabético dentro de cada clase.

---

## 1. Clave Única de Establecimientos de Salud (CLUES)

- **Nombre / siglas:** Clave Única de Establecimientos de Salud (CLUES).
- **Clase de fuente:** Registro administrativo `[verificado]`.
- **Institución:** Dirección General de Información en Salud (DGIS), Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** actualización continua, corte mensual `[verificado]`.
- **Cobertura:** todo establecimiento del sector salud (público, privado, social, fijo o móvil) — entidad, municipio, localidad y domicilio; tipo, tipología, institución `[verificado]`. Coordenadas geográficas (lat/long) nativas **no confirmadas** en el catálogo oficial — derivados de terceros (Ominis, datamx.io) podrían geocodificarlo, no verificado aquí `[ambiguo]`.
- **Granularidad:** establecimiento (con domicilio/localidad/municipio).
- **Microdatos:** sí, catálogo completo descargable en Excel/CSV `[verificado]`.
- **Acceso:** directa, sin registro `[verificado]`.
- **URL:** http://www.dgis.salud.gob.mx/ (host real es HTTP, no HTTPS, en este entorno — verificado por sondeo directo) · réplicas en datos.gob.mx, gobi.salud.gob.mx (no alcanzable en el sondeo de esta sesión, ver forense/notas de Tarea B).
- **Enlazable con encuesta:** parcial — vía clave CLUES ya citada como variable en microdatos de encuestas de salud (ENSANUT la registra; SAEH ya la usa, `data/inventarios/inventario_fuentes_salud_mexico.md:79`) y como llave institución/localidad. No confirmado que ENSANUT libere CLUES en el microdato público (solo que el instrumento la conoce internamente) — verificar antes de usar como llave real de enlace.
- **Independiente del prestador:** no — es la propia Secretaría de Salud describiendo su propia infraestructura. No es auto-reporte de conducta o desempeño (no aplica el mismo sesgo que "cobertura reportada por el prestador"), pero tampoco es un tercero externo.
- **Relación con el dominio:** es exactamente la clase de fuente que R9.1 necesitaba para una variable de distancia objetivo — georreferenciación de establecimiento, no de conducta.

## 2. Subsistema de Información de Equipamiento, Recursos Humanos e Infraestructura (SINERHIAS)

- **Nombre / siglas:** Subsistema de Información de Equipamiento, Recursos Humanos e Infraestructura para la Salud (SINERHIAS).
- **Clase de fuente:** Registro administrativo `[verificado]`.
- **Institución:** Dirección General de Información en Salud (DGIS), Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** semestral (septiembre, parcial) y anual (abril del año siguiente, cierre) `[verificado]`.
- **Cobertura:** capacidad instalada por unidad médica en operación — camas, consultorios, quirófanos, salas de parto, equipo médico, personal por categoría `[verificado]`.
- **Granularidad:** establecimiento/unidad médica (agregado de capacidad, no de individuos).
- **Microdatos:** agregado por unidad, no microdato de persona `[verificado]`.
- **Acceso:** directa, sin registro (bases de datos abiertas por unidad) `[verificado]`.
- **URL:** http://www.dgis.salud.gob.mx/contenidos/sinais/subsistema_sinerhias.html · https://sinba.salud.gob.mx/SSASINERHIAS (ambas verificadas alcanzables en el sondeo de Tarea B).
- **Enlazable con encuesta:** sí, parcial — vía CLUES de la unidad médica (misma llave que #1).
- **Independiente del prestador:** no — Secretaría de Salud.
- **Relación con el dominio:** candidata directa para R4.1 (mejora documentada de acceso público) SI trae fecha de apertura/ampliación de unidad, verificable a nivel de instrumento, no confirmado en esta sesión — ver Tarea D.

## 3. Subsistema Automatizado de Egresos Hospitalarios (SAEH)

- **Ya en catálogo v1.0, línea 91 — esta entrada solo añade la etiqueta de clase, no es fuente nueva.**
- **Nombre / siglas:** Subsistema Automatizado de Egresos Hospitalarios (SAEH).
- **Clase de fuente:** Registro administrativo `[verificado]`.
- **Institución:** DGIS, Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** bases anuales desde 2008, cubos desde 2000 `[verificado]`.
- **Cobertura:** egreso hospitalario individual (caso), con clave CLUES de la unidad `[verificado, ya documentado en `data/inventarios/inventario_fuentes_salud_mexico.md:79`]`.
- **Granularidad:** individuo (caso de egreso), con CLUES de unidad.
- **Microdatos:** sí, bases anuales abiertas `[verificado]`.
- **Acceso:** directa, sin registro `[verificado]`.
- **URL:** http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html · https://sinba.salud.gob.mx/CubosDinamicos
- **Enlazable con encuesta:** sí — CLUES↔localidad de la unidad, mismo mecanismo que #1/#2.
- **Independiente del prestador:** no — Secretaría de Salud.
- **Relación con el dominio:** ya inventariada por dominio SAL; esta entrada solo añade la etiqueta de clase que le faltaba. No es fuente nueva — `dedup.py` la fusiona con la entrada existente por acrónimo.

## 4. Sistema Nacional de Vigilancia Epidemiológica — Anuarios de Morbilidad

- **Ya inventariado, dominio salud ítem 4 (`data/inventarios/inventario_fuentes_salud_mexico.md:59`) — esta entrada solo añade la etiqueta de clase, no es fuente nueva.**
- **Nombre / siglas:** Sistema Nacional de Vigilancia Epidemiológica (SINAVE), componente de notificación semanal SUIVE.
- **Clase de fuente:** Registro administrativo `[verificado]`.
- **Institución:** Dirección General de Epidemiología (DGE), Secretaría de Salud `[verificado, ya en `inventario_fuentes_salud_mexico.md:62`]`.
- **Periodicidad y ediciones:** anual, serie 1984-2024; microdato caso a caso solo para eventos de notificación obligatoria específicos (influenza, COVID) `[verificado]`.
- **Cobertura:** nacional y estatal, por semana epidemiológica `[verificado]`.
- **Granularidad:** entidad (agregado); caso individual solo en subsistemas de notificación obligatoria específicos, no confirmado el acceso público a ese nivel `[ambiguo]`.
- **Microdatos:** agregado (tabulados); microdato de caso — no verificado el acceso público en esta sesión.
- **Acceso:** directa, sin registro, para los tabulados `[verificado]`.
- **URL:** https://epidemiologia.salud.gob.mx/anuario/html/index.html
- **Enlazable con encuesta:** parcial — entidad×año.
- **Independiente del prestador:** no — Secretaría de Salud.
- **Relación con el dominio:** ya inventariada por dominio SAL; esta entrada añade la etiqueta de clase.

## 5. Padrón Único de Beneficiarios de Bienestar (PUB)

- **Nombre / siglas:** Padrón Único de Beneficiarios de Bienestar (PUB).
- **Clase de fuente:** Padrón de programa `[verificado]`.
- **Institución:** Secretaría de Bienestar `[verificado]`.
- **Periodicidad y ediciones:** vigente; periodicidad de actualización no confirmada con precisión en esta sesión `[ambiguo]`.
- **Cobertura:** beneficiarios de programas de desarrollo social federal (incluye Pensión del Bienestar, Becas Benito Juárez, etc.) `[verificado]`.
- **Granularidad:** **no verificada con precisión** — el fetch directo al dataset federal (`datos.gob.mx`) falló por certificado; una variante local (CDMX, `tubienestar.cdmx.gob.mx`) sí parece manejar registro por persona beneficiaria, no confirmado si el federal libera nominal o solo agregado por municipio/programa `[ambiguo, declarado explícitamente — no se rellena a favor de ninguna lectura]`.
- **Microdatos:** ambiguo — no verificado.
- **Acceso:** portales de consulta (`pub.bienestar.gob.mx`, `cpid.bienestar.gob.mx`) no alcanzables en el sondeo de Tarea B desde este entorno (ver nota de host); dataset en `datos.gob.mx` reporta existencia pero no se abrió el esquema.
- **URL:** https://www.datos.gob.mx/dataset/padron_unico_beneficiarios_bienestar · https://www.gob.mx/bienestar/acciones-y-programas/padrones-de-beneficiarios-72139 (alcanzable, verificado) · pub.bienestar.gob.mx, cpid.bienestar.gob.mx (no alcanzables en el sondeo)
- **Enlazable con encuesta:** potencialmente sí — ENIGH ya identifica beneficiarios de la Pensión del Bienestar por clave de programa en su cuestionario de ingresos (`P044`/`P104`, ver `forense/hitoD-preregistro-v2_0.md` Nota 16), lo que sugiere que el padrón podría enlazarse por beneficiario o por entidad×año; no verificado a nivel de microdato del padrón mismo.
- **Independiente del prestador:** no — es el propio operador del programa reportando su padrón. No satisface el criterio de "auditado" que los Umbrales del Hito D exigen cuando piden verificación independiente.
- **Relación con el dominio:** exactamente el tipo de fuente que R5.1 usa indirectamente (vía ENIGH) — un padrón nominal, si fuera enlazable a nivel de hogar, mejoraría la identificación de beneficiarios más allá del proxy de clave de ingreso que Nota 16 ya usa.

## 6. Cero Desabasto

- **Nombre / siglas:** Cero Desabasto — plataforma de reporte ciudadano de desabasto de medicamentos.
- **Clase de fuente:** Transparencia / sociedad civil `[verificado]`.
- **Institución:** colectivo de +140 organizaciones de sociedad civil, impulsado por Práctica: Laboratorio para la Democracia y Nosotrxs — funcionalmente independiente del gobierno `[verificado]`.
- **Periodicidad y ediciones:** operación continua desde hace 5 años; informes anuales "Radiografía del Desabasto de Medicamentos en México", ediciones 2019-2023 confirmadas, PDF descargables `[verificado]`.
- **Cobertura:** reportes de desabasto de medicamentos/insumos/vacunas/anticonceptivos, recolectados directamente de pacientes/familiares/personal de salud vía plataforma web y chatbot de WhatsApp; +14,000 reportes acumulados (cifra creciente, no reconciliada entre fuentes citadas) `[verificado]`.
- **Granularidad:** **no verificada con precisión** — existe sección "Representaciones Estatales" que sugiere desglose por entidad; no confirmado si baja a unidad médica o clave de medicamento sin abrir directamente la sección de datos `[ambiguo, declarado explícitamente]`.
- **Microdatos:** sección "Datos Abiertos" existe en el sitio; formato de descarga y esquema no confirmados en esta sesión `[ambiguo]`.
- **Acceso:** portal público, sin registro para consulta de informes `[verificado]`.
- **URL:** https://cerodesabasto.org (alcanzable, verificado en Tarea B).
- **Enlazable con encuesta:** parcial — potencial entidad×año con ENSANUT (ambas cubren desabasto/vacunación en ventanas comparables), no verificado a nivel de variable.
- **Independiente del prestador:** sí, por diseño — es exactamente el tipo de fuente que R9.2 exige y que el catálogo v1.0 no tenía.
- **Relación con el dominio:** candidata directa para la mitad no cubierta de R9.2 ("disponibilidad y alcance de campaña verificados por fuente independiente del prestador") — ver Tarea D para el contraste contra el D archivado.

## 7. Encuesta Nacional MCCI sobre Corrupción e Impunidad

- **Nombre / siglas:** Encuesta Nacional MCCI sobre Corrupción e Impunidad.
- **Clase de fuente:** Transparencia / sociedad civil `[verificado]`.
- **Institución:** Mexicanos Contra la Corrupción y la Impunidad (MCCI), organización no gubernamental fundada en 2015 `[verificado]`.
- **Periodicidad y ediciones:** ediciones 2019, 2022, 2024 (según hallazgos del fork de investigación; no verificado el listado completo) `[no verificado con precisión]`.
- **Cobertura:** percepción y prevalencia de corrupción; incluye temas de corrupción en instituciones de salud (IMSS/ISSSTE/INSABI) según cobertura declarada, no confirmado el detalle del cuestionario `[ambiguo]`.
- **Granularidad:** nacional, con posible desagregación — no verificado con precisión.
- **Microdatos:** MCCI declara publicar bases completas de cada edición, pública y gratuita `[verificado por declaración de la organización, no se abrió el dataset]`.
- **Acceso:** portal público `[verificado]`, pero el sondeo directo del host devolvió 403 en esta sesión (posible bloqueo anti-bot, no necesariamente indisponibilidad — ver Tarea B).
- **URL:** https://contralacorrupcion.mx/encuesta-nacional-mcci-corrupcion-e-impunidad/
- **Enlazable con encuesta:** parcial — tema de corrupción en instituciones de salud podría cruzar con ENCIG/ENSANUT a nivel entidad×año, no verificado a nivel de variable.
- **Independiente del prestador:** sí — ONG.
- **Relación con el dominio:** candidata adicional para el eje de transparencia, no ligada directamente a ninguna de las 27 fichas en esta sesión — se registra por completitud de barrido de clase.

## 8. Comisión Nacional del Sistema de Ahorro para el Retiro (CONSAR) — series ampliadas

- **Nombre / siglas:** CONSAR — estadísticas del Sistema de Ahorro para el Retiro (SAR): recursos administrados, aportaciones voluntarias, comisiones por AFORE.
- **Clase de fuente:** Regulador o sectorial no-INEGI `[verificado]`.
- **Institución:** Comisión Nacional del Sistema de Ahorro para el Retiro `[verificado]`.
- **Periodicidad y ediciones:** series históricas vigentes, actualización periódica `[verificado]`.
- **Cobertura:** aportación voluntaria (ya citada como fuente de R1.2), y series adicionales de comisiones y traspasos entre AFORE `[verificado la existencia; no verificada la desagregación exacta de cada serie]`.
- **Granularidad:** AFORE/entidad-agregado — no confirmada desagregación individual `[ambiguo]`.
- **Microdatos:** agregado (montos por AFORE, no por cuentahabiente) `[verificado]`.
- **Acceso:** directa, sin registro `[verificado]`.
- **URL:** https://www.consar.gob.mx (alcanzable por HTTPS, verificado) · https://www.gob.mx/consar (alcanzable, verificado) · réplica en datos.gob.mx.
- **Enlazable con encuesta:** parcial — mismo problema que la fuente ya usada en R1.2, agregado no individual.
- **Independiente del prestador:** sí — regulador.
- **Relación con el dominio:** ya usada en R1.2 (dato puntual de aportación voluntaria); esta entrada confirma que existen series adicionales del mismo regulador, sin verificar si alguna ayuda a otra ficha.

## 9. Instituto Nacional Electoral (INE) — cómputos y resultados electorales

- **Nombre / siglas:** Sistema de Consulta de la Estadística de las Elecciones (SICEE) y cómputos distritales del INE.
- **Clase de fuente:** Regulador o sectorial no-INEGI `[verificado]`.
- **Institución:** Instituto Nacional Electoral, órgano constitucional autónomo `[verificado]`.
- **Periodicidad y ediciones:** por proceso electoral, histórico disponible `[verificado]`.
- **Cobertura:** resultados electorales oficiales `[verificado]`.
- **Granularidad:** **casilla, sección, distrito, municipio, entidad — confirmado explícitamente por el propio INE** `[verificado]`. Es más fina que la que el cruce v1.0 asumía ("granularidad municipal es hueco declarado", `forense/cruce-catalogo-fichas-v1_0.md:176` sobre R7.1) — hallazgo relevante para Tarea D/C, no adjudicado aquí, requiere abrir el instrumento.
- **Microdatos:** sí, bases de cómputos descargables por casilla `[verificado]`.
- **Acceso:** directa, sin registro `[verificado]`.
- **URL:** https://www.ine.mx (alcanzable, verificado) — cómputos y PREP en subdominios por año, no sondeados individualmente en esta sesión.
- **Enlazable con encuesta:** sí, parcial — sección electoral podría parear con localidad/AGEB de encuestas de hogar si ambas comparten geocódigo INEGI, no verificado a nivel de instrumento.
- **Independiente del prestador:** sí — regulador autónomo.
- **Relación con el dominio:** revisa el hueco de granularidad que el cruce v1.0 declaró para R7.1 — la candidata (ENCUP + registros del INE) puede ser más viable de lo que v1.0 registró, si la sección electoral es la unidad correcta. No se adjudica aquí — ver Tarea C.

## 10. Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL) — reclasificación

- **Nombre / siglas:** CONEVAL — medición multidimensional de la pobreza.
- **Clase de fuente:** Regulador o sectorial no-INEGI **hasta jul/2025; después, ya no aplica esa clase** — ver nota de reclasificación abajo.
- **Institución:** Consejo Nacional de Evaluación de la Política de Desarrollo Social, **absorbido por INEGI el 17/jul/2025** según hallazgo del fork de investigación de esta sesión `[verificado por búsqueda; no re-verificado por segunda fuente independiente — reportar con esa reserva]`.
- **Periodicidad y ediciones:** histórico hasta jul/2025; medición vigente ahora publicada por el propio INEGI.
- **Cobertura:** pobreza multidimensional, derivada de ENIGH; carencia por acceso a servicios de salud y por alimentación `[verificado, ya en `inventario_fuentes_salud_mexico.md:275`, aunque sin la fecha de absorción]`.
- **Granularidad:** individuo/hogar (ENIGH-derivado).
- **Microdatos:** sí, bases de cálculo y programas de replicación descargables `[verificado]`.
- **Acceso:** directa `[verificado]`.
- **URL:** https://www.coneval.org.mx (alcanzable, redirección 301, verificado — archivo histórico) · producción vigente en inegi.org.mx.
- **Enlazable con encuesta:** sí — deriva de ENIGH, ya en el catálogo.
- **Independiente del prestador:** no aplica de la misma forma tras la absorción — ya no es una entidad reguladora separada de INEGI, el propio productor de la encuesta base.
- **Relación con el dominio:** **nota de reclasificación, no hallazgo de fuente nueva.** Si esta absorción se confirma en un acto posterior con fuente primaria (no solo el hallazgo de búsqueda de este acto), CONEVAL deja de contar como ejemplo de la clase "regulador o sectorial no-INEGI" — se declara aquí como advertencia, no se ajusta el catálogo existente sin verificación adicional.

## 11. Comisión Federal para la Protección contra Riesgos Sanitarios (COFEPRIS) — Visor de Registros Sanitarios

- **Nombre / siglas:** COFEPRIS — Visor de Registros Sanitarios de Medicamentos.
- **Clase de fuente:** Regulador o sectorial no-INEGI `[verificado]`.
- **Institución:** Comisión Federal para la Protección contra Riesgos Sanitarios `[verificado]`.
- **Periodicidad y ediciones:** plataforma activa desde abril de 2025 `[verificado]`.
- **Cobertura:** registro de vigencia/autorización de producto farmacéutico (28 campos, consulta por 8 criterios) — **no mide desabasto ni disponibilidad**, es registro de producto, no de conducta ni de existencia física en unidad `[verificado]`.
- **Granularidad:** por registro sanitario / medicamento (no por establecimiento ni por evento de desabasto).
- **Microdatos:** microdato-tipo, consultable por criterios, no descarga masiva confirmada `[ambiguo]`.
- **Acceso:** directa, consulta pública `[verificado]`.
- **URL:** https://www.gob.mx/cofepris (alcanzable, verificado) · transparencia.cofepris.gob.mx (no sondeado individualmente).
- **Enlazable con encuesta:** no directo — es registro de producto, no de conducta ni de establecimiento georreferenciado.
- **Independiente del prestador:** sí — regulador.
- **Relación con el dominio:** **descartada explícitamente para R9.2** — no construye la variable de abasto/campaña que esa ficha necesita, pese a ser regulador independiente del prestador asistencial (es regulador del producto, no auditor de existencias en unidad).

## 12. Encuesta de Satisfacción, Trato Adecuado y Digno (ESTAD) — buscada como "ENSATD"

- **Nombre / siglas:** Encuesta de Satisfacción, Trato Adecuado y Digno (ESTAD/SESTAD según entidad). **Discrepancia de nomenclatura declarada:** el nombre "ENSATD" que cita el encargo no se encontró verbatim en ninguna fuente institucional — el instrumento real se llama ESTAD (federal) o SESTAD (variante estatal, ej. Quintana Roo) `[verificado — se reporta como hallazgo, no como fuente inexistente]`.
- **Clase de fuente:** Encuesta institucional (no de hogares) `[verificado]`.
- **Institución:** Dirección General de Calidad y Educación en Salud (DGCES), con Instituto Nacional de Salud Pública (INSP), desde 2015 `[verificado]`.
- **Periodicidad y ediciones:** vigente desde 2015, aplicación continua en Consulta Externa `[verificado]`.
- **Cobertura:** satisfacción y trato digno — 8 dimensiones (trato digno, confidencialidad, oportunidad, comunicación interpersonal, autonomía, financiamiento, calidad técnica, calidad percibida). Aplicada en paralelo por Monitores Institucionales y Monitores Ciudadanos (Aval Ciudadano), diseño explícito para contrastar ambas fuentes `[verificado por lectura directa del instructivo oficial]`.
- **Granularidad:** establecimiento (unidad médica) — el formulario se llena unidad por unidad.
- **Microdatos:** no verificado si hay portal de datos abiertos público; el instructivo consultado es interno para monitores `[ambiguo]`.
- **Acceso:** no verificado el acceso público a los resultados agregados o microdato `[ambiguo]`.
- **URL:** https://calidad.salud.gob.mx (alcanzable, verificado) · variante estatal https://sesa.qroo.gob.mx/sestad/ (no alcanzable en el sondeo de esta sesión).
- **Enlazable con encuesta:** no — no comparte muestra con encuestas de hogar.
- **Independiente del prestador:** parcial — el componente de Aval Ciudadano introduce una capa no institucional, pero la propia Secretaría de Salud diseña y coordina el instrumento.
- **Relación con el dominio:** es exactamente la clase que faltaba para el confusor de "trato" que R4.1 declara CONFUNDIDO — candidata a proxy más fuerte que la mención espontánea de ENSANUT (`U0202`), no verificada a nivel de variable ni de acceso a microdato en esta sesión.

## 13. Encuesta Nacional de Calidad de la Atención del Servicio de Salud (ENCAL, IMSS)

- **Nombre / siglas:** Encuesta Nacional de Calidad de la Atención del Servicio de Salud (ENCAL).
- **Clase de fuente:** Encuesta institucional (no de hogares) `[verificado]`.
- **Institución:** Instituto Mexicano del Seguro Social (IMSS) `[verificado]`.
- **Periodicidad y ediciones:** anual, edición 2024 confirmada `[verificado]`.
- **Cobertura:** satisfacción de usuarios del IMSS con la atención recibida.
- **Granularidad:** regional (Norte/Sureste/etc.) — no confirmada desagregación por unidad individual `[ambiguo]`.
- **Microdatos:** agregado — resultados publicados en PDF por región, no microdato confirmado `[verificado como agregado]`.
- **Acceso:** informes públicos `[verificado]`; microdato no confirmado.
- **URL:** https://www.imss.gob.mx/encuesta-nacional (no sondeado individualmente en Tarea B — host imss.gob.mx no incluido en el lote probado).
- **Enlazable con encuesta:** no — encuesta a usuarios/pacientes del IMSS, no a hogares.
- **Independiente del prestador:** no — el IMSS evaluándose a sí mismo.
- **Relación con el dominio:** confirma la existencia de la clase "encuesta institucional no de hogares" en el sector salud; no se identifica ficha del Hito D que la use directamente en esta sesión.

## 14. Familia de instrumentos de satisfacción de usuarios (IMSS) — ENSAT, ES-HR y afines

- **Nombre / siglas:** Sistema Integral de Medición de la Satisfacción de Usuarios (IMSS), incluye instrumentos como ENSAT y ES-HR.
- **Clase de fuente:** Encuesta institucional (no de hogares) `[verificado la existencia de la familia; no profundizado por instrumento]`.
- **Institución:** IMSS `[verificado]`.
- **Periodicidad y ediciones:** múltiples instrumentos, evidencia de aplicación 2018-2022 `[no verificado con precisión — familia de instrumentos, no uno solo]`.
- **Cobertura:** satisfacción por unidad/hospital, según instrumento `[ambiguo — no diferenciado instrumento por instrumento]`.
- **Granularidad:** por unidad/hospital según instrumento, no verificado con precisión.
- **Microdatos:** no verificado.
- **Acceso:** no verificado.
- **URL:** imss.gob.mx (no sondeado el subdominio específico).
- **Enlazable con encuesta:** no verificado.
- **Independiente del prestador:** no — IMSS.
- **Relación con el dominio:** **registrada como clase vacía de detalle, búsqueda hecha, no descartada.** Requiere sesión dedicada para diferenciar instrumentos antes de usarse como candidata de ninguna ficha.

## 15. Global Findex Database (México como país incluido)

- **Ya en catálogo v1.0, línea 89 (`data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:174`) — esta entrada solo añade la etiqueta de clase, no es fuente nueva.**
- **Nombre / siglas:** Global Findex Database.
- **Clase de fuente:** Internacional con dato de México `[verificado]`.
- **Institución:** Banco Mundial.
- **Cobertura:** inclusión financiera, México incluido como país de la muestra.
- **Granularidad:** nacional (país como unidad de reporte primario); algunos años con microdato de la encuesta base a nivel individuo, no confirmado el acceso para México específicamente en esta sesión `[ambiguo]`.
- **Microdatos:** agregado por país en el reporte estándar; posible microdato de encuesta base no verificado aquí.
- **Acceso:** directa `[verificado]`.
- **URL:** https://www.worldbank.org (alcanzable, verificado en Tarea B).
- **Enlazable con encuesta:** no, a nivel agregado nacional.
- **Independiente del prestador:** no aplica (fuente internacional, no hay "prestador" en el sentido de las fichas de salud).
- **Relación con el dominio:** ya en catálogo v1.0 por dominio FIN; esta entrada solo añade la etiqueta de clase.

## 16. Barómetro de las Américas (LAPOP)

- **Ya en catálogo v1.0, línea 53 — esta entrada solo añade la etiqueta de clase, no es fuente nueva.**
- **Nombre / siglas:** LAPOP / AmericasBarometer.
- **Clase de fuente:** Internacional con dato de México `[verificado]`.
- **Institución:** Vanderbilt University.
- **Granularidad:** individuo (encuesta), agregable a nacional.
- **Microdatos:** sí `[verificado, ya en catálogo]`.
- **Acceso:** directa `[verificado]`.
- **URL:** vanderbilt.edu (dominio ya en la lista blanca de red de este entorno).
- **Enlazable con encuesta:** sí — comparable con ENCUCI (confianza interpersonal, cultura cívica).
- **Independiente del prestador:** no aplica.
- **Relación con el dominio:** ya en catálogo v1.0; esta entrada añade la etiqueta de clase. Candidata ya descartada explícitamente para R8.3 en `forense/cruce-catalogo-fichas-v1_0.md:124` (más del mismo problema de `conf.06`, no lo reconcilia).

## 17. Latinobarómetro

- **Ya en catálogo v1.0, línea 54 — esta entrada solo añade la etiqueta de clase, no es fuente nueva.**
- **Nombre / siglas:** Latinobarómetro — muestra de México.
- **Clase de fuente:** Internacional con dato de México `[verificado]`.
- **Institución:** Corporación Latinobarómetro.
- **Granularidad:** individuo.
- **Microdatos:** sí `[verificado, ya en catálogo]`.
- **Acceso:** directa `[verificado]`.
- **URL:** latinobarometro.org (dominio ya en la lista blanca de red de este entorno).
- **Enlazable con encuesta:** sí, mismo argumento que LAPOP.
- **Independiente del prestador:** no aplica.
- **Relación con el dominio:** ya en catálogo v1.0; misma descartada para R8.3 que LAPOP, mismo motivo.

## 18. Health at a Glance: Latin America and the Caribbean (OCDE)

- **Nombre / siglas:** Health at a Glance: Latin America and the Caribbean (OCDE/Banco Mundial).
- **Clase de fuente:** Internacional con dato de México `[verificado]`.
- **Institución:** OCDE, con Banco Mundial.
- **Periodicidad y ediciones:** ediciones 2020, 2023 `[verificado]`.
- **Cobertura:** indicadores comparativos de salud entre 33 países, incluido México.
- **Granularidad:** **nacional (país) — no se confirmó desagregación subnacional para México** `[verificado como limitación]`.
- **Microdatos:** agregado únicamente, indicadores comparativos `[verificado]`.
- **Acceso:** directa, informes públicos `[verificado]`.
- **URL:** https://www.oecd.org (el sondeo directo del host devolvió 403 en esta sesión — probable bloqueo anti-bot del sitio, no necesariamente indisponibilidad; ver Tarea B).
- **Enlazable con encuesta:** no — granularidad nacional no enlaza con ninguna condición de Umbral que pida conducta individual.
- **Independiente del prestador:** no aplica.
- **Relación con el dominio:** nueva para el catálogo, pero **su propia granularidad la descalifica** para cualquiera de las 27 fichas del Hito D, todas construidas sobre conducta individual u hogar — útil solo como contexto comparativo internacional, nunca como fuente de un Umbral.

---

## Clases sin resultado adicional verificable en esta sesión

Ninguna de las seis clases quedó sin al menos una fuente verificada — todas están representadas
arriba (Registro administrativo: #1-4 · Padrón de programa: #5 · Transparencia/sociedad civil:
#6-7 · Regulador o sectorial no-INEGI: #8-11 · Encuesta institucional no de hogares: #12-14 ·
Internacional con dato de México: #15-18). Búsqueda hecha: 11 consultas WebSearch + 5 WebFetch
(fork de investigación de esta sesión) + sondeo directo de host para cada una (Tarea B, mismo
acto). No se afirma que esta lista sea exhaustiva — es la primera pasada, con la disciplina de
`README-inventarios.md`: catalogación, no exploración de estructura.
