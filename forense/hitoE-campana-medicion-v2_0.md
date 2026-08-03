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
