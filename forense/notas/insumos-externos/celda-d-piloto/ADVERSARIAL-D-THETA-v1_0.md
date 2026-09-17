<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO EXTERNO tipo 3 — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Astra (asistente ChatGPT/Codex), rol solicitado por dirección
> - **Fecha del documento:** 16/sep/2026 · **fecha de archivo:** 2026-09-16.
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `850f9cefe4334acd679d7eaa38eceafa4da19d903bd38997f448534b32d082e7`
>   — coincide con el prefijo `850f9cefe4334acd…` que el encargo declara.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1-TRES-DISENOS-UN-CAREO.md`, P0 (segunda entrega, tras el PARO de A.3).
> - **Nota:** Adversarial de Astra sobre D-θ v1.0, que el brief externo de este encargo lista como adjunto «tu propio adversarial — para que no te repitas». Es el documento cuyos hallazgos `H1`–`H10` produjeron la v1.1 de dirección que se archiva junto a él. Astra declaró su sha256 local en su propio retorno (`850f9cefe4334acd679d7eaa38eceafa4da19d903bd38997f448534b32d082e7`) y **coincide byte a byte** con el del archivo que mesa cargó: es la primera vez en este acto que un sha declarado por el externo se coteja contra el archivo real, y cuadra.

---

# Revisión adversarial de D-θ v1.0

**Fecha:** 16 de septiembre de 2026.  
**Objeto:** `D-THETA-DOCUMENTO-PARA-ADVERSARIAL-v1_0.md`.  
**Dictamen:** **no aprobar §6 como está; aprobar una habilitación experimental acotada tras corregir el objeto matemático y el contrato de salida.** La revisión no recomienda esperar a identificar causalmente todo el motor.

## 1. Qué cambia la decisión

El documento acierta al declarar que el motor matricial todavía no produce estimaciones y que una asociación no acredita un efecto causal. Sin embargo, construye la elección A/B/C sobre una mezcla de objetos distintos: matriz de coeficientes, predictor de persistencia, distribuciones de atributos, probabilidades de conducta y efectos causales. Añadir intervalos no resuelve esa mezcla.

Hay tres correcciones anteriores a la elección entre puntos y bandas:

1. **El B del motor no es el B de persistencia del duelo.** El código define `g(x)=B·θ(x)` con una matriz de coeficientes. El predictor de persistencia es una referencia externa.
2. **Cargar θ no desbloquea por sí solo el cálculo.** Con los datos vigentes, `matriz.g()` lanza `SinMagnitud` por `G5 × familismo_obligacion` antes de consultar θ. Lo reproduje.
3. **La deuda de dispersión se está dimensionando con el esquema anterior.** El canon v4.0 reformula los 90 parámetros de perfiles como 15 distribuciones condicionales. El diseño E1 conserva el diagnóstico antiguo. Esto cambia el alcance de la primera corrida.

La opción útil es autorizar un piloto descriptivo o predictivo de una ruta completa, con incertidumbre adecuada a su estimando, y reservar la lectura causal para preguntas que efectivamente la necesiten.

## 2. Alcance y comprobaciones

Leí el documento completo y contrasté las premisas materiales con `origin/main`, obtenido mediante `git fetch`, en **`1353616309dde6cd976a7fefe4305d5e4b6c163a`**, merge de #817. No cambié código, decisiones ni PR.

Los ZIP de agosto se inspeccionaron como contexto histórico. En particular, `espejo/modelo-decision-v3_2.md` sí contiene la deuda de 90 parámetros de dispersión; no sustituye al v4.0 actual. El ZIP de sesión contiene encargos y un LEEME, no una implementación alternativa del motor vigente.

Comprobaciones dirigidas realizadas:

- Lectura de `theta.py`, `motor.py`, `matriz.py`, `procedencia.yaml`, el diseño E1, la firma F-18 y los apartados pertinentes del modelo canónico.
- Verificación de que los tres módulos ejecutados son idénticos entre el checkout local y el `main` consultado; carga de `procedencia.yaml` extraído de ese `main` para la reproducción del bloqueo.
- Lectura de los insumos de `CALC-TRIADA-0002`: incluye `IN-F5C-SNAPSHOT-M`. La distinción entre emisor y motor matricial se sostiene.
- Recálculo desde `celdas.tsv`: MAE de M **4.986673 pp**, L_SOLO **3.957362 pp**, L_CORPUS **3.889026 pp**; fracción cívica del error de M **68.8759%**. Con igual peso por las **cinco familias**: M **5.028459**, L_SOLO **7.315042**, L_CORPUS **7.529374**. Estas cuentas del documento se sostienen.
- Lectura dirigida de fuentes primarias metodológicas. Se pudo consultar texto de Cinelli–Hazlett, Li–O’Donoghue y Vernon et al. (2014). Otras consultas sólo devolvieron resúmenes o tuvieron bloqueos; no se presentan como lecturas completas.

No repetí microdatos ni los experimentos F5/F6. No recertifiqué los contadores generales: no deciden esta revisión.

## 3. Hallazgos materiales

### H1 · Bloqueante: la premisa identifica dos B diferentes

**Dónde:** §1 y las consecuencias operativas de §§3, 6 y 7.

El documento define B como persistencia y lo introduce en `g(B,Θ(x))`. En cambio, [`milpa/src/matriz.py`](https://github.com/Josanoforo/Modelado-Mexicano/blob/1353616309dde6cd976a7fefe4305d5e4b6c163a/milpa/src/matriz.py) define B como matriz por `(generador, coeficiente)`, con valores asignados y algunos overrides medidos. `g()` calcula sumas de productos entre esos coeficientes y valores de θ. No incorpora la última ola de una serie.

El [`pre-registro de B-piso`](https://github.com/Josanoforo/Modelado-Mexicano/blob/1353616309dde6cd976a7fefe4305d5e4b6c163a/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md) establece, además, que la persistencia se consume en la comparación y que sus cifras no se adoptan al motor.

**Consecuencia:** no se está aprobando sólo una política de incertidumbre. El documento podría inducir una arquitectura diferente y confundir un coeficiente de B con una condicional de θ. Una etiqueta de escala no arregla una asignación a la ranura equivocada.

**Corrección mínima:** distinguir `B_matriz`, `b_persistencia`, `θ_k(x)` y la salida de conducta. Para el piloto, escribir la ruta exacta: cantidad observada → parámetro que representa → transformación → función consumidora → salida evaluable. Si se quisiera usar persistencia como intercepto o ancla del nuevo predictor, sería una propuesta explícita de modelo, no una descripción del existente.

### H2 · Bloqueante: el diagnóstico de ejecutabilidad omite un bloqueo anterior a θ

**Dónde:** §1, §3 y §7.4.

Reproducción con el B vigente y un sustituto de θ que devolvería `0.5` para cualquier nombre:

```text
SinMagnitud: G5 × familismo_obligacion
signo negativo o no monotónico — SIN MAGNITUD
llamadas a theta.valor: 0
```

El bucle inicial de `matriz.g()` comprueba toda B y detiene la ejecución antes de multiplicar. Por tanto, **ni una θ completamente cargada haría computable esta función con la matriz completa actual**.

Además, [`motor.py`](https://github.com/Josanoforo/Modelado-Mexicano/blob/1353616309dde6cd976a7fefe4305d5e4b6c163a/milpa/src/motor.py) produce veredictos de estado; cargar θ no implementa automáticamente la transformación de generadores a probabilidades ni su evaluación.

**Corrección mínima:** el primer encargo debe tener una ruta completa ejecutable. Si se propone aislar un generador sin dependencias faltantes, hay que especificarlo y autorizarlo; el código actual no ofrece ese aislamiento por el mero hecho de pedir una celda. No rellenar el coeficiente con cero ni afirmar que el motor completo quedó habilitado.

### H3 · Material: E1 arrastra deuda histórica y una afirmación demasiado fuerte sobre escalas

**Dónde:** §§2.1–2.2, 5.3, 6.2 y 8.8.

El [`modelo canónico v4.0`](https://github.com/Josanoforo/Modelado-Mexicano/blob/1353616309dde6cd976a7fefe4305d5e4b6c163a/canon/modelo-decision-v4_0.md), §§1.1 y 6, dice explícitamente que la deuda pasó de 90 parámetros de perfiles a **15 familias de distribución sin declarar**. No desaparece; cambia de objeto. E1 vuelve a condicionar trabajo a listar los 90 parámetros antiguos.

También existe una enmienda de ADR-220 en §2 que declara un enlace identidad para pares específicos. Eso no demuestra que el enlace sea científicamente suficiente ni que todas las escalas estén resueltas, pero contradice la afirmación absoluta de que el canon no declara escala para ninguna salida.

**Corrección mínima:** resolver estas dos discrepancias leyendo las enmiendas ya existentes, sin abrir un recenso general. Separar inventario histórico de perfiles, condicionales vigentes y dependencias realmente consumidas por el piloto. No exigir 90 calibraciones por una premisa superada ni tratar todos los pares como si carecieran de enlace declarado.

### H4 · Bloqueante conceptual: falta fijar qué se pretende estimar

**Dónde:** pregunta D-θ de §3 y comparación de opciones en §5.

La falta de identificación **causal** no vuelve ilegítima una prevalencia descriptiva ni impide por sí sola construir un predictor. Sí impide interpretar automáticamente una asociación como respuesta a una intervención.

| Producto | Pregunta | Evidencia necesaria |
|---|---|---|
| Descripción | ¿Qué proporción presenta Y en esta población y periodo? | Universo, medición, muestreo, selección y precisión. |
| Predicción | ¿Qué Y esperamos en una población o periodo objetivo? | Predictores disponibles al corte, soporte y evaluación fuera del desarrollo. |
| Intervención | ¿Cómo cambiaría Y si modificamos A? | Estimando causal y supuestos de identificación, o cotas de sensibilidad justificadas. |
| Simulación de agentes | ¿Qué trayectorias genera una población sintética? | Distribuciones conjuntas/condicionales y dependencias pertinentes; alcance de la validación. |

**Consecuencia:** la opción B impone una barrera causal a productos que pueden no necesitarla; la opción C promete compensar esa barrera con bandas sin especificar el efecto causal al que corresponderían.

**Corrección mínima:** decidir primero el producto y su estimando. Admitir puntos con incertidumbre para descripción/predicción, cuando proceda; reservar la lectura causal. La validación predictiva tampoco identifica un mecanismo causal.

### H5 · Bloqueante: C es una lista de métodos, no un intervalo definido

**Dónde:** §§3 y 5.3.

El documento trata como intercambiables objetos diferentes:

- IC por error de muestreo de un estimador.
- Distribución de heterogeneidad entre personas de la misma celda.
- Intervalo predictivo para un resultado futuro.
- Conjunto identificado bajo restricciones explícitas.
- Rango de escenarios al variar supuestos.
- Discrepancia entre simulador y realidad.

No se obtiene una cobertura conocida sumando sus anchuras. Tampoco una banda elegida antes de abrir resultados adquiere validez por haber sido predeclarada.

El **E-value** mide una fuerza de confusión en escala de razón de riesgos; no constituye una receta universal para ensanchar cualquier IC de p o de un índice. El trabajo de [VanderWeele y Ding](https://pubmed.ncbi.nlm.nih.gov/28693043/) describe ese objeto específico. [Cinelli y Hazlett](https://carloscinelli.com/files/Cinelli%20and%20Hazlett%20(2020)%20-%20Making%20Sense%20of%20Sensitivity.pdf) sí desarrollan ajustes de estimaciones e intervalos dentro de un marco de regresión y parámetros de sensibilidad definidos; no basta con añadir su robustness value a una salida del motor.

**Corrección mínima:** escoger un solo método aplicable al piloto y declarar qué contiene el intervalo, en qué escala, bajo qué supuestos y con qué cobertura, si alguna. Si sólo es envolvente de escenarios, llamarla así. Preservar las dependencias entre parámetros; intervalos marginales separados no definen por sí solos una distribución conjunta.

### H6 · Material: «ambos signos → NO-EMITE» decide sobre la cantidad equivocada

**Dónde:** §§3, 5.3 y 6.3.

Una probabilidad vive en `[0,1]`: no tiene dos signos. Un intervalo `[0.10,0.90]` pasaría ese filtro aunque fuera inútil para decidir respecto de un umbral de 0.50. Por otra parte, un contraste `[-0.01,0.01]` puede ser informativo sobre la pequeñez del efecto aunque no determine su dirección.

Si C calcula una cota válida y luego la suprime por cruzar cero, desperdicia precisamente la información que pretendía conservar.

**Corrección mínima:** separar **emitir la estimación** de **activar una decisión automática**. Emitir intervalos válidos que cruzan cero; abstenerse de afirmar dirección. Para un tier, comparar el conjunto de salidas con los umbrales del consumidor: si todos los valores conducen al mismo tier, la decisión es robusta bajo esos supuestos; si no, informar ambigüedad. La regla exacta debe responder a la pérdida o utilidad del consumidor.

Fuera de soporte puede corresponder abstenerse de predecir o emitir sólo un escenario explícito. No es la misma razón que incertidumbre sobre un signo.

### H7 · Material: el texto vuelve a introducir fuga de validación

**Dónde:** history matching en §5.3; condiciones de §6.2; nueva frase para el informe.

Hay tres problemas:

1. **Descartar θ con datos retenidos usa esos datos para calibrar/seleccionar.** Después no son una evaluación final independiente de los θ sobrevivientes. [Vernon et al.](https://arxiv.org/pdf/1405.4976) describen regiones no descartadas por implausibilidad; esa región no equivale automáticamente a un IC ni valida causalidad.
2. **U3 ya fue observada y motivó decisiones de diseño.** Puede servir como diagnóstico y referencia histórica; no debe presentarse como un holdout fresco para esta nueva elección. Varias celdas son olas de una misma familia y no aportan automáticamente independencia entre familias.
3. **La comparación F5 evaluó el emisor**, no el motor matricial que se quiere construir. No se transfiere su evaluación a otro ejecutable.

**Corrección mínima:** usar datos de desarrollo para calibración/history matching y una partición no utilizada para selección para la evaluación final; o un diseño de validación anidada adecuado si es viable. Si hoy falta ese panel, el piloto puede seguir como diagnóstico de factibilidad, con valor predictivo añadido pendiente.

La frase propuesta «estimador [...] validado donde hay piso» no está autorizada por la evidencia. Tener un baseline no es superar una evaluación. Mantener **«candidato con incertidumbre declarada; valor predictivo añadido pendiente de evaluación»** hasta obtenerla.

### H8 · Material: inversión de signo no demuestra interacción

**Dónde:** edge case 19, §5.3 y umbral del 10% de §6.3.

Contraejemplo construido para esta revisión, sin datos del programa:

| Estrato Z | P(Y=1\|X=0,Z) | P(Y=1\|X=1,Z) | Diferencia |
|---|---:|---:|---:|
| 0 | 0.10 | 0.20 | +0.10 |
| 1 | 0.80 | 0.90 | +0.10 |

La media condicional es aditiva: `0.10 + 0.10X + 0.70Z`; no hay interacción X×Z en esa escala. Si `P(Z=1|X=1)=0.10` y `P(Z=1|X=0)=0.90`, las medias marginales son **0.27 frente a 0.73**: diferencia **−0.46**. Hay inversión sin interacción.

**Consecuencia:** Sobol no es una cura de ese diagnóstico ni demuestra qué ajuste causal corresponde. El signo marginal tampoco es necesariamente el signo «correcto» que debería sobrevivir al condicionar.

**Corrección mínima:** retirar «firma de una interacción» y el umbral universal >~10%. Evaluar si el contraste estima la misma cantidad y si su uso cambia una decisión. No convertir cada cambio de signo en veto, ni esperar a un porcentaje arbitrario para examinar uno que afecte una decisión importante. Sensibilidad global cuando la ruta y sus interacciones lo requieran, no como condición universal previa a cualquier carga.

### H9 · Material: etiquetas y dispersión marginal no resuelven incompatibilidades ni población sintética

**Dónde:** tabla de curas de §4.4; §6.2 y §6.4.

Escribir escala/universo no convierte un β en p, no corrige un ponderador incorrecto, no hace comparable un cuestionario rediseñado y no añade precisión a una celda pequeña. Hace visibles los problemas; la transformación, restricción o abstención debe resolver el uso.

Para agentes, una distribución marginal por atributo tampoco determina la conjunta. Ejemplo: dos atributos binarios con prevalencia 0.5 cada uno pueden tener coocurrencia entre **0 y 0.5**; suponer independencia fija 0.25 sin evidencia adicional. Una regla que requiere ambos atributos cambiaría sustancialmente.

Una prevalencia por celda puede sustentar sorteos sintéticos bajo supuestos explícitos, pero esos sorteos no identifican qué individuo real presenta el rasgo ni validan trayectorias conjuntas. Tampoco un IC sobre la media representa la dispersión de las personas.

**Corrección mínima:** distinguir la heterogeneidad exigida por ADR-28.d de la incertidumbre sobre parámetros. En un piloto de agentes, declarar las dependencias necesarias y su procedencia; si no se conocen, tratarlas como escenarios. Para un producto exclusivamente agregado, no cargarle automáticamente todas las dependencias de un simulador individual. Esa delimitación debe quedar explícita; no deroga ADR-28.d para el motor de agentes.

### H10 · Material: el benchmark no demuestra la recomendación universal

**Dónde:** síntesis de §4.2; §§5 y 6.2.

«Todas presentes como obligatorias en los comparables» no se deriva de una tabla que mezcla métodos, guías, modelos aritméticos y conductuales, con evidencia de resúmenes. Que un artículo no anuncie identificación en el resumen no prueba que carezca de argumento en el texto.

Hay una contradicción concreta: la prohibición general de alinear a agregados se atribuye a comparables que usan alineación. [Li y O’Donoghue (2014)](https://www.jasss.org/17/1/15.html) estudian seis métodos, describen su uso extendido y evalúan ventajas y limitaciones; no establecen una prohibición universal. **Ajustar con agregados de entrenamiento y evaluarse en otros datos no equivale a ajustar al árbitro de evaluación.** El programa puede prohibirlo por decisión propia; no debe presentar esa elección como consenso de las fuentes.

Asimismo, [OBR describe incertidumbre alrededor de una previsión central](https://obr.uk/box/presenting-uncertainty-in-our-forecasts/). Eso no respalda la oposición tajante «rangos, no puntos» ni una regla basada en identificación causal. Esta comprobación de OBR procede del extracto indexado; la apertura directa fue bloqueada.

**Corrección mínima:** conservar el benchmark como repertorio de métodos y retirar las afirmaciones universales. Verificar el método concreto que se adopte, sin exigir leer toda la bibliografía antes de un piloto. No se usa la afirmación no comprobada sobre CBO para este dictamen.

## 4. Respuestas a los nueve blancos de §8

| Blanco | Dictamen adversarial |
|---|---|
| 1 · ¿B-persistencia es circular? | **No por compartir serie.** Pronosticar una ola con la anterior es un baseline legítimo si la información estaba disponible al corte y el estimando es comparable. La estabilidad temporal puede explicar su buen desempeño; eso no lo invalida. Revisiones retrospectivas, uso del objetivo o filtros desiguales sí podrían contaminarlo. No he certificado todas las fechas de publicación. |
| 2 · ¿C es estado del arte? | Sus componentes tienen literatura; la combinación propuesta no es un procedimiento validado. Debe evaluarse como diseño propio, método por método. |
| 3 · ¿10% arbitrario? | Sí. Sustituir por impacto sobre el estimando y la decisión; no por otro porcentaje sin fundamento. |
| 4 · ¿Validación disjunta real? | No queda demostrada para el nuevo motor. U3 es evidencia ya expuesta; los datos usados para descartar θ son desarrollo. No presentar F6 pendiente como validación realizada. |
| 5 · ¿Consumidores de escalares? | Hay que especificar su comportamiento. No elegir el punto medio silenciosamente. Emitir incertidumbre y abstenerse de la decisión automática si cruza sus umbrales. |
| 6 · ¿Falacia ecológica inevitable? | Ninguna opción autoriza inferencia causal o individual desde un agregado. Simular individuos es posible con supuestos de distribución; validar agregados sólo acredita propiedades agregadas. |
| 7 · ¿Fuentes de resumen? | Insuficientes para obligaciones universales. Ya se contrastaron algunos textos centrales; no hace falta convertir el resto en otro proyecto bibliográfico. |
| 8 · ¿S2 convierte C en B? | La deuda sigue, pero su representación de 90 parámetros está superada en el canon. Dimensionar el piloto según las condicionales consumidas, sin afirmar que el motor completo queda cerrado. |
| 9 · ¿Emisor/motor se sostiene? | **Sí.** Código e insumos de F5 lo respaldan. Precisamente por eso F5 no valida ni refuta la capacidad del motor matricial futuro. |

Dos precisiones adicionales: «A es peor que B exactamente en las fallas 1, 2, 13 y 19» no está demostrado, sea B la opción de esperar o el baseline; y no disponer de identificación causal no vuelve experimental a un intervalo sólo por llamarlo sensibilidad.

## 5. Recomendación sustitutiva para decisión de mesa

**Propuesta; no firma ni modificación de la decisión vigente:**

> Se autoriza un piloto acotado de carga de Θ para un estimando descriptivo o predictivo nombrado, sobre una ruta completa y ejecutable. Se distinguen la matriz de coeficientes, la referencia de persistencia, las distribuciones condicionales y la salida final. La ausencia de identificación causal no impide el uso descriptivo o predictivo, pero impide atribuir efectos de intervención sin supuestos adicionales explícitos.
>
> Cada parámetro del piloto debe tener fuente, unidad, universo, escala, transformación y consumidor compatibles. La incertidumbre se representa con el método que corresponda; se distinguen IC, heterogeneidad, predicción y escenarios. No se exige una banda causal universal por el solo rótulo AUSENCIA_DECLARADA.
>
> Se pueden emitir estimaciones válidas aunque sus intervalos incluyan cero. La decisión automática se abstiene cuando los valores admitidos llevan a acciones diferentes bajo la regla del consumidor. Las limitaciones de soporte se declaran por separado.
>
> Los datos usados para ajustar o seleccionar parámetros no se presentan como validación final independiente. El piloto se compara con una referencia simple cuando sea construible bajo el mismo corte y estimando. Su resultado permanece experimental hasta superar la evaluación correspondiente.
>
> La dispersión y las dependencias se resuelven para las condicionales efectivamente consumidas. No se declara completado el motor de agentes ni cerrada la deuda general por ejecutar una ruta parcial.

Esto permite avanzar con **A acompañada de incertidumbre apropiada, C cuando exista una receta justificada y abstención limitada al uso que carezca de soporte**. No exige elegir una política idéntica para objetos estadísticos distintos.

## 6. Siguiente acción concreta

Un solo piloto, sin activar de entrada una calibración de todo el inventario:

1. **Elegir una salida y una ruta.** Identificar el parámetro que alimenta, el enlace, la función consumidora y sus dependencias. Resolver el bloqueo `SinMagnitud` mediante un alcance explícito o la decisión pendiente correspondiente; no mediante imputación.
2. **Fijar el producto.** Descripción, predicción o escenario. Definir población, periodo, eje ya homologado, unidad y criterio de comparación. Si no hay ninguna ruta compatible, entregar esa incompatibilidad nominal, no otro censo global.
3. **Congelar una receta suficiente.** Método de estimación, incertidumbre pertinente y tratamiento de dependencias. Conservar separados desarrollo y evaluación. No invocar E-value, Sobol ni history matching salvo que respondan a una necesidad concreta de esa ruta.
4. **Producir una salida consumible.** Estimación, intervalo o escenarios claramente tipados, referencia comparable si existe, y estado del consumidor: decisión estable, ambigua o fuera de soporte.
5. **Parar y decidir.** El resultado útil es saber si esa ruta calcula algo interpretable y si merece escalarse. Sin evaluación independiente, llamarlo factibilidad; con ella, informar desempeño y alcance. No actualizar el informe a «validado» por el mero éxito técnico.

La corrección del documento y la especificación breve del piloto pueden vivir en la misma entrega. Archivar dos investigaciones completas, reclasificar los veinte casos y abrir varias capas de gobernanza no debe preceder obligatoriamente a ese resultado.

**¿Quedó el proyecto más cerca de producir una explicación, medición, decisión o modelo mejor? Sí:** esta revisión identifica un bloqueo ejecutable omitido, corrige el objeto de la carga y propone una vía para obtener una primera salida interpretable sin prometer causalidad ni validación que todavía no existen.
