# PISOS ENCIG 2023 por ejes v2.0

Sucesor de `CALC-PISOS-ENCIG2023-EJES-0001-v1_1`. Los datos ya fueron vistos
en #866. El universo comparable exige `N_TRA=01` y `P7_3 in {1,2,4,5,6}`;
el numerador digital util es `P7_3 in {4,5}`. Los codigos 3, 7, 8, 9 y blanco
no se convierten en ceros.

Edad tiene cuatro categorias con limite efectivo 96. Escolaridad agrupa `NIV`
como 0--2 / 3 / 4--7 / 8--9. Sexo conserva 1/2. Unidad tramite, peso
`FAC_TRA`, estrato `EST_DIS`, UPM `UPM_DIS`; bootstrap de UPM dentro de
estrato, 10 000 replicas, PCG64 seed 42. Cada celda emite punto, IC95, n y
denominador ponderado como RESULT numericos. El IC es muestral de 2023.
