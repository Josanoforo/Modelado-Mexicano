# ACTO ENSAFI-DESCRIPTOR · el descriptor de ENSAFI 2023 existe, la extensión era el obstáculo

`ENCARGO ENSAFI-DESCRIPTOR — una descarga quirúrgica (el descriptor/FD de ENSAFI 2023) y el
re-censo C1 que FP-157 está esperando`, dirección, 25/ago/2026, SHA de redacción `dad74ee`.
Worktree `/home/pc0/mm-ensafi-descriptor`, rama `acto/ensafi-descriptor`.
**Entorno UBUNTU** (descarga + apertura de corpus). Sin doble, sin firma.

**La sesión cruzó la medianoche.** Los dos payloads se bajaron el **25/ago/2026 a las 21:27**
hora local (`fecha_descarga: '2026-08-25'` en `data/manifiesto.yaml`, consistente con el `mtime`
de los archivos); el resto del acto se escribió el **26/ago**. Ambas fechas son reales y se
declaran en vez de colapsarse a una.

---

## 0 · Arranque y firma de entorno (`A.2`, tres partes)

**1 · REPO.** Worktree nuevo creado sobre `dad74ee`. El clon principal
(`/home/pc0/Modelado-Mexicano`) estaba parado en `acto/cal-g3-puntual`, no en `main` — la caja del
acto es propia, y `F0` se corrió dentro de ella.

**2 · SHA.** `git fetch origin` → `e3bbaab..dad74ee main`. `origin/main` **es exactamente**
`dad74ee`; `git rev-list --count dad74ee..origin/main` → **0**. `main` no avanzó ni un commit desde
la redacción: no hay refresco que reportar.

**3 · Corpus.** `data/raw` **no existía** en el worktree nuevo (gitignorado, no se hereda). Se
enlazó a la raíz compartida y se copió el archivo de raíces:

```
$ ln -s /home/pc0/mm-corpus/raw data/raw
$ cp /home/pc0/mm-r34-ensafi-censa/data/raices.local.yaml data/raices.local.yaml
$ readlink -f data/raw
/home/pc0/mm-corpus/raw
$ git status --short          # vacío -- el symlink no ensucia el árbol
```

**4 · Firma de entorno, las tres partes:**

```
(1) CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: sin_variable
(2) $ curl -sS -o … -w 'http_code=%{http_code} size=%{size_download} …' https://www.inegi.org.mx/
    http_code=200 size=153606 time=0.695497 ctype=text/html
(3) $ ls data/raw/ | head -3
    2005trim1_csv.zip
    2008trim1_csv.zip
    2012trim1_csv.zip
    entradas: 321        (9.6 G)
```

Corpus montado, sin `PARO`. Sonda **cruda** (`GET` con cuerpo descartado), nunca `curl -I`.

**5 · `grep`.** Verificado con `type grep`: es una **función** que envuelve `ugrep -I`. Todo negativo
de esta nota se corrió con `command grep` y lleva control positivo al lado (`A.13`).

---

## 1 · `F0` · Existencia (`A.8`), contra `dad74ee`

```
$ command grep -n -i "ensafi" data/manifiesto.yaml
3939:- id: ensafi2023_bd_csv_zip
3940:  usado_para: 'Encargo B-3 (mesa #20): cierre del barrido de alcanzabilidad -- ENSAFI 2023
3942:    haberse sondeado. Portal INEGI resuelto esta sesion via /programas/ensafi/ (stub JS a
3945:    (portal /programas/ensafi/2023/ es SPA sin listado estatico, WebFetch solo recupera <title>;
3949:  url_origen: https://www.inegi.org.mx/contenidos/programas/ensafi/2023/microdatos/ensafi_2023_bd_csv.zip
3951:  descargado_por: 'agente, directamente de inegi.org.mx (portal /programas/ensafi/ -> stub
3954:  archivo: ensafi2023/ensafi_2023_bd_csv.zip
3957:  formato: CSV (comprimido en ZIP) -- Base de datos ENSAFI 2023. No se abrio ni extrajo.
$ command grep -c -i "ensafi" data/manifiesto.yaml
8
```

**Un solo `id` de `ENSAFI`, y es la base de datos.** Ningún `id` de `FD` ni de cuestionario. La
premisa del encargo se confirma: el descriptor **no** estaba registrado al arrancar, y `F2` no se
salta. El corpus tampoco lo tenía: `ls data/raw/ensafi2023/` traía **un** archivo,
`ensafi_2023_bd_csv.zip`.

---

## 2 · `F1` · La descarga — y el hallazgo que reabre cuatro actos

### 2.1 · El FD por el patrón vivo, con control positivo y control negativo

