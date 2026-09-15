# ENCIG 2023 · la mordida por canal de trámite — pre-registro congelado de `CALC-ENCIG-2023-0001`

### `prereg-caja-ENCIG-MORDIDA-2023` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENCIG-MORDIDA-2023-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENCIG-MORDIDA-2023`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **en NUBE y antes de abrir un solo byte de microdato**, de `CALC-ENCIG-2023-0001`: el **mismo estimando** que la familia **B** de `CALC-ENCIG-0001` (`prereg-caja-ENCIG-MORDIDA`, v1.0) midió sobre ENCIG 2025 — proporción ponderada de **eventos de trámite** con `P8_4 = 1`, partida por canal (`P7_3`), ponderada por `FAC_TRA`, con IC95 de diseño — **medido sobre la ola 2023**. Sucesora en el sentido de `E.3`: no reescribe ni un byte de la v1.0 sellada. |
> | **QUÉ NO ES** | **No es un estimando nuevo.** No cambia universo, codificación, ponderador, canal ni método de IC respecto de la familia B de la v1.0; lo único que cambia es la **ola**. No mide la familia **A** (reactivo 8.3, unidad persona), ni la **C** (`N_TRA` = 01, adopción digital), ni la **X** (`P8_6`) — §5. No promedia olas, no construye serie, no ajusta tendencia, no extrapola de 2025 a 2023 ni al revés. **No adopta nada a `milpa/`** y no escribe cita bajo ninguna rama. No corre el medidor y **no escribe `medidor.py`**. |
> | **VERIFICAS ASÍ** | CAJA confirma, **antes de estimar**, que las trece columnas declaradas existen en los dos miembros nombrados; que la **llave del join** es única donde esta spec dice que debe serlo; y que `FAC_TRA` se leyó **de `sec_7`** y no el `FAC_P18` que trae `sec_8`. Cualquiera de las tres que falle **para** con un `NO-ESTIMABLE` nombrado, en vez de producir una cifra parecida a la correcta. |

**Acto:** `ACTO GEN2-FIRMAS-MESA-1`, 15/sep/2026, entorno **NUBE** (`data/raw/` **ausente**, corpus `montado=NO`, `numpy`/`pandas`/`pyreadstat` **ausentes**, `archivos_examinados = 0`), sobre `2b65202d615d8f5f14f3ec6d09e2778bf4ec4a09`.

**Firma que la autoriza, verbatim:** «Si a todas.» — mesa, 15 de septiembre de 2026, sobre la HOJA DE FIRMAS DE MESA 2026-09-15, archivada por `A.3` en `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`. **OBJETO 4**, transcrito íntegro: *«D1 / NC-0197 — opción (b): medir ENCIG 2023 con spec sucesora de `CALC-ENCIG-0001`. Spec aquí; corrida en caja.»*

**Base inmutable:** `forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`, `sha256 00c7c4a67a4a579fff8a64c01979deefe2d458c75cfbaa630de21fa05d37cf8a` (`prereg-caja-ENCIG-MORDIDA`), y su ratificación de método de IC `…-spec-v1_1.md`.

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · La frase falsa que esta spec corrige **sin reescribir el sello**

`ENCIG-MORDIDA-spec-v1_0.md:142` dice, dentro de un documento sellado:

> *«`CORR-0001` (ENCIG2023, **sin payload**, 4 `RESULT`) no es de este lote: ni se mide ni se declara (ADENDA 3).»*

`NC-0197` (`forense/no-corrido.tsv:193`) registra que esa frase es **FALSA EN LA LETRA desde el 29/jul/2026**: el payload de ENCIG 2023 está en `data/manifiesto.yaml` desde esa fecha, **en cinco formatos** (CSV, RData, DBF, DTA, SAV). La misma `NC` registra que **no se edita**: `E.3`, lo sellado no se reescribe.

**Esta spec es el vehículo correcto de esa corrección, y se dice explícitamente aquí:** la v1.0 conserva su letra, su `sha256` y su identidad de input; lo que estaba mal no era el juicio del ejecutor de septiembre (que no tenía el payload en su perímetro) sino un hecho que caducó — y un hecho que caducó se corrige **con una sucesora fechada que mide lo que la frase declaró no medible**, no con un `sed` sobre el sello. Ninguna línea de la v1.0 ni de la v1.1 cambia por este acto.

