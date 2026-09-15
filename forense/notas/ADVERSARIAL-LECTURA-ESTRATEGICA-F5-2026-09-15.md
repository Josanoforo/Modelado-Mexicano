<!-- PROCEDENCIA: insumo externo (Astra), pegado por mesa en la conversación de dirección el 15/sep/2026 como adversarial de LECTURA-ESTRATEGICA-F5 v1.0. Archivado verbatim para NC-0219. Dirección verificó sus cifras contra el repo: todas reproducen. -->

# Adversarial de la lectura estratégica F5 · 15 de septiembre de 2026

**Dictamen: conservar la prioridad de medir, comparar contra una referencia simple y escribir resultados; corregir las premisas antes de adoptar la lectura como estrategia. D-A procede reformulada como reanálisis descriptivo; D-B no procede como autorización automática por seis familias; D-C puede empezar ahora.**

## Alcance y evidencia

Documento revisado: `LECTURA-ESTRATEGICA-F5-2026-09-15.md`. Se consultó GitHub: `main` resolvió a `582d4e936654cf0b5cac9574a60a9aafb0a2f5a4`, la misma base declarada por la lectura. Se contrastaron resultados, notas, protocolo y demanda publicados en ese corte. La copia local incluye un commit posterior de habilitación; sus modificaciones se excluyeron de este análisis. La demanda se leyó directamente mediante `git show 582d4e93:...`. Los ZIP del 7 de agosto se inspeccionaron como antecedentes, sin emplearlos para determinar estados actuales.

No se modificó el repositorio, no se cerraron NC, no se autorizaron llamadas y no se volvió a ejecutar microdato. Los cálculos nuevos son reanálisis exploratorios de resultados existentes, sin adjudicación ni cambio de los resultados sellados.

## 1. B no es medición directa del objetivo: cambia la tesis central

La lectura transforma el resultado de B en «la medición directa lo es por mucho» y propone que el valor esté en medir mediante B. El cierre B-MARCO define otra cosa: **persistencia de la última ola anterior de la misma serie**. El valor fuente está medido; aplicarlo al objetivo de otra ola es una predicción mediante una regla simple.

Ejemplo: para CIV-M-02, objetivo 2013, B·PERSISTENCIA usa la proporción de 2012. No mide 2013. El control que reproduce R en la ola objetivo comprueba que el medidor usa el mismo estimando; no es la predicción que se puntúa como B.

B-MARCO, además, separa PERSISTENCIA (10/14 celdas) y OPERATIVO (5/14). No se puede describir la cobertura de persistencia como disponibilidad operativa acreditada al corte. El cierre declara también exposición a los resultados: B es una comparación retrospectiva con regla fija, no una validación ciega.

**Consecuencia estratégica:** el hallazgo sostiene que una regla temporal simple merece ser el comparador de M. No demuestra por sí mismo la superioridad general de medir directamente ni identifica un límite óptimo de error. Un baseline puede mejorarse; no es un techo de lo alcanzable.

**Corrección:** «En las series evaluables, la persistencia temporal ofrece una referencia competitiva y barata. El valor añadido de M frente a ella sigue por demostrar».

## 2. La comparación útil con B se puede producir ahora

La tabla B-MARCO usa L de `CALC-C0D-MARCADOR-v3`, mientras la tríada limpia usa las capturas de F5 completa. La lectura advierte el cambio de snapshot, pero todavía utiliza ambos órdenes para una tesis conjunta. Además, la comparación antigua contiene L_SOLO con n=9 frente a B/M con n=10: tampoco es una comparación de cuatro brazos sobre idénticas celdas.

Se cruzaron los puntos exactos de `F5-completa-resultado-v1_0.json` con `CALC-B-MARCO-MAE-0001/resultados.json`. Se verificó igualdad del R compartido con tolerancia 1e-12. Se tomó únicamente la intersección con U3 y se calculó `100 × media(abs(punto−R))` para todos los brazos sobre las mismas filas.