La URL candidata **no se tecleó del encargo**: se derivó del patrón que el propio `manifiesto.yaml`
tiene vivo para `ENASIC`/`ENFIH`
(`contenidos/programas/{acr}/{año}/microdatos/{acr}_{año}_fd.xlsx`, líneas 3927 y 4034). Las cuatro
sondas de la misma pasada:

| URL | `http` | bytes | `content-type` | primeros 8 bytes |
|---|---:|---:|---|---|
| `…/ensafi/2023/microdatos/ensafi_2023_fd.xlsx` | 200 | **2 263** | `text/html` | `3c21444f43545950` (`<!DOCTYP`) |
| `…/enasic/2022/microdatos/enasic_2022_fd.xlsx` *(control +)* | 200 | **266 488** | `…spreadsheetml.sheet` | `504b030414000600` (`PK`) |
| `…/enfih/2019/microdatos/enfih_2019_fd.xlsx` *(control +)* | 200 | **202 396** | `…spreadsheetml.sheet` | `504b030414000600` (`PK`) |
| `…/ensafi/2023/microdatos/URL_INVENTADA_CONTROL_NEGATIVO.xlsx` *(control −)* | 200 | **2 263** | `text/html` | `3c21444f43545950` |

El patrón **está vivo** (los dos controles positivos devuelven el `XLSX` real, con los bytes exactos
que el manifiesto ya registraba: 266 488 y 202 396). La candidata de `ENSAFI` es **byte a byte
idéntica en tamaño y tipo al control negativo inventado**: soft-404, la firma de 2 263 B que
`ADR-194` fijó. Confirmado por cuarta vez, ahora con control negativo emparejado en la misma
pasada.

### 2.2 · El hallazgo: la API declara `_xlsx.zip`, no `.xlsx`

En vez de adivinar más variantes, se fue al catálogo que el propio portal usa. Los parámetros **no
se inventaron**: se leyeron del JS vivo.

```
$ curl -sS https://www.inegi.org.mx/programas/ensafi/2023/data/pestana/pestanadata.js
   … "titulo": "Microdatos", … "data-id": "3364", "data-tipoinformacion": "4" …

$ curl -sS https://www.inegi.org.mx/componentes/descargaMasiva/js/descargaMasivaV2.min.js \
    | command grep -oE "archivoscompaginacion[^\"']{0,300}"
archivoscompaginacion?tema=…&subtema=…&areaGeografica=…&proyecto=…&anio=…&tipodocto=…
  &agrupacion=b64EncodeUnicode("Todas")&idBiinegi=…&desde=1&hasta=1000&textoBuscar=…
  &ordenar=…&ingles=0&datosAbiertos=0&orden=…
```

*(Precedente corregido, para el sucesor: la nota de `ENUT` del 31/jul concluyó que «el parámetro es
`tipoinformacion`, no `tipodocto`». Las dos cosas son ciertas y no se contradicen —
`data-tipoinformacion` es el **atributo del `div`**, `tipodocto` es el **nombre del parámetro de
query** al que ese valor se asigna. Llamar al endpoint con `tipoinformacion=4` devuelve `204 No
Content`; con `tipodocto=4` y el juego completo de nueve parámetros, devuelve la lista. Se verificó
en las dos formas.)*

Con el juego completo:

```
$ curl -sS ".../archivoscompaginacion?tema=0&subtema=0&areaGeografica=0&proyecto=0&anio=0
    &tipodocto=4&agrupacion=VG9kYXM=&idBiinegi=3364&desde=1&hasta=1000&textoBuscar=
    &ordenar=orden&ingles=0&datosAbiertos=0&orden=asc"
http=200 bytes=801   n=2
   Base de datos                | _csv.zip&4.79 MB  | /programas/ensafi/2023/microdatos/ensafi_2023_bd
   Descriptor de archivos (FD)  | _xlsx.zip&1.09 MB | /programas/ensafi/2023/microdatos/ensafi_2023_fd
```

**El `formato` que el catálogo declara es `_xlsx.zip`, no `.xlsx`.** La URL real se construye
`https://www.inegi.org.mx/contenidos` + `pathLogico` + `formato`, la misma regla que la nota de
`ENUT` ya había establecido:

> `https://www.inegi.org.mx/contenidos/programas/ensafi/2023/microdatos/ensafi_2023_fd_xlsx.zip`

**Este es el hallazgo del acto.** Cuatro actos previos —`B-3` (4/ago), el lote de reactivos del 5/ago (`forense/notas/2026-08-05-m3-lote-b3-diez-reactivos.md`), `M-ADQ`
(12/ago), `R34-ENSAFI-CENSA` (25/ago)— sondearon `ensafi_2023_fd.xlsx` y recibieron el soft-404, y
los cuatro concluyeron, correctamente sobre lo que probaron, que el FD «no está publicado bajo el
patrón declarado». **La conclusión era correcta sobre la URL probada y falsa sobre el hecho:** el
patrón vivo de `ENASIC`/`ENFIH` es `.xlsx` a secas, y `ENSAFI` publica el suyo **comprimido**. El
mismo manifiesto ya tenía un precedente de esa forma —`enif2021_fd_zip`,
`enif_2021_fd_pdf.zip`— que nadie cruzó contra `ENSAFI`. **No era «la fuente no lo publica»; era
«probamos una extensión de dos».**

