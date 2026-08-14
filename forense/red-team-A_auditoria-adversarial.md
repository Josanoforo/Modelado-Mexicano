# RED TEAM A — Auditoría adversarial del análisis de benchmarks de mesa

**Alcance:** revisor sin acceso al repositorio del programa. Solo se adjudica si el autor
enunció bien las **condiciones** de los papers que cita. Todo lo que exige ver los archivos
del programa se marca *REQUIERE VERIFICACIÓN CONTRA ARCHIVO* y no se resuelve por plausibilidad.

---

## Síntesis previa

El patrón del documento es consistente: **el autor enuncia bien las condiciones de casi todos
los papers, pero da un paso de más en la inferencia.** Con una excepción menor, no hay casos de
"el paper no dice eso". Los defectos son del tipo "el paper lo dice, pero el salto a la conclusión
no está autorizado por lo que el paper cubre". El hallazgo más grave no está en ninguno de los
cuatro ataques originales: es una **contradicción interna** entre el Punto 2 y el Punto 4.

Orden de entrega: por severidad.

---

## A5 · Contradicción interna Punto 2 ↔ Punto 4 (lo que no estaba en la lista)

**VEREDICTO — SE SOSTIENE.** Es el hallazgo más consecuente.

**EVIDENCIA.** No requiere paper externo; es el propio texto. Sobre el *mismo* resultado archivado
de Encargo X (reversión de signo en 33/39 celdas), el documento afirma dos cosas incompatibles:

- **Punto 2:** "cuando X encontró que el marginal se invierte al condicionar, eso sí es señal
  —confusión o modificación de efecto—, **no artefacto**."
- **Punto 4:** "Lo que X llamó 'reversión de signo en 33 de 39 celdas' es formalmente
  **indistinguible**, con este diseño, de la firma de error tipo I inflado…" (es decir, artefacto).

El autor nunca reconcilia esto. La reconciliación existe y es lo que falta escribir: la
colapsabilidad (Punto 2) solo descarta **un** artefacto —el de no-colapsabilidad, propio del
momio/hazard— pero **no toca** el artefacto de inflación de error tipo I por dicotomización
(Punto 4), que opera por otro mecanismo (no-linealidad mal representada). Ambos "podrían ser
ciertos" porque hablan de artefactos distintos; pero las **conclusiones tal como están redactadas**
("no artefacto" vs. "indistinguible de artefacto") se contradicen de frente.

**SEVERIDAD — bloqueante** para cualquier lectura conjunta de los Puntos 2 y 4. Quien use el
documento para decidir sobre Encargo X recibe dos veredictos opuestos.

**QUÉ HABRÍA QUE HACER.** Escribir el reparto de trabajo entre las dos objeciones: "la
colapsabilidad de la diferencia de proporciones descarta el artefacto de no-colapsabilidad, pero
**no** el de inflación por dicotomización; por tanto la reversión de X **no puede** declararse
señal genuina hasta re-estimar sin dicotomizar θ". Esto convierte Punto 2 y Punto 4 en una sola
cadena coherente en lugar de dos conclusiones que se anulan.

**Omisiones de primera línea que agravan esto:**

- **Pearl (2014), *Understanding Simpson's Paradox*, The American Statistician 68(1):8-13.**
  Decidir si vale el marginal o el condicional es una cuestión **causal irresoluble solo con los
  datos**: si particionar o no la población no puede basarse en las probabilidades, sino en la
  información adicional del modelo causal. Socava el Punto 2, que deriva "es señal" de una propiedad
  puramente estadística (colapsabilidad). No citado.
- **VanderWeele (2019), Eur J Epidemiol 34(3):211-219** (relevante a Punto 3). No citado.

---

## A2 · La colapsabilidad de la diferencia de proporciones (Punto 2)

**VEREDICTO — SE SOSTIENE.** El dato colapsabilidad está bien enunciado; la inferencia que el
autor extrae de él, no.

