# S6 · Pre-registro de `salud.atencion.grave` — medible como está, dos linajes sin reconciliar

### `prereg-caja-S6-L16` · **v1.1** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S6-L16-spec-v1_1.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S6-L16`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`/`.sav`, de **dos** diseños falsadores paralelos e independientes para `salud.atencion.grave` (`R4.4`) — el panel `ENNVIH` (+ corroboración `ENDIREH` 2016), linaje de `MAESTRA34-N5`/`MAESTRA37-L1`, y `ENSANUT2024` (`integrantes_ensanut2024_w_icb.dta` + `utilizadores_ensanut2024_w.dta`), linaje de `MAESTRA37-L3`/`L3-BIS` — porque el árbol trae **dos** `EXISTE-SATISFACE` ya sellados para este mismo `id`, sobre reactivos que **no se solapan**, sin que ninguna nota los reconcilie (§0.2). **v1.1 reescribe §1.3** (ponderador de la Rama A) — ver §0.4. |
> | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `salud.atencion.grave` (hoy `[MEDIA]`, línea 527) ni sella la clasificación `MEDIBLE-COMO-ESTÁ` que `N10 §2.2` propone. No decide cuál de los dos linajes es "el" correcto — eso es trabajo de dirección/mesa, no de esta pieza (§0.2). |
> | **VERIFICAS ASÍ** | Caja abre primero el que tenga codebook accesible; si ambos lo tienen, corre los dos y reporta ambos veredictos por separado — nunca promedia ni elige uno para reportar solo. Confirma en particular si `H0402`/`H0409A-D` (rama `ENSANUT2024`) realmente distinguen severidad/complejidad del síntoma, o si — como `es09` de 2009 (§1.1) — la palabra que la ficha asume ("grave") no es literalmente la que el reactivo trae. Para la Rama A (§1.3, v1.1): corre el CHEQUEO DE CONSISTENCIA del ponderador **antes** de calcular una sola celda — si falla, el proceso se PARA (§1.3, cuarto punto). |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd1d566220ac81ebbac47c1c80ae14d66e` (SHA de redacción del encargo original de `v1.0`). **v1.1 redactada por `ACTO MAESTRA38-N19`, 7/sep/2026, entorno NUBE sin corpus**, sobre `origin/main` tras `PR #580` (`MAESTRA38-TRAMITE-5`, este mismo grupo de actos).

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

**Re-verificado al redactar `v1.1` (7/sep/2026):** `ACTO MAESTRA38-LOTE-ENSANUT` (`L16`, 6/sep/2026) corrió esta spec — pero **solo la Rama B**. Su propio recibo en el tablero, verbatim: *"PARO parcial declarado en ambas piezas: Rama A (`ENNVIH`+`ENDIREH`) NO corrida — ponderador del libro `bx`/2002 con tres candidatos (`fac_3a_px`/`fac_3b_px`/`fac_4_px`) sin codebook de `ENNVIH` en el corpus para desambiguar."* `v1.1` existe exactamente para destrabar ese `PARO` — la Rama A **sigue sin correr ninguna celda**; esta pieza no la mide, la deja lista para que un acto `CAJA` la corra por primera vez.

### 0.2 · Corrección de premisa — dos linajes `EXISTE-SATISFACE`, sin reconciliar, verificado contra el texto real de cada nota (A.8/D-13)

