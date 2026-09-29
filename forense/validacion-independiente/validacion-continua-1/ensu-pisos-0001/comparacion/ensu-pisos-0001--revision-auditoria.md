# Revisión de auditoría · ensu-pisos-0001 · CERO-LECTURAS-FUERA

La auditoría automática marcó `$TMPDIR/fd/fd-2024-mar.txt`, `fd-2025-sep.txt`, `fd-2025-dic.txt` y `/pdftotext`.

**Revisión (receptora, 28/sep/2026, antes de dictaminar).** Los tres `.txt` son el texto que la reconstructora extrajo con `pdftotext` de `paquete/docs/fd-2024-mar.pdf`, `fd-2025-sep.pdf` y `fd-2025-dic.pdf`, es decir, derivados de documentos del paquete. `/pdftotext` es el nombre del binario en `entorno.txt`. La reconstructora no listó ni leyó nada ajeno en `$TMPDIR`.

**Veredicto:** CERO-LECTURAS-FUERA por revisión. Aplica la reserva general del acto sobre `$TMPDIR`.
