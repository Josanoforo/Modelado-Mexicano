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

Tras el reporte del ejecutor («22 de las 32 posiciones; el runner paró solo por `TECHO-SOLICITUDES` en 94/96 … las 10 posiciones restantes están en NC-0190 esperando tu decisión»), mesa contestó:

«termina el encargo entonces, ese techo es un estimado»

Efecto operativo: el techo de 96 (spec §4.4, solicitudes facturables) se re-dimensiona en la unidad que el contrato v1_1 (c) carga —turnos reales, 3 por invocación mínima—: 32 × 3 × 3 = **288**, con el ledger arrastrado (94 ya gastados). Se corren únicamente las 10 posiciones `NO-CORRIDA`; las 22 capturas existentes se reanudan por identidad, no se repiten.

## NO-CORRIDO / RESERVAS

- **P2 · «Las 32 posiciones bajo el techo de 96»** — corrieron las 32, pero no bajo 96: la primera pasada paró por `TECHO-SOLICITUDES` en 94/96 con 22/32 · `DECISIÓN-DE-MESA-PENDIENTE` → **tomada en sesión**, firma verbatim archivada arriba («termina el encargo entonces, ese techo es un estimado»): hueco de escala del contrato (techo 96 dimensionado a una solicitud facturable por llamada lógica, spec §4.4; v1.1 (c) carga turnos reales, 3–8 por invocación) re-dimensionado en la unidad que se cuenta, 32 × 3 × 3 = 288 turnos, ledger arrastrado; las 10 faltantes corrieron en una segunda pasada (130/288, 0 reintentos) · impacto: ninguno sobre el veredicto (ambas celdas ÉXITO 8/8 vs 0/8); `cuenta_gen2` no se mueve (sin CALC) · sucesor: `NC-0190`, abierta y `CERRADA` en este mismo acto con la resolución.
- **P2 · paso `--verify` del contrato** · `DECISIÓN-DE-MESA-PENDIENTE` (reserva ya tomada en #756: «Sigue, con reserva»): volvió a fallar por el único campo `sha256_manifiesto_fuentes` (`data/manifiesto.yaml` sigue creciendo por commits ajenos; fuentes, paquetes y ancestros reproducen) · impacto: el contrato no imprime `OK` mientras el manifiesto crezca; runner y corrida intactos · sucesor: `NC-0178`, sin cambio (fuera de alcance por letra de v1.1 (e)).
- **P3 (b) · «si el contrato sella CALC: cadena E.2 completa y cuenta_gen2 = SI»** · condicional no activada: el contrato v1.0/v1.1 no sella CALC · impacto: contador cero, dicho en una línea como pide el encargo · sucesor: la lectura conjunta de mesa y dirección (P3 (e)).
- **P3 (d) · «enmienda fechada de REANUDACIÓN en F5-documental-ejecucion-v1_0.md»** · `SUSTITUIDO-POR:ACTO GEN2-F5-DOCUMENTAL-RUN-2` — las dos enmiendas (ejecución y PARO por techo; continuación por firma de mesa) se asentaron en `F5-documental-ejecucion-v1_1.md`, el contrato que gobernó la corrida, porque v1.1 manda que v1.0 «no se edita, no se enmienda»; absorben íntegra la pieza (fecha, acto, solicitudes contra el techo, estado); nada queda huérfano · impacto: ninguno sobre contadores · sucesor: ninguno necesario.
- **P1 · «verifica que el CLI opera con el modelo que el contrato nombra»** · reserva declarada, no desviación: opera (`claude-opus-5`, `usage` reconcilia campo a campo en la sonda y en las 32 posiciones) con `claude-haiku-4-5` auxiliar admitido por la regla (a) de v1.1 (≤ 200 tokens de salida); el cliente es `2.1.272`, no el `2.1.270` de v1.1 — `--help` re-verificado en vivo, sin `--max-turns`, con `--max-budget-usd` y `--allowedTools` · impacto: ninguno · sucesor: ninguno necesario.
- **Sonda no repetida tras el cambio del techo** · reserva declarada: el runner cambió (`TECHO_SOLICITUDES`, ruta del plan) entre la sonda v1.1 y la segunda pasada, y no se gastó una sonda nueva porque el transporte (comando, flags, herramienta, modelo) no cambió; las 10 posiciones nuevas verificaron la identidad del modelo por mensaje con la misma regla (a), 10/10 · impacto: ninguno · sucesor: ninguno necesario.

## CONSUMIDO

Ejecutado en `PR #764`, `ACTO GEN2-F5-DOCUMENTAL-RUN-2`. La fusión queda con mesa.

- **P1** (arranque y sonda): ARRANQUE completo (base `7de3acb`, merge de #761; worktree propio; `data/raw` enlazada; entorno `sin_variable`/red 200/corpus 413); compuerta verificada por producto; runner `tools/f5_documental.py` ajustado a (a)-(d) del contrato v1.1 (`2897970`), tests 11/11; cliente `2.1.272` re-verificado; `--verify` con la misma reserva de #756 (`NC-0178`); plan v1.1 congelado (mismo orden, prompts y materialización que v1.0); **sonda `TRANSPORTE-VALIDADO` 5/5**, ledger 5/96.
- **P2**: `--run` bajo v1.1 — primera pasada 22/32 y parada por `TECHO-SOLICITUDES` en 94/96 (hueco de escala, reportado a mesa); firma de mesa en sesión → techo 288 turnos, plan v1.2, segunda pasada 10/10 sin reintentos. **32/32, ledger 130/288**: 16/16 réplicas dirigidas con `PUNTO` trazable (revisión mecánica 4/4 criterios), 16/16 contextuales `ABSTENCION`, 0 errores.
- **P3 (a)**: veredicto de la secundaria, primer párrafo de la nota, con la fila §4.3 citada textual y el alcance «documental, acotado al panel y al paquete»: **`DIN-M-01` ÉXITO, `TRA-M-07` ÉXITO** (8/8 vs 0/8 cada una). **(b)**: sin CALC (el contrato no lo sella): contador cero, en una línea. **(c)**: `FP-373` sigue `FIRMADA` con `ejecutada_en` → `EJECUTADA`; `NC-0160` → `CERRADA` con el desenlace real; `NC-0177` → `CERRADA`; `NC-0190` abierta y `CERRADA`. **(d)**: dos enmiendas fechadas en `F5-documental-ejecucion-v1_1.md` (v1.0 intacto por letra de v1.1). **(e)**: la lectura conjunta no se escribió.
- Cascada: `ADR-507` (renumerado de `ADR-504` y `NC-0189` de `NC-0186` por `GEN2-ADOPCION-VENTANILLA-2`, PR #762; de `ADR-505` por `GEN2-SANEA-REGISTRO-Y-RESCATE`, PR #767; y de `ADR-506`/`NC-0189` a `ADR-507`/`NC-0190` por `GEN2-LOTE-MEDICION-PENDIENTE-1`, PR #766 — los tres fusionaron primero), L0 y tres contadores reconciliados (`cierre_acto.py --aplica`), rótulo censado, hallazgo, `NC-0190` con `#764`, suite `--baseline` VERDE (3 FAIL preexistentes iguales al baseline).