`N10 §2.2` cita el linaje `ENNVIH` (`es09`/`es09a` disparador, `cen10*` desenlace) como la base de la propuesta `MEDIBLE-COMO-ESTÁ` — el mismo linaje que `MAESTRA34-N5` estableció (`forense/notas/2026-09-03-mapeo-ola6-N5.md:59`) y que `MAESTRA37-L1` heredó sin cambio (`-remapeo.md:25`, *"sin cambio — 14 aciertos de institución (IMSS/Seguro Popular)... refuerzan el desenlace ya satisfecho por N5, no lo cambian"*). Pero **dos actos posteriores en la misma cadena — `MAESTRA37-L3` y `L3-BIS` — sellaron `EXISTE-SATISFACE` para el mismo `id` sobre un par de reactivos completamente distinto**: `H0402`/`H0409A-D` (disparador, `integrantes_ensanut2024_w_icb.dta`) y `u0201`/`u0204h`/`u0204m`/`u0205h`/`u0205m`/`U0202UA` (desenlace, `utilizadores_ensanut2024_w.dta`), ambos `ENSANUT2024`. `L3-veredictos.md:88` afirma que esto es lo que *"`L1` lo dio `EXISTE-SATISFACE` sin cambio (**heredado de `N5`**)"* — verificado: **`N5` no menciona ni `ENSANUT`, ni `u0201`, ni `H0409` en ningún punto de su propio texto** (`grep -in "ensanut\|u0201\|H0409\|utilizadores" forense/notas/2026-09-03-mapeo-ola6-N5.md` → 0 apariciones). `L3` no confirma el par de `N5`; lo **sustituye** por uno nuevo, sin declarar la sustitución como tal — y `L3-BIS` re-sella ese mismo par ("`CONFIRMADO SIN CAMBIO`") sin mencionar `ENNVIH`/`ENDIREH` tampoco (0 apariciones, verificado). `N10 §2.2`, al escribir su propia ficha, tampoco cruza contra `L3`/`L3-BIS` — cita solo el linaje `ENNVIH`/`N5`, con el comentario *"confirma que no hay mejor instrumento que ENNVIH, no lo desplaza"* — una afirmación que no se sostiene si `L3`/`L3-BIS` ya habían sellado un instrumento distinto, con codebook, un día antes.

**Esta pieza no adjudica cuál de los dos linajes es el correcto** — eso excede el perímetro de un pre-registro y es, en rigor, una pregunta para dirección/mesa (dos sellos `EXISTE-SATISFACE` en pie, sin que ninguno se haya retirado). Pre-registra **los dos**, como falsadores independientes (§3-§4), y dejan la reconciliación declarada, no resuelta.

### 0.3 · Segunda corrección — `cen10*` no distingue público de privado (verificado, no asumido)

`N5`/`N10` describen `cen10*` como "desenlace, lugar de consulta" — leído como si permitiera distinguir sistema público de privado. Verificado contra las tres olas de `data/inventario-reactivos-ext-v1_0.tsv` (`ehh02dta_all/ehh02dta_b5/v_cen1.dta`, `ehh05dta_b5/v_cen1.dta`, `ehh09dta_all/ehh09dta_b5/v_cen1.dta`, listado completo de cada módulo): **`cen10d_1`/`cen10l_1`/`cen10m_1`/`cen10e_1`/`cen10p_1` son, sin excepción, identificadores geográficos** — dirección, localidad, municipio, estado, país del lugar de consulta — **ninguno codifica tipo de institución** (IMSS/ISSSTE/privado/Seguro Popular). Las únicas variables de ese mismo módulo que sí nombran una institución (`clave1` "ID CLINICA COMUNITARIO", `clave2` "ID PROVEEDOR SALUD COMUNITARIO") existen **solo en la ola 2002**, ausentes en 2005 y 2009. **El desenlace "sistema público" del `SI...ENTONCES` no está en `cen10*` por sí solo** — requeriría cruzar contra un directorio externo de establecimientos por dirección/municipio, que este repo no tiene registrado, o depender de `clave1`/`clave2`, solo disponibles en una de las tres olas. Esta corrección no retira la clasificación `MEDIBLE-COMO-ESTÁ` propuesta por `N10` (la rama `ENDIREH` sí trae público/privado explícito, §1.2) — pero sí corrige la caracterización de `cen10*` antes de que caja asuma que basta abrirlo.

### 0.4 · v1.1 reescribe §1.3 (`ADR-357`, `FP-328`(a)/(c), `ACTO MAESTRA38-C1`)

