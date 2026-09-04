# MAESTRA37-A2 · REVISA-COLA-A-DETALLE — informe por fila

`ADR-331` (candidato original `ADR-330`, renumerado tras el merge de `origin/main`/`PR #523` que fusionó primero `ADR-328`/`ADR-329` de `MAESTRA37-N8` y dejó `ADR-330` a `MAESTRA37-N9`, misma rama) · `FP-288` recibo · `FP-289` (mesa firma la clasificación final, vence 2026-09-11).

COMPUERTA verificada: `MAESTRA37-N8 · CONSOLIDA-DECISIONES` corrió (NUBE, 4/sep/2026), quedó `## CONSUMIDO` y se fusionó a `main` vía `PR #523` (merge `4b508ad`, cierre `d96bf44`). Su P5 reclasificó cinco filas comerciales a `NO-ADQUIRIDA-POR-COSTO` y `WB6667` a `PENDIENTE-DE-MESA`.

## Universo (COMMIT-1)

`data/curacion-registro/cola-adquisicion-registro.tsv`: 112 filas totales; 83 `OBTENIDO` + 1 `CERRADA-PREEXISTENTE` = 84 cerradas; **universo de este acto = 112 − 84 = 28 filas** no `OBTENIDO`/`CERRADA` (comando: `awk -F'\t' 'NR>1 && $5!="OBTENIDO" && $5!~/^CERRADA/'`, corrido 4/sep/2026). El `§A.8` del encargo anticipaba 29 (asumiendo que N8 movía 2 filas a `PENDIENTE-DE-MESA`); N8 movió **una** (`WB6667`; `ICPSR 35024` quedó ambigüedad documentada sin degradar su estado, ya `OBTENIDO`) — de ahí la diferencia de 1.

**Nota metodológica sobre A.5 (sondeo de alcanzabilidad).** Las 28 filas ya traen, en su columna `nota`, sondas de red de ≤3 días (`ACTO MAESTRA33-A3`, `MAESTRA34-L1/L6`, `MAESTRA35-L3/L6/A1`, `MAESTRA36-A2`, todas 2026-09-01/02/03), cada una con salida cruda (código HTTP, tamaño en bytes, comando exacto) y, en la mayoría, las cuatro rutas de A.5 ya recorridas. Repetir esas sondas hoy sin información nueva no produciría una señal distinta (mismo criterio ya aplicado por esas caminatas a sí mismas). Este informe **sintetiza y clasifica** esa evidencia ya en disco -- con fecha, comando y bytes citados verbatim -- en vez de re-sondear lo mismo; donde la evidencia existente NO cubre una ruta (declarado `SIN-FETCH` o similar), este acto lo dice explícitamente en vez de inventar un resultado.

Tabla con la pregunta (regla/necesidad) que cada fila responde, derivada de `relaciones.tsv`/`necesidad-objeto-modelo.tsv`:

| # | fila_origen | fuente_canonica | estado | pregunta que responde (regla/necesidad) |
|---|---|---|---|---|
| 1 | `:6` | IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016 (WB6667) | PENDIENTE-DE-MESA | `relaciones.tsv`: sin cita directa por este nombre; el objeto es el microdato WB6667 ya mapeado en `ids_manifiesto` (documentación/DDI). Ninguna fila de `relaciones.tsv` cita `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` — se dice, no se inventa. |
| 2 | `:20` | SE | PENDIENTE | Ninguna cita en `relaciones.tsv`/`necesidad-objeto-modelo.tsv` bajo este nombre exacto (colisión de token con el pronombre "se", ya diagnosticada por `TRIAGE-63`). |
| 3 | `:21` | CANAL_DE_ADQUISICION_REFERIDOS_FINTECH | PENDIENTE | `relaciones.tsv` → `N19` (`NEGATIVA`, `NO-ENCONTRADO`) → `necesidad-objeto-modelo.tsv` `N19` → `dinero.credito.scoring_alternativo`. |
| 4 | `:22` | DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO | NO-ACCESIBLE | `relaciones.tsv` → `N20` (`NEGATIVA`, `NO-ENCONTRADO`) → `N20` → `civico.denuncia.con_seguro`. |
| 5 | `:28` | BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO (LAOMS) | NO-OBTENIDO(31 int.) | `relaciones.tsv` → `N27` (`CANDIDATA`) → `N27` → `R7.5`. |
| 6 | `:35` | HOMESCAN_CONSUMER_PANEL_SERVICES | NO-ADQUIRIDA-POR-COSTO | `relaciones.tsv` → `N21` (`NO_ACCESIBLE`) → `N21` → `R1.4`. |
| 7 | `:37` | OECD | NO-ACCESIBLE | `relaciones.tsv` → `N30` (`CANDIDATA`, `NO_DETERMINADO`) → `N30` → `R8.3`. |
| 8 | `:38` | PANEL_DE_COMPRA_DE_HOGARES (Kantar) | NO-ADQUIRIDA-POR-COSTO | `relaciones.tsv` → `N21` (`NO_ACCESIBLE`) → `N21` → `R1.4` (misma pregunta que la fila 6: dos proveedores comerciales candidatos al mismo objeto). |
| 9 | `:39` | PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND | NO-OBTENIDO(1 int.) | `relaciones.tsv` → `N21` (`CANDIDATA`, `INDEXADO-NO-DESCARGADO`) → `N21` → `R1.4` (tercer candidato a la misma pregunta que 6/8, vía académica en vez de comercial). |
| 10 | `:40` | REGISTRO_DE_TANDAS_Y_REPUTACION | NO-ADQUIRIDA-POR-COSTO | `relaciones.tsv` → `N29` (`NO_ACCESIBLE`) → `N29` → `R8.2`. |
| 11 | `:41` | REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES | NO-ADQUIRIDA-POR-COSTO | `relaciones.tsv` → `N29` (`NO_ACCESIBLE`) → `N29` → `R8.2` (misma pregunta que 10: familia Tanda+). |
| 12 | `:50` | ENAFIN | NO-ACCESIBLE | Ninguna cita en `relaciones.tsv`/`necesidad-objeto-modelo.tsv` bajo `ENAFIN`. |
| 13 | `:51` | PI | PENDIENTE | Ninguna cita — identidad del código de 2 letras irresoluble sin mesa. |
| 14 | `:58` | EARTHQUAKE_TRUST_LAPOP_2017 | PENDIENTE | Ninguna cita bajo este nombre; el corpus LAPOP amplio (fila 52, ya `OBTENIDO`) no tiene un módulo distinto confirmado. |
| 15 | `:59` | IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA | PENDIENTE | Ninguna cita en `relaciones.tsv`/`necesidad-objeto-modelo.tsv`. |
| 16 | `:61` | MERCER_GPTW_CLIMA_DESEMPENO | NO-ADQUIRIDA-POR-COSTO | Ninguna cita directa localizada. |
| 17 | `:63` | EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 | OBTENIDO-PARCIAL | Rótulo real es EXT-OF-05 (`data/cola-ext-oficial-2026-08-06.tsv:4`), ya corregido en la nota de la fila; destino `R3.1`/`R3.2` (declarado por `MAESTRA37-N3`). |
| 18 | `:70` | EXT_OF_11_REUNE_REDECO | NO-OBTENIDO(1 int.) | Ninguna cita directa en `relaciones.tsv`; objeto administrativo CONDUSEF (S9 del mapa `cola-ext-oficial`). |
| 19 | `:76` | ENVIPE_EXTRACCION_TEXTO_REACTIVO | PENDIENTE | `forense/notas/2026-09-01-mapeo-fp190.md#CIV-08` → `FP-190` `CIV-08` (inseguridad percibida en la calle). |
| 20 | `:78` | BANXICO_ENCUESTA_COMPETENCIAS_FINANCIERAS_EXTRACCION_TEXTO | PENDIENTE | `forense/notas/2026-09-01-mapeo-fp190.md#DIN-07` → `FP-190` `DIN-07` θ (presupuesto en el hogar). |
| 21 | `:79` | DIN-11_CONOCIMIENTO_CUENTAS_SIN_COMISION_SIN_CANDIDATA | PENDIENTE | `forense/notas/2026-09-01-mapeo-fp190.md#DIN-11` → `FP-190` `DIN-11` (conocimiento de cuentas sin comisión). |
| 22 | `:80` | SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA | PENDIENTE | `forense/notas/2026-09-01-mapeo-fp190.md#SFT-06` → `FP-190` `SFT-06` (acuerdo entre hermanos para el cuidado). |
| 23 | `:81` | SICEE | NO-OBTENIDO(1 int.) | `relaciones.tsv` → `N25` (`CANDIDATA`, fuente cívica concurrente) y `N26` (`CANDIDATA`, lado electoral de `R7.3`) → `necesidad-objeto-modelo.tsv` `N25`→`R7.1`, `N26`→`R7.3`. |
| 24 | `NUEVA-L6` | TEPJF_ELECCIONES_CONCURRENTES_1991_2018 | NO-OBTENIDO(1 int.) | Sin cita en `relaciones.tsv`; benchmark nombrado por la firma DC1 (`ACTO MAESTRA34-L6`). |
| 25 | `NUEVA-L3` | IEEPCO_OAXACA_SERIE_MUNICIPAL | NO-OBTENIDO(6 int.) | Sin cita en `relaciones.tsv`; serie municipal para el mapa L3 de concejales/ayuntamientos por estado. |
| 26 | `NUEVA-L3` | IETAM_TAMAULIPAS_SERIE_MUNICIPAL | NO-OBTENIDO(5 int.) | Igual que 25: serie municipal, mapa L3. |
| 27 | `NUEVA-L6` | INEGI_CNGF | NO-ACCESIBLE-DESDE-LA-CAJA | Sin cita en `relaciones.tsv` por nombre; candidato a `tramite.gobierno_digital.coercitivo_*` (documentado por la firma c1 de mesa, `MAESTRA35-L6`) — unidad de análisis institucional, no satisface por diseño. |
| 28 | encargo N3 | PDN_SESNA_S1_S2_S3_S6 | OBTENIDO-PARCIAL | `R3.1`/`R3.2` (mismo destino que EXT-OF-05, fila 17 — objeto distinto hasta que mesa decida fusión, `FP-265`). |

