# ENCARGO · ACTO GEN2-TUBERIA-CI-TIEMPO-2 · El círculo que deja `check` en rojo y el canal sin publicar desde el 25/sep: la derivación de vistas sale del check requerido a un job propio, el lote de replay se trocea para que la base avance aunque un run se corte, y el canal vuelve a abrir `[deriva]` en cada push, a mano y cada noche

> ENTORNO: **NUBE** — `.github/workflows/`, `tools/lote_desde_asientos.py`, `tools/corrida0.py registro --lote`. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `9ceb1eac` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; contadores propios: minutos de `check` en push a `main` (< 25, medido), tamaño del lote pendiente de replay (121 → 0 en N runs, medido), fecha del último `[deriva]` fusionado (25/sep → hoy). **Ningún test se relaja; ningún veredicto de replay se salta**: cambia dónde y en cuántas partes corre.

## 1 · OBJETIVO
Medición de CI-TIEMPO-1 (#1187, NC `…c6d9-05`): en los push de #1185/#1187/#1188/#1189, `suite` termina en 3 min 17 s y `adicionales` en 3 min 34 s, pero `guardias` muere a los 30 min en «Deriva vistas y abre PR automático» con un lote de replay de 121 CALC (asientos posteriores al último punto derivado `b804165…`); como el run se cancela, la base no avanza y el lote crece con cada merge. (P1) **Job propio `derivados`**, disparado por `push` a `main`, `workflow_dispatch` y `schedule` nocturno, **fuera de `needs` de `check`**: el check requerido conserva su nombre y sigue exigiendo `suite`, `adicionales`, `guardias` (sin el paso de derivados), `preflight-calc`, `guardas-res`, `enrutamiento-pr`; ningún test cambia. (P2) **Lote troceado con base que avanza**: `lote_desde_asientos.py` arma trozos de tamaño fijo (declarado en la spec; sugerencia inicial 20 CALC) y `registro --escribe --lote <trozo>` publica cada trozo en el mismo PR `[deriva]` (commit por trozo, `ANTES` avanza por trozo); si el job se corta, el siguiente run retoma desde el último trozo publicado, no desde el 25/sep. El tope del job: 30 min (se conserva); con trozos de 20 nunca debería tocarse, y si lo toca, el siguiente run continúa. (P3) **Drenar el rezago hoy**: tras el merge, disparar a mano hasta que el lote pendiente sea 0 y el `[deriva]` resultante traiga `usos.tsv`, `corridas.tsv`, `resultados.tsv` (< 50 MB), `marcador-segmento.tsv`, `canon/TABLERO-PROGRAMA.md` (con `¿árbol == origin/main? True`) y `README` derivado; auto-merge lo fusiona. (P4) **Guardia de crecimiento**: si el lote pendiente supera un umbral declarado (p. ej. 60 CALC), el job lo dice en la primera línea del log y abre NC automática (no falla el check: avisa). (P5) Cerrar `…c6d9-05` y las NC del canal que sigan abiertas por «sin [deriva]» (por id, A.17).
«Hecho» sobre el commit final con origin/main fusionado: el run del push a `main` de este PR termina con `check` VERDE en **< 25 min** (citado) · el job `derivados` existe, no está en `needs` de `check`, se dispara por push/dispatch/schedule · un `[deriva]` fusionado después de este acto, citado por PR, con las cinco vistas y el tablero adentro, y `status` en `main` con los valores del derivador (`adoptados` > 81 esperado; el número lo da el derivador) · lote pendiente = 0 al cierre (comando pegado) · guardia de crecimiento con test · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
D4-A y R(a) (check requerido y auto-merge de rutinas: el `[deriva]` sigue siendo rutina), D-16 (la suite adjudica por FAIL), D-23 (una herramienta de verificación no muta el clon; el job de derivados escribe solo en su PR), E.7 (toda corrida sellada entra a la vista: **trocear no es excluir**; ningún CALC se salta), CI-TIEMPO-1 (#1187) como antecedente. **Dirección, 26/sep (chat, tras la medición de la sesión de -1):** «CI-TIEMPO-2 con los dos cambios y uno más: derivación en job propio fuera del check, lote troceado con base que avanza, y disparo manual y nocturno.»

## 3 · LO QUE DIRECCIÓN SABE
`[LEÍDO]` reporte de la sesión de CI-TIEMPO-1 (26/sep): run `36291122052` 03:20–03:50 cancelado; `suite` 3m17s (`check.py` 2m59s); `adicionales` 3m34s; `guardias` → paso de derivados: «asientos nuevos examinados: 121», muerto a 03:50:48 con `python3` vivo; base `ANTES: b804165…`; el lote crece con cada merge. `[EJECUTADO]` (`9ceb1eac`) `verify.yml`: `guardias` 30 min contiene el paso de derivados (TABLERO-EN-CANAL-1 lo puso ahí con dos pasadas del marcador y el tablero; VISTA-4 la guarda 100→50); sin `[deriva]` fusionado desde #1147 (25/sep); `status` en `main` = vistas del 23–25. `[SUPUESTO]` que `registro --escribe --lote` es incremental (solo re-deriva los CALC del lote y funde con la vista existente): si no lo es, el troceo exige que lo sea, y eso se hace aquí con test de equivalencia byte a byte contra una derivación completa.

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c CI-TIEMPO-2` → 0. CI-TIEMPO-1 archivado y consumido (#1186, #1187): se cita; sus NC `c6d9-01..06` se leen. **Repítelo** (búscalo por archivo, no por rama).

## 5 · PIEZAS
P1 job propio → P2 troceo con base por trozo (+ test de incrementalidad) → P3 drenaje a mano hasta 0 → P4 guardia → P5 cierre.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 + AMPLITUD
1–7 verbatim. Tamaño del trozo, umbral de la guardia, hora del nocturno: tuyos, declarados. Si `registro --lote` no es incremental y hacerlo excede el acto, se publica por trozos re-derivando completo pero commiteando por trozo (la base avanza igual) y se abre NC. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) excluir un CALC del lote, `--force`, `--excluye`, editar vistas a mano, relajar un test, cambiar el nombre del check · c) mover contadores a mano · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«El check requerido no pierde ningún test; solo pierde la derivación» protege **congelar** (D-16). «Trozo publicado = trozo derivado completo y verificado; nada se salta» protege **borrar** (E.7). «Base avanza solo por commit en el PR `[deriva]`» protege **congelar** (D-23).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml` (job `derivados` nuevo; `guardias` sin ese paso; `on:`), `tools/lote_desde_asientos.py`, `tools/corrida0.py` (solo `registro --lote`, incrementalidad), `tools/ci_guardias.py` (guardia de crecimiento), tests, `no-corrido.tsv`, nota, L0, cascada. Ajeno: `check.py`, tests individuales, medidores, vistas (solo por el job). En vuelo: RECIBO-ASTRA6-1 (nube; no toca CI), Astra (no toca CI); `derivados/2026-09-26` (rutina: se fusiona antes o el drenaje lo absorbe).

## 10 · LO QUE NO HACE · SUCESORES
No cambia qué se verifica ni qué se publica. Sucesor: `-3` solo si el nocturno revela que un trozo quedó sin publicar.

## NO-CORRIDO / RESERVAS

| qué (del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| (P3) Drenar el rezago hoy: disparar a mano hasta lote pendiente 0 y `[deriva]` fusionado con las cinco vistas y el tablero | NO-VERIFICABLE-AQUÍ — el job `derivados` solo existe en main tras el merge de mesa | el canal sigue sin publicar hasta el merge | esta sesión tras el merge de #1198 (disparo manual) |
| «Hecho»: run del push a `main` con `check` VERDE < 25 min, citado | NO-VERIFICABLE-AQUÍ — solo existe tras el merge | sin cita hasta el merge | esta sesión tras el merge de #1198 |
| (P5) Cerrar `…c6d9-05` y las NC del canal abiertas por «sin [deriva]» | DIFERIDO-A:post-merge de #1198 — cerrarlas exige el run de main y el `[deriva]` fusionado | NC siguen ABIERTAS | esta sesión tras el merge de #1198 |
| Reserva: dos runs de `derivados` sobre bases distintas proponen el mismo trozo en dos PR | DIFERIDO-A:GEN2-TUBERIA-CI-TIEMPO-3 — la concurrencia evita correr a la vez, no el solape | el segundo PR queda en conflicto, sin auto-merge | GEN2-TUBERIA-CI-TIEMPO-3 |

Filas `NC-260927-GEN2-TUBERIA-CI-TIEMPO-2-a387-01..04` en `forense/no-corrido.tsv`.

## CONSUMIDO

Consumido por Josanoforo/Modelado-Mexicano#1198. ADR `ADR-260927-GEN2-TUBERIA-CI-TIEMPO-2-a387-01`; nota `forense/notas/nota-2026-09-27-gen2-tuberia-ci-tiempo-2.md`.
