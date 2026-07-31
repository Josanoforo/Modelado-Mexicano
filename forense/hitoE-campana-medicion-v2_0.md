<!-- PROCEDENCIA — leer antes que el cuerpo.

Este archivo NO lo produjo la sesión que lo recogió al repo (sesión del
30/jul/2026, rama `claude/new-session-gdstpo`, HEAD de entrada `78d5d54`).
Lo entregó el autor como archivo adjunto, producido en chat.

Clasificación por la regla de procedencia de la lectura (`instrucciones` v2.1):
**tipo (3)** — reportado por otra sesión/conversación, no verificado en origen.
Por protocolo §3, un documento de chat **no escribe hechos sobre el repo**: sus
afirmaciones se leen como preguntas a verificar, nunca como instrucción ni como
hecho. Se recoge al repo para que deje de vivir sólo en un adjunto y quede
versionado y citable.

**Ni una palabra del cuerpo se editó.** En particular, NO se corrigieron las
afirmaciones que la verificación de premisas encontró que no se sostienen
contra archivo — corregir el texto para que cuadre está prohibido por
`instrucciones` v2.1 ("Verificación de premisas antes de ejecución"): quien
ejecuta reporta el defecto, no lo ajusta.

**Este documento NO rige.** Su propia cabecera lo declara: `CLASE: Propuesta.
No es decisión. No rige sin ADR`. No hay ADR que lo selle. Nada de lo que
propone —E0 a E4, las puertas de decisión, el benchmark— está aprobado.

**Verificación de premisas:** `forense/notas/2026-07-30-verificacion-premisas-hitoE.md`,
derivada contra `78d5d54`. Cuatro afirmaciones del cuerpo no se sostienen
contra archivo; una de ellas —el conteo de constructos— es un número que el
propio documento declara derivado en su módulo de auditoría. Registradas en
`canon/cola.yaml` como `I-19`, `D-12` y `E-07` (los dos primeros se
registraron como `I-17`/`D-12` y se renumeraron al fusionar con `origin/main`;
ver la nota de renumeración en la verificación).

Quien use este plan lee la nota de verificación antes que el cuerpo.
-->

# HITO E · Campaña de medición
### Plan agresivo · v2.0 · propuesta sin sello · 30/jul/2026

> **v2.0 corrige un defecto de diseño de la v1.0.** La v1 asumía que un efecto
> medido puede sustituir un peso asignado del generador, y de ahí derivaba que
> la unidad de trabajo debía ser el generador completo. **Ese supuesto está
> refutado en el propio archivo que la v1 citaba:** la ficha `CAL-G3` declaró
> la opción (b) — elasticidad autónoma que **no** calibra el `-0.60`, porque no
> hay mapeo defendible entre efecto medido y peso del generador. La v1 heredó
> la conmensurabilidad de la palabra «calibración» y nunca la verificó. Misma
> familia que la regla v2.2: una restricción supuesta que dio forma al diseño y
> que nadie midió. Lo destapó una pregunta del autor, no la revisión del plan.

> | | |
> |---|---|
> | **CLASE** | Propuesta. No es decisión. No rige sin ADR |
> | **PROCEDENCIA** | Estructura de los 15 coeficientes derivada de `milpa/procedencia.yaml` contra `origin/main`. El diseño de campaña es tipo (3) |
> | **QUÉ ES** | Producir una **capa de efectos medidos** sobre los 8 constructos del motor: magnitudes reales, con banda, fuente y ventana temporal |
> | **QUÉ NO ES** | Sustituir los pesos asignados de los generadores. **Nada se convierte.** Los pesos siguen `ASIGNADO` y declarados |
> | **QUÉ DECIDE** | Si un LLM con la capa medida predice mejor que uno con las reglas solas. Si no, el programa lo sabrá |

---

## 0 · Por qué esto y no seguir como veníamos

`CAL-G3` tardó una jornada completa y terminó **sin estimar nada**. No por incompetencia: por diseño. La ficha era un falsador puesto sobre una tarea de calibración, y ADR-47 acaba de nombrar esa confusión.