## Informe por fila (COMMIT-2)

Formato por fila: **(a)** rutas/A.5 (síntesis de lo ya sondeado, con fecha) · **(b)** hermanas (criterio A.7) · **(c)** qué trae / qué falta contra la pregunta · **(d)** recomendación.

---

### 1 · IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016 (WB6667) — `PENDIENTE-DE-MESA`
**(a)** `EXIGE-CREDENCIAL` confirmado 2 veces (`ADQ-15` 2026-08-18, `LOTE-UBUNTU-ADQ-1` 2026-08-19): el microdato `.dta` está tras registro; la documentación/DDI (24 payloads) ya está en el corpus.
**(b)** Sin hermana conocida — es un microdato específico del Banco Mundial (World Bank Microdata Library), sin espejo declarado en `aliases-fuentes.tsv`.
**(c)** Trae: documentación completa del instrumento. Falta: el `.dta` con los microdatos, bloqueado por registro (no por red).
**(d) MESA-DECIDE.** Opción (a): mesa crea cuenta gratuita en el World Bank Microdata Library y baja el `.dta` — costo: ~10 min de registro institucional, sin pago. Opción (b): no perseguir, quedarse con la documentación ya obtenida — costo: la evaluación de impacto medible no se puede correr sin el microdato.

### 2 · SE — `PENDIENTE`
**(a)** Sin `url_conocida`, sin nombre de instrumento, sin host — no hay ruta (i)-(iv) que abrir (confirmado `TRIAGE-63` + `MAESTRA33-A3`, 2026-09-01).
**(b)** Sin hermana — no hay identidad de fuente que buscar.
**(c)** No trae nada bajable; falta identidad completa del instrumento.
**(d) NO-BAJAR-PORQUE** el código "SE" es una colisión de token (pronombre "se") sin URL, sin nombre de estudio ni hermana — universo agotado por vía semántica, términos "SE" contra `manifiesto.yaml`, 2026-09-01.

### 3 · CANAL_DE_ADQUISICION_REFERIDOS_FINTECH — `PENDIENTE`
**(a)** Búsqueda web dirigida (`"canal de adquisición" referidos fintech México dataset`), 2026-09-01: sin encuesta/dataset público nombrado; universo = literatura de marketing genérica, sin host.
**(b)** Sin hermana.
**(c)** No trae nada; falta identidad de instrumento con URL propia.
**(d) NO-BAJAR-PORQUE** universo (búsqueda web general), términos (citados arriba) y fecha (2026-09-01) ya declarados sin candidato — no hay ruta que un `/adquiere` pueda abrir.

### 4 · DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO — `NO-ACCESIBLE`
**(a)** `gob.mx/cnsf` → 200, 1878 B (stub sin datos), 2026-09-01. Ninguna estadística agregada pública de CNSF/AMIS cruza denuncia con tenencia de seguro.
**(b)** Sin hermana — es un cruce administrativo (denuncia × seguro) que solo aseguradora/Ministerio Público podrían enlazar.
**(c)** No trae nada; falta el cruce mismo, que requeriría convenio inter-institucional.
**(d) NO-BAJAR-PORQUE** barrera institucional (requiere convenio entre aseguradora y Ministerio Público), no técnica — ningún curl ni receta de navegador la cambia.

### 5 · BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO (LAOMS) — `NO-OBTENIDO-POR-ESTE-AGENTE(31 intentos)`
**(a)** 31 intentos acumulados; el más reciente (`/adquiere` 2026-09-02) probó las 4 rutas de A.5 con salida cruda completa: (i) URL directa `laoms.org` → 200, HTML real, 65 322 B; (ii) API REST de WordPress → sin tipo de contenido "dataset", categoría "eventos de protesta" son documentos sobre protesta, no registro codificado; (iii) no aplica (biblioteca de medios sin archivos de dato); (iv) Harvard Dataverse `q=LAOMS` → `total_count=0`.
**(b)** Espejo académico sondeado (Harvard Dataverse) sin resultado; Crowd Counting Consortium es de EE.UU., no es la misma fuente (criterio A.7: distinto país/cobertura, no "misma envoltura").
**(c)** El sitio describe el proyecto pero no publica ningún enlace de descarga (`0 href` a `.csv/.xlsx/.zip/.dta/.sav`).
**(d) NO-BAJAR-PORQUE** las cuatro rutas de A.5 están agotadas (universo: sitio propio + Harvard Dataverse; términos: "LAOMS", "eventos de protesta México", "Inclan protest Mexico"; fecha: 2026-09-02) y el sitio público del proyecto no expone la base por ninguna vía.

