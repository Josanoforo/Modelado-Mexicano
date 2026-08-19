# ACTO SELLO-FICHA-G3 · Verificación de gate — NO se lanza el sello de `ficha-id-g3` (`FP-11`)

**Estado: GATE NO CUMPLIDO. Declarado por qué, no fracaso.** Este acto recibió el encargo de sellar `ficha-id-g3` (`FP-11`, PROPUESTA DE SELLO COMPLETA desde el 5/ago) y de redactar el encargo de ejecución `EXEC-FICHA-G3`. El propio encargo trae, en su cabecera, un gate explícito: *"lanzar después de que `LANE-A-E0-E5` fusione ... romperlo sería el ejecutor decidiendo el orden que mesa firmó. 🚫 Sin `--freeze`."* — y su bloque de VERIFICACIÓN DE EXISTENCIA marca ese punto, a diferencia de los demás (todos `EXISTE-SATISFACE`), como algo que quien ejecuta debe verificar, no algo ya dado. Verificado hoy contra el árbol real: el gate **no** está cumplido. Este acto no ejecutó C1 (la pregunta estructurada de sello), no escribió ningún ADR, no tocó `firmas-pendientes.tsv`, y no redactó `EXEC-FICHA-G3` — los cuatro, condicionados al gate por el propio texto del encargo.

Contador: cero. `FP-11` sigue `FIRMADA-CONDICIONAL`, sin encargo de ejecución. El "0 de 15" no se toca.

---

## 0 · ARRANQUE

1. **REPO.** Clon no-superficial en `/home/user/Modelado-Mexicano`. Rama `claude/sello-ficha-g3-coeficiente-tytshy`, ya creada al abrir, sin commits propios sobre `origin/main` al iniciar. `git status`: árbol limpio.
2. **SHA.** `git fetch origin main`: `origin/main` real = `290f9a0011f7b56379373f9ae6bf86a706012668` (`Merge pull request #259 from Josanoforo/claude/encargo-acto-consolida-2-v2-edbp2h`) — coincide exactamente con el SHA de redacción del encargo (`290f9a0`). `git merge-base` confirma que la rama de trabajo parte exactamente de ese commit. Sin diferencia que reportar, no hizo falta re-derivar por contenido.
3. **`data/raw`.** No se usó — este acto no abre microdato ni verifica payloads MxFLS. El propio encargo ya declaraba esos payloads "A VERIFICAR" y los condicionaba al encargo de ejecución; con el gate cerrado, verificarlos aquí habría sido trabajo fuera de lugar.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — firma correcta de nube. Sin red nueva más allá de `git fetch`; se salta la sonda `curl` contra host externo, como el propio punto 4 permite cuando el acto no toca red nueva.
5. **ESPEJO.** Ninguno usado. Toda cifra de este documento sale del clon de (1), con archivo:línea o comando citado.

## 1 · Verificación de existencia — contra el árbol, no contra lo declarado

Repetidos los puntos que el propio encargo marcó `EXISTE-SATISFACE` (no por dudar de ellos sin razón, sino porque un acto de sello no hereda verificación ajena sin repetirla — el mismo criterio que el Paso 0 de la propia ficha se exige a sí mismo):

- `forense/ficha-id-g3-v1_0.md` — EXISTE. Leída completa (173 líneas): RUTA-I, `G3·horizonte_temporal`, panel MxFLS olas 2-3, exposición `FORMAL_CONTRATO` vía tenencia de AFORE del hogar (`ah03h`, Paso 1-2), criterio en RR no en pp (Paso 2(7), lección `R3.2`/`CAL-G3`), inventario de contaminación en Paso 0, hereda la restricción de D-10 (Paso 2(2), ventana 2005-2012). La descripción del encargo es fiel al archivo — verificado línea por línea, no solo por título.
- `forense/notas/2026-08-05-s-idg3-verificacion-no-sello.md` — EXISTE. §2(1) y §2(3) citan verbatim contra `canon/gobernanza-v1_15.md:623` (ADR-57(c)) y contra el Paso 2(8)/fila `E` de la ficha — confirmado por lectura directa de ambos extremos de la cita.
- `forense/firmas-pendientes.tsv` `FP-11` (línea 12) — EXISTE, `estado=FIRMADA-CONDICIONAL`, texto verbatim: *"sellarla es decisión de mesa"*; columna `gatea`: *"contador 'coeficientes en escala del modelo' (hoy 0 de 15) — sellar esto sería el primero"*; columna `encargo`: `SIN ENCARGO`.

## 2 · El gate — verificado, no cumplido

El encargo cita `FP-26` (`firmas-pendientes.tsv:27`) como fuente del orden: DISPARADOR-A ejecuta *"verificación de MOTOR-3/E0 -> E5/FP-15 -> sello de ficha-id-g3/FP-11 [decisión de mesa propia, no se cuela aquí] -> E3-TRIAGE/FP-14 -> T20/FP-18"* — `FP-11` explícitamente **después** de `E5/FP-15`. Cuatro verificaciones independientes, todas hechas hoy contra el archivo real, no heredadas de una foto anterior:

1. **`FP-15` (`firmas-pendientes.tsv:16`).** Columna `estado` = **`ABIERTA`**. No `FIRMADA`, no cerrada. La propia fila declara qué falta: *"No falta decisión de mesa: falta un número de ADR ... `MOTOR-1 §4` ... ya derivó todo su contenido"* — es decir, falta ejecución, no deliberación de mesa.
2. **`forense/encargos/2026-08-18-LANE-A-E0-E5.md`** (el encargo que ejecutaría E0→E5 y cerraría `FP-15`), línea 5: **`Estado: VIVO`**. No fusionado, no consumido. Su propio bloque de arranque (líneas 11-22) registra `milpa/src/` ausente al redactarse.
3. **`milpa/src/`** — verificado hoy con `test -d`: **no existe**. Consistente con (2): `git log` muestra que `ACTO MOTOR-3/E0` (PR #237, commit `2abf292`) solo corrió su FASE-PLAN — *"cero código, el gate devolvió 0"* (mensaje verbatim del propio commit) — nunca la fase CON SELLO que `LANE-A-E0-E5` tiene por tarea (su Tarea, punto 1).
4. **`forense/registro-recalculo-v1_0.md:41`**, tabla §1, fila **5** (`ADR-50 / ADR-51 / ADR-57(c)`, la Entrada 5 que `LANE-A-E0-E5` debe cerrar — su Tarea, punto 3) — columna de veredicto: **`ABIERTA`**.

Los cuatro coinciden, por vías independientes (un TSV de firmas, un archivo de encargo, el estado del árbol de código, y un registro de recálculo distinto): **el gate de este acto — "LANE-A fusionó y FP-15 cerró" — no está cumplido.** No hay ambigüedad ni lectura alternativa que lo cierre.

## 3 · Decisión

**No se procede.** No se ejecuta C1 (pregunta estructurada de sello vía `AskUserQuestion`) — hacerlo presentaría como disponible una decisión de mesa que el propio programa ya fijó que no lo está todavía (`FP-26`, DISPARADOR-A). No se escribe ningún ADR. No se toca `firmas-pendientes.tsv` — `FP-11` sigue exactamente como estaba, `FIRMADA-CONDICIONAL`, `SIN ENCARGO`. No se redacta `EXEC-FICHA-G3` — su propio C3 lo describe como parte del mismo acto gateado (C1→C2→C3 secuenciales), no como pieza independiente que pueda adelantarse. El encargo, tal como llegó a esta sesión (por conversación, no pre-archivado en `forense/encargos/`), no se marca `CONSUMIDO`: no se consumió, se encontró bloqueado, y `--freeze` — el único mecanismo que el propio texto nombra para saltar el gate — no fue dado.

Esto es "declara qué falta y qué lo desbloquearía", no fracaso del encargo — que en sus propios términos (resumen fiel, perímetro, las tres opciones de C1) sigue listo para correr en cuanto el gate abra.

## 4 · Qué lo desbloquearía

1. Que `LANE-A-E0-E5` corra su fase CON SELLO completa (C1-C3 de su propio encargo: catálogo de momentos sellado, rebanada mínima del motor con holdout probado, cierre con los 15 fixes de `RONDA-M`) y cierre `FP-15` — acto propio, perímetro `milpa/src/**` y `tests/test_motor_*.py`, ajeno al perímetro de este acto.
2. Con `FP-15` cerrada y `LANE-A-E0-E5` `CONSUMIDO`, re-derivar este mismo bloque de arranque — no asumir que sigue cumplido por haber estado bloqueado antes — y recién entonces ejecutar C1-C4 del encargo original.

## 5 · Perímetro y lo que no se hizo

Tocado: este archivo (nuevo). **No tocado:** `canon/gobernanza-v1_15.md`, `forense/ficha-id-g3-v1_0.md`, `forense/firmas-pendientes.tsv`, `canon/estado-programa-v1_10.md`, `forense/hallazgos.md`, `forense/encargos/`. No se corrió ninguna estimación, no se abrió microdato, no se tocó MxFLS, no se re-diseñó nada de la ficha, no se movió `0 de 15`.

## 6 · Marcador T22 — falso positivo, explicado (A.12)

`tests/check.py` (T22, protección (b)) marcó este archivo por `_T22_MARCADOR_PENDIENTE` (`PROPUESTA.*mesa`), en la línea 3 del Estado: la línea cita, una junto a otra sin relación, "PROPUESTA DE SELLO COMPLETA" (el estado ya existente de `FP-11`, `firmas-pendientes.tsv:12`, sin cambiarlo) y "...que mesa firmó" (cita verbatim del gate del propio encargo, §2 arriba). No es una ranura nueva sin registrar: `FP-11` ya tiene su fila, sigue `FIRMADA-CONDICIONAL`, y este acto no le tocó el estado (§3, §5). Excluido vía `_T22_ARCHIVOS_CONOCIDOS` en `tests/check.py`, mismo criterio de autocaptura verbatim que las notas de `TABLERO-FIRMAS`/`CI-CATEGORIA` ya usaron para el mismo género de coincidencia.

---

**2026-08-18 (re-verificación, ENCARGO SELLO-FICHA-G3 v2).** Mismo gate, mismas cuatro señales,
re-derivadas hoy contra el árbol real, no heredadas de esta acta: `FP-15` (`firmas-pendientes.tsv:16`)
sigue `ABIERTA`; `milpa/src/` sigue sin existir (`test -d milpa/src` → ausente); `registro-recalculo-v1_0.md:41`
fila 5 (`ADR-50/ADR-51/ADR-57(c)`) sigue `ABIERTA`; `forense/encargos/2026-08-18-LANE-A-E0-E5.md`
sigue `Estado: VIVO`, no `CONSUMIDO`. Las cuatro coinciden, igual que en el ARRANQUE original de
esta acta: el gate no está cumplido. Este acto v2 se PARA en el mismo punto, por la misma razón,
sin ejecutar C1-C4 de su propio encargo ni tocar `firmas-pendientes.tsv`, `ficha-id-g3-v1_0.md`,
`canon/gobernanza-v1_15.md` ni `forense/encargos/`. `0 de 15` no se toca. Pregunta a mesa: sin
novedad sobre lo ya declarado en §4 de esta acta — sigue siendo `LANE-A-E0-E5` quien debe fusionar
y cerrar `FP-15` primero.
