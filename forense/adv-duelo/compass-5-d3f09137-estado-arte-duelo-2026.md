# ADV-1 y ADV-2 — Demolición del diseño de duelo y rúbrica top-tier para un duelo pre-registrado LLM-vs-simulador arbitrado por microdato mexicano

> **Nota de procedencia (20/ago/2026 · `ACTO SELLA-ADV` T1):** deep research corrido fuera del proyecto (herramienta externa, no sigue la disciplina Bloque A/B/C del programa — mismo patrón que `compass-4`/`FP-61`), con dos entregables propios embebidos (`ADV-1` y `ADV-2`, ver cuerpo). Citado por CAREO (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §A) como insumo "deep search compass-5". Archivo de origen (fuera del repo, no se re-sube con ese nombre): `compass_artifact_wfd3f091379eb25e3ebf34dc2883351e73_text_markdown.md`. Renombrado al archivar siguiendo el patrón de `compass-1`…`compass-4` (`compass-N-<shortid>-<tema>-<año>.md`, shortid tomado de los 8 caracteres tras `wf`). sha256 del adjunto verificado contra el paquete de lanzamiento del 19/ago/2026: `10f4bcc2b374bf9dee9dd66675c8b4e0eeef24615f96a8fad4ce49433447cdb4`, coincidencia exacta. Archivado verbatim, sin edición de cuerpo; a partir de este commit es base de evidencia fechada del programa y no se retoca (doctrina `FP-57`/`ADR-114`).

---

## ENTREGABLE 1 — ADV-1: DEMOLICIÓN DEL DISEÑO

### TL;DR
- **El duelo, tal como está descrito, puede declarar un ganador falso por al menos tres vías ROMPE-DISEÑO simultáneas:** contaminación del corredor L (el LLM casi con seguridad vio en entrenamiento las mismas encuestas que sirven de árbitro), circularidad del corredor M (el motor se calibró con encuestas de la misma familia que R) y un marcador "≥X de N" sin poder estadístico, sin reglas de scoring propias y sin manejar la incertidumbre del propio árbitro.
- **Cada modo de fallo ya está documentado a nivel mundial** con casos reales que sirven de advertencia operativa: GSM1k/Scale AI (contaminación de benchmarks), *The Leaderboard Illusion* (gaming de leaderboards), Kapoor & Narayanan (leakage y crisis de reproducibilidad en ML aplicado), y el Fragile Families Challenge (techo de predictibilidad que aplana a todos los competidores).
- **El arreglo más barato no es abandonar ningún bando.** Es un duelo v2 con corte temporal post-entrenamiento, validación estrictamente fuera de muestra para M, scoring propio (Brier/log/WIS), un baseline obligatorio de tasa base/persistencia, y un tercer veredicto pre-declarado explícito: "ambos lejos de R".

### A. Tabla de hallazgos

