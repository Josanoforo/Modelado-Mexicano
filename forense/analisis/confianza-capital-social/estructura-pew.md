# Estructura Pew Global Attitudes Survey (GAS) — olas 2013, 2015, 2017, 2018, 2023, 2024

Informe de ESTRUCTURA (metadatos), no de datos. Extraído con `pyreadstat.read_sav(..., metadataonly=True)` — no se leyó, imprimió ni calculó ningún valor de microdato (sin frecuencias, medias, `value_counts`, `head()`, ni lectura de columnas). Payloads en `/home/pc0/mm-corpus/descargas_mx_espejo/UNIVERSO-2026-09/PEW/`.

**Ola RESERVADA (E.6): PEW Spring 2025 — `pew_gas_spring2025.zip` NO fue abierto** (ni siquiera se listaron sus miembros), y los PDF `pew_gas2025_social_trust_*` no fueron tocados. No aparece en este informe.

---

## 1. Miembros del zip, archivo de datos, filas×columnas (por ola)

| Ola | Miembros del zip | Archivo de datos (.sav) | Filas × columnas |
|---|---|---|---|
| 2013 | Topline PDF, Data Info .txt, **Dataset for web.sav**, Methods PDF, Questionnaire .docx | `Pew Research Global Attitudes Project Spring 2013 Dataset for web.sav` | 37653 × 761 |
| 2015 | Dataset .sav, Data Info .txt, Questionnaire .docx, Topline .pdf | `Pew Research Global Attitudes Spring 2015 Dataset for Web FINAL.sav` | 45435 × 896 |
| 2017 | Data Info .txt, Dataset .sav, Topline .pdf, Questionnaire .docx | `Pew Research Global Attitudes Spring 2017 Dataset WEB FINAL.sav` | 41953 × 875 |
| 2018 | Data Info .txt, Questionnaire .docx, Dataset .sav | `Pew Research Global Attitudes Spring 2018 Dataset WEB FINAL.sav` | 30109 × 565 |
| 2023 | Data Info .txt, Data Dictionary .xlsx, Dataset .sav, Questionnaire .pdf, Topline .pdf | `Pew Research Center Global Attitudes Spring 2023 Dataset CORRECTED.sav` | 27285 × 427 |
| 2024 | Data Dictionary .xlsx, Dataset .csv, **Dataset .sav**, Errata .pdf, Instructions US .pdf, Metadata .xml, Questionnaire .pdf, Syntax .pdf, Topline .pdf, README Data Info .pdf | `Pew Research Center Global Attitudes Spring 2024 Dataset.sav` | 41503 × 653 |

---

## 2. País y diseño (por ola)

| Ola | Var país | Código México | ¿México presente? | Ponderador | Estrato (Mex) | PSU/cluster (Mex) |
|---|---|---|---|---|---|---|
| 2013 | `COUNTRY` | 25 = "Mexico" | Sí | `WEIGHT` | — (no hay `STRATUM_MEX`/`PSU_MEX`) | — |
| 2015 | `COUNTRY` | 21 = "Mexico" | Sí | `WEIGHT` | `STRATUM_MEX` (circunscripción×urbano/rural×partido ganador 2012, 30 categorías) | `PSU` genérico existe pero sin etiquetas de valor (vacío) |
| 2017 | `Country` | 20 = "Mexico" | Sí | `weight` | `STRATUM_MEX` (15 cat.: circunscripción×urban/suburban/rural) | `PSU_MEX` (existe, sin etiquetas de valor — códigos numéricos opacos) |
| 2018 | `COUNTRY` | 15 = "Mexico" | Sí | `weight` | `STRATUM_MEX` (5 "Electoral Region") | `PSU_MEX` (existe, sin etiquetas) |
| 2023 | `country` | 24 = "Mexico" | Sí | `weight` | `region_mexico` (5 circunscripciones) — no hay `STRATUM_MEX`/`PSU_MEX` explícito | — |
| 2024 | `country` | 35 = "Mexico" | Sí | `weight` | `region_mexico` (5 circunscripciones) — no hay `STRATUM_MEX`/`PSU_MEX` explícito | — |

Rareza de diseño: `STRATUM_MEX`/`PSU_MEX` (variables de diseño complejo por país, con `PSU_MEX` opaco/sin etiquetas) solo existen en 2015/2017/2018. En 2013 no hay ninguna variable de diseño específica de país. En 2023/2024 el único remanente de "diseño" documentado es `region_mexico` (5 circunscripciones) — no hay estrato/PSU declarados para México en esos años; solo queda el ponderador `weight`.

---

## 3. Segmentación en México

