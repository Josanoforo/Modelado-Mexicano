# ACTO SONDA-1 · El mapa de barreras que le falta a la firma del Lote 2

`ENCARGO ACTO SONDA-1`, 12/ago/2026 (`forense/encargos/2026-08-12-sonda1-mapa-barreras-lote2.md`), archivado como primer commit de este acto (regla A.3). Base declarada por el encargo: `origin/main = b17a6f6`. Worktree `/home/pc0/mm-sonda1`, rama `sonda1-mapa-barreras-lote2`.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-sonda1` (`git worktree add -b sonda1-mapa-barreras-lote2 /home/pc0/mm-sonda1 origin/main`). `git log -1`: `b17a6f6 Merge pull request #195 from Josanoforo/z/inventario-curador-20260812-184630`. `git status`: árbol limpio al abrir.
   - `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy` — misma contención conocida de esta máquina (memoria de sesión: `project_modelado_mexicano_git_config_contention.md`). Verificado independientemente: `git log -1` quedó en `b17a6f6`, `git status` limpio, `git worktree list` lo lista — la creación no falló, solo la escritura de metadato de tracking.
2. **SHA.** `origin/main = b17a6f6` — exactamente el SHA contra el que se redactó el encargo (`git merge-base --is-ancestor b17a6f6 origin/main` → confirmado ancestro, de hecho es la punta misma). Sin deriva que re-derivar.
3. **data/raw.** Ausente (`ls data/raw` → `No such file or directory`). Esperado — este acto no descarga, así que no se crea ni se enlaza.
4. **ENTORNO.** `echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]"` → `[]` (sin variable, firma de caja). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. Firma de caja-con-red-a-dominios-de-datos confirmada, entorno correcto para este acto.
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de este worktree o de comandos de red corridos en esta sesión, con el comando a la vista.

Las cinco líneas cuadran con lo que el encargo supone. Sin PARO.

## 1 · Premisas (crudas, comando a la vista)

```
$ ls data/cola-adquisicion-*.tsv | sort | tail -1
data/cola-adquisicion-2026-08-12.tsv

$ awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l
99

$ awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l
62
```

Coincide exactamente con lo que el encargo reporta (62 filas `gap_mapeo_map_b`, cola vigente `2026-08-12`). Acto habilitado.

**Premisa que podía PARAR el acto — leída íntegra:** `forense/notas/2026-08-12-acto-p-lote1-adquisicion.md` (493 líneas). Hallazgos relevantes para este lote:

- §5.1-§5.5 mapean barreras de **GESIS/ISSP** (Cloudflare, bloqueo a nivel de dominio, 403 idéntico con/sin sandbox), **WVS** (SPA, `AJDownload.jsp` exige sesión autenticada, devuelve 1 byte a `curl` anónimo), **Banco Mundial catálogo 2661** (pestaña "Documentation" libre, pestaña "Get Microdata" exige cuenta NADA gratuita — registro ejecutado por el agente, `jonieqsa@gmail.com`, activación pendiente de correo en ese momento), **GPS/briq** (do-files libres, dataset real exige formulario Laravel con correo — enviado, entrega declarada por correo), **CSES** (sin barrera, `cses.org` fuera del allowlist de red de la caja — requiere override de sandbox, no es bloqueo del portal).
- **Ninguna de las 15 fuentes de este lote es GESIS/ISSP, WVS, Banco Mundial catálogo 2661, GPS o CSES** — no hay barrera ya documentada que citar en vez de sondear, fuente por fuente. Pero **sí hay 3 fuentes de este lote en el mismo dominio ya mapeado** (`microdata.worldbank.org`, palancas 9/23/35, catálogos 6453/2049/1039 — distintos de 2661): el patrón de dominio (documentación libre, "Get Microdata" gateado tras cuenta NADA) es contexto directamente aplicable, y la cuenta `jonieqsa@gmail.com` ya existe — si cualquiera de las 3 pide login, no se registra una cuenta nueva, se cita la existente (§13 de la nota P·Lote-1 registra que el usuario confirmó activación el 2026-08-13, ver `universo-puertas` fila `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661`).
- §11 (sesión de continuación) registra que el usuario cerró WVS e ISSP por su propio carril (`descargas_mx`) después del bloqueo que el agente reportó — confirma la contra-regla B-bis del encargo: NO OBTENIDO POR ESTE AGENTE no es fracaso final, es traspaso de carril.

