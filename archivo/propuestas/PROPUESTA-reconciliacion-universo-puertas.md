# PROPUESTA · Precedencia entre ADR-69 y ADR-70 sobre el puntero de puertas
### v0.1 · 13/ago/2026 · ACTO RECONCILIA-PUERTAS, COMMIT 2 · propuesta sin sello; mesa aprueba sellando el ADR candidato de §3 y aplicando el diff de §2, o los enmienda

| | |
|---|---|
| **EL DEFECTO, NOMBRADO** | 16 filas de `data/universo-puertas-2026-08-12.tsv` describen la misma fuente dos veces, con estados opuestos: una vez contra dos tablas internas del programa (`NO-ENCONTRADO`), una vez contra el portal real (`EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` / `NO OBTENIDO POR ESTE AGENTE`). Nadie sabe cuál leer. |
| **LA CAUSA RAÍZ** | ADR-69 (proceso: qué recorrer antes de un negativo) y ADR-70 (registro: la tabla consolidada) se sellaron el mismo día, en ramas distintas, sobre el mismo hallazgo raíz, y su propio texto dejó dicho —`gobernanza:922`, verbatim— que reconciliar sus dos artefactos *"queda pendiente nombrado, de mesa"*. Sin regla de precedencia escrita, cada acto que sondea una fuente ya declarada `gap_mapeo_map_b` la añade al lado sin retirar la vieja — SONDA-1 lo hizo 15 veces y lo declaró él mismo, atado además por un perímetro de encargo ("solo filas nuevas") que se lo prohibía hacer distinto. |
| **QUÉ PROPONE** | (a) una regla de precedencia operacionalizable con un comando, no con juicio de lector — §1; (b) el diff exacto, verificado dos veces con `git apply --check` contra el archivo real, que la aplicaría a las 16 filas identificadas en COMMIT 1 — §2; (c) el texto de un ADR candidato que la sellaría — §3. **No ejecuta el diff.** Mesa decide si aplicarlo tal cual, enmendarlo o rechazarlo. |

Depende de `forense/notas/2026-08-13-reconcilia-puertas.md` (COMMIT 1) — ahí vive el mapa campo por campo, las dos preguntas de gobierno y la identificación fila por fila del caso testigo con su evidencia. Este documento no repite esa evidencia; la usa.

---

## 1 · La regla de precedencia

**Texto para sellar:**

> Cuando dos o más filas de `data/universo-puertas-*.tsv` describen la misma fuente —mismo `puerta`, o identidad confirmada por URL exacta / cita explícita entre `url_conocida` de `cola-adquisicion` y `url` de la fila real, nunca por parecido de cadena (criterio de `map-b-crosswalk.md §1`)— rige la de mayor precedencia bajo este orden:
>
> **Regla 1.** Cualquier fila con `clase_origen ≠ gap_mapeo_map_b` gobierna sobre cualquier fila con `clase_origen = gap_mapeo_map_b` para la misma fuente, **sin importar la fecha**.
>
> **Regla 2.** Entre filas empatadas en la Regla 1 (todas `gap_mapeo_map_b`, o todas no-`gap_mapeo_map_b`), gobierna la de `fecha_sondeo` más reciente.

### 1.1 · Es la candidata del encargo, con dos precisiones — declaradas, no en silencio

La candidata original decía: *"manda la de `fecha_sondeo` más reciente cuyo `universo_declarado` cite un portal, no una tabla interna."* Esta propuesta conserva la intención completa y cambia dos cosas, cada una con el defecto concreto que la motiva:

**(i) De "dos filas" a "todas las filas que compartan fuente".** Tres de las 16 fuentes del caso testigo tienen más de dos filas viejas apuntando al mismo instrumento (`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` + `MASS_MOBILIZATION_PROTEST_DATA` + `MASS_MOBILIZATION_PROTEST_DATA_MEXICO`; las dos `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_*`; `DOES_CORRUPTION_INFORMATION_INSPIRE…` + `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009`). Una regla de pares no cubre esos tres sin ambigüedad sobre cuál "de las dos" compara.