### 2.3 · Sonda antes de bajar (`A.6`), con control negativo de la misma forma

```
$ curl -sS -r 0-0 -D - -o /dev/null .../ensafi_2023_fd_xlsx.zip
HTTP/1.1 206 Partial Content
Content-Type: application/x-zip-compressed
Last-Modified: Fri, 26 Jul 2024 22:00:01 GMT
Content-Range: bytes 0-0/1108577

$ curl -sS -r 0-0 -o /dev/null -w 'http=%{http_code} bytes=%{size_download}\n' \
    .../ensafi_2023_INVENTADO_xlsx.zip
http=200 bytes=2263          # control negativo con la MISMA forma -> soft-404
```

**206 real contra 200-soft-404 inventado, en la misma forma de URL.** No es un artefacto del patrón.

### 2.4 · Lo bajado, y dónde quedó

El **cuestionario** también se bajó. Su URL **no se derivó por analogía**: la declara el propio
servidor en `/programas/ensafi/2023/data/arbol/arbolData.js`, nodo `"Cuestionario"`,
`"url": "/contenidos/programas/ensafi/2023/doc/ensafi_2023_cuestionario.pdf"`, `"tamnio": " 1.13 MB"`.
Es la pieza que `ADR-194` §5 localizó y dejó sin bajar por perímetro.

| pieza | `http` | bytes | tipo | destino |
|---|---:|---:|---|---|
| `ensafi_2023_fd_xlsx.zip` | 200 | 1 108 577 | `application/x-zip-compressed` | `mm-corpus/raw/ensafi2023/` |
| `ensafi_2023_cuestionario.pdf` | 200 | 1 182 405 | `application/pdf` | `mm-corpus/raw/ensafi2023/` |

Los bytes bajados coinciden con la sonda (`0-0/1108577`) y con lo que `ADR-194` midió sin bajar
(1 182 405). Ambos registrados con `tests/manifiesto.py --registra` — `sha256` y tamaño **derivados
del archivo**, nunca tecleados.

**⚠️ Verificación de destino exigida por el encargo (defecto `PR #77`).** Los dos payloads están en
el **corpus compartido**, no en el worktree:

```
$ ls -la /home/pc0/mm-corpus/raw/ensafi2023/
-rw-r--r-- 5027338 Aug  4 21:37 ensafi_2023_bd_csv.zip
-rw-r--r-- 1182405 Aug 25 21:27 ensafi_2023_cuestionario.pdf
-rw-r--r-- 1108577 Aug 25 21:27 ensafi_2023_fd_xlsx.zip
```

**Verificación `A.1`, una invocación por `--id`, salida cruda:**

```
$ python3 tests/manifiesto.py --verifica --id ensafi2023_fd_xlsx_zip
ensafi2023_fd_xlsx_zip [data_raw]: COINCIDE -- sha256 y tamaño (1108577 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id ensafi2023_cuestionario_pdf
ensafi2023_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1182405 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id ensafi2023_bd_csv_zip
ensafi2023_bd_csv_zip [data_raw]: COINCIDE -- sha256 y tamaño (5027338 bytes) verificados contra data/manifiesto.yaml
```

**3/3 `COINCIDE`.** Ninguna de las tres respuestas que no se colapsan —`AUSENTE`,
`raíz-no-configurada`, `hash-discordante`— se disparó.

**Cero fallos de descarga.** No hay ninguna pieza que declarar `NO OBTENIDO`, y por tanto ninguna
receta manual que escribir: las dos piezas del perímetro se obtuvieron por agente al primer intento
tras derivar el patrón correcto. *(La receta que sí queda registrada, y que es el entregable
transferible, es la de §2.2: **ante un soft-404 de INEGI, consultar `archivoscompaginacion` y usar
el `formato` que declara, en vez de asumir la extensión del patrón hermano**.)*

---

## 3 · `F2` · El re-censo, sobre el descriptor

### 3.1 · Lo que el FD resultó ser

El ZIP trae **dos** archivos, no uno: `ensafi_2023_fd.pdf` (1 043 071 B) y `ensafi_2023_fd.xlsx`
(109 082 B). El libro tiene **4 hojas** — `TVIVIENDA`, `THOGAR`, `TSDEM`, `TMODULO` — una por tabla
del microdato, con seis columnas por reactivo declaradas por el propio archivo:

> `[1]` Pregunta *(«Corresponde a la pregunta textual del instrumento de captación»)* · `[2]`
> Nemónico · `[3]` Tipo · `[4]` Tamaño · `[5]` Códigos válidos · `[6]` Concepto

Es decir: **el puente código↔texto de pregunta que faltaba**, más el universo (por `SECCIÓN` y por
`FILTRO`) y el formato de respuesta completo.

### 3.2 · Control de integridad — el descriptor cubre el microdato sin hueco

Antes de censar, se verificó que el descriptor **no deja columnas fuera**, cruzando sus nemónicos
contra las cabeceras reales del `ensafi_2023_bd_csv.zip` que ya estaba en corpus:

| tabla | cabeceras en la BD | reactivos en el FD | sólo-BD | sólo-FD |
|---|---:|---:|---|---|
| `TVIVIENDA` | 36 | 36 | — | — |
| `THOGAR` | 55 | 55 | — | — |
| `TSDEM` | 25 | 25 | — | — |
| `TMODULO` | 253 | 253 | — | — |
| **TOTAL** | **369** | **369** | **0** | **0** |

*(La única diferencia aparente es el `BOM`+comillas de la primera columna de cada `.csv`
—`Ï»¿"LLAVEVIV"` frente a `LLAVEVIV`— artefacto de codificación, no columna faltante.)*

**Correspondencia 1:1 exacta.** Las **369** cabeceras que `ADR-194` leyó a ciegas son las mismas
369, y ahora **las 369 tienen texto**. Los «354 códigos `P`-numerados no buscables por término» de
`ADR-194` dejan de existir como categoría.

### 3.3 · Universo declarado del censo (`A.4`)

10 secciones, 369 reactivos, todos con pregunta verbatim:

| tabla | sección | reactivos |
|---|---|---:|
| `TVIVIENDA` | llave · S1 Características de la vivienda · S2 Identificación de los hogares | 1 · 23 · 12 |
| `THOGAR` | llaves · S4 Características socioeconómicas del hogar | 2 · 53 |
| `TSDEM` | llaves · S3 Características sociodemográficas de las personas | 3 · 22 |
| `TMODULO` | llaves · S5 Características personales y laborales · S6 Deuda, ahorro y gasto individual · S7 Conductas financieras y factores psicológicos · S8 Estrés financiero · S9 Metas financieras · S10 Conocimientos sobre CONDUSEF y temas de interés *(incluye las 27 derivadas y de diseño)* | 3 · 54 · 52 · 58 · 41 · 9 · 36 |

**Superficie buscada por reactivo:** pregunta verbatim `+` nemónico `+` **el concepto de cada
opción de respuesta** (columna `[6]`), normalizada sin acentos a mayúsculas. Es decir, se buscó
también dentro de las opciones, no sólo en el enunciado.

### 3.4 · Control positivo del extractor

Los mismos 12 términos financieros de `ADR-194`: **12 de 12 con coincidencia** (contra 11/12 sobre
cabeceras) — `AHORR` 35 · `CREDIT` 28 · `INGRES` 33 · `SALARI` 5 · `DEUD` 26 · `ESTRES` 1 ·
`BIENES` 5 · `OPTIM` 1 · `IMPULS` 1 · `CONTROL` 2 · `ORIEN` 2 · `DEPEN` 8. **El que faltaba,
`CREDIT`, ahora acierta**: el descriptor lee estrictamente más que la cabecera. El extractor lee.

### 3.5 · `C1` — la tabla término·hit·pregunta-verbatim

Los 16 términos de `ADR-194`, uno por uno, sobre los 369 reactivos:

| # | término | reactivos con coincidencia | pregunta verbatim del hit | juicio |
|---:|---|---:|---|---|
| 1 | `SAT` | 2 | `P1_4_09`: «1.4 ¿En esta vivienda tienen servicio de televisión de paga (cable o satelital)?…» | **falso positivo** — subcadena de `SATELITAL` (`P1_4_09`, TV de paga) y de `SATISFACTORIO` (`P7_11_3`). El `SAT` como institución no aparece. |
| 2 | `FISC` | **0** | — | sin coincidencia |
| 3 | `IMPUEST` | **0** | — | sin coincidencia |
| 4 | `HACIEND` | 3 | `P3_10`: «3.10 Aunque ya me dijo que (NOMBRE) (CONDICIÓN DE 3.9), ¿la semana pasada...…» | **falso positivo** — gerundio `HACIENDO` (`P5_15` gestiones de negocio; `P3_10`/`P5_16` «aprendiz o haciendo su servicio social»). La *Secretaría de Hacienda* no aparece. |
| 5 | `VIGIL` | **0** | — | sin coincidencia |
| 6 | `RASTRE` | **0** | — | sin coincidencia |
| 7 | `EVAS` | **0** | — | sin coincidencia |
| 8 | `DECLAR` | **0** | — | sin coincidencia |
| 9 | `AUTORID` | **0** | — | sin coincidencia |
| 10 | `GOBIER` | 9 | `P1_7`: «1.7 ¿La persona dueña o propietaria de esta vivienda...…» | **falso positivo por sentido** — 9 reactivos, los 9 sobre **recibir** apoyos/subsidios/programas del gobierno (`P1_7`, `P1_8_4`, `P4_1_1`, `P5_11`, `P5_23_5`, `P5_23_8`, `P6_2_03`, `P8_6_04`, `P9_3_1`). El gobierno aparece como **fuente de transferencia**, nunca como observador, fiscalizador ni riesgo. |
| 11 | `PRIVAC` | **0** | — | sin coincidencia |
| 12 | `INFORMAL` | **0** | — | sin coincidencia |
| 13 | `FORMALIZ` | **0** | — | sin coincidencia |
| 14 | `REVIS` | 3 | `P3_6_3`: «3.6 ¿En qué día y mes nació (NOMBRE)?…» | **falso positivo** — subcadena de `IMPREVISTO` (`P7_8_1`, `P8_1_5`) y de `ENTREVISTA` (`P3_6_3`). |
| 15 | `AUDIT` | 1 | `P5_2_2`: «5.2 (ENTREGUE LA TARJETA 2) En su vida diaria, ¿usted cuánta dificultad tiene para oír, aun usando aparato aud…» | **falso positivo** — subcadena de `AUDITIVO` (`P5_2_2`, dificultad para oír). |
| 16 | `DATO` | **0** | — | sin coincidencia |

**5 de 16 términos coincidieron; los 5 son falsos positivos.** Cuatro por subcadena (`SATELITAL`,
`SATISFACTORIO`, `HACIENDO`, `IMPREVISTO`, `ENTREVISTA`, `AUDITIVO`) y uno por sentido (`GOBIERNO`,
9 reactivos, los 9 sobre **recibir** dinero del gobierno). **Reactivos genuinos de percepción de
riesgo fiscal o de vigilancia: 0 de 369.**

### 3.6 · Barrido ampliado de `C1` — 27 términos más allá de los 16

Para que el negativo no dependa de la lista de `ADR-194`, se corrió un segundo barrido con
vocabulario fiscal y de vigilancia que aquella no incluía:

```
RFC 0 · CONTRIBU 0 · RECAUD 0 · FACTUR 0 · COMPROBANTE 0 · DECLARACION 0 · TESORER 0 · ISR 0
· TRIBUT 0 · SUPERVIS 0 · MONITORE 0 · REPORTA 0 · DETECT 0 · "CONTROL DEL GOB" 0 · LAVAD 1
· ILICIT 0 · BLANQUE 0 · REGIMEN 0 · CONTABIL 0 · NOMINA 2 · CFDI 0 · SANCION 0 · MULTA 0
· CASTIG 0 · PERSEGU 0 · INSPECCION 0 · IVA 6
```

Los tres no-cero son falsos positivos por subcadena: `LAVAD` → `P1_4_02` («¿tienen **lavadora**?»);
`NOMINA` → `P6_2_01`/`P6_6_3`, cuenta y crédito **de nómina** (producto financiero, no obligación
fiscal); `IVA` → `PRIVADA`, `ACTIVIDAD` y similares. **43 términos, 0 reactivos genuinos.**

### 3.7 · Contraste independiente contra el cuestionario

Los mismos 16 términos sobre el texto completo del `PDF` del cuestionario
(`pdftotext -layout`, 195 679 caracteres normalizados) — **un artefacto distinto, extraído por una
herramienta distinta**. Control positivo: 12/12. Tres términos coinciden ahí y no en el FD, y los
tres se abrieron verbatim:

| término | contexto verbatim | juicio |
|---|---|---|
| `AUTORID` (1) | «*…los datos e informes que les soliciten las **autoridades** competentes para fines estadísticos, censales y geográficos… serán estrictamente confidenciales…*» | **portada legal `LSNIEG`**, no un reactivo |
| `PRIVAC` (1) | «**PRIVACIÓN** ECONÓMICA» — encabezado del bloque `4.10` | *privación*, no *privacidad* |
| `INFORMAL` (4) | «AHORRO **INFORMAL** Y FORMAL», «CRÉDITO **INFORMAL** Y CRÉDITO FORMAL» | **canal** de ahorro/crédito (tanda, casa de empeño), no formalidad fiscal ni laboral |

**El cuestionario confirma el FD.** Los dos artefactos, leídos por dos vías, dan el mismo cero.

### 3.8 · Veredicto `A.4` real, por constructo

> **`C1` · Percepción de riesgo fiscal / `SAT` / vigilancia al usar pagos o servicios digitales →
> `NO-ENCONTRADO`.**