**EVIDENCIA.**

- *Los hechos que el autor enuncia son correctos.* La diferencia de riesgos y la razón de riesgos
  son colapsables; el momio y el hazard ratio no (Greenland, Robins & Pearl 1999, *Confounding and
  Collapsibility in Causal Inference*, Statistical Science 14(1):29-46,
  doi:10.1214/ss/1009211805). Definición precisa: una medida es colapsable si sus valores marginal
  y por estrato coinciden **siempre que no haya confusión por C ni modificación de efecto por C**;
  la razón de riesgos y la diferencia de riesgos son colapsables, el momio no.
- *El salto está en esa misma definición.* La igualdad marginal = estrato requiere
  "no confusión **Y** no modificación de efecto". El autor colapsa la disyuntiva a
  "confusión o modificación de efecto = señal" y **omite las demás fuentes de reversión**:
  - **Sesgo de colisionador/selección.** Si formalidad o ingreso son colisionadores o descendientes
    del tratamiento —lo que el *propio Punto 3* teme— condicionar sobre ellos **induce** asociación
    espuria. La reversión sería un artefacto *creado por* el condicionamiento, no confusión
    *revelada por* él. La colapsabilidad **no protege** contra esto: es aritmética del promediado
    sobre un no-confusor, no una licencia causal para condicionar.
  - **Error de medición diferencial** y **agregación**: generan reversiones sin confusión ni
    modificación de efecto genuina.
  - En la literatura de Simpson: la reversión o el cambio de magnitud es común en el análisis
    condicional, y las explicaciones y soluciones están en el razonamiento causal apoyado en
    conocimiento de fondo, no en criterios estadísticos.
- *Diseño muestral complejo:* los ponderadores/estratos/UPM no alteran la colapsabilidad de la
  *medida*, pero gobiernan la **varianza**; las "9 significativas" dependen de un estimador de
  conglomerado último correcto. Secundario, **declarable**.
- *Imprecisión menor:* "la mayoría de los GLM son colapsables" es engañosa —el GLM más usado para
  binario es el logístico (momio, no colapsable)—. **Cosmético.**

**SEVERIDAD — declarable**, con un sub-veredicto **bloqueante** para la frase literal "es señal,
no artefacto": esa conclusión no se sigue de la colapsabilidad. La *recomendación* de Punto 2 (que
D-C declare colapsabilidad por coeficiente) sobrevive intacta.

**QUÉ HABRÍA QUE HACER.** Restringir la conclusión: "la colapsabilidad descarta el artefacto de
no-colapsabilidad; si la reversión es confusión genuina, sesgo inducido por condicionar sobre un
colisionador/mediador, o artefacto de medición, **no se decide con la colapsabilidad** sino con las
suposiciones causales del Punto 3 y el chequeo del Punto 4". Citar Pearl (2014) y
Greenland-Robins-Pearl (1999).

---

## A1 · El salto de Maxwell-Delaney (Punto 4)

**VEREDICTO — SE SOSTIENE DEBILITADO.** Las condiciones están citadas con fidelidad casi literal.
"Formalmente indistinguible" sobrepasa lo que los papers cubren.

**EVIDENCIA.**

- *Las cuatro condiciones que el autor lista son las reales.* Formulación canónica: habrá tasas
  infladas de error tipo I para la prueba de la **interacción** entre las dos variables categorizadas
  si están correlacionadas entre sí y una de ellas no se relaciona o se relaciona de forma no lineal
  con el desenlace (Maxwell & Delaney 1993, Psychological Bulletin 113(1):181-190,
  doi:10.1037/0033-2909.113.1.181). Y Vargha et al.: los resultados espuriamente significativos
  también ocurren cuando **solo una** de las dos variables se dicotomiza (Vargha, Rudas, Delaney &
  Maxwell 1996, J Educ Behav Stat 21(3):264-282). El autor no cambió las condiciones.
