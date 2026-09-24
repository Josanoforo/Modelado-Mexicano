# CALC-ENCUP-PISOS-2012-0002 · Interés, eficacia y confianza

El primer resultado que produzca este procedimiento es el que se reporta.
Sucesor explícito de `CALC-ENCUP-PISOS-2012-0001`: su primer run falló sin
sellar por buscar códigos como nombres completos de columna. La inspección
posterior de cabeceras mostró que cada columna comienza `CÓDIGO. ` seguido
del texto de pregunta. Esta versión resuelve exactamente una columna por
prefijo código+punto+espacio y preserva los estimandos y umbrales previos.
Fuente: `encup_2012_base_datos_xlsx`, hoja `BaseDatos_ENCUP_2012_Final`.
Unidad: persona entrevistada por ENCUP 2012. Las cinco olas con cuestionario
(2001, 2003, 2005, 2008 y 2012) no equivalen a cinco bases disponibles:
este CALC usa únicamente la base 2012. No construye serie ni inferencia por
entidad. Los ejes existentes del instrumento incluyen edad, pero no se
publican cruces pequeños en este piso.

Reactivos y códigos de cuestionario 2012:

* `P37`: «En general ¿qué tan interesado está usted en la política?» 1 mucho,
  2 poco, 3 nada, 98 no sé, 99 no contesta. Se publica distribución ordinal y
  proporción 1 entre 1/2/3, fijada antes de ver el resultado.
* `P51_2`: «¿Qué tanto cree usted que los ciudadanos pueden influir en las
  decisiones del gobierno?» 1 mucho, 2 poco, 3 nada, 98/99 no respuesta.
  Se publica distribución y proporción 1 entre 1/2/3.
* `P30_15`: «¿Qué tanto confía en… El Instituto Federal Electoral?» escala
  0 nada a 10 mucho, 99 no contesta. Distribución 0..10 y proporción 8..10
  entre 0..10. El umbral 8 define confianza alta antes de la corrida.
* `P30_10`: mismo tallo de pregunta, «Los vecinos». Mismo umbral. Objeto
  interpersonal distinto de confianza en institución electoral.

Se lee el XLSX completo, sin ponderador: no hay peso/estrato/UPM verificado
en el corpus para ENCUP, y este CALC no afirma que la distribución de las
filas sea estimación representativa de México. Se reportan conteos válidos y
no sustantivos por reactivo. No hay IC de diseño hasta resolver esas piezas.
El n mínimo para una proporción es 30; si hay menos, se devuelve null con
conteos y el estado NO-ESTIMABLE. No se elige un umbral tras mirar resultados.
No se usa `P44A` (obediencia a leyes) ni `P68` (voluntad de mayoría) como
jerarquía interpersonal. No se combinan personas ENCUP con secciones INE.

## Auditoría de rigor extremo

Las cifras son retrospectivas de personas entrevistadas y no se mezclan con
marcas de voto administrativas. Interés y eficacia declarados no prueban
conducta electoral. El IFE de 2012 no se renombra como INE de 2024.
Clase media urbana, condiciones rurales/indígenas, no respuesta y modo de
levantamiento pueden cambiar una comparación. No se atribuye cultura a
restricciones de información o incentivos. Sin contraste directo con
clientelismo causal. Cero contadores movidos antes de ejecutar.
