# Tablero por carriles · los 31 reports del mexicano

Un carril por report de `corpus/reports/`: cómo está (evidencia), qué lo detiene (stoppers) y cuál es la siguiente acción. Todo lo que está entre las marcas `TABLERO-DERIVADO` lo escribe `python3 tools/tablero_carriles.py --actualiza` (el canal lo regenera en cada push a `main`); no se edita a mano. Versión web: [docs/tablero-carriles.html](../../docs/tablero-carriles.html). Tablero del programa (GEN1→GEN2): [TABLERO-PROGRAMA.md](TABLERO-PROGRAMA.md).

## Lectura de dirección

<!-- LECTURA-DIRECCION: única sección tecleada por un humano; opinión, fechada. -->
_Opinión de dirección, 28/sep/2026 (ACTO GEN2-TABLERO-CARRILES-1). No es derivado: se lee contra las tarjetas de abajo, que sí lo son._

- **Ningún carril está en verde, y no por falta de cifras.** Casi todos los carriles con dominio medido tienen cifras adoptadas en su núcleo; lo que los detiene en amarillo es que sus reglas SI-ENTONCES siguen sin dictamen con cifra (la hoja C3 está toda en PROPUESTA). El cuello de botella del modelo es contrastar reglas, no descargar encuestas.
- **Los rojos son dominios sin encuesta propia en el catálogo** (rural-indígena, duelo, tiempo, humor, juventud, emociones morales, autoridad). Ahí la siguiente acción no es un CALC: es decidir si existe instrumento o si el carril queda descriptivo.
- **La adquisición pendiente es casi toda documental.** La mayor parte de las afirmaciones «con adquisición» citan estudios, informes o sondeos que no son programas del corpus (fila SIN-UNION con su propietario Astra). Las que sí casan con un programa en su mayoría ya están en el manifiesto o tienen su programa OBTENIDO en la cola: antes de pedir una descarga, mirar esa línea del carril.
- **Una firma destraba muchos carriles a la vez:** el acceso C1 del lote 3 (`FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-02`) es la siguiente acción de la mayoría de los carriles con stopper de firma. Es la de mayor palanca para la sesión de mesa.
- **Límites de esta lectura:** la unión carril ↔ instrumento es por palabra en `instrumento_ola`, y la reserva de ENIGH 2024 que la memoria operativa declara no tiene token en el manifiesto ni en tabla-final, así que el tablero no la ve (hallazgo del acto).

<!-- TABLERO-DERIVADO:BEGIN -->
## Cómo leer

Umbrales (único sitio: cabecera de `tools/tablero_carriles.py`): núcleo = dominio con peso ≥ 0.2 (más el de mayor peso) · VERDE exige cifra adoptada en todo el núcleo y reglas con dictamen ≥ 0.5 · NARANJA = núcleo cubierto por cifra adoptada o piso sellado registrado en la vista pendiente de adopción (visibilidad, no adopción) · GRIS = dominio principal en GENETICA, GENOMICA o NO-MEDIBLE-POR-DISEÑO > 0.5 · a lo más 5 stoppers listados por categoría ⟨S⟩

Precedencia de la siguiente acción: FIRMA > RESERVA > ADQUISICION > NC-PARO > CALC > EDITORIAL. Cada línea con un número lleva `⟨F…⟩`: el archivo del que sale, con su blob y su lector en «Cadena de procedencia». `S` = regla del script. El catálogo no trae `report`: la unión carril ↔ cifra pasa por dominio × instrumento. Firmas, reservas, NC, CALC, actos en vuelo y validación casan con los instrumentos del núcleo y se ordenan por relevancia. ⟨S⟩

## Resumen

Carriles 31: 🔴 ROJO 3 · 🟡 AMARILLO 21 · 🟠 NARANJA 4 · 🟢 VERDE 0 · ⚪ GRIS 3 ⟨F1 F2 F3 S⟩

| carril | report | semáforo | afirm. | núcleo con cifra | reglas con dictamen | stoppers | siguiente acción | ⟨⟩ |
|---|---|---|---:|---:|---:|---:|---|---|
| CARRIL-02 | Ausencia sin certeza · duelo y pérdida ambigua en familias d | 🔴 ROJO | 41 | 0/1 | 0% de 4 | 2 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-13 | Humor in Mexican Psychological Life · 2023-2026 Update | 🔴 ROJO | 34 | 0/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-17 | Moral Emotions in Mexico · Declared Dignity · Relational Fac | 🔴 ROJO | 31 | 0/1 | 0% de 2 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-24 | Psicología del Trabajo en México · Un Mapa Basado en Evidenc | 🟡 AMARILLO | 57 | 1/1 | 0% de 3 | 5 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-15 | La familia mexicana como sistema psicológico · entre el afec | 🟡 AMARILLO | 51 | 1/1 | 0% de 3 | 5 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-07 | El Efecto Ambiental de la Violencia Crónica en México · Cómo | 🟡 AMARILLO | 48 | 1/1 | 0% de 4 | 3 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-10 | Elegir · Cortejar y Amar en el México de Hoy · Díada de Pare | 🟡 AMARILLO | 46 | 2/2 | 0% de 4 | 4 | FIRMA: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-14 | La arquitectura invisible de la interacción social en México | 🟡 AMARILLO | 45 | 1/2 | 0% de 2 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-01 | Adopción y Resistencia Tecnológica en México · La Paradoja d | 🟡 AMARILLO | 43 | 1/1 | 0% de 3 | 3 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-06 | El Clasemediero Mexicano · Identidad · Ansiedad de Estatus y | 🟡 AMARILLO | 43 | 1/1 | 0% de 2 | 5 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-20 | Psicología Política y Comportamiento Cívico del Mexicano Con | 🟡 AMARILLO | 43 | 1/1 | 30% de 10 | 6 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-19 | Non-Family Social Capital in Mexico · Cooperation · Trust ·  | 🟡 AMARILLO | 42 | 1/1 | 44% de 9 | 6 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-25 | Psychology of Mexico-US Migration · Identity · Family · Aspi | 🟡 AMARILLO | 42 | 1/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-12 | Health · Body · Food and Substance Use in Mexico · The Behav | 🟡 AMARILLO | 39 | 1/1 | 0% de 3 | 7 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-29 | Salud Mental en México · Prevalencia · Estigma y la Brecha e | 🟡 AMARILLO | 39 | 1/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-18 | Mérito · Movilidad Social y Desigualdad en México · Actualiz | 🟡 AMARILLO | 38 | 1/1 | 0% de 4 | 6 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-23 | Psicología del Consumidor Mexicano · Patrones · Contradiccio | 🟡 AMARILLO | 38 | 2/2 | 40% de 5 | 2 | RESERVA: `ENDUTIH 2025` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-27 | Religiosidad y Psicología del Mexicano Contemporáneo · Moral | 🟡 AMARILLO | 38 | 1/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-28 | Report 26 · The Contemporary Mexican and Knowledge · Experti | 🟡 AMARILLO | 38 | 2/2 | 22% de 9 | 4 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-31 | Vejez y Cuidado Intergeneracional en México · El Debilitamie | 🟡 AMARILLO | 38 | 1/1 | 25% de 4 | 2 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-04 | Behavioral Finance Mexicano · Estructura · Adaptación Racion | 🟡 AMARILLO | 35 | 1/1 | 33% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-05 | Confianza y Desconfianza en México · Anatomía Psicológica de | 🟡 AMARILLO | 33 | 1/1 | 0% de 4 | 5 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-26 | Reconfiguración de los Guiones de Género en México · Masculi | 🟡 AMARILLO | 33 | 2/2 | 0% de 3 | 5 | FIRMA: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-21 | Psicología · Conducta y Sociedad en el México Contemporáneo  | 🟡 AMARILLO | 28 | 2/2 | 0% de 0 | 6 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-09 | El México Rural e Indígena en sus Propios Términos · Comunal | 🟠 NARANJA | 49 | 0/1 | 0% de 3 | 3 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-08 | El Mexicano y el Tiempo · Estructura · no Cultura · en la Pl | 🟠 NARANJA | 38 | 0/1 | 29% de 7 | 4 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-22 | Psicología de la Juventud Mexicana Contemporánea · Gen Z y M | 🟠 NARANJA | 32 | 0/1 | 0% de 4 | 4 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-03 | Autoridad y jerarquía en el México contemporáneo · anatomía  | 🟠 NARANJA | 30 | 0/1 | 0% de 3 | 6 | FIRMA: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-11 | Genetica y Conducta del Mexicano Contemporaneo · Canal Indiv | ⚪ GRIS | 38 | 0/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-16 | Mexican Population Genomics · 2025-2026 Scientific and Marke | ⚪ GRIS | 33 | 0/1 | 0% de 2 | 4 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-30 | Sanción Social Horizontal en México · Chisme · Envidia y Mal | ⚪ GRIS | 22 | 0/1 | 0% de 2 | 2 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |

## Adquisición — global

Cola de adquisición: 952 filas; por estado A4/A5 (primer token, tal cual): OBTENIDO 879 · OBTENIDO-PARCIAL 20 · SOLICITUD-PREPARADA 13 · NO-ACCESIBLE 10 · NO-OBTENIDO-POR-ESTE-AGENTE 8 · NO-ENCONTRADO 6 · CERRADA 4 · CERRADA-PREEXISTENTE 4 · SUPERADA-POR 4 · SIN-FETCH 2 · DIFERIDO-A 1 · NO-ADQUIRIDA-POR-COSTO 1 ⟨F5⟩

Manifiesto: 7198 payloads; con `estado_reserva`: RESERVADA-NO-ABIERTA-NO-INDEXAR-L 173 · DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS 45 · RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR 4; licencia ausente o NO-DECLARADA: 220 ⟨F6⟩

Vocabulario de instrumentos: 149 tokens; tokens de la cola citados por los reports y fuera del vocabulario: ninguno ⟨F12 F2 F1 F5 S⟩

Fuentes pendientes en la cola (quién la pide, por la regla QUIEN_PIDE):

| fuente | estado A4/A5 | prioridad | quién la pide | ⟨F5⟩ |
|---|---|---|---|---|
| `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | OBTENIDO-PARCIAL | 20 | caja (completa el payload) | ⟨F5 S⟩ |
| `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | OBTENIDO-PARCIAL | 21 | caja (completa el payload) | ⟨F5 S⟩ |
| `OECD` | OBTENIDO-PARCIAL | 36 | caja (completa el payload) | ⟨F5 S⟩ |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | OBTENIDO-PARCIAL | 38 | caja (completa el payload) | ⟨F5 S⟩ |
| `REGISTRO_DE_TANDAS_Y_REPUTACION` | OBTENIDO-PARCIAL | 39 | caja (completa el payload) | ⟨F5 S⟩ |
| `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | SOLICITUD-PREPARADA | 40 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENAFIN` | OBTENIDO-PARCIAL | 49 | caja (completa el payload) | ⟨F5 S⟩ |
| `MERCER_GPTW_CLIMA_DESEMPENO` | NO-ADQUIRIDA-POR-COSTO | general-9 | mesa (costo) | ⟨F5 S⟩ |
| `SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA` | NO-ENCONTRADO | fp190-6 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENJUVE` | OBTENIDO-PARCIAL | sin-prioridad-asignada | caja (completa el payload) | ⟨F5 S⟩ |
| `REUTERS_DNR` | OBTENIDO-PARCIAL | sin-prioridad-asignada | caja (completa el payload) | ⟨F5 S⟩ |
| `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `RUPC` | OBTENIDO-PARCIAL(RUPC historico 2019 via datamx.io | a6-reconciliacion | caja (completa el payload) | ⟨F5 S⟩ |
| `ENSAFI_TANDAS_PARTICIPACION_R8_2_N29` | OBTENIDO-PARCIAL | — | caja (completa el payload) | ⟨F5 S⟩ |
| `CONDUSEF_CNBV_TANDAS_FUERA_DE_PERIMETRO` | NO-ENCONTRADO | — | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ROSCA_ACADEMICO_MEXICO_BUSQUEDA` | NO-ENCONTRADO | — | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENNVIH_DIN_M_01_DISENO_INFERENCIAL` | SOLICITUD-PREPARADA | GEN2-E09-DIN | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXI` | OBTENIDO-PARCIAL | 0 | caja (completa el payload) | ⟨F5 S⟩ |
| `MPS2012_35024_0001_DATA_DTA` | SOLICITUD-PREPARADA | 18 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `OECD_TRUST_PUM_2021_2023_2025` | SOLICITUD-PREPARADA | 36 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENJUVE_MICRODATOS_2000_2005_2010` | SOLICITUD-PREPARADA | sin-prioridad-asignada | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENVIPE_ROSTER_UPM_O_SERVICIO_VARIANZA` | SOLICITUD-PREPARADA | 0 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENCIG_TASA_NACIONAL_PAGO_INFORMAL_POR_CANAL` | SOLICITUD-PREPARADA | 0 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENSAFI_TANDAS_REPUTACION_INCUMPLIMIENTO` | NO-ENCONTRADO | 39 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `CFPB_BNPL_UNSECURED_DEBT_2025` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENPOL_2016_MICRODATOS_CSV` | OBTENIDO-PARCIAL | 60 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENAPROCE_2015_2018_MICRODATO_COMPLETO` | NO-ACCESIBLE | F6-R03 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `CONDUSEF-REDECO_SERIE` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `EMOVI_2011` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `EMOVI_2023` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENAFI_SIN-OLA` | NO-ENCONTRADO | 3 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENEM_2024` | NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `EQD-PANEL_2018` | NO-OBTENIDO-POR-ESTE-AGENTE(3 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `IFPS-MEXICO_2020-2021` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `INEGI-MMP_2024` | NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `MCPS_SIN-OLA` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `WVS-EEUU-JAPON_7` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `WVS-LONGITUDINAL_1981-2022` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENAPROCE_2015_2018_MICRODATO_COMPLETO` | NO-ACCESIBLE | F6-R03 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ECRIGE_CDMX_2019` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ECRIGE_CDMX_2019_FD` | NO-OBTENIDO-POR-ESTE-AGENTE(10) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_2012_2022_DATOS_ABIERTOS_Y_DOCUMENTACION` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENVE_2012_2014_DATOS_ABIERTOS` | NO-OBTENIDO-POR-ESTE-AGENTE(4) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_2020_2022_BASE_EJEMPLO` | NO-OBTENIDO-POR-ESTE-AGENTE(4) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_MICRODATO_COMPLETO_2012_2024` | NO-ACCESIBLE | OBTENCION-EXTERNA-1 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENCRIGE_2016_MICRODATO_COMPLETO` | NO-ACCESIBLE | OBTENCION-EXTERNA-1 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `IECM_SEPCOPP_RESULTADOS_2011_2025` | NO-OBTENIDO-POR-ESTE-AGENTE(11) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `IECM_COPACO_2020_2023_RESULTADOS_E_INTEGRACION` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `MECANISMO_PROTECCION_INFORMES_ESTADISTICOS` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `JEMS_47_6_REPLICAS_3X1_Y_REMESAS_VIGILANTISMO` | NO-ENCONTRADO | OBTENCION-EXTERNA-1 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `BANXICO_ESTUDIOS_EFECTIVO_Y_BILLETES` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `PROFECO_QQP` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ECCO_SFP_CLIMA_CULTURA_ORGANIZACIONAL` | NO-OBTENIDO-POR-ESTE-AGENTE(13) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `SANDOVAL_2026_LATIN_AMERICAN_POLICY` | SIN-FETCH | OBTENCION-EXTERNA-1 | acto de nube (abrir la fuente) | ⟨F5 S⟩ |
| `PELLEGRINI_SCANDURA_2008_JOM` | SIN-FETCH | OBTENCION-EXTERNA-1 | acto de nube (abrir la fuente) | ⟨F5 S⟩ |
| `BANXICO_CODI_TAG_RESEARCH_ESTUDIO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `SEGOB_MECANISMO_INCORPORACIONES_E_INCIDENTES_2012_2026` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `FELIX_BRASDEFER_ROLE_PLAYS_CODIFICADOS` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `FIU_DELANEY_2021_MICRODATO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `WORLDPANEL_NUMERATOR_CONVENIO_ACADEMICO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |

## Frente 2027 ⟨F11⟩

| familia | ola | estado | gate faltante | firma que lo abre | carriles que alimenta | ⟨⟩ |
|---|---|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-ASTRA6-C1-PA | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-04, CARRIL-05, CARRIL-08, CARRIL-15, CARRIL-23 | ⟨F11 F1⟩ |
| ENIF-HORIZONTE-AHORRO | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-ASTRA6-C1-PA | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-04, CARRIL-05, CARRIL-08, CARRIL-15, CARRIL-23 | ⟨F11 F1⟩ |
| ENCIG-PAGO-DIGITAL | encig_2027 | SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01) | CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-dato del re | FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01 (FIRMADA: suspender); FP-2609 | CARRIL-05, CARRIL-07, CARRIL-18, CARRIL-20 | ⟨F11 F1⟩ |
| ENCIG-SOLICITUD-MORDIDA | encig_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-05, CARRIL-07, CARRIL-18, CARRIL-20 | ⟨F11 F1⟩ |
| ENVIPE-DENUNCIA-U4 | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-02, CARRIL-05, CARRIL-07, CARRIL-19, CARRIL-20, CARRIL-30 | ⟨F11 F1⟩ |
| ENVIPE-EVASION-NORMA | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-02, CARRIL-05, CARRIL-07, CARRIL-19, CARRIL-20, CARRIL-30 | ⟨F11 F1⟩ |
| ENOE-INFORMALIDAD | 2027T4 | NO-LANZAR-TODAVIA | CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(FP-260927-G | FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01; FP-260926-GEN2-AST | CARRIL-06, CARRIL-08, CARRIL-10, CARRIL-12, CARRIL-15, CARRIL-18, CARRIL-21, CARRIL-22, CARRIL-24, CARRIL-26, CARRIL-28, CARRIL-31 | ⟨F11 F1⟩ |
| ENSU-CAMPECHE-INSEGURIDAD | 2027T4 | NO-LANZAR-TODAVIA | CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA(FP-260926- | FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 | CARRIL-07, CARRIL-14, CARRIL-30 | ⟨F11 F1⟩ |

## Carriles

### 🔴 CARRIL-02 · Ausencia sin certeza · duelo y pérdida ambigua en familias de personas desaparecidas en México ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 41**: medible en corpus 3 · con adquisición 24 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: DUELO 33 (80%) núcleo · CONFIANZA 1 (2%) · FAMILIA_CUIDADOS 1 (2%) · GENERO 1 (2%) · MIGRACION 1 (2%) · RELIGIOSIDAD 1 (2%) · SALUD 1 (2%) · SALUD_MENTAL 1 (2%) · SANCION_SOCIAL 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 3 · ENNVIH 1 · ENVIPE 1; sin instrumento reconocido: 36 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: DUELO ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 4 · PASA 142 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 9 / 23 / 3 / 20): EN-MAIN · recibo pr-1246 · regla adoptada: No acreditada aquí · reserva material: 20 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): SIN-UNION 24 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F8⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 24 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL ×13, ASTRA5-MESA-DOCUMENTAL ×6, ASTRA5-U5 ×5 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL ×13, ASTRA5-MESA-DOCUMENTAL ×6, ASTRA5-U5 ×5 ⟨F1 F5 F6⟩

### 🔴 CARRIL-13 · Humor in Mexican Psychological Life · 2023-2026 Update ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 34**: medible en corpus 1 · con adquisición 19 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 1 ⟨F1⟩
- **Dominios**: HUMOR 28 (82%) núcleo · SALUD_MENTAL 4 (12%) · GENERO 2 (6%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): LATINOBAROMETRO 3; sin instrumento reconocido: 31 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): LATINOBAROMETRO 3 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: HUMOR ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 68 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 3 / 15 / 0 / 17): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 17 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · SIN-UNION 17 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 17 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CULTURA ×5, ASTRA5-MESA-CULTURA / ASTRA5-MESA-DOCUMENTAL ×3, ASTRA5-U4 ×3 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-CULTURA ×5, ASTRA5-MESA-CULTURA / ASTRA5-MESA-DOCUMENTAL ×3, ASTRA5-U4 ×3 ⟨F1 F5 F6⟩

### 🔴 CARRIL-17 · Moral Emotions in Mexico · Declared Dignity · Relational Face · and Residual Catholic Guilt ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 31**: medible en corpus 7 · con adquisición 15 · no medible por diseño 8 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 2 ⟨F1⟩
- **Dominios**: EMOCIONES_MORALES 22 (71%) núcleo · CONFIANZA 3 (10%) · RELIGIOSIDAD 2 (6%) · FAMILIA_CUIDADOS 1 (3%) · RURAL_INDIGENA 1 (3%) · SALUD_MENTAL 1 (3%) · VIOLENCIA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): LATINOBAROMETRO 2 · CCPV 1 · CONEVAL 1 · ENADIS 1 · ENASEM 1 · ENASIC 1 · ENBIARE 1 · ENCUCI 1 · ENDIREH 1 · WVS 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: EMOCIONES_MORALES ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · FAMILIA_CUIDADOS 1449 · RELIGIOSIDAD 404 · SALUD_MENTAL 2758 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 19 / 0 / 15): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 15 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 14 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 14 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-INTERACCION ×8, ASTRA5-MESA-SALUD ×2, ASTRA5-MESA-GENERO ×2 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-INTERACCION ×8, ASTRA5-MESA-SALUD ×2, ASTRA5-MESA-GENERO ×2 ⟨F1 F5 F6⟩

### 🟡 CARRIL-24 · Psicología del Trabajo en México · Un Mapa Basado en Evidencia ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 57**: medible en corpus 5 · con adquisición 34 · no medible por diseño 18 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: TRABAJO 38 (67%) núcleo · CONFIANZA 4 (7%) · GENERO 4 (7%) · JUVENTUD 3 (5%) · CONOCIMIENTO 2 (4%) · RURAL_INDIGENA 2 (4%) · CONSUMO 1 (2%) · POLITICA 1 (2%) · SALUD_MENTAL 1 (2%) · TIEMPO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 5 · OECD 3 · CONEVAL 1 · WVS 1; sin instrumento reconocido: 48 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENOE 3 · OECD 2 · CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TRABAJO (núcleo): 26409 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENOE* 26409 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · CONOCIMIENTO 280 · CONSUMO 4470 · GENERO 7304 · POLITICA 84 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 134 · PASA 2 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 49 / 2 / 94): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 94 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 31 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F8 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 31 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U1 ×31 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟡 CARRIL-15 · La familia mexicana como sistema psicológico · entre el afecto · la obligación y la adaptación económica ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 51**: medible en corpus 8 · con adquisición 32 · no medible por diseño 9 · no construible 2; citan un CALC/RESULT en `gen2_existente`: 9 ⟨F1⟩
- **Dominios**: FAMILIA_CUIDADOS 23 (45%) núcleo · DINERO 6 (12%) · SALUD_MENTAL 5 (10%) · GENERO 4 (8%) · JUVENTUD 4 (8%) · TRABAJO 4 (8%) · CAPITAL_SOCIAL 2 (4%) · RURAL_INDIGENA 1 (2%) · SALUD 1 (2%) · VIOLENCIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIGH 3 · ENOE 3 · ENUT 3 · CCPV 2 · CONEVAL 2 · OECD 2 · SHF 2 · BANXICO 1 · ECCO 1 · EDR 1 · ENASIC 1 · ENDIREH 1 · ENIF 1 · ENSAFI 1 · INTERCENSAL 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CCPV 2 · ENUT 2 · CONEVAL 1 · ENASIC 1 · ENSAFI 1 · OECD 1 · SHF 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - FAMILIA_CUIDADOS (núcleo): 611 · 838 · 0 · 0 — por instrumento (* = el carril lo cita): CCPV* 640, EDER 2, ENADID 679, ENASIC* 98, ENIF* 3, ENIGH* 26, ENUT* 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CAPITAL_SOCIAL 614 · DINERO 100 · GENERO 7304 · SALUD 800 · SALUD_MENTAL 2758 · TRABAJO 26409 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 420 · NO-PASA 229 · PASA 257 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 49 / 1 / 70): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 70 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 6 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENUT) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-FAMILIA ×9, ASTRA5-MESA-SALUD ×4, ASTRA5-U1 ×2 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-13-ENASIC-SPLIT.md`, `2026-09-19-GEN2-ENSAFI-ESTRATEGIAS-CONJUNTAS-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### 🟡 CARRIL-07 · El Efecto Ambiental de la Violencia Crónica en México · Cómo el Miedo Reorganiza la Conducta Psicológica de la Población ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 48**: medible en corpus 14 · con adquisición 21 · no medible por diseño 12 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 8 ⟨F1⟩
- **Dominios**: VIOLENCIA 22 (46%) núcleo · DINERO 8 (17%) · CONFIANZA 5 (10%) · SALUD_MENTAL 5 (10%) · GENERO 4 (8%) · MIGRACION 2 (4%) · AUTORIDAD 1 (2%) · POLITICA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENVIPE 7 · ENSU 5 · SESNSP 2 · BANXICO 1 · ENCIG 1 · ENCOAP 1 · ENVE 1 · LATINOBAROMETRO 1 · OECD 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 5 · ENSU 3 · SESNSP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12634 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU* 12634, ENVIPE* 138 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · DINERO 100 · GENERO 7304 · MIGRACION 126 · POLITICA 84 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12109 · NO-PASA 525 · PASA 146 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 9 / 25 / 2 / 104): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 104 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 18 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F8⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 18 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-VIOLENCIA ×14, ASTRA5-MESA-MIGRACION ×2, ASTRA5-U2 ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENSU) — PARO-PREMISA · P3 → FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-VIOLENCIA ×14, ASTRA5-MESA-MIGRACION ×2, ASTRA5-U2 ×1 ⟨F1 F5 F6⟩

### 🟡 CARRIL-10 · Elegir · Cortejar y Amar en el México de Hoy · Díada de Pareja · Apps de Citas y Cambio en los Guiones de Género ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 46**: medible en corpus 5 · con adquisición 25 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: PAREJA 30 (65%) núcleo · VIOLENCIA 12 (26%) núcleo · GENERO 1 (2%) · MIGRACION 1 (2%) · RELIGIOSIDAD 1 (2%) · SALUD 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): EMAT 6 · ENDIREH 4 · ENADID 2 · ENDISEG 2 · ENOE 2 · CCPV 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EMAT 6 · ENDIREH 4 · ENDISEG 2 · ENOE 2 · ENADID 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - PAREJA (núcleo): 0 · 3304 · 0 · 0 — por instrumento (* = el carril lo cita): EMAT* 3304 ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12634 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU 12634, ENVIPE 138 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12879 · NO-PASA 535 · PASA 3332 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 24 / 2 / 48): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 48 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 6 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` (por ENDIREH) — ACOTAR RESULT-ENDIREH2016-PF-TABLA#4 y #50 (edad 60+, vida y desde oct-2015) en catálogo v1.4 con rótulo «60+  → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-PAREJA ×10, ASTRA5-U2 ×4, ASTRA5-MESA-GENERO ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-03` (por ENDIREH) — PARO-PREMISA: · ENTORNO · ENDIREH 2021 → MESA (2026-10-05) · encargo por escribir: GEN2-ASTRA6-C1-LOTE-4 (767 ENDIREH 2021 -ventana ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md`, `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md`, `2026-09-23-ASTRA5-U2-GENERO-ENDIREH.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩

### 🟡 CARRIL-14 · La arquitectura invisible de la interacción social en México ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 45**: medible en corpus 2 · con adquisición 30 · no medible por diseño 13 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: INTERACCION 14 (31%) núcleo · TRABAJO 9 (20%) núcleo · SALUD_MENTAL 6 (13%) · GENERO 3 (7%) · JUVENTUD 3 (7%) · VIOLENCIA 3 (7%) · EMOCIONES_MORALES 2 (4%) · AUTORIDAD 1 (2%) · CONFIANZA 1 (2%) · HUMOR 1 (2%) · POLITICA 1 (2%) · SANCION_SOCIAL 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENASIC 1 · ENNVIH 1 · ENSU 1 · LAPOP 1 · WVS 1; sin instrumento reconocido: 41 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ninguno ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TRABAJO (núcleo): 26409 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENOE 26409 ⟨F2⟩
  - núcleo sin filas en el catálogo: INTERACCION ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · GENERO 7304 · POLITICA 84 · SALUD_MENTAL 2758 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 134 · PASA 2 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 26 / 1 / 22): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 22 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · SIN-UNION 28 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 28 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-INTERACCION ×9, ASTRA5-MESA-SALUD ×5, ASTRA5-U1 ×3 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md` ⟨F13⟩
- **Frente 2027**: ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-INTERACCION ×9, ASTRA5-MESA-SALUD ×5, ASTRA5-U1 ×3 ⟨F1 F5 F6⟩

### 🟡 CARRIL-01 · Adopción y Resistencia Tecnológica en México · La Paradoja de la Baja Confianza Institucional ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 16 · con adquisición 15 · no medible por diseño 12 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 12 ⟨F1⟩
- **Dominios**: TECNOLOGIA 38 (88%) núcleo · CONFIANZA 2 (5%) · RURAL_INDIGENA 1 (2%) · SALUD 1 (2%) · TRABAJO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENDUTIH 11 · LATINOBAROMETRO 2 · ENADID 1 · OECD 1 · WVS 1; sin instrumento reconocido: 28 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENDUTIH 11 · OECD 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TECNOLOGIA (núcleo): 1827 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENDUTIH* 1578, MOCIBA 249 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · SALUD 800 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 7 / 42 / 7 / 74): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 74 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · SIN-UNION 14 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 14 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U4 ×9, ASTRA5-U3_U4 ×4, ASTRA5-U3 ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U4-TECNOLOGIA.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-U4 ×9, ASTRA5-U3_U4 ×4, ASTRA5-U3 ×1 ⟨F1 F5 F6⟩

### 🟡 CARRIL-06 · El Clasemediero Mexicano · Identidad · Ansiedad de Estatus y el Miedo Racional a Caer ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 4 · con adquisición 24 · no medible por diseño 15 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: MOVILIDAD 25 (58%) núcleo · POLITICA 5 (12%) · CONOCIMIENTO 4 (9%) · SALUD_MENTAL 4 (9%) · DINERO 3 (7%) · CONSUMO 1 (2%) · TRABAJO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENBIARE 3 · ENIGH 3 · CEEY_EMOVI 1 · CNBV 1 · CONEVAL 1 · ENOE 1 · IECM 1 · MMSI 1; sin instrumento reconocido: 31 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIGH 3 · ENBIARE 2 · CEEY_EMOVI 1 · CONEVAL 1 · MMSI 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI* 158 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONOCIMIENTO 280 · CONSUMO 4470 · DINERO 100 · POLITICA 84 · SALUD_MENTAL 2758 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 1): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 425 · NO-PASA 6 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 15 / 4 / 41): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 41 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 3 · SIN-UNION 16 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (4) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 16 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MOVILIDAD ×7, ASTRA5-MESA-CONOCIMIENTO ×4, ASTRA5-U3 ×3 ⟨F1 F5 F6⟩
    - `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` — estado OBTENIDO-PARCIAL; prioridad 3; afirmaciones 1; origen MAESTRA38-N6 (propaga FP-298, disena MAESTRA38-N5 #3 dinero. → caja (completa el payload) ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟡 CARRIL-20 · Psicología Política y Comportamiento Cívico del Mexicano Contemporáneo · Una Lectura Anti-Esencialista desde Abajo · 2026 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 30% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 18 · con adquisición 14 · no medible por diseño 11 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 17 ⟨F1⟩
- **Dominios**: POLITICA 40 (93%) núcleo · CONFIANZA 2 (5%) · VIOLENCIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENVIPE 8 · ENCIG 6 · ENEM 3 · LAPOP 2 · LATINOBAROMETRO 2 · WVS 2 · CSES 1 · MMSI 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 7 · ENCIG 6 · ENEM 3 · LATINOBAROMETRO 2 · CSES 1 · LAPOP 1 · MMSI 1 · WVS 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - POLITICA (núcleo): 16 · 68 · 0 · 0 — por instrumento (* = el carril lo cita): ENCUCI 2, ENVIPE* 14, LATINOBAROMETRO* 68 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (10; encabezados excluidos 0): MATIZA 2 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 7; con dictamen distinto de SIN-CIFRA-GEN2 30% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 230 · PASA 148 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 6 / 16 / 4 / 34): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 34 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 13 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `CSES 2016` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×1; afirmaciones que la citan: 1 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito ⟨F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 13 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×13 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
    - `NC-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` (por ENCIG) — PARO-PREMISA · P3 (canal completo): 16 celdas de GOB.gobierno_digital.encig2025.edad_x_sexo + . → MESA (2026-10-05) · cerrable al fusionar el [deriva] o su acto: EN-CURSO [canal [deriva] · ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md`, `2026-09-23-ASTRA5-U3-POLITICA.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

### 🟡 CARRIL-19 · Non-Family Social Capital in Mexico · Cooperation · Trust · and Collective Action Beyond Kinship ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 44% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 42**: medible en corpus 13 · con adquisición 13 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 11 ⟨F1⟩
- **Dominios**: CAPITAL_SOCIAL 24 (57%) núcleo · RURAL_INDIGENA 5 (12%) · AUTORIDAD 3 (7%) · DINERO 3 (7%) · CONFIANZA 2 (5%) · RELIGIOSIDAD 2 (5%) · VIOLENCIA 2 (5%) · TECNOLOGIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 5 · ENVIPE 3 · CAAS 1 · CONDUSEF 1 · ENADIS 1 · ENSAFI 1 · ENUT 1 · LAPOP 1; sin instrumento reconocido: 29 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCUCI 5 · ENSAFI 1 · ENUT 1 · ENVIPE 1 · LAPOP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CAPITAL_SOCIAL (núcleo): 0 · 614 · 0 · 0 — por instrumento (* = el carril lo cita): LAPOP* 614 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · DINERO 100 · RELIGIOSIDAD 404 · TECNOLOGIA 1827 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (9; encabezados excluidos 0): MATIZA 1 · MATIZA-SIN-CRUCE 3 · SIN-CIFRA-GEN2 5; con dictamen distinto de SIN-CIFRA-GEN2 44% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 4 · PASA 301 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 5 / 0 / 83): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 83 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · SIN-UNION 12 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENCUCI, ENUT) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 12 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RURAL ×6, ASTRA5-MESA-CAPITAL_SOCIAL ×3, ASTRA5-U3 ×2 ⟨F1 F5 F6⟩
    - `CONDUSEF-REDECO_SERIE` — estado OBTENIDO-PARCIAL; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-CRFAC-005 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `CONDUSEF_CNBV_TANDAS_FUERA_DE_PERIMETRO` — estado NO-ENCONTRADO; prioridad —; afirmaciones 1; origen gen2-universo-c → acto de nube (/sonda) ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md`, `2026-09-19-GEN2-ENSAFI-ESTRATEGIAS-CONJUNTAS-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### 🟡 CARRIL-25 · Psychology of Mexico-US Migration · Identity · Family · Aspiration · and Wellbeing in 2025 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 42**: medible en corpus 4 · con adquisición 17 · no medible por diseño 20 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: MIGRACION 42 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENADID 7 · BANXICO 2 · ENIGH 2 · PEW 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENADID 7 · BANXICO 2 · ENIGH 2 · PEW 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MIGRACION (núcleo): 0 · 126 · 0 · 0 — por instrumento (* = el carril lo cita): PEW* 126 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 55 · NO-PASA 2 · PASA 105 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 19 / 1 / 48): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 48 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MIGRACION ×15 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-MIGRACION ×15 ⟨F1 F5 F6⟩

### 🟡 CARRIL-12 · Health · Body · Food and Substance Use in Mexico · The Behavioral Layer of Decisions · Environment and Structure ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 39**: medible en corpus 11 · con adquisición 22 · no medible por diseño 6 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: SALUD 32 (82%) núcleo · CONSUMO 7 (18%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENSANUT 13 · ENCODAT 7 · CONEVAL 1 · ENADID 1 · ENCUCI 1 · ENOE 1 · LAPOP 1; sin instrumento reconocido: 16 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENSANUT 11 · ENCODAT 7 · CONEVAL 1 · ENADID 1 · ENCUCI 1 · ENOE 1 · LAPOP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - SALUD (núcleo): 2 · 798 · 0 · 0 — por instrumento (* = el carril lo cita): ENCODAT* 130, ENSANUT* 670 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 400 · PASA 99 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 15 / 0 / 35): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 35 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 10 · SIN-UNION 12 ⟨F1 F5 F6⟩
- **Stoppers** (7): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENCUCI) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **RESERVA** (4) ⟨F12 F6 F15⟩
    - `ENCODAT 2025` — manifiesto estado_reserva: DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS ×5; RESERVADA-NO-ABIERTA-NO-INDEXAR-L ×3; afirmaciones que la citan: 7 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito; expediente forense/prereg-aperturas/ENCODAT-2025 (CODIGO-CONGELADO del expediente ENCODAT-) ⟨F6⟩
    - `ENOE 2026` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×2; RESERVADA-NO-ABIERTA-NO-INDEXAR-L ×1; afirmaciones que la citan: 1 → familia 2027 ENOE-INFORMALIDAD; expediente forense/prereg-aperturas/ENOE-2026T2 (CODIGO-CONGELADO del expediente ENOE-202) ⟨F6⟩
    - `ENOE 2026T2` — tabla-final olas_reservadas_al_entrar; afirmaciones que la citan: 1 → familia 2027 ENOE-INFORMALIDAD; expediente forense/prereg-aperturas/ENOE-2026T2 (CODIGO-CONGELADO del expediente ENOE-202) ⟨F12⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 12 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×12 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md`, `2026-09-17-GEN2-ADQ-HANDOFF-RESULTADO-Y-SALUD-1-ENCARGO.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` … y 1 más ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### 🟡 CARRIL-29 · Salud Mental en México · Prevalencia · Estigma y la Brecha entre Necesidad y Atención ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 39**: medible en corpus 6 · con adquisición 23 · no medible por diseño 9 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 5 ⟨F1⟩
