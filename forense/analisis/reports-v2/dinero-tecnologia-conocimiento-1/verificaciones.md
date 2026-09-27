# Verificaciones

EJECUTADO: comparación byte a byte del encargo recibido con su archivo ya archivado por #1191; SHA-256 del cuerpo completo y tres adjuntos en adjuntos-verificados.json. No se modifica el archivo fuente.

EJECUTADO: `python3 tests/check.py --rapido --baseline` sobre corte inicial y asientos comunes: exit 0; 0 FAIL, LÍNEA BASE VERDE. Log local `/tmp/astra6-c3-dinero-baseline-inicial.log`. Un intento de consultar `check.py --help` inició la suite porque el script no procesa esa opción; interrumpido en T32-ter, no cuenta como gate completo ni evidencia del producto.

Los controles locales verifican regeneración, cobertura y trazabilidad. No acreditan identificación causal, adopción, capacidad predictiva, validación ciega C1 ni recibo independiente.

EJECUTADO: productor conjunto, --check y --self-test VERDE. Cobertura/índice sin diferencias; mutaciones materiales rechazadas por las tres piezas. Fetch global chocó con actualización concurrente de referencias remotas compartidas; fetch dirigido origin main resuelto, sin modificación de trabajos ajenos.

EJECUTADO al cierre sobre origin/main `11602de8e375c10b90807d1b74e088f6b9e99c8b` incorporado desde arranque: `python3 tests/check.py --rapido --baseline`, exit 0, 0 FAIL y LÍNEA BASE VERDE. Log `/tmp/astra6-c3-dinero-baseline-final.log`. Conserva WARN heredados; no se modifican tests, baseline ni CI. `git diff --check` limpio.

El control rápido es el gate ejecutado para este lote editorial, como en el precedente fusionado género/violencia/salud. No se presenta la suite completa ni CI como prueba sustantiva. Los tres productores y sus autopruebas ejercitan errores del contenido propio.

EJECUTADO: `cierre_acto.py --sin-suite --encargo <archivo archivado>` dry-run exit 0, HEAD deriva de origin/main True, rótulo censado, ninguna NC huérfana ni reconciliación de contadores necesaria. La herramienta deriva celdas_validadas=219 y no encuentra 0-bis por su heurística de nombre: el archivo fue archivado por el acto separado #1191 (9df094900), cuyo hash se conserva. Detecta CONSUMIDO ausente en el cuerpo fuente; se conserva ese cuerpo íntegro y se cita el asiento local de nota-cierre.md según INTERPRETACIÓN-DECLARADA, sin duplicar ni sobrescribir el testimonio recibido. El campo de FP se escribe ABIERTA, que es el estado que lee la herramienta, no un sinónimo.

EJECUTADO tras normalización LF y serialización TSV con campos vacíos entre comillas, preservando semántica: regeneración local VERDE, git diff --cached --check limpio, hashes de bytes staged iguales al árbol local. Gate rápido de entrega exit 0, 0 FAIL y LÍNEA BASE VERDE; log `/tmp/astra6-c3-dinero-baseline-entrega.log`. Las advertencias se conservan; el FP propio queda ABIERTA para revisión, no firmado.

Corrección FIN-022/FIN-029 solicitada en #1196: productor y --check VERDE; autopruebas dinero PASS; gate rápido contra baseline exit 0, cero FAIL y línea base VERDE (`/tmp/astra6-c3-dinero-correccion-fin022-fin029.log`). Revisión dirigida de objetos: hipótesis L31 separada de lectura país→persona L45/L66, primera cláusula ingreso–disposición separada de inferencia desde sobreprecios L19. No cambian cifras ni los reports de tecnología/conocimiento.
