# RED TEAM A — Auditoría adversarial de los benchmarks de mesa

**Alcance ejercido.** Se verificó solo lo verificable sin el repositorio: si el autor enunció bien las *condiciones* de los papers que cita. Todo lo que dependía de los archivos del programa (forma real de θ→Y, si los ejes están categorizados y correlacionados, si las 9 celdas significativas provienen de una prueba de interacción, qué significa "normalización de θ" en la ficha) queda marcado como **REQUIERE VERIFICACIÓN CONTRA ARCHIVO** y no se resolvió por plausibilidad.

Orden por severidad, no por el orden de entrada.

---

## A5 · La contradicción interna entre Punto 2 y Punto 4 — el hallazgo más consecuente

**VEREDICTO: SE SOSTIENE.**

Es el defecto que ninguno de los cuatro ataques nombrados captura y el más grave del documento. El mismo resultado archivado —la reversión marginal→condicional de X— recibe dos veredictos incompatibles:

- **Punto 2:** "cuando X encontró que el marginal se invierte al condicionar, eso sí es señal —confusión o modificación de efecto—, **no artefacto**."
- **Punto 4:** "Lo que X llamó 'reversión de signo en 33 de 39 celdas' es formalmente **indistinguible**, con este diseño, de la firma de error tipo I inflado."

Uno afirma "no es artefacto"; el otro, "es indistinguible de un artefacto". Sobre el objeto central de todo el análisis, el documento sostiene las dos cosas.

**EVIDENCIA — por qué es contradicción real y no aparente.** La reconciliación existe pero el autor nunca la escribe, y sin escribirla el Punto 2 queda mal. La colapsabilidad (Punto 2) es propiedad de la *medida* calculada sobre las variables *verdaderas*. El artefacto de dicotomización (Punto 4) opera sobre θ *ya dicotomizada*: la "diferencia de proporciones" del programa es la RD de una exposición dicotomizada, cantidad distinta de la RD de θ continua. La colapsabilidad de la medida **no protege** contra el sesgo de dicotomizar. Los dos enunciados son lógicamente compatibles (uno excluye el artefacto de no-colapsabilidad; el otro introduce el de dicotomización), pero el Punto 2 no dice "no es *ese* artefacto" sino "no artefacto" sin calificar — y eso es falso a la luz del propio Punto 4.

**SEVERIDAD: bloqueante.** La decisión que todo el documento informa —qué hacer con la reversión archivada— depende de resolver esto, y el documento la deja abierta en dos direcciones opuestas.

**QUÉ HABRÍA QUE HACER.** Reescribir el Punto 2 para que su conclusión diga solo lo que la colapsabilidad autoriza: "la reversión no es artefacto de la medida (no-colapsabilidad); queda por descartar que sea artefacto de la dicotomización, de selección o de medición". Con eso el Punto 2 y el Punto 4 dejan de contradecirse y se encadenan.

---

## A1 · El salto de Maxwell-Delaney (Punto 4)

**VEREDICTO: SE SOSTIENE** (con una parte que **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**).

**EVIDENCIA.**

*La paráfrasis de las condiciones NO es el defecto — hay que decirlo.* Maxwell & Delaney (1993, *Psychological Bulletin* 113(1):181–190, DOI 10.1037/0033-2909.113.1.181) demostraron que se inflan las tasas de error tipo I para la prueba de interacción entre dos variables categorizadas si están correlacionadas entre sí y una tiene relación nula o no lineal con el desenlace. Vargha, Rudas, Delaney & Maxwell (1996, *Journal of Educational and Behavioral Statistics* 21:264–282, DOI 10.2307/1165272) extendieron el resultado al caso en que solo una de las dos variables se dicotomiza. Las cuatro condiciones que el autor lista (θ dicotomizada, θ→Y no lineal, predictores correlacionados, se prueban interacciones) **son paráfrasis fiel**, no alterada. La acusación "el paper no dice eso" **no** aplica aquí.

*El defecto está en el salto, y es doble.* Ambos papers trabajan sobre **regresión/ANOVA con desenlace continuo y término producto (X₁·X₂)**. El mecanismo, según MacCallum, Zhang, Preacher & Rucker (2002, *Psychological Methods* 7(1):19–40, DOI 10.1037/1082-989X.7.1.19), es que tras dicotomizar dos predictores el ANOVA rinde una interacción significativa como mera representación errónea de la no linealidad del efecto directo. El programa hace dos cosas que esos papers no cubren:

1. **Desenlace binario, no continuo.** El resultado de inflación se deriva y simula para desenlace continuo. El programa estima diferencias de proporciones (binario). Los papers citados no establecen que la inflación transfiera al caso binario; el autor la transfiere sin puente.
2. **Estratificar-y-estimar-por-celda no es el término producto del paper.** La firma que describen es una *prueba de interacción espuriamente significativa*. El programa reporta un *conteo de reversiones de signo* (33/39). Error tipo I es falsa *significancia*: lo homologable serían las **9 celdas significativas**, no las 33 reversiones. El autor equipara "reversión" con "firma de tipo I", y no son la misma estadística.

Por eso "formalmente indistinguible" no está licenciado por la literatura citada: es un salto de "el paper describe un artefacto en un diseño vecino" a "este resultado ES indistinguible de ese artefacto".

*Lo que requiere el archivo:* si θ→Y es no monótona con pico en 4, si los ejes están categorizados y correlacionados, y si las 9 significativas provienen de una prueba de interacción — **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**.

*Prueba diagnóstica (lo más valioso).* Existe, y es la que la propia literatura recomienda: **reestimar con θ en forma continua** (o con términos flexibles/spline que capturen el pico en 4) e incluir la interacción θ×estrato. El mecanismo predice que la interacción *desaparece* al modelar la no linealidad. Si la reversión **persiste** con θ continua, no es el artefacto de dicotomización; si **se desvanece**, lo era. Esa prueba hoy no está corrida.

**SEVERIDAD: bloqueante** para "formalmente indistinguible" (bajarla a "no puede descartarse sin reanálisis con θ continua"); **declarable** para la alarma de fondo (dicotomizar una θ no monótona es preocupación legítima que sobrevive).

**QUÉ HABRÍA QUE HACER.** Sustituir "formalmente indistinguible" por el reanálisis con θ continua como condición de entrada. Hasta correrlo, la reversión no es interpretable ni como señal ni como artefacto.

---

## A2 · La colapsabilidad de la diferencia de proporciones (Punto 2)

**VEREDICTO: SE SOSTIENE.**

**EVIDENCIA.**

*Lo que el autor tiene bien:* la no-colapsabilidad del momio y del hazard ratio, y que RD y RR sí son colapsables, es correcto. Greenland, Robins & Pearl (1999, *Statistical Science* 14(1):29–46, DOI 10.1214/ss/1009211805) establecen que la diferencia de riesgos es estrictamente colapsable, mientras el momio no. Esa parte del Punto 2 es correcta.

*Primer defecto — "colapsable ⟹ no artefacto" es un non-sequitur.* La colapsabilidad significa que marginal y estrato-específico coinciden **cuando no hay confusión y no hay modificación de efecto** (Greenland-Pearl-Robins 1999; Whittemore 1978). Por contrapositiva, si difieren, la causa es *algo real* — pero "algo real" incluye **selección (condicionar sobre un colisionador), error de medición diferencial entre estratos, y el propio artefacto de dicotomización del Punto 4**, ninguno de los cuales es "confusión o modificación de efecto". La colapsabilidad excluye **un** artefacto (el de la medida); no autoriza "no artefacto" a secas. El autor cerró la lista de causas a dos cuando son al menos cinco.

*Segundo defecto — "modificación de efecto" no puede voltear el signo.* Bajo no-confusión, la RD marginal es un promedio ponderado convexo de las RD por estrato. Una combinación convexa de negativos es negativa: **no puede** tener signo opuesto a todas ellas. Una reversión genuina de signo implica **confusión (o selección)**, no modificación de efecto. Incluir "modificación de efecto" como causa de la reversión es un error técnico.

*Tercer punto — el enunciado "colapsable" necesita calificación.* Afirmar en abstracto "la diferencia de riesgos es colapsable" es dependiente de escala y condiciones. La frase "las medidas de la mayoría de los GLM son colapsables" es imprecisa: entre enlaces comunes, identidad (RD) y log (RR) son colapsables; logit (OR) y Cox (HR) no. Es mitad y mitad, no "la mayoría". (Cosmético.)

*Diseño muestral complejo:* los ponderadores definen cuál "marginal" se compara y pueden incrustar selección vía ajuste de no-respuesta; no rescatan la colapsabilidad de las amenazas de selección/medición. El detalle concreto **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**.

**SEVERIDAD: bloqueante** para "sí es señal … no artefacto" (otra cara de A5); **declarable** para el desliz de "modificación de efecto"; **cosmético** para "la mayoría de los GLM". La *recomendación* del Punto 2 (declarar colapsabilidad por coeficiente) es correcta y sobrevive intacta.

