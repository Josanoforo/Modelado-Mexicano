# Encargo `SELLA-A1-CODI` — aterrizar `benchmark-unidad-homogenea-codi-spei-v1_0.md` verbatim y propagar la firma de mesa sobre `FP-104` (fila A1, enmienda §10.7)

**SHA de redacción:** `c502a43` (`origin/main` al redactar, verificado por clon en la sesión de dirección del 25/ago/2026). Si `main` se movió al arrancar: NO es PARO — refresca, re-deriva lo que dependa del perímetro y reporta la diferencia antes de editar.
**Redactado por:** sesión de dirección (maestra), conversación del proyecto, 25/ago/2026. Mandato de mesa verbatim: *«dame el encargo ahora si, para subir este archivo y sellar la decisión»*.

**ENTORNO ASIGNADO: NUBE (`cloud_default`).** Este acto no toca microdato ni red de datos. **NO lanzarlo en UBUNTU** (esa capacidad se reserva para actos con corpus) **y no lanzarlo en los dos entornos a la vez** — las dos veces que esa línea faltó, el encargo salió duplicado.

**ADJUNTOS REQUERIDOS en el mensaje de lanzamiento — sin cualquiera de los dos, PARO en F0 sin tocar nada:**
1. El archivo `benchmark-unidad-homogenea-codi-spei-v1_0.md` — **sha256 `2ed226e7207d13d05800b2a5f781adcd75dd5c369ba0b599fc76bca001b71679`**, 85 líneas.
2. La **firma de mesa**, como línea propia del lanzamiento (ranura en F0).

---

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara (`c502a43`). Si `main` se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Este acto NO descarga nada.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado: `cloud_default`. Este acto no toca microdato ni red de datos: dilo y salta la sonda. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien ESCRIBE el encargo (dirección, 25/ago/2026, contra `c502a43`) ═══

1 · ESTRUCTURA. Tablas gobernantes de este dominio: `forense/firmas-pendientes.tsv` (tablero, regla A.12) · `canon/gobernanza-v1_15.md` (registro de decisiones/ADR) · `forense/ficha-r34-conda-v2-spec.md` (ficha del par, enmiendas fechadas) · `canon/estado-programa-v1_10.md` (sincronía). `data/INFRAESTRUCTURA-v1_0.md` gobierna tablas de `data/` — este acto no toca ese dominio. Este encargo ESCRIBE: las cuatro nombradas + `forense/` (benchmark, nota, encargo archivado). Deliberadamente NO escribe: `milpa/` (la firma adjudica una condición, no un coeficiente del ejecutable), `forense/hitoD-preregistro-v2_0.md` y `README.md` (R3.4 sigue SIN veredicto integrado — B y C con base medida 0 de 2 — así que Hito D no se mueve), `tests/aceptacion_r3_4.py` (el gate integrado sigue NO-ADJUDICADO; ADR-160 ya declaró correcto su xfail).

2 · CONTENIDO. Comandos corridos por dirección, salida cruda:
- `find . -iname "*benchmark*codi*" -not -path "./.git/*" | wc -l` → **0** (árbol completo salvo `.git`). **NO-ENCONTRADO** — el benchmark no existe en el árbol.
- grep del sha `2ed226e7` sobre **1,909 archivos** del árbol → **0**. **NO-ENCONTRADO.**
- Tablero: `FP-104` estado = **ABIERTA** (comando csv estándar del §1 del transfer). **EXISTE-NO-SATISFACE** — la fila existe y la firma no está dada.
- `grep -c "### 10.8" forense/ficha-r34-conda-v2-spec.md` → **0** (1 archivo, 396 líneas). La enmienda de sello NO existe aún.
El ejecutor RE-CORRE estos cuatro comandos en F0 contra su base; si alguno cambió (p. ej. `FP-104` ya `FIRMADA`), el trabajo ya está hecho total o parcialmente: **PARA y reporta** (A.8) en vez de duplicar.

3 · COBERTURA RETROACTIVA. Nacimiento por `git log --diff-filter=A`: tablero **2026-08-14** (`6e0f2a1`) · ficha **2026-08-24** (`71f2be8`) · gobernanza **2026-07-30** (`8a341da`). Todo lo que este acto toca es posterior al nacimiento de sus tablas gobernantes — sin brecha retroactiva.

════════════════════════════════════════════════════════════════════

## PERÍMETRO Y CONCURRENCIA

**Archivos que este acto toca, lista cerrada:**
- `forense/benchmark-unidad-homogenea-codi-spei-v1_0.md` — NUEVO, byte-idéntico al adjunto.
- `forense/firmas-pendientes.tsv` — solo la fila `FP-104`.
- `forense/ficha-r34-conda-v2-spec.md` — solo APPEND de la enmienda fechada §10.8; §1–§10.7 no se editan hacia atrás.
- `canon/gobernanza-v1_15.md` — ADR nuevo + cabecera (conteo).
- `canon/estado-programa-v1_10.md` — recifrado estándar (cabecera/L0, línea de suite; los `:N` pueden haber derivado — derívalos, no los supongas).
- `forense/notas/2026-08-25-sella-a1-codi-cierre.md` — NUEVA (sufijo `-cierre`, T02).
- `forense/encargos/2026-08-25-SELLA-A1-CODI.md` — este texto, archivado `CONSUMIDO` con su PR (A.3).

**"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."**

