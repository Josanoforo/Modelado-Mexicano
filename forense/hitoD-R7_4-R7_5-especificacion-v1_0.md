# HITO D · Falsador compartido `R7.4`/`R7.5` — especificación, congelada tras adquisición real (declarado, no ocultado)

### `hitoD-R7.4-R7.5-especificacion` · **v1.0** · 24 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_4-R7_5-especificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.4-R7.5-especificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec (COMMIT 1) del falsador **único, compartido** de `R7.4`/`R7.5`: las piezas que exige, jerarquía de fuentes, caveats mapeados a consecuencia, árbol y precedencia. |
> | **QUÉ NO ES** | No calcula la tasa que el Umbral pide. No adjudica. No mueve el contador `16 de 27` por sí sola. |
> | **VERIFICAS ASÍ** | esta spec está congelada antes de que `hitoD-R7.4-R7.5-veredicto` intente construir la tasa; §1 declara con exactitud qué se vio antes y por qué no contamina el árbol de §6. |

**Acto:** `ACTO ADQ-CORRE-R74R75`, 24/ago/2026, entorno **UBUNTU**, sobre `origin/main = b053491`.

---

## 0 · Ficha bajo prueba, verbatim (`hitoD-preregistro-v2_0.md:200-210`)

> **R7.4 · Agravio + entorno urbano → protesta `[MEDIA-FUERTE]`**
> **R7.5 · Agravio + vacío rural → autodefensa `[MEDIA-FUERTE]`**
>
> *Partidas en v2.4 (ADR-33). Comparten el antecedente —agravio + falla estatal + red previa— y difieren en el disparador ambiental. Por eso su falsador es común y cruzado, que es lo que la diagonal impedía.*
>
> **Falsador (uno solo, para las dos).** Un caso donde el entorno no prediga la forma: agravio + falla estatal + red previa en entorno urbano con espacio público que derive en autodefensa, o en entorno rural con vacío estatal que derive en protesta institucional sostenida.
> **Umbral.** Que ≥25% de los casos documentados de respuesta colectiva ante agravio crucen la predicción ambiental.
>
> **A** ≥25% de casos cruzados en un registro sistemático · **B** casos cruzados anecdóticos sin denominador · **C** exigiría un registro de respuestas colectivas codificado por entorno · **D** probable: no se conoce ese registro.

---

## 1 · Lo que este ejecutor ya vio antes de congelar, declarado y no oculto — más de lo habitual, y se dice por qué no contamina

**Este acto es de adquisición real (PARTE A), no de reconocimiento de metadato como en `hitoD-R8.1-especificacion §1`.** Descargar y registrar las 5 filas de la cola exigió abrir contenido de los tres payloads antes de que esta spec se congelara — no solo nombres de campo. Se declara completo, en vez de minimizarlo:

1. **UCDP GED v26.1** (`ucdp_ged261_csv`, ya registrado 2026-08-13 por `GDELT-UCDP-RECON`, reutilizado): conteo `country=='Mexico'` (25,714 de 417,968 filas globales), distribución de `type_of_violence` en esas filas (no-estatal=25,324 · unilateral=355 · estatal=35), la tabla de pares `side_a`/`side_b` más frecuentes (dominada por narcotráfico: Cártel de Juárez/Sinaloa, CJNG/Sinaloa, etc.), y una búsqueda de patrón (`autodefensa|comunitari|vigilant|civil defen`) sobre esos dos campos que devolvió **un solo** nombre: `Autodefensas Unidas de Michoacán`. Rango de años real: 1989-2025.
2. **Mass Mobilization Project, mmALL v16** (`adqcorre_r74r75_massmobilization_mmall_v16`): conteo `country=='Mexico'` (153 de 17,145 filas globales), rango de años real (1990-2020, no 2018 — corrige el caveat de la cola), distribución de `protesterdemand1` en esas 153 filas, muestra de valores del campo `location` (texto libre de lugar), y el mismo patrón de búsqueda sobre `protesteridentity`+`notes`+`protesterdemand1`, que devolvió **una** coincidencia tangencial.
3. **GDELT 1.0** (`adqcorre_r74r75_gdelt_masterreducedv2`): estructura de columnas de las primeras líneas del archivo real (encabezado `Date,Source,Target,CAMEOCode,NumEvents,NumArts,QuadClass,Goldstein,...`, conteo de columnas variable línea a línea), suficiente para descubrir que **no trae columna de país** — hallazgo estructural, no de contenido sustantivo.
4. **GDELT 2.0, día UTC completo 2026-08-24** (`adqcorre_r74r75_gdelt2_export_mx_20260824`): 487 filas con `ActionGeo_CountryCode=='MX'` de 97,839 totales; distribución completa de `EventRootCode` sobre esas 487; las **26** filas con código 18/19/20 inspeccionadas una por una contra su `SOURCEURL` real.
5. **Ausencia de catálogo rural/urbano**: `ls /home/pc0/mm-corpus/raw | grep -iE "rural|urban|localidad|cuaeg|marco.?geo"` → vacío. Un archivo examinado (el listado completo de la raíz), cero coincidencias.

