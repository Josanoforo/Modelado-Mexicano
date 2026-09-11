# Benchmark web de las cuatro decisiones GEN2

Fecha: 11 de septiembre de 2026. Objetos: DIN/FP-371, S6/FP-372, complemento ENVIPE/NC-0085 y tasas de corrupción/NC-0107. Es investigación y propuesta para mesa, **no firma ni modificación del repo**.

Se contrastaron las preguntas exactas del corte `67f0b6ef96436c560ddfec116d32575da5a865a1` con nueve fuentes primarias. Se reutilizaron los benchmarks D11/D16 ya archivados, ampliando su aplicación con los resultados de #689, #693, #695 y #702. No se repitieron cálculos con microdatos ni se hizo otra revisión de merges.

## 1. Resultado para decidir

| Decisión | Qué respalda el benchmark | Recomendación revisada | Cambio respecto de la bandeja anterior |
|---|---|---|---|
| DIN | La falta de diseño para la varianza no elimina automáticamente el punto ponderado. El hogar no acredita la UPM. | **A precisada:** punto descriptivo; aproximaciones sólo en sensibilidad; buscar una vía oficial de varianza. | A y B comparten la restricción inferencial: difieren principalmente en mostrar u omitir las sensibilidades. |
| S6 | La agrupación por localidad no queda validada por obtener un join correcto ni por repetir el bootstrap. | **A precisada:** puntos y asociaciones descriptivas; ninguna promoción basada sólo en IC aproximados. | Un IC que incluye cero tampoco prueba ausencia de asociación. Tres clases socioeconómicas no significan que el diseño completo tenga sólo tres estratos. |
| Complemento ENVIPE | El complemento es un estimador válido bajo la misma partición, población y ponderación. | **A condicionada al consumo correcto:** residual del recorte a nivel persona, dependiente del padre. | «Ningún delito elegible en el grupo padre» no equivale a «algún delito con otra razón». |
| Corrupción | La prevalencia entre personas, el conteo anual por tipo de trámite y la probabilidad por evento/canal son objetos distintos. | **A reforzada:** retirar expectativa de adopción de las dos tasas antiguas; revisar r2 como proxy/contexto, sin atribuirle una probabilidad por evento no identificada. | **No basta conservar r2 tal cual con un filtro de dominio.** Recomiendo separar su uso descriptivo de una calibración empírica por evento. |

Las recomendaciones de uso son inferencias de este benchmark aplicadas al proyecto. Ninguna institución citada evaluó el motor ni certificó sus cifras.

## 2. Referencias comparadas y alcance de lectura

