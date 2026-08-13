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