Quitado ese aparato, el cuello de botella desaparece. **Calibrar no exige poder para refutar** — exige una fuente, una operacionalización declarada antes de mirar, y una banda honesta. Eso escala; un pre-registro de falsación por regla, no.

El estado real, derivado:

| Generador | Coeficientes | Valores asignados |
|---|---|---|
| **G1** | 2 | `confianza_institucional −0.60` · `radio_confianza −0.35` |
| **G2** | 2 | `sens_estatus 0.55` · `aversion_riesgo 0.20` |
| **G3** | 3 | `horizonte_temporal −0.60` · `aversion_riesgo 0.40` · `familismo_apoyo 0.20` |
| **G4** | 4 | `exposicion_violencia 0.70` · `confianza_institucional −0.40` · `horizonte_temporal −0.20` · `sens_estatus −0.15` |
| **G5** | 3 | `familismo_apoyo 0.50` · `familismo_obligacion` **sin magnitud** · `radio_confianza 0.15` |
| **G6** | 1 | `deferencia 0.45` |

**Los 15 son 8 constructos latentes reutilizados.** `confianza_institucional` aparece en G1 y G4; `horizonte_temporal` en G3 y G4; `aversion_riesgo` en G2 y G3; `sens_estatus` en G2 y G4. Operacionalizar los **8 constructos** resuelve los 15 coeficientes. Ese es el apalancamiento que hace la campaña viable.

---

## 1 · La estructura del reto

Cuatro fases. La primera y la última son las difíciles; las dos de en medio son trabajo.

```
E0 · MAPEO DE OPERACIONALIZACIÓN     ← firewall: tipo y existencia, nunca contenido
      8 constructos × 61 fuentes
                │
E1 · PRE-REGISTRO MASIVO, SELLADO    ← el cuello de botella real
      15 specs escritas ANTES de abrir un solo dato
                │
      ┌─────────┴─────────┐
E2 · ESTIMACIÓN EN PARALELO          ← n sesiones, una por generador
      cada una contaminada solo para lo suyo
                │
E3 · CONSOLIDACIÓN                   ← procedencia.yaml: ASIGNADO → MEDIDO
                │
E4 · EL BENCHMARK                    ← lo que decide si algo de esto sirvió
```

---

## 2 · E0 · Mapeo de operacionalización

**El problema que resuelve.** `confianza_institucional` no es una variable de encuesta. Es un constructo. Alguien tiene que decidir —**antes de ver datos**— qué reactivo medible lo representa, y declarar esa decisión.

**El entregable:** una matriz `constructo × fuente candidata`, con:
- qué instrumento cubre el constructo
- qué olas, qué cobertura, qué unidad (individuo / hogar / localidad)
- si la fuente permite el corte por segmento que el motor exige
- **alternativas descartadas con su razón** — obligatorio, con 61 fuentes disponibles

**Firewall, sin excepción:** tipo y existencia. Puede decir *«ENCUCI cubre confianza en instituciones, nacional, 2020, microdatos abiertos»*. **No** puede nombrar variables, ni citar reactivos, ni afirmar que un cruce es posible.

**Riesgo declarado:** algunos de los ocho pueden no tener proxy limpio. `deferencia` y `familismo_obligacion` son los candidatos a quedarse sin fuente. Si tres de ocho no se operacionalizan, la campaña baja de 15 coeficientes a ~9. **Eso es un resultado, no un fracaso** — y hay que decirlo antes de empezar.

---

## 3 · E1 · Pre-registro masivo — el cuello de botella

**Aquí está la dificultad real, y no es técnica.** Quince specs deben escribirse **antes de que nadie abra ninguna de las fuentes**. Una vez abierta una, esa sesión queda inhabilitada para pre-registrar contra ella (ADR-46).

Cada spec declara, sin excepción:

1. **Constructo y su operacionalización** — qué mide qué, decidido aquí
2. **Fuente, ola y unidad de análisis**
3. **Especificación de estimación** — la forma funcional, los controles, el estimador
4. **La banda esperada** — un intervalo declarado a priori para el coeficiente
5. **Criterio de conformidad**: `CONFIRMA` si lo medido cae dentro de la banda asignada · `MATIZA` si cae fuera pero conserva el signo · `ROMPE` si invierte el signo
6. **Qué haría inejecutable la estimación** — el equivalente de `CAL-X`, verificado con conteos del codebook antes de abrir microdatos

**El punto 4 es lo que convierte la campaña en algo falsable.** La banda a priori **no se declara sobre el peso del generador** —que está en otras unidades— sino sobre el **efecto medido en las unidades de la fuente**: puntos porcentuales, razón, elasticidad, lo que corresponda. Sin banda declarada antes, medir es describir; con banda, cada estimación es una predicción que puede fallar. `R3.2` ya demostró que fallan, y falló precisamente por confundir unidades.

**Regla dura:** las 15 specs se sellan **juntas, en un commit**. Nada de sellar cinco, estimar, y sellar las otras diez con lo aprendido.

---

## 4 · E2 · Estimación en paralelo

Una sesión por generador, seis en total. Cada una:

- lee **solo** su spec sellada
- abre **solo** las fuentes que su spec declara
- queda inhabilitada para todo lo demás, y lo declara al cerrar
- reporta **estimación, banda, n efectivo, y veredicto de conformidad**
- **se detiene** si el `CAL-X` de su spec dispara

**Disciplina de entorno, aprendida hoy:** un `worktree` por sesión, checkout compartido a `main` al terminar, y una sola sesión escribiendo el manifiesto a la vez.

**El constructo compartido es el riesgo técnico.** `confianza_institucional` se estima en G1 y en G4. Si las dos sesiones lo operacionalizan distinto, el modelo queda con dos valores del mismo constructo. **Mitigación: la operacionalización se fija en E0 y es única por constructo, no por generador.** Si dos generadores exigen operacionalizaciones distintas, eso es hallazgo y va a mesa antes de estimar.

---

## 5 · E3 · Consolidación — en artefacto nuevo, no en el motor

**`milpa/procedencia.yaml` no se toca.** Los 15 pesos siguen `ASIGNADO`, y eso no cambia al terminar la campaña.

La capa medida vive en un artefacto propio. Cada entrada declara: constructo, efecto estimado, **unidad** (pp, razón, elasticidad), banda, fuente, ola, n efectivo, operacionalización usada, y **la ventana temporal pegada** — la lección de `CAL-G3`: toda cifra viaja con su época o se degrada al citarse.

Obligación que no se negocia: **los constructos que no se pudieron medir se declaran como no medidos, con su razón.** Una campaña que mide 5 de 8 y nombra los 3 huecos es honesta. Una que fuerza los 3 con proxies malos, no.

**Y la regla que hace que esto no se corrompa:** ninguna entrada de la capa medida se escribe en la casilla de un peso del generador. Si alguien quiere esa conversión algún día, tendrá que defender la regla de mapeo **por separado y en mesa** — y hoy no existe.

---

## 6 · E4 · El benchmark — lo que decide si algo de esto sirvió

Esta es la parte que hace de la campaña un reto y no una tarea.

**Tres brazos, mismo modelo de lenguaje, mismas preguntas:**

| Brazo | Contexto cargado |
|---|---|
| **1 · LLM solo** | nada del programa |
| **2 · LLM + motor** | las reglas y sus pesos asignados, tal como están hoy |
| **3 · LLM + motor + capa medida** | lo mismo, más los efectos medidos de E3 como hechos anexos |

**Preguntas:** predicciones sobre conducta segmentada que alguna fuente pueda medir y que nadie haya medido aún. Pre-registradas antes de abrir el dato de validación.

**Métrica:** error absoluto contra lo medido. Y una sola pregunta que importa:

> **¿El brazo 3 le gana al 2? ¿Y el 2 al 1?**

**Los tres resultados posibles, y los tres son publicables:**