**Por qué esto no invalida el árbol de §6, declarado y no asumido:** el Umbral (`≥25%`) y la definición del falsador (cruce ambiental) **no los fija este acto** — vienen fijados, verbatim, desde `hitoD-preregistro-v2_0.md` (v2.4, ADR-33), anteriores a esta adquisición y a cualquier inspección de estos tres payloads. Lo que este acto vio **no** le permitió elegir un umbral favorable: el umbral ya estaba escrito. Lo que sí pudo sesgar es la **credibilidad previa** de este ejecutor sobre si D era el desenlace correcto — la propia ficha ya lo pre-registraba como "probable" antes de que este acto existiera (`hitoD-preregistro:210,329`), así que la dirección de la sospecha tampoco nace aquí. **No se calculó, antes de congelar esta spec, ninguna tasa de cruce** —el número que el Umbral pide— porque, como se verá en §2, ninguna de las tres fuentes ofrece el denominador que esa tasa exige; medirla no era posible, no que se evitara por disciplina.

---

## 2 · Qué exige el falsador, desarmado en piezas verificables

| # | pieza | por qué es indispensable |
|---|---|---|
| **Q1** | **Universo de "casos documentados de respuesta colectiva ante agravio"**: un caso = agravio + falla estatal + red previa, con un desenlace de respuesta colectiva observado | sin universo no hay denominador, y el Umbral es un porcentaje |
| **Q2** | **Forma de la respuesta, categórica**: protesta institucional **vs.** autodefensa, para cada caso de Q1 | sin las dos categorías no hay "cruce" que detectar |
| **Q3** | **Entorno del caso, categórico**: urbano **vs.** rural, para cada caso de Q1 | el falsador es específicamente sobre el entorno prediciendo (o no) la forma |
| **Q4** | **Conjunción cruzada**: [urbano ∧ autodefensa] ∨ [rural ∧ protesta institucional sostenida], como fracción de Q1 | es literalmente el numerador del Umbral |

**Q1-Q4 deben construirse sobre la MISMA unidad de caso** — no basta con tener por separado "una tasa de protesta" y "una tasa de violencia": el falsador pide que **cada caso individual** de respuesta a agravio traiga su propio par (entorno, forma), para poder contar cuántos casos cruzan.

---

## 3 · Jerarquía de fuentes, declarada antes de intentar Q1-Q4

**Ninguna de las tres fuentes es primaria sobre las otras dos** para este falsador — son **complementarias por diseño de inclusión, no jerárquicas**, y esa es la primera pieza de terreno que este acto encuentra distinta de lo que el encargo supone (que hubiera una jerarquía que declarar):

