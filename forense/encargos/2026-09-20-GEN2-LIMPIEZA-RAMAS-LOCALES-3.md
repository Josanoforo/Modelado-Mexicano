ENCARGO · ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-3 · BORRAR LO QUE MESA FIRMÓ, RESCATAR UNA MEDICIÓN, Y DICTAMINAR UNA COLISIÓN DE CALC-id QUE LIMPIEZA-2 NO VIO
⚠ ENTORNO: MÁQUINA LOCAL (la caja) — NO NUBE. Si el hook no dice CAJA, PARA.

CABECERA (D-12) · SHA de redacción 8b7b0562; re-deriva · una sola sesión · COMPUERTA: #913 en main (cumplida) · MODELO: Sonnet para P1; P3 exige juicio: si no lo tienes claro, lista y no concluyas · CONTADOR: P2 puede sumar una corrida a la vista; cuenta_gen2 nace PENDIENTE-DE-MESA · FP/ADR/NC: deriva al cierre.

FIRMA DE MESA (propuesta por dirección sobre el texto de #913 §P5; tu lanzamiento es el sello; sin texto, solo corre P0 y P3)

"Se borran con -D las ramas de las cubetas CONTENIDO-EN-MAIN y HISTORIA-GEN1 de limpieza2_tabla.tsv, re-verificadas hoy una por una; los bundles 34c39bfa… y 0e38bdca… las conservan. No se borran: las que sigan EN-VUELO por la regla de 24 h, las de worktree sucio, las 5 REVISAR-A-MANO y las 2 MEDICION-SIN-RESCATAR. CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001 se rescata. CALC-PISOS-ENIF2021-EJES-0002 de la rama Codex no se rescata como CALC: se archiva como evidencia y se dictamina."

PIEZAS

P0 · Respaldo vigente. git bundle verify de los dos bundles y sha256 contra #913. El clon ya no es superficial (--is-shallow-repository → false): confírmalo; si volvió a serlo, PARA — toda la clasificación depende de eso. P1 · Borrado, cubeta por cubeta. Para cada rama firmada: re-deriva hoy git cherry origin/main <rama> y la comparación de árbol de #913; si ya no cae en su cubeta, no se borra y se lista. git branch -D solo sobre esa lista; git worktree remove sin --force y solo si data/raw en ese worktree es symlink o no existe (la comprobación de #910). Estado final crudo: git branch | wc -l, git worktree list | wc -l. P2 · Rescate de MOTRAL. Desde el commit 914e92f3 (no desde el worktree, que tiene un rebase abortado con marcadores de conflicto): rama nueva desde main, trae solo data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/, su spec, su test y su nota; corrida0.py verify en proceso aislado; fila en la vista y asiento de replay (E.7); PR. MOTRAL 2015 es evidencia (a), módulo de trayectorias laborales: la nota declara universo y unidad en su primera línea. Si verify no reproduce, no se rescata: NC con la salida cruda. P3 · La colisión que #913 no vio. #913 dice que CALC-PISOS-ENIF2021-EJES-0002 de codex/gen2-marcador-adopcion-cli-1 está «ausente de main, sin colisión de id». Dirección verificó lo contrario contra 8b7b0562: ls data/corrida0/CALC-PISOS-ENIF2021-EJES-0002/ → medidor.py spec.yaml; corridas.tsv → SUPERADO→…-0003 · n_res = 0 · NO-CORRIDA. Mismo id, otro contenido. Y eso abre una pregunta de orden que importa, porque …-EJES-0003 alimenta hoy 28 celdas del marcador: main afirma que -0002 nunca corrió; en otra rama, sí corrió y se selló el 19/sep, antes de la «corrección posicional» que dio origen a -0003. Dictamina, sin abrir microdato: (a) archiva el directorio de la rama como evidencia, no como CALC: forense/notas/insumos-externos/pisos-enif2021-0002-rama-codex/ + sha256; (b) compara spec.yaml y medidor.py de las dos versiones de -0002 y contra -0003: ¿qué es la corrección posicional, exactamente?; (c) compara los resultados.json de la -0002 ejecutada contra -0003: qué celdas cambian y cuánto; (d) con los timestamps de commit de ambas ramas, responde: ¿la corrección se hizo después de haber visto los resultados de -0002? Tres respuestas posibles y ninguna se fuerza: CORRECCION-INDEPENDIENTE-DEL-RESULTADO (un defecto de código que cualquier lectura del FD revela) · CORRECCION-POSTERIOR-A-VER-RESULTADO (no invalida -0003, pero su sello no es "primer resultado": FP a mesa, y -0003 lleva reserva) · NO-DETERMINABLE. P4 · Nota por /acto, con la corrección a #913 asentada por enmienda (no se edita su nota).

PERÍMETRO

En disco: P1 sobre la lista firmada. En el repo: nota, forense/notas/insumos-externos/…, el PR de rescate de MOTRAL (rama propia), hallazgos.md, NC/FP, cascada. No toca CALC-PISOS-ENIF2021-EJES-0002 ni -0003 en main · ningún worktree sucio · origin salvo los PR propios. Prohibidos worktree remove --force, git clean, stash drop, push --delete. «Si te encuentras borrando o escribiendo fuera de esta lista, PARA.»

## NO-CORRIDO / RESERVAS

- **qué:** P1 · Borrado, cubeta por cubeta.
  **por qué:** `PARO-PREMISA`.
  **impacto:** ningún `branch -D` ejecutado; las cubetas `CONTENIDO-EN-MAIN`/`HISTORIA-GEN1` de `limpieza2_tabla.tsv` siguen firmadas y pendientes de borrado; `git branch | wc -l` / `git worktree list | wc -l` de la caja no se movieron.
  **sucesor:** `NC-0404` → re-invocación verbatim de este encargo tras confirmar clon no-superficial de forma estable.

- **qué:** P2 · Rescate de MOTRAL.
  **por qué:** `PARO-PREMISA`.
  **impacto:** `CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001` (evidencia (a), verificada como ausente de `main` por `#913`) sigue sin rama propia, sin `verify`, sin fila en la vista ni asiento de replay; ningún PR de rescate abierto.
  **sucesor:** `NC-0405` → mismo sucesor que P1.

- **qué:** P3 · La colisión que `#913` no vio (dictamen `CALC-PISOS-ENIF2021-EJES-0002`).
  **por qué:** `PARO-PREMISA` — el propio dictamen depende de comparar timestamps de commit y árbol entre `codex/gen2-marcador-adopcion-cli-1` y `origin/main`, la misma clase de comparación que un clon superficial puede sesgar.
  **impacto:** `#913` sigue afirmando "ausente de main, sin colisión de id" sin corrección; las 28 celdas que hoy alimenta `…-EJES-0003` no llevan la reserva que un veredicto `CORRECCION-POSTERIOR-A-VER-RESULTADO` exigiría si ese resultara ser el caso; el directorio de la rama Codex no quedó archivado como evidencia.
  **sucesor:** `NC-0406` → mismo sucesor que P1.

- **qué:** P4 · Nota por `/acto` con la corrección a `#913` asentada por enmienda.
  **por qué:** `PARO-PREMISA` (parcial: la nota de este acto sí se produjo — es esta misma, `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-3-paro.md` — pero la enmienda a `#913` que P4 pedía depende del dictamen de P3, que no corrió).
  **impacto:** `#913` no lleva enmienda; su texto original permanece intacto (correcto: A.3 prohíbe editar la nota).
  **sucesor:** `NC-0407` → mismo sucesor que P1.

## CONSUMIDO

Ejecutado por `PR #923` (`acto/gen2-limpieza-ramas-locales-3`) — `PARO-PREMISA` en P0, cero commits sustantivos. Ver `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-3-paro.md` y `canon/gobernanza-v1_15.md ADR-563`.
