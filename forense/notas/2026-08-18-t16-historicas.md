# Nota del acto · T16-HISTÓRICAS — cerrar el bucle de congelados por su última puerta

18/ago/2026 · rama `claude/new-session-cy41al` · SHA de arranque `d2fedb0` (verificado, `origin/main` no se había movido).

## §6 · Auditoría — contadores movidos

**Cero.** `13 de 27`, `0 de 15`, `11 de 15` y `1 de 2` no se mueven en este acto. Todo lo que sigue es gobierno de la suite de verificación, no medición sobre México.

Afirmación de este artefacto que describe el estado del corpus y no fue derivada por comando (única, declarada por A.4/v2.1): el juicio de que las cinco citas de `gobernanza:764,856,1274,1387,1393` "narran lo que un acto pasado midió" es lectura humana del texto, no salida de un script — el censo de *qué líneas* vigila T16 (§2 abajo) sí es 100% derivado; la *clasificación semántica* de cada una (vigente vs. histórica) es juicio, aplicado con el mismo criterio para las 11 y comparado contra la propuesta del encargo.

## §1 · Verificación de existencia — confirmada contra `d2fedb0`

```
grep -n "MARCA_HISTORICA" tests/check.py          → 536 (definición) · 560 (uso, en t15_adr_count)
grep -c "MARCA_HISTORICA" tests/check.py          → 2
grep -rn "cita-historica" canon/                  → gobernanza:970 · gobernanza:1686 · gobernanza:1700
```

Confirmado: `t16_suite_self_check` solo consultaba `_CAMBIO_FECHADO`. `MARCA_HISTORICA` no existía en el árbol de T16.

## Commit 1 · T16 honra `MARCA_HISTORICA`

Parche de cuatro líneas en `t16_suite_self_check` (`tests/check.py`), espejo exacto de `t15_adr_count`. Ampliado el `LÍMITE DECLARADO` del docstring: ya no es cierto que `_CAMBIO_FECHADO` sea el único marcador mecánico — se documenta `MARCA_HISTORICA` con fecha y acto (T16-HISTÓRICAS, 18/ago/2026).

**Controles, corridos antes de commitear, revertidos después (no quedan en el árbol):**

- **N1** — inyectada en `canon/gobernanza-v1_15.md`: `Control: **99 FAIL · 99 WARN** sin marca.` → `python3 tests/check.py` da `[FAIL] T16 T-SUITE-SELF-CHECK (4 fail)`, con `canon/gobernanza-v1_15.md:1799 declara 99 FAIL · 99 WARN vigente; la corrida real da 19 FAIL · 135 WARN`. **Protección intacta.**
- **N2** — misma línea, con ` {cita-historica}` detrás → `[FAIL] T16 T-SUITE-SELF-CHECK (3 fail)`, de vuelta a los 3 FAIL permanentes de base (`:1106`, `:1136`, `:1658`). **El marcador exime.**
- **N3** — corrida tras el Commit 2 (una vez existen las 8 marcas reales): `[ ok ] T15 T-ADR-COUNT` y `[ ok ] T16 T-SUITE-SELF-CHECK` a la vez. **T15 no se rompe con su propio uso de la marca.**

Las dos inyecciones de N1/N2 se revirtieron con `cp` desde una copia de respaldo antes de tocar nada más; `git status` confirmó el árbol limpio antes de seguir.

## Commit 2 · Censo re-derivado y marcado de las ocho

Censo derivado por script independiente (no de memoria del encargo) sobre las dos expresiones regulares que `t16_suite_self_check` vigila, contra `canon/*.md`:

