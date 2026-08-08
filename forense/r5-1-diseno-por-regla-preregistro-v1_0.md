# R5.1 · Pre-registro de un diseño por regla de elegibilidad (documento autónomo, no enmienda)

### `r5-1-diseno-por-regla-preregistro` · **v1.0** · 4 de agosto de 2026 · **PRE-REGISTRO SELLADO**

> | | |
> |---|---|
> | **ARCHIVO** | `r5-1-diseno-por-regla-preregistro-v1_0.md` |
> | **NOMBRE ESTABLE** | **`r5-1-diseno-por-regla-preregistro`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Un protocolo **autónomo**, no una enmienda de `hitoD-preregistro-v2_0.md` §R5.1 (línea 138). No toca su Umbral (línea 143) ni su escala A–D (línea 149). Define un segundo diseño de identificación para la misma pregunta sustantiva, sobre **elegibilidad por regla**, no sobre **recepción declarada** |
> | **VERIFICAS ASÍ** | §2 fija el tratamiento por regla **antes** de nombrar una variable de dato · §4 fija las olas y por qué **no** son 2018→2020 · §6 es una escala A–D propia con precedencia explícita, para no repetir el solape de `D5`/`D6` (P3) y `A`/`D` (`R7.2`) · §8 deja la pregunta de si esto cuenta como veredicto de R5.1 **sin resolver**, a propósito |
> | **ESTADO** | **SELLADO.** Cualquier enmienda posterior al primer ajuste se marca **POST-DATO** (§9) |

---

## 0 · Por qué autónomo y no enmienda — la razón completa, antes de cualquier otra cosa

`hitoD-preregistro-v2_0.md` §R5.1 (línea 138-149) ya tiene una corrida completa: `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md` corrió el falsador con ENIGH transversal repetida y propuso fila **A**, sin adjudicar (Nota 16 del pre-registro, línea 890). **Ese resultado ya se vio.** Cualquier cambio al Umbral o a la escala de esa ficha, hecho después de ver ese resultado, es **POST-DATO** — el mismo defecto que `forense/p3-lca-preregistro-v1_0.md` §10 nombra para el LCA multinivel de P3: *"una enmienda posterior al primer ajuste se marca POST-DATO y todo veredicto que dependa de ella se reporta como exploratorio"*.

La salida que ese mismo documento adoptó para su propio caso análogo (el LCA multinivel condicional, §2.5 de `p3-lca-preregistro-v1_0.md`) es la que este documento reproduce aquí: **un protocolo nuevo, sellado antes de correr, con su propio archivo, que no edita el original.** No se reabre `hitoD-preregistro-v2_0.md:138-149`. No se escribe una línea nueva en el Registro de veredictos archivados (append-only, solo emisiones — acto de mesa, no de este documento).

**Contaminación de la sesión que escribe esto, declarada.** Esta sesión leyó `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md` completo — incluyendo sus resultados (§5-§9 de esa nota) — porque el Encargo V se lo pidió explícitamente para escribir §3.3 de este mismo acto. Eso **no** es la misma contaminación que ADR-46 define para microdato: esta sesión **no abrió ningún ZIP ni archivo de datos** de ENIGH, ENASEM ni ninguna otra fuente (verificable: ningún comando de este acto referencia `data/raw`). Pero sí es contaminación de un tipo distinto y hay que decirlo con la misma disciplina: **esta sesión ya sabe que el resultado de R5.1-transversal fue "no hay retroceso, fila A".** Esto no invalida el pre-registro de un diseño *distinto* (mismo principio de ADR-46 y de `p3-lca-preregistro-v1_0.md` §8·Q9: la unidad de contaminación es la sesión, y lo que contamina es haber visto **el mismo dato que este protocolo va a usar**, no haber visto un resultado de un diseño diferente) — pero si algún renglón de abajo parece calibrado para que salga el mismo signo que ya se vio, es exactamente el sesgo que hay que vigilar, y se marca donde aparece (§6, nota al pie de la escala).

---

## 1 · Procedencia — qué se citó, qué se derivó, qué no se abrió

