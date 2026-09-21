# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3` · congelado: **292 ids declarados anulables en EMISIONES** (9 marginal `-P` · 27 marginal EE/IC · 48 candidato `-P` · 144 candidato EE/IC · 32 C1A-IC · 32 control y |C2−control|) **y 174 en ADJUDICACION** (16 `-R-P` · 48 R EE/IC · 16 `-DELTA-25` · 80 `-D-PP` · 11 MAE/ΔMAE de retadores y C2 · 2 MAE C1A/C1B · 1 umbral); **8 de 8 caminos pasan `corrida0._valida_outputs` con cero problemas y cero valores no finitos** (los siete de §5 P3 más la adjudicación con oro 2023 como R); sin tocar una línea de código

**Veredicto del piloto: NO HAY, y este acto no lo busca.** Universo: pagos ordinarios del servicio de luz (`N_TRA == 01`), unidad TRÁMITE, escala proporción/pp. Cero corridas selladas, cero cifras de 2025, cero contadores movidos (`CONTADOR: NO-APLICA`). Lo que entrega es la **condición de sellabilidad** que a `#951` le faltó: el `spec.yaml` de cada CALC declara todo `null` que el código congelado puede emitir, y el validador que sella lo acepta en cada rama terminal, incluida la que sólo se alcanza después de derivar el cruce.

Entorno **CAJA** (`ENTORNO-DERIVADO = CAJA`, WSL2, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, `montado=SI archivos_examinados=420`, red PERMITIDA http 200), Opus 5, sesión `165ce648`, sin sub-agentes, **MODO RÍGIDO**. Encargo archivado verbatim (A.3) con sello de cuerpo `684d0213…1708d`, idéntico al `.sha256` que lo acompañó en `Descargas MX` (`sha256sum -c` → `OK` sobre los dos archivos recibidos, encargo y `ensayo-rama5-celda-rara.py`). 0-bis `5870e652`, empujado y confirmado por `git ls-remote`. Base: `origin/main = 4bb29d96` (el encargo declaraba `346ab2bc`; main se movió **21 commits** — `#949`, `#956`, `#957` y el censo del día —; ninguno toca los dos CALC ni la spec humana; re-derivado, no es PARO). `ADR-589` (el candidato contiguo era 588; `PR #947` fusionó primero con `ADR-588` mientras este acto cerraba — renumerado 588 → 589, regla de la casa).

---

## 0 · Para mesa, en una página

**F3, declarado.** El encargo dice «congela la sesión de `#944`». Esta sesión es **nueva** (`165ce648`): no es la de `#944` ni la de `#951` (`c0ab3df1`, que corrió el medidor sobre 2025 y por prudencia se excluyó de congelar). No corrió el medidor sobre 2025, no abrió ENCIG 2025 más allá del `sha256` del preflight, no leyó diseños A/B ni careo. Cumple «quien congela no ejecuta»: los COMMIT-2/3a/3 los ejecuta otra sesión. Si mesa quería literalmente la sesión de `#944`, que lo diga: la salida de este acto no depende de qué sesión tecleó.

**Qué cambió, exactamente.** Sólo los dos `spec.yaml`:
- **P1** — `permite_no_estimable: true` en **292 / 565** ids de EMISIONES y **174 / 349** de ADJUDICACION, cada uno con la causa y la línea de código pegada a su `unidad` (edición línea a línea; el diff son esas dos líneas por id y nada más — verificado por diff estructural: cero llaves raíz cambiadas, cero ids añadidos/quitados/reordenados, cero `tipo` cambiado).
- **P2** — bloque `ejecucion_previa:` en EMISIONES: la corrida de `#951` (21/sep, 13,76 s, 565 RESULT, 40 `null`, descartados por `corrida0` antes de escribir, ninguna cifra vista) y por qué re-correr no es un segundo resultado (E.5, firma de mesa).
- **P4** — llave `commit_3_cierre_control_60_96` en `secuencia_commits` de ADJUDICACION: las cuatro restas |C2 − control `-60-X-`| se asientan al cierre del COMMIT-3 como **aritmética derivada** entre sellados, no como RESULT.

