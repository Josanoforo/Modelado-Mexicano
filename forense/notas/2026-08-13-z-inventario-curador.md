# ACTO Z · Inventario del clon Modelado-Mexicano-curador — 2026-08-13

1. Contenido único: **NINGUNO**. Los 590 commits "sin empujar" de `codex/curador-baseline-semantico` (`/home/pc0/Modelado-Mexicano-curador`) son historia pre-purga, no trabajo huérfano — no hay nada que rescatar.
2. Prueba de pre-purga: `git merge-base origin/main HEAD` → `9301e59 2026-07-29` — mismo ancestro común que los 6 refs `*-huerfana-20260813`.
3. `HEAD` de curador → `3d5f34c 2026-08-07` — misma ventana temporal pre-purga que las seis (tips del 6/ago).
4. `git diff --diff-filter=A --name-only origin/main HEAD | wc -l` → **0** — cero archivos que `main` no tenga.
5. `HEAD` (corto y completo) aparece exactamente 1 vez cada uno en `canon/remapeo-shas-purga-2026-08-10.tsv` (626 líneas, leído vía `origin/main` — el archivo no existe en el checkout de curador, anterior a la purga del 10/ago).
6. Misma firma que los seis huérfanos (590 commits sin empujar + `ancestor_of_origin_main=NO` = pre-purga con 0 únicos), confirmada por comando, no por analogía con lo que ACTO W declaró candidato. No se empuja rama de preservación: a diferencia de los seis (que vivían solo en un clon que el barrido no había visto), este worktree ya existe, conocido, en el clon base — no hay riesgo de pérdida que una preservación resuelva, y no hay contenido que preservar.
7. Se cierra aquí, per el criterio del encargo (`archivos_que_main_NO_tiene = 0`) — sin paso 2 ni 3. `tests/check.py` no aplica: este acto no edita datos ni código.

Contadores de medición: 0.
