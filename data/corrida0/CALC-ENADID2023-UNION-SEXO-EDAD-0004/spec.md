# CALC-ENADID2023-UNION-SEXO-EDAD-0004

Mide situación conyugal actual por sexo×edad, la proporción de unión libre
entre personas actualmente en unión libre o casadas y la diferencia
mujeres−hombres bruta y estandarizada a una composición común de edad.

Unidad, códigos, universos, filtros, remuestreo compartido, tratamiento de
singleton, degeneraciones, intervalos y regla de estandarización están
congelados en
`forense/prereg-caja/ENADID2023-UNION-SEXO-EDAD-spec-v1_0.md` y parametrizados
en `spec.yaml` y en la sucesión humana
`forense/prereg-caja/ENADID2023-UNION-SEXO-EDAD-spec-v1_3.md`. Esta operación conoce el resultado del padre
`CALC-ENADID-0001`; lo reconstruye como control por masas y residuos, sin
volver a publicar otro nacional como novedad.

Es análisis descriptivo transversal. No mide primera unión, no usa EDER ni
variables del módulo femenino, y la resta bruto−estandarizado no identifica
un efecto causal ni un porcentaje explicado.

Este CALC sucede a 0003, que permanece sellado. 0003 construyó correctamente
ambos conteos, pero su esquema de serialización heredado omitió la columna
`n_numerador`. 0004 añade esa columna a `STD_COLUMNS`; no cambia universo,
masas, pesos, puntos, réplicas, incertidumbre ni estandarización.
