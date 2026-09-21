# INFORME · ACTO GEN2-TUBERIA-CI-MEDICION-1 · Cuánto tarda de verdad el CI en GitHub

Fecha: 21/sep/2026. Base: `8535a977c9fe42b20465f74cd9ccc10f2b98cdd3` (origin/main
al abrir; el encargo se redactó contra `13129c05`, main se movió, no fue
PARO). Worktree: `/home/pc0/mm-gen2-tuberia-ci-medicion-1`, rama
`acto/gen2-tuberia-ci-medicion-1`. ENTORNO: CAJA (`gh auth status`: logueado
como `Josanoforo`; `gh api rate_limit` → `core.limit=5000` al abrir, no 60 —
confirma que no corre en la nube). Sólo lectura sobre GitHub: ningún
workflow se relanzó, canceló ni disparó; ningún test, workflow, `check.py`
ni `acto.md` se tocó.

**FALSADOR (§10 del encargo), verificado primero.** La lista trae **3**
recomendaciones de abaratar/eliminar (no cero) y **ninguna** de las cinco
metas de dirección se cumple hoy en el runner (ver tabla siguiente) — el
falsador no se dispara: el diagnóstico de dirección se sostiene con
evidencia fresca, no se hereda de memoria.

## Las cinco metas de dirección, medidas hoy

| Meta | Objetivo | Medido hoy | Cumple |
|---|---|---|---|
| Trabajo posterior a CONSUMIDO (mediana) | ≤ 10 min | 39 min (TUBERÍA, EJECUTADO, antecedente no re-derivado aquí — este acto mide CI, no arqueología de PR) · complementario propio: PR creado→fusionado, mediana **56.2 min**, p90 570 min (83 PR, incluye espera de mesa, no sólo ciclo de re-fusión) | **NO** |
| PR con renumeración | 0 | TUBERÍA: 29/78 · propio (grep de mensajes de commit por `renumer`): **26/83 (31.3%)** | **NO** |
| PR con dos o más re-fusiones de main | < 10% | TUBERÍA: 35/78 (44.9%) · propio (commits `Merge branch main`): **18/83 (21.7%)** — ver nota metodológica abajo | **NO** |
| Suite local | ≤ 60 s | **93.5 s** real (`--baseline --parallel`, VERDE, este acto, commit 8535a977) · TUBERÍA midió 189 s pero **sin** `--parallel` y en 1 núcleo — no es la misma medición | **NO** |
| Ejecuciones de la suite por cierre | 1 | **hasta 6** núcleos de `check.py` por cierre sin re-fusión: 3 invocaciones top-level (`acto.md`:351 dentro de `cierre_acto.py` Fase A, :384, :456) × 2 (T16 relanza el núcleo una vez por invocación) | **NO** |

**Nota metodológica (P4).** El conteo propio de re-fusiones cuenta commits
de mensaje `Merge branch 'main'…`; un PR resincronizado por *rebase* +
force-push no deja ese commit y no se cuenta, así que la cifra propia es un
**piso**, no el total — la brecha con la cifra de TUBERÍA (76.9% vs 51.8%
con ≥1) probablemente viene de ahí, no de que TUBERÍA se equivocara. Las
dos cifras se citan, ninguna se descarta.

## P0 · Sonda de acceso

```
$ gh auth status
✓ Logged in to github.com account Josanoforo — token scopes: gist, read:org, repo, workflow
$ gh api rate_limit --jq .rate
{"limit":5000,"used":7,"remaining":4993,...}
```
Sin PARO-ENTORNO. Ningún token se escribió en disco, en el repo ni en un log.

## P1 · El universo de corridas

`gh api repos/Josanoforo/Modelado-Mexicano/actions/workflows/verify.yml/runs`
paginado, filtro `created:>=2026-09-18`, 21/sep ~15:00 UTC. Script:
[`p1_recolecta_runs.py`](p1_recolecta_runs.py). Salida cruda:
[`runs.json`](runs.json) (330 objetos) · [`universo-corridas.tsv`](universo-corridas.tsv).

**330 corridas examinadas, 330 leídas (0 NO-ACCESIBLE).**

| conclusión | n |
|---|---|
| success | 208 |
| failure | 75 |
| cancelled | 47 |

| evento | n |
|---|---|
| pull_request | 235 |
| push | 83 |
| workflow_dispatch | 12 |

Rango: `2026-09-18T14:41:00Z` → `2026-09-21T15:03:43Z`.

## P2 · Jobs y pasos

