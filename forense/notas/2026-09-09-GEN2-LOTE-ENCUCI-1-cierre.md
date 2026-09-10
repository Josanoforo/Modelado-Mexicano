# `ACTO GEN2-LOTE-ENCUCI-1` — cierre. La mordida de 2020 resulta no medir lo que su rótulo dice, y la protesta reproduce al dígito

**Fecha:** 9/sep/2026 · **Entorno:** CAJA (Ubuntu/WSL2), corpus montado · **Base:** `origin/main = d20039a3` (`PR #669`)
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENCUCI-1.md` (A.3, verbatim)
**Spec sellada:** `forense/prereg-caja/ENCUCI-MORDIDA-PROTESTA-spec-v1_0.md` (`prereg-caja-ENCUCI-MORDIDA-PROTESTA`, `sha 33add378…`)
**Corrida:** `data/corrida0/CALC-ENCUCI-0001/` — `spec-check 30 OK · 0 FAIL` → `PRE-FLIGHT VERDE` → `run exit=0` → `verify: REPRODUCE` (119/119, `CONTEXTO=IDENTICO`)

---

## 0 · El titular, antes de nada

**El control positivo sale 2 de 4, y la mitad que falla es la interesante.** Las
dos celdas de **protesta** reproducen el valor sellado **al grano de seis
decimales** y quedan adoptadas con cita `corrida0_resultado_id` +
`corrida0_generacion: GEN2`. Las dos de **mordida** no reproducen — y al montar
la cadena aparece por qué, y algo más grande:

> **La celda `paga_mordida_encuci2020` no mide «pagar una mordida», y tampoco
> mide lo que la anotación vigente del motor dice que mide.** ENCUCI 2020
> pregunta **dos** cosas distintas —si le **pidieron** (`AP5_17`) y si **tuvo
> que dar** (`AP5_18`)— y la celda sellada es la **unión** de ambas. Medido:
> solicitud **0.106319**, entrega **0.073640**, unión **0.126006**. El valor que
> el motor consume está **71% por encima** de la tasa de pago efectivo.

Contadores del programa, salida cruda: `adoptados_activos` **10 → 12**,
`dependencias_legacy` **195 → 193**. Sonda de consumo contra `milpa.src.emisor`:
**4/4**.

Y de paso, tres cosas que ninguna de las cuatro cifras GEN1 dice: **`FP-201` es
falso también para ENCUCI 2020** (§5), **la guardia `NC-0094` destapó un defecto
heredado en `main`** (§7), y **`tests/check.py` escribe en el árbol de trabajo**
(§9-bis).

---

## 1 · Compuerta, premisas y `P0`, re-derivados antes de editar

| lo que el encargo declaró | lo real, verificado |
|---|---|
| `COMPUERTA: GATED a PR del ACTO GEN2-F5-RECAPTURA-L fusionado` | **CUMPLIDA, por producto.** `PR #669` `MERGED 2026-09-10T01:01:11Z`, merge commit `d20039a3` = `HEAD` de `origin/main`; `git cat-file -e origin/main:forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md` → existe. |
| base `cc1cfe2c` | base real **`d20039a3`**. Re-derivado todo lo que depende del perímetro. |
| «**4** RESULT … incluye las conductas `paga_mordida_encuci2020`» | **CIERTO, y el «incluye» era la mitad del encargo.** Los cuatro son de **dos constructos**: `RES-0005`/`RES-0006` mordida y `RES-0061`/`RES-0062` **protesta** (`civico.protesta.agravio_urbano_encuci2020`). Enumerados desde la demanda vigente en §1.4 de la sellada. |
| `P1` · «**el** reactivo de pago informal» (singular) | La plaza exige **cuatro** reactivos: `AP5_17`, `AP5_18`, `AP7_3_5` y `AP4_3_2`. La spec cubre los cuatro. |
| «(a) el inventario es ciego a DBF (`NC-0123`)» | **Cierto en la conclusión, falso en la causa** — §6. |
| «(b) `FP-201` mintió tres veces» | **Cuatro** — §5. |
| «(c) ENCUCI es UNA ola (2020, contexto COVID)» | Cierto, y estampado en cada `RESULT`. Nada se puentea a ENCIG 2025. |

