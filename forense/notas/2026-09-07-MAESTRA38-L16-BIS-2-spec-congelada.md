# ACTO MAESTRA38-L16-BIS-2 · COMMIT-1 · spec congelada citada antes de abrir un solo `.dta`

**Acto:** `MAESTRA38-L16-BIS-2` — MIDE-RAMA-A-ENNVIH-CONTRA-S6-v1_1.
**Fecha:** 7 de septiembre de 2026. **Entorno:** UBUNTU (caja, corpus montado).
**Rama base:** `origin/main` = `3d6dee33` (la cabecera del encargo citaba `7e0fb716`, PR #583; la punta avanzó a `3d6dee33` entre la redacción y el lanzamiento — se declara, no se corrige hacia atrás).

Este commit se escribe **antes de abrir un solo `.dta`**. Nada de lo que sigue se re-escribe después de ver el dato.

---

## (i) Nombre estable y sello de la spec

- **Nombre estable:** `prereg-caja-S6-L16` · **v1.1**
- **Archivo:** `forense/prereg-caja/S6-L16-spec-v1_1.md`
- **sha256:** `7a0120a3a471fe81a732035dec6c2a9ed292d9b722cc408248eaec96d2e6643a`
- **Compuerta verificada por producto, no por rótulo:** `git show origin/main:forense/prereg-caja/S6-L16-spec-v1_1.md | sha256sum` devolvió exactamente ese valor contra `origin/main` = `3d6dee33`. CUMPLIDA.

Este acto **no reescribe ni enmienda** la spec. La consume.

---

## (ii) Transcripción verbatim de la spec — §1.3, §3, §4, §6 (Rama A)

### §1.3 · Universo y ponderador — Rama A (REESCRITO en v1.1)

> **Universo de `bx`: subpoblación, declarada como tal — nunca contra un marginal poblacional (A-bis 4).** El módulo `bx` de `ENNVIH` es el **libro Proxy**: lo responde un informante del hogar **en nombre de** miembros del hogar que están ausentes al momento del levantamiento (migrantes, principalmente), no el universo completo de personas del hogar. `p_portad.dta` (ola 2002) tiene **1 903 filas** — la cobertura del libro Proxy, verificada contra `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (comentario de cabecera: *"libro bx = ehh02dta_bx/p_portad.dta (1903 filas, Proxy)"*), frente a **8 441 filas** del libro hogar (`c_portad.dta`, libro C) y **35 664 folios de hogar** que sí resuelven contra el join de ponderador (ver abajo). Por `A-bis 4` (`instrucciones-proyecto-v2_12.md`, Bloque A-bis, regla 4, verbatim: *"Un estimando restringido a una subpoblación no se compara contra uno poblacional... Se recalcula el marginal restringido al mismo universo, o se declara el resultado como acotado a esa subpoblación"*): toda celda que este falsador produzca sobre `bx` se declara **acotada a la subpoblación de miembros ausentes respondida por proxy** — nunca se reconcilia ni se compara contra una proporción del padrón completo de `ENNVIH`, ni contra la Rama B (`ENSANUT2024`, universo distinto por diseño). Si caja necesita un marginal de referencia, lo recalcula restringido al mismo universo `bx`, no al universo general.
>
> **Ponderador: `fac_3b_px`.** Fuente: `ennvih1_2002_ponderador` (`data/manifiesto.yaml`, `ennvih/ehh02w_all.zip`), archivo interno `ehh02w_all/ehh02w_bx.dta`. Adjudicado sobre los otros dos candidatos ambiguos que `ADR-357` había dejado sin resolver, con la evidencia que `ACTO MAESTRA38-C1` levantó (`data/ennvih2002-ponderadores-candidatos-v1_0.tsv`, verificado de nuevo al redactar esta spec):
>
> | candidato | libro | `n_no_nulo_gt0` | criterio |
> |---|---|---|---|
> | `fac_3a_px` | `bx` (`ehh02w_bx.dta`) | 21 631 | descartado — mismo libro, menor cobertura que `fac_3b_px` |
> | **`fac_3b_px`** | **`bx`** (`ehh02w_bx.dta`) | **21 645** | **adjudicado** — mayor `n_no_nulo_gt0` de los tres candidatos del libro `bx`, misma etiqueta verbatim que los otros dos (`'FACTOR DE EXPANSIÓN LIBRO PROXY'`), pero el que más observaciones pondera con peso positivo |
> | `fac_4_px` | `bx` (`ehh02w_bx.dta`) | 9 037 | descartado — cobertura muy inferior (≈42% de `fac_3b_px`) |
>
> Los tres candidatos comparten la etiqueta verbatim `'FACTOR DE EXPANSIÓN LIBRO PROXY'` — no se distinguen por nombre, solo por `n_no_nulo_gt0` y por el hecho medido de que ninguno de los 11 codebooks de `ennvih/ehh02cb_all.zip` menciona la cadena `'fac'` (`C1`, verificado, control positivo 340 376 B de texto extraído). El documento que explica los tres es `ennvih/calculo-de-factores-de-expansion.pdf` §1.2 — caja lo abre si necesita la fórmula exacta; esta spec no la re-deriva.
>
> **Llave de join: `folio`/`ls`, normalizada a entero ANTES de unir — sin esto, el join da 0.** Hallazgo de `C1`, verificado de nuevo aquí contra `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (comentario de cabecera, verbatim): *"En `ehh02w_all.zip` `folio` es cadena con ceros a la izquierda (`'00001000'`) y en el microdato es `float64` (`2000.0`): sin normalizar, TODOS los joins dan 0 — resultado falso, no hallazgo."* Normalizando ambos lados a entero (`int(folio)`, sin ceros a la izquierda, sin punto decimal), el join real produce **1 903 de 1 903** filas del libro Proxy resueltas contra el ponderador, y **35 664** folios de hogar resueltos contra el libro C — cifras que `C1` ya midió y esta spec hereda sin re-correrlas. Caja **no** intenta el join con `folio` sin normalizar: el resultado (0 filas) no es un hallazgo de que el ponderador no aplica, es el bug ya documentado.
>
> **La rama directa `b3b` usa `fac_3b` (sin `_px`) y se reporta POR SEPARADO de `bx` — nunca agrupados.** El módulo `b3b` (`iiib_es.dta`, etiqueta "SERIO", §1.1) tiene su propio ponderador, `fac_3b` (sin sufijo `_px`), archivo `ehh02w_all/ehh02w_b3b.dta`, `n_no_nulo_gt0 = 19 809` — un archivo, una etiqueta ("FACTOR DE EXPANSIÓN LIBRO 3B") y una cobertura de universo **distintos** de `fac_3b_px`. El parecido de nombre (`fac_3b` vs `fac_3b_px`) es la trampa exacta que esta spec existe para evitar: `bx`/`fac_3b_px` mide sobre la subpoblación Proxy (miembros ausentes, etiqueta "GRAVE"); `b3b`/`fac_3b` mide sobre el universo directo del libro `3b` (miembros presentes, etiqueta "SERIO"). Agruparlos sumaría dos universos con dos ponderadores distintos bajo una sola celda — exactamente el error que `A-bis 4` prohíbe. Si caja corre ambas ramas (`bx` y `b3b`), **reporta dos filas separadas**, cada una con su propio ponderador y su propia declaración de subpoblación.
>
> **CHEQUEO DE CONSISTENCIA OBLIGATORIO — se corre ANTES de calcular una sola celda; si falla, el proceso se PARA.** Sobre las filas de `p_es.dta` con `es09` no nulo (el universo real del falsador, no las 35 677 filas de persona-observación de todo el libro `bx` que sí discriminan por `n_no_nulo` pero no por respuesta a `es09` específicamente — ver la nota de `C1` sobre por qué `n_no_nulo` no discrimina y hay que usar `n_no_nulo_gt0`), `n_no_nulo_gt0` de `fac_3b_px` debe ser **mayor o igual** que el de `fac_3a_px` **y** que el de `fac_4_px`. Pseudocódigo/comando que caja corre:
>
> ```python
> import pyreadstat
> df, meta = pyreadstat.read_dta("ehh02w_all/ehh02w_bx.dta")
> p_es, _ = pyreadstat.read_dta("ehh02dta_all/ehh02dta_bx/p_es.dta")
> folios_es09 = set(int(f) for f in p_es.loc[p_es["es09"].notna(), "folio"])
> df["folio_int"] = df["folio"].astype(int)
> sub = df[df["folio_int"].isin(folios_es09)]
> n_3b_px = (sub["fac_3b_px"].fillna(0) > 0).sum()
> n_3a_px = (sub["fac_3a_px"].fillna(0) > 0).sum()
> n_4_px  = (sub["fac_4_px"].fillna(0) > 0).sum()
> assert n_3b_px >= n_3a_px and n_3b_px >= n_4_px, "PARA: la asignación libro→factor es incorrecta"
> ```
>
> **Este acto no corre el chequeo contra el subconjunto exacto `es09` no nulo** (no abre microdato, NUBE sin corpus) — pero la versión ya medida por `C1` sobre el libro `bx` completo (35 677 filas de persona, `n_no_nulo_gt0`: `fac_3b_px=21 645` ≥ `fac_3a_px=21 631` ✔ y ≥ `fac_4_px=9 037` ✔) **ya satisface la desigualdad**, con margen estrecho contra `fac_3a_px` (14 observaciones de diferencia) y margen amplio contra `fac_4_px`. Si el subconjunto restringido a `es09` no nulo invierte el orden entre `fac_3b_px` y `fac_3a_px` (el margen de 14 es lo bastante estrecho para que eso sea posible), **la asignación libro→factor es incorrecta y el proceso se PARA** — caja no continúa con `fac_3b_px` sin volver a correr este chequeo sobre el subconjunto real.

### §3 · Dicotomizaciones y celdas

> **Rama A:** `SINTOMA_GRAVE` = 1 si `es09`=1 (módulo `bx`, 2002/2005, §1.1); `BUSCA_PUBLICO` — no construible directamente de `cen10*` (§0.3); se pre-registra como **`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`** salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente. Celda de corroboración (no del mismo antecedente): `ENDIREH` `INSTITUCION_PUBLICA` (`p6_*_7`) vs. `INSTITUCION_PRIVADA` (`p6_*_8`), sobre el universo de mujeres que buscaron ayuda tras violencia — reportada aparte, nunca sumada a la celda de `R4.4` (antecedentes distintos, §1.2). Ponderador de esta celda: `fac_3b_px` (§1.3, v1.1) — declarado acotado a la subpoblación `bx` (`A-bis 4`).
>
> **Rama B:** `NECESIDAD_ULTIMA` (`H0402`, categorías pendientes de codebook) y/o `ATENCION_REQUIRIO_X` (`H0409A-D`, pendiente de codebook para saber qué mide cada sufijo) como candidatos a `SINTOMA_GRAVE` — ya medida (§2.1, `L16`). `INSTITUCION_PUBLICA` = subconjunto de categorías de `u0201` que el codebook marque como público (IMSS/ISSSTE/SSA/Bienestar) vs. privado.
>
> **Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que el resto de esta serie (`S4`/`S5`/`S8`).

### §4 · Falsador `B-bis` (columna Rama A, verbatim)

> | | Rama A (`ENNVIH`+`ENDIREH`, corroboración) |
> |---|---|
> | **Signo esperado** | entre síntoma grave (`es09=1`), mayor proporción busca institución pública que privada (si `clave1`/`clave2` lo permiten, 2002 solamente) |
> | **`CORROBORADA`** | proporción pública > proporción privada, IC95 excluye la paridad |
> | **`CONTRARIA`** | proporción pública < privada, IC95 excluye paridad en signo opuesto |
> | **`NO-DISCRIMINA`** | IC95 contiene la paridad |
> | **`NO-ESTIMABLE`** | **fila que `B-bis` exige:** si `clave1`/`clave2` (única vía a institución en Rama A) no alcanza para clasificar la muestra completa, o el numerador de alguna celda cae bajo 10, **o si el CHEQUEO DE CONSISTENCIA de §1.3 falla** (`n_no_nulo_gt0` de `fac_3b_px` menor que el de `fac_3a_px` o `fac_4_px` sobre el subconjunto `es09` no nulo), el veredicto de Rama A queda **sin construir** — la corroboración `ENDIREH` (§1.2) se reporta aparte, declarada como evidencia de que el contraste público/privado existe en el corpus, no como sustituto del falsador de `R4.4` |
>
> **Reserva, declarada antes de medir.** Asociación transversal, sin identificación causal. El `PORQUE` ("la complejidad excede al consultorio") es mecanismo, no antecedente exigible — no se mide, mismo criterio que el resto de esta serie. Ninguno de los cortes de §3 está confirmado sin codebook; caja los declara al abrir, no los hereda de esta pieza a ciegas.

### §6 · Archivos que la caja necesita abrir — Rama A, verbatim

> | id de manifiesto | archivo | sha256 |
> |---|---|---|
> | `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
> | `ennvih2_2005_hogar_dta` | `ennvih/ehh05dta_all.zip` | `fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a` |
> | `ennvih3_2009_hogar_dta` | `ennvih/ehh09dta_all.zip` | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` |
> | `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | `bbe8006844f715c19b724ebb74f1408c4cfa07e2efdfe7d6748b5182ef214587` |
> | `ennvih3_2009_ponderador_transversal` | `ennvih/ehh09w_all.zip` | `e7929b49a7cd4f1eae5aa17da77c7eea4794d0f26265fbd40dde5e9c8e3ef8b8` |
> | `endireh_2016_bd_mujeres_endireh2016_sitioinegi_spss` | `endireh2016/bd_mujeres_endireh2016_sitioinegi_spss.zip` | `d198b9022d5727d24cddccdfd019c749ca42acc5d3f3e86a5d67e40ebe6eff3a` |
> | `ennvih1_2002_hogar_cb` **(nuevo en v1.1, no citado por v1.0)** | `ennvih/ehh02cb_all.zip` | ver `data/manifiesto.yaml` — codebook, deflate64 (`C1`: `zipfile` de Python lo rechaza limpio; `tar.exe` de Windows lo extrae relleno de ceros sin avisar — usar `zipfile-deflate64` o equivalente) |

`ennvih1_2002_hogar_cb` en `data/manifiesto.yaml`: `archivo: ennvih/ehh02cb_all.zip`, `sha256: a3220412505d6684e50548bdd1e01ce816d3af99ed846e4e27f30f35e9b506b2`, 2 195 863 B.

---

## (iii) IC95 — procedimiento y semilla, declarados antes de ver el dato

- **IC95 por bootstrap con la UNIDAD DE REMUESTREO = HOGAR, dentro de estrato.** Se remuestrean hogares (llave `folio` normalizada a entero) con reemplazo, dentro de cada estrato, conservando el número de hogares por estrato; todas las personas de un hogar sorteado entran juntas. La proporción se recalcula ponderada (`fac_3b_px` para el brazo `bx`; `fac_3b` para el brazo `b3b`) en cada réplica.
- **Réplicas:** 2 000 por celda.
- **Semilla declarada:** `20260907`.
- **IC95** = percentiles 2.5 y 97.5 de la distribución de réplicas. El contraste público−privado se bootstrapea sobre la misma réplica (diferencia pareada por réplica), y la paridad es el 0 de esa diferencia.
- Si el estrato no está disponible en el archivo de ponderador, se declara y se bootstrapea por hogar sin estratificar — se dice en COMMIT-2, no se sustituye en silencio.

## Brazos que este acto reporta POR SEPARADO (§1.3)

1. **Brazo `bx`** — `ehh02dta_all/ehh02dta_bx/p_es.dta`, `es09` («HA TENIDO PROBLEMA SALUD GRAVE»), ponderador `fac_3b_px` de `ehh02w_all/ehh02w_bx.dta`, universo declarado **acotado a la subpoblación Proxy (miembros ausentes)**.
2. **Brazo `b3b`** — `ehh02dta_all/ehh02dta_b3b/iiib_es.dta`, `es09` («HA TENIDO PROBLEMA SERIO SALUD»), ponderador `fac_3b` de `ehh02w_all/ehh02w_b3b.dta`, universo directo del libro 3B.

**Nunca agrupados, nunca promediados.** Ola: **solo 2002** (la spec restringe `clave1`/`clave2` a 2002).

---

## (iv) Cierre

**El primer resultado que produzca este procedimiento es el que se reporta.**
