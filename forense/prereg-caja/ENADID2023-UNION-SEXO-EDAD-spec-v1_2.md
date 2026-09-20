# Sucesión de contrato · conteos de pesos estándar

`CALC-ENADID2023-UNION-SEXO-EDAD-0003` sucede a la corrida sellada
`CALC-ENADID2023-UNION-SEXO-EDAD-0002` por una corrección material de
semántica tabular detectada después de publicar 0002.

En 0002, cada fila `peso_estandar_edad` publicó en `n_denominador` el número
de personas del tramo, aunque `masa_denominador` era correctamente la masa
conjunta del universo de los cinco tramos. El peso, calculado como masa del
tramo entre masa conjunta, y toda su incertidumbre fueron correctos.

0003 cambia exclusivamente esos dos campos de conteo:

1. `n_numerador`: personas del tramo, con sexo conocido, edad válida y
   `P3_27∈{1,6}`;
2. `n_denominador`: personas conjuntas de los cinco tramos en el mismo
   universo.

Se conservan 0002, su sello y sus resultados. No cambian código estadístico,
universo, filtros, masas, puntos, pesos estándar, tasas, diferencias,
réplicas, semilla, covarianza, intervalos, tratamiento de singleton,
degeneraciones ni tolerancia. La prueba sintética exige que la suma de los
cinco `n_numerador` sea el `n_denominador` común. Los RESULT de 0003 reciben
identidades `RESULT-ENADID-USE3-*`; no hay adopción y
`cuenta_gen2=PENDIENTE-DE-MESA`.
