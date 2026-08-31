# MAESTRA32-E12 · EXTRACTOR-FD — COMMIT-1 (spec congelada ANTES de abrir un solo payload)

Rama (b) de FP-175. Extiende `data/inventario-fd-v1_1.tsv` (29 instrumentos, .xlsx únicamente) a los formatos que `tools/inventario_reactivos.py:50` manda a `FORMATOS_SIN_CAMPOS` (.pdf, .xls, .html) más .zip que envuelve esos miembros.

## (a) Perímetro re-derivado por comando, por formato

Unión, deduplicada por `payload_id`, de dos conjuntos:

1. `causa B` con `formato=.pdf` en `data/cobertura-composicion-v1_0.tsv` (32 filas: `awk -F'\t' '$4=="B" && $2==".pdf"'`).
2. Payloads cuyo nombre casa el patrón de ficha descriptiva/diccionario que `tools/inventario_fd.py::casa_patron_nombre()` ya usa (token `fd` delimitado, o `diccionario`/`glosario`/`descriptor`), restringido a formato ≠ `.xlsx` — el mismo universo de "46" que registra FP-173.

Verificado: los 32 de (1) son subconjunto estricto de los 46 de (2) (`comm -23` vacío) — el perímetro final de este acto es **46**, no 78. Re-derivado en vivo sobre `data/raw` de este worktree (321 top-level, 696 archivos hasta profundidad 2), NO heredado de memoria de acto anterior.

Lista completa (46), por formato:

**PDF (34):** `FD_ENCUCI2020.pdf`, `eder2017/eder2017_fd.pdf`, `enbiare2021/enbiare_2021_fd.pdf`, `encig2011/fd_encig2011.pdf`, `endireh2003/fd_endireh2003.pdf`, `endireh2021/endireh2021_fd.pdf`, `engasto2012/engasto12_fd.pdf`, `enoe_123_fd_c_bas_amp.pdf`, `enoe_325_fd_c_bas_amp.pdf`, `enpol2021/fd_enpol2021.pdf`, `enti2022/enti_2022_fd.pdf`, `enut2002_fd.pdf`, `enut2009_fd.pdf`, `envipe2014/fd_envipe2014.pdf`, `envipe2015/fd_envipe2015.pdf`, `envipe2016/fd_envipe2016.pdf`, `envipe2017/fd_envipe2017.pdf`, `fd_c_amp_v1.pdf`, `fd_c_amp_v2.pdf`, `fd_c_amp_v3.pdf`, `fd_c_amp_v4.pdf`, `fd_c_bas_amp_15ymas.pdf`, `fd_c_bas_amp_conapo.pdf`, `fd_c_bas_v1.pdf`, `fd_c_bas_v2.pdf`, `fd_envipe2018.pdf`, `fd_envipe2019.pdf`, `fd_envipe2020.pdf`, `fd_envipe2021.pdf`, `fd_envipe2022.pdf`, `fd_envipe2023.pdf`, `fd_envipe2024.pdf`, `fd_envipe2025.pdf`, `fd_iter_cpv2020.pdf`.

**XLS (6):** `elcos2012/elcos_fd.xls`, `endireh2006/fd_endireh06.xls`, `endireh2011/fd_endireh11.xls`, `enut2014_fd.xls`, `envipe2011/fd_envipe2011.xls`, `envipe2012/fd_envipe2012.xls`.

**HTML (4):** `enut2009_diccionario_variables.html`, `enut2014_diccionario_variables.html`, `enut2019_diccionario_variables.html`, `enut2024_diccionario_variables.html`.

**ZIP (2):** `enif_2021_fd_pdf.zip` (envuelve un PDF de ficha descriptiva), `ensafi2023/ensafi_2023_fd_xlsx.zip` (envuelve un XLSX de ficha descriptiva — mismo mecanismo `_xlsx.zip` que ADR-198/ENSAFI-DESCRIPTOR).

## (b) Regla de extracción, cerrada

