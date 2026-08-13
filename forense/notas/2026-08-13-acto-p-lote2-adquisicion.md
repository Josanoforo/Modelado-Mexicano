# ACTO P·LOTE-2 · adquisición real del lote firmado por mesa

Worktree `/home/pc0/mm-p-lote2`, rama `acto-p/lote2-adquisicion`, base `origin/main` en `184882b` (5f90757 + PR #198 CENSO-v1.1, sin colisión de perímetro verificada antes de ramificar).

## Commit 1 · el lote congelado, antes de tocar red

### Lote firmado (§1, mesa)

5 fuentes, copiadas verbatim de `data/cola-adquisicion-2026-08-12.tsv` (8 columnas: fuente_canonica, n_necesidades_servidas, destraba_sin_ruta, destraba_condicional_faltante, celda_piloto_FIN, url_conocida, clasificacion_a4_previa, palanca):

1. **ENCOAP** (palanca 17) — `2:N2,N30` — destraba_sin_ruta NO — destraba_condicional: `N2:no representa ámbito rural; falta mapear variables y confirmar cuál desenlace financiero/social coincide con G5/R8.3 || N30:ruralidad y variables destino / no representa ámbito rural; falta mapear variables y confirmar cuál desenlace financiero/social coincide con G5/R8.3` — celda_piloto_FIN NO — `https://www.inegi.org.mx/programas/encoap/2023/default.html` — CANDIDATA(APERTURA_INDETERMINADA)
2. **CNGMD** (palanca 28) — `1:N28` — NO — `N28:falta saber si identifica comité, monitoreo, sanción, contribución sostenida y entorno rural/urbano; no observa persona` — NO — `https://www.inegi.org.mx/rnm/index.php/catalog/977` — CANDIDATA(APERTURA_INDETERMINADA)
3. **ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION** (palanca 33) — `1:N29` — NO — `N29:no identifica BNPL como modalidad separada ni incumplimiento de tanda entre desconocidos; comparabilidad anual por verificar` — NO — `https://www.banxico.org.mx/publicaciones-y-prensa/encuesta-de-competencias-financieras-de-la-poblaci/microdatos/competencias-financieras-mi.html` — CANDIDATA(APERTURA_INDETERMINADA)
4. **ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION** (palanca 31) — `1:N25` — NO — `N25:ids estables, cobertura y descarga` — NO — url_conocida **con el DOI erróneo aún sin corregir en este punto de la lectura**, `https://www.nature.com/articles/s41597-025-04999-0` (ver T1 abajo, §5.1) — CANDIDATA(APERTURA_INDETERMINADA)
5. **INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO** (palanca 12) — `2:N3,N17` — NO — `N3:traslado al objeto exacto / mapear equivalencia con sens_estatus y reclutamiento || N17:mapear equivalencia con sens_estatus y reclutamiento` — SI — `https://www.nature.com/articles/s41562-024-02043-y` — CANDIDATA(APERTURA_INDETERMINADA)

Fuera del lote, con razón dada por mesa: **JPAL_CorruptionInformation·30** — sin objeción de fondo, aplazada por ser la de menor palanca de las 6 candidatas del Grupo A. No se toca en este acto. Nada del Grupo B ni del Grupo C entra.

### Fila de puerta de SONDA-1 por fuente (mapa de barreras, ya pagado — `data/universo-puertas-2026-08-12.tsv`, fecha_sondeo 2026-08-12)

| fuente | puerta | clasificacion_a4 | condicion_acceso | universo_declarado (resumen) |
|---|---|---|---|---|
| ENCOAP·17 | `INEGI_ENCOAP_2023` | EXISTE-SATISFACE | libre, descarga directa sin registro ni sesión | Portada 200; JSON-LD trae señuelo `prueba.pdf` (soft-404 fijo, NO usado); mecanismo B (idBiinegi=3369 vía API descargamasiva) da URL real, GET -r 0-0 → 206, Content-Range 0-0/420306, zip real |
| CNGMD·28 | `RNM_CNGMD_2023_catalogo977` | EXISTE-SATISFACE | libre — ficha RNM declara "sitio de descarga directa" | Ficha 200; sin pestaña NADA "Get Microdata"; mecanismo B (idBiinegi=3298, tipoinformacion=12) da 87 archivos reales, uno verificado GET -r 0-0 → 206, Content-Range 0-0/2835380 |
| Banxico·33 | `Banxico_EncuestaCompetenciasFinancieras` | EXISTE-SATISFACE | libre, descarga directa sin registro ni sesión | Página 200 (16537 B, Latin-1); 6 enlaces .xlsx directos 2019–2024 sin formulario; ola 2024 verificada GET -r 0-0 → 206, Content-Range 0-0/1210013 |
| Zenodo·31 | `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal` | EXISTE-SATISFACE | libre, descarga directa sin registro ni sesión | Página real 200 -L (287370 B) con el DOI correcto `s41597-025-04918-9` (la cola trae el erróneo, ver T1); API Zenodo confirma 1 archivo, 739952144 B, access_right=open; GET -r 0-0 directo sobre el archivo también verificado |
| OSF·12 | `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico` | EXISTE-SATISFACE | libre, sin registro — API pública OSF, nodo `f7bzy` público | Artículo 200 -L (351081 B); OSF es SPA, sondeado vía API REST pública (`api.osf.io/v2/nodes/f7bzy/`); 10 archivos listados en `Data/`, incluye `Master_Data.dta` (1290938 B) |

### Criterio de cierre A.4, por fuente

EXISTE-SATISFACE para esta adquisición exige las cuatro condiciones a la vez: **(a)** payload íntegro en el corpus compartido (`/home/pc0/mm-corpus/raw`, no solo el worktree); **(b)** sha256 en `manifiesto.yaml` por su vía (`tests/manifiesto.py --escanea/--promueve`, nunca a mano); **(c)** decisión de adquisición por la vía del motor (`decide_acquisition.py`, el TSV de cola nunca se edita a mano para esto); **(d)** ficha/puerta nueva en el conducto. Si (a)-(c) sí y (d) no → EXISTE-NO-SATISFACE, declarando qué ficha se buscó y no se encontró. Registro gratuito sin fricción cuenta como hecho, no como NO-ACCESIBLE; pago o afiliación institucional sí cuenta como NO-ACCESIBLE, con receta manual.

### 4-bis · resultado del override, congelado ANTES de tocar red

Protocolo: sondeo crudo sin `dangerouslyDisableSandbox`, luego el mismo sondeo con override activo. El lote firmado usa 4 dominios distintos (no 5 — INEGI sirve tanto ENCOAP como CNGMD):

| dominio | fuente(s) | código SIN override | código CON override |
|---|---|---|---|
| www.inegi.org.mx | ENCOAP·17, CNGMD·28 | **200** | 200 |
| www.banxico.org.mx | Banxico·33 | **200** | 200 |
| zenodo.org | Zenodo·31 | **200** | 200 |
| osf.io | OSF·12 | **200** | 200 |

**Hallazgo que contradice la nota de SONDA-1 (relevante, se declara):** SONDA-1 registró que 7 de 9 dominios de su barrido exigieron override, incluyendo `zenodo.org` y `osf.io`. En esta sesión, los 4 dominios del lote firmado — incluidos zenodo.org y osf.io — respondieron 200 con contenido real (verificado por tamaño de descarga y `<title>`, no solo por el código: INEGI 153639 B/"Instituto Nacional de Estadística y Geografía (INEGI)", Banxico 27463 B, Zenodo 73554 B/"Zenodo", OSF 4207 B/"OSF") **sin necesidad de override alguno**. El tráfico pasa por un proxy local (`localhost:3128`) en ambos casos, con y sin la bandera. No se puede derivar de este acto si la política de sandbox cambió entre la sesión de SONDA-1 y esta, o si el entorno de ejecución (subagente de flujo de trabajo vs. sesión interactiva) tiene una lista de permitidos distinta — es un hecho de infraestructura fuera del perímetro de este acto, y se reporta sin especular más.

**Consecuencia para el lote:** ningún dominio bloquea. Las 5 fuentes firmadas siguen vivas para intento de descarga real; el paro por dominio (4-bis) no se activa para ninguna. Esto no prejuzga el resultado de la descarga íntegra (§4.1/4.2 de cada fuente) — SONDA-1 verificó portada y `GET -r 0-0`, no bajada completa; son dos hechos distintos (pre-registro de falsación, abajo).

### Pre-registro de falsación (B-bis)

SONDA-1 verificó portada y `GET -r 0-0`, no descarga completa. Que una fuente falle al bajar íntegra no refuta su sondeo: son dos hechos distintos — "la puerta responde" y "el payload bajó íntegro" — y se reportan con palabras distintas. Un lote que cierre con 3 de 5 está dentro de lo esperado. **El primer resultado que produzca este procedimiento es el que se reporta.**

## Commit 2 · la ejecución

### Resultado por fuente

**ENCOAP·17 — EXISTE-SATISFACE salvo (c), ver nota debajo.** El mecanismo B documentado por SONDA-1 (API `/app/api/descarga/componente/descargamasiva/lista/archivoscompaginacion?idBiinegi=3369&tipodocto=4`) devolvió **204 No Content** en esta sesión, de forma sistémica: probado con 7 valores de `tipodocto` (1-6, 12), con y sin cabeceras `Referer`/`X-Requested-With`, con cookie-jar de sesión real, con y sin `tipodocto`, y con 2 reintentos espaciados — siempre 204. Control de sanidad: el mismo endpoint con un `idBiinegi` inválido (`999999`) también devuelve 204 — el endpoint está caído para toda consulta en esta sesión, no es un problema del id. Una segunda ruta (adivinar la URL directa `/programas/encoap/2023/microdatos/bd_encoap2023.zip`) dio un soft-404 real de 13.370 bytes, `Content-Type: text/html`, título "Página no encontrada" — verificado, no asumido. La fuente real se recuperó por una **tercera ruta, no prevista por el encargo**: `data/curacion-universo/universo-declarado-t0.tsv` (tabla de otro dominio, Dominio 3) ya tenía una declaración T0 previa (`ACT-050e7d14027179aad03439ee`, `bd_encoap2023_csv.zip`, `/contenidos/programas/encoap/2023/microdatos/`) — verificada independientemente con `GET -r 0-0`: 206, `Content-Range 0-0/420306`, **coincide exacto** con el tamaño que SONDA-1 ya había reportado por la vía de la API (mismo archivo real, alcanzado por una ruta distinta). Descarga completa: 420.306 bytes exactos, zip válido (`file` confirma `Zip archive data`). Registrado en `manifiesto.yaml` como `inegi_encoap_2023_csv`.

**CNGMD·28 — NO OBTENIDO POR ESTE AGENTE.** Mismo síntoma que ENCOAP en la API (204 sistémico, incl. control de id inválido). El `contentUrl` del JSON-LD de la página real (`programas/cngmd/2023/`) apunta a `contenidos/programas/cngmd/2023/datosabiertos/ayuntamientos_cngmd2023_csv.zip` — verificado con `GET -r 0-0`: **es el señuelo soft-404 exacto de 2.263 bytes** que el encargo advirtió (mismo patrón que INEGI ya usa en ENCOAP/ENVIPE). Se buscó un rescate igual al de ENCOAP en `universo-declarado-t0.tsv`: CNGMD tiene 438 coincidencias en esa tabla, pero **solo para años 2011-2021 y 2025 (tabulados)** — ningún activo declarado para el microdato 2023 real ("Datos Abiertos", 87 archivos, `tipoinformacion=12`, el formato que INEGI introdujo específicamente para esa edición). El catálogo maestro huérfano `DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` (7.930 URLs, ajeno a este acto, solo consultado en lectura) tampoco tiene CNGMD más allá de 2019. Conclusión: la migración de CNGMD a "Datos Abiertos" en 2023 no está capturada en ninguna de las 3 fuentes de descubrimiento disponibles en esta caja; se necesita sesión de navegador real o que la API vuelva a funcionar. Receta manual (<1 min): abrir `https://www.inegi.org.mx/rnm/index.php/catalog/977`, pestaña real en `programas/cngmd/2023/` → tab "Datos abiertos" → descargar.

**Banxico_EncuestaCompetenciasFinancieras·33 — EXISTE-SATISFACE salvo (c).** Mecanismo de SONDA-1 reproducido sin cambios: 6 enlaces `.xlsx` directos en la portada (extraídos con Python/regex — el `grep -E` con `LC_ALL=C` que SONDA-1 documentó no funcionó en esta sesión, posible diferencia de locale del contenedor; Python evitó el problema). Ola 2024 verificada `GET -r 0-0`: 206, `Content-Range 0-0/1210013`. Descarga completa: 1.210.013 bytes exactos. Registrado como `banxico_encuesta_competencias_financieras_2024`.

**Zenodo_ElectoralPrecinctLevel·31 — EXISTE-SATISFACE salvo (c).** Récord de Zenodo re-consultado fresco (`api/records/14991955`): título, DOI y `access_right=open` coinciden exacto con SONDA-1. `GET -r 0-0`: 206, `Content-Range 0-0/739952144`. Descarga completa (2m19s, ~5.3 MB/s): 739.952.144 bytes exactos, **md5 `d1cbf7125ab6f2ffecf3d9f0e0ab125e` coincide byte a byte** con el reportado por la API de Zenodo. Registrado como `zenodo_electoral_precinct_level_mexico_municipal`.

**OSF_InteractingAsEquals·12 — EXISTE-SATISFACE salvo (c).** Nodo `f7bzy` re-consultado fresco: público, carpeta `Data/` con **10 archivos**, coincide exacto con el conteo de SONDA-1. SONDA-1 solo había listado metadatos (nombre+tamaño), sin abrir ningún archivo — este acto descargó los 10 completos: cada tamaño coincide exacto con el declarado por la API antes de bajar (verificación 1:1, no solo por total), firmas de tipo confirmadas (8 Stata Release 118, 1 CSV ASCII, 1 Excel 2007+ — ninguno es página de error). Registrados como 10 entradas `osf_iae_*` en `manifiesto.yaml`.

### Hallazgo que contradice a SONDA-1, reafirmado con el traspaso T3

4-bis ya declaró (Commit 1) que los 4 dominios del lote respondieron 200 real **sin** override, incluidos `zenodo.org` y `osf.io` — que SONDA-1 había registrado como bloqueados sin override. Este Commit 2 lo confirma con descargas completas exitosas en los 4 dominios, sin activar `dangerouslyDisableSandbox` en ningún momento. No se investiga la causa (fuera de perímetro); se dejan ambas mediciones (SONDA-1 y esta) como hechos de sesiones distintas.

### Criterio A.4(c) — hallazgo de alcance, no de una fuente

Las 4 fuentes cerradas cumplen (a) payload íntegro en el corpus compartido, (b) sha256 en `manifiesto.yaml`, y (d) ficha/puerta nueva en el conducto. Ninguna cumple (c) tal como el encargo lo exige ("decisión de adquisición por la vía del motor"): `tools/curador_registro/decide_acquisition.py` fue leído completo antes de invocarlo (per instrucción del encargo, "verifica que sigue corriéndose antes de usarlo") y **su esquema no tiene ninguna vía de decisión para una fuente de `cola-adquisicion-2026-08-12.tsv` que se acaba de adquirir** — sus dos únicas acciones posibles son `NO_ADQUIRIR_AHORA` (para el conjunto exacto de filas `DECLARADO_NO_ADQUIRIDO` de `universo-declarado-t0.tsv`, un universo de 35.517 activos T0 que no incluye a estas 5 fuentes por nombre) y `BUSQUEDA_DIRIGIDA` (para activos ya declarados en `activos-descubiertos-durante-ronda.tsv`, tampoco el caso). Esto **no es un hallazgo nuevo**: `data/INFRAESTRUCTURA-v1_0.md`, Dominio 2, trampa 5 (ya existente antes de este acto) ya documentaba que `cola-adquisicion` y `decisiones-adquisicion.tsv` son "dos mecanismos desconectados". Este acto lo reconfirma desde el lado de la ejecución real, no solo de la lectura de código. **Hallazgo + EN-ESPERA-DE-VÍA**, tal como el encargo previó para este caso exacto: no se editó `decisiones-adquisicion.tsv` a mano. Por tanto, la clasificación A.4 honesta de las 4 fuentes cerradas es **EXISTE-SATISFACE en (a)(b)(d), bloqueado estructuralmente en (c) por ausencia de vía del motor** — no un EXISTE-NO-SATISFACE por decisión pendiente ni un NO-ACCESIBLE por fricción de fuente.

## §5 · Los tres traspasos, cerrados

**T1 (DOI).** `data/cola-adquisicion-2026-08-12.tsv`, palanca 31: `url_conocida` corregida de `.../s41597-025-04999-0` a `.../s41597-025-04918-9`. `git diff --unified=0` confirma exactamente 1 línea, 1 campo tocado (mecanismo: split/join indexado por nombre de columna, nunca `csv.writer`).

**T2 (regla de lectura).** Añadida una línea a `data/INFRAESTRUCTURA-v1_0.md`, Dominio 2 (ítem 6 de "Trampas confirmadas"). Cifras verificadas en sesión: **62** filas `gap_mapeo_map_b` (conteo directo, sin ambigüedad). **15**: no se pudo re-derivar de forma confiable por fecha (otros actos del mismo 12/13-ago también escriben filas `EXISTE-SATISFACE`/`NO-OBTENIDO` en esta tabla — un primer intento de conteo por fecha dio 24, no 15, por esa mezcla) — se cita en cambio el autorreporte de SONDA-1 (nota §5 y su propio mensaje de commit `210b045`: "sondeo real de 15 fuentes, 15 puertas nuevas"; desglose 9+2+4+0=15 verificado que suma). Ningún campo de esquema ni test añadido, tal como pidió el encargo.

**T3 (override).** Resultado congelado en Commit 1 y reafirmado en Commit 2: los 4 dominios del lote alcanzables sin override en esta sesión. Ningún dominio forzado ni ninguna fuente movida al carril usuario por esta causa.

## §6 · El conducto de este acto — candidatos para ENLACE-2, derivados por comando

`relaciones.tsv` (Carril A, un solo escritor) **no se tocó**. Búsqueda por `fuente_canonica_normalizada` en `data/curacion-registro/relaciones.tsv` (solo lectura), para que ENLACE-2 no tenga que re-derivarla:

| payload (`id_manifiesto`) | fuente_canonica (cola) | `relacion_id` candidato(s) | nota |
|---|---|---|---|
| `inegi_encoap_2023_csv` | ENCOAP | `REL-d82eb6cef055001e7587db31` (N2) · `REL-1d4ea097a836307f28dd2f49` y `REL-2fab7f66a0e6963788542b3a` (N30, **duplicado — 2 filas para la misma necesidad**, no resuelto aquí) · `REL-8da82cf2f91efb7fe1958467` (N15) · `REL-e74ad11dd79c7485c9704116` (N16) | ENCOAP sirve 5 relaciones, no solo N2/N30 (la cola solo declaraba N2,N30 — N15/N16 están en `relaciones.tsv` pero no en la fila de cola de este lote) |
| `banxico_encuesta_competencias_financieras_2024` | ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION | `REL-63835b1a27c62356495d6104` (N29) | existe también `REL-87b4ab08a7e1b65f965ffb88` bajo el nombre variante `..._2019_2024` (mismo N29) — **dos filas para lo que parece la misma fuente con dos ortografías**, no resuelto aquí |
| `zenodo_electoral_precinct_level_mexico_municipal` | ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION | `REL-374d073941162109bb37265b` (N25) | 1 sola fila, sin ambigüedad |
| `osf_iae_*` (10 archivos) | INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO | `REL-10b7203dd243231cb3602e47` (N17) · `REL-71d03c31e21a53076736dfd0` y `REL-f0cb8d6fa174935fae071144` (N3, **duplicado — 2 filas para la misma necesidad**, no resuelto aquí) | — |
| — | CNGMD | `REL-e10120bebb9ed07d210a3a86` (N28) | no adquirido en este acto — candidato queda para el siguiente lote |

Los duplicados (N30 de ENCOAP, N29 de Banxico con nombre variante, N3 de OSF) se reportan tal cual se encontraron — decidir cuál fila enlazar (o si fusionarlas) es del Carril A, no de este acto.

## §7 · CONTADOR — PRISMA de 7 cifras

| intentadas | sondeadas-200 | bajadas | íntegras | con-ficha | no-accesibles | no-obtenidas |
|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 4 | 4 | 0 | 1 |

4 payloads nuevos íntegros en el corpus compartido (13 entradas de `manifiesto.yaml`: 1 ENCOAP + 1 Banxico + 1 Zenodo + 10 OSF). Necesidades cuyo estado cambia por disponibilidad real de payload (no de relación — `relaciones.tsv` no se tocó, ver §6): N2, N3, N17, N25, N29, N30. No capa2.

**Verificación PR#77:** confirmado con `ls -la` directo sobre `/home/pc0/mm-corpus/raw/` (no el symlink del worktree) — los 4 payloads están físicamente en el corpus compartido: `banxico_encuesta_competencias_financieras_2024.xlsx` (1.210.013 B), `inegi_encoap_2023_csv.zip` (420.306 B), `zenodo_electoral_precinct_level_mexico_municipal.zip` (739.952.144 B), `osf_interacting_as_equals/` (10 archivos, 2.321.478 B).

**Línea honesta:** el lote firmado admitía cerrar en 3 de 5. Cerró en **4 de 5** — mejor que el piso autorizado por mesa, por una vía (`universo-declarado-t0.tsv`) que ni el encargo ni SONDA-1 habían anticipado para ENCOAP. CNGMD queda genuinamente NO OBTENIDO, no forzado.

## §8 · Confirmación de guardas

No se tocó `relaciones.tsv`, `canon/**`, `milpa/**`, `tools/**`, `tests/**`, ninguna fila ajena de ningún TSV, GDELT, UCDP, ni JPAL. `data/curacion-universo/decisiones-adquisicion.tsv` no se editó a mano (hallazgo EN-ESPERA-DE-VÍA en su lugar, ver arriba). Efecto lateral menor y correcto: `data/manifiesto-staging.yaml` ahora incluye una entrada `PENDIENTE` para `DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` (archivo huérfano preexistente en el corpus compartido, ajeno a este acto) — es el comportamiento normal de `--escanea data_raw`, no una edición deliberada; se deja tal cual para quien sea dueño de ese archivo.