| Fuente primaria | Parte consultada y aporte específico |
|---|---|
| [ENNViH, FAQ](https://ennvih-mxfls.org/faq.html) | Definición de folio, clases de tamaño de localidad y respuesta sobre publicación de UPM. |
| [INEGI, diseño ENNViH-1, 2004](https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf) | §§4–7, cuadro 1 y §10: selección, 180 UPM y método de precisión. |
| [CDC/NHANES, estimación de varianza](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx) | Pesos/diseño, unidades enmascaradas, dominios y variación del efecto de diseño. |
| [Parker et al., NCHS Series 2 n.º 175](https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf) | Estándares de proporciones, especialmente «Complementary Proportions», página impresa 4; revisión del informe hasta 2021. |
| [Park y Lee, Survey Methodology 30(2), 2004, pp. 183–193](https://www150.statcan.gc.ca/n1/pub/12-001-x/2004002/article/7751-eng.pdf) | §§1–2 y conclusión: el DEFF depende del estimador y de la variable; no se traslada universalmente. No se reprodujeron sus demostraciones completas. |
| [ASA, comunicado de principios de 2016](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf) | Los seis principios y su alcance: una decisión científica no depende exclusivamente de cruzar un umbral. |
| [ONU/UNODC, metadatos ODS 16.5.1](https://unstats.un.org/sdgs/metadata/files/Metadata-16-05-01.pdf) | Definición, población expuesta y experiencia directa, versión fechada 29/jul/2024. |
| [INEGI, cuestionario ENCIG 2025](https://www.inegi.org.mx/contenidos/programas/encig/2025/doc/encig25_cuestionario.pdf) | Secciones VII–VIII: canal, últimos eventos y conteo de experiencias de corrupción. |
| [INEGI, módulo ENVIPE 2025](https://www.inegi.org.mx/contenidos/programas/envipe/2025/doc/cuest_modulo_envipe2025.pdf) | Pregunta 1.23 y catálogo de razones, página PDF 4. |

Es un benchmark dirigido, no una revisión sistemática exhaustiva. El manual UNODC de 2018 no se recuperó íntegro en esta consulta; no se usa como respaldo nuevo. Tampoco se atribuyen al texto completo de Lumley (2004) conclusiones obtenidas sólo de su ficha editorial. Las cifras del proyecto proceden de los recibos indicados, no de una reproducción independiente hecha aquí.

## 3. DIN: conservar el punto sin inventar precisión

**Problema en el repo.** DIN-M-01 publica un punto `0.15558094338412926`. El IC de v4 procede de estrato constante y agrupación por folio. El recibo de #693 comprobó el enlace individual y el ponderador del libro; no encontró un diseño público ejecutable. [Nota DIN del corte revisado](https://github.com/Josanoforo/Modelado-Mexicano/blob/67f0b6ef96436c560ddfec116d32575da5a865a1/forense/notas/2026-09-10-GEN2-ADQUISICION-DIRIGIDA-DIN.md).

**Benchmark.** ENNViH distingue el identificador del hogar de la información de UPM, cuya publicación restringe por confidencialidad. NHANES muestra una alternativa institucional: variables de varianza enmascaradas creadas por el productor; no son un identificador arbitrario elegido por el analista. [FAQ ENNViH](https://ennvih-mxfls.org/faq.html), [tutorial NHANES](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx).

**Aplicación propuesta.** Mantener 15.56% como estimación puntual descriptiva de su población, variable y periodo. No tratarlo como certeza individual ni extenderlo a toda decisión de crédito. Registrar la incertidumbre de diseño como no acreditada, nunca como cero. Si el motor necesita explorar consecuencias, usar escenarios explícitos; no sortear una distribución paramétrica ajustada al IC aproximado presentándola como incertidumbre medida.

| Ruta | Qué la habilita | Uso defendible aquí |
|---|---|---|
| Diseño oficial o variables enmascaradas validadas | Correspondencia de ola, libro, población y estimador | Inferencia de diseño según el método documentado. |
| Réplicas oficiales o servicio de varianza | Réplicas con método/escala/grados de libertad, o respuesta oficial para el estimando exacto | Sucesor inferencial sin pedir geografía identificable. |
| Modelo inferencial alternativo explícito | Supuestos identificados y validación propia | Posible línea futura; no convierte la receta histórica en diseño oficial. |
| Recetas folio/SRS disponibles | Supuestos conocidos, sin garantía de cobertura | Sensibilidad exploratoria, separada del resultado principal. |

**Casos límite.** Un bootstrap estable sólo demuestra estabilidad bajo su receta. El tamaño bruto no recupera las unidades de selección faltantes. Las réplicas del LLM no aumentan el tamaño de la encuesta. Una sensibilidad cuyo rango no cambia la salida del motor muestra robustez dentro de esos escenarios; no demuestra que cubra la verdad.

**Por qué no propongo otro multiplicador automático.** El diseño ENNViH menciona DEFF 6.010 para planificar una muestra usando migración como variable de referencia. No es el DEFF observado de DIN. Park y Lee explican por qué el efecto de diseño depende de la variable, el estimador y su relación con los pesos. Aplicar 6.010 a DIN por ser la misma encuesta sería una transferencia no demostrada. [Diseño ENNViH, §6](https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf), [Park y Lee, §2 y conclusión](https://www150.statcan.gc.ca/n1/pub/12-001-x/2004002/article/7751-eng.pdf).

**Texto propuesto de firma:** «FP-371: conservar DIN como punto descriptivo. SRS y constante+folio podrán mostrarse sólo como sensibilidades; no se usarán como ground truth inferencial ni como distribución de incertidumbre validada. Continuar la vía oficial de varianza». Alternativa B: omitir por completo esas sensibilidades de la presentación actual. Ambas conservan el punto.

## 4. S6: separar magnitud observada de evidencia inferencial

**Problema en el repo.** C1 tiene delta puntual −6.60 pp; C3 +18.19 pp y C4 +6.70 pp. Sus etiquetas históricas de corroboración o no discriminación usan bootstrap por localidad. El corte mantiene R4.4 en MEDIA, sin adopción nueva de estas tasas. [Contraste S6 de #702](https://github.com/Josanoforo/Modelado-Mexicano/blob/67f0b6ef96436c560ddfec116d32575da5a865a1/forense/notas/2026-09-10-GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL-contraste.md).

**Benchmark.** El documento oficial registra 180 UPM y una estratificación socioeconómica de tres clases dentro de una estructura geográfica más amplia. La FAQ describe los cuatro valores públicos de `estrato` como categorías de tamaño de localidad. Ninguna de esas referencias acredita que las 150 localidades identificadas por el cálculo sean unidades equivalentes para estimar la varianza oficial. [Diseño ENNViH, §4.1.2 y cuadro 1](https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf), [FAQ, área urbana/rural](https://ennvih-mxfls.org/faq.html).

La diferencia 150/180 no permite, por sí sola, calcular sesgo ni afirmar que una agrupación más amplia sea inútil. Hace falta justificar la relación entre unidades. Tampoco corresponde construir un diseño artificial con sólo tres estratos a partir del resumen del manual.

**Aplicación propuesta.** Mantener el dato que describe cada contraste. No promover C3/C4 porque su IC aproximado excluye cero; no afirmar que C1 prueba ausencia de asociación porque lo incluye. Las etiquetas históricas permanecen ligadas al contrato que las produjo. ASA recomienda que las conclusiones no dependan únicamente de superar un umbral y distingue significancia de tamaño o importancia del efecto. [Principios ASA](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf).

Para el motor, las asociaciones pueden informar contexto o escenarios si el consumidor lo pide, pero no identifican un efecto causal individual. Antes de una decisión basada en estos contrastes, definir qué magnitud cambiaría la acción; ese umbral debe venir del problema, no de buscar qué fila supera significancia. Si la decisión cambia al variar supuestos plausibles, priorizar la varianza oficial.

**Casos límite.** Corregir un join hogar/persona no valida el diseño. Elegir la agrupación que haga C3 positiva y significativa sería seleccionar el método por su resultado. Las sensibilidades deben conservar conjuntamente las estimaciones que comparten muestra; no sortear sus incertidumbres como si fueran independientes. Para una eventual varianza de dominio, utilizar la información del diseño completo necesaria para ese estimador. [Análisis de dominios NHANES](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx).

**Texto propuesto de firma:** «FP-372: usar C1/C3/C4 como puntos y asociaciones descriptivas. Sus IC por localidad se conservan sólo como sensibilidad; no justifican promociones nuevas ni afirmaciones de ausencia de asociación. R4.4 permanece MEDIA. NC-0156 sigue abierta por diseño oficial». Alternativa B: omitir los EE/IC del uso actual. Esta firma es independiente de FP-371.

## 5. Complemento ENVIPE: sí sirve, con su objeto exacto

**Problema en el repo.** El padre identifica personas con algún delito elegible cuya razón pertenece a `{01,02,06,08}`. RES-0028 materializa su complemento, dentro del recorte de razones 01–08. No estima la respuesta literal 09 y excluye del recorte 99 y blancos. [Ficha RES-0028 de #689](https://github.com/Josanoforo/Modelado-Mexicano/blob/67f0b6ef96436c560ddfec116d32575da5a865a1/forense/notas/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS-cierre.md).

**Benchmark.** NCHS trata expresamente proporciones complementarias: comparten error estándar y anchura del intervalo, aunque su precisión relativa puede diferir. ENVIPE separa 01–08 de la respuesta residual 09 y la no respuesta 99; además pregunta por la razón principal de un delito, no por una categoría única permanente de la persona. [NCHS, página impresa 4](https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf), [ENVIPE, pregunta 1.23](https://www.inegi.org.mx/contenidos/programas/envipe/2025/doc/cuest_modulo_envipe2025.pdf).

**Derivación propia, no otra medición:** para la misma población elegible U, ponderadores y variable binaria,

\[
\hat q=1-\hat p,\qquad
\operatorname{Var}(\hat q)=\operatorname{Var}(\hat p),\qquad
\operatorname{Cov}(\hat p,\hat q)=-\operatorname{Var}(\hat p).
\]

Con las cifras publicadas, `p=0.29431298745731216`, `q=0.7056870125426878`. La transformación del IC del padre da `[0.6942008049952509, 0.7169802491746927]`. No se hizo un nuevo cálculo de encuesta: sólo se transformaron los límites publicados. La validez inferencial de ese intervalo no supera la del padre.

**Caso que debe proteger el consumo a nivel persona.** Una persona registra dos delitos elegibles: uno con razón 01 y otro con razón 04. Tiene un delito del grupo padre y también uno del resto de códigos. Para el estimando actual, indicador padre=1 y complemento=0. Por eso `q` no significa «tiene algún delito con otra razón»; significa «no tiene ningún delito elegible del grupo padre», dentro del universo de personas admitidas.

**Uso recomendado.** Permitir la adopción bajo ese contrato. El motor usa un padre y deriva su opuesto; no genera dos Bernoulli independientes ni presenta ambos como evidencia adicional. Si se necesita una tasa por delito, o incluir 09, es un estimando sucesor. La ampliación B puede aportar valor después, pero no es necesaria para que el complemento actual sea matemáticamente válido.

**Aceptación mínima:** misma unidad, población y pesos; mezcla de razones en una persona resuelta correctamente; 09/99/blancos no convertidos en negativos universales; denominador vacío produce no estimable; cada réplica satisface `p[b]+q[b]=1`; cita de padre y transformación. En p=0/1, un intervalo empírico degenerado no prueba certeza poblacional.

**Texto propuesto de firma:** «Adoptar RES-0028 exclusivamente como complemento dependiente del padre a nivel persona bajo U1/U4. No representa 09 Otra ni cualquier delito con otra razón. Compartir incertidumbre y rechazar usos fuera del dominio». NC-0085 cierra cuando la adopción y su consumo queden implementados, no por la firma sola.

## 6. Corrupción: retirar cifras antiguas y precisar el papel de r2

**Problema en el repo.** #695 demuestra que elegir primera/última fila eliminaría eventos legítimos. `ID_TRA` identifica persona×tipo; `NT_TIPO` distingue eventos. `P8_4` vive en ID_TRA, mientras el canal vive en el evento. La r2 sin deduplicar reproduce una estadística de la tabla unida, pero eso no demuestra que localice la solicitud en cada evento. Las tasas antiguas RES-0009/0011 siguen sin adopción. [Cierre técnico #695](https://github.com/Josanoforo/Modelado-Mexicano/blob/67f0b6ef96436c560ddfec116d32575da5a865a1/forense/notas/2026-09-10-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL-cierre.md).

**Benchmark externo.** ODS 16.5.1 mide personas con experiencia de solicitud o entrega entre quienes tuvieron contacto con funcionarios en el mismo periodo. La unidad es persona expuesta, no transacción ni exclusivamente personas que ya declararon corrupción. ENCIG registra canales de los últimos eventos y recoge por separado el tipo de trámite afectado y el número de veces con la experiencia. [Metadatos ONU/UNODC](https://unstats.un.org/sdgs/metadata/files/Metadata-16-05-01.pdf), [ENCIG, preguntas 7.3 y 8.4–8.5](https://www.inegi.org.mx/contenidos/programas/encig/2025/doc/encig25_cuestionario.pdf).

**Consecuencia propia.** Un join 1:m puede ser correcto para conservar las filas y, aun así, producir un indicador distinto del que necesita el motor. Replicar el mismo resultado de ID_TRA sobre sus eventos introduce multiplicidad; para estimar una probabilidad por evento se debe acreditar tanto la atribución como el ponderador que corresponde a esa unidad.

| Objeto que podría querer el motor | Fuente/condición necesaria | Qué no lo sustituye |
|---|---|---|
| Riesgo anual de persona con contacto | Experiencia directa, contactos y población/persona correspondientes | Proporción sobre quienes ya declararon corrupción. |
| Experiencia anual por persona×tipo de trámite | Resultado y frecuencia anual en esa unidad | Elegir el último evento para representar todas las realizaciones. |
| Probabilidad de solicitud en evento presencial/digital | Solicitud y canal del mismo evento, negativos elegibles, pesos y periodo | Copiar un indicador anual en cada evento y cambiar su etiqueta. |
| Escenario descriptivo de la tabla unida | Definición literal del proxy y multiplicidad documentada | Presentarlo como una tasa empírica de solicitud por evento. |

**Ejemplo hipotético:** una persona tuvo cuatro realizaciones del mismo trámite durante el año; sólo observamos el canal de las tres últimas y sabemos que hubo una experiencia de corrupción. Puede haber ocurrido en cualquiera de ellas o en la cuarta. No se resuelve asignándola a la primera fila ni porque las tres visibles tengan el mismo canal. Las cotas sólo son válidas para el universo cubierto por sus supuestos; la envolvente de #695 no pasa a ser una cota nacional por nombrarla así.

También debe conservarse la codificación: el agregado histórico `{3,4,5}` de P7_3 incluye teléfono, Internet y cajero/kiosco; no significa únicamente Internet. No cambiar ahora ese grupo por el que produzca mayor diferencia. Una separación futura requiere otra spec. [Catálogo P7_3 de ENCIG](https://www.inegi.org.mx/contenidos/programas/encig/2025/doc/encig25_cuestionario.pdf).

**Recomendación revisada:** A para retirar la expectativa de adoptar RES-0009/0011, **con una corrección adicional de alcance para r2**. Puede conservarse como resultado histórico y contexto/proxy explícito. Si un consumidor la interpreta como probabilidad de solicitud en ese evento, propongo suspender ese uso concreto hasta identificarlo o aprobar un escenario provisional con otro contrato. No borrar el dato, cambiar capturas históricas ni afirmar que toda r2 es numéricamente errónea.

Esto no reduce adquisición. Continuar NC-0153 con la solicitud oficial del enlace o una fuente equivalente. ENEAC sirve dentro de su universo de microempresas de Aguascalientes; no acredita un parámetro nacional. Puede abrirse B como sucesor científico con una pregunta útil, sin intentar recuperar por conveniencia las dos tasas antiguas.

**Texto propuesto de firma:** «Desistir de adoptar RES-0009/0011, preservando su historia. Mantener r2 sólo bajo una interpretación descriptiva o de escenario explícito; no usarla como probabilidad empírica de solicitud por evento/canal sin identificación. Continuar la fuente general y preparar un sucesor si el motor requiere ese riesgo». Este texto es más preciso que la opción A anterior y requiere una elección expresa de mesa.

## 7. Qué implica para los encargos ya preparados

1. **17:** no cambia su objetivo de linaje. Un dato reproducible puede seguir sin identificar el parámetro que se le atribuye.
2. **18:** adjuntar este benchmark. Incorporar las decisiones elegidas, la prueba de persona con razones mixtas y la separación entre proxy r2 y probabilidad por evento. Completar esas fases con las herramientas existentes; no crear otra plataforma de gobernanza.
3. **19:** mantener separados punto de R, incertidumbre de encuesta, variación del LLM y conjunto de celdas. Las firmas DIN/S6 no convierten el panel conocido en una evaluación independiente ni autorizan nuevas llamadas por sí solas.
4. **Adquisición:** reutilizar la solicitud ENNViH para DIN/S6 y el expediente ENCIG. Primero metadatos o respuesta oficial; después spec sucesora y cálculo. No exigir datos nuevos para utilizar un complemento ya identificado.

La evidencia favorece seguir usando lo identificado y dirigir el trabajo nuevo a lo que falta identificar. **Mi propuesta final es DIN A, S6 A, complemento A con contrato de persona, y corrupción A reforzada con revisión del uso de r2.** No quedan firmadas por la realización de este benchmark.
