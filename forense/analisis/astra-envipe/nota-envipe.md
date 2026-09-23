# C-ASTRA · ENVIPE 2025 · evasión de norma

Estado: cuatro CALC sellados y verificados en la rama `codex/astra-interaccion-dinamica-1`; aún no acreditados en `origin/main`. No se evaluó el piloto ni se abrió R. La entrada al piloto depende de main antes de COMMIT-2 y de la aceptación de celdas por el piloto.

## Secuencia y exposición

[EJECUTADO] Worktree `/home/pc0/mm-astra-envipe-1`, rama propia, base `origin/main` 34c5d85b, limpio al congelar. La rama solicitada no existía local ni remotamente; se creó sin atribuirle continuidad. `00-ARRANQUE-Y-COORDINACION-ASTRA-1.md` y la adenda histórica SHA 44145283… no se hallaron en los archivos accesibles. Misión SHA 949a0f1a… archivada íntegra. Encargo propio SHA 3f03f981… archivado íntegro.

[LEÍDO] `decisiones.tsv` por CSV, cuatro reservas `reserva:*`: ENVIPE 2026 entera, crédito ENIF 2024 salvo par visto, ENIGH 2024 entera y regla de ola nueva. Ni el duelo levantó reserva general ni esta sesión abrió esos datos. `marcador-segmento.tsv` por metadatos: cuatro grupos RESERVADA/EMITIDA-SIN-R; 8+8+6+16=38. Edad × dominio 2025, NC-0328, excluida; escolaridad × dominio consumida por piloto 2. No se abrieron sus R ni se usaron sus resultados para escoger hiperparámetros.

[LEÍDO] `prereg-caja-ENVIPE-EVASION-NORMA`; `TRA-evade-norma-sxd12-spec-v1_0.md` §0: texto de BP1_20 y BP1_23 idéntico 2023/24/25, códigos 04 pérdida de tiempo, 05 trámites largos, 06 desconfianza, 08 actitud hostil. El rótulo corto de BP1_20 cambió, no el reactivo. Sexo/edad tmod_vic; NIV de tsdem con enlace ID_PER único. Los códigos y el lector histórico quedaron pinados por SHA. La estimación es conjunta por delito sobre BP1_20 ∈ {1,2}, con FAC_DEL, EST_DIS y UPM_DIS. No se promediaron delitos con personas.

[EJECUTADO] SHA de ZIPs históricos: 2023 `0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404`; 2024 `90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2`, iguales al manifiesto. Corpus montado en namespace de `bwrap` como `data/raw` de solo lectura, sin escribir fuera del perímetro. Lista ejecutable solo esos dos ids y el YAML público SHA `93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f` (extracción del segmento `tramite.evasion_norma_ejes_envipe2025`). No se incluyó ni abrió `envipe2025_csv`; no se listaron miembros de su ZIP.

El historial de esta sesión: solo documentos, marcador, marginales públicos, 2023/24 y ejecución de los cuatro CALC. `git log --all -- data/corrida0/CALC-ASTRA-ENVIPE-EDADXSEXO-0001` muestra freeze 5bfcf842 antes de emisión 50a73d47. La ausencia de un `git log -S` por sí sola no prueba ceguera; la declaración se apoya también en los inputs sellados y esta traza. No hay exposición conocida de esta sesión a los cruces objetivo 2025.

## Procedimiento y ejecución

`tools/astra/envipe/model.py` SHA `47ded83d3e8a9283a2972289240d8fa6b90c440cefb238bca04255e044a11212`. Lectores pinados: `marginales_reproduccion.py` 4df2c630…, `ejes_maestra35_l1.py` 502f5a41…, `calibracion_mordida_encig_serie.py` b2e636b0…. Antes del ajuste se probó sobre datos sintéticos logit/expit, bloqueo de ruta ficticia ENVIPE 2025, y falla de frontera. Freeze 5bfcf842 se publicó antes de la primera corrida histórica. Fórmula y pooling exactos en las specs; C-ASTRA añade ruido por celda y persistencia entre 2023/24 a C2; no preserva necesariamente marginales.