- **Dominios**: SALUD_MENTAL 22 (56%) núcleo · GENERO 3 (8%) · JUVENTUD 3 (8%) · MIGRACION 2 (5%) · RELIGIOSIDAD 2 (5%) · TECNOLOGIA 2 (5%) · VIOLENCIA 2 (5%) · EMOCIONES_MORALES 1 (3%) · FAMILIA_CUIDADOS 1 (3%) · RURAL_INDIGENA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENSANUT 4 · EDR 2 · ENDUTIH 2 · ENIGH 2 · ENCOVID 1 · ENNVIH 1; sin instrumento reconocido: 28 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EDR 2 · ENSANUT 2 · ENCOVID 1 · ENIGH 1 · ENNVIH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - SALUD_MENTAL (núcleo): 180 · 2578 · 0 · 0 — por instrumento (* = el carril lo cita): EDR* 2578, ENBIARE 180 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · TECNOLOGIA 1827 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 541 · NO-PASA 6 · PASA 2291 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 36 / 2 / 68): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 68 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×15, ASTRA5-MESA-GENERO ×2, ASTRA5-U0 ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-SALUD ×15, ASTRA5-MESA-GENERO ×2, ASTRA5-U0 ×1 ⟨F1 F5 F6⟩

### 🟡 CARRIL-18 · Mérito · Movilidad Social y Desigualdad en México · Actualización 2025-2026 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 6 · con adquisición 22 · no medible por diseño 6 · no construible 4; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: MOVILIDAD 22 (58%) núcleo · CONFIANZA 5 (13%) · DINERO 3 (8%) · JUVENTUD 2 (5%) · TRABAJO 2 (5%) · CONSUMO 1 (3%) · GENERO 1 (3%) · MIGRACION 1 (3%) · POLITICA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): CEEY_EMOVI 8 · ENCIG 3 · ENIGH 3 · MMSI 3 · ENOE 2 · BANXICO 1 · ENADIS 1 · LATINOBAROMETRO 1 · OECD 1 · WVS 1; sin instrumento reconocido: 15 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CEEY_EMOVI 8 · MMSI 3 · ENIGH 2 · ENADIS 1 · LATINOBAROMETRO 1 · WVS 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI* 158 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · CONSUMO 4470 · DINERO 100 · GENERO 7304 · MIGRACION 126 · POLITICA 84 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 245 · NO-PASA 2 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 3 / 26 / 0 / 54): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 54 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 7 · EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 10 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7 F12 F15⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 2) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 10 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MOVILIDAD / ASTRA5-MESA-DOCUMENTAL ×4, ASTRA5-U1 ×2, ASTRA5-MESA-ECONOMIA ×2 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 7; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 7; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