## 2 · Re-derivación del filtro de 15 fuentes (no copiado del encargo — corrido en esta sesión)

```
$ awk -F'\t' 'NR>1' data/cola-adquisicion-2026-08-12.tsv | wc -l
54

$ awk -F'\t' 'NR>1 && $6 ~ /^http/ {print $8"\t"$1"\t"$7}' data/cola-adquisicion-2026-08-12.tsv | sort -n
1  ISSP                                                              CANDIDATAx13+NEGATIVAx1
2  ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER       NEGATIVA(CURADURIA_SEMANTICA_MULTI2)
4  EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014     CANDIDATA(APERTURA_INDETERMINADA)
5  IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016               NEGATIVA(APERTURA_NEGATIVA_EXPLICITA)
6  GPS                                                                CANDIDATA(APERTURA_INDETERMINADA)
7  CSES                                                                CANDIDATA(APERTURA_INDETERMINADA)
9  WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023                          CANDIDATAx3+NEGATIVAx3
11 GDELT                                                               CANDIDATA(APERTURA_INDETERMINADA)
12 INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO      CANDIDATA(APERTURA_INDETERMINADA)
14 MASS_MOBILIZATION_PROTEST_DATA                                     CANDIDATA(APERTURA_INDETERMINADA)
16 UCDP                                                                CANDIDATAx2+NEGATIVAx2
17 ENCOAP                                                              CANDIDATA(APERTURA_INDETERMINADA)
18 MEXICO_PANEL_STUDY_2012                                             CANDIDATA(APERTURA_INDETERMINADA)
23 LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2   CANDIDATA(APERTURA_INDETERMINADA)
25 MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP   CANDIDATA(APERTURA_INDETERMINADA)
28 CNGMD                                                               CANDIDATA(APERTURA_INDETERMINADA)
30 DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE    CANDIDATA(APERTURA_INDETERMINADA)
31 ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION   CANDIDATA(APERTURA_INDETERMINADA)
33 ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION         CANDIDATA(APERTURA_INDETERMINADA)
35 IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM                  CANDIDATA(APERTURA_INDETERMINADA)
36 OECD                                                                CANDIDATA(APERTURA_INDETERMINADA)
38 PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND           CANDIDATA(APERTURA_INDETERMINADA)
```

22 filas con `url_conocida` con `http`. Exclusiones, cada una verificada contra `data/universo-puertas-2026-08-12.tsv` (no solo contra la cola):

- **ISSP·1, CSES·7** — cerradas `EXISTE-SATISFACE` contra portal. Verificado: fila `CSES_Modulo5_2016_2021` → `EXISTE-SATISFACE` (2026-08-12); fila `GESIS_ISSP` → `EXISTE-SATISFACE` (2026-08-13, 3/3 módulos, México verificado en el dato real para 2 de 3). La fila bare `ISSP` que sí aparece `NO-ENCONTRADO` es un artefacto de MAP-B (búsqueda por nombre exacto contra tablas internas, no encontró la puerta porque quedó registrada bajo el nombre `GESIS_ISSP`) — no reabre el caso.
- **EARLY_CHILDHOOD·4, GPS·6** — carril del usuario. Verificado: filas `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661` y `GPS_Global_Preferences_Survey` → ambas `EXISTE-NO-SATISFACE`, ambas con registro/formulario ya ejecutado por el agente o usuario, microdato nuclear pendiente de un acto de descarga (no de sondeo).
- **BRASDEFER·2, MOBILE_TUTORS·5** — `NEGATIVA` sellada en la cola (`CURADURIA_SEMANTICA_MULTI2` / `APERTURA_NEGATIVA_EXPLICITA`), reapertura es decisión de mesa (`plan-descargas-completo` §8). No se toca.
- **MEXICO_PANEL_STUDY·18** — fila `ICPSR_Mexico_Panel_Study_2012` → `NO-ACCESIBLE` ya sondeada (2026-08-08): "exige Restricted Data Use Agreement, no es solo registro gratuito". Cerrada, no se re-sondea.

