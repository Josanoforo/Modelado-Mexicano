# Modelo de decisión del mexicano contemporáneo
### `modelo` · **v3.4** · CANÓNICO OPERATIVO

> | | |
> |---|---|
> | **ARCHIVO** | `modelo-decision-v3.4.md` |
> | **REEMPLAZA A** | `modelo-decision-v3.3.md` — **borrar** |
> | **VERIFICAS ASÍ** | §0 llega al **cambio 36** · la regla R1.1 de §3.1 trae la marca `DOMINIO AGRÍCOLA: INEJECUTABLE` · §7 trae el **Registro congelado de IDs** (tabla de 49 filas) junto a la declaración del perímetro · §0.1 y §7 distinguen explícitamente las tres poblaciones de "prueba de falsación" (ADR-45) |
> | **NOMBRE ESTABLE** | **`modelo`** — cítalo así (*"ver `modelo §3.B`"*), **nunca por nombre de archivo**. Así las versiones suben sin dejar referencias colgando |

> **v3.4 — 30/jul/2026. Vocabulario de "prueba de falsación" fijado (D-05, ADR-45).** El motor sigue en **49 reglas**; el perímetro del Hito D sigue en **27**. Lo que cambia: (1) §0.1 separa el vocabulario de veredicto de **reglas** (Hito D: `RX.Y → A-D`, fuente única el bloque append-only de `hitoD-preregistro`) del vocabulario de **generadores** (Hito C: ✅/⚠️/⬜, fuente `hitoC-prueba-generadores`) — estaban mezclados en una sola oración; (2) §7 deja de decir "una prueba de falsación corrida" — son **2 de 27 corridas archivadas** (`R1.1` → `D`, `R3.2` → `B`); un veredicto `D` es una corrida cuenta igual que cualquier otra, la letra viaja con el conteo; (3) §7 deja de citar el ejercicio informal de `glosario §6/§10` (27/jul, seguro agrícola, veredicto B) como si fuera una regla del motor — es una tercera población, sin ID de regla y sin bloque archivado, distinta de Hito D y de Hito C.
>
> | # | Cambio | Origen |
> |---|---|---|
> | 36 | **§0.1 y §7: las tres poblaciones de "prueba de falsación" se etiquetan siempre que se citan** — Hito D (reglas, 27/49, bloque append-only), Hito C (generadores, 7, `hitoC-prueba-generadores`), ejercicio de glosario (G1a/seguro agrícola, 27/jul, informal, sin bloque archivado). Ninguna cifra de conteo de corridas se reporta sin decir de cuál habla | **D-05 / ADR-45** |

> **v3.1 — 28/jul/2026. Tres defectos de redacción corregidos, detectados al escribir el pre-registro del Hito D.** El motor sigue en **49 reglas**; lo que cambia es **qué afirman tres `PORQUE`**.
>
> | # | Cambio | Origen |
> |---|---|---|
> | 30 | **`§3.1` R1.2: el `PORQUE` deja de ser una capacidad.** Decía *"la estabilidad **permite** horizonte"* — y una capacidad **no se refuta**: si el formal estable no planea, siempre se puede decir que podía. El `ENTONCES` es conductual (afore, seguro, hipoteca): **se predecía conducta y se justificaba con capacidad** | **D-01** |
> | 31 | **`§3.4` R4.1 y `§3.9` R9.1: se acota *"adaptación racional"*.** Sin acotar explica cualquier resultado — el riesgo inverso al culturalismo, y el que este corpus tiene más cerca. Ambas quedan acotadas con **la misma prueba**: si el acceso mejora, la conducta debe moverse | **D-04** |
> | 33 | **`§3.1` R1.1 recibe marca de dominio inejecutable.** Primer veredicto del Hito D Paso 2: **`D`** en el dominio agrícola. No cambia el enunciado ni el tier — **impide reintentarlo como si estuviera abierto** | **`hitoD-R1.1`** |
> | 32 | **`§3.7` R7.1 deja de ser una predicción histórica.** Enunciaba dos elecciones concretas; **dos elecciones no falsan un mecanismo**. Se reformula contra **peso percibido del acto**, con las cifras como **instancias**, no como la regla | **D-05** |
>
> ⚠️ **Lo que NO se tocó, a propósito.** **D-02** (drivers `(b)` de diáspora bajo tier `[FUERTE]` en R4.2 y R5.2) y **D-03** (la fuerza vive en una palabra: *"SOLO"* legitima, *"destruye"* capital social, en R2.2 y R10.2) **son exactamente lo que sus falsadores van a atacar.** Corregirlos ahora sería mover el blanco después de apuntar. **D-06** no es defecto de redacción: es el conflicto de dato `conf.06`, abierto.

> **v3.3 — 29/jul/2026. Corrección de rótulo del perímetro + registro congelado de IDs.** El motor sigue en **49 reglas**; el perímetro sigue en **27**. Ninguno de los dos cambia — lo que cambia es cómo se nombran y se citan.
>
> | # | Cambio | Origen |
> |---|---|---|
> | 34 | **`§7`: corrección de RÓTULO.** El registro de decisión decía *"20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas"*, tratando a `R1.4` (`[FUERTE como correlación]`) como si fuera una segunda mitad partida. No lo es: la única regla que su propia ficha declara compuesta ("dos falsadores, uno por mitad") es `R4.3` (`[FUERTE / MEDIA]`). `R1.4` es un tier distinto, con un solo falsador que ataca la correlación, no la causa. **El perímetro no cambia: siguen siendo las mismas 27 fijadas el 28/jul/2026, antes de escribir el primer falsador** | Verificación 29/jul/2026 |
> | 35 | **`§7`: Registro congelado de IDs.** El esquema de ID vigente se derivaba de (posición, tier): las fichas numeran secuencialmente solo entre reglas de perímetro, saltando las `[MEDIA]` y `[HIPÓTESIS]`. Es inservible para un pre-registro — si una `[MEDIA-FUERTE]` se degrada tras su falsador, la regla siguiente cambiaría de ID por efecto de una falsación, no de una decisión. Los **24 IDs ya usados en fichas quedan fijos, nunca se recomputan**; `§3.3` recibe ID por primera vez, tomado de las citas que ya existen en `gobernanza` y `estado`; las **22 reglas restantes** reciben el número libre de su sección en orden posicional — de ahí que `§3.4`, `§3.7` y `§3.9` queden fuera de orden posicional: **un ID es etiqueta, no posición** | Verificación 29/jul/2026 |

**MAYOR 3.0 porque absorbe la ficha canónica, que se elimina.** *(ADR-36.)* La ficha no tenía una sola afirmación propia: era una compresión del modelo v1, que no era autocontenido. El v2 sí lo es, así que la ficha solo aportaba **superficie de desincronización** — y esa desincronización fue el mecanismo del Hito 2: *de 13 reglas que los verticales dijeron estresar, 6 no existían y 4 divergían*. No inventaron: leyeron una ficha desfasada. **Una sección no se puede desincronizar de su propio documento.**

**Este documento se pega íntegro** al inicio de cualquier corrida vertical, junto con el preámbulo forense. Es el texto canónico: cruza tus hallazgos contra él, no contra tu memoria.

---

### 0.1 Cómo leer este documento — no lo saltes

**Toda afirmación de este documento viene con dos marcas. Si lo citas, cita las marcas.**

**Procedencia de la evidencia:**
- **(a)** dato primario sobre población **EN México**
- **(b)** muestra **mexicano-americana / de diáspora** — sujeta a aculturación y selección migratoria; **no es evidencia directa sobre México**
- **(c)** marco teórico importado

*Histórico: esta marca vivía solo aquí y se perdía al comprimirse en la ficha derivada — y como la ficha era lo que se pegaba en los prompts, cada corrida heredaba constructos de diáspora sin saberlo. **La ficha se eliminó en v3.0 precisamente por eso.***

**Estado de falsación de los GENERADORES** (§2.1, siete constructos — no reglas): ✅ probado · ⚠️ contradicho o contestado · ⬜ sin falsar.

**Estado de falsación de las REGLAS del motor (49 total; perímetro pre-registrado del Hito D = 27, subconjunto de las 49):** vocabulario `RX.Y → veredicto A-D`, fuente única el bloque append-only de `hitoD-preregistro §Registro de veredictos archivados`. **2 de 27 corridas archivadas** — `R1.1` → veredicto `D`, `R3.2` → veredicto `B` (§7). Un veredicto `D` es una corrida igual que cualquier otra: cuenta en el conteo, no se descarta por ser inejecutable.

---

### 0.2 Alcance y frontera — leer primero

- **Dentro:** el **mexicano moderno** —el que decide dentro del mercado, la economía monetaria, la ciudad (o el pueblo conectado a ella) y el Estado nacional—. Incluye la **huella indígena difusa** (sincretismo, folk-psicología, compadrazgo), que vive dentro de los perfiles modernos.
- **Fuera por diseño (otro modelo, no un hueco):** el **sistema indígena-comunal vivo** —asamblea como autoridad, cargos rotativos, tierra comunal, tequio obligado, usos y costumbres—. Es otro orden institucional; meterlo en esta rejilla es error categorial *(ADR-10)*.
- **Sesgo declarado:** el corpus sobre-muestrea al **clasemediero urbano formal** y sub-muestrea al **popular informal**, que es el peso demográfico dominante *(ADR-13)*.
- **Firewall genético:** prohibida la inferencia ascendencia → conducta de grupo. Se admite un canal individual estrecho (ADH1B/alcohol, CYP2A6/nicotina), pequeño frente a la estructura, que modifica una *consecuencia*, no una *decisión* *(ADR-19)*.

---

---

## 0 · Registro de cambios

| # | Cambio | ADR | Tipo |
|---|---|---|---|
| 1 | `confianza_institucional` pasa de escalar a **vector por tipo de institución** | 28.b | Esquema |
| 2 | `params_base` pasa de valor puntual a **distribución** | 28.d | Esquema |
| 3 | Bases por perfil solo con **mecanismo estructural nombrado** + test de dominancia de celda | 28.c | Esquema |
| 4 | **`procedencia` obligatoria** en los **144** números *(eran 107 en el v1)* | 28.a | Esquema |
| 5 | `familismo` se desdobla en **`familismo_apoyo`** y **`familismo_obligacion`** | 30 | Esquema |
| 6 | Los **42 disparadores de dominio** entran como booleanos, junto a los 7 globales | 26 | Motor |
| 7 | **G1 se desdobla**: adopción por canal personal vs. difusión radial | 20 *(nunca llegó al motor)* | Generadores |
| 8 | Las **seis cláusulas falsables se reescriben** al nivel donde el generador opera | Hito C | Generadores |
| 9 | **Prohibición de parámetro de bienestar agregado nacional** | 27 | Salidas |
| 10 | `§3.7` transferencia directa: **HIPÓTESIS → FUERTE** | Hito 2 + V2 + glosario v5 | Tier |
| 11 | `§3.3` regla de utilidad: **alcance acotado a gobierno digital**, la extensión a crédito se retira | Hito 2 | Alcance |
| 12 | `§3` disparador 7: **"ocho perfiles" → seis** | Corrección | Errata |