### 🟡 CARRIL-23 · Psicología del Consumidor Mexicano · Patrones · Contradicciones y Estrategia ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 40% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 5 · con adquisición 23 · no medible por diseño 10 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: CONSUMO 25 (66%) núcleo · DINERO 9 (24%) núcleo · TECNOLOGIA 2 (5%) · CONFIANZA 1 (3%) · JUVENTUD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 3 · ENDUTIH 2 · ENIGH 2 · BANXICO 1 · WVS 1; sin instrumento reconocido: 29 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 3 · ENIGH 2 · BANXICO 1 · ENDUTIH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONSUMO (núcleo): 0 · 4470 · 0 · 0 — por instrumento (* = el carril lo cita): ENGASTO 330, ENIGH* 4140 ⟨F2⟩
  - DINERO (núcleo): 68 · 32 · 0 · 0 — por instrumento (* = el carril lo cita): ENFIH 2, ENIF* 97, ENNVIH 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · TECNOLOGIA 1827 ⟨F2⟩
- **Reglas del report** (5; encabezados excluidos 1): CONFIRMA 1 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 40% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 6 · NO-PASA 3 · PASA 18 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 69 / 0 / 144): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 144 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `ENDUTIH 2025` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×1; afirmaciones que la citan: 1 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito; expediente forense/prereg-aperturas/ENDUTIH-2025 (SOLO-MESA-POR-ESCRITO (sin contendiente ) ⟨F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CONSUMO ×14, ASTRA5-MESA-DINERO ×3, ASTRA5-MESA-DIGITAL ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `ENDUTIH 2025` → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito; expediente forense/prereg-aperturas/ENDUTIH-2025 (SOLO-MESA-POR-ESCRITO (sin contendiente ) ⟨F6⟩

### 🟡 CARRIL-27 · Religiosidad y Psicología del Mexicano Contemporáneo · Moral · Afrontamiento · Consumo e Identidad en Transformación ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 4 · con adquisición 22 · no medible por diseño 9 · no construible 3; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: RELIGIOSIDAD 28 (74%) núcleo · CONSUMO 3 (8%) · POLITICA 3 (8%) · SALUD_MENTAL 2 (5%) · GENERO 1 (3%) · MIGRACION 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): PEW 5 · CCPV 2 · TEPJF 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): PEW 5 · CCPV 2 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - RELIGIOSIDAD (núcleo): 0 · 404 · 0 · 0 — por instrumento (* = el carril lo cita): LATINOBAROMETRO 34, PEW* 237, WVS 133 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 · GENERO 7304 · MIGRACION 126 · POLITICA 84 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 451 · NO-PASA 227 · PASA 6 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 106 / 4 / 47): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 47 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 19 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 19 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RELIGION ×16, ASTRA5-MESA-MIGRACION ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-RELIGION ×16, ASTRA5-MESA-MIGRACION ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩

### 🟡 CARRIL-28 · Report 26 · The Contemporary Mexican and Knowledge · Expertise · Education and Information as Decision Behavior ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 22% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 3 · con adquisición 19 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: CONOCIMIENTO 17 (45%) núcleo · SALUD 8 (21%) núcleo · CONFIANZA 6 (16%) · TECNOLOGIA 3 (8%) · TRABAJO 3 (8%) · RURAL_INDIGENA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): OECD 4 · ENPECYT 3 · ENSANUT 3 · PISA 3 · ENDUTIH 2 · ENOE 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 24 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): OECD 4 · ENPECYT 3 · PISA 3 · ENSANUT 2 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONOCIMIENTO (núcleo): 0 · 280 · 0 · 0 — por instrumento (* = el carril lo cita): ENPECYT* 280 ⟨F2⟩
  - SALUD (núcleo): 2 · 798 · 0 · 0 — por instrumento (* = el carril lo cita): ENCODAT 130, ENSANUT* 670 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (9; encabezados excluidos 0): MATIZA 1 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 7; con dictamen distinto de SIN-CIFRA-GEN2 22% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 450 · PASA 90 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 5 / 28 / 2 / 99): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 99 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 9 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CONOCIMIENTO ×5, ASTRA5-MESA-CONOCIMIENTO / ASTRA5-MESA-DOCUMENTAL ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md`, `2026-09-17-GEN2-ADQ-HANDOFF-RESULTADO-Y-SALUD-1-ENCARGO.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟡 CARRIL-31 · Vejez y Cuidado Intergeneracional en México · El Debilitamiento del Seguro Familiar ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 25% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 9 · con adquisición 24 · no medible por diseño 5 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: FAMILIA_CUIDADOS 15 (39%) núcleo · TRABAJO 5 (13%) · DINERO 4 (11%) · SALUD 4 (11%) · SALUD_MENTAL 4 (11%) · MIGRACION 2 (5%) · CONSUMO 1 (3%) · GENERO 1 (3%) · RURAL_INDIGENA 1 (3%) · TIEMPO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENASEM 5 · ENOE 3 · CCPV 2 · ENUT 2 · CONEVAL 1 · ENADID 1 · ENIGH 1; sin instrumento reconocido: 23 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CCPV 2 · ENADID 1 · ENIGH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - FAMILIA_CUIDADOS (núcleo): 611 · 838 · 0 · 0 — por instrumento (* = el carril lo cita): CCPV* 640, EDER 2, ENADID* 679, ENASIC 98, ENIF 3, ENIGH* 26, ENUT* 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 · DINERO 100 · GENERO 7304 · MIGRACION 126 · SALUD 800 · SALUD_MENTAL 2758 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): MATIZA 1 · SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 25% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 420 · NO-PASA 229 · PASA 101 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 42 / 0 / 86): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 86 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 6 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 16 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 16 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-VEJEZ ×13, ASTRA5-MESA-SALUD ×3 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟡 CARRIL-04 · Behavioral Finance Mexicano · Estructura · Adaptación Racional y Cultura en el Ahorro · Crédito y Riesgo ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 33% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 35**: medible en corpus 18 · con adquisición 6 · no medible por diseño 10 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 11 ⟨F1⟩
