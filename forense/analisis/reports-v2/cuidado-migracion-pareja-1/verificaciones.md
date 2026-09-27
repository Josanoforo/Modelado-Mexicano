# Verificaciones · cuidado, migración y pareja

EJECUTADO: productores conjuntos generan tablas, índice y hashes; --check PASS en tres piezas; --self-test rechaza mutaciones materiales de cobertura, respaldo, valor, denominador, selección de población, veto y fuente no leída. Revisión dirigida de ROMPE y mecanismos por los ejecutores, no independiente.

EJECUTADO: `tools/verifica_sidecars.py` sin FAIL; WARN heredado de encabezado ajeno en cierre ENIF, sin modificación por este lote.

EJECUTADO: primera suite `tests/check.py --baseline --parallel` exit 1: dos FAIL nuevos T25 por referencias bibliográficas sin prefijo en archivos locales; el siguiente gate reveló una tercera identidad en la misma plantilla al retirarse la primera coincidencia. Corrección propia mediante prefijos estables, sin tocar tests/CI. T06 (consistencia GEN1) y T08 (mapa de evidencia GEN1) son fallos heredados ajenos, no reparados. La nueva ejecución y el gate posterior al apéndice se registran al obtener sus resultados.

CONTADOR: `python3 tools/corrida0.py status` al cierre, [salida cruda](contador-corte.txt), desde vistas del corte. Ninguna medición, adopción o celda nueva producida por este diff; no se editan decisiones, resultados, usos ni contadores.

Corte editorial y main incorporado: `11602de8e375c10b90807d1b74e088f6b9e99c8b`, fetch final con cero commits pendientes de incorporación. Los gates verifican consistencia del producto; no adjudican el incidente de exposición documental ni acreditan recepción independiente.

EJECUTADO: prefijos corregidos y búsqueda del regex exacto T25 sin coincidencias locales; productores regenerados, --check PASS. Gate rápido final sin FAIL. La última suite completa corre sobre la corrección total, sin modificar baseline.

EJECUTADO: suite final `tests/check.py --baseline --parallel` exit 0, LÍNEA BASE VERDE sin FAIL nuevos. Persisten tres FAIL heredados (T06/T08 del corpus original); no se reparan ni se modifica baseline. [Salida de adjudicación](gate-final.txt). Productores y gate rápido posterior al apéndice pasan; esto no resuelve las reservas de contenido o el incidente.
