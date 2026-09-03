# MAESTRA37-N2 · GUARDIA-TSV-Y-CAPA2-LISTAS — nota de cierre

Encargo: `forense/encargos/2026-09-03-MAESTRA37-N2-GUARDIA-TSV-Y-CAPA2-LISTAS.md`.
Entorno: NUBE. SHA de redacción: `8f49eab8` (`origin/main`, merge PR #511).
ARRANQUE: clon existente (`/home/user/Modelado-Mexicano`), `.git/shallow` presente al
arrancar (298 commits visibles) → `git fetch --unshallow origin` corrido antes de
cualquier otro paso → 2 439 commits. `data/raw` no está montada (esperado en nube, ARRANQUE
punto 3). Este acto no toca red ni microdato (ARRANQUE punto 4, saltado por instrucción
explícita del encargo).

## P1 — FP-258, vía (ii)

Control congelado (`forense/notas/2026-09-03-MAESTRA37-N2-control.md`): round-trip
`csv.reader`→`csv.writer` (tab, `QUOTE_MINIMAL`) sobre `data/curacion-registro/
cola-adquisicion-registro.tsv` (112 líneas) da **4** líneas distintas: 29, 47, 63, 94.
El hallazgo original (`FP-258`) declaraba 3 (29, 47, 94); la 63 es la fila de CompraNet
que `ACTO MAESTRA36-A2` (`ADR-314`) editó línea por línea después de que `FP-258` se
abriera — creció, y se declara así en `forense/hallazgos.md`, no se fuerza al número
original.

`tools/curador_registro/tsv_crudo.py` (nuevo). `leer_lineas`/`escribir_lineas` tratan
cada línea como texto opaco: nunca la reinterpretan, así que un round-trip que no cambia
nada es la identidad por construcción — verificado, **0 líneas distintas**.

**Discrepancia con la vía descrita en el encargo, medida al implementar.** El encargo
pedía una sola estrategia ("split por `\t`, sin quoting, sin normalizar comillas") tanto
para el round-trip como para leer valores. Al implementarla así y correr la regresión de
la vista, el `diff` **no** salió vacío: la línea 9 del registro
(`WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023`) SÍ está correctamente citada en CSV real
(empieza y termina con `"`, comillas internas dobladas `""`), y un split naïve por tab
deja esas comillas literales dentro del valor de `nota` — corrompía la vista donde el
`csv.DictReader` original no la corrompía. Por eso `tsv_crudo.py` separa las dos
funciones: `leer_lineas`/`escribir_lineas` (texto opaco, para el round-trip) y
`leer_dicts` (delega en `csv`, para valores correctos). `tools/vista_cola_adquisicion.py`
adopta `leer_dicts`; la regresión es entonces genuinamente byte a byte:

```
$ python3 tools/vista_cola_adquisicion.py
$ diff <vista antes> data/cola-adquisicion-v1_0.tsv
IDENTICAL
```

`T26-bis` (`tests/check.py`, nuevo): control (round-trip csv da 4, no el 3 original —
falla si el número cambia sin declararse) + regresión (round-trip con `tsv_crudo` da 0).
No se normalizó ninguna de las 4 notas: se congelaron tal cual, verificadas una a una
como parte del control.

## P2 — FP-246, vía (a)

Control congelado: `relaciones.tsv` tiene **6** filas con `;` en `id_manifiesto` (29
payloads: INE 5, IEC_COAHUILA 7, IEEM_EDOMEX 7, IEEBC_BC 4, IEEZ_ZACATECAS 2,
IEECH_CHIHUAHUA 4), las seis declaran `capa2_manifiesto = SI` — coincide exacto con lo
que `FP-246` medía.

`tools/curador_registro/via_capa2.py`: `id_manifiesto` se parte por `;`, cada id se
resuelve por separado contra `manifiesto.yaml`, la fila entra a `estados_verificacion`
solo si **todos** sus ids coinciden, y el `diff` enumera el estado por id sin colapsar
(A.1).

**Regresión, modo lectura (`--escribe` no se usa en ningún momento de este acto).**
Sobre las filas SIN lista, la salida de `python3 tools/curador_registro/via_capa2.py`
es byte a byte idéntica a la de `origin/main`, salvo el contador agregado
`estados_verificacion` (`AUSENTE`: 54 → 83 — exactamente los 29 payloads de las 6 filas
que ahora sí se examinan). `diffs_propuestos` sigue en `0`.

**Discrepancia medida con el encargo.** El encargo declaraba que en nube las 6 filas
devolverían `raiz-no-configurada` por id. Medido: ninguno de los 29 ids declara `raiz`
propia en `manifiesto.yaml` (`raiz: None` para los 29, verificado uno a uno). Sin `raiz`,
`verificar_entrada()` resuelve contra `root/data/raw/<archivo>`, ausente en esta sesión
de nube → **`AUSENTE`**, no `RAIZ_NO_CONFIGURADA`. El resultado sustantivo no cambia (0
de 29 promueven sin corpus montado), pero el estado exacto sí — se declara aquí en vez de
forzarse a coincidir con el dictado.

Sucesor de caja, sin cambio respecto al encargo: correr `via_capa2.py` con `data/raw`
montada sobre las 6 filas / 29 payloads cierra `FP-246` como `EJECUTADA`.

## P3 — tablero

`forense/firmas-pendientes.tsv`: `FP-258` → `FIRMADA-EJECUTADA` (firma de mesa verbatim
+ lectura de dirección en `firmada_en`; `ejecutada_en` cita el módulo, `T26-bis` y la
regresión). `FP-246` → `FIRMADA`, **NO EJECUTADA** (verificación con corpus queda como
sucesor de caja, declarado en la propia fila). `FP-272` nueva, recibo del acto.
`forense/hallazgos.md`: una línea con el 3→4 de `FP-258`.

## Cascada

- `ADR-320` (`canon/gobernanza-v1_15.md`, derivado por el comando de la casa: máximo
  `319` → candidato `320`; sin colisión conocida con `MAESTRA37-L1`, perímetro disjunto y
  no toca `gobernanza-v1_15.md`). Cabecera de conteo recifrada (`319 ADR` → `320 ADR`).
- `L0` recifrado en `canon/estado-programa-v1_11.md` (línea 105: nueva anotación
  insertada ANTES de la de `ADR-319`, que queda intacta) y las dos citas numéricas de
  `319 ADR` que quedaban sueltas (líneas 27 y 343) — atrapadas por `T25` (`T15` de
  `tests/check.py`, consistencia numérica) al correr la suite: `ROJO` con 1 entrada nueva
  hasta corregirlas, `VERDE` después.
- `canon/registro-rotulos.tsv`: fila nueva `MAESTRA37-N2` (espacio `N`, junto a
  `MAESTRA37-N1`).
- `T25`: ningún rótulo pelado nuevo en el encargo ni en las notas de este acto
  (`_T25_ROTULO_BARE` no matchea sobre ninguno de los dos archivos, verificado con el
  mismo regex del test) — nada que añadir a `_T25_ARCHIVOS_CONOCIDOS`.
- `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE**, `19 FAIL` sin cambio frente
  a `tests/baseline.json`. `baseline.json` NO se recongela (no hace falta: cero entradas
  nuevas de `FAIL`).

## Perímetro — verificado, no solo declarado

Tocado: `forense/encargos/2026-09-03-MAESTRA37-N2-GUARDIA-TSV-Y-CAPA2-LISTAS.md` (nuevo)
· `tools/curador_registro/tsv_crudo.py` (nuevo) · `tools/vista_cola_adquisicion.py` ·
`tools/curador_registro/via_capa2.py` · `tests/check.py` (`T26-bis`) ·
`data/INFRAESTRUCTURA-v1_0.md` · `forense/notas/2026-09-03-MAESTRA37-N2-{control,cierre}.md`
· `forense/hallazgos.md` · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md`
(`ADR-320` + cabecera) · `canon/estado-programa-v1_11.md` (`L0` + 2 citas numéricas) ·
`canon/registro-rotulos.tsv`.

`git diff --stat origin/main..HEAD` confirma que **ningún** archivo fuera de esa lista
cambió, y en particular: **cero** líneas de `data/curacion-registro/*.tsv` (el registro
no se normalizó — verificado, las 4 líneas de `FP-258` y las 6 de `FP-246` quedan tal
cual estaban), `data/manifiesto.yaml` intacto, `data/raw/**` no tocado (no existe en esta
sesión), `milpa/**` intacto, `tools/inventario_reactivos*.py` / `tools/busca_reactivos.py`
/ `.claude/commands/**` intactos (carriles de `MAESTRA37-L1`), y la cola de encargos
(`forense/encargos/cola/`) intacta.

## Estado final

`FP-258`: **EJECUTADA** (vía ii, regresión byte a byte en verde). `FP-246`: **FIRMADA,
NO EJECUTADA** — el script está reparado y su regresión de lectura pasa; la promoción
real de las 6 filas / 29 payloads necesita `data/raw` montada, sucesor de caja.

Este acto no editó ninguna fila de ningún TSV del registro, no verificó contra corpus,
no tocó la cola ni `L10`, no midió, no decidió.