- **Dominios**: DINERO 30 (86%) núcleo · CONFIANZA 3 (9%) · CONSUMO 1 (3%) · GENERO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 10 · ENAFI 1; sin instrumento reconocido: 25 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 9 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - DINERO (núcleo): 68 · 32 · 0 · 0 — por instrumento (* = el carril lo cita): ENFIH 2, ENIF* 97, ENNVIH 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · CONSUMO 4470 · GENERO 7304 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 33% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 1 · NO-PASA 1 · PASA 7 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 24 / 5 / 64): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 64 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): SIN-UNION 6 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 6 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-DINERO ×6 ⟨F1 F5 F6⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-DINERO ×6 ⟨F1 F5 F6⟩

### 🟡 CARRIL-05 · Confianza y Desconfianza en México · Anatomía Psicológica de una Sociedad Dual ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 6 · con adquisición 17 · no medible por diseño 7 · no construible 3; citan un CALC/RESULT en `gen2_existente`: 7 ⟨F1⟩
- **Dominios**: CONFIANZA 19 (58%) núcleo · CAPITAL_SOCIAL 4 (12%) · DINERO 4 (12%) · AUTORIDAD 3 (9%) · GENERO 1 (3%) · JUVENTUD 1 (3%) · TRABAJO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCIG 4 · WVS 3 · ENVIPE 2 · LAPOP 2 · OECD 2 · BANXICO 1 · CNBV 1 · ENIF 1 · ENSI 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 18 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCIG 4 · WVS 3 · ENVIPE 2 · OECD 2 · ENSI 1 · LAPOP 1 · LATINOBAROMETRO 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONFIANZA (núcleo): 28 · 798 · 0 · 0 — por instrumento (* = el carril lo cita): ENCIG* 6, ENCUCI 3, ENVIPE* 15, INSTRUMENTO-NO-IDENTIFICADO 4, LATINOBAROMETRO* 323, WVS* 475 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CAPITAL_SOCIAL 614 · DINERO 100 · GENERO 7304 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 72 · PASA 147 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 150 / 6 / 201): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 201 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 3 · SIN-UNION 11 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 11 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×8, ASTRA5-MESA-CONFIANZA ×1, ASTRA5-U2 ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` (por ENCIG) — PARO-PREMISA · P3 (canal completo): 16 celdas de GOB.gobierno_digital.encig2025.edad_x_sexo + . → MESA (2026-10-05) · cerrable al fusionar el [deriva] o su acto: EN-CURSO [canal [deriva] · ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

### 🟡 CARRIL-26 · Reconfiguración de los Guiones de Género en México · Masculinidades · Feminidades y Violencia a través de Clase · Generación y Región ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 9 · con adquisición 18 · no medible por diseño 6 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 10 ⟨F1⟩
- **Dominios**: GENERO 12 (36%) núcleo · VIOLENCIA 7 (21%) núcleo · TRABAJO 5 (15%) · POLITICA 3 (9%) · FAMILIA_CUIDADOS 2 (6%) · MIGRACION 1 (3%) · PAREJA 1 (3%) · RURAL_INDIGENA 1 (3%) · TECNOLOGIA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 3 · ENCUCI 2 · ENDIREH 2 · ENUT 2 · SESNSP 2 · ENADID 1 · ENADIS 1 · ENCUP 1 · ENDUTIH 1 · ENNVIH 1 · LAPOP 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 20 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENDIREH 2 · SESNSP 2 · ENADIS 1 · ENCUCI 1 · ENCUP 1 · LAPOP 1 · LATINOBAROMETRO 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - GENERO (núcleo): 7304 · 0 · 7 · 689 — por instrumento (* = el carril lo cita): ENDIREH* 6880, ENDISEG 424 ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12634 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU 12634, ENVIPE 138 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): FAMILIA_CUIDADOS 1449 · MIGRACION 126 · PAREJA 3304 · POLITICA 84 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12582 · NO-PASA 535 · PASA 160 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 8 / 16 / 1 / 93): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 93 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` (por ENDIREH) — ACOTAR RESULT-ENDIREH2016-PF-TABLA#4 y #50 (edad 60+, vida y desde oct-2015) en catálogo v1.4 con rótulo «60+  → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENCUCI) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U2 ×7, ASTRA5-MESA-GENERO ×4, ASTRA5-U3 ×2 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-03` (por ENDIREH) — PARO-PREMISA: · ENTORNO · ENDIREH 2021 → MESA (2026-10-05) · encargo por escribir: GEN2-ASTRA6-C1-LOTE-4 (767 ENDIREH 2021 -ventana ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U2-GENERO-ENDIREH.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩

### 🟡 CARRIL-21 · Psicología · Conducta y Sociedad en el México Contemporáneo · Análisis Transcultural y Estructural ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 28**: medible en corpus 1 · con adquisición 21 · no medible por diseño 4 · no construible 2; citan un CALC/RESULT en `gen2_existente`: 1 ⟨F1⟩
- **Dominios**: MOVILIDAD 4 (14%) núcleo · SALUD_MENTAL 4 (14%) núcleo · CONOCIMIENTO 3 (11%) · INTERACCION 3 (11%) · TRABAJO 3 (11%) · GENERO 2 (7%) · RURAL_INDIGENA 2 (7%) · CONFIANZA 1 (4%) · DINERO 1 (4%) · EMOCIONES_MORALES 1 (4%) · FAMILIA_CUIDADOS 1 (4%) · MIGRACION 1 (4%) · POLITICA 1 (4%) · VIOLENCIA 1 (4%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 2 · CCPV 1 · CEEY_EMOVI 1 · CONEVAL 1 · ENUT 1 · OECD 1 · SESNSP 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CEEY_EMOVI 1 · CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI 158 ⟨F2⟩
  - SALUD_MENTAL (núcleo): 180 · 2578 · 0 · 0 — por instrumento (* = el carril lo cita): EDR 2578, ENBIARE 180 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · CONOCIMIENTO 280 · DINERO 100 · FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · POLITICA 84 · TRABAJO 26409 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (0; encabezados excluidos 0): ninguna; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 708 · NO-PASA 4 · PASA 2290 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 61 / 22 / 20): EN-MAIN · recibo pr-1247 · regla adoptada: No acreditada aquí · reserva material: 20 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 17 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (5) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 17 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×3, ASTRA5-MESA-INTERACCION ×2, ASTRA5-MESA-FAMILIA ×2 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟠 CARRIL-09 · El México Rural e Indígena en sus Propios Términos · Comunalidad · Autoridad y Reciprocidad como Sistemas con Lógica Propia ⟨F1 F14⟩