### 6 · HOMESCAN_CONSUMER_PANEL_SERVICES (NielsenIQ) — `NO-ADQUIRIDA-POR-COSTO`
**(a)** Decisión de mesa (D5, 3/sep/2026, propagada por N8): comercial, alto costo, sin contacto con el proveedor.
**(b)** Hermanas comerciales: `PANEL_DE_COMPRA_DE_HOGARES` (Kantar, fila 8) y `PRICE_AND_INFORMATION_TYPE...` (académico, fila 9) — mismo objeto (`R1.4`), tres proveedores distintos, no la misma fuente (A.7: contenido distinto — panel comercial vs. paper académico).
**(c)** No trae nada adquirido; falta la decisión de mesa de solicitar ficha de cobertura sin contratar.
**(d) NO-BAJAR-PORQUE** ya decidido por mesa (D5): comercial, alto costo, sin contacto — no se re-litiga aquí.

### 7 · OECD — `NO-ACCESIBLE`
**(a)** `oecd.org`, `sdmx.oecd.org`, `oecd-ilibrary.org` → 403 con `cf-mitigated:challenge` (reto Cloudflare, no bloqueo de origen), reconfirmado 2026-09-01. El candidato de disco (`ea3385cf_en`, Terms of Use del OECD Trust Survey PUF) fue bajado por mesa el 2026-09-02: es el formulario de solicitud, no el microdato.
**(b)** Ambigüedad de identidad sin resolver: el código "OECD" no dice cuál encuesta exacta se busca.
**(c)** Trae: el formulario de acceso (Terms of Use). Falta: el microdato en sí, que se solicita firmando y enviando ese formulario a `govtrustinfo@oecd.org`.
**(d) MESA-DECIDE.** Opción (a): mesa firma y envía el formulario ya en el corpus a `govtrustinfo@oecd.org` (`oe.cd/trust`) para solicitar el microdato — costo: trámite institucional con el organismo, sin pago pero con espera. Opción (b): no perseguir el microdato, quedarse con el Terms of Use como evidencia de instrumento — costo: sin dato individual del OECD Trust Survey.

### 8 · PANEL_DE_COMPRA_DE_HOGARES (Kantar Worldpanel) — `NO-ADQUIRIDA-POR-COSTO`
**(a)** Decisión de mesa (D5, propagada por N8): comercial, alto costo, sin contacto.
**(b)** Ver fila 6 (Homescan) y fila 9 (Bauchet académico) — mismo objeto `R1.4`, tres candidatos, ninguno adquirido.
**(c)** No trae nada; falta decisión de mesa sobre cotización.
**(d) NO-BAJAR-PORQUE** ya decidido por mesa (D5) — comercial, alto costo.

### 9 · PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND (Bauchet 2014) — `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`
**(a)** 4 rutas 2026-09-01: (i) `cenfri.org/research-paper/...` → 403 `cf-mitigated:challenge`; (ii) no aplica (página individual sin API); (iii) no aplica (un solo PDF); (iv) SSRN `papers.ssrn.com/sol3/papers.cfm?abstract_id=2474620` → mismo 403 Cloudflare. `web.archive.org` tiene snapshot de la página (200, 327 387 B) pero sin enlace `.pdf` directo.
**(b)** Dos PDF adyacentes del mismo autor (Bauchet) ya en el corpus (`ssrn_bauchet_2589578`, `ssrn_bauchet_2689238`) — verificados por A.7 como **otros** papers (títulos y contenido distintos), no una envoltura distinta del mismo objeto: no cuentan como hermana del objeto pedido.
**(c)** Trae: dos papers adyacentes del mismo autor/tema. Falta: el paper exacto (`abstract_id=2474620`).
**(d) BAJAR** — receta ≤1 min: abrir `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2474620` en un navegador real (el reto Cloudflare que bloquea al agente automatizado típicamente se resuelve para un navegador humano) y descargar el PDF; si SSRN sigue bloqueando, alternativa `https://cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/`.