### 1.1 · `P0` · `NC-0114` — el día no la dejó (cero espera, cero bloqueo)

- Último disparo de producción: **2026-09-09 07:30:07**, ya atribuido y sellado
  por `ACTO GEN2-ADQ-VERIFICACION-CAJA` (`PR #666`).
- Retiro del crontab legado: `PR #668`, fusionado **2026-09-09 15:16 local**.
- `forense/adq-log/2026-09-09.log` termina a las **07:34**; no hay log
  posterior. `Get-ScheduledTaskInfo \ModeladoMexicano\AdquiereCron` →
  `LastRunTime = 09/09/2026 07:30:00` · `LastTaskResult = 0` ·
  **`NextRunTime = 09/10/2026 07:30:00`** · `NumberOfMissedRuns = 0`.

**«Sin corrida posterior aún».** La única corrida existente es **anterior** al
retiro, así que no puede probar que el disparador quedó único. **`NC-0114` sigue
`ABIERTA`, sin cambio.**

`NC-0120` tampoco avanza: `(Get-WinEvent -ListLog
'Microsoft-Windows-TaskScheduler/Operational').IsEnabled` → **`False`**. Se
anota, no se cierra.

*(Nota de entorno, declarada: el sandbox de Bash de esta sesión **no lee
`/mnt/c` en absoluto** — `powershell.exe` sale `No such file or directory`. Las
dos lecturas de arriba se hicieron con el sandbox desactivado, y son consultas
de **sólo lectura**: no se instaló, reinstaló ni modificó ninguna tarea.)*

---

## 2 · La medición

Payload `encuci2020_bd_dbf`, `sha256 0414fd59…f283` **verificado byte a byte en
la caja**, idéntico al manifiesto y al `sha256_payload` de las dos entradas de
`milpa/tramite.yaml`.

**Universo estampado en cada `RESULT`:** ENCUCI 2020, población mexicana de **15
años y más**, dominios **nacional urbano / nacional rural / seis regiones** — a
diferencia de ENCIG 2025, **estos estimadores sí son nacionales**. Ventana de
los reactivos de 12 meses: «de **agosto de 2019** a la fecha». `AP7_3_5` es
**«alguna vez en su vida»**.

### 2.1 · Familia A · mordida (`tramite.mordida.discrecional`)

| celda | qué mide | `p` | IC95 | n |
|---|---|---|---|---|
| `A-P-SOLICITUD` **(primaria)** | `AP5_17`: **le pidieron** | **0.106319** | [0.098075, 0.115041] | 13 411 |
| `A-P-ENTREGA` **(primaria)** | `AP5_18`: **tuvo que dar** | **0.073640** | [0.066144, 0.081044] | 13 411 |
| `A-P-CUALQUIERA` *(celda GEN1, adoptable)* | unión `AP5_17`∨`AP5_18` | **0.126006** | [0.116666, 0.135942] | 13 411 |
| `A-P-AMBAS` | le pidieron **y** dio | 0.053954 | — | 13 411 |
| `A-P-SOLICITUD-SIN-ENTREGA` | le pidieron y **no** dio | 0.052366 | — | 13 411 |
| `A-P-COMPLEMENTO-CUALQUIERA` | `AP5_17=2` **y** `AP5_18=2` | 0.873994 | — | 13 411 |
| `A-P-CUALQUIERA-POBLACION` | la misma unión sobre **toda** la población 15+ | **0.079958** | — | 21 495 |

`A-SUMA-CUALQUIERA = 1.0` exacto · `A-METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA`
(1 estrato de 281 con una sola UPM: **el IC es límite inferior de la anchura
verdadera**) · `A-VEREDICTO-EXHAUSTIVIDAD = EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U-A`.

**Control positivo: `NO-REPRODUCE`.** `A-DELTA-VS-GEN1 = +1.836e-04`
(`0.126006` contra `0.125822`) y el complemento su espejo exacto
(`−1.836e-04`). **Nada se ajustó hacia atrás.**

### 2.2 · Familia B · protesta (`civico.protesta.agravio_urbano_encuci2020`)

Eje **entorno × agravio**, unidad persona 15+, `FAC_SEL`, `n = 20 184`,
281 estratos, 3 095 UPM, **cero estratos de UPM única** → `METODO-IC =
IC-BOOTSTRAP-UPM-EN-ESTRATO` (IC limpio).

