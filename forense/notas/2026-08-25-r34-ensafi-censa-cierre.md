# `ACTO R34-ENSAFI-CENSA` · cierre

**25/ago/2026 · entorno UBUNTU · modelo Opus · `SHA` de redacción `ba0a7e4` · `ADR-193` · CONTADOR: cero**

> **Qué hace este acto.** Abre `ENSAFI 2023` — el payload que `#359` dejó como única candidata
> `NO-ACCESIBLE` del censo de `B`/`C` de `R3.4` — y la censa contra los cuatro constructos que
> `FP-157` necesita. **No mide, no adjudica `FP-157`, no firma nada.**
>
> **Qué encuentra, en una línea.** Los cuatro constructos cierran en **`NO-ACCESIBLE`**, no en
> `NO-ENCONTRADO`: el microdato está completo y abierto, pero **ningún descriptor de `ENSAFI 2023`
> existe en ninguna raíz del corpus**, y sin él los 354 códigos `P`-numerados no son ni siquiera
> buscables por término. El censo de `#359` **no queda exhaustivo** — queda exhaustivo *hasta el
> techo del corpus*, que es una cosa distinta y se declara como tal.
>
> **Y encuentra una cosa que nadie había buscado.** Una sonda de solo-lectura (12 URLs, ningún
> byte guardado) localiza publicado y vivo hoy el **cuestionario** de `ENSAFI 2023`
> (`.../2023/doc/ensafi_2023_cuestionario.pdf`, `http=200`, **1 182 405 bytes**, `application/pdf`).
> Los actos previos buscaron el **`FD`** — que sigue en soft-404 — y no el cuestionario. El
> cuestionario es justamente donde vive el **texto verbatim del reactivo**, que es lo único que le
> falta a este censo. La opción (1) de `FP-157` («adquisición dirigida y acotada») deja de ser una
> apuesta sobre un descriptor incierto y pasa a ser **un archivo verificado de 1.18 MB**.
> **Este acto NO lo descarga** — el encargo lo prohíbe explícitamente y `data/manifiesto.yaml` está
> fuera de su perímetro. Lo entrega como receta `A.5` lista, con su URL sondeada hoy.

---

## §0 · ARRANQUE (`A.2`, tres partes) y compuertas `F0`

**1 · Repo.** Clon existente `/home/pc0/Modelado-Mexicano`. Caja del acto:
`/home/pc0/mm-r34-ensafi-censa`, rama `r34-ensafi-censa`, creada desde `ba0a7e4`.
*(La caja es del acto por la razón ya canonizada: el worktree principal está parado en
`ea22bdd` / `acto/cal-g3-puntual`, un árbol distinto; correr `F0` ahí produce premisas falsas.)*

**2 · `SHA`.** `ba0a7e4` verificado **igual** a `origin/main`:
`git rev-list --count ba0a7e4..origin/main` → **`0`**. `git merge-base --is-ancestor` → sí.
Sin refresco, sin drift.

**3 · Corpus.** `data/raw` → symlink a `/home/pc0/mm-corpus/raw` — **CORPUS COMPARTIDO**,
**321 entradas** de primer nivel, **718 archivos** en total bajo la raíz.
`data/raices.local.yaml` copiado a la caja (gitignorado) para que las tres raíces queden
configuradas y ninguna respuesta de `A.1` sea `raíz-no-configurada` por accidente de caja.

**4 · Firma de entorno, tres partes.**

