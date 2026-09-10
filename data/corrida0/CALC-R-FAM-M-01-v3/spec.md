# `CALC-R-FAM-M-01-v3` — sucesor técnico de replay del árbitro R

 **Corrección adversarial PR #680:** sucede al sello `-v2` sin mutarlo. FP-370 conserva su alcance y no se extiende a este identificador técnico. **Celda:** `FAM-M-01`.

Hereda sin cambio los campos y resultados esperados congelados en `-v2`. Se crea después de la medición únicamente para completar la cadena de replay del estimando fijado en
`codificacion-R-v1_2.tsv`, sucesora registral de v1.1 que conserva el estimando y explicita reservas: payload `enif2018_csv`,
tabla `tmodulo2`, variable `p9_9_4`, universo `la tabla ya es ese universo (personas seleccionadas de tmodulo2, seccion 9.9); sin filtro adicional declarado en el diccionario`,
codificación `y=1 si p9_9_4=='1' (Si); y=0 si=='2' (No); 9 (no sabe/no responde) fuera`, ponderador `fac_per`, estrato
`est_dis` y UPM `upm_dis`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
Este sucesor técnico no añade una medición: hereda el conteo único de la cadena desde `CALC-R-FAM-M-01-v2`, cuyo objeto firmado es la medición R de `FAM-M-01`.
