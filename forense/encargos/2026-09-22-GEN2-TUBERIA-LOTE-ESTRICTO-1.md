# ENCARGO · ACTO GEN2-TUBERIA-LOTE-ESTRICTO-1 · La bandera que hace efectiva la firma del canal: `registro --escribe --lote` escribe solo las filas del lote, y el primer push real publica los 22 sellados sin tocar los 13 con drift

> ENTORNO: **NUBE** — cero microdato (el job corre en CI; aquí solo código, test y push sintético). Hook; si no coincide, PARA.

CABECERA · SHA `c9b67bf8` · una sola sesión · MODELO: Opus (tocar `registro --escribe` es tocar el único paso que escribe la vista) · MODO: **ABIERTO** · CONTADOR: cero mediciones; al primer push real posterior, `corridas.tsv` gana las filas de los CALC con asiento y sin fila (22 al redactar; derivado) · ids raíz de acto.

## 1 · OBJETIVO
Que `python3 tools/corrida0.py registro --verifica --escribe --lote <ids>` escriba **solo** las filas de los `calc_id` del lote y deje intactas todas las demás — sin re-proyectar el replay de corridas fuera del lote y sin que el guardia `REPLAY-PISADO` tenga nada que pisar fuera de él —, con un test que lo pruebe y un push sintético en rama que lo demuestre contra el drift real. Es la opción (a) de FP 7d98-01, firmada. «Hecho» = `tests/test_registro_lote_estricto.py` en verde (fixture: vista con 3 corridas, una con drift fuera del lote; `--lote` con 1 id nueva → la vista cambia en exactamente una fila y el guardia no dispara); push sintético en rama con un asiento de fixture → job del canal termina en `[deriva]` con una fila nueva y **sin** tocar las 13 con drift (log pegado); ≤ 30 líneas netas en `corrida0.py` (o el número real, dicho); primer push real tras fusionar: `status` antes/después y `grep -c` de `corridas.tsv` en la nota (o cita al commit `[deriva]` si fusiona por botón).

## 2 · FIRMAS DE MESA
Ya sellada, se cita: FP `…CANAL-PUBLICACION-1-7d98-01`, opción (a) (22/sep/2026; asentada por `GEN2-TRAMITE-FIRMAS-8` o, si este acto abre antes, citada del hilo de dirección como tipo (3) — la firma es de mesa; la fila la pone el trámite). Ninguna nueva.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` `.github/workflows/verify.yml:422-480`: el job deriva el lote con `tools/lote_desde_asientos.py "$ANTES" HEAD --csv` y corre `registro --verifica --escribe --lote "$LOTE"`; si el guardia para, el job falla con la salida cruda. `[LEÍDO]` `tools/corrida0.py:2985-2999` (doctrina), `:4140` (guardia `REPLAY-PISADO`), `:1139` (`_asigna_ids(estricto=False)` es **otro** objeto: ids, no lote). `[LEÍDO]` NC 7d98-02: «no se añadió … DECISIÓN-DE-MESA-PENDIENTE»; FP 7d98-01: «13 corridas ajenas cuyo veredicto ya no coincide con lo publicado, medido con push sintético».
- `[SUPUESTO]` Hoy `--lote` acota qué se **verifica** pero `--escribe` re-proyecta la vista entera desde `replay-evidencia.tsv` (por eso el drift dispara el guardia aunque esas corridas no estén en el lote). Si resulta que `--lote` ya acota la escritura y el guardia dispara por otra causa, el hallazgo es esa causa y el acto la mide antes de escribir código.
- `[SUPUESTO]` Acotar la escritura al lote no rompe la doctrina «las vistas se derivan de la fuente»: las filas fuera del lote se copian tal cual del último `corridas.tsv` publicado, que ya fue derivado de la fuente en su momento. Si resulta que alguna vista derivada (`resultados.tsv`, `usos.tsv`) no admite escritura parcial, PARO f) y el diseño vuelve a dirección.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -n "lote" tools/corrida0.py | grep -i "escrib\|estricto"` → reporta; `ls tests/ | grep -i "lote"` → `test_lote_desde_asientos.py` (otro objeto). Ramas vivas: TRAMITE-FIRMAS-8 (tablero) — sin archivo común.