- **Mass Mobilization Project** es, por criterio de inclusión del propio dataset, **exclusivamente de protesta** (`protest`, campo constante=1 en el diseño). **No puede, estructuralmente, contener ni un solo caso de la rama "autodefensa"** — no es que los omita, es que no son parte de lo que el proyecto releva. Rol: cubre como máximo la mitad del espacio de Q2, nunca la conjunción.
- **UCDP GED** es, por umbral de inclusión propio (conflicto armado con víctimas, ≥25 muertes/año/díada para el conjunto agregado), **exclusivamente de violencia organizada letal**. La rama "autodefensa" existe ahí solo en la medida en que un grupo de autodefensa entra en conflicto armado letal sostenido — un umbral mucho más alto que "hay una autodefensa comunitaria". De 25,714 filas mexicanas, **una única** cadena de eventos nombra un actor de ese tipo (`Autodefensas Unidas de Michoacán`), y esas filas describen su enfrentamiento armado con cárteles, **no** el antecedente de agravio+falla estatal+red previa que la regla exige como causa. Rol: cubre, en el mejor caso, un fragmento minúsculo y no representativo de la rama "autodefensa", y **cero** de la rama "protesta institucional" (no es su objeto).
- **GDELT** es la única fuente que, por diseño, **podría** cubrir ambas ramas a la vez (tiene `EventRootCode` 14=PROTESTA y códigos 18-20 de violencia/asalto/fuerza sobre el mismo esquema de evento). Es también la única que la cola ya marcaba como necesitando construcción completa ("debe construirse universo México, deduplicar noticias, clasificar agravio/respuesta y unir entorno rural/urbano") — no una fuente lista para usarse, sino un insumo crudo para construir Q1-Q4 desde cero.

**Ninguna fuente trae Q3 (entorno urbano/rural codificado).** Las tres dan, cuando mucho, un nombre de lugar en texto libre (`location` en MassMob, `adm_1`/`where_description` en UCDP, `ActionGeo_FullName` en GDELT) — nunca una bandera. Construir Q3 exigiría un catálogo de localidades con umbral rural/urbano, que §1.5 confirma **no existe en ningún punto de este corpus**.

---

## 4 · Caveats de la cola, mapeados a consecuencia ANTES de intentar Q1-Q4

| caveat de la cola (fila) | consecuencia declarada aquí |
|---|---|
| GDELT: "ruido, validación y costo" | **Degrada a EXISTE-NO-SATISFACE si el ruido domina el subconjunto clasificable como Q2** — se mide en §2 de `hitoD-R7.4-R7.5-veredicto`, no se asume |
| GDELT: "debe construirse universo México, deduplicar noticias, clasificar agravio/respuesta y unir entorno rural/urbano" | **Vuelve la rama GDELT inejecutable-D si la construcción no es viable dentro del alcance de un acto** (no de un programa de clasificación nuevo) — criterio de viabilidad: ¿existe ya, en este corpus, el insumo para Q2 y Q3 sin escribir un clasificador de texto libre nuevo? |
| GDELT: "sesgo de cobertura" | Solo acota — no degrada por sí solo, se declara junto al resultado |
| MassMob: "termina 2018" | **Corregido por este acto**: el archivo real (v16) llega a 2020. Acota la ventana, no degrada |
| MassMob: "granularidad, actores, geografía, cobertura y licencia exactas" | **Vuelve la rama MassMob estructuralmente incompleta para Q2** (solo protesta) — no degrada por dato faltante, degrada por diseño de inclusión, ver §3 |
| UCDP: "solo conflicto violento" | **Vuelve la rama UCDP estructuralmente incompleta para Q2** (solo la mitad "autodefensa", y solo su cola más letal) — mismo tipo de degradación que MassMob, en el sentido opuesto |
| UCDP: "cobertura MX puede ser escasa por definición de conflicto" | Acota — medido en §3 arriba: no es escasa en volumen (25,714 filas), es escasa en **pertinencia** al mecanismo de la regla (dominada por narcotráfico, no por agravio→autodefensa) |

**Ninguno de los siete caveats, mapeado antes de medir, apunta a "falta un dato que podría llegar" — los siete apuntan a "el instrumento no está diseñado para esta pregunta".** Esa distinción es la misma que `hitoD-R8.1-veredicto §4` ya usó para R8.1 y se declara aquí, antes de la corrida, para que el desenlace no se lea al revés si se confirma.

---

## 5 · Universo, escalas y unidad — fijados al sellar