Ya **no** `NO-ACCESIBLE`. La distinción es exactamente la que `ADR-194` dejó pendiente: entonces
era «no pude alcanzar la fuente», ahora es «**la fuente no tiene el dato**». Universo del negativo:
369 de 369 reactivos con texto verbatim (correspondencia 1:1 verificada contra el microdato),
43 términos, dos artefactos independientes (`XLSX` y `PDF`), control positivo 12/12.

Los otros tres constructos, censados en la misma pasada y ahora también con texto:

| # | constructo | términos | hallazgo sobre los 369 reactivos | veredicto `A.4` |
|---|---|---:|---|---|
| **C1** | Riesgo fiscal / vigilancia al usar pagos digitales | 16 (+27) | **0 genuinos** — los 5 hits son subcadena o «recibir apoyo del gobierno» | **`NO-ENCONTRADO`** |
| **C2** | Razones de no-uso de pagos/servicios digitales (¿`CoDi`?) | 15 | **`CoDi` no aparece; `SPEI` = 0.** Los 3 hits de `CODI` son la palabra `CÓDIGO` en instrucciones de filtro (`FILTRO_S5_3_1`, `FILTRO_S6_1`, `FILTRO_S6_2`). Sí existe **tenencia** digital (`P7_2_4` app de gasto, `P6_2_08` cuenta *fintech* «Mercado Pago o Albo», `P6_6_8` crédito en línea), pero la **única** batería de razones del instrumento es `7.5` y es sobre **llevar registro de ingresos y gastos**, no sobre medios de pago | **`NO-ENCONTRADO`** para el constructo; **`EXISTE-NO-SATISFACE`** si se lee sólo «uso digital» |
| **C3** | Fricción declarada (dificultad, requisitos, fallas) | 11 | **0 genuinos.** `DIFIC` (12) → discapacidad (`P5_2_1/2`), procrastinación (`P7_10_07`), dificultad de **ahorrar** (`P8_1_6`) y de cumplir una meta (`P9_2`); `TRAMIT` (3) → búsqueda de empleo; `COMISION` (1) → el nombre de la **CONDUSEF**; `ESPERA` (2) → `INESPERADOS`. Ninguna fricción **de servicio financiero o digital** | **`NO-ENCONTRADO`** |
| **C4** | Confianza: canal personal vs. institucional | 9 | **`EXISTE-NO-SATISFACE`, ahora por contenido y no sólo por forma.** La batería `7.9` (`P7_9_1/2/3`, Tarjeta 6, escala `[1-4]`) mide **autoeficacia** —«¿qué tanto confía en **su habilidad** para…?»—, no confianza en un canal. `CONF_FINAN` resulta ser una **derivada** (hoja `TMODULO`, bloque de variables construidas junto a `NIV_ESTRES`/`OPTIMISMO`), lo que **confirma** el descarte por forma de `ADR-194` y le añade la causa. **Y aparece lo que `ADR-194` no podía ver:** `8.6` (Tarjeta 8) **sí** contrasta canal personal e institucional **ítem por ítem, misma batería, mismos individuos, respuesta múltiple** — `P8_6_01` «Pedir un préstamo a **familiares o amistades**» frente a `P8_6_02` «Solicitar un crédito en un **banco o institución financiera**» (`0`=No se mencionó, `1`=Sí se mencionó); e igual `6.1`/`6.5` separan tanda/familiares/caja de ahorro frente a banco. Pero **las tres son de recurso o tenencia, no de confianza**: miden a quién acudiría o con quién tiene el producto, no cuánto confía en cada canal | **`EXISTE-NO-SATISFACE`** |

### 3.9 · No hay spec-candidata, y por qué eso es una respuesta y no un vacío

La rama `EXISTE-SATISFACE` de `F2` —pegar la pregunta verbatim, el código `P`, el universo del
módulo y el formato de respuesta como spec-candidata del medidor de `B`— **no aplica**: ningún
constructo la alcanzó. Lo que se entrega en su lugar es lo que el encargo nombra como el otro
desenlace: **el censo de la condición `B` queda exhaustivo**.

`ENSAFI 2023` era la **última** fuente del censo de `#359` que no estaba abierta hasta el fondo.
Con este acto, las siete candidatas —`ENIF`, `ENDUTIH`, `IFT SFD`, `ENCIG`, `ECF`, `ENAFIN` y
`ENSAFI`— están todas abiertas a nivel de reactivo con texto verbatim, y las siete dan cero para
`riesgo_fiscal_percibido`. **`FP-157` ya no se decide sobre terreno incompleto.**

Y `ENSAFI` falla por partida doble, lo que cierra la puerta sin ambigüedad: no sólo carece de la
**exposición** de `B` (`riesgo_fiscal_percibido`), también carece de su **desenlace** — `CoDi` no
aparece ni una vez en los 369 reactivos ni en las 195 679 caracteres del cuestionario. Ni siquiera
con la variable fiscal prestada de otra encuesta serviría.

