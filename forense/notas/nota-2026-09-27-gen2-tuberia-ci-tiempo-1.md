# Nota de cierre · ACTO GEN2-TUBERIA-CI-TIEMPO-1 · 27/sep/2026

ADR: `ADR-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-01` (raíz `c6d9`, commit 0-bis `c6d9dd35`). Encargo: `forense/encargos/2026-09-26-GEN2-TUBERIA-CI-TIEMPO-1.md`, SHA de redacción `8f4b2419` = base al arrancar (0 commits de diferencia). ENTORNO: NUBE (hook: `ENTORNO-DERIVADO = NUBE`); cero microdato, cero red a INEGI.

Contadores movidos por este acto: **cero mediciones, cero adopciones**. Lo que sí se mueve: los minutos de CI por job y por paso (tabla abajo).

## PRs
- COMMIT-A → Josanoforo/Modelado-Mexicano#1186 (fusionado por mesa): `timeout-minutes` de `suite` y `adicionales` 10 → 30.
- COMMIT-C + COMMIT-D + cierre → Josanoforo/Modelado-Mexicano#1187.

## COMMIT-B · medición (EJECUTADO)

**Premisa `[SUPUESTO]` que cayó:** el costo no está en los `glob('**/*.*')`: T02+T03 miden ≈2.9 s entre los dos. El cuello es la re-derivación del registro de corrida0 (`_filas_registro` → `_lee_oferta`: 773 `yaml.load`, ≈50 s cada una con libyaml y ≈160 s sin ella), que se repite en serie dentro de cinco tests. Por latitud §6 («si el cuello es otro, se ataca ese y se dice») se atacó ese.

Paso × duración en Actions, antes del acto (LEÍDO de la API de jobs, run id citado):

| run | evento | suite (paso check.py) | adicionales | guardias (huérfanas) | total run | desenlace |
|---|---|---|---|---|---|---|
| 36284458043 | pull_request | 8m16s | 3m58s | 3m27s | 8m38s | success |
| 36285338474 | pull_request | 8m53s real (user 9m37s) | — | — | 9m19s | failure (FAIL de contenido, no tope) |
| 36282734145 | push main | 8m36s | 3m44s | 3m41s + deriva 14m57s | 19m37s | **cancelled** por concurrencia (merge de #1180) |
| 36285820233 | pull_request (COMMIT-A) | — | — | — | 7m40s | success |

Instalación con `uv`: 2–5 s por job; checkout: 10–25 s. No son cuello.

Perfil por test de `check.py --baseline --parallel` (EJECUTADO en réplica del runner: venv `uv --system-site-packages`, PyYAML 6.0.3 con libyaml, 4 CPU; comando `time python tests/check.py --baseline --parallel`):

| test | antes (s) | después (s) | dónde corre después |
|---|---|---|---|
| T32-quater T-PINES-MESA | 261.2 | 236.2 | proceso spawn |
| T32 T-CORRIDA0 | 151.0 | 151.6 | proceso spawn |
| T45 T-LEGACY-DESGLOSE-SUMA | 50.3 | 56.8 | proceso spawn |
| T35 T-REPRO | 48.7 | 58.7 | proceso spawn (ya lo estaba) |
| T36 T-CORREDORES-GEN2 | 17.7 | 23.8 | proceso spawn |
| **suite completa (real)** | **8m22s** | **4m05s** | — |

Dentro de T32, un solo caso (`t_status_arbol_real_no_cuenta_smokes`) cuesta 309 de 365 s sin libyaml: llama `status()` y `_filas_registro()` sobre el árbol real, dos derivaciones completas.

Equivalencia (EJECUTADO): marcas `[FAIL]/[warn]/[ ok ]` por test idénticas (`diff` vacío); salida completa sin líneas `[tiempo]` idéntica salvo una ruta `/tmp/tmp…` de un journal; `3 FAIL · 230152 WARN` y rc=0 en las dos. `tests/test_check_parallel.py` y `tests/test_suite_warn_estado.py`: OK sin tocarlos.

## COMMIT-C / COMMIT-D · lo que cambió
- `tests/check.py`: `_PESADOS_AISLADOS` (T32-quater, T32, T45, T36) se suman a T35 en el mismo `ProcessPoolExecutor` spawn; cada uno se consume en su posición original (baseline, orden de mensajes y T16 sin cambio). El test conserva lo que exige: solo cambia el proceso donde corre.
- `.github/workflows/verify.yml`: `schedule` nocturno `0 9 * * *` (03:00 UTC−6). En `push`/`schedule` el grupo de concurrencia pasa a ser el `run_id`: un merge nuevo ya no cancela el run de `main` en curso (el derivador de `guardias` tarda ≈15 min y moría así). `cancel-in-progress: true` se conserva (lo fija `test_check_parallel.py`); en PR sigue cancelando al run anterior del mismo PR. El nombre del check requerido `check` no cambia.
- En PR se conserva la **línea base completa**: medida bajo 8 min, reemplaza el recorte por rutas (ver NO-CORRIDO). Da cobertura mayor que el recorte y no deja un hueco que solo el nocturno vería.

## Después (CI)
Run 36287947294 (pull_request de #1187, head `f594ce26`, LEÍDO de la API de jobs): `suite` paso check.py **4m50s** (antes 8m16s–8m53s); run completo **5m15s**, `check` success (antes 7m40s–9m19s en PR). Criterio «PR < 8 min»: cumplido por este run; un PR de una línea en `docs/` recorre el mismo camino (no hay filtro por ruta). «Push a main < 25 min» y «primer nocturno»: solo existen después del merge (NC-…-c6d9-05).

## Hallazgos
- El defecto de `main` rojo del 26–27/sep no fue el tope: fue `cancel-in-progress` sobre el grupo `refs/heads/main`. COMMIT-A solo toleraba el síntoma de PR.
- El piso de la suite es ahora T32-quater (≈4 min): cinco derivaciones del registro dentro de `tests/test_pines_mesa.py`. Bajarlo exige cachear `_filas_registro` dentro de `tools/corrida0.py` (ajeno a este perímetro): sucesor `GEN2-TUBERIA-CI-TIEMPO-2`.
