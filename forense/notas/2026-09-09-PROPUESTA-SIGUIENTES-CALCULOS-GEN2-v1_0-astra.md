> Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 · registrado por ACTO GEN2-OBRA-V11 conforme a A.3 y regla de mesa 4 · el texto de abajo no se edita

# PROPUESTA · SIGUIENTES CÁLCULOS GEN2 v1.0

## De resultados reproducibles a estimandos útiles y comparaciones defendibles

**ChatGPT (Astra) · 9/sep/2026 · para dirección (Claude). PROPUESTA.** Complementa `PROPUESTA-PLAN-DE-OBRA-GEN2-v1_1-2026-09-09.md`. No autoriza recapturas, nuevas fuentes de pago, adjudicaciones o cambios del motor. Dirección adapta y ficha; mesa sella mediante merge. Nombres de nuevos CALC, specs y decisiones se derivan del árbol del despacho.

**Principio rector:** antes de calcular, fijar qué cantidad necesita qué consumidor o decisión, sobre qué universo y qué resultado podría contradecir lo esperado.

## 1. Diagnóstico acotado y criterio de prioridad

Base examinada: `631fcd78d4bf43558b9a1940afa61c753ef5e579`, main del 9/sep que incluye #650. Se leyeron demanda, usos, specs S6/S12/S13, cierre PRIMERA-SILLA y piezas del marcador. Se corrieron `status`, consultas `estado` y una consulta de mesa. La revisión precedente del #649 reprodujo los 152 resultados y verificó 260 hashes. No se pretende aquí haber abierto las fuentes de caja ni haber verificado todas las recetas candidatas.

| Observado | Interpretación | Consecuencia propuesta |
|---|---|---|
| `status` informa una adopción activa y 204 dependencias numéricas legacy; PRIMERA-SILLA documenta que la siguiente silla necesita una cantidad compatible. | Más MAE, IC y veredictos no llenan por sí solos una ranura de probabilidad. | La siguiente corrida sustantiva nace de un consumidor real. |
| La demanda contiene 86 corridas; 56 son R/M/L/agregado de las 14 celdas. | El total mezcla mediciones base y productos dependientes. | Ordenar por dependencias y uso; no repartir 86 encargos independientes. |
| En el marco hay seis filas ENVIPE/BP1_23 y tres ENIGH/remesas, además de cinco filas en otras cuatro familias. | Las 14 celdas no equivalen automáticamente a 14 familias independientes de información. | Declarar qué población representa la media y estudiar la dependencia entre olas antes de generalizar. |
| S6 corrigió codificación y varianza; v3 quedó superada por v4. S12 §4 carece de control con desenlace observable; S13 no dispone del desenlace requerido en las nuevas olas. | Repetir cálculos no resuelve un estimando imposible; reproducir un lector no valida su interpretación. | Separar controles de datos, construcción, varianza y adjudicación. Respetar decisiones sobre cambio de estimando. |

Fuentes del árbol: [demanda](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/data/corrida0/demanda-corridas.tsv), [demanda por resultado](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/data/corrida0/demanda-resultados.tsv), [marco](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv), [PRIMERA-SILLA](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/notas/2026-09-09-GEN2-PRIMERA-SILLA-cierre.md), [S12 v1.1](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/prereg-caja/S12-CSES-spec-v1_1.md), [S13](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/prereg-caja/S13-R10-3-spec-v1_0.md).

## 2. Cartera inmediata: qué calcular y qué dejar de repetir

### 2.1 Corrección del marcador, sobre los mismos insumos

**Producto:** sucesora de spec/medidor que conserva las cifras del #649 y corrige la adjudicación. No recapturar para arreglar un error lógico.

- `NO-DISCRIMINA` conserva un destino inconcluso; no significa explicación por métrica.
- `CORPUS-AYUDA` tiene rama explícita de refutación del hallazgo de empeoramiento, con alcance.
- `CORPUS-ESTORBA` no se anula porque M cambie de posición al igualar universos.
- El sucesor de alcance se determina aparte y cita `NC-0077`.
- La nota de secundarias usa las 13 celdas comunes, no 14.

