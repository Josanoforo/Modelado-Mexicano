# PREDICCIÓN 2024 · emisiones marginales de crédito · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1 (21/sep/2026, CAJA), piezas
P1/P2/P3 (P0 ya cerrado: FP-…-ff56-01/02, commits `f1469f52`/`17d27f82`/
`e6225e90`). CALC: `CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001`.
Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1.md`
(sha256 `b3c62b4a7ed4bf65175c795fdd462379811554b8f0a99d7b65fce8d0da90c72b`).
Compuerta única (protege: abrir dato): esta spec, `spec.yaml` y
`medidor.py` congelados en este COMMIT-1, con el sidecar verificado, antes
de correr sobre los pisos sellados (COMMIT-2, misma sesión — este CALC
nunca abre ENIF 2024, así que no hay reserva que proteger aquí; la
compuerta es sobre el procedimiento, no sobre el dato).

## 0 · Qué es y qué NO es este CALC

**No abre ENIF 2024 en ninguna forma** (PARO a del encargo). Toda su
entrada son `RESULT-` ya sellados de los cuatro pisos de crédito
(`CALC-DIN-CREDITO-PISOS-ENIF2012-0001`, `-2015-0001`, `-2018-0001` —
sellados por `#932`/`#943` — y `CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`,
sellado por este mismo acto en P0-a) más el medidor determinista sellado
de `#972` (`tools/encig_origen_movil.py`), importado por bytes (sha256).
Aritmética entre sellados, escala logit: cero microdato, cero réplica
bootstrap propia.

**Universo: 18-70 en las cuatro olas** — por eso P0-a existe: sin el
recorte, la ola 2021 no sería conmensurable con 2012/2015/2018.

**Lo que SÍ produce:** para cada conducta que el encargo declara entrando
(§1) y cada una de las 18 celdas de eje ya selladas en los cuatro pisos
(`NACIONAL-TODOS` + 14 categorías de sexo/edad/escolaridad/localidad/cuenta
+ 2 de formalidad + `UNIVERSO-TRABAJA`), CUATRO contendientes —
`PERSISTENCIA`, `TENDENCIA-2`, `TENDENCIA-3`, `TENDENCIA-SERIE` — para
CADA año objetivo en `{2015, 2018, 2021, 2024}`: los tres primeros son
**backtest** (se comparan contra el valor real ya sellado de esa ola,
P3/oro, §4); `2024` es la **emisión prospectiva** (sin valor real: nadie
la ha medido, y este acto no la mide).

**Lo que NO produce:** ninguna cifra de ENIF 2024; ninguna adjudicación
(elegir un contendiente ganador) — eso exige el valor real de 2024, que
está reservado; ninguna composición de cruces (`C2`, dos ejes a la vez) —
el encargo lo declara para `COMMIT-3` (§3 del encargo: «C2 no existe hasta
abrir los marginales… se compone dentro del COMMIT-3»); este CALC produce
los marginales de los que C2 se compondrá, no C2 mismo.

## 1 · Alcance (P1) — conductas que entran y por qué

Entran, con unidad P (persona) consistente entre sí — «oferta antes que
preferencia» (v2.16 §3): `K1`, `K2-DEPARTAMENTAL`, `K2-NOMINA`,
`K2-AUTOMOTRIZ` («K2-no-bancaria»: la familia bancaria de K2 queda fuera,
FP-404, medida aparte en `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001`),
`K3`, `K4A-AUTOEXCLUSION`, `K4B-OFERTA`, `K5`, `K6-P-TENEDORES`.

**Decisión declarada (no hay ambigüedad que preguntar a mesa: se deriva
del propio contrato de unidad).** El encargo nombra «K6» sin sufijo; el
medidor de pisos (`#943`) emite DOS variantes con unidad distinta:
`K6-PR` (unidad **PR**, una fila por producto tenido) y
`K6-P-TENEDORES` (unidad **P**, agregable a P — así lo declara
`data/credito-comparabilidad-texto-v1_1.tsv`). Esta spec usa
`K6-P-TENEDORES`: es la única de las dos que comparte unidad con el resto
de la lista («cada marginal de K1–K3 se publica con K4(b) y K5 al lado» —
frase que sólo tiene sentido si todo está en la misma unidad). `K6-PR`
queda fuera de este CALC; no hay pérdida — es agregable desde
`K6-P-TENEDORES` más el conteo de productos, que sigue sellado en cada
piso.

