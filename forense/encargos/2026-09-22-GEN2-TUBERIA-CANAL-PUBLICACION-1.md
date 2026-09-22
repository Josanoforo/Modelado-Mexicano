# ENCARGO · ACTO GEN2-TUBERIA-CANAL-PUBLICACION-1 · La vista deja de mentir sola: el push a `main` registra lo que cada acto asentó, y los tres archivos de append entran a `merge=union`

> ENTORNO: **NUBE** — cero microdato; el job corre en CI, no aquí. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus (CI + guarda de union: código con juicio) · MODO: **ABIERTO** · CONTADOR: cero mediciones; al primer push posterior, `corridas.tsv` gana las filas de los CALC con asiento y sin fila (22 al redactar; reportado, no prometido) · ids raíz de acto.

## 1 · OBJETIVO
(a) Que el job de push a `main` (`verify.yml:374`, «Re-deriva por comando y commitea [deriva]») ejecute también `corrida0 registro --verifica --escribe --lote <CALC>` con el **lote derivado mecánicamente** del diff de `forense/replay-evidencia.tsv` en ese push (asientos nuevos → sus `calc_id`), sin juicio y sin `--force`; (b) que `forense/replay-evidencia.tsv`, `forense/analisis/ci-guardias/censo-tests.tsv` y `data/corrida0/decisiones.tsv` entren a `merge=union` en `.gitattributes` con la misma guarda de líneas repetidas que ya protege a `no-corrido.tsv` (`tests/test_tuberia_ids_union.py`, caso G3-bis). «Hecho» = un push sintético en rama de prueba con un asiento nuevo produce un commit `[deriva]` con la fila en `corridas.tsv` (log de CI pegado); `git check-attr merge -- <los tres>` → `union`; el test de guarda cubre los tres; las 22 corridas sin fila entran en el primer push real (`status` antes/después).

## 2 · FIRMAS DE MESA
Ya selladas, se citan: FP `…PENDIENTES-CAJA-1-c09b-02` y `…ESCOLARIDAD-2-0af9-01`, opción (a) — «el job del push a main corre `registro --escribe --lote <CALC con asiento nuevo>`, con el lote derivado del diff de `replay-evidencia.tsv` (sin juicio: solo lo que un acto asentó)» (asentadas en #1004 y #1005). Firma de mesa 21/sep §2(2): «los archivos derivados no viajan en los PR» — este acto la respeta: los derivados los escribe el job en `main`, nunca un PR.
*Propuesta de dirección (union), mesa sella o borra:* «Los tres archivos de append (`replay-evidencia.tsv`, `censo-tests.tsv`, `decisiones.tsv`) entran a `merge=union` con guarda de líneas repetidas; sin ella, cada tanda de más de dos actos cuesta un sync por PR (medido: 7 de 9 el 22/sep).»

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` `.github/workflows/verify.yml:359-390`: el job de push a `main` re-deriva `derivados_protegidos.py` y commitea `[deriva]` si hay diff; excluye `registro` «porque exige `--lote`» (:370). `[LEÍDO]` `.gitattributes:19-54`: union para `hallazgos.md`, `bitacora.md`, `no-corrido.tsv`, `firmas-pendientes.tsv`, `gobernanza-v1_15.md`, `registro-rotulos.tsv`; **0** menciones de los tres archivos de (b). `:16`: «NO usar el editor web de conflictos en archivos union».
- `[EJECUTADO]` 22 CALC con `sello.json` y sin fila en `corridas.tsv` al redactar; simulación `git merge-tree` en cadena sobre los 9 PR del 22/sep: solo 2 fusionan sin sync; los otros 7 chocan en esos tres archivos. `[LEÍDO]` `tools/corrida0.py:2985-2999` (doctrina: la fuente es `replay-evidencia.tsv`; las vistas se derivan de ella) y `:4140` (guardia `REPLAY-PISADO`).
- `[SUPUESTO]` `registro --escribe --lote` acepta una lista de `calc_id` y no toca las corridas fuera del lote. Si resulta falso (re-proyecta todo y el guardia para por corridas ajenas sin asiento), el job no fuerza: falla en voz alta con la lista y ese es el hallazgo; **nada de `--force` ni de `--excluye`**.
- `[SUPUESTO]` GitHub no aplica drivers de merge en el botón, pero sí aplica el atributo `union` interno de git en merges locales y en `merge-tree`. Si resulta que el botón tampoco honra `union` interno, la ganancia queda en los syncs locales y en CI, y se dice.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -n "registro" .github/workflows/verify.yml` → solo la exclusión; `grep -c "replay-evidencia\|censo-tests\|decisiones.tsv" .gitattributes` → 0; `grep -rl "CANAL-PUBLICACION\|canal de publicacion" forense/encargos/` → 0 al redactar. Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1 · Derivación del lote.** `tools/lote_desde_asientos.py` (o dentro de `corrida0`): dado `git diff <antes> <después> -- forense/replay-evidencia.tsv`, devuelve los `calc_id` con asiento nuevo cuyo CALC tiene `sello.json` y no tiene fila. Test con un diff sintético.
- **P2 · El job.** Un paso nuevo en el job de push a `main` (solo `push` a `main`, después de la re-derivación, mismo guard anti-loop `[deriva]`): si el lote no está vacío → `registro --verifica --escribe --lote <lote>`; commit `[deriva]` con la lista en el mensaje; si el guardia `REPLAY-PISADO` para → el job falla con la salida cruda (no fuerza). Prueba en rama: un push sintético con un asiento de un CALC de fixture.
- **P3 · Union.** Las tres rutas en `.gitattributes` con el comentario que explica por qué (append-only, una fila por objeto); `tests/test_tuberia_ids_union.py` extendido: dos ramas que añaden filas distintas fusionan sin conflicto; dos que añaden la **misma** fila → la guarda lo atrapa (líneas repetidas). La guarda corre en CI como huérfano (`ci_guardias --ejecuta-huerfanos`).
- **P4 · Primer push real y nota.** Tras fusionar, el primer push registra las corridas con asiento; `status` antes/después y `grep -c` de `corridas.tsv` en la nota (o, si este PR fusiona vía botón, el job lo hace en el push de merge y la nota cita ese commit `[deriva]`). NC-0257/0284/0329 y las `NO-CORRIDO` «DIFERIDO-A: acto TUBERIA» de #1008/#1012/#1005/#1003 → enmienda fechada con este acto como sucesor cumplido (cierra las que solo esperaban el canal).

## 6 · LATITUD
DECIDES TÚ: nombre y ubicación del derivador del lote, cómo simular el push en rama, el texto de `.gitattributes`. PREGUNTAS A MESA: si `registro --escribe` no admite `--lote` parcial sin re-proyectar todo (§3), ¿se añade la bandera de lote **estricto** en `corrida0.py` (recomendado: ≤ 30 líneas, con test) o el job registra todo lo que tenga asiento? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · **b) `--force`, `--excluye`, reescribir sellos o vistas a mano** · c) adoptar · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
«P2 probado con push sintético en rama antes de tocar `main` — protege: borrar (una vista mal escrita en `main` es un borrado).»