`python3 tools/corrida0.py --help`, seguido para cada CALC de `preflight → run → verify` dentro de `bwrap` con corpus histórico montado de solo lectura. Los cuatro preflight VERDE; los cuatro run SELLADO; los cuatro verify REPRODUCE, CONTEXTO IDENTICO. Los commits de emisión son 50a73d47, 86c678af, d8536f29 y be602aa2. Replay propio se añadió como cuatro filas a `forense/replay-evidencia.tsv`.

Diagnóstico histórico del lector: 2023 35,135 delitos, 18,106 Y=1, 604 estratos, 10,183 UPM, 0 huérfanos, escolaridad fuera 104, edad fuera 143, BP1_23 vacío entre no denunciados 148. 2024 37,614 delitos, 19,532 Y=1, 601 estratos, 10,096 UPM, 0 huérfanos, escolaridad fuera 149, edad fuera 200, BP1_23 vacío entre no denunciados 125. Ambos universos BP1_20 tienen cero filas fuera. Los vacíos se conservan como Y=0 dentro del universo, como especifica el estimando.

El intervalo es **predictivo aproximado**, condicionado a los marginales 2025 como puntos públicos. Incluye muestreo histórico compartido, variación de hiperparámetros y deriva anual; no es IC de R. Esos sorteos no acreditan cobertura empírica del 95% ni calibración frente a la ola objetivo. Según la spec humana congelada del piloto 4 (`445531a31`, §2.1), C-ENCOGIDA conserva la **regla** del piloto 3 y deriva una λ propia por cruce con sus deltas históricos; no hereda el valor de λ del piloto 3. No se tocó ese candidato. No se hizo validación contra 2025, cálculo de victoria ni IC de ΔMAE.

## Emisiones

