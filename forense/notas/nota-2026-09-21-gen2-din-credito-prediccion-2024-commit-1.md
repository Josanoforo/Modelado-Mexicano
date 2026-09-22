# Nota de cierre · ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1

21/sep/2026, CAJA. Encargo:
`forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1.md`
(sha256 cuerpo `b3c62b4a7ed4bf65175c795fdd462379811554b8f0a99d7b65fce8d0da90c72b`).
Rama `acto/gen2-din-credito-prediccion-2024-commit-1`.

## 1 · Qué predice el programa de crédito 2024 — SIN ninguna cifra de 2024

**Ninguna variable de la sección de crédito de ENIF 2024 se abrió en este
acto** (PARO a, verificado: `data/raw/enif2024_csv.zip` nunca se leyó más
allá de su encabezado de columnas y su descriptor — spec.md de
-ADJUDICACION-0001 §1). Lo que sigue es qué predicen los cuatro
contendientes ya sellados, y qué tan bien habrían predicho cada ola
histórica si se les hubiera pedido — nunca qué midió 2024.

**Nueve conductas entran** (K1, K2-departamental/nómina/automotriz, K3,
K4A-autoexclusión, K4B-oferta, K5, K6-persona-tenedora), las mismas que
el encargo nombra menos `K7` (una sola ola comparable: no hay serie que
extrapolar) y `K2-bancaria`/`K8` (FP-404). Cuatro contendientes por
`(conducta, celda de eje)`: `PERSISTENCIA` (el valor de 2021 sin cambio),
`TENDENCIA-2`/`TENDENCIA-3`/`TENDENCIA-SERIE` (rectas en escala logit
sobre 2/3/todas las olas anteriores) — estos tres solo donde hay `>= 3`
olas comparables tras excluir celda rara (7 de 9 conductas; K4A/K4B se
quedan en solo-persistencia, 2 olas comparables).

**El hallazgo central, medido por backtest sobre las cuatro olas reales
ya selladas (2012/2015/2018/2021, historia pública, sin reserva) — «el
procedimiento corrido como si cada ola fuera la nueva» que el OBJETIVO
del encargo pedía:** `PERSISTENCIA` tiene el error medio más bajo en
**7 de 9** conductas. Solo `K1` (tenencia de cualquier crédito formal) y
`K6-P-TENEDORES` (atraso entre tenedores) favorecen `TENDENCIA-3`, y por
márgenes estrechos (K1: MAE de backtest 2.02 pp de tendencia contra 2.03
pp de persistencia — prácticamente empatados). En ninguna conducta una
tendencia gana por un margen que esta pieza llame «material»: no se fijó
un umbral de materialidad para el backtest a propósito (spec.md de
-EMISIONES §4) — inventar una constante que nadie va a usar para decidir
nada es justo lo que v2.16 §2 prohíbe.

**Lectura para mesa:** el programa, hoy, no tiene evidencia histórica de
que extrapolar una tendencia prediga mejor que simplemente cargar 2021
hacia adelante, en la gran mayoría de las conductas de crédito. Esto es
consistente con el patrón ya visto en `#972` (ENCIG: la tendencia tampoco
venció materialmente a persistencia — dictamen `SALTO-SIN-EXPLICAR`).
Cuando 2024 se abra (COMMIT-2/3, otra sesión), la pregunta que de verdad
se puede contestar es si ESTA vez el patrón se sostiene o si crédito se
comporta distinto a confianza en gobierno digital — no algo que este acto
pueda anticipar sin abrir el dato.

## 2 · Lo que se congeló (P0-P4)

- **P0** (FP-…-ff56-01/02): recorte 18-70 de ENIF 2021 (corrida propia,
  mismo medidor de `#943` importado por bytes) — commits `f1469f52`
  (COMMIT-1) / `17d27f82` (COMMIT-2); K2-bancaria histórica de `#975`
  corrida — commit `e6225e90`. Las dos FP quedan cerradas con corrida
  propia sellada cada una.
