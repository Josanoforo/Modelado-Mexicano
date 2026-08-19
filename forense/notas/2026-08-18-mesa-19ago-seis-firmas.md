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

**D-4 · worktree `curador`** → primero **espera ordenada**, verbatim: *"Espera. Regreso contigo, avanza en lo demás si puedes y cuando llegues a este punto espera, hasta que te de la instrucción."* El prompt se había formulado **dos veces**, con la evidencia de `ACTO W` enfrente y con la nota de perímetro (caja Ubuntu no libre). Luego llegó la instrucción, **por directiva y no por opción del widget** — ver §10, donde se registra verbatim, se verifica la nota que cita, y se corrige lo que este acto había afirmado mientras esperaba.

**D-5 · `U2/EV-1`** → **`Escribir gateado`**. **D-6 · `DOC-BACKFILL`** → **`Escribir gateado`**. Ambos a «`B2-SEMANTICO` fusionado», cada uno con su A.8 citado por ruta y línea. Ninguno se lanza aquí.

## 4 · Propagación — qué se movió, por respuesta

| Respuesta | Fila | Encargo escrito (ninguno lanzado) |
|---|---|---|
| D-1 | `FP-54` → **FIRMADA** (dos sub-respuestas verbatim + sha256 del benchmark) | `2026-08-19-FICHA-R51-D3.md` — VIVO, Ubuntu, gateado a caja libre. Vía al **14 de 27** |
| D-2 (c) | `FP-53` → **FIRMADA** | `2026-08-19-CORTE-EDAD-CONVENCION.md` (NUBE, sin gate, 9 sitios con procedencia citada) + `2026-08-19-CORTE-EDAD-EMPIRICO.md` (Ubuntu, gateado) |
| D-3 (a) | `FP-56` → **FIRMADA** | `2026-08-19-REFUTACIONES-SIN-OBJETO.md` (NUBE) — ejecuta la letra exacta: dar objeto, cero retiros; enmienda a `ADR-35` **redactada y no ejecutada**; denominador re-derivado, no anunciado |
| D-4 | `FP-55` → **FIRMADA** por directiva (`PROMPT-RESPONDIDA-POR-DIRECTIVA`, §10) | **ninguno** — `RESCATE-CURADOR` no se escribe: su premisa cayó |
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
| `FIRMADA` | 40 | **46** (+6) |
| `ABIERTA` | 12 | **6** (−6, tras la firma de `FP-55` por directiva) |
| `FIRMADA-CONDICIONAL` | 4 | **4** |

Las `ABIERTA` restantes ya no incluyen `FP-55`: la directiva de mesa la firmó (§10). El recuento de esta sección es el del cuerpo del acto, antes de fusionar `origin/main`; el definitivo, 57 filas, está en §9 y §10.

## 6 · Cascada y ADR

`ADR-110`, multi-inciso, seis incisos (a)-(f) con las respuestas verbatim. Conteo de ADR re-derivado **dos veces**: al escribir, contra `f3d3f95` → máximo **105**, sin huecos, candidato `106` (el encargo traía «máximo hoy: 104» — foto vencida por la fusión de `ADR-105`/`COND-ATRIB`); segunda derivación obligatoria al fusionar, con renumerado si otro carril tomó el `106`. Sitios de cascada: `gobernanza-v1_15.md:2` (105→106) y `estado-programa-v1_10.md:27,101` (105→106). ⚠️ `FP-48` respetado: `estado-programa` editado **cláusula por cláusula**, nunca por bloque, mientras `ESTADO-SPLIT` no fusione.

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

**1 · El número de ADR. La contingencia ocurrió.** `ACTO CONF-07-CIERRE` fusionó primero su propio **`ADR-106`** (sello de la partición de `modelo §3.7`, `conf.07` RESUELTA). Máximo re-derivado contra `cb0d98f`: **106**, sin huecos → este acto pasa a **`ADR-110`** y se reordena **después** del `106` ajeno, cuyo texto se preserva verbatim. Noveno ejercicio del mismo protocolo. Renumerado propagado a las seis encargos, al tablero, a `hallazgos.md` y a esta nota; el `ADR-106(d)` que cita la fila `FP-57` es el de `CONF-07-CIERRE` y **no se tocó**.

**2 · `FP-48` dejó de ser contingencia.** `ESTADO-SPLIT` fusionó y **partió `estado-programa:101` en 66 cláusulas, una por línea** — justo lo que la advertencia del encargo anticipaba. La cascada se rehízo **donde el split la dejó**: cláusula propia `- a 107 después, con ADR-110…` en la lista, no reinsertando el párrafo monolítico que ya no existe. Cabecera de la tabla (`:27`) y `L0` (`:101`): 106→**107**.

