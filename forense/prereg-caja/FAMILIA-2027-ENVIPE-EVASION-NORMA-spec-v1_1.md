# FAMILIA-2027-ENVIPE-EVASION-NORMA · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENVIPE 2027; referencia: 2025; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **delito con BP1_20∈{1,2} y FAC_DEL**, escala: proporción [0,1]. Estimando único: proporción conjunta ponderada evade_norma = (BP1_20=2 y BP1_23∈{04,05,06,08}) sobre delitos con BP1_20∈{1,2}, FAC_DEL; RESULT-EVASIONNORMA-A-P-EVADE.
- Piso inmutable: `RESULT-EVASIONNORMA-A-P-EVADE` de `CALC-EVASION-NORMA-0001-v1_1`, cuyo `sello.json` tiene SHA-256 `8076d9ff1e18ab1fe6ac7168600810580cabe99c1df9373ee21c8b40e9d2abe8`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** n delitos válidos ≥10,000, ≥100 estratos y ≥1,000 UPM; cero sin BP1_20, BP1_23, FAC_DEL o diseño. ENVIPE 2025: n=40,280, numerador=21,761 y 10,694 UPM; el CALC no conserva conteos de estratos/UPM únicos, que se exigirán al futuro ejecutor. Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** Es tasa conjunta en todo el universo BP1_20∈{1,2}; BP1_23 sólo clasifica a no denunciados. Valores vacíos/código no válido se informan como faltante y nunca se imputan a 0. Si faltantes del disparador o desenlace superan 1% del peso potencial o la ausencia impide distinguir skip legítimo de pérdida, NO-ESTIMABLE.
- **Comparabilidad:** Misma unidad delito, disparador BP1_20, códigos normalizados BP1_23, FAC_DEL, EST_DIS/UPM_DIS y categorías {04,05,06,08}. No comparar con el derivado persona/U4 ni con el condicional entre no denunciantes (no estimable en la spec vigente). Cambio en categorías que definen norma: NO-COMPARABLE.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

spec legado declara bootstrap de conglomerado estratificado, 10,000 réplicas, seed 42; punto 0.562774, IC95 [0.551982,0.573448], n=40,280. Sin vector guardado, no se deriva IC del error ni potencia; el futuro CALC debe exportar por réplica el resultado R y diferencia con piso. Se requieren n efectivo y conteos de estratos/UPM únicos.

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Condiciones comunes ENVIPE; verificar equivalencia BP1_20/BP1_23, categorías, universo de delitos y pesos de 2025. Una apertura compartida con denuncia-U4; mantener dos outcomes y sus soportes separados.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
