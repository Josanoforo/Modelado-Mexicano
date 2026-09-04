# ENCARGO ACTO MOTOR-1 CONSOLIDADO — cabecera de archivo (A.3)

**Archivado por A.3** (`instrucciones-proyecto-v2_5.md` Bloque D-bis) al ejecutar el acto **MOTOR-1**, 14/ago/2026.

## Dónde está el texto del encargo, y por qué no se copia aquí

El cuerpo autocontenido de MOTOR-1 es el **§3 de `forense/encargos/2026-08-13-PROC-10-BIS-clase-septima-y-anexos.md`**, líneas **61-79**, archivado verbatim por el acto PROC-10-bis (PR #227). Ese §3 se declara a sí mismo el encargo completo: *"Este §3 ES el encargo completo de MOTOR-1 — sustituye a «cuerpo original + deltas»"*.

**Desvío de A.3, declarado con su razón — no se re-copia el verbatim.** La convención pide el texto completo en `forense/encargos/`. Ese texto **ya está** en `forense/encargos/`, verbatim, desde el 13/ago. Copiarlo por segunda vez en el mismo directorio no añade una sola palabra de información y sí tiene un costo medido: el §3 cita por nombre cinco archivos que no existen en el árbol (compass-1-7edaceda · compass-2-8b198c56 · compass-3-d72e6a97 · red-team-A_auditoria-adversarial · red_team_A_auditoria, todos `.md` — se nombran aquí sin comillas invertidas a propósito, para no reproducir la cita colgante que se está describiendo) y T03 los marca uno por uno. `tests/baseline.json` ya congela esas seis entradas **contra la ruta del archivo de PROC-10-bis**; un segundo archivo con el mismo texto produce seis entradas nuevas y deja la suite en `LÍNEA BASE: ROJO` por una copia. Se archiva la cabecera con el puntero exacto (archivo + rango de líneas, en el mismo repo, no en una conversación) en lugar de la copia. El propósito de A.3 —que el encargo sea visible para el programa y auditable después— queda cumplido; la letra de "texto completo aquí" no, y se dice.

## Cabecera obligatoria (`forense/encargos/convencion.md`)

- **SHA de redacción.** El §3 se escribió contra `origin/main` = `560d305` (merge PR #224), declarado en la cabecera de PROC-10-bis. El `origin/main` **real** al arrancar MOTOR-1 es **`84b2acf`** (`Merge pull request #228 from Josanoforo/triage-63-sondeo`) — cuatro merges más allá (#225 ADJ-4, #226 R2, #227 PROC-10-bis, #228 TRIAGE-63). Los tres gates del commit 2 se re-verificaron por comando contra ese árbol real (abajo) y los tres dan verde; ninguna de las cuatro fusiones toca el perímetro de escritura de este acto (`forense/` únicamente). Declarada, no silenciada. **Y volvió a moverse durante la ejecución**, entre el COMMIT 2 y el COMMIT 3: `84b2acf` → **`d653ab9`** (#229 `SELLA-FREEZE`, #230 `S4-AMANUENSE-MESA`, con ADR-81/82/83). Se hizo `git merge origin/main` y se re-derivó todo lo dependiente de `canon/`; y una tercera al resolver el merge del PR (`d653ab9` → `f988b54`, #231 `SANEA-MAPEO`, que no toca `canon/`, `milpa/`, `README.md` ni `tests/`: todo re-verificado, nada cambia). El acto cierra sobre **`f988b54`**. Cambian dos cifras y tres anclas, ninguna conclusión — detalle en `forense/CASCADA-M1-2026-08-14.md` §5.
- **Entorno asignado.** **Nube** (`cloud_default`), repo-only, SIN red. **NO** es la sesión de RONDA-M — el encargo v2 §5 exige que RONDA-M corra en sesión NUEVA de Opus, explícitamente no la de MOTOR-1, no linaje Fable. Esta sesión no ejecuta RONDA-M ni parte de él.
- **Estado.** **`CONSUMIDO` PARCIAL.** Ejecutado 14/ago/2026 en `cloud_default`, rama `claude/motor-1-acto-ejecucion-1xn00f`, tres commits. Nota: `forense/notas/2026-08-14-motor-1.md`.
  - **COMMIT 1 — ejecutado, con un punto PARADO.** Los incisos 1 (cifras del dossier), 3 (E5/ADR-57(c)) y 4 (rúbrica Ronda) corrieron completos. El inciso **2 (commitear los cinco archivos verbatim) NO corrió: los cinco archivos no llegaron a esta sesión** — tercera sesión consecutiva. Ver abajo.
  - **COMMIT 2 — ejecutado.** `forense/CASCADA-M1-2026-08-14.md`, con los tres predicados corregidos verificados verdes.
  - **COMMIT 3 — ejecutado.** Paquete a mesa en la nota, §7.
- **Bloque VERIFICACIÓN DE EXISTENCIA (A.8), contestado** contra el árbol real (`84b2acf`, antes de escribir nada):
  ```
  $ find . -iname "*compass*" -not -path "./.git/*" | wc -l
  0                     # esperado 0 -- y sigue siendo 0 DESPUÉS de que el lanzador
                        #   declaró subirlos: no llegaron. Ver "El PARA" abajo.
  $ ls forense/ | grep -c "RONDA-M\|CASCADA-M1"
  0                     # nada de RONDA-M ni de MOTOR-1 corrió antes
  $ ls forense/red-team-A_auditoria-adversarial.md forense/red_team_A_auditoria.md 2>/dev/null | wc -l
  0                     # esperado
  --- gates del COMMIT 2 (predicados CORREGIDOS, no el `grep -c obligacion` roto) ---
  $ grep -c "norma_de_género" canon/modelo-decision-v4_0.md
  12                    # ≥1 -> #224 fusionado
  $ ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml
  (existe)              # #224 fusionado
  $ grep -cE "MEDIDO·NACIONAL" milpa/procedencia.yaml
  5                     # ≥1 -> PROC-10-bis (#227) fusionado; la cascada se deriva
                        #   sobre la taxonomía FINAL
  --- estado de RONDA-M, por comando, al cerrar ---
  $ ls forense/ | grep -c "RONDA-M"
  0
  $ git branch -r
  origin/main · origin/claude/motor-1-acto-ejecucion-1xn00f ·
  origin/claude/sanea-mapeo-encargo-lw5hhr   (ninguna de RONDA-M)
  $ gh pr list --state open        # vía MCP: list_pull_requests state=open
  []                    # cero PR abiertos
                        # => RONDA-M: NO LANZADO. No EN-VUELO: sin artefacto,
                        #    sin rama y sin PR. MOTOR-2 no se firma sin él.
  ```

## El PARA, acotado — y por qué es acotado y no total

El §3 fija: *"El lanzador sube a la sesión CINCO archivos, verificables por hash ANTES de cualquier commit (discordante ⇒ PARA)"*. **Los cinco no llegaron.** Verificado por `find / -iname "*compass*"` sobre el contenedor entero (no solo el clon), más `/mnt/attach` y `/mnt/user-data/working` vacíos. Es la **tercera** sesión consecutiva en que el lanzador declara subirlos y no llegan (#224 A.3, #227 §3, y ésta).

Los dos actos anteriores leyeron esa cláusula como PARA total y no commitearon nada de MOTOR-1. Este acto la lee **acotada al inciso que la regla protege**, y dice por qué:

- Lo que la regla protege es que **no entre al repo contenido no verificado**. Ese riesgo vive entero en el inciso 2 del COMMIT 1 ("commitea los cinco archivos verbatim"). Ese inciso **no se ejecuta**: cero bytes de los cinco archivos entran al árbol en este acto, que es exactamente el desenlace que la regla busca.
- Los incisos 1, 3 y 4 del COMMIT 1, el COMMIT 2 entero y el COMMIT 3 entero se derivan **del repo**, no de los cinco archivos. Ninguna línea que este acto escribe cita el contenido de un compass o de un red team; donde el encargo los nombra, se nombran como **ausentes**.
- El costo de la lectura total, medido: dos actos, cero entregables, y una cascada que MOTOR-2 necesita y sigue sin existir. Un tercer PARA idéntico no protege nada más de lo que ya protege no commitear los archivos.

**Lo que queda abierto por esto, sin maquillaje:** la cadena A.3 de CAREO **NO** queda cerrada. El §6 del encargo v2 lista como precondición de MOTOR-2 *"compass ×3 + RT-B/RT-D en repo (cadena A.3 cerrada…)"*. Esa precondición **sigue incumplida**. Si el ADR del sello cita CAREO, **sigue citando ausentes**. MOTOR-2 no puede firmarse hasta que una sesión reciba los cinco archivos y los commitee con hash verificado; ese acto es un commit de un solo paso y no depende de nada de este.

## Advertencias de dirección levantadas por este acto

1. **El predicado del hallazgo de E5 se auto-contamina, igual que el `grep -c obligacion` de PROC-11 §6.1.** El §3 manda verificar que el encargo de E5 no está archivado con `grep -rln "Entrada 5" forense/encargos/ → vacío`. Hoy **da 2**, y los dos hits son los encargos de MOTOR-COND-v2 y de PROC-10-bis *mencionando* E5 — no el encargo de E5. El hallazgo sustantivo se sostiene (E5 no está archivado); el comando que lo probaba dejó de probarlo en el momento en que el propio encargo se archivó. Predicado discriminante propuesto: `ls forense/encargos/*E5* forense/encargos/*entrada-5* 2>/dev/null | wc -l` → `0`. Ver nota §4.2.
2. **Tres anclas archivo:línea del §3 habían derivado.** `modelo:628` (22 g.l.) → **`:640`** (y `:262` para el mismo par); `estado:97` / `modelo:17` (titular `4 de 144`) → el titular ya **no vive en `estado-programa`**, vive en `modelo:638` y `README:39`; `procedencia.yaml:625-636` (la matriz B que `motor-matriz §1.4` transcribe) → **`:709`**. Re-derivadas todas en `forense/CASCADA-M1-2026-08-14.md`; ninguna cambia una conclusión, todas cambian la cita.
3. **La cifra "0 llaves ejercidas" que `motor-matriz §4.3` usa está vencida.** Hoy es **`1` de `2`** (`estado-programa-v1_10.md:99`, `forense/registro-llaves-identificacion-v1_0.md`, movida por ACTO ADJ-4: `R5.1-D2` firma `EJERCIDA_INDECISA`). Es material para el inciso (7) de MOTOR-2 y para el universo de E5: la propuesta que M1 adoptaría afirma "hoy hay cero" en el párrafo mismo donde razona sobre la compuerta de ADR-57(c). Ver nota §4.1.
4. **La suite base que el encargo v2 declara está vencida por partida doble.** El encargo cita `3d0d1e5, 20 FAIL · 107 WARN`; `gobernanza:856` declara `18 FAIL · 107 WARN`; la corrida real al cerrar da **`20 FAIL · 119 WARN`, LÍNEA BASE VERDE** contra `tests/baseline.json` (HEAD congelado `0ad9b7b`) — eran `24 FAIL` antes del merge de `d653ab9`; ADR-81 saldó cuatro. La discrepancia `gobernanza:856` ↔ corrida real ya es un `T16` vigente y baselineado, no un defecto nuevo de este acto; se declara porque **RONDA-M §5(a) manda citar la base al juzgar** y citaría una cifra muerta.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-14-MOTOR-1-consolidado.md" canon/gobernanza-v1_15.md` cita ADR-101, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-101 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
