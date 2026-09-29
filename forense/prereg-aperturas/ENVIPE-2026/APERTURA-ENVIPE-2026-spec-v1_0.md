# Expediente de apertura · ENVIPE 2026 (reserva restante) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: lo que no leyeron los duelos
sellados sigue RESERVADO (E.6; firma FP-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-b05c-01: «lo que no emita este CALC
sigue RESERVADA»); lo levanta el código congelado de este expediente, en caja, en el commit que mesa autorice.
Sirve a **dos** contendientes sellados antes de abrir (E.6: «una apertura sirve a todos los contendientes que se
sellaron antes»), con **una sola** comparación primaria (§4).

## 0 · Premisas

- [EJECUTADO] Id de la ola en `data/manifiesto.yaml` (lector YAML, filtro por id): `envipe2026_csv` (datos abiertos CSV,
  sha256 `dd79f589…`, «no inspeccionado, solo hasheado»), **sin** `estado_reserva` en el campo; la reserva vive en
  `data/corrida0/decisiones.tsv` (`reserva:envipe2026`) y en la firma citada arriba. Vista
  `data/corrida0/aperturas-pendientes-v1_0.tsv`: `PREMISA-CAIDA-YA-ABIERTA` (apertura PARCIAL, abajo).
- [LEÍDO] Contendiente 1 (regla 6: ninguno nuevo): `CALC-ENVIPE-PERCEPCION-2024-0001` — piso ENVIPE 2024 con IC de
  diseño (bootstrap de UPM, 2 000 réplicas), 3 conductas × {TOTAL, SEXO, EDAD, ESCOLARIDAD, DOMINIO, ENTIDAD}; etiqueta
  «2024 abierta; 2026 RESERVADA (E.6), no es input»; ejecución 2026-09-26T18:51Z. Spec humana:
  `forense/prereg-caja/COLA-ENVIPE-PERCEPCION-spec-v1_0.md`. Publica P, EE, IC-LO, IC-HI, N; sin IC de persistencia.
- [LEÍDO] Contendiente 2: `CALC-MC2-ENVIPE2025-0001` (`spec.yaml` l.14 «ola_reservada: ENVIPE 2026 (no es input)»; tipo
  `PISO-DESCRIPTIVO-RETROSPECTIVO`; COMMIT-1 `f7ea93f4` 2026-09-28T17:52-06:00, ejecución 2026-09-28T23:57Z; spec humana
  `forense/prereg-caja/MC2-ENVIPE2025-spec-v1_0.md`). Medidor sellado (sha256 `6cfd637b…`) y `resultados.json` (sha256
  `d004f24f…`): 205 celdas con `-P`, `-IC95-INF`, `-IC95-SUP` (bootstrap de UPM dentro de estrato, 2 000 réplicas,
  `PCG64(42)`, percentiles 2.5/97.5) y `-N`, más 15 `DIAG-*`. Celdas: delitos de ENVIPE 2025 (`tmod_vic`, unidad
  **DELITO**, `FAC_DEL`: CIFRA-NEGRA, DENUNCIA, CARPETA-DADA-DENUNCIA × NAC/HOMBRE/MUJER/DOM-U/DOM-C/DOM-R; EXT-TELEFONICA
  × NAC/HOMBRE/MUJER); EDO-INSEGURO (`AP4_3_3`) 2024 (NAC, SINALOA) y 2025 (NAC, SINALOA, sexo, dominio, 4 edades) y la
  diferencia SINALOA 2025−2024; y sobre ENVIPE 2024 (`tper_vic1`, unidad **PERSONA**, `FAC_ELE`): DEJO-SALIR-NOCHE
  (`AP4_10_01`), 11 PREOC (`AP4_2_*`), 5 INSEGURO (`AP4_4_03/07/08/09/11`) × NAC/sexo/dominio/4 edades. Su medidor no
  importa recetas (sólo `io`, `zipfile`, numpy, pandas).
