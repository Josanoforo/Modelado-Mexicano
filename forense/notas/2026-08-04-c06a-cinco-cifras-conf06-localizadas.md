# ACTO C-06a — Las cinco cifras de `conf.06`, localizadas

*4 de agosto de 2026. Sesión LIMPIA: no se abrió ENCUCI ni ningún microdato. No se editó `canon/glosario-v5_6.md`, `forense/hitoD-preregistro-v2_0.md` ni `forense/cruce-catalogo-fichas-v2_0.md`. No se adjudicó `R8.3`. No se selló ADR. No se calculó ninguna proporción — toda cifra citada aquí es una relectura de un artefacto ya escrito por una sesión anterior, con archivo y línea.*

**Corrección de mesa que origina el acto.** Una sesión previa declaró que `conf.06` "se resuelve leyendo". Es falso: leer da las cinco cifras y qué dicen medir; adjudicar cuál es cuál exige calcular, y eso queda fuera de este acto por diseño (§4).

---

## 0 · Verificación de premisas antes de obedecer

- **HEAD al abrir esta sesión:** `2bc613b8860c221a848ff8cab7730e2ce0088424`, rama `claude/conf-06-cinco-cifras-sdepqt`, árbol limpio (`git status` sin cambios antes de escribir).
- **La premisa "`conf.06` sigue abierto hoy" — verificada, no asumida.** `canon/glosario-v5_6.md:320` (§11, tabla de conflictos abiertos) y `:398` (§15, deudas vivas) lo confirman vigente sin ADR. **Hallazgo colateral, declarado y no corregido aquí (fuera de perímetro):** `forense/historico/TRANSFER-maestra-7.md:154-156` — documento marcado **`DOCUMENTO MUERTO`** en su propia cabecera (línea 1, "el estado vive en `estado`") — afirma *"`conf.06` RESUELTO: eran TRES REACTIVOS distintos de la misma escala (62.1% conocidos · 32.1% vecinos · 21.8% 'la mayoría')"*. Esa resolución **nunca se propagó**: el glosario vigente, la gobernanza vigente y el modelo vigente siguen citando `conf.06` como abierto (`canon/gobernanza-v1_15.md:750`, `canon/modelo-decision-v4_0.md:542`). Este acto no reabre ni cierra esa discrepancia — la nombra porque es exactamente el patrón de "fuga de custodia" que `glosario §14` ya documenta cuatro veces, y porque §4 de este acto encuentra evidencia que **contradice** la hipótesis de los "tres reactivos" tal como quedó escrita allí.

---

## 1 · Receta de búsqueda, probada contra un caso conocido antes de confiar en ella

**Caso conocido usado para validar:** `tests/check.py` T06 (líneas 239-255) ya tiene una receta mecánica publicada y su resultado está congelado en `tests/baseline.json:24-27`: *"12 valores distintos de **confianza interpersonal** en el corpus: 12 (4x) · 15 (4x) · 16 (1x) · 20 (1x) · 22 (5x) · 28 (1x) · 33 (2x) · 34 (1x) · 5 (1x) · 50 (1x) · 66 (1x) · 70 (1x)"*.

Se reprodujo esa receta exacta (mismo patrón `confian\w+ interpersonal[^.\n]{0,90}?(\d{1,2}(?:\.\d)?)\s?%`, mismo alcance `corpus/reports/*.md` + `corpus/forense/*.md`) en un script aparte: **coincide dígito por dígito con la línea base**, con cita de archivo:línea para cada uno de los 12 valores. Validación pasada.

**Pero la receta de T06 tiene un defecto que la propia prueba expuso, no uno inventado aquí:** al ser `re.finditer` sin solape, cada aparición de la frase *"confianza interpersonal"* solo captura **el primer porcentaje que sigue**, no todos los de la misma oración. `La_arquitectura_invisible_de_la_interacción_social_en_México.md:43` dice literalmente *"la confianza interpersonal en México ha caído... del 34% en 1990 al 12% en 2012. Solo el 21.8% de los mexicanos confía en 'la mayoría de las personas' según la ENCUCI 2020"* — la receta de T06 captura **34** (el más cercano) y **nunca ve el 21.8% ni el 12%** de esa misma línea, porque la frase ancla no se repite. **La cifra que el propio glosario declara canónica (21.8%, `conf.06`) es invisible para el test que mide "cuántas cifras hay".** Además, `canon/` (donde vive la tabla de las cinco cifras, `glosario-v5_6.md:84`) **no está en el alcance de T06** (solo `corpus/reports` y `corpus/forense`).

