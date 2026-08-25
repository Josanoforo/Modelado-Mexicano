# HITO D · `R10.1` — spec sucesora v2.0, PROPUESTA (no sellada)

### `hitoD-R10.1-spec-v2_0-propuesta` · **v2.0-PROPUESTA** · 25 de agosto de 2026 · ENTORNO NUBE

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R10_1-spec-v2_0-PROPUESTA.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R10.1-spec-v2_0-propuesta`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El texto operativo que `FP-108` (FIRMADA, 24/ago/2026, mesa "Si a las tres cosas", respuesta 10) autorizó a redactar aparte, con las cuatro piezas nombradas en la fila de tablero *"spec sucesora v2.0 de R10.1 — GO de mesa"*: codificación pragmática · segundo codificador · arista rama4→C · techo de `n` declarado. |
> | **QUÉ NO ES** | **CONTADOR: cero.** No corre nada. No recodifica ninguna transcripción. No adjudica `R10.1`. No toca `hitoD-R10_1-especificacion-v1_0.md` ni `hitoD-R10_1-veredicto-v1_0.md` ni `hitoD-R10_1-defecto-spec-v1_0.md` — los tres quedan intactos, que es lo que los hace prueba de qué se supo y cuándo (regla del bloque append-only, `ADR-40`). **PROPUESTA de mesa**: correrla y sellarla son actos posteriores (v2.1 corrida, v2.3 sello — numeración de dirección, no de este acto). |
> | **VERIFICAS ASÍ** | las cuatro piezas de `FP-108` aparecen cada una con su sección propia (§2–§5); la escala de falsación trae la fila `B-bis` completa con precedencia; el insumo declara veredicto `A.4` por corpus, sin adivinar disponibilidad. |

---

## 0 · Por qué existe este acto y qué hereda sin re-derivar

`hitoD-R10_1-defecto-spec-v1_0.md §4` ya especificó los cuatro requisitos del sucesor — *"no escrita en ese acto"*. `ACTO SELLA-AGO24-D` (24/ago/2026) selló `D-08` y abrió la fila de tablero *"spec sucesora v2.0 de R10.1 — GO de mesa"* con `ejecutada_en` vacío: **el GO de mesa ya existe; falta el texto operativo.** Este acto lo escribe. Se hereda sin volver a derivar:

- El defecto que motiva el sucesor (`hitoD-R10_1-defecto-spec-v1_0.md §1`): la lista cerrada de cabezas de negación de COMMIT B cuenta como directas excusas mitigadas que el marco del ancla codifica como indirectas, y empareja negaciones que no son la cabeza del rechazo (una de ellas en una interacción que ni siquiera termina en rechazo).
- El hueco de árbol (`§2` del mismo documento): la rama 4 (*"medido pero sin potencia"*) no tiene arista a la fila `C`.
- El techo de `n`: con seis transcripciones por brazo, el IC de la diferencia mide **±56.58 pp** bajo COMMIT B — ninguna recodificación imaginable lo cierra por debajo de 15 pp con ese mismo `n`.

Este acto no cuestiona ni repite esas tres derivaciones: las toma como dadas y construye la spec que las corrige hacia adelante.

---

## 1 · Ficha bajo prueba, sin cambio (`hitoD-preregistro-v2_0.md:279-287`, verbatim de `hitoD-R10_1-especificacion-v1_0.md §0`)

> **R10.1 · Rechazo → indirecto `[FUERTE]`**
> SI hay que emitir un rechazo ENTONCES se hace indirecto — PORQUE preservación de face + simpatía *(Félix-Brasdefer, muestra en México)*
>
> **Falsador — separa los dos drivers.** Si el driver es **face**, la indirección debe **variar con la asimetría de poder** (más hacia arriba, menos hacia abajo). Si es **simpatía** como rasgo, debe ser **constante**.
> **Umbral.** Diferencia en tasa de rechazo indirecto entre interlocutor superior e inferior **<15 puntos** → el driver no es face situado, y `simpatía` **(b)** quedaría sin sustituto **(a)**.

**Esta spec v2.0 no reescribe la ficha, el umbral de 15 pp, ni el `PORQUE` mixto.** Corrige el **instrumento de medición** (cómo se cuenta indirecto/directo) y el **árbol de decisión** (a dónde va el desenlace cuando se mide sin potencia). Ambos vivían en `hitoD-R10_1-especificacion-v1_0.md`, que es lo que este acto sucede, no la ficha del preregistro.

---

## 2 · Pieza 1 — esquema de codificación pragmática, no léxico

**Qué reemplaza.** La lista cerrada de cabezas de negación de COMMIT B (`no puedo` · `no voy a` · … 14 cadenas) por un esquema de **acto de habla**, tomado del propio marco de Félix-Brasdefer que ancla la ficha (el estudio del 64% de Tlaxcala), no inventado para este acto.

**2.1 · Unidad de análisis.** El **turno de rechazo**, no la cadena léxica. Cada turno se descompone en:
- **Acto nuclear (*head act*):** el segmento que realiza el rechazo en sí — lo que, si se quitara, dejaría la interacción sin rechazo cumplido.
- **Adjuntos:** los segmentos que rodean al acto nuclear sin realizarlo (razones, disculpas, atenuadores, marcadores de apertura/cierre).

**2.2 · Regla de clasificación, sobre el acto nuclear únicamente:**
- **Directo:** el acto nuclear contiene una negación performativa explícita y no mitigada (`no`, `no puedo`, `me niego` funcionando como la propia realización del rechazo, no incrustada en una excusa).
- **Indirecto — cuatro subtipos, tomados del marco del ancla, cada uno con su regla de disparo:**
  - **Excusa:** el acto nuclear se realiza dando una razón externa que hace el rechazo implícito (*"tengo otra cita"*).
  - **Aplazamiento:** el acto nuclear pospone la decisión sin negar (*"lo pienso y te digo"*).
  - **Alternativa:** el acto nuclear ofrece una opción distinta a cambio del rechazo (*"mejor el jueves"*).
  - **Evasión:** el acto nuclear no responde directamente a la petición/invitación/sugerencia (cambio de tema, respuesta tangencial).

**2.3 · Regla explícita para excusas mitigadas — el defecto 1.1 de `hitoD-R10_1-defecto-spec-v1_0.md`.** Un acto nuclear que combine una negación (`no puedo`, `no, no`) con una razón externa en la misma cláusula o adyacente (*"no, pues no, no me puedo quedar [porque tengo otra cita]"*) se codifica **indirecto por excusa**, no directo. La negación aislada solo cuenta como acto nuclear directo cuando **no** va acompañada de razón externa en el mismo turno de rechazo.

**2.4 · Regla para negaciones que no son la cabeza — el defecto 1.2.** Una cadena de negación (`no puedo`, `no voy`, …) que se refiera a un objeto **distinto** del acto que se está codificando (p. ej. una negación sobre otra decisión mencionada dentro del mismo turno) **no se cuenta**. El codificador debe identificar primero el objeto del rechazo (qué petición/invitación/sugerencia se está rechazando) y clasificar la cabeza que responde a **ese** objeto, no la primera cadena de negación que aparezca en el texto.

**2.5 · Regla para interacciones sin rechazo consumado — el mismo defecto, su otra cara.** Una transcripción donde el interlocutor termina aceptando, aplazando sin resolver hacia el rechazo, o cuya interacción no cierra con un acto de rechazo identificable (`Rechazo 10` es el caso ya documentado: la interacción cierra con *"si salgo antes, pues llego"* / *"te espero"*) se marca **`NO-RECHAZO`** y se **excluye del denominador** de la tasa directo/indirecto de ambos brazos. No se cuenta como directo, indirecto, ni se descarta en silencio: se reporta con su motivo, por brazo, junto a la tasa.

---

## 3 · Pieza 2 — segundo codificador independiente

**3.1 · Independencia.** El segundo codificador no debe haber leído `hitoD-R10_1-especificacion-v1_0.md`, `hitoD-R10_1-veredicto-v1_0.md` ni `hitoD-R10_1-defecto-spec-v1_0.md` antes de codificar. Recibe únicamente: las 12 transcripciones íntegras (`forense/notas/2026-08-20-r10-1-rechazo-poder-salida.txt`), el esquema de §2 de este documento, y el código de poder (`+P`/`−P`) ya asignado por el corpus (no se le pide inferirlo).

**3.2 · Por qué es barato y no negociable.** Con 12 unidades, un segundo codificador completo cuesta una sesión. `hitoD-R10_1-defecto-spec-v1_0.md §3` ya declaró por qué un codificador único que vio el resultado bajo la regla equivocada no puede recodificar: conoce la hipótesis y sabe qué número queda mejor. El segundo codificador es la única vía que no repite ese defecto.

**3.3 · Acuerdo entre codificadores, reportado siempre.** Se calcula **Cohen's κ** sobre las 12 unidades, en dos niveles:
- **Nivel 1 (grueso):** directo vs. indirecto (colapsando los cuatro subtipos).
- **Nivel 2 (fino):** directo vs. {excusa, aplazamiento, alternativa, evasión, `NO-RECHAZO`}.

**3.4 · Umbral de aceptación y su regla de desempate.** `κ ≥ 0.60` (acuerdo sustancial, escala de Landis & Koch) en Nivel 1 habilita el conteo por consenso (discutir y resolver cada discrepancia con las dos codificaciones a la vista, sin tercer codificador). `κ < 0.60` en Nivel 1 **no habilita conteo**: el resultado se archiva como `D` de instrumento — *"el esquema no es aplicable con acuerdo suficiente a este corpus"* — y **no** se fuerza un consenso que sería, de nuevo, un solo criterio disfrazado de dos. El `κ` se reporta en ambos niveles aunque el Nivel 1 apruebe; el Nivel 2 es diagnóstico, no gate.

---

## 4 · Pieza 3 — arista explícita de "medido pero sin potencia" a la fila `C`

**4.1 · El árbol de `hitoD-R10_1-especificacion-v1_0.md §4.2`, con la arista que faltaba (marcada `NUEVO`):**

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Los dos brazos existen con denominador, y la diferencia es **<15 pp**, con IC95% que **no cruza** 15 pp | **`A`** |
| **2** | Los dos brazos existen con denominador, y la diferencia es **≥15 pp**, con IC95% que **no cruza** 15 pp por abajo | **`B`** |
| **3** | Al menos un brazo tiene **cero** rechazos mexicanos codificables, o falta el denominador | **`D`** |
| **4** | Los dos brazos existen pero el IC95% de la diferencia **cruza** 15 pp (el punto satisface `A` o `B` pero el intervalo no despeja) **→ NUEVO: si el ancla del falsador es población universitaria/elicitada (como en este corpus), la rama enruta a `C`, no solo a "no adjudica"** | **`C`** *(y se registra también como "no adjudica" bajo `A-bis`, que no se elimina — ver 4.2)* |
| **5** *(NUEVO)* | Los dos brazos existen, el IC95% cruza 15 pp, **y** el instrumento **no** es universitario/elicitado (población y diseño ya generalizables) | **"no adjudica"** puro, sin ruta a `C` — el hueco es de `n`, no de universo |

**4.2 · Por qué la rama 4 no reemplaza "no adjudica": lo complementa.** `hitoD-R10_1-veredicto-v1_0.md §3` ya usó correctamente "no adjudica" bajo `A-bis` para el desenlace de COMMIT B: eso describe **qué hace el número** (no decide). La fila `C` describe **qué haría falta** (replicación fuera de población universitaria). Son respuestas a preguntas distintas y ambas se registran cuando la rama 4 dispara: "no adjudica (`A-bis`); la vía declarada es `C`: replicación fuera de universitarios". Este es el precedente de `ADR-55`/`ADR-58` (fila `E`) aplicado un nivel más adentro, tal como `hitoD-R10_1-defecto-spec-v1_0.md §2` ya lo nombró — esta spec solo construye la arista que ese documento pidió, sin declarar una fila nueva de la escala del preregistro.

**4.3 · Precedencia, extendida de `hitoD-R10_1-especificacion-v1_0.md §4.3` (sin alterar 1–4, agregando 5):**
1. `A` y `B` mandan sobre `C` y `D` si las dos tasas se construyen y el IC no cruza el umbral.
2. `B` manda sobre `C` cuando el punto cruza 15 pp con IC que no cruza — la diferencia ya se estableció y su límite de generalización se nombra junto con ella.
3. `D` manda sobre `C` cuando un brazo está vacío.
4. **`C` manda sobre "no adjudica" puro cuando el IC cruza el umbral Y el instrumento es universitario/elicitado** — la condición exacta que produjo el veredicto de `hitoD-R10_1-veredicto-v1_0.md`.
5. Si el instrumento no es universitario/elicitado y el IC cruza, no hay `C` que proponer: es "no adjudica" desnudo, y la pieza 4 (techo de `n`) es la que se declara en su lugar.

---

## 5 · Pieza 4 — declaración de techo, escrita antes de correr

**5.1 · El techo, calculado, no estimado.** Con `n=6` por brazo (el único instrumento en disco, Brasdefer/México), el IC95% Wald de una diferencia de proporciones con las dos tasas en 50% mide **±56.58 pp** (medido en `hitoD-R10_1-veredicto-v1_0.md §2`). **Ninguna recodificación bajo el esquema de §2 de este documento puede, por sí sola, cerrar ese intervalo por debajo de 15 pp** — el ancho del IC es función de `n`, no de qué tan bien se clasifique cada turno. Un `n` mayor sube la potencia; una mejor codificación sube la validez de constructo. Son ejes distintos y esta spec no promete que corregir el segundo resuelva el primero.

**5.2 · Consecuencia operativa, declarada antes de correr.** Si la corrida de esta spec vuelve a caer en rama 4/5 con el mismo corpus de 12 transcripciones, **eso no es una falla de la spec v2.0**: es la confirmación de lo que este párrafo ya predijo. El objetivo de recodificar con este esquema es corregir la **validez** de la medición (defecto 1 del sucesor), no su **potencia** (defecto de `n`). Adjudicar `R10.1` — llevarla a `A` o `B` con un IC que no cruce 15 pp — exige **más rechazos mexicanos con los dos brazos de poder**, no una mejor codificación de los mismos 12.

**5.3 · Ruta declarada para conseguir más `n`, heredada sin re-derivar.** `hitoD-R10_1-defecto-spec-v1_0.md §4.4` ya nombró la candidata: **PRESEEA**, clasificada `NO-ACCESIBLE` por `CONF-17` desde el 5/ago/2026 y ausente de `data/manifiesto.yaml` (verificado de nuevo en `hitoD-R10_1-especificacion-v1_0.md §1.4`: `grep -ic preseea` → 0, control positivo `ENIF` → 95). Esta spec no reabre esa verificación — la hereda — y no promete que PRESEEA vaya a volverse accesible.

---

## 6 · Escala de falsación completa, con la fila de no-refutación `B-bis`

Se reproduce completa, no por referencia, para que esta spec sea auto-contenida al sellarse (regla del perímetro del preregistro, `hitoD-preregistro-v2_0.md:19`):

**Escala del preregistro:** **A** refutada · **B** sostenida no cerrada · **C** cerrada con búsqueda exhaustiva · **D** inejecutable (archivo como hueco de mundo, nunca como confirmación).

**Bloque B-bis — qué significa que el falsador NO refute, con precedencia explícita (adoptado literal de `hitoD-R10_1-especificacion-v1_0.md §5`, sin cambio):**

1. **`corroborada` — techo declarado: NO disponible con este instrumento, ni en el mejor caso.** Aunque los dos brazos existieran con diferencia enorme e IC estrecho, el corpus es role-play universitario. El resultado más fuerte alcanzable con Brasdefer/México es `acotada`, nunca `corroborada`.
2. **`acotada` — es la fila `B`.** Contenido si sale: *el driver `face` sobrevive la prueba en muestra estudiantil mexicana, y `simpatía` (b) sigue sin sustituto (a) fuera de esa muestra.*
3. **`falsador demasiado débil` — es la fila `D`, con precisión.** Si un brazo queda vacío tras excluir `NO-RECHAZO` (§2.5), no es que el falsador sea débil: no llega a existir. Un contraste de dos tasas con una sola tasa es un no-contraste.

**Precedencia del bloque B-bis:** `corroborada` está excluida por diseño para este instrumento (declarado en el punto 1, no se re-evalúa caso por caso); entre `acotada` y `falsador demasiado débil`, manda `falsador demasiado débil` (`D`) cuando aplica la condición de brazo vacío, sin importar qué tan clara sea la diferencia en el brazo restante — un solo brazo no produce `acotada`, produce ausencia de contraste.

**Universo pre-registrado, sin cambio respecto a v1.0:** los rechazos de habla mexicanos documentados en las tres páginas del corpus Brasdefer en disco (`adq15_brasdefer_actos_de_habla`, `adq15_brasdefer_convelic_conversaciones`, `adq15_brasdefer_encuentros_de_servicio`).

**Unidad:** el turno de rechazo mexicano codificable (ver §2.1), dentro del universo anterior, excluyendo las unidades marcadas `NO-RECHAZO` (§2.5) del denominador de la tasa directo/indirecto pero **incluyéndolas** en el reporte de cobertura del universo (cuántas transcripciones había, cuántas eran codificables como rechazo).

**Qué exactamente contaría como `C`:** una corrida de esta spec sobre un instrumento **distinto** de Brasdefer/México — con rechazos mexicanos elicitados o naturales fuera de población universitaria, con los dos brazos de poder y denominador — que produzca un IC95% que **no cruce** 15 pp, en cualquier dirección. Si el IC no cruza y el punto está por debajo de 15 pp → `A`. Si el IC no cruza y el punto está por encima → `B`. Si el IC cruza pese al `n` mayor → sigue sin adjudicar, y ahí sí sin ruta a `C` adicional (rama 5 de §4.1): sería la señal de que el propio umbral de 15 pp, no el `n`, es el problema — y eso es materia de un acto distinto, no de esta spec.

---

## 7 · Insumo que la corrida necesita — veredicto `A.4` por insumo, sin adivinar disponibilidad

Esta spec declara qué necesita para correr. **No adivina si eso existe fuera de lo ya verificado en disco** — cada insumo lleva su veredicto `A.4` (universo declarado, término de búsqueda, resultado).

| insumo | para qué pieza | veredicto `A.4` |
|---|---|---|
| **Las 12 transcripciones de `actos_de_habla.html`, bloque México, ya en disco** (`forense/notas/2026-08-20-r10-1-rechazo-poder-salida.txt`) | Piezas 1–3 (recodificación con el esquema nuevo, por dos codificadores) | **EXISTE — verificado.** Universo: las tres páginas Brasdefer, `COINCIDE` en `hitoD-R10_1-veredicto-v1_0.md`. No requiere adquisición nueva. |
| **Un segundo codificador humano, independiente, no expuesto al resultado previo** (Pieza 2) | Recodificación con acuerdo inter-codificador reportado | **NO ES UN INSUMO DE CORPUS — es de campo (personal).** Este acto **no verifica su disponibilidad**: asignar o reclutar a esa persona es decisión de dirección/mesa al abrir el acto de corrida (v2.1), no de esta spec. Se declara `POR-ASIGNAR`, no `EXISTE` ni `NO-ACCESIBLE` — no se adivina lo que dirección no ha resuelto. |
| **PRESEEA** (candidata para subir `n` más allá de las 12 unidades, §5.3) | Adjudicar `R10.1` de fondo (fuera del alcance de esta spec, que solo recodifica las 12 existentes) | **NO-ACCESIBLE**, heredado sin re-verificar de `CONF-17` y confirmado en `data/manifiesto.yaml` (`grep -ic preseea` → 0, control `ENIF` → 95, verificado en `hitoD-R10_1-especificacion-v1_0.md §1.4`, 20/ago/2026). Esta spec **no depende** de PRESEEA para correr — solo la nombra como la vía si mesa quiere resolver el techo de `n`, no la codificación. |
| **Entorno de cómputo para correr el recuento (Python, mismo patrón que `tests/hitod_r10_1_rechazo_poder.py`)** | Piezas 1, 3, 4 (conteo, κ, IC) | **EXISTE — verificado.** El script base ya está en el repo (`tests/hitod_r10_1_rechazo_poder.py`) y requiere solo la extensión del esquema de codificación (§2) y el cálculo de κ (§3.3); ambos son cómputo puro, sin insumo externo nuevo. Entorno declarado para la corrida: **UBUNTU** (como v1.0, no NUBE — coherente con `data/triaje-hitoD-2026-08-24.tsv:11`: *"NUBE (redactar spec v2.0) luego UBUNTU (recodificar con segundo codificador)"*). |

**Lo que este acto NO resuelve, y lo dice antes de que alguien lo asuma:** la disponibilidad de una persona para el segundo codificador es una decisión operativa de mesa/dirección, no un hecho verificable en un manifiesto o un corpus. Marcarlo `EXISTE` sin haber asignado a nadie sería la misma clase de error que `hitoD-R10_1-defecto-spec-v1_0.md` documentó en otro punto: reportar disponible lo que no se ha verificado.

---

## 8 · Qué NO hace este acto (cierre)

**CONTADOR: cero.** No corre la spec. No recodifica ninguna transcripción. No calcula ningún `κ`. No adjudica `R10.1` — sigue abierta, rama 4/`A-bis` de v1.0, sin fila. No edita `hitoD-R10_1-especificacion-v1_0.md`, `hitoD-R10_1-veredicto-v1_0.md` ni `hitoD-R10_1-defecto-spec-v1_0.md` (bloque append-only, `ADR-40`). No toca `hitoD-preregistro-v2_0.md` ni su tabla de defectos (`D-01`–`D-08`, línea 313) ni la fila de "GO de mesa" que ya vive ahí. No asigna a nadie como segundo codificador. No verifica de nuevo la disponibilidad de PRESEEA. Es **PROPUESTA**: sellarla (fijar esta versión como `v2.0` congelada) y correrla son actos posteriores que mesa autoriza aparte.

---

**el primer resultado que produzca la corrida de esta spec es el que se reporta — mismo principio que rige a su antecesora.**
