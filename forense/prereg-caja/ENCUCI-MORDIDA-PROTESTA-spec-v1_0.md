# ENCUCI-MORDIDA-PROTESTA · Pre-registro de la mordida (solicitud y entrega) y de la protesta por entorno × agravio, ENCUCI 2020

### `prereg-caja-ENCUCI-MORDIDA-PROTESTA` · **v1.0** · 9 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-ENCUCI-1` · CAJA (Ubuntu/WSL2) · base `origin/main = d20039a3`
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENCUCI-1.md` (A.3, verbatim)
**Releva:** `CORR-0003` (ENCUCI2020) → **4** `RESULT`: `RES-0005`, `RES-0006`, `RES-0061`, `RES-0062`
**Corrida:** `data/corrida0/CALC-ENCUCI-0001/`

> **CONGELADA EN EL COMMIT-1, ANTES DE LEER UN SOLO REGISTRO DE UN `.dbf`.**
> Lo único abierto al escribirla: `data/manifiesto.yaml`; el descriptor
> `FD_ENCUCI2020.pdf` (4 005 líneas extraídas con `pdftotext -layout`); la
> **lista de miembros** del ZIP y la **cabecera** de cada `.dbf` (los 32 bytes
> del encabezado y los descriptores de campo de 32 bytes — nombre, tipo,
> ancho, decimales: metadato del archivo, no registros); los cuatro
> inventarios de reactivos de la casa; `milpa/tramite.yaml`;
> `data/corrida0/demanda-*.tsv`; y las notas de identidad y migración de
> `PR #662`. **Ningún registro de microdato.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Las premisas del encargo, contrastadas (ninguna bloquea)

| lo que el encargo declaró | lo real, verificado |
|---|---|
| «redactado contra `origin/main = cc1cfe2c`» | base real al abrir: **`d20039a3`** (merge de `PR #669`). Re-derivado todo lo que depende del perímetro. |
| «**4** RESULT tras la migración … incluye las conductas `paga_mordida_encuci2020` de `tramite.mordida.discrecional`» | **CIERTO, y el «incluye» importa**: los cuatro son de **dos constructos distintos**, no de uno. `RES-0005`/`RES-0006` son la mordida (`tramite.mordida.discrecional`); `RES-0061`/`RES-0062` son **protesta** (`civico.protesta.agravio_urbano_encuci2020`), enumerados en §1.4. |
| «`P1` · **el** reactivo de pago informal» (singular) | La plaza exige **dos** reactivos de pago informal (`AP5_17` **y** `AP5_18`) **más** los dos de la familia de protesta (`AP7_3_5`, `AP4_3_2`). La spec cubre los cuatro; escribirla sobre uno solo habría dejado la mitad de la plaza sin procedimiento. |
| «`CORR-0003` … identidad corregida por la migración `#662`» | **CIERTO, verificado por producto**: `demanda-corridas.tsv` fila `CORR-0003` → `instrumento = ENCUCI2020`, `payload_ids = encuci2020_bd_dbf`, `entorno_requerido = CAJA`. |
| «payload `encuci2020_bd_dbf` EXISTE en manifiesto» | **EXISTE-SATISFACE en la RAÍZ, no sólo en el manifiesto**: `data/raw/BD_ENCUCI2020_dbf.zip`, 6 913 684 bytes, `sha256 0414fd59e2af…f283` — **idéntico** al declarado por el manifiesto y al `sha256_payload` de las dos enmiendas de `milpa/tramite.yaml`. |
| «(a) el inventario de reactivos es ciego a DBF (`NC-0123`)» | **CIERTO en la conclusión, FALSO en la causa** — ver §0.2. No es ceguera al DBF: `inventario-reactivos-v1_2.tsv` no trae texto de reactivo para **nada**. |
| «(b) `FP-201` mintió tres veces sobre diseño muestral» | **Miente una cuarta vez.** ENCUCI 2020 declara `FAC_SEL`, `DOMINIO`, `ESTRATO`, `UPM_DIS` y `EST_DIS` en **las cinco** tablas del DBF (§3.7). El diseño es identificable y **se usa**. |
| «(c) ENCUCI es UNA ola (2020, contexto COVID)» | **CIERTO y se estampa en cada `RESULT`**: ventana de referencia declarada por el propio reactivo, «los últimos 12 meses, es decir, de **agosto de 2019** a la fecha». Ningún estimador se puentea a la serie ENCIG. |
| «`P0` · `NC-0114` si el día ya la dejó» | **No la dejó.** Sin corrida de adquisición posterior al retiro del cron legado — §0.4. Cero espera, la pieza no bloqueó nada. |

Ninguna cifra del encargo se dio por buena sin comando.

### 0.2 · Cobertura retroactiva

**(a) La spec no existe.** `ls forense/prereg-caja/` sobre el **listado completo**
del directorio (A.13: el directorio entero, no una muestra) → **0** aciertos de
`encuci`; control positivo `encig` → **1**, `exit 0`. `NO-ENCONTRADO`:
producirla no duplica nada.

**(b) El texto de los reactivos no está en ningún inventario de la casa.**
Cuatro archivos examinados, con universo declarado:

