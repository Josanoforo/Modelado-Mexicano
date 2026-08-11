> **NOTA DE RECUPERACIÓN · 11/ago/2026.** Este documento existía solo en el espejo del proyecto; el encargo del motor adaptativo lo citó y la Ronda 1 lo clasificó NO-ENCONTRADO en repo (universo: árbol + git log --all). Entra verbatim desde el espejo — procedencia tipo (2), sin sello de commit de origen. sha256 del original en espejo: 8bae9213559d33a143f881968eda87da2f6fe38b24243c92518c9496dc3ec995. Resolución M0 de mesa, 11/ago/2026. Su contenido NO se edita.

# Auditoría adversarial — análisis de benchmarks de mesa

**Alcance.** Solo se juzga si el autor enunció bien las *condiciones* de los papers citados. Lo que dependa de los archivos del programa se marca **REQUIERE VERIFICACIÓN CONTRA ARCHIVO**. Los cuatro papers metodológicos centrales están revisados por pares; se marcan como preprints no revisados arXiv:2307.00190 y arXiv:2310.15131.

Ordenado por severidad.

---

## A1 · El salto de Maxwell-Delaney (Punto 4)

**VEREDICTO: SE SOSTIENE** (con una sub-parte marcada REQUIERE VERIFICACIÓN CONTRA ARCHIVO)

**EVIDENCIA.**
Los papers están bien identificados y las *condiciones* están parafraseadas de forma defendible — no es un caso de "el paper no dice eso".

- Maxwell, S. E. & Delaney, H. D. (1993), *Bivariate median splits and spurious statistical significance*, Psychological Bulletin 113(1):181-190, DOI 10.1037/0033-2909.113.1.181. Condición real: hay tasas infladas de error tipo I **para la prueba de la interacción entre las dos variables categorizadas** si están correlacionadas entre sí y **al menos una tiene relación no lineal con —o no está relacionada con— la variable de desenlace**.
- Vargha, Rudas, Delaney & Maxwell (1996), *Dichotomization, Partial Correlation, and Conditional Independence*, Journal of Educational and Behavioral Statistics 21(2):264-282. Extiende: el efecto espurio ocurre incluso cuando **solo una** de las dos se dicotomiza.
- MacCallum, Zhang, Preacher & Rucker (2002), Psychological Methods 7(1):19-40, DOI 10.1037/1082-989X.7.1.19. Reformulación más precisa: la interacción espuria aparece cuando hay **efectos no lineales directos** de X₁ y/o X₂ sobre Y **pero ninguna interacción en el modelo de regresión**, y el ANOVA posterior a la dicotomización la produce como *tergiversación de la no linealidad de un efecto principal*. (Los números que cita el autor — r de .30 a .21 y r² de .09 a .04 — se confirman literalmente en el artículo.)

El defecto **no** es "el paper no lo dice" sino "lo dice pero no aplica tal como el autor lo transfiere", por dos razones verificables desde los papers:

1. **Procedimiento distinto.** El resultado formal de M-D/Vargha es sobre el **coeficiente de interacción (término producto X₁·X₂) en un único modelo lineal/ANOVA factorial** sobre desenlace **continuo**. El programa no ajusta un término producto ni testea su coeficiente: estratifica en 39 celdas y estima diferencias de proporciones *dentro* de cada celda, luego cuenta reversiones de signo. "33/39 celdas invierten el signo" es una lectura de heterogeneidad del efecto de θ entre estratos — emparentada con una interacción, pero **no es la prueba del coeficiente de interacción a cuya tasa de error tipo I se refiere el teorema**. La equivalencia entre ambos procedimientos no está establecida por ninguno de los papers citados.
2. **Desenlace binario.** Toda la derivación de M-D y Vargha vive en el modelo lineal normal (Y continuo). El programa tiene Y binario y estimador de diferencia de proporciones. **Ningún paper citado establece que la inflación de error tipo I se traslade a ese caso.**

Por eso "formalmente indistinguible" es la palabra que no se sostiene: no hay resultado *formal* que cubra el procedimiento y el desenlace del programa.

**REQUIERE VERIFICACIÓN CONTRA ARCHIVO:** que la curva θ→Y sea no monótona con pico en 4, que los tres ejes estén correlacionados entre sí y con θ, y qué prueba produjo las "9 significativas". El autor admite haber derivado las cuatro condiciones de las *notas del programa*, no de los datos.

