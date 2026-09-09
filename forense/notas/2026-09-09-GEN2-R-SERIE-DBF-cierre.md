# `ACTO GEN2-R-SERIE-DBF` · cierre — el trío viejo reproduce al bit, y la serie llega a siete puntos

**Acto:** `ACTO GEN2-R-SERIE-DBF · LA SERIE SE CERTIFICA DE CERO, TRÍO VIEJO`, 9/sep/2026.
**Caja:** Ubuntu (WSL2) con corpus montado, Opus, sobre `4497029`.
**Compuerta:** `GATED a PR del ACTO GEN2-R-SERIE-CSV fusionado` — **CUMPLIDA**, verificada
por producto (`R-ENVIPE-SERIE-spec-v1_0.md` y los tres `CALC-R-CIV-M-{10,12,13}/spec.yaml`
en `origin/main`; `4497029` ancestro; `## CONSUMIDO` del encargo CSV citando `PR #657`),
nunca por `grep` del rótulo (`ADR-277`).

---

## 1 · Los tres `R` con cadena, y el veredicto de los tres controles

| celda | ola | delitos de | `R` (primario, `U_R`, `FAC_DEL`) | `EE` | IC95 | `CV` | `N` | control vs GEN1 |
|---|---|---|---|---|---|---|---|---|
| `CIV-M-01` | ENVIPE 2012 | 2011 | `0.25899878251638075` | `0.006970703455227148` | `[0.2453364547940205, 0.272661110238741]` | 2.69% | 26 848 | **`REPRODUCE`**, Δ `+0` |
| `CIV-M-02` | ENVIPE 2013 | 2012 | `0.24339981393062482` | `0.0062378246817035195` | `[0.23117390220974182, 0.2556257256515078]` | 2.56% | 40 889 | **`REPRODUCE`**, Δ `+0` |
| `CIV-M-04` | ENVIPE 2015 | 2014 | `0.24366832225578466` | `0.007483508419929803` | `[0.229000915271278, 0.25833572924029136]` | 3.07% | 39 286 | **`REPRODUCE`**, Δ `+0` |

`preflight` VERDE → `run` → `verify` **`REPRODUCE`** con `CONTEXTO=IDENTICO` en las tres.
`VEREDICTO-CV = CV-ACEPTABLE` en las tres.

El control positivo es **externo y posterior**: lo corre
`forense/prereg-caja/R-ENVIPE-SERIE-DBF-control-gen1.py`, **después** de que existieran los
tres `sello.json`. Los tres medidores no abren `corridas-R/` ni reciben el valor GEN1 por
ningún parámetro. **Delta `+0` exacto en las tres**, igual que en el trío moderno.

Coinciden además, sin que ninguna fuera objetivo: `EE`, los dos extremos del IC,
`n_efectivo` (26 848 / 40 889 / 39 286), `n_estratos` (358 / 268 / 238),
`n_estratos_singleton` (30 / 4 / 3), `n_upm_total` (9 129 / 10 526 / 9 477),
`n_filas_leidas` (32 493 / 47 117 / 44 699) y `n_codigo_no_valido`
(5 645 / 6 228 / 5 413, que aquí sale partido en `99` + blanco).

---

## 2 · El hallazgo del lote: **`BPCOD` está corrido un lugar en 2012**

`BP1_23` —el reactivo— es **idéntico** en las tres olas: mismo nombre, tipo `C 2`, y los once
códigos `01…09 · 99 · b` con las mismas etiquetas. Ahí no había nada que mapear.

Lo que sí cambia es **`BPCOD`**, que define el universo secundario `U1`:

- **2013 y 2015** traen quince códigos, `01…15`, idénticos al catálogo moderno; bloque
  personal `{05,…,15}`.
- **2012** trae **catorce**, `01…14`. No existe el código de vandalismo, y su `03` es «Robo en
  su casa habitación» mientras que su `04` ya es «Robo o asalto en la calle» — un delito
  **personal**. Bloque hogar `{01,02,03}`, bloque personal `{04,…,14}`.

Las **once parejas de etiquetas**, lado a lado y con su cita exacta, están verbatim en
`forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md` §3.1. El bloque personal de 2012
equivale **uno a uno y en orden** al `{05,…,15}` moderno.