| inventario | filas | filas ENCUCI | de ellas, con `texto_reactivo` | de mis 9 variables |
|---|---|---|---|---|
| `data/inventario-reactivos-v1_2.tsv` (el vigente) | 178 246 | **458** | **0** | 0 |
| `data/inventario-reactivos-ext-v1_0.tsv` | 63 345 (24 138 con texto) | **0** | 0 | 0 |
| `data/inventario-fd-ext-v1_0.tsv` | — | **62** (todas con texto) | 62 | **0** — son descripciones de **tabla**, no de variable |
| `data/inventario-fd-v1_1.tsv` | — | **0** | 0 | 0 |

**El matiz corrige a `NC-0123`:** `inventario-reactivos-v1_2.tsv` no trae
`texto_reactivo` para **ninguna** de sus 178 246 filas — ni DBF ni CSV, ni
ENCUCI ni ENCIG (control positivo: `encig`, 10 465 filas, **0** con texto). La
ceguera no es al formato DBF; es de la columna entera en ese archivo. Y el
único inventario que **sí** trae texto (`-ext-v1_0`) no tiene **ninguna** fila
de ENCUCI. Consecuencia operativa idéntica a la que el encargo anticipa:
**todo código y todo texto de esta spec sale del `FD_ENCUCI2020.pdf`, y ningún
negativo de esta spec se apoya en el inventario.**

**(c) Los valores GEN1 existen y son control positivo, jamás insumo (E.1).**
Los cuatro están sellados en `milpa/tramite.yaml` desde agosto/septiembre
(líneas 76-77 y 1229-1230). **Lo que falta es la cadena, no los números.**

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Al congelar, esta sesión ya había leído:

1. Los **cuatro** valores GEN1 (`0.125822`, `0.874178`, `0.112192`, `0.091912`)
   en el encargo, en `demanda-resultados.tsv` y en `milpa/tramite.yaml`.
2. La **codificación GEN1 completa** de la familia A, en el bloque
   `enmienda_encuci2020` de `milpa/tramite.yaml`: `desenlace: "AP5_17|AP5_18 --
   compuesto: 1 si AP5_17=1 o AP5_18=1"`, `ponderador: FAC_SEL`, `universo:
   "SEC_4_5 con contacto declarado AP5_16_1..10>=1 … (n≈13435 de 21519)"`,
   `ic95: [0.116323, 0.135544]`, `n: 13435`.
3. La codificación GEN1 completa de la familia B, en el bloque de la regla
   `civico.protesta.agravio_urbano_encuci2020`: `universo: "20 187 de 21 519 =
   93.80%. Desenlace AP7_3_5==1 (alguna vez protesta) x DOMINIO agrupado
   (urbano/rural) x AP4_3_2"`, `ponderador: FAC_SEL`, y los dos contrastes
   `C1_entorno_con_agravio` (+2.0279 pp, IC95 [-0.1796, 4.1211], NO-DISCRIMINA)
   y `C2_agravio_en_urbano` (+3.7233 pp, IC95 [2.2183, 5.2206], CORROBORADA).
4. Las anotaciones `SEMANTICA (D4, NC-0113)` y `DERIVADO-NO-MEDIDO (D1,
   NC-0108)` que `ACTO GEN2-MOTOR-SEMANTICA` dejó sobre las dos conductas de la
   familia A.

**Por eso las PRIMARIAS de esta spec NO son las de GEN1.** La primaria de la
familia A es **`A-P-ENTREGA`** (`AP5_18` solo: la entrega efectiva), elegida
por el codebook — es el único reactivo de ENCUCI que pregunta si **dio**, y es
el que corresponde al nombre de la conducta `paga_mordida`. La celda GEN1
(`AP5_17|AP5_18`) se mide igual, como **`A-P-CUALQUIERA`**, y es la única
adoptable (§5.3). La primaria de la familia B es el **eje completo de 2×2
celdas**, no sólo las dos con agravio.

**Lo genuinamente desconocido al congelar** —y por tanto lo único que esta
corrida puede descubrir— es: el peso del residuo `9`/blanco en cada reactivo;
cuánto separan `A-P-SOLICITUD` y `A-P-ENTREGA` (nadie lo ha medido: GEN1 sólo
publicó la unión); la prevalencia de la familia A sobre la **población
completa** y no sólo sobre el recorte de contacto; el reparto de `DOMINIO`
entre sus **tres** valores `U`/`C`/`R` y qué le hace al eje la asignación de
`C`; el perfil de las llaves opacas; y si los tipos que el DBF declara
coinciden con los que el descriptor declara. **Ninguno aparece en fuente
alguna leída.**

### 0.4 · `P0` · `NC-0114` — la correlación que el día no dejó

Verificado al abrir, con cero espera:

- Último disparo de producción: **2026-09-09 07:30:07**, dos `run_id` en el
  mismo segundo (`…-491` crontab de WSL, `…-371` Task Scheduler), ya
  atribuido y sellado por `ACTO GEN2-ADQ-VERIFICACION-CAJA` (`PR #666`).
- Retiro del crontab legado: `PR #668`, fusionado **2026-09-09 15:16 local**.
- `forense/adq-log/2026-09-09.log` termina a las **07:34**; no hay archivo de
  log posterior. `Get-ScheduledTaskInfo \ModeladoMexicano\AdquiereCron` →
  `LastRunTime = 09/09/2026 07:30:00`, `LastTaskResult = 0`,
  **`NextRunTime = 09/10/2026 07:30:00`**, `NumberOfMissedRuns = 0`.

**Veredicto: «sin corrida posterior aún».** La única corrida existente es
**anterior** al retiro, así que no puede probar que el disparador quedó único.
`NC-0114` **sigue ABIERTA**, sin cambio.