**(ii) De "cita un portal" (prosa) a `clase_origen ≠ gap_mapeo_map_b` (columna).** `gap_mapeo_map_b` es, por definición de quien lo creó, un universo que nunca tocó un portal — *"cero red en ninguna de estas filas"* (`map-b-crosswalk.md §1`, línea 34). Usar la columna en vez de leer la prosa de `universo_declarado` es la misma regla, hecha ejecutable con `awk -F'\t' '$2!="gap_mapeo_map_b"'` en vez de un lector humano — y evita un falso negativo real: 4 de las 16 filas nuevas del caso testigo (`MassMobilization_Dataverse_MMdata`, `openICPSR_Microcredit_MexicoPlacement_proj116334`, `OECD_TrustSurveyData`, `Cenfri_MicroinsuranceMexico`) sondearon un portal real y quedaron en `NO OBTENIDO POR ESTE AGENTE EN N INTENTOS` — su `universo_declarado` no siempre repite la URL en la misma frase que "cita" un portal de forma reconocible por patrón; su `clase_origen` sí es, sin ambigüedad, distinto de `gap_mapeo_map_b`.

### 1.2 · Por qué la Regla 1 no puede ser "gana la fecha más reciente" a secas

Medido en COMMIT 1 §4.3: en **14 de los 16** pares del caso testigo, la fila `gap_mapeo_map_b` es la más reciente por `fecha_sondeo` — y aun así es la que hay que retirar. Una regla de solo-fecha habría elegido mal en el 87.5% del caso que la motiva. La Regla 1 existe precisamente para eso: filtra por *qué tan real fue el sondeo* antes de mirar cuándo.

### 1.3 · Verificación — la regla, corrida contra las 16 filas reales

Corrida real contra `data/universo-puertas-2026-08-12.tsv` en esta rama, `pares_16.tsv` con las 16 parejas de COMMIT 1 §4.2 (columna 1 = fuente vieja, columna 2 = puerta real), salida cruda completa, no un conteo solo:

```bash
$ while read -r fuente puerta_real; do
    cls_vieja=$(awk -F'\t' -v p="$fuente" '$1==p{print $2}' data/universo-puertas-2026-08-12.tsv)
    cls_nueva=$(awk -F'\t' -v p="$puerta_real" '$1==p{print $2}' data/universo-puertas-2026-08-12.tsv)
    if [ "$cls_vieja" = "gap_mapeo_map_b" ] && [ "$cls_nueva" != "gap_mapeo_map_b" ]; then
      echo "OK: $puerta_real gobierna sobre $fuente"
    else
      echo "FALLO: $fuente(cls=$cls_vieja) vs $puerta_real(cls=$cls_nueva)"
    fi
  done < pares_16.tsv

OK: GDELT_RawDataFiles gobierna sobre GDELT
OK: UCDP_Downloads_GED gobierna sobre UCDP
OK: INEGI_ENCOAP_2023 gobierna sobre ENCOAP
OK: RNM_CNGMD_2023_catalogo977 gobierna sobre CNGMD
OK: WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453 gobierna sobre WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023
OK: WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049 gobierna sobre LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2
OK: WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039 gobierna sobre IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM
OK: openICPSR_Microcredit_MexicoPlacement_proj116334 gobierna sobre MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP
OK: JPAL_CorruptionInformation_MexicoVoters_2009 gobierna sobre DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE
OK: Zenodo_ElectoralPrecinctLevel_MexicoMunicipal gobierna sobre ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION
OK: Banxico_EncuestaCompetenciasFinancieras gobierna sobre ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION
OK: OECD_TrustSurveyData gobierna sobre OECD
OK: Cenfri_MicroinsuranceMexico gobierna sobre PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND
OK: OSF_InteractingAsEquals_PartisanPolarizacion_Mexico gobierna sobre INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO
OK: MassMobilization_Dataverse_MMdata gobierna sobre MASS_MOBILIZATION_PROTEST_DATA
OK: GESIS_ISSP gobierna sobre ISSP
```

16 de 16 `OK`, 0 `FALLO`. Las 16 resuelven limpio bajo la Regla 1 sola — ninguna necesitó la Regla 2 (no hay, hoy, dos filas no-`gap_mapeo_map_b` compitiendo por la misma fuente). La Regla 2 queda escrita para el primer caso futuro que sí las tenga, no por necesidad de hoy.

---

## 2 · El diff exacto

Aplica la Regla 1 a las 16 filas identificadas en COMMIT 1 §4.2: retira la fila `gap_mapeo_map_b` de cada una, deja intacta la fila real que ya la gobierna. **No toca ninguna otra fila** — ni las 46 `gap_mapeo_map_b` que quedan sin par real todavía (siguen abiertas, correctamente, hasta que algo las sondee), ni los 5 casos de alias de demanda de COMMIT 1 §5.2 (no confirmados por URL/cita, fuera del criterio de identidad de §1).

**Verificado, no descrito:** generado contra el archivo real de esta rama, diferenciado con `diff --unified=1`, y confirmado con `git apply --check` (no aplicado — solo valida que aplicaría limpio):

