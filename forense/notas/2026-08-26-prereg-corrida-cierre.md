# Nota de cierre — `ACTO PREREG-CORRIDA`, 26/ago/2026

**Acto:** `PREREG-CORRIDA` (nube, `cloud_default`). `SHA` de redacción `9c25f28`. Encargo: `forense/encargos/2026-08-26-PREREG-CORRIDA.md` (`CONSUMIDO`).

## Qué produjo este acto

1. `forense/prereg-duelo-v2/prereg-corrida-v1_0.md` — pre-registro de la corrida del duelo `ADV1-M2`: hashes de los cuatro corredores comprometidos antes de que `R` exista (F1), spec de elicitación ADV1-M2 congelada con modelo/temperatura/k/agregado/formato/plantilla/`comparacion_principal_id` sellados (F2), banda TOST/margen material citados sin re-derivar y dejados abiertos para mesa (F3).
2. `canon/gobernanza-v1_15.md` `ADR-197` — registra RANURA 1 (cuál-`L`) y RANURA 2 (quién corre `L`), con el razonamiento de mesa y la respuesta de dirección verbatim.
3. `forense/firmas-pendientes.tsv` `FP-162` (`FIRMADA` — RANURA 1, gatea corridas `L` y scoring) y `FP-163` (`ABIERTA` — banda TOST/margen material del piloto, para mesa).
4. `canon/estado-programa-v1_10.md` — recifra de ADR (193→194) y línea del duelo actualizada: «pre-registro sellado; L listas para correr; árbitro después de L».
5. `forense/encargos/2026-08-26-PREREG-CORRIDA.md` — encargo archivado, `CONSUMIDO`.

## Verificación de existencia (A.8), tal como el arranque la exigió

- `find forense/prereg-duelo-v2 -iname "*arbitr*" -o -iname "*-R-*" -o -iname "*resultado-R*"` → vacío, antes y después de este acto.
- Ningún `prereg-corrida*.md` preexistía en `forense/prereg-duelo-v2/`.
- `data/raw/` ausente — OK para entorno `cloud_default`, sin red ni microdato; sonda de fuente saltada, negativo registrado con razón (no con inferencia).

## Suite

`python3 tests/check.py --baseline` (nunca `--freeze`): **19 FAIL · 131 WARN**, línea base VERDE contra `tests/baseline.json` (HEAD congelado `e24d033`). Ninguna cifra del árbitro se movió — **CONTADOR: cero, declarado**.

## Lo que este acto NO hizo

No corrió ninguna `L`. No computó ningún `R` ni CV. No tocó el sorteo, el marco congelado ni los cuatro corredores (solo los hashea, sin editarlos — `git status` limpio antes y después). No fijó la banda TOST/margen material por mesa. No designó una sesión concreta para correr `L`, solo el patrón de RANURA 2. Orden sagrado del diseño, respetado: hashes → L → R → scoring — nunca `R` antes de los hashes.

## Qué sigue

Mesa sella `FP-163` (banda TOST/margen material) cuando decida. Una sesión limpia fuera de este proyecto, conforme a RANURA 2, corre las 30 entradas de `L` (15 celdas × 2 variantes × `k=8`) siguiendo la spec congelada en `prereg-corrida-v1_0.md` §F2, sin haber leído este pre-registro ni el árbol `forense/prereg-duelo-v2/`. Solo después de que `L` complete y sus hashes queden comprometidos (ya lo están, F1) corre el árbitro `R`.
