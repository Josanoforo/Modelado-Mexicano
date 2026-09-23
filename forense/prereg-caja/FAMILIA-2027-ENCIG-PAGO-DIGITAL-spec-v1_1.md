# FAMILIA-2027-ENCIG-PAGO-DIGITAL · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENCIG 2027; referencia: 2025; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **trámite del universo C ENCIG MOR (FAC_TRA)**, escala: proporción [0,1]. Estimando único: proporción ponderada de pagos de luz digital/autoservicio P7_3∈{4,5} sobre U_C; RESULT-ENCIG-MOR-C-P-ADOPTA.
- Piso inmutable: `RESULT-ENCIG-MOR-C-P-ADOPTA` de `CALC-ENCIG-0001`, cuyo `sello.json` tiene SHA-256 `9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** n elegible ≥10,000 trámites, ≥100 estratos y ≥1,000 UPM; residuos/códigos fuera de la partición ≤1% del peso elegible; sin unidad sin FAC_TRA. En ENCIG 2025: U_C n=20,203, 441 estratos, 8,486 UPM; residuo=189 filas, pero el CALC no registra su masa ponderada: el límite de 1% es comprobación futura, no dato ya acreditado. Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** Mantener como residuo aparte los canales no incluidos y NS/NR/blancos; no recodificarlos a presencial/digital. Pérdida de FAC_TRA o clave de diseño excluye la unidad del IC y se reporta; si supera 1% del peso elegible, NO-ESTIMABLE. No deduplicar sin aplicar la llave ID_TRA+NT_TIPO verificada.
- **Comparabilidad:** Mismo servicio luz, evento de pago, unidad trámite, canal digital={4,5}, no adopta={1,2,6}, universo C, FAC_TRA y llaves de evento. Canal nuevo/ambiguo conserva residuo; si cambia el significado de pago o la unidad/denominador, NO-COMPARABLE. No interpretar el resultado como digitalización general.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

CALC-ENCIG-0001 conserva IC95 [0.662900,0.684530], bootstrap de UPM dentro de estrato (2,000 réplicas); 8 estratos de UPM única, de modo que el IC es límite inferior de anchura verdadera. No se guardaron las réplicas; el IC marginal no da varianza del error contra el punto fijo. Hace falta vector futuro por réplica y n efectivo para IC de error/potencia.

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Fecha y cuestionario oficial confirmados; misma definición de evento y servicio; instrumento mantiene identificación de estrato, UPM, FAC_TRA y tipo de evento. Apertura compartida con ENCIG-SOLICITUD-MORDIDA.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