| Variable | 2013 | 2015 | 2017 | 2018 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Sexo/género | `Q164` ("Gender") | `Q145` ("Gender (RECORD BY OBSERVATION)") | `sex` | `sex` | `sex` | `gender` (Q108) |
| Edad | ausente como var. continua directa (no se halló `age`/`AGE`) | ausente (no se halló `age`/`AGE`) | `age` | `age` | `age` | `age` (Q109) + `d_age_mexico` (rango 18-29/30-39/40-49/50+, solo si age=98/99) |
| Escolaridad Mex | no hay var. `*_mexico` de educación | no hay | `d_educ_mexico_2017` (12 niveles, en español) | `d_educ_mexico_2017` (12 niveles, en inglés) | `d_educ_mexico` (12 niveles) | `d_educ_mexico` (12 niveles) |
| Ingreso Mex | no hay | no hay | `d_income_mexico` (14 tramos en salarios mínimos) + `d_income2_mexico` (binaria vs. mediana) | `d_income_mexico` (11 tramos) + `d_income2_mexico` | `d_income_mexico` (9 tramos en pesos) + `d_income2_mexico` | `d_income_mexico` (9 tramos en pesos) + `d_income2_mexico` |
| Región Mex | no hay | no hay | no aparece `region_mexico` (solo `STRATUM_MEX`) | no aparece `region_mexico` (solo `STRATUM_MEX`) | `region_mexico` (5 circunscripciones) | `region_mexico` (5 circunscripciones) |
| Urbano/rural | no aparece variable específica de México | `Q165BURBAN`/`Q165BRURAL` (genéricas, no verificado alcance México) | no hay var. propia de México (implícito en `STRATUM_MEX`) | no hay propia | `urbanicity` (genérica, no específica de México) | `urbanicity` (genérica) |

Rareza: la escala de tramos de ingreso en pesos cambia de definición entre olas (2017: salarios mínimos; 2018: salarios mínimos con otro corte; 2023/2024: tramos directos en pesos) — **no son comparables entre sí sin homologar**, y el ítem de "mediana del país" (`d_income2_mexico`) cambia el valor de la mediana citada en cada ola (4,380 en 2017; 3,600 en 2018; 4,050/5,400 en 2023/2024 respectivamente — únicamente se cita el texto de la etiqueta, no un valor de microdato).

---

## 4. Reactivos candidatos (tabla)