- *Mecanismo, según el propio MacCallum et al.:* tras dicotomizar X1 y X2, un ANOVA subsiguiente a
  menudo arroja una interacción significativa como simple tergiversación de la no-linealidad en el
  efecto de X1 y/o X2. Es decir: **artefacto de la prueba de interacción en ANOVA/regresión con
  desenlace continuo.**
- ⚠️ **El salto crítico — dos huecos:**
  1. **Desenlace continuo vs. binario (se resuelve con las fuentes):** todas las derivaciones
     publicadas (Maxwell-Delaney vía ANOVA/correlaciones; Vargha vía correlación parcial en marco
     normal bivariado; el ejemplo de MacCallum) suponen **Y continuo**. No hay en estos papers una
     derivación de la inflación para desenlace **binario** por diferencia de proporciones. Por tanto
     "formalmente indistinguible" —que reclama cobertura a nivel de teorema— **no está autorizado**:
     el teorema fue probado para otra clase de desenlace.
  2. **"Estratificar por celda" vs. "término producto X1·X2" — *REQUIERE VERIFICACIÓN CONTRA
     ARCHIVO*:** si la reversión celda-a-celda *es* operacionalmente una prueba de interacción en el
     sentido del paper, o un procedimiento distinto, depende del código de estimación. Conceptualmente
     están emparentados (heterogeneidad del efecto entre celdas de predictores dicotomizados), pero
     la **equivalencia formal** no se puede afirmar sin el repositorio. No se resuelve por
     plausibilidad. Aun así, el hueco (1) basta para debilitar "formalmente indistinguible".
- *Los números de MacCallum son exactos:* la dicotomización redujo r de .30 a .21, y r² de .09 a
  .04 (MacCallum, Zhang, Preacher & Rucker 2002, Psychological Methods 7(1):19-40,
  doi:10.1037/1082-989X.7.1.19). "Rara vez defendible y a menudo engañosa" reproduce fielmente la
  tesis. Sin defecto aquí.
- *Depende de notas del programa — REQUIERE VERIFICACIÓN CONTRA ARCHIVO:* que θ se dicotomice en
  ≥6, que θ→Y tenga pico en 4, y que los ejes estén correlacionados. El autor lo admite. No se
  resuelve.

**SEVERIDAD — declarable.** El fondo es legítimo (el diseño comparte los ingredientes generadores
del artefacto, así que la reversión **no puede presumirse genuina**). Solo "indistinguible"
sobre-afirma.

**QUÉ HABRÍA QUE HACER.** Degradar "formalmente indistinguible" a "comparte las condiciones
generadoras del artefacto; por tanto la reversión no puede presumirse genuina". **La prueba
diagnóstica publicada existe y es la recomendación de MacCallum et al.: no dicotomizar.** Re-estimar
con θ en escala continua y no-linealidad flexible (spline/polinomio) con la interacción modelada
explícitamente: si la reversión persiste, es genuina; si desaparece, era el artefacto de
dicotomización. Lo más accionable del reporte.

---

## A4 · ¿Es exigible la justificación gráfica? (Punto 3)

**VEREDICTO — SE SOSTIENE DEBILITADO.** Cinelli-Forney-Pearl dicen lo que el autor les atribuye;
la *recomendación* es más fuerte de lo que la literatura exige.

**EVIDENCIA.**

- *La atribución es correcta.* Cinelli, Forney & Pearl (2024, Sociological Methods & Research
  53(3):1071-1104, doi:10.1177/00491241221099552; **revisado por pares**) tratan el sobrecontrol
  como "mal control" y matizan el folclore: en ciertos casos (criterio de puerta delantera) se
  pueden explotar variables post-tratamiento para la identificación. "No todas las variables
  post-tratamiento son malos controles" es fiel. (Su paráfrasis de la puerta trasera es algo laxa
  pero no tergiversación.)