22 − 7 = **15**. El conjunto resultante es idéntico, palanca por palanca, al que el encargo propone — sin diferencia que reportar.

## 3 · Las 15 fuentes, congeladas verbatim (antes de tocar red)

| pal | fuente | nec | FIN | URL de la cola |
|---|---|---|---|---|
| 9 | WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023 | 3 | NO | https://microdata.worldbank.org/catalog/6453 |
| 11 | GDELT | 2 | SI | https://www.gdeltproject.org/data.html |
| 12 | INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO | 2 | SI | https://www.nature.com/articles/s41562-024-02043-y |
| 14 | MASS_MOBILIZATION_PROTEST_DATA | 2 | SI | https://massmobilization.github.io/ |
| 16 | UCDP | 2 | SI | https://ucdp.uu.se/downloads/ |
| 17 | ENCOAP | 2 | NO | https://www.inegi.org.mx/programas/encoap/2023/default.html |
| 23 | LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2 | 1 | SI | https://microdata.worldbank.org/catalog/2049 |
| 25 | MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP | 1 | SI | https://www.openicpsr.org/openicpsr/project/116334/version/V1/view |
| 28 | CNGMD | 1 | NO | https://www.inegi.org.mx/rnm/index.php/catalog/977 |
| 30 | DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE | 1 | NO | https://www.povertyactionlab.org/evaluation/information-dissemination-campaign-and-voters-behavior-2009-municipal-elections-mexico |
| 31 | ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION | 1 | NO | https://www.nature.com/articles/s41597-025-04999-0 |
| 33 | ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION | 1 | NO | https://www.banxico.org.mx/publicaciones-y-prensa/encuesta-de-competencias-financieras-de-la-poblaci/microdatos/competencias-financieras-mi.html |
| 35 | IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM | 1 | NO | https://microdata.worldbank.org/catalog/1039/study-description |
| 36 | OECD | 1 | NO | https://www.oecd.org/en/data/datasets/oecd-trust-survey-data.html |
| 38 | PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND | 1 | NO | https://cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/ |

**Nota de allowlist de red de la caja, verificada contra la config del sandbox de esta sesión (no adivinada):** de los 9 dominios distintos en esta tabla, 2 están en el allowlist directo (`www.inegi.org.mx` → palancas 17/28; `www.banxico.org.mx` → palanca 33). Los otros 7 (`microdata.worldbank.org`, `gdeltproject.org`, `nature.com`, `massmobilization.github.io`, `ucdp.uu.se`, `openicpsr.org`, `povertyactionlab.org`, `oecd.org`, `cenfri.org` — 9 dominios en 7 grupos) van a requerir el mismo override de sandbox que `cses.org`/`gps.econ.uni-bonn.de` necesitaron en ACTO P·Lote-1 (§5.5 de esa nota): eso mide un límite de la caja, no del portal — se declara por fuente, igual que ahí, con el 403/timeout sin override como primer dato y el resultado con override como el que se reporta (A.5: "el primer resultado que produzca este procedimiento").

## 4 · Criterio de clase A.4, por fuente — escrito antes de sondear

Este acto no descarga, así que su vocabulario es más estrecho que el de P·Lote-k:

- **EXISTE-SATISFACE** — la puerta responde, y la portada declara microdato de México accesible con registro gratuito o menos. No afirma que el payload se bajó — eso es de un acto de descarga (P·Lote-k).
- **EXISTE-NO-SATISFACE** — responde, y falta algo específico: no hay México, no hay microdato, la cobertura temporal no sirve. Se dice qué falta.
- **NO-ACCESIBLE** — pago, afiliación institucional o licencia restringida. Registro gratuito o aceptar términos de uso NO cuenta aquí.
- **NO OBTENIDO POR ESTE AGENTE EN N INTENTOS** — la sonda falló. No es NO-ENCONTRADO. Van los N intentos con salida cruda + receta manual ejecutable en navegador en <1 min (A.5).
- **NO-ENCONTRADO** — solo si la puerta responde y el recurso no está ahí, con los términos y el universo en la misma línea.

Prohibido concluir cualquier cosa de un portal desde conocimiento de entrenamiento. El corte es anterior a hoy. Si no se sondeó en esta sesión, no se sabe.

Regla A.6 (no violable): una candidata localizada por buscador y no abierta byte a byte se registra SIN-FETCH, jamás se promueve.

Contra-regla B-bis, escrita antes de ver el dato: este acto puede terminar sin una sola puerta nueva utilizable, y eso sería un resultado, no un fracaso. Si las 15 vuelven NO OBTENIDO POR ESTE AGENTE, el entregable son 15 recetas manuales — el carril usuario+`descargas_mx` ya cerró tres veces (ISSP, WVS, y parcialmente Banco Mundial/GPS vía registro) lo que el agente declaró imposible. La receta es el entregable de mayor rendimiento, no su consuelo.

El primer resultado que produzca este procedimiento es el que se reporta.

---

## 5 · Commit 2 — la ejecución

Por fuente, en el orden del encargo: `curl` (nunca `curl -I`) → si falla, reintento con cabeceras de navegador real, declarando si el 403 cambia → apertura byte a byte de lo que responda → clasificación A.4 en la misma línea que su universo + mecanismo + fecha. WebFetch no se probó de nuevo contra estas 15 — el barrido de las 17 condiciones ya lo reportó 403 en el 100% de los intentos contra un dominio de control neutral (dato heredado, citado, no re-medido); se usó `curl` desde el primer intento.

### 5.1 · Las 9 EXISTE-SATISFACE

**INEGI_ENCOAP_2023 (palanca 17).** La portada JSON-LD trae un `contentUrl` señuelo (`.../prueba.pdf`) — el mismo patrón de soft-404/placeholder que este repo ya documentó para ENVIPE 2024. No se le creyó. Se aplicó el mecanismo B ya probado en 5+ programas INEGI (API `archivoscompaginacion`, sin adivinar nombre de archivo): `idBiinegi=3369` → `pathLogico=/programas/encoap/2023/microdatos/bd_encoap2023` → verificado con `GET -r 0-0`: **206 Partial Content, 420 306 bytes reales**, no el soft-404 fijo de 2263 bytes. Libre, sin registro.

**RNM_CNGMD_2023_catalogo977 (palanca 28).** La ficha RNM declara textualmente "Uso público... a través de un sitio de descarga directa". Verificado en el sitio real (`programas/cngmd/2023/`, tab "Datos abiertos", `tipoinformacion=12` — no 4, distinto de ENCOAP): **87 archivos reales**, uno verificado (`GET -r 0-0`: 206, 2 835 380 bytes).

**Banxico_EncuestaCompetenciasFinancieras (palanca 33).** 6 enlaces `.xlsx` directos (2019-2024) en la propia portada, sin formulario. Verificado 2024: **206, 1 210 013 bytes**.

**JPAL_CorruptionInformation_MexicoVoters_2009 (palanca 30).** Enlace "Download data (545 KB)" directo en la página J-PAL, sin registro. Verificado (siguiendo redirects http→https→CDN): **206, 184 801 bytes**.

