# Ficha B-bis de re-triage — `R4.1` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R4_1-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R4.1-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R4.1`: sin IMSS + padecimiento leve → farmacia con consultorio, falsador de la comparación antes/después de una mejora documentada de acceso público |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R4.1` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

### 1 · ¿El hueco era de instrumento? — **SÍ. Falta el diseño, no la variable.**

El `D` de `R4.1` se archivó porque **ninguna fuente del catálogo construye la comparación
antes/después que el Umbral exige** ("tras una mejora documentada de acceso público"): ENSANUT y
ENIGH son ambas corte transversal, sin panel ni evento fechado de apertura de clínica (Nota 20,
`hitoD-preregistro-v2_0.md:924`; Nota 23, `:962`; detalle en
`forense/notas/2026-08-04-z1-declaracion-fuente-r4-1-r9-1.md` y `-z4-`). El confusor de trato
quedó con un proxy débil (mención espontánea, no escala), declarado y no resuelto. Nota 20 lo dice
con precisión: **"ausencia de instrumento, no de variable con otro nombre — verificado contra los
dos cuestionarios completos, no contra sus catálogos"**.

`forense/notas/2026-08-04-aa-relectura-cuatro-d.md` §R4.1 releyó esa razón contra el catálogo
extendido y dejó **dos pistas abiertas**, explícitamente no adjudicadas, que la Entrada 3 es el
acto que puede contestar contra disco:

- **ESTAD/SESTAD** — transversal por establecimiento, sin panel; aporta proxy de trato, no el
  antes/después.
- **SINERHIAS por CLUES** — "en principio" podría fechar la ampliación/apertura de una unidad;
  **no verificado** si sus series retrospectivas son descargables por unidad.
- **Lectura ecológica alternativa** — corte transversal repetido de ENSANUT flanqueando el arranque
  de INSABI (enero 2020), con el precedente de `R5.1`/Nota 16 (que usó ENIGH repetida, no panel).

### 2 · ¿El instrumento estaba en disco? — **PARCIALMENTE, y el corte cae justo donde importa.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv` (672 filas):

| pieza que la relectura dejó abierta | ¿en el ledger de 672? | evidencia |
|---|---|---|
| **SESTAD reporte 2021** | **SÍ** — `conf17_r4_1_sestad_reporte_2021`, `R4_1_SESTAD_ESTAD/SESTAD_reporte_2021.pdf`, `PRESENTE-INTEGRO`, `E2`, 397 objetos, terminal `SI` | fila de ledger |
| **CLUES / SINERHIAS** (series retrospectivas por unidad) | **NO** — cero filas | `grep -i` sobre los 672 `payload_id`: la única coincidencia de la cadena es `datosgobmx_ckan_..._cero_resultados.json`, falso positivo léxico ("cero resultados"), no CLUES |
| **ENSANUT 2018, microdato** (pata "antes" de la lectura ecológica) | **NO** — la única pieza ENSANUT 2018 en disco es un **cuestionario en blanco**: `conf17_r9_1_ensanut_2018_cuestionario_utilizadores` (PDF) | filas de ledger, familia `ensanut` |
| **ENSANUT CONTINUA 2024, microdato** (pata "después") | **SÍ** — 23 payloads, cuestionarios + microdatos + catálogos | filas de ledger |
| **ENIGH** | **SÍ, seis olas**: 2012, 2014, 2016, 2018, 2020, 2022 (`enighAAAA_nc_csv`) | filas de ledger |

### 3 · ¿Construye la condición del Umbral? — **NO, y ahora por razones medidas, no por reserva.**

**La lectura literal del Umbral** (panel o evento local fechado de apertura de clínica): sigue sin
instrumento. SESTAD **está en disco y se leyó** — `CONF-17` corrida B
(`forense/notas/2026-08-05-conf17-fetch-corrida-B.md:419-445`) confirmó que el reporte agregado
2021 existe y se descargó completo, y lo clasificó **`EXISTE-NO-SATISFACE`**: es agregado, no
microdato por establecimiento; **sigue sin confirmarse si el microdato cuatrimestral por
establecimiento es descargable en bloque**. El catálogo CLUES, en la misma corrida, resultó
**`NO-ACCESIBLE`**: certificado autofirmado con valores de plantilla (inverificable) *y* `404` en
las dos URL aun bypaseando TLS; `gobi.salud.gob.mx` sin conexión; la búsqueda CKAN por "CLUES" no
encuentra el catálogo. Con CLUES inaccesible, **SINERHIAS-por-CLUES no es una pista viva**: su
llave de enlace no está.

**La lectura ecológica alternativa** (corte transversal repetido de ENSANUT antes/después de
INSABI): **cae por falta de la pata "antes", medido.** El disco tiene ENSANUT CONTINUA 2024
completa y **no tiene microdato de ENSANUT 2018** — solo el cuestionario en blanco de Utilizadores,
adquirido por `CONF-17` para otra ficha (`R9.1`). Un antes/después con una sola ola no es un
antes/después. La relectura del 4/ago pudo dejar esa lectura "no adjudicada" porque no había
medición de disco; hoy la hay, y el disco dice que no.

