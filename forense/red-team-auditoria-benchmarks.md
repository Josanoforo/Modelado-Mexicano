> **NOTA DE RECUPERACIÓN · 11/ago/2026.** Este documento existía solo en el espejo del proyecto; el encargo del motor adaptativo lo citó y la Ronda 1 lo clasificó NO-ENCONTRADO en repo (universo: árbol + git log --all). Entra verbatim desde el espejo — procedencia tipo (2), sin sello de commit de origen. sha256 del original en espejo: 01d474050c3ca858f8cdfb9cdc9cb685bcecfcb20aba58e2bbaa710142fe4617. Resolución M0 de mesa, 11/ago/2026. Su contenido NO se edita.

# Auditoría adversarial — Análisis de benchmarks metodológicos

**Alcance:** revisión de las *condiciones* enunciadas de los papers citados. No hay acceso al repositorio del programa; toda afirmación que exija ver los archivos se marca **REQUIERE VERIFICACIÓN CONTRA ARCHIVO** y no se resuelve por plausibilidad. Todas las fuentes de carga son revisadas por pares salvo donde se indica *(preprint, no revisado)*. Ordenado por severidad.

---

## A2 · La colapsabilidad de la diferencia de proporciones (Punto 2)

**VEREDICTO — SE SOSTIENE.**

**EVIDENCIA.** El defecto no es qué es colapsable —eso está bien— sino qué *autoriza* la colapsabilidad. Definición formal (Greenland, Robins & Pearl, "Confounding and Collapsibility in Causal Inference," *Statistical Science* 14(1):29–46, 1999, DOI 10.1214/ss/1009211805): una medida M es colapsable si el valor marginal iguala al de los estratos *siempre que no haya confusión por C **ni modificación de efecto de M por C***. Garantiza igualdad marginal↔condicional bajo **dos** condiciones ausentes, no una. La razón de riesgos y la diferencia de riesgos son colapsables; el momio y el hazard ratio no (Miettinen & Cook 1981; Greenland 1996; confirmado en Greenland, "Noncollapsibility, confounding, and sparse-data bias. Part 1," *J Clin Epidemiol* 2021).

De ahí el salto. El autor escribe: *reversión → "confusión o modificación de efecto, no artefacto"*. Pero la colapsabilidad solo excluye **un** artefacto —el de la escala (la no-colapsabilidad de la propia medida)— y no los artefactos **inducidos por el condicionamiento**:

- **Sesgo de selección / colisionador.** Condicionar sobre un descendiente del tratamiento o sobre un colisionador *induce* asociación no causal (Hernán, Hernández-Díaz & Robins, "A structural approach to selection bias," *Epidemiology* 15:615–625, 2004). No es confusión ni modificación de efecto: es un tercer mecanismo estructural, y **sí es un artefacto**. La diferencia de riesgos, aun colapsable, no protege contra él.
- **Error de medición diferencial** y **agregación/ponderación diferencial entre celdas**: dos rutas más por las que marginal y condicional divergen sin que la divergencia sea "señal".

**Lo que lo hace bloqueante: el documento se contradice.** El Punto 2 afirma que la reversión "es señal, no artefacto". El Punto 3 afirma que `formalidad` e `ingreso` son candidatos a **descendiente o colisionador** y que condicionar sobre ellos "puede ser sobrecontrol". Si el Punto 3 tiene razón, la reversión del Punto 2 puede ser exactamente el artefacto de selección que el Punto 2 declara imposible. Ambas no pueden ser ciertas como están escritas.

Sub-pregunta 4 (diseño muestral complejo): la colapsabilidad es propiedad de la *medida*, no del *estimador*; los ponderadores no la alteran, pero agregan otra ruta de divergencia (el marginal es promedio ponderado por diseño; la ponderación diferencial entre celdas hace marginal ≠ promedio ingenuo de condicionales). Refuerza el defecto, no lo rescata.

Procedencia: el documento ancla esta sección en un preprint de arXiv y un blog personal (Schnitzer). La afirmación es correcta, pero la fuente canónica revisada por pares es Greenland-Robins-Pearl 1999.

**SEVERIDAD — bloqueante** para "eso sí es señal —confusión o modificación de efecto—, no artefacto". Non sequitur, verificable sin abrir archivos, e incoherente con el Punto 3.

