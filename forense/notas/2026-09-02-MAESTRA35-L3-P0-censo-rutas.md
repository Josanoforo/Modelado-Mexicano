# `ACTO MAESTRA35-L3` — `P0`, censo de rutas y tabla de identificación

Commit de `P0`. Se escribe **antes** de depositar un solo byte en el corpus y
**antes** de abrir un solo resultado. Todo veredicto de este documento sale de
una sonda real de **esta** sesión (2/sep/2026, ~15:00-15:15 CST), con el código
crudo a la vista; **ninguno se hereda de memoria ni de un acto anterior** (`A.5`).

Convención de este acto, declarada: **sondear e inspeccionar en el directorio
temporal de la sesión es censo (`P0`); depositar en el corpus compartido y
registrar en el manifiesto es adquisición (`P1`)**. Ningún archivo de este censo
está todavía en `data/raw/`.

---

## §0 · Firma de entorno y herramienta de sonda

| parte | valor crudo |
|---|---|
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | `sin_variable` |
| `curl … https://www.inegi.org.mx/` | **200** |
| `curl … https://repositoriodocumental.ine.mx/` | **200** |
| `curl … https://www.ieehidalgo.org.mx/` | **403** con el UA por defecto de `curl`; **200** (309 190 B) con UA de navegador |
| `ls data/raw/ \| head -1` | `2005trim1_csv.zip` (370 entradas; enlazada a `/home/pc0/mm-corpus/raw`) |

Los hosts que `ADR-288` midió bloqueados por IP (`siceen`, `siceef`,
`computos2024`, `portalanterior`, `prep2021` de `ine.mx`) **no se sondearon**.

**Herramienta de sonda de este acto**, porque dos veredictos dependen de ella:
`curl -s -L --max-time N -A "<UA de navegador>" --cacert <paquete>`. El UA de
navegador es necesario (Hidalgo devuelve 403 sin él); el paquete de CA es
necesario por `§1`.

---

## §1 · Un defecto de transporte que el censo atrapó (candidato `FP-247`)

`https://www.ieebc.mx/` y `https://www.ieepco.org.mx/` devolvieron
`http_code = 000`. La salida cruda:

```
curl: (60) SSL certificate OpenSSL verify result: unable to get local issuer certificate (20)
```

**No es el sandbox y no es un bloqueo**: los dos servidores mandan una **cadena
incompleta**. Medido abriendo la sesión TLS a través del proxy y leyendo lo que
el servidor presenta:

| host | certs que presenta | emisor del hoja | intermedio que falta |
|---|---:|---|---|
| `www.ieebc.mx` | **1** (sólo la hoja) | Go Daddy Secure Certificate Authority - G2 | `http://certificates.godaddy.com/repository/gdig2.crt` |
| `www.ieepco.org.mx` | **2** (la hoja, dos veces) | GeoTrust TLS RSA CA G1 | `http://cacerts.geotrust.com/GeoTrustTLSRSACAG1.crt` |

Bajando los dos intermedios y anexándolos al almacén del sistema
(121 → 123 certificados), **los dos pasan a 200** con verificación real:

```
www.ieebc.mx           200|279635|text/html; charset=UTF-8
www.ieepco.org.mx      200|65652|text/html; charset=UTF-8
```

**En ningún momento se usó `--insecure`.** Es la misma clase de defecto que el
proyecto ya midió en la CNBV: un negativo de red que era una cadena de
certificados, no una puerta cerrada. Sin esta reparación, Baja California —que
resulta ser la entidad **mejor** documentada de las 12— se habría declarado
`NO-OBTENIDO` por un motivo falso.

---

## §2 · Alcance de los 12 faltantes y sonda de portal (A.4, A.13)

`P0` de `MAESTRA34-L6` fijó **14** entidades `TRATADO`; `L6` midió **2**
(Coahuila, Nayarit). Faltan **12**, y Zacatecas está entre ellas porque su pata
**2016** —la única no concurrente de su serie— nunca se adquirió.

Sonda de portal, una por entidad, con el comando de `§0` (12 hosts examinados,
12 con salida cruda registrada):