**Conclusión de la prueba:** una receta mecánica de una sola coincidencia por línea, acotada a `corpus/`, ni sustituye ni reproduce el barrido que este acto pide (`canon/`, `corpus/`, `milpa/`, `forense/`, todas las coincidencias por línea). Se usó como **piso de validación**, no como receta final. La receta final usada en §2-§3 es una búsqueda de raíz `confi\w*` + ventana de contexto, sin límite de una coincidencia por línea, sobre los cuatro directorios, filtrada a mano línea por línea (no solo por regex) porque el ruido (cifras de pensiones, Suecia/Noruega, Colombia/Brasil/Perú, LADI, juegos económicos) es mayor que la señal — ver §3.3.

---

## 2 · Las cinco cifras canónicas (las que `conf.06` nombra)

Tabla base: `canon/glosario-v5_6.md:84` (mapa de evidencia, entrada "Confianza radial — magnitud") y `:320` (§11, tabla de conflictos). Repetida, idéntica en las cinco cifras, en `canon/gobernanza-v1_15.md:750` y `canon/modelo-decision-v4_0.md:542`. Origen documental de la tabla: `forense/lectura-cuatro-pivotes.md:34-42` (27/jul/2026).

| Valor | Archivo:línea (fuente primaria en `corpus/`) | Qué dice medir | Contexto de uso |
|---|---|---|---|
| **12%** | `corpus/reports/La_arquitectura_invisible_de_la_interacción_social_en_México.md:43` — *"la confianza interpersonal en México ha caído dramáticamente del 34% en 1990 al 12% en 2012"* | **WVS 2012** (Encuesta Mundial de Valores), ítem de confianza generalizada, tendencia desde 1990 | Sustenta que la indirección comunicativa es protección ante desconfianza generalizada |
| **21.8%** | mismo archivo:línea, misma oración — *"Solo el 21.8% de los mexicanos confía en 'la mayoría de las personas' según la ENCUCI 2020"* | **ENCUCI 2020**, reactivo **"la mayoría de las personas"** (candidato: `AP5_1_1`, ver §4) | Mismo argumento: desconfianza generalizada como driver de cautela interpersonal |
| **22%** | Tres fuentes con tres atribuciones **distintas entre sí** para el mismo número (ver §3.1): `corpus/reports/Confianza_y_Desconfianza_en_México__Anatomía_Psicológica_de_una_Sociedad_Dual.md:9` (**WVS 2018**) · `corpus/reports/Moral_Emotions_in_Mexico...md:29,84,186` (**ENAFI/Encuesta Mundial de Valores**) · `canon/glosario-v5_6.md:84` (**Latinobarómetro/LAPOP**) | Confianza generalizada / interpersonal, nacional | Ancla numérica de "baja confianza generalizada" en tres reports distintos |
| **32.1%** | Dos fuentes con **atribución de reactivo contradictoria entre sí** (ver §3.2, es el nudo real): `corpus/reports/Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md:71` (**vecinos**, candidato `AP5_1_3`) · `corpus/reports/Non-Family_Social_Capital_in_Mexico__Cooperation__Trust__and_Collective_Action_Beyond_Kinship.md:12` (**"la mayoría"**, candidato `AP5_1_1`) | **ENCUCI 2020** — pero no hay acuerdo intra-corpus sobre el reactivo | Es la mitad "misma ENCUCI 2020" del conflicto que `conf.06` nombra |
| **18%** | `corpus/reports/Non-Family_Social_Capital_in_Mexico__Cooperation__Trust__and_Collective_Action_Beyond_Kinship.md:12` — *"solo 18% de los adultos mexicanos dice que 'se puede confiar en la mayoría de las personas' — el segundo nivel más bajo de 25 países tras Turquía (14%)"* | **Pew Research 2025** (28,333 adultos, presencial, 8 ene–26 abr 2025, publicado 1 dic 2025), ítem de confianza generalizada | Ancla la "confianza radial / personalización de la confianza" como cálculo racional, no rasgo |

**Las dos que reclaman ser la misma encuesta (21.8% y 32.1%-si-es-`AP5_1_1`) difieren 10.3 puntos** — la cifra que el glosario ya usa para nombrar el conflicto (`canon/glosario-v5_6.md:320`, `:84`).

