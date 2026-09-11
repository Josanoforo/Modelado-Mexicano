# S12 · CIDE-CSES 2015 — composición del alineamiento entre receptores

### `prereg-caja-S12` · **v1.2** · 10 de septiembre de 2026 · `sucesora_de: v1_1`

Esta versión ejecuta D14/`FP-363` con una pregunta nueva y explícita. No modifica ni rescata el contraste de v1.1: `ALINEADO | receptor` frente a `ALINEADO | no receptor` permanece `NO-ESTIMABLE-CON-ESTA-FUENTE` porque el no receptor carece de partido contraparte.

## Pregunta y alcance

Dentro de quienes declararon haber recibido una **oferta** o una **amenaza** clientelar, ¿qué proporción votó por un partido compatible con el señalado y qué proporción no lo hizo? Oferta y amenaza son dos ramas separadas; nunca se suman ni se promedian y una persona puede aparecer en ambas si recibió ambas.

Es una descripción/asociación condicionada a receptores. La selección en ese subuniverso impide identificar el efecto causal de recibir oferta o amenaza y el contraste no responde a la pregunta original de v1.1.

## Fuente, población, ventana y variables

Fuente única: `cide_cses2015_nacional_poselectoral.sav`, manifiesto `cide_cses2015_nacional_poselectoral`, sha256 `1ef01a17fe6ca10b73db9e988ac4dacac766a6b0759af43f1fd690d3f60d4d80`, 1,200 adultos. Se usa porque `peledip` pregunta por el voto emitido para diputados federales el 7 de junio de 2015; el archivo preelectoral registra otro cargo y no replica este desenlace.

| rama | receptor | partido señalado | códigos |
|---|---|---|---|
| OFERTA | `pcyc13 == 1` | `pcyc13_1` | `1=Sí`, `2=No`, `9=Ns/NC`; partido `97=Ninguno`, `99=NS/NC` |
| AMENAZA | `pcyc14 == 1` | `pcyc14_1` | mismos códigos; el texto condiciona «si Usted recibe alguno de estos beneficios» |

`peledip` es el desenlace de voto. `ALINEADO=1` usa el crosswalk oferente→voto de v1.1: `{1:1, 2:2, 3:4, 4:8, 5:9, 6:19, 7:34, 8:35, 9:36, 10:37, 12:10}`; `peledip=29` (PRI-PVEM) alinea con oferente PRI o PVEM. Votos emitidos `11 Ninguno`, `12 No sabe`, `13 Blanco`, `14 Anulado` y `39 Independiente` son `NO-ALINEADO`, como en v1.1. Oferente `97/99`, partido señalado faltante, voto faltante, ponderador no positivo o atributo de diseño faltante se excluyen y se cuentan.

La exposición ocurrió en la campaña previa y el desenlace corresponde a la elección del 7-jun-2015; el diseño transversal retrospectivo no establece secuencia individual verificable.

## Diseño, ponderación y estimandos

Ponderador global `PONDFIN` («Ponderador nacional»), estrato `dominio` y UPM `upmmn`, confirmados en el metadato. Para cada rama se reportan:

- `n` bruto y suma de pesos de `ALINEADO` y `NO-ALINEADO`;
- proporción ponderada e IC95 de cada grupo;
- contraste descriptivo `Δ_comp = P(ALINEADO) − P(NO-ALINEADO) = 2P(ALINEADO)−1`, con IC95.

Los IC95 son percentiles de 2,000 bootstrap de UPM dentro de estrato, `numpy.PCG64`, semilla `20260910`. La compuerta se satisface si ambos grupos tienen al menos un caso con peso positivo y diseño completo. Una categoría con `n<10` no se borra: se publica con `LIMITADA-N-MENOR-10` y no sustenta generalización. El resultado de una rama no se usa para adjudicar `R7.3`/`R7.6`, mover su tier ni cargar una tasa al motor.

## Soporte previo a congelar

Las etiquetas y saltos reales confirman que `pcyc13_1` y `pcyc14_1` sólo tienen respuesta sustantiva entre receptores, mientras `peledip`, `PONDFIN`, `dominio` y `upmmn` existen en el mismo archivo. Ambas categorías de `ALINEADO` existen en cada rama. Eso abre el cálculo; no anticipa su contraste ni lo convierte en causal.

**El primer resultado que produzca este procedimiento es el que se reporta.**
