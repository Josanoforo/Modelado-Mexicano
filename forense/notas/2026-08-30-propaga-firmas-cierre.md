# Nota de cierre · ACTO MAESTRA32-E5 · PROPAGA-FIRMAS-Y-COLA

30/ago/2026. Encargo: `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md`. Rama `claude/maestra32-e5-firmas-cola-vroay4`. `ADR-222`.

## 1 · Arranque (A.2/A.13, con conteo de archivos examinados)

1. **Repo.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó uno nuevo). `git log -1` al arrancar: `f10b277 Merge pull request #393 from Josanoforo/claude/maestra32-e2-motor-texto-c5grsj` — coincide exacto con el SHA de redacción del encargo. `git status`: rama `claude/maestra32-e5-firmas-cola-vroay4`, árbol limpio.
2. **SHA.** Sin diferencia que re-derivar — `main` no se había movido desde la redacción.
3. **`data/raw`.** Ausente (`ls data/raw` → `No such file or directory`); no se creó ni se enlazó — este acto no toca microdato. `ls data/raw/ 2>/dev/null | head -1` (A.2 tercera parte): valor crudo vacío, esperado.
4. **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con NUBE declarado en la cabecera). Sonda de red (`curl` a INEGI) **omitida a propósito**: este acto no toca microdato ni red, condición explícita del ARRANQUE del propio encargo para saltar el punto 4. Comando que produjo este negativo: `echo "$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE"` — examina 0 archivos, es lectura de variable de entorno, no de árbol; se declara así por disciplina A.13 aunque el punto no aplique.
5. **Espejo.** No se usó — todas las cifras de esta nota salen del clon de (1), comando a la vista en cada una.

## 2 · Grieta A.3 de `MAESTRA32-E3` — cómo se cerró

Al arrancar: `ls forense/encargos/ | command grep -c MAESTRA32` → **2** (`2026-08-28-MAESTRA32-E1-SELLA-ENLACE.md`, `2026-08-28-MAESTRA32-E2-EMPAREJA-MOTOR-TEXTO.md`) — `MAESTRA32-E3` no estaba archivado, confirmando la VERIFICACIÓN DE EXISTENCIA del encargo.

El propio encargo de este acto declaraba el texto de `MAESTRA32-E3 · EXTRACTOR-DTA` como "adjunto al lanzamiento" — pero no llegó adjunto al lanzamiento real de esta sesión: no estaba en el repo (`grep -rli "extractor-dta" .` → solo referencias *a* él en `firmas-pendientes.tsv`, el encargo de E2 y `gobernanza-v1_15.md`, nunca su cuerpo) ni en el mensaje de arranque. Divergencia entre letra y árbol (B-bis) — se paró y se reportó a dirección antes de escribir nada del Paso 1, en vez de inventar texto atribuido a dirección. Dirección cargó el texto real como archivo en un turno posterior; se verificó **byte a byte** contra el archivo cargado (`orig.rstrip('\n') == copia.rstrip('\n')` → `True`, 12063 caracteres) antes de archivarlo. Paso 1 se completó con esa verificación, no por confianza.

`forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md`: cuerpo verbatim (verificado como arriba), con **una** cabecera añadida (`> RANURA M-EXTRACTOR: FIRMADA...`) resolviendo su ranura de firma con la letra "a y b" de `F-175` — la ranura original del propio E3 (`[FIRMA M — VACÍA]`, líneas 11-17 del original) no se editó.

## 3 · Las tres firmas, propagadas (A.12: mismo commit que el tablero)

`forense/firmas-pendientes.tsv`, `FP-175`/`FP-170`/`FP-172`: `ABIERTA` → `FIRMADA`, con la letra y la razón de mesa verbatim en `firmada_en`, `ejecutada_en` = `ADR-222`. Verificado por `csv.DictReader`: **175 filas totales tras el cambio** (174 antes + 1 fila-grito nueva), 0 filas malformadas nuevas (las 2 preexistentes, `FP-156`/`FP-158`, con conteo de campos ≠9 por comillas sin escapar, no se tocaron ni se repararon — fuera de perímetro).

## 4 · Ranuras opcionales — las cuatro llegaron VACÍAS, las cuatro se dejan vacías

Texto del encargo, verbatim, para las cuatro: `[FIRMA M — VACÍA]`. Ninguna letra de mesa acompaña la propuesta de dirección en ninguna de las cuatro — el diseño/benchmark que sigue a cada etiqueta es contexto para cuando alguien la firme, no una firma. Aplicando el fail-closed del propio encargo (precedente `ADR-220`, `M-LECTURAS`: *"llegó vacía — mesa no indicó filas — y se deja vacía, no se llena por inferencia"*):

- **`R-168` (`FP-168`)** — sin cambio, `ABIERTA`.
- **`R-AGREGA`** — sin cambio en `milpa/procedencia.yaml` ni en `tests/test_matriz_sellados.py`: `git diff --stat -- milpa/procedencia.yaml tests/test_matriz_sellados.py` → vacío, confirmado antes de cerrar. Aplica el default explícito del encargo, **VACÍA = (a′)**: no se corre Paso 3 (ningún script, ningún `valor_ejecutable` interino); la re-estimación compuesta queda **pre-registrada** como entrada (4) de la fila-grito `FP-179`.
- **`R-169` (`FP-169`)** — sin cambio, sigue `FIRMADA-PARCIAL` (no se ratifica ni se anota "lectura alternativa").
- **`R-ENTERADOS` (`FP-171`/`FP-173`/`FP-174`/`FP-178`)** — sin cambio, las cuatro siguen `ABIERTA`.

