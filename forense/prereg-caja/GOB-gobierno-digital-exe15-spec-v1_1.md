# PILOTO 3 · pago de luz por canal digital · ENCIG 2025 · `edad × escolaridad` · spec v1.1

**Lo que se estima, en una línea:** la **proporción de pagos ordinarios del servicio de luz (`N_TRA == 01`) hechos por canal digital (`P7_3 ∈ {4,5}`: internet/app · cajero o kiosco inteligente) entre los pagos hechos por un canal válido (`{1,2,4,5,6}`)**, por `edad × escolaridad`, en ENCIG 2025, con el **trámite** como unidad. No es «gobierno digital» en general ni «confianza en el Estado». El nombre de la regla del motor (`tramite.gobierno_digital.util_sin_coercion`) no se cambia aquí; el rótulo del estimando sí se precisa. Confirmado por texto del cuestionario: el código `01` de 6.1 es «el pago ordinario del servicio de luz?» en 2021, 2023 y 2025 (nota de `PR #924`, §2).

**Pre-registro de caja.** `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1`, 20/sep/2026, CAJA, rama `acto/gen2-celda-d-piloto-3-commit-1-v1_1`. Sucede a la v1.0 (`GOB-gobierno-digital-exe15-spec-v1_0.md`, `sha256 20c358b6…`), que queda **SUPERADA-SIN-CORRER** (`n_resultados = 0`): su `medir()` era `NotImplementedError` (`PR #924`). **Congelada sin abrir ENCIG 2025**: ni respuestas ni conteos. Firmas de mesa que la habilitan, verbatim en el encargo archivado: **`FP-399`** (S2) y **`FP-400`** (herencia).

**Herencia (FP-400):** esta spec hereda **VERBATIM** de la v1.0 el estimando (§1), la rejilla, las 15 `PUNTUADA` y la `FUERA-DE-SOPORTE` ex ante (§2), los candidatos y sus fórmulas (§3), `λ = 0.8937949410086089` (§3.1), soporte y adjudicación (§4), la lectura secundaria (§4.1) y el B-bis (§4.2). **Cambian tres cosas y sólo tres:** el cuerpo de medición (§5), la semántica de la guardia S2 (§0) y la cláusula de validación de «congelado» (§6). Donde abajo dice «= v1.0», el texto de la v1.0 rige palabra por palabra.

---

## 0 · Condiciones suspensivas, resueltas

- **S1 — cerrada.** `NC-0355` cerró `CAMBIO-MENOR` (`PR #924`): reactivo 7.3, nueve opciones y códigos, `N_TRA=01` y flujo idénticos en 2021/2023/2025; el catálogo de 2025 inserta el trámite `15` y desplaza `15–22 → 16–23`, fuera del estimando. El contrato lo lleva como `s1_veredicto: CAMBIO-MENOR`; el medidor para si recibe otra cosa.
- **S2 — firmada (`FP-399`).** `97` es edad real censurada («97 años o más») y se reconoce como tal; `98`/`99` son no especificada. En 2021 y 2023 el residuo F1-bis (104 / 107 trámites) es 100 % código `98`: la regla no está sacando población real y **se mantiene**. Para 2025, el COMMIT-2 **cuenta** los trámites con código `97`, `98` y `99` con **una sola variable de agrupación** y lo reporta; siguen fuera del universo del cruce para conservar la comparabilidad con la rejilla sellada del árbitro (`60–96`). **Si `97` supera el 1 % de los trámites de la banda 60+ (`60-96 ∪ 97`), el veredicto lleva la marca `RESERVA-S2`; no detiene el piloto.** La guardia S2 del código deja de ser un paro por significado del código y pasa a exigir que `FP-399` figure `FIRMADA` en `forense/firmas-pendientes.tsv` (input del CALC).
- **F3.** Quien congela este COMMIT-1 (esta sesión) **no ejecuta** COMMIT-2 ni COMMIT-3.

## 1 · Qué se estima — = v1.0

`p(adopta canal digital | edad, escolaridad)` en ENCIG 2025 sobre el universo de **pagos de luz realizados** (`N_TRA == 01`). Unidad **TRÁMITE**; desenlace `adopta = P7_3 ∈ {4,5}`, `no adopta = {1,2,6}`, fuera `{3,7,8,9,blanco}`; ponderador `FAC_TRA`; diseño `EST_DIS × UPM_DIS`. Llave de unión trámites↔personas: **`ID_PER`**, `m:1`, validada (la v1.0 la declaraba `(ID_TRA, NT_TIPO)` como llave de fila sin deduplicar; eso sigue: no se deduplica ningún trámite). Identidad de códigos con `tools/medidor_gobierno_digital_encig25.py:12-14,36`.

