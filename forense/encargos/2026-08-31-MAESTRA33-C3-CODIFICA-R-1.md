ENCARGO · MAESTRA33-C3 · CODIFICA-R-1 — invoca /acto
SHA de redacción: d353d82 (merge PR #421). ENTORNO: CAJA (data/raw montado; firma A.2 de tres partes) — NO NUBE, NO doble. COMPUERTA: tools/arbitra.py en origin/main (#417 fusionado, verificado por dirección). MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim): «[mesa: aprobación de la opción A — tabla de codificación al lado del marco, marco intacto. Si el corchete queda vacío, cero commits]».
A.8 (dirección contra d353d82): marco v1_1 sin columnas codificacion/upm/diseño (verificado). corridas-R/DIN-11.json EXISTE con codificacion, estrato, upm, ponderador, tabla, payload_id, universo. Tabla de codificación: NO-ENCONTRADO (ls prereg-duelo-v2/ → 0 archivos codificacion*). marco-M-sorteado-v1_1.tsv EXISTE (11 celdas, PR #419).
P1 · forense/prereg-duelo-v2/codificacion-R-v1_0.tsv (cabecera '#'): id · payload_id · tabla · variable · codificacion · universo_filtro · ponderador · estrato · upm · fuente (R-json | FD:<archivo>) · estado (DERIVADA | PROPUESTA | ACEPTADA) · fecha. Pobla por código las filas de todos los R con estado COMPUTADO leyendo sus JSON (declara cuántos examinó, A.13). El marco no se toca: verifica su sha256 al cierre.
P2 · Regresión: arbitra.py consume la tabla; recalcula DIN-11/SFT-04/TIC-08 y diff contra los JSON en R, EE, n_efectivo, n_estratos, n_upm. Coincide → ACEPTADA (anótalo en arbitra.md). No coincide → PARO-reporta cifras y comando, sin ajustar.
P3 · Primer lote nuevo: las 4 primeras celdas de marco-M-sorteado-v1_1.tsv sin R, en su orden de archivo (CIV-M-01, 06, 08, 09 — deriva, no heredes). Por celda: lee el FD del payload, escribe su fila PROPUESTA (valores que cuentan, los que quedan fuera, universo, diseño) — todo en COMMIT-1 con la frase de sello, ANTES de abrir microdato; COMMIT-2 corre arbitra y escribe corridas-R/<id>.json. CIEGO: jamás abre corridas-M/ ni milpa/tramite.yaml.
PERÍMETRO: codificacion-R-v1_0.tsv, tools/arbitra.py (lectura de tabla), arbitra.md, corridas-R/ (solo nuevos), data/cola-adquisicion-v1_0.tsv (payload ausente → fila), forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: puntos R sobre celdas sorteadas 0→N (N ≤ 4).
LO QUE NO HACE: no edita el marco ni su sha256; no re-escribe ningún R; no sortea; no emite M; no compara M contra R.
SUCESORES: lotes de 4 sobre las 7 sorteadas restantes (cola, ENTORNO: CAJA).

## CONSUMIDO

Commits `4436394` (0-bis A.3), `e56a750` (P1), `3a95057` (P2), `b299bf7`
(P3 COMMIT-1), `87141a5` (P3 COMMIT-2), `b27b27d` (cascada) y el commit de
sincronización de este mismo acto, en la rama
`acto/maestra33-c3-codifica-r-1`, **PR #423**. Veredicto: **P2 ACEPTADA**
(regresión `DIN-11`/`SFT-04`/`TIC-08` `COINCIDE` exacto) — resuelve el
`PARO` de `ACTO MAESTRA33-C2 · ARBITRO-R-1` (`ADR-245`). **P3: 4 puntos R
nuevos** (`CIV-M-01`/`06`/`08`/`09`, `CONTADOR: 4`, dentro del tope `N ≤
4`). Marco no tocado (`sha256` verificado sin cambio en cada commit).
`CIEGO` respetado: `corridas-M/` y `milpa/tramite.yaml` no se abrieron en
ningún commit de este acto (el merge de sincronización trae 11 archivos
`corridas-M/M-*.json` de `ACTO MAESTRA33-E6 · EMISOR-M-1`, `PR #422` — no
se abrieron para resolver el merge, solo se aceptaron íntegros de
`origin/main`, ninguna comparación M-vs-R). `tablero (recibo)`: no se creó
fila nueva en `forense/firmas-pendientes.tsv` — ningún hallazgo de este
acto queda pendiente de firma de mesa (mismo patrón que `ACTO
MAESTRA33-C2`, cuyo perímetro traía la misma frase y tampoco generó una).
Detalle: `forense/notas/2026-08-31-codifica-r-1-p1-tabla.md`,
`forense/notas/2026-08-31-codifica-r-1-p2-regresion.md`,
`forense/prereg-duelo-v2/notas-arbitra/2026-08-31-lote-civ-m-01-06-08-09.md`,
`forense/notas/2026-08-31-codifica-r-1-p3-commit2.md`.

**Colisión de ADR y sincronización.** Al sincronizar contra `origin/main`
(que había avanzado con `PR #422`, `ACTO MAESTRA33-E6 · EMISOR-M-1`) se
encontró que ese acto también candidateó `ADR-250` y fusionó primero —
regla de la casa, renumera quien fusiona segundo: este ADR pasa de `250`
a **`251`**. Conflictos de merge en `canon/estado-programa-v1_10.md`
(línea `L0`) y `canon/registro-rotulos.tsv` resueltos con el patrón ya
establecido: contenido de `origin/main` preservado verbatim, la anotación
de este acto insertada antes (L0) o después (registro-rotulos, orden de
fusión) sin reescribir ni una palabra de lo ya fusionado. `python3
tests/check.py --baseline` re-verificado **VERDE** tras la sincronización
y el renumerado, sin `FAIL` nuevo.
`python3 tests/check.py --baseline`: **VERDE**, `19 FAIL · 159 WARN`,
idéntico a `tests/baseline.json`, sin `FAIL` nuevo.