**Zenodo_ElectoralPrecinctLevel_MexicoMunicipal (palanca 31) — con hallazgo de calidad de la cola.** La URL congelada en el Commit 1 (`.../s41597-025-04999-0`, verbatim de `data/cola-adquisicion-2026-08-12.tsv`) da **404 real de Nature** (confirmado con cookie-jar para descartar bucle de consentimiento, no un bloqueo de caja). Buscado el título exacto en el buscador propio de `nature.com` (A.6: candidata de buscador, promovida solo tras abrir byte a byte) → DOI real `s41597-025-04918-9`. Página real: título coincide exacto con el `fuente_canonica` de la cola. Su sección "Data Records" declara Zenodo + GitHub; verificado vía API de Zenodo: **1 archivo, 739 952 144 bytes, `access_right=open`**, confirmado también con `GET -r 0-0` directo. **La cola tiene un DOI mal transcrito para esta fuente — reportado a mesa, no editado (fuera de perímetro de este acto).**

**OSF_InteractingAsEquals_PartisanPolarizacion_Mexico (palanca 12).** El artículo declara en "Data availability": datos y código en `osf.io/f7bzy/`, con una limitación explícita del propio paper (texto crudo de chats no disponible por protección de sujetos humanos, pero las medidas derivadas sí). OSF es SPA sin contenido en HTML crudo — sondeado con su API pública (`api.osf.io/v2/`): nodo `public: true`, carpeta `Data/` con **10 archivos reales** (incl. `Master_Data.dta`, datos municipales y de pobreza 2020), sin autenticación. Solo listado de metadatos, ningún archivo abierto a nivel de contenido.

**WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453 (palanca 9) — mecanismo distinto a los otros 2 catálogos WB de este lote.** Su tab "Get Microdata" NO usa el login NADA de `microdata.worldbank.org` (a diferencia de 2049/1039/2661) — declara "Data available from external repository" y remite a `enterprisesurveys.org` → botón "Access microdata" → `login.enterprisesurveys.org` → formulario de registro (nombre/correo/contraseña/"primary institution affiliation" como **campo de texto libre**, país, resumen de 1 párrafo del proyecto, aceptar "Data Access Protocol") — sin cargo, sin verificación de afiliación real. Registro gratuito, no ejecutado (este acto no descarga).

**WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049 (palanca 23) y WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039 (palanca 35).** Mismo patrón NADA que catálogo 2661 ya documentado en P·Lote-1 (`"Login to access data..."`). **La cuenta de este proyecto (`jonieqsa@gmail.com`, creada en P·Lote-1, activada 2026-08-13 según la fila `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661`) sirve para estos 2 catálogos también — no hace falta registrar de nuevo.**

### 5.2 · Las 2 EXISTE-NO-SATISFACE

**GDELT_RawDataFiles (palanca 11) y UCDP_Downloads_GED (palanca 16).** Ambas 100 % libres, sin registro, verificadas con contenido real (UCDP: `GET -r 0-0` da 206, 39 122 522 bytes). Ambas con **cero menciones de "mexico"/"méxico" en el HTML crudo de la portada** — son bases globales (eventos noticiosos geolocalizados / conflicto armado, todos los países) sin recorte de país en el mecanismo de descarga documentado. Para GDELT esto no es un hallazgo nuevo: la propia cola ya lo declaraba antes de sondear ("debe construirse universo México, deduplicar noticias, clasificar agravio/respuesta"). Ninguna de las dos es NO-ACCESIBLE (cero barrera) ni NO-ENCONTRADO (el recurso responde y existe) — lo que falta es la declaración/recorte de México, no el acceso.

### 5.3 · Las 4 NO OBTENIDO POR ESTE AGENTE

