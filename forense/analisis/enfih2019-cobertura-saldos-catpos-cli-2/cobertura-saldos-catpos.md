# ENFIH 2019 — cobertura y saldos Afore por CAT_POS

`CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001` describe hogares, pesos
corrientes ENFIH 2019 y saldo total conocido del hogar. `CAT_POS` es posición
ocupacional de la persona de referencia; no es formalidad ni conducta.

## Resultados

| CAT_POS | Etiqueta | n marco | Masa | Tenencia | Cobertura completa | Media completos | Mediana |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | Persona no ocupada | 4,354 | 8,852,474 | 38.31% | 38.01% | $119,258 | $60,000 |
| 1 | Empleado(a) u obrero(a) | 8,154 | 16,324,432 | 72.30% | 34.58% | $243,607 | $90,000 |
| 2 | Jornalero(a) o peón(a) | 987 | 2,195,923 | 29.40% | 38.23% | $68,411 | $33,000 |
| 3 | Patrón(a) o empleador(a) | 390 | 698,263 | 56.88% | 35.63% | $147,080 | $65,000 |
| 4 | Cuenta propia | 3,428 | 7,472,609 | 41.61% | 44.59% | $86,265 | $47,000 |
| 5 | Familiar sin pago | 452 | 1,100,979 | 35.19% | 48.67% | $86,272 | $36,000 |

Los grupos reconstruyen exactamente el marco (17,765 hogares, masa
36,644,680) y el control nacional: cobertura 37.1601%, media $180,197.68 y
mediana $71,000. No hubo residuo CAT_POS en este payload; se publicó la fila
`DESCONOCIDO` de todos modos para conservar el contrato.

Frente al resto de categorías nativas, empleados/obreros tienen 6.43 pp menos
cobertura completa (IC95 −8.94, −3.93), pero $142,973 más de media y $40,000
más de mediana entre completos. Cuenta propia tiene 8.82 pp más cobertura
(5.50, 12.15), pero $115,830 menos de media y $33,000 menos de mediana.
Estos contrastes son descriptivos, comparten réplicas y no tienen ajuste por
multiplicidad.

## Interpretación y reserva

La tenencia por CAT_POS no resuelve la selección monetaria: la cobertura del
total completo va de 34.58% a 48.67% entre categorías. Por eso las diferencias
de saldo describen únicamente a quienes tienen total conocido; no identifican
la distribución de todos los tenedores, ni diferencias poblacionales de ahorro
o planeación. No se imputó ningún desconocido ni se estimó stock nacional.

## RESULT → estimando → universo

| RESULT | Estimando | Universo |
|---|---|---|
| `TABLA-CATEGORIAS-JSON` | marco, estados, cobertura, cuantiles y sensibilidad positiva | cada CAT_POS; estados con denominador todos los tenedores |
| `TABLA-CONTRASTES-JSON` | categoría menos resto nativo, IC compartido | categorías 0–5; excluye desconocido de ambos lados |
| `CONTROL-NACIONAL-JSON` | reconstrucción y controles nacionales | marco completo |
| `REPLICAS-VALIDAS-JSON` | soporte efectivo de precisión | 2,000 réplicas UPM-en-EDIS |

La ejecución sellada identifica el payload por SHA-256
`be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5` y el
FD por `326b68b342797de45a7a4eb3dbf04f3790d11035df2611d7f9153d1ae12a48e1`.
