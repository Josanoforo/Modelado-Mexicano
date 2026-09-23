# FAMILIA-2027-ENIF-AHORRO-FORMAL · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENIF 2027; referencia: 2024; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **persona de 18+**, escala: proporción [0,1]. Estimando único: proporción ponderada de personas 18+ con ahorro formal (denominador compartido B de ENIF AHO; FAC_PER).
- Piso inmutable: `RESULT-ENIF-AHO-B-P-FORMAL-P` de `CALC-ENIF-0001`, cuyo `sello.json` tiene SHA-256 `0c90801873c91ac109219fbe3bf88632fc6aa8a6bcef637f9876398e95f76de6`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** n no ponderada ≥ 10,000; ≥150 estratos y ≥1,000 UPM utilizables; cero personas sin peso/diseño; el CALC 2024 tiene n=13,502, 190 estratos, 2,164 UPM y cero sin diseño. Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** Conservar el denominador B fijado por FAC_PER válido; clasificar el código de ahorro exactamente como en el cuestionario 2024. Respuesta NS/NR o blanco queda fuera del numerador, no se imputa como no ahorro; reportar n y masa de ponderador excluidos. Si no puede reconstruirse el mismo dominio, NO-ESTIMABLE.
- **Comparabilidad:** Mismo universo persona 18+, reactivo y categorías que definen ahorro formal, FAC_PER y regla de dominio. Recodificación que conserve significado y partición documentable: sensibilidad descriptiva sin cambiar la primaria. Cambio de universo, ponderador o concepto: NO-COMPARABLE.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

El padre guarda IC95 por bootstrap de UPM dentro de estrato: [0.274161, 0.296777], 190 estratos, 2,164 UPM, sin estrato de UPM única; no guarda las réplicas. La media del IC no mide incertidumbre del error prospectivo ni potencia. Hace falta el vector de réplicas futuras emparejadas con el piso fijo y n efectivo para IC del error/potencia.

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Fecha oficial de publicación dentro de 23/sep/2026–23/mar/2028; cuestionario público cotejado; ninguna ola intermedia cambia la identidad del estimando; especificación técnica y código congelados antes de abrir esa única ola.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