- ⚠️ **El problema práctico es real pero solo parcial.** Exigir el **DAG completo** antes de estimar
  es casi circular en un programa que investiga el mecanismo. Pero **no** hace falta el DAG completo:
  el **criterio de causa disyuntiva modificado** (VanderWeele 2019, *Principles of Confounder
  Selection*, Eur J Epidemiol 34(3):211-219, doi:10.1007/s10654-019-00494-6; y VanderWeele &
  Shpitser 2011, Biometrics 67(4):1406-1413) exige solo saber, para cada covariable, si es causa de
  la exposición y si es causa del desenlace —mucho menos que un DAG y operable. La dicotomía del
  autor ("DAG declarado O rótulo de mera asociación") es innecesariamente binaria.
- *Matiz que favorece al autor:* el criterio disyuntivo selecciona covariables **pre-tratamiento**;
  si formalidad/ingreso son post-tratamiento, también las excluiría, coincidiendo con su cautela.
  La literatura omitida respalda su preocupación, pero desmiente que la única salida sea un DAG
  completo.
- *El caso contra el programa tiene respuesta afirmativa y el autor ya la anota:* un conjunto
  pre-registrado que contenga un colisionador/mediador es **peor que no ajustar** (induce
  M-bias/sobrecontrol). "Un mal control pre-registrado sigue siendo un mal control" — correcto.

**SEVERIDAD — declarable.** La recomendación sobrevive con un límite escrito.

**QUÉ HABRÍA QUE HACER.** Sustituir el binario por tres niveles: (1) llave de identificación con
DAG → coeficiente causal; (2) **criterio de causa disyuntiva modificado** + análisis de sensibilidad
a confusión omitida (E-value; sensemakr) → coeficiente ajustado con supuestos declarados; (3) sin
nada de eso → "asociación condicional sobre S". Citar VanderWeele (2019).

---

## A3 · ¿Es E9(R1) el marco correcto? (Punto 1)