| CALC/sufijo | Celda | RESULT base | Punto | Intervalo | Tipo | Estado |
|---|---|---|---:|---|---|---|
| EDADXSEXO | 18-29 × 1 Hombre | RESULT-ASTRA-EDADXSEXO-01 | 0.551533 | [0.525895, 0.571010] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 18-29 × 2 Mujer | RESULT-ASTRA-EDADXSEXO-02 | 0.492448 | [0.470957, 0.517366] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 30-44 × 1 Hombre | RESULT-ASTRA-EDADXSEXO-03 | 0.617105 | [0.595619, 0.638053] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 30-44 × 2 Mujer | RESULT-ASTRA-EDADXSEXO-04 | 0.546814 | [0.525025, 0.566658] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 45-59 × 1 Hombre | RESULT-ASTRA-EDADXSEXO-05 | 0.639170 | [0.617099, 0.663028] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 45-59 × 2 Mujer | RESULT-ASTRA-EDADXSEXO-06 | 0.564975 | [0.541244, 0.587430] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 60+ × 1 Hombre | RESULT-ASTRA-EDADXSEXO-07 | 0.599717 | [0.576609, 0.620986] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXSEXO | 60+ × 2 Mujer | RESULT-ASTRA-EDADXSEXO-08 | 0.534332 | [0.511379, 0.557760] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | hasta primaria × 1 Hombre | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-01 | 0.529149 | [0.503161, 0.553051] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | hasta primaria × 2 Mujer | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-02 | 0.461311 | [0.438188, 0.484353] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | secundaria × 1 Hombre | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-03 | 0.609444 | [0.581382, 0.633055] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | secundaria × 2 Mujer | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-04 | 0.527264 | [0.502736, 0.557717] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | media superior × 1 Hombre | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-05 | 0.578632 | [0.555515, 0.603225] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | media superior × 2 Mujer | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-06 | 0.510905 | [0.487309, 0.533021] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | superior × 1 Hombre | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-07 | 0.618672 | [0.597545, 0.642603] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| ESCOLARIDADPROXYXSEXO | superior × 2 Mujer | RESULT-ASTRA-ESCOLARIDADPROXYXSEXO-08 | 0.563530 | [0.538163, 0.585838] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Rural × 1 Hombre | RESULT-ASTRA-DOMINIOXSEXO-01 | 0.449077 | [0.428825, 0.473919] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Rural × 2 Mujer | RESULT-ASTRA-DOMINIOXSEXO-02 | 0.361733 | [0.338418, 0.381553] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Complemento urbano × 1 Hombre | RESULT-ASTRA-DOMINIOXSEXO-03 | 0.563059 | [0.545097, 0.585560] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Complemento urbano × 2 Mujer | RESULT-ASTRA-DOMINIOXSEXO-04 | 0.483744 | [0.461252, 0.500723] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Urbano × 1 Hombre | RESULT-ASTRA-DOMINIOXSEXO-05 | 0.620751 | [0.607618, 0.634443] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| DOMINIOXSEXO | Urbano × 2 Mujer | RESULT-ASTRA-DOMINIOXSEXO-06 | 0.566714 | [0.552398, 0.579834] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 18-29 × hasta primaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-01 | 0.450324 | [0.419363, 0.487689] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 18-29 × secundaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-02 | 0.524700 | [0.489033, 0.560102] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 18-29 × media superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-03 | 0.500416 | [0.464194, 0.534711] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 18-29 × superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-04 | 0.547879 | [0.512023, 0.580639] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 30-44 × hasta primaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-05 | 0.511618 | [0.475375, 0.545624] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 30-44 × secundaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-06 | 0.585337 | [0.551251, 0.617081] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 30-44 × media superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-07 | 0.561563 | [0.526163, 0.597147] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 30-44 × superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-08 | 0.607770 | [0.573763, 0.641088] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 45-59 × hasta primaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-09 | 0.532698 | [0.497442, 0.566028] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 45-59 × secundaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-10 | 0.605688 | [0.568733, 0.636158] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 45-59 × media superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-11 | 0.582248 | [0.548037, 0.620017] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 45-59 × superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-12 | 0.627720 | [0.594452, 0.661069] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 60+ × hasta primaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-13 | 0.496521 | [0.457611, 0.531873] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 60+ × secundaria | RESULT-ASTRA-EDADXESCOLARIDADPROXY-14 | 0.570607 | [0.537149, 0.608302] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 60+ × media superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-15 | 0.546642 | [0.513845, 0.583782] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |
| EDADXESCOLARIDADPROXY | 60+ × superior | RESULT-ASTRA-EDADXESCOLARIDADPROXY-16 | 0.593283 | [0.560329, 0.624792] | predictivo 95% | ESTIMABLE: INTERVALO-PREDICTIVO-95 |

## Límites y pendiente

Los 38 puntos tienen intervalo; ninguna celda fue excluida por no estimabilidad histórica. El hiperparámetro tau² de edad × escolaridad resultó cero por la regla congelada; en ese cruce el punto coincide con C2 y el intervalo conserva incertidumbre predictiva. Esto no se ajustó tras verlo. Se condicionó la incertidumbre de los marginales públicos 2025 y no se afirma cobertura de R. No se abrió R, no se adjudicó PROSPECTIVA y no se ejecutó `registro --escribe`. Falta que el PR se fusione antes de COMMIT-2; no se ha declarado EN-MAIN.

`admisibilidad-envipe.tsv` ofrece el contrato por clave de eje y celda para los 38 RESULT. El cotejo favorable es documental frente a `445531a31` y no equivale a aceptación del candidato: caja debe confirmar las claves finales, el soporte `n₂₀₂₅`, la elegibilidad temporal y la inferencia de ΔMAE/B-bis antes de abrir R. No se generaron ni emparejaron sorteos ASTRA con réplicas del árbitro.
