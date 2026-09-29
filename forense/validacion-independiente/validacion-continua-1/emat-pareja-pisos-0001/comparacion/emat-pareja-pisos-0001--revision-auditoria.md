# Revisión de auditoría · emat-pareja-pisos-0001 · CERO-LECTURAS-FUERA

La auditoría automática marcó la «ruta» `/pdftotext`. En el transcript aparece dentro del comando que escribe `salida/entorno.txt` (versión del binario del sistema `pdftotext`): es un nombre de programa, no una lectura. No hay otras rutas fuera del cwd.

**Veredicto:** CERO-LECTURAS-FUERA por revisión. Aplica la reserva general del acto sobre `$TMPDIR`.
