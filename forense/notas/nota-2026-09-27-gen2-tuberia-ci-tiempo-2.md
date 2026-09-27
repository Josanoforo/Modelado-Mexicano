# Nota de cierre · ACTO GEN2-TUBERIA-CI-TIEMPO-2 · 27/sep/2026

ADR: `ADR-260927-GEN2-TUBERIA-CI-TIEMPO-2-a387-01` (raíz `a387`, commit 0-bis `a387355c`). Encargo: `forense/encargos/2026-09-26-GEN2-TUBERIA-CI-TIEMPO-2.md`, SHA de redacción `9ceb1eac`; base al arrancar `7fcbc2e6` (main avanzó 5 commits por #1192, RECIBO-ASTRA6-1, sin tocar CI: se fusionó y se declara). ENTORNO: NUBE (hook `ENTORNO-DERIVADO = NUBE`); cero microdato, cero red a INEGI.

Contadores movidos: **cero mediciones, cero adopciones**. Contadores propios: minutos de `check` en push a `main`, lote pendiente de replay (121 hoy), fecha del último `[deriva]` fusionado. Los tres se leen **después del merge de mesa** (ver NO-CORRIDO del encargo).

## Premisas
- `[LEÍDO]` run 36291122052: re-leído por la API de jobs; `guardias` → «Deriva vistas…» cancelado 03:24:45 → 03:50:48 con «asientos nuevos examinados: 121». Se sostiene.
- `[SUPUESTO]` «`registro --escribe --lote` es incremental»: **cayó a medias.** Con lote, las filas YA publicadas y ajenas se congelan byte a byte (LOTE-ESTRICTO-1), pero toda fila **nunca publicada** se escribe fresca aunque no esté en el lote. Consecuencia medida en el código: un trozo de 20 habría publicado de golpe los 121 CALC —los 101 restantes sin su `verify`— y el pendiente habría caído a 0 sin que se verificaran. Se resuelve aquí con `registro --pospone` (difiere lo no publicado; PARO si se pospone algo publicado o algo del lote) y se prueba la equivalencia (abajo).
- `[EJECUTADO]` pendiente local = 121 (`python3 tools/lote_desde_asientos.py --incluir-pendientes --json`: `examinados 121 · lote 121 · descartados 0`).

## Medición del costo (EJECUTADO, réplica sin corpus)
`registro` base sin `verify`: **157.7 s**. `verify` por CALC sobre los primeros 53 del lote (se cortó a 900 s): media 13.9 s, mediana ≈8 s; 49 NO-EJECUTABLE, 2 REPRODUCE, 2 NO-REPRODUCE; cola larga **`CALC-ENOE-PISOS-0003`: 311 s**. 121 × ≈13 s ≈ 26 min: explica el corte a los 30 min.

## Lo que cambió
- **P1 · job `derivados`** (`.github/workflows/verify.yml`): disparado por push a `main` (salvo `[deriva]`), `workflow_dispatch` y el `schedule` nocturno ya existente (`0 9 * * *` = 03:00 UTC−6). **Fuera de `needs` de `check`**; `check` sigue exigiendo `suite, adicionales, guardias, preflight-calc, guardas-res, enrutamiento-pr` y conserva el nombre. `guardias` pierde el paso y sus permisos de escritura; no pierde ningún test. Concurrencia propia `derivados-main`, en cola, nunca cancelada.
- **P2 · troceo con base que avanza**: `lote_desde_asientos.py --trozo N --csv` (línea 1 trozo, línea 2 resto; los CALC del diff ya publicados van siempre en el trozo porque no quedarían pendientes). `registro --verifica --escribe --lote <trozo> --pospone <resto>`. HEAD no se mueve (el guardián del tablero exige HEAD == origin/main): cada trozo se publica con `git commit-tree` como commit `[deriva] trozo K …` en `derivados/auto-<run>`, el PR se abre con el primer trozo y cada push dispara su `verify`. No se abre un trozo nuevo pasados **900 s** (trozo = **20**): lo que no cabe sigue ausente de `corridas.tsv` y el run siguiente lo retoma.
- **P4 · guardia de crecimiento**: primera línea del paso `LOTE-PENDIENTE: N CALC (umbral 60) · OK|CRECE` (`tools/ci_guardias.py --crecimiento-lote`); con CRECE, anotación `::warning` y **NC automática como issue de GitHub** (una abierta a la vez). Se eligió issue y no fila de `no-corrido.tsv` porque el PR `[deriva]` sólo puede traer archivos DERIVADO (guarda de `enrutamiento-pr`). Nunca falla el check.
- `tests/test_check_parallel.py`: la derivación «todo job salvo el gate es requerido» exime **sólo** a `derivados`, y aserta que sigue fuera del gate, sólo en `main` y con sus tres disparos. Ningún otro job deja de ser requerido.

## Equivalencia (compuerta «trozo publicado = trozo derivado completo»)
- Sintética (`tests/test_ci_tiempo_2.py`, 6 casos, verde; con el código del acto retirado por `git stash` el archivo sale en rojo): tres CALC en tres trozos == un solo lote, byte a byte en las tres vistas. Paros POSPONE-EN-LOTE y POSPONE-PUBLICADA sin escritura.
- **Real (EJECUTADO en worktree temporal, D-23)**: los 121 pendientes, `registro --escribe --lote <121>` (173 s) contra tres trozos de 60/60/1 con `--pospone` (673 s acumulados) → `sha256sum` de `corridas.tsv`, `resultados.tsv` y `usos.tsv`: **IDÉNTICO**; pendiente tras los trozos: `examinados 0 · lote 0`. (Sin `--verifica`, para acotar el tiempo; `verify` sólo cambia el veredicto de los CALC del lote y no toca el congelado de lo ajeno.)

## Hallazgos
- Un PR o un merge hechos con `GITHUB_TOKEN` no disparan workflows: el drenaje **no se auto-encadena** tras el auto-merge de un `[deriva]`. Por eso el nocturno y el disparo manual; con ≈40–60 CALC por run, 121 se drenan en 2–3 runs.
- Dos runs de `derivados` sobre bases distintas (el segundo antes de que fusione el PR del primero) proponen el mismo trozo en dos PR; el segundo quedará en conflicto y sin auto-merge. La concurrencia `derivados-main` evita que corran a la vez, no que se solapen. Reserva declarada.