`v1.0` (§1.3 original) declaraba el ponderador del libro `bx`/2002 como una ambigüedad sin resolver entre `fac_3a_px`/`fac_3b_px`/`fac_4_px` — la misma ambigüedad que `ADR-357` había registrado y que causó el `PARO` parcial de `ACTO MAESTRA38-LOTE-ENSANUT` sobre esta misma Rama A (§0.1). `ACTO MAESTRA38-C1 · RE-ASIENTO` (7/sep/2026, pieza (h)) inventarió los candidatos con codebook real (`data/ennvih2002-ponderadores-candidatos-v1_0.tsv`, 13 filas) sin adjudicar — dejó la tabla para que dirección o un acto sucesor resolviera (`FP-328`(c)). **`v1.1` es ese acto sucesor**: adjudica `fac_3b_px` como el ponderador de la Rama A y reescribe §1.3 completo con la evidencia de `C1`. `v1.0` **no se edita** — sigue íntegra en su ruta original (A.10).

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

**Solo el módulo `bx` (`p_es.dta`) de 2002 y 2005 trae literalmente la palabra "GRAVE"** — el mismo módulo en 2009 y el módulo `b3b` en las tres olas dicen "SERIO", un adjetivo distinto. Esta pieza pre-registra el módulo `bx`/2002 (`es09` = «HA TENIDO PROBLEMA SALUD GRAVE») como el más cercano textualmente al `SI` de la regla, y declara 2005 (mismo módulo, mismo texto) como réplica; 2009 y el módulo `b3b` de las tres olas se citan como evidencia de la variable, no como parte del falsador de §3 — la palabra que cambia (GRAVE→SERIO) no se hereda a ciegas. **Esta distinción de módulo/etiqueta es exactamente la que separa el ponderador de §1.3, abajo: `bx`/GRAVE usa `fac_3b_px`; `b3b`/SERIO usa `fac_3b` (sin `_px`) — nunca el mismo factor, nunca la misma fila.**

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

### 1.3 · Universo y ponderador — Rama A · **REESCRITO en v1.1, ver §0.4**

**Universo de `bx`: subpoblación, declarada como tal — nunca contra un marginal poblacional (A-bis 4).** El módulo `bx` de `ENNVIH` es el **libro Proxy**: lo responde un informante del hogar **en nombre de** miembros del hogar que están ausentes al momento del levantamiento (migrantes, principalmente), no el universo completo de personas del hogar. `p_portad.dta` (ola 2002) tiene **1 903 filas** — la cobertura del libro Proxy, verificada contra `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (comentario de cabecera: *"libro bx = ehh02dta_bx/p_portad.dta (1903 filas, Proxy)"*), frente a **8 441 filas** del libro hogar (`c_portad.dta`, libro C) y **35 664 folios de hogar** que sí resuelven contra el join de ponderador (ver abajo). Por `A-bis 4` (`instrucciones-proyecto-v2_12.md`, Bloque A-bis, regla 4, verbatim: *"Un estimando restringido a una subpoblación no se compara contra uno poblacional... Se recalcula el marginal restringido al mismo universo, o se declara el resultado como acotado a esa subpoblación"*): toda celda que este falsador produzca sobre `bx` se declara **acotada a la subpoblación de miembros ausentes respondida por proxy** — nunca se reconcilia ni se compara contra una proporción del padrón completo de `ENNVIH`, ni contra la Rama B (`ENSANUT2024`, universo distinto por diseño). Si caja necesita un marginal de referencia, lo recalcula restringido al mismo universo `bx`, no al universo general.

**Ponderador: `fac_3b_px`.** Fuente: `ennvih1_2002_ponderador` (`data/manifiesto.yaml`, `ennvih/ehh02w_all.zip`), archivo interno `ehh02w_all/ehh02w_bx.dta`. Adjudicado sobre los otros dos candidatos ambiguos que `ADR-357` había dejado sin resolver, con la evidencia que `ACTO MAESTRA38-C1` levantó (`data/ennvih2002-ponderadores-candidatos-v1_0.tsv`, verificado de nuevo al redactar esta spec):

| candidato | libro | `n_no_nulo_gt0` | criterio |
|---|---|---|---|
| `fac_3a_px` | `bx` (`ehh02w_bx.dta`) | 21 631 | descartado — mismo libro, menor cobertura que `fac_3b_px` |
| **`fac_3b_px`** | **`bx`** (`ehh02w_bx.dta`) | **21 645** | **adjudicado** — mayor `n_no_nulo_gt0` de los tres candidatos del libro `bx`, misma etiqueta verbatim que los otros dos (`'FACTOR DE EXPANSIÓN LIBRO PROXY'`), pero el que más observaciones pondera con peso positivo |
| `fac_4_px` | `bx` (`ehh02w_bx.dta`) | 9 037 | descartado — cobertura muy inferior (≈42% de `fac_3b_px`) |

Los tres candidatos comparten la etiqueta verbatim `'FACTOR DE EXPANSIÓN LIBRO PROXY'` — no se distinguen por nombre, solo por `n_no_nulo_gt0` y por el hecho medido de que ninguno de los 11 codebooks de `ennvih/ehh02cb_all.zip` menciona la cadena `'fac'` (`C1`, verificado, control positivo 340 376 B de texto extraído). El documento que explica los tres es `ennvih/calculo-de-factores-de-expansion.pdf` §1.2 — caja lo abre si necesita la fórmula exacta; esta spec no la re-deriva.

**Llave de join: `folio`/`ls`, normalizada a entero ANTES de unir — sin esto, el join da 0.** Hallazgo de `C1`, verificado de nuevo aquí contra `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (comentario de cabecera, verbatim): *"En `ehh02w_all.zip` `folio` es cadena con ceros a la izquierda (`'00001000'`) y en el microdato es `float64` (`2000.0`): sin normalizar, TODOS los joins dan 0 — resultado falso, no hallazgo."* Normalizando ambos lados a entero (`int(folio)`, sin ceros a la izquierda, sin punto decimal), el join real produce **1 903 de 1 903** filas del libro Proxy resueltas contra el ponderador, y **35 664** folios de hogar resueltos contra el libro C — cifras que `C1` ya midió y esta spec hereda sin re-correrlas. Caja **no** intenta el join con `folio` sin normalizar: el resultado (0 filas) no es un hallazgo de que el ponderador no aplica, es el bug ya documentado.

