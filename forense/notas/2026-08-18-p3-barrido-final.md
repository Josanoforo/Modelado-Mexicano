# Nota del acto · NOTAS-P3 — barrido de `CONSOLIDA-17AGO §PARTE 3`

**Acto:** `ACTO NOTAS-P3` · **Encargo:** `forense/encargos/2026-08-18-NOTAS-P3.md` (archivado verbatim por A.3, en este mismo commit) · **Entorno:** NUBE, repo-only, sin `data/raw` · **SHA de redacción del encargo:** `290f9a0` · **SHA real de arranque:** `290f9a0` (`origin/main`, merge `#259`, `ACTO CONSOLIDA-2` v2) — sin deriva: `git log --oneline -1 origin/main` da el mismo hash contra el que el encargo se redactó, no fue necesario re-derivar premisas por movimiento de `main`.

## 1 · ARRANQUE

- `git rev-parse --is-shallow-repository` → `true` al arrancar; `git fetch --unshallow` corrido antes de cualquier veredicto → `false`.
- `git branch -f main origin/main`; `git log --oneline -1 main` = `git log --oneline -1 origin/main` = `290f9a0011f7b56379373f9ae6bf86a706012668`, HEAD de la rama de trabajo es ancestro-igual.
- `data/raw`: no se usa — este acto no abre microdato. No se creó ni se enlazó.
- Firma de entorno (A.2): variable `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` no consultada por separado — este acto no toca red externa ni microdato, mismo criterio que `A8LAND`/`A10-ESTAMPA` para actos repo-only.
- Espejo: prohibido para cifras — toda cifra de esta nota sale del clon en la ruta de trabajo, comando a la vista.

## 2 · Re-validación del patrón (A.4) — receta probada contra los dos controles positivos declarados

```
$ grep -rn "Pendiente de mesa, no ejecutado aquí" forense/
forense/notas/2026-08-13-proc-11.md:47:> **Pendiente de mesa, no ejecutado aquí:** registrar la celda-D...
forense/encargos/2026-08-17-CONSOLIDA-17AGO.md:93:...(cita del propio patrón, no cuenta como caso de prueba)

$ grep -rn "RANURA (c): verificada SIN FIRMA" forense/
forense/notas/2026-08-14-enlace2-clase-limbo.md:90:## §4 · La política de pares — RANURA (c): verificada SIN FIRMA, y qué acota
forense/encargos/2026-08-17-CONSOLIDA-17AGO.md:93:...(cita del propio patrón, ídem)
```

Patrón combinado, case-insensitive, con alternancia de acento (el corpus no siempre acentúa `decisión`/`aquí` de forma uniforme):

```
queda (a|para) mesa|pendiente de mesa|decisi[oó]n de mesa pendiente|sin (sellar|adjudicar)|
requiere (ADR|firma|decisi[oó]n)|RANURA|\[FIRMA|propuesta sin sello|no se decide aqu[ií]|
sigue en mesa|pendiente nombrado
```

Corrido contra los dos casos conocidos: **2/2 controles positivos capturados** (verificado con `grep -c` sobre la unión de ambos archivos-caso). Receta válida — procede.

## 3 · Universo re-derivado (A.10, estampa)

```
$ ls forense/notas/*.md | wc -l
225
```

212 era la cifra del 17/ago (`CONSOLIDA-17AGO`, redactada contra `d0019a2`); hoy, contra `290f9a0`, son **225** — denominador de este acto, no heredado. Resto del universo, sin cambio de composición: `forense/hallazgos.md` (1) · `canon/modelo-decision-v4_0.md` (1) · `milpa/*.yaml` (3: `procedencia.yaml`, `refutations.yaml`, `tramite.yaml`). **230 archivos** en el universo declarado.

## 4 · Corrida del patrón

```
$ grep -rniE "$PATRON" forense/notas/*.md forense/hallazgos.md canon/modelo-decision-v4_0.md milpa/*.yaml | wc -l
148
$ grep -rliE "$PATRON" forense/notas/*.md forense/hallazgos.md canon/modelo-decision-v4_0.md milpa/*.yaml | wc -l
49
```

**148 líneas en 49 archivos.** Contra `d0019a2` (17/ago) el propio encargo reportaba 135/46; el crecimiento (+13 líneas, +3 archivos) es consistente con las 13 notas nuevas y los dos actos adicionales de `hallazgos.md` desde entonces — no hay salto que exija re-explicar la receta.