| Universo común | n | B, MAE pp | L_CORPUS | L_SOLO | M |
|---|---:|---:|---:|---:|---:|
| U3 ∩ B·PERSISTENCIA | 9 | 0.884716 | 1.222815 | 1.480597 | 4.638093 |
| U3 ∩ B·OPERATIVO | 4 | 0.497681 | 2.216857 | 1.654357 | 8.148157 |

Primera fila: CIV-M-01/02/04/10/12/13 y FAM-M-05/06/07. B presenta menos error que M en 7/9. Segunda: CIV-M-04/10/12/13; B presenta menos error que M en 4/4.

**La ventaja descriptiva de B persiste utilizando L de la tríada limpia.** No depende de mantener los malos resultados L del marcador anterior. Pero el primer subconjunto contiene solamente seis celdas cívicas y tres de remesas; el segundo es enteramente cívico. No identifica superioridad universal ni informa sobre las cuatro celdas sin B.

Esto adelanta el contenido analítico de D-A, sin nuevas llamadas. Una publicación formal puede registrar el reanálisis y su consumo. No hace falta esperar ese trámite para interpretar la tabla o empezar el informe.

**Corrección material de identidad:** U3 incluye TRA-M-03, no TRA-M-07. La lista de la lectura cambia una por otra. TRA-M-07 es precisamente una celda sin punto L_CORPUS de la primaria y luego recuperada por RUN-2. Ese intercambio puede contaminar la intersección para D-A; debe corregirse desde los IDs del resultado sellado.

## 3. «M último» no basta para determinar el papel del motor

Es cierto que M ocupa el último puesto puntual bajo el promedio por celda de la tríada. Es falso extenderlo a «donde podemos verificar, el motor no es el mejor estimador» sin conservar el alcance del panel y la incertidumbre.

Las seis celdas CIV aportan 68.88% del MAE de M. Una sola celda, FAM-M-01, aporta 54.17% del MAE de los dos L. El orden depende considerablemente de qué mecanismo se repite más en el panel.

Como comprobación exploratoria de esa sensibilidad, se calculó la media del error de cada uno de los cinco grupos del diagnóstico representados en U3 —CIV, remesas, apoyo ENIF, ENCUCI y ENCIG— y después se dio el mismo peso a cada grupo:

| Agregación exploratoria con igual peso por grupo | MAE pp |
|---|---:|
| M | 5.028459 |
| L_SOLO | 7.315042 |
| L_CORPUS | 7.529374 |

**El orden puntual se invierte.** No se propone este promedio como nueva adjudicación: cambia la ponderación, usa grupos exploratorios y conserva los defectos de comparabilidad. Su función es demostrar que «M último» no es una propiedad estable frente a una elección sustantiva de ponderación.

También hay cobertura de celda basada en pocas respuestas: L_CORPUS aporta FAM-M-01 y TRA-M-02 con 1/8 respuestas válidas cada una. El 12/14 no equivale a respuesta robusta en doce celdas. Los IC de la primaria no incorporan simultáneamente toda la variación L y la incertidumbre R, como reconoce el diagnóstico.

**Decisión:** conservar SIN-GANADOR-UNICO. Usar el ranking como descripción del panel, no como justificación suficiente para relegar o adoptar un estimador.

## 4. Alineación explica un problema; no absuelve a los parámetros

La evidencia confirma una comparación cívica defectuosa: persona frente a delito, recortes y códigos distintos, y olas distintas. Esa parte no identifica el error del parámetro para el estimando propio de M. Tampoco identifica su corrección.

La frase «el error de M es de alineación, no de p» convierte una limitación de evaluación en una conclusión sobre p. FAM-M-01 conserva un problema de comparabilidad entre versiones. La sensibilidad conocida reduce MAE de M de 4.986673 a 4.263829; no acredita que el error restante desaparezca ni valida el motor renovado.

**Corrección:** «La evaluación actual no permite atribuir buena parte del error a p. Primero hay que comparar el mismo estimando; después medir el error residual».

Hacer explícito el contrato puede transformar una emisión incompatible en NO_COVERAGE. Eso mejora el uso, pero no demuestra menor error predictivo. La siguiente evaluación debe publicar conjuntamente precisión y cobertura.

