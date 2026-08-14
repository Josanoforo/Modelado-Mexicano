# ACTO SANEA-MAPEO · H1 (crosswalk stale) + H10 (sondeo-27 sin consumir)

**Encargo:** `ENCARGO SANEA-MAPEO`, §4.B del documento de dirección "AUDITORÍA A-Z DEL PROGRAMA + INFRAESTRUCTURA DEL SIMULADOR + PLAN MULTIFASE" (14/ago/2026, subido a la sesión, no versionado en este repo) · **Entorno:** nube, repo-only, cero red, sin baja de dato · **Base:** `origin/main = 84b2acf` (post-#228, verificado `git rev-parse HEAD`/`origin/main` idénticos al arrancar) · **Rama:** `claude/sanea-mapeo-encargo-lw5hhr`.

## 0 · ARRANQUE

1. **REPO.** Clon en uso, sin worktree adicional (rama dedicada ya asignada). `git status` limpio al arrancar.
2. **SHA.** `84b2acfb0616a1c26b8a2d57dd0a798d11d1fbf5`, idéntico a `origin/main`. Cadena ADR (`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md`) contigua 1..80 — este acto no sella ninguno, no hay decisión de mesa que registrar aquí.
3. **data/raw.** Ausente — no aplica, este acto no descarga nada (perímetro del encargo).
4. **ENTORNO.** `echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]"` → `[cloud_default]`, firma de nube, consistente con la tabla de lanzamiento del plan (sesión 5, "nube").
5. **Espejo.** No se usó ninguno — toda cifra de esta nota sale de comandos corridos en este árbol, a la vista abajo.

**Premisas re-derivadas, no heredadas (regla del encargo: "no heredar 27/17").**

```
$ awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l                 -> 122   (no 104: el plan cita ~104 de forma aproximada; 8 filas se sumaron entre la redacción del plan y hoy)
$ awk -F'\t' 'NR>1 && $2!="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l  -> 61 reales
$ awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l  -> 61 gap
$ awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)if($i=="estado_triaje")c=i} $c=="CANDIDATA-A-SONDEO"' data/acceso-puertas-2026-08-13.tsv | wc -l  -> 27  (no "17", regla ADR-80(a): SONDEO-COMPLETO cubrió las 27)
$ awk -F'\t' 'NR>1{print $3}' data/curacion-registro/relaciones.tsv | sort -u | wc -l  -> 75  (universo de fuentes, sin cambio desde MAP-B)
```

Ningún archivo de `relaciones.tsv` se toca en este acto (perímetro explícito del encargo — es de `ENLACE-2`). Ningún byte se descarga.

---

## 1 · Commit 1 — método congelado, declarado antes de tocar ninguna fila

### 1.1 · (a) Re-derivación del crosswalk contra el puntero VIGENTE

**El puntero vigente es `data/universo-puertas-2026-08-12.tsv`** (único archivo `universo-puertas-*` con fecha más reciente; no existe versión 08-13 ni 08-14 previa a este acto). Método: exactamente la jerarquía de evidencia de `forense/notas/2026-08-13-map-b-crosswalk.md §1`, citada verbatim, no reinventada:

1. **URL** — `cola-adquisicion.url_conocida` coincide (normalizado por host+path, ignorando `www.`/protocolo) con `universo-puertas.url`.
2. **Necesidad** — `universo-puertas.necesidad_que_sirve` nombra el mismo `necesidad_id` que alguna relación de esa fuente, **reforzado por** identidad de nombre/institución — necesidad compartida sola no basta (mismo criterio que rechazó `IMSS` en MAP-B).
3. **Cita explícita** de otro archivo del repo.

**Extensión declarada de este acto, no del método original:** para el criterio 1 (URL), además de `cola-adquisicion.url_conocida` se admite la `url` que el propio sondeo-27 (`data/acceso-puertas-2026-08-13.tsv`, columna `url`) haya encontrado para una `CANDIDATA-A-SONDEO` cuyo `url_conocida` en la cola estaba `VACIO` — es la misma regla de evidencia (URL exacta, no parecido de cadena), solo con una segunda fuente de URLs que MAP-B no tenía disponible el 13/ago temprano (el sondeo-27 corrió después, `PR #228`). Dos filas se benefician de esta extensión (§2.2).

**Ambigüedad y rechazo explícito:** mismas reglas que MAP-B — `EQUIVALENCIA-AMBIGUA` cuando ≥2 puertas son candidatas plausibles sin evidencia que prefiera una; rechazo declarado (no silencioso) cuando solo hay traslape de institución/tema sin URL ni cita que confirme mismo producto.

**Re-verificación completa, no parche puntual.** Se recorrieron las 75 fuentes (no solo las citadas por el plan como H1) contra el puntero vigente completo — exacto por nombre, por URL (cola + sondeo-27), y necesidad+institución para las que quedan — y se comparó cada resultado contra `data/crosswalk-fuente-puerta-2026-08-13.tsv` para detectar tanto filas que ganan puerta como filas cuya `clasificacion_a4_de_la_puerta` copiada quedó `stale` sin cambiar de puerta (columna es copia, no re-derivación — cualquier cambio en la puerta real debe propagarse).

### 1.2 · (b) Consumo del sondeo-27 (`#228`) hacia su fila de puerta

Cada una de las 27 filas `CANDIDATA-A-SONDEO` de `data/acceso-puertas-2026-08-13.tsv` corresponde, por nombre idéntico, a una fila `gap_mapeo_map_b` en `data/universo-puertas-2026-08-12.tsv` (verificado 27/27, ningún nombre huérfano). Regla de consumo, declarada antes de aplicarla:

- **`quien_puede = AGENTE` o `USUARIO_REGISTRO` (portal real confirmado, sin bloqueo o con registro gratuito accesible)** → `clasificacion_a4 = EXISTE-NO-VERIFICADO` **(valor nuevo de este acto, justificado abajo)**, con `universo_declarado` citando el sondeo (código HTTP, URL, fecha). **Excepción declarada:** si el propio sondeo cita una fuente previa que ya declaró el dato — no el portal — como propietario/restringido (`HOMESCAN_CONSUMER_PANEL_SERVICES`, `PANEL_DE_COMPRA_DE_HOGARES`, `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES`, `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY`), la clasificación es `NO-ACCESIBLE` — la pregunta relevante es la del dato, no la del portal.
- **`quien_puede = NADIE`, con `http_sin_override` y `http_con_override` idénticos (2 intentos reales, mismo resultado)** → `clasificacion_a4 = NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS` — reutiliza el valor ya en uso 5 veces en el propio puntero (`Mejoredu_INEE_Bases_Datos`, `CIDE_Panel_Mexico_2006`, etc.), mismo significado exacto (N intentos reales de este agente, todos fallidos, causa declarada).
- **`quien_puede = NO_PROBADO` (sin URL identificable)** → `clasificacion_a4` se queda `NO-ENCONTRADO` (sin cambio de valor), pero `universo_declarado` se amplía citando que TRIAGE-63/#228 también buscó y no encontró — segunda búsqueda independiente que refuerza el negativo bajo A.4, no lo cambia.

**Por qué `EXISTE-NO-VERIFICADO` y no `EXISTE-SATISFACE`.** El propio acto que produjo el sondeo lo declaró en su cierre, verbatim: *"este acto sondea reachability de portal, no adjudica `EXISTE-SATISFACE`/`NO-ACCESIBLE` de la necesidad ni toca `estado_triaje`"* (`forense/notas/2026-08-13-triage-63-commit2-sondeo.md §6`). `EXISTE-SATISFACE`/`EXISTE-NO-SATISFACE` en este puntero, en cada caso ya poblado (`ENSAFI`, `ENFIH`, `WVS`, `GESIS_ISSP`…), se ganaron verificando piezas del universo mínimo (criterio `ADR-69`) o abriendo el dato real — nunca solo por un `GET` de reachability. Adjudicar `EXISTE-SATISFACE` a partir de un sondeo que su propio autor declaró fuera de ese alcance sería inventar una clasificación que el sondeo no sostiene — el mismo defecto que `A.4` existe para prevenir, aplicado en sentido inverso (afirmar de más, no de menos). Ningún valor existente en el puntero (`NO-ENCONTRADO`, `EXISTE-SATISFACE`, `EXISTE-NO-SATISFACE`, `NO-ACCESIBLE`, `SIN-FETCH`, `NO OBTENIDO EN N INTENTOS`) describe honestamente "portal confirmado real, contenido no evaluado contra universo mínimo" — mismo patrón que `MAP-B` siguió al declarar `gap_mapeo_map_b` en `clase_origen` cuando ninguno de los 6 valores en uso encajaba: se declara un valor nuevo, justificado aquí, en vez de forzar uno existente.

**Casos excluidos del consumo directo, declarados uno a uno (no silenciosos):**

- **`MICROCREDIT_IMPACTS_COMPARTAMOS_RCT`** — su fila ya trae `clasificacion_a4 = EXISTE-SATISFACE` con URL propia (de un acto anterior a este, no identificado por nombre en las notas revisadas). El sondeo de hoy dio `403`/`USUARIO_REGISTRO` — no se retrocede: un `403` anónimo no contradice un payload ya adquirido por otra vía (mismo patrón que `WVS`/`GESIS_ISSP`/`GPS` en notas previas, donde el bloqueo era del sondeo anónimo, no del acceso real ya logrado). Revisado, sin cambio, razón declarada.
- **`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`** y **`MASS_MOBILIZATION_PROTEST_DATA_MEXICO`** — su propia URL de sondeo (`massmobilization.github.io/`) es idéntica a la de la puerta real `MassMobilization_Dataverse_MMdata`, ya fusionada en el crosswalk (§1.1/§2.2). No se les asigna una clasificación independiente en su propia fila `gap_mapeo_map_b` — hacerlo crearía una instancia nueva del mismo defecto de filas contradictorias (misma fuente, dos clasificaciones) que `PROPUESTA-reconciliacion-universo-puertas.md`/`ADR-74(candidato)` ya documentó y dejó pendiente de sello de mesa. Se declara la fusión, no se ejecuta la retirada de fila que ese ADR candidato propondría (fuera de perímetro de este encargo, que no autoriza tocar la mecánica de precedencia del puntero).

### 1.3 · Adquisiciones habilitadas → PROPUESTA a la cola

De las 24 filas consumidas, **15 tienen `clasificacion_a4 = EXISTE-NO-VERIFICADO`** (portal real, dato no conocido de antemano como bloqueado) — el subconjunto donde el veredicto **habilita** adquisición, no solo alcanzabilidad de portal. Las 4 `NO-ACCESIBLE` (dato ya declarado bloqueado por fuente previa), las 3 `NO OBTENIDO EN 2 INTENTOS` y las 2 `NO-ENCONTRADO` quedan fuera — su propio veredicto declara que la adquisición no está habilitada hoy. Estas 15 se proponen a `data/cola-adquisicion-2026-08-12.tsv` en `PROPUESTA-cola-sondeo27-2026-08-14.md` — **como propuesta, no como fila escrita**: la palanca (prioridad) y la firma de lote son decisión de mesa, este acto no las adjudica (mismo principio que `PROPUESTA-reconciliacion-universo-puertas.md` ya siguió: producir el artefacto listo para sellar, no sellarlo).

---

## 2 · Commit 2 — los dos TSV con fecha propia + el embudo

**Regla del puntero (snapshot superset):** se publican `data/crosswalk-fuente-puerta-2026-08-14.tsv` y `data/universo-puertas-2026-08-14.tsv` como snapshots nuevos, fechados hoy — el archivo del 08-12/08-13 **no se borra ni se sobrescribe**, queda como historia. `data/universo-puertas-2026-08-14.tsv` es superset: las 122 filas del 08-12 completas, con las 24 filas de §1.2 actualizadas en `clasificacion_a4`/`universo_declarado`/`fecha_sondeo`/`url` — ninguna fila retirada, ninguna añadida (el retiro de duplicados es competencia de `ADR-74(candidato)`, no de este acto).

### 2.1 · El embudo del crosswalk, contado

```
$ awk -F'\t' 'NR>1{print $NF}' data/crosswalk-fuente-puerta-2026-08-14.tsv | sort | uniq -c
     31 CON-PUERTA-CLASIFICADA
      1 EQUIVALENCIA-AMBIGUA
     43 SIN-PUERTA
```

**12 → 31 `CON-PUERTA-CLASIFICADA`** (de 75 fuentes), **1 `EQUIVALENCIA-AMBIGUA`** (sin cambio — `REPOSITORIOS_UNAM_COLMEX_ITAM_DATAVERSE_ICPSR`, ninguna evidencia nueva prefiere una de las 5 candidatas), **62 → 43 `SIN-PUERTA`**. El plan citaba "7/1/67" como snapshot de H1 — cifra ya vieja incluso contra el estado del 13/ago (que era 12/1/62, tras la reconciliación de `forense/notas/2026-08-13-map-b-crosswalk.md §3`); ninguna de las dos se hereda aquí, ambas quedan re-derivadas.

**19 fuentes ganan puerta en este acto** (12 preexistentes de MAP-B no se tocan salvo su `clasificacion_a4_de_la_puerta`, ver abajo):

| fuente_canonica | puerta | evidencia |
|---|---|---|
| `LAPOP` | `LAPOP` | nombre idéntico — la puerta real reemplazó su propio placeholder `gap_mapeo_map_b` vía `REG-LOTE3` (13/ago), MAP-B no lo vio |
| `CNGMD` | `RNM_CNGMD_2023_catalogo977` | URL exacta (cola vs puertas) |
| `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` | `JPAL_CorruptionInformation_MexicoVoters_2009` | URL exacta |
| `ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION` | `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal` | URL exacta |
| `ENCOAP` | `INEGI_ENCOAP_2023` | URL exacta |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION` | `Banxico_EncuestaCompetenciasFinancieras` | URL exacta |
| `GDELT` | `GDELT_RawDataFiles` | URL exacta |
| `IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM` | `WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039` | URL exacta |
| `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` | `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico` | URL exacta |
| `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` | `WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049` | URL exacta |
| `MASS_MOBILIZATION_PROTEST_DATA` | `MassMobilization_Dataverse_MMdata` | URL exacta (vía cola) |
| `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` | `MassMobilization_Dataverse_MMdata` | URL exacta (vía sondeo-27, §1.1 extensión) |
| `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` | `MassMobilization_Dataverse_MMdata` | URL exacta (vía sondeo-27, §1.1 extensión) |
| `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` | `openICPSR_Microcredit_MexicoPlacement_proj116334` | URL exacta |
| `OECD` | `OECD_TrustSurveyData` | URL exacta |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `Cenfri_MicroinsuranceMexico` | URL exacta |
| `UCDP` | `UCDP_Downloads_GED` | URL exacta |
| `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` | `WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453` | URL exacta |
| `ISSP` | `GESIS_ISSP` | nombre "ISSP" citado literal dentro de `puertas.institucion`, más necesidad idéntica en ambos lados (`N2,N3,N12,N13,N14,N28,N30`) — MAP-B comparó `puerta=="ISSP"`, no `puerta=="GESIS_ISSP"`; ya nombrado sin corregir en `PROPUESTA-reconciliacion-universo-puertas.md §3(g)` |

**3 fuentes ya `CON-PUERTA-CLASIFICADA` tenían `clasificacion_a4_de_la_puerta` `stale`, corregida en este acto (columna es copia, no re-derivación — sin tocar la puerta real):**

| fuente | puerta | antes | ahora | causa |
|---|---|---|---|---|
| `WVS` | `WVS_World_Values_Survey` | `NO-ENCONTRADO` | `EXISTE-SATISFACE` | ya declarado stale en `forense/notas/2026-08-13-map-b-crosswalk.md §3`, no corregido hasta hoy |
| `GPS` | `GPS_Global_Preferences_Survey` | `EXISTE-NO-SATISFACE` | `EXISTE-SATISFACE` | la puerta real avanzó (`REG-LOTE3`, 13/ago) después de que MAP-B copiara el valor |
| `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` | `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661` | `EXISTE-NO-SATISFACE` | `EXISTE-SATISFACE` | ídem |

**Rechazos explícitos re-verificados, sin cambio (institución/tema comparten con un candidato real pero sin URL/cita que confirme mismo producto — mismo criterio que descartó `IMSS` en MAP-B):** `AHORRO FINANCIERO Y FINANCIAMI`, `BDIF`, `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH`, `ENAFIN`, `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY`, `FINANZAS` (candidatos CNBV/BID, ninguno confirmado — `pnif.cnbv.gob.mx` ≠ `CNBV_Portafolio_Informacion`), `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` (catálogo World Bank `870`, distinto de `6453`), `SE`, `IMSS` (sin cambio, mismo rechazo de siempre) — declarados fila por fila en `evidencia_de_equivalencia` del TSV, no omitidos.

### 2.2 · El embudo del consumo del sondeo-27, contado

```
$ awk -F'\t' 'NR>1 && $15=="2026-08-14"' data/universo-puertas-2026-08-14.tsv | wc -l
24
```

24 de 27 filas `CANDIDATA-A-SONDEO` consumidas hacia su fila de puerta (clasificación A.4 + universo, `fecha_sondeo` re-fechada a hoy); 3 excluidas y declaradas (§1.2): 1 ya resuelta por evidencia más fuerte, 2 fusionadas dentro del crosswalk hacia una puerta real ya existente, sin editar su propia fila para no duplicar.

```
$ awk -F'\t' 'NR>1 && $15=="2026-08-14"{print $13}' data/universo-puertas-2026-08-14.tsv | sort | uniq -c
     15 EXISTE-NO-VERIFICADO
      4 NO-ACCESIBLE
      3 NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS
      2 NO-ENCONTRADO
```

**15 filas propuestas a la cola de adquisición** (§1.3, detalle en `PROPUESTA-cola-sondeo27-2026-08-14.md`).

### 2.3 · Cierre

```
$ python3 tests/check.py --baseline
```
Ver resultado real en el commit de cierre. Este acto no toca `tests/`, no toca `relaciones.tsv`, no toca `data/manifiesto.yaml`, no descarga ningún byte. Perímetro tocado: `data/crosswalk-fuente-puerta-2026-08-14.tsv` (nuevo), `data/universo-puertas-2026-08-14.tsv` (nuevo), `PROPUESTA-cola-sondeo27-2026-08-14.md` (nuevo), este archivo, `forense/hallazgos.md`.

**Contadores movidos:** crosswalk `CON-PUERTA-CLASIFICADA` 12 → 31 de 75; `SIN-PUERTA` 62 → 43; sondeo-27 consumido hacia puerta 0 → 24 de 27; filas propuestas a cola 0 → 15. Ningún contador de Hito D, condicionales, coeficientes o probabilidades del motor se mueve — este acto sanea mapeo, no mide México.
