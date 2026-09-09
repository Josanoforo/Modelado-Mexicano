# R-ENVIPE-SERIE-DBF · Pre-registro por ola de los tres árbitros `R` de ENVIPE en formato DBF (olas 2012, 2013, 2015)

### `prereg-caja-R-ENVIPE-SERIE-DBF` · **v1.0** · 9 de septiembre de 2026

> | | |
> |---|---|
> | **QUÉ ES** | La **extensión por ola** de `prereg-caja-R-ENVIPE-SERIE` a las tres olas que viven en payloads DBF. Fija, por ola y leyendo el descriptor de esa ola, el reactivo, el catálogo de códigos, la partición de `BPCOD`, las columnas físicas de diseño y ponderador, y la tabla. |
> | **QUÉ NO ES** | **No edita la spec sellada del trío CSV**: `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md` (`sha256 b9a29cf6…`) queda intacta byte a byte. Esto es **sucesión, no reescritura**. No es re-lectura de los dictámenes `R` de GEN1: `corridas-R/CIV-M-01.json` / `-02` / `-04` son **control positivo calculado DESPUÉS de sellar, por script aparte**. No adjudica el duelo, no mueve `tier`, no adopta ningún `R`. |
> | **ACTO** | `ACTO GEN2-R-SERIE-DBF`, 9/sep/2026, CAJA (Ubuntu) con corpus montado, Opus, sobre `4497029`. |
> | **CONGELADO** | En el `COMMIT-1`, **antes de abrir un solo registro de microdato**. |

---

## 0 · Contaminación declarada (`ADR-46`)

Al congelar, esta sesión **ya había leído** los tres puntos `R` de GEN1 —
`0.25899878251638075` (2012) · `0.24339981393062482` (2013) ·
`0.24366832225578466` (2015)— porque el encargo los cita y porque el A.8 del
ejecutor abrió los tres JSON para verificar que existen y están `COMPUTADO`.

Nada de lo que esta spec fija se elige para acercarse ni para alejarse de esos
valores. La codificación, el universo, el ponderador y el diseño se copian
**verbatim** de `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`
(`sha256 cf5dfb18…`), anterior a esta sesión; la variable y la escala, de
`espec-R-ciega-v1_2.tsv` (`sha256 b2dacd8a…`). Lo único que esta spec añade es
**arqueología de descriptores**: qué se llama cómo en cada libro.

**El primer resultado que produzca este procedimiento es el que se reporta.**

Lo que esta sesión **no** abrió al congelar: ningún registro de los tres
`.dbf`, `tools/arbitra.py`, y ningún `data/corrida0/CALC-R-*/resultados.json`.
Lo que sí abrió: el manifiesto, las cabeceras de campo de los `.dbf` (que son
metadato, no microdato), los tres descriptores (`FD_ENVIPE_2012.xls`,
`FD_ENVIPE13.xlsx`, `fd_envipe2015.pdf`) y la lista de miembros de los tres ZIP.

⚠️ **La premisa (3) del encargo sobre el inventario NO se sostiene contra el
árbol, y se corrige aquí.** El encargo declara que
`data/inventario-reactivos-v1_2.tsv` «trae 0 filas `BP1_2x` para `envipe_2013` y
`envipe_2015`» y que «el inventario NO cubre los payloads DBF». Medido:

| instrumento | filas en el inventario | filas `BP1_2*` | `BP1_23` | `texto_reactivo` no vacío |
|---|---|---|---|---|
| `envipe2012` | 400 | 12 | 1 | **0** |
| `envipe2013` | 419 | 11 | 1 | **0** |
| `envipe2015` | 485 | 11 | 1 | **0** |

El inventario **sí** cubre las tres olas DBF a nivel de **presencia de columna**
(`metodo = INSPECT_ZIP`, `universo_declarado = PRESENTE_EN_DATA_RAW`), y trae
`BP1_23`, `BP1_20`, `BPCOD`, `FAC_DEL` y las columnas de diseño **con su nombre
correcto por ola** —`EST`/`UPM` en 2012 y 2013, `EST_DIS`/`UPM_DIS` en 2015—.
Por eso `corrida0 spec-check` verifica las seis columnas de cada `CALC` contra
él y da **6 OK · 0 FAIL en los tres**: es un control positivo mecánico que el
encargo daba por no disponible.

