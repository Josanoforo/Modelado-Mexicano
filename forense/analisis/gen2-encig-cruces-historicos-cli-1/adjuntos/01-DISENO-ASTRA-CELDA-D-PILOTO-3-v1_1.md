# CELDA-D · Piloto 3 · Diseño independiente B (Astra)
**Estimando propuesto: proporción de trámites con el desenlace ENCIG del árbitro, entre trámites de su universo elegible, por sexo y edad de quien los realizó; no proporción de personas.**

Base declarada: brief v1.1, `8e455bd6`, 19/sep/2026 21:10 UTC. Diseño de dos páginas, sin ejecución, microdatos, cruces derivados ni consulta de diseños ajenos. Los ZIP de agosto no se usan para establecer el estado de septiembre. Los hechos siguientes se aceptan sellados del brief, no se verifican ni reestiman aquí.

## Página 1 · Decisión y estimadores

**1. Primero cobertura; después contraste.** Propongo emitir C2 en nube para los 22 pares reservados, donde existan marginales compatibles de idéntico desenlace, universo, ponderación y ola. Cada emisión queda `EMITIDA-SIN-EVALUAR`: disponible para escenarios exploratorios del motor, excluida de su estimación adoptada y de decisiones automáticas. Si el motor no distingue esos estados, entregar una tabla consultable hasta separar su consumo. Componer no consume reservas; tampoco identifica una distribución conjunta ni garantiza que sus celdas reproduzcan los marginales. No inventar pesos de celda para agregarlas. Incompatibilidades o probabilidades 0/1: `NO-EMITIBLE`, sin suavizado oportunista.

Esto produce más cobertura inmediata que otro concurso aislado. El piloto 3 sería su chequeo fuera de muestra, no permiso retroactivo para adoptar las 22 rejillas. C2 ya ganó en DIN y TRA: MAE 1.47 y 1.57 pp, ADR-538/542; C6/C7 empeoraron en TRA (2.85/2.66 pp). Es evidencia favorable localizada, no validación universal.

**2. Chequeo elegido: ENCIG 2025, sexo × edad.** Tercer dominio; unidad trámite, conservando dependencias entre trámites de una persona y el diseño muestral. Propuesta de categorías: hombre/mujer y 18–29/30–44/45–59/60+; no reasignar faltantes. Solo lanzar si esas bandas son componibles exactamente desde marginales sellados, con numeradores y denominadores compatibles, y desde ENCIG 2023. El desenlace y filtros serán literalmente los de ENCIG en `PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`; no se sustituye por otro resultado.

El brief no contiene esos marginales, sus categorías ni tamaños: **no afirmo soporte demostrado ni una especificación ejecutable terminada**. Antes del COMMIT-1, adjuntar únicamente sus identificadores y verificar compatibilidad; si falla, continuar la emisión y aplazar este piloto, sin buscar otro cruce favorable. Bandas amplias reducen fragmentación, pero no prueban soporte. Para masas marginales selladas q(a), q(b), el soporte conjunto está entre max(0,q(a)+q(b)−1) y min(q(a),q(b)); q(a)q(b) es solo planificación bajo independencia, nunca evidencia de n efectivo.

**3. Un retador, fijado sin 2025.** Sea L=logit y E=expit. Para celda ab:

- **C2:** E[L(p₂₅,a)+L(p₂₅,b)−L(p₂₅)].
- **S½:** E[L(p₂₅,a)+L(p₂₅,b)−L(p₂₅)+½δ₂₃,ab], con δ₂₃,ab=L(p₂₃,ab)−L(p₂₃,a)−L(p₂₃,b)+L(p₂₃).
- **C1:** p₂₃,ab, únicamente si el cruce histórico existe o se construye y sella antes de emitir; los pisos marginales #871/#874 no lo proporcionan.

δ es el residuo respecto de C2 en escala logit, no interacción causal. El factor ½ es una regularización convencional predeclarada, no óptima ni aprendida de los pilotos. Usa solo ENCIG 2023; no selecciona signos ni celdas significativas. Su construcción histórica pertenece a una ejecución posterior autorizada, no a este diseño. Sin comparabilidad o soporte histórico, no hay S½ ni concurso confirmatorio; queda factibilidad de C2.

