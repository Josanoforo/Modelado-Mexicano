# ACTO RESCATE-CURADOR — cierre: historia = PURGA-ARTIFACT, untracked rescatado, `ADR-110(d)` corregido, `FP-58` abierta

`PR #274` · Base final: `e6864ed` → merge `d00d1ab` · `ADR-111` sella este cierre. Ejecutado en dos fases con dos herramientas convergiendo en la misma rama (§3), corregido en su premisa por directiva de mesa (§1) y en su plan de ejecución por ocho precisiones de dirección (§3, nota de coordinación) — ambas citadas íntegras, con la segunda como adenda, en `forense/encargos/2026-08-18-RESCATE-CURADOR.md`.

## §0 · Arranque

`pgrep -af "curador|barrido2|semantic"` → sin proceso ajeno vivo, corrido varias veces a lo largo del acto. `git worktree list` tomado como mapa antes de tocar nada. Ninguna marca `DUEÑO-<pid>-<fecha>` en `multi1-staging/`/`multi2-staging/` del worktree `curador`. `b2-semantico` (`PR #268`) verificado como caja con dueña activa en el arranque de este acto — su worktree local avanzó de `5b35be9` a `f7817eb` en ~12 minutos entre dos chequeos; **se fusionó durante este mismo acto** (`mergedAt` `2026-08-19T01:08:42Z`) y con ella se abrió el gate original del encargo v2. No se tocó su worktree, su staging, `.barrido2/` ni el corpus en ningún momento.

## §1 · El reframe — `ACTO Z` ya había cerrado el titular

Verbatim, `forense/notas/2026-08-13-z-inventario-curador.md:3-4` (commit `740af59`, **12/ago/2026 18:47**, un día *antes* de que `forense/notas/2026-08-13-w-limpieza-worktrees.md` declarara a `curador` "la pieza más grande del inventario sin adjudicar"):

> 1. Contenido único: **NINGUNO**. Los 590 commits "sin empujar" de `codex/curador-baseline-semantico` son historia pre-purga, no trabajo huérfano — no hay nada que rescatar.
> 2. Prueba de pre-purga: `git merge-base origin/main HEAD` → `9301e59 2026-07-29` — mismo ancestro común que los 6 refs `*-huerfana-20260813`.

Re-verificado en esta sesión, contra `e6864ed`: `merge-base` sigue en `9301e59`; `git diff --diff-filter=A --name-only origin/main HEAD | wc -l` → `0`. `PURGA-PRIVACIDAD` (10/ago) corrió `filter-repo` sobre un espejo de `origin` para eliminar 1,737 filas con datos personales, reescribiendo cada SHA de `main`; `curador` (última actividad 07/ago) nunca se rebasó sobre esa historia. `canon/remapeo-shas-purga-2026-08-10.tsv` confirma el HEAD de `curador` (`3d5f34c`) como commit reescrito conocido.