| Fuente | Qué se tomó | Tipo |
|---|---|---|
| `forense/hitoD-preregistro-v2_0.md:138-149` | Umbral y escala originales de R5.1, citados literal para contrastar, no para editar | (1) leído en esta sesión |
| `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md` | Operacionalización de los dos desenlaces (§5), resultado y reserva (§9) — citado como antecedente, no re-derivado | (1) leído en esta sesión |
| `forense/cruce-catalogo-fichas-v1_0.md §3` (caso de prueba R5.1) | ENASEM/MHAS como candidata de panel para R5.1, con sus olas 2018/2021 | (1) leído en esta sesión |
| `forense/notas/2026-08-04-enasem-paso1-descriptor.md` | El límite de la categoría "otra institución" en 2018 (§3, líneas 165-188) | (1) leído en esta sesión |
| `forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` (§3.1 de este mismo Encargo V) | La regla de elegibilidad por régimen, con cita de DOF y fecha para cada tramo | (1) escrito en este mismo acto, anterior a este documento |
| `data/manifiesto.yaml` | Confirmación de que `enigh2018_nc_csv` y `enigh2022_nc_csv` están en el manifiesto (no abiertos, solo se verificó su entrada) | (1) leído en esta sesión, sin abrir el paquete |

**Lo que NO se abrió:** ningún ZIP de `data/raw` (ENIGH, ENASEM ni ninguna otra fuente), ningún diccionario de datos, ningún catálogo de claves de ingreso. Este documento **no verifica** el nombre exacto de la clave de `ingresos` para "jubilación o pensión de tipo contributivo" en ENIGH — lo declara como hueco (§3) y ordena a quien ejecute que lo derive y lo reporte, en vez de teclear un identificador esperado (misma regla que `p3-lca-preregistro-v1_0.md` §5.1 aplica a las variables de diseño de ENIGH).

---

## 2 · Definición de tratamiento por regla, no por recepción declarada

**Por qué esto es un diseño distinto y no una repetición de la corrida ya hecha.** La corrida de `2026-08-04-hitoD-r5-1-pension-bienestar.md` define "beneficiario" por **recepción observada**: hogar con ≥1 registro en `ingresos` con la clave del programa (`P044`/`P104`) y `ing_tri > 0`. Esa definición depende de que la persona **haya solicitado y recibido** el apoyo — mezcla el efecto de la política con quién se acercó a cobrarla (cobertura entre 33% y 76% de los hogares con adulto mayor, según la propia nota, §2). Este documento define el tratamiento por el **cambio de regla**, no por quién cobró:

> **Grupo de tratamiento ("nuevo elegible por regla"):** personas de 65 años o más que, evaluadas contra la regla de elegibilidad vigente en el régimen 2014-2018 (`forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` §2), habrían sido **excluidas** de la población objetivo por recibir una pensión o jubilación de tipo contributivo **superior a $1,092 pesos mensuales** — y que, evaluadas contra la regla vigente desde 2019 (misma nota, §3-§4), **son elegibles** porque la prueba de ingreso por pensión contributiva ya no existe.
>
> **Grupo de comparación ("elegible en ambos regímenes"):** personas de 65 años o más cuyo ingreso por pensión o jubilación de tipo contributivo es **≤$1,092 pesos mensuales o nulo** — ya elegibles bajo la regla vieja, y elegibles bajo la regla nueva por la misma condición de edad. Su **estatus de elegibilidad no cambia** con la reforma; lo que cambia (si algo) es el resto del entorno de política, igual que para el grupo de tratamiento.

**Por qué esta definición es más fuerte, declarado antes de correr nada:** aísla el efecto del **cambio de regla de ingreso**, no el efecto de "cobrar o no cobrar". Una persona del grupo de tratamiento que nunca se acerca a cobrar la pensión universal **sigue contando como tratada** en este diseño (se volvió elegible por regla), mientras que en el diseño de recepción declarada contaría como "no beneficiaria". Si el patrón de "familia como seguro" responde a la **elegibilidad** (la certeza de que el Estado va a entrar) y no solo al **cobro efectivo**, este diseño lo puede ver y el de recepción declarada no.