```diff
diff --git a/data/universo-puertas-2026-08-12.tsv b/data/universo-puertas-2026-08-12.tsv
--- a/data/universo-puertas-2026-08-12.tsv
+++ b/data/universo-puertas-2026-08-12.tsv
@@ -40,12 +40,7 @@
 CCPV	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N31		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-CNGMD	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N28		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N25		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N20		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N25		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N25		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 ENAFIN	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N19		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 ENCIG	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N1,N16,N8		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-ENCOAP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N15,N16,N2,N30		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N29		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N29		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 ENCUP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N25		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
@@ -61,3 +56,2 @@
 FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N19		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-GDELT	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N27		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 GLOBAL_PREFERENCES_SURVEY	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N15		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
@@ -65,11 +59,6 @@
 IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N15		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N28		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 IMSS	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N18		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N3		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-ISSP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N12,N13,N14,N2,N28,N3,N30		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 LAPOP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N30		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N5		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 LATINOBARÓMETRO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N15,N30		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N27		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-MASS_MOBILIZATION_PROTEST_DATA	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N27		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 MASS_MOBILIZATION_PROTEST_DATA_MEXICO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N27		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
@@ -77,6 +66,3 @@
 MICROCREDIT_IMPACTS_COMPARTAMOS_RCT	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N3		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N3		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-OECD	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N30		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 PANEL_DE_COMPRA_DE_HOGARES	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N21		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N21		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 PUB	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N26,N28		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
@@ -91,5 +77,3 @@
 SIN_CANDIDATO_IDENTIFICADO	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N33		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-UCDP	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N17,N27		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 VOTAR_ENTRE_BALAS	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N27,N8		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
-WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023	gap_mapeo_map_b	NO-ENCONTRADO		(sin puerta -- gap de mapeo, ver crosswalk-fuente-puerta-2026-08-13.tsv)						N22,N23,N32		NO-ENCONTRADO	buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)	2026-08-13
 RNM_ENSAFI_2023_ficha992	catalogo_metadatos_inegi	INEGI (en colaboracion con CONDUSEF)	https://www.inegi.org.mx/rnm/index.php/catalog/992	ficha_metadatos_ddi	2023 (levantamiento declarado 25/sep-17/nov/2023 en prosa; tabla "Periodo de ejecucion" da 14/ago/2023-12/abr/2024 para su propia fila "Levantamiento" -- discrepancia interna, ver nota)	viviendas, hogares, persona elegida 18+; tablas TVIVIENDA/THOGAR/TSDEM/TMODULO	nacional y por entidad federativa	si, declarado en la ficha; fuente ya en corpus propio (ensafi2023_bd_csv_zip, manifiesto.yaml) pero sin FD descargable propio -- ver nota	publico, confidencialidad LSNIEG arts. 37/45/47/100; requiere citar fuente			EXISTE-NO-SATISFACE	CORRECCION post-revision (era EXISTE-SATISFACE): la ficha satisface 8 de 10 piezas del universo minimo, pero 2 quedan sin cerrar y una clasificacion de una sola palabra las escondia. FALTA: (1) FD/descriptor propio -- nivel 1 solo parcial, atenuado por el data-dictionary navegable de la ficha pero sin archivo descargable; (2) PDF "Conociendo la base de datos" -- NO-ENCONTRADO, universo recorrido: los 3 tabs de la ficha + export JSON (portal del programa NO revisado para esta pieza especifica, pendiente, no un NO-ENCONTRADO adicional). Resto (muestreo, recoleccion, factores de expansion, cuestionario, politica de acceso, indicadores de calidad, 3 documentos de biblioteca) EXISTE-SATISFACE. Ficha de metadatos DDI de ENSAFI 2023; cuestionario (10 secciones) e indicadores de calidad (1, IC90%) verificados byte a byte; 3 documentos de biblioteca correctos via Materiales de Referencia (Informe operativo/Documento conceptual/Diseno muestral); DEFECTO declarado: 2 citas en prosa de la propia ficha (upc 889463903888/889463903871) resultaron ser documentos de ENIF 2021, no de ENSAFI, no corregido en el catalogo; ver forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md	2026-08-12
```

**Efecto, verificado:** 114 filas de datos → 98 (16 suprimidas, 0 añadidas, 0 filas ajenas tocadas). `gap_mapeo_map_b`: 62 → 46. `puerta` duplicada tras el diff: 0 (`awk -F'\t' 'NR>1{print $1}' | sort | uniq -d` → vacío). `git apply --check` contra el archivo real de esta rama: aplica limpio.

---

## 3 · El ADR propuesto

