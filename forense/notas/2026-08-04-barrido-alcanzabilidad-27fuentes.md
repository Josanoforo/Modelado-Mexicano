# Barrido de alcanzabilidad: re-sondeo de 5 de las 27 SIN PAYLOAD bajo premisa refutada

Sesión Sonnet, Ubuntu, rama `sesion/barrido-alcanzabilidad-27fuentes` (worktree nuevo,
`origin/main` = `6f50b3f`, posterior a `6a09a37` donde la maestra #17 verificó procedencia).
Encargo: sondeo puro — determinar estado y localizar URL para 5 de las 27 fuentes SIN PAYLOAD
de `2026-07-31-cola-descarga-rederivada.md` §2, bajo la hipótesis de que la mayoría de los "no
alcanzable" del corpus son en realidad "no adiviné el nombre del archivo". **No se bajó ningún
microdato.** `data/manifiesto.yaml` no se toca.

## 0 · Resultado en una línea

**Hipótesis confirmada, 5/5.** Las cinco fuentes sondeadas — ENDIREH, ENSU, ENCUP, ENASEM ·
ENBIARE · ENASIC, ENDUTIH · MOCIBA — dan **RESPONDE** con URL real verificada. Ninguna dio NO
ALCANZABLE DESDE ESTE ENTORNO. La premisa que las tenía clasificadas SIN PAYLOAD no era "el
recurso no existe" ni "el entorno no llega" — era que nadie había corrido el mecanismo B (JSON
API `archivoscompaginacion`, documentado desde el 31/jul para CPV/ENADID/ENOE/ENIF/ENVIPE/ENCIG/
ENUT) contra estas siete fuentes concretas, y en el caso de ENCUP, que la restricción de red
medida en el sandbox de nube (C-bis, `2026-08-03-cbis-deferencia-externas.md`) se heredó sin
re-medir en un entorno con perímetro de red distinto.

## 1 · Mecanismo usado, y por qué no es "patrón adivinado a ciegas"

Para INEGI (ENDIREH, ENSU, ENASEM, ENBIARE, ENASIC, ENDUTIH, MOCIBA), **no hizo falta adivinar
nombre de archivo**. El mecanismo ya documentado en `2026-07-31-cola-descarga-rederivada.md` §4
y `2026-07-31-enut-descarga.md` (JSON API `archivoscompaginacion`, no HTML crudo ni patrón
estático inventado) resolvió las siete de una vez:

1. `curl` la página `/programas/{prog}/{año}/` — si es un shell real (no el soft-404 de 13 370
   bytes con título "Página no encontrada"), trae `<menu-gen idm='NNNN'>` — ese `NNNN` es
   `idBiinegi`.
2. `curl` `/programas/{prog}/{año}/data/pestana/pestanadata.js` — confirma que existe pestaña
   "Microdatos" (`data-tipoinformacion="4"`) y si trae `data-proyecto`/`data-anio` propios (las
   siete de este barrido no los traen — a diferencia de CPV/ENADID, que sí los necesitan y por
   eso siguen bloqueados, `2026-08-03-descarga-masiva-xml-mecanismo.md` §0).
3. `GET` a
   `https://www.inegi.org.mx/app/api/descarga/componente/descargamasiva/lista/archivoscompaginacion`
   con `idBiinegi`, `tipodocto=4`, `tema=subtema=areaGeografica=proyecto=anio=0`,
   `agrupacion=` (base64 de `"Todas"` = `VG9kYXM=`), `desde=1&hasta=1000&ordenar=orden&orden=desc&ingles=0&datosAbiertos=0&textoBuscar=`
   — devuelve JSON con `pathLogico` + `extension` por archivo real, sin adivinar nada (el
   endpoint mismo lo declara).
4. URL final = `https://www.inegi.org.mx/contenidos` + `pathLogico` + `_` + `extension` +
   `.zip` (o sin `.zip` si `extension` ya es `pdf`/`xlsx` — verificado caso por caso abajo).