⚠️ **Hueco declarado, no resuelto aquí — instrucción a quien ejecute:** este documento **no teclea** el nombre exacto de la(s) clave(s) de `ingresos` que identifican pensión/jubilación de tipo **contributivo** (IMSS, ISSSTE u otro sistema formal) en el catálogo de cada ola de ENIGH, porque no se abrió el paquete para verificarlo. La nota `2026-08-04-hitoD-r5-1-pension-bienestar.md` §8 valida un agregado llamado *"jubilación"* contra un boletín de INEGI (ENIGH 2022, cifra $5,168.6 vs. publicado $5,169) — **eso confirma que existe una variable o agregado de jubilación en el instrumento, no que sea la clave correcta ni que aísle "contributivo" de "no contributivo" al nivel de detalle que este diseño exige.** Quien ejecute: localiza la(s) clave(s) en `ingreso.csv`/`ingresos_cat.csv` de las olas 2018 y 2022, verifica que corresponda a régimen contributivo (no a la Pensión del Bienestar ni a otro programa no contributivo), y **reporta el hallazgo antes de aplicar el corte de $1,092** — si el instrumento no permite aislar "contributivo" de "no contributivo" con esa granularidad, **eso es un resultado** (empuja hacia la fila D de §6), no un motivo para aproximar con la variable más parecida.

---

## 3 · Grupo de comparación — elegibles en ambos regímenes, sin solape con el grupo de tratamiento

Los dos grupos de §2 son, por construcción, **mutuamente excluyentes** dentro de la misma ola: una persona de 65+ tiene ingreso contributivo >$1,092/mes (tratamiento) o ≤$1,092/mes o nulo (comparación), nunca ambas. **No hay tercera categoría** en este corte — a diferencia del régimen 2019-2021, que si se usara como ola introduciría una tercera partición por edad (65-67 grandfathered vs. 68+, ver §4). Es exactamente la razón por la que §4 evita ese régimen como ola.

**Universo compartido, declarado antes:** personas de 65 años o más, en hogares con datos completos de ingreso por persona en `ingresos`. Se excluye —y se cuenta cuántas— a quien no tenga ninguna fila en `ingresos` (ni de pensión contributiva ni de ningún otro concepto), porque para esa persona el corte de §2 no es aplicable, no es cero por definición.

---

## 4 · Olas pre y post — con la justificación de la fecha de corte, no la ola más cercana al choque

> **Pre: ENIGH 2018. Post: ENIGH 2022.** Se rechaza explícitamente ENIGH 2020 como ola post, con la razón escrita antes de tocar el dato.

**Por qué 2018, no una ola más temprana.** Es la última ola completa levantada íntegramente bajo el régimen 2014-2018 (`forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` §2): $1,092 y 65+ sin distinción indígena/no indígena, vigente hasta la reforma de feb/2019. Usar una ola más antigua (2016, 2014) no añade identificación —la regla no cambió entre 2014 y 2018— y aleja la comparación del choque sin necesidad.

**Por qué 2022, no 2020 — el argumento completo, porque es la decisión de diseño que hace a este documento distinto de simplemente repetir la ventana 2018→2020 de la corrida anterior.** ENIGH 2020 se levantó ago-nov 2020, **dentro** de la ventana de transición 2019-jul/2021: en esa ventana la elegibilidad por edad **no era uniforme** — 65+ solo para municipios catalogados como indígenas, 68+ para el resto, más una cláusula de transición para quienes tenían 65-67 años y ya estaban en el padrón activo a dic/2018 (`forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` §3, cita literal del acuerdo de feb/2019). Bajo ese régimen, **el universo "personas de 65+" de §3 no es homogéneo en elegibilidad**: dentro de él hay personas elegibles y personas no elegibles según municipio y padrón previo, y ENIGH no trae, hasta donde este documento verificó (no se abrió el paquete), un identificador de "municipio catalogado como indígena" ni del padrón activo de dic/2018 que permita separarlas. Usar 2020 mezclaría, dentro del propio universo de 65-67 años, personas del grupo de comparación que en realidad no eran elegibles todavía — **contaminaría exactamente el grupo que este diseño existe para mantener limpio.**

