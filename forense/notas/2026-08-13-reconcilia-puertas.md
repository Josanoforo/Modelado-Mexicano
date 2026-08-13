# ACTO RECONCILIA-PUERTAS · El mapa del solape entre ADR-69 y ADR-70

`ENCARGO RECONCILIA-PUERTAS`, 13/ago/2026 (`forense/encargos/2026-08-13-reconcilia-puertas.md`), archivado como primer commit de este acto (regla A.3). Cierra **D11**. Base declarada por el encargo: ninguna explícita — se usa `origin/main` al abrir.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/user/Modelado-Mexicano`. `git log -1`: `b7aa67c Merge pull request #205 from Josanoforo/vp/verifica-puertas`. `git status`: árbol limpio al abrir.
2. **SHA.** `origin/main = b7aa67c`, exactamente el HEAD de este worktree — sin deriva que re-derivar.
3. **data/raw.** Ausente (`No such file or directory`) — irrelevante: este acto no abre microdato, es lectura de dos artefactos ya commiteados y de texto.
4. **ENTORNO.** Este acto no toca portal ni microdato — cero red. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE = cloud_default`, coherente con el entorno asignado (NUBE, repo-only). Se salta la sonda de `curl` — no aplica (punto 4 lo prevé explícitamente para actos que no tocan red).
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de `grep`/`awk`/`wc` corridos en este worktree en esta sesión, con el comando a la vista.

Las cinco líneas cuadran con lo que el encargo supone. Sin PARO. `python3 tests/check.py --baseline` corrido antes de escribir: **18 FAIL · 105 WARN, LÍNEA BASE VERDE** — igual al vigente, este acto todavía no ha tocado nada.

---

## 1 · Premisas verificadas (no heredadas del encargo sin re-derivar)

```
$ wc -l data/universo-puertas-2026-08-12.tsv
115 data/universo-puertas-2026-08-12.tsv                    → 114 filas de datos

$ awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l
62

$ wc -l data/UNIVERSO-MINIMO-FUENTE-v1_0.md
58 data/UNIVERSO-MINIMO-FUENTE-v1_0.md

