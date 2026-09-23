# FAMILIA-2027-ENIF-HORIZONTE-AHORRO · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENIF 2027; referencia: 2024; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **persona de 18+ (estimando derivado de tres proporciones ENIF)**, escala: proporción [0,1]. Estimando único: proporción de ambas vías de ahorro según HVD: solo formal + solo informal − tiene ahorros; identidad y denominadores fijados por CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1.
- Piso inmutable: `RESULT-HVD-A-AMBAS-VIAS` de `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1`, cuyo `sello.json` tiene SHA-256 `1c8b329fb2088d24298acb3081e9bb2d2366dce05c6e238d282271d251d92609`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** n común de referencia ≥10,000 personas 18+; denominadores/olas armonizados y cada componente identificable. ENIF padre: n=13,502, 190 estratos y 2,164 UPM. El derivado no tiene su propio n efectivo. Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** No imputar ni renormalizar componentes. Si falta cualquier componente o cambia el universo de una de las tres fuentes futuras, no calcular HVD y dictaminar NO-ESTIMABLE; publicar conteos y componentes disponibles como diagnósticos sin sustituir el primario.
- **Comparabilidad:** Requiere invariancia de la definición de ahorro formal, informal y tenencia total, con mismas personas y periodo de referencia. El resultado histórico es aritmética determinista sobre tres proporciones selladas, no estimación conjunta: CALC declara expresamente que no hay IC95 propio por falta de covarianza entre corridas. La futura evaluación no lo llamará calibrado ni comparará R con un IC histórico.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

No existe vector de réplicas conjuntas ni covarianza entre insumos sellados, ni n efectivo del derivado; no se puede estimar varianza histórica o potencia sin reabrir/recalcular bajo una nueva unidad autorizada. Hace falta archivo de réplicas conjuntas de los tres componentes (mismo esquema de UPM/estrato) o medición futura diseñada para estimar directamente la proporción conjunta. No combinar extremos de IC.

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Condiciones comunes de ENIF, más prueba de que el instrumento futuro identifica los tres componentes bajo el mismo universo y permite estimar directamente HVD. Si sólo es posible reconstruir una suma de marginales sin unión individual, NO-ELEGIBLE.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
