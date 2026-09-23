# ENCARGO · ACTO GEN2-DUELO-ENCIG2025-CIERRE-1 · No es un piloto: es el cierre de la reserva de ENCIG 2025 — los tres cruces que quedan, todos los contendientes a la vez, una comparación primaria, y se acabó la reserva de ese instrumento

> ENTORNO: **CAJA** — abre microdato de ENCIG 2025 (ola reservada) solo con el código congelado en COMMIT-1. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-duelo-encig2025-cierre-1` (D-17) · MODELO: Opus (mide; no bajar) · MODO: RÍGIDO con reserva de evaluación (E.6): tres commits; latitud solo en logística · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: sella tres corridas (una por cruce) + la de adjudicación, `cuenta_gen2: SI`; `celdas_validadas` sube por las celdas-D que registra; adopta solo lo que la firma §2 ya dice (piso no vencido = adjudicado, firma 17/sep) — cualquier retador que venza va a FP, no se adopta aquí.

## 1 · OBJETIVO
Responder la pregunta de mesa («¿por qué seguimos haciendo piloto del piloto?») con hechos: ENCIG 2025 tiene **tres** cruces en reserva (`marcador-segmento.tsv`: `edadxsexo`, `escolaridadxsexo`, y `edadxescolaridad` si FIRMAS-9 no lo consumió ya — se lee del marcador al abrir, no se teclea). Este acto los evalúa todos, con todos los contendientes ya sellados (C2 piso, C-ASTRA ENCIG de #1030 por id, C-ENCOGIDA por la misma regla de λ del piloto 4, C7 si la spec de la casa lo emitió), y deja ENCIG 2025 sin reserva. Después de esto no hay más «pilotos» en ENCIG: la siguiente prueba prospectiva es ENCIG 2027, y su familia la diseña ASTRA-4.
«Hecho» sobre el commit final con origin/main fusionado: `grep -c RESERVADA data/corrida0/marcador-segmento.tsv` filtrado a ENCIG 2025 → 0 · una celda-D por cruce con veredicto sellado y marcador PROSPECTIVA · `CALC-ENCIG-DUELO-2025-*` con sello, asiento y `verify` REPRODUCE · nota con la tabla cruce × candidato × ΔMAE(IC) × dictamen y una frase de producto por cruce.

## 2 · FIRMAS DE MESA
Ya selladas: 17/sep (piso no vencido = estimador adjudicado); E.6 (una apertura sirve a todos los contendientes sellados antes); D1 (todo lo de Astra se utiliza). **Propuesta de firma para lanzar (mesa la da verbatim o la cambia):** «Mesa autoriza abrir los cruces reservados de ENCIG 2025 en un solo acto con todos los contendientes sellados antes del COMMIT-2 (C2, C-ASTRA #1030, C-ENCOGIDA misma regla del piloto 4, C7 si existe); comparación primaria = diferencia de error medio con IC por réplica; umbral = el del piloto 4; vocabulario B-bis del piloto 4. Un retador que venza con IC que despeje va a firma de adopción con su nombre; si nadie vence, la serie de retadores de la casa sobre ENCIG se cierra con ese dictamen y se publica en el informe v1.3.»

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `grep -i encig marcador-segmento.tsv | grep -c RESERVADA` → 3 (edadxescolaridad, edadxsexo, escolaridadxsexo) al `f28d1038`. `[LEÍDO]` FIRMAS-9 P2 debía consumir la adjudicación de `gobierno_digital × edad×escolaridad` (piloto 3, champion C2, F3): si el marcador ya no la muestra RESERVADA al abrir, son dos cruces; si sigue, **se lee la celda-D** `GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` l.84-86: está adjudicada → no se reabre (E.6: cruce visto se declara consumido). Son dos cruces nuevos como máximo; el tercero solo si su celda-D no existe.
- `[EJECUTADO]` #1030 en main (`de7bc272`): `CALC-ASTRA-ENCIG-EDADXSEXO-0001` y `…ESCOLARIDADXSEXO-0001`, inputs `historico_2021/2023`, `marginales_publicos_2025`; recibo #1033 verificó (a)–(c) contra las filas RESERVADA/EMITIDA-SIN-R de ENCIG. Entran por id, no se re-miden.
- `[LEÍDO]` Piloto 4: spec humana, `spec.yaml`, medidor congelado en `5939e9d4`, §6 «misma regla» λ = τ̂²/(τ̂²+σ̄²) re-derivada de deltas históricos; ADENDA-1 con las condiciones (a)–(c) para candidato externo; vocabulario cerrado. **Se hereda por sha**, cambiando solo el instrumento y las variables (por texto de pregunta, A.15). `[LEÍDO]` Encargos del duelo ENVIPE 2026 (`2026-09-21-GEN2-DUELO-ENVIPE2026-CONGELA-1.md`, `-COMMIT-1.md`): patrón de tres commits sobre ola nunca vista.
- `[EXISTE]` `PILOTO-5-ENCOGIDA-ENCIG-1` (`c2a2635c997e846f`) + ADENDA-1 (`5d2e7a0ea21c02bf`), escritos por la sesión anterior, no lanzados, en poder de mesa. **Este encargo los sustituye**; si mesa los prefiere, se lanza aquél y este se archiva como SUSTITUIDO-POR.
- `[SUPUESTO]` ENCIG 2025 tiene réplicas de diseño o factor y estratos suficientes para el bootstrap del árbitro como en 2023. Si no: la spec declara la alternativa antes de COMMIT-1 y el RESULT lleva apellido del instrumento.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -c 'ENCIG-DUELO-2025\|PILOTO-5'` → 0. `git ls-remote --heads origin | grep -i 'piloto-5\|encig2025'` → 0. Piloto 3 ya evaluó un cruce de ENCIG 2025 (celda-D existente): no se repite.