**Número candidato: ADR-74.** `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md` da 73 únicos, contiguos 1..73, sin huecos, verificado en este mismo commit — 74 es el siguiente número libre **hoy, contra este `origin/main`**. **No se sella aquí ni se escribe en `gobernanza-v1_15.md`** — eso es lo que "propuesto" significa, y es la misma razón por la que ADR-70/71 tuvieron que renumerarse tres veces (`gobernanza:938`): otros actos de este mismo lanzamiento (ADJ-4, BENCHMARK-ENLACE, REAPERTURA-52A-54, ENASIC-SPLIT) corren en paralelo y pueden sellar su propio ADR antes de que éste se funda. **Quien selle esto re-deriva el número contra el `origin/main` real de ese momento (receta de T15), no copia el 74 de este párrafo.**

> **ADR-74 (candidato) · Precedencia entre las filas de `data/universo-puertas-*.tsv` cuando dos describen la misma fuente — cierra el pendiente nombrado de ADR-70.** Decisión de mesa propuesta por ACTO RECONCILIA-PUERTAS, 13/ago/2026, sobre COMMIT 1 (`forense/notas/2026-08-13-reconcilia-puertas.md`) y este COMMIT 2 (`PROPUESTA-reconciliacion-universo-puertas.md`).
>
> **(a) La regla.** Texto verbatim de §1 de la propuesta: Regla 1 (`clase_origen ≠ gap_mapeo_map_b` gana sobre `gap_mapeo_map_b`, sin importar fecha) + Regla 2 (empate → `fecha_sondeo` más reciente), con identidad de fuente confirmada por `puerta` idéntica, URL exacta o cita explícita — nunca por parecido de cadena.
>
> **(b) Aplica el diff de §2**, verificado con `git apply --check` contra `origin/main` al sellar. 16 filas `gap_mapeo_map_b` retiradas, 0 filas añadidas, 0 filas ajenas tocadas. Contador de filas contradictorias del puntero: **16 → 0**, derivado (§6), no tecleado.
>
> **(c) Regla de conducto — enmienda nombrada a ADR-70(c).** ADR-70(c) decía: *"Toda nota de exploración que descubra puerta, capacidad o restricción cierra su acto subiendo la fila a la tabla consolidada o declarando por qué no."* Le faltaba la otra mitad del mismo defecto: **todo acto que añada una fila real para una fuente que ya tenía fila `gap_mapeo_map_b` retira esa fila vieja en el mismo commit, o declara explícitamente por qué no puede** (p. ej. porque su propio encargo tiene perímetro "solo filas nuevas" — en ese caso, el encargo declara la excepción por su nombre, no la deja implícita). Esto es lo que le faltó al encargo de SONDA-1: no falló por descuido, siguió al pie de la letra un perímetro que no traía la excepción. La enmienda es al encargo futuro, no un reproche al acto pasado.
>
> **(d) Cierra el pendiente nombrado.** `gobernanza:922`, última frase de ADR-70: *"reconciliar sus dos artefactos... en una sola tabla queda pendiente nombrado, de mesa."* Esta ADR-74 es ese acto — con la precisión de que no fusiona los dos artefactos en una tabla única (COMMIT 1 §2.3 muestra por qué no tienen el mismo esquema y fusionarlos sería forzar una receta y su bitácora en una sola forma) sino que resuelve la pregunta real detrás del pendiente: cuál fila gobierna cuando compiten.
>
> **(e) Pendiente nombrado nuevo — no resuelto aquí.** COMMIT 1 §3 (Pregunta 2): el título de `UNIVERSO-MINIMO-FUENTE-v1_0.md` dice *"para fuentes INEGI"* (línea 18); 53 de las 62 filas `gap_mapeo_map_b` no lo son. Si el mínimo de búsqueda de ADR-69 rige en espíritu para fuentes no-INEGI, o si esas 53 filas no violan ninguna regla escrita todavía, queda para un acto propio — diseñar qué es un "nivel 3, ficha de catálogo" para un repositorio Zenodo o un catálogo Banco Mundial no es trabajo de esta reconciliación.
>
> **(f) Pendiente nombrado nuevo — duplicados de alias del lado de la demanda.** COMMIT 1 §5.2 agrupa 5 casos por cercanía de nombre; contadas una por una son 6 filas (`COMPARATIVE_STUDY_OF_ELECTORAL_SYSTEMS_MEXICO_2018`, `GLOBAL_PREFERENCES_SURVEY`, `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024`, `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`, `MASS_MOBILIZATION_PROTEST_DATA_MEXICO`, `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009`) que parecen nombrar una fuente que ya tiene puerta real, bajo una identidad de `fuente_canonica` distinta, sin URL ni cita que lo confirme. MAP-B ya lo señaló (`map-b-crosswalk.md §2`) y no lo resolvió. Es trabajo de quien mantenga `data/curacion-registro/aliases-fuentes.tsv` / `data/inventarios/alias-fuentes.yaml`, no de esta regla de precedencia — aplicarla ahí sin evidencia de identidad sería el "parecido de cadena" que la Regla de este ADR prohíbe expresamente.
>
> **(g) Nota adyacente, no ejecutada.** `data/crosswalk-fuente-puerta-2026-08-13.tsv`, columna `clasificacion_a4_de_la_puerta`, fila `ISSP`, quedó `stale` en `NO-ENCONTRADO` cuando `GESIS_ISSP` pasó a `EXISTE-SATISFACE` — ya declarado y no corregido por el propio MAP-B (`map-b-crosswalk.md §3`). Un solo valor, archivo distinto del que este ADR toca; se nombra para que no se pierda, no se incluye en el diff de (b).
>
> **Cascada.** Conteo de ADR vía receta T15, al momento real de sellar — no el 74 de este borrador si otro acto ya lo tomó. Contadores que NO se mueven: ningún contador de Hito D, coeficientes o probabilidades del motor. El único contador que este ADR instituye es el de (b): filas contradictorias del puntero, derivable con `awk` sobre `puerta`+`clase_origen` (receta en §6), sin compuerta nueva de CI — mismo criterio que ADR-72 usó para su propio contador ("instituye un número y ninguna compuerta nueva").

