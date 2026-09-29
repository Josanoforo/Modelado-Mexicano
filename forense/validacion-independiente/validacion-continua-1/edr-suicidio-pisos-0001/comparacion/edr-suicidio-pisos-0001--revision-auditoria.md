# Revisión de auditoría · edr-suicidio-pisos-0001 · CERO-LECTURAS-FUERA

La auditoría automática marcó dos «rutas fuera del cwd»: `/home/pc0/tmp/claude-1000/desc/2015.txt` y `/pdftotext`.

**Revisión (receptora, 28/sep/2026, antes de dictaminar).** `desc/2015.txt` es el texto que la propia reconstructora generó en `$TMPDIR` con `pdftotext -layout paquete/docs/descriptor-2015.pdf` (comando previo del mismo transcript). Leerlo es leer un derivado de un documento del paquete. `/pdftotext` es un fragmento del nombre del binario del sistema, no una lectura de datos. La reconstructora no listó ni leyó nada ajeno en `$TMPDIR`.

**Veredicto:** CERO-LECTURAS-FUERA por revisión. Aplica la reserva general del acto: `$TMPDIR` es compartido y la ceguera se sostiene por la auditoría del transcript.
