# ENSAFI 2023 · estrategias conjuntas ante insuficiencia · spec v1.0

Congelada antes de abrir las respuestas de `TMODULO.csv`. Es una extensión de
`CALC-ENSAFI-DISENO-0001`, no una reedición de sus ocho marginales. Se conocían
esas marginales, por lo que el análisis no es ciego.

Universo: persona elegida de 18 años y más con `P6_9=2`. Las ocho estrategias
son `P6_10_1..8`; solamente `1=si` y `2=no` son respuestas válidas. Blanco,
especial, fuera de salto y cualquier otro código es desconocido, nunca `no`.
`FAC_ELE` pondera personas; `EST_DIS×UPM_DIS` define el diseño. La muestra
completa se conserva para la linealización y lo que quede fuera de cada dominio
aporta cero. Sin FPC; el IC es t bilateral 95% con gl de diseño. Singleton no
aporta varianza ni gl y se declara. En frontera o con diseño faltante no se
acredita EE/IC cero.

Se emiten: (a) cobertura y número de respuestas desconocidas; (b) partición
ponderada del conteo 0..8, su media y umbrales; (c) las 28 tablas 2×2, ambas y
condicionales entre vector completo; (d) la sensibilidad al dominio donde sólo
la pareja es válida, con diferencia e IC por influencia conjunta; y (e) límites
de identificación por faltantes para los tres umbrales. Los límites no son IC.
Controles: la partición suma uno, la media coincide con la suma marginal,
las 2×2 reconstruyen sus márgenes y las marginales reproducen exactamente los
denominadores del padre. No se llama índice de estrés/severidad, no se infiere
secuencia/causalidad/producto de deuda y no se modifica ningún consumidor.