**QUÉ HABRÍA QUE HACER.** Reescribir: *"Con diferencia de proporciones (colapsable) la reversión no es artefacto de la escala. Pero sigue siendo compatible con (a) confusión, (b) modificación de efecto, (c) sesgo de selección/colisionador por condicionar sobre los ejes que el §3 marca como post-exposición, y (d) error de medición diferencial. La colapsabilidad localiza la pregunta; no la responde."* Resolver la contradicción con el §3.

---

## A1 · El salto de Maxwell-Delaney (Punto 4)

**VEREDICTO — SE SOSTIENE DEBILITADO** (con la resolución empírica marcada como **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**).

**EVIDENCIA.** Lo que el paper *sí* dice, en su alcance. Maxwell & Delaney, "Bivariate median splits and spurious statistical significance," *Psychological Bulletin* 113(1):181–190, 1993 (DOI 10.1037/0033-2909.113.1.181). Enunciado real (resumen del propio paper y revisión secundaria en *J Experimental Psychopathology* 2(2):197–209): la categorización artificial infla el error tipo I **para el test de la interacción entre dos predictores categorizados en un ANOVA multifactorial**, si están correlacionados y uno está *no relacionado con, o tiene relación no lineal con,* el desenlace. Vargha, Rudas, Delaney & Maxwell (1996) lo extienden a cuando **solo uno** se categoriza. (La condición real es "no relacionado **o** no lineal"; la lista del documento estrecha esto en dirección conservadora, así que no es el defecto.)

El defecto es el marcado con ⚠️. El resultado está derivado para **(1)** desenlace **continuo** (ANOVA/medias) y **(2)** un **test formal del término de interacción**. El programa hace otra cosa: estratifica y estima **diferencias de proporciones** (desenlace **binario**) *dentro* de cada celda, y compara **signos** entre celdas.

- **"Formalmente" es el sobrealcance.** Una estimación estratificada saturada equivale a un modelo con todas las interacciones —en ese sentido "contiene" interacción—, pero la inflación de tipo I de M-D es un enunciado sobre **un test específico**, no sobre "reversión de signo descriptiva". Las "9 significativas" de X, si son pruebas de que cada celda ≠ 0, son tests de **efecto simple dentro de celda**, no del **contraste de interacción** entre celdas. Que el test de interacción tenga tipo I inflado no implica nada directo sobre tests de efecto simple. "Formalmente indistinguibles" no está sostenido por el paper.
- **La extensión a desenlace binario no está justificada.** El autor afirma "las cuatro se cumplen" sin abordar que la derivación asume DV continuo. Hay literatura de estimando para desenlaces binarios (p. ej. Fang & Jin, arXiv 2510.15000 — *preprint, no revisado por pares*), pero el resultado concreto de M-D no se ha trasladado al caso binomial en lo que el documento cita.

**REQUIERE VERIFICACIÓN CONTRA ARCHIVO:** que θ esté dicotomizada a ≥6, que θ→Y sea no monótona con pico en 4, que `formalidad/edad/ingreso` estén correlacionadas y *ellas mismas* categorizadas (no naturalmente binarias), y si las "9 significativas" son tests de interacción o de efecto simple. No lo resuelvo por plausibilidad.

Sub-pregunta 4 (diagnóstico publicado): sale de los propios papers. MacCallum, Zhang, Preacher & Rucker ("On the Practice of Dichotomization of Quantitative Variables," *Psychological Methods* 7(1):19–40, 2002, DOI 10.1037/1082-989X.7.1.19 — cifras del documento correctas: r .30→.21, r² .09→.04) señalan que una relación no lineal se representa con **regresión no lineal sobre la variable continua**, y que es la dicotomización la que la borra. Diagnóstico limpio: *no dicotomizar* — reestimar con θ continua/ordinal, ejes continuos, forma flexible y término producto θ×eje. Si la reversión **sobrevive**, no es el artefacto; si **desaparece**, lo era.

**SEVERIDAD — bloqueante** para "formalmente indistinguible de la firma de error tipo I inflado"; **declarable** para la cautela residual.

**QUÉ HABRÍA QUE HACER.** (1) Bajar "formalmente indistinguible" a "compatible con, no descartable sin más". (2) Añadir el paso diagnóstico: reestimar con θ continua y forma flexible antes de interpretar la reversión. (3) No presentar "las cuatro condiciones se cumplen" como hecho: dos son del archivo y una (desenlace continuo) no se cumple.