**No entran** (y por qué, verificado por objeto contra los cuatro pisos
sellados, no por prosa):
- `K7-*` (canal del último crédito): sólo tiene celda sellada en 2021 (0
  puntos previos comparables — `data/credito-comparabilidad-texto-v1_1.tsv`
  fila K7 declara `NO-ESTIMABLE` en 2012/2015/2018) — con 1 sola ola,
  únicamente `PERSISTENCIA` sería computable y el resultado sería
  indistinguible de citar el sellado de 2021 sin aritmética nueva; no
  aporta sobre lo ya sellado.
- `K8`, `K2-bancaria`: FP-404 firmada, fuera de la serie entera; ningún
  piso las mide, incluido 2021.
- `K5-ENTRE-SOLICITANTES`, `K6-PR`, `K4B1/K4B2/K4B3` (sub-cortes de
  `K4B-OFERTA`): existen selladas en los pisos pero el encargo no las
  nombra entre las que entran; quedan disponibles para un sucesor que las
  pida explícitamente.

## 2 · Contendientes y la compuerta de comparabilidad (P1)

Por `(conducta, celda)`, la serie es de hasta 4 puntos (2012, 2015, 2018,
2021), leída de los `RESULT-` ya sellados de cada piso. **Celda rara**: si
el IC95 sellado de una ola tiene límite inferior `<= 0` o superior
`>= 1`, el logit es indefinido — esa ola se **excluye** de la serie para
esa `(conducta, celda)` (nunca se inventa un valor) y queda declarada en
`-CELDAS-RARAS-EXCLUIDAS`. Medido contra los cuatro pisos ya sellados: 4
celdas caen en este caso dentro de las conductas que entran aquí (las
tres de `K2-AUTOMOTRIZ` en 2012 —`CUENTA-SIN-CUENTA`, `ESCOLARIDAD-HASTA-PRIMARIA`
con `P=0` exacto, `LOCALIDAD-MENOR-DE-15-000`— y una de `K2-NOMINA` en
2021, `CUENTA-SIN-CUENTA`); las otras 4 celdas raras del corpus (`K4B2`,
`K7-*`) son de conductas que no entran aquí.

**Contendientes, por número de puntos usables tras filtrar celdas raras**
(mínimos de `tools/encig_origen_movil.py::MINIMO_OLAS`, importados sin
cambio): `PERSISTENCIA` con `>= 1` punto (siempre disponible: toda celda
de toda conducta que entra tiene al menos su valor 2021 sellado).
`TENDENCIA-2`/`TENDENCIA-SERIE` técnicamente aceptarían 2 puntos, pero
**esta spec exige `>= 3` para cualquier contendiente de tendencia** —
la razón textual del encargo («T-serie solo donde la comparabilidad dé >=
3 puntos») se aplica a los tres, no sólo a T-serie: un ajuste OLS de 2
puntos es degenerado (interpola exacto, cero residuo, IC espurio) y el
propio `#972` gatea su dictamen completo al mismo umbral
(`n_comp < 3 → NO-DECIDIBLE`). `TENDENCIA-3` exige además que, de esos
`>= 3`, al menos 3 sean los inmediatamente anteriores al año objetivo.

Derivado por objeto (no tecleado) contra los cuatro pisos sellados y el
filtro de celda rara: `K1`, `K2-DEPARTAMENTAL`, `K2-NOMINA`,
`K2-AUTOMOTRIZ`, `K3`, `K5`, `K6-P-TENEDORES` tienen sus 4 olas selladas
en TODAS las 18 celdas (mínimo 3 tras excluir celda rara donde aplica) →
los cuatro contendientes entran. `K4A-AUTOEXCLUSION`, `K4B-OFERTA` sólo
están selladas en 2018 y 2021 (2012/2015: `CAMBIO-DE-INSTRUMENTO`, ningún
piso las midió) → 2 puntos, bajo el umbral de 3 → **sólo `PERSISTENCIA`**.

## 3 · Procedimiento (P2, congelado)