`NC-0120` tampoco avanza: `(Get-WinEvent -ListLog
'Microsoft-Windows-TaskScheduler/Operational').IsEnabled` → **`False`**. El
canal sigue deshabilitado; la pierna de eventos de la correlación sigue sin
existir. Se anota, no se cierra.

---

## 1 · Identidad

### 1.1 · Payload, por el manifiesto y por la raíz

| campo | valor |
|---|---|
| `id` | `encuci2020_bd_dbf` |
| archivo | `BD_ENCUCI2020_dbf.zip` (`data/raw/`) |
| `sha256` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` — **verificado byte a byte en la caja**, idéntico al manifiesto |
| tamaño | 6 913 684 bytes |
| `url_origen` | `https://www.inegi.org.mx/programas/encuci/2020/` |
| descriptor | `data/raw/FD_ENCUCI2020.pdf` (`encuci2020_fd_pdf`, 1 758 249 bytes, 61 páginas) |

### 1.2 · Ola, población y periodo, por el descriptor

- **Instrumento:** Encuesta Nacional de Cultura Cívica (ENCUCI) **2020**. Una
  sola ola: no hay serie ENCUCI en el corpus para este constructo.
- **Población:** «población mexicana de **15 años y más**, residente en las
  viviendas seleccionadas». **No** es 18+ y **no** es 18-70.
- **Dominios de estimación declarados:** «representatividad a nivel **nacional
  urbano, nacional rural** y para **seis regiones**». Los estimadores de esta
  spec son **nacionales** (a diferencia de ENCIG 2025, que es urbano 100k+).
- **Ventana de referencia** de los reactivos de 12 meses (5.16, 5.17, 5.18):
  «los últimos 12 meses, es decir, de **agosto de 2019** a la fecha» — el
  levantamiento es de 2020 y la ventana **precede al confinamiento**, aunque la
  entrevista ocurra dentro de él. `AP7_3_5` es **«alguna vez en su vida»**: no
  tiene ventana de 12 meses.
- **Contexto COVID:** se declara como límite (§6), no se modela.

### 1.3 · Tablas, llaves, unidad y ponderador

Cinco miembros en el ZIP; conteo de registros leído de la **cabecera** de cada
`.dbf` (metadato, no registros):

| miembro | registros | campos | llave primaria (descriptor) |
|---|---|---|---|
| `ENCUCI_2020_VIV.dbf` | 21 564 | 34 | `UPM + VIV_SEL` |
| `ENCUCI_2020_SD.dbf` | 75 189 | 54 | `UPM + VIV_SEL + N_REN` |
| **`ENCUCI_2020_SEC_4_5.dbf`** | **21 519** | 164 | `UPM + VIV_SEL + R_SEL` |
| **`ENCUCI_2020_SEC_6_7_8.dbf`** | **21 519** | 156 | `UPM + VIV_SEL + R_SEL` |
| `ENCUCI_2020_SEC_9_10.dbf` | 21 519 | 50 | `UPM + VIV_SEL + R_SEL` |

- **Unidad de observación de las dos familias:** la **persona informante
  seleccionada** (secciones IV en adelante). Las 21 519 filas de `SEC_4_5` /
  `SEC_6_7_8` son personas seleccionadas, una por vivienda entrevistada.
- **Ponderador:** **`FAC_SEL`** — el descriptor lo define como «Ponderador que
  se utiliza para estimar resultados de las preguntas que se refieren al
  **informante seleccionado**». **No** se usa `FAC_VIV` (otra unidad).
- **Llave de join de la familia B:** el descriptor declara `UPM + VIV_SEL +
  R_SEL`; el DBF trae además **`ID_PER`**, definido por el propio descriptor
  como «`UPM + VIV_SEL + R_SEL`», `Alfanumérico(13)`. Esta spec **no adopta
  ninguna llave por autoridad**: mide la unicidad de las **dos** (`ID_PER` y la
  terna declarada) en las dos tablas, y si `ID_PER` no es único el join no se
  hace (§3.5).

### 1.4 · Los 4 `RESULT` de `CORR-0003`, enumerados desde la demanda vigente

Salida cruda de `data/corrida0/demanda-corridas.tsv`, fila `CORR-0003`:

```
CORR-0003  ENCUCI2020  encuci2020_bd_dbf  SIN-CANDIDATO-EN-EL-REGISTRO  4
           RES-0005;RES-0006;RES-0061;RES-0062  CAJA  PARCIAL:script+spec+spec_sha  1
```

| `RES` | consumidor (`milpa/tramite.yaml`) | `valor_legacy` | familia | clase |
|---|---|---|---|---|
| `RES-0005` | `tramite.mordida.discrecional:paga_mordida_encuci2020` | `0.125822` | **A** | primario GEN1 (unión `AP5_17|AP5_18`) |
| `RES-0006` | `tramite.mordida.discrecional:tramite_normal_encuci2020` | `0.874178` | **A** | **complemento** — `1 − 0.125822` exacto |
| `RES-0061` | `civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_urbano_con_agravio_encuci2020` | `0.112192` | **B** | celda del eje |
| `RES-0062` | `civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_rural_con_agravio_encuci2020` | `0.091912` | **B** | celda del eje |

