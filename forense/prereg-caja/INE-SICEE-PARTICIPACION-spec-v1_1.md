# Serie SICEE-INE · sucesor CALC-INE-PISOS-SICEE-0002

El primer resultado que produzca este procedimiento es el que se reporta.

Sucesor de `CALC-INE-PISOS-SICEE-0001`, que se congeló en el COMMIT-1
`9ce97ca6` bajo `INE-SICEE-PARTICIPACION-spec-v1_0.md`. Su primera corrida
**falló antes del sello**, aplicando la regla congelada «valor no numérico
detiene sin sello»: `medidor_fallo:ValueError: valor no numérico: None`.
Nada se escribió y el CALC 0001 queda congelado sin editar.

Diagnóstico de estructura, sin calcular tasas. Hay 18 de las 94 filas
con `total_votos` y `lista_nominal` en `null` y `porcentaje_participacion`
igual al literal `sinregistro`: `SEN_MR` 2021 y 2023 (distribuciones 1 y 2),
`SEN_RP` 2012/2018/2024 (distribución 1), `DIP_RP` 2009–2024 (distribución 1),
`SEN` 1994 (distribución 2), `CONS_POP` 2021 y `CONS_POP_RM` 2022
(distribuciones 1 y 2). Antes de congelar este sucesor se verificó, sólo
aplicando la regla de parseo a cada campo, que con el marcador declarado
abajo no queda ningún valor sin convertir (0 de 94 filas).

Cambio único. Un `null` en `total_votos` o `lista_nominal` produce la fila
con estado `SIN-DATO-PUBLICADO`, tasa `null` y diferencia `null`. En
`porcentaje_participacion`, `null` o el literal `sinregistro` equivalen a
«sin tasa publicada»: la tasa propia se calcula igual si hay numerador y
denominador, y la diferencia en puntos queda `null`. Cualquier otro texto no
numérico sigue deteniendo la corrida sin sello. Objeto, cargos, llave opaca
`distribucion`, prohibición de sumar y límites: idénticos a la v1_0.