ENIGH 2022 se levantó ago-nov 2022, más de un año después del acuerdo del 7/jul/2021 que unificó la edad a 65+ para todas las personas sin distinción (`forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` §4). En 2022 el universo "personas de 65+" vuelve a ser homogéneo en elegibilidad por edad, igual que en 2018 — la única diferencia de regla entre las dos olas es exactamente la que este diseño quiere aislar: la prueba de pensión contributiva. **Esto es un diseño en dos cortes limpios, no el más cercano al choque**, y se declara la renuncia a 2020 explícitamente para que no se lea como omisión.

**No es panel.** ENIGH es transversal repetida — 2018 y 2022 son muestras independientes, no las mismas personas. El diseño es diferencias-en-diferencias por *grupo definido por regla*, no seguimiento longitudinal del mismo individuo. Se declara la misma reserva que la ficha original ya trae en su fila **C** (línea 149): un panel de la misma cohorte sería una prueba más fuerte todavía, y este documento no lo es.

---

## 5 · Los dos desenlaces — registrados por separado, sin combinarlos en un índice

Se adoptan las mismas dos operacionalizaciones que `2026-08-04-hitoD-r5-1-pension-bienestar.md` §5 ya usó y validó por robustez (citadas, no re-derivadas — este documento no abrió ENIGH para confirmarlas de nuevo):

- **Corresidencia intergeneracional:** `concentradohogar.clase_hog ∈ {3 Ampliado, 4 Compuesto}`. La nota citada (§7) ya verificó que restringir a solo `clase_hog=3` no cambia el hallazgo en más de 1pp — se hereda esa robustez, no se re-verifica aquí.
- **Transferencia intrafamiliar hacia mayores:** persona de 65+ con `ingresos.clave = P040` ("Donativos en dinero provenientes de otros hogares") y `ing_tri > 0`. Mismo límite heredado y declarado, no resuelto: `P040` no distingue donante familiar de no familiar.

**Por qué se registran por separado y no como índice combinado:** el Umbral original (línea 143) ya las nombra como dos medidas distintas ("reducción... en corresidencia intergeneracional **o** en transferencias intrafamiliares"), y la corrida previa encontró que **se separan** — corresidencia sin brecha significativa, transferencia con brecha significativa y de signo positivo (§5 de la nota citada). Un índice combinado habría ocultado esa separación. Este documento la mantiene.

**Estimador:** diferencia-en-diferencias ponderada, conglomerado último (`tests/svystat.py`, reutilizado sin modificar, ya validado en el repo contra caso SRS sintético y contra el boletín de INEGI 420/23 — mismo estimador que la corrida previa, citado, no re-derivado). Se reporta la brecha tratamiento−comparación en 2018, la misma brecha en 2022, y la diferencia de las dos brechas (el DiD), con IC95%, para cada uno de los dos desenlaces por separado.

---

## 6 · Umbral de veredicto y escala A–D propias, con regla de precedencia

**Umbral, en la misma forma que el Umbral original (línea 143) pero traducido a diferencias-en-diferencias, porque este diseño no tiene una sola ola post con la que comparar transversalmente:**

> Reducción **<10 puntos porcentuales** en la brecha (grupo nuevo-elegible por regla **menos** grupo elegible en ambos regímenes) de corresidencia intergeneracional **o** de transferencia intrafamiliar hacia mayores, **entre la ola 2018 y la ola 2022** — es decir, el DiD estimado es menor a 10pp en valor absoluto en la dirección que predeciría sustitución (el grupo nuevo-elegible converge hacia el grupo siempre-elegible, o lo cruza).

**Escala — cuatro filas, mutuamente excluyentes, con precedencia explícita para no repetir el solapamiento de `D5`/`D6` (P3, `forense/notas/2026-08-04-p3-lca-segmentacion.md` §6) y `A`/`D` (`R7.2`, Notas 11-13 de `hitoD-preregistro-v2_0.md`):**

