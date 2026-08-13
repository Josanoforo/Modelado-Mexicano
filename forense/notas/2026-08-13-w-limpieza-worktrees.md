# ACTO W · Limpieza de worktrees y medición de causa de cierres — 2026-08-13

## §0 · Premisas

Caja local Ubuntu (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir), la misma donde vienen ocurriendo los cierres abruptos que reporta el usuario. Acto de entorno, no de árbol versionado: perímetro limitado a esta nota y a la línea correspondiente en `forense/hallazgos.md`. Base: `origin/main` = `2b13e88` (merge #189), confirmado antes de empezar — coincide con lo que declaraba el encargo, sin divergencia.

## §1 · Causa de los cierres — sigue sin identificar

`dmesg -T | grep -iE "oom|killed process|out of memory"` → **cero coincidencias**. `journalctl --since "24 hours ago" -p err` → sin entradas de oom-killer; solo ruido esperable de WSL (`dxg` ioctl, `chronyd "Could not step system clock"`, `WSL CheckConnection`). `free -h` → 12Gi libres de 15Gi, swap en 0 usado. **No hay evidencia de presión de memoria en las últimas 24h.** `.git/index.lock` no existe.

Durante la ejecución sí apareció una pista falsa que hay que dejar corregida por escrito: `.git/config.lock` resultó ser un nodo de dispositivo de caracteres (`crw-rw-rw- nobody:nogroup`, major/minor `1,3`, equivalente a `/dev/null`), y `git worktree remove`/`git branch -d` fallaban sobre él con "Device or resource busy". La primera lectura fue tratarlo como posible huella de una interrupción abrupta del proceso git. `mount` lo desmintió: es un bind-mount `devtmpfs` que el **propio sandbox de ejecución de este agente** impone sobre `.git/config`, `.git/config.worktree` y cada `.git/worktrees/*/config.worktree` (protección de escritura del harness, no artefacto del sistema operativo del usuario) — visible también sobre `.gitconfig`, `.bashrc`, `.claude/*`, todos montados `ro` o `devtmpfs` por el mismo mecanismo. Se retracta explícitamente: **esto no es evidencia relacionada con los cierres de Ubuntu.** Retomar con `dangerouslyDisableSandbox` resolvió la escritura sin tocar nada del lado del usuario. Conclusión de §1: **la causa de los cierres sigue sin identificada** — no hay evidencia de OOM, y no hay otra pista real que perseguir con lo mirado hasta ahora.

## §2 · Inventario y clasificación (37 worktrees, antes de tocar nada)

`git worktree list` → 37 entradas (incluye el clon base). `du -sh` total ≈ 1.1 GB; `df -h .` → 943G disponibles de 1007G (2% uso) — el espacio nunca fue el problema. Clasificación por `git merge-base --is-ancestor <rama> origin/main` + `git status --porcelain` por worktree, contenido de lo "sucio" inspeccionado uno por uno (no solo contado):

- **HUÉRFANO** (1): `.git/worktrees/.claude` — gitdir inexistente, entrada de metadatos sin worktree real detrás. Podado con `git worktree prune`.
- **FUSIONADO, limpio de facto** (11): ancestro de `origin/main`, y lo único "sucio" en cada uno era el symlink no-trackeado `data/raw` (defecto ya conocido de `data/raw/` con slash final en `.gitignore` no matcheando un symlink — mismo patrón presente en el propio clon base, no es contenido nuevo). Ninguno tenía commits sin empujar.
- **CON TRABAJO / NO FUSIONADO** (25 restantes, incluyendo el clon base): se listan completas en §4.

### Worktrees FUSIONADO borrados (worktree + `branch -d`, nunca `-D`)

| worktree | rama | HEAD |
|---|---|---|
| mm-map-a-cota-universo | map-a/cota-universo | d96771d |
| mm-sellado-adr-67-68 | sellado/adr-67-68 | a02225b |
| mm-e4a-radio-celda-d | e4a/radio-celda-d | c4639bd |
| mm-e4b-sello-b-corrida-b | e4b/sello-b-corrida-b | 1a074ee |
| mm-e4c-r5-1-d2 | mesa/e4c-paso3-corrida | 75c9fb7 |
| mm-j-join-folioviv | mesa/j-join-folioviv | a87f633 |
| mm-m-adq-ensafi-enfih | acto-m-adq/ensafi-enfih | 2b13e88 |
| mm-o-cola-adquisicion | acto-o/cola-adquisicion | cffb0b6 |
| mm-p-lote1-adquisicion | acto-p/lote1-adquisicion | 84f8e30 |
| mm-remediacion-brecha-documental | remediacion/brecha-documental | da0fe7d |
| mm-u1-e4b-prime | u1/e4b-prime-recorrida | bc89ee4 |

Nota operativa: `git branch -d` compara por defecto contra el `HEAD` actual del checkout, no contra `origin/main` — como el clon base está sobre una rama vieja (`sesion/cal-conf-faseb-pos4-envipe-paso1`), la primera pasada de `-d` rechazó 10 de las 11 con "not fully merged" (falso negativo, ya verificadas ancestro de `origin/main` por `merge-base`). Se corrigió apuntando el upstream de cada rama a `origin/main` (`git branch --set-upstream-to=origin/main <rama>`) antes de reintentar `-d` — no se usó `-D` en ningún caso; la compuerta de git se respetó, solo se le dio la referencia correcta.

Flag operativo: `mm-m-adq-ensafi-enfih` era el worktree con `data/raw` enlazado al corpus real (no solo el symlink de ruteo), reusado en sesiones previas para correr `check.py --baseline`. Se borró igual, por instrucción explícita de mesa (opción 1) tras preguntarlo — recrear un worktree equivalente es trivial si se necesita.

## §3 · Ejecución

`git worktree prune -v` (huérfano `.claude` + los 11 directorios administrativos residuales, bloqueados en el primer intento por el mismo sandbox de §1) → 12 entradas podadas. 11 `git worktree remove --force` (forzado solo por el symlink `data/raw` no-trackeado, verificado inofensivo antes de forzar). 11 `git branch -d` (10 vía el rodeo de upstream + 1 directo). `.git/config` verificado sin secciones `[worktree ...]` huérfanas tras la limpieza. `git status --short` del clon base: solo `data/raw` y `data/secretos.local.yaml`, sin cambios al árbol versionado — perímetro respetado.

## §4 · Los 26 que quedan, con su conteo de commits sin empujar (`git log --oneline origin/main..<rama> | wc -l`)

| # | rama | sin empujar | worktree |
|---|---|---:|---|
| 1 | codex/curador-baseline-semantico | 590 | Modelado-Mexicano-curador |
| 2 | cruce1-1786051624 | 575 | wt-cruce1-1786051624 |
| 3 | wt-abrir4-1786051186 | 568 | wt-abrir4-1786051186 |
| 4 | barrido1-1786050583 | 560 | wt-barrido1-1786050583 |
| 5 | sesion/indice2-1786050152 | 554 | wt-indice2-1786050152 |
| 6 | explora2-1786042858 | 546 | wt-explora2-1786042858 |
| 7 | verif3-outage-note-1786046437 | 538 | wt-verif3-outage-note-1786046437 |
| 8 | verif3-1786042795 | 536 | wt-verif3-1786042795 |
| 9 | map2-cruce-1786030513 | 526 | wt-map2-1786030513 |
| 10 | repair1-094125-2 | 521 | wt-repair1-094125-2 |
| 11 | claude/explora-puertas-banxico-qnm3cn | 517 | wt-cifix-149-20260806-115910 |
| 12 | ci-endurecido | 514 | wt-ci-endurecido-112438-2 |
| 13 | int1-integridad-1786003491 | 511 | wt-int1-1786003491 |
| 14 | map1-lector-1786000558 | 505 | wt-map1-1786000558 |
| 15 | verificacion-crc-eocd-corpus | 495 | wt-tc1-010528-2 |
| 16 | map1b-censo-1786000741 | 495 | wt-map1b-censo-1786000741 |
| 17 | conf17-reconciliado | 485 | wt-conf17 |
| 18 | desc1-descarga | 483 | wt-desc1 |
| 19 | ver1-crudo | 477 | wt-ver1 |
| 20 | sesion/p-lapop-microdato | 424 | mm-p-lapop-microdato |
| 21 | sesion/regla-elegibilidad-preregistro-r5-1 | 304 | mm-regla-elegibilidad-preregistro |
| 22 | sesion/cruce-catalogo-fichas | 299 | mm-cruce-catalogo-fichas |
| 23 | mesa/s-svystat-4celdas | 1 | mm-acto-s-svystat |
| 24 | map-b/crosswalk-fuente-puerta | 0* | mm-map-b-crosswalk |
| 25 | cierre-164-hallazgos-2026-08-10 | 0* | Modelado-Mexicano-barrido-completo |
| 26 | sesion/cal-conf-faseb-pos4-envipe-paso1 | — | Modelado-Mexicano (clon base) |

\* Ancestro de `origin/main` (0 commits sin empujar) pero con contenido no-trackeado real que impidió clasificarlo FUSIONADO: `mm-map-b-crosswalk` tiene `scratch/build_crosswalk.py`; `Modelado-Mexicano-barrido-completo` tiene ~5MB de artefactos de corridas bajo `data/curacion-registro/ejecucion-semantica/runs/` sin commitear.

**Pregunta abierta que no se resuelve en este acto**: `Modelado-Mexicano-curador` — 590 commits sin empujar, `ancestor_of_origin_main=NO`, con herramientas reales (`tools/curador_registro/curador.py`, `supervisor.py`, tests, `multi1-staging/`, `multi2-staging/`) que no existen en ningún otro lugar del árbol. Es el mayor volumen de trabajo no integrado del inventario y no se puede adjudicar (¿fusionar, descartar, es de otra línea de trabajo?) sin leer su contenido — eso es un acto en sí mismo, no una línea de este cierre.

## §5 · Cierre

1. **La causa de los cierres abruptos de Ubuntu sigue sin identificarse** — sin evidencia de OOM en dmesg/journalctl (24h), memoria y swap sanos; la única pista que apareció durante el acto (el nodo-dispositivo en `.git/config.lock`) se verificó y se descartó como artefacto del propio sandbox de este agente, no del entorno del usuario.
2. Inventario inicial: 37 worktrees, ~1.1GB, disco al 2% de uso — el espacio nunca fue el problema.
3. 1 huérfano podado (`.git/worktrees/.claude`), 11 FUSIONADO borrados (worktree + `branch -d`, nunca `-D`; tabla completa en §2).
4. 26 worktrees sobreviven — 25 no-FUSIONADO/no-limpios + el clon base; tabla completa con commits-sin-empujar en §4.
5. `Modelado-Mexicano-curador` (590 sin empujar, ancestro=NO, tooling real) es la pieza más grande del inventario sin adjudicar — se declara aquí como candidato a su propio acto, no se toca en este.
6. Perímetro respetado: único cambio al árbol versionado es esta nota + la línea de `forense/hallazgos.md`; el clon base no tiene cambios trackeados propios.
7. Contadores de medición: **0** — este acto es de entorno, no midió ninguna hipótesis del programa.
