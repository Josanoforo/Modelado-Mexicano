# Nota del acto · ESTADO-SPLIT — `estado-programa:101` deja de ser una sola línea

18/ago/2026 · `PR #264` · rama `claude/launcher-estado-split-wglzaf` · SHA de arranque `f3d3f95` (`origin/main`, merge `#263`, `ACTO COND-ATRIB`, `ADR-105`) · encargo `forense/encargos/2026-08-18-ESTADO-SPLIT.md`.

Acto **de forma, no de contenido**: no sella ADR, no mueve ningún contador de medición sobre México, no reclasifica nada. Cambia una sola cosa —cómo `git` ve la línea `:101`— y la cambia entera.

## §0 · Arranque, verificado por comando

```
git log -1 --format="%h %s"  → f3d3f95 Merge pull request #263 from Josanoforo/cond-atrib
git status                   → limpio, sin worktree residual
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → cloud_default  (NUBE, como el encargo asigna)
data/raw/                    → ausente — DECLARADO, no paro: este acto no usa microdato ni red
```

La sonda de red de A.2 se omite por la regla explícita del punto 4 del ARRANQUE (acto sin microdato ni red). Ninguna cifra de abajo sale de espejo: todas se derivaron del clon, con el comando a la vista.

## §1 · La compuerta del encargo, releída y corregida

El encargo declaraba la compuerta como «`GATE-DURABLE-V7` e `INTEGRATE-T23` fusionados (`PR #255`, `PR #256`)». **Esa lectura estaba mal en una mitad y se corrige aquí**: `PR #255` es `ACTO B2-V7`, no el `GATE`. El `GATE-DURABLE-V7` es **`PR #260`** (`6178bf9`, `ADR-100` en su rama, renumerado a `ADR-103` al fusionar). La compuerta real es, entonces, **`PR #260` + `PR #256`** — y hoy los dos están en `origin/main`:

```
git log --oneline --all | grep -E "#256|#260"
  → 6178bf9 Merge pull request #260 from Josanoforo/gate-durable-v7          (GATE-DURABLE-V7)
  → 93a4dd9 Merge pull request #256 from Josanoforo/claude/acto-t23-...      (INTEGRATE-T23)
  ambos ancestros de f3d3f95 (verificado: git merge-base --is-ancestor)
```

La confusión venía de la nota de `#257`, que citaba `#255` donde correspondía el `GATE`. **Compuerta CUMPLIDA de verdad**, no por lectura laxa: se cumple con la cita corregida, no a pesar de ella.

## §2 · La urgencia creció entre la redacción del encargo y su ejecución

`FP-48` se escribió (17/ago) sobre dos merges de `BARRIDO-2` en que el automerge se quedó con un lado entero **y salió bien por suerte** (`main` iba atrás). Entre esa redacción y hoy, la misma línea **mordió dos veces, de verdad**, y ambas quedaron escritas en el mensaje del propio merge:

```
git log --merges --oneline -- canon/estado-programa-v1_10.md
  a0be3d5  Merge origin/main (290f9a0) -- ADR-100 renumera a ADR-103,
           y FP-48 esta vez choco de verdad                          (merge de #260 al carril CONSOLIDA-2)
  8158ab4  Merge origin/main (PR #260, ACTO GATE-DURABLE-V7, ADR-103) --
           renumera ADR-103 provisional a ADR-104,
           FP-48 choca de verdad por segunda vez                     (merge al carril de #261)
```

Es decir: el riesgo que `FP-48` describía como hipotético («si el orden hubiera sido el inverso») dejó de ser hipotético dos veces en 24 horas. Las dos se citan aquí por eso, y en el `ADR` que las herede: no son color, son la razón de que este acto se ejecute hoy y no la semana que viene.

## §3 · Qué se hizo, exactamente

`canon/estado-programa-v1_10.md:101` era **un párrafo de 31 462 caracteres en una sola línea física** — toda la historia de la numeración de ADR desde el 29/jul (`32` → `105`). Pasa a:

- **1 línea de cabecera**: `**L0 · Gobierno — completo y al día.** 105 ADR, … *(Corregido 29/jul/2026: … `censo-integridad-v1_0.md` C1-02.`
- **66 ítems de lista**, uno por cláusula, del `Subió a 39…` al `a 105 después, con ``ADR-105``…`.

El corte se hizo **solo** en el separador `«; »` que precede a cada `a NNN después,` — el `;` queda al final del ítem anterior, ningún carácter se añade ni se quita salvo el prefijo `- ` de lista. El archivo pasa de 225 a 291 líneas de contenido; el resto del archivo no se toca.

**66 ítems para 67 estados del contador (39–105) no es un hueco nuevo:** el `42` nunca tuvo cláusula propia — el original dice *«a 43 después, con ADR-42/43, misma sesión»*, dos ADR sellados en un acto. Se conserva tal cual; partir esa cláusula en dos habría sido reescribir contenido, que es exactamente lo que este acto tiene prohibido.

## §4 · Verificación del contenido: por diff automatizado, no por lectura

El criterio del encargo (punto 3, mismo método que `ADR-98`) es que el texto plano reconstruido sea idéntico **carácter por carácter** al original, salvo el formato de lista. Regla de reconstrucción: *cabecera + `" "` + los 66 ítems sin su `- `, unidos por un espacio*.

```
original (git show f3d3f95:canon/estado-programa-v1_10.md, línea 101)
  longitud  31462
  sha256    3f1af7a083f1340d590792775ba35d8e1c7286211bb9a29505d85ad498c91954

reconstrucción desde la lista nueva (cabecera + 66 ítems)
  longitud  31462
  sha256    3f1af7a083f1340d590792775ba35d8e1c7286211bb9a29505d85ad498c91954

IDÉNTICO CARÁCTER POR CARÁCTER: True     (comparación de cadenas, no de resumen visual)
```

Control cláusula por cláusula, independiente del hash: los 66 ítems parsean todos contra `^(?:Subió )?a (\d+) `, la secuencia es **estrictamente creciente**, va de `39` a `105`, y el único número ausente del rango es el `42` ya explicado. Cero cláusulas duplicadas, cero perdidas.

## §5 · Control T15/T16, antes y después — obligatorio, y cumplido

El control se hizo en **dos niveles**, y se declaran los dos por separado porque dicen cosas distintas.

**Nivel 1 — el split solo** (commit 1, `canon/estado-programa` y nada más). La suite completa se corrió **antes** de tocar el archivo y **después**, y las dos salidas se compararon con `diff`:

```
tests/check.py --baseline  (antes, f3d3f95)     → 19 FAIL · 129 WARN · LÍNEA BASE: VERDE
tests/check.py --baseline  (después del split)  → 19 FAIL · 129 WARN · LÍNEA BASE: VERDE
diff antes.txt despues.txt                      → sin diferencias, ni una línea
```

**Partir la línea no mueve absolutamente nada de la suite.** Es el control que se pedía: `T15`/`T16` quedan exactamente como estaban, byte a byte en la salida.

**Nivel 2 — el acto completo**, incluidos los archivos de `forense/`. Aquí sí se mueve una cifra, y es la que este acto **debe** mover: `FP-48` pasa de `FIRMADA` sin ejecutar a ejecutada, así que el WARN de `T22(c)` que la vigilaba (*"FP-48 FIRMADA sin ejecutar desde 2026-08-17"*) desaparece. **129 → 128 WARN, FAIL sin cambio en 19.** Esa es toda la diferencia, y su causa está identificada por comando, no supuesta: la corrida en un `git worktree` sobre `f3d3f95` limpio contra la corrida de aquí deja `T22` en `16 warn` y `15 warn` respectivamente, sin ningún otro test movido.

