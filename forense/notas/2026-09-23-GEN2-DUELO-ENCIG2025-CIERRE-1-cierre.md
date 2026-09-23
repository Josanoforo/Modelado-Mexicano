# ACTO GEN2-DUELO-ENCIG2025-CIERRE-1 · nota

Encargo: `forense/encargos/2026-09-23-GEN2-DUELO-ENCIG2025-CIERRE-1.md` (0-bis `657c88d1`, sello de
cuerpo `410d75dc…`). Spec: `forense/prereg-caja/ENCIG-DUELO-2025-cierre-spec-v1_0.md` (COMMIT-1
`5e0a357b`). Rama `acto/gen2-duelo-encig2025-cierre-1`, CAJA, una sola sesión (Opus).

## 0 · ARRANQUE

- **0.a** `git fetch --prune`; `git rev-list --count HEAD..origin/main` → `0` (base `73b7f115`,
  PR #1036). Al congelar, `origin/main` había avanzado 17 commits (hasta `ef9ff6ca`, PR #1050): se
  fusionó (`00e9def7`) sin conflicto antes de los `preflight`. No es PARO.
- **0.b** `git status --porcelain` → vacío.
- **0.c** `git ls-remote --heads origin | grep -ic "encig2025-cierre"` → `0` (sobre 10 ramas
  remotas); `git worktree list | grep -i encig2025` → sólo el worktree propio; `gh pr list --search
  "ENCIG2025-CIERRE" --state open` → vacío.
- **0.d** `tools/limpia_arbol.py --reporta`: base al día; 2 ramas remotas `fuera_de_politica`
  (`acto/gen2-tramite-firmas-11`, `acto/gen2-tuberia-rutinas-automerge-2`), ajenas.
- **REPO** `/home/pc0/mm-gen2-duelo-encig2025-cierre-1` (worktree nuevo sobre `origin/main`).
  **SHA** encargo `f28d1038` → base `73b7f115` (main movido, no PARO; re-derivado abajo).
  **data/raw** enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre.
- **ENTORNO** (`python3 tools/entorno.py --arranque`): `ENTORNO-DERIVADO = CAJA` ·
  `senal-corpus: montado=SI archivos_examinados=438` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`
  · `red: PERMITIDA (http_code=200)`. Coincide con el encargo (CAJA).
- **MODELO.** El encargo exige Opus («mide; no bajar»); la sesión arrancó en Sonnet 5 y mesa la
  pasó a Opus (`/model`) antes del 0-bis. Todo lo sustantivo corrió en Opus.
- **COMPUERTA.** El encargo no trae línea `GATED a`/`COMPUERTA:`; su §8 declara compuertas que
  protegen abrir dato / congelar / adoptar / borrar.

## 1 · Firmas y preguntas a mesa (verbatim)

Pregunta de la sesión (PARO f: la firma §2 no estaba en el repo) → **mesa, 23/sep/2026: «Firmada
verbatim»**. Asentada como `FP-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-01` FIRMADA (A.12), y
congelada como constancia en `tools/encig/duelo_2025/constancia-firma-657c-01.tsv`.

Pregunta §6 (marcador y celda-D discrepan sobre `edadxescolaridad`) → **mesa: «Consumido; NC al
marcador»**. `edad × escolaridad` no se reabre; la NC va al derivador del marcador.

## 2 · Premisas del encargo, verificadas

| premisa (rótulo) | verificación | resultado |
|---|---|---|
| 3 cruces RESERVADA en el marcador (EJECUTADO) | `grep` en `data/corrida0/marcador-segmento.tsv` | se sostiene: `edadxescolaridad`, `edadxsexo`, `escolaridadxsexo` |
| FIRMAS-9 P2 consumió `edad × escolaridad` (LEÍDO) | celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` l.84-86 | adjudicada (`FALSADOR-DEBIL`, `champion_actual: C2`) → **dos cruces**, rama que el propio encargo previó |
| #1030 en main (EJECUTADO) | `gh pr view 1030` MERGED; `git merge-base --is-ancestor de7bc272 origin/main` | se sostiene; recibo #1033 FUSIONAR-CON-NC (la NC era el cotejo celda por celda, que corre aquí) |
| piloto 4 heredable por sha (LEÍDO) | `git show 5939e9d4:…/medidor.py \| sha256sum` = `6d4668fd…` = blob de hoy | se sostiene; el árbitro heredado es la versión corregida `7ffa0a0e` (enmienda 2) |
| `PILOTO-5-ENCOGIDA-ENCIG-1` + ADENDA-1 (EXISTE) | no están en el repo | mesa lanzó este encargo: aquel queda sustituido por éste (NO-CORRIDO) |
| réplicas/estratos suficientes en ENCIG 2025 (SUPUESTO) | `CALC-ARBITRO-MARGINALES-ENCIG2025-0001` y el árbitro del piloto 3 ya corrieron bootstrap UPM-en-estrato sobre esta ola | se sostiene por precedente sellado; el RESULT no lleva apellido especial |
| payload `encig_2025_encig` (texto del encargo) | `data/manifiesto.yaml` | el id es `encig25_base_datos_csv` (sha `47daf2f7…`); logística |
| nada hecho (§4) | `ls data/corrida0 \| grep -c 'ENCIG-DUELO-2025\|PILOTO-5'` → 0; ramas remotas → 0 | se sostiene |
| concurrencia §9: `codex/astra3-encig-persistencia-1` no toca 2025 | fusionada como PR #1041 (`412f2800`); su diff: 0 líneas con `encig25/encig_2025/encig2025` (control: 64 con `encig23`/`2023`) | sin PARO (a) |

Hallazgos de diseño que la spec absorbe (no tocan qué se mide): la receta ENCIG cambió de blob
después de sellar el histórico 2023 (`3899d086…` → `31d7cf3b…`) — se importa pinneada y el oro
prueba que reproduce; el C2 compuesto no trae IC (sus `DIAG` no son IC95) y el contrato v0.6 de
celda-D exige IC para adoptar — el árbitro lo emite por réplica, rotulado `NACE-CON-R`.

## 3 · COMMIT-1 y D-22 — salida cruda

**Qué congela** `5e0a357b`: spec humana + sidecar; `spec.yaml` de
`CALC-ENCIG-DUELO-2025-{EDADXSEXO,ESCOLARIDADXSEXO}-EMISIONES-0001` y
`CALC-ENCIG-DUELO-2025-ADJUDICACION-0001`; `tools/encig/duelo_2025/duelo.py` (`74e8aa49…`),
depositado byte a byte como `medidor.py` en los tres; `tests/test_encig_duelo_2025.py`; firma §2.

**(1) `corrida0 preflight`** sobre `00e9def7` (COMMIT-1 con `origin/main` fusionado):

```
CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001        PRE-FLIGHT: VERDE  (6/6 inputs repo COINCIDE; spec_md NO-EN-MAIN, aviso)
CALC-ENCIG-DUELO-2025-ESCOLARIDADXSEXO-EMISIONES-0001 PRE-FLIGHT: VERDE  (6/6 inputs repo COINCIDE; spec_md NO-EN-MAIN, aviso)
CALC-ENCIG-DUELO-2025-ADJUDICACION-0001               [COINCIDE] encig25_base_datos_csv origen=manifiesto raiz=data_raw
PRE-FLIGHT: BLOQUEADO input_repo_ausente=emisiones_edadxsexo_resultados:… input_repo_no_commiteado=emisiones_edadxsexo_resultados
  input_repo_ausente=emisiones_edadxsexo_sello:… input_repo_no_commiteado=emisiones_edadxsexo_sello
  input_repo_ausente=emisiones_escolaridadxsexo_resultados:… input_repo_no_commiteado=emisiones_escolaridadxsexo_resultados
  input_repo_ausente=emisiones_escolaridadxsexo_sello:… input_repo_no_commiteado=emisiones_escolaridadxsexo_sello
```

El árbitro bloquea **exactamente** por los cuatro inputs de COMMIT-3a y por nada más (declarado en
su `spec.yaml`, `preflight_esperado_antes_del_commit_3a`). El payload de 2025 sólo se hasheó.

**(2)–(3) conducto y nulos.** `pytest tests/test_encig_duelo_2025.py -v` sobre `00e9def7`:

```
test_a_todo_con_soporte PASSED
test_a_soporte_parcial PASSED
test_a_fuera_de_soporte_global PASSED
test_a_cero_puntuadas_y_lambda_k_insuficiente PASSED
test_a_celda_vaciada_en_una_replica PASSED
test_a_categoria_con_masa_cero PASSED
test_a_control_no_reproduce_no_emite_ic_de_c2 PASSED
test_a_astra_no_entra PASSED
test_b_oro_encig2023_reproduce_cruces_y_marginales_sellados PASSED
test_c_emision_para_sin_firma_o_con_input_de_2025 PASSED
test_c_arbitro_para_sin_sello_o_sello_falso PASSED
test_c_guardia_de_pares PASSED
test_c_firma_asentada_y_congelada PASSED
test_c_reserva_en_los_calc PASSED
test_d_lambda_se_rederiva_y_es_la_del_piloto4 PASSED
test_e_mutantes_atrapados PASSED
test_f_medidores_byte_a_byte PASSED
test_f_resultados_del_spec_son_el_esquema PASSED
test_f_estado_gana_es_la_del_piloto4 PASSED
test_f_inputs_de_los_spec_existen_con_su_sha PASSED
20 passed in 20.36s
```

Cada rama `test_a_*` pasa `corrida0._valida_outputs(spec, out) == []` contra el `resultados:` del
`spec.yaml` real y exige que ningún flotante sea NaN/inf. El test fue corregido una vez antes de
congelar: el fixture de «celda vaciada en una réplica» ponía una persona de la misma celda en la
otra UPM del estrato, de modo que ninguna réplica podía vaciarla (defecto del fixture, no del
medidor).

**Oro ENCIG 2023** (receta de hoy desde sus bytes, 10 000 réplicas, `PCG64(20260919)`):

```
payload encig23_base_datos_csv: COINCIDE af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d
celdas=16 N identico=16/16 replicas=10000 semilla=20260919
max |dif| vs CALC-ENCIG2023-CRUCES-HISTORICOS-0002: {'P': '0.000e+00', 'P-IC-LO': '0.000e+00', 'P-IC-HI': '0.000e+00', 'P-EE': '0.000e+00', 'DELTA': '5.551e-17', 'DELTA-EE': '0.000e+00'}
max |dif| 10 marginales de un eje vs CALC-PISOS-ENCIG2023-EJES-0002: 0.000e+00
diagnostico receta 2023: {'FILAS-EVENTOS': 123186, 'JOIN-SIN-DEMOGRAFIA': 0, 'N-UNIVERSO': 20934, 'N-DISENO-VALIDO': 20934, 'P7-3-EXCLUIDAS': 122}
```

**Ejecución diagnóstica declarada (spec §7):** `emisiones` sobre sus insumos reales por el conducto
de `corrida0` (`preflight` → `_ejecuta` → `_valida_outputs`), después del COMMIT-1. Se registró
sólo esto; los números no se leyeron:

```
CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001 preflight VERDE exit 0 err - outputs 221 nulos 0 _valida_outputs 0 sha256(json canonico) 757ad5121555d3c23ea32235e6f10c5f2bce7c69ac19e48bab100526fae21830
CALC-ENCIG-DUELO-2025-ESCOLARIDADXSEXO-EMISIONES-0001 preflight VERDE exit 0 err - outputs 221 nulos 0 _valida_outputs 0 sha256(json canonico) 1007e03c7fceb385d382493ff1eea2242b2c1d8928582478cf1803fe0b0c514e
```

El `run` del COMMIT-2 tiene que dar esas dos huellas.

**(4)** Ningún input con hash sobre un archivo vivo: la firma entra como constancia (cabecera + su
fila), no como el libro `forense/firmas-pendientes.tsv`.

**Auditoría y mutación.** `auditoria(duelo.py)` → `[]`; los cinco mutantes (sin guardia de
emisiones · sin guardia de sellos · par consumido autorizado · emisión que lee 2025 · máscara sin
guardia) son atrapados (`test_e`). `tools/ci_guardias.py --ejecuta-huerfanos` → el test nuevo
`SKIP` por dependencia, `fallidos=0`. `tests/check.py --rapido` → `0 FAIL · 336 WARN` (dos FAIL de
forma corregidos antes del commit: T02 por la copia íntegra del libro de firmas, reemplazada por
la constancia; T22 por dos frases de la spec que mencionaban un pendiente hipotético con los
tokens del patrón).

## 4 · COMMIT-2, COMMIT-3a, COMMIT-3 — el orden del diff es el sello

| paso | commit | qué |
|---|---|---|
| COMMIT-2 (1/2) | `6f0aebea` | `corrida0 run CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001` → SELLADO; json canónico `757ad512…` = la ejecución diagnóstica, bit a bit |
| COMMIT-2 (2/2) | `96460709` | `…-ESCOLARIDADXSEXO-EMISIONES-0001` → SELLADO; `1007e03c…` = la diagnóstica, bit a bit; **las dos, en origin** (`git cat-file -e FETCH_HEAD:…/sello.json`) antes de seguir |
| COMMIT-3a | `1de91d9a` | cuatro líneas `sha256` en el `spec.yaml` del árbitro (`git diff --stat`: 4 inserciones, nada más); `preflight` → VERDE, 8/8 inputs COINCIDE |
| COMMIT-3 | `dc732db7` | `corrida0 run CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` → SELLADO al primer intento (14.7 s); **primera y única apertura de los dos cruces de ENCIG 2025** |

Controles del árbitro, antes de adjudicar: auditoría de su código `LIMPIA`; sellos de las dos
emisiones `COINCIDEN`; 11 marginales de un eje contra `CALC-ARBITRO-MARGINALES-ENCIG2025-0001`:
`max |dif| = 0.0`, `N` discordantes `0` → `REPRODUCE`; composición contra el C2 sellado:
`2.99e-07` (edad×sexo) y `5.56e-07` (escolaridad×sexo) ≤ `1e-5` → `REPRODUCE`. Universo 2025:
`N-UNIVERSO = N-DISENO-VALIDO = 20 203` trámites (el bloque público dice 20 203), `P7-3-EXCLUIDAS
= 189`, `JOIN-SIN-DEMOGRAFIA = 0`; residuo del par edad×sexo = 115 (edad fuera de 18-96).

**E.7 — asientos** (`tools/verifica_aislada.py`, un intérprete por CALC; `forense/replay-evidencia.tsv`):

```
CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001--0a80be9cb9d4          REPRODUCE IDENTICO 221/221 max|delta| 0.0
CALC-ENCIG-DUELO-2025-ESCOLARIDADXSEXO-EMISIONES-0001--6f0aebea62c7   REPRODUCE IDENTICO 221/221 max|delta| 0.0
CALC-ENCIG-DUELO-2025-ADJUDICACION-0001--1de91d9af6b4                 REPRODUCE IDENTICO 498/498 max|delta| 0.0
```

La vista (`corridas.tsv`/`resultados.tsv`) no viaja en el PR: desde #1050 la publica el job de
`main` a partir de estos asientos (`lote_desde_asientos.py --incluir-pendientes`). Hasta que mesa
fusione, las tres corridas están **selladas en disco, asentadas, no registradas en la vista**.

## 5 · Resultados — tabla de la comparación primaria

Unidad: **trámite** (pago ordinario de luz). Escala: puntos porcentuales. Todas las emisiones
comparadas son **PROSPECTIVA** (selladas antes de que existiera R). ΔMAE = MAE(C2) − MAE(retador),
positivo = el retador erró menos; IC 2.5/97.5 sobre 10 000 réplicas de R con los puntos fijos.

| cruce | candidato | MAE vs R (pp) | ΔMAE vs C2 (pp) [IC95] | GANA | celdas GANA / INDEC. (descr.) | cobertura R∈IC (Wilson) |
|---|---|---:|---|---|---|---|
| edad × sexo | **C2 (piso)** | 0.966 | — | — | — | IC nace con R (no se cuenta) |
| edad × sexo | C7 | 0.776 | +0.189 [−0.367, +0.565] | NO | 0 / 8 | 6/8 [0.41, 0.93] |
| edad × sexo | C-ENCOGIDA (λ = 0.519) | 0.776 | +0.190 [−0.169, +0.334] | NO | 0 / 8 | 2/8 [0.07, 0.59] |
| edad × sexo | C-ASTRA | 0.775 | +0.191 [−0.266, +0.480] | NO | 0 / 8 | 8/8 [0.68, 1.00] |
| edad × sexo | C1 (referencia 2023) | 11.192 | — | — | — | 0/8 [0.00, 0.32] |
| escolaridad × sexo | **C2 (piso)** | 1.007 | — | — | — | IC nace con R (no se cuenta) |
| escolaridad × sexo | C7 | 1.459 | −0.452 [−0.488, +0.332] | NO | 1 / 7 | 4/8 [0.22, 0.78] |
| escolaridad × sexo | C-ENCOGIDA (λ = 0.540) | 1.252 | −0.244 [−0.245, +0.265] | NO | 0 / 8 | 2/8 [0.07, 0.59] |
| escolaridad × sexo | C-ASTRA | 1.353 | −0.346 [−0.366, +0.318] | NO | 0 / 8 | 8/8 [0.68, 1.00] |
| escolaridad × sexo | C1 (referencia 2023) | 10.312 | — | — | — | 0/8 [0.00, 0.32] |

| cruce | B-bis (spec §4.1) | celda-D `veredicto` | `champion_actual` |
|---|---|---|---|
| edad × sexo | **FALSADOR-DEBIL** (nadie vence; el IC superior de C7 es 0.565 > 0.5) | FALSADOR-DEBIL | C2 |
| escolaridad × sexo | **CORROBORADA** (nadie vence; los tres IC superiores ≤ 0.5: 0.332, 0.265, 0.318) | SIN-CANDIDATO-SUPERIOR | C2 |
| **agregado** | **FALSADOR-DEBIL** (manda por precedencia) | — | — |

λ por cruce (método de momentos del piloto 4, `k = 8`, `K-SUFICIENTE`): edad×sexo `τ̂² = 9.49e-04`,
`σ̄² = 8.81e-04`, `λ = 0.5185`; escolaridad×sexo `τ̂² = 1.10e-03`, `σ̄² = 9.34e-04`, `λ = 0.5404`.
Soporte: 8/8 `PUNTUADA` en los dos cruces (n₂₀₂₅ mínimo 1 086; ninguna celda falla). Punto del
candidato dentro del IC de R: C2 8/8 y 7/8; C7, C-ENCOGIDA y C-ASTRA 8/8 y 8/8; C1 0/8 y 0/8.

**Por celda** (`RESULT-ENCIG-DUELO-2025-ADJ-…`; `d` = |candidato − R| en pp; H = hombre, M = mujer):

**edad × sexo**

| celda | n₂₀₂₅ | R [IC95] | C2 | C7 | C-ENC | C-ASTRA | C1 | d C2 / C7 / C-ENC / C-ASTRA | veredicto C7 / C-ENC / C-ASTRA vs C2 | δ₂₅ | δ̄ hist. |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| 18-29×H | 1489 | 0.7545 [0.7169, 0.7898] | 0.7585 | 0.7478 | 0.7530 | 0.7502 | 0.6407 | 0.40 / 0.67 / 0.15 / 0.44 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.023 | -0.057 |
| 18-29×M | 1317 | 0.7485 [0.7115, 0.7841] | 0.7448 | 0.7562 | 0.7508 | 0.7537 | 0.6306 | 0.36 / 0.77 / 0.23 / 0.52 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.021 | +0.061 |
| 30-44×H | 3331 | 0.7756 [0.7501, 0.7993] | 0.7810 | 0.7854 | 0.7833 | 0.7845 | 0.6745 | 0.54 / 0.98 / 0.77 / 0.90 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.033 | +0.026 |
| 30-44×M | 3677 | 0.7739 [0.7527, 0.7940] | 0.7682 | 0.7644 | 0.7662 | 0.7651 | 0.6319 | 0.57 / 0.95 / 0.77 / 0.88 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.034 | -0.021 |
| 45-59×H | 2803 | 0.6920 [0.6648, 0.7181] | 0.6771 | 0.6838 | 0.6806 | 0.6825 | 0.5674 | 1.49 / 0.82 / 1.14 / 0.95 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.067 | +0.031 |
| 45-59×M | 2996 | 0.6480 [0.6211, 0.6742] | 0.6609 | 0.6561 | 0.6584 | 0.6570 | 0.5056 | 1.29 / 0.80 / 1.04 / 0.90 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.055 | -0.022 |
| 60-96×H | 2331 | 0.4976 [0.4663, 0.5287] | 0.4848 | 0.4902 | 0.4876 | 0.4891 | 0.4137 | 1.27 / 0.73 / 0.99 / 0.84 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.049 | +0.022 |
| 60-96×M | 2144 | 0.4485 [0.4154, 0.4829] | 0.4666 | 0.4533 | 0.4597 | 0.4563 | 0.3788 | 1.81 / 0.48 / 1.12 / 0.78 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.071 | -0.053 |

**escolaridad × sexo**

| celda | n₂₀₂₅ | R [IC95] | C2 | C7 | C-ENC | C-ASTRA | C1 | d C2 / C7 / C-ENC / C-ASTRA | veredicto C7 / C-ENC / C-ASTRA vs C2 | δ₂₅ | δ̄ hist. |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| HASTA-PRIMARIA×H | 1086 | 0.4129 [0.3678, 0.4574] | 0.4006 | 0.3837 | 0.3914 | 0.3879 | 0.3026 | 1.23 / 2.93 / 2.15 / 2.50 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.051 | -0.071 |
| HASTA-PRIMARIA×M | 1213 | 0.3717 [0.3300, 0.4146] | 0.3832 | 0.4011 | 0.3928 | 0.3970 | 0.3204 | 1.15 / 2.94 / 2.11 / 2.54 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.049 | +0.075 |
| SECUNDARIA×H | 2040 | 0.5775 [0.5417, 0.6124] | 0.5735 | 0.5717 | 0.5725 | 0.5721 | 0.4568 | 0.40 / 0.57 / 0.49 / 0.54 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.016 | -0.007 |
| SECUNDARIA×M | 2176 | 0.5520 [0.5183, 0.5859] | 0.5555 | 0.5591 | 0.5574 | 0.5584 | 0.4207 | 0.35 / 0.71 / 0.54 / 0.64 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.014 | +0.014 |
| MEDIA-SUPERIOR×H | 2674 | 0.6922 [0.6652, 0.7190] | 0.6864 | 0.6833 | 0.6847 | 0.6839 | 0.5753 | 0.59 / 0.90 / 0.75 / 0.83 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | +0.027 | -0.014 |
| MEDIA-SUPERIOR×M | 2908 | 0.6652 [0.6374, 0.6934] | 0.6704 | 0.6746 | 0.6727 | 0.6737 | 0.5388 | 0.52 / 0.94 / 0.75 / 0.85 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.024 | +0.019 |
| SUPERIOR×H | 4198 | 0.8004 [0.7793, 0.8206] | 0.8184 | 0.8124 | 0.8152 | 0.8136 | 0.7344 | 1.80 / 1.20 / 1.48 / 1.32 | INDECIDIBLE / INDECIDIBLE / INDECIDIBLE | -0.117 | -0.040 |
| SUPERIOR×M | 3908 | 0.8274 [0.8097, 0.8444] | 0.8072 | 0.8125 | 0.8101 | 0.8114 | 0.7253 | 2.01 / 1.49 / 1.73 / 1.60 | GANA-CHALLENGER / INDECIDIBLE / INDECIDIBLE | +0.135 | +0.034 |

Lectura descriptiva, no adjudica: en escolaridad × sexo la interacción de 2025 (`δ₂₅`) tiene signo
opuesto al promedio histórico (`δ̄`) en 6 de 8 celdas; en edad × sexo coincide en 6 de 8. Por eso
toda corrección hacia la historia empeora en escolaridad × sexo y mejora poco en edad × sexo: la
interacción de estos pares es pequeña (|δ| ≤ 0.14 logit) y no persiste lo bastante entre olas.

## 6 · Dictamen (firma §2) y frase de producto por cruce

**Nadie vence.** Por la firma §2, la serie de retadores de la casa sobre ENCIG (C7, C-ENCOGIDA) y
el candidato externo C-ASTRA se cierran con este dictamen, que va al informe v1.3: **FALSADOR-DEBIL**
agregado; CORROBORADA en escolaridad × sexo, FALSADOR-DEBIL en edad × sexo. No hay FP de adopción
(ningún retador despejó ni 0 ni el umbral), ni `PROPUESTA-CON-RESERVA`. ENCIG 2025 queda **sin
reserva** en sus tres pares (edad × escolaridad, piloto 3; los dos de aquí). La próxima prueba
prospectiva de ENCIG es la ola 2027 (`MISION-ASTRA-4`).

- **edad × sexo (PROSPECTIVA, unidad trámite).** Para estimar qué proporción de pagos de luz se hace
  por internet o cajero en cada combinación de edad y sexo, en ciudades de 100 mil habitantes o más,
  combinar los dos marginales publicados de 2025 (C2) es el estimador adoptado: erró 0.97 pp en
  promedio sobre 8 celdas. Las tres correcciones por interacción histórica erraron 0.19 pp menos,
  pero el intervalo de esa ganancia va de −0.37 a +0.57 pp: no se demuestra mejora, **y tampoco se
  descarta una de hasta ~0.57 pp**. Acotado, no corroborado.
- **escolaridad × sexo (PROSPECTIVA, unidad trámite).** Mismo estimando: C2 erró 1.01 pp en
  promedio sobre 8 celdas y es el estimador adoptado; las tres correcciones erraron **más** (entre
  0.24 y 0.45 pp más), y ninguna mejora compatible con los datos supera 0.33 pp. Corroborado: para
  este par, los marginales sin interacción son el estimador honesto de celda.

Ninguna frase mezcla columnas: todas las cifras de candidatos son PROSPECTIVA y de unidad trámite;
C1 (persistencia 2023, error medio 10–11 pp) es referencia y no se promedia con nada; el IC de C2 que
cita la celda-D **nace con R** y no se reporta como cobertura.

## 7 · Registro

- Celdas-D nuevas, v0.6, `unidad_objetivo: evento`, `champion_actual: C2` por la firma del 17/sep y
  la §2 (este acto no adopta retadores): `GOB.gobierno_digital.encig2025.edad_x_sexo.yaml`
  (`veredicto: FALSADOR-DEBIL`) y `…escolaridad_x_sexo.yaml` (`veredicto: SIN-CANDIDATO-SUPERIOR`,
  B-bis CORROBORADA); `margen_material` = MAE de C2; generadas desde los RESULT sellados;
  `python3 tests/test_celdas_d.py` → 12/12 validan.
- **Derivador del marcador** (pregunta a mesa, respuesta verbatim: **«Arreglo de 2 líneas
  (Recomendado)»**): `tools/marcador_segmento.py` deja de fijar `{edad, escolaridad}` para toda
  celda-D `GOB.` y deriva el par del id. Medido: derivación en memoria → **0** grupos `RESERVADA`
  de ENCIG 2025 (21 → 19 grupos reservados en todo el marcador; 32 filas GOB `ADOPTADO-POR-FIRMA`).
  `tests/test_marcador_segmento.py` `T-VEINTE-ADOPTADAS` 36 → 52 (+16 de este acto), 13/13 PASA.
- El TSV publicado `data/corrida0/marcador-segmento.tsv` sigue con 3 `RESERVADA` de ENCIG 2025:
  es derivado protegido (no viaja en el PR) y el job publicador de #1050 todavía **no** lo
  re-deriva (`verify.yml`: «El marcador, la demanda y usos.tsv quedan pendientes»). Por eso
  `edadxescolaridad` aparecía `RESERVADA` en main aunque el código ya lo daba por pilotado: era un
  derivado desfasado, no una reserva viva. NC abajo.
- `data/INFRAESTRUCTURA-v1_0.md`: enmienda fechada que registra las dos celdas-D (T27).

## 8 · Contadores

`cuenta_gen2 = SI` en los tres CALC (etiqueta de la spec; el registro lo resuelve al publicarse).
**Corridas selladas: +3** (dos emisiones + la adjudicación), asentadas en `replay-evidencia.tsv`,
**no registradas en la vista** hasta que mesa fusione (canal #1050). **Celdas-D con veredicto
sellado: +2** (16 celdas de cruce). **`celdas_validadas`: 92 → 92 (Δ0)** @ `dc732db7`, medido con
`python3 tools/celdas_validadas.py --linea` con y sin las dos celdas-D: la métrica busca el error
por celda con dos patrones fijos (`-C2-D-PP`, `-ARB-D-C2-`) y un CALC de R por celda-D, y este
árbitro emite `…-D-C2` para dos cruces a la vez. Las cuatro celdas-D del piloto 4 están en la misma
situación (`clase_1_celdas_d_sin_contar`, mismo motivo). No se parcha aquí (no es ≤10 líneas, y
filtrar por cruce rompería el emparejamiento del piloto 3): NC y FP abajo. Adopciones de retadores:
**0**. FP nuevas: la firma §2 (FIRMADA) y dos preguntas a mesa.

## 9 · Auditoría de rigor extremo

¿Contadores movidos? Corridas +3, celdas-D +2, `celdas_validadas` 0 (por cableado, declarado).
¿Escala y comparación? Todo en pp de proporción de **trámites** de pago de luz; ΔMAE compara
errores del mismo universo y la misma R; nada se compara con cifras por persona ni con otros
trámites. ¿PROSPECTIVA/RETROSPECTIVA mezcladas? No: candidatos PROSPECTIVA; el IC de C2 se rotula
`NACE-CON-R` y queda fuera de la cobertura. ¿Qué cambia con foco rural/popular? Todo lo de aquí vale
sólo para ciudades de 100 mil habitantes o más (universo de ENCIG). Pagar la luz por internet o en
cajero supone cuenta o tarjeta, conectividad, recibo a nombre propio y oferta de cajeros, que es
urbana. En lo rural y popular el canal presencial domina por oferta, no por preferencia, y este
resultado no se transporta. ¿Qué parece psicológico y es incentivo u oferta? El gradiente por edad
(0.45–0.50 en 60-96 frente a 0.75–0.78 en 18-44) y por escolaridad (0.37–0.41 en hasta primaria
frente a 0.80–0.83 en superior) es primero acceso (bancarización, conectividad, habilidades
digitales), antes que «cultura digital». ¿Sobregeneralización de clase media urbana? Sí es el
riesgo: el denominador es quien pagó, y quien paga en línea es desproporcionadamente bancarizado.
¿Sexo? Las diferencias hombre/mujer dentro de cada edad o escolaridad son chicas y sin
interacción demostrable (R: 0.2–4.9 pp entre sexos por celda); si aparecieran, lo primero a descartar es composición (quién es titular
del contrato de luz en el hogar), no conducta. ¿Evidencia débil con intuición fuerte? La lectura
«la interacción no persiste» se apoya en dos pares y dos olas: es evidencia media, no ley.
¿Peligroso leído simplista? «Los mayores no usan lo digital»: el trámite de quien no pagó, o pagó
otro miembro del hogar, no está en el denominador.

## 10 · Hallazgos de aparato (una línea cada uno en `forense/hallazgos.md`)

- El derivador del marcador fijaba el par GOB a mano (arreglado aquí, firma de mesa).
- `celdas_validadas` no ve árbitros multi-cruce ni el sufijo `-D-C2` (piloto 4 y este acto): NC y FP.
- El contrato v0.6 exige punto e IC del campeón en **un** CALC, y el marcador exige emisión y R en
  CALC **distintos** para rotular PROSPECTIVA. Con E.6 (nada de 2025 antes del COMMIT-2), un piso
  sin IC propio (C2 compuesto) sólo puede adoptarse con un IC que nace con R: la fila adoptada sale
  `ORDEN-NO-DERIVABLE` por construcción. Pregunta a mesa (FP).
