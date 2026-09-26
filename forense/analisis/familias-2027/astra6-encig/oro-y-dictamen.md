# Oro histórico y dictamen de factibilidad

EJECUTADO: auxiliar congelado antes del microdato, dos puntos reproduciéndose contra RESULT y hashes históricos. No validación ciega ni predicción futura. El conducto acepta correctamente la rama NO-ESTIMABLE; el IC del diagnóstico no habilita saltar el gate.

| Familia | RESULT del oro | Estado soporte | n | UPM dominio | Residuo ponderado | Diferencia respecto a piso |
|---|---|---|---:|---:|---:|---:|
| PAGO-DIGITAL | RESULT-ENCIG-AUX-PAGO-DIGITAL-P | NO-ESTIMABLE | 20203 | 8486 | 1.117575% (`RESULT-ENCIG-AUX-PAGO-DIGITAL-RESIDUO-FRACCION`) | 0 |
| SOLICITUD-MORDIDA | RESULT-ENCIG-AUX-SOLICITUD-MORDIDA-P | ESTIMABLE | 40042 | 9172 | 0.225778% (`RESULT-ENCIG-AUX-SOLICITUD-MORDIDA-RESIDUO-FRACCION`) | 0 |

PROPUESTO-POR-EJECUTOR: no activar PAGO-DIGITAL con el gate actual como prueba cuya factibilidad histórica haya sido acreditada. Conservar la emisión real del piso como compromiso prospectivo sin R; mantener el gate fijo. Propuesta concreta: retirar temporalmente la activación de esta familia y encargar una enmienda pre-dato fundada del tratamiento de residuo al circuito de mesa. Alternativa: conservarla CONDICIONAL bajo el gate idéntico; si la ola futura no lo cumple, NO-ESTIMABLE, sin relajar después de R. No se cambia umbral en este PR.

SOLICITUD-MORDIDA supera soporte histórico y queda CONDICIONAL a comparabilidad y autorización de ola. El marco completo tiene 442 estratos, 9172 UPM y 0 estratos de UPM única; el dominio digital conserva sus 8 singleton sin tratarlos como varianza cero. Bootstrap con reemplazo, sin ajustes de calibración reestimados: cobertura nominal no certificada. Kish no sustituye tamaño efectivo del diseño.

Las dos emisiones son puntos del RESULT fijo, no tasas inventadas ni declaraciones de viabilidad. El universo persona y evento se mantienen separados. Los escenarios de potencia son condicionales a cumplir comparabilidad y soporte; no incluyen probabilidad estimada de pasar el gate residual de una ola inexistente.
