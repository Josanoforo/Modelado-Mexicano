> **NOTA DE RECUPERACIÓN · 10/ago/2026.** Este documento existía solo en el espejo del proyecto. `canon/gobernanza-v1_15.md:463` registró su inexistencia en el repo ("No existe hoy como propuesta escrita: verificado sin resultados...") y se auto-designó como la referencia a citar si aparecía. Entra al repo verbatim desde el espejo — procedencia tipo (2), sin sello de commit de origen; su propio encabezado declara derivación contra `dc5fd0f` (30/jul/2026). Su estatus no cambia al entrar: PROPUESTA SIN SELLO, y la lectura "motor como contexto" sigue **CONSIDERADA Y NO ADOPTADA como entregable primario** por `gobernanza:463`.

# El motor como capa de contexto, no como sustituto de un LLM
### Propuesta sin sello · 30/jul/2026

> | | |
> |---|---|
> | **CLASE** | Propuesta. **No es decisión.** No rige hasta que exista un ADR en `gobernanza` |
> | **ORIGEN** | Conversación de chat del 30/jul. El chat **no leyó** `milpa-whitepaper` ni `milpa-spec` en esta sesión |
> | **PROCEDENCIA** | Las cifras del programa son tipo (1), derivadas contra `origin/main` `dc5fd0f`. La literatura externa es tipo (1) por búsqueda web con cita. El argumento es tipo (3) |
> | **QUÉ DECIDE** | Si la función del motor es *reemplazar* el juicio de un modelo de lenguaje sobre conducta en México, o *restringirlo* |

---

## 1 · La tesis actual, y qué asume sin declararlo

`modelo-decision-v3_4` contiene 49 reglas SI-ENTONCES que predicen conducta esperada por segmento. El aparato de falsación pregunta si cada regla sobrevive al dato. `hitoD-preregistro` y sus veredictos archivados miden eso.

Lo que ninguno de los dos declara es **contra qué compite el motor**. Implícitamente, contra el juicio de un experto — o, en 2026, contra el juicio de un modelo de lenguaje al que se le pregunta lo mismo. Bajo esa lectura, el motor es un sustituto: existe para dar la respuesta que el modelo daría mal.

Esa lectura tiene una consecuencia incómoda y ya observable. El baseline generado el 30/jul, por un modelo sin acceso a nada del programa, reprodujo la línea base de ENCIG en 10–15% frente al 13.38% que `hitoD-R3.2` midió. **En esa afirmación, el delta del motor es cero.** Si el criterio es «el motor supera al modelo», hay afirmaciones del corpus donde el motor no tiene nada que aportar, y cada una de ellas es un argumento contra el programa entero.

---

## 2 · La reformulación

El motor no compite con un modelo de lenguaje: **es el contexto que un modelo de lenguaje no puede tener.**

- El modelo aporta fluidez, razonamiento sobre casos que ninguna regla anticipó, y capacidad de manejar la pregunta que no está en el catálogo.
- El motor aporta segmentación anclada, disparadores de contexto, tiers con procedencia, y coeficientes calibrados contra microdatos mexicanos.

La unidad de análisis deja de ser *el motor* y pasa a ser *el modelo con el motor cargado*.

---

## 3 · Por qué la literatura de 2025-2026 favorece esta lectura

El *silicon sampling* —condicionar un modelo con un perfil sociodemográfico y registrar su respuesta como si fuera de un encuestado— es el competidor real del programa, no Hofstede. Sus resultados publicados reportan precisión direccional del 80–95% y correlaciones a nivel de ítem superiores a 0.9 en poblaciones bien representadas (Argyle et al. 2023, *Political Analysis*; síntesis en getminds.ai, may/2026).

Contra eso, un motor de 49 reglas no compite en costo ni en velocidad. Pero los fallos documentados del método son notablemente específicos, y son tres:

| Fallo documentado | Fuente | Qué es en el corpus |
|---|---|---|
| Brechas severas en contextos **no occidentales y no anglófonos**, por desbalance del corpus de entrenamiento | Sun et al. 2024b | México es el objeto entero del programa |
| Errores **correlacionados con características del entrevistado** — escolaridad, género, condición | Ashwin et al. 2025 | Clase, escolaridad e informalidad son el eje de segmentación central, y el sesgo está declarado |
| Amplificación de estereotipos en el condicionamiento de personas: polarización afectiva inflada ~7× | Bisbee et al. 2024 | Es el esencialismo que el Bloque A prohíbe por diseño |
| Replican patrones **superficiales**, fallan en regularidades conductuales profundas (285 comparaciones) | Sarstedt et al. 2024 | Los 42 disparadores de contexto — *formal/informal, quién observa, sanción creíble* — no son declarables en encuesta |