- **PDF**: primero `pdfplumber.extract_tables()` por página, buscando la primera columna cuyo encabezado normalizado (minúsculas, sin acentos) contenga `nemonico`/`mnemonico`/`nombre`/`variable` (columna id) y otra que contenga `descripcion`/`pregunta`/`etiqueta` (columna texto) — misma lógica de prioridad que `ID_LABELS`/`TEXT_LABELS` de `tools/inventario_fd.py`, adaptada a substring en vez de igualdad exacta (los encabezados de tabla PDF traen envoltura de línea que rompe la igualdad exacta). Si ninguna tabla de la página trae ambas columnas: texto por línea (`page.extract_text()`), regex de mnemónico `^[A-Z][A-Z0-9_]{1,19}$` aplicado a cada línea completa (tras strip); la línea siguiente no vacía es `texto_reactivo`. Regex fijo aquí, no se toca tras ver el resultado (falsador en (e)).
- **XLS**: `xlrd`, misma búsqueda de encabezados que `tools/inventario_fd.py::encuentra_rotulos()`/`ID_LABELS`/`TEXT_LABELS` (reimportadas, no reescritas) fila por fila, encabezado re-evaluado en cada fila.
- **HTML**: `bs4` + `lxml`, cada `<table>`; primera fila con celdas que casen `ID_LABELS`/`TEXT_LABELS` (mismas listas) es el encabezado; filas siguientes son datos.
- **ZIP**: se abre con `zipfile` (stdlib); cada miembro se despacha por su propia extensión con la regla de arriba que le corresponda (pdf→regla PDF, xlsx→se reporta pero NO se re-extrae aquí — `enif_2021_fd_pdf.zip` envuelve pdf, `ensafi2023/ensafi_2023_fd_xlsx.zip` envuelve xlsx: ese miembro xlsx se procesa con la MISMA regla PDF/XLS/HTML no aplica — es xlsx, así que se marca `NO-EXTRAIDO:zip-miembro-xlsx-fuera-de-perimetro` porque extraer xlsx es trabajo de `tools/inventario_fd.py`, no de este acto — perímetro es "no-xlsx"; no se generaliza).

Columnas de salida: exactamente las 9 de `data/inventario-fd-v1_1.tsv` (`payload_id, sha256_12, instrumento, ola, archivo_miembro, variable_id, texto_reactivo, metodo, universo_declarado`). `metodo` ∈ {`INSPECT_PDF_FD`, `INSPECT_XLS_FD`, `INSPECT_HTML_FD`}. `instrumento`: `tools/etiqueta_v1_2.py::aplica_v1_1()` primero, `aplica_v1_2()` después (mismo orden que produjo `inventario-fd-v1_1.tsv`), resto `(sin-instrumento-derivable)`. `payload_id`/`sha256_12` con las funciones de `tools/inventario_reactivos.py` (`sha256_file_12`), sin reimplementar.

## (c) Control positivo, pre-registrado (no se ajusta tras ver el resultado)

- `fd_envipe2025.pdf` → conjunto de `variable_id` extraído se contrasta contra `variable_id` de instrumento `envipe2025` en `data/inventario-reactivos-ext-v1_0.tsv` (1,770 filas — verificado `grep -c envipe2025`).
- `FD_ENCUCI2020.pdf` → conjunto de `variable_id` extraído se contrasta contra las filas cuyo `payload_id` contiene `encuci` en `data/inventario-reactivos-v1_0.tsv` (458 filas — verificado `grep -ic encuci`).
- Umbral: solape ≥ 60% (intersección / conjunto extraído) para VALIDAR el parser de PDF. Por debajo: el parser PDF se reporta `NO VALIDADO`, sus filas se marcan con una décima columna NO — corrección: el esquema es fijo a 9 columnas (intocable), así que un control fallido se declara en la nota de cierre y en el ADR, no en una columna nueva de la tabla.
- El regex de mnemónico y las etiquetas de encabezado NO se tocan después de correr el control. El primer resultado que produzca el procedimiento es el que se reporta.

## (d) Falsador

Cobertura (payloads con ≥1 fila) < 50% del perímetro (46) ⇒ se abandona la vía para ese formato, no se itera sobre el regex/reglas de encabezado.

## (e) B-bis — dos coberturas por formato

1. Payloads con ≥1 fila / total del formato.
2. Filas con `texto_reactivo` no vacío / filas totales del formato.

Alta en ambas ⇒ la capa de texto crece de forma útil para RE-EMPAREJA (E4, nube). Baja ⇒ hallazgo de heterogeneidad real de las fichas (formato no estandarizado), con la lista de payloads que no aportaron filas.

El primer resultado que produzca este procedimiento es el que se reporta.
