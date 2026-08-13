# RECONCILIA-PUERTAS — el mapa del solape ADR-69/ADR-70 y la duplicidad interna de `universo-puertas`

**Acto:** RECONCILIA-PUERTAS (los dos artefactos pendientes-nombrados de ADR-69 y ADR-70) · **Cierra:** D11 · **Entorno:** NUBE, repo-only, sin gate · **Base:** `origin/main = 1e6e6a9` (post-PR #203, ALIAS-P+MOTOR-DIAG) · **Worktree:** `~/mm-reconcilia-puertas`, rama `reconcilia-puertas`.

## §0 · Premisas verificadas

```
git log origin/main -1                              -> 1e6e6a9 (merge PR #203)
python3 -c "import csv; ..." sobre universo-puertas  -> 114 filas de datos, 62 gap_mapeo_map_b, 52 no-gap
wc -l data/crosswalk-fuente-puerta-2026-08-13.tsv    -> 76 (75 filas + header)
grep -oE "ADR-[0-9]+" canon/gobernanza-v1_15.md | sort -u | wc -l   -> 73, contiguo 1..73
```

## §1 · Qué dice cada artefacto — no son tablas comparables

**`data/UNIVERSO-MINIMO-FUENTE-v1_0.md` (ADR-69, `canon/gobernanza-v1_15.md:896`).** No es un registro de fuentes: es una lista de **6 niveles** (payload+FD → PDF "Conociendo la base de datos" → ficha RNM → indicadores de calidad publicados → biblioteca → DOF) que un acto debe recorrer **antes** de declarar `NO-ENCONTRADO` sobre un campo **material** de una fuente **ya identificada**. Ámbito declarado explícitamente estrecho: **"para fuentes INEGI"** (`UNIVERSO-MINIMO-FUENTE-v1_0.md:18`) — el mecanismo (RNM, biblioteca INEGI, DOF) no generaliza a las demás instituciones. Alcance retroactivo acotado: solo donde un `NO-ENCONTRADO` bloquea hoy un cálculo o ficha (`:902`). No decide qué fuentes existen (`:12`).

**`data/universo-puertas-2026-08-12.tsv` (ADR-70(a)-(c), `canon/gobernanza-v1_15.md:908-920`).** Es un registro: 114 filas × 15 columnas, multi-institución (INEGI, CNBV, IMSS, STPS, INE, CONEVAL, Banco Mundial, GESIS, OSF, Zenodo, J-PAL, etc.), no solo INEGI. Tres cláusulas relevantes: **(a)** la RNM y fichas de fuentes activas entran al universo consolidado; **(b)** `documentacion_fuente` se vuelve campo de contrato exigido por `validate` en specs nuevas (cambio de esquema, sin contraparte en ADR-69); **(c)** "regla de conducto" — todo acto que descubra puerta/capacidad/restricción cierra subiendo la fila a la tabla o declarando por qué no. `ADR-70(d)` (congelamiento de `tools/curador_registro/`) y `(e)` (falsador/caducidad a 3 meses) son cláusulas propias de ADR-70 sin relación con el solape que este acto investiga — se nombran para no ocultarlas, no se tocan aquí.

## §2 · Dónde se solapan y difieren — ya resuelto por el propio ADR-70, no requiere adjudicación nueva

El párrafo "Solape con ADR-69, declarado" (`canon/gobernanza-v1_15.md:922`) ya contesta la pregunta a nivel de **regla**: ambos nacen del mismo hallazgo raíz (ficha RNM 922/E4b) pero *"resuelven preguntas distintas"* — ADR-69 es profundidad de búsqueda antes de un `NO-ENCONTRADO` sobre una fuente INEGI ya identificada; ADR-70(a)-(c) es completitud de registro para cualquier institución. **No compiten, componen:** una fila INEGI puede necesitar satisfacer el checklist de ADR-69 *y* la regla de conducto de ADR-70(c) a la vez, sin que ninguna de las dos "gane" sobre la otra. El propio párrafo ya declara por qué no se fusionan en un ADR — nada de esto necesita resellarse.

## §3 · La pregunta real no es entre artefactos — es una duplicidad dentro de `universo-puertas` misma

El encargo original preguntaba: *"cuando una fuente aparece en los dos [artefactos] con estados distintos, ¿cuál gobierna?"* Verificado contra el texto real: esa situación **no puede ocurrir tal como está planteada** — `UNIVERSO-MINIMO-FUENTE-v1_0.md` no tiene filas ni estados por fuente, es una lista de 6 pasos. La duplicidad real, verificada, vive **dentro del artefacto de ADR-70**: la misma fuente real aparece dos veces en `universo-puertas-2026-08-12.tsv` — una vez como fila `gap_mapeo_map_b`/`NO-ENCONTRADO` (creada por MAP-B por *ausencia* de evidencia de puerta) y otra vez como fila real con evidencia de portal (creada por un acto de sondeo posterior) — sin que la primera se retire. Es una ejecución parcial de la propia regla de conducto de ADR-70(c): la fila nueva sí se sube; la vieja no se marca. Reformulado así porque la pregunta original, aplicada literalmente, no tiene caso — declarado, no ocultado (mismo criterio que ADR-69(a)/(b) fijaron para sus propias correcciones de premisa).

## §4 · El caso testigo, verificado fila por fila — no son ~15, son 21 (+1 de confianza media) contradichas, y 2 falsos positivos declarados

Insumo del encargo ("~15 fuentes con dos filas contradictorias por SONDA-1") **no reprodujo**. Verificado por comando (normalización alfanumérica + subcadena, ver script abajo) y por lectura completa de las 21 filas nuevas no-`gap_mapeo_map_b` con fecha posterior a MAP-B (líneas 95-115, el bloque no alfabético anexado tras la corrida de MAP-B):

```python
import csv, re
rows = list(csv.reader(open('data/universo-puertas-2026-08-12.tsv', encoding='utf-8'), delimiter='\t'))[1:]
gap = [r for r in rows if r[1] == 'gap_mapeo_map_b']          # 62
real = [r for r in rows if r[1] != 'gap_mapeo_map_b']         # 52
norm = lambda s: re.sub(r'[^A-Z0-9]', '', s.upper())
# ver §4 para los 7 pares que esto captura mecánicamente, y por qué BIARE/IMSS son falsos positivos
```

**20 pares de alta confianza** (mismo `necesidad_que_sirve` exacto entre la fila vieja y la nueva, o cita explícita cruzada, o URL/título literal compartido — nunca solo cercanía de nombre):

| fila vieja (`gap_mapeo_map_b`) | fila nueva (real) | necesidades | evidencia |
|---|---|---|---|
| `GDELT` (:62) | `GDELT_RawDataFiles` (:102) | N17,N27 = N17,N27 | subcadena mecánica + necesidad exacta |
| `UCDP` (:92) | `UCDP_Downloads_GED` (:105) | N17,N27 = N17,N27 | subcadena mecánica + necesidad exacta |
| `ENCOAP` (:48) | `INEGI_ENCOAP_2023` (:101) | N2,N30 ⊂ N15,N16,N2,N30 | subcadena mecánica; **N15/N16 siguen sin puerta pese a resolverse la identidad** |
| `CNGMD` (:41) | `RNM_CNGMD_2023_catalogo977` (:106) | N28 = N28 | subcadena mecánica + necesidad exacta |
| `ISSP` (:69) | `GESIS_ISSP` (:100) | mismo conjunto de 7 | subcadena mecánica + necesidad idéntica |
| `OECD` (:79) | `OECD_TrustSurveyData` (:114) | N30 = N30 | subcadena mecánica + necesidad exacta |
| `GLOBAL_PREFERENCES_SURVEY` (:63) | `GPS_Global_Preferences_Survey` (:99) | N15 ≠ N2,N4,N5,N6,N17 | subcadena mecánica; **necesidades no coinciden** — confianza viene de MAP-B, no de esto (ver §5) |
| `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` (:68) | `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico` (:103) | N3,N17 = N3,N17 | título/necesidad idénticos |
| `ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION` (:45) | `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal` (:112) | N25 = N25 | fila nueva cita explícitamente que corrige la URL de la cola de esta misma fuente |
| `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` (:71) | `WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049` (:108) | N5 = N5 | título/necesidad idénticos |
| `IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM` (:66) | `WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039` (:109) | N28 = N28 | título verbatim citado en la fila nueva |
| `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` (:94) | `WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453` (:107) | N22,N23,N32 = N22,N23,N32 | título verbatim citado en la fila nueva |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` (:81) | `Cenfri_MicroinsuranceMexico` (:115) | N21 = N21 | URL de la fila nueva contiene el título literal de la fila vieja |
| `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` (:78) | `openICPSR_Microcredit_MexicoPlacement_proj116334` (:110) | N3 = N3 | necesidad exacta + "MexicoPlacement" |
| `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` (:44) | `JPAL_CorruptionInformation_MexicoVoters_2009` (:111) | N25 = N25 | necesidad exacta; título de la vieja es plausible título de artículo real de la nueva |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` (:49) | `Banxico_EncuestaCompetenciasFinancieras` (:113) | N29 = N29 | necesidad exacta; **MAP-B ya lo declaró duplicado de demanda** (§5) |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION` (:50) | `Banxico_EncuestaCompetenciasFinancieras` (:113) | N29 = N29 | ídem — dos filas viejas, una puerta real |
| `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` (:73) | `MassMobilization_Dataverse_MMdata` (:104) | N17,N27 = N17,N27 | necesidad exacta, título compartido |
| `MASS_MOBILIZATION_PROTEST_DATA` (:74) | `MassMobilization_Dataverse_MMdata` (:104) | N17,N27 = N17,N27 | ídem — tres filas viejas, una puerta real |
| `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` (:75) | `MassMobilization_Dataverse_MMdata` (:104) | N17,N27 = N17,N27 | ídem |

**1 par de confianza media**, corroborado de forma independiente por MAP-B (§5): `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018` (:42) ↔ `CSES_Modulo5_2016_2021` (:97) — N25 ⊂ {N17,N25,N26,N27}, pero el año/módulo citado difiere (2018 vs. Módulo 5 2016-2021); no se cuenta como confirmado por este acto solo, se apoya en la declaración de MAP-B.

**2 falsos positivos, verificados y descartados explícitamente — no se cuentan arriba:**
- `BIARE` (:38, necesidad N30) **no** es `RNM_ENBIARE_2021_ficha730` (:31) — el propio `ADR-73` (`canon/gobernanza-v1_15.md:995`, sellado horas antes de este acto) ya verificó que `BIARE` casa por subcadena embebida dentro de `enbiare` pero son *"fuente real distinta"*. La fuente real `ENBIARE` sí tiene su puerta, pero bajo el nombre `ENBIARE` (crosswalk :19), no `BIARE`.
- `IMSS` (:67, necesidad N18) **no** es `IMSS_Datos_Abiertos_Asegurados` (:3) — ya rechazado con razonamiento explícito por MAP-B (`data/crosswalk-fuente-puerta-2026-08-13.tsv:44`): misma institución, producto verificablemente distinto (encuestas de satisfacción vs. registro administrativo de asegurados).

Ambos falsos positivos importan: confirman que un mecanismo puramente de subcadena sobre-cuenta, y que la evidencia de identidad tiene que declararse, no inferirse por parecido — exactamente el principio que MAP-B ya había fijado (§5).

## §5 · Tercer artefacto no nombrado por el encargo, pero directamente decisivo: `data/crosswalk-fuente-puerta-2026-08-13.tsv`

No nombrado por ADR-69 ni ADR-70, pero citado por las 62 filas `gap_mapeo_map_b` (*"ver crosswalk-fuente-puerta-2026-08-13.tsv"*) — se leyó completo (76 líneas) porque ignorarlo habría reproducido trabajo ya hecho. Producido por `ACTO MAP-B` (`forense/notas/2026-08-13-map-b-crosswalk.md`, PR #189, ya fusionado).

**MAP-B ya fijó el método de equivalencia correcto — este acto lo reafirma, no lo reinventa.** Jerarquía declarada en `2026-08-13-map-b-crosswalk.md:18-22`: (1) URL coincide, (2) necesidad compartida *reforzada por* nombre/institución (necesidad sola no basta), (3) cita explícita en otro archivo del repo — **"nunca por parecido de cadena"**, literal, dos veces en la nota. La candidata de precedencia que el encargo de este acto proponía ("manda la `fecha_sondeo` más reciente...") es **más débil** que esto: aplicada ingenuamente por fecha sola, invierte el resultado correcto en el 100% de los 20 pares de §4, porque las filas `gap_mapeo_map_b` llevan `fecha_sondeo=2026-08-13` (fecha en que MAP-B las creó) y varias de las filas reales que las resuelven llevan `2026-08-12` — **la fila stale es más "reciente" que la real bajo lectura literal de fecha**. Ver §7 para la regla corregida.

**MAP-B ya corrió su propia reconciliación una vez (§3 de su nota) — no es una omisión, es que nadie la volvió a correr.** Al fusionar PR #186/#187 vía #189, retiró 5 filas gap propias (`CSES`, `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014`, `ENFIH`, `ENSAFI`, `GPS`) y actualizó el crosswalk correspondiente — verificado: ninguna de esas 5 sobrevive como fila `gap_mapeo_map_b` en el archivo real de hoy. Pero esa reconciliación fue manual y de una sola vez, contra el estado de `origin/main` en el momento del merge de MAP-B (anterior a SONDA-1/#197, P·Lote-1, M-ADQ y R2) — los ~19 puertas reales que esos actos posteriores abrieron para fuentes ya `gap_mapeo_map_b` **nunca pasaron por el mismo paso**. Esto es la causa raíz precisa: no hay mecanismo que obligue a re-aplicar el método de MAP-B cada vez que un acto de sondeo abre una puerta para una fuente que ya tenía fila `gap_mapeo_map_b` — la regla de conducto (ADR-70(c)) exige subir la fila nueva, pero no exige (todavía) retirar/marcar la vieja.

**MAP-B ya había nombrado 3 de los 4 pares "raros" de §4 como pendientes, sin resolverlos — corrobora, no descubre:** `2026-08-13-map-b-crosswalk.md:62,70` declara explícitamente `CSES`/`COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018`, `GPS`/`GLOBAL_PREFERENCES_SURVEY` y las dos `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_*` como *"el mismo instrumento real bajo dos identidades de `fuente_canonica` distintas... fuera de perímetro... trabajo de un acto de alias"*. Este acto no es ese "acto de alias" (eso resolvería duplicados del lado de la demanda en `relaciones.tsv`, un problema distinto y ya nombrado — MAP-B mismo lo dice, `:22`) — pero para el propósito de §4, la declaración de MAP-B es evidencia independiente que refuerza (no reemplaza) el veredicto de este acto sobre esas 4 filas.

**Una tercera staleness, menor, ya declarada por MAP-B y no corregida — se nombra para no repetir el patrón de "hallazgo que no llega a receta" que ADR-69(a) ya criticó:** la fila `WVS` del crosswalk (:76) copió `clasificacion_a4_de_la_puerta = NO-ENCONTRADO` al fusionar, pero la puerta real `WVS_World_Values_Survey` se actualizó a `EXISTE-SATISFACE` en la misma ventana — MAP-B lo declaró (`:70`) y no lo tocó, fuera de su perímetro. Fuera del perímetro de este acto también (es staleness del crosswalk, no de `universo-puertas`) — se nombra, no se repara aquí.

## §6 · Contador de esta parte

**Filas `gap_mapeo_map_b` en contradicción confirmada con una fila real, dentro de `universo-puertas-2026-08-12.tsv`: 21 de 62 (20 de alta confianza + 1 de confianza media corroborada por MAP-B), no las ~15 del pre-registro.** 2 candidatas adicionales verificadas y descartadas explícitamente (`BIARE`, `IMSS`), no cuentan. Contador que COMMIT 2 propone mover a 0 — vía marca, no vía edición de las filas existentes (ver §7).

---

## §7 · Commit 2 — regla de precedencia y cierre propuesta

**No se fusionan los artefactos aquí.** Lo que sigue es propuesta para que mesa selle; este acto no edita `universo-puertas-2026-08-12.tsv` ni `crosswalk-fuente-puerta-2026-08-13.tsv`.

**(a) Regla de equivalencia: se reafirma la de MAP-B, no se reemplaza.** `2026-08-13-map-b-crosswalk.md:18-22` ya la fijó — URL > necesidad reforzada por nombre/institución > cita explícita, nunca por parecido de cadena — y §5 mostró que es más sólida que la candidata que este mismo encargo proponía (fecha más reciente sola invierte el resultado en 20/20 casos verificados). Se mantiene sin cambio.

**(b) Cláusula de cierre que falta — enmienda a la regla de conducto de ADR-70(c).** Hoy (c) exige subir la fila nueva; no exige nada sobre la fila vieja. Texto propuesto:

> Todo acto que abra o actualice, en `data/universo-puertas-*.tsv`, una fila con `clasificacion_a4` distinta de `NO-ENCONTRADO` para una fuente que ya tiene una fila `clase_origen=gap_mapeo_map_b` en el mismo archivo, para declarar cerrado su conducto debe: **(1)** aplicar el método de equivalencia de MAP-B (§1 de `2026-08-13-map-b-crosswalk.md`) entre su puerta nueva y las filas `gap_mapeo_map_b` vigentes; **(2)** si hay evidencia de identidad, marcar la fila vieja con `superseded_por = <puerta nueva>` (columna nueva, aditiva) sin editar ni borrar el resto de su contenido, y actualizar la fila correspondiente de `crosswalk-fuente-puerta-*.tsv` de `SIN-PUERTA`/`VACIO` a `CON-PUERTA-CLASIFICADA`; **(3)** si no hay evidencia suficiente bajo ese método, no hace nada más — el gap sigue legítimamente abierto. Mecanismo de "no editar, marcar" con el mismo precedente que ya fijó `ADR-71(c)` (`canon/gobernanza-v1_15.md:934`): *"una entrada fechada posterior vence en alcance a la anterior, la anterior se conserva verbatim, y la nueva lo dice en su propia línea."* Mientras una fila `gap_mapeo_map_b` no tenga `superseded_por`, se trata como vigente.

## §8 · El diff exacto que implementaría la regla sobre el backlog de hoy

**En `data/universo-puertas-2026-08-12.tsv`:** añadir columna 16, `superseded_por` (vacía salvo donde se indica). **En `data/crosswalk-fuente-puerta-2026-08-13.tsv`:** para las mismas 20 filas por `fuente_canonica`, `puerta` pasa de `VACIO` al valor de la columna 2 de abajo, `clasificacion_a4_de_la_puerta` pasa al valor real (columna 3), `gap` pasa de `SIN-PUERTA` a `CON-PUERTA-CLASIFICADA`.

| fila vieja (`universo-puertas`, `superseded_por` nuevo valor) | puerta real | `clasificacion_a4_de_la_puerta` a copiar |
|---|---|---|
| `GDELT` | `GDELT_RawDataFiles` | EXISTE-NO-SATISFACE |
| `UCDP` | `UCDP_Downloads_GED` | EXISTE-NO-SATISFACE |
| `ENCOAP` | `INEGI_ENCOAP_2023` | EXISTE-SATISFACE |
| `CNGMD` | `RNM_CNGMD_2023_catalogo977` | EXISTE-SATISFACE |
| `ISSP` | `GESIS_ISSP` | EXISTE-SATISFACE |
| `OECD` | `OECD_TrustSurveyData` | NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS |
| `GLOBAL_PREFERENCES_SURVEY` | `GPS_Global_Preferences_Survey` | EXISTE-NO-SATISFACE |
| `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` | `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico` | EXISTE-SATISFACE |
| `ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION` | `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal` | EXISTE-SATISFACE |
| `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` | `WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049` | EXISTE-SATISFACE |
| `IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM` | `WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039` | EXISTE-SATISFACE |
| `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` | `WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453` | EXISTE-SATISFACE |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `Cenfri_MicroinsuranceMexico` | NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS |
| `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` | `openICPSR_Microcredit_MexicoPlacement_proj116334` | NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS |
| `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` | `JPAL_CorruptionInformation_MexicoVoters_2009` | EXISTE-SATISFACE |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` | `Banxico_EncuestaCompetenciasFinancieras` | EXISTE-SATISFACE |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION` | `Banxico_EncuestaCompetenciasFinancieras` | EXISTE-SATISFACE |
| `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` | `MassMobilization_Dataverse_MMdata` | NO OBTENIDO POR ESTE AGENTE EN 4 INTENTOS |
| `MASS_MOBILIZATION_PROTEST_DATA` | `MassMobilization_Dataverse_MMdata` | NO OBTENIDO POR ESTE AGENTE EN 4 INTENTOS |
| `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` | `MassMobilization_Dataverse_MMdata` | NO OBTENIDO POR ESTE AGENTE EN 4 INTENTOS |

**Aparte, condicionada a confirmación de mesa (confianza media, no automática):** `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018` → `CSES_Modulo5_2016_2021` (EXISTE-SATISFACE) — aplicar solo si mesa confirma que el módulo 2016-2021 cubre la ronda 2018 citada por la fila vieja; si no, queda `gap_mapeo_map_b` legítimo.

**No tocar** (verificado y descartado, no candidatas): `BIARE`, `IMSS`.

**Contador que este diff produce:** filas `gap_mapeo_map_b` en contradicción sin marcar: **21 → 0** (o 20 → 0 si mesa no confirma el par de confianza media, quedando esa fila abierta legítimamente en 1).

## §9 · ADR propuesto (no sellado por este acto)

**Candidato `ADR-74`** (73 únicos y contiguos en `canon/gobernanza-v1_15.md` al momento de este acto, `origin/main=1e6e6a9` — re-derivar contra el `main` real al sellar, mismo criterio que `ADR-71` y `ADR-73` ya dejaron escrito).

> **ADR-74 · Enmienda a la regla de conducto de ADR-70(c): obligación de reconciliar `gap_mapeo_map_b` al abrir puerta real, y columna `superseded_por`.** Decisión de mesa, sobre `ACTO RECONCILIA-PUERTAS` (`forense/notas/2026-08-13-reconcilia-puertas.md`).
>
> **(a)** Se añade a ADR-70(c) la obligación de cierre descrita en §7(b) de la nota citada — verbatim, no se repite aquí.
>
> **(b)** `data/universo-puertas-*.tsv` gana la columna `superseded_por` (16ª, aditiva, vacía por defecto). Ningún archivo fuera de `universo-puertas` y `crosswalk-fuente-puerta` cambia de esquema.
>
> **(c)** Se autoriza, como acto de mantenimiento separado (no este), aplicar el diff de §8 de la nota citada: 20 filas `gap_mapeo_map_b` marcadas `superseded_por`, más 1 condicionada a confirmación de mesa sobre el módulo ISSP/CSES citado ahí.
>
> **(d)** Se reafirma, sin cambio, el método de equivalencia de MAP-B (`2026-08-13-map-b-crosswalk.md:18-22`) como mecanismo vigente de identidad fuente↔puerta — no se sustituye por un criterio de fecha.
>
> **Cascada:** conteo de ADR vía receta T15, re-derivado al sellar. Contadores que NO se mueven: ninguno de medición sobre México — esta ADR es higiene de dos artefactos de registro, no una medición nueva.

**Cierre de este acto: no aplica el diff, no sella el ADR — los entrega a mesa, tal como el encargo lo pidió.**

## §10 · Addendum 1 — colisión real: PR #208 ya cerró este mismo encargo, desde `nube`

Al hacer `git fetch` para el cierre se descubrió `origin/main=959006a` y una rama ya borrada (`claude/reconcilia-puertas-adr-206k23`, mergeada como **PR #208, "Document reconciliation of ADR-69 and ADR-70 source door mappings", `2026-08-13T06:39:55Z`**) — el LANZAMIENTO original asignó `RECONCILIA-PUERTAS` a `nube`; esa sesión lo hizo, en paralelo a este acto en `caja`, sin que ninguna de las dos supiera de la otra hasta ahora. No es colisión de escritura (ningún worktree ajeno tocó éste) — es trabajo duplicado, mismo encargo, dos sesiones ciegas entre sí.

**Convergencia real, verificada leyendo su PR mergeado, no solo el resumen:** mismo método (URL/cita explícita, nunca parecido de cadena), misma conclusión de fondo ("la más reciente" sola falla — ellos en 14/16, este acto en 20/20), `GDELT`↔`GDELT_RawDataFiles` y `UCDP`↔`UCDP_Downloads_GED` idénticos en ambas listas por la misma evidencia de URL.

**Divergencia real, declarada, no resuelta aquí:** PR #208 cuenta **16** pares (no 21) y propone **borrar** las 16 filas `gap_mapeo_map_b` stale (114→98 filas) vía diff aplicado con `git apply --check`; este acto propuso **marcar** `superseded_por` sin borrar (precedente `ADR-71(c)`) sobre 21. No se concilian los dos conteos aquí — exigiría leer las 16 filas exactas de PR #208 fila por fila contra las 21 de este acto, trabajo nuevo fuera del perímetro ya cerrado de este acto.

**Resolución de este acto: no compite.** PR #208 es la versión mergeada y autoritativa — mesa ya la tiene. Este acto no abre PR propio (duplicaría el encargo ya cerrado). Las ramas/commits de este acto se preservan sin fusionar, vía ref nombrado en origin (`git push origin reconcilia-puertas:refs/heads/reconcilia-puertas-independiente-huerfana`), para que la convergencia/divergencia quede disponible si mesa quiere cotejar los dos conteos (16 vs. 21) más adelante — no se descarta silenciosamente.

## §11 · Addendum 2 — el mecanismo de duplicación se repitió mientras este acto corría (P·LOTE-2)

Al fusionar `origin/main` para el cierre (`fbe4e0a`, tras PR #204 P·LOTE-2 y PR #205 VERIFICA-PUERTAS), `universo-puertas-2026-08-12.tsv` ganó 4 filas más: `INEGI_ENCOAP_2023_adquisicion_PLOTE2`, `Banxico_EncuestaCompetenciasFinancieras_adquisicion_PLOTE2`, `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal_adquisicion_PLOTE2`, `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico_adquisicion_PLOTE2` — P·LOTE-2 descargó bytes reales para 4 de las mismas fuentes que §4 ya identificó (`ENCOAP`, `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_*`, `ELECTORAL_PRECINCT_LEVEL_DATABASE...`, `INTERACTING_AS_EQUALS...`), y lo hizo creando fila nueva con sufijo, no actualizando la fila real que SONDA-1 ya había puesto. **Confirma el mecanismo de §5/§6 en vivo, no lo cambia:** estas 4 fuentes ya estaban contadas dentro de las 21 de §4 (la fila `gap_mapeo_map_b` sigue siendo la misma, sin marcar); lo que cambia es que ahora hay dos filas *reales* por fuente (SONDA-1 + P·LOTE-2), no solo una. No se cuenta como contradicción nueva — no es `gap_mapeo_map_b` contra real, es real contra real, una pregunta distinta a la que este acto contestó. **Declarado para quien aplique el diff de §8:** para estas 4, `superseded_por` debería apuntar a la fila `_adquisicion_PLOTE2` (bytes+sha256 verificados, estrictamente más completa) en vez de a la fila de SONDA-1 citada en la tabla — el resto de la tabla no cambia. No se re-abre el análisis de §4 por esto; perímetro de este acto se mantiene.