| celda | `p` | IC95 | n |
|---|---|---|---|
| `B-P-URB-AGR` **(`RES-0061`)** | **0.11219151** | [0.101188, 0.123397] | 8 322 |
| `B-P-RUR-AGR` **(`RES-0062`)** | **0.09191244** | [0.074306, 0.109818] | 2 050 |
| `B-P-URB-SIN` | 0.074959 | [0.064839, 0.085566] | 6 356 |
| `B-P-RUR-SIN` | 0.066996 | [0.057307, 0.077275] | 3 456 |
| `B-P-U` (sin partir el eje) | 0.093532 | — | 20 184 |

**Control positivo: `REPRODUCE` las dos.** `B-DELTA-URB-VS-GEN1 = −4.869e-07`
· `B-DELTA-RUR-VS-GEN1 = +4.441e-07`; al grano de seis decimales, **delta
exactamente `0.0`** en ambas → `ADOPTABLE-POR-REPLICA`.

**Y reproduce los dos veredictos de contraste, no sólo los puntos** (los dos
rotulados **`ASOCIACION-NO-CAUSAL`**):

| contraste | `p` | IC95 | GEN1 decía | aquí |
|---|---|---|---|---|
| `C1` entorno, dado agravio (URB−RUR) | +0.020279 | **[−0.001154, +0.041644]** | `NO-DISCRIMINA` (+2.0279 pp, IC contiene 0) | **contiene 0 → NO-DISCRIMINA** |
| `C2` agravio, dentro de urbano (AGR−SIN) | +0.037233 | **[+0.022822, +0.052217]** | `CORROBORADA` (+3.7233 pp, IC excluye 0) | **excluye 0 → CORROBORADA** |

Los dos puntos coinciden con los `brecha_pp` sellados **a cuatro decimales**, y
los IC —calculados con un método que nadie había pre-registrado— caen casi
encima de los de GEN1. Eso es corroboración que no se buscó.

---

## 3 · Hallazgo 1 — el rótulo `paga_mordida` describe una **unión**, y la anotación vigente del motor tampoco la describe

`A-VEREDICTO-SEMANTICA = LA-UNION-EXCEDE-A-CADA-PARTE`.

`milpa/tramite.yaml:76` anota hoy `paga_mordida_encuci2020` como
*«SEMANTICA (D4, `NC-0113`): mide **solicitud** de pago informal, **no pago
consumado**»*. Esa lectura es **correcta para ENCIG 2025**, cuyo reactivo 8.3
sólo pregunta si le solicitaron. **No describe la celda de ENCUCI**, y ahora
está medido por qué:

- ENCUCI **sí tiene** el reactivo de pago consumado: `AP5_18`, *«¿hubo alguna
  ocasión en la que **tuvo que darle** … una dádiva, un favor o dinero extra
  (que no sea la tarifa oficial)?»*.
- La celda sellada es la **unión** `AP5_17|AP5_18` (verbatim del bloque
  `enmienda_encuci2020`), y por tanto **excede a cada parte**: `0.126006` contra
  `0.106319` (solicitud) y `0.073640` (entrega).
- **El `0.1258` que el motor consume está 71% por encima de la tasa de pago
  efectivo** y 18% por encima de la de solicitud. No es «solicitud», no es
  «pago»: es «le pidieron **o** dio».

Y dentro del par aparece el dato que separa los dos constructos, que **nadie
había medido en esta fuente**:

- **`A-P-SOLICITUD-SIN-ENTREGA = 0.052366`** — el **49.3%** de las solicitudes
  **no** termina en entrega. Casi una de cada dos.
- `A-P-ENTREGA − A-P-AMBAS = 0.019686` — hay quien **dio sin declarar que le
  pidieran**: casi 2 puntos de la población con contacto.

Esta spec **no edita** la anotación `NC-0113` (fuera de perímetro): la mide y la
deja asentada como fila `NC` con sucesor.

## 4 · Hallazgo 2 — por qué la familia A no reproduce, y qué dice el 0.1258 sobre su denominador

