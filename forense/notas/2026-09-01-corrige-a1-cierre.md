# Cierre de `ACTO MAESTRA33-A2 · CORRIGE-A1`

Nota propia del ejecutor (`forense/notas propia` del perímetro declarado
en `forense/encargos/2026-08-31-MAESTRA33-A2-CORRIGE-A1.md`). Detalle
crudo de `P1` (re-corrida de `A.8` fila por fila) y `P2` (absorción de la
quinta cola), para que quien audite después no tenga que repetir el
trabajo — es exactamente lo que la calibración de `A1`
(`forense/notas/2026-08-31-revisa-calibracion-maestra33-a1.md`) pidió que
faltaba.

---

## §1 · Método de `P1`

`data/manifiesto.yaml` tiene **794** entradas, todas con clave `id:` — no
tiene ningún campo `payload_id` (`grep -c` → `0`), que es el universo
contra el que el `A.8` de `WVS` se había corrido por error en `PR #414`.
Cada fila de `data/cola-adquisicion-v1_0.tsv` se re-corrió por uno de dos
métodos, según su `estado_A4A5` de entrada:

- **Filas ya `OBTENIDO`** (21 de 72): existencia de cada `id` listado en
  `ids_manifiesto` contra el campo `id:` real del manifiesto — detecta un
  id inventado o mal transcrito, no solo un id ausente.
- **Filas NO `OBTENIDO`** (51 de 72: `PENDIENTE`, `NO-ACCESIBLE`,
  `NO-OBTENIDO-POR-ESTE-AGENTE`): re-chequeo de ausencia — host de
  `url_conocida` (si la fila lo trae) contra `url_origen:` de cada
  entrada, y patrón de nombre derivado de `fuente_canonica` contra
  `usado_para:`/`id:`/`url_origen:`. Criterio de acierto de `A.8`
  (`.claude/commands/adquiere.md` §2): host exacto **y** patrón de
  nombre — un acierto de un solo lado se inspecciona a mano antes de
  aceptarlo, igual que exige la skill.

Comando base, corrido por fila (`794` entradas examinadas cada vez,
A.13):

```
python3 -c "... grep equivalente sobre id:/usado_para:/url_origen: ..."
```

(script completo corrido interactivamente sobre un parseo de
`data/manifiesto.yaml` en 794 entradas; no se pegó aquí por longitud —
cada resultado de la tabla de §3 es reproducible re-derivando el mismo
parseo).

**Nueve filas cambian de estado; el resto queda verificado sin cambio.**
Detalle de las nueve en §2. Ningún resultado de este acto vino de
"conocimiento del modelo" ni de inferencia sin comando — A.5/A.6, la
misma disciplina que el propio encargo exige.

---

## §2 · Las nueve correcciones, con el comando que las sostiene

### 1 · `WVS` → `OBTENIDO`

El `BLOQUEA` portante de la calibración. El `A.8` original citaba *"0 de
489 `payload_id` del inventario"* — ese campo no existe en
`data/manifiesto.yaml`. Re-corrido:

```
$ grep -c 'payload_id' data/manifiesto.yaml
0
$ grep -c '^- id:' data/manifiesto.yaml
794
```

Búsqueda por host (`worldvaluessurvey.org`, de `url_conocida`) + nombre
(`wvs`): **11** entradas, **6** microdato:

```
f00013032_wvs_wave_7_mexico_spss_v5_1
f00013084_wvs_wave_7_mexico_stata_v5_1
f00013146_wvs_wave_7_mexico_csv_v5_1
f00013203_wvs_wave_7_mexico_excel_v5_1
f00013259_wvs_wave_7_mexico_exceltxt_v5_0
f00013316_wvs_wave_7_mexico_csvtext_v5_1
```

Las otras 5 (cuestionario, informe de metodología, ficha del equipo,
diseño muestral, codebook v3.0) documentan el mismo estudio — no entran
a `ids_manifiesto` por no ser microdato.

### 2 · `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` → `OBTENIDO`

La fila ya declaraba *"posible duplicado de `ECEPIE_CIDE_WB_2012_2014`
(cola-ext-academico-2026-08-06.tsv:5, mismos años) — no forzado"*.
Verificado: **no es duplicado, es el mismo estudio**.

