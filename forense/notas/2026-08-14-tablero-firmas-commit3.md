# ACTO TABLERO-FIRMAS COMMIT 3 · Reconciliación tras `origin/main` — el propio acto verifica que su tablero sigue siendo verdad

Commit 3, no anticipado por el encargo original: mientras Commits 1-2 corrían, `origin/main` avanzó con tres actos ajenos, dos de los cuales tocan directamente el contenido del tablero. Se documenta como acto propio (mismo criterio que `ACTO MOTOR-1`/`forense/CASCADA-M1-2026-08-14.md` ya usó para "origin/main se movió DOS veces durante un solo acto") en vez de silenciarlo dentro de los commits anteriores.

## §0 · Lo que llegó

```
$ git fetch origin main
$ git log HEAD..origin/main --oneline
```
→ 12 commits, tres PR: `#236` `ACTO ENLACE-2` (adjudicación de 68 `SI_O_REFERENCIADO` + 19 `INDEXADO-NO-DESCARGADO`), `#237` `ACTO MOTOR-3/E0` (los cinco archivos del espejo — compass ×3 + RT-B/RT-D — aterrizan; FASE-PLAN de `milpa/src/`), `#238` `ACTO RECONCILIA-SPEC` (reconciliación de `especificaciones-produccion.json`).

`git diff HEAD...origin/main --stat` acotado a lo que el tablero vigila: `canon/estado-programa-v1_10.md`, `canon/gobernanza-v1_15.md` (las citas de WARN — colisión esperable, ver §1), `data/curacion-registro/especificaciones-produccion.json` (**exactamente** lo que `FP-23` señalaba), cinco archivos nuevos en `forense/` (compass ×3, red-team ×2), y los encargos/notas de `ENLACE-2`/`MOTOR-3-E0`/`RECONCILIA-SPEC`.

## §1 · Merge y sus dos conflictos

`git merge origin/main --no-edit` → `CONFLICT (content)` en `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md`, ambos en las mismas citas de WARN que Commit 2 ya había sincronizado (`gobernanza:764,856`, `estado-programa:129,221`) — `ACTO MOTOR-3/E0` las sincronizó también, de forma independiente, desde el mismo punto de partida (119 WARN) pero en dirección contraria (−11 por los archivos del espejo landing, contra +19 de este acto por `T21`). Mismo patrón que la colisión de `ADR-73` entre `ADJ-4` y `ALIAS-P`: **ninguno de los dos erró**, cada uno derivó correcto contra el terreno que tenía delante. Resuelto conservando ambas narrativas (mine primero, cronológicamente escrita antes; la de `MOTOR-3/E0` después, fusionada primero a `main`), con una frase de reconciliación explícita en vez de elegir una y perder la otra.

**Número de ADR: sin colisión.** `T15` contra el árbol fusionado: únicos 84, max 84, sin huecos — ninguno de los tres PR ajenos selló un ADR nuevo (los tres son higiene/reconciliación de CI, no decisiones de mesa nuevas).

## §2 · Verificación fila por fila contra el árbol fusionado — no se hereda nada

**`FP-23` (`especificaciones-produccion.json`).** `grep -n "requiere_decision" data/curacion-registro/especificaciones-produccion.json` → las cuatro entradas en `"NO"`, incluidas las dos que este mismo tablero había registrado `ABIERTA` horas antes. `forense/notas/2026-08-14-reconcilia-spec.md` confirma: línea 61 (`ESP-OPACA-B-d13ec4fe`, `norma_de_género`) corregida citando `ADR-75(a)`; línea 106 (`ESP-OPACA-C-9ecb5c61`, `radio_confianza`) corregida citando `ADR-82`. `FP-23` → `FIRMADA`, `ACTO RECONCILIA-SPEC`, `PR #238`.

**`FP-01`-`FP-06` (M1-M6).** `grep -n "Firma de mesa (M" forense/ADR-MOTOR-2-esqueleto-2026-08-14.md` → las seis siguen `[FIRMA M_ — VACÍA]`, sin cambio — el archivo del esqueleto no fue tocado por ningún PR ajeno. Pero `forense/notas/2026-08-14-motor3-plan.md` y la cascada de citas en `gobernanza:764/856` (ver §1) declaran, verbatim, "resuelta en el terreno la M6 que `ADR-68(e)` exigía" — la **precondición** de M6 (los cinco archivos en el repo) está cumplida; la **ranura** (la firma verbatim de mesa) no lo está. Se distingue explícitamente en `FP-06`, no se marca `FIRMADA` por la precondición sola.