**La rama directa `b3b` usa `fac_3b` (sin `_px`) y se reporta POR SEPARADO de `bx` — nunca agrupados.** El módulo `b3b` (`iiib_es.dta`, etiqueta "SERIO", §1.1) tiene su propio ponderador, `fac_3b` (sin sufijo `_px`), archivo `ehh02w_all/ehh02w_b3b.dta`, `n_no_nulo_gt0 = 19 809` — un archivo, una etiqueta ("FACTOR DE EXPANSIÓN LIBRO 3B") y una cobertura de universo **distintos** de `fac_3b_px`. El parecido de nombre (`fac_3b` vs `fac_3b_px`) es la trampa exacta que esta spec existe para evitar: `bx`/`fac_3b_px` mide sobre la subpoblación Proxy (miembros ausentes, etiqueta "GRAVE"); `b3b`/`fac_3b` mide sobre el universo directo del libro `3b` (miembros presentes, etiqueta "SERIO"). Agruparlos sumaría dos universos con dos ponderadores distintos bajo una sola celda — exactamente el error que `A-bis 4` prohíbe. Si caja corre ambas ramas (`bx` y `b3b`), **reporta dos filas separadas**, cada una con su propio ponderador y su propia declaración de subpoblación.

**CHEQUEO DE CONSISTENCIA OBLIGATORIO — se corre ANTES de calcular una sola celda; si falla, el proceso se PARA.** Sobre las filas de `p_es.dta` con `es09` no nulo (el universo real del falsador, no las 35 677 filas de persona-observación de todo el libro `bx` que sí discriminan por `n_no_nulo` pero no por respuesta a `es09` específicamente — ver la nota de `C1` sobre por qué `n_no_nulo` no discrimina y hay que usar `n_no_nulo_gt0`), `n_no_nulo_gt0` de `fac_3b_px` debe ser **mayor o igual** que el de `fac_3a_px` **y** que el de `fac_4_px`. Pseudocódigo/comando que caja corre:

