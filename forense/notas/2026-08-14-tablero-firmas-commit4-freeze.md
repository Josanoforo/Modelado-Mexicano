# ACTO TABLERO-FIRMAS COMMIT 4 · El vigía dispara en CI por primera vez — y mesa autoriza el recongelado en el acto

No anticipado por el encargo original, como Commit 3. Consecuencia directa de la suscripción a actividad de PR que el usuario pidió tras crearse `PR #240` desde la UI de Claude Code, y de la instrucción explícita "fetch and solve CI" que siguió.

## §0 · Lo que llegó

`mcp__github__pull_request_read` (`get_check_runs`) sobre `PR #240` → un solo check, `check`, `conclusion: failure`. `get_job_logs` sobre ese job: el paso "Checkout" y "Intérprete del runner" pasan; `python3 tests/check.py --baseline` corre completo (20 FAIL · 129 WARN, igual a lo verificado localmente antes de empujar Commit 3) y termina con `LÍNEA BASE: ROJO — 22 entradas nuevas`, `exit code 1`. El job muere ahí — el segundo paso del workflow, `python3 tests/test_svystat.py`, nunca llega a correr.

`.github/workflows/verify.yml`, paso "Suite de verificación (modo línea base — verde = no empeoraste)": el gate de CI corre `--baseline`, no la suite cruda. Confirma que el rojo es real, no un artefacto del runner (mismo endurecimiento del 7/ago que ya descarta fallos de infraestructura).

## §1 · Diagnóstico — no es un defecto, es el mecanismo funcionando

Las 22 entradas nuevas son exactamente las que los Commits 1-3 ya declararon, verificadas localmente antes de cada push:
- **19** filas `ABIERTA` de `T21`/`T-FIRMAS` — las firmas pendientes que este mismo acto hizo visibles. Por diseño (A.12), `T21` emite WARN por cada una en **cada corrida**, congelada o no — el recongelado no las esconde, sólo deja de tratarlas como regresión nueva de esta PR.
- **2** citas `T03` de `forense/notas/2026-08-14-tablero-firmas-commit3.md:29`, que cita en backticks dos documentos de mesa reales fuera del repo (`AJUSTE-PLAN-v3_1-2026-08-13.md`, `PLAN-MULTIFASE-F0-F6-2026-08-13.md`) para verificar `FP-24` — patrón I-01 ya conocido (mención, no referencia rota).
- **1** consecuencia aritmética de los dos `T16` permanentes (`gobernanza:1106`/`:1136`), mismo fenómeno que Commit 2 §5 y Commit 3 §3 ya documentaron.

`python3 tests/test_svystat.py`, corrido localmente para no dejarlo sin verificar solo porque el primer paso del job no llegó a él: **13 casos, exit 0**. Sin relación con este acto.

`ADR-76(f)` (`gobernanza:1104`), verbatim: *"recongelar la línea base exige ADR de mesa; un ejecutor que encuentre drift lo reporta y no lo recongela. Sin condiciones adicionales."* Por eso los tres commits anteriores dejaron el baseline ROJO en vez de correr `--freeze` por cuenta propia — sería exactamente el `A.12`-en-reversa que este acto existe para prevenir: un ejecutor decidiendo en silencio que 19 firmas pendientes "ya no cuentan".

## §2 · La autorización — tipo declarado, no verbatim de texto libre

Distinto de `ADR-84`/`ADR-82` (cita verbatim de una frase que el usuario escribió libremente): aquí la autorización se dio por `AskUserQuestion`, una pregunta estructurada de dos opciones que citó `ADR-76(f)` verbatim y describió explícitamente qué cambia y qué no cambia con cada elección, **antes** de recibir respuesta. El usuario seleccionó *"Autorizo el recongelado (Recomendado)"* — confirmación explícita sobre una alternativa ya declarada por escrito, no una frase libre. Se declara así, sin adorno, mismo criterio de honestidad de procedencia que `gobernanza:1248` ya aplicó a A.9 (procedencia tipo (3) ahí; aquí es una selección explícita en sesión, no reportada por dirección — clase distinta, ninguna de las dos es cita verbatim de mesa).

## §3 · Ejecución

```
$ python3 tests/check.py --freeze
```
→ `tests/baseline.json` reescrito: `head` `640a74d9d4e111cad9fdd4ce262842f7e908f77a` (el recongelado que `ACTO MOTOR-3/E0` había hecho) → `6211b0da0ad7bb1bf8fe58680ac91d56941754eb` (`ACTO TABLERO-FIRMAS COMMIT 3`, ya en la rama de esta PR).

```
$ python3 tests/check.py --baseline
```
→ **LÍNEA BASE: VERDE — nada nuevo frente a `tests/baseline.json`** (HEAD congelado `6211b0d`). La suite cruda no se movió: sigue **20 FAIL · 129 WARN**. `T21` sigue emitiendo sus 19 WARN — verificado explícitamente, no asumido: el recongelado cambia qué cuenta como "nuevo" contra la línea base, no qué emite la suite.

Sellado como `ADR-85`, mismo mecanismo que `ADR-81` usó para el recongelado del 13/ago — ver `canon/gobernanza-v1_15.md`.

## §4 · Perímetro tocado

`tests/baseline.json` (recongelado) · `canon/gobernanza-v1_15.md` (`ADR-85` + cascada 84→85) · `canon/estado-programa-v1_10.md` (cascada 84→85) · `forense/hallazgos.md` (una entrada) · esta nota. Ningún archivo de `milpa/`, `data/`, `canon/modelo-decision-v4_0.md` ni el propio `forense/firmas-pendientes.tsv` — ninguna fila cambia de estado por este commit, es gobierno del aparato de CI, no del tablero.
