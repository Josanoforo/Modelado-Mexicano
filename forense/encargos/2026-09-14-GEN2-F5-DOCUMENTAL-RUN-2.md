# ENCARGO · ACTO GEN2-F5-DOCUMENTAL-RUN-2 (relanzamiento de GEN2-F5-DOCUMENTAL-RUN)

**SHA de redacción:** lanzado sobre el merge de PR #761 (`7de3acb4`, `origin/main` re-derivado al abrir: `7de3acb`)
**Entorno asignado:** CAJA (UBUNTU/WSL de mesa), Opus
**Compuerta:** GATED al merge de GEN2-VERIFICACION-CAJA-2 (PR #761) — cumplida por producto (`git merge-base --is-ancestor 7de3acb4… HEAD` → OK; `forense/notas/2026-09-14-GEN2-VERIFICACION-CAJA-2-cierre.md` en `origin/main`) — y al merge del contrato v1_1 (PR #758: `forense/prereg-duelo-v2/F5-documental-v1_0/F5-documental-ejecucion-v1_1.md` en `origin/main`)
**Encargo que se ejecuta:** el archivado en `forense/encargos/2026-09-14-GEN2-F5-DOCUMENTAL-RUN.md` (texto verbatim del 14/sep, CONSUMIDO en PR #756 con PARO `NC-0177`/`NC-0178`), ahora contra el contrato v1_1. Firma de FP-373 archivada en `F5-documental-firma-v1_0.md` (sha `aa7135c8…`), válida para v1_1 por el propio contrato.

## Texto del encargo, verbatim tal como se lanzó

RELANZAMIENTO · ACTO GEN2-F5-DOCUMENTAL-RUN · CAJA, Opus · ejecuta el encargo archivado contra el contrato v1_1 (PR #758); techo con embudo ARRASTRADO desde 2/96; 32 posiciones; criterio ≥6/8; FP-373 sigue FIRMADA. Si la sonda choca con el contrato: PARO otra vez.

Compuerta cumplida por producto: #761 fusionado — arranca sobre ese merge (7de3acb4). Firma de mesa, 15/sep/2026.

*(Nota del ejecutor: la firma dice 15/sep; el reloj de la caja marcaba 14/sep 18:56 CST al archivarla — 15/sep en UTC. El archivo se fecha por el reloj local, como los demás encargos del día.)*

## Firma de mesa en sesión, verbatim (continuación tras el PARO por techo)

Tras el reporte del ejecutor («22 de las 32 posiciones; el runner paró solo por `TECHO-SOLICITUDES` en 94/96 … las 10 posiciones restantes están en NC-0186 esperando tu decisión»), mesa contestó:

«termina el encargo entonces, ese techo es un estimado»

Efecto operativo: el techo de 96 (spec §4.4, solicitudes facturables) se re-dimensiona en la unidad que el contrato v1_1 (c) carga —turnos reales, 3 por invocación mínima—: 32 × 3 × 3 = **288**, con el ledger arrastrado (94 ya gastados). Se corren únicamente las 10 posiciones `NO-CORRIDA`; las 22 capturas existentes se reanudan por identidad, no se repiten.

## NO-CORRIDO / RESERVAS

- **P2 · «Las 32 posiciones bajo el techo de 96»** — 10 de 32 posiciones `NO-CORRIDA` (`DIN-M-01` dirigidas 3, 6, 7 y contextuales 1, 3, 6; `TRA-M-07` dirigida 5 y contextuales 1, 6, 8) · `PARO-PREMISA`: el runner paró por `TECHO-SOLICITUDES` al intentar la posición 23 con el ledger en 94/96 — hueco de escala del contrato: el techo 96 está dimensionado a una solicitud facturable por llamada lógica (spec §4.4, 32×3) y el contrato v1.1 (c) carga el `num_turns` real de cada invocación (3 en las dirigidas, 3–8 en las contextuales), con lo que 96 cubre ~20 posiciones; se reporta, no se enmienda ni se negocia · impacto: `DIN-M-01` sin veredicto (5/5 `PUNTO` trazables corridas, 3 dirigidas sin correr: ni `≥6/8` ni `<6/8`); `TRA-M-07` alcanza el criterio con lo observado (7/7, robusto a sus 4 no corridas salvo «cero sustituciones» en la réplica dirigida 5); `cuenta_gen2` no se mueve · sucesor: `NC-0186` — decisión de mesa (contrato v1.2 con el techo en la unidad que se cuenta y reanudación sobre las capturas existentes, o veredicto con lo observado).
- **P2 · paso `--verify` del contrato** · `DECISIÓN-DE-MESA-PENDIENTE` (reserva ya tomada en #756: «Sigue, con reserva»): volvió a fallar por el único campo `sha256_manifiesto_fuentes` (`data/manifiesto.yaml` sigue creciendo por commits ajenos; fuentes, paquetes y ancestros reproducen) · impacto: el contrato no imprime `OK` mientras el manifiesto crezca; runner y corrida intactos · sucesor: `NC-0178`, sin cambio (fuera de alcance por letra de v1.1 (e)).
- **P3 (b) · «si el contrato sella CALC: cadena E.2 completa y cuenta_gen2 = SI»** · condicional no activada: el contrato v1.0/v1.1 no sella CALC · impacto: contador cero, dicho en una línea como pide el encargo · sucesor: la lectura conjunta de mesa y dirección (P3 (e)).
- **P3 (d) · «enmienda fechada de REANUDACIÓN en F5-documental-ejecucion-v1_0.md»** · `SUSTITUIDO-POR:ACTO GEN2-F5-DOCUMENTAL-RUN-2` — la enmienda se asentó en `F5-documental-ejecucion-v1_1.md` (el contrato que gobernó la corrida) porque v1.1 manda que v1.0 «no se edita, no se enmienda»; absorbe íntegra la pieza (fecha, acto, solicitudes contra el techo, estado); nada queda huérfano · impacto: ninguno sobre contadores · sucesor: ninguno necesario.
- **P1 · «verifica que el CLI opera con el modelo que el contrato nombra»** · reserva declarada, no desviación: opera (`claude-opus-5`, `usage` reconcilia campo a campo en la sonda y en las 22 posiciones) con `claude-haiku-4-5` auxiliar admitido por la regla (a) de v1.1 (15 tokens de salida ≤ 200); el cliente es `2.1.272`, no el `2.1.270` de v1.1 — `--help` re-verificado en vivo, sin `--max-turns`, con `--max-budget-usd` y `--allowedTools` · impacto: ninguno · sucesor: ninguno necesario.

## CONSUMIDO

Ejecutado en `PR #764`, `ACTO GEN2-F5-DOCUMENTAL-RUN-2`. La fusión queda con mesa.

- **P1** (arranque y sonda): ARRANQUE completo (base `7de3acb`, merge de #761; worktree propio; `data/raw` enlazada; entorno `sin_variable`/red 200/corpus 413); compuerta verificada por producto; runner `tools/f5_documental.py` ajustado a (a)-(d) del contrato v1.1 (`2897970`), tests 11/11; cliente `2.1.272` re-verificado; `--verify` con la misma reserva de #756 (`NC-0178`); plan v1.1 congelado (mismo orden, prompts y materialización que v1.0); **sonda `TRANSPORTE-VALIDADO` 5/5**, ledger 5/96.
- **P2**: `--run` bajo v1.1 — **22/32 posiciones** (12 `PUNTO` trazables 12/12 en el brazo dirigido, 10 `ABSTENCION` en el control, 0 errores), 1 reintento técnico por `error_max_budget_usd`, parada por `TECHO-SOLICITUDES` en 94/96; 10 posiciones `NO-CORRIDA` (ver `## NO-CORRIDO / RESERVAS`, `NC-0186`). Cero solicitudes extra.
- **P3 (a)**: veredicto de la secundaria, primer párrafo de la nota, con la fila §4.3 citada textual y el alcance «documental, acotado al panel y al paquete»: `TRA-M-07` alcanza el criterio; `DIN-M-01` sin veredicto. **(b)**: sin CALC (el contrato no lo sella): contador cero, en una línea. **(c)**: `FP-373` sigue `FIRMADA` con `ejecutada_en` → `EJECUTADA-PARCIAL`; `NC-0160` → `CERRADA` con el desenlace real; `NC-0177` → `CERRADA`. **(d)**: enmienda fechada en `F5-documental-ejecucion-v1_1.md` (v1.0 intacto por letra de v1.1). **(e)**: la lectura conjunta no se escribió.
- Cascada: `ADR-504`, L0 y tres contadores reconciliados (`cierre_acto.py --aplica`), rótulo censado, hallazgo, `NC-0186` con `#764`, suite `--baseline` VERDE (3 FAIL preexistentes iguales al baseline).
