# PAQUETE-RECETAS-10 — 2026-09-06

Producido por `ACTO MAESTRA38-A4 · ADQUIERE-TODO-LO-PUBLICO`. **Esta es la lista que mesa recibe.** Contiene **sólo lo que caja no pudo bajar**, cada objeto con la razón exacta medida y una receta de un minuto: URL exacta · qué botón · qué nombre va a tener el archivo · dónde depositarlo.

Firma que este acto ejecutó, verbatim (6/sep): «*Lo que pueda bajar caja que lo baje caja, lo que no, dame las ligas y el detalle de qué tengo que bajar*».

**Caja bajó 25 de 33 objetivos** (201 archivos, 5.39 GB, todos con doble descarga y `sha256` idéntico entre dos transportes distintos). Quedan **5 objetos** aquí. Los otros 3 son las fichas de diseño sin objeto adquirible que el `COMMIT-1` ya declaró y que ninguna receta puede cubrir (§6).

Cada objeto de abajo **agotó** el protocolo `/adquiere` v2.2 antes de llegar a esta lista: transportes distintos (`curl`, `wget`, `python3`), encabezados de navegador real con `Referer`, sesión completa antes de API, espejos y rutas alternas (Wayback, CKAN, subdominio, vintage anterior), reintentos espaciados, y lectura de la página real antes de nombrar la razón. La salida cruda de cada intento está en `forense/notas/2026-09-06-MAESTRA38-A4-resultados.md`.

---

## Tablero

| # | objeto | razón exacta | costo para mesa |
|---:|---|---|---|
| 1 | `35024-0001-Data.dta` — ICPSR 35024 completo (1 555 × 374) | **EXIGE-CUENTA** | 1 minuto — **la cuenta ya existe y los términos ya se aceptaron** |
| 2 | Microdato firma-a-firma — WB Enterprise Surveys México 2023 | **EXIGE-CUENTA** | minutos + hasta 2 días hábiles de aprobación |
| 3 | PDF Bauchet, SSRN 2474620 | **EXIGE-SESION-NAVEGADOR** (Cloudflare + login) | 1 minuto con navegador |
| 4 | Microdato individual — Reuters Digital News Report | **EXIGE-SOLICITUD-ESCRITA** | un correo, respuesta incierta |
| 5 | Microdato ENJUVE 2000/2005/2010 | **HOST-NO-RESPONDE** en 3 hosts | **no hay receta ejecutable hoy** — ver §5 |

---

## 1 · `35024-0001-Data.dta` — Mexico Panel Study 2012 (ICPSR 35024)

**Razón: `EXIGE-CUENTA`.** Y el detalle importa, porque cambia el costo de días a un minuto: el paquete que ya está en el corpus (`academico_icpsr35024/icpsr35024_mexico_panel_study_2012_paquete_v1.zip`, 14 665 813 B) trae **10 entradas y cero archivos de datos** — dos cuestionarios, cuatro *codebooks*, tres textos y `TermsOfUse.html`. Pero dentro de ese mismo paquete, `35024-manifest.txt` lista bajo `DS0001 Public Use Data (Spanish Language)` el archivo `35024-0001-Data.dta` (MD5 `3f717dfcd8f3ba136c5d5ac0f571990c`, 1 555 registros, 374 variables) junto con `.rda`, `.sav`, `.stc`, `.tsv`, `.txt`; y `TermsOfUse.html` dice verbatim: «*On 2026-09-02, Jonatan Guadarrama agreed to the terms below pursuant to the download of study 35024*».

**Traducción: la cuenta ya se tiene, los términos ya se firmaron, y lo que se descargó el 2/sep fue el paquete de DOCUMENTACIÓN en vez del de DATOS.** No falta un trámite: falta marcar otra casilla.

**Receta, ≤1 minuto:**

1. Abrir `https://www.icpsr.umich.edu/web/ICPSR/studies/35024` e iniciar sesión con la cuenta que ya aceptó los términos el 2/sep/2026 (la misma que generó el zip que está en el corpus).
2. Botón **Download** → **Download All Files** (o `Delimited`/`Stata` si se prefiere un solo formato). **La diferencia con lo que se bajó antes es esta pantalla**: hay que elegir el paquete de **datos**, no el de **documentation only**.
3. El navegador descarga `ICPSR_35024.zip` (o `icpsr35024-V1.zip`), **~15-30 MB**, que esta vez debe contener `DS0001/35024-0001-Data.dta`.
4. **Verificación antes de registrar** (esto es lo que decide si la descarga sirvió): el `.dta` debe dar **MD5 `3f717dfcd8f3ba136c5d5ac0f571990c`**, y al abrirlo, **1 555 filas × 374 columnas**. Si el zip vuelve a traer sólo PDF, se eligió otra vez el paquete de documentación.
5. **Depositar en** `data/raw/academico_icpsr35024/` (junto al paquete que ya está ahí; **no lo sobreescribas** — son dos objetos distintos) y registrar con `python3 tests/manifiesto.py --registra`.

