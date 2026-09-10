# ENCIG-MORDIDA · Pre-registro de la mordida por canal y de la adopción de gobierno digital, ENCIG 2025

### `prereg-caja-ENCIG-MORDIDA` · **v1.0** · 9 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-ENCIG-1` · CAJA (Ubuntu/WSL2) · base `origin/main = 606f6ee`
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENCIG-1.md` (A.3, verbatim, con su ADENDA DE PROPAGACIÓN)
**Releva:** `CORR-0002` (ENCIG2025) → **12** `RESULT`: `RES-0003`, `RES-0004`, `RES-0009`…`RES-0016`, `RES-0021`, `RES-0022`
**Corrida:** `data/corrida0/CALC-ENCIG-0001/`

> **CONGELADA EN EL COMMIT-1, ANTES DE ABRIR UN SOLO `conjunto_de_datos/*.csv`.**
> Lo único abierto al escribir: `data/manifiesto.yaml`, el descriptor
> `encig25_estructura_base_datos.pdf`, la lista de miembros del ZIP, el
> inventario de reactivos de la casa, `milpa/tramite.yaml` y
> `data/corrida0/demanda-*.tsv`. Ningún microdato.
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Las premisas del encargo que NO se sostienen (y ninguna bloquea)

| lo que el encargo declaró | lo real, verificado |
|---|---|
| «`CORR-0002`, **10** RESULT (`RES-0003/0004/0009–0016`)» | **12**. La ADENDA (3) lo corrige y la demanda vigente lo confirma: `+RES-0021`, `+RES-0022`. Enumerado en §1.4. |
| «`P0` · la derivación que etiquetó mal» | **SUPERSEDED**. `ACTO GEN2-PREP-LOTE` (`PR #662`) ya corrigió `_instrumento()`; ADENDA (2). No se toca. |
| «`COMPUERTA: GATED a … R-SERIE-DBF`» | reescrita por ADENDA (1) a «#661 **y** #662 fusionados». Ambos verificados **por producto** en el ARRANQUE. |
| «redactado contra `origin/main = 4497029a`» | base real al abrir: **`606f6ee`**. Re-derivado todo lo que depende del perímetro. |
| **«qué distingue la ronda base de la `_r2` (dos rondas del cuestionario)»** | **La premisa es falsa.** `_r2` **no** es una segunda ronda del cuestionario: ENCIG 2025 tiene **un** cuestionario. Son **dos corridas de la misma medición** sobre el mismo reactivo (`P8_4`), y lo único que las separa es la **deduplicación** — ver §3.4. Se declara aquí en vez de contestar una pregunta que el instrumento no plantea. |

Ninguna cifra del encargo se dio por buena sin comando.

### 0.2 · Cobertura retroactiva

`forense/prereg-caja/` — **0** aciertos de `encig` sobre el listado completo del
directorio (A.13: se examinó el directorio entero, no una muestra). La spec
**no existía**; producirla no duplica nada. Los doce valores GEN1 **sí**
existen y están sellados en `milpa/tramite.yaml` (líneas 60-61, 140-148,
348-349). **Lo que falta es la cadena, no los números.**

`tools/ya_medido.py` sobre las tres reglas — salida cruda en la nota de cierre —
resuelve `tramite.mordida.discrecional → R3.1`,
`tramite.mordida.con_registro → R3.2`,
`tramite.gobierno_digital.util_sin_coercion → R3.4`, las tres **ya medidas**
en `milpa/tramite.yaml`. Este acto **no descubre territorio virgen y no lo
presenta como tal**.

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Al congelar esta spec la sesión ya había leído, en el repo:

- **(a)** los doce valores GEN1, en el encargo y en `demanda-resultados.tsv`;
- **(b)** los IC95, las `n`, los conteos de estratos/UPM y el ponderador de las
  tres enmiendas, en `milpa/tramite.yaml`;
- **(c)** **la codificación GEN1 completa**: variable `P8_3_1` y regla
  `1=Sí / 2=No / 9 y resto fuera` para la familia A; `P8_4` × `P7_3` con
  `presencial={1}` y `digital={3,4,5}` para la familia B; `N_TRA=01` con
  `adopta={4,5}` y `rechaza={1,2,6}` sobre `P7_3∈{1,2,4,5,6}` para la familia C;
- **(d)** el diagnóstico de `MAESTRA35-L1` sobre la deduplicación de `r1`.

**Consecuencia deliberada, igual que en `ACTO GEN2-LOTE-ENVIPE-1`:** donde el
codebook admite más de una lectura, la **primaria de esta spec no es la de
GEN1** — se mide el juicio en vez de heredarlo:

- familia **A**: primaria `SOLANY` (los **tres** incisos del reactivo 8.3), no
  el inciso único `P8_3_1` de GEN1; `DELTA-SOLANY-SOL1` mide lo que vale la
  restricción (§3.2);
- familia **B**: primaria **`SD`** (sin deduplicar), porque el codebook declara
  `NT_TIPO` (*«Número de trámite / Último evento», 01-03*) precisamente para
  distinguir eventos repetidos del mismo tipo; la rama `CD` reproduce `r1`
  y se mide el delta (§3.4).

Lo genuinamente desconocido al congelar — y donde está el riesgo real — son:
el peso residual de las categorías de `P7_3` que el par presencial/digital
**no** usa; el peso de `{9, blanco}` en `P8_3_1`; la cobertura del join
`sec_7 × sec_8`; y si la llave declarada por el descriptor es la llave real.
**Ninguno aparece en fuente alguna leída.**

---

## 1 · Identidad

### 1.1 · Payload, por el manifiesto

- `id: encig25_base_datos_csv` · `archivo: encig25_base_datos_csv.zip`
- `sha256: 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`
  — **verificado byte a byte en la caja** contra el manifiesto.
- `tamano_bytes: 37624925` · `url_origen`
  `https://www.inegi.org.mx/contenidos/programas/encig/2025/microdatos/encig25_base_datos_csv.zip`
- **Estampa de universo, del propio manifiesto:** *«Universo: áreas urbanas de
  100 mil habitantes o más (82 áreas) — todo estimador derivado de este payload
  queda acotado a esa subpoblación, no a la nacional.»* Se hereda a **todos**
  los `RESULT` de esta spec, sin excepción.

### 1.2 · Ola, población y periodo, por el descriptor

`encig25_estructura_base_datos.pdf` (INEGI, *ENCIG. Estructura de la base de
datos. 2026*), §Presentación y §1.3:

> *«…la población de **18 años y más** en ciudades de **100 mil habitantes o
> más** sobre los trámites y servicios que proporcionaron los diferentes
> ámbitos de gobierno **durante 2025**.»*

Periodo de referencia de los reactivos de corrupción: **2025** (el propio
enunciado 8.3 dice *«Durante 2025»*).

### 1.3 · Tablas, unidad y ponderador — **declarado, porque cambia el denominador**

El descriptor §1.4 declara **tres** factores de expansión y esta spec usa dos:

| miembro del ZIP | contenido (descriptor §2.1) | unidad | ponderador | llave primaria DECLARADA |
|---|---|---|---|---|
| `encig2025_01_sec1_A_3_4_5_8_9_10.csv` | residentes, percepción de corrupción, corrupción y corrupción general (279 vars) | **PERSONA** (informante seleccionado, 18+) | `FAC_P18` | `CVE_ENT, UPM, V_SEL, R_ELE` |
| `encig2025_04_sec_7.csv` | calidad de los trámites realizados **de manera personal** (52 vars) | **TRÁMITE** | `FAC_TRA` | `CVE_ENT, UPM, V_SEL, R_ELE, N_TRA` |
| `encig2025_05_sec_8.csv` | *«percepción de corrupción»* (26 vars) | **TRÁMITE** | `FAC_P18` (el que trae la tabla) | `CVE_ENT, UPM, V_SEL, R_ELE, N_TRA` |

**El descriptor no menciona `ID_TRA` como llave** (sólo lo describe como
*«Identificador del trámite»*), y **omite `NT_TIPO` de la llave declarada** pese
a que lo define como *«Número de trámite / Último evento», códigos `01-03`*.
`ACTO MAESTRA35-L1` verificó contra el archivo que la llave única de `sec_7`
es `(ID_TRA, NT_TIPO)`. **Esta spec no adopta ninguna de las dos por
autoridad**: las verifica las dos, y el resultado es un `RESULT` (§3.5, G-2/G-3).

### 1.4 · Los 12 `RESULT` de `CORR-0002`, enumerados desde la demanda vigente

| `RESULT` | consumidor (`milpa/tramite.yaml`) | valor GEN1 | familia |
|---|---|---|---|
| `RES-0003` | `tramite.mordida.discrecional:paga_mordida_encig2025` | 0.085118 | **A** |
| `RES-0004` | `…:tramite_normal_encig2025` | 0.914882 | **A** (complemento) |
| `RES-0009` | `tramite.mordida.con_registro:paga_mordida_encig2025_presencial` | 0.116000 | **B** · `CD` · presencial |
| `RES-0010` | `…:tramite_normal_encig2025_presencial` | 0.884000 | **B** (complemento) |
| `RES-0011` | `…:paga_mordida_encig2025_digital` | 0.027358 | **B** · `CD` · digital |
| `RES-0012` | `…:tramite_normal_encig2025_digital` | 0.972642 | **B** (complemento) |
| `RES-0013` | `…:paga_mordida_encig2025_presencial_r2` | 0.141041 | **B** · `SD` · presencial |
| `RES-0014` | `…:tramite_normal_encig2025_presencial_r2` | 0.858959 | **B** (complemento) |
| `RES-0015` | `…:paga_mordida_encig2025_digital_r2` | 0.029868 | **B** · `SD` · digital |
| `RES-0016` | `…:tramite_normal_encig2025_digital_r2` | 0.970132 | **B** (complemento) |
| `RES-0021` | `tramite.gobierno_digital.util_sin_coercion:adopta_encig2025_luz` | 0.673393 | **C** |
| `RES-0022` | `…:rechaza_servicio_encig2025_luz` | 0.326607 | **C** (complemento) |

`CORR-0001` (ENCIG2023, sin payload, 4 `RESULT`) **no es de este lote**: ni se
mide ni se declara (ADENDA 3).

---

## 2 · Los reactivos, verbatim del descriptor

### 2.1 · Familia A — reactivo 8.3 (tabla PERSONA)

> **8.3 Durante 2025, para agilizar, realizar, evitar procedimientos o multas
> en alguno de estos trámites, pagos o solicitudes:**
>
> - `P8_3_1` *¿Un(a) servidor(a) público(a) o empleado(a) de gobierno **intentó
>   apropiarse o le solicitó de forma directa** algún beneficio (dinero, regalos
>   o favores) que usted pudiera otorgarle?*
> - `P8_3_2` *¿**Una tercera persona o coyote** le insinuó o pidió de forma
>   directa dinero, un regalo o favor para algún(a) servidor(a) público(a) o
>   empleado(a) de gobierno?*
> - `P8_3_3` *¿Un(a) servidor(a) público(a) o empleado(a) de gobierno **le
>   insinuó o generó las condiciones** para que le proporcionara dinero, un
>   regalo o favor para su persona?*
>
> Los tres: `1 Si` · `2 No` · `9 No sabe / no responde`.

**Dos hechos del codebook que la cifra GEN1 no dice:**

1. **8.3 es UNA pregunta con TRES incisos.** GEN1 usó sólo el inciso 1. Es un
   juicio defendible, no un dato: por `E.1`, GEN1 no elige la codificación de
   GEN2. Primaria = `SOLANY` (cualquiera de los tres = 1); `SOL1` (GEN1) queda
   como secundaria y `DELTA-SOLANY-SOL1` mide lo que vale la restricción.
2. **Ninguno de los tres mide *pagar*.** Los tres miden que **le solicitaron o
   insinuaron**. El consumidor se llama `paga_mordida`. El reactivo que mide
   entrega efectiva es **`P8_6`** (*«¿Cuál fue la cantidad aproximada que en
   total los(las) servidores(as) públicos(as) … se apropiaron…?»*, con
   `1 = No le dio nada`), y vive en **otra tabla y otra unidad**. Se mide como
   hallazgo con su propio denominador (§4, familia X) y **no** sustituye a
   ningún consumidor.

### 2.2 · Familia B — reactivo 8.4 (tabla `sec_8`) y 7.3 (tabla `sec_7`)

> **8.4 ¿En cuál de los trámites o servicios que usted hizo se suscitaron las
> anteriores circunstancias?** — `P8_4`: `1 Si` · `0 No` · `b blanco`.

Nótese que el «no» de `P8_4` es **`0`**, no `2`. Y *«las anteriores
circunstancias»* son las de 8.3: **`P8_4` sólo tiene sentido para quien ya
declaró algo en 8.3** — auto-selección que GEN1 declaró como reserva y que esta
spec **cuenta** (§3.3, `B-N-SEC7-SIN-PAREJA`, `B-COBERTURA`).

> **7.3 ¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el
> trámite o pago?** — `P7_3`:
> `1` Instalaciones de gobierno (oficinas, tesorería, hospital, etcétera) ·
> `2` Banco, supermercado, tiendas o farmacias ·
> `3` Líneas de atención telefónica ·
> `4` Internet (página web, aplicaciones de celular, tablet, etcétera) ·
> `5` Cajero automático o kiosco inteligente ·
> `6` Módulos, clínicas u oficinas temporales o móviles ·
> `7` No se ha podido concluir el trámite o pago ·
> `8` Otro · `9` No sabe / no responde · `b` blanco.

**`P7_3` tiene OCHO categorías sustantivas, no dos.** El par
presencial `{1}` / digital `{3,4,5}` de GEN1 usa **cuatro** y deja fuera `2`
(banco/tienda/farmacia) y `6` (módulos móviles), que son canales reales y
frecuentes. Igual que el hallazgo 3.2 del lote ENVIPE, **«presencial vs digital»
es una propiedad del RECORTE, no del instrumento** — y esta spec mide el peso
de lo que el recorte deja fuera antes de rotular nada.

### 2.3 · Familia C — `N_TRA` (tabla `sec_7`)

> `N_TRA` — *«Códigos para trámites»*, `01` = **el pago ordinario del servicio
> de luz**.

---

## 3 · Universos, codificación y unidad — todo pre-declarado

### 3.1 · Regla general

- Sumas ponderadas en **orden fijo de fila**. `p = Σ(w·d)/Σ(w)`.
- **Cero NUNCA sustituye falta de dato.** Blanco, `9`/`99` y no-numérico se
  **cuentan aparte** y salen del denominador; no se imputan.
- Escala de toda proporción: `[0,1]`. Dirección declarada por `RESULT`.
- Si falta una columna declarada → `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`; si
  existe y no tiene ningún valor válido → `NO-ESTIMABLE-COLUMNA-VACIA:<col>`;
  si un universo queda vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`.
- **`NO-APLICA` es un valor** y se escribe como tal.

### 3.2 · Familia A · unidad **PERSONA**, ponderador `FAC_P18`

- `U_A` = filas de `encig2025_01_sec1_A_3_4_5_8_9_10.csv` con
  `P8_3_1 ∈ {1,2}` **y** `FAC_P18` finito `> 0`.
- `d(SOL1) = 1` si `P8_3_1 = 1`, `0` si `P8_3_1 = 2`. **(codificación GEN1)**
- `d(SOLANY) = 1` si **alguno** de `P8_3_1, P8_3_2, P8_3_3` `= 1`; `0` si los
  tres están en `{2}`. Las filas con algún `9`/blanco en `P8_3_2`/`P8_3_3` pero
  `P8_3_1 ∈ {1,2}` **permanecen en `U_A`** y se cuentan aparte
  (`A-N-SOLANY-PARCIAL`): un `9` en un inciso no borra un `1` en otro, pero sí
  impide afirmar el `0`. Regla: si algún inciso `= 1` → `d = 1`; si ninguno
  `= 1` y **alguno** es `9`/blanco → la fila **sale** de `U_SOLANY` (contada);
  si los tres son `2` → `d = 0`.
- Residuo del reactivo, **contado**: `P8_3_1 ∈ {9}` (`A-N-P831-NSNR`) y
  `P8_3_1` blanco/no numérico (`A-N-P831-BLANCO`).
- **Dirección:** más alto = más solicitud de soborno declarada.

### 3.3 · Familia B · unidad **EVENTO DE TRÁMITE**, ponderador `FAC_TRA`

- Join `sec_7` (canal, `FAC_TRA`, diseño) **×** `sec_8` (`P8_4`) por `ID_TRA`.
- `U_B` = filas emparejadas con `P8_4 ∈ {0,1}` **y** `FAC_TRA` finito `> 0`.
- `d(B) = 1` si `P8_4 = 1`, `0` si `P8_4 = 0`. Blanco → fuera, contado.
- **Canales:** `PRE` = `P7_3 = 1`; `DIG` = `P7_3 ∈ {3,4,5}`.
  **Residuo de canal, contado y pesado:** `P7_3 ∈ {2,6,7,8,9,blanco}`
  (`B-N-RESIDUO-CANAL`, `B-P-RESIDUO-CANAL`).
- **Cobertura del join, contada:** `B-N-SEC7-FILAS`, `B-N-SEC8-FILAS`,
  `B-N-EMPAREJADAS`, `B-N-SEC7-SIN-PAREJA`, y `B-COBERTURA` =
  `B-N-EMPAREJADAS / B-N-SEC7-FILAS`. Si la cobertura es baja, el estimando
  **no** es `p(mordida | canal)` sobre el universo de trámites sino
  `p(este trámite fue el señalado | trámite de alguien que ya declaró en 8.3)`,
  y se rotula así en el veredicto, sin adornos.

### 3.4 · Familia B · las dos ramas, `SD` y `CD` — lo que de verdad separa base de `_r2`

| rama | qué hace | qué consumidor releva |
|---|---|---|
| **`SD`** (**PRIMARIA**) | **sin deduplicar**: cada fila de `sec_7` es un evento y entra una vez | `RES-0013`…`RES-0016` (`_r2`) |
| **`CD`** | **deduplica `sec_7` por `ID_TRA`**, conservando la primera fila en orden de archivo | `RES-0009`…`RES-0012` (base) |

`SD` es la primaria **por el codebook, no por GEN1**: el descriptor define
`NT_TIPO` (*«Número de trámite / Último evento», `01-03`*) exactamente para
distinguir eventos repetidos del mismo tipo hechos por la misma persona;
colapsarlos por `ID_TRA` borra eventos que el instrumento captó a propósito.
`B-N-EVENTOS-DESCARTADOS-POR-DEDUP` mide cuántos.

**Esto, y no «dos rondas del cuestionario», es lo que distingue base de `_r2`
(§0.1).** ENCIG 2025 tiene **un** cuestionario y **un** reactivo `P8_4`; las dos
cifras selladas salen del mismo reactivo medido dos veces con distinta regla de
deduplicación. Los consumidores base (`RES-0009`…`RES-0012`) son, por lo tanto,
**CONSTRUIBLES** — se reproducen con la rama `CD`. Ninguno se marca
`NO-CONSTRUIBLE`.

### 3.5 · Guardias de existencia y de llave — **paran, no adivinan**

Se corren **antes** de estimar y su salida es `RESULT`:

- **G-1** columnas declaradas presentes en los tres miembros → si no,
  `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`.
- **G-2** `G-LLAVE-SEC7-DECLARADA-UNICA`: ¿es `(CVE_ENT,UPM,V_SEL,R_ELE,N_TRA)`
  — la llave que **declara el descriptor** — única en `sec_7`?
- **G-3** `G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA`: ¿lo es `(ID_TRA,NT_TIPO)` — la que
  **verificó `MAESTRA35-L1`**?
- **G-4** `G-LLAVE-SEC8-IDTRA-UNICA`: ¿es `ID_TRA` única en `sec_8`? De ello
  depende que el join sea uno-a-muchos exacto.
- Las tres reportan `UNICA` o `NO-UNICA:<grupos>/<filas>`. **Ninguna corrige
  nada**: si la llave de `MAESTRA35-L1` no es única, el join se declara
  `JOIN-NO-EXACTO` y las ramas de B salen `NO-ESTIMABLE-LLAVE-NO-UNICA`.
  No se elige otra llave sobre la marcha.

### 3.6 · Familia C · unidad **TRÁMITE tipo `01`**, ponderador `FAC_TRA`

- `U_C` = filas de `sec_7` con `N_TRA = 1` **y** `P7_3 ∈ {1,2,4,5,6}` **y**
  `FAC_TRA` finito `> 0`. **Sin deduplicar** (misma razón que §3.4).
- `d(C) = 1` si `P7_3 ∈ {4,5}` (adopta) · `0` si `P7_3 ∈ {1,2,6}` (no adopta).
- Residuo, contado y pesado: `P7_3 ∈ {3,7,8,9,blanco}` (`C-N-RESIDUO`,
  `C-P-RESIDUO`). `3` = teléfono y `7` = trámite no concluido son categorías
  sustantivas que el universo GEN1 excluye.
- **Dirección:** más alto = más uso de canal digital/autoservicio.
- **Advertencia de rótulo, pre-declarada:** `d = 0` significa *«usó un canal
  físico»*, **no** *«rechazó un servicio digital»*. Se reporta como asociación
  descriptiva de canal. El propio `alcance` de la regla ya lo estampa: *«la
  condición sin coerción/sin riesgo fiscal la impone la construcción del
  universo, no el informante»*.

### 3.7 · Diseño: ponderador, estrato y UPM — **la lección de FP-201**

`EST_DIS` y `UPM_DIS` están declarados **en las tres tablas** por el descriptor
y confirmados por el inventario de reactivos de la casa. **La varianza de
diseño ES identificable y no se renuncia a ella.**

- **Método IC:** bootstrap de `UPM_DIS` **con reemplazo dentro de** `EST_DIS`,
  conservando el número de UPM por estrato; percentiles 2.5/97.5;
  **2 000 réplicas**, `numpy.PCG64`, semilla **`20260909`**.
- `EST_DIS`/`UPM_DIS` se tratan como **llaves de texto opacas**: nunca se
  convierten a entero ni se re-rellenan a un ancho tomado del descriptor
  (lección de `ACTO GEN2-LOTE-ENVIPE-1` §3.4 — el descriptor iba desfasado y
  normalizarlas habría partido estratos en silencio).
- **Estrato con una sola UPM:** se re-muestrea a sí mismo (varianza cero). No
  se colapsa (decisión de diseño que esta spec no está autorizada a tomar) ni
  se descarta (sesgaría el punto). Si el conteo es `> 0`, `METODO-IC` sale
  `IC-CON-ESTRATOS-DE-UPM-UNICA` y **el IC se lee como límite inferior de la
  anchura verdadera**, nunca como IC exacto.
- Filas sin `EST_DIS` o sin `UPM_DIS` se cuentan (`*-N-SIN-DISENO`): afectan al
  IC, **no** al punto.
- **Ranura no pre-registrada:** nadie pre-registró el método de IC para estas
  series. Lo elige el ejecutor sobre ranura vacía, se declara aquí y se eleva a
  mesa. **No se espera coincidencia dígito a dígito** de los extremos con los
  IC95 GEN1.

---

## 4 · Familia X · el pago efectivo (hallazgo, NO consumidor)

`P8_6` (tabla `sec_8`): `1 No le dio nada` · `2` hasta $200 · `3` $201-500 ·
`4` $501-1 000 · `5` $1 001-5 000 · `6` más de $5 000 · `7 Otros` ·
`9 NS/NR` · `b blanco`.

- `U_X` = filas de `sec_8` con `P8_6 ∈ {1,…,7}` y ponderador válido.
- `X-P-DIO-ALGO` = peso de `P8_6 ∈ {2,…,7}` sobre `U_X`.
- **Se reporta con su denominador escrito y NO releva a ningún `RESULT`.**
  Existe para contestar, con dato, si el rótulo `paga_mordida` describe lo que
  la celda sellada mide (§2.1, hecho 2). Su cita de adopción está **prohibida**.

---

## 5 · Ramas pre-declaradas — escritas ANTES del dato

### 5.1 · Control positivo contra GEN1 (`REPRODUCE-GEN1`)

Para cada uno de los **seis** consumidores «positivos» se calcula
`DELTA-VS-GEN1 = medido − sellado` **con signo**, y:

`REPRODUCE` si `|delta| ≤ 1e-6` · `NO-REPRODUCE` en otro caso ·
`NO-COMPARABLE` si el estimando salió `NO-ESTIMABLE`.

| celda de esta spec | valor GEN1 |
|---|---|
| `A-P-SOL1` | 0.085118 |
| `B-P-PRE-CD` | 0.116000 |
| `B-P-DIG-CD` | 0.027358 |
| `B-P-PRE-SD` | 0.141041 |
| `B-P-DIG-SD` | 0.029868 |
| `C-P-ADOPTA` | 0.673393 |

**`NO-REPRODUCE` no invalida la corrida, no autoriza tocar el medidor y no se
ajusta hacia atrás**: se reporta con el embudo completo a la vista.

### 5.2 · Exhaustividad de cada par (`VEREDICTO-EXHAUSTIVIDAD`)

Para cada familia se mide el **peso residual** de las categorías del reactivo
que el denominador del par excluye, y se emite:

- `EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO` si el residuo pesa exactamente `0`;
- `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE` si pesa `> 0`.

### 5.3 · Criterio de adopción de P3, pre-declarado (patrón `NC-0085`)

Un `RESULT` es **`CANTIDAD-MEDIDA`** — y sólo entonces se le escribe cita
`corrida0_resultado_id` + `corrida0_generacion: GEN2` en `milpa/tramite.yaml` —
si cumple **las dos**:

1. su numerador es una **categoría declarada del reactivo, contada
   directamente** (no `1 −` otra cosa), y
2. reproduce el valor sellado al **grano de `milpa/`, seis decimales**
   (`ADOPCION-DELTA = round(medido, 6) − sellado`, `= 0`).

Es **`COMPLEMENTO-CON-DENOMINADOR-RECORTADO`** — **sin cita**, y con fila `NC`
de advertencia — si se obtiene como `1 − p` sobre un denominador que excluye
categorías sustantivas del reactivo (residuo `> 0` por §5.2).

Bajo este criterio, **pre-declarado antes de medir**, los candidatos a cita son
los seis positivos de §5.1 (`RES-0003`, `RES-0009`, `RES-0011`, `RES-0013`,
`RES-0015`, `RES-0021`) y los seis complementos (`RES-0004`, `RES-0010`,
`RES-0012`, `RES-0014`, `RES-0016`, `RES-0022`) quedan sin cita **si y sólo si**
su residuo pesa `> 0`. **La medición decide, no esta lista.**

### 5.4 · La diferencia presencial − digital

`B-DIFERENCIA-PRE-DIG-SD` y `B-RAZON-PRE-DIG-SD` se emiten **rotulados
`ASOCIACION`**. La elección de canal y la elegibilidad por canal confunden la
comparación: quien puede hacer un trámite por internet no es una muestra
aleatoria de quien lo hace en ventanilla. **Ningún `RESULT` de esta spec es
causal**, y la regla `falsable_si` del motor no se declara probada por esta
corrida.

---

## 6 · Límites declarados (van también en la nota de cierre)

- **Geográfico.** 82 áreas urbanas de 100 mil habitantes o más. **No nacional.**
- **Poblacional.** 18 años y más, informante seleccionado.
- **Temporal.** ENCIG 2025, referencia 2025. No valida transferencia a otras
  olas ni a las siete olas de `serie_olas`, que no se tocan.
- **Causalidad: ninguna.** Todos los desenlaces son **declarados** por la
  persona.
- **No se calibra contra el marco.** Ninguna celda `M` se usa para calibrar;
  el marcador, las capturas y los `CALC-R` no se tocan.
- **Reserva heredada y no resuelta:** `P8_4` se pregunta sobre un subconjunto
  auto-seleccionado por 8.3. Se **cuenta** (§3.3) y se declara; **no** se
  corrige, porque corregirlo exigiría un universo que el instrumento no da.

---

## 7 · Congelamiento

Esta spec, `data/corrida0/CALC-ENCIG-0001/spec.yaml` y
`data/corrida0/CALC-ENCIG-0001/medidor.py` se congelan en el **COMMIT-1** de
`ACTO GEN2-LOTE-ENCIG-1`, **antes de abrir un solo `conjunto_de_datos/*.csv`**.
El COMMIT-2 corre `preflight → run → verify` y **no edita el COMMIT-1**.

**El primer resultado que produzca este procedimiento es el que se reporta.**
