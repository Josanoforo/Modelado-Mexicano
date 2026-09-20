# ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-2 — PARO-COMPUERTA en ARRANQUE

Encargo verbatim: `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-2.md`. CABECERA: SHA de redacción `8a842afc`; COMPUERTA declarada: "PR #910 fusionado". **La compuerta no se cumple contra el árbol real. Cero commits sustantivos — P1 a P6 (el análisis de las 131 ramas CON-TRABAJO-PROPIO) no se ejecutaron.**

## ARRANQUE

- **Gate caja/nube:** `git -C /home/pc0/Modelado-Mexicano worktree list | wc -l` → 54. `ls data/raw | head -1` → `2005trim1_csv.zip` (corpus montado). CAJA confirmada.
- **0.c duplicado:** `git ls-remote --heads origin | grep -i limpieza-ramas-locales-2` → sin coincidencia (exit 1); `git worktree list | grep -i limpieza-ramas-locales-2` → sin coincidencia; `gh pr list --search "limpieza-ramas-locales-2" --state open` → sin PR abierto con ese rótulo exacto (el único resultado fue el propio #910, de LOCALES-**1**). Control positivo (`acto/gen2-limpieza-ramas-locales-1` en `ls-remote`) → 1 coincidencia, confirma que el barrido examinó de verdad. **Sin duplicado.**
- **Artefacto de sandbox, no de git:** el primer `git worktree add` falló con `error: could not lock config file .git/config: File exists` sobre `/home/pc0/Modelado-Mexicano/.git/config.lock`. Verificado antes de tocarlo: el archivo era de 0 bytes, `-r--r--r--`, con timestamp idéntico al segundo del propio comando fallido; ningún proceso lo tenía abierto (`ps`/`fuser` vacíos); escribir sobre él dio **`Read-only file system`** (error de punto de montaje, no de permisos de archivo normal) — mismo mecanismo que enmascaró `.git/config`/`hooks` como nodos de `/dev/null` en `ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-1` (ver `feedback_p0_home_git_y_mm_adq_son_casos_especiales`), aquí sobre el clon real, no sobre el `/home/pc0/.git` espurio. Se reintentó el mismo comando con el sandbox desactivado para esa sola llamada; la rama ya había quedado creada por el intento fallido (`git branch` la lista), así que el segundo intento solo adjuntó el worktree a la rama existente — ningún dato se perdió ni se forzó.

## P0 · Punto de partida (verificado antes de la compuerta)

- **Bundles de #910, íntegros:** `git bundle verify` sobre ambos da `The bundle records a complete history.` — sin cambios desde que se crearon.
- **`sha256` sin discrepancia:** `34c39bfa6cc1f263625eafdf37d43a4b95e919f267464e65d4629ba2dab48cb7` (Modelado-Mexicano) y `0e38bdcafcfb04802dfc27880df5a5b267a9674a174e81301db8bff0d1d95284` (mm-adq) — coinciden byte a byte con lo declarado en la nota de #910 (leída directamente de la rama del PR, `acto/gen2-limpieza-ramas-locales-1`, ya que esa nota nunca llegó a `origin/main`).
- **Conteo de ramas corregido, como pedía el encargo:** la nota de #910 trae tres cifras distintas para el mismo universo — `306` en el cuerpo (P2), `307` en la línea de `hallazgos.md`, y `150` en su propio párrafo de resumen de cierre. Re-derivado: `git branch --no-color | wc -l` da `270` en `Modelado-Mexicano` y `37` en `mm-adq`, pero esa segunda cifra **incluye la línea pseudo-rama `* (HEAD detached at …)`** que `git branch` antepone cuando el clon está en `HEAD` desprendido — no es una rama. Ramas locales reales: `270 + 36 = **306**`. La cifra correcta es la que ya traía el cuerpo de la nota (P2); `307` cuenta de más (incluye el detached-HEAD) y `150` es un error simple sin derivación reconstruible. No se edita la nota de #910 (ya no está en `main`, y de todas formas el acto que la escribió está cerrado); esta corrección queda archivada aquí para quien la use como referencia.

## COMPUERTA — verificación por producto

El encargo declara `COMPUERTA: PR #910 fusionado`. Verificación mecánica, no por defecto genérico (§2 de `/acto`):

```
$ git fetch --prune origin && git -C Modelado-Mexicano cat-file -e origin/main:forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1.md
fatal: path 'forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1.md' does not exist in 'origin/main'

$ gh pr view 910 --repo Josanoforo/Modelado-Mexicano --json state,mergedAt,mergeCommit
{"state":"OPEN","mergedAt":null,"mergeCommit":null}
```

**La compuerta no se cumple.** PR #910 sigue abierto — no fusionado, no cerrado, la rama `acto/gen2-limpieza-ramas-locales-1` sigue viva y con su contenido intacto (verificado también: nada se perdió, el trabajo de LIMPIEZA-1 está exactamente donde se dejó). El encargo de LIMPIEZA-2 se redactó (SHA `8a842afc`) asumiendo un estado — #910 fusionado — que todavía no ocurrió al momento de abrir este acto.

Por `/acto` §2.3: *"Si la compuerta no se cumple: reporta con A.4/A.13 ... y termina con cero commits. No adelantes ningún paso del acto 'por si acaso'."* Precedente directo en este mismo repo, mismo patrón: `ACTO GEN2-C2-COMPUESTO-IC-ENVIPE2025-1` (`ADR-553`) paró en P0 por premisa no sostenida y archivó una nota de PARO sin ejecutar el resto del encargo.

**Este acto no ejecuta P1–P6.** No se tocó ninguna de las 131 ramas CON-TRABAJO-PROPIO más allá de lo ya hecho en #910; no se generó la tabla TSV; no hay clasificación en las cuatro cubetas.

## Qué falta para que LIMPIEZA-2 pueda correr

Una sola cosa: que alguien con permiso fusione (o cierre explícitamente, si mesa decide no fusionarlo) el PR #910. En cuanto `origin/main` contenga `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1.md`, este mismo encargo (verbatim, sin cambios) puede volver a invocarse y correr P0–P6 completos — los bundles y el inventario que necesita ya están verificados y listos, como consta arriba.

## Cierre

### ## NO-CORRIDO / RESERVAS
P1–P6 completos: `NO-CORRIDO` por `PARO-PREMISA` (compuerta declarada como cumplida, verificada como no cumplida). Sucesor: re-invocar el mismo encargo tras fusionar (o cerrar) PR #910.

### ## CONSUMIDO
Este PR (solo esta nota de PARO — ningún análisis sustantivo).

### Estado final (crudo)

```
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
54
$ gh pr view 910 --json state,mergedAt
{"state":"OPEN","mergedAt":null}
```