| Variable(s) por ola | Etiqueta (texto de pregunta) | Etiquetas de valor completas (incl. DK/Refused) | Olas con el MISMO texto |
|---|---|---|---|
| `Q178`(13) / `Q152`(15) / `religion_import`(17,18,23,24) | "How important is religion in your life – very important, somewhat important, not too important, or not at all important?" | 1 Very important / 2 Somewhat important / 3 Not too important / 4 Not at all important / 8 DK / 9 Refused | **6 olas** (2013,2015,2017,2018,2023,2024) — texto virtualmente idéntico (variantes menores de puntuación/"all"↔"at all") |
| `Q176`(13) / `Q151`(15) | "People practice their religion in different ways. Outside of attending religious services, do you pray several times a day, once a day, a few times a week, once a week or less, or never?" | 1 Several times a day…5 Never / 8 DK / 9 Refused | 2013, 2015 (texto idéntico) |
| `pray_several`(17,18,23) | "Aside from religious services, do you pray ___?" / "How often do you pray in normal days aside from religious services on special days?" | 1 Several times a day…7 Never / 98 DK / 99 Refused (7 categorías, escala más fina que 2013/2015) | 2017, 2018, 2023 (mismo esqueleto; 2017 fraseo ligeramente distinto a 18/23 pero mismas categorías de valor) |
| `pray_freq`(24) | "Outside of attending religious services, do you pray several times a day, once a day, a few times a week, once a week, a few times a month, less often than that, OR never?" | igual estructura de 7 niveles pero "less often than that" en vez de "seldom" | 2024 (texto propio, no idéntico a 2017/18/23) |
| `Q179`(13) | "Aside from weddings and funerals how often do you attend religious services... more than once a week, once a week, once or twice a month, a few times a year, seldom, or never?" | 1..6 + 8 DK / 9 Refused | Solo 2013 — **asistencia a servicios religiosos NO aparece como reactivo propio en 2015/2017/2018/2023/2024** (no se halló variable equivalente en la búsqueda de metadatos) |
| `d_relig_mexico` (17,18) | "What is your current religion, if any?" (lista específica México: Católico, Protestante/Evangélico, Testigo de Jehová, Mormón, Judío, Tradicional maya/indígena, Ateo, Agnóstico, Otro, Ninguno, Solo cristiano) | 1..11 + 98 DK + 99 Refused | 2017, 2018 (texto idéntico). **No se halló `d_relig_mexico` en 2013, 2015, 2023 ni 2024** en la búsqueda de metadatos — rareza a confirmar en el Data Dictionary si se requiere certeza |
| creencia en Dios necesaria para ser moral | — | — | **No se encontró ningún reactivo con ese patrón textual en ninguna ola** (búsqueda por "necessary to believe in God" / "believe in God to be moral" sin resultados) |
| `trust_gov` (17,24) | "How much do you trust the national government to do what is right for (survey country) — a lot, somewhat/some, not much/not too much, or not at all?" | 1 A lot / 2 Somewhat(17)-Some(24) / 3 Not much(17)-Not too much(24) / 4 Not at all / 8 DK / 9 Refused | 2017, 2024 — texto muy cercano, no idéntico letra por letra (variante "somewhat"→"some") |
| confianza en instituciones (bancos/medios/cortes/policía) | — | — | **No se encontró un bloque genérico de confianza institucional** en la búsqueda de metadatos (patrones probados: "confidence in", "trust in" + cortes/policía/bancos/medios) — puede existir bajo otros nombres no capturados por el patrón; requiere revisión del diccionario completo si se necesita certeza |
| `trustpeople` (17) | "Generally speaking, would you say that most people can be trusted or that you can't be too careful in dealing with people?" | 1 Most people can be trusted / 2 You can't be too careful / 3 Other/Both/Neither (volunteered) / 8 DK / 9 Refused | **Solo 2017** — confianza interpersonal clásica no aparece en las otras 5 olas |
| `Q90`(13) / `Q11`(15) / `satisfied_democracy`(17,18,23,24) | "How satisfied are you with the way democracy is working in our country/(survey country) – very satisfied, somewhat satisfied, not too satisfied or not at all satisfied?" | 1 Very satisfied…4 Not at all satisfied / 8 DK / 9 Refused | **6 olas** (2013,2015,2017,2018,2023,2024) — texto prácticamente idéntico salvo "our country"→"(survey country)" desde 2023 |
| `polsys_junta` (17,23,24) | "…would it be a very good, somewhat good, somewhat bad or very bad way of governing this country? … the/The military rules the country" | 1 Very good…4 Very bad / 8 DK / 9 Refused | 2017, 2023, 2024 (mismo ítem de batería de sistemas políticos) |
| `polsys_autocracy` (17,23,24) | "…a system in which a strong leader can make decisions without interference from parliament or the courts" | igual escala 1-4 + DK/Refused | 2017, 2023, 2024 |
| `polsys_technocracy` (17,23,24) | "…experts, not elected officials, make decisions according to what they think is best for the country" | igual escala | 2017, 2023, 2024 |
| `Q84D` (13) | "Do you personally believe that homosexuality is morally acceptable, morally unacceptable, or is it not a moral issue?" | 1 Morally acceptable / 2 Morally unacceptable / 3 Not a moral issue / 4 Depends on situation (volunteered) / 8 DK / 9 Refused | **Solo 2013** — tolerancia a homosexualidad (marco de aceptación moral) no reaparece con este texto en olas posteriores |
| `civic_speech`/`civic_online`/`civic_volunteer` (18) | batería "I am going to list some different political and social actions…have you done this…" (asistir a evento de campaña, publicar opinión política online, voluntariado político/caritativo/religioso) | escala Sí/No (no capturada en detalle, ver Data Dictionary) | **Solo 2018** — batería de participación cívica explícita no se halló en 2013/2015/2017/2023/2024 con ese patrón textual |

---

## 5. Matriz reactivo × ola

| Reactivo | 2013 | 2015 | 2017 | 2018 | 2023 | 2024 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Importancia de la religión | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (texto idéntico las 6) |
| Frecuencia de oración (escala fina 7 niveles) | texto distinto (5 niveles) | texto distinto (5 niveles) | ✓ | ✓ | ✓ | texto propio (7 niveles, redacción distinta) |
| Asistencia a servicios religiosos | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Afiliación religiosa México (`d_relig_mexico`) | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Creencia en Dios necesaria para ser moral | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Confianza en gobierno nacional (`trust_gov`) | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ |
| Confianza en instituciones (bancos/medios/policía/cortes) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Confianza interpersonal ("most people can be trusted") | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Satisfacción con la democracia | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (texto idéntico las 6) |
| Apoyo a gobierno militar (`polsys_junta`) | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ |
| Apoyo a líder fuerte sin control (`polsys_autocracy`) | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ |
| Apoyo a gobierno de expertos (`polsys_technocracy`) | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ |
| Tolerancia a homosexualidad (aceptación moral) | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Participación cívica (batería explícita) | ✗ | ✗ | parcial (1 ítem `participation_politicalparty`) | ✓ (batería completa) | ✗ | ✗ |

✓ = presente; ✗ = no se halló variable equivalente en la búsqueda de metadatos de esta ola.