### 0.2 · A.8 — qué ya existe, y por qué esto no es un duplicado

`CALC-ENCIG-0001` midió la familia B sobre **ENCIG 2025** y produjo, sellado:

| `RESULT` | valor |
|---|---|
| `RESULT-ENCIG-MOR-B-P-PRE-SD` | `0.1410407168724654` |
| `RESULT-ENCIG-MOR-B-P-DIG-SD` | `0.029867554626649372` |

con `n = 11167` y `n = 7219` eventos respectivamente (`milpa/tramite.yaml:185,187`). **Ese es otro payload y otra ola.** Nada de lo que produzca esta spec re-mide, contradice ni reabre aquello: `CALC-ENCIG-0001` sigue vigente, sellado y citado donde está citado. Lo que aquí se abre es la ranura que la ADENDA 3 de la v1.0 dejó explícitamente vacante.

En `forense/prereg-caja/` no existe ninguna spec sobre ENCIG 2023 (directorio listado entero, `A.13`): las únicas dos que dicen `ENCIG` son la v1.0 y la v1.1 de `prereg-caja-ENCIG-MORDIDA`, ambas sobre 2025.

### 0.3 · El entorno, dicho sin disfraz

Esta spec se redacta en **NUBE**. `data/raw/` **no existe**, el corpus no está montado y `numpy`, `pandas` y `pyreadstat` están **ausentes**. `E.5` permite en nube abrir **codebook y metadato**, y nada más. **Cero bytes de microdato se abrieron para escribirla.** Toda afirmación de §1 sobre qué columnas existen y en qué archivo viven está anclada a `data/inventario-reactivos-v1_2.tsv` — un inventario a nivel de **columna** producido por inspección real de los ZIP (`metodo = INSPECT_ZIP`) — y a `data/manifiesto.yaml`. Donde el inventario calla, esta spec **pone una guardia, no una suposición**.

---

## 1 · A.15 — identidad y reactivos, verificados **por archivo**

### 1.1 · El payload, resuelto por manifiesto

| | |
|---|---|
| `payload_id` | **`encig23_base_datos_csv`** (`data/manifiesto.yaml:28`) |
| archivo | `encig23_base_datos_csv.zip` |
| `sha256` | `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d` |
| bytes | 38 309 647 |
| `fecha_descarga` | `2026-07-29` |
| formato | ZIP con **6** CSV |

El manifiesto registra además **cuatro gemelos** del mismo microdato — `RData`, `DBF`, `DTA`, `SAV` — y un sexto ZIP distinto (`encig2023_datosabiertos_csv.zip`, 26 171 769 bytes, `sha256 4e3839cd…`) que el propio manifiesto declara **NO coincidente** con éste. **Esta spec abre exactamente un payload: `encig23_base_datos_csv`.** Ningún gemelo entra, ni como respaldo ni como contraste: son formatos distintos del mismo dato y mezclarlos es cómo se fabrica un `sha256` que no corresponde a lo medido (`A.7`).

El `sha256_12` del inventario para las filas de este instrumento es **`af733d867a56`** — prefijo exacto del `sha256` del manifiesto. El inventario se derivó **del mismo archivo** que CAJA va a abrir.

### 1.2 · Los dos miembros, nombrados verbatim

El inventario resuelve **460 filas de columna** bajo `af733d867a56`, repartidas en los seis miembros del ZIP. Los dos que esta spec abre:

| miembro | columnas indexadas | unidad | qué aporta |
|---|---|---|---|
| `encig2023_04_sec_7.csv` | **51** | **EVENTO DE TRÁMITE** | canal (`P7_3`), ponderador (`FAC_TRA`), diseño (`EST_DIS`, `UPM_DIS`), llaves |
| `encig2023_05_sec_8.csv` | **25** | **EVENTO DE TRÁMITE** | desenlace (`P8_4`), llaves, diseño |

Los otros cuatro (`encig2023_01_sec1_A_3_4_5_8_9_10.csv` con 267 columnas, `encig2023_01_sec_11.csv` con 69, `encig2023_02_residentes_sec_2.csv` con 25, `encig2023_03_sec_6.csv` con 23) **no se abren**.

### 1.3 · Las columnas, verificadas una por una

`encig2023_04_sec_7.csv`, inventario completo de sus 51 columnas:

```
AREAM CVE_ENT CVE_MUN EST_DIS FAC_TRA ID_PER ID_TRA ID_VIV NOM_AREAM NOM_ENT
NOM_MUN NT_TIPO N_TRA P7_1 P7_10 P7_11 P7_11_3_ES P7_11_ESP P7_12 P7_12A P7_2
P7_3 P7_3_ESP P7_4_01…P7_4_11 P7_5A_A P7_5A_M P7_5B_D P7_5B_M P7_5C_D P7_5D_H
P7_5D_M P7_6 P7_7 P7_8 P7_9 R_DEF R_ELE TT_TIPO UPM UPM_DIS V_SEL
```

`encig2023_05_sec_8.csv`, inventario completo de sus 25 columnas:

```
AREAM CVE_ENT CVE_MUN EST_DIS FAC_P18 ID_PER ID_TRA ID_VIV NOM_AREAM NOM_ENT
NOM_MUN N_TRA P8REG_4 P8_4 P8_4_ESP P8_5 P8_6 P8_6_ESP P8_7 P8_7_TXT R_DEF
R_ELE UPM UPM_DIS V_SEL
```

| variable | miembro | papel |
|---|---|---|
| **`P8_4`** | `sec_8` | **desenlace** — 8.4, *«¿en cuál de los trámites se suscitaron las anteriores circunstancias?»*; `1 = Sí`, `0 = No`, blanco fuera |
| **`P7_3`** | `sec_7` | **canal** — `presencial = {1}`, `digital_registrado = {3,4,5}`, residuo contado |
| **`FAC_TRA`** | **`sec_7`** | **ponderador de evento de trámite** |
| `EST_DIS`, `UPM_DIS` | ambos | estrato y UPM — **llaves de texto opacas** |
| `ID_TRA` | ambos | llave del join |
| `ID_VIV`, `ID_PER`, `N_TRA` | ambos | llave de control del join |
| `NT_TIPO` | **sólo `sec_7`** | número de evento del trámite; separa la rama `SD` de la `CD` |
| `UPM`, `V_SEL`, `CVE_ENT`, `R_ELE` | ambos | llave declarada alternativa (guardia) |

**Ninguna columna de esta spec se infiere de la ola 2025.** Las trece se leyeron del inventario de 2023.

### 1.4 · Hecho central 1 — **el ponderador vive en `sec_7`, y se declara como parámetro**

`FAC_TRA` aparece en `encig2023_04_sec_7.csv` y **NO aparece en `encig2023_05_sec_8.csv`**. Lo que `sec_8` trae es **`FAC_P18`**, que es **otro ponderador sobre otro universo** (persona de 18+ seleccionada), no el de evento de trámite.

Esto no es un detalle de implementación: **resolver el ponderador por nombre de variable sobre la tabla unida tomaría el equivocado sin avisar** y produciría una cifra plausible, del orden correcto y falsa. `A.15(c)`, en su forma más cara. Por eso:

> **`archivo_de_ponderador: encig2023_04_sec_7.csv` es un PARÁMETRO explícito del contrato.** El medidor toma `FAC_TRA` **de ese archivo, por archivo y no por nombre**. `FAC_P18` de `sec_8` **no entra en ningún estimando de esta spec**, ni como respaldo si `FAC_TRA` faltara: si `FAC_TRA` falta, el `RESULT` sale `NO-ESTIMABLE-COLUMNA-AUSENTE:FAC_TRA`. **No hay sustituto.**

### 1.5 · Hecho central 2 — **la medición exige un JOIN, y la llave se declara**

`P7_3` (canal) vive en `sec_7`. `P8_4` (mordida por trámite) vive en `sec_8`. **No hay ningún miembro del ZIP que traiga las dos.** Por lo tanto el estimando **no es construible sin unir las dos tablas**, y la llave del join es parte del contrato, no del medidor:

- **LLAVE PRIMARIA DEL JOIN: `ID_TRA`.** Es la misma que usó `CALC-ENCIG-0001` sobre 2025 (§3.3 de la v1.0) y está presente en los dos miembros de 2023. Se elige **por continuidad del estimando**: cambiar la llave cambiaría qué filas se emparejan y, con ello, el estimando — que es precisamente lo que esta sucesora tiene prohibido cambiar.
- **LLAVE DE CONTROL: `(ID_VIV, ID_PER, ID_TRA, N_TRA)`.** Las cuatro están en los dos miembros. Se computa **también**, y su resultado es un `RESULT` (`G-JOIN-LLAVE-CONTROL-COINCIDE`), no una corrección: si las dos llaves emparejan conjuntos distintos de filas, **el join se declara `JOIN-NO-EXACTO` y las ramas de B salen `NO-ESTIMABLE-LLAVE-NO-UNICA`**. No se elige la llave que dé más filas.
- **Si `ID_TRA` no es única en `sec_8`** — es decir, si el join no es uno-a-muchos exacto —, el estimando sale `NO-ESTIMABLE-LLAVE-NO-UNICA`. **No se deduplica sobre la marcha, no se toma la primera fila, no se promedia.** Esa decisión es de mesa, no del medidor.
- `UPM` y `V_SEL` están en ambos miembros y se usan **sólo** para la guardia de llave declarada (`G-LLAVE-SEC7-DECLARADA-UNICA`), nunca para unir.

---

## 2 · Qué mide, exactamente — **el mismo estimando, otra ola**

### 2.1 · Universo

`U_B`, unidad **EVENTO DE TRÁMITE**: filas de `encig2023_04_sec_7.csv` emparejadas con `encig2023_05_sec_8.csv` por `ID_TRA`, con `P8_4 ∈ {0,1}` **y** `FAC_TRA` finito `> 0`.

- **Rama `SD` (PRIMARIA):** sin deduplicar. Cada fila de `sec_7` es un evento y entra una vez. `NT_TIPO` existe en `sec_7` 2023 (verificado, §1.3) precisamente para distinguir eventos repetidos del mismo tipo; colapsarlos borra lo que el instrumento captó a propósito. **Es la rama que corresponde a `RESULT-ENCIG-MOR-B-P-*-SD` de 2025.**
- **Rama `CD` (SECUNDARIA):** deduplica `sec_7` por `ID_TRA`, conservando la primera fila en orden de archivo. Existe **sólo** para que el par 2023 sea comparable con el par `CD` de 2025; no es la primaria y no se adopta.

**Canales:** `PRE` = `P7_3 = 1`; `DIG` = `P7_3 ∈ {3,4,5}`. El residuo `P7_3 ∈ {2,6,7,8,9,blanco}` se **cuenta y se pesa** (`B-N-RESIDUO-CANAL`, `B-P-RESIDUO-CANAL`) y **no se reasigna**: «presencial vs digital» es una propiedad del **recorte**, no del instrumento, y el `RESULT` `B-VEREDICTO-CANAL` lo dice con dato en vez de con adjetivo.

### 2.2 · Estimando

**DESCRIPTIVO.** `p = Σ(w·d)/Σ(w)` con `w = FAC_TRA` leído de `sec_7`, `d = 1` si `P8_4 = 1` y `0` si `P8_4 = 0`, sumas en **orden fijo de fila**. Los complementos se cuentan **directamente** sobre `d == 0`, nunca como `1 − p`, y `B-SUMA-*` verifica el cierre.

**Ningún `RESULT` de esta spec es causal.** `B-DIFERENCIA-PRE-DIG-SD` y `B-RAZON-PRE-DIG-SD` salen rotuladas **`ASOCIACION`**: quien puede hacer un trámite por internet no es una muestra aleatoria de quien lo hace en ventanilla. La `falsable_si` de `tramite.mordida.con_registro` **no se declara probada** por esta corrida.

**Reserva heredada de la v1.0 y no resuelta aquí:** `P8_4` pregunta *«las anteriores circunstancias»*, que son las del reactivo 8.3 — se pregunta sobre un subconjunto **auto-seleccionado**. Se **cuenta** (`B-COBERTURA`, `B-N-SEC7-SIN-PAREJA`) y se declara; **no se corrige**, porque corregirlo exigiría un universo que el instrumento no da. Si la cobertura es baja, el estimando no es `p(mordida | canal)` sobre el universo de trámites sino `p(este trámite fue el señalado | trámite de alguien que ya declaró en 8.3)`, **y se rotula así, sin adornos**.

### 2.3 · Diseño