**SEVERIDAD: bloqueante** para la afirmación tal como está escrita. La versión salvable ("la dicotomización de θ con pico interno más ejes correlacionados es un riesgo real que hay que descartar") es apenas **declarable**.

**QUÉ HABRÍA QUE HACER.** Sustituir "formalmente indistinguible" por "no descartable sin re-estimar". El diagnóstico existe y sale de esta misma literatura: **re-estimar sin dicotomizar**, con θ y los ejes en forma continua y forma funcional flexible (splines/polinomios), sobre un GLM apropiado al desenlace binario; si la reversión sobrevive al modelado explícito de la no linealidad, no es el artefacto de M-D. No hay un "test con nombre" único; el remedio canónico de MacCallum et al. (retener la forma continua) *es* la prueba diagnóstica.

---

## A5 · Lo que no está en la lista — la contradicción interna

**VEREDICTO: SE SOSTIENE** (hallazgo no cubierto por A1–A4)

**EVIDENCIA.** El documento afirma tres cosas incompatibles con la confianza con que las afirma:

- **Punto 2** concluye que la reversión de 33/39 celdas "sí es señal —confusión o modificación de efecto—, no artefacto".
- **Punto 3** advierte que condicionar sobre formalidad e ingreso "puede ser sobrecontrol" (sesgo de colisionador/descendiente).
- **Punto 4** advierte que la misma reversión es "formalmente indistinguible" de un artefacto de dicotomización.

Los Puntos 3 y 4 ofrecen, cada uno, un mecanismo de **artefacto** que produce exactamente la reversión que el Punto 2 declara **genuina**. No pueden sostenerse los tres al nivel de confianza escrito. La resolución la fija la definición de colapsabilidad (Greenland, Robins & Pearl, 1999, *Confounding and Collapsibility in Causal Inference*, Statistical Science 14(1):29-46, DOI 10.1214/ss/1009211805; formulación de Rothman-diagrams, arXiv:2310.15131, **preprint no revisado**): una medida colapsable iguala marginal y estratos *cuando no hay confusión ni modificación de efecto* — de modo que la colapsabilidad **solo descarta el artefacto de escala (no-colapsabilidad), no los demás**. La reversión sigue pudiendo venir de colisionador/selección (Punto 3) o de dicotomización (Punto 4). El Punto 2 no establece "señal genuina"; establece solo "no es artefacto de no-colapsabilidad".

**Literatura de primera línea omitida que cambiaría el Punto 1 (y el encuadre entero):**

- **Emulación de ensayo objetivo** — Hernán & Robins (2016), *Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available*, Am J Epidemiol 183(8):758-764, DOI 10.1093/aje/kwv254; síntesis en Hernán, Dahabreh, Dickerman & Swanson (2025), Ann Intern Med 178:402-407. Para una pregunta causal en datos observacionales es el marco de referencia y obliga a fijar *tiempo cero*, elegibilidad y asignación — donde una encuesta transversal sin seguimiento cruje. El propio paper aclara: la emulación resuelve problemas de diseño, no de limitación de datos.
- **Estimandos en evidencia de mundo real** — Chen et al., *Estimands in Real-World Evidence Studies*, arXiv:2307.00190 (**preprint no revisado**); capítulo Springer DOI 10.1007/978-3-031-26328-6_9, que especifica qué atributos hay que modificar al salir del ECA.

**SEVERIDAD: bloqueante** para la conclusión central del Punto 2; **declarable** para las omisiones del Punto 1.

**QUÉ HABRÍA QUE HACER.** Reescribir el Punto 2 como "la colapsabilidad de la diferencia de riesgos descarta que la reversión sea un artefacto *de escala*; no descarta colisionador, selección, error de medición diferencial ni dicotomización — ver Puntos 3 y 4". Anclar el Punto 1 en emulación de ensayo objetivo, no solo en E9(R1).

---

## A2 · La colapsabilidad de la diferencia de proporciones (Punto 2)

**VEREDICTO: SE SOSTIENE**

