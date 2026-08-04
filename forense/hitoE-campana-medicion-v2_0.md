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
## Adenda · 31/jul/2026 · contraste contra el catálogo de fuentes

> Disciplina aplicada: **append-only**. La cabecera de este archivo prohíbe
> editar el cuerpo (*«corregir el texto para que cuadre está prohibido»*), así
> que ni una palabra de `§0`–`§10` se tocó. Lo que sigue es contraste nuevo,
> no corrección del texto de arriba.

**Procedencia de esta adenda.** Tipo (1): derivado en esta sesión leyendo
`data/catalogo-fuentes-v1_0.md` (119 fuentes) y `data/inventarios/*.md`
contra `milpa/procedencia.yaml`, bajo el límite de lectura de ADR-46 (solo
alcance temático declarado — nunca reactivo, nunca portal). El catálogo no
existía cuando este plan se escribió (30/jul); entró al repo el mismo día
por otra sesión y hoy es el primer artefacto que lo cita.

**Unidad de trabajo:** el constructo, no los 144 números uno por uno. Los 15
coeficientes de `milpa/procedencia.yaml:270-281` son **9 constructos
únicos**, no 8 — ya registrado como defecto en `forense/hallazgos-congelados-2026-07-30.yaml:439-448`
(`I-19`) y reconfirmado aquí de forma independiente contando la misma
sección del archivo. `confianza_institucional` se trató como **vector de
seis** componentes (ADR-28.b), no como escalar, honrando `D-12`. El
inventario de trabajo queda en 15 unidades: los 8 constructos no-confianza
compartidos entre generadores + los 6 componentes del vector +
`acceso_digital` (aparece solo en `params_base`, no en los 15 coeficientes,
pero es de la misma familia de escalas — `canon/modelo-decision-v3_4.md:96`).

### 1 · Corrección de §10 punto 8 — el conteo de constructos

El plan declara **derivado** «los 15 se reducen a 8 constructos». Contando
`milpa/procedencia.yaml:270-281` de nuevo, con script y a mano, dan **9**:
`aversion_riesgo, confianza_institucional, deferencia, exposicion_violencia,
familismo_apoyo, familismo_obligacion, horizonte_temporal, radio_confianza,
sens_estatus`. El faltante es `radio_confianza` (G1, G5) — el propio plan lo
nombra entre los frágiles en `§8` sin contarlo en el denominador. Esta
adenda no corrige `§0`/`§1`/`§2`/`§5`/`§9`: los deja como están, tipo (3), y
apunta a `I-19` para el detalle completo.

### 2 · §113 — la hipótesis de los proxies frágiles, contrastada

**Afirmación:** `deferencia` y `familismo_obligacion` son "los candidatos a
quedarse sin fuente".

**Contraste, por alcance temático declarado en las 119 fuentes:** de los 9
constructos-coeficiente (tratando `confianza_institucional` como escalar
único, como hace la tabla de `§0`), **6 quedan SIN INSTRUMENTO**:
`aversion_riesgo`, `deferencia`, `familismo_apoyo`, `familismo_obligacion`,
`horizonte_temporal`, `sens_estatus`. Solo `exposicion_violencia` queda
INSTRUMENTADO limpio (ENVIPE / ENDIREH); `radio_confianza` y
`confianza_institucional` quedan PARCIAL (hay fuente con alcance declarado
adyacente — confianza interpersonal genérica, confianza institucional
genérica — pero ninguna ficha del catálogo declara textualmente el
componente que el modelo necesita, y confirmarlo exige inspección de
instrumento, fuera del límite de esta sesión).

**Veredicto:** la hipótesis de `§113` acierta en la dirección — los dos
nombrados sí están SIN INSTRUMENTO — pero **subestima el tamaño del
problema por un factor de tres**. No son 2 de 9 los frágiles; son 6 de 9.
La compuerta de `§9` (E0→E1, "≥5 de 8/9 constructos con fuente candidata")
no se habría pasado ni con el denominador correcto ni con el incorrecto: con
9, hay 3 candidatos (`exposicion_violencia` instrumentado + 2 parciales) —
muy por debajo de 5.

### 3 · `confianza_institucional` como vector — instrumentado componente a componente

Contra ADR-28.b, que exige tratarlo como vector de 6 y no como promedio:

| Componente | Veredicto | Candidata |
|---|---|---|
| salud | **INSTRUMENTADO** | ENSANUT — declara explícitamente "confianza en instituciones y servicios de salud" |
| seguridad / FFAA | PARCIAL | ENCIG, ENVIPE — "confianza en instituciones" genérico, sin desagregar el componente |
| justicia-policía | PARCIAL | ENVIPE, ENCIG — mismo alcance genérico que arriba |
| electoral / partidos | PARCIAL | ENCUCI, LAPOP, Latinobarómetro — alcance adyacente, sin frase textual de "confianza electoral" |
| educación | **SIN INSTRUMENTO** | — |
| financiera | **SIN INSTRUMENTO** | — |

Con esta desagregación, el componente que `G4` usa (`justicia-policía`) es
PARCIAL, no ciego; el que `G1` usa (`[dominio]`, sin resolver cuál de los
seis — ver `D-12`) no puede siquiera evaluarse hasta que se decida el
componente, así que su ficha se cuenta como SIN INSTRUMENTO por
indeterminación, no por ausencia de fuente.

### 4 · Riesgo cruzado — `exposicion_violencia` y `ref.B.05`

`milpa/procedencia.yaml:296-302` exige que la refutación `ref.B.05` no
tenga componente base por perfil independiente de la celda, y que el
parámetro sí lo tiene (6 números, 0.35–0.70). Del lado de instrumento: la
fuente de mayor cobertura para este constructo, **ENVIPE**, declara
desagregación geográfica (entidad, urbano/rural) pero **no** desagregación
demográfica por perfil en su alcance declarado; la fuente que sí desagrega
por perfil, **ENDIREH**, tiene universo acotado (mujeres de 15+, violencia
en el hogar). Ninguna de las dos, con el alcance hoy declarado, sostiene un
efecto medido por perfil sin mezclar universos — así que instrumentar este
constructo no resuelve por sí solo el riesgo cruzado con `ref.B.05`; solo
provee la magnitud agregada, que es justo lo que la refutación cuestiona.

### 5 · §196 — las "15 fichas huérfanas del cruce"

