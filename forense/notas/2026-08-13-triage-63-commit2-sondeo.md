# ACTO TRIAGE-63 COMMIT 2 · el sondeo — ejecución

## 0 · ARRANQUE

1. **REPO.** Clon existente en uso: `/home/pc0/Modelado-Mexicano`. Worktree nuevo `/home/pc0/mm-triage-63-sondeo`, rama `triage-63-sondeo` (el worktree `mm-triage-63` de COMMIT 1 quedó atado a una rama ya fusionada/borrada, no reusable). `git worktree add` chocó con el defecto conocido de `.git/config` "Device or resource busy" — el worktree quedó funcional, verificado con `git log -1`/`git status` antes de confiar en él.
2. **SHA.** `origin/main` al arrancar: `1cb6e3e` (merge PR #219), 8 commits por delante de la línea base congelada `3d0d1e5`/ADR-76(f). No es PARO. ADR re-derivado por la receta T15 (`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md`): 78 únicos, contiguo 1..78 — **79 siguiente libre, sin diferencia contra lo que el encargo asumía**.
3. **data/raw.** Ausente (`ls data/raw` → no existe). No es PARO — este acto no descarga microdato, solo sondea reachability de portales.
4. **ENTORNO**, las tres partes: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío (firma CAJA) · `curl -s -o /dev/null -w "%{http_code}" https://www.inegi.org.mx/` → `200` (red viva) · consistente con CAJA con red, como exige el encargo.
5. **Espejo.** No se usó ninguno — toda cifra sale de este clon/worktree, comandos a la vista abajo.

**Gate del encargo, verificado 0/2 al recibirlo, luego 2/2 tras dos actos ajenos.** Ver `forense/encargos/2026-08-13-triage-63-no-probado.md` ADENDA 2 para la cronología completa (PARO declarado a mesa, espera sin auto-adjudicación, resolución vía `ADR-79`/`PR #225`/`ADR-80`). `origin/main` re-fetcheado inmediatamente antes de escribir cualquier columna: `d55ae72` → `c8e9cc0`, sin más movimiento relevante al perímetro de este acto.

## 1 · Orden de sondeo — re-derivación de "las 17 que gatean Hito D"

El encargo entrega ya construida la lista de 17 (agrupada por N-número) y pide re-derivarla contra `data/curacion-registro/necesidad-objeto-modelo.tsv` y reportar si difiere.

Verificado estructuralmente, no de memoria: `necesidad-objeto-modelo.tsv` (33 filas, `N1`-`N33`) tiene `objeto_modelo_origen` en formato `R#.#` y cita `forense/hitoD-preregistro-v2_0.md` en `fuentes_verificacion` **solo para `N21`-`N33`** (`R1.4` a `R10.3`); `N1`-`N15` son coeficientes del censo, `N16`-`N20` son "objetos de regla" (`tramite.*`, `dinero.*`, `civico.*`) sin ficha de Hito D propia (con la excepción parcial de `N17`, que sí cita `hitoD-preregistro` pero cuyo `objeto_modelo_origen` no es `R#.#` — no afecta ninguna fila de las 27, ver abajo).

**Regla aplicada:** una fila de `CANDIDATA-A-SONDEO` "gatea Hito D" si al menos uno de sus `fuentes_que_sirve` cae en `N21`-`N33`. Aplicada a las 27 filas reales (`awk -F'\t' '$11=="CANDIDATA-A-SONDEO"{print $1"\t"$8}'`), reproduce **exacto** el conjunto de 17 que trae el encargo — **sin diferencia**, verificado por cruce 1:1, cero sobrantes, cero faltantes:

| N (rango 21-33) | fila(s) que califican por ese N |
|---|---|
| N21 R1.4 | `HOMESCAN_CONSUMER_PANEL_SERVICES` · `PANEL_DE_COMPRA_DE_HOGARES` |
| N22 R2.1 / N23 R2.2 | `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` |
| N24 R3.4 | `REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES` · `SERIES_SPEI_CODI_BANXICO` |
| N25 R7.1 | `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009` |
| N27 R7.4/R7.5 | `BASE_DEL_OBSERVATORIO_DE_CONFLICTOS_POR_EL_AGUA` · `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` · `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` · `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` · `VOTAR_ENTRE_BALAS` |
| N28 R8.1 | `SICS` |
| N29 R8.2 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` · `FINANZAS` · `REGISTRO_DE_TANDAS_Y_REPUTACION` · `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` |
| N31 R10.1 | `ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER` |

Las 10 restantes (`ITAM_panel_household_finance`, `AHORRO FINANCIERO Y FINANCIAMI`, `BDIF`, `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO`, `ENAFIN`, `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY`, `GLOBAL_PREFERENCES_SURVEY`, `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016`, `IMSS`, `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT`) tienen todos sus `fuentes_que_sirve` en `N1`-`N20` exclusivamente (o vacío, caso `ITAM`) — ninguna toca `N21`-`N33`. Regla ejecutada, no la lista pegada: `mesa firmó SONDEO-COMPLETO (ADR-80(a))`, así que las 10 también se sondean, después de las 17.

## 2 · Mecánica aplicada

GET real (`curl`, nunca `HEAD`/`curl -I`) sobre cada URL candidata. **Sin override primero, con override solo si falló, los dos reportados** — en la práctica, 23 de 26 URLs candidatas resultaron alcanzables sin necesitar `dangerouslyDisableSandbox`; solo se invocó el override para diagnosticar las que fallaron, confirmando en cada caso que el fallo era del servidor/red real, no del sandbox del agente (mismos códigos/errores con y sin override). Diagnóstico de contenido: `grep` de huellas de bloqueo conocidas (Cloudflare "Attention Required"/"Just a moment", Incapsula) y verificación de `<title>`/`<h1>` real contra el nombre esperado de la fuente — ninguna de las 200 resultó ser una página de bloqueo disfrazada.

**Identificación de URL antes de sondear:** para 13 de las 27 filas existía ya una URL o institución citada en tablas del propio repo (`data/mapa-fuentes-externas-consolidado-2026-08-06.tsv`, `data/mapa-ext-{general,civil,oficial,academico}-2026-08-06.tsv`, `data/cola-adquisicion-2026-08-12.tsv`, la nota de COMMIT 1) — usadas en vez de buscar de cero. Para las 14 restantes, `WebSearch` (universo declarado por fila, ver §3-4); 2 de esas 14 no resolvieron a una identidad confirmada (`REGISTRO_DE_TANDAS_Y_REPUTACION`, y `FINANZAS`/`AHORRO FINANCIERO Y FINANCIAMI` con identidad solo parcial — ver abajo).

## 3 · Resultado — las 17 prioritarias (Hito D)

| # | fila | url probada | sin override | con override | quien_puede |
|---|---|---|---|---|---|
| 1 | `BASE_DEL_OBSERVATORIO_DE_CONFLICTOS_POR_EL_AGUA` | omca.imta.gob.mx/omca/acerca_ocam | 200 | no necesario | AGENTE |
| 2 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | laoms.org | 200 | no necesario | AGENTE |
| 3 | `MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` | massmobilization.github.io | 200 | no necesario | AGENTE |
| 4 | `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` | massmobilization.github.io (misma URL que #3) | 200 | no necesario | AGENTE |
| 5 | `VOTAR_ENTRE_BALAS` | votarentrebalas.datacivica.org | 200 | no necesario | AGENTE |
| 6 | `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` | banxico.org.mx/.../competencias-financieras-mi.html | 200 | no necesario | AGENTE |
| 7 | `FINANZAS` | pnif.cnbv.gob.mx (identidad NO confirmada 1:1) | 000 (SSL: cadena incompleta) | 000 idéntico | AGENTE con salvedad |
| 8 | `REGISTRO_DE_TANDAS_Y_REPUTACION` | sin URL propia verificable | N/A | N/A | NO_PROBADO |
| 9 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | tandamas.mx ("Tanda+") | 200 | no necesario | AGENTE (portal; registro NO-ACCESIBLE por fuente previa) |
| 10 | `HOMESCAN_CONSUMER_PANEL_SERVICES` | nielseniq.com/.../homescan | 200 | no necesario | AGENTE (portal; dato NO-ACCESIBLE por fuente previa) |
| 11 | `PANEL_DE_COMPRA_DE_HOGARES` | kantar.com/.../Mexico | 200 | no necesario | AGENTE (portal; dato NO-ACCESIBLE por fuente previa) |
| 12 | `REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES` | ift.org.mx/.../reporte-sfd | 200 | no necesario | AGENTE |
| 13 | `SERIES_SPEI_CODI_BANXICO` | banxico.org.mx/.../sistema-pagos-electronicos-in001.html | 200 | no necesario | AGENTE |
| 14 | `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` | microdata.worldbank.org/catalog/870 | 200 | no necesario | USUARIO_REGISTRO |
| 15 | `EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009` | povertyactionlab.org/evaluation/... | 200 | no necesario | AGENTE |
| 16 | `SICS` | sics.funcionpublica.gob.mx + consultasics.buengobierno.gob.mx | 000 (timeout) | 000 (timeout/TLS anómalo) | NADIE |
| 17 | `ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER` | pragmatics.indiana.edu/.../Encdeserv.html | 200 | no necesario | AGENTE |

**15 de 17 alcanzables (AGENTE/USUARIO_REGISTRO), 1 sin URL identificable (`NO_PROBADO`), 1 técnicamente inalcanzable dos veces (`NADIE`).**

## 4 · Resultado — las 10 restantes (SONDEO-COMPLETO)

| # | fila | url probada | sin override | con override | quien_puede |
|---|---|---|---|---|---|
| 18 | `ITAM_panel_household_finance` | (ya sondeada por VERIFICA-PUERTAS, sin URL propia) | — | — | NO_PROBADO *(sin cambio, no re-sondeada)* |
| 19 | `AHORRO FINANCIERO Y FINANCIAMI` | pnif.cnbv.gob.mx/dnoticia/reporteahorrofinancieroyfinanciamientomarzo2025 | 000 (mismo defecto de certificado que #7) | 000 idéntico | AGENTE con salvedad |
| 20 | `BDIF` | gob.mx/cnbv/.../bases-de-datos-de-inclusion-financiera | 200 | no necesario | AGENTE |
| 21 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | amis.com.mx (candidato, no confirmado) | 000 (timeout) | 000 idéntico | NADIE |
| 22 | `ENAFIN` | inegi.org.mx/rnm/index.php/catalog/1106 | 200 | no necesario | AGENTE |
| 23 | `FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY` | kellogg.northwestern.edu/.../gender-differentiated-digital-credit... | 200 | no necesario | AGENTE (dato NO-ACCESIBLE por fuente previa) |
| 24 | `GLOBAL_PREFERENCES_SURVEY` | gps.econ.uni-bonn.de/downloads | 200 | no necesario | AGENTE |
| 25 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | microdata.worldbank.org/catalog/6667 | 200 | no necesario | USUARIO_REGISTRO |
| 26 | `IMSS` | datos.imss.gob.mx | 503 (Incapsula WAF) | 503 idéntico | NADIE |
| 27 | `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` | openicpsr.org/.../116334 (URL de la fila hermana, no fusionada) | 403 | 403 idéntico (con UA de navegador también) | USUARIO_REGISTRO |

**6 de 9 sondeadas alcanzables, 2 técnicamente inalcanzables (`NADIE`), 1 bloqueada por acceso real no bot (`USUARIO_REGISTRO`); la 10ª (`ITAM`) ya estaba sondeada por un acto previo y no se re-sondeó — fuera del mecanismo de este acto, que sondea URLs nuevas, no re-verifica lo ya hecho.**

## 5 · Hallazgos declarados, no resueltos aquí (fuera de perímetro — no toca `estado_triaje`)

- **`SICS` ya tiene payload real adquirido** (`r8_1_contraloria_social_2019_2025_csv`, `EXISTE-NO-SATISFACE`, `forense/notas/2026-08-08-verif3.md`) — la fila `CANDIDATA-A-SONDEO` de este acto describe el *sistema operativo* de captura a nivel-comité (`sics.funcionpublica.gob.mx`), un objeto distinto del dataset agregado ya en corpus. El fallo de hoy (timeout/TLS) reproduce exacto el de hace 8 días (`2026-08-05-conf17-fetch-corrida-B.md:316`) — falla técnica persistente, no un bloqueo nuevo.
- **`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO` y `MASS_MOBILIZATION_PROTEST_DATA_MEXICO` resuelven a la misma URL** (`massmobilization.github.io`) — mismo objeto bajo dos nombres, ya sospechado por `forense/notas/2026-08-13-triage-63.md` filas 17-18, ahora con evidencia de URL idéntica. No fusionado.
- **`EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009`** resuelve a la página J-PAL de la campaña de información en las elecciones municipales 2009 (Jalisco/Morelos/Tabasco) — mismo tema exacto que `DOES_CORRUPTION_INFORMATION_INSPIRE_THE_FIGHT_OR_QUASH_THE_HOPE` (bucket A, Chong/De La O/Karlan/Wantchekon, *Journal of Politics*). Ambigüedad ya declarada por `forense/notas/2026-08-13-triage-63.md` fila 10, ahora con URL confirmando el tema — sigue sin fusionarse.
- **`GLOBAL_PREFERENCES_SURVEY`**: `mapa-ext-academico-2026-08-06.tsv:12` lo clasificó `NO-ACCESIBLE`/`REQUIERE-DECISIÓN-DE-MESA` hace 8 días; hoy la página de descargas responde 200 real. Posible cambio de terreno (mismo patrón que `VERIFICA-PUERTAS` ya documentó para otros dominios el mismo día) — declarado, no reclasificado.
- **Certificado incompleto en `pnif.cnbv.gob.mx`** (filas `FINANZAS` y `AHORRO FINANCIERO Y FINANCIAMI`): idéntico con y sin override (no es artefacto de sandbox), `-k` confirma contenido real detrás. Defecto del lado del servidor (cadena de certificado sin intermedio), no bloqueo.
- **`IMSS`**: 503 con cabeceras Incapsula reales (`X-Iinfo`, cookies `visid_incap_`/`incap_ses_`) — bloqueo activo de bot-management, no caída de servicio genérica.
- **Identidad no confirmada, declarada como tal:** `FINANZAS` y `AHORRO FINANCIERO Y FINANCIAMI` (candidato CNBV por coincidencia temática/de nombre truncado, no por URL heredada) y `REGISTRO_DE_TANDAS_Y_REPUTACION` (sin URL alguna, "Tanda Ahorro MX" no resuelve por buscador — 2 intentos, universo declarado en la tabla).

## 6 · Cierre

`python3 tests/check.py --baseline`: **20 FAIL · 107 WARN, LÍNEA BASE VERDE** contra `tests/baseline.json` (HEAD congelado `3d0d1e5`), corrido antes y después de escribir — sin cambio. Perímetro tocado: `data/acceso-puertas-2026-08-13.tsv` (columnas de sondeo, 26 filas — `estado_triaje` intacto, verificado con `awk` antes/después, sigue 27 `CANDIDATA-A-SONDEO`), `forense/encargos/2026-08-13-triage-63-no-probado.md` (ADENDA 2 + cierre de Estado), este archivo, `forense/hallazgos.md`. No se tocó `canon/`, no se selló ADR, no se tocó `data/manifiesto.yaml` ni `universo-puertas`.

Contador que este acto mueve: filas de `acceso-puertas` `CANDIDATA-A-SONDEO` con sondeo real (`http_sin_override` ≠ `NO_PROBADO`), 0 → 26 de 27 (la 27ª, `ITAM`, ya lo tenía de VERIFICA-PUERTAS). Ningún contador de Hito D, condicionales o coeficientes del motor se mueve — este acto sondea reachability de portal, no adjudica `EXISTE-SATISFACE`/`NO-ACCESIBLE` de la necesidad ni toca `estado_triaje`.