## 5 · PIEZAS
- **P1 · Medición previa.** Reproducir el drift con push sintético en rama (como hizo el canal): lista de las 13, salida del guardia. Es el caso de prueba real.
- **P2 · La bandera.** `registro --escribe --lote <ids>` acota la **escritura** a esas filas (y sus derivados por fila: `resultados.tsv`, `usos.tsv`); las demás se conservan byte a byte; el guardia se evalúa solo sobre el lote. Sin bandera nueva si `--lote` puede significar eso (recomendado: cambiar la semántica de `--escribe` con `--lote` y documentarlo en la ayuda); con bandera `--estricto` solo si hay un consumidor que necesite el comportamiento viejo (nómbralo). Docstring con la doctrina. ≤ 30 líneas netas o el número real.
- **P3 · Tests.** `tests/test_registro_lote_estricto.py` (fixture de §1) + caso «guardia dispara si el propio lote pisa un veredicto sin causa nombrada». Cableado en `verify.yml` como bloqueante (NC-0331: un test que nadie corre es decoración).
- **P4 · Push sintético y nota.** El job del canal contra una rama con un asiento de fixture: `[deriva]` con una fila, 13 intactas, log pegado. Nota: qué cambió, qué no, y la lista de las 13 para `GEN2-REPLAY-ASIENTOS-2`.

## 6 · LATITUD
DECIDES TÚ: bandera nueva vs semántica de `--lote`, nombre del test, cómo copiar filas fuera del lote. PREGUNTAS A MESA (y sigues): si `usos.tsv` se deriva de forma global (no por fila) y no admite escritura parcial, ¿se re-deriva entero pero sin tocar `resultado_replay` de corridas fuera del lote (recomendado) o se PARA? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · **b) `--force`, `--excluye`, reescribir vistas a mano, o cambiar veredictos fuera del lote** · c) adoptar · d) no aplica · e) caja · f) inalcanzable → PARO como entregable.

## 8 · COMPUERTAS
«Push sintético VERDE en rama antes de fusionar — protege: borrar (una escritura parcial mal acotada es un borrado de vista).»

## 9 · PERÍMETRO
Propio: `tools/corrida0.py` (`cmd_registro`/`--escribe --lote`, ≤ 30 líneas netas) · `tests/test_registro_lote_estricto.py` (nuevo) · `.github/workflows/verify.yml` (un paso de test; **no** el job del canal) · `forense/no-corrido.tsv` (NC 7d98-02 → CERRADA; 7d98-01/-04 y las cuatro `DIFERIDO-A` cierran cuando el primer push real publique, con cita) · nota · `canon/L0/<raíz>.md`. Ajeno: `lote_desde_asientos.py`, `.gitattributes`, sellos, `replay-evidencia.tsv` (se lee). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No registra a mano, no asienta drift (eso es `GEN2-REPLAY-ASIENTOS-2`, caja), no toca el job salvo el test. Sucesor: el primer push real (publica los 22); `GEN2-REPLAY-ASIENTOS-2` (los 13). Auditoría: no aplica. Cierre por /acto.

## NO-CORRIDO / RESERVAS

- **qué**: §1 OBJETIVO — «primer push real tras fusionar: `status` antes/después y `grep -c` de `corridas.tsv` en la nota (o cita al commit `[deriva]` si fusiona por botón)».
  **por qué**: DIFERIDO-A:primer push real a main — el mecanismo (P1+P2) está implementado y probado con push sintético en un clon desechable (antes/después del fix, log en la nota), pero el objetivo de §1 exige un push REAL a `main` con el fix ya fusionado, que depende de que mesa fusione este PR y de que un push posterior traiga un asiento nuevo en `replay-evidencia.tsv` que dispare el canal.
  **impacto**: `corridas.tsv`/`resultados.tsv` de `main` siguen sin las 22+ corridas selladas sin fila (mismo estado que `ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` dejó); lo que cambia es que el mecanismo que las publicará ya no bloquea con las 13 corridas ajenas.
  **sucesor**: el primer push real a `main` (mecanismo ya probado en este acto); `GEN2-REPLAY-ASIENTOS-2` para asentar o re-verificar la evidencia de las 13 corridas con drift real. Fila: `NC-260923-GEN2-TUBERIA-LOTE-ESTRICTO-1-9428-01`.

## CONSUMIDO

PR [#1028](https://github.com/Josanoforo/Modelado-Mexicano/pull/1028). `ADR-260923-GEN2-TUBERIA-LOTE-ESTRICTO-1-9428-01`. `tests/check.py --rapido`: VERDE, 0 FAIL (303 WARN). El PR queda propuesto contra `main`; mesa central fusiona.
