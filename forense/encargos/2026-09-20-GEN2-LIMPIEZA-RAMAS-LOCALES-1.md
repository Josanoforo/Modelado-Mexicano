ENCARGO · ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-1 · INVENTARIO Y LIMPIEZA DE RAMAS, WORKTREES Y RESTOS DE CODEX Y CLAUDE EN LA MÁQUINA LOCAL: PRIMERO SE CUENTA, DESPUÉS SE RESPALDA, AL FINAL SE BORRA SOLO LO FUSIONADO
⚠ ENTORNO: MÁQUINA LOCAL (la caja) — NO NUBE

Este acto limpia el disco donde corrieron Codex CLI y Claude Code. En una sesión remota no hay nada que limpiar. Primera acción, antes de cualquier otra: git worktree list y ls data/raw | head -1. Si data/raw no existe y hay un solo worktree recién clonado, estás en nube: PARA y dilo en una línea. (El 20/sep un encargo de caja se lanzó en nube; este recuadro existe por eso.)

CABECERA (D-12) · SHA de redacción a92126f0; re-deriva al abrir · una sola sesión · compuerta: ninguna · MODELO: Sonnet (receta sin juicio; donde haga falta juicio, el encargo manda listar, no borrar) · CONTADOR: cuenta_gen2 = NO; no mide; cero contadores del programa · FP/ADR/NC: deriva al cierre · vehículo /acto para la parte que escribe en el repo (la nota); la limpieza en sí no es un commit.

Gate D-14, contestado: defecto ya observado — el 19/sep una rama sin PR fue invisible para mesa durante horas, el mismo CALC-id vivió en dos ramas, y mesa borró ramas en GitHub que siguen vivas en local. ¿Cambia una decisión? Sí: qué trabajo sin fusionar se rescata. ¿Cuesta menos que corregirlo? Sí: tools/limpia_arbol.py ya existe (--reporta / --aplica); este acto lo usa, no lo reinventa.

REGLA DE ORO DE ESTE ACTO

Nada se borra con fuerza. Prohibidos git branch -D, git worktree remove --force, git clean, git stash drop/clear, rm -rf sobre cualquier clon, y git push --delete. Lo único que se borra es lo que git acepta borrar sin forzar. Todo lo demás se lista para mesa.

RAMAS EN VUELO — INTOCABLES (leídas de git ls-remote --heads origin a las 03:30 UTC del 20/sep; re-deriva la lista al abrir y usa la tuya)

acto/gen2-c2-compuesto-ic-enif2024-1 · acto/gen2-c2-compuesto-ic-envipe2025-1 · acto/gen2-pisos-enut2019-ejes-1 · claude/intelligent-albattani-v7kf2s · claude/lucid-lamport-32k9t3 · claude/optimistic-cray-15co3n · claude/relaxed-bell-rs3dhf. Regla general: toda rama presente en origin, toda rama con commit en las últimas 24 h, y toda rama que sea el HEAD de un worktree con proceso vivo, es EN-VUELO: no se toca ni se cambia de rama en su worktree.

PIEZAS

P0 · ¿Cuántos clones hay? find ~ -maxdepth 5 -type d -name .git 2>/dev/null y, para cada uno, git -C <dir> remote get-url origin: quédate con los que apunten a Josanoforo/Modelado-Mexicano. Codex y Claude pueden haber trabajado en clones o worktrees distintos. Declara cuántos directorios examinaste y cuántos casaron (A.13). P1 · Inventario, solo lectura, por cada clon. git fetch --prune origin · python3 tools/limpia_arbol.py --reporta --json · git worktree list --porcelain · git branch -vv · git stash list · git status --porcelain en cada worktree. Una fila por rama local con: clon, rama, carril (codex/, claude/, acto/, adq/, censo/, otro), último commit (fecha, asunto), git log origin/main..<rama> --no-merges | wc -l (commits propios), si existe en origin, si tiene worktree, si el worktree está sucio. P2 · Clasificación mecánica (token en el campo, A.16):

