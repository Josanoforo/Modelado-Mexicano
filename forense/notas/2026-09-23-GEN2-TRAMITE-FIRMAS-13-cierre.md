# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-13

23/sep/2026, entorno NUBE, Sonnet 5, MODO ABIERTO. Base al arrancar y al cerrar: `origin/main = ef5a746` (0 commits de diferencia).

## Qué se hizo

Mesa entregó en esta sesión los cuatro adjuntos que `GEN2-TRAMITE-FIRMAS-12` había declarado ausentes: `INFORME-COMPETENCIA-2026-09-23.md`, `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md`, `MISION-ASTRA-4-ADENDA-1.md` y `HOJA-DE-DECISIONES-2026-09-23.md`.

**Verificación de sha256, los cuatro, contra lo declarado:**
- `INFORME-COMPETENCIA-2026-09-23.md`: `acbaa795b67017c80844a253c2c3da6c2d5a496950991fe2c9d489fc2fa16f04` — coincide con el prefijo `acbaa795b67017c8…` de `FIRMAS-12` §3.
- `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md` (recibido como `BRIEF-DEEP-SEARCH-2-…`, mismo objeto): `d3d646b0bc3562a0ffc68025c1cdbd3ad362268d2f82632fa17a44d4fe104ea3`.
- `MISION-ASTRA-4-ADENDA-1.md`: `d674b5feedec8e82ca4ebe5e54e20dec9cee8762b3431c587a230fea744418cd`.
- `HOJA-DE-DECISIONES-2026-09-23.md`: `0fc5b52b57e6b3656bb82eeaa8e67625e29fcd1d0c6946922f7a0629ed674073` — coincide con el prefijo `0fc5b52b57e6b365…` que la NC de P3 citaba.

Los cuatro coinciden exacto. Archivados con sidecar `.sha256`: los tres primeros en `forense/encargos/fuentes/`, la adenda en `forense/encargos/`.

**Cierre de NC.** `NC-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-01` y `-02` pasan a `CERRADA` (`cerrado_por = ACTO GEN2-TRAMITE-FIRMAS-13`, `fecha_cierre = 2026-09-23`), editadas línea por línea (no con un round-trip completo del módulo `csv`, que `canon/gobernanza-v1_15.md` ya documenta como fuente de un defecto real sobre este mismo archivo). Verificado con `git diff` que solo esas dos líneas cambiaron.

## Lo que no se hizo

No se reprocesaron las ocho decisiones (D1-D8) de `HOJA-DE-DECISIONES-2026-09-23.md`. Ya están resueltas por `ACTO GEN2-TRAMITE-FIRMAS-11` (PR #1049, fusionado): sus filas `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-01..07` traen firma real de mesa, que en `D1` (PR #1030/#1031) es distinta de la recomendación que la hoja proponía (la hoja recomendaba devolver `#1031` sin fusionar; mesa firmó integrar los dos). Archivar el documento fuente no reabre esa decisión.

No se verificó si `D3` (celdas_validadas de crédito) o `D8` (`INDETERMINADO`) de la hoja tienen fila propia en `FIRMAS-11` — queda fuera de perímetro de este acto; si falta, es deuda de `FIRMAS-11`, no de éste.

## Contadores

`celdas_validadas`: 92 → 92 (sin cambio). CONTADOR del acto: cero mediciones, no adopta.

## Suite

`python3 tests/check.py --rapido` → VERDE, 0 FAIL.
