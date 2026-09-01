# ACTO MAESTRA33-C7 · APERTURA-VERIFICA — cierre

**Encargo:** `forense/encargos/2026-09-01-MAESTRA33-C7-APERTURA-ENFIH-ENSAFI-V1_1.md` (mesa, 1/sep/2026, formato corto, `SHA de redacción c7fa424`, `COMPUERTA: ninguna`, declarada). Ejecutado con la skill `/acto` de `ADR-237`.

**ARRANQUE.** Repo: `/home/pc0/mm-apertura-verifica` (worktree nuevo, `git worktree add -b acto/maestra33-c7-apertura-verifica`), sobre `origin/main` real. `SHA`: el encargo declara `c7fa424`; `origin/main` había avanzado a `02ec20b` (un merge más, `PR #429`, `MAESTRA33-E10 · PROCEDIMIENTO-SCORING-v1_1-PROPUESTA`) — verificado que ese merge **no toca** el perímetro de este acto (`git diff --stat c7fa424 origin/main` sobre `canon/gobernanza-v1_15.md`/`canon/estado-programa-v1_10.md` únicamente: conteo de ADR 256→257, sin tocar `FP-179`, `coef-universo`, `APERTURA-FASE-CALCULO`, ni ningún archivo de `apertura-enfih-ensafi`). No es PARO — refrescado, perímetro re-derivado contra `origin/main = 02ec20b`. `data/raw`: ausente en el worktree nuevo (esperado), enlazado a `/home/pc0/mm-corpus/raw` (321 entradas). Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`; sonda `curl` a `www.inegi.org.mx` → `200` — consistente con `ENTORNO: CAJA` declarado por el encargo. Este acto no abre microdato ni descarga nada (lectura de canon únicamente).

---

## P1 · Tabla "§3 exige → ADR-134 cubrió → delta"

**Primero, el rótulo.** A.8 declaró `Encabezado "S3": NO-ENCONTRADO por grep (1 archivo)`. Verificado de nuevo por este acto: `grep -n "S3\|## S\|§S" canon/APERTURA-FASE-CALCULO-v1_2.md` → **0 coincidencias**, 1 archivo examinado (A.13). Se deriva leyendo, tal como A.8 instruye: el documento sí trae `## §3 · ENCARGO embebido · APERTURA-ENFIH-ENSAFI` (línea 32 de `canon/APERTURA-FASE-CALCULO-v1_2.md`). "S3" de `FP-179(5)` = `§3`. Confirmado también contra el propio encargo original archivado (`forense/encargos/2026-08-20-APERTURA-ENFIH-ENSAFI.md`), que cita literalmente `"Ley de fondo: APERTURA v1.2 §3, verbatim"`.

**§3 completo, leído íntegro** (`canon/APERTURA-FASE-CALCULO-v1_2.md:32-38`) contra **ADR-134 completo** (`canon/gobernanza-v1_15.md:2679`):

| §3 exige | ADR-134 cubrió | Delta (A.4) |
|---|---|---|
| **Ley de fondo** — celdas objetivo re-derivadas de `coef-universo-v1_0.tsv`, filas ENFIH/ENSAFI (el texto de §3 aún nombra el paso intermedio "censo de β") | ADR-134 deriva **directo** de `coef-universo-v1_0.tsv` ("no del censo β, superado"): `N3`/`N4`/`N11`/`N15`, las cuatro `SIN-RUTA` reales tras excluir `N6` (`SIN-DEMANDA`, `ADR-121`) y `N10` (ganó ruta desde el censo v1.2). El propio ADR declara que la premisa de "ley de fondo" del encargo, no sostenida al arrancar, "resulta sostenida por una fusión concurrente detectada al cerrar" — y el encargo original archivado (`2026-08-20-APERTURA-ENFIH-ENSAFI.md`) ya traía la misma corrección escrita antes de T1 ("de ahí salen las celdas objetivo, no del censo β del plan viejo, que quedó superado") | **∅** — mismas cuatro celdas objetivo bajo cualquiera de las dos rutas de derivación; discrepancia administrativa, declarada por el propio acto y reconciliada, no de contenido |
| **T1** — abrir ENFIH 2019 y ENSAFI 2023 a nivel variable, términos pre-registrados en COMMIT A antes de abrir archivo, `command grep` con conteo, codebooks antes de microdato | ADR-134: "las busca en ENSAFI 2023/ENFIH 2019 con protocolo pre-registrado". Verificado contra el artefacto (`data/apertura-enfih-ensafi-v1_0.tsv`, ver abajo): cada una de las 8 filas cita el barrido completo por variable (369 encabezados ENSAFI vía `zipfile+csv`; 780 variables ENFIH vía `openpyxl`) y "declarado en COMMIT A antes de abrir" | **∅** |
| **T2** — tabla con `variable_id`, universo del instrumento, escala declarada, veredicto A.4, por celda objetivo | `data/apertura-enfih-ensafi-v1_0.tsv` **EXISTE** (confirmado, A.8), 8 filas = 4 necesidades × 2 instrumentos, columnas `variable_encontrada`/`universo_declarado`/`escala`/`clasificacion_a4` presentes en las 8 | **∅** |
| **T3** (condicional) — si aparece reactivo que reabre `ADR-52A`/`54`, NO reabrir, escribir propuesta acotada | Condición **nunca se disparó**: 0 `EXISTE-SATISFACE`, 2 `EXISTE-NO-SATISFACE` ya conocidos (sin reactivo nuevo), 6 `NO-ENCONTRADO`. Declarado explícitamente en el artefacto mismo, fila `N4`/ENFIH: *"T3 del encargo no se dispara porque no hay reactivo nuevo"* | **∅** — condición no aplicable, declarado en la fuente primaria, no inferido |
| **T4** — cerrar: cuántas `SIN-RUTA` ganaron ruta (número dicho), fichas B-bis para lo medible ya, ADR, fila(s), nota | ADR-134: *"ninguna SIN-RUTA gana ruta"* — número dicho = **0**. Fichas B-bis: no aplica (0 `EXISTE-SATISFACE`, nada medible que fichar). ADR = `ADR-134`. Nota: `forense/notas/2026-08-20-apertura-enfih-ensafi-cierre.md` | **∅** |

