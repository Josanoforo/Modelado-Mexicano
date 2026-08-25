# Ficha B-bis de re-triage — `R7.2` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_2-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.2-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R7.2`: delito sin seguro → no denuncia, falsador de brecha de denuncia entre delitos asegurados y no asegurados |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R7.2` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

### 1 · ¿El hueco era de instrumento? — **SÍ, y es el caso más puro de los siete: hueco de diseño DENTRO de un instrumento presente.**

El `D` de `R7.2` no se archivó por ausencia de fuente ni por hueco de dato accidental. Se archivó
porque `BP2_1` ("Vehículo robado asegurado", `TMod_Vic`, ENVIPE 2025) **es la única variable de
cobertura de seguro que el instrumento formula, y la formula exclusivamente para `BPCOD=01`**
(robo total de vehículo) — verificado por diseño del cuestionario (Sección II, tras la cual
"TERMINE MÓDULO") y empíricamente contra el microdato (1 028 de 40 280 filas con `BP2_1` válido,
el 100 % de ellas `BPCOD=01`). La condición C de la propia ficha exige que la cobertura **varíe
entre clases de delito**; no varía — existe como concepto medido para 1 de las 15 (Nota 11,
`hitoD-preregistro-v2_0.md:689`; detalle en `hitoD-R7_2-veredicto-v1_0.md`).

La ficha previó exactamente este desenlace en su fila `D`: *"D si ENVIPE no cruza cobertura de
seguro con tipo de delito"*.

### 2 · ¿El instrumento estaba en disco? — **SÍ, y en cantidad: ~~44~~ 76 payloads ENVIPE, quince años.**

> **ENMIENDA fechada 2026-08-24 (`ACTO SELLA-AGO24-D`, `FP-85` → FIRMADA+ejecutada, mesa "corregirla. A." — respuesta 7).** La cifra
> original de esta ficha (`44`) es falsa: medido de nuevo hoy sobre
> `data/curacion-universo/ledger-inspecciones-barrido2.tsv` con el mismo `sha256`
> (`81b72932b406753a`) que cita la Entrada 3 de `registro-recalculo` — `grep -c envipe` sobre el
> archivo da **76** filas, no 44 (verificado también en `f3d3f95`, el SHA contra el que esta ficha
> corrió originalmente — mismo resultado). El texto original de abajo queda **intacto**, tachado, no
> borrado: es el registro de qué decía la ficha sellada. **No mueve el veredicto D de R7.2** (76 ≥
> 44 lo hace más cierto, no menos) — mismo criterio que `ACTO E3-TRIAGE` ya fijó al declarar T-3
> aunque el veredicto no se moviera. Ver `FP-85`, `forense/notas/2026-08-24-sella-d.md`.

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv`: **44 filas** con
`payload_id` de familia `envipe`, todas `PRESENTE-INTEGRO`, `estado_terminal=SI`. Años cubiertos,
derivados del propio `payload_id`: **2011-2025, quince ediciones consecutivas**, cada una con sus
`csv`, `cuest_principal_pdf`, `cuest_modulo_pdf` y `fd_pdf`.

Esto no es una novedad para el veredicto — Nota 13 (`hitoD-preregistro-v2_0.md:717`) ya había
corrido ocho olas ENVIPE 2018-2025 buscando el pareo por identificabilidad. Lo que es nuevo es que
hoy el disco está **medido y sellado**: gate material `672/672`, `ADR-103`, `PR #260`. La respuesta
"el instrumento estaba en disco" deja de ser una impresión y pasa a ser una fila de ledger.

### 3 · ¿Construye la condición del Umbral? — **NO, y ninguna cantidad de ediciones lo arregla.**

Aquí está el punto que este re-triage existe para dejar escrito: **el hueco de `R7.2` es
invariante al disco.** El instrumento está completo, en quince ediciones, íntegro. La condición
falta porque el cuestionario **no la pregunta** — `BP2_1` cuelga estructuralmente de `BPCOD=01`
por ruteo del propio formulario. Sumar olas multiplica filas de la misma pregunta; no crea la
pregunta que no está.

Es el contraejemplo que la Entrada 3 necesitaba para que su propio criterio no se lea mal: *"el
instrumento estaba en disco"* **no** implica *"el `D` era recuperable"*. Un `D` puede ser correcto
con el instrumento entero delante.

**Hallazgo adyacente, ya declarado y no adjudicado, que este re-triage no mueve:** dentro de
`BPCOD=01`, la denuncia por `BP2_1` da 79.1 % (n=402) asegurado vs. 67.2 % (n=614) no asegurado,
brecha de 11.9 pp en la dirección del "vuelco" (Nota 11). Nota 12 (`:703`) registró que esa cifra
satisface, leída literal, la fila `A` de la escala propia de la ficha, y que **la ficha no declara
precedencia entre ambas lecturas** — `forense/hitoD-R7_2-revision-v1_0.md` lo desarrolla. Eso es
una decisión de mesa sobre la redacción de la escala de `R7.2`, **no** una pregunta sobre el disco:
queda **fuera del perímetro de la Entrada 3**, y esta ficha no la resuelve ni la reabre.

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

`T-4` no aplica: el disco tiene el instrumento entero y la pregunta sigue sin existir. `T-1` no
aplica por lo mismo, al revés. `T-3` no aplica: la razón escrita en Nota 11 es exacta y se
reverifica sin cambio.

**Qué haría falta para reabrir `R7.2`:** que ENVIPE (o un instrumento equivalente) formule
cobertura de seguro **fuera** de `BPCOD=01` — es decir, un cambio de cuestionario, no de corpus.
Ninguna adquisición lo produce.
