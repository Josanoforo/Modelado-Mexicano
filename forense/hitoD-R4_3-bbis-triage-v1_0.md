# Ficha B-bis de re-triage — `R4.3` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R4_3-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R4.3-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R4.3`: desabasto → abandono (mitad A) / familia cuidadora → adherencia (mitad B), las dos mitades archivadas `D` por separado |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R4.3` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

> **Dos mitades, una ficha.** `R4.3` se archivó `D` en ambas mitades, "archivadas por separado"
> (Nota 24). Esta ficha B-bis las re-tría por separado y les asigna fila por separado; van juntas
> en un solo archivo porque comparten la fila `D` de la escala original de la ficha (línea 132 del
> pre-registro: *"si solo hay adherencia auto-reportada"*), que es lo que disparó ambas.

### 1 · ¿El hueco era de instrumento? — **SÍ en las dos mitades, y en las dos es hueco de variable inexistente en el catálogo entero.**

**Mitad A (desabasto → abandono).** Fuente declarada: ENSANUT CONTINUA 2024, secciones de
Diabetes/Hipertensión del Cuestionario de Adultos — única candidata con variable de motivo de
interrupción de tratamiento que distingue desabasto (`A0314`, códigos 05/06/10). El hueco: **la
única variable de adherencia disponible en el catálogo entero es `A0313`** (recuento de suspensión
por entrevista), **no adherencia por surtimiento**. Específico de mitad A: la duración del
desabasto tiene **techo abierto en "1 mes o más"**, no aísla el episodio ≥3 meses exacto (Notas 21
y 24, `hitoD-preregistro-v2_0.md:938` y `:970`; detalle en
`forense/notas/2026-08-04-z2-declaracion-fuente-r4-3.md` y `-z5-`).

**Mitad B (familia cuidadora → adherencia).** **No existe variable de cuidadora**; el único proxy
(corresidencia) es el mismo confusor socioeconómico que la propia ficha ya advierte (línea 130).
No se corrió ese proxy sin control, **por diseño, no por omisión**.

`forense/notas/2026-08-04-aa-relectura-cuatro-d.md` releyó ambas contra el catálogo extendido y
las dos veces concluyó **"la razón se sostiene"**, con una frase que este re-triage hace suya:
*"es el pre-registro funcionando, no un error de búsqueda"*.

### 2 · ¿El instrumento estaba en disco? — **El declarado sí; el que haría falta, no existe.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv` (672 filas):

| pieza | ¿en el ledger de 672? |
|---|---|
| **ENSANUT CONTINUA 2024** (fuente declarada de ambas mitades) | **SÍ** — 23 payloads: los cinco cuestionarios con etiquetas, microdatos `csv`/`stata` de cada muestra, catálogos `xlsx`/`csv`; todos `PRESENTE-INTEGRO`, terminal `SI` |
| **Registro de dispensación/surtimiento enlazable a persona** (lo que mitad A necesita) | **NO** — cero filas |
| **Registro administrativo de salud** (CLUES, SINERHIAS, SAEH, SINAVE) | **NO** — cero filas; la única coincidencia léxica de la cadena en los 672 `payload_id` es `datosgobmx_ckan_..._cero_resultados.json`, falso positivo |
| **Instrumento con variable de cuidadora** de adulto con padecimiento crónico (lo que mitad B necesita) | **NO** — cero filas. ENUT sí está en disco y con profundidad (**16 payloads**, olas 2002/2009/2014/2019/2024), pero mide **uso del tiempo en cuidados**, no cuidadora asignada a un paciente crónico identificado, y no enlaza con adherencia de ese paciente en una unidad común |

### 3 · ¿Construye la condición del Umbral? — **NO, y en las dos mitades el hueco es anterior al corpus.**

Éste es el caso donde la pregunta de la Entrada 3 se contesta **más limpio de los siete**: el
instrumento declarado está en disco, íntegro y sellado, y **el instrumento que haría falta no
existe en México**, hasta donde el barrido de la clase Registro administrativo pudo verificar — no
hay registro público de receta electrónica ni de surtimiento farmacéutico enlazable a persona
(`aa-relectura` §R4.3 mitad A). El disco de 672, medido, lo confirma por ausencia: ninguna
familia de payload construye dispensación por paciente ni cuidadora asignada.

**Lo que este re-triage NO hace, declarado.** No corre el proxy de corresidencia para la mitad B.
Nota 24 lo excluyó por diseño (es el confusor que la ficha misma advierte), y correrlo aquí sería
sustituir la pregunta de la Entrada 3 —¿estaba el instrumento en disco?— por una corrida nueva
que ningún gate autoriza. Tampoco toca `A0313`/`A0314`: el microdato de ENSANUT 2024 está en
disco pero no en este entorno, y el hueco no es de lectura, es de variable inexistente.

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

## Filas asignadas — una por mitad, como Nota 24 las archivó

**Mitad A → `T-1 · D SOSTENIDO — sin instrumento en disco`.**
**Mitad B → `T-1 · D SOSTENIDO — sin instrumento en disco`.**

En ambas, "sin instrumento en disco" se refiere al instrumento que **construiría la condición**
(registro de surtimiento; variable de cuidadora), no a la fuente declarada — ENSANUT 2024 sí está
en disco y ya se sabía que no construye la condición: ése es el contenido del `D`, no una novedad.
`T-2` se consideró y se descartó por eso: `T-2` es para cuando la pieza candidata que **podría**
haber cambiado el veredicto resulta estar en disco y no servir; aquí no hay pieza candidata
alguna que el disco pudiera aportar. `T-4` no aplica. `T-3` no aplica: ninguna razón de Nota 24
resultó falsa — se reverifican las dos, y `aa-relectura` ya las había sostenido contra el catálogo
extendido.

**Qué haría falta para reabrir `R4.3`:** mitad A, un registro de dispensación o receta electrónica
enlazable a persona (no existe públicamente en México hoy); mitad B, un instrumento con variable
de cuidadora identificada de un paciente crónico. Ninguna de las dos es adquisición de algo que ya
esté publicado: son instrumentos que nadie levanta.