**Intactos, byte a byte contra `826bf3a1`** (`git hash-object` = blob en `826bf3a1`): `medidor.py` (`05d4c205…`), `adjudicacion.py` (`0727a18b…`), `forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` (`62d8d07d…`) y su `.sha256`.

**Cuenta de dirección contra la mía.** Coinciden exactas: **292 y 174**, origen por origen (§2). No encontré ningún sitio adicional que emita `None` fuera de los listados. Sí encontré **un sitio que puede emitir un no finito** —no un nulo— y lo declaro en §3 porque es la clase que PARO (c) vigila: no se alcanza en ninguno de los ocho caminos ni en el dato real, y no se arregla declarando.

**Ensayo, con el validador que sella.** `tests/test_piloto3_v13_conducto.py` (P5) pasa por `corrida0._valida_outputs` —importado de `tools/corrida0.py`, no una copia— la salida de los ocho caminos, contra el `spec.yaml` ya declarado. **Expectativa escrita antes de correr: cero problemas y cero no finitos en los ocho.** Resultado: **7 passed in 21.35s** (los caminos 2 y 8 comparten una función con oro 2023). Control positivo: la misma salida contra el `spec.yaml` de `HEAD~1` (antes de P1) da **40** problemas en EMISIONES y **3** en ADJUDICACION — el validador sí discrimina.

**Celda rara, confirmada.** Fixture con 18-29 × HASTA-PRIMARIA concentrada en 3 UPM (n = 37): de **2 000 réplicas, 1 913 válidas** (87 la vacían — la misma cifra que el ensayo de dirección); ADJUDICACION emite `null` en `-R-P-EE`, `-R-P-IC-LO`, `-R-P-IC-HI` de esa celda, **3 ids**, dentro de los 174; `-R-P` = 0.4906 (finito); el resto del cruce sella entero (15 PUNTUADA, CON-SOPORTE). Cero no finitos.

**Preflight.** EMISIONES **VERDE** (5/5 inputs `COINCIDE`, payload 2025 por `sha256` solamente, `script_blob_sha256 05d4c205…`, 565 ids únicos). ADJUDICACION **BLOQUEADO exactamente por** `input_repo_ausente=emisiones_resultados`, `input_repo_no_commiteado=emisiones_resultados`, `input_repo_ausente=emisiones_sello`, `input_repo_no_commiteado=emisiones_sello` — y por nada más. Ambas salidas coinciden con lo escrito antes de correr.

**Firma.** `FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01` pasa a **FIRMADA** con el PR de este acto (texto verbatim de §2 del encargo). `cuenta_gen2 = SI` se hereda para los COMMIT-2/3 (ya asentado en `decisiones.tsv:184-185` por `#944`; no se toca).

---

## 1 · Arranque (`/acto`, guard 0.a–0.d)

- **0.a** `git fetch --prune` · worktree nuevo `/home/pc0/mm-piloto3-v13` desde `origin/main` `4bb29d96` · `rev-list --count HEAD..origin/main = 0`. `346ab2bc` es ancestro de `origin/main` (21 commits detrás).
- **0.b** `git status --porcelain` vacío.
- **0.c** `git ls-remote --heads origin | grep -i "v1_3\|piloto-3-commit-1"` → 0 · `git worktree list | grep piloto` → `mm-piloto-3-v12` (`#944`, fusionado) y `mm-piloto3-c23` (`#951`, fusionado `ba5fafe5`) · `gh pr list --search v1_3 --state open` → 0. Sin duplicado.
- **0.d** `tools/limpia_arbol.py --reporta`: 12 ramas locales ya fusionadas y vivas, base al día, 1 rama remota fuera de política (`claude/epic-cori-4aiuak`, ajena). Sólo reporte.
- **data/raw** enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiada de `mm-piloto3-c23` (gitignorados). `git worktree add` imprimió `could not write config file .git/config: Device or resource busy` dos veces (sandbox enmascara el config del clon padre; el worktree quedó bien y la rama se empujó).
- **Entorno** (`tools/entorno.py --arranque`, cruda): `ENTORNO-DERIVADO = CAJA` · `senal-corpus: montado=SI archivos_examinados=420` · `senal-nube-env: sin_variable` · `red: PERMITIDA (http_code=200)` · `worktrees: 16` · `data-raw-en-este-worktree: SI`.
- **Compuerta**: el encargo no declara `GATED`/`COMPUERTA:` de merge; su §8 es compuerta de **congelar spec** (protege una de las cuatro): «`_valida_outputs` vacía y cero no finitos en los siete caminos + preflight con salida esperada, pegados». Cumplida en §4 y §5.

