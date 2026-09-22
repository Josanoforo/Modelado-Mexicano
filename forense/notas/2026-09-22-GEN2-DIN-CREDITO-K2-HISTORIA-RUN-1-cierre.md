# Nota de cierre · ACTO GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1 · 22/sep/2026

ADR `ADR-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01` (raíz `ef6f` = 0-bis `ef6f74a6`). CAJA, Opus 5.5 (el encargo sugería Sonnet; D-13 permite subir), sin sub-agentes, MODO RÍGIDO. Encargo archivado verbatim: `forense/encargos/2026-09-22-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1.md` (adjunto y cuerpo `9d5ef52a…`).

**Contadores movidos:** una corrida GEN2 sellada (`N_corridas_selladas` 158 → 159), `cuenta_gen2 = SI`, `adopta = NO`. La corrida queda «sellada en disco, no registrada» en la vista publicada (§4).

## 1 · Arranque y compuertas

- Guardias 0.a–0.d: base `ccd7c0eb` (= SHA de redacción), árbol limpio, rótulo sin rama/worktree/PR previos, `limpia_arbol --reporta` sin novedad propia.
- Entorno: `tools/entorno.py --sonda-red` → `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · red 200 · `data_raw:SI descargas_mx:SI` · `corpus=SI(examinados=436)`. CAJA.
- **Compuerta «no hay otro acto de caja en vuelo» (protege: borrar): NO se cumplía al abrir.** A las 13:46 los dos hermanos de caja de la tanda (`GEN2-DIN-CREDITO-ESCOLARIDAD-2`, worktree recién creado; `GEN2-DIN-LOTE-C2-RESTRINGIDO-1`, 0-bis `4e123a98`) estaban vivos. Se preguntó a mesa; respuesta verbatim: «Espera a que cierre E1 y E2 y ten una sonda para que reanudes cuando se fusionen». Cero commits hasta que una sonda (`gh pr list --head <rama> --state all`, cada 180 s) vio los dos PR `MERGED`: #1005 (`0f833085`, 21:12Z) y #1003 (`26236d29`, 21:24Z). Se reanudó sobre `origin/main = 26236d29` (fast-forward).
- **Compuerta «firma ff56-02 presente» (protege: abrir dato): cumplida.** La firma viaja verbatim en §2 del encargo; en el repo la fila `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02` estaba `ABIERTA`. Este acto la asienta `FIRMADA` (A.12: la firma que viaja en el encargo la asienta el acto que lo ejecuta).

## 2 · P1 · Verificación de sello (ninguna edición)

`python3 tools/corrida0.py preflight CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001`: los 8 inputs `COINCIDE` (4 payloads ENIF 2012/2015/2018/2021 en `data_raw`, 2 medidores y 2 metadatos del repo), `[SELLO_COINCIDE]`, único bloqueo `calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO`. `spec.yaml` `5826d4ce…`, `medidor.py` `7e8d80f9…`.

## 3 · P2 · `run` y `verify`

- **Premisa `[SUPUESTO]` §3, confirmada por ejecución:** `corrida0 run …-0001` → `RUN: CALC-INMUTABLE · YA-SELLADO … bytes intactos` (`tools/corrida0.py:2369`). Se toma la rama prevista: **CALC nuevo `-0002`**.
- **Premisa que cae (logística, declarada):** «la misma `spec.yaml` (sha idéntico)» es imposible. El `-0002` tiene que llevar su propio `calc_id`, su `script` y `repite_de` en la raíz, porque sólo `repite_de` autoriza repetir los 92 ids de RESULT (`tools/corrida0.py:4327`). Diff completo contra el `-0001`: esas tres claves más las dos etiquetas de estado (`estado_al_congelar`, `medidor_ejecutado_al_congelar`), que describían el COMMIT-1 del `-0001`. Estimando, universo, variables, ponderador, parámetros, semilla, tolerancia y los 92 `resultados` son idénticos. `medidor.py` es idéntico byte a byte (`7e8d80f9…`). `spec.yaml` del `-0002`: `0902dddf…`.
- COMMIT-1 del `-0002`: `d72ddfaa`, sin microdato. `preflight` VERDE (92 ids, 8/8 inputs COINCIDE, árbol limpio, sin sello previo).
- `run` (11 s): `exit_code 0`, sellado, `[COINCIDE] sello nuevo`; corrida `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002--d72ddfaa7635`. COMMIT-2: `64639074`.
- `verify`: **`REPRODUCE` (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)**. Repetido en proceso aislado (`tools/verifica_aislada.py`): igual, `ids_faltantes=0`. 92 RESULT, ninguno `None` ni no finito.
- **Oro (control positivo, lectura del sellado ajeno):** en 2012/2015/2018 la razón ponderada tenedores/todos (`…ENTRE-TENEDORES…-DEN-W / …BANCARIA…-DEN-W`) es igual al `K1-NACIONAL-TODOS-P` de `CALC-DIN-CREDITO-PISOS-ENIF{2012,2015,2018}-0001` con |Δ| = 0.0, y `FILAS-PERSONAS` coincide (6 113 / 6 039 / 12 446).

**Resultados (DESCRIPTIVO rotulado; unidad persona; «tarjeta de crédito bancaria», texto idéntico en las cuatro olas; poblaciones 18-70 en 2012-2018 y 18+ en 2021):**

| ola | toda persona elegida: % [IC95] (n) | entre tenedores de crédito formal: % [IC95] (n) |
|---|---|---|
| 2012 | 9.03 [8.13, 9.95] (6 113) | 32.90 [30.09, 35.72] (1 616) |
| 2015 | 10.76 [9.78, 11.80] (6 039) | 37.04 [34.22, 39.90] (1 752) |
| 2018 | 10.53 [9.77, 11.31] (12 446) | 33.81 [31.74, 35.91] (4 117) |
| 2021 | 10.12 [9.39, 10.85] (13 554) | 32.39 [30.44, 34.33] (4 561) |

Todas las celdas con soporte `OK` (n ≥ 200) y 10 000/10 000 réplicas válidas. 2024: `RESERVADA-NO-MEDIDA`. **Frontera FP-404 (2), en los RESULT de texto: `NO-SE-COMPARA` 2021↔2024, y la cifra del corpus «+5.2 pp desde 2021» `NO-SE-CITA` sin la frontera.** ENIF 2024 no se abrió: no es input de la spec.

Lectura mínima, rotulada: RETROSPECTIVA, descriptiva, sin serie causal. El nivel general se mueve poco más de un punto entre olas, y el de 2018 queda dentro del IC de 2015. Ninguna frase compara estos niveles con 2024.

## 4 · P3 · Vista (E.7)

- **Asiento:** una fila propia en `forense/replay-evidencia.tsv` (append, `REPRODUCE`/`IDENTICO`, procedencia `VERIFY-AISLADO · GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1`), con evidencia cruda en `forense/notas/2026-09-22-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-evidencia-replay.json`. Commit `1251792b`.
- **Registro: no viaja en el PR (premisa de logística que cae).** Desde #984, `verify.yml:542-546` bloquea todo PR que toque un derivado. `FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-02` está FIRMADA opción (a): el job del push a main publicará la vista a partir del diff de `replay-evidencia.tsv`. Ese job todavía no existe (`verify.yml:369-370` sigue exigiendo `--lote`). Así cerraron también `ESCOLARIDAD-2` (#1005) y `C2-RESTRINGIDO-1` (#1003). Medido en el árbol: `registro --escribe` sin lote para con `REPLAY-PISADO` y no escribe nada, porque movería el replay de 13 corridas ajenas (`NO-VERIFICADO → REPRODUCE/IDENTICO`). Las 13 tienen asiento en `origin/main` hecho por `GEN2-PENDIENTES-CAJA-1`: la vista publicada va atrás de su fuente. Este acto no las mueve (no son suyas y la vista no viaja).
- `status` antes (`origin/main` limpio, worktree temporal) / después (esta rama): `N_corridas_selladas` 158 → 159; `N_resultados_sellados` 48 015 → 48 107 (+92). `N_resultados_gen2_sellados` se queda en 47 414 porque cuenta ids únicos y el `-0002` reutiliza a propósito los 92 ids del `-0001` (`repite_de`). Adoptados sin cambio.
- **Enmienda fechada (22/sep/2026) al `-0001`:** `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` queda como constancia del COMMIT-1 de `GEN2-DIN-CREDITO-HISTORIA-1`: sus 92 RESULT salieron sólo del sintético. Por `repite_de`, el registro lo proyecta `SUPERADO→CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002`. Sus bytes no se tocan.

## 5 · Filas de gobierno

- `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02` → `FIRMADA` (texto verbatim en el encargo §2), ejecutada por el `-0002`.
- `NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-04` (sucesor: este acto) → `CERRADA`: K2 corrió, se selló y se asentó aquí.
- `NC-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01` (nueva, ABIERTA): publicar la fila del `-0002` en la vista, diferida al job de TUBERÍA.