---

## A5 · Lo que no está en la lista

**VEREDICTO — SE SOSTIENE.** Tres hallazgos.

1. **Contradicción interna Punto 2 ↔ Punto 3 (bloqueante).** Ver A2. Es el hallazgo más valioso: no se puede sostener "la reversión es señal, no artefacto" (§2) y a la vez "condicionar sobre `formalidad/ingreso` puede ser sobrecontrol/colisionador" (§3), porque el segundo describe un artefacto que el primero declara imposible.

2. **Literatura de primera línea omitida (declarable→bloqueante vía punto 1).** Hernán, Hernández-Díaz & Robins, "A structural approach to selection bias," *Epidemiology* 15:615–625, 2004: el sesgo de selección/colisionador como bias *estructural* distinto de la confusión. Obliga a reescribir la dicotomía "señal vs. artefacto" del Punto 2.

3. **La recomendación obvia que el documento no da (declarable).** Todo el Punto 4 se apoya en MacCallum et al. 2002, cuya tesis es que *dicotomizar rara vez es defendible*. Sin embargo el documento trata la dicotomización de θ a ≥6 como fija y nunca recomienda estimar β sobre θ continua/ordinal. Dicotomizar y *luego* preocuparse por el artefacto de dicotomización es evitable si θ está medida 0–10.

**Verificación de relevancia:** el quinto atributo del Punto 1 informa una decisión de *manejo de datos*, no la decisión D-A de *admisión a coeficiente* (enlace/normalización/ajuste/universo). Correcto pero parcialmente desalineado con lo que D-A decide (ver A3).

**SEVERIDAD — bloqueante** (punto 1) / **declarable** (puntos 2 y 3).

**QUÉ HABRÍA QUE HACER.** Integrar el sesgo de selección en la taxonomía del §2; añadir "estimar sobre θ sin dicotomizar" como default cuando la escala lo permita; reubicar el quinto atributo como refinamiento del universo/manejo de datos.

---

## A4 · ¿Es exigible la justificación gráfica? (Punto 3)

**VEREDICTO — SE SOSTIENE DEBILITADO.**

**EVIDENCIA.** Cinelli, Forney & Pearl, "A Crash Course in Good and Bad Controls," *Sociological Methods & Research* 53(3):1071–1104, 2024 (DOI 10.1177/00491241221099552, revisado por pares). Es un tutorial gráfico sobre cuándo añadir una variable a una **ecuación de regresión** crea discrepancia entre el coeficiente y el efecto pretendido (sobrecontrol, malos controles), vía DAGs y puerta trasera. La atribución del autor es sustancialmente fiel — **no es "el paper no dice eso"**. Lo que el paper **no** exige es un DAG completo declarado como condición para llamar "coeficiente" a un resultado; eso lo agrega el autor.

El problema (⚠️): la recomendación "DAG declarado o rotúlalo asociación condicional" es **innecesariamente fuerte**, porque existe un criterio operable *sin* grafo completo. VanderWeele & Shpitser, "A New Criterion for Confounder Selection," *Biometrics* 67(4):1406–1413, 2011 (DOI 10.1111/j.1541-0420.2011.01619.x, revisado por pares): el **criterio de causa disyuntiva** está diseñado *"cuando la estructura causal subyacente es desconocida"* — requiere saber, por covariable, solo (i) si causa el tratamiento y (ii) si causa el desenlace, con las relaciones entre covariables *desconocidas*, y ajustar por toda covariable **pre-tratamiento** que cause a uno u otro. Si *algún* subconjunto observado basta para controlar confusión, el elegido por este criterio también basta. VanderWeele (2019), "Principles of confounder selection," *Eur J Epidemiol* 34(3):211–219: versión modificada (excluir instrumentos y variables de la trayectoria).

Esto resuelve la **circularidad** (sub-pregunta 2): el criterio disyuntivo no exige conocer el efecto investigado ni el grafo completo, solo el estatus causal cualitativo de cada covariable — exactamente lo que el §3 ya razona ("la mordida puede afectar el ingreso → el ingreso es post-exposición"). La objeción de circularidad es válida contra la versión fuerte y **se disuelve** contra la débil.