| línea | `_CAMBIO_FECHADO` | clase (mi lectura) |
|---|---|---|
| `estado-programa:50` | sí | exenta por changelog |
| `estado-programa:129` | no | **vigente** — declara el total real, no se marca |
| `estado-programa:221` | no | **vigente** — declara el total real, no se marca |
| `gobernanza:764` (ADR-62) | no | **histórica** — narra lo que ADR-62 midió al sellarse |
| `gobernanza:856` (ADR-66) | no | **histórica** — narra lo que ADR-66 midió al sellarse |
| `gobernanza:1106` (ADR-76(f)) | no | **histórica** — narra un recongelado pasado |
| `gobernanza:1136` (ADR-77) | no | **histórica** — narra el estado al sellar ADR-77 |
| `gobernanza:1274` (cascada de ADR-81, cita ADR-84) | no | **histórica** — narra su propia trayectoria pasada |
| `gobernanza:1387` (enmienda de ADR-85, cita ADR-84) | no | **histórica** — narra el resultado de un merge pasado |
| `gobernanza:1393` (ADR-86) | no | **histórica** — narra el estado al sellar ADR-86 |
| `gobernanza:1658` (ADR-94) | no | **histórica** — narra el estado "antes de este acto" |

**Coincide exacto con la tabla del §0 del encargo** (1 exenta · 3 FAIL permanente · 7 rastreador vivo, de las cuales 5 se marcan y 2 se quedan vigentes). Sin diferencias en la clasificación.

Marcadas las ocho con ` {cita-historica}` **inmediatamente** después de la cifra en negritas, sin tocar ningún dígito (verificado por diff, ver commit 2). `estado-programa:129` y `:221` no se tocan: ya traen `135 WARN` / `19 FAIL · 135 WARN`, coinciden con el real, y son declaraciones de estado vigente por diseño (siguen la convención descrita en su propio texto: *"cifra mantenida en sincronía por T16"*).

## Commit 3 · Qué decía cada una cuando se selló

Recuperado con `git log --format="%h %ad %s" -G"<fragmento fijo de la línea>" -- canon/gobernanza-v1_15.md`, listando **todos** los commits que tocaron cada línea (no solo el primero), y `git show <sha>:canon/gobernanza-v1_15.md` para leer el texto en cada punto.

**Nota de terreno:** el clon con el que arrancó este acto era **superficial** (`git rev-parse --is-shallow-repository` → `true`, 283 commits visibles). `git log -S`/`-G` sobre un clon superficial puede devolver orden y resultados incorrectos — se detectó al ver dos commits "sin padre" y fechas fuera de orden para `:764`. Se corrió `git fetch --unshallow` (1053 commits tras el fetch) antes de derivar esta tabla; repetirla sobre un clon superficial habría dado el commit de sello equivocado para varias filas.

| cita | ADR | sellado (commit, fecha) | cifra original | cifra de hoy | commits que la sobreescribieron (orden cronológico, sin contar el de marcado de este acto) |
|---|---|---|---|---|---|
| `gobernanza:764` | ADR-62 | `4195f37`, 5/ago/2026 | **18 FAIL · 95 WARN** | **19 FAIL · 135 WARN** | `162789a` · `4cc2131` · `4bd96ef` · `85b6856` · `8f6e185` · `764c29f` · `beccf38` · `2af748c` · `3f00a1b` · `872c206` · `6947992` · `2fb4106` · `fa3b9de` · `6d9b68e` · `54e9b18` · `24cd4d8` · `9fc1297` (17 reescrituras) |
| `gobernanza:856` | ADR-66 | `e4fd7ce`, 10/ago/2026 | **18 FAIL · 95 WARN** | **19 FAIL · 135 WARN** | mismos 16 commits que `:764` desde `162789a` en adelante (se resincronizan siempre juntas — `54e9b18` literalmente se titula *"Resincroniza gobernanza:764/856"*) |
| `gobernanza:1106` | ADR-76(f) | `abf5b17`, 13/ago/2026 | **18 FAIL · 104 WARN** | **18 FAIL · 104 WARN** | **ninguno** — nunca se sobreescribió; es la única de las tres FAIL-permanente que ya se comportaba así desde su sello |
| `gobernanza:1136` | ADR-77 | `eaae2f9`, 13/ago/2026 | **18 FAIL · 104 WARN** | **18 FAIL · 104 WARN** | **ninguno** |
| `gobernanza:1274` | cascada de ADR-81, cita a ADR-84 (T21/T-FIRMAS) | `beccf38`, 14/ago/2026 | **18 FAIL · 138 WARN** | **19 FAIL · 135 WARN** | `2af748c` · `3f00a1b` · `872c206` · `6947992` · `2fb4106` · `fa3b9de` · `6d9b68e` · `9fc1297` (8 reescrituras) |
| `gobernanza:1387` | enmienda de ADR-85, cita a ADR-84 | `2af748c`, 14/ago/2026 | **18 FAIL · 131 WARN** | **19 FAIL · 135 WARN** | `3f00a1b` · `872c206` · `6947992` · `2fb4106` · `fa3b9de` · `6d9b68e` · `9fc1297` (7 reescrituras) |
| `gobernanza:1393` | ADR-86 | `2af748c`, 14/ago/2026 | **18 FAIL · 131 WARN** | **19 FAIL · 135 WARN** | mismos 7 commits que `:1387` (mismo párrafo de sello del recongelado, se resincronizan juntas) |
| `gobernanza:1658` | ADR-94 | `573bde3`, 18/ago/2026 | **24 FAIL · 126 WARN** | **24 FAIL · 126 WARN** | **ninguno** |

