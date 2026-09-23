# REGION-ENVIPE2025-SEGURO · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. ENVIPE 2025, cuatro tasas de denuncia por seguro en robo total de vehículo; unidad **delito** y 32 entidades de residencia de la víctima. R1/R2 del 23/sep/2026: solo geografía admisible; publicar punto e IC con denominador no ponderado ≥200, varianza estimable y regla oficial más estricta. Conservar todas las filas pequeñas como SUPRIMIDA-N con punto/IC nulos. `adopta: NO`, **RETROSPECTIVA**.

Se heredan exactamente universo, reactivos, códigos y unidad de `CALC-ENVIPE-DENUNCIA-SEGURO-0001`: `BPCOD=01`; `BP2_1=1` con seguro, `2` sin seguro; `BP1_20=1` denunció y `2` no denunció. Cuatro estimandos separados: denuncia y no denuncia en cada dominio de cobertura. Los complementos se **cuentan** mediante `BP1_20=2`; no se derivan por `1−p`. Denominadores distintos con y sin seguro. Factor `FAC_DEL`. `ID_PER` enlaza `TMOD_VIC` con `TSDEM` para la **residencia**, no para deduplicar delitos ni atribuir el lugar del robo.

Diseño: `EST_DIS`/`UPM_DIS` textuales, dominio sobre marco completo, 1 000 réplicas compartidas de UPM dentro de estrato, semilla PCG64 `20260923`, IC percentil y n efectivo Kish. Los RESULT `-JSON` retienen réplicas conjuntas sin IDs ni pesos individuales. Adaptador, estadística y función de réplicas compartidas quedan pinados en spec ejecutable. El control nacional posterior contrasta los cuatro puntos con el CALC sellado existente, sin tomarlos como fuente.

## Auditoría de rigor extremo

Cobertura de seguro no es asignación aleatoria. Una tasa de robo de vehículo no describe otros delitos ni toda la población. Las entidades representan residencia y las celdas pequeñas se suprimen, aunque el instrumento tenga diseño estatal general. No se deducen causalidad, preferencias culturales ni cambios futuros.
