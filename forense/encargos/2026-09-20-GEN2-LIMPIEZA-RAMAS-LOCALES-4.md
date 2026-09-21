# GEN2-LIMPIEZA-RAMAS-LOCALES-4 — encargo (A.3, archivado verbatim)

Pegado por el usuario directamente en esta sesión (CAJA, pc0-0d), sin pasar por
`forense/encargos/cola/`, 20/sep/2026. Texto verbatim a continuación.

---

INPUT DE MESA · 20/sep/2026 · a la sesión de limpieza (CAJA). Acto nuevo, rama nueva:
GEN2-LIMPIEZA-RAMAS-LOCALES-4 — la pasada final. MODO: ABIERTO. Pegarlo es el sello de las firmas.

OBJETIVO. Que el clon de la caja quede en: main al día, solo ramas de actos vivos, y cada
resto que no sea rama con un destino decidido. «Hecho»: `git branch | wc -l` y
`git worktree list | wc -l` reportados, y una tabla de lo que queda con su porqué.

LO QUE DIRECCIÓN SABE
[LEÍDO] nota de cierre de #923: quedan 50 ramas y 48 worktrees; 8 excluidas del borrado
(3 EN-VUELO por la regla de 24 h, 4 WORKTREE-SUCIO, 1 revisada a mano); 2 MEDICION-SIN-RESCATAR;
5 REVISAR-A-MANO. MOTRAL: NO-EJECUTABLE, no rescatable. ENIF -0002 de Codex: archivada como
evidencia en forense/notas/insumos-externos/pisos-enif2021-0002-rama-codex/.
[LEÍDO] nota de #910: el clon base está parado en claude/tramite-2026-09-17 con un error.log
sin seguimiento; 26 ramas FUSIONADA quedaron protegidas ese día por la regla de 24 h.
[EXISTE] forense/notas/insumos-externos/marcador/codex-03-2d662e7.diff — no sé si el tip local
de codex/gen2-marcador-adopcion-cli-1 sigue siendo 2d662e7.
[SUPUESTO] que las 3 EN-VUELO y las 26 ya pasaron la ventana de 24 h. Si alguna no: se queda.

FIRMAS
F-A · "Se borran, re-verificadas hoy una por una con el método de #923 (cherry + árbol contra
la HISTORIA de origin/main): las 3 que eran EN-VUELO y las 26 FUSIONADA de #910 si ya pasaron
24 h; claude/encargo-maestra38-sello-3 (redundancia verificada a mano en #923);
codex/optimiza-verificacion-ci-prueba-compuerta (un commit de prueba temporal)."
F-B · "codex/gen2-marcador-adopcion-cli-1 se borra SI su tip es 2d662e7 y los dos archivos de
evidencia están en main. Si el tip va más adelante: archiva el diff faltante como insumo con
sha256, y entonces se borra."
F-C · "codex/gen2-recibo-codex-3 y las tres de mm-adq (adq/2026-09-15-nc-0202,
adq/2026-09-16-gen2-38-investigacion, censo/2026-09-16): para cada una, si su contenido ya está
en la historia de main, se borra; si no, se archiva su diff contra main como insumo externo con
sha256 y se borra. Ninguna trae CALC sellado (#913)."
F-D · "MOTRAL: se archiva como insumo externo la spec, el medidor y la salida cruda de verify
(forense/notas/insumos-externos/motral2015-prioridades/), para que una re-medición futura parta
de ahí. Después se borra la rama. Su worktree está en estado AA por un rebase abortado: es el
ÚNICO caso en que se autoriza `git worktree remove --force`, y solo después de guardar
`git status` y `git diff` de ese worktree junto al insumo."
F-E · "El clon base vuelve a main: mueve error.log a ~/ (no lo borres), git checkout main,
git pull --ff-only. Si no es fast-forward, PARA esa pieza y dilo."

LOS 4 WORKTREES SUCIOS — aquí preguntas, no decides. Por cada uno (codex/autoridad-semantica-
enif, codex/autoridad-semantica-marco-cobertura-total, llave2-decreto, marco-produccion-total):
lista archivos sin seguimiento o modificados con ruta, tamaño y fecha. Si algo parece cruzar
dos variables de una ola reservada (encig25*, enif2024*, envipe2025*, eder2025*): ruta, fecha y
tamaño — NO lo abras. Preséntale a mesa, por worktree, tres opciones con tu recomendación
(archivar como insumo · descartar · conservar), y sigue con lo demás mientras contesta.

PAROS (lista cerrada): cualquier --force fuera de F-D · borrar una rama presente en origin o con
commit < 24 h · abrir un resto de ola reservada · git clean · stash drop · push --delete.
No es paro: un clon otra vez superficial (desprofundiza y dilo — y si pasó, el arreglo de #923
no bastó: reporta qué comando lo causó).

AL CERRAR: corre la suite y DESPUÉS comprueba `git rev-parse --is-shallow-repository`. Una línea
en hallazgos: el hook de arranque ya imprime el número de worktrees; si pasa de 60, es hora de
otra pasada. No construyas nada más para esto (D-14).

## NO-CORRIDO / RESERVAS

- `NC-0423`: `git branch -D` sobre las 6 ramas rechazadas por `git branch -d` (contenido
  verificado redundante o propio real, pero no ancestro de `main`) — razón
  `DECISION-DE-MESA-PENDIENTE`. Sucesor: `FP-402`. Detalle completo en la nota de cierre.

## CONSUMIDO

`PR #929` — ver `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-4-cierre.md`.