---

## 3 · Más de cinco — derivado, no heredado

El barrido ampliado (§1, cuatro directorios, sin límite de una coincidencia por línea) encuentra que **la lista de cinco del glosario es un subconjunto curado, no el universo de cifras en circulación.** Tres hallazgos concretos, cada uno con cita:

### 3.1 · El propio "22%" no es una cifra: son tres atribuciones distintas de la misma cifra

| Cita | Fuente que declara |
|---|---|
| `corpus/reports/Confianza_y_Desconfianza_en_México...md:9,47` | **WVS 2018** |
| `corpus/reports/Moral_Emotions_in_Mexico...md:29` | **ENAFI/Encuesta Mundial de Valores** |
| `corpus/reports/Moral_Emotions_in_Mexico...md:84` | **Latinobarómetro, ENAFI, LAPOP** (los tres juntos) |
| `canon/glosario-v5_6.md:84` | **Latinobarómetro/LAPOP** |

Cuatro documentos, tres combinaciones de fuente distintas, para el mismo número. Esto no es "una quinta cifra": es evidencia de que ni la cifra que el glosario sí reconoce como una de las cinco tiene procedencia estable dentro del propio corpus.

### 3.2 · Una sexta cifra explícitamente ENCUCI 2020, ausente de la lista de cinco

**62.1%** — "confía (grado 8-10) en personas que conoce personalmente" / "confianza particularizada". Aparece, con el **mismo valor y el mismo reactivo atribuido**, en cuatro lugares independientes:
- `corpus/reports/Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md:71`
- `corpus/reports/Non-Family_Social_Capital_in_Mexico...md:12` — *"pero 62.1% confía (grado 8-10) en personas que conoce personalmente"*
- `corpus/reports/Non-Family_Social_Capital_in_Mexico...md:32`
- `corpus/reports/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md:19` — *"El 62.1% confía en personas conocidas personalmente"*
- (redondeado a "~62%") `corpus/reports/El_Efecto_Ambiental_de_la_Violencia_Crónica_en_México...md:107`

Es, de las seis, **la más consistente**: mismo valor, mismo reactivo, sin contradicción entre citas. Y sin embargo **no está en la tabla de "cinco cifras en circulación" del glosario** (`glosario-v5_6.md:84,320`), pese a ser tan explícitamente ENCUCI 2020 como 21.8% y 32.1%. Esto **rompe el marco "dos dicen ser la misma ENCUCI 2020"** de la propia entrada `conf.06`: contando bien, **son tres**, no dos, las cifras que se declaran ENCUCI 2020 (21.8%, 32.1%, 62.1%).

### 3.3 · Otras cifras encontradas — reales, pero fuera del universo de `conf.06` (declarado, no descartado en silencio)

| Valor | Archivo:línea | Por qué NO entra al conflicto de `conf.06` |
|---|---|---|
| **56.5%** | `corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura...md:137` — *"la ENCOAP 2023 de INEGI (urbana) reporta que 56.5% dice tener confianza alta o moderadamente alta en la mayoría de las personas"* | **Mismo reactivo conceptual, instrumento distinto** (ENCOAP 2023, no ENCUCI 2020) y escala categórica declarada distinta (alta/mod. alta/baja/nula), no la escala 0-10 de ENCUCI. Candidato a *sexto/séptimo* dato de contraste, no una de las cinco. |
| **12-28%** | `corpus/reports/Psicología__Conducta_y_Sociedad...md:21` y `corpus/reports/Psicología_del_Trabajo_en_México...md:15` (mismo dato, un report en inglés) | **WVS Wave 7 (2018)**, citado como rango, no punto — atribuido a un WVS distinto del "12% WVS 2012" que el glosario sí tiene en su lista de cinco |
| **12% (LAC)** · **15% (LAC, Latinobarómetro 2024)** · **16% (LAC)** · **17% (LAC)** | `Confianza_y_Desconfianza...md:221` · `Sanción_Social_Horizontal...md:23,73` · `Report_26...md:161` · `Psicología__Conducta_y_Sociedad...md:205` | **Promedio regional (América Latina), no cifra de México** — universo geográfico distinto, aunque el nombre del constructo ("confianza interpersonal") sea idéntico. Cuatro fuentes, cuatro números distintos, para "el promedio de la región" |
| **26%** | `Sanción_Social_Horizontal...md:73` — *"Latinobarómetro 2024: 15% regional, 26% México"* | Es México, es 2024, **no es ENCUCI y no está en la lista de cinco** — candidata real a séptima/octava cifra si se amplía el universo de `conf.06` más allá de lo que el glosario ya declaró |
| **12% "desconocidos"**, tabla con fuente doble | `Psicología_del_Consumidor_Mexicano...md:55` — *"Confianza interpersonal 12% \| Fuerte \| WVS Wave 6 (2012), Latinobarómetro"* | Mismo valor que la cifra canónica del glosario, pero atribuido a **dos fuentes a la vez** (WVS Wave 6 2012 **y** Latinobarómetro) — otra grieta de procedencia sobre una cifra que el glosario ya trata como resuelta en su origen |