```
$ grep -A1 'ecepie' data/manifiesto.yaml | grep usado_para | head -1
  usado_para: microdato PUF (formatos SAS/SPSS/ASCII/Stata12) -- Early Childhood Education
    Program Impact Evaluation 2012-2014 (Banco Mundial catalogo 2661)
```

5 ids `mex_2012_2014_ecepie_*` (microdato PUF real, adquirido 2026-08-13
vía navegador) + 7 ids `wb2661_*` (documentación: ASQ questionnaires,
instrumentos y reportes de Baseline/Year1/Endline, adquirida 2026-08-12
directo de `microdata.worldbank.org` sin sesión) = **12 ids**, mismo
catálogo del Banco Mundial (`2661`) en ambos grupos.

### 3 · `ACLED` → `OBTENIDO`

```
$ grep -A6 'r7_4_r7_5_acled_hdx_demonstration_events' data/manifiesto.yaml | grep -E 'fecha_descarga|sha256'
  fecha_descarga: '2026-08-06'
  sha256: 376bdf04ca9c319950ede74c1711c9f8f3c55df52d3ef45afd07175bd157e8f6
```

1 entrada real y registrada. Límite preservado en la nota: agregado
MES×AÑO, **no** evento individual georreferenciado — esa granularidad
fina vive en `acleddata.com` gateada por registro, no intentada (SIN
sondear red).

### 4 · `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` → `OBTENIDO`

```
$ grep -c 'osf_iae' data/manifiesto.yaml
10
```

10 entradas, `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico`,
paquete de replicación completo (`.dta`/`.xlsx`), coincide por nombre
exacto con la fila.

### 5 · `ENCOAP` → `OBTENIDO`

```
$ grep -A1 'inegi_encoap_2023_csv' data/manifiesto.yaml | grep usado_para
  usado_para: 'P-LOTE-2 (N2,N30): ENCOAP 2023, microdato formato CSV, palanca 17'
```

1 entrada, microdato 2023. Ola 2025 (que la fila también nombra) **no**
está en el manifiesto — no se asume, queda pendiente esa ola si mesa la
requiere.

### 6 · `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` → `OBTENIDO`

```
$ grep -c 'lfepie' data/manifiesto.yaml
4
$ grep -A1 'mex_2011_lfepie_v01_m$' data/manifiesto.yaml | grep usado_para
  usado_para: microdato PUF -- Large-Scale Financial Education Program Impact Evaluation 2011-2012
    (Banco Mundial catalogo 2049)
```

4 entradas, microdato PUF real. Resuelve el "posible duplicado" con
`LFEPIE_2011_2012` declarado en la fila: mismo estudio.

### 7-8 · `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` y `..._RANDOMIZED_..._PLACEMENT_EXP` → `OBTENIDO`

```
$ grep -A3 '^- id: 116334_v1' data/manifiesto.yaml | grep usado_para -A2
  usado_para: paquete de replicación AEJ 'Compartamos_AEJ' (RCT de colocación de microcrédito)
    -- identificado por listado interno del zip; openICPSR proj116334 (fila 110, bloqueado
    Cloudflare para el agente); resuelve también filas 77/78 gap_mapeo_map_b (MICROCREDIT_IMPACTS_COMPARTAMOS_RCT
    / RANDOMIZED_..._PLACEMENT_EXP)
```

El propio manifiesto declara, en su `usado_para`, que este único payload
resuelve **ambas** filas — no son fuentes separadas. `TRIAGE-63` (nota
previa citada por ambas filas) ya había identificado `openICPSR 116334`
como candidata; se confirma que se adquirió después (`fecha_descarga
2026-08-13`).

### 9 · `ENIF` → `OBTENIDO`

La fila decía explícitamente *"PENDIENTE-VERIFICAR, no
PENDIENTE-DE-CERO... fuera del tiempo disponible de esta caminata"*.

```
$ grep -c 'enif' data/manifiesto.yaml
21
```

21 entradas: microdato en 5 olas (2012, 2015, 2018, 2021, 2024) en
CSV/DBF/SAV, más documentación (FD/cuestionario/modelo) por ola. Serie
histórica completa.

### Nota, no corrección · `OECD`

```
$ grep -A1 '^- id: ea3385cf_en' data/manifiesto.yaml | grep usado_para
  usado_para: OECD Survey on Drivers of Trust in Public Institutions in Latin America and
    the Caribbean, 2025 Results -- identificado por texto propio del PDF...
```

