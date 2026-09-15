# GEN2-38 · DEM-AHORRO-STOCK-DURACION-01

Fecha de exploración: 2026-09-15. Entorno: CAJA (WSL2), con
`data/raw -> /home/pc0/mm-corpus/raw` y red real confirmada contra
`https://www.inegi.org.mx/` (HTTP 200). Este documento registra una sonda; no
adopta científicamente una fuente.

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`.

Definición: «¿Existe un instrumento público mexicano que observe por separado
tenencia/ausencia de ahorro y duración suficiente del stock?»

Estado de entrada: ENIF, EACF, ENSAFI, Findex, ENFIH e IIEG Jalisco ya fueron
examinados. ENIF 2024 P4_10 mezcla «menos de una semana» con «no tiene ahorros»;
no se repitieron las tres descargas IIEG agotadas.

Modos ejecutados: CONSTRUCTO, HERMANAS y LATERAL.

## Consultas y resultados

- Buscador web: `site:microdata.worldbank.org Mexico financial capability survey savings how long cover expenses questionnaire`. Localizó el catálogo del Banco Mundial y el estudio mexicano de capacidades financieras de 2012; no afloró una ficha de variable que midiera duración del mismo stock.
- Buscador web: `México encuesta capacidades financieras cuánto tiempo cubrir gastos ahorros microdatos`. Reprodujo EACF/ENIF ya examinadas y ubicó la familia de capacidades financieras Banco Mundial/CNBV/CONDUSEF.
- Buscador web: `Mexico financial capability survey 2013 questionnaire savings emergency duration stock`. Ubicó el informe público del levantamiento mexicano 2012.
- Buscador web: `site:datos.gob.mx encuesta ahorro cuánto tiempo podría cubrir gastos sin ingresos`. No añadió un instrumento distinto con el objeto exacto.
- Buscador web: `"Encuesta de capacidades financieras" México 2012 cuestionario ahorro "tiempo" gastos`. Confirmó el instrumento 2012 y documentación, sin acreditar el reactivo conjunto requerido.
- Buscador web: `"Financial Capability Survey" Mexico 2012 questionnaire microdata`. Confirmó población nacional de 2,022 adultos, ponderadores y diseño probabilístico multietápico.
- Inspección de contenido del informe público `https://documents1.worldbank.org/curated/en/653031468287158989/pdf/821340ESW0whit00Box379873B00PUBLIC0.pdf`: documenta ahorro formal, tandas y ahorro sin intermediario, y capacidad para cubrir un gasto inesperado equivalente a un mes de ingreso. Las búsquedas internas `how long`, `emergency`, `savings account` y `unexpected expense` no acreditaron una duración en días/meses condicionada al stock observado.

## Candidata examinada

`MEXICO_FINANCIAL_CAPABILITY_SURVEY_2012` (CNBV, CONDUSEF y Banco Mundial),
informe público citado arriba. Es nueva respecto del universo declarado para
esta versión, pero no es una candidata adquirible pertinente al objeto exacto:
acredita persona adulta, muestra nacional, ponderación/diseño, tenencia/uso de
ahorro y una medida separada de capacidad ante un gasto inesperado; no acredita
que la capacidad sea duración del mismo stock de ahorro ni ofrece categorías
temporales comparables con ENIF 2024. Clasificación: EXISTE-NO-SATISFACE. No se
crea residual ni relación; tampoco se descarga el informe como sustituto de
microdato.

## Segunda pasada crítica y frontera

Se examinó el objeto exacto, no sólo «ahorro» o «resiliencia». Los resultados
web se contrastaron con población, unidad, variable, temporalidad y diseño. Un
informe y una landing no se trataron como microdato. No quedó una URL de payload
pertinente que justificara handoff GEN2-38.

Resultado operativo corregido: `continua`, sin hallazgo material en este
ciclo. La frontera pública concreta descrita abajo obliga a reanudar el
2026-09-16; no corresponde la espera general hasta el 11/oct. Suficiencia:
identidad PARCIAL (instrumento
identificado, variable exacta no), concepto NO_ACREDITADA, población ACREDITADA,
selección/no respuesta ACREDITADA, unidad ACREDITADA, temporalidad PARCIAL,
diseño ACREDITADA, identificación NO_APLICA; uso INCOMPATIBLE y pregunta
ABIERTA.