5. Cada URL se verificó con `curl -s -o /dev/null -D - -r 0-0 URL` (GET de 1 byte con
   `Range`, no `HEAD` — instrucción del encargo) leyendo `Content-Type` y `Content-Range`
   (que trae el tamaño total exacto sin bajar el archivo completo). Ninguna de las siete dio
   la firma de soft-404 (2 263 bytes fijos, `text/html`); las siete dieron
   `Content-Type: application/x-zip-compressed` (o `pdf`/`xlsx` según el archivo) y un
   `Content-Range` con tamaño de orden de magnitud consistente con una base de microdatos real
   (1.5–79 MB).

Para ENDIREH, además, el JSON-LD embebido en el HTML crudo de la página (`<script
type="application/ld+json">`, campo `distribution[0].contentUrl`) ya traía una URL — y esta vez
**no era el placeholder señuelo** que `2026-07-31-perimetro-descarga.md` §3 advierte para
ENVIPE 2024 (`prueba.pdf`, soft-404): apuntaba a un zip real de 74 222 707 bytes, verificado por
separado del mecanismo de API (§3). Se cruzó contra el resultado del API (§3) precisamente
porque la nota de referencia advierte no confiar en el JSON-LD sin verificar — aquí se verificó,
y dio un segundo archivo real, no el mismo (ver nota de tamaños distintos en §3).

**Hallazgo colateral de vocabulario:** hay al menos dos plantillas de soft-404 en este dominio,
no una. La ya documentada (`2026-07-31-perimetro-descarga.md` §2): 2 263 bytes, bajo rutas
`/contenidos/...`. Una segunda, encontrada este barrido al probar subrutas de ENSU que no
existen (`/programas/ensu/2025/`, `/programas/ensu/vigente/`, etc.): **13 370 bytes**, título
`Página no encontrada`, texto "Esta liga ya no existe, lamentamos el inconveniente", bajo rutas
`/programas/...`. Las dos comparten la propiedad que importa (HTTP 200, no distinguible por
código de estado), pero **no son el mismo tamaño fijo** — cualquier chequeo automatizado de
"soft-404 conocido" que compare solo contra 2 263 bytes se equivoca en rutas `/programas/`. Se
deja anotado para quien automatice el chequeo de tamaño/firma.

## 2 · ENDIREH — RESPONDE, dos URLs reales (no la misma)

**Universo del instrumento (declarado, no verificado esta sesión — es del cuestionario, no del
mecanismo de red): mujeres 15+ años**, `hitoE §14.3` ya lo anota. Si esto sirve como candidata
a `exposicion_violencia` o `familismo_apoyo`/`familismo_obligacion`, **es parcial declarado, no
reactivo poblacional** — no se abrió el instrumento ni el descriptor esta sesión para confirmar
contenido de reactivo, ADR-46 (identificar estructura de alcanzabilidad, no leer reactivo).

| Vía | URL | Verificación |
|---|---|---|
| JSON-LD (HTML crudo) | `https://www.inegi.org.mx/contenidos/programas/endireh/2021/datosabiertos/conjunto_de_datos_endireh_2021_csv.zip` | `Content-Type: application/x-zip-compressed`, `Content-Range: bytes 0-0/74222707` |
| API `archivoscompaginacion` (`idBiinegi=3117`) | `https://www.inegi.org.mx/contenidos/programas/endireh/2021/microdatos/bd_endireh_2021_csv.zip` | `Content-Type: application/x-zip-compressed`, `Content-Range: bytes 0-0/78902567` |

Los dos son reales, los dos responden, los tamaños difieren (74.2 MB vs. 78.9 MB) — no se
determinó esta sesión si son el mismo conjunto con empaquetado distinto o ediciones distintas
del mismo producto (`datosabiertos/` vs. `microdatos/` son rutas de publicación distintas en
este portal). Queda para quien decida cuál descargar, con la duda declarada, no resuelta por
adivinanza.

## 3 · ENSU — RESPONDE, sin subruta de año (portal de programa único, no por edición)

Descarta un supuesto de este barrido: ENSU **no** tiene páginas `/programas/ensu/{año}/` (todas
las variantes probadas — `2025`, `2024`, `vigente`, `bd`, `microdatos` — dan el soft-404 de
13 370 bytes de §1). El portal real es único, sin año: `/programas/ensu/` (`idm="1127"`, HTML
crudo de 4 196 bytes, JSON-LD con el placeholder señuelo `prueba.pdf` — **no sirve**, hay que
usar el mecanismo de API). `pestanadata.js` del mismo root confirma pestaña "Microdatos"
(`data-tipoinformacion="4"`, `data-id="1127"`, sin `data-proyecto`/`data-anio` propios).