**Advertencia de honestidad que va en el encabezado, no en una nota al pie:** el v2 tiene **más parámetros asignados que el v1** —familia partida, 42 disparadores, distribuciones—. Eso es superficie nueva en un modelo cuyo defecto documentado es la infalsabilidad. Lo que lo hace defendible es que **cada número lleva ahora su etiqueta de procedencia (28.a) y tres de los cambios traen un test que corre solo** (28.c, 28.d, 30). Sin esos tests, esta versión empeoraría el problema en vez de arreglarlo.

---

## 1 · Los seis perfiles

No son tipos puros: una persona real combina rasgos, y **la variación dentro de un perfil suele ser mayor que la variación entre países** (Fischer & Schwartz). Por eso los parámetros son distribuciones y no puntos — ver §1.2.

### 1.1 Tabla de parámetros

**Escalas.** Horizonte temporal (corto / mixto / largo) · Radio de confianza (estrecho / medio / transnacional) · Aversión al riesgo (media / alta) · Sensibilidad a estatus (baja / media / alta) · Deferencia (alta / recalibrada / baja) · **`familismo_apoyo`** (medio / alto) · **`familismo_obligacion`** (medio / alto) · Exposición a violencia (media / alta) · **`confianza_institucional`: vector, ver §1.3** · Acceso digital (bajo / medio / alto / muy alto).

| Perfil | Horizonte | Radio conf. | Aversión | Estatus | Deferencia | `fam_apoyo` | `fam_oblig` | Violencia | Acceso | Tier |
|---|---|---|---|---|---|---|---|---|---|---|
| **1. Clasemediero urbano formal** | mixto→largo | medio | media | **alta** | recalibrada | medio-alto | medio | media | alto | **el mejor evidenciado** (y fuente del sesgo) |
| **2. Popular informal** (urbano y rural mestizo) | **corto** | estrecho→medio | **alta** | media | alta | **alto** | **alto** | alta | bajo→medio | Media (el extremo rural, submuestreado) |
| **3. Vulnerable en ascenso** | corto→mixto | estrecho→medio | **alta** | **alta** (miedo a caer) | alta | alto | **alto** | alta | medio | Media |
| **4. Élite A/B urbana** | largo | medio (burbuja privada) | media | media-alta | recalibrada→baja | medio | medio | media (amortiguada) | **muy alto/global** | Media, delgado |
| **5. Joven Gen Z urbano conectado** | corto (inmediatez) | medio (puentes digitales) | media | alta | **recalibrada** | medio | medio | media | muy alto | Media (sesgo urbano-digital) |
| **6. Migrante / transnacional** | mixto | **transnacional** | alta | media | alta | **alto** (diversificación) | **alto** | variable | variable | Media |

**Tamaños aproximados** (con cautela; INEGI/CONEVAL): clase media *identidad* 60–77% pero *consolidada* ~25–27%; informalidad **54.8%** de la población ocupada (ENOE 1T 2026; cruza perfiles 2, 3 y 6).

⚠️ **Cambio 5 en la tabla.** Donde el v1 tenía una columna `Familismo`, el v2 tiene dos. Los perfiles 2, 3 y 6 —donde el v1 marcaba familismo **alto**— quedan **alto en ambas**: es la configuración de la cuidadora, con red y carga simultáneas. Los perfiles 1, 4 y 5 quedan **medio en obligación**, consistente con la recalibración de deferencia. Ambos parámetros son `ASIGNADO` y heredan marca **(b)**: las escalas de familismo están validadas en contextos migratorios.

### 1.2 Los parámetros son distribuciones *(ADR-28.d)*

Cada celda de la tabla de arriba especifica **una distribución, no un valor**. Dos agentes del mismo perfil en la misma celda geográfica **deben poder diferir**.

*Motivación:* con valores puntuales el modelo produce seis clases de mexicano — la forma estadística del esencialismo que este corpus combate, y la que el validador no atrapa porque revisa estructura, no dispersión.

**Check de compilación:** una configuración donde la varianza intraperfil sea cero se rechaza.

### 1.3 `confianza_institucional` es un vector *(ADR-28.b)*

**No es un escalar.** Un escalar predice que quien desconfía de la policía desconfía de la Marina, y eso es falso y está medido:

| Institución | Confianza |
|---|---|
| Marina | 89% |
| Familia | 87% |
| Escuelas públicas | 77% |
| Universidades | 76% |
| **Partidos políticos** | **23.9%** |
| Judicial, policía, legisladores | bajas |

El vector mínimo distingue: **seguridad-fuerzas armadas · educación · salud · electoral-partidos · justicia-policía · financiera**. G1 opera sobre el componente relevante al dominio, no sobre un promedio.

### 1.4 Modificadores transversales

Género, edad, región, urbanización, escolaridad, religiosidad, exposición internacional.

⚠️ **Marca de procedencia obligatoria** *(ADR-29)*: los modificadores **marianismo**, **machismo/caballerismo** y **simpatía** son constructos `Media` con procedencia **(b)** — muestras mexicano-americanas. La marca viaja con el modificador a **cualquier** dominio donde se use, no solo a §3.10. En el v1 la marca vivía en una nota al pie de comunicación y se perdía en §1, §3.4 y §3.6.

### 1.5 Bases por perfil: admisibles solo con mecanismo *(ADR-28.c)*

Un diferencial por perfil **no es automáticamente esencialista**. Un vendedor informal en vía pública está más expuesto a extorsión que un empleado formal del mismo municipio: eso es estructura, no cultura.

Lo inadmisible es la **constante por perfil sin mecanismo nombrado**. Regla:

> Una base por perfil es admisible si **(a)** el mecanismo estructural está declarado con fuente, y **(b)** se cumple la **condición de dominancia**: un agente del perfil 2 en celda de baja violencia debe terminar por debajo de un agente del perfil 1 en celda de alta violencia.

**Si el orden no se invierte, la base domina al entorno y el parámetro es un rasgo.** Se rechaza en compilación.

---

## 2 · Los generadores latentes

Siete generadores (el v1 tenía seis; G1 se desdobla por ADR-20).

### 2.1 Definición y cláusula falsable

Las cláusulas del v1 estaban escritas a nivel de **régimen nacional** —"si la confianza generalizada subiera por encima del 30%", "con un Sistema Nacional de Cuidados"—, de modo que **solo la historia podía probarlas** y ningún caso observable podía refutarlas. El Hito C lo documentó: cero de seis cláusulas especificaba una condición alcanzable.

**Regla de redacción del v2:** *si la cláusula solo puede probarla la historia, no es una cláusula falsable — es una predicción histórica.* Toda cláusula debe ser refutable **al nivel donde la afirmación se usa**.

| Gen | Qué genera | **Cláusula falsable (v2)** |
|---|---|---|
| **G1a** · Adopción por canal de confianza personal | Adopción individual mediada por puente personal | **Se refuta si** un producto llega a un segmento por canal personal y **no** sube la adopción frente a un canal impersonal comparable, a utilidad y fricción igualadas |
| **G1b** · Difusión por confianza radial | Propagación de adopción por recomendación interpersonal | **Se refuta si** hay difusión masiva **sin** canal personal en entorno de baja confianza. ⚠️ **YA CONTRADICHO** — Casos 2 (Nu: 15M clientes, sin sucursales, adopción rural = urbana) y 3 (Kueski/Aplazo). Tier baja a **HIPÓTESIS**, coeficiente a revisión |
| **G2** · Desigualdad + baja movilidad | Ansiedad de estatus, consumo compensatorio | **Se refuta si** un segmento de movilidad bloqueada **no** señaliza estatus y prioriza precio. ⚠️ **CONTESTADO en D/E** — Caso 5 (Bodega Aurrera), leído como confirmación en su momento |
| **G3** · Informalidad + volatilidad de ingreso | Horizonte corto, ahorro informal, aversión | **Se refuta si** al estabilizarse el ingreso el horizonte **no** se alarga. ✅ **PROBADO Y SOBREVIVE** — Progresa, aleatorizado (+14% consumo, +11% alimentos). *Confirma conducta intermedia, no efecto estructural: CEPAL halla impacto limitado en movilidad ocupacional* |
| **G4** · Exposición a violencia + impunidad | Conducta defensiva, retracción del espacio público | **Se refuta si** exposición alta **no** produce conducta defensiva, o si la conducta defensiva aparece sin exposición ni impunidad local. ⚠️ **SIN FALSAR** — cero casos disponibles |
| **G5** · Familia como seguro ante Estado ausente | Pooling, corresidencia, carga de cuidado | **Se refuta si** `familismo_obligacion` alto mejora simultáneamente bienestar y logro individual. **SIN FALSAR** |
| **G6** · Jerarquía + indulgencia | Deferencia, iniciativa suprimida, paternalismo | **Se refuta si** la autoridad autoritaria **no** benévola produce buen desempeño y satisfacción. ⚠️ **SIN FALSAR** — dos casos disponibles, ambos declarados no probatorios |

**Estado de falsación, declarado en el modelo y no en un anexo:** de siete generadores, **uno probado y sobrevive (G3)**, **uno contradicho (G1b)**, **uno contestado (G2)**, **cuatro sin falsar (G1a, G4, G5, G6)**.

⚠️ **G1a sin falsar (arriba) y §7 más abajo describen poblaciones distintas — ADR-45, D-05.** Esta línea habla de **Hito C** (generadores; fuente `hitoC-prueba-generadores`): los Casos 2/3 refutan G1b (difusión radial), no G1a (canal personal), así que G1a sigue sin falsar aquí. §7 cita, por separado, un **ejercicio suelto de `glosario §6/§10`** (27/jul/2026, "utilidad + fricción baja > confianza", veredicto informal B, seguro agrícola) que usa la misma evidencia Nu/Kueski/Aplazo pero es una tercera población: no tiene ID de regla, no está en el bloque append-only de `hitoD-preregistro`, y es anterior a que el Hito D existiera. Ambas líneas son ciertas a la vez porque hablan de poblaciones distintas.