## 5. RUN-2 tiene éxito local; no prueba un servicio completo de recuperación

El resultado 8/8 contra 0/8 en cada una de dos celdas satisface el criterio previamente fijado. No hay razón para repetir las 32 posiciones ni desconocer ese producto.

La expresión «fiabilidad máxima» debe sustituirse por **éxito observado completo en dos celdas y sus paquetes**. Son 16 respuestas dirigidas sobre dos tareas, no 16 tareas independientes. El control carece del material necesario y se abstiene correctamente. El tratamiento añade documentos nativos, variables y ponderadores específicos: el experimento prueba su aprovechamiento bajo ese montaje.

No prueba por separado que el sistema descubra autónomamente la fuente, negocie acceso, seleccione el reactivo correcto en una encuesta nueva o construya el paquete sin intervención. Tampoco aísla cuánto valor añade L sobre una función determinista: las trazas aceptadas se verifican contra `weighted_distribution` sobre `analysis.tsv`.

**Implicación práctica:** mantener al agente donde se requiere buscar e interpretar documentación; una vez fijados fuente, variable, población y ponderador, aprovechar el cálculo determinista ya disponible. La ventaja específica del agente frente a ese cálculo aún no se midió.

NC-0152 tiene fundamento para cierre por cobertura documental recuperada mediante el sucesor. El cierre debe conservar que el tratamiento original se abstuvo y que la tríada primaria no se completa retrospectivamente con las nuevas respuestas.

## 6. D-B confunde dos preguntas experimentales

La lectura afirma que F6 probará la transferencia de la capacidad documental. Sin embargo, FP-374 §5.1 define:

`d_f = error_M,f − error_L_SOLO,f`

Su éxito requiere un límite superior del IC95 inferior a −0.02. Es una hipótesis de ventaja de M frente a L_SOLO, no de cobertura documental del brazo dirigido frente a contexto.

**Decisión necesaria:** escoger qué pregunta merece el siguiente presupuesto. La repetibilidad documental en tareas nuevas requiere continuidad de FP-373 con su desenlace de cobertura/trazabilidad. Evaluar capacidad predictiva de M requiere FP-374 y su diseño. Son fines legítimos y diferentes; uno no debe financiarse presentándolo como el otro.

## 7. Seis familias no bastan para autorizar automáticamente FP-374

La propuesta vigente §6.4 pide lista nominal previa de 18 familias × 2 celdas y consumidor M: seis piloto y doce confirmatorias mínimas. El piloto puede exigir más familias confirmatorias según la varianza. Cambiar esta condición es una decisión de rediseño, no un resultado automático de actualizar el inventario.

Además, un resultado nuevo no es necesariamente una familia nueva, y una familia nueva no es necesariamente retenida. Hace falta comprobar exposición, split previo, dos celdas no redundantes, comparabilidad, consumidor y reserva del objetivo. Clasificar como retenida una medición después de examinar su resultado no restaura independencia. La adquisición orientada a alimentar el motor puede exponer o incorporar al desarrollo justamente aquello que después se pretende reservar.

**Recomendación:** inventario corto por familia con elegibilidad y faltante concreto; reserva prospectiva antes de exponer valores. Si no hay una ruta realista al confirmatorio, la propia propuesta permite factibilidad acotada de hasta tres familias, sin adjudicación de transferencia. Eso produce aprendizaje sin fingir que el confirmatorio está listo.

La referencia de la lectura a «el analiza.py del panel» tampoco identifica un ejecutable que resuelva ese juicio: el `analiza.py` localizado reconstruye F5 y sus contribuciones; no acredita familias retenidas actuales.

## 8. El cron no acredita que esté llenando ese panel

La demanda publicada en `582d4e93` coloca NC-0161 y NC-0162 en `ESPERA_O_DELEGADA`, responsable FP-374, etapa `DECISION_O_IMPLEMENTACION`, y las incluye entre las excluidas de investigación. Sus contratos científicos están incompletos.