| # | Superficie | Edge case (paso a paso, con caso real) | Severidad | Arreglo | Costo |
|---|---|---|---|---|---|
| 1 | **Contaminación del corredor L** | El set v1 incluye una celda sobre, p. ej., prevalencia de victimización por hogar. El LLM la responde con altísima precisión porque las tablas de la ENVIPE 2021-2024 estaban en su corpus. L "gana" a M pero no modeló: recitó. **Caso real:** Zhang et al. (Scale AI, *A Careful Examination of LLM Performance on Grade School Arithmetic*, arXiv:2405.00332, 2024) construyeron GSM1k —1,205 problemas nuevos emparejados en dificultad a GSM8k— y observaron caídas de exactitud de hasta 13%, con varias familias (Phi, Mistral) mostrando sobreajuste sistemático; hallaron una relación positiva (Spearman r²=0.32) entre la probabilidad de que un modelo genere un ejemplo de GSM8k y su brecha de desempeño GSM8k→GSM1k: evidencia directa de memorización parcial. | **ROMPE-DISEÑO** | Evaluar L solo sobre datos posteriores al corte de entrenamiento del modelo (olas retenidas no publicadas al congelar), más perturbaciones/contrafactuales que la memoria no responde. | 2-3 sesiones + alinear con calendario de publicación de INEGI |
| 2 | **Circularidad del corredor M** | El motor se parametrizó con la ENIGH; la celda-árbitro también viene de la ENIGH de la misma ola. M coincide con R no porque el mecanismo sea correcto, sino porque el parámetro fue ajustado dentro de muestra. **Caso real:** Kapoor & Narayanan (*Leakage and the Reproducibility Crisis in ML-based Science*, Patterns 4(9):100804, 2023; arXiv:2207.07048) hallaron leakage en 17 campos afectando 294 papers en la versión Patterns (329 en el preprint arXiv 2022); en su reanálisis de predicción de guerra civil, corregidos los errores, los modelos ML complejos no superan sustantivamente a la regresión logística de décadas atrás. | **ROMPE-DISEÑO** | Declarar por celda la clase de procedencia (medido nacional / parcial / asignado) y excluir del marcador las celdas donde el parámetro de M provino de la misma ola/encuesta que R (validación fuera de muestra estricta). | 1-2 sesiones (el etiquetado de procedencia ya existe) |
| 3 | **No-independencia L↔R de segundo orden** | El corpus del lado L fue escrito leyendo la literatura que resume a R (los mismos reportes de INEGI). Ninguna pregunta discrimina modelado de repetición de literatura secundaria. | DEBILITA | Incluir solo "momentos" cuyo desenlace real NO esté en literatura de divulgación (microdato crudo, cruces no tabulados, olas nuevas). | 2 sesiones de curaduría |
| 4 | **"Distancia a R" ignora la incertidumbre del árbitro** | R = 22.4% con CV alto. L dice 21%, M dice 24%; el diseño declara ganador a L, pero ambos están dentro del IC de R: el resultado es ruido. INEGI publica EE, CV y DEFF y semaforiza la precisión por umbrales de CV (acuerdo CAC-007/01/2018). | **ROMPE-DISEÑO** | Reglas de scoring propias (Brier/log binarios; CRPS/WIS continuos); reportar calibración; NO puntuar celdas donde el CV de R supere el umbral INEGI o donde ambos caigan en el IC de R (declarar "empate por imprecisión del árbitro"). | 2-3 sesiones |
| 5 | **El dueño del motor elige el set** | El dueño de M elige preferentemente celdas donde el motor calibró bien; además las preguntas de tasa base trivial inflan el empate gratis. **Caso real:** Singh et al. (*The Leaderboard Illusion*, arXiv:2504.20879; NeurIPS 2025 Datasets & Benchmarks), sobre ~2M batallas de 243 modelos de 42 proveedores (ene 2024–abr 2025), identificaron 27 variantes privadas probadas por un proveedor (Meta, previo a Llama-4) antes de publicar la mejor; elegir el mejor de N submissions infla el rating sistemáticamente. | **ROMPE-DISEÑO** | Preselección ciega del set por un tercero, estratificación por dificultad/dominio pre-declarada, exclusión de celdas de tasa base trivial. | 2 sesiones + un revisor externo |
| 6 | **"≥X de N" sin poder ni corrección múltiple** | Con N=10-15, un corredor gana 8-de-12 por azar con probabilidad no despreciable. **Caso real:** Schoenegger et al. (*Wisdom of the silicon crowd*, Science Advances 10(45), 2024) reportaron que un ensemble de 12 LLMs era estadísticamente indistinguible de 925 pronosticadores humanos, pero solo sobre 31 preguntas binarias en un torneo de 3 meses: poder limitado. | **ROMPE-DISEÑO** | N fijado por cálculo de poder; prueba binomial/de signos con magnitud (no solo conteo); corrección por comparaciones múltiples; TOST para empates. | 1 sesión de cálculo + N mayor (costo real de datos) |
| 7 | **Mismo equipo escribe L y M** | Aunque el commit de L sea previo, el redactor conoce el motor y (consciente o no) escribe L para perder o ganar. | DEBILITA | Generar L con un modelo distinto en sesión sin contexto del motor, con prompt de L pre-registrado y firmado; idealmente un tercero corre L. | 1-2 sesiones |
| 8 | **Varianza del LLM** | Misma pregunta, dos corridas, dos respuestas; se reporta la que gana. Bisbee et al. (2024) documentaron inestabilidad temporal de silicon samples (abril vs julio 2023). | DEBILITA | Fijar versión, fecha y temperatura del modelo; usar self-consistency (mediana de k corridas) o un ensemble congelado, todo pre-declarado. | 1 sesión |
| 9 | **Goodhart en la regla semanal** | "Una celda o una fila cada semana" presiona a producir celdas basura o fáciles para cumplir. | DEBILITA | Cada celda debe pasar un checklist de admisibilidad (procedencia, CV del árbitro, no-trivialidad) antes de contar; permitir explícitamente "nada esta semana y se dice". | 0.5 sesión |
| 10 | **Los 7 umbrales del GO son de proceso** | Umbrales verificados "por comando" (¿corre el script? ¿existe el commit?) son gamificables construyendo la celda para pasarlos. | DEBILITA | ≥3 de los 7 deben ser umbrales de resultado: (a) calibración dentro de banda, (b) diferencia L-M vs R que supere el IC del árbitro, (c) fracción de celdas no-triviales. | 1 sesión |
| 11 | **Consecuencias pre-declaradas incompletas** | Si L gana se concluye "el motor no sirve"; pero "M > L" no prueba "M es bueno" — ambos pueden estar lejos de R. Falta el tercer resultado. **Caso real:** en el Fragile Families Challenge (Salganik et al., PNAS 117(15):8398-8403, 2020), 160 equipos con un dataset rico (4,242 familias) y ML optimizado "the best predictions were not very accurate and were only slightly better than those from a simple benchmark model" (el mejor R² en holdout ≈0.2 para material hardship y GPA, cercano a 0 en los otros cuatro outcomes): el techo de predictibilidad era bajo para todos. | **ROMPE-DISEÑO (lógico)** | Pre-declarar tres desenlaces: (i) L más cerca, (ii) M más cerca, (iii) ambos fuera del IC de R (fenómeno poco predecible con estas herramientas); y separar "M>L" de "M alcanza utilidad absoluta vs baseline". | 0.5 sesión |
| 12 | **Re-validación bajo demanda deja errores fuera para siempre** | Un error del corpus que el duelo nunca toca queda sin corregir indefinidamente. | DEBILITA | Barrido mínimo complementario: muestreo aleatorio de un % pequeño del corpus viejo por trimestre para auditoría, independiente del duelo, sin re-auditar todo. | 1 sesión/trimestre |

