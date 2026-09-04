# ENCARGO TRIAGE-63 · las filas NO_PROBADO de acceso-puertas — triaje antes de sondeo

SHA de redacción: `a97dc28` (`origin/main`, merge #217 · ADR-77/A.8). Corregido en vuelo por `ADENDA 1`, emitida contra `e90a7a6` (merge #218 · ADR-78).

Archivado junto con su ejecución (regla A.3), no antes — llegó pegado en la conversación de dirección, sin archivo propio en el repo al momento de lanzarse.

**Estado: CONSUMIDO — COMMIT 1 por PR #219, COMMIT 2 por este PR.** El PARO de COMMIT 1 (`CANDIDATA-A-SONDEO = 27 > 20`, `forense/notas/2026-08-13-triage-63.md §7`) fue retirado sin fundamento por `ADR-79(i)`/`ADR-80(a)` (ver ADENDA 2 abajo) — no invalida el triaje de COMMIT 1. Ejecución de COMMIT 2 en `forense/notas/2026-08-13-triage-63-commit2-sondeo.md`.

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

## ADENDA 2 — dispatch de COMMIT 2 (recibido en mensaje separado, mismo día)

Texto verbatim del ítem que lanza este acto (numerado `8` dentro de un dispatch mayor de esa misma sesión de dirección; los ítems 1-7 no fueron recibidos por este acto y no se archivan aquí — fuera de lo que este acto puede auditar):

```
8 · TRIAGE-63 COMMIT 2 — el sondeo
Entorno: CAJA con red · Gate: ADR-79 con (i) firmado + REG-LOTE3 cerrado
Perímetro: columnas de sondeo de data/acceso-puertas-2026-08-13.tsv, nota, hallazgos. ⚠️ No toca estado_triaje.

Orden — las 17 que gatean Hito D primero, derivado por cruce contra necesidad-objeto-modelo.tsv;
re-derívalo y reporta si difiere: [lista de 17 filas por N-número, ver forense/notas/2026-08-13-triage-63-commit2-sondeo.md §1]
Las 10 restantes solo si mesa firmó SONDEO-COMPLETO.

Mecánica: GET nunca HEAD, nunca curl -I · sin override primero, con override solo si falla,
reportando los dos. A.5: "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS" con salida cruda y receta
manual de menos de un minuto. A.6: lo hallado por buscador y no abierto va SIN-FETCH. A.4: ninguna
clasificación negativa sin universo en la línea. Sin gate numérico. Si se acaba la capacidad, entrega
lo sondeado con la frontera declarada.
```

Precedido, en el mismo dispatch, por el bloque ARRANQUE + VERIFICACIÓN DE EXISTENCIA compartido de esa sesión (líneas base 3d0d1e5/ADR-76(f), receta T15, vocabulario A.4 EXISTE-SATISFACE/EXISTE-NO-SATISFACE/NO-ENCONTRADO/NO-ACCESIBLE) — no retranscrito aquí por ser genérico a todo el dispatch, no específico de este ítem; seguido verbatim, ver `forense/notas/2026-08-13-triage-63-commit2-sondeo.md §0`.

**El gate no estaba satisfecho al recibir el encargo — 0/2, verificado con comando, no asumido.** `ADR-79` no existía (máximo sellado 78) y `REG-LOTE3` no existía en ningún branch/commit/PR/worktree. Sesión reportó el estado exacto al usuario (actuando como mesa) y esperó, sin auto-adjudicarse el desbloqueo — mismo criterio que `R5.1-D3` (`forense/encargos/2026-08-13-r5-1-d3.md`) el mismo día. El gate se resolvió más tarde, sin acción de este acto: `ADR-79` sellado por `ACTO SELLA-3` (con su inciso `(i)`/`D-M` explícitamente **NO** sellado — "REGISTRADO, NO SELLADO", `gobernanza-v1_15.md:1183`), `REG-LOTE3` cerrado por `PR #225`, y `(i)` sellado como `SONDEO-COMPLETO` por enmienda in situ de `ADR-80(a)` (`ACTO FIRMAS-2`, `gobernanza-v1_15.md:1199`, firma de mesa verbatim: *"Sondeo Completo."*) — verificado de nuevo por comando (`git grep`, `gh pr view`) antes de arrancar el sondeo, no heredado de la notificación.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-13-triage-63-no-probado.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-13-triage-63-commit2-sondeo.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
