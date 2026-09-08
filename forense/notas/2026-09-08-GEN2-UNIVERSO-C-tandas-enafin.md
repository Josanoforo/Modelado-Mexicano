# ACTO GEN2-UNIVERSO-C · TANDAS Y ENAFIN — el universo conocido no limita la exploración del desconocido

Firma de mesa que gobierna el acto (verbatim, 8/sep/2026): «Si no tenemos la
data completa la descargamos, o buscamos paralelos, o datos de otras fuentes,
que lo que tengamos "universo conocido" no nos limite de explorar el Universo
Desconocido.»

Entorno: CAJA (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`), red real
verificada (`curl` a inegi.org.mx → 200), corpus montado (`data/raw` enlazado,
`data/raices.local.yaml` con `descargas_mx`; 398 archivos examinados por
`tools/entorno.py` al abrir). A.15 primero: los inventarios canónicos
consultados antes de sondear nada son
`data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md`
(30/jul/2026) y `data/curacion-registro/cola-adquisicion-registro.tsv` (filas
9, 10, 40, 41, 50).

---

## §1 · P1 — ENAFIN, la ruta directa

### 1.a · Inventario completo, contra el árbol de hoy (A.15)

El inventario canónico ya cataloga ENAFIN (§C.15) y sus paralelos de crédito/
ahorro (§A-B, 14 fuentes). La cola de adquisición (fila 50, `ids_manifiesto`)
ya trae **10 payloads** `ADQ15_ENAFIN_2024_RNM_INEGI/*` obtenidos desde
18/ago/2026, y la propia nota de la fila ya declaraba, dos veces (4/sep, 6/sep),
que "tabulados ENAFIN ya en corpus no lo traen" [el cruce que N19 pide] y que
el microdato de empresa es `NO-OBTENIDO-POR-ESTE-AGENTE, razon EXIGE-CUENTA`.

**Ninguna de esas dos afirmaciones sobrevive la re-verificación de hoy.**

**Hallazgo central (A.8, con orgullo — el objeto ya estaba en el corpus):**
`data/manifiesto.yaml` (`id: adq15_enafin_conjunto_de_datos_enafin_2024_csv`,
sha256 `0f0ff75db3b728f218e33210c9eb08e0c20ec04fe4317aacacfef45ab8cb5e45`,
descargado 18/ago/2026) es el ZIP de datos abiertos de ENAFIN 2024
(`conjunto_de_datos_enafin_2024_csv.zip`, re-descargado hoy y verificado
sha256 idéntico). Dentro, `tr_enafin_tam_sec_loc_2024.csv` (11 filas,
`DOMINIO_ESTUDIO` = Total · Grande · Mediana · Pequeña · Micro · Sector
construcción · Sector industrias manufactureras · Sectores de comercio ·
Sectores de servicios · 500 000 y más habitantes · 50 000 a 499 999
habitantes) trae, entre 2 971 columnas (ver diccionario adjunto en el mismo
ZIP), el bloque **51** completo:

- `K_51`/`X_51`/`AK_51` — "Número de empresas según factores que han limitado
  el acceso al financiamiento en los últimos 12 meses, por escala, 2024 …
  **No tiene historial crediticio**" (limita mucho / poco / nada), **por cada
  uno de los 11 dominios de estudio** (verificado con `python3 -c` sobre el
  CSV: fila Total → 25 656 / 41 927 / 212 464 empresas estimadas; fila Micro →
  16 122 / 22 284 / 111 733; fila Grande → 611 / 1 638 / 10 893 — la cifra
  varía por segmento, no es un valor repetido).
- `H_43`/`I_43`/`D_44` — motivos por los que las empresas no solicitaron
  crédito: "Lo han rechazado anteriormente" / "Tiene mal historial
  crediticio" / "Cuenta con mal historial crediticio", también por los 11
  dominios.

Esto **es** el cruce exacto que `N19` pide, **por segmento** (tamaño de
empresa, sector, tamaño de localidad), publicado por INEGI sin registro,
sentado en el corpus desde hace 21 días sin que ningún acto anterior abriera
el diccionario de datos completo (2 971 filas) para encontrarlo — dos actos
(`MAESTRA38-N4` 4/sep, `MAESTRA38-A4` 6/sep) declararon el tabulado
insuficiente sin haber mirado más allá de la cabecera.

**Clasificación (A.4):** `EXISTE-SATISFACE` para la pieza "por segmento" de
`N19` — universo examinado: el ZIP completo de datos abiertos ENAFIN 2024 (2
CSV + 2 diccionarios + 1 metadato, 5 archivos), mecanismo: lectura completa de
ambos diccionarios de datos con `python3`/`csv`, fecha: 8/sep/2026.

### 1.b · Microdato de empresa (registro individual) — sigue NO-ACCESIBLE, receta re-verificada

El propio ZIP de datos abiertos (`licencia` en el manifiesto, ya correcta) y
el catálogo RNM ya en corpus (`ADQ15_ENAFIN_2024_RNM_INEGI/enafin2024_rnm_catalog.html`,
sha256 ya registrado) declaran, verbatim (grep con `python3`, no `ugrep`, por
A.13 — el archivo tiene bytes no-UTF8 y `grep`/`ugrep -I` lo descarta en
silencio):

> "… a la información de microdatos de manera indirecta a través del
> siguiente mecanismo: Laboratorio de análisis de datos para servidores
> públicos del Estado Mexicano, funcionarios de organismos internacionales e
> investigadores y estudiantes calificados, a través del vínculo:
> https://www.inegi.org.mx/microdatos/"

**Clasificación (A.4/A.5):** `NO-ACCESIBLE` para el microdato de empresa —
universo examinado: 2 páginas del catálogo RNM de ENAFIN 2024, mecanismo:
lectura completa de HTML con decodificación UTF-8 explícita, fecha: 8/sep/2026.
**Receta institucional para mesa** (≤1 min de lectura, no de ejecución — este
trámite no es de navegador): Laboratorio de Microdatos INEGI, presencial,
instalaciones del productor; solicitante debe ser servidor público mexicano,
funcionario de organismo internacional, o investigador/estudiante calificado;
trámite vía https://www.inegi.org.mx/microdatos/. No es el patrón de
credencial-por-navegador que rompió WBES (§1.c) — es presencial, sin plazo
publicado en esta página.

### 1.c · Paralelos

**WBES/Enterprise Surveys México (hermana citada por la propia cola, filas 9
y 10).** Ya `OBTENIDO` en el corpus desde el 1/sep/2026 por `ACTO
MAESTRA34-A1` (mesa-navegador rompió el muro de credencial) — **este hecho
tampoco había sido cruzado contra N19 hasta hoy**. Abierto con `pyreadstat`
(`Mexico-2023-full-data.dta`, 1322×357): trae `k20a1` ("What Was The Outcome
Of That Most Recent Application For Loan/Line of Credit?" — 1=aprobada
completa, 2=aprobada parcial, 3=**rechazada**, 4=retirada; 58 rechazos de 1322
empresas) y `k17` ("Main Reason For Not Applying" — incluye "Did not think it
would be approved", proxy de autoexclusión, no de rechazo institucional por
historial). Segmentación disponible: `a6a`/`a6b`/`a6c` (tamaño de muestreo),
`stratificationsectorcode`, `stratificationregioncode`, `stratificationsizecode`.
**Clasificación:** `EXISTE-SATISFACE-PARCIAL` — trae rechazo por segmento,
pero ninguna variable codifica la RAZÓN del rechazo (no existe un análogo a
`k20a1` con desglose de motivo); no sustituye al hallazgo de §1.a, lo
corrobora desde otro ángulo (outcome vs. factor limitante autopercibido).

**ENIF.** Ya evaluado por `ACTO MAESTRA38-A6` (6/sep/2026, cita en la propia
fila 40 de la cola): `PARALELA-NINGUNA` para tandas. No se re-abrió aquí — A.8
contra medición ya corrida (`ADR-340`): repetirlo sería el defecto que esa
regla existe para evitar.

**CNBV bases abiertas (BDIF, PI, Ahorro Financiero — inventario §A.1-3).**
Las tres son agregados por institución/región, no microdato ni por motivo de
rechazo — confirmado por lectura del inventario, no por sondeo nuevo (A.15: el
inventario ya declara "no publica microdatos a nivel persona" para las tres).
`EXISTE-NO-SATISFACE`.

**Global Findex 2025 (Banco Mundial, México incluido).** Archivo país
público, sin registro (`GlobalFindexDatabase2025.csv`, 438 columnas ×
países×grupo demográfico, descargado hoy de
`thedocs.worldbank.org/.../GlobalFindexDatabase2025.csv`, sha256 abajo).
Búsqueda completa de las 438 columnas: **ninguna** columna captura razón de
rechazo de crédito ni historial crediticio (las columnas de crédito son
`borrow_any_t_d` y análogas — "pidió prestado sí/no", sin motivo). El
microdato individual (que sí traería reactivos de razón) vive en
`microdata.worldbank.org`, mismo patrón de credencial que WBES
(`HTTP 401 → /auth/login`, confirmado hoy) — mismo tipo de cuenta que mesa ya
abrió para WBES, no necesariamente la misma cuenta. **No se persigue**: el
archivo público ya descarta que Findex tenga el reactivo exacto, así que subir
el costo de una cuenta nueva no compra nada que ENAFIN (§1.a) no dé ya mejor.
`EXISTE-NO-SATISFACE` para el archivo público; `DECISIÓN-DE-MESA-PENDIENTE`
para el microdato (de bajo rendimiento esperado, declarado así).

---

## §2 · P2 — Tandas, el universo desconocido

Las dos bases comerciales (`REGISTRO_DE_TANDAS_Y_REPUTACION` / tanda.mx,
`REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` / Tanda+) quedan **sin tocar**, tal
como manda el encargo — filas 40/41 de la cola, `NO-ADQUIRIDA-POR-COSTO`,
convenio.

### 2.a · Datasets académicos de ROSCA con microdato depositado

Búsqueda web (4 consultas: inglés/español, por plataforma — Dataverse, ICPSR,
Zenodo, OSF — y por institución mexicana). **Ningún dataset mexicano de
tandas/ROSCA con microdato depositado en repositorio abierto localizado.**
Candidata más cercana, abierta byte a byte (A.6, no `SIN-FETCH`): Fujiwara,
Kanemoto y otros, "Reciprocity and exclusion in informal financial
institutions" (PMC6114866) — experimento de laboratorio en el Tokyo Institute
of Technology (diciembre 2011–junio 2013), **no México** — mide exactamente
reputación (contribuciones previas), exclusión (votación) e incumplimiento,
pero sobre población japonesa de laboratorio. `EXISTE-NO-SATISFACE` (universo
correcto de mecanismo, universo incorrecto de población — no sustituye a un
dato mexicano). Datos declarados en ResearchGate del autor, no en repositorio
estándar — no se persiguió (bajo rendimiento esperado: no es México).
Referencias institucionales de México encontradas sin dataset específico
confirmado (repositorio-digital.cide.edu, repositorio.colmex.mx) quedan
`SIN-FETCH` — no abiertas byte a byte, ninguna prometía un dataset de tandas
en el título del resultado de búsqueda.

### 2.b · ENIF y ENSAFI — inventario por instrumento completo

**ENSAFI 2023.** Microdato ya `OBTENIDO` en el corpus desde 4/ago/2026
(`ensafi2023_bd_csv_zip`, "no se abrió ni extrajo" — nota original). Abierto
hoy por primera vez: el descriptor de archivos (`ensafi2023_fd_xlsx_zip`,
también ya en corpus) trae en `TMODULO` (998 filas × 8 columnas) el bloque
completo `P6_1_*` a `P6_13` (mecanismos de ahorro informal, sección 6 del
cuestionario). Reactivo exacto:

> `P6_1_5` — "6.1 Actualmente, ¿usted participa en una tanda?" (Sí/No,
> persona)

Además `P6_5_1` (deuda en caja de ahorro del trabajo/conocidos), `P6_7`
("¿usted se ha atrasado en el pago de uno de estos préstamos o créditos?" —
pero remite al bloque `P6_6`, tarjetas/créditos formales y semi-formales, NO
al bloque `P6_1` de tandas/cajas informales) y `P6_10_7`/`P6_10_8` (atraso
general / recurrió a prestamistas para cubrir gastos, sin atar el atraso a la
tanda específicamente).

**Clasificación (A.15 — universo completo del bloque 6 examinado, 998 filas
del descriptor, comando `openpyxl` sobre las 4 hojas):** `EXISTE-SATISFACE-PARCIAL`
para `R8.2`/`N29` — ENSAFI mide **participación** en tanda (binaria, por
persona, cruzable con toda la demografía de `TSDEM`/`THOGAR`), pero **ninguna**
pregunta liga el atraso/incumplimiento de pago (`P6_7`) específicamente a la
tanda — el atraso medido es sobre créditos formales/semi-formales (`P6_6`),
no sobre el mecanismo de ahorro informal (`P6_1`). No hay reactivo de
reputación (expulsión, confianza, orden de turno) en ningún bloque del
cuestionario. La necesidad de modelo (reputación/incumplimiento *dentro* de
la tanda) sigue sin instrumento; la necesidad adyacente (quién participa en
tandas, con qué perfil) sí queda satisfecha y no estaba explotada.

**ENIF.** No re-sondeada — ver §1.c, ya evaluada `PARALELA-NINGUNA` por acto
previo (A.8 contra medición ya corrida).

### 2.c · CONDUSEF / CNBV

Sondeo web de hoy: CONDUSEF declara explícitamente que **no** tramita quejas
contra cajas de ahorro **no autorizadas** — las remite al Ministerio Público
o a FIPAGO; su Registro de Prestadores (SIPRES) y el Buró de Entidades
Financieras cubren únicamente instituciones **reguladas** (cooperativas y
SOFIPOS con autorización CNBV, verificables en focoop.com.mx). Una tanda no es
una entidad regulada — no tiene registro, no tiene queja tramitable, no tiene
microdato. `EXISTE-NO-SATISFACE`, universo examinado: 8 páginas
institucionales de condusef.gob.mx sobre registro y quejas, mecanismo:
búsqueda + lectura de resultados, fecha: 8/sep/2026. Esto no es una novedad
respecto del inventario (§A.6, REDECO/REUNE ya declarado "universo de quejas,
no muestra"), pero hoy queda confirmado que el mecanismo administrativo
**excluye por diseño** al objeto (tandas), no solo que no lo cubre por
casualidad.

### 2.d · Literatura mexicana con datos de réplica

Ver §2.a — CIDE/Colmex/UNAM no rindieron un dataset específico de tandas en
esta sesión; los resultados de búsqueda mencionan a los tres como
instituciones activas en el tema pero ningún resultado individual apuntó a un
repositorio con microdato depositado. `SIN-FETCH`, no perseguido más allá —
bajo rendimiento esperado de una búsqueda adicional sin nombre de autor/paper
concreto que perseguir.

---

## §3 · P3 — El mapa de vuelta a mesa

| Fuente | Clasificación A.4 | Qué cubre del hueco | Costo de la ruta que queda | Recomendación |
|---|---|---|---|---|
| ENAFIN 2024, tabulado abierto (ya en corpus) | `EXISTE-SATISFACE` | N19 por segmento (tamaño/sector/localidad) — historial crediticio como factor limitante | Cero — ya está, ya se leyó | Usar directamente; es el dato de N19, no hace falta nada más |
| ENAFIN, microdato de empresa | `NO-ACCESIBLE` | N19 a nivel establecimiento individual | Trámite presencial, Laboratorio de Microdatos INEGI (servidor público / investigador calificado) | No perseguir — el tabulado ya satisface; solo si mesa necesita nivel-empresa por otra razón |
| WBES México 2023 (ya en corpus) | `EXISTE-SATISFACE-PARCIAL` | Rechazo de crédito por segmento (tamaño/sector/región) — sin razón codificada | Cero — ya está, ya se leyó | Corrobora ENAFIN desde otro ángulo; no sustituye |
| ENSAFI 2023 (ya en corpus) | `EXISTE-SATISFACE-PARCIAL` | Participación en tanda por persona/segmento demográfico | Cero — ya está, ya se leyó | Usar para "quién participa"; no cubre reputación/incumplimiento |
| Global Findex 2025, archivo país (bajado hoy) | `EXISTE-NO-SATISFACE` | Nada específico — sin reactivo de razón de rechazo | Cero para el archivo país; cuenta gratuita en microdata.worldbank.org para el microdato individual | No perseguir — el público ya descarta el reactivo exacto |
| ROSCA lab Japón (PMC6114866) | `EXISTE-NO-SATISFACE` | Mecanismo de reputación/exclusión, pero población equivocada | Datos en ResearchGate del autor, sin cuenta institucional | No perseguir — no es México |
| CONDUSEF/CNBV (tandas) | `EXISTE-NO-SATISFACE` | Nada — excluidas por diseño regulatorio | N/A | Cerrar la vía; no hay registro que perseguir |
| CIDE/Colmex/UNAM (repositorios) | `SIN-FETCH` | Desconocido — sin dataset específico localizado | Búsqueda dirigida por autor/paper concreto (horas, no minutos) | DECISIÓN-DE-MESA-PENDIENTE si se quiere insistir |
| Tanda.mx / tandamas.mx (comercial) | `NO-ADQUIRIDA-POR-COSTO` | R8.2/N29 completo, si se accede | Convenio (semanas-meses) | Sin cambio — fuera de perímetro de este acto |
| Tanda+ (comercial) | `NO-ADQUIRIDA-POR-COSTO` | R8.2/N29 completo, si se accede | Convenio, contacto equipo@tandamas.mx | Sin cambio — fuera de perímetro de este acto |

**Conclusión para mesa, en una línea por hueco:** el hueco de **ENAFIN/N19**
se cierra hoy — el dato ya estaba en el corpus, segmentado, sin que nadie lo
hubiera leído completo; el hueco de **tandas/R8.2/N29** sigue abierto — el
universo desconocido explorado hoy (académico, ENIF/ENSAFI, CONDUSEF/CNBV) no
rindió una fuente con reputación/incumplimiento dentro de la tanda, y las dos
únicas fuentes que sí lo tendrían siguen en convenio comercial, tal como ya
se sabía.