Script: [`p2_recolecta_jobs.py`](p2_recolecta_jobs.py) (jobs+pasos de las
330 corridas, `gh api .../actions/runs/{id}/jobs`) →
[`jobs.json`](jobs.json), [`jobs-pasos.tsv`](jobs-pasos.tsv) (8547 filas).
**330/330 corridas con jobs leídos, 0 NO-ACCESIBLE.**

**Hallazgo no anticipado por el encargo: `verify.yml` cambió de arquitectura
tres veces en la propia ventana medida** (18 modificaciones al archivo desde
el 18/sep, `git log --since=2026-09-18 -- .github/workflows/verify.yml`).
Agrupar por nombre de job sin más mezclaba un job `check` monolítico viejo
(hacía TODO en un solo job, hasta el 20/sep ~02:00) con el job `check` de
compuerta rápida de hoy (1 paso, ~3-24 s) — mismo nombre, funciones
opuestas. Corregido agrupando por la FIRMA real de jobs de cada corrida
(script [`p2b_analiza_por_era.py`](p2b_analiza_por_era.py) →
[`censo-eras-verify.tsv`](censo-eras-verify.tsv)):

| era | n corridas | primera vista | última vista |
|---|---|---|---|
| ERA1 — un solo job `check` (monolítico) | 166 | 18/sep 14:41 | 20/sep 02:17 |
| ERA2 — `suite`+`adicionales`+`check` (sin `guardias`) | 61 | 20/sep 02:00 | 20/sep 14:28 |
| ERA3 — + `guardias` | 97 | 20/sep 05:33 | 21/sep 14:16 |
| ERA4 — + `preflight-calc` (PR #948, actual) | 5 | 21/sep 06:19 | 21/sep 15:03 |
| ERA0 — cancelada antes de programar ningún job | 1 | 19/sep 23:23 | — |

Las eras ERA2 y ERA3 se solapan en el tiempo (una corrida de PR con base
vieja corre con el `verify.yml` de su propia rama hasta re-fusionar main —
la causa exacta que el mandato de este acto describe).

**Duración de corrida completa** (success/failure, n=283, todas las eras,
[`duracion-por-corrida.tsv`](duracion-por-corrida.tsv)): mediana **198 s**,
p90 **286 s** (consistente con el antecedente de PR #901: medianas
"165 s suite / 160 s adicionales en paralelo" ≈ 172 s de corrida completa,
mismo orden de magnitud). Espera inicial (creación → primer job en
marcha), n=329: mediana **3 s**, p90 **17 s** — GitHub no es el cuello de
botella de arranque.

**Job que fija la ruta crítica hoy (ERA3/4,** [`duracion-por-job-por-era.tsv`](duracion-por-job-por-era.tsv)**):**

| job | mediana s | p90 s |
|---|---|---|
| adicionales | 159-167 | 217-220 |
| suite | 121-204 | 171-207 |
| guardias | 50-57 | 58-60 |
| preflight-calc | 14 | 15 |
| check (compuerta) | 3 | 4 |

`adicionales` es hoy el job más lento de los que corren en paralelo — más
que `suite`, que es el que tiene fama de caro. Coincide con el antecedente
de PR #901 ("adicionales ~160 s"), no se ha movido.

**Paso más caro (ERA3,** [`duracion-por-paso-por-era.tsv`](duracion-por-paso-por-era.tsv)**):**

| job | paso | mediana s | p90 s |
|---|---|---|---|
| adicionales | marcador por segmento — tabla derivada y guardias | **136** | **149** |
| suite | Suite de verificación (`tests/check.py`) | 109 | 171 |
| guardias | Guardias huérfanas — censo + invocador | 37 | 44 |
| adicionales | métrica rectora — celdas_validadas | 36 | 45 |

El paso del marcador (134 s medido por PR #901 el 20/sep) sigue en 136 s
hoy: nadie lo ha tocado desde entonces.

## P3 · Tests en el runner

Universo: todo job con el paso `Suite de verificación (modo línea base —
verde = no empeoraste)` y conclusión completa (success/failure) —
**283 de 283 leídos, 0 NO-ACCESIBLE** (no es muestra: es el universo
completo de corridas completas, declarado por volumen manejable dentro del
rate limit). Script: [`p3_descarga_logs.py`](p3_descarga_logs.py) (baja
cada log via `gh api .../jobs/{id}/logs`, extrae `[tiempo]` y `[FAIL]` sin
persistir el log completo) →
[`tiempos-tests-runner.tsv`](tiempos-tests-runner.tsv) (6995 filas),
[`fallos-tests-runner.tsv`](fallos-tests-runner.tsv) (722 filas).

**Límite declarado (A.13):** la instrumentación `[tiempo]` por test la
introdujo el commit `01b35f9f` (19/sep 19:59 -06 = 20/sep 01:59 UTC — el
mismo commit que separó `suite`/`adicionales`, PR #901). Las 166 corridas
de ERA1 (antes de ese commit) no imprimen esas líneas: el desglose test por
test cubre **140 corridas** (ERA2-4 tras el commit), no las 283. Los
fallos por test sí cubren las 283 (`[FAIL]` existe desde antes) — 408 en
job `check`-ERA1, 314 en job `suite`-ERA2-4.

**Los 5 tests más caros en el runner** ([`tiempos-tests-runner-agg.tsv`](tiempos-tests-runner-agg.tsv), n=140):

| test | mediana s | p90 s |
|---|---|---|
| T16 T-SUITE-SELF-CHECK | 61.4 | 87.7 |
| T32 T-CORRIDA0 | 39.4 | 65.7 |
| T32-quater T-PINES-MESA (n=21, recién nacido) | 28.4 | 29.9 |
| T35 T-REPRO | 7.8 | 25.2 |
| T45 T-LEGACY-DESGLOSE-SUMA | 6.7 | 7.4 |

**Tests que atraparon algo en CI en la ventana medida** ([`fallos-tests-runner-agg.tsv`](fallos-tests-runner-agg.tsv)):
15 de 53 tests fallaron al menos una vez. Los dos con más fallos —T06
(282) y T08 (282)— son **FAIL heredados y aceptados en baseline** (FP-293:
"nota de aceptación, no fix"; confirmado: fallan también en la corrida
local de este acto, VERDE por `--baseline` de todas formas) — no son
señal de que el CI "atrape algo nuevo", son ruido de baseline. Descontados
esos dos, el resto **sí es señal real**: T16 (66 veces, 55 en rama de PR),
T02 (51, 40 en PR), T22 (10, 8 en PR), T27 (6, 6 en PR), T30/T25/T26-bis
(4 cada uno, todos en PR), y siete más con 1-3 fallos cada uno. **44 de las
45 corridas de PR que hicieron fallar `T06`/`T08`-descontados atraparon
algo ANTES de fusionar** — el patrón dominante es exactamente el que
justifica tener la suite en CI.

## P4 · Espera de CI por PR

83 PR fusionados desde el 18/sep (`gh pr list --state merged --search
"merged:>=2026-09-18"`; TUBERÍA midió 78 — la diferencia son PR fusionados
entre esa medición y ésta). Script:
[`p4_espera_por_pr.py`](p4_espera_por_pr.py) →
[`espera-ci-por-pr.tsv`](espera-ci-por-pr.tsv) (83/83 con ≥1 corrida
indexada por rama, 0 sin indexar). Complemento propio
[`p4b_refusiones_por_pr.py`](p4b_refusiones_por_pr.py) →
[`refusiones-por-pr.tsv`](refusiones-por-pr.tsv).

- Corridas por PR: mediana 3, algunos con 8+ (cada empuje relanza y
  cancela el anterior — `cancel-in-progress: true`).
- Tiempo de reloj sumado de CI por PR: variable, cola larga (p90 muy por
  encima de la mediana — ver TSV completo).
- PR creado → fusionado: mediana **56.2 min**, p90 **570 min** (esto
  incluye espera de mesa, no sólo el ciclo CI — se declara como métrica
  complementaria, no como sustituto de "trabajo posterior a CONSUMIDO").

## P5 · La lista del barrido

**151 filas en total**, en cuatro tablas (universo declarado en cada
script; ninguna es muestra):

| tabla | filas | script |
|---|---|---|
| [`barrido-check-tests.tsv`](barrido-check-tests.tsv) | 53 (los 53 tests que `tests/check.py` registra hoy, incluido T16 — el encargo decía 54; recontado mecánicamente, `awk '/^def main/,/^if __name__/'`, da 53: 52 base + T16 condicional) | [`p5_ensambla_barrido.py`](p5_ensambla_barrido.py) |
| [`barrido-verify-steps.tsv`](barrido-verify-steps.tsv) | 37 (todos los pasos del `verify.yml` vigente hoy) | [`p5b_ensambla_barrido_verify.py`](p5b_ensambla_barrido_verify.py) |
| [`cascada-acto-md.tsv`](cascada-acto-md.tsv) | 17 (4 guardas de ARRANQUE + 13 pasos de CIERRE) | curado a mano contra `.claude/commands/acto.md` |
| [`no-cableados-44.tsv`](no-cableados-44.tsv) | 44 (36 NECESITA-DEPENDENCIA + 8 FALLA-DE-VERDAD del censo — el encargo decía 134 archivos en el censo; recontado, son 135: 91 CORRE-EN-CI + 36 + 8) | [`p5c_ensambla_no_cableados.py`](p5c_ensambla_no_cableados.py) |

**Recomendaciones, por tabla:**

| recomendación | n | dónde |
|---|---|---|
| ELIMINAR | 1 | T16 T-SUITE-SELF-CHECK (decisión ya tomada por dirección; evidencia aportada aquí) |
| ABARATAR | 2 | paso "marcador por segmento" (job propio); paso 1 de la cascada (saltar el `check.py` interno de `cierre_acto.py` cuando hay VERDE reciente) |
| FUERA-DE-ALCANCE | 6 | T06-T11, reglas de contenido §3, excluidas por el propio encargo |
| DEFECTO-ABIERTO-NO-SE-TOCA-AQUI | 8 | los 8 FALLA-DE-VERDAD del censo — activos, con dueño sin asignar, PARO de este acto prohíbe tocarlos |
| MANTENER / MANTENER-SIN-CABLEAR | 134 | el resto |

Ninguna recomendación de eliminar toca algo que proteja abrir dato,
congelar spec, adoptar o borrar (regla del encargo). T-REPRO se mantiene
sin abaratar más (ya se abarató una vez, PR #901).

## P6 · Ahorro estimado

| recomendación | ahorro por corrida | ahorro por acto | base |
|---|---|---|---|
| ELIMINAR T16 | 61.4 s mediana / 87.7 s p90, por cada invocación de `check.py` (CI o local) | ≥ 2 invocaciones obligatorias por cierre (pasos 6 y 12 de `acto.md`) → **123-175 s por acto como piso**, más si hay re-fusión o si la sesión corrió el núcleo antes de cerrar | tiempos-tests-runner-agg.tsv + tiempos-locales-run1.tsv |
| ABARATAR "marcador por segmento" → job propio | 20-70 s en la ruta crítica de **cada** corrida de `verify.yml` (max(suite,adicionales) baja de ~159-220 s a ~136-149 s) | mismo ahorro × corridas que dispara el acto (mediana 3 por PR, más con re-fusión) | duracion-por-job-por-era.tsv, duracion-por-paso-por-era.tsv |
| ABARATAR paso 1 de la cascada (saltar `check.py` interno si hay VERDE reciente) | n/a (paso local, no de CI) | 60-200 s por cierre (1 de hasta 3 invocaciones del núcleo) | tiempos-locales-run1.tsv |

Los tres juntos, en el caso más favorable (un cierre sin re-fusión, dos
invocaciones de CI): **≈ 200-450 s de reloj por acto** entre CI y sesión
local — no cierra la brecha completa contra la meta de "≤ 10 min tras
CONSUMIDO" por sí solo (el mandato ya lo señala: el ciclo re-fusionar →
renumerar → re-correr es sistémico, no un test suelto), pero es la parte
que este acto puede cuantificar con evidencia de runner real, no
estimación.

## P7 · Cierre

Cascada de `/acto` en curso en el commit de cierre de este mismo PR;
`tests/check.py --baseline --parallel` VERDE (93.5 s, este acto,
`8535a977`) antes de escribir este informe. `## NO-CORRIDO / RESERVAS` y
`## CONSUMIDO` van en el encargo archivado
(`forense/encargos/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1.md`), no aquí.

## Hallazgos que no bloquean pero se declaran (A.13/regla de señal)

1. **La premisa "54 tests, incluido T16" de TUBERÍA no calza**: son 53
   (52 registrados + T16 condicional). Diferencia de uno, sin impacto en
   ninguna pieza — se corrige aquí, no se repite en `hallazgos.md` aparte
   (D-14: no vale la pena instrumentar una verificación para esto).
2. **La premisa "134 archivos" del censo no calza**: son 135
   (91 CORRE-EN-CI + 36 + 8). Mismo trato.
3. `verify.yml` cambió de arquitectura de jobs 3 veces en 3 días de
   ventana medida (18 commits al archivo) — el propio aparato de CI es tan
   inestable como el ciclo que el mandato describe. No es un hallazgo
   nuevo que este acto deba resolver (fuera de perímetro: no se toca
   `verify.yml`), pero contextualiza por qué "cuánto tarda el CI" no tiene
   una sola respuesta esta semana.