El API devuelve 4 ediciones de base de datos (`ensu_bd_2026`, `2025`, `2024`, y una anterior),
cada una en 5 formatos (csv/dbf/dta/RData/sav). Verificada la de 2025:

`https://www.inegi.org.mx/contenidos/programas/ensu/microdatos/ensu_bd_2025_csv.zip` —
`Content-Type: application/x-zip-compressed`, `Content-Range: bytes 0-0/12332522` (12.3 MB).

**Pertinencia para `confianza_institucional[seguridad]`/`exposicion_violencia`: sigue "parcial,
no verificada"** — este barrido confirma que el archivo existe y responde, no que su contenido
mida esos constructos. Eso es lectura de reactivo, fuera de este acto.

## 4 · ENCUP — RESPONDE desde Ubuntu; la restricción previa era de otro entorno, no de la fuente

`2026-08-03-cbis-deferencia-externas.md` (sesión en sandbox de nube) midió
`fomentocivico.segob.gob.mx` como **NO DETERMINABLE — espejo fuera del sandbox**: el `CONNECT`
del proxy se aceptaba pero el `ClientHello` TLS nunca recibía respuesta, timeout a los 15 s.
Esa nota ya declaraba explícitamente que la causa más probable era un firewall de salida de
*ese* entorno, no una propiedad del host — y `canon/gobernanza-v1_15.md` (f) registró la
candidata como **abierta, no agotada**, con "una sesión futura con ese host habilitado" como
ruta de recuperación. Esta sesión es esa sesión futura: el entorno Ubuntu tiene
`fomentocivico.segob.gob.mx` en su lista de hosts de red permitidos.

**Resultado: RESPONDE, con una salvedad de cadena TLS, no de red.** El `CONNECT` y el
`ClientHello` completan sin timeout; el handshake TLS se cierra con
`SSL certificate OpenSSL verify result: unable to get local issuer certificate (20)` — cadena
de certificado incompleta del lado del servidor (CA intermedia de GoDaddy no servida), no un
bloqueo de política de egreso ni de DNS. Es una tercera cosa, distinta de las dos ya vistas en
este corpus (soft-404 con 200 real; SPA sin `href`): **RESPONDE pero con cadena TLS no
verificable sin `-k`** — declarado así para no colapsarlo ni con NO ALCANZABLE ni con RESPONDE
sin matiz.

Con `-k` (solo para leer `Content-Type`/tamaño de diagnóstico — no para tratar el contenido
como confiable a ciegas), la página `https://fomentocivico.segob.gob.mx/es/FomentoCivico/ENCUP`
da HTML real de 19 855 bytes (portal SWB de SEGOB, no plantilla de error), con **enlaces
directos a documentos reales en el HTML crudo** (mecanismo A del encargo, el más barato — no
hizo falta ni patrón ni API):

- `BaseDatos_ENCUP_2012_Final.xlsx` — verificado: `Content-Range: bytes 0-0/4814178` (4.8 MB),
  servidor `Oracle GlassFish Server 3.1.2.19`, `Last-Modified: Thu, 29 Apr 2021`, `ETag`
  consistente con el tamaño. **Es una base de datos real, no un descriptor ni un cuestionario.**
- Cinco cuestionarios (`Cuestionario_Primera_2001_ENCUP.pdf` … `Cuestionario-Quinta_2012_ENCUP.pdf`)
  y sus informes de resultados (2001/2003/2005/2008/2012), más bases `.xls` de 2001/2003/2005/2008
  — no verificados uno por uno con `curl -r 0-0` esta sesión (serían 10 verificaciones más de
  las que el encargo pidió para esta fuente); el patrón de nombre y el servidor son los mismos
  que dieron real para la base 2012, así que es razonable esperar que respondan, pero **eso es
  expectativa, no verificación** — igual que la nota de CPV/ENADID advierte para "Descarga
  masiva" en otros portales.