## 9 · PERÍMETRO
Propio: `.github/workflows/verify.yml` (un paso) · `tools/lote_desde_asientos.py` (nuevo) · `.gitattributes` (tres líneas) · `tests/test_tuberia_ids_union.py` · `tests/test_lote_desde_asientos.py` (nuevo) · `forense/no-corrido.tsv` (enmiendas) · nota · `canon/L0/<raíz>.md`. Ajeno: `tools/corrida0.py` salvo la bandera de §6 si mesa la autoriza; ningún CALC; ninguna vista a mano. Otro acto en vuelo: E12–E15 (todos asientan en `replay-evidencia.tsv`): sin conflicto de contenido; **este PR fusiona primero**. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No registra a mano, no adopta, no cambia E.7 (la cumple). Sucesor: P5 del plan (clases de auto-merge) ahora que el canal existe. Auditoría: no aplica. Cierre por /acto.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P4 · primer push real que registre el backlog (22 CALC selladas sin fila al redactar, más las de las NC enmendadas abajo) | DECISIÓN-DE-MESA-PENDIENTE: el mecanismo (P1+P2) existe y está PROBADO con push sintético en rama (camino feliz + camino de guardia), pero el estado real de `main` hoy tiene drift preexistente (13 corridas ajenas cuyo veredicto en `replay-evidencia.tsv` ya no coincide con lo publicado) que dispara `REPLAY-PISADO` sobre cualquier lote pequeño. Este PR no toca `corridas.tsv`/`resultados.tsv`/`usos.tsv` (firma de mesa 21/sep §2(2)), así que no puede ejecutar el catch-up desde aquí. | `corridas.tsv` sigue sin las 22+ corridas selladas «en disco, no registradas»; `corrida0 status` las proyecta, la vista publicada no. | `FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` (pregunta a mesa: ¿lote estricto en `corrida0.py`, o catch-up explícito primero?) |
| §6 LATITUD · bandera de lote estricto en `tools/corrida0.py` | DECISIÓN-DE-MESA-PENDIENTE: el encargo la deja explícitamente como pregunta a mesa, no como LATITUD del ejecutor. | El primer push real probablemente PARA por `REPLAY-PISADO` hasta que mesa decida esta bifurcación o autorice un catch-up. | `FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` |
| Cierre de `NC-0257`/`NC-0284`/`NC-0329` citadas en P4 | SUSTITUIDO-POR:ya CERRADAS por otra vía antes de este acto (re-verificado, `estado=CERRADA` en `forense/no-corrido.tsv`) — premisa de logística del encargo, no un hallazgo de este acto. | Ninguno: ya estaban resueltas. | Ninguno — ya cerradas |
| Cierre de las cuatro NC `DIFERIDO-A: acto TUBERIA` (#1008/#1012/#1005/#1003) | NO-VERIFICABLE-AQUÍ: el encargo pedía "sucesor cumplido → cierra", pero cerrar exigiría que la fila esté PUBLICADA en `corridas.tsv`, y sigue sin estarlo (el mecanismo existe, no se ha ejecutado en `main`). Se ENMENDARON con fecha (mecanismo entregado y probado), no se cerraron — cerrarlas ahora sería falso. | Las cuatro corridas correspondientes siguen "selladas en disco, no registradas". | El propio primer push real (fila de arriba) |