| entidad | host | código | lectura |
|---|---|---:|---|
| Hidalgo | `www.ieehidalgo.org.mx` | **200** | alcanzable (con UA de navegador) |
| Zacatecas | `www.ieez.org.mx` | **200** | alcanzable |
| Aguascalientes | `www.ieeags.mx` | **200** | alcanzable, **pero ver `§4`** |
| Chiapas | `www.iepc-chiapas.org.mx` | **200** | alcanzable |
| Chihuahua | `ieechihuahua.org.mx` | **200** | alcanzable |
| Quintana Roo | `www.ieqroo.org.mx` | **200** | alcanzable |
| Sinaloa | `www.ieesinaloa.mx` | **200** | alcanzable (portada de 151 MB) |
| Tamaulipas | `www.ietam.org.mx` | **200** | redirección `meta refresh` a `/PortalN/` |
| Oaxaca | `www.ieepco.org.mx` | **000 → 200** | recuperada por `§1` |
| Baja California | `www.ieebc.mx` | **000 → 200** | recuperada por `§1` |
| Tlaxcala | `www.itetlax.org.mx` | **200** | SPA de React (1 283 B de cascarón) |
| **Veracruz** | `www.oplever.org.mx` | **403** | reto de Cloudflare («Just a moment…») **también con UA de navegador** → sólo navegador |

**11 de 12 alcanzables por programa. 1 (Veracruz) no.**

---

## §3 · El `.rar` de Hidalgo 2016 (`P0 (ii)`), medido

```
$ head -c 16 data/raw/electoral_local_municipal_serie/ieeh_hidalgo_2016_ayuntamientos.rar | xxd
00000000: 5261 7221 1a07 00cf 9073 0000 0d00 0000  Rar!.....s......
$ file …
RAR archive data, v4, os: Win32
```

Extractores, uno por uno (**7 binarios + 3 módulos examinados**):

| candidato | resultado |
|---|---|
| `bsdtar` `unrar` `unar` `7z` `7za` `7zz` `p7zip` | **los 7 AUSENTES** |
| `python3 -c "import rarfile"` | `ModuleNotFoundError` |
| `python3 -c "import patoolib"` | `ModuleNotFoundError` |
| `python3 -c "import py7zr"` | **OK, 1.1.3** — pero `py7zr` lee **7z**, no **RAR** |
| `libarchive` (`ctypes.util.find_library('archive')`) | **None** |

**Veredicto: la pata Hidalgo 2016 va `NO-OBTENIDO-POR-ESTE-AGENTE`** por falta de
extractor, con la receta de `§6`. No se instaló nada fuera de `pip` y de hecho no
se instaló nada: `rarfile` sin binario `unrar` de respaldo tampoco descomprime
entradas RAR3 comprimidas, así que instalarlo no habría cambiado el veredicto.

---

## §4 · Censo de rutas, por entidad y por pata

Vocabulario de la cola. `VOTOS` y `DENOMINADOR` se dictaminan por separado,
porque son el defecto real: **de las 12, ninguna carecía de votos publicados; la
que falta casi siempre es la lista nominal.**

### Baja California — **RUTA COMPLETA, las 4 patas** ✅

`https://ieebc.mx/archivos/estadisticas/elecciones/<año>/` publica la serie
histórica **1995…2025** por casilla. Descargados a temporal e inspeccionados:

| pata | archivo | bytes | cabecera (fila 6) |
|---|---|---:|---|
| 2016 | `Municipes_X_Casilla_Final.xlsx` | 1 195 969 | `MUNICIPIO, DISTRITO, SECCION, TIPO, …, TOTAL VOTOS, LISTA NOMINAL, % DE PARTICIP., % DE ABST.` |
| 2019 | `ComputoPorCasilla_Mun.xls` | 2 723 328 | idem (4 812 filas) |
| 2021 | `ComputoPorCasilla_Mun_Ajustado_Tribunal_SG.xls` | 3 468 288 | idem (4 978 filas) |
| 2024 | `ComputoPorCasilla_Mun Encabezados.xls` | 1 718 272 | idem (5 397 filas) |

**Las cuatro traen `LISTA NOMINAL` y `% DE PARTICIP.` en la misma fila que los
votos** — denominador en la fuente y control aritmético gratis. `VOTOS`
`OBTENIBLE`, `DENOMINADOR` `OBTENIBLE`, las 4 patas.

