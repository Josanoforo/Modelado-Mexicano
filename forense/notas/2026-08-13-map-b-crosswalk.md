# MAP-B — crosswalk demanda↔puertas

**Acto:** ENCARGOS · MAPEO DE UNIVERSO COMPLETO — MAP-B · **Entorno:** CAJA LOCAL Ubuntu CC, repo-only (cero red, sonda omitida como ACTO O) · **Base:** `origin/main = 11083af` (post-#184, verificado antes de abrir worktree) · **Worktree:** `~/mm-map-b-crosswalk`, rama `map-b/crosswalk-fuente-puerta`.

## §0 · Premisas verificadas

```
awk -F'\t' 'NR>1{print $3}' data/curacion-registro/relaciones.tsv | sort -u | wc -l   -> 75
ls data/universo-puertas-*.tsv | sort | tail -1                                        -> data/universo-puertas-2026-08-12.tsv
ls data/cola-adquisicion-*.tsv | sort | tail -1                                        -> data/cola-adquisicion-2026-08-12.tsv
```
`relaciones.tsv`: 198 líneas (197 relaciones + header). `universo-puertas-2026-08-12.tsv`: 32 líneas (31 puertas + header). `cola-adquisicion-2026-08-12.tsv`: 55 líneas (54 fuentes + header, subconjunto de las 75 — solo la capa `NO_REFERENCIADO` que ACTO O derivó).

**Tres actos pushearon hoy (PR #185, #186, #187) tocando `data/universo-puertas-2026-08-12.tsv` en sus propias ramas — ninguno fusionado a `origin/main` todavía.** Este worktree, cortado limpio de `origin/main`, no ve esas filas. Correcto y esperado: este acto trabaja contra lo que realmente hay en `main`, no reconcilia contra ramas sin fusionar — mesa hace esa reconciliación multi-vía al fusionar.

## §1 · El método de equivalencia, declarado ANTES de cruzar nada

El cruce por nombre exacto entre `fuente_canonica_normalizada` (75 valores) y `puerta` (31 valores) da **0 coincidencias** (`comm -12` sobre ambos conjuntos ordenados-únicos). Dos vocabularios sin tabla de equivalencia. Toda equivalencia que este acto declare se establece por evidencia citada, en esta jerarquía, nunca por parecido de cadena:

1. **URL** — `cola-adquisicion.url_conocida` coincide (mismo recurso, aunque difiera el prefijo de colección/ruta) con `universo-puertas.url`.
2. **Necesidad** — `universo-puertas.necesidad_que_sirve` nombra el mismo `necesidad_id` que alguna relación de esa fuente en `relaciones.tsv`, **reforzado por** identidad de nombre/institución (necesidad compartida SOLA, sin refuerzo de nombre, no basta — varias puertas distintas sirven la misma necesidad sin ser la misma fuente; ver ejemplo real en §2, IMSS).
3. **Cita explícita de otro archivo del repo** (archivo:línea) que declare la relación — incluye los registros de alias ya existentes (`data/curacion-registro/aliases-fuentes.tsv`, `data/inventarios/alias-fuentes.yaml`), consultados como fuente de evidencia, no de fusión: si un alias registry no declara una identidad, este acto NO la inventa (verificado: ninguno de los dos registros de alias contiene una entrada relevante a las equivalencias fuente↔puerta de este acto — cubren duplicados dentro del lado de la demanda, `ENBIARE2021→ENBIARE` etc., un problema distinto).

**Ambigüedad:** si una fuente corresponde plausiblemente a **más de una** puerta sin evidencia que prefiera una sobre las otras, la fila queda `gap = EQUIVALENCIA-AMBIGUA`, columna `puerta` lista TODAS las candidatas separadas por `;`, y `evidencia_de_equivalencia` declara por qué ninguna se prefirió. No se resuelve adivinando — ni tomando la primera, ni la de nombre más largo, ni ninguna heurística de conveniencia.

**Rechazo explícito, no silencioso:** una coincidencia de institución o de tema por sí sola, sin URL ni necesidad ni cita que confirme que es el MISMO producto/dataset, se declara y se descarta — la fila queda `SIN-PUERTA` con la candidata rechazada nombrada en `evidencia_de_equivalencia`, no se omite de la nota. Ver §2 para el caso real (IMSS).

**Columnas de `data/crosswalk-fuente-puerta-2026-08-13.tsv`** (una fila por cada una de las 75 fuentes): `fuente_canonica · puerta (o VACIO) · evidencia_de_equivalencia · clasificacion_a4_de_la_puerta (copiada de la puerta real, no re-derivada) · capa2_agregada · en_cola · gap`.

`capa2_agregada`: 10 de las 75 fuentes tienen `capa2_manifiesto` heterogéneo entre sus propias relaciones (p. ej. `ENBIARE` trae tanto `SI` como `SI_O_REFERENCIADO` en filas distintas de `relaciones.tsv`). Regla de agregación, declarada aquí antes de aplicarla: se reporta el valor de mayor cobertura presente, orden `SI > SI_O_REFERENCIADO > NO_REFERENCIADO` — refleja "esta fuente tiene AL MENOS una relación en esta capa", consistente con cómo ACTO O ya trata `capa2_manifiesto` como filtro de máxima-cobertura, no se inventa un criterio nuevo.

`en_cola`: el valor de `palanca` de `data/cola-adquisicion-2026-08-12.tsv` si la fuente aparece ahí (54 de 75), si no, `NO` — no todas las 75 fuentes están en la cola porque la cola es solo la capa `NO_REFERENCIADO` de ACTO O (105 relaciones → 54 fuentes únicas), las demás 21 ya tienen `capa2 ∈ {SI, SI_O_REFERENCIADO}` y no entraron a esa cola por diseño de ese acto, no por omisión de este.

`gap` para `SIN-PUERTA`: por cada una, se añade una fila nueva al puntero vigente (`data/universo-puertas-2026-08-12.tsv`) con `puerta = <fuente_canonica_normalizada misma>` (identificador trazable, no una institución inventada), `clase_origen = gap_mapeo_map_b` (valor nuevo, deliberado — ninguno de los 6 valores ya en uso en esa columna — `canasta_publica`, `catalogo_metadatos_inegi`, `ong_observatorio`, `organismo_internacional`, `repositorio_academico`, `transparencia` — describe honestamente "no se encontró institución", forzar uno de esos sería una clasificación falsa), `clasificacion_a4 = NO-ENCONTRADO`, `universo_declarado` cita el mecanismo exacto de búsqueda y la fecha. Cero red en ninguna de estas filas — nacen `NO-ENCONTRADO` de mapeo, no de sondeo.

**El primer resultado que produzca este cruce es el que se reporta** — no se re-corre buscando un embudo con menos `SIN-PUERTA`.

## §2 · Commit 2 (resultados) — el embudo, tal como lo produjo el método de §1

**7 `CON-PUERTA-CLASIFICADA` · 1 `EQUIVALENCIA-AMBIGUA` · 67 `SIN-PUERTA`, de 75.** `CON-PUERTA-SIN-CLASIFICAR` = 0 — verificado aparte: las 31 puertas del puntero vigente tienen las 31 con algún valor real en `clasificacion_a4` (ninguna columna vacía), así que ese valor de `gap` no ocurre en este corte, no por defecto del método.

**Los 7 matches confirmados, con el nivel de evidencia real de cada uno (ninguno por parecido de cadena):**

| fuente_canonica | puerta | evidencia |
|---|---|---|
| `WVS` | `WVS_World_Values_Survey` | nombre idéntico |
| `ENASIC` | `RNM_ENASIC_2022_ficha922` | nombre idéntico (ya en producción propia, SELLO-B) |
| `ENBIARE` | `RNM_ENBIARE_2021_ficha730` | nombre idéntico |
| `ENCUCI` | `RNM_ENCUCI_2020_ficha647` | nombre idéntico |
| `MEXICO_PANEL_STUDY_2012` | `ICPSR_Mexico_Panel_Study_2012` | **URL**: mismo `study_id` ICPSR 35024, solo difiere el prefijo de colección (`ICPSR` vs `RCMD`) |
| `PI` | `CNBV_Portafolio_Informacion` | nombre + **necesidad** (N19 en ambos lados, única relación de `PI`) |
| `INE` | `INE_Conteos_Censales_Participacion` | institución + **necesidad parcial** (`INE` sirve N25 y N26; la puerta solo cubre N25 — N26 queda declarado sin puerta, no se fuerza una cobertura que no existe) |

**El caso ambiguo:** `REPOSITORIOS_UNAM_COLMEX_ITAM_DATAVERSE_ICPSR` nombra explícitamente las mismas cinco instituciones que cinco puertas ya clasificadas (`UNAM_Repositorio_Institucional_panel`, `COLMEX_Repositorio_panel`, `ITAM_panel_household_finance`, `Harvard_Dataverse_Mexico_panel`, `ICPSR_Mexico_Panel_Study_2012`) — ninguna evidencia en el repo prefiere una sobre las otras cuatro. Nota aparte, no una contradicción: `ICPSR_Mexico_Panel_Study_2012` es también la puerta CONFIRMADA de `MEXICO_PANEL_STUDY_2012` (fila separada arriba) — la misma puerta puede servir a dos demandas distintas a la vez.

**Un rechazo explícito, declarado en vez de omitido:** `IMSS` (fuente_nombre = "Familia de instrumentos de satisfacción de usuarios") se comparó contra `IMSS_Datos_Abiertos_Asegurados` (microdato administrativo de población asegurada) — mismo institución, producto verificablemente distinto (encuestas de satisfacción vs. registro administrativo de asegurados), sin URL ni cita que los identifique. Queda `SIN-PUERTA`, no `CON-PUERTA-CLASIFICADA` por cercanía de nombre.

**Un valor centinela, no una fuente real:** `SIN_CANDIDATO_IDENTIFICADO` es un valor de `relaciones.tsv` sin `fuente_nombre` — no hay nada que buscarle puerta; `SIN-PUERTA` trivial, declarado para que no se lea como un gap sustantivo.

**Las 67 filas `SIN-PUERTA` restantes** cubren, entre otras familias reconocibles por nombre: eventos de protesta/conflicto (`ACLED`, `GDELT`, `UCDP`, tres variantes de `MASS_MOBILIZATION_*`, dos bases de eventos de protesta/agua), evaluaciones de impacto del Banco Mundial (siete entradas `IMPACT_EVALUATION_*`/`MICROCREDIT_*`/`LARGE_SCALE_FINANCIAL_EDUCATION*`/`PRICE_AND_INFORMATION*`/`EARLY_CHILDHOOD*`), encuestas INEGI sin puerta propia todavía (`ENAFIN`, `ENCIG`, `ENCOAP`, `ENCUP`, `ENIF`, `ENIGH`, `ENNVIH`, `ENOE`, `ENVIPE`, `ENSAFI`, `ENFIH` — estas dos últimas SÍ tienen ficha RNM real, pero esa fila vive en una rama sin fusionar todavía, PR #187, invisible a este corte por diseño), literatura académica de encuestas/experimentos electorales (`CSES` y su duplicado aparente `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018`, `LAPOP`, `LATINOBARÓMETRO`, `OECD`, cuatro entradas electorales/polarización), y un racimo de fuentes financieras/tandas sin puerta institucional dedicada (`BDIF`, `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH`, `REGISTRO_DE_TANDAS_Y_REPUTACION`, `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES`, `SERIES_SPEI_CODI_BANXICO`, entre otras). Ninguna de estas 67 se fuerza a una puerta existente por cercanía temática — el TSV es la lista completa, esta nota no repite las 67 filas.

**Nota sobre duplicados aparentes del lado de la demanda, no resueltos aquí:** `CSES`/`COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018`, `GPS`/`GLOBAL_PREFERENCES_SURVEY`, y las dos entradas de `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_*` parecen nombrar el mismo instrumento real bajo dos identidades de `fuente_canonica` distintas. Fuera de perímetro de este acto (eso es resolución de alias del lado de la demanda, no crosswalk demanda↔puerta) — declarado para quien mantenga `aliases-fuentes.tsv`.

## §3 · Reconciliación post-fusión (#186/#187), en el merge de #189 hacia `main`

Al fusionar `origin/main` en esta rama (previo al botón de #189), conflicto real esperado en `data/universo-puertas-2026-08-12.tsv` (dos inserciones ancladas en la misma línea de contexto, `RNM_ENCUCI_2020_ficha647`) — resuelto **conservando ambos lados** (las 67 filas gap de este acto + las 5 filas reales que aportaron #186/#187 vía #187, merge commit `50f893b9`). Verificado por comando, no por la lista de la sesión que disparó esta reconciliación: `diff` entre `data/universo-puertas-2026-08-12.tsv` en el punto de bifurcación de esta rama y en `origin/main` da exactamente 5 `puerta_id` nuevos — `CSES_Modulo5_2016_2021`, `GPS_Global_Preferences_Survey`, `RNM_ENFIH_2019_ficha709`, `RNM_ENSAFI_2023_ficha992`, `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661` — mismos cinco que §2 ya señalaba como invisibles a este corte "por diseño" (ENSAFI/ENFIH) o como gap ordinario (CSES/GPS/EARLY_CHILDHOOD).

Para cada uno de los cinco, cruzado el `fuente_canonica` del crosswalk cuyo `gap` era `SIN-PUERTA` y cuyo nombre corresponde a la puerta nueva por la misma evidencia de identidad ya usada en este acto (nombre/institución/estudio, nunca parecido de cadena sin corroborar): **retirada su fila gap propia** (`clase_origen=gap_mapeo_map_b`, no sellada, de esta misma rama sin fusionar — no historia forense) de `universo-puertas-2026-08-12.tsv` (`CSES`, `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014`, `ENFIH`, `ENSAFI`, `GPS`; 67→62 filas gap, 99 líneas totales), y **actualizada su fila en el crosswalk** (`puerta` de `VACIO` a la puerta real, `clasificacion_a4_de_la_puerta` copiada de la fila fusionada, `gap` de `SIN-PUERTA` a `CON-PUERTA-CLASIFICADA`; `capa2_agregada` y `en_cola` sin tocar — dimensión distinta, no afectada por esta fusión). Resultado: 12 `CON-PUERTA-CLASIFICADA` · 1 `EQUIVALENCIA-AMBIGUA` · 62 `SIN-PUERTA`, de 75.

**No tocado, a propósito:** las dos filas de posible alias del lado de la demanda que §2 ya señaló sin resolver — `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018` y `GLOBAL_PREFERENCES_SURVEY` — siguen `SIN-PUERTA` aunque nombren temas cercanos a `CSES`/`GPS`; la evidencia de este acto no basta para fusionarlas con las demandas ya confirmadas, sigue siendo trabajo de un acto de alias, no de esta reconciliación. Tampoco se tocó la fila `WVS` (ya `CON-PUERTA-CLASIFICADA` desde antes de esta rama) aunque su `clasificacion_a4_de_la_puerta` copiada (`NO-ENCONTRADO`) quedó stale por la actualización que #186 hizo a la puerta real (ahora `EXISTE-SATISFACE`) — fuera del perímetro de "gap que gana puerta" que esta reconciliación cubre; declarado, no corregido aquí.

**Verificación de cierre:** `python3 tests/check.py --baseline` → resultado en el commit de cierre (ver hallazgos.md).

