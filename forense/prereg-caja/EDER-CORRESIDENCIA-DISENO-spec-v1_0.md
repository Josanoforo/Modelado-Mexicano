# EDER-CORRESIDENCIA-DISENO · Pre-registro de la re-estimación con diseño muestral de la tasa de fase 1 de EDER 2017 (`familia.corresidencia.adulto_familiar`)

### `prereg-caja-EDER-CORRESIDENCIA-DISENO` · **v1.0** · 14 de septiembre de 2026

**Acto:** `ACTO GEN2-DISENO-FASE1-CIERRE` · CAJA (Ubuntu/WSL2) · base `origin/main = 4fedf1cf` (PR #757)
**Encargo:** `forense/encargos/2026-09-14-GEN2-DISENO-FASE1-CIERRE.md` (A.3, verbatim)
**Sucesor de:** la tasa de fase 1 `familia.corresidencia.adulto_familiar` (`FP-201`, `ACTO MAESTRA32-E18`, 31/ago/2026): `p = 0.996086`, `ic95 = [0.994794, 0.997250]`, `n = 14887`, ponderador `factor`, bootstrap simple de filas — sellada **sin carga** en `milpa/tramite-ola5-propuesta-v0.yaml:110-129` (`situacion: SELLADA-SIN-CARGA`, `FP-200=b`, `D2-b`); producida por `tools/tasas_base_fase1.py::regla_familia_corresidencia` y reportada en `forense/notas/2026-08-31-reglas-fase1-cierre.md:78`. **No releva ninguna `CORR-*` de la demanda**: la tasa nunca entró al motor (`CORR-0013`/`RES-0043`/`RES-0044` son `familia.union.libre`, otra regla sobre el mismo payload).
**Corrida:** `data/corrida0/CALC-EDER-0001/`

> **CONGELADA EN EL COMMIT-1, ANTES DE LEER UN SOLO VALOR DEL MICRODATO.**
> Lo único abierto al escribirla (E.5): `data/manifiesto.yaml`; el descriptor
> `eder2017_fd.pdf` (7 521 líneas extraídas con `pdftotext -layout`) y la
> receta oficial `eder2017_descripcion_calculoR.pdf` (516 líneas); la **lista
> de miembros** del ZIP con sus tamaños, la **cabecera** (primera línea, nombres
> de columna) de los cinco `.csv` y el **conteo de líneas** de `vivienda.csv` y
> `antecedentes.csv`; `data/diseno-muestral.yaml`; `data/inventario-reactivos-v1_2.tsv`;
> `milpa/tramite-ola5-propuesta-v0.yaml`; `tools/tasas_base_fase1.py`;
> `data/corrida0/demanda-*.tsv`; y las notas de fase 1. **Ningún valor de
> ninguna fila.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Lo que el encargo declaró, contrastado

| lo que el encargo declaró | lo real, verificado |
|---|---|
| «redactado contra el corte del 14/sep (re-deriva al abrir)» | base real al abrir: **`4fedf1cf`** (merge de `PR #757`, `GEN2-B-MARCO`). Compuerta verificada por producto, ver el encargo archivado. |
| «las fuentes de fase 1 con la revisión PENDIENTE: ENNViH (MxFLS olas 2–3) y EDER 2017» | **CIERTO en la lista, con matiz en ENNViH**: la existencia de diseño en ENNViH **ya fue revisada tres veces** (`RECENSO-DISENO-14` 24/ago, `CAL-G3-PUNTUAL` PASO 0 24/ago, `GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL` 10/sep) con el mismo veredicto: sin UPM ni estrato de diseño públicos. Lo que **nadie** había hecho es cerrar esa revisión contra `NC-0086`; eso lo hace la nota de auditoría de este acto (P1), sin repetir la revisión. |
| «Los payloads de ambas EXISTEN en el manifiesto» | EDER: **CIERTO** (`eder_2017_eder2017_bases_csv`, `data/manifiesto.yaml:4421-4428`, sha `bcc7eb90…`). ENNViH: **FALSO en la letra** — `data/manifiesto.yaml` sigue sin `id:` para `ehh05dta_all.zip`/`ehh05w_all.zip` (hallazgo preexistente de fase 1, `2026-08-31-reglas-fase1-cierre.md` hallazgo 1); los ZIP existen en la raíz. No bloquea: ENNViH no se re-estima aquí. |
| «⚠️ El inventario de reactivos NO cubre formatos viejos (NC-0123, precedente DBF): todo se resuelve por descriptor/codebook DE LA FUENTE» | Obedecido: los veredictos de P1 salen del FD y de la receta R de INEGI, con página. El inventario sólo se usa como control positivo de `spec-check` (EDER 2017 CSV **sí** está inventariado: `vivienda.csv::est_dis/upm/factor`, `antecedentes.csv::factor_per`). |

### 0.2 · Cobertura retroactiva (E.1)

El valor GEN1 (`0.996086`, `n = 14887`) es **control positivo posterior sobre el
punto**, jamás insumo: el medidor no lo lee del árbol, lo recibe como parámetro
de referencia y sólo lo usa para escribir `A-DELTA-VS-GEN1`. El IC de fase 1
(`[0.994794, 0.997250]`, bootstrap simple de filas, `seed=42`) **no se compara**
con ningún IC de esta corrida (A-bis.3, lección del lote ENIF): dos métodos
distintos no se ponen lado a lado. La única lectura autorizada del IC viejo es
la **cláusula `se_mueve_si`** que la propia propuesta escribió (§4.4).

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Al congelar, la sesión ya había leído: el `p`, el `n`, el `ic95` y el universo
de la tasa de fase 1 (encargo, propuesta, nota de cierre, script); el `p =
0.057531` de la re-especificación `familia.corresidencia.adulto_familiar_actual`
(`MAESTRA33-C1`) y su reserva sobre `factor_per`; y la fila EDER de
`data/diseno-muestral.yaml` (conteos de distintos sobre las primeras filas de
`vivienda.csv`, `RECENSO-DISENO-14`). **Lo genuinamente desconocido al
congelar:** el número real de estratos y UPM en el universo de personas, si
alguna UPM cruza estratos, cuántos estratos quedan con una sola UPM, la anchura
del IC de diseño, la distancia entre `factor` y `factor_per` sobre este
estimando, y si los códigos `*_cor` llegan como `'1'` o como `'1.0'` al leer
con pandas — ninguno aparece en fuente alguna leída.

---

## 1 · Identidad

### 1.1 · Payload, por el manifiesto y por la raíz

`eder_2017_eder2017_bases_csv` → `data/raw/eder2017/eder2017_bases_csv.zip`,
`sha256 bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`,
13 313 736 bytes, ZIP de 5 miembros: `persona.csv` (12 412 670 B),
`vivienda.csv` (5 708 665 B), `antecedentes.csv` (3 690 653 B),
`historiavida.csv` (400 713 759 B), `hogar.csv` (862 735 B). Mismo payload y
mismo sha que fase 1 y que `ACTO MAESTRA32-E16`.

Descriptores, en la misma carpeta de la raíz (no en el ZIP):
`eder2017_fd.pdf` (`sha256 dd4d9311…5890541`) y
`eder2017_descripcion_calculoR.pdf` (`sha256 01c21e5e…6ff2e6f`).

### 1.2 · Ola, población y unidad, por el descriptor

EDER 2017 (INEGI), única ola; «Las unidades de análisis para la EDER 2017 son
personas de 20 a 54 años del hogar» (`eder2017_fd.pdf` §1.1.2, p. 7-8).
`Folioviv` «Consta de 10 dígitos: dos dígitos con la clave de la entidad
federativa, uno con el ámbito (…), cuatro dígitos del número consecutivo de la
unidad primaria de muestreo (UPM) y tres dígitos con un número consecutivo para
la vivienda seleccionada» (p. 7). `Foliohog` e `Id_pobla` completan la llave de
persona (p. 8).

### 1.3 · Diseño muestral: lo que el descriptor declara, verbatim

`eder2017_fd.pdf`, tabla VIVIENDA (p. 15), entradas #105-#109, tipo tal como
el catálogo lo declara:

| # | variable | descripción del FD | tipo declarado |
|---|---|---|---|
| 105 | `tam_loc` | Tamaño de localidad | `C (1)` |
| 106 | `est_socio` | Estrato socioeconómico | `C (1)` |
| **107** | **`est_dis`** | **Estrato de diseño muestral** | **`C (4)`** |
| **108** | **`upm`** | **Unidad primaria de muestreo** | **`C (5)`** |
| **109** | **`factor`** | **Factor de expansión** | **`N (5)`** |

Definiciones (p. 40): `est_dis` — «Son los estratos seleccionados en la
segunda etapa del muestreo y corresponden a grupos de UPMs de acuerdo con su
estrato geográfico (entidad-ámbito-zona). Nota: Variable definida en el diseño
muestral.» `upm` — «Las unidades primarias de muestreo están constituidas por
agrupaciones de viviendas (…). Estas unidades son seleccionadas en la primera
etapa del muestreo y corresponden a áreas geográficas con límites
identificables en el terreno (…). Nota: Variable definida en el diseño
muestral.» `factor` — «Factor de expansión de los hogares que respondieron el
Módulo.»

Tabla ANTECEDENTES (p. 17), entrada #52: **`factor_per`** — «Factor de
expansión», `N (5)`; definición p. 66: «Factor de expansión. NOTA: Variable
definida en el diseño muestral.»

§1.1.3 (p. 8), verbatim: «En la EDER 2017 el factor de expansión para las
personas de 20 a 54 años de edad, se encuentra en la variable factor_per de la
tabla ANTECEDENTES. En la ENH 2017 el factor de expansión para las tablas que
complementan la EDER 2017, como son: VIVIENDA, HOGAR y PERSONA, se encuentra en
la variable factor de la tabla VIVIENDA.»

Receta oficial de varianza, `eder2017_descripcion_calculoR.pdf`: p. 5
`options(survey.lonely.psu="adjust")` bajo el comentario «# Opción para tratar
los casos de los estratos con una sola una UPM»; p. 7 `viv<- viv[
c("folioviv", "est_dis", "upm", "factor", "ubica_geo")]`; p. 8 (y 9-11)
`DIS <- svydesign(id=~upm, strata=~est_dis, data= tabla_fin, weights=~factor_per)`.

Cabecera real de los CSV (primera línea, sin valores): `vivienda.csv` trae
`…,tam_loc,est_socio,est_dis,upm,factor` (109 columnas; 23 548 líneas de
datos); `antecedentes.csv` trae `…,factor_per` (52 columnas; 23 831 líneas);
`historiavida.csv` trae `folioviv,foliohog,id_pobla,…,padre_cor,…,madre_cor,…,
hnos_cor,…` (200 columnas) — `suegro_cor`/`suegra_cor` están más allá de la
columna 60 y se verifican como guardia G-2 al abrir. El primer nombre de
columna de cada archivo llega con BOM (`ï»¿folioviv` bajo latin-1): el medidor
lo resuelve por `endswith("folioviv")`, igual que fase 1.

**Veredicto de P1 para EDER 2017: `EXISTE-SATISFACE`** — ponderador, estrato y
UPM existen en las tablas y en el descriptor oficial, con receta de varianza
publicada por el productor. `FP-201` («sin campo de diseño UPM/estrato
reproducible» para las cinco fuentes de fase 1) **es falso también para EDER
2017** — quinta fuente en que cae (ENVIPE, ENIF, ENCUCI y las olas de
`GEN2-R-SERIE-CSV` antes) — y la propia spec de fase 1 (§(c)4) ya sospechaba
«EDER trae est_dis/upm de diseño», sin verificarlo. `RECENSO-DISENO-14`
(24/ago/2026, `ADR-149`) lo tenía **MAPEADO** en `data/diseno-muestral.yaml`
una semana antes de que `FP-201` lo negara.

---

## 2 · El estimando, verbatim de fase 1 (E.3: mismos estimandos, sellos viejos intactos)

`tools/tasas_base_fase1.py:258-316`, reproducido paso a paso en el medidor:

1. `vivienda.csv` leído con `pandas.read_csv(encoding="latin-1", low_memory=False)`;
   **universo de viviendas** = filas con `tipo_adqui` no nulo y distinto de
   `""` tras `astype(str).str.strip()`; `pesos_hogar = factor` indexado por
   `folioviv`.
2. `historiavida.csv` leído igual; para cada una de `padre_cor, madre_cor,
   hnos_cor, suegro_cor, suegra_cor`: `astype(str).str.strip()`; fila
   co-reside si alguna es exactamente `"1"`.
3. **Persona** = grupo `(folioviv, foliohog, id_pobla)` de `historiavida.csv`;
   `desenlace = max` del indicador de fila (1 si co-residió con ascendiente,
   hermano o suegro en alguna fila del panel retrospectivo, 0 si nunca).
4. `peso = factor` de la vivienda del `folioviv` de la persona (map); personas
   sin peso (vivienda fuera del universo o inexistente) **salen** — ésa es la
   diferencia `n_personas_historiavida_total → n_con_ponderador` de fase 1.
5. `p = Σ peso·desenlace / Σ peso` sobre las personas con peso. Sumas en el
   orden de aparición de las llaves (pandas `groupby` ordena por llave; el
   estimador es invariante al orden salvo redondeo de float64).

**El universo, el ponderador, la codificación y el colapso NO cambian.** Lo
único que esta corrida añade es (a) la varianza de diseño y (b) una
sensibilidad de ponderador pre-declarada (§3.3), que **no** sustituye al
estimando sucesor.

---

## 3 · Método — todo pre-declarado

### 3.1 · Llaves opacas y unión con el diseño

`est_dis` y `upm` se leen como **texto crudo** (`dtype=str`), nunca `int()`,
nunca `zfill()`: normalizarlas fusionaría o partiría estratos en silencio. Se
unen a cada persona por `folioviv` desde `vivienda.csv` (donde el descriptor
las coloca). Se emite el perfil de anchos observados (`G-PERFIL-EST-DIS`,
`G-PERFIL-UPM`) y si toda `upm` anida en un solo `est_dis`
(`G-UPM-ANIDA-EN-EST-DIS`). La clave de conglomerado del bootstrap es el par
`(est_dis, upm)`, con separador que no aparece en el dato.

### 3.2 · Varianza de diseño — patrón ENVIPE/ENCUCI, con la regla de UPM única

**Primaria (`A-IC-LO`/`A-IC-HI`):** bootstrap de `upm` **con reemplazo dentro
de** `est_dis`, conservando el número de UPM por estrato, **2 000 réplicas**,
percentiles 2.5/97.5, `seed = 20260914`, `rng = numpy.PCG64`, sumas por UPM en
orden fijo. **Regla de estratos-de-UPM-única, pre-declarada:** un estrato con
exactamente una UPM se re-muestrea a sí mismo (varianza cero); **no se colapsa**
(decisión de diseño que esta spec no está autorizada a tomar) y **no se
descarta** (sesgaría el punto). Si `A-N-ESTRATOS-UPM-UNICA > 0`, `A-METODO-IC`
sale `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior de la
anchura verdadera**. Las personas de `U` sin `est_dis` o sin `upm` se cuentan
(`A-N-SIN-DISENO`) y afectan al IC, no al punto; si **toda** `U` careciera de
diseño, `A-METODO-IC = NO-ESTIMABLE-DISENO-INCOMPLETO` y los IC salen `null`
con el punto reportado igual.

**Secundaria, sensibilidad de método (`A-EE-TAYLOR`, `A-IC-LO-TAYLOR`,
`A-IC-HI-TAYLOR`):** la receta del productor — linealización de Taylor del
cociente `p = Σwd/Σw` con `z_i = w_i(d_i − p)/Σw`, totales por UPM, varianza
`Σ_h n_h/(n_h−1) Σ_j (z_hj − z̄_h)²`; para un estrato con una sola UPM se
aplica una **aproximación declarada** de `survey.lonely.psu="adjust"`: su UPM
se centra en la media global de los totales por UPM y entra con factor 1. IC =
`p ± 1.959964·EE`. Es lo que INEGI publica para EDER (`svydesign(id=~upm,
strata=~est_dis, …)`); se reporta para que quien use R pueda cotejar, **no**
sustituye a la primaria y **no** se adopta.

### 3.3 · Sensibilidad de ponderador (`B-*`) — la ranura `se_mueve_si`

La propuesta escribió, en la propia entrada de la regla
(`milpa/tramite-ola5-propuesta-v0.yaml:112`): `se_mueve_si: "re-corrida con
factor_per (ponderador oficial) reproduce p dentro del IC → carga tier FUERTE;
fuera del IC → re-especificación"`. Esta spec **ejecuta esa re-corrida y no la
adjudica**: mismo universo de personas que `A` (§2, pasos 1-4 con `factor`
presente), mismo desenlace, y peso `factor_per` de `antecedentes.csv` unido por
`(folioviv, foliohog, id_pobla)`. Personas sin `factor_per`, con `factor_per`
no finito o `≤ 0` **salen de `B`** contadas (`B-N-SIN-FACTOR-PER`,
`B-N-FACTOR-PER-CERO` — la receta R marca `POB <- ifelse(!factor_per %in% 0,
1, 0)`, así que el cero es «fuera de la población objetivo», no un peso). Misma
varianza de diseño que `A` (bootstrap primario + Taylor secundario).
`B-CLAUSULA-SE-MUEVE-SI` lee la cláusula **literalmente** sobre el IC de fase 1
`[0.994794, 0.997250]`: `DENTRO-DEL-IC-FASE1` si `0.994794 ≤ B-P ≤ 0.997250`,
`FUERA-DEL-IC-FASE1` en otro caso. Esto **no es una comparación de IC** (no se
pone ningún IC de esta corrida junto al viejo): es la aplicación mecánica de la
condición que mesa dejó escrita. La consecuencia («carga tier FUERTE» /
«re-especificación») **es de mesa, no de este acto**.

### 3.4 · Guardias — paran, no adivinan

- **G-1 miembros:** si falta `vivienda.csv`, `historiavida.csv` o
  `antecedentes.csv` → `NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>`.
- **G-2 columnas:** si falta cualquiera de `folioviv`(por sufijo), `tipo_adqui`,
  `factor`, `est_dis`, `upm` (vivienda); `foliohog`, `id_pobla`, las cinco
  `*_cor` (historiavida); `factor_per` (antecedentes) →
  `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`.
- **G-3 llave:** `folioviv` único en `vivienda.csv` (`SI`/`NO`); si `NO`, el
  `map` de fase 1 sería ambiguo → `A-VEREDICTO = NO-ESTIMABLE-LLAVE-NO-UNICA`
  y no se elige otra llave. `(folioviv, foliohog, id_pobla)` único en
  `antecedentes.csv` (`SI`/`NO`); si `NO`, sólo la familia `B` sale
  `NO-ESTIMABLE-LLAVE-NO-UNICA`.
- **G-4 tipo:** `G-N-PADRE-COR-CADENA-UNO` (texto crudo exactamente `'1'`) vs
  `G-N-PADRE-COR-NUMERICO-UNO` (parsea a 1 con parte fraccionaria nula) sobre
  las filas de `historiavida.csv`: mide la trampa de tipo `'1'` vs `'1.0'`
  en vez de suponerla. Si difieren, el estimando sucesor **sigue usando la
  cadena** (es la codificación de fase 1, E.3) y la diferencia se reporta.
- Universo vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`. **Cero nunca sustituye falta
  de dato.**

### 3.5 · Tipos: manda el archivo

`factor` y `factor_per` se leen como flotante tal cual (pandas por defecto);
`factor = 0` o no finito hace que la persona salga de `A` contada
(`A-N-SIN-PONDERADOR`), replicando el `dropna` de fase 1 más la guardia de
finitud. Los CSV se leen con `encoding="latin-1"` como fase 1 (el BOM UTF-8
queda como prefijo del primer nombre de columna y se resuelve por sufijo).

---

## 4 · Ramas pre-declaradas — escritas ANTES del dato

### 4.1 · Control positivo contra GEN1 (`punto, no IC`)

| celda medida | valor GEN1 | `RESULT` de delta |
|---|---|---|
| `A-P` | `0.996086` (propuesta-v0 `:116`) | `A-DELTA-VS-GEN1` |
| `A-N-U` | `14887` (propuesta-v0 `:123`) | `A-DELTA-N-VS-GEN1` |

`A-REPRODUCE-GEN1 ∈ {REPRODUCE (|delta| ≤ 1e-6), NO-REPRODUCE, NO-COMPARABLE}`.
Un `NO-REPRODUCE` **no invalida** la corrida, **no autoriza** tocar el medidor
y **no se ajusta hacia atrás**: se reporta con su embudo y se atribuye (lección
`GEN1 familia A`). El complemento (`A-P-COMPLEMENTO`) se cuenta directamente
sobre el mismo denominador, nunca como `1 − p`; `A-SUMA` prueba que los dos
bloques agotan `U`.

### 4.2 · Adopción (P2/P3 del encargo), pre-declarada

El único consumidor de esta tasa es `milpa/tramite-ola5-propuesta-v0.yaml:110`
(`SELLADA-SIN-CARGA`, sin cita `corrida0_*`, archivo que el motor no carga) —
**no tiene cita GEN2 vigente**, así que por el encargo «queda listado para
adopción de mesa»: **este acto no escribe ninguna cita en `milpa/`**.
`A-ADOPCION-P3 ∈ {LISTADO-PARA-MESA-REPRODUCE, LISTADO-PARA-MESA-NO-REPRODUCE,
NO-ADOPTABLE-NO-ESTIMABLE}`. `familia.corresidencia.adulto_familiar_actual`
(`MAESTRA33-C1`, ventana actual, `p = 0.057531`, misma reserva de ponderador)
**no es tasa de fase 1** y queda fuera de este CALC, nombrada como sucesor.

### 4.3 · Qué cambia y qué no

Si los controles pasan: **el punto no cambia** (es el mismo estimando); lo que
cambia es la **varianza** — de bootstrap simple de filas a bootstrap de UPM
dentro de estrato (más la Taylor de cotejo). La lectura del techo casi saturado
(`hallazgo` de la propuesta) no se toca: sigue siendo un artefacto del diseño
«alguna vez en la vida».

---

## 5 · Estimando

**DESCRIPTIVO.** Ningún `RESULT` es causal.

- **Sucesor (adoptable por mesa):** `A-P` con `A-IC-LO`/`A-IC-HI`.
- **Secundarios declarados:** `A-P-COMPLEMENTO`, la Taylor de cotejo, toda la
  familia `B` (sensibilidad de ponderador — **no** adoptable como sucesor de
  la tasa de fase 1 porque cambia el estimando), los perfiles de llave y todos
  los conteos de embudo.

---

## 6 · Límites declarados (van también en la nota de cierre)

- **Una sola ola** (EDER 2017). No se toca EDER 2011 ni EDER 2025.
- **IC como límite inferior** si algún estrato queda con una sola UPM.
- **`factor` es ponderador de vivienda (ENH)** por el FD §1.1.3; la tasa de fase
  1 lo usó para personas y el sucesor lo hereda por E.3. `factor_per` es el
  oficial de persona y va como sensibilidad `B`, con la cláusula literal.
- **Aproximación declarada** de `lonely.psu="adjust"` en la Taylor secundaria.
- **A-bis.3:** el IC de fase 1 no se compara con ninguno de esta corrida.
- **Contaminación (ADR-46):** la corrida **no es ciega**; §0.3 la declara.
- **Causalidad: ninguna.**

---

## 7 · Congelamiento

Esta spec se escribe y se commitea **antes** de que el medidor lea un solo
valor. `data/corrida0/CALC-EDER-0001/spec.yaml` es su cara mecánica y cita su
`sha256`; `medidor.py` se congela en el mismo commit y **no se edita después**
— si resultara equivocada, se escribe una `v1.1` fechada, nunca una corrección
hacia atrás.

**El primer resultado que produzca este procedimiento es el que se reporta.**