### B. El diseño reconstruido (duelo v2 — solo arreglos ROMPE-DISEÑO)

1. **Corte temporal (anti-contaminación).** L solo se evalúa en celdas cuyo árbitro proviene de olas/microdato publicados DESPUÉS del corte de entrenamiento del modelo fijado. Versión, fecha y temperatura del LLM congeladas y firmadas antes de abrir datos.
2. **Fuera de muestra para M.** Se excluyen del marcador las celdas donde el parámetro de M provino de la misma encuesta/ola que R; cada celda lleva su clase de procedencia visible.
3. **Scoring propio + incertidumbre del árbitro.** Brier/log (binarios), CRPS/WIS (continuos); se reporta calibración además de exactitud; se declara "empate por imprecisión" cuando ambos corredores caen dentro del IC de R o el CV de R excede el umbral INEGI.
4. **Selección ciega y estratificada.** Un tercero selecciona el set, estratificado por dificultad/dominio, sin celdas de tasa base trivial.
5. **Poder y equivalencia.** N fijado por cálculo de poder; prueba de signos con magnitud + corrección por comparaciones múltiples; TOST para empates.
6. **Baseline obligatorio.** Además de L y M, un corredor B = predicción de tasa base / persistencia. Ni L ni M "ganan" en sentido fuerte si no superan a B (vara mínima al estilo COVID-19 Forecast Hub).
7. **Tres consecuencias pre-declaradas**, incluida "ambos lejos de R".

*Resistir la tentación de la perfección: cada elemento añadido paga su costo porque cierra una vía de ganador falso. Todo lo demás (comparaciones múltiples finas, cegado total, ODD completo) es DEBILITA y puede posponerse.*

### C. Qué cambiaría mi veredicto (condiciones bajo las que mis objeciones caen)