Lo que el inventario **no** trae es `texto_reactivo`: está **vacío en las 1 304
filas** de las tres olas. Es decir, inventaría **nombres de columna, no
reactivos**. Por lo tanto la instrucción operativa del encargo sigue siendo
correcta por la razón que importa —el catálogo de códigos y las etiquetas, que
es lo que este acto necesitaba, **no están ahí y salieron del codebook de cada
ola**—, pero su afirmación literal sobre las filas es falsa y no se hereda
(`A.13`: el negativo se corrige donde se midió).

---

## 1 · Identidad: payload, tabla, unidad

| celda | ola | delitos de | payload (`id` de manifiesto) | miembro dentro del ZIP | filas (cabecera DBF) |
|---|---|---|---|---|---|
| `CIV-M-01` | ENVIPE 2012 | 2011 | `envipe_2012_base_de_datos_envipe_2012_dbf` | `Tmod_Vic.DBF` | 32 493 |
| `CIV-M-02` | ENVIPE 2013 | 2012 | `envipe_2013_bd_envipe13_dbf` | `tmod_vic.dbf` | 47 117 |
| `CIV-M-04` | ENVIPE 2015 | 2014 | `envipe_2015_bd_envipe2015_dbf` | `TMod_Vic.dbf` | 44 699 |

⚠️ **El nombre del miembro cambia de caja en las tres olas** (`Tmod_Vic.DBF`,
`tmod_vic.dbf`, `TMod_Vic.dbf`). Cada `spec.yaml` trae su ruta literal; un
medidor que arme el nombre por plantilla falla en dos de las tres.

La fila es **un DELITO** y el ponderador es `FAC_DEL`. Las tres corridas son de
unidad delito y **ninguna colapsa a persona**.

---

## 2 · El reactivo `BP1_23` — idéntico en las tres olas

Pregunta 1.23. Verificado en los tres descriptores, uno por uno:

| ola | fuente citada | ubicación exacta | redacción |
|---|---|---|---|
| 2012 | `FD_ENVIPE12.zip` → `FD_ENVIPE_2012.xls` | hoja `TMod_Vic`, fila **231** | «¿Cuál fue la razón principal por la que **no denunció** el delito ante el Ministerio Público?» |
| 2013 | `FD_ENVIPE13.xlsx` | hoja `TMod_Vic`, fila **292** | «¿Cuál fue la razón principal por la que **no denunció o no denunciaron** el delito ante el Ministerio Público?» |
| 2015 | `fd_envipe2015.pdf` | página **57** (1-based) | «¿Cuál fue la razón principal por la que **no denunció o no denunciaron** el delito ante el Ministerio Público?» |

**Los once códigos son idénticos en las tres olas**, con las mismas etiquetas:

| código | etiqueta | 2012 | 2013 | 2015 |
|---|---|---|---|---|
| `01` | Por miedo al agresor | ✓ | ✓ | ✓ |
| `02` | Por miedo a que lo extorsionaran | ✓ | ✓ | ✓ |
| `03` | Delito de poca importancia | ✓ | ✓ | ✓ |
| `04` | Pérdida de tiempo | ✓ | ✓ | ✓ |
| `05` | Trámites largos y difíciles | ✓ | ✓ | ✓ |
| `06` | Desconfianza en la autoridad | ✓ | ✓ | ✓ |
| `07` | No tenía pruebas | ✓ | ✓ | ✓ |
| `08` | Por actitud hostil de la autoridad | ✓ | ✓ | ✓ |
| `09` | Otra | ✓ | ✓ | ✓ |
| `99` | No sabe/no responde | ✓ | ✓ | ✓ |
| `b` | blanco | ✓ | ✓ | ✓ |

Tipo físico en la cabecera de los tres `.dbf`: `BP1_23` **`C 2`**, `BP1_20`
**`C 1`**. **No hay residuo y no hay ola `NO-CONSTRUIBLE` por el reactivo.**
La diferencia de redacción de 2012 («no denunció» sin «o no denunciaron») no
mueve ningún código y se declara aquí para que no se descubra después.

---

## 3 · `BPCOD` — el catálogo **sí** cambia, y 2012 va corrido un lugar