```python
import pyreadstat
df, meta = pyreadstat.read_dta("ehh02w_all/ehh02w_bx.dta")
p_es, _ = pyreadstat.read_dta("ehh02dta_all/ehh02dta_bx/p_es.dta")
folios_es09 = set(int(f) for f in p_es.loc[p_es["es09"].notna(), "folio"])
df["folio_int"] = df["folio"].astype(int)
sub = df[df["folio_int"].isin(folios_es09)]
n_3b_px = (sub["fac_3b_px"].fillna(0) > 0).sum()
n_3a_px = (sub["fac_3a_px"].fillna(0) > 0).sum()
n_4_px  = (sub["fac_4_px"].fillna(0) > 0).sum()
assert n_3b_px >= n_3a_px and n_3b_px >= n_4_px, "PARA: la asignación libro→factor es incorrecta"
```

**Este acto no corre el chequeo contra el subconjunto exacto `es09` no nulo** (no abre microdato, NUBE sin corpus) — pero la versión ya medida por `C1` sobre el libro `bx` completo (35 677 filas de persona, `n_no_nulo_gt0`: `fac_3b_px=21 645` ≥ `fac_3a_px=21 631` ✔ y ≥ `fac_4_px=9 037` ✔) **ya satisface la desigualdad**, con margen estrecho contra `fac_3a_px` (14 observaciones de diferencia) y margen amplio contra `fac_4_px`. Si el subconjunto restringido a `es09` no nulo invierte el orden entre `fac_3b_px` y `fac_3a_px` (el margen de 14 es lo bastante estrecho para que eso sea posible), **la asignación libro→factor es incorrecta y el proceso se PARA** — caja no continúa con `fac_3b_px` sin volver a correr este chequeo sobre el subconjunto real.

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

**Estado real (v1.1): esta rama ya corrió** (`ACTO MAESTRA38-LOTE-ENSANUT`, `L16`, 6/sep/2026) — ver §0.1. Se conserva aquí sin cambio (v1.0 → v1.1 no toca §2) por completitud del pre-registro, no porque quede pendiente.

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

**Ponderador, estrato, UPM** (mismo diseño muestral que comparten los módulos de persona de `ENSANUT2024`): `ponde_f` («Ponderador»), `estrato` («Estrato urbanidad/ruralidad»), `est_sel` («Estrato de selección»), `upm` («Unidad primaria de muestreo»). Sin `cluster`/`conglomerado` bajo ese nombre literal.

---

## 3 · Dicotomizaciones y celdas

**Rama A:** `SINTOMA_GRAVE` = 1 si `es09`=1 (módulo `bx`, 2002/2005, §1.1); `BUSCA_PUBLICO` — no construible directamente de `cen10*` (§0.3); se pre-registra como **`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`** salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente. Celda de corroboración (no del mismo antecedente): `ENDIREH` `INSTITUCION_PUBLICA` (`p6_*_7`) vs. `INSTITUCION_PRIVADA` (`p6_*_8`), sobre el universo de mujeres que buscaron ayuda tras violencia — reportada aparte, nunca sumada a la celda de `R4.4` (antecedentes distintos, §1.2). Ponderador de esta celda: `fac_3b_px` (§1.3, v1.1) — declarado acotado a la subpoblación `bx` (`A-bis 4`).

**Rama B:** `NECESIDAD_ULTIMA` (`H0402`, categorías pendientes de codebook) y/o `ATENCION_REQUIRIO_X` (`H0409A-D`, pendiente de codebook para saber qué mide cada sufijo) como candidatos a `SINTOMA_GRAVE` — ya medida (§2.1, `L16`). `INSTITUCION_PUBLICA` = subconjunto de categorías de `u0201` que el codebook marque como público (IMSS/ISSSTE/SSA/Bienestar) vs. privado.

**Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que el resto de esta serie (`S4`/`S5`/`S8`).

---

## 4 · Falsador `B-bis`