$ grep -c -E "^[0-9]\." data/UNIVERSO-MINIMO-FUENTE-v1_0.md
6
```

Coincide exactamente con lo que el encargo declara (114 filas, 62 `gap_mapeo_map_b`). El "~15" de filas contradictorias **no** viene dado — es el caso testigo que este commit tiene que identificar fila por fila para que COMMIT 2 pueda escribir un diff exacto. §4 lo deriva.

---

## 2 · Los dos artefactos, campo por campo

### 2.1 · `universo-minimo-fuente` (ADR-69, sellado 12/ago sobre ENCARGO C)

**Qué es**, verbatim de su propia cabecera: *"La lista de sitios que un acto debe recorrer antes de declarar `NO-ENCONTRADO` sobre un campo material de una fuente."* Es una **receta en prosa**, no una tabla: seis niveles numerados, en orden de costo creciente (payload/descriptor en `data/raw` → PDF "Conociendo la base de datos" → ficha RNM → indicadores de calidad publicados → biblioteca digital INEGI → DOF). No tiene una fila por fuente; tiene una fila por *nivel de búsqueda*, aplicada a cualquier fuente que caiga en su alcance.

**Alcance declarado, textual — y es angosto.** El propio encabezado de la lista dice: *"La lista, para fuentes INEGI, en orden de costo creciente"* (`UNIVERSO-MINIMO-FUENTE-v1_0.md:18`). Los seis niveles son, además, específicos de la maquinaria INEGI — ficha RNM (`inegi.org.mx/rnm`), biblioteca INEGI (`inegi.org.mx/app/biblioteca`) — ninguno tiene equivalente declarado para un catálogo Banco Mundial, un repositorio Zenodo o un dataverse académico.

**Qué NO es**, también verbatim: *"No es una lista de dónde buscar fuentes nuevas — eso es `data/inventarios/` y `catalogo-fuentes-v2_0.md`"*. No decide qué fuentes existen; decide qué recorrido agotó lo barato antes de declarar un negativo.

**Verificable por:** `grep -c -E "^[0-9]\." data/UNIVERSO-MINIMO-FUENTE-v1_0.md` → 6 (verificado arriba). No produce ninguna cifra de estado — no hay "cuántas fuentes cumplieron el mínimo" derivable de este archivo solo.

### 2.2 · El puntero de puertas (ADR-70, sellado 12/ago sobre `PROPUESTA-remediacion-brecha-documental.md`)

**Qué es:** una tabla, 15 columnas (`puerta · clase_origen · institucion · url · tipo · cobertura_temporal · unidad_observacion · granularidad_geo · hay_microdato · condicion_acceso · necesidad_que_sirve · llave_ADR57c_si_alguna · clasificacion_a4 · universo_declarado · fecha_sondeo`), 114 filas. Cada fila es un **resultado** — de un sondeo real de portal, o (desde MAP-B, 13/ago) de un gap declarado sin sondeo.

**Alcance: universal, no restringido a INEGI.** `clase_origen` toma 7 valores distintos en el archivo real: `canasta_publica · catalogo_metadatos_inegi · ong_observatorio · organismo_internacional · repositorio_academico · transparencia · gap_mapeo_map_b` — cinco de los siete no son INEGI en absoluto (Banco Mundial, GESIS, OSF, Zenodo, CONEVAL, CONAPO, MCCI…).

**Vocabulario de `clasificacion_a4`** (ADR-70 hereda el vocabulario cerrado de `instrucciones-proyecto-v2_6.md` A.4/A.5/A.6, sellado el mismo 12/ago): `EXISTE-SATISFACE · EXISTE-NO-SATISFACE · NO-ENCONTRADO · NO-ACCESIBLE · NO OBTENIDO POR ESTE AGENTE EN N INTENTOS · SIN-FETCH`.

**Lo que ADR-70 añade que ADR-69 no toca en absoluto** (ya declarado así en `gobernanza:922`, verificado aquí, no repetido de memoria): ADR-70(b) hace `documentacion_fuente` un campo del contrato de producción (`tools/curador_registro/schemas/production-spec.schema.json:86-99` — confirmado, el campo existe, tipo `array` de `{url, fecha_consulta, campos_resueltos}`, no está en la lista `required` de nivel superior del schema; el enforcement real vive en `validate.py` para "specs nuevas", no en el schema estático). Es un artefacto de un tercer archivo — ninguna fila de `universo-puertas` ni ninguna línea de `UNIVERSO-MINIMO-FUENTE` lo menciona. Queda fuera del solape que este acto mapea.

**Verificable por:** los tres `wc`/`awk` de §1.

### 2.3 · Comparación campo por campo

| dimensión | ADR-69 · `universo-minimo-fuente` | ADR-70 · `universo-puertas-2026-08-12.tsv` |
|---|---|---|
| forma | receta en prosa, 6 niveles | tabla, 15 columnas, 114 filas |
| gobierna | el **proceso** antes de escribir un negativo | el **registro** del resultado (cualquier valor de A.4) |
| alcance declarado | "para fuentes INEGI" (línea 18, textual) | universal — 7 valores de `clase_origen`, mayoría no-INEGI |
| unidad | un nivel de búsqueda | una fuente sondeada (o un gap declarado) |
| produce fila propia | no — es la vara, no la medida | sí — una fila por `puerta` |
| vocabulario que usa | ninguno cerrado (es prosa) | A.4/A.5/A.6 (`EXISTE-SATISFACE`…) |
| campo de contrato que además toca | ninguno | `documentacion_fuente` en `production-spec.schema.json` (ADR-70(b), fuera de este solape) |
| verificación mecánica | `grep -c -E "^[0-9]\."` → 6 | `wc -l`, `awk -F'\t'` sobre columnas |

**No hay colisión de esquema.** Los dos artefactos no comparten una sola columna ni una sola llave — no hay fila de `UNIVERSO-MINIMO-FUENTE` que "compita" con una fila de `universo-puertas`. Cualquier lectura que buscara "fusionarlos" en una tabla única (como el pendiente de `gobernanza:922` deja abierto como posibilidad) estaría fusionando una receta con su propia bitácora de cumplimiento — formas distintas por diseño, no un accidente a corregir.

---

## 3 · Dónde se solapan de verdad — y las dos preguntas que hay que contestar

El solape no es de esquema, es de **momento**: el instante en que un acto está a punto de escribir `clasificacion_a4 = NO-ENCONTRADO` en una fila de `universo-puertas` es exactamente el instante en que ADR-69 exige haber agotado sus seis niveles. ADR-69 gobierna el *insumo* de una clase específica de fila de ADR-70. Cuando el proceso no se sigue, la tabla registra un negativo que no debería existir todavía — ese es el defecto que produce §4.

### Pregunta 1 (la que nombra el encargo) — precedencia entre filas

**Cuando una fuente aparece en dos filas de `universo-puertas` con estados distintos, ¿cuál gobierna?** Hoy no hay regla escrita. §4 identifica el caso testigo exacto (16 filas, no ~15 — derivado, no adivinado) y COMMIT 2 responde esta pregunta.

### Pregunta 2 (la que este commit encuentra, no la que cierra) — ¿a quién obliga ADR-69?

Los 62 `gap_mapeo_map_b` nacieron **sin recorrer ningún nivel de ADR-69** — MAP-B lo declara textualmente (`forense/notas/2026-08-13-map-b-crosswalk.md:34`): *"Cero red en ninguna de estas filas. Nacen `NO-ENCONTRADO` de mapeo, no de sondeo."* Su `universo_declarado` dice, verbatim y sin variación en las 62: *"buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL"* — dos tablas del propio programa, cero de los seis niveles de ADR-69 (payload propio, PDF, ficha RNM, indicadores de calidad, biblioteca, DOF).

Para las fuentes de acrónimo reconociblemente INEGI, eso es una violación clara y verificada del espíritu de ADR-69 — el mismo defecto que motivó ADR-69 (ENASIC declaró `NO_DETERMINADO` sin llegar al tercer sitio), solo que aquí ni siquiera se llegó al primero. Verificado, no de memoria (`data/inventarios/inventario_fuentes_*.md`, `revision-publicacion-2026-07-30.md:88`, y las fichas RNM ya en el propio puntero):

```
INEGI confirmado           ENAFIN · ENCIG · ENCOAP · ENCUP · ENIF · ENIGH · ENOE · ENVIPE · CNGMD   (9 de 62)
NO-INEGI, pese al patrón    ENNVIH  —  "ENNViH/MxFLS ... no es INEGI" (revision-publicacion-2026-07-30.md:88;
                            panel académico, MxFLS, requiere registro propio)