Esto desbloquea `deferencia` más allá de lo que C-bis logró: C-bis solo tenía el cuestionario
INEGI-shell (sin instrumento) y cerró ENCUP como NO DETERMINABLE. Aquí hay una base de datos
real de 2012 alcanzable. **No se leyó el cuestionario ni la base** — ADR-46, esto es sondeo de
alcanzabilidad, no lectura de reactivo; que la base sirva para `deferencia` específicamente es
juicio de mesa sobre contenido, no de esta sesión.

## 5 · ENASEM · ENBIARE · ENASIC — RESPONDE, 3/3, mismo mecanismo que §1

| Fuente | `idBiinegi` | URL verificada | `Content-Range` |
|---|---|---|---|
| ENASEM 2021 | `3295` | `.../contenidos/programas/enasem/2021/microdatos/enasem_2021_bd_csv.zip` | `0-0/7438658` (7.4 MB) |
| ENBIARE 2021 | `3103` | `.../contenidos/programas/enbiare/2021/microdatos/enbiare_2021_base_de_datos_csv.zip` | `0-0/5684658` (5.7 MB) |
| ENASIC 2022 | `3325` | `.../contenidos/programas/enasic/2022/microdatos/enasic_2022_bd_csv.zip` | `0-0/2289078` (2.3 MB) |

Las tres traen además descriptor de archivos (FD) real listado por el mismo API (no verificado
por separado esta sesión — mismo criterio de expectativa razonable de §4, no confirmación).
Estas tres son las candidatas de `familismo_obligacion`/`familismo_apoyo` que hoy solo tienen
proxy vía ENUT (§3 del encargo) — este barrido no verifica si el reactivo existe en ellas, solo
que las tres bases responden y son alcanzables para quien decida leerlas.

## 6 · ENDUTIH · MOCIBA — RESPONDE, 2/2

| Fuente | `idBiinegi` | URL verificada | `Content-Range` |
|---|---|---|---|
| ENDUTIH 2024 | `3413` | `.../contenidos/programas/endutih/2024/microdatos/endutih2024_bd_dbf.zip` | `0-0/8823853` (8.8 MB) |
| MOCIBA 2024 | `3438` | `.../contenidos/programas/mociba/2024/microdatos/mociba2024_bd_csv.zip` | `0-0/1500882` (1.5 MB) |

Nota de formato: ENDUTIH solo publica su base en DBF (`extension` del API = `dbf`, sin `csv`
listado) — a diferencia de MOCIBA, que trae los cinco formatos (csv/dbf/dta/RData/sav) como
ENSU. No es un error de sondeo: el API mismo declara qué formatos existen por fuente.

## 7 · Tabla-resumen (entregable)