- **A** — DiD <10pp (o de signo contrario al predicho por sustitución) en al menos uno de los dos desenlaces, con monto de la Pensión del Bienestar documentado como suficiente (mismo criterio que la corrida previa, §6 de esa nota: monto / gasto per cápita del hogar tratado en la ola post) **y** la clave de pensión contributiva de §2 identificada con éxito por el ejecutor. **La regla se refuta a este nivel de identificación también.**
- **B** — DiD entre 10 y 20pp, o monto insuficiente, o las dos medidas de §5 dan resultados en direcciones opuestas sin que ninguna alcance significancia clara. **Ambiguo — no refuta ni confirma.**
- **C** — el diseño exigiría, además de lo que ENIGH ya ofrece, seguimiento panel de la **misma persona** clasificada por regla en 2018 y observada de nuevo en 2022 (no cohorte transversal repetida) — prueba más fuerte que ninguna fuente en disco sostiene hoy para esta ventana exacta. Se archiva C si el resultado de A/B es débil y la mejora de diseño identificable es, específicamente, panel de persona.
- **D** — si el ejecutor no logra aislar la clave de pensión **contributiva** de §2 con granularidad suficiente para aplicar el corte de $1,092 (el hueco declarado en §2), o si el grupo de comparación o de tratamiento colapsa a un tamaño de muestra insuficiente para el diseño (umbral de tamaño mínimo: a fijar por el ejecutor con el mismo criterio de `E3` de `p3-lca-preregistro-v1_0.md` §3.5 — ninguna celda con <5% de la muestra relevante, umbral **ARBITRARIO**, declarado aquí y no después). **Se archiva D por diseño, no por hallazgo posterior.**

**Regla de precedencia:** se evalúan en el orden A → B → C → D. A exige que la identificación de §2 haya tenido éxito (si no, no se evalúa A: se va directo a D). B se evalúa solo si A no se satisface. C se invoca solo si, satisfecho o no A/B, la reserva dominante resulta ser específicamente la ausencia de panel — no un cajón de sastre para cualquier reserva. D tiene precedencia sobre las tres si el hueco de §2 no se resuelve, independientemente de qué mostrarían los números con una aproximación: **no se reporta un veredicto sobre una clave de pensión contributiva que el ejecutor no pudo verificar como tal.**

⚠️ **Nota de vigilancia (heredada de §0):** esta escala se escribió sabiendo ya que la corrida por recepción declarada dio fila A. Si el resultado de este diseño también da A, **no se puede leer como confirmación independiente sin más** — hay que preguntar primero si la escala se calibró (sin querer) para que A fuera fácil de alcanzar. Se deja constancia de que el umbral de 10pp y las bandas de B se copiaron del original **por consistencia con la ficha que este documento no enmienda**, no porque se hayan re-derivado para este diseño específicamente — es una limitación real, no retórica, y se declara aquí en vez de en un anexo.

---

## 7 · Fuente propuesta — ENIGH primaria, ENASEM secundaria y pendiente

**Fuente propuesta: ENIGH**, olas 2018 y 2022 (`enigh2018_nc_csv`, `enigh2022_nc_csv`, confirmadas en `data/manifiesto.yaml`, no abiertas por este documento). Estimador ya validado contra INEGI (Comunicado 420/23: total de hogares, dif. relativa 0.000%; tres medias de ingreso a ≤0.03% — `2026-08-04-hitoD-r5-1-pension-bienestar.md` §8). Es la fuente que ya está en disco, con estimador probado, y sostiene el diseño de dos cortes transversales de §4.

**Candidata secundaria, declarada pendiente, no resuelta aquí: ENASEM/MHAS** (panel real, olas 2018 y 2021, señalada por `forense/cruce-catalogo-fichas-v1_0.md` §3 como candidata para R5.1 precisamente porque es panel).

**Por qué el límite de 2018 de ENASEM, documentado por `2026-08-04-enasem-paso1-descriptor.md` §3, deja de ser un bloqueo bajo este diseño — y por qué eso NO significa que ENASEM ya esté lista:**

El límite documentado es que la variable de recepción de transferencia pública en la ronda 2018 de ENASEM (`K79A_1_1_18`) **no tiene categoría nombrada** para el programa de pensión a mayores — cae en "otra institución", indistinguible de cualquier otro programa no listado (cuatro categorías: PROAGRO, PROSPERA, INAPAM, otra institución). Ese límite bloquea un diseño **por recepción declarada** (no se puede identificar quién recibía el programa en 2018 con esa variable). **No bloquea un diseño por regla como el de este documento**, porque el tratamiento de §2 no depende de si ENASEM nombra el programa en 2018 — depende de si ENASEM mide, para 2018, el **monto de pensión o jubilación de tipo contributivo** de la persona, para aplicar el mismo corte de $1,092.