**VEREDICTO — SE SOSTIENE DEBILITADO** — y el cargo *amplio* propuesto ("importó un estándar donde
no aplica") **NO SE SOSTIENE.**

**EVIDENCIA.**

- *El cargo amplio falla:* E9(R1) **no** es solo de ECAs; el propio addendum se declara aplicable a
  estudios observacionales, aunque construir estimandos para evidencia de mundo real (RWE) puede
  requerir consideraciones adicionales (ver el capítulo de estimandos en RWE, Springer 2023; y la
  emulación de ensayo objetivo de Hernán-Robins). El autor **no** trasplantó un estándar inaplicable.
- *Los cinco atributos que lista son los reales:* población, tratamiento, desenlace, eventos
  intercurrentes, resumen poblacional. Su tesis central —que E9(R1) hace del resumen/enlace un
  atributo *definitorio* del estimando— es lectura correcta del addendum.
- *El cargo estrecho SÍ se sostiene: el análogo "eventos intercurrentes" está estirado.* Un evento
  intercurrente es **post-basal, temporal** (no-adherencia, rescate, muerte). La no-aplicabilidad
  estructural ("sin contacto", pregunta que no existió) es **dato que no existe por diseño /
  elegibilidad**, que la literatura distingue explícitamente del manejo de ICE. En datos
  transversales sin seguimiento no hay período post-basal: **no hay análogo limpio de ICE**. El
  autor lo intuye (lo marca como "lo que falta") pero lo rotula mal.
- *Mapeo TRATAMIENTO ↔ "normalización de θ":* defendible, no forzado —la normalización/corte de θ
  define el contraste de exposición (θ≥6 vs. θ<6)—, pero θ es una **exposición no manipulable**, no
  un tratamiento; conviene decirlo (problema de intervención bien definida).

**SEVERIDAD — declarable, rozando cosmético.** La recomendación (añadir un quinto requisito para
no-aplicabilidad estructural y no-respuesta, distinguiéndolas) es el instinto correcto y
**sobrevive**; solo hay que dejar de llamarlo "análogo de eventos intercurrentes" y citar la
literatura de estimandos en RWE.

**QUÉ HABRÍA QUE HACER.** Reetiquetar: el quinto requisito no es "el análogo de ICE" sino un
atributo propio de encuestas transversales (no-aplicabilidad estructural vs. no-respuesta vs.
no-elegibilidad). Anclar en la literatura de estimandos observacionales/RWE en vez del addendum
crudo de ECAs. Declarar θ como exposición no manipulable.

> **Nota de fuentes.** El borrador "Estimands in Real-World Evidence Studies" circula como preprint
> de arXiv 2307.00190 (**no revisado por pares**); la versión de capítulo de libro (Springer) sí lo
> está. La definición de colapsabilidad se ancló en Greenland-Robins-Pearl 1999 (revisado por
> pares), no en preprints.

---

## Cierre — cuáles de los cuatro puntos quedan en pie tal como están escritos

| Punto | Estado |
|-------|--------|
| **1 — E9(R1)** | En pie **casi tal cual**; la recomendación sobrevive; corregir la etiqueta "eventos intercurrentes" y citar la adaptación observacional. |
| **2 — colapsabilidad → señal** | **NO en pie tal como está.** El hecho es correcto; la conclusión "es señal, no artefacto" no está autorizada y contradice al Punto 4. |
| **3 — justificación gráfica** | En pie **solo si se suaviza**; la exigencia binaria es más fuerte de lo necesario dado el criterio de causa disyuntiva. |
| **4 — Maxwell-Delaney** | Las condiciones, **en pie y bien citadas**; la conclusión "formalmente indistinguible", **NO en pie** (continuo vs. binario) y en tensión frontal con el Punto 2. |

El defecto que ordena a todos los demás no es ninguno de los cuatro por separado: es que
**Punto 2 y Punto 4 emiten veredictos opuestos sobre el resultado de Encargo X y el documento no
los reconcilia.** Ahí está el trabajo.

---

## Referencias verificadas

- Maxwell, S. E., & Delaney, H. D. (1993). Bivariate median splits and spurious statistical
  significance. *Psychological Bulletin*, 113(1), 181-190. doi:10.1037/0033-2909.113.1.181
- Vargha, A., Rudas, T., Delaney, H. D., & Maxwell, S. E. (1996). Dichotomization, partial
  correlation, and conditional independence. *Journal of Educational and Behavioral Statistics*,
  21(3), 264-282.
- MacCallum, R. C., Zhang, S., Preacher, K. J., & Rucker, D. D. (2002). On the practice of
  dichotomization of quantitative variables. *Psychological Methods*, 7(1), 19-40.
  doi:10.1037/1082-989X.7.1.19
- Cinelli, C., Forney, A., & Pearl, J. (2024). A Crash Course in Good and Bad Controls.
  *Sociological Methods & Research*, 53(3), 1071-1104. doi:10.1177/00491241221099552
- Greenland, S., Robins, J. M., & Pearl, J. (1999). Confounding and collapsibility in causal
  inference. *Statistical Science*, 14(1), 29-46. doi:10.1214/ss/1009211805
- Pearl, J. (2014). Understanding Simpson's Paradox. *The American Statistician*, 68(1), 8-13.
  (contenido verificado vía Stanford Encyclopedia of Philosophy y literatura secundaria; no leído
  el texto primario directamente)
- VanderWeele, T. J. (2019). Principles of confounder selection. *European Journal of Epidemiology*,
  34(3), 211-219. doi:10.1007/s10654-019-00494-6
- VanderWeele, T. J., & Shpitser, I. (2011). A new criterion for confounder selection.
  *Biometrics*, 67(4), 1406-1413.
- ICH E9(R1) (2019/2021). Statistical Principles for Clinical Trials: Addendum — Estimands and
  Sensitivity Analysis in Clinical Trials.