Por `(conducta, celda, año objetivo ∈ {2015, 2018, 2021, 2024})`: la
serie previa es la sub-serie con año `< objetivo`; para cada contendiente
con datos suficientes, `tools/encig_origen_movil.py::predice` (importado
por bytes) da `{p, lo, hi}` en escala logit convertida a proporción.
`PERSISTENCIA` hereda el IC95 sellado de la última ola verbatim; los
tres de tendencia propagan varianza analítica:
`var = Σ w_i² ee_i²` sobre los pesos OLS cerrados de `pesos()`. Si el año
objetivo tiene un valor real ya sellado (2015/2018/2021, nunca 2024), se
emite además `-ERROR-PP` (predicción menos real, pp) y `-CUBRE` (SI/NO,
real dentro del IC95 de la predicción) — esto es el **backtest**, no una
adjudicación: no hay regla de veredicto (`VENCE`/`PROPUESTA-CON-RESERVA`),
sólo el error medido, porque el objetivo aquí es «qué tan bien habría
predicho este contendiente la ola siguiente», sobre el dato ya sellado
libremente, no sobre una reserva.

**Nulos declarados (D-22 punto 3):** toda combinación `(conducta, celda,
año, contendiente)` sin datos suficientes emite sus tres campos
(`-P`, `-IC-LO`, `-IC-HI`) con valor `None`, nunca los omite. `-ERROR-PP`/
`-CUBRE` son `None` para `año=2024` (no hay real) y para cualquier
contendiente sin predicción. Ningún valor no finito (NaN, inf) es
alcanzable: la conversión logit↔proporción está definida en todo el rango
`(0,1)` abierto, que es exactamente lo que el filtro de celda rara
protege (§2).

## 4 · P3 — Ensayo y oro (D-22 punto 2, «sobre sintético y sobre oro»)

**Sintético** (antes de abrir ningún sellado real):
`tests/test_din_credito_prediccion_2024_emisiones.py` fabrica series de
proporciones inventadas — 1, 2, 3 y 4 puntos; una serie con celda rara
deliberada (`lo=0.0` exacto); una con las cuatro olas — y corre
`medir()` sobre inputs sintéticos completos (los cuatro `PISO-*` son
JSON fabricados, no los reales) para probar cada rama terminal: sin datos
(`None` declarado), sólo persistencia (2 puntos, bajo el umbral de 3),
los cuatro contendientes (4 puntos), y la celda rara excluida sin que el
medidor reviente.

**Oro:** el propio backtest de §3, corrido sobre los CUATRO PISOS REALES
ya sellados (que no son un dato nuevo: son historia pública 2012-2021,
nada reservado), ES el oro de este procedimiento — «el procedimiento
corrido como si 2021 (o 2018, o 2015) fuera la ola nueva» que el encargo
pide en su OBJETIVO. Resultado real (COMMIT-2 de esta pieza, ver nota de
cierre): `PERSISTENCIA` tiene el MAE de backtest más bajo en 7 de 9
conductas con backtest definido (K4A/K4B sólo tienen backtest en el
objetivo 2021, con un único punto previo — 2018 —, así que sólo
`PERSISTENCIA` corre ahí también); ninguna tendencia lo vence por un
margen que esta spec declare «material» — deliberadamente esta spec NO
fija un umbral de materialidad para el backtest (a diferencia de la
adjudicación real contra 2024, que si lo necesitará): inventar una
constante de corte que nadie va a usar para decidir nada es exactamente
lo que v2.16 §2 prohíbe («ninguna cifra esperada se teclea»). El
`MEJOR-CONTENDIENTE-BACKTEST` por conducta se reporta tal cual, sin
adjudicar.

## 5 · Lo que esta spec no hace

No abre ENIF 2024; no adjudica (`VENCE`/`PROPUESTA-CON-RESERVA` exige el
valor real 2024, reservado); no compone `C2` (COMMIT-3, otra sesión); no
edita `#943`, `#972` ni ningún CALC sellado; no fija el código guardado
de una sola variable para la apertura futura de 2024 (eso es
`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`, congelado aparte,
sin ejecutar — P2 del encargo, `commit_3a` previsto en su propio
`spec.yaml`); no adopta (`cuenta_gen2 = SI`, cuenta y no adopta).