**(a) El universo GEN1 se reproduce a la unidad… en el paso anterior al que la
spec usa.** `A-N-CONTACTO = **13 435**` — **exactamente** la `n: 13435` que
declara `enmienda_encuci2020`. `A-N-U = **13 411**`, es decir **−24**: las filas
que declaran contacto pero traen `9` (No sabe/no responde) en `AP5_17` o
`AP5_18` (17 y 17, con solapamiento).

De esos dos conteos —los dos pre-declarados, ninguno buscado— se sigue que el
universo GEN1 **incluyó** esas 24 filas, y por tanto contó su `9` como `0`. Esta
spec no lo hace: **cero nunca sustituye falta de dato**. Es la explicación
aritmética que encaja con `A-DELTA-VS-GEN1 = +1.836e-04` (un denominador mayor
con el mismo numerador da un `p` menor).

**No se ha medido**, y deliberadamente: recodificar el `9` a `0` **después** de
ver que el punto no reproduce sería elegir la codificación por su resultado, que
es exactamente lo que el congelamiento existe para impedir. Queda como fila `NC`
con sucesor y su propio pre-registro.

**(b) El `0.1258` es, en buena parte, propiedad del recorte.** `8 084` de las
`21 519` personas seleccionadas (**37.6%**) **no declaran ningún contacto** con
ninguno de los diez tipos de servidor público. Sobre la población de 15+
completa, la misma unión da **`A-P-CUALQUIERA-POBLACION = 0.079958`** en vez de
`0.126006`: **el 36.5% de la cifra sellada desaparece al cambiar de
denominador**. La regla `tramite.mordida.discrecional` la consume como tasa base
de conducta; qué denominador quiere es una decisión de mesa, no de esta spec.
`A-P-RESIDUO-POBLACION = 0.001037` — lo que sale por falta de dato pesa una
milésima, no explica nada por sí solo.

## 5 · Hallazgo 3 — la trampa de tipo, medida en vez de supuesta; y `FP-201` cae por cuarta vez

**`G-VEREDICTO-TIPO-AP5-16 = SOLO-NUMERO-ACIERTA`.** Los dos conteos
pre-declarados: `G-N-AP5-16-1-CADENA-UNO = **0**` ·
`G-N-AP5-16-1-NUMERICO-UNO = **4 087**`.

El descriptor declara `AP5_16_x` como «Numérico(1)»; **el DBF lo declara `N`
19 con 15 decimales**, y el texto crudo llega `1.000000000000000`. Un filtro de
contacto escrito como `== "1"` habría dado **0 de 21 519** y el universo A
habría salido vacío — sin excepción, sin error, con la corrida «terminando
bien». La guardia estaba escrita en el `COMMIT-1` y la corrida la contesta con
dato.

De las **once** variables declaradas, **cuatro** discrepan del descriptor en
tipo o en ancho (`AP5_17`/`AP5_18` son `C 6` y no numéricos; `FAC_SEL` es
`N 19,10` y no un entero de 6; `EST_DIS` mide 7 en el DBF y 3 en el papel).
**Manda el header.**

**`FP-201` es falso también para ENCUCI 2020.** `G-VEREDICTO-DISENO =
DISENO-IDENTIFICABLE`: `FAC_SEL`, `DOMINIO`, `ESTRATO`, `UPM_DIS` y `EST_DIS`
están en las **cinco** tablas; **281 estratos, 3 096 UPM, 0 filas sin diseño, 0
ponderadores inválidos**. Es la **cuarta** fuente en que ese `FP` resulta falso
(tras ENVIPE, ENIF y las tres olas de `GEN2-R-SERIE-CSV`). El diseño **se usó**:
no se renunció al IC correcto.

**Las llaves opacas, perfiladas antes de agrupar:** `G-PERFIL-EST-DIS =
len3=21519;con_espacio_en_bordes=0` · `G-PERFIL-UPM-DIS =
len7=21519;con_espacio_en_bordes=0`. Aquí el descriptor **no** miente sobre el
contenido (3 y 7 caracteres, dentro de los rangos declarados) — miente el ancho
del campo del DBF. Se agruparon como cadena cruda de todos modos.

