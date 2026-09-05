# S6 · Pre-registro de `salud.atencion.grave` — medible como está, dos linajes sin reconciliar

### `prereg-caja-S6-L16` · **v1.0** · 5 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S6-L16-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S6-L16`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`/`.sav`, de **dos** diseños falsadores paralelos e independientes para `salud.atencion.grave` (`R4.4`) — el panel `ENNVIH` (+ corroboración `ENDIREH` 2016), linaje de `MAESTRA34-N5`/`MAESTRA37-L1`, y `ENSANUT2024` (`integrantes_ensanut2024_w_icb.dta` + `utilizadores_ensanut2024_w.dta`), linaje de `MAESTRA37-L3`/`L3-BIS` — porque el árbol trae **dos** `EXISTE-SATISFACE` ya sellados para este mismo `id`, sobre reactivos que **no se solapan**, sin que ninguna nota los reconcilie (§0.2). |
> | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `salud.atencion.grave` (hoy `[MEDIA]`, línea 527) ni sella la clasificación `MEDIBLE-COMO-ESTÁ` que `N10 §2.2` propone. No decide cuál de los dos linajes es "el" correcto — eso es trabajo de dirección/mesa, no de esta pieza (§0.2). |
> | **VERIFICAS ASÍ** | Caja abre primero el que tenga codebook accesible; si ambos lo tienen, corre los dos y reporta ambos veredictos por separado — nunca promedia ni elige uno para reportar solo. Confirma en particular si `H0402`/`H0409A-D` (rama `ENSANUT2024`) realmente distinguen severidad/complejidad del síntoma, o si — como `es09` de 2009 (§1.1) — la palabra que la ficha asume ("grave") no es literalmente la que el reactivo trae. |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd1d566220ac81ebbac47c1c80ae14d66e` (SHA de redacción del encargo).

---

## 0 · Ficha bajo prueba y corrección de premisa (A.8/D-13)

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:527` (§3.4 Salud y cuerpo), verbatim:

> *SI el síntoma es grave o crónico complejo ENTONCES busca el sistema público pese a la espera — PORQUE la complejidad excede al consultorio — `[MEDIA]`.* · **id:** `salud.atencion.grave`

Verificación previa (A.8, `tools/ya_medido.py`, corrida el 5/sep/2026 desde `origin/main = b17d19bd`):

```
$ python3 tools/ya_medido.py salud.atencion.grave
=== ya_medido: salud.atencion.grave ===
  resuelto por canon: salud.atencion.grave -> R4.4
-- milpa/tramite.yaml -- (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 -- R4.4 | L241 | ... | [MEDIA] | No
-- forense/notas/*-L*-*.md -- MAESTRA37-L1-censo.md:70, -remapeo.md:25;
     MAESTRA37-L3-BIS-veredictos.md:59,67,248,255; MAESTRA37-L3-veredictos.md:77,97,215,222
-- forense/prereg-caja/S*-spec-*.md -- S3-C1-spec-v1_0.md:30 (mención de N36, no de esta regla)
-- canon/registro-rotulos.tsv (alias) -- L MAESTRA37-L3-BIS
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA` — ninguna de las citas de arriba es una falsación real corrida; son clasificaciones `EXISTE-SATISFACE`/`EXISTE-NO-SATISFACE` **de existencia de reactivo**, no corridas del falsador. Consistente con `N10 §2.2`, que también declara `NUNCA-MEDIDA` antes de proponer `MEDIBLE-COMO-ESTÁ`.

### 0.2 · Corrección de premisa — dos linajes `EXISTE-SATISFACE`, sin reconciliar, verificado contra el texto real de cada nota (A.8/D-13)

