# ENCUCI2020-EXPOSICION-RESPUESTA-0001 · preregistro v1.0

Congelado el 19 de septiembre de 2026, antes de abrir registros del microdato
en este acto. Gobierna `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001`; el primer
resultado se conservará. La especificación ejecutable completa está en
`data/corrida0/CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001/spec.md` y
`spec.yaml`.

## Preguntas y universo

ENCUCI 2020, persona seleccionada de 15 años o más, `SEC_4_5`, últimos doce
meses desde agosto de 2019. `AP5_16_1..10` son contactos no excluyentes con
diez tipos de autoridad; `AP5_17` es solicitud y `AP5_18` entrega de dádiva.
`FAC_SEL` pondera persona; `EST_DIS`/`UPM_DIS` definen el diseño y `DOMINIO`
conserva sus categorías nativas U/C/R. Los códigos 9, blancos y ajenos no son
negativos.

## Salidas fijadas

1. Proporción Sí por cada tipo entre respuestas 1/2, con n, masa desconocida e
   IC; contacto cualquiera con lógica trivaluada; conteo 0/1/2/3+ sólo con las
   diez respuestas válidas y cobertura explícita.
2. Distribución exhaustiva ninguna/sólo solicitud/sólo entrega/ambas entre
   contacto acreditado y respuestas 1/2, para total, conteo 1/2/3+ y cada
   DOMINIO U/C/R. No se cruza dominio con conteo. Cada grupo informa cobertura,
   P(entrega|solicitud) y P(entrega|no solicitud). Denominador vacío es
   NO-ESTIMABLE sólo para esa razón.
3. Contrastes 2−1 y 3+−1 para la unión solicitud/entrega y para la brecha entre
   los dos condicionales anteriores. Se publican todos los grupos, no sólo los
   que parezcan distintos.

## Incertidumbre y límites

Bootstrap de 2,000 réplicas de UPM dentro de estrato, semilla 20260919 y
`numpy.PCG64`, sobre el marco completo con `FAC_SEL`. Un único sorteo alimenta
todas las estadísticas y diferencias, por lo que conserva covarianza. UPM
singleton se autorremuestrea; diseño incompleto deja IC no disponible sin
eliminar puntos. Ningún contraste es causal. Los tipos no son trámites ni
frecuencias; la dádiva no se atribuye a una autoridad; solicitud y entrega no
demuestran una secuencia de la misma transacción.

## Exposición a resultados

Se conocían `CALC-ENCUCI-0001`, sus resultados nacionales, su medidor, el
preregistro `ENCUCI-MORDIDA-PROTESTA` y la resolución F2. Se usan sólo para
definición y control de contexto; no se reclama ceguera ni se republica la tasa
nacional equivalente como novedad.
