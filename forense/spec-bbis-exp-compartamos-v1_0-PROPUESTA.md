# `EXP-COMPARTAMOS-1` — spec B-bis, congelada antes de tocar el microdato

### `spec-bbis-exp-compartamos-v1_0-propuesta` · **v1.0-PROPUESTA** · 25 de agosto de 2026 · ENTORNO NUBE · `ADR-162`

> | | |
> |---|---|
> | **ARCHIVO** | `spec-bbis-exp-compartamos-v1_0-PROPUESTA.md` |
> | **NOMBRE ESTABLE** | **`spec-bbis-exp-compartamos-v1_0-propuesta`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El texto que `forense/registro-llaves-identificacion-v1_0.md` fila `EXP-COMPARTAMOS-1` (`:64`, §10) declara faltante para que esa llave pueda ejercerse: *"una spec B-bis, congelada antes de tocar el microdato, que declare qué θ o qué generador del modelo informa esta evidencia"*. Congelada **sin haber abierto un solo número** del paquete `116334-V1.zip` — la compuerta que define este acto. |
> | **QUÉ NO ES** | No ejerce la llave. No corre ningún diseño. No estima nada. No es el acto `EJERCE-LLAVE` (posterior, en UBUNTU, tras el sello de mesa). No toca `milpa/` — el conducto (`FP-144`, `EVIDENCIA_EXPERIMENTAL_TERCEROS`) ya existe y no se modifica aquí. **PROPUESTA de mesa**: sellarla es un acto posterior. |
> | **VERIFICAS ASÍ** | §1 cita la necesidad `FP-147`/`N34` verbatim y declara la disyuntiva de mapeo sin resolverla por invención; §2 fija ITT por conglomerado con EE agrupados, exactamente como los `.do` censados; §3 fija la escala del veredicto ANTES de haber visto el dato; §4 declara la escala B-bis completa con precedencia; §5 declara los límites. Cero cifras del espejo en todo el documento. |

---

## 0 · Insumos, lista cerrada — nada fuera de ella

`forense/registro-llaves-identificacion-v1_0.md` fila `EXP-COMPARTAMOS-1` (`:64`) y su §10 (`:252`) · `forense/notas/2026-08-25-eval-compartamos.md` · la fila `openicpsr — Compartamos AEJ` de `data/diseno-muestral.yaml` (cinco campos censados) · los `.do`/documentación ya citados ahí (código y documentación, no datos) · la necesidad `FP-147` (`data/curacion-registro/necesidad-objeto-modelo.tsv`, fila `N34`) · el molde de `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` (sellado, `FP-128`) · `canon/modelo-decision-v4_0.md` §2 y `milpa/procedencia.yaml` (la octava clase, `cita`+`llave_id` obligatorios, "no admite llave pendiente"). **No se abrió** `Compartamos_AEJ/Main/data/analysis_data_AEJ_pub.dta` ni ningún otro archivo del zip en este acto.

---

## 1 · Objetivo declarado — qué θ o qué generador informa esta evidencia

**La necesidad que ancla este objetivo es propia, no derivada de un generador existente.** `FP-147` (`FIRMADA`, mesa L8/`FP-132`, opción **b**: *no se reutiliza `confianza_institucional` ni `radio_confianza`, se abre necesidad propia*) abrió la fila `N34` de `data/curacion-registro/necesidad-objeto-modelo.tsv`, reclamando `EXP-COMPARTAMOS-1` para el objeto `dinero.credito.baja_friccion_usura_dano_downstream` (`canon/modelo-decision-v4_0.md:501`) — el segundo objeto de crédito del modelo, el que la terna del curador no cubría (hallazgo de `FP-132`). Ese es el objeto que este acto adopta, verbatim de `N34`, sin re-derivarlo.

**La disyuntiva, declarada y no resuelta por invención.** `dinero.credito.baja_friccion_usura_dano_downstream` **no es uno de los siete generadores de `canon/modelo-decision-v4_0.md` §2.1** (`G1a`–`G6`): es una regla del motor con tier propio (`[MEDIA]`, evidencia `(a)`, `ENSAFI`/`CNBV`), sin entrada hoy en `milpa/procedencia.yaml` y sin θ latente que la module — verificado (`grep -n "baja_friccion_usura_dano_downstream" milpa/procedencia.yaml` → 0 coincidencias). Al derivar el mapeo de `FP-147` contra §2.1 no aparece ningún generador que lo reclame sin ambigüedad: la evidencia no informa un θ del vector de generadores, informa el **valor `ASIGNADO` de una regla de motor independiente de `G1`–`G6`**. Eso es un hallazgo de este acto, no un defecto de redacción, y se lleva a mesa como disyuntiva:

- **(a)** la spec ejerce la llave para producir un número que **compite por el mismo sitio que el `[MEDIA](a)` hoy vigente** de `dinero.credito.baja_friccion_usura_dano_downstream` (sustituirlo exige acto propio de mesa — no lo hace esta spec, §3); o
- **(b)** la spec ejerce la llave para producir un número que entra a `milpa/procedencia.yaml` bajo la octava clase (`EVIDENCIA_EXPERIMENTAL_TERCEROS`, `cita`+`llave_id`) como **entrada nueva** de esa regla, hoy inexistente en el archivo, sin tocar el `[MEDIA](a)` de `modelo-decision`.

Este acto no elige entre (a) y (b) — mesa decide al sellar (§3 fija la mecánica común a ambas; la elección de destino es un acto de firma, no de redacción).

**Cláusula falsable del generador, citada verbatim de `modelo-decision` §2.1** (la que rige toda cláusula del modelo, aunque el objeto de esta spec no sea un generador de esa tabla): *"si la cláusula solo puede probarla la historia, no es una cláusula falsable — es una predicción histórica. Toda cláusula debe ser refutable al nivel donde la afirmación se usa."* La regla `dinero.credito.baja_friccion_usura_dano_downstream` ya trae su propio falsador pre-registrado en `modelo-decision:501` (IMOR de consumo del sector popular sostenido ~25-30% sin que el CAT pueda subir más) — **este acto no lo reemplaza ni lo re-escribe**; el falsador de esta spec B-bis (§4) es el de la llave `EXP-COMPARTAMOS-1`, una pieza adicional de evidencia sobre el mismo objeto, no una sustitución de ese falsador.

---

## 2 · Estimando

**ITT por conglomerado, EE agrupados por unidad de aleatorización — exactamente como el propio paquete.** `Treatment` (ola de seguimiento, 238 conglomerados, 120 tratados / 118 control, constante dentro de cada conglomerado) o `BTreatment` (línea base, 34 conglomerados, 17/17), según la ola que declare el diseño al ejercer; errores estándar agrupados por conglomerado (`vce(cl cluster)`, mismo mecanismo que las 60 regresiones de `Compartamos_AEJ/Main/Compartamos-AEJ-tables-2-8.do:9-79`). **No se estima cumplimiento (TOT/LATE)** — el paquete lo permite (`in_admin`) pero ITT es lo que la unidad de aleatorización identifica sin supuesto adicional de exclusión.

**Universo y ola, declarados por diseño, no por conveniencia.** Unidad de análisis: la persona (mujer, 18-60 años). Ola de seguimiento, N=16,560, es el universo primario — es la que trae `Treatment` constante por conglomerado y la que el propio paquete usa en sus 60 regresiones. La línea base (`BTreatment`, N=6,778) solo entra si el diseño concreto lo declara explícitamente como universo secundario, con su propio N y su propia justificación — nunca por default.

**Reservas nombradas, con las cifras del censo, no re-derivadas:**
- **`in_admin`** (toma de tratamiento por registro administrativo del banco): 12.37% (2,048/16,560), sin desglose por brazo en el censo — cualquier diseño que la use como covariable o para TOT declara ese hueco.
- **atrición**: 37.43% (1,090/2,912) sobre el universo buscado para seguimiento (`!mi(attrited)`), con tabla de atrición diferencial propia del paquete (`Appendix-Table-1.do:117`) — cualquier diseño declara si corrige por atrición diferencial o la deja como reserva sin corregir, y por qué.
- **Sin identificador de persona ni de hogar en el archivo público**: cierra por sí solo la vía de panel (§5) y obliga a que todo ejercicio de la llave sea transversal por conglomerado, nunca intra-persona.

---

## 3 · Escala del veredicto — fijada ANTES del dato

**En qué escala entra al canon.** El desenlace que informa `dinero.credito.baja_friccion_usura_dano_downstream` es un ITT sobre una variable de **adopción/toma de crédito grupal** (el paquete la mide en niveles: `in_admin`, `Q21_3_comp`) o sobre un desenlace de **daño downstream** que el diseño concreto identifique en el microdato (mora, cobranza — a verificar contra las 124 variables al ejercer, no supuesto aquí). La escala declarada, siguiendo `A-bis` regla 3: **puntos porcentuales (pp) de la variable de desenlace, ITT por conglomerado** — nunca en la escala de "techo de mora regulada 15-20%" de `dinero.credito.scoring_alternativo` (`modelo-decision:500`), que es de otro objeto y otro mecanismo; las dos no se cruzan sin enlace de escala declarado, y este acto no declara ninguno.