Esa frase no existe en ningún otro archivo del repo (ya registrado en
`I-19`, punto 3: "la cadena huérfana/huerfana no aparece en ningún archivo
del repo"). Interpretando "las 15" como los 15 coeficientes de
`milpa/procedencia.yaml:270-281` — es el único conjunto de 15 que el plan
maneja — y cruzando cada ficha (generador × coeficiente) contra el veredicto
de su constructo:

| Generador | Coeficiente | Veredicto de la ficha |
|---|---|---|
| G1 | `confianza_institucional[dominio]` | SIN INSTRUMENTO (componente sin resolver, `D-12`) |
| G1 | `radio_confianza` | PARCIAL |
| G2 | `sens_estatus` | SIN INSTRUMENTO |
| G2 | `aversion_riesgo` | SIN INSTRUMENTO |
| G3 | `horizonte_temporal` | SIN INSTRUMENTO |
| G3 | `aversion_riesgo` | SIN INSTRUMENTO |
| G3 | `familismo_apoyo` | SIN INSTRUMENTO |
| G4 | `exposicion_violencia` | **INSTRUMENTADO** |
| G4 | `confianza_institucional[justicia]` | PARCIAL |
| G4 | `horizonte_temporal` | SIN INSTRUMENTO |
| G4 | `sens_estatus` | SIN INSTRUMENTO |
| G5 | `familismo_apoyo` | SIN INSTRUMENTO |
| G5 | `familismo_obligacion` | SIN INSTRUMENTO |
| G5 | `radio_confianza` | PARCIAL |
| G6 | `deferencia` | SIN INSTRUMENTO |

**4 de 15 fichas tienen candidata** (1 instrumentada + 3 parciales); **11 de
15 no tienen ninguna**. Ninguna de las 11 huérfanas tiene fuente candidata
identificada entre las 119 — al contrario de lo que `§196` afirma para el
conjunto entero.

### 6 · §211 — recálculo de "la campaña puede terminar en 4 de 15"

El plan escribió esa cifra sin catálogo, como techo pesimista. Con las 119
fuentes:

- **Bajo el criterio estricto** (candidata = INSTRUMENTADO, sin pendiente de
  inspección): **1 de 15** — solo `exposicion_violencia` (G4). **Baja**, y
  baja mucho: el techo pesimista del plan era optimista.
- **Bajo el criterio laxo** (candidata = INSTRUMENTADO o PARCIAL, con
  inspección de instrumento pendiente y fuera del alcance de esta sesión):
  **4 de 15** — la misma cifra que el plan escribió a ciegas, pero por una
  razón distinta y con 3 de las 4 marcadas explícitamente como no
  confirmadas.

**Conclusión:** el «4 de 15» del plan no se sostiene como habría querido
sostenerse — coincide con el criterio laxo por coincidencia numérica, no
porque el plan haya acertado el mecanismo, y bajo el criterio que de verdad
importa para pre-registrar (fuente confirmada, no candidata a confirmar)
la cifra real es **1 de 15**.

### 7 · Cobertura sobre los 144 números

Multiplicando por perfiles, no por celda:

| | INSTRUMENTADO | PARCIAL | SIN INSTRUMENTO | Total |
|---|---|---|---|---|
| 15 coeficientes (fichas, tabla §5) | 1 | 3 | 11 | 15 |
| 90 `params_base` (15 parámetros × 6 perfiles) | 3×6=18 | 4×6=24 | 8×6=48 | 90 |
| **Subtotal constructo-parametrizado** | **19** | **27** | **59** | **105** |
| 39 probabilidades de regla | — fuera del alcance de este contraste (no son constructo-parametrizadas de la misma forma) | | | 39 |
| **144** | | | | |

**El entregable central:** de los 105 números de los 144 que dependen de un
constructo (15 coeficientes + 90 `params_base`), **19 quedan sobre fuente
instrumentada, 27 sobre fuente parcial (pendiente de inspección de
instrumento) y 59 sin ninguna fuente candidata en las 119.** Los 39 de
probabilidades de regla no se tocaron: no son de la misma familia de
parámetro y el encargo no pidió recorrerlos.

### 8 · Cola priorizada — operables sin bajar que más desbloquean

De las 32 operables sin bajar (`data/catalogo-fuentes-v1_0.md`, sección
"Operables no bajadas"), por impacto estimado en constructos hoy PARCIAL o
SIN INSTRUMENTO — impacto **estimado por alcance declarado**, no
confirmado; confirmarlo exige la inspección que ADR-46 reserva a otra
sesión:

1. **ENCUP** — candidata a instrumentar hasta 3 componentes del vector de
   confianza institucional (electoral, justicia-policía, posiblemente
   seguridad) si su batería declarada resulta suficientemente desagregada.
2. **ENSAFI** — candidata a `aversion_riesgo` y a `confianza_institucional[financiera]`.
3. **ENFIH** — mismo par que ENSAFI.
4. **GLOBAL FINDEX DATABASE** — su alcance ya declara "gestionar riesgo
   financiero"; candidata a `aversion_riesgo` y a la componente financiera
   del vector.
5. **ENCUESTA NACIONAL PARA EL SISTEMA DE CUIDADOS** — candidata a
   `familismo_apoyo` (redes de apoyo entre hogares).
6. **ENADID** — sospecha ya documentada de "captación de redes de apoyo";
   candidata a `familismo_apoyo`.
7. **ENDIREH** — candidata a `familismo_obligacion` y a reforzar la
   desagregación por perfil de `exposicion_violencia` (§4 de esta adenda).
8. **ENCUESTA NACIONAL DE BIENESTAR (ENBIARE)** — candidata especulativa a
   familismo; su módulo de bienestar/relaciones no está confirmado.
9. **EDER** — candidata especulativa y débil a `horizonte_temporal`
   (trayectorias de curso de vida).

Ninguna de las 32 se bajó. Ninguna de estas candidaturas se confirma sin
abrir el instrumento — quedan como orden de prioridad, no como veredicto.

### 9 · Límite de lectura declarado (ADR-46)

Esta adenda leyó únicamente: `data/catalogo-fuentes-v1_0.md`; los 11
archivos de `data/inventarios/` (los 10 dominios + `README-inventarios.md`);
`milpa/procedencia.yaml`; `canon/modelo-decision-v3_4.md` (solo las líneas
citadas arriba, para resolver el rótulo `G1a`/`[dominio]` y el vector de
`§1.3`); `forense/hallazgos-congelados-2026-07-30.yaml` (`I-19`, `D-12`).
No se abrió ningún portal, ninguna URL de fuente, ningún diccionario de
variables. Todo veredicto PARCIAL en esta adenda lleva razón "requiere
inspección de instrumento" cuando esa es la causa — la sesión que abra el
instrumento se declara contaminada al hacerlo (ADR-46).

### 10 · Fuera de perímetro, y por qué no se tocó

No se bajó ninguna fuente. No se abrió ningún ADR. No se modificó
`milpa/procedencia.yaml` ni el modelo — si el cruce de arriba implicara
poblar el vector de confianza o resolver `[dominio]` de G1, eso es decisión
de mesa (`D-12` ya la dejó abierta) y esta sesión no la toma. No se
propusieron constructos nuevos: los 9 (más `acceso_digital`) son los que
`milpa/procedencia.yaml` y `canon/modelo-decision-v3_4.md` ya declaran.

---

> **NOTA FECHADA · 31/jul/2026 · sesión R4, resaca de ADR-49.** No se edita
> el cuerpo de arriba: este documento es **tipo (3)**, propuesta sin sello,
> y se respeta como tal (ver cabecera). Se deja constancia de que el
> **criterio de orden de la "Cola priorizada" de la adenda del 31/jul
> (§7, tabla de 10 filas, puesto 1 = `ENOE`) cayó con ADR-49 D1** y la cola
> **debe rederivarse antes de usarse para decidir qué bajar primero**. Dos
> motivos, ninguno resuelto aquí — no se reordena nada:
>
> 1. El puesto 1 (`ENOE`) se justifica explícitamente arriba (línea de la
>    tabla y el párrafo de criterio que la precede) por ser "la única con
>    ruta de calibración ya declarada en `procedencia.yaml`
>    (`unico_calibrable_hoy`)". Esa premisa es exactamente la que ADR-49 D1
>    retira — `unico_calibrable_hoy` se retira, no se corrige, porque la
>    vía que codificaba (ENOE → elasticidad `G3 → horizonte_temporal` vía
>    conducta financiera) es falsa a nivel de reactivo. Con la premisa
>    retirada, el criterio "distinto y más fuerte" que la adenda usa para
>    poner a `ENOE` por delante de fuentes que desbloquean más filas
>    (`ENDIREH`, `ENASIC`, `ENBIARE`, `ENASEM`) deja de sostenerse tal como
>    está escrito.
> 2. La misma cola lista a `ENOE`, `ENUT` (puesto 7) y `ENSANUT` (puesto 8)
>    como **"operables sin bajar"**. ⚠️ Esta nota **no verifica** ese estado
>    contra `data/manifiesto.yaml` — hacerlo sacaría a esta sesión de su
>    perímetro limpio (ADR-46). Se deja como **afirmación a verificar por
>    una sesión con acceso al manifiesto**, no como hecho: si alguna de las
>    tres ya está bajada, la cola tiene un segundo defecto independiente del
>    de D1.
>
> Ninguna de las dos observaciones reordena la cola — eso es decisión de
> mesa. Ambas quedan para que la sesión que reordene (o la que verifique el
> manifiesto) parta de aquí.

---

## 12 · Adenda 03/ago/2026 — `CAL-CONF` Fase A tumba dos veredictos SIN INSTRUMENTO; cierre de `D-12` re-declara la ficha de `G1`

**Disciplina aplicada:** adenda fechada, append-only. El cuerpo (§0–§11,
incluidas sus dos adendas del 31/jul) no se tocó — ni una palabra. Esta
sección es de otra sesión, con otra procedencia.

**Procedencia.** Tipo (1) para lo verificado contra archivo en esta sesión;
la premisa de qué dice `CAL-CONF` Fase A es tipo (3) hasta leerla aquí, y
tras leerla se sostiene. Fuentes: `forense/notas/2026-07-31-cal-conf-fasea.md`
(Fase A, íntegra); `forense/hallazgos.md`, entrada **2026-08-03** ("Cierre de
`D-12`"); `canon/gobernanza-v1_15.md` §4, entrada **ADR-51**; y, solo para
resolver que `G1a` sigue escrito como `confianza_institucional[dominio]` sin
componente fijo, `canon/modelo-decision-v4_0.md` líneas 386 y 394 (leídas,
no editadas — ADR-46 no se viola: son líneas de canon ya publicadas, no un
descriptor, cuestionario ni microdato). No se abrió ningún portal, cuestionario
adicional ni microdato. No se tocó `canon/` ni `milpa/`.

### 1 · Educación y financiera dejan de ser SIN INSTRUMENTO

`forense/hitoE-campana-medicion-v2_0.md:370-371` (esta misma sesión las leyó
sin cambios) marca **educación** y **financiera** como SIN INSTRUMENTO, celda
de fuente vacía. `CAL-CONF` Fase A — que abrió descriptor y cuestionario, no
solo alcance temático de catálogo — encontró para ambos un reactivo
**específico**, no adyacente:

- **Educación → INSTRUMENTADO.** Fase A, tabla "Resultado por componente":
  *"ENCUCI `AP5_2_6` 'Universidades' (`FD_ENCUCI2020.pdf`, pregunta 5.2, p.
  26) · ENCIG ítem 1 'Universidades públicas', ítem 16 'Escuelas públicas de
  nivel básico' (`encig21_cuestionario.pdf`, sección XI, p. 22)"*. Reactivo
  específico == "SÍ" en la columna de Fase A, mismo criterio que ya usa esta
  tabla para clasificar salud como INSTRUMENTADO ("declara explícitamente").
  No PARCIAL: no es alcance adyacente, es la variable nombrada.
- **Financiera → INSTRUMENTADO.** Fase A: *"ENIF, Sección 11 'Confianza y
  protección de personas usuarias de servicios financieros', `P11_1_1`-`P11_1_5`
  (`enif_2024_fd.xlsx`, hoja `TMODULO`; `enif_2024_cuestionario.pdf`, p.
  28)"* — y Fase A verificó aparte, sección "De paso", que la batería **no
  está condicionada** a tener producto financiero: todo entrevistado adulto
  la contesta. Fase A lo dice explícito: *"Esto tumba el veredicto SIN
  INSTRUMENTO que `forense/hitoE-campana-medicion-v2_0.md:370-371` declara
  para el componente financiero"*.

No se infla el estatus de los otros cuatro componentes. Fase A también
reporta reactivo específico para seguridad-FFAA, justicia-policía y
electoral-partidos (hoy PARCIAL en la tabla de §3) — pero revisar esos tres
es re-priorizar coberturas de la campaña, y el encargo que produce esta
adenda lo prohíbe expresamente ("no rederivar la cola priorizada de hitoE").
Queda anotado, sin actuar: otra sesión, contra el canon v4.0 completo.

**Tabla de §3, corregida solo en las dos filas que cambian:**

| Componente | Veredicto (antes) | Veredicto (ahora) | Candidata |
|---|---|---|---|
| educación | SIN INSTRUMENTO | **INSTRUMENTADO** | ENCUCI `AP5_2_6` "Universidades" |
| financiera | SIN INSTRUMENTO | **INSTRUMENTADO** | ENIF Sección 11, `P11_1_1`-`P11_1_5` |

### 2 · El razonamiento de `hitoE:373-377` caducó — la ficha de `G1` se re-declara

**Lo que decía.** `G1` usa `confianza_institucional[dominio]`, sin resolver
cuál de los seis componentes — atado a `D-12`, abierta — así que "no puede
siquiera evaluarse hasta que se decida el componente" y se contaba SIN
INSTRUMENTO por indeterminación, no por ausencia de fuente.

**Lo que cambió.** `forense/hallazgos.md`, entrada 2026-08-03: *"Cierre de
`D-12`... El reencuadre perfiles→atributos elimina esa tabla... `confianza_institucional`
sale de la clase 'inidentificable con cualquier número de momentos' y pasa a
IDENTIFICADO·TRUNCADO. ADR-51 es ese acto de mesa."* `canon/gobernanza-v1_15.md`
§4, ADR-51, lo confirma: *"cierra `D-12`"*. La causa que esta ficha citaba —
"no puede evaluarse hasta que se decida el componente" porque `modelo §1.1`
no daba valor por componente bajo perfiles — ya no existe: esa tabla se
eliminó.

**Lo que NO cambió, y por qué la ficha no pasa a INSTRUMENTADO.**
`canon/modelo-decision-v4_0.md:386` sigue escribiendo el coeficiente de `G1a`
como `confianza_institucional[dominio] −0.60` — sin componente fijo, a
diferencia de `G4` que usa `[justicia]` nombrado. La misma línea 394 lo
explica: el `−0.60` "se aplica al componente que el dominio seleccione"
(ADR-49, D3 — homogeneidad de pendientes declarada, no medida). `G1` no es
una ficha sobre un componente: es una ficha que puede aterrizar en
**cualquiera** de los seis, según qué regla de dominio dispare. Bajo el
modelo v4.0, esos seis se miden donde vive su instrumento — la tabla
corregida de §1 de esta adenda da: **3 INSTRUMENTADO** (salud, educación,
financiera), **3 PARCIAL** (seguridad-FFAA, justicia-policía, electoral-partidos),
**0 SIN INSTRUMENTO**. Ningún componente al que `G1a` pueda aterrizar queda
ya sin candidata — la indeterminación que justificaba SIN INSTRUMENTO
desapareció — pero tampoco los seis son INSTRUMENTADO, así que darle ese
estatus a la ficha sería inflarla sobre el peor caso posible.

**Re-declarado:** `G1` (`confianza_institucional[dominio]`) → **PARCIAL**
(antes SIN INSTRUMENTO). Mismo criterio de piso que usa esta tabla en otras
fichas con candidata adyacente, no textual, no confirmada por inspección
completa.

**Nota sin resolver, declarada y no actuada.** `canon/modelo-decision-v4_0.md:394`
trae, en la misma nota de ADR-49 D3, la frase *"No cierra `D-12`... sigue
abierta, es otro asunto"* — refiriéndose a si `G1a` debe desdoblarse en seis
`ASIGNADO` nombrados como `G4`. Esa frase, leída sola, contradice el cierre
que `hallazgos.md` (3/ago) y `gobernanza-v1_15.md` §4 (ADR-51) registran para
el mismo `D-12`. Esta adenda no la resuelve — no edita `canon/` — y sigue la
instrucción del encargo de verificar el cierre contra `hallazgos.md` (3/ago)
y ADR-51, las dos fuentes que el propio encargo señaló como autoridad. Se
deja la tensión anotada para que la sesión que sí pueda tocar `canon/` la
concilie.

### 3 · Efecto sobre el conteo del inventario, derivado

Unidad y aritmética son las que ya usa `hitoE:445-462` (§7, "Cobertura sobre
los 144 números") — no se inventa unidad nueva.

**Tabla §5 (15 fichas, `hitoE:402-419`).** Solo la fila de `G1` cambia (SIN
INSTRUMENTO → PARCIAL); ninguna otra fila la toca `educación`/`financiera`
porque no son coeficientes de generador, son componentes del vector que solo
`G1` y `G4` referencian. Antes: *"4 de 15 fichas tienen candidata (1
instrumentada + 3 parciales); 11 de 15 no tienen ninguna."* Ahora: **5 de 15
tienen candidata (1 instrumentada + 4 parciales); 10 de 15 no tienen
ninguna.**

**Tabla §6 (`hitoE:425-443`, criterio estricto/laxo).** Estricto
(INSTRUMENTADO puro) no cambia: sigue **1 de 15** (`exposicion_violencia`,
G4) — ni `G1` ni `educación`/`financiera` alimentan un coeficiente con
INSTRUMENTADO. Laxo (INSTRUMENTADO + PARCIAL) sube de 4 a **5 de 15**, por la
misma fila de `G1`.

**Tabla §7 (105 números constructo-parametrizados, `hitoE:449-455`).** La
fila de 90 `params_base` se reparte en 15 unidades × 6 perfiles (8
constructos no-confianza + 6 componentes del vector + `acceso_digital`, como
declara la adenda del 31/jul antes de esta tabla). Educación y financiera son
2 de esas 15 unidades, y las dos saltan de SIN INSTRUMENTO a INSTRUMENTADO
directo — sin pasar por PARCIAL, porque Fase A encontró reactivo específico,
no adyacente:

```
params_base (90 = 15 unidades × 6 perfiles):
  INSTRUMENTADO:      18 (3 unidades) → 30 (5 unidades)   Δ +12  (educación +6, financiera +6)
  PARCIAL:             24 (4 unidades) → 24 (4 unidades)   Δ  0
  SIN INSTRUMENTO:     48 (8 unidades) → 36 (6 unidades)   Δ −12

15 coeficientes (fichas, tabla §5):
  INSTRUMENTADO:  1 → 1   Δ  0
  PARCIAL:        3 → 4   Δ +1   (ficha de G1)
  SIN INSTRUMENTO:11 → 10  Δ −1

Subtotal 105 (15 + 90):
  INSTRUMENTADO:  19 → 31   Δ +12
  PARCIAL:        27 → 28   Δ +1
  SIN INSTRUMENTO:59 → 46   Δ −13
  (31 + 28 + 46 = 105 — se conserva el total, ✔)
```

**Sobre el "12 números recuperados" que circula:** sí se deriva de este
archivo, y es exactamente el número de arriba — **los 12 `params_base` de
educación (6 perfiles) y financiera (6 perfiles) que saltan de SIN
INSTRUMENTO a INSTRUMENTADO.** No es el efecto total sobre el inventario: el
efecto total, incluida la ficha de `G1`, es **+12 INSTRUMENTADO / +1 PARCIAL
/ −13 SIN INSTRUMENTO** sobre los 105 números constructo-parametrizados. Los
39 `probabilidades_de_regla` no se tocan — no son de esta familia, igual que
declara la tabla original.

### 4 · Límite de lectura declarado

Esta adenda leyó: `forense/hitoE-campana-medicion-v2_0.md` completo (para no
repetir lo que las dos adendas del 31/jul ya cubren); `forense/notas/2026-07-31-cal-conf-fasea.md`
completa; `forense/hallazgos.md` (entrada 2026-08-03, "Cierre de `D-12`");
`canon/gobernanza-v1_15.md` §4 (entrada ADR-51); `canon/modelo-decision-v4_0.md`
líneas 380-398 (tabla de coeficientes de generador y su nota de homogeneidad
de `G1a`). No se abrió ningún descriptor, cuestionario, portal ni microdato
nuevo — todo lo citado ya estaba escrito en Fase A o en canon publicado. No
se rederivó la cola priorizada de `§8`/`§9` de las adendas del 31/jul: sigue
como estaba.

## 13 · Adenda 03/ago/2026 — la nota "queda anotado, sin actuar" de `§12` se resuelve: los tres PARCIAL restantes también tienen reactivo específico

**Disciplina aplicada:** adenda fechada, append-only. El cuerpo (§0–§12) no
se tocó — ni una palabra, incluida la adenda de `PR #48`. Esta sección es de
otra sesión, con otra procedencia.

**Procedencia.** Tipo (3) hasta verificarla aquí: la premisa de qué dice
`CAL-CONF` Fase A sobre seguridad-FFAA, justicia-policía y electoral-partidos
viene citada de segunda mano en `§12.1` ("Fase A también reporta reactivo
específico... queda anotado, sin actuar") y de la adenda del `PR #48`; esta
sesión la contrasta contra `forense/notas/2026-07-31-cal-conf-fasea.md`
(Fase A, tabla "Resultado por componente", leída completa) — tipo (1) desde
aquí. También se leyó `forense/notas/2026-08-03-cal-conf-faseb-medicion.md`
§4 (íntegra esa sección), `data/manifiesto.yaml` (grep sobre los cuatro ids
de instrumento citados) y se corrió `tests/manifiesto.py --verifica` sobre
esos cuatro ids en esta sesión. No se abrió descriptor, cuestionario, portal
ni microdato nuevo — todo lo citado ya estaba escrito en Fase A. No se tocó
`canon/` ni `milpa/`. No se rederivó la cola priorizada de `§8`/`§9`.

### 1 · La premisa, verificada línea por línea contra Fase A

`§12.1` dice, sin actuar: *"Fase A también reporta reactivo específico para
seguridad-FFAA, justicia-policía y electoral-partidos (hoy PARCIAL en la
tabla de §3) — pero revisar esos tres es re-priorizar coberturas de la
campaña, y el encargo que produce esta adenda lo prohíbe expresamente."* El
encargo que produce **esta** adenda es distinto: pide leer Fase A
directamente y aplicar, sin inflar, el mismo criterio que ya clasificó salud
(y luego educación y financiera) como INSTRUMENTADO. Leída la tabla de Fase
A completa, la premisa se sostiene y con el mismo nivel de detalle que la
premisa exigía — variable, archivo, página — para los tres:

- **Seguridad-fuerzas armadas → SÍ, específico.** Fase A: *"ENVIPE `AP5_4_08`
  Ejército, `AP5_4_09` Fuerza Aérea, `AP5_4_10` Marina, `AP5_4_04` Guardia
  Nacional (`fd_envipe2025.pdf`, sección 5.4, pp. 33-34) · ENCUCI `AP5_3_4`
  'Ejército y Marina', `AP5_3_5` 'Guardia [Nacional]' (`FD_ENCUCI2020.pdf`,
  pregunta 5.3, p. 27) · ENCIG ítem 20 'Guardia Nacional', ítem 21 'Ejército
  y Marina' (`encig21_cuestionario.pdf`, sección XI, pregunta 11.1, p. 22)"*.
  Institución nombrada por variable, en tres instrumentos independientes —
  no "confianza en instituciones" sin desagregar.
- **Justicia-policía → SÍ, específico.** Fase A: *"ENVIPE `AP5_4_01/02/03/05`
  (policía de tránsito/preventiva/estatal/ministerial), `AP5_4_06` Ministerio
  Público, `AP5_4_07` Fiscalía General, `AP5_4_11` Jueces (pp. 29-34) ·
  ENCUCI `AP5_3_1` Jueces, `AP5_3_3` Policía (p. 27) · ENCIG ítem 2
  'Policías', ítem 17 'Jueces y Magistrados', ítem 22 'Ministerio Público'
  (p. 22)"*. Mismo patrón: variable nombrada por institución, tres
  instrumentos.
- **Electoral-partidos → SÍ, específico.** Fase A: *"ENCUCI `AP5_2_5`
  'Partidos' (p. 26), `AP5_3_6` 'Senadores federales', `AP5_3_7`
  'Diputados', `AP5_3_8` 'Instituto [Nacional Electoral]' (p. 27-28) · ENCIG
  ítem 12 'Cámaras de Diputados y Senadores', ítem 14 'Institutos
  electorales', ítem 19 'Partidos políticos' (p. 22)"*.

**El criterio que decide, aplicado sin inflar.** `§12.1` fijó la regla:
*"Reactivo específico == 'SÍ' en la columna de Fase A, mismo criterio que ya
usa esta tabla para clasificar salud como INSTRUMENTADO ('declara
explícitamente'). No PARCIAL: no es alcance adyacente, es la variable
nombrada."* Las tres filas de arriba cumplen exactamente esa condición — la
misma tabla de Fase A que trae "SÍ" para las tres, con variable, archivo y
página, y no "alcance temático" de catálogo (`data/catalogo-fuentes-v1_0.md`,
la fuente que sí sustentaba el PARCIAL original de `hitoE:367-369`). El
motivo original de PARCIAL — *"confianza en instituciones genérico, sin
desagregar el componente"* — era una lectura de catálogo, no de instrumento;
Fase A abrió el instrumento y encontró exactamente la desagregación que
faltaba. No se aplica aquí la regla de "no inflar": los tres reactivos no
son genéricos, y clasificarlos PARCIAL a estas alturas — con la cita en
mano — sería subestimar, no el error simétrico.

**Lo que esto NO dice.** Ningún componente tiene ya, en esta adenda, corte
formal/informal distinto del que Fase A ya reportaba (`§`"Corte
formal/informal" de la nota): los tres traen "SÍ, vía ENCUCI: mismo
`AP3_15_4`" — no cambia con esta corrección, solo el estatus de reactivo.

### 2 · Tabla de `§3`, corregida en las tres filas restantes

| Componente | Veredicto (antes, `§12`) | Veredicto (ahora) | Candidata |
|---|---|---|---|
| seguridad / FFAA | PARCIAL | **INSTRUMENTADO** | ENVIPE `AP5_4_04/08/09/10`, ENCUCI `AP5_3_4`/`AP5_3_5`, ENCIG ítem 20/21 |
| justicia-policía | PARCIAL | **INSTRUMENTADO** | ENVIPE `AP5_4_01/02/03/05/06/07/11`, ENCUCI `AP5_3_1`/`AP5_3_3`, ENCIG ítem 2/17/22 |
| electoral / partidos | PARCIAL | **INSTRUMENTADO** | ENCUCI `AP5_2_5`/`AP5_3_6`/`AP5_3_7`/`AP5_3_8`, ENCIG ítem 12/14/19 |

**Tabla de `§3` completa, hoy: 6 INSTRUMENTADO · 0 PARCIAL · 0 SIN
INSTRUMENTO.** Los seis componentes del vector `confianza_institucional`
tienen ya reactivo específico verificado contra descriptor/cuestionario en
al menos un instrumento.

### 3 · Cascada sobre las fichas de `§5` — `G1` deja de ser "el peor caso posible"; `G4` sube directo

**`G4` (`confianza_institucional[justicia]`), directo.** La ficha de `G4`
nombra el componente `justicia` explícitamente (`canon/modelo-decision-v4_0.md:392`).
Con justicia-policía → INSTRUMENTADO (§2 arriba), la ficha sube en el mismo
movimiento — no hay indeterminación de componente que resolver, a diferencia
de `G1`.

**`G1` (`confianza_institucional[dominio]`), por el piso.** `§12.2` razonó:
*"esos seis se miden donde vive su instrumento... tampoco los seis son
INSTRUMENTADO, así que darle ese estatus [a `G1`] sería inflarla sobre el
peor caso posible"* — y por eso dejó a `G1` en PARCIAL, el peor caso de los
seis en ese momento (3 INSTRUMENTADO, 3 PARCIAL). Con la corrección de `§2`
arriba, el peor caso posible entre los seis componentes es hoy
INSTRUMENTADO — no queda ningún componente al que `G1a` pueda aterrizar por
debajo de ese estatus. Mismo razonamiento de piso que usó `§12.2`, aplicado
al nuevo piso: **`G1` (`confianza_institucional[dominio]`) → INSTRUMENTADO**
(antes PARCIAL). Esto no resuelve `D-12` ni la pregunta de homogeneidad de
pendientes que `canon/modelo-decision-v4_0.md:396` deja abierta (si `G1a`
debe desdoblarse en seis `ASIGNADO` nombrados) — esa pregunta es sobre la
*forma* del coeficiente, no sobre si su componente tiene instrumento; sigue
sin decidir, y esta adenda no la toca.

**Tabla de `§5` (15 fichas), corregida:**

| Generador | Coeficiente | Veredicto (antes, `§12`) | Veredicto (ahora) |
|---|---|---|---|
| G1 | `confianza_institucional[dominio]` | PARCIAL | **INSTRUMENTADO** |
| G4 | `confianza_institucional[justicia]` | PARCIAL | **INSTRUMENTADO** |

Las 13 filas restantes de `§5` no cambian: `radio_confianza` (G1, G5),
`sens_estatus`/`aversion_riesgo`/`horizonte_temporal`/`familismo_apoyo`/`familismo_obligacion`/`deferencia`
no son componentes del vector `confianza_institucional` y Fase A no los
tocó. **Total `§5`: 3 INSTRUMENTADO (antes 1) · 2 PARCIAL (antes 4) · 10 SIN
INSTRUMENTO (sin cambio). 3+2+10=15.**

### 4 · Efecto derivado sobre `§6` y `§7`

**Tabla `§6` (estricto/laxo, 15 fichas).** Estricto (INSTRUMENTADO puro):
**1 → 3 de 15** (se suman `G1` y `G4`). Laxo (INSTRUMENTADO + PARCIAL): sigue
**5 de 15** — no cambia el total laxo, solo se redistribuye de PARCIAL a
INSTRUMENTADO dentro de él.

**Tabla `§7` (105 números, unidad y aritmética de `hitoE:445-462`, sin
inventar unidad nueva).** De las 15 unidades de `params_base` (8 constructos
no-confianza + 6 componentes del vector + `acceso_digital`, per `§12.3`),
las tres que suben son exactamente las tres de `§2` arriba — 3 unidades × 6
perfiles = 18 `params_base` que se mueven de PARCIAL a INSTRUMENTADO:

```
params_base (90 = 15 unidades × 6 perfiles), sobre el estado post-§12:
  INSTRUMENTADO:      30 (5 unidades) → 48 (8 unidades)   Δ +18  (seguridad-FFAA, justicia-policía, electoral-partidos, +6 c/u)
  PARCIAL:             24 (4 unidades) → 6 (1 unidad)      Δ −18  (queda solo radio_confianza)
  SIN INSTRUMENTO:     36 (6 unidades) → 36 (6 unidades)   Δ  0

15 coeficientes (fichas, tabla §5):
  INSTRUMENTADO:  1 → 3   Δ +2   (fichas de G1 y G4)
  PARCIAL:        4 → 2   Δ −2   (quedan radio_confianza de G1 y de G5)
  SIN INSTRUMENTO:10 → 10  Δ  0

Subtotal 105 (15 + 90), sobre el post-§12 (31/28/46):
  INSTRUMENTADO:  31 → 51   Δ +20
  PARCIAL:        28 →  8   Δ −20
  SIN INSTRUMENTO:46 → 46   Δ  0
  (51 + 8 + 46 = 105 — se conserva el total, ✔)
```

Los 39 `probabilidades_de_regla` no se tocan, igual que declaraba `§12.3`.

### 5 · Nota de consecuencia para Fase B — insumo para la segunda ola, declarado y no ejecutado

Los tres componentes que suben quedan con fuente y variable nombradas, en
los mismos tres instrumentos que la primera ola de Fase B
(`forense/notas/2026-08-03-cal-conf-faseb-medicion.md`) ya abrió a nivel de
microdato (ENCIG 2021, ENCUCI 2020) más uno que esa ola no abrió (ENVIPE
2025). Payload en disco, derivado con `tests/manifiesto.py --verifica`
corrido en esta sesión sobre los cuatro ids de instrumento citados — los
cuatro **AUSENTE** en esta sesión (el payload no se commitea; no es hallazgo
nuevo, mismo patrón que el resto del repo):

- **seguridad-FFAA** — fuente ENVIPE, variable `AP5_4_04`/`AP5_4_08`/`AP5_4_09`/`AP5_4_10`;
  id de manifiesto `envipe2025_fd_pdf` (`fd_envipe2025.pdf`) → AUSENTE en
  `data_raw` en esta sesión.
- **justicia-policía** — fuente ENVIPE, variable `AP5_4_01`/`02`/`03`/`05`/`06`/`07`/`11`;
  mismo id `envipe2025_fd_pdf` → AUSENTE.
- **electoral-partidos** — fuente ENCUCI, variable `AP5_2_5`/`AP5_3_6`/`AP5_3_7`/`AP5_3_8`;
  id de manifiesto `encuci2020_fd_pdf` (`FD_ENCUCI2020.pdf`) → AUSENTE.

(Los tres también tienen candidata en ENCIG — ids `encig2021_cuestionario_pdf`
y `encig2021_estructura_base_datos_pdf`, ambos verificados AUSENTE en esta
sesión también.) Ninguna cifra de esta sección se tecleó: los cuatro ids se
corrieron contra `tests/manifiesto.py --verifica` en esta misma sesión. Esta
adenda no mide — no abre microdato, no corre el script de Fase B — es
insumo declarado para quien ejecute esa segunda ola.

### 6 · Discrepancia señalada, no corregida

`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §4 describe a los tres
componentes de esta adenda como *"candidata adyacente, no reactivo textual
confirmado por inspección completa"* — heredado de la caracterización de
`§12` antes de esta corrección. Con `§1`-`§2` de esta adenda, esa frase ya
no describe lo que Fase A trae. Esta adenda no edita esa nota — es de otra
sesión, con su propia fecha — y la deja anotada para quien la mantenga.

### 7 · Límite de lectura declarado

Esta adenda leyó: `forense/hitoE-campana-medicion-v2_0.md` completo (para no
repetir §0-§12); `forense/notas/2026-07-31-cal-conf-fasea.md` completa;
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` (procedencia, §0 y §4);
`canon/modelo-decision-v4_0.md` líneas 386-396 (leídas, no editadas);
`data/manifiesto.yaml` (grep sobre los ids de `envipe2025_fd_pdf`,
`encuci2020_fd_pdf`, `encig2021_cuestionario_pdf`,
`encig2021_estructura_base_datos_pdf`) y corrió `tests/manifiesto.py
--verifica` sobre esos cuatro ids. No se abrió descriptor, cuestionario,
portal ni microdato nuevo. No se rederivó la cola priorizada de `§8`/`§9`
de las adendas del 31/jul: sigue como estaba.

---

## 14 · Adenda 03/ago/2026 — la cola priorizada de `§11` queda **REEMPLAZADA**: cola de medición rederivada contra el canon v4.0 completo

**Disciplina aplicada:** adenda fechada, append-only. El cuerpo (§0–§13,
incluidas las tres adendas previas) no se tocó — ni una palabra. Esta sección
es de otra sesión, con otra procedencia.

**Por qué el vehículo es `hitoE` y no una nota nueva** *(decidido contra la
convención del archivo, no heredado del encargo)*. La cola que se reemplaza
vive en **`§11`** de este archivo (`:278`, "Cola priorizada — de las 32
operables sin bajar, cuáles desbloquean más constructos", diez posiciones), y
la convención de este archivo para corregir su propio cuerpo es la adenda
fechada append-only que `§12` y `§13` ya usaron dos veces. Una cola de
reemplazo alojada fuera dejaría `§11:278` legible **sin marca de que está
vencida** — que es exactamente el patrón de propagación fallida que `§8` de
`canon/modelo-decision-v4_0.md` documenta ("dos de los seis casos figuraban
como reparados sin estarlo") y que ADR-29.a existe para impedir. El costo de
elegir este vehículo se declara: `hitoE` es tipo (3) y su cabecera dice
`CLASE: Propuesta. No es decisión. No rige sin ADR`. **Esta adenda hereda esa
clase entera: es una propuesta de orden de trabajo, no un acto de canon, y no
rige sin ADR.** No mueve ningún contador, no mide nada, no toca `canon/` ni
`milpa/`.

**Procedencia.** Tipo (1) para todo lo derivado contra archivo abajo. Las
premisas del encargo entraron como tipo (3) y se verificaron una por una en
`§14.0`; **una no se sostiene** y su caída se declara ahí con su consecuencia
sobre el contenido de la cola.

---

### 14.0 · Verificación de premisas antes de obedecer

| Premisa del encargo | Verificación | Veredicto |
|---|---|---|
| Existe una cola vieja en `hitoE §"Cola priorizada"` con **10 posiciones** | `forense/hitoE-campana-medicion-v2_0.md:278`, tabla de 10 filas numeradas (ENOE · ENDIREH · ENASIC · ENBIARE · ENASEM · ENSU · ENUT · ENSANUT · ENCUP · Global Findex) más una fila `—` de resto. *(Hay una segunda cola, de 9 posiciones, en `§8:464` de la otra adenda del 31/jul; no es la que el encargo nombra y esta adenda tampoco la rederiva — ver `§14.5`.)* | **SE SOSTIENE** |
| Su criterio de orden cayó con **ADR-49 D1** | El criterio de `§11` es "cuántas de las 14 filas desbloquea", **con una excepción declarada**: ENOE encabeza *"porque es la única fuente que `procedencia.yaml` ya declara calibrable con dato público (`unico_calibrable_hoy`)"*. `canon/modelo-decision-v4_0.md:400`: *"**`unico_calibrable_hoy` se retira (ADR-49, D1)** … la premisa muere a nivel de reactivo, no de tema."* El campo que sostenía la posición 1 ya no existe | **SE SOSTIENE** |
| **Tres** de sus posiciones ya están en disco | Derivado contra `data/manifiesto.yaml` (182 ids): **ENOE** (pos. 1) → `enoe_2019_1t_csv` … `enoe_2026_1t_csv`, 26 ids trimestrales + 6 cuestionarios; **ENUT** (pos. 7) → `enut2019_bd_csv`, `enut2024_bd_csv` (+2002/2009/2014); **ENSANUT** (pos. 8) → 23 ids (`hogar_ensanut2024_w_icb_csv_csv`, `adultos_ensanut2024_w_catlogo`, …). Las otras siete (ENDIREH, ENASIC, ENBIARE, ENASEM, ENSU, ENCUP, Global Findex) no tienen ningún id | **SE SOSTIENE — exactamente tres** |
| El reencuadre cambió la unidad de lo que se mide | `modelo` v4.0 cabecera (`:11`) y §1.1.F: la unidad pasa de *perfil × parámetro* a **condicional θ_k( · \| x )**, y `D`=14. La cola de `§11` ordena **fuentes a bajar** por *constructos que desbloquean*; ninguna de las dos unidades sobrevive intacta | **SE SOSTIENE** |
| El contador vigente es **3 de 14** con desglose 3 / 6 / 3 / 2 | Titular localizado en `modelo` **§1.1.F paso 5** (`:275`), repetido en **§6.1** (`:619`) y **§12** (`:723`), citando `forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §5. Desglose **rederivado abajo en `§14.1`, no copiado** | **SE SOSTIENE** |
| Las dos adendas de hitoE del 3/ago y sus efectos | `§12` (PR #48: educación y financiera dejan de ser SIN INSTRUMENTO) y `§13` (PR #52: los tres PARCIAL restantes también tienen reactivo específico; tabla de `§3` queda 6 INSTRUMENTADO · 0 PARCIAL · 0 SIN INSTRUMENTO) | **SE SOSTIENEN** |
| Veredictos de instrumento C / C-bis / P2 | `forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` §2.3 (ENUT `6.11`/`6.11a` → PROXY); `…/2026-08-03-cbis-deferencia-externas.md` §0 (Latinobarómetro `P4NOIJ` → PROXY; LAPOP SIN REACTIVO; WVS y ENCUP abiertas); `…/2026-08-01-p2-momentos-atributos.md` §2.c y §2.d | **SE SOSTIENEN** |
| **Precondición: "ola 2 de Fase B fusionada y su contador propagado"** | `origin/main` = `f6bcaaa`. Fusionado hay: **ola 1** de Fase B (PR #50, `7f53fa7`, mide salud/educación/financiera), **la propagación del contador** (PR #51, `c658b96`) y **la adenda `§13`** (PR #52, `75b12c5`). La **ola 2 no existe**: `§13.5` la titula literalmente *"insumo para la segunda ola, **declarado y no ejecutado**"* y declara sus tres componentes con fuente y variable pero sin medición | ❌ **NO SE SOSTIENE** |

**Por qué esta sesión no se detiene, dicho con la consecuencia.** La regla del
encargo es *"DETENTE si una premisa cae"*. La premisa caída es una
**precondición de higiene**, y lo que protege —*"la cola se deriva contra el
estado final, no contra uno en tránsito"*— **sí se cumple**: `origin/main` está
en `f6bcaaa`, el árbol de trabajo limpio, no hay rama viva salvo la de esta
sesión, y el contador **está** propagado a `canon` en tres sitios. Lo que la
premisa erró no es el estado del repo sino **qué es la ola 2**: no es un
insumo ya consumado de la cola, es **materia de la cola**. La consecuencia es
directa y visible abajo: los tres componentes restantes de
`confianza_institucional` **son posiciones 1–3**, no trabajo hecho. Detenerse
habría entregado cero y dejado la cola vieja vigente por omisión; se declara
el defecto y se sigue, que es lo que `instrucciones` v2.1 pide de quien
ejecuta. **Segunda caída, del mismo tronco:** el encargo dice
*"`exposicion_violencia` (ENVIPE, que la ola 2 ya abrió)"* — **ENVIPE no está
abierta**. `§13.5` la nombra como *"uno que esa ola no abrió (ENVIPE 2025)"*.
`exposicion_violencia` no cobra descuento de instrumento-ya-abierto en el
orden de abajo.

---

### 14.1 · El desglose de las 14, derivado

Derivado de `modelo` §1.1.F paso 1–2 (los 15 parámetros menos `acceso_digital`,
que sale por C3) y de los veredictos de instrumento de C, C-bis y P2 §2.c —
no copiado del titular:

**Las 14** = 8 escalares (`horizonte_temporal`, `radio_confianza`,
`aversion_riesgo`, `sens_estatus`, `deferencia`, `familismo_apoyo`,
`familismo_obligacion`, `exposicion_violencia`) + 6 componentes de
`confianza_institucional` (seguridad-FFAA, educación, salud, electoral-partidos,
justicia-policía, financiera).

| Clase | Cuáles | n |
|---|---|---|
| **MEDIDO·PARCIAL(x)** | `confianza_institucional[salud]` (ENCIG `P11_1_3`) · `[educación]` (ENCUCI `AP5_2_6`) · `[financiera]` (ENIF `P11_1_1`-`P11_1_5`) | **3** |
| **Reactivo directo localizado, sin medir** | `radio_confianza` (ENCUCI `AP5_1_1/2/3`) · `exposicion_violencia` (ENVIPE `BP1_20/23/28`) · `familismo_apoyo` (ENIF `P9_9_1..6`) · `confianza_institucional[seguridad-FFAA]` (ENVIPE `AP5_4_04/08/09/10`) · `[justicia-policía]` (ENVIPE `AP5_4_01/02/03/05/06/07/11`) · `[electoral-partidos]` (ENCUCI `AP5_2_5`, `AP5_3_6/7/8`) | **6** |
| **Solo proxy localizado** | `horizonte_temporal` (ENIF `P4_10`, ⚠️ falla C3) · `familismo_obligacion` (ENUT `6.11`/`6.11a`) · `deferencia` (Latinobarómetro `P4NOIJ`) | **3** |
| **Sin reactivo o no determinable en este régimen** | `sens_estatus` · `aversion_riesgo` | **2** |
| | **3 + 6 + 3 + 2** | **14** ✔ |

Coincide con el titular de `modelo:723`. El control es el que importa: **la
suma cierra en 14 por derivación independiente**, no por copia.

---

### 14.2 · El criterio, declarado antes de la lista

Se toma la propuesta del encargo, **con dos cambios derivados** que se
declaran en vez de aplicarse en silencio. Es **un** criterio, escrito arriba y
aplicado parejo a las doce posiciones.

**Compuerta de factibilidad (se aplica antes de ordenar, no es un nivel).** Una
posición entra como **medición** solo si cumple las dos:

- **(i) payload registrado** — el instrumento tiene id en `data/manifiesto.yaml`;
- **(ii) co-observación** — reactivo y **condicionantes** salen del **mismo
  instrumento**. No es cautela: `canon` §1.1.C dice *"la síntesis amplía la
  malla de atributos; no amplía la malla de pares (parámetro, desenlace)"*, y
  Fase B §0 ya derivó la consecuencia — condicionar sobre ejes de ENIGH vía
  reponderación **fabricaría una conjunta que nadie midió**.

Lo que falla (i) entra como posición de **desbloqueo** (descarga), no de
medición. Lo que falla (ii) **no entra**: es límite, y va a `§14.4`.

**Orden, por lo que la posición cierra — estrictamente en este orden:**

- **(a)** mueve el contador `3 de 14` **directamente** (medición de una
  condicional con reactivo directo);
- **(b)** desbloquea una **decisión pre-registrada pendiente** — P3 (LCA,
  `forense/p3-lca-preregistro-v1_0.md` §6.1) o P4 / desdoblamiento de G1a
  (`modelo:396`, pre-registro de ADR-49 D3);
- **(c)** cierra un parámetro cuyo **proxy ya está localizado**;
- **(d)** todo lo demás.

**Desempate dentro de cada nivel, en orden:** 1) payload registrado **y ningún
insumo faltante declarado** — no basta el payload si la posición está bloqueada
por otra cosa; 2) es prerequisito de una posición posterior; 3) cierra una
segunda cosa además de la que la clasifica.

**Los dos cambios respecto de la propuesta del encargo, y por qué.** El primero
es la **compuerta**: sin ella, una posición que "mueve el contador" pero cuyo
microdato nadie puede abrir encabezaría la cola, y el encargo prohíbe fabricar
urgencia. El segundo es el **primer desempate**: el encargo dice "primero lo
que tiene payload ya registrado"; se le añade *"y ningún insumo faltante"*
porque hay al menos una posición (P4) con payload completo y **bloqueada por
una co-observación que no está establecida en archivo** — ordenarla por payload
sola la pondría por delante de una posición ejecutable hoy.

---

### 14.3 · La cola — doce posiciones

**Sesión-tipo, vocabulario del repo, no inventado aquí:** **Ubuntu microdato**
= sesión Ubuntu local, *"única vertiente con salida a dominios de datos
mexicanos"* (`forense/notas/2026-07-31-perimetro-descarga.md:3`) y el checkout
que monta `data_raw`; contamina por ADR-46 al abrir microdato. **Navegador del
autor** = lo que `data/manifiesto.yaml` registra como `descargado_por: usuario,
vía navegador (la SPA de INEGI no expone el enlace a herramientas headless)`
(`encig23_base_datos_csv`, `encuci2020_bd_dbf`), y la vía para portales con
licencia/registro (Encargo C §3.4). **Mesa** = decisión, no medición.

#### Nivel (a) — mueven el contador directamente

| # | Qué se mide | Fuente · variable (citada) | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **1** | `confianza_institucional[justicia-policía]` | **ENVIPE**, `AP5_4_01/02/03/05/06/07/11` (`§13.5`) | Contador → 4/14. **Segunda cosa que cierra** (desempate 3): P2 §2.d marca el coeficiente `G4 · confianza_institucional[justicia]` **JUSTO IDENTIFICADO** con C1 *"solo por **proxy**"* (ENVIPE `AP5_5_*`, percepción de corrupción). Medir `AP5_4_*` sustituye ese proxy por reactivo directo **en el mismo instrumento** | `envipe2025_fd_pdf` + microdato `envipe2018_csv`…`envipe2025_csv` — **registrados** | Ubuntu microdato |
| **2** | `confianza_institucional[seguridad-FFAA]` | **ENVIPE**, `AP5_4_04/08/09/10` (`§13.5`) | Contador → 5/14. Prerequisito de la posición 8 (P4) | mismos ids — **registrados** | Ubuntu microdato |
| **3** | `confianza_institucional[electoral-partidos]` | **ENCUCI**, `AP5_2_5` · `AP5_3_6/7/8` (`§13.5`) | Contador → 6/14. Cierra los **seis** componentes del vector de ADR-28.b: prerequisito de la posición 8 | `encuci2020_fd_pdf` + `encuci2020_bd_dbf` — **registrados**; instrumento **ya abierto** por Fase B ola 1 | Ubuntu microdato |
| **4** | `exposicion_violencia` | **ENVIPE**, `BP1_20`/`BP1_23`/`BP1_28` (P2 §2.c, inventario l.353) | Contador → 7/14. Es además la C1 del coeficiente `G4 · exposicion_violencia`, **IDENTIFICADO·TRUNCADO** (P2 §2.d) | mismos ids que 1–2 — **registrados**. ⚠️ ENVIPE **no** está abierta: `§13.5` la nombra como la que la ola 1 *no* abrió | Ubuntu microdato |
| **5** | `radio_confianza` | **ENCUCI**, `AP5_1_1`/`AP5_1_2`/`AP5_1_3` (P2 §2.c, inventario l.264) | Contador → 8/14. Es la C1 de `G1 · radio_confianza`, **IDENTIFICADO** (P2 §2.d) | `encuci2020_bd_dbf` — **registrado**; instrumento ya abierto | Ubuntu microdato |
| **6** | `familismo_apoyo` | **ENIF**, `P9_9_1..6` (P2 §2.c, inventario l.171) | Contador → 9/14. C1 de `G3 · familismo_apoyo`, **IDENTIFICADO**, sobre *"ENIF 6 ejes estrictos, la malla más rica del corpus"* (P2 §2.d) | `enif2024_csv` — **registrado**; instrumento ya abierto por Fase B ola 1 | Ubuntu microdato |

> **Nota de ejecución, no de orden.** Las posiciones 1, 2 y 4 comparten
> instrumento (ENVIPE) y las 3 y 5 comparten instrumento (ENCUCI): son dos
> sesiones, no cinco. Agrupar por instrumento es economía de ejecución y **no
> reordena nada** — el orden de arriba sale del criterio, no del calendario.

#### Nivel (b) — desbloquean una decisión pre-registrada pendiente

| # | Qué se hace | Fuente · variable | Qué decide | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **7** | **Ejecutar P3** — LCA de segmentación | **ENIGH 2022 nueva serie**, `enigh2022_nc_csv`; siete indicadores citados de `p3-lca-preregistro-v1_0.md` §2.1: `segsoc` · `edad` · `residencia` · `tam_loc` · `est_socio` · `celular` (SERV_2) · `conex_inte` (SERV_4); `k` = 1…8, regla de decisión sellada en §3.3 | **No mueve el contador** — el propio pre-registro lo prohíbe (§6.2 punto 4, §7 punto 2: *"cero de las 14 condicionales. Ni una."*). **Decide canon:** cuál de D1–D6 de la tabla §6.1, y bajo D2/D4/D6 el destino de los seis descriptores de `modelo` §1.1.D. Es la prueba de falsabilidad de la segmentación | `enigh2022_nc_csv` — **registrado**, sha256 verificado por P1 y citado por P3 §2.1 | Ubuntu microdato. ⚠️ El ejecutor **no puede** ser una sesión que haya escrito el pre-registro, y §6.1·D4 le **prohíbe** reescribir §1.1.D con las clases que le salgan |
| **8** | **P4** — dispersión de confianza entre instituciones condicionada a atributos | Batería completa de confianza institucional en **un solo instrumento**; la candidata nombrada para el vector completo es **ENCIG batería XI** (P2 §2.d, C1; `modelo` §1.3) | Decide **si `G1a` se desdobla** en seis `ASIGNADO` nombrados, como ya hace `G4`. Pre-registro escrito antes del dato en `modelo:396` (ADR-49 D3): *"si la dispersión entre componentes es la que ADR-28.b sostiene (Marina 89% vs. partidos 23.9%), la pendiente común queda implausible"* | **Bloqueada — no por payload.** Ver evaluación abajo | Mesa primero (definir la co-observación), luego Ubuntu microdato |

> **Evaluación de P4, que el encargo pide explícitamente: ¿ya es corrible con
> las mediciones de Fase B?** **No, y el faltante es nombrable.** P4 compara
> **entre componentes**; las tres condicionales que Fase B midió salen de
> **tres instrumentos distintos** —salud de ENCIG, educación de ENCUCI,
> financiera de ENIF (`§14.1`)—, así que una dispersión *entre* ellas
> condicionada a atributos exigiría cruzar instrumentos: **exactamente la
> conjunta que §1.1.C prohíbe fabricar** y que la propia Fase B §0 declaró como
> el matiz que tumba la premisa de condicionar sobre los ejes de ENIGH.
> Completar las posiciones 1–3 **tampoco** lo resuelve por sí solo: deja los
> seis componentes medidos, pero repartidos entre ENVIPE, ENCUCI y ENIF/ENCIG.
> **Lo que le falta a P4, dicho como tarea y no como deseo:** verificar si la
> **batería XI de ENCIG cubre los seis componentes** — hoy consta en archivo
> que cubre salud (`P11_1_3`, medido) y que es *"candidata adyacente"* para los
> tres de `§13.5` (ids `encig2021_cuestionario_pdf`,
> `encig2021_estructura_base_datos_pdf`), pero **que cubra educación y
> financiera no está establecido en ningún archivo leído aquí**. Ese chequeo
> —descriptor, no microdato— es el primer paso de la posición 8, y si sale
> negativo P4 **no es corrible en este régimen** y eso mismo es su resultado.
> **Ninguna cifra se teclea aquí:** el `Marina 89% / partidos 23.9%` de arriba
> es cita literal de `modelo:396`, que a su vez es lo que P4 va a contrastar.

#### Nivel (c) — cierran un parámetro con proxy ya localizado

| # | Qué se mide | Fuente · variable (citada) | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **9** | `familismo_obligacion` — carga de cuidado intra-hogar por persona | **ENUT** 2019 y 2024, preguntas `6.11`/`6.11a`: `P6_11_01`…`P6_11_11` (11 tareas de cuidado) y `P6_11A_XX_1`…`P6_11A_XX_4` (tiempo, lun-vie vs. sáb-dom). Encargo C §2.2, verificado persistente entre ediciones | **PROXY con supuesto declarado**, no reactivo directo: *"carga de cuidado alta y asimétrica ≈ conducta consistente con obligación internalizada — no la prueba"* (C §2.3). **Si eso cuenta o no en el contador `3 de 14` es decisión de mesa, no de esta cola** — por eso es nivel (c) y no (a). Cierra además la mitad medible del check de ADR-30 (contraste apoyo vs. obligación) que P2 §3.b declaró PERSISTENTE, porque `6.16` (ayuda **inter**-hogar) da el contraste dentro del mismo instrumento | `enut2019_bd_csv`, `enut2024_bd_csv` (+2002/2009/2014) — **registrados** | Ubuntu microdato |
| **10** | `horizonte_temporal` | **ENIF**, `P4_10` *"¿por cuánto tiempo cubriría gastos con ahorros?"* (P2 §2.c, inventario l.320) | PROXY (*"stock de ahorro ≠ tasa de descuento"*). ⚠️ **Falla C3** y hay que decir para qué: `P4_10` **es** la variable con la que Tabla B observa `dinero.ahorro.volatilidad_horizonte_corto`, el desenlace de G3 (P2 §2.d) — medir la condicional es legítimo, **usarla después para identificar `G3 · horizonte_temporal` es circular**. Compra la condicional, no el coeficiente | `enif2024_csv` — **registrado** | Ubuntu microdato |
| **11** | `deferencia` — **desbloqueo, no medición** | **Latinobarómetro 2024**, ítem `P4NOIJ` "Obediencia" entre las cualidades a inculcar en los niños (C-bis §0) | PROXY con supuesto declarado. **Falla la compuerta (i):** `data/manifiesto.yaml` registra `latinobarometro2024_cuestionario_esp` y `latinobarometro2024_fichas_tecnicas` — **el microdato no está registrado**. La posición es la descarga, no la estimación | Cuestionario y ficha **registrados**; microdato **ausente del manifiesto**. Fricción de licencia/registro de usuario, no bloqueo técnico (C §3.4) | **Navegador del autor** |

#### Nivel (d) — todo lo demás

| # | Qué se hace | Fuente | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **12** | Cerrar las **dos candidatas abiertas de `deferencia`** que C-bis dejó sin agotar | **WVS Ola 7** — `WVS7 Questionnaire Mexico 2018 Spanish.pdf`, `DOID 6635`, `SAID 3203` (localizado con precisión, **no legible** con las herramientas de esa sesión) · **ENCUP** — portal INEGI confirmado sin instrumento estático; ruta de recuperación `fomentocivico.segob.gob.mx`, fuera de los hosts alcanzables del sandbox | No mueve el contador. **Mejoraría el proxy** de la posición 11: C-bis declara que WVS *"es la candidata que la literatura señala como más probable de tener el reactivo mejor formulado … y queda sin cerrar, no descartada"* | Ninguno registrado | **Navegador del autor** |

---

### 14.4 · Lo que NO entra en la cola — límite vigente, con cita

**No son posiciones y no se les fabrica urgencia.** Son las 2 de las 14 sin
reactivo ni proxy, y su estado es un **límite de régimen**, no una tarea
pendiente:

| Condicional | Estado | Cita |
|---|---|---|
| **`sens_estatus`** | **NO DETERMINABLE EN ESTE RÉGIMEN.** Ningún reactivo de sensibilidad a estatus **reportado**; vive en §3.1/§3.9, dominios **no prioritarios** del inventario, que *"solo trae filas sí/parcial, así que no se puede distinguir 'no reportado' de 'no existe'"*. El desenlace sí existe (ENIGH `gastotarjetas`) y las celdas también — lo que falta es la C1 | P2 §2.c y §2.d (`G2 · sens_estatus`, `G4 · sens_estatus`) |
| **`aversion_riesgo`** | **NO DETERMINABLE EN ESTE RÉGIMEN.** El único candidato, ENIF `P5_23`/`P5_24`, mide **conocimiento de protección de depósitos IPAB**: es *"el moderador que la regla `dinero.ahorro.seguro_deposito_atenua_aversion` pone en el `SI`, no una medida de aversión"* | P2 §2.c y §2.d (`G2`/`G3 · aversion_riesgo`) |

**Ninguna de las dos se colapsa a "no existe en el dato mexicano".** Levantar
el límite exige graduar los dominios §3.1/§3.9 del inventario — **un acto de
inventario, no una medición**, y por eso no es posición de esta cola. Que
`Global Findex` figurara en la posición 10 de la cola vieja como candidata a
`aversion_riesgo` no cambia esto: la propia fila declaraba que la fuente
*"declara 'gestión de riesgo financiero', no una escala de aversión al riesgo"*
(`§11:278`, fila 10).

---

### 14.5 · Qué queda vencido, qué no

- **`§11:278` ("Cola priorizada — de las 32 operables sin bajar")** →
  **REEMPLAZADA** por `§14.3`. No se edita ni se hereda: sigue legible como
  registro histórico, con esta marca.
- **`§8:464` (la otra cola, 9 posiciones, adenda del 31/jul)** → **no se
  rederiva aquí**. El encargo nombra una cola de 10 posiciones y esa es la de
  `§11`. `§8` ordena lo mismo —fuentes operables sin bajar— con el mismo
  criterio de constructos desbloqueados, así que hereda las mismas tres vías de
  caducidad; **decir eso no es rederivarla** y esta adenda no la sustituye.
  Queda declarado, no ejecutado, igual que `§13.7` lo dejó.
- **`p3-lca-preregistro-v1_0.md` §6.2 punto 4** dice *"'0 de 14 condicionales
  medidas' sigue siendo 0"*. El contador es hoy **3**; la afirmación
  **sustantiva** del punto —que el LCA no estima ningún θ_k y no mueve el
  contador— **sigue en pie** y es la que la posición 7 usa. **Discrepancia
  señalada, no corregida:** es un pre-registro **sellado** y esta adenda no lo
  edita.

---

### 14.6 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/hitoE-campana-medicion-v2_0.md` completo;
`canon/modelo-decision-v4_0.md` §1.1.F, §1.2, §1.3, §2.2, §6.1, §7, §12
(leídas, no editadas); `canon/gobernanza-v1_15.md` (ADR-28.a, ADR-50, ADR-51,
por `grep`); `forense/p3-lca-preregistro-v1_0.md` §2.1, §2.2, §6, §7;
`forense/notas/2026-08-01-p2-momentos-atributos.md` §2.c y §2.d;
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §0 y §5;
`forense/notas/2026-08-03-cbis-deferencia-externas.md` §0–§3;
`forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` completa;
`revision-programa-2026-07-31.md` §5–§7; `forense/hallazgos.md`;
`data/manifiesto.yaml` (enumeración de ids por patrón).

**Cero portales, cero cuestionarios, cero descriptores, cero microdato.** Esta
adenda **no mide nada** — ordena. Ninguna cifra de este documento se tecleó:
las variables, ids y veredictos son citas de las notas nombradas, y el estado
de payload sale de enumerar `data/manifiesto.yaml`.

⚠️ **Qué significa exactamente "payload registrado" arriba, y qué no.**
`python3 tests/manifiesto.py --verifica` se corrió en esta sesión: **este
entorno no monta `data_raw`** (todos los ids dan `AUSENTE — el payload no se
commitea`, y las raíces `descargas_mx` dan `RAÍZ NO CONFIGURADA`). Por tanto el
hecho verificable que esta adenda afirma es **"registrado en
`data/manifiesto.yaml`"**, nunca "está en disco". Quien ejecute cualquier
posición corre `--verifica` en el entorno que sí monta la raíz **antes** de
empezar.

### 14.7 · Fuera de perímetro, y por qué no se tocó

No se tocó `canon/` ni `milpa/`. No se selló ningún ADR. No se movió ningún
contador. No se editó `§11` ni ninguna línea del cuerpo `§0`–`§13`. No se
rederivó la cola de `§8`. No se corrigió `p3-lca-preregistro-v1_0.md` §6.2
punto 4 (sellado). No se descargó ninguna fuente.

---

## 15 · Adenda 04/ago/2026 — corrige fila 4 de `§14.3`: `exposicion_violencia` sigue sin fuente verificada

**Disciplina aplicada:** adenda fechada, append-only. `§14.3` no se edita —
la fila 4 queda íntegra, con esta marca de que está vencida en su columna
"Fuente · variable"; el resto de sus columnas (posición, contador de
destino, mención de `C1` de `G4`) no cambia.

**Clase: Corrección de fila, misma clase que `§14` entero — Propuesta. No
es decisión. No rige sin ADR.**

**Qué pasó.** La sesión que ejecutó la posición 4 (`PR #57`,
`forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`) verificó el
descriptor de `BP1_20`/`BP1_23`/`BP1_28` contra `fd_envipe2025.pdf` y
encontró que el trío no mide `exposicion_violencia`: `BP1_20` es *"¿Acudió
a denunciar el delito?"*, condicionado por construcción de `TMod_Vic` a ya
haber sido víctima — mide conducta de denuncia, no exposición a violencia.
Detalle completo, con las tres razones verificadas contra `canon` y
`milpa/`, en esa nota §4.0 y en `forense/hallazgos.md` (entrada
04/ago/2026).

**Origen del defecto, para que la próxima cola no lo repita.** La fila 4
citó `P2 §2.c, inventario l.353` y `P2 §2.d` sin que ninguna sesión
verificara el descriptor de `BP1_20` contra el cuestionario antes de
escribir la fila — exactamente el paso que esta adenda de `§14` (arriba,
`§14.6`) declara *"no mide nada — ordena"*: la cola se construyó citando
notas, no reactivos verificados. `P2:229` marca el trío como *"reportado"*,
no *"verificado"* — la distinción que `instrucciones` v2.1 exige y que
esta fila no propagó.

**Consecuencia sobre la fila 4, dicha con precisión.** La posición **sigue
viva**: `exposicion_violencia` sigue siendo el único de los 8 escalares
restantes con marca `IDENTIFICADO` en P2 (`§2.d`), y sigue sin medir — el
contador no se movió (`PR #57` lo corrigió de vuelta a 6/14). Lo que cae es
solo la columna "Fuente · variable" de la fila: **`BP1_20`/`BP1_23`/`BP1_28`
quedan retirados como su reactivo**, y ninguna fuente/variable los
sustituye todavía. Encontrar el reactivo correcto de `exposicion_violencia`
—si existe uno en el corpus ya inventariado, o si el parámetro cae a
`NO DETERMINABLE EN ESTE RÉGIMEN` como `sens_estatus`/`aversion_riesgo`
(`§14.4`)— es trabajo de otra sesión, no de esta adenda.

**Fila 4, `§14.3`, corregida:**

| # | Qué se mide | Fuente · variable (citada) | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **4** | `exposicion_violencia` | **PENDIENTE DE VERIFICACIÓN** — `BP1_20`/`BP1_23`/`BP1_28` de ENVIPE **retirados**: miden conducta de denuncia condicionada a victimización, no exposición a violencia (`PR #57`, `forense/hallazgos.md` 04/ago/2026) | Contador → 7/14, sin cambio de destino. Sigue siendo la C1 del coeficiente `G4 · exposicion_violencia`, **IDENTIFICADO·TRUNCADO** en P2 (`§2.d`) — esa marca de P2 hereda el mismo rótulo sin verificar y no se corrige aquí | Sin determinar | Sin determinar hasta localizar reactivo |

**Efecto sobre `civico.denuncia.con_seguro` y
`comunicacion.inseguridad.ver_oir_callar`, señalado sin resolver.** `PR
#57` §4.2 encuentra que `BP1_20`/`BP1_28` (con `BP2_1` faltante) son
candidato cercano para `civico.denuncia.con_seguro` (P2:248,
`IDENTIFICADO`, regla de probabilidad libre — no una de las 14
condicionales, no mueve este contador) y que `BP1_23` es candidato para
`comunicacion.inseguridad.ver_oir_callar` (P2:264, `C2` `Parcial` de
`G4`). Ninguno de los dos se adjudica aquí — es exactamente el trabajo de
inventario que `§14.6` reserva a otra sesión.

### 15.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`
completa (§0.2, §4.0-§4.2, §5); `forense/hallazgos.md` (entrada nueva);
`canon/modelo-decision-v4_0.md:365-380` (tabla de generadores); esta
sección (`§14.3`-`§14.7`) para no repetirla. No se abrió microdato nuevo,
no se leyó cuestionario ni descriptor — la verificación del reactivo la
hizo la sesión de `PR #57`, citada aquí, no re-derivada. No se tocó
`canon/` ni `milpa/`. No se movió ningún contador (sigue en 6/14, `PR
#57`). No se rederivó ninguna otra fila de `§14.3`.

---

## 16 · Adenda 04/ago/2026 — cierra fila 8 de `§14.3`: P4 no es corrible en este régimen, faltante nombrado

**Disciplina aplicada:** adenda fechada, append-only, mismo mecanismo que
`§15`. `§14.3` no se edita — la fila 8 queda íntegra; esta adenda registra
el resultado del paso 1 que la propia fila declaraba pendiente ("Bloqueada
— no por payload. Ver evaluación abajo").

**Clase: Corrección de fila, misma clase que `§14` entero — Propuesta. No
es decisión. No rige sin ADR.**

**Qué pasó.** La sesión que ejecutó el paso 1 de la posición 8 (`PR #58`,
`forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md`) verificó si
la batería XI de ENCIG 2021 (25 ítems, sección "Confianza en
instituciones") cubre, en un solo instrumento, los seis componentes de
`confianza_institucional` de ADR-28.b — la condición que la evaluación de
`§14.3` (arriba) dejó como "primer paso de la posición 8". Verificado
contra `encig21_cuestionario.pdf` y `encig21_estructura_base_datos.pdf`,
ítem por ítem: **CUBIERTO** salud (`P11_1_3`), educación (`P11_1_1`,
`P11_1_16`), seguridad-FFAA (`P11_1_20`, `P11_1_21`), justicia-policía
(`P11_1_2`, `P11_1_17`, `P11_1_22`), electoral-partidos (`P11_1_14`,
`P11_1_19`) — **NO CUBIERTO** financiera: ningún ítem de los 25 mide
confianza en una institución de servicios financieros; el candidato más
cercano por nombre (`P11_1_5`, "Empresarios") descarta por descriptor —
confianza en un actor social, no en una institución financiera. Detalle
completo, con las 25 filas y el veredicto por componente, en esa nota §1-§3.

**Consecuencia sobre la fila 8, dicha con precisión.** Ningún instrumento
del corpus trae los seis componentes de `confianza_institucional` en una
sola batería — completar posiciones 1-3 de esta misma cola tampoco lo
resuelve, porque deja los seis medidos pero repartidos entre ENVIPE, ENCUCI
y ENIF/ENCIG (la evaluación de arriba ya lo anticipaba). Medir la
dispersión *entre* componentes exigiría cruzar instrumentos distintos —
exactamente la conjunta que `modelo` §1.1.C prohíbe fabricar. **P4 no es
corrible en este régimen, y ese es su resultado, no una tarea pendiente**
— mismo tipo de límite que las 2 de `§14.4` (`sens_estatus`,
`aversion_riesgo`): no se colapsa a "P4 no existe", se registra como
**NO DETERMINABLE EN ESTE RÉGIMEN sin fabricar una conjunta prohibida**,
con el faltante nombrado (**financiera**) para que quede verificable, no
solo declarado. **Esto no decide si `G1a` se desdobla en seis `ASIGNADO`**
— `canon/modelo-decision-v4_0.md:396` (ADR-49 D3) registra el mismo cierre
por enmienda in situ: el pre-registro corrió y su resultado es que el dato
no puede llegar en este régimen, así que la pregunta de homogeneidad de
pendientes **vuelve a mesa**, no se resuelve aquí.

**Fila 8, `§14.3`, corregida:**

| # | Qué se hace | Fuente · variable | Qué decide | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **8** | **P4** — dispersión de confianza entre instituciones condicionada a atributos | Batería completa de confianza institucional en **un solo instrumento**; ENCIG batería XI verificada (`PR #58`): cubre 5 de 6 (falta financiera) | **NO DETERMINABLE EN ESTE RÉGIMEN** sin fabricar la conjunta que §1.1.C prohíbe — faltante nombrado: **financiera**. No decide el desdoblamiento de `G1a`; la pregunta vuelve a mesa (`modelo:396`, ADR-49 D3, enmienda in situ 4/ago/2026) | Chequeo de batería corrido — **NO CUBIERTO** financiera | Ubuntu microdato (`PR #58`) |

### 16.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md`
completa (§1-§5); `canon/modelo-decision-v4_0.md:396` (enmienda in situ,
misma sesión); esta sección (`§14.3`, `§16` para no repetirla). No se abrió
microdato de ENCIG (`encig2021_csv.zip`) — el chequeo de la batería XI lo
hizo la sesión de `PR #58`, citada aquí, no re-derivada. No se tocó
`milpa/`. No se movió ningún contador (P4 no mueve contador — `hitoE`
§14.3, fila 8 original, columna "Qué mueve" nunca lo declaró; el contador
de condicionales sigue en `canon/modelo-decision-v4_0.md`). No se decidió
el desdoblamiento de `G1a`. No se rederivó ninguna otra fila de `§14.3`.

---

## 17 · Adenda 04/ago/2026 — `§14.4` se divide: `sens_estatus` no es límite verificado, es no examinado

**Disciplina aplicada:** adenda fechada, append-only. `§14.4` no se edita —
las dos filas quedan íntegras, con esta marca de que agrupaban dos estados
distintos bajo el mismo título ("límite vigente").

**Qué pasó.** `§14.4` pone `sens_estatus` y `aversion_riesgo` en la misma
fila de tratamiento porque ambos terminan en el mismo veredicto —
**NO DETERMINABLE EN ESTE RÉGIMEN** — citado de P2 (`forense/notas/2026-08-01-p2-momentos-atributos.md`
§2.c, §2.d). Leídos los dos veredictos completos, el fundamento no es el
mismo:

- **`aversion_riesgo`** tiene un candidato **examinado y descartado con
  argumento**: ENIF `P5_23`/`P5_24` mide conocimiento de protección de
  depósitos IPAB, que P2 identifica como *"el moderador que la regla
  `dinero.ahorro.seguro_deposito_atenua_aversion` pone en el `SI`, no una
  medida de aversión"*. Alguien fue a ver el reactivo y lo descartó.
- **`sens_estatus`** no tiene ningún candidato examinado. El veredicto de
  P2 dice, literalmente, que el inventario *"solo trae filas sí/parcial,
  así que no se puede distinguir 'no reportado' de 'no existe'"* — es una
  limitación del instrumento de catalogación, no un hallazgo sobre las
  fuentes. Nadie ha ido a la fuente. El desenlace sí existe (ENIGH
  `gastotarjetas`) y las celdas también (P2 §2.d: "4 ejes estrictos").

**Consecuencia.** `§14.4` deja de ser una sola clase. Dentro de "lo que no
entra en la cola":

- **`aversion_riesgo` = límite verificado.** Levantar el límite exige
  graduar los dominios §3.1/§3.9 del inventario (`§14.4` ya lo dice) — acto
  de inventario, no de fuente.
- **`sens_estatus` = no examinado.** Su examen es barato: lectura de
  descriptor de las fuentes de §3.1/§3.9 contra `sens_estatus`, del mismo
  tipo que la posición 8 de `§14.3` paso 1 (chequeo de batería, sin abrir
  microdato). Podría ser un encargo de escritorio, no una medición. Hasta
  que ese examen se corra, `sens_estatus` no debería citarse como si fuera
  el mismo tipo de límite que `aversion_riesgo` — como sí ocurrió en
  `§15` (línea *"si el parámetro cae a `NO DETERMINABLE EN ESTE RÉGIMEN`
  como `sens_estatus`/`aversion_riesgo` (`§14.4`)"*), cita que esta adenda no
  corrige por ser texto de otra sección ya cerrada, pero que queda marcada
  aquí como heredando la misma imprecisión.

Detalle en `forense/notas/2026-08-04-barrido-escritorio-pendientes.md` §6.

### 17.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `§14.4` y `§15` de este mismo archivo;
`forense/notas/2026-08-01-p2-momentos-atributos.md` §2.c, §2.d, :234, :268.
No se abrió ningún descriptor de fuente nueva — el examen que esta adenda
recomienda para `sens_estatus` no se corrió aquí, queda encargado. No se
tocó ninguno de: `milpa/procedencia.yaml`, `canon/modelo-decision-v4_0.md`,
`canon/gobernanza-v1_15.md`. No se movió ningún contador. No se reclasificó
ninguna otra fila de `§14.3` o `§14.4`.

## 18 · Adenda 04/ago/2026 — ENDIREH paso 1: fila 4 de `§14.3` sí tiene candidatos, sin adjudicar

**Disciplina aplicada:** adenda fechada, append-only, mismo mecanismo que
`§15`-`§17`. `§14.3` no se edita — la fila 4 (corregida por `§15`) queda
íntegra; esta adenda registra el resultado del paso 1 sobre ENDIREH que
`canon/modelo-decision-v4_0.md:275` nombra como uno de los dos actos de
búsqueda en curso para `exposicion_violencia` (el otro, "posición 4
rehecha sobre `TPer_Vic1`", volvió **NO ALCANZABLE** por `PR #61`, sin
examinar nada).

**Clase: Corrección de fila, misma clase que `§14` entero — Propuesta. No
es decisión. No rige sin ADR.**

**Qué pasó.** `forense/notas/2026-08-04-cal-conf-faseb-pos4-endireh-paso1.md`
bajó el descriptor de archivos de ENDIREH 2021 (`endireh2021_fd.pdf`, FD,
730 pp., registrado en `data/manifiesto.yaml` como `endireh2021_fd_pdf`,
sha256 verificado) y lo leyó contra la frase-criterio de `exposicion_violencia`.
**Encontró once candidatas en `TB_VD` ("Tabla de variables derivadas")**:
`VTOT_A`/`VTOT_12M` (agregado, cualquier tipo/ámbito), `VPSI`/`VFIS`/`VECO`/`VSEX`
× vida/12m (por tipo de violencia), `VESC`/`VLAB`/`VCOM`/`VFAM`/`VPAR` ×
vida/12m (por ámbito, con universos progresivamente más angostos que
"mujeres 15+" — estudiantes, trabajadoras, con pareja). Ninguna mide
conducta posterior (denuncia, búsqueda de ayuda) — el defecto que
inhabilitó `BP1_20`/`BP1_23`/`BP1_28` de ENVIPE (`§15`) — todas describen
"condición de violencia... a lo largo de la vida/últimos 12 meses" con
catálogo con-incidencia/sin-incidencia, la incidencia misma, no la
conducta que sigue.

**Lo que la nota deja abierto, declarado, no fabricado.** El chequeo C3
(circularidad contra Tabla B) pasa — ENDIREH no está entre las 8 fuentes
de Tabla B, ninguna candidata puede aparecer del lado del desenlace. El
chequeo C2 (mismo instrumento observa un desenlace enrutado por `G4`:
`civico.protesta.agravio_urbano`, `civico.autodefensa.agravio_rural`,
`comunicacion.inseguridad.ver_oir_callar`) **no se resolvió** — ninguna de
las 20 secciones de ENDIREH se describe, por su resumen de tabla, como
protesta/autodefensa/ver-oír-callar, pero la nota no leyó las 20 secciones
completas para descartarlo con certeza. Si C2 falla, ENDIREH mediría la
condicional `θ_k(x)` de `exposicion_violencia` sin identificar el
coeficiente `β_G4` — "compra la condicional, no el coeficiente", el mismo
patrón ya declarado para `familismo_apoyo`/`radio_confianza` (`modelo:271`).

**Consecuencia sobre la fila 4, dicha con precisión.** La fila sigue
**PENDIENTE DE VERIFICACIÓN** — este acto no midió nada y no mueve el
contador (sigue en **8/14**). Lo que cambia es que la fila deja de estar
sin ningún acto que la haya examinado con el instrumento abierto: por
primera vez desde que `PR #57` retiró el reactivo de ENVIPE, hay
candidatas verificadas por descriptor literal, con universo (mujeres
15+, más angosto por ámbito) y ejes disponibles declarados (edad,
urbanización, acceso digital a nivel hogar — confiables; ingreso a nivel
persona — parcial; formalidad laboral y migración — sin equivalente
confirmado en ENDIREH). **Cuenta como uno de los actos nombrados de la
condición de caducidad de ADR-52 A** — no la cierra, porque sí produjo
candidatos; de haber vuelto sin ninguno, habría sido el tercero y hubiera
cerrado la búsqueda.

**Qué le falta a la próxima sesión (paso 2).** Elegir entre el agregado
(`VTOT_A`/`VTOT_12M`) y el desglose por ámbito/tipo, resolver C2 (leer las
20 secciones o descartarlo por otra vía), y medir la condicional con el
mismo rigor que ya se aplicó a `radio_confianza`/`familismo_apoyo`
(ponderación, dispersión por conglomerado, estimador validado) —
`endireh2021_fd.pdf` ya está registrado con hash, no hace falta volver a
bajarlo si sigue en disco de esa sesión.

### 18.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/notas/2026-08-04-cal-conf-faseb-pos4-endireh-paso1.md`
completa; `canon/modelo-decision-v4_0.md:275` (para citar la condición de
caducidad) y `:372` (cláusula de `G4`) — no re-derivados, solo citados.
No se abrió microdato ni descriptor nuevo en este acto de adenda — la
lectura del FD la hizo la nota citada. No se tocó `canon/` ni `milpa/`.
No se movió ningún contador. No se reclasificó ninguna otra fila de
`§14.3`.

---

## 19 · Adenda 04/ago/2026 — ENVIPE paso 1: fila 4 de `§14.3` — `TPer_Vic1` NO TIENE EL DATO, argumentado

**Disciplina aplicada:** adenda fechada, append-only, mismo mecanismo que
`§15`-`§18`. `§14.3` no se edita — la fila 4 (corregida por `§15`) queda
íntegra; esta adenda registra el resultado del otro de los dos actos que
`canon/modelo-decision-v4_0.md:275` nombra para `exposicion_violencia`:
*"posición 4 rehecha sobre `TPer_Vic1`"*, que en sus dos intentos previos
(`PR #61` y su reemisión) volvió **NO ALCANZABLE**, sin examinar nada.

**Clase: Corrección de fila, misma clase que `§14` entero — Propuesta. No
es decisión. No rige sin ADR.**

**Qué pasó.** `forense/notas/2026-08-04-cal-conf-faseb-pos4-envipe-paso1.md`
verificó primero que este entorno **no** repite la firma de bloqueo de los
dos intentos previos (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin declarar,
INEGI responde `200`, `data/raw` poblado en el checkout de trabajo) y, con
eso resuelto, **sí abrió** `fd_envipe2025.pdf` y `cuest_principal_envipe2025.pdf`
(ambos ya registrados y verificados contra `data/manifiesto.yaml`) contra
la tabla `TPer_Vic1` (240 variables, Sección IV "Percepción sobre
seguridad pública" + Sección V "Desempeño institucional"). **Ninguna de
sus variables sirve**: la Sección IV completa pregunta por conocimiento o
rumor del entorno (`AP4_5`, *"¿sabe usted o ha escuchado...?"*), expectativa
subjetiva de riesgo futuro (`AP4_6`, `AP4_7`) o conducta de evitación/protección
motivada por miedo (`AP4_10`, `AP4_11`) — percepción/actitud o conducta
defensiva, nunca un hecho de violencia sufrida por la persona misma; la
Sección V completa es reconocimiento/confianza en autoridades
(`confianza_institucional`, parámetro ya aparte del modelo). Detalle
completo, tabla candidato por candidato con wording literal, universo y
catálogo, en la nota citada, §5.

**Consecuencia sobre la fila 4, dicha con precisión.** La posición **sigue
viva** — `exposicion_violencia` sigue sin medir, el contador no se mueve
(**8/14**). Lo que se cierra es solo la pregunta sobre `TPer_Vic1`
específicamente: de los "dos actos en curso" que `gobernanza:527` nombraba,
**ninguno sigue en curso hoy** — el de ENDIREH concluyó con candidato
parcial (`§18`, arriba); este concluye con NO SIRVE argumentado. Ninguno
de los dos volvió *sin examinar* como en los intentos previos de este
mismo acto.

**Nota para mesa, citada de la nota original, no decidida aquí.** La nota
señala un paralelo con el precedente que cerró `aversion_riesgo` y, por
esa vía, `sens_estatus` (ADR-52 A / ADR-54): un candidato **examinado y
descartado con argumento**, no un acto bloqueado por entorno. Si mesa
decide que ese precedente aplica, la búsqueda sobre `TPer_Vic1` cerraría
por argumento en vez de necesitar un tercer acto sin reactivo. **Esta
adenda no toma esa decisión** — la deja escrita para que mesa la tome con
el hecho ya verificado delante.

**Chequeos C2/C3, ejes de atributos.** C3 (circularidad contra Tabla B):
ENVIPE **sí** es una de las 8 fuentes de Tabla B — a diferencia de
ENDIREH, donde C3 pasaba limpio — pero no llega a materializarse porque
ninguna variable de `TPer_Vic1` se adjudica. C2 (mismo instrumento observa
un desenlace de `G4`): **declarado abierto**, misma disciplina que
`§18` — el candidato más próximo (`AP4_11_09`, "adquirir armas de fuego")
no es wording de `civico.autodefensa.agravio_rural`, pero comparte familia
conceptual con lo que `G4` produce; no se leyeron `TMod_Vic`/`TPer_Vic2`/Secciones
VI-VII para descartarlo con certeza. Ejes de atributos disponibles en
ENVIPE (citados de `forense/notas/2026-07-31-inventario-segmentacion.md`,
no re-derivados): **2 de 6 confiables** (edad, urbanización), **2
parciales** (formalidad laboral, ingreso), **2 sin equivalente** (acceso
digital, migración).

**Declaración de contaminación (ADR-46).** Esta sesión abrió el FD y el
cuestionario principal de ENVIPE 2025 — queda inhabilitada para
pre-registrar contra ENVIPE mientras retenga este contexto.

### 19.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/notas/2026-08-04-cal-conf-faseb-pos4-envipe-paso1.md`
completa; `canon/modelo-decision-v4_0.md:275` (condición de caducidad) —
no re-derivado, solo citado. No se abrió ningún PDF ni microdato en este
acto de adenda — la lectura del FD y del cuestionario la hizo la nota
citada. No se tocó `canon/` ni `milpa/`. No se movió ningún contador. No
se reclasificó ninguna otra fila de `§14.3`.

---

## 20 · Adenda 04/ago/2026 — ENDIREH paso 1-bis: microdato abierto, `VFAM` corregido, C2 cerrado

**Disciplina aplicada:** adenda fechada, append-only, mismo mecanismo que
`§15`-`§19`. `§14.3` no se edita — la fila 4 (corregida por `§15`) queda
íntegra; esta adenda registra el resultado de abrir el ZIP de microdatos
de ENDIREH (`endireh2021_bd_csv_zip`) que `§18` solo había prometido por
descriptor (FD en PDF, sin abrir el archivo).

**Clase: Corrección de fila, misma clase que `§14` entero — Propuesta. No
es decisión. No rige sin ADR.**

**Qué pasó.** `forense/notas/2026-08-04-endireh-paso1bis-verificacion-microdato.md`
re-descargó el ZIP (sha256 coincidente con el registrado — durabilidad
confirmada en sentido positivo para este payload), lo abrió, y contrastó
las once candidatas de `§18` contra el archivo real, columna por columna,
con catálogo observado y denominador cuantificado con `n`.

**Corrección puntual, no cosmética: `VFAM` no tiene par "a lo largo de la
vida".** `§18` describía el grupo "por ámbito" como `VESC/VLAB/VCOM/VFAM/
VPAR × vida/12m`, dando a entender que las cinco siguen el mismo patrón
dual de ventana temporal. El archivo trae `VFAM` como **una sola
columna** (no `VFAM_A`/`VFAM_12M`), y su descripción literal en el FD es
"Condición de violencia total en el ámbito familiar **en los últimos 12
meses**" — no existe versión de por vida para el ámbito familiar en
`TB_VD`. El descriptor prometía una forma; el archivo trae otra.

**Segunda corrección: no los cinco ámbitos angostan el universo.** `§14.3`
generaliza "los ámbitos tienen universos progresivamente más angostos
por diseño". Verificado con `n` real: **cierto para `VESC`** (n=104 212
alguna vez / 11 092 últimos 12m, condicionado a `POB_E_A`/`POB_E_12M`),
**`VLAB`** (n=88 760/55 328, condicionado a `POB_L_A`/`POB_L_12M`) y
**`VPAR`** (n=105 278, condicionado a `POBP`≠0, `T_INSTRUM`≠C2) — **falso
para `VCOM` y `VFAM`**, ambas con denominador = 110 127 = universo
completo, igual que `VTOT`/`VPSI`/`VFIS`/`VECO`/`VSEX`. Ninguna de las
19 columnas repite el defecto exacto de `BP1_20` (condicionar sobre
haber sufrido violencia, `§72` de `forense/hallazgos.md`) — las
condicionadas lo están por aplicabilidad de dominio (estudió/trabajó/
tiene pareja), no por victimización previa.

**C2 se cierra.** `§18` lo dejaba declarado abierto por no haber leído
las 20 secciones completas. Esta adenda registra que sí se leyó el
resumen de contenido de las 27 tablas completo y se corrió `grep` de
siete términos (protesta, autodefensa, policía/ronda comunitaria,
manifestación, linchamiento, insegur*) sobre el texto íntegro del FD
(51 795 líneas): cero resultados en las siete búsquedas, salvo
`denuncia` (755, todos sobre violencia sufrida por la propia mujer, no
agravio urbano/rural). **ENDIREH no observa los tres desenlaces de
`G4`**, con el límite de lectura declarado en la nota citada (no se
leyó ítem por ítem el resto de las ~23 secciones).

**C3 re-derivado**, no heredado: `grep -in endireh` contra
`forense/notas/2026-07-31-inventario-segmentacion.md` sigue en cero
resultados. Pasa.

**Ejes de atributos, corregidos con `n` real.** `§18` los daba como
"edad, urbanización, acceso digital a nivel hogar — confiables; ingreso
a nivel persona — parcial; formalidad laboral y migración — sin
equivalente". Verificado contra columnas reales: **edad** (`EDAD`,
`TSDem`, n=432 746) y **acceso digital** (`P1_4_5`/`P1_4_9`, `TVIV`,
n=122 646) confiables como los daba `§18`; **urbanización** (`DOMINIO`,
3 categorías U/C/R) **no es confiable como `§18` decía** — es un proxy
más burdo que `tam_loc` (4 categorías), reclasificado aquí a **parcial**;
**ingreso** (`TB_SEC_IV`, n=110 127, por fuente, de la mujer, no de
hogar) sigue parcial; **formalidad laboral** y **migración** siguen sin
equivalente confirmado en lo leído (`TSDem`, `TVIV`, `TB_SEC_IV`; no se
abrieron las 23 tablas restantes).

**Consecuencia sobre la fila 4, dicha con precisión.** La fila sigue
**PENDIENTE DE VERIFICACIÓN** — este acto no midió nada y no mueve el
contador (sigue en **8/14**). Lo que cambia frente a `§18` es que las
once candidatas dejan de estar verificadas solo por descriptor: están
verificadas contra el archivo, con catálogo, universo y denominador
cuantificados fila por fila, y con dos correcciones de detalle que
importan para paso 2 (`VFAM` sin par de por vida; `VCOM`/`VFAM` sin
angostar universo).

**Qué le falta a la próxima sesión (paso 2).** Elegir entre agregado
(`VTOT_A`/`VTOT_12M`) y desglose — **CP-1, sigue en mesa, este acto no la
decide**. Si se elige desglose, decidir qué hacer con la asimetría de
`VFAM` (sin ventana de por vida) antes de tratarlo como par de las otras
cuatro. Medir con ponderación (`FAC_MUJ`) y diseño muestral (`UPM_DIS`/
`EST_DIS`/`ESTRATO`), no con los conteos crudos de esta adenda.

### 20.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó: `forense/notas/2026-08-04-endireh-paso1bis-verificacion-microdato.md`
completa — la lectura del ZIP, del FD y de los headers de `TSDem`/`TVIV`/
`TB_SEC_IV` la hizo la nota citada, no este acto de adenda directamente.
No se tocó `canon/` ni `milpa/`. No se movió ningún contador. No se
reclasificó ninguna otra fila de `§14.3`. Esta sesión abrió el
instrumento de ENDIREH — inhabilitada para pre-registrar contra ENDIREH
(ADR-46).

---

## 21 · Adenda 04/ago/2026 — ENVIPE `TPer_Vic2`/`TMod_Vic`: fila 4 de `§14.3` tiene CANDIDATO VÁLIDO, sin adjudicar

**Disciplina aplicada:** adenda fechada, append-only. `§14.3` no se edita
— la fila 4 (ya corregida por `§15`, `§19`) queda íntegra; esta adenda
registra un candidato nuevo sobre la columna "Fuente · variable", que
sigue **PENDIENTE DE VERIFICACIÓN** hasta que mesa adjudique.

**Clase: registro de acto, misma clase que `§18`/`§19` — no es decisión,
no rige sin ADR.**

**Qué pasó.** La sesión que abrió `TPer_Vic2` y `TMod_Vic` de ENVIPE 2025
(`forense/notas/2026-08-04-envipe-tper-vic2-tmod-vic-paso1.md`) —
insumos que `§19` dejó explícitamente fuera de perímetro (su §11) —
encontró que `TPer_Vic2`, Sección VII (Victimización personal), trae seis
variables (`AP7_3_09` a `AP7_3_14`) que preguntan directamente a la
persona seleccionada si sufrió, durante 2024, un hecho específico de
violencia (amenaza, agresión física con lesión, secuestro, agresión
sexual, violación), sobre el universo completo de la tabla — persona
seleccionada 18+, `n`=91 182, sin condicionar a `RESUL_H`, cero blancos.
`TMod_Vic`, la otra tabla del acto, se recorrió completa y no sirve:
mismo defecto de denominador que `PR #57` encontró en
`BP1_20`/`BP1_23`/`BP1_28` (subpoblación de víctimas por construcción,
`RESUL_H='A'` en el 100% de sus filas).

**Consecuencia sobre la fila 4, dicha con precisión.** La posición
**sigue viva y no se adjudica aquí** — el acto que la abrió tiene
prohibido medir y decidir CP-1 (protocolo §4.1). El contador no se movió
(sigue en **8/14**, sin cambio). Lo que cambia es que la fila 4 deja de
tener solo NO SIRVE argumentado (`TPer_Vic1`, `§19`) — ahora tiene además
un CANDIDATO VÁLIDO nombrado, con universo, denominador, `n` y C3
resueltos, y C2 declarado abierto y acotado con un riesgo estructural
concreto (`BP1_23`, candidato de `comunicacion.inseguridad.ver_oir_callar`
en `§15`, depende por diseño del instrumento de la misma subpoblación
que dispara `AP7_3_XX`=1 — no son independientes si ambas se adjudican
del mismo ENVIPE 2025).

**Fila 4, `§14.3`, nota sobre su estado (no se reescribe la fila):**

| # | Qué se mide | Fuente · variable (citada) | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **4** | `exposicion_violencia` | **PENDIENTE DE VERIFICACIÓN** — `TPer_Vic1` (ENVIPE) descartada con argumento (`§19`); `TMod_Vic` (ENVIPE) descartada con argumento (defecto de denominador, este acto); **`TPer_Vic2` (ENVIPE), `AP7_3_09`-`_14`, CANDIDATO VÁLIDO sin adjudicar** (este acto); ENDIREH tiene candidato parcial más estrecho (universo mujeres 15+, `PR #67`) | Contador sin cambio, sigue **8/14**. Sigue siendo la C1 del coeficiente `G4 · exposicion_violencia`, `IDENTIFICADO·TRUNCADO` en P2 (`§2.d`) | Sin determinar | Sin determinar — adjudicación es de mesa |

**Efecto sobre `comunicacion.inseguridad.ver_oir_callar`, señalado sin
resolver (extiende `§15`).** Si mesa adjudica `AP7_3_09`-`_14` como
reactivo de `exposicion_violencia` **y** `BP1_23` como reactivo de
`comunicacion.inseguridad.ver_oir_callar` en el mismo acto o en actos
distintos sin cruzarlos, la dependencia estructural entre ambas
variables (misma cascada de disparo del Instrumento B) queda sin
declarar en el momento de medir. Señalado para que la sesión de medición
lo resuelva explícitamente — no se resuelve aquí.

**Nota de serie, para mesa, sin explorar aquí.** ENVIPE 2025 es la
octava ola de una serie 2018-2025 con FD y cuestionarios propios por año
(32 ids en el manifiesto). Si el candidato de este acto se adjudica, eso
abre la puerta a una serie repetida de corte transversal de ocho olas,
no un dato de un año — con el mismo problema de los 15 coeficientes de
ritmo en cero que `§11`/Encargo E ya dejaron registrado. No se
pre-registra nada contra esa posibilidad.

### 21.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó completa la nota
`2026-08-04-envipe-tper-vic2-tmod-vic-paso1.md` citada arriba; no
reabrió el FD ni el cuestionario de ENVIPE 2025 — esa lectura la hizo la
nota citada. No se tocó `canon/` ni `milpa/`. No se movió ningún
contador. No se reclasificó ninguna otra fila de `§14.3`.

## 22 · Adenda 04/ago/2026 — Encargo K: fila 4 de `§14.3` CIERRA — `exposicion_violencia` medida, contador 8→9/14

**Disciplina aplicada:** adenda fechada, append-only. `§14.3` no se edita
— la fila 4 (última nota en `§21`) queda íntegra; esta adenda registra
el cierre.

**Clase: registro de acto de MEDICIÓN — mueve el contador. Distinta de
`§18`-`§21` (registro de acto de búsqueda, no movían el contador).**

**Qué pasó.** El acto que `§21` dejó en CANDIDATO VÁLIDO sin adjudicar
(`TPer_Vic2` de ENVIPE 2025, `AP7_3_09`-`_14`) se midió en
`forense/notas/2026-08-04-medicion-exposicion-violencia-envipe.md`.
Núcleo de cinco ítems limpios (`AP7_3_10` amenaza · `AP7_3_11` agresión
física con lesión · `AP7_3_12` secuestro · `AP7_3_13` agresión sexual ·
`AP7_3_14` violación), binario "sufrió al menos uno, 2024", ponderado
por `FAC_ELE`, dispersión por conglomerado último (`EST_DIS`×`UPM_DIS`).
`AP7_3_09` (extorsión) medida aparte por su matiz patrimonial no
resuelto, reportada como condicional con/sin. Estimador contrastado
contra caso conocido (INEGI, presentación nacional ENVIPE 2025:
violación sexual, 279 por 100 mil mujeres, 2024) — reproducido con
0.09% de diferencia.

**Consecuencia sobre la fila 4, dicha con precisión.** El contador
**se mueve: 8/14 → 9/14**. `exposicion_violencia` sale de "sin reactivo
verificado — búsqueda abierta" (que queda vacía, no por agotar los tres
actos de la condición de caducidad de ADR-52 A —que sigue intacta como
criterio— sino porque el segundo acto de búsqueda encontró candidato y
este acto lo midió) y entra a `MEDIDO·PARCIAL(edad,dominio,formalidad,
ESTRATO)`. C3 limpio (re-verificado, ninguna candidata en Tabla B). C2
**sellado, no resuelto**: `BP1_23` (candidato de `comunicacion.
inseguridad.ver_oir_callar`, `§15`) depende estructuralmente de la misma
subpoblación que dispara `AP7_3_XX`=1 — declarado como límite que viaja
con el número en `milpa/procedencia.yaml`, no resuelto porque resolverlo
exigiría adjudicar `ver_oir_callar`, fuera del alcance de este acto.

**Fila 4, `§14.3`, nota sobre su estado (no se reescribe la fila):**

| # | Qué se mide | Fuente · variable (citada) | Qué mueve | Payload | Sesión-tipo |
|---|---|---|---|---|---|
| **4** | `exposicion_violencia` | **MEDIDO·PARCIAL(x)** — `TPer_Vic2` (ENVIPE 2025), `AP7_3_10`-`_14` (núcleo) + `AP7_3_09` (extorsión, condicional aparte); `TPer_Vic1`/`TMod_Vic` (ENVIPE) descartadas con argumento (`§19`/`§21`); ENDIREH queda como complemento (CP-1), no reactivo alternativo | Contador **8/14 → 9/14**. Compra la condicional base del coeficiente `G4 · exposicion_violencia`, `IDENTIFICADO·TRUNCADO` en P2 (`§2.d`) — el coeficiente sigue `ASIGNADO` (0.70), solo la condicional queda medida | Sin extorsión: 5.675% [IC95% 5.427-5.924%]. Con extorsión: 9.668% [IC95% 9.358-9.977%]. Ejes: edad×dominio (conjunto) + formalidad/ESTRATO (marginal) | Medición — `forense/notas/2026-08-04-medicion-exposicion-violencia-envipe.md` |

**CP-1, dicho con las palabras del encargo que la cierra, sin
reabrirla aquí.** ENVIPE es el reactivo de `exposicion_violencia`
(universo poblacional, sin marca de parcialidad, encuadre de
victimización delictiva). ENDIREH queda como complemento con dos
funciones nombradas (ventana de vida, desdoble tipo×ámbito) — nunca se
suman ni promedian con ENVIPE, constructos y universos distintos. Esta
adenda no reabre CP-1: reporta que se cerró y qué se hizo con la
decisión.

**Efecto sobre `comunicacion.inseguridad.ver_oir_callar`, señalado y
sellado, no resuelto (extiende `§15`, `§21`).** La dependencia
estructural entre `AP7_3_XX` y `BP1_23` (misma cascada de disparo del
Instrumento B) queda declarada en `milpa/procedencia.yaml`
(`limite_c2`), pegada al número, para que quien adjudique cualquiera de
las dos variables la encuentre ahí.

### 22.1 · Límite de lectura declarado (ADR-46)

Esta adenda leyó completa la nota
`2026-08-04-medicion-exposicion-violencia-envipe.md` citada arriba; no
reabrió el FD ni el cuestionario de ENVIPE 2025 — esa lectura ya la
hizo `§21`/la nota de paso 1. Sí abrió microdato nuevo: el CSV de
`TPer_Vic2` (`envipe2025_csv.zip`, ya registrado en manifiesto, hash
verificado) y el CSV de `TSDem` (mismo zip) para el join de formalidad.
No se tocó ninguna otra fila de `§14.3`. Cascada ejecutada:
`milpa/procedencia.yaml` (entrada nueva), `canon/modelo-decision-v4_0.md`
(§1.1.F Paso 5, §6.1, §7 — contador y reparto), `forense/hallazgos.md`
(línea de cierre).

## 23 · Adenda 04/ago/2026 — ENCUP paso 1 (Encargo M): `deferencia` LA FUENTE NO TIENE EL DATO

> **Número reservado al abrir rama, no al escribir esta adenda** — `PR #79`
> (abierto al momento de esta sesión, ver §0.1 de la nota citada abajo) ya
> reserva `§22` para su propia adenda de `exposicion_violencia`; se
> verificó su diff (`gh pr diff 79 --name-only` /
> `grep "^+## " `) antes de numerar esta, para no repetir la colisión que
> `§21` documentó dos entradas atrás.

`deferencia` no es una fila de `§14.3` (esa cola cubre las 14 condicionales
medibles; `deferencia` y `sens_estatus` son los dos huecos totales que
`§14.3` explícitamente no lista, `§14.4`). Esta adenda no mueve ninguna
fila de la cola — documenta el resultado de examinar la candidatura de
`deferencia` sobre `ENCUP 2012`, que el manifiesto (`data/manifiesto.yaml`,
campo `usado_para` de los seis payloads de ENCUP) ya declaraba abierta
junto a la de posición 9 (`confianza_institucional[electoral]`, sin tocar
aquí).

**Resultado: LA FUENTE NO TIENE EL DATO.** Cuestionario 2012 completo (84
preguntas) recorrido contra una frase-criterio escrita antes de abrir el
PDF (deferencia = acatar decisión de autoridad jerárquica/institucional/de
edad aun sin acuerdo propio, distinta de confianza institucional,
obediencia como valor de crianza, y conformidad entre pares). Dos
candidatas por vocabulario (`P44A` "obedecer siempre las leyes aún
injustas"; `P68` "obedecer la voluntad de la mayoría") examinadas y
descartadas con argumento — ninguna nombra una jerarquía interpersonal
concreta con efecto conductual, que es lo que `R2.1`
(`trabajo.jerarquia.deferencia_iniciativa_suprimida`) necesita. `P44A` en
particular es precedente casi textual de `ENCUCI AP5_11`, ya descartado
por la misma razón en Encargo C. C2 (desenlaces de `G6`) cierra: ningún
wording de las tres reglas que invocan `G6` vive en el instrumento. C3
limpio: ENCUP no está en Tabla B. `deferencia` sigue en `PROXY CON
SUPUESTO DECLARADO (M3, Latinobarómetro `P4NOIJ`, ADR-51(f))`, sin
cambio de contador (sigue en 3 de 14 en ese estado; 8 de 14 medidas —
9 si `PR #79` fusiona antes que esta). Detalle completo, candidata por
candidata, con `n` de correspondencia cuestionario↔base, denominador,
ejes de atributos y viabilidad de H-07/H-08, en
`forense/notas/2026-08-04-encup-paso1-deferencia.md`.

### 23.1 · Límite de lectura declarado (ADR-46)

Esta sesión abrió y leyó completo `Cuestionario-Quinta_2012_ENCUP.pdf` y
los encabezados/recuentos agregados de `BaseDatos_ENCUP_2012_Final.xlsx`
— **inhabilitada para pre-registrar contra ENCUP** (cualquier constructo).
No abrió los cuatro cuestionarios de contexto (2001, 2003, 2005, 2008)
más allá de un barrido de términos de una palabra sobre el texto plano,
declarado en la nota citada §11. No tocó `canon/` ni `milpa/`. No movió
ningún contador de `§14`-`§21`. No reclasificó ninguna fila de `§14.3`
(`deferencia` nunca estuvo en esa tabla).
