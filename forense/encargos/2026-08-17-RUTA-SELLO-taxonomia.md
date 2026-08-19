# ENCARGO E-RUTA · RUTA-SELLO — sellar como canon la taxonomía RUTA-A/RUTA-C/RUTA-I/SIN-RUTA, con estampa
- **SHA de redacción:** `f3873c2` · **Fecha:** 2026-08-17 · **Redactor:** dirección (Fable) · **Estado:** CONSUMIDO — ACTO RUTA-SELLO, `PR #245` (`b653bb4`), 17/ago/2026. Sella `ADR-89`.
- **Evidencia de consumo (derivada del árbol, ACTO CONF-07-CIERRE 18/ago/2026):** el sello existe — `canon/gobernanza-v1_15.md:1455`, verbatim *"ADR-89 · Sella como canon la taxonomía RUTA-A/RUTA-I/RUTA-C/SIN-RUTA (censo v1.0 §1) y estampa (A.10) el reparto de los 15 coeficientes […] y `FP-13` pasa a `FIRMADA`"*, con la firma que lo autoriza citada en `gobernanza:1457` (*"sellémosla."*, `ADR-79(f)`). El gate de arranque del encargo (`instrucciones-proyecto-v2_10.md` en `origin/main`) se cumplió: E-A10 fusionó en `PR #242`, antes de `PR #245`. Queda vigente el rótulo `VENCIBLE EN ALCANCE al cierre de BARRIDO-2` que el propio `ADR-89` le puso al reparto — es una reserva del ADR, no un pendiente de este encargo.
- **Entorno asignado:** NUBE · Modelo: Sonnet 4.6. **NO** en la caja de Codex.
- **GATE DE ARRANQUE (comando, duro):** `git cat-file -e origin/main:instrucciones-proyecto-v2_10.md`
  → si falla, E-A10 no ha fusionado: PARA y reporta "gate no cumplido". Este sello usa A.10 y comparte
  archivos con E-A10; no corren en paralelo.
- **Concurrencia:** BARRIDO-2 en paralelo — su lista de colisión es territorio prohibido; este acto no toca
  `data/` ni `tools/`.

════════ ARRANQUE ════════ (idéntico: rama `claude/ruta-sello` · base `f3873c2` + el gate de arriba ·
no toca microdato, salta data/raw · entorno nube + sonda github · espejo prohibido)
══════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección, 2026-08-17, contra `f3873c2` ═══
1 · ESTRUCTURA. Gobiernan: `canon/gobernanza-v1_15.md` (ADR) · `forense/censo-estimabilidad-coeficientes-
    v1_1.md` (la taxonomía y sus cifras; su cabecera declara base `origin/main = dcc4f6a`) ·
    `forense/firmas-pendientes.tsv` (FP-13) · `canon/glosario-v5_6.md` SOLO si T05 lo exige. Nada en `data/`.
2 · CONTENIDO. El sello NO existe, verificado tres veces: `censo v1_1:45` verbatim *"sigue sin ser canon,
    sigue sin regir nada hasta que una mesa la selle con ADR"* · `gobernanza:1056` (un ADR ratificó el
    movimiento de 3 filas y declaró explícitamente NO sellar la taxonomía) · `gobernanza:984` la lista como
    contador con universo provisional. La firma EXISTE-SATISFACE: ADR-79(f), verbatim *"sellémosla."*
    (`gobernanza:1179`), que nombra a RUTA-SELLO como sucesor, sin número de ADR anticipado.
3 · COBERTURA RETROACTIVA. Censo v1_1 nació 2026-08-12 (`13e2ffa`), anterior a ADR-79 (13/ago) — la firma ya
    lo vio; sin brecha.
═══════════════════════════════════════════════════════════════════