---

## 4 · `F3` · Lo que se escribe, y lo que no

**Contador de medición sobre México: cero, declarado.** Este acto no mide nada del motor, no toca
`Hito D` (`18 de 27`, sin cambio), ni coeficientes (`0/15`, sin cambio), ni `milpa/`, ni el
pre-registro. Le da a mesa el terreno; el gate lo mueve su firma.

**Lo que este acto NO hace, verbatim del perímetro.** No mide `B` (eso es el medidor, acto aparte).
**No adjudica `FP-157`.** No toca `tests/aceptacion_r3_4.py` (verificado: sin cambios en el `diff`).
No baja nada más que el descriptor y el cuestionario de `ENSAFI 2023`. No reclasifica `CONF_FINAN`
para la necesidad 14 de `ABRIR-4`. No mueve `data/diseno-muestral.yaml` — `ENSAFI` sigue
`PENDIENTE` ahí, y **ahora hay con qué sacarla**, pero eso es otro acto.

**Una deuda que este acto abre y no cierra, declarada.** El FD recién bajado trae el diseño muestral
a nivel de variable (`FAC_ELE`, `UPM_DIS`, `EST_DIS`, presentes en `TMODULO`). `FP-95` /
`ADR-135(f)` censan parámetros de diseño de fuentes `PENDIENTE` con payload material: `ENSAFI` era
`PENDIENTE` **por falta de descriptor**, y esa causa acaba de desaparecer. Se nombra aquí para que
el sucesor no lo redescubra; no se ejecuta, está fuera de la lista cerrada.

**Corrida de arranque de la suite:** `19 FAIL · 131 WARN`, `LÍNEA BASE: VERDE`. Corrida final: en
§5.

**Reserva honesta sobre el alcance del negativo.** Este censo es exhaustivo sobre el **instrumento
publicado**: los 369 reactivos y el cuestionario. No cubre lo que `ENSAFI` pudiera tener en
tabulados o en datos abiertos que no correspondan a una columna del microdato — pero por
construcción esas son agregaciones de las mismas 369 columnas, no reactivos nuevos. Y no cubre
ediciones futuras de `ENSAFI`: el veredicto es sobre **2023**, la única levantada.

---

## 5 · Suite y cascada

**Corrida de arranque:** `19 FAIL · 131 WARN`, `LÍNEA BASE: VERDE`.
**Corrida final:** `19 FAIL · 131 WARN`, `LÍNEA BASE: VERDE` contra `tests/baseline.json`
(`HEAD` congelado `e24d033`). **Nunca `--freeze`.**

> **Corrección de este mismo párrafo, escrita al resolver el CI (§6).** La corrida que dio esa
> cifra se lanzó **antes** de que se apendara la tabla de abajo, y esa tabla reintrodujo el
> `T25` que narra —el defecto exacto que la fila `T25` describe: *mencionar el rótulo es
> usarlo*—. El commit `3235410` entró, por tanto, con **20 `FAIL`**, no 19, y la cifra
> declarada arriba no correspondía al árbol commiteado. Detectado al re-correr la suite en el
> commit del CI, corregido ahí (la fila ya no transcribe el rótulo) y re-medido sobre el árbol
> real: **`19 FAIL · 131 WARN`, `LÍNEA BASE: VERDE`**. Se declara en vez de reescribirse en
> silencio: una cifra de suite en un forense es una afirmación verificable, y ésta estuvo mal
> un commit.

**Los `FAIL` no se movieron ni un punto en todo el acto.** Los que este acto llegó a introducir se
atraparon y cerraron dentro de él — **6 entradas nuevas en la corrida intermedia, las 6
autoinfligidas y las 6 cerradas**:

| test | causa | cierre |
|---|---|---|
| `T15` ×2 | la cabecera de `gobernanza` y la fila de registro de `estado` seguían citando `197 ADR` tras el recifrado a `198` | actualizadas a `198` |
| `T15` ×1 | la línea de cascada de `ADR-197` dice `**196 → 197 ADR**`, cifra **correcta cuando se escribió** y ahora vencida | se le añade `{cita-historica}` **dentro** de las negritas, inmediatamente tras `ADR` (`T15` exime *sólo* la cita inmediatamente anterior a la marca). No se edita hacia atrás la sustancia de un acto ajeno: se marca como historia, que es lo que es |
| `T25` ×2 | la ficha y esta nota traían el rótulo pelado del acto del 5/ago (el que `T25` vigila; no se transcribe aquí — **escribirlo vuelve a crear el defecto**) | sustituido por su nota (`forense/notas/2026-08-05-m3-lote-b3-diez-reactivos.md`), que no es rótulo pelado. **No** se tocó `tests/check.py` ni `_T25_ARCHIVOS_CONOCIDOS`: está fuera de la lista cerrada del perímetro, y la vía dentro del perímetro existía |
| `T16` ×2 | consecuencia mecánica de los `FAIL` de arriba: `canon` declaraba `19 FAIL · 131 WARN` vigente y la corrida real daba otra cifra | desapareció al cerrar las causas; la cifra declarada vuelve a ser la real |

