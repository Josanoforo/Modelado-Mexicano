# Ficha B-bis de re-triage — `R9.2` · v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R9_2-bbis-triage-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R9.2-bbis`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis propia que la **Entrada 3** de `registro-recalculo` exige para el veredicto `D` de `R9.2`: servicio disponible → la mayoría acepta — la meta-regla del corpus, falsador de cobertura baja Y abasto/campaña verificados por tercero |
> | **QUÉ NO ES** | **No adjudica, no emite y no retira ningún veredicto `RX.Y`.** El veredicto `D` de `R9.2` sigue archivado donde siempre, en el bloque append-only de `hitoD-preregistro` (ADR-40); esta ficha no lo toca ni reproduce su forma canónica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | trae la escala de re-triage completa (4 filas + precedencia), la pregunta de la Entrada 3 contestada con cita, y una sola fila asignada. |

**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
**Encargo:** `forense/encargos/2026-08-18-E3-TRIAGE.md` (`FP-14`, firmada-condicional `ADR-91`, `PR #246`).
**Criterio, verbatim de la Entrada 3** (`forense/registro-recalculo-v1_0.md` §1, fila 3): *"archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco"*.

---

## La pregunta de la Entrada 3, en dos partes

> **Cuidado adicional, heredado de la propia ficha.** `R9.2` es la meta-regla del corpus. Nota 25
> lo dice con todas sus letras: *"este `D` es ausencia determinable de instrumento auditor, no
> ausencia del fenómeno ni evidencia de que el hueco sea actitudinal — la meta-regla del corpus no
> cae por este veredicto"*. Este re-triage hereda esa cautela y no la relaja en ninguna dirección.

### 1 · ¿El hueco era de instrumento? — **SÍ, y de un instrumento AUDITOR, que es una categoría aparte.**

El Umbral exige una conjunción: **cobertura baja Y abasto/campaña verificados por fuente
independiente del prestador**. La segunda condición no tenía ninguna fuente en el catálogo
completo; la única disponible (**DGIS — Otros subsistemas**) es la propia Secretaría de Salud
reportándose a sí misma, **excluida por la ficha misma** (línea 271). La conjunción nunca puede
cruzar a `A` sin esa pieza, así que no se corrió la mitad de cobertura: no cambia el veredicto
(Notas 22 y 25, `hitoD-preregistro-v2_0.md:950` y `:978`; detalle en
`forense/notas/2026-08-04-z3-declaracion-fuente-r9-2.md` y `-z6-`). El anti-superviviente de
Bloque C se cumplió a nivel de instrumento: se buscó en las **119 fuentes** del catálogo, no solo
en ENSANUT.

### 2 · ¿El instrumento estaba en disco? — **NO. La única candidata seria no aparece en las 672.**

Medido contra `data/curacion-universo/ledger-inspecciones-barrido2.tsv` (672 filas):

| pieza | ¿en el ledger de 672? |
|---|---|
| **Cero Desabasto** (auditor independiente del prestador — la candidata que `aa-relectura` levantó) | **NO** — cero filas. La única coincidencia léxica de la cadena entre los 672 `payload_id` es `datosgobmx_ckan_enaproce_enestyc_cero`, cuyo `ruta_relativa` es `..._cero_resultados.json`: falso positivo, es la palabra "cero" de "cero resultados" |
| **DGIS / otros subsistemas del prestador** | **NO** — cero filas; y estaría excluida por la ficha aunque estuviera |
| **ENSANUT CONTINUA 2024** (mitad de cobertura, vía Cartilla mostrada) | **SÍ** — 23 payloads, `PRESENTE-INTEGRO`, terminal `SI`. Irrelevante para el desenlace: la conjunción cae por la otra mitad |

### 3 · ¿Construye la condición del Umbral? — **NO, y la razón escrita en el archivo ya estaba mal desde el 4/ago.**

**Lo que `aa-relectura` encontró y nadie propagó.** `forense/notas/2026-08-04-aa-relectura-cuatro-d.md`
§R9.2 —el mismo día en que Nota 25 archivó el `D`— dictaminó, verbatim:

> *"la razón declarada, tal como está escrita ('ninguna fuente en el catálogo completo... la única
> disponible es el propio prestador'), **NO se sostiene sin reserva**. Existe al menos una fuente
> independiente del prestador (**Cero Desabasto**) que el catálogo v1.0 no tenía clase para
> catalogar, y que cubre explícitamente vacunas dentro de su alcance de desabasto."*

El hueco no era "no existe auditor externo"; era **"el catálogo no tenía la clase
transparencia/sociedad civil, así que ningún auditor externo podía aparecer en él"** — que es un
defecto de instrumento de catalogación, no del universo de fuentes. Esa distinción es la que Nota
25 no registra y esta ficha sí.

**Por qué el `D` se sostiene igual, y con qué alcance exacto.** `aa-relectura` dejó dos piezas sin
verificar, y ninguna se ha verificado desde entonces:

1. **Granularidad ambigua** — no se confirmó si Cero Desabasto reporta a nivel de entidad, unidad
   médica o solo nacional agregado. Sin al menos entidad×año no enlaza ni ecológicamente con la
   cobertura individual/hogar de ENSANUT.
2. **"Alcance de campaña" ≠ "abasto"** — el Umbral pide **las dos**. Cero Desabasto documenta
   reportes de ausencia de producto; no se confirmó que documente fechas ni cobertura geográfica
   de campañas de vacunación como evento programático.

Y ahora hay un tercer hecho, que es el que este acto aporta y los anteriores no podían: **Cero
Desabasto no está en disco.** Cero de 672. La condición del Umbral no la construye ninguna pieza
del corpus medido, y la única candidata conocida no ha sido siquiera adquirida. La conjunción del
Umbral sigue sin cerrar — **por un motivo distinto al que Nota 25 declaró**, exactamente como
`aa-relectura` anticipó.

**Defecto de propagación, segunda aparición en este mismo acto.** Igual que en `R9.1`: una
relectura fechada el mismo día del archivo dictaminó que la razón no se sostenía como estaba
escrita, se guardó en `forense/notas/`, y la Nota del veredicto nunca la incorporó. Dos de siete
`D` llevaban dos semanas archivados con una razón que otro documento del mismo repositorio ya
había corregido. Ninguno de los dos veredictos cambia por ello — pero nadie lo sabía, porque nadie
lo había vuelto a leer.

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

Por la regla de precedencia: `T-1` también aplica de hecho (no hay instrumento auditor en disco),
pero `T-3` manda cuando una razón del archivo resultó falsa. `T-4` no aplica: la candidata no está
en disco y, aunque estuviera, sus dos piezas sin verificar (granularidad, alcance de campaña) le
impiden construir la condición completa.

**Y una advertencia que esta ficha está obligada a repetir, porque `R9.2` es la meta-regla.** Que
el `D` se sostenga **no** es evidencia de que el hueco sea actitudinal, ni de que el fenómeno no
exista. Es lo que Nota 25 ya declaró, y sigue siendo cierto con más razón ahora que sabemos que
hay un auditor externo real que nadie ha traído al corpus: el `D` de `R9.2` mide **nuestra
capacidad de auditar**, no la conducta de nadie.

**Qué haría falta para reabrir `R9.2`, y es concreto, barato y nombrable:** adquirir Cero
Desabasto y verificar sus dos piezas abiertas — (a) granularidad ≥ entidad×año, para enlazar
ecológicamente con la cobertura de ENSANUT; (b) si documenta alcance de campaña de vacunación como
evento programático, y no solo ausencia de producto. Si ambas responden que sí, la condición del
Umbral pasa a construible y `R9.2` deja de ser inejecutable. **Es la única de las siete fichas de
este acto con una ruta de reapertura identificada, nombrada y no ejercida** — y es adquisición
más verificación, no relectura, así que no cabe en el perímetro de la Entrada 3. Se deja escrita
aquí para que la mesa la vea; este acto no la promueve ni abre fila de firma por ella.
