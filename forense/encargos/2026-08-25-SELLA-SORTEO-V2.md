**SHA de redacción:** `c502a43` (`origin/main` al redactar, verificado por clon en la sesión de dirección del 25/ago/2026). `origin/main` avanzó a `769fa97` antes de que este acto arrancara (incluye el merge de `SELLA-A1-CODI`/`ADR-177`, `PR #350`) — no fue PARO, re-derivado en F0 contra el árbol real.

**Entorno asignado:** NUBE (`cloud_default`). No lanzado en Ubuntu, no lanzado en los dos entornos a la vez.

**Estado:** `CONSUMIDO` — ejecutado por `ACTO SELLA-SORTEO-V2` en esta misma rama (`claude/sella-sorteo-v2-firma-cn7hr9`), sella `FP-150` (`ADR-178`). PR de este acto.

---

## Texto del encargo (verbatim, tal como se lanzó)

Encargo `SELLA-SORTEO-V2` — propagar la firma de mesa sobre `FP-150` (sello del reglamento del sorteo de `ACT-PIL-3`, cifras post-`#345`)

SHA de redacción: `c502a43` (`origin/main` al redactar, verificado por clon en la sesión de dirección del 25/ago/2026). Si `main` se movió al arrancar: NO es PARO — refresca, re-deriva lo que dependa del perímetro y reporta la diferencia antes de editar. Redactado por: sesión de dirección (maestra), conversación del proyecto, 25/ago/2026. Mandato de mesa verbatim: «damelo» (sobre el ofrecimiento del encargo gemelo de `L14`).

ENTORNO ASIGNADO: NUBE (`cloud_default`). Este acto no toca microdato ni red de datos. NO lanzarlo en UBUNTU y no lanzarlo en los dos entornos a la vez. Puede correr en la misma sesión NUBE que `SELLA-A1-CODI`, en serie (uno cierra su PR, luego el otro); si corren en paralelo, aplica la regla de la casa: renumera quien fusiona segundo y re-mide sobre el árbol fusionado.

REQUERIDO en el mensaje de lanzamiento — sin esto, PARO en F0 sin tocar nada: la firma de mesa como línea propia (ranura en F0). Este encargo no lleva adjunto: el reglamento ya vive en el árbol y se verifica por sha256 (pin abajo).

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara (`c502a43`). Si `main` se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Este acto NO descarga nada.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado: `cloud_default`. Este acto no toca microdato ni red de datos: dilo y salta la sonda. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien ESCRIBE el encargo (dirección, 25/ago/2026, contra `c502a43`) ═══

1 · ESTRUCTURA. Tablas gobernantes: `forense/firmas-pendientes.tsv` (tablero, A.12) · `canon/gobernanza-v1_15.md` (ADR) · `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` (el reglamento que se sella; enmiendas fechadas por append) · `canon/estado-programa-v1_10.md` (sincronía). `data/INFRAESTRUCTURA-v1_0.md` gobierna `data/` — dominio no tocado. Este encargo ESCRIBE: las cuatro nombradas + nota de cierre + encargo archivado. Deliberadamente NO escribe: `forense/marco-candidatas-piloto-v1_0.tsv` (el sello no congela el marco — eso es del sucesor), `milpa/`, `README.md`/Hito D (sin movimiento), `FP-133` (FIRMADA, su ejecución no es de este acto).

2 · CONTENIDO. Comandos corridos por dirección, salida cruda:

* Tablero: `FP-150` estado = ABIERTA, `ejecutada_en` vacía. EXISTE-NO-SATISFACE — la fila existe, la firma no está dada.
* `grep -ci "SELLAD" forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` → 0 (1 archivo, 316 líneas). El reglamento no trae marca de sello.
* Barrido de firma: `grep` de verbatims de mesa sobre sorteo en `canon/gobernanza-v1_15.md` + las 12 notas del 25/ago (6,413 líneas) → cero firmas; `ADR-175` dice verbatim que `FP-150` «sigue ABIERTA … no se firma en este acto». NO-ENCONTRADO como sello previo.
* Cadena previa: `FP-145` FIRMADA + ejecutada (la redacción del reglamento ya corrió — no se re-redacta nada) · `FP-133` FIRMADA, ejecutada vacía (fuera de perímetro).
* Pin de integridad del reglamento: sha256 al redactar = `92c017765820585e7ab2471e187f4cb7221d35ba59e3c215bef1b076bc487a79` (316 líneas). Mesa firma estas reglas; el pin es lo que F0 verifica. El ejecutor RE-CORRE estos comandos en F0; si `FP-150` ya está `FIRMADA` o el reglamento ya trae sello, el trabajo está hecho: PARA y reporta (A.8).

3 · COBERTURA RETROACTIVA. Nacimientos por `git log --diff-filter=A`: tablero 2026-08-14 (`6e0f2a1`) · gobernanza 2026-07-30 (`8a341da`) · reglamento 2026-08-25 (`330af5b`). Todo lo tocado es posterior al nacimiento de sus tablas gobernantes — sin brecha.
════════════════════════════════════════════════════════════════════

PERÍMETRO Y CONCURRENCIA

Archivos que este acto toca, lista cerrada:

* `forense/firmas-pendientes.tsv` — solo la fila `FP-150`.
* `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` — solo APPEND de la sección de sello al final; §0–§7 no se editan hacia atrás y el archivo NO se renombra (las citas vivas de T02/T03 apuntan a este nombre).
* `canon/gobernanza-v1_15.md` — ADR nuevo + cabecera (conteo).
* `canon/estado-programa-v1_10.md` — recifrado estándar (cabecera/L0, línea de suite) + nota fechada breve SOLO en las líneas vivas que citen `FP-150` y cuyo estado cambie por este sello (derívalas por `grep`, no de memoria; «ACT-PIL-3 (sorteo) sigue sin correr» sigue siendo verdad y no se toca).
* `forense/notas/2026-08-25-sella-sorteo-v2-cierre.md` — NUEVA (sufijo `-cierre`, T02).
* `forense/encargos/2026-08-25-SELLA-SORTEO-V2.md` — este texto, archivado `CONSUMIDO` con su PR (A.3).

"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

Concurrencia conocida al redactar: `SELLA-A1-CODI` (mismo día, misma clase, filas distintas del tablero) puede estar lanzado — serie recomendada, paralelo tolerado con renumeración de la casa (grep corregido de `ADR-169` para el máximo de ADR). PR de Codex abierto — perímetro intocable (`tools/curador_registro/**`, `data/curacion-universo/**`, `generar_marco`). Ramas residuales sin fusionar, no se tocan. Mesa declara en el lanzamiento si lanzó algo más.

F0 · Compuertas — antes de escribir una sola línea

1. Firma. Busca en el mensaje de lanzamiento la cadena `FIRMO FP-150` como línea propia de mesa, fuera de la cita de esta compuerta (la autocaptura verbatim de una compuerta no es autorización — precedente `FP-63`/L5). Ausente → PARO sin tocar nada. Firma esperada (mesa puede adoptarla o dictar la suya; se propaga la que venga):
RANURA — FIRMA DE MESA: `FIRMO FP-150: sello sorteo-v2 sobre cifras post-#345 (33/60=55.0% · 27/50=54.0%).`
2. Integridad del reglamento. `sha256sum forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` == pin `92c01776…87a79`. Discordante → PARO y reporta: di qué cambió (`git log -- <archivo>` desde `c502a43`) antes de concluir nada (A.7) — mesa firmó el pin; si §2–§2.3/§3 cambiaron, la firma no se propaga sobre texto distinto.
3. A.8 en fresco. Re-corre los comandos del bloque de existencia. `FP-150` ya `FIRMADA` o sello ya presente → PARA y reporta.

F1 · Propagar la firma

1. ADR nuevo en `gobernanza`: verbatim de mesa completo; qué sella — el algoritmo determinista de `ACT-PIL-3` tal como está en el reglamento pinneado (cuota `floor(0.20·n_sorteo)` dura, infactibilidad verificada ANTES de sortear con fallback §2.3, protocolo de semilla §3 = SHA de merge del acto que congele marco+sorteo, determinismo, 3 casos de prueba), sobre las cifras vivas post-#345 (33/60 = 55.0 %, exceso +21 · 27/50 = 54.0 %, exceso +17; la discrepancia contra la nota de `#345` §5 ya quedó declarada por `ADR-175` y este ADR la cita, no la re-litiga); qué NO sella — no congela el marco, no corre el sorteo, no mueve Hito D. Candidatea contra el máximo verificado con el grep de la casa; renumera quien fusiona segundo.
2. Reglamento, sección nueva por append al final («## Sello de mesa — 25/ago/2026»): firma verbatim, ADR, pin sha256 verificado, y la línea: «El sorteo real corre en el acto sucesor de congelado; la semilla nace del SHA de merge de ESE acto, conforme a §3 — este sello no la fija.»
3. Tablero: `FP-150` → `FIRMADA`; `firmada_en` = fecha + verbatim + ADR; `ejecutada_en` = este acto (la pregunta de la fila — «mesa sella sorteo-v2» — queda contestada por esta propagación).

F2 · Sincronía y cierre

* Set de sincronía: cabecera de `gobernanza` · `estado-programa` cabecera/L0 + línea de suite (declarado = medido, cifra de la corrida real) + notas fechadas solo donde el `grep` de `FP-150` lo exija. Hito D NO se mueve; `README.md` fuera de perímetro — dilo en el ADR.
* Suite antes y después: `timeout 900 python3 tests/check.py --baseline` — 🚫 jamás `--freeze`. Neto esperado −1 WARN (`FP-150` sale de `ABIERTA`); se reporta lo medido, no lo esperado. Toda tubería con `iconv -f utf-8 -t utf-8 -c`; todo negativo con conteo de archivos examinados (A.13).
* Nota de cierre comando a comando; este encargo archivado `CONSUMIDO` con el PR.
* CONTADOR: cero, declarado.

Lo que este acto deliberadamente NO hace
No congela el marco y no corre el sorteo — sucesor declarado: acto `CONGELA-SORTEA` (dirección lo redacta en cuanto este sello fusione; ahí nace la semilla por §3 y se implementa el pseudocódigo contra los 3 casos de prueba antes del sorteo real). No toca `FP-133`, `forense/marco-candidatas-piloto-v1_0.tsv`, `milpa/`, `data/`, `corpus/`, `README.md`, ni el perímetro de Codex. No renombra el reglamento. No re-deriva el cuadro (ya lo hizo `ADR-175`; se cita). Si la suite rompe por algo fuera de esta lista, PARA y reporta en vez de ajustar fuera de perímetro.

FIRMO FP-150: sello sorteo-v2 sobre cifras post-#345 (33/60=55.0% · 27/50=54.0%).

## CONSUMIDO

Derivación mecánica (`/tramite`, §3.3): único `Merge pull request #N` cuyo mensaje cita el rótulo `SELLA-SORTEO-V2` — `PR #351` (`b767ea6`), y ese merge toca este archivo además de otros 6 (`git diff --stat b767ea6^1 b767ea6`).