`RES-0005 + RES-0006 = 1.000000` **exacto**: `RES-0006` es un complemento
derivado, y `milpa/tramite.yaml:77` ya lo anota así
(`DERIVADO-NO-MEDIDO (D1, NC-0108)`). `RES-0061 + RES-0062 = 0.204104`: **no**
son complementos entre sí, son dos celdas de un eje — las dos son cantidades
primarias, y las dos son adoptables si reproducen.

---

## 2 · Los reactivos, verbatim del descriptor

### 2.1 · Familia A — el filtro 5.16 y los dos reactivos de pago informal

**Filtro (5.16), tabla `SEC_4_5`, variables `AP5_16_1` … `AP5_16_10`:**

> «En los últimos 12 meses, es decir, de agosto de 2019 a la fecha, ¿ha tenido
> contacto con alguno de los siguientes funcionarios o servidores públicos,
> incluso a través de un intermediario?»

Diez incisos: 1 Policía (de tránsito, seguridad pública) · 2 Ministerio Público
· 3 Jueces · 4 Médico(a)/Enfermero(a)/Servidor(a) social en hospital o clínicas
públicas · 5 Maestros(as) de escuelas o universidades públicas · 6 Autoridades
de seguridad social y bienestar · 7 Empleados de oficinas de gobierno en los
municipios o alcaldías · 8 Empleados de oficinas de gobierno estatal o federal
· 9 Guardia Nacional · 10 Ejército y Marina.

Códigos de cada inciso: **`1` Sí · `2` No · `9` No sabe/no responde**.
**Ninguno declara código `b`** → el bloque 5.16 se pregunta a **toda** la
persona seleccionada. (Es el control positivo de la lógica del blanco: cuando
el descriptor no declara `b`, la pregunta es universal.)

**`AP5_17` (5.17) — SOLICITUD:**

> «De esos contactos, en los últimos 12 meses, es decir de agosto a la fecha
> ¿hubo alguna ocasión en la que un funcionario o servidor público le haya
> **pedido** dar una dádiva, un favor o dinero extra por un asunto o trámite
> relacionado con sus funciones?»

Códigos: **`1` Sí · `2` No · `9` No sabe/no responde · `b` blanco**.

**`AP5_18` (5.18) — ENTREGA:**

> «En los últimos 12 meses, es decir de agosto a la fecha ¿hubo alguna ocasión
> en la que **tuvo que darle** a alguno de ellos una dádiva, un favor o dinero
> extra (que no sea la tarifa oficial) por un asunto o trámite?»

Códigos: **`1` Sí · `2` No · `9` No sabe/no responde · `b` blanco**.

**Lo que esto significa, y que corrige una anotación vigente del motor.**
`milpa/tramite.yaml:76` anota `paga_mordida_encuci2020` como «SEMANTICA (D4,
`NC-0113`): mide **solicitud** de pago informal, **no pago consumado**». Esa
lectura es correcta para ENCIG 2025 (cuyo reactivo 8.3 sólo pregunta si le
solicitaron) pero **no** describe la celda de ENCUCI: la celda GEN1 es la
**unión** `AP5_17|AP5_18`, y `AP5_18` es exactamente el pago consumado. La
celda ENCUCI mide **«le pidieron O dio»**, que no es ninguna de las dos cosas
por separado. Esta spec **no edita esa anotación** (fuera de perímetro): la
mide — emite `A-P-SOLICITUD`, `A-P-ENTREGA` y `A-P-CUALQUIERA` por separado, y
un veredicto `A-VEREDICTO-SEMANTICA` que la contesta con dato.

### 2.2 · Familia B — protesta y agravio

**`AP7_3_5` (7.3 inciso 5), tabla `SEC_6_7_8` — DESENLACE:**

> «Alguna vez en su vida, ¿ha realizado alguna de las siguientes actividades
> relacionadas con asuntos públicos? … 5. **Participado en una protesta**»

Códigos: **`1` Sí · `2` No · `9` No sabe/no responde · `b` blanco**.

⚠️ **El mapeo de códigos es POR REACTIVO, no por batería (A.15c).** Dentro de
la **misma** pregunta 7.3, el inciso `AP7_3_4` («Recurrido a un partido
político») declara **`3` = No sabe/no responde** donde sus nueve hermanos
declaran `9`. No es mi variable, pero prueba el punto: en este descriptor,
heredar el mapeo del inciso vecino es un error mecánico. Cada variable de esta
spec trae su dominio **escrito uno por uno** en §3.

**`AP4_3_2` (4.3 inciso 2), tabla `SEC_4_5` — EJE DE AGRAVIO:**

> «¿En su (COLONIA/LOCALIDAD) han tenido problemas de… 2. **pandillerismo,
> robos o delincuencia?**»

Códigos: **`1` Sí · `2` No · `9` No sabe / no responde**. **Sin código `b`** →
universal para la persona seleccionada.

**Nota de alcance obligatoria:** «agravio» en esta plaza **no** es un agravio
genérico ni personal. Es, literalmente, **problema declarado de pandillerismo,
robos o delincuencia en la colonia o localidad** — percepción de entorno, no
victimización propia. Todo `RESULT` de la familia B lo estampa.

**`DOMINIO`, tablas `SEC_4_5` y `SEC_6_7_8` — EJE DE ENTORNO:**

El descriptor lo declara `Alfanumérico`, longitud 1, con **tres** valores:

| código | concepto |
|---|---|
| `U` | Urbano |
| `C` | **Complemento urbano** |
| `R` | Rural |

