# Nota de cierre · ACTO GEN2-TUBERIA-3 · 28/sep/2026 · NUBE

ADR-260928-GEN2-TUBERIA-3-f18c-01 (raíz `f18c`, 0-bis `f18cf407`). SHA de redacción del encargo `98f80cc7` = `origin/main` al abrir (base al día, 0 commits detrás; el hook de arranque decía «detrás=699» por clon superficial). Árbol limpio, sin duplicado de rótulo (rama remota, worktrees: 1, PR abiertos: solo el `[deriva]` #1290). ENTORNO-DERIVADO = NUBE, sonda de red DENEGADA-POR-POLITICA, corpus no montado (archivos examinados: 0): acto sin microdato.

## Contadores
Cero mediciones; no adopta. Ningún contador se movió por código de este acto: la lectura de `status` cambia solo `N_corridas_requeridas` y `N_resultados_pendientes` (P3, por dictamen citado); `dependencias_numericas_legacy_activas` no cambia por código (P2).

## P2 · Legacy: el «defecto de conteo» es vista atrasada, no código de conteo
[EJECUTADO] `python3 tools/corrida0.py status`, HEAD `98f80cc7`, dos estados del MISMO commit:

| estado de `data/corrida0/demanda-*.tsv` | N_resultados_activos | legacy_activas | adoptados_activos |
|---|---|---|---|
| comprometido en main (última escritura: PR #1186, 26/sep) | 211 | **67** | 128 |
| re-derivado con `corrida0 demanda` (sin commitear, revertido) | 236 | **82** | 138 |

Antes/después crudo: 67 → 82 sin cambiar código ni definición de legacy. Las dos filas son reproducibles; el «82» de dirección venía de vistas de demanda al día y el «67» del dictamen P8 (`nota-2026-09-28-gen2-tuberia-y-curacion-1.md`) de las vistas comprometidas. **Causa:** `demanda-corridas.tsv` y `demanda-resultados.tsv` no están en la lista de publicación del job `derivados` (`grep -c "demanda-" .github/workflows/verify.yml` → 0 líneas de publicación) y solo las escribe `corrida0 demanda`. No hay defecto en el código de conteo que corregir; **el dictamen DEFECTO-DE-CONTEO de P8 queda matizado** (no reescrito: es de dirección/mesa): el defecto es de publicación. No se publica `dependencias_numericas_legacy_definicion_desde` (la definición no cambió). Test que fija el conteo sobre caso conocido: `tests/test_tuberia3.py::test_p3_status_lee_el_dictamen_y_legacy_no_se_mueve` (3 dependencias legacy antes y después del dictamen).

## P3 · `status` lee el dictamen
`tools/corrida0.py::_reduccion_por_dictamen` es la única fuente de la reducción; la usan `cmd_demanda` y `status` (refactor sin cambio de salida de `demanda`: mismos 0 / 63 / cerrados 173 antes y después). Ningún total tecleado. Tablero y README derivan de `status()` y por eso leen lo mismo (sin edición).

[EJECUTADO] Con vistas de demanda al día: `demanda` → requeridas **0** (105 no requeridas), pendientes **63**; `status` → requeridas **0**, pendientes **63**. COINCIDEN. Sobre el árbol comprometido, `status` da 0 / **158** (vista atrasada de 211 activos) contra 63 de `demanda`: el criterio «coinciden» se cumple solo cuando la vista de demanda se publica (ver P2 y FP).

## P4 · El `[deriva]` no se queda en cola por lentitud: el auto-merge no se dispara
[EJECUTADO] PR #1290 (`derivados/auto-36471922339`), 105 CALC en trozos de 20 (cada trozo: verificación por `workflow_dispatch` de ~5-6 min). Runs `verify` de dispatch sobre los trozos 1 y 2 (36472806458, 36473592636): `success`. `automerge-rutinas.yml` corre por `workflow_run` de «Verificación del corpus»; consulta por rama `derivados/auto-36471922339`: `total_count = 0` runs de auto-merge, tras dos verificaciones exitosas. Los únicos runs recientes de auto-merge son sobre `main`. El PR queda abierto hasta que mesa fusiona a mano. No se pudo comprobar en esta sesión que un `[deriva]` fusione en < 1 h: no hay ninguno fusionado por el canal desde el 23/sep (la guardia de CALC bloqueaba la clase, corregida el 28/sep en el yml).
No se editó ningún archivo del canal (cambiar quién dispara el merge es regla del auto-merge). Opciones y recomendación: FP-260928-GEN2-TUBERIA-3-f18c-01.

## P1 · Canal en disco
`tools/deriva_cron.sh`: worktree en `$DERIVA_WORKTREES_DIR` (defecto `$HOME/worktrees`), temporales en `$DERIVA_TMPDIR` (`$HOME/deriva-tmp`), `git worktree prune` al abrir (`prepara_worktree_aislado`) y al cerrar (`retira_worktree`), y worktree borrado siempre; si hubo PARO, `status`, parche y no versionados van antes a `forense/deriva-log/estado/evidencia-<RUN_ID>/` (la compuerta «nada en /tmp» protege borrar: no se pierde el trabajo del caso de 1.1 GB). `grep -c "/tmp" tools/deriva_cron.sh` → 0. Test huérfano `tests/test_tuberia3.py` (2 pruebas de P1: sin `/tmp`; huérfano prunable + worktree con trabajo → borrado, evidencia guardada, `git worktree list` = 1). Manual: sección en `MANUAL-canal-deploy-key-2026-09-23.md` y `docs/sesiones.md` §4.
Premisa caída: `MANUAL-sesiones-que-se-cierran` figura [EXISTE] en el encargo y no está en el clon (`find . -name "MANUAL-sesiones*"` → 0); las líneas de TMPDIR y prune van a `docs/sesiones.md`. No se ejecutó el derivador real (necesita corpus de caja): el comportamiento se probó con las funciones extraídas del script, sobre un repo temporal.

Incidente declarado: al redactar el cierre, un heredoc de shell sin comillas ejecutó por sustitución de comandos `tools/deriva_cron.sh` (código de P1) una vez, a las 19:55 UTC. Terminó en `PARO-CORPUS` (data/raw ausente) antes de crear worktree: efectos = un `git fetch origin main`, log/heartbeat en `forense/deriva-log/` (gitignorado) y los directorios vacíos `$HOME/worktrees` y `$HOME/deriva-tmp`; cero push, cero commit, cero worktree. Los archivos de gobierno que ese heredoc alcanzó a escribir con texto corrupto se revirtieron con `git checkout` (estaban limpios) y se reescribieron desde un script de Python; el `deriva_cron.lock` vacío que dejó (T02 lo marcaba idéntico a un `__init__.py`) se borró. Sirvió de prueba de humo: el camino de salida temprana (cierre sin worktree) corre sin error.

## P5 · Plantilla RECIBO-ASTRA6-N v2
`forense/encargos/2026-09-28-GEN2-RECIBO-ASTRA6-N-v2.md` (+ `.cuerpo.sha256`): criterio común K7 (lista de lecturas con comando; archivo > 200 líneas íntegro con razón; sin lista → FUSIONAR-CON-NC). El «9 de 13 PR con NC» es [REPORTADO] por el encargo; no se re-midió.

## Verificación
`python3 tests/check.py --rapido` → 0 FAIL (ver cierre en el PR). `python3 -m pytest -q tests/test_tuberia3.py` → 3 passed. La suite completa la juzga el CI del push.