Frontera no examinada: cuestionario y diccionario variable-por-variable del
levantamiento mexicano 2012 si aparecen en un repositorio público distinto del
informe; encuestas estatales distintas de IIEG; módulos académicos mexicanos no
indexados. Quedan fuera login, compra y contacto.

Cursor del ciclo siguiente: localizar primero el cuestionario o catálogo de
variables del `MEX_2012_FCS` en catálogo/archivo público y comprobar si existe
una secuencia tenencia positiva -> meses/días financiables sólo con ese ahorro;
no repetir ENIF, EACF, ENSAFI, Findex, ENFIH, IIEG ni las consultas generales de
este ciclo. Si un segundo ciclo de esta versión tampoco avanza materialmente,
presentar a mesa la alternativa concreta ya configurada: relabel del uso
acotado autorizado por #772, sin ejecutarlo por clasificación.

## Continuación del segundo ciclo · 2026-09-15T12:17:36-06:00

Checkpoint de necesidad: owner `2026-09-15T121736-152735`. Se ejecutaron los
tres modos sobre la frontera heredada, sin repetir las consultas generales del
primer ciclo:

- CONSTRUCTO/HERMANAS, buscador web: `"MEX_2012_FCS" questionnaire`,
  `"Mexico Financial Capability Survey" 2012 questionnaire pdf`,
  `"MEX_2012_FCS" variables savings` y
  `site:microdata.worldbank.org "MEX_2012_FCS"`. El resultado indexado fue el
  informe público ya examinado y estudios mexicanos distintos; no apareció un
  cuestionario ni diccionario del objeto exacto.
- LATERAL, buscador web: `microdata library Mexico 2012 Financial Capability
  Survey MEX FCS catalog`, `site:microdata.worldbank.org/index.php/catalog
  Mexico Financial Capability Survey 2012`,
  `site:microdata.worldbank.org/index.php/catalog/ "Financial Capability
  Survey" Mexico` y `site:microdata.worldbank.org/index.php/catalog/
  "MEX_2012"`. El catálogo indexó ENIF 2012 y otros estudios, no el cuestionario
  de `MEX_2012_FCS`.
- LATERAL, consulta directa del buscador público del catálogo:
  `curl -L -A 'Mozilla/5.0' --max-time 30
  'https://microdata.worldbank.org/index.php/catalog/?sk=MEX_2012_FCS&sort_by=rank'`.
  Resultado crudo: HTTP/2 200, 388422 bytes; la página conserva el término de
  búsqueda pero muestra cero estudios. El `200` acredita la consulta, no la
  existencia de un payload.

No se localizó candidata pública nueva y pertinente, por lo que no hubo objeto
de descarga, checkpoint de objeto, residual ni relación. El resultado sigue
siendo `continua`: quedan como frontera concreta archivos públicos de
CNBV/CONDUSEF o repositorios institucionales que pudieran conservar el
cuestionario no indexado, encuestas estatales distintas de IIEG y módulos
académicos mexicanos con catálogo de variables. Quedan fuera login, compra y
contacto.

Cursor siguiente: examinar archivos web públicos de CNBV/CONDUSEF y un
repositorio académico mexicano no recorrido, sin repetir el buscador exacto del
Banco Mundial ni las familias ya agotadas. Evento de reactivación alterno: que
aparezca un cuestionario/diccionario público nuevo del levantamiento 2012.

Este es el segundo ciclo sin avance material. Alternativa concreta para firma
de mesa: cambiar los tres consumidores rotulados `horizonte_corto` a un uso
acotado que refleje exactamente el corte autorizado por #772 (P4_10: categoría
mezclada de menos de una semana o ausencia de ahorro), manteniendo explícito
que no estima duración pura del stock. Esta sonda no ejecuta ni adopta ese
relabel.

Suficiencia separada tras este ciclo: identidad PARCIAL; concepto
NO_ACREDITADA; población ACREDITADA; selección/no respuesta ACREDITADA; unidad
ACREDITADA; temporalidad PARCIAL; diseño ACREDITADA; identificación NO_APLICA;
uso INCOMPATIBLE; pregunta ABIERTA.