**3 · El tablero.** Conflicto real en `forense/firmas-pendientes.tsv`: `origin` abrió **`FP-57`** (`conf.08` / *"ni broker"* en `corpus/`) inmediatamente después de mi `FP-56`. Resuelto conservando **las dos**: mi `FP-56` firmada y la `FP-57` de origin intacta. Recuento tras la fusión: **57 filas** — `FIRMADA` 45 · `ABIERTA` 7 · `FIRMADA-CONDICIONAL` 4 · `CERRADA` 1 (esta última, de `LANE-A-E0-E5`).

**4 · Las cifras de la suite, recifradas dos veces en el mismo día por dos actos distintos.** `LANE-A-E0-E5` ya había recifrado 129→**128** WARN (y T03 44→**47**). Sobre esa base, las seis firmas de este acto bajan **−6 WARN de `T22`** → **122**. Corrida final tras resolver todo:

```
$ python3 tests/check.py --baseline
  19 FAIL · 122 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

`T15` (conteo de ADR) y `T16` (self-check de cifras) atraparon los tres desalineamientos intermedios —tabla en 106, y las dos declaraciones de WARN— y los tres se corrigieron cláusula por cláusula antes de commitear. **`tests/baseline.json` no se tocó; no se usó `--freeze`.**

## 10 · D-4, respondida por directiva — y la premisa del prompt, vencida

Respuesta de mesa, verbatim:

> Otro: el titular 590 está VENCIDO por ACTO Z (nota z-inventario-curador, 12/ago) — historia pre-purga, cero contenido único. La fila se corrige y cierra vía el acto RESCATE ya en curso con directiva de mesa; registra esta respuesta como PROMPT-RESPONDIDA-POR-DIRECTIVA citando la nota.

**La nota se verificó en el árbol; no se aceptó de palabra.** `forense/notas/2026-08-13-z-inventario-curador.md`, `ACTO Z`, siete puntos, todos por comando:

| # | Lo que `ACTO Z` corrió | Resultado |
|---|---|---|
| 1 | Contenido único del worktree | **NINGUNO** |
| 2 | `git merge-base origin/main HEAD` | `9301e59` (29/jul) — **misma firma pre-purga** que los seis refs `*-huerfana-20260813` |
| 3 | `HEAD` de curador | `3d5f34c` (7/ago) — misma ventana pre-purga |
| 4 | `git diff --diff-filter=A --name-only origin/main HEAD \| wc -l` | **0** archivos que `main` no tenga |
| 5 | `HEAD` corto y completo en `canon/remapeo-shas-purga-2026-08-10.tsv` | 1 vez cada uno, en 626 líneas |
| 6 | Firma completa | 590 sin empujar + `ancestor_of_origin_main=NO` = **pre-purga con 0 únicos**, «confirmada por comando, no por analogía con lo que ACTO W declaró candidato» |
| 7 | Rama de preservación | **no se empuja**: el worktree ya existe, conocido, en el clon base — «no hay riesgo de pérdida que una preservación resuelva, y no hay contenido que preservar» |

**Una discrepancia, dicha y sin efecto sobre el fondo:** la nota está fechada **13/ago**, no 12/ago como la citó la directiva. El fondo se sostiene íntegro.

**Corrección a lo que este mismo acto afirmó.** Mientras `D-4` estuvo en espera, esta nota, el `ADR`, `hallazgos.md` y los mensajes de mesa dijeron que *"el riesgo declarado el 13/ago sigue vivo y sin respaldo"*. **Era falso, y lo era ya al escribirlo.** `ACTO Z` retiró ese riesgo el **mismo 13/ago**, por comando, y refutó ese mismo día a `ACTO W` —la fuente que este acto citó, y que llamó al worktree «la pieza más grande del inventario sin adjudicar» con «tooling que no existe en ningún otro lugar del árbol»—. El defecto es de método y se nombra: **la evidencia de la fila se leyó en su nota de origen y no se buscó nota posterior que la refutara**; el titular vencido viajó cinco días, del 13 al 18, dentro de una fila del tablero. La columna `dónde` de `FP-55` queda corregida in situ, con los comandos de `ACTO Z` citados.

**Consecuencia operativa.** No hay contenido que rescatar ni riesgo de pérdida que un bundle resuelva: **`RESCATE-CURADOR` no se escribe** — era la propagación prevista para la vía (b) del prompt, y su premisa cayó. `FP-55` queda **FIRMADA** como `PROMPT-RESPONDIDA-POR-DIRECTIVA`; su **corrección y cierre formal ocurren en el `ACTO RESCATE` ya en curso**, por directiva de mesa, no en este acto.

**Tablero, re-contado por comando tras esta firma:** 57 filas — `FIRMADA` **46** · `ABIERTA` **6** · `FIRMADA-CONDICIONAL` 4 · `CERRADA` 1.

**Encargo `MESA-19AGO`: CONSUMIDO.** Las seis preguntas formuladas, las seis respondidas, las seis propagadas; los seis encargos escritos y ninguno lanzado. Contadores de medición sobre México: **0**.

## 11 · Cierre — el encargo, archivado y consumido

El encargo `MESA-19AGO` llegó **inline** de dirección y **no tenía archivo en el árbol**; se archiva bajo A.3 al cierre —`forense/encargos/2026-08-19-MESA-19AGO.md`— con su instrucción verbatim y una tabla de cumplimiento punto por punto, para que el acto sea auditable contra su propia orden y no contra el recuerdo de ella. Queda **`CONSUMIDO`**.

Tres cosas que la tabla de cumplimiento registra en vez de callar:

1. **El material de mesa que el encargo citaba —`DECISIONES-SEIS-FIRMAS-RH`— no existe en el árbol y no llegó a este acto.** `T03` lo atrapó al archivar el encargo, y por eso se nombra sin extensión. No hizo falta: la orden era preguntar, no releerlo.
2. **Dos premisas del encargo estaban vencidas al ejecutarse:** el máximo de ADR («104» → era 105 al escribir y 106 al fusionar) y el titular de 590 commits de `FP-55` (refutado desde el 13/ago por `ACTO Z`). Ambas re-derivadas, ninguna heredada.
3. **`RESCATE-CURADOR`, la propagación que el encargo preveía para la vía (b) de D-4, no se escribió** — la directiva de mesa retiró su premisa.

Corrida final del acto completo:

```
$ python3 tests/check.py --baseline
  19 FAIL · 122 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

