# Nota de acto — `ACTO E3-TRIAGE`: la Entrada 3 de `registro-recalculo`, cerrada

*18 de agosto de 2026. Entorno **NUBE** (`cloud_default`, repo-only), sin acceso a microdato ni a
`.barrido2/`. Base: `origin/main = f3d3f95` (`PR #263`, `ACTO COND-ATRIB`), verificado por
`git fetch origin main` antes de arrancar — `HEAD` y `origin/main` idénticos al comenzar.
Encargo: `forense/encargos/2026-08-18-E3-TRIAGE.md`. Firma: `FP-14`, firmada-condicional
`ADR-91` / `PR #246` — texto adoptado verbatim: "E3-TRIAGE corre automáticamente al cierre de
BARRIDO-2, contra su índice E2".*

---

## §0 · Gate, verificado antes de escribir nada

| condición | estado | evidencia |
|---|---|---|
| Entradas 1 y 2 de `registro-recalculo` cerradas (gate propio de la Entrada 3) | **CUMPLIDO** | §1 del registro: Entrada 1 `RECALCULADO — CAMBIA` (`PR #198`), Entrada 2 `RECALCULADO — SIN CAMBIO` (`ACTO E2`) |
| `BARRIDO-2` cerrado materialmente (gate de `FP-14`/`ADR-91`) | **CUMPLIDO** | `GATE-DURABLE-V7`, `PR #255` + `PR #260`, `ADR-103`: gate material `ok:true` · **672/672** · 1 833 802 registros · 0 errores · `rc=0` |
| `FP-26` `DISPARADOR-A` permite arrancar sin semántica del barrido | **CUMPLIDO** | `ADR-101(h)`, enmienda in situ de la fila `FP-26` |

## §1 · Tarea 1 del encargo — ¿dónde vive el "índice E2"? Contestada, y con consecuencia

El encargo dejó esto `A VERIFICAR AL LANZAR`. Medido:

- **El índice E2 completo NO está en el repo.** 1 331 710 registros, ~2.1 GB, vive solo en
  `.barrido2/`, gitignorado por diseño (staging con material sin curar). En este entorno el
  directorio **no existe** (`ls -d .barrido2` → `No such file or directory`), como corresponde a
  un contenedor de nube que clonó el repo y nada más.
- **Lo durable SÍ está**, y es lo que este acto necesita:
  `data/curacion-universo/ledger-inspecciones-barrido2.tsv` — **672 filas**, una por
  representación inspeccionada, `sha256` del archivo `81b72932b406753a…`. Distribución verificada
  por comando: `estado_e0` = `PRESENTE-INTEGRO` en **672/672**; `estado_terminal` = `SI` en
  **672/672**. Más `reportes-inspeccion-barrido2-v1_0.tsv` (2 717 filas) y
  `prisma-material-barrido2.md`.
- **Decisión, y su justificación:** el acto corre en NUBE contra el ledger durable, **no** contra
  el índice E2 crudo, porque la pregunta que la Entrada 3 se hace es *"¿estaba el **instrumento**
  en disco?"* — granularidad de representación/payload, que es exactamente la que el ledger
  decide con precisión total. No se pidió Ubuntu.
- **Límite declarado, no escondido:** el ledger **no** decide a nivel de variable. Y el índice E2,
  aun estando, tampoco lo haría bien: conserva evidencia semántica en **4.09 %** de sus registros
  y `categorias` en **0.00 %** de lo tabular (`forense/hallazgos.md:333`). Donde este acto
  necesitó nivel de variable, **citó una lectura directa ya archivada** (`CONF-17` corridas A/B)
  en vez de inferirla. Las tres fichas donde eso ocurre lo declaran en su propio texto.

## §2 · Tarea 2 — los siete `D`, identificados por su código

Derivados de `canon/estado-programa-v1_10.md` §L5 (que enumera las 13 corridas archivadas) y
confirmados uno por uno contra sus Notas de archivo en `hitoD-preregistro-v2_0.md`:

| ficha | Nota de archivo | encargo que lo produjo |
|---|---|---|
| `R1.1` | Nota 5 (`:454`) | 29/jul, migrado desde `estado` |
| `R7.2` | Nota 11 (`:689`) | 4/ago |
| `R4.2` | Nota 17 (`:896`) | Encargo Y, `ADR-55` |
| `R4.1` | Notas 20 + 23 (`:924`, `:962`) | Encargo Z, `ADR-56` |
| `R9.1` | Notas 20 + 23 | Encargo Z, `ADR-56` |
| `R4.3` (mitades A y B) | Notas 21 + 24 (`:938`, `:970`) | Encargo Z, `ADR-56` |
| `R9.2` | Notas 22 + 25 (`:950`, `:978`) | Encargo Z, `ADR-56` |