Este es el hallazgo de archivista de este acto. `BPCOD` no filtra el universo
**primario** `U_R` (que toma todos los tipos de delito), pero **sí define el
universo secundario homologado `U1`**, que es `BPCOD ∈ {05,…,15}` (delitos
personales) en el lenguaje de `prereg-caja-ENVIPE-DENUNCIA`.

| ola | fuente citada | ubicación | códigos |
|---|---|---|---|
| 2012 | `FD_ENVIPE_2012.xls` | hoja `TMod_Vic`, fila **26** | `01…14` (**catorce**) |
| 2013 | `FD_ENVIPE13.xlsx` | hoja `TMod_Vic`, fila **30** | `01…15` |
| 2015 | `fd_envipe2015.pdf` | página **51** (1-based) | `01…15` |

**2013 y 2015 son idénticos entre sí y al catálogo moderno.** 2012 es otro
libro: no tiene el código de vandalismo y su bloque de hogar es más corto.

### 3.1 · La tabla de mapeo, verbatim, once parejas

Etiquetas copiadas verbatim de cada descriptor. **A la izquierda 2012; a la
derecha 2013/2015, que son el lenguaje de la serie.**

| `BPCOD` 2012 | etiqueta 2012 (verbatim) | ≡ | `BPCOD` 2013/2015 | etiqueta 2013/2015 (verbatim) |
|---|---|---|---|---|
| `04` | Robo o asalto en la calle o en el transporte público (incluye robo en banco o cajero automático) | ≡ | `05` | Robo o asalto en la calle o en el transporte público (incluye robo en banco o cajero automático) |
| `05` | Robo en forma distinta a los anteriores | ≡ | `06` | Robo en forma distinta a la anterior |
| `06` | Clonación de tarjeta (crédito o débito) y fraude bancario | ≡ | `07` | Alguien usó su chequera, número de tarjeta o cuenta bancaria sin su permiso para realizar cargos o para extraer dinero de sus cuentas (fraude bancario) |
| `07` | Entrega de dinero por un producto o un servicio que no recibió conforme a lo acordado (fraude) | ≡ | `08` | Entregó dinero por un producto o un servicio que no recibió conforme a lo acordado (fraude al consumidor). |
| `08` | Amenazas, presiones o engaños para exigirle dinero o bienes; o para que hiciera algo o dejara de hacerlo (extorsión). | ≡ | `09` | Amenazas, presiones o engaños para exigirle dinero o bienes; o para que hiciera algo o dejara de hacerlo (extorsión). |
| `09` | Amenazas verbales de alguien plenamente identificado y que le causaron temor real | ≡ | `10` | Amenazas verbales de alguien plenamente identificado o por escrito hacia su persona diciendo que le va a causar un daño a usted, a su familia, a sus bienes o su trabajo |
| `10` | Lesiones por una agresión física | ≡ | `11` | Alguien sólo por actitud abusiva o por una discusión lo(a) golpeó generándole una lesión física (moretones, fracturas, cortadas, etc.) |
| `11` | Secuestro para exigir dinero o bienes | ≡ | `12` | Lo secuestraron para exigir dinero o bienes |
| `12` | Hostigamiento, manoseo, exhibicionismo, intento de violación | ≡ | `13` | Alguien en contra de su voluntad lo(a) agredió mediante hostigamiento sexual, manoseo, exhibicionismo o intento de violación |
| `13` | Violación sexual | ≡ | `14` | Fue obligado(a) mediante violencia física o amenaza por alguien conocido o desconocido a tener una actividad sexual no deseada (Violación sexual) |
| `14` | Otros delitos distintos a los anteriores | ≡ | `15` | Otros delitos distintos a los anteriores |

**Once parejas, en orden, sin hueco.** El bloque personal de 2012 es
`{04,…,14}` y equivale exactamente al `{05,…,15}` de 2013/2015.

El bloque de **hogar** de 2012 es `{01,02,03}`: `01` robo total de vehículo,
`02` robo de accesorios de vehículos, `03` **robo en su casa habitación**.
En 2013/2015 el bloque de hogar es `{01,02,03,04}`.

### 3.2 · El residuo, con su razón completa