Candidato real, pero el código bare `OECD` de la fila no especifica cuál
encuesta se busca — no se fuerza el emparejamiento, mismo criterio que el
resto de la tabla usa para "posible duplicado, no forzado". Nota añadida,
estado sin cambio.

---

## §3 · Tabla completa, las 72 filas originales (A.13 por fila)

| fila | fuente_canonica | tipo de chequeo | campo(s) consultado(s) | entradas examinadas | resultado |
|---|---|---|---|---|---|
| 2 | `ISSP` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 3 | `ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 4 | `WVS` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 5 | `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 6 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 7 | `GPS` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 8 | `CSES` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 9 | `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 10 | `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 11 | `ACLED` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 12 | `GDELT` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 13 | `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 14 | `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 15 | `MASS_MOBILIZATION_PROTEST_DATA` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 16 | `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 17 | `UCDP` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 18 | `ENCOAP` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 19 | `MEXICO_PANEL_STUDY_2012` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 20 | `SE` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 21 | `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 22 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 23 | `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 24 | `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 25 | `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 26 | `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 27 | `BASE_DEL_OBSERVATORIO_DE_CONFLICTOS_POR_EL_AGUA` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 28 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 29 | `CNGMD` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 30 | `COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 31 | `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 32 | `ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 33 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 34 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 35 | `HOMESCAN_CONSUMER_PANEL_SERVICES` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 36 | `IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 37 | `OECD` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | nota de candidato añadida, sin forzar (ver §2) |
| 38 | `PANEL_DE_COMPRA_DE_HOGARES` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 39 | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 40 | `REGISTRO_DE_TANDAS_Y_REPUTACION` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 41 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 42 | `REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 43 | `SICS` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 44 | `VOTAR_ENTRE_BALAS` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 45 | `ENIF` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | **CORREGIDO → `OBTENIDO`** (ver §2) |
| 46 | `SERIES_SPEI_CODI_BANXICO` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 47 | `INE` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 48 | `AHORRO FINANCIERO Y FINANCIAMI` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 49 | `BDIF` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 50 | `ENAFIN` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 51 | `PI` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 52 | `ENCUP` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 53 | `LAPOP` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 54 | `LATINOBARÓMETRO` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 55 | `PUB` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 56 | `ISSP_FAMILY_2012_MEXICO` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 57 | `CAPITAL_RETURNS_LEON_2005_2006` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 58 | `EARTHQUAKE_TRUST_LAPOP_2017` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 59 | `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 60 | `CERO_DESABASTO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 61 | `MERCER_GPTW_CLIMA_DESEMPENO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 62 | `OBSERVATORIO_DE_CUIDADOS_INDICADORES_TERRITORIALES` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 63 | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 64 | `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 65 | `EXT_OF_03_PARTICIPACION_LOCAL_2024` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 66 | `EXT_OF_08_ASF_INFORME_2023` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 67 | `EXT_OF_01_IEPC_JALISCO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 68 | `EXT_OF_09_AGENDA_GASTO_CANDIDATURA` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 69 | `EXT_OF_10_SESNA_INFORME` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 70 | `EXT_OF_11_REUNE_REDECO` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 71 | `EXT_OF_12_PREP_2024` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |
| 72 | `EXPERIMENTO_INFORMACION_ELECTORAL_2009` | existencia de id (fila ya `OBTENIDO`) | `id:` | 794 | sin cambio (ids verificados existentes) |
| 73 | `FINANZAS` | re-chequeo de ausencia (fila NO `OBTENIDO`) | `id:`+`usado_para:`+`url_origen:` | 794 | sin cambio |

**Total: 30 `OBTENIDO`, 35 `PENDIENTE`, 6 `NO-ACCESIBLE`, 1
`NO-OBTENIDO-POR-ESTE-AGENTE`** sobre las 72 filas originales (antes de
`P2`). Re-derivado por comando:

```
$ awk -F'\t' 'NR>1 && NF {print $2}' data/cola-adquisicion-v1_0.tsv | sed -E 's/\(.*//' | sort | uniq -c
     30 OBTENIDO
     35 PENDIENTE
      6 NO-ACCESIBLE
      1 NO-OBTENIDO-POR-ESTE-AGENTE
```

---