| | Rama A (`ENNVIH`+`ENDIREH`, corroboración) | Rama B (`ENSANUT2024`) |
|---|---|---|
| **Signo esperado** | entre síntoma grave (`es09=1`), mayor proporción busca institución pública que privada (si `clave1`/`clave2` lo permiten, 2002 solamente) | entre quienes `H0409` marca como requiriendo mayor complejidad, mayor proporción en `u0201`=institución pública |
| **`CORROBORADA`** | proporción pública > proporción privada, IC95 excluye la paridad | ídem, sobre `u0201` |
| **`CONTRARIA`** | proporción pública < privada, IC95 excluye paridad en signo opuesto | ídem |
| **`NO-DISCRIMINA`** | IC95 contiene la paridad | ídem |
| **`NO-ESTIMABLE`** | **fila que `B-bis` exige:** si `clave1`/`clave2` (única vía a institución en Rama A) no alcanza para clasificar la muestra completa, o el numerador de alguna celda cae bajo 10, **o si el CHEQUEO DE CONSISTENCIA de §1.3 falla** (`n_no_nulo_gt0` de `fac_3b_px` menor que el de `fac_3a_px` o `fac_4_px` sobre el subconjunto `es09` no nulo), el veredicto de Rama A queda **sin construir** — la corroboración `ENDIREH` (§1.2) se reporta aparte, declarada como evidencia de que el contraste público/privado existe en el corpus, no como sustituto del falsador de `R4.4` | si `H0402`/`H0409` no discriminan gravedad tras abrir el codebook (por ejemplo, si son puramente categóricas sin gradiente de severidad), el veredicto de Rama B queda igual de `NO-ESTIMABLE`, declarado |

**Qué significaría corroborar cualquiera de las dos ramas.** Sería la primera falsación real de `R4.4` sobre la Rama A (§0.1; la Rama B ya corrió, `L16`, `NO-DISCRIMINA` — ver §2.1). Dado que las dos ramas ya traen `EXISTE-SATISFACE` sellado por actos distintos sin reconciliar (§0.2), corroborar Rama A **en el mismo sentido que predeciría un instrumento independiente** sería evidencia relevante — un segundo instrumento sobre la misma regla, aunque la Rama B ya midió y no discriminó.

**Reserva, declarada antes de medir.** Asociación transversal, sin identificación causal. El `PORQUE` ("la complejidad excede al consultorio") es mecanismo, no antecedente exigible — no se mide, mismo criterio que el resto de esta serie. Ninguno de los cortes de §3 está confirmado sin codebook; caja los declara al abrir, no los hereda de esta pieza a ciegas.

---

## 5 · `se_mueve_si`

**Rama A:** si entre quienes reportan síntoma grave (`es09=1`, 2002/2005) la proporción que acude a institución pública (vía `clave1`/`clave2`, 2002) **no es mayor** que la que acude a privada, la regla se rompe para esa rama. **Rama B (ya medida, `L16`):** `NO-DISCRIMINA` — el corte de severidad construido contra el codebook (hospitalización/urgencias vs. consulta externa/otro) no distingue institución pública vs. privada (ambas celdas ≈52%, IC95 solapado). Si Rama A cae por `NO-ESTIMABLE` (§4, incluido el fallo del chequeo de consistencia de §1.3), `se_mueve_si` de la regla completa queda sin poder evaluarse con la Rama A — hallazgo a reportar, no a forzar; la Rama B, medida, ya no sostiene el `ENTONCES` de la regla por sí sola.

**Fila B-bis (ponderador) — se_mueve_si.** El encargo de dirección que originó esta `v1.1` pedía citar aquí, verbatim, la `se_mueve_si` de la "fila 2" de `ACTO MAESTRA38-SELLO-2`. **Verificado antes de escribir esta fila — no existe tal texto en el repo.** `forense/encargos/2026-09-07-MAESTRA38-SELLO-2.md`, su propia sección `## CONSUMIDO`, declara explícitamente: *"Bloque B (filas 2-5, benchmark): NO ejecutado — el lanzamiento de esta tarea no pidió explícitamente 'con bloque B'; quedan `PENDIENTE-DE-MESA` sin movimiento, nota en `forense/hallazgos.md`."* Las filas 2-5 de `SELLO-2` (donde viviría la "fila 2") nunca se redactaron en prosa dentro de este repo — ni `canon/gobernanza-v1_15.md` (`ADR-363`, "dos incisos": fila 1 y fila 6, ninguna fila 2) ni `milpa/tramite-ola5-propuesta-v0.yaml` traen una entrada de fila 2. El hallazgo más cercano — `ACTO MAESTRA38-LOTE-CRUCE` (`ADR-371`, `FP-329`) midiendo que "las tres `se_mueve_si` de `SELLO-2 §B`" (`R7.7`, `R7.6` brazo proximidad, `R10.3`, condicionadas a `clien1n`/`clien1na`) **no se pueden disparar** porque esas variables no existen en LAPOP 2021/2023 — es de una **regla distinta** (`R7.x`/`R10.3`, cívico), no de `R4.4` (salud) que esta spec trata. No hay sustituto verbatim aplicable.

