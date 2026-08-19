# NOTA · FP10-PRECEDENCIA — ejecución del diff de 16 pares sobre `data/universo-puertas-2026-08-14.tsv`

**Acto:** `ACTO FP10-PRECEDENCIA`, 19/ago/2026, sobre `forense/encargos/2026-08-18-FP10-PRECEDENCIA.md`.
**SHA de arranque:** `35c9c9f` (`origin/main`).

## 1 · Verificación de la precondición (A.8, recontestada, no heredada del encargo)

El encargo (redactado contra `93a4dd9`) declaraba la fase semántica de `BARRIDO-2` **NO SATISFECHA**. Releído hoy contra `origin/main` real:

- **Gate material:** `ADR-103` (`canon/gobernanza-v1_15.md:1940`) — *"el gate cierra 672/672 por primera vez desde `ledger-v5`, muestra adversarial 39/39"*. `canon/estado-programa-v1_10.md:165` confirma la misma cifra. `PR #260` (`gate-durable-v7`) fusionado — visible en `git log` (`6178bf9 Merge pull request #260`).
- **Fase semántica:** `ADR-108` (`gobernanza:2077`) — `ACTO B2-SEMANTICO`, `PR #268` fusionado (`e563e5d Merge pull request #268 from Josanoforo/b2-semantico`) — cascada fuente→payload `R1 ∪ R7`, `INFRAESTRUCTURA-v1_0.md` gana dominios 3-bis/4-bis, `FP-35` ejecutada. `ADR-109` (`gobernanza:2127`) — mismo encargo, `FP-46` ejecutada.
- **Conclusión:** la precondición del `DISPARADOR-B` está satisfecha. Este acto se lanza.

## 2 · ¿Superada o ejecutada?

`PROPUESTA-reconciliacion-universo-puertas.md` §2 declara 16 pares contradictorios sobre `data/universo-puertas-2026-08-12.tsv` (114→98 filas esperado tras el diff). Se releyeron los 16 pares contra el universo vigente, `data/universo-puertas-2026-08-14.tsv` (122 filas de datos antes de este acto, sucesor del `-08-12` citado en la propuesta).

Verificado por comando, **antes** de tocar el archivo: las 16 fuentes listadas en el diff de la propuesta **seguían presentes como fila `gap_mapeo_map_b` sin retirar**, y sus 16 puertas reales correspondientes (que las gobiernan bajo la Regla 1, `ADR-76(e)`) **también existen** en el archivo vigente, con `clase_origen` distinto de `gap_mapeo_map_b`. Es decir: ni `BARRIDO-2` (material ni semántico) ni ningún acto intermedio retiró las filas viejas — el defecto que `ADR-76(e)` dejó nombrado seguía intacto. **No hay superación: se ejecuta el diff.**

```
$ for f in <16 fuentes de la propuesta §2>; do
    awk -F'\t' -v p="$f" '$1==p{print $1"\t"$2}' data/universo-puertas-2026-08-14.tsv
  done
CNGMD  gap_mapeo_map_b
DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE  gap_mapeo_map_b
ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION  gap_mapeo_map_b
ENCOAP  gap_mapeo_map_b
ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION  gap_mapeo_map_b
GDELT  gap_mapeo_map_b
IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM  gap_mapeo_map_b
INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO  gap_mapeo_map_b
ISSP  gap_mapeo_map_b
LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2  gap_mapeo_map_b
MASS_MOBILIZATION_PROTEST_DATA  gap_mapeo_map_b
MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP  gap_mapeo_map_b
OECD  gap_mapeo_map_b
PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND  gap_mapeo_map_b
UCDP  gap_mapeo_map_b
WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023  gap_mapeo_map_b
```

16 de 16 confirmadas: una sola fila `gap_mapeo_map_b`, sin `clase_origen` distinta compitiendo (es decir, todavía sin resolver por la Regla 1). Y las 16 filas reales que las gobiernan (`GDELT_RawDataFiles`, `UCDP_Downloads_GED`, `INEGI_ENCOAP_2023`, `RNM_CNGMD_2023_catalogo977`, `WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453`, `WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049`, `WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039`, `openICPSR_Microcredit_MexicoPlacement_proj116334`, `JPAL_CorruptionInformation_MexicoVoters_2009`, `Zenodo_ElectoralPrecinctLevel_MexicoMunicipal`, `Banxico_EncuestaCompetenciasFinancieras`, `OECD_TrustSurveyData`, `Cenfri_MicroinsuranceMexico`, `OSF_InteractingAsEquals_PartisanPolarizacion_Mexico`, `MassMobilization_Dataverse_MMdata`, `GESIS_ISSP`) existen, cada una con `clase_origen ≠ gap_mapeo_map_b` (`repositorio_academico`, `catalogo_metadatos_inegi`, `organismo_internacional`, `canasta_publica`, `ong_observatorio`, según el caso) — verificado uno por uno, mismo comando.