**Residuo, con su razón completa** (§3.2): el código moderno `03` (vandalismo) no tiene
contraparte en 2012, pertenece al **bloque hogar**, y `U1` excluye el bloque hogar **por
construcción** — luego el residuo es **nulo sobre el universo secundario**. Ninguna fila que
`U1` habría contado en 2013/2015 queda sin contraparte en 2012, y ninguna fila de 2012 entra a
`U1` sin pareja.

### 2.1 · El corrimiento se falsa **por estructura, sin usar ningún resultado**

La contaminación declarada prohíbe validar el mapeo contra resultados. Cada corrida emite
`PERFIL-BPCOD`: la distribución de `BPCOD` código por código, **sin ponderador y antes de todo
filtro**.

| ola | `PERFIL-BPCOD` |
|---|---|
| 2012 | `01=1655;02=7316;03=5161;04=5066;05=1227;06=1407;07=1107;08=5095;09=2294;10=1063;11=81;12=790;13=74;14=157` |
| 2013 | `01=1588;02=8726;03=9857;04=6266;05=5821;06=434;07=1551;08=1707;09=6388;10=3038;11=1012;12=82;13=485;14=81;15=81` |
| 2015 | `01=1131;02=7685;03=8279;04=5651;05=5357;06=1482;07=1539;08=1699;09=7113;10=3022;11=950;12=81;13=552;14=67;15=91` |

**2012 no tiene código `15` y las otras dos sí.** El catálogo declarado y el archivo coinciden
en las tres. Si el corrimiento estuviera mal, esta tabla lo delataría, y no participa ningún
estimando en la comprobación.

---

## 3 · El diseño cambia de **nombre**, no de existencia — y eso pudo costar dos olas

La guardia de columna ausente de la familia nombra `EST_DIS` y `UPM_DIS`. En **2012 y 2013 esas
columnas no existen con ese nombre**: se llaman `EST` (`C 3`) y `UPM` (`C 5`). Aplicar la
guardia por nombre literal habría declarado `NO-ESTIMABLE` dos de las tres olas por un **falso
negativo de nombre**, con el dato entero disponible en el archivo.

La guardia **no se editó**. Cada `spec.yaml` declara un vínculo `rol → nombre físico`
(`parametros.mapa_columnas`) y el medidor no conoce ningún nombre por su cuenta. Es sucesión,
no reescritura: `R-ENVIPE-SERIE-spec-v1_0.md` queda intacta byte a byte.

Dos trampas más del mismo tipo, ambas declaradas antes de medir:

- **`FAC_DEL` cambia de tipo**: `Caracter(6)` en 2012/2013, `Numerico(12)` en 2015. El medidor
  lee **todo campo DBF como texto crudo** y convierte después, así que el tipo declarado en la
  cabecera no puede mover el resultado.
- **En 2015 conviven `UPM` (`C 7`) y `UPM_DIS` (`C 5`) y no son la misma columna.** Se usó
  `UPM_DIS`, unidad primaria de **diseño**, como manda el descriptor (p. 50) y como hizo GEN1.

`PERFIL-DISENO` salió limpio en las tres: estrato `len3` y UPM `len5` en todas las filas del
universo, **sin espacios en los bordes**. A diferencia de las olas CSV, aquí el descriptor **no
mintió** sobre la longitud de las llaves opacas.

`PERFIL-DBF` registra lo que el lector vio en cada archivo: `0` registros borrados y `0`
truncados en las tres, y `n_leidos` igual a `nrec_cabecera` en las tres. Diferencia registrada y
no corregida: **codepage `0x03` en 2012 y 2013, `0x00` en 2015**.

---

## 4 · La premisa (3) del encargo no se sostiene — y se corrige con número

El encargo declara que `data/inventario-reactivos-v1_2.tsv` «trae **0 filas `BP1_2x`** para
`envipe_2013` y `envipe_2015`» y que «el inventario **NO cubre** los payloads DBF». Medido
contra el árbol:

| instrumento | filas | `BP1_2*` | `BP1_23` | `texto_reactivo` no vacío |
|---|---|---|---|---|
| `envipe2012` | 400 | 12 | 1 | **0** |
| `envipe2013` | 419 | 11 | 1 | **0** |
| `envipe2015` | 485 | 11 | 1 | **0** |

