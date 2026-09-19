# PISOS ENIF 2021 por ejes y dos desenlaces · sucesor v2.1

El primer resultado que produzca este procedimiento es el que se reporta.

Sucesor correctivo de `CALC-PISOS-ENIF2021-EJES-0002`. La corrida 0002
se ejecutó tras su congelado, pero su control sustantivo detectó D9=0 en toda
celda. El defecto fue una alineación de etiquetas de columna al combinar
`P5_4_1..9` con `P5_7_1..9`: pandas alineó nombres distintos en vez de
pares posicionales. Sus salidas no se incorporaron ni publicaron. Esta v2.1
congela la comparación posicional antes de volver a ejecutar; conserva todas
las demás decisiones de v2.0 y la exposición queda declarada.

- Ahorro informal: cualquiera de `P5_1_1..P5_1_6=1`; no si todas =2.
- Ahorro formal: sí si cualquier `P5_7_1..9=1`; no si, para cada tipo
  homólogo i, `P5_4_i=2` o `P5_7_i=2`. Los pares se comparan por posición.
- D9 = informal sí y formal no; cero si informal no o formal sí.
- `informal_cualquiera` conserva el indicador informal.
- Cuenta por `P5_4`, localidad por `TLOC`, edad 18–96 y educación 00–09.
  Formalidad sigue NO-CONSTRUIBLE por ausencia de contraparte de P3_13.
- FAC_ELE, EST_DIS × UPM_DIS, 10 000 remuestras PCG64(42), un solo plan de
  réplicas compartido por ambos desenlaces y todas las celdas.
