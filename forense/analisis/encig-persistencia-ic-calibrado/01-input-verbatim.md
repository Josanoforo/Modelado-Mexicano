# ASTRA-3 · U2 · intervalo de persistencia ENCIG con variación temporal

**Lanzamiento: AHORA, sesión nueva sin exposición a ENCIG2025.** Rama `codex/astra3-encig-persistencia-1`; worktree `/home/pc0/mm-astra3-encig-persistencia-1`. No usar la sesión autora ASTRA-ENCIG que ya leyó marginales2025. Este es un producto de calibración histórica, sin piloto nuevo.

## Objetivo y premisa corregida

Medir τ² por desenlace×eje, el ancho que añade al piso y su cobertura retrospectiva2021→2023; entregar una regla reutilizable con datos2017/2019/2021/2023. No adoptar ni modificar el piloto5.

La misión afirma que #972 atribuyó el fallo a un salto de instrumento. LEÍDO por Astra: su ADR `ADR-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01` concluye SALTO-SIN-EXPLICAR y NO atribuye el salto a cambio de instrumento. Esa lectura de dirección incluye un resumen referido a2025: no lo uses como dato de calibración ni abras sus resultados. La sesión nueva decide comparabilidad exclusivamente por documentación de2017–2023. No elimina un par por presentar un cambio grande.

## Definiciones antes de resultados

1. Deriva la rejilla de los pisos ENCIG2023 y sus specs/tablas de identidad, sin leer valores de evaluación. Mismos desenlaces, ejes, unidad TRÁMITE y universo del consumidor. Verifica la premisa «oro2023»: un CALC llamado ARBITRO puede contener R2025. No abrirlo por el nombre. Para2023 emplea `CALC-PISOS-ENCIG2023-EJES-0002` si su spec confirma exactamente ese objeto; jamás `CALC-ARBITRO-MARGINALES-ENCIG2025-*`.
2. Comparabilidad por texto/pases y códigos: excluir del pooling primario únicamente pares con cambio de instrumento demostrado documentalmente. Congelar tabla y motivos antes de valores. Si no hay tal cambio, incluir el par aunque arroje salto grande. No intentar atribuir retrospectivamente el cambio a la pandemia o a psicología como conclusión causal.
3. Grupo g = desenlace×eje. No promediar entre desenlaces, unidades o periodicidades diferentes. Para cada transición bienal comparable y celda, Δ=logit(p_fin)−logit(p_inicio). Fronteras0/1 quedan SIN-DEFINIR; no recorte seleccionado después.
4. Regla heredada explícitamente de ENIF: τ²_g = media de Δ², sin centrar ni descontar ruido muestral; ponderar por igual transiciones y dentro de cada transición sus celdas elegibles. Fijar antes el conjunto comparable para evitar composición oculta. Rotular como segundo momento empírico del cambio observado, con componente muestral; no varianza pura del proceso identificada.
5. IC alrededor del piso: expit(logit(p_piso) ± 1.959964 sqrt(ee_logit_piso² + τ²_g)); ee_logit=(logit(HI)−logit(LO))/(2×1.959964). Declarar aproximación, posible conservadurismo y casos NO-CALIBRABLE. No usar el éxito de cobertura para variar el multiplicador.

## Separación entre evaluación histórica y parámetro final

Para evaluar2021→2023, calcula τ² SOLO con2017→2019 y2019→2021, usando los pares documentalmente comparables. Congela regla y pronóstico retrospectivo desde2021 antes de consultar las cantidades2023 de evaluación. Luego computa cobertura por celda frente al punto2023. Esta evaluación sigue rotulada RETROSPECTIVA, no se presenta como nuevo holdout ciego del programa.

Después, con la misma regla, emite τ² FINAL usando también2021→2023 para una futura aplicación alrededor del piso2023. Usa IDs distintos para τ² entrenamiento y τ² final. La cobertura2021→2023 NO valida ese ajuste final que ya usó2023. No abrir2025 ni medir cobertura contra esa ola. Si no hay transiciones comparables pre2023, el parámetro final puede ser construible, pero la evaluación temporal será NO-EVALUABLE con causa: no usar el mismo par para entrenar y atribuir validación.

La spec humana y spec.yaml deben congelar AMBOS pasos y la secuencia de lectura antes de cualquier valor. No esperar firma intermedia entre ellos.

## Incertidumbre y producto

Reusar diseño muestral y lectores comprobados de ENCIG, con réplicas comunes por ola y dominios del consumidor. Congela bootstrap/semilla/recuento y tolerancia. Documenta dependencias entre cambios consecutivos por compartir una ola; no multiplicar artificialmente el número de choques.

Entrega N elegibles/cubiertas/no calibrables, indicador por celda, cobertura global y por desenlace/eje, IC binomial Wilson de referencia y resumen por grupos. Las celdas solapadas no son ensayos Bernoulli independientes. Si se hereda el Wilson con n efectivo=grupos de la plantilla ENIF, rotularlo aproximación heurística; no llamarlo inferencia por conglomerados garantizada. Añadir, cuando haya grupos suficientes, bootstrap de grupos completos para la proporción, declarando que compartir muestra limita su independencia. Con pocos grupos, informar incertidumbre insuficientemente determinada en vez de fabricar precisión.

