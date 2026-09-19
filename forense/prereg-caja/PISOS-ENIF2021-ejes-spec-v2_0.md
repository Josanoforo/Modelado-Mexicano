# PISOS ENIF 2021 por ejes v2.0

Sucesor de `CALC-PISOS-ENIF2021-EJES-0001`. Los datos ya fueron vistos en
#866. Mide solo ahorro solo informal D9: alguna `P5_1_1..6=1` y ninguna
`P5_7_1..9=1`. `P5_7` conserva el ahorro formal; la tenencia de cuenta se
deriva de `P5_4_1..9`. `P5_6` no se usa: en 2021 mide tarjeta de debito.

Edad excluye 97, 98, 99 y tiene 18--29 / 30--44 / 45--59 / 60--96.
Escolaridad agrupa `P3_1_1` como 00--02 / 03 / 04--07 / 08--11 y excluye 99.
Localidad agrupa `TLOC {3,4}` como menos de 15 mil y `{1,2}` como 15 mil y
mas. Sexo conserva 1/2. Unidad persona elegida, peso `FAC_ELE`, estrato
`EST_DIS`, UPM `UPM_DIS`; bootstrap de UPM dentro de estrato, 10 000 replicas,
PCG64 seed 42. Cada celda emite punto, IC95, n y denominador ponderado como
RESULT numericos. El IC es muestral de 2021, no predictivo de 2024.