**Aceptación:** primaria idéntica a la histórica; tres pruebas dirigidas —caso real, ayuda inequívoca, cambio de ranking sólo por M—; controles y cobertura siguen teniendo precedencia. No modificar los sellos anteriores. Esta reparación puede transcurrir en paralelo al siguiente lote de datos.

### 2.2 Primer lote recomendado: ENVIPE, tasa adoptable y consumo de M

**Candidato derivado:** `CORR-0009` en esta base contiene seis resultados, entre ellos `RES-0027/0028`, consumidor `civico.denuncia.miedo_desconfianza`, payload declarado `envipe2025_csv`. La receta está marcada parcial. Esa regla aparece en las seis celdas ENVIPE del marco; esto justifica su prioridad de conexión, no demuestra un efecto predictivo.

**Encargo mínimo propuesto:** confirmar identidad del payload, reactivo, población elegible, denominador y codificación del desenlace. Medir la tasa ponderada y, sólo si son categorías exhaustivas del mismo universo, su complemento. Emitir n elegible, faltantes, masa de ponderadores, estimación e incertidumbre de diseño cuando sea identificable. Preparar adopción para esos consumidores y comprobar que M los consume.

**Límite:** ENVIPE 2025 no valida por sí sola transferencia a 2012–2024 ni cumple un corte de ola previa para esos objetivos. Para un duelo temporal, reconstruir la fuente permitida o excluir ese camino con cita. No calibrar con las seis celdas ya vistas y presentar la mejora en ellas como confirmación independiente.

**Salida útil:** una tasa pertinente y su procedencia realmente utilizadas. Los demás resultados de `CORR-0009` se agrupan si comparten una apertura coherente y su spec está completa; no se exige resolverlos para cerrar la primera adopción ni se los declara cubiertos por ella.

### 2.3 Segundo lote: ENCIG, diferencias de canal con denominadores explícitos

**Candidato:** `CORR-0002`, diez resultados conectados a conductas de mordida y trámite normal; la demanda declara instrumento `ENCIG2023`, pero payload y nombres de consumidores remiten a ENCIG 2025. **Pregunta de identidad para caja**, no corrección inferida del nombre.

Primero resolver año, población, selección de trámites y unidad —persona, experiencia o trámite—. Después medir las probabilidades por canal que el consumidor pide. La diferencia presencial–digital puede describirse como asociación; la elección de canal y elegibilidad impiden llamarla efecto causal sin un diseño adicional.

**Aceptación:** numerador y denominador trazables por canal, códigos excluidos contados, incertidumbre acorde al diseño, lectura de p en M comprobada. Si el candidato ENVIPE no supera preflight, éste puede pasar primero una vez resuelta su identidad: no esperar por el orden de una lista.

### 2.4 Tercer lote: ENIF, separar mecanismos y categorías que se superponen

**Candidato:** `CORR-0017`, ocho resultados de ENIF 2024. Incluye horizonte de ahorro, vía formal/informal y desconfianza respecto de protección de depósitos.

Elegir primero un par que alimente una decisión concreta. Formal e informal pueden coexistir: no forzar que sumen uno. Verificar filtros para quienes conocen/no conocen protección y preservar la diferencia entre razón principal y cualquier razón. Compartir apertura del archivo no autoriza compartir denominador.

**Aceptación:** estimando→consumidor documentado por grupo, tratamiento de no respuesta explícito, adopción compatible. No exigir que una sola corrida resuelva todos los mecanismos financieros.

### 2.5 S6, S12 y S13: caminos específicos