**Estructura:** `G-VEREDICTO-ESTRUCTURA = LLAVE-DECLARADA-Y-ID-PER-COINCIDEN`.
`ID_PER` **y** la terna declarada `UPM+VIV_SEL+R_SEL` son **ambas** únicas en
las dos tablas, y `B-COBERTURA-JOIN = 1.0` (21 519 de 21 519). Ninguna llave se
adoptó por autoridad: se midieron las dos, con la rama
`NO-ESTIMABLE-LLAVE-NO-UNICA` pre-escrita por si acaso.

## 6 · Hallazgo 4 — el eje de la familia B depende de una decisión que la cita GEN1 no explicitaba

`DOMINIO` tiene **tres** valores, no dos: `U` Urbano (**10 308**), `C`
**Complemento urbano** (**5 295**), `R` Rural (**5 916**). La regla sellada dice
sólo *«`DOMINIO` agrupado (urbano/rural)»* — y **no dice dónde va `C`**.

Esta spec lo congeló en el `COMMIT-1` por el descriptor (`C` se **llama**
«Complemento **urbano**», y los dominios declarados del instrumento son urbano y
rural): `urbano = {U, C}`, `rural = {R}`. Que era la de GEN1 se **supo después**,
porque el punto reprodujo.

**Lo que vale esa decisión, medido:** `B-DELTA-AGRUPACION = **−0.012124**`. Bajo
la agrupación alternativa (`urbano = {U}`, `rural = {R, C}`) la misma celda da
`0.124316` en vez de `0.112192`, y la rural `0.081633` en vez de `0.091912`.
**1.21 pp de movimiento por una decisión de codificación — el 60% del tamaño del
contraste `C1` que el eje existe para medir (2.03 pp).** Las cuatro celdas
alternativas se emiten (`B-ALT-P-*`) y **no** son adoptables.

**Aviso para quien lea la regla después:** «urbano» aquí incluye el complemento
urbano; «agravio» es, literalmente, **problema declarado de pandillerismo, robos
o delincuencia en la colonia o localidad** (`AP4_3_2`) — percepción de entorno,
**no victimización propia**.

Y el `b` del descriptor era real: **1 198 filas (5.6%)** traen `AP7_3_5` en
blanco, más 67 en `9` y 70 con `AP4_3_2` fuera de `{1,2}`. `B-N-U = 20 184`
contra las `20 187` que declara la regla (**−3**); el punto reproduce igual.

## 7 · Hallazgo 5 — la guardia `NC-0094` destapó un defecto heredado en `main`

Al re-derivar las vistas, `registro --escribe` **paró**:

```
PARO · REPLAY-PISADO (NC-0094): escribir borraria o cambiaria evidencia de
replay de 1 corrida(s) AJENA(s) al lote autorizado (2 campo(s)).
    CALC-ENCIG-0001--c3ae00e62e59 · contexto_replay: IDENTICO -> DISTINTO
    CALC-ENCIG-0001--c3ae00e62e59 · resultado_replay: REPRODUCE -> REPLICA-RESULTADO · CONTEXTO-DISTINTO
```

**Causa, verificada contra `origin/main`, no supuesta:**

| commit | qué hizo | `sha256` de `forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md` |
|---|---|---|
| `c3ae00e` (9/sep 11:50, `COMMIT-1` de `GEN2-LOTE-ENCIG-1`) | crea la spec sellada; `CALC-ENCIG-0001` la declara **input** con su `sha256` | `00c7c4a6…` |
| `be9b0c0` (9/sep 15:37, `ACTO GEN2-MOTOR-SEMANTICA`, `PR #670`) | **le añade el §8 «Enmienda fechada»** | `e62b523e…` |

`git log … -- <ese archivo>` sobre mi rama contra `origin/main` sale **vacío**:
este acto **no lo tocó**.

**Consecuencia:** un acto fusionado editó un artefacto que otro `CALC` ya
sellado declara como input con su hash, y con eso invalidó en silencio el
contexto de replay de esa corrida. `verify CALC-ENCIG-0001` hoy dice
`CONTEXTO: DISTINTO · razon: input_cambiado=IN-ENCIG-SPEC-SELLADA` — **el
resultado sigue reproduciendo**; lo que cambió es el contexto. La vista decía
`IDENTICO` porque nadie la re-derivó tras `PR #670`.

