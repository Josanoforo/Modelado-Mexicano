# GEN2-LIMPIEZA-RAMAS-LOCALES-5 · cierre

Encargo archivado verbatim en `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-5.md`.
Sesión CAJA (`pc0-0d`), Sonnet 5, `origin/main` al abrir = `1dfb6726` (merge de `#929`). Sin
sub-agentes de escritura ni cross-session: todo este acto se ejecutó directo, sin forks.

## P5 · A-MEDIAS — al frente, como pide el encargo

**Una fila. No sale vacía.**

### `acto/gen2-f5-recaptura-l` (worktree `/home/pc0/mm-gen2-f5-recaptura-l`)

- **Qué quería hacer el acto:** re-capturar el corredor L (bootstrap manual/humano de un duelo
  L-vs-M-vs-R) para las 4 celdas `CIV-M-01/02/04/10`, subiendo de 8 a 16 réplicas por celda
  (mismo `runner_l_cli.py`, mismo `L-spec-v1_2.json` — solo cambia el número de réplicas
  capturadas).
- **Hasta dónde llegó:** el re-captura se completó al 100%: las 28 filas `RES-*` de
  `data/corrida0/demanda-resultados.tsv` que citan `CAPTURA-CORREDOR` están TODAS actualizadas
  de "(8 replicas)" a "(16 replicas)" con valores nuevos de `celda_L` y de los tres marcadores
  `z_*` derivados en `AGREGADO`. El `mtime` del archivo (`2026-09-09 18:57:14`) es 52 segundos
  ANTES del último commit de la rama (`2026-09-09 18:58:06`, un merge de sincronización con
  `origin/main`) — la sesión terminó la recaptura, hizo un merge de housekeeping, y nunca
  comprometió el resultado. Lleva **11 días** sin commit.
- **Qué falta o qué se pierde:** falta literalmente un `git add data/corrida0/demanda-
  resultados.tsv && git commit`, y decidir si esa recaptura de 16 réplicas necesita registro
  aparte (`corrida0.py`/`registro --escribe`) o si basta con el commit sobre `demanda-
  resultados.tsv`. Si se abandona: se pierde una remedición completa (no parcial) que dobla la
  precisión de captura del corredor L en las 4 celdas CIV-M del duelo — trabajo humano/manual de
  captura, no reproducible por script sin repetir la captura desde cero.

**Dos opciones:**
1. **Terminar** — encargo corto para la mesa dueña del duelo (`prereg-duelo-v2/`, la misma que
   firmó `ADR-207`/`ADR-208`/`ACTO MAESTRA30-E8` y sucesores): verificar que las 16 réplicas
   nuevas fueron capturadas correctamente (no son un artefacto de una edición a mano), comprometer
   el archivo, y decidir si el registro de `corrida0` necesita una fila nueva o una actualización
   de la existente. Bajo costo: el trabajo pesado (la captura) ya está hecho.
2. **Abandonar** — cerrar `NC-0429` con razón, archivar el diff de `demanda-resultados.tsv` como
   insumo externo (ya con procedencia: 8→16 réplicas, 9/sep/2026), y borrar la rama/worktree.
   Se pierde la remedición.

**Recomendación:** *Terminar* — es la opción barata (un commit, no una remedición desde cero) y
el trabajo humano de capturar 16 réplicas manualmente no es trivial de repetir. Pero **no lo hago
yo**: el encargo lo prohíbe explícitamente (§6, §10) y verificar que esas 16 réplicas son
genuinas (no una edición manual del TSV sin captura real detrás) exige juicio de quien conoce el
protocolo de captura, no de esta sesión de limpieza.

## P1/P2 · Inventario completo

### Modelado-Mexicano — con worktree