**Ruido descartado explícitamente** (encontrado por la búsqueda amplia, verificado línea por línea y excluido por no ser una afirmación de magnitud de confianza interpersonal mexicana): comparadores Colombia/Brasil/Perú (5%/7%/5%, `Confianza_y_Desconfianza...md:219`), Suecia/Noruega 60-70% (`Sanción_Social_Horizontal...md:231`), pensión universal 3,200 pesos (`La_familia_mexicana...md:109`), brecha de género Ipsos (`Confianza_y_Desconfianza...md:205`), índice LADI 2017, donaciones en juegos económicos (`integrador-psicologia-mexicano.md:58`, ~34%/~50%). Estos son los valores que inflan el conteo mecánico de T06 (5, 50, 66, 70, 28 en la línea base) sin ser candidatos reales a "magnitud de confianza interpersonal en México".

**Veredicto de este punto: sí, son más de cinco.** Contando solo cifras de México (no LAC-regional) con instrumento y reactivo declarados: al menos **ocho** cifras distintas circulan como "magnitud de confianza interpersonal en México" (12%, 21.8%, 22%, 32.1%, 18%, 62.1%, 56.5%, 26%, más el rango 12-28% de WVS Wave 7 y las cuatro variantes regionales LAC si se cuentan aparte). El glosario cura cinco; el corpus completo trae más.

---

## 4 · Mapa de compatibilidad

**Regla del acto, tomada literal de §9.2 del encargo:** dos cifras del mismo reactivo son un conflicto; dos cifras de reactivos distintos no lo son necesariamente — pueden ser las dos correctas.

### 4.1 · Conflicto real, mismo reactivo, misma encuesta, mismo año

**21.8% vs. 32.1%-si-es-`AP5_1_1`** — si el reactivo de 32.1% es en verdad "la mayoría de las personas" (la lectura de `Non-Family_Social_Capital...md:12`), entonces las dos cifras miden **exactamente el mismo ítem** de la **misma encuesta** (ENCUCI 2020) y **difieren 10.3 puntos**. Esto no es item-dependencia: es una contradicción abierta sobre el mismo reactivo, tal como el glosario ya lo nombra.

### 4.2 · Conflicto de atribución (nuevo, no estaba nombrado así en el glosario)

**¿A qué reactivo corresponde 32.1%?** Dos lecturas del corpus, mutuamente excluyentes:
- `Psicología__Conducta_y_Sociedad...md:71`: 32.1% = **vecinos** (`AP5_1_3`), en la misma oración que 62.1% = conocidos.
- `Non-Family_Social_Capital...md:12`: 32.1% = **"la mayoría"** (`AP5_1_1`), en la misma oración que 62.1% = conocidos.

Ambas citas coinciden en que 62.1% = conocidos. **No pueden coincidir las dos en que 32.1% signifique cosas distintas.** Esto es un conflicto de **atribución de reactivo**, no de magnitud — y resolverlo decide si el conflicto de §4.1 existe o no: si 32.1% es vecinos, entonces 32.1% y 21.8% son reactivos distintos y **no son necesariamente incompatibles entre sí** (aunque 21.8% seguiría sin un segundo dato de contraste para su propio reactivo).

### 4.3 · No conflicto — reactivos distintos, ambos podrían ser correctos