**Lo que este re-triage NO decide, y lo dice:** cuál de las dos lecturas del Umbral prevalece —
literal (panel/evento local) o ecológica (transversal repetida). `aa-relectura` la dejó
explícitamente a mesa, y la Entrada 3 no es el acto que fija la lectura de un Umbral: es el acto
que pregunta por el disco. Contra el disco medido, **ambas lecturas caen hoy**, así que la
ambigüedad no cambia la fila asignada. Si un acto futuro adquiere el microdato de ENSANUT 2018, la
lectura ecológica vuelve a estar viva y **entonces** la mesa tendrá que decidir — y esa
adquisición sería el disparador, no una relectura.

## Escala de re-triage — cuatro filas mutuamente excluyentes, con regla de precedencia estricta

Declarada íntegra en cada una de las siete fichas de este acto (no por referencia: la escala de la
ficha gobierna sobre cualquier legend genérico, y hay que decirlo en la ficha — Bloque B-bis,
`instrucciones-proyecto-v2_10.md:113`).

| fila | significa |
|---|---|
| `T-1 · D SOSTENIDO — sin instrumento en disco` | el hueco es de instrumento, y **ninguna** pieza candidata aparece en el ledger durable de las 672 representaciones inspeccionadas. El disco no tiene nada que decir. |
| `T-2 · D SOSTENIDO — instrumento en disco, no construye la condición` | la pieza candidata **sí** está en disco, `PRESENTE-INTEGRO`, grado `E2`, terminal `SI`, y su lectura directa ya archivada muestra que no construye la condición del Umbral. |
| `T-3 · D SOSTENIDO CON RAZÓN CORREGIDA` | el veredicto se sostiene, pero al menos una de las razones escritas en su Nota de archivo es **falsa** contra el instrumento real, medido. |
| `T-4 · D RE-ABRIBLE` | la pieza está en disco y su lectura directa **sí** construye la condición: el `D` deja de ser inejecutable y pasa a mesa. |

**Regla de precedencia, fijada al sellar y no después:** `T-4` manda sobre las tres. `T-3` manda
sobre `T-1` y `T-2` cuando ambas aplican — una razón falsa se declara aunque el veredicto no se
mueva, porque el archivo de un `D` es su razón, no solo su letra.

**Qué significa que el re-triage NO reabra** (obligación propia del Bloque B-bis: declarar el
desenlace de no-refutación antes de correr): que el `D` era correcto y **además** hoy es
correcto contra un disco medido, no contra un catálogo. Eso es un resultado, no un no-resultado:
sube el `D` de "no encontramos el instrumento" a "el instrumento está aquí, íntegro, y no
construye la condición". Es el desenlace más informativo de los cuatro para `T-2`, y el que
esta escala existe para poder anotar.

**Límite duro del criterio, declarado antes de aplicarlo.** "En disco" se decide contra
`data/curacion-universo/ledger-inspecciones-barrido2.tsv` — 672 filas, todas `PRESENTE-INTEGRO`
y `estado_terminal=SI`, gate material cerrado por `ACTO GATE-DURABLE-V7` (`ADR-103`, `PR #260`).
Ese ledger decide **a granularidad de representación/payload**, que es exactamente la
granularidad que la pregunta de la Entrada 3 pide ("¿estaba el *instrumento* en disco?"). No
decide a granularidad de variable: el índice E2 completo (1 331 710 registros, ~2.1 GB) vive solo
en `.barrido2/`, gitignorado, fuera de este entorno — y aun estando, conserva evidencia semántica
en el 4.09 % de sus registros (`forense/hallazgos.md:333`). Donde este acto necesita nivel de
variable, **cita una lectura directa ya archivada; no la rehace ni la sustituye por inferencia.**

---

## Fila asignada

**`T-2 · D SOSTENIDO — instrumento en disco, no construye la condición`.**

Se asigna `T-2` y no `T-1` porque la pieza decisiva de una de las tres pistas (SESTAD) **sí** está
en disco, íntegra e inspeccionada, y su lectura directa ya archivada la descarta — que es
exactamente el desenlace que `T-2` existe para anotar. Las otras dos pistas (CLUES/SINERHIAS,
ENSANUT 2018) están ausentes del disco, lo que por sí solo daría `T-1`; la precedencia no las
separa porque ninguna reabre. `T-4` no aplica: ninguna de las tres construye la condición.
`T-3` no aplica: la razón de Nota 23 se sostiene tal como está escrita.

**Qué haría falta para reabrir `R4.1`:** (a) microdato de ENSANUT 2018 en disco — habilitaría la
lectura ecológica y forzaría a mesa a decidir entre las dos lecturas del Umbral; o (b) series
retrospectivas de SINERHIAS por unidad, hoy bloqueadas porque el catálogo CLUES que las llavea no
es accesible. Ninguna de las dos es relectura: ambas son adquisición.
