# Nota del acto · MESA-19AGO — las seis firmas pendientes, prompteadas una por una y propagadas

**Acto de captura de decisiones.** No ejecuta ninguna de las seis: pregunta, registra verbatim, propaga a filas y encargos. **Contadores de medición sobre México: 0** — los movimientos viven en los encargos que este acto deja escritos, no aquí.

## 1 · ARRANQUE

| Paso | Resultado |
|---|---|
| Repo | `/home/user/Modelado-Mexicano`, clon no-superficial, `main` local actualizada a `origin/main` **antes** de cualquier `checkout` |
| SHA | El encargo se redactó contra `57984b5` (#262). **`origin/main` ya se había movido a `f3d3f95`** (#263, `COND-ATRIB`) al arrancar — todas las premisas se re-derivaron **por contenido**, no por número de línea, y todas se sostuvieron |
| `data/raw` | No se usa en este acto — repo-only |
| Entorno | Sesión NUBE (A.2). No se abrió microdato ni se lanzó ninguna corrida |
| Espejo | Toda cifra de abajo sale del clon, con su comando a la vista. **Ninguna tecleada de memoria**: 0/45, $4,034.74, 23.16%, 1,312/2,201, los 8 ids y los 590 commits se citan de sus fuentes |

## 2 · Verificación de existencia — las seis, derivadas por comando

```
$ awk -F'\t' '$1~/^FP-(54|53|56|55|32|33)$/{print $1"  "$6}' forense/firmas-pendientes.tsv
FP-32 ABIERTA · FP-33 ABIERTA · FP-53 ABIERTA · FP-54 ABIERTA · FP-55 ABIERTA · FP-56 ABIERTA
```

Las seis **ABIERTA** contra `f3d3f95`. Evidencia de cada una, verificada en su fuente antes de prompterla:

| Fila | Evidencia | Verificado |
|---|---|---|
| `FP-54` | `forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md` §1 (:59, indexación: 0 real, 23.16%, $4,034.74/trim, 45 personas) y §2.2 (:90, hogares mixtos: 1,312 / 2,201) | sí, leída |
| `FP-53` | 9 sitios `corte PENDIENTE` en `canon/modelo-decision-v4_0.md`, **dos redacciones** — receta de `CONSOLIDA-2`: `grep -niE "corte PENDIENTE\|Corte de .?edad.? PENDIENTE"` → **9/9** (`:189 :215 :219 :220 :355 :357 :361 :457 :482`). El patrón ancho `"corte"` da falsos por *"cortes iniciales"* (`FP-02`): no se usó | sí, corrido |
| `FP-56` | Bloque `decision_pendiente` en `milpa/refutations.yaml:60`. ⚠️ **El yaml no enumera los 8 ids** — solo nombra `ref.A.02`. La enumeración vive en `forense/corrida-refutaciones.md §3` (deuda de completitud ya señalada por `censo-integridad-v1_0.md` C4-05). Los 8 se pusieron a la vista en el prompt desde ahí | sí, leída |
| `FP-55` | `forense/notas/2026-08-13-w-limpieza-worktrees.md` §4/§5 — 590 commits sin empujar, `ancestor_of_origin_main=NO`, tooling real (`curador.py`, `supervisor.py`, tests, `multi1-staging/`, `multi2-staging/`) | sí, leída |
| `FP-32`/`FP-33` | Sus propias filas, con el texto de las cuatro preguntas ya inline (`REGISTRA-17AGO-II`, procedencia tipo 3). **Citado, no re-pedido** | sí |

## 3 · Los seis prompts y sus respuestas — verbatim

Cada uno con su evidencia enfrente, en el orden del encargo. `D-1` fueron dos preguntas.

**D-1a · umbral de indexación de `R5.1-D3`** → **`Deflactado (45)`**. Pesos constantes de 2018, umbral 2022 equivalente $4,034.74/trim, 23.16% de inflación acumulada, 45 personas reclasificadas. La vía nominal (0 indexación real encontrada) queda como sensibilidad declarada. *(La vía (c) del prompt original no se ofreció como opción viva: la propia nota la descarta — el programa no indexó el umbral en ningún momento de 2014-2018, así que no hay regla real que seguir. Se dijo así en el prompt.)*

**D-1b · doble conteo de hogar** → verbatim:

> Regla 1 como primaria: excluir mixtos solo del desenlace de corresidencia, con universo ACOTADO declarado (A-bis r4) y el marginal recalculado sobre ese universo. Sensibilidad obligatoria pre-declarada en COMMIT A: universo completo con "hogar T si tiene ≥1 persona 65+ en T" (precedente Duflo/Case-Deaton) — no la variante P032-máx, descartada por falta de precedente y signo perverso. Regla 3 descartada. Al acta va la advertencia Hamoudi-Thomas 2014: la exclusión condiciona en composición endógena y sesga hacia cero, por eso la sensibilidad no es opcional. Fuente: BENCHMARK-R51D3-hogares-mixtos — archívese en forense/ y cítese en el ADR.

La mesa entregó el benchmark durante el acto. Archivado como pidió la firma:

```
$ sha256sum forense/BENCHMARK-R51D3-hogares-mixtos-2026-08-18.md
380a035a526d013129f997779129bea8205deca38b2679c33e35f3b578a65d26
```

Clase **segunda-mano `SIN-FETCH`** por declaración del propio benchmark: todo hallazgo viene de abstracts/snippets de buscador; las URL son la receta de verificación. Este acto **no** las convierte en evidencia de primera mano.

**D-2 · corte de «edad joven»** → **`(c) Ambas`** — *"Convención declarada ahora para desbloquear los 9 sitios, más derivación empírica con dato mexicano propio como acto en cola que puede corregirla."* Corte propuesto en el prompt y adoptado: **15-29** (convención INEGI/ENOE de población joven en estadística laboral, el registro de `R2.4`); alterno declarable **12-29** (Ley del IMJ art. 2). **Aviso escrito en el propio prompt: ninguna de las dos fuentes está hoy citada en el árbol** — la procedencia se cita al propagar, no se hereda de aquí. Los dos encargos lo llevan escrito.

**D-3 · las ocho sin objeto** → **`(a) Añadir variables`**. Los 8 ids estuvieron a la vista en el prompt: `ref.A.02` (esfuerzo, **MUY_FUERTE**, única de las 49), `ref.A.04` (prestamista), `ref.A.14` (salud mental), `ref.A.20` (emprendimiento), `ref.A.28` (canal de compra), `ref.B.04` (colorismo), `ref.B.06` (religiosidad), `ref.A.17` (ítem actitudinal). ⚠️ **Deliberación registrada, no aplanada:** en la primera presentación la mesa marcó `(c) Partir`; pidió re-presentar el widget y en la segunda marcó `(a)`. **Rige la última.** Ambas quedan en el acta y en la fila.

**D-4 · worktree `curador`** → **en espera, por instrucción de mesa**, verbatim: *"Espera. Regreso contigo, avanza en lo demás si puedes y cuando llegues a este punto espera, hasta que te de la instrucción."* El prompt se formuló **dos veces**, con su evidencia enfrente y con la nota de perímetro (caja Ubuntu no libre → con (b) el bundle no corre en este acto). **No es `PROMPT-SIN-RESPUESTA`: es espera ordenada.** Consecuencia dicha sin suavizar: `FP-55` sigue `ABIERTA`, **no se escribió `RESCATE-CURADOR`**, **no se ejecutó bundle alguno**, y los 590 commits siguen sin respaldo — el riesgo declarado el 13/ago sigue vivo.

**D-5 · `U2/EV-1`** → **`Escribir gateado`**. **D-6 · `DOC-BACKFILL`** → **`Escribir gateado`**. Ambos a «`B2-SEMANTICO` fusionado», cada uno con su A.8 citado por ruta y línea. Ninguno se lanza aquí.

## 4 · Propagación — qué se movió, por respuesta

| Respuesta | Fila | Encargo escrito (ninguno lanzado) |
|---|---|---|
| D-1 | `FP-54` → **FIRMADA** (dos sub-respuestas verbatim + sha256 del benchmark) | `2026-08-19-FICHA-R51-D3.md` — VIVO, Ubuntu, gateado a caja libre. Vía al **14 de 27** |
| D-2 (c) | `FP-53` → **FIRMADA** | `2026-08-19-CORTE-EDAD-CONVENCION.md` (NUBE, sin gate, 9 sitios con procedencia citada) + `2026-08-19-CORTE-EDAD-EMPIRICO.md` (Ubuntu, gateado) |
| D-3 (a) | `FP-56` → **FIRMADA** | `2026-08-19-REFUTACIONES-SIN-OBJETO.md` (NUBE) — ejecuta la letra exacta: dar objeto, cero retiros; enmienda a `ADR-35` **redactada y no ejecutada**; denominador re-derivado, no anunciado |
| D-4 | `FP-55` → **sigue ABIERTA** | **ninguno** — espera de mesa |
| D-5 | `FP-32` → **FIRMADA** | `2026-08-19-U2-EV1.md`, GATEADO |
| D-6 | `FP-33` → **FIRMADA** | `2026-08-19-DOC-BACKFILL.md`, GATEADO |

## 5 · Tablero re-contado por comando

```
$ python3 -c "import csv,collections; r=list(csv.reader(open('forense/firmas-pendientes.tsv',newline=''),delimiter='\t')); \
  print(len(r)-1, collections.Counter(x[5] for x in r[1:]))"
```

| | contra `origin/main` (`f3d3f95`) | después de este acto |
|---|---|---|
| Filas totales | 56 | **56** (ninguna fila nueva — este acto firma, no abre) |
| `FIRMADA` | 40 | **45** (+5) |
| `ABIERTA` | 12 | **7** (−5) |
| `FIRMADA-CONDICIONAL` | 4 | **4** |

Las 7 `ABIERTA` restantes incluyen `FP-55`, en espera de mesa.

## 6 · Cascada y ADR

`ADR-107`, multi-inciso, seis incisos (a)-(f) con las respuestas verbatim. Conteo de ADR re-derivado **dos veces**: al escribir, contra `f3d3f95` → máximo **105**, sin huecos, candidato `106` (el encargo traía «máximo hoy: 104» — foto vencida por la fusión de `ADR-105`/`COND-ATRIB`); segunda derivación obligatoria al fusionar, con renumerado si otro carril tomó el `106`. Sitios de cascada: `gobernanza-v1_15.md:2` (105→106) y `estado-programa-v1_10.md:27,101` (105→106). ⚠️ `FP-48` respetado: `estado-programa` editado **cláusula por cláusula**, nunca por bloque, mientras `ESTADO-SPLIT` no fusione.

## 7 · Lo que este acto NO hizo

No diseñó la ficha `D3` · no tocó `milpa/refutations.yaml`, `canon/modelo-decision-v4_0.md` ni microdato · no ejecutó el rescate del worktree ni bundle alguno · **no lanzó nada de lo que dejó escrito** · no adjudicó `D-4` · no re-pidió el texto de las cuatro preguntas ni la especificación de `U2` (los citó por ruta y línea).

## 8 · Verificación final

```
$ python3 tests/check.py --baseline
  19 FAIL · 124 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

Contra `origin/main` la corrida daba **19 FAIL · 129 WARN**. La diferencia es **−5 WARN de `T22`**, y es exactamente lo que este acto hizo: cinco filas pasan de `ABIERTA` a `FIRMADA` con `ejecutada_en` poblado, así que dejan de señalarlas tanto la rama (a) —fila abierta— como la rama (c) —firmada sin ejecutar— de `T22`. `FP-55` sigue `ABIERTA` y sigue contando: la espera de mesa no la borra del vigía.

Paso intermedio, declarado porque ocurrió: al bajar el WARN a 124, `T16` (self-check de la suite) marcó **2 FAIL nuevos** — `estado-programa:129` y `:221` seguían declarando 129. Se recifraron **cláusula por cláusula** (`FP-48`, `ESTADO-SPLIT` sin fusionar), con la razón escrita en cada una, y la corrida volvió a **19 FAIL** y a **LÍNEA BASE: VERDE**. **`tests/baseline.json` no se tocó y no se usó `--freeze`** — el encargo lo prohíbe y no hizo falta: la mejora no baja la cifra congelada.

## 9 · ADENDA — la fusión, y la segunda derivación que este acto se comprometió a hacer

Mientras el acto esperaba la firma de `D-4`, `origin/main` avanzó de `f3d3f95` a **`cb0d98f`**: `PR #264` (`ESTADO-SPLIT`), `PR #265` (`CONF-07-CIERRE`), `PR #266` (`LANE-A-E0-E5`). `PR #267` quedó en conflicto (`mergeable_state: dirty`). Se fusionó `origin/main` en la rama —**merge, nunca rebase ni force-push**— y se resolvió a mano:

**1 · El número de ADR. La contingencia ocurrió.** `ACTO CONF-07-CIERRE` fusionó primero su propio **`ADR-106`** (sello de la partición de `modelo §3.7`, `conf.07` RESUELTA). Máximo re-derivado contra `cb0d98f`: **106**, sin huecos → este acto pasa a **`ADR-107`** y se reordena **después** del `106` ajeno, cuyo texto se preserva verbatim. Noveno ejercicio del mismo protocolo. Renumerado propagado a las seis encargos, al tablero, a `hallazgos.md` y a esta nota; el `ADR-106(d)` que cita la fila `FP-57` es el de `CONF-07-CIERRE` y **no se tocó**.

**2 · `FP-48` dejó de ser contingencia.** `ESTADO-SPLIT` fusionó y **partió `estado-programa:101` en 66 cláusulas, una por línea** — justo lo que la advertencia del encargo anticipaba. La cascada se rehízo **donde el split la dejó**: cláusula propia `- a 107 después, con ADR-107…` en la lista, no reinsertando el párrafo monolítico que ya no existe. Cabecera de la tabla (`:27`) y `L0` (`:101`): 106→**107**.

**3 · El tablero.** Conflicto real en `forense/firmas-pendientes.tsv`: `origin` abrió **`FP-57`** (`conf.08` / *"ni broker"* en `corpus/`) inmediatamente después de mi `FP-56`. Resuelto conservando **las dos**: mi `FP-56` firmada y la `FP-57` de origin intacta. Recuento tras la fusión: **57 filas** — `FIRMADA` 45 · `ABIERTA` 7 · `FIRMADA-CONDICIONAL` 4 · `CERRADA` 1 (esta última, de `LANE-A-E0-E5`).

**4 · Las cifras de la suite, recifradas dos veces en el mismo día por dos actos distintos.** `LANE-A-E0-E5` ya había recifrado 129→**128** WARN (y T03 44→**47**). Sobre esa base, las cinco firmas de este acto bajan **−5 WARN de `T22`** → **123**. Corrida final tras resolver todo:

```
$ python3 tests/check.py --baseline
  19 FAIL · 123 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

`T15` (conteo de ADR) y `T16` (self-check de cifras) atraparon los tres desalineamientos intermedios —tabla en 106, y las dos declaraciones de WARN en 128— y los tres se corrigieron cláusula por cláusula antes de commitear. **`tests/baseline.json` no se tocó; no se usó `--freeze`.**
