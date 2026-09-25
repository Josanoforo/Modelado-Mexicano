# DONDE-CAMBIO · spec v1.0 · vocabulario, umbrales y reglas de dictamen (COMMIT-1)

ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1 · 24/sep/2026 · encargo
`forense/encargos/2026-09-24-GEN2-DONDE-CAMBIO-EL-MEXICANO-1.md` (0-bis `96ee84fd`).
Generación GEN2 · `cuenta_gen2: SI` · `adopta: NO` · todo lo que produce es **RETROSPECTIVA**
(v2.16 §4): ninguna ola evaluada es posterior al sello de ninguna emisión.

El primer resultado que produzca este procedimiento es el que se reporta.

## §0 · Exposición declarada antes de este commit

Esta sesión leyó, antes de congelar: el encargo; los métodos (no los resultados) de
`ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md`, `ENCIG-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md` y
`ENOE-PERSISTENCIA-spec-v1_0.md`; la lista de CALC en `data/corrida0`; y las columnas NO numéricas
de `canon/catalogo-del-mexicano-v1_0.tsv` (dominio, estado, temporalidad, instrumento_ola, ids de
RESULT). **Ningún valor** (punto, IC, τ², cobertura) de ninguna serie ni piso. Un subagente de
inventario imprimió por error en su propia terminal valores de IC del catálogo; no los transmitió a
esta sesión (declarado, A.13/ADR-46: la sesión ejecutora no los vio).

## §1 · Unidad: la serie

Una **serie** es `(instrumento, conducta, eje, segmento)` con sus olas `w1 < … < wk`, cada una con
un RESULT sellado de punto `p` y de IC95 muestral `[lo, hi]`, misma unidad y mismo denominador
(v2.16 §4: nunca se mezclan unidades persona/hogar/delito/trámite). La tabla de series
(`DONDE-CAMBIO-mapa-series-v1_0.tsv`) lista sólo **ids de RESULT**, nunca valores; se congela
por hash antes de que el medidor lea un solo valor.

**Universo (P2).** Toda conducta con RESULT en el catálogo U1 o en las series selladas nombradas
por el encargo, en cualquier instrumento, que tenga RESULT en ≥ 2 olas. Una conducta con RESULT en
una sola ola se lista y se dictamina `SIN-SERIE` sin más lectura. Olas **RESERVADAS** en
`data/manifiesto.yaml` (y ENIF 2024, ENVIPE 2025, ENCIG 2025, ENUT 2024 y cualquier ola que el
manifiesto marque así) no se abren: sólo entran si ya existe un RESULT sellado de esa ola en
`data/corrida0` producido por el código autorizado (E.6: «un cruce visto sirve para describir… en
retrospectiva»); si no existe, la ola no cuenta.

## §2 · Comparabilidad del par (por texto, nunca por magnitud)

