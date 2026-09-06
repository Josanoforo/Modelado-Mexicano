# `ACTO MAESTRA38-A4 · ADQUIERE-TODO-LO-PUBLICO` — COMMIT-2 · resultados por objetivo

6/sep/2026 · rama `acto/maestra38-a4-adquiere-todo-lo-publico` · base `origin/main` = `a5350e59` · corpus compartido `/home/pc0/mm-corpus/raw` · lista congelada en `forense/notas/2026-09-06-MAESTRA38-A4-spec.md`.

**Contador.** Objetivos obtenidos por caja: **0 → 25 de 33** (+ 4 fichas sin objeto adquirible, declaradas en el `COMMIT-1`). Payloads nuevos en el corpus compartido: **201 archivos, 5.39 GB**. Manifiesto **1 315 → 1 515** (+200; el 201.º, el bulk S3 de la PDN, **no** se re-registra: reprodujo el `sha256` de una entrada ya existente — ver §PDN). Cola: `OBTENIDO` **92 → 104**. Medición de modelo: **cero**, como el encargo declaró.

**Lo que va a `PAQUETE-RECETAS-10`: 5 objetos.** No 33. La firma de mesa era «lo que pueda bajar caja que lo baje caja, lo que no, dame las ligas» — caja bajó casi todo.

---

## 0 · Disciplina de red y de verificación, aplicada a los 33

- **A.7, doble descarga por DOS transportes distintos.** Cada objeto se bajó con `curl` y con `wget` por separado y sólo se depositó si el `sha256` del contenido coincidió entre las dos. Cuatro intentos con la misma herramienta no son cuatro rutas: por eso el par es curl+wget, no curl+curl.
- **Sonda antes que contenido.** `curl -r 0-0 -L` devuelve `Content-Range` con el tamaño total sin bajar el cuerpo; los 33 pasaron por ahí antes de que este acto pidiera un solo byte de contenido (tabla en el `COMMIT-1`).
- **Sandbox.** `https://www.inegi.org.mx/` da `000` dentro del sandbox de bash y `200` fuera. **Toda** descarga de este acto corrió fuera del sandbox. Un `000` medido dentro del sandbox no es un hecho sobre el portal.
- **`testzip`** sobre todo `.zip`/`.xlsx`: `None` (ningún CRC malo) en 100% de los casos.
- **Tres hallazgos distintos, nunca colapsados**: RED (`000`/timeout) · SERVIDOR (`4xx`/`5xx` con cuerpo) · VACÍO (`200` sin contenido útil: shell SPA, soft-404 de INEGI de 2 263 B, `Welcome to nginx`).

---

## 1 · Obtenidos (25 objetivos · 201 archivos)