El inventario **sí** cubre las tres olas a nivel de **presencia de columna**
(`metodo = INSPECT_ZIP`, `universo_declarado = PRESENTE_EN_DATA_RAW`), con `BP1_23`, `BP1_20`,
`BPCOD`, `FAC_DEL` y el diseño **bajo su nombre correcto por ola**. Por eso
`corrida0 spec-check` verifica las seis columnas de cada `CALC` contra él y da **6 OK · 0 FAIL
en los tres**: un control positivo mecánico que el encargo daba por no disponible.

Lo que el inventario **no** trae es `texto_reactivo`, **vacío en las 1 304 filas**: inventaría
nombres de columna, no reactivos. Así que la instrucción operativa del encargo sigue siendo
correcta **por la razón que importa** —el catálogo de códigos y las etiquetas salieron del
codebook de cada ola, que es lo único que podía darlos— pero su afirmación literal sobre las
filas es falsa y **no se hereda**.

---

## 5 · La serie completa hasta hoy — **siete puntos**, sólo en el estimando secundario homologado

Eje: **año de DELITO**, no nombre de ola. Codificación `C1` y universo `U1` de
`prereg-caja-ENVIPE-DENUNCIA` en los siete puntos. IC por el **mismo bootstrap** de UPM en
estrato, **semilla `20260909`, 2 000 réplicas**, en los siete.

| año de delito | ola | `p(C1,U1)` | IC95 (bootstrap) | `N-U1` | origen |
|---|---|---|---|---|---|
| **2011** | ENVIPE 2012 | `0.29557241046799515` | `[0.27891134759227953, 0.3121719247213795]` | 14 532 | este acto ⚠️ **costura** |
| **2012** | ENVIPE 2013 | `0.29308206937572356` | `[0.2760974416310341, 0.31000900392370456]` | 16 411 | este acto |
| **2014** | ENVIPE 2015 | `0.2852054204148126` | `[0.2676350408114433, 0.3052034687005675]` | 17 393 | este acto |
| **2020** | ENVIPE 2021 | `0.239889932104125` | `[0.2283500030048174, 0.2512259782295049]` | 16 798 | `GEN2-R-SERIE-CSV` |
| **2022** | ENVIPE 2023 | `0.2437993175187952` | `[0.232411106714311, 0.25591090294323354]` | 16 283 | `GEN2-R-SERIE-CSV` |
| **2023** | ENVIPE 2024 | `0.22694480140329618` | `[0.2131119926277141, 0.24113708076566334]` | 17 297 | `GEN2-R-SERIE-CSV` |
| **2024** | ENVIPE 2025 | `0.23168863494549488` | `[0.21919101986211595, 0.24446191145648544]` | 20 225 | `CALC-ENVIPE-0001`, leído |

⚠️ **La costura del punto 2011 va visible, como mandó dirección.** Su `U1` se construyó con el
bloque personal `{04,…,14}` por el corrimiento de §2, no con `{05,…,15}`. El residuo es nulo
sobre `U1` (§2), pero el punto lleva la marca para que nadie lo lea como si el instrumento
hubiera sido el mismo.

**Lo que se puede decir y lo que no.** El recorrido de los siete puntos es `0.0686`
(`0.29557` en 2011, `0.22694` en 2023), y las anchuras de IC van de `0.0229` a `0.0376`: a
diferencia de los cuatro puntos modernos —cuyo recorrido entero cabía dentro de un solo
intervalo— **aquí el recorrido no cabe**. Los tres puntos viejos (`0.285`–`0.296`) y los cuatro
modernos (`0.227`–`0.244`) están en niveles distintos, y esa diferencia **no** es artefacto del
corrimiento de 2012: 2013 y 2015 ya traen el catálogo moderno y quedan igual de arriba.

Y aun así, **la serie se publica descriptiva y no adjudicada**. Entre 2014 y 2020 hay **seis
años de delito sin medir** (olas 2011, 2014, 2016, 2017, 2018, 2019, 2020 y 2022): cualquier
lectura de forma sobre este salto es lectura sobre un hueco. Transferencia y estabilidad
temporal se contratan en `F5`. **Ningún `RESULT` es causal**: la razón principal es lo que la
persona **declaró**.