## 2 · Rejilla — = v1.0

`edad`: `18-29` · `30-44` · `45-59` · `60-96`. `escolaridad` (`NIV`): `HASTA-PRIMARIA {0,1,2}` · `SECUNDARIA {3}` · `MEDIA-SUPERIOR {4,5,6,7}` · `SUPERIOR {8,9}`. 16 celdas · 15 `PUNTUADA` ex ante · `18–29 × HASTA-PRIMARIA` `FUERA-DE-SOPORTE` ex ante (n = 110 en 2021, 70 en 2023). Firma `F1-bis` (`FP-389`): residuo fuera del universo, contado y reportado; coherencia contra marginales recalculados sobre ese mismo universo.

## 3 · Candidatos — = v1.0

| id | rol | qué es |
|---|---|---|
| **C2** | **PISO A VENCER** | `expit(logit p_a + logit p_b − logit p_all)` con marginales de 2025, réplica por réplica |
| C2-compuesto | control | `CALC-C2-COMPUESTO-RESERVADAS-0001`, punto sin IC; se reporta `|C2 − control|` |
| C1a | referencia | compuesto con marginales de 2023 = `expit(logit p₂₃(a,b) − δ₂₃(a,b))`; punto sellado; **IC no derivable** (las réplicas de 2023 no se sellaron) — declarado, no estimado |
| C1b | referencia | `p₂₃(a,b)` directo, punto e IC sellados |
| **S½** | retador | `expit(logit C2 + ½·δ₂₃)`, réplica por réplica sobre C2 |
| **Sλ** | retador | `expit(logit C2 + λ·δ̄)`, `δ̄ = (δ₂₁+δ₂₃)/2`, réplica por réplica sobre C2 |

### 3.1 · `λ` — = v1.0
`λ = 0.8937949410086089` (`τ̂² = 0.02525670198316379`, `σ̄² = 0.003001124084482884`, `Var_entre = 0.028257826067646673`, k = 15). `tests/test_piloto3_v11.py::test_d` la re-deriva de los `DELTA`/`DELTA-EE` sellados y exige coincidencia a 1e-12.

## 4 · Soporte y adjudicación — = v1.0

`PUNTUADA` si `n ≥ 200` en 2021, 2023 **y 2025**; `FUERA-DE-SOPORTE` global si fallan ≥ 5 de 15; `INDECIDIBLE` por celda con las dos condiciones verbatim (`CAREO-ADV-DUELO-diseno-v2:38`: «INDECIDIBLE si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)», L = retador, M = C2, `EE(R) = (IC95sup − IC95inf)/3.92`); un retador **gana** sólo si vence a C2 en ≥ ¾ de las `PUNTUADA` (`INDECIDIBLE` no es vencer; el denominador son todas las `PUNTUADA`).

**Dónde se lee el tercer requisito (precisión de cableado, no cambio de regla):** `n(a,b)` de 2025 exige agrupar la ola reservada por dos variables, y E.6 sólo lo autoriza al código del COMMIT-3. Por eso el COMMIT-2 emite `SOPORTE-HISTORICO` (2021 y 2023) y el COMMIT-3, antes de adjudicar, lee `n₂₀₂₅` y fija `PUNTUADA`/`FUERA-DE-SOPORTE` con la misma regla. La v1.0 §4 decía «sólo se puede verificar en el COMMIT-2»; con guardia de una sola variable, es en el COMMIT-3. La regla no cambia; el momento sí, y se declara aquí.

### 4.1 · Lectura secundaria — = v1.0
`ΔMAE = MAE(C2) − MAE(j)` sobre las `PUNTUADA`, en pp, con IC **réplica por réplica** (`R_r`, `C2_r` y `j_r` de la misma réplica del mismo bootstrap).

### 4.2 · B-bis — = v1.0
Nadie vence **y** límite superior de `ΔMAE ≤ 0.5 pp` (para todos los retadores) → **corroborada**, acotada a cruces de dos ejes estructurales en tres dominios · nadie vence pero algún IC admite `> 0.5 pp` → **falsador débil**, aunque sea la tercera vez · **si ambas caben, manda falsador débil** · un retador vence → limita a C2 sólo en este desenlace, rejilla y ola; C2 sigue adoptado en DIN y TRA (A.10) · Sλ vence y S½ no, o al revés → el hallazgo es sobre **cuánto encoger**. Si las emisiones traen `RESERVA-S2`, el veredicto lleva esa marca.

## 5 · Cuerpo de medición (nuevo)

Dos CALC, dos commits, dos archivos:

| | `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` · `medidor.py` (COMMIT-2) | `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` · `adjudicacion.py` (COMMIT-3) |
|---|---|---|
| ola | **parámetro** del contrato (`ola`, `payload_id`); 2023 sirve de control | ídem |
| carga | payload por id de manifiesto; `sec_7` ↔ `residentes_sec_2` **por `ID_PER`, `m:1`, validado** — nunca por índice de fila | mismo cargador |
| agrupación | **una sola variable**: marginales de edad (4), escolaridad (4) y total; conteo S2 por código | única función autorizada a cruzar 2025: `n(a,b)`, `R(a,b)` |
| bootstrap | UPM con reposición dentro de estrato, singleton de certeza, `PCG64(20260919)`, 10 000 réplicas en bloques de 50 — semilla y réplicas leídas del precedente sellado (`CALC-ENCIG2023-CRUCES-HISTORICOS-0002/spec.yaml:38-40`); el marco de diseño entero entra al sorteo y «caso completo» va dentro de cada máscara | mismas multiplicidades (no dependen de las máscaras) → C2 se reproduce y R comparte réplicas con C2 |
| emite | C2, S½, Sλ con IC por celda; C1a (punto), C1b (punto e IC sellados); control; residuos F1-bis; `S2-EDAD-97/98/99-N/MASA`, `S2-FRACCION-97-EN-60MAS`, `S2-RESERVA`; `SOPORTE-HISTORICO` | soporte definitivo, veredicto por celda, `VENCE-N`, `GANA`, `MAE`, `ΔMAE` con IC, `B-BIS` |
| se niega si | S1 no habilitante; `FP-399` no `FIRMADA`; insumo de 2025 con `ola ≠ 2025` | falta `emisiones_resultados`/`emisiones_sello`, o el sha256 no coincide, o el C2 recalculado no reproduce el sellado a 1e-9, o semilla/réplicas del contrato ≠ selladas |

`resultados:` de cada `spec.yaml` se deriva por comando (`esquema_resultados()`), y la prueba sintética exige que el conjunto emitido sea exactamente ese.

## 6 · Validación de «congelado» (nuevo) — `tests/test_piloto3_v11.py`

Un COMMIT-1 no está congelado si su punto de entrada nunca corrió. Las dos son obligatorias y las dos corrieron en este acto:

- **(a) sintética:** `medir()` de punta a punta sobre un fixture de 7 000 personas (tres estratos, 24 UPM, edades 97/98/99 incluidas) produce las cinco emisiones por celda con IC; `adjudicacion.medir()` corre sobre ese R sintético con sello, ≥ 12 celdas `PUNTUADA`, y se niega sin sello o con sello alterado.
- **(b) de oro, sobre ENCIG 2023 (no reservada):** el mismo código con `ola=2023` reproduce, contra `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, los 16 `n` exactos, `p(a,b)` y `δ` a `< 1e-10` y los IC95 a `< 1e-9`, sobre el universo F1-bis (residuo 107 = 100 % código `98`). **Control, no medición: no se sella como CALC.** Corrió en esta caja (20/sep/2026): 7/7 en verde.
- **(c) reserva:** ningún `ejecucion.json`/`resultados.json`/`sello*` en los dos CALC; ningún archivo versionado trae un `RESULT-GOB-EXE15-2025-MARGINAL*` ni `RESULT-GOB-EXE15-ADJ-2025-*`; el medidor no nombra `encig25_base_datos_csv.zip` ni `data/raw`.
- **(d) λ** re-derivada de los sellados = congelada.

## 7 · Lo que esta spec NO autoriza — = v1.0

No adjudica ni corona; no re-rotula `CALC-PISO-PERSISTENCIA-ERROR-0001`; no toca marcador, rejilla del árbitro ni CALC sellados; las 7 celdas con IC95 de δ que excluye 0 en 2023 no son evidencia confirmatoria independiente.

## 8 · Auditoría (afirma sobre México) — = v1.0

El universo son **pagos de luz realizados**: excluye a quien no pagó luz (o no la tiene contratada a su nombre), más rural, más informal. `edad × escolaridad` en pago digital es, antes que actitud hacia el Estado, **brecha de acceso, conectividad y alfabetización digital por cohorte**; y el canal de pago de la CFE es tanto oferta (app, bancos, tiendas) como demanda. **Peligroso leído simplista:** «+11 pp» = «los mexicanos ya confían en el gobierno digital» — ni el signo ni la magnitud autorizan esa lectura, y con instrumento comparable (`NC-0355`) el +11 pp aún puede ser cambio de canal, no de disposición. Evidencia clase (a).

El primer resultado que produzca este procedimiento es el que se reporta.