**EVIDENCIA.** Lo *factual* del Punto 2 es correcto: la diferencia de riesgos es colapsable (Greenland, Robins & Pearl, 1999, la llaman "estrictamente colapsable"), el momio y el hazard son no colapsables, y comparar marginal y condicional de una medida no colapsable es comparar parámetros distintos.

El salto es la inferencia final. Colapsable **no** implica "marginal = condicional"; implica que *si* difieren, la diferencia no es artefacto de la escala de la medida. De ahí a "sí es señal —confusión o modificación de efecto" hay un hueco: la definición iguala marginal y estratos solo en ausencia de confusión **y** de modificación de efecto, asumiendo estratos válidamente estimados. Quedan fuera, y el autor no los menciona:

1. **Sesgo de selección/colisionador inducido por el propio condicionamiento** (justo lo que teme su Punto 3).
2. **Error de medición diferencial.**
3. El **artefacto de dicotomización** del Punto 4.

Ninguno es "confusión o modificación de efecto" en el sentido del estimando, y todos producen la misma reversión.

Sobre el diseño muestral complejo: la colapsabilidad es propiedad del **estimando/medida**, no del estimador; ponderadores, estratos y UPM **no rompen** la colapsabilidad de la diferencia de riesgos. Sí cambian la población sobre la que se marginaliza y la varianza (efecto de diseño), pero eso es otra cosa. No requiere el archivo.

**SEVERIDAD: declarable.** La recomendación sobrevive con límite escrito: el autor tiene razón en que "marginales jamás entran" y en pedir que D-C declare colapsabilidad por coeficiente.

**QUÉ HABRÍA QUE HACER.** Cambiar "no artefacto" por "no artefacto *de no-colapsabilidad*", y enumerar las tres causas alternativas de reversión que la colapsabilidad **no** excluye, remitiendo a los Puntos 3 y 4.

---

## A4 · ¿Es exigible la justificación gráfica? (Punto 3)

**VEREDICTO: SE SOSTIENE DEBILITADO**

**EVIDENCIA.** La atribución es fiel: Cinelli, Forney & Pearl (2024), *A Crash Course in Good and Bad Controls*, Sociological Methods & Research 53(3):1071-1104, DOI 10.1177/00491241221099552 (en línea 2022). El autor dice casi textual lo que dicen: el criterio de puerta trasera "excluye controles que son descendientes del tratamiento por caminos hacia el desenlace" (Modelos 11-12) y "contra el folclore, no todas las variables post-tratamiento son malos controles" (Modelos 14-15). Sin tergiversación.

El ataque es a la **recomendación**, y tiene razón parcial. Exigir un **DAG declarado completo** o degradar a "asociación condicional sobre S" es más fuerte de lo que la literatura exige; existen criterios operables con conocimiento **parcial** del grafo:

- **VanderWeele & Shpitser (2011)**, *A New Criterion for Confounder Selection*, Biometrics 67(4):1406-1413, DOI 10.1111/j.1541-0420.2011.01619.x: el **criterio de causa disyuntiva** funciona "cuando la estructura causal subyacente es desconocida"; basta saber, por covariable, si es causa del tratamiento y/o del desenlace. Demuestran que si algún subconjunto observado basta para controlar confusión, el elegido por el criterio también basta.
- **VanderWeele (2019)**, *Principles of confounder selection*, Eur J Epidemiol: variante modificada (excluir instrumentos, incluir proxies de confusores no medidos).

Lo que **debilita el ataque** y en parte rescata al autor:

1. El criterio disyuntivo **asume covariables pre-tratamiento**; si formalidad e ingreso son **post-tratamiento** (la mordida afecta ingreso/situación laboral), no rescata nada — sigues necesitando el estatus pre/post.
2. Contra el programa: ajustar sin grafo puede ser **peor que no ajustar** — sesgo-M / *butterfly bias* al condicionar un colisionador pre-tratamiento (Ding & Miratrix, 2015, *To Adjust or Not to Adjust?*, Journal of Causal Inference 3(1):41-57). Un conjunto pre-registrado a ciegas puede *introducir* sesgo ausente sin ajuste — apoya el espíritu del Punto 3 aunque hunda su redacción absolutista.

Determinar si formalidad/ingreso son pre- o post-tratamiento **REQUIERE VERIFICACIÓN CONTRA ARCHIVO** (o input de dominio).