Cascada obligada por ese único movimiento, y **desvío declarado del perímetro**: el encargo decía «solo la línea `:101`», pero `T16` vigila las dos declaraciones de la cifra de la suite que viven en `estado-programa:195` y `:287`, y dejarlas en `129` habría dejado el canon mintiendo y la suite en rojo. Se recifran las dos a `128`, cada una con su paréntesis de recifrado y su causa, en el formato que ya usan `NOTAS-P3`/`CONSOLIDA-2`/`MESA-18AGO` en esas mismas líneas. Es cascada mecánica de la cifra, no contenido nuevo.

Un tercer efecto, atrapado por la suite y corregido antes de cerrar: la nota de este acto se llamaba `2026-08-18-estado-split.md` y `T02` marcó **colisión de nombre normalizado** con `forense/encargos/2026-08-18-ESTADO-SPLIT.md`. Renombrada a `2026-08-18-estado-split-clausula-por-linea.md` — mismo patrón que ya usa `SELLA-RUTAS` (nota corta, encargo con sufijo). `T02` vuelve a `ok`.

Estado final, corrida real: **19 FAIL · 128 WARN · `LÍNEA BASE: VERDE`**, con `T15`, `T16` y `T02` los tres en `ok`.

Por qué el nivel 1 sale limpio está medido **antes** de partir, no descubierto después:

- **T15 (`T-ADR-COUNT`)** escanea `canon/*.md` línea por línea buscando `(\d+)\s*ADR\b`. En `:101` hay **un solo match**, `105 ADR`, en la cabecera — igual al real de `gobernanza`. Partir la línea no puede crear matches nuevos (el texto no cambia) y la cabecera se queda entera, así que T15 sigue derivando el conteo desde donde siempre. Verificado además que ninguna cláusula queda separada de una marca `{cita-historica}` suya: en `:101` no hay ninguna.
- **T16 (`T-SUITE-SELF-CHECK`)** busca `\*\*(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN\*\*` y `total de WARN de la suite es …`. En `:101` **no hay ni un match** de ninguno de los dos patrones (los `18 FAIL`/`107 WARN` que aparecen en la prosa no van en negrita y no son lo que el regex vigila). T16 es indiferente a este cambio, y la corrida lo confirma.

## §6 · Punto 4 del encargo: `merge=union` **NO se añade**, y por qué

Decisión declarada, no omisión: **`.gitattributes` no se toca**.

1. **Mesa eligió una de las tres opciones, no dos.** `D-7` es *«Partirlo completamente»* — la opción «partir en una cláusula por línea», que es exactamente lo entregado. La lista partida ya hace viable el merge línea a línea, que era el problema que `FP-48` planteaba.
2. **`estado-programa` no es append-only, y `union` solo es seguro sobre append-only.** `hallazgos.md` y `bitacora.md` crecen por el final y nunca se editan en medio; `:101` se edita en medio cada vez que un ADR se renumera al fusionar — que es, literalmente, lo que pasó en `a0be3d5` y `8158ab4`. `union` no conflictúa nunca: **duplica en silencio**.
3. **Es el mismo motivo, ya escrito en `.gitattributes`, por el que `hitoD-preregistro` está excluido a propósito**: los tests cuentan sobre ese archivo, y una duplicación silenciosa infla un contador sin ruido. `estado-programa` es el archivo **más** contado del repo (T15, T16, T17, T20…). *«Un merge manual que conflictúa es ruidoso; un union que duplica no lo es»* — el argumento es de `.gitattributes`, y aplica aquí con más fuerza, no con menos.
4. **La segunda capa tampoco sería garantía.** Per `forense/notas/2026-08-12-union-vs-boton-github.md`, el botón «Merge pull request» de GitHub **no honra el driver del lado servidor**: `union` solo protege en merge local. Añadirlo daría cobertura aparente en la ruta por la que este repo fusiona de verdad.

Requisito colateral verificado de todos modos, por si mesa reabre: `canon/estado-programa-v1_10.md` **termina en salto de línea** (`True`), que es la precondición dura que `.gitattributes` exige para cualquier archivo `union`.

## §7 · Punto 5 del encargo: perímetro libre, verificado antes de tocar