**QUÉ HABRÍA QUE HACER.** Reemplazar "confusión o modificación de efecto, no artefacto" por: "confusión, selección o medición diferencial — la colapsabilidad solo excluye el artefacto de no-colapsabilidad de la medida; la modificación de efecto por sí sola no invierte el signo agregado".

---

## A4 · ¿Es exigible la justificación gráfica? (Punto 3)

**VEREDICTO: SE SOSTIENE DEBILITADO.**

**EVIDENCIA.**

*Lo que el autor tiene bien:* Cinelli, Forney & Pearl (2024, *Sociological Methods & Research* 53(3):1071–1104, DOI 10.1177/00491241221099552) dicen lo que se les atribuye: taxonomía de buenos/malos controles vía DAG, y sí sostienen que no todo control post-tratamiento es malo (p. ej. explotan la puerta delantera). Que un mal control pre-registrado sigue siendo malo es correcto, y el diagnóstico de que formalidad e ingreso pueden ser descendientes/colisionadores de la experiencia de mordida es sólido.

*El defecto — la recomendación es innecesariamente fuerte y omite literatura de primera línea.* El autor plantea la dicotomía "DAG declarado completo, o el resultado se rotula 'mera asociación'". Existe una vía operable intermedia que no cita: el **criterio de causa disyuntiva** (VanderWeele & Shpitser 2011, *Biometrics* 67(4):1406–1413; VanderWeele 2019, *European Journal of Epidemiology* 34(3):211–219), diseñado precisamente para cuando la estructura causal se desconoce y solo hay conocimiento limitado. Selecciona las covariables pre-tratamiento que son causa de la exposición, del desenlace o de ambos; excluye instrumentos; e incluye proxies de causas comunes no medidas, con la propiedad de que el conjunto elegido es suficiente si algún subconjunto de lo observado lo es. Requiere saber, por covariable, si es pre-tratamiento y si causa exposición o desenlace — no el grafo completo. Hay alternativas operables, así que exigir un DAG completo es más fuerte de lo que el estado del arte pide.

*Matiz que debilita también el ataque:* el criterio disyuntivo **igual** exige resolver si formalidad/ingreso son pre- o post-tratamiento — justo lo contencioso. Así que "ningún análisis podría cumplir el requisito" es demasiado fuerte en la otra dirección: el DAG completo se evita, pero *algún* supuesto estructural (pre/post) es ineludible para cualquier ajuste causal.

*El caso contra el programa:* existe. Ajustar a ciegas puede ser **peor que no ajustar**: controlar un colisionador o un instrumento amplifica sesgo (VanderWeele 2019, sobre amplificación por instrumentos; Ding & Miratrix 2015, *Journal of Causal Inference* 3(1):41–57, sobre M-bias). Esto respalda el núcleo del autor (pre-registro ≠ validez), no lo refuta.

**SEVERIDAD: declarable.** La recomendación sobrevive en forma modificada.

**QUÉ HABRÍA QUE HACER.** Cambiar "DAG declarado o mera asociación" por: "justificación causal por covariable vía criterio de causa disyuntiva (estatus pre-tratamiento + causa de exposición/desenlace), más análisis de sensibilidad a confusión omitida (E-values, sensemakr)". Reservar "mera asociación" para cuando ni eso pueda declararse.

---

## A3 · ¿Es E9(R1) el marco correcto? (Punto 1)

**VEREDICTO: NO SE SOSTIENE** en su forma fuerte; **SE SOSTIENE DEBILITADO** solo en la analogía de eventos intercurrentes.

**EVIDENCIA.**

*El cargo principal falla.* "El autor importó un estándar de ensayos clínicos donde no aplica" no se sostiene, porque el propio addendum lo desmiente: afirma que sus principios también son aplicables a ensayos de un solo brazo y estudios observacionales, aunque construir estimandos para RWE requiera consideraciones adicionales (revisión de estimandos en RWE, Springer 2023; Rippin 2024, *Frontiers in Drug Safety and Regulation*, DOI 10.3389/fdsfr.2023.1332040). Los cinco atributos que el autor lista (población, tratamiento, variable, eventos intercurrentes, resumen poblacional) están correctos, y su lectura de la innovación de E9(R1) —convertir el enlace/resumen en atributo definitorio del estimando y conectar población con método— es fiel.

*Lo que sí se sostiene, debilitado:* el análogo de "eventos intercurrentes" en datos transversales es estirado. Por definición son eventos que ocurren después del inicio del tratamiento y afectan la interpretación o la existencia de las mediciones — inherentemente temporales/post-línea-base. En una encuesta de hogares sin seguimiento, θ y Y son contemporáneos: no hay "después del tratamiento". El autor los mapea a "no-aplicabilidad estructural" (preguntas que no existieron). Captura el aspecto de *existencia del dato* (que tiene análogo en la truncación por muerte de E9(R1)), pero pierde el núcleo *temporal/post-tratamiento*. Analogía parcial, no falsa.

