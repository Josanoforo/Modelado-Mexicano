ENCARGO · ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-2 · LAS 131 RAMAS "CON TRABAJO PROPIO": QUÉ DE ESO YA ESTÁ EN MAIN, QUÉ ES MEDICIÓN SIN RESCATAR Y QUÉ ES HISTORIA — SOLO LECTURA; NO BORRA NADA
⚠ ENTORNO: MÁQUINA LOCAL (la caja) — NO NUBE

Primera acción: git worktree list | wc -l y ls data/raw | head -1 desde /home/pc0/Modelado-Mexicano. Si no hay corpus ni worktrees, PARA en una línea.

CABECERA (D-12) · SHA de redacción 8a842afc; re-deriva al abrir · una sola sesión · COMPUERTA: PR #910 fusionado (este acto parte de su inventario y de sus bundles) · MODELO: Sonnet · CONTADOR: cuenta_gen2 = NO; cero contadores · este acto no borra, no fusiona y no empuja nada salvo su nota.

POR QUÉ UNA SEGUNDA PASADA ANTES DE BORRAR

LIMPIEZA-1 clasificó por ancestría: "commits propios" = commits que no son ancestros de origin/main. Eso no dice si el contenido ya llegó a main por otra vía — una rama …-cierre, un cherry-pick, otro PR — ni si lo que queda es una medición sellada que nunca se empujó. Borrar 131 ramas con -D sobre esa sola señal perdería de vista las dos cosas. El caso que lo prueba ya apareció: CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001 vive en un worktree con un merge a medias y no está en main (ls data/corrida0 | grep MOTRAL → solo VALORACION-SS).

REGLA DE ORO (la misma)

Prohibidos git branch -D, worktree remove --force, git clean, stash drop, rm -rf, push --delete, merge, rebase, checkout en worktrees ajenos. Ramas EN-VUELO (presentes en origin, con commit < 24 h, o con proceso vivo): ni se leen sus archivos sin seguimiento. Olas reservadas (encig25*, enif2024*, envipe2025*, eder2025*): si un resto parece cruzar dos variables, se reporta ruta, fecha y tamaño — no se abre.

PIEZAS

P0 · Punto de partida verificado. Los dos bundles de LIMPIEZA-1 existen en /home/pc0/, git bundle verify sigue dando "complete history", y su sha256 coincide con el de la nota de #910. Si no: PARA — sin respaldo no hay siguiente paso. Corrige de paso, en tu nota, el conteo de ramas examinadas que #910 dejó inconsistente (dice 150 en el resumen y 306 en el cuerpo): deriva el bueno. P1 · Para cada rama CON-TRABAJO-PROPIO, tres preguntas mecánicas: (a) ¿Su contenido ya está en main? git cherry origin/main <rama> (equivalencia por parche) y git diff --stat origin/main...<rama>; cuenta commits + (sin equivalente) y - (con equivalente). (b) ¿Trae archivos que main no tiene? Lista rutas que existen en la rama y no en origin/main, agrupadas por zona. La zona que importa: data/corrida0/CALC-*/ con sello.json — una corrida sellada fuera de main. (c) ¿De qué era es? Fecha del último commit y prefijo (sesion/, acto/, codex/, claude/, adq/, preservado/, otro). P2 · Cuatro cubetas (token en el campo, A.16), una fila por rama:

CONTENIDO-EN-MAIN — todos sus commits tienen equivalente, o el diff contra main es vacío o solo de derivados regenerables.
MEDICION-SIN-RESCATAR — trae al menos un CALC-* con sello que main no tiene. Para cada uno: id, fecha, si tiene resultados.json, si su spec.yaml toca una ola reservada (por nombre de payload, sin abrir datos), y si el mismo CALC-id existe en main con otro contenido (colisión).
HISTORIA-GEN1 — último commit anterior a 03bcd6f6 (corte de generación, 7/sep), sin CALC GEN2. Las 53 sesion/ deberían caer aquí; verifícalo, no lo supongas.
REVISAR-A-MANO — lo que no cae limpio en ninguna. Con una línea de por qué. P3 · Los tres bultos grandes, una línea cada uno: acto/gen2-e5-calc-0001-0003 (2 112 commits propios según #910: ¿es una base vieja divergente o trabajo real?), marco-produccion-total (931, worktree SUCIO), preservado/r3-1-merge-verificado-no-empujado (249; el nombre dice que alguien lo guardó a propósito: busca por qué en hallazgos.md y notas). P4 · Los 15 + 2 worktrees sucios: por cada uno, git status --porcelain | wc -l y las zonas tocadas. El merge a medias de MOTRAL (AA en medidor.py): reporta los dos lados del conflicto por nombre de rama y fecha, no lo resuelvas. P5 · Propuesta de firma para mesa, por cubeta — texto listo para firmar, no ejecutado:
CONTENIDO-EN-MAIN y HISTORIA-GEN1: "se borran con -D; el bundle <sha256> las conserva".
MEDICION-SIN-RESCATAR: "no se borran; pasan a un acto de rescate, una por una".
REVISAR-A-MANO: lista corta para dirección. P6 · Nota en el repo por /acto (forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-2.md), con la tabla completa como TSV adjunto y los conteos por cubeta derivados. Una línea en hallazgos.
PERÍMETRO

En disco: nada — solo lectura. En el repo: la nota, su TSV, hallazgos.md, cascada mínima. «Si te encuentras borrando, fusionando o escribiendo fuera de esta lista, PARA.»

SUCESORES

LIMPIEZA-3 (ejecuta los borrados que mesa firme, con -D, cubeta por cubeta) · un acto de rescate por cada MEDICION-SIN-RESCATAR que mesa quiera.

CIERRE

## NO-CORRIDO / RESERVAS · ## CONSUMIDO · estado final crudo.