**Archivos nuevos con marcador, verificados uno por uno (`T21` los encontró, no un grep manual):**
- `forense/encargos/2026-08-14-MOTOR-3-E0-autocontenido.md` — cita `[RANURA M2/M3/M5 del ADR]`, las mismas tres ya cubiertas por `FP-02/03/05`. Sumado a `_T21_ARCHIVOS_CONOCIDOS`, sin fila nueva — no es una firma distinta, es otro documento que depende de la misma.
- `forense/encargos/2026-08-14-ENLACE-2-adjudicacion-68-y-19.md`, `forense/notas/2026-08-14-enlace2-68-mas-19.md`, `forense/notas/2026-08-14-enlace2-clase-limbo.md` — los tres citan una `RANURA (c)` **distinta**: la política de pares para `relaciones.tsv` (fila `SI` + fila "gemela" `NO_DETERMINADO`, mismo `necesidad_id`). Verificado en `forense/notas/2026-08-14-enlace2-clase-limbo.md` §4: dos fuentes fuera del repo (`AJUSTE-PLAN-v3_1-2026-08-13.md`, `PLAN-MULTIFASE-F0-F6-2026-08-13.md`) la declaran `PROPUESTA` desde el 13/ago; `grep` sobre los 84 ADR de `gobernanza`, cero resultados — nunca se selló. `ACTO ENLACE-2` no la adjudicó ("enlaza los sin-par y lo declara", 48 de 68 resueltas, 20 quedan con par intacto). Fila nueva: **`FP-24`**.

**Nota sobre "la política de pares de relaciones" del encargo original.** `FP-10` (precedencia de `universo-puertas-*.tsv`, `ADR-76(e)`) fue la lectura adoptada el 14/ago por la mañana, sin coincidencia literal en el árbol de ese momento. `FP-24`, aparecida horas después con el nombre "política de pares" verbatim en dos planes de mesa, es un candidato más literal. Ninguna de las dos se descarta — ambas son reales, ambas están sin firma, y el propio `A.12` prefiere la fila de más ("el tablero prefiere falso-pendiente a limbo"); si mesa confirma cuál es "la" política que el encargo señalaba, la otra queda como lo que genuinamente es: otro pendiente real, no un error de lectura.

## §3 · Contadores

Tablero: **24 filas → 19 `ABIERTA`, 5 `FIRMADA`** (antes de este commit: 23/19/4; `FP-23` sale de `ABIERTA`, `FP-24` entra).

**Autocorrección, declarada, no escondida.** La primera pasada de este commit escribió las citas mutables con `127 WARN`, derivado de la aritmética de rama (138+108−119) que el propio texto ya advertía como no autoritativa. Al correr `python3 tests/check.py` una vez más, ya con la nota de este commit en el árbol (que cita verbatim, para verificar `FP-24`, dos documentos de mesa fuera del repo), la corrida real dio **129 WARN, no 127** — y un `T21` FAIL nuevo: la propia nota, al citar el patrón de marcador para documentarlo, se autocapturó (mismo fenómeno que ya tuvo Commit 2 §5, segunda vez que el mecanismo se prueba a sí mismo contra un archivo genuinamente nuevo). Dos correcciones, ambas en este mismo commit: (1) la nota se sumó a `_T21_ARCHIVOS_CONOCIDOS`; (2) las **seis** citas mutables (`gobernanza:764,856,1274`, `estado-programa:129,221`, más `gobernanza:1360` — la propia "Enmienda in situ" de este commit, que había repetido el error ya aprendido en Commit 1 (`ADR-84`, primera redacción): hornear el total completo `20 FAIL` dentro del patrón en negritas que `T16` compara contra el núcleo `18`, no contra la corrida completa) se resincronizaron contra la corrida real, no contra la aritmética.

`python3 tests/check.py`, corrida final: **20 FAIL · 129 WARN** — 18 FAIL núcleo (`CHECK_SELFCHECK_CHILD=1`) + 2 T16 permanentes (`gobernanza:1106,1136`, sin cambio, congelados desde antes de este acto). `T21`: 0 FAIL, 19 WARN (una por fila `ABIERTA`).

`python3 tests/check.py --baseline`: ROJO, **22 entradas nuevas** (19 `T21` `ABIERTA` + 2 `T03` de la propia nota de este commit, citando en backticks `AJUSTE-PLAN-v3_1-2026-08-13.md`/`PLAN-MULTIFASE-F0-F6-2026-08-13.md` — documentos de mesa reales, fuera del repo, mismo patrón I-01 que ya tiene bucket propio en `tests/baseline.json` + 1 consecuencia aritmética de T16 permanente, mismo fenómeno que Commit 2 §5) contra `tests/baseline.json` — que ahora trae el `head` que `ACTO MOTOR-3/E0` recongeló (`640a74d`) durante su propio CI fix, fusionado limpio, sin conflicto; 2 entradas de la línea base previa ya no aparecen (mejora, no bloquea). No se recongela aquí, mismo razonamiento que Commit 2.

## §4 · Perímetro tocado

`canon/gobernanza-v1_15.md` (resolución de merge + enmienda in situ de `ADR-84` + su propia autocorrección de cifra) · `canon/estado-programa-v1_10.md` (resolución de merge + nota de enmienda + su propia autocorrección de cifra) · `forense/firmas-pendientes.tsv` (`FP-23`→`FIRMADA`, `FP-06` nota, `FP-24` nueva) · `tests/check.py` (`_T21_ARCHIVOS_CONOCIDOS` +5, la quinta es esta misma nota) · `forense/hallazgos.md` (una entrada) · esta nota. Ningún archivo de `milpa/`, `data/` (fuera de la lectura de verificación) ni `canon/modelo-decision-v4_0.md`.
