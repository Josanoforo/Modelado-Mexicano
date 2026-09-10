# `CALC-R-TRA-M-03` — preregistro mecánico del árbitro R

**Acto:** `GEN2-R-COMPLETA-MARCO`, FP-370, 9/sep/2026. **Celda:** `TRA-M-03`.

Congelado antes de abrir microdato. Mide el estimando ya fijado en
`codificacion-R-v1_1.tsv`, sucesora byte-idéntica de v1.0: payload `encig_2013_encig13_base_datos_dbf`,
tabla `Encig2013_01_viv_sec_1_3_4_5_8_9.DBF`, variable `P8_3`, universo `de los 33000 registros de la tabla (roster de vivienda+persona), 4617 son menores de 18 (FAC_P18<=0, correctamente fuera del universo 18+); de los 28383 restantes (18 anios y mas), 22653 (79.8%) tienen respuesta individual valida en la seccion VIII y 5730 (20.2%) quedan en blanco en P8_3 pese a que la vivienda muestra R_DEF=00 (entrevista de vivienda completa) -- no-respuesta a nivel PERSONA (R_ELE con codigo distinto de 01 en su mayoria), distinta de la no-respuesta a nivel vivienda; arbitra.py los excluye igual que a cualquier codigo invalido (blanco no calza '1' ni '2'), tratamiento estandar de no-respuesta. R se calcula sobre los 22653 adultos con respuesta valida. Este patron NO aparece en 2017/2021 (~0.2-0.4% en blanco): las tablas de datos abiertos de esas olas ya vienen filtradas al informante entrevistado, mientras que la tabla de 2013 conserva una fila por cada miembro del hogar en el roster, responda o no la seccion VIII -- diferencia de estructura de tabla entre olas, no de universo pretendido (las tres apuntan a poblacion de 18 anios y mas)`,
codificación `y=1 si P8_3=='1' (Si); y=0 si=='2' (No); 9 (No sabe / no responde) fuera`, ponderador `FAC_P18`, estrato
`EST_DIS` y UPM `UPM_DIS`. Ninguno de esos campos se elige en la corrida.

Salida esperada por nombre, nunca por valor: punto, EE/IC o reserva, n, masa,
exclusiones, estratos y UPM. El medidor no abre L, corpus, M, TRIADA ni R legado.
`cuenta_gen2 = SI` para este `CALC-R-TRA-M-03`; objeto explícito: la medición R de `TRA-M-03`.