- **3 > 2 > 1** — la capa medida mejora y el motor aporta. El programa tiene producto, y no necesitó convertir un solo peso.
- **3 ≈ 2 > 1** — el motor aporta, la capa medida no añade. Vale saberlo: significa que el valor está en la estructura de reglas, no en las magnitudes.
- **3 ≈ 2 ≈ 1** — el motor no aporta nada sobre un LLM. **Es el resultado que mata al programa**, y hay que estar dispuesto a publicarlo.

**La ventana que se cierra sola:** el repo es público. En cuanto se indexe, el brazo 1 deja de ser limpio — un modelo con búsqueda puede alcanzar `modelo §3`. Esto tiene el mismo reloj que `D1` y es la razón para no demorarlo.

---

## 7 · Lo que corre en paralelo y no bloquea

- **ENSANUT** — 20 archivos bajados, sin registrar. Desbloquea 4 fichas.
- **ENUT** — 5 ediciones catalogadas como *existen y son alcanzables*, sin bajar.
- **Las 15 fichas huérfanas** del cruce, ahora con fuente candidata identificada.
- **La reclasificación del perímetro de 27** — cuántas son falsación y cuántas calibración. ADR-47 lo abrió y puede reducir el denominador que el README publica.

---

## 8 · Los cinco riesgos, sin adorno

**1 · Los constructos pueden no operacionalizarse.** Es el riesgo más probable. `deferencia`, `familismo_obligacion` y `radio_confianza` son los frágiles. Mitigación: E0 tiene compuerta — si menos de cinco constructos tienen fuente limpia, la campaña se replantea antes de pre-registrar.

**2 · La tentación de convertir.** Un efecto medido de `−0.08` no puede ocupar el lugar de un peso de `−0.60`: no son la misma magnitud ni están en las mismas unidades, y no existe regla de conversión defendible. Este es el defecto que hundió la v1.0 de este plan y el modo de falla de `R3.2` —probabilidades del motor 4x-34x fuera de escala—. Mitigación, y es dura: **`milpa/procedencia.yaml` no se toca en toda la campaña.** Los pesos siguen `ASIGNADO`. La capa medida vive en artefacto propio, con sus unidades declaradas en cada entrada. Cualquier sesión que proponga sustituir un peso se detiene y lo reporta.

**3 · El pre-registro masivo es frágil a la contaminación.** Quince specs escritas por sesiones que no pueden haber visto ninguna fuente. Un solo descuido invalida una spec. Mitigación: E0 produce el mapeo con firewall, y quien pre-registra **lee el mapeo, no las fuentes**.

**4 · El benchmark puede no distinguir nada.** Si las preguntas son demasiado fáciles, los tres brazos aciertan; si son demasiado difíciles, los tres fallan. Mitigación: pre-registrar más preguntas de las necesarias y declarar el criterio de descarte antes de ver resultados.

**5 · Y el riesgo real, que no es técnico: la campaña puede terminar en 4 de 15.** Con constructos sin fuente, generadores incompletos y `CAL-X` disparando. Eso sigue siendo **cuatro veces lo que hay hoy** y el registro lo dirá tal cual.

---

## 9 · Puertas de decisión

| Fase | Se pasa si | Si no |
|---|---|---|
| **E0 → E1** | ≥5 de 8 constructos con fuente candidata | Replantear alcance, no forzar proxies |
| **E1 → E2** | 15 specs selladas en un commit, con banda a priori y `CAL-X` verificado | No estimar nada |
| **E2 → E3** | ≥1 constructo medido con unidad y banda declaradas | La campaña reporta cero y lo dice |
| **E3 → E4** | La capa medida existe y contiene hechos que el LLM no tiene | No hay brazo 3 que correr |

---

## 10 · Módulo de auditoría

**1-6.** No aplican: es un plan de proceso, no afirma nada sobre México.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Dos. *«15 coeficientes medidos»* si en realidad son 15 coeficientes con proxies de calidad desigual — de ahí la obligación de declarar operacionalización y banda por cada uno. Y *«el motor calibrado gana el benchmark, luego el modelo es válido»*: ganar un benchmark de tres brazos sobre preguntas propias no valida un modelo sobre la población mexicana. Mide una cosa estrecha, y así hay que decirlo.