### Zacatecas 2016 — **RUTA COMPLETA, la pata que faltaba** ✅

`https://ieez.org.mx/PE_2016.html` enlaza:

* `resultados/ayuntamientos_2016.htm` (200, 158 315 B) — tabla HTML con
  cabecera **`Municipio | LN | …`**: lista nominal por municipio, 66 filas `<TR>`;
* `resultados/Eleccion_2016_CON_CASILLAS.xls` (200, 3 270 144 B,
  `Composite Document File V2`, sha256 `a39c946b…`) — cómputo por casilla.

`VOTOS` `OBTENIBLE`, `DENOMINADOR` `OBTENIBLE`.

⚠️ Aviso de método que este censo pagó una vez: la primera sonda escribió dos
URL distintas en **el mismo nombre de archivo** y el `404` de la segunda pisó el
`200` de la primera; el `.xls` parecía contener `Not Found [CFN #…`. Se
identifica el contenido por su identidad (magic bytes, tamaño, sha), no por el
código de la última respuesta.

### Hidalgo — **VOTOS sí, DENOMINADOR `NO-ENCONTRADO`** ❌

| pata | votos | denominador |
|---|---|---|
| 2016 | `.rar` en corpus, **sin extractor** (`§3`) | — |
| 2020 | `ieeh_hidalgo_2020_computos_x_casilla.xlsx` en corpus, **84 hojas, ninguna con lista nominal** — verificado columna por columna: las 84 terminan en `TOTAL`. Re-descargado del IEEH hoy: **sha256 `1491d182…` idéntico byte a byte al del corpus** | **no existe en la fuente** |
| 2024 | `ieeh_hidalgo_2024_computos.zip` → `Ayuntamientos.zip` → 86 XLSX por municipio; cabecera de 23 columnas `# iddistritolocal … seccion, numcasilla, …, VN, TOTAL` — **trae `seccion`, no trae lista nominal** | **no existe en la fuente** |

Rutas de denominador probadas para Hidalgo, con sonda de esta sesión:

1. **El propio IEEH**: no publica listado nominal. Su página de 2019-2020 dice
   explícitamente que esa información es del INE.
2. **`www.ine.mx/credencial/estadisticas-lista-nominal-padron-electoral/`**
   (re-sondeo declarado: `MAESTRA34-L3` preguntó por **sección**; aquí se
   pregunta por **municipio**, que es una agregación más gruesa y más común).
   200, y publica **un solo fichero**: `PE-y-LN_Nacional-Extranjero_20-08-2026.xlsx`
   — nacional, del corte vigente, sin desglose ni serie. **`NO-ENCONTRADO`, y
   ahora también para la pregunta municipal.**
3. **Catálogos DERFE del corpus** (`CRFE_22032016_1aSO_P07_1_3.xlsx`,
   `…_1_4.xlsx`): abiertos y leídos — son **catálogos puros**
   (`ENTIDAD, NOMBRE_ENTIDAD, DISTRITO_LOCAL, MUNICIPIO, NOMBRE_MUNICIPIO, SECCION`),
   **sin una sola columna de lista nominal**. Confirma lo que `L3` (`ADR-280`)
   midió: la ruta (iv) da el **crosswalk**, no el **denominador**.
4. **PREP federal 2024 del corpus** (`20240603_2005_PREP.zip`): sí trae
   `LISTA_NOMINAL` por casilla con `ID_ENTIDAD` y `SECCION` — **pero su propio
   preámbulo declara `PORCENTAJE_ACTAS_CAPTURADAS = 95.2352`**. Es un conteo
   **preliminar**: sumar su lista nominal subestima el denominador en ~5 % y
   **inflaría la participación** sin aviso. Se declara **descartado como
   denominador principal** aquí y no después de ver un número.

**Hidalgo queda `OBTENIDO-SIN-DENOMINADOR` en sus tres patas.** Es el caso que el
encargo llamaba «el más limpio del diseño» y no lo es: es el más limpio en
*calendario* y el más pobre en *denominador*.

### Aguascalientes — **defecto de portal medido, reconfirmado** ⚠️