| Rama | Último commit | ¿En origin? | PR | Cherry vs main | Veredicto | Acción P3 |
|---|---|---|---|---|---|---|
| `acto/gen2-din-credito-comparabilidad-texto-1` | 20/sep 17:xx | SÍ | #932 OPEN | n/a | **EN-CURSO** | No tocar (mesa lo pidió explícito; ADR-571 candidato ya redactado ahí) |
| `acto/gen2-f5-recaptura-l` | 9/sep 18:58 (merge) | no | #669 MERGED | 0 propios | **A-MEDIAS** | Ver P5 arriba — no se toca |
| `acto/gen2-limpieza-ramas-locales-4-cierre-fp402` | 20/sep (hoy) | SÍ | #934 OPEN | n/a | **EN-CURSO** | Mío, activo — no tocar |
| `acto/gen2-limpieza-ramas-locales-5` | 20/sep (hoy) | SÍ | (este) | n/a | **EN-CURSO** | Mío, este acto — no tocar |
| `acto/gen2-reparacion-cierre-consolidacion-cron` | 16/sep | no | #813 MERGED | 0 | **CERRADO-FALTA-BORRAR** | `-d` intentado, **bloqueado**: worktree tiene `data/curacion-registro/cola-adquisicion-registro.tsv.lock` sin seguimiento (0 bytes, residuo de un lock de escritura, 16/sep) — no autorizado a `rm` sin firma |
| `codex/autoridad-semantica-enif` | 25/ago | no | ninguno | 0 | **CERRADO-FALTA-BORRAR** | Contenido sin commitear ya archivado en `main` vía `#929` (`forense/notas/insumos-externos/autoridad-semantica-enif-2026-09-20/`, con el hallazgo de que parece superado). `-d` **bloqueado**: worktree sigue sucio (2 trackeados modificados + 3 sin seguimiento), descartar ese contenido no está firmado aquí |
| `codex/gen2-encuci2020-respuesta-por-contacto-cli-2` | 19/sep | no | #891 MERGED | 0 | **CERRADO-FALTA-BORRAR** | `-d` **bloqueado**: `forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/controles-medidor.json` sin seguimiento (534B, diagnóstico desechable de una CALC ajena a esta rama — mismo archivo repetido en 3 worktrees, ver nota abajo) |
| `codex/gen2-issp2017-consistencia-apoyo-familiar-cli-2` | 19/sep | no | #892 MERGED | 0 | **CERRADO-FALTA-BORRAR** | `-d` **bloqueado**: mismo `controles-medidor.json` |
| `llave2-decreto` | 25/ago | no | #336 MERGED | 0 | **CERRADO-FALTA-BORRAR** | Contenido sin commitear ya archivado en `main` vía `#929` (`forense/notas/insumos-externos/llave2-decreto-scratchpad-2026-09-20/`). `-d` **bloqueado**: worktree sigue con `scratchpad/` sin seguimiento |
| `worktree-agent-a336d4013203d5b8e` | 15/sep | — | — | — | **INFRAESTRUCTURA** | Ajena (Claude Code, `.claude/worktrees/`), no tocar |
| `worktree-agent-a7d8e527ae88b7feb` | 15/sep | — | — | — | **INFRAESTRUCTURA** | ídem |
| `worktree-agent-a9facc03b479266d6` | 15/sep | — | — | — | **INFRAESTRUCTURA** | ídem |

**Nota sobre `controles-medidor.json`:** el mismo archivo de 534 bytes (controles de
`CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001`, todo `true`/booleanos triviales) aparece sin
seguimiento en al menos 3 worktrees distintos (`issp2017-consistencia`, `encuci2020-respuesta`, y
bloqueó también un intento sobre un tercero ya borrado). Es diagnóstico desechable — no hay
CALC sellado nuevo detrás, solo un chequeo de controles regenerable re-corriendo el medidor — pero
no está en la lista de residuo excepcionado por nombre (`__pycache__`, `.pytest_cache`, etc.), así
que bloquea `git worktree remove` sin `--force`, que este acto no tiene autorizado usar aquí.

### Modelado-Mexicano — sin worktree

| Rama | Último commit | ¿En origin? | Veredicto | Acción P3 |
|---|---|---|---|---|
| `codex/optimiza-verificacion-ci-prueba-compuerta` | 19/sep, ~22h de edad al medir | no | **EN-CURSO** | `<24h` (además: 1 commit propio real, "prueba temporal" en `.github/workflows/verify.yml`, sin PR) — se queda |
| `main` | — | — | **INFRAESTRUCTURA** | HEAD del clon, no se toca |

