# PROPUESTA · 15 filas del sondeo-27 (#228) a `data/cola-adquisicion-2026-08-12.tsv`
### v0.1 · 14/ago/2026 · ACTO SANEA-MAPEO, COMMIT 2 · propuesta sin sello; mesa aprueba fijando `palanca` y `destraba_condicional_faltante` para cada fila, o las enmienda

| | |
|---|---|
| **DE DÓNDE SALE** | `forense/notas/2026-08-14-sanea-mapeo.md §1.3/§2.2` — de las 27 filas `CANDIDATA-A-SONDEO` de `data/acceso-puertas-2026-08-13.tsv` (TRIAGE-63/#228), 15 tienen `quien_puede ∈ {AGENTE, USUARIO_REGISTRO}` **sin** que una fuente previa ya haya declarado el dato (no solo el portal) como propietario/bloqueado. Esas 15 son el subconjunto donde el veredicto del sondeo habilita adquisición, no solo alcanzabilidad de portal. |
| **QUÉ NO HACE** | No escribe estas filas en `data/cola-adquisicion-2026-08-12.tsv`. No asigna `palanca` (prioridad de lote) ni completa `destraba_sin_ruta`/`destraba_condicional_faltante`/`celda_piloto_FIN` — esas cuatro columnas requieren juicio de mesa sobre qué destraba qué condicional del motor, fuera del perímetro de un acto de saneamiento de mapeo. Mismo patrón que `PROPUESTA-reconciliacion-universo-puertas.md`: el artefacto queda listo para que quien selle solo tenga que decidir, no que re-derive la evidencia. |

## La tabla — evidencia, no juicio de prioridad

| fuente_canonica | n_necesidades_servidas | quien_puede (sondeo-27, #228) | url_conocida |
|---|---|---|---|
| `AHORRO FINANCIERO Y FINANCIAMI` | 1 | `AGENTE (con salvedad de certificado -- ver receta)` | https://pnif.cnbv.gob.mx/dnoticia/reporteahorrofinancieroyfinanciamientomarzo2025 (candidato por coincidencia de nombre truncado -- ver `cabecera_diagnostica`) |
| `BASE_DEL_OBSERVATORIO_DE_CONFLICTOS_POR_EL_AGUA` | 1 | `AGENTE` | https://omca.imta.gob.mx/omca/acerca_ocam |
| `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | 1 | `AGENTE` | https://laoms.org/ |
| `BDIF` | 1 | `AGENTE` | https://www.gob.mx/cnbv/acciones-y-programas/bases-de-datos-de-inclusion-financiera |
| `ENAFIN` | 1 | `AGENTE` | https://www.inegi.org.mx/rnm/index.php/catalog/1106 |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` | 1 | `AGENTE` | https://www.banxico.org.mx/publicaciones-y-prensa/encuesta-de-competencias-financieras-de-la-poblaci/microdatos/competencias-financieras-mi.html |
| `ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER` | 2 | `AGENTE` | https://pragmatics.indiana.edu/textbook/corpus/Encdeserv.html |
| `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009` | 1 | `AGENTE` | https://www.povertyactionlab.org/evaluation/information-dissemination-campaign-and-voters-behavior-2009-municipal-elections-mexico |
| `FINANZAS` | 5 | `AGENTE (con salvedad de certificado -- ver receta)` | https://pnif.cnbv.gob.mx/ (candidato más plausible por tema -- CNBV Portal Nacional de Inclusión Financiera; identidad NO confirmada 1:1 con el nombre genérico "FINANZAS") |
| `GLOBAL_PREFERENCES_SURVEY` | 1 | `AGENTE` | https://gps.econ.uni-bonn.de/downloads |
| `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | 1 | `USUARIO_REGISTRO` | https://microdata.worldbank.org/catalog/6667 |
| `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` | 3 | `USUARIO_REGISTRO` | https://microdata.worldbank.org/catalog/870/data-dictionary/F2 |
| `REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES` | 1 | `AGENTE` | https://www.ift.org.mx/usuarios-y-audiencias/reporte-sobre-el-uso-y-la-confianza-de-los-servicios-financieros-digitales-sfd |
| `SERIES_SPEI_CODI_BANXICO` | 2 | `AGENTE` | https://www.banxico.org.mx/servicios/sistema-pagos-electronicos-in001.html |
| `VOTAR_ENTRE_BALAS` | 2 | `AGENTE` | https://votarentrebalas.datacivica.org/ |

**`n_necesidades_servidas`** contado fresco contra `data/curacion-registro/relaciones.tsv` en esta sesión (número de `necesidad_id` únicos que la fuente sirve), mismo criterio de columna que usa `data/cola-adquisicion-2026-08-12.tsv`. **`quien_puede`/`url_conocida`** copiados verbatim de `data/acceso-puertas-2026-08-13.tsv` (columnas `quien_puede`/`url`), sin re-sondear — evidencia de `#228`, no de este acto.

**Dos casos con identidad no confirmada 1:1, declarados en la propia fila del sondeo y heredados aquí sin resolver:** `AHORRO FINANCIERO Y FINANCIAMI` y `FINANZAS` apuntan ambas a dominios `pnif.cnbv.gob.mx`, candidatos por coincidencia temática/de nombre truncado, no por URL exacta confirmada contra el nombre de la fuente en `relaciones.tsv`. Quien selle esta propuesta puede requerir una confirmación de identidad adicional antes de asignar palanca a esas dos filas específicamente.

**Excluidas de esta propuesta, y por qué (no lo decide este documento, ya está decidido por el propio veredicto del sondeo):** las 4 filas `NO-ACCESIBLE` (`HOMESCAN_CONSUMER_PANEL_SERVICES`, `PANEL_DE_COMPRA_DE_HOGARES`, `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES`, `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY`) — el dato ya está declarado propietario/bloqueado por una fuente previa citada en el propio sondeo, proponerlas a la cola de adquisición sería proponer algo que el programa ya sabe que no puede adquirir. Las 3 `NO OBTENIDO EN 2 INTENTOS` (`DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO`, `IMSS`, `SICS`) — inalcanzables dos veces, técnicamente. Las 2 `NO-ENCONTRADO`/`NO_PROBADO` (`ITAM_panel_household_finance`, `REGISTRO_DE_TANDAS_Y_REPUTACION`) — sin URL identificable, nada que poner en cola todavía.

---

**Verificación de cierre:** `python3 tests/check.py --baseline` — ver `forense/notas/2026-08-14-sanea-mapeo.md §2.3`. Este documento no toca `data/cola-adquisicion-2026-08-12.tsv`.