Anchos en pp, medianas/rango y ancho por celda; comparación con los35pp ENIF únicamente como escala de amplitud, no igualdad de instrumentos o calidad. Calcular descriptivamente el ancho mínimo simétrico alrededor de cada piso que alcanzaría el punto2023; no usarlo para recalibrar la regla. No inventar un umbral de utilidad firmado: entregar cuánto discrimina el intervalo, saturación cerca de[0,1] y recomendación fundada de uso/no uso.

## Datos y perímetro

Ids a resolver en manifiesto: `encig2017_csv`, `encig2019_csv`, `encig2021_csv` o `encig_2021_encig21_base_datos_csv`, `encig23_base_datos_csv`. Verifica formato, universo y hash, no asumir equivalencia entre los dos2021. Ya hay cuestionarios/FD históricos registrados; corpus primero. No extender a2011–2015 por inercia.

Escritura: `forense/prereg-caja/ENCIG-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md` y sidecar; `data/corrida0/CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001/`; `tools/astra/encig/ic_calibrado/`; `tests/test_astra3_encig_ic_calibrado.py`; `forense/analisis/encig-persistencia-ic-calibrado/`; replay append. No leer resultados2025 de ASTRA-1, árbitro, piloto3, tabulados o comunicados.

Hecho = CALC reproducible, τ²/ancho/evaluación histórica con el alcance anterior, comparabilidad y recibo con propuesta de uso para mesa. Si solo admite intervalos inútilmente amplios o no admite calibración, ése es el resultado; no una búsqueda de variantes hasta cubrir.

## Reglas de ejecución de esta tanda

Adjunta y lee íntegra `MISION-ASTRA-3-mide-lo-que-falta.md`. Base verificada por Astra `523f3c6d8ddc3d11594efe33f97a1e9a89bab228`; `git fetch origin` al abrir, declara ruta/HEAD/status y comprueba por objeto que tu unidad no esté ya ejecutándose. Una sesión escritora por unidad y un PR propio. No tomar el worktree de ASTRA-2 ni detener esa misión.

Usa primero manifiesto, catálogos, documentación y corpus compartido existente. Los ids abreviados de la misión no son necesariamente ids exactos: deriva id/ruta/hash del manifiesto y de las specs vigentes; no crees duplicados. Si falta un insumo concreto, búsqueda primaria y adquisición por carril adq autorizado, antes de consumirlo; no un inventario general. La ausencia de data/raw en un worktree no prueba ausencia de bytes.

Entorno CAJA para microdato. Antes de lectura de valores: cuestionarios/FD, decisiones de método, spec humana + sidecar y spec.yaml con inputs/hash, medidor completo y commit de freeze. Incluye «el primer resultado que produzca este procedimiento es el que se reporta». Hash y presencia del payload pueden verificarse sin tabularlo. Una lectura previa de resultados debe declararse; un git log por sí solo no prueba que nadie abrió bytes. Las sesiones que ya vieron una ola no vuelven a declararse ciegas.

Lee las reservas aplicables, sin abrir los resultados que protegen. No ENCIG2025, ENVIPE2026, ENCO2025/2026 ni ENIGH2024; ENVIPE2025 queda fuera de estas tareas. ENIF2024 se permite solo en el alcance consumido expresamente autorizado a cada unidad. No extrapolar esa autorización a crédito o variables nuevas.

El proceso continúa hasta cerrar: preparación documental → freeze → preflight → run → verify → asiento propio append en forense/replay-evidencia.tsv → nota y recibo → commit/push/PR. No esperes otra tanda entre fases ya autorizadas. No modificar registro ni correr `registro --escribe`; no tocar CI/check.py/verify.yml, tablero, marcador, celdas-D, milpa ni sellos ajenos. Tests dirigidos propios, sin instrumentar CI. Un defecto fuera de perímetro se declara en una línea y no absorbe el encargo.

Etiquetas completas: generacion GEN2, cuenta_gen2 SI para las corridas de esta misión, adopta NO y origen_numerico verdadero conforme al contrato (MICRODATO si se estima de microdato; cálculo sobre RESULT sellados, rotulado según el esquema vigente sin fingir nueva apertura). Tipo de evidencia e incertidumbre explícitos. Una estimación no construible es nula con causa, nunca cero.

No dejar la entrega en una spec si es ejecutable. Reutiliza herramientas selladas por ruta/hash sin modificarlas, prueba únicamente transformaciones y fallos materiales propios. Replay REPRODUCE y tolerancia fijada antes. Corrige bugs preservando primera emisión y exposición; no seleccionar variantes por resultado.

Cada nota/recibo usa EJECUTADO/LEÍDO/REPORTADO según la evidencia, cifras con comando, escala, unidad, universo, generación, hashes/commits, límites y lo no corrido con razón. `## NO-CORRIDO / RESERVAS` («Ninguno.» si aplica) y `## CONSUMIDO` con PR. Guarda misión e input verbatim en tu carpeta de análisis propia. Publicar rama/PR está autorizado; fusionar o adoptar queda en mesa.

