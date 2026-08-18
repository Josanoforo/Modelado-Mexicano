# BENCHMARK · `conf.05` — consumo compensatorio · edge cases y frontera de manejo de datos · insumo para FP-28

### Corrido el 17/ago/2026 · universo declarado: lectura del corpus (glosario, cuatro reports, modelo, preregistro) + cuatro búsquedas web (GRADE inconsistencia/indirectness · falacias jingle-jangle · revisión de consumo compensatorio · la cita que sostiene el tier).
### **No** se consultaron bases de microdato. Procedencia de lo externo: tipo (c), marcos y literatura.

---

## 0 · Qué está en disputa, verbatim del corpus

**Vía consumidor — `Fuerte`.** `Psicología del Consumidor`:64 — *"Desigualdad → consumo compensatorio | **Fuerte** | Velandia-Morales 2022"*. Desenlace: **consumo de estatus** (marca, logo, mensualidades). Mecanismo: desigualdad → ansiedad de estatus → señalización.

**Vía salud — `Hipótesis razonable`.** `Health, Body, Food`:35 — *"El consumo de comida/alcohol como recompensa asequible (consumo compensatorio) explica parte de la persistencia del refresco y la botana en hogares de bajo ingreso. Hay lógica económica pero **poca medición directa**."* Desenlace: **ingesta de comida y alcohol**. Mecanismo: escasez → recompensa asequible.

**El casillero dice `No promediar`** y no dice qué sí hacer. Ésa es la ranura.

**Y el propio glosario ya atrapó una confusión adyacente en esta misma celda** (`glosario:136`): el modelo lo marca `FUERTE como correlación`, V1 lo rompió *"como driver decisivo aislado"* — y el glosario anota que **no es la misma afirmación**. El corpus ya detectó una vez que bajo esta etiqueta viven proposiciones distintas. No generalizó el hallazgo.

---

## 1 · Hallazgos del benchmark

### (a) La frontera aquí no es de tier: **es de constructo.** Y la literatura ya la trazó

La revisión de consumo compensatorio no trata el fenómeno como una cosa: enumera **estrategias distintas con mecanismos distintos**. Dos de ellas son exactamente los dos lados de `conf.05`:

- **Autocompletamiento simbólico / señalización** — <cite index="69-1">ofrece beneficios simbólicos, porque señala logros en dominios no relacionados con la discrepancia</cite>. Es la vía consumidor.
- **Escapismo y distracción vía comida de consuelo** — la misma revisión reporta que quienes recordaron una derrota de su equipo favorito consumieron más alimentos grasos para desviar la atención de la discrepancia (Cornil & Chandon, 2013), y clasifica esa estrategia como de **beneficio hedónico**, no simbólico. Es la vía salud.

**Beneficio simbólico y beneficio hedónico son dos mecanismos documentados y separados dentro del mismo paraguas.** No son dos lecturas del mismo hallazgo: son dos hallazgos.

### (b) Es una falacia jingle, y la literatura predice que ocurra **justo aquí**

<cite index="66-1">La falacia jingle es suponer que dos medidas llamadas por el mismo nombre capturan el mismo constructo.</cite> Y la revisión sistemática más reciente identifica el patrón exacto de este caso: <cite index="65-1">no es infrecuente que el mismo término se use para fenómenos psicológicos distintos entre disciplinas</cite>.

`conf.05` es literalmente eso: **investigación del consumidor y investigación en salud usando "consumo compensatorio" para dos fenómenos distintos.** El choque de tiers es el síntoma; la causa es que las dos vías no están midiendo lo mismo.

Y el costo está nombrado en la literatura: los constructos afectados por estas falacias <cite index="63-1">muestran validez reducida, porque no se distinguen claramente de otros constructos</cite>. Un motor que consuma `consumo compensatorio` como una celda hereda esa validez reducida.

### (c) La frontera de manejo de datos: GRADE ya la tiene escrita, y dice **no agregues**