**8 · ¿Qué afirmación sobre el estado del corpus no fue derivada?** Derivadas: la estructura de los 6 generadores y sus 15 coeficientes con valores, de `milpa/procedencia.yaml`; que los 15 se reducen a 8 constructos, por inspección de esa misma estructura; que `familismo_obligacion` está sin magnitud. **No derivado:** que existan fuentes para los 8 constructos — es la pregunta que E0 responde, y este plan **no la presupone**.

**9 · (v2.2) ¿Qué deuda asumida caduca aquí?** Dos, y la segunda es de este documento. *«Los coeficientes se calibran de uno en uno»* nunca se registró como decisión: se heredó de que `CAL-G3` fue el primero y se trató como plantilla; caduca por ADR-47. Y **la conmensurabilidad entre efecto medido y peso asignado**, que la v1.0 de este plan dio por buena sin verificarla pese a que la ficha `CAL-G3` ya la había refutado por escrito. Registrar eso importa: la regla v2.2 no se cumple por conocerla — se citó tres veces el mismo día en que se violó.

---

## 11 · Adenda 31/jul/2026 — el catálogo de fuentes contra los cuatro contrastes

**Disciplina aplicada:** adenda fechada, append-only. El cuerpo (§0–§10) no se tocó — ni una palabra —, por la misma regla de procedencia que la cabecera ya invoca para el resto del documento: este archivo es tipo (3), no rige, y corregirlo para que cuadre está prohibido. Esta sección es de otra sesión, con otra procedencia: deriva de `data/catalogo-fuentes-v1_0.md` (119 fuentes, verificado 31/jul/2026 contra `origin/main` en `2114d93` con `tests/catalogo.py` y `tests/dedup.py`, ambos consistentes) y de `milpa/procedencia.yaml` (sin modificar).

**Límite de lectura — ADR-46, declarado antes de leer resultado alguno.** Esta sesión leyó `data/catalogo-fuentes-v1_0.md` completo y los diez inventarios de `data/inventarios/` en su texto de *alcance temático declarado* (las líneas que cada inventario marca como "Alcance temático declarado" / "Pertinencia al dominio" / "Relación con el dominio"). **No abrió ningún portal, ninguna página de fuente, ningún cuestionario ni diccionario de variables.** Cada inventario declara en su cabecera que es "catalogación de instrumentos" y que "no contiene variables, reactivos, cifras de resultados ni valoraciones de calidad" — con ese material solo se pueden producir **candidatas**, nunca un veredicto de instrumentación. Por eso la escala de este contraste tiene dos valores, no tres:

- **CANDIDATA CON DOCUMENTACIÓN PENDIENTE** — el alcance temático declarado de la fuente sugiere que mide el constructo. Falta el cuestionario para saber con qué reactivo y a qué segmentación llega; esa inspección la hace una sesión que se declare contaminada (ADR-46), no ésta.
- **SIN CANDIDATA** — ninguna de las 119 declara alcance temático compatible. Este veredicto sí se sostiene solo con el catálogo.

**La unidad es el constructo, no la celda.** `milpa/procedencia.yaml:270-281` (`asignados_coeficiente.detalle`) da, por inspección directa, **9 constructos únicos** tras los 15 coeficientes: `aversion_riesgo, confianza_institucional, deferencia, exposicion_violencia, familismo_apoyo, familismo_obligacion, horizonte_temporal, radio_confianza, sens_estatus`. Por ADR-28.b, `confianza_institucional` no es escalar: es un vector de 6 componentes (seguridad, educación, salud, electoral, justicia-policía, financiera), **sin poblar** (`procedencia.yaml:65`). Contado el vector, el barrido cubrió **14 filas**: 9 constructos, con `confianza_institucional` desdoblado en sus 6 componentes en vez de una fila agregada.