### 10 · REGISTRO_DE_TANDAS_Y_REPUTACION (Tanda+) — `NO-ADQUIRIDA-POR-COSTO`
**(a)** `tanda.mx` → 200, 11 792 B, 2026-09-01: sitio de mercadotecnia sin ningún enlace de datos/API/reporte/estadística.
**(b)** Hermana: fila 11 (`REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES`), mismo hallazgo, misma familia Tanda+.
**(c)** No trae nada bajable — no hay muro que cruzar, el activo es interno de la empresa.
**(d) NO-BAJAR-PORQUE** el sitio no publica ningún dato; decisión de mesa (D5) ya lo marca `NO-ADQUIRIDA-POR-COSTO` sin contacto.

### 11 · REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES — `NO-ADQUIRIDA-POR-COSTO`
**(a)/(b)/(c)** Idénticos a la fila 10 (misma familia, mismo hallazgo `tanda.mx`, 2026-09-01).
**(d) NO-BAJAR-PORQUE** misma razón que la fila 10.

### 12 · ENAFIN — `NO-ACCESIBLE`
**(a)** `NO-ACCESIBLE-INSTITUCIONAL` confirmado 2 veces (catálogo RNM ficha 1106, reconfirmado 2026-08-19): el microdato de empresa exige acceso presencial al Laboratorio de Microdatos de INEGI.
**(b)** Sin hermana — es un microdato de empresa único de INEGI.
**(c)** Trae: 10 payloads de csv tabulados (agregados por dominio de estudio). Falta: el microdato de empresa, que exige laboratorio presencial.
**(d) NO-BAJAR-PORQUE** barrera institucional (acceso presencial obligatorio) — no hay receta de navegador ni de red que la resuelva remotamente.

### 13 · PI — `PENDIENTE`
**(a)** Código de 2 letras sin `url_conocida`, sin elaboración en ninguna tabla histórica, 2026-09-01.
**(b)** Sin hermana — identidad irresoluble.
**(c)** No trae nada; falta la identidad misma del instrumento.
**(d) NO-BAJAR-PORQUE** universo (`manifiesto.yaml` + tablas históricas), términos ("PI") y fecha (2026-09-01) ya declarados sin candidato — requiere que mesa aclare a qué instrumento se refiere antes de poder perseguirlo.

### 14 · EARTHQUAKE_TRUST_LAPOP_2017 — `PENDIENTE`
**(a)** Búsqueda dirigida (`LAPOP AmericasBarometer 2017 México sismo confianza terremoto módulo especial`), 2026-09-01: no se encontró un módulo/dataset distinto y nombrado — solo la ronda regular AmericasBarometer 2016/17, ya en el corpus (fila 52).
**(b)** Hermana: el corpus LAPOP amplio ya `OBTENIDO` (fila 52) — si el reactivo existe, vive ahí (misma envoltura, A.7), no es una fuente distinta.
**(c)** Trae: el corpus LAPOP completo, ya obtenido. Falta: confirmar si el reactivo de confianza post-sismo existe dentro de ese corpus (tarea de extracción, no de descarga).
**(d) NO-BAJAR-PORQUE** no hay una fuente nueva que bajar — si el reactivo existe, es una extracción de texto sobre un payload ya `OBTENIDO`, fuera del alcance de una descarga.

### 15 · IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA — `PENDIENTE`
**(a)** Búsqueda dirigida sobre `imssbienestar.gob.mx` (transparencia) y `bienestar.gob.mx`, 2026-09-01: no se localizó layout/CSV público de "Acciones de Infraestructura"; ninguno de los dos hosts fue **probado por red** en esa caminata (declarado explícitamente `no probado`).
**(b)** Sin hermana identificada.
**(c)** No trae nada; falta localizar la página específica del programa dentro de esos dos hosts.
**(d) MESA-DECIDE.** Opción (a): dedicar una caminata de `/adquiere` con más tiempo a `imssbienestar.gob.mx`/`bienestar.gob.mx` específicamente (probar los 2 hosts que la caminata previa declaró "no probados") — costo: tiempo de agente, sin garantía de hallazgo. Opción (b): dejarlo `PENDIENTE` sin más presupuesto de búsqueda hasta que mesa aporte una URL o nombre de programa más específico — costo: cero, pero sin avance.

### 16 · MERCER_GPTW_CLIMA_DESEMPENO — `NO-ADQUIRIDA-POR-COSTO`
**(a)** Comercial, alto costo declarado en tabla de origen; sin `url_conocida`, sin sondeo de red (decisión de mesa lo excluye antes de intentar).
**(b)** Sin hermana declarada.
**(c)** No trae nada; falta decisión de mesa sobre pedir ficha técnica sin comprar.
**(d) NO-BAJAR-PORQUE** ya decidido por mesa (D5) — comercial, alto costo, sin contacto.