| parte | valor medido |
|---|---|
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | **`sin_variable`** (esperado para UBUNTU) |
| sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` | **`200`** |
| `ls data/raw/` | montado, **321 entradas** — sin `PARO` |

**5 · Cero cifras del espejo.** Ninguna cifra de este documento se hereda de otro documento del
repo: todas se re-derivaron en esta sesión contra el árbol o contra el microdato, con el comando
al lado. Donde una cifra coincide con una previa, se dice que coincide.

### `F0` · `A.1` — verificación de payloads, una invocación por `--id`

`ENSAFI` tiene **un solo** id en el manifiesto. Derivación del universo, con conteo:
`grep -ain "ensafi" data/manifiesto.yaml` → **8 líneas** sobre **15 426**, todas de la misma
entrada (`data/manifiesto.yaml:3939`); control positivo del mismo comando sobre el mismo archivo,
`enif` → **95** líneas. *(El encargo anticipaba «6 menciones»; son 8 — misma entrada única, la
diferencia es de conteo, no de inventario.)*

Salida cruda, invocación única, sin colapsar las tres respuestas:

```
$ python3 tests/manifiesto.py --verifica --id ensafi2023_bd_csv_zip
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

ensafi2023_bd_csv_zip [data_raw]: COINCIDE -- sha256 y tamaño (5027338 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

**Las tres respuestas, cada una en cero salvo la que aplica:** `ausente=0` · `sin_configurar=0`
(raíz-no-configurada) · `no_coincide=0` (hash-discordante) · **`coincide=1`**.

### `F0` · `A.8` en fresco — qué ya existía, y dónde el encargo se queda corto

| premisa del encargo | verificada contra `ba0a7e4` | veredicto |
|---|---|---|
| `ensafi2023_bd_csv_zip` en `data/manifiesto.yaml:3939` | sí, línea exacta | **cierta** |
| «6 menciones `ensafi` sobre 15 426 líneas» | son **8** sobre 15 426, misma entrada única | **cierta en sustancia, imprecisa en el conteo** |
| «Censo `B`/`C` sobre `ENSAFI`: NO EXISTE» | `grep -acin "ensafi" forense/ficha-r34-condBC-v1_0.md` → **4** menciones, ninguna es anexo; los encabezados de la ficha (`grep -an "^## "`) son 10 y **ninguno** dice «Anexo». Control positivo: `enif` → **11** menciones en el mismo archivo | **cierta — sin `PARO`** |
| «`FP-157` ABIERTA» | `forense/firmas-pendientes.tsv`, columna `estado` = `ABIERTA` | **cierta** |
| «(única del tablero)» | `awk` sobre la columna `estado`: **2 `ABIERTA`** — `FP-157` **y `FP-159`** (más 136 `FIRMADA`, 16 `CERRADA`, 1 `CERRADA POR PREMISA REFUTADA`) | **falsa, y sin consecuencia** — `FP-159` es de otro acto (`PASE-FALSADORES`), disjunta de `R3.4` |
| «la única candidata `NO-ACCESIBLE` **por no abierta**» | **`ENSAFI` ya fue abierta dos veces**: `ABRIR-4` (8/ago) y `ACTO APERTURA-ENFIH-ENSAFI` (20/ago, `ADR-133`, `PR #302`) — `data/apertura-enfih-ensafi-v1_0.tsv` trae **4 filas `ENSAFI`** con sus 369 columnas leídas | **falsa en el diagnóstico, cierta en el efecto** |

**La corrección que importa, y es la premisa central del encargo.** `ENSAFI` **no** está
«sin abrir». Está abierta —dos veces, con el mismo resultado— y **cerrada por otra cosa**: le falta
el **descriptor**, no la apertura. La ficha `condBC` ya lo decía en su §3 (*«un `.csv` sólo aporta
nombres de variable, no el texto del reactivo»*, línea 68) y en la fila 10 de su tabla; lo que este
acto añade no es el diagnóstico sino su **verificación a nivel de bytes** —abrir el zip y contar—
en lugar de la inferencia. Sin `PARO`: el censo `B`/`C` sobre `ENSAFI` de verdad no existía, y es
lo que este acto entrega.

---

## §1 · El techo del instrumento, medido y no heredado (`A.4` · `A.13`)

**(a) El zip no trae descriptor.** `zipfile` sobre `data/raw/ensafi2023/ensafi_2023_bd_csv.zip`
(sha256 `c0594079…`, `COINCIDE`) → **4 entradas, las 4 `.csv`**:

| archivo | bytes | columnas | filas |
|---|---:|---:|---:|
| `TSDEM.csv` | 9 901 787 | 25 | 67 781 |
| `TVIVIENDA.csv` | 3 421 816 | 36 | 20 201 |
| `THOGAR.csv` | 5 190 647 | 55 | 20 448 |
| `TMODULO.csv` | 21 551 649 | 253 | 20 448 |
| **total** | | **369** | |

Ningún `.pdf`, ningún `.xlsx`, ningún diccionario. Las 369 columnas coinciden con las que
`APERTURA-ENFIH-ENSAFI` declaró el 20/ago; se re-contaron aquí, no se copiaron.

**(b) Tampoco lo trae ninguna raíz.** Barrido físico por nombre, con control positivo y conteo
de archivos examinados (`A.13`):

| raíz | archivos examinados | `*ensafi*` | control positivo |
|---|---:|---:|---|
| `data_raw` → `/home/pc0/mm-corpus/raw` | **718** | **2** (el directorio y el zip de datos) | `*_fd*` → **32** · `*enasic*` → **4** (incluye `enasic_2022_fd.xlsx`) |
| `descargas_mx` → `/mnt/c/Users/PC0/Descargas MX` | **122** | **0** | `*fd*` → **1** |
| `downloads` → `/mnt/c/Users/PC0/Downloads` | **147** | **0** | `*fd*` → **0** |
| **total** | **987** | **2, ninguno descriptor** | **32 descriptores de otras encuestas sí aparecen** |

El control positivo es del **patrón**, no sólo del comando: el mismo `find` que devuelve cero
descriptores de `ENSAFI` devuelve 32 descriptores de otras encuestas en la misma raíz.

**(c) Ni el árbol versionado tiene el texto.** `grep -rail "TMODULO"` (tabla exclusiva de `ENSAFI`)
sobre el árbol sin `.git` ni `forense/rescate/` → **53 archivos** (`--exclude` de esta misma
nota, que también lo menciona; 54 contándola), y ninguno mapea código
`P`-numerado a texto de pregunta: los que citan variables citan **nombres de columna derivada**
(`CONF_FINAN`, `IMPULSIVID`, `GRA_CONTROL`) y todos anotan explícitamente `[SIN TEXTO]`.
`forense/notas/2026-08-08-abrir4.md:161` ya lo había escrito verbatim: *«Sin diccionario, ninguno
de los ~360 códigos P-numerados (P5_1…P10_4_6) trae texto de pregunta recuperable en este corpus»*.
Universo del negativo: **1 960 archivos versionados**.

**Consecuencia formal, declarada antes de censar nada.** Bajo `A.4`, ningún constructo puede
sellarse `EXISTE-SATISFACE` en `ENSAFI 2023` con el corpus de hoy, porque el veredicto exige la
**pregunta verbatim** y la pregunta verbatim **no existe en el corpus para 354 de las 369
columnas**. El techo es del corpus, no del instrumento — que es exactamente la distinción que
`v2.2` fija entre *«no pude alcanzar la fuente»* y *«la fuente no tiene el dato»*.

---

## §2 · `F1` · El censo, constructo por constructo

**Mecanismo.** Barrido de términos sobre las **369 cabeceras** de las 4 tablas, leídas íntegras con
`zipfile`+`csv` (no `grep` de cadena sobre el binario). Fecha: 25/ago/2026.

**Control positivo del extractor, corrido en la misma pasada:** 12 términos de dominio financiero
(`AHORR`, `CREDIT`, `INGRES`, `SALARI`, `DEUD`, `ESTRES`, `BIENES`, `OPTIM`, `IMPULS`, `CONTROL`,
`ORIEN`, `DEPEN`) → **11 coincidencias** (`GTOS_AHORR`, `INGRESO_M`, `SALARIO_ENT`, `NIV_ESTRES`,
`NIV_BIENES`, `OPTIMISMO`, `IMPULSIVID`, `GRA_CONTROL`, `ORIEN_FUT`, `ORIEN_ACCI`, `DEPEN_SUM`).
El extractor lee.

### Tabla del censo

| # | constructo | términos barridos | reactivo hallado | veredicto `A.4` | universo declarado |
|---|---|---:|---|---|---|
| **C1** | **Percepción de riesgo fiscal / SAT / vigilancia al usar pagos o servicios digitales** — *la pieza que apaga `B`* | 16 (`SAT`, `FISC`, `IMPUEST`, `HACIEND`, `VIGIL`, `RASTRE`, `EVAS`, `DECLAR`, `AUTORID`, `GOBIER`, `PRIVAC`, `INFORMAL`, `FORMALIZ`, `REVIS`, `AUDIT`, `DATO`) | **ninguno** — 0 coincidencias | **`NO-ACCESIBLE`** | 369 cabeceras de `TSDEM`/`TVIVIENDA`/`THOGAR`/`TMODULO` leídas íntegras con `zipfile`+`csv`, 25/ago/2026; control positivo 11/12 términos financieros; los 354 códigos `P`-numerados restantes **no son buscables por término** porque no existe descriptor en ninguna de las 3 raíces (987 archivos examinados, 0 descriptores `ENSAFI`, 32 descriptores de otras encuestas como control) |
| **C2** | **Razones de no-uso de pagos/servicios financieros digitales** (*¿`CoDi` nombrado?*) | 15 (`CODI`, `SPEI`, `TRANSFER`, `DIGITAL`, `APP`, `CELUL`, `MOVIL`, `BANCA`, `TARJET`, `EFECTIV`, `PAGO`, `NOUSO`, `MOTIV`, `RAZON`, `INTERNET`) | **ninguno** — 0 coincidencias; **`CoDi` no aparece como cadena en ninguna cabecera** | **`NO-ACCESIBLE`** | ídem C1 |
| **C3** | **Fricción declarada** (dificultad, requisitos, fallas) | 11 (`DIFIC`, `REQUIS`, `FALLA`, `TRAMIT`, `COMPLIC`, `COMISION`, `COSTO`, `LEJOS`, `DISTANC`, `ESPERA`, `RECHAZ`) | **ninguno** — 0 coincidencias | **`NO-ACCESIBLE`** | ídem C1 |
| **C4** | **Confianza: canal personal vs. institucional** (*¿misma batería, mismos individuos?*) | 9 (`CONF`, `FIA`, `FAMILI`, `AMIG`, `VECIN`, `BANCO`, `INSTITU`, `PREST`, `TANDA`) | **1 candidato legible: `CONF_FINAN`** (`TMODULO`, binaria `{1,2}`, 20 448/20 448 no vacías) — **sin texto** | **`NO-ACCESIBLE`**, con **descarte estructural parcial del único candidato legible** | ídem C1, más el perfil de valores de `CONF_FINAN` medido en esta sesión sobre las 20 448 filas |

**El descarte parcial de C4, que sí se puede hacer sin el descriptor.** `CONF_FINAN` es **una sola
columna derivada binaria**. La conjunción que `C` necesita —canal personal **separado** del
institucional, **en la misma batería y sobre los mismos individuos**— exige por construcción
**dos ítems o más**. Una variable única no puede satisfacerla, cualquiera que sea su texto. Eso
descarta al único candidato legible **por forma**, no por contenido; no descarta a las baterías
`P`-numeradas, que siguen sin ser legibles. *(`CONF_FINAN` ya estaba clasificada
`EXISTE-NO-SATISFACE` para la necesidad 14 «puente `radio_confianza`» desde `ABRIR-4`; este acto no
la reabre ni la reclasifica — la evalúa contra otro constructo, el de `C`.)*

### Lo que el encargo pide y **sí** se puede contestar sin descriptor: respuesta única vs. múltiple

> *«…si es respuesta única o múltiple (el defecto que mató a `ENIF` para la conjunción de `B`
> — decláralo explícito)»*

El formato de respuesta **no** necesita el texto: se mide contando marcas por fila. Una pregunta de
respuesta **única** recodificada en dummies tiene exactamente **una** marca por fila; una de
respuesta **múltiple** tiene filas con **más de una**. Medido sobre `TMODULO` (20 448 filas), las
**18 baterías** del módulo:

| bloque | ítems | universo | filas con >1 marca | lectura |
|---|---:|---:|---:|---|
| `P5_23_*` (0/1) | 9 | 5 707 | 1 505 (26.4 %) | múltiple |
| `P7_5_*` (0/1) | 6 | 12 226 | 687 (5.6 %) | múltiple |
| `P8_5_*` (0/1) | 9 | 16 572 | 3 694 (22.3 %) | múltiple |
| `P8_6_*` (0/1) | 11 | 14 004 | 7 382 (52.7 %) | múltiple |
| `P5_2_*` (1/2) | 8 | 20 448 | 20 133 (98.5 %) | múltiple |
| `P5_18_*` (1/2) | 7 | 9 563 | 5 168 (54.0 %) | múltiple |
| `P6_1_*` (1/2) | 6 | 20 448 | 2 137 (10.5 %) | múltiple |
| `P6_2_*` (1/2) | 10 | 20 448 | 5 455 (26.7 %) | múltiple |
| `P6_5_*` (1/2) | 5 | 20 448 | 410 (2.0 %) | múltiple |
| `P6_6_*` (1/2) | 9 | 20 448 | 2 899 (14.2 %) | múltiple |
| `P6_10_*` (1/2) | 8 | 6 224 | 3 543 (56.9 %) | múltiple |
| `P6_11_*` (1/2) | 5 | 14 224 | 3 640 (25.6 %) | múltiple |
| `P7_2_*` (1/2) | 4 | 20 448 | 6 650 (32.5 %) | múltiple |
| `P7_6_*` (1/2) | 8 | 20 448 | 13 418 (65.6 %) | múltiple |
| `P8_2_*` (1/2) | 4 | 20 448 | 8 426 (41.2 %) | múltiple |
| `P8_3_*` (1/2) | 10 | 20 448 | 6 336 (31.0 %) | múltiple |
| `P9_3_*` (1/2) | 7 | 20 448 | 17 241 (84.3 %) | múltiple |
| `P10_4_*` (1/2) | 6 | 20 448 | 11 920 (58.3 %) | múltiple |

**Las 18 son de respuesta múltiple. Ninguna es «elige una».** Esto es un hallazgo con valor propio
y **prospectivo**: el defecto que descalificó a `ENIF` para la conjunción de `B` —una pregunta de
respuesta única, donde marcar un motivo excluye los demás y la conjunción no se puede construir—
**no aplica estructuralmente a ninguna batería de `ENSAFI`**. Si el descriptor llega y alguna de
estas baterías resulta ser el ítem fiscal o el de razones de no-uso, su formato de respuesta ya
está libre del obstáculo, medido de antemano.

### Universos del módulo, leídos del propio microdato

Los filtros del instrumento declaran a quién se le pregunta cada sección, sin necesidad de
descriptor (`1` = pasa el filtro):

| filtro | tabla | pasa | no pasa | vacío |
|---|---|---:|---:|---:|
| `FILTRO_S4_1` | `THOGAR` | 3 107 | 17 341 | — |
| `FILTRO_S5_1` | `TMODULO` | 11 311 | 9 137 | — |
| `FILTRO_S5_2` | `TMODULO` | 14 050 | 6 398 | — |
| `FILTRO_S5_3` | `TMODULO` | 5 258 | 15 190 | — |
| `FILTRO_S5_3_1` | `TMODULO` | 6 107 | 13 319 | 1 022 |
| `FILTRO_S5_4` | `TMODULO` | 5 707 | 14 741 | — |
| `FILTRO_S6_1` | `TMODULO` | 10 732 | 9 716 | — |
| `FILTRO_S6_2` | `TMODULO` | 9 049 | 11 399 | — |

Cadena estructural verificada: `FILTRO_S5_4 = 1` → **5 707**, exactamente el universo de la batería
`P5_23_*`. Los filtros **son** los universos, y están completos; lo que falta es saber **qué**
filtran.

### Candidatos estructurales, nombrados y **no adjudicables**

Cuatro bloques tienen la **forma** de una batería de motivos («marca todas las que apliquen», sobre
un subgrupo filtrado): `P5_23_1..9` (universo 5 707), `P7_5_1..6` (12 226), `P8_5_1..9` (16 572),
`P8_6_01..11` (14 004). **Ninguno se asigna a `C1`, `C2` ni `C3`.** Asignar una batería a un
constructo por su forma, sin su texto, es exactamente la **sustitución de constructo** que `ADR-25`
creó y `ADR-37` corrigió; se nombran aquí para que el acto que tenga el descriptor sepa dónde
mirar primero, y por ninguna otra razón.

---

## §3 · Ponderador y diseño (lo que `F2` pide para una spec-candidata)

`data/diseno-muestral.yaml:977-997`, `ENSAFI` → **`estado: PENDIENTE`**, y por la misma causa:

- **Ponderadores:** `FAC_VIV` (`TVIVIENDA`), `FAC_HOG` (`TSDEM`, `THOGAR`), `FAC_ELE` (`TMODULO`)
  **existen como columnas** — verificado de nuevo en esta sesión: `FAC_ELE` no vacío en
  **20 448/20 448** filas de `TMODULO`, 5 890 valores distintos.
- **Estrato / UPM:** `EST_DIS` (277 distintos) y `UPM_DIS` (2 915 distintos) existen en las cuatro
  tablas, no vacíos.
- **La reserva, que es la misma de todo este acto:** sin descriptor **no se puede citar la
  definición de universo de ninguno de los tres**, y el proyecto no la infiere de otras encuestas
  del INEGI. `RECENSO-DISEÑO-14` (24/ago, `ADR-149`) ya dejó esta fila en `PENDIENTE` por falta de
  **descriptor**, no de payload. Este acto la deja donde está y **no la toca** — está fuera de su
  perímetro.

**Traducción para `FP-157`:** aunque el reactivo apareciera mañana, la spec de `B` necesitaría el
descriptor **dos veces** — una para el texto del reactivo y otra para la definición del ponderador.
Es el mismo archivo. El costo no se duplica.

---

## §4 · Sonda de solo-lectura: el cuestionario **está publicado**

> **Alcance declarado.** Sonda, **no adquisición**. `curl -sL -o /dev/null`, sólo código de estado,
> tamaño y `content-type`; **ningún byte se guardó**, `data/raw/` no se tocó, `data/manifiesto.yaml`
> no se tocó. El encargo prohíbe descargar y este acto **no descarga**. La sonda se corre porque la
> opción (1) de `FP-157` depende enteramente de si el descriptor es obtenible, y mesa no puede
> decidirlo sin ese dato.

**Firma del soft-404 del portal, establecida con control negativo deliberado:** una URL inventada
(`NO_EXISTE_CONTROL_NEGATIVO.pdf`) devuelve `http=200`, **2 263 bytes**, `text/html`. Ése es el
patrón de «no existe» de `inegi.org.mx` — **no** un 404 honesto. Todo resultado de 2 263 bytes /
`text/html` es una ausencia.

**12 URLs sondeadas, 25/ago/2026:**

| URL (bajo `www.inegi.org.mx/contenidos/programas/…`) | `http` | bytes | tipo | lectura |
|---|---:|---:|---|---|
| **`ensafi/2023/doc/ensafi_2023_cuestionario.pdf`** | **200** | **1 182 405** | **`application/pdf`** | **EXISTE** |
| `ensafi/2023/doc/ensafi_2023_fd.xlsx` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/microdatos/ensafi_2023_fd.xlsx` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi2023_cuestionario.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi_2023_descripcion_archivos.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi_2023_fd.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/fd_ensafi_2023.xlsx` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi_2023_diseno_muestral.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi_2023_cuestionario_basico.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `ensafi/2023/doc/ensafi_2023_glosario.pdf` | 200 | 2 263 | `text/html` | soft-404 |
| `enasic/2022/doc/enasic_2022_fd.xlsx` *(control: ese `FD` sí está en el corpus)* | 200 | 2 263 | `text/html` | soft-404 — su ruta real es otra |
| `ensafi/2023/doc/NO_EXISTE_CONTROL_NEGATIVO.pdf` *(control negativo)* | 200 | 2 263 | `text/html` | soft-404 |

**1 de 12 devuelve un archivo real.** Y es el que importa.

**Por qué nadie lo había encontrado.** Todos los actos anteriores —`B-3` (4/ago), `M-3` (5/ago),
`ABRIR-4` (8/ago), `APERTURA-ENFIH-ENSAFI` (20/ago), `RECENSO-DISEÑO-14` (24/ago), `FP-115`(c),
la ficha `condBC`— buscaron el **`FD`**, siguiendo el patrón `enasic_2022_fd.xlsx` /
`enfih_2019_fd.xlsx`. El `FD` de `ENSAFI` **efectivamente no está publicado** bajo ningún patrón
probado, y esa conclusión sigue en pie. Pero el **cuestionario** es un artefacto distinto, bajo
otro patrón de nombre, y **contiene precisamente lo que a este censo le falta**: el texto verbatim
de cada reactivo, con sus opciones de respuesta y sus pases de filtro. El descriptor y el
cuestionario responden preguntas distintas; el censo de `B` necesita el segundo, y los actos
buscaron el primero.

**Receta `A.5`, NO ejecutada aquí.** Un acto sucesor con perímetro que incluya `data/raw/` y
`data/manifiesto.yaml`:

1. `curl -sL -o data/raw/ensafi2023/ensafi_2023_cuestionario.pdf "https://www.inegi.org.mx/contenidos/programas/ensafi/2023/doc/ensafi_2023_cuestionario.pdf"`
2. Verificar tamaño ≈ 1 182 405 bytes y `%PDF` en los primeros bytes (la firma de soft-404 es
   2 263 bytes de `text/html` — si el tamaño no coincide, **no** es el cuestionario).
3. Registrar en `data/manifiesto.yaml` con `sha256`, `url_origen`, `licencia` (Términos de Libre
   Uso del INEGI) y `entorno_descarga`; `tests/manifiesto.py --verifica --id <nuevo id>`.
4. Extraer texto (`pdftotext -layout`) y **re-correr este censo**: los 354 códigos `P`-numerados
   pasan de no-buscables a buscables, y las cuatro filas de `C1`-`C4` pasan de `NO-ACCESIBLE` a un
   veredicto real — `EXISTE-SATISFACE` o `EXISTE-NO-SATISFACE`, según lo que diga el texto.
5. Reserva honesta que viaja con la receta: **el cuestionario no trae los nombres de columna**. El
   puente código↔reactivo tendrá que armarse por posición y por sección (`P5_*` ↔ Sección 5, etc.),
   con las tasas de no-respuesta y los universos de `FILTRO_S*` de §2 como verificación cruzada. Es
   trabajo, y es **posible**; sin el `PDF` no lo es en absoluto.

---

## §5 · Entrega — qué se propone y qué no

**No hay spec-candidata**, porque ningún constructo alcanzó `EXISTE-SATISFACE`. La rama de `F2`
que aplica es la segunda, **con una corrección**: el encargo la anticipaba como
`NO-ENCONTRADO`/`EXISTE-NO-SATISFACE`, que dejaría el censo de `#359` *exhaustivo*. Lo medido es
**`NO-ACCESIBLE`**, que es la tercera respuesta del vocabulario de `A.4` y **no** deja el censo
exhaustivo: deja constancia de que el terreno **no se puede recorrer con el corpus de hoy**, y
nombra el archivo exacto que lo abriría.

**Lo que este acto entrega a `FP-157`, y es lo que se le pidió:**

1. **`ENSAFI` no es una candidata sin abrir.** Está abierta —tres veces ya— y el obstáculo es de
   procedencia documental, no de acceso al microdato. La frase de `FP-157` *«hasta que exista,
   `ENSAFI` no está censada sino sin abrir»* queda **corregida**: está abierta y censada hasta el
   techo del corpus, y el techo tiene nombre.
2. **El costo de la opción (1) baja y se vuelve verificable.** Deja de ser «adquirir un descriptor
   cuyo patrón de URL está en soft-404» y pasa a ser **un `PDF` de 1.18 MB, sondeado vivo hoy, con
   URL exacta y firma de tamaño para distinguirlo del soft-404**.
3. **Un obstáculo conocido queda descartado de antemano.** Las 18 baterías de `ENSAFI` son de
   respuesta múltiple; el defecto que descalificó a `ENIF` para la conjunción de `B` no aplica aquí.
4. **Lo que sigue sin saberse, dicho sin adorno.** Que el cuestionario exista **no** implica que el
   reactivo fiscal exista. `ENSAFI` es una encuesta de *salud financiera* —deuda, ahorro, seguros,
   remesas, capacidades—, y que mida percepción de riesgo fiscal/vigilancia **al usar un medio de
   pago digital** es **plausible a priori y no verificado**. El `PDF` puede confirmarlo o cerrarlo
   en firme; hoy no se sabe, y este acto no lo simula.

**No se adjudica `FP-157`.** No se propone veredicto para `B` ni para `C`; la propuesta de `#359`
(`B` `INDETERMINADA`, `C` `INDETERMINADA`) queda **intacta y sin tocar**. `R3.4` sigue sin
veredicto. **Base medida de `B`/`C`: sigue en `0 de 2`.** **CONTADOR: cero.**

---

## §6 · Perímetro, concurrencia y verificación de salida

**Perímetro respetado, lista cerrada:** `forense/ficha-r34-condBC-v1_0.md` (append) ·
`forense/notas/2026-08-25-r34-ensafi-censa-cierre.md` (este archivo) ·
`canon/gobernanza-v1_15.md` (`ADR-193`) · `canon/estado-programa-v1_10.md` (línea `R3.4` y conteo
de `ADR`) · `forense/firmas-pendientes.tsv` (**sólo** la enmienda a `FP-157`) ·
`forense/encargos/2026-08-25-R34-ENSAFI-CENSA.md` (archivado, `CONSUMIDO`) ·
`data/raw/` **en lectura**. Nada fuera de la lista se tocó: `tests/aceptacion_r3_4.py` intacto,
`data/manifiesto.yaml` intacto, `data/diseno-muestral.yaml` intacto, `data/` sin archivos nuevos
(por eso la tabla del censo vive en esta nota y no en un `.tsv`).

**Concurrencia.** `CORRE-R10.1` y `SPEC-EXPCOMP-BBIS` corren en paralelo; Codex-CLI, disjunto.
`ADR-193` se candidateó contra el máximo re-derivado en esta sesión —
`grep -aoE "ADR-[0-9]+" canon/gobernanza-v1_15.md | grep -oE "[0-9]+" | sort -n | uniq | tail`
→ `188 189 190 191 192`, sin huecos → **193**. **Se re-deriva y se renumera al fusionar si
colisiona** — renumera quien fusiona segundo.

**Suite (`--baseline`, nunca `--freeze`).** Corrida en la caja del acto:
**19 `FAIL` · 129 `WARN`**, **LÍNEA BASE: VERDE** — nada nuevo frente a `tests/baseline.json`
(`HEAD` congelado `e24d033`). Coincide con la cifra que `estado:303` cita para el 25/ago.

**Encargo: `CONSUMIDO`.**
