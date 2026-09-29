# Revisión de auditoría · ccpv-fam-pisos-0001 · CERO-LECTURAS-FUERA

La auditoría automática marcó siete «rutas fuera del cwd»: `/`, `/1e9`, `/with`, `/ccpv_cache.pkl`, `/ccpv-rec-propio/cache.pkl`, `/ccpv-rec-propio/smoke` y `/ccpv-rec-propio/smoke/diagnostico.json`.

**Revisión (receptora, 28/sep/2026, antes de dictaminar), sobre los comandos del transcript:**
- `/`, `/1e9` y `/with` son fragmentos de texto: una división, una constante y un comentario, no rutas.
- Los tres `ccpv*` son la caché propia en `$TMPDIR`: un pickle de las columnas autorizadas, escrito y leído por su propio `carga.py`, más una corrida de humo. La reconstructora los borró con `rm -rf "$TMPDIR/ccpv-rec-propio"` antes de sellar.
- No listó ni leyó nada ajeno en `$TMPDIR`.
- La lectura de microdato se limita a las columnas autorizadas (`usecols`; pyreadstat desde `paquete/lib` para los `.dta` Stata 110 de la entidad 15).

**Veredicto:** CERO-LECTURAS-FUERA por revisión. Aplica la reserva general del acto sobre `$TMPDIR`.
