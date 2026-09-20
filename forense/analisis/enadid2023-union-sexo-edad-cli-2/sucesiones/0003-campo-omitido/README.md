# CALC 0003 · corrección incompleta conservada

`CALC-ENADID2023-UNION-SEXO-EDAD-0003` permanece sellado. Corrigió
`n_denominador` de las cinco filas `peso_estandar_edad` al conteo conjunto
`152834`, pero el esquema `STD_COLUMNS` heredado no contenía
`n_numerador`. El serializador con `extrasaction="ignore"` omitió por ello el
conteo de cada tramo que el medidor ya había construido.

Se conserva aquí la tabla emitida por 0003 antes de que 0004 la suceda. No
cambió ningún punto, masa, réplica, error estándar ni intervalo respecto de
0002. 0004 añade la columna omitida; no reabre ni altera el sello de 0003.
