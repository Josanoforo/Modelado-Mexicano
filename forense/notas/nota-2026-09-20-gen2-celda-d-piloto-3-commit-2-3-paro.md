# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3` · PARO (b) sin parche: el CALC congelado no corre bajo `corrida0 run` — su `preflight` sale BLOQUEADO por tres defectos de cableado del `spec.yaml`; ENCIG 2025 sigue sin abrirse

**20/sep/2026 (21:07–21:40 CST) · CAJA (`ENTORNO-DERIVADO`: `corpus=SI(examinados=419)`, `raices=data_raw:SI descargas_mx:SI`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, python 3.14.4, numpy 2.3.5, pandas 2.3.3) · Opus 5 · rama `acto/gen2-celda-d-piloto-3-commit-2-3`, worktree `/home/pc0/mm-piloto-3-c23` · base `04a2edeb` = `origin/main` al abrir = SHA de redacción del encargo (`git rev-list --count HEAD..origin/main` → `0`).**

Encargo archivado (A.3): `forense/encargos/2026-09-20-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3.md` (sha256 `70e6d662…`, commit `223a94bc`, rama empujada antes de cualquier paso sustantivo).

---

## 0 · Para mesa, en una página

**Qué se iba a probar.** Si la interacción edad × escolaridad que fue estable en ENCIG 2021 y 2023 (pagar la luz por canal digital) se transporta a 2025, cuando el nivel subió once puntos: el tercer piloto pre-registrado, con el código que `#926` congeló, en tres pasos (emisiones → realidad y veredicto → registro).

**Qué salió.** No se probó nada, y no por un defecto del dato ni del método: **el CALC congelado no corre por el único conducto que sella** (`python3 tools/corrida0.py run …`). El runner corre primero su `preflight`, y ese `preflight` sale `BLOQUEADO` para los DOS CALC por tres defectos del `spec.yaml` congelado:

1. `spec_md: forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` — el runner resuelve esa ruta **relativa al directorio del CALC** (`tools/corrida0.py:1615`, `md = d / spec_md`), así que busca `data/corrida0/CALC-…/forense/prereg-caja/…` y no la encuentra → `ausente=…`. La convención de la casa es `spec_md: spec.md` (150 `spec.yaml` del árbol) o `../../../forense/prereg-caja/…` (7). Sólo la v1.0 de `#903` (nube, nunca corrida) y las dos v1.1 usan la forma sin `../../../`.
2. Cuatro inputs `origen: repo` sin `sha256` declarado (`encig2021_cruces_resultados`, `encig2023_cruces_resultados`, `c2_compuesto_resultados`, `firmas_pendientes_tsv`) → `input_repo_sin_sha_declarado` ×4. Las specs selladas hermanas (p. ej. `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`) los declaran.
3. `dependencias_materiales` ausente → `campo_sustantivo_ausente=dependencias_materiales` (esquema endurecido, `etiquetas.generacion = GEN2`).

Las tres comprobaciones existen en `corrida0.py` desde el 7–8/sep (`3699db72`, `2969ddc8`); `tools/corrida0.py` no cambió entre el commit de la spec (`826bf3a1`, 20/sep) y hoy salvo `d2eb1bcc` (RELEVO-RECONCILIA-1, que no toca `preflight`). El COMMIT-1 v1.1 validó el medidor **por pytest** (sintético + oro 2023, 7/7 aquí también) y **nunca corrió `corrida0 preflight`**: misma clase de defecto que `#903` (`_prepara()` unía por índice) y `#924` (`medir()` sin cuerpo): cableado invisible para la prueba propia del congelador — esta vez congelado en caja, no en nube.

**Con qué certeza.** Total sobre el bloqueo: es determinista, se reproduce con un comando (`python3 tools/corrida0.py preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002`), y `run` lo respeta por construcción (`tools/corrida0.py:2064-2069`: `if pre["veredicto"] != "VERDE": return NO-EJECUTADO`). Ninguna de las tres causas es de entorno ni de sandbox (el payload `encig25_base_datos_csv` está `COINCIDE`, 37 624 925 B, sha256 `47daf2f7…`; `FP-352` no aplica).

**Qué no significa.** No dice nada sobre la hipótesis, sobre el dato de 2025 ni sobre la validez del método: `medir()` sí reproduce lo sellado de 2023 a 1e-9. Tampoco se arregla desde aquí: el `spec.yaml` es parte de la spec congelada (perímetro ajeno; PARO (a)) y el encargo fija el sucesor — **COMMIT-1 v1.2 de otra sesión** (PARO (b)) — cuyo cambio previsible son tres llaves de cableado del `spec.yaml` (ruta de `spec_md`, cuatro `sha256`, `dependencias_materiales`), sin tocar `spec.md`, su sidecar, `medidor.py` ni `adjudicacion.py`. La `FP-407` le pide a mesa que lo confirme y diga quién congela.