**Concurrencia conocida al redactar:** PR de Codex `codex/autoridad-semantica-marco-produccion` abierto — su perímetro es intocable desde Claude (`tools/curador_registro/**`, `data/curacion-universo/**`, `generar_marco`); ramas residuales `claude/fp57-…` y `rescate/reconcilia-puertas-local` sin fusionar, no se tocan. Mesa declara en el lanzamiento si lanzó algo más desde el corte. Colisiones de numeración ADR/FP al fusionar son normales: renumera quien fusiona segundo, re-derivando el máximo con el grep de la casa (forma corregida de `ADR-169`: `command grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | command grep -oE '[0-9]+' | sort -n | tail -1`).

---

## F0 · Compuertas — antes de escribir una sola línea

1. **Adjunto.** Verifica `sha256sum` del archivo adjunto == `2ed226e7207d13d05800b2a5f781adcd75dd5c369ba0b599fc76bca001b71679`. Ausente o discordante → **PARO** (reporta el sha real; A.7: si discordara, di qué campo cambió antes de concluir nada).
2. **Firma.** Busca en el mensaje de lanzamiento la cadena `FIRMO FP-104` **como línea propia de mesa, fuera de la cita de esta compuerta** (la autocaptura verbatim de una compuerta no es autorización — precedente `FP-63`/`ACTO SELLA-AGO25-F` L5). Ausente → **PARO sin tocar nada**. La firma esperada (mesa puede adoptarla o dictar la suya; se propaga la que venga):
   > **RANURA — FIRMA DE MESA:** `FIRMO FP-104: fila A1 con enmienda 10.7 (unidad homogénea, sin enlace), solo pata A, reservas de la ficha + benchmark CoDi-SPEI incluidos.`
3. **A.8 en fresco.** Re-corre los cuatro comandos del bloque de existencia. `FP-104` ya `FIRMADA` o benchmark ya presente → PARA y reporta.

## F1 · Aterrizar el benchmark (commit propio)

Escribe `forense/benchmark-unidad-homogenea-codi-spei-v1_0.md` byte-idéntico al adjunto; verifica con `sha256sum` tras escribir. **Cero ediciones** (precedente `ADR-151`: adjunto de mesa se commitea verbatim).

## F2 · Propagar la firma (commit propio o mismo PR, orden F1→F2)

1. **ADR nuevo** en `gobernanza`: verbatim de mesa completo, qué sella (fila **A1** de la condición A de `R3.4` bajo la cláusula sustituida de §10.7), qué NO sella (R3.4 completo; Hito D `18 de 27` sin cambio; B/C base medida 0 de 2, `ASIGNADO`s), reservas que viajan (§10.6 completa + §2 antigüedad + B6 del benchmark), y el benchmark como insumo citado. Candidatea contra el máximo verificado con el grep de la casa.
2. **Ficha, §10.8 (enmienda fechada, append):** «Fila `A1` SELLADA por [ADR-N], firma de mesa verbatim […]. La cláusula de §10.7 queda adoptada. Reservas §10.6/§2 viajan con la firma. `R3.4` SIGUE SIN VEREDICTO: el gate exige A∧B∧C y B/C siguen con base medida 0 de 2.» Nada de §1–§10.7 se edita.
3. **Tablero:** `FP-104` → `FIRMADA`; `firmada_en` = fecha + verbatim + ADR; `ejecutada_en` = este acto (la pregunta reformulada por D3 — «¿queda sellada la condición A re-especificada?» — queda contestada por esta propagación).

## F3 · Sincronía y cierre

- **Set de sincronía:** cabecera de `gobernanza` (conteo ADR) · `estado-programa` cabecera/L0 + línea de suite (declarado = medido, cifra de la corrida real) + nota fechada breve en la línea que hoy narra `FP-104`/R3.4 si existe (derívalo con grep, no de memoria). **Hito D NO se mueve**: `README.md` fuera de perímetro, dilo en el ADR.
- **Suite antes y después:** `timeout 900 python3 tests/check.py --baseline` — 🚫 jamás `--freeze`. Reporta las cifras REALES (el neto esperado es −1 WARN por `FP-104` saliendo de `ABIERTA`, pero se reporta lo medido, no lo esperado). Toda tubería con `iconv -f utf-8 -t utf-8 -c`; todo negativo con conteo de archivos examinados (A.13).
- **Nota de cierre** con el detalle comando a comando; **este encargo archivado `CONSUMIDO`** con el PR.
- **CONTADOR: cero, declarado** — ningún contador de medición sobre México se mueve por este acto.

## Lo que este acto deliberadamente NO hace

No adjudica `R3.4` completo ni mueve Hito D. No toca `L14`/`FP-150` (firma aparte, acto aparte). No corre la sensibilidad P2 del benchmark (opcional, sin fila, hasta que mesa la pida). No toca `milpa/`, `data/`, `corpus/`, `tests/aceptacion_r3_4.py`, ni el perímetro de Codex. Si la suite rompe por algo que esta lista no cubre, PARA y reporta en vez de ajustar fuera de perímetro.

---

**ARCHIVADO CONSUMIDO** — ejecutado en `ACTO SELLA-A1-CODI`, 25/ago/2026, `ADR-177`. Ver `forense/notas/2026-08-25-sella-a1-codi-cierre.md`.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-25-SELLA-A1-CODI.md" canon/gobernanza-v1_15.md` cita ADR-177, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-177 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
