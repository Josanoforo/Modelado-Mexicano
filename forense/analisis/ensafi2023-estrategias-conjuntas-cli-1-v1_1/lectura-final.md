# ENSAFI 2023 · estrategias conjuntas · sucesor vigente v1.1

`CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1` sucede al CALC original,
que permanece sellado como evidencia histórica. Corrige la escala del IC de la
media del conteo a [0,8], publica soporte/denominador/EE/IC de ambas
condicionales en las 28 parejas, y publica diagnósticos de pesos, diseño y
singleton. No cambia los puntos sustantivos: media 1.84465, IC95
[1.78918, 1.90012].

Hay tres evidencias distintas. El control independiente recalcula P(conteo≥2)
y su EE mediante otra implementación. La integridad de archivos compara hashes
de tablas materializadas y no prueba que se hayan regenerado. El replay dirigido
oficial sí vuelve a ejecutar el medidor desde el ZIP declarado en un intérprete
nuevo: `REPRODUCE · IDENTICO`, 29/29 RESULT, sin diferencias ni IDs faltantes.
Su evidencia y el asiento canónico están en
`evidencia-replay-dirigido.json` y `forense/replay-evidencia.tsv`.