`N10 §2.2` cita el linaje `ENNVIH` (`es09`/`es09a` disparador, `cen10*` desenlace) como la base de la propuesta `MEDIBLE-COMO-ESTÁ` — el mismo linaje que `MAESTRA34-N5` estableció (`forense/notas/2026-09-03-mapeo-ola6-N5.md:59`) y que `MAESTRA37-L1` heredó sin cambio (`-remapeo.md:25`, *"sin cambio — 14 aciertos de institución (IMSS/Seguro Popular)... refuerzan el desenlace ya satisfecho por N5, no lo cambian"*). Pero **dos actos posteriores en la misma cadena — `MAESTRA37-L3` y `L3-BIS` — sellaron `EXISTE-SATISFACE` para el mismo `id` sobre un par de reactivos completamente distinto**: `H0402`/`H0409A-D` (disparador, `integrantes_ensanut2024_w_icb.dta`) y `u0201`/`u0204h`/`u0204m`/`u0205h`/`u0205m`/`U0202UA` (desenlace, `utilizadores_ensanut2024_w.dta`), ambos `ENSANUT2024`. `L3-veredictos.md:88` afirma que esto es lo que *"`L1` lo dio `EXISTE-SATISFACE` sin cambio (**heredado de `N5`**)"* — verificado: **`N5` no menciona ni `ENSANUT`, ni `u0201`, ni `H0409` en ningún punto de su propio texto** (`grep -in "ensanut\|u0201\|H0409\|utilizadores" forense/notas/2026-09-03-mapeo-ola6-N5.md` → 0 apariciones). `L3` no confirma el par de `N5`; lo **sustituye** por uno nuevo, sin declarar la sustitución como tal — y `L3-BIS` re-sella ese mismo par ("`CONFIRMADO SIN CAMBIO`") sin mencionar `ENNVIH`/`ENDIREH` tampoco (0 apariciones, verificado). `N10 §2.2`, al escribir su propia ficha, tampoco cruza contra `L3`/`L3-BIS` — cita solo el linaje `ENNVIH`/`N5`, con el comentario *"confirma que no hay mejor instrumento que ENNVIH, no lo desplaza"* — una afirmación que no se sostiene si `L3`/`L3-BIS` ya habían sellado un instrumento distinto, con codebook, un día antes.

**Esta pieza no adjudica cuál de los dos linajes es el correcto** — eso excede el perímetro de un pre-registro y es, en rigor, una pregunta para dirección/mesa (dos sellos `EXISTE-SATISFACE` en pie, sin que ninguno se haya retirado). Pre-registra **los dos**, como falsadores independientes (§3-§4), y dejan la reconciliación declarada, no resuelta.

### 0.3 · Segunda corrección — `cen10*` no distingue público de privado (verificado, no asumido)

`N5`/`N10` describen `cen10*` como "desenlace, lugar de consulta" — leído como si permitiera distinguir sistema público de privado. Verificado contra las tres olas de `data/inventario-reactivos-ext-v1_0.tsv` (`ehh02dta_all/ehh02dta_b5/v_cen1.dta`, `ehh05dta_b5/v_cen1.dta`, `ehh09dta_all/ehh09dta_b5/v_cen1.dta`, listado completo de cada módulo): **`cen10d_1`/`cen10l_1`/`cen10m_1`/`cen10e_1`/`cen10p_1` son, sin excepción, identificadores geográficos** — dirección, localidad, municipio, estado, país del lugar de consulta — **ninguno codifica tipo de institución** (IMSS/ISSSTE/privado/Seguro Popular). Las únicas variables de ese mismo módulo que sí nombran una institución (`clave1` "ID CLINICA COMUNITARIO", `clave2` "ID PROVEEDOR SALUD COMUNITARIO") existen **solo en la ola 2002**, ausentes en 2005 y 2009. **El desenlace "sistema público" del `SI...ENTONCES` no está en `cen10*` por sí solo** — requeriría cruzar contra un directorio externo de establecimientos por dirección/municipio, que este repo no tiene registrado, o depender de `clave1`/`clave2`, solo disponibles en una de las tres olas. Esta corrección no retira la clasificación `MEDIBLE-COMO-ESTÁ` propuesta por `N10` (la rama `ENDIREH` sí trae público/privado explícito, §1.2) — pero sí corrige la caracterización de `cen10*` antes de que caja asuma que basta abrirlo.