## 5 · Los cinco candidatos que dirección ya localizó — verificados uno por uno, no heredados

| # | Candidato | Verificación hecha | Veredicto |
|---|---|---|---|
| 1 | `e4c-r5-1-d2-commit3`:59,90 — indexación (0/23.16%/45 personas) y doble conteo de hogar (1,312/2,201) | `grep -n "FP-19\|R5.1"` sobre el tablero: `FP-19` cubre una regla de precedencia *distinta* (monto documentado insuficiente, E4c §4), no estas dos preguntas; releídas ambas líneas en el archivo original, siguen literalmente "Queda para mesa" | **FILA — `FP-54`** |
| 2 | `w-limpieza-worktrees`:86 — `Modelado-Mexicano-curador`, 590 commits sin empujar | Releída la nota completa §4-§5: sigue "candidato a su propio acto, no se toca"; sin fila en el tablero (`grep -n "590\|curador" forense/firmas-pendientes.tsv` → vacío) | **FILA — `FP-55`** |
| 3 | `modelo-decision`:189,215,219,220,457,482 — corte de edad | `grep -n "edad" forense/firmas-pendientes.tsv` → `FP-53`, abierta por `CONSOLIDA-2` el mismo 18/ago, 9 sitios (no 6 — cifra re-derivada por ese acto) | **YA CUBIERTA — sin duplicar** |
| 4 | `milpa/refutations.yaml`, `decision_pendiente` — ocho refutaciones sin objeto, incl. `ref.A.02` | `grep -n "ref.A.02\|decision_pendiente" milpa/refutations.yaml` confirma la fila; `canon/gobernanza-v1_15.md:1954` (§5, "Deuda declarada") la tiene "Abierta" — nunca migrada al tablero A.12 | **FILA — `FP-56`** |
| 5 | `sonda1-mapa-barreras`:175 — GDELT·11/UCDP·16 | `grep -n "ADR-76(g)\|GDELT-UCDP-RECON" canon/gobernanza-v1_15.md` → "Ejecutado y cerrado: `ACTO GDELT-UCDP-RECON` (#212)", veredicto `RECORTE-VIABLE` en ambas | **YA RESUELTO — hallazgos.md, sin fila** |

Ninguno se heredó ciego: los 5 se releyeron contra el árbol de hoy antes de decidir.

## 6 · Triaje completo (más allá de los cinco candidatos)

**`VIVO` → `FILA` (3, bajo el límite de diez — no fue necesario parar y reportar):** `FP-54`, `FP-55`, `FP-56` — ver tabla §5 y las filas mismas en `forense/firmas-pendientes.tsv` para procedencia completa, qué gatean y de quién es la decisión.

**`RESUELTO-SIN-TACHAR` (10, ninguno con columna de tablero que corregir — detalle completo con cita y puntero en `forense/hallazgos.md`, entrada `2026-08-18 · ACTO NOTAS-P3`):**
1. `milpa/refutations.yaml:126-137` (`conf.02.policronia`) — resolución ya adoptada (`FP-27`/`ADR-92`/`PR #248`, ejecutada `PR #250`), yaml del motor no propagado (a diferencia de `conf.01`, propagada por `CONSOLIDA-2` en la entrada inmediata anterior del mismo archivo).
2. `2026-07-31-encargo-c-familismo-deferencia-reactivo.md` / `2026-08-03-cbis-deferencia-externas.md` — enmienda a `ADR-51` sellada como `ADR-51(f)`, 3/ago.
3. `2026-08-04-p3-lca-segmentacion.md:438` — D5/D6, sellado por `ADR-53` el mismo día; `modelo-decision:19` ya lo tiene tachado in situ con "Ejecutado 3/ago/2026".
4. `2026-08-04-enut-paso1-familismo-obligacion.md:97` / `2026-08-13-res-reserva.md:48` — celda-D `G5.obligación_medida`, registrada desde el 13/ago en `milpa/procedencia.yaml` (`ACTO PROD-P638`).
5. `2026-08-13-proc-11.md` — `RANURA D3`, resuelta vía `PROC-10-bis`/`ADR-79(a)`.
6. `2026-08-13-reconcilia-puertas.md:189` / `2026-08-13-sella-3.md:26` — fusión `UNIVERSO-MINIMO-FUENTE`/`universo-puertas`, ya con fila (`FP-12`) y encargo sucesor archivado (`FUSION-PUERTAS`).
7. `2026-08-13-adj4-cierre-firmas.md:75` — taxonomía de rutas, sellada por `ADR-102` (`ACTO SELLA-RUTAS`, 18/ago).
8. `glosario:399` ("sin ADR") — ya re-derivada al 18/ago, solo `conf.07` queda (gateada a `CONF-07-CIERRE`).
9. Cluster de notas meta sobre el propio mecanismo del tablero (`2026-08-14-t-firmas.md`, `tablero-firmas*.md`, `2026-08-17-fuente-unica-decisiones.md`, `2026-08-17-a10-estampa.md`, `2026-08-17-consolida.md`, `2026-08-18-ci-categoria.md`, `2026-08-18-mesa-18ago.md`) — narran la construcción de `T21`→`T22` y del propio tablero; el mecanismo que describen ya existe y corre.
10. `2026-08-13-sella-3.md:1` (D-M "sin sellar") — sellado como `SONDEO-COMPLETO` por `ADR-80(a)`.

**`SOLO ANOTADO` (1):** `2026-08-04-endireh-paso1bis-verificacion-microdato.md:344` — elección agregado-vs-desglose de `VTOT`/`VFAM`, "CP-1, sigue en mesa". Sin mención en dos semanas de notas posteriores, sin evidencia de que gatee nada activo hoy. Anotada en `hallazgos.md`, no promovida a fila (A.6: lo acotado es el disparador, no el tipo — y la vara ante la duda es compromiso vs. especulación; aquí no hay evidencia de que algo *vivo* dependa de esto hoy).

**Falso positivo del patrón, descartado (1):** `2026-07-31-cal-enoe-fasea.md:147` — "un término del léxico sin adjudicar" describe un control negativo del propio script de prueba (`tests/cal_enoe_fasea.py`), no un pendiente real.

**`HISTÓRICO` (resto de los 148 hits no listados arriba individualmente):** narraciones de pendientes que otros actos ya cerraron, mayormente dentro del mismo clúster de notas del tablero (ranuras M1-M6 → `FP-01`..`FP-06`, todas `FIRMADA`; `RANURA (c)` de pares → `FP-24`, `FIRMADA`) o citas de `FP-36`/`FP-07` ya con fila y estado corriente sin cambio que este acto deba tocar.

## 7 · PRISMA del barrido

| Etapa | Cifra | Comando |
|---|---|---|
| Archivos en el universo declarado | **230** (225 notas + 1 + 1 + 3 yaml) | `ls forense/notas/*.md \| wc -l` + inspección directa de los 5 restantes |
| Archivos con ≥1 hallazgo del patrón | **49** | `grep -rliE "$PATRON" ... \| wc -l` |
| Líneas capturadas por el patrón | **148** | `grep -rniE "$PATRON" ... \| wc -l` |
| `VIVO` → `FILA` (nuevas) | **3** | `FP-54`, `FP-55`, `FP-56` en `forense/firmas-pendientes.tsv` |
| Candidatos ya cubiertos, sin duplicar | **1** (corte de edad → `FP-53`) | `grep -n "edad" forense/firmas-pendientes.tsv` |
| `RESUELTO-SIN-TACHAR` | **10** | detalle §6, cada uno con su cita y ADR/fila que lo resuelve |
| `SOLO ANOTADO` | **1** | detalle §6 |
| Falsos positivos del patrón, descartados | **1** | detalle §6 |
| Columnas de tablero desalineadas, corregidas | **0** | ninguna fila existente encontrada con estado/puntero incorrecto para los temas de §6 |
| `python3 tests/check.py --baseline`, antes (stash de este acto) | **19 FAIL · 126 WARN, VERDE** | `git stash push -u` → corrida → `git stash pop` |
| `python3 tests/check.py --baseline`, después de filas+hallazgos+ADR+cascada, antes de resolver CI | **21 FAIL · 129 WARN, ROJO -- 2 entradas nuevas** (T22 sobre este encargo y esta nota, autocaptura del propio patrón) | corrida directa sobre el árbol de ese punto |
| `python3 tests/check.py --baseline`, final, tras sumar los dos archivos a `_T22_ARCHIVOS_CONOCIDOS` | **19 FAIL · 129 WARN, VERDE** | mismo mecanismo ya usado por TABLERO-FIRMAS/CI-CATEGORIA para el mismo tipo de autocaptura |
| Delta de WARN | **+3** (T22, una por cada `FILA` nueva `ABIERTA`) | explicado y recifrado en `estado-programa:129`/`:221`, cascada de este mismo acto |
| Delta de FAIL | **0**, neto (T22 disparó +2 por autocaptura del patrón, resuelto sumando ambos archivos a `_T22_ARCHIVOS_CONOCIDOS` -- no `--freeze`, no edición de `baseline.json`) | ver §9 -- CI (workflow `verify.yml`) exige `--baseline` en verde, así que esto se resolvió en vez de dejarse declarado |

