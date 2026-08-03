# Modelo de decisión del mexicano contemporáneo
### `modelo` · **v4.0** · CANÓNICO OPERATIVO

> | | |
> |---|---|
> | **ARCHIVO** | `modelo-decision-v4_0.md` |
> | **REEMPLAZA A** | `modelo-decision-v3_4.md` — **borrar** |
> | **VERIFICAS ASÍ** | §0 llega al **cambio 37** · **§1.1 es un diseño de síntesis de población, no una tabla de perfiles** — si encuentras una tabla de 6 filas × 15 parámetros, estás leyendo el v3.4 · §1.1.D trae la **prohibición de condicionar sobre número de perfil** · §1.1.F trae el **denominador derivado** con su aritmética · la regla R1.1 de §3.1 trae la marca `DOMINIO AGRÍCOLA: INEJECUTABLE` · §7 trae el **Registro congelado de IDs** (tabla de 49 filas) |
> | **NOMBRE ESTABLE** | **`modelo`** — cítalo así (*"ver `modelo §3.B`"*), **nunca por nombre de archivo**. Así las versiones suben sin dejar referencias colgando |

> **v4.0 — 3/ago/2026. MAYOR: la unidad de población deja de ser el perfil. §1.1 pasa de tabla a diseño de síntesis; los seis perfiles pasan de BASES a DESCRIPTORES.** *(ADR-51 · `revision-programa-2026-07-31.md` §2 · P1 `forense/notas/2026-07-31-p1-enigh-semilla.md` · P2 `forense/notas/2026-08-01-p2-momentos-atributos.md`.)* El motor sigue en **49 reglas**; el perímetro del Hito D sigue en **27**; los siete generadores de §2 y sus quince coeficientes **no cambian de contenido**. Lo que cambia es **sobre qué se define un agente**: ya no pertenece a uno de seis perfiles con quince valores puntuales, sino que porta un **vector de atributos observables** y los parámetros del modelo son **distribuciones condicionales sobre ese vector**. Las 10 reglas que citaban número de perfil citan ahora el atributo que ya codificaban, **sin cambio predictivo** (§1.6). El contador nuevo del programa es **"condicionales medidas sobre atributos: ~~6~~ 8 de 14"** *(corregido 4/ago/2026 — `CAL-CONF` Fase B posiciones 5-6 midió `radio_confianza` (ENCUCI) y `familismo_apoyo` (ENIF), `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §5)*, con `D`=14 derivado en §1.1.F.
>
> | # | Cambio | Origen |
> |---|---|---|
> | 37 | **§1.1: la tabla 6×15 sale; entra el diseño de síntesis de población.** Vector de atributos observables (P1, seis ejes con variable, módulo y llave citados), parámetros como condicionales, semilla ENIGH reponderada por **IPU**, y los dos límites declarados verbatim de `revision §4`. Los seis perfiles se conservan como **descriptores** de regiones del espacio de atributos, con prohibición explícita de que cualquier componente del motor condicione sobre número de perfil. Los 90 `ASIGNADO` de la tabla vieja pasan a **hipótesis falsables sobre las condicionales** (12 conservadas, 5 patrones descartados con motivo). Denominador nuevo derivado: **14 condicionales** | **ADR-51 · revisión 31/jul · P1 · P2** |
>
> ⚠️ **Lo que este acto NO hace.** No toca `gobernanza` ni `estado` (Encargo A, ADR-51). No cambia el contenido de §2 (generadores) ni de §3 más allá de la traducción perfil→atributo de las 10 reglas que citaban perfil. **No inventa umbrales ni formas funcionales:** donde no hay evidencia, la condicional queda declarada con forma **PENDIENTE** y tier honesto, no rellenada. No mueve `4 de 144` (congelado, `forense/hallazgos.md` 31/jul) — ver §6.
>
> ⚠️ ~~**DETENTE declarado, no ejecutado (§1.1.D).** El disparador global 7 de `§3.A` es `segmento` = *"cuál de los seis perfiles"* — es un componente del motor que condiciona sobre número de perfil, exactamente lo que §1.1.D prohíbe. Traducirlo cambiaría contenido de §3, fuera del perímetro de este acto. **Queda como contradicción declarada, pendiente de mesa.**~~ **Ejecutado 3/ago/2026.** El disparador global 7 de `§3.A` se tradujo a `vector de atributos` — verificado que ninguna de las 49 reglas de §3.B condiciona directamente sobre él, así que la traducción no cambia ninguna predicción, misma disciplina que las 10 reglas de §1.6. Ver §3.A.

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

## 1 · La población: síntesis sobre atributos, perfiles como descriptores

No hay tipos puros: una persona real combina rasgos, y **la variación dentro de un perfil suele ser mayor que la variación entre países** (Fischer & Schwartz) **(c)**. Hasta el v3.4 esa advertencia convivía con una tabla que asignaba cada agente a **uno** de seis perfiles con quince valores puntuales — la advertencia decía una cosa y el esquema hacía otra.

**Desde el v4.0 el esquema hace lo que la advertencia decía.** Un agente no pertenece a un perfil: **porta un vector de atributos observables**, y los parámetros del modelo son **distribuciones condicionales sobre ese vector**. Los seis perfiles se conservan —son el resumen del corpus— pero como **descriptores** de regiones del espacio de atributos, no como casillas de asignación exclusiva (§1.1.D). La distinción es la estándar de Wedel & Kamakura entre **bases** y **descriptores** de segmentación **(c)**.

### 1.1 Diseño de síntesis de población

> **La tabla 6×15 sale.** Sus 90 celdas eran `ASIGNADO` —juicio informado, cero medidos— y su forma imponía un *forced choice* de segmentación a priori que falla el criterio de identificabilidad (`revision-programa-2026-07-31.md` §0, §2). Lo que valía de ellas se conserva como **hipótesis falsables sobre las condicionales** (§1.1.E), no como valores.

#### 1.1.A · El vector de atributos observables

Un agente sintético queda descrito por **seis ejes**. Las variables, módulos y llaves de abajo son las que **P1 verificó leyendo el paquete en disco** (`forense/notas/2026-07-31-p1-enigh-semilla.md` §1-§2, ENIGH 2022 nueva serie, `enigh2022_nc_csv`, sha256 verificado contra `data/manifiesto.yaml`) — **se citan, no se reescriben de memoria**. La base del registro sintético es el módulo `poblacion`, con llave **PERSONA** `folioviv`+`foliohog`+`numren`.

| # | Eje | Variable(s) exacta(s) · valores | Módulo | Llave de unión a persona | Nivel real |
|---|---|---|---|---|---|
| 1 | **Formalidad laboral** | `segsoc` — 1 Sí / 2 No (derechohabiencia) | `poblacion` | PERSONA directa (`folioviv`+`foliohog`+`numren`) | **persona** |
| 1b | | `contrato`, `tipocontr`, `pres_1..20` (incl. **`pres_8`** = SAR/AFORE), `medtrab_1..7` | `trabajos` | PERSONA vía `folioviv`+`foliohog`+`numren` **+ `id_trabajo`** (1 principal / 2 secundario); **sin fila para quien no trabajó** | **persona** |
| 2 | **Edad** | `edad` — entero, años | `poblacion` | PERSONA directa | **persona** |
| 3 | **Urbanización / tamaño de localidad** | `tam_loc` — 1 · 100 000+ / 2 · 15 000–99 999 / 3 · 2 500–14 999 / 4 · <2 500 (catálogo `tam_loc.csv`) | `concentradohogar` (copiada de `viviendas`) | HOGAR (`folioviv`+`foliohog`), heredada a cada persona del hogar | **hogar** |
| 4 | **Ingreso** | `ing_cor` (monto trimestral, continuo) + `est_socio` (catálogo `est_socio.csv`: 1 Bajo / 2 Medio bajo / 3 Medio alto / 4 Alto) | `concentradohogar` | HOGAR, heredada | **hogar** |
| 5 | **Acceso digital** | `celular` (SERV_2), `conex_inte` (SERV_4) — 1 Sí / 2 No, **tenencia binaria** | `hogares` | HOGAR, heredada | **hogar** |
| 6 | **Condición migratoria** | `residencia` — 32 entidades + "Estados Unidos de América" + "Otro país" (catálogo `residencia.csv`, 34 categorías) | `poblacion` | PERSONA directa | **persona** |
| 6b | | `remesas` — Σ de `ingresos.ing_tri` cuando clave ∈ {**P041**} (complementaria, no necesaria) | `concentradohogar` | HOGAR, heredada | **hogar** |

**Veredicto de P1, citado:** los seis ejes llegan a **EN CONJUNTA** o **EN CONJUNTA VÍA HOGAR**; ninguno cae en FUERA DE CONJUNTA. El veredicto global es **CONJUNTA COMPLETA** (P1 §3).

⚠️ **RESTRICCIÓN DE NIVEL HOGAR — declarada aquí porque el diseño la hereda, no la resuelve.** P1 §3, verbatim:

> *"3 de 6 ejes (urbanización, ingreso, acceso digital) y el componente `remesas` del eje 6 son atributos de **hogar**, no de persona — todas las personas del mismo hogar comparten el mismo valor en esas columnas tras el join. Si P2 va a construir celdas de atributos que requieran varianza intra-hogar en tamaño de localidad, ingreso o acceso digital (ej. 'dos hermanos del mismo hogar en celdas distintas por ingreso'), esa varianza **no existe en ENIGH** — es indistinguible de una persona a otra del mismo hogar por diseño del instrumento, no por un hueco de esta sesión. Edad, formalidad laboral y residencia (ejes 1/2/6) sí varían persona a persona."*

Consecuencias, aplicadas y no asumidas (P2 §1.b):

- **La malla es mixta:** un agente hereda **3 coordenadas de su hogar** (urbanización, ingreso, acceso digital) y porta **3 propias** (formalidad, edad, migración).
- **Ninguna condicional puede definirse por contraste intra-hogar en los tres ejes de hogar.** No es una celda vacía por muestra pequeña: es vacía **por diseño del instrumento**.
- **Ahí muerde el check de ADR-30** (apoyo vs. obligación): el contraste que ese check exige —quien da cuidado frente a quien lo recibe, bajo el mismo techo— cae exactamente en la dimensión que la malla no resuelve. Ver §1.1.E, H-11.

⚠️ **Dos límites del propio eje, declarados por P1 y no corregidos aquí:** (i) el eje 5 es **más débil que los demás** — tenencia binaria del hogar, sin distinguir celular básico de *smartphone*, sin uso individual ni banca en línea; (ii) del eje 6, ni el diccionario ni `metadatos_enigh_2022_ns.txt` traen el texto literal de la pregunta, así que **no se puede confirmar la referencia temporal de `residencia`** (¿hace cinco años? ¿al nacer?) sin el cuestionario, que no viene en el paquete.

#### 1.1.B · Los parámetros son distribuciones condicionales sobre atributos

Cada parámetro del modelo deja de ser una constante por perfil y pasa a ser una **distribución condicional** sobre el vector de atributos:

> **θ_k( · | x )**, con **x** = (formalidad, edad, urbanización, ingreso, acceso digital, migración) del agente.

Tres propiedades, y ninguna es opcional:

1. **Es una distribución, no una media.** ADR-28.d sigue vigente y se relee sobre la malla nueva: dos agentes **con el mismo vector de atributos deben poder diferir**. La dispersión no es un extra: es parte de la especificación de θ_k.
2. **La restricción de nivel hogar viaja con la condicional.** Cuando **x** entra por un eje de hogar (3, 4, 5), la condicional está definida **sobre una coordenada compartida por todas las personas del hogar**: no puede separar a dos miembros del mismo hogar en esa dimensión, y toda hipótesis que lo pretenda es infalsable con ENIGH (§1.1.A).
3. **La forma funcional NO se inventa en este acto.** Ninguna condicional recibe aquí umbrales, tramos ni familia paramétrica. Donde no hay evidencia, la condicional queda **declarada con forma PENDIENTE** y tier honesto. Inventarlas para poder multiplicar celdas sería teclear una cifra esperada — el error que P2 §1.a nombra y rechaza.

⚠️ **Lo que este cambio compra y lo que cuesta, sin regatear (P2 §2.b).** Bajo perfiles, θ_k **venía dado** por los 90 `ASIGNADO`: era un supuesto. Bajo atributos, θ_k **hay que estimarlo**: es una medición. Se cambió un supuesto por una medición — y para **6 de los 9 parámetros que los generadores multiplican, esa medición no existe o no es determinable con el corpus en disco**. El caso más limpio es `deferencia`/G6, que INV-SEG p3 daba por sano bajo perfiles y **empeora** bajo atributos (ADR-51 (e)). El reencuadre **reubica** la subidentificación; no la disuelve.

⚠️ **Y no basta con que el reactivo exista.** El criterio operativo lo fija P2 §2.b (C1–C4) y ADR-51 lo adopta: un coeficiente `β_gk` queda identificado solo si el reactivo de θ_k y un desenlace de una regla que el generador enruta **se observan en el mismo instrumento**, con variables distintas y con variación entre celdas. **La reponderación no fabrica esa conjunta** (§1.1.C).

#### 1.1.C · Semilla y reponderación: ENIGH + IPU

**Semilla.** El microdato semilla es **ENIGH** —la fuente que P1 verificó con los seis ejes en el mismo registro-persona—, construido sobre `poblacion` y uniendo `trabajos` por persona (`+id_trabajo`) y `hogares`/`concentradohogar` por hogar. La edición en disco es **ENIGH 2022 nueva serie**; ENIGH 2024 solo tiene *placeholder* de plantilla en `data/manifiesto.yaml`, no publicada (P1 §0).

**Reponderación.** El método de referencia es **IPU — *Iterative Proportional Updating*** (Ye, Konduri, Pendyala, Sana & Waddell, 2009) **(c)**, **no IPF plano**. La razón es la restricción de §1.1.A y no una preferencia de estilo: tres de los seis ejes son marginales de **hogar** y tres son marginales de **persona**, y el IPF plano ajusta un solo nivel a la vez, de modo que satisfacer las marginales de persona desajusta las de hogar y viceversa. IPU ajusta **pesos de hogar reproduciendo simultáneamente marginales de hogar y de persona**, que es exactamente la consistencia que esta malla mixta necesita.

⚠️ **IPU entra marcado como (c) — marco teórico importado, PENDIENTE DE CRÍTICA en el diseño ejecutable.** Se nombra como método de referencia, no como método sellado. Lo que el diseño ejecutable debe criticar antes de correrlo, como mínimo: el criterio de convergencia, el tratamiento de celdas de peso cero, la fuente de cada marginal (el inventario de INV-SEG partes 1–2 es el insumo) y si la consistencia hogar-persona que IPU promete sobrevive a los ejes que ENIGH mide solo a nivel hogar. **Ningún resultado de este documento depende de que IPU sea el método final.**

> ### Límites declarados de la síntesis
>
> **(i) La cola alta A/B no se observa** — `revision-programa-2026-07-31.md` §4, **verbatim**:
>
> > *"**La cola alta sigue sin observarse.** IPF no inventa datos: si las encuestas de hogar no capturan a la élite A/B, la población sintética tampoco. Esto se declara como límite permanente del dato público mexicano, no se resuelve."*
>
> **(ii) La síntesis hereda la conjunta de la semilla** — misma revisión, **§7**, verbatim:
>
> > *"la síntesis IPF hereda sus propios supuestos (la conjunta de la semilla se preserva al reponderar) — no es magia, es un supuesto distinto y declarable."*
>
> Y su corolario operativo, derivado por P2 §1.d: **el IPU reproduce marginales; no fabrica conjuntas que nadie midió.** Si el reactivo de un parámetro vive en la fuente A y el desenlace del generador que lo usa vive en la fuente B, ninguna reponderación crea la covarianza individual entre los dos. **La síntesis amplía la malla de atributos; no amplía la malla de pares (parámetro, desenlace).**
>
> **(iii) Se pierde la comparabilidad con lo escrito en términos de perfiles** — `revision §4`, verbatim: *"hitoD (12 menciones), fichas, notas históricas — son append-only y quedan como historia. Toda referencia futura necesita la traducción perfil→región de atributos."* Esa traducción es §1.1.D.
>
> *Nota de citación: el encargo que comisiona este acto atribuye los dos primeros límites a `revision §4`. El primero está en §4; el segundo está en **§7** del mismo documento. Se cita cada uno donde vive.*

#### 1.1.D · Los seis descriptores — y la prohibición

Los seis perfiles **se conservan como vocabulario**: son el resumen del corpus y la forma en que este programa lleva un año hablando de heterogeneidad. Dejan de asignar agentes y pasan a **nombrar regiones del espacio de atributos**. Cada región se define abajo **en términos de los atributos de §1.1.A**, con sus cortes explícitamente marcados cuando no existen.

| Descriptor | Región en el espacio de atributos (variables de §1.1.A) | Estado |
|---|---|---|
| **1 · Clasemediero urbano formal** | `segsoc`=1 (o `contrato` formal con `pres_8`) **∧** `tam_loc`=1 **∧** `est_socio` ∈ {3 Medio alto} | Región definible. Sigue siendo **el mejor evidenciado y la fuente declarada del sesgo** (§0.2, ADR-13) |
| **2 · Popular informal** | `segsoc`=2 **∧** `est_socio` ∈ {1 Bajo, 2 Medio bajo}; `tam_loc` **sin restringir** (urbano y rural) | Región definible. El extremo rural sigue submuestreado |
| **3 · Vulnerable en ascenso** | **No es una región.** Es una **trayectoria** entre regiones | ⚠️ **No definible en transversal.** `revision §3`: *"deja de ser celda. Si se conserva, es una **transición**"* — su ruta es el pseudo-panel de cohortes, no una celda de atributos |
| **4 · Élite A/B urbana** | `est_socio`=4 (Alto) + cola alta de `ing_cor` | ⚠️ **Región NO OBSERVADA.** Límite declarado (i) de §1.1.C: la encuesta de hogar no la captura, la síntesis tampoco. Se nombra, no se puebla |
| **5 · Joven Gen Z urbano conectado** | `edad` joven (**corte PENDIENTE** — sin partición canónica en P1) **∧** `tam_loc`=1 **∧** `conex_inte`=1 | Región definible salvo el corte de edad. **Eje transversal a la formalidad**, no un rival de ella — por eso ya no hay solapamiento que resolver |
| **6 · Migrante / transnacional** | `residencia` ∈ {"Estados Unidos de América", "Otro país"} **∨** hogar con `remesas` (P041) > 0 | Región definible, con el límite (ii) de §1.1.A: la referencia temporal de `residencia` no está confirmada |

**Lo que el reencuadre disuelve por construcción** (P2 §1.c): las tres patologías que INV-SEG parte 3 nombró —las dos uniones forzadas `{1∪4}` y `{2∪3}`, el solapamiento del perfil 5 y la heterogeneidad del perfil 6— **desaparecen, porque ya no hay partición que violar**. Un agente puede estar en la región 2 y en la 5 a la vez; eso ya no es un defecto, es lo que el espacio de atributos permite.

> ### 🚫 PROHIBICIÓN · Ningún componente del motor puede condicionar sobre número de perfil
>
> **Ni una regla de §3, ni un generador de §2, ni un disparador, ni una salida, ni un archivo de `rules/*.yaml` puede tomar como entrada "el agente es del perfil N".** El número de perfil no es un dato del agente: el agente lleva atributos, y un perfil es una etiqueta de conveniencia para hablar de una región de ese espacio.
>
> **Por qué, sin suavizar:** condicionar sobre perfil reintroduce el *forced choice* que el reencuadre eliminó, y con él la forma estadística del esencialismo —seis clases de mexicano— que este corpus existe para combatir. Es el mismo argumento con que §1.2 rechaza en compilación la varianza intra-celda cero, un nivel más arriba.
>
> **Check de compilación:** una configuración cuyo motor lea un identificador de perfil se rechaza.
>
> ⚠️ ~~**DETENTE — la prohibición tiene hoy una violación en el propio canon, y este acto no la corrige.** El **disparador global 7 de `§3.A`** es `segmento` — *"cuál de los seis perfiles"*. Es literalmente un componente del motor que condiciona sobre número de perfil. Traducirlo cambiaría el contenido de §3, que está **fuera del perímetro de este acto** (el reencuadre es de unidad de población, no de maquinaria causal). Se declara aquí como **contradicción abierta, pendiente de decisión de mesa**, y no se resuelve en silencio. La traducción natural —`segmento` deja de ser "cuál de los seis perfiles" y pasa a ser "el vector de atributos del agente"— **no se ejecuta aquí**.~~ **Traducción ejecutada 3/ago/2026** (decisión de mesa ya implícita en el sello de ADR-51, misma disciplina que las 10 reglas de §1.6): `segmento` pasa a `vector de atributos del agente` en `§3.A`. Verificado antes de traducir que ninguna regla de `§3.B` condiciona su `SI` sobre este disparador —leen atributos individuales, no la etiqueta de nivel 1— así que la traducción **no cambia ninguna predicción**. La contradicción con esta prohibición **queda cerrada**.

#### 1.1.E · Los 90 `ASIGNADO` traducidos: doce hipótesis falsables, cinco patrones descartados

Los 90 valores puntuales eran `ASIGNADO` — juicio informado, cero medidos. `revision §4`, verbatim: *"Lo que valía de ellos (los patrones relativos: el perfil 2 con horizonte más corto que el 1) se conserva como hipótesis sobre las condicionales, ahora falsables."* Eso es lo que sigue.

**Aritmética de la traducción, derivada de la tabla que sale:** la tabla del v3.4 tenía 6 filas × 15 parámetros = **90 celdas**, pero solo **nueve columnas traían valor** (Horizonte, Radio conf., Aversión, Estatus, Deferencia, `fam_apoyo`, `fam_oblig`, Violencia, Acceso) → **54 celdas pobladas**. Las otras **36** son el vector `confianza_institucional` (6 componentes × 6 perfiles), que la tabla **declaraba y nunca poblaba**: remitía a §1.3, que da porcentajes nacionales, no valores por perfil (§6, nota del +30). **54 + 36 = 90.** No hay patrón relativo que traducir en esas 36 — su pérdida es una ausencia que la tabla ocultaba, no información que se va.

**Cada hipótesis va con su atributo condicionante, su falsador y su estado de medición.** El estado de medición viene de P2 §2.c y de ADR-51 (c); **ninguna está medida hoy** (§1.1.F).

| # | Hipótesis sobre la condicional | Atributo condicionante (variable de §1.1.A) | Estado del reactivo | Tier |
|---|---|---|---|---|
| **H-01** | E[`horizonte_temporal` \| informal] **<** E[`horizonte_temporal` \| formal] | Formalidad — `segsoc`, `contrato`, `pres_8` | Proxy ENIF `P4_10`; ⚠️ **falla C3** frente al desenlace de G3 (P2 §2.d) | `[FUERTE]` en dirección (es la cláusula de G3, único generador probado) · **forma PENDIENTE** |
| **H-02** | E[`horizonte_temporal` \| joven urbano conectado] **<** E[`horizonte_temporal` \| adulto urbano formal] | Edad (**corte PENDIENTE**) × `tam_loc`=1 × `conex_inte` | Mismo proxy, mismo defecto | `[HIPÓTESIS]` — el "corto (inmediatez)" del perfil 5 nunca tuvo dato mexicano citado |
| **H-03** | E[`radio_confianza` \| migración o remesas] **>** E[`radio_confianza` \| sin migración] | `residencia` ∈ {EUA, Otro país}; `remesas` (P041) | **Reactivo directo** ENCUCI `AP5_1_1/2/3` | `[MEDIA]` **(b)** — el radio transnacional se sostiene en evidencia de diáspora |
| **H-04** | E[`aversion_riesgo` \| informal, ingreso bajo] **>** E[`aversion_riesgo` \| formal, ingreso medio-alto] | `segsoc` × `est_socio` | **NO DETERMINABLE EN ESTE RÉGIMEN** (P2 §2.c) | `[MEDIA]` en dirección · **no comprobable hoy** |
| **H-05** | E[`sens_estatus` \| ingreso medio-alto formal] **>** E[`sens_estatus` \| ingreso bajo informal] | `est_socio` × `segsoc` | **NO DETERMINABLE EN ESTE RÉGIMEN** | `[MEDIA]` · **no comprobable hoy** |
| **H-06** | E[`sens_estatus` \| joven urbano conectado] **>** E[`sens_estatus` \| resto urbano] | Edad (corte PENDIENTE) × `tam_loc`=1 × `conex_inte` | **NO DETERMINABLE EN ESTE RÉGIMEN** | `[HIPÓTESIS]` · **no comprobable hoy** |
| **H-07** | E[`deferencia` \| joven] **<** E[`deferencia` \| mayor] | `edad` (corte PENDIENTE) | ~~**NO DETERMINABLE**, cola de verificación **C-bis** declarada y no corrida (ADR-51 (c))~~ → **PROXY CON SUPUESTO DECLARADO (parcial)** — Latinobarómetro 2024 `P4NOIJ` ("Obediencia" entre cualidades a inculcar en los niños), México n=1200, C-bis corrida (ADR-51 (f), `forense/notas/2026-08-03-cbis-deferencia-externas.md`) | `[MEDIA]` · **forma PENDIENTE, no comprobable hoy contra este corte de edad** |
| **H-08** | E[`deferencia` \| `tam_loc` ∈ {3,4}] **>** E[`deferencia` \| `tam_loc`=1] | `tam_loc` | Ídem H-07 | `[MEDIA]` · **forma PENDIENTE, no comprobable hoy contra este eje** |
| **H-09** | E[`familismo_apoyo` \| informal, ingreso bajo] **>** E[`familismo_apoyo` \| formal, ingreso medio-alto] | `segsoc` × `est_socio` | **Reactivo directo** ENIF `P9_9_1..6` (familia vs. Estado vs. mercado) | `[MEDIA]` **(b)** |
| **H-10** | E[`familismo_apoyo` \| migración o remesas] **>** E[`familismo_apoyo` \| sin migración] | `residencia`; `remesas` (P041) | Ídem H-09 | `[HIPÓTESIS]` **(b)** — "diversificación" era lectura, no medición |
| **H-11** | E[`familismo_obligacion` \| informal, ingreso bajo] **>** E[`familismo_obligacion` \| formal, ingreso medio-alto] | `segsoc` × `est_socio` | **PROXY CON SUPUESTO DECLARADO** — ENUT 6.11/6.11a, carga de cuidado a nivel persona (ADR-51 (c), M2) | `[HIPÓTESIS]` **(b)** · **forma PENDIENTE y sin magnitud** |
| **H-12** | E[`exposicion_violencia` \| ingreso bajo] **>** E[`exposicion_violencia` \| ingreso alto] | `est_socio` × `tam_loc` | **Reactivo directo** ENVIPE `BP1_20`/`BP1_23`/`BP1_28` | `[MEDIA]` **(a)** · ⚠️ **malla truncada**: ENVIPE no tiene digital ni migración, y el ingreso solo entra como `ESTRATO` de área |

⚠️ **H-11 no rescata el check de ADR-30, y decirlo importa más que la hipótesis.** El check obligatorio exige el **contraste** apoyo/obligación, no la correlación: *"si el modelo no puede producir el caso en que la familia daña, el parámetro es adorno."* Ese contraste vive **dentro del hogar** —la hija cuidadora carga obligación mientras su hermano recibe apoyo, bajo el mismo techo— y cae exactamente en la dimensión que los tres ejes de hogar no resuelven (§1.1.A, P2 §3.b). **H-11 es falsable en dirección y no en el contraste que el check pide.** El hallazgo **PERSISTE**; es problema del modelo, no de la segmentación.

**Los cinco patrones que NO sobreviven a la traducción — listados, no borrados en silencio:**

| # | Patrón descartado | Motivo |
|---|---|---|
| **X-01** | Todo patrón cuya región sea la **élite A/B** (perfil 4): horizonte largo, radio "medio (burbuja privada)", violencia "media (amortiguada)", deferencia "recalibrada→baja", acceso "muy alto/global" | **La región no se observa.** Límite (i) de §1.1.C, verbatim de `revision §4`. Una hipótesis sobre una región que la semilla no captura no es falsable con dato público mexicano |
| **X-02** | `sens_estatus` **alta por "miedo a caer"** del perfil 3 | **El perfil 3 no es una región, es una trayectoria** (`revision §3`). No hay corte de atributos que lo defina en un transversal. Se traslada a la ruta de pseudo-panel de cohortes; no se conserva como condicional |
| **X-03** | La columna entera **Acceso digital** (bajo / medio / alto / muy alto por perfil) | **`acceso_digital` deja de ser parámetro: es el eje 5 del vector de atributos.** Una condicional sobre sí misma es circular (criterio C3, P2 §2.b). Pasa de hipótesis a **marginal que la reponderación debe reproducir**. ⚠️ Se pierde granularidad: la tabla lo graduaba en cuatro niveles por persona, ENIGH lo observa como **tenencia binaria del hogar** |
| **X-04** | Los **36 valores de `confianza_institucional`** (6 componentes × 6 perfiles) | **Nunca estuvieron poblados.** La tabla declaraba el vector y remitía a §1.3, que da porcentajes nacionales. No hay patrón relativo que traducir |
| **X-05** | "**Violencia: variable**" y "**Acceso: variable**" del perfil 6 | *"Variable"* no es un valor ordenado: no genera predicción relativa y por tanto no genera hipótesis falsable. Era una casilla que decía "no sabemos" con otra palabra |

⚠️ **La marca (b) sobrevive al cambio de esquema y viaja con las condicionales.** `familismo_apoyo` y `familismo_obligacion` se sostienen en escalas validadas en **muestras mexicano-americanas** (Sabogal, Lugo Steidel, Knight, Calzada, Zeiders) — H-09, H-10 y H-11 heredan la marca, igual que la heredaban las celdas de la tabla vieja (⚠️ Cambio 5 del v3.4). El esquema cambió; la deuda de procedencia no se saldó.

#### 1.1.F · El denominador nuevo, derivado del diseño

**Paso 1 — cuáles eran los 15 parámetros por perfil.** Derivado de la línea "Escalas" de `§1.1` del v3.4 y del desglose de `§6`, no de memoria:

1 `horizonte_temporal` · 2 `radio_confianza` · 3 `aversion_riesgo` · 4 `sens_estatus` · 5 `deferencia` · 6 `familismo_apoyo` · 7 `familismo_obligacion` · 8 `exposicion_violencia` · 9 **`acceso_digital`** · 10–15 `confianza_institucional` × **6 componentes** (seguridad-fuerzas armadas · educación · salud · electoral-partidos · justicia-policía · financiera, §1.3).

**Control aritmético contra §6:** el v1 tenía **9** parámetros (familismo único, confianza escalar). 9 + 5 (escalar → vector de 6) + 1 (familismo desdoblado) = **15**, y 15 × 6 perfiles = **90** — exactamente el `+36` y el `90` que §6 declara. ✔

⚠️ **Esto cierra un hallazgo abierto.** `forense/hallazgos.md` (31/jul/2026) registró que *"14 de los 15 parámetros por perfil quedan identificables por nombre; el 15º no tiene identidad legible en el archivo"* — el archivo era `milpa/procedencia.yaml`. **El 15º es `acceso_digital`**, legible en la línea "Escalas" y en la columna "Acceso" de la tabla del v3.4, ausente de `procedencia.yaml` porque **ningún coeficiente de generador lo multiplica** (§2.2). El hueco era del inventario, no del modelo.

**Paso 2 — de 15 parámetros a 14 condicionales.** `acceso_digital` **sale de la lista de parámetros**: bajo el reencuadre es el **eje 5 del vector de atributos** (§1.1.A). Un parámetro no puede ser una condicional sobre sí mismo — es el criterio C3 de P2 §2.b, el mismo que inhabilita los pares circulares del ajuste. **La salida no toca §2:** los nueve parámetros que los generadores multiplican son `confianza_institucional`, `radio_confianza`, `sens_estatus`, `aversion_riesgo`, `horizonte_temporal`, `familismo_apoyo`, `familismo_obligacion`, `exposicion_violencia` y `deferencia` (§2.2) — `acceso_digital` no está entre ellos.

> ### **D = 14 condicionales** = 8 escalares + 6 componentes de `confianza_institucional`

**Paso 3 — sobre qué malla.** Sobre los **seis ejes** de §1.1.A. **No se teclea un número de celdas**, y la razón es derivada, no cautela retórica (P2 §1.a):

- **Los cortes no existen.** Solo `tam_loc` (4 tramos) y `est_socio` (4 categorías) traen partición canónica verificada en P1. **Edad, acceso digital y migración no tienen partición canónica**, y la formalidad admite al menos dos operacionalizaciones (`segsoc` frente a `contrato`/`pres_*`). Fijar cortes aquí sería inventar la forma funcional que §1.1.B prohíbe.
- **El número de celdas no es el cuello de botella.** Partir la edad en cinco tramos en vez de tres no añade una sola cantidad identificable: lo que las celdas identifican depende de la forma de la condicional, no de cuántas haya. Con condicional lineal en los seis ejes serían 6 pendientes + 1 intercepto por condicional — **pero la linealidad es un supuesto declarado de P2, no un resultado**, y este documento no la adopta. **Por eso `D` cuenta condicionales, no cantidades estimables.**

**Paso 4 — cómo se relaciona con los 22 grados de libertad.** Los **22 g.l. reales del ajuste** (ADR-51: **7** de probabilidad + **15** coeficientes, corregidos desde el "29 = 14+15" de ADR-50) **no incluyen** las 14 condicionales. Bajo ADR-50 §(1) los 90 `params_base` estaban **exentos** del ajuste — "se miden de transversal". ADR-51 retira esa exención en bloque y la acota a la lista nombrada. La relación es de dependencia, no de suma:

> Si θ_k(x) se estima **de los mismos momentos** que β_gk, ambos entran **solo como producto**: β_gk → λβ_gk con θ_k → θ_k/λ deja los momentos idénticos. **El producto es identificable; los factores no** (P2 §2.b). Por eso el contador nuevo cuenta **condicionales MEDIDAS**, y no condicionales ajustadas: una condicional ajustada contra los mismos momentos no rompe la indeterminación, la esconde.

**Paso 5 — cuántas están medidas.** Estado por condicional (P2 §2.c, más M2/M3 de ADR-51 (c)):

| Estado | Condicionales | Cuenta |
|---|---|---|
| **MEDIDO·PARCIAL(x)** *(nuevo 3/ago/2026, ver clase sellada en `milpa/procedencia.yaml`)* | `confianza_institucional[salud]` (ENCIG `P11_1_3`, condicionada a edad) · `confianza_institucional[educación]` (ENCUCI `AP5_2_6`, formalidad×edad + marginales urbanización/ingreso/acceso digital) · `confianza_institucional[financiera]` (ENIF `P11_1_1`-`P11_1_5`, formalidad×edad + marginales urbanización/migración/ingreso) — `forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §4-5 · `confianza_institucional[seguridad-FFAA]` (ENVIPE `AP5_4_04/08/09/10`, por institución, condicionada a edad/dominio) · `confianza_institucional[justicia-policía]` (ENVIPE `AP5_4_01/02/03/05/06/07/11`, por institución, condicionada a edad/dominio) · `confianza_institucional[electoral-partidos]` (ENCUCI `AP5_2_5`/`AP5_3_6/7/8`, por ítem, condicionada a formalidad×edad/dominio) — `forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md` §3-5 · `radio_confianza` (ENCUCI `AP5_1_1/2/3`, por ítem, condicionada a formalidad×edad + marginal dominio) · `familismo_apoyo` (ENIF `P9_9_1..6`, por ítem — `p9_9_4` opera el constructo, condicionada a formalidad×edad + marginal urbanización) — `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1-5 | ~~**6**~~ **8** |
| ⚠️ **Reactivo declarado retirado, pendiente de localizar** *(PROPUESTA de clase, no sellada — decisión de mesa, ver nota)* | `exposicion_violencia` — su reactivo reportado (ENVIPE `BP1_20/23/28`) fue **retirado**: mide conducta de denuncia condicionada a victimización, no exposición a violencia (`PR #57`, `forense/hitoE-campana-medicion-v2_0.md` §15). Ya no pertenece a "reactivo directo reportado, sin medir" (el reactivo que la justificaba ahí dejó de sostenerse) y no es evidente que pertenezca a "sin reactivo o no determinable" (esa clase agrupa límites de régimen; aquí el reactivo está pendiente de localizar, no descartado) | **1** |
| **Proxy declarado, pendiente de medición** | `horizonte_temporal` (ENIF `P4_10`, ⚠️ falla C3) · `familismo_obligacion` (ENUT 6.11/6.11a, M2) · `deferencia` (M3, Latinobarómetro `P4NOIJ`, ADR-51 (f)) | **3** |
| **Sin reactivo o no determinable** | `sens_estatus` · `aversion_riesgo` | **2** |
| | | **14** ✔ *(8+1+3+2)* |
| **MEDIDAS** | los seis componentes de `confianza_institucional` (arriba) más `radio_confianza` y `familismo_apoyo` — distribución condicional empírica, no media puntual, sobre un subconjunto declarado de `x` en los ocho casos (nunca los seis ejes a la vez); los tres de la ola 2 medidos **por institución**, `radio_confianza`/`familismo_apoyo` medidos **por ítem**, ninguno como escalar único (`forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.0, §4-5). Marca C3 declarada, viaja con el número: `familismo_apoyo` no identifica `G5`; `radio_confianza` no identifica `cooperacion.confianza.puente_personal` (misma nota, §1.0) | ~~**6**~~ **8** |

> ## 📊 **Condicionales medidas sobre atributos: ~~6~~ 8 de 14**
> *(Corregido 4/ago/2026 — `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §5, Fase B posiciones 5-6 midió `radio_confianza` (ENCUCI) y `familismo_apoyo` (ENIF). `4 de 144` sigue congelado y no se mueve — ver §6.1. **Nota de reparto, no sellada:** `exposicion_violencia` sale de "reactivo directo reportado, sin medir" porque `PR #57` retiró su reactivo (`hitoE` §15); dónde cae —clase nueva o "no determinable"— queda propuesto arriba y pendiente de mesa, no decidido aquí.)*
>
> **`D`=14 es derivado del diseño de §1.1, nunca estimado.** Su aritmética completa está arriba, pasos 1–5. Si alguien mueve `D`, tiene que mover uno de esos cinco pasos y decir cuál.

**Qué le pasa al `144`.** 144 = 90 `params_base` + 15 coeficientes + 39 probabilidades. Los **90 salen del conteo de números** y son sustituidos por **14 condicionales de dimensión indeterminada** — indeterminada porque la forma funcional está PENDIENTE, no porque no se haya contado. Quedan **54 números enumerables** (15 + 39), de los cuales **4 son `MEDIDO`**. ⚠️ **Este documento NO mueve el titular `4 de 144`**: sigue **congelado** por decisión de mesa (`forense/hallazgos.md`, 31/jul/2026), y elegir entre congelarlo como cifra histórica o retirarlo del titular es una decisión que `revision §6.3` deja abierta y que este encargo no implementa. Se deriva la aritmética y se deja la decisión donde está.

**Qué le pasa a la deuda de los 90 parámetros de dispersión** (§6). Bajo la tabla, ADR-28.d exigía 90 parámetros de dispersión que no existían en archivo — de ahí el "conteo real es 234". Bajo condicionales, **la dispersión es parte de la especificación de θ_k** (§1.1.B, propiedad 1): no son 90 números aparte, son **14 familias de distribución sin declarar**. La deuda no se salda —sigue sin poder correr el check de 28.d—, pero **cambia de tamaño y de forma, y es enumerable**.

### 1.2 Las condicionales son distribuciones *(ADR-28.d, releído sobre atributos)*

Cada condicional θ_k( · | x ) de §1.1.B especifica **una distribución, no un valor**. Dos agentes **con el mismo vector de atributos** deben poder diferir.

*Motivación, sin cambio respecto del v3.4 salvo la unidad:* con valores puntuales el modelo produce clases de mexicano — la forma estadística del esencialismo que este corpus combate, y la que el validador no atrapa porque revisa estructura, no dispersión. Bajo perfiles el riesgo eran seis clases; bajo celdas de atributos sin dispersión sería el mismo esencialismo con más casillas.

**Check de compilación:** una configuración donde la varianza **intra-celda de atributos** sea cero se rechaza. *(Antes decía "intraperfil"; es el mismo check sobre la unidad nueva.)*

⚠️ **El check sigue sin poder correr**, y ahora se sabe por qué con precisión: exige que cada una de las **14 condicionales** declare familia de distribución y dispersión con clase de procedencia, y **ninguna la declara hoy** (§1.1.F).

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

⚠️ **En el v4.0 los seis componentes son seis condicionales**, no seis columnas de una tabla — son 6 de los 14 de `D` (§1.1.F). Los porcentajes de arriba son **nacionales**, no valores por región de atributos: siguen sin poblar, igual que en el v3.4. Lo que cambió es que ahora hay una ruta nombrada para poblarlos —ENCIG batería XI, co-observada con `tramite.mordida.discrecional` en el mismo instrumento— y que por eso `confianza_institucional` sale de la clase "inidentificable con cualquier número de momentos" y pasa a **IDENTIFICADO · TRUNCADO** (ADR-51 (d), que cierra `D-12` con esa derivación). **Truncado** porque ENCIG no observa ingreso en ningún régimen y su universo excluye por diseño toda localidad de menos de 100 000 habitantes: los componentes se pueden condicionar sobre edad, no sobre ingreso ni sobre ruralidad.

### 1.4 Modificadores transversales

Género, edad, región, urbanización, escolaridad, religiosidad, exposición internacional.

⚠️ **Marca de procedencia obligatoria** *(ADR-29)*: los modificadores **marianismo**, **machismo/caballerismo** y **simpatía** son constructos `Media` con procedencia **(b)** — muestras mexicano-americanas. La marca viaja con el modificador a **cualquier** dominio donde se use, no solo a §3.10. En el v1 la marca vivía en una nota al pie de comunicación y se perdía en §1, §3.4 y §3.6.

### 1.5 Diferenciales por atributo: admisibles solo con mecanismo *(ADR-28.c, releído sobre atributos)*

Un diferencial **por atributo** no es automáticamente esencialista. Un vendedor informal en vía pública está más expuesto a extorsión que un empleado formal del mismo municipio: eso es estructura, no cultura.

Lo inadmisible es el **desplazamiento constante por atributo sin mecanismo nombrado**. Regla, con la unidad nueva:

> Un diferencial de θ_k por atributo es admisible si **(a)** el mecanismo estructural está declarado con fuente, y **(b)** se cumple la **condición de dominancia**: un agente **informal de ingreso bajo** en celda de baja violencia debe terminar por debajo de un agente **formal de ingreso medio-alto** en celda de alta violencia.

**Si el orden no se invierte, el diferencial domina al entorno y el parámetro es un rasgo.** Se rechaza en compilación.

⚠️ *Antes decía "un agente del perfil 2" y "un agente del perfil 1". El enunciado es el mismo test; lo que cambia es que ahora nombra los atributos que el perfil abreviaba — y así el check es **ejecutable sin leer un número de perfil**, como exige la prohibición de §1.1.D.*

---

### 1.6 Las 10 reglas que citaban perfil: traducción a atributos

Diez de las 49 reglas de §3.B citan número de perfil en su `SI`. Derivadas con la receta canónica —`grep -n '^- \*\*SI\*\*' <modelo> | grep "perfil"` → 10 líneas—, re-corrida sobre este archivo antes de editarlo, con el mismo resultado que la línea del 31/jul/2026 de `forense/hallazgos.md`: las menciones son `perfiles 2,3,6` (×2), `perfiles 1,4`, `perfiles 2,3,5`, `perfil 5` solo (×2), `perfil 2` con modificador rural/sur, `perfiles 2,3`, `perfil 1 con hijos`, `perfil 1`. **Cuatro ejes, no uno.**

**En las diez, el conjunto de perfiles era redundante con una condición que el `SI` ya enunciaba.** Por eso la traducción **no cambia ninguna predicción**: sustituye una abreviatura por lo que abreviaba.

| Regla · id | Conjunto viejo | Condición nueva (atributos de §1.1.A) | ¿Cambia la predicción? |
|---|---|---|---|
| `R1.1` · `dinero.ahorro.volatilidad_horizonte_corto` | perfiles 2, 3, 6 | `segsoc`=2 **∨** sin `contrato`/`pres_*` en `trabajos` — el `SI` ya decía *"ingreso volátil/informal"* | **No.** El conjunto era la formalidad con otro nombre |
| `R1.2` · `dinero.planeacion.formal_estable` | perfiles 1, 4 | `segsoc`=1 **∧** `contrato` formal **∧** `pres_8` (SAR/AFORE) — el `SI` ya decía *"empleo formal e ingreso estable"* | **No.** ⚠️ La mitad "élite" del conjunto viejo (perfil 4) era región no observada; el `SI` nunca dependió de ella |
| `R1.4` · `dinero.consumo.estatus_mediado_por_credito` | perfiles 2, 3, 5 | (`segsoc`=2 **∧** `est_socio` ∈ {1,2}) **∨** (`edad` joven **∧** `tam_loc`=1 **∧** `conex_inte`=1) | **No.** Unión de dos regiones = unión de los tres perfiles. ⚠️ **Corte de `edad` PENDIENTE** |
| `R2.1` · `trabajo.jerarquia.deferencia_iniciativa_suprimida` | perfil 2 (+ modificador rural/sur) | `segsoc`=2 **∧** `tam_loc` ∈ {3,4} | **No.** ⚠️ El modificador **"sur"** NO se traduce: la región geográfica no está en el vector de seis ejes y P1 no la inventarió. Se conserva literal como modificador (§1.4) |
| `R2.4` · `trabajo.rotacion.joven_urbano_sin_culpa` | perfil 5 | `edad` joven **∧** `tam_loc`=1 — el `SI` ya decía *"joven urbano"* | **No.** ⚠️ Corte de `edad` PENDIENTE |
| `R4.1` · `salud.atencion.leve_sin_imss` | perfiles 2, 3 | `segsoc`=2 — el `SI` ya decía *"no hay IMSS"* | **No.** Es la traducción más literal de las diez: `segsoc` **es** derechohabiencia |
| `R4.5` · `salud.consumo.sellos_precio_similar` | perfil 1 **con hijos** | `segsoc`=1 **∧** `est_socio` ∈ {3,4} **∧** hogar con menores | **No.** ⚠️ **Eje de composición de hogar NO VERIFICADO** — ver el aviso de abajo |
| `R5.1` · `familia.seguro.volatilidad_ausencia_estado` | perfiles 2, 3, 6 | `segsoc`=2 **∨** `residencia` ∈ {EUA, Otro país} **∨** hogar con `remesas` (P041) — el `SI` ya decía *"ingreso volátil / ausencia de Estado"* | **No** |
| `R5.4` · `familia.cortejo.urbano_joven_apps` | perfil 5 | `edad` joven **∧** `tam_loc`=1 **∧** `conex_inte`=1 — el `SI` ya decía *"urbano-joven-conectado"* | **No.** ⚠️ Corte de `edad` PENDIENTE |
| `R9.4` · `informacion.escuela.miedo_a_caer_clase_media` | perfil 1 | `segsoc`=1 **∧** `est_socio`=3 (Medio alto) | **No.** ⚠️ *"con miedo a caer"* permanece como condición subjetiva declarada y **no observada** — no era el número de perfil quien la aportaba |

⚠️ **AVISO — el cuarto eje no está verificado, y hay que decirlo antes de que alguien lo use.** El reencuadre necesita **cuatro** ejes para las diez reglas: formalidad, edad × urbano, migración y **composición de hogar** (`forense/hallazgos.md`, 31/jul/2026). Los tres primeros están en el vector de §1.1.A con variable, módulo y llave verificados por P1. **El cuarto no está**: P1 inventarió seis ejes y la composición de hogar no es ninguno de ellos. La variable natural existe —`poblacion.parentesco`, que P1 §2 cita solo de paso al descartar `edad_jefe` como redundante— pero **P1 no la verificó como eje**, y este acto no abre descriptores. La condición de `R4.5` queda por tanto **declarada con variable PENDIENTE DE VERIFICACIÓN**, no cerrada. Es hueco de premisa, no licencia para inventarla.

**Ninguna otra regla de §3 cambia.** Las 39 restantes no citaban perfil y su texto no se toca. Los tiers, los ids y el perímetro de 27 del Hito D quedan exactamente como estaban.

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

⚠️ **G1a: homogeneidad de pendientes DECLARADA, no medida (ADR-49, D3).** El `−0.60` de `confianza_institucional[dominio]` se aplica al componente que el dominio seleccione — eso **asume una elasticidad común a los seis componentes** del vector de ADR-28.b. Es un supuesto declarado, no una medición; **no se desdobla en seis `ASIGNADO` donde hoy hay uno.** `G4` no comparte este problema: usa `confianza_institucional[justicia]`, componente nombrado, sin selección variable. **Pre-registro:** la salida de `CAL-CONF` Fase A (los seis niveles de confianza institucional por perfil) es lo que revisita el supuesto — si la dispersión entre componentes es la que ADR-28.b sostiene (Marina 89% vs. partidos 23.9%), la pendiente común queda implausible y el desdoblamiento pasa a justificado. Condición escrita **antes** de tener el dato. ~~**No cierra `D-12`** (`forense/hallazgos-congelados-2026-07-30.yaml`): D-12 es la operacionalización única de Hito E que derogaría ADR-28.b sin nombrarlo — sigue abierta, es otro asunto.~~ *(Corregido 3/ago/2026 — redacción heredada, no contradicción sustantiva. `D-12` sí cierra hoy, pero por una causa distinta de la que esta nota discute: `gobernanza` ADR-51 (d) lo cierra porque el reencuadre perfiles→atributos elimina la tabla que forzaba a tratar `confianza_institucional` como escalar — esa era la causa original de `D-12`. La pregunta que esta nota deja abierta —si el `−0.60` de G1a debe desdoblarse en seis `ASIGNADO` nombrados, como hace `G4`— nunca fue literalmente `D-12`: es una pregunta adyacente sobre la homogeneidad de pendientes, distinta de si el vector de 6 componentes sobrevive. `forense/hitoE-campana-medicion-v2_0.md` §12.2 señaló esta misma tensión sin resolverla ("esta adenda no la resuelve — no edita `canon/`"); esta sesión sí puede tocar `canon/` y la concilia aquí. **La pregunta de homogeneidad de pendientes sigue sin decidir** — el pre-registro de este párrafo sigue vigente y esperando la salida de `CAL-CONF` Fase A por dominio-perfil, que no es lo mismo que la Fase B por atributos que ya corrió (`forense/notas/2026-08-03-cal-conf-faseb-medicion.md`).)* **Enmienda in situ, 4/ago/2026 — el pre-registro corrió, y su resultado es que no puede llegar en este régimen.** `hitoE §14.3` posición 8 (P4) llevó este pre-registro a paso 1: verificar si un solo instrumento trae los seis componentes de `confianza_institucional` en la misma batería, condición necesaria para medir la dispersión *entre* componentes sin fabricar la conjunta que §1.1.C prohíbe. `PR #58` (`forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md`) corrió ese chequeo contra la batería XI de ENCIG 2021 (25 ítems, sección "Confianza en instituciones"): **CUBIERTO** salud, educación, seguridad-FFAA, justicia-policía y electoral-partidos — **NO CUBIERTO** financiera (ningún ítem de los 25; el candidato más cercano por nombre, "Empresarios", es confianza en un actor social, no en una institución financiera). Ningún instrumento del corpus trae los seis en una sola batería. **Resultado, no tarea pendiente:** la dispersión entre componentes no es estimable en este régimen sin fabricar la conjunta prohibida — el dato que este pre-registro esperaba no puede llegar por esta vía. **Esto NO decide si `G1a` se desdobla en seis `ASIGNADO` nombrados** — esa pregunta no se resuelve, **vuelve a mesa**: el pre-registro suponía que el dato revisitaría el supuesto de homogeneidad; lo que se verificó es que el dato no puede producirse en este régimen, así que mesa decide con el supuesto declarado intacto, no con evidencia nueva. Ver cierre de fila en `hitoE §14.3` posición 8 (adenda fechada).*

⚠️ **`familismo_apoyo` se conserva en G3** *(corrección a la propuesta original de ADR-30)*. Ahí el mecanismo es **pooling económico bajo volatilidad** — la tanda, el préstamo del primo, la corresidencia. `§3.1` enruta el ahorro informal por G3; retirarlo dejaría esa regla sin canal. No hay doble conteo: en G3 es pooling ante volatilidad, en G5 es seguro ante Estado ausente.

**`unico_calibrable_hoy` se retira (ADR-49, D1).** El campo asumía que el panel rotativo de la ENOE permite estimar la elasticidad `G3 → horizonte_temporal`; `forense/hallazgos.md` (31/jul/2026) encontró que ningún cuestionario de ENOE/ENOEN trae conducta financiera (ahorro, crédito, deuda, planeación, expectativas) — la premisa muere a nivel de reactivo, no de tema. Lo que sí sobrevive, **sin adjetivo de unicidad**, es una propiedad del instrumento: el panel rotativo trimestral de la ENOE sigue al mismo hogar cinco trimestres, cruzando formal↔informal. Eso no identifica un ritmo (una elasticidad) hoy. ⚠️ No confundir con los **seis valores de `horizonte_temporal` por perfil** (`params_base`, ORDINAL→CARDINAL) — esos nunca dependieron de ENOE y no cambian con este retiro.

---

## 3 · El motor de reglas

### 3.A Los dos niveles de disparadores *(ADR-26)*

> ⚠️ *Renumerado en v2.1. Antes era «§3.1», que colisionaba con el dominio §3.1 (Dinero). Los dominios conservan su número; las secciones meta pasan a letra.*

El motor evalúa contra la tupla **`(perfil, params, d_global, d_dominio)`**.

**Nivel 1 — siete disparadores globales**, evaluados en todos los dominios:
`formal / informal` · `quién observa` · `sanción creíble` · `puente personal` · `urgencia` · `cobertura formal` · `vector de atributos` (**el vector de atributos observables del agente, §1.1.A** — corregido 3/ago/2026, traducción ejecutada de §1.1.D: decía `segmento`, "cuál de los seis perfiles", corregido del v1 que decía "ocho". **Sin cambio predictivo**: ninguna de las 49 reglas de §3.B condiciona su `SI` sobre el valor de este disparador directamente — leen los atributos individuales del vector, ya traducidos en §1.6 — así que sustituir la etiqueta por lo que el motor ya lee no mueve ninguna salida, misma disciplina que §1.6).

**Nivel 2 — 42 palancas de dominio**, declaradas en la cabecera de cada `rules/<dominio>.yaml` y transcritas literalmente de la línea con que el modelo cierra cada dominio.

⚠️ **Entran como booleanos de contexto, no como parámetros continuos** *(adenda a ADR-26)*. En el modelo son estados —`hay registro / no hay registro`, `riesgo fiscal percibido sí / no`—, no magnitudes. Tratarlas como parámetros añadiría ~42 números que habría que calibrar sin dato.

**Por qué importa:** el gate de Fase 1 (ADR-25) exige que apagar `riesgo_fiscal_percibido` borre la diferencia OXXO/CoDi. Ese campo vive en `§3.3` (dominio de trámite) y **no existe** entre los siete globales. Sin el nivel 2, el go/no-go del programa se apoya en una variable que el motor nunca evaluaría.

### 3.B Las 49 reglas SI-ENTONCES

> ⚠️ *Eran 42. En v2.1 la regla de transferencia directa de §3.7 **se parte en dos** (conf.07), porque empaquetaba una afirmación `[FUERTE]` y una `[HIPÓTESIS]` bajo un solo tier. **El perímetro de reglas `[FUERTE]` no cambia: sigue siendo 20.***

*Transcritas literalmente del v1 el 27/jul/2026, no reescritas de memoria. Las cuatro ediciones aprobadas van marcadas en línea con `*(v2: …)*`.*

### 3.1 Dinero, ahorro, crédito y consumo

- **SI** el ingreso es volátil/informal (`segsoc`=2 **∨** sin `contrato`/`pres_*`) **ENTONCES** horizonte corto, ahorro informal (tanda, "guardado en casa"), foco en emergencia — PORQUE G3 (volatilidad) + escasez — `[FUERTE]` **(a)**. 🚫 **DOMINIO AGRÍCOLA: INEJECUTABLE** *(v3.2 — veredicto `D` de `hitoD-R1.1`, 28/jul/2026)*. El falsador pre-registrado —productores de temporal con compromiso formal voluntario de horizonte largo— **no puede correrse**: el instrumento que cubre a esa población, el Seguro Agrícola Catastrófico, **no puede ser contratado por el productor** (SADER, textual; aporta ~2.5% de la prima), y los Fondos de Aseguramiento, que sí son voluntarios, viven en riego y gran extensión (62%/66% en Sonora-Sinaloa-Tamaulipas). ⚠️ **La ausencia de seguro voluntario en temporal NO cuenta como apoyo a esta regla:** está confundida con exclusión de mercado. **La regla sale igual que entró — no ganó ni perdió información.** · **id:** `dinero.ahorro.volatilidad_horizonte_corto`
- **SI** hay empleo formal e ingreso estable (`segsoc`=1 **∧** `contrato` **∧** `pres_8`) **ENTONCES** planeación larga: afore, seguro, hipoteca — PORQUE **el ingreso estable baja el costo esperado de comprometerse a un instrumento de horizonte largo**: cae la probabilidad de incumplir y perder lo aportado — `[FUERTE]` **(a)**. *(v3.1 — **D-01**: el `PORQUE` decía *"la estabilidad **permite** horizonte"*. **Permitir es una capacidad y una capacidad no se refuta**: si el formal estable no planea, siempre se puede decir que podía. El `ENTONCES` es conductual, así que se predecía conducta y se justificaba con capacidad. El `PORQUE` nuevo nombra un **mecanismo con dirección comprobable**. ⚠️ **Si el falsador R1.2 sale `A`, la regla no se rompe entera: se parte** — sobrevive *"la estabilidad permite"* como capacidad `[FUERTE]`, y cae *"produce"*, que es la que el motor usa para enrutar perfiles 1 y 4.)* · **id:** `dinero.planeacion.formal_estable`
- **SI** se ofrece un producto financiero por un **canal de confianza personal** (recomendación, no institución fría) **ENTONCES** sube la adopción; sin puente, desconfía — PORQUE G1 — `[FUERTE]`. · **id:** `dinero.ahorro.informal_sin_puente` **+** `dinero.ahorro.con_puente_y_respaldo` ⚠️ *dos ids ya existentes en `procedencia.yaml` para una sola regla — anomalía, ver `forense/hallazgos.md`*
- **SI** hay movilidad real bloqueada + presión de estatus ((`segsoc`=2 **∧** `est_socio` ∈ {1,2}) **∨** (`edad` joven **∧** `tam_loc`=1 **∧** `conex_inte`=1)) **ENTONCES** consumo compensatorio/aspiracional (marca, logo, mensualidades), aun apalancado — PORQUE G2 — `[FUERTE como correlación]`. *(v2: sin cambio de tier. V1 forense lo rompió "como driver decisivo aislado" — **afirmación distinta** de "fuerte como correlación" — y **omitió el perfil 5**. Hito 2.)* · **id:** `dinero.consumo.estatus_mediado_por_credito`
- **SI** existe seguro de depósito visible o marca confiable **ENTONCES** se atenúa la aversión (la fintech con respaldo penetra donde el banco tradicional no) — PORQUE G1 + diseño — `[MEDIA]`. · **id:** `dinero.ahorro.seguro_deposito_atenua_aversion`
- **SI** el hogar es popular/informal y el crédito es de **efectivo o tarjeta de alto CAT** **ENTONCES** paga sobreprecios notables **hasta un techo**: la mora regulada se estabiliza en **15–20%**, viable solo con **CAT de tres dígitos y castigo agresivo** — PORQUE el precio absorbe el error de predicción del scoring, no porque el scoring falle — `[MEDIA]` **(a)**, métrica **AUDITADA** (CNBV). *(v2.5 — **P-04 del barrido**. La regla *"bajo ingreso ≠ baja disposición a pagar"* vivía en el motor **sin su límite**, y un enunciado sin techo no se puede romper por arriba. Base: **ENSAFI 2023** — solo **27.3%** de los endeudados se atrasó, es decir **72.7% al corriente** pese a ingresos bajos; pago mensual máximo sostenible **declarado** de 2,777 pesos. CAT de **80–97%** en BanCoppel son pagados por el segmento. ⚠️ **Falsador ya pre-registrado por el forense V4, con umbral:** *si el IMOR de consumo del sector popular superara **~25–30% sostenido** SIN que el CAT pudiera subir más —por techo regulatorio o competencia—, el modelo «utilidad > confianza» empezaría a romperse **por el lado del cliente**.* Es el umbral mejor especificado del corpus.)* · **id:** `dinero.credito.scoring_alternativo`
- **SI** el producto de crédito combina **baja fricción de acceso** **Y** tasa usuraria (CAT >100%) **Y** reporte crediticio incompleto o invisible (BNPL) **ENTONCES** la adopción produce **daño downstream** — concentración de mora en productos no garantizados, quejas de cobranza — PORQUE la advertencia es **condicional a la estructura, no a la conducta**: la baja fricción **sola** no daña — `[MEDIA]` **(a)**. *(v2.5 — **P-05 del barrido**, con la tier que V5 le asignó literalmente: *"una ADVERTENCIA downstream, de fuerza MEDIA"*. Es MEDIA y no más porque **el costo observado se confunde** con el diseño de precio predatorio y con el choque de ingreso — no está aislado. **Se había retirado junto con la extensión a crédito del cambio 11, cuando aplicaba justo a ese lado.** ⚠️ **La lectura peligrosa es la inversa:** leerla como *"la baja fricción daña"* culpa al diseño accesible y borra las dos condiciones estructurales que la activan.)* · **id:** `dinero.credito.baja_friccion_usura_dano_downstream`
- *Disparadores que voltean:* formalización del empleo; default de inscripción automática; presencia de un puente personal; garantía/seguro explícito.

### 3.2 Trabajo y carrera

- **SI** hay jerarquía tradicional/empresa familiar (`segsoc`=2 **∧** `tam_loc` ∈ {3,4}; modificador *sur* sin traducir, §1.6) **ENTONCES** deferencia hacia arriba, iniciativa suprimida, el "sí" que significa "probablemente" — PORQUE G6 + G1 — `[FUERTE]`. · **id:** `trabajo.jerarquia.deferencia_iniciativa_suprimida`
- **SI** el liderazgo es **benévolo** (provee, protege, cuida) **ENTONCES** lealtad y satisfacción altas; **SI** es autoritario no-benévolo **ENTONCES** peor desempeño — PORQUE solo el paternalismo benévolo legitima — `[MEDIA-FUERTE]`. · **id:** `trabajo.liderazgo.benevolencia_legitima`
- **SI** hay prestaciones formales (IMSS, Infonavit) **ENTONCES** pesan más que el salario nominal (la formalidad es beneficio de estatus) — PORQUE G3 (seguridad escasa) — `[MEDIA]`. · **id:** `trabajo.prestaciones.formalidad_pesa_mas_que_salario`
- **SI** el trabajador es joven urbano (`edad` joven, corte PENDIENTE **∧** `tam_loc`=1) **ENTONCES** cambia de empleo sin culpa (no es deslealtad) y exige que las decisiones se justifiquen — PORQUE recalibración de G6 — `[MEDIA]`. · **id:** `trabajo.rotacion.joven_urbano_sin_culpa`
- *Disparadores:* benevolencia percibida del jefe; formalidad del contrato; canal privado/anónimo para expresar desacuerdo.

### 3.3 Autoridad, trámite y relación con el Estado

- **SI** el trámite es presencial con funcionario discrecional y sin registro **ENTONCES** alta probabilidad de mordida — PORQUE trampa social (G1): cada quien paga porque supone que los demás pagan — `[FUERTE]` **(a)**. ⚠️ *(v2.2: **`trampa social` no tiene entrada propia en el glosario** — solo existe ahí como refutación del mito "la mordida es inherente a lo mexicano", con base en el equilibrio de Bardhan **(c)** y ENCIG 2023 **(a)**. El tier `[FUERTE]` se sostiene por el dato, no por la etiqueta. Ver `glosario §16`: **al pre-registrar su falsador, escribirlo contra el dato —¿baja la mordida al digitalizar y hacer registrable al funcionario?— no contra el nombre del mecanismo.**)* · **id:** `tramite.mordida.discrecional`
- **SI** el trámite se digitaliza / hay testigos / el funcionario es registrable **ENTONCES** la mordida baja — PORQUE se rompe la trampa — `[FUERTE]`. · **id:** `tramite.mordida.con_registro`
- **SI** una norma se percibe como inútil o extractiva y la sanción es improbable **ENTONCES** evasión ("hacerse guaje") — PORQUE cálculo ante institución de baja calidad — `[MEDIA]`. *(Distinguir evasión de subsistencia [informalidad] de evasión por cinismo de clase alta.)* · **id:** `tramite.evasion.norma_inutil_sancion_improbable`
- **SI** se ofrece un servicio de gobierno digital de forma **coercitiva y con riesgo fiscal** (tipo CoDi/SAT) **ENTONCES** se rechaza; **SI** es útil y sin amenaza (tipo SPEI) **ENTONCES** se adopta — PORQUE la confianza institucional no predice adopción; la utilidad sí — `[MEDIA-FUERTE]`. *(v2: **alcance acotado a gobierno digital**. Su extensión a crédito en §7 del v1 se retira — Hito 2: la regla migró de dominio sin autorización.)* · **id:** `tramite.gobierno_digital.coercitivo` **+** `tramite.gobierno_digital.util_sin_coercion` ⚠️ *dos ids ya existentes en `procedencia.yaml` para una sola regla — anomalía, ver `forense/hallazgos.md`*
- *Disparadores:* discrecionalidad vs. registro; utilidad vs. coerción; riesgo fiscal percibido.

### 3.4 Salud y cuerpo

- **SI** el padecimiento es leve-moderado y no hay IMSS (`segsoc`=2) **ENTONCES** farmacia con consultorio o automedicación — PORQUE **la conducta responde a la estructura de acceso en tres dimensiones — costo, tiempo y trato — y no a una preferencia**: si las tres mejoran, la conducta debe moverse — `[FUERTE]` **(a)**. *(v3.1 — **D-04**: el `PORQUE` decía *"adaptación racional (costo/tiempo/trato)"* sin acotar, y **sin acotar explica cualquier resultado**: siempre se puede inventar un incentivo que haga óptima cualquier conducta. Es el riesgo inverso al culturalismo y el que este corpus tiene más cerca. **La acotación es la prueba:** mejora documentada de acceso → movimiento de conducta. ⚠️ **El trato es la dimensión que no mejora al abrir una clínica** — si el uso no cae, puede ser el trato, que sigue siendo adaptación racional. **Sin medir trato no se distingue refutación de re-atribución.**)* · **id:** `salud.atencion.leve_sin_imss`
- **SI** el síntoma es grave o crónico complejo **ENTONCES** busca el sistema público pese a la espera — PORQUE la complejidad excede al consultorio — `[MEDIA]`. · **id:** `salud.atencion.grave`
- **SI** es hombre trabajador sin permiso laboral (modificador machista) **ENTONCES** pospone el chequeo hasta el síntoma grave — PORQUE machismo + costo de oportunidad del tiempo — `[FUERTE]`. *(v2: driver **machismo marcado (b)** — muestra mexicano-americana. El patrón conductual tiene dato mexicano; la atribución causal no. ADR-29.)* · **id:** `salud.prevencion.hombre_sin_permiso`
- **SI** hay desabasto + gasto de bolsillo alto **ENTONCES** abandono o intermitencia del tratamiento crónico; **SI** hay familia cuidadora + medicamento surtido **ENTONCES** mayor adherencia — PORQUE estructura + G5 — `[FUERTE / MEDIA]`. · **id:** `salud.adherencia.desabasto_vs_cuidadora`
- **SI** el producto tiene sellos y hay alternativa de **precio similar** (`segsoc`=1 **∧** `est_socio` ∈ {3,4} **∧** hogar con menores — variable PENDIENTE DE VERIFICACIÓN, §1.6) **ENTONCES** elige el de menos sellos; **SI** el hogar es de bajo ingreso sin sustituto barato **ENTONCES** compra igual — PORQUE el precio domina sobre la información — `[MEDIA]`. · **id:** `salud.consumo.sellos_precio_similar`
- *Disparadores:* gravedad; tener o no seguridad social; desabasto; precio relativo; permiso laboral; alcoholímetro/sanción (para alcohol).

### 3.5 Familia y pareja

- **SI** hay ingreso volátil / ausencia de Estado (`segsoc`=2 **∨** `residencia` ∈ {EUA, Otro país} **∨** hogar con `remesas` P041) **ENTONCES** la familia opera como seguro (corresidencia, pooling, remesas) — PORQUE G5 — `[FUERTE]`. · **id:** `familia.seguro.volatilidad_ausencia_estado`
- **SI** se trata de cuidado (mayores, niños, enfermos) **ENTONCES** recae sobre mujeres 40+ (hijas/nueras) — PORQUE estructura + guion marianista, no "cultura del cuidado" — `[FUERTE]`. *(v2.2: driver **marianismo marcado (b)** — constructo `Media` validado en cohorte HCHS/SOL, hispana en EE.UU. **La carga de cuidado está medida en México (a); la atribución al guion, no.** Mismo defecto que el v2 corrigió en §3.4 y aquí pasó inadvertido.)* · **id:** `familia.cuidado.recae_mujeres_40mas`
- **SI** hay baja garantía institucional del matrimonio **ENTONCES** la unión libre es opción racional (no "unión fallida") — PORQUE evita costos ante baja garantía — `[MEDIA]`. · **id:** `familia.union.baja_garantia_institucional`
- **SI** el cortejo es urbano-joven-conectado (`edad` joven, corte PENDIENTE **∧** `tam_loc`=1 **∧** `conex_inte`=1) **ENTONCES** apps + lógica de mercado, pero los guiones de género se reconfiguran **desigual** (actitud rápida, conducta lenta) — PORQUE cohorte + exposición — `[MEDIA / HIPÓTESIS]`. · **id:** `familia.cortejo.urbano_joven_apps`
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
- **SI** el hogar es clase media con miedo a caer (`segsoc`=1 **∧** `est_socio`=3; *miedo a caer* no observado) **ENTONCES** escuela privada como seguro anticaída + credencial; **SI** es popular **ENTONCES** pública con aspiración universitaria alta — PORQUE G2 + cálculo de retorno — `[MEDIA]`. · **id:** `informacion.escuela.miedo_a_caer_clase_media`
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

Orden de aplicación: **vector de atributos** → parámetros (condicionales sobre ese vector) → generadores → disparadores globales → disparadores de dominio → regla → salida con tier.

⚠️ *v4.0: el primer paso decía **"segmento"**, y bajo la tabla de perfiles eso significaba asignar el agente a una de seis casillas. Bajo el reencuadre el agente **ya trae** su vector de atributos desde la síntesis (§1.1.C) y no hay paso de asignación: se lee el vector, no se elige una casilla. El resto del orden no cambia.*

⚠️ ~~**Este paso no está cerrado y no se cierra aquí.** El disparador global 7 de `§3.A` sigue siendo `segmento` = *"cuál de los seis perfiles"*, en contradicción con la prohibición de §1.1.D. Ver el DETENTE declarado ahí: traducirlo es decisión de mesa, no de este acto.~~ **Cerrado 3/ago/2026.** El disparador global 7 de `§3.A` ya es `vector de atributos`, sin cambio predictivo. Ver §1.1.D y §3.A.

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

⚠️ **DEUDA CON REQUISITO DE SALIDA — la dispersión.** ADR-28.d obliga a que cada parámetro sea una **distribución**, y §1.2 rechaza en compilación toda configuración con varianza cero dentro de la unidad. Bajo la tabla de perfiles eso implicaba **90 parámetros de dispersión** que no existían ni tenían familia declarada, y el conteo real habría sido **234**. **Bajo el v4.0 la deuda cambia de forma:** la dispersión es parte de la especificación de cada condicional (§1.1.B), así que no son 90 números invisibles sino **14 familias de distribución sin declarar** — enumerables, y con dueño. Mientras no se declaren, el check de 28.d **sigue sin poder correr**: es un principio sin artefacto de salida, el patrón que explica casi todos los fallos de este programa.
**Requisito v4.0:** para cada una de las **14 condicionales** de §1.1.F, declarar familia de distribución, dispersión y clase de procedencia.

---

### 6.1 El denominador bajo el v4.0 *(deriva completa en §1.1.F)*

**Los 144 se parten en dos, y solo una parte sigue siendo un conteo de números.**

| Bloque | v3.4 | **v4.0** |
|---|---|---|
| `params_base` | **90** números (15 parámetros × 6 perfiles) | **14 condicionales** θ_k( · \| x ) de dimensión indeterminada — la forma funcional está PENDIENTE (§1.1.B) |
| Coeficientes de generador | 15 | **15** — sin cambio |
| Probabilidades de regla | 39 | **39** — sin cambio |
| **Enumerables como números** | **144** | **54** (15 + 39), de los cuales **4** son `MEDIDO` |

**Titular nuevo del bloque de parámetros (M6, mesa del 31/jul):**

> ## 📊 **Condicionales medidas sobre atributos: ~~6~~ 8 de 14**
> *(Corregido 4/ago/2026 — `CAL-CONF` Fase B posiciones 5-6, `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §5: mide `radio_confianza` (ENCUCI) y `familismo_apoyo` (ENIF). Ver §1.1.F, Paso 5. `4 de 144` sigue congelado y no se toca, ver abajo.)*

**`D`=14 sale del diseño de §1.1, no de una estimación.** Su aritmética: 15 parámetros por perfil (nombrados y controlados contra el `+36` de la tabla de arriba) **menos** `acceso_digital`, que bajo el reencuadre es un **atributo observable** y no un parámetro. Ver §1.1.F, pasos 1–5.

⚠️ **`4 de 144` no se mueve en este acto.** Sigue congelado por decisión de mesa (`forense/hallazgos.md`, 31/jul/2026). La aritmética de arriba muestra qué le pasa al denominador; **qué hacer con el titular** —congelarlo como cifra histórica o retirarlo— es la decisión que `revision §6.3` dejó abierta, y no está entre las que este acto implementa.

⚠️ **Los 22 grados de libertad del ajuste (ADR-51: 7 + 15) no incluyen las 14 condicionales.** Son cosas distintas: 22 es lo que el ajuste tiene que fijar; 14 es lo que hay que **medir** para que el ajuste pueda fijar los 15 coeficientes sin quedarse en el producto β·θ (§1.1.F, paso 4). Sumarlos sería un error de categoría.

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
- **Condicionales medidas sobre atributos: ~~6~~ 8 de 14** (§1.1.F · §6.1, corregido 4/ago/2026 — `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §5). De las 14: **8 MEDIDO·PARCIAL** (`confianza_institucional[salud/educación/financiera/seguridad-FFAA/justicia-policía/electoral-partidos]`, 6 de 6, más `radio_confianza` y `familismo_apoyo`), 1 con reactivo retirado pendiente de localizar (`exposicion_violencia` — propuesta de clase, no sellada, ver §1.1.F Paso 5), 3 solo proxy, 2 sin reactivo o no determinables.
- **Números enumerables: 54** (15 coeficientes + 39 probabilidades), **cuatro medidos**. ⚠️ *El titular `4 de 144` sigue congelado y no se mueve aquí (§6.1).*
- **Grados de libertad reales del ajuste: 22** = 7 de probabilidad + 15 coeficientes (ADR-51, corrigiendo el "29 = 14+15" de ADR-50). **De esos 22: 7 identificados —2 truncados—, 2 justo identificados, 5 inidentificables, 8 no determinables en este régimen** (P2 §2.d).
- **Las 14 familias de distribución exigidas por ADR-28.d no están declaradas** — mientras falten, el check de varianza intra-celda no puede correr (§1.2, §6).

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

*Módulo completo (las nueve preguntas del Bloque B, `instrucciones-proyecto-v2.md`). **Este artefacto sí afirma sobre México** — describe cómo se construye la población simulada del país y qué se puede y no se puede medir de ella—, así que el módulo aplica entero, no en la forma reducida que ADR-48 dejó para artefactos de solo proceso.*

**1 · ¿Qué parte confunde pobreza, desigualdad, violencia o informalidad con "cultura"? — y en particular: ¿el diseño de celdas confunde estructura con cultura?**

**El riesgo se reduce en un lugar y se concentra en otro. Los dos hay que decirlos.**

**Dónde baja.** La tabla vieja tenía una fila llamada *"Popular informal"* con **quince valores puntuales asociados a ella**. Un lector razonable la leía como un tipo de persona: quince rasgos que van juntos porque quien está en esa fila **es así**. Bajo el v4.0 no hay fila: hay un vector de atributos —derechohabiencia, tramo de localidad, índice socioeconómico, tenencia de conexión— y catorce condicionales que se estiman **sobre esos atributos**. `segsoc`=2 no es una identidad: es un hecho sobre la relación laboral de una persona con el IMSS. Ese cambio de unidad es, en sí mismo, el mayor movimiento anti-esencialista que el modelo ha hecho: **la condicional dice "quién está expuesto a qué", donde la fila decía "quién es quién".**

**Dónde sube, y es la respuesta honesta.** Las celdas son celdas **de estructura** —formalidad, ingreso, localidad—, y sobre ellas se van a estimar parámetros con nombres **psicológicos**: `deferencia`, `familismo_obligacion`, `aversion_riesgo`, `sens_estatus`. Encontrar que E[`deferencia` | rural] > E[`deferencia` | urbano] **no distingue** entre "la gente rural defiere más" (cultura) y "en un mercado laboral sin salida y sin sanción creíble al patrón, deferir es lo que conviene" (estructura). **El diseño de celdas hace la correlación medible sin hacer el mecanismo identificable** — y una correlación bien medida con nombre psicológico es exactamente el material del que se hacen los estereotipos con cita.

Tres cosas lo contienen, y ninguna lo elimina:
- **§1.5** exige mecanismo estructural nombrado con fuente, más la **condición de dominancia** — el agente informal en entorno benigno debe terminar por debajo del formal en entorno hostil. Si el orden no se invierte, el diferencial es un rasgo y se rechaza en compilación.
- **§1.1.D** prohíbe que el motor lea número de perfil, que es la vía por la que la etiqueta volvía a operar como identidad.
- **La malla no se define sobre variables culturales.** Los seis ejes son de estructura y de exposición; ninguno pregunta por valores, creencias ni preferencias.

⚠️ **Y el caso peor sigue siendo `familismo_obligacion`**, ahora con nombre propio: la configuración "apoyo alto + obligación alta" describe hogares donde el *pooling* es **estrategia económica ante Estado ausente**, no intensidad cultural de afecto. H-11 (§1.1.E) lo condiciona sobre formalidad × ingreso, es decir sobre estructura — pero **el contraste que separaría apoyo de obligación vive dentro del hogar y la malla no lo resuelve** (§1.1.A). Mientras eso siga así, "estas familias son más familieras" es una lectura que el dato **no puede refutar**, y por tanto una que este documento no autoriza.

**2 · ¿Qué sobregeneraliza desde clases medias urbanas?** El sesgo declarado de ADR-13 no lo toca este acto: el corpus sigue sobre-muestreando al clasemediero urbano formal. El reencuadre **cambia dónde se ve el sesgo**: antes era el perfil 1 —el mejor evidenciado— rodeado de cinco filas peor evidenciadas; ahora es una región del espacio de atributos donde las condicionales tendrán más soporte que en el resto. Es el mismo sesgo, más honesto de leer: una condicional con soporte desigual **muestra** dónde adelgaza, mientras que una fila de tabla no mostraba nada. Lo que **sí** empeora es la cola alta: el perfil 4 era una fila con valores, y ahora es una región declarada **no observada** (§1.1.D). Perder la ilusión de cobertura no es perder cobertura.

**3 · ¿Qué está sesgado por marcos o muestras extranjeras?** Dos cosas, distintas entre sí.
- **Muestras (b):** `familismo_apoyo` y `familismo_obligacion` se sostienen en escalas validadas en muestras mexicano-americanas (Sabogal, Lugo Steidel, Knight, Calzada, Zeiders). H-09, H-10 y H-11 heredan la marca. **Se sigue reestructurando el esquema sobre medición de diáspora**, y el cambio de unidad no salda esa deuda: solo la traslada de celdas a condicionales.
- **Marco (c) nuevo, introducido por este acto:** **IPU** es literatura de transporte y planeación urbana estadounidense, adoptada aquí sin crítica propia. Se declara como marco importado **pendiente de crítica** (§1.1.C) precisamente para que no entre por la puerta trasera. También son (c) la distinción bases/descriptores de Wedel & Kamakura y la advertencia de Fischer & Schwartz que abre §1.

**4 · ¿Qué cambiaría con foco rural, indígena o popular?** Tres cosas concretas y una vieja.
- **El eje de urbanización se vuelve el eje crítico**, y es de nivel **hogar**: `tam_loc` no puede distinguir a dos personas del mismo hogar. Para un foco rural eso importa más que para uno urbano, porque los hogares rurales son más heterogéneos internamente en ocupación.
- **ENCIG, la fuente de los desenlaces de trámite, excluye por diseño toda localidad de menos de 100 000 habitantes** (§1.3). Cualquier condicional estimada ahí es **ciega al México rural**, y el truncamiento está declarado, no descubierto después.
- **El sistema indígena-comunal sigue fuera por diseño** (ADR-10) y el reencuadre no lo cambia: los seis ejes son ejes de la economía monetaria y del Estado nacional. Un vector de atributos no vuelve conmensurable lo que es de otro orden institucional.
- Y sigue en pie lo de siempre: `ref.A.02` (esfuerzo) y `ref.B.04` (colorismo), las dos refutaciones que más protegerían al México popular, están entre las **ocho sin objeto**. El modelo no tiene esas variables, y este acto no las añade.

**5 · ¿Qué parece psicológico y es un incentivo racional?** El resultado de G3, si se lee mal — Progresa muestra que **al estabilizar el ingreso cambia la conducta**, lo cual es a la vez la victoria del generador y la demostración de que manda el entorno. El v4.0 añade un caso nuevo: **H-01** (horizonte más corto bajo informalidad) es la hipótesis mejor sostenida del conjunto **y** la que más fácilmente se lee como impaciencia cultural. No lo es: dice que quien no sabe cuánto va a ingresar el mes que viene descuenta más el futuro, que es aritmética de la volatilidad, no un rasgo. La regla `R1.1` ya trae ese aviso; ahora la condicional también.

**6 · ¿Dónde hay evidencia débil e intuición fuerte?** En dos lugares nombrados.
- **El desdoblamiento de familismo**: la distinción apoyo/obligación está bien fundada en la literatura y **nadie la ha medido por separado en población EN México**. Bajo el v4.0 el problema es visible en vez de estar disuelto en dos columnas: H-11 tiene proxy (ENUT 6.11/6.11a) y **forma PENDIENTE y sin magnitud**.
- **El corte de `edad`**: tres de las doce hipótesis (H-02, H-06, H-07), tres de las diez reglas traducidas (`R1.4`, `R2.4`, `R5.4`) y el descriptor 5 dependen de un umbral de "joven" que **ningún inventario fija**. La intuición de que existe una cohorte divergente es fuerte en el corpus; el corte que la operacionaliza no existe. Está marcado **PENDIENTE** en los siete sitios donde se usa, y no se inventó aquí.

**7 · ¿Qué conclusión sería peligrosa mal usada?** Dos, y son casi opuestas.
- *"El v4.0 arregló el problema de identificabilidad."* **No.** P2 lo derivó y ADR-51 lo selló: la subidentificación **persiste sobre atributos**, con la causa mudada de la segmentación a la medición. El reencuadre arregla lo que estaba roto en cómo se particiona la población y **no toca** lo que está roto en qué reactivos existen. De 22 g.l., 5 son inidentificables y 8 no determinables en este régimen.
- *"Los perfiles estaban mal."* **Tampoco** — es la lectura que `revision §7` ya anticipó. Los perfiles fallan como **bases de asignación exclusiva** con estos datos; como **descriptores de heterogeneidad** siguen siendo el resumen del corpus, y por eso se conservan íntegros en §1.1.D. Lo que se retiró es la casilla, no el vocabulario.
- Y una tercera, propia de este acto: *"ahora la población es real porque viene de microdato."* La síntesis **hereda la conjunta de la semilla** y **no observa la cola alta** (§1.1.C). Una población sintética bien construida es un supuesto declarado, no una fotografía.

**8 · ¿Qué afirmación sobre el estado del corpus no fue derivada, sino escrita a mano?**

*Todo conteo de este documento va con su receta. Esta es la tabla completa.*

| Conteo | Receta · fuente | ¿Derivado? |
|---|---|---|
| **10 reglas citan perfil** | `grep -n '^- \*\*SI\*\*' <modelo> \| grep "perfil"` → 10 líneas, re-corrido sobre este archivo antes de editar. Coincide con `forense/hallazgos.md` 31/jul | **Sí, en esta sesión** |
| **Los 4 ejes que exigen** (formalidad, edad×urbano, migración, composición de hogar) | Lectura de las 10 líneas de arriba, una por una (§1.6) | **Sí** |
| **15 parámetros por perfil, nombrados** | Línea "Escalas" de `§1.1` del v3.4 + control contra §6: 9 (v1) + 5 (vector) + 1 (familismo) = 15, y 15 × 6 = 90 | **Sí** (§1.1.F, paso 1) |
| **`D` = 14 condicionales** | 15 − 1 (`acceso_digital` pasa a atributo, criterio C3) | **Sí** (§1.1.F, paso 2) |
| **9 + 2 + 3 = 14 por estado de reactivo** | P2 §2.c, más M2/M3 de ADR-51 (c); `confianza_institucional` contada por sus 6 componentes | **Sí** (§1.1.F, paso 5) |
| **0 condicionales medidas** | Ningún artefacto de `forense/` reporta una condicional estimada; los reactivos están localizados en inventario, no leídos en microdato | **Sí, por ausencia verificada** |
| **54 celdas pobladas + 36 vacías = 90** | Conteo de columnas con valor en la tabla del v3.4 (9 con valor × 6 filas) frente al vector de 6 componentes × 6 filas | **Sí** (§1.1.E) |
| **54 números enumerables** | 144 − 90 = 15 coeficientes + 39 probabilidades | **Sí** (§6.1) |
| **22 g.l. reales del ajuste (7 + 15)** | **NO derivado aquí — heredado.** ADR-51 (b), con dos derivaciones independientes citadas (P2 §0.2 y la sesión de ADR-51). Este documento **no** re-corrió el script sobre `milpa/procedencia.yaml` | **No — citado con su fuente** |
| **7 identificados / 2 justos / 5 inidentificables / 8 no determinables** | **NO derivado aquí — heredado** de P2 §2.d, tabla parámetro × estatus | **No — citado con su fuente** |
| **Variables, módulos y llaves de ENIGH** (§1.1.A) | **NO derivado aquí — citado** de P1 §1-§2, que sí las leyó del ZIP en disco. Este acto **no abre descriptores ni microdato** | **No — citado con su fuente** |
| **49 reglas · 27 de perímetro · 2 de 27 corridas · 20 `[FUERTE]`** | Sin cambio respecto del v3.4; recuento mecánico sobre §3.B, reproducible con `python3 tests/validador_registro_ids.py` | **Heredado, con receta ejecutable** |

⚠️ **Lo escrito a mano, sin receta, y por tanto lo que hay que vigilar:** (i) las **regiones de atributos de §1.1.D** son lectura de este documento sobre las descripciones verbales de los seis perfiles — nadie verificó que `est_socio`=3 sea "clasemediero", y no hay corte publicado que lo sostenga; (ii) la asignación **hipótesis → atributo condicionante** de §1.1.E es interpretación de los patrones de la tabla vieja, no una derivación mecánica; (iii) la correspondencia **reactivo ↔ parámetro** (que ENCUCI `AP5_1_*` mida `radio_confianza`, que ENIF `P9_9_4` mida `familismo_apoyo`) es lectura de etiquetas de inventario y **P2 ya la declaró sin validación de constructo**. Ninguna de las tres se presenta como medición.

**9 · ¿Qué restricción o deuda hereda este artefacto sin verificar?** Tres, nombradas:
- **P1 no se re-verificó.** Las variables, catálogos y llaves de §1.1.A se citan de P1, que leyó el ZIP con hash verificado. **Este acto no abrió `data/raw/` ni ningún descriptor** — perímetro `canon/` + `forense/`, ADR-46. Si P1 se equivocó en un nombre de campo, este documento hereda el error.
- **La composición de hogar entra como eje sin haber sido inventariada** (§1.6). El encargo la exige, P1 no la verificó, y aquí queda declarada PENDIENTE en vez de resuelta o silenciada.
- **El renombre de archivo deja citas colgando.** ADR-36 obliga a renombrar al subir versión mayor, y M5 lo ratifica. Seis citas por nombre de archivo a `modelo-decision-v3_4.md` viven en `canon/gobernanza-v1_15.md` (5) y `canon/estado-programa-v1_9.md` (1), **ambos fuera del perímetro de este acto** (Encargo A). Quedan como **cascada declarada y no ejecutada**, igual que ADR-50 hizo con la suya. Las de `forense/` no se tocan: ese árbol es append-only y sus citas son históricas por diseño.

---

## 9 · Si vas a cruzar hallazgos contra este documento

**Cita la regla textualmente**, con su tier, su dominio y **su condición de atributos** *(v4.0: antes decía "y perfiles" — las diez reglas que citaban número de perfil citan ahora el atributo, §1.6)*. Si tu encargo te pidió estresar una regla que no aparece en §3.B, **es una propuesta nueva** y tu veredicto **no cuenta como validación del modelo** — cuenta como evaluación de una hipótesis.

⚠️ **Si vas a citar en términos de perfiles, traduce primero.** Todo lo escrito antes del v4.0 —`hitoD-preregistro`, fichas, notas de `forense/`— habla de perfiles y **queda como historia append-only**, no se reescribe. La tabla de traducción perfil → región de atributos es **§1.1.D**; la de regla → condición nueva es **§1.6**. Citar un número de perfil como si fuera una entrada del motor es lo que §1.1.D prohíbe.

⚠️ **Este documento ES el motor: contiene las 49 reglas, no una foto de ellas.** La ficha derivada que existía hasta v2.5 omitía cuatro `[FUERTE]` y degradaba una: si un encargo previo te pidió estresar algo del dominio **Familia y pareja**, de la **tanda** o del **puente personal**, y no lo encontraste, el hueco estaba en la ficha, no en el motor. **Esa clase de fuga ya no es posible: una sección no se puede desincronizar de su propio documento.**

*Por qué: de 13 reglas que las cuatro verticales dijeron estresar, **6 no existían en el motor** y 4 divergían en alcance. Sus veredictos no transfirieron.*