**Qué se hizo aquí, y por qué:** se nombró
`CALC-ENCIG-0001--c3ae00e62e59` en `--lote` —el camino que la propia herramienta
prescribe— porque la vista derivada estaba **desfasada del árbol** y escribir el
valor verdadero es refrescarla, no borrar evidencia: los artefactos sellados de
ENCIG (`ejecucion.json`, `sello.json`) conservan intacto lo que era cierto al
sellar. **Auditoría del resto, exigida por `NC-0094`:** de las **28** celdas con
veredicto de replay escrito antes de la escritura, **27 sobreviven byte a byte**;
la única que cambia es la de ENCIG, documentada arriba; y entra **1** nueva, la
de este acto. **Cero filas ajenas alteradas.**

La decisión de fondo —si `CALC-ENCIG-0001` se re-sella o si la enmienda del §8
debía haber sido una `v1.1` con su propio archivo— **no es de este acto**: sube
como fila `NC` con sucesor a mesa.

## 8 · `P3` · Adopción y consumo — **dos citas, no cuatro**

| `RES` | consumidor | rama pre-declarada | cita |
|---|---|---|---|
| `RES-0061` | `protesta_alguna_vez_urbano_con_agravio_encuci2020` | `ADOPTABLE-POR-REPLICA` (delta al grano `0.0`) | **`RESULT-ENCUCI-B-P-URB-AGR`** |
| `RES-0062` | `protesta_alguna_vez_rural_con_agravio_encuci2020` | `ADOPTABLE-POR-REPLICA` (delta al grano `0.0`) | **`RESULT-ENCUCI-B-P-RUR-AGR`** |
| `RES-0005` | `paga_mordida_encuci2020` | **`NO-ADOPTABLE-POR-DISCREPANCIA`** (`+1.836e-04` > `1e-6`) | **sin cita** |
| `RES-0006` | `tramite_normal_encuci2020` | **`COMPLEMENTO-CON-DENOMINADOR-RECORTADO`**, por construcción | **sin cita** |

El `p` **no se movió** en ninguna de las cuatro: la adopción es **cita**, no
cambio de cifra. `git diff --numstat milpa/tramite.yaml` → **`2 2`**: dos líneas
tocadas, dos escritas, ninguna fila ajena.

`RES-0005` no recibe cita porque **no reproduce**: escribírsela lo presentaría
como replicado cuando no lo está. `RES-0006` no la recibe porque falla la
condición (1) del criterio —no es una categoría contada directamente que releve
un primario independiente—, y eso estaba **escrito en la spec antes de medir**
(`D1`/`NC-0108`), no elegido a posteriori.

**Sonda de consumo (solo lectura): PASA 4/4.** `cargar_reglas() -> 21 reglas`;
para las dos adoptadas, `emitir_binaria()` devuelve `valor_punto` **igual** a
`round(RESULT, 6)`; para las dos no adoptadas, el emisor sigue emitiendo
exactamente lo que emitía antes del acto. El árbol quedó intacto tras la sonda
(`git status --porcelain` sin cambios nuevos). **La compatibilidad queda
demostrada, no supuesta.**

**Contadores, salida cruda, sin cifra esperada (E.4)** — `corrida0 status`
deriva del árbol vivo, así que el «antes» se tomó con el `CALC` ya sellado y las
citas aún sin escribir; el delta es el de la adopción:

```
ANTES     N_resultados_gen2_adoptados_activos=10    dependencias_numericas_legacy_activas=195
DESPUES   N_resultados_gen2_adoptados_activos=12    dependencias_numericas_legacy_activas=193
```

## 9 · Hallazgo 6 — el texto de los reactivos de ENCUCI no está en ningún inventario de la casa

El encargo lo anticipaba como «el inventario es ciego a DBF (`NC-0123`)». **La
conclusión operativa es la misma; la causa no.** Cuatro inventarios examinados,
con universo declarado:

| inventario | filas | filas ENCUCI | con `texto_reactivo` | de mis 9 variables |
|---|---|---|---|---|
| `data/inventario-reactivos-v1_2.tsv` (el vigente) | 178 246 | **458** | **0** | 0 |
| `data/inventario-reactivos-ext-v1_0.tsv` | 63 345 (**24 138** con texto) | **0** | 0 | 0 |
| `data/inventario-fd-ext-v1_0.tsv` | — | **62** (todas con texto) | 62 | **0** — son descripciones de **tabla** |
| `data/inventario-fd-v1_1.tsv` | — | **0** | 0 | 0 |