resto (52 de 62)            no-INEGI por institución declarada o por ausencia de institución
                            (ACLED, GDELT, UCDP, Banco Mundial, académicas, ONG, financieras…)
```

**Pero el título de ADR-69 dice "para fuentes INEGI".** Como está escrito hoy, no reclama jurisdicción sobre los otros 53 (52 no-INEGI + `ENNVIH`, que solo lo parece). Eso deja una pregunta real y no retórica: ¿el mínimo de búsqueda de ADR-69 rige, en espíritu, para *cualquier* fuente del universo consolidado (lo que ADR-70(c), la regla de conducto, parece asumir sin decirlo — *"toda nota de exploración que descubra puerta, capacidad o restricción cierra su acto subiendo la fila... o declarando por qué no"*, sin distinguir INEGI de no-INEGI), o el mínimo de búsqueda para fuentes no-INEGI sencillamente no existe todavía y los 53 gap no-INEGI no violan ninguna regla escrita, solo una que falta?

**Esta pregunta no la contesta este acto.** No es la pregunta que el encargo nombra (§4 es el caso testigo de la Pregunta 1, no de ésta), y contestarla bien exigiría diseñar un mínimo de búsqueda propio por tipo de institución (qué es el "nivel 3, ficha de catálogo" para un repositorio Zenodo, o para un catálogo Banco Mundial) — trabajo de otro acto. Queda **nombrada, no resuelta**, en §5.

---

## 4 · El caso testigo: 16 filas contradictorias, identificadas una por una

### 4.1 · Método, declarado antes de cruzar nada (mismo criterio que MAP-B, §1 de `map-b-crosswalk.md`)

Ninguna identidad se declara por parecido de cadena. Jerarquía de evidencia, en orden:

1. **URL idéntica** entre `data/cola-adquisicion-2026-08-12.tsv.url_conocida` (columna 6) y `universo-puertas.url` (columna 4) de la fila real.
2. **Cita explícita**, dentro del propio texto de la fila real, que nombre la fuente vieja o corrija su URL (caso `Zenodo_ElectoralPrecinctLevel…`, que declara byte a byte por qué la URL de la cola estaba mal transcrita; caso `GESIS_ISSP`, que se auto-cita contra el hallazgo de `cola-adquisicion` para N3).
3. **Declaración propia de SONDA-1** (`forense/notas/2026-08-12-acto-sonda1-mapa-barreras.md §6`), que nombra sus 15 fuentes por `palanca` de la cola y confirma, comando en mano, que las 15 ya tenían fila `gap_mapeo_map_b` propia.

Rechazado explícitamente, no en silencio (mismo principio que MAP-B): **parecido de nombre solo, sin URL/cita que confirme, no basta.** Ver §5.2 para los casos que este criterio excluye.

### 4.2 · Las 16 filas, verificadas por comando

```bash
$ while read -r p; do
    n=$(awk -F'\t' -v p="$p" '$1==p' data/universo-puertas-2026-08-12.tsv | wc -l)
    cls=$(awk -F'\t' -v p="$p" '$1==p{print $2}' data/universo-puertas-2026-08-12.tsv)
    echo "$p -> matches=$n clase_origen=$cls"
  done < retirar.txt