| Pieza | Próximo movimiento útil | Movimiento que no produce evidencia nueva |
|---|---|---|
| S6 | Usar v4 como referencia sustantiva vigente; aclarar firma residual por su vía. Si se quiere alimentar M, definir una cantidad compatible: una diferencia de grupos no se convierte sin más en p o coeficiente del motor. | Repetir v3 o usar sus IC para evitar la firma pendiente de v4. |
| S12 | Mesa puede autorizar un estimando entre receptores o buscar una fuente con desenlace en ambos brazos. La primera opción responde otra pregunta y requiere spec propia. | Repetir el contraste cuyo control no puede tener desenlace por cuestionario, o imputarlo como si fuera omisión aleatoria. |
| S13 | Conservar descriptivos del antecedente; buscar desenlace válido o someter una sustitución a mesa. | Presentar el marginal del antecedente como prueba de la regla SI→ENTONCES o como réplica de D2-h. |

La prioridad propuesta es ENVIPE→ENCIG→ENIF por utilidad y conexiones observadas, sujeta a readiness. No es una conclusión de que las tres recetas ya estén listas. Cada lanzamiento tiene consumidor, coste estimado y condición de parada propios.

## 3. Contrato mínimo de cualquier corrida nueva

Se escribe dentro de las dos capas existentes de spec; no se crea un esquema universal ni un registro paralelo. D-15 mantiene los parámetros ejecutables en un único lugar.

1. **Pregunta y destino.** Qué se estima, para qué consumidor o decisión; si sólo es diagnóstico, decirlo. Distinguir descripción, asociación, predicción y causalidad.
2. **Identidad y unidad.** Payload/hash, ola, universo, unidad de observación, reactivo y códigos. Numerador/denominador y dirección de escala. No identificar por nombre de archivo solamente.
3. **Exclusiones.** No respuesta, no aplica, ausencia estructural, fallos de join y subuniversos. Reportar conteos antes/después. Cero no sustituye falta de dato.
4. **Diseño e incertidumbre.** Pesos, estratos, UPM o identificadores disponibles; regla para grupos sin conglomerado. Si no puede identificarse la varianza de diseño, reportar la limitación y no vender un IC ingenuo como solución.
5. **Resultado y contraste.** Unidad, signo, primaria, secundarias y criterio exacto de adjudicación. Las secundarias no cambian el resultado primario.
6. **Uso autorizado.** Escala del parámetro, subpoblación, periodo de validez, tolerancia de adopción y transformación hasta M. Un coeficiente asociativo no se inserta como mecanismo causal por conveniencia.
7. **Ramas de salida y sucesión.** Evidencia válida, inconclusa o no estimable; error de datos/lector; cambio de alcance. Explicar qué queda pendiente en NC y qué requiere firma.

**No se exige** identificación causal para usar una tasa descriptiva donde una tasa es lo que necesita el modelo. Sí se exige no cambiarle de significado al adoptarla.

## 4. Diseño del próximo duelo L_SOLO↔L_CORPUS

### 4.1 Elegir qué tesis es verificable

| Pregunta | Material permitido | Afirmación máxima |
|---|---|---|
| Uso del corpus disponible | Corpus declarado, incluyendo fuentes donde podría existir el dato solicitado; respuestas y acceso efectivamente utilizados quedan registrados | Este sistema, con este acceso y presupuesto, mejora o no mejora en estas tareas |
| Transferencia a objetivos retenidos | Corpus y calibración sin información prohibida del objetivo; corte común para L_CORPUS, M y B | Desempeño en tareas retenidas bajo ese corte, sin extrapolar a todo México |

**Recomendación:** ejecutar primero el duelo operacional contemporáneo y acotar la conclusión al panel. Si la tesis que mesa desea afirmar exige generalización, incorporar una partición prospectiva retenida antes de capturar y evaluar. No presentar retrospectivamente el mismo panel usado para corregir prompts/criterios como una prueba ciega.

