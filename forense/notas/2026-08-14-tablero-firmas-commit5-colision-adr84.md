# ACTO TABLERO-FIRMAS COMMIT 5 · Colisión ADR-84/T21 con ACTO B2 — quien fusiona segundo renumera

Commit 5, no anticipado por el encargo original ni por Commits 1-4. Instrucción del usuario: *"main moved again fetch and solve"*.

## §0 · Lo que llegó

```
$ git fetch origin main
$ git log HEAD..origin/main --oneline
```
→ 5 commits, dos PR: `#239` `ACTO C` (correcciones de registro de ENLACE-2 + ADENDA-1 de M-APERTURA, no sella ADR) y `#241` `ACTO B2` (mantenimiento acotado de `via_capa2.py` bajo la ventana `ADR-70(d)`).

`ACTO B2` derivó y selló, de forma independiente y con la misma receta de T15, **su propio `ADR-84`** (83 únicos, contiguos, sin huecos, antes de escribirlo — verbatim de su propio commit) y añadió a `tests/check.py` su propio **`T21 T-CAPA2-CAPA3`**. Colisión doble, exacta, contra el `ADR-84`/`T21` de este mismo acto (`ACTO TABLERO-FIRMAS COMMIT 1`), derivados también contra una base de 83 únicos — la misma ventana de concurrencia que ya produjo la colisión `ADR-73` entre `ADJ-4`/`ALIAS-P`, y la de `ADR-69` entre `ENCARGO CABLEADO-100`/`PR #175`.

## §1 · Regla aplicada, sin ambigüedad

Precedente, ya escrito dos veces en `gobernanza`: *"renumerado de ADR-69 tras colisión de numeración con `PR #175`, que selló su propio ADR-69 sobre el mismo hallazgo raíz y fusionó primero"* (`ADR-70`); mismo criterio en la colisión `ADR-73` entre `ADJ-4`/`ALIAS-P`. **Gana quien fusiona primero a `origin/main`; el otro renumera.** `ACTO B2` (`PR #241`) ya está fusionado — `git log HEAD..origin/main` lo trae como historia ya integrada. Este acto (`PR #240`) no lo está. No hay ambigüedad que resolver: este acto renumera.

**Ninguno de los dos actos erró.** Cada uno corrió `T15` contra el `origin/main` real que tenía delante en su propio momento y ambos derivaron correcto — 83 únicos, contiguos, sin huecos, en los dos casos. La colisión es de concurrencia, no de mecanismo: dos ramas independientes reclamando el mismo número siguiente no es detectable por ningún acto hasta que una de las dos intenta fusionar contra la otra ya fusionada.

## §2 · Renumeración ejecutada

**ADR:** mi `ADR-84` (ACTO TABLERO-FIRMAS, Commit 1 + enmienda de Commit 3) → **`ADR-85`**. Mi `ADR-85` (autorización de recongelado, Commit 4) → **`ADR-86`**. `T15` contra el árbol fusionado: únicos 86, max 86, sin huecos.

**Test:** mi `T21 T-FIRMAS` → **`T22 T-FIRMAS`**, en `tests/check.py`: función `t21_firmas` → `t22_firmas`, helper `_t21_tabla` → `_t22_tabla`, constantes `_T21_MARCADOR_RANURA`/`_T21_MARCADOR_PENDIENTE`/`_T21_ARCHIVOS_CONOCIDOS` → `_T22_...`, todas las llamadas `fail("T21", ...)`/`warn("T21", ...)` internas del bloque propio → `"T22"`. El `T21 T-CAPA2-CAPA3` de `ACTO B2` no se toca — es código y prosa ya fusionados a `main`, ajenos a este acto.

**Alcance de la renumeración, declarado con precisión.** Se editó directamente el texto de mis propios `ADR-84`/`ADR-85` (aún no fusionados a `main`, todavía borrador de esta rama/PR) — no es una "enmienda in situ" sobre historia ya sellada (esa convención es para ADR que YA están en `main` y que ningún acto vuelve a tocar); es corregir un borrador antes de publicarlo, mismo tratamiento que recibiría un typo. Lo que **no** se toca es el `ADR-84`/`T21` de `ACTO B2`, ya fusionado — eso sí es historia sellada ajena.

## §3 · Verificación fila por fila contra el árbol fusionado