PERÍMETRO Y CONCURRENCIA. Toca EXACTAMENTE: `canon/gobernanza-v1_15.md` (append ADR) ·
`forense/censo-estimabilidad-coeficientes-v1_1.md` (SOLO la línea :45 y una línea de cabecera: "sellada por
ADR-<n>") · `forense/firmas-pendientes.tsv` (FP-13) · `canon/glosario-v5_6.md` solo si T05 obliga · nota ·
self-archive A.3. "Fuera de esta lista, PARA."

## Cuerpo — un ADR, dos commits
**Commit 1 (el sello).** (a) A.3. (b) ADR, número derivado al merge (colisión posible con Codex; T15 arbitra):
— **Canon:** las CUATRO definiciones (RUTA-A / RUTA-I / RUTA-C / SIN-RUTA) citadas verbatim del censo (v1.0 §1
  vía v1_1), ahora vocabulario que rige.
— **Cifras con estampa (A.10):** deriva el reparto POR COMANDO desde la tabla del censo v1_1 (awk sobre sus
  15 filas; pega comando y salida cruda — NO heredes 3/1/2/9 ni ningún reparto de memoria: v1.1 movió filas)
  y séllalo COMO SNAPSHOT al universo del censo (base `dcc4f6a`, régimen que el propio censo declara),
  rotulado explícitamente: **VENCIBLE EN ALCANCE al cierre de BARRIDO-2 — no es estado del programa, no es
  denominador ni cuota para el barrido, no rige territorio nuevo.**
— FP-13 → FIRMADA; la línea :45 del censo actualizada citando el ADR.
**Commit 2 (verificación).** Suite VERDE · `git diff --check` · nota con la frase de sello.
**Qué NO hace.** No adjudica ni mueve ninguna ruta · no toca registro-recalculo ni el censo salvo las dos
líneas dichas · no fija nada para BARRIDO-2 · no mueve `13/27`, `11/15`, `0/15`, `1/2`, `4/144`.
**Contadores: 0.** Tablero: FP-13 FIRMADA. **Cierre:** PR, reporte corto, JAMÁS auto-fusión.

---

## Nota de archivo (A.3), añadida al self-archivar — no parte del texto de lanzamiento de arriba

Este encargo se lanzó dos veces. **Primer lanzamiento** (mismo texto de arriba, base `f3873c2`): el GATE DE
ARRANQUE falló — `git cat-file -e origin/main:instrucciones-proyecto-v2_10.md` devolvió
`fatal: path 'instrucciones-proyecto-v2_10.md' does not exist in 'origin/main'` (`origin/main` llegaba solo
hasta `instrucciones-proyecto-v2_9.md`). Verificado también, sin rama/PR/encargo de E-A10 en ningún sitio del
repo. Conforme a la instrucción del propio encargo ("PARA y reporta 'gate no cumplido'"), y siguiendo el
precedente ya escrito en este mismo repositorio para un PARO de gate duro sin fase de repliegue declarada
(`forense/notas/2026-08-13-sella-mesa.md` §1, *"Segundo PARO, reportado, sin escritura"*): se paró y se
reportó en el chat, **sin tocar un solo archivo del repo** — cero commits, cero rama nueva más allá de la ya
provista por el entorno.

**Segundo lanzamiento** (este mismo texto, dirección confirma "instrucciones actualizadas y ese PR merged"):
gate re-corrido contra `origin/main` fresco (`git fetch`) → PASA. `origin/main` avanzó de `f3873c2` a
`4c9da5b`; el rango trae `instrucciones-proyecto-v2_10.md` (A.10 escrito, `ADR-87`) y `ADR-88`
(`T22-DERIVA`). El acto se retoma desde cero contra `4c9da5b`, sin heredar número de ADR ni cifras del primer
intento — mismo criterio que el propio encargo exige ("número derivado al merge... nunca se fija") y que
`ADR-70`/`ADR-71`/`ADR-74` ya aplicaron tras sus propias colisiones de numeración.

**Este archivo se commitea junto con el sello que ejecuta (`ADR-89`), en el mismo Commit 1** — la propia
instrucción del encargo agrupa "(a) A.3. (b) ADR" en un solo commit; no hay, por tanto, un hash de commit
distinto y anterior que citar aquí para "consumido" (a diferencia de actos donde el A.3 se commitea aparte,
antes de la firma). **Estado se deja `VIVO`** en la cabecera de arriba — mismo criterio que
`forense/encargos/2026-08-17-EA10-a10-estampa.md` aplicó en la situación idéntica (self-archive y ejecución
en el mismo acto): la cita `CONSUMIDO — ejecutado en ... commits <hash>` que otros encargos usan
(`2026-08-13-adr-provisionalidad.md`, `2026-08-14-B2-mantenimiento-via-capa3.md`) cita hashes de commits
*anteriores* al propio archivo, no el commit que el propio archivo integra — citarse a sí mismo por hash es
circular. El registro de qué lo consumió vive en `ADR-89` (`canon/gobernanza-v1_15.md`) y en la columna
`firmada_en` de `FP-13` (`forense/firmas-pendientes.tsv`), ambos con número de PR real una vez abierto —
mismo mecanismo de `PR #<n>` que `FP-09`/`ADR-87` ya usó (`forense/notas/2026-08-17-a10-estampa.md`).