Éste es el benchmark procedimental que FP-28 pedía. GRADE —el estándar de facto para graduar cuerpos de evidencia— resuelve este caso sin ambigüedad, en tres piezas:

**1. La certeza se gradúa POR DESENLACE, no por constructo.** <cite index="54-1">En el sistema GRADE, la calidad de la evidencia para cada desenlace se gradúa como ALTA, MODERADA, BAJA</cite>. Un cuerpo de evidencia con dos desenlaces produce **dos calificaciones**. Producir una sola para "consumo compensatorio" es una operación que GRADE no contempla.

**2. Cuando los desenlaces difieren, eso es *indirectness*, no inconsistencia.** <cite index="52-1">La calidad de la evidencia puede disminuir cuando existen diferencias sustanciales entre la población, la intervención o los desenlaces medidos en los estudios y aquellos bajo consideración</cite>, y <cite index="56-1">la evidencia puede ser indirecta cuando los desenlaces difieren de los de interés primario</cite>. **La distinción importa mucho:** la inconsistencia se penaliza; la indirectness se resuelve **separando la pregunta**, no promediando la respuesta.

**3. La inconsistencia solo se penaliza cuando es *inexplicada*.** <cite index="55-1">Los evaluadores pueden bajar la certeza si hay inconsistencia o heterogeneidad inexplicada</cite>. Aquí la heterogeneidad **está explicada** — dos desenlaces, dos mecanismos. Por lo tanto no hay inconsistencia que penalizar, y no hay nada que reconciliar.

> **Traducción a la ranura de FP-28:** el "conflicto de tiers" de `conf.05` **no es un conflicto**. Es la señal de que dos preguntas distintas están compartiendo una casilla. La regla externa no dice "elige un tier" ni "promedia": dice **separa el desenlace y gradúa cada uno**.

### (d) Y el tier `Fuerte` tiene un problema de procedencia, encontrado de paso

`glosario:136` marca esta celda como procedencia **`(a)+(c)`** —o sea, incluye datos primarios sobre población **en México**— y la sostiene con Velandia-Morales 2022, anotada como *"base latinoamericana"*.

Verificado: los tres autores firman desde el <cite index="82-1">Departamento de Psicología Social, Centro de Investigación Mente, Cerebro y Comportamiento (CIMCYC), Universidad de Granada, España</cite>. Es un estudio **experimental**, no de campo mexicano. Y una revisión posterior reporta que, con ese diseño, <cite index="77-1">Velandia-Morales et al. (2022) no encontraron una relación estadísticamente significativa entre desigualdad de ingresos y estatus</cite> en al menos una de sus pruebas.

**Dos consecuencias, y ninguna es cosmética:**
1. La marca `(a)` para esta celda **no se sostiene por esta cita**. Es (c) —marco importado— o a lo sumo (b). Es la falla recurrente que el Bloque A nombra: confundir evidencia regional/de laboratorio con evidencia sobre población en México.
2. Un tier `Fuerte` apoyado en un experimento con un resultado nulo declarado adentro es **`Fuerte` para el efecto experimental**, no para la magnitud poblacional mexicana.

---

## 2 · Veredicto del benchmark

**Las dos opciones que ofrece la fila —"con qué tier entra cuando dos vías discrepan" y "se parte en dos constructos"— no están en pie de igualdad. La segunda es la que la metodología externa respalda, y la primera es la que GRADE nombra como error de categoría.**

Recomendación, en el vocabulario del programa:

> **`conf.05` se parte en dos constructos con tier propio**, porque no son dos lecturas de un hallazgo sino dos hallazgos con desenlace y mecanismo distintos:
>
> - **`consumo_compensatorio.estatus`** — desigualdad/movilidad bloqueada → señalización de estatus (marca, logo, apalancamiento). Desenlace: gasto en bienes posicionales. Mecanismo: beneficio simbólico. **Tier: revisar a la baja del `Fuerte` actual** por (d) — la cita que lo sostiene es experimental y no mexicana. Propuesta: `Fuerte como correlación` **acotado a evidencia regional/experimental**, con la procedencia corregida a (c).
> - **`consumo_compensatorio.recompensa`** — escasez → comida/alcohol como recompensa asequible. Desenlace: ingesta. Mecanismo: beneficio hedónico. **Tier: `Hipótesis razonable`, sin cambio.** Su propio report ya declara *"poca medición directa"* y eso es correcto.
>
> **`No promediar` deja de ser una prohibición sin contraparte** y pasa a ser lo que siempre fue: la observación de que no había una sola cosa que promediar.

**Y la contraparte honesta, que también hay que decir.** Partir tiene precio: el motor gana un constructo y `R1.4` tiene que declarar cuál de los dos consume. Hoy `R1.4` (`hitoD-preregistro`:59-60 y `modelo`:446) dice *movilidad bloqueada + presión de estatus → consumo compensatorio/aspiracional (marca, logo, mensualidades)* — **eso ya es la rama de estatus, no la de recompensa**. La partición **no rompe `R1.4`; la hace explícita.** Es el mejor caso posible: la separación ya estaba operando de hecho en el motor y solo faltaba nombrarla.

---

## 3 · Propagación declarada

Si mesa adopta la partición, seis sitios tocan y ninguno se descubre solo:

| Sitio | Qué pasa |
|---|---|
| `glosario:136` | La celda se desdobla en dos filas; se corrige la procedencia `(a)+(c)` → `(c)`; se conserva la nota de "no es la misma afirmación", que ahora tiene explicación |
| `glosario:319` y `estado-programa:137` y `gobernanza:1601` | `conf.05` pasa de `Abierto — no promediar` a resuelto, con ADR |
| `modelo:446` (`R1.4`) | Declara que consume la rama **estatus**. Sin cambio de contenido |
| `hitoD-preregistro`:59-60 | Igual: la ficha `R1.4` ya está escrita sobre estatus |
| `integrador`:36, :113, :204 | Hoy sostienen `Fuerte` sin distinguir rama — hay que acotar a estatus |
| `integrador`:255 | Ya distingue: dice que el compensatorio como driver del refresco es `Hipótesis`. **Es el único sitio del corpus que ya tenía la partición correcta.** |
| `Health, Body, Food`:35, :75, :281 | Sin cambio de tier; gana el nombre de rama |

**Hallazgo colateral, y es el mismo patrón que salió en `conf.02`:** el `integrador`:255 ya había separado las dos ramas por su cuenta, sin ADR, mientras `integrador`:36 y :204 seguían tratándolas como una. **La meta-síntesis se contradice a sí misma en la misma celda.** Nadie lo había notado porque el casillero solo miraba el choque entre reports, no dentro del integrador.

---

## 4 · Qué cambiaría este veredicto

**Falsador de la partición:** un estudio que mida **los dos desenlaces en la misma muestra mexicana** y encuentre que cargan en un solo factor —que quien señaliza estatus sea la misma persona que usa comida como recompensa, con correlación alta y sin discriminante— justificaría una sola celda. Es la prueba estándar contra la falacia jingle: análisis factorial conjunto, no etiquetas.

**Falsador del tier de la rama estatus:** una medición mexicana representativa que ligue desigualdad con gasto en bienes posicionales por decil. **Ya está identificada en el propio programa** — `recovery-plan`:65 asigna `R1.4` a **ENIGH, 6 olas**. Es dato mexicano, propio, en disco. Si esa corrida ocurre, la rama estatus deja de depender de un experimento granadino.

**Lo que NO cambiaría nada:** más citas a Velandia-Morales, o más literatura de consumo compensatorio general. La primera es la misma fuente; la segunda ya dijo lo que tenía que decir — que son estrategias distintas.