- **P1/P2 (emisiones)/P3**: `CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001`
  — commits `e7deeb39` (COMMIT-1) / `463163f5` (COMMIT-2). El backtest
  (§1 de aquí) es el oro/ensayo integrado en el mismo CALC.
- **P2 (adjudicación)**: `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`
  — commit `1960c5fe`, **congelado sin correr** (F3): guardia de una
  variable, mapa de columnas 2021→2024 desde el descriptor (A.15, con el
  hallazgo de nemónicos desplazados documentado en spec.md §1),
  extracción+estimación probada solo sobre sintético. `commit_3a`
  previsto en su propio `spec.yaml`.
- **P4**: esta nota; D-22 verificado (preflight VERDE en las cuatro
  piezas nuevas; sin NaN/inf; declarado==emitido byte a byte en las tres
  piezas que sí corrieron).

## 3 · Decisiones propias declaradas (no había mesa síncrona; se declaran
aquí para revisión, no se ocultan)

1. **«K6» del encargo = `K6-P-TENEDORES`, no `K6-PR`.** El encargo nombra
   «K6» sin sufijo; `#943` emite las dos, con unidad distinta (P vs PR).
   Se usó la de unidad P por ser la única consistente con el resto de la
   lista («cada marginal … se publica con K4(b) y K5 al lado» solo tiene
   sentido en la misma unidad). Declarado en spec.md de -EMISIONES §1.
   Si mesa prefiere K6-PR o ambas, es un sucesor de una línea.
2. **Umbral de `>= 3` olas comparables para T2/T3/T-serie**, no el
   mínimo de 2 que `tools/encig_origen_movil.py::MINIMO_OLAS` acepta por
   sí solo para T2/T-serie. Un ajuste de 2 puntos es degenerado (cero
   residuo, IC espurio); `#972` gatea su propio dictamen al mismo umbral.
   Un FALLA real de un test sintético (caso DOS-OLAS) atrapó que el
   primer medidor no implementaba este umbral pese a declararlo — se
   corrigió antes de sellar nada (ver commit `e7deeb39`, cuerpo).
3. **La regla de adjudicación (COMMIT-3) no se diseñó aquí.** El
   encargo mismo la difiere a COMMIT-3; forzar el contrato de
   `cruces_familia.py::adjudica()` (basado en réplicas bootstrap por
   celda) sobre esta serie (propagación analítica en logit) habría sido
   incoherente. Queda como decisión explícita de la sesión sucesora,
   con las dos cosas ya abiertas.
4. **`CREDITO-COMPARABILIDAD-TEXTO` se citó en v1.1**, no v1.0 (la que
   `#943` selló) — verificado que las 8 filas `ola=2021` son
   byte-idénticas entre ambas versiones antes de citar la más nueva.

## 4 · Hallazgos (una línea cada uno, `forense/hallazgos.md`)

- El sidecar de `#943` (`DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md.sha256`)
  usa la convención de nombre vieja que `sella_sha256.py` ya no reconoce
  — no es un sello roto, solo el nombre; fuera de perímetro re-sellarlo.

## 5 · FP/NC candidatas para mesa

- **FP-…-`<hhhh>`-01**: ¿mesa confirma `K6-P-TENEDORES` (no `K6-PR`) como
  la conducta K6 que entra al lote de predicción? (decisión §3.1 de
  aquí, latitud del encargo — se declara para ratificar o corregir).
- **FP-…-`<hhhh>`-02**: la regla de adjudicación de COMMIT-3 (§3.3 de
  aquí) — bootstrap sintético desde el SE analítico de -EMISIONES, o una
  regla puramente analítica sobre la diferencia de errores. Se pregunta
  cuando 2024 esté abierto, con las cifras reales delante, no antes.

## 6 · Sucesores

`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` COMMIT-2/3: abre
ENIF 2024 (una sesión distinta a esta, F3), extrae los marginales reales
de las 9 conductas, decide la regla de adjudicación (FP-02 de arriba) y
adjudica contra las emisiones ya selladas. `K6-PR` y `K7-*` quedan fuera
de este lote (§3.1, §1) — un sucesor explícito los retoma si mesa los
pide.