**Tres de las ocho nunca fueron sobreescritas** (`:1106`, `:1136`, `:1658`): su cifra de hoy es la que se selló. Coincide con que las tres son precisamente las que ya declaraba el §0 del encargo como "FAIL permanente" — son las que *dejaron* de perseguirse, y por eso quedaron congeladas en su valor real desde el primer día. Las otras cinco sí se persiguieron activamente, entre 7 y 17 veces cada una.

`gobernanza:1274` es el caso que el encargo (§3) advertía como delicado: la propia línea ya narra su trayectoria en prosa ("se actualizaron... a 18 FAIL · 119 WARN... subieron a 138... quedan en 19 FAIL · 135 WARN"). La cifra "original" que devuelve `git log -G` (**138**) es el primer punto final que tuvo esa frase, no el "119" que la prosa cita como arranque de la propia trayectoria — la frase entera ya es un resumen histórico escrito de una vez, con un final que se mantuvo actualizándose por separado. Restaurar el 138 no sería más "verdadero" que dejar el 135: ambos son puntos de una misma trayectoria que la prosa ya declara. **No se toca — es la fila que motiva la pregunta abierta de mesa, no una respuesta que este acto deba dar.**

## Commit 4 · Cierre

- `tests/baseline.json` — **no tocado**, `git status` limpio en ese archivo antes y después de los cuatro commits.
- **Ningún `--freeze` corrido.** Verificado, no supuesto:

  | | antes (`d2fedb0`) | después (este acto) |
  |---|---|---|
  | `T16` | 3 FAIL | **`[ ok ]`** |
  | suite cruda | 22 FAIL · 135 WARN | **19 FAIL · 135 WARN** |
  | rastreadores vivos | 7 | **2** (`estado-programa:129`, `:221`) |
  | línea base (`--baseline`) | VERDE | **VERDE**, con 2 entradas que dejan de aparecer (mejora, no recongelado — mensaje explícito de `check.py`: *"no baja la cifra congelada sin --freeze explícito"*) |

  La premisa del encargo se confirma exacta, cifra por cifra. **Esto es el falsador de `FP-51` pasando su primera prueba real: un acto que repara la causa del defecto en vez de silenciar el vigía, y cierra en verde sin tocar el congelado.**