### 2.2 Coeficientes

**Los quince coeficientes son `ASIGNADO`.** Ninguno es medido, y la razón es estructural, no descuido: un coeficiente es una **elasticidad**, y el corpus es transversal — da estados, no ritmos. Ninguna fuente citada publica elasticidades; **no existían para ser citadas**.

> **El signo de los generadores está bien sostenido por el corpus. La magnitud no.** Esto es lo que permitiría a un generador explicar cualquier cosa moviéndole el coeficiente, y es el riesgo que el §2.1 acota con cláusulas al nivel correcto.

| Gen | Coeficientes |
|---|---|
| G1a | `confianza_institucional[dominio] −0.60` · `radio_confianza −0.35` |
| G1b | *a revisión — el generador está contradicho* |
| G2 | `sens_estatus 0.55` · `aversion_riesgo 0.20` |
| G3 | `horizonte_temporal −0.60` · `aversion_riesgo 0.40` · **`familismo_apoyo 0.20`** |
| G4 | `exposicion_violencia 0.70` · `confianza_institucional[justicia] −0.40` · `horizonte_temporal −0.20` · `sens_estatus −0.15` |
| G5 | **`familismo_apoyo 0.50`** · **`familismo_obligacion` (signo negativo o no monotónico)** · `radio_confianza 0.15` |
| G6 | `deferencia 0.45` |

⚠️ **`familismo_apoyo` se conserva en G3** *(corrección a la propuesta original de ADR-30)*. Ahí el mecanismo es **pooling económico bajo volatilidad** — la tanda, el préstamo del primo, la corresidencia. `§3.1` enruta el ahorro informal por G3; retirarlo dejaría esa regla sin canal. No hay doble conteo: en G3 es pooling ante volatilidad, en G5 es seguro ante Estado ausente.

**Punto de calibración prioritario.** `G3 → horizonte_temporal` es la única elasticidad del modelo estimable con dato público mexicano, vía el **panel rotativo de la ENOE** (mismo hogar, cinco trimestres, cruzando formal↔informal). Sería el **primer coeficiente MEDIDO** de los 144 números. Dos rutas independientes lo señalan: la auditoría de procedencia y el único caso del registro con diseño adecuado.

---

## 3 · El motor de reglas

### 3.A Los dos niveles de disparadores *(ADR-26)*

> ⚠️ *Renumerado en v2.1. Antes era «§3.1», que colisionaba con el dominio §3.1 (Dinero). Los dominios conservan su número; las secciones meta pasan a letra.*

El motor evalúa contra la tupla **`(perfil, params, d_global, d_dominio)`**.

**Nivel 1 — siete disparadores globales**, evaluados en todos los dominios:
`formal / informal` · `quién observa` · `sanción creíble` · `puente personal` · `urgencia` · `cobertura formal` · `segmento` (**cuál de los seis perfiles** — corregido del v1, que decía "ocho").

**Nivel 2 — 42 palancas de dominio**, declaradas en la cabecera de cada `rules/<dominio>.yaml` y transcritas literalmente de la línea con que el modelo cierra cada dominio.

⚠️ **Entran como booleanos de contexto, no como parámetros continuos** *(adenda a ADR-26)*. En el modelo son estados —`hay registro / no hay registro`, `riesgo fiscal percibido sí / no`—, no magnitudes. Tratarlas como parámetros añadiría ~42 números que habría que calibrar sin dato.

**Por qué importa:** el gate de Fase 1 (ADR-25) exige que apagar `riesgo_fiscal_percibido` borre la diferencia OXXO/CoDi. Ese campo vive en `§3.3` (dominio de trámite) y **no existe** entre los siete globales. Sin el nivel 2, el go/no-go del programa se apoya en una variable que el motor nunca evaluaría.

### 3.B Las 49 reglas SI-ENTONCES

> ⚠️ *Eran 42. En v2.1 la regla de transferencia directa de §3.7 **se parte en dos** (conf.07), porque empaquetaba una afirmación `[FUERTE]` y una `[HIPÓTESIS]` bajo un solo tier. **El perímetro de reglas `[FUERTE]` no cambia: sigue siendo 20.***

*Transcritas literalmente del v1 el 27/jul/2026, no reescritas de memoria. Las cuatro ediciones aprobadas van marcadas en línea con `*(v2: …)*`.*

### 3.1 Dinero, ahorro, crédito y consumo

- **SI** el ingreso es volátil/informal (perfiles 2, 3, 6) **ENTONCES** horizonte corto, ahorro informal (tanda, "guardado en casa"), foco en emergencia — PORQUE G3 (volatilidad) + escasez — `[FUERTE]` **(a)**. 🚫 **DOMINIO AGRÍCOLA: INEJECUTABLE** *(v3.2 — veredicto `D` de `hitoD-R1.1`, 28/jul/2026)*. El falsador pre-registrado —productores de temporal con compromiso formal voluntario de horizonte largo— **no puede correrse**: el instrumento que cubre a esa población, el Seguro Agrícola Catastrófico, **no puede ser contratado por el productor** (SADER, textual; aporta ~2.5% de la prima), y los Fondos de Aseguramiento, que sí son voluntarios, viven en riego y gran extensión (62%/66% en Sonora-Sinaloa-Tamaulipas). ⚠️ **La ausencia de seguro voluntario en temporal NO cuenta como apoyo a esta regla:** está confundida con exclusión de mercado. **La regla sale igual que entró — no ganó ni perdió información.** · **id:** `dinero.ahorro.volatilidad_horizonte_corto`
- **SI** hay empleo formal e ingreso estable (perfiles 1, 4) **ENTONCES** planeación larga: afore, seguro, hipoteca — PORQUE **el ingreso estable baja el costo esperado de comprometerse a un instrumento de horizonte largo**: cae la probabilidad de incumplir y perder lo aportado — `[FUERTE]` **(a)**. *(v3.1 — **D-01**: el `PORQUE` decía *"la estabilidad **permite** horizonte"*. **Permitir es una capacidad y una capacidad no se refuta**: si el formal estable no planea, siempre se puede decir que podía. El `ENTONCES` es conductual, así que se predecía conducta y se justificaba con capacidad. El `PORQUE` nuevo nombra un **mecanismo con dirección comprobable**. ⚠️ **Si el falsador R1.2 sale `A`, la regla no se rompe entera: se parte** — sobrevive *"la estabilidad permite"* como capacidad `[FUERTE]`, y cae *"produce"*, que es la que el motor usa para enrutar perfiles 1 y 4.)* · **id:** `dinero.planeacion.formal_estable`
- **SI** se ofrece un producto financiero por un **canal de confianza personal** (recomendación, no institución fría) **ENTONCES** sube la adopción; sin puente, desconfía — PORQUE G1 — `[FUERTE]`. · **id:** `dinero.ahorro.informal_sin_puente` **+** `dinero.ahorro.con_puente_y_respaldo` ⚠️ *dos ids ya existentes en `procedencia.yaml` para una sola regla — anomalía, ver `forense/hallazgos.md`*
- **SI** hay movilidad real bloqueada + presión de estatus (perfiles 2, 3, 5) **ENTONCES** consumo compensatorio/aspiracional (marca, logo, mensualidades), aun apalancado — PORQUE G2 — `[FUERTE como correlación]`. *(v2: sin cambio de tier. V1 forense lo rompió "como driver decisivo aislado" — **afirmación distinta** de "fuerte como correlación" — y **omitió el perfil 5**. Hito 2.)* · **id:** `dinero.consumo.estatus_mediado_por_credito`
- **SI** existe seguro de depósito visible o marca confiable **ENTONCES** se atenúa la aversión (la fintech con respaldo penetra donde el banco tradicional no) — PORQUE G1 + diseño — `[MEDIA]`. · **id:** `dinero.ahorro.seguro_deposito_atenua_aversion`
- **SI** el hogar es popular/informal y el crédito es de **efectivo o tarjeta de alto CAT** **ENTONCES** paga sobreprecios notables **hasta un techo**: la mora regulada se estabiliza en **15–20%**, viable solo con **CAT de tres dígitos y castigo agresivo** — PORQUE el precio absorbe el error de predicción del scoring, no porque el scoring falle — `[MEDIA]` **(a)**, métrica **AUDITADA** (CNBV). *(v2.5 — **P-04 del barrido**. La regla *"bajo ingreso ≠ baja disposición a pagar"* vivía en el motor **sin su límite**, y un enunciado sin techo no se puede romper por arriba. Base: **ENSAFI 2023** — solo **27.3%** de los endeudados se atrasó, es decir **72.7% al corriente** pese a ingresos bajos; pago mensual máximo sostenible **declarado** de 2,777 pesos. CAT de **80–97%** en BanCoppel son pagados por el segmento. ⚠️ **Falsador ya pre-registrado por el forense V4, con umbral:** *si el IMOR de consumo del sector popular superara **~25–30% sostenido** SIN que el CAT pudiera subir más —por techo regulatorio o competencia—, el modelo «utilidad > confianza» empezaría a romperse **por el lado del cliente**.* Es el umbral mejor especificado del corpus.)* · **id:** `dinero.credito.scoring_alternativo`
- **SI** el producto de crédito combina **baja fricción de acceso** **Y** tasa usuraria (CAT >100%) **Y** reporte crediticio incompleto o invisible (BNPL) **ENTONCES** la adopción produce **daño downstream** — concentración de mora en productos no garantizados, quejas de cobranza — PORQUE la advertencia es **condicional a la estructura, no a la conducta**: la baja fricción **sola** no daña — `[MEDIA]` **(a)**. *(v2.5 — **P-05 del barrido**, con la tier que V5 le asignó literalmente: *"una ADVERTENCIA downstream, de fuerza MEDIA"*. Es MEDIA y no más porque **el costo observado se confunde** con el diseño de precio predatorio y con el choque de ingreso — no está aislado. **Se había retirado junto con la extensión a crédito del cambio 11, cuando aplicaba justo a ese lado.** ⚠️ **La lectura peligrosa es la inversa:** leerla como *"la baja fricción daña"* culpa al diseño accesible y borra las dos condiciones estructurales que la activan.)* · **id:** `dinero.credito.baja_friccion_usura_dano_downstream`
- *Disparadores que voltean:* formalización del empleo; default de inscripción automática; presencia de un puente personal; garantía/seguro explícito.

### 3.2 Trabajo y carrera