**Cascada de numeración.** `ADR-198`, contra el máximo re-derivado **por conteo entero** —
`re.findall(r'ADR-(\d+)')` → `197`, sin huecos. **No** con `sort -t- -k2 -n`, que parte en el primer
guion y devuelve un máximo falso. `gh pr list --state open` al arrancar → **vacío**, y así queda
registrado — ver §6, donde se declara la colisión viva que apareció después. Recifrado `197 → 198` propagado a la cabecera de
`gobernanza`, a `estado §L0` y a la fila de registro de artefactos de `estado`.

**Perímetro, verificado por `git diff --name-only` al cerrar** — nada fuera de la lista cerrada, y
`tests/aceptacion_r3_4.py` ausente del `diff`.

---

## 6 · Adenda de cierre — el CI y una colisión que apareció después

Escrita al resolver el CI de `PR #370`, después de §5. No modifica nada de lo anterior.

### 6.1 · El `startup_failure` no fue de esta rama

El primer run del workflow (`32985370802`, `2026-08-26T15:31:15Z`) murió en **`startup_failure`, 0
segundos** — sin ejecutar una línea. GitHub imprime *«This run likely failed because of a workflow
file issue»*, y eso es texto genérico, no diagnóstico. **Verificado que es falso para esta rama:**

```
$ git diff origin/main HEAD -- .github/ --stat        # vacío
$ git rev-parse HEAD:.github/workflows/verify.yml      49d4e0414c83b98a11977e8eae6b57b0ead5fa31
$ git rev-parse origin/main:.github/workflows/verify.yml
                                                       49d4e0414c83b98a11977e8eae6b57b0ead5fa31
```

**Mismo blob, byte a byte**, y ese mismo archivo corrió **verde** en `main` doce horas antes
(`32925827992`, `PR #367`). El YAML parsea. Este acto **no toca `.github/`** — está fuera de su
lista cerrada.

Es la clase de fallo que la **cabecera del propio workflow ya documenta** (endurecimiento del
7/ago tras `PR #149`/`#150`/`#151`: *«`#151` murió en "Set up job" con Service Unavailable bajando
la definición de la action, antes de ejecutar una línea de código»*). Señal de degradación
concurrente, no de contenido: el `PR #369` hermano tenía su run **encolado 27 minutos** en la misma
ventana.

`gh run rerun` **no sirve** para esta clase: responde *«run … cannot be rerun; its workflow file may
be broken»* — un `startup_failure` no tiene jobs que relanzar. La vía es **re-disparar el evento
`pull_request`** con un commit nuevo sobre la rama, que es lo que hace el commit de esta adenda.

### 6.2 · Colisión viva de `ADR`, declarada

`gh pr list --state open` corrió al arrancar y salió **vacío**; queda registrado como salió. Al
resolver el CI apareció que **`PR #369`** (`ACTO CIERRA-4-FIRMAS`, rama
`claude/cierra-4-firmas-8b6f2r`) candidatea **también `ADR-198`**.

| hecho | marca de tiempo |
|---|---|
| `PR #369` creado | `2026-08-26T15:11:17Z` |
| commit de este acto | `2026-08-26T15:27:06Z` |
| `PR #370` creado | `2026-08-26T15:27:54Z` |

La consulta de arranque cayó **dentro de esa ventana de minutos**. **No se reclama precisión sobre
cuál instante fue primero** — se declara la consulta como salió y el hecho como es, en vez de
inventar un orden que justifique el número propio.

**Regla aplicada, la misma que `ADR-194` ya aplicó sobre sí mismo: el que fusione primero se queda
con el número.** Si `PR #369` fusiona antes, este acto pasa a **`ADR-199`** al resolver el merge, y
**la contribución ajena se conserva íntegra — nunca se edita hacia atrás lo ya commiteado por
otro**. `PR #369` toca además `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md` y
`forense/firmas-pendientes.tsv`: conflicto de `git merge` esperado en los tres, a resolver a mano
conservando lo ajeno y renumerando lo propio (incluida la cabecera de conteo y `estado §L0`).

La corrección de §5 es de esa clase: la línea de cascada decía *«ninguna colisión viva que
declarar»* — cierto cuando se escribió, **vencido** al empujar. Se corrige en vez de dejarse, porque
es una afirmación de hecho dentro de `canon`.