- [LEÍDO] Qué leyeron de ENVIPE 2026 los CALC sellados que la consumen (`spec.yaml:variables` con archivo `*2026*`):
  `CALC-DUELO-ENVIPE2026-EMISIONES-0001` y `-ADJUDICACION-0001` (ejecuciones 2026-09-22T20:16Z y 20:19Z): `tmod_vic`
  (BP1_20, BP1_23, BPCOD, DOMINIO, EDAD, EST_DIS, FAC_DEL, ID_PER, SEXO, UPM_DIS; unidad **DELITO**) y `tsdem` (ID_PER,
  NIV, como eje del delito); `CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` (2026-09-23T01:01Z): `tmod_vic` (BPCOD,
  BP1_20, BP2_1, EST_DIS, FAC_DEL, UPM_DIS). Emitieron R de `no-denunciado` (BP1_20 = 2 ∧ BP1_23) y `evade_norma`
  (BP1_20 = 2 ∧ BP1_23), nacional y por sexo, dominio, edad y NIV. **Ninguno lee `tper_vic1`** ni los reactivos AP4_*
  (sección 4 del cuestionario principal); ninguno lee `BP1_21`, `BP1_24` ni `BP1_5A_2` (`grep` sobre sus `spec.yaml`: 0).
- [EJECUTADO] Quién mide AP4_* sobre ENVIPE (`grep -l` sobre los 394 `spec.yaml` de `data/corrida0/`): `AP4_3_3|AP4_4_A|
  AP4_10_02` → sólo los dos contendientes; `AP4_2_|AP4_4_0|AP4_4_1|AP4_10_01` → sólo MC2.

### 0.1 · Celdas de PERCEPCION ya vistas (RETROSPECTIVAS) y reservadas

Una celda es «vista» si algún CALC sellado emitió (o pudo derivar de lo que leyó) su R: aquí, la proporción
ponderada por `FAC_ELE` de una conducta AP4_* entre personas elegidas de 18+ en una categoría de un eje. Los duelos
agregaron **delitos** ponderados por `FAC_DEL` (otra unidad y otra tabla), y usaron `NIV`, `SEXO`, `EDAD`, `DOMINIO` sólo
como ejes de delitos. Resultado [LEÍDO, por variable]: **0 de 138 celdas vistas; 138 reservadas**, todas PROSPECTIVAS.
Coincide con el asiento de los duelos en `data/corrida0/decisiones.tsv` (`reserva:envipe2026-consumida-por-duelo`:
«QUEDÓ SIN ABRIR y SIGUE RESERVADA … toda otra tabla del zip (el código sólo leyó tmod_vic y tsdem), todo otro
desenlace o variable»; ídem `…-marginales-2`). Exposición previa declarada en `reserva:envipe2026`: «dirección vio
titulares nacionales de denuncia en el comunicado de prensa» — denuncia, no percepción.

### 0.2 · Celdas de MC2: PROSPECTIVAS, RETROSPECTIVAS, DUPLICADAS y apartadas

La rejilla se lee del árbitro (las 205 celdas con `-P` en el `resultados.json` sellado de MC2), no se teclea; la clase va
en el id de la celda (A.16). Contendiente por celda: su **última ola** medida (2025 para EDO-INSEGURO; 2024 para el resto;
2025 para los delitos).

