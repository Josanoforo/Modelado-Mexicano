# PISOS ENIF 2021 · recorte 18-70 · conductas de crédito K1–K7 por ejes · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1 (21/sep/2026, CAJA), pieza P0
(FP-…-ff56-01: «el sucesor inmediato corre el mismo medidor de `#943` sobre
ENIF 2021 con recorte 18-70, como corrida propia, para conmensurar con
2012/2015/2018; 2021 sigue siendo la ola de referencia del lote»). CALC:
`CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`. Encargo archivado por A.3
en `forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1.md`
(sha256 `b3c62b4a7ed4bf65175c795fdd462379811554b8f0a99d7b65fce8d0da90c72b`).
Compuerta única (protege: abrir dato): esta spec, `spec.yaml` y `medidor.py`
congelados en este COMMIT-1, con el sidecar verificado, antes de tocar
`TMODULO` de 2021.

## 0 · Delta declarado contra la spec madre — no se repite lo que no cambia

Esta spec es un RECORTE de universo sobre el procedimiento ya congelado y
sellado en `forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md`
(`CALC-DIN-CREDITO-PISOS-ENIF2021-0001`, `#943`, sellado, universo 18+). Todo
lo que esa spec declara — alcance §1, desenlaces §2, ejes y rejilla §3,
marco de diseño y guardias §4, diagnóstico §5 — **se hereda verbatim y no se
repite aquí**; esta spec sólo documenta el único cambio:

- **Universo: `EDAD` (numérica, columna `EDAD` de `TModulo`) restringida a
  `[18, 70]` inclusive**, aplicada **antes** de construir ejes, celdas o
  cualquier desenlace — es decir, antes de que `_age` (importado de -0003)
  bucketice la edad para el eje `edad`. Personas con `EDAD` fuera de ese
  rango (incluidos los centinelas de no-sabe/no-aplica que el propio
  `pd.to_numeric(..., errors="coerce")` deja fuera de `[18,70]`) **no entran
  a ningún desenlace, a ninguna celda, a ningún denominador** — no es un
  filtro de un eje entre varios: recorta el universo entero de la corrida,
  igual que 2012/2015/2018 lo traen recortado por diseño del propio
  cuestionario INEGI (`data/credito-comparabilidad-texto-v1_1.tsv`, filas
  K1/K3 · ola 2012 y 2015: «Persona elegida de 18 a 70 años»).
- **Por qué:** ENIF 2021 (y 2024) preguntan a personas elegidas de 18 años y
  más SIN tope superior (FD 2021 TModulo fila 1502: `EDAD 18-96`); 2012,
  2015 y 2018 preguntan sólo a 18-70. Comparar el piso 18+ de 2021 (`#943`)
  contra los tres pisos anteriores 18-70 mezcla dos universos distintos en
  la misma serie — el recorte de esta spec hace que las cuatro olas
  históricas (2012/2015/2018/2021-recortado) compartan universo antes de
  entrar como contendiente «persistencia» o «tendencia» al COMMIT-2/3 de
  predicción 2024.
- **Lo que NO cambia:** las 14 conductas y sus 20 desenlaces (§1-2 de la
  spec madre), los cinco ejes + formalidad y sus cortes (§3, importados
  **byte a byte** del mismo medidor sellado de `CALC-PISOS-ENIF2021-EJES-0003`
  que usa `#943`), el marco de diseño (`FAC_ELE`, `EST_DIS × UPM_DIS`,
  10 000 réplicas `PCG64(42)`, un solo plan de réplicas), las tres guardias
  (unidad, soporte `n < 200`, coherencia `1e-6`), K8 y K2-bancaria fuera
  (FP-404), el par «crédito por app» fuera (reserva 20/sep). El código de
  `#943` (`CALC-DIN-CREDITO-PISOS-ENIF2021-0001/medidor.py`, sha256
  `a8f97e4c87e473e9923055e1d434262cb87fc68c15122c953632c6553db97a8a`) se
  **importa por bytes, sin copiar ni editar una sola línea de su lógica de
  conducta**: el `medidor.py` de este CALC ejecuta ese módulo verbatim,
  wrappeando únicamente el punto donde carga el CSV (para aplicar el
  recorte de edad antes de que nada más lo lea) y el nombre `PREFIJO` (para
  que los `RESULT-` de esta corrida no colisionen con los ya sellados de
  `#943`, que son otra medición, sobre otro universo). Verificable: un
  `diff` de la lógica de conducta es un `diff` vacío porque no hay una
  segunda copia — hay una sola, importada.

## 1 · Exposición declarada (ADR-46)

Ídem `DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md` §0: nada nuevo se lee del
microdato de 2021 ni de 2024 antes de congelar. El payload sintético de D-22
lo fabrica `tests/test_din_credito_pisos_enif2021_recorte1870.py`
(reutiliza `payload_sintetico()` de `tests/test_din_credito_pisos_enif2021.py`,
que ya incluye edades `randint(18, 97)` — el recorte se ejerce sobre ese
mismo generador, sin uno nuevo). Cifra esperada: ninguna.

## 2 · Procedimiento congelado (P3, P4)

Idéntico a la spec madre §4, con el filtro de universo de §0 aplicado en el
primer paso (dentro de la función que carga el CSV, antes de calcular
`_w`/`_est`/`_upm`/ejes/desenlaces). Guardias 1-3 (unidad, soporte,
coherencia) corren **sobre la población ya recortada** — la coherencia
verifica que las celdas de cada eje sumen al nacional **de ese universo
recortado**, no al de `#943`.

## 3 · Ejes y rejilla, desenlaces, diagnóstico

Idénticos a la spec madre §2, §3, §5 — se leen ahí, no se copian aquí (D-15:
esta spec basta para recalcular junto con la madre citada, sin abrir el
código).

## 4 · Oro (P3 del encargo)

El encargo (§1) pide que «el procedimiento corrido como si 2021 fuera la
ola nueva reproduzca `#943` (18+)». Ese oro se satisface por construcción:
si `EDAD_MIN=18, EDAD_MAX=96` (el rango completo de la variable en 2021), el
filtro de §0 no excluye a nadie y `medir()` de este CALC — que es el mismo
`medir()` de `#943`, byte a byte, sólo con el marco pre-filtrado —
reproduce sus RESULT- exactamente (mismo código, mismo input, mismo
universo). Esta identidad se verifica en
`tests/test_din_credito_pisos_enif2021_recorte1870.py` sobre el payload
sintético: correr el wrapper con `[18,96]` contra correr `#943` sin
wrapper, mismo payload, misma semilla → salidas idénticas. La corrida real
de este CALC usa `[18,70]`, que es el recorte pedido, no el oro.

## 5 · Lo que esta spec no hace

No abre ENIF 2024; no adjudica ni corona; no escribe reglas en el motor; no
mide K8 ni K2-bancaria; no edita `#943` ni ninguna spec, tabla de identidad
o CALC sellado; no adopta (`cuenta_gen2 = SI`, cuenta y no adopta, misma
firma que `#943`).
