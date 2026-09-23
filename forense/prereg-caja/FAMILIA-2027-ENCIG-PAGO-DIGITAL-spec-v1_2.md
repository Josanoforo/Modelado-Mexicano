# FAMILIA-2027-ENCIG-PAGO-DIGITAL · spec humana condicional v1.2

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENCIG 2027; referencia: 2025; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **trámite del universo C ENCIG MOR (FAC_TRA)**, escala: proporción [0,1]. Estimando único: proporción ponderada de pagos de luz digital/autoservicio P7_3∈{4,5} sobre U_C; RESULT-ENCIG-MOR-C-P-ADOPTA.
- Piso inmutable: `RESULT-ENCIG-MOR-C-P-ADOPTA` de `CALC-ENCIG-0001`, cuyo `sello.json` tiene SHA-256 `9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.
- **Numerador y denominador:** Numerador = suma(FAC_TRA) de trámites del universo U_C con P7_3∈{4,5}. Denominador = suma(FAC_TRA) de trámites tipo 01 (N_TRA=1) con P7_3∈{1,2,4,5,6} y FAC_TRA finito >0. Códigos 3,7,8,9 y blanco quedan fuera del denominador, se cuentan y se ponderan como residuo; en particular NS/NR/blanco no se recodifican a canal presencial o digital.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo: dos unidades por cada cien en la escala del estimando. Se elige como margen absoluto pequeño, redondo, común y fácil de interpretar entre tasas base muy distintas; usar un margen relativo haría variar el error tolerado entre familias. Es una decisión práctica, no una conclusión empírica, ni precisión/potencia acreditada, equivalencia psicológica o la tolerancia numérica del CALC. Reportar siempre error absoluto y signo.
- **Soporte mínimo propuesto:** n elegible ≥10,000 trámites, ≥100 estratos y ≥1,000 UPM; residuos/códigos fuera de la partición ≤1% del peso elegible; sin unidad sin FAC_TRA. En ENCIG 2025: U_C n=20,203, 441 estratos, 8,486 UPM; residuo=189 filas, pero el CALC no registra su masa ponderada: el límite de 1% es comprobación futura, no dato ya acreditado. Justificación operativa: n=10,000 es 49% del n histórico 20,203; ≥100/441 estratos y ≥1,000/8,486 UPM fijan un piso conservador de cobertura de diseño, no una precisión calculada. El límite de residuo 1% también es un gate operativo, pendiente de masa ponderada. Los conteos/estratos/UPM mínimos filtran soporte muy ralo y permiten exigir presencia suficiente de diseño; no certifican precisión, potencia, cobertura nominal ni suficiencia para detectar 2 pp. Además, el IC futuro requiere ≥1,000 réplicas válidas de 2,000 y denominador válido en ≥95% de réplicas. Incumplimiento: `NO-ESTIMABLE`; no relajar tras R.
- **Faltantes:** Mantener como residuo aparte los canales no incluidos y NS/NR/blancos; no recodificarlos a presencial/digital. Pérdida de FAC_TRA o clave de diseño excluye la unidad del IC y se reporta; si supera 1% del peso elegible, NO-ESTIMABLE. No deduplicar sin aplicar la llave ID_TRA+NT_TIPO verificada.
- **Comparabilidad:** Mismo servicio luz, evento de pago, unidad trámite, canal digital={4,5}, no adopta={1,2,6}, universo C, FAC_TRA y llaves de evento. Canal nuevo/ambiguo conserva residuo; si cambia el significado de pago o la unidad/denominador, NO-COMPARABLE. No interpretar el resultado como digitalización general.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Primero resuelve la compuerta: si el estimando/universo/unidad/códigos/pesos no son equivalentes, `NO-COMPARABLE`; si falta soporte, dato para el contraste o un IC válido conforme al diseño, `NO-ESTIMABLE`. Un estrato de una UPM que aporte varianza cero deja el IC como límite inferior de anchura; salvo que antes de abrir se haya fijado un método de varianza válido para ese caso, no sirve para dictaminar y queda `NO-ESTIMABLE`. Sólo con ambas compuertas superadas y un intervalo finito ordenado se asigna exactamente una etiqueta estadística.
2. Ejecutar bootstrap de UPM dentro de estrato con el diseño oficial. Compartir apertura y réplica entre familias de una misma ola; nunca tratar outcomes del mismo instrumento como oportunidades independientes de observar R. Guardar cada `R_k`, y calcular directamente `d_k = R_k - p0` en cada réplica (p0 es el punto histórico fijo), más error puntual con signo, |d|, y fracción de réplicas con |d_k|≤0.02. Obtener IC95 percentil de los `d_k`; no reconstruir réplicas desde extremos de IC marginales. Si el diseño produce varianza cero por estratos de una UPM, reportarlo como limitación del IC y no afirmar calibración/cobertura.
3. Para IC95=[L,U] en proporción (equivale a pp tras multiplicar por 100), reglas cerradas: `COMPATIBLE-CON-TOLERANCIA` si **−0.02 ≤ L y U ≤ +0.02** (equivale a todo el IC dentro de [−2,+2] pp, límites incluidos); `DESVÍO-MATERIAL` si **U < −0.02 o L > +0.02** (estrictamente separado de la banda); `INDETERMINADO` en todo otro caso, incluidos intervalos anchos y los que sólo tocan la banda por un extremo. No se exige que el IC contenga cero: un IC estrecho [0.007,0.013] queda compatible. La regla clasifica un contraste local, no calibra un sistema.
4. Casos de comprobación (pp): [−5,+5]→INDETERMINADO; [+0.7,+1.3]→COMPATIBLE-CON-TOLERANCIA aunque no incluye 0; [+2.1,+3]→DESVÍO-MATERIAL; [−2,+2]→COMPATIBLE-CON-TOLERANCIA; [+2,+2.5] y [−2.5,−2]→INDETERMINADO; [+2.01,+2.5]→DESVÍO-MATERIAL. Con intervalo válido, ordenado y finito estas tres etiquetas son mutuamente excluyentes y exhaustivas.
5. Una sola comparación dentro de tolerancia permite decir únicamente **compatible con esta tolerancia local** para este estimando, piso y ola. No permite declarar `CALIBRADO`, calibración general, estabilidad entre olas ni cobertura nominal. Sin segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

CALC-ENCIG-0001 conserva IC95 [0.662900,0.684530], bootstrap de UPM dentro de estrato (2,000 réplicas); 8 estratos de UPM única, de modo que el IC es límite inferior de anchura verdadera. No se guardaron las réplicas; el IC marginal no da varianza del error contra el punto fijo. Hace falta vector futuro por réplica y n efectivo para IC de error/potencia.

La banda ±2 pp es una decisión práctica propuesta, no precisión acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector de diferencias por réplica, soporte efectivo y conteos de UPM/estratos; si faltan, el resultado queda `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Fecha y cuestionario oficial confirmados; misma definición de evento y servicio; instrumento mantiene identificación de estrato, UPM, FAC_TRA y tipo de evento. Apertura compartida con ENCIG-SOLICITUD-MORDIDA.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