> **Residuo del mapeo:** el código moderno `03` (**«Pinta de barda o grafiti en
> su casa, rayones intencionales en su vehículo u otro tipo de vandalismo»**) no
> tiene contraparte en 2012 — el instrumento de 2012 no captaba ese delito. Ese
> código pertenece al **bloque hogar** (`{01,…,04}` en 2013/2015), que `U1`
> **excluye por construcción**. Por lo tanto el residuo es **nulo sobre el
> universo secundario**: ninguna fila que `U1` habría contado en 2013/2015 queda
> sin contraparte en 2012, y ninguna fila de 2012 entra a `U1` sin pareja.
>
> El residuo **sí** afecta al bloque hogar, que no es universo de ningún
> estimando de esta spec y que se reporta sólo como conteo estructural
> (`N-BPCOD-HOGAR`).

### 3.3 · Cómo se falsa el corrimiento sin tocar el estimando

Cada corrida emite `PERFIL-BPCOD`: la distribución de `BPCOD` **código por
código, sin ponderador, antes de todo filtro**. Es reporte **estructural**, no
estimación. Si el corrimiento declarado arriba estuviera mal, la forma de esa
distribución lo delata —2012 no puede tener un código `15`, y su masa por
código debe seguir el orden de las once parejas— **sin que ningún resultado
participe en la validación**. La contaminación declarada prohíbe validar el
mapeo contra resultados: aquí se valida contra **etiquetas y estructura**, que
es lo único admisible.

---

## 4 · Diseño y ponderador — **vínculo por ola, no edición de la guardia**

La guardia de columna ausente de la familia nombra `EST_DIS` y `UPM_DIS`. En
2012 y 2013 esas columnas **no existen con ese nombre**: se llaman `EST` y
`UPM`. Aplicar la guardia por nombre literal declararía `NO-ESTIMABLE` dos de
las tres olas por un **falso negativo de nombre**.

La guardia **no se edita**. Cada `spec.yaml` declara un **vínculo
`rol → nombre físico`** (`mapa_columnas`) y el medidor no conoce ningún nombre
por su cuenta:

| rol | 2012 | 2013 | 2015 |
|---|---|---|---|
| `BP1_23` (desenlace) | `BP1_23` `C 2` | `BP1_23` `C 2` | `BP1_23` `C 2` |
| `BP1_20` (ruta de universo) | `BP1_20` `C 1` | `BP1_20` `C 1` | `BP1_20` `C 1` |
| `BPCOD` (tipo de delito) | `BPCOD` `C 2` | `BPCOD` `C 2` | `BPCOD` `C 2` |
| `FAC_DEL` (ponderador) | `FAC_DEL` **`C 6`** | `FAC_DEL` **`C 6`** | `FAC_DEL` **`N 12`** |
| `ESTRATO` (estrato de diseño) | **`EST`** `C 3` | **`EST`** `C 3` | **`EST_DIS`** `C 3` |
| `UPM` (unidad primaria) | **`UPM`** `C 5` | **`UPM`** `C 5` | **`UPM_DIS`** `C 5` |

Tipos leídos de la **cabecera del propio `.dbf`**, no del FD. Citas del FD para
el revisor: 2012 `FD_ENVIPE_2012.xls` hoja `TMod_Vic` filas **621** (`FAC_DEL`),
**627** (`EST`), **628** (`UPM`); 2013 `FD_ENVIPE13.xlsx` hoja `TMod_Vic` filas
**626**, **632**, **633**; 2015 `fd_envipe2015.pdf` páginas **50** (`EST_DIS`,
`UPM_DIS`, declarados `Alfanumérico`) y **64** (`FAC_DEL`).

⚠️ **`FAC_DEL` cambia de tipo entre olas** (`C` en 2012/2013, `N` en 2015). El
medidor lee **todo campo DBF como texto crudo** y convierte después: así el
tipo declarado en la cabecera no puede cambiar el resultado.

⚠️ **En 2015 conviven `UPM` (`C 7`) y `UPM_DIS` (`C 5`) y NO son la misma
columna.** Esta spec usa `UPM_DIS`, que es la unidad primaria de *diseño*. GEN1
usó lo mismo (`CIV-M-04.json`, campo `upm: "UPM_DIS"`), y el descriptor de 2015
la declara explícitamente «Unidad primaria de muestreo». La coincidencia con
GEN1 se cita como **precedente**, no como autoridad: la autoridad es el
descriptor.

