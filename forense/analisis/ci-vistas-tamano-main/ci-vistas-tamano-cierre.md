# Vista de resultados bajo el límite del canal

Encargo explícito de mesa: después de fusionar #1181, hacer fetch/sync y resolver CI contra main. #1184 ya estaba fusionado; se sincronizó el worktree de C1 a b804165b y se verificaron 3371 identidades y diez pruebas. El CI 36288663825 aprobó suite y pruebas, pero falló al regenerar resultados.tsv: 82 MiB > 50 MiB. No fue un fallo de las reconstrucciones C1.

Corrección en /home/pc0/mm-ci-vistas-tamano-main, rama codex/ci-vistas-tamano-main, base 3149b4e2bb2de36c940b02f62814a7b869e5ed7d. Se amplía únicamente el código de representación/lectura de vistas y su prueba existente. El límite de 50 MiB se conserva. El canal seguirá siendo el único escritor de derivados publicados; no se editaron vistas, sellos, números, adopciones ni CI a mano.

Ocho campos de texto pueden guardarse una vez por corrida si todas sus filas llevan exactamente el mismo texto no vacío: spec_id, sello, validacion_ref, alcance_validacion, rol_evaluacion, validacion_independiente, valor_legacy y delta_legacy. Campo variable, vacío verdadero o corrida única permanece inline. El mapa JSON constantes_resultados vive en corridas.tsv; cada fila compactada lleva constantes_corrida=1. Sin mapa válido la lectura falla en voz alta. Lectores de vistas, join del motor, consulta y relevo restituyen los textos. Formato anterior sigue admitido.

EJECUTADO: derivación sin verifica ni escribe, valor por referencia sin escribir, normalización y comparación exacta de cada diccionario completo antes/después de restaurar: 233428 filas idénticas. Texto que produciría el escritor: resultados.tsv 50787654 bytes (48.43 MiB), corridas.tsv 16516303 bytes (15.75 MiB). Constancia en ci-vistas-tamano-medicion.json. No es recálculo científico ni nuevo recibo independiente.

EJECUTADO: tests/test_vista.py y tests/test_valor_por_referencia.py: 14 pasan, incluidos vacíos variables, Unicode, corrida única, idempotencia, los lectores y metadata inválida/ausente. Puerta rápida: 0 FAIL, 598 WARN, baseline VERDE, sin congelar baseline. git diff --check pasa. La guarda mantiene un margen limitado de tamaño; un crecimiento futuro puede exigir otra normalización, no aumentar el límite automáticamente.

El PR contiene la corrección revisable; la mesa decide la fusión. La publicación de vistas necesita ejecutar el canal sobre main con la corrección incorporada.

Pruebas de integración EJECUTADAS: registro de lote estricto, linaje superado y overlay de validación independiente: 8 pasan y 2 subtests pasan.