### 17 · EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 (rótulo real: EXT-OF-05, CompraNet) — `OBTENIDO-PARCIAL`
**(a)** 3 caminatas (`MAESTRA33-A3`, `MAESTRA35-A1`, `MAESTRA36-A2`, 2026-09-01/02/03): dominio migró de `compranet.hacienda.gob.mx`/`compranet.funcionpublica.gob.mx` (no resuelven) a `upcp-compranet.buengobierno.gob.mx`/`comprasmx.buengobierno.gob.mx` (SPA Angular, 200 pero shell sin contenido para `curl`). Los 4 archivos que el encargo original nombraba (bajo `funcionpublica.gob.mx`) no resuelven DNS; en su lugar se obtuvieron, con doble bajada y sha256 verificado (A.7), `Contratos_CompraNet5.xlsx` (4 417 249 B, 13 406×45) y `Expedientes_CompraNet5.xlsx` (1 573 365 B, 7200×21).
**(b)** Alias ya registrado en `aliases-fuentes.tsv` (`compranet_upcp`, `COMPRANET5_DATOS_ABIERTOS`) — el propio sistema de alias ya reconoce que es una fuente con envoltura cambiante (A.7), no una fuente distinta cada vez que migra de dominio.
**(c)** Trae: contratos y expedientes (2/4 archivos declarados por el encargo original). Falta: los 3 `DD_RUPC_*`/`DD_PIC_*` de datos abiertos, con receta de navegador ya documentada.
**(d) BAJAR** — receta ≤1 min ya verificada: abrir `https://comprasmx.buengobierno.gob.mx/datos-abiertos`, esperar a que cargue la SPA, ir al ancla "datos_relevantes_de_los_contratos_ingresados_a_la_plataforma" y guardar los enlaces `DD_PIC_CONTRATOS_*.xlsx`, `DD_PIC_EXPEDIENTES.xlsx` y `DD_RUPC_*.xlsx`.

### 18 · EXT_OF_11_REUNE_REDECO (CONDUSEF) — `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`
**(a)** 2026-09-01: `gob.mx/condusef/...` → 200, 1878 B (stub JS); `www.condusef.gob.mx/?p=reune` → 200, 74 340 B (real, con `-k` por cadena TLS incompleta), enlaza a `eduweb.condusef.gob.mx/Reune/wpinicio.aspx` — herramienta de consulta interactiva por institución, no archivo de descarga masiva.
**(b)** Sin hermana — es un registro administrativo único de CONDUSEF.
**(c)** Trae: confirma que REUNE ofrece consulta pública. Falta: un archivo único descargable — no existe, es una herramienta de búsqueda interactiva.
**(d) NO-BAJAR-PORQUE** REUNE es una herramienta de consulta por institución, no un archivo — no hay un payload único que un curl o una receta de navegador de ≤1 min pueda bajar; una descarga masiva requeriría automatizar N consultas, fuera del alcance de una receta simple.

### 19 · ENVIPE_EXTRACCION_TEXTO_REACTIVO — `PENDIENTE`
**(a)** No aplica sondeo de red — el payload ENVIPE ya está `OBTENIDO` en el corpus; esta fila es una tarea de extracción de texto sobre un archivo ya presente (`v1_2:131370-76`, 0% texto de reactivo real).
**(b)** No aplica — no es una adquisición.
**(c)** Trae: el payload completo, sin texto de reactivo extraído. Falta: extracción de texto (fuera del perímetro de una descarga).
**(d) NO-BAJAR-PORQUE** no es una fila de adquisición — es trabajo de extracción de texto sobre un payload ya obtenido, declarado fuera de perímetro de `/adquiere` y de este acto (`A2` no abre contenido semántico de payloads).

### 20 · BANXICO_ENCUESTA_COMPETENCIAS_FINANCIERAS_EXTRACCION_TEXTO — `PENDIENTE`
**(a)/(b)/(c)** Igual que la fila 19: el payload (`banxico_encuesta_competencias_financieras_2019.xlsx`) ya está `OBTENIDO` (fila 33); faltan 306 filas de texto de reactivo (hoja de códigos sin descripción).
**(d) NO-BAJAR-PORQUE** misma razón que la fila 19 — tarea de extracción, no de adquisición.

### 21 · DIN-11_CONOCIMIENTO_CUENTAS_SIN_COMISION_SIN_CANDIDATA — `PENDIENTE`
**(a)** Universo agotado: 241 591 filas, 5 formulaciones de búsqueda (`"sin comision"`, regex cuenta/comisión, `"comision"`+ENIF, `"comision"` abierta -19 candidatas de gasto/propina-, `"cuenta bancaria"`/`"cuenta de ahorro"` abierta -6 candidatas, todas miden tenencia no conocimiento), 2026-09-01. Sin URL, sin nombre de instrumento candidato.
**(b)** Sin hermana — sin candidato de ningún tipo.
**(c)** No trae nada; falta un instrumento con reactivo de conocimiento declarativo (no tenencia) sobre cuentas sin comisión.
**(d) NO-BAJAR-PORQUE** universo (241 591 filas), 5 términos de búsqueda y fecha (2026-09-01) ya declarados sin candidato de red — hueco real de instrumento, no de acceso.

