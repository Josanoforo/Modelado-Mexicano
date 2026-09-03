# ENCARGO · ACTO MESA-18AGO — nueve firmas propagadas, las vencidas cerradas, el disparador partido

**SHA de redacción:** `ae25137` (merge #255, `origin/main`, verificado por `ls-remote` el 18/ago/2026)
**Entorno asignado:** **NUBE** (sesión nueva, clon fresco, no superficial). No toca microdato.
**Estado:** `CONSUMIDO` — ejecutado 18/ago/2026, rama `claude/new-session-yzskdx`. `ADR-100`/`ADR-101` sellados; detalle completo en `forense/notas/2026-08-18-mesa-18ago.md`.
**Concurrencia declarada:** corren en paralelo `GATE-DURABLE-V7` (Ubuntu: `barrido2_material.py` + productos de `curacion-universo`) e `INTEGRATE-T23` (cloud: `integrate_barrido2.py` + `tests/check.py`). **Cero archivos de trabajo en común con este acto. La colisión TRIPLE de número de ADR es esperada** — re-deriva al escribir y otra vez al fusionar; protocolo con cinco precedentes. `forense/hallazgos.md` es `merge=union`; si tu merge toca `estado-programa:101`, cláusula por cláusula (es FP-48, y este mismo acto sella su remedio sin ejecutarlo).
🚫 No congeles. Este acto debe cerrar con línea base VERDE por construcción.

---

## §0 · PROTOCOLO DE PROMPTS A MESA — mesa lo autorizó verbatim: *"que la sesión de cloud lo promptee para aprobarlo"*

Cuatro puntos de este acto necesitan palabra de mesa que hoy no existe en texto. En cada uno: **pregunta estructurada** (el mecanismo de ADR-86/88/90 — citas la fila y las opciones, registras la respuesta **verbatim** en el ADR), y **nada se sella sin la respuesta**. Si mesa no contesta alguno, ese inciso queda `PROMPT-SIN-RESPUESTA` en el tablero y el resto del acto cierra igual.

| # | prompt | opciones a presentar |
|---|---|---|
| P1 | **M6** — la ranura `[FIRMA M6 — VACÍA]` del esqueleto de ADR-MOTOR-2. Precondición cumplida desde PR #237 (los 5 dictámenes en `forense/`) | texto libre de firma, o "firmo M6 tal cual" |
| P2 | **FP-51** — mesa dijo *"Esa regla ya no sirve, nos detuvo más de lo que funcionó."* Lectura propuesta: muere el recongelado rutinario **y el trámite caso-por-caso de ADR-76(f) que lo acompañaba**; se sella la regla de FP-51 (recongelar >1 vez = test mal categorizado; el recongelado queda para el caso único con ADR) | (a) confirmo esa lectura, séllala · (b) mi frase era otra cosa: [texto] |
| P3 | **FP-18** — T20 para "llaves de identificación ejercidas": la propia fila dice *"pregunta lista para mesa"* desde que el contador se movió 0→1 el 13/ago | (a) se instrumenta · (b) no · (c) se difiere con razón |
| P4 | **FP-33/FP-42** — "las cuatro preguntas del transfer" no existen en el árbol (verificado: disco completo, cero resultados) | mesa pega el texto inline, o declara `IRRECUPERABLE` y FP-33 se re-especifica post-barrido |

---

════════ ARRANQUE ════════
1 · REPO. Clon fresco si no hay; `git rev-parse --is-shallow-repository` → `false` o `--unshallow`. Reporta ruta · `git log -1` · `git status`.
2 · SHA. Contra `ae25137`. Main se mueve rápido hoy (tres carriles): si avanzó, re-deriva el bloque de existencia y reporta antes de editar.
3 · data/raw. AUSENTE NO ES PARO — este acto no la usa.
4 · ENTORNO (A.2): variable cruda · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` (nunca `-I`) · `ls data/raw/ 2>/dev/null | head -1`. Un 403 es la allowlist de esta caja, no INEGI (A.5).
5 · ESPEJO. Toda cifra del clon, con comando.
════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe, contra `ae25137` ═══
```
esqueleto del sello:  forense/ADR-MOTOR-2-esqueleto-2026-08-14.md (109 líneas)      EXISTE-SATISFACE
contenido de E5:      forense/encargos/2026-08-14-MOTOR-1-consolidado.md §4          EXISTE-SATISFACE
expedientes FP-47:    data/curacion-registro/expedientes-produccion/
                      t0-89f4c3a49c00c0e1/ESP-OPACA-{A-7baf278d,B-d13ec4fe,
                      C-9ecb5c61,D-d800e103}/                                        EXISTE-SATISFACE
                      · mecanismo: prepare_production.canonical_analyst_spec incrusta
                        baseline_sha256; los 4 divergen de la maestra tras el bootstrap
                        (4dd527eb → db88a09a)
método de FP-29:      forense/benchmark-enlace-invarianza-v1_0.md + estándar sellado
                      por ADR-76(d)(4)/ADR-80 ("argumento de vinculación declarado")
                      + espec operativa forense/notas/2026-08-04-c06a-…-conf06 §5-§6  EXISTE-SATISFACE
cola de FP-17:        data/cola-adquisicion-2026-08-12.tsv — 54 filas, columnas
                      incluyen clasificacion_a4_previa y palanca; las 15 se DERIVAN
                      por clasificación, no se teclean                               EXISTE-SATISFACE
texto FP-24 (FP-42):  ADR-93 "adopta como canónico el texto de la política de pares"
                      — VERIFICA que el texto esté ahí; si está, esa mitad de FP-42
                      venció; si no, P4 se amplía                                    A VERIFICAR
las 4 preguntas FP-33: NO-ENCONTRADO en el árbol (disco completo barrido, cero)      → P4
registro-recalculo:   forense/registro-recalculo-v1_0.md existe; ⚠️ mi control de
                      formato (`grep -c "^## Entrada"`) dio 0 — la receta del
                      encabezado NO es esa. Deriva el formato leyendo el archivo.
D-1, nodo E0:         ACTO MOTOR-3/E0 corrió al menos parcial (PR #237). Su estado
                      de cierre NO está verificado aquí — lo derivas tú en C6.
```
═══════════════════════════

**PERÍMETRO.** `canon/gobernanza-v1_15.md` (ADR multi-inciso + las 5 líneas de FP-52) · `forense/firmas-pendientes.tsv` · `canon/estado-programa-v1_10.md` (**solo** `:27`/`:101` cascada y `:136`-`:137` para FP-44/45 — ⚠️ FP-48) · `forense/registro-recalculo-v1_0.md` (E5, condicional) · `forense/ADR-MOTOR-2-esqueleto-…md` (solo la ranura M6) · `data/curacion-registro/expedientes-produccion/**` y lo que la herramienta canónica regenere (FP-47) · `forense/encargos/` (los nuevos, VIVO) · `forense/notas/` · `forense/hallazgos.md` (append). **NO toca:** `tests/**` · `tools/**` (salvo **leer** `prepare_production` para FP-47; si re-firmar exige **correr** algo que escriba fuera de esta lista o pida corpus → PARA en ese inciso y deja encargo) · `milpa/` · `glosario`/`integrador`/`corpus/reports` (eso es CONSOLIDA-2) · `hitoD-preregistro` (FP-43 es de CONSOLIDA-2). Fuera de la lista: PARA.

---

## C1 · Las nueve firmas de hoy, verbatim al ADR

Regístralas tal como mesa las escribió — son la fuente de todo lo demás:

> **D-1** *"se parte."* · **D-2** *"Se arregla, ni hablar."* (ya ejecutándose: GATE-DURABLE-V7) · **D-3** *"Esa regla ya no sirve, nos detuvo más de lo que funcionó."* (→ P2) · **D-4** *"concuerdo, mecanismo puntual, generalización caso por caso con ADR."* · **D-5** *"restauración línea por línea."* · **D-6** *"se re-firman con V5."* · **D-7** *"Partirlo completamente."* · **D-8** *"Para esto se hizo un benchmark web, encontramos la forma de 'reconciliar' esas diferencias, me sorprende que lo volvamos a tratar…"* · **D-9** *"Llamémoslos para cerrarlo."* · **D-10** *"démosle fila."*

## C2 · Las vencidas y los punteros — que ninguna vuelva a replantearse

- **FP-34 → FIRMADA.** Verifica la premisa (gateaba en "fusión de #244", ya ocurrió; ADR-95 selló tres de las cuatro decisiones) y sella el inciso que le faltaba: el texto de **privacidad** queda canónico **por cita al encargo archivado** (`forense/encargos/2026-08-17-BARRIDO-2-…md §0`), no reescrito.
- **FP-24.** Sin acción de decisión — su gatea gana el puntero: *"política sellada (ADR-93 texto, ADR-95 aplicación dinámica); lo ejecutable es FP-46"*.
- **FP-29.** No se adjudica el 22% aquí. La fila gana el puntero que le faltó y que causó el re-planteo a mesa: método = `benchmark-enlace-invarianza-v1_0.md` + estándar ADR-76(d)(4)/ADR-80; procedimiento = nota 4/ago §5-§6; **pendiente real = solo la adquisición de las series** (WVS/Pew/Latinobarómetro → carril de ADQ). Línea en `hallazgos.md`: *la fila se replanteó a mesa porque no citaba su propio método ya sellado — defecto de puntero, no de decisión.*
- **FP-42.** Verifica ADR-93 (mitad FP-24); la mitad FP-33 va a P4.

## C3 · Firmas simples al tablero

- **FP-49 → FIRMADA** con D-4 verbatim: SENAL es mecanismo puntual de T22; generalizar exige ADR caso por caso.
- **FP-51** → tras **P2**: si (a), FIRMADA y la regla se sella en `gobernanza` con su falsador y caducidad tal como la fila ya los trae — y el inciso declara que **sustituye** el caso-por-caso de ADR-76(f); si (b), registra la corrección verbatim y deja la fila como mesa diga.
- **FP-18** → tras **P3**, FIRMADA con la respuesta; si (a), escribe el encargo `T20-LLAVES` (va a `tests/` → carril cloud, **después** de que INTEGRATE-T23 fusione).
- **FP-17 → FIRMADA** con D-9: lote completo, orden = la columna `palanca` existente de la cola. **Deriva las 15 filas por su clasificación** (`EXISTE-NO-VERIFICADO`), pega el comando y el conteo. La ejecución es el encargo `ADQ-15` (C10) — Ubuntu, post-GATE, porque necesita red a las fuentes.

## C4 · M6 y el sello de MOTOR-2

Tras **P1**: escribe la firma en la ranura del esqueleto (único cambio permitido a ese archivo, más el número), copia el esqueleto a `gobernanza` como el ADR siguiente (re-derivado), y pasa **FP-01..FP-06** a FIRMADA (`firmada_en` = ese ADR, `ejecutada_en` = este acto). **Declara en el inciso, sin excepción:** el sello adopta el diseño (M1-M6); **la re-verificación de M2/M4/M5 contra los productos semánticos del barrido queda en el carril B y no la sustituye este sello.** Es la condición bajo la que D-1 es seguro.

## C5 · D-1 — el disparador, partido

Enmienda in situ sobre la fila FP-26 (texto original intacto) + inciso de ADR:

- **DISPARADOR-A (no consume semántica del barrido — arranca YA):** verificación de E0 → E5/`FP-15` → sello de `ficha-id-g3` (`FP-11`, **decisión de mesa con su propuesta completa a la vista** — sería el primer coeficiente, 0→1 de 15; no se cuela en este batch) → `E3-TRIAGE` (`FP-14`, gate cumplido) → `T20` (`FP-18`, según P3).
- **DISPARADOR-B (sí consume — espera §28 completo):** re-verificación M2/M4/M5 → lo que la fase semántica gatee. `FP-32`/`FP-33` siguen post-cierre por diseño propio.
- **FP-10/FP-12:** asigna su carril **por contenido, no por lista** — deriva si consumen productos semánticos del barrido (sus perímetros son `data/universo-puertas*`); lo que derives, ese es su carril, y lo dices.

## C6 · E5, condicional a E0

Deriva primero el estado de cierre de `ACTO MOTOR-3/E0` (PR #237: ¿cerró completo?). **Si cerró:** ejecuta E5 — la Entrada 5 de `registro-recalculo` con el contenido que `MOTOR-1 §4` ya derivó (universo a citar, veredicto `57(c)` = SIN CAMBIO, y la cifra que **no** debe copiar: llaves = **1 de 2, no 0**). Formato de entrada: **derívalo del propio archivo** — el control `^## Entrada` da 0, esa no es la receta. **Si E0 no cerró:** no ejecutes; escribe el encargo `LANE-A-E0-E5` y dilo. En ningún caso decides nada: propagas lo derivado.

## C7 · FP-47 — la re-firma, por la herramienta y no a mano

Lee `prepare_production.canonical_analyst_spec` (solo lectura de `tools/`). Re-deriva el `baseline_sha256` **vigente** de `data/curacion-registro/baseline.json` — la "V5" de mesa es *el vigente al ejecutar*, no una constante. Regenera las cuatro especificaciones por la vía canónica, marca los expedientes re-firmados citando D-6 verbatim, y verifica que la divergencia contra la maestra queda en cero (el test que la fila cita). **Si la regeneración exige correr producción o abrir corpus: PARA en este inciso**, deja el encargo `REFIRMA-OPACA` para Ubuntu y sigue.

## C8 · FP-52 — restauración línea por línea

Las cinco sobreescritas (`gobernanza:764 · :856 · :1274 · :1387 · :1393`): re-deriva tú los commits de sello (la tabla vive en `forense/notas/2026-08-18-t16-historicas.md` — verifícala, no la heredes), restaura **cada línea desde su commit de sello**, conserva el `{cita-historica}`, y añade al final de línea el rastro `*(restaurada a su valor de sello por ACTO MESA-18AGO, D-5)*`. **Si el diff de una línea contiene algo más que cifras y rastros de resync, PARA en esa línea y repórtala como mixta** — `:1274` es la candidata, su prosa narra su propia trayectoria. Las tres nunca sobreescritas no se tocan. Al final: `T16 [ok]`, línea base VERDE, **cero freeze** — si no, el commit se revierte y se reporta.

## C9 · FP-44 · FP-45 · FP-37

- `estado-programa:136-137`: los textos ya redactados (verifícalos por contenido en la nota de CONSOLIDA/notas del 17/ago, no por número de línea). Ejecuta y marca las dos filas.
- **FP-37:** intenta la derivación por comando del censo de estimabilidad; si el alcance excede una sesión corta, escribe el encargo `CENSO-CMD` y deja la fila con el puntero. No la finjas.

## C10 · Los encargos que faltaban, escritos VIVO (no lanzados)

Con convención completa (ARRANQUE + A.8 + entorno + SHA de este acto): `FP10-PRECEDENCIA` · `FUSION-PUERTAS` (FP-12) · `E3-TRIAGE` (FP-14) · `ADQ-15` (FP-17 — **Ubuntu, gateado a que GATE-DURABLE-V7 fusione**, las 15 filas derivadas dentro) · `ESTADO-SPLIT` (FP-48, D-7 — **gateado a que GATE-DURABLE-V7 e INTEGRATE-T23 fusionen**, porque parte el archivo que los tres tocan) · y `LANE-A-E0-E5` o `T20-LLAVES`/`REFIRMA-OPACA` solo si C6/C3/C7 los dejaron pendientes.

## C11 · Cierre

ADR multi-inciso (número re-derivado dos veces: al escribir y al fusionar — colisión triple esperada) · cascada `:27`/`:101` con el número final · re-conteo del tablero **derivado** (estados, y cuántas ABIERTA quedan) · nota del acto con la lista de prompts y sus respuestas verbatim · línea en `hallazgos.md` · encargo `CONSUMIDO`.

**Auditoría (lo aplicable):** contadores de medición sobre México: **cero — salvo que C6 ejecute E5**, que mueve el contador de entradas de `registro-recalculo` adjudicadas (aparato) y **cita** llaves `1 de 2` sin moverlo. Dilo con esa precisión. Ninguna cifra tecleada. ¿Qué afirmación describe el estado del corpus escrita a mano? — ninguna: prompts, punteros y restauraciones llevan comando o respuesta verbatim.

**Lo que NO hace:** no ejecuta FP-46 (acto propio en `data/`, conviene post-GATE con la evidencia E2 fresca) · no sella `ficha-id-g3` (FP-11 es la siguiente decisión de mesa del carril A, con su propuesta a la vista) · no lanza los encargos que escribe · no toca lo de CONSOLIDA-2 · no congela.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-18-MESA-18AGO-nueve-firmas.md" canon/gobernanza-v1_15.md` → 2: citado bajo ADR-100, ADR-101 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
