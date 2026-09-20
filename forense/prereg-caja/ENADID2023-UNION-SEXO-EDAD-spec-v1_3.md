# Sucesión de contrato · serialización de conteos estándar

`CALC-ENADID2023-UNION-SEXO-EDAD-0004` sucede a la corrida sellada 0003.
0003 calculó el conteo de cada tramo como `n_numerador` y el conjunto de los
cinco tramos como `n_denominador`, pero el esquema heredado `STD_COLUMNS` no
incluía `n_numerador`; `csv.DictWriter(extrasaction="ignore")` lo omitió de la
tabla publicada.

0004 añade exclusivamente `n_numerador` a `STD_COLUMNS`. Se conservan 0002,
0003, sus sellos y la tabla emitida por 0003. No cambian universo, filtros,
masas, pesos, puntos, tasas, diferencias, réplicas, semilla, covarianza,
intervalos, singleton, degeneraciones ni tolerancia. Los RESULT reciben
identidades `RESULT-ENADID-USE4-*`; no hay adopción y
`cuenta_gen2=PENDIENTE-DE-MESA`.
