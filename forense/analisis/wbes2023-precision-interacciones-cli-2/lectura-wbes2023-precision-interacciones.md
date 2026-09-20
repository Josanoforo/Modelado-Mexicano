# Lectura específica · WBES2023 precisión de interacciones

Esta lectura reemplaza el nombre genérico `lectura.md` (colisión T02). La salida principal sellada contiene 62 filas y SHA-256 `067911e668442955a9108d97061dd53727889f91a9112d2f88ee3a447d93f632`.

El complemento trazable `wbes2023-fiscal-operacion-complemento.csv` publica los dos puntos, numeradores y denominador común que la serialización de la primera corrida omitió. No altera ni reinterpreta el sello de `CALC-WBES2023-PRECISION-INTERACCIONES-0001`.

El contraste se apoya en sólo dos establecimientos doblemente expuestos y con ambos desenlaces válidos. Sus EE=0 e IC=[0,0] son una degeneración de la muestra observada: no son evidencia de equivalencia poblacional, ni justifican inferir igualdad entre fiscal (último año) y operación (dos años).

El control independiente `control_independiente_contraste.py` no importa el medidor sellado y reproduce punto, varianza y covarianza del contraste directamente desde el microdato, bajo ambos escenarios singleton.