---

## 1 · Rama A — `ENNVIH` + `ENDIREH` (linaje `N5`/`L1`)

**Nota de procedencia del inventario:** ninguna de las variables de esta rama aparece en `data/inventario-reactivos-descargas-mx-v1_1.tsv` (verificado, 0 filas para `es09`/`cen10`/`p6_15_8`/`p6_17_8`/`ennvih`/`endireh`) — viven en `data/inventario-reactivos-v1_2.tsv` + `data/inventario-reactivos-ext-v1_0.tsv` (el universo de 241 591 filas que `N5` usó, `forense/firmas-pendientes.tsv:204`/`FP-212`). Esta pieza cita `ext-v1_0.tsv` explícitamente en cada fila para que caja no la busque donde no está.

### 1.1 · `es09`/`es09a` (disparador) — el texto varía por ola y por módulo, declarado

| ola | módulo (`archivo_miembro`) | línea (`ext-v1_0.tsv`) | texto verbatim |
|---|---|---|---|
| 2002 | `ehh02dta_all/ehh02dta_b3b/iiib_es.dta` | 34929 | «HA TENIDO PROBLEMA SERIO SALUD» |
| 2002 | `ehh02dta_all/ehh02dta_bx/p_es.dta` | 37019 | «HA TENIDO PROBLEMA SALUD GRAVE» |
| 2005 | `ehh05dta_b3b/iiib_es.dta` | 38186 | «HA TENIDO PROBLEMA SERIO SALUD» |
| 2005 | `ehh05dta_bx/p_es.dta` | 40697 | «HA TENIDO PROBLEMA SALUD GRAVE» |
| 2009 | `ehh09dta_all/ehh09dta_b3b/iiib_es.dta` | 46103 | «HA TENIDO PROBLEMA SERIO SALUD?» |
| 2009 | `ehh09dta_all/ehh09dta_bx/p_es.dta` | 48578 | «HA TENIDO PROBLEMA SERIO SALUD?» |

**Solo el módulo `bx` (`p_es.dta`) de 2002 y 2005 trae literalmente la palabra "GRAVE"** — el mismo módulo en 2009 y el módulo `b3b` en las tres olas dicen "SERIO", un adjetivo distinto. Esta pieza pre-registra el módulo `bx`/2002 (`es09` = «HA TENIDO PROBLEMA SALUD GRAVE») como el más cercano textualmente al `SI` de la regla, y declara 2005 (mismo módulo, mismo texto) como réplica; 2009 y el módulo `b3b` de las tres olas se citan como evidencia de la variable, no como parte del falsador de §3 — la palabra que cambia (GRAVE→SERIO) no se hereda a ciegas.

`es09a` (ventana temporal, ausente en 2002): 2005 `ehh05dta_b3b/iiib_es.dta:38187` «TENIDO PROBLEMA SALUD ULT 4ANIOS», `ehh05dta_bx/p_es.dta:40698` «TENIDO PROB SALUD GRAVE ULT 4ANIOS»; 2009 `iiib_es.dta:46104`/`p_es.dta:48579` «HA TENIDO PROBLEMA SERIO SALUD ULT 4ANIOS?» (ambos módulos, mismo texto). La ventana declarada ("4 años") no coincide aritméticamente con la separación real entre 2002 y 2005 (3 años) — coincide con 2005→2009 (4 años). Frase fija del instrumento, no algo que este repo calculó; se declara, no se corrige.

### 1.2 · Desenlace — `cen10*` (geografía, §0.3) + `ENDIREH` (público/privado explícito, corroboración)

`cen10*` (mismas tres olas, módulo `v_cen1.dta`) da solo geografía (§0.3) — se cita como variable existente, no como desenlace suficiente por sí solo.

**Corroboración `ENDIREH 2016`** (`endireh2016/bd_mujeres_endireh2016_sitioinegi_spss.zip`, miembro `BD_MUJERES_ENDIREH2016_SitioINEGI.sav`, `data/inventario-reactivos-ext-v1_0.tsv`), la única fuente del corpus con público/privado explícito en el texto del reactivo:

| variable | línea | texto verbatim | institución |
|---|---|---|---|
| `p6_15_7_1/2/3` | 21273 | «6.15.7. En clínica, centro de salud u hospital público, ¿usted solicitó…» | **público** |
| `p6_16_7` | 21291 | «…pidió apoyo, orientación o servicios a, clínica, centro de salud u hospital público?» | público |
| `p6_17_7` | 21301 | «La última vez que acudió a, clínica, centro de salud u hospital público, ¿le dieron la información...?» | público |
| `p6_18_7` | 21311 | «…cómo la atendieron?» (público) | público |
| `p6_15_8_1/2/3` | 21276-21278 | «6.15.8. En consultorio médico, clínica u hospital privado, ¿usted solicitó…» | **privado** |
| `p6_17_8` | 21302 | «6.17.8. La última vez que acudió a, consultorio médico, clínica u hospital privado, ¿le dieron la información, apoyo o servicio que necesitaba?» | privado |

**Reserva declarada, honesta (mismo criterio que `N5` ya aplicó):** estos ítems viven en la Sección 6 de `ENDIREH` — una batería sobre búsqueda de ayuda **tras violencia** contra la mujer, no tras un síntoma de salud grave. El contraste público/privado es real y explícito, pero el antecedente que lo activa (violencia) no es el antecedente de esta regla (síntoma grave/crónico complejo). Se cita como **corroboración de que la distinción público/privado existe y es medible en el corpus**, no como satisfacción directa del `SI` de `R4.4` — mismo estándar que `N5` fijó para esta misma fuente.

### 1.3 · Universo y ponderador — Rama A

**Universo:** personas encuestadas en el módulo de salud de `ENNVIH` (hogar) que reportan `es09=1` (síntoma grave, módulo `bx`, ola 2002 o 2005). El vínculo entre `es09`/`es09a` (libro `bx`/`b3b`) y `cen10*` (libro `b5`) requiere unir por folio de persona/hogar — **libros distintos del mismo cuestionario**, no la misma tabla; declarado, no asumido como trivial.

**Ponderador — hallazgo nuevo de esta pieza, no heredado de prosa.** Búsqueda exhaustiva (`awk` filtrado por payload + regex de ponderador) sobre el zip que trae `es09`/`cen10*` (`ehh0Xdta_all.zip`): **0 filas** — el zip de hogar **no trae ningún ponderador**. El factor de expansión vive en un payload **separado**, no indexado en `data/inventario-reactivos-descargas-mx-v1_1.tsv` en absoluto:

| ola | id de manifiesto | archivo | variable de peso | ambigüedad declarada |
|---|---|---|---|---|
| 2002 | `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | (no inspeccionado línea a línea en esta pieza — ver `S5`-style reserva) | — |
| 2009 | `ennvih3_2009_ponderador_transversal` | `ennvih/ehh09w_all.zip` | `fac_3b` (libro 3B, `ehh09w_b3b.dta`) para la copia de `es09` en `iiib_es.dta`; **para la copia en `p_es.dta` (libro `bx`), tres candidatos** (`fac_3a_px`/`fac_3b_px`/`fac_4_px`, todos «FACTOR DE EXPANSIÓN LIBRO PROXY») **sin que el inventario, por sí solo, diga cuál corresponde** | sí — resolver contra codebook, no adivinar |

**Estrato:** una sola variable, `estrato` («ESTRATO»), en `ehh0Xdta_all/ehh0Xdta_bc/c_portad.dta` (2002 línea 4159, 2005 línea 7639, 2009 línea 48050 [conteo de `ext-v1_0.tsv`, confirmado por dos agentes de investigación independientes con el mismo resultado]). **Ningún `upm`/`cluster`/`psu`/`conglomerado`** en ninguna de las tres olas — buscado, cero.

Si caja no resuelve la ambigüedad de peso del libro `bx`/2002, la corrida sale **sin ponderar**, declarado, mismo criterio que el resto de esta serie de specs.

---

## 2 · Rama B — `ENSANUT2024` (linaje `L3`/`L3-BIS`)

**Nota de procedencia:** estas variables sí están en `data/inventario-reactivos-descargas-mx-v1_1.tsv` — el mismo inventario que `N10` usó para todo lo demás en su acto.

### 2.1 · Disparador — `integrantes_ensanut2024_w_icb.dta`

| variable | línea | texto verbatim (truncado en la fuente, tal cual) |
|---|---|---|
| `h0402` | 29181 | «H0402 ¿Podría decirme cuál fue la última necesidad de salud que tuvo (USTED/NOMB[RE]…» |
| `H0409A` | 29196 | «H0409 ¿La atención que buscó (USTED/NOMBRE) requirió…» |
| `H0409B` | 29197 | «H0409 ¿La atención que buscó (USTED/NOMBRE) requirió…» |
| `H0409C` | 29198 | «H0409 ¿La atención que buscó (USTED/NOMBRE) requirió…» |
| `H0409D` | 29199 | «H0409 ¿La atención que buscó (USTED/NOMBRE) requirió…» |

**Reserva, honesta, antes de que caja lo dé por hecho:** `H0402` pregunta por la **última necesidad de salud** — abierta/categórica, no una escala de gravedad. `H0409A-D` pregunta si la atención **requirió** algo (el texto se corta antes de decir qué — hospitalización, cirugía, medicamento, especialista, son las cuatro opciones más probables por el patrón A-D, **no confirmado sin abrir el codebook**). Ninguna de las dos, con el texto disponible en el inventario, dice literalmente "grave" o "crónico complejo" — `L3`/`L3-BIS` las clasificaron `EXISTE-SATISFACE` presumiblemente por el texto completo del cuestionario en PDF (`data/l3-ensanut2024-cuestionarios-v1_0.txt`, citado por `L3-veredictos.md:3-10`), no por el inventario. **Esta pieza no reabre esa clasificación — la cita y advierte que el inventario por sí solo no la confirma; caja verifica con el codebook antes de calcular.**

### 2.2 · Desenlace — `utilizadores_ensanut2024_w.dta`

| variable | línea | texto verbatim (truncado en la fuente) |
|---|---|---|
| `u0201` | 30756 | «U0201 ¿En qué institución de salud (USTED/NOMBRE) se atendió/recibió atención?» |
| `U0202UA` | 30779 | «U0202 ¿Por qué motivos se atendió en este lugar?» |
| `u0204h`/`u0204m` | 30784-30785 | «U0204H/M Aproximadamente, ¿cuánto tiempo tardó en llegar al lugar en donde le aten[dieron]…» |
| `u0205h`/`u0205m` | 30786-30787 | «U0205H/M Una vez en el lugar de atención, ¿cuánto tiempo aproximadamente tuvo que [esperar]…» |

`u0201` es la variable que sí puede dar institución (lista de opciones — IMSS, ISSSTE, SSA/público, privado, etc. — pendiente de codebook, no visible en el inventario) — **más directa que `cen10*` de la Rama A**, que solo da geografía (§0.3). `u0205h`/`u0205m` (tiempo de espera **en el lugar**) es, textualmente, la variable más cercana a "pese a la espera" del propio `PORQUE`/`ENTONCES` de la regla — ninguna variable de la Rama A tiene un análogo directo a esto.

### 2.3 · Universo y ponderador — Rama B

**Universo:** `integrantes_ensanut2024_w_icb.dta` es el módulo de integrantes del hogar (`H0402`/`H0409`); `utilizadores_ensanut2024_w.dta` es el módulo de quienes efectivamente utilizaron un servicio (`u0201`/`u0204`/`u0205`) — unión por folio de persona, dos tablas distintas del mismo levantamiento 2024, declarado igual que la Rama A.

**Ponderador, estrato, UPM** (mismo diseño muestral que comparten los módulos de persona de `ENSANUT2024`, ya verificado para `S7 §2` sobre los mismos payloads): `ponde_f` («Ponderador»), `estrato` («Estrato urbanidad/ruralidad»), `est_sel` («Estrato de selección»), `upm` («Unidad primaria de muestreo»). Sin `cluster`/`conglomerado` bajo ese nombre literal.

---

## 3 · Dicotomizaciones y celdas

**Rama A:** `SINTOMA_GRAVE` = 1 si `es09`=1 (módulo `bx`, 2002/2005, §1.1); `BUSCA_PUBLICO` — no construible directamente de `cen10*` (§0.3); se pre-registra como **`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`** salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente. Celda de corroboración (no del mismo antecedente): `ENDIREH` `INSTITUCION_PUBLICA` (`p6_*_7`) vs. `INSTITUCION_PRIVADA` (`p6_*_8`), sobre el universo de mujeres que buscaron ayuda tras violencia — reportada aparte, nunca sumada a la celda de `R4.4` (antecedentes distintos, §1.2).

**Rama B:** `NECESIDAD_ULTIMA` (`H0402`, categorías pendientes de codebook) y/o `ATENCION_REQUIRIO_X` (`H0409A-D`, pendiente de codebook para saber qué mide cada sufijo) como candidatos a `SINTOMA_GRAVE` — **sin corte pre-registrable hasta que caja abra el codebook**, declarado como brecha, no como corte inventado. `INSTITUCION_PUBLICA` = subconjunto de categorías de `u0201` que el codebook marque como público (IMSS/ISSSTE/SSA/Bienestar) vs. privado — **mismo pendiente**.

**Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que el resto de esta serie (`S4`/`S5`/`S8`).

---

## 4 · Falsador `B-bis`

| | Rama A (`ENNVIH`+`ENDIREH`, corroboración) | Rama B (`ENSANUT2024`) |
|---|---|---|
| **Signo esperado** | entre síntoma grave (`es09=1`), mayor proporción busca institución pública que privada (si `clave1`/`clave2` lo permiten, 2002 solamente) | entre quienes `H0409` marca como requiriendo mayor complejidad, mayor proporción en `u0201`=institución pública |
| **`CORROBORADA`** | proporción pública > proporción privada, IC95 excluye la paridad | ídem, sobre `u0201` |
| **`CONTRARIA`** | proporción pública < privada, IC95 excluye paridad en signo opuesto | ídem |
| **`NO-DISCRIMINA`** | IC95 contiene la paridad | ídem |
| **`NO-ESTIMABLE`** | **fila que `B-bis` exige:** si `clave1`/`clave2` (única vía a institución en Rama A) no alcanza para clasificar la muestra completa, o el numerador de alguna celda cae bajo 10, el veredicto de Rama A queda **sin construir** — la corroboración `ENDIREH` (§1.2) se reporta aparte, declarada como evidencia de que el contraste público/privado existe en el corpus, no como sustituto del falsador de `R4.4` | si `H0402`/`H0409` no discriminan gravedad tras abrir el codebook (por ejemplo, si son puramente categóricas sin gradiente de severidad), el veredicto de Rama B queda igual de `NO-ESTIMABLE`, declarado |

**Qué significaría corroborar cualquiera de las dos ramas.** Sería la primera falsación real de `R4.4` (§0.1, `NUNCA-MEDIDA`). Dado que las dos ramas ya traen `EXISTE-SATISFACE` sellado por actos distintos sin reconciliar (§0.2), corroborar **ambas, en el mismo sentido**, sería la evidencia más fuerte posible — dos instrumentos independientes, mismo signo. Corroborar solo una y no la otra (o que una salga `NO-ESTIMABLE` por las razones de §0.3/§2.1) es un resultado igual de informativo: dice cuál de los dos linajes de clasificación sobrevive el primer contacto con datos reales.

**Reserva, declarada antes de medir.** Asociación transversal, sin identificación causal. El `PORQUE` ("la complejidad excede al consultorio") es mecanismo, no antecedente exigible — no se mide, mismo criterio que el resto de esta serie. Ninguno de los cortes de §3 está confirmado sin codebook; caja los declara al abrir, no los hereda de esta pieza a ciegas.

---

## 5 · `se_mueve_si`

**Rama A:** si entre quienes reportan síntoma grave (`es09=1`, 2002/2005) la proporción que acude a institución pública (vía `clave1`/`clave2`, 2002) **no es mayor** que la que acude a privada, la regla se rompe para esa rama. **Rama B:** si entre quienes `H0409` marca con mayor requerimiento de atención la proporción en institución pública (`u0201`) **no es mayor** que en privada, se rompe para esa rama. Si ambas ramas caen por `NO-ESTIMABLE` (§4), `se_mueve_si` queda sin poder evaluarse con el corpus actual — hallazgo a reportar, no a forzar.

---

## 6 · Archivos que la caja necesita abrir

**Rama A:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
| `ennvih2_2005_hogar_dta` | `ennvih/ehh05dta_all.zip` | `fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a` |
| `ennvih3_2009_hogar_dta` | `ennvih/ehh09dta_all.zip` | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` |
| `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | `bbe8006844f715c19b724ebb74f1408c4cfa07e2efdfe7d6748b5182ef214587` |
| `ennvih3_2009_ponderador_transversal` | `ennvih/ehh09w_all.zip` | `e7929b49a7cd4f1eae5aa17da77c7eea4794d0f26265fbd40dde5e9c8e3ef8b8` |
| `endireh_2016_bd_mujeres_endireh2016_sitioinegi_spss` | `endireh2016/bd_mujeres_endireh2016_sitioinegi_spss.zip` | `d198b9022d5727d24cddccdfd019c749ca42acc5d3f3e86a5d67e40ebe6eff3a` |

**Rama B:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.stata.stata.zip` | `20a9fae339da3fa3fc6ce20e81b6b1cf32375b40baf5a876d760a15f01ec6aa9` |
| `utilizadores_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/utilizadores_ensanut2024_w.stata.stata.zip` | `b40a4dce264e657026b4046b07047031437a224182e373d27dde4a5e0360a563` |