# las 16 dan matches=1 clase_origen=gap_mapeo_map_b — cada una tiene exactamente
# una fila vieja, y esa fila es siempre la de universo interno.
```

| # | fuente (fila vieja, `gap_mapeo_map_b`) | puerta real (fila nueva) | evidencia | fecha vieja → nueva |
|---|---|---|---|---|
| 1 | `GDELT` | `GDELT_RawDataFiles` | URL exacta (`gdeltproject.org/data.html`) | 08-13 → 08-12 |
| 2 | `UCDP` | `UCDP_Downloads_GED` | URL exacta (`ucdp.uu.se/downloads/`) | 08-13 → 08-12 |
| 3 | `ENCOAP` | `INEGI_ENCOAP_2023` | URL exacta | 08-13 → 08-12 |
| 4 | `CNGMD` | `RNM_CNGMD_2023_catalogo977` | URL exacta | 08-13 → 08-12 |
| 5 | `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` | `WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453` | URL exacta | 08-13 → 08-12 |
| 6 | `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` | `WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049` | URL exacta | 08-13 → 08-12 |
| 7 | `IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM` | `WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039` | URL exacta | 08-13 → 08-12 |
| 8 | `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` | `openICPSR_Microcredit_MexicoPlacement_proj116334` | URL exacta | 08-13 → 08-12 |
| 9 | `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` | `JPAL_CorruptionInformation_MexicoVoters_2009` | URL exacta | 08-13 → 08-12 |
| 10 | `ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION` | `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal` | cita propia (corrige DOI mal transcrito de la cola) | 08-13 → 08-12 |
| 11 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION` | `Banxico_EncuestaCompetenciasFinancieras` | URL exacta | 08-13 → 08-12 |
| 12 | `OECD` | `OECD_TrustSurveyData` | URL exacta | 08-13 → 08-12 |
| 13 | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `Cenfri_MicroinsuranceMexico` | URL exacta | 08-13 → 08-12 |
| 14 | `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` | `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico` | URL exacta | 08-13 → 08-12 |
| 15 | `MASS_MOBILIZATION_PROTEST_DATA` | `MassMobilization_Dataverse_MMdata` | URL exacta (de las 3 variantes `MASS_MOBILIZATION_*`, la única con URL en la cola) | 08-13 → 08-12 |
| 16 | `ISSP`† | `GESIS_ISSP` | cita propia (`GESIS_ISSP` se compara contra el hallazgo N3 de `cola-adquisicion` por nombre) | 08-13 → 08-13 |