## 3 · Diff aplicado, comando por comando

```
$ cp data/universo-puertas-2026-08-14.tsv /tmp/.../universo-puertas-antes.tsv
$ awk -F'\t' -v OFS='\t' 'NR==FNR{del[$1]=1; next} !( $1 in del && $2=="gap_mapeo_map_b" )' \
    16-fuentes.txt data/universo-puertas-2026-08-14.tsv > /tmp/.../universo-puertas-despues.tsv
$ diff <(awk -F'\t' '{print $1}' antes.tsv) <(awk -F'\t' '{print $1}' despues.tsv) | grep '^<'
< CNGMD
< DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE
< ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION
< ENCOAP
< ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION
< GDELT
< IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM
< INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO
< ISSP
< LARGE_SCALE_FINANCIAL_EDUCATION_PROGRAM_IMPACT_EVALUATION_2011_2
< MASS_MOBILIZATION_PROTEST_DATA
< MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP
< OECD
< PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND
< UCDP
< WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023
```

Exactamente las 16 filas listadas arriba, ninguna otra tocada.

```
$ awk -F'\t' 'NR>1' antes.tsv | wc -l                                    # 122
$ awk -F'\t' 'NR>1' despues.tsv | wc -l                                  # 106  (122-16)
$ awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' antes.tsv | wc -l           # 61
$ awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' despues.tsv | wc -l         # 45  (61-16)
$ awk -F'\t' 'NR>1{print $1}' despues.tsv | sort | uniq -d               # (vacío -- 0 duplicados de "puerta")
$ cp despues.tsv data/universo-puertas-2026-08-14.tsv
$ git diff --stat data/universo-puertas-2026-08-14.tsv
 data/universo-puertas-2026-08-14.tsv | 16 ----------------
 1 file changed, 16 deletions(-)
```

**Fusión `MassMobilization`.** La propuesta (§1.1(i)) agrupa tres puertas viejas bajo el mismo instrumento — `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`, `MASS_MOBILIZATION_PROTEST_DATA`, `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` — pero el diff verificado de §2 solo retira una: `MASS_MOBILIZATION_PROTEST_DATA` (identidad confirmada por URL/cita contra `MassMobilization_Dataverse_MMdata`). Las otras dos (`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`, `MASS_MOBILIZATION_PROTEST_DATA_MEXICO`) quedan explícitamente fuera del diff y son citadas por la propia propuesta en §3(f) como "duplicados de alias de demanda" — pendiente nombrado, no resuelto por la Regla 1 (sin URL/cita que confirme identidad, sería "parecido de cadena", expresamente prohibido). Verificado: siguen presentes, sin tocar, en `data/universo-puertas-2026-08-14.tsv` tras este acto.

## 4 · `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`

Verificado antes de escribir: `FUSION-PUERTAS` (`FP-12`, encargo `forense/encargos/2026-08-18-FUSION-PUERTAS.md`) sigue `VIVO`, sin rama ni PR en el árbol (`git branch -a`/`git log --all` sin resultado para "fusion-puertas"), fila `FP-12` en el tablero `FIRMADA-CONDICIONAL`, sin ejecutar. `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` no trae marca `SUPERADO POR`. Este acto **no lo toca** — está fuera del perímetro de `FP-10` y de esta nota; la fusión con `FP-12` es tarea de `FUSION-PUERTAS`, acto propio.

## 5 · Verificación (tests)

```
$ python3 tests/check.py --baseline
21 FAIL · 118 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(1 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Sin `--freeze`. `baseline.json` no tocado.

## 6 · Contadores de medición sobre México movidos

**Cero.** Este acto retira 16 filas `gap_mapeo_map_b` (metadatos de gobierno del puntero de puertas: qué fuente ya tiene puerta real vs. cuál sigue siendo un gap de mapeo) — no toca ningún coeficiente, probabilidad, dato de microdato ni cifra del corpus. `13 de 27` (Hito D), `9 de 14` (condicionales), `0 de 15` (coeficientes), `1 de 2` (llaves), `4 de 144`: ninguno se mueve.
