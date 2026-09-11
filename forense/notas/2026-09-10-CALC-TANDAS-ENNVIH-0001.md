# CALC-TANDAS-ENNVIH-0001 · medición y extracción

Fecha de ejecución: 10 de septiembre de 2026, CAJA/Ubuntu. Corrida:
`CALC-TANDAS-ENNVIH-0001`. Spec final `4f2203cf…`; `verify: REPRODUCE`,
`CONTEXTO=IDENTICO`. `tools/ya_medido.py R8.2` devolvió `NUNCA-MEDIDA` antes
de abrir el objeto.

## Resultado útil

El primer estimando identificado es la participación individual en al menos
una tanda durante los últimos 12 meses entre quienes respondieron el Libro
IIIB de la ENNViH (15 años o más), usando el factor puntual de ese libro y de
esa ola. No es una tasa de incumplimiento ni el efecto de conocer a la
organizadora.

| ola / campo | p ponderada | n / sí | masa ponderada | faltante `cr04` | respuesta válida sin factor puntual | IC |
|---|---:|---:|---:|---:|---:|---|
| ENNViH-1, 2002 (campo concluido en agosto) | 14.67% | 19,802 / 2,469 | 68,285,970 | 0 | 0 | no estimable sin UPM/estrato/réplicas |
| ENNViH-2, mediados de 2005–2006 | 8.58% | 18,973 / 1,335 | 68,777,734 | 150 | 1,484 | no estimable sin UPM/estrato/réplicas |
| ENNViH-3, mediados de 2009–2012 | 12.04% | 23,354 / 2,488 | 76,045,400 | 1,470 | 103 | no estimable sin UPM/estrato/réplicas |

Las tres preguntas tienen la misma ventana textual, pero no se vende una
tendencia: ENNViH es panel con desdoblamientos y seguimiento, los factores
puntuales representan poblaciones de cada ola y los largos periodos de campo
2005–06/2009–12 impiden asignar un único año a cada respuesta. `pid_link` y
los factores longitudinales no se usaron.

El control crudo contra los codebooks reproduce 2002 (`2,469/17,333`) y
2005–06 (`1,505/18,952`). En 2009–12 no reproduce por una observación:
microdato `2,496/20,961`, codebook `2,497/20,960`, con igual total `23,457`.
La corrida conserva el microdato y publica el desacuerdo.

### Cortes por edad

| ola | 15–29 | 30–49 | 50+ |
|---|---:|---:|---:|
| 2002 | 15.22% (`n=7,669`) | 18.85% (`n=7,336`) | 7.04% (`n=4,797`) |
| 2005–06 | 9.38% (`n=6,761`) | 11.00% (`n=6,878`) | 4.22% (`n=5,334`) |
| 2009–12 | 13.09% (`n=9,463`) | 15.56% (`n=7,678`) | 6.15% (`n=6,213`) |

Son descripciones, no contrastes causales ni comparaciones con incertidumbre
de diseño. Una edad falta en 2005–06 y cinco están fuera/faltantes en
2009–12; sólo salen de estos cortes.

### Montos y duración secundarios

| cantidad | media ponderada | mediana ponderada | n | unidad / reserva |
|---|---:|---:|---:|---|
| 2002, monto aportado | 2,463.68 | 1,000 | 2,437 | pesos nominales; no es cuota periódica |
| 2002, monto recibido | 2,369.27 | 1,000 | 2,310 | pesos nominales |
| 2002, monto por recibir | 1,773.32 | 0 | 2,066 | pesos nominales; separado de recibido |
| 2005–06, monto aportado | 2,215.90 | 1,000 | 1,329 | pesos nominales; no es cuota periódica |
| 2005–06, monto recibido | 2,749.91 | 1,000 | 1,309 | pesos nominales |
| 2005–06, monto por recibir | 1,560.65 | 0 | 1,274 | pesos nominales; separado de recibido |
| 2009–12, recibido o por recibir | 3,973.90 | 2,000 | 2,478 | pesos nominales; última tanda; 3 montos negativos excluidos |
| 2009–12, duración homologada | 115.89 | 91.3125 | 2,451 | días; 82 respuestas en días, 786 en semanas, 1,591 en meses |

La duración usa días×1, semanas×7 y meses×`365.25/12`. No convierte la
periodicidad de aportación. No se deflactan montos ni se comparan en términos
reales.

## Evidencia académica de grupos

Los números de página son del PDF; entre paréntesis se da la página impresa
cuando aparece.

