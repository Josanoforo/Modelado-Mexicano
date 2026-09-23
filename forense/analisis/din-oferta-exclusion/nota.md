# DIN oferta y exclusión · lectura de primeras emisiones

## EJECUTADO

Cuatro CALC GEN2 desde microdato ENIF 2012, 2015, 2018 y 2021; una corrida por ola, persona 18–70. Cada `run` siguió al commit de freeze `5ab593e7`; los cuatro `verify` fueron `REPRODUCE` con contexto `IDENTICO`, tolerancia absoluta 1e-10. Unidad de P e IC95: proporción ponderada del total de no usuarios de la conducta; en esta tabla se multiplica por 100 y se informa en porcentaje. `N` son personas sin ponderar y `DEN-W` suma de factores persona.

| Ola | Producto no usado | N | DEN-W personas | OFERTA % [IC95] | PREFERENCIA % [IC95] | OTRO/NS % [IC95] | Cobertura % [IC95] | Cualquier oferta % [IC95] | Mixta % [IC95] |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2012 | CREDITO | 4497 | 51053390 | 30.2 [28.5, 32.0] | 56.1 [54.1, 58.1] | 13.7 [12.3, 15.0] | 98.9 [98.5, 99.2] | 39.5 [37.6, 41.4] | 8.4 [7.3, 9.5] |
| 2012 | CUENTA | 3989 | 45382727 | 5.2 [4.4, 6.1] | 15.6 [14.2, 17.0] | 79.2 [77.7, 80.7] | 99.4 [99.1, 99.6] | 10.9 [9.6, 12.3] | 1.3 [0.9, 1.7] |
| 2015 | CREDITO | 4287 | 54033165 | 33.3 [31.4, 35.2] | 42.1 [40.2, 44.0] | 24.6 [23.0, 26.3] | 100.0 [100.0, 100.0] | 44.3 [42.2, 46.3] | 8.7 [7.6, 9.8] |
| 2015 | CUENTA | 3346 | 42604135 | 7.8 [6.7, 9.0] | 34.5 [32.6, 36.5] | 57.7 [55.6, 59.7] | 100.0 [100.0, 100.0] | 8.6 [7.4, 9.8] | 0.3 [0.1, 0.5] |
| 2018 | CREDITO | 8329 | 54459292 | 35.9 [34.6, 37.3] | 56.0 [54.7, 57.4] | 8.0 [7.3, 8.8] | 100.0 [100.0, 100.0] | 35.9 [34.6, 37.3] | 0.0 [0.0, 0.0] |
| 2018 | CUENTA | 6149 | 41846268 | 15.8 [14.6, 17.0] | 43.1 [41.3, 44.8] | 41.1 [39.4, 42.9] | 100.0 [100.0, 100.0] | 15.8 [14.6, 17.0] | 0.0 [0.0, 0.0] |
| 2021 | CREDITO | 8000 | 56334122 | 34.6 [33.1, 36.1] | 58.0 [56.5, 59.6] | 7.4 [6.7, 8.1] | 100.0 [100.0, 100.0] | 34.6 [33.1, 36.1] | 0.0 [0.0, 0.0] |
| 2021 | CUENTA | 5974 | 42585907 | 12.6 [11.7, 13.7] | 50.3 [48.8, 51.9] | 37.0 [35.5, 38.5] | 100.0 [99.9, 100.0] | 12.6 [11.7, 13.7] | 0.0 [0.0, 0.0] |

La partición OFERTA + PREFERENCIA + OTRO/NS = 100% por celda. En 2012 y 2015 algunas preguntas son de respuesta múltiple: “cualquier oferta” incluye mezclas y no se equipara a razón principal. 2018 y 2021 usan razones principales en ambos pases y no tienen mezcla por diseño. La cifra de cuenta describe tenencia de cuenta o tarjeta formal, no ahorro activo.

## LEÍDO

Los cuestionarios y FD del INEGI identifican los pases y opciones documentados en `conmensuracion-v1_0.tsv` (hash `3aefeba16447ad0b8b6a81d21352ae46ff4bc1d03a7e2fd9cd7f0850a2cc34f4`). El congelamiento clasificó como OTRO/NS el texto compuesto “desconfianza o mal servicio” por ambigüedad; tampoco convirtió ingreso insuficiente en costo del producto. Los FD de 2012/2015 preguntan derechohabiencia general: no hay formalidad laboral comparable; 2018/2021 sí tienen seguridad social por trabajo.

## REPORTADO