- **§7 — `_baseline_key`/`_T16_REAL_SUFIJO` (ADR-90):** no se tocó ningún código de normalización. La colisión de clave que el transfer del 18/ago describía para 7 rastreadores se disuelve sola al bajar a 2 — verificado: `_T16_REAL_SUFIJO = re.compile(r"la corrida real da (\d+ FAIL · )?\d+ WARN")` sigue aplicándose igual a las claves de línea base de `estado-programa:129`/`:221`, que ahora son las únicas dos que producen ese sufijo variable en `FAILS`/`WARNS` de T16; con solo 2 en vez de 7, no hay ningún par de claves que colisionen entre sí que no colisionaran ya antes (la normalización sigue haciendo su trabajo, simplemente sobre menos entradas). No se verificó ni se tocó ningún otro uso de `_baseline_key` fuera de T16.
- **Cascada de ADR (96→97):** derivada, no tecleada — `grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | grep -oE "[0-9]+" | sort -n | tail -1` → `96`, sin huecos. Sitios de cascada re-derivados con `grep -noE ".{0,40}[0-9]+\s*ADR\b.{0,40}" canon/estado-programa-v1_10.md` → **dos** sitios, `:27` y `:101` (el encargo citaba tres, `:27,:99/:101`; `:99` no es cita de conteo de ADR — es la línea de "llaves de identificación ejercidas" — diferencia reportada, no corregida en silencio). Los tres sitios (`gobernanza-v1_15.md:2`, `estado-programa:27`, `:101`) suben de `96` a `97` con `ADR-97`.
- **PR:** no abierto en este acto — no solicitado explícitamente por quien lanzó el encargo (mismo criterio que `ACTO CI-CATEGORIA` fijó para su propio cierre). La rama `claude/new-session-cy41al` queda lista para revisión; `firmas-pendientes.tsv` registra el pendiente de PR en `ejecutada_en` de `FP-50`.

## Commit 5 · T16 espeja a T15 de verdad

El parche del Commit 1 seguía usando `re.search`, que solo devuelve la **primera** coincidencia de la línea. `t15_adr_count` (`tests/check.py:556`) ya iteraba con `re.finditer`, comprobando `MARCA_HISTORICA` por cada cita, no una vez por línea — `T16` no lo espejaba de verdad.

**Control que expone el defecto, antes y después (inyectado en `canon/gobernanza-v1_15.md`, revertido con `cp` desde respaldo, no queda en el árbol):**

```
Control doble: **99 FAIL · 99 WARN** {cita-historica} y además **88 FAIL · 88 WARN** sin marca.
```

- **Antes** (código del Commit 1, `re.search`): `[ ok ] T16 T-SUITE-SELF-CHECK` — la primera cita (marcada) hacía que la función nunca mirara la segunda. Confirmado con `git stash` sobre el código, sin tocar la inyección.
- **Después** (`re.finditer`): `[FAIL] T16 T-SUITE-SELF-CHECK (1 fail)` — `canon/gobernanza-v1_15.md:1823 declara 88 FAIL · 88 WARN vigente; la corrida real da 19 FAIL · 135 WARN`. Señala exactamente la segunda cita, deja exenta la primera.

**N1/N2/N3 del Commit 1, re-corridos contra el cambio** (mismo camino de código): los tres con el resultado esperado — N1 (cita mala sin marca) `FAIL`; N2 (misma cita, con marca) `[ ok ]`; N3 (T15 con las 8 marcas reales del Commit 2) `[ ok ]`.

**Ninguna de las ocho citas marcadas tenía una segunda cita FAIL/WARN oculta en la misma línea.** Verificado dos veces: (1) `grep -oE` sobre cada una de las 8 líneas cuenta exactamente una cita `**N FAIL · M WARN**` en negritas por línea; (2) tras el cambio a `re.finditer`, la suite se mantiene en `19 FAIL · 135 WARN` con `T16 [ ok ]` — de haber una segunda cita sin marcar, habría aparecido como `FAIL` nuevo, y no fue el caso. No es un hallazgo nuevo esta vez.

**Casi-incidente propio, corregido en el mismo commit:** el primer borrador de la enmienda `(g)` de `ADR-97` citaba el control de arriba con `**88 FAIL · 88 WARN**` en negritas dentro de la propia prosa del ADR — y `T16`, ya corregido, lo detectó como cita vigente sin marcar (`20 FAIL · 135 WARN`, línea base ROJA). Corregido quitando las negritas del ejemplo ilustrativo dentro del ADR (mismo cuidado que `ADR-96` ya tuvo con `T03` para sus propios ejemplos) — sin usar `{cita-ilustrativa}`, que es mecanismo de `T03`, no de `T16`. Re-verificado: `19 FAIL · 135 WARN`, `T16 [ ok ]`, línea base VERDE.

`python3 tests/check.py --baseline` final: `19 FAIL · 135 WARN`, `LÍNEA BASE: VERDE`, sin `--freeze`, `tests/baseline.json` intacto.