Sub-pregunta 4 (el caso *contra* el programa): existe y es fuerte. Ajustar por el conjunto equivocado pre-registrado puede ser **peor** que no ajustar — ajustar por un instrumento amplifica el sesgo por confusión no medida (Myers et al., *Am J Epidemiol* 174:1213–1222, 2011; Pearl, "On a class of bias-amplifying variables," UAI 2010); ajustar por un colisionador lo induce (Ding & Miratrix, *J Causal Inference* 3(1):41–57, 2015). La preocupación del §3 no solo es correcta: está subestimada.

**SEVERIDAD — declarable.** La cláusula sobrevive con límite escrito: preocupación válida, remedio demasiado binario.

**QUÉ HABRÍA QUE HACER.** Sustituir "DAG completo o no es coeficiente" por: *el conjunto de ajuste entra si (a) satisface el criterio de causa disyuntiva modificado, (b) se restringe a covariables pre-tratamiento excluyendo mediadores/instrumentos, y (c) se acompaña de análisis de sensibilidad a confusión no medida*. Grafo completo no exigible; "lo pre-registramos" tampoco basta.

---

## A3 · ¿Es E9(R1) el marco correcto? (Punto 1)

**VEREDICTO — SE SOSTIENE DEBILITADO.**

**EVIDENCIA.** Dos mitades con veredictos opuestos.

*El marco sí transfiere (esta mitad NO se sostiene).* El addendum declara que sus principios aplican también a estudios de un brazo y observacionales, y hay literatura revisada por pares que lo extiende: Chen et al., "Estimands in Real-World Evidence Studies," *Statistics in Biopharmaceutical Research* 16(2), 2024 (DOI 10.1080/19466315.2023.2259829); capítulo Springer "Estimand in Real-World Evidence Study" (2023), que confirma los cinco atributos —población, tratamiento, endpoint, eventos intercurrentes, resumen poblacional— y advierte que RWE "podría requerir consideraciones adicionales". El autor no importó un estándar donde no aplica. El mapeo tampoco está forzado en lo esencial: "normalización de θ" como contraste de exposición y "enlace/forma" como medida-resumen son defendibles.

*El análogo de "eventos intercurrentes" sí está estirado (esta mitad SÍ se sostiene).* Los eventos intercurrentes son **post-basales/temporales** por definición y —dato decisivo, en fuente revisada por pares (re-evaluación de estimandos en depresión, PMC9543408)— *deben distinguirse de datos que no existen*. El documento mapea "no-aplicabilidad estructural" (la pregunta no existió; campo en blanco) al atributo de eventos intercurrentes, pero eso es precisamente "datos que no existen", que la literatura separa de ese atributo. En datos transversales sin seguimiento no hay eventos intercurrentes en sentido técnico; el fenómeno pertenece al atributo **población/universo** o a cobertura/faltantes.

**SEVERIDAD — declarable.** La recomendación de declarar estrategia para no-aplicabilidad estructural vs. no-respuesta es sólida; solo no debe venderse como "el atributo de eventos intercurrentes".

**QUÉ HABRÍA QUE HACER.** Mantener el quinto requisito, re-etiquetado: refinamiento del atributo *población/universo* (o atributo separado de cobertura/faltantes), no análogo de eventos intercurrentes. La distinción no-aplicabilidad-estructural vs. no-respuesta se conserva.

---

## Cierre — qué queda en pie tal como está escrito

- **Punto 1 (E9(R1)):** en pie con enmienda menor. El marco transfiere; re-etiquetar el quinto atributo.
- **Punto 2 (colapsabilidad):** **no queda en pie.** "Reversión colapsable ⟹ señal, no artefacto" es non sequitur y contradice al §3. Defecto más grave del documento.
- **Punto 3 (justificación gráfica):** en pie en su diagnóstico (sobrecontrol real, incluso subestimado); remedio demasiado fuerte; sobrevive rebajado al criterio de causa disyuntiva + sensibilidad.
- **Punto 4 (Maxwell-Delaney):** en pie como *cautela*, no como *conclusión*. "Formalmente indistinguible de artefacto" no está sostenido (desenlace binario, test-vs-descripción); la operación efectiva del artefacto **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**.

Un solo hilo conecta A2, A4 y A5: el documento trata "confusión" y "modificación de efecto" como el universo de causas de una reversión, y deja fuera el sesgo de selección/colisionador — que su propio §3 introduce sin reconciliarlo con el §2. Cerrar esa brecha arregla tres de los cinco ataques a la vez.