## 2 · P1 — la lectura estática, contada contra los ids de cada `spec.yaml`

Derivada por script (`declara_p1.py`, en el scratchpad de la sesión; construye los ids desde `M.CELDAS`/`M.EDADES`/`A.CANDIDATOS` del propio código y falla si alguno no existe en la spec), no a mano.

**EMISIONES — 292 de 565.**

| origen en `medidor.py` | ids | causa pegada a `unidad` |
|---|---|---|
| marginal `-P` (`:389`) | 9 | nulo si el punto no es finito: máscara sin masa |
| marginal `-P-EE/-IC-LO/-IC-HI` (`:387` → `resumen` `:283,291`) | 27 | nulo si una réplica vacía la celda |
| candidato C2/S-MEDIO/S-LAMBDA `-P` (`:410`) | 48 | nulo si el punto no es finito |
| candidato `-P-EE/-IC-LO/-IC-HI` (`:409` → `:291`) | 144 | nulo si una réplica vacía la celda |
| `-C1A-P-IC-LO/HI` (`:416`) | 32 | IC NO-DERIVABLE: sin réplicas selladas de 2023 |
| `-CONTROL-C2COMP-P` (`:355`, `.get`) y `-C2-VS-CONTROL-ABS` (`:424-425`) | 32 | control rotulado `-60-X-` en la casa (`tools/ejes_maestra35_l1.py:60`), mismo universo; se recupera al cierre como aritmética entre sellados |

**ADJUDICACION — 174 de 349.**

| origen en `adjudicacion.py` | ids | causa |
|---|---|---|
| `-R-P` (`:202`) | 16 | nulo si R no es finita (celda vacía en 2025) |
| `-R-P-EE/-IC-LO/-IC-HI` (`:200` ← `:116` → `M:291`) | 48 | nulo si una réplica vacía la celda |
| `-DELTA-25` (`:204`) | 16 | nulo si δ no es finita (R ∈ {0,1} o celda vacía) |
| `-{C2,C1A,C1B,S-MEDIO,S-LAMBDA}-D-PP` (`:208`) | 80 | nulo si R no es finita o el candidato es nulo |
| `-{j}-MAE-PP`, `-{j}-DELTA-MAE-PP/-EE/-IC-LO/-IC-HI` ×2, `-C2-MAE-PP` (`:233-241`) | 11 | nulo si no hay celdas puntuadas; los IC además si una réplica vacía |
| `-C1A-MAE-PP`, `-C1B-MAE-PP` (`:243-245`) | 2 | nulo si no hay celdas puntuadas |
| `-UMBRAL-VENCER-N` (`:219`) | 1 | nulo si no hay celdas puntuadas |

**Lo que NO se declara, y por qué.** Los ids que copian constantes selladas (`-C1B-P`, `-C1B-P-IC-LO/HI`, `-DELTA-21/23`, `-N-2021/2023`, `-ADJ-…-C1A-P`, `-C1B-P`) sólo serían nulos si el `resultados.json` sellado los trajera nulos: verificado que **ninguno de los tres inputs sellados tiene un solo `null`** (576 + 580 + 632 valores). No es un camino del código; es un input inmutable por `sha256`. Los `-{j}-VS-C2`, `-SOPORTE`, `-B-BIS`, `-S2-RESERVA` y los conteos son siempre texto o entero.