**Eso queda sin verificar, y se declara así, no se resuelve:** este documento **no confirmó** si el codebook de ENASEM 2018 trae una variable de monto de jubilación/pensión contributiva con precisión suficiente (mensual, en pesos, distinguible de otras transferencias) para aplicar el corte de §2. `2026-08-04-enasem-paso1-descriptor.md` no lo verifica —esa nota resuelve preguntas sobre la variable de **recepción de la pensión no contributiva**, no sobre el monto de pensión **contributiva** — y este documento tampoco abrió el codebook para comprobarlo (habría sido abrir una fuente de datos fuera del perímetro de este acto). **Queda como pendiente explícito para quien decida promover a ENASEM sobre ENIGH**, no como candidata lista.

---

## 8 · La pregunta para la mesa — planteada, no decidida aquí

> **¿Un veredicto producido por este diseño autónomo cuenta como veredicto de `R5.1` en el Hito D — reemplazando o coexistiendo con la fila que emergiera de la ficha original —, o es una corrida nueva, con su propio renglón y su propio identificador, que no toca el contador de `R5.1`?**

Este documento no la resuelve, a propósito: resolverla es una decisión de mesa sobre qué identifica una ficha del Hito D —la pregunta sustantiva (¿la familia sustituye al Estado?) o el diseño específico pre-registrado en su momento (comparación transversal beneficiario/no-beneficiario)—, y las dos lecturas tienen defensores razonables:

- **A favor de que cuente como R5.1:** el `PORQUE` y el falsador (línea 139-141) son sobre la pregunta sustantiva, no sobre una operacionalización particular; el propio Umbral original ya admite dos lecturas de diseño (transversal vs. panel, según discute `2026-08-04-hitoD-r5-1-pension-bienestar.md` §9 y la Nota 16 del pre-registro).
- **A favor de que sea corrida nueva:** el Umbral y la escala de este documento son literalmente distintos de los de la línea 143/149 —no una ejecución del mismo protocolo con otro dato, sino un protocolo nuevo— y el registro append-only de veredictos (`hitoD-preregistro-v2_0.md`, sección homónima) no tiene mecanismo declarado para que dos protocolos distintos escriban a la misma fila.

Ninguna de las dos lecturas se adopta aquí. **Se plantea para que la mesa la resuelva antes de que exista un resultado que la fuerce a resolverse bajo presión de un dato ya visto** — la misma razón por la que este documento es un pre-registro y no una nota de resultado.

---

## 9 · Enmiendas

**Ninguna a la fecha del sello.**

> **Regla de enmienda:** cualquier cambio a §2 (definición de tratamiento), §4 (olas), §5 (desenlaces) o §6 (umbral/escala) posterior a la fecha del sello **se anexa aquí como enmienda fechada, con el texto viejo visible y la razón del cambio** — nunca como edición silenciosa del cuerpo. **Una enmienda posterior al primer ajuste se marca POST-DATO** y todo veredicto que dependa de ella se reporta como **exploratorio**, no como pre-registrado — misma regla que `p3-lca-preregistro-v1_0.md` §10, citada, no reinventada.
>
> El cuerpo de este documento queda **sellado el 4 de agosto de 2026**, antes de que ninguna fuente de microdato fuera abierta por esta sesión.

---

## 10 · Lo que este documento no hace — perímetro explícito

No enmienda `hitoD-preregistro-v2_0.md:138-149`. No escribe en el Registro de veredictos archivados (append-only). No abre ENIGH, ENASEM ni ningún otro microdato. No resuelve el hueco de §2 (clave de pensión contributiva) ni el pendiente de §7 (monto en ENASEM 2018) — los declara y ordena derivarlos a quien ejecute. No decide la pregunta de §8. **Contadores movidos por este documento: cero** — es un pre-registro; no mide, no ajusta, no cierra hallazgos.

---

*Escrito por una sesión que no abrió microdato — con la contaminación distinta y declarada de §0 (haber leído el resultado de la corrida por recepción declarada). El mérito que reclama es más estrecho que el de un pre-registro sobre dato nunca visto, y se dice así en vez de disimularlo.*