No hay codebook de `ENNVIH` (2002/2005/2009) registrado como documento separado en el manifiesto en esta pieza — el mapeo de valores de `es09`/`clave1`/`clave2` y la resolución del ponderador de `p_es.dta`/2002 quedan pendientes de que caja lo busque en la documentación de `ennvih-mxfls.org`. `ENSANUT2024` sí tiene cuestionarios PDF ya citados por `L3` (`data/l3-ensanut2024-cuestionarios-v1_0.txt`) — no re-listados aquí, ese acto ya los registró.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `salud.atencion.grave` (`[MEDIA]`, línea 527) ni sella `MEDIBLE-COMO-ESTÁ`. No decide cuál de las dos ramas (`ENNVIH`/`ENDIREH` vs. `ENSANUT2024`) es la medición canónica de esta regla — declara la discrepancia (§0.2) para que dirección/mesa la resuelva, no la resuelve por su cuenta. No corrige `MAESTRA37-L3`/`L3-BIS` ni los retira — quedan `EXISTE-SATISFACE`/`CONFIRMADO SIN CAMBIO` como están. No reclasifica `salud.vacunacion.disponible` ni `comunicacion.inseguridad.ver_oir_callar` (`S7`/`S8`, mismo lote, piezas separadas). No toca `canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`.

**Medición: caja, acto `MAESTRA38-L16`** (rótulo derivado por continuidad de la serie `L`, máximo registrado hoy `L14`; `L15` deliberadamente sin usar aquí — ya propuesto en prosa por `N10 §2.4` para el acto sucesor de las candidatas `CNGMD`; `L17`/`L18` van a `S7`/`S8` de este mismo lote, contiguos).

**El primer resultado que produzca este procedimiento es el que se reporta — de cada rama, por separado.**
