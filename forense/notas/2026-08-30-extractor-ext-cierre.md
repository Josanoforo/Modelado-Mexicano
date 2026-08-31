# ACTO MAESTRA32-E3 · EXTRACTOR-DTA (v2) — cierre

Corrida única de `tools/inventario_reactivos_ext.py` sobre el perímetro
re-derivado de 133 payloads (125 `.zip` + 8 `.dta` sueltos, causa B de
`data/cobertura-composicion-v1_0.tsv`), siguiendo la especificación congelada
en `forense/notas/2026-08-30-extractor-ext-spec.md` (COMMIT-1). "El primer
resultado que produzca este procedimiento es el que se reporta" — no se
re-ejecutó buscando otro número; la única razón de una segunda corrida
observada en la sesión fue una comprobación de reproducibilidad del comando
(mismo resultado, determinista).

## Resultado (B-bis, ambas coberturas, ambas informativas)

Verificado por comando independiente (`python3 -c "..."` sobre
`data/inventario-reactivos-ext-v1_0.tsv`, `csv.DictReader` saltando la
cabecera `#`):

- **Payloads con ≥1 fila útil (variable_id ≠ ERROR): 123/133 (92.5%).**
  Muy por encima del falsador de COMMIT-1(e) (<50%) — **no se disparó**; no
  se abandona la vía.
- **Filas con `texto_reactivo` no vacío: 24035/63242 (38.0%).** Viene
  enteramente de las familias con etiqueta (`INSPECT_STATA`/`INSPECT_SPSS`);
  las 8596 filas de `INSPECT_RDATA` (única familia R con hits en este
  perímetro) contribuyen 0 a este numerador por diseño de `pyreadr.list_objects`
  (solo nombres de objeto/columna, sin metadato de etiqueta) — declarado en
  COMMIT-1(f), no es un fallo de la corrida.
- Filas totales (sin ERROR): 63242. Filas ERROR: 103 (fallos por payload,
  documentados, no parchados). Por método: `INSPECT_STATA` 37504,
  `INSPECT_SPSS` 17142, `INSPECT_RDATA` 8596. `INSPECT_SAS`/`INSPECT_DBF`:
  0 filas — 0 miembros `.dbf`/`.sas7bdat`/`.xpt` encontrados en los 125 zips
  de este perímetro (dato de COMMIT-1(a); las tres bibliotecas de todas
  formas se cargaron y quedan disponibles para un perímetro futuro que sí
  los tenga).
- Miembros de zip despachados (de las 3 familias): 853. Miembros de otras
  extensiones (xls/pdf/do/zip anidado/sin extensión), contados e ignorados:
  97.
- **5 payloads con SOLO error (0 filas útiles):**
  `endireh2016/bd_mujeres_endireh2016_sitioinegi_RData.zip` (RData con
  encoding inválido), `endireh2021/bd_endireh_2021_RData.zip` (idem),
  `envipe2023/bd_envipe_2023_RData.zip` (idem), `latinobarometro2024_bd_stata.zip`
  (dta con formato Stata no soportado por `pyreadstat`), `osf_interacting_as_equals/Data_SI_F9.dta`
  (encoding no UTF-8 en el archivo mismo). Los 5 quedan documentados con su
  fila `ERROR` cruda en la tabla; ninguno se reintentó con otra heurística.
- Otros 103-5×(errores por payload multi-miembro)… en total 103 filas ERROR
  distribuidas en 10 payloads distintos (5 de ellos ya listados arriba como
  "solo error"; los otros 5 tienen ≥1 fila útil además de algún miembro que
  falló — p. ej. `ADQ15_JPAL.../Replication-files-24ft7wz.zip` (2 miembros
  `__MACOSX/._*` corruptos, resto OK) y `ennvih/eloc02dta_all.zip` (miembros
  bajo subcarpetas comprimidas con un método no soportado por `zipfile`,
  el resto del zip sí se abre).

## Lectura declarada de antemano (COMMIT-1 §f)

Cobertura alta (92.5%) → **el corpus se abre en 123 payloads nuevos para el
sucesor RE-EMPAREJA (E4)**, no un hallazgo de heterogeneidad de formato. La
heterogeneidad real observada es acotada: 2 causas de fallo (RData con
encoding no-latin1/no-utf8 en el propio archivo R, y compresión de zip no
soportada por el módulo estándar `zipfile` de Python) sobre 10/133 payloads.

## Formatos obtenidos / no obtenidos

Las tres bibliotecas se instalaron en el primer intento
(`pip install pyreadstat dbfread pyreadr --break-system-packages`):
`pyreadstat` 1.3.6, `dbfread` 2.0.7, `pyreadr` 0.5.6. **0 formatos NO
OBTENIDOS** — no hubo PARO parcial por ninguna familia.

## Intocables (verificado, `git diff --stat` vacío)

`tools/inventario_reactivos.py`, `tools/etiqueta_v1_2.py`,
`data/inventario-reactivos-v1_0.tsv`, `data/inventario-reactivos-v1_1.tsv`,
`data/inventario-reactivos-v1_2.tsv`, `data/inventario-fd-v1_0.tsv`,
`data/inventario-fd-v1_1.tsv`, `data/cobertura-composicion-v1_0.tsv` — los 8
confirmados sin cambio.

## Residuos

0 archivos en `tmp` (cada extracción de zip usó `tempfile.TemporaryDirectory()`,
limpiado automáticamente al salir del `with`). 0 archivos nuevos en
`data/raw` (este acto no descarga nada; solo lee bytes ya presentes en el
corpus compartido `/home/pc0/Modelado-Mexicano/data/raw`, enlazado por
symlink en este worktree).

## FP-179, entrada (1)

**EJECUTADA por este acto**, con PR (pendiente de abrir al cierre de esta
sesión — ver reporte de la agente). No se encontró que E8 la hubiera marcado
"lanzado" por la secuencia vieja: `forense/firmas-pendientes.tsv` FP-179
listaba la entrada (1) como "encargo archivado, listo" (sin marca de
lanzamiento indebida) — no hizo falta enmienda correctiva sobre ese punto
específico.

## FP pre-asignadas — deviación declarada

El encargo asumía "máximo hoy FP-182; E11 tiene 183-184, E8 185-186" y
pre-asignaba FP-187–FP-188. Re-derivado por comando
(`python3` sobre `forense/firmas-pendientes.tsv`, regex `^FP-(\d+)\t`): el
máximo real hoy es **FP-185** (usada por E8 · MEDICION-COMPUESTA), no 186 —
E8 solo consumió una fila, no dos. FP-186 y FP-187 están libres. Este acto
usa **FP-186** (una sola fila de recibo; el encargo mismo dice "uso: mesa
recibe la cobertura ext... las dos cifras juntas" — una sola entrada de
mesa, no dos) — declarado como corrección al supuesto de la redacción, no
como error del acto.
