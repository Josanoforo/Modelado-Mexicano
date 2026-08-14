# Estado del arte metodológico: fijación y estimación de parámetros en modelos basados en agentes (ABM) y de simulación

## TL;DR
- No existe una única "práctica establecida": conviven tres familias con supuestos distintos. La estimación coeficiente-a-coeficiente contra microdatos (econometría de elección/latente) exige declarar una función de enlace y una normalización de escala; la calibración contra salidas agregadas (SMM/inferencia indirecta, calibración bayesiana KOH, history matching, emulación GP, ABC) opera sobre el output del modelo y **no** requiere enlace por coeficiente. Para el problema descrito, esto es decisivo.
- La obstrucción del equipo (estimandos en escala de diferencia-de-proporciones vs. escala del índice) es un problema real y bien fundado: un coeficiente de índice latente está identificado sólo hasta una escala fijada por la distribución del error (enlace). Importar un estimando en escala de probabilidad exige un modelo de enlace/medición que no tienen. La salida recomendada es **no** inscribir β directamente, sino calibrar el conjunto de β contra momentos/proporciones agregadas que el ABM reproduce (SMM/history matching), tratando la diferencia-de-proporciones como el momento objetivo, no como el coeficiente.
- Toda familia tiene críticas publicadas graves: no-identificabilidad de θ vs. discrepancia en KOH (Brynjarsdóttir & O'Hagan 2014; Tuo & Wu 2015), maldición de la dimensión y sesgo bajo mala especificación en ABC (Frazier, Robert & Rousseau 2020), equifinalidad y "sloppiness" endémicas en ABM. El subcampo está fragmentado en comunidades (econometría, UQ/computer-experiments, ABM/complejidad, microsimulación) que apenas se citan entre sí.

## Key Findings

### 1. Las dos grandes rutas y por qué la ruta agregada evita el enlace

**Hallazgo 1 — Familia de "distancia mínima simulada" (SMM, inferencia indirecta).** (Tier d2)
- CLAIM: La inferencia indirecta y el método de momentos simulados estiman el vector completo de parámetros minimizando la distancia entre estadísticos de resumen (momentos, o parámetros de un modelo auxiliar) calculados sobre datos reales y sobre datos simulados por el modelo; operan sobre la salida agregada del simulador, no sobre cada coeficiente por separado.
- CONDICIONES: requiere ergodicidad/estacionariedad para que los momentos simulados converjan, elección previa de estadísticos de resumen y de una matriz de ponderación; el número de momentos debe ser ≥ número de parámetros para identificación.
- IMPLICACIÓN: para el diseño descrito, esta ruta permite usar la diferencia-de-proporciones observada en la encuesta como el momento objetivo y buscar los β del índice que hacen que el ABM reproduzca esa diferencia — sin declarar función de enlace, porque el enlace queda implícito en el propio mecanismo del modelo. Es la ruta que disuelve el obstáculo declarado.
- FUENTE: Gourieroux, Monfort & Renault, "Indirect Inference", Journal of Applied Econometrics 8:S85–S118 (1993), DOI 10.1002/jae.3950080506; Grazzini & Richiardi, Journal of Economic Dynamics and Control 51:148–165 (2015), DOI 10.1016/j.jedc.2014.10.006.

**Hallazgo 2 — Consistencia de SMM para ABM requiere ergodicidad.** (Tier d1/d2)
- CLAIM: Grazzini & Richiardi demuestran que los ABM ergódicos pueden estimarse consistentemente por distancia mínima simulada tanto en equilibrio de largo plazo como en fase de ajuste, pero la consistencia depende críticamente de que el modelo sea ergódico y estacionario.
- CONDICIONES: ergodicidad y estacionariedad del proceso simulado; sin ellas, los momentos de una sola corrida larga no estiman los momentos poblacionales.
- IMPLICACIÓN: antes de calibrar, el equipo debe verificar que su ABM sea ergódico en las variables que producen las proporciones agregadas; si hay dependencia de condiciones iniciales o absorción, la estimación por momentos no es válida.
- FUENTE: Grazzini & Richiardi, J. Econ. Dyn. Control 51:148–165 (2015), DOI 10.1016/j.jedc.2014.10.006.

**Hallazgo 3 — Estimación coeficiente-a-coeficiente contra microdatos exige normalización de escala (enlace).** (Tier d1)
- CLAIM: En cualquier modelo de índice latente G = Σβᵢθᵢ que genera una respuesta binaria/de umbral, β está identificado sólo hasta una escala fijada por la varianza del error; una normalización de escala (equivalentemente, declarar la CDF de error/enlace) es una necesidad matemática de identificación. Como muestra Train (2009), al normalizar la varianza del error a 1 "los coeficientes logit pueden dividirse por √1.6, para que la varianza del error sea 1, igual que en el modelo probit" — la reescala es mecánica y depende del enlace asumido, no del dato.
- CONDICIONES: modelos de cruce de umbral / elección discreta; la normalización no es inocua: distintos enlaces reescalan β.
- IMPLICACIÓN: confirma formalmente la objeción del equipo. No se puede inscribir un estimando de encuesta como β sin declarar el modelo de enlace/medición que fija la escala. La estimación directa por microdatos **no** evita el problema; lo hace explícito.
- FUENTE: Manski, "Semiparametric analysis of discrete response", Journal of Econometrics 27(3):313–333 (1985), DOI 10.1016/0304-4076(85)90009-0; Train, Discrete Choice Methods with Simulation, 2ª ed., Cambridge University Press (2009), DOI 10.1017/CBO9780511805271.

**Hallazgo 4 — El factor de escala logit/probit hace concreto el problema.** (Tier d1)
- CLAIM: El mismo índice latente produce magnitudes de coeficiente sistemáticamente distintas según el enlace: los coeficientes logit ≈ 1.6× los probit, sólo porque el error logístico tiene varianza π²/3 ≈ 3.29 frente a 1 del normal estándar. Greene lo deriva explícitamente: "si los efectos marginales han de ser iguales, entonces 0.3989 β_pk = 0.25 β_lk, o β_lk = 1.6 β_pk, la regularidad observada por Amemiya"; y advierte que "al alejarnos del centro de la distribución, la relación se apartará de 1.6... el cociente tenderá a ser mayor que 1.6". Un efecto marginal (escala de probabilidad) = β × f(índice); recuperar β desde una cantidad en escala de probabilidad exige dividir por una densidad que depende del enlace desconocido.
- CONDICIONES: cualquier mapeo GLM/índice latente; el mapeo entre efectos en probabilidad y coeficientes del índice depende del punto del espacio de covariables donde se evalúa y del error asumido, y sólo vale ≈1.6 en el centro de la distribución.
- IMPLICACIÓN: la diferencia-de-proporciones y el coeficiente del índice **no** son intercambiables; convertir uno en otro requiere la derivada del enlace. Esto es exactamente por qué "escribir β" desde la proporción es ilegítimo sin evidencia del enlace.
- FUENTE: Amemiya, "Qualitative Response Models: A Survey", Journal of Economic Literature 19:1483–1536 (1981); Greene, Econometric Analysis (cap. Discrete Choice); Manski (1985), DOI 10.1016/0304-4076(85)90009-0.

### 2. Para cada método: ¿requiere enlace por coeficiente o no?

**Hallazgo 5 — Calibración bayesiana de Kennedy–O'Hagan (KOH).** (Tier d2)
- CLAIM: KOH modela las observaciones como Y = m(θ,x) + δ(x) + ε, donde m es el simulador con parámetros de calibración θ, δ una función de discrepancia (proceso gaussiano) y ε ruido; infiere θ por vía bayesiana operando sobre la salida del modelo comparada con observaciones reales.
- CONDICIONES: requiere emulador GP del simulador y priors; **no** requiere declarar una función de enlace por coeficiente, pues opera sobre el output agregado.
- IMPLICACIÓN: aplicable al diseño sin declarar enlace, pero con la advertencia crítica del Hallazgo 9 (no-identificabilidad de θ frente a δ).
- FUENTE: Kennedy & O'Hagan, JRSS-B 63(3):425–464 (2001), DOI 10.1111/1467-9868.00294.

**Hallazgo 6 — History matching (HM).** (Tier d2/d3)
- CLAIM: HM no busca el "mejor" θ sino que descarta por olas las regiones del espacio de parámetros "implausibles", usando una medida de implausibilidad I(x)=|E[f(x)]−z|/√(Var_emulador+Var_discrepancia+Var_obs); lo que queda es la región "no descartada aún" (NROY).
- CONDICIONES: umbral típico de implausibilidad 3 (regla tres-sigma de Pukelsheim); requiere cuantificar las tres varianzas; opera sobre salidas agregadas, sin enlace por coeficiente. La región NROY puede quedar vacía, lo que es diagnóstico de mala especificación.
- IMPLICACIÓN: idóneo para el diseño porque entrega directamente el **conjunto** de β compatibles con las proporciones observadas (aborda de frente la equifinalidad) en vez de un punto espurio, y no necesita enlace.
- FUENTE: Craig, Goldstein, Seheult & Smith, "Pressure matching…", Lecture Notes in Statistics (1997); Vernon, Goldstein & Bower, Bayesian Analysis 5(4):619–669 (2010), DOI 10.1214/10-BA524.

**Hallazgo 7 — Emulación por procesos gaussianos (GP).** (Tier d2)
- CLAIM: Cuando el simulador es costoso, se sustituye por un emulador GP que predice su salida con incertidumbre; el emulador se usa dentro de KOH, HM o ABC para explorar el espacio de parámetros a coste bajo.
- CONDICIONES: supone estacionariedad/suavidad de la superficie de respuesta; escala mal en alta dimensión de entradas y de salidas (típicamente se reduce por componentes principales).
- IMPLICACIÓN: habilita cualquiera de las rutas agregadas para un ABM costoso; no introduce enlace por coeficiente, pero sus supuestos de estacionariedad deben verificarse.
- FUENTE: Kennedy & O'Hagan (2001), DOI 10.1111/1467-9868.00294; Salter et al., JASA 114:1800–1814 (2019), DOI 10.1080/01621459.2018.1514306.

**Hallazgo 8 — Approximate Bayesian Computation (ABC).** (Tier d2)
- CLAIM: ABC aproxima la posterior sin verosimilitud: simula del modelo, resume datos reales y simulados en estadísticos de resumen y acepta parámetros cuyos resúmenes simulados caen a distancia < tolerancia de los observados; opera sobre salida agregada, sin enlace por coeficiente.
- CONDICIONES: requiere elegir estadísticos de resumen (idealmente suficientes) y tolerancia; sufre maldición de la dimensión.
- IMPLICACIÓN: viable con la diferencia-de-proporciones como estadístico de resumen; produce una posterior sobre β (útil para diagnosticar equifinalidad), pero con los sesgos del Hallazgo 18.
- FUENTE: Beaumont, "Approximate Bayesian computation in evolution and ecology", Annu. Rev. Ecol. Evol. Syst. 41:379–406 (2010), DOI 10.1146/annurev-ecolsys-102209-144621.

### 3. Equifinalidad e identificabilidad

**Hallazgo 9 — No-identificabilidad de KOH: θ frente a δ.** (Tier d1)
- CLAIM: En KOH, los parámetros de calibración θ y la función de discrepancia δ **no** son conjuntamente identificables; distintas configuraciones de ambos explican los datos igual de bien. θ sólo converge a su valor físico si no hay discrepancia, o si δ tiene media cero y es independiente de θ. Con discrepancia sistemática, las estimaciones de θ son sesgadas y el único remedio es conocer a priori la forma de δ.
- CONDICIONES: presencia de discrepancia sistemática (garantizada en ABM sociales, que siempre son abstracciones); δ modelado con GP flexible.
- IMPLICACIÓN: crucial. Si el equipo interpretara los β calibrados por KOH como "efectos psicosociales verdaderos", incurriría en sesgo; los β así obtenidos son parámetros de ajuste, no cantidades con interpretación sustantiva, salvo con priors fuertes sobre la discrepancia.
- FUENTE: Brynjarsdóttir & O'Hagan, "Learning about physical parameters: the importance of model discrepancy", Inverse Problems 30(11):114007 (2014), DOI 10.1088/0266-5611/30/11/114007.

**Hallazgo 10 — Inconsistencia L2 de KOH (Tuo & Wu).** (Tier d1)
- CLAIM: Una versión simplificada del método KOH es asintóticamente L2-inconsistente en la estimación de calibración; puede dar estimaciones no razonables para modelos imperfectos. Proponen la "calibración L2" y prueban su eficiencia semiparamétrica.
- CONDICIONES: modelos computacionales imperfectos (con discrepancia); resultado asintótico.
- IMPLICACIÓN: refuerza que no debe confiarse en el punto β de KOH como estimación insesgada; conviene métodos con garantías (L2/kernel proyectado) o interpretar β sólo como ajuste predictivo.
- FUENTE: Tuo & Wu, "Efficient calibration for imperfect computer models", Annals of Statistics 43(6):2331–2352 (2015), DOI 10.1214/15-AOS1314.

**Hallazgo 11 — Equifinalidad en ABM y modelos "sloppy".** (Tier d2)
- CLAIM: En ABM es endémico que múltiples conjuntos de parámetros produzcan la misma salida agregada (equifinalidad); en modelos multiparamétricos esto se manifiesta como "sloppiness": la salida es muy sensible a pocas combinaciones no lineales de parámetros y esencialmente insensible a otras. Gutenkunst et al. (2007) documentan que "los autovalores de sensibilidad estaban aproximadamente equiespaciados sobre muchas décadas"; una separación de más de 3 órdenes de magnitud en los autovalores basta para considerar el modelo sloppy (Chis, Villaverde et al. 2016), llegando en algunos casos a abarcar ~20 órdenes de magnitud.
- CONDICIONES: modelos con muchos parámetros interactuantes; se diagnostica con análisis de identificabilidad estructural/práctica (no basta el análisis de sloppiness, que puede ser engañoso: modelos sloppy pueden ser identificables).
- IMPLICACIÓN: con sólo unas pocas proporciones agregadas como objetivo, es improbable que los β del índice queden identificados individualmente; lo esperable es una variedad (manifold) de β equivalentes. El equipo debe reportar la región compatible, no un punto, y hacer análisis de identificabilidad práctica.
- FUENTE: Gutenkunst et al., PLoS Comp. Biol. 3(10):e189 (2007), DOI 10.1371/journal.pcbi.0030189; Transtrum et al., J. Chem. Phys. 143(1):010901 (2015), DOI 10.1063/1.4923066; Chis, Villaverde, Banga & Balsa-Canto, Math. Biosci. 282:147–161 (2016), DOI 10.1016/j.mbs.2016.10.009.

### 4. Calibración con datos de ENCUESTA con diseño muestral complejo

**Hallazgo 12 — Estimación design-based de coeficientes: fundamento (Binder).** (Tier d1)
- CLAIM: Para cualquier parámetro "censal" definido por una ecuación de estimación suave, ponderar las funciones de estimación por los pesos muestrales (tipo Horvitz–Thompson) da un estimador design-consistente cuya varianza se obtiene aplicando la fórmula de varianza estratificada-por-conglomerados a los valores linearizados (función de influencia) por unidad.
- CONDICIONES: ecuaciones de estimación diferenciables (la regresión LAD/mediana es un caso de fallo conocido); el objetivo es consistencia respecto al diseño, no eficiencia del modelo.
- IMPLICACIÓN: da la base rigurosa para producir los estimandos de encuesta (proporciones, coeficientes) respetando estratos, PSU y pesos; pero produce estimandos en escala design-based, que siguen necesitando enlace para convertirse en β del índice (Hallazgos 3–4).
- FUENTE: Binder, "On the variances of asymptotically normal estimators from complex surveys", International Statistical Review 51(3):279–292 (1983), DOI 10.2307/1402588; Godambe & Thompson, Int. Stat. Rev. 54(2):127–138 (1986), DOI 10.2307/1403139.

**Hallazgo 13 — Ajuste de GLM a datos de encuesta con SE design-based.** (Tier d3)
- CLAIM: El tratamiento autoritativo moderno para ajustar modelos de regresión a datos de encuesta compleja es Lumley & Scott / el paquete `survey`: `svyglm` ajusta GLM ponderados y devuelve siempre errores estándar "model-robust" (tipo sándwich Horvitz–Thompson) por linearización de Taylor o pesos replicados; el objeto de diseño codifica explícitamente estratos, PSU/conglomerados, pesos y correcciones de población finita.
- CONDICIONES: pesos = inversos de probabilidad de inclusión, posiblemente calibrados; sigue vivo el debate sobre si ponderar en inferencia model-based.
- IMPLICACIÓN: es la maquinaria concreta que el equipo debe usar para obtener los estimandos (incluida la diferencia-de-proporciones) con incertidumbre correcta bajo diseño complejo, antes de cualquier calibración del ABM.
- FUENTE: Lumley & Scott, "Fitting regression models to survey data", Statistical Science 32(2):265–278 (2017), DOI 10.1214/16-STS605; Lumley, Complex Surveys, Wiley (2010), DOI 10.1002/9780470580066.

**Hallazgo 14 — "Calibración" en microsimulación ≠ "calibración" en computer-experiments.** (Tier d1/d3)
- CLAIM: En estadística de encuestas, "calibración" (Deville & Särndal) significa ajustar los pesos de diseño d_k a nuevos pesos w_k lo más próximos posible bajo una distancia (p.ej. chi-cuadrado Σ(w_k−d_k)²/(d_k q_k)) sujetos a que los totales ponderados de variables auxiliares igualen totales poblacionales conocidos (Σ w_k x_k = X); minimizar distancia chi-cuadrado con la restricción lineal da exactamente el estimador de regresión generalizada (GREG). Esto es reponderar-para-cuadrar-márgenes, operación radicalmente distinta de la calibración KOH (inferencia inversa de parámetros latentes).
- CONDICIONES: ganancia de eficiencia exige auxiliares correlacionados con la variable de estudio; el estimando es un total/media poblacional (o, vía ecuaciones de estimación, un coeficiente).
- IMPLICACIÓN: el equipo debe evitar la ambigüedad terminológica: "calibrar" la muestra (IPF/GREG para generar la población sintética inicial del ABM) y "calibrar" los β (inferencia inversa contra salidas) son dos operaciones distintas que probablemente ambas necesitarán.
- FUENTE: Deville & Särndal, "Calibration estimators in survey sampling", JASA 87(418):376–382 (1992), DOI 10.1080/01621459.1992.10475217; Deville, Särndal & Sautory, JASA 88(423):1013–1020 (1993), DOI 10.1080/01621459.1993.10476369.

**Hallazgo 15 — Inicialización de poblaciones sintéticas por IPF y pesos no enteros.** (Tier d2/d3)
- CLAIM: La microsimulación espacial usa IPF (o recocido simulado / GREGWT) para reponderar microdatos de encuesta de modo que reproduzcan márgenes censales de áreas pequeñas; los pesos de IPF son no enteros y deben "enterizarse" (p.ej. TRS: truncar-replicar-muestrear) antes de poblar un ABM.
- CONDICIONES: requiere microdatos individuales y tablas agregadas de restricción; IPF es determinista y converge a un único conjunto de pesos.
- IMPLICACIÓN: da la vía estándar para construir la población de agentes inicial a partir de la encuesta respetando su estructura; es complementaria (no sustituta) de la estimación de los β.
- FUENTE: Lovelace, Birkin, Ballas & van Leeuwen, JASSS 18(2):21 (2015), DOI 10.18564/jasss.2768; Tanton et al., JRSS-A 174(4):931–951 (2011), DOI 10.1111/j.1467-985X.2011.00690.x.

**Hallazgo 16 — Parametrización orientada a patrones (POM) como filtrado inverso.** (Tier d2/d3)
- CLAIM: POM usa múltiples patrones observados a distintas escalas como filtros para rechazar combinaciones de parámetros que no los reproducen; el resultado es típicamente un conjunto de conjuntos de parámetros que pasan todos los filtros (equivale a Monte Carlo filtering / modelado inverso), no un punto óptimo.
- CONDICIONES: requiere varios patrones informativos; un patrón "fuerte" restringe fuertemente el espacio (p.ej. Wiegand et al. calibraron 13 parámetros a la vez con 5 patrones; uno de ellos aceptó sólo una pequeña fracción de los conjuntos).
- IMPLICACIÓN: si el equipo dispone de varias proporciones/diferencias (por construcción, subgrupo, ola), usarlas como patrones-filtro simultáneos es la vía natural para restringir los β y atacar la equifinalidad sin declarar enlace.
- FUENTE: Grimm et al., "Pattern-oriented modeling of agent-based complex systems", Science 310(5750):987–991 (2005), DOI 10.1126/science.1116681.

### 5. Limitaciones y críticas por método (sin las cuales el review es inútil)

**Hallazgo 17 — Crítica a SMM/inferencia indirecta: arbitrariedad y mala especificación.** (Tier d2)
- CLAIM: SMM es criticado por la elección arbitraria de momentos en la función criterio; la inferencia indirecta desplaza esa arbitrariedad a la elección del modelo auxiliar. Bajo mala especificación del simulador, las fórmulas estándar de varianza asintótica dejan de valer: se requieren fórmulas "sándwich" dobles (una para el DGP, otra para el simulador, que difiere del DGP bajo mala especificación) y un tratamiento específico de las variables exógenas.
- CONDICIONES: simulador mal especificado (regla en ABM sociales); matriz de ponderación mal elegida degrada eficiencia.
- IMPLICACIÓN: el equipo no puede tomar los errores estándar por defecto; con un ABM casi seguramente mal especificado respecto de la realidad, la inferencia sobre β requiere corrección sándwich y análisis de sensibilidad a los momentos elegidos.
- FUENTE: Dridi, Guay & Renault, "Indirect inference and calibration of DSGE models", Journal of Econometrics 136(2):397–430 (2007), DOI 10.1016/j.jeconom.2005.11.009.

**Hallazgo 18 — Crítica a ABC: maldición de la dimensión, elección de resúmenes y sesgo bajo mala especificación.** (Tier d1/d2)
- CLAIM: ABC sufre maldición de la dimensión: al aumentar el número de estadísticos de resumen, la tasa de aceptación cae y crece el error de aproximación; los resúmenes rara vez son suficientes. Bajo mala especificación del modelo, distintas versiones de ABC dan resultados sustancialmente distintos: la posterior ABC de aceptación-rechazo concentra masa en un "pseudo-verdadero" pero **no** da intervalos con cobertura frecuentista válida, y el ajuste por regresión local puede **empeorar** la inferencia, desplazando la posterior a otro punto.
- CONDICIONES: alta dimensión de resúmenes; mala especificación (esperable en ABM sociales); comportamiento asintótico no estándar (no gaussiano).
- IMPLICACIÓN: si el equipo usa muchas proporciones como resúmenes, la aceptación colapsa; y como el ABM está mal especificado, los intervalos de credibilidad sobre β serán poco fiables y el post-procesamiento por regresión puede sesgar. Debe usar los diagnósticos de mala especificación de Frazier et al.
- FUENTE: Frazier, Robert & Rousseau, "Model misspecification in ABC: consequences and diagnostics", JRSS-B 82(2):421–444 (2020), DOI 10.1111/rssb.12356; Prangle, "Summary statistics in ABC", en Handbook of ABC (2018), arXiv:1512.05633 (no revisado por pares en esa forma).

**Hallazgo 19 — Crítica a emulación GP y a HM: estacionariedad, escala y falsa convergencia.** (Tier d2)
- CLAIM: Los emuladores GP suponen estacionariedad y escalan mal en alta dimensión de entrada/salida; en HM multi-ola se han documentado rasgos dependientes del diseño y del emulador que causan convergencia aparente pero prematura de las estimaciones de incertidumbre paramétrica. La descomposición por componentes principales de la salida puede inducir un "caso terminal" en que el modelo no puede reproducir las observaciones dentro de la discrepancia y la calibración estándar falla.
- CONDICIONES: salida de alta dimensión; base de proyección mal elegida; superficie de respuesta no estacionaria.
- IMPLICACIÓN: si el ABM produce muchas proporciones correlacionadas, la reducción por PCA puede sabotear la calibración; el equipo debe usar bases "calibración-óptimas" y verificar diagnósticos del emulador.
- FUENTE: Salter et al., "UQ for computer models with spatial output using calibration-optimal bases", JASA 114:1800–1814 (2019), DOI 10.1080/01621459.2018.1514306; Salter & Williamson, Environmetrics 27:507–523 (2016), DOI 10.1002/env.2405.

**Hallazgo 20 — Crítica a la estimación directa: incluso "óptima", el diseño experimental puede volver relevantes mecanismos omitidos.** (Tier d2)
- CLAIM: En sistemas sloppy, el diseño de experimentos y la estimación de parámetros "óptimos" pueden fallar: los modelos sloppy pueden dejar de ajustar bien los datos generados por experimentos "óptimos", y el diseño puede inadvertidamente volver relevantes detalles omitidos del modelo, reduciendo su poder predictivo.
- CONDICIONES: modelos aproximados (todos los ABM) con parámetros prácticamente no identificables.
- IMPLICACIÓN: perseguir el β "puntual óptimo" es frágil; es preferible caracterizar la variedad de β compatibles y su poder predictivo fuera de muestra.
- FUENTE: White, Tolman, Thames, Withers, Mason & Transtrum, "The limitations of model-based experimental design and parameter estimation in sloppy systems", PLoS Comp. Biol. 12(12):e1005227 (2016), DOI 10.1371/journal.pcbi.1005227.

### 6. Estado del subcampo: comunidades separadas

**Hallazgo 21 — Fragmentación en comunidades que apenas se citan.** (Tier d3)
- CLAIM: Coexisten al menos cuatro tradiciones con vocabularios y prácticas distintas: (i) econometría de estimación (inferencia indirecta, SMM, estimación bayesiana de ABM económicos: Gourieroux–Monfort–Renault, Grazzini–Richiardi, Platt); (ii) UQ/computer-experiments (KOH, history matching, emulación GP: Kennedy–O'Hagan, Craig–Vernon–Goldstein, Tuo–Wu); (iii) ABM/complejidad y ecología (POM, ABC aplicada: Grimm, Thiele); (iv) microsimulación/estadística de encuestas (IPF, calibración de pesos Deville–Särndal). El propio término "calibración" tiene significados incompatibles entre (ii) y (iv).
- CONDICIONES: observación bibliométrica/terminológica, no un teorema.
- IMPLICACIÓN: el equipo debe traducir explícitamente entre vocabularios y no asumir que "calibración" significa lo mismo para su estadístico de encuestas y para su modelador UQ; muchos hallazgos negativos de una comunidad son desconocidos en otra.
- FUENTE: Platt, "A comparison of economic agent-based model calibration methods", J. Econ. Dyn. Control 113:103859 (2020), DOI 10.1016/j.jedc.2020.103859; McCulloch et al., JASSS 25(2):1 (2022), DOI 10.18564/jasss.4791.

**Hallazgo 22 — Comparación empírica: bayesiano vs. frecuentista en ABM.** (Tier d2)
- CLAIM: En experimentos controlados de calibración de ABM económicos, la estimación bayesiana (menos popular en la literatura) supera consistentemente a los enfoques frecuentistas basados en función objetivo, pero ninguna técnica logra calibrar definitivamente modelos a gran escala. En palabras de Platt (2020): "Encontramos que la estimación bayesiana, aunque menos popular en la literatura, supera consistentemente a los enfoques frecuentistas basados en función objetivo y produce estimaciones de parámetros razonables en muchos contextos. A pesar de esto, también hallamos que las técnicas de calibración de ABM requieren mayor desarrollo para calibrar definitivamente modelos a gran escala."
- CONDICIONES: modelos financieros/económicos de escala pequeña-media; la degradación de rendimiento se observa "sólo al considerar un modelo a gran escala e intentar ajustar un subconjunto"; los métodos likelihood-free requieren muchas simulaciones.
- IMPLICACIÓN: para un ABM grande de constructos psicosociales, ninguna técnica garantiza identificación completa; se debe priorizar identificar el subconjunto de β realmente estimables y fijar el resto por juicio con análisis de sensibilidad.
- FUENTE: Platt, J. Econ. Dyn. Control 113:103859 (2020), DOI 10.1016/j.jedc.2020.103859.

## Details

El problema del equipo tiene una estructura precisa: un índice lineal latente cuyos coeficientes quieren anclarse a datos, y un estimando de encuesta (diferencia de proporciones) que vive en escala de probabilidad. La literatura ofrece un diagnóstico inequívoco (Hallazgos 3–4): un coeficiente de índice latente sólo está identificado hasta una escala, y esa escala la fija el enlace/error. Por eso "escribir β = diferencia de proporciones" es una operación mal definida sin un modelo de medición. La objeción del equipo es correcta y tiene respaldo tanto en la teoría de identificación de Manski como en la mecánica GLM (factor logit/probit ≈1.6, que además sólo vale en el centro de la distribución).

La salida no es inventar un enlace sin evidencia, sino cambiar de ruta: en lugar de estimar cada β contra microdatos (ruta que fuerza el enlace), calibrar el conjunto de β contra las proporciones agregadas que el propio ABM produce (rutas del §2). En SMM/inferencia indirecta, history matching, ABC o KOH, el objeto que se compara es la salida del modelo, y el "enlace" queda absorbido implícitamente por el mecanismo generativo del ABM: uno busca los β tales que el modelo reproduce la diferencia-de-proporciones observada. Esto disuelve el obstáculo declarado.

Ahora bien, disolverlo tiene un precio que el review honesto debe subrayar: (a) no-identificabilidad/equifinalidad (Hallazgos 9–11) — con pocas proporciones objetivo, muchos β distintos reproducen igual la salida; lo esperable es una variedad de soluciones, no un punto; (b) los β así obtenidos son parámetros de ajuste, no necesariamente "efectos psicosociales verdaderos" (Brynjarsdóttir & O'Hagan; Tuo & Wu); (c) mala especificación — un ABM social siempre tiene discrepancia sistemática, lo que sesga KOH y rompe la cobertura de ABC (Frazier et al.).

Sobre los datos de encuesta específicamente (§4): habilitan estimar correctamente los estimandos-objetivo (proporciones, coeficientes design-based) respetando estratos, PSU y pesos (Binder; Lumley & Scott), y habilitan construir la población de agentes inicial por reponderación (IPF/GREG; Deville–Särndal). Lo que **no** habilitan por sí solos es fijar la escala del índice: eso sigue requiriendo un modelo de enlace. Es decir, la encuesta resuelve la inicialización y la medición de objetivos agregados, pero no elimina la necesidad de una estrategia de calibración inversa para los β. Debe además notarse un matiz terminológico peligroso: en la comunidad de encuestas/microsimulación, "calibración" (Deville–Särndal, IPF, GREGWT) significa reponderar la muestra para cuadrar márgenes; en la comunidad UQ, "calibración" (KOH) significa inferir parámetros latentes contra observaciones. Son operaciones distintas y el equipo probablemente necesitará ambas.

## Recommendations

Escalonadas, con umbrales que cambiarían la decisión:

1. **Reencuadrar el estimando (inmediato).** Dejar de tratar la diferencia-de-proporciones como candidata a coeficiente y tratarla como **momento/patrón objetivo**. Esto reubica el problema en la ruta agregada, donde el enlace no hace falta. Umbral que revierte la decisión: si se insiste en interpretar β como efecto causal individual, entonces sí hace falta un modelo de enlace/medición explícito, que habría que estimar o declarar y someter a análisis de sensibilidad al enlace.

2. **Producir objetivos con inferencia design-based (inmediato).** Estimar proporciones/diferencias con `svydesign`/`svyglm` (linearización de Taylor o pesos replicados) para propagar la estructura muestral a la incertidumbre de los objetivos (Binder; Lumley & Scott). Estos errores estándar alimentarán las varianzas de observación en HM/KOH.

3. **Construir la población inicial por reponderación (corto plazo).** IPF/GREGWT sobre la microdata de la encuesta para cuadrar márgenes poblacionales; enterizar pesos (TRS) antes de instanciar agentes (Lovelace et al.; Tanton et al.).

4. **Elegir la ruta de calibración de β según nº de parámetros y coste del modelo:**
   - Pocos β (≤ ~5) y modelo barato → SMM/inferencia indirecta con corrección sándwich por mala especificación (Dridi–Guay–Renault) y análisis de sensibilidad a los momentos.
   - Modelo costoso o muchos β → history matching con emulador GP y bases calibración-óptimas (Vernon–Goldstein–Bower; Salter et al.), reportando la región NROY (conjunto de β compatibles) en vez de un punto.
   - Si se quiere posterior sobre β → KOH o ABC, **pero** con priors informativos/constraints sobre la discrepancia (para mitigar no-identificabilidad) y diagnósticos de mala especificación (Frazier et al.).
   - Si hay varios patrones agregados → POM como filtrado inverso multi-patrón (Grimm et al.).

5. **Diagnosticar identificabilidad ANTES de reportar (corto plazo).** Análisis de identificabilidad estructural y práctica; reportar la variedad de β equivalentes y la sensibilidad de la salida a combinaciones de β (sloppiness). Umbral: si los β objetivo resultan prácticamente no identificables con los patrones disponibles, fijar los no identificables por juicio experto (documentado) y calibrar sólo el subconjunto identificable.

6. **Interpretación (permanente).** Comunicar que los β calibrados contra salidas agregadas son parámetros de ajuste condicionados a la estructura del ABM y a la discrepancia; no equivalen a efectos causales individuales salvo bajo supuestos de enlace fuertes y verificables.

## Caveats
- Varias fuentes de crítica son preprints/working papers y se marcan como no revisados por pares en su forma citada: Prangle (arXiv:1512.05633) y la versión arXiv:1902.05938 de Platt (la versión revisada por pares es J. Econ. Dyn. Control 2020). Los resultados principales de Tuo & Wu sí están en Annals of Statistics (2015, revisado); su nota "Prediction based on the KOH model" (arXiv:1703.01326) no lo está.
- El problema exacto "diferencia-de-proporciones → coeficiente de índice latente" no aparece tratado como un único problema nombrado en un solo artículo primario; es la unión de dos literaturas (estimación design-based de encuestas + identificación hasta escala de índices latentes). La recomendación se apoya en ambas conjuntamente.
- Algunos DOIs de fuentes clásicas (Binder 1983: 10.2307/1402588; Godambe–Thompson 1986: 10.2307/1403139; Manski 1985: 10.1016/0304-4076(85)90009-0; Deville–Särndal–Sautory 1993: 10.1080/01621459.1993.10476369) fueron inferidos de metadatos de volumen/página estándar y conviene verificarlos antes de publicar. El DOI de Vernon–Goldstein–Bower (2010, Bayesian Analysis, 10.1214/10-BA524) también conviene confirmarlo.
- La afirmación de fragmentación entre comunidades (Hallazgo 21) es una observación bibliométrica/terminológica, no un teorema; se ofrece explícitamente como información sobre el estado del subcampo, según lo pedido.
- La superioridad "bayesiano > frecuentista" (Hallazgo 22) se demostró en ABM económicos de escala pequeña-media; su extrapolación a un ABM psicosocial grande es una conjetura, no un resultado establecido.
- La referencia clásica de Craig, Goldstein, Seheult & Smith (1997) es un capítulo en Lecture Notes in Statistics (Springer) sin DOI estándar de artículo; se cita por título y serie.