# Cierre — `ACTO MAESTRA30-E9 · SCORING-V2`

26/ago/2026. `main` en `6d213a6` al arrancar (incluye `E7 #378`, `E8 #380`
— el gate —, `E10 #379`), sin avance nuevo al cerrar (re-verificado).
Worktree `/home/pc0/mm-e9-scoring-v2`, rama `acto/e9-scoring-v2`.

## 1 · Compuerta cero

`E8` (`PR #380`, `ACTO MAESTRA30-E8`) `MERGED` `2026-08-26T23:11:03Z`.
`sha256sum forense/prereg-duelo-v2/scoring-adv1-m3.py` =
`63418cc8cfdb03ba5d851d01f1bba23e2f21dbac5cfbed2d88c2832cba13a8cf`,
coincide con la fila `## F1 · enmienda 2026-08-26` de `prereg-corrida-v1_0.md`
(no con la tabla original). `tests/test_crosswalk_encuesta.py`: 4 passed.

## 2 · Corrida de `M` — conteos A.13

- Celdas sorteadas evaluadas: **15 de 15**.
- `construir_crosswalk()` re-ejecutado en vivo, dos corridas frescas:
  filas de datos **idénticas** entre sí y contra
  `forense/crosswalk-pregunta-regla-v1_1.tsv` ya comprometido (único diff:
  9 líneas de comentario documental que preceden a los datos en el
  archivo comprometido, cero diferencia en las filas de datos mismas).
- `NO-EMITE` en pasada 1: **15 de 15** (0 alcanzan `CANDIDATO-EMITE`).
- `emisor.emitir_binaria` invocado: **0 veces** (exige un objeto `Regla`
  real; ninguna de las 15 lo tiene — no hay invocación posible, no que se
  haya omitido).
- `corridas-M/M-{celda}.json` escritos: **15 de 15**, todos `NO-EMITE`,
  citando la fila correspondiente de `enlace-M-v1_0.md`. (Prefijo `M-`
  para no colisionar de nombre con `corridas-R/{celda}.json` bajo `T02` —
  re-verificado `--baseline` VERDE tras el renombre.)
- Celdas M-emitidas con punto real: **0**.

## 3 · Intento de scoring real — conteos A.13

- Documento construido: corredores activos **2** (`L_SOLO`, `M`),
  comparaciones `L↔M` declaradas **1** (`L_SOLO_vs_M`), `e_id` ausente
  (sin corredor `E` activo), `delta`/`nivel_ic`/`seed` **omitidos a
  propósito** (0 citas en el árbol tras búsqueda exhaustiva, ver
  `procedimiento-scoring-v1_0.md` §3).
- `ejecutar_scoring(documento)` invocado: **1 vez** (mismo resultado
  reproducido una segunda vez desde el script comprometido,
  `corridas-M/intento_scoring_e9.py`, para confirmar determinismo del
  intento mismo).
- Resultado: `ErrorScoring` / `CONFIGURACION_INVALIDA` / *"faltan
  parámetros obligatorios: delta, nivel_ic, seed"*.
- Celdas pareadas `L↔M` que el motor llegó a construir: **0** (el error
  ocurre en `validar_configuracion`, antes de que `construir_matriz_mediciones`
  se invoque siquiera — no hay universo que contar).
- Comparación con `E7`/v1.0: `E7` falló en la capa de conteo de
  corredores (`1 de 4` exigidos). Este acto **supera esa capa** (el
  contrato `F1` de `E8` la relajó) y falla en la siguiente, más profunda.
  Progreso real, no repetición del mismo hallazgo.

## 4 · Hallazgo adicional declarado (no ejecutado como segunda corrida)

Por lectura de código, citada con línea: aun con `delta`/`nivel_ic`/`seed`
presentes, la comparación principal fallaría con `SIN_CELDAS_PAREADAS`
(`scoring-adv1-m3.py:1044-1048`) porque `M` tiene 0 puntos en las 15 y
`L-solo` no tiene una `skill` normalizada poblable sin baseline `B`
(`SIN_BASELINE` en las 15). Adicionalmente, `interval_score`/
`crps_normal_aprox` están definidas en el módulo pero `ejecutar_scoring`
nunca las invoca (verificado leyendo la función completa) — no hay
salida de esas métricas que reportar. Este acto **no corrió una segunda
vez con valores fabricados** para confirmar `SIN_CELDAS_PAREADAS`
empíricamente — la conclusión sale de leer el código, no de contaminar
el intento con un `delta`/`nivel_ic`/`seed` inventado.

## 5 · Marcador v1.1

`marcador-piloto-v1_1.md` escrito. Misma cabecera `PILOTO SIN VEREDICTO`
verbatim. Tabla de 15 celdas re-confirmada idéntica a v1.0 en `L-solo`
(re-agregado de `corridas-L/`, sin cambio de insumo) y en `R`/`EE`/`dif`/
banda (re-computado directo de `corridas-R/`, sin cambio de insumo). `M`
sigue `NO-EMITE` en las 15 — mismo cero, cita actualizada a
`enlace-M-v1_0.md`/`ADR-208` (crosswalk corregido) en vez de
`DERIVACION-M-v1_0.md` (diagnóstico pre-corrección). Comparación `L↔M`:
**no reportada** — `n=0`, condición explícita del encargo para omitirla.
Reserva `FP-163` del v1.0 (banda `0.5·EE(R)` "no firmada") **corregida**:
FIRMADA, `ADR-199`, 26/ago/2026. `marcador-piloto-v1_0.md` marcado
`SUPERADO` en su cabecera, intacto en el resto.

## 6 · Fila de tablero — sí se abre (A.12)

Se abre `FP-168`: el hallazgo es genuino y de otro modo queda solo
narrado en esta nota, sin rastro en el tablero que futuros actos
consultan primero. Paralelo directo de `FP-163` (que sí trackeaba el
hueco de la banda TOST antes de que mesa la firmara) — aquí el hueco es
`nivel_ic`/`seed` del mismo script, nunca antes trackeado porque ningún
acto anterior llegó a esta capa de validación.

## 7 · Qué NO se hizo (perímetro)

No se editó `emisor.py`, `scoring-adv1-m3.py`, el crosswalk ni el enlace.
No se recalculó `R` ni `B`. No se llamó red ni API. No se adjudicó
casilla, letra ni tier. No se inventó `delta` (más allá de la regla ya
firmada), `nivel_ic` ni `seed`. No se convirtió "0 de 15" en veredicto.
Hito D: sin movimiento (por diseño del acto).

## 8 · Suite

`python3 tests/check.py --baseline` — resultado en el cuerpo del PR (se
corre después de esta nota, antes de abrir PR).

Detalle completo, con comandos y salidas verbatim: `procedimiento-scoring-v1_0.md`,
`corridas-M/_intento-scoring-v1_1.json`, `marcador-piloto-v1_1.md`.