| # | objetivo | qué llegó | bytes | verificación |
|---:|---|---|---:|---|
| 1-2 | `EARTHQUAKE_TRUST_LAPOP_2017` | `Final_dataset_Mexico_Earthquake.dta` + `Final_do_file_Mex_quake.do` | 674 621 · 44 712 | sha idéntico; abierto con `pandas.read_stata` → **1 733 × 67**, con la variable de tratamiento `Earthquake` |
| 3-5 | `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA` | 2 `xlsx` + 1 `csv` | 251 823 · 1 278 564 · 8 795 | los tres tamaños exactos de la receta; `testzip None`, 15 y 18 entradas |
| 6-7 | `EXT_OF_11_REUNE_REDECO` | REDECO 1T2026, REDECO 30/09/25 (**recurso extra hallado por la API CKAN, no estaba en la receta**), REUNE 31/03/26 | 678 710 · 673 104 · 4 482 648 | sha idéntico |
| 8-9 | `ENVIPE_EXTRACCION_TEXTO_REACTIVO` | XML DDI de ENVIPE 2025 (cat. 1130) y ENSU 2025 (cat. 1100) | 2 334 820 · 2 628 278 | sha idéntico; XML bien formado |
| 10 | `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` | `JEA_Elecciones_concurrentes.pdf` | 1 441 115 | tamaño exacto de la receta |
| 11-14 | `IETAM_TAMAULIPAS_SERIE_MUNICIPAL` | **46 archivos**: 2016 PDF, **43 xlsx de 2018**, 2021, 2024 | 3.8 MB | 46/46 sha idéntico, `testzip None` |
| 15 | `PRICE_AND_INFORMATION…` (hermana) | `MILK-RCT…pdf` | 1 111 333 | sha idéntico |
| 16 | `IEEPCO_OAXACA_SERIE_MUNICIPAL` | `ESTADISTICA_CONCEJALES_2016_IEEPCO.xlsx` | 968 301 | `testzip None`, 61 entradas — **con verificación TLS completa, sin `-k`** |
| 17-19 | `INEGI_CNGF` | 2 PDF + 1 XLSX | 2 014 714 · 1 075 400 · 195 845 | los tres muy por encima del soft-404 de 2 263 B |
| 20 | `EXT_OF_07…` (CompraNet) | `compranet_historico.csv` | **951 619 345** | sha idéntico entre curl y wget sobre 951 MB |
| 21 | DeclaraNet federal | **6 CSV, 2013-2018** | 261.1 MB | sha idéntico; encabezado real (`dependencia,nombre,fecha_envio,declaracion,…`) |
| 22 | `ENAFIN` (hermana WB) | cuestionario B-READY 2023 + Implementation Report | 1 041 388 · 602 312 | sha idéntico |
| 23 | `ICPSR35024` (parcial) | `35024-0001-Data_partial.tab` + codebook | 59 307 · 28 502 | sha idéntico |
| 24 | `LOS_MEXICANOS_VISTOS_POR_SI_MISMOS` | **113 archivos, 24 módulos** | 144.2 MB | 113/113 sha idéntico, 0 fallidos, **0 por espejo** |
| 25 | `ECOPRED_2014_INEGI` | `ecopred14_bd_dbf.zip` | 22 296 331 | `testzip None`, 10 entradas: 8 DBF + FD + cuestionarios |
| 27 | `PDN_SESNA_S1_S2_S3_S6` | **4 bulk** (S1, S2, S3, S6) + los 6 DeclaraNet de arriba | 3 975.1 MB | sha idéntico; `testzip None`; **control positivo contra `pdn_s3v2`** |
| 29 | `ENJUVE` (parcial) | 4 tabulados de 2005 vía espejo | 6.6 MB | sha idéntico |
| 31 | `CULTURA_CONSTITUCIONAL_UNAM_IIJ` | microdato `csv`/`dta`/`sav` + cuestionario + metodología + libro | 6.9 MB | sha idéntico |
| 32 | `ENFIH 2019` | (verificación, no adquisición) | 4 404 049 | `sha256` = `be372533…2ef4d5`, **COINCIDE** con `manifiesto.yaml:4115` |
| 33 | ICPSR `TermsOfUse.html` | leído | 7 148 | ver §3(d) |

---

## 2 · Objetivo #27 · PDN — **ADENDA aplicada** (`R0`–`R7`)

