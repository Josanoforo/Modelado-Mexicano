# GEN2-CALC-ALTERNOS-LOTE-1 · cierre

Contadores movidos: **nueve CALC GEN2 sellados** (`cuenta_gen2 = SI`, no adoptan); 9/9 verify aislado REPRODUCE · IDENTICO con asiento en `forense/replay-evidencia.tsv`; `celdas_validadas` Δ0 (ningún CALC es celda-D).

Acto `GEN2-CALC-ALTERNOS-LOTE-1` · CAJA (`tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red 200, corpus SI con 515 archivos examinados) · MODO RÍGIDO por CALC desde COMMIT-1 · base `98f80cc7` (el encargo declaró `3c55bfc5`; main avanzó por #1284–#1289, sin tocar el perímetro) · 0-bis `795b1053` · ADENDA-1 (respuesta de mesa) `forense/encargos/2026-09-28-GEN2-CALC-ALTERNOS-LOTE-1-ADENDA-1.md`.

## 1 · Qué se pidió y qué decidió mesa a mitad del acto

El §1 del encargo pedía CALC para M05, M12, M13, M14, M15, M16, M17, M19, M22, M23 y R03+R08. La firma R08 A2 (b) que el propio encargo cita dice, verbatim: «M12, M14, M15, M16 y M17 quedan con su vía documentada en el mapa, sin fecha». Gastar esos HOLDOUT es irreversible (E.6), así que se preguntó a mesa. **Respuesta verbatim: «Obedecer R08 (b) (Recommended)».** Las once filas de esos cinco momentos no se abrieron y su HOLDOUT sigue intacto.

## 2 · Conteo de las 20 filas `CALC-CAJA` del mapa, más R03

| destino | filas del mapa | n |
|---|---|---|
| **CALC sellado** | 12, 13 (M05) · 32 (M13) · 53, 59 (M19) · 60 (M22) · 65 (M23) | 7 |
| **Diferido por reserva** | 33 (CSES Módulo 5, R04 RESERVADA) · 57 (ENVIPE 2025 `AP5_4_*`, fuera del árbitro: ningún CALC sellado abrió esa columna) | 2 |
| **Sin fecha por firma R08 (b) + ADENDA-1** | 24, 25, 26, 28, 29 (M12) · 36, 37, 38 (M14) · 42 (M15) · 44 (M16) · 48 (M17) | 11 |
| **Total** | | **20** |
| **R03 + R08** | ENCRIGE 2020 y ENVE 2024 (tabulados) | 2 CALC |

NO-CONSTRUIBLE parcial, dentro de los CALC sellados: `p17`/`p18` de CIDE-CSES 2015 poselectoral (§4) y el cruce tamaño × sector de R03 (no existe como tabulado).

**HOLDOUT gastado:** `M13`, `M19`, `M22`, `M23` (M23 ya estaba consumido según R07). Censo de familias 2027 antes de gastar (R01 (b)): 0 menciones de `M05|M13|M19|M22|M23` ni de `R7.1|R8.3|R10.3|via_informal|evasion_norma` en 140 archivos de `forense/analisis/familias-2027` (control positivo `ENIF`: 66 archivos). M05 es AJUSTE; R03 no es momento.

## 3 · CALC, commits y resultados

Specs humanas en `forense/prereg-caja/ALT-*-spec-v1_0.md` (+ `.sha256`). Medidor genérico idéntico en los seis CALC de microdato. Meter de reproducción para WVS; extractor de tabulados para R03. Lectura por `tools/corpus_loader.py::cargar`, fijado por sha256 (`84ec626c…`). IC95 = bootstrap de UPM dentro de estrato, 2 000 réplicas, semilla `20260928`, pareado dentro de cada CALC. Las cifras son proporciones ponderadas.

| CALC | COMMIT-1 | COMMIT-2 |
|---|---|---|
| CALC-ALT-M05-LAPOP2021-0001 | `d41cda11` (+1-bis `a88343c8`) | `da659fc3` |
| CALC-ALT-M05-LAPOP2019-0001 | `d41cda11` (+1-bis) | `28ae5b96` |
| CALC-ALT-M19-ENCUCI2020-0001 | `06a9173c` (+1-bis) | `0380cd11` |
| CALC-ALT-M23-ENSAFI2023-0001 | `6b102a38` (+1-bis) | `582bf412` |
| CALC-ALT-M13-CIDECSES2015-0001 | `99142486` (+1-bis) | `5d555835` |
| CALC-ALT-R03-ENCRIGE2020-0001 | `3e899ac7` (+1-bis) | `d03e1ee7` |
| CALC-ALT-R03-ENVE2024-0001 | `3e899ac7` (+1-bis) | `158df9cf` |
| CALC-ALT-M22-ENVIPE2025-0001 | `c2137b75` (+1-bis) | `b1a2bd40` |
| CALC-ALT-M19-WVS2018-REPRO-0001 | `fb2fb894` (+1-bis) | `41175083` |

**M05 · LAPOP 2021 (actitud).** `p(EXC18 = Sí)` = 0.198 [0.174, 0.222] (n = 1 494; 1 496 sin respuesta: el reactivo no se aplicó a toda la muestra). Con castigo probable ALTO 0.216 [0.179, 0.253] y con castigo BAJO 0.182 [0.152, 0.214]. Contraste pre-registrado BAJO − ALTO = −0.034 [−0.080, +0.011]: **cubre 0, así que no corrobora en actitud** (§ pre-registro). Por escolaridad: básica 0.214, media 0.200, superior 0.167. `p(pr3dnr ∈ {3,4})` = 0.449. Diseño: 2 990 UPM para 2 990 entrevistas (CATI, cada entrevista es su propia UPM): el IC equivale a muestreo aleatorio estratificado; se declara.

**M05 · LAPOP 2019.** `p(EXC18 = Sí)` = 0.169 [0.148, 0.189] (n = 1 566). Por años de escolaridad: 0–6 0.179, 7–12 0.170, 13 o más 0.149. Urbano 0.173, rural 0.150; contraste RURAL − URBANO = −0.023 [−0.074, +0.027]. No es serie con 2021 (cambio de modo).

**M19 · ENCUCI 2020** (`FAC_SEL`, corte ≥ 8/10, ADR-64). Sin puente (`AP5_1_1`) 0.219 [0.211, 0.227]; con puente (`AP5_1_2`) 0.622 [0.613, 0.633]; diferencia pareada +0.404 [0.393, 0.414]. El contraste pre-registrado, sin puente entre quienes confían en la policía menos quienes no, es **+0.145 [0.128, 0.163]: enteramente > 0**. Según el pre-registro esto es **consistente con «cálculo»**, con la reserva de método común (los dos reactivos vienen del mismo informante), que sesga hacia arriba. Por dominio, sin puente: urbano 0.228, complemento urbano 0.206, rural 0.208.

**M19 · WVS 7 México 2018: reproducción del abridor GEN1 → REPRODUCE.** 19 de 31 entidades elegibles; mediana 0.2435; 9 entidades ALTO y 10 BAJO; `p_ALTO` = 0.0456 y `p_BAJO` = 0.0500; `d` = −0.4422 pp, IC [−3.36, +2.47] pp (la misma cifra que publicó el abridor); secundaria +0.30 pp. Los cinco chequeos están dentro de 5e-7. `RES-0194` tiene ahora respaldo GEN2 sellado. En M19 los dos instrumentos no concuerdan: el contexto por entidad (WVS) no mueve la confianza sin puente, la percepción individual de la policía (ENCUCI) sí. Es la misma asimetría eje 1 / eje 2 que el abridor pre-declaró (método común). No se adjudica aquí.

**M22 · ENVIPE 2025.** Unidad delito, `FAC_DEL`. Universo: 22 536 delitos personales no denunciados (15 518 fuera por `BPCOD`, 2 226 por `BP1_20`), de los que 20 225 tienen razón válida. `p(miedo)` nacional = 0.080 [0.072, 0.091]. Las 32 entidades son estimables. Las tres más bajas: 22 Querétaro 0.045, 25 Sinaloa 0.049, 31 Yucatán 0.053. Las tres más altas: 28 Tamaulipas 0.132, 11 Guanajuato 0.137, 12 Guerrero 0.143. Sin enlace por `ID_PER`: 0. Hay 69 estratos con UPM única (se fijan). Es un piso de exposición: no toca el tratamiento de R10.3.

**M23 · ENSAFI 2023** (`FAC_ELE`, 20 448 personas). Solo informal 0.261 [0.252, 0.271]; informal 0.403; formal 0.251. Solo informal por tamaño de localidad: 100 mil y más 0.228, 15–99 mil 0.255, 2 500–15 mil 0.300, menos de 2 500 0.313. Contraste rural − urbano +0.085 [0.064, 0.108]. La informalidad no varía con el tamaño de localidad (0.39–0.41); lo que varía es la formalidad (0.32 → 0.14). Es un contraste de definición frente al RESULT ENIF 2024 sellado, que se cita y no se promedia. ENSAFI no distingue oferta de preferencia. La oferta al lado vive en `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001`.

**M13 · CIDE-CSES 2015 poselectoral.** `p(votó)` = 0.833 [0.809, 0.856]. En entidades con elección local concurrente 0.861 y sin ella 0.798; contraste **+0.063 [+0.015, +0.112]: > 0, consistente** (participación declarada, no causal). `p17`/`p18` quedan **NO-ESTIMABLE, n = 0**: las 1 200 filas vienen vacías en los dos reactivos (§4).

**R03 + R08 · ENCRIGE 2020 (tabulados `t6_33`/`t6_34`).** Control de fórmula PASA (máx Δ 5e-16). Control positivo contra #826: participación nacional 0.0509853592480 frente al sellado 0.050985359248 (Δ 2.7e-14). Participación, luego cota superior por conocimiento de terceros, luego percepción:
- Nacional: 0.051 · 0.221 · 0.443.
- Por tamaño: Micro 0.055 · 0.215 · 0.485 · Pequeña 0.022 · 0.253 · 0.157 · Mediana 0.044 · 0.301 · 0.387 · Grande 0.067 · 0.230 · 0.392.
- Por sector: Comercio 0.066 · 0.227 · 0.462 · Industria 0.038 · 0.210 · 0.458 · Servicios 0.053 · 0.228 · 0.407.

La cota superior supera a la participación en todos los dominios (sin anomalía). La percepción de Pequeña (0.157) se aparta de los otros tamaños (0.39–0.49); se reporta sin corregir.

**R03 + R08 · ENVE 2024 (tabulados `t1_21`/`t1_22`, año 2023).** Control PASA. Víctima de corrupción: nacional 0.0355; Comercio 0.033, Industria 0.037, Servicios 0.038; Micro 0.033, Pequeña 0.072, Mediana 0.084, Grande 0.065. ENCRIGE (empresa, 2020) y ENVE (unidad económica, 2023) no se combinan en ninguna cifra.

## 4 · Premisas que cayeron o se ajustaron (logística; objetivo alcanzable)

- **Base:** el encargo trae `3c55bfc5`; el acto arrancó sobre `98f80cc7`. Los PR fusionados en medio (#1284–#1289) no tocan el perímetro.
- **ENCRIGE 2020 / ENVE 2024 no son microdato.** `conjunto_de_datos_*_csv` son tabulados de datos abiertos, y el microdato ENCRIGE es de Laboratorio. R03 se extrae de tabulados con el régimen de #826: sin IC y sin cruce tamaño × sector.
- **Clasificador de concurrencia M13:** el calendario INE no está en el corpus. Se usó el marco del levantamiento local del mismo estudio: las etiquetas de valor de `edompio` en `cide_cses2015_nacional_preelectoral.sav` dan 16 entidades. Declarado en la spec.
- **`p17`/`p18` vacíos en el poselectoral nacional** (A.15: la columna existe y está vacía). Es un hallazgo sobre el archivo, no un procedimiento a corregir.
- **WVS:** se leyó el `.dta` v5.1 que usó el abridor (`f00013084`), no el CSV `f00013146` que nombra la fila del mapa. El CSV va separado por `;` y no declara su separador decimal. Desviación declarada en la spec antes de congelar.
- **Espejo:** `F00013146` y `F00013084` (WVS) se copiaron a `mm-corpus/descargas_mx_espejo/`; su sha256 es idéntico al del manifiesto. `data/raices.local.yaml` (gitignorado) apunta `descargas_mx` al espejo en este worktree.
- **ENVIPE 2025 «sólo lo que su árbitro abrió»:** se leyeron sólo columnas ya abiertas por CALC sellados de 2025: `TMOD_VIC` del árbitro y `CVE_ENT` de `TPER_VIC2` de REGION-2025. `AP5_4_*` no se abrió.
- **«PR por instrumento»:** un solo PR, con un commit por spec y dos por CALC (latitud §6: agrupación de PR). Así mesa fusiona en un solo acto de adopción.

## 5 · COMMIT-1-bis, declarado (v2.16 §6)

La primera corrida de `CALC-ALT-M05-LAPOP2021-0001` la rechazó el conducto antes de sellar: «RESULT-ALT-M05-LAPOP2021-TABLA: VALOR-LARGO (5121 bytes, str) -- una lista o tabla va a tablas/ del CALC y el RESULT la cita por REF». No se selló nada ni se imprimió ningún valor. `a88343c8` cambia sólo la serialización (helper `_ref`, mismo patrón que `CALC-FAMILIA-2027-ENIF-ORO-0002`) y el texto de `unidad` en los nueve `spec.yaml`. Quedan intactos estimando, universo, códigos, diseño, semilla y specs humanas (sidecars sin cambio). Defecto propio: el chequeo sintético previo ejercitó `_valida_outputs` pero no `_problemas_valor_largo`. El test del acto ahora ejercita los dos.

## 6 · Firmas asentadas (A.12)

`FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-01` (R07), `-02` (R08) y `-29` (R10) pasan a FIRMADA, con `ejecutada_en = ADR-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-01`. R01–R06 no tienen fila FP (`(sin FP)` en `decisiones-21.tsv`) y se asientan en el ADR: R01 (b) aplicado con censo; R02/R03 abiertas-como-vistas, leídas; R04 CSES M5 y R05 ENDUTIH 2025 sin abrir; R06 ENIF 2024 m7 sin abrir (no la usa ningún CALC del acto).

## 7 · Ninguna ola reservada abierta

Payloads abiertos: `mex_2021_lapop_americasbarometer_v1_2_w`, `mexico_lapop_americasbarometer_2019_v1_0_w`, `encuci2020_bd_dbf`, `ensafi2023_bd_csv_zip`, `cide_cses2015_nacional_poselectoral`, `f00013084_wvs_wave_7_mexico_stata_v5_1`, `envipe2025_csv` (columnas ya abiertas), `conjunto_de_datos_encrige_2020_csv` y `conjunto_de_datos_enve_2024_csv` (abiertas-como-vistas por R02/R03). Ninguno tiene `reserva` en `data/manifiesto.yaml`, y ninguno es CSES M5, ENDUTIH 2025, ENIF 2024 m7, ENCODAT 2025 ni ENVIPE 2026. De `cide_cses2015_nacional_preelectoral.sav` sólo se leyeron metadatos (`metadataonly=True`).

## 8 · Defecto adyacente arreglado (D-21, ≤ 10 líneas)

`forense/analisis/catalogo/genera_catalogo_v1_{1,2,3}.py` cuentan «CALC con cuenta_gen2=SI sellados en disco» por instrumento en el nombre, con un glob vivo sobre `data/corrida0/CALC-*`. Por eso los nueve CALC de este acto reescribían los catálogos v1.1–v1.3 ya publicados (CAPITAL_SOCIAL 6→7, POLITICA 11→13) y `test_regenera_identico` fallaba en el job `guardias` (3 FAIL). Es el mismo patrón que #1279 corrigió para la serie de oferta. Arreglo: una línea por generador que excluye la serie `CALC-ALT-`, posterior al corte publicado. Resultado: `ci_guardias --ejecuta-huerfanos` da 103 ejecutados, 0 fallidos, y los catálogos quedan byte-idénticos.