## 3 · Un no finito posible por lectura estática, fuera de los ocho caminos — declarado, no tocado

`adjudicacion.py:185,188-189` escribe `cand_pt["C2"] = cr["C2"]` y `S-MEDIO`/`S-LAMBDA` = `float(expit(logit(C2)+…))` **sin guardia de finitud**; `:207` los emite como `-{cid}-P`. `cr["C2"]` (`:119`) es NaN sólo si alguna **marginal de una variable** (una banda de edad entera, un nivel de escolaridad entero, o el total) tiene masa cero en el punto. En ese caso EMISIONES ya habría emitido `null` en `-MARGINAL-…-P` y en los 48 candidatos (`medidor.py:389,410`, con guardia), pero ADJUDICACION emitiría **NaN** en `-{cid}-P` de las 4 celdas de esa banda y `_valida_outputs` respondería `valor_no_finito`. Alcanzabilidad: exige que ENCIG 2025 no tenga **ningún** pago de luz válido en una banda de edad o nivel completo (n por marginal en 2023: miles); ninguno de los ocho caminos lo produce y **no se produjo** (cero no finitos en todas las corridas). No es PARO (c) —PARO (c) es «un camino del ensayo produce un no finito»— y no se arregla declarando ni tocando código (PARO b). Queda escrito para D-22 ampliada: la enumeración por herramienta debe cubrir también `NaN`, no sólo `None`.

## 4 · P3/P5 — los ocho caminos por `_valida_outputs`, crudo

`tests/test_piloto3_v13_conducto.py` (hermano del v1.1, para no tocar `test_piloto3_v11.py`; reutiliza sus fixtures por `import`). Fixtures del control **desde los ids reales** de `CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` (16 ids con `-60-X-`), no desde `M.PREFIJO_CONTROL`. Los ids de la salida sintética (ola `2099`) y de oro (`2023`) se remapean a la ola `2025` de la spec **sólo en el prefijo**, 1 vez por id.

Expectativa, escrita antes de correr: cero problemas y cero no finitos en los ocho; nulos esperados 40 en EMISIONES (sintético y oro), 0 / 0 / 0 / 14 / 3 / 0 en ADJUDICACION.

```
tests/test_piloto3_v13_conducto.py::test_1_emisiones_sintetico_sella PASSED
tests/test_piloto3_v13_conducto.py::test_3_adjudicacion_todas_con_soporte PASSED
tests/test_piloto3_v13_conducto.py::test_4_adjudicacion_soporte_parcial PASSED
tests/test_piloto3_v13_conducto.py::test_5_adjudicacion_fuera_de_soporte_global_con_puntuadas PASSED
tests/test_piloto3_v13_conducto.py::test_6_adjudicacion_cero_puntuadas PASSED
tests/test_piloto3_v13_conducto.py::test_7_adjudicacion_celda_rara_vaciada_por_una_replica PASSED
tests/test_piloto3_v13_conducto.py::test_2_y_8_oro_2023_emisiones_y_adjudicacion_sellan PASSED
============================== 7 passed in 21.35s ==============================
```

| # | camino | nulos emitidos | problemas | no finitos |
|---|---|---|---|---|
| 1 | EMISIONES sintético (300 réplicas) | 40 (32 C1A-IC + 8 banda 60-96) | 0 | 0 |
| 2 | EMISIONES oro 2023 (10 000, PCG64 20260919) | 40 (idem) | 0 | 0 |
| 3 | ADJ todas con soporte (15 PUNTUADA) | 0 | 0 | 0 |
| 4 | ADJ soporte parcial (13 PUNTUADA, 2 FUERA por n sellado 2021 = 150) | 0 | 0 | 0 |
| 5 | ADJ FUERA-DE-SOPORTE global con 10 PUNTUADA | 0 | 0 | 0 |
| 6 | ADJ cero PUNTUADA | 14 (11 MAE/ΔMAE + 2 C1A/C1B + umbral) | 0 | 0 |
| 7 | ADJ celda rara (n = 37 en 3 UPM; 2 000 réplicas, 1 913 válidas) | 3 (`-R-P-EE/-IC-LO/-IC-HI`) | 0 | 0 |
| 8 | ADJ oro 2023 como R (10 000; 16/16 celdas `B-VALIDAS = 10000`) | 0 | 0 | 0 |