`grep -n "PDN\|pdn_s3v2\|fila 28" forense/notas/2026-09-06-MAESTRA38-A4-spec.md` → tres aciertos (líneas 84, 85, 91): la fila 28 **sí** está en el `COMMIT-1` congelado (objetivo #27, y #21 como su receta lateral). La fila no estaba cerrada cuando llegó la adenda. Alcance respetado: **un objeto del `COMMIT-1` de A4**, no el barrido paginado de los cuatro sistemas — eso es `MAESTRA38-A5`, rama propia. **Una petición por segundo, sin paralelismo**, todo fuera del sandbox.

### `R0` · Control positivo
```
curl -sS -A "$UA" -o /dev/null -w "%{http_code} %{size_download}" --max-time 30 https://www.inegi.org.mx/
→ 200 153615
```
Hay red. Todo lo de abajo es hallazgo sobre la PDN, no sobre el entorno.

### `R1` · Backends públicos — **el experimento que zanja la discrepancia de lectura de código**

Dos documentos afirmaban cosas opuestas leyendo el mismo GitHub: la adenda decía que los backends responden **sin token** (la PDN guarda las credenciales OAuth de cada estado); un reconocimiento paralelo decía que las OAS de `PDNMX/api_docs` describen una API OAuth2 sin bulk público. Ninguno probó el host. **Este acto sí. Gana la adenda:**

```
GET  https://api.plataformadigitalnacional.org/                       → 200 · 1170 B · text/html · "Welcome to nginx!"   [VACÍO, no veredicto]
GET  .../s1/v1/providers          Accept: application/json           → 200 · 4302 B · application/json  (lista de SESEA estatales)
POST .../s1/v1/search  {"supplier_id":"EDOMEX","page":1,"pageSize":10} → 200 · 49643 B · application/json
     pagination = {"pageSize":10,"page":1,"totalRows":153011,"hasNextPage":true}
     results[0] trae datosGenerales.nombre/primerApellido/segundoApellido, institución, escolaridad, empleo — persona con id.
POST .../s2/api/v1/suppliers  {}                                      → 200 · 4016 B · application/json
POST .../s2/api/v1/summary    {}                                      → 200 · 4467 B · application/json (totalRows por entidad)
GET  .../s6/api/v1/summary                                            → 500 · 149 B · {"error":"Error de conexión a base de datos",
                                                                          "details":"connect ECONNREFUSED 10.151.2.181:27600"}   [SERVIDOR]
GET  .../s6/api/v1/buyers                                             → 000 · curl (28) timeout 60 s                              [RED]
POST .../s6/api/v1/search?supplier_id=SHCP                            → 000 · curl (28) timeout 60 s                              [RED]
GET  .../s3-wrapper/api/v1/providers                                  → 200 · 2444 B · application/json {"success":true,"data":[…]}
```

**Sin token, sin cuenta, sin clickwrap.** S1 y S2 y S3 responden; S6 está caído hoy por su base de datos (mensaje de error propio, con IP interna). Ese `500` es un hecho sobre S6 hoy, no sobre el método.

### `R2` · El botón «Descarga todos los datos { JSON }» — **la ruta que rindió**

El shell de `/declaraciones` pesa 1 144 B (React), pero **sí trae `<script src=…>`**: `index.1d5282f65e.js`, `309.51829b29a2.js`, `lib-react`, `lib-router`, `lib-polyfill`, más `/__zenedge/assets/hic.js`. Bajado el bundle (1 047 335 B), los cinco `href` del botón están ahí, estáticos, y **apuntan a Google Drive**, no a un dominio de la PDN:

```
tipoGA:"bulk-s1"  → drive.google.com/file/d/1RSYOwWabsWqtxt7VNHIjf-yt1P5bPSbE
tipoGA:"bulk-s2"  → drive.google.com/file/d/1KWcst_YLI5YVlKnzmd3Xm5prAP4NVhAD
tipoGA:"bulk-s3P" → drive.google.com/uc?export=download&id=1i-HjNju04xdKThHgGDAzHb97GdF_cqS8   (mismo id para "bulk-s3SP")
tipoGA:"bulk-s6"  → drive.google.com/file/d/1OM-P1JAp7PKeGL_InRYOQ1UO5Vpcs9Oi
```

Por eso ninguna lectura de las OAS podía encontrarlos: **no viven en la API**. Bajados con el formulario de confirmación de Drive (los grandes no salen a la primera):

| bulk | bytes | entradas | `testzip` | primera entrada |
|---|---:|---:|---|---|
| S1 declaraciones | **2 912 499 396** | 16 070 | `None` | `PDN_S1/Aguascalientes/data-0000000001.json` |
| S2 servidores en contrataciones | 1 782 572 | 156 | `None` | `AGUASCALIENTES/data-0000000001.json` |
| S3 servidores sancionados | 1 459 284 | 34 | `None` | `faltas_graves_de_servidores_publicos/edomex_s3_servidores_publicos.json` |
| S6 contratos OCDS | **1 059 406 620** | 12 | `None` | `PDN_S6/aguascalientes_releases.json` |

**Control positivo obligatorio, cumplido: `CONTROL-COINCIDE`.** El bulk de S3 dio `sha256 = 923d0dd06d6855babec620b373394381de1c0d7eb16c523066f6d333efb11adb`, **idéntico** a la entrada `pdn_s3v2` que mesa bajó a mano el 9/may/2025 — mismos 34 JSON, mismos bytes. El método reproduce exactamente lo que un humano con navegador obtuvo. Por eso ese archivo **no se re-registra** (`--escanea` lo detectó como ya registrado y lo excluyó él solo).

### `R3`-`R7` · no fueron necesarias para el objeto, se declara qué son
- **`R3` (Wayback)**: no se ejecutó como ruta de rescate porque `R2` rindió el objeto. Es la ruta de respaldo si el bundle cambia. **Declarado, no ejecutado** — no se reporta como hallazgo lo que no se midió.
- **`R4` (OpenAPI del portal)**: el bundle enlaza `/oas/ui/` y `/validapi/`; las OAS reales están en `raw.githubusercontent.com/PDNMX/api_docs/master/S{1,2,3}/oas/*.json`, y el propio bundle las carga desde ahí. No aportan al objeto: describen la API de consulta, no el bulk.
- **`R5` (GitHub)**: el bundle también referencia `PDNMX/bulk-generator` (`Reporte de validador de buscador/reporte_s{2,3p,3s}.json`) — es decir, la PDN **publica el generador de los bulk**. Ruta viva para futuros vintages.
- **`R6` (navegador en la caja)**: innecesaria. `R2` extrajo los `href` sin ejecutar JS.
- **`R7` (datos abiertos federales)**: sí se usó, y rindió: la API CKAN de `datos.gob.mx` dio la URL real de CompraNet y las **seis** de DeclaraNet.

### Términos y licencia
`https://www.plataformadigitalnacional.org/terminos` es shell React (668 B tras el reto Zenedge; **VACÍO**, no `403`). La licencia sí está en el bundle, verbatim: «**Plataforma Digital Nacional © 2018 se encuentra bajo la licencia CC BY-NC 4.0**» (`creativecommons.org/licenses/by-nc/4.0/deed.es`). Uso no comercial: compatible con este programa.

---

## 3 · Hallazgos — cada uno corrige un cierre anterior

**(a) `losmexicanos.unam.mx` no está caído; estaba mal direccionado.** El cierre del 5/sep declaró `SIN-FETCH … bloqueado desde NUBE por política de egreso, tres sondas independientes, mismo veredicto`. Medido hoy desde Ubuntu con red, **tres intentos espaciados 20 s**:

```
https://losmexicanos.unam.mx/       → 000 · curl (35) Recv failure: Connection reset by peer   ×3
http://www.losmexicanos.unam.mx/    → 200 · 17452 B · text/html                                 ×3
```

Es el **esquema + el hostname**, no el host. Con la forma correcta bajaron **113 de 113** archivos en vivo, **cero** por espejo. La lección es del tipo «un negativo mide el comando que lo produjo»: tres sondas idénticas sobre la misma URL mal formada son una sonda repetida tres veces.

**(b) `ieepco.org.mx`: el `000` era cadena TLS incompleta, no ausencia.** `openssl s_client` muestra que el servidor sirve el *leaf* **dos veces** y omite el intermedio; `Verify return code: 21 (unable to verify the first certificate)`. El *leaf* declara su propio AIA: `CA Issuers - URI:http://cacerts.geotrust.com/GeoTrustTLSRSACAG1.crt`. Traído ese intermedio, convertido a PEM y concatenado con `/etc/ssl/certs/ca-certificates.crt`, **curl y wget bajaron el archivo con verificación completa, sin `-k`**. Misma clase que el defecto ya medido en CNBV. Un navegador nunca lo nota porque completa la cadena por AIA solo.

**(c) `403` de directorio ≠ ausencia de archivo.** `MexicanosConstitucion/encuesta_nacional/base_datos/` responde `403` (listado deshabilitado); los archivos **dentro** responden `200`. Probar el directorio y concluir «no hay microdato» habría sido un falso negativo — y es exactamente lo que la ficha `CULTURA_CONSTITUCIONAL_UNAM_IIJ` decía («ni siquiera la existencia de un portal está confirmada»). Existe, y el microdato es público en tres formatos.

**(d) El paquete ICPSR no traía el `.dta`, y la razón no era la que se suponía.** `unzip -l` (§1 del `COMMIT-1`): 10 entradas, **cero archivos de datos**. Pero el `35024-manifest.txt` **que viene dentro del propio paquete** lista, bajo `DS0001 Public Use Data (Spanish Language)`, el archivo `35024-0001-Data.dta` con `MD5 3f717dfcd8f3ba136c5d5ac0f571990c`, `1,555` registros, `374` variables — junto con `.rda`, `.sav`, `.stc`, `.tsv`, `.txt` y los `Setup.*`. Y `TermsOfUse.html` dice, verbatim: «*On 2026-09-02, Jonatan Guadarrama agreed to the terms below pursuant to the download of study 35024*». Es decir: **la cuenta ya se tenía y los términos ya se aceptaron; lo que se descargó fue el paquete de documentación, no el de datos.** La razón que aplica de las tres del encargo es **`EXIGE-CUENTA`** (estudio *member-funded* de ICPSR), y el arreglo es de un minuto, no de trámite — está en `PAQUETE-RECETAS-10 §1`. Además, este acto encontró un **subconjunto público del mismo `DS0001` en Harvard Dataverse sin login** (`35024-0001-Data_partial.tab`, 59 307 B, DOI `10.7910/DVN/ESRIBE`): **es parcial y no sustituye** el `1 555 × 374`; se registra como lo que es.

**(e) Una URL de página no es una URL de recurso, y la API CKAN lo resuelve.** `www.datos.gob.mx/dataset/<id>` devuelve `200 · text/html` — parece vivo y no sirve el dato. `GET /api/3/action/package_show?id=<id>` devuelve `resources[].url`. Así aparecieron el CSV real de CompraNet y **seis** recursos de DeclaraNet donde la receta citaba uno.

**(f) El `503` de DeclaraNet era una ruta vieja, no un host caído.** La receta citaba `/api_update/secretaria_de_la_funcion_publica/…`. La SFP se renombró **Secretaría Anticorrupción y Buen Gobierno** y el prefijo pasó a `/api_update/sabg/…`, que responde `200` con los 45 284 941 B exactos que la receta predecía. Un `503` sobre un prefijo obsoleto no es un hecho sobre la disponibilidad del dato.

**(g) El bulk oficial de la PDN vive en Google Drive.** Ninguna especificación OpenAPI de la PDN podía revelarlo: los cinco `href` son literales inyectados en el bundle React desde `.env`. Leer el bundle es la ruta; leer la OAS no lo es.

**(h) La API SPA de INEGI está en mantenimiento hoy, y no hace falta.** `app/api/productos/interna_v1/archivoscompaginacion/1733?tipodocto=N` devuelve `200 · 6375 B · «Página en mantenimiento»` para `tipodocto` 0-7, y `406` si se pide `Accept: application/json`. Pero la URL directa por convención (`contenidos/programas/ecopred/2014/microdatos/ecopred14_bd_dbf.zip`) responde con los 22 296 331 B reales. **El discriminador es el tamaño**: el soft-404 de INEGI son `200 · 2 263 B`; todas las rutas `doc/*` de ECOPRED dan exactamente eso. El descriptor no existe como descarga separada — **viene dentro del zip** (`ecopred14_base_datos.pdf`, 2 134 631 B).

---

## 4 · Registro por las tres capas

1. **Manifiesto** (`data/manifiesto.yaml`): `1 315` → `1 515`. Ciclo `--escanea data_raw --grupo <patrón> --url … --usado-para …` seguido de `--promueve --grupo <patrón>`, **una fuente a la vez** — `--escanea` regenera el staging entero, así que promover antes del siguiente escaneo es obligatorio. 18 fuentes. `data/manifiesto-staging.yaml` queda **a vacío**. `--verifica` sobre `data_raw`: **`coincide=1195 · no_coincide=0 · ausente=0 · sin_configurar=0`**.
2. **Cola** (`data/curacion-registro/cola-adquisicion-registro.tsv` + vista `data/cola-adquisicion-v1_0.tsv`): **18 filas tocadas, 114 intactas byte a byte**. Escritas con `tools/curador_registro/tsv_crudo` por línea opaca; la llave es el par (`fila_origen`, `fuente_canonica`) porque `fila_origen` **no es única** (`…:NUEVA-L3` y `…:NUEVA-L6` se repiten). `OBTENIDO` `92` → `104`. Vista regenerada con `tools/vista_cola_adquisicion.py` (132 filas).
3. **Relaciones/procedencias/utilidad**: **no se tocan, y se declara por qué.** El perímetro las admite «sólo por `alta_relacion.py` para fuente nueva». Ninguna de las fuentes nuevas es citada hoy por una necesidad de `relaciones.tsv` — verificado para CNGF e IMSS-Bienestar en sus propias recetas (`0 necesidades`), y este acto no abrió ningún payload para medir. Dar de alta una relación sin una necesidad que la cite sería inventar el vínculo. `baseline.json` intacto por lo mismo.

---

## 5 · Suite y anti-PR#77

```
python3 tests/check.py --baseline
→ 3 FAIL · 170 WARN
→ LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

**Anti-PR#77.** Los 201 payloads están en el **corpus compartido**, no sólo en este worktree: `data/raw` es un symlink a `/home/pc0/mm-corpus/raw` y todo depósito se escribió contra esa ruta absoluta.

```
python3 -c "…os.walk…" sobre /home/pc0/mm-corpus/raw/<17 subcarpetas nuevas>
→ 199 archivos · 5 393.2 MB   (+ 2 en academico_icpsr35024 = 201)
```
