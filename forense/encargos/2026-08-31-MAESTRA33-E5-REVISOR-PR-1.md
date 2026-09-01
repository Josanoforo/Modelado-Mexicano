# ENCARGO · MAESTRA33-E5 · REVISOR-PR-1 — invoca `/acto`

*(Archivado verbatim por A.3 antes de ejecutar ningún paso sustantivo. Texto tal
como lo entregó dirección el 31/ago/2026. No se edita en ningún otro punto: es el
registro de qué se pidió, para poder auditar si el ejecutor hizo lo que se le dijo.)*

---

ENCARGO · MAESTRA33-E5 · REVISOR-PR-1 — invoca /acto
SHA de redacción: 8b6aa85 (merge PR #415). ENTORNO: NUBE — NO CAJA, NO doble. COMPUERTA: PR de MAESTRA33-E4 (DELTA-E3) fusionado; si no, cero commits. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 31/ago/2026): "Dame las siguientes automatizaciones" · "necesito que estas conversaciones se enfoquen más en estrategia, guía y dirección que en ejecución".
A.8 (dirección contra 8b6aa85): .claude/commands/ = acto, adquiere, despacha, tramite — revisor: NO-ENCONTRADO. Las revisiones adversariales de #411/#413/#415 existen como commits inline, sin checklist versionado (grep -rln "revisión adversarial" .claude/ forense/agente-*.md → 0 skill).
P1 · .claude/commands/revisa.md — dado un PR (número o rama), sobre la VISTA PREVIA DEL MERGE, verifica y pega comando+salida por punto: (1) encargo archivado verbatim (A.3) y coherencia con el reporte; (2) orden de commits: en actos que miden, spec congelada ANTES de resultados y cero ediciones hacia atrás; (3) perímetro declarado vs archivos tocados; (4) negativos con conteo de archivos (A.13); (5) toda cifra del reporte re-derivada por comando, ninguna aceptada; (6) originales intactos donde el encargo lo exija (líneas borradas = 0); (7) escala y universo declarados en cada cantidad medida (A-bis 3/4); (8) ADR/FP candidatos y renumeración si main se movió; (9) tests/check.py --baseline sobre la vista previa; (10) "lo que NO hace" respetado. Salida: UN comentario en el PR con VEREDICTO ∈ {FUSIONABLE · FUSIONABLE-CON-RESERVA · NO-FUSIONAR} y hallazgos numerados. Nunca aprueba formalmente, nunca empuja commits, nunca fusiona: comentar es todo lo que hace.
P2 · forense/agente-revisor-v1_0.md — runbook + prompt (≤5 líneas) para rutina con activador "Evento de GitHub · Solicitud de extracción: Abierto", filtro: título que NO empiece por "[TRAMITE]"; corrección automática OFF; cero conectores; falsador a 1 mes: si mesa fusiona un PR con un defecto que la lista habría atrapado → se añade el punto y se anota; si bloquea en falso 3 veces → se revisa la lista.
P3 · Calibración: corre /revisa sobre el PR de A1 (adquisición, ya fusionado) post-hoc — no comenta en GitHub; deja el veredicto en forense/notas propia. Es la prueba de que la lista atrapa lo que dirección atrapó hoy a mano.
PERÍMETRO: revisa.md, agente-revisor-v1_0.md, forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: cero, declarado.
LO QUE NO HACE: no aprueba ni fusiona; no empuja a ramas ajenas; no toca acto/tramite/despacha/adquiere.
si usas agentes que sean en sonnet

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E5 · REVISOR-PR-1`, abierto 31/ago/2026 y
cerrado 1/sep/2026, entorno **NUBE**, rama
`claude/revisor-pr-automatizado-yg8d0v`, **`PR #418`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/418). Commits:
`d61692a` (0-bis A.3, este archivo) · `aa9a1bb` (`P1`,
`.claude/commands/revisa.md`) · `6832edd` (`P2`,
`forense/agente-revisor-v1_0.md`) · `ee70a17` (`P3`, calibración post-hoc
en `forense/notas/2026-08-31-revisa-calibracion-maestra33-a1.md`) ·
cascada (`ADR-246` candidato — RENUMERADO de 245 a 246 al fusionar `main`
antes de cerrar, porque `ACTO MAESTRA33-C2 · ARBITRO-R-1` / `PR #417` fusionó
primero y tomó el 245; `canon/gobernanza-v1_15.md` y
`canon/estado-programa-v1_10.md` recifrados 245 → 246,
`canon/registro-rotulos.tsv` censado, `FP-211` abierta como recibo).

Resultado: los tres `P` ejecutados. `P3` dio **`NO-FUSIONAR`** sobre
`PR #414` ya fusionado, con **6 `BLOQUEA`** — entre ellos que la fila
`WVS` declara `(ausente)` del manifiesto contra un inventario que no
tiene el campo consultado, cuando el manifiesto sí trae seis payloads de
microdato de esa misma fuente, y que por eso el acto re-sondeó por red
algo ya `OBTENIDO`. Ninguno se arregló aquí: el revisor reporta y no
coautora. Los dos pesos que la calibración dejó bajo sospecha **no se
ablandaron**, porque la lista se congeló en `aa9a1bb` antes de la
corrida. `tests/check.py --baseline`: **VERDE**, nada nuevo.
