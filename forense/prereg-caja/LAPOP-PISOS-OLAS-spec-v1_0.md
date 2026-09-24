# LAPOP México por ola · pisos de interés, eficacia, confianza, tolerancia y oferta

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `ASTRA5-U3-POLITICA-COMPLETAR` (0-bis `d459637e`), sucesor de
`ASTRA5-U3-POLITICA` (#1084, fusionado en `72595501`). Gobierna cinco CALC,
uno por estudio mexicano AmericasBarometer disponible en la raíz:
`CALC-LAPOP-PISOS-2004-0001`, `CALC-LAPOP-PISOS-2006-0001`,
`CALC-LAPOP-PISOS-2019-0002`, `CALC-LAPOP-PISOS-2021-0001` y
`CALC-LAPOP-PISOS-2023-0001`. El dictamen por ola y reactivo que decide qué se
mide y qué comparaciones son admisibles vive en
`forense/analisis/dominios/politica/lapop-dictamen-olas-v1_0.tsv` y se congela
en el mismo commit que esta spec, antes de abrir cualquier valor.

## Qué no se repite

`CALC-LAPOP-PISOS-2019-0001` (#1084) ya selló `clien1na` (oferta a la persona)
y `b18` (confianza alta en la Policía) de 2019. No se recalculan: el CALC
`2019-0002` sólo mide los reactivos 2019 que faltan. `CALC-0002` mide `b18`
sólo entre víctimas como índice de contexto y
`CALC-ARBITRO-MARGINALES-2-LAPOP-0001` mide asociaciones oferta/voto y
`vb20`; ninguno es un marginal nacional de estos reactivos. Valores GEN1
(`data/l4-*`, `data/l9-*`) orientan el código, no alimentan números.

## Estimandos y umbrales, fijados antes de abrir valores

Unidad: persona entrevistada del estudio nacional de la ola. Universo por
reactivo: entrevistas con código sustantivo dentro de la escala declarada.
No sabe, no responde e inaplicable quedan fuera y se cuentan como
`n_no_sustantivo`. Todo estimando es una proporción ponderada
`suma(peso·evento)/suma(peso)`:

| familia | reactivo | escala | evento | razón del umbral |
|---|---|---|---|---|
| confianza | `b18`, `b21` | 1 nada … 7 mucho | 6 ó 7 | el mismo corte ya sellado para `b18` 2019 en `2019-0001`; los dos puntos superiores de siete |
| eficacia | `eff1`, `eff2` | 1 muy en desacuerdo … 7 muy de acuerdo | 6 ó 7 | mismo corte que la batería 1–7 de confianza, para no elegir umbral por reactivo |
| interés | `pol1` | 1 mucho, 2 algo, 3 poco, 4 nada | 1 ó 2 | corte en el punto medio de cuatro categorías ordenadas |
| tolerancia | `d1`–`d4` | 1 desaprueba firmemente … 10 aprueba firmemente | 6 a 10 | mitad superior de la escala de diez |
| oferta | `clien1n` | 1 sí, 2 no | 1 | «a alguien que usted conoce le ofrecieron»; objeto distinto de `clien1na` |

Ninguno de esos umbrales se mueve después de ver resultados. `clien1n` es un
reporte sobre terceros conocidos: no es oferta a la persona, recepción,
aceptación ni voto comprado, y no se suma con `clien1na`.

## Diseño por ola

| CALC | payload | estrato | UPM | peso | modo y población |
|---|---|---|---|---|---|
| 2004-0001 | `642348348mexico_2004_export_version` | `mestrat` (4 regiones) | `mprov`×`msec` (sección electoral dentro de estado) | 1 (reporte técnico: *Unweighted*) | presencial en papel; adultos, 130 sitios |
| 2006-0001 | `518939279mexico_lapop_final_2006_data_set_092906` | `ESTRATOPRI` | `UPM` | 1 (reporte técnico: *Unweighted*) | presencial; «idéntico en diseño a 2004», 127 secciones, conglomerados de 12 |
| 2019-0002 | `mexico_lapop_americasbarometer_2019_v1_0_w` | `estratopri` | `upm` | `wt` (=1, autoponderada) | presencial con dispositivo; marco padrón 2010 |
| 2021-0001 | `mex_2021_lapop_americasbarometer_v1_2_w` | `estratopri` | `upm` | `wt` (ponderada) | **telefónica CATI, RDD móvil**; sólo personas con celular funcional |
| 2023-0001 | `mex_2023_lapop_americasbarometer_v1_0_w` | `estratopri` | `upm` | `wt` (=1, autoponderada) | presencial; marco Censo 2020 |

Los reportes técnicos 2021 y 2023 nombran `strata` en su `svyset`. En ambos
archivos esa variable está etiquetada «Peso estandarizado», así que no se usa.
Se usa el estrato primario `estratopri`, del que se anidan las UPM. Es una
estratificación más gruesa y conservadora para la varianza, e igual a la
de 2019. En 2004 la variable `wt` se lee sólo como diagnóstico (mínimo y
máximo); el peso usado es 1 porque así lo declara la ficha técnica.

## Procedimiento

1. Se lee el `.dta` con `pyreadstat` sin convertir faltantes de usuario: los
   faltantes extendidos de Stata (`.a`, `.b`, `.c`) llegan como vacíos. Los
   códigos numéricos de no respuesta que declara cada spec (8/88 en 2004 y
   2006; 888888/988888/999999 en 2019–2023) cuentan como no sustantivos.
2. Cualquier otro valor fuera de la escala, que no sea vacío ni un código de
   no respuesta declarado, detiene la estimación de ese reactivo con
   `ESCALA-DISCREPANTE`. Se reporta el conteo y no se recodifica. Esta
   guardia protege 2006, cuya escala 1–7 se sostiene por el diseño idéntico a
   2004 y por la etiqueta, porque no hay cuestionario 2006 en el corpus.
3. Filtro de diseño: peso finito y positivo, estrato y UPM presentes.
4. Guardia de tamaño: con `n < 30` el reactivo sale `NO-ESTIMABLE`.
5. IC95: 2 000 réplicas de bootstrap de UPM con reemplazo dentro de estrato.
   Los estratos con una sola UPM quedan fijos. Generador `numpy.PCG64`, con
   semilla `42 + desplazamiento` fijado por reactivo en cada `spec.yaml`, y
   percentiles 2.5/97.5. Se reportan `n`, `n_evento`, masa ponderada,
   estratos, UPM y réplicas finitas.
6. Salida: JSON canónico ordenado. En 2023, `b18` y `b21` forman
   `RESULT-LAPOP-PISOS-2023-POL001`, el contrato U0 POL-001, separado del
   resto de reactivos de la ola.

## Comparaciones y rupturas

Cada ola es un punto retrospectivo propio. El dictamen admite comparar
**descriptivamente** los puntos de las olas marcadas `EQUIVALENTE` para un
reactivo, siempre con fechas de campo y marcos explícitos. 2021 queda como
**ruptura de modo y población** y se reporta aparte: nunca entra en la misma
línea que las olas presenciales. En 2023, `d3` y `d4` se preguntaron sin `d1`
y `d2` antes, así que su equivalencia lleva reserva de orden. No se construye
serie, modelo de tendencia, IC predictivo, retador ni detección de cambio.
Cinco olas irregulares, con marcos y modos distintos, no calibran: todos los
CALC quedan `SIN-HISTORIA-PARA-CALIBRAR`. Tampoco se atribuye causalidad a
elecciones, escándalos ni campañas que coinciden con el campo, como la
campaña presidencial de 2006, la intermedia de 2021 o la pandemia.

No hay celdas geográficas ni cruces por segmento. No se une a secciones INE ni
se perfilan votantes. Sólo se publican agregados nacionales; el microdato
LAPOP, sujeto a la licencia de clic de uso no transferible, no entra al repo.

## Auditoría de rigor extremo

Son proporciones declaradas de entrevistados, retrospectivas, con IC de
muestreo bajo un diseño aproximado. Ese IC no cubre sesgo de no respuesta,
de cobertura (en 2021, quienes no tienen celular) ni efectos de casa
encuestadora. La confianza declarada en policía y partidos puede responder a
experiencias con instituciones, violencia y acceso, no a una disposición
cultural fija. Un marginal nacional no dice nada de rural, indígena o
popular. «Le ofrecieron a un conocido» no prueba compra de voto y la oferta
no es asignación aleatoria. El secreto del voto limita cualquier inferencia
sobre elección. Ninguna diferencia entre olas se presenta como cambio causal.