⚠️ **Tres valores, no dos.** La cita GEN1 dice «`DOMINIO` agrupado
(urbano/rural)» y **no dice cómo se agrupó `C`**. Esta spec lo congela en §3.4
y mide la sensibilidad de esa elección, en vez de heredarla.

---

## 3 · Universos, codificación y unidad — todo pre-declarado

### 3.1 · Regla general

- **Cero nunca sustituye falta de dato.** `9` (NS/NR) y blanco **salen** del
  universo del punto, **contados** en su propio `RESULT`, y jamás se imputan.
- Las sumas ponderadas se hacen en **orden fijo de fila** (el del archivo).
- **`NO-APLICA` es un valor**: cada `RESULT` que no aplica a una familia se
  emite con ese texto, no se omite.
- Toda comparación de código se hace sobre el valor **normalizado** por
  `_cod()` (§3.3), nunca por comparación de cadena cruda contra `"1"`.

### 3.2 · Tipos: **lo que el header del DBF declara manda sobre el descriptor**

Leído de los descriptores de campo de 32 bytes de cada `.dbf` (tipo en el byte
11, ancho en el 16, **decimales en el 17**), **antes** de codificar nada:

| variable | tabla | descriptor (FD) dice | **el DBF declara** | consecuencia |
|---|---|---|---|---|
| `AP5_16_1`…`_10` | `SEC_4_5` | Numérico, long. 1 | **`N` 19,15** | el texto crudo llega como `1.000000000000000`; **comparar por valor numérico** |
| `AP5_17` | `SEC_4_5` | Numérico, long. 1 | **`C` 6,0** | llega `'1'`/`'2'`/`'9'`/`''` |
| `AP5_18` | `SEC_4_5` | Numérico, long. 1 | **`C` 6,0** | idem |
| `AP4_3_2` | `SEC_4_5` | Numérico, long. 1 | **`N` 19,15** | comparar por valor numérico |
| `AP7_3_5` | `SEC_6_7_8` | Numérico, long. 1 | **`C` 7,0** | llega como cadena |
| `FAC_SEL` | ambas | Numérico, **1-999999, long. 6** | **`N` 19,10** | **no se normaliza, no se redondea, no se trunca**: se lee como flotante tal cual |
| `DOMINIO` | ambas | Alfanumérico, long. **1** | **`C` 7,0** | cadena opaca, `strip()` y comparar |
| `ESTRATO` | ambas | Numérico, `1,2,3,4`, long. **1** | **`C` 7,0** | cadena opaca |
| `UPM_DIS` | ambas | Carácter, long. **7** | **`C` 7,0** | **llave opaca de texto** |
| `EST_DIS` | ambas | Carácter, long. **3** | **`C` 7,0** | **llave opaca de texto** — el ancho del papel (3) **no** es el del archivo (7) |
| `ID_PER` | ambas | Alfanumérico, long. 13 | **`C` 13,0** | cadena |

**Cuatro de las once discrepan del descriptor en tipo o en ancho.** La regla es
la del encargo, verbatim: *«tipos tal como el header los declara (FAC como lo
diga, jamás normalizar)»*.

### 3.3 · `_cod()` — la normalización, escrita antes del dato

`_cod(v)` devuelve un **entero** si el texto crudo del campo, tras `strip()`,
parsea como flotante finito con parte fraccionaria nula; devuelve `None` en
cualquier otro caso (vacío, `'b'`, no numérico, con decimales). Así `'1'` y
`'1.000000000000000'` dan **el mismo** `1`, sin que la spec tenga que apostar
por uno de los dos formatos.

**Guardia `G-3`, pre-declarada, que mide la trampa en vez de suponerla.**
Sobre `AP5_16_1`, se emiten **los dos** conteos: filas cuyo texto crudo es
exactamente `"1"` (`G-N-AP5-16-1-CADENA-UNO`) y filas con `_cod(...) == 1`
(`G-N-AP5-16-1-NUMERICO-UNO`), más el veredicto
`G-VEREDICTO-TIPO-AP5-16` ∈ {`CADENA-Y-NUMERO-COINCIDEN`,
`SOLO-NUMERO-ACIERTA`, `SOLO-CADENA-ACIERTA`, `NINGUNO-ACIERTA`}. Si el
segundo conteo es 0 el universo A queda vacío y la corrida **para** con
`NO-ESTIMABLE-UNIVERSO-VACIO` — no publica un cero.

### 3.4 · Familia A · unidad **PERSONA**, ponderador `FAC_SEL`

`U_A` (universo del punto), sobre `SEC_4_5`:

1. `FAC_SEL` finito y `> 0` (si no → `A-N-SIN-PONDERADOR`, fuera);
2. **contacto declarado**: `_cod(AP5_16_k) == 1` para **algún** `k ∈ 1..10`
   (si no → `A-N-SIN-CONTACTO`, fuera del punto, **contado**);
3. `_cod(AP5_17) ∈ {1,2}` **y** `_cod(AP5_18) ∈ {1,2}` (si alguno cae en `9`,
   blanco o fuera de dominio → fuera, contado en
   `A-N-NSNR-17`/`A-N-NSNR-18`/`A-N-BLANCO-17`/`A-N-BLANCO-18`/
   `A-N-FUERA-DE-DOMINIO`).

Desenlaces sobre `U_A`:

- `d(SOLICITUD) = 1` si `AP5_17 = 1`, `0` si `= 2`.
- `d(ENTREGA) = 1` si `AP5_18 = 1`, `0` si `= 2`.
- `d(CUALQUIERA) = 1` si `AP5_17 = 1` **o** `AP5_18 = 1`; `0` si ambos `= 2`.
  **(la codificación GEN1, verbatim de `enmienda_encuci2020`)**
- `d(AMBAS) = 1` si `AP5_17 = 1` **y** `AP5_18 = 1`; `0` en otro caso.

`U_A_POB` (**segundo denominador, pre-declarado**): las filas de `SEC_4_5` con
`FAC_SEL` válido que **sin contacto** (`d = 0`) o que están en `U_A`
(`d = d(CUALQUIERA)`). El `0` de «sin contacto» **no es imputación**: 5.17
pregunta «**De esos contactos**…», así que sin contacto no hay ocasión posible
— y es exactamente por eso que el descriptor declara el código `b` en 5.17 y
5.18 y **no** lo declara en 5.16.

**Las filas con contacto y con `9`/blanco NO entran a `U_A_POB` como `0`.**
Ésas sí serían imputación: salen, y su peso se reporta aparte en
`A-P-RESIDUO-POBLACION` sobre el total de filas con ponderador válido. **Cero
nunca sustituye falta de dato**, tampoco en el denominador ancho.

`A-P-CUALQUIERA-POBLACION` es la prevalencia sobre la población de 15+, no
sobre el recorte de contacto; **no** es la celda adoptable y **no** sustituye al
primario: contesta cuánto del `0.1258` sellado es propiedad del recorte.

**Complemento (`RES-0006`), bajo D1.** `A-P-COMPLEMENTO-CUALQUIERA` se emite
como **suma ponderada directa** de las filas con `d(CUALQUIERA) = 0` sobre el
**mismo** denominador `U_A` — no como `1 −` nada — y se emite además
`A-SUMA-CUALQUIERA` como prueba mecánica. **No recibe cita `corrida0_*`, no
recibe rango de medido**: la decisión ya está tomada por `D1`/`NC-0108` y esta
spec la obedece, no la reabre.

### 3.5 · Familia B · unidad **PERSONA**, join `SEC_6_7_8` × `SEC_4_5`

`U_B`:

1. join por `ID_PER` entre `SEC_6_7_8` (desenlace) y `SEC_4_5` (eje de
   agravio); filas sin pareja → `B-N-SIN-PAREJA`, fuera, contadas;
2. `FAC_SEL` (el de `SEC_6_7_8`) finito y `> 0`;
3. `_cod(AP7_3_5) ∈ {1,2}` (si no → `B-N-NSNR` / `B-N-BLANCO`, fuera);
4. `_cod(AP4_3_2) ∈ {1,2}` (si no → `B-N-AGRAVIO-NSNR`, fuera);
5. `DOMINIO` (tras `strip()`) ∈ `{U, C, R}` (si no → `B-N-DOMINIO-FUERA`,
   fuera).

Desenlace: `d(B) = 1` si `AP7_3_5 = 1`, `0` si `= 2`.

**Agrupación de `DOMINIO`, CONGELADA:** `urbano = {U, C}` · `rural = {R}`.
Razón, del propio descriptor y no del dato: el instrumento declara sus dominios
de estimación como «nacional **urbano**, nacional **rural**», y el valor `C` se
llama, literalmente, **«Complemento urbano»** — su etiqueta lo coloca dentro de
lo urbano. No se elige para acercarse a ninguna cifra GEN1.

**Sensibilidad pre-declarada, no primaria:** se emiten además las cuatro celdas
bajo la agrupación alternativa `urbano = {U}` · `rural = {R, C}`
(`B-ALT-P-*`), el conteo de filas por cada valor de `DOMINIO`
(`B-N-DOMINIO-U/-C/-R`) y `B-DELTA-AGRUPACION` (la diferencia entre
`B-P-URB-AGR` y `B-ALT-P-URB-AGR`). Así la elección queda **auditada**, no
escondida. Las celdas alternativas **no** son adoptables.

Las **cuatro** celdas del eje (primarias, todas):

| `RESULT` | celda |
|---|---|
| `B-P-URB-AGR` | urbano ∧ `AP4_3_2 = 1` — **candidata de `RES-0061`** |
| `B-P-RUR-AGR` | rural ∧ `AP4_3_2 = 1` — **candidata de `RES-0062`** |
| `B-P-URB-SIN` | urbano ∧ `AP4_3_2 = 2` |
| `B-P-RUR-SIN` | rural ∧ `AP4_3_2 = 2` |

Contrastes, **rotulados `ASOCIACION`, jamás causales**: `B-DIF-C1` = URB-AGR −
RUR-AGR (entorno, dado agravio) y `B-DIF-C2` = URB-AGR − URB-SIN (agravio,
dentro de urbano), con sus IC95 de la diferencia por el mismo bootstrap.

### 3.6 · Guardias de existencia y de llave — **paran, no adivinan**