**62.1% (conocidos, `AP5_1_2`) vs. 21.8%/32.1% (desconocidos o vecinos)** — son referentes sociales distintos (confianza particularizada vs. generalizada/comunitaria). El propio corpus lo verbaliza así: *"la ENCUCI 2020 matiza el cuadro: solo 32.1% cree que 'se puede confiar en la mayoría', pero 62.1% confía... en personas que conoce personalmente"* (`Non-Family_Social_Capital...md:12`). Un 62.1% de confianza en conocidos y un 21-32% de confianza en desconocidos/vecinos **no se contradicen**: son la firma exacta de "confianza radial" que el glosario ya tiene tierada como concepto `Fuerte` (`forense/lectura-cuatro-pivotes.md:97`, "cinco fuentes convergen en dirección").

### 4.4 · No conflicto de magnitud, sí de instrumento — necesitan reconciliación de tendencia, no de reactivo

**12% (WVS 2012) vs. 18% (Pew 2025) vs. 22% (WVS2018/ENAFI/Latinobarómetro, atribución inestable, §3.1)** — mismo reactivo conceptual ("la mayoría de las personas"/confianza generalizada), pero **encuestas, años y metodologías distintas**. Por la regla del acto, esto **no es automáticamente un conflicto** — pueden ser tres puntos válidos de una misma serie con ruido de instrumento, o una trayectoria real (el propio corpus reporta una caída y recuperación parcial: 33%→16%→22%, `Confianza_y_Desconfianza...md:295`, y una trayectoria distinta y no reconciliada con la anterior: 34%→12%, `La_arquitectura_invisible...md:43` — **estas dos trayectorias del WVS tampoco coinciden entre sí** en el punto de partida de 1990 ni en el punto más reciente, un conflicto adicional, de serie histórica, no de corte transversal).

### 4.5 · Ninguna de las seis (cinco + 62.1%) es hoy "usable" tal como está, por razones distintas

- 21.8% y 32.1%(-si-`AP5_1_1`): conflicto directo, §4.1.
- 32.1%: conflicto de atribución sin resolver, §4.2 — no se sabe qué mide hasta resolver eso.
- 62.1%: sin conflicto de magnitud ni de atribución, pero **sin corte verificado contra la medición ya hecha** (§5) — la cifra "parece" limpia y aun así no se puede dar por buena sin repetir el ítem con el corte correcto.
- 12%, 18%, 22%: no son ENCUCI, no compiten por reactivo con las anteriores — pero **22% no tiene procedencia estable** (§3.1) y las dos series WVS del corpus no coinciden entre sí (§4.4).

---

## 5 · Qué tendría que calcularse para adjudicar cada una — especificación, sin calcular nada

**Punto de partida, no heredado a ciegas: ya existe una medición real de los tres reactivos ENCUCI**, hecha por una sesión anterior y no dirigida a resolver `conf.06` — `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` (§1.1, §3.1) midió `AP5_1_1`/`AP5_1_2`/`AP5_1_3` completos, dicotomizados **≥6/10** ("aprobatorio", ancla tomada del propio enunciado "como en la escuela"), con `n`, proporción ponderada, SE e IC95%, condicionado por formalidad×edad y marginal por dominio. **Ninguna de las celdas de esa tabla reproduce 21.8%, 32.1% ni 62.1%** — la celda más baja de `AP5_1_1` (Informal 30-44, 41.8%) y la más alta (Formal 60+, 64.8%) no rozan 21.8%; lo mismo para `AP5_1_2` (72.6%-87.4%, lejos de 62.1%) y `AP5_1_3` (49.4%-72.3%, lejos de 32.1%). **Esto no es un cálculo nuevo — es una comparación de dos tablas ya escritas.**

**Hipótesis que emerge de releer, no de calcular:** `Non-Family_Social_Capital...md:12` dice explícitamente que 62.1% es *"confía (grado 8-10)"* — un corte **≥8/10**, no el ≥6/10 que usó la medición de Fase B. Es plausible por simple monotonía (menos gente puntúa 8-10 que 6-10) que 21.8%/32.1%/62.1% vengan de recodificar los mismos tres reactivos con corte ≥8/10 en vez de ≥6/10. **Esto es una hipótesis a favor de la siguiente sesión, no una adjudicación de esta.**

Especificación de lo que el acto siguiente tendría que correr, por cifra:

| Cifra | Reactivo candidato | Corte a probar | Ponderador | Universo | Qué ya está resuelto (reusar) | Qué es nuevo |
|---|---|---|---|---|---|---|
| **21.8%** | `AP5_1_1` (mayoría de las personas) | ≥8/10 (no ≥6/10) | `FAC_SEL` — ya verificado, suma 96,427,583 ≈ Censo 2020 pob. 15+ | Completo, sin filtro estructural — ya verificado | Instrumento, join `SEC_4_5`+`SD`, ponderador, universo (`2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.1) | **Agregado nacional único** con corte ≥8/10 (la medición existente solo dio celdas condicionadas, nunca un punto nacional — es deliberado, `canon §1.1.B` Propiedad 1) |
| **32.1%** | `AP5_1_1` **o** `AP5_1_3` — a decidir por el propio resultado del cálculo, no antes | ≥8/10 | Idéntico | Idéntico | Idéntico | Mismo agregado nacional a ≥8/10 para **ambos** reactivos candidatos — el que numéricamente reproduzca 32.1% resuelve también el conflicto de atribución de §4.2 |
| **62.1%** | `AP5_1_2` (personas que conoce) | ≥8/10 (confirmar la lectura literal del report) | Idéntico | Idéntico | Idéntico | Mismo agregado nacional a ≥8/10 — es la de mayor probabilidad de reproducirse limpia, por ser la más consistente entre citas (§3.2) |
| **12%, 18%, 22%** | No aplica reactivo ENCUCI — son WVS/Pew/Latinobarómetro | No aplica | No aplica | No aplica | Nada — no son recalculables desde microdato en disco | Reconciliar exige **series temporales de instrumentos externos** (WVS 7 olas, Pew 2025, Latinobarómetro), no una re-corrida sobre ENCUCI. Ver §6 |

**Límite duro, ya escrito antes de este acto y que este acto no puede saltarse:** `milpa/procedencia.yaml:226-228,245-249` marca que `radio_confianza` (el mismo dato de `AP5_1_1/2/3`) **NO identifica** la regla `cooperacion.confianza.puente_personal` — el desenlace observado de esa regla en Tabla B **es** `AP5_1_2`, el propio reactivo: sería circular (fallo C3, `forense/notas/.../pos5-6...md` §1.0). Cualquier cálculo nuevo que reconcilie 21.8%/32.1%/62.1% **compra la condicional de `G1`, no un dato para identificar la regla detrás de `R8.3`** — ver §7.

---

## 6 · Cuáles de las cinco NO salen de ENCUCI 2020

**Tres de las cinco canónicas, no:**
- **12%** — WVS 2012 (`La_arquitectura_invisible...md:43`), con una variante WVS Wave 6 (`Psicología_del_Consumidor...md:55`) y una variante WVS Wave 7 2018 citada como rango 12-28% (`Psicología__Conducta_y_Sociedad...md:21`).
- **22%** — WVS 2018 / ENAFI-WVS / Latinobarómetro-LAPOP, atribución inestable entre tres reports (§3.1).
- **18%** — Pew Research 2025 (`Non-Family_Social_Capital...md:12`, con metodología citada: 28,333 adultos, presencial, ene-abr 2025).

**Dos de las cinco, sí dicen ser ENCUCI 2020:** 21.8% y 32.1%. Y una **sexta** cifra fuera de la lista canónica también dice serlo: **62.1%** (§3.2). Contando bien, esto rompe el marco literal de la propia entrada `conf.06` ("21.8% vs. 32.1% en la MISMA ENCUCI 2020") — el supuesto correcto no es "dos cifras compiten dentro de ENCUCI", es **"al menos tres cifras compiten dentro de ENCUCI, y ninguna trae su corte de dicotomización declarado en el report que la cita"**.

---

## 7 · Qué desbloquea exactamente en `R8.3`

Ficha completa: `forense/hitoD-preregistro-v2_0.md:236-246`. Cruce v2.0: `forense/cruce-catalogo-fichas-v2_0.md:93`. Dependencia declarada: `forense/hitoD-preregistro-v2_0.md:322` (fila `D-06`).

**Las cuatro condiciones de `R8.3` y su relación con `conf.06`, letra por letra:**

- **A** — *"<10 puntos con enforcement variado"* (el veredicto que refutaría la regla). **No depende de `conf.06` directamente** — depende del falsador real ("disposición a transar con desconocidos" en enforcement alto vs. bajo), que la propia ficha dice que **no existe hoy en el corpus** (línea 244: *"el falsador exige medición propia o una fuente nueva reconciliada"*).
- **B** — *"cualquier resultado apoyado en las cifras en conflicto — no cuenta"*. **Depende de `conf.06` en su totalidad**: mientras el conflicto siga abierto, **toda** cifra de confianza interpersonal del corpus (las cinco, la sexta, o cualquier subconjunto) activa esta condición automáticamente. Este acto no cierra `conf.06`, así que B sigue activa.
- **C** — *"exigiría reconciliar `conf.06` primero"*. **Es la condición que este acto trabaja, sin cerrarla.** §4 y §5 son la mitad de escritorio de esa reconciliación: mapa de qué conflictúa con qué (§4) y especificación exacta de qué correr para adjudicar (§5). Lo que falta para satisfacer C es correr esa especificación — acto siguiente, no éste.
- **D** — *"pre-registrado como probable mientras `conf.06` siga abierto"*. **Es el estado actual y sigue siéndolo después de este acto** — `conf.06` no se cierra aquí (§10 del encargo lo prohíbe explícitamente).

**Lo que este acto encuentra y que matiza el "desbloqueo" hacia abajo, no hacia arriba:** aun si la sesión siguiente reconcilia `conf.06` por completo (adjudica reactivo y corte para 21.8%/32.1%/62.1%), **eso no le da automáticamente un falsador a `R8.3`**. El dato ENCUCI candidato (`radio_confianza`, `AP5_1_1/2/3`) tiene marca **C3** contra la regla exacta que sostiene `R8.3` (`cooperacion.confianza.puente_personal`, `canon/modelo-decision-v4_0.md:498`): el desenlace observado de esa regla en Tabla B es `AP5_1_2`, el mismo reactivo que serviría de insumo — circular (`milpa/procedencia.yaml:226-228`, `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.0). **Reconciliar `conf.06` resuelve la condición B (deja de haber "cifras en conflicto" que invaliden cualquier resultado) y avanza la condición C (ya no hace falta descubrir qué hay que calcular, solo correrlo) — pero no resuelve la condición A por sí solo**, porque el propio corpus no tiene, hoy, un reactivo que mida "disposición a transar con desconocidos según nivel de enforcement" sin caer en la circularidad que `procedencia.yaml` ya marcó. La propia ficha de `R8.3` ya lo anticipaba con esa frase exacta de la línea 244 — este acto la confirma con la fuente C3 puntual, no la contradice.

