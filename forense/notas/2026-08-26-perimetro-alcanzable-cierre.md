# Cierre · ACTO MAESTRA31-E3 · PERIMETRO-ALCANZABLE

Encargo: `forense/encargos/2026-08-26-MAESTRA31-E3-PERIMETRO-ALCANZABLE.md` (dirección, maestra-31, 26/ago/2026, archivado por A.3 antes de ejecutar). Entregable: `forense/perimetro-alcanzable-v1_0.md`.

## 1 · ARRANQUE

- Clon existente localizado: `/home/pc0/Modelado-Mexicano`, parado en `acto/cal-g3-puntual` (`ea22bdd`), mismo patrón que `MAESTRA31-E1`/`MAESTRA30-E9`. No se clonó uno nuevo.
- Worktree propio creado sobre `origin/main`: `git worktree add -b acto/maestra31-e3-perimetro-alcanzable /home/pc0/mm-maestra31-e3-perimetro-alcanzable origin/main`. `.git/config` dio "Device or resource busy" (bind-mount de sandbox conocido, no falla real — el worktree se creó correctamente, `git log -1` lo confirma).
- SHA: `origin/main = e5a36ab` (`Merge pull request #382 from Josanoforo/acto/e1-reloj-cruce`) — coincide EXACTO con lo que el encargo declara. `gh pr view 381` → `MERGED 2026-08-27T00:11:47Z`; `gh pr view 382` → `MERGED 2026-08-27T05:18:33Z`. Ambos confirmados vía `gh`, no vía estado de worktree.
- `data/raw`: ausente en el worktree fresco (esperado). Enlazada: `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo destino que usa `/home/pc0/Modelado-Mexicano`). `ls data/raw | wc -l` → 321 entradas.
- Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío (sin_variable, esperado). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. `ls data/raw/ | head -1` → `2005trim1_csv.zip` (corpus montado, no vacío).
- Espejo: no se derivó ninguna cifra de él.

Todo cuadró con lo que el encargo supone. No hubo PARO.

## 2 · Conteos A.13 — cada negativo con comando y universo examinado

- **Búsqueda de "18/31" vigente en el árbol (C3):** `command grep -rn "18/31\|18 con valor\|18 reglas.*31\|18-31" --include="*.md" --include="*.yaml" --include="*.tsv" --include="*.py" .` examinó **1,116 archivos** (`find . -path ./data/raw -prune -o -path ./.git -prune -o \( -iname "*.md" -o -iname "*.yaml" -o -iname "*.tsv" -o -iname "*.py" \) -print | wc -l`). Resultado: 7 hits, todos citas históricas de una corrección ya hecha el 31/jul/2026 (D4) — cero apariciones de "18/31" como valor vigente. `command grep` (no `ugrep`) usado explícitamente.
- **Git log de `cobertura-motor.md`:** `git log --follow --format="%h %ad %s" --date=short -- forense/cobertura-motor.md` → un solo commit, `2026-07-31`. Examina el historial completo del archivo (`--follow`), no una muestra.
- **Reproducción de `censo_estimabilidad.py`:** corrida completa (`--write`), no una muestra — 15/15 filas comparadas con `diff` contra el archivo comprometido, cero diferencias.
- **Conteo de `coef-universo-v1_0.tsv`:** `csv.DictReader` sobre las 58 filas de datos (encabezado excluido), sin muestreo.
- **Conteo de `cruce-oferta-demanda-v0_1.tsv`:** `awk` sobre las 49 filas de datos (`NR>1`), sin muestreo.
- **Conteo de `enlace-M-v1_0.md`:** `sed -n '45,104p'` aísla exactamente las 60 filas de la tabla (verificado con `grep -c "^|"` → 60), sin muestreo.
- **Máximo ADR:** `command grep -rohE "ADR-[0-9]+" forense/ canon/ | sed 's/ADR-//' | sort -n -u | tail -5` → `210` como máximo, verificado también contra `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` por separado (mismo resultado en las tres consultas independientes). Nuevo ADR candidateado en el commit de cierre: **211**. **Renumerado a `ADR-212` al resolver `PR #384` contra `origin/main`:** `PR #383` (`ACTO MAESTRA31-E2 · REGISTRA-PENDIENTES`) fusionó primero (`merge commit 7b4493c`) y se quedó con `ADR-211`; este acto renumera al fusionar segundo, misma regla que `ADR-198`/`ADR-199`/`ADR-204`/`ADR-209`.