**`ACTO C` (`PR #239`) toca `relaciones.tsv`** — un único diff de una fila, `REL-45672e7d7c5ac7c69edaede4` (N6/ENFIH): retracta una caracterización de `ACTO ENLACE-2` sobre por qué esa fila difiere de su "gemela" `REL-ba510588463c8ab0539acf46`. **No toca la política de pares en sí** — `FP-24` (`RANURA (c)`, política de pares `SI`+`NO_DETERMINADO` para `relaciones.tsv`) sigue exactamente igual de cierta y sin firma: verificado con `git diff cf0dd68..c8c3507 -- data/curacion-registro/relaciones.tsv`, un solo diff, ninguna fila nueva de la clase que `FP-24` describe. `FP-24` no cambia.

**`ACTO B2`/`ACTO C`, archivos nuevos con marcador:** ninguno dispara `T22` — corrida limpia contra el árbol fusionado, cero FAIL nuevos (`_T22_ARCHIVOS_CONOCIDOS` no necesitó entradas nuevas de estos dos actos).

**Tablero: sin cambio.** 24 filas, 19 `ABIERTA`, 5 `FIRMADA` — ni `ACTO B2` ni `ACTO C` resuelven ni abren ninguna fila del tablero.

## §4 · Contadores

`python3 tests/check.py`, corrida sobre el árbol fusionado y renumerado, sin necesidad de tocar las citas mutables de WARN (el total no se movió por esta colisión — coincidencia verificada, no asumida): **20 FAIL · 131 WARN** — 18 núcleo (`CHECK_SELFCHECK_CHILD=1`) + 2 T16 permanentes (`gobernanza:1106`/`:1136`, sin cambio). `T22`: 0 FAIL, 19 WARN. `T16`: exactamente 2 (los permanentes) — ninguna cita mutable quedó desincronizada por la renumeración, porque ninguna de ellas citaba el número de ADR o de test dentro del patrón que `T16` vigila (`**N FAIL · M WARN**`), solo prosa alrededor.

`python3 tests/check.py --baseline`, antes de recongelar: **ROJO, 19 entradas nuevas** — no son firmas nuevas, es el propio renombre `T21`→`T22`: `tests/baseline.json` tenía las 19 filas `ABIERTA` guardadas bajo la clave `T21:...`, y ahora la corrida real las emite como `T22:...` — mismo contenido semántico, clave de test distinta, 100% de las entradas "nuevas" son ese efecto y nada más (verificado uno por uno contra la lista: las 19 son exactamente las mismas `FP-*` que ya estaban `ABIERTA` antes de este commit, ninguna fila nueva del tablero).

## §5 · Freeze

`tests/baseline.json` apuntaba a `head` `6211b0d` (el recongelado de Commit 4), ya no el HEAD real tras este commit. La instrucción del usuario (*"fetch and solve"*) autoriza, en la misma línea que la autorización estructurada de Commit 4, resolver esta colisión de principio a fin — incluido dejar CI verde. Se recongela en este mismo commit, documentado aquí en vez de en un commit aparte, porque es la misma categoría de drift mecánico que Commit 4 ya cerró (no una decisión de mesa nueva): el renombre de clave no cambia ninguna fila del tablero ni ninguna cifra de FAIL/WARN, solo re-etiqueta bajo qué nombre de test vive cada WARN. `python3 tests/check.py --freeze` → `tests/baseline.json` con `head` `2af748c` (`ACTO TABLERO-FIRMAS COMMIT 4`, el HEAD real al momento de recongelar — este commit 5 aún no existía); `python3 tests/check.py --baseline` → **LÍNEA BASE: VERDE**. `python3 tests/test_svystat.py`: 13 casos, exit 0, sin relación con este acto.

## §6 · Perímetro tocado

`canon/gobernanza-v1_15.md` (resolución de merge: `ADR-84` de `ACTO B2` entra intacto; mis `ADR-84`/`ADR-85` renumerados a `ADR-85`/`ADR-86`) · `canon/estado-programa-v1_10.md` (resolución de merge, cascada 84→86, trayectoria L0 fusionada con la clausula de `ACTO B2` añadida) · `tests/check.py` (resolución de merge: `T21`/`t21_firmas` propio renombrado a `T22`/`t22_firmas`; `T21 T-CAPA2-CAPA3` de `ACTO B2` intacto) · `tests/baseline.json` (recongelado, ver §5) · `forense/hallazgos.md` (una entrada) · esta nota. `forense/firmas-pendientes.tsv` no cambia — ninguna fila nueva, ninguna resuelta.
