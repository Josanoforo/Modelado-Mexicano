# Prerregistro de caja — ENUT 2024 distribución de horas

Congelado en COMMIT-1 de `GEN2-ENUT2024-DISTRIBUCION-HORAS-CLI-2`, antes de
abrir las respuestas de `tvar_crea.csv`. Gobiernan la cara ejecutable
`data/corrida0/CALC-ENUT2024-DISTRIBUCION-HORAS-0001/spec.yaml` y su
explicación humana `spec.md` (sha256
`7aed1a3bdf3f922e64d8aee3538485296411f092efd655c379a6e21a006f9bab`).

Se fijan: persona 12–96; universo común y ocho variables idénticos al padre
#879; total/hombres/mujeres; dominios todas las válidas y participantes; p25,
p50, p75 y p90 por inversa izquierda de CDF ponderada sin interpolación;
concentración del 10% superior por masa de personas, fraccionando peso en el
umbral; CON_CP y SIN_CP; diferencias pareadas SIN−CON para p50, p90 y
concentración; diferencias mujer−hombre CON_CP para p50/p90; 2 000 réplicas
de UPM dentro de estrato, PCG64 semilla 20260919 e IC percentil.

El plan parte del marco con peso y claves válidos; los dominios contribuyen
cero. Ceros son valores; desconocidos no se imputan. Edad 97/98 queda en
reserva. No hay edad, 15A59, recorte a 168, winsorización ni inferencia causal.
La exposición incluye CALC-ENUT-0001, medias históricas y el padre #879.
Contador, consumo y adopción quedan `PENDIENTE-DE-MESA`.