- **Universo pre-registrado:** México, casos de respuesta colectiva a agravio documentados en fuente pública, sin ventana temporal fija a priori (la ficha no la fija) — la ventana real la determina cada fuente y se declara, no se recorta.
- **Unidad de análisis:** el **caso individual** de respuesta colectiva (evento o serie de eventos de la misma protesta/autodefensa), no mes-entidad ni agregado — el falsador pide contar casos, no tasas agregadas.
- **No hay "ponderador" en el sentido de diseño muestral** (`FAC_*`/estratos/UPM): las tres fuentes son catálogos de eventos por rastreo de fuente abierta (prensa/informes), no encuestas con marco muestral. La escala aplicable (`A-bis 3`) es la de **cobertura de fuente**, no la de varianza de diseño — se declara para no importar un vocabulario de encuesta que no aplica aquí.
- **Ningún número de una fuente se compara directamente contra el de otra sin declarar que miden universos de inclusión distintos** (protesta pura vs. violencia letal pura vs. evento de prensa sin filtrar) — cruzarlos sin decirlo sería la comparación entre escalas que `A-bis 3` prohíbe.

---

## 6 · Árbol de decisión y precedencia, fijados antes de la corrida

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Alguna fuente (o combinación) construye Q1+Q2+Q3 sobre la misma unidad de caso, con ≥25% de cruce verificado | **`A`** |
| **2** | Se encuentran casos cruzados anecdóticos (p. ej. el caso único de UCDP) pero sin denominador de Q1 | **`B`** |
| **3** | Ninguna fuente en disco (de las 3 adquiridas por este acto) construye Q1+Q2+Q3, y la razón es estructural (diseño de inclusión, no dato faltante) | **`D`** |
| **4** | Alguna fuente permitiría construir un registro más fino con trabajo de clasificación nuevo (NLP/geocodificación) fuera del alcance de un acto | **`D`**, con la vía nombrada para un sucesor — no es `C`: ver precedencia abajo |

**Precedencia, igual que `ADR-56`/`hitoD-R8.1-especificacion §6.3` ya fijó para casos análogos:** **`D` manda sobre `C`.** Que sea *concebible* construir Q1-Q3 con un clasificador de texto y un catálogo geográfico nuevos no archiva `C` — archiva `D`, con la vía de construcción nombrada como lo que desbloquearía la ficha, no como un inventario pendiente. Si dos filas de este árbol se satisfacen a la vez (por ejemplo, rama 3 para MassMob/UCDP y rama 4 para GDELT), **la fila que se archiva es la que corresponde al panorama conjunto de las tres fuentes**, no la más favorable de una sola — este falsador es "uno solo, para las dos" reglas, y también uno solo sobre las tres fuentes juntas.

---

## 7 · Qué significa que el falsador NO refute (Bloque B-bis)

- **`corroborada`** — no disponible: no encontrar el cruce con estas tres fuentes no corrobora que el entorno prediga la forma, porque las tres fuentes tienen un sesgo de selección que **por diseño** subrepresenta exactamente el tipo de caso que refutaría la regla (protesta rural sostenida, autodefensa urbana). Ausencia de cruce en una muestra sesgada contra encontrarlo no es evidencia a favor.
- **`acotada`** — aplicaría solo si una de las tres fuentes, por sí sola y con Q1-Q3 completos, produjera un resultado válido **para el subconjunto que esa fuente cubre** (p. ej. "dentro del universo GDELT-noticias-clasificadas, X%"). Se nombra aquí porque §6 rama 1 lo dejaría abierto si ocurriera.
- **`falsador débil`** — es el desenlace que este acto anticipa como más probable, dado §3-§4: no por falta de casos mexicanos de agravio→respuesta, sino porque **ningún instrumento de los tres adquiridos codifica conjuntamente entorno y forma sobre el mismo caso** — mismo patrón que `R8.1` (`Q3` con cobertura cero) y `R7.3` (RDD no construible), ahora una tercera vez.
- **Regla de precedencia si dos filas se satisfacen** (exigida por el encargo): ya fijada en §6 — manda la fila que describe el panorama conjunto de las tres fuentes, y `D` manda sobre `C` por el precedente de `ADR-56`.

---

## 8 · Qué NO hace esta spec

No calcula Q1-Q4. No adjudica. No toca `milpa/` ni los tiers `[MEDIA-FUERTE]` de `R7.4`/`R7.5`. No construye ningún clasificador de texto ni geocodificador nuevo — si la corrida concluye que eso es lo que faltaría, se nombra como vía para un sucesor, no se escribe aquí. No toca las otras 25 fichas del perímetro.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
