# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-13 · Archiva los cuatro adjuntos que FIRMAS-12 declaró ausentes y cierra sus dos NC

> ENTORNO: **NUBE** — cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · una sola sesión, rama propia `acto/gen2-tramite-firmas-13` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta.

## 1 · OBJETIVO
Nombrado como sucesor por `NC-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-01` y `-02` (`forense/no-corrido.tsv`, `forense/encargos/2026-09-23-GEN2-TRAMITE-FIRMAS-12.md` §`NO-CORRIDO`): archivar con sha256 verificado los cuatro adjuntos que el encargo `GEN2-TRAMITE-FIRMAS-12` declaró y que no llegaron con esa sesión, y cerrar las dos NC.
«Hecho»: los cuatro archivos existen con sidecar `.sha256` que coincide con el sha declarado por `FIRMAS-12`/`FIRMAS-11` · las dos filas `NC-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-01/02` en `CERRADA` · `check.py --rapido` VERDE.

## 2 · ADJUNTOS RECIBIDOS EN ESTA SESIÓN (verificados por sha256 contra lo declarado)
- `INFORME-COMPETENCIA-2026-09-23.md` — sha256 `acbaa795b67017c80844a253c2c3da6c2d5a496950991fe2c9d489fc2fa16f04` (coincide con el prefijo `acbaa795b67017c8…` que `FIRMAS-12` §3 citaba).
- `BRIEF-DEEP-SEARCH-2-competencia-Mexico-2026-09-23.md` — sha256 `d3d646b0bc3562a0ffc68025c1cdbd3ad362268d2f82632fa17a44d4fe104ea3`.
- `MISION-ASTRA-4-ADENDA-1.md` — sha256 `d674b5feedec8e82ca4ebe5e54e20dec9cee8762b3431c587a230fea744418cd`.
- `HOJA-DE-DECISIONES-2026-09-23.md` — sha256 `0fc5b52b57e6b3656bb82eeaa8e67625e29fcd1d0c6946922f7a0629ed674073` (coincide con el prefijo `0fc5b52b57e6b365…` que P3 de `FIRMAS-12` citaba).

## 3 · PIEZAS
- **P1.** `INFORME-COMPETENCIA-2026-09-23.md` y `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md` (renombrado desde `BRIEF-DEEP-SEARCH-2-…`, mismo objeto que §3 de `FIRMAS-12` nombraba) a `forense/encargos/fuentes/`, con sidecar `.sha256`.
- **P2.** `MISION-ASTRA-4-ADENDA-1.md` a `forense/encargos/`, con sidecar `.sha256` — perímetro ya declarado por `FIRMAS-12` §9.
- **P3.** `HOJA-DE-DECISIONES-2026-09-23.md` a `forense/encargos/fuentes/`, con sidecar `.sha256`.
- **P4.** Cierra `NC-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-01` y `-02` en `forense/no-corrido.tsv` (edición dirigida por línea, no reescritura completa del TSV — defecto ya documentado en `canon/gobernanza-v1_15.md` sobre el módulo `csv` y este archivo).

## 4 · LATITUD
Ninguna decisión de mesa pendiente: el contenido de `HOJA-DE-DECISIONES-2026-09-23.md` (D1-D8, propuestas de dirección) ya se resolvió por `ACTO GEN2-TRAMITE-FIRMAS-11` (`PR #1049`, fusionado, filas `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-01..07` con firma verbatim real de mesa, que en algunos casos difiere de la recomendación escrita en la hoja — p. ej. D1: la hoja recomendaba devolver `#1031`, mesa firmó integrar los dos). Este acto **no reabre ni reprocesa** esas decisiones: solo archiva el documento fuente con sha, tal como P3 de `FIRMAS-12` lo exigía.

## 5 · PAROS — lista cerrada
a) no aplica · b) no aplica · c) no aplica · d) no aplica · e) CAJA · f) algún sha no coincide con lo declarado.

## 6 · PERÍMETRO
Propio: `forense/encargos/fuentes/*`, `forense/encargos/MISION-ASTRA-4-ADENDA-1.md` (+sidecar), `forense/no-corrido.tsv` (edición de estado de las dos filas citadas), nota, L0, cascada. Ajeno: todo lo demás — en particular, no reabre `firmas-pendientes.tsv` D1-D8 de la hoja, ya resueltas por `FIRMAS-11`.

## 7 · LO QUE NO HACE · SUCESORES
No reprocesa D3/D8 de la hoja si quedaron sin fila propia en `FIRMAS-11` — eso, si aplica, es deuda de `FIRMAS-11`, no de este acto.
