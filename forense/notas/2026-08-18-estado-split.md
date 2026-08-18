# Nota del acto · ESTADO-SPLIT — `estado-programa:101` deja de ser una sola línea

18/ago/2026 · rama `claude/launcher-estado-split-wglzaf` · SHA de arranque `f3d3f95` (`origin/main`, merge `#263`, `ACTO COND-ATRIB`, `ADR-105`) · encargo `forense/encargos/2026-08-18-ESTADO-SPLIT.md`.

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

La suite completa se corrió **antes** de tocar el archivo y **después**, y las dos salidas se compararon con `diff`:

```
tests/check.py --baseline  (antes, f3d3f95)  → 19 FAIL · 129 WARN · LÍNEA BASE: VERDE
tests/check.py --baseline  (después)         → 19 FAIL · 129 WARN · LÍNEA BASE: VERDE
diff antes.txt despues.txt                   → sin diferencias, ni una línea
```

No es coincidencia, y por qué importa está medido antes de partir:

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
- No toca `:27` ni ninguna otra línea de `estado-programa`, ni ningún otro archivo de `canon/`.
- No añade `merge=union` (§6).
- No resume, no moderniza redacción, no corrige ninguna cláusula, ni siquiera el `.;` sobrante que arrastra el final de la cláusula de `ADR-102` — está en el original, se conserva en el ítem. Corregirlo habría sido contenido.