## §4 · `P2` — absorción de `data/cola-aperturas-externas-2026-08-06.tsv`

15 filas, mapeadas por tema contra la tabla viva (14 con equivalente, 1
sin él):

| orden | fuente (cola-aperturas) | destino en la tabla viva |
|---|---|---|
| 1 | Auditoría ASF 165-DS Servicios de vacunación ISSSTE 2024 | **sin equivalente** — fila nueva `AUDITORIA_ASF_165_DS_SERVICIOS_VACUNACION_ISSSTE_2024`, `PENDIENTE`, prioridad `aperturas-1` |
| 2 | Encuesta Anual de Competencias Financieras Banxico 2019-2024 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` |
| 3 | Reporte IFT uso y confianza SFD | `REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES` |
| 4 | Cero Desabasto | `CERO_DESABASTO` |
| 5 | Experimento de información electoral 2009 | `EXPERIMENTO_INFORMACION_ELECTORAL_2009` |
| 6 | Mexico Enterprise Surveys panel candidato 2006-2010 | `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` |
| 7 | Compartamos RCT 2008-2012 | `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` |
| 8 | Large-Scale Financial Education Program 2011-2012 | `LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2` |
| 9 | ISSP Social Networks 2017 México | `ISSP` |
| 10 | ISSP Family and Changing Gender Roles 2012 México | `ISSP_FAMILY_2012_MEXICO` |
| 11 | CSES Module 5 México 2018 | `CSES` |
| 12 | Mass Mobilization Protest Data México | `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` (+ cruce a `MASS_MOBILIZATION_PROTEST_DATA`, mismo payload) |
| 13 | Votar entre Balas | `VOTAR_ENTRE_BALAS` |
| 14 | ENCOAP 2023/2025 | `ENCOAP` (sólo ola 2023 confirmada) |
| 15 | Early Childhood Education Program Impact Evaluation 2012-2014 | `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` |

Verificación de la fila 1 (sin equivalente), antes de darla por nueva
(A.13):

```
$ grep -ci 'issste' data/manifiesto.yaml
0
$ grep -ci '165-ds\|165ds' data/manifiesto.yaml
0
$ grep -i 'vacunaci' data/manifiesto.yaml | wc -l
7
```

Las 7 menciones de "vacunación" que sí existen son genéricas (módulos de
encuestas de salud tipo ENSANUT que preguntan por vacunación como tema,
no la auditoría ASF específica) — verificadas a mano, ninguna nombra
ISSSTE ni 165-DS.

Cada una de las 14 filas mapeadas recibe el puntero
`cola-aperturas-externas-2026-08-06.tsv:N` en su columna `origen`,
**sin** tocar `estado_A4A5` ni `ids_manifiesto` (eso ya lo hizo `P1`).

Desglose final, tras `P1`+`P2` (73 filas):

```
$ awk -F'\t' 'NR>1 && NF {print $2}' data/cola-adquisicion-v1_0.tsv | sed -E 's/\(.*//' | sort | uniq -c
     36 PENDIENTE
     30 OBTENIDO
      6 NO-ACCESIBLE
      1 NO-OBTENIDO-POR-ESTE-AGENTE
```

---

## §5 · Suite y cierre

`python3 tests/check.py --baseline`: **VERDE — nada nuevo frente a
`tests/baseline.json`** (`19 FAIL`, HEAD congelado `c6a0d72`). `T15` y
`T25` en `[ ok ]`, verificados explícitamente antes de escribir la
entrada de gobernanza (ningún rótulo `M`/`E` pelado nuevo, ninguna cita
de conteo de `ADR` sin marcar). Anti-`PR#77`: no aplica, este acto no
descargó nada.

**Contador: cero, declarado.** Corrige registros de adquisición
(estados/ids/punteros), no mide México.

**Lo que este acto NO hizo**, por mandato explícito del encargo: no
sondeó red, no descargó nada, no re-ejecutó la caminata de `/adquiere`
(ninguna fila `NO-OBTENIDO-POR-ESTE-AGENTE` se reintentó — `A.5`), no
tocó `milpa/**`. Las tres decisiones que `FP-211` dejaba pendientes de
mesa (activar la rutina de `/revisa` por evento; qué hacer con los
hallazgos ahora corregidos; ajustar los dos pesos bajo sospecha de la
lista de diez puntos) siguen sin decidir — no eran de este acto.
