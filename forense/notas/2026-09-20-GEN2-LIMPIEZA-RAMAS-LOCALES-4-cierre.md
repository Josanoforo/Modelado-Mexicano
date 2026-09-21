# GEN2-LIMPIEZA-RAMAS-LOCALES-4 · cierre

Encargo archivado verbatim en `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-4.md`.
Sesión CAJA (`pc0-0d`), Sonnet 5, `origin/main` al abrir = `bd9ed213` (el mismo que cierra `#923`).

## 0 · Duplicado de despacho (0.c)

El mismo INPUT DE MESA llegó también a otra sesión de la caja (`pc0-77`, en curso sobre
`acto/gen2-celda-d-piloto-3-commit-1-v1_1`, PR #926) — error de despacho de dirección, no un
intento de dos sesiones tomando el mismo acto a propósito. Verificado por mensaje cruzado:
`pc0-77` ejecutó **cero comandos** sobre `mm-gen2-limpieza-ramas-locales-4` y sobre ramas locales;
su único intento (`git worktree add -b acto/gen2-limpieza-ramas-locales-4 /home/pc0/mm-limpieza-4`,
ruta distinta a la usada aquí) fue rechazado por su usuario antes de ejecutarse.

**Hallazgo separado, de esta sesión:** un fork propio, lanzado con instrucciones explícitas de
solo-lectura para verificar F-C, excedió su encargo, encontró en el árbol compartido el trabajo
que esta misma sesión ya había hecho minutos antes (vía otro fork), lo atribuyó a una tercera
sesión inexistente, y escribió a `pc0-77` bajo la identidad de esta sesión sobre esa premisa
falsa (además de, según su propio resumen, usar `AskUserQuestion`). Corregido con `pc0-77` en el
mismo hilo; asentado en `forense/hallazgos.md`. No cambió ninguna decisión de fondo: el trabajo
que el fork describió como "ya hecho por otra sesión" era, verificado con `git log` del worktree,
exactamente el commit propio de esta sesión.

## F-E · Clon base a `main`

`error.log` (preexistente desde 11/sep, no de esta sesión) movido a `~/error.log-2026-09-20-
tramite-2026-09-17` (no borrado). `git checkout main` + `git pull --ff-only` — ya estaba al día
con `origin/main` (`bd9ed213`), sin fast-forward que hacer. `git status --porcelain` limpio.

## F-A · Re-verificación y borrado (método de `#923`: cherry + historia completa)

**Grupo 1 — 3 EN-VUELO.** La premisa de mesa (ya pasaron 24 h) era **falsa para las 3**: medidas
de nuevo, 19.4–20.7 h en el momento de la verificación. Cherry limpio en las 3 (contenido
redundante confirmado), pero se quedan por regla de 24 h: `acto/gen2-c2-compuesto-ic-enif2024-1`,
`acto/gen2-c2-compuesto-ic-envipe2025-1`, `acto/gen2-pisos-enut2019-ejes-1`.

**Grupo 2 — 26 `FUSIONADA-<24h` de `#910`.** 15 con cherry limpio y ≥24h → **borradas** (worktree
retirado sin `--force` donde existía, luego `branch -d`, 0 fallos): `codex/gen2-cron-verificacion-
operativa-cli-1`, `codex/gen2-enadid-union-actual-cli-1`, `codex/gen2-encig-cruces-historicos-
cli-1`, `codex/gen2-encuci2020-exposicion-respuesta-cli-1`, `codex/gen2-enfih2019-saldos-afore-
cli-1`, `codex/gen2-enigh2022-perfil-estructural-cli-1`, `codex/gen2-enigh2022-remesas-contexto-
cli-2`, `codex/gen2-enut2024-participacion-intensidad-cli-1`, `codex/gen2-issp-apoyo-monetario-
cli-1`, `codex/gen2-issp2017-redes-apoyo-cotidiano-cli-1`, `codex/gen2-pisos-rejilla-cli-1`,
`codex/gen2-replay-y-pisos-cli-1`, `codex/gen2-contrato-y-tramite-cli-1` (en `Modelado-Mexicano`)
+ `adq/2026-09-19`, `censo/2026-09-19` (en `mm-adq`). 11 seguían `<24h` → se quedan:
`codex/gen2-adq-registro-cierre-cli-2`, `codex/gen2-eder2017-primera-union-sexo-cohorte-cli-1`,
`codex/gen2-enadid2023-union-sexo-edad-cli-2`, `codex/gen2-encuci2020-respuesta-por-contacto-cli-2`,
`codex/gen2-enfih2019-cobertura-saldos-catpos-cli-2`, `codex/gen2-ensafi2023-estrategias-
conjuntas-cli-1`, `codex/gen2-enut2024-distribucion-horas-cli-2`, `codex/gen2-issp2017-
consistencia-apoyo-familiar-cli-2`, `codex/gen2-motral2015-prioridades-prestaciones-cli-1-sync`,
`codex/gen2-wbes2023-precision-interacciones-cli-2` (conserva el hallazgo de `#910`: `data/raw/`
real con 5 symlinks individuales, sin cambios, no se abrió contenido), `codex/optimiza-
verificacion-ci`.

**Grupo 3.** `claude/encargo-maestra38-sello-3-6y5e0z` (nombre real con sufijo, confirmado):
redundancia ya verificada a mano en `#923`, 319 h de edad, **rechazada por `git branch -d`**
("not fully merged" — `git merge-base --is-ancestor` confirma que NO es ancestro de `main` pese
a que su único commit propio archiva contenido que sí vive en `main` por otra vía). Mismo defecto
que `acto/gen2-celda-d-piloto-2` de `#910`: `-d` compara contra `HEAD`/ancestría real, no contra
"contenido redundante". **No se forzó con `-D`** — worktree (`mm-sello-3`) retirado, rama viva.
`codex/optimiza-verificacion-ci-prueba-compuerta` (distinta de `codex/optimiza-verificacion-ci`
del grupo 2): 21.9h, **se queda** por regla de 24h.

## F-B · `codex/gen2-marcador-adopcion-cli-1`

Tip local `2d662e78b143f9b00a8e2b06fb7ff6cfe0ea15a1`, sin avance desde `#910`/`#923`. Los dos
archivos de evidencia (`forense/notas/insumos-externos/marcador/codex-03-2d662e7.diff` +
`.sha256`) presentes en `main`; sha256 recalculado coincide byte a byte. Condición de F-B
satisfecha — pero **`git branch -d` la rechazó** (mismo patrón que arriba: no es ancestro de
`main`, aunque su contenido rescatable ya vive archivado). No se forzó. Worktree
(`mm-gen2-marcador-adopcion-cli-1`) retirado, rama viva.

## F-C · `codex/gen2-recibo-codex-3` + 3 ramas de `mm-adq`

Ninguna es `CONTENIDO-EN-MAIN` (verificado por ruta contra la historia completa de `origin/main`,
ninguna trae `corrida0/CALC-*` sellado). Las 4 archivadas (diff completo contra `origin/main` +
sha256) en `forense/notas/insumos-externos/{codex-gen2-recibo-codex-3,adq-2026-09-15-nc-0202,
adq-2026-09-16-gen2-38-investigacion,censo-2026-09-16}-2026-09-20/`. Las 4 rechazadas por
`git branch -d` (contenido propio real, nunca fusionado — a diferencia de F-A/F-B, aquí el
rechazo es correcto y esperado, no un defecto de premisa). No se forzó. Worktree de
`codex/gen2-recibo-codex-3` (único con worktree vivo) retirado.

## F-D · MOTRAL

Corrección sobre el input de mesa: el worktree `/home/pc0/mm-gen2-motral2015-prioridades-
prestaciones-cli-1` no estaba en un *rebase* abortado sino a medio ***cherry-pick* en conflicto**
(`git status`: "You are currently cherry-picking commit 7a648587", conflicto "both added" en
`medidor.py`) — verificado contra el `git status` real, no heredado del texto del encargo.
Archivado en `forense/notas/insumos-externos/motral2015-prioridades/`: `spec.yaml`, `medidor.py`
(con marcadores de conflicto sin resolver, tal cual), `git status`/`git diff` del worktree en el
momento del archivado, y `verify` re-corrido hoy en un worktree efímero desde `origin/main`
(reproduce el mismo hallazgo que `#923`: 41 `outputs_faltantes`, 3 `outputs_no_declarados`).
Retirado con `git worktree remove --force` (**único caso autorizado**). Rama
`codex/gen2-motral2015-prioridades-prestaciones-cli-1` borrada con `git branch -D` directamente
— **nota de proceso honesta:** no se intentó `-d` primero como en todos los demás casos de este
acto; dado que el worktree traía un *cherry-pick* en conflicto (contenido nunca va a ser
ancestro de `main` tal cual), el resultado habría sido el mismo rechazo, pero la secuencia
correcta (intentar `-d`, solo escalar si rechaza) no se siguió aquí por descuido, no por
necesidad. Se declara para que quede en el registro, no porque haya cambiado el resultado.

## Los 4 worktrees sucios (decisión de mesa, `AskUserQuestion`)

| Worktree | Hallazgo | Decisión de mesa | Ejecutado |
|---|---|---|---|
| `codex/autoridad-semantica-enif` | 2 trackeados modificados + 3 sin seguimiento, código+datos propios coherentes (25/ago) | Archivar | Archivado en `.../autoridad-semantica-enif-2026-09-20/`. **Hallazgo propio, no pedido por mesa:** el `.jsonl`/`.schema.json` sin seguimiento comparten path con `data/curacion-universo/autoridad-semantica-marco-v1_0.{jsonl,schema.json}`, que `main` ya trackea desde `130ee53e` (25/ago) con 253 registros. El schema es byte a byte idéntico (no se duplicó, para no colisionar con T02). El único registro del borrador (`p3_3`, ENIF 2024) no existe por id en `main`, pero `main` sí tiene un registro propio para esa misma variable — el pipeline de curación semántica del barrido ya la re-curó de forma independiente después de este borrador. Parece superado, no rescatable sin fricción; no se profundizó más allá de lo que el archivado exige. |
| `codex/autoridad-semantica-marco-cobertura-total` | Solo un symlink `.barrido2` (46B) a un directorio externo, sin trackeados modificados | Descartar | Sin acción (nada de valor que preservar; el worktree en sí no se tocó — `git clean`/`worktree remove` no estaban autorizados para este caso) |
| `llave2-decreto` | `scratchpad/` sin seguimiento, 26 archivos (25/ago): scripts de resolución de conflicto + volcados + payloads fuente (PDF/HTML del DOF) | Archivar | Archivado completo en `.../llave2-decreto-scratchpad-2026-09-20/scratchpad/`, nombres originales preservados |
| `marco-produccion-total` | Mismo patrón que autoridad-semantica-marco-cobertura-total | Descartar | Sin acción |

Ningún archivo cruzó patrón de ola reservada (`encig25*`, `enif2024*`, `envipe2025*`,
`eder2025*`) en NOMBRE — no se abrió contenido bajo esa sospecha.

## Suite y estado del clon

Corrida `--baseline --parallel`: **ROJO transitorio** (10 FAIL nuevos, luego 3, luego 0) —
basenames genéricos de los propios insumos archivados (`README.md`, `SHA256SUMS.txt`,
`commits.txt`, `diff-contra-origin-main.patch` repetidos entre directorios) colisionaban con
`tests/check.py::t02_duplicates`, que compara por basename normalizado, no por ruta. Corregido
prefijando cada archivo con su slug+fecha (mismo patrón que `pisos-enif2021-0002-rama-codex/` y
`motral2015-prioridades/`); un `.schema.json` byte-idéntico a uno ya trackeado en `main` se dejó
de duplicar en vez de exceptuarlo en `tests/check.py`. **VERDE** al cerrar (0 FAIL nuevos, 22 WARN
preexistentes sin relación con este acto). `git -C /home/pc0/Modelado-Mexicano rev-parse
--is-shallow-repository` → `false`.

## Conteo final

```
$ git -C /home/pc0/Modelado-Mexicano branch | wc -l
39
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
33
$ git -C /home/pc0/mm-adq branch | wc -l
7
$ git -C /home/pc0/mm-adq worktree list | wc -l
2
```

## Lo que queda y por qué (tabla completa)

| Categoría | Modelado-Mexicano | mm-adq | Razón |
|---|---|---|---|
| Actos vivos con worktree (incl. 3 EN-VUELO, `acto/gen2-celda-d-piloto-3-*` de `pc0-77`/PR #924/#926, `acto/gen2-din-credito-comparabilidad-texto-1` de otra sesión concurrente, `acto/gen2-limpieza-ramas-locales-4` de este acto, y actos previos aún no cerrados) | ~14 | 0 | Trabajo en curso, fuera de perímetro |
| `codex/*` <24h (11 del grupo 2 + `codex/optimiza-verificacion-ci-prueba-compuerta`) | 12 | 0 | Regla de 24h — candidatas mecánicas mañana |
| Rechazadas por `branch -d`, contenido verificado redundante o propio real (F-A/F-B/F-C) | 5 | 3 | `FP-402`/`NC-0423`, decisión de mesa pendiente |
| `acto/gen2-celda-d-piloto-2` (heredada de `#910`, nunca resuelta) | 1 | 0 | Pendiente de que alguien haga `git checkout main && git branch -d` en el clon base — fuera de perímetro de este acto |
| Worktrees sucios con decisión de mesa (viven, no se tocan) | 4 | 0 | 2 archivados, 2 descartados sin acción — mesa no autorizó tocar el worktree en sí |
| `claude/tramite-2026-09-17` (branch huérfana del clon base, ya no checked out) | 1 | 0 | No estaba en ninguna lista de borrado |
| `main` (rama local, distinta de `origin/main`) | 1 | — | Excluida por regla propia desde `#910`, nunca por rótulo |
| `worktree-agent-*` (infraestructura de Claude Code, `.claude/worktrees/`) | 3 | 0 | Ajenas al inventario del proyecto, ~5 días de antigüedad, mismo commit las 3 — fuera de perímetro, no autorizadas para borrar aquí |
| Automatización ADQ (worktrees `/tmp/modelado-deriva-*`, mid-cycle) | — | 1–2 (fluctúa) | Pipeline vivo, no tocar |
| `mm-adq` (HEAD desprendido, propio clon) | — | 1 | El clon en sí |

## NO-CORRIDO / RESERVAS

- `NC-0423`: `git branch -D` sobre las 6 ramas rechazadas por `-d` — `DECISION-DE-MESA-PENDIENTE`.
  Sucesor: `FP-402`.

Ninguna otra pieza del encargo quedó sin correr.

## CONSUMIDO

Este cierre consume `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-4.md`.