1. Si L se corre exclusivamente sobre microdato genuinamente post-corte y no publicado, la objeción de contaminación (#1, #3) cae.
2. Si M se evalúa solo fuera de muestra (parámetros de una fuente, árbitro de otra), la circularidad (#2) cae.
3. Si el N crece hasta tener poder declarado y se usa scoring propio + baseline, el "≥X de N" (#4, #6, #11) deja de ser gamificable.
4. Si un tercero ciego selecciona el set y corre L, el sesgo de selección y del redactor (#5, #7) cae.
5. Si se pre-declara el tercer desenlace y el baseline, la inferencia falaz "M>L ⇒ M bueno" (#11) deja de ser posible.

---

## ENTREGABLE 2 — ADV-2: ESTADO DEL ARTE Y RÚBRICA TOP-TIER

### TL;DR
- **El mejor trabajo existente convergió en una rúbrica clara:** control de contaminación del corte de entrenamiento, baselines obligatorios, reglas de scoring estrictamente propias, calibración, poder estadístico, cegado, techo de predictibilidad declarado, y manejo explícito de la incertidumbre del árbitro.
- **El diseño descrito CUMPLE en disciplina de pre-registro y procedencia de parámetros**, es PARCIAL en manejo de incertidumbre, cegado y validación fuera de muestra, y FALTA en scoring propio, baselines, poder estadístico, calibración y control de contaminación.
- **La síntesis no-purista:** tomar *scoring rules + baselines + ensembles* del forecasting; *validación por patrones + procedencia de parámetros + validación fuera de muestra* del ABM; *control de contaminación + fijación de versión + self-consistency* del LLM-eval.

### A. Rúbrica top-tier (14 criterios, con fuente)

1. **Control de contaminación del corte de entrenamiento** — Zhang et al./Scale AI, GSM1k (arXiv:2405.00332, 2024); Kapoor & Narayanan, Patterns 2023.
2. **Baseline obligatorio como vara** — COVID-19 Forecast Hub / FluSight (CDC): el COVIDhub-baseline es un modelo de persistencia de referencia y el ensemble la vara de desempeño (Cramer et al. 2022; Bracher et al. 2021).
3. **Reglas de scoring estrictamente propias** — Brier (1950); log score; CRPS/Weighted Interval Score (Bracher et al., *Evaluating epidemic forecasts in an interval format*, PLOS Comp Biol 2021); fundamento en Gneiting & Raftery (2007).
4. **Calibración además de exactitud** — M5 uncertainty competition (Makridakis et al. 2022); triptych MCB-DSC (arXiv:2301.10803).
5. **Poder estadístico y N defendible** — crítica a Schoenegger et al. (31 preguntas, Science Advances 2024); Lu (2025, arXiv:2507.04562): a 50% de ruido en 50 preguntas el pronosticador ruidoso gana ~24% de las veces.
6. **Corrección por comparaciones múltiples** — estándar de reproducibilidad; garden of forking paths (Gelman & Loken 2014).
7. **Prueba de equivalencia (TOST) para empates** — Lakens, Scheel & Isager, *Equivalence Testing for Psychological Research: A Tutorial*, AMPPS 2018; Schuirmann (1987).
8. **Cegado / independencia de corredores** — Singh et al., *The Leaderboard Illusion* (NeurIPS 2025); Recht et al. (2019) y Roelofs et al. (2019) sobre adaptive overfitting y reuso de holdout.
9. **Consecuencias y análisis pre-registrados** — registered reports (Chambers et al.; Nosek & Lakens 2014); OSF prereg; pre-registro en modelado predictivo (Hofman et al.).
10. **Manejo de la incertidumbre del árbitro** — INEGI publica EE/CV/DEFF y semaforiza por umbrales de CV (acuerdo CAC-007/01/2018).
11. **Validación estrictamente fuera de muestra del simulador** — Fagiolo, Moneta & Windrum, *A Critical Guide to Empirical Validation of ABMs in Economics* (Computational Economics 2007); indirect calibration; macro-validación EUROMOD contra estadística administrativa.
12. **Documentación estandarizada del modelo** — protocolo ODD (Grimm et al., JASSS 2020) + pattern-oriented modeling (Grimm et al. 2005); TRACE (Grimm et al. 2014).
13. **Techo de predictibilidad declarado** — Fragile Families Challenge (Salganik et al., PNAS 2020).
14. **Ensemble como referencia fuerte** — Schoenegger et al. (2024) "wisdom of the silicon crowd"; ensemble del COVID-19 Forecast Hub consistentemente superior a modelos individuales.

### B. Calificación del diseño descrito contra la rúbrica

| # | Criterio | Veredicto | Práctica top-tier que lo resolvería |
|---|---|---|---|
| 1 | Contaminación | **FALTA** | Enfoque GSM1k: árbitros post-corte / olas retenidas |
| 2 | Baseline obligatorio | **FALTA** | COVIDhub-baseline de persistencia + tasa base |
| 3 | Scoring propio | **FALTA** | Brier/log/WIS en vez de "distancia a R" cruda |
| 4 | Calibración | **FALTA** | Triptych / MCB-DSC; RF por cuantil (M5) |
| 5 | Poder estadístico | **FALTA** | Cálculo de poder pre-registrado; N mayor |
| 6 | Comparaciones múltiples | **FALTA** | Corrección estándar (Holm/BH) |
| 7 | TOST para empates | **PARCIAL** | "Empates definidos" → TOST formal (Lakens 2018) |
| 8 | Cegado | **PARCIAL** | Commit previo de L, pero mismo equipo → L por modelo/tercero distinto |
| 9 | Consecuencias pre-declaradas | **PARCIAL** | Existen, pero falta el tercer desenlace → formato registered report |
| 10 | Incertidumbre del árbitro | **PARCIAL** | Se declaran escalas/universos, no el CV de R → semaforización INEGI |
| 11 | Validación fuera de muestra | **PARCIAL** | Hay clase de procedencia, pero no excluye in-sample del marcador → marco Fagiolo-Moneta-Windrum |
| 12 | Documentación ODD | **PARCIAL** | Reglas SI-ENTONCES con nivel de evidencia; falta ODD formal + TRACE |
| 13 | Techo de predictibilidad | **CUMPLE (parcial)** | La "pregunta esencial" reconoce límites; reforzar citando Fragile Families |
| 14 | Ensemble | **FALTA** | Self-consistency / ensemble congelado de L |

**Lectura del tablero:** el diseño es fuerte precisamente donde la mayoría de los benchmarks fallan —disciplina de pre-registro, dos commits, procedencia declarada, contadores públicos— pero débil donde el forecasting y la epidemiología ya resolvieron el problema hace años: scoring propio, baselines y manejo de incertidumbre. Es un diseño de *proceso* excelente colgado de una *métrica* frágil.

### C. La síntesis no-purista (1 página)

**Del mundo del forecasting**, el diseño debe tomar: (i) reglas de scoring estrictamente propias —Brier/log para binarios, CRPS/WIS para continuos— que penalizan la sobreconfianza y permiten comparar corredores en la escala de R; (ii) un **baseline obligatorio** (persistencia o tasa base) como vara mínima que ambos corredores deben superar antes de que "ganar el uno al otro" signifique algo —la lección central del COVID-19 Forecast Hub, donde incluso pronósticos que superaban al baseline eran poco confiables en fases de cambio rápido—; y (iii) el **ensemble** como referencia fuerte, dado que la evidencia (Schoenegger 2024; hubs de la CDC) muestra que el ensemble supera consistentemente a los modelos individuales.

**Del mundo del ABM/microsimulación**, debe tomar: (i) **validación por patrones** (pattern-oriented modeling de Grimm) —exigir que M reproduzca múltiples patrones a distintas escalas, no una sola celda—; (ii) **procedencia explícita de parámetros** y **validación estrictamente fuera de muestra** (Fagiolo-Moneta-Windrum: separar ajuste dentro-de-muestra de capacidad fuera-de-muestra); (iii) **macro-validación** contra estadística externa al estilo EUROMOD (comparar agregados simulados con cifras administrativas independientes, con "health warnings" documentados); y (iv) **documentación ODD** para que la especificación congelada sea auditable por terceros.

**Del mundo del LLM-eval**, debe tomar: (i) **control de contaminación por corte de entrenamiento** (GSM1k: usar solo árbitros post-corte); (ii) **fijación de versión, fecha y temperatura** del modelo; y (iii) **self-consistency** (mediana de k corridas) para domar la varianza intrínseca del LLM, dado que la inestabilidad temporal y de corrida está documentada (Bisbee et al. 2024).

**Las 3 incorporaciones de mayor rendimiento-por-costo para un equipo chico:**
1. **Baseline de tasa base/persistencia + regla de scoring propia (Brier/WIS).** Barato (≈1-2 sesiones) y transforma el marcador de gamificable a defendible: es el cambio que más "ganadores falsos" elimina por peso.
2. **Corte temporal de contaminación.** Casi gratis si se alinea con el calendario de publicación de INEGI; neutraliza la objeción #1, la más letal para el corredor L.
3. **Manejo de la incertidumbre del árbitro usando el CV que INEGI ya publica.** No puntuar celdas donde R es impreciso; usa metadata existente y evita declarar ganadores dentro del ruido muestral.

### D. Anexo de fuentes y contexto de las encuestas mexicanas (árbitro)

**Casos y literatura (referencia por afirmación):**
- Contaminación de benchmarks: Zhang et al. (Scale AI), *A Careful Examination of LLM Performance on Grade School Arithmetic*, arXiv:2405.00332 (2024) — GSM1k, 1,205 ítems, caídas de hasta 13%, Spearman r²=0.32.
- Leakage / reproducibilidad: Kapoor & Narayanan, *Leakage and the Reproducibility Crisis in ML-based Science*, Patterns 4(9):100804 (2023); arXiv:2207.07048 (2022) — 17 campos, 294/329 papers; ML complejo ≈ regresión logística tras corregir.
- Gaming de leaderboards: Singh et al., *The Leaderboard Illusion*, arXiv:2504.20879; NeurIPS 2025 D&B — 27 variantes privadas; ~2M batallas, 243 modelos, 42 proveedores.
- Adaptive overfitting / reuso de holdout: Recht et al. (2019) e ImageNet/CIFAR-10; Roelofs et al. (2019) sobre 100+ competencias Kaggle; Dwork et al. sobre reuso de holdout.
- Techo de predictibilidad: Salganik et al., PNAS 117(15):8398-8403 (2020) — 160 equipos, 6 outcomes, mejor R² holdout ≈0.2.
- LLMs como pronosticadores: Halawi et al. (NeurIPS 2024, arXiv:2402.18563); Schoenegger et al., *Wisdom of the silicon crowd*, Science Advances 10(45) (2024) — 12 LLMs vs 925 humanos en 31 preguntas; Metaculus AI Benchmarking (Q3 2024–Q2 2025): los Pro Forecasters superaron a los mejores bots con significancia estadística (p=0.036 en Q3 2024; p≈0.00001 en Q2 2025).
- Silicon sampling / simuladores de opinión: Argyle et al. (2023, "algorithmic fidelity"); Santurkar et al. (2023, OpinionQA — divergencia respecto de la población general de EE. UU.); Bisbee et al. (2024 — 48% de coeficientes difieren significativamente de ANES; inestabilidad temporal); homogeneización ("Das Man"). Park et al., *Generative Agent Simulations of 1,000 People* (arXiv:2411.10109, 2024): agentes basados en entrevistas a 1,052 personas replican respuestas de la GSS con exactitud normalizada de **0.83** (raw 65.67% ÷ auto-consistencia test-retest a dos semanas 79.53%), redondeado a **85%** en el abstract; el enfoque reduce sesgos de exactitud entre grupos raciales e ideológicos frente a agentes basados solo en descripciones demográficas — precedente clave para fijar el techo de expectativas del corredor L en México.
- Validación ABM: Fagiolo, Moneta & Windrum (Computational Economics 30(3):195-226, 2007; JASSS 10(2):8, 2007); Grimm et al. (ODD, JASSS 2020; POM 2005). Microsimulación: EUROMOD macro-validación contra estadística administrativa (IJM).
- Equivalencia y pre-registro: Lakens, Scheel & Isager (AMPPS 2018, TOST); registered reports (Center for Open Science; Wikipedia/Chambers).
- Scoring epidemiológico: Bracher et al. (PLOS Comp Biol 2021, WIS); Cramer et al. (2022, COVIDhub-baseline y ensemble).

**Encuestas mexicanas como árbitro (periodicidad, diseño, representatividad, advertencias):**
- **ENIGH** (Ingresos y Gastos de los Hogares): bienal; diseño probabilístico, estratificado, por conglomerados y multietápico; representativa nacional con corte urbano/rural. INEGI publica EE, CV y DEFF y semaforiza por umbrales de CV (acuerdo CAC-007/01/2018). **Advertencia de comparabilidad:** cambios en el umbral urbano/rural (definido en 2,500 hab. desde 1992; antes 15,000) y en los marcos muestrales dificultan comparar olas (Teruel et al., *Los problemas de comparabilidad de las ENIGH*, Scielo). "Nueva serie" 2024 publicada.
- **ENVIPE** (Victimización y Percepción sobre Seguridad Pública): anual desde 2011 (la edición 2025 es el 15º ejercicio ininterrumpido); diseño probabilístico, trietápico, estratificado y por conglomerados; unidad última = persona de 18+; representativa nacional y por entidad federativa; declarada Información de Interés Nacional; usa la Muestra Maestra.
- **ENBIARE** (Bienestar Autorreportado): edición 2021; muestra representativa de población adulta (cierre con 36,978 viviendas); **limitación conocida:** el diseño puede implicar limitaciones para la representación de minorías, y la entrevista directa requiere lecto-escritura en español; encuesta de percepción/bienestar subjetivo.
- **ENASIC** (Encuesta Nacional para el Sistema de Cuidados): edición 2022, **primera de su tipo** (no periodicidad establecida); mide demanda y oferta de cuidados en los hogares y repercusiones en personas cuidadoras (en especial mujeres); representativa nacional a nivel hogar; complementa la ENUT. *[El acrónimo NO corresponde a educación ni salud: es "Sistema de Cuidados".]* Diseño muestral detallado (trietápico/estratificado): NO ENCONTRADO en la página de programa ni en la Nota Técnica consultadas; requeriría el documento de diseño muestral de ENASIC 2022.
- **ENFIH** (Encuesta Nacional sobre las Finanzas de los Hogares): edición 2019, **primera y única a la fecha** (proyecto conjunto Banxico–INEGI); mide la hoja de balance de los hogares (activos y pasivos, financieros y no financieros, flujos y acervos); diseño probabilístico, trietápico, estratificado y por conglomerados; muestra de 17,386 viviendas (40,940 personas de 18+), que representan 35.7 millones de viviendas y 86.4 millones de personas 18+; cobertura nacional y por localidad (NO estatal).
- **ENSAFI** (Encuesta Nacional sobre Salud Financiera): edición 2023, **primera de su tipo** (INEGI + CONDUSEF); mide la salud financiera de la población de 18+ (seguridad, resiliencia, control, libertad) y el estrés financiero; diseño probabilístico, en varias etapas, estratificado y por conglomerados, unidad última = persona; muestra ajustada a ~22,982 viviendas (20,189 entrevistas completas; 87.85% de respuesta; confianza 90%, DEFF 1.77, error relativo máx. 15%); representativa nacional y por entidad federativa.

**Nota transversal crítica para el árbitro:** como todas estas encuestas se seleccionan a partir de la Muestra Maestra del INEGI, comparten estructura de conglomerados, y el DEFF típico (>1; p. ej. 1.77 en ENSAFI) implica que los errores estándar reales son mayores que bajo muestreo aleatorio simple. Ignorar el DEFF al fijar el IC del árbitro subestimaría su incertidumbre y produciría "ganadores falsos" dentro del ruido muestral — exactamente el fallo #4 de ADV-1.

### Caveats
- Mi presupuesto de búsqueda web se agotó antes de confirmar por fuente primaria dos puntos menores: el diseño muestral exacto (etapas) de **ENASIC 2022** (NO ENCONTRADO en la página de programa y la Nota Técnica; el subagente lo verificó para ENFIH y ENSAFI pero no para ENASIC) y las cifras de las ediciones más recientes de ENIGH 2024 más allá de su publicación. Repórtense como pendientes de verificación en el documento de diseño muestral respectivo de INEGI.
- Varias fuentes secundarias de alta circulación (Medium, Substack, LessWrong) se usaron solo para contexto o crítica; toda afirmación cuantitativa está anclada en la fuente primaria (arXiv, PNAS, Science Advances, PLOS, journals INEGI/Banxico).
- La cifra de Park et al. tiene un matiz declarado: el abstract redondea a 85% (0.85) mientras el cuerpo reporta 0.83 para agentes basados en entrevistas, 0.82 solo-encuesta y 0.86 encuesta+entrevista. Úsese 0.83 como valor preciso del agente comparable a L.
- Las cifras de Metaculus (p-values pro-vs-bot) provienen de reportes del propio Metaculus/LessWrong, no de un paper revisado por pares; trátense como evidencia de plataforma, robusta pero no arbitrada.