**Contra qué se lee.** La octava clase de `milpa/procedencia.yaml` (`EVIDENCIA_EXPERIMENTAL_TERCEROS`) exige `cita`+`llave_id` obligatorios y **no admite llave pendiente**: cualquier número que resulte de ejercer `EXP-COMPARTAMOS-1` cita esa llave en `llave_id` y la referencia bibliográfica del paquete en `cita`. **El número no sustituye ningún valor `ASIGNADO` existente sin acto propio de mesa** — hoy `dinero.credito.baja_friccion_usura_dano_downstream` no tiene fila en `milpa/procedencia.yaml` (§1), así que no hay valor que desplazar por default; si mesa elige la vía (a) de §1 (competir por el `[MEDIA](a)` de `modelo-decision`), eso es un acto de firma posterior y explícito, no un efecto automático de correr esta spec.

---

## 4 · Escala B-bis completa — declarada al sellar, no después

| fila | qué significa | condición |
|---|---|---|
| **corrobora** | El ITT del desenlace de adopción/daño downstream identificado va en la **misma dirección** que el mecanismo que `dinero.credito.baja_friccion_usura_dano_downstream` postula (baja fricción + tasa usuraria + reporte incompleto → daño), con IC95% que excluye cero en esa dirección | |
| **acota** | El ITT es significativo pero de magnitud menor a la que el `[MEDIA]` vigente asumiría, o el desenlace disponible en el microdato solo cubre adopción y no daño downstream (measurement parcial del mecanismo de tres condiciones) | |
| **rompe** | El IC95% del ITT del desenlace de daño downstream **cruza cero o va en dirección contraria** a la que el mecanismo postula, bajo un universo con potencia suficiente (N≫ el mínimo declarado para el desenlace concreto) | |
| **inejecutable** | El microdato no trae ninguna variable de daño downstream identificable (mora, cobranza) medible a nivel de conglomerado con potencia — solo adopción — y mesa no autoriza sustituir el mecanismo por el de adopción sola | |
| **no-refuta** (fila que el defecto `R5.1-D2` obliga a nombrar antes de correr) | El ITT no cae limpiamente en ninguna de las cuatro anteriores: p. ej., IC95% ancho que ni excluye cero ni lo cruza con margen, o desenlace parcialmente identificado. Se declara **ambiguo — no refuta ni confirma**, nunca se fuerza a `rompe` ni a `corrobora` por cercanía | |

**Precedencia si dos filas pueden dispararse a la vez:** `rompe → inejecutable → acota → corrobora → no-refuta`. Un desenlace que simultáneamente cruza cero (candidato a `rompe`) y solo mide adopción parcial (candidato a `inejecutable`) se archiva `rompe` — la falta de identificación de una condición del mecanismo no protege al mecanismo de un cero limpio en la condición que sí se pudo medir. `no-refuta` solo se alcanza si ninguna de las otras cuatro aplica, nunca por default cuando una corrida es simplemente ambigua en un solo eje.

---

## 5 · Qué NO informa esta evidencia

- **Transversal en seguimiento, no panel.** Solo 1,823 de 16,560 personas aparecen en las dos olas, y el archivo público no trae identificador de persona ni de hogar — nadie puede leer esto como panel intra-persona, ni siquiera con las 1,823 en común.
- **Un solo experimento, un solo estado.** Nogales, Sonora — no generaliza a otra geografía de colocación de crédito grupal sin declarar la vía de transporte, que esta spec no fija.
- **Un solo experimento, un solo producto de crédito.** Expansión de colocación de crédito grupal de Compartamos Banco — no informa nada sobre BNPL, tarjeta de alto CAT, ni ningún otro producto de `dinero.credito.*` distinto de este.
- **No informa la magnitud del `[MEDIA](a)` de `dinero.credito.scoring_alternativo`** (`modelo-decision:500`) — objeto distinto, mecanismo distinto (precio/mora, no acceso aleatorizado).
- **No adjudica que los reactivos de confianza del instrumento** (`Q15_2_mean_formal`, `Q15_2_mean_people`) sean el mismo constructo que `confianza_institucional`/`radio_confianza` del modelo — esa vía quedó cerrada por firma de mesa (`FP-132`, opción b) y esta spec no la reabre.