- **SI** hay jerarquía tradicional/empresa familiar (perfil 2; modificador rural/sur) **ENTONCES** deferencia hacia arriba, iniciativa suprimida, el "sí" que significa "probablemente" — PORQUE G6 + G1 — `[FUERTE]`. · **id:** `trabajo.jerarquia.deferencia_iniciativa_suprimida`
- **SI** el liderazgo es **benévolo** (provee, protege, cuida) **ENTONCES** lealtad y satisfacción altas; **SI** es autoritario no-benévolo **ENTONCES** peor desempeño — PORQUE solo el paternalismo benévolo legitima — `[MEDIA-FUERTE]`. · **id:** `trabajo.liderazgo.benevolencia_legitima`
- **SI** hay prestaciones formales (IMSS, Infonavit) **ENTONCES** pesan más que el salario nominal (la formalidad es beneficio de estatus) — PORQUE G3 (seguridad escasa) — `[MEDIA]`. · **id:** `trabajo.prestaciones.formalidad_pesa_mas_que_salario`
- **SI** el trabajador es joven urbano (perfil 5) **ENTONCES** cambia de empleo sin culpa (no es deslealtad) y exige que las decisiones se justifiquen — PORQUE recalibración de G6 — `[MEDIA]`. · **id:** `trabajo.rotacion.joven_urbano_sin_culpa`
- *Disparadores:* benevolencia percibida del jefe; formalidad del contrato; canal privado/anónimo para expresar desacuerdo.

### 3.3 Autoridad, trámite y relación con el Estado

- **SI** el trámite es presencial con funcionario discrecional y sin registro **ENTONCES** alta probabilidad de mordida — PORQUE trampa social (G1): cada quien paga porque supone que los demás pagan — `[FUERTE]` **(a)**. ⚠️ *(v2.2: **`trampa social` no tiene entrada propia en el glosario** — solo existe ahí como refutación del mito "la mordida es inherente a lo mexicano", con base en el equilibrio de Bardhan **(c)** y ENCIG 2023 **(a)**. El tier `[FUERTE]` se sostiene por el dato, no por la etiqueta. Ver `glosario §16`: **al pre-registrar su falsador, escribirlo contra el dato —¿baja la mordida al digitalizar y hacer registrable al funcionario?— no contra el nombre del mecanismo.**)* · **id:** `tramite.mordida.discrecional`
- **SI** el trámite se digitaliza / hay testigos / el funcionario es registrable **ENTONCES** la mordida baja — PORQUE se rompe la trampa — `[FUERTE]`. · **id:** `tramite.mordida.con_registro`
- **SI** una norma se percibe como inútil o extractiva y la sanción es improbable **ENTONCES** evasión ("hacerse guaje") — PORQUE cálculo ante institución de baja calidad — `[MEDIA]`. *(Distinguir evasión de subsistencia [informalidad] de evasión por cinismo de clase alta.)* · **id:** `tramite.evasion.norma_inutil_sancion_improbable`
- **SI** se ofrece un servicio de gobierno digital de forma **coercitiva y con riesgo fiscal** (tipo CoDi/SAT) **ENTONCES** se rechaza; **SI** es útil y sin amenaza (tipo SPEI) **ENTONCES** se adopta — PORQUE la confianza institucional no predice adopción; la utilidad sí — `[MEDIA-FUERTE]`. *(v2: **alcance acotado a gobierno digital**. Su extensión a crédito en §7 del v1 se retira — Hito 2: la regla migró de dominio sin autorización.)* · **id:** `tramite.gobierno_digital.coercitivo` **+** `tramite.gobierno_digital.util_sin_coercion` ⚠️ *dos ids ya existentes en `procedencia.yaml` para una sola regla — anomalía, ver `forense/hallazgos.md`*
- *Disparadores:* discrecionalidad vs. registro; utilidad vs. coerción; riesgo fiscal percibido.

### 3.4 Salud y cuerpo

- **SI** el padecimiento es leve-moderado y no hay IMSS (perfiles 2, 3) **ENTONCES** farmacia con consultorio o automedicación — PORQUE **la conducta responde a la estructura de acceso en tres dimensiones — costo, tiempo y trato — y no a una preferencia**: si las tres mejoran, la conducta debe moverse — `[FUERTE]` **(a)**. *(v3.1 — **D-04**: el `PORQUE` decía *"adaptación racional (costo/tiempo/trato)"* sin acotar, y **sin acotar explica cualquier resultado**: siempre se puede inventar un incentivo que haga óptima cualquier conducta. Es el riesgo inverso al culturalismo y el que este corpus tiene más cerca. **La acotación es la prueba:** mejora documentada de acceso → movimiento de conducta. ⚠️ **El trato es la dimensión que no mejora al abrir una clínica** — si el uso no cae, puede ser el trato, que sigue siendo adaptación racional. **Sin medir trato no se distingue refutación de re-atribución.**)* · **id:** `salud.atencion.leve_sin_imss`
- **SI** el síntoma es grave o crónico complejo **ENTONCES** busca el sistema público pese a la espera — PORQUE la complejidad excede al consultorio — `[MEDIA]`. · **id:** `salud.atencion.grave`
- **SI** es hombre trabajador sin permiso laboral (modificador machista) **ENTONCES** pospone el chequeo hasta el síntoma grave — PORQUE machismo + costo de oportunidad del tiempo — `[FUERTE]`. *(v2: driver **machismo marcado (b)** — muestra mexicano-americana. El patrón conductual tiene dato mexicano; la atribución causal no. ADR-29.)* · **id:** `salud.prevencion.hombre_sin_permiso`
- **SI** hay desabasto + gasto de bolsillo alto **ENTONCES** abandono o intermitencia del tratamiento crónico; **SI** hay familia cuidadora + medicamento surtido **ENTONCES** mayor adherencia — PORQUE estructura + G5 — `[FUERTE / MEDIA]`. · **id:** `salud.adherencia.desabasto_vs_cuidadora`
- **SI** el producto tiene sellos y hay alternativa de **precio similar** (perfil 1 con hijos) **ENTONCES** elige el de menos sellos; **SI** el hogar es de bajo ingreso sin sustituto barato **ENTONCES** compra igual — PORQUE el precio domina sobre la información — `[MEDIA]`. · **id:** `salud.consumo.sellos_precio_similar`
- *Disparadores:* gravedad; tener o no seguridad social; desabasto; precio relativo; permiso laboral; alcoholímetro/sanción (para alcohol).

### 3.5 Familia y pareja

- **SI** hay ingreso volátil / ausencia de Estado (perfiles 2, 3, 6) **ENTONCES** la familia opera como seguro (corresidencia, pooling, remesas) — PORQUE G5 — `[FUERTE]`. · **id:** `familia.seguro.volatilidad_ausencia_estado`
- **SI** se trata de cuidado (mayores, niños, enfermos) **ENTONCES** recae sobre mujeres 40+ (hijas/nueras) — PORQUE estructura + guion marianista, no "cultura del cuidado" — `[FUERTE]`. *(v2.2: driver **marianismo marcado (b)** — constructo `Media` validado en cohorte HCHS/SOL, hispana en EE.UU. **La carga de cuidado está medida en México (a); la atribución al guion, no.** Mismo defecto que el v2 corrigió en §3.4 y aquí pasó inadvertido.)* · **id:** `familia.cuidado.recae_mujeres_40mas`
- **SI** hay baja garantía institucional del matrimonio **ENTONCES** la unión libre es opción racional (no "unión fallida") — PORQUE evita costos ante baja garantía — `[MEDIA]`. · **id:** `familia.union.baja_garantia_institucional`
- **SI** el cortejo es urbano-joven-conectado (perfil 5) **ENTONCES** apps + lógica de mercado, pero los guiones de género se reconfiguran **desigual** (actitud rápida, conducta lenta) — PORQUE cohorte + exposición — `[MEDIA / HIPÓTESIS]`. · **id:** `familia.cortejo.urbano_joven_apps`
- *Disparadores:* presencia de red familiar; género; generación; formalidad del vínculo.

### 3.6 Tiempo y compromiso

- **SI** la cita es formal-laboral con checador/sanción/dinero **ENTONCES** puntual (5-10 min antes); **SI** es social-familiar sin sanción **ENTONCES** hora aproximada, "ahorita" — PORQUE el interruptor formal/informal — `[MEDIA]`. · **id:** `tiempo.puntualidad.formal_vs_social`
- **SI** es invitación social y decir "no" sería descortés **ENTONCES** dice "sí voy" aunque la asistencia sea incierta — PORQUE simpatía/quedar bien (NO confundir con mentira) — `[HIPÓTESIS]`. · **id:** `tiempo.compromiso.si_voy_incierto`
- **SI** hay recursos escasos y urgencias compitiendo **ENTONCES** pospone lo no urgente, improvisa el "bomberazo" — PORQUE **escasez de recursos y competencia de urgencias** (G3) — `[MEDIA]` **(a)**. ⚠️ **El mecanismo cognitivo NO es parte de la regla.** *(v2.4 — **P-01 del barrido forense, la fuga más seria**: el `PORQUE` decía «bandwidth tax». V5 lo declaró **marco importado (c) —Mullainathan y Shafir— y «MATIZADA y parcialmente REFUTADA como motor primario»**, porque la ENIF muestra **38.4% de aversión declarada al endeudamiento**, dato que contradice un cortoplacismo cultural. Ese veredicto estaba archivado desde la Ronda 4 y nunca bajó. **Lo que sobrevive es la conducta observada; la explicación por ancho de banda cognitivo no.** Y toca **G3, el único generador PROBADO** — con más razón su mecanismo nombrado no puede ir sin marca. Ver `glosario §16` y `barrido-propagacion-forense`.)* · **id:** `tiempo.bomberazo.recursos_escasos_urgencias`
- **SI** hay cita médica/trámite con costo por faltar **ENTONCES** cumple más si hay recordatorio y baja barrera de asistir — PORQUE incentivo + reducción de fricción — `[MEDIA]`. · **id:** `tiempo.cumplimiento.recordatorio_baja_barrera`
- *Disparadores:* formal/informal; costo por faltar; recordatorio; escasez.

### 3.7 Cívico y participación

