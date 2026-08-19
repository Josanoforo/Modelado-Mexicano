# Ficha B-bis de re-triage — `R9.1` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R9_1-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R9.1-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R9.1`: experto accesible → defiere, falsador de acceso objetivo (distancia) contra deferencia al experto |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R9.1` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

### 1 · ¿El hueco era de instrumento? — **SÍ, y la Nota de archivo declara DOS razones independientes.**

Nota 20 (`hitoD-preregistro-v2_0.md:924`) y Nota 23 (`:962`), sobre ENSANUT CONTINUA 2024:

> *"Sin variable de distancia en km (solo tiempo de traslado) y con exclusión estructural, por
> diseño del cuestionario de Utilizadores, de quien no consultó a nadie."*

Desglosadas, tal como Nota 20 las escribió:

1. **No existe variable de distancia en km**, solo tiempo de traslado.
2. **El único cuestionario con acceso objetivo cuantitativo (Utilizadores) excluye por diseño a
   quien no buscó ninguna atención** — la subpoblación donde *"prevalece 'yo sé por experiencia'"*
   sería más visible; el Cuestionario Hogar cubre a todos pero su lista de motivos de no-atención
   es enteramente institucional, sin categoría de preferencia por conocimiento propio/allegado.

`forense/notas/2026-08-04-aa-relectura-cuatro-d.md` §R9.1 releyó ambas: la (1) "se sostiene con
reserva declarada" (CLUES podría dar geocodificación, pero faltaban dos piezas por confirmar);
la (2) **"se sostiene sin reserva"**.

### 2 · ¿El instrumento estaba en disco? — **SÍ, y en dos ediciones distintas.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv` (672 filas):

| pieza | ¿en el ledger de 672? |
|---|---|
| **ENSANUT CONTINUA 2024, Cuestionario de Utilizadores (PDF con etiquetas)** | **SÍ** — `5_vfinal_cuestionario_utilizadores_ensanut2024_etiquetas`, `PRESENTE-INTEGRO`, `E2`, terminal `SI` |
| **ENSANUT CONTINUA 2024, microdato de Utilizadores** (`csv`, `stata`, catálogo `xlsx`) | **SÍ** — tres payloads |
| **ENSANUT 2018, Cuestionario de Utilizadores (PDF)** | **SÍ** — `conf17_r9_1_ensanut_2018_cuestionario_utilizadores`, `R9_1_ENSANUT_utilizadores/ensanut_2018_utilizadores_servicios_salud.pdf`, `PRESENTE-INTEGRO`, `E2`, 177 objetos, terminal `SI` |
| **CLUES** (georreferenciación de establecimientos — llave de la razón 1) | **NO** — cero filas en los 672 |

### 3 · ¿Construye la condición del Umbral? — **NO. Pero una de las dos razones del archivo es falsa, medida.**

**Razón (1) — distancia en km: se sostiene, y su reserva se cierra en contra.** `aa-relectura`
dejó la razón (1) viva-con-reserva a condición de que un acto futuro confirmara (a) coordenadas
geocodificadas de CLUES y (b) la llave CLUES en el microdato público de ENSANUT. Ninguna de las
dos se confirmó, y hoy hay medición sobre la primera: `CONF-17` corrida B
(`forense/notas/2026-08-05-conf17-fetch-corrida-B.md:437-445`) encontró el catálogo CLUES
**`NO-ACCESIBLE`** — certificado autofirmado con valores de plantilla (inverificable) *y* `404` en
las dos URL aun bypaseando la verificación TLS; `gobi.salud.gob.mx` sin conexión; búsqueda CKAN
por "CLUES" sin resultado. Y CLUES **no aparece en ninguna de las 672 filas del ledger**. Sin
CLUES no hay geocodificación y no hay llave: la reserva no se cierra a favor, se cierra en contra.
La razón (1) sostiene el `D` por sí sola.

**Razón (2) — "exclusión estructural del que no consultó": NO SE SOSTIENE como está escrita.**
`CONF-17` corrida B abrió completo el PDF del Cuestionario de Utilizadores de ENSANUT **2018** y
leyó su Sección II (`:468-488`). El resultado, verbatim de esa nota:

> *"el título de la Ficha 14 dice 'Población que no consultó a nadie, **excluida** del Cuestionario
> de Utilizadores' — la lectura directa muestra lo contrario: la Sección II de este mismo
> cuestionario **está dirigida específicamente** a quien no buscó atención, preguntándole por qué.
> Esta población no está excluida del instrumento; es el objeto central de una de sus secciones."*

La pregunta `2.1 ¿Por qué no buscó atención?` trae 15 códigos exhaustivos (01-14 + 99). La
población que la razón (2) daba por estructuralmente ausente del instrumento **es el objeto de una
sección entera del instrumento**.

**Alcance exacto de la corrección, acotado y no sobregirado.** Lo medido es el cuestionario de
**2018**; la fuente declarada de `R9.1` (Nota 20) es ENSANUT CONTINUA **2024**. Este acto no puede
abrir el PDF de 2024 — corre en NUBE, repo-only: la fila de ledger prueba que el archivo está en
disco, íntegro e inspeccionado, pero el archivo mismo vive en `.barrido2/`/corpus fuera de git, y
el índice E2 durable en repo no conserva el texto de sus reactivos (defecto ya medido,
`forense/hallazgos.md:333`: evidencia semántica en 4.09 % de los registros, `categorias` en
0.00 % de lo tabular). Así que lo que queda escrito es lo que se puede sostener: **la razón (2)
está refutada para la edición 2018 del mismo instrumento y queda SIN VERIFICAR para 2024** —
no "confirmada para 2024", que es lo que Nota 23 afirma hoy sin haberlo leído por esa vía.

**El `D` no se mueve**, y por una razón sustantiva, no por conservadurismo: la lista de 15 códigos
de `2.1` es **enteramente institucional o genérica** — la más cercana a *"yo sé por experiencia"*
es `08 Decidió no atenderse` o el catch-all `14 Otro (especifica)`. Es exactamente lo que Nota 20
dice del Cuestionario Hogar. O sea: la subpoblación **sí** está en el instrumento, y la **variable
que el Umbral necesita sigue sin estar**. La conclusión sobrevive; el camino por el que se llegó a
ella, no del todo.

**Defecto de propagación, que es el hallazgo de esta ficha.** La medición que refuta la razón (2)
se hizo el **5/ago/2026**, un día después de que Nota 23 archivara el `D`, y quedó registrada en
`forense/hallazgos.md:151` — y **nunca llegó a la Nota**. Un veredicto puede quedar correcto
mientras una de sus razones lleva trece días refutada en el mismo repositorio, porque nadie
vuelve a leer las razones de un `D` una vez que su letra está archivada. La Entrada 3 es
precisamente el mecanismo que existe para releerlas, y lo encontró a la primera pasada.

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

**`T-3 · D SOSTENIDO CON RAZÓN CORREGIDA`.**

Por la regla de precedencia declarada arriba: `T-2` también aplica de hecho (el instrumento está
en disco y no construye la condición), pero `T-3` manda sobre `T-2` cuando ambas concurren —
*"una razón falsa se declara aunque el veredicto no se mueva, porque el archivo de un `D` es su
razón, no solo su letra"*. `T-4` no aplica: la variable de distancia sigue sin existir y CLUES
sigue inaccesible.

**Lo que se corrige y dónde vive la corrección.** El bloque de veredictos de `hitoD-preregistro`
es append-only y **no se edita**; Nota 23 tampoco. La corrección vive aquí, en la ficha B-bis que
la Entrada 3 manda escribir, que es el lugar previsto para ella.

**Qué haría falta para reabrir `R9.1`:** (a) una variable de distancia en km, o la llave CLUES en
el microdato público de ENSANUT **más** coordenadas geocodificadas de CLUES — hoy imposible, el
catálogo no es accesible ni está en disco; y (b) una categoría de motivo de no-atención que
distinga preferencia por conocimiento propio/allegado, que ninguna de las dos ediciones leídas
tiene. Pendiente barato y acotado, no ejecutable desde NUBE: **abrir el Cuestionario de
Utilizadores de ENSANUT 2024 (ya en disco, ya inspeccionado) y verificar si su Sección de
no-atención replica la estructura de 2018** — cierra el "SIN VERIFICAR" que esta ficha deja
declarado. Es una lectura de un PDF que ya está en el corpus; requiere Ubuntu, no adquisición.
