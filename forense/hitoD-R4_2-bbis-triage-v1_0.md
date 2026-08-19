# Ficha B-bis de re-triage — `R4.2` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R4_2-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R4.2-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R4.2`: hombre sin permiso laboral → pospone el chequeo, falsador del cruce permiso laboral × conducta preventiva |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R4.2` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

### 1 · ¿El hueco era de instrumento? — **SÍ. Dos preguntas que el cuestionario no formula.**

El `D` de `R4.2` se archivó tras chequeo barato completo contra el cuestionario Hogar y Adultos de
ENSANUT 2024 en etiquetas y los catálogos de `integrantes`/`adultos` (Nota 17,
`hitoD-preregistro-v2_0.md:896`; detalle en `forense/notas/2026-08-04-y4-veredicto-r4-2.md`):

1. **No existe pregunta sobre "sin permiso laboral para atender su salud"** — `grep -i "permiso"`
   sin ninguna coincidencia relacionada con trabajo en ningún cuestionario.
2. **No existe pregunta dedicada de posposición de chequeo** — `H0402=30` capta solo la última
   necesidad de salud en 3 meses, no un evento repetible.
3. La pieza más cercana, `H0405` motivo **"06 No tuvo tiempo"**, no distingue motivo laboral de
   ningún otro.

Verificado, sin solape con `A`/`B`/`C`: las tres exigen que el cruce exista en alguna forma
medible. La ficha pre-anticipó el caso en su fila `D`: *"si la encuesta no cruza permiso laboral
con conducta preventiva"*.

### 2 · ¿El instrumento estaba en disco? — **SÍ. ENSANUT CONTINUA 2024 completa: 23 payloads.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv`: **23 filas** de familia
`ensanut` correspondientes a ENSANUT CONTINUA 2024, todas `PRESENTE-INTEGRO`, `estado_terminal=SI`
— los cinco cuestionarios en PDF con etiquetas (Hogar, Niños 0-9, Adolescentes, Adultos,
Utilizadores), los microdatos en `csv` y `stata` de cada muestra, y sus catálogos `xlsx`/`csv`
(`hogar`, `integrantes`, `menores`, `adolescentes`, `adultos`, `utilizadores`, `NSE_Hogar`,
`NSE_Integrantes`). Una fila (`1_vfinal_cuestionario_hogar_..._ETIQUETAS`) trae la
`ruta_relativa` `[REDACTADO-PRIVACIDAD]` por el pipeline de cegamiento del barrido — su
`estado_e0` y su `estado_terminal` no están redactados y son `PRESENTE-INTEGRO`/`SI`.

**Es exactamente el instrumento contra el que se corrió el chequeo del 4/ago, y hoy está sellado
por el gate material `672/672`** (`ADR-103`, `PR #260`).

### 3 · ¿Construye la condición del Umbral? — **NO. Mismo caso que `R7.2`: hueco invariante al disco.**

El chequeo de Nota 17 se hizo contra los cuestionarios completos, no contra sus catálogos. Que el
corpus haya crecido y se haya sellado no añade una pregunta de permiso laboral a ENSANUT 2024, ni
convierte `H0405=06` ("No tuvo tiempo") en una variable de motivo laboral. **Ninguna pieza nueva
del ledger de 672 toca este hueco**: no hay en disco ninguna encuesta de salud con módulo de
condiciones laborales de acceso a atención — buscado por familia en el ledger completo, cero
coincidencias.

Detalle adicional que este re-triage confirma sin rehacer: el hueco es de **instrumento**, no de
variable con otro nombre. Nota 17 lo estableció por lectura del cuestionario; nada en el disco
medido lo contradice.

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

`T-4` no aplica: las dos preguntas no existen en el instrumento presente. `T-1` no aplica: el
instrumento sí está, completo y sellado. `T-3` no aplica: las tres razones de Nota 17 se
reverifican sin cambio.

**Qué haría falta para reabrir `R4.2`:** un instrumento que cruce permiso/flexibilidad laboral con
conducta preventiva en la misma unidad de observación. No está en el corpus de 672 ni en el
catálogo extendido; sería adquisición nueva, no relectura.
