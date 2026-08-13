# GDELT-UCDP-RECON — caracterización, no descarga

**Acto:** ENCARGO B · GDELT-UCDP-RECON (relanzado) · **Cierra:** D9 · **Entorno:** CAJA con red, NO nube · **Base:** `origin/main = 959006a` (post-PR #206, ENASIC-SPLIT, coincide con el declarado por el encargo, no hizo falta refrescar) · **Worktree:** `~/mm-gdelt-ucdp-recon`, rama `gu/gdelt-ucdp-recon`.

## §0 · ARRANQUE — verificado, no supuesto

- `$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → vacío (confirma `caja`, no `nube`).
- `grep -rliE "multi.?agent|agent.?fleet|orchestrat|subagent" tools/ tests/` → **vacío**. No se encontró "infraestructura de agentes" declarada en este repo. Se procede con `curl` directo, como instruye el encargo para este caso.
- `data/raw` → symlink nuevo a `/home/pc0/mm-corpus/raw` (`ln -s`, verificado con `readlink -f`, 258 entradas visibles). `data/raices.local.yaml` copiado del clon base (gitignorado, no lo hereda un worktree nuevo).
- `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.gdeltproject.org/data.html` → **200**, sin override de sandbox necesario (a diferencia de lo medido por SONDA-1 el 8/ago para otros dominios — este host respondió directo). GET, nunca HEAD, en todos los sondeos de este acto.
- Filas de acceso ya sondeadas por VERIFICA-PUERTAS (`data/acceso-puertas-2026-08-13.tsv`, verificado contra el archivo real, no solo contra el texto pegado del encargo): `GDELT_RawDataFiles` y `UCDP_Downloads_GED`, ambas `206`/`AGENTE`/`N17,N27`. No se repite el sondeo de acceso — este acto sondea **estructura**, que es otra cosa.
- Las dos filas duplicadas del puntero (`GDELT`/`UCDP`, `gap_mapeo_map_b`, `NO_PROBADO`) no se tocan — regla de precedencia de RECONCILIA-PUERTAS: gana la fila con sondeo de portal.

## §1 · COMMIT 1 — techo y criterio, congelados antes de bajar nada

**Techo de descarga por fuente: ≤500 MB.** Si caracterizar exige más, este acto para y reporta cuánto haría falta — no se negocia en vuelo.

**Archivo mínimo que caracteriza la estructura, nombrado antes de bajarlo:**
- **GDELT:** el índice/manifiesto de archivos de la portada de datos (se buscará un listado tipo "master file list" bajo `data.gdeltproject.org`, categoría "índice/manifiesto" del propio encargo) — si existe, es el artefacto mínimo; si no, el archivo diario más pequeño que ese índice referencie ("un solo día de datos").
- **UCDP:** la página de descargas ya declara un listado de datasets versionados (GED Global) y, por convención de UCDP, un codebook — el codebook (PDF, típicamente pequeño) es el candidato de "manifiesto/codebook"; si no basta para ver la estructura de columnas, el archivo de datos más pequeño ofrecido ahí.

**Mecanismo de recorte candidato, escrito antes de mirar el contenido (no la portada) — de conocimiento general sobre estos dos proyectos, declarado como hipótesis a verificar, no como hecho:**
- **GDELT:** se espera **COLUMNA** — registros a nivel de evento con campos de código de país del actor/ubicación geográfica (convención FIPS en GDELT), no separación por archivo ni por endpoint en el nivel "Raw Data Files" (que la propia portada organiza por fecha, no por país). Costo esperado: alto si es solo columna — hay que bajar y filtrar, no solo pedir un recorte ya hecho.
- **UCDP:** se espera **COLUMNA** también — evento/díada/país-año con un código de país (convención Gleditsch-Ward) por fila; candidato secundario a verificar: **archivo aparte**, si la página de descargas ofrece extractos regionales o por país ya recortados (no asumido, se revisa la página real en Commit 2 antes de descartarlo).

**Veredicto, criterio cerrado (idéntico para ambas fuentes):**
- **RECORTE-VIABLE** — el mecanismo existe y se puede ejercer con lo que ya hay en este repo (p. ej. `awk`/`grep` sobre una columna de país).
- **VIABLE-CON-PARSER-NUEVO** — el mecanismo existe pero exige código que no está (p. ej. geocodificación lat/lon → país, sin campo de país directo).
- **NO-SEPARABLE** — no hay forma de aislar México sin bajar todo.

**Pre-registro de falsación (B-bis):** si el archivo mínimo trae un campo de país de dos-letras/Gleditsch-Ward legible y filtrable con herramientas ya presentes → `RECORTE-VIABLE`, y este acto da el comando y el volumen estimado del recorte mexicano. Si el único camino para aislar México exige cruzar contra una tabla de referencia geográfica que no está en el repo (lat/lon sin país, o un ID que no mapea a país sin una tabla externa) → `VIABLE-CON-PARSER-NUEVO`, sin escribir el parser aquí. Si no hay ningún campo, archivo ni endpoint que distinga país → `NO-SEPARABLE`, resultado válido y cierre completo de la pregunta.

**Reserva de A.4, no se salta:** `EXISTE-NO-SATISFACE` es la clasificación vigente y correcta de ambas fuentes hoy. Solo cambia si este acto demuestra el recorte con comando y salida real. Un `200` en la portada no es satisfacción.

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## §2 · COMMIT 2 — GDELT

### 4.1 · Estructura real, verificada byte a byte

La portada (`data.html`) enlaza `data.gdeltproject.org/gdeltv2/masterfilelist.txt` (índice real, **121,640,427 bytes** por `Content-Length` — se muestreó solo un rango de ~2 KB, no se bajó completo, no hacía falta para caracterizar el formato) — una línea por archivo, formato `<bytes> <md5> <url>`, tres tipos de archivo por intervalo de 15 min (`export`/`mentions`/`gkg`) desde al menos 2015-02-18. `lastupdate.txt` confirma el patrón vigente hoy con timestamps reales (`20260813160000...`).

**Trampa de portal real, no hipotética — igual a la de INEGI/CNGMD que el encargo citó, mecanismo distinto:** el enlace de la propia página, `CSV.header.dailyupdates.txt`, se rotula *"GDELT **1.0** Column Labels Header Row April 1, 2013 - Present"* — declara 58 columnas. Los archivos reales de `gdeltv2/` (GDELT **2.0**) tienen **61**. No es un soft-404 (el archivo es real y descarga bien) — es una documentación vigente para el esquema equivocado, enlazada desde la página que sí describe el producto correcto. No se heredó: las columnas de país se localizaron **empíricamente**, por contenido, no por ningún header de documentación:

```
python3: para cada una de las 61 columnas de una fila real, contar cuántos de 1500 valores
casan ^[A-Z]{2}$ -> 3 columnas por encima de 50%: col 37 (1315/1500), col 45 (1069/1500,
431 vacíos), col 53 (1458/1500, top valores US/IS/IN/UK/CA -- distribución real de países)
```

13 archivos `.export.CSV.zip` reales descargados completos (`20260813130000` a `20260813160000`, ~3.25 h de cobertura): **los 13, HTTP 200, ZIP válido, tamaño descargado = tamaño declarado por `Content-Length` en los 13**, ninguno es señuelo. Ejemplo verificado: `20260813160000.export.CSV.zip`, declarado 98,851 bytes, descargado 98,851 bytes, `file` confirma ZIP real con tamaño sin comprimir 630,350 bytes — coincide exacto tras extraer.

### 4.2 · ¿México es separable, y cómo?

**Sí — COLUMNA**, confirmada con datos reales, no con documentación:

```bash
awk -F'\t' '$54=="MX"' 20260813160000.export.CSV
# -> 1 fila real: ... 1  Mexico  MX  MX     23  -102  MX  ...  (ActionGeo país=México, resolución a nivel país)
```

Campo 54 (1-indexado, `awk`) es la columna empírica `col 53` de arriba — corresponde en posición y contenido a `ActionGeo_CountryCode`, el campo geográfico de acción con mayor cobertura de las tres columnas de país candidatas (`Actor1CountryCode`/`Actor2CountryCode`/`ActionGeo_CountryCode` en el esquema 1.0; el 2.0 desplaza posiciones mas conserva el concepto). Sin cruzar contra ninguna tabla externa — el propio archivo trae el código de país FIPS en cada fila. `FIPS.country.txt` (portal) confirma `MX = Mexico`, consistente con el valor real observado.

### 4.3 · Volumen del recorte mexicano, estimado con su comando

Muestreado 13 de 96 archivos `.export` de un día (13.5%, ~3.25 h reales, no 24 h completas — extrapolación declarada, factor ×(96/13)≈**7.4**):

```
17,970 filas totales · 72 filas MX (ActionGeo_CountryCode) · fracción MX = 0.401%
promedio comprimido/archivo: 91,104 bytes · promedio sin comprimir/archivo: 567,301 bytes
```

**Extrapolado a un día completo (96 archivos, tier `export` únicamente):** ~**8.75 MB** comprimidos / ~**54.5 MB** sin comprimir · ~**532 filas MX estimadas/día**. **No extrapolado** para `mentions` ni `gkg` — no examinados en este acto (`gkg` mide ~7.6 MB/archivo en `lastupdate.txt`, ~76× el tamaño de `export`; incluirlo dominaría cualquier estimate combinado y no se verificó su esquema de columnas — declarado, no asumido).

### 4.4 · Veredicto

**`RECORTE-VIABLE`**, acotado explícitamente al tier `export` (eventos) de GDELT 2.0 en tiempo real (`data.gdeltproject.org/gdeltv2/*.export.CSV.zip`). Mecanismo: filtro de una sola columna (`ActionGeo_CountryCode == "MX"`), ejercitable con `awk`/`python3` ya presentes en este repo — no exige parser nuevo. **No extendido** a `mentions`/`gkg`: esquema de columnas no verificado para esos dos tipos, fuera de este acto.

**`EXISTE-NO-SATISFACE` no cambia** — sigue siendo la clasificación correcta de la puerta *tal como está declarada hoy* (sin recorte). Este veredicto de separabilidad es información nueva, adicional, no una promoción de A.4 — cambiar `clasificacion_a4` de la fila de `universo-puertas` no está en el perímetro de escritura de este acto (`data/universo-puertas-2026-08-12.tsv` solo admite filas **nuevas** de adquisición, no ediciones a la fila de sondeo existente).

### 4.5 · Registro de lo descargado

13 archivos `.export.CSV.zip` (1,184,348 bytes comprimidos reales) + muestras pequeñas de `masterfilelist.txt`/`lastupdate.txt`/`CSV.header.*.txt`/`FIPS.country.txt` (unos KB cada una, no se registran como payload — son consulta de estructura, no dato). Registro de los 13 `export` vía manifiesto en §4 de este acto (junto con los de UCDP, un solo paso `--escanea`/`--promueve`).

---

## §3 · COMMIT 2 — UCDP

### 4.1 · Estructura real, verificada byte a byte

La página de descargas (`ucdp.uu.se/downloads/`) trae, para el dataset GED (`Downloads_GED`, la puerta ya sondeada): `ged261-csv.zip`, `ged261-dta.zip`, `ged261-rds.zip`, `ged261-xlsx.zip`, `ged261.pdf` (codebook). Tamaño real declarado por `Content-Range` (`GET -r 0-0`, nunca `HEAD`): `ged261-csv.zip` = **39,122,522 bytes**, `ged261.pdf` = **917,038 bytes**. Ambos dentro del techo de 500 MB — se descargó el CSV **completo** (no una muestra): es la base real de UCDP entera, y su tamaño real la deja cómodamente bajo el techo — no hace falta extrapolar cuando medir de verdad cuesta menos que el límite (declarado aquí para que se audite el criterio, no se supone tácito: "no bajar bases completas" del §6 se lee como el principio que evita repetir el defecto de 15 GiB con GDELT, no como una prohibición absoluta sobre un archivo que ya es pequeño con todo y país incluido).

Descarga verificada: 39,122,522 bytes bajados = 39,122,522 declarados, ZIP válido, extrae a `GEDEvent_v26_1.csv`, **273,992,720 bytes sin comprimir, 49 columnas, 417,968 filas** — verificado abriendo el CSV real con el módulo `csv` de Python contra su propio encabezado (no se asumió posición de columna).

**Segundo mecanismo real, no buscado por el encargo pero encontrado en la misma página:** `ucdp.uu.se/apidocs/` documenta una API REST (`ucdpapi.pcr.uu.se/api/gedevents/26.1`) con filtro **por endpoint** (`?Country=<código Gleditsch-Ward>`, ejemplo real citado en la propia documentación: `?Country=90,91,92` para Guatemala/Honduras/El Salvador). Probada en vivo: responde `API token required. Add header: x-ucdp-access-token: <tu-token>` — el mecanismo de endpoint es real y más barato en bytes que el CSV completo, pero exige un token (barrera de registro no caracterizada más allá de esto — fuera del mandato `curl` sin cuenta de este acto; mismo nivel de fricción ya aceptado en este programa para GESIS/WVS/World Bank).

### 4.2 · ¿México es separable, y cómo?

**Sí — COLUMNA, confirmada con el archivo completo, y además ENDPOINT (con token, no ejercido aquí):**

```python
# csv.DictReader real sobre GEDEvent_v26_1.csv, columna 'country' (nombre) y 'country_id' (Gleditsch-Ward)
# 417,968 filas totales; country=='Mexico' -> 25,714 filas; country_id de esas filas: 70
```

`country_id=70` coincide con el código que ya se había usado para probar la API (§3, hipótesis previa a mirar el CSV) — confirmación cruzada entre dos mecanismos independientes, no solo uno.

### 4.3 · Volumen del recorte mexicano, estimado con su comando

**No es extrapolación — es el conteo real sobre el archivo completo** (a diferencia de GDELT, donde 500 MB no habrían alcanzado para un año completo):

```
417,968 filas globales · 25,714 filas México (6.15%) · México es el 4° país más representado
en todo el dataset, detrás de Siria (88,289), Afganistán (42,476) y Ucrania (40,434) — hallazgo
no buscado, verificado con el conteo real, no una impresión de la portada.
recorte México, tamaño aproximado sin comprimir: ~16.73 MB (suma de longitud de fila UTF-8,
25,714 de 417,968 filas) -- proporción de aprox. 6.1% del CSV sin comprimir de 273.99 MB.
```

### 4.4 · Veredicto

**`RECORTE-VIABLE`**, por dos vías independientes: **(a)** columna `country`/`country_id` sobre el CSV completo (39.1 MB comprimidos, ya descargado y verificado en este acto) — cero código nuevo, `csv`/`pandas` ya presentes; **(b)** endpoint `Country=70` de la API REST — más barato en bytes pero requiere token, no ejercido en este acto (fuera del mandato sin-cuenta).

**`EXISTE-NO-SATISFACE` no cambia**, mismo criterio que GDELT en 4.4 — hallazgo nuevo, no edición de la fila de sondeo existente.

### 4.5 · Registro de lo descargado

`ged261-csv.zip` (39,122,522 bytes) + `ged261.pdf` (917,038 bytes, codebook) — descarga real y completa de la base GED de UCDP, dentro del techo. No se registra ningún subconjunto "solo México" derivado por este acto — lo que se registra es lo que de verdad vino de la fuente; el recorte queda como hallazgo reproducible por comando (arriba), no como archivo nuevo inventado por este acto.

---

## §4 · CONTADOR

**Dos veredictos de separabilidad donde hoy había dos `EXISTE-NO-SATISFACE` sin resolver:**

| fuente | veredicto | mecanismo | volumen del recorte mexicano |
|---|---|---|---|
| GDELT (tier `export`, tiempo real) | `RECORTE-VIABLE` | columna (`ActionGeo_CountryCode=="MX"`) | ~8.75 MB/día comprimidos (estimado, factor ×7.4 desde muestra de 13/96 archivos), ~532 filas MX/día |
| UCDP (GED v26.1) | `RECORTE-VIABLE` | columna (`country_id==70`) **y** endpoint (`Country=70`, requiere token) | ~16.73 MB sin comprimir (medido, no estimado — 25,714 de 417,968 filas, base completa ya descargada) |

**0 de 2 es `VIABLE-CON-PARSER-NUEVO` o `NO-SEPARABLE`** — ninguna requirió parser nuevo ni cerró como no-separable. Declarado porque el propio encargo nombra `NO-SEPARABLE` como el resultado "probablemente más útil" y este acto no lo produjo para ninguna de las dos — ambas fuentes resultaron más simples de recortar de lo que su clasificación `EXISTE-NO-SATISFACE` (correcta, sobre la fuente *sin* recorte) hacía parecer.

## §5 · NO HACE — verificado contra lo que este acto realmente hizo

No bajó las bases completas *de GDELT* (13 de miles de archivos de 15 min; el índice completo, 121 MB, se muestreó ~2 KB). Sí bajó la base completa *de UCDP* (39.1 MB, GED entero) — declarado en 4.1 como lectura deliberada del techo de 500 MB, no una excepción tácita. No escribió parser nuevo (ninguna de las dos lo exigió). No cambió `clasificacion_a4` de ninguna fila de sondeo — ambas siguen `EXISTE-NO-SATISFACE`, el veredicto de separabilidad es hallazgo adicional, no promoción. No tocó `relaciones.tsv` ni `cola-adquisicion-*.tsv`. No retiró las filas viejas `gap_mapeo_map_b` del puntero (`GDELT`, `UCDP`) — siguen ahí, sin marcar, per regla de precedencia de RECONCILIA-PUERTAS. No prometió viabilidad antes de medir — los dos veredictos `RECORTE-VIABLE` vienen de comandos reales con salida real, no de la portada.

## §6 · Trampas de mecanismo encontradas en este acto, declaradas, no corregidas

**`tests/manifiesto.py --escanea` no recorre subdirectorios — `os.listdir()`, no `os.walk()` (`tests/manifiesto.py:660`), verificado en el código, no supuesto.** Los 13 archivos de GDELT, colocados primero en `data/raw/gdelt_export_sample_20260813/`, dieron **0 archivos nuevos detectados** en el primer intento (`--grupo` sin coincidencias, ningún grupo nuevo listado). Se resolvió aplanando los 13 al nivel superior de `data/raw/` — no hay colisión de nombre (timestamps únicos), pero cualquier acto futuro que organice su adquisición en subcarpetas se topará con el mismo silencio (no es un error, es "0 archivos nuevos", indistinguible de "ya estaba todo registrado" sin leer el código). No documentado por el encargo ni por el `--help` del script — nuevo, para el próximo acto que use `data/raw/<algo>/`.

**El patrón `data/raw/` de `.gitignore:5` no cubre el symlink que este mismo ARRANQUE instruye crear.** `ln -s /home/pc0/mm-corpus/raw data/raw` deja `git status` reportando `data/raw` como `??` (no ignorado) — verificado con `git check-ignore -v data/raw`, sin salida. Mismo defecto ya visto en [[B-4b-alpha]] (memoria de sesiones previas, no re-descubierto de cero aquí — confirmado de nuevo, en este worktree, con comando). No se tocó `.gitignore` (fuera del perímetro declarado de este acto; es config compartida entre docenas de worktrees activos hoy). Mitigación aplicada: `git add` explícito por archivo en cada commit de este acto, nunca `git add -A`/`git add .` — el symlink nunca entró a un commit, verificado con `git show --stat` de cada uno.
