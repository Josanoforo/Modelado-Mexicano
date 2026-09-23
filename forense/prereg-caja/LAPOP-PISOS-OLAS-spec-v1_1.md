# LAPOP México 2004 · sucesor CALC-LAPOP-PISOS-2004-0002

El primer resultado que produzca este procedimiento es el que se reporta.

Sucesor de `CALC-LAPOP-PISOS-2004-0001`, que se congeló en el COMMIT-1
`9ce97ca6` bajo `LAPOP-PISOS-OLAS-spec-v1_0.md`. Su primera corrida
**falló antes del sello**:
`medidor_fallo:ValueError: Out of range float values are not JSON compliant: nan`.
No se escribió `ejecucion.json`, `resultados.json` ni sello, y el CALC queda
congelado tal cual, sin editar. Causa, diagnosticada sin leer estimaciones:
la variable `wt` de 2004, que la v1_0 lee **sólo como diagnóstico**, viene
vacía en las 1 556 filas. Su mínimo y máximo son `NaN`, y el JSON estricto
los rechaza.

Todo lo de la v1_0 rige sin cambio para 2004: estimandos, umbrales,
reactivos, códigos, diseño (estrato `mestrat`, UPM `mprov`×`msec`, peso 1),
semillas, réplicas y guardias. La única diferencia es que el diagnóstico de
`wt` emite `null` en mínimo y máximo cuando no hay valores, y conserva
`n_vacios`. Que `wt` venga vacío confirma la ficha técnica *Unweighted*;
el peso usado nunca fue `wt`. Esta falla es de cableado del diagnóstico: no
toca estimando, universo ni umbral, y no es un primer resultado distinto.