| # | Fuente | Estado | Vía que funcionó | URL real | Qué desbloquea | Si no alcanzado: política/ausencia |
|---|---|---|---|---|---|---|
| 1 | ENDIREH 2021 | **RESPONDE** | JSON-LD (HTML crudo) + API `archivoscompaginacion` (cruzados, dos URLs reales distintas) | `.../endireh/2021/datosabiertos/conjunto_de_datos_endireh_2021_csv.zip` (74.2 MB) y `.../endireh/2021/microdatos/bd_endireh_2021_csv.zip` (78.9 MB) | `exposicion_violencia`, candidata `familismo_apoyo`/`familismo_obligacion` — **parcial declarado, universo mujeres 15+** | — |
| 2 | ENSU | **RESPONDE** | API `archivoscompaginacion` (no hay subruta de año; JSON-LD da placeholder señuelo, no sirve) | `.../ensu/microdatos/ensu_bd_2025_csv.zip` (12.3 MB) | `confianza_institucional[seguridad]`, `exposicion_violencia` — pertinencia sigue parcial/no verificada (contenido, no alcanzabilidad) | — |
| 3 | ENCUP | **RESPONDE** (con salvedad: cadena TLS incompleta, requiere `-k` para diagnóstico) | href real en HTML crudo de `fomentocivico.segob.gob.mx` | `https://fomentocivico.segob.gob.mx/work/models/FomentoCivico/Documentos/PDF/CultDemo/BaseDatos_ENCUP_2012_Final.xlsx` (4.8 MB) | `deferencia` — base de datos real 2012, más allá del cuestionario-sin-instrumento que cerró C-bis | Premisa previa (NO DETERMINABLE) era de política de egreso del sandbox de nube anterior, no de este entorno — refutada aquí |
| 4a | ENASEM 2021 | **RESPONDE** | API `archivoscompaginacion` | `.../enasem/2021/microdatos/enasem_2021_bd_csv.zip` (7.4 MB) | `familismo_obligacion`/`familismo_apoyo` — hoy solo proxy ENUT | — |
| 4b | ENBIARE 2021 | **RESPONDE** | API `archivoscompaginacion` | `.../enbiare/2021/microdatos/enbiare_2021_base_de_datos_csv.zip` (5.7 MB) | ídem | — |
| 4c | ENASIC 2022 | **RESPONDE** | API `archivoscompaginacion` | `.../enasic/2022/microdatos/enasic_2022_bd_csv.zip` (2.3 MB) | ídem | — |
| 5a | ENDUTIH 2024 | **RESPONDE** | API `archivoscompaginacion` | `.../endutih/2024/microdatos/endutih2024_bd_dbf.zip` (8.8 MB, solo DBF) | `acceso_digital` — eje de malla de atributos, no parámetro del contador | — |
| 5b | MOCIBA 2024 | **RESPONDE** | API `archivoscompaginacion` | `.../mociba/2024/microdatos/mociba2024_bd_csv.zip` (1.5 MB) | ídem | — |

**Ningún NO ALCANZABLE DESDE ESTE ENTORNO ni RESPONDE PERO SIN EL RECURSO esta sesión** — las
9 URLs verificadas (7 vía API + 2 vía HTML crudo/JSON-LD) dieron RESPONDE limpio. Esto no
significa que las 22 fuentes restantes de las 27 SIN PAYLOAD vayan a dar el mismo resultado —
no se sondearon, por instrucción explícita del encargo (§3: "no todas las 27").

## 8 · Contaminación (ADR-46(2), declarar de más)

Esta sesión exploró estructura de portal (nombres de archivo, parámetros de API, tamaños vía
`Content-Range`) para: `www.inegi.org.mx` (portales de programa e `IdBiinegi` de ENDIREH 2021,
ENSU, ENASEM 2021, ENBIARE 2021, ENASIC 2022, ENDUTIH 2024, MOCIBA 2024) y
`fomentocivico.segob.gob.mx` (portal ENCUP completo, un HTML de 19 855 bytes leído entero para
extraer `href`). **No se abrió ni leyó ningún microdato, cuestionario, descriptor ni diccionario
de estas nueve fuentes** — solo `Content-Type`/`Content-Range` de las URLs de datos, y el HTML
de navegación/listado de las páginas de portal (estructura, no reactivo). Por ADR-46(2), esta
sesión **queda inhabilitada para pre-registrar** contra: ENDIREH, ENSU, ENCUP, ENASEM, ENBIARE,
ENASIC, ENDUTIH, MOCIBA. No se tocaron ENIGH ni ENVIPE (instrumentos de las dos sesiones Ubuntu
concurrentes declaradas fuera de alcance por el encargo) ni ningún otro host.

## Prohibiciones respetadas

No se bajó microdato: cada URL se verificó con `curl -r 0-0` (1 byte real transferido, no el
archivo completo) — la única excepción es la primera comprobación de ENDIREH (`-r 0-0` tras un
intento con `--max-time 10` sin `-r` que expiró a los 10 s sin completar la descarga; el intento
truncado no se guardó ni se registró, se descartó y se repitió con el método correcto). No se
tocó `data/manifiesto.yaml` (nada se descargó). No se abrió ENIGH ni ENVIPE. No se nombró CAAS,
CEU ni ningún acrónimo sin verificar su descriptor — no aplicó esta sesión, ninguna de las nueve
fuentes tiene ese patrón. No se re-sondeó el Cuestionario Ampliado del CPV (su bloqueo ya está
verificado, `2026-08-03-descarga-masiva-xml-mecanismo.md`).