**Verificación independiente contra el artefacto primario** (no solo la prosa del ADR): `data/apertura-enfih-ensafi-v1_0.tsv` tiene exactamente 8 filas de datos. Conteo por `clasificacion_a4`: `NO-ENCONTRADO` ×6, `EXISTE-NO-SATISFACE` ×2, `EXISTE-SATISFACE` ×0 — **coincide exacto** con "0 de 8 celdas en EXISTE-SATISFACE (dos EXISTE-NO-SATISFACE reconfirmados sin novedad, seis NO-ENCONTRADO)" de `ADR-134`. `N15/G6.deferencia` en ambos instrumentos declara *"Primera vez que deferencia se busca en ENSAFI/ENFIH"* — coincide con "deferencia buscada por primera vez en ambos instrumentos".

**Veredicto: delta = ∅.** `ADR-134`, por sí solo, cubre íntegro lo que `§3` exige. `FP-179(5)` cierra como **`EJECUTADA-EN-ADR-134`**.

### Sobre la cita "`(+ADR-194/198)`" de la enmienda del 30/ago

La fila `FP-179` ya trae una enmienda (30/ago/2026, `ACTO MAESTRA32-E9 · PROPAGA-2`, F6) que marcó `(5) → CONSUMIDA-PREEXISTENTE: ejecutada por ADR-134 (+ADR-194/198)`. Verificados los dos ADR adicionales (`canon/gobernanza-v1_15.md:3649` y `:3681`): `ADR-194` (`ACTO R34-ENSAFI-CENSA`) y `ADR-198` (`ACTO ENSAFI-DESCRIPTOR`) censan `ENSAFI 2023` a nivel reactivo contra los constructos **B/C de `R3.4`** ("regla dinero") y resuelven el acceso al descriptor/cuestionario para esa regla — **`FP-157`, un rótulo distinto**, no `FP-179`. Ninguno de los dos re-examina `N3`/`N4`/`N11`/`N15` ni cambia ningún veredicto de `data/apertura-enfih-ensafi-v1_0.tsv`. Con vocabulario A.4: la cita de `ADR-194`/`ADR-198` en la enmienda del 30/ago es **contexto** (tranquiliza que ningún otro hilo de ENFIH/ENSAFI quede huérfano al cerrar), **no cobertura** de `§3` — `§3`/`ADR-134` no los necesita para cerrar, y este acto cierra citando `ADR-134` en solitario, tal como `P1` de su encargo pide.

---

## P2 — no aplica

Delta = ∅. Por instrucción explícita de `P1` del encargo ("Si delta = ∅: ...PARA — ese cierre es el entregable"), este acto no ejecuta `P2`. No toca `data/`, no toca `milpa/tramite-ola5-propuesta-v0.yaml`, no carga al motor, no abre dominio — tal como `LO QUE NO HACE` del encargo exige.

---

## P3 · Cierre de FP-179(5) y nota sobre (3)/(4)

`FP-179(5)` cerrada en `forense/firmas-pendientes.tsv` con una nueva `ENMIENDA FECHADA` (1/sep/2026, este acto), append-only, sin tocar ninguna palabra de las enmiendas anteriores.

**Sobre "deja (3) y (4) intactas con sus fechas (C8 lun 7/sep, C9 mar 8/sep)":** ninguna entrada de `FP-179` se toca en este acto salvo `(5)` — cumplido por construcción. Verificado además, para que "quede claro y estipulado cuáles quedan pendientes" (firma de mesa verbatim que abre el encargo de este acto): releída la fila completa de `FP-179`,