**Ya borradas en este acto (11 CERRADO-FALTA-BORRAR limpias):** `acto/gen2-c2-compuesto-ic-enif2024-1` (PR #911), `acto/gen2-c2-compuesto-ic-envipe2025-1` (PR #907), `acto/gen2-celda-d-piloto-3-commit-1-v1_1` (PR #926), `acto/gen2-celda-d-piloto-3-ejecucion` (PR #924), `acto/gen2-guardian-envipe-ejes-ic-1` (PR #916), `acto/gen2-limpieza-ramas-locales-1/2/3/4` (PR #910/#913/#923/#929), `acto/gen2-pisos-enif2021-formalidad-1` (PR #915), `acto/gen2-pisos-enut2019-ejes-1` (PR #908) — las tres que la nota de `#929` llamaba "EN-VUELO" resultaron, en este acto, ya fusionadas (la premisa de mesa de que solo faltaba esperar 24h ya no aplicaba: llevaban PR propio fusionado desde entonces). **Más 6 `codex/*` con PR propio fusionado** (#900, #897, #898, #899, #890, #901: eder2017, enadid2023, enfih2019, ensafi2023, wbes2023 — este último con el hallazgo ya conocido de `#910`/`#929` de `data/raw/` real con 5 symlinks, sin cambios, no se abrió contenido —, optimiza-verificacion-ci) y `codex/gen2-adq-registro-cierre-cli-2`/`enut2024-distribucion-horas-cli-2`/`motral2015-prioridades-prestaciones-cli-1-sync` (fusionadas mecánicamente, ≥24h, cherry limpio). Más las 2 huérfanas (`acto/gen2-celda-d-piloto-2`, `claude/tramite-2026-09-17`, `-d` desde `main`). Más `codex/autoridad-semantica-marco-cobertura-total` y `marco-produccion-total` (firma de mesa: symlink `.barrido2` retirado, worktree limpio, `-d` sin `--force`).

**Corrección a una premisa del encargo:** la clasificación de "12 codex/* < 24h" heredada de
`#929` estaba desactualizada — 7 de esas 12 ya tenían PR propio fusionado (más fuerte que el
cherry-check mecánico) y se procesaron como `CERRADO-FALTA-BORRAR` sin esperar el reloj de 24h,
porque el criterio real (PR fusionado) ya estaba satisfecho. Las 5 restantes siguen genuinamente
`<24h` sin PR: `codex/gen2-enadid2023-union-sexo-edad-cli-2` fue re-verificada aparte (fusionada,
PR #897) — de las 12 originales de `#929`, terminaron **9 con PR propio + 3 sin cambios** (el
resto del inventario de `#929` ya se había resuelto en actos previos).

### mm-adq

| Rama/worktree | Veredicto | Nota |
|---|---|---|
| `censo/2026-09-20` | **EN-CURSO/ajeno** | Automatización de hoy, perímetro ajeno (§9) |
| `codex/adq-2026-09-20` | **EN-CURSO/ajeno** | ídem |
| `main` (local) | **INFRAESTRUCTURA** | — |
| `/tmp/modelado-deriva-2026-09-20-*` ×2 | **INFRAESTRUCTURA/ajeno** | Worktrees de la rutina de adquisición, perímetro ajeno |

Ninguna rama de `mm-adq` se tocó en este acto (las de FP-402 ya se habían borrado en el acto
anterior).

## P3 · Mecánico ejecutado

- Bundles verificados íntegros antes de tocar nada: `git bundle verify` → "records a complete
  history" en los dos; sha256 idéntico al registrado en `#910` (`34c39bfa…dab48cb7` y
  `0e38bdca…5267d95284`). Compuerta cumplida.
- 11 + 9 = 20 ramas `CERRADO-FALTA-BORRAR` limpias borradas (worktree retirado sin `--force`,
  `data/raw` symlink o ausente en todas salvo `wbes2023-precision-interacciones-cli-2`, cuyo
  `data/raw/` real con 5 symlinks —hallazgo ya conocido, sin bytes de payload en riesgo— no
  bloqueó el retiro).
- 2 huérfanas del clon base borradas (`-d` desde `main`).
- 2 worktrees con symlink `.barrido2` retirado por firma de mesa, luego worktree + rama borrados
  (cherry limpio, 0 commits propios).
- 5 `CERRADO-FALTA-BORRAR` **no se pudieron borrar**: bloqueados por residuo sin seguimiento no
  cubierto por ninguna firma de este acto (`NC-0430`).
- 1 `A-MEDIAS` no tocada (`acto/gen2-f5-recaptura-l`, `NC-0429`).
- 4 `EN-CURSO` no tocadas (din-credito, las dos ramas propias de este carril de limpieza,
  optimiza-verificacion-ci-prueba-compuerta).
- 3 `INFRAESTRUCTURA` no tocadas.

## P4 · El día que falta

`forense/censo-raiz/2026-09-16.txt` restaurado con `git apply --include=... <parche archivado de
censo/2026-09-16>` — aplicó limpio contra `main`, sha256 `2d4f2837…f50017`. Procedencia: el
archivo vivía en el commit de la rama `censo/2026-09-16` (borrada en `GEN2-LIMPIEZA-RAMAS-
LOCALES-4-CIERRE-FP402`, PR pendiente de merge en el momento de este acto) y su diff completo
contra `origin/main` quedó archivado en `#929` como
`forense/notas/insumos-externos/censo-2026-09-16-2026-09-20/censo-2026-09-16-2026-09-20-diff-
contra-origin-main.patch` — de ahí se extrajo, no se re-generó ni se editó.

## Suite y estado del clon

VERDE (ver commit de cierre). `git -C /home/pc0/Modelado-Mexicano rev-parse
--is-shallow-repository` → `false`.

## Conteo final

```
$ git -C /home/pc0/Modelado-Mexicano branch | wc -l
14
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
13
$ git -C /home/pc0/mm-adq branch | wc -l
4
$ git -C /home/pc0/mm-adq worktree list | wc -l
3
```

## NO-CORRIDO / RESERVAS

- `NC-0429`: terminar o abandonar `acto/gen2-f5-recaptura-l` — `DECISION-DE-MESA-PENDIENTE`.
  Sucesor: `FP-403`.
- `NC-0430`: 5 `CERRADO-FALTA-BORRAR` bloqueados por residuo sin seguimiento no firmado para
  descartar — `DECISION-DE-MESA-PENDIENTE`.

## CONSUMIDO

Este cierre consume `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-5.md`.
