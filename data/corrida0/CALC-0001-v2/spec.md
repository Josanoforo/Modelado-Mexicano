# `CALC-0001-v2` — composición de alineamiento entre receptores CSES 2015

Ejecuta `prereg-caja-S12` v1.2. Sucede a `CALC-0001`, cuyo `NO-ESTIMABLE` se conserva: esta corrida responde otra pregunta y no reemplaza el contraste receptor/no receptor.

## Contrato congelado

Fuente: CIDE-CSES 2015 nacional poselectoral, 1,200 adultos. Oferta (`pcyc13=1`) y amenaza (`pcyc14=1`) se procesan por separado. El partido señalado (`pcyc13_1`/`pcyc14_1`) se cruza con el voto a diputados (`peledip`) mediante el crosswalk sellado en S12 v1.2; no se comparan códigos directamente.

Por rama, el estimando es la composición ponderada entre `ALINEADO` y `NO-ALINEADO`, y `Δ_comp=P(ALINEADO)-P(NO-ALINEADO)`. Se publican tamaños brutos y ponderados, intervalos por grupo y del contraste. Bootstrap de UPM `upmmn` dentro de `dominio`, 2,000 réplicas, PCG64, semilla 20260910.

Los receptores sin partido contraparte resoluble, voto, peso positivo, estrato o UPM se excluyen y cuentan. Si una categoría tiene menos de 10 casos se rotula `LIMITADA-N-MENOR-10`; el intervalo se publica, pero no sustenta una generalización. Esta corrida es descriptiva/asociativa, no causal, no mueve tiers ni añade tasas al motor.

## Validación independiente prevista

Después del sello, una segunda vía leerá directamente el `.sav` y hará tabulación/cocientes ponderados sin importar `medidor.py`. Debe coincidir exactamente en los conteos brutos y dentro de `1e-12` en numerador, denominador y proporción decisivos. El bootstrap se valida por `verify`, no duplicando su función.