**Lo que este acto SÍ dejó hecho:** P0 completo (sidecar OK, 7/7 con la prueba de oro); rastros de apertura de 2025 censados (§2: ninguno); `[SUPUESTO]` del yaml legacy verificado (§3: ninguno de los dos CALC lo lee); la lista exacta de bloqueos para el v1.2 (§4). **ENCIG 2025 no se abrió** — ni por una variable ni por dos: el único acceso al zip fue el `sha256` del `preflight`.

---

## 1 · Arranque (`/acto`, guard 0.a–0.d) y F3

- 0.a `git rev-list --count HEAD..origin/main` → `0`. 0.b árbol limpio. 0.c rótulo `PILOTO-3` / `commit-2-3`: 0 ramas remotas, 0 worktrees ajenos, 0 PR abiertos. 0.d `limpia_arbol --reporta`: base al día; 8 ramas locales fusionadas vivas (ajenas); 3 remotas sin PR (ajenas).
- `data/raw` enlazada a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiada del clon padre. `tools/entorno.py`: `montado=SI`, `archivos_examinados=419`.
- **F3:** esta sesión es nueva (Opus 5, arrancada en `/home/pc0` el 20/sep 21:06 CST); no es `pc0-77`; no tiene en contexto los diseños A/B ni el careo del piloto 3. Sí tiene, por memoria del proyecto, el resumen de los actos `#924`/`#926` (que S2/S1 se cerraron por texto, que el v1.1 sortea el bootstrap sobre el marco entero) — se declara por exceso; no es un diseño ni un careo.
- Sin compuerta `GATED a` en el encargo; sus dos compuertas propias (§8) protegen «abrir dato» y se respetaron: la primera se cumplió (oro en verde) y la segunda nunca se alcanzó.

## 2 · `[SUPUESTO]` nadie abrió ENCIG 2025 por dos variables — censo

`git ls-files | grep -iE "encig.?2025|encig25"` fuera de spec/código/encargos/notas → sólo `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` (`#926`, `SPEC-CONGELADA`, `unidad_objetivo: persona`). Los dos directorios CALC traen sólo `spec.yaml` + su `.py` (0 `ejecucion.json`/`resultados.json`/`sello.*` en ningún checkout de `/home/pc0`, `find -maxdepth 6`).

Disco (`find /home/pc0 -maxdepth 4 -newermt 2026-09-19`, nombres `encig*25*`, `piloto*3*`, `edad*escol*`, `emisiones*`, `adjudic*`): sólo copias versionadas en otros worktrees (`tests/test_piloto3_*.py`, `tools/medidor_gobierno_digital_encig25.py`, notas/encargos de `#894`–`#926`). Fuera del repo, **no abiertos**: `/tmp/claude-1000/s2/encig25_cuestionario.txt` (287 028 B, 20/sep 15:11) y `/tmp/claude-1000/s2/encig25_estructura_base_datos.txt` (585 210 B, 20/sep 15:11) — por nombre y tamaño, texto del cuestionario y del descriptor (la lectura S1/S2 de `#924`), no microdato; y `/tmp/claude-1000/pytest-of-pc0/pytest-*/…/encig2099_sintetico.zip` — fixture sintético de `tests/test_piloto3_v11.py`. **Veredicto: sin rastro de 2025 abierto por dos variables; PARO (h) no aplica.**

## 3 · Premisas verificadas

| premisa | resultado |
|---|---|
| `[EJECUTADO]` sidecar | `sha256sum -c GOB-gobierno-digital-exe15-spec-v1_1.sha256` → `OK` |
| `[EJECUTADO]/[LEÍDO]` pytest, incluida la de oro | `python3 -m pytest tests/test_piloto3_v11.py -q` → **7 passed, 20.9 s**; `test_b_oro_2023_reproduce_los_sellados PASSED` en esta caja |
| `[EJECUTADO]` FP-389/399/400 FIRMADA, NC-0355 CERRADA | `test_c_fp399_firmada_en_el_repo PASSED`; `cierre_acto.py`: FP-399/400 no figuran entre las 12 ABIERTA |
| `[EXISTE]` celda-D yaml | existe, nace con `unidad_objetivo: persona` (nota de `#926`); FP-393 sigue ABIERTA en `04a2edeb` |
| `[SUPUESTO]` los CALC no leen el yaml legacy | `grep -n "celdas-d\|curacion-registro\|\.yaml"` sobre `medidor.py` y `adjudicacion.py` → 0 lecturas (una mención en docstring, `medidor.py:433`, sobre `spec.yaml`) |
| `[SUPUESTO]` 2025 no abierto por dos variables | §2: sin rastro |
| **NUEVA — no prevista:** el CALC corre bajo `corrida0 run` | **FALSA**: `preflight` BLOQUEADO (§4) |

## 4 · El bloqueo, crudo

