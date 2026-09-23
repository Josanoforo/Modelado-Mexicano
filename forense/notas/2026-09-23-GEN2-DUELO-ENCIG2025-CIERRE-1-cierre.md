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