## 12 · ADENDA 2 — segunda fusión: el número vuelve a moverse, y dos gates se abren

`origin/main` avanzó de `cb0d98f` a **`e563e5d`** (ocho PR: `#268` `B2-SEMANTICO`, `#269` `T20-LLAVES`, `#270` `CENSO-CMD`, `#271` `SELLO-FICHA-G3-V2`, `#272` `ESTADO-SPLIT` SS10, `#273` `E3-TRIAGE`, más sus merges). Fusionado en la rama —merge, nunca rebase— y resuelto a mano:

**1 · Tercer conteo de ADR, segundo renumerado. `107` → `110`.** `SELLO-FICHA-G3-V2` (`PR #271`) fusionó **otro** `ADR-107`, y `B2-SEMANTICO` (`PR #268`) renumeró su propio par a `108`/`109`. Máximo re-derivado contra `e563e5d`: **109**, sin huecos → este acto queda en **`ADR-110`**, reordenado tras el `109`. **Ningún texto ajeno se tocó**: el `ADR-107` de `SELLO-FICHA-G3-V2` y el `ADR-106` de `CONF-07-CIERRE` quedan donde estaban, y la fila `FP-11`, que cita ese `ADR-107` ajeno, no se modificó. Renumerado propagado a mis seis encargos, al tablero, a `hallazgos.md` y a esta nota — y **solo** a ellos.

**2 · Conflicto real en el tablero, resuelto a favor de `origin`.** `FP-14` y `FP-15` chocaron: mi lado traía el estado viejo (`FIRMADA-CONDICIONAL`, sin `ejecutada_en`), el de `origin` el nuevo — `ACTO E3-TRIAGE` cerró `FP-14` mientras este acto esperaba. **Gana `origin`**: es trabajo posterior y real, y este acto no tiene nada que decir sobre esas filas. Verificado después de resolver: contra `origin/main`, las **únicas** filas que este acto cambia son sus seis (`FP-32`, `FP-33`, `FP-53`, `FP-54`, `FP-55`, `FP-56`). El choque lo provocó el re-quoting de mi propia reescritura del TSV, no una edición de contenido — anotado para quien vuelva a editar el tablero con `csv`.

**3 · Las cifras, por tercera vez.** Base de `origin` tras `CENSO-CMD`: 124 WARN. Las seis firmas de este acto quitan **−6 de `T22`** → **118**. `T15` (conteo de ADR) quedó en `ok` tras el renumerado; `T16` atrapó las dos declaraciones desalineadas y se recifraron cláusula por cláusula.

```
$ python3 tests/check.py --baseline
  19 FAIL · 118 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

**4 · Consecuencia que este acto NO ejecuta pero debe dejar dicha: `B2-SEMANTICO` fusionó (`PR #268`), así que el gate de `U2-EV1` y `DOC-BACKFILL` —«`B2-SEMANTICO` fusionado»— está satisfecho.** Los dos encargos quedan **lanzables**, y siguen sin lanzarse: este acto escribe encargos, no los corre. Al abrirlos, sus propias instrucciones mandan — `U2-EV1` debe re-derivar su perímetro y verificar por comando si la fila ENASIC sigue obligatoria tras `BARRIDO-2`; `DOC-BACKFILL` debe re-derivar su población y decidir si los productos de `BARRIDO-2` ya lo absorben.