**No es ceguera al DBF:** `inventario-reactivos-v1_2.tsv` no trae
`texto_reactivo` en **ninguna** de sus 178 246 filas — control positivo `encig`,
10 465 filas, **0** con texto. Y el único inventario que sí lo trae no tiene
**ninguna** fila de ENCUCI. Todo el texto y todos los códigos de esta spec
salen del `FD_ENCUCI2020.pdf`, y **ningún negativo de este acto se apoya en el
inventario**.

*(`spec-check` sí encuentra las 30 variables: **30 OK · 0 FAIL**, 317 718 filas
examinadas. El inventario indexa **nombres**; lo que no trae es el **texto**.)*

## 9-bis · Hallazgo 7 — **la suite escribe en el árbol**, y por eso se vio que la demanda estaba desfasada

Al montar el cierre apareció `data/corrida0/demanda-resultados.tsv` modificado
sin que ningún paso de este acto lo hubiera editado. Aislado con un experimento
de tres pasos, no supuesto:

```
git checkout HEAD -- data/corrida0/demanda-resultados.tsv   -> sin cambios
python3 tools/corrida0.py status                            -> sin cambios
python3 tests/check.py --baseline                           -> 28  28  data/corrida0/demanda-resultados.tsv
```

**Es `tests/check.py`.** La cadena: `check.py::t32_corrida0` corre
`tests/test_corrida0.py`, y ahí `t_cmd_demanda_aplica_fp339` llama
`C.cmd_demanda(None)` **sobre el árbol de trabajo real** —su propio docstring lo
dice: *«`cmd_demanda` real (árbol de trabajo, no fixture)»*—, y `cmd_demanda`
**escribe** `demanda-resultados.tsv` y `demanda-corridas.tsv`. Un verificador que
escribe.

Normalmente es invisible porque la demanda ya está al día. Aquí se vio porque
**no lo estaba**: las 28 filas que cambian son las celdas `L` del duelo, cuyo
`escala_legacy` pasa de `CAPTURA-CORREDOR (8 replicas)` a `(16 replicas)`. El
árbol tiene, contado, **16** capturas por celda (`ls
forense/prereg-duelo-v2/corridas-L/ | grep "L-CIV-M-01-M__L-solo" | wc -l` →
`16`): las dejó `ACTO GEN2-F5-RECAPTURA-L` (`PR #669`), que **no re-derivó la
demanda al cerrar**. La re-derivación de este acto la pone al día; ninguna cifra
de este lote depende de esas 28 filas.

**Por qué importa más allá de aquí:** cualquier acto que corra la suite y cierre
con `git add -A` se lleva esa re-derivación ajena dentro de su PR sin saberlo, y
en sentido contrario un `git status` sucio después de correr la suite parece
trabajo propio sin serlo. Va como fila `NC` con sucesor; **este acto no toca
`tests/`** (fuera de perímetro).

## 10 · El guardián que no habría guardado — `ya_medido.py`, tercera confirmación

`tools/ya_medido.py tramite.mordida.discrecional` → **`NUNCA-MEDIDA`**, para una
regla que `milpa/tramite.yaml:76` trae medida y sellada con
`clase: "MEDIDO·p(tasa base ponderada)"` y `p: 0.125822`. Es el mismo falso
negativo que `NC-0109` (lote ENCIG) y `NC-0129` (lote ENIF) ya asentaron:
`_tiene_veredicto_real()` no reconoce `MEDIDO`. **Tercera confirmación en tres
lotes consecutivos**; no se abre fila nueva, se apunta a las dos abiertas.
`civico.protesta.agravio_urbano_encuci2020` y `R7.4` sí salen `MEDIDA-EN:`.

## 11 · Límites declarados

- **Geográfico y poblacional.** Nacional, 15 años y más. **Sí** son estimadores
  nacionales (a diferencia de ENCIG 2025, urbano 100k+ y 18+).