**6 de 9 filas destino sin cambio**, declaradas así, no descubiertas después.

## 5 · Respaldo web de R-168 / R-AGREGA (dos líneas cada una, fuentes completas aquí)

Estas búsquedas no deciden nada (ninguna ranura se firmó) — documentan la base que dirección citó en su propuesta, para quien eventualmente firme.

**R-168 — nivel_ic / seed / diseño de bootstrap.** El percentil bootstrap al 95% con del orden de 10,000 remuestreos es la práctica dominante en evaluación de LLM hoy, y el bootstrap *pareado* por ítem/celda es preferible al IC por brazo porque explota el apareamiento dentro de la muestra (dos referencias con implementación concreta abajo); para el lado L (no-determinismo del LLM), el patrón vigente es cluster-bootstrap sobre k corridas por ítem, tratando input×corridas como estructura jerárquica. `seed=42` es, en cambio, **convención cultural sin propiedad estadística especial** (referencia a *The Hitchhiker's Guide to the Galaxy* — cualquier entero fijo cumple igual la función de reproducibilidad); se declara esto para no sobre-representar el respaldo de dirección en el ADR.
- [Bootstrap Confidence Intervals for LLM Evaluation — Indeed Engineering Blog](https://engineering.indeedblog.com/blog/2026/07/bootstrap-confidence-intervals-for-llm-evaluation/)
- [Bootstrap confidence intervals for your LLM eval metrics — DEV Community](https://dev.to/marcuswwchen/bootstrap-confidence-intervals-for-your-llm-eval-metrics-3599)
- [Why Pairing Your Bootstrap Is Necessary, And When It Stops Helping — DEV Community](https://dev.to/natnael_alemseged/why-pairing-your-bootstrap-is-necessary-and-when-it-stops-helping-2iim)
- [When +1% Is Not Enough: A Paired Bootstrap Protocol for Evaluating Small Improvements](https://arxiv.org/html/2511.19794)
- [Ever wondered why you often see 42 as a random seed in machine learning codes? — Medium](https://medium.com/@karimanalytics/ever-wondered-why-you-often-see-42-as-a-random-seed-in-machine-learning-codes-77bbbbfbcaf0)

**R-AGREGA — agregación de pares multi-ítem.** La vía estándar de compuesto (media/suma unit-weighted, o factor scores) sí requiere reabrir el microdato — no hay atajo válido sin caja, confirmado contra la literatura de psicometría de composite scores. El ítem único post-hoc (o cualquier peso derivado de cargas factoriales de esta muestra) queda desaconsejado porque las cargas factoriales son específicas de la muestra («sample-specific») y no replican de forma confiable entre estudios — exactamente la razón que el encargo cita para descartar esa vía.
- [Unit-Weighted Composite Score Calculator — MetricGate](https://metricgate.com/docs/unit-weighted-composite-score/)
- [How can I run factor analysis to obtain composite scores? — ResearchGate](https://www.researchgate.net/post/How_can_I_run_factor_analysis_to_obtain_composite_scores)

## 6 · Fila-grito `FP-179`

Nueva, `ABIERTA` a propósito, 5 entradas (rama (a) de E3 ya archivada; rama (b) PDF-FD por redactar; mediciones diferidas de `FP-172`; re-estimación compuesta pre-registrada por `R-AGREGA`; `APERTURA-ENFIH-ENSAFI`). No va en tsv nueva: `grep -rl` sobre `tools/` y `tests/` para las 6 colas `.tsv` de `data/` ya citadas por `INFRAESTRUCTURA-v1_0.md:240-242` → 0 resultados, confirmado — todas están en "tablas que nadie lee". El mecanismo que sí grita en cada corrida es esta fila `ABIERTA` bajo gobernanza.

## 7 · Suite y cascada

`python3 tests/check.py --baseline` corrido después de todos los cambios de árbol; resultado y comparación contra la línea base pegados en el commit de cierre. `tests/check.py` `_T25_ARCHIVOS_CONOCIDOS`: se añaden `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md` (trae bare `E1`/`E2`/`E3`/`E4`/`E5` en prosa narrativa — verificado con el mismo regex del test, corrido en vivo sobre el archivo) y `forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` (trae bare `E2`/`E4`/`E6`/`E8`, mismas referencias narrativas a actos ya censados). `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` ya estaban en la lista desde antes de este acto (verificado, sin necesidad de re-añadirlos).

## 8 · CONTADOR

**3 de 9 filas destino `FIRMADA`** (`FP-175`, `FP-170`, `FP-172`) · **6 de 9 sin cambio, declaradas** (`FP-168`, `FP-169`, `FP-171`, `FP-173`, `FP-174`, `FP-178`) · **grieta A.3 de `MAESTRA32-E3` reparada** (`ls forense/encargos/ | command grep -c MAESTRA32` → 3 tras este acto) · **cola-Ubuntu registrada con 5 entradas** bajo `FP-179` `ABIERTA` · **sin `b′`: cero pares nuevos con `valor_ejecutable`** (sigue en `3/15`, sin cambio respecto a `ADR-220`; `milpa/procedencia.yaml` intocado, confirmado por `git diff --stat` vacío).

## Lo que este acto NO hizo

No lanzó ninguna entrada de la cola. No redactó la rama (b) ni el encargo medidor. No corrió Paso 3 (R-AGREGA vacía). No tocó Hito D, censos vencidos, `limite_c2`, `FP-152`. No usó `data/raw`, red ni microdato.
