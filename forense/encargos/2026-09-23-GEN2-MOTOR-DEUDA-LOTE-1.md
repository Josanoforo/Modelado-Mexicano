# ENCARGO · ACTO GEN2-MOTOR-DEUDA-LOTE-1 · Con la autorización D7-A: corrige las dos citas de `motor.py`, resuelve el `commit_declaracion` de ADR-68 para catálogo/motor, y deja en verde o dictaminadas las ocho fallas restantes de los tests del motor y de consulta

> ENTORNO: **NUBE** — código y tests; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `ae19a710` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-motor-deuda-lote-1` (D-17) · MODELO: Opus · MODO: ABIERTO (lote D-11: cuatro piezas afines; una que PARA no tumba el lote) · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; si una edición mueve el contexto de replay de un sello, ese CALC se sucede por uno nuevo (E.3) — no se reescribe.

## 1 · OBJETIVO
Cerrar la deuda del motor que llevaba dos días esperando permiso: NC `…MOTOR-THETA-CONGELADA-1-e8fa-01` (editar `milpa/src/motor.py:20` y `:129`: citar BARRIDO-2 en vez de ADR-531), `…e8fa-02` (`commit_declaracion` de ADR-68 para catálogo/motor; `test_motor_holdout::test_c_roles_sellados_antes_que_todo_resultado` FAIL anterior a #883), NC-0445 (4 fallas de `tests/test_motor_gen2_explicito.py`: el p de `tramite.evade/cuidado` vs `RESULT-ENUT-A-R` sellado, y la `ola_calibracion` faltante de `tramite.evasion_norma`), NC-0446 (4 fallas de `tests/test_consulta_gen2.py`: respuestas de ejemplo `forense/ejemplos/GEN2-*` congeladas contra un índice que cambió). Habilita: ASTRA-2 (θ) y MOTOR sin tests rotos que nadie puede tocar.
«Hecho»: `pytest tests/test_motor_gen2_explicito.py tests/test_consulta_gen2.py tests/test_motor_holdout.py -q` con 0 FAIL, **o** cada falla restante con dictamen en la nota (`NO-PROCEDE` con razón / `DIFERIDO-A` con sucesor) y su NC; `grep -n 'ADR-531' milpa/src/motor.py` → 0 en las líneas de la NC · las cuatro NC CERRADAS o con sucesor nombrado · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
D7 (23/sep, verbatim «A.», asentada por FIRMAS-11): «Se autoriza un acto de MOTOR a editar milpa/src/motor.py en las líneas citadas por NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01; los dos sellos cuyo contexto cambie se suceden por CALC nuevos, no se reescriben.»

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Las cuatro NC (texto y sucesor) en `no-corrido.tsv` al `ae19a710`; todas ABIERTAS. e8fa-01 nombra líneas :20 y :129 — **verifica que sigan siendo esas** (el archivo pudo moverse; se busca por objeto, la cita a ADR-531, no por número de línea).
- `[LEÍDO]` NC-0445: la causa original (ValueError del cargador) ya está CERRADA; quedan dos causas nuevas. NC-0446: ídem; quedan comparaciones de ejemplos.
- `[SUPUESTO]` que editar `motor.py` cambia el hash de contexto de dos CALC sellados (la NC lo dice: «mueve el contexto de replay de dos sellos»). **Identifícalos por comando** (`grep -rl motor.py data/corrida0/CALC-*/spec.yaml` o el campo `dependencias_materiales`) antes de editar; para cada uno, `verify` después de la edición: si RESULTADO=REPRODUCE y CONTEXTO=DISTINTO, se declara en la nota y NO se re-sella (E.3: NO-VERIFICABLE/DISTINTO no se degrada); si RESULTADO cambia, CALC sucesor.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log --oneline -3 -- milpa/src/motor.py` → reporta; ningún commit posterior a #883 toca las citas. `git ls-remote --heads origin | grep -i motor` → 0.

## 5 · PIEZAS
- **P1 · Citas de `motor.py`** (e8fa-01): ADR-531 → BARRIDO-2 en las dos líneas; prueba de que el texto citado existe. `verify` de los CALC afectados (§3).
- **P2 · `commit_declaracion` ADR-68** (e8fa-02): leer ADR-68 y `test_motor_holdout`; si el test exige un commit de declaración de roles anterior a todo RESULT y ese commit existe pero no está citado, se cita; si no existe, el test no puede pasar por historia → dictamen `NO-PROCEDE-HISTÓRICO` con la evidencia (`git log`), el test se marca `xfail` con razón y la NC lo cita. No se reescribe historia.
- **P3 · NC-0445**: (1) el p de `tramite.evade/cuidado`: si el índice del motor tiene un valor tecleado y el RESULT sellado otro, el índice se corrige al RESULT por id (regla de oro §2); (2) `ola_calibracion` de `evasion_norma`: se toma del CALC que la sella (piloto 4 la re-derivó) por id; si no existe sellada, `NO-CONSTRUIBLE` y el test lo refleja.
- **P4 · NC-0446**: las respuestas de ejemplo `forense/ejemplos/GEN2-*` se re-sellan contra el índice actual **solo si** cada diferencia se explica por un RESULT sellado posterior (cítalo); una diferencia sin explicación es hallazgo, no re-sello.