Bootstrap de `UPM_DIS` con reemplazo **dentro de** `EST_DIS`, conservando el número de UPM por estrato; 2 000 réplicas, `numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5.

Este método **no lo elige el ejecutor**: lo hereda. `prereg-caja-ENCIG-MORDIDA` **v1.1** (enmienda fechada del 9/sep/2026, que cierra `NC-0112`) elevó el método de §3.7 de la v1.0 a **estándar pre-registrado de la familia** para toda ranura sin método propio. Esta spec es una de esas ranuras y lo toma sin volver a elegirlo. Lo único propio es la **semilla del acto** (`20260915`).

`EST_DIS` y `UPM_DIS` se agrupan como **cadena cruda** (`dtype=str`): nunca a entero, nunca re-rellenadas a un ancho tomado de un descriptor (lección de `ACTO GEN2-LOTE-ENVIPE-1` §3.4 — normalizarlas partiría o fusionaría estratos en silencio). Estrato con UPM única se **re-muestrea a sí mismo**: no se colapsa (decisión de diseño que esta spec no está autorizada a tomar) ni se descarta (sesgaría el punto); si el conteo es `> 0`, `B-METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` y **el IC se lee como límite inferior de la anchura verdadera**, nunca como IC exacto. Filas sin `EST_DIS` o sin `UPM_DIS` se cuentan (`B-N-SIN-DISENO`): afectan al IC, **no** al punto.

`EST_DIS` y `UPM_DIS` están en **ambos** miembros (§1.3). Se toman del lado **`sec_7`** de la tabla unida, por la misma razón que `FAC_TRA`: el diseño que corresponde a la unidad del ponderador.

---

## 3 · Guardias — **paran, no adivinan**

Se corren **antes** de estimar y cada una es un `RESULT`:

| guardia | qué contesta | qué pasa si falla |
|---|---|---|
| `G-1` columnas | ¿están las trece columnas declaradas en los dos miembros? | `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>` |
| `G-1b` miembro | ¿están los dos miembros en el ZIP? | `NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>` |
| `G-2` llave declarada | ¿es `(CVE_ENT,UPM,V_SEL,R_ELE,N_TRA)` única en `sec_7`? | se reporta `UNICA`/`NO-UNICA:<grupos>/<filas>`; **no bloquea** |
| `G-3` `ID_TRA`+`NT_TIPO` | ¿es `(ID_TRA,NT_TIPO)` única en `sec_7`? | se reporta; **no bloquea** |
| `G-4` **`ID_TRA` en `sec_8`** | ¿es única? De ello depende que el join sea uno-a-muchos exacto | **`NO-ESTIMABLE-LLAVE-NO-UNICA`** — las ramas de B no se estiman |
| `G-5` llave de control | ¿`(ID_VIV,ID_PER,ID_TRA,N_TRA)` empareja el mismo conjunto de filas que `ID_TRA`? | `JOIN-NO-EXACTO` → **`NO-ESTIMABLE-LLAVE-NO-UNICA`** |
| `G-6` **ponderador** | ¿`FAC_TRA` se leyó de `sec_7`? ¿existe `FAC_P18` en `sec_8` y quedó sin usar? | el `RESULT` `G-PONDERADOR-POR-ARCHIVO` lo declara; ausencia de `FAC_TRA` → `NO-ESTIMABLE-COLUMNA-AUSENTE:FAC_TRA`, **sin sustituto** |
| `G-7` soporte | ¿`P8_4` tiene soporte fuera de `{0,1,blanco}`? ¿`P7_3` fuera de `{1..9,blanco}`? | `NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:<col>` |
| `G-8` universo | ¿`U_B` o alguno de sus brazos quedó vacío? | `NO-ESTIMABLE-UNIVERSO-VACIO` |
| `G-9` diseño | ¿toda fila carece de `EST_DIS`/`UPM_DIS`? | `B-METODO-IC = NO-ESTIMABLE-DISENO-INCOMPLETO`; IC `null`, **el punto se reporta igual** |

**`CERO NUNCA SUSTITUYE FALTA DE DATO.** Blanco, `9` y no numérico se cuentan aparte y salen del denominador; no se imputan. `NO-APLICA` es un valor y se escribe como tal.

---

## 4 · Hipótesis pre-registrada — **escrita ANTES de abrir el dato**

Se escribe aquí, en el commit que congela, para que no pueda escribirse después de ver la cifra.