---

## 4 · Falsador y caducidad (Bloque B-bis)

**Métrica**, derivable con dos `awk` (§6): fuentes del puntero con ≥2 filas donde al menos una es `gap_mapeo_map_b` y al menos una no lo es, para la misma fuente confirmada por identidad de §1.

**Falsador declarado.** Si dentro de los próximos tres actos que añadan filas reales a `universo-puertas-*.tsv` sobre una fuente ya `gap_mapeo_map_b`, alguno vuelve a dejar la fila vieja sin retirar y sin declarar por qué no (violando (c) de §3), la Regla de conducto sola no bastó — hace falta instituir un chequeo mecánico (un T-check en `tests/check.py`, o una validación en `tools/curador_registro/`) en vez de una regla que depende de que el siguiente acto la recuerde y la aplique.

**Caducidad.** Si en tres meses el contador de (b) no volvió a moverse de 0 — ninguna fila contradictora nueva apareció — la vigilancia de este ADR se retira como innecesaria: la Regla de conducto sola bastó, y no hace falta instrumentar más que el conteo. Misma regla de señal que gobierna todo lo demás: *"cada sesión produce una medición, o produce nada."*

---

## 5 · Qué NO hace esta propuesta

No fusiona `UNIVERSO-MINIMO-FUENTE-v1_0.md` y `universo-puertas-2026-08-12.tsv` en un solo artefacto — COMMIT 1 §2.3 muestra que no comparten esquema y que fusionarlos sería forzar una receta y su bitácora en una sola forma. No aplica el diff de §2 — queda para el acto que mesa autorice después de sellar. No resuelve la Pregunta 2 (alcance de ADR-69 fuera de INEGI, §3(e)) ni los duplicados de alias de demanda (§3(f)) — ambos quedan nombrados, ninguno adivinado. No toca `production-spec.schema.json` ni `documentacion_fuente` (ADR-70(b)) — artefacto de un contrato distinto, ya declarado fuera de este solape en COMMIT 1 §2.2. No instituye ninguna compuerta de CI nueva — el contador de §3(b)/§6 es derivable por comando, sin bloquear ningún PR (coherente con "Sin gate" del encargo de este acto).

---

## 6 · Receta de verificación (para quien selle, o para quien dude de esta propuesta)

```bash
# Cifras de COMMIT 1, re-derivables:
awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l                              # 114
awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l     # 62

# Las 16 filas que este diff retira, y que cada una tiene una fila real que la gobierna
# bajo la Regla 1 (clase_origen distinto de gap_mapeo_map_b, misma fuente por URL/cita):
# ver tabla completa en forense/notas/2026-08-13-reconcilia-puertas.md §4.2

# Tras aplicar el diff de §2 (verificar en una copia, nunca contra el archivo real sin
# autorización de mesa):
awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l                              # esperado: 98
awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l     # esperado: 46
awk -F'\t' 'NR>1{print $1}' data/universo-puertas-2026-08-12.tsv | sort | uniq -d           # esperado: vacío (0 duplicados)
```