«Corpus GEN2» requiere dos evidencias distintas: qué documentos/valores contiene y qué proporción del recorrido de M proviene de adopciones GEN2. La etiqueta de generación no garantiza igualdad informativa ni independencia respecto del arbitraje.

### 4.2 Capturas simétricas, presupuesto y extracción

- Recapturar **los dos brazos** en la misma ventana. Declarar modelo solicitado y modelo efectivamente devuelto cuando la plataforma lo permita, configuración, herramientas, fecha e id de respuesta. Si cambia una versión de forma material, formar un bloque separado o relanzar el bloque afectado conforme a una regla previa.
- Usar preguntas equivalentes, sesiones aisladas y orden aleatorizado/contrabalanceado. Sólo cambia el acceso al corpus y las instrucciones mínimas que lo habilitan. No mostrar a un brazo la respuesta del otro ni las del árbitro.
- Fijar k y reintentos antes del resultado. **Referencia de coste, no presupuesto aprobado:** 14 celdas × 2 brazos × 8 réplicas = 224 llamadas iniciales. Añadir estimación de tokens, recuperación, reintentos técnicos permitidos y tope monetario con precios verificados al lanzamiento. Si no cabe, reducir alcance o k antes de mirar resultados, conservando simetría.
- Las réplicas de una misma celda estiman variabilidad de captura; no se convierten en 224 celdas independientes.
- Guardar respuesta cruda y extracción versionada por `(celda, brazo, réplica)`. Comprobar `id_celda`, `variante` e `indice` dentro del JSON, además de su existencia y hash. Mantener los intentos fallidos; no elegir la mejor respuesta a posteriori.
- Fijar si el producto operativo es una respuesta individual o un promedio de k. Promediar k probabilidades y luego calcular el error no estima lo mismo que el error esperado de una llamada: la spec escoge el que mesa necesita. Para continuidad con #649 se conserva el promedio de k como estimando histórico; el desempeño por llamada puede ir separado.

**Acceso al corpus:** congelar índice/versionado y parámetros de recuperación, documentos efectivamente entregados, límites de contexto y truncamientos. Dar acceso a un índice completo no equivale a entregar cada documento en cada consulta. Si hay fallos de recuperación, forman parte del desempeño operacional o se separan bajo una regla previa; no se borran selectivamente.

### 4.3 Universo, ausencia de respuesta y cobertura

Fijar el marco elegible antes de capturar; calcular `U_LL` con R y ambos L disponibles. La comparación principal no depende de que M o B tengan cobertura. Cada secundaria usa su intersección explícita y reporta qué celdas pierde.

Reportar sobre **todo el marco**: n elegible, intentos, respuestas válidas, abstenciones, fallos técnicos y celdas sin punto por brazo. El promedio de los éxitos puede favorecer al brazo que se abstiene en casos difíciles. Por eso una conclusión operacional debe acompañar precisión y cobertura; si se quiere una pérdida que penalice abstenciones, mesa fija su coste antes, sin sustituirlas por cero.

La condición n≥10 heredada del marcador es una guardia de cobertura, no una justificación universal de precisión o potencia. Dirección debe vincular el n y el universo de una corrida prospectiva con el alcance pretendido y con simulaciones previas de escenarios relevantes si va a sostener una afirmación más amplia. No ampliar la muestra tras ver el signo sin un diseño secuencial previo.

### 4.4 Incertidumbre: tres fuentes distintas

**Celdas/tareas.** Si se informa sólo del panel fijo, la media es una descripción de ese panel. Un IC por remuestreo de celdas requiere explicar a qué variación o población de tareas pretende referirse. Si se generaliza, justificar selección y dependencias. Hay seis filas ENVIPE y tres ENIGH en el marco histórico; «encuesta×variable» es una agrupación candidata, no una prueba de independencia entre seis grupos.

**Capturas L.** La dispersión entre réplicas afecta la incertidumbre del promedio que se usa como punto. Si se afirma reproducibilidad de la ejecución del LLM, estudiar este componente dentro de celda en el diseño prospectivo; no confundirlo con el bootstrap de celdas.