### 22 · SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA — `PENDIENTE`
**(a)** Universo agotado: 241 591 filas, 5 formulaciones (regex hermano/cuidado, "hermano"+ENASEM, frases de reparto -0 cada una-, "hermano" abierto -350 candidatas de corresidencia/dependencia económica, ninguna sobre acordar el cuidado-, "cuidador"/"cuida a" -7 candidatas de niñero/nietos-), 2026-09-01.
**(b)** Sin hermana.
**(c)** No trae nada; falta un instrumento con reactivo específico sobre acuerdos de cuidado compartido entre hermanos adultos.
**(d) NO-BAJAR-PORQUE** mismo criterio que la fila 21 — universo, 5 términos y fecha declarados, sin candidato.

### 23 · SICEE — `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`
**(a)** `WebFetch` de `https://sicee.ine.mx/` (`ACTO MAESTRA34-L1`, 1/sep/2026): SPA sin contenido accesible sin navegador (mismo patrón que INE/INEGI ya documentado en `manifiesto.yaml:2729`). Cobertura declarada por el propio sistema: elecciones locales desde 2015 (2006/2012 fuera por diseño, no por falla de búsqueda).
**(b)** Alias ya registrado en `aliases-fuentes.tsv` (`sicee_ine` → `SICEE_INE_ESTADISTICA_ELECCIONES`) — mismo objeto, ya reconocido como fuente propia (A.7), no hermana externa.
**(c)** Trae: identidad y cobertura confirmadas. Falta: la descarga real vía navegador (SPA no accesible por `curl`/`WebFetch`).
**(d) BAJAR** — receta ≤1 min ya documentada: `forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md` líneas 183-198 (nota: la cita "l.165-195" del encargo original apunta a un rango equivocado, corregido aquí).

### 24 · TEPJF_ELECCIONES_CONCURRENTES_1991_2018 — `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`
**(a)** 4 rutas 2026-09-02: (i) `te.gob.mx/publicaciones/` → 200, 2102 B, y una ruta profunda inexistente da el MISMO 2102 B (soft-404); (ii) buscador del portal (`q=elecciones+concurrentes...`) → 200, 702 482 B, cero enlaces con "concurren"/"1991"; (iii) no aplica (solo PDF conocido); (iv) espejo académico, `SIN-FETCH` (no probado).
**(b)** Sin hermana — benchmark único del TEPJF.
**(c)** No trae nada; falta abrir el catálogo (aplicación JavaScript, por eso `curl` solo ve el shell) y localizar el PDF del libro.
**(d) BAJAR** — receta ≤1 min ya documentada: abrir `https://www.te.gob.mx/publicaciones/`, esperar a que cargue el catálogo (JS), escribir "Elecciones concurrentes" en el buscador del catálogo, abrir la ficha del libro "Elecciones concurrentes y participación electoral en México, 1991-2018" (2020) y descargar el PDF.

### 25 · IEEPCO_OAXACA_SERIE_MUNICIPAL — `NO-OBTENIDO-POR-ESTE-AGENTE(6 intentos)`
**(a)** 2026-09-02: pata 2016 **verificada y localizada** — `https://www.ieepco.org.mx/archivos/elecciones-2016/ESTAD%C3%8DSTICA%20CONCEJALES%20%202016.xlsx` → 200, 968 301 B, xlsx real con `LISTA_NOM` por casilla (25 hojas). Patas 2018/2021/2022/2024: 8 sondas del mismo patrón de URL, ninguna devolvió xlsx.
**(b)** Hermanas de la misma familia (series municipales por OPLE estatal) ya registradas en `aliases-fuentes.tsv`: `IEC_COAHUILA`, `IEEM_EDOMEX`, `IEEBC_BC`, `IEEZ_ZACATECAS`, `IEECH_CHIHUAHUA` — mismo objeto (resultados municipales por casilla/municipio), fuente distinta por estado (A.7: no son la misma fuente, son análogas). Se propone en texto (no se da de alta) el patrón `IEEPCO_OAXACA` como sexta entrada de esa misma familia.
**(c)** Trae: la pata 2016 completa (concejales por casilla). Falta: 2018, 2021, 2024 (exige el filtro de usos y costumbres que la spec original excluye con conteo) — portal de autoridades electas (`/autoridades_electas/resultados/`) declarado como sucesor.
**(d) BAJAR** — receta ≤1 min para la pata 2016 (URL directa arriba, xlsx real); las patas 2018/2021/2024 quedan `MESA-DECIDE` de un acto sucesor (costo: navegar el portal de autoridades electas por consulta, sin URL directa conocida) — no se fuerza a un solo valor una fila con partes en estados distintos.

