# ACTO GEN2-SONDA-CAJA-1 · CIERRA-RESERVAS-PR632 — nota de cierre

**Encargo:** cierra las tres reservas materiales que `PR #632` (`ACTO GEN2-SONDA-2 ·
OPERACIONALIZA-SONDA-LATERAL`, `forense/notas/2026-09-08-GEN2-SONDA-2-operacionaliza-sonda-lateral.md`)
no pudo verificar por estar ejecutándose en NUBE sin `data/raw` y con política de egreso bloqueada.

**Entorno:** CAJA UBUNTU, `Linux 6.18.33.2-microsoft-standard-WSL2`. Worktree nuevo
`/home/pc0/mm-gen2-sonda-caja-1`, rama `acto/gen2-sonda-caja-1-cierra-reservas-pr632`,
creada desde `origin/main` re-derivado (`git fetch --prune` → `a800f299`, PR #632 confirmado
`MERGED` por `gh pr view`). El worktree principal (`/home/pc0/Modelado-Mexicano`) estaba
parado en `tramite/absorbe-historico`, 186 commits detrás de `origin/main` — clon padre
desfasado, no se usó (mismo patrón que `feedback_clon_padre_desfasado_trae_acto_viejo`).
`data/raw` del worktree nuevo no traía el symlink (worktree recién creado, no ausencia de
corpus) — reconstruido: `ln -s /home/pc0/mm-corpus/raw data/raw`, 397 entradas visibles.
`descargas_mx` confirmada montada y accesible fuera del sandbox de Claude Code
(`/mnt/c/Users/PC0/Descargas MX`, 1450208 archivos). Red real confirmada: `curl
https://www.inegi.org.mx` → `200`. **Todas las sondas de red de este acto se ejecutaron con
`dangerouslyDisableSandbox` — el sandbox por defecto de Claude Code no expone `/mnt/c` real
ni la red real (necesario para esta caja, no un hallazgo de `/sonda`).**

**Compuerta:** ninguna compuerta previa que verificar por producto — este acto es el propio
seguimiento CAJA que `PR #632` dejó pendiente. `python3 tests/check.py --baseline` corrido
al arranque: **LÍNEA BASE VERDE** (3 FAIL / 210 WARN, todos ya congelados en
`tests/baseline.json`, ninguno nuevo).

---

## P1 · R5.4 / ENADID 2023 — `NO-ENCONTRADO-EN-ENADID2023`

**Definición VERBATIM (`canon/modelo-decision-v4_0.md:538`):**

> SI el cortejo es urbano-joven-conectado (`edad` joven, 15-29 años, convención declarada
> — §1.1.A ∧ `tam_loc`=1 ∧ `conex_inte`=1) ENTONCES apps + lógica de mercado, pero los
> guiones de género se reconfiguran **desigual** (actitud rápida, conducta lenta) — PORQUE
> cohorte + exposición — `[MEDIA / HIPÓTESIS]`. · **id:** `familia.cortejo.urbano_joven_apps`

**Resolución de ENADID 2023 contra el manifiesto:** codebook ya en corpus,
`data/raw/fd_enadid23.xlsx` (`fd_enadid23_xlsx` en `data/manifiesto.yaml`), hoja `TMUJER1`
(mujeres 15-54 años con módulo). Abierto con `openpyxl` (solo el descriptor, ninguna
distribución ni resultado).

**Hallazgo — `CONOCE_1..6` es un falso positivo nominal.** Filas 888-906 de la hoja
`TMUJER1`:

| variable | etiqueta | categorías |
|---|---|---|
| `CONOCE` | Conocimiento y tipo de métodos anticonceptivos | (encabezado del bloque) |
| `CONOCE_1` | Conocimiento de OTB (oclusión tubaria bilateral) | 1=Sí, 2=No |
| `CONOCE_2` | Conocimiento de vasectomía | 1=Sí, 2=No |
| `CONOCE_3` | Conocimiento de métodos hormonales | 1=Sí, 2=No |
| `CONOCE_4` | Conocimiento de métodos no hormonales | 1=Sí, 2=No |
| `CONOCE_5` | Conocimiento de métodos tradicionales | 1=Sí, 2=No |
| `CONOCE_6` | Conocimiento de métodos (resumen) | 0=Conoce ≥1 método, 1=No conoce, 2=No especificado |