**Corrección de revisión (misma sesión, antes del merge):** la primera pasada de este barrido marcó `horizonte_temporal` como SIN CANDIDATA. Es un error — `milpa/procedencia.yaml:282-288`, campo `asignados_coeficiente.unico_calibrable_hoy`, nombra explícitamente la fuente: `coeficiente: "G3 → horizonte_temporal"`, `con_que: "El panel rotativo trimestral de la ENOE sigue al mismo hogar cinco trimestres... Es la única elasticidad del modelo que México permite estimar con dato público."` — en el mismo bloque `asignados_coeficiente` que ya se había leído. `ENOE` está en `data/catalogo-fuentes-v1_0.md` (espina dorsal, 3 dominios, `micro=sí libre=sí`, operable, sin bajar). Corregido: `horizonte_temporal` → **CANDIDATA CON DOCUMENTACIÓN PENDIENTE**, fuente `ENOE`, y con una marca que el resto de las candidatas de esta adenda no llevan — no es solo "alcance temático declarado sugiere que mide el constructo": el propio `procedencia.yaml` ya la declara la única vía de estimación con dato público, aunque como *proxy de elasticidad* (cambio formal↔informal en el panel), no como reactivo directo de horizonte temporal.

### Conteo derivado (el entregable central)

| | Filas (de 14) | Constructos únicos (de 9) |
|---|---|---|
| **CANDIDATA CON DOCUMENTACIÓN PENDIENTE** | 10 | 7 (con al menos un componente candidato) |
| **SIN CANDIDATA** | 4 | 2 (`sens_estatus`, `deferencia`) |

Traducido a los 144 números — y aquí la unidad vuelve a la celda solo para multiplicar, no para buscar: de los **144**, **39 son `probabilidades_de_regla`, una unidad distinta (reglas implementadas, no constructos latentes) y quedan fuera de este contraste.** De los **105 restantes** (15 coeficientes + 90 `params_base`, ambos construidos sobre los mismos 9 constructos):

| | Números | Base del cálculo |
|---|---|---|
| **CON CANDIDATA** | **72** | 12/15 coeficientes (slots cuyo constructo tiene candidata) + 60/90 params_base (`confianza_institucional` 24/36 · `radio_confianza` 6/6 · `aversion_riesgo` 6/6 · `exposicion_violencia` 6/6 · `familismo_apoyo` 6/6 · `familismo_obligacion` 6/6 · `horizonte_temporal` 6/6) |
| **SIN CANDIDATA** | **27** | 3/15 coeficientes (`sens_estatus`×2, `deferencia`×1) + 24/90 params_base (`confianza_institucional` 12/36 · `sens_estatus` 6/6 · `deferencia` 6/6) |
| **NO DERIVABLE ESTA SESIÓN** | **6** | 1 de los 15 `params_base` no tiene nombre declarado en `procedencia.yaml` (la reconstrucción del desglose 54→90 vía `delta_v1_v2` deja 14 de 15 parámetros identificados por nombre; el 15º queda sin identidad legible en este archivo — línea para `forense/hallazgos.md`, no bloquea) |

El reparto de `confianza_institucional` (24 candidata / 12 sin candidata de sus 36 números) asume partición pareja entre sus 6 componentes — **supuesto, no medido**; el vector está declarado "sin poblar" y esta sesión no lo llena.

### Los cuatro contrastes

**1 · §196 — "las 15 fichas huérfanas del cruce, ahora con fuente candidata identificada".** Ese cruce (qué son las "15 fichas huérfanas") no existe en el árbol — ya lo registró `I-19` (`hallazgos-congelados-2026-07-30.yaml:440`): la cadena "huérfana" no aparece en ningún archivo del repo. Interpretando "las 15" como los 15 coeficientes de `asignados_coeficiente` — la única estructura de 15 elementos que el repo sí declara —, el resultado de cruzarlos contra las 119 fuentes es: **12 de 15 tienen candidata con documentación pendiente; 3 de 15 no tienen ninguna** (`sens_estatus` en G2 y G4, `deferencia` en G6). §196 afirma que las 15 "ahora" tienen candidata — la cifra real es 12, no 15, y la brecha no es cosmética: los 3 sin candidata tocan 2 constructos enteros sin ninguna fuente utilizable en el catálogo completo.

