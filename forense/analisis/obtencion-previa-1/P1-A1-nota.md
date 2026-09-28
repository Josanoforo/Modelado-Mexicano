# P1 · A1 · M05 y M23 contra sus RESULT sellados · GEN2-OBTENCION-PREVIA-1

Commit de lectura: `cff4c5bf` (rama claude/new-session-sbqki2). Tabla: `P1-A1-M05-M23.tsv`.

## Premisas
- LEÍDO `milpa/catalogo-momentos-v0_1.tsv` l.6 (M05) y l.24 (M23): computo_pretendido, nivel=persona, spec_ref, estado_relevo vacío.
- LEÍDO `milpa/tramite.yaml` l.490-503 (`tramite.evasion_norma`: condicional a `sancion_creible=false`, uso_motor «conjunta vs condicional») y l.1477-1500 (`dinero.ahorro.via_informal`, sin disparadores). Los punteros del catálogo (:487, :1306) están desplazados.
- LEÍDO `forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md` l.117-142: unidad DELITO, estimando conjunto.
- EJECUTADO `jq` sobre `data/corrida0/CALC-{TRA-EVADE-NORMA-SXD,DIN-AHORRO-SOLO-INFORMAL}-ARBITRO-CRUCE-0002/resultados.json`: R por celda (12 y 8), nacionales, CHAMPION=NINGUNO, SIN-CANDIDATO-SUPERIOR. Solo se leyeron resultados sellados; no se abrió microdato ni se derivó nada de ola reservada.
- EJECUTADO `tools/busca_reactivos.py --tablas todas` con cinco búsquedas (términos en la tabla); universo 314 256 identidades, 113 780 con texto.

## Dictamen
- M05: EXISTE-NO-SATISFACE — el cruce está sellado, pero en unidad delito y como conjunta; el momento pide persona y la regla pide condicional a sanción creíble.
- M23: EXISTE-SATISFACE, con reserva: el valor es RETROSPECTIVO y el holdout ya se consumió, así que solo sirve para describir.
- Ninguno de los dos cabe en la opción (a) HISTÓRICO-SIN-RELEVO de la hoja: la premisa «no hay con qué responder» no se sostiene.

## NC para CAJA (propuesta, no asentada: fuera del perímetro)
M05 a nivel persona: en caja, `python3 corrida0.py demanda` y luego una spec nueva sobre ENVIPE 2025 `TPer_Vic` + `tmod_vic` agregando por `ID_PER`. Antes, que mesa confirme si la reserva consumida del cruce escolaridad×dominio (catálogo l.6, columna reserva) admite ese recálculo descriptivo.

## NO-CORRIDO / RESERVAS
- La etiqueta de BP1_23 («pérdida de tiempo», «desconfianza en la autoridad») no aparece por texto en el índice (0 candidatas). NO-VERIFICABLE-AQUÍ sin el FD de ENVIPE 2025; eso no afecta al dictamen.
