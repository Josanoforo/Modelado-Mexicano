# ASTRA5-U2 ENDIREH · falsadores y no conformidades residuales

**Evidencia primaria mexicana:** cuestionarios, FD, diseño y microdatos INEGI de ENDIREH 2021, 2016, 2011 y 2006 identificados por hash en cada `spec.md`; para 2003, cuestionario/FD públicos y [diseño muestral oficial](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/metodologias/est/dm_endireh03.pdf). Los reports U0 son afirmaciones a contrastar, no fuente de las cifras. Marco importado: ninguno para los estimandos mexicanos. Tier: descriptivo de encuesta compleja, retrospectivo; adopción NO.

## FP · pruebas que podrían falsar el producto

| ID | Instrumento y afirmación contrastable | Falsador concreto |
|---|---|---|
| FP-ENDIREH-2021-A | Pareja física A1/A2 y ayuda/decisiones de relación actual | Cotejo literal del cuestionario A/FD que cambie elegibilidad, ventana o mapeo 1–3/4; recálculo independiente que no reproduzca punto e IC bajo `FAC_MUJ`, `EST_DIS`, `UPM_DIS`. |
| FP-ENDIREH-2021-BC | Pareja B1/B2/C1 física/no física, ayuda y denuncia | Cotejo de cuestionarios B/C que muestre otro subuniverso o un acto especial C mal incluido; recálculo con la misma unión de actos y réplicas que no reproduzca el sello. |
| FP-ENDIREH-2021-83 | Discriminación laboral 8.3 | Evidencia documental de que `P8_3_2_*=3` significa «no sufrió perjuicio estando embarazada»; o discrepancia reproducible tras filtrar `P8_2=1` y respuestas 1/2. |
| FP-ENDIREH-2016 | Ámbitos VI/VII/VIII/X/XIII, servicios y decisiones XIV | Cotejo de los FD A/B/C que invalide el salto por acto, la unión de `P7_11_18` en parte `_2`, el código de decisión 1/4/5 o la asignación de institución/razón; replay divergente con igual corpus. |
| FP-ENDIREH-2016-73 | Discriminación laboral 7.3 | Cotejo del cuestionario que cambie ventana octubre 2011 o semántica del 3; discrepancia reproducible entre RESULT y recálculo independiente con la misma elegibilidad. |
| FP-ENDIREH-2011 | A/B/C y hechos externos 2.6 | FD/cuestionarios que invalide `CP4_1`, códigos 1–3/4, empalme `TSDem` o clasificación por agresor/lugar; reproducción que no cuadre para un mismo dominio/UPM. |
| FP-ENDIREH-2006 | MC/MD/MS | FD/cuestionarios que cambie códigos 1/2 frente a 3 de pareja MC/MD, `P23` de MS o llave de módulos; replay no idéntico con el ZIP fijado. |
| FP-ENDIREH-2003 | Dictamen de no medibilidad con IC de diseño | Un archivo oficial que entregue UPM y estrato por `LLAVE`, o pesos replicados equivalentes y documentación del factor actualizado: habilitaría spec y tabla 2003 independientes. |

## NC · límites con operación exacta

| ID | Estado | Evidencia y siguiente operación |
|---|---|---|
| NC-ENDIREH-2003-DISENO | **Dependencia externa demostrada** | `nacionalm2` tiene actos y `FAC_PER`, pero los cinco CSV públicos carecen de UPM/estrato y FD/leeme no los derivan de `LLAVE`. Solicitar la llave de diseño o réplicas oficiales por registro, documentar factor actualizado, congelar CALC 2003 propio antes de abrir filas. No se publica punto sin IC. |
| NC-ENDIREH-SERIE | **SIN-HISTORIA-PARA-CALIBRAR** | Actos, elegibilidad y ventanas difieren entre 2006/2011/2016/2021; 2003 carece de llave de diseño. Para pronóstico exigir matriz literal homologada, transiciones independientes no usadas en ajuste y prueba de cobertura. Con esta rama solo hay IC de diseño por ola. |
| NC-ENDIREH-U0-701 | **Sin contraste directo** | El 70.1% U0 es agregado de cualquier violencia. Las tablas por ámbito no comparten siempre universo/ventana y las mujeres pueden aparecer en varios ámbitos. Si se solicita el agregado, congelar unión por mujer y definición oficial exacta en CALC nuevo; nunca sumar prevalencias. |
| NC-ENDIREH-SUBREGISTRO | **No identificado como tasa total** | Ayuda/denuncia se observa entre afectadas con respuesta válida. No se observa la violencia no declarada ni se identifica causalmente por qué no se acudió. Una validación externa enlazada con selección/no respuesta y diseño documentados sería la operación para estimar esa brecha. |
| NC-ENDIREH-PUBLICACION | **Sellada en disco, no registrada** | RESULT, sellos y TSV están en el PR sucesor; el registro público requiere su canal de publicación y firma de mesa. El merge futuro no autoriza adopción causal ni elimina NC anteriores. |

Las diferencias entre grupos describen respuestas por estructura y oportunidad de exposición; no revelan preferencias, adaptación racional individual, psicología, cultura o genética. Ninguna genética poblacional predice la conducta de una persona o grupo. Una razón declarada para no acudir a una autoridad no prueba elección libre cuando la oferta, seguridad o costo de acceso varían. La auditoría de rigor extremo consiste en volver a comprobar texto/código del instrumento, elegibilidad, denominador, diseño, supresión, hash y replay para cada cifra antes de usarla; los FP anteriores indican qué hallazgo obligaría a corregir o retirar una inferencia.