**Estilo `A.10`:** el sello de `w-limpieza`/`FP-55` fue correcto contra su propio universo. `NOTAS-P3` (18/ago, #261) tampoco se equivocó: citó `w-limpieza`, verificó que no había fila en el tablero y abrió `FP-55` con la evidencia que tenía enfrente. **Lo vencido es el número — no la prudencia de ninguno de los dos actos que lo propagaron.**

## §2 · Un segundo eco de la misma premisa vencida — `ADR-110(d)`, corregido sin tocarlo

`MESA-19AGO` (`PR #267`) resolvió `D-4` con la misma directiva de mesa citada arriba, y su ejecutor registró la respuesta (`ADR-110(d)`) — pero añadió una inferencia propia que la firma de mesa no decía: *"no hay contenido que rescatar ni riesgo de pérdida que un bundle resuelva, así que `RESCATE-CURADOR` no se escribe."* Esa frase mide únicamente lo que `ACTO Z` medía — historia commiteada — y por construcción no puede ver contenido no-trackeado. El contenido en cuestión está fechado **07/ago/2026**, antes de `ACTO Z` (12/ago) y de `ADR-110` (18-19/ago): el universo no creció después del sello, **la conclusión nació ya excedida**. Clasificado en `ADR-111` (§5) como `CONCLUSIÓN MÁS ANCHA QUE SU UNIVERSO DECLARADO` (`A.10` Corolario 2 / `ADR-67(b)`), no `VENCIDO EN ALCANCE`. La firma de mesa sobre el titular de 590 commits **queda intacta** — se corrige la extensión del ejecutor, no la decisión.

## §3 · Rescate del untracked — el riesgo real, y una colisión de sesiones resuelta en el terreno

`ACTO Z` cerró la historia de commits; su método no puede ver, por construcción, contenido no-trackeado. El worktree `curador` sí tenía algo que ese método nunca iba a encontrar: **101 archivos no-trackeados**, fechados **07/ago/2026**.

**Qué es.** `tools/curador_registro/AGENTS.md`: *"Curador del Registro Demanda-Universo... Procesar exactamente una necesidad N1-N33 por invocación del trabajador."* Sistema multi-worker con supervisor fail-closed: `curador.py` → `supervisor.py` → `multi_supervisor.py` → `multi2_fix_supervisor.py` → `multi2_fix2_finalizer.py`. `multi1-staging/` (456K) y `multi2-staging/` (1.2M) son las corridas reales de ese pipeline. **Cero coincidencia de nombre de archivo** con el `tools/curador_registro/` vigente de `main` (49 archivos, vía `BARRIDO-2`/`B2-SEMANTICO`).

**Compuerta PII — limpia, cinco ángulos, cero hits.** Encabezados TSV (61 columnas únicas, ninguna `nombre`/`apellido`/`curp`/`rfc`/`telefono`/`correo`), llaves JSON (mismo resultado), `CURP`-shaped, `RFC`-shaped, teléfono-10-dígitos, email — los cinco en cero archivos. Ningún archivo excluido del commit.

**Colisión de sesiones, real y resuelta sin pérdida.** Esta parte se ejecutó dos veces, en paralelo, sobre el mismo worktree (`../mm-rescate`) que la directiva de mesa nombra por ruta literal: otra sesión llegó primero al commit (`e24d033`, el rescate; `64609c4`, excepción `T02`/`T16` + `--freeze`), empujados como **`PR #274`**. `git status` en `../mm-rescate` volvió limpio al detectarlo — la otra sesión ya había terminado. Verificado, no repetido: mismos 101 archivos, mismo método (copia de filesystem, nunca `merge`/`cherry-pick` de la rama vieja), misma compuerta PII. No se abrió un segundo PR.

**Copia, no fusión.** `forense/rescate/curador-untracked-20260807/`, preservando ruta relativa, con `MANIFIESTO-RESCATE.tsv` propio (ruta/tamaño/mtime/sha256 de los 101). No entra a `tools/` (`ADR-95` es lista cerrada). Ninguna ancestría pre-purga se empujó.

**El tar de mesa — no observado al cierre.** `~/respaldo-worktrees/` revisado repetidamente a lo largo del acto: solo aparece `curador-2026-08-18.bundle` (sha256 `19dbf51e39962a744db8a5b97358d6fb44c7a168b2a39a286ab183ae67d79618`, 199 refs, `is okay`). Ningún `.tar` nuevo. No bloquea el cierre: la protección real para `curador` ya se logró por otra vía, más fuerte — commiteado y empujado a GitHub (`PR #274`). La pieza que **sigue sin red propia** es `barrido-completo` (§4).

## §4 · `barrido-completo` y la relación `N1-N33` — reconciliado contra un segundo análisis

`Modelado-Mexicano-barrido-completo`: **780 archivos, 6.5MB**, cero commits, cero PR, todos bajo `data/curacion-registro/ejecucion-semantica/runs/`. ⚠️ Corrige una cifra de una nota de sesión anterior que citaba "883/51MB" — recifrado por comando directo: **780/6.5MB** es la vigente.

Nombres bajo `runs/`: `SEMRUN-<hash>/contratos/SEMTSK-<hash>.json`, `SEMRUN-<hash>/inputs-curador/TCUR-<hash>.json`. Barrido explícito del patrón `N1`...`N33`: **0 coincidencias** en 780 nombres.

**Dos análisis independientes, dos ejes distintos, ambos correctos.** `PR #274` comparó el rescate contra el *tracked* `data/curacion-registro/relaciones.tsv` de `main` y concluyó `MISMA-OBRA-EN-DOS-ETAPAS`, citando la colisión literal de `decisiones-humanas.tsv` (capturada por `T02`, congelada vía `--freeze`). Verificado aquí: `data/curacion-registro/relaciones.tsv` trae `capa1_universo_indexado`/`capa2_manifiesto`/`capa3_disco_real`/`capa4_apertura_mapeo`/`clasificacion_relacion`/`reason_code` — casi idéntico al esquema de `multi1-staging/integrado/registro-demanda-universo-curado.tsv` del rescate (no al `worker-1-relaciones.tsv` crudo, más simple). **Confirma linaje real**: el prototipo `Demanda-Universo` de `curador` evolucionó hacia el esquema que hoy vive trackeado en `main`.

Pero la pregunta de la directiva era más estrecha: ¿son la misma obra los **dos cuerpos en riesgo**? Ahí la respuesta no cambia: lo untracked de `barrido-completo` es exclusivamente `SEMRUN-*/SEMTSK-*/TCUR-*` — artefactos de *ejecución*, no una copia del registro `relaciones`/`decisiones-humanas`.

**Veredicto final, con las dos piezas integradas:** `MISMA-OBRA-EN-DOS-ETAPAS` a nivel de programa (linaje real, con evidencia de esquema) **y** `TEMAS-COINCIDENTES-OBRAS-DISTINTAS` a nivel de los dos cuerpos específicamente en riesgo. Ninguno de los dos análisis estaba equivocado; medían ejes distintos.

**`FP-58` abierta.** El rescate-a-PR de `barrido-completo` es acto sucesor declarado, no ejecutado aquí.

## §5 · Barrido de las otras 24 ramas de `w-limpieza §4`

Mismo método de `ACTO Z`, re-corrido por comando contra `e6864ed` sobre cada una de las 24 ramas restantes:

| rama | merge-base | fecha | HEAD/mb ∈ remap-tsv | sin-empujar (fresco) | sin-empujar (nota 13/ago) | veredicto |
|---|---|---|---|---:|---:|---|
| `cruce1-1786051624` | `9301e59` | 29/jul | Sí (HEAD) | 575 | 575 | `PURGA-ARTIFACT` |
| `wt-abrir4-1786051186` | `9301e59` | 29/jul | Sí (HEAD) | 568 | 568 | `PURGA-ARTIFACT` |
| `barrido1-1786050583` | `9301e59` | 29/jul | Sí (HEAD) | 560 | 560 | `PURGA-ARTIFACT` |
| `sesion/indice2-1786050152` | `9301e59` | 29/jul | Sí (HEAD) | 554 | 554 | `PURGA-ARTIFACT` |
| `explora2-1786042858` | `9301e59` | 29/jul | Sí (HEAD) | 546 | 546 | `PURGA-ARTIFACT` |
| `verif3-outage-note-1786046437` | `9301e59` | 29/jul | Sí (HEAD) | 538 | 538 | `PURGA-ARTIFACT` |
| `verif3-1786042795` | `9301e59` | 29/jul | Sí (HEAD) | 536 | 536 | `PURGA-ARTIFACT` |
| `map2-cruce-1786030513` | `9301e59` | 29/jul | Sí (HEAD) | 526 | 526 | `PURGA-ARTIFACT` |
| `repair1-094125-2` | `9301e59` | 29/jul | Sí (HEAD) | 521 | 521 | `PURGA-ARTIFACT` |
| `claude/explora-puertas-banxico-qnm3cn` | `9301e59` | 29/jul | Sí (HEAD) | 517 | 517 | `PURGA-ARTIFACT` |
| `ci-endurecido` | `9301e59` | 29/jul | Sí (HEAD) | 514 | 514 | `PURGA-ARTIFACT` |
| `int1-integridad-1786003491` | `9301e59` | 29/jul | Sí (HEAD) | 511 | 511 | `PURGA-ARTIFACT` |
| `map1-lector-1786000558` | `9301e59` | 29/jul | Sí (HEAD) | 505 | 505 | `PURGA-ARTIFACT` |
| `verificacion-crc-eocd-corpus` | `9301e59` | 29/jul | Sí (HEAD) | 495 | 495 | `PURGA-ARTIFACT` |
| `map1b-censo-1786000741` | `9301e59` | 29/jul | Sí (HEAD) | 495 | 495 | `PURGA-ARTIFACT` |
| `conf17-reconciliado` | `9301e59` | 29/jul | Sí (HEAD) | 485 | 485 | `PURGA-ARTIFACT` |
| `desc1-descarga` | `9301e59` | 29/jul | Sí (HEAD) | 483 | 483 | `PURGA-ARTIFACT` |
| `ver1-crudo` | `9301e59` | 29/jul | Sí (HEAD) | 477 | 477 | `PURGA-ARTIFACT` |
| `sesion/p-lapop-microdato` | `9301e59` | 29/jul | Sí (merge-base) | 424 | 424 | `PURGA-ARTIFACT` |
| `sesion/regla-elegibilidad-preregistro-r5-1` | `9301e59` | 29/jul | Sí (HEAD) | 304 | 304 | `PURGA-ARTIFACT` |
| `sesion/cruce-catalogo-fichas` | `9301e59` | 29/jul | Sí (HEAD) | 299 | 299 | `PURGA-ARTIFACT` |
| `mesa/s-svystat-4celdas` | `f9e58e8` | **11/ago** | No | 1 | 1 | ver nota* |
| `map-b/crosswalk-fuente-puerta` | `bcd8a66` | 12/ago | No | 0 | 0 | ver nota** |
| `cierre-164-hallazgos-2026-08-10` | `cfb3756` | 10/ago | No | 0 | 0 | `Modelado-Mexicano-barrido-completo`, §4 |

**21 de 24 son `PURGA-ARTIFACT` limpio.** Cero deriva en 5 días contra los conteos de `w-limpieza` del 13/ago.

**\* `mesa/s-svystat-4celdas`.** Su único commit es un merge de bookkeeping (`7ce1636`, 11/ago) sobre una base **posterior** a la purga — no es historia pre-purga, es estancamiento post-purga. `git diff --diff-filter=A --name-only origin/main mesa/s-svystat-4celdas | wc -l` → **0**. Veredicto: **`SIN-CONTENIDO-ÚNICO`** (mismo resultado que `PURGA-ARTIFACT`, mecanismo distinto). Untracked en su worktree: solo `data/raw` (defecto ya conocido, presente también en el clon base).

**\*\* `map-b/crosswalk-fuente-puerta`.** 0 sin empujar, ya ancestro de `origin/main`. Riesgo real, ya señalado por `w-limpieza`, es de disco: `scratch/build_crosswalk.py`, un script. No cubierto por ninguna fila de tablero hoy — señalado para que no se pierda por silencio, sin abrir fila nueva sin marca de mesa (fuera del mandato explícito de esta directiva).

## §6 · Cierre

**`FP-55` → `CERRADA`.** `firmada_en` (de `ADR-110(d)`, sin tocar) queda intacto; `ejecutada_en` = `PR #274, ADR-111`; `encargo` = `forense/encargos/2026-08-18-RESCATE-CURADOR.md`.

**`FP-58`** abierta para `barrido-completo` (§4).

**`ADR-111`** cita y corrige `ADR-110(d)` sin tocar su texto. Cascada re-derivada dos veces (al escribir: máximo 110, candidato 111; al fusionar: re-derivar contra el árbol real en ese momento — colisión esperada, misma protocolo usado nueve veces esta semana).

**Merge `d00d1ab`: conflicto real en `canon/estado-programa-v1_10.md`, resuelto por comando, no por aritmética.** Dos ramas divergentes desde `e6864ed`/`6ded00c` habían recifrado correctamente su propio árbol (`origin/main`: 19 FAIL·118 WARN; esta rama: 21 FAIL·126 WARN) y ninguna tenía la del árbol fusionado. `python3 tests/check.py --baseline` sobre el árbol ya fusionado, dos iteraciones (`T16` atrapó dos citas propias desincronizadas, corregidas cláusula por cláusula, mismo patrón que `ESTADO-SPLIT`/`CONF-07-CIERRE` ya documentaron): **21 FAIL · 119 WARN, LÍNEA BASE: VERDE**. `tests/baseline.json` sin tocar, cero `--freeze` nuevo (los 2 `T02` ya estaban congelados por `PR #274`).

**Worktrees `PURGA-ARTIFACT`: no se borran en este acto.** Limpieza física es acto aparte, con el bundle (`~/respaldo-worktrees/curador-2026-08-18.bundle`, verificado) como red.

**Contadores de medición sobre México que mueve este cierre: cero.**

`encargo` → `CONSUMIDO`.