**SEVERIDAD: declarable.**

**QUÉ HABRÍA QUE HACER.** Suavizar de "DAG completo o no es coeficiente" a: "declarar, por covariable, (a) si es causa de la exposición y/o del desenlace y (b) si es pre- o post-exposición; con eso basta el criterio de causa disyuntiva — el grafo completo no es exigible". Mantener el veto solo para covariables post-exposición.

---

## A3 · ¿Es E9(R1) el marco correcto? (Punto 1)

**VEREDICTO: SE SOSTIENE DEBILITADO**

**EVIDENCIA.** Los cinco atributos están **enunciados correctamente** (población, tratamiento/condiciones comparadas, variable/desenlace, resumen a nivel poblacional, eventos intercurrentes) — coinciden con ICH E9(R1). La forma fuerte del ataque ("importó un estándar de ECA donde no aplica") **no se sostiene**: el propio addendum declara que sus principios aplican a estudios de un solo brazo y **observacionales** (confirmado en la literatura de estimandos RWE, capítulo Springer DOI 10.1007/978-3-031-26328-6_9). No es préstamo ilegítimo.

Lo que **sí** se sostiene son dos costuras:

1. **El análogo de "eventos intercurrentes" está estirado.** Un evento intercurrente es, por definición, un evento **post-línea-base que afecta la existencia o interpretación del desenlace** (muerte, cambio de tratamiento, rescate). En datos **transversales sin seguimiento** no hay ese eje temporal. El autor lo mapea a "no-aplicabilidad estructural" (la pregunta que no existió, el campo en blanco), pero E9(R1) **distingue explícitamente** los eventos intercurrentes de los "datos que no existen" — que es lo que es un "sin contacto". Se conflaciona una categoría con otra que el estándar mantiene aparte.
2. **"normalización de θ = atributo TRATAMIENTO" es correspondencia forzada al menos en parte.** El atributo tratamiento especifica las *condiciones comparadas*; mapear el corte de θ a "contraste de exposición" es defendible, pero θ es un constructo psicosocial **no manipulable**, y llamarlo "tratamiento" importa el supuesto de manipulabilidad ("no causation without manipulation"). No es fatal, pero no es limpio.

Omisión relevante (se cruza con A5): no cita la literatura de **estimandos en RWE** ni **emulación de ensayo objetivo**, donde está escrito qué hay que cambiar al sacar E9(R1) del ECA.

**SEVERIDAD: declarable.**

**QUÉ HABRÍA QUE HACER.** Conservar el mapeo de los cuatro atributos que sí calzan; **renombrar** el quinto requisito: no es "análogo de eventos intercurrentes" sino "estrategia declarada para **datos estructuralmente inexistentes** y no-respuesta, distinguiéndolas". Añadir una frase reconociendo que θ es exposición no manipulable.

---

## Cierre — qué queda en pie tal como está escrito

De los cuatro puntos, **ninguno sobrevive intacto**, pero se dividen limpio:

- **Punto 1 (E9(R1))** — en pie **con límite escrito**: los cinco atributos y la transferencia a lo observacional son correctos; renombrar el "quinto requisito" y añadir emulación de ensayo objetivo / estimandos RWE.
- **Punto 2 (colapsabilidad)** — su **conclusión central no queda en pie**: lo factual es correcto, pero "sí es señal, no artefacto" debe reducirse a "no es artefacto *de no-colapsabilidad*", y queda contradicho por los Puntos 3 y 4.
- **Punto 3 (malos controles)** — en pie **con límite escrito**: la cita a Cinelli-Forney-Pearl es fiel; la recomendación de DAG completo es innecesariamente fuerte y debe bajarse a criterio de causa disyuntiva + estatus pre/post.
- **Punto 4 (dicotomización)** — su **afirmación de cierre no queda en pie**: números y citas correctos, pero "formalmente indistinguible" no está sostenido para desenlace binario ni para el procedimiento estratificado del programa.

Un solo defecto atraviesa tres de los cuatro: **el documento trata la reversión de 33/39 como cosas distintas en los Puntos 2, 3 y 4 sin reconciliarlas** — señal genuina, artefacto de colisionador y artefacto de dicotomización — y la colapsabilidad, que es su ancla, solo cierra una de las tres puertas.