| guardia | qué mide | rama si falla |
|---|---|---|
| `G-1` | los 5 miembros del ZIP están presentes | `NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>` |
| `G-2` | cada columna declarada existe en su tabla | `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>` |
| `G-3` | tipo de `AP5_16_1`: cadena vs número (§3.3) | universo A vacío → `NO-ESTIMABLE-UNIVERSO-VACIO` |
| `G-4` | `ID_PER` único en `SEC_4_5` y en `SEC_6_7_8`; y la terna declarada `UPM+VIV_SEL+R_SEL` también | si `ID_PER` no es único → familia B `NO-ESTIMABLE-LLAVE-NO-UNICA`; **no se elige otra llave sobre la marcha** |
| `G-5` | dominio de códigos observado ⊆ dominio declarado, por variable | se cuenta `*-N-FUERA-DE-DOMINIO`; el punto se reporta igual |
| `G-6` | `DOMINIO` observado ⊆ `{U,C,R}` | `B-N-DOMINIO-FUERA`, contado |
| `G-7` | `FAC_SEL`, `EST_DIS`, `UPM_DIS` presentes y no vacíos | `G-VEREDICTO-DISENO` |
| `G-8` | perfil de llaves opacas: longitudes observadas y si algún valor trae espacio en los bordes | `G-PERFIL-EST-DIS` / `G-PERFIL-UPM-DIS`, texto |

### 3.7 · Diseño: `FP-201` se verifica, no se hereda

El descriptor declara, en el bloque **«Campos empleados para el diseño
muestral»** de cada tabla de persona: `FAC_SEL` (ponderador), `DOMINIO`,
`ESTRATO` (`1,2,3,4`), **`UPM_DIS`** (`0000001-9999999`) y **`EST_DIS`**
(`001-999`). Confirmado en la cabecera del DBF: las cinco tablas los traen.

**`FP-201` («sin campo de diseño UPM/estrato reproducible» para las fuentes de
fase 1) es FALSO también para ENCUCI 2020.** Es la cuarta fuente en que se
comprueba falso (ENVIPE, ENIF y las tres olas de `GEN2-R-SERIE-CSV` fueron las
anteriores). El diseño **se usa**: no se renuncia al IC correcto.

**Llaves opacas.** `EST_DIS` y `UPM_DIS` se agrupan como **cadena cruda**.
Nunca `int()`, nunca `zfill()`, nunca re-relleno al ancho del papel:
normalizarlas partiría o fusionaría estratos **en silencio**. El descriptor ya
discrepa del archivo en el ancho de `EST_DIS` (3 en el papel, 7 en el DBF), que
es exactamente el síntoma que la lección de `GEN2-R-SERIE-CSV` documenta.

