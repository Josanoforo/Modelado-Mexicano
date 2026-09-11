# ACTO GEN2-PUBLICACION-POST693-Y-CIERRES · cierre

## Resultado útil

Las tres vistas derivadas de corrida0 publican ahora la procedencia de replay para 150 corridas, 3 335 resultados y 207 usos. La reconciliación no reejecutó medidores ni alteró resultados o sellos: enlazó evidencia ya publicada por identidad exacta, conservó expresamente el negativo posterior de las dos corridas C0D y dejó visibles los tres CALC que faltaban.

| obligación | evidencia | cerrada/residual | siguiente acción |
|---|---|---|---|
| publicar `fuente_replay` | `data/corrida0/{corridas,resultados,usos}.tsv`; seco posterior sin diferencia | CERRADA; `NC-0104` | conservar `forense/replay-evidencia.tsv` y exigir lote explícito ante transiciones futuras |
| preservar evidencia negativa | dos asientos C0D posteriores a PR #683 permanecen `NO-REPRODUCE` / `CONTEXTO-DISTINTO` | CERRADA | no sustituirlos por el asiento positivo anterior |
| mostrar los tres CALC omitidos | `CALC-0001-v2`: 38 RESULT; `CALC-ENIF-0002`: 59 RESULT y un uso; `CALC-TRIADA-0002`: 27 RESULT; los tres con fuente | CERRADA; `NC-0154` | ninguna publicación adicional |
| registrar ejecución de D13/D14 | `forense/firmas-pendientes.tsv`, FP-361/363; firmas originales intactas y ejecución enlazada a PR #688 | CERRADA | ninguna; no repetir los CALC |
| conciliar POST685 | cabeceras/bitácoras de lotes 01–06 remiten a PR #687/#689/#691/#688/#692/#693 | PARCIAL deliberada: lote 07 pendiente | ejecutar lote 07 sólo bajo su propia compuerta |
| conservar residuales reales | `NC-0151`, `NC-0152`, `NC-0153` y `NC-0155` continúan `ABIERTA` | RESIDUAL | seguir la acción específica de cada fila; no confundir replay con validación independiente |

## Método y estabilidad

`tools/corrida0.py registro` detectó 64 transiciones distribuidas en 32 corridas. Se incorporaron asientos en `forense/replay-evidencia.tsv` sin `--verifica`: 30 citan la identidad exacta del registro publicado y dos C0D citan el cierre posterior que documentó su cambio de contexto. `CALC-0001-v2`, que aún no existía en la vista anterior, cita el cierre de PR #688 que acredita 38/38 resultados reproducidos. La publicación se hizo con `registro --escribe --lote` acotado a esas 32 identidades.

La lectura seca posterior de corridas, resultados y usos fue estable. El hash agregado de todos los `resultados.json` y `sello.json` fue `b5a819a625ee26d533daad59add38e322d3e006924e6f45775f4f9d839ee3` antes y después: este acto publica metadatos derivados, no produce ni cambia números científicos.

## Límites

`HEREDADO-DEL-REGISTRO-PUBLICADO` acredita continuidad del asiento versionado, no una verificación nueva. `VERIFY-CITADO-DE-NOTA-DE-CIERRE` conserva la prueba ya reportada por el acto productor, tampoco la repite. El acto no adopta parámetros, no modifica `milpa/`, no cierra `NC-0155` y no fusiona su propio PR.

## Pruebas

- `python3 tests/test_corrida0.py`: 84 casos, 84 OK, 0 fallos.
- `python3 tests/test_cierre_acto.py`: 8 pruebas, 0 fallos.
- `python3 tests/check.py --baseline`: línea base VERDE; 3 FAIL históricos y 2 632 WARN, ninguna entrada nueva.
- `python3 tools/corrida0.py registro`: seco estable, sin diferencia en 150/3 335/207 filas.
