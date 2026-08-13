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