## 6 · LATITUD
Orden libre. ≤ 10 líneas adyacentes: sí, declarado. Pregunta a mesa (sigues): si P2 exige elegir entre `xfail` y borrar el test — recomendación: `xfail` con razón.

## 7 · PAROS — lista cerrada
a) no aplica · b) reescribir un sello o un CALC (`run` se niega; sucesor sí) · c) mover contadores a mano · d) no aplica · e) CAJA · f) las cuatro NC ya están cerradas en origin/main.

## 8 · COMPUERTAS
«`verify` de cada CALC afectado antes y después de tocar `motor.py`» protege: **borrar/reescribir** (E.3). «Índice corregido solo hacia un RESULT sellado por id» protege: **congelar** (§2).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `milpa/src/motor.py` (solo las líneas de la NC), `milpa/src/` índice de consulta donde viva el p y la ola (cita), `tests/test_motor_gen2_explicito.py`, `tests/test_consulta_gen2.py`, `tests/test_motor_holdout.py`, `forense/ejemplos/GEN2-*` (P4), CALC sucesores si los hay, `no-corrido.tsv`, nota, L0, cascada. Ajeno: `matriz.py`, `celdas.py`, `tramite.yaml`, cualquier CALC sellado. En vuelo: `codex/astra-theta-*` lee el motor y **no lo edita** (MISION-ASTRA-2); si una rama de Astra tocó `motor.py`, PARA esa pieza y avisa.

## 10 · LO QUE NO HACE · SUCESORES
No calibra θ, no toca la matriz. Sucesores: ASTRA-2 sigue sobre el motor limpio; `GEN2-MOTOR-DEUDA-LOTE-2` para lo que quede `DIFERIDO-A`.

## NO-CORRIDO / RESERVAS

- **P1 · Citas de `motor.py` (e8fa-01)** — `PARO-PREMISA` (superado, re-verificado A.17). Al arrancar, D7 solo existía en `origin/acto/gen2-tramite-firmas-11` (PR #1049), sin fusionar. **Re-verificado tras `git merge origin/main` (23/sep, mismo día):** PR #1049 fusionó; `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01` está CERRADA en `origin/main` citando `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-06` («A.»), y mesa nombró el sucesor de la edición como `GEN2-MOTOR-LOADER-Y-RESELLO-1` — no este rótulo. Este acto nunca amplió su perímetro a ejecutar P1 (el encargo la deja fuera §10), así que no hay edición que hacer aquí: la pieza cierra por objeto, la ejecución le toca al rótulo que mesa ya nombró. `motor.py` sigue sin editar por este acto (fuera de perímetro, no PARO). Fila: `NC-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-01` (CERRADA).
- **P3 · NC-0445 (2 fallas de `tests/test_motor_gen2_explicito.py`)** — `PARO-PREMISA`. Las causas que la NC documentaba (21/sep: el `p` de `tramite.evade/cuidado` vs `RESULT-ENUT-A-R`; `ola_calibracion` faltante) están `VENCIDAS EN ALCANCE` (A.10): las fallas reales hoy son por universo GEN2 nuevo (`forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:*`, 32 vs 13 esperados) y un snapshot congelado (`snapshot-M-gen2-explicito-v1_2.json`) con un diff de 234 298 caracteres. Toca qué se mide (universo declarado, snapshot congelado) — no se re-sella sin decisión de mesa. Impacto: `tests/test_motor_gen2_explicito.py` sigue con 2 FAIL. Sucesor: `GEN2-MOTOR-DEUDA-LOTE-2`, re-censar el universo vigente antes de intentar cerrarla. Fila: `NC-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-02`.
- **P4 · NC-0446 (4 fallas de `tests/test_consulta_gen2.py`)** — `PARO-PREMISA`. Misma familia de causa que P3 (universo GEN2 nuevo para `test_01`/`test_01b`) más las respuestas de ejemplo congeladas de `forense/ejemplos/GEN2-*`; NC-0446 exigía re-sellar solo si cada diferencia se explica por un RESULT sellado posterior citado, y verificarlo para 2 respuestas completas excede lo resoluble de pasada en este acto. Impacto: `tests/test_consulta_gen2.py` sigue con 4 FAIL. Sucesor: `GEN2-MOTOR-DEUDA-LOTE-2`. Fila: `NC-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-03`.

Lo demás del lote — P2 (`commit_declaracion` de ADR-68) — sí corrió: ver `## CONSUMIDO`.

## CONSUMIDO

Ejecutado por PR #1054 (`acto/gen2-motor-deuda-lote-1`). P2 resuelto (dictamen `NO-PROCEDE-HISTÓRICO`, `NC-...-e8fa-02` CERRADA); P1/P3/P4 en `## NO-CORRIDO / RESERVAS` arriba. Detalle: `canon/gobernanza-v1_15.md` `ADR-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-01`, `forense/notas/2026-09-23-GEN2-MOTOR-DEUDA-LOTE-1-cierre.md`.
