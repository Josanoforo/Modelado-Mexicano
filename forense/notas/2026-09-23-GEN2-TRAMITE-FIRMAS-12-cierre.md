# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-12

23/sep/2026, entorno NUBE (`ENTORNO-DERIVADO = NUBE`, corpus no montado, red `DENEGADA-POR-POLITICA`, coincide con lo declarado por el encargo). Sonnet 5, MODO ABIERTO. Base al arrancar y al cerrar: `origin/main = 7722b9c` (0 commits de diferencia).

## Qué se hizo

**P1 · Firmas.** Las cuatro decisiones de §2 (D1-D4) del encargo llegan verbatim dentro del propio texto del encargo que las ejecuta — no hay un trámite de mesa separado que las repita, así que la firma viaja dentro del encargo (§0 de las instrucciones vigentes). Entraron a `forense/firmas-pendientes.tsv` como cinco filas: `D1`-`D4` en `FIRMADA`, con el acto ejecutor citado en la columna `gatea`; la quinta (alianza académica CIDE/ITAM) en `ABIERTA`, dueño mesa, exactamente como el propio §2 la marca «Pendiente sin firma».

**P2/P3 · No ejecutadas.** Verificado al abrir la sesión: `ls /root/.claude/uploads/<sesión>/` devolvió un solo archivo (el .md del encargo); ninguno de los tres adjuntos que §3 declara (`INFORME-COMPETENCIA-2026-09-23.md`, `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md`, `MISION-ASTRA-4-ADENDA-1.md`) llegó, ni el cuarto que P3 exige (`HOJA-DE-DECISIONES-2026-09-23.md`). `ls forense/encargos/fuentes/` mostró 4 entradas preexistentes, ninguna de competencia. Esto es exactamente el PARO f de §7 del encargo: «mesa no dio las firmas o los adjuntos no llegaron (se archiva lo que llegó y se declara el resto)». No se archivó nada sin sha verificable contra el adjunto real — hacerlo violaría la compuerta §8. Ambas piezas quedan declaradas en `## NO-CORRIDO / RESERVAS` del encargo archivado y como filas `NC-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-01/02` en `forense/no-corrido.tsv`, `ABIERTA`, sucesor `GEN2-TRAMITE-FIRMAS-13` (nombrado por el propio encargo §10).

## Lo que no se hizo

No corre el deep search 2. No escribe el informe v1.3. No toca las filas D1-D8 de `FIRMAS-11` (repetido explícitamente por §4 del encargo — se verificó que siguen intactas). No archiva ningún adjunto sin sha verificado.

## Contadores

`celdas_validadas`: 92 → 92 (sin cambio, declarado). CONTADOR del acto: cero mediciones, no adopta (declarado desde la cabecera del encargo). `firmas-pendientes.tsv`: +5 filas. `no-corrido.tsv`: +2 filas.

## Suite

`python3 tests/check.py --rapido` → VERDE, 0 FAIL (corrida antes de este commit y repetida al final de la cascada).