Siete fichas, ocho veredictos (`R4.3` archiva sus dos mitades por separado). Ninguna otra fila del
bloque append-only trae `D`.

## §3 · Tarea 3 — la escala de re-triage, y la corrida

**La escala** (4 filas mutuamente excluyentes + regla de precedencia estricta, declarada al sellar
y no después, Bloque B-bis `instrucciones-proyecto-v2_10.md:113`) va **íntegra en cada una de las
siete fichas**, no por referencia: `T-1` sin instrumento en disco · `T-2` instrumento en disco que
no construye la condición · `T-3` `D` sostenido con razón corregida · `T-4` `D` re-abrible.
Precedencia: `T-4` > `T-3` > {`T-1`, `T-2`}.

**Resultado — 7 fichas, 8 veredictos, ninguno se mueve:**

| ficha | fila | por qué |
|---|---|---|
| `R1.1` | `T-2` | los 4 recursos AGROASEMEX **están en disco** (`conf17_r1_1_*`, íntegros, `E2`); leídos por `CONF-17` corrida B: ninguno llega a nivel productor, el eje temporal es fiscal y no ciclo agrícola, ninguna columna distingue voluntario de atado-a-crédito |
| `R7.2` | `T-2` | **44 payloads ENVIPE, 2011-2025**, íntegros. El hueco es de diseño del cuestionario: `BP2_1` cuelga por ruteo de `BPCOD=01`. Invariante al disco |
| `R4.2` | `T-2` | ENSANUT CONTINUA 2024 completa (23 payloads). No existe pregunta de permiso laboral ni de posposición repetible. Invariante al disco |
| `R4.1` | `T-2` | SESTAD 2021 **en disco** y ya leído (`EXISTE-NO-SATISFACE`, agregado); CLUES **no está** y es `NO-ACCESIBLE`; **falta el microdato de ENSANUT 2018**, así que la lectura ecológica que `aa-relectura` dejó viva cae por falta de la pata "antes" |
| `R9.1` | **`T-3`** | la razón (2) del archivo —"exclusión estructural del que no consultó"— **es falsa** contra el cuestionario real, medido el 5/ago y nunca propagado. La razón (1) (sin distancia en km) sostiene el `D` sola |
| `R4.3` A y B | `T-1` ×2 | el instrumento que construiría la condición (registro de surtimiento; variable de cuidadora) **no existe**: cero filas en los 672, y `aa-relectura` ya lo había verificado contra el catálogo extendido |
| `R9.2` | **`T-3`** | la razón del archivo —"ninguna fuente… la única disponible es el prestador"— **no se sostiene**: existe **Cero Desabasto**, auditor independiente. Pero no está en disco (0 de 672) y sus dos piezas (granularidad, alcance de campaña) siguen sin verificar |

**Conteo:** `T-1` = 2 veredictos (una ficha, dos mitades) · `T-2` = 4 · `T-3` = 2 · **`T-4` = 0**.

## §4 · Tarea 4 — la Entrada 3, cerrada

**Veredicto: `RECALCULADO — SIN CAMBIO`.** Los siete `D` se sostienen contra un disco medido. El
contador `13 de 27` **no se mueve** — y no podría moverlo este acto aunque quisiera: solo lo mueve
un veredicto archivado en el bloque append-only de `hitoD-preregistro`, nunca una edición ni una
ficha de re-triage. `0 de 15` (coeficientes), `10 de 15` (condicionales), `1 de 2` (llaves),
`22/550` (consumo trazable): ninguno se toca.

Por §2 del propio registro, `SIN CAMBIO` **no sella ADR nuevo** — precedente de las Entradas 0, 2
y 4. Este acto no sella ninguno.