Control positivo (misma salida, `spec.yaml` de `HEAD~1`, antes de P1): 40 y 3 problemas. `tests/test_piloto3_v11.py`: **7 passed in 23.21s** (sin cambio).

**Sobre el camino 8.** El código admite la adjudicación con la ola 2023 como R (`A.medir` no lleva `_guardia_reserva`; `M.medir` con `ola=2023` la lleva y pasa porque ningún input se llama `2025`); se validó. Es control de conducto, no medición: C1b es la propia R sellada, así que sus veredictos no significan nada y no se reportan.

## 5 · P6 — preflight e intactos, crudo

Expectativa escrita antes: EMISIONES `VERDE`; ADJUDICACION `BLOQUEADO` sólo por los cuatro `emisiones_*`.

```
[EN-MAIN-COINCIDE] spec_md_sha256 · [UNICOS] ids de resultados: 565 declarados · script_blob_sha256 = 05d4c2058ea00bd3a2074a2ba3aa5cef4bbe24a407e523b294bb5bfe6075d4dc
[COINCIDE] encig25_base_datos_csv origen=manifiesto raiz=data_raw · [COINCIDE] ×4 inputs repo
PRE-FLIGHT: VERDE
PRE-FLIGHT: BLOQUEADO input_repo_ausente=emisiones_resultados:… input_repo_no_commiteado=emisiones_resultados input_repo_ausente=emisiones_sello:… input_repo_no_commiteado=emisiones_sello
```

Intactos (`git hash-object` = `git rev-parse 826bf3a1:<ruta>`): `medidor.py 503f119f…` IGUAL · `adjudicacion.py 78cf485e…` IGUAL · `GOB-gobierno-digital-exe15-spec-v1_1.md 5d27b269…` IGUAL · `.sha256 6cd17c3f…` IGUAL.

## 6 · Latitud ejercida (§6 del encargo)

- Sintético de la celda rara: la receta de dirección (`ensayo-rama5-celda-rara.py`, sha256 verificado) trasladada al test, con `upms_raras=(0,1,2)` y 2 000 réplicas.
- Orden: sintético → ramas de soporte → celda rara → oro (lo caro al final).
- P5 en test hermano, no en `test_piloto3_v11.py`.
- `pytest` ya estaba instalado (9.1.1); no se instaló nada.
- Censo de guardias: `tools/ci_guardias.py --censo` regeneró **81 filas ajenas** (clasificaciones dependientes del entorno); se descartó esa regeneración y se añadió **sólo la fila propia**, con la misma clasificación que `test_piloto3_v11.py` (`NECESITA-DEPENDENCIA(pytest)`: CI no instala numpy/pandas/pytest — FP de mesa ya abierta, `requirements.txt`). Consecuencia declarada en NO-CORRIDO: el test corre en CAJA y en `tests/check.py` no; en CI se salta en voz alta igual que el v1.1.
- Ningún defecto adyacente tocado.

## 7 · Sucesores

1. **COMMIT-2 / 3a / 3 del v1.3**, otra sesión, CAJA. Primer comando tras P0: `corrida0 preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → VERDE; P0 añade `pytest tests/test_piloto3_v13_conducto.py` en verde. Al cierre del COMMIT-3: las cuatro restas del control 60-96 como aritmética derivada (llave `commit_3_cierre_control_60_96`) y la lista de cada `null` emitido por familia de id; si alguna PUNTUADA pierde su IC de R (`adjudicacion.py:210-211`), el veredicto lo dice.
2. **D-22 ampliada** (dirección, semilla v2.16): enumeración por herramienta de todo `None` **y todo `NaN`** (§3).
3. **Piloto de ahorro PRODUCTO-DINERO**: no se congela sin este ensayo desde su COMMIT-1.