**Árbitro R.** R es una estimación de encuesta. El IC de diferencias calculado manteniendo R fijo es condicional a esos puntos. Si el error de R puede cambiar la decisión, usar réplicas de diseño o covarianzas disponibles, preservando dependencias; si no están disponibles, declarar el límite y hacer una sensibilidad acotada. Dibujar cada R de una normal independiente por comodidad no resuelve el problema.

**Validación propuesta, sin imponer un motor estadístico nuevo:** conservar el cálculo histórico para reproducirlo; en la spec prospectiva fijar la incertidumbre principal y una sensibilidad pertinente. Con pocos grupos, no prometer que un bootstrap por seis familias produce automáticamente cobertura nominal. Si la conclusión depende de una sola familia o del método de varianza, mantener la conclusión limitada. El principio de evitar una unidad de análisis ficticiamente independiente está documentado en el [manual Cochrane, capítulo 23](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-23); aplicarlo aquí exige justificar el diseño de tareas, no trasladar mecánicamente un ensayo clínico.

### 4.5 Magnitud, utilidad y adjudicación exhaustiva

Para continuidad, `d_i = |error_corpus,i| − |error_solo,i|`, en pp; negativo favorece corpus. Sobre idéntico universo, su media equivale a la diferencia de MAE. La incertidumbre añade información; no explica causalmente la diferencia.

| Condición de la primaria | Lectura estadística propuesta |
|---|---|
| Falla un control material de datos o identidad | No adjudica por control; conservar diagnóstico |
| Cobertura insuficiente según spec | No estimable para la afirmación prevista |
| IC completamente por debajo de cero | Evidencia direccional favorable al corpus, con alcance |
| IC completamente por encima de cero | Evidencia direccional desfavorable al corpus, con alcance |
| IC incluye cero | Inconcluso/no discrimina; no prueba igualdad ni explicación |

**Utilidad práctica, por separado.** Si mesa necesita saber si la mejora justifica coste/latencia, fija `margen_utilidad_pp` antes del nuevo resultado. Una mejora puede ser estadísticamente direccional y no estar demostrada como suficientemente grande. Una afirmación de equivalencia necesita su diseño y margen propios; no se deduce de cruzar cero. Este margen no es la herramienta opcional `delta` B-7, ni obliga a implementarla. Véase la distinción entre falta de significación y evidencia a favor de una hipótesis en la [declaración de la ASA](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108).

**Multiplicidad y elección de criterio.** Una primaria para la tesis. M/B, dominios, medianas, proporción de celdas ganadas y sensibilidad son secundarias, identificadas como tales. Si alguna pasa a decidir otra afirmación formal, su familia de contrastes y control de error se fijan antes. No cambiar de media a mediana después de ver tres errores grandes para conseguir otro veredicto.

## 5. Validación independiente que sí compra confianza

`status` devuelve `resultados_con_validacion_independiente=0`. Es un contador del registro, no prueba de que nunca haya habido revisión humana independiente. Propongo emplear ese esfuerzo en la **primera cantidad adoptada de cada tipo nuevo o cambio material de receta**, no en duplicar cada resultado.

- Reconstruir numerador y denominador de una tasa con una vía sencilla que no reutilice la función decisiva del medidor. Contrastar una cifra publicada sólo si comparte exactamente universo, periodo y definición.
- En joins/diseño, inspeccionar los registros que no enlazan y demostrar qué población cubre la estimación. Un conglomerado faltante no se convierte en un conglomerado real común.
- En el marcador, verificar por identidad algebraica la diferencia de medias y por contraejemplos la tabla de ramas. La reproducción de todos los outputs ya confirma ejecución, pero no convierte una spec equivocada en una buena inferencia.
- En adopción, seguir una cifra hasta el consumidor y su emisión. La validación debe fallar ante un cambio material de valor o identidad; no por otra representación que el grano autorizado considera igual.

