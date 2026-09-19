# PISOS ENVIPE 2024 por ejes v2.0

Sucesor de `CALC-PISOS-ENVIPE2024-EJES-0001`. Los datos ya fueron vistos en
la medicion defectuosa de #866; este correctivo se congela antes de ejecutar
su sucesor, no reclama ceguera nueva.

Evasion usa solamente delitos con `BP1_20 in {1,2}` y define el evento como
`BP1_20=2 and BP1_23 in {04,05,06,08}`. Edad tiene cuatro categorias y limite
efectivo 96. Escolaridad agrupa `NIV` como 00--02 / 03 / 04--07 / 08--09.
Dominio conserva R/C/U. Denuncia usa su universo propio: `BPCOD=01`,
`BP2_1 in {1,2}`, con evento `BP1_20=1`, por no asegurado/asegurado.

Unidad delito, peso `FAC_DEL`, estrato `EST_DIS`, UPM `UPM_DIS`; bootstrap de
UPM dentro de estrato, 10 000 replicas, PCG64 seed 42. Cada celda emite punto,
IC95 percentil, n sin ponderar y denominador ponderado como RESULT numericos.
Los intervalos son incertidumbre muestral de 2024, no predictiva de 2025.
