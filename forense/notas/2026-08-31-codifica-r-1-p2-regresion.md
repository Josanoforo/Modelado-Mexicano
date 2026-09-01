# CODIFICA-R-1 · P2 — regresión de `tools/arbitra.py` contra DIN-11/SFT-04/TIC-08

ENCARGO: `forense/encargos/2026-08-31-MAESTRA33-C3-CODIFICA-R-1.md`.

## Qué se cambió en `tools/arbitra.py`

Se agregó (sin tocar el modo marco original, que sigue funcionando igual):

- `lee_codificacion()`: lee `codificacion-R-v1_0.tsv` (cabecera `#id\t...`).
- `_correr_r()`: carga `corridas-R/correr-R.py` como módulo por ruta
  (el nombre trae un guion, no es importable con `import` normal) para
  reusar `estima()`, `csv_zip()`, `dbf_zip()` — el cálculo estadístico no
  se reimplementa, se reusa tal cual.
- `parsea_codificacion_binaria()`: regex sobre la prosa
  `y=1 si VAR=='V1' ...; y=0 si=='V2' ...` → `(uno, cero)`. Si la prosa no
  calza ese patrón simple, devuelve `None` (nunca adivina) — es
  exactamente lo que pasa con la prosa distinta de `TIC-12`
  (categórica, "y=0 si p3n en 1..10 distinto de 8"), que este mecanismo no
  intenta resolver.
- `calcula_desde_tabla()`: dado un `id_celda`, busca su fila en la tabla,
  rechaza explícitamente si `tabla` declara un `join` (no reproducible sin
  código de join, que la tabla no trae), resuelve `payload_id` contra
  `data/manifiesto.yaml`, lee el CSV o DBF correspondiente y llama
  `estima()` con `variable/ponderador/estrato/upm` de la tabla (en
  minúsculas, porque `csv_zip`/`dbf_zip` normalizan sus llaves a
  minúsculas).
- `regresion(ids)`: para cada id, si `corridas-R/<id>.json` no existe,
  reporta NO-COINCIDE con motivo; si existe, calcula desde la tabla y
  diffea `R`, `EE_R`, `n_efectivo`, `n_estratos`, `n_upm_total` contra el
  JSON real. **Nunca escribe en `corridas-R/`.**

## Límite declarado (no oculto)

`universo_filtro` en `codificacion-R-v1_0.tsv` es la prosa que ya traía el
JSON fuente (ver nota de P1) — no es código ejecutable. Este mecanismo
**no aplica ningún filtro de universo** más allá de la codificación
binaria. Es correcto exactamente para las celdas donde "la tabla ya es el
universo" (sin filtro adicional) — que resultan ser las tres que P2 pide
regresionar. Para una celda que sí necesite un filtro real no declarado
en forma ejecutable (ejemplo verificado en el árbol: `DIN-05`, universo
`TLOC=='4'`) este cálculo daría un número distinto del real — lo atraparía
la propia regresión como NO-COINCIDE, no una detección previa. Tampoco se
generalizó el caso `join` (`DIN-03`/`TIC-01`/`TIC-12`): se declara y se
para, no se adivina el join desde la prosa de `tabla`. Generalizar
filtro/join queda fuera del perímetro de este acto.

## Comando y salida cruda

```
$ python3 tools/arbitra.py --regresion DIN-11 SFT-04 TIC-08
DIN-11: COINCIDE
    R: nuevo=0.4583913965555015 == existente=0.4583913965555015
    EE_R: nuevo=0.007241245036334212 == existente=0.007241245036334212
    n_efectivo: nuevo=12446 == existente=12446
    n_estratos: nuevo=182 == existente=182
    n_upm_total: nuevo=1908 == existente=1908
    advertencia: DIN-11: universo_filtro es informativo, NO se ejecuta como filtro (...)
SFT-04: COINCIDE
    R: nuevo=0.0604055335123943 == existente=0.0604055335123943
    EE_R: nuevo=0.004140846076745225 == existente=0.004140846076745225
    n_efectivo: nuevo=10103 == existente=10103
    n_estratos: nuevo=128 == existente=128
    n_upm_total: nuevo=4555 == existente=4555
    advertencia: SFT-04: universo_filtro es informativo, NO se ejecuta como filtro (...)
TIC-08: COINCIDE
    R: nuevo=0.9044714694763597 == existente=0.9044714694763597
    EE_R: nuevo=0.0023885166040940498 == existente=0.0023885166040940498
    n_efectivo: nuevo=47240 == existente=47240
    n_estratos: nuevo=437 == existente=437
    n_upm_total: nuevo=8741 == existente=8741
    advertencia: TIC-08: universo_filtro es informativo, NO se ejecuta como filtro (...)
```

`echo $?` tras la corrida: `0` (las tres coincidieron; el script sale `1`
si alguna no coincide). `git status --short` inmediatamente después:
solo `tools/arbitra.py` modificado — nada bajo `corridas-R/` se tocó.

## Veredicto

**Coincide → ACEPTADA.** Las tres celdas (`DIN-11`, `SFT-04`, `TIC-08`)
reproducen exacto `R`, `EE_R`, `n_efectivo`, `n_estratos`, `n_upm_total`
contra su JSON real, usando solo `codificacion-R-v1_0.tsv` +
`data/manifiesto.yaml` + el estimador ya existente. Anotado en
`.claude/commands/arbitra.md` (sección "Actualización · CODIFICA-R-1").

Esto resuelve, para estas tres celdas, el PARO que `ARBITRO-R-1` (PR #417)
había declarado en su propio P3: la causa que ese acto documentó
("ningún marco declara codificación ni diseño") sigue siendo cierta del
marco — pero ya no es un bloqueo, porque la codificación y el diseño ahora
viven en una tabla aparte que `arbitra.py` sabe leer.