**Ya obtenido por caja, y no lo sustituye:** `academico_icpsr35024/icpsr35024_ds1_subconjunto_dataverse.tab` (59 307 B) + su codebook (28 502 B), un **subconjunto público de variables del mismo `DS0001`** depositado en Harvard Dataverse sin login (DOI `10.7910/DVN/ESRIBE`). Es parcial: no es el `1 555 × 374`.

---

## 2 · Microdato firma-a-firma — World Bank Enterprise Surveys México 2023

**Razón: `EXIGE-CUENTA`** (registro con aprobación, no clickwrap). Medido: `microdata.worldbank.org/index.php/catalog/6453` responde `200`, y los documentos bajan **sin cuenta** — pero el microdato exige registro aprobado en `login.enterprisesurveys.org`.

**Receta:**

1. Registrarse en `https://login.enterprisesurveys.org/en/registration` (nombre, institución, uso previsto). **La aprobación tarda hasta 2 días hábiles** — no es instantánea.
2. Con la cuenta aprobada, abrir `https://microdata.worldbank.org/index.php/catalog/6453`, pestaña **Get Microdata**, aceptar los términos de citación y descargar.
3. Archivo esperado: `MEX_2023_ES_v01_M_Stata.zip` (o el equivalente en SPSS/CSV según lo que ofrezca).
4. **Depositar en** `data/raw/wb_enterprise_surveys_mx2023/` y registrar.

**Ya obtenido por caja, sin cuenta, y sirve para decidir antes de tramitar:** `ES_B-READY_2023_Questionnaire.pdf` (1 041 388 B) y `Mexico_2023_ES_Implementation_Report.pdf` (602 312 B). **Léelos primero**: si el cuestionario no trae el reactivo «motivo de rechazo de crédito = sin historial crediticio» que `N19` pide, el trámite de la cuenta no vale la pena. Esa pregunta se puede contestar hoy, gratis, con lo que ya está en el corpus.

---

## 3 · PDF Bauchet — SSRN 2474620 (`PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND`)

**Razón: `EXIGE-SESION-NAVEGADOR`** (reto Cloudflare + login SSRN). `NO-OBTENIDO-POR-ESTE-AGENTE EN 5 INTENTOS`, cinco rutas **distintas**, no cinco veces la misma:

```
papers.ssrn.com/sol3/papers.cfm?abstract_id=2474620                → 403 · 5781 B · text/html
papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2474620_code1234.pdf      → 403 · 5911 B · text/html
cenfri.org/research-paper/price-and-information-type-…             → 200 · 263155 B · 0 enlaces .pdf en el HTML
web.archive.org/web/2020/…papers.cfm?abstract_id=2474620           → 200 · 84810 B · es la PÁGINA archivada, no el PDF
api.semanticscholar.org/graph/v1/paper/search?query=…              → 429 · rate limit sin llave
```

**Receta, ≤1 minuto:**

1. Abrir en un navegador real `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2474620` (el reto de Cloudflare se resuelve solo en un navegador).
2. Botón **Download This Paper** (pide una cuenta SSRN gratuita si no hay sesión).
3. Nombre esperado: `SSRN-id2474620.pdf`.
4. **Depositar en** `data/raw/milk_rct_microseguro/` (junto a su hermana) y registrar.

**Advertencia para mesa, para que la receta no prometa de más:** ni este PDF ni la hermana ya obtenida cierran `R1.4` — ninguno de los dos trae comparador de marca / sustituto. Bajarlo completa el registro bibliográfico; **no** cierra la necesidad de modelo.

**Ya obtenido por caja:** `MILK-RCT--Study-of-Life-MI-Purchasing-Decisions-in-Mexico.pdf` (1 111 333 B), misma RCT, mismos ~8 700 clientes de Compartamos Banco, mismo autor principal.

---

## 4 · Microdato individual — Reuters Institute Digital News Report

**Razón: `EXIGE-SOLICITUD-ESCRITA`.** `NO-OBTENIDO-POR-ESTE-AGENTE EN 3 INTENTOS`, tres **depósitos** distintos, no tres reintentos:

```
UK Data Service (datacatalogue.ukdataservice.ac.uk, búsqueda "digital news report") → 200 · sin depósito del DNR
ORA Oxford (ora.ox.ac.uk/search?q=digital+news+report+dataset)                      → 404
Reuters Institute — sólo formulario de contacto, ningún enlace de datos             → 200
```

**Receta (no es de un minuto, y se dice):**

1. Abrir `https://reutersinstitute.politics.ox.ac.uk/digital-news-report/archive/contact-us/index.html` y llenar el formulario, **o** escribir directo a `reuters.institute@politics.ox.ac.uk`.
2. Pedir explícitamente: *individual-level survey data, Mexico, DNR <año>*, indicando institución y uso académico no comercial.
3. **La respuesta y el plazo son inciertos** — es solicitud, no descarga. Si llega, el archivo suele ser `.sav`.
4. **Depositar en** `data/raw/reuters_dnr/` y registrar.

**Ya obtenido en actos previos:** las 9 tablas *topline* de México 2025 vía `datawrapper.dwcdn.net/<chart_id>/<version>/dataset.csv`. Cubren alcance por marca, confianza global y por marca, dispositivos y redes — **agregados, no por persona**.

---

## 5 · Microdato ENJUVE 2000/2005/2010 — **sin receta ejecutable hoy, y eso es el entregable**

**Razón: `HOST-NO-RESPONDE`** en los tres hosts que alguna vez lo alojaron. `NO-OBTENIDO-POR-ESTE-AGENTE EN 4 INTENTOS`, cuatro rutas distintas:

```
www.gob.mx/imjuve/documentos/base-de-datos-…-2010   → 200, pero la página sólo lista PDF de cuestionario
cendoc.imjuventud.gob.mx                            → curl (6) Could not resolve host  — el DNS ya no existe
bdsocial.inmujeres.gob.mx                           → curl (7) Failed to connect port 443
CDX de Wayback sobre cendoc.imjuventud.gob.mx       → 200 · sólo 4 binarios archivados, los 4 .xls, ningún .sav/.dta
```

**No se escribe una receta que no se puede ejecutar.** Lo que mesa puede hacer, en orden de costo:

1. **Solicitud de acceso a la información** al IMJUVE por la Plataforma Nacional de Transparencia, pidiendo las bases de datos de la ENJ 2000/2005/2010 en formato electrónico. Es el único camino identificado.
2. Preguntar a `bdsocial.inmujeres.gob.mx` (INMUJERES) si el acervo migró: el host no conecta hoy, pero la institución existe.

**Ya rescatado por caja del espejo Wayback (y es lo único que sobrevive públicamente):** cuatro **tabulados** de la ENJ 2005 en `data/raw/enjuve_imjuve/` — `ENJ005EDUCACION.xls` (1 079 296 B), `ENJ2005ESFERADELAVIDAPRIVADA.xls` (1 788 928 B), `ENJ2005ESFERADELAVIDAPUBLICA.xls` (2 735 104 B), `ENJ2005VALORESYACCESOALAJUSTICIAYLOSDH.xls` (989 696 B). **Son tabulados, no microdato.**

---

## 6 · Lo que NO lleva receta, y por qué

Tres filas del universo son **fichas de diseño sin objeto adquirible** (`MAESTRA38-N10`): `salud.adherencia.desabasto_vs_cuidadora`, `cooperacion.comite.monitoreo_sancion_visible`, `cooperacion.faena.sancion_social_pueblo_mestizo`. En las tres, el *driver* institucional ya está medido (Cero Desabasto, MACU, CNGMD) y lo que falta es el **desenlace individual**, que **no existe como registro administrativo**: nadie sigue al paciente para saber si abandonó el tratamiento, ni registra si esta persona cooperó bajo monitoreo. No hay URL que bajar. Una receta para un objeto que nadie ha visto sería inventada, y este paquete no las trae.

La cuarta ficha, `CULTURA_CONSTITUCIONAL_UNAM_IIJ`, **salió de esta categoría**: decía «ni siquiera la existencia de un portal está confirmada», y este acto encontró y bajó su microdato completo en `.csv`/`.dta`/`.sav` más cuestionario, metodología y libro. Ya no necesita receta.

---

## Contador

Objetivos del `COMMIT-1`: **33**. Obtenidos por caja: **25** (201 archivos, 5.39 GB). En este paquete para mesa: **5**. Sin objeto adquirible: **3**. Recetas de un minuto reales: **3** (§1, §2, §3); solicitud escrita: **1** (§4); sin receta ejecutable, con vía institucional declarada: **1** (§5).