**Filas 1-15 = exactamente las 15 que el propio SONDA-1 declara**, verbatim, en su nota de cierre (`2026-08-12-acto-sonda1-mapa-barreras.md §6`): *"Las 15 fuentes de este lote ya tenían una fila `gap_mapeo_map_b`/`NO-ENCONTRADO` propia... esas 15 filas viejas quedan tal cual, ahora stale... Retirarlas es trabajo de un acto tipo MAP-B... no de este."* Ese acto es este.

**† Fila 16, `ISSP`, es un caso hermano, no del lote de SONDA-1** — el propio SONDA-1 lo señala y explícitamente lo deja fuera de su cuenta de 15 por no ser una fila que él haya escrito (`§2`): *"La fila bare `ISSP` que sí aparece `NO-ENCONTRADO` es un artefacto de MAP-B... no reabre el caso."* `GESIS_ISSP` (fila real) viene de un tercer acto (`ACTO R″`, `forense/notas/2026-08-13-r2-registro-via-completa.md`), no de SONDA-1. Se incluye aquí porque cumple exactamente el mismo patrón — vieja fila interna, nueva fila de portal, mismo `fecha_sondeo` del día (13/ago para ambas, verificado: la vieja por MAP-B, la nueva por `ACTO R″`) — y porque dejarla fuera del diff de COMMIT 2 sería reproducir el mismo defecto que este acto existe para cerrar.

**Conteo, dos formas de contarlo, ninguna en conflicto con la otra:** como lo nombra el encargo — el lote propio de SONDA-1, **15** — o medido completo por este acto — **16**, sumando el caso hermano que SONDA-1 mismo señaló sin resolver. COMMIT 2 usa 16.

### 4.3 · Por qué "la fecha más reciente gana", sola, habría elegido mal

En **14 de las 16** parejas, la fila vieja (`gap_mapeo_map_b`) trae `fecha_sondeo = 2026-08-13` — **posterior** a la fila real que la contradice (`2026-08-12`). Verificado en la tabla de §4.2, columna final. Si la regla de precedencia fuera solo "gana la fecha más reciente", **GDELT, UCDP, CNGMD, ENCOAP y diez más se resolverían hacia el lado equivocado** — la fila que dice `NO-ENCONTRADO` contra dos tablas internas le ganaría a la fila que sondeó el portal real con `curl -r 0-0` y confirmó bytes. Es la razón textual por la que la candidata del encargo no dice "la más reciente" a secas, sino "la más reciente **cuyo `universo_declarado` cite un portal, no una tabla interna**" — la cláusula de portal no es un adorno, es lo que evita que la regla escoja mal en 14 de 16 casos reales. COMMIT 2 lo retoma.

---

## 5 · Hallazgos adyacentes — declarados, no resueltos en este commit

### 5.1 · La Pregunta 2 (§3): alcance de ADR-69 fuera de INEGI