### 5.1 · Lo que vale el código `08`, medido en cada ola del trío viejo

`DELTA-C2-C1` es lo que cambia el punto si «actitud hostil de la autoridad» se reclasifica como
desconfianza:

| ola | `p(C1,U1)` | `p(C2,U1)` | `DELTA-C2-C1` |
|---|---|---|---|
| 2012 | `0.29557241046799515` | `0.32851321938371886` | `+0.03294080891572371` |
| 2013 | `0.29308206937572356` | `0.34017303288920003` | `+0.04709096351347647` |
| 2015 | `0.2852054204148126` | `0.35409381581701865` | `+0.06888839540220604` |

El peso del código `08` **crece monótonamente** en el trío viejo y es en 2015 el doble que en
2012. Se reporta como medición, no como tendencia adjudicada.

---

## 6 · `U4` no se midió, y la razón está declarada

`prereg-caja-ENVIPE-DENUNCIA` define un `U4` (unidad persona, `ID_PER`, `FAC_ELE`,
`tper_vic2`). **La familia `R-ENVIPE-SERIE` no lo mide**: sus dos estimandos son de unidad
delito sobre `tmod_vic` con `FAC_DEL`, y ningún `RESULT` del trío CSV toca `tper_vic2`. Luego,
para las tres olas de este acto, la guardia de `tper_vic2` es **`NO-APLICA`** — valor declarado,
no omisión (`D-15`).

Se deja escrito además, porque un sucesor lo va a necesitar: si alguna vez se pidiera `U4` en
estas olas, **2015 podría** (`TPer_Vic2.dbf` trae `ID_PER` `C 16` y `FAC_ELE` `N 12`) y **2012
no**. Su `tper_vic.dbf` tiene **311 436 filas — las mismas que `tsdem.DBF`**, es decir el censo
completo del hogar y no la persona seleccionada, y **no trae `N_REN`**: ningún campo dice qué
renglón es esa fila. Aislar a la persona seleccionada exigiría un join a `tsdem` por
`N_REN == R_SEL` que ninguna spec de esta familia declara. Fuente: `FD_ENVIPE_2012.xls`, hoja
`TPer_Viv`. Esa ruta **no se improvisó**: es fila `NC` con sucesor.

---

## 7 · Contadores

`cuenta_gen2 = SI` en los tres `CALC`, escrita con la firma de mesa verbatim y su OBJETO
explícito. **El merge la perfecciona.**

Contadores de la suite movidos por este acto (`T-CORRIDA0::T-STATUS-SMOKES`):
`N_corridas_selladas` 11 → **14** · `N_resultados_sellados` 901 → **1021** ·
`N_resultados_gen2_sellados` 631 → **751**. El trío DBF emite **40** `RESULT` por corrida y no
38: añade `PERFIL-DBF` y `PERFIL-BPCOD`, y renombra `N-BPCOD-01-04`/`-05-15` a
`N-BPCOD-HOGAR`/`-PERSONALES` precisamente porque en 2012 esos rangos no significan lo mismo.

`python3 tests/check.py --baseline` → **LÍNEA BASE VERDE**, nada nuevo frente a
`tests/baseline.json`.

---

## 8 · Lo que este acto NO hizo, con su razón

Ni un `RESULT` de `U4`. Ni un byte de `milpa/`, del marcador o de las capturas `L`. Ni una
edición a `R-ENVIPE-SERIE-spec-v1_0.md` ni a los JSON GEN1: los tres siguen con sus bytes
intactos y su `sha256` original. Ninguna adopción —los seis `R` esperan a `F3`, por lote y con
firma de mesa—, ninguna transferencia, ninguna estabilidad temporal adjudicada. Y **ninguna
reparación del inventario de reactivos**: aunque §4 muestra que cubre más de lo que el encargo
suponía, lo que le falta (`texto_reactivo`) sigue faltando, y repararlo es acto propio.

`FP-370` sigue **ABIERTA** y ahora gatea también la lectura del estatus del insumo de estas tres
celdas: `codificacion-R-v1_0.tsv`, de donde salen la codificación, el universo, el ponderador y
el diseño de las seis, continúa en estado `PROPUESTA`. Ninguna cifra de los seis `CALC` cambia
por eso; lo que cambia es el estatus del insumo.