Eso no demuestra que ningún otro trabajo pueda beneficiar el panel. Sí impide afirmar que su demanda «ya es exactamente ésa» o que el servicio lo llenará automáticamente. Operación del cron, adquisición pertinente y familia experimental retenida son resultados diferentes.

**Corrección mínima:** si mesa elige ampliar el panel, identificar las familias candidatas y el producto que necesita cada una, con reserva experimental explícita antes de acceso a valores. No hace falta otra capa general de gobernanza.

## 9. D-C introduce una espera innecesaria

La tríada previa respondía una pregunta explícita entre tres contendientes. Agregar B es útil para entender el valor añadido; su ausencia no invalida retroactivamente SIN-GANADOR-UNICO ni convierte el estudio en inutilizable.

El informe puede escribirse hoy con primaria, recuperación documental, comparación exploratoria con B y limitaciones. El trámite de registro de D-A no debe bloquearlo. F6 debe figurar como propuesta pendiente, no «en curso», mientras no exista ejecución acreditada.

El informe tampoco debe dar por probado el valor de M «donde no hay fuente». La ausencia del objetivo observable no valida la extrapolación. M puede usarse allí como escenario o hipótesis explícita, con incertidumbre y dominio de aplicación; convertirlo en estimador confiable requiere evaluación externa pertinente.

## Decisiones recomendadas

| Decisión | Recomendación |
|---|---|
| D-A | Sí, como reanálisis descriptivo sobre intersecciones explícitas, puntos L de la tríada limpia y B separado por variante. El cálculo principal ya está en §2. No cambiar retrospectivamente la adjudicación. |
| D-B | No autorizar por el umbral aislado de seis. Primero separar pregunta documental de transferencia de M y comprobar elegibilidad/reserva. Usar factibilidad acotada si es el camino útil disponible. |
| D-C | Escribir ahora. Integrar B como diagnóstico; conservar F6 pendiente y los límites de cada experimento. |
| NC-0152 | Cierre justificable por RUN-2, acotado al tratamiento sucesor y sin modificar la primaria. |
| NC-0161/0162 | Una decisión puede resolver el pendiente de autorización o cambiar el objetivo; no debe registrarse como ejecución o validación del M renovado. |
| NC-0187 | Resolver el destino de B mediante consumo analítico; no tratar las 471 filas RESULT como 471 estimaciones independientes ni su ausencia de adopción como desperdicio. |

**Tesis estratégica corregida:** el programa ya demuestra mediciones reproducibles y aprovechamiento documental exitoso en dos tareas. La persistencia temporal es una referencia competitiva en el subconjunto comparable. F5 no acredita ventaja general de M ni permite descartarlo globalmente. El siguiente gasto debe dirigirse a una pregunta concreta —valor predictivo añadido o adquisición documental en tareas nuevas— con una evaluación que efectivamente la mida.

**¿Quedó el proyecto más cerca de una medición, decisión o modelo mejor? Sí:** se produjo una comparación limpia de cuatro brazos y se identificó qué decisión experimental evitaría gastar llamadas para responder otra pregunta.

## Fuentes principales del corte revisado

- [Resultado sellado TRIADA-0002](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/data/corrida0/CALC-TRIADA-0002/resultados.json).
- [F5 completa: puntos por celda](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/prereg-duelo-v2/F5-completa-resultado-v1_0.json).
- [Diagnóstico de aprendizajes](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/notas/2026-09-10-GEN2-F5-APRENDIZAJES-Y-SUCESOR-diagnostico.md).
- [Cierre B-MARCO](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/notas/2026-09-14-GEN2-B-MARCO-cierre.md).
- [Puntos de B para el cruce](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/data/corrida0/CALC-B-MARCO-MAE-0001/resultados.json).
- [Cierre RUN-2](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/notas/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-2-cierre.md).
- [Protocolo FP-373 y FP-374](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/prereg-duelo-v2/F5-panel-viabilidad-presupuesto-spec-v1_0.md).
- [Demanda publicada](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/data/adq-demanda-activa-v1_0.json).
- [Pendientes NC](https://github.com/Josanoforo/Modelado-Mexicano/blob/582d4e93/forense/no-corrido.tsv).