- **Semáforo NARANJA** — núcleo con cifra adoptada 0/1 y piso sellado registrado pendiente de adopción en 1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 49**: medible en corpus 7 · con adquisición 23 · no medible por diseño 19 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 5 ⟨F1⟩
- **Dominios**: RURAL_INDIGENA 38 (78%) núcleo · SALUD 5 (10%) · MIGRACION 3 (6%) · RELIGIOSIDAD 2 (4%) · GENERO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENUT 4 · CONEVAL 2 · ENIGH 2 · CAAS 1 · ENADID 1 · ENASEM 1 · ENASIC 1 · ENDIREH 1 · ENSANUT 1; sin instrumento reconocido: 38 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENUT 3 · CONEVAL 2 · ENASEM 1 · ENASIC 1 · ENIGH 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: RURAL_INDIGENA: CALC-MC2-ENSANUT2024-0001, CALC-PDR1-ENADID2023-0001, CALC-PDR1-ENUT2024-0001; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: RURAL_INDIGENA ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 19 · NO-PASA 2 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 5 / 21 / 2 / 32): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 32 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENUT) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U5 ×18, ASTRA5-MESA-RURAL ×2 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-13-ENASIC-SPLIT.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### 🟠 CARRIL-08 · El Mexicano y el Tiempo · Estructura · no Cultura · en la Planeación y el Compromiso Temporal ⟨F1 F14⟩

- **Semáforo NARANJA** — núcleo con cifra adoptada 0/1 y piso sellado registrado pendiente de adopción en 1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 12 · con adquisición 12 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 7 ⟨F1⟩
- **Dominios**: TIEMPO 18 (47%) núcleo · TRABAJO 4 (11%) · DINERO 3 (8%) · MOVILIDAD 3 (8%) · VIOLENCIA 3 (8%) · INTERACCION 2 (5%) · CONFIANZA 1 (3%) · CONSUMO 1 (3%) · GENERO 1 (3%) · JUVENTUD 1 (3%) · SALUD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 1 · ENOE 1 · ENUT 1; sin instrumento reconocido: 35 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 1 · ENUT 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: TIEMPO: CALC-MC2-ENIF2024-0001, CALC-PDR1-ENUT2024-0001; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: TIEMPO ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · CONSUMO 4470 · DINERO 100 · GENERO 7304 · MOVILIDAD 172 · SALUD 800 · TRABAJO 26409 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (7; encabezados excluidos 2): MATIZA 1 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 5; con dictamen distinto de SIN-CIFRA-GEN2 29% ⟨F3⟩
- **Validación ciega**: PASA 7 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 10 / 5 / 29): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 29 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 5 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENUT) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 2) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U1 ×7 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → MESA (2026-10-05) · encargo por escribir (decidida por delegación: decididas-por-delegacio ⟨F8⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### 🟠 CARRIL-22 · Psicología de la Juventud Mexicana Contemporánea · Gen Z y Millennials Jóvenes como Cohorte Divergente ⟨F1 F14⟩

- **Semáforo NARANJA** — núcleo con cifra adoptada 0/1 y piso sellado registrado pendiente de adopción en 1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 32**: medible en corpus 9 · con adquisición 14 · no medible por diseño 8 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 8 ⟨F1⟩
- **Dominios**: JUVENTUD 10 (31%) núcleo · POLITICA 4 (12%) · TRABAJO 4 (12%) · GENERO 3 (9%) · SALUD_MENTAL 3 (9%) · AUTORIDAD 2 (6%) · FAMILIA_CUIDADOS 2 (6%) · TECNOLOGIA 2 (6%) · PAREJA 1 (3%) · RELIGIOSIDAD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): EDER 3 · ENADID 3 · ENOE 3 · ENDUTIH 2 · OECD 2 · EDR 1 · ENCODAT 1 · ENDISEG 1 · ENSANUT 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 14 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EDER 3 · ENADID 3 · OECD 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: JUVENTUD: CALC-MC2-ENOE-0001; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: JUVENTUD ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): FAMILIA_CUIDADOS 1449 · GENERO 7304 · PAREJA 3304 · POLITICA 84 · RELIGIOSIDAD 404 · SALUD_MENTAL 2758 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 8 · PASA 94 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 10 / 4 / 26): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 26 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×3, ASTRA5-MESA-JUVENTUD ×2, ASTRA5-MESA-GENERO ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-EDER-PRIMERA-UNION-SEXO-COHORTE.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

