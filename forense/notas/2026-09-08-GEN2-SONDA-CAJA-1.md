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

## P6 · Cierre

| objeto | antes de CAJA | evidencia nueva | veredicto | cambio material |
|---|---|---|---|---|
| R5.4 / ENADID `conoce_1..6` | `HIPÓTESIS-SIN-INSTRUMENTO` (candidata nominal sin verificar) | Descriptor `fd_enadid23.xlsx`, hoja `TMUJER1`: 6 variables = conocimiento de métodos anticonceptivos | `NO-ENCONTRADO-EN-ENADID2023` (falso positivo nominal) | Ninguno (solo esta nota) |
| RUPC | `NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)`, 3 laterales SIN-FETCH sin ejecutar | (a) Folio RUPC en `Contratos_CompraNet5.xlsx` ya OBTENIDO (72.6% cobertura); (b) Cloudflare challenge confirmado 3 mecanismos; (c) 0 datasets RUPC-nacional en CKAN | Objeto original sigue `NO-OBTENIDO-POR-ESTE-AGENTE`; hallazgo colateral (a) ya en corpus | Fila `RUPC` actualizada (nota + estado), vista regenerada |
| R7.9 / Bienestar | `HIPÓTESIS-SIN-INSTRUMENTO`; PUB/PREP ya en corpus, granularidad no verificada en CAJA | PUB confirmado agregado (de nuevo); PREP confirma `SECCION`; portal nominal SIN-FETCH (TLS, 3 mecanismos); Anexo 2 archivado (Wayback) revela esquema con `AGEB`/`CLAVE_MZNA`/domicilio | `ENLACE-POTENCIALMENTE-CONSTRUIBLE` (esquema) + `SIN-FETCH`/agregado (acceso hoy) | Ninguno (solo esta nota) |

**CONTADORES:**

```
N_reservas_PR632 = 3
N_reservas_resueltas = 3   (las tres pasaron de "no verificable por NUBE" a evidencia real de CAJA, positiva o negativa)
N_candidatas_confirmadas = 1   (Folio RUPC en Contratos_CompraNet5.xlsx, ya en corpus)
N_candidatas_descartadas = 1   (ENADID conoce_1..6, falso positivo nominal)
N_fuentes_adquiridas = 0   (todo lo usado ya estaba en corpus; nada nuevo descargado ni registrado en manifiesto)
N_handoffs_nuevos = 0   (una fila EXISTENTE actualizada, ninguna fila nueva)
```

**CRITERIO DE ÉXITO cumplido:** las tres reservas de `PR #632` dejaron de ser "no
verificables por NUBE" — cada una tiene ahora evidencia obtenida en CAJA con red real,
positiva (R5.4: negativo acotado con causa; RUPC: hallazgo colateral confirmado) o mixta
(R7.9: esquema con llave defendible, acceso aún bloqueado, ambos declarados con precisión).

**Suite final:**

```
python3 tests/check.py --baseline → LÍNEA BASE VERDE (sin cambio respecto al arranque)
python3 tools/vista_cola_adquisicion.py → 134 filas, coherente con el registro
```

---

## Siguiente avance

De las tres, **RUPC** es la que queda más lista para un paso de medición/adquisición real
inmediato: el Folio RUPC ya está en corpus (`compranet5_contratos_2022_2023_xlsx`), sin
necesidad de ninguna adquisición nueva — lo único que falta es que mesa decida si ese nivel
(folio por contrato, sin domicilio/estatus/historial de sanciones) satisface el uso que
motivó la fila, o si vale la pena seguir con sesión de navegador real contra PNT/`norah`
para el padrón completo. R7.9 quedó con el hallazgo más rico (esquema con llave geográfica
defendible) pero requiere un paso adicional no trivial (verificar "Descarga por Municipio"
en vivo cuando el TLS del host responda, o conseguir el Marco Geográfico Electoral del INE a
nivel manzana) antes de ser candidata a spec. R5.4 queda cerrada como negativo — sin vía
abierta dentro de ENADID 2023; si se busca instrumento para esta hipótesis, el siguiente
paso sería `/sonda ... CONSTRUCTO` sobre otra familia de fuente, no otra sonda sobre ENADID.

---

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015kCCqrpZ5K4RHWC7USW7wv
