# GEN2-LIMPIEZA-RAMAS-LOCALES-3 · PARO-PREMISA en P0

**Rama:** `acto/gen2-limpieza-ramas-locales-3` · **HEAD de arranque:** `8b7b0562` (merge de `#913`, `origin/main`) · **Entorno:** caja (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir) · **Compuerta declarada:** `#913` en `main` — verificada: `gh pr view 913` → `state=MERGED`, `mergedAt=2026-09-20T20:50:48Z`, `baseRefName=main`. Cumplida.

## Qué pedía P0

> "git bundle verify de los dos bundles y sha256 contra #913. El clon ya no es superficial (--is-shallow-repository → false): confírmalo; si volvió a serlo, PARA — toda la clasificación depende de eso."

## Qué se verificó

- **Bundles.** `/home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle` y `-mm-adq.bundle`: `git bundle verify` en ambos → `The bundle records a complete history.` sha256 recalculado en los dos coincide byte a byte con el registrado (`34c39bfa…` y `0e38bdca…`, los mismos prefijos que cita la firma de mesa). **Este subpaso pasa.**
- **Superficialidad del clon.** `git -C /home/pc0/Modelado-Mexicano rev-parse --is-shallow-repository` → **`true`**. `.git/shallow` existe (`ls -la` → modificado `Sep 20 14:44`, 369 bytes, 5+ SHA de commit-frontera). `mm-adq` (el segundo clon real de la caja, ver `feedback_p0_home_git_y_mm_adq_son_casos_especiales`) da `false` — no es el mismo caso. **Este subpaso NO pasa.**

El propio texto del encargo hace de este segundo hecho una condición de parada explícita, no una observación a documentar y seguir: *"si volvió a serlo, PARA — toda la clasificación depende de eso."* Un clon superficial rompe `git cherry origin/main <rama>` y cualquier comparación de árbol/merge-base sobre historia que caiga fuera de la ventana superficial — exactamente el mecanismo que P1 (re-derivación cubeta por cubeta) y P3 (timestamps de commit de dos ramas, comparación contra `origin/main`) necesitan para no clasificar mal. Clasificar mal aquí es irreversible: `git branch -D` no tiene deshacer limpio sobre una rama que en realidad no estaba fusionada.

## Decisión

**PARO-PREMISA.** No se ejecuta P1 (sin re-derivación confiable no hay `branch -D`), no se ejecuta P2 (el rescate de MOTRAL depende de que `914e92f3` sea alcanzable con historia completa — no se verificó bajo esta condición), no se ejecuta P3 (el dictamen de la colisión `CALC-PISOS-ENIF2021-EJES-0002` compara timestamps de commit entre dos ramas — el mismo tipo de comparación que un clon superficial puede sesgar). Cero commits sustantivos, cero borrados, cero archivos tocados fuera de esta nota, el encargo archivado (0-bis) y la cascada de cierre.

No se intentó `git fetch --unshallow` para "arreglarlo y seguir": el texto de la firma anticipa exactamente este caso ("si volvió a serlo") y lo resuelve con PARA, no con una receta de reparación silenciosa — la disciplina de este proyecto (`ADR-224`/`ADR-234`, ver también el precedente de `#913`/`LIMPIEZA-2` con compuerta falsa) es que un ejecutor no decide por sí mismo pasar por encima de una condición de parada escrita; esa decisión es de mesa.

## Para el sucesor inmediato

1. `git -C /home/pc0/Modelado-Mexicano fetch --unshallow` (operación aditiva, no destructiva) y re-confirmar `--is-shallow-repository → false` de forma estable antes de re-lanzar.
2. Vale la pena que mesa registre **por qué** este clon vuelve a quedar superficial entre actos — ya ocurrió una vez antes de `#910`/`#913` y ahora una segunda vez. Candidatos no verificados en esta sesión (fuera de perímetro de P0, no investigados): un `git clone --depth` corrido por algún proceso de la caja (el runner de `mm-adq`, un cron, otra sesión) contra este mismo directorio, o una reconfiguración de `fetch` con profundidad limitada. Si se repite una tercera vez, ese patrón en sí mismo es el hallazgo, no el síntoma.
3. Con el clon confirmado no-superficial, re-invocar `GEN2-LIMPIEZA-RAMAS-LOCALES-3` verbatim — su P0 de bundles (verify + sha256) ya quedó verificado en esta sesión y no necesita rehacerse; solo el subpaso de superficialidad.

## NO-CORRIDO / RESERVAS

Ver la sección homónima en `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-3.md`.