**2 · §211 — "la campaña puede terminar en 4 de 15".** Esa cifra se fijó sin catálogo, como piso de riesgo genérico. Con las 119 fuentes, el piso **no baja — cambia de naturaleza**. Antes era un riesgo difuso ("puede que no todo se opere"); ahora es un mecanismo nombrado: **3 de 15 coeficientes no tienen ninguna candidata en el catálogo completo**, así que ningún ejercicio de pre-registro puede llevarlos más allá de "no medido, sin fuente" — no es una cuestión de banda o de `CAL-X`, es que el corpus entero no lo cubre. De los 12 restantes, **ninguno pasó de candidata a instrumentado**: esta sesión no puede confirmar que alguno vaya a sobrevivir la inspección de instrumento. "4 de 15" sigue siendo un resultado posible — pero ahora es optimista, no pesimista, si alguno de los 12 candidatos falla la inspección de reactivo o segmentación. El catálogo no sube el número; lo hace defendible.

**3 · §113 — "`deferencia` y `familismo_obligacion` son los candidatos a quedarse sin proxy limpio".** Contrastada: **parcialmente sostenida y demasiado angosta, y en un sentido distinto al que la primera pasada de esta adenda reportó.** `deferencia` se confirma — cero mención de deferencia, jerarquía o respeto a la autoridad como constructo en los diez inventarios; **SIN CANDIDATA**, sin matiz. `familismo_obligacion` es más ambiguo de lo que la hipótesis supone: sí hay candidatas (`ENASEM` cuidado a adultos mayores, `ENDIREH`, `ENASIC`, `ENBIARE` relaciones y percepción de vida familiar), pero **ninguna es la escala de familismo** — son proxies conductuales de cuidado/obligación, y las dos marcas (b) de `procedencia.yaml:278-280` (escalas validadas en contexto migratorio, nadie las midió en población en México) siguen sin resolverse aunque exista candidata. `horizonte_temporal` **no** pertenece a este grupo — corregido arriba: tiene candidata nombrada (`ENOE`, vía `unico_calibrable_hoy`), así que la hipótesis no falló en omitirlo. Lo que la hipótesis **sí no vio** es `sens_estatus`: cero mención de sensibilidad al estatus, consumo aspiracional o prestigio como constructo declarado en los diez inventarios — termina en el mismo **SIN CANDIDATA** que `deferencia`, y la hipótesis original no lo nombró como frágil. Además, dos de los seis componentes de `confianza_institucional` (educación, financiera) también quedan sin candidata. La hipótesis nombró 2 constructos frágiles; el catálogo confirma uno (`deferencia`), matiza el otro (`familismo_obligacion`: candidata débil, no instrumento limpio) y encuentra uno que la hipótesis no vio (`sens_estatus`), más 2 componentes sin candidata de un cuarto constructo.

**4 · Los constructos declarados vs. los derivados.** El plan (§0, §1, §2, §5, módulo de auditoría punto 8) declara **8**. `milpa/procedencia.yaml:270-281` (`asignados_coeficiente.detalle`), inspeccionado en esta sesión independientemente, da **9**: el plan omite `radio_confianza` (presente en G1 y G5) de su lista de constructos compartidos en §0, pese a nombrarlo entre los frágiles en §8. El conteo correcto — derivado aquí de la tabla `detalle`, no tomado de ningún número que se me haya dictado — es **9**, y coincide con el ya registrado en `I-19` (`forense/hallazgos-congelados-2026-07-30.yaml:440`), abierto desde el 30/jul/2026 y todavía sin resolver. Esta adenda no lo cierra — no es decisión de mesa, es una sesión de catálogo — pero confirma el 9 por una vía distinta a la que I-19 usó.

### Cola priorizada — de las 32 operables sin bajar, cuáles desbloquean más constructos

