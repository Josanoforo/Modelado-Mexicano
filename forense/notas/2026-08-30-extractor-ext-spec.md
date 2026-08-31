# ACTO MAESTRA32-E3 · EXTRACTOR-DTA (v2) — COMMIT-1: especificación congelada

Redactada ANTES de abrir un solo payload de la rama (a). SHA de trabajo: `b371430`
(origin/main al arrancar; el encargo se redactó contra `2799132`, main avanzó 19
commits — ninguno toca `data/cobertura-composicion-v1_0.tsv` ni `tools/inventario_reactivos.py`,
verificado con `git log 2799132..b371430 -- data/cobertura-composicion-v1_0.tsv tools/inventario_reactivos.py`
→ 0 commits).

## (a) Perímetro re-derivado por comando

```
python3 -c "
import csv
with open('data/cobertura-composicion-v1_0.tsv') as f:
    rows=list(csv.DictReader(f, delimiter='\t'))
causaB=[r for r in rows if r['causa']=='B']
print(len(rows), Counter(r['causa'] for r in rows))
"
```
→ 404 filas totales; causa A=204, B=178, C=22 (coincide con el encargo).
Causa B por formato: `.zip` 125 · `.pdf` 32 · `.xls` 7 · `.dta` 8 · `.json` 4 · `.tab` 1 · `.gz` 1 (coincide).
Bucket dentro de causa B: `SIN_CAMPOS` 168 · `NO_EXTRAIDO` 10 (coincide).

**Rama (a) = 125 `.zip` + 8 `.dta` sueltos = 133 payloads.** Lista completa en
`forense/notas/2026-08-30-extractor-ext-perimetro-133.txt` (133 payload_id, un
`git diff --stat` de este acto no la toca porque es un archivo nuevo de este
mismo acto). Verificado: los 133 archivos existen en `data/raw/` (0 faltantes,
comando `Path(RAW/pid).exists()` sobre los 133).

Extensión real de miembros de los 125 zips, derivada con `zipfile.namelist()`
sobre los 125 (0 zips corruptos, 0 excepciones): `.dta` 709 · `.sav` 116 ·
(sin extensión) 42 · `.xls` 28 · `.RData`/`.rdata` 20 · `.pdf` 14 · `.zip` 9
(zip-de-zip, fuera de alcance de este acto) · `.do` 4. **0 miembros `.dbf`,
`.por`, `.sas7bdat`, `.xpt`, `.rds`** en estos 125 zips — dato nuevo, no
anticipado por el encargo (que cita `.dbf`/`.rds` como parte de la firma FP-175
en abstracto, no como presencia confirmada en el perímetro). Esto no cambia el
despacho: las tres bibliotecas se cargan igual, `dbfread`/`pyreadr` simplemente
no encontrarán objetivos de su formato preferido dentro de zips en esta corrida
(`pyreadr` sí aplica a los miembros `.RData`).

## (b) Regla de extracción por familia y regla de despacho

- `.dta/.sav/.por/.sas7bdat/.xpt` → `pyreadstat.read_*(path, metadataonly=True)`
  (función exacta por extensión: `read_dta`, `read_sav`, `read_por`,
  `read_sas7bdat`, `read_xport`). Da `meta.column_names` y
  `meta.column_labels`.
- `.dbf` → `dbfread.DBF(path, load=False).field_names` (solo cabecera; sin
  etiquetas — `texto_reactivo` queda vacío, declarado en la fila).
- `.rdata/.rds` → `pyreadr.list_objects(path)`: lista `[{"object_name":...,
  "columns":[...]}]` por objeto R serializado; sin etiquetas — igual que `.dbf`.
  `pyreadr.read_r()` no se usa (cargaría los datos); `list_objects` es
  metadato puro.

Despacho por payload de la rama:
1. Si `payload_id` termina en `.dta` (los 8 sueltos) → familia Stata directo.
2. Si es `.zip` → `zipfile.namelist()`; para cada miembro cuya extensión
   (case-insensitive) esté en `{.dta,.sav,.por,.sas7bdat,.xpt,.dbf,.rdata,.rds}`:
   extraer a `tempfile.TemporaryDirectory()`, inspeccionar, borrar el
   directorio temporal al salir del `with` (limpieza garantizada aunque falle
   la inspección). Miembros de cualquier otra extensión (`.xls`, `.pdf`,
   `.do`, `.zip` anidado, sin extensión) se cuentan por payload y se ignoran
   — ya los vio o los descartó el inventario general (`FORMATOS_SIN_CAMPOS`/
   `NO_EXTRAIDO` de `tools/inventario_reactivos.py`).

## (c) Columnas

`payload_id, sha256_12, instrumento, ola, archivo_miembro, variable_id, texto_reactivo, metodo, universo_declarado`
(mismo esquema de `data/inventario-reactivos-v1_2.tsv`, verificado por comando
`head -1` sobre esa tabla).

