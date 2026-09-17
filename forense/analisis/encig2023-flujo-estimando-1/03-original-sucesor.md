# ENCIG 2023 · resultado original y sucesor

La corrida `CALC-ENCIG2023-FLUJO-0001` reproduce exactamente el agregado
condicionado y después aplica el contrato documental de flujo. Las categorías
cierran 123,186 eventos y masa `FAC_TRA` 402,225,102; la unión a 38,966
personas es muchos-a-uno, sin pérdida ni multiplicación.

## Clasificación total

| categoría | n | masa `FAC_TRA` | lectura |
|---|---:|---:|---|
| Respuesta válida observada | 23,100 | 63,712,439 | `P8_4∈{0,1}` después de algún `P8_3_*=1` |
| Salto negativo lógico | 99,924 | 337,524,702 | los tres `P8_3_*=2`; el salto acredita ausencia de las circunstancias |
| Fuera del universo / no aplica | 0 | 0 | ninguna fila de `sec_7` cae fuera del universo fijado |
| Elegibilidad no determinable | 162 | 987,961 | ningún 1 y al menos un 9 en `P8_3` |
| Respuesta faltante pese a ser aplicable | 0 | 0 | no aparece |
| Código o combinación contradictoria | 0 | 0 | no aparece |
| **Total** | **123,186** | **402,225,102** | cierre exacto |

La descomposición completa por `PRE`, `DIG`, `OTRO` y
`CANAL_FALTANTE` está en `02-categorias.tsv`. Este último es una parte
contable, no un canal sustantivo.

## Original frente a sucesor

| campo | agregado condicionado original | sucesor de flujo |
|---|---|---|
| Desenlace | marca `P8_4=1` del **tipo** repetida sobre filas-evento | ocurrencia de circunstancia de solicitud/intento en el evento |
| ¿Mismo desenlace? | — | **distinto en unidad operacional**; ninguno acredita pago |
| Población | eventos con `P8_4` observado | los 123,186 eventos de `sec_7` |
| Unidad | fila-evento ponderada que hereda marca de persona × tipo | evento; una marca de tipo repetido sólo impone “al menos uno” |
| Numerador ponderado | 13,024,773 | conjunto identificado: [8,494,556, 14,012,734] |
| Denominador ponderado | 63,712,439 | 402,225,102 |
| Resultado | **0.2044306136200499** | **[0.021118910674053356, 0.03483803952146179]** |
| Precisión muestral | IC del padre, sin cambio | **NO-CALCULADA**; el rango es identificación lógica, no IC |

El original reconcilia también 23,100 observaciones y 100,086 blancos. Entre
los tipos positivos hay 4,540 `ID_TRA`; 1,195 tienen dos o tres eventos. Por
eso atribuir la marca positiva a todos ellos produce el numerador del padre,
pero no un numerador de eventos con circunstancia.

## Partición y límites

Para el desenlace por evento:

| estado individual | n | masa `FAC_TRA` |
|---|---:|---:|
| positivo conocido (tipo con un solo evento) | 3,345 | 5,844,827 |
| negativo conocido | 116,688 | 388,212,368 |
| desconocido individual | 3,153 | 8,167,907 |
| **universo** | **123,186** | **402,225,102** |

La fórmula de partición sin restricciones internas da
`[5,844,827 / 402,225,102, (5,844,827 + 8,167,907) / 402,225,102]` =
**[0.014531233806486797, 0.03483803952146179]**. La documentación agrega una
restricción válida: cada uno de los 1,195 tipos positivos repetidos contiene
al menos un evento positivo. Sumando el menor `FAC_TRA` dentro de cada tipo,
el límite inferior se estrecha a 8,494,556 / 402,225,102 =
**0.021118910674053356**. No se elige punto medio ni se imputa por canal.

## Lectura sustantiva

El conjunto sucesor describe solicitud, intento o condiciones de corrupción.
No mide entrega: `P8_6` permite explícitamente “No le dio nada”. En
consecuencia, ni el punto original ni el conjunto sucesor corresponden a
`paga_mordida` o a su complemento `tramite_normal` entendido como pago.