```
git branch -r  →  origin/main
                  origin/claude/sello-ficha-g3-v2-coeficiente-pnojt6
git diff --stat origin/main...origin/claude/sello-ficha-g3-v2-...
   → forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md | 13 +
     1 file changed  — NO toca canon/estado-programa
```

Ningún carril remoto vivo tiene `estado-programa` en su perímetro activo. Revisados además los encargos `VIVO` de `forense/encargos/`: ninguno declara `canon/estado-programa-v1_10.md` en su bloque ESCRIBE (`ADQ-15`, `CENSO-CMD`, `E3-TRIAGE`, `LANE-A-E0-E5`, `REFIRMA-OPACA`, `T20-LLAVES`, `FP10-PRECEDENCIA`, `FUSION-PUERTAS` escriben `data/`, `tools/`, `tests/`, `milpa/` o notas). La condición del punto 5 se cumple **en el momento de ejecutar**, y por eso se ejecuta.

**Conducta de fusión declarada (última cláusula del carril).** La ola 1 toca `:27`/`:101` en cascada. Este acto pide ser **el último de la ola en fusionar**. Si no lo es —si otro carril sella un ADR y añade su cláusula a `:101` antes—, la reconciliación se hace **cláusula por cláusula una sola vez más**, a mano y declarada: se toma la cláusula nueva del lado de `main`, se añade como **un ítem más** al final de la lista, y se re-corre el control del §4 (reconstrucción y hash contra el párrafo de `main`, más el conteo de secuencia). Es la última vez que ese trabajo manual hace falta: a partir de este commit, dos ramas que añadan cláusulas distintas al final tocan líneas distintas y `git` las fusiona sin decidir por nadie — o conflictúa ruidosamente si tocan la misma. Que es todo lo que `FP-48` pedía.

## §8 · Lo que este acto NO hace

- No sella ADR ni mueve el conteo: sigue **105**, y la cabecera de `:101` lo sigue declarando. Un acto de forma no gana cláusula propia en la narración que acaba de partir.
- No toca `:27`, ni ningún otro archivo de `canon/`. Las únicas líneas de `estado-programa` distintas de `:101` que cambian son `:195` y `:287`, y solo en la cifra de WARN de la suite (`129`→`128`) que `T16` obliga a mantener sincronizada — desvío del perímetro declarado en §5, con su causa única identificada.
- No añade `merge=union` (§6).
- No resume, no moderniza redacción, no corrige ninguna cláusula, ni siquiera el `.;` sobrante que arrastra el final de la cláusula de `ADR-102` — está en el original, se conserva en el ítem. Corregirlo habría sido contenido.

## §9 · Apéndice, 18/ago/2026 — la primera fusión sobre la línea ya partida, y un duplicado de `union` en el camino

Añadido después del merge de `PR #264`, cuando `PR #265` (`ACTO CONF-07-CIERRE`, `ADR-106`) fusionó sobre este trabajo. Dos resultados, uno esperado y uno no:

**1. La partición hizo su trabajo, y se puede verificar.** `#265` añadió su cláusula como **un ítem más** al final de la lista (`- a 106 después, con ``ADR-106``…`) y no tocó ninguna de las 66 anteriores. La cabecera pasó de `105 ADR` a `106 ADR` en su línea, sola. Ese merge, con `:101` como párrafo único, habría sido otra vez la ruleta que `FP-48` describe: un lado entero gana, el otro desaparece en silencio. Es la primera evidencia positiva del cambio, no una promesa.

**2. `merge=union` duplicó una entrada, en `hallazgos.md`, en un merge real.** El commit de backfill del número de `PR #264` **edita una línea en medio** del archivo en vez de apendizar al final; `union` se quedó con la versión de `main` (sin backfill) **y** con la de la rama (con él), sin conflicto y sin aviso. Resuelto a mano conservando el orden de `main` y aplicando el backfill sobre esa copia. El detalle está en `forense/hallazgos.md`; lo que importa para esta nota es que **es un caso vivo del argumento de §6**: hasta hoy esa duplicación solo se había reproducido en ramas de prueba (5/ago), y bastó poner un número de PR para provocarla. Si `estado-programa` llevara `union`, la copia duplicada habría sido una cláusula de canon o una cifra que los tests derivan — no una línea de bitácora. La decisión de no extender el driver se mantiene, ahora con evidencia en vez de solo con precedente.