- **`(3)`** (mediciones diferidas de `FP-172`) — **sigue ABIERTA**, sin enmienda que la cierre. Consistente con programarla como `C8`, lunes 7/sep.
- **`(4)`** (re-estimación compuesta de los 2 pares multi-item) — **ya tiene una `ENMIENDA FECHADA` previa que la marca `→ CONSUMIDA`** (30/ago/2026, `ACTO MAESTRA32-E8 · MEDICION-COMPUESTA`, β̂ compuesto de `G1.radio_confianza`/`G4.confianza_institucional`, escrito a `milpa/procedencia.yaml::coeficientes_generador_sellados`, ver `forense/notas/2026-08-30-compuesta-cierre.md`). Si `C9` (martes 8/sep) suponía trabajo pendiente sobre `(4)`, esa entrada **ya no lo tiene** — está cerrada desde tres días antes de que `FP-179` existiera como fila (`creado` = 30/ago) con el mismo sello de fecha.

Este acto **no reclasifica `(4)`** — `P3` pide dejarla intacta y así se hace; se declara la discrepancia para que mesa/dirección decidan si `C9` se redirige a otro objeto o se retira. No se resuelve aquí: es exactamente el tipo de decisión que corresponde a mesa, no al ejecutor.

---

## CONTADOR

**0** — delta = ∅, dicho, tal como el encargo instruye para ese caso. Ninguna cifra de θ ni candidata de regla dinero se produce (no hubo delta que forzara `P2`).

## Lo que este acto NO hace

No repite ninguna búsqueda que `ADR-134` ya corrió (no reabre `data/raw`, no re-busca en ENSAFI/ENFIH). No carga al motor. No abre dominio nuevo. No reclasifica `FP-179(3)` ni `FP-179(4)` — solo cierra `(5)` y declara la discrepancia de fecha sobre `(4)`.

---

## Sincronización post-cierre (1/sep/2026)

Tras abrir `PR #431` y reportar el cierre, `origin/main` avanzó un merge más: `PR #432`, `ACTO MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS`. `git fetch origin main` lo reveló al intentar sincronizar antes de un segundo push.

**Colisión de ADR.** `MAESTRA33-E11` fusionó primero y tomó `ADR-258` (el candidato que este acto también había derivado). Regla de la casa: renumera quien fusiona segundo. Este acto pasa a **`ADR-259`**, contiguo, sin hueco — verificado de nuevo por comando (`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | ... | tail -1` → `258` sobre `origin/main` ya fusionado).

**`MAESTRA33-E11` es la misma firma 6, disparada dos veces sin coordinarse.** Su propio texto (`canon/gobernanza-v1_15.md` `ADR-258`, `forense/notas/2026-09-01-criterios-y-vencimientos-cierre.md`) trae, entre otras siete firmas propagadas: "`FP-179(5)` verificada contra `ADR-134` (`canon/gobernanza-v1_15.md`): **CONFIRMA**" — **mismo veredicto que este acto**, alcanzado de forma independiente, sin que ninguno de los dos actos supiera del otro mientras corría. Dos verificaciones distintas del mismo hecho, mismo resultado — la clase de redundancia que este proyecto trata como corroboración, no como desperdicio.

**`MAESTRA33-E11` ya formalizó la discrepancia de `(4)` que este acto solo declaraba.** Abrió `FP-217` (`C8`, deriva de `FP-179(3)`, vence `2026-09-07`) y `FP-218` (`C9`, deriva de `FP-179(4)`, "declara la tensión con la `CONSUMIDA` ya anotada arriba en vez de resolverla en silencio", vence `2026-09-08`) — exactamente la nota que este acto dejó en su primer cierre, ahora con fila propia del tablero y fecha de vencimiento en vez de un párrafo suelto. Este acto no añade nada nuevo aquí: cede a `FP-217`/`FP-218` como el lugar donde mesa decide.

**Resolución del `git merge origin/main`.** Conflicto en cuatro sitios — `canon/gobernanza-v1_15.md` (auto-merge limpio, sin marcador, porque las dos entradas nuevas caían en regiones no solapadas del archivo), `canon/estado-programa-v1_10.md` (conflicto real: ambos actos tocaron la tabla de artefactos y la línea `L0`), `canon/registro-rotulos.tsv` (conflicto real: ambos actos añadieron una fila al final del archivo), y `forense/firmas-pendientes.tsv` (conflicto real: ambos actos amendaron el mismo campo de la misma fila `FP-179`, en el mismo punto de anclaje textual). Resuelto a mano, conservando las dos inserciones — la de `MAESTRA33-E11` primero (fusionó primero), la de este acto después — nunca sobrescribiendo ni acortando el texto ajeno. Verificado por conteo, no a ojo: columnas por fila (`awk -F'\t' '{print NF}' | sort -u` → un solo valor uniforme en las dos `.tsv`), anotaciones de la línea `L0` (`grep -o` del patrón `*(\`ADR-N\`` → exactamente una nueva, `ADR-259`, sin duplicar `ADR-258`), y una corrección de un defecto propio de reconstrucción: un primer intento de fusión programática del campo `FP-179` dejó un salto de línea suelto dentro del campo (partió la fila en dos líneas físicas del `.tsv`) — detectado porque el conteo de columnas dejó de ser uniforme en todo el archivo, corregido re-uniendo las dos líneas antes de seguir.

`python3 tests/check.py --baseline` re-corrido después de la fusión y de las correcciones: **VERDE**, sin `FAIL` nuevo.