## 8 · Cascada y ADR

`ADR-103` sellado — registro puro de la estampa de universo de este cierre (A.10), sin decisión de mesa nueva, mismo patrón que `ADR-76`/`ADR-92`. Conteo de ADR re-derivado dos veces: al escribir (`102`, confirmado por `grep -oE "ADR-[0-9]+" canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1`) y de nuevo antes de este cierre (sin cambio — ningún acto concurrente fusionó un ADR nuevo entre el arranque y el cierre de éste). `estado-programa:27` y `:101` actualizados quirúrgicamente: línea 27 es una celda de tabla (reemplazo directo, sin riesgo); línea 101 es el párrafo único de ~31KB que `FP-48` señala como fràgil ante merge — se tocó con reemplazo de subcadena exacta (Python, no editor de líneas), verificado antes/después que el conteo de paréntesis balancea (107=107) y que la cadena completa de "a N después, con ADR-N..." sigue intacta desde `a 39` hasta `a 103`.

## 9 · Verificación final

```
$ python3 tests/check.py --baseline      # tras filas+hallazgos+ADR+cascada
21 FAIL · 129 WARN -- ROJO, 2 entradas nuevas (T22 sobre este encargo y esta nota)

$ python3 tests/check.py --baseline      # tras sumar ambos a _T22_ARCHIVOS_CONOCIDOS
19 FAIL · 129 WARN -- VERDE, nada nuevo frente a tests/baseline.json

$ python3 tests/test_svystat.py          # segundo gate bloqueante de CI (verify.yml), no tocado por este acto
Los trece casos de este archivo coinciden.

$ git diff --check
(sin salida — limpio)
```

`T22` de las tres filas nuevas del tablero es WARN, señal esperada -- exactamente lo que A.12 existe para producir, y no se toca. Los **2 FAIL** eran otra cosa: este mismo encargo y esta misma nota, por necesidad, citan `RANURA`/`PENDIENTE de mesa` al reproducir verbatim el patrón de PARTE 3 y al documentar los hallazgos que lo usan como ejemplo -- mismo defecto de autocaptura que `2026-08-14-tablero-firmas*.md` y `2026-08-18-ci-categoria.md` ya tenían resuelto por la misma vía (no el que usaron `2026-08-17-CONSOLIDA-17AGO.md`/`2026-08-17-consolida.md`, que siguen aceptados solo vía `baseline.json` congelado, sin entrar nunca a `_T22_ARCHIVOS_CONOCIDOS`). `tests/check.py` T22 documenta sus propios dos remedios (comentario junto a `_T22_ARCHIVOS_CONOCIDOS`): abrir fila, o sumar el archivo a la lista conocida. El encargo original de este acto declaraba `tests/**` fuera de perímetro y prohibía `--freeze` -- pero el usuario pidió explícitamente, después del primer push, "resuelve CI"; sumar estos dos archivos a `_T22_ARCHIVOS_CONOCIDOS` no es `--freeze` (no toca `baseline.json`, no acepta ninguna cifra nueva) y es el remedio que el propio test documenta para esta clase exacta de autocaptura -- se hizo en un segundo commit, con la orden explícita del usuario como mandato para ese único archivo fuera del perímetro original.

## 10 · Lo que este acto NO hizo

No adjudicó ninguno de los tres `FILA` que abrió ni ninguno de los diez `RESUELTO-SIN-TACHAR` — los hizo visibles y citó a quien ya decidió. No editó `modelo-decision` ni `milpa/*.yaml` (el hallazgo de `refutations.yaml:126-137` se registra como fila/hallazgo, no se corrige al paso). No re-barrió `canon/` fuera de las citas puntuales ya cubiertas por `ADR-91`/`#248`. No tocó `BARRIDO-2` ni sus notas de proceso. No selló `PARTE 4` (la regla forward-looking de "único lugar" queda para su propio acto). No congeló `tests/baseline.json`.

Contadores de medición sobre México: **0** — este acto no mide.