<!-- SALTO DE PÁGINA -->

## Página 2 · Incertidumbre, fallo y alcance

**4. Incertidumbre y adjudicación.** Propagar conjuntamente marginales, cruce histórico y R mediante réplicas que respeten estratos, UPM, pesos y agrupación de trámites por persona; preservar la dependencia C2–R en 2025. Separar olas solo con independencia justificada. La incertidumbre histórica se multiplica por ½ en escala logit; esto no cubre por sí solo deriva temporal ni error estructural. Sin covarianzas/diseño recuperables, emitir puntos con incertidumbre incompleta y declarar `INDECIDIBLE`, no fabricar independencia.

Soporte propuesto, congelado: cada celda histórica y actual debe tener n efectivo de Kish ≥100 y al menos 20 personas distintas con evento y 20 sin evento; el IC respeta además el diseño, no solo Kish. Si alguna falla, no se eliminan celdas para mejorar el marcador: resultado global `INDECIDIBLE-POR-SOPORTE`, análisis parcial descriptivo. Estos umbrales son convenciones del diseño, no garantías de potencia.

Métrica primaria: MAE no ponderado sobre las ocho celdas fijas. Δⱼ=MAE(C2)−MAE(j), en pp. Superioridad: límite inferior del IC simultáneo 95% de Δⱼ >0.5 pp **y** límite superior simultáneo del empeoramiento absoluto en cada celda <2 pp. Control familiar sobre todas las comparaciones de superioridad y daño previstas (S½ y C1 si disponible), mediante réplicas conjuntas y Bonferroni. Todos los márgenes se fijan ahora. Si solo el punto cumple, propuesta con reserva, sin adjudicación. Si ambos vencen a C2 pero no se distinguen entre sí, superioridad sobre C2 demostrada, ganador único `INDECIDIBLE`. C1 ganador acreditaría persistencia, no éxito de transportar interacción.

**5. B-bis y precedencia.** Primero validez del cegamiento y soporte; después superioridad; después ausencia de mejora. R anticipado → factibilidad. Un ganador válido limita C2 como regla general solo en este desenlace, rejilla y ola. Si nadie vence y todos los límites superiores de Δ quedan ≤0.5 pp, C2 queda **corroborado de manera acotada frente a estos retadores**. Si los IC todavía admiten mejoras relevantes, es falsador débil/`INDECIDIBLE`, aunque sea la tercera vez sin ganador. Una interacción histórica casi nula vuelve S½ casi idéntico a C2: escasa capacidad de falsación, no prueba de ausencia de interacción actual. Un veto por daño impide adoptar al retador, pero no demuestra equivalencia. No extender una firma a reservas no evaluadas.

**6. Uso ciego del CALC.** Dentro de ENCIG, llamar a cada eje PERSISTE o CAMBIA solo si >50% de sus categorías comparables recibe esa etiqueta; lo restante es mixto/no resuelto. Hay mayoría de ejes seleccionados solo si ambos concuerdan. Con PERSISTE, conservar sexo × edad: C1 gana plausibilidad, no puntos ni adopción. Con CAMBIA, conservar también el cruce: C2 y S½ ganan plausibilidad relativa frente a C1 porque actualizan marginales, pero **S½ no gana ventaja sobre C2** por ese dato; estabilidad marginal no identifica estabilidad de δ. En resultados mixtos, mismas fórmulas y reglas. No ajustar ½, elegir celdas ni desplazar instrumento después del CALC. La propuesta funciona en ambos escenarios; brechas de ENCIG (dos años) y pandemia de ENIF impiden extrapolar el diagnóstico entre instrumentos.

**7. Ejecución posterior.** COMMIT-1: spec, categorías compatibles, incertidumbre y código congelados; acceso a ola reservada con guardia de una sola variable de agrupación. COMMIT-2: emisiones selladas, sin R. COMMIT-3: R y adjudicación por la vía de descegamiento preregistrada. Nada analítico en scratch. Sexo/edad son marcadores estructurales: reportar asociaciones y efectos, no psicología. Región y condición indígena quedan fuera del alcance. **Avance previsto:** cobertura explícitamente provisional y una decisión contrastable en un tercer dominio; ninguna medición se produjo en esta sesión.