### 🟠 CARRIL-03 · Autoridad y jerarquía en el México contemporáneo · anatomía psicológica de un sistema dual ⟨F1 F14⟩

- **Semáforo NARANJA** — núcleo con cifra adoptada 0/1 y piso sellado registrado pendiente de adopción en 1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 30**: medible en corpus 9 · con adquisición 10 · no medible por diseño 11 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: AUTORIDAD 29 (97%) núcleo · POLITICA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 3 · LATINOBAROMETRO 2 · CEEY_EMOVI 1 · WVS 1; sin instrumento reconocido: 23 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCUCI 3 · LATINOBAROMETRO 2 · CEEY_EMOVI 1 · WVS 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: AUTORIDAD: CALC-PDR1-ENCUCI2020-0002; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: AUTORIDAD ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): POLITICA 84 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 68 · PASA 3 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 16 / 1 / 41): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 41 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · EN-MANIFIESTO 1 · SIN-UNION 8 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (3) ⟨F7⟩
    - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (por ENCUCI) — §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, m → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 8 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×6, ASTRA5-MESA-MOVILIDAD ×1, ASTRA5-MESA-EMPRESA ×1 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` → mesa firma; encargo 2026-09-28-GEN2-TUBERIA-TABLERO-INSUMOS-1.md ⟨F7⟩

### ⚪ CARRIL-11 · Genetica y Conducta del Mexicano Contemporaneo · Canal Individual vs · Estructura ⟨F1 F14⟩

- **Semáforo GRIS** — dominio GENETICA fuera por firewall genético ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 0 · con adquisición 35 · no medible por diseño 3 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: GENETICA 38 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ninguno del vocabulario; sin instrumento reconocido: 38 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ninguno ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3**: ningún dominio del carril tiene filas en el catálogo ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 4 / 22 / 8 / 9): EN-MAIN · recibo pr-1251 · regla adoptada: No acreditada aquí · reserva material: 9 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 34 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 34 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL ×34 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL ×34 ⟨F1 F5 F6⟩

### ⚪ CARRIL-16 · Mexican Population Genomics · 2025-2026 Scientific and Market Opportunity Update ⟨F1 F14⟩

- **Semáforo GRIS** — dominio GENOMICA fuera por firewall genético ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 0 · con adquisición 26 · no medible por diseño 6 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: GENOMICA 33 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): MCPS 2 · PEW 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): MCPS 2 · PEW 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.3**: ningún dominio del carril tiene filas en el catálogo ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 44 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 14 / 4 / 15): EN-MAIN · recibo pr-1251 · regla adoptada: No acreditada aquí · reserva material: 15 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · SIN-UNION 24 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por MCPS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por MCPS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **ADQUISICION** (2) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 24 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-GENOMICA ×11, ASTRA5-MESA-LEGAL ×6, ASTRA5-MESA-MERCADO ×4 ⟨F1 F5 F6⟩
    - `MCPS_SIN-OLA` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 2; origen ASTRA5-U0 ASTRA5-U0-GENBEH-010 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

### ⚪ CARRIL-30 · Sanción Social Horizontal en México · Chisme · Envidia y Mal de Ojo como Mecanismos de Nivelación ⟨F1 F14⟩

- **Semáforo GRIS** — NO-MEDIBLE-POR-DISEÑO 64% > 50% ⟨F1 F2 F3 S⟩
- **Afirmaciones 22**: medible en corpus 3 · con adquisición 5 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: SANCION_SOCIAL 11 (50%) núcleo · INTERACCION 2 (9%) · TRABAJO 2 (9%) · CONFIANZA 1 (5%) · DINERO 1 (5%) · GENERO 1 (5%) · JUVENTUD 1 (5%) · MIGRACION 1 (5%) · RURAL_INDIGENA 1 (5%) · VIOLENCIA 1 (5%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENADID 1 · ENSU 1 · ENVE 1 · ENVIPE 1 · LATINOBAROMETRO 1 · MOCIBA 1; sin instrumento reconocido: 16 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENSU 1 · ENVE 1 · MOCIBA 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: SANCION_SOCIAL: CALC-PDR1-ENSU2024-0001; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: SANCION_SOCIAL ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 826 · DINERO 100 · GENERO 7304 · MIGRACION 126 · TRABAJO 26409 · VIOLENCIA 12772 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12105 · NO-PASA 525 · PASA 4 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 11 / 0 / 18): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 18 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 4 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F8⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 4 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RURAL ×2, ASTRA5-MESA-ESTATUS ×1, ASTRA5-MESA-INTERACCION ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENSU) — PARO-PREMISA · P3 → FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-MOCIBA-FLUJO-DOCUMENTAL-1.md` ⟨F13⟩
- **Frente 2027**: ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-RURAL ×2, ASTRA5-MESA-ESTATUS ×1, ASTRA5-MESA-INTERACCION ×1 ⟨F1 F5 F6⟩

## Cadena de procedencia

Todo número de arriba sale de estos archivos por `python3 tools/tablero_carriles.py --json`; «blob» es el `git hash-object` del contenido leído (la salida no depende de HEAD ni de la fecha). El crosswalk F14 se escribe con `--crosswalk` y `--verifica` lo compara.

| clave | archivo | blob | lector | filas leídas |
|---|---|---|---|---:|
| F1 | `canon/mapa-dominios-v1_2.tsv` | `14210b7f869a` | lee_tsv (csv.DictReader), filas con report corpus/reports/* | 1396 |
| F2 | `canon/catalogo-del-mexicano-v1_3.tsv` | `dfd6c29a4e9a` | lee_tsv, agrega por (dominio, instrumento, estado_adopcion) | 63706 |
| F3 | `canon/reglas-contrastadas-v1_0.tsv` | `422256e0be14` | lee_tsv, report = basename(fuentes) | 162 |
| F4 | `corpus/reports-v2/INDICE.md` | `cf3d1a1fa04d` | indice(): filas de la tabla markdown | 31 |
| F5 | `data/cola-adquisicion-v1_0.tsv` | `e96592d42f57` | lee_tsv (salta líneas #) | 952 |
| F6 | `data/manifiesto.yaml` | `d8ac4943b224` | manifiesto(): campos id y estado_reserva por línea | 7198 |
| F7 | `forense/firmas-pendientes.tsv` | `c60fe4c8ed18` | lee_tsv, estado ABIERTA* | 654 |
| F8 | `forense/no-corrido.tsv` | `eb96cf18147c` | lee_tsv, estado ABIERTA*, razón PARO-PREMISA*/PARO-ENTORNO* | 1102 |
| F9 | `data/corrida0/demanda-dictamen-v1_0.tsv` | `59ab68b09e08` | lee_tsv, dictamen SIN-BASE-GEN2 / ESPERA-* | 341 |
| F10 | `data/corrida0/validaciones-independientes.tsv` | `b7b72fc00114` | lee_tsv, join resultado_id → catálogo.result_id | 21266 |
| F11 | `forense/analisis/familias-2027/familias-2027-estado-v1_1.tsv` | `e8bfab28c374` | lee_tsv | 8 |
| F12 | `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` | `4a647dd37503` | lee_tsv, programa y olas_reservadas_al_entrar | 146 |
| F13 | `forense/encargos/*.md` | `a851dda028ca (lista)` | glob; en vuelo = sin línea «## CONSUMIDO» | 818 |
| F15 | `data/corrida0/aperturas-pendientes-v1_0.tsv` | `4c7f99590390` | lee_tsv, (programa, año de ola) -> expediente y qué la abre | — |
| F16 | `forense/analisis/*/*dictamenes.tsv` | `cd78601b716d (lista)` | pisos_pendientes(): glob; filas con dominio · calc · resultado_id | 74 |
| F17 | `data/corrida0/resultados.tsv` | `c8eb7a535433` | pisos_pendientes(): conjunto de resultado_id registrados (salta líneas #) | — |
| F14 | `canon/crosswalk-carriles-v1_0.tsv` | `9539d131abd1` | crosswalk() (misma derivación; --verifica compara con el archivo) | 31 |
| S | `tools/tablero_carriles.py` | `c23b28762de9` | constantes de la cabecera | — |
<!-- TABLERO-DERIVADO:END -->