**H1 (dirección).** La mordida presencial de 2023 será **mayor** que la digital de 2023: `B-P-PRE-SD > B-P-DIG-SD`. Es la dirección que predice `tramite.mordida.con_registro` (*«el registro rompe la trampa social»*) y la que 2025 exhibió. El `RESULT` `H1-VEREDICTO` sale `H1-SOSTENIDA` / `H1-NO-SOSTENIDA` / `H1-NO-EVALUABLE`. **`H1-NO-SOSTENIDA` no invalida la corrida, no autoriza tocar el medidor y no se ajusta hacia atrás.**

**H2 (nivel, y por qué se declara aunque sea débil).** Se pre-registra la comparación de nivel contra 2025 — `B-DELTA-2023-VS-2025-PRE-SD` = `B-P-PRE-SD(2023) − 0.1410407168724654`, con signo, y su gemela digital contra `0.029867554626649372` — **sin pre-registrar un signo esperado**. Dos olas del mismo instrumento no son una serie, y esta spec **no la construye**: el delta se emite **rotulado `CONTRASTE-DE-OLA-NO-SERIE`**, con los IC de las dos olas escritos al lado, y su lectura correcta es *«cuánto difiere esta ola de aquélla»*, nunca *«cuánto cambió la mordida»*. Ningún `RESULT` de esta spec afirma tendencia.

**H3 (exhaustividad).** El residuo de canal pesará `> 0`, es decir `B-VEREDICTO-CANAL = DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE`. `P7_3` tiene ocho categorías sustantivas y el par `{1}` / `{3,4,5}` usa cuatro. Si el residuo pesa exactamente `0`, la hipótesis cae y se dice.

**Lo que esta spec NO pre-registra, porque no lo sabe:** ningún valor puntual esperado para 2023. **Nada en el árbol lo dice**, y fabricar una expectativa numérica sería contaminar el pre-registro con la ola equivocada.

---

## 5 · Contaminación declarada (`ADR-46`) — esta corrida **NO es ciega**

**Lo que la sesión YA conoce al congelar, dicho sin disfraz:**

1. **Los dos puntos GEN2 de la ola 2025 con toda su precisión:** `RESULT-ENCIG-MOR-B-P-PRE-SD = 0.1410407168724654` y `RESULT-ENCIG-MOR-B-P-DIG-SD = 0.029867554626649372`, con sus `n` (`11167` y `7219` eventos), sus conteos de diseño (`381`/`2996` y `362`/`2518` estratos/UPM) y su lectura (`razón ~4.2x, IC95 sin traslape`).
2. **Las cifras GEN1 selladas** de `milpa/tramite.yaml`, reglas `tramite.mordida.*`: `0.116000`/`0.884000` (presencial, rama `CD`), `0.027358`/`0.972642` (digital, `CD`), `0.141041`/`0.858959` y `0.029868`/`0.970132` (las `_r2`, rama `SD`), `0.085118`/`0.914882` (familia A), y los `ASIGNADO` de `CORR-0001`: `0.62`/`0.38` y `0.88`/`0.12`.
3. **La codificación completa de 2025**: `P8_4 ∈ {0,1}` con el «no» en `0`, `presencial = {1}`, `digital = {3,4,5}`, `FAC_TRA` como ponderador de evento, la distinción `SD`/`CD` y el papel de `NT_TIPO`.
4. Los rótulos `rol_uso: proxy_descriptivo` y `NO-ADOPTAR-NC-0107` que `milpa/` lleva sobre esas celdas.

**Consecuencia deliberada:** la codificación de esta spec **es la misma de 2025 a propósito**, y eso es lo correcto aquí y no lo sería en otro acto. El OBJETO 4 pide *«spec sucesora»* — el mismo estimando sobre otra ola. Elegir una codificación distinta haría incomparables las dos olas y convertiría una sucesora en un estimando nuevo, que es exactamente lo que la firma **no** autoriza. Donde la v1.0 midió su propio juicio (familia A `SOLANY`, familia B `SD` primaria) fue porque estaba abriendo territorio; aquí, replicar el recorte **es** el encargo, y las reservas del recorte se heredan escritas, no se re-litigan.

**Lo genuinamente desconocido al congelar** — y donde está el riesgo real:

- **cuántos estratos y cuántas UPM** hay en `U_B` de 2023, y **cuántos estratos quedan con UPM única** (de eso depende que el IC sea IC o límite inferior);
- **el soporte observado de `P8_4` en 2023**: si el «no» sigue siendo `0` y no `2`, y cuánto pesa el blanco;
- **el soporte observado de `P7_3` en 2023** y el peso del residuo de canal;
- **si `ID_TRA` es única en `sec_8` de 2023**, y si la llave de control empareja el mismo conjunto de filas — es decir, **si el join es siquiera exacto**;
- **la cobertura del join** `sec_7 × sec_8` en esta ola;
- **la anchura del IC** bajo esta semilla, y si los dos brazos se traslapan.

**Ninguno de los seis aparece en fuente alguna leída.** El inventario indexa nombres de columna, no valores; y `data/inventario-reactivos-v1_2.tsv` declara además, en su propia cabecera, que **ENCIG está entre los 102 instrumentos con `texto_reactivo` vacío en el 100% de sus filas** — la verificación de 2023 es por `variable_id`, no por texto, y esta spec no afirma nada sobre el enunciado de los reactivos de 2023 que no herede del descriptor de la v1.0.

---

## 6 · Lo que esta spec **no** hace

- **No abre microdato.** Cero bytes. `data/raw/` no existe en este entorno.
- **No escribe `medidor.py`.** El medidor es del acto de **CAJA** que consuma este contrato. Consecuencia declarada, y correcta: `python3 tools/corrida0.py preflight CALC-ENCIG-2023-0001` reportará **`BLOQUEADO:script_ausente`** hasta que CAJA lo escriba. **Eso no es un defecto de esta spec: es el estado que el encargo ordena** («Spec aquí; corrida en caja»).
- **No adopta.** No escribe cita `corrida0_resultado_id` ni `corrida0_generacion` en `milpa/` bajo **ninguna** rama, no crea conducta nueva, no cambia ninguna cifra vigente y no toca ningún `tier`. Los `RESULT` salen `LISTADO-PARA-MESA-*` y ahí se detienen.
- **No mide las familias A, C ni X.** Los reactivos existen en este payload (`P8_3_1/2/3` con `FAC_P18` en `encig2023_01_sec1_A_3_4_5_8_9_10.csv`; `N_TRA` y `P7_3` en `sec_7`; `P8_6` en `sec_8` — todos verificados en el inventario). **Quedan fuera por perímetro, no por imposibilidad**, y se dice así para que nadie lo lea como un negativo: el OBJETO 4 firma *una* sucesora del estimando de canal, y tres familias más serían tres estimandos que la firma no menciona.
- **No reescribe ningún sello.** Ni la v1.0, ni la v1.1, ni `CALC-ENCIG-0001`.
- **No construye serie.** Dos olas no son una tendencia (§4, H2).
- **No toca `CORR-0002`, `CORR-0004/0005/0006/0019`** (que son del OBJETO 3) **ni `CORR-0018`** (OBJETO 5).

### 6.1 · Qué demanda toca, y con qué honestidad

`CORR-0001` (`ENCIG2023`, 4 `RESULT`: `RES-0001`, `RES-0002`, `RES-0007`, `RES-0008`) es la fila que esta spec **habilita**, y la relación **no es uno a uno**:

- `RES-0007` / `RES-0008` consumen `tramite.mordida.con_registro:tramite_normal` / `:paga_mordida` (`0.88` / `0.12`, clase `ASIGNADO`) — **sin partir por canal**. Lo que esta spec produce **sí** está partido por canal. Un `ASIGNADO` sin canal no se releva con un medido por canal sin una decisión de mesa sobre cuál brazo (o qué agregación) lo sustituye, y **esta spec no toma esa decisión**.
- `RES-0001` / `RES-0002` consumen `tramite.mordida.discrecional` — **familia A**, que esta spec no mide (§6).

Por lo tanto: `demanda_que_releva` se declara como **candidatura para mesa**, no como relevo consumado. **Decirlo es el entregable; darlo por concedido sería el error.**

---

## 7 · Congelamiento

Esta spec, `data/corrida0/CALC-ENCIG-2023-0001/spec.yaml` y `data/corrida0/CALC-ENCIG-2023-0001/spec.md` se congelan en el **COMMIT-1** de `ACTO GEN2-FIRMAS-MESA-1`, **en NUBE y antes de abrir un solo byte de microdato**. `medidor.py` **no existe** y lo escribe el acto de CAJA a partir de este contrato, sin editar el COMMIT-1.

**El primer resultado que produzca este procedimiento es el que se reporta.**