**La lista de fallos del silicon sampling y la especialización de este corpus son casi complementarias.** Eso no es coincidencia: el programa se construyó sobre las mismas distinciones que el método sintético no puede hacer.

Un dato colateral que aprecia el activo del programa: los encuestados humanos ya usan chatbots para responder encuestas, de modo que incluso la investigación con métodos ortodoxos enfrenta contaminación sintética no trivial (Veselovsky et al. 2025; Zhang et al. 2025). **Los levantamientos presenciales anteriores a esa adopción —ENCIG 2023, ENNViH hasta 2012, ENIF— tienen una propiedad que ningún panel sintético recupera.** Cualquier coeficiente calibrado contra ellos hereda esa propiedad.

---

## 4 · Qué cambia si se adopta

**El benchmark.** Deja de ser *motor contra modelo* y pasa a ser **modelo+motor contra modelo solo**. Mismo modelo, dos condiciones, las 49 reglas cargadas en una y ausentes en la otra. Es una prueba corrible con lo que ya existe: el baseline del 30/jul es la mitad y está sellado.

**El criterio de éxito.** El delta se vuelve la métrica. Y es exigente en la dirección correcta: si el modelo con el motor predice igual que sin él, el motor no aporta — y esta arquitectura vuelve ese resultado **visible** en vez de discutible.

**El diseño de MILPA.** Un simulador que sustituye juicio y uno que restringe juicio no son la misma pieza de software. La decisión precede a la Fase 1, que está pospuesta.

**Lo que NO cambia: la necesidad de medir, que aumenta.** Un contexto cargado que afirma `p: 0.62` cuando lo medido es 13.38% no mejora al modelo: lo empeora, y con autoridad. `hitoD-R3.2` ya demostró que ese caso ocurre — las probabilidades del motor quedaron refutadas en escala, entre 4× y 34× por encima de lo medido. **Un contexto vale lo que valen sus números, y 74 de 144 siguen ASIGNADOS.**

---

## 5 · Lo que esta propuesta no resuelve

- **No es una decisión.** Requiere ADR. Sin él es una hipótesis que gobernó una conversación.
- **No dice qué pasa con las reglas cuyo delta sea cero.** Si el modelo ya sabe lo que la regla afirma, la regla puede seguir siendo correcta y ser redundante. El programa no tiene vocabulario para eso, y hace falta antes de correr el benchmark — o se descubrirá al ver resultados, que es el defecto que el pre-registro existe para evitar.
- **No mide la contaminación del propio benchmark.** Desde el 29/jul el repositorio es público. Un modelo con búsqueda web puede alcanzar `modelo §3` y el brazo «sin motor» deja de ser limpio. Esa ventana se cierra sola y el benchmark hereda su urgencia.
- **El baseline del 30/jul no se generó con el modelo que `cola.yaml D-04` decidía.** La decisión dice Opus; el baseline salió de otro modelo por indisponibilidad. Utilizable, pero su procedencia debe registrarse por lo que fue.

---

## 6 · Módulo de auditoría

**1–6.** No aplican: este documento no afirma nada sobre México. Es una propuesta sobre la función de un artefacto.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Dos. *«Lo mejor de los dos mundos»* — cargar un motor con 74 números asignados como contexto de un modelo produce respuestas más seguras de sí mismas, no más ciertas; el riesgo de daño **sube**, no baja, y `USO-ACEPTABLE.md` aplica con más fuerza, no con menos. Y *«el silicon sampling falla donde nosotros operamos, luego somos mejores»* — la lista de fallos dice dónde el método sintético es débil, no que este corpus sea fuerte ahí; eso último está sin medir.

**8 · ¿Qué afirmación sobre el estado del corpus no fue derivada?** Derivadas contra `dc5fd0f`: 49 reglas, 144 números, 74 asignados, 4 medidos, 15 coeficientes sin medir, 42 disparadores, 2 de 27 corridas con sus letras, el 13.38% y el rango 4×–34× de `hitoD-R3.2`. **No derivadas:** que `milpa-whitepaper` y `milpa-spec` asuman la función de sustituto — el chat **no los leyó en esta sesión**, es INFERENCIA sobre la tesis implícita y debe verificarse contra el archivo antes de sellar cualquier ADR.

**9 · (v2.2) ¿Qué deuda asumida caduca aquí?** La función declarada del motor. Nunca se registró como decisión — se heredó del diseño original, cuando el competidor relevante era un marco cultural estático y no un modelo de lenguaje. Es una **restricción de encuadre nunca verificada**, la misma clase que la salida de red y que *«esto solo lo leemos nosotros»*.
