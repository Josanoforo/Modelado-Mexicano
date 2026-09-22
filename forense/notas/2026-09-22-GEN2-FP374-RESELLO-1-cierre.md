# Nota de cierre · ACTO GEN2-FP374-RESELLO-1 · ADR-260922-GEN2-FP374-RESELLO-1-dfbe-01

## P1 · Universo actual de FP-374

- **Qué preguntaba** (verbatim de la fila original, 11/sep): si autorizar el piloto de transferencia F5 — snapshot 712, 10 familias fuente-estimando/16 celdas, 0 con rol retenido ejecutable de las 18 disjuntas exigidas (6 piloto + 12 confirmatorias). Recomendación original: NO AUTORIZAR.
- **Panel con el que se firmó**: F-16 (15/sep) firmó con **7 retenidas** del panel `F5-panel-candidatos-v1_1.tsv` (13 filas: 7 RETENIDA, 5 EXPUESTA, 1 INDETERMINADA), y solo 2 realistas para piloto (R01-MOCIBA, R02-WBES condicionada a firma de unidad).
- **Panel que hay hoy**: `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv` (PR #815) redujo 7→2 ejecutables; `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml:125,128` (PR #825) deja **0 elegibles**: R01-MOCIBA `CANDIDATO-NO-ELEGIBLE`. **Corrección post-revisión (§ Corrección post-revisión, abajo):** R09-ISSP NO es `CONDICIONADA` — cita re-derivada (`tarjetas.yaml:209,257`, tarjetas `R09-ISSP-2017-SEX-1/2`) muestra `enlace_M.estado: CANDIDATO-NO-ELEGIBLE` y `reserva.estado: EXPUESTA-OBJETIVO` (ya vio incidentalmente la distribución objetivo de v26 — pretensión de evaluación ciega retirada). `CONDICIONADA` es una cita heredada de una enmienda previa de `ACTO GEN2-TRAMITE-4` (16/sep, ya sellada en `data/corrida0/decisiones.tsv:118` y en `FP-380`/`NC-0283`, no editadas aquí) que este acto reprodujo sin re-derivar (A.8) hasta que `/revisa` lo señaló sobre el PR. El estado real es igual o más restrictivo que "CONDICIONADA": **0 elegibles y cero llamadas autorizadas se sostienen, con más margen.** Esta cadena (7→2→0) ya la asentó `ACTO GEN2-TRAMITE-4` (16/sep) y la reasignó a mesa MOTOR `GEN2-TRAMITE-FIRMAS-3` (21/sep, firma B5), junto con NC-0161/0162/0234/0237.
- **Qué han respondido desde entonces los duelos con ola reservada** (leídos verbatim):
  - `forense/encargos/2026-09-21-GEN2-DUELO-ENVIPE2026-CONGELA-1.md` (PARTE A/B, RÍGIDO, `reserva:envipe2026` en `data/corrida0/decisiones.tsv:181`): compite `piso` contra retadores generados por matriz.g/θ — K, T3, T5/TC, Sλ/P/S1/AP — sobre ENVIPE 2026 (unidad **delito**, marginales por eje y cruces nacionales). No cita F6, M, L_SOLO ni B en ningún punto del encargo.
  - `forense/encargos/2026-09-22-GEN2-ENIGH2024-DUELO-COMMIT-2-3.md` (sellado; `reserva:enigh2024-remesas-nacional-liberada`, `data/corrida0/decisiones.tsv:212`): compite persistencia/C-PISO contra C-MEDIA y tendencias sobre ENIGH 2024, estimando remesas>0 (unidad **hogar**). Tampoco cita F6, M, L_SOLO ni B.
  - Ambos son el mecanismo de **E.6** (ola nueva de una encuesta **con historia en el corpus**, RESERVADA al entrar al manifiesto), no el panel de **familias de encuesta nunca usadas para afinar M** (MOCIBA/WBES/OECD-Trust/ENJUVE) que F6/FP-374 exigían.

**Conclusión de P1:** el `[SUPUESTO]` del encargo resulta **FALSO**. Los duelos con ola reservada responden una pregunta de generalización temporal/de muestra dentro de un dominio ya modelado (delito, remesas), no la pregunta de transferencia de M a un dominio/familia nunca vista que F6 planteaba. Se toma la rama prevista por el encargo para este caso.

## P2 · Sello nuevo

Dictamen (vocabulario cerrado): **`EN-ESPERA-PANEL`**. FP-374 recibió sucesor `FP-260922-GEN2-FP374-RESELLO-1-dfbe-01` (`forense/firmas-pendientes.tsv`, fila añadida; FP-374 no se editó salvo el sucesor apuntado en `ejecutada_en`, enmienda fechada 2026-09-22, patrón ya usado por las enmiendas previas de esa misma fila). Fila espejo en `data/corrida0/decisiones.tsv` (objeto `FP-374:alcance`) con la firma de §2 del encargo, verbatim.

La FP-encargo `FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-01` queda `CERRADA`.

## P3 · NC-0161 / NC-0162 / NC-0237

- **NC-0161 y NC-0162**: `ABIERTA`, sucesor actualizado (enmienda fechada 2026-09-22) para citar el sello nuevo por id y nombrar la acción concreta que las destraba, tomada de `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv` (prioridad 1, `MONTAJE-DE-RAIZ`, cero descargas): leer en CAJA el FD de MOCIBA 2021/2023 (ids en manifiesto: `mociba_2021_mociba2021_fd` línea 9291, `mociba_2023_mociba2023_fd` línea 9550) para fijar la batería de denuncia; y, en paralelo, R09-FAM-ISSP (`za6980_q_mx`, línea 11485, ya en la raíz compartida) para leer la categoría de respuesta de v26. Tres ids verificados por manifiesto, conteo = 3 (A.15).
- **NC-0237**: sigue `CERRADA` — no se reabre. Enmienda fechada 2026-09-22: con el sello nuevo, la condición de su fila («no se decide mientras F6 esté en espera de acreditación») sigue vigente sin cambio de fondo, porque el dictamen es `EN-ESPERA-PANEL`, no `SUPERADA`.

## P4 · Lo que hereda el informe

`canon/informe-programa-v1_2.md` **no tiene hoy** una sección «Transferencia de M (F6)» — se verificó con `grep -n "F6\|Transferencia" canon/informe-programa-v1_2.md`, cero coincidencias; su §4 real es «Qué puede afirmar el producto hoy, y qué no» y no menciona F6. Premisa de logística que no se sostuvo: el encargo asumía una sección existente por nombrar; el objetivo (dejar dicho cómo leerla) sigue alcanzable declarando lo que hay, no editando el informe (perímetro ajeno). Para cuando el informe incorpore F6:

1. F6 no está `SUPERADA` por los duelos ENVIPE 2026/ENIGH 2024: son un mecanismo distinto (E.6, ola reservada de encuesta con historia), no evidencia sobre transferencia de M a una familia nueva.
2. El panel F6 (`F5-panel-candidatos-v1_3.tsv`, `tarjetas.yaml`) sigue en 0 elegibles; no se autorizan llamadas.
3. Lo que destraba F6 es adquisición-cero (lectura de FD ya en manifiesto: MOCIBA 2021/2023, ISSP v26), no una decisión de dirección ni presupuesto nuevo.

## Auditoría de rigor extremo

No aplica — este acto no afirma nada sobre México; afirma sobre el estado de una firma (§5 del cuerpo normativo, sección "Estructura de artefactos").

## Contador

Cero mediciones. Mueve el tablero de firmas: una FP `VENCIDA-EN-ALCANCE` recibe sucesor sellado (FP-374 → FP-260922-GEN2-FP374-RESELLO-1-dfbe-01); una FP-encargo cierra (FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-01); dos NC (NC-0161, NC-0162) actualizan sucesor sin cambiar estado (siguen ABIERTA); NC-0237 recibe enmienda sin reabrir. `celdas_validadas`, `adoptados_activos` y `N_corridas_selladas` no se movieron.

## Corrección de fuente (mid-acto, antes de cerrar)

El 0-bis original archivó el encargo desde el texto pegado en el mensaje que invocó `/acto`. El operador envió después el adjunto `.md` real (`f91ea315-ENCARGO-GEN2-FP374-RESELLO-1-2026-09-22.md`), que es la fuente que §0 exige. `diff` normalizado (viñetas y envoltura de párrafo aparte) mostró **cero diferencia normativa** entre ambos textos. Se corrigió antes de cerrar: `forense/encargos/2026-09-22-GEN2-FP374-RESELLO-1.md` se sobrescribió con el verbatim del adjunto y su sidecar `.cuerpo.sha256` se recalculó sobre el mismo commit de 0-bis (rama propia, aún no fusionada, sin otra sesión que dependa del sello viejo) — no es el caso que la regla "el sello no se regenera nunca" prohíbe (regenerar para pasar un verificador sobre un sello ya público); es corregir la fuente antes de que exista un sello consumido por nadie más. Una línea en `forense/hallazgos.md` lo declara (§1: defecto sin impedir medir).

## Corrección post-revisión (`/revisa` PR #998, Hallazgo 1)

`/revisa` señaló que "R09-ISSP `CONDICIONADA`" no aparece en `tarjetas.yaml` — cero coincidencias del literal `CONDICIONADA` en el archivo (271 líneas). Re-derivado: `tarjetas.yaml:180-271` (tarjetas `R09-ISSP-2017-SEX-1` y `-SEX-2`) trae `enlace_M.estado: CANDIDATO-NO-ELEGIBLE` (mismatch de constructo: recepción efectiva de dinero ≠ intención hipotética de pedir prestado) y `reserva.estado: EXPUESTA-OBJETIVO` (la distribución objetivo de v26 apareció incidentalmente durante la búsqueda documental; se retiró toda pretensión de evaluación ciega). Las líneas 125/128 que el encargo cita pertenecen íntegramente a la tarjeta `R01-MOCIBA-2021`, no a R09.

`CONDICIONADA` es una cita heredada: aparece primero en la enmienda de `ACTO GEN2-TRAMITE-4` (16/sep/2026), ya sellada en `data/corrida0/decisiones.tsv:118`, `forense/firmas-pendientes.tsv:FP-380` y `forense/no-corrido.tsv:NC-0283` — ninguna de las tres se edita aquí (A.10: el desajuste queda como hallazgo, no como reescritura de lo sellado). Este acto la reprodujo verbatim en su propio texto nuevo (§3 `[LEÍDO]` del encargo, la fila FP sucesora y esta nota) sin re-derivarla contra `tarjetas.yaml` — exactamente el defecto que 2.5 exige atrapar. Corregido en `forense/firmas-pendientes.tsv` (fila `FP-260922-…-dfbe-01` y enmienda propia a `FP-374`) y en esta nota; `forense/encargos/2026-09-22-GEN2-FP374-RESELLO-1.md` no se toca (verbatim sellado, A.3 — el error es del encargo original, no de la ejecución).

**No cambia el dictamen.** `CANDIDATO-NO-ELEGIBLE` + `EXPUESTA-OBJETIVO` es igual o más restrictivo que `CONDICIONADA`: "0 elegibles", "cero llamadas autorizadas" y el dictamen `EN-ESPERA-PANEL` se sostienen con más margen. Una línea en `forense/hallazgos.md` lo declara.

**Nota para el sucesor de NC-0161 (adquisición dirigida).** La acción concreta que se nombró para R09-FAM-ISSP en `NC-0161`/`NC-0162` (leer `za6980_q_mx` para fijar la categoría de respuesta de v26) sigue siendo válida como trabajo de *codificación* (`definicion.estado: CODIFICACION-INTEGRADA-NO-ACREDITADA`), pero no reabre la elegibilidad de las dos celdas ya construidas (`R09-ISSP-2017-SEX-1/2`): esas están `CANDIDATO-NO-ELEGIBLE` por mismatch de constructo, no por codificación, y además `EXPUESTA-OBJETIVO`. Cualquier celda R09 nueva que el acto sucesor construya tendría que partir de un diseño ciego distinto — se declara para que el sucesor no repita el mismo error de lectura.
