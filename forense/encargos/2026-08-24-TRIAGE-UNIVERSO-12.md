# ENCARGO · ACTO TRIAGE-UNIVERSO-12 — lo calculado se recalcula si se tiene que recalcular

| | |
|---|---|
| **Redactado por** | dirección, 24/ago/2026, contra clon propio `origin/main = fb02421` |
| **Firma de mesa que lo autoriza, verbatim (24/ago)** | «Lo calculado se recalcula si se tiene que recalcular recuerda que se calculó con solo el 0.9% del universo conocido abierto» — cópiala así al ADR. Ancla derivada: los cierres se sellaron cuando `ADR-67` medía **509 de 35,708 activos (1.43%)** y **0.52% de instrumentos**; hoy `data/manifiesto.yaml` trae **760 entradas** (grep de dirección, 24/ago). |
| **⛔ ORDEN** | Lanzar **tras fusionar `REPARA-PROPAGA-15`** (verifica en ARRANQUE 2). Puede correr **en paralelo con `RECENSO-DISEÑO-14` (UBUNTU)** — cajas distintas; colisión posible solo en gobernanza/tablero: quien fusiona segundo renumera. |
| **ENTORNO ASIGNADO** | **NUBE** (`cloud_default`). **NO UBUNTU** — clasifica rutas, no abre microdato. |
| **Modelo** | Opus |
| **Reglas fijas** | 🚫 `--freeze` · `pgrep -af claude` · `iconv -f utf-8 -t utf-8 -c` |
| **CONTADOR DECLARADO** | Directo: **Hito D 15→16 si la firma F1 viene adjunta** (Parte 0). Indirecto: produce la cola que moverá los demás — dicho a propósito (v2.3). |

**Encontrar que el terreno no es el que este encargo supone es entregable, no interrupción.**

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
1 · REPO. Clon existente; ruta · `git log -1 --format="%h %s"` · `git status`.
No arranques desde el home.
2 · SHA. La base debe INCLUIR `REPARA-PROPAGA-15` fusionado (su ADR debe
existir en gobernanza y la suite del árbol debe abrir VERDE — verifícalo).
Si no está: este acto se lanzó antes de tiempo, PARA y repórtalo.
Si main se movió más allá: refresca, re-deriva, reporta.
3 · data/raw. AUSENTE NO ES PARO; este acto no la abre. Repórtala igual.
4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado `cloud_default`.
Sin red ni microdato: dilo y salta la sonda.
⚠️ [v2.11] Un negativo de un comando que no examinó archivos no es un
negativo (A.13): todo veredicto negativo declara cuántos archivos examinó.
5 · ESPEJO. Ninguna cifra del espejo; todo del clon, comando a la vista.
════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (24/ago) ═══
1 · ESTRUCTURA. Gobiernan: `forense/hitoD-preregistro-v2_0.md` (fichas y
bloque append-only) · `data/manifiesto.yaml` (qué payload existe) ·
`data/censo-explotacion-2026-08-17.tsv` (627 filas) · `data/curacion-universo/`
· tablero · gobernanza. Sin hueco de índice para este dominio.
2 · CONTENIDO, derivado hoy por dirección:
- Las 12 faltantes del perímetro 27 (receta: encabezados `## R` del
  preregistro menos las 15 archivadas): **R1.4 · R2.1 · R2.2 · R3.4 ·
  R7.3 · R7.4 · R7.5 · R8.2 · R8.3 · R10.1 · R10.2 · R10.3**. Re-deriva
  la lista tú mismo antes de usarla.
- 8 de ellas están pre-registradas «probables D (inejecutables)»
  (`hitoD-preregistro:324-328`) por tres razones: dato organizacional
  propietario (R2.2/R8.2/R10.2) · hueco de dato ya declarado (R1.4/R8.3)
  · límite ético (R10.3). **Esos cierres son informacionales sellados bajo
  el ~1% del universo** — el blanco de este acto.
- Candidatas calientes vistas por dirección (verifícalas, no las heredes):
  **R1.4** — su hueco «panel D/E» puede haberse disuelto: ENNViH/MxFLS ya
  son payloads propios (194 menciones en manifiesto; `ennvih1_2002_hogar_dta`
  marcado `usado_para: CAL-G3`), y la ficha la pre-marca «posiblemente ya
  falsada por evidencia que el corpus contiene». **R8.3** — su condición A
  (falsador de transar-con-desconocidos por enforcement) se declaró
  inexistente el 5/ago (ADR-64(e)) bajo el universo viejo; WVS/ISSP entraron
  al manifiesto el 12/ago (premisa (3), del transfer — verifícala contra el
  yaml). Ojo con la marca **C3** de circularidad de ENCUCI en R8.3: sigue
  vigente, no la disuelvas por entusiasmo.
3 · COBERTURA RETROACTIVA. Los cierres a revisar (5/ago y antes) preceden
a manifiesto-expandido (12/ago+), censo-explotacion (17/ago) y ENOE (20/ago):
**su ausencia de ruta ahí no prueba nada — es exactamente la brecha A.8(3)
que este acto existe para cerrar.**
════════════════════════════════════════════════════════════════════

## PARTE 0 · Firmas adjuntas al lanzamiento (ejecuta verbatim; si no vienen, salta y dilo)