En 2018–2021, la oferta declarada como razón principal entre quienes no usan crédito formal es aproximadamente 35–36%; para no tener cuenta formal, 13–16%. Es una descripción de razones declaradas, no una atribución causal ni un límite causal de cuánto acceso resolvería ampliar oferta. En 2012–2015, la respuesta múltiple y los pases impiden comparar directamente esas prevalencias con la razón principal de 2018–2021. En 2012 la insuficiencia de ingreso, por sí sola, domina OTRO/NS de cuenta; ello no equivale a costo explícito del servicio.

`enlace-pisos.tsv` recorre 1242 RESULT `-P` de cinco CALC históricos de piso: 413 tienen id de exclusión de crédito de la misma ola, población y eje; 829 tienen causa explícita. Es enlace contextual: el marginal del piso conserva su propio denominador y la exclusión usa no usuarios de crédito formal. Los RESULT de cuenta se entregan en los CALC de esta unidad, sin fingir un piso consumidor de crédito.

Opciones presentes sólo en una ola no deben contrastarse como cero: la opción “no quiere que le cobren impuestos” de 2021 no existe en la pregunta de 2018 (cuenta ni crédito); 2012 separa intereses bajos y comisiones altas de cuenta, mientras 2015–2021 los funden. Los contrastes de opción son `NO-COMPARABLE`; la partición global se informa por ola, con el matiz de respuesta múltiple frente a principal.

## Linaje y reproducibilidad

| Ola | CALC | corrida | commit usado al correr | payload sha256 | sello sha256 |
|---|---|---|---|---|---|
| 2012 | CALC-DIN-OFERTA-EXCLUSION-ENIF2012-0001 | CALC-DIN-OFERTA-EXCLUSION-ENIF2012-0001--5ab593e75c9c | `5ab593e75c9c` | `7bafcf6fdd3747bf330099dd752f2010441e0cd18fe942c35b15249d98092e55` | `329a31804175b32cca44a13ab014616dcc773594a8f5680ddbad55625728f2f3` |
| 2015 | CALC-DIN-OFERTA-EXCLUSION-ENIF2015-0001 | CALC-DIN-OFERTA-EXCLUSION-ENIF2015-0001--27b70b7ecb30 | `27b70b7ecb30` | `284e8a0c57f92256efc9743785c756986fb118fff424061bdb991f28779ce5fd` | `06f9a6bcfa632fc1d90c4aee825ba16a154d503e14fe5905b71493779741ef1c` |
| 2018 | CALC-DIN-OFERTA-EXCLUSION-ENIF2018-0001 | CALC-DIN-OFERTA-EXCLUSION-ENIF2018-0001--f43640111823 | `f43640111823` | `51f33ec74ccd596dc74b695587310d02e651923467255520aadc4d9fe13461d5` | `ff3e69da995cd8c900df0b0a0da6f9fa09ba2c36cd3fdbd4b7dee7e62878675e` |
| 2021 | CALC-DIN-OFERTA-EXCLUSION-ENIF2021-0001 | CALC-DIN-OFERTA-EXCLUSION-ENIF2021-0001--5f9375661527 | `5f9375661527` | `0f314fa3733b4b5519486ed4015fca1c9e0864840bcd5944aa7de27796fe5cd9` | `531d3dda97de11336c19dd361605060a4691f03d13e82ce970226a1c775a80df` |

Comandos: `python3 tools/corrida0.py preflight CALC-DIN-OFERTA-EXCLUSION-ENIF<ola>-0001`; `python3 tools/corrida0.py run CALC-DIN-OFERTA-EXCLUSION-ENIF<ola>-0001`; `python3 tools/corrida0.py verify CALC-DIN-OFERTA-EXCLUSION-ENIF<ola>-0001`. Semilla 42, 10 000 réplicas PCG64, remuestreo UPM dentro de estrato, plan único por ola. Los cuatro asientos propios están en `forense/replay-evidencia.tsv`.

## NO-CORRIDO / RESERVAS

ENIF 2024 y las olas reservadas de ENCIG, ENVIPE, ENCO y ENIGH: fuera de U1. No se modificaron ni reestimaron pisos, marcador, registro, CI ni derivados.

## CONSUMIDO

PR [#1042](https://github.com/Josanoforo/Modelado-Mexicano/pull/1042). Se consumieron specs y RESULT sellados de los cinco CALC de piso citados en `enlace-pisos.tsv`; los payloads se tomaron del manifiesto y corpus compartido con los hashes anteriores.
