ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE — revisión de la cola a detalle

Encargo archivado verbatim: `forense/encargos/2026-09-03-MAESTRA37-A2-REVISA-COLA-A-DETALLE.md`.

## §0 · Premisas

**Compuerta.** `PR de N8 fusionado` — verificado contra `origin/main` recién fetcheado: PR #523 (MAESTRA37-N8 CONSOLIDA-DECISIONES) fusionó como `4b508ad` (`d96bf44 CONSUMIDO: MAESTRA37-N8 ejecutado`, `c088df8 0-bis A.3: archiva encargo MAESTRA37-N8`). Cumplida.

**FIRMA DE MESA citada por el encargo.** El encargo cita «la de «Descargas manuales» en §0» como firma verbatim. Se buscó esa cita (`grep -rl "^§0" --include="*.md"` cruzado con «Descargas manuales/Descargas Manuales» en todo el repo) y no se localizó un §0 único e inequívoco con ese rótulo exacto — el término «§0» es una convención genérica de encabezado usada en más de 130 notas de este repo, y ninguna de las que además mencionan «Descargas manuales» data de una sesión que pueda identificarse como *la* referida por este encargo. Se declara la búsqueda en vez de inventar la cita. Lo que sí es inequívoco, porque el propio encargo lo da como paráfrasis operativa inmediatamente después, es la regla que gobierna este acto: **ninguna fila se cierra por veredicto de agente; el entregable es información para que mesa decida.** Ese es el criterio bajo el que corre todo este documento — ninguna recomendación de abajo cambia `estado_A4A5`.

**Universo, derivado al arrancar (no heredado del A.8 del encargo, que es una foto pre-N8).** `data/curacion-registro/cola-adquisicion-registro.tsv` en `origin/main` (`4b508ad`): 112 filas totales. Excluyendo `estado_A4A5 == OBTENIDO` (83) y todo lo que empieza con `CERRADA` (`CERRADA-PREEXISTENTE`, 1), quedan **28** filas no-OBTENIDO/CERRADA:

| estado_A4A5 | filas |
|---|---:|
| PENDIENTE | 9 |
| NO-OBTENIDO-POR-ESTE-AGENTE | 7 |
| NO-ADQUIRIDA-POR-COSTO | 5 |
| NO-ACCESIBLE | 3 |
| OBTENIDO-PARCIAL | 2 |
| PENDIENTE-DE-MESA | 1 |
| NO-ACCESIBLE-DESDE-LA-CAJA | 1 |
| **total** | **28** |

Nota de discrepancia con el A.8 del encargo (informativa, no bloqueante): el encargo anticipaba, tras N8, «5 a NO-ADQUIRIDA-POR-COSTO y 2 a PENDIENTE-DE-MESA» — el resultado real de N8 en `origin/main` trae 5 `NO-ADQUIRIDA-POR-COSTO` (coincide) y **1** `PENDIENTE-DE-MESA` (no 2), más una fila nueva `CERRADA-PREEXISTENTE` que el A.8 del encargo no anticipaba. El encargo mismo advierte que su A.8 es una foto pre-N8 y que el universo real «es lo que quede no OBTENIDO, derivado al arrancar» — este documento deriva contra el árbol, no contra el forecast.

## §1 · COMMIT-1 — lista congelada y pregunta por fila

Por fila: la necesidad/regla que la cita en `data/curacion-registro/relaciones.tsv` (unida por `fuente_canonica_normalizada` exacta) y, si existe, el `objeto_modelo_origen` de esa necesidad en `necesidad-objeto-modelo.tsv`. Cuando ninguna relación cita la fila por identidad exacta de fuente, se declara — es información para mesa, no un cierre de la fila ni una afirmación de que la fila carece de propósito (dos filas, `..._SIN_CANDIDATA`, llevan el código de regla en su propio nombre de fila aunque `relaciones.tsv` no las una todavía por fuente; se preserva esa pista en la columna `origen`/`nota` de la fila, no se inventa una unión).