⚠️ **Llaves opacas.** `ESTRATO` y `UPM` se agrupan como cadenas crudas: nunca
`int()`, nunca `zfill()`, nunca re-relleno al ancho del descriptor. El perfil
observado se emite en `PERFIL-DISENO` y su desacuerdo con el descriptor es
hallazgo, no defecto a corregir.

⚠️ **`FAC_DEL_AM` (2015) no se usa**: es el factor ajustado a las 32 áreas
metropolitanas, otro dominio de estimación. 2012 y 2013 no lo traen.

---

## 5 · La guardia de `tper_vic2` — **`NO-APLICA`, por ola, con cita**

`prereg-caja-ENVIPE-DENUNCIA` define un universo `U4` (unidad **persona**,
llave `ID_PER`, ponderador `FAC_ELE`, tabla `tper_vic2`) y una guardia de
columna ausente que lo nombra.

**La familia `R-ENVIPE-SERIE` no mide `U4`.** Sus dos estimandos —`U_R`
primario y `U1` secundario homologado— son **ambos de unidad delito sobre
`tmod_vic` con `FAC_DEL`**, y ninguno de los 38 `RESULT` del trío CSV toca
`tper_vic2`. `ID_PER` aparece una sola vez en la familia (§2.1), como una de
las columnas cuya presencia se verificó en el inventario, no como unidad medida.

Por lo tanto, para las tres olas de este acto: **guardia de `tper_vic2` =
`NO-APLICA`**. Es un valor declarado, no una omisión (`D-15`).

**Y se declara además, porque es un hecho del descriptor que un sucesor va a
necesitar:** si algún acto futuro quisiera `U4` en estas olas, 2015 podría
(`TPer_Vic2.dbf` trae `ID_PER` `C 16` y `FAC_ELE` `N 12`) y **2012 no**. El
`tper_vic.dbf` de 2012 tiene **311 436 filas — exactamente las mismas que
`tsdem.DBF`**, es decir el censo completo del hogar y no la persona
seleccionada, y **no trae `N_REN`**: tiene `N_INF`, `R_SEL` y `TOT_PER`, pero
ningún campo que diga qué renglón es *esa* fila. Aislar a la persona
seleccionada exigiría un join a `tsdem` por `N_REN == R_SEL` que ninguna spec de
esta familia declara. Fuente: `FD_ENVIPE_2012.xls`, hoja `TPer_Viv`. Esa ruta
**no se improvisa aquí**: queda como fila `NC` con sucesor.

---

## 6 · Estimandos, universos y codificación — copiados, no elegidos

Idénticos a la familia sellada, §3.1 y §3.2. Se repiten para que esta spec sea
legible sola, pero **manda la sellada** donde difieran.

- **`U_R` (PRIMARIO).** Filas de `TMod_Vic` con `BP1_23 ∈ {01,…,09}` y `FAC_DEL`
  válido. **Todos** los tipos de delito, sin filtro de `BPCOD`. `99` y blanco
  quedan fuera. `R = p(C_R, U_R)`, con `d = 1` si `BP1_23 ∈ {01,02,06}` y `0` si
  `∈ {03,04,05,07,08,09}`.
- **`U1` (SECUNDARIO HOMOLOGADO).** `BPCOD` en el **bloque personal de la ola**
  (`{04,…,14}` en 2012; `{05,…,15}` en 2013 y 2015), `BP1_20 = 2`,
  `BP1_23 ∈ {01,…,08}`, `FAC_DEL` válido. `C1`: `1` si `∈ {01,02,06}`, `0` si
  `∈ {03,04,05,07,08}`. `C2` (partición GEN1): `1` si `∈ {01,02,06,08}`.
- **`U_R` y `U1` no se comparan entre sí** (`A-bis.4`): están en la misma
  corrida porque salen de la misma lectura del mismo archivo.

**Estimadores.** `EE` e `IC95` por conglomerado último importando
`tests/svystat.py:prop_ultimate_cluster` —sellado, no se reimplementa— y, sólo
para el secundario, IC por **bootstrap de UPM con reemplazo dentro de estrato**,
conservando el número de UPM por estrato, percentiles 2.5/97.5, **semilla
`20260909`, 2 000 réplicas**: los mismos que fijaron el IC de la ola 2025 y el
del trío CSV, para que la columna de IC de la serie sea homogénea en los siete
puntos y no en cuatro.