**MassMobilization_Dataverse_MMdata (palanca 14) — EN 4 INTENTOS.** La portada (`massmobilization.github.io`) es 100 % libre y responde 200. El repositorio real (`dataverse.harvard.edu/dataverse/MMdata`) da **HTTP 202 con cabecera `x-amzn-waf-action: challenge`** en las 4 rutas probadas (página directa, API REST `/api/dataverses/MMdata/contents`, dominio raíz, reintento con cabeceras de navegador real Chrome/Windows — 202 idéntico, sin cambio). Es un reto anti-bot **AWS WAF** a nivel de dominio — mismo patrón funcional que el Cloudflare de GESIS/ISSP (P·Lote-1 §5.1), proveedor distinto.

**openICPSR_Microcredit_MexicoPlacement_proj116334 (palanca 25), OECD_TrustSurveyData (palanca 36) y Cenfri_MicroinsuranceMexico (palanca 38) — EN 2 INTENTOS cada una.** Las 3 dan la **firma Cloudflare idéntica a GESIS/ISSP** (`server: cloudflare`, `cf-mitigated: challenge`, CSP referenciando `challenges.cloudflare.com`, título `"Just a moment..."`), sin cambio con cabeceras de navegador real. openICPSR (a diferencia de ICPSR clásico, que exige *Restricted Data Use Agreement* — ver `ICPSR_Mexico_Panel_Study_2012`, `NO-ACCESIBLE`) suele permitir registro gratuito, pero el bloqueo ocurrió antes de ver ese formulario — no se puede confirmar ni descartar.

Ninguna de las 4 es NO-ACCESIBLE: en ningún caso se confirmó pago o afiliación institucional — el bloqueo ocurrió antes de ver contenido alguno. Las 4 recetas manuales (<1 min cada una, abrir en navegador real — el reto se resuelve solo, como en ISSP/WVS) quedan en las filas nuevas del puntero (§6).

## 6 · Filas nuevas escritas en `data/universo-puertas-2026-08-12.tsv`

Verificado sin drift antes de escribir: `git fetch origin main` + `git merge-base --is-ancestor origin/main HEAD` → confirmado, nadie más empujó desde que este acto abrió el worktree. **15 filas añadidas por `append` puro (Python, escritura de texto plano tabulado — nunca `csv.writer`, defecto ya documentado en este proyecto para estos TSV), 0 filas ajenas tocadas** — verificado con `git diff --stat` (15 insertions, 0 deletions) y con conteo de columnas (`awk -F'\t' '{print NF}' | sort -u` → `15` único valor, las 114 filas). El puntero pasa de 99 a 114 filas de datos.

**Hallazgo de perímetro, declarado y no resuelto por este acto.** Las 15 fuentes de este lote ya tenían una fila `gap_mapeo_map_b` / `NO-ENCONTRADO` propia (las mismas 62 de la premisa) — verificado por comando, las 15 coinciden por nombre exacto. El perímetro de este acto es estrictamente aditivo ("SOLO filas nuevas, jamás editar filas ajenas"), así que esas 15 filas viejas **quedan tal cual**, ahora stale (dicen NO-ENCONTRADO contra las tablas internas, mientras la fila nueva de al lado dice EXISTE-SATISFACE/EXISTE-NO-SATISFACE/NO OBTENIDO contra el portal real). Retirarlas es trabajo de un acto tipo MAP-B (que sí tiene ese mecanismo y ese perímetro, ver `forense/notas/2026-08-13-map-b-crosswalk.md`), no de este. Mismo razonamiento aplica a `data/crosswalk-fuente-puerta-2026-08-13.tsv` (75 filas, fuera de este perímetro): el contador que el encargo cita ("12 de 75 con A.4 derivada de portal") no se actualizó en ESE archivo por este acto — la evidencia que lo movería ya vive en las 15 filas nuevas de `universo-puertas`, lista para que el acto de reconciliación la levante.

