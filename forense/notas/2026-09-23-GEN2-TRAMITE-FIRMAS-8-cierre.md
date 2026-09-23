# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-8

0-bis: `aa3ffe8` (rama `claude/new-session-edpgs6`, sobre `c9b67bf8` = `origin/main` al abrir, 0 commits de diferencia).

## Tabla: firma · fila · qué desbloquea · qué sigue abierto y por qué

| Firma (FP) | Fila en `decisiones.tsv` | Qué desbloquea | Qué sigue abierto | Por qué |
|---|---|---|---|---|
| `FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` (opción a: lote ESTRICTO) | Sí, objeto = este id, FIRMADA | Autoriza construir la bandera `estricto` en `corrida0.py registro` (≤30 líneas, con test) | `NC-260922-...-7d98-01/-02/-04` y las cuatro `NC-...-4e12-01/-0af9-01/-009f-01/-ef6f-01` (#1003/#1005/#1008/#1012) — todas ABIERTAS, enmendadas: cierran con el primer push real **tras** el lote estricto, no antes | La implementación (`tools/corrida0.py`) es AJENA al perímetro de este acto (§9 del encargo) — sucesor `GEN2-TUBERIA-LOTE-ESTRICTO-1` (`NC-...-aa3f-01`) |
| `FP-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1-e889-01` (instrumentar auto-merge de rutina) | Sí, objeto = este id, FIRMADA | Autoriza construir P1 (`rutinas-clases-v1_0.tsv`), P2 (workflow + prueba sintética) y P3 (huella) del acto | Esos tres entregables — no se construyen aquí (relanzamiento es sucesor, `NC-...-aa3f-02`). Sub-pregunta `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04` (protección de `main` / merge queue / quién fusiona) sigue ABIERTA: mesa dejó las tres líneas en blanco otra vez (segundo intento, `NC-...-aa3f-04`) | El acto no implementa nada (§10 del encargo: "no relanza el automerge, lo hace mesa"); la instrumentación puede instalarse **apagada** mientras 8e53-04 sigue sin respuesta |
| `FP-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01` (opción a: R02/R08 fuera del panel F6 por unidad) | Sí, objeto = este id, FIRMADA (tipo 3 — firma de mesa, no del PR) | Cierra la pregunta de unidad para R02-WBES/R08-ENCRIGE: ninguna se adquiere | `NC-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-03` (la fila que la propia FP gatea) sigue sin poder cerrarse desde aquí — vive solo en la rama `claude/new-session-ceszds` (PR #1014), sin fusionar. `NC-0161`/`NC-0162` (panel F6, más amplias) reciben enmienda fechada: panel F6 sin R02/R08, `EN-ESPERA-PANEL` con R01/R09/R10/R11 | La FP y su NC gatilladora nacieron en una rama todavía sin fusionar (tipo 3, §2 de procedencia); la firma es de mesa (verbal, en esta conversación) y se registra igual en `decisiones.tsv`, pero no puedo cerrar una fila de `no-corrido.tsv` que no existe en mi árbol — sucesor `NC-...-aa3f-03`, se cierra cuando #1014 fusione |

## Verificación de premisas (§4 del acto)

- `[EJECUTADO]` FP abiertas en main al `c9b67bf8`: confirmado — 7d98-01, e889-01 y 3d56-01 (física, no tocada) presentes; e7be-01 ausente en main (vive en PR #1014 sin fusionar, tipo 3 — confirmado con `git show origin/claude/new-session-ceszds:forense/firmas-pendientes.tsv`).
- `[EJECUTADO]` `grep -n estricto tools/corrida0.py` → 7 coincidencias, las 7 de `_asigna_ids(estricto=...)` (objeto ids, no `registro --lote`) — confirmado, la bandera de lote ESTRICTO no existe todavía.
- `[EJECUTADO]` `grep -cE "7d98-01|e889-01|e7be-01" data/corrida0/decisiones.tsv` → 0 antes de este acto — confirmado.
- `[SUPUESTO]` "Mesa rellenó las tres líneas de 8e53-04 al firmar T2" — **falso**: el encargo trae las tres líneas en blanco (`___` × 3), verbatim, en §2. Consecuencia prevista por el propio encargo: 8e53-04 queda ABIERTA con la pregunta, y el automerge (e889-01) se marca FIRMADA de todas formas — ejecutado tal cual lo previó §3.

## Tres PR en cola citados por la cabecera (re-verificados al abrir)

`git fetch` mostró exactamente los tres PR abiertos que la cabecera anticipaba: #1014 (`claude/new-session-ceszds`, ACTO GEN2-ADQ-F6-DIRIGIDA-1), #1025 (MARCADOR-CONSUMO-2) y #1021 (duelo ENVIPE2026-MARGINALES-2). Ninguno fusionó antes de este acto — confirmado con `mcp__github__list_pull_requests` (estado `open` los tres). La FP e7be-01 se trató en consecuencia como tipo (3).

## Hallazgo de paso (no citado por el encargo, encontrado al leer `canon/gobernanza-v1_15.md` antes de escribir el ADR propio)

`ADR-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1-e889-01` (el PARO del acto anterior con el mismo hex) registra que `FP-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01` (20/sep/2026, FIRMADA) dejó el auto-merge explícitamente **NO instrumentado**, «reevaluable si esa fracción crece» (9 % de los merges eran de rutina en ese momento). La firma de mesa que este acto registra (`e889-01`) no cita esa fila ni el dato de fracción actualizado — es una decisión nueva y explícita de mesa sobre el mismo objeto («se instrumenta el auto-merge…»), no un olvido de este acto ni del encargo: mesa tiene autoridad para reevaluar sin repetir la cita. Se deja asentado en `firmas-pendientes.tsv` (fila `e889-01`) y en `NC-260923-GEN2-TRAMITE-FIRMAS-8-aa3f-02` para que el acto que relance `GEN2-TUBERIA-RUTINAS-AUTOMERGE-1` cite ambas FP en su ADR (9a2c-01 superada por e889-01) en vez de tropezar de nuevo con el mismo PARO.

## No se tocó

`tools/corrida0.py`, `verify.yml`, ningún CALC, ninguna vista derivada (`data/corrida0/corridas.tsv`, `resultados.tsv`, `usos.tsv`) — todo ajeno al perímetro (§9 del encargo).