- **SI** el votante percibe que el acto **pesa** —resultado abierto **y** consecuencia palpable— **ENTONCES** participa; **SI** lo percibe **decidido de antemano o sin consecuencia** **ENTONCES** se abstiene — PORQUE cálculo del peso del acto — `[FUERTE]` **(a)**. *Instancias observadas, **no la regla**: presidencial 2024 ≈ **59.8%**; judicial 2025 abstención **>85%**.* *(v3.1 — **D-05**: la regla enunciaba **dos elecciones concretas**, y **dos elecciones no falsan un mecanismo — son una predicción histórica**, que es justo lo que el Hito C prohibió. El driver declarado siempre fue **el peso percibido**, no el tipo de comicio; ahora la regla lo dice y las cifras bajan a instancias. **Efecto sobre el falsador:** se vuelve comprobable con **elecciones locales concurrentes vs. no concurrentes** —mismo electorado, mismo año, distinto peso percibido—, en vez de esperar a que la historia produzca otro caso.)* · **id:** `civico.participacion.contingente`
- **SI** el delito no tiene cobertura de seguro y el agresor es identificable **ENTONCES** no denuncia (cifra negra) — PORQUE miedo + inutilidad percibida (denunciar rinde 0.8%) — `[FUERTE]`; **SI** es robo de vehículo asegurado **ENTONCES** sí denuncia (por el trámite del seguro). · **id:** `civico.denuncia.sin_seguro` **+** `civico.denuncia.con_seguro` ⚠️ *dos ids ya existentes en `procedencia.yaml` para una sola regla — anomalía, ver `forense/hallazgos.md`*
- **SI** hay transferencia directa universal no condicionada **Y NO** hay proximidad/focalización del reparto **Y NO** hay monitoreo percibido del voto **ENTONCES** **conserva autonomía de la ELECCIÓN de voto**: subir el tamaño del beneficio no mueve a quién se vota — PORQUE no hay monitoreo del voto individual ni sanción creíble por cómo se vota — `[FUERTE]` **(a)**. · **id:** `civico.voto.agencia_con_secreto`
- **SI** hay **proximidad/focalización del reparto** **O** el votante **percibe que su voto puede ser monitoreado** **ENTONCES** **la autonomía CEDE localmente** — PORQUE cálculo racional bajo incertidumbre sobre el secreto del voto — `[MEDIA]` **(a)**. *(v2.4 — **P-02 del barrido**: V2 midió las dos condiciones de cesión y el motor enunciaba la autonomía sin ellas. **Cantú 2019**: efecto persuasivo real de las tarjetas Soriana bajo focalización. **Ascencio-Chang 2025**: la probabilidad de voto clientelar sube de **0.06 a 0.63** en laboratorio cuando el votante cree que su voto puede observarse. Sin estas condiciones la regla de autonomía era **infalsable por generalidad**: todo contraejemplo se descartaba como "local".)* · **id:** `civico.voto.clientelar_si_observable`
- **SI** hay dádiva o transferencia **Y** el partido puede monitorear al **broker** (no al votante) **ENTONCES** compra **ASISTENCIA a las urnas** de simpatizantes, **no la elección de voto** — PORQUE *turnout buying* ≠ *vote-choice buying* — `[MEDIA]` **(a)**. *(v2.4 — **P-03 del barrido**: el motor trataba "el voto" como objeto único. La dádiva **sí** mueve que vayas a votar y **no** mueve a quién le votas; son dos conductas distintas. Larreguy, Montiel Olea y Querubín 2017 (AJPS): la eficacia del SNTE viene del **apego partidista**, no de la dádiva. Sin esta distinción, un falsador contra "no mueve el voto" sale ambiguo: es verdadero para la elección y falso para la asistencia.)* ⚠️ *(v2.3: se retira «ni broker» del `PORQUE`. El forense V2 lo declaró **ROTO PARCIALMENTE**: Langston 2025 documenta a los **Servidores de la Nación** como capa de intermediación centralizada — **sí hay broker**, de afiliación y propaganda, aunque **no de monitoreo del voto individual**. La rotura estaba escrita en el forense desde la Ronda 4 y nunca bajó al motor: séptimo caso de propagación fallida, ADR-29.a.)* *(v2: sube de HIPÓTESIS a FUERTE — V2 forense con RCTs y contrafactual 2018, glosario v5 e Hito 2 coincidían; solo el motor decía Hipótesis.)* · **id:** `civico.clientelismo.turnout_no_vote_choice`
- **SI** hay transferencia directa universal no condicionada **ENTONCES** **se vive como derecho** — entitlement despersonalizado: el apoyo *corresponde*, y quien firma el decreto es reemplazable — PORQUE el beneficio llega sin intermediario ni corresponsabilidad — `[HIPÓTESIS]` **(a)**. *(v2.3: mitad A de la diagonal partida. El glosario tierea «entitlement de derecho» como **Hipótesis**. Ancla institucional, no conductual: la pensión está en el **artículo 4.º constitucional desde 2020**, así que «derecho» tiene referente jurídico — lo que **no** está medido es que el beneficiario lo viva así. **Falsador candidato:** conducta de reclamo ante retraso o falla de pago —un derecho se exige, un favor se agradece—, que es observable sin preguntar por estados mentales.)* · **id:** `civico.transferencia.entitlement_derecho`
- **SI** hay transferencia directa universal no condicionada **ENTONCES** **la atribución va al líder y se expresa como aprobación**, no como voto comprado — PORQUE premio retrospectivo al desempeño e identidad partidista — `[MEDIA]` **(a)**, **correlacional**. ⚠️ **CONFUNDIDO.** *(v2.3: mitad B. Tier **leído del forense V2**, que asigna literalmente «Tier: MEDIA (correlacional para la 4T)» — el motor la traía dentro de un `[FUERTE]`. ENEM 2024, N=2,700: identificación morenista y aprobación de AMLO son **predictores dominantes**; ser beneficiario es **factor secundario**. **Aislabilidad: CONFUNDIDO** con aprobación presidencial (73%), identidad partidista, maquinaria territorial, voto retrospectivo por salario mínimo y debilidad opositora. ⚠️ **La «gratitud» puede no ser psicológica**: puede ser **voto retrospectivo racional** —recompensar ingreso real recibido—, no lealtad afectiva. **Falsador ya pre-registrado por el propio forense:** un **RDD sobre la Pensión del Bienestar que muestre efecto electoral independiente de la aprobación presidencial**.)* *(v2.1: **partida de la anterior** por conf.07. Las dos mitades tenían tier distinto y viajaban bajo un solo `[FUERTE]`. La identificación causal del forense V2 sostiene la autonomía del voto, **no** el mecanismo subjetivo de "derecho". El glosario v5 ya tenía "entitlement de derecho" como **Hipótesis** y el motor lo empaquetaba como Fuerte: es el mismo defecto de la regla estrella, una capa más abajo.)* · **id:** `civico.transferencia.atribucion_lider`
- **SI** hay agravio personal/familiar + falla estatal palpable + red previa **Y** el entorno es **urbano con espacio público disponible** **ENTONCES** se suma a **protesta** (8M: mujeres jóvenes urbanas; colectivos de búsqueda: familiares) — PORQUE G4 (destructor selectivo) — `[MEDIA-FUERTE]` **(a)**. · **id:** `civico.protesta.agravio_urbano`
- **SI** hay agravio personal/familiar + falla estatal palpable + red previa **Y** el entorno es **rural con vacío estatal y sin monopolio creíble de la fuerza** **ENTONCES** se suma a **autodefensa** — PORQUE G4 + ausencia de proveedor de seguridad — `[MEDIA-FUERTE]` **(a)**. *(v2.4: **segunda diagonal partida** — ADR-33. Protestar y armarse son conductas distintas, de segmentos opuestos y con condiciones ambientales distintas; unidas por una `o`, cualquier respuesta colectiva confirmaba la regla y ninguna podía refutarla. **El disparador que las separa no es el agravio —que comparten— sino la disponibilidad de espacio público frente al vacío de seguridad.**)* · **id:** `civico.autodefensa.agravio_rural`
- *Disparadores:* relevancia percibida del acto; cobertura de seguro; agravio directo; red comunitaria; monitoreo del voto.

### 3.8 Cooperación y bienes públicos (fuera del parentesco)

- **SI** hay comité con liderazgo confiable + monitoreo + sanción visible **ENTONCES** contribuye; **SI** no hay monitoreo ni sanción **ENTONCES** free-riding racional — PORQUE adaptación + institución — `[FUERTE]`. · **id:** `cooperacion.comite.monitoreo_sancion_visible`
- **SI** conoce personalmente a la organizadora/miembros **ENTONCES** entra a la tanda; **SI** es tanda de desconocidos **ENTONCES** alto riesgo de fraude, evita — PORQUE confianza personalizada como sustituto de enforcement — `[FUERTE]`. · **id:** `cooperacion.tanda.conoce_organizadora`
- **SI** hay un puente personal (conocido en común, correligionario, paisano) **ENTONCES** confía en el desconocido; **SI** no hay puente **ENTONCES** desconfía por defecto — PORQUE G1 (la desconfianza es cálculo, no rasgo) — `[FUERTE]`. · **id:** `cooperacion.confianza.puente_personal`
- **SI** es pueblo mestizo con faena/cooperación normada y sanción (multa, exclusión, presión vecinal) **ENTONCES** participa (coerción normativa); **SI** es urbano sin sanción **ENTONCES** participación voluntaria baja — PORQUE sanción social horizontal — `[MEDIA]`. · **id:** `cooperacion.faena.sancion_social_pueblo_mestizo`
- *Disparadores:* liderazgo honesto percibido; mecanismo de sanción creíble; puente personal; obligación normada.
- *Frontera:* la **faena/tequio bajo usos y costumbres** (comunidad indígena) no es una regla de este dominio: es obligación institucional de otro orden y queda **fuera del modelo** (§1.4).

### 3.9 Información y creencia (a quién le cree)