| cantidad / mecanismo | valor o rango | población / periodo / denominador | fuente | uso permitido | uso no identificado |
|---|---|---|---|---|---|
| Razón principal de participar: ahorrar | 66% | participantes de DF, Guadalajara y Monterrey, encuesta 1996; denominador del subconjunto no publicado | Campos 1998, PDF p.12 (impresa 200), texto y gráfica 3 cuyo pie dice, contradictoriamente, nacional nov. 1997 | mecanismo/motivación cualitativa con porcentaje contextual | prevalencia nacional o parámetro puntual sin denominador |
| Dejó de participar porque “no le pagaban completo” | 10% | ex participantes de las tres ciudades, 1996; denominador no publicado | Campos 1998, PDF pp.13–14 (201–202); el pie de gráfica 4 dice nacional nov. 1997 | razón de salida / señal de riesgo | **no es tasa de incumplimiento**, fraude ni impago por turno |
| Participación alguna vez | 49% narrado frente a 41% en nota/tablas | tres ciudades, 1996; tablas: 295/715=41%; la narración no da denominador | Campos 1998, PDF pp.13, 16 y 23 (201, 204, 211) | rango/discrepancia explícita | calibración puntual; no resolver 49/41 por inferencia |
| Tamaño de grupo | 50% diez miembros; 20% once | participantes; texto atribuye tres ciudades 1996, pie de gráfica 5 dice nacional nov. 1997; denominador no publicado | Campos 1998, PDF pp.14–15 (202–203) | escenario de tamaño 10/11 | distribución nacional puntual |
| Duración/frecuencia y fondo | ~1/3: dos meses con pagos semanales; 40%: fondo 500–1,000 pesos de los noventa | texto atribuye tres ciudades 1996; pies de gráficas 6/7 dicen nacional nov. 1997; denominador no publicado | Campos 1998, PDF pp.17–18 (205–206) | escenarios históricos nominales | deflactación, cuota actual o calibración puntual |
| Filtro y sanción reputacional | conocimiento laboral/vecinal; admisión de cumplidos; exclusión y daño reputacional | descripción institucional, sin denominador | Campos 1998, PDF p.14 (202) | mecanismo compatible con R8.2 | magnitud del efecto causal o probabilidad condicional |
| Hogares con mención/caso de tanda | 52 casos | 116 hogares seleccionados intencionalmente, 21 localidades/13 estados, campo del estudio BANSEFI–PATMIR; conteos no excluyentes | BANSEFI–CIESAS–UIA 2006, PDF pp.8, 15–16 | cobertura cualitativa / localización de casos | prevalencia nacional ponderada |
| Tanda/mutualista de un caso | 22 personas, fondo 1,000 en 5 meses; o 37 números, 150 semanales, fondo 5,000 en 8 meses; comisión 10% | Diana, Mérida; un hogar/caso | BANSEFI–CIESAS–UIA 2006, PDF p.106 (impresa 105) | escenarios coherentes de grupo, monto, duración y organizadora | promedio poblacional o tasa de falla |
| Frecuencia/monto de un caso | 2–3 veces al año; 1,000–3,000; 10 abonos semanales | Ema y José, Tehuacán; un hogar/caso | BANSEFI–CIESAS–UIA 2006, PDF p.179 | rango de escenario cualitativo | frecuencia poblacional |
| Arquitectura y sanción | participantes se conocen; vigilancia/flexibilidad; perder abonos y participación futura | síntesis cualitativa del producto, sin denominador | BANSEFI–CIESAS–UIA 2006, PDF pp.212–213 | mecanismo y diseño de escenarios | tasa de impago o efecto causal |

## Destino para R8.2 y residual

Propuesta sin adopción: usar `p_participa_12m` por ola (8.58%–14.67%, no como
intervalo estadístico) como escenario mexicano de exposición/participación
potencial alrededor de `cooperacion.tanda.conoce_organizadora`. Campos y
BANSEFI sostienen cualitativamente el mecanismo de conocimiento previo,
recomendación y sanción futura. Ninguna fuente estima
`P(entra | conoce organizadora)` frente a `P(entra | no conoce)`, por lo que
R8.2 no recibe una nueva probabilidad ni cambia de fuerza sin firma de mesa.

El panel entrada/salida queda residual separado: aunque 2005/2009 traen
`pid_link` y existen ponderadores longitudinales, la base 2002 no porta esa
llave en `iiib_cr.dta` y esta entrega no homologó el crosswalk ni un universo
de attrition. Resolverlo exige una spec propia; no bloquea los tres puntos
puntuales.

Sigue abierto el faltante material: no se localizó un ledger mexicano abierto
de grupo, organizadora, turnos, cuotas y pagos. La vía comercial permanece
diferida por D18. Una encuesta individual no cierra ese faltante.

## Recibo de publicación posterior al publicador 09

Después de integrar `origin/main` con los PR #695–#703 ya fusionados, se
asentó el comprobante `VERIFY-ESTRUCTURADO` en
`forense/replay-evidencia.tsv` y se ejecutó una sola publicación explícita:
`python3 tools/corrida0.py registro --escribe --lote
CALC-TANDAS-ENNVIH-0001`. El lote añadió exactamente **1 corrida** y **39
resultados**, sin borrar ni modificar filas ajenas. La vista de usos quedó
byte-idéntica porque no existe consumidor firmado. Totales posteriores:
151 corridas, 3,374 resultados y 207 usos. La corrida publicada conserva
`REPRODUCE/IDENTICO` y cita la fuente estructurada de `ADR-468`; no adopta
R8.2 ni incrementa el contador GEN2.