El corpus tiene 22 XLSX de 2019 y 2021 por municipio, sin lista nominal. La ruta
del portal es una trampa que `L6` ya había medido y que este censo reconfirmó con
**24 sondas**: `https://www.ieeags.mx/media/Resultados/<ciclo>/<elección>/`
devuelve **200 para las 24 combinaciones probadas** (`1516`, `1819`, `2122`,
`2324`, `2016`, `2019`, `2021`, `2024` × `Ayuntamientos`, `Ayuntamiento`,
`Municipios`) — y **las 24 respuestas miden exactamente 34 606 bytes**: es el
mismo cascarón de la SPA. Ninguna es un directorio. El único `/media/Resultados/`
real que el JS embebido expone es `2122/Gobernador/`. **Se identifica por la
identidad de la respuesta, no por el `200`.**

### Chihuahua, Quintana Roo, Oaxaca, Tamaulipas, Chiapas, Sinaloa, Tlaxcala

Sondeadas las páginas de proceso; ninguna expone todavía el fichero de cómputos
municipales por una ruta estática hallada en este censo:

* **Chihuahua**: `_PE2015-2016`, `_PE2017-2018`, `_PE2020-2021`, `_PE2023-2024`
  existen (200) pero sólo publican *candidaturas electas*. Los resultados viven
  en `/atlas` («Atlas de Resultados Electorales»), que es un **formulario POST**,
  no un índice de archivos. Ruta viva, pero requiere POST.
* **Quintana Roo**: publica `descargas/organizacion/Padron_Listanominal/<año>/<mes>.xlsx`
  —una **serie mensual de lista nominal**, que es exactamente el denominador que
  falta en otras entidades—; los cómputos no aparecieron en este censo.
* **Oaxaca**: `autoridades_electas/resultados/` es un portal PHP por consulta.
* **Tamaulipas**: `ietam.org.mx` redirige por `meta refresh` a `/PortalN/`;
  las rutas de resultados probadas dieron 404.
* **Chiapas, Sinaloa, Tlaxcala**: portada 200, sin índice estático hallado.

**Estas 7 no reciben veredicto definitivo en `P0`**: quedan como
`PENDIENTE-DE-INTENTO` y se dictaminan en `P1` con `N` intentos y salida cruda,
dentro del tope de tiempo. Declarar aquí un `NO-OBTENIDO` sería declarar un
negativo que ningún comando examinó (`A.13`).

### Veracruz — `NO-OBTENIDO-POR-ESTE-AGENTE`, con receta ❌

`www.oplever.org.mx` responde **403** con el interstitial de Cloudflare
(`<title>Just a moment...</title>`) incluso con UA de navegador. Es exactamente
el supuesto de la firma `DS-a`: lo que exige navegador es de mesa. Receta en `§6`.

---

## §5 · Tabla de identificación (`P0 (iii)`), escrita antes de abrir resultados

Generada por `python3 tools/mide_participacion_tipo_boleta.py --tabla-identificacion`
sobre `data/p0-calendario-ayuntamientos-v1_0.tsv`, salida en
`data/l3-tabla-identificacion-v1_0.tsv` (**73 transiciones, 32 entidades**).
`D_pres = 1` para 2018 y 2024; `D_int = 1` para 2015 y 2021; Chiapas 2015 entra
como **no concurrente** por la excepción que el calendario ya documenta.

**Conteo por parámetro identificado, en el universo entero:**

| identifica | transiciones |
|---|---:|
| `alpha` (STAY: mismo tipo en las dos patas) | **5** |
| `beta_pres` (+`alpha`) | 9 |
| `beta_int` (+`alpha`) | 5 |
| `beta_pres − beta_int` (+`alpha`) | **54** |
| **total** | **73** |

**Las 5 STAY del universo entero**, nombradas:

| entidad | transición | hueco | estatus |
|---|---|---:|---|
| Aguascalientes | 2016 → 2019 | 3 | TRATADO `g2021` |
| **Baja California** | **2016 → 2019** | **3** | TRATADO `g2021` |
| Durango | 2016 → 2019 | 3 | NUNCA-TRATADO |
| Durango | 2019 → 2022 | 3 | NUNCA-TRATADO |
| Hidalgo | 2016 → 2020 | 4 | TRATADO `g2024` |

**Lo que esto dice del diseño, antes de medir nada:**