- **SI** la información la reenvía un **allegado de confianza** **ENTONCES** sube la credibilidad inicial; **SI** el tema es de alto riesgo **ENTONCES** una fracción verifica en otro medio — PORQUE la confianza radial fija el prior, la duda dispara la verificación — `[MEDIA]`. · **id:** `informacion.credibilidad.allegado_confianza`
- **SI** el experto formal es accesible, cercano y asequible **ENTONCES** defiere; **SI** es caro, lejano o ya falló **ENTONCES** prevalece "yo sé por experiencia" y el consejo del allegado — PORQUE **la deferencia responde al costo de acceso al experto, no a una postura ante la ciencia**: si el acceso se vuelve fácil, cercano y gratuito, la consulta debe subir — `[FUERTE]` **(a)**. *(v3.1 — **D-04**, misma acotación que `§3.4`. ⚠️ **Registrar el veredicto junto al de `§3.4`:** si ambas fallan por el mismo lado —el acceso mejora y la conducta no se mueve— **no son dos refutaciones, son una**, y apuntan a que *"adaptación racional"* está haciendo de comodín en todo el motor.)* · **id:** `informacion.deferencia.costo_acceso_experto`
- **SI** la vacuna/servicio está disponible y la campaña llega **ENTONCES** la mayoría acepta — PORQUE el default es aceptación y el hueco es logístico (no actitudinal) — `[FUERTE]`. · **id:** `salud.vacunacion.disponible` ⚠️ *id ya existente en `procedencia.yaml`, con dominio equivocado (`salud.*` en un id de §3.9, no §3.4) — no se corrige, ver `forense/hallazgos.md`*
- **SI** el hogar es clase media con miedo a caer (perfil 1) **ENTONCES** escuela privada como seguro anticaída + credencial; **SI** es popular **ENTONCES** pública con aspiración universitaria alta — PORQUE G2 + cálculo de retorno — `[MEDIA]`. · **id:** `informacion.escuela.miedo_a_caer_clase_media`
- *Disparadores:* proximidad del emisor; accesibilidad/costo del experto; disponibilidad del servicio; miedo a caer.

### 3.10 Comunicación y conflicto

*(Reglas del report de comunicación, ya con la corrección de la meta-auditoría: el driver es adaptación racional + face bajo dignidad, NO "honor".)*

- **SI** hay que emitir un rechazo **ENTONCES** se hace indirecto ("vamos a ver", "déjame ver") — PORQUE preservación de face + simpatía; el "no" directo se lee como falta de respeto — `[FUERTE]` (Félix-Brasdefer, muestra en México). · **id:** `comunicacion.rechazo.indirecto_face`
- **SI** se da retroalimentación negativa **ENTONCES** debe ser privada, indirecta y enmarcada positivamente; en público destruye capital social — PORQUE G6 + face — `[MEDIA-FUERTE]`. · **id:** `comunicacion.retroalimentacion.privada_publica_capital_social`
- **SI** el contexto es de inseguridad/autoridad no confiable **ENTONCES** "ver, oír y callar" — PORQUE G4 (adaptación racional, no timidez) — `[FUERTE]`. · **id:** `comunicacion.inseguridad.ver_oir_callar`
- **SI** el interlocutor es norteño/joven-urbano **ENTONCES** mayor directividad; **SI** es sur/mayor/rural **ENTONCES** más indirección — PORQUE modificador regional/generacional — `[MEDIA]`. · **id:** `comunicacion.directividad.regional_generacional`
- *Nota de procedencia:* la evidencia de simpatía/marianismo/machismo es en buena parte de **muestras mexicano-americanas** (marcar; no dar por verificada en población en México).
- *Disparadores:* público vs. privado; posición jerárquica (asertividad fluye hacia abajo, indirección hacia arriba); región; generación; seguridad del entorno.

---

---

## 4 · Protocolo de uso

Transcripción del v1, sin cambios. Orden de aplicación: segmento → parámetros → generadores → disparadores globales → disparadores de dominio → regla → salida con tier.

---

## 5 · Límites del modelo

### 5.0 Las seis prohibiciones duras, en una lista

1. **Ningún parámetro de bienestar, felicidad o afecto agregado a nivel nacional** *(ADR-27)*. México sale #10 mundial en satisfacción vital y a la vez registra 18.1M de carga de salud mental y 135,445 desaparecidos: **eso no es contradicción, es artefacto de agregación**. Ambos lados son verdaderos en sus segmentos. Se admite bienestar **por segmento**.
2. **Ninguna salida con precisión decimal.** **60 de 144** números son ordinales cardinalizados y 74 asignados: la aritmética conserva orden, no magnitud. *(El conteo v1 era 54 de 107; recomputado en `modelo v2.1 §6`.)*
3. **Ninguna cifra de confianza interpersonal como establecida.** Hay cinco en circulación (12% · 21.8% · 22% · 32.1% · 18%) y **dos dicen ser la misma ENCUCI 2020 con 10.3 puntos de diferencia**. Conflicto abierto.
4. **Ninguna afirmación de "burbuja de sobreendeudamiento"** *(v2.5, P-06)*. El término admitido es **"riesgo latente focalizado y vigilable"**. La mora sube pero es baja, el crédito se desacelera, **el IMORA está en mínimos de una década** y el financiamiento a hogares es **18.7% del PIB** — base baja en comparación internacional. **La adopción de crédito fácil es real; la burbuja downstream NO está demostrada.**
5. **Ninguna inferencia ascendencia → conducta de grupo.**
6. **Ninguna afirmación sobre "el mexicano" sin segmento.**

---

*Las dos que necesitan desarrollo propio:*

> ### 5.4 Prohibición de bienestar agregado nacional *(ADR-27)*
>
> **El modelo no produce, no reporta y no admite ningún parámetro de bienestar, felicidad o afecto agregado a nivel nacional.**
>
> *Por qué:* México sale #10 mundial en satisfacción vital (WHR 2025) y simultáneamente registra 18.1M de carga de salud mental, 39.8% de soledad en adultos mayores y 135,445 desaparecidos. **Eso no es una contradicción empírica: es un artefacto de agregación.** Ambos lados son verdaderos en sus segmentos y solo chocan cuando se promedian en un número nacional. Un parámetro de bienestar agregado es precisamente el objeto que fabrica la paradoja.
>
> Las dos resoluciones fáciles —*"el mexicano feliz a pesar de todo"* y *"esa felicidad es negación"*— son igual de esencialistas.
>
> **Pendiente real y separado:** la escalera de Cantril mide **evaluación vital, no alegría**. Parte del lado "felicidad" del choque no está midiendo lo que se le atribuye.
>
> **Lo que sí se admite:** bienestar **por segmento**, con la pregunta bien planteada — *¿qué le pasa a la evaluación vital de una familia buscadora? ¿De una cuidadora de 60 años con 39.7 horas semanales no remuneradas?*

> ### 5.5 Prohibición de afirmar "burbuja de sobreendeudamiento" *(v2.5 — P-06 del barrido forense)*
>
> **El modelo no afirma una burbuja de sobreendeudamiento en México. El término admitido es "riesgo latente focalizado y vigilable".**
>
> *Por qué:* el forense V5 ordenó la degradación con dato duro y **la conclusión llegó a la ficha sin la evidencia que la obliga** — que es la forma exacta en que un matiz se convierte en eslogan. La evidencia: la mora sube **pero es baja**; el crédito **se desacelera**; el sistema es resiliente; **la métrica ajustada (IMORA) está en mínimos de una década**; y el financiamiento a los hogares es **18.7% del PIB** (REF Banxico, dic. 2025), una base **baja** en comparación internacional dentro de un financiamiento total al sector no financiero de 102.6%.
>
> **La adopción de crédito fácil es real; la burbuja downstream NO está demostrada.** Confirmar la premisa no autoriza la consecuencia — y el salto de una a otra es el error que esta prohibición bloquea.
>
> **Lo que sí se admite:** riesgo **focalizado** (BNPL invisible al buró, productos no garantizados de alto CAT, cohorte 18–29 con 28.6% de retrasos según ENSAFI 2023) y **vigilable** con indicadores nombrados. ⚠️ **El umbral de vigilancia es el de P-04:** IMOR popular sostenido por encima de **25–30%** sin margen de CAT.

---

## 6 · Procedencia de los números *(ADR-28.a)*

**Cada probabilidad y cada coeficiente lleva etiqueta obligatoria.** El validador rechaza la compilación si falta.

| Clase | v1 | **v2** |
|---|---|---|
| `MEDIDO` | 4 | **4** |
| `DERIVADO` | 6 | **6** |
| `ORDINAL→CARDINAL` | 54 | **60** |
| `ASIGNADO` | 43 | **74** |
| **TOTAL** | **107** | **144** — *97.2% no medido* |

*Motivación:* hoy un `0.93` leído de ENVIPE y un `0.74` puesto a criterio **se ven idénticos en el archivo**. Esa indistinción es la puerta por la que un pilar falso entra al modelo.

**Corolario, que además se registra como guardarraíl de lectura en la batería de refutaciones:** como `params = base + Σ coef` y los coeficientes son asignados, **la aritmética conserva orden pero no magnitud**. Ninguna salida se reporta con precisión decimal. Rangos o categorías.

**Desglose del salto 107 → 144** *(publicado en v2.1; la v2 declaraba el aumento sin dar la cifra)*:

| Componente | v1 | v2 | Δ | Por qué |
|---|---|---|---|---|
| `params_base` de perfil | 54 | **90** | +36 | 9 → 15 parámetros por perfil × 6 |
| ↳ `familismo` desdoblado | — | — | +6 | ADR-30 · `ORDINAL→CARDINAL` (la etiqueta existe en §1.1) |
| ↳ `confianza_institucional` escalar → **vector de 6** | — | — | +30 | ADR-28.b · `ASIGNADO`. ⚠️ **Sin poblar**: §1.3 declara el vector y da porcentajes nacionales, no valores por perfil |
| Coeficientes de generador | 14 | **15** | +1 | ADR-30 · `familismo_obligacion` en G5, `ASIGNADO` y **sin magnitud** (su spec es "signo negativo o no monotónico") |
| Probabilidades de regla | 39 | **39** | 0 | Sin cambio de esquema; corresponde a las 18 reglas implementadas de 42 |

**Los 42 disparadores de dominio NO cuentan como números** *(adenda a ADR-26)*: entran como **booleanos de contexto**, no como parámetros calibrables. Contarlos añadiría ~42 magnitudes que habría que calibrar sin dato.

⚠️ **DEUDA CON REQUISITO DE SALIDA — los 90 parámetros de dispersión.** ADR-28.d obliga a que cada `params_base` sea una **distribución**, y §1.2 rechaza en compilación toda configuración con varianza intraperfil cero. Eso implica **90 parámetros de dispersión que hoy no existen ni tienen familia declarada**. Mientras no se escriban, el check de 28.d **no puede correr**: es un principio sin artefacto de salida, el patrón que explica casi todos los fallos de este programa.
**Requisito:** `procedencia.yaml` lista, para cada uno de los 90 `params_base`, su familia de distribución y su dispersión con clase de procedencia. Si el archivo no los trae, el conteo real es **234**, y 90 de ellos son invisibles.

---

## 7 · Estado de validación

**Marcador honesto, actualizado al 30 de julio de 2026** *(el marcador original era del 27 de julio; el Hito D no existía todavía)*:

- **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 2 de 27 corridas archivadas** — `R1.1` → veredicto `D` (inejecutable por hueco de mercado, no de dato), `R3.2` → veredicto `B` (gate de 20pp aritméticamente inalcanzable). Fuente única: `hitoD-preregistro §Registro de veredictos archivados`.
- **Ejercicio distinto, no confundir con lo anterior (ADR-45, D-05):** `glosario §6/§10` corrió por su cuenta, el 27/jul/2026 — antes de que el Hito D existiera —, un ejercicio informal sobre "utilidad + fricción baja > confianza" (dominio seguro agrícola), **veredicto informal B**: sin contraejemplo limpio, candidato irresuelto, techo estructural que impide alcanzar el veredicto C con fuentes públicas. No tiene ID de regla, no vive en el bloque append-only de `hitoD-preregistro`, y no cuenta en el "2 de 27" de arriba.

**⚠️ PERÍMETRO DEL HITO D — fijado en v2.1 por conteo mecánico sobre §3.B, no de memoria:**

| Tier | Cuenta |
|---|---|
| `[FUERTE]` puro | **20** |
| `[MEDIA]` | **19** |
| `[MEDIA-FUERTE]` | **5** |
| `[FUERTE como correlación]` | 1 |
| `[FUERTE / MEDIA]` | 1 |
| `[MEDIA / HIPÓTESIS]` | 1 |
| `[HIPÓTESIS]` | **2** |
| **TOTAL** | **49** *(v2.5: +2 por la ampliación de alcance a crédito · v2.4: +3 por la segunda diagonal y las tres reglas que bajaron del barrido forense)* |

**Son 20 reglas `[FUERTE]`, no 19.** El "19" venía de `CHECKPOINT-v2 §9` —hoy fusionado en `estado`— y se contó **antes** del cambio 10 (§3.7 HIPÓTESIS → FUERTE) y quedó congelado. Distribución por dominio: §3.1 **3** · §3.2 1 · §3.3 **2** · §3.4 2 · §3.5 2 · §3.6 0 · §3.7 3 · §3.8 3 · §3.9 2 · §3.10 2.
**✅ PERÍMETRO DEL HITO D — DECIDIDO el 28/jul/2026: 27 reglas.** = 20 `[FUERTE]` + 1 `[FUERTE como correlación]` + 1 compuesta `[FUERTE / MEDIA]` + **5** `[MEDIA-FUERTE]`. *(Eran 26; la partición de protesta/autodefensa convirtió una `[MEDIA-FUERTE]` en dos.)* *(Decisión tomada antes de escribir el primer falsador, no después de ver resultados — que es el requisito.)*

⚠️ **Corrección de RÓTULO, 29/jul/2026 (cambio 34).** Este renglón decía *"20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas"*. Solo existe **una** compuesta: `R4.3` (`[FUERTE / MEDIA]`), cuya propia ficha en `hitoD-preregistro` se declara *"Compuesta: dos falsadores, uno por mitad"*. La segunda plaza que el rótulo contaba como compuesta la ocupaba `R1.4`, que es tier `[FUERTE como correlación]` — distinto de `[FUERTE / MEDIA]` y **no** una regla partida: lleva un solo falsador, que ataca la correlación. **El perímetro NO cambia: siguen siendo las mismas 27 reglas fijadas el 28/jul/2026, antes de escribir el primer falsador** — esto es una corrección de cómo se nombran 2 de las 27, no de cuáles son las 27.

**Registro congelado de IDs *(v3.3, cambio 35)*.** El esquema anterior derivaba el ID de (posición, tier): las 24 fichas de `hitoD-preregistro` numeran secuencialmente solo entre reglas de perímetro, saltando las `[MEDIA]` y `[HIPÓTESIS]` — así, `R4.2` ("hombre sin permiso laboral") es el 3.er bullet de `§3.4` pero el 2.º ID de perímetro, y `R7.4`/`R7.5` (protesta/autodefensa) son los bullets 8 y 9 de `§3.7`. Eso es inservible para un pre-registro: `gobernanza` pre-registra que una `[MEDIA-FUERTE]` que no sobreviva su falsador queda **degradada a `[MEDIA]`** — fuera del perímetro —, y si eso le pasa a `R7.4`, `R7.5` cambiaría de ID sin que nadie la haya tocado. **Un ID pre-registrado no puede cambiar como resultado de una falsación.**

**Decisión: los IDs son un registro CONGELADO, no una fórmula.** (a) Los **24 IDs ya usados en fichas** (`R1.1`–`R10.3`, ver `hitoD-preregistro`) quedan exactamente como están; nunca se recomputan. (b) `§3.3` nunca tuvo ficha; sus IDs salen de las citas que ya existen en `gobernanza` y `estado` (`R3.4` = el gate). (c) Las **22 reglas restantes** (sin ficha) reciben el número libre de su sección, en **orden posicional** entre sí — por eso `§3.4`, `§3.7` y `§3.9` quedan fuera de orden posicional frente a la línea del motor: **un ID es etiqueta, no posición.**

| ID | Línea | Enunciado corto | Tier | ¿Ficha? |
|---|---|---|---|---|
| `R1.1` | L213 | Volatilidad/informalidad → horizonte corto, ahorro informal | `[FUERTE]` | Sí |
| `R1.2` | L214 | Empleo formal estable → planeación larga (afore/seguro/hipoteca) | `[FUERTE]` | Sí |
| `R1.3` | L215 | Canal de confianza personal → sube adopción financiera | `[FUERTE]` | Sí |
| `R1.4` | L216 | Movilidad bloqueada + presión de estatus → consumo compensatorio | `[FUERTE como correlación]` | Sí |
| `R1.5` | L217 | Seguro de depósito/marca confiable → atenúa aversión | `[MEDIA]` | No |
| `R1.6` | L218 | Popular/informal + crédito alto CAT → sobreprecio con techo (15–20%) | `[MEDIA]` | No |
| `R1.7` | L219 | Baja fricción + usura + reporte incompleto → daño downstream | `[MEDIA]` | No |
| `R2.1` | L224 | Jerarquía tradicional → deferencia, iniciativa suprimida | `[FUERTE]` | Sí |
| `R2.2` | L225 | Liderazgo benévolo → lealtad; **SOLO** benevolencia legitima | `[MEDIA-FUERTE]` | Sí |
| `R2.3` | L226 | Prestaciones formales (IMSS/Infonavit) → pesan más que salario | `[MEDIA]` | No |
| `R2.4` | L227 | Joven urbano (perfil 5) → cambia de empleo sin culpa | `[MEDIA]` | No |
| `R3.1` | L232 | Trámite presencial discrecional sin registro → mordida | `[FUERTE]` | No |
| `R3.2` | L233 | Digitalización/testigos/registrable → baja la mordida | `[FUERTE]` | Sí |
| `R3.3` | L234 | Norma inútil + sanción improbable → evasión ("hacerse guaje") | `[MEDIA]` | No — **fuera del perímetro** |
| `R3.4` | L235 | Gobierno digital coercitivo (CoDi) rechazado vs. útil (SPEI) adoptado — **el gate** | `[MEDIA-FUERTE]` | No |
| `R4.1` | L240 | Sin IMSS + leve-moderado → farmacia con consultorio/automedicación | `[FUERTE]` | Sí |
| `R4.4` | L241 | Grave/crónico complejo → sistema público pese a la espera | `[MEDIA]` | No |
| `R4.2` | L242 | Hombre sin permiso laboral → pospone el chequeo | `[FUERTE]` | Sí |
| `R4.3` | L243 | Desabasto → abandono / familia cuidadora → adherencia | `[FUERTE / MEDIA]` — compuesta | Sí |
| `R4.5` | L244 | Producto con sellos + precio similar → elige menos sellos | `[MEDIA]` | No |
| `R5.1` | L249 | Volatilidad/ausencia de Estado → familia como seguro | `[FUERTE]` | Sí |
| `R5.2` | L250 | Cuidado (mayores/niños/enfermos) → recae en mujeres 40+ | `[FUERTE]` | Sí |
| `R5.3` | L251 | Baja garantía institucional del matrimonio → unión libre | `[MEDIA]` | No |
| `R5.4` | L252 | Cortejo urbano-joven-conectado → apps, guiones desiguales | `[MEDIA / HIPÓTESIS]` | No |
| `R6.1` | L257 | Cita formal-laboral vs. social → interruptor formal/informal | `[MEDIA]` | No |
| `R6.2` | L258 | Invitación social + descortesía de decir no → "sí voy" incierto | `[HIPÓTESIS]` | No |
| `R6.3` | L259 | Recursos escasos + urgencias → pospone, "bomberazo" | `[MEDIA]` | No |
| `R6.4` | L260 | Cita médica con costo por faltar → cumple más con recordatorio | `[MEDIA]` | No |
| `R7.1` | L265 | Peso percibido del acto → participación diferencial | `[FUERTE]` | Sí |
| `R7.2` | L266 | Delito sin cobertura de seguro → no denuncia (cifra negra) | `[FUERTE]` | Sí |
| `R7.3` | L267 | Transferencia sin proximidad/monitoreo → conserva autonomía del voto | `[FUERTE]` | Sí |
| `R7.6` | L268 | Proximidad/focalización o monitoreo percibido → autonomía cede localmente | `[MEDIA]` | No |
| `R7.7` | L269 | Dádiva + broker → compra turnout, no vote-choice | `[MEDIA]` | No |
| `R7.8` | L270 | Transferencia no condicionada → se vive como derecho (entitlement) | `[HIPÓTESIS]` | No |
| `R7.9` | L271 | Transferencia no condicionada → atribución al líder, no voto comprado | `[MEDIA]` | No |
| `R7.4` | L272 | Agravio + falla estatal + red previa + entorno urbano → protesta | `[MEDIA-FUERTE]` | Sí |
| `R7.5` | L273 | Agravio + falla estatal + red previa + vacío rural → autodefensa | `[MEDIA-FUERTE]` | Sí |
| `R8.1` | L278 | Comité con monitoreo + sanción visible → contribuye; sin ellos, free-riding | `[FUERTE]` | Sí |
| `R8.2` | L279 | Conoce a la organizadora → entra a la tanda; desconocidos → evita | `[FUERTE]` | Sí |
| `R8.3` | L280 | Puente personal → confía en el desconocido; sin puente, desconfía | `[FUERTE]` | Sí |
| `R8.4` | L281 | Pueblo mestizo con sanción social → participa; urbano sin sanción → baja | `[MEDIA]` | No |
| `R9.3` | L287 | Allegado de confianza → sube credibilidad inicial | `[MEDIA]` | No |
| `R9.1` | L288 | Experto accesible/cercano/asequible → defiere | `[FUERTE]` | Sí |
| `R9.2` | L289 | Vacuna/servicio disponible + campaña llega → la mayoría acepta | `[FUERTE]` | Sí |
| `R9.4` | L290 | Clase media con miedo a caer → escuela privada como seguro anticaída | `[MEDIA]` | No |
| `R10.1` | L297 | Rechazo → indirecto (face + simpatía) | `[FUERTE]` | Sí |
| `R10.2` | L298 | Retroalimentación negativa pública → destruye capital social | `[MEDIA-FUERTE]` | Sí |
| `R10.3` | L299 | Inseguridad/autoridad no confiable → "ver, oír y callar" | `[FUERTE]` | Sí |
| `R10.4` | L300 | Interlocutor norteño/joven vs. sur/mayor/rural → directividad distinta | `[MEDIA]` | No |

