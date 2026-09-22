# ENCARGO · ACTO GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1 · La interacción encogida, replicada donde nadie ha mirado: los cruces reservados de evasión de norma en ENVIPE 2025, con C2 ya emitido, persistencia anual y la regla del piloto 3 congelada antes de abrir

> ENTORNO: **CAJA** — abre ENVIPE 2024 (cruces de la ola anterior) y ENVIPE 2025 **solo** en COMMIT-3 por el CALC congelado. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 · CONTADOR: +2 corridas selladas (emisiones, adjudicación), `cuenta_gen2 = SI`, **no adopta**; `celdas_validadas` sube por cada celda PROSPECTIVA (hasta ≈38 si los cuatro grupos siguen reservados: derivado, no prometido) · CALC-ids: `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001`, `…-ARBITRO-CRUCES-0001` · ids raíz de acto.

## 1 · OBJETIVO
Responder la única pregunta que los tres pilotos dejaron abierta con dato a favor: ¿la interacción **encogida hacia cero** (piloto 3: ΔMAE −1.47 pp vs C2, IC [0.44, 2.12], 3/15 celdas) **replica** en otra familia? Celda-D: `tramite.evasion_norma` (ENVIPE 2025), cruces **realmente** reservados de los cuatro `EMITIDA-SIN-R` (`edad×sexo`, `escolaridad_proxy×sexo`, `dominio×sexo`, `edad×escolaridad_proxy`; ≈38 celdas), confirmados por E16 o derivados por objeto. Candidatos: C2 (marginales 2025 sin interacción — la emisión ya existe si el marcador la selló; si no, se sella aquí), C1 (persistencia del cruce 2024, anual), **C-ENCOGIDA** (C2 + λ·I₂₀₂₄ con la **misma regla de λ** del piloto 3, citada verbatim de su spec sellada, sin re-estimar), C7 (interacción promediada 2023–24, la de piloto 2). «Hecho» = tres commits en orden; test de historial (ninguna lectura de los cruces 2025 antes de COMMIT-3); veredicto por cruce con vocabulario cerrado y comparación primaria = diferencia de error medio con IC por réplica; rótulo PROSPECTIVA; B-bis leído.

## 2 · FIRMAS DE MESA
- Ya selladas, se citan: FP-383; A-bis 5/6; FP-385 (piloto 2, diseño); veredicto del piloto 3 (`FALSADOR DÉBIL`, ADR de `GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3`).
- *Propuesta de dirección, mesa sella o borra:* «Se autoriza el piloto 4: `evasion_norma` × los cruces reservados de ENVIPE 2025 que E16 confirme; candidatos C2, C1, C-ENCOGIDA (regla λ del piloto 3, congelada) y C7; sin L; los cruces se derivan solo en COMMIT-3. Un cruce que resulte ya visto sale del piloto y se declara.» Sin texto → PARA.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `marcador-segmento.tsv`: los cuatro grupos `EMITIDA-SIN-R` de `evasion_norma` ENVIPE 2025. `[EJECUTADO]` `edad×dominio` está `CONSUMIDA-SIN-PILOTO` (NC-0328) y `escolaridad×dominio` consumida por el piloto 2: **no entran**. `[EXISTE]` spec sellada del piloto 3 (`CALC-GOB-DIGITAL-EXE-*`, v1.3) con la regla de encogida: no sé su forma exacta ni su λ; **el acto la cita verbatim y la congela sin cambio**.
- `[SUPUESTO]` Ninguno de los cuatro cruces fue derivado por otro acto (Codex descriptivo, duelo). Verificación por id de CALC y `grep` sobre `data/corrida0/`; el que aparezca derivado sale con cita.
- `[SUPUESTO]` La emisión C2 de esos cruces existe sellada (por eso son `EMITIDA-SIN-R`). Si es solo derivada en el marcador y no en un CALC, COMMIT-2 la sella aquí — sigue siendo prospectiva porque R no existe.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-TRA-EVADE-NORMA-CRUCES*` → 0; `grep -rn "evasion_norma.*edadxsexo\|edad × sexo" forense/notas/*cierre*` → reporta. Ramas vivas: `DUELO-ENVIPE2026-MARGINALES-2` (caja) — **este acto arranca cuando aquel fusione**.

## 5 · PIEZAS
- **COMMIT-1:** spec congelada: cruces (lista final por id), desenlace y universo de `ENVIPE-EVASION-NORMA-spec-v1_0` verbatim, receta del árbitro, candidatos con fórmulas (C-ENCOGIDA verbatim del piloto 3), criterio con `INDECIDIBLE` verbatim y comparación primaria con IC por réplica (v2.16 §4), umbral fijado antes, B-bis; guardián de una variable en el control de marginales (E.6); verificación por texto de BP1_20/BP1_23 entre 2023/2024/2025. `spec-check` VERDE; D-22 sintético.
- **COMMIT-2:** emisiones selladas (C1 desde 2024, C7 desde 2023/2024, C2 y C-ENCOGIDA desde marginales 2025 sellados); test de historial. **COMMIT-3:** R de los cruces por el CALC congelado; adjudicación; cobertura por celda y conglomerado; veredicto; celda-D registrada; el marcador la consume (tool de E16).
- **P4 · Lectura para mesa:** si C-ENCOGIDA vence en TRA como en GOB → es el primer retador con réplica y va a firma de adopción; si no → la encogida era de una familia, y se dice.

## 6 · LATITUD
DECIDES TÚ: cuáles de los cuatro grupos entran (los reservados de verdad), orden, cableado D-18. PREGUNTAS A MESA (y sigues hasta COMMIT-3a): si la regla λ del piloto 3 depende de un parámetro de esa familia (p. ej. n por celda), ¿se congela el mismo valor (recomendado) o la misma regla? NO DECIDES: §7.

## 7 · PAROS
**a) cualquier lectura de los cruces 2025 antes de COMMIT-3, scratch incluido** · b) editar lo congelado o forzar · c) adoptar · d) re-estimar λ · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«Firma de §2 presente — protege: abrir dato.» «Lista de cruces confirmada reservada (E16 o por objeto) — protege: congelar spec.» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/TRA-evade-norma-cruces-encogida-spec-v1_0.md` (+ sidecar, yaml) · los dos CALC · celda-D nueva · derivados por comando · `replay-evidencia.tsv` · nota · `canon/L0/<raíz>.md`. Ajeno: specs de pilotos anteriores (lectura), `tramite.yaml`, el marcador (lo consume su tool). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no elicita L, no toca cruces vistos. Sucesor: firma de adopción de C-ENCOGIDA si replica; piloto 5 en ENCIG (los dos cruces reservados de `gobierno_digital`). Auditoría: la spec la trae; la nota la contesta. Cierre por /acto.


