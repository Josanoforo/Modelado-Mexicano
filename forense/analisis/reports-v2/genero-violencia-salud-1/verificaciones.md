# Verificaciones del lote

EJECUTADO: arranque desde main `1eeb855272b933642177e3f32d51adc89f1009a0`; baseline rápida antes de integrar productos: `python3 tests/check.py --rapido --baseline` exit 0, LÍNEA BASE VERDE, sin FAIL nuevos. El intento de suite completa preparatoria se interrumpió durante T33 y no se usa como veredicto. No se modifica el baseline.

EJECUTADO: bytes del encargo recibidos con hash crudo y sello de cuerpo normalizado separado; hashes de adjuntos verificados por extracción de bytes. No se reescribe el cuerpo ni ningún sello al añadir cierre.

Los comandos locales de regeneración, comprobación y autoprueba están en resumen-lote.json. La verificación automática comprueba coherencia de decisiones, cobertura, trazabilidad cuantitativa y denominadores; no concede revisión independiente ni adopción.

EJECUTADO: primera comprobación conjunta VERDE; mutaciones de las tres piezas rechazadas. Gate rápido con los tres productos: exit 0, LÍNEA BASE VERDE, sin FAIL nuevos. WARN se conservan como observaciones, no adjudican. La corrección material del PDF ENCIG se verifica de nuevo por su productor y por el integrador antes del commit final.

EJECUTADO: main `3aacda232b3b03f158950738f31aa4ea509d3162` incorporado por merge sin conflictos. Verificador conjunto y autopruebas VERDE sin diferencias. `tests/check.py --rapido --baseline` exit 0: 0 FAIL, LÍNEA BASE VERDE. Se mantienen WARN y no se modifica baseline. Cambio cosmético propio: TSV de salud representa campos no aplicables como NO-APLICA, conservando columnas y regeneración.