**Universo declarado, en la misma línea de la fila** (regla del §1 del registro), transcrito aquí
completo: 672 filas de `data/curacion-universo/ledger-inspecciones-barrido2.tsv`
(`sha256` `81b72932b406753a…`, 672/672 `PRESENTE-INTEGRO`, 672/672 `estado_terminal=SI`, gate
material `ADR-103`/`PR #260`) × 2 717 filas de `reportes-inspeccion-barrido2-v1_0.tsv` × las
8 Notas de archivo de los 7 `D` (5, 11, 17, 20-25 de `hitoD-preregistro-v2_0.md`) ×
`forense/notas/2026-08-04-aa-relectura-cuatro-d.md` (relectura de 4 de los 7, ya existente, no
adjudicada) × `forense/notas/2026-08-05-conf17-fetch-corrida-A.md` y `forense/notas/2026-08-05-conf17-fetch-corrida-B.md` (lecturas
directas de AGROASEMEX, SESTAD/CLUES y ENSANUT 2018) × `forense/cruce-catalogo-fichas-v2_0.md`
(cruce por condición del Umbral, ~34 condiciones), @ `f3d3f95`.

## §5 · Los tres deltas del lanzador, contestados uno por uno

**(1) Gate.** Cumplido, verificado, §0 arriba.

**(2) El disco cambió — se re-tría contra el estado de hoy, no contra el del 13/ago.** Hecho: las
siete fichas miden contra el ledger de 672 sellado el 18/ago, no contra el catálogo del 4/ago.
Esto es lo que produjo los dos hallazgos de `T-3` y el cierre en contra de tres reservas
(AGROASEMEX, CLUES, ENSANUT 2018).

**(3) `FP-54` — no está firmada, y `R5.1` no entra aquí de todos modos.** Verificado contra
`origin/main = f3d3f95`: la fila `FP-54` de `forense/firmas-pendientes.tsv` está **`ABIERTA`**,
`firmada_en` vacío. No existe en el repo ningún acto ni encargo `MESA-19AGO` (el más reciente es
`2026-08-18-MESA-18AGO-nueve-firmas.md`). **`R5.1` queda `ESPERA-FP-54`, y se dice.** Nota
adicional que el lanzador no pedía pero que corresponde declarar: `R5.1` tiene veredicto **`A`**,
no `D` — **no está entre los siete del perímetro de la Entrada 3** bajo ninguna lectura, así que
su espera no bloquea el cierre de esta entrada. Lo que `FP-54` gatea es el diseño de `R5.1-D3`,
único acto capaz de mover el contador `13 de 27`; este acto no lo toca y no lo mueve.

**(4) Contador.** Se mueve solo por veredicto archivado, jamás por edición. Ninguna de las siete
fichas reproduce la forma canónica de veredicto, ninguna toca el bloque append-only, y `T18`
(que deriva el conteo de ese bloque) sigue verde.

## §6 · La cifra "~21 falsables de 27" — no se ratifica, y se explica por qué

El lanzador la cita como sugerencia de alcanzabilidad medida. Este acto **no la re-deriva ni la
ratifica**, por la misma razón que `forense/cruce-catalogo-fichas-v1_0.md:209` ya declaró:
*"esa cifra es aritmética sobre inferencias de cobertura, no un conteo de este documento"*. Lo que
sí hay medido es el cruce por condición de `cruce-catalogo-fichas-v2_0.md`: sobre **~34
condiciones** de las 27 fichas, **7 VIABLE · 6 VIABLE ECOLÓGICO · 5 NO ENLAZA · ~16 NO EXISTE**, y
ese documento **se niega explícitamente a colapsarlo a una cifra por ficha** porque su pregunta es
por condición. Este acto respeta esa negativa. Lo que mide en cambio es su propia pregunta, la de
la Entrada 3, y la contesta con las ocho filas de §3.

## §7 · Hallazgos del acto

1. **Dos de los siete `D` llevaban dos semanas archivados con una razón que otro documento del
   mismo repositorio ya había corregido** (`R9.1`, `R9.2`). En ambos casos la corrección se
   produjo el 4-5/ago —el mismo día o el siguiente al archivo— quedó guardada en `forense/notas/`
   y en `forense/hallazgos.md:151`, y **nunca llegó a la Nota del veredicto**. Ninguno de los dos
   veredictos cambia; lo que cambia es que ahora alguien lo sabe. El mecanismo que lo encontró es
   la propia Entrada 3, a la primera pasada — que es exactamente para lo que ADR-72 la abrió.
2. **La reserva de `cruce-catalogo-fichas-v2_0.md` sobre el padrón AGROASEMEX de `R1.1` estaba
   contestada desde el día siguiente a escribirse, y en contra.** El documento (4/ago) declaró
   "NO EXISTE, con reserva declarada — no se buscó"; `CONF-17` (5/ago) buscó, encontró, descargó
   los cuatro CSV y leyó sus encabezados: no llegan a nivel productor. Dos documentos correctos,
   ninguno de los dos equivocado, y trece días sin que nadie los pusiera uno al lado del otro.