*Requiere archivo:* si "normalización de θ declarada" es de verdad el análogo del atributo *tratamiento* (contraste de exposición por el corte) o una correspondencia forzada, depende de la ficha. **REQUIERE VERIFICACIÓN CONTRA ARCHIVO.**

**SEVERIDAD: cosmético/declarable.** La recomendación (añadir un requisito de no-aplicabilidad estructural) es buena y coincide con lo que la literatura RWE pide (atributos adicionales); solo hay que reetiquetarla como *atributo adicional para datos transversales*, no como "el análogo de eventos intercurrentes".

**QUÉ HABRÍA QUE HACER.** Mantener el quinto requisito, pero presentarlo como extensión propia del marco observacional (no como mapeo directo del atributo de eventos intercurrentes), citando que el addendum ya prevé consideraciones adicionales para estudios observacionales.

---

## Cierre — qué queda en pie tal como está escrito

- **Punto 1 (E9-R1):** en pie. El marco transfiere (el addendum lo dice), los cinco atributos están bien y la recomendación es sólida; solo reetiquetar la analogía de eventos intercurrentes.
- **Punto 2 (colapsabilidad):** **no** queda en pie. La conclusión "sí es señal, no artefacto" es un non-sequitur y contradice al Punto 4; hay que calificarla. La recomendación de declarar colapsabilidad por coeficiente sí queda.
- **Punto 3 (controles):** en pie en sustancia, pero la recomendación es demasiado fuerte: hay que ofrecer el criterio de causa disyuntiva y el análisis de sensibilidad como vía intermedia.
- **Punto 4 (dicotomización):** **no** queda en pie tal como está. La paráfrasis de las condiciones es fiel, pero "formalmente indistinguible" no está licenciado (desenlace binario y estratificación no son el marco continuo/término-producto de los papers) y debe bajarse a hipótesis a dirimir con θ continua.

El defecto mayor no es ninguno de los cuatro por separado, sino que Puntos 2 y 4 emiten veredictos opuestos sobre el mismo resultado (A5). Corregir eso reordena todo lo demás.

---

## Referencias verificadas

- Maxwell, S. E., & Delaney, H. D. (1993). Bivariate median splits and spurious statistical significance. *Psychological Bulletin*, 113(1), 181–190. DOI 10.1037/0033-2909.113.1.181. [revisado por pares]
- Vargha, A., Rudas, T., Delaney, H. D., & Maxwell, S. E. (1996). Dichotomization, partial correlation, and conditional independence. *Journal of Educational and Behavioral Statistics*, 21, 264–282. DOI 10.2307/1165272. [revisado por pares]
- MacCallum, R. C., Zhang, S., Preacher, K. J., & Rucker, D. D. (2002). On the practice of dichotomization of quantitative variables. *Psychological Methods*, 7(1), 19–40. DOI 10.1037/1082-989X.7.1.19. [revisado por pares]
- Greenland, S., Robins, J. M., & Pearl, J. (1999). Confounding and collapsibility in causal inference. *Statistical Science*, 14(1), 29–46. DOI 10.1214/ss/1009211805. [revisado por pares]
- Cinelli, C., Forney, A., & Pearl, J. (2024). A Crash Course in Good and Bad Controls. *Sociological Methods & Research*, 53(3), 1071–1104. DOI 10.1177/00491241221099552. [revisado por pares]
- VanderWeele, T. J., & Shpitser, I. (2011). A new criterion for confounder selection. *Biometrics*, 67(4), 1406–1413. [revisado por pares]
- VanderWeele, T. J. (2019). Principles of confounder selection. *European Journal of Epidemiology*, 34(3), 211–219. [revisado por pares]
- Ding, P., & Miratrix, L. W. (2015). To adjust or not to adjust? Sensitivity analysis of M-bias and butterfly bias. *Journal of Causal Inference*, 3(1), 41–57. [revisado por pares]
- ICH E9(R1) (2019). Addendum on estimands and sensitivity analysis to the guideline on statistical principles for clinical trials. [guía regulatoria]
- Rippin, G. (2024). External comparators and estimands. *Frontiers in Drug Safety and Regulation*. DOI 10.3389/fdsfr.2023.1332040. [revisado por pares]

*Nota: no se citó ningún preprint de arXiv como fuente de autoridad; los enunciados provienen de las versiones publicadas y revisadas por pares arriba listadas.*
