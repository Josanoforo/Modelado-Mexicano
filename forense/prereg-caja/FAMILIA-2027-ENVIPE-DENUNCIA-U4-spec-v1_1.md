# FAMILIA-2027-ENVIPE-DENUNCIA-U4 · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENVIPE 2027; referencia: 2025; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **persona víctima en U4 con FAC_ELE**, escala: proporción [0,1]. Estimando único: proporción persona de motivo C2 de no denuncia en U4, FAC_ELE; RESULT-ENVIPE-DEN-P-C2-U4.
- Piso inmutable: `RESULT-ENVIPE-DEN-P-C2-U4` de `CALC-ENVIPE-0001`, cuyo `sello.json` tiene SHA-256 `18310f8adb6fb5963038d67c2e8a7eaba50e09c062dddbc579e918f090cbde16`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** n personas U4 ≥5,000, ≥100 estratos y ≥1,000 UPM; cero sin FAC_ELE/diseño. ENVIPE 2025 U4: n=13,023, masa FAC_ELE=14,982,594; el método tiene 83 estratos de UPM única en U1, por lo que su IC subestima anchura verdadera y sirve como diagnóstico, no prueba de calibración. Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** Preservar la regla C2/U4 completa, códigos y exclusiones de personas/delitos del CALC. NS/NR/blanco/fuera de universo nunca se convierten a no denuncia. Si falta un componente del universo, el código de motivo o FAC_ELE, NO-ESTIMABLE; publicar conteos de no respuesta y U4 sin ajustar el punto.
- **Comparabilidad:** Mismo dominio U4/persona, persona con ≥1 delito elegible U1, codificación C2, FAC_ELE y diseño de tper_vic2. No sustituir FAC_DEL/U1 (unidad delito). Requiere verificar BP1_23/FAC_ELE y saltos del cuestionario. Cambios en esas piezas o en la composición U4: NO-COMPARABLE.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

Histórico: CALC-ENVIPE-0001 declara 2,000 réplicas (seed 20260909/PCG64) y conserva IC95 [0.283020,0.305799], n=13,023 U4, pero ningún vector de réplicas; 83 estratos con una UPM en U1 generan varianza cero. Los conteos de diseño se publican para U1, no U4; la exigencia futura ≥100 estratos/≥1,000 UPM es una verificación nueva específica del universo U4. La proporción de estratos únicos específica U4 no está declarada. No usar su cobertura como evidencia calibrada. Hace falta archivo futuro de réplicas U4 y n efectivo; no recomputar desde extremos.

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Fecha/cuestionario confirmados, código C2 y universo U4 cotejados con la ficha vigente del instrumento. Abrir una sola vez la ola ENVIPE para ambas familias U4, sin abrir ENVIPE 2026 ni microdato de olas reservadas durante esta continuación.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