## 7 · PRISMA — embudo de las 15 fuentes de este lote

| intentadas | respondieron (200, contenido real) | con-México-declarado | con-microdato-declarado | no-accesibles | no-obtenidas | con-receta-manual |
|---|---|---|---|---|---|---|
| 15 | 11 | 9 | 9 | 0 | 4 | 4 |

Lectura: de 15 intentadas, 11 dieron contenido real (las otras 4 se quedaron en el reto anti-bot antes de mostrar nada). De esas 11, 9 declaran México explícitamente (título o contenido) — las mismas 9 que declaran microdato real accesible: no hubo ningún caso de "México sí, microdato no" en este lote (a diferencia de lo que sí ocurrió con GESIS/ZA7600 en P·Lote-1). Las otras 2 de las 11 (GDELT, UCDP) son bases globales sin declarar México — ni accedidas-sin-satisfacer por falta de dato, sino por falta de recorte/declaración. Cero NO-ACCESIBLE: en este lote nunca se llegó a confirmar pago o afiliación institucional como condición — todas las barreras encontradas fueron técnicas (Cloudflare/AWS WAF) antes de ver siquiera un formulario.

## 8 · Propuesta de firma del Lote 2 — ordenada por lo que el sondeo encontró

La firma del PLAN v1 (`GDELT·11 · ENCOAP·17 · WB_ENTERPRISE·9`) resulta, medida: 1 fuente que no satisface (GDELT, base global sin México), 1 fuente limpia (ENCOAP) y 1 fuente con registro nuevo pendiente (WB_ENTERPRISE). Un acierto de tres, con dos sondas gastadas en encontrarlo. Con el mapa completo, la reordenación por evidencia:

**Lote 2 propuesto — agente-ejecutable de punta a punta, cero fricción (6 fuentes, listas para un P·Lote-k hoy mismo):** `ENCOAP·17` · `CNGMD·28` · `Banxico_EncuestaCompetenciasFinancieras·33` · `JPAL_CorruptionInformation·30` · `Zenodo_ElectoralPrecinctLevel·31` · `OSF_InteractingAsEquals·12`. Las 6 ya están verificadas con `GET -r 0-0`/API real, sin registro, sin espera de correo — sirven N2,N3,N17,N25,N28,N29,N30 (7 necesidades). Costo de la caja: ~0 adicional, ya sondeado en este mismo acto.

**Carril usuario+navegador (no agente) — registro ya iniciado o requerido, mismo patrón que cerró ISSP/WVS tres veces:** `WorldBank_MEX_LargeScaleFinancialEducation·23` y `WorldBank_MEX_ParentalEmpowerment·35` (cuenta NADA ya activa, solo falta iniciar sesión y clic — cero registro nuevo) · `WORLD_BANK_ENTERPRISE_SURVEY·9` (cuenta nueva en `enterprisesurveys.org`, gratuita, sin pago) · `MASS_MOBILIZATION·14` / `openICPSR_Microcredit·25` / `OECD_TrustSurvey·36` / `Cenfri_Microinsurance·38` (reto anti-bot que un navegador real resuelve solo — recetas en §6).

**Requiere decisión de mesa antes de cualquier acto de descarga — no es un Lote de descarga, es una decisión de ingeniería:** `GDELT·11` y `UCDP·16`. Ambas 100 % libres pero globales (GDELT: >2.5 TB/año; UCDP: decenas de archivos) — bajarlas completas sin definir primero el mecanismo de recorte/construcción de universo México sería gastar la caja en peso muerto, exactamente el riesgo que este acto fue encargado a prevenir. Palancas 12 y 16 que el encargo señalaba como saltadas por el PLAN v1: la 12 (Nature/OSF) ya quedó resuelta arriba (Lote 2 limpio); la 16 (UCDP) es la que de verdad necesita esta decisión antes de tocarla.

El primer resultado que produjo este acto es el que se reporta.