---

## 8 · Límite de lectura declarado

**Leído completo o por grep dirigido en esta sesión:** `canon/glosario-v5_6.md` (§6 mapa de evidencia, §11, §15) · `canon/gobernanza-v1_15.md` (fila `conf.06`, §4.2(e)/(f) sobre `radio_confianza`) · `canon/modelo-decision-v4_0.md` (H-03, §1.1.F, §7 reglas de cooperación) · `canon/integrador-psicologia-mexicano.md` (grep dirigido a confianza) · `forense/lectura-cuatro-pivotes.md` (completo) · `forense/hitoD-preregistro-v2_0.md` (ficha `R8.3` completa, nota `D-06`) · `forense/cruce-catalogo-fichas-v2_0.md` (fila `R8.3`) · `forense/historico/TRANSFER-maestra-7.md` (completo, documento muerto) · `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` (completo) · `milpa/procedencia.yaml` (entrada `radio_confianza`) · `milpa/refutations.yaml` (grep dirigido) · `tests/check.py` (T06) · `tests/baseline.json` (T06) · 22 reports de `corpus/reports/` por grep dirigido con cita verificada línea por línea (lista completa: §2-§3 de esta nota).

**No se abrió:** ningún `.dbf`, `.csv`, `.pdf` de microdato o diccionario de datos; ningún archivo bajo `data/raw`; `data/raw` ni siquiera se montó en este entorno. No se ejecutó ningún script de `tests/` que abra microdato (`cal_conf_faseb_*.py`, `svystat.py`, etc.) — solo se leyeron sus **resultados ya publicados** en la nota de §5.

**No se editó:** `canon/glosario-v5_6.md`, `forense/hitoD-preregistro-v2_0.md`, `forense/cruce-catalogo-fichas-v2_0.md`, `milpa/procedencia.yaml`. No se selló ADR. No se adjudicó `R8.3`.

**Contadores movidos: 0.** Este acto es un mapa, no una corrida — no mueve el contador de condicionales medidas (`8 de 14`), ni el de fichas del Hito D, ni ningún ADR.