| clase | celdas | id | qué hace | por qué |
|---|---|---|---|---|
| PROSPECTIVA | 170 | `MC2-<celda>` | R y **puntúa** (lo/hi = IC95 sellado 2024; punto = P) | DEJO-SALIR-NOCHE, 11 PREOC, 5 INSEGURO × 10 segmentos; `tper_vic1` 2026 no la leyó nadie; MC2 se selló antes de abrirla |
| RETROSPECTIVA | 21 | `MC2-RETROSPECTIVA-<celda>` | R **sin puntuar** (lo/hi None; punto None: unidad DELITO) | `tmod_vic` 2026 fue abierta por los duelos (22–23/sep) **antes** del COMMIT-1 de MC2 (28/sep): el orden de los sellos no deja PROSPECTIVA (§4 v2.16); su desenlace de denuncia (`BP1_20`) se cruzó por sexo y dominio —los segmentos de MC2—; dirección vio titulares nacionales de denuncia; y lo que el comunicado reporte de carpeta o extorsión telefónica no es verificable aquí (leerlo está vedado, E.6), y NO-VERIFICABLE-AQUÍ no satisface la guarda de una rama irreversible |
| DUPLICADA | 11 | `MC2-DUPLICADA-<celda>` | R **sin puntuar** (lo/hi None) | EDO-INSEGURO-2025 × {NAC, SINALOA, HOMBRE, MUJER, DOM-U/C/R, 4 edades} = mismo estimando (AP4_3_3 2 frente a 1, `FAC_ELE`, `tper_vic1`) y mismo segmento que ESTADO-INSEGURO de PERCEPCION (TOTAL-TODOS, ENTIDAD-25, SEXO, DOMINIO, EDAD); la puntúa PERCEPCION, sellado antes (26/sep) y ya fijado en este expediente: no se cuenta dos veces |
| APARTADA | 3 | — | nada | EDO-INSEGURO-2024-NAC y -SINALOA: ola superada por la 2025 del mismo contendiente; EDO-INSEGURO-SINALOA-DIF-2025-2024: diferencia entre olas, no un nivel; su análogo 2026 sería otro estimando |

Universo de la DUPLICADA frente a su gemelo: idéntico salvo que PERCEPCION exige EDAD ≤ 97 y MC2 no (EDAD fuera de
18–97 en `tper_vic1` sería código de no especificado [SUPUESTO: persona elegida de 18+; no verificable sin el FD 2026
en NUBE]); con EDAD en 18–97 el test comprueba R idénticos sobre sintético.

## 1 · Estimandos

**PERCEPCION** (138 celdas): **R = Σw·y / Σw** en ENVIPE 2026 por conducta y categoría de cada eje, con la recodificación
y el universo del contendiente (CONDUCTAS, MAPAS, EDADES, `une()` del medidor sellado, importado por bytes con sha256
fijado en `APERTURA-ENVIPE-2026-spec.yaml`):
- ESTADO-INSEGURO: `AP4_3_3` = 2 (inseguro) → 1; = 1 (seguro) → 0; 9 fuera.
- INSEGURO-CAMINAR-DE-NOCHE: `AP4_4_A` ∈ {3, 4} → 1; ∈ {1, 2} → 0; 5, 9 fuera.
- DEJO-PERMITIR-MENORES-SALIR-SOLOS: `AP4_10_02` = 1 → 1; = 2 → 0; 3, 9 fuera.

**MC2** (202 celdas emitidas; 170 puntúan): **R = Σw·y / Σw** por celda, con la recodificación de su medidor sellado
(`frame_del`, `frame_per`, `celdas_del`, `celdas_per`; ceros a la izquierda quitados, `_bin(col, SÍ, NO)`) y la ola 2026
en la ranura de la última ola de cada estimando (tabla 2026 servida donde su código pide `tper_vic1_envipe2024`,
`tper_vic1_envipe2025` o `tmod_vic_envipe2025`):
- DEJO-SALIR-NOCHE: `AP4_10_01` = 1 → 1; = 2 → 0; otro fuera.
- PREOC-<tema>: `AP4_2_<código>` = «1» → 1, otro → 0, entre quienes no marcaron `AP4_2_99` = 1 (temas y códigos: `PREOC`
  del medidor sellado, 01–11).
- INSEGURO-<espacio>: `AP4_4_<código>` = 2 → 1; = 1 → 0; otro fuera (CALLE 03, BANCO 07, CAJERO 08, TRANSPORTE 09,
  CARRETERA 11: `AP44` del medidor sellado).
- EDO-INSEGURO (DUPLICADA): `AP4_3_3` = 2 → 1; = 1 → 0.
- RETROSPECTIVAS (delito, sobre `BP1_20` ∈ {1, 2}): DENUNCIA = `BP1_20` = 1 o `BP1_21` = 1; CIFRA-NEGRA = no (denuncia y
  `BP1_24` = 1); CARPETA-DADA-DENUNCIA = `BP1_24` = 1 entre denunciados; EXT-TELEFONICA = `BP1_5A_2` 1/0 entre
  `BPCOD` = 9.