**Método de IC — ranura no pre-registrada.** Nadie pre-registró un método de IC
para ENCUCI. Lo elige el ejecutor sobre ranura vacía, se declara y **se eleva a
mesa**: bootstrap de `UPM_DIS` **con reemplazo dentro de** `EST_DIS`,
conservando el número de UPM por estrato, 2 000 réplicas, percentiles
2.5/97.5, `seed` y `rng` declarados. Un estrato con **una sola** UPM se
re-muestrea a sí mismo (varianza cero): **no se colapsa** (decisión de diseño
que esta spec no está autorizada a tomar) y **no se descarta** (sesgaría el
punto); si su conteo es `> 0`, `METODO-IC` sale
`IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior de la
anchura verdadera**. **No** se espera coincidencia dígito a dígito con los
`ic95: [0.116323, 0.135544]` de la enmienda GEN1 — su método no está escrito en
ningún artefacto reproducible, y **A-bis.3 prohíbe ponerlos lado a lado**.

---

## 4 · Ramas pre-declaradas — escritas ANTES del dato

### 4.1 · Control positivo contra GEN1 (`punto, no IC`)

Se compara **sólo el punto**, con `|delta| ≤ 1e-6` como umbral de réplica:

| celda medida | valor GEN1 | `RESULT` de delta |
|---|---|---|
| `A-P-CUALQUIERA` | `0.125822` (`RES-0005`) | `A-DELTA-VS-GEN1` |
| `A-P-COMPLEMENTO-CUALQUIERA` | `0.874178` (`RES-0006`) | `A-DELTA-COMP-VS-GEN1` |
| `B-P-URB-AGR` | `0.112192` (`RES-0061`) | `B-DELTA-URB-VS-GEN1` |
| `B-P-RUR-AGR` | `0.091912` (`RES-0062`) | `B-DELTA-RUR-VS-GEN1` |

`*-REPRODUCE-GEN1` ∈ {`REPRODUCE`, `NO-REPRODUCE`, `NO-COMPARABLE`}. Un
`NO-REPRODUCE` **no invalida** la corrida, **no autoriza** tocar el medidor y
**no se ajusta hacia atrás**: se reporta con su embudo.

Además, control de `n`: `A-N-U` contra la `n: 13435` que la enmienda declara
(`A-DELTA-N-VS-GEN1`), y `B-N-U` contra las `20 187` que la regla declara
(`B-DELTA-N-VS-GEN1`). Son conteos, no estimaciones: si difieren, el universo
no es el mismo aunque el punto coincida.

### 4.2 · Semántica de la familia A (`A-VEREDICTO-SEMANTICA`)

Pre-declarado, decidido por el dato:

- `SOLICITUD-Y-ENTREGA-COINCIDEN` si `|A-P-SOLICITUD − A-P-ENTREGA| ≤ 1e-9`;
- `LA-UNION-EXCEDE-A-CADA-PARTE` si `A-P-CUALQUIERA >` ambas, en cuyo caso la
  anotación `NC-0113` («mide solicitud, no pago consumado») **no describe** la
  celda ENCUCI y se dice así, con las tres cifras;
- `ENTREGA-DOMINA` / `SOLICITUD-DOMINA` según cuál sea mayor.

Se emite también `A-P-AMBAS` y `A-P-SOLICITUD-SIN-ENTREGA` (pidieron y no dio):
la fracción de solicitudes que **no** terminan en entrega, que es el dato que
distingue los dos constructos y que nadie ha medido en esta fuente.

### 4.3 · Exhaustividad del par de la familia A (`A-VEREDICTO-EXHAUSTIVIDAD`)

`EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO` si `A-SUMA-CUALQUIERA = 1` y no hay
ninguna fila en `9`/blanco/sin-contacto; `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U_A`
si suman 1 pero el residuo pesa `> 0`; `NO-EXHAUSTIVAS` si no suman 1.
`A-P-RESIDUO-POBLACION` da el peso de lo que `U_A` deja fuera sobre `U_A_POB`.

### 4.4 · Criterio de adopción de P3, pre-declarado (patrón `NC-0085`)

Un `RESULT` es **`CANTIDAD-MEDIDA`** — y sólo entonces recibe cita
`corrida0_resultado_id` + `corrida0_generacion: GEN2` en `milpa/tramite.yaml` —
si y sólo si:

1. su numerador es una categoría declarada del reactivo **contada
   directamente** — no `1 −` otra cosa; **y**
2. `round(medido, 6) == valor_sellado` (el grano con que `milpa/` materializa).

En otro caso: `NO-ADOPTABLE-POR-DISCREPANCIA` (falla 1e-6),
`NO-ADOPTABLE-POR-GRANO` (reproduce a 1e-6 pero no al sexto decimal),
`COMPLEMENTO-CON-DENOMINADOR-RECORTADO` (falla la condición 1) o
`NO-ADOPTABLE-NO-ESTIMABLE`.

**Predeterminado por construcción:** `RES-0006` **no puede** ser adoptable —
falla la condición 1 por ser el complemento que `D1` ya declaró
`DERIVADO-NO-MEDIDO`. Se dice aquí, antes de medir, para que no parezca una
conclusión encontrada a posteriori. Los otros tres se deciden por la medición,
no por la lista.

**El `p` no se mueve.** La adopción es **cita**, no cambio de cifra: si una
celda reproduce, se escribe de dónde viene; si no reproduce, no se escribe cita
y eso es el hallazgo.

---

## 5 · Estimando

**DESCRIPTIVO.** Ningún `RESULT` es causal.

- **Primarios de A:** `A-P-ENTREGA` (pago informal efectivo, el reactivo que
  corresponde al nombre `paga_mordida`) y `A-P-SOLICITUD`.
- **Celda adoptable de A:** `A-P-CUALQUIERA` (la codificación GEN1). Se mide
  igual y con el mismo rigor; **no** es la primaria por codebook.
- **Primarias de B:** las **cuatro** celdas del eje `entorno × agravio`.
- **Secundarios declarados:** `A-P-CUALQUIERA-POBLACION`, `A-P-AMBAS`,
  `A-P-SOLICITUD-SIN-ENTREGA`, el complemento con su denominador escrito, las
  cuatro celdas de la agrupación alternativa de `DOMINIO`, los pesos residuales
  y todos los conteos de embudo.
- `B-DIF-C1` y `B-DIF-C2` van rotuladas **`ASOCIACION`**: entorno y agravio no
  se asignan al azar, y quien vive en zona urbana con problemas de delincuencia
  no es una muestra aleatoria de nadie.

---

## 6 · Límites declarados (van también en la nota de cierre)

- **Una sola ola.** ENCUCI 2020. **No se puentea a la serie ENCIG** ni se
  compara con ENCIG 2025 en ninguna salida. La comparabilidad entre ENCUCI 2020
  y ENCIG 2025 queda **declarada como pregunta abierta, no como supuesto**:
  mismo constructo (pago informal a servidor público) **≠** mismo instrumento —
  difieren el universo (nacional 15+ vs. urbano 100k+ 18+), la ventana
  (12 meses desde agosto 2019 vs. «durante 2025»), el filtro de entrada
  (contacto con 10 tipos de funcionario vs. realización de trámites) y el
  reactivo (dos preguntas, solicitud y entrega, vs. tres incisos de solicitud).
  **Cruzarlas exige su propio pre-registro**; esta spec no lo hace.
- **Contexto COVID.** El levantamiento es de 2020; la ventana de referencia de
  la familia A empieza en agosto de 2019 y por tanto **precede** al
  confinamiento, mientras que la entrevista ocurre dentro de él. El desenlace
  de la familia B es «alguna vez en su vida». Ni el contexto ni su efecto se
  modelan: se declaran.
- **Causalidad: ninguna.**
- **IC como límite inferior** si algún estrato queda con una sola UPM.
- **Ranura de IC no pre-registrada** — elegida por el ejecutor, elevada a mesa.
- **Contaminación (ADR-46):** la corrida **no es ciega**; §0.3 la declara
  entera.
- **`FAC_SEL` es el ponderador de persona seleccionada.** Ningún estimador de
  esta spec es de vivienda, y `FAC_VIV` no se usa.

---

## 7 · Congelamiento

Esta spec se escribe y se commitea **antes** de que el medidor lea un solo
registro. `data/corrida0/CALC-ENCUCI-0001/spec.yaml` es su cara mecánica y cita
su `sha256`; `medidor.py` se congela en el mismo commit y **no se edita
después** — si resultara equivocada, se escribe una `v1.1` fechada, nunca una
corrección hacia atrás.

**El primer resultado que produzca este procedimiento es el que se reporta.**