| # | fuente_canonica | estado_A4A5 | pregunta que responde (necesidad / objeto_modelo_origen) |
|---:|---|---|---|
| 1 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | PENDIENTE-DE-MESA | N15 (NEGATIVA) → `G6.deferencia` |
| 2 | `SE` | PENDIENTE | N22 (NEGATIVA) → `R2.1`; N32 (NEGATIVA) → `R10.2`; N21 (CANDIDATA) → `R1.4` |
| 3 | `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | PENDIENTE | N19 (NEGATIVA) → `dinero.credito.scoring_alternativo` |
| 4 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | NO-ACCESIBLE | N20 (NEGATIVA) → `civico.denuncia.con_seguro` |
| 5 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | NO-OBTENIDO-POR-ESTE-AGENTE(31 intentos) | N27 (CANDIDATA) → `R7.5` |
| 6 | `HOMESCAN_CONSUMER_PANEL_SERVICES` | NO-ADQUIRIDA-POR-COSTO | N21 (NO_ACCESIBLE) → `R1.4` |
| 7 | `OECD` | NO-ACCESIBLE | N30 (CANDIDATA) → `R8.3` |
| 8 | `PANEL_DE_COMPRA_DE_HOGARES` | NO-ADQUIRIDA-POR-COSTO | N21 (NO_ACCESIBLE) → `R1.4` |
| 9 | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intento) | N21 (CANDIDATA) → `R1.4` |
| 10 | `REGISTRO_DE_TANDAS_Y_REPUTACION` | NO-ADQUIRIDA-POR-COSTO | N29 (NO_ACCESIBLE) → `R8.2` |
| 11 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | NO-ADQUIRIDA-POR-COSTO | N29 (NO_ACCESIBLE) → `R8.2` |
| 12 | `ENAFIN` | NO-ACCESIBLE | N19 (CANDIDATA) → `dinero.credito.scoring_alternativo` |
| 13 | `PI` | PENDIENTE | N19 (CANDIDATA) → `dinero.credito.scoring_alternativo` |
| 14 | `EARTHQUAKE_TRUST_LAPOP_2017` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 15 | `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 16 | `MERCER_GPTW_CLIMA_DESEMPENO` | NO-ADQUIRIDA-POR-COSTO | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 17 | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | OBTENIDO-PARCIAL | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 18 | `EXT_OF_11_REUNE_REDECO` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intento) | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 19 | `ENVIPE_EXTRACCION_TEXTO_REACTIVO` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 20 | `BANXICO_ENCUESTA_COMPETENCIAS_FINANCIERAS_EXTRACCION_TEXTO` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 21 | `DIN-11_CONOCIMIENTO_CUENTAS_SIN_COMISION_SIN_CANDIDATA` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 22 | `SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA` | PENDIENTE | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 23 | `SICEE` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intento) | N25 (CANDIDATA) → `R7.1`; N26 (CANDIDATA) → `R7.3` |
| 24 | `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intentos) | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 25 | `IEEPCO_OAXACA_SERIE_MUNICIPAL` | NO-OBTENIDO-POR-ESTE-AGENTE(6 intentos) | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 26 | `IETAM_TAMAULIPAS_SERIE_MUNICIPAL` | NO-OBTENIDO-POR-ESTE-AGENTE(5 intentos) | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 27 | `INEGI_CNGF` | NO-ACCESIBLE-DESDE-LA-CAJA(firma c1) | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |
| 28 | `PDN_SESNA_S1_S2_S3_S6` | OBTENIDO-PARCIAL | *ninguna necesidad la cita por fuente_canonica_normalizada exacta en relaciones.tsv* |

Esta lista y esta tabla quedan congeladas para el resto del acto: COMMIT-2 investiga estas 28 filas, en este orden, y no agrega ni quita ninguna.