**Criterio, con una excepción declarada, no silenciosa.** El orden por defecto es cuántas de las 14 filas (constructo o componente de `confianza_institucional`) tienen en esa fuente una candidata con documentación pendiente. `ENOE` rompe ese orden a propósito: por conteo de filas desbloqueadas vale 1, igual que `ENUT`, `ENSANUT`, `ENCUP` o `Global Findex` — pero es la única fuente de toda la cola (y del catálogo completo) que `procedencia.yaml` ya declara *calibrable con dato público*, no solo temáticamente afín (`unico_calibrable_hoy`, citado arriba). Ese es un criterio distinto y más fuerte que "cuántos constructos toca", y por eso encabeza la cola en vez de ir en el bloque de 1-fila. Ninguna de las 6 ya en disco (`ENCIG`, `ENCUCI`, `ENIF`, `ENIGH`, `ENNVIH`, `ENVIPE`) está en esta cola — ya están bajadas —, aunque `ENCIG` y `ENCUCI` ya aportan candidata declarada para `radio_confianza` y componentes de `confianza_institucional`, y `ENVIPE` para `exposicion_violencia` y `confianza_institucional[seguridad/justicia-policía]`.

| Orden | Fuente | Filas que desbloquea (candidata) |
|---|---|---|
| 1 | **ENOE** | 1 · `horizonte_temporal` — pero es la única con ruta de calibración ya declarada en `procedencia.yaml` (`unico_calibrable_hoy`), no solo afinidad temática; por eso encabeza pese a desbloquear menos filas que las siguientes cuatro |
| 2 | **ENDIREH** | 3 · `exposicion_violencia`, `familismo_apoyo`, `familismo_obligacion` (proxy conductual) |
| 3 | **ENASIC** (Encuesta Nacional para el Sistema de Cuidados) | 2 · `familismo_apoyo`, `familismo_obligacion` (proxy conductual — población cuidadora) |
| 4 | **ENBIARE** (Encuesta Nacional de Bienestar Autorreportado) | 2 · `familismo_apoyo`, `familismo_obligacion` (declara "relaciones en el hogar y percepción de la vida familiar") |
| 5 | **ENASEM** | 2 · `familismo_apoyo`, `familismo_obligacion` (proxy conductual — cuidado a adultos mayores) |
| 6 | **ENSU** | 2 · `confianza_institucional[seguridad]`, `exposicion_violencia` — débil: el propio inventario marca "pertinencia parcial, no verificada" |
| 7 | **ENUT** | 1 · `familismo_apoyo` (trabajo no remunerado al hogar) |
| 8 | **ENSANUT** | 1 · `confianza_institucional[salud]` (el propio inventario la marca "marginal, catalogada por completitud") |
| 9 | **ENCUP** | 1 · `confianza_institucional[electoral]` |
| 10 | **Global Findex Database** | 1 · `aversion_riesgo` (declara "gestión de riesgo financiero", no una escala de aversión al riesgo) |
| — | Las 22 operables restantes de las 32 | 0 · ninguna declara alcance temático compatible con los 9 constructos, según lectura de esta sesión |

Ningún constructo se resuelve bajando una sola fuente: los dos huecos totales (`sens_estatus`, `deferencia`) no tienen candidata en ninguna de las 119, bajadas o no — bajar no los toca.

**Hasta dónde leyó esta sesión, declarado:** `data/catalogo-fuentes-v1_0.md` completo (133 líneas); los diez archivos de `data/inventarios/` en sus secciones de alcance temático declarado (no completos línea por línea en los casos de `inventario-fuentes-migracion-mexico.md` y `inventario_fuentes_tramites_estado_mexico.md`, donde se usó búsqueda dirigida por palabra clave en vez de lectura corrida); `milpa/procedencia.yaml` completo; `forense/hallazgos-congelados-2026-07-30.yaml` (entradas I-19 y D-12) para contexto de lo ya registrado. Cero portales, cero cuestionarios, cero diccionarios de variables.