**Estratos de UPM única:** no se colapsan (decisión de diseño que esta spec no
está autorizada a tomar) y no se descartan (sesgaría el punto). Entran al punto,
aportan varianza cero, y en el bootstrap se re-muestrean a sí mismos. Si su
conteo es `> 0`, `METODO-IC` sale `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee
como **límite inferior** de la anchura verdadera.

**Guardias de existencia.** Columna declarada ausente → `ESTADO =
NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`. `BP1_23` sin ningún valor válido →
`NO-ESTIMABLE-COLUMNA-VACIA:BP1_23`. `U_R` vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`.
**Cero nunca sustituye falta de dato.**

**Registros borrados.** Un `.dbf` marca los registros borrados con `*` en el
primer byte. No entran al universo y **se cuentan aparte** en `PERFIL-DBF`, con
el número de registros que la cabecera declara y el que se leyó de verdad. Un
desacuerdo entre los dos es hallazgo, no algo que el medidor corrija.

---

## 7 · Control positivo externo contra GEN1 — después de sellar, y sólo entonces

Lo corre `forense/prereg-caja/R-ENVIPE-SERIE-DBF-control-gen1.py`, **script
aparte**, DESPUÉS de sellar, contra `forense/prereg-duelo-v2/corridas-R/CIV-M-01.json`,
`-02` y `-04`. El medidor no abre esos JSON ni recibe el valor GEN1 por ninguna vía.

**La celda comparable es el PUNTO PRIMARIO `R`, nunca el IC.** Los tres JSON del
trío viejo declaran `ponderador: FAC_DEL`, tabla `TMod_Vic` y unidad delito
(`n_filas_leidas` 32 493 / 47 117 / 44 699), es decir la misma unidad y el mismo
ponderador que `U_R`. Se compara `PUNTO` contra el campo `R` del JSON.

Cuatro ramas pre-declaradas:

- **`REPRODUCE`** si `|Δ| ≤ 1.0e-9`.
- **`REPRODUCE-CON-TOLERANCIA`** si `1.0e-9 < |Δ| ≤ 1.0e-6`.
- **`NO-REPRODUCE`** si `|Δ| > 1.0e-6`. **No invalida la corrida, no autoriza
  tocar el medidor y no cambia el estimando.** Se reporta el delta **con signo**
  y se abre `NC` con sucesor.
- **`NO-COMPARABLE`** si la corrida sale `NO-ESTIMABLE` por cualquier guardia.

⚠️ El control se calcula **después** de que los tres `sello.json` existan. Que
el resultado coincida o no coincida **no vuelve hacia atrás sobre esta spec**:
si hubiera que cambiar algo, sería un tercer commit que lo dijera (`E.5`).

---

## 8 · Límites declarados (van también en la nota)

1. **La serie sigue sin ser completa.** Con este trío la serie tiene **siete**
   puntos (2012, 2013, 2015, 2021, 2023, 2024, 2025 en año de ola), no trece.
   Faltan las olas 2011, 2014, 2016, 2017, 2018, 2019, 2020 y 2022.
2. **El eje es el año de DELITO, no el nombre de la ola.** La ola 20NN mide
   delitos de 20NN−1. Confundirlos desplaza la serie un año.
3. **El punto 2012 lleva su costura visible.** Su `U1` se construyó con el
   bloque personal `{04,…,14}` por el corrimiento de §3.1. La serie lo marca en
   ese punto; no se esconde.
4. **Descriptiva, no adjudicada.** Ningún `RESULT` es causal: la razón principal
   es lo que la persona **declaró**. Transferencia y estabilidad temporal se
   contratan en `F5`.
5. **Ninguna adopción.** Los `R` no se adoptan en ningún consumidor del duelo:
   eso es `F3`, por lote y con firma de mesa.
6. **`U4` no se mide** (§5), y el inventario de reactivos sigue sin cubrir DBF:
   eso es fila `NC` con sucesor, no arreglo de este acto.

---

## 9 · Congelamiento

Esta spec, los tres `spec.md`, los tres `spec.yaml` y el `medidor.py` —**byte
idéntico en los tres `CALC`**— quedan congelados en el `COMMIT-1` de este acto,
antes de abrir un solo registro de microdato.

> **El primer resultado que produzca este procedimiento es el que se reporta.**