**En su lugar, declarado explícitamente como NO-verbatim:** la `se_mueve_si` de esta fila B-bis es el propio CHEQUEO DE CONSISTENCIA de §1.3, redactado por este acto: *si, sobre las filas de `p_es.dta` con `es09` no nulo, `n_no_nulo_gt0` de `fac_3b_px` resulta MENOR que el de `fac_3a_px` o que el de `fac_4_px`, la asignación libro→factor que esta spec adjudica es incorrecta — el falsador de la Rama A no corre con `fac_3b_px`, el proceso se PARA, y un acto sucesor re-adjudica el ponderador con el subconjunto real (no con el libro `bx` completo, que esta spec usa solo como evidencia indirecta, §1.3).* Esta cláusula es la más cercana, con evidencia real del repo, a lo que una `se_mueve_si` de "fila 2" habría dicho si hubiera llegado — pero no es una cita, y se declara así para que nadie la trate como verbatim de mesa.

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
| `ennvih1_2002_hogar_cb` **(nuevo en v1.1, no citado por v1.0)** | `ennvih/ehh02cb_all.zip` | ver `data/manifiesto.yaml` — codebook, deflate64 (`C1`: `zipfile` de Python lo rechaza limpio; `tar.exe` de Windows lo extrae relleno de ceros sin avisar — usar `zipfile-deflate64` o equivalente) |

**Rama B:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.stata.stata.zip` | `20a9fae339da3fa3fc6ce20e81b6b1cf32375b40baf5a876d760a15f01ec6aa9` |
| `utilizadores_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/utilizadores_ensanut2024_w.stata.stata.zip` | `b40a4dce264e657026b4046b07047031437a224182e373d27dde4a5e0360a563` |

`ENSANUT2024` trae cuestionarios PDF ya citados por actos anteriores (`MAESTRA37-L1`/`L3`) — no re-listados aquí.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `salud.atencion.grave` (`[MEDIA]`, línea 527) ni sella `MEDIBLE-COMO-ESTÁ`. No decide cuál de las dos ramas (`ENNVIH`/`ENDIREH` vs. `ENSANUT2024`) es la medición canónica de esta regla — declara la discrepancia (§0.2) para que dirección/mesa la resuelva, no la resuelve por su cuenta. No corrige `MAESTRA37-L3`/`L3-BIS` ni los retira — quedan `EXISTE-SATISFACE`/`CONFIRMADO SIN CAMBIO` como están. No reclasifica `salud.vacunacion.disponible` ni `comunicacion.inseguridad.ver_oir_callar` (`S7`/`S8`, mismo lote, piezas separadas). No toca `canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`. **No corre el chequeo de consistencia de §1.3** contra el subconjunto real `es09` no nulo — solo lo especifica y verifica que la versión disponible (libro `bx` completo) ya lo satisface; caja lo re-corre contra el subconjunto exacto antes de calcular una sola celda.

**Medición: NUBE, `ACTO MAESTRA38-N19` (este acto, redacción de la spec). La medición de la Rama A sigue pendiente de un acto `CAJA` sucesor** — a diferencia de `S7-L17 v1.1` (mismo lote, misma fecha), que registró un mapeo ya usado por una medición corrida, esta `v1.1` destraba una medición que **todavía no se ha corrido ni una vez**.

**El primer resultado que produzca este procedimiento es el que se reporta — de cada rama, por separado.**
