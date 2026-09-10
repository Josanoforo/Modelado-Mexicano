# `CALC-R-FAM-M-06-v3` — sucesor técnico de replay del árbitro R

 **Corrección adversarial PR #680:** sucede al sello `-v2` sin mutarlo. FP-370 conserva su alcance y no se extiende a este identificador técnico. **Celda:** `FAM-M-06`.

Hereda sin cambio los campos y resultados esperados congelados en `-v2`. Se crea después de la medición únicamente para completar la cadena de replay del estimando fijado en
`codificacion-R-v1_2.tsv`, sucesora registral de v1.1 que conserva el estimando y explicita reservas: payload `enigh2018_nc_csv`,
tabla `conjunto_de_datos_concentradohogar_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2018_ns.csv`, variable `remesas`, universo `hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2018 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 74647 filas leidas, 0 vacios en remesas`,
codificación `y=1 si remesas > 0; y=0 si remesas == 0 -- UMBRAL NUMERICO, no conjunto de codigos: remesas es monto continuo en pesos con 1424 valores distintos en 2018`, ponderador `factor`, estrato
`est_dis` y UPM `upm`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
Este sucesor técnico no añade una medición: hereda el conteo único de la cadena desde `CALC-R-FAM-M-06-v2`, cuyo objeto firmado es la medición R de `FAM-M-06`.
