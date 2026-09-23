# FAMILIA-2027-ENCIG-SOLICITUD-MORDIDA · spec humana condicional v1.2

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENCIG 2027; referencia: 2025; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **persona adulta de universo A ENCIG MOR (FAC_P18)**, escala: proporción [0,1]. Estimando único: proporción ponderada con solicitud directa de beneficio, P8_3_1=1, universo A y FAC_P18; RESULT-ENCIG-MOR-A-P-SOL1.
- Piso inmutable: `RESULT-ENCIG-MOR-A-P-SOL1` de `CALC-ENCIG-0001`, cuyo `sello.json` tiene SHA-256 `9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.
- **Numerador y denominador:** Numerador = suma(FAC_P18) de personas del universo A con P8_3_1=1. Denominador primario = suma(FAC_P18) de personas del universo A con P8_3_1∈{1,2}; no es sólo el subconjunto afirmativo y no incluye P8_3_1=9/blanco/no numérico. Reportar esas no respuestas aparte en conteo y peso, y además la cobertura del universo A. Éste es el universo del estimador histórico CALC-ENCIG-0001.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo: dos unidades por cada cien en la escala del estimando. Se elige como margen absoluto pequeño, redondo, común y fácil de interpretar entre tasas base muy distintas; usar un margen relativo haría variar el error tolerado entre familias. Es una decisión práctica, no una conclusión empírica, ni precisión/potencia acreditada, equivalencia psicológica o la tolerancia numérica del CALC. Reportar siempre error absoluto y signo.
- **Soporte mínimo propuesto:** n elegible ≥10,000 personas, ≥100 estratos y ≥1,000 UPM; NS/NR+blanco ≤2% del peso de A; cero unidades sin FAC_P18. ENCIG 2025: A n=40,042, 442 estratos y 9,172 UPM; 94 NS/NR en P8_3_1, cero blancos y cero sin diseño/ponderador. Justificación operativa: n=10,000 es 25% del n histórico 40,042; ≥100/442 estratos y ≥1,000/9,172 UPM son pisos operativos, no garantía inferencial. El tope 2% limita cuánto puede diferir el universo de respuesta válida del universo A; el CALC histórico no conserva la masa faltante para certificarlo. Los conteos/estratos/UPM mínimos filtran soporte muy ralo y permiten exigir presencia suficiente de diseño; no certifican precisión, potencia, cobertura nominal ni suficiencia para detectar 2 pp. Además, el IC futuro requiere ≥1,000 réplicas válidas de 2,000 y denominador válido en ≥95% de réplicas. Incumplimiento: `NO-ESTIMABLE`; no relajar tras R.
- **Faltantes:** El contrato histórico define U_A con P8_3_1∈{1,2} y FAC_P18 positivo; códigos 9/NS/NR, blanco/no numérico se excluyen del punto, se cuentan aparte y no se imputan como 'no'. Por ello el estimando es entre respuesta válida (denominador U_A válido), no sobre toda A. Informar pérdida de cobertura contra A; si el peso excluido supera 2% del peso potencial A, NO-ESTIMABLE. Si futuro cambia el tratamiento de estos casos o el denominador, NO-COMPARABLE con el piso sellado.
- **Comparabilidad:** Mismo evento solicitud directa, pregunta P8_3_1 o equivalencia textual documentada, categorías sí/no, universo A, FAC_P18 y diseño EST_DIS/UPM_DIS. No mezclar los otros incisos de SOLANY con SOL1. Cambio de evento, informante o recorte del universo: NO-COMPARABLE. El CALC histórico registra 94 NS/NR pero no el peso expandido faltante; el umbral de 2% debe comprobarse en el vector/payload futuro y no se afirma aquí que se cumpla en 2025.

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Primero resuelve la compuerta: si el estimando/universo/unidad/códigos/pesos no son equivalentes, `NO-COMPARABLE`; si falta soporte, dato para el contraste o un IC válido conforme al diseño, `NO-ESTIMABLE`. Un estrato de una UPM que aporte varianza cero deja el IC como límite inferior de anchura; salvo que antes de abrir se haya fijado un método de varianza válido para ese caso, no sirve para dictaminar y queda `NO-ESTIMABLE`. Sólo con ambas compuertas superadas y un intervalo finito ordenado se asigna exactamente una etiqueta estadística.
2. Ejecutar bootstrap de UPM dentro de estrato con el diseño oficial. Compartir apertura y réplica entre familias de una misma ola; nunca tratar outcomes del mismo instrumento como oportunidades independientes de observar R. Guardar cada `R_k`, y calcular directamente `d_k = R_k - p0` en cada réplica (p0 es el punto histórico fijo), más error puntual con signo, |d|, y fracción de réplicas con |d_k|≤0.02. Obtener IC95 percentil de los `d_k`; no reconstruir réplicas desde extremos de IC marginales. Si el diseño produce varianza cero por estratos de una UPM, reportarlo como limitación del IC y no afirmar calibración/cobertura.
3. Para IC95=[L,U] en proporción (equivale a pp tras multiplicar por 100), reglas cerradas: `COMPATIBLE-CON-TOLERANCIA` si **−0.02 ≤ L y U ≤ +0.02** (equivale a todo el IC dentro de [−2,+2] pp, límites incluidos); `DESVÍO-MATERIAL` si **U < −0.02 o L > +0.02** (estrictamente separado de la banda); `INDETERMINADO` en todo otro caso, incluidos intervalos anchos y los que sólo tocan la banda por un extremo. No se exige que el IC contenga cero: un IC estrecho [0.007,0.013] queda compatible. La regla clasifica un contraste local, no calibra un sistema.
4. Casos de comprobación (pp): [−5,+5]→INDETERMINADO; [+0.7,+1.3]→COMPATIBLE-CON-TOLERANCIA aunque no incluye 0; [+2.1,+3]→DESVÍO-MATERIAL; [−2,+2]→COMPATIBLE-CON-TOLERANCIA; [+2,+2.5] y [−2.5,−2]→INDETERMINADO; [+2.01,+2.5]→DESVÍO-MATERIAL. Con intervalo válido, ordenado y finito estas tres etiquetas son mutuamente excluyentes y exhaustivas.
5. Una sola comparación dentro de tolerancia permite decir únicamente **compatible con esta tolerancia local** para este estimando, piso y ola. No permite declarar `CALIBRADO`, calibración general, estabilidad entre olas ni cobertura nominal. Sin segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

CALC-ENCIG-0001 guarda IC95 [0.080867,0.089021], bootstrap UPM dentro de estrato, 2,000 réplicas, seed 20260909/PCG64; ningún estrato de UPM única. No guarda vector de réplicas: no derivar de ahí EE exacta, IC del error o potencia. Requiere vector futuro del contraste emparejado piso−R y n efectivo.

La banda ±2 pp es una decisión práctica propuesta, no precisión acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector de diferencias por réplica, soporte efectivo y conteos de UPM/estratos; si faltan, el resultado queda `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

Condiciones comunes ENCIG, con texto/saltos equivalentes de P8_3_1 y acceso a FAC_P18/diseño. Misma apertura ENCIG que pago digital; dos outcomes en protocolo sellado previo, sin dos accesos ni selección posterior.

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