- `variable_id` = nombre de columna/campo (`column_names[i]` de pyreadstat,
  `field_names[i]` de dbfread, `columns[i]` de pyreadr).
- `texto_reactivo` = `column_labels[i]` de pyreadstat si no vacío; `""` para
  dbfread/pyreadr (declarado, no inventado).
- `metodo` ∈ {`INSPECT_STATA`, `INSPECT_SPSS`, `INSPECT_SAS`, `INSPECT_DBF`,
  `INSPECT_RDATA`} — `INSPECT_SAS` cubre tanto `.sas7bdat` como `.xpt` (no
  aparecen instancias en el perímetro re-derivado, pero el despachador los
  soporta si aparecieran).
- `instrumento`: se importan `aplica_v1_1`, `aplica_v1_2`, `familias_canonicas`,
  `carga_manifiesto` de `tools/etiqueta_v1_2.py` (módulo NO editado, solo
  importado — cumple "importado si expone función"). Orden: `aplica_v1_1`
  primero (regex sobre `payload_id`); si no resuelve, `aplica_v1_2` con
  `data/manifiesto.yaml` y las familias canónicas derivadas de
  `data/inventario-reactivos-v1_1.tsv`; si ninguna resuelve,
  `(sin-instrumento-derivable)` — sin forzar heurística nueva.
- `payload_id`, `sha256_12` (`sha256_file_12`), `universo_declarado`
  (constante `"PRESENTE_EN_DATA_RAW"`, misma convención de
  `filas_desde_objetos`) importados/replicados de `tools/inventario_reactivos.py`
  sin editarlo.
- `ola` = constante `NO_DETERMINADO` (misma convención que
  `tools/inventario_reactivos.py:110`).
- `archivo_miembro` = nombre del miembro dentro del zip, o el propio
  `payload_id` para los 8 `.dta` sueltos.

## (d) Codificaciones

La que la biblioteca detecte automáticamente (pyreadstat/dbfread/pyreadr
manejan su propia detección de encoding interna). Un fallo de lectura (I/O,
formato corrupto, encoding no decodificable, excepción de la biblioteca)
produce **una fila de error** por payload — no reintento, no parche, no
heurística de encoding manual. Fila de error: `variable_id="ERROR"`,
`texto_reactivo=<mensaje crudo de la excepción, truncado a 200 chars>`,
`metodo=<INSPECT_* correspondiente>`.

## (e) Falsador

Cobertura del perímetro = payloads con ≥1 fila de variable_id / 133
(re-derivado, no el 133 heredado de la redacción — coincide tras
re-derivación). **Si < 50% ⇒ se abandona la vía tal como está, no se itera la
regla** (precedente E4/E6 de la cascada). Esta cifra se calcula EN COMMIT-2,
después de correr; aquí solo se congela el umbral y el denominador.

## (f) B-bis — declarado antes de ver el dato

Se reportan dos coberturas, ambas informativas, ninguna sustituye a la otra:
1. **Payloads con ≥1 fila** sobre 133 (cualquier variable_id extraído, con o
   sin etiqueta).
2. **Filas con `texto_reactivo` no vacío** sobre el total de filas producidas
   (las familias `.dbf`/`.rdata` solo dan nombres, nunca contribuyen aquí por
   diseño de biblioteca — declarado, no es un fallo).

Lectura declarada de antemano: alta cobertura (1) = el corpus se abre en N
payloads nuevos para el sucesor RE-EMPAREJA (E4); baja = hallazgo de
heterogeneidad de formato, con la lista concreta de qué payload/familia
falló y por qué. Ambos resultados son informativos — ninguno es "el acto
falló".

**Cierre de este COMMIT: el primer resultado que produzca este procedimiento
es el que se reporta** (no se re-ejecuta buscando un número distinto).

## Herramientas — versión obtenida

| familia | biblioteca | versión | estado |
|---|---|---|---|
| Stata/SPSS/SAS | `pyreadstat` | 1.3.6 | OBTENIDA (pip install --break-system-packages) |
| dBase | `dbfread` | 2.0.7 | OBTENIDA |
| R | `pyreadr` | 0.5.6 | OBTENIDA |

Las tres se instalaron en el primer intento (`pip install pyreadstat dbfread
pyreadr --break-system-packages`), sin necesidad de PARO parcial. 0 formatos
NO OBTENIDOS.

## Intocables declarados (verificación al cierre con `git diff --stat`)

`tools/inventario_reactivos.py`, `tools/etiqueta_v1_2.py`,
`data/inventario-reactivos-v1_0.tsv`, `data/inventario-reactivos-v1_1.tsv`,
`data/inventario-reactivos-v1_2.tsv`, `data/inventario-fd-v1_0.tsv`,
`data/inventario-fd-v1_1.tsv`, `data/cobertura-composicion-v1_0.tsv`.