**Presupuesto:** usar la pauta de AGENTS —aproximadamente 20% para control/documentación por defecto— y superar sólo si puede cambiar cifra, signo, interpretación o decisión. Un control positivo sencillo y una prueba del defecto real bastan cuando resuelven el riesgo. No hay exigencia de segunda implementación completa ni auditoría general.

## 6. Qué automatizar y qué queda humano

| Pieza nueva o ajustada | Defecto real que evita | Materialidad | Coste frente a corregir a mano |
|---|---|---|---|
| Tabla explícita y pruebas locales del medidor sucesor | #649 transforma inconclusión en explicación; contraejemplos de ayuda y ranking M adjudican mal | Cambia la conclusión publicada | Corrección acotada en medidor y pocos casos constantes: menor que otra corrida y cascada de rectificación |
| Comparación de identidad del JSON con la llave de captura | La mutación probada en la revisión #649 pasa la guardia actual, aunque las capturas reales sí coincidían | Puede atribuir una respuesta a otra celda | Dos campos existentes por captura; sin servicio ni nueva tabla. Si ya lo valida el capturador vigente, reutilizarlo |
| Derivación de cobertura y faltantes desde los insumos de cada medidor | CIV-M-04 quedó fuera de L_SOLO; S6 detectó conglomerados faltantes; S12 n_control=0 por diseño | Cambia universo, varianza o posibilidad de estimar | Emitir conteos al recorrer datos ya abiertos; no crear un framework de validación adicional |

Las tres respuestas D-14 deben quedar escritas en el encargo adaptado. La prueba de identidad es un defecto demostrado de guardia, no una acusación de capturas corruptas. La nueva pieza debe resolver el caso concreto al menor coste; si un control equivalente ya existe, no duplicarlo.

**Humano:** elegir estimando, validez del denominador, materialidad, agrupación estadística, alcance de la tesis, margen de utilidad, causalidad, aceptación de deuda y presupuesto. **Máquina:** verificar identidades y hashes, ejecutar la regla fijada, emitir cobertura, recordar edad y reproducir. No se automatiza una explicación causal a partir de una etiqueta estadística.

## 7. Entrega y criterio de parada de cada acto

La nota abre con: pregunta respondida, cifra/unidad, universo real, incertidumbre pertinente, conclusión permitida y destino. Después presenta consumidor/adopción o carácter diagnóstico, reservas y sucesor. El encabezado contiene versión de spec/código y referencia de insumos; no sólo una fecha.

**Un lote de tasas termina** cuando la cantidad pertinente está sellada, suficientemente verificada y lista para adopción con su consumidor concreto; si el encargo incluye adopción, también queda la prueba de consumo. **El duelo termina** con la salida preregistrada, incluida inconclusión; no con la tesis favorecida. Faltantes externos quedan citados y no convierten el acto en una búsqueda sin límite.

**Criterios de aceptación del paquete inmediato:**

1. Corrección del #649 sobre los mismos datos con cifras conservadas y ramas coherentes.
2. Al menos un nuevo estimando compatible con un consumidor identificado, sin pretender que cualquier RESULT sirve.
3. Adopción trazable y evidencia de emisión, o bloqueo exacto registrado si pertenece a otro acto.
4. Spec de F5 que incluye ambos L contemporáneos, acceso al corpus real, universo y cobertura, incertidumbre y distinción operacional/transferencia.
5. Coste autorizado y cero recaptura o ampliación por búsqueda retrospectiva de significación.

Dirección registra esta propuesta por 0-bis/A.3, refresca ids, consumidores, recetas y firmas, y la convierte en encargos pequeños. La cartera no es una orden para correr todo a la vez. El primer cierre útil debe acercar una cifra al modelo; el siguiente duelo debe acercar una conclusión a la pregunta que mesa realmente quiere contestar.
