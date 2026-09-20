# CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001

Extensión descriptiva de `CALC-EDER-0003`; no lo reemplaza ni modifica.
Fuente: EDER 2017 CSV, SHA `bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`.
El FD ubica sexo en `persona.csv`, variable `sexo`: 1 Hombre, 2 Mujer,
enlazado por la terna de persona. El desenlace, universo, ponderador y diseño
son los del padre. Primer código no-cero se ordena por `anio_retro`; empates
con códigos distintos no se rompen arbitrariamente.

Se publican perfiles total, sexo, cohorte y sexo×cohorte con libre, directo y
residual. La diferencia mujer−hombre de p(libre) se estima por cohorte y en
el universo sexo/cohorte válido; la estandarizada usa pesos de cohorte de la
composición conjunta mujer+hombre de ese mismo universo. Bootstrap: 2,000
réplicas PCG64, UPM con reemplazo dentro de estrato, una misma réplica para
todos los contrastes y pesos recalculados en cada réplica. Estratos singleton
se conservan y aportan varianza cero: los IC no son límites garantizados.
