# ENCARGO · ACTO GEN2-F5-DOC-CONTRATO-V1_1

**SHA de redacción:** redactado contra el corte del 14/sep (re-derivado al abrir: `22aa835`, merge de PR #756, `origin/main`)
**Entorno asignado:** NUBE, Opus
**Compuerta:** GATED al merge del PARO de F5-DOCUMENTAL-RUN (verificado: `origin/main` HEAD = `22aa835`, merge de PR #756 "ACTO GEN2-F5-DOCUMENTAL-RUN")

## Texto del encargo, verbatim tal como se lanzó

— ENCARGO · ACTO GEN2-F5-DOC-CONTRATO-V1_1 · NUBE, Opus · COMPUERTA: GATED al merge del PARO de F5-DOCUMENTAL-RUN · FIRMA DE MESA, 14/sep/2026, verbatim: «[pega aquí tu respuesta "1" y este mensaje]» — única entrega: el contrato F5-documental-ejecucion-v1_1.md como sucesión (v1_0 intacto), redactado con el archivo y la evidencia cruda del PARO enfrente: (a) qué hace exactamente el auxiliar haiku-4-5 en claude -p — si toca la RUTA DE RESPUESTA o solo compactación/telemetría, con la cita de la salida JSON que lo demuestre; si toca respuesta, el contrato lo PROHÍBE y dice cómo (flag exacto); si no, lo DECLARA como componente auxiliar permitido con la evidencia de identidad del modelo respondedor por mensaje; (b) el conjunto mínimo de --allowedTools/negaciones MCP que preserva el blindaje, listado y justificado línea por línea; (c) por qué el print mode consumió 3 turnos contra el límite de 2, y el límite nuevo con su razón — no "3 porque salió 3": la causa; (d) la sonda de transporte re-especificada (qué valida, qué evidencia pega, cuántas solicitudes cuesta) y el embudo que ARRASTRA las 2/96 ya gastadas; (e) todo lo demás del v1_0 — 32 posiciones, techo 96, criterio ≥6/8, exclusión FP-374/F6 — copiado sin tocar y declarado así. El contrato cierra con la frase de sello. PERÍMETRO: el archivo v1_1 + nota + no-corrido (la NC sucesora del PARO → token) + 0-bis + cascada; nada más. LO QUE NO HACE: no ejecuta ninguna solicitud, no toca el runner todavía (el RUN relanzado lo ajusta bajo el contrato nuevo), no re-abre la escala del criterio. SUCESOR: relanzar GEN2-F5-DOCUMENTAL-RUN apuntando a v1_1 — mismo encargo, una línea de mesa.

## NO-CORRIDO / RESERVAS

- **Editar `tools/f5_documental.py` para materializar (a)-(d)** (`--allowedTools`, tope de salida del auxiliar, `--max-budget-usd` en vez de `--max-turns`, `cargo_solicitudes` sin recorte a la baja, `sonda_transporte` con las cinco condiciones) · `FUERA-DE-PERÍMETRO`: el propio encargo, LO QUE NO HACE, dice "no toca el runner todavía (el RUN relanzado lo ajusta bajo el contrato nuevo)" · impacto: el runner sigue ejecutando el código sellado de v1.0 (con los tres defectos de (a)-(c)) hasta que el acto sucesor lo edite; `NC-0177` sigue `ABIERTA` · sucesor: el `SUCESOR` declarado por este mismo encargo — relanzar `GEN2-F5-DOCUMENTAL-RUN` apuntando a v1_1.
- **Correr las 32 posiciones bajo el techo de 96** · `FUERA-DE-PERÍMETRO`: mismo LO QUE NO HACE ("no ejecuta ninguna solicitud") · impacto: `cuenta_gen2` no se mueve, la secundaria del duelo sigue sin veredicto (ni `≥6/8` ni `<6/8`) · sucesor: el mismo relanzamiento de `GEN2-F5-DOCUMENTAL-RUN` apuntando a v1_1.
- **`NC-0178` (`--verify` / `sha256_manifiesto_fuentes`)** · `FUERA-DE-PERÍMETRO`: no es una de las piezas (a)-(e) que este encargo pide, aunque `NC-0178` anticipaba "el mismo sucesor de NC-0177" — el texto verbatim de este encargo no lo cubre y no se absorbe por inercia · impacto: `NC-0178` sigue `ABIERTA` sin cambio, el verificador sigue comparando contra un manifiesto que crece · sucesor: `SIN-ASIGNAR` — un acto que ajuste `sha256_manifiesto_fuentes` a las 8 filas del contrato, no al archivo entero.
- **Re-abrir la escala del criterio (`≥6/8`, cero sustituciones, mejora de cobertura `≥4/8`)** · `FUERA-DE-PERÍMETRO`: LO QUE NO HACE explícito del encargo · impacto: ninguno — la escala de v1.0 sigue vigente sin cambio · sucesor: `SIN-ASIGNAR`.

## CONSUMIDO

Ejecutado en `PR #758`, `ACTO GEN2-F5-DOC-CONTRATO-V1_1`. Entrega única:
`forense/prereg-duelo-v2/F5-documental-v1_0/F5-documental-ejecucion-v1_1.md`
(sucesión fechada, v1.0 intacto), con las cinco piezas (a)-(e) del encargo
resueltas dentro del propio contrato, cada una con su evidencia cruda
citada. `NC-0177` pasa de `SIN-ASIGNAR` a token (este PR); sigue `ABIERTA`
— las 32 posiciones siguen sin correr hasta que `GEN2-F5-DOCUMENTAL-RUN` se
relance apuntando a v1.1. `NC-0178` sin tocar. Cascada: `ADR-499`, L0 y
tres contadores reconciliados (`cierre_acto.py --aplica`), rótulo censado
en `canon/registro-rotulos.tsv`, suite `--baseline` VERDE (3 FAIL
preexistentes iguales al baseline).