⚠️ **La identidad de cada ID es el texto de la regla, NO la línea.** El validador (`tests/validador_registro_ids.py`) ancla cada ID a una subcadena estable del propio `SI` de la regla, y localiza esa subcadena por búsqueda de texto dentro de su sección — nunca por número de línea. La columna **Línea** de arriba es solo referencia de lectura contra esta versión del archivo (v3.3): si el documento se reedita y las reglas se desplazan, la línea cambia pero el ID **no**, porque no depende de ella. Un registro anclado a posición reintroduciría el acoplamiento (posición, tier) que este registro congelado vino a eliminar — ver PASO 2 de la sesión del 29/jul. *(49 filas: las 27 de perímetro con ficha o con cita en canon, más las 22 sin ficha de las demás secciones. Recuento exacto: `python3 tests/validador_registro_ids.py`.)*

**Cómo se pre-registran las 6 que no son `[FUERTE]` pura, para que la ambigüedad de tier informe en vez de estorbar:**

| Grupo | Regla de pre-registro |
|---|---|
| **Las 4 `[MEDIA-FUERTE]`** | El falsador se escribe **contra la lectura fuerte**. Si sobrevive → el tier sube y queda justificado. Si no sobrevive → **no queda refutada: queda degradada a `[MEDIA]`.** Degradar es resultado, no fracaso |
| **`[FUERTE / MEDIA]`** (§3.4 desabasto/adherencia) | Son **dos mitades con tier distinto**: **un falsador cada una**, no uno compuesto |
| **`[FUERTE como correlación]`** (§3.1 consumo compensatorio) | El falsador ataca **la correlación**, no la causalidad. ⚠️ V1 la "rompió" como *driver decisivo aislado* — **afirmación distinta**. Repetir ese ataque reproduce el error del Hito 2 |
- **De 13 reglas que las cuatro verticales dijeron estresar: 6 no existían en el motor, 4 divergían, 3 eran fieles.** V2 (clientelismo) es el único vertical cuyas reglas ancla son fieles al canon.
- **49 refutaciones corridas por primera vez contra el modelo: 27 pasan, 3 fallan, 8 sin objeto, 11 requieren el ejecutable.** Los tres fallos son los cambios 1, 2 y 5 de este v2. *(Resultados incorporados a `refutations.yaml` v0.2.0 el 28/jul; hasta entonces vivían solo en `corrida-refutaciones.md` y el YAML seguía marcado como "propuesta".)*
- **Siete generadores: uno probado (G3), uno contradicho (G1b), uno contestado (G2), cuatro sin falsar. Quince coeficientes: cero medidos.**
- **144 números: cuatro medidos** (§6). Y **90 parámetros de dispersión exigidos por ADR-28.d que no existen en archivo** — mientras falten, el check de varianza intraperfil no puede correr.

**Ocho refutaciones no tienen objeto en el modelo** — incluida `ref.A.02` (*"los mexicanos son flojos"*), **la única de tier MUY_FUERTE de las 49**, con el dato más contundente del corpus: 2,207 h/año, el mayor de la OCDE. El modelo no tiene variable de esfuerzo ni de horas. Tampoco tiene colorismo, salud mental ni entidad prestamista. **Decisión pendiente: ampliar el modelo o declarar el alcance y retirarlas de la batería.**

> **Lectura correcta de este marcador.** El modelo es hoy **una síntesis rigurosa de literatura con tiers leídos, no un artefacto validado.** Eso no lo invalida —un tier derivado de lectura disciplinada es evidencia legítima— pero la diferencia importa mucho cuando alguien lo use para decidir algo caro.

---

## 8 · Cómo se propaga un cambio a este documento *(ADR-29)*

**Bidireccional, no en cascada.** Cuando una validación rompe o degrada una afirmación:

1. El **report dueño** recibe nota de corrección fechada *(29.a)*.
2. El **artefacto forense se archiva como canónico** junto a los reports, completo e **incluyendo los casos descartados con su motivo** *(29.b)*.
3. El modelo se **sincroniza internamente**: §3 no puede cargar tiers que §7 ya superó *(29.c)*.
4. **El validador rechaza un artefacto forense sin tabla de descartes**, igual que rechaza un número sin procedencia *(adenda)*.

*Por qué el punto 4:* el defecto nunca fue que faltara el protocolo — fue que **nadie estaba obligado a ejecutarlo**. Con la misma plantilla, V1 archivó sus descartes y V3 no archivó ninguno. Un principio necesita un artefacto de salida que **falte visiblemente** si no se cumple.

**Casos conocidos de propagación fallida** (seis; **cinco cerrados y verificados**, uno consumado):

| Caso | Estado |
|---|---|
| Hofstede en consumidor | ✅ **Parchado en la fuente el 28/jul/2026**, con nota fechada. ⚠️ El registro lo daba por hecho el 27/jul y **era falso**: la decisión existía (ADR-06), la nota no |
| Honor en comunicación | ✅ **Parchado en la fuente el 28/jul/2026**, con nota fechada. Mismo falso positivo que el anterior |
| Honor "híbrido" en foundational | ✅ **Resuelto por ADR-31 y parchado el 28/jul/2026**. Era el único de los tres correctamente registrado como abierto |
| G1 empaquetado en el motor | ✅ *(v2)* |
| `§3.7` en HIPÓTESIS | ✅ *(v2)*. ⚠️ En v2.1 se descubre que el ascenso arrastró una **segunda** afirmación de tier menor: regla partida (conf.07) |
| **PD-01 · 14 descartes irrecuperables** | ❌ **Pérdida consumada. No reconstruir.** |

⚠️ **Requisito de salida añadido en v2.1 (ADR-32 propuesto).** Dos de los seis casos figuraban como reparados sin estarlo. **Un caso de retropropagación no se marca ✅ sin `grep` verificado contra el report dueño**, y la nota de corrección en la fuente es el artefacto que falta visiblemente si no se hizo. Sin eso, el registro de propagación mide intenciones, no archivos.

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** El riesgo mayor entra por `familismo_obligacion`. La configuración "apoyo alto + obligación alta" de los perfiles 2, 3 y 6 describe hogares donde el pooling es **estrategia económica ante Estado ausente**, no intensidad cultural de afecto. Si el parámetro se lee como "estas familias son más familieras", el modelo reproduce el esencialismo que combate. La marca **(b)** y el mecanismo nombrado de `§1.5` son lo que lo impide.

**¿Qué sobregeneraliza desde clases medias urbanas?** El perfil 1 sigue siendo el mejor evidenciado y la fuente declarada del sesgo. Y ADR-28.d lo agrava antes de aliviarlo: hasta que las distribuciones se especifiquen con dispersión real, el clasemediero seguirá siendo un punto bien medido rodeado de puntos mal medidos.

**¿Qué está sesgado por marcos o muestras extranjeras?** Los dos parámetros nuevos de familismo son **(b)** — Sabogal, Lugo Steidel, Knight, Calzada, Zeiders, casi todas con muestras mexicano-americanas. **Se está reestructurando el esquema sobre medición de diáspora.** Es defendible porque la marca viaja con el parámetro, pero es una deuda, no una solución.

**¿Qué cambiaría con foco rural, indígena o popular?** Las dos refutaciones que más protegerían al México popular —`ref.A.02` (esfuerzo) y `ref.B.04` (colorismo)— son dos de las ocho **sin objeto**. El modelo no tiene parámetros para ellas. No es casualidad: es el sesgo de clase reproducido en la elección de variables, y este v2 no lo repara.

**¿Qué parece psicológico y es un incentivo?** El resultado de G3, si se lee mal. Progresa confirma que **al estabilizar el ingreso cambia la conducta** — lo cual es a la vez la victoria del generador y la demostración de que el driver es estructural. G3 es el generador que mejor sobrevive **y** el que más claramente dice que manda el entorno.

**¿Dónde hay evidencia débil e intuición fuerte?** En el desdoblamiento de familismo. La distinción apoyo/obligación está bien fundada en la literatura, pero **nadie ha medido los dos parámetros por separado en población EN México**. Son dos números asignados donde había uno. Lo que lo hace defendible es el test de dominancia; sin él, es superficie nueva sin información nueva.

**¿Qué conclusión sería peligrosa mal usada?** Que el v2 "arregló el modelo". Arregló **tres fallos confirmados** de la batería y **una capa de generadores mal especificada**. No tocó: los 43 números asignados, los cuatro generadores sin falsar, las 41 reglas sin prueba, ni las ocho variables ausentes. **El corpus se defiende bien; el aparato de validación sigue a medio construir.**

---

## 9 · Si vas a cruzar hallazgos contra este documento

**Cita la regla textualmente**, con su tier, dominio y perfiles. Si tu encargo te pidió estresar una regla que no aparece en §3.B, **es una propuesta nueva** y tu veredicto **no cuenta como validación del modelo** — cuenta como evaluación de una hipótesis.

⚠️ **Este documento ES el motor: contiene las 49 reglas, no una foto de ellas.** La ficha derivada que existía hasta v2.5 omitía cuatro `[FUERTE]` y degradaba una: si un encargo previo te pidió estresar algo del dominio **Familia y pareja**, de la **tanda** o del **puente personal**, y no lo encontraste, el hueco estaba en la ficha, no en el motor. **Esa clase de fuga ya no es posible: una sección no se puede desincronizar de su propio documento.**

*Por qué: de 13 reglas que las cuatro verticales dijeron estresar, **6 no existían en el motor** y 4 divergían en alcance. Sus veredictos no transfirieron.*