3. **`T-4` = 0, y eso es un resultado, no un vacío.** La escala se escribió con una fila para
   "el `D` se reabre" y ninguna ficha aterrizó ahí. El desenlace de no-reapertura estaba declarado
   antes de correr (Bloque B-bis), así que se puede anotar: los siete `D` suben de "no
   encontramos el instrumento" a "el instrumento está aquí, íntegro y sellado, y no construye la
   condición" — para los cuatro `T-2`; y a "el instrumento no existe, verificado contra un disco
   medido" para el resto.
4. **La única ruta de reapertura nombrada del acto es `R9.2` vía Cero Desabasto**, y es
   adquisición + verificación de dos piezas (granularidad ≥ entidad×año; alcance de campaña como
   evento programático), no relectura. Queda escrita en su ficha, **no promovida**: este acto no
   abre fila de firma por ella ni la mete en ningún disparador.

## §8 · Perímetro respetado

**Escrito:** `forense/registro-recalculo-v1_0.md` (Entrada 3, solo la celda `estado` — que es la
única edición que el propio archivo permite en una fila existente) · 7 fichas B-bis nuevas en
`forense/` · `forense/firmas-pendientes.tsv` (`FP-14`) · `forense/hallazgos.md` · esta nota ·
`forense/encargos/2026-08-18-E3-TRIAGE.md` (cabecera `CONSUMIDO`).

**No escrito, como el encargo manda:** `canon/` — ningún archivo · `data/curacion-registro/**` ·
`milpa/` · `tests/` · el bloque append-only de `hitoD-preregistro-v2_0.md` · las Notas 5/11/17/20-25
(append-only, no se editan; las correcciones viven en las fichas B-bis) ·
`forense/cruce-catalogo-fichas-v2_0.md` y `forense/cruce-catalogo-fichas-v1_0.md` (append-only) ·
`forense/notas/2026-08-04-aa-relectura-cuatro-d.md`.

**ADR sellados: ninguno.** `SIN CAMBIO` no sella ADR (§2 del registro).
**Contadores de medición sobre México movidos: 0.** Declarado explícitamente, no por omisión.

## §9 · Gates, corridos

| gate | antes del acto | después | veredicto |
|---|---|---|---|
| `python3 tests/check.py --baseline` | **19 FAIL · 129 WARN, VERDE** (verificado en el árbol limpio antes de escribir nada) | **19 FAIL · 129 WARN, VERDE** | **sin entradas nuevas**, mismas cifras exactas |
| `python3 tests/test_svystat.py` (segundo gate de CI) | — | `exit 0` | sin cambio; este acto no toca `tests/` |
| `git diff --check` | — | limpio | — |

**Dos defectos propios, encontrados por los tests y corregidos antes de commitear, declarados y no
maquillados:**

1. **`T02` — colisión de nombre normalizado.** La nota de este acto se llamaba, en su primer borrador, igual que el encargo salvo por mayúsculas
   (encargo *E3-TRIAGE*, nota *e3-triage*), y los dos nombres colisionan al normalizarse.
   Renombrada al nombre que lleva hoy; las tres citas a la ruta vieja (en `registro-recalculo`,
   `hallazgos.md` y la cabecera del encargo) se actualizaron en el mismo commit.
2. **`T03` ×3 — citas abreviadas que no resuelven a archivo.** se habían escrito abreviaturas de continuación —el sufijo del archivo hermano tras nombrar el
   primero, en las citas a las dos corridas de CONF-17 y a las dos versiones de
   `cruce-catalogo-fichas`— en vez de la ruta completa. `T03` tiene razón: una abreviatura así no es citable por máquina. Las tres se
   expandieron a la ruta completa.

**No se corrió `--freeze` y no se tocó `tests/baseline.json`.** Tampoco hizo falta cascada a
`canon/estado-programa-v1_10.md:129`/`:221`: los dos `T16` que aparecieron en la primera corrida
eran consecuencia aritmética de mis propios `FAIL`/`WARN` nuevos, y desaparecieron al corregirlos
— las cifras vigentes que `estado-programa` declara siguen exactas, así que no había nada que
propagar. Es el desenlace correcto para un acto cuyo perímetro prohíbe escribir `canon/`.