## 2 · Universo, unidad, ponderador, diseño

PERCEPCION: persona elegida de 18–97 (`EDAD`, tabla `tper_vic1`); ponderador `FAC_ELE`; válido `FAC_ELE` > 0, `EST_DIS` y
`UPM_DIS` no vacíos. Ejes: SEXO (1/2), EDAD (18-29, 30-44, 45-59, 60+), ESCOLARIDAD (`NIV` de `tsdem` por `ID_PER`,
deduplicado: 00-02 / 03-05 / 06-07 / 08-09), DOMINIO (`U`/`C`/`R`), ENTIDAD (`CVE_ENT` 01–32).
MC2: el universo de su `_estima` — peso finito > 0, estrato y UPM no vacíos; persona elegida de `tper_vic1` (`FAC_ELE`,
sin tope de EDAD) o delito de `tmod_vic` (`FAC_DEL`). Segmentos: NAC, HOMBRE/MUJER (`SEXO`), DOM-U/C/R (`DOMINIO`),
EDAD-18-29/30-44/45-59/60-MAS (`EDAD`), SINALOA (`CVE_ENT` = 25).
Payload: `envipe2026_csv`. R es un punto.
**IC del contendiente por celda:** PERCEPCION: IC-LO/IC-HI sellados de 2024 (IC de diseño); punto = P sellado. MC2:
`-IC95-INF`/`-IC95-SUP` sellados de su última ola (bootstrap); punto = `-P`. Ninguno trae IC de persistencia.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada (PERCEPCION: un eje;
MC2: la máscara de un segmento); un cruce levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast`
sobre su propio archivo y exige que los inputs sean exactamente el payload y los repo del contrato. Única lectura:
`lee_payload_reservado` — cabeceras de los tres miembros (primeros 64 KiB, fin de línea `\r`/`\r\n` normalizado), luego
`tper_vic1` y `tsdem` con la receta de pisos (columnas de PERCEPCION) y `tmod_vic` y `tper_vic1` con el lector sellado de
MC2 (`_lee`, columnas de MC2); sólo columnas que existan. Estructura ausente → PARO: PERCEPCION `ID_PER`, `EDAD`,
`FAC_ELE`, `EST_DIS`, `UPM_DIS` (`ID_PER` en `tsdem`); MC2 `EST_DIS`, `UPM_DIS` y `FAC_DEL` (`tmod_vic`) o `FAC_ELE`
(`tper_vic1`). Desenlace ausente → celda NO-ESTIMABLE (R None); eje ausente → segmento vacío → R None. Miembro no
único o lector de MC2 que levanta `ReservaRota` → PARO. Probado sobre sintético con el esquema de los dos contendientes:
`tests/test_apertura_envipe_2026.py` (con soporte, desenlace sin columna, categoría vacía, estructura ausente de cada
contendiente, fin de línea `\r`, R de MC2 contra cálculo directo, DUPLICADA igual a su gemelo, rejilla de MC2, `medir()`
completo, auditoría y las 9 mutaciones) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi y R finitos (sólo PERCEPCION y MC2-PROSPECTIVA traen lo/hi). **Primaria** (una sola, sobre todas
las celdas puntuadas de los dos contendientes, todas de unidad PERSONA): cobertura k/n = #celdas con lo ≤ R ≤ hi, con
IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95;
**SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(excluyentes). Secundarias, descriptivas: cobertura por conglomerado (conducta de PERCEPCION; el CALC para MC2) y error
absoluto medio punto-vs-R **sólo sobre celdas PERSONA** (`UNIDAD_MAE`; el punto de una celda DELITO va None: nada se
promedia entre unidades). Las RETROSPECTIVAS y DUPLICADAS emiten R y no entran a k, n, Wilson ni MAE.
B-bis: los IC son de diseño de una ola anterior (PERCEPCION y 170 celdas de MC2: 2024, dos olas antes; ENVIPE 2025 está
abierta pero ningún CALC sellado mide AP4_2, AP4_4_0x/1x ni AP4_10_01 sobre ella: «nadie ocupó la fila»): no absorben el
error muestral de R ni el cambio 2024→2026. **SUBCUBRE es esperable aun sin cambio**; se lee «el piso con su IC de diseño
no anticipa 2026». CALIBRADO = pisos **corroborados en alcance**; SOBRECUBRE = **acotados**. Falsador débil por
construcción, declarado. Las celdas de las dos fuentes comparten muestra (misma ola 2026, mismas personas): la
cobertura no es de celdas independientes, y así se lee.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Periodo de referencia: la pregunta 4.10 de 2024 dice «Durante 2023» [LEÍDO, spec del contendiente §2]; se espera «Durante
  2025» en 2026 [SUPUESTO; lo verifica la receta paso 3]. Mismo texto con otro año = misma pregunta.
- [SUPUESTO→rama prevista] NUBE sin corpus montado: los catálogos 2026 del paquete no se leen aquí; los códigos se fijan
  **sobre los catálogos de las olas de los pisos** (2024 y 2025, specs de los contendientes), rotulado así.
- [SUPUESTO por analogía; cero o más de uno → PARO] Nombres de miembro 2026: el duelo sellado resolvió por sufijo
  `tmod_vic_envipe2026/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv` (`RESULT-DUELO26-ADJ-R-ND-MIEMBRO`);
  por la misma convención se resuelven `conjunto_de_datos_tper_vic1_envipe2026.csv` y `conjunto_de_datos_tsdem_envipe2026.csv`.
- Regla fijada: si en caja, antes de correr, el catálogo 2026 del paquete no trae una columna de un contendiente con el
  mismo texto y códigos, **esa celda sale NO-ESTIMABLE** (ausente → R None; sin recodificación ad hoc) y se declara. Si
  trae la columna con códigos distintos, el acto de apertura PARA antes de correr y se emite una v1_1. Leer catálogos y
  cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENVIPE-2026-<celda>-R` (340: 138 de PERCEPCION `<conducta>-<eje>-<cat>`; 202 de MC2 `MC2-<celda>`,
`MC2-RETROSPECTIVA-<celda>`, `MC2-DUPLICADA-<celda>`), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA`
(= PROSPECTIVA: rotula la primaria, que sólo usa celdas PROSPECTIVAS; las R RETROSPECTIVAS llevan el rótulo en el id).
Ningún None/NaN fuera de R NO-ESTIMABLE, Wilson y MAE cuando n = 0.
Contrato: `APERTURA-ENVIPE-2026-spec.yaml` (calc_id `CALC-APERTURA-ENVIPE-2026-0001`). Como el payload no lleva
`estado_reserva`, el paso 4a de la receta (levantar custodia) no mueve nada; el cierre re-rotula la reserva en
`decisiones.tsv` como consumida por completo.

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA/RETROSPECTIVA: la primaria es PROSPECTIVA por construcción (PERCEPCION ejecutado 2026-09-26, MC2
  2026-09-28; `tper_vic1` 2026 no leída por nadie, §0.1–0.2). Las 21 RETROSPECTIVAS de MC2 (delito, `tmod_vic`) y las de
  los duelos no se mezclan con esta cobertura en ninguna frase.
- Unidad: la primaria es **persona elegida**; las celdas DELITO de MC2 no puntúan ni entran al MAE; nada se promedia con
  unidad delito ni hogar.
- Escala: proporción 0..1; «R dentro del IC del contendiente»; MAE descriptivo.
- Violencia es estructura: la percepción de inseguridad, las preocupaciones y la restricción de salidas son respuesta
  adaptativa al entorno, no rasgo cultural; la cifra negra es desempeño institucional, no desconfianza «cultural».
  DOMINIO es urbano/complemento/rural, no clase; ESCOLARIDAD aproxima clase sólo en parte.
- Cifras escritas a mano: ninguna; las constantes son hashes fijados, la regla (0.95, z = 1.959964) y los conteos de
  celdas, que el test deriva de la rejilla del árbitro.
