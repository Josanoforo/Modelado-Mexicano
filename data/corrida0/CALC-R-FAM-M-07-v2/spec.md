# `CALC-R-FAM-M-07-v2` — preregistro mecánico del árbitro R

**Acto:** `GEN2-R-COMPLETA-MARCO`, FP-370, 9/sep/2026. **Celda:** `FAM-M-07`.

Congelado antes de abrir microdato. Mide el estimando ya fijado en
`codificacion-R-v1_1.tsv`, sucesora byte-idéntica de v1.0: payload `enigh2020_nc_csv`,
tabla `conjunto_de_datos_concentradohogar_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2020_ns.csv`, variable `remesas`, universo `hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2020 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 89006 filas leidas, 0 vacios en remesas`,
codificación `y=1 si remesas > 0; y=0 si remesas == 0 -- UMBRAL NUMERICO, no conjunto de codigos: remesas es monto continuo en pesos con 1389 valores distintos en 2020`, ponderador `factor`, estrato
`est_dis` y UPM `upm`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
`cuenta_gen2 = SI` para este `CALC-R-FAM-M-07-v2`; objeto explícito: la medición R de `FAM-M-07`.
