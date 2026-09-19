# DISEÑO A · CELDA-D PILOTO 3 · v1.0
**Autor:** diseñador (A), sesión nueva de Claude Opus, a ciegas. **Base declarada por el brief:** origin/main = 8e455bd6, 19/sep/2026 21:10 UTC (brief v1.1).
**Procedencia (§2 instrucciones):** no clono repo ni abro microdato en esta sesión. Toda cifra que uso es **lectura tipo (3), reportada por el brief** (ADR-538, ADR-542, #871/#873/#874, marcador-segmento.tsv) y viaja como premisa **a verificar por quien ejecute**, no como hecho verificado aquí. Nada se deriva del espejo del proyecto.

---

## 0 · Respuesta a la pregunta estratégica (§3.6) — va primero porque condiciona el resto

**No son excluyentes y el orden importa: primero el compuesto, después el piloto, y el piloto sólo en un dominio nuevo.**

Emitir C2 compuesto para los 22 cruces RESERVADA **no es colar adopción** siempre que se cumplan tres candados, y con ellos **es la medición de más valor hoy**:
1. Estado **EMITIDA-SIN-EVALUAR** en el campo del marcador (A.16: token por prefijo, no prosa), distinto de ADOPTADO-POR-FIRMA. Ningún consumidor del motor puede leer una sin ver la otra.
2. **No consume reserva** porque sólo compone marginales sellados; se asienta explícitamente en el CONTADOR que ninguna ola reservada se abrió, y el cruce sigue RESERVADA para evaluación.
3. **Prohibición de re-sello por conveniencia:** la emisión compuesta no puede convertirse en adoptada por uso; sólo por un piloto que la evalúe fuera de muestra, o por firma de mesa que declare el alcance (A.10).

Sin esos candados, sí es colar adopción, y entonces la respuesta correcta sería "ninguna celda; primero lo otro".

Valor relativo, honesto: un tercer piloto que repita ENIF/ENVIPE tendría **valor informativo bajo** — sería la tercera corroboración del mismo hallazgo en el mismo tipo de dominio. El piloto sólo gana valor si **cambia el universo**: dominio no pilotado y unidad del dato distinta. Por eso el piloto 3 que propongo es ENCIG 2025 (unidad trámite), y sólo ése.

---

## 1 · Celda-D propuesta (§3.1)

**Estimando, primera línea:** proporción de **trámites** (no de personas) con el desenlace del árbitro, en el universo ENCIG 2025 **restringido a trámites realizados**, por celda del cruce **edad × escolaridad**. Unidad del dato: **trámite** (A-bis 3). Un estimando restringido a trámites no se compara contra ninguno poblacional ni contra ENIF/ENVIPE sin función de enlace (A-bis 3/4): la comparación entre pilotos es **sólo de MAE del método**, nunca de niveles.

- **Instrumento:** ENCIG 2025. **Cruce:** edad × escolaridad (RESERVADA, no consumido). **Categorías:** las del piso marginal ENCIG 2023 (#871), heredadas sin recodificar, para que C1 y C2 vivan en la misma rejilla; si la ola 2025 cambió cortes, eso es PARO-PREMISA y se reporta, no se ajusta.
- **Por qué éste y no ENIF/ENVIPE:** (a) dominio no pilotado → tercer orden institucional (oferta del Estado), no repetición; (b) es el **único** cruce reservado cuyos **dos ejes** tienen piso t−1 en la misma unidad (ENCIG 2023, 10 celdas marginales, brecha 2 años), así que **C1 existe para el cruce entero**; (c) en ENVIPE 2025 el eje dominio ya está quemado (edad × dominio, NC-0328) y en ENIF el t−1 es 2021, dato de pandemia con brecha 3 años.
- **Soporte esperado sin mirar el cruce:** producto de los marginales sellados ENCIG 2023 por eje × n de trámites de la ola, con el supuesto de independencia que el propio C2 asume. Es una **cota de planeación, no una estimación**, y se declara así en COMMIT-1. Si esa cota anticipa menos de 8 celdas por encima del soporte mínimo, la celda **no se lanza** y el entregable es ese hueco.

## 2 · Retadores, declarados antes del dato (§3.2)

Piso y retadores se emiten en la misma corrida, misma escala (logit), mismo universo.

- **C2 (piso, siempre):** p̂(a,b) = expit(logit p(a) + logit p(b) − logit p), marginales ENCIG **2025** (misma ola, sin interacción).
- **C1 (piso de persistencia):** C2 pero con marginales **ENCIG 2023** por eje (t−1). Es piso, no retador: acota, no identifica.
- **C3 — interacción agregada (un solo parámetro):** p̂ = expit(logit p(a)+logit p(b)−logit p + δ̂·s(a,b)), con **δ̂ único** para toda la rejilla, no por celda, estimado **sólo de ENCIG 2023** (y 2021 si el inventario la cubre en la misma unidad; si no la cubre, se declara y se usa 2023 sola). s(a,b) = signo esperado del gradiente monótono edad→escolaridad fijado en COMMIT-1.
- **C4 — interacción por celda encogida:** δ̂_shrunk(a,b) = λ·δ̂_prev(a,b), con **λ = τ̂²/(τ̂² + σ̄²)** calculado **íntegramente en olas previas** (τ̂² = varianza entre celdas de las interacciones previas; σ̄² = varianza muestral media de esas mismas interacciones). λ queda **congelado como constante numérica en COMMIT-1**, derivado en la sesión y no tecleado (§2 instrucciones); ver la ola reservada para fijar λ invalidaría el piloto.
- **Incertidumbre:** bootstrap con el diseño complejo de ENCIG (estratos/UPM y ponderador de trámite), B = 1000, semilla fijada en COMMIT-1. La incertidumbre de δ̂_prev **se propaga** al IC de C3/C4 (bootstrap anidado sobre las emisiones previas); un retador que llegue sin IC no compite.

## 3 · Adjudicación (§3.4)

- **Métrica:** MAE en puntos porcentuales contra el cruce directo de la ola reservada, sobre celdas que pasan soporte.
- **Soporte mínimo:** n **sin ponderar** ≥ 100 trámites por celda. Celdas por debajo se reportan y **no entran al MAE**. Si pasan < 8 celdas → **NO-CONSTRUIBLE**, sin veredicto (E.5).
- **Vence a C2** sólo si: ΔMAE ≥ **0.30 pp** a favor del retador **y** el IC95 bootstrap de ΔMAE excluye 0.
- **INDECIDIBLE:** punto que cumple el umbral con IC que no lo despeja → **propuesta con reserva**, no adjudica (§4 instrucciones). Se asienta como tal y no se adopta.
- **SIN-CANDIDATO-SUPERIOR** si ningún retador cumple ambas condiciones. El piso se mantiene adoptado por firma.

## 4 · B-bis · pre-registro de falsación (§3.5)

- **Si nadie vence a C2 (tercera vez):** **corroborada y acotada** — corroborada en un tercer dominio y una tercera unidad del dato; **acotada** a cruces de dos ejes estructurales con marginales de la misma ola y ≥8 celdas con soporte. No se lee como corroboración general del método ni se extiende a cruces de tres ejes, ni a región/condición indígena (fuera de la rejilla, límite declarado).
- **Si C3 vence:** falsa el "sin interacción" en este dominio; C3 entra como **candidato** para la celda ENCIG, sin destituir a C2 en ENIF/ENVIPE (A.10: el sello viejo no se edita).
- **Si C4 vence y C3 no:** el hallazgo es sobre **encogimiento**, no sobre interacción: la señal previa sirve sólo atenuada; se reporta así.
- **Si vence uno pero el otro queda INDECIDIBLE:** manda el que cumple; el otro se asienta como reserva.
- **Si sólo pasan 8–9 celdas:** puede cumplirse "corroborada" y "falsador débil" a la vez. **Manda falsador débil:** soporte escaso descalifica la corroboración. Esta cláusula se sella ahora.

## 5 · Regla de uso del error de persistencia, escrita a ciegas (§3.7)

CALC-PISO-PERSISTENCIA-ERROR-0001, leído **sólo para ENCIG (brecha 2 años)**:

- **Mayoría de ejes PERSISTE:** **sigo con ENCIG edad × escolaridad**, y C1 sube de piso auxiliar a **segundo piso reportado**; C3/C4 conservan su margen porque la interacción de 2023 gana credibilidad, pero λ **no se recalcula** (queda el de COMMIT-1).
- **Mayoría de ejes CAMBIA (IC95 que excluye 0):** C1 **sale** como piso —no puede acotar lo que se movió— y C3/C4 **pierden margen**, porque su insumo es exactamente la ola que se movió; el umbral de victoria sube de 0.30 a **0.50 pp** para cualquier retador que use señal de 2023.
- **Si además ≥ 2 de los 2 ejes del cruce CAMBIAN con signo discordante entre sí:** **me muevo**: retiro ENCIG edad × escolaridad y propongo ENVIPE 2025 escolaridad_proxy × sexo, cuyo t−1 tiene brecha de 1 año. Lo declaro ahora para que el careo no lo lea como racionalización posterior.
- **Si el CALC no sella a tiempo:** el piloto **no arranca**; se emite el C2 compuesto de §0 y se difiere (A.14, DIFERIDO-A).

## 6 · Lo que este diseño NO hace

No abre microdato, no deriva cruces, no toca reservas distintas de ENCIG 2025 edad × escolaridad, no propone región ni condición indígena (fuera de la rejilla del árbitro), no interpreta ninguna interacción como psicología de segmento: si aparece, es **asociación** en escala logit, en el universo trámites-ENCIG-2025, con tamaño de efecto (H5, §3 instrucciones). No compara niveles entre pilotos.

## 7 · Tres commits (E.6, heredado sin discutir)

COMMIT-1: spec.yaml + sidecar humano, con categorías, λ numérico, semilla, umbrales, soporte mínimo y la guardia de una sola variable de agrupación; **sin microdato**. COMMIT-2: emisiones selladas de C1/C2/C3/C4 y del cruce directo, sin R. COMMIT-3: R, adjudicación, B-bis resuelto. Nada en scratch. Un R antes del COMMIT-2 degrada esto a factibilidad y se declara.