```
$ python3 tools/corrida0.py preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002
PRE-FLIGHT CALC-GOB-DIGITAL-EXE-EMISIONES-0002   (data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002)
  [COMMITEADO] data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/spec.yaml
  [NO-EJECUTABLE] spec_md_sha256
              declarado en spec.yaml = 62d8d07d70dd4d53544975bf8b541e5cd63079080d9537b5fde8414115579eb5
              arbol                  = None
              origin/main            = NO-EN-MAIN
  [UNICOS] ids de resultados: 565 declarados
  [UNICOS] ids de inputs: 5 declarados
  [EXISTE] script data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/medidor.py
              script_blob_sha256 = 05d4c2058ea00bd3a2074a2ba3aa5cef4bbe24a407e523b294bb5bfe6075d4dc
  inputs declarados: 5
    [COINCIDE] encig25_base_datos_csv  origen=manifiesto  raiz=data_raw   (sha256 47daf2f7… = esperado; 37624925 B)
    [SIN-SHA-DECLARADO] encig2021_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2021-CRUCES-HISTORICOS-0003/resultados.json   (real 285eeb55…)
    [SIN-SHA-DECLARADO] encig2023_cruces_resultados  origen=repo  ruta=data/corrida0/CALC-ENCIG2023-CRUCES-HISTORICOS-0002/resultados.json   (real b7d3dfe9…)
    [SIN-SHA-DECLARADO] c2_compuesto_resultados  origen=repo  ruta=data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json   (real be24d879…)
    [SIN-SHA-DECLARADO] firmas_pendientes_tsv  origen=repo  ruta=forense/firmas-pendientes.tsv   (real e0f1ec86…)
  [ENDURECIDO] esquema de spec   (etiquetas.generacion = GEN2)
  [LIMPIO] git status --porcelain (0 lineas)
  [SIN-SELLO-PREVIO] sello previo

PRE-FLIGHT: BLOQUEADO ausente=data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md input_repo_sin_sha_declarado=encig2021_cruces_resultados input_repo_sin_sha_declarado=encig2023_cruces_resultados input_repo_sin_sha_declarado=c2_compuesto_resultados input_repo_sin_sha_declarado=firmas_pendientes_tsv campo_sustantivo_ausente=dependencias_materiales
```

`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`: los mismos tres bloqueos, más los esperables `input_repo_ausente`/`input_repo_no_commiteado` de `emisiones_resultados` y `emisiones_sello` (que sólo existirían tras el COMMIT-2).

**Por qué no se parcha aquí.** `spec.yaml` es la spec en su forma legible por máquina: perímetro ajeno del encargo (§9: «la spec y su sidecar»); editarlo es PARO (a) y «el código congelado no corre → no se parcha» es PARO (b), con el sucesor ya nombrado (COMMIT-1 v1.2 de otra sesión). Correr `medir()` a mano, fuera de `corrida0`, produciría una salida no sellada — PARO (d) — y quebraría «el primer resultado que produzca este procedimiento es el que se reporta». La latitud (§6) cubre reintentar «un paso que falló por entorno»; esto no es entorno.

**Lo que sí se comprobó, estáticamente, para el v1.2:** la interfaz runner↔script coincide (`_ejecuta` llama `medir(inputs, contrato)`; `medidor.py:474` y `adjudicacion.py:296` la exponen); el payload resuelve y coincide; el esquema endurecido no reporta otros faltantes. No se garantiza que no haya un cuarto defecto detrás del tercero: `preflight` corta en la lista que imprime.

## 5 · Contadores y perímetro

- `N_corridas_selladas` +0; `adoptados_activos` sin mover; `usos.tsv`, `corridas.tsv`, `resultados.tsv`, `replay-evidencia.tsv` sin filas propias. Celda-D GOB sigue `SPEC-CONGELADA`; el par edad × escolaridad de ENCIG 2025 sigue `RESERVADA`; los otros dos cruces intactos.
- La propuesta de sello (`cuenta_gen2 = SI` para ambas corridas «sea cual sea el veredicto») quedó **sellada por el lanzamiento pero sin corrida a la que aplicarse**; se hereda al sucesor por `FP-407`, no se re-pide.
- Pisada revertida en la sesión (declarada por exceso): `python3 tools/asienta_replay_aislado.py --help` re-asentó una fila WBES ajena en `forense/replay-evidencia.tsv` (el script no tiene argparse; defecto ya conocido); `git checkout --` la devolvió a la base antes de cualquier commit. `git diff origin/main -- forense/replay-evidencia.tsv` → vacío.
- Nada escrito en scratch por este acto; los únicos temporales son los de pytest (`$TMPDIR/pytest-of-pc0/pytest-9`, fixture sintético `encig2099`).

## 6 · Sucesor — qué necesita el COMMIT-1 v1.2 (para la sesión que lo congele; no es instrucción de mesa)

Tres llaves del `spec.yaml` de cada CALC: `spec_md` como `../../../forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` (o copiar la spec a `spec.md` dentro del CALC, que es la forma mayoritaria); `sha256` en los cuatro inputs `origen: repo` (valores reales arriba, al SHA `04a2edeb`); `dependencias_materiales: [numpy, pandas]`. Y **la prueba que faltó**: `python3 tools/corrida0.py preflight <CALC>` → `VERDE` antes de congelar, sin abrir 2025 (`preflight` sólo hace `sha256` del zip). Si esas tres llaves son todo, `spec.md`, su sidecar y ambos `.py` quedan byte a byte, y `spec_md_sha256` no cambia — mesa decide en `FP-407` si eso cuenta como «hereda verbatim».
