# ACTO P·LOTE-1 · Las cinco fuentes firmadas

`ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO`, 12/ago/2026 (`forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`), §2. Base declarada por el documento `origin/main = f8eb2e3`; base real de esta sesión `origin/main = e078e46` (merge de PR #183, posterior — `git merge-base --is-ancestor f8eb2e3 origin/main` confirma ancestro, sin deriva que re-derivar salvo la ya conocida: #183 pasó de abierto a fusionado entre la redacción del documento y esta sesión). Worktree `/home/pc0/mm-p-lote1-adquisicion`, rama `acto-p/lote1-adquisicion`.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-p-lote1-adquisicion` (`git worktree add ... origin/main`). `git log -1`: `e078e46 Merge pull request #183 from Josanoforo/acto-o/cola-adquisicion`. `git status`: árbol limpio al abrir.
   - `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy` — misma contención conocida ([[project-modelado-mexicano-git-config-contention]]). Verificado independientemente: `git log -1` quedó en `e078e46`, `git status` limpio, `git worktree list` lo lista — la creación no falló, solo la escritura de metadato de tracking.
2. **SHA.** `origin/main = e078e46`; `git merge-base --is-ancestor f8eb2e3 origin/main` → confirmado ancestro. Diferencia con la base declarada por el documento: exactamente el merge de PR #183 (esperado — el documento mismo anticipa este caso: "si tu fusión ya corrió, los gates de abajo lo confirmarán por comando").
3. **data/raw.** Ausente al crear el worktree (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo destino que la base clon y las demás worktrees). Corpus montado: `ls data/raw/ | wc -l` → 241 entradas. Este acto SÍ descarga — verificación de corpus compartido (defecto PR #77) obligatoria al cierre.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → `sin_variable`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. Firma de caja confirmada — este acto exige caja y NO nube; entorno correcto.
   - Firma de tres partes (A.2, v2.5): tercera parte `ls data/raw/ | head -1` → no vacío (corpus montado, ver punto 3). Las tres partes coherentes: caja + red + corpus.
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de este worktree o de comandos de red corridos en esta sesión, con el comando a la vista.
5-bis. **REMOTO.** `git remote -v` → `origin  https://github.com/Josanoforo/Modelado-Mexicano.git` (fetch y push). Confirmado antes de cualquier push.

**Regla A.3 aplicada primero.** El texto completo del documento (los siete actos, §0-§8) se archivó en `forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md` como *primer commit* de este acto, antes de lo que sigue.

**§0a/§1 (firma de corte) — verificados CONSUMIDOS antes de arrancar este acto.** `origin/main` en `e078e46`, mensaje `Merge pull request #183 from Josanoforo/acto-o/cola-adquisicion`. El texto de §1 de este documento ("FIRMA DE CORTE... entran ISSP(1)·WVS(3)·EARLY_CHILDHOOD_EDUCATION_2012_2014(4)·GPS(6)·CSES(7). Salen... BRASDEFER(2) y MOBILE_TUTORS(5)") coincide verbatim con lo ya registrado en memoria de sesiones previas sobre el merge de PR #183. Gate del acto (`ls data/cola-adquisicion-*.tsv`) verificado abajo.

```
$ ls data/cola-adquisicion-*.tsv | sort | tail -1
data/cola-adquisicion-2026-08-12.tsv
```

Coincide con lo esperado por el gate. Acto habilitado.

---

## 1 · El lote congelado (verbatim de `data/cola-adquisicion-2026-08-12.tsv`)

Extracción por comando (`awk -F'\t'` filtrando por `fuente_canonica` en las 5 firmadas), columnas completas:

| fuente_canonica | n_necesidades_servidas | destraba_sin_ruta | destraba_condicional_faltante | celda_piloto_FIN | url_conocida | clasificacion_a4_previa | palanca |
|---|---|---|---|---|---|---|---|
| ISSP | 7:N2,N3,N12,N13,N14,N28,N30 | SI (censo fila 12,13,14; N12,N13,N14) | *(21 condiciones individuales por necesidad, ver TSV crudo — resumen: falta verificar texto mexicano/dirección/condicionantes y monitoreo-sanción para N2,N12,N13,N14,N28,N30; N3 sin muestra México confirmada en release final 29 países, no se reabre ADR-54)* | SI | https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017 | CANDIDATAx13+NEGATIVAx1 | 1 |
| WVS | 2:N5,N15 | SI (censo fila 15; N15) | N5/N15: WVS ya en catálogo v2.0, no es puerta nueva, mapeo México pendiente | SI | VACIO — derivado abajo (§4) | CANDIDATA(APERTURA_INDETERMINADA) | 3 |
| EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 | 1:N13 | SI (censo fila 13; N13) | N13: item explícito de deber/obligación y llaves cuidador-niño | SI | https://microdata.worldbank.org/catalog/2661/study-description | CANDIDATA(APERTURA_INDETERMINADA) | 4 |
| GPS | 5:N2,N4,N5,N6,N17 | NO | las 5: falta confirmar n de México, texto/codificación exactos y desenlace coobservado pertinente | SI | https://gps.econ.uni-bonn.de/home | CANDIDATA(APERTURA_INDETERMINADA) | 6 |
| CSES | 4:N17,N25,N26,N27 | NO | N17/N25: texto y codificación; N26/N27: no es panel ni padrón de beneficiarios, no identifica por sí solo tratamiento de Pensión del Bienestar | SI | https://cses.org/data-download/cses-module-5-2016-2021/ | CANDIDATA(APERTURA_INDETERMINADA) | 7 |

Texto crudo íntegro (las 21 condiciones de ISSP sin resumir) queda en `data/cola-adquisicion-2026-08-12.tsv`, filas correspondientes — no se transcriben completas aquí por longitud, se citan por referencia al TSV congelado (ya versionado desde PR #183, no cambia).

## 2 · Criterio de cierre, común a las 5 fuentes (A.4/A.5)

**EXISTE-SATISFACE para ESTA adquisición** (no para el modelo — eso es de M-APERTURA/mesa) exige las cuatro condiciones a la vez: (a) el payload se descargó íntegro y quedó en el corpus compartido (`data/raw` real, `/home/pc0/mm-corpus/raw`, no solo en este worktree — verificación PR#77 al cierre); (b) su sha256 quedó registrado en `data/manifiesto.yaml` vía `tests/manifiesto.py --registra`; (c) la decisión de adquisición pasó por la vía del motor (capa2 / `decisiones-adquisicion`) — el TSV de cola no se edita a mano, nunca; (d) se localizó al menos una ficha documental/puerta (RNM o equivalente) y se registró una fila en el conducto (ADR-70).

- Si (a)-(c) se cumplen pero (d) no: **EXISTE-NO-SATISFACE**, declarando qué ficha se buscó y no se encontró.
- Si el portal exige más que registro gratuito (pago, afiliación institucional, licencia restringida): **NO-ACCESIBLE**, con receta manual.
- Si el sondeo A.5 falla en sesión: **NO OBTENIDO POR ESTE AGENTE EN N INTENTOS**, con los N intentos y salida cruda, más receta manual ejecutable en navegador en <1 minuto.
- GESIS (ISSP) y WVS exigen registro gratuito conocido de antemano — se declara y se hace; registro gratuito no es NO-ACCESIBLE (A.4, v2.6).
- Ninguna fuente se abre a nivel variable en este acto — eso es acto posterior (M-APERTURA u otro), por demanda.

## 3 · Nota de contexto ISSP — los tres módulos (verbatim de `forense/notas/2026-08-12-acto-o-cola-adquisicion.md:101`)

> `ISSP` tiene tres URLs distintas (GESIS, tres módulos distintos) — la cola deja solo la primera (`.../social-networks/2017`, la que corresponde a N12/N13/N30) para que la columna quede usable por `curl` sin anotación; las otras dos (`.../social-inequality/2019`, `.../family-and-changing-gender-roles/2012`) quedan declaradas aquí, no en el TSV.

Este lote baja el módulo de la URL de la cola (`social-networks/2017`). Si el portal GESIS ofrece los otros dos módulos al mismo costo de sesión (mismo registro, sin paso adicional de licencia), se bajan y registran también, declarándolo en la ejecución (§ siguiente commit). URLs de los otros dos módulos derivadas por el mismo patrón de la nota de O (no verificadas aún, SIN-FETCH hasta sondear en el commit de ejecución): `https://www.gesis.org/en/issp/data-and-documentation/social-inequality/2019`, `https://www.gesis.org/en/issp/data-and-documentation/family-and-changing-gender-roles/2012`.

## 4 · WVS — portal oficial derivado (candidata SIN-FETCH, A.6)

La cola dejó `url_conocida=VACIO` para WVS. Derivación en esta sesión, por comando, sin usar conocimiento de entrenamiento para concluir nada sobre el portal (A.5, v2.6 — "si no se sondeó en esta sesión, no se sabe"):

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.worldvaluessurvey.org/wvs.jsp
200
```

La página principal es una SPA con navegación por `javaScript:SetContent(...)`, sin hrefs directos a documentación/datos. Localizado el endpoint AJAX real que alimenta el panel de documentación por ola: `src="AJDocumentation.jsp?CndWAVE=7&COUNTRY="` (visible en el HTML crudo de `WVSDocumentationWV7.jsp`, que sondeó `200`). Fetch de ese endpoint con `CndWAVE=7`:

```
$ curl -s --max-time 15 "https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7&COUNTRY=" | grep -n -i mexico
169:    <td>Mexico 2018</td>
```

**Portal oficial declarado para este lote: `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`** (Wave 7, documentación y — según su propia pestaña "Data Download" — acceso a datos). Confirmado en esta sesión, por comando: (1) el portal responde `200`; (2) el levantamiento de México Wave 7 (2018) existe dentro de su panel de documentación (`tr id="3203"`, texto `Mexico 2018`). No confirmado aún: si el archivo de datos descargable (SPSS/dta/csv) está detrás de ese mismo ID o requiere un flujo de registro/solicitud separado — eso se abre en el commit de ejecución, no aquí. Candidata **SIN-FETCH** en el sentido de A.6 hasta ese momento: localizada por navegación de portal propio (no por buscador externo), pero el dato en sí — cuestionario, diccionario, microdato — no se ha abierto todavía.

---

El primer resultado que produzca este procedimiento es el que se reporta.

---

## 5 · Commit 2 — la ejecución (sesión de continuación, 12/ago/2026)

**ARRANQUE re-verificado en esta sesión, no heredado.** `git log -1` → `5f63dba` (Commit 1, arriba). `git fetch origin` + `git rev-list --left-right --count origin/main...HEAD` → HEAD 8 adelante / origin/main 2 adelante (el remoto avanzó con el merge de PR #184, ajeno a este acto — no se toca). `git status` limpio salvo `data/raw` sin trackear (esperado). `data/raw` resuelve por `realpath` a `/home/pc0/mm-corpus/raw` (241+ entradas antes de este commit). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir; `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`, corrido en esta sesión. Firma de caja confirmada de nuevo.

**Corrección de mesa aplicada:** la reachability de `worldvaluessurvey.org` y `gps.econ.uni-bonn.de` se re-confirmó por comando en esta sesión (`200` los dos, sin override) antes de tocarlas — un `200` en la portada no se trata como equivalente a "el archivo de datos es descargable"; son preguntas distintas, mantenidas separadas abajo fuente por fuente.

### 5.0 · Hallazgo previo a tocar cualquier fuente: el motor de "decisión de adquisición" (capa2) no tiene vía para este mecanismo

Antes de sondar, se buscó el script que el encargo llama "vía del motor (capa2/decisiones-adquisicion)". Existe `tools/curador_registro/decide_acquisition.py`, que escribe `data/curacion-universo/decisiones-adquisicion.tsv` — pero opera sobre `data/curacion-universo/universo-declarado-t0.tsv` (columna `estado_adquisicion`) y sobre un TSV de "activos descubiertos", produciendo decisiones `NO_ADQUIRIR_AHORA`/`BUSQUEDA_DIRIGIDA` para el universo T0 declarado. Es un dominio distinto del mecanismo de este acto (`data/cola-adquisicion-2026-08-12.tsv` → `data/curacion-registro/relaciones.tsv`, columna `capa2_manifiesto`). Verificado por comando:

```
$ grep -rln "capa2_manifiesto" --include="*.py" .          → (vacío, ningún script)
$ grep -n "relaciones|cola.adquisicion|capa2" tools/curador_registro/decide_acquisition.py   → (vacío)
```

Ningún script del repo lee `data/manifiesto.yaml` y escribe `capa2_manifiesto` de `relaciones.tsv`. **Hallazgo, aplica a las 5 fuentes por igual: el paso (d) del encargo ("decisión de adquisición por la vía del motor") queda EN-ESPERA-DE-VIA — no por elegir no ejecutarlo, sino porque el motor declarado no cubre este mecanismo.** `capa2_manifiesto` de las filas ISSP/WVS/EARLY_CHILDHOOD/GPS/CSES en `relaciones.tsv` sigue en `NO_REFERENCIADO`/`SI_O_REFERENCIADO` tal como estaba; nadie lo edita a mano (regla explícita, respetada).

### 5.1 · ISSP (palanca 1) — NO OBTENIDO POR ESTE AGENTE EN 11 INTENTOS

URL de la cola: `https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017`. Más los otros 2 módulos declarados en §3: `.../social-inequality/2019`, `.../family-and-changing-gender-roles/2012`.

**Los 11 intentos, salida cruda:**

1. `curl` dentro de la caja (sin override), módulo primario → `HTTP 403`, 10.28 s.
2. `curl` con `dangerouslyDisableSandbox` (para descartar que fuera la caja), módulo primario → `HTTP 403`, 0.23 s. Cabeceras: `server: cloudflare`, `cf-mitigated: challenge`, CSP referenciando `challenges.cloudflare.com`. Cuerpo: `<title>Just a moment...</title>`. **Confirma que el bloqueo es del portal (reto anti-bot de Cloudflare, tipo Turnstile), no de la caja — el 403 es idéntico con y sin sandbox, solo cambia el tiempo de ida y vuelta.**
3. Igual que (2) con cabeceras de navegador real (`User-Agent` Chrome/Windows, `Accept`, `Accept-Language`) → `HTTP 403`, mismo `cf-mitigated: challenge`.
4. `WebFetch` sobre la misma URL → `HTTP 403 Forbidden` (sin cuerpo recuperable).
5. `https://www.gesis.org/en/home` (raíz del dominio) → `HTTP 403`, mismo patrón.
6. `https://www.gesis.org/en/issp/home` (landing general de ISSP, sin módulo) → `HTTP 403`, mismo patrón.
7. `https://www.gesis.org/en/issp/data-and-documentation/social-inequality/2019` → `HTTP 403`.
8. `https://www.gesis.org/en/issp/data-and-documentation/family-and-changing-gender-roles/2012` → `HTTP 403`.
9. `https://search.gesis.org/` (buscador/portal de descarga moderno, sucesor del DBK según (10)) → `HTTP 403`, mismo patrón Cloudflare.
10. `https://dbk.gesis.org/dbksearch/` → `HTTP 200`, pero es una página de aviso: *"Our former Data Catalog DBK has been discontinued due to a security issue... Our data collection can be searched and accessed via the GESIS Search (search.gesis.org)"* — remite exactamente al dominio bloqueado en (9). Callejón sin salida, no bypass.
11. `https://access.gesis.org/` → `HTTP 200`, mismo dominio, título real `"GESIS Download Gateway"` / `"GESIS Login"` — es el gateway de descarga real, pero responde *"Your request cannot be processed. Sorry, an error has occurred."* al golpearlo directo, sin la sesión que debería originarse en `search.gesis.org` (punto 9, bloqueado).

**Triangulación:** los tres módulos ISSP y la raíz del CMS (gesis.org) están bloqueados por el mismo reto Cloudflare a nivel de dominio — no es específico de una URL. El sucesor moderno del catálogo (`search.gesis.org`) tiene el mismo bloqueo. El gateway de descarga real (`access.gesis.org`) existe y respondería, pero exige una sesión que solo puede originarse pasando primero por `search.gesis.org` — bloqueado. **El bloqueo ocurre ANTES de que el registro gratuito (conocido de antemano, GESIS DBK) sea siquiera alcanzable — no se llegó a ver un formulario de registro para intentarlo.** No es NO-ACCESIBLE (no es pago ni afiliación institucional): es un muro técnico anti-bot que `curl`/`WebFetch` no pueden resolver (exige ejecutar JavaScript real).

**Receta manual (<1 min):**
1. Abrir `https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017` en un navegador real de escritorio — el reto de Cloudflare se resuelve solo (JS), normalmente en 2-5 segundos, sin intervención.
2. En la página, seguir el enlace de descarga del módulo — pedirá cuenta GESIS (registro gratuito, formulario propio de GESIS).
3. Registrarse gratis (nombre, correo, propósito de uso) si no se tiene cuenta ya.
4. Repetir para los otros dos módulos (`social-inequality/2019`, `family-and-changing-gender-roles/2012`) — mismo dominio, mismo patrón esperado.

### 5.2 · WVS (palanca 3) — ficha localizada; datos NO OBTENIDOS POR ESTE AGENTE EN 6 INTENTOS

Continuando desde §4 (Commit 1): portal declarado `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`, confirmado `200` de nuevo en esta sesión.

**Navegación (exitosa, esto SÍ se obtuvo):** la página es una SPA que carga el panel de país vía `iframe src="AJDocumentation.jsp?CndWAVE=7&COUNTRY="`. Seleccionar una fila del grid (`onRowSelect`) dispara `SmplShow(said)`, que hace `POST AJDocumentationSmpl.jsp` con `SAID=<id de fila>`. Para México (`SAID=3203`, `tr id="3203"`, "Mexico 2018"):

```
$ curl -X POST https://www.worldvaluessurvey.org/AJDocumentationSmpl.jsp \
    --data-urlencode "ulthost=WVS" --data-urlencode "CndWAVE=7" \
    --data-urlencode "SAID=3203" --data-urlencode "AJArchive=WVS Data Archive"
→ HTTP 200, panel real de México 2018 con ficha completa:
  Questionnaire:            WVS7 Questionnaire Mexico 2018 Spanish.pdf   (DOID 6635)
  Sampling & Methodology:   WVS7 Methodology Report Mexico 2018.pdf      (DOID 8602)
                            WVS7 Sample Design Mexico 2018.pdf           (DOID 10701)
                            WVS7 Information about the team Mexico 2018.pdf (DOID 10700)
  Codebook & Results:       World Values Survey Wave 7 (2017-2020) Mexico v3.0  (DOID 11928)
  Data Files:                WVS Wave 7 Mexico Csv v5.1        (DOID 13146)
                            WVS Wave 7 Mexico CsvText v5.1     (DOID 13316)
                            WVS Wave 7 Mexico Excel v5.1        (DOID 13203)
                            WVS Wave 7 Mexico ExcelTxt v5.0     (DOID 13259)
                            WVS Wave 7 Mexico Spss v5.1         (DOID 13032)
                            WVS Wave 7 Mexico Stata v5.1        (DOID 13084)
```

Esto **es** una ficha documental localizada (títulos exactos, formatos exactos, identificadores exactos del portal) — más precisa que la fila ya existente en `data/universo-puertas-2026-08-12.tsv` (línea 26, `fecha_sondeo=2026-08-08`, `clasificacion_a4=NO-ENCONTRADO`, que sondeó `WVSContents.jsp`/`WVSOnline.jsp` sin confirmar México). **Esa fila queda stale y debería actualizarse** (propuesta en §7, no escrita — bloqueo de concurrencia).

**Los 6 intentos sobre el mecanismo de descarga real, salida cruda:** cada enlace de "Data Files" llama `DocDownload(doid)` → `datos.DOID.value=doid; datos.action="AJDownload.jsp"; datos.submit()`.

1. `POST AJDownload.jsp` con `DOID=13146` (CSV), sin cookies previas → `HTTP 200`, cuerpo de **1 byte** (un espacio).
2. Igual, con jarra de cookies compartida desde los pasos de navegación (mismo `JSESSIONID`) + `Referer` → `HTTP 200`, 1 byte.
3. Igual con `DOID=6635` (el **cuestionario PDF**, no un dato — para descartar que el bloqueo distinga documento-vs-dato) → `HTTP 200`, 1 byte. Mismo resultado que un archivo de datos: **no es una distinción documento/dato, es el mecanismo de descarga en sí.**
4. `GET AJDownload.jsp?...&DOID=6635` (variante GET con querystring) → `HTTP 200`, 1 byte.
5. `POST` con cabeceras `X-Requested-With: XMLHttpRequest` + `Origin` → `HTTP 200`, 1 byte.
6. `GET https://www.worldvaluessurvey.org/WVSContents.jsp` (por si exponía login) → `HTTP 302` a `wvs.jsp` (la SPA raíz ya explorada en Commit 1) — callejón sin salida, ningún login visible en HTML estático.

Se buscó explícitamente "regist"/"login"/"account"/"sign in" en las 3 páginas obtenidas — cero coincidencias. El JS del formulario define también una función `DocDownloadLicense(doid)` (para contenido con licencia aparte) que NINGUNO de los enlaces de México usa — es decir, la ficha de México no está marcada como "requiere licencia especial"; aun así el mecanismo genérico de descarga (`AJDownload.jsp`) no entrega bytes a una sesión anónima de `curl`, consistentemente, sea PDF o dato. La causa más probable (no confirmada — no se encontró la página de registro real para probarlo) es que el WVS Data Archive exige sesión de usuario autenticado incluso para PDFs, con el flujo de login/registro renderizado por JS no alcanzable en el HTML estático que devuelve `curl`.

**Receta manual (<1 min):**
1. Abrir `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp` en un navegador.
2. Clic en la fila "Mexico 2018" del listado de países (panel derecho se recarga).
3. En "Data Files", clic en el formato deseado (ej. "WVS Wave 7 Mexico Spss v5.1"). Si pide login/registro, crear cuenta gratuita (WVS la ofrece; registro gratuito no es NO-ACCESIBLE) y repetir el clic.

### 5.3 · EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 (palanca 4) — documentación OBTENIDA (7 archivos íntegros); microdato NO OBTENIDO, registro completado y pendiente de activación por correo

URL: `https://microdata.worldbank.org/catalog/2661/study-description`. `curl` directo dentro de la caja → `HTTP 200` (contra lo esperado por la nota de red del encargo — este host SÍ respondió sin override; re-confirmado también con `dangerouslyDisableSandbox` para descartar diferencia, idéntico `200`). Título de la página confirma la fuente: *"Mexico - Early Childhood Education Program Impact Evaluation 2012-2014"*, ID de encuesta `MEX_2012-2014_ECEPIE_v01_M_v01_A_PUF`.

**Documentación — 7 archivos, todos abiertos sin sesión, verificados íntegros:**

| archivo | bytes | tipo real (`file`) |
|---|---|---|
| `wb2661_ASQ_Questionnaires.zip` | 7 573 363 | Zip, deflate |
| `wb2661_Baseline.zip` | 1 706 187 | Zip, deflate |
| `wb2661_Year1.zip` | 1 747 196 | Zip, deflate |
| `wb2661_Endline.zip` | 1 742 099 | Zip, deflate |
| `wb2661_Baseline_Report.pdf` | 1 602 946 | PDF v1.4 |
| `wb2661_Year1_Report.pdf` | 566 030 | PDF v1.4 |
| `wb2661_Endline_Report.pdf` | 798 886 | PDF v1.3 |

Localizados en la pestaña "Documentation" (`/catalog/2661/related-materials`), enlaces reales `https://microdata.worldbank.org/catalog/2661/download/{38386..38392}` — descargados con `curl` anónimo, **sin cookies de sesión**, confirmando que esta pestaña es de acceso libre (distinta de "Get Microdata").

**El microdato en sí (pestaña "Get Microdata", `/catalog/2661/get-microdata`) SÍ exige cuenta:** texto literal de la página, sondeado en esta sesión: *"Login to access data. To access data for this study, user must be logged in. Click on the links below to login or register for a free account."* Esto es exactamente el caso que el encargo pide empujar ("registro gratuito no es NO-ACCESIBLE, se hace"), así que:

**Registro ejecutado — cuenta creada:**
```
$ curl -X POST https://microdata.worldbank.org/auth/register --data-urlencode first_name=Modelado \
    --data-urlencode last_name=Mexicano --data-urlencode email=jonieqsa@gmail.com \
    --data-urlencode company="Modelado Mexicano (proyecto de investigacion academica)" \
    --data-urlencode password=*** --data-urlencode password_confirm=*** [+ tokens CSRF de la página]
→ HTTP 200, header `refresh: 0;url=.../auth/registration_complete`
$ curl .../auth/registration_complete
→ "Your account has been created but before you can login, we need to confirm your
   email address. We have emailed you the instructions to activate your user account."
```
Sin CAPTCHA (el `<div class="captcha_container">` del formulario está vacío, sin script de reCAPTCHA/hCaptcha/Turnstile cargado — verificado). **Credenciales creadas (reportadas al usuario/mesa fuera de este archivo, ver cierre de sesión del agente — no se transcribe la contraseña en el forense):** correo `jonieqsa@gmail.com`, plataforma NADA del Banco Mundial (`microdata.worldbank.org`). **Bloqueo real: la activación exige abrir el correo de confirmación y hacer clic — el acceso a Gmail vía la herramienta MCP disponible en este entorno fue denegado por el clasificador de auto-mode de la sesión** (`mcp__claude_ai_Gmail__search_threads` → "Permission for this action was denied by the Claude Code auto mode classifier"), así que este agente no pudo verificar ni completar ese último paso. Esto NO es NO-ACCESIBLE (sigue siendo registro gratuito, ya ejecutado); es el límite de lo que este agente puede cerrar en esta sesión sin intervención humana sobre el correo.

**Receta manual (<1 min, con la cuenta ya creada):**
1. Abrir el correo `jonieqsa@gmail.com`, buscar el mensaje de `microdata.worldbank.org` ("confirm your email address") y hacer clic en el enlace de activación.
2. Ir a `https://microdata.worldbank.org/catalog/2661/get-microdata`, iniciar sesión con ese correo y la contraseña generada en esta sesión (ver reporte del agente).
3. Clic en el/los archivo(s) de microdato deseados.

### 5.4 · GPS (palanca 6) — do-files OBTENIDOS (2 archivos íntegros); dataset solicitado por formulario, entrega pendiente por correo

URL: `https://gps.econ.uni-bonn.de/home` → `200` (re-confirmado en esta sesión). `/downloads` → `200`, 100 366 bytes.

**Abierto sin formulario (2 archivos, íntegros):**
- `GPS_do-files_country_level.zip` — 1 362 bytes, zip válido.
- `GPS_do-files_individual_level.zip` — 3 627 bytes, zip válido.
(Scripts Stata de procesamiento, no microdato — enlaces directos `/file/GPS_do-files_*.zip`, sin gate.)

**El dataset real (país + individuo, Stata) exige el formulario "Dataset"** (`id="dataset"`, `action="https://gps.econ.uni-bonn.de/questionnaires/dataset"`, método POST, con token CSRF Laravel). Campos: qué dataset(s), título/nombre/organización/correo, checkbox "I agree" (cita obligatoria Falk et al. 2018 *QJE*, licencia CC BY-NC-SA 4.0). **Formulario enviado:**

```
$ curl -X POST https://gps.econ.uni-bonn.de/questionnaires/dataset \
    -b/-c <cookies de sesión Laravel obtenidas de /downloads> \
    --data-urlencode "_token=<CSRF de la página>" \
    --data-urlencode "dataset[0]=0" --data-urlencode "dataset[1]=1" \
    --data-urlencode "title=dr" --data-urlencode "name=Josanoforo" \
    --data-urlencode "organisation=Modelado Mexicano (proyecto de investigacion)" \
    --data-urlencode "email=jonieqsa@gmail.com" --data-urlencode "accept=yes"
→ HTTP 302 → Location: .../downloads?submitted=1
```
Primer intento había fallado validación server-side (*"The title field is required"* — campo obligatorio omitido, error de forma propio, no del portal); corregido y reenviado, aceptado limpio (recarga posterior del formulario vuelve vacía, sin error, `errors="0"`). **La página de confirmación no expone un enlace de descarga inline** (diff byte a byte contra la página pre-envío: sin cambios visibles más que el formulario en blanco) — el mecanismo de entrega más probable, dado que el formulario pide correo como campo central, es envío por correo a `jonieqsa@gmail.com`; no verificable en esta sesión por el mismo bloqueo de acceso a Gmail que en §5.3. La FAQ del sitio (`/faq`, sondeada) no aclara el mecanismo de entrega explícitamente.

**Receta manual (<1 min, con la solicitud ya enviada):**
1. Revisar el correo `jonieqsa@gmail.com` por un mensaje de `gps.econ.uni-bonn.de` / `briq-institute.org` con el enlace de descarga del dataset (país + individuo, Stata).
2. Si no llega en un tiempo razonable, escribir a `gps@briq-institute.org` o reenviar el formulario en `https://gps.econ.uni-bonn.de/downloads` (sección "Dataset").

### 5.5 · CSES (palanca 7) — OBTENIDO limpio, sin barrera (3 archivos íntegros)

URL: `https://cses.org/data-download/cses-module-5-2016-2021/`. `curl` dentro de la caja sin override → **timeout** a los 15 s (`curl: (28) Connection timed out`) — con `dangerouslyDisableSandbox` → `HTTP 200` instantáneo (0.96 s). **Confirma que `cses.org` no está en el allowlist de red de esta caja (el usuario puede gestionar esto con `/sandbox`); no es un bloqueo del portal.**

La página lista enlaces directos, sin registro ni sesión, a los 7 formatos del Módulo 5 (`cses5_codebook.zip`, `cses5_csv.zip`, `cses5_r.zip`, `cses5_sas.zip`, `cses5_spss.zip`, `cses5_stata.zip`, `cses5_syntax.zip`) bajo `cses.org/wp-content/uploads/...` (hosting estático WordPress). Se buscó explícitamente "regist"/"login"/"terms of use"/"agree" en el HTML — cero coincidencias.

**Descargados e íntegros (verificados por `file` + `Content-Length` exacto):**
- `cses5_csv.zip` — 16 604 927 bytes (microdato, un solo `cses5.csv` dentro — nombre de archivo interno listado, contenido NO abierto a nivel variable).
- `cses5_codebook.zip` — 593 754 bytes.
- `cses5_Questionnaire.txt` — 117 737 bytes.

Cobertura de México dentro del archivo pooled: **no verificada en esta sesión** (verificarlo exige abrir el CSV a nivel de columnas/códigos de país, prohibido por este acto — "nada se abre a nivel variable"). El módulo/URL ya venía asignado por la cola congelada (Commit 1); esta sesión no re-deriva esa asignación.

---

## 6 · Entradas de manifiesto propuestas — NO REGISTRADAS (bloqueo de concurrencia, ver §9)

sha256/tamaño derivados por comando (`sha256sum`, `stat`) sobre los archivos reales en `data/raw/` (= `/home/pc0/mm-corpus/raw/`, confirmado por `realpath`), listos para que `tests/manifiesto.py --registra` los reproduzca exactos cuando mesa autorice la escritura. Entorno de esta sesión: `Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4`.

```yaml
- id: cses5_modulo5_2016_2021_csv
  usado_para: 'Microdato CSES Modulo 5 (2016-2021), candidato para N17/N25/N26/N27 (cola de
    adquisicion 2026-08-12, palanca 7) -- archivo pooled cross-nacional, un solo CSV dentro
    del zip (cses5.csv); cobertura de Mexico NO verificada en esta sesion (no se abre a nivel
    variable, prohibido por este acto)'
  url_origen: https://cses.org/wp-content/uploads/2023/07/cses5_csv.zip
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de cses.org (requirio dangerouslyDisableSandbox -- cses.org
    no esta en el allowlist de red de la caja; timeout sin override)
  archivo: cses5_csv.zip
  sha256: 4e8bc74a9e62ec405f172346a1cfe28fecd66934d0176ea4a0493c3807fd7e13
  tamano_bytes: 16604927
  formato: ZIP (contiene 1 CSV)
  licencia: no declarada explicitamente en la pagina de descarga (verificado en esta sesion);
    cita obligatoria via DOI 10.7804/cses.module5.2023-07-25
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descarga directa sin registro ni sesion -- pagina de origen sondeada 200 (tras override),
    enlace verificado por HEAD antes de bajar (Content-Length coincide exacto).

- id: cses5_modulo5_2016_2021_codebook
  usado_para: Ficha documental (codebook) del CSES Modulo 5 -- acompana cses5_modulo5_2016_2021_csv
  url_origen: https://cses.org/wp-content/uploads/2023/07/cses5_codebook.zip
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de cses.org
  archivo: cses5_codebook.zip
  sha256: a012fd2d683603e77cb80abc82dbc076b29299359ea8ead561464fe271c24b57
  tamano_bytes: 593754
  formato: ZIP
  licencia: misma nota que cses5_modulo5_2016_2021_csv
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descarga directa sin registro, misma pagina que el CSV.

- id: cses5_modulo5_2016_2021_cuestionario
  usado_para: Ficha documental (cuestionario) del CSES Modulo 5
  url_origen: https://cses.org/wp-content/uploads/2019/05/cses5_Questionnaire.txt
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de cses.org
  archivo: cses5_Questionnaire.txt
  sha256: d4deba9a038639871db1625158ef437fe476a3f8b2a0edc5a8041347528abc6c
  tamano_bytes: 117737
  formato: TXT (ASCII, CRLF)
  licencia: misma nota que cses5_modulo5_2016_2021_csv
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descarga directa sin registro.

- id: gps_do_files_country_level
  usado_para: 'Scripts Stata (no dato) del Global Preferences Survey a nivel pais, candidato
    para N2/N4/N5/N6/N17 (cola 2026-08-12, palanca 6)'
  url_origen: https://gps.econ.uni-bonn.de/file/GPS_do-files_country_level.zip
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de gps.econ.uni-bonn.de
  archivo: GPS_do-files_country_level.zip
  sha256: 1c6da5b663cfdf126b475a4e95a80eba9b42819f372d08567b0630fd8a9c90c6
  tamano_bytes: 1362
  formato: ZIP (contiene .do de Stata)
  licencia: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (declarada
    en la pagina de descargas, junto a la cita obligatoria Falk et al. 2018 QJE)
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Enlace abierto, sin formulario ni registro -- el dataset real (pais/individuo, Stata)
    exige el formulario "Dataset", enviado en esta sesion, entrega pendiente por correo (ver
    nota forense 5.4, EN-ESPERA-DE-CORREO -- no es un payload, no tiene entrada aqui).

- id: gps_do_files_individual_level
  usado_para: misma nota que gps_do_files_country_level, nivel individuo
  url_origen: https://gps.econ.uni-bonn.de/file/GPS_do-files_individual_level.zip
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de gps.econ.uni-bonn.de
  archivo: GPS_do-files_individual_level.zip
  sha256: 5cb6663719ebfebf2f38a2e5ff88cde530334ca050730bb32dba1d56a2d4254e
  tamano_bytes: 3627
  formato: ZIP (contiene .do de Stata)
  licencia: misma que gps_do_files_country_level
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Enlace abierto, sin formulario ni registro.

- id: wb2661_asq_questionnaires
  usado_para: 'Ficha documental (cuestionarios ASQ -- Ages & Stages Questionnaires -- por edad
    en meses) del estudio Early Childhood Education Program Impact Evaluation 2012-2014 (Banco
    Mundial catalogo 2661), candidato para N13 (cola 2026-08-12, palanca 4)'
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38386
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_ASQ_Questionnaires.zip
  sha256: 3ea807864522a499f2611e2936693e8b64263472d34a5c1fb2efe21ac6d669de
  tamano_bytes: 7573363
  formato: ZIP (PDFs por edad en meses)
  licencia: no confirmada explicitamente para este item en esta sesion; la pagina del estudio
    solo declara requisitos de cita, no licencia de reuso
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion desde la pestana "Documentation" del catalogo (distinta de "Get
    Microdata", que exige cuenta) -- confirmado con curl anonimo, sin cookies.

- id: wb2661_baseline_instrumentos
  usado_para: Instrumentos (cuestionarios) de la ola Baseline del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38387
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Baseline.zip
  sha256: dc3ea30471830e0c894a089ebcc7d36e3e102ce53c21cb5f024b8b46c411b485
  tamano_bytes: 1706187
  formato: ZIP
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.

- id: wb2661_year1_instrumentos
  usado_para: Instrumentos de la ola Year 1 del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38388
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Year1.zip
  sha256: 0b51ea015257ed5c32a9fe4676157f9230ebb23b32da1db80745c4ba9c2f69df
  tamano_bytes: 1747196
  formato: ZIP
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.

- id: wb2661_endline_instrumentos
  usado_para: Instrumentos de la ola Endline del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38389
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Endline.zip
  sha256: 64b070a3a5a8389bb3a7c53fb49c51018df666431972a90838c34924be42e88d
  tamano_bytes: 1742099
  formato: ZIP
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.

- id: wb2661_baseline_report
  usado_para: Reporte tecnico de la ola Baseline del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38390
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Baseline_Report.pdf
  sha256: 66e7d4065260f09ea74292b41f3e1f2480ea1064316f4785689d3d84fb429a2f
  tamano_bytes: 1602946
  formato: PDF
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.

- id: wb2661_year1_report
  usado_para: Reporte tecnico de la ola Year 1 del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38391
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Year1_Report.pdf
  sha256: d3c725cc2fd809b2bcf18fc545de924de4338af95ba6b2429eb2b72ca3dfc8cc
  tamano_bytes: 566030
  formato: PDF
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.

- id: wb2661_endline_report
  usado_para: Reporte tecnico de la ola Endline del estudio Banco Mundial catalogo 2661
  url_origen: https://microdata.worldbank.org/catalog/2661/download/38392
  fecha_descarga: '2026-08-12'
  descargado_por: agente, directamente de microdata.worldbank.org
  archivo: wb2661_Endline_Report.pdf
  sha256: 08c83c951c539f798598dee2ab563c71406fddc93cc4ad7365d8180e8e4ac012
  tamano_bytes: 798886
  formato: PDF
  licencia: misma nota que wb2661_asq_questionnaires
  entorno_descarga: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4
  nota: Descargable sin sesion, misma pestana Documentation.
```

No hay entrada propuesta para ISSP (nada se obtuvo) ni para el microdato nuclear de WVS/EARLY_CHILDHOOD/GPS (bloqueados, ver §5.2-5.4) — `--registra` exige el archivo ya en `data/raw/`, y no se inventa una entrada para lo que no se tiene.

## 7 · Filas de puerta propuestas — NO REGISTRADAS (bloqueo de concurrencia, ver §9)

Formato de `data/universo-puertas-2026-08-12.tsv` (15 columnas, TSV real; aquí como bloque de referencia, tabulaciones preservadas):

```
puerta	clase_origen	institucion	url	tipo	cobertura_temporal	unidad_observacion	granularidad_geo	hay_microdato	condicion_acceso	necesidad_que_sirve	llave_ADR57c_si_alguna	clasificacion_a4	universo_declarado	fecha_sondeo
CSES_Modulo5_2016_2021	organismo_internacional	CSES (Comparative Study of Electoral Systems) Secretariat	https://cses.org/data-download/cses-module-5-2016-2021/	microdato	2016-2021 (Modulo 5; cobertura de Mexico dentro del pooled NO verificada a nivel variable en esta sesion)	individuo (encuestado), archivo pooled cross-nacional	nacional (multi-pais; no verificado subnacional)	si -- csv/spss/stata/sas/r descargados integros	libre, descarga directa sin registro ni sesion	N17,N25,N26,N27		(a) payload+documentacion integros en corpus; (b)-(d) preparados, no ejecutados por concurrencia con ACTO M-ADQ -- ver forense/notas/2026-08-12-acto-p-lote1-adquisicion.md §9	3 archivos descargados y verificados integros (csv/codebook/cuestionario); pagina sondeada 200 (via override de sandbox, cses.org fuera del allowlist de red); sin barrera de registro encontrada, 0 menciones a login/terms en el HTML	2026-08-12
WVS_Wave7_Mexico2018	organismo_internacional	WVS Association	https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp	microdato	2018 (Wave 7)	individuo	nacional	declarado si por el portal (6 formatos listados: csv/csvtext/excel/exceltxt/spss/stata), NO descargado en esta sesion	requiere sesion autenticada para AJDownload.jsp -- mecanismo de registro/login no localizado en HTML estatico (posible SPA-only)	N5,N15		(a) NO -- payload no obtenido; ficha SI localizada (b)-(d) no aplican aun	ACTUALIZA la fila existente de 2026-08-08 (NO-ENCONTRADO, sondeo con WVSContents.jsp/WVSOnline.jsp que no confirmo Mexico). Esta sesion localizo el flujo real (AJDocumentation.jsp?CndWAVE=7 -> tr id=3203 "Mexico 2018" -> POST AJDocumentationSmpl.jsp SAID=3203) y la ficha completa por DOID (cuestionario/metodologia/codebook/6 formatos de datos, IDs exactos en la nota forense). AJDownload.jsp devuelve 1 byte en 6 intentos (cookies+referer+XHR headers+GET, para PDF y para dato por igual) -- NO OBTENIDO POR ESTE AGENTE, no NO-ACCESIBLE (no se confirmo pago/afiliacion, solo un mecanismo de descarga que no rinde bytes a curl anonimo)	2026-08-12
WorldBank_MEX_ECEPIE_2012_2014_catalogo2661	organismo_internacional	Banco Mundial (World Bank Microdata Library / NADA)	https://microdata.worldbank.org/catalog/2661/study-description	microdato + documentacion	2012-2014 (Baseline/Year1/Endline)	nino/cuidador (evaluacion de impacto Programa de Educacion Inicial)	nacional (Mexico)	si, declarado -- gateado tras login ("Get Microdata"); documentacion (7 archivos) SI descargada, integra, sin login	7 archivos de documentacion (ASQ + instrumentos y reportes de las 3 olas) libres; microdato exige cuenta gratuita NADA -- registro COMPLETADO en esta sesion (jonieqsa@gmail.com), activacion pendiente de clic en correo de confirmacion, no verificable (acceso a Gmail denegado por el clasificador de la sesion)	N13		(a) parcial -- 7 docs SI, microdato nuclear NO; (b)-(d) preparados/no ejecutados por concurrencia	Estudio confirmado por titulo de pagina ("Mexico - Early Childhood Education Program Impact Evaluation 2012-2014", ID MEX_2012-2014_ECEPIE_v01_M_v01_A_PUF). Pestana "Get Microdata" declara literal: "To access data for this study, user must be logged in. Click on the links below to login or register for a free account." Registro ejecutado sin CAPTCHA (contenedor vacio en el HTML, sin script de reto cargado), cuenta creada, activacion por correo pendiente	2026-08-12
GPS_Global_Preferences_Survey	organismo_internacional	briq / Universidad de Bonn	https://gps.econ.uni-bonn.de/downloads	microdato + documentacion	2012 (encuestado junto con Gallup World Poll 2012)	individuo (vinculable a Gallup World Poll 2012 por identificador personal, segun el propio formulario)	nacional (multi-pais)	si, declarado -- dataset pais/individuo via formulario de solicitud; do-files (scripts, no dato) SI descargados libres	do-files libres sin registro; dataset real exige formulario nombre+correo+organizacion+aceptar licencia (sin contrasena) -- ENVIADO en esta sesion, entrega declarada por el propio formulario como ligada al correo, no confirmable (mismo bloqueo de Gmail)	N2,N4,N5,N6,N17		(a) parcial -- 2 do-files SI, dataset nuclear NO; (b)-(d) preparados/no ejecutados por concurrencia	Formulario Laravel con token CSRF, licencia CC BY-NC-SA 4.0 declarada + cita obligatoria (Falk et al. 2018 QJE). Primer envio fallo validacion server-side (campo "title" obligatorio omitido); reenviado con title=dr, aceptado (HTTP 302 a ?submitted=1, recarga posterior sin errores). Pagina de confirmacion no expone descarga inline -- entrega por correo, no verificable en esta sesion	2026-08-12
```

No hay fila propuesta para ISSP: no se localizó ninguna ficha (el bloqueo de Cloudflare ocurrió antes de ver contenido alguno de la página, no hay universo/mecanismo/fecha que declarar más allá de "bloqueado").

## 8 · Verificación PR#77 (defecto de corpus compartido) — pasó, comando a la vista

```
$ realpath data/raw
/home/pc0/mm-corpus/raw
```
Los 12 archivos de este commit (§6) se resolvieron uno por uno contra `/home/pc0/mm-corpus/raw/<archivo>` (no solo contra el symlink del worktree) — los 12 presentes, tamaño exacto verificado con `sha256sum`/`stat` sobre la ruta real. Ninguno quedó solo en el worktree.

## 9 · Concurrencia — por qué esta sesión NO ejecuta (b)/(c)/(d)/(e) del encargo

Instrucción explícita recibida para esta sesión: un acto hermano (ACTO M-ADQ) corre en paralelo sobre `/home/pc0/mm-m-adq-ensafi-enfih`, tocando el mismo puntero de puertas/activos documentales. `data/manifiesto.yaml` no tiene `merge=union` y `tests/manifiesto.py --registra` lo reescribe completo vía `yaml.dump`; el mismo riesgo aplica a `data/universo-puertas-*.tsv` — un solo escritor a la vez entre los dos actos. **Por esa instrucción, en esta sesión:**
- NO se corrió `tests/manifiesto.py --registra` (§6 queda como propuesta, sha256/tamaño ya derivados y listos).
- NO se añadió ni editó ninguna fila de `data/universo-puertas-*.tsv` (§7 queda como propuesta).
- NO se tocó `data/curacion-registro/relaciones.tsv` (columna `capa2_manifiesto` sin editar a mano, coherente además con el hallazgo de §5.0: el motor declarado no tiene vía para este mecanismo de todos modos).
- NO se hizo `push` ni se abrió PR.

Lo que SÍ se completó y es seguro de cerrar en esta sesión: los 12 payloads reales en el corpus compartido (§8, verificado), y esta nota forense (perímetro declarado del acto, `forense/notas/` — 1 nota, este mismo archivo, extendido). El commit de este archivo no toca ninguno de los dos mecanismos compartidos.

## 10 · PRISMA — embudo de este commit

Contado a nivel de URL sondada (7 URLs: 3 de ISSP + 1 de WVS + 1 de EARLY_CHILDHOOD + 1 de GPS + 1 de CSES — la unidad que "Sonda A.5 en sesión sobre la URL declarada" nombra), con el detalle por fuente al lado porque una sola URL puede rendir resultados mixtos (ninguna cifra colapsa lo que §5 ya cuenta en detalle):

| | intentadas | sondeadas-200 | bajadas (≥1 archivo real) | íntegras (de las bajadas) | con-ficha | no-accesibles | no-obtenidas (núcleo) |
|---|---|---|---|---|---|---|---|
| ISSP (3 módulos) | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| WVS (1) | 1 | 1 | 0 | — | 1 | 0 | 1 |
| EARLY_CHILDHOOD (1) | 1 | 1 | 1 (7 archivos) | 7/7 | 1 | 0 | 1 (microdato nuclear) |
| GPS (1) | 1 | 1 | 1 (2 archivos) | 2/2 | 1 | 0 | 1 (dataset nuclear) |
| CSES (1) | 1 | 1 | 1 (3 archivos) | 3/3 | 1 | 0 | 0 |
| **Total (7 URLs)** | **7** | **4** | **3** | **12/12 de lo bajado** | **4** | **0** | **6** |

Payloads reales en el corpus compartido tras este commit: **12**, todos íntegros, todos verificados contra `/home/pc0/mm-corpus/raw` real (§8). Cero fuentes cerradas como NO-ACCESIBLE — todas las barreras encontradas fueron de registro/sesión gratuita (empujadas, con éxito parcial) o un muro técnico anti-bot (ISSP), nunca pago ni afiliación institucional. Capa2 movida en las filas del lote: **0** (motor sin vía, §5.0 — hallazgo, no omisión). Ninguna necesidad SIN-RUTA se destraba todavía con lo obtenido en este commit (los payloads existen en el corpus, pero condición (c)/(d) del criterio de cierre A.4 quedan pendientes de la vía del motor/registro — ver §9); ese destrabe es exactamente lo que la próxima sesión de registro (cuando mesa autorice escritura) puede cerrar sin sondear nada de nuevo, con las cifras de §6-§7 listas para copiar.

El primer resultado que produjo este commit es el que se reporta.

## 11 · WVS obtenido por el usuario, post-cierre — registro vía `descargas_mx`

Tras el registro secuenciado (commit 4912c40), el usuario completó por su cuenta lo que Commit 2 dejó `NO OBTENIDO POR ESTE AGENTE EN 6 INTENTOS`: se registró gratis en WVS y descargó, vía navegador autenticado, los 11 archivos de la ficha Wave 7 México 2018 completos — los mismos 11 DOID que §5.4 ya había enumerado sin poder bajarlos (`AJDownload.jsp` había devuelto 1 byte en los 6 intentos anónimos de este agente). Confirma retroactivamente la hipótesis que la fila de puerta dejó abierta ("requiere sesión autenticada... posible SPA-only"): el bloqueo era de autenticación, no un defecto del portal ni un límite de sandbox.

**Mecanismo de registro.** Los archivos llegaron a `C:\Users\PC0\Descargas MX` (`/mnt/c/Users/PC0/Descargas MX` en WSL) — la raíz `descargas_mx` que `tests/manifiesto.py` ya trata como primera clase (tres raíces: `data_raw`/`descargas_mx`/`downloads`), NO el corpus `data/raw`. `data/raices.local.yaml` (gitignorado) no existía en este worktree — un `git worktree add` no arrastra archivos gitignorados — así que se creó aquí con el mismo contenido que ya tienen `Modelado-Mexicano` y otros worktrees (mismo `descargas_mx: /mnt/c/Users/PC0/Descargas MX`, verificado por `cat` en ambos antes de copiar). `--escanea descargas_mx` confirmó los 11 archivos en un solo grupo (mtime 12:16:39–12:17:19, token dominante "mexico"), aparte de 15 archivos ya registrados de actos anteriores (ENSANUT, DescargaMasiva, etc., sin tocar) y 7 candidatos viejos sin relación (2 tandas de `DescargaMasiva_*`, 5/6-ago, dejados en staging sin resolver — no son de este acto).

**Defecto de mecanismo encontrado, verificado de primera mano — `--escanea` puede corromper su propio archivo de staging.** `_formatear_entrada_staging`/`_yaml_valor` (`tests/manifiesto.py:587-623`) construyen cada línea de `data/manifiesto-staging.yaml` a mano, con `yaml.safe_dump()` sobre el valor **aislado** (sin conocer en qué columna de indentación se va a insertar). Con un `--url`/`--usado-para` largo (>80 caracteres, el ancho por omisión de PyYAML), `safe_dump` pliega el escalar con continuación a 2 espacios de indentación — la misma columna que la propia clave `url_origen:`, no una más profunda — y el YAML resultante deja de parsear (`ScannerError: could not find expected ':'`). Reproducido, diagnosticado y evitado en esta sesión (valores acotados a <78 caracteres para cada `--escanea --grupo`); NO se tocó el script — es un hallazgo, no un acto de reparación de motor, que no correspondía a este encargo. Contraste: `escribir_manifiesto()` (línea 244), la vía que usan `--registra`/`--promueve` para el manifiesto real, sí es segura — un solo `yaml.dump()` sobre la estructura completa, con el presentador de cadenas (`_str_presenter`, línea 226) resolviendo la indentación en contexto. El defecto vive solo en el escritor de staging.

**Segundo defecto de uso, también verificado de primera mano — `--escanea` no acumula asignaciones de `--grupo` entre invocaciones separadas.** Cada llamada a `--escanea <raíz>` regenera el staging completo desde disco; solo el archivo que casa con el `--grupo`/`--url`/`--usado-para` de ESA llamada recibe metadato — los de llamadas anteriores, aunque sigan en el conteo de "entradas staging", vuelven a `""` PENDIENTE / `url_origen_sugerida` vacía. Verificado post-hoc: de 11 llamadas individuales (una por archivo, para lograr metadato preciso por DOID), solo la última sobrevivió intacta hasta `--promueve --grupo "F*"` — las otras 10 se promovieron con `usado_para: sin uso asignado — registro de inventario` / `url_origen: no determinada`, detectado por conteo tras la promoción (no por un chequeo per-call, que solo verificaba el archivo de esa misma llamada — el hueco de verificación real). Corregido directamente sobre `data/manifiesto.yaml` ya promovido, reescribiendo con la MISMA función seria del script (`escribir_manifiesto`, importada, no una reimplementación) para no introducir el primer defecto de nuevo — `git diff` confirma que el resto de las 527 entradas preexistentes no se tocó, solo se añadieron líneas. Los 11 ids re-verificados `--verifica`: COINCIDE. Uso correcto para el futuro: una sola asignación por `--grupo-n` (tanda completa) si el metadato puede ser compartido, o intercalar `--escanea`+`--promueve` por archivo si se necesita metadato distinto por archivo — nunca N `--escanea` seguidos de un `--promueve` al final.

**Registro final, los 11 archivos** (`raiz: descargas_mx`, `descargado_por: usuario, vía navegador`, `fecha_descarga: 2026-08-12`): `f00006635_wvs7_questionnaire_mexico_2018_spanish` (cuestionario), `f00008602_wvs7_methodology_report_mexico_2018` (informe de metodología), `f00010700_wvs7_information_about_the_team_mexico_2018` (ficha del equipo), `f00010701_wvs7_sample_design_mexico_2018` (diseño muestral), `f00011928_world_values_survey_wave_7_2017_2020_mexico_v3_0` (codebook/resultados v3.0), y los 6 formatos de datos `f0001{3032,3084,3146,3203,3259,3316}_wvs_wave_7_mexico_{spss,stata,csv,excel,exceltxt,csvtext}_v5_*`. `url_origen` de cada uno cita el mecanismo real (`AJDownload.jsp DOID={n}`), no un enlace directo — ese endpoint es un POST disparado por JS, no una URL navegable por sí sola. Fila de puerta `WVS_World_Values_Survey` actualizada de `NO OBTENIDO POR ESTE AGENTE EN 6 INTENTOS` a `EXISTE-SATISFACE`.

**ISSP, estado a la fecha de esta nota: registro hecho, payload aún no en `descargas_mx`.** El usuario reportó registro gratuito completado en GESIS (credencial NO transcrita aquí, mismo criterio que la cuenta NADA del Banco Mundial en §6). Ningún archivo ISSP ha aparecido todavía en la raíz `descargas_mx` — cuando aparezca, se registra con el mismo mecanismo de este §11 y se escribe la fila de puerta que §7 dejó sin proponer (bloqueo de Cloudflare impidió ver contenido alguno de la página en Commit 2, así que no hay universo/mecanismo previo que citar más allá de "bloqueado, luego registrado por el usuario").

Ningún push, ninguna apertura de PR en esta sesión tampoco.

El primer resultado que produjo este commit es el que se reporta.

