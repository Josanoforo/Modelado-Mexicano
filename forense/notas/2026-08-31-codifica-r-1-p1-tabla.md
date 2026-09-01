# CODIFICA-R-1 · P1 — construcción de `codificacion-R-v1_0.tsv`

ENCARGO: `forense/encargos/2026-08-31-MAESTRA33-C3-CODIFICA-R-1.md`.

## A.13 — cuántos archivos examinó el comando

`forense/prereg-duelo-v2/corridas-R/*.json` tiene **18** archivos. De esos,
**15** son JSON de celda (nombre sin `_` inicial); los otros 3
(`_corredor-B.json`, `_plan-r-v1_0.json`, `_scoring-intento.json`) son
auxiliares de otros mecanismos, no celdas R, y se excluyeron por ese
criterio de nombre, no a mano.

De los 15 JSON de celda, `estado` se leyó de cada uno (no se asumió):

**`estado==COMPUTADO` (9, pasan a la tabla):** `CIV-08`, `DIN-03`, `DIN-05`,
`DIN-11`, `SFT-04`, `SFT-06`, `TIC-01`, `TIC-08`, `TIC-12`.

**`estado!=COMPUTADO` (6, excluidos, NO son R real):** `DIN-07`
(`RESERVA-SIN-MICRODATO`), `DOC-06` (`RESERVA-SIN-PAYLOAD`), `EMP-02`
(`RESERVA-SIN-MICRODATO`), `EMP-04` (`RESERVA-SIN-MICRODATO`), `EMP-05`
(`RESERVA-SIN-MICRODATO`), `TIC-06` (`RESERVA-SPEC-INCONSISTENTE`).

Los 9 `COMPUTADO` tienen los 9 campos fuente necesarios
(`id_celda`, `payload_id`, `tabla`, `variable`, `codificacion`, `universo`,
`ponderador`, `estrato`, `upm`) — verificado por script, no a ojo.

## Mapeo de columnas (JSON → tabla)

Correspondencia 1:1 salvo un renombre declarado: la columna del JSON
`universo` puebla la columna `universo_filtro` de la tabla — no existe en
el JSON un campo de filtro estructurado distinto del texto de universo que
`correr-R.py` ya escribió a mano por celda; es el único contenido
disponible para esa columna en las 9 celdas derivadas.

`fuente` se pobló con el literal `R-json` (no `R-json:<archivo>`) porque el
encargo lo da como valor fijo del enum (`fuente (R-json | FD:<archivo>)`) y
la columna `id` ya identifica sin ambigüedad cuál `corridas-R/<id>.json` es
la fuente.

`estado` se pobló con el literal `DERIVADA` para las 9 filas: son
codificación/diseño **extraídos por código** de un R ya `COMPUTADO`
(hardcodeado a mano en su momento por `correr-R.py`, según el propio
`tools/arbitra.py` documenta en su docstring), no una especificación nueva
propuesta antes de calcular (`PROPUESTA`, reservado a P3) ni una fila que
ya pasó la regresión de P2 (`ACEPTADA`, ver nota de P2 — solo aplica a
`DIN-11`/`SFT-04`/`TIC-08`, que si coinciden se re-marcan `ACEPTADA` en un
paso propio, no en este commit).

`fecha` = `2026-08-31` (fecha de esta derivación, no la fecha original de
cómputo de cada R — el JSON fuente no trae timestamp de cómputo que citar).

## El marco no se toca

Este paso no abre ningún marco en modo escritura. `sha256sum` antes y
después de P1, sobre los dos marcos `v1_1` que este acto podría tocar:

```
8e6459dd49869063986daa16cfbb8067575ee7c747e3cadd6a35f1b51d582477  forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv
9f5921085a9082bfa80458e238ee6ecae8a5d8da7439cf37d7686379cb22379c  forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv
```

`marco-M-congelado-v1_1.tsv` coincide además con el sha256 ya registrado en
`forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256` (sellado por ACTO
MAESTRA32-E20 · LOTE-NUBE-1 · P2). `marco-M-sorteado-v1_1.tsv` no tenía un
`.sha256` propio registrado; el valor de arriba es la línea base de este
acto, para comparar al cierre.

## Resultado

`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` — 9 filas, cabecera
`#id	payload_id	tabla	variable	codificacion	universo_filtro	ponderador	estrato	upm	fuente	estado	fecha`.
Verificación de columnas: las 10 líneas (1 cabecera + 9 filas) tienen
exactamente 12 campos separados por tab cada una — sin tabs ni saltos de
línea incrustados que hayan roto una fila.