Repetido de §3 para que quede en un solo lugar de "pendientes": **si ADR-69 rige (en espíritu) fuentes no-INEGI, o si esas 53 filas gap no violan nada escrito.** No se adivina aquí. Candidato para un acto propio o para una cláusula del ADR que selle COMMIT 2 — ver "Qué NO hace" en la propuesta.

### 5.2 · Duplicados aparentes del lado de la demanda — un defecto distinto, ya nombrado por MAP-B, no reabierto aquí

Cinco casos donde una fila `gap_mapeo_map_b` **parece** nombrar la misma fuente que otra fila (real o gap) bajo una identidad de `fuente_canonica` distinta — pero sin URL ni cita que lo confirme, solo cercanía de nombre o de tema. Rechazados por el método de §4.1, igual que MAP-B ya los rechazó en su momento (`map-b-crosswalk.md §2`, *"fuera de perímetro... trabajo de quien mantenga `aliases-fuentes.tsv`"*):

- `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018` (gap, fila 42) — nombre completo de `CSES`, que ya tiene puerta real (`CSES_Modulo5_2016_2021`). Sin URL propia en la cola que lo confirme.
- `GLOBAL_PREFERENCES_SURVEY` (gap, fila 63) — mismo patrón contra `GPS`/`GPS_Global_Preferences_Survey`.
- `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` (gap, fila 49) — nombre casi idéntico a la fila 11 de §4.2 (`…_DE_LA_POBLACION`, que sí se retira, confirmada por URL). Ésta, sin URL en la cola, no se toca.
- `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` (fila 73) y `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` (fila 75) — variantes de la fila 15 de §4.2, que sí se retira por tener la URL confirmada. Estas dos, sin URL propia, no se tocan.
- `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009` (gap, fila 58) — posible duplicado de la fila 9 de §4.2 (`DOES_CORRUPTION_INFORMATION_INSPIRE…`, que sí se retira). Sin URL propia en la cola.

Son evidencia de un defecto real — el mismo instrumento entra dos veces al lado de la demanda con dos identidades de `fuente_canonica`, MAP-B ya lo documentó y no lo resolvió — pero es un defecto de *alias del lado de la demanda* (`relaciones.tsv`/`aliases-fuentes.tsv`), no del solape ADR-69↔ADR-70 que este acto reconcilia. Fusionarlos aquí, sin URL ni cita, sería exactamente el "por parecido de cadena" que §4.1 y el propio MAP-B prohíben. No entran al diff de COMMIT 2.

### 5.3 · Un patrón sano, para que no se lea como si todo el archivo estuviera roto

No todas las correcciones del puntero son filas duplicadas sin retirar. `WVS_World_Values_Survey` (fila 26) y las fichas `RNM_ENSAFI_2023`/`RNM_ENFIH_2019` (filas 95-96) muestran el patrón correcto — **corrección en el mismo renglón** ("ACTUALIZA la fila de…", "CORRECCION post-revision") en vez de una fila nueva al lado de la vieja. El defecto de §4 es específico de la transición *gap interno → hallazgo real*, no general al archivo.

---

## 6 · Qué entrega este commit, y qué no

**Entrega:** el mapa campo por campo (§2), las dos preguntas de gobierno (§3), y las 16 filas del caso testigo, identificadas con evidencia verificable por comando, no por parecido (§4).

**No fusiona nada.** No edita `data/universo-puertas-2026-08-12.tsv`. No edita `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`. No sella ninguna regla de precedencia — eso es COMMIT 2, con su propio diff y su propio ADR propuesto, sin sellar aquí. No resuelve §5.1 ni §5.2 — quedan nombrados.

**Cascada.** Ningún contador de Hito D, coeficientes o probabilidades del motor se mueve — este acto es aparato de gobierno del propio programa, no medición sobre México. El contador que instituye este acto es el que trae COMMIT 2: filas contradictorias del puntero, hoy **16** (medido; el encargo decía "~15", cifra del lote de SONDA-1 sin el caso hermano de ISSP), propuestas a **0**.