- **Temporal y de contexto.** Una sola ola, 2020. La ventana de la familia A
  empieza en **agosto de 2019** y por tanto **precede al confinamiento**,
  mientras que la entrevista ocurre dentro de él. La familia B es «alguna vez en
  su vida». Ni el contexto COVID ni su efecto se modelan: **se declaran**.
- **Comparabilidad con ENCIG 2025: PREGUNTA ABIERTA, no supuesto.** Mismo
  constructo ≠ mismo instrumento. Difieren el universo (nacional 15+ vs. urbano
  100k+ 18+), la ventana (12 meses desde agosto 2019 vs. «durante 2025»), el
  filtro de entrada (contacto con 10 tipos de funcionario vs. realización de
  trámites) y el reactivo (dos preguntas, solicitud **y** entrega, vs. tres
  incisos de solicitud). **Ninguna salida de este acto las pone lado a lado**, y
  el cruce exige su propio pre-registro.
- **Causalidad: ninguna.** `B-DIF-C1` y `B-DIF-C2` van rotuladas
  **`ASOCIACION-NO-CAUSAL`**: entorno y agravio no se asignan al azar.
- **IC como límite inferior** en la familia A (1 estrato de 281 con una sola
  UPM). La familia B no tiene ninguno: su IC es limpio.
- **Ranura de IC no pre-registrada.** Nadie había pre-registrado un método de IC
  para ENCUCI. Lo eligió el ejecutor sobre ranura vacía, declarado en §3.7 de la
  sellada, y **se eleva a mesa**. Los `ic95 [0.116323, 0.135544]` de
  `enmienda_encuci2020` **no se ponen lado a lado** con los de aquí (A-bis.3).
- **Contaminación (ADR-46).** La corrida **no fue ciega**: al congelar, la
  sesión ya había leído los cuatro valores GEN1 y **la codificación GEN1
  completa** de las dos familias. Está declarado en §0.3 de la sellada, y es la
  razón de que las primarias sean `A-P-ENTREGA` y las cuatro celdas del eje. Lo
  genuinamente desconocido al congelar —la separación solicitud/entrega, el peso
  del recorte de contacto, el reparto de `DOMINIO`, el perfil de las llaves y
  los tipos del header— es exactamente lo que resultó ser el hallazgo.

## 12 · Contador

`cuenta_gen2` de `CALC-ENCUCI-0001` queda en **`SI`**, asentado en
`data/corrida0/decisiones.tsv` (`motivo_cuenta_gen2` pasa de «etiqueta de la
spec» a «decisión de mesa (`decisiones.tsv`)», y las vistas se re-derivaron
**después** de escribir esa fila). La firma que ordena el lote **sí tiene como
objeto el contador**: el encargo trae, verbatim, *«cuenta_gen2 = SI para el CALC
que este acto selle»*. Estándar `FP-367/368` satisfecho (autoridad + fecha +
**OBJETO**). **El merge de mesa la perfecciona.**

## 13 · A.13 — qué se examinó

**Microdato: 2 archivos**, abiertos por primera vez en el `COMMIT-2`, nunca
antes de congelar — `ENCUCI_2020_SEC_4_5.dbf` (**21 519** registros, 164 campos)
y `ENCUCI_2020_SEC_6_7_8.dbf` (**21 519**, 156 campos).
**Metadato y codebook (`COMMIT-1`):** el manifiesto (2 entradas ENCUCI,
`sha256` del payload verificado en la caja); el descriptor `FD_ENCUCI2020.pdf`
(**4 005** líneas extraídas con `pdftotext -layout`); la **lista de 5 miembros**
del ZIP y la **cabecera** de los cinco `.dbf` (encabezado de 32 bytes +
descriptores de campo de 32 bytes: nombre, tipo, ancho, decimales); los
**cuatro** inventarios de reactivos (§9); `milpa/tramite.yaml`;
`data/corrida0/demanda-*.tsv`; y las notas de identidad y migración de `PR #662`.
**`forense/prereg-caja/`:** directorio completo, **0** aciertos de `encuci`
(control positivo `encig` → 1, `exit 0`).
**Contrato del medidor:** verificado contra **fixture sintética** antes de tocar
el payload — **119 declarados = 119 emitidos**, 0 problemas de tipo.
**Suite:** `python3 tests/check.py --baseline` → **VERDE**, 3 `FAIL` de línea
base, ninguno nuevo.