## §10 · Dos cosas que este acto encontró y **no** arregló, con su razón

Las dos salieron del barrido que siguió al duplicado de `#265`. Ninguna entra en el perímetro de `ESTADO-SPLIT`, y las dos quedan aquí escritas en vez de arregladas al paso — que es la diferencia entre un hallazgo registrado y un acto que se ensancha solo.

### (a) `forense/bitacora.md:1052-1098` — dos sesiones prensadas bajo un solo encabezado

El archivo tiene **26** marcadores `**Fecha:**` contra **25** encabezados `## 20…` y **25** separadores `---`: sobra exactamente un bloque de sesión sin cabecera propia. En `:1052-1098` conviven, bajo un único `## 2026-08-03`, la sesión de `sesion/hitoD-r7-2-delito-sin-seguro` y la de `sesion/cal-conf-faseb-pos4-envipe-tpervic2-tmodvic-paso2` — dos ramas y dos juegos de commits distintos, sin `---` ni `##` entre ellas.

**No es de `merge=union`, y el dato importa porque la tentación era achacárselo:**

```
git log -1 --format='%h %ci %s' 3c8b44b
  → 3c8b44b 2026-08-04 00:33:47 -0600 forense/bitacora.md: resuelve conflicto de stash pop (append-only)
     Fecha: 22 → 23   ·   ## 20…: 22 → 22        (el bloque entra sin su encabezado)
primer commit con merge=union en .gitattributes
  → bec10ea 2026-08-05 17:11:09 +0000 Encargo CU: T20 cascada vigilada...
```

El defecto es del **4/ago**; el driver llegó el **5/ago**. Lo produjo una **resolución manual de conflicto** (`stash pop`), el otro modo de falla del mismo problema: donde `union` duplica sin avisar, la mano pega sin encabezado. No se toca aquí por una razón concreta además del perímetro: `forense/bitacora.md` **se genera con `tests/bitacora.py`**, así que la corrección correcta es por el generador —o por la vía que ese script defina— y no editando el archivo a mano, que es justo lo que lo rompió.

### (b) Esta clase de defecto no tiene vigía, y el que se propondría es más angosto de lo que parece

`T02` vigila duplicados **de archivo** (dos archivos con el mismo nombre normalizado o el mismo contenido) — de hecho atrapó la colisión de nombre de la nota de este acto. Ninguno de los 22 tests vigila una **entrada repetida dentro de un archivo**, que es exactamente lo que llevaba cinco días en `hallazgos.md`.

El predicado que sí funcionaría, medido contra el árbol de hoy y no imaginado:

> *ninguna entrada fechada de `forense/hallazgos.md` —línea que abre con `- **20`— aparece dos veces byte-idénticas.*

Hoy daría **verde** (312 entradas, 0 repetidas) y no movería ninguna cifra de la suite: un test que pasa no añade `FAIL` ni `WARN`, así que no arrastra cascada a `estado §4`.

**Lo que no funciona, y por eso el predicado no se puede escribir «para los archivos `union`» en general:** el mismo criterio aplicado a `forense/bitacora.md` da **91 líneas de commit repetidas de 287** (una llega a repetirse **5** veces), y son legítimas — el generador lista rangos que se solapan entre sesiones. Ahí la unidad no es la línea sino el bloque de sesión, y un test a nivel de bloque **nacería en rojo** por el defecto (a), no por uno nuevo. Un vigía honesto de esta clase, entonces, es: `hallazgos.md` por entrada ya; `bitacora.md` solo después de arreglar (a), y por bloque.

Escribirlo es **acto propio con su encargo** —toca `tests/check.py`, que es el aparato que mide el programa entero, y este acto es de forma sobre un archivo de canon—, no una línea que se cuele en el cierre de `ESTADO-SPLIT`.

