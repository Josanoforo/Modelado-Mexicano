# Encargo `SORTEO-V2-PROPUESTA`

**SHA de redacción:** `26ea239` (`origin/main`, merge de `PR #338`).
**Entorno asignado:** NUBE (`cloud_default`). Sin red externa ni microdato.
**Estado:** CONSUMIDO — ejecutado por `ACTO SORTEO-V2-PROPUESTA`, 25/ago/2026. Ver `forense/notas/nota-2026-08-25-sorteo-v2.md`.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- `FP-145` — EXISTE en `forense/firmas-pendientes.tsv`: `FIRMADA` (`firmada_en` cita `ADR-168(h)`, ruling `L9/FP-133` opción `c`), `ejecutada_en` vacío antes de este acto.
- `ADV1-M1` (marco de 60 casillas, tope 20% publicadas) — EXISTE: `forense/adv-duelo/ADV-1_demolicion_duelo_L_vs_M.md:59,380`; marco real `forense/marco-candidatas-piloto-v1_0.tsv` (60 filas, columna `estrato`/`publicada` verificadas por comando, §1 de la propuesta).
- Semilla `867948c` anulada — EXISTE, verificado por `grep -rn "867948c"` (múltiples notas y `ADR-135(d)`/`canon/gobernanza-v1_15.md:2706`, verbatim: *"la semilla ... queda anulada explícitamente"*).
- `P0/P1/P2` — EXISTE como columna `grado_dependencia` del marco.
- Las `8 PENDIENTE-FUERA-DE-INDICE` — EXISTEN, verificadas por conteo directo sobre el TSV (§1 de la propuesta).
- `FP-146` — EXISTE, `FIRMADA` sin ejecutar (índice Banxico/CNBV/BMV), citada como condición de elegibilidad de las 8 filas.

## Texto del encargo (verbatim, resumen operativo)

Ejecutar `FP-145` (`L9-c`) — **solo redactar, no ejecutar ningún sorteo real**. Redactar `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` con: algoritmo determinista con la cuota del 20% como restricción dura; regla de infactibilidad por estrato y su fallback; protocolo de semilla = SHA de merge del acto que congele marco+sorteo (no un número fijo); interacción con P0/P1/P2 y con las 8 `PENDIENTE-FUERA-DE-INDICE` (elegibles solo si `FP-146` las resuelve antes); pseudocódigo verificable; 3 casos de prueba (normal, infactibilidad por estrato, límite del 20%). Fila nueva en `A.12` («mesa sella sorteo-v2», `ABIERTA`). Marcar `FP-145` ejecutada (= propuesta redactada, no sorteo realizado).