- **F1 (`FP-112`)** si mesa la adjunta: archiva `R7.3 → C` (append en preregistro citando `hitoD-R7_3-veredicto`), `FP-112 → FIRMADA` con verbatim, contador **15→16** derivado del oráculo, propagación completa (README + citas — que E-0 acaba de dejar en 15; muévelas a 16 en ESTE acto, están en tu perímetro).
- **F4 (`FP-113`)** si mesa adjunta el `.md` íntegro de coerción: commitéalo byte-idéntico a `forense/`, rotulado `PROPUESTA (no sellada)`, `FP-113 → FIRMADA`. Si no viene: no lo reconstruyas, la fila queda.

## PARTE 1 · El triaje, ficha por ficha (las 12)

Para cada regla faltante, en este orden y con esta salida:

1. **Localiza el cierre**: archivo:línea + fecha/SHA del acto que lo selló. Cita textual de la razón.
2. **Clasifica la razón**: `INFORMACIONAL` (NO-ENCONTRADO / hueco de dato / tier bajo por falta de información / «no hay fuente») · `ESTRUCTURAL` (propietario, ético, spec defectuosa, firma pendiente). Las tres redacciones del corolario retroactivo de A.6 cuentan como informacionales.
3. **Solo las INFORMACIONALES se re-buscan**, contra el universo de HOY: manifiesto (760), censo-explotacion (627), `curacion-universo/`, ENOE recién fusionado. Vocabulario A.4 obligatorio (`EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` / `NO-ENCONTRADO` con dónde y términos / `NO-ACCESIBLE`), conteo de archivos examinados en todo negativo (A.13). **`ENCONTRADO-POR-BÚSQUEDA ≠ VERIFICADO` (A.6): una ruta de payload en manifiesto es ruta, no dato abierto — este acto NO abre microdato; propone el acto UBUNTU que lo abra.**
4. **Si el cierre viejo quedó superado**: márcalo `VENCIDO EN ALCANCE` (A.10) con **enmienda in situ fechada** sobre el párrafo original — el original no se toca (precedente PROXY_PARCIAL, ADR-67(a)). Nada del bloque append-only se edita; ningún veredicto ya archivado se reabre (los 15/16 archivados no son objeto de este acto).
5. **Las ESTRUCTURALES no se fuerzan**: R10.3 (límite ético) **no se reabre** — un límite ético no es un hueco informacional. R3.4 se anota «ruta EMISOR-M-2 → re-spec condición A» sin correr nada. R10.1 se anota «espera spec sucesora (FP-108)». Propietarias: si la razón fue pago/afiliación, es `NO-ACCESIBLE` y se queda — pero deja la **receta manual de un minuto** (A.5) por si mesa quiere intentarla a mano.

**Salida principal**: `data/triaje-hitoD-2026-08-24.tsv` — columnas: `regla · cierre_original (archivo:línea, fecha, SHA) · clase · veredicto_hoy (A.4) · ruta_payload_si_existe · siguiente_acto_propuesto (entorno) · prioridad`. Más nota en `forense/notas/` con el razonamiento por ficha, y **filas de tablero** (A.12) para todo lo que exija firma de mesa antes de correr.

**Cierre a mesa**: un párrafo — cuántas de las 12 quedaron ejecutables hoy, cuántas vencidas en alcance, cuántas firmes con estampa, y cuál es la corrida #1 recomendada para mañana en UBUNTU.

## PERÍMETRO Y CONCURRENCIA

Archivos: `data/triaje-hitoD-2026-08-24.tsv` (nuevo) · `forense/notas/2026-08-24-triaje-universo-12.md` (nueva) · `forense/hitoD-preregistro-v2_0.md` (**solo** enmiendas in situ fechadas y, con F1, el append de R7.3) · `forense/firmas-pendientes.tsv` · `canon/estado-programa-v1_10.md` + `README.md` + `canon/modelo-decision-v4_0.md` (**solo** con F1, contador 15→16) · `canon/gobernanza-v1_15.md` (ADR) · `forense/` doc de coerción (**solo** con F4) · `forense/encargos/2026-08-24-TRIAGE-UNIVERSO-12.md` (este, `CONSUMIDO` al cerrar).

**Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.**

Concurrencia: `RECENSO-DISEÑO-14` puede estar corriendo en UBUNTU (archivos disjuntos salvo gobernanza/tablero — renumera quien fusiona segundo). `AMPLIA-MARCO-SATURA` espera a que ESTE fusione.

---

## CONSUMIDO — 24/ago/2026

Ejecutado como `ACTO TRIAGE-UNIVERSO-12`, commit `9151ac9` (rama `claude/universo-recalculo-triage-w93rj3`). Este archivo llegó como texto de conversación *después* del acto; se commitea ahora, retroactivamente, para cerrar el perímetro que lo declaraba `CONSUMIDO al cerrar`. Ver `forense/notas/2026-08-24-triaje-universo-12.md` para el cierre a mesa completo.

Verificación numérica contra el arranque real del acto: `194` menciones case-insensitive de `ennvih|mxfls` en `data/manifiesto.yaml` (confirmado, no `137` — ese número era solo el conteo de líneas con `ennvih` en minúscula estricta; `194` es el correcto reportado por dirección). `760` entradas de manifiesto confirmadas. `627` filas de censo-explotación confirmadas. `data/curacion-universo/` existe y no contiene ninguna de las 12 rutas de este triaje (36 archivos examinados, ninguno con nombre o contenido referente a las reglas del Hito D — son artefactos de `BARRIDO-2`, dominio distinto).