EN-VUELO — regla de arriba. No se toca.
FUSIONADA — 0 commits propios y git branch -d la aceptaría (git branch --merged origin/main la lista). Candidata a borrar.
CON-TRABAJO-PROPIO — ≥ 1 commit propio. No se borra. Sub-rótulo: REMOTO-BORRADO si ya no está en origin.
WORKTREE-SUCIO — cambios sin commitear o archivos sin seguimiento. No se toca. P3 · Respaldo antes de borrar nada. Por clon: git bundle create ~/respaldo-ramas-2026-09-20-<clon>.bundle --all · git bundle verify · sha256sum. El bundle vive fuera del repo. Si verify falla, PARA: no hay limpieza. P4 · Limpieza, solo lo seguro. Para cada FUSIONADA sin worktree: git branch -d <rama> (minúscula). Para cada FUSIONADA con worktree limpio y sin proceso: git worktree remove <ruta> (sin --force) y luego -d. Al final git worktree prune y git remote prune origin. Si git se niega en cualquier paso, esa rama pasa a la lista de mesa con el mensaje de git pegado crudo; no insistas. P5 · Lo que NO se borra, presentado para que mesa decida fácil. Tabla de CON-TRABAJO-PROPIO y WORKTREE-SUCIO con: qué hay (archivos por zona: data/corrida0/CALC-*, tools/, milpa/, gobierno…), si ese trabajo ya está respaldado en main por otra vía, y recomendación en una palabra (RESCATAR / ARCHIVAR-DIFF / BORRABLE-TRAS-FIRMA). Casos que dirección ya conoce y que debes verificar, no suponer:
codex/gen2-marcador-adopcion-cli-1: su diff está archivado en forense/notas/insumos-externos/marcador/codex-03-2d662e7.diff (+ .sha256). Verifica que el tip local sea 2d662e7…; si coincide → BORRABLE-TRAS-FIRMA; si el local va más adelante, hay trabajo sin respaldar: dilo.
codex/gen2-enadid2023-union-sexo-edad-cli-2: 16 commits propios, cuatro versiones de CALC, borrada de GitHub, nunca fusionada. Es medición real; su dictamen es de RECIBO-CODEX-6. Aquí: RESCATAR — confirma que el bundle la contiene y reporta su tip.
codex/gen2-recibo-codex-3, codex/optimiza-verificacion-ci-prueba-compuerta y …-base-medicion: duplicado y pruebas temporales; reporta commits propios y recomienda. P6 · Restos que no son ramas — y una prohibición de lectura. En cada worktree, lista archivos sin seguimiento bajo data/corrida0/ (un CALC sellado en disco y no empujado es una medición que el contador no ve: E.7), forense/, y cualquier carpeta tipo scratch/, tmp/, notebooks/. Si encuentras un script, notebook o salida que parezca agrupar por dos variables una ola reservada (encig25*, enif2024*, envipe2025*, eder2025*): reporta que existe, su ruta, fecha y tamaño. No lo abras, no lo ejecutes, no pegues su contenido. Se pide la categoría del defecto, nunca su contenido (lección NC-0328: un cruce visto no se puede desver). P7 · Anti-PR#77. ls data/raw | wc -l por clon y si data/raw es directorio real o enlace al corpus compartido. Si algún clon tiene payloads propios que no están en el corpus compartido, lístalos; no los muevas. P8 · Nota en el repo (forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1.md, por /acto, rama propia desde main): tablas de P1–P7, comandos con salida cruda, sha256 de los bundles, conteos de archivos examinados, y la lista de decisiones para mesa. Una línea en hallazgos.md: cuántas ramas había, cuántas se borraron, cuántas quedan para firma.
PERÍMETRO

En disco: solo las operaciones de P4 sobre ramas FUSIONADA. En el repo: la nota, hallazgos.md, cascada mínima. No toca ninguna rama EN-VUELO, ningún worktree sucio, ningún archivo sin seguimiento, origin (ni una sola escritura remota salvo el PR de la nota), data/raw, ni configuración global de git. «Si te encuentras escribiendo —o borrando— fuera de esta lista, PARA.»

LO QUE NO HACE

No fusiona · no rescata (lista para que otro acto rescate) · no dictamina la calidad de ninguna medición · no borra bundles viejos · no toca GitHub.

CIERRE

## NO-CORRIDO / RESERVAS ("Ninguno." si aplica) · ## CONSUMIDO con PR · estado final: git branch | wc -l y git worktree list por clon, pegados crudos.