1. La corrección `c1` **rescata 54 transiciones que `L6` estaba usando como
   controles puros**. Las entidades siempre concurrentes hacen
   `presidencial → intermedia → presidencial`: bajo `ΔD = 0` de `L6` eran
   «tratamiento fijo, no informan»; bajo `ΔD_pres`/`ΔD_int` **identifican
   `β_pres − β_int`**. Esa es, medida, la razón mecánica por la que la `γ` de
   `L6` estaba contaminada — lo que `L6 §11` anticipó y no pudo cuantificar.
2. **`α` es ahora el parámetro frágil**, no `β`. El panel de `L6` contiene **una
   sola** STAY (Durango 2016→2019, y en un solo municipio). El encargo fija el
   umbral: **menos de 3 STAY ⇒ `α` se identifica con reserva y se reporta también
   la variante sin `α`**. Se declara **antes de `P1`** que ese umbral se cumplirá
   o no según qué entidades entren, y que la variante sin `α` se reporta pase lo
   que pase.
3. Por lo tanto la prioridad de adquisición que **maximiza identificación** no es
   la del volumen sino la de las STAY: **Baja California** (STAY 2016→2019 **y**
   la serie completa con lista nominal) y **Aguascalientes** (STAY 2016→2019).
   El orden obligatorio del encargo se respeta; esta nota deja dicho por qué,
   dentro de él, Baja California es la adquisición de mayor rendimiento.

---

## §6 · Recetas manuales (entregable, no consuelo)

**Hidalgo 2016 — extraer el `.rar`.** El archivo ya está en el corpus:
`/home/pc0/mm-corpus/raw/electoral_local_municipal_serie/ieeh_hidalgo_2016_ayuntamientos.rar`
(444 642 B, RAR v4). En Windows: clic derecho → **7-Zip → Extraer aquí**;
comprimir el resultado como `ieeh_hidalgo_2016_ayuntamientos.zip` y dejarlo en
la misma carpeta. Origen, si se prefiere volver a bajarlo:
`https://www.ieehidalgo.org.mx/images/Procesos/Proceso%202015-2016/Ayuntamientos/AyuntamientosC.rar`
(≤ 1 min).

**Hidalgo — denominador (las tres patas).** Ninguna fuente programable lo tiene.
La que sí lo tiene es el **SICEEN/SICEEF del INE**, que la firma `DS-a` asigna a
mesa por navegador, y que este acto **no sondeó** por `ADR-288`.

**Veracruz — cómputos municipales 2017 y 2021.** `www.oplever.org.mx` exige
resolver el reto de Cloudflare, que sólo un navegador real pasa. Abrir
`https://www.oplever.org.mx/` en el navegador, ir a *Resultados electorales* →
proceso 2016-2017 y 2020-2021, y descargar los cómputos de ayuntamientos por
casilla (≤ 1 min una vez pasado el reto).

---

## §7 · Lo que `P0` deja fijado

* **11 de 12** entidades faltantes son alcanzables por programa; **1** (Veracruz)
  no lo es y va con receta.
* **2 entidades quedan con ruta completa confirmada y verificada por
  inspección**: **Baja California** (4 patas con lista nominal en la fuente) y
  **Zacatecas 2016** (la pata que faltaba, con lista nominal por municipio).
* **Hidalgo** —el caso que el encargo ordenó primero— queda
  `OBTENIDO-SIN-DENOMINADOR` en sus **tres** patas, con las **cuatro** rutas de
  denominador probadas y descartadas una por una, incluida la del PREP federal,
  que se descarta **por una cifra que el propio archivo declara** (95.2352 % de
  actas) y no por preferencia.
* **7 entidades** quedan `PENDIENTE-DE-INTENTO` para `P1`.
* La tabla de identificación queda escrita y versionada **antes** de que exista
  un solo resultado, y ya dice cuál es el parámetro frágil: **`α`, no `β`**.

**Tope de tiempo de `P1`, declarado aquí:** la adquisición cierra a las **19:15
CST del 2/sep/2026** (4 h desde el ARRANQUE) o antes si se agotan las rutas. Al
tope se cierra con lo obtenido y se pasa a `P2`; la cobertura que quede es la que
se declara.
