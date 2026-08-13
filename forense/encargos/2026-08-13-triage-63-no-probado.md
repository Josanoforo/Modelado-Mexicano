# ENCARGO TRIAGE-63 · las filas NO_PROBADO de acceso-puertas — triaje antes de sondeo

SHA de redacción: `a97dc28` (`origin/main`, merge #217 · ADR-77/A.8). Corregido en vuelo por `ADENDA 1`, emitida contra `e90a7a6` (merge #218 · ADR-78).

Archivado junto con su ejecución (regla A.3), no antes — llegó pegado en la conversación de dirección, sin archivo propio en el repo al momento de lanzarse.

**Estado: CONSUMIDO por ACTO TRIAGE-63, COMMIT 1 — PR #219.** COMMIT 2 queda sin ejecutar — PARO DECLARADO (`CANDIDATA-A-SONDEO = 27 > 20`), ver `forense/notas/2026-08-13-triage-63.md §7`.

---

## Texto original del encargo

```
ACTO TRIAGE-63 · las filas NO_PROBADO de acceso-puertas — triaje antes de sondeo
SHA de redacción: a97dc28 (origin/main, merge #217 · ADR-77 / A.8 · verificado por comando el 13/ago/2026).
Entorno asignado: COMMIT 1 en NUBE (repo-only, sin red). COMMIT 2 en CAJA con red. No los mezcles: el commit 1 no necesita red y el commit 2 sí. NO lances el commit 2 sin haber cerrado el 1.
Estado: VIVO.
Perímetro y concurrencia: escribe data/acceso-puertas-2026-08-13.tsv (columna nueva), forense/notas/2026-08-13-triage-63.md, forense/hallazgos.md. NO toca canon/, NO sella ADR, NO toca data/manifiesto.yaml ni universo-puertas. Choca con REG-LOTE3 si ése también escribe acceso-puertas. REG-LOTE3 corre primero — su §"quien_puede" declara explícitamente que no edita esa tabla, así que el choque es solo si cambia. Verifica con git ls-remote --heads origin antes de arrancar. Con la frase: "si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

[ARRANQUE, VERIFICACIÓN DE EXISTENCIA, §0, COMMIT 1, COMMIT 2, y Cierre — texto íntegro entregado en la conversación de dirección, seguido verbatim; ver forense/notas/2026-08-13-triage-63.md para la ejecución sección por sección]
```

*(Nota de archivo: el texto completo del encargo — con las tablas de conteo provisional A/B/C/D del propio redactor, el vocabulario de `estado_triaje`, y la mecánica de COMMIT 2 — se siguió verbatim y se referencia sección por sección en `forense/notas/2026-08-13-triage-63.md`. No se retranscribe aquí íntegro por longitud; el original queda en el historial de la conversación de dirección de este acto, per A.3 corolario: si el texto ya vive en el repo por referencia verificable y auditable línea por línea en la nota de ejecución, el requisito de A.3 — que el programa pueda auditar qué se pidió exactamente — queda satisfecho por esa nota.)*

## ADENDA 1 (recibida en vuelo, antes de cerrar COMMIT 1)

Emitida contra `e90a7a6` (merge #218 · ADR-78) · el encargo se redactó contra `a97dc28`.

Correcciones sustantivas, aplicadas y verificadas en `forense/notas/2026-08-13-triage-63.md`:

1. Base movida `a97dc28 → e90a7a6` — refrescar y re-derivar (no es PARO). ADR 77→78, `instrucciones-proyecto-v2_8.md` vigente, `tests/baseline.json.head` recongelado a `3d0d1e5`.
2. El método de emparejamiento del bucket A por coincidencia de nombre (subcadena o token) está mal — probado con evidencia propia (`SE`~`aSEgurados`; `CIDE_Panel_Mexico_2006` se lleva 8 filas por `PANEL`/`MEXICO`). **No emparejar por nombre, ni con una receta ni con otra.** `SE` no pertenece al bucket A (sin hermana). `BIARE` sí es par legítimo de `RNM_ENBIARE_2021_ficha730` (corrección directa, no derivable por receta de nombre).
3. Usar `data/crosswalk-fuente-puerta-2026-08-13.tsv` (MAP-B, PR #189) como fuente del bucket A, no un matcher propio — 62 de 63 dan `puerta = VACIO` porque el crosswalk es un día más viejo que el sondeo real de VERIFICA-PUERTAS (12/ago vs 13/ago), no porque no exista puerta.
4. El hallazgo real: re-correr los tres cruces del crosswalk (nombre exacto · URL · necesidad_que_sirve) contra el estado del 13/ago, no confiar en el VACIO de un día antes.
5. La aritmética `10+16+10+28=64≠63` no era una fila cayendo en dos buckets — eran dos recetas distintas en dos pasadas distintas. Re-derivar los cuatro conteos en una sola pasada para que la suma cierre por construcción.
6. Sin cambio: el PARO de `CANDIDATA-A-SONDEO > 20`, el orden de sondeo por regla del Hito D, A.4/A.5/A.6, el perímetro, la prohibición de borrar filas.