## 5 · PIEZAS (tres commits, E.6)
- **COMMIT-1 (sin microdato de 2025).** Spec humana `forense/prereg-caja/ENCIG-DUELO-2025-cierre-spec-v1_0.md` + `spec.yaml` + medidor congelado + código único autorizado a tocar `encig_2025_encig` con guardia de una sola variable de agrupación (auditoría automática del código y prueba por mutación antes de abrir); lista cerrada de contendientes con sus CALC por id; celdas por texto de pregunta; umbral y regla primaria; qué pasa si el falsador NO refuta (corroborada / acotada / falsador débil) por fila y cuál manda; ejecución diagnóstica declarada si la hay. D-22 completo con salida cruda.
- **COMMIT-2.** Emisiones selladas de C-ENCOGIDA y C7 (las de Astra ya lo están); hashes fijados; nada de 2025.
- **COMMIT-3.** Abre 2025 con el código congelado, sella R, adjudica, registra celdas-D con `champion_actual`, marcador PROSPECTIVA, asientos, dictamen. FP de adopción si un retador vence; NC de retroalimentación a ASTRA-1 en cualquier caso.

## 6 · LATITUD
Solo logística (rutas, entorno, orden de piezas dentro de un commit). Enmienda de cableado (D-18) permitida antes de `ejecucion.json`. Pregunta a mesa (sigues con lo que no dependa): si el marcador y la celda-D discrepan sobre `edadxescolaridad` (§3 primer punto).

## 7 · PAROS — lista cerrada
a) abrir, derivar o imprimir dato de ENCIG 2025 fuera del código congelado en COMMIT-1, o antes de COMMIT-2 · b) reescribir un sello (de Astra, del piloto 3, propio) · c) adoptar un retador aquí · d) cambiar umbral, regla, λ, lista de candidatos o B-bis después de COMMIT-1 · e) NUBE · f) mesa no dio la firma §2, o #1030 no está en main.

## 8 · COMPUERTAS
«COMMIT-1 con guardia y auditoría antes de cualquier lectura de 2025» protege: **abrir dato**. «Contendientes por id; nada se re-mide» protege: **congelar**. «Retador que vence → FP» protege: **adoptar**. «Cruce con celda-D existente no se reabre» protege: **borrar** (un sello del piloto 3).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/ENCIG-DUELO-2025-*`, `data/corrida0/CALC-ENCIG-DUELO-2025-*`, `tools/encig/duelo_2025/` (medidor y guardia), celdas-D nuevas de los cruces abiertos, `replay-evidencia.tsv`/`firmas-pendientes.tsv`/`no-corrido.tsv` (append), nota, L0, cascada. Ajeno: CALC de Astra, celda-D del piloto 3, marcador (derivado), `tramite.yaml`. En vuelo en CAJA: ninguno con reserva (piloto 4 cerró); Codex/Astra pueden correr sin escribir derivados; `codex/astra3-encig-persistencia-1` lee ENCIG 2017–2023 y **no** 2025 — si su rama toca `encig_2025`, PARO (a) y aviso.

## 10 · LO QUE NO HACE · SUCESORES
No evalúa ENVIPE (es ASTRA-ENVIPE-ADJUDICACION-1), no toca ENCIG ≤ 2023, no diseña la familia 2027. Sucesores: firma de adopción si alguien vence; `MISION-ASTRA-4` (familias con reserva para 2027); informe v1.3. Auditoría de rigor extremo: aplica a la nota — PROSPECTIVA en cada cifra, unidad trámite/persona rotulada, sin promediar entre ellas, ¿qué cambia con foco rural/popular?