Cada par de olas consecutivas `(a, b)` de la serie lleva un estado documental, leído de una fuente
escrita **antes** de este acto (tabla `data/*comparabilidad*`, spec sellada de la serie, o dictamen
sellado como #972), con su cita:

- `COMPARABLE` — MISMO-INSTRUMENTO o CAMBIO-MENOR en la fuente.
- `CAMBIO-DOCUMENTADO` — cambio de cuestionario, modo o diseño citado por texto
  (CAMBIO-DE-INSTRUMENTO, ruptura, cambio de marco/era, NO-ESTIMABLE-RUPTURA-ESTRUCTURAL).
- `NO-DOCUMENTADO` — ninguna fuente escrita dictamina el par. **No se presume comparable:**
  el par corta la serie (A.15, «nadie corrió el mecanismo» ≠ «es comparable»).
- `NO-COMPARABLE` — la fuente dice que el constructo no es el mismo; corta la serie.

El tramo evaluable es la **corrida más larga** de olas consecutivas unidas por pares
`COMPARABLE` o `CAMBIO-DOCUMENTADO` (desempate: la más reciente). `k` = número de olas del tramo
con `p`, `lo`, `hi` estrictamente en (0, 1).

## §3 · IC calibrado de persistencia (P3)

Para el par `(a, b)`: `Δ = logit p_b − logit p_a`; `ee_a = (logit hi_a − logit lo_a)/(2·1.959964)`;
el piso `t−1` **cubre** a `t` si
`p_b ∈ expit( logit p_a ± 1.959964 · √(ee_a² + τ²) )`. Si no, el par está **FUERA**, con
dirección `signo(Δ)`.

`τ²` es el parámetro de persistencia **del instrumento por eje** (`τ²_{I,e}`):

1. **ENIF** — sellado #1009 (`CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`): para el eje `e`,
   la media de τ² de sus dos desenlaces en `e`; eje no cubierto → media de los doce τ².
2. **ENCIG** — sellado #1041 (`CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001`): `TAU2-FINAL` del
   eje `e`; eje no cubierto (incluido NACIONAL) → media de los tres.
3. **Resto** (ENVIPE, ENUT, ENIGH, ENOE, ENDIREH, MOCIBA) — se calcula aquí con **el mismo
   método** y se emite como RESULT reutilizable: para cada eje `e`, media entre pares (peso igual
   por par de olas) de la media, dentro del par, de `Δ²` sobre todas las series `COMPARABLE` del
   instrumento en `e`. Sin centrar y sin restar ruido muestral (igual que #1009/#1041). Eje sin
   ningún Δ → media de los ejes del instrumento; instrumento sin ningún Δ → `NO-CALIBRABLE` y sus
   series se dictaminan `SIN-SERIE` con causa.

Pares `CAMBIO-DOCUMENTADO` **no** entran al cálculo de τ² (son los que se quieren detectar).
Declarado, no corregido: τ² incluye los pares que después se juzgan, lo que empuja el dictamen
hacia `ESTABLE` — un `CAMBIO-SOSTENIDO` aquí es conservador. ENOE: su spec sellada declara que el
IC predictivo no es estimable por el panel rotatorio; aquí τ² es sólo el segundo momento empírico
del cambio (lo que el método es), con esa reserva escrita en cada fila ENOE
(`SIN-COVARIANZA-LONGITUDINAL`). ENOE sólo se evalúa dentro de era, con los pares que su spec
sellada admite.

## §4 · Vocabulario cerrado y orden de desempate (B-bis)

Se aplica la **primera** regla que se cumpla, sobre el tramo evaluable:

1. `SIN-SERIE` — `k < 3`.
2. `CAMBIO-SOSTENIDO` — ≥ 2 pares `COMPARABLE` FUERA en la misma dirección, y esa dirección tiene
   estrictamente más pares `COMPARABLE` FUERA que la contraria. Se emite la dirección
   (`SUBE`/`BAJA`) y la magnitud acumulada `p_wk − p_w1` en pp.
3. `SALTO-DE-INSTRUMENTO` — ≥ 1 par `CAMBIO-DOCUMENTADO` FUERA (con su cita).
4. `SALTO-SIN-EXPLICAR` — ≥ 1 par `COMPARABLE` FUERA sin cumplir la regla 2.
5. `ESTABLE` — todos los pares del tramo cubiertos.

**Interpretación declarada (cláusula de autonomía 2 y 3, PROPUESTO-POR-EJECUTOR):** el encargo
fija cuatro palabras y exige «0 filas sin dictamen». Un único par fuera sin cambio documentado no
es ESTABLE (no cubre), ni SOSTENIDO (un par), ni SALTO-DE-INSTRUMENTO (sin cita): con cuatro
palabras quedaría sin dictamen. Se añade la quinta, `SALTO-SIN-EXPLICAR`, que es el término ya
sellado por #972 (ENCIG 2017→2019). La línea-resumen reporta las cinco.

«Pares consecutivos» se lee como pares de olas consecutivas del tramo; los dos pares FUERA no
necesitan ser adyacentes entre sí.

## §5 · Marcas de auditoría (no cambian el dictamen)

- `PAR-2020`: el par toca una ola levantada o referida a 2020 (crisis sanitaria). Todo
  `CAMBIO-SOSTENIDO` o `SALTO-*` cuyo único par FUERA en su dirección toca 2020 se lista en el
  módulo de auditoría como **estructura o crisis, no cultura** candidata.
- `IC-SIN-CALIBRACION-ACREDITADA`: el IC muestral del piso viene rotulado así en el catálogo.
- Magnitud de cada par en pp (`100·(p_b − p_a)`), con la unidad de la serie.

## §6 · Salidas

Por instrumento, un CALC `CALC-<INST>-SERIE-DICTAMEN-0001` que consume RESULT sellados por hash
(sin microdato): τ²_{I,e} (sólo instrumentos del punto 3), y por serie: `K`, `N-FUERA`,
`DICTAMEN` (texto del vocabulario), `DIRECCION`, `DELTA-PP` acumulado. `verify` con tolerancia
absoluta 1e-10. La tabla `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv` (una fila por
serie) y el documento `canon/donde-cambio-el-mexicano-v1_0.md` citan sólo RESULT de estos CALC o
de los sellados; test: 0 cifras sin RESULT.

## §7 · Lo que no hace

No predice, no adopta, no mueve `celdas_validadas`, no re-mide series selladas (E.5), no abre
microdato, no abre olas reservadas. No atribuye causa: «cambió» es un hecho de la serie, no de la
psicología (v2.16 §3).

El primer resultado que produzca este procedimiento es el que se reporta.
