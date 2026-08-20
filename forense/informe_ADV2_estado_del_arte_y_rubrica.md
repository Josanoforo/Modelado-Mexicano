# ADV-2 · Estado del arte, rúbrica top-tier y calificación del duelo LLM vs motor

> **Nota de procedencia (20/ago/2026 · `ACTO SELLA-ADV` T1):** informe adversarial para dirección, sesión limpia con búsqueda web, autodeclarado en su propio cuerpo: "sesión limpia con búsqueda web · 19/ago/2026 · insumo para el CAREO previo a sellar APERTURA v1.2". Insumo `ADV-2` del careo adjudicado en `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §A. Modelo autor: no autodeclarado en el cuerpo del documento. sha256 del adjunto verificado contra el paquete de lanzamiento del 19/ago/2026: `d26b8251db8ec23a8c818e9e22a4729cac59fbb0769e2ba3de326b933daa4465`, coincidencia exacta. Archivado verbatim, sin edición de cuerpo; a partir de este commit es base de evidencia fechada del programa y no se retoca (mismo patrón que `compass-4`, doctrina `FP-57`/`ADR-114`).

*Informe adversarial para dirección · sesión limpia con búsqueda web · 19/ago/2026 · insumo para el CAREO previo a sellar APERTURA v1.2*

---

## 1. Lo que enseña el mejor trabajo existente

### 1.1 Fragile Families Challenge: el techo de predictibilidad

El precedente más directo para "predecir conducta/desenlaces de vida con datos ricos" es el Fragile Families Challenge (Salganik et al., PNAS 2020): 160 equipos compitieron por predecir seis desenlaces a los 15 años usando datos de nacimiento a los 9 años, sobre una cohorte longitudinal de más de 4,000 familias estadounidenses seguida durante 15 años. El resultado central: ni siquiera los modelos más sofisticados de machine learning lograron predicciones precisas de los desenlaces de vida, y la conclusión explícita de los autores es que los tomadores de decisión no deben asumir que modelos complejos producirán automáticamente predicciones exactas sobre el futuro de un individuo. Además, los mejores modelos apenas superaron un benchmark lineal con un puñado de predictores elegidos por un experto — la ganancia de la sofisticación fue marginal.

El seguimiento de 2024 (Lundberg et al., PNAS) profundiza: mediante entrevistas cualitativas con 40 familias de la misma cohorte y una descomposición matemática del error de predicción, los autores concluyen que la impredecibilidad debe *esperarse* en muchas tareas de predicción de desenlaces de vida, incluso con algoritmos complejos y datasets grandes, distinguiendo dos fuentes aditivas de error con orígenes conceptualmente distintos: error irreducible y error de aprendizaje. Y el comentario de PNAS agrega el matiz clave para el programa: no poder predecir desenlaces individuales no implica no entenderlos — los modelos siguen sirviendo para descripción agregada, identificación causal y diseño de intervenciones.

**Portable al duelo:** (a) el resultado más probable en varias celdas es que L y M queden *ambos* lejos de R — el diseño debe tratar "ambos lejos" como resultado de primera clase, no como anomalía; (b) sin un baseline trivial nadie sabe si "ganar" significa algo; (c) hay que pre-declarar qué afirmación explicativa/estructural de M sobrevive aunque pierda el duelo predictivo.

### 1.2 Competencias de pronóstico y la ola LLM-forecaster

Las M-competitions aportan la arquitectura: benchmarks ingenuos obligatorios, reglas de scoring propias (pinball loss para cuantiles en M5), y la lección repetida de que las combinaciones superan a los métodos individuales. La M6 (Makridakis et al., IJF 2024/2025) añadió tres innovaciones directamente relevantes: evaluación en vivo sobre datos reales a través de múltiples periodos (a diferencia de las cuatro competencias anteriores, que usaron evaluación de origen fijo con un solo split dentro/fuera de muestra), un marco cross-seccional de desempeño relativo, y evaluación directa de la utilidad de los pronósticos para decisiones — encontrando una desconexión notable entre exactitud de pronóstico y calidad de decisión.

Sobre LLMs como pronosticadores, el estado del arte se mueve rápido pero es medible porque el campo resolvió la contaminación por diseño:

- **Halawi et al. (2024):** entrenaron con preguntas anteriores al 1 de junio de 2023 y evaluaron solo con preguntas posteriores al corte de pre-entrenamiento. Su sistema con recuperación de noticias logró Brier de .179 contra .149 de la multitud humana, superándola específicamente cuando la multitud estaba incierta (predicciones entre .3 y .7).
- **Schoenegger et al. (2024):** un ensemble de doce LLMs alcanza exactitud estadísticamente indistinguible de una multitud de 925 humanos — pero con solo ~30 preguntas, lo que limita severamente su poder estadístico; un análisis citado estima que con ese N un pronosticador con 50% de ruido "ganaría" 24% de las veces. Ese es exactamente el tamaño del set v1 del duelo.
- **ForecastBench (Karger et al., ICLR 2025; actualizaciones FRI 2025–2026):** institucionalizó la solución — benchmark dinámico, libre de contaminación, con preguntas probabilísticas continuamente actualizadas; el banco se actualiza cada noche desde mercados de predicción (Manifold, Metaculus, Polymarket, RAND) y datasets (ACLED, FRED, Wikipedia, Yahoo! Finance). Resultados vigentes: en octubre de 2025 los superforecasters mantenían ventaja con Brier ajustado por dificultad de 0.081 contra 0.101 del mejor LLM, con extrapolación lineal sugiriendo paridad hacia noviembre de 2026; en enero de 2026 la brecha era de 0.017 puntos Brier — equivalente a un año de progreso de los modelos — con sistemas externos basados en ensembles y recuperación en los puestos 2 y 3. Sistemas agénticos especializados (AIA Forecaster, nov 2025) ya igualan el Brier de superforecasters en la partición de mercado (0.0753 vs 0.0740) vía búsqueda de evidencia, agregación y calibración post-hoc.
- **Torneos trimestrales de Metaculus (AI Benchmarking Series, 2024–2025):** los Pro Forecasters superaron significativamente a los bots (Q1 2025: p = 0.001, t-test unilateral sobre spot peer scores); el factor dominante es el modelo subyacente más que el scaffolding; y los bots ganadores hacen algo muy simple: una búsqueda, un prompt, cinco pronósticos por pregunta y una agregación. La ventaja Pro es mayor en preguntas no binarias.
- **Advertencia transversal (síntesis 2026):** los papers que afirman paridad bot-superforecaster vía backtesting retrospectivo contra preguntas ya resueltas son desconfiables por fuga de información en sus pipelines; la evaluación creíble es en vivo, hacia adelante.

**Portable al duelo:** contaminación resuelta por diseño temporal (no por confianza); scoring propio (Brier/log/CRPS); L debe ser agregado de k corridas, no una corrida; versión y fecha del modelo son parte del resultado ("los LLM" no ganan ni pierden — *un* modelo fechado sí); N=10-15 solo alcanza para descripción, no para veredicto inferencial.

### 1.3 Hubs epidemiológicos: baseline, ensemble y score de intervalos

Los hubs (COVID-19 Forecast Hub, CDC FluSight, hub europeo) son el estándar de oro operativo para duelos multi-modelo contra dato real. Tres piezas:

1. **El score.** La métrica primaria es el weighted interval score (WIS), que mide qué tan consistente es una colección de intervalos de predicción con el valor observado (Bracher et al., 2021); es una regla propia que aproxima el CRPS, se interpreta como una generalización del error absoluto a pronósticos probabilísticos, y se descompone en agudeza más penalizaciones por sobre- y sub-predicción. Formato estandarizado de cuantiles para todos los participantes.
2. **El baseline obligatorio.** El COVIDhub-baseline fue diseñado como modelo neutral de referencia — mediana igual al último valor observado, con incertidumbre derivada de los cambios históricos de la serie — y todo se reporta como WIS relativo: la razón de WIS medios entre un modelo y el baseline, a través de todos los horizontes, ubicaciones y fechas.
3. **El ensemble como vara.** Hubo alta variación de exactitud entre y dentro de modelos individuales, mientras el ensemble que combinaba todos los modelos elegibles fue consistentemente más preciso y superó el desempeño de todos los modelos que lo componían (Cramer et al., PNAS 2022). Para comparar corredores con cobertura desigual de preguntas se usan comparaciones pareadas escaladas contra un modelo de referencia. Estas prácticas siguen vivas en los ensembles entrenados de FluSight 2022–2025.

**Portable al duelo:** el duelo tiene dos corredores y le faltan dos: el baseline ingenuo B y el ensemble L⊕M. Sin B, "M venció a L" es ininterpretable; sin L⊕M, el duelo no responde la pregunta económicamente valiosa (¿la combinación supera a ambos?). Y con N chico, los hubs no declaran ganadores por conteo: promedian scores relativos sobre muchas celdas-horizonte-ubicación.

### 1.4 Silicon sampling: cuándo un LLM representa una distribución y cuándo la aplana

**El lado optimista.** Argyle et al. (2023) mostraron que GPT-3 condicionado con historias sociodemográficas de participantes reales exhibe "fidelidad algorítmica" — reproduce distribuciones de respuesta correlacionadas demográficamente a través de subgrupos. Park et al. (2024) elevaron el techo: agentes construidos desde entrevistas cualitativas de dos horas con 1,052 individuos reales replican sus respuestas del General Social Survey con 85% de la exactitud con que los propios participantes replican sus respuestas dos semanas después (exactitud cruda de 65.67% dividida por la auto-consistencia humana de 79.53%), reduciendo además los sesgos de exactitud entre grupos raciales e ideológicos frente a agentes basados solo en demografía; el resultado se reprodujo casi exacto al re-correr con modelos más nuevos en 2025. La lección: el condicionamiento rico con datos idiosincráticos hace que el modelo recurra menos a generalizaciones basadas en raza, y los prompts solo-demográficos producen resultados significativamente menos precisos que los que incorporan contexto.

**El lado crítico (2024–2026), contundente:**

- Bisbee et al. (2024): las respuestas sintéticas comprimen la varianza y voltean el signo de efectos en ~32% de los casos en ítems del ANES.
- Boelaert et al. (2025): "machine bias" de opinión socialmente inconsistente entre temas — no espeja a ninguna población humana.
- Wang et al. (2025): los LLMs con personas de identidad tergiversan y aplanan grupos minoritarios; Li et al. (2025) lo formalizan como homogeneización "Das Man" impulsada por decodificación maximizadora de exactitud.
- Zhou et al. (2025): incluso con muestreo aleatorio repetido, la población de silicio sobrerrepresenta grupos y es mucho más determinista que los humanos en ítems actitudinales.
- La varianza artificialmente baja aparece también en baterías psicológicas, juicios morales, ítems del GSS y respuestas al American Community Survey; y los LLMs interpolan dentro de datos existentes en lugar de extrapolar, que es justo lo que se les pediría al sustituir levantamiento de dato nuevo.
- Santurkar et al. (2023, OpinionQA): desalineación sustancial entre las opiniones reflejadas por los LMs y las de 60 grupos demográficos de EE.UU. — del orden de la brecha demócrata-republicana en cambio climático — que persiste incluso al dirigir explícitamente el modelo hacia el grupo.

**Para México importa el sesgo cultural:** los LLMs se anclan en perfiles WEIRD aun cuando el país está explícito en el prompt (Atari et al.; Kharchenko et al.); los modelos evaluados contra encuestas nacionalmente representativas se parecen a países angloparlantes y protestantes europeos, aunque el "cultural prompting" acorta la brecha en 71–81% de las jurisdicciones (Tao et al., 2024); las respuestas tienden a parecerse a las opiniones de EE.UU. y algunos países europeos y sudamericanos, y al forzar la perspectiva de un país pueden aflorar estereotipos culturales dañinos (Durmus et al.). Casi toda esa evaluación, además, es de un solo turno y en inglés, incluso cuando la población objetivo no habla inglés — el idioma del prompt es una variable del duelo, no un detalle.

**Portable al duelo:** L no debe evaluarse solo en el punto (media/tasa): hay que medir forma, varianza y subgrupos (sexo, región, decil) contra el microdato, con chequeo explícito anti-aplanamiento; correr L en español y en inglés como sensibilidad; y reconocer que "L con acceso al corpus tierizado" y "L a pelo" son corredores distintos (el corpus es la "entrevista" de Park — legítimo, pero pre-registrado y etiquetado).

---

## 2. Rúbrica top-tier y calificación del diseño

Escala por dimensión: **2** = práctica top-tier · **1** = parcial · **0** = ausente o por debajo del estándar.

| # | Dimensión | Qué exige el estado del arte (fuente) | Nota | Brecha concreta del diseño |
|---|---|---|---|---|
| 1 | Pre-registro y congelamiento | Espec congelada antes de datos, evaluación hacia adelante, no retrospectiva (M6, ForecastBench, Metaculus) | **2** | Los dos commits y la espec congelada son genuinamente top-tier; pocos papers de silicon sampling lo hacen. |
| 2 | Contaminación de entrenamiento (L) | Preguntas/árbitros posteriores al corte del modelo, u olas retenidas; la contaminación se resuelve por diseño temporal, nunca por confianza (Halawi, ForecastBench) | **0** | Las encuestas-árbitro casi seguro están en el pre-entrenamiento; nada en el diseño lo aísla. |
| 3 | Circularidad dentro/fuera de muestra (M) | Split explícito: parámetros de una ola/fuente, árbitro de otra; evaluación de origen rodante, no fijo (M6) | **1** | Las clases de procedencia (medido/parcial/asignado) existen — por delante de la mayoría — pero no se usan para separar el marcador en "in-sample" vs "out-of-sample". |
| 4 | Regla de scoring propia | Brier/log para probabilidades; CRPS/WIS/pinball para distribuciones; calibración además de exactitud (hubs, M5, GJP) | **0** | "Distancia a R en la escala de R" no es regla propia, no premia calibración y es manipulable con predicciones de punto sin incertidumbre. |
| 5 | Incertidumbre del árbitro | R trae EE/CV de diseño muestral; se evalúa contra la distribución de R o en unidades de su error estándar; celdas con IC ancho se marcan o excluyen | **0** | El diseño trata a R como verdad puntual. |
| 6 | Baseline obligatorio | Corredor ingenuo B (tasa base / última ola / regresión simple tipo FFC); todo score se reporta relativo a B (hubs, FFC) | **0** | Ausente. Sin B, "ganar" el duelo no licencia ninguna afirmación de competencia absoluta. |
| 7 | Ensemble como vara | La combinación de modelos supera consistentemente a los componentes; el híbrido es el cuarto corredor obligado (COVID Hub, silicon crowd) | **0** | No contemplado — y es el hallazgo más robusto de dos de las cuatro literaturas. |
| 8 | Poder estadístico y criterio de decisión | Test pre-registrado (signos/permutación), banda de equivalencia para empates, magnitudes y no solo conteos; N dimensionado (M-comps, hubs) | **1** | "≥X de N" está pre-declarado (bien), pero con N=15 y test de signos unilateral a α=.05 se necesitan 12/15 victorias, y un corredor genuinamente superior que gane 70% de las preguntas solo cruza esa barra ~30% de las veces. El v1 solo puede ser descriptivo. |
| 9 | Selección y estratificación del set | Selección independiente o adversarial-conjunta; estratificación por dominio/dificultad/tasa base; universo de preguntas pre-registrado antes de muestrear (ForecastBench muestrea de un banco) | **0** | El dueño del motor elige las preguntas; sesgo de selección en ambas direcciones sin control. |
| 10 | Objeto de comparación: distribución, no solo punto | Fidelidad distribucional (forma, varianza, subgrupos), chequeo anti-aplanamiento, sensibilidad al idioma del prompt (crítica al silicon sampling) | **1** | Escalas y universos declarados es buena higiene, pero el marcador parece puntual; sin subgrupos ni varianza, un L aplanado puede "ganar" la media perdiendo la población. |
| 11 | Reproducibilidad de la generación | No basta congelar el artefacto: versión/fecha del modelo, prompt pre-registrado, k corridas con agregación declarada (Metaculus: 5 corridas + mediana) | **1** | El commit congela *una* corrida; el proceso generador de L (modelo, temperatura, k, quién lo corre) queda sin fijar, y el redactor conoce el motor. |
| 12 | Mapa de consecuencias y techo de predictibilidad | Pre-declarar qué prueba y qué NO prueba cada desenlace; "ambos lejos de R" como resultado de primera clase; expectativas ancladas al techo FFC; predicción ≠ explicación | **0** | El duelo binario L-vs-M no tiene tercer resultado ni mapa de afirmaciones; el desenlace más probable según FFC ni siquiera tiene casilla. |

**Total: 6/24.**

**Veredicto:** el diseño tiene **disciplina de proceso casi top-tier** (commits, congelamiento, procedencia, regla de honestidad semanal — cosas que buena parte de la literatura de silicon sampling ni intenta) montada sobre un **motor de medición por debajo del estándar**: score impropio, árbitro sin incertidumbre, sin baseline, sin ensemble, sin poder estadístico y sin control de contaminación. En su forma actual, el duelo puede ejecutarse impecablemente y aun así declarar un ganador que ningún hub, M-competition ni benchmark dinámico aceptaría como establecido.

---

## 3. Qué tomar de cada mundo (el paquete mínimo, sin purismo)

**De los hubs:** convertir el duelo de 2 a 4 corredores — L, M, **B** (baseline ingenuo: tasa base de la ola anterior o regresión de 3-4 variables a la FFC) y **H** (híbrido L⊕M, agregación pre-registrada). El titular no es "¿L o M?" sino la matriz completa: quién supera a B, y si H supera a ambos. Score: si los corredores entregan distribuciones, CRPS/WIS; si probabilidades, Brier/log; reportar siempre magnitud relativa a B, no solo conteo de victorias.

**Del Fragile Families:** pre-declarar el techo — para cada celda, anotar antes de abrir datos cuánto explica el predictor trivial, y registrar "ambos lejos de R" como desenlace con consecuencias propias (probablemente el más informativo para el programa). Y separar por escrito la afirmación predictiva de la explicativa: que M pierda en predicción no invalida su valor estructural/causal, pero eso solo es defendible si se dijo *antes* del marcador.

**De la ola LLM-forecaster:** contaminación por diseño temporal — al menos 3-5 preguntas cuyo árbitro se resuelve o publica después del corte del modelo (ola nueva de encuesta, desenlace 2026), más olas retenidas (parametrizar M con la ola vieja, arbitrar con la nueva, para L y para M simétricamente) y 2-3 contrafactuales/perturbadas que la memoria no responde. L = mediana de k≥5 corridas con prompt pre-registrado, en sesión limpia sin contexto del motor, con modelo+versión+fecha fijados en el commit; el veredicto se fecha ("Modelo X, agosto 2026"), porque la brecha con humanos se mueve del orden de 0.015 Brier por año.

**Del silicon sampling:** marcador secundario distribucional obligatorio en las celdas donde R es microdato — distancia de forma (KS/Wasserstein), razón de varianzas sintética/muestral como alarma de aplanamiento, y al menos un corte por subgrupo mexicano (sexo, región o decil) por celda; sensibilidad español/inglés del prompt de L; y dos variantes de L etiquetadas (con y sin acceso al corpus tierizado), porque la evidencia dice que el condicionamiento rico es donde los LLMs realmente rinden — esa comparación interna vale casi tanto como el duelo mismo.

Con esos cuatro injertos — B y H como corredores, score propio con incertidumbre del árbitro, aislamiento temporal de contaminación, y capa distribucional — el duelo v1 queda honesto como **piloto descriptivo** de 10-15 celdas, y el criterio inferencial "≥X de N" se difiere a un v2 con N≥40-60 celdas, que es donde el estado del arte empezaría a creerle un ganador.

---

## Fuentes principales

- Salganik, M. J., et al. (2020). *Measuring the predictability of life outcomes with a scientific mass collaboration.* PNAS 117.
- Lundberg, I., et al. (2024). *The origins of unpredictability in life outcome prediction tasks.* PNAS 121(24).
- Makridakis, S., et al. (2024/2025). *The M6 forecasting competition: Bridging the gap between forecasting and investment decisions.* International Journal of Forecasting 41(4).
- Halawi, D., Zhang, F., Chen, Y.-H., & Steinhardt, J. (2024). *Approaching Human-Level Forecasting with Language Models.* NeurIPS 2024.
- Schoenegger, P., et al. (2024). *Wisdom of the Silicon Crowd.*
- Karger, E., et al. (2025). *ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities.* ICLR 2025; actualizaciones del Forecasting Research Institute (oct 2025, ene 2026); Alur et al. (2025), *AIA Forecaster*.
- Metaculus AI Benchmarking Series, reportes trimestrales Q3 2024 – Q2 2025; síntesis "AI Forecasting in 2026: What 11 Analyses Say" (2026).
- Cramer, E. Y., et al. (2022). *Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality in the United States.* PNAS 119.
- Bracher, J., et al. (2021). *Evaluating epidemic forecasts in an interval format.* PLOS Computational Biology.
- Evaluaciones FluSight 2022–2025 (ensembles entrenados, rWIS vs baseline).
- Argyle, L., et al. (2023). *Out of One, Many.* Political Analysis.
- Santurkar, S., et al. (2023). *Whose Opinions Do Language Models Reflect?* (OpinionQA). ICML.
- Park, J. S., et al. (2024). *Generative Agent Simulations of 1,000 People.*
- Bisbee, J., et al. (2024), Political Analysis; Boelaert et al. (2025); Wang et al. (2025); Li et al. (2025); Zhou et al. (2025) — críticas de varianza, aplanamiento y "machine bias".
- Durmus, E., et al. (2023). *Towards measuring the representation of subjective global opinions in language models*; Tao et al. (2024); Atari et al. (2023) — sesgo WEIRD y cultural prompting.
