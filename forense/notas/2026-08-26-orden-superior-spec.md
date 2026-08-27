# COMMIT-1 · ACTO MAESTRA31-E4 · ORDEN-SUPERIOR — especificación (congelada antes de abrir un solo archivo)

Fecha: 2026-08-26 (ejecutado 2026-08-27). Rama: `maestra31-e4-orden-superior`, contra `main`=`77fddf2`.

## Qué cuenta como reactivo

Propuesta de dirección, ADOPTADA sin refutación: un reactivo es un par `(variable_id, texto)` donde
`variable_id` es un identificador de columna en un archivo de microdato o en un diccionario de datos,
y `texto` es su descripción declarada. Un encabezado de CSV/TSV/TXT/XLSX/DBF sin diccionario adjunto
da `variable_id` con `texto_reactivo` vacío — cuenta como fila, y se marca `metodo=SIN-TEXTO` en
`texto_reactivo`, porque el emparejador de E5 (`construir_crosswalk`, `milpa/src/emisor.py`) trabaja
por token exacto de variable, no por texto libre.

## Esquema exacto (heredado de las cuatro tablas existentes, menos `necesidad`)

```
payload_id	sha256_12	instrumento	ola	archivo_miembro	variable_id	texto_reactivo	metodo	universo_declarado
```

- `payload_id`: ruta relativa del archivo bajo `data/raw` (identificador estable, único por payload físico).
- `sha256_12`: primeros 12 hex del sha256 del payload físico (no del miembro dentro del zip).
- `instrumento`: nombre del directorio contenedor bajo `data/raw` (mejor proxy disponible sin diccionario adicional; NO se infiere semánticamente el nombre del programa — eso sería adjudicación).
- `ola`: `NO_DETERMINADO` — este acto no abre diccionario de instrumento para resolver ola/edición; queda declarado, no inferido.
- `archivo_miembro`: nombre del miembro dentro del contenedor (para ZIP: ruta del miembro; para XLSX: nombre de hoja; para top-level CSV/TSV/TXT/DBF/XLS: el propio archivo o `NO_APLICA`).
- `variable_id`: nombre de columna / campo tal como aparece en el encabezado o diccionario BIFF/DBF.
- `texto_reactivo`: vacío si no hay diccionario adjunto (caso dominante: encabezados crudos).
- `metodo`: qué extractor de `inspect_assets.py` produjo la fila (`INSPECT_ZIP`, `INSPECT_CSV`, `INSPECT_XLSX`, `INSPECT_XLS`, `NO-EXTRAIDO:<formato>`).
- `universo_declarado`: `PRESENTE_EN_DATA_RAW` (constante — este acto no filtra por demanda).

## Formatos atacados y no atacados

`inspect_assets.py::inspect_one()` despacha por extensión. Formatos con soporte de columnas/campos
(dan reactivos): `.csv/.tsv/.txt` (encabezado top-level, vía `inspect_csv`/`decode_header`),
`.xlsx` (primera fila de cada hoja, vía `inspect_xlsx`/openpyxl), `.zip` (recursa un nivel: dentro de
cada miembro `.csv/.tsv/.txt` lee encabezado, dentro de cada miembro `.dbf` lee campos DBF — vía
`inspect_zip`; NO recursa dentro de un zip anidado dentro de otro zip, ni dentro de un xlsx/dbf que
sea a su vez miembro de zip más allá de lo que la función ya hace).

Formatos que `inspect_one()` despacha pero NO producen columnas/reactivos (dan 0 filas de variable,
solo estructura): `.xls` (solo nombres de hoja BIFF, no celdas — `inspect_xls`), `.html` (encabezados
H1-H6, no columnas — `inspect_html`), `.json` (claves de nivel raíz, no reactivos — `inspect_json`),
`.pdf` (encabezados de texto observado, no reactivos — `inspect_pdf`), `.xml` (hijos raíz — `inspect_xml`).
Estos formatos SÍ se abren (para no dejar payloads sin fila alguna en el inventario) pero su fila de
variable, si la hay, queda vacía o es una fila `SIN-CAMPOS-EXTRAIBLES` documentada — no se falsea cobertura.

Formatos SIN soporte en `inspect_one()` (van a `NO-EXTRAIDO:<extensión>`, cero filas de variable):
`.dta` (Stata), `.sav` (SPSS), `.gz`, `.2a`, `.tab` cuando no matchea ningún dispatch, y cualquier
extensión no listada arriba. `inspect_assets.py` NO tiene parser de Stata/SPSS pese a que el
`manifiesto.yaml` cita "spss"/"dta" en descripciones de formato — confirmado por lectura de
`inspect_one()` (líneas 302-312): el dispatch es exhaustivo por `if/elif` sobre 8 extensiones, sin
rama para `.dta`/`.sav`. Esta es la REGLA DE TOPE del encargo aplicada: cero extractores nuevos.

## Denominador de cobertura

Denominador = payloads presentes físicamente en `data/raw` hoy (universo conocido), contados por
`find -L data/raw -mindepth 1 -type f` excluyendo el bucle de symlink `data/raw/raw` (auto-referencia
detectada, ver nota de cierre). Un payload cuenta como "cubierto" si el inventario produjo AL MENOS
UNA fila para él (de variable real o de `NO-EXTRAIDO`/estructura vacía documentada) — es decir,
"cubierto" = "el script lo abrió y produjo un renglón trazable", no "produjo un reactivo con texto".

## Qué significa el resultado (declarado ANTES de correr — B-bis)

Falsador: si la cobertura de payloads (payloads con ≥1 fila producida / denominador) es **<50%**, O
si la tabla resultante tiene **<258 filas totales** (el piso que ya alcanzan las 4 tablas demanda-primero
existentes) → **LA VÍA SE ABANDONA**: se conserva lo producido, no se itera, no se prueba otro formato,
no se mejora el extractor. Se documenta en `forense/hallazgos.md` con la palabra "abandonada".

Si cae entre 50% y el techo (100% de cobertura de payloads, sin techo superior declarado para el
conteo de filas — más filas es simplemente más reactivos encontrados, no un techo a vigilar) se
reporta tal como cae, sin ajustar el criterio.

Si supera todo limpiamente (cobertura alta Y muchas filas), se reporta con las cifras exactas —
eso sería evidencia de que la deuda retroactiva (7 actos que abrieron payloads a mano) era evitable
desde antes.

«El primer resultado que produzca este procedimiento es el que se reporta.»