Las seis variables miden **conocimiento de métodos anticonceptivos** entre mujeres en edad
fértil — nada relacionado con cortejo, aplicaciones de citas, `tam_loc` como condición de
disparo, ni `conex_inte`. El verbo compartido "conocer" (conocer un método vs. "el cortejo
es… conectado") es la única coincidencia — coincidencia léxica sobre el string `conoce`, no
sustantiva. No hay universo/filtro documentado en el descriptor que acerque estas variables
a la definición de R5.4.

**VEREDICTO: C. `NO-ENCONTRADO-EN-ENADID2023`.** `TMUJER1:conoce_1..6` fue un falso
positivo nominal de la sonda HERMANAS de `PR #632`. No se tocó `R5.4`, tier, `milpa/**`,
canon ni spec alguna.

---

## P2 · RUPC — sonda LATERAL real ejecutada, negativo sobre el objeto original + hallazgo colateral ya en corpus

**Estado de entrada:** fila `RUPC` de `data/curacion-registro/cola-adquisicion-registro.tsv`
(`fila_origen=forense/notas/2026-09-06-MAESTRA38-A6-reconciliacion.md#RUPC`),
`NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)`. Nota de `PR #632` propone 3 rutas laterales
ADICIONALES, sin verificar por ejecución (red NUBE bloqueada).

**Las tres rutas, ejecutadas con red real de CAJA:**

**(a) Backend público de contratos adjudicados de comprasmx.** Antes de sondear red: A.8
contra `data/manifiesto.yaml` — `compranet5_contratos_2022_2023_xlsx` ya `OBTENIDO`
(`ACTO MAESTRA36-A2`, corpus compartido). Abierto con `openpyxl` (objeto ya adquirido, no
requiere red): columna 36 es literalmente **"Folio en el RUPC"**, junto a columna 37 (`RFC`)
y 38 (`Proveedor o contratista`).

```
python3 -c "... col 36 'Folio en el RUPC' sobre las 13406 filas ..."
→ 9730 de 13406 filas con folio poblado (72.6%)
```

Ejemplos verificados: `(6735, 'GMS971110BTA', 'GRUPO MEXICANO DE SEGUROS SA DE CV')`,
`(4855, 'SIN9408027L7', 'SEGUROS INBURSA SA...')`. **La candidata (a) queda CONFIRMADA por
contenido, no solo por código de respuesta** — y ya está `OBTENIDA` desde `MAESTRA36-A2`
(6/sep), sin necesidad de adquisición nueva. Expone el Folio RUPC del proveedor ganador
**por contrato**, no el padrón/reporte RUPC completo (sin domicilio, sin estatus del
proveedor, sin historial de sanciones) — pieza parcial del hueco "persona + sanción" que la
fila nombra, no su cierre.

**(b) Plataforma Nacional de Transparencia (PNT/INAI).** `buscador.plataformadetransparencia.org.mx`
existe (DNS resuelve, TLS handshake completa) pero está detrás de un reto de Cloudflare —
confirmado por **tres mecanismos independientes**:

```
curl -D - https://buscador.plataformadetransparencia.org.mx/
  → HTTP/2 403, cabecera cf-mitigated: challenge, server: cloudflare, 234981 B (página de reto JS)
WebFetch(misma URL) → "The server returned HTTP 403 Forbidden."
```

**SIN-FETCH — barrera de WAF confirmada, no inexistencia.** No se intentó sesión de
navegador real (headless) ni resolución del challenge — fuera del alcance de esta skill
(`/sonda` no abre sesión, no simula navegador).

**(c) CKAN datos.gob.mx con query específica de RUPC.** API correcta usada:
`https://datos.gob.mx/api/3/action/package_search` (el prefijo `/busca/api/3/` da `403`
de Akamai — WAF distinto, no relacionado con RUPC; documentado ya en memoria del proyecto).
Requiere `User-Agent` de navegador — sin él, la primera petición cae en un `403` de Akamai
antes incluso de llegar al backend CKAN (`308` con UA de navegador → sigue a `200`).

```
q=RUPC                                              → count 0
q=RUPC SFP                                          → count 0
q=RUPC contratistas                                 → count 0
q=Registro Unico de Proveedores y Contratistas      → count 17 (ninguno es SFP/RUPC nacional)
q=proveedores contratistas                          → count 3
q=padron de proveedores                             → count 99
q=Funcion Publica proveedores                        → count 41
organization_show(id=secretaria_bienestar)          → (irrelevante para RUPC, ver P3)
```

Los candidatos que sí aparecen (`padron_proveedores_contratistas` = CAPUFE,
`padron_proveedores_contratistas_sesna` = SESNA, `padron_personas_proveedoras_contratistas`
= SECIHTI) son **padrones institucionales propios**, mismo nombre genérico, organismos
distintos — no el RUPC nacional que administra la SFP/Secretaría Anticorrupción y Buen
Gobierno. **NEGATIVO ACOTADO: 0 datasets del RUPC nacional en CKAN datos.gob.mx**, universo
de 7 formulaciones de query agotado para este término.

**NEGATIVO ACOTADO (objeto original):** ninguna de las tres rutas laterales obtiene el
padrón/reporte RUPC en sí (el objeto que `norah/.../obtener` sigue rechazando con
`EXIGE-SESION-NAVEGADOR`, no reintentado hoy — ruta ya agotada por `MAESTRA38-A6`). Lo que
SÍ cambió: la ruta (a) resultó en un hallazgo colateral real, ya en corpus, sin necesidad de
adquisición.

**Fuera de este sondeo:** sesión de navegador real contra PNT; resolución del challenge de
Cloudflare; cualquier ruta no nombrada por las 3 laterales de `PR #632`.

**HANDOFF:** ninguno nuevo a la cola (candidata (a) ya `OBTENIDA`). Se actualizó la fila
`RUPC` existente (`upsert_fila`, misma clave `fila_origen`, no se duplicó) con el hallazgo
de (a)/(b)/(c) y se regeneró `data/cola-adquisicion-v1_0.tsv`
(`tools/vista_cola_adquisicion.py`).

**RECOMENDACIÓN:** si mesa considera que el Folio RUPC por contrato (ya en corpus) es
suficiente para el uso que motivó la fila, la fila puede recalificarse; si se necesita el
padrón completo (domicilio, estatus, sanciones), la vía que sigue abierta es sesión de
navegador real contra PNT o clientes con cookie de sesión legítima contra `norah/` — no se
decide aquí.

---

## P3 · R7.9 / Padrón de Bienestar — hallazgo mixto: esquema admite llave defendible, acceso hoy sigue bloqueado

**Definición VERBATIM (`canon/modelo-decision-v4_0.md:557`):**

> SI hay transferencia directa universal no condicionada ENTONCES **la atribución va al
> líder y se expresa como aprobación**, no como voto comprado — PORQUE premio retrospectivo
> al desempeño e identidad partidista — `[MEDIA]` (a), correlacional. · **id:**
> `civico.transferencia.atribucion_lider`

**Objetos ya en corpus (verificados antes de sondear red, A.8):**

- `r7_3_pub_beneficiarios_bienestar_csv` (`data/raw/R7.3_PUB_Bienestar/padron_unico_bienestar.csv`,
  ya `OBTENIDO`, verificado byte a byte por `CONF-17` el 6/ago): **agregado
  ENTIDAD×TRIMESTRE, 748 filas × 14 columnas** — sin folio individual, sin coordenadas, sin
  fecha de alta por beneficiario. Confirmado de nuevo hoy (releído, no descargado de nuevo).
- `ine_prep2024_base_datos_20240603_2005_zip`: PREP 2024 ya trae `SECCION` y
  `LISTA_NOMINAL` (documentado en `data/manifiesto.yaml:18866`, cruzado por
  `ieem_edomex_2024_ayuntamientos_x_seccion_xlsx`). **La llave electoral del lado PREP está
  confirmada disponible** — no se requirió sondeo adicional de red para esta mitad.

**Sondeo de red — portales nominales de Bienestar (`pub.bienestar.gob.mx`,
`cpid.bienestar.gob.mx`):**

```
getent hosts pub.bienestar.gob.mx / cpid.bienestar.gob.mx  → ambos resuelven a 200.188.126.42
curl -v https://pub.bienestar.gob.mx/
  → TLSv1.3 Client Hello enviado, luego "TLS alert, decode error" / "unexpected eof while reading"
curl --tlsv1.2 / --tls-max 1.2 / http (puerto 80)           → los tres, 000
WebFetch(https://pub.bienestar.gob.mx/)                     → "Socket is closed"
```

**Confirmado por 3 mecanismos independientes: TLS rechazado a nivel de servidor, misma
firma ya documentada para `historico-compranet.buengobierno.gob.mx`** (nota
`MAESTRA36-A2`). No es un artefacto del sandbox (se corrió con `dangerouslyDisableSandbox`,
red real de CAJA) ni bloqueo de política de egreso NUBE — es un rechazo TLS del host mismo,
reproducido igual en CAJA. **`pub.bienestar.gob.mx`/`cpid.bienestar.gob.mx` siguen
SIN-FETCH hoy**, con más precisión diagnóstica que el `000` genérico de la sonda del 4/ago
(`forense/notas/2026-08-04-aa-barrido-alcanzabilidad.md`).

**Hallazgo nuevo — mirror legítimo (Wayback Machine, técnica explícita de `/sonda §3`).**
El host vivo está bloqueado, pero `web.archive.org` conserva capturas del portal y de su
bundle JS (`main.288a966b.chunk.js`, capturado **20260902**, 6 días antes de este acto):

```
https://web.archive.org/web/20260414220908id_/https://pub.bienestar.gob.mx/
  → SPA React, título "Consulta al Padrón Único de Beneficiarios"
grep API paths en el bundle → /api/catalog/pub/{persons,resume,socialActors,anexo},
  /api/resume/{person,integral,publish/estate}, baseURL = https://pub.bienestar.gob.mx/v1|v2/
```

La API vive en el **mismo host** ya confirmado bloqueado (no hay host alterno que rodear el
bloqueo). Pero los `title`/`header` extraídos del bundle (`"Descarga por Municipio"`,
`"Clave Municipal"`, `"Padrones de personas físicas"`) apuntan a un documento de estructura
de datos, también archivado:

```
CDX de pub.bienestar.gob.mx/data/v2/anexos/ → Anexo_2_Estructura_de_datos.pdf (2022-12),
  recuperado vía Wayback id_ (351059 B, PDF 1.7)
```

**Este PDF ("Anexo 2. Estructura de Datos", Dirección General de Padrones de Beneficiarios,
Secretaría de Bienestar) documenta el esquema fuente que las dependencias reportan a
DGGPB — no el archivo público descargable — y trae, para la estructura "Persona" (71
campos):**

- `NB_CURP`, `NB_PRIMER_AP`/`NB_SEGUNDO_AP`/`NB_NOMBRE`, `FH_NACIMIENTO`, `CD_SEXO`;
- domicilio geográfico completo: `TIPOVIAL`/`NOMVIAL`, `NUMEXTNUM1/2`, `CP`, `TIPOASEN`/`NOMASEN`;
- geografía jerárquica completa: `CVE_LOC`/`NOM_LOC` (localidad), `CVE_MUN`/`NOM_MUN`
  (municipio), `CVE_ENT`/`NOM_ENT` (entidad);
- **`AGEB`** (Área Geoestadística Básica, INEGI) y **`CLAVE_MZNA`** (manzana);
- **`LONGITUD`/`LATITUD`** (coordenadas, con rango válido declarado para México);
- **`CVE_INE`** — "Clave de elector registrada en el INE".

**Lectura honesta, sin construir el enlace:** `AGEB` + `CLAVE_MZNA` + domicilio geográfico
completo es **la misma unidad que el propio Marco Geográfico Electoral del INE usa** para
adscribir manzanas a secciones — un cruce cartográfico estándar y público (no una inferencia
epistemológicamente inadmisible, a diferencia de inferir sección desde edad/sexo). `CVE_INE`
(la cadena de la credencial) **no** codifica la sección electoral por sí misma y el padrón
electoral confidencial del INE no es de acceso público — esa vía puntual no es defendible
sin el cruce geográfico. **Pero el esquema documentado SÍ contiene, del lado geográfico
(AGEB/manzana/domicilio), una secuencia de llaves defendible hacia sección electoral.**

**El límite honesto de este hallazgo:** este Anexo describe el **esquema interno/de
reporte** que las dependencias deben enviar a DGGPB — **no** está confirmado que el archivo
público descargable (el botón "Descarga por Municipio"/"Descarga por Entidad" de la SPA)
sirva estos mismos campos a nivel persona. El recurso público que SÍ se obtuvo y verificó
(`padron_unico_bienestar.csv`, CKAN) es agregado ENTIDAD×TRIMESTRE — muy por debajo de este
esquema. Por Ley General de Protección de Datos, es esperable que una descarga pública
anonimice o agregue exactamente los campos PII/geográficos finos (`CURP`, nombre, domicilio,
lat/long, `CVE_INE`) que harían el enlace posible. **No se intentó invocar la API en vivo
(host bloqueado) ni descargar "Descarga por Municipio" (no localizado en el índice de
Wayback) — CAJA no pudo verificar si ese nivel intermedio existe públicamente.**

**Búsqueda adicional en CKAN — sin nueva candidata de la Secretaría de Bienestar:**
`organization_show(id=secretaria_bienestar)` → exactamente **1 paquete publicado**,
`padron_unico_beneficiarios_bienestar` (el mismo agregado ya en corpus, sin actualizar desde
2025-06-05). Se exploró tangencialmente `programa_nacional_becas_bienestar_benito_juarez_*`
(CNBBBJ) — programa **condicionado** (becas escolares), no la transferencia universal no
condicionada que R7.9 exige — sus CSV por estado sí llegan a nivel `CVE_MUN`/`CVE_LOC` (un
registro por beneficiario, sin folio/nombre), lo que confirma que **algunas dependencias del
paraguas Bienestar sí publican municipio/localidad** — pero no es la fuente que R7.9 nombra
y no se descargó (solo se leyeron 5 filas de una muestra vía HTTP Range, sin registrar en
manifiesto ni cola).

**VEREDICTO — no colapsa a una sola letra, honestamente:**

- Del lado del **esquema documentado** (evidencia oficial DGGPB, archivada, no ejecutada
  hoy en vivo): **A. `ENLACE-POTENCIALMENTE-CONSTRUIBLE`** — existe una secuencia de llaves
  geográficas (`AGEB`/`CLAVE_MZNA`/domicilio) defendible hacia sección electoral, la misma
  que usa el marco geoelectoral oficial.
- Del lado de **lo accesible hoy** (recurso público ya obtenido + portal en vivo): **B/C
  combinados** — el recurso público confirmado es agregado (`GRANULARIDAD-INSUFICIENTE`) y
  el portal que serviría un nivel más fino sigue **`SIN-FETCH`** (TLS rechazado, confirmado
  en CAJA con red real, no artefacto de NUBE).

No se construyó el enlace, no se calculó asociación, no se abrió CALC, no se cambió R7.9.

**HANDOFF:** ninguno nuevo a la cola — `PUB`/`PREP 2024` ya tienen fila `OBTENIDO`. Se
reporta aquí, para quien diseñe la spec GEN2 de esta regla o para un `/sonda ... LATERAL`
futuro dedicado a: (i) intentar sesión de navegador real contra `pub.bienestar.gob.mx`
cuando el TLS vuelva a responder; (ii) verificar si "Descarga por Municipio" expone
`CVE_MUN`/`CVE_LOC` públicamente (nivel intermedio entre el agregado ya obtenido y el
esquema completo de Persona); (iii) obtener el Marco Geográfico Electoral del INE a nivel
AGEB/manzana (ya hay un ítem parcial en corpus, `ine_marco_geografico_electoral/*`, no
verificado a esa granularidad por este acto).

**RECOMENDACIÓN:** el hallazgo del Anexo 2 es material nuevo real (esquema con llave
geográfica defendible) pero no cambia el estado de acceso hoy — no ameritan por sí solos
abrir un CALC; sí ameritan quedar citados si mesa diseña una spec futura para R7.9.

---

## P4 · Validación de `/sonda` en CAJA

Ejecución real, primera vez en el entorno local: los tres modos usados (CONSTRUCTO
implícito en P1 al descartar el falso positivo, LATERAL explícito en P2, mixto
LATERAL+CONSTRUCTO en P3). **Ningún defecto material del contrato encontrado:**

- resolvió el universo YA examinado correctamente contra `PR #632` y la fila de cola antes
  de sondear (§1);
- distinguió barrera técnica (TLS/WAF/Cloudflare) de inexistencia en las tres reservas, sin
  necesitar corrección;
- no duplicó ninguna fila de cola (`upsert_fila` sobre la misma clave `fila_origen`);
- no confundió bloqueo de NUBE con negativo — de hecho, esta caja permitió **diferenciar**
  qué de lo que `PR #632` reportó era bloqueo de política de egreso (nada, en este caso: los
  tres bloqueos de hoy — Cloudflare en PNT, TLS en `pub.bienestar.gob.mx` — son del host
  mismo, reproducibles con red real);
- la vista de adquisición se regeneró limpio, sin errores, `134` filas antes y después (solo
  cambió el contenido de una fila).

**`/sonda` funciona como fue redactada — no se modificó `.claude/commands/sonda.md`.**

---

## AMPLIACIÓN (mismo día) — barrido paralelo con técnicas no aplicadas en la primera pasada; corrige un error propio

El operador preguntó explícitamente si se habían agotado todos los trucos disponibles. Auditar
la primera pasada contra la disciplina de `/sonda §5` ("declara el máximo, no el mínimo")
encontró que sí faltaban técnicas aplicables — y, al aplicarlas, una de ellas **refutó una
afirmación de esta misma nota**. Se declara aquí, sin editar el texto original de P3 arriba.

### Corrección a P3 — el PUB SÍ tenía una API de búsqueda nominal, no solo catálogos de metadatos

P3 arriba interpretó los tabs `persons`/`socialActors` del bundle archivado como catálogos de
metadatos ("Catálogos para la integración de padrones..."). **Eso era una lectura incompleta.**
Un segundo pase sobre el mismo bundle JS (`main.288a966b.chunk.js`) reveló, en construcciones de
URL que el primer grep no aisló, cuatro endpoints reales de **búsqueda nominal por apellido**:

```
GET /api/resume/integral/program/{prog}/period/{period}/estate/{clave}/person/?lastName=...&secondLastName=...&name=...
GET /api/resume/integral/program/{prog}/period/{period}/municipality/{clave_mun}/person/?lastName=...&secondLastName=...&name=...
```

Esto confirma que el portal en vivo (cuando responde) **sí** exponía consulta de un beneficiario
individual por nombre, filtrable a municipio — el título "Consulta al Padrón Único de
Beneficiarios" no era retórico. Solo se encontró el **patrón de URL/parámetros** en el código
fuente archivado — nunca se llamó a estos endpoints (host bloqueado) ni se vio/guardó dato de
persona alguna.

### Corrección a P3 — sí existe un agregado real a nivel MUNICIPIO, parcialmente recuperable hoy

`pub.bienestar.gob.mx/v1/api/resume/estate/{clave}` es un endpoint real (JSON,
`{municipalityKey, name, beneficiary, interventions}`, una fila por municipio) que Wayback
archivó de forma incidental para solo algunas entidades. Verificación exhaustiva de las **32
entidades reales + el bucket "99 no especificado"** (`web.archive.org/cdx/search/cdx`, uno por
uno, sin filtrar por prefijo estrecho):

| entidad archivada | filas | fecha de captura |
|---|---|---|
| `01` Aguascalientes | 12 municipios | 2023-09-28 |
| `07` Chiapas | 125 municipios | 2025-10-03 |
| `09` CDMX | (1105 B) | 2023-09-28 |
| `99` no especificado | 1 (bucket residual) | 2023-09-28 |
| **02–06, 08, 10–32** (29 de 32) | **0 — sin captura** | — |

Es genuinamente más fino que el agregado "por Entidad" ya conocido (748 filas nacionales), pero
**parcial e incidental** (el crawler nunca rastreó sistemáticamente el resto). El botón real
"Descarga por Municipio" del frontend (`/data/v2/municipalities/{prog}/{period}/{state}/...zip`)
tiene **cero** capturas en Wayback — nunca se generó como link estático rastreable.

### Corrección/precisión a P3 — la llave `AGEB`/`CLAVE_MZNA` que cité como "defendible" NO está respaldada por nada que ya tengamos en corpus

Verificación local (sin red) de `data/raw/ine_marco_geografico_electoral/*`, ya en corpus: los
tres archivos declaran explícitamente su propio tope — *"CATÁLOGOS A NIVEL ENTIDAD, DISTRITO
LOCAL, MUNICIPIO Y SECCIÓN"* y *"CATÁLOGOS A NIVEL ENTIDAD Y MUNICIPIO"* — **sección** es el
nivel más fino que contienen, nada de `AGEB`/manzana. La llave que P3 propuso como "defendible"
(vía cartografía electoral) sigue siendo conceptualmente válida, pero **el producto cartográfico
real (shapefiles del Marco Geográfico Electoral del INE, a nivel manzana) no está adquirido** —
sería un objeto nuevo y distinto, no una relectura de algo que ya está en el corpus. Nota
adicional: al revisar el archivo `.zip` de esa carpeta se sospechó un objeto nunca abierto por
la herramienta equivocada (7-zip servido con extensión `.zip`, `zipfile.ZipFile` lo rechaza) —
falsa alarma: el manifiesto ya documentaba correctamente el formato real (`py7zr`) desde
`MAESTRA34-L3`.

### P2 · RUPC — hallazgo mayor: el registro SÍ existe, republicado por sociedad civil — adquirido

Un barrido de organizaciones mexicanas de sociedad civil/civic-tech que históricamente raspan
CompraNet/RUPC encontró que **datamx.io** (portal CKAN operado por **Codeando México**) republica
un datastore propio del RUPC, **independiente** de todos los hosts oficiales ya confirmados
muertos:

- `https://datamx.io/dataset/compranet-rupc` — metadata CKAN: *"Proveedores y Contratistas de
  Gobierno inscritos en el Registro Único de Proveedores y Contratistas (RUPC)"*, licencia CC-BY,
  cosechado `2019-07-28`.
- Datastore vivo verificado por el operador (no solo por el agente): `datastore_search` sobre
  `resource_id=5ef00daf-42ee-4d7b-a62a-7531ef74ff03` responde `200`, `success:true`, con filas
  reales (`Folio RUPC`, `RFC`, `Nombre de la empresa`, `Entidad Federativa`, `Sector`, `Giro`,
  `Contratos`, `Fecha de inscripción al RUPC`, `Grado de cumplimiento LAASSP/LOPSRM`).
- **A.8**: `grep -in "datamx\|compranet-rupc\|RUPC\.csv"` sobre manifiesto/cola/alias → 0
  aciertos, candidata genuinamente nueva.
- **A.7**: doble descarga de `https://datamx.io/datastore/dump/5ef00daf-...?format=json`, sha256
  idéntico (`2e6c98ed3e557b239b331b746dc31b73dadf62c802923a53a9a38e0204cb3ee9`), 18 298 registros ×
  17 campos, verificado con `json.load` (no solo tamaño de archivo).
- **Registrado**: `python3 tests/manifiesto.py --registra --id rupc_datamx_json` →
  `RUPC_datamx_2019/compranet_rupc_datamx.json` en el corpus compartido (`/home/pc0/mm-corpus/raw/`),
  5 810 200 B, sha256 arriba.
- **Fila `RUPC` actualizada** (`upsert_fila`, misma clave): `estado_A4A5 =
  OBTENIDO-PARCIAL(RUPC histórico 2019 vía datamx.io; objeto vivo sigue
  NO-OBTENIDO-POR-ESTE-AGENTE)`, `ids_manifiesto` gana `rupc_datamx_json`. Vista regenerada.

**Límite honesto, declarado explícitamente:** es un **snapshot histórico** (fechas de inscripción
reales hasta 2019-04-25), **no** el RUPC vivo/actual. El host oficial que datamx.io cita como
fuente (`compranetinfo.hacienda.gob.mx/datosabiertos/RUPC.csv`) ya no resuelve por DNS. Una ruta
histórica adicional, documentada por dos repos de GitHub de 2018
(`siac.funcionpublica.gob.mx/DatosAbiertos/rupc/RUPC.csv` + diccionario en
`compranetinfo.funcionpublica.gob.mx`), tampoco resuelve hoy y **no tiene ninguna copia en
Wayback** — ruta muerta sin rastro, esquema de campos documentado pero irrecuperable.

**Por qué `norah/documentos` rechaza con 403 — explicado, no solo declarado.** Dos repos de
GitHub de terceros, independientes entre sí (`humandesignlab/veta`, actualizado jul-2026;
`javiercamarapp/atiende-licitaciones`, sep-2026), documentan y corroboran cruzadamente la misma
arquitectura: la API "Whitney" de ComprasMX (`upcp-cnetservicios.buengobierno.gob.mx/whitney/sitiopublico`)
hoy exige headers firmados (RSA, derivados de `adele/interoperabilidad/tp/reloj` — confirmado en
vivo, `200`, reloj de servidor real) — no se implementó ese esquema de firma (sería bypass de
anti-bot, fuera de alcance de `/sonda` y de este acto).

**Handoff declarado, NO ejecutado (fuera del alcance RUPC de este acto):** el mismo repo
documenta y esta sonda verificó EN VIVO tres rutas más de CompraNet, sin tocarlas más allá de un
`HEAD`/`curl` de verificación:
- `Contratos_CompraNet{2023,2024,2025}.csv` y `Expedientes_PICompraNet2025.csv` bajo
  `upcp-compranet.buengobierno.gob.mx/cnetassets/datos_abiertos_contratos_expedientes/` — `200`,
  72–188 MB cada uno, formato/vintage distinto a `Contratos_CompraNet5.xlsx` ya en corpus.
- API OCDS oficial `api.datos.gob.mx/v2/contratacionesabiertas` (300 265 registros confirmados
  vía Wayback a jul-2024) — hoy inalcanzable en vivo (TLS cortado, misma firma que
  `pub.bienestar.gob.mx`, confirmado con `openssl s_client` directo).
- El CSV histórico de 951 MB que apareció en esta misma búsqueda (`repodatos.atdt.gob.mx/api_update/sabg/...`)
  **ya está en corpus** — mismo tamaño exacto (951 619 345 B) que `compranet_historico.csv`,
  adquirido por `MAESTRA38-A4`. No es un hallazgo nuevo, se verificó para no duplicar.

**Negativo, ampliado y más riguroso:** CKAN datos.gob.mx censado ahora por **organización**
(`sabg`=22, `sfp`=11, `sesna`=28 datasets, 61 en total vía `package_search?fq=organization:<slug>`,
no solo por texto) — ninguno es el RUPC. `q=RUPC` da `count=0` en todo el catálogo. Esto es
"bloqueo de existencia" en esa fuente específica, no bloqueo técnico — el catálogo respondió
`200` en todos los intentos.

**Vía intentada y bloqueada por infraestructura ajena, declarada sin forzar:** `archive.today`
(y sus 5 espejos) rechazó **toda** conexión desde este entorno — TCP conecta, el servidor
mantiene el socket ~12s y corta el handshake TLS sin responder, en los 4 objetivos probados. Tres
mecanismos (curl HTTPS, curl HTTP puro, `openssl s_client`) confirman el mismo patrón; Google y
Wayback Machine responden con normalidad desde el mismo entorno en el mismo momento. La IP de
egreso de esta caja (`187.13.203.159`) pertenece a `AS212238 Datacamp Limited` — un ASN de
datacenter/proxy — que coincide con el comportamiento anti-scraping documentado de
`archive.today` contra rangos de datacenter. **Advertencia metodológica honesta:** esto no se
pudo distinguir de un bloqueo específico del servidor de destino en el caso de `archive.today`
mismo — pero para los bloqueos TLS de `pub.bienestar.gob.mx`/`cpid.bienestar.gob.mx`/
`consultapublicamx.inai.org.mx`/`api.datos.gob.mx` declarados como "del servidor" en esta nota,
la corroboración independiente de dos repos de terceros con infraestructura propia
(`humandesignlab/veta`, `javiercamarapp/atiende-licitaciones`) reportando el mismo tipo de
bloqueo sobre los mismos hosts reduce (no elimina) la probabilidad de que sea únicamente un
artefacto de la IP de esta caja. No se intentó (ni se intentará) enmascarar la IP de salida —
eso cruzaría de reconocimiento pasivo a evasión.

**Colateral — el endpoint `wayback/available` está roto ahora mismo.** Devuelve `404` genérico
para cualquier URL, incluyendo `example.com` como control — no es evidencia de ausencia de
captura, es una falla del propio servicio. Se documenta para que un acto futuro no lo tome como
señal; `web.archive.org/cdx/search/cdx` es el método fiable confirmado.

**Otras vías genuinas exploradas, sin hallazgo utilizable:** repositorios académicos
(Dataverse/Zenodo/ICPSR vía SHARE/DataCite) — un solo dataset real y tangencial (`COEP
Replication Package`, DOI `10.3886/E219822`, contratos marco/nómina, Pace University, bloqueado
por Cloudflare para ver su esquema exacto, alcance declarado como acotado y no equivalente al
RUPC); IMCO (`github.com/imco/IRC`) documentó una granularidad de CompraNet más fina
(participantes/licitantes por procedimiento) pero su único punto de acceso (bucket S3
`opi-compranet`) está confirmado **eliminado** (`NoSuchBucket` en los 9 archivos documentados);
MCCI/Data Cívica/Fundar/Serendipia/Animal Político — sin dataset relevante encontrado; PNT — las
3 rutas alternas en vivo confirmadas muertas (`api.plataformadetransparencia.org.mx` no existe en
DNS; `www.infomex.org.mx` es un dominio **secuestrado por un sitio de casino en línea**, no
usar/visitar pensando que es INAI; `consultapublicamx.inai.org.mx` resuelve pero corta TLS incluso
contra la IP directa vía `openssl s_client`) — Wayback sí reveló que el reto de Cloudflare existe
desde sep-2022 (no reciente) y que hay una captura de mayo-2023 con el formulario de búsqueda
real, sin utilidad para búsquedas en vivo hoy.

---

## P6 · Cierre (final, tras la ampliación)

| objeto | antes de CAJA | evidencia nueva | veredicto final | cambio material |
|---|---|---|---|---|
| R5.4 / ENADID `conoce_1..6` | `HIPÓTESIS-SIN-INSTRUMENTO` (candidata nominal sin verificar) | Descriptor `fd_enadid23.xlsx`, hoja `TMUJER1`: 6 variables = conocimiento de métodos anticonceptivos | `NO-ENCONTRADO-EN-ENADID2023` (falso positivo nominal) | Ninguno (solo esta nota) |
| RUPC | `NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)` | (a) Folio RUPC en `Contratos_CompraNet5.xlsx` (ya en corpus); (b) datamx.io/Codeando México republica el RUPC completo (18 298 registros, histórico 2019) — **adquirido**; (c) PNT/CKAN/archive.today/hosts oficiales negativos, ampliamente corroborados | `EXISTE-SATISFACE-PARCIAL` (histórico 2019, no el RUPC vivo) | **Sí** — `rupc_datamx_json` en manifiesto + corpus; fila `RUPC` → `OBTENIDO-PARCIAL`; vista regenerada |
| R7.9 / Bienestar | `HIPÓTESIS-SIN-INSTRUMENTO`; PUB/PREP ya en corpus | PUB: agregado por Entidad confirmado + agregado por Municipio parcial (3/32 estados, vía Wayback) + API de búsqueda nominal por nombre confirmada (patrón de URL, sin datos vistos); portal en vivo SIN-FETCH (TLS, corroborado por terceros); llave `AGEB`/manzana NO respaldada por el corpus actual (tope real: sección) | `ENLACE-POTENCIALMENTE-CONSTRUIBLE` (esquema, sin producto cartográfico adquirido) + `GRANULARIDAD-PARCIAL` (municipio, 3/32) + `SIN-FETCH` (portal en vivo) | Ninguno a `milpa`/canon; solo esta nota |

**CONTADORES (finales):**

```
N_reservas_PR632 = 3
N_reservas_resueltas = 3
N_candidatas_confirmadas = 2   (Folio RUPC en Contratos_CompraNet5.xlsx; RUPC completo vía datamx.io)
N_candidatas_descartadas = 1   (ENADID conoce_1..6, falso positivo nominal)
N_fuentes_adquiridas = 1   (rupc_datamx_json, A.7+A.8+registro completos)
N_handoffs_nuevos = 0   (una fila EXISTENTE de RUPC actualizada dos veces; ninguna fila nueva en la cola)
```

**CRITERIO DE ÉXITO cumplido, y superado en RUPC:** las tres reservas de `PR #632` dejaron de
ser "no verificables por NUBE" — RUPC pasó de negativo a una adquisición real (histórico 2019,
límite declarado); R7.9 ganó evidencia sustancialmente más rica (municipio parcial + API nominal
confirmada) sin cruzar ninguna línea de construcción de enlace/CALC; R5.4 cerró limpio.

**Suite final:**

```
python3 tests/check.py --baseline → LÍNEA BASE VERDE (sin cambio; corrida de nuevo tras la
  ampliación y la adquisición de rupc_datamx_json)
python3 tools/vista_cola_adquisicion.py → 134 filas, coherente con el registro (fila RUPC
  actualizada dos veces, ninguna fila nueva)
```

---

## Siguiente avance

**RUPC** ya tiene dato real adquirido (histórico 2019, 18 298 folios) — el siguiente paso, de
mesa, es decidir si ese corte satisface el uso original de la fila o si vale la pena perseguir
una versión más actual (ninguna ruta viva encontrada hoy; la única forma de actualizarlo sería
lograr acceso al RUPC oficial vigente, que sigue exigiendo sesión/firma anti-bot). **R7.9**
ganó el hallazgo más rico de los tres: existe una API de búsqueda nominal real y un agregado
municipal parcial, pero para construir el enlace a sección electoral hacen falta dos cosas que
hoy NO están en corpus — (a) el TLS de `pub.bienestar.gob.mx` respondiendo de nuevo (para
completar el agregado municipal a las 29 entidades faltantes, o para intentar `/api/resume/estate/{clave}/person/`),
y (b) el producto cartográfico real del INE a nivel manzana (el crosswalk ya en corpus solo
llega a sección) — ninguno de los dos se adquirió aquí, ambos declarados como huecos concretos,
no como excusa. **R5.4** queda cerrada como negativo limpio — sin vía abierta dentro de ENADID
2023; el siguiente paso sería `/sonda ... CONSTRUCTO` sobre otra familia de fuente, no otra sonda
sobre ENADID.

---

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015kCCqrpZ5K4RHWC7USW7wv