Ningún veredicto negativo de este acto se apoyó en un comando que no examinó archivos (A.13 §3).

## 3 · Qué se produjo

- `forense/perimetro-alcanzable-v1_0.md` — entregable, N=12 de 30 alcanzables, tres adjudicaciones (C1 RECONCILIADA, C2 DOMINIOS DISJUNTOS, C3 RECONCILIADA-y-premisa-incorrecta).
- Esta nota.
- `FP-170` nueva fila (la cifra ante mesa).
- `FP-169` → `FIRMADA-PARCIAL` con la condición textual de RANURA M-RELOJ propagada tal cual, más la lectura de C2 aplicada (Instrumento no reabre bajo la lectura declarada — ver `perimetro-alcanzable-v1_0.md` §2, C2).
- `FP-168`, columna `gatea` (equivalente semántico de "desbloquea" — no existe columna literal con ese nombre en `firmas-pendientes.tsv`; las columnas son `id/qué_se_firma/dónde/creado/gatea/estado/firmada_en/ejecutada_en/encargo`) corregida: de "nivel_ic/seed bastan" a las tres cosas reales (nivel_ic, seed, y resolver `SIN_CELDAS_PAREADAS`), leyendo `forense/notas/2026-08-26-e9-scoring-v2-cierre.md` §4.
- Tres líneas nuevas en `forense/hallazgos.md`: C1 (staleness real de `procedencia.yaml`), C2 (la resolución del aparente contradicción entre las dos tablas A.4), y el hallazgo de granularidad (6 filas-generador vs. 15 gen×coef en la propia `procedencia.yaml`). C3 NO recibe línea — la contradicción no resultó real (ya estaba resuelta desde el 31/jul, la premisa del encargo es la que estaba desactualizada, no el árbol).
- Enmienda fechada al final de `forense/notas/2026-08-25-cruce-oferta-demanda.md` (la adjudicación de C2 toca directamente esa nota, vía la fila G5.familismo_obligacion citada y la RANURA M-RELOJ).
- `ADR-212` (renumerado desde `ADR-211` al resolver `PR #384` contra `PR #383`/`ACTO MAESTRA31-E2`, que fusionó primero) en `canon/gobernanza-v1_15.md` + párrafo `Cascada`.
- Recifrado `§L0` de `canon/estado-programa-v1_10.md` (211→212 ADR, sobre el 210→211 ya aplicado por `ACTO MAESTRA31-E2`) + `canon/gobernanza-v1_15.md:2` + `canon/estado-programa-v1_10.md:27` (tabla de artefactos).
- `canon/registro-rotulos.tsv`: fila nueva `MAESTRA31-E3`.
- `tests/check.py` `_T25_ARCHIVOS_CONOCIDOS`: los tres archivos nuevos de este acto que citan el rótulo pelado "E3" (el encargo archivado verbatim, el entregable y esta nota).

## 4 · Lo que este acto NO hizo (perímetro)

No re-especificó ningún censo. No promovió ninguna fila a acto medidor. No decidió qué hacer con la cifra N=12/30 (esa decisión es de mesa). No tocó `milpa/**`, ni `data/coef-universo-v1_0.tsv`, ni `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`, ni `forense/cobertura-motor.md`, ni `forense/censo-estimabilidad-coeficientes-v1_2.md`, ni `forense/prereg-duelo-v2/**`, ni `forense/hitoD-preregistro-v2_0.md`. No re-especificó `riesgo_fiscal_percibido`. No adjudicó casilla/letra/tier. No usó red salvo el chequeo de política del ARRANQUE (`curl` a INEGI, sin descargar nada). No abrió ningún payload (§4 del entregable). No corrigió `procedencia.yaml` pese a encontrar la staleness de C1 — queda declarada para un sucesor con firma, mismo criterio que el 18/31 de C3.

## 5 · Suite

`python3 tests/check.py --baseline` corrido tras todos los cambios — ver resultado en el commit de cierre.