### 26 · IETAM_TAMAULIPAS_SERIE_MUNICIPAL — `NO-OBTENIDO-POR-ESTE-AGENTE(5 intentos)`
**(a)** 2026-09-02: la página de Estadística Electoral (`ietam.org.mx/PortalN/Paginas/EstadisticaEl/Estadistica_Electoral.aspx`) enumera 43 archivos `Municipios_2017-2018/<Municipio>.xlsx`; 24 de PE2021 son de diputaciones (no ayuntamientos) y 16 de PE2024 son de la elección judicial (no municipal) — defecto medido y declarado. La URL directa por patrón (`/documentos/Municipios_2017-2018/Abasolo.xlsx`) da 404: la base real de esas rutas relativas no es la raíz del dominio.
**(b)** Misma familia de hermanas que la fila 25 (series municipales por OPLE estatal).
**(c)** Trae: identificación de los 43 archivos de 2018 municipales (nombre y ruta relativa). Falta: resolver la base real del enlace para poder bajarlos, y localizar 2016/2021/2024 municipales (ausentes de esa página).
**(d) BAJAR** — receta ≤1 min: abrir `https://ietam.org.mx/PortalN/Paginas/EstadisticaEl/Estadistica_Electoral.aspx` en un navegador, hacer clic en cualquiera de los 43 enlaces `Municipios_2017-2018/<Municipio>.xlsx` (el navegador resuelve la ruta relativa real que un `curl` con URL adivinada no resuelve) y descargar; repetir por municipio.

### 27 · INEGI_CNGF — `NO-ACCESIBLE-DESDE-LA-CAJA(firma c1)`
**(a)** Sonda única (2026-09-02): `curl` a `inegi.org.mx/programas/cngf/` → 200 pero 321 B (stub JS); programa real en `/programas/cngf/2025/`. Ficha RNM 1145 (estática) confirma identidad: unidad de análisis = instituciones de la Administración Pública Federal, NO personas.
**(b)** Sin hermana — es un censo institucional único.
**(c)** Trae: nada en el corpus (`grep -c -i cngf manifiesto.yaml` = 0 de 20 529 líneas). Falta: el tabulado agregado — pero aun bajado, da OFERTA institucional agregada, no conducta individual.
**(d) NO-BAJAR-PORQUE** doble razón declarada por mesa (firma c1, `MAESTRA35-L6`): (i) acceso administrativo requiere navegador o solicitud de transparencia, no red desde la caja; (ii) aun accedido, la unidad de análisis institucional no satisface la regla `tramite.gobierno_digital.coercitivo_*` (que exige conducta individual) — bajarlo no cierra nada por sí solo.

### 28 · PDN_SESNA_S1_S2_S3_S6 — `OBTENIDO-PARCIAL`
**(a)** Mesa depositó `PDN_S3v2.zip` (1 459 284 B, 34 miembros, 2026-09-03): solo el sistema S3 (servidores públicos sancionados), un `.json` por entidad. S1 (declaraciones), S2 (personas en contrataciones) y S6 (contratos) no llegaron.
**(b)** Alias declarado explícitamente como NO fusionado (por decisión de mesa pendiente, `FP-265`) con `COMPRANET5_DATOS_ABIERTOS` ni con `EXT_OF_07` (fila 17) — son objetos distintos hasta que mesa decida.
**(c)** Trae: S3 completo. Falta: S1, S2, S6 — receta: portal PDN de SESNA (`plataformadigitalnacional.org`) y documentación de estructuras en `github.com/PDNMX`.
**(d) BAJAR** — receta ≤1 min: abrir `https://www.plataformadigitalnacional.org/`, localizar los sistemas S1 (declaraciones), S2 (personas en contrataciones) y S6 (contratos) en el menú de sistemas, y descargar los mismos formatos `.json` por entidad que ya se usó para S3; documentación de la estructura de cada sistema en `github.com/PDNMX` si el nombre de archivo no es evidente.

## Resumen (28 filas)

| Recomendación | Filas |
|---|---|
| **BAJAR** | 9, 17, 23, 24, 25 (parcial: 2016), 26, 28 — **7** |
| **NO-BAJAR-PORQUE** | 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 27 — **18** |
| **MESA-DECIDE** | 1, 7, 15 — **3** |

Recetas de las filas `BAJAR` compiladas en `forense/notas/2026-09-04-MAESTRA37-A2-PAQUETE-RECETAS-3.md`.

## Lo que NO decide este acto

Ninguna fila cambia `estado_A4A5` por este acto — la columna `nota` de la cola recibe un append con puntero a este informe (a A.5, INFRA-1, ya escribe columnas ampliadas sin tocar `estado_A4A5`). La clasificación BAJAR/NO-BAJAR-PORQUE/MESA-DECIDE es información para que mesa decida (`FP-289`), no un cierre de fila.
