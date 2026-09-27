# ENCARGO · ACTO GEN2-TUBERIA-CI-TIEMPO-1 · La suite ya no cabe en diez minutos y GitHub cancela los checks: hoy se destraba subiendo los topes, y en el mismo acto se reestructura para que un PR corra solo lo que toca (< 8 min) y `main` corra la línea base completa (< 25), con tiempos medidos por paso

> ENTORNO: **NUBE** — `.github/workflows/`, `tests/check.py`, `tools/ci_guardias.py`. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `8f4b2419` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; contadores propios: minutos por job y por paso en PR y en `main`, antes/después, leídos de los logs de Actions y pegados. **Ningún test se relaja ni se borra**: cambia cuándo corre, no qué exige.

## 1 · OBJETIVO
- **COMMIT-A (destrabar, primero y por separado):** `timeout-minutes` de `suite` y `adicionales` a 30 (como `guardias`); `check` sigue en 1 (solo agrega). PR chico, merge de mesa, y la cola vuelve a correr. Esto no arregla el tiempo: lo tolera.
- **COMMIT-B (medir):** tabla paso × duración desde los tres últimos runs completos de `main` y de un PR (logs de Actions por id). Qué pesa: `check.py --baseline` entero, las series T con `glob('**/*.*')` (líneas 275 y 578 de `tests/check.py`: dos recorridos completos del árbol por corrida), `T-REPRO` sobre las 287 corridas, los pytest de `adicionales`, la instalación (ya con `uv`).
- **COMMIT-C (por evento):** en `pull_request`: `check.py --rapido` + `ci_guardias` + los tests de pytest afectados por las rutas del diff (`paths-filter` o `git diff --name-only` → mapa ruta→tests declarado en `tools/ci_guardias.py`) + `T-REPRO --lote` **solo sobre las corridas que el PR toca** (`lote_desde_asientos.py` ya existe para el canal); en `push` a `main` y en `schedule` nocturno (03:00 −06:00): `check.py --baseline --parallel` completo + `pytest -n auto`; en `merge_group`: lo mismo que PR. El check requerido por el ruleset sigue llamándose `check` en todos los eventos (no cambia la protección de `main`). Un PR que toque `tests/check.py`, `tools/corrida0.py` o `.github/` corre la línea base completa aunque sea PR (guardia por ruta).
- **COMMIT-D (rapidez real):** inventario de archivos del árbol calculado una vez por corrida y cacheado en memoria (o `git ls-files` en vez de `glob` recursivo, que además respeta `.gitignore`); `pytest-xdist` (`-n auto`) en `adicionales` y en la línea base; `actions/cache` para `uv` y para el inventario de `data/corrida0/*/sello.json` (llave = sha del árbol de `data/corrida0`); tiempos antes/después.
«Hecho» sobre el commit final con origin/main fusionado: un PR de prueba con un cambio de una línea en `docs/` termina `check` VERDE en **< 8 min** (run citado); el push a `main` correspondiente termina `check` VERDE en **< 25 min** (run citado); la corrida nocturna existe y su primer run se cita; tabla paso × duración antes/después en la nota; 0 tests eliminados o marcados `skip` (diff de `tests/` sin `skip`/`xfail` nuevos salvo los ya existentes); `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
D4-A y R(a) (el check `check` es el requerido; auto-merge para rutinas), D-14 (cada paso declara qué defecto evita: aquí, la cancelación por tiempo observada el 26/sep), D-16 (la suite adjudica por FAIL; los conteos se derivan), D-23 (una herramienta de verificación no muta el clon). **Mesa, 26/sep (chat):** «Los CI están pasando 10 minutos y se están cancelando».

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`8f4b2419`) `verify.yml`: jobs `suite` (10 min, `check.py --baseline --parallel`), `adicionales` (10), `guardias` (30), `preflight-calc` (10), `guardas-res` (10), `enrutamiento-pr` (5), `check` (1, agrega); disparo en `push`, `pull_request`, `merge_group`, `workflow_dispatch`; 302 archivos de tests, 1 560 tests; `check.py` recorre `**/*.*` en dos sitios; `uv` ya instalado; sin `-n auto`; sin `schedule`; `automerge-rutinas.yml` aparte. `[REPORTADO]` por mesa: cancelaciones a los 10 minutos en varios PR hoy. `[SUPUESTO]` que el mayor costo es `check.py --baseline` (T-REPRO × 287 + globs); COMMIT-B lo confirma antes de COMMIT-D.

## 4 · YA HECHO / YA DECIDIDO
CABLEADO-SESIONES-1 (#1165) dejó `-n auto` diferido a `ci_guardias` y `uv.lock`: verificar qué entró (`grep -n 'xdist\|-n auto' tools/ci_guardias.py .github/workflows/verify.yml`) y no repetir. TABLERO-EN-CANAL-1 subió el job de derivados a 30 min: se conserva.

## 5 · PIEZAS
A (PR aparte, hoy) → B → C → D → prueba de «Hecho».

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 + AMPLITUD
1–7 verbatim. Cómo se calcula «tests afectados» (mapa declarado o `pytest --lf`+rutas), umbrales de tiempo, hora del nocturno: tuyos, declarados. Si COMMIT-B muestra que el cuello es otro, se ataca ese y se dice. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) borrar, `skip` o relajar un test; cambiar el nombre del check requerido; tocar sellos o vistas · c) no aplica · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«Ningún test se elimina ni se relaja; solo cambia el evento en que corre; la línea base completa corre en cada push a `main` y cada noche» protege: **congelar** (D-16: la suite sigue adjudicando por FAIL sobre el commit final con `origin/main` fusionado). «Guardia por ruta: PR que toca CI o `check.py` corre todo» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml`, `tests/check.py` (solo inventario/caché y `--lote`; no aserciones), `tools/ci_guardias.py` (mapa ruta→tests, `-n auto`), `requirements-dev.txt`/`pyproject.toml` (xdist), nota, L0, cascada. Ajeno: `automerge-rutinas.yml` (salvo que dependa del nombre del check: se conserva), tests individuales, `corrida0.py`, medidores. En vuelo: las tres rutinas de hoy (censo, adq, derivados) esperan este COMMIT-A; ASTRA-6 (no toca CI).

## 10 · LO QUE NO HACE · SUCESORES
No cambia qué se verifica. Sucesor: `-2` si el nocturno revela un FAIL que el PR no vio (se abre NC y se ajusta el mapa ruta→tests).

## NO-CORRIDO / RESERVAS

| qué (del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| COMMIT-C: PR corre `--rapido` + ci_guardias + pytest afectados (mapa ruta→tests) + `T-REPRO --lote`; merge_group igual | SUSTITUIDO-POR:GEN2-TUBERIA-CI-TIEMPO-1/COMMIT-D — la línea base completa, medida en 4m50s, corre en todo evento; absorbe el objetivo de tiempo y no deja huérfano nada | ninguno | GEN2-TUBERIA-CI-TIEMPO-2 si pasa de 8 min |
| COMMIT-D: inventario cacheado / `git ls-files` | DIFERIDO-A:GEN2-TUBERIA-CI-TIEMPO-2 — globs medidos ≈2.9 s; D-14 | ninguno | GEN2-TUBERIA-CI-TIEMPO-2 |
| COMMIT-D: `pytest -n auto` en adicionales y línea base | SUSTITUIDO-POR:GEN2-TUBERIA-CABLEADO-SESIONES-1 — guardias ya usa `-n auto`; adicionales no invoca pytest; línea base usa spawn | ninguno | SIN-ASIGNAR |
| COMMIT-D: `actions/cache` | DECISIÓN-DE-MESA-PENDIENTE — verify.yml declara cero actions del marketplace; uv mide 2–5 s; recomendación: no | ninguno | SIN-ASIGNAR |
| «Hecho»: run de push a main < 25 min y primer nocturno citados | NO-VERIFICABLE-AQUÍ — existen solo tras el merge de mesa | sin cita hasta el merge | GEN2-TUBERIA-CI-TIEMPO-2 o trámite |
| Bajar el piso T32-quater (≈4 min) cacheando `_filas_registro` | FUERA-DE-PERÍMETRO — `tools/corrida0.py` es ajeno; pieza de GEN2-TUBERIA-CI-TIEMPO-2 | la suite no baja de ≈4 min | GEN2-TUBERIA-CI-TIEMPO-2 |

Filas `NC-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-01..06` en `forense/no-corrido.tsv`.

## CONSUMIDO

Consumido por Josanoforo/Modelado-Mexicano#1186 (COMMIT-A, fusionado) y Josanoforo/Modelado-Mexicano#1187 (COMMIT-C, COMMIT-D y cierre). ADR `ADR-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-01`; nota `forense/notas/nota-2026-09-27-gen2-tuberia-ci-tiempo-1.md`.
