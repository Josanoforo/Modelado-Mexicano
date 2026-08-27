# ACTO MAESTRA31-E4 · ORDEN-SUPERIOR — nota de cierre

Fecha: 2026-08-26 (ejecutado 2026-08-27). Rama `maestra31-e4-orden-superior`, contra `main`=`77fddf2`.
Encargo archivado verbatim: `forense/encargos/2026-08-26-MAESTRA31-E4-ORDEN-SUPERIOR.md`.
Spec congelada antes de correr (COMMIT-1): `forense/notas/2026-08-26-orden-superior-spec.md`.

## 0 · Verificación de existencia (obligatoria antes de construir nada)

Ninguna de las cuatro señales que el encargo pedía vigilar apareció: no existe otra tabla
de reactivos, ningún modo "profundo" corrido de `inspect_assets.py` (solo existe
`MINIMA_ESTRUCTURAL_NEUTRAL`, verificado leyendo el archivo completo — no hay parámetro
`profundo` ni `grado_inspeccion` alterno), y no hay otra rama con este trabajo (`git branch
-a` sin ramas `*orden-superior*`/`*inventario-reactivos*` salvo la propia). El "80% ya
construido" que citaba el encargo se confirma exactamente (ver §1).

## 1 · Verificación de las cifras citadas por dirección — TODAS reconciliadas exactas

Comandos re-corridos contra el árbol real (`c615bfd`, tras COMMIT-1):

```
$ awk -F'\t' 'NR>1 && $14!=""{n++} END{print n" de "NR-1}' data/curacion-universo/reportes-inspeccion.tsv
1527 de 1527
```
```
$ awk -F'\t' 'NR>1{print $14}' data/curacion-universo/reportes-inspeccion.tsv | sort -u
contenido fuera de la frontera
contenido más allá de la frontera declarada
documentación semántica o contenido completo, si una orden superior lo solicita
```
```
$ awk -F'\t' 'NR>1{print $12}' data/curacion-universo/reportes-inspeccion.tsv | sort | uniq -c | sort -rn | head -1
646  Se abrió el contenedor completo y se enumeró su directorio central; solo se leyeron
     encabezados de miembros CSV/TSV/TXT/DBF con compresión soportada, no el contenido
     completo de los demás miembros.
```
```
$ awk -F'\t' 'NR>1{print $9}' data/curacion-universo/reportes-inspeccion.tsv | grep -cE "P[0-9]+_[0-9]+|VAR[0-9]|variable"
2
```
```
$ awk -F'\t' 'NR>1{print $8}' data/curacion-universo/universo-declarado-t0.tsv | sort | uniq -c
    509 ADQUIRIDO
  35199 DECLARADO_NO_ADQUIRIDO
```
(35,708 activos totales = 509 + 35199, coincide con "35,708 activos" citado.)

```
$ n=0; for f in data/reapertura-52a-54-variables-2026-08-13.tsv data/abrir4-variables-2026-08-08.tsv \
    data/apertura-issp-variables-2026-08-13.tsv data/apertura-enfih-ensafi-v1_0.tsv; do
    echo "$f -> $(( $(wc -l < "$f") - 1 )) filas"; done
data/reapertura-52a-54-variables-2026-08-13.tsv -> 208 filas
data/abrir4-variables-2026-08-08.tsv -> 28 filas
data/apertura-issp-variables-2026-08-13.tsv -> 14 filas
data/apertura-enfih-ensafi-v1_0.tsv -> 8 filas
```
208+28+14+8 = **258**, exacto.

```
$ find tools/curador_registro -iname "materialize_inspection_contracts.py"
tools/curador_registro/materialize_inspection_contracts.py   (líneas 19-22: REQUIRED
    incluye grado_inspeccion y criterio_parada -- confirmado)
$ find . -iname "inspector-contract.schema.json"
./data/curacion-registro/ejecucion-semantica/schemas/inspector-contract.schema.json
```

**Las seis cifras citadas por dirección (35,708 · 1527/1527 · 646 · 2 · 258 · 509) se
verifican EXACTAS, sin corrección.** Ninguna requirió ajuste.

## 2 · Paso 1 del encargo — universo conocido y su solape (los tres números, sin fusionar)

```
$ find -L data/raw -type f 2>/dev/null | wc -l
720
```
(`data/raw` es symlink a `/home/pc0/mm-corpus/raw`. Hallazgo aparte, no pedido por el
encargo: `/home/pc0/mm-corpus/raw/raw` es un symlink que apunta a sí mismo — auto-referencia
detectada por `find -L` con `bfs: error: data/raw/raw: Filesystem loop back to data/raw`,
excluida explícitamente de todos los conteos de este acto. No se investiga su origen —
fuera de perímetro — pero queda declarado aquí para que un acto futuro no tropiece con la
misma advertencia sin saber qué es.)

```
$ python3 -c "import yaml; print(len(yaml.safe_load(open('data/manifiesto.yaml'))))"
794
```

```
$ find -L data/raw -mindepth 1 -maxdepth 1 2>/dev/null | wc -l
321
```

**Las dos cifras de dirección (794 en `manifiesto.yaml`, 321 en `data/raw` según
`ACTO MAESTRA31-E1`) NO se contradicen — miden cosas distintas, reconciliado:**
- **794** = entradas de `data/manifiesto.yaml` (registro de adquisición, un registro por
  descarga declarada, puede incluir entradas para archivos que ya no están en `data/raw`
  o que viven en otra ruta).
- **321** = entradas de **primer nivel** (`-maxdepth 1`) bajo `data/raw`: 231 archivos +
  90 directorios. `ACTO MAESTRA31-E1` contó el nivel superior, no recursivo.
- **720** = archivos **recursivos** bajo `data/raw` (`-type f`, sin límite de profundidad,
  excluyendo el ciclo `raw/raw`) — este es el "universo conocido" que usa este acto,
  porque muchos de los 90 directorios de primer nivel contienen más de un payload.

Solape con lo ya inspeccionado (509 activos `ADQUIRIDO` en
`data/curacion-universo/universo-declarado-t0.tsv`):

```
$ awk -F'\t' 'NR>1 && $8=="ADQUIRIDO"{print $9}' data/curacion-universo/universo-declarado-t0.tsv > rutas509.txt
$ while read -r p; do [ -f "data/raw/$p" ] && echo OK || echo MISSING; done < rutas509.txt | sort | uniq -c
    509 OK
```
**Los 509 activos `ADQUIRIDO` del universo T0 son un subconjunto exacto de los 720
archivos recursivos de `data/raw` hoy** (509 de 509 rutas existen). Los 211 archivos
restantes (720−509) están físicamente en `data/raw` pero no aparecen como activo
`ADQUIRIDO` en el universo T0 — llegaron después del snapshot T0 (13/ago) o por actos
posteriores (p.ej. `ADQ15_CNBV_*`, trimestres de ENOE `20XXtrimN_csv.zip`, exportes
`202608131[3-4]00.export.CSV.zip`, etc.). **Los tres números, sin fusionar: 794
(manifiesto) · 321 (primer nivel de data/raw) · 720 (recursivo de data/raw, universo usado
por este acto) · 509 (subconjunto ya inspeccionado estructuralmente por el curador,
100% presente en los 720).**

## 3 · Ejecución del inventario (paso 3 del encargo)

Script delgado: `tools/inventario_reactivos.py` (fuera de `tools/curador_registro/`, NO
edita ese módulo — solo importa `inspect_one` de `tools/curador_registro/inspect_assets.py`).
Regla de tope respetada: cero parsers nuevos escritos; todo formato sin dispatch en
`inspect_one()` va a `NO-EXTRAIDO:<extension>`.

Corrida completa (`data/raw` entero, 720 payloads), tiempo real:

```
$ time python3 tools/inventario_reactivos.py
{
  "conteo_por_estado": {
    "NO-EXTRAIDO:2a": 6,
    "NO-EXTRAIDO:dta": 8,
    "NO-EXTRAIDO:gz": 1,
    "NO-EXTRAIDO:tab": 1,
    "OK": 316,
    "SIN-CAMPOS-EXTRAIBLES": 388
  },
  "denominador_payloads": 720,
  "filas_totales": 178246,
  "payloads_cubiertos": 704
}
real    2m23.601s
```
Corrida completa dos veces (segunda vez tras el saneado de celdas descrito abajo), ambas
con los mismos conteos exactos — determinista.

Criterio de corte de tiempo/profundidad usado, documentado (spec §"Formatos atacados"):
`inspect_zip` recursa un nivel (miembros CSV/TSV/TXT/DBF dentro del zip), no zips
anidados dentro de zips ni xlsx/dbf empaquetados más allá de eso — es el límite que ya
trae `inspect_assets.py`, no uno nuevo que este acto haya impuesto. No se truncó ningún
archivo por tiempo: el único límite declarado (90s/archivo) no se alcanzó en ninguna fila
(`grep -c ":LENTO=" data/inventario-reactivos-v1_0.tsv` → 0). Los dos zips más pesados del
corpus (`ADQCORRE_R74R75_GDELT/GDELT.MASTERREDUCEDV2.1979-2013.zip`, 1.1 GB, y
`zenodo_electoral_precinct_level_mexico_municipal.zip`, 706 MB) se procesaron dentro de la
corrida completa sin exceder el límite.

**Hallazgo de saneado (no un defecto del extractor, un defecto de mi propio script,
corregido en la misma sesión antes de comitear):** la primera corrida usó
`csv.DictWriter` para escribir el TSV; algunas celdas `texto_reactivo` provenientes de
diccionarios `.xlsx` (p.ej. `ADQ15_CNBV_AhorroFinanciero_Financiamiento/Diccionario_DGEE.xlsx`)
traen saltos de línea embebidos, que `csv.DictWriter` cita entre comillas — rompiendo la
convención de este repo (TSV plano, una línea por fila, sin comillas CSV, verificada contra
las 4 tablas de variables existentes: `grep -c '"' data/abrir4-variables-2026-08-08.tsv` → 0).
Es el mismo defecto que `feedback_csv_module_corrompe_tsv` ya documentó para este proyecto
y que `ADR-127`/`gobernanza:2520` narra explícitamente ("nunca con el módulo csv, que ya
corrompió este archivo dos veces antes"). Corregido: `sanitiza_celda()` colapsa
tab/CR/LF a espacio antes de escribir, y la escritura final es `"\t".join(...)` manual, sin
`csv.DictWriter`. Verificado en el archivo final: `awk -F'\t' '{print NF}' ... | sort -u` →
únicamente `9` (el número de columnas del esquema, ninguna fila rota) y
`grep -c '"' data/inventario-reactivos-v1_0.tsv` → `0`.

## 4 · Esquema y muestra

```
$ head -1 data/inventario-reactivos-v1_0.tsv
payload_id  sha256_12  instrumento  ola  archivo_miembro  variable_id  texto_reactivo  metodo  universo_declarado
$ wc -l data/inventario-reactivos-v1_0.tsv
178247   (178246 filas de datos + 1 cabecera)
```
`ola` = `NO_DETERMINADO` en el 100% de las filas (declarado en COMMIT-1: este acto no abre
diccionario de instrumento para resolver ola/edición — es una columna presente en el
esquema pero sin fuente que la llene en esta pasada; no se inventa un valor).
`texto_reactivo` no vacío únicamente en filas provenientes de diccionarios `.xlsx`
explícitos (p.ej. `Diccionario_DGEE.xlsx`, `Glosario_Base_de_Ahorro_Financiero_...xlsx`);
la inmensa mayoría de filas son encabezados crudos de CSV/TSV/TXT dentro de ZIP
(`metodo=INSPECT_ZIP`, 174,459 de 178,246 filas — 97.9%) y llevan `texto_reactivo` vacío,
exactamente el caso `SIN-TEXTO` que COMMIT-1 previó (la columna `metodo` identifica el
extractor; no se añadió una columna `SIN-TEXTO` separada porque `texto_reactivo` vacío ya
es esa señal sin redundancia — nombrado aquí para que quede explícito, no oculto).

## F1 · enmienda 2026-08-27 — retractación de §4 y alcance medido del hueco en diccionarios

**Autoriza esta enmienda:** el propio encargo, paso 3 («COMMIT-2 — la tabla... enmienda por
adición si hace falta, nunca corrección hacia atrás»); el precedente ya corrido en este
programa bajo el mismo texto («tercer commit → lo dice; nunca se corrige hacia atrás»,
`gobernanza:2883`, `R10.1`) y bajo el mismo rótulo `F1` (`gobernanza:3813`,
`ACTO MAESTRA30-E8`, enmienda dentro de `prereg-corrida-v1_0.md`); e instrucción directa
de dirección en sesión de seguimiento, 27/ago/2026, ordenando el tercer commit y las dos
derivaciones de abajo antes de escribirlo. El texto de §4 arriba **no se toca**.

### F1.1 · Retractación nombrada

La frase de §4 «`texto_reactivo` no vacío únicamente en filas provenientes de diccionarios
`.xlsx` explícitos (p.ej. `Diccionario_DGEE.xlsx`, `Glosario_Base_de_Ahorro_Financiero_...xlsx`)»
es **falsa**:

```
$ awk -F'\t' 'NR>1 && length($7)>0{c++} END{print c+0}' data/inventario-reactivos-v1_0.tsv
0
```

`texto_reactivo` está vacío en el 100% de las 178,246 filas, **sin excepción** — incluidas
las de los dos archivos citados por nombre en §4. Lo que de verdad ocurre en esas dos filas,
confirmado con los bytes crudos: el párrafo descriptivo del diccionario cayó en `variable_id`
(columna 6), no en `texto_reactivo` (columna 7). §4 describió el defecto correcto en el
archivo correcto y en la columna equivocada.

### F1.2 · El mecanismo, con lo que se abrió y lo que no

`inspect_xlsx` toma la primera fila de cada hoja como candidatos a `variable_id`. Las fichas
descriptivas de INEGI anteponen a cada hoja un bloque de portada de 5-6 renglones
(nombre de la encuesta, «ESTRUCTURA DEL ARCHIVO», «Tabla de datos: `<hoja>`», renglón vacío)
antes de la tabla de variables real. Dos síntomas del mismo defecto, según dónde cae ese
bloque: si empieza en la fila 1, `inspect_xlsx` captura su celda como un `variable_id` falso
de una sola fila por hoja (`SOLO-TÍTULO`); si hay un renglón en blanco antes (fila 1
totalmente vacía), no captura nada y la hoja aporta cero filas (`SIN-FILAS`) — la tabla de
variables real nunca se alcanza en ningún caso.

Evidencia directa reunida para esta enmienda, **13 de 69** candidatos (el resto se clasifica
en F1.3 por consulta sobre la tabla ya producida, no por apertura):

- **Fuente abierta con `openpyxl`/`pdf_extract` (5):** `enasem2018/enasem_2018_fd.xlsx`
  (título en fila 1 de 11 hojas) · `enasic2022/enasic_2022_fd.xlsx` y `enif_2024_fd.xlsx`
  (fila 1 vacía, título en fila 2 columna B — el síntoma `SIN-FILAS`) ·
  `ADQ15_CNBV_BDIF_inclusion_financiera/Diccionario_DGPASF.xlsx` (sin bloque de portada:
  fila 1 = `Nombre de la BD | Nombre de la columna | Descripción | Tipo de dato`, encabezado
  real) · `eder2017/eder2017_fd.pdf` (vía `tools/curador_registro/pdf_extract.extract_pdf()`,
  el extractor ya existente, invocado solo para lectura: página 1 = «Encuesta Demográfica /
  Retrospectiva 2017 / EDER / Descripción de la base de datos» — la misma convención de
  portada institucional, en pdf).
- **Fila de la tabla ya producida, leída directamente (8):** `Diccionario_DGEE.xlsx`,
  `Glosario_Base_de_Ahorro_Financiero_y_Financiamiento.xlsx`,
  `Glosario_Datos_Abiertos_DGASF.xlsx` (hermano de `DGPASF`, mismo encabezado real, 36
  filas), `mociba2015_fd.xlsx`, `mociba2016_fd.xlsx`, `mociba2017_fd.xlsx`,
  `mociba2019_fd.xlsx`, `diccionario_cuestionario_ampliado_cpv2020.xlsx`.

`ADQ15_CNBV_BDIF_inclusion_financiera` (DGPASF/DGASF) es un subprograma distinto de
`ADQ15_CNBV_AhorroFinanciero_Financiamiento` (DGEE) dentro del mismo lote CNBV — el defecto
no es del formato `.xlsx` en general, es de la plantilla de portada que un subprograma usa y
el otro no.

### F1.3 · Derivación 1 — el converso

El patrón de nombre que el encargo original citó (`*_fd.xlsx`, `Diccionario_*`, `Glosario_*`)
resultó incompleto: no cubre el convenio con el token al inicio (`fd_*`), usado por
`fd_enif2012.xlsx`, `FD_ENDUTIH2023.xlsx`, la mayoría de los `.pdf`, etc. Ampliado antes de
contar:

```
$ find -L data/raw -type f \( -iname '*_fd.*' -o -iname 'fd_*' -o -iname 'diccionario*' -o -iname 'glosario*' \) 2>/dev/null | wc -l
69
$ find -L data/raw -type f \( -iname '*_fd.*' -o -iname 'fd_*' -o -iname 'diccionario*' -o -iname 'glosario*' \) 2>/dev/null | sed 's/.*\.//' | tr 'A-Z' 'a-z' | sort | uniq -c
     32 pdf
      6 xls
     31 xlsx
```

Cruzando esos 69 `payload_id` contra `data/inventario-reactivos-v1_0.tsv` (campo 6,
`variable_id`, clasificado por longitud >60 caracteres como proxy inicial de «texto de
portada, no variable», refinado a mano en los 5 casos que el proxy dejaba ambiguos —
resultaron ser el mismo síntoma con cadena corta: nombre de hoja «ÍNDICE»/«DIAGRAMA
ENTIDAD-RELACIÓN» o de sección censal «MIGRANTES»/«PERSONAS»/«VIVIENDAS», no una variable),
de los **31 `.xlsx`**:

- **2 de 31 — `EXTRAJO-VARIABLES` real:** `Diccionario_DGPASF.xlsx` y
  `Glosario_Datos_Abiertos_DGASF.xlsx`, 36 filas cada uno, 72 reactivos reales con
  `variable_id` corto y `texto_reactivo`... vacío también (mismo límite de F1.1: el
  encabezado real de 4 columnas no incluye la celda de descripción como fila propia).
- **24 de 31 — síntoma (título o nombre de sección como `variable_id` falso):** 19 con
  todas sus filas largas (`SOLO-TÍTULO` puro) + 5 reclasificados tras inspección
  (`diccionario_cuestionario_ampliado_cpv2020.xlsx`, `mociba2015/16/17/19_fd.xlsx`).
- **5 de 31 — `SIN-FILAS`:** `enasic2022_fd.xlsx`, `enfih_2019_fd.xlsx`, `enif_2024_fd.xlsx`,
  `enut2019_fd.xlsx`, `enut2024_fd.xlsx` (2 de 5 confirmados por apertura, ver F1.2; los
  otros 3 comparten el mismo resultado de cero filas en la tabla, no abiertos
  individualmente).

**Respuesta al converso: no es 30 de 30 — es más parejo de lo que §4 hacía parecer en un
sentido y más duro en otro.** Solo 2 de 31 `.xlsx` con nombre de diccionario extrajeron
variables reales (6.5%); pero esos 2 lo hicieron limpio (72 filas, cero ambigüedad), y los
otros 29 (93.5%) no aportan ninguna definición utilizable, ni siquiera parcial.

### F1.4 · Derivación 2 — el otro formato

De los 69, **38 no son `.xlsx`** (32 `.pdf` + 6 `.xls`). Cruzados contra la tabla:

```
$ awk -F'\t' 'NR==FNR{c[$0]; next} $1 in c{n++} END{print n+0}' <(find -L data/raw -type f \( -iname '*.pdf' -o -iname '*.xls' \) \( -iname '*_fd.*' -o -iname 'fd_*' -o -iname 'diccionario*' -o -iname 'glosario*' \) 2>/dev/null | sed 's|^data/raw/||') data/inventario-reactivos-v1_0.tsv
0
```

**0 de 38 (0%) produjeron una fila de `variable_id`** — ninguna sorpresa nueva: COMMIT-1 ya
declaraba `.pdf` («encabezados de texto observado, no reactivos») y `.xls` («solo nombres de
hoja BIFF, no celdas») sin soporte de columnas, y el resultado mide exactamente ese límite
declarado, no lo desmiente.

Lo que sí responde la pregunta de fondo — ¿es la portada un vicio de `.xlsx` o una convención
de INEGI que cruza formato: **confirmado en pdf** (`eder2017_fd.pdf`, F1.2): la misma
convención de portada institucional (nombre de encuesta antes de cualquier tabla) aparece en
al menos un `.pdf`, no verificado en los 31 restantes. Es institucional, no de un formato
—pero en pdf es irrelevante para el resultado, porque `inspect_pdf` nunca intentó producir
columnas ahí; en xlsx sí importa, porque `inspect_xlsx` sí lo intenta y la portada es
precisamente lo que se lo impide.

### F1.5 · Corrección al significado de la cifra de cobertura

No es un matiz: el número dice otra cosa de la que suena. Los 30 (ahora 69) payloads con
nombre de diccionario cuentan como «cubiertos» bajo la definición de COMMIT-1 («produjo al
menos una fila trazable, real o de estructura vacía documentada») — y lo están, literalmente
— pero 67 de 69 (97.1%) están cubiertos **solo de nombre**: ni una definición de variable
legible. `FP-171` se corrige por adición con los dos números (ver fila actualizada en
`forense/firmas-pendientes.tsv`); el `CONTADOR` de `ADR-213` (704/720, 178,246 filas) no
cambia — sigue siendo la cifra correcta para la pregunta que responde, cobertura de
extracción, no cobertura semántica.

### F1.6 · Lo que COMMIT-1 esperaba y el dato refutó

COMMIT-1 trató `SIN-TEXTO` como la excepción («un encabezado de CSV sin diccionario da
`variable_id` con texto vacío») — la expectativa implícita era que un encabezado *con*
diccionario adjunto sí traería texto. El dato lo refuta: **el 100%** de las filas —
incluidas las que sí provienen de un diccionario explícito — llevan `texto_reactivo` vacío,
porque ningún método de `inspect_one()` lee una celda de descripción como campo distinto de
`variable_id`; el diccionario, cuando se abre, se lee con el mismo método ciego que un
encabezado crudo. Esto no es un defecto de quien ejecutó COMMIT-2: es una expectativa de
dirección que el resultado refutó, y se registra como tal, no se disculpa.

### F1.7 · Lo que esto NO cambia

El veredicto del falsador (§5, abajo) se sostiene sin ajuste: la cobertura y el conteo de
filas que lo evalúan son cifras de extracción, no de contenido semántico, y esta enmienda no
las toca. `E5` empareja por token exacto de `variable_id`, no por `texto_reactivo` (COMMIT-1,
`spec §"Qué cuenta como reactivo"`) — que el texto esté vacío al 100% no bloquea el cruce
inverso que este acto habilita. Lo que sí cambia es que el corpus no tiene hoy la capa de
texto que haría ese cruce legible para un humano sin abrir el archivo fuente. No se reabre
`inspect_xlsx` para las fichas descriptivas — sería un quinto extractor con otro nombre, y el
encargo lo prohíbe por escrito; el hueco queda revelado y medido, y abrirlo es acto sucesor
con decisión propia, con un argumento más fuerte a su favor precisamente por haber sido
medido aquí. No se re-corre nada de COMMIT-2 ni de esta corrida.

## 5 · Falsador (declarado en COMMIT-1) — evaluado

- Cobertura: 704/720 = **97.78%** (umbral de abandono: <50%). **NO se cruza.**
- Filas totales: **178,246** (umbral de abandono: <258). **NO se cruza.**

**El falsador NO SE DISPARÓ.** Cae muy por encima del techo declarado en COMMIT-1 ("si
supera todo limpiamente, repórtalo también con las cifras") — 690× el piso de 258 filas
que alcanzaban las 4 tablas demanda-primero combinadas, con 97.78% de cobertura de
payloads. No se itera, no se prueba otro formato, no se mejora el extractor — la vía no
requiere abandono ni ajuste; se reporta tal como cayó.

## 6 · Deuda retroactiva (§3 del encargo)

Siete actos citados por dirección como habiendo abierto payloads a mano en las últimas
tres semanas: E1, R34-ENSAFI-CENSA, APERTURA-ENFIH-ENSAFI, REAPERTURA-52A-54, ABRIR-4,
INDICE-NO-INEGI, BIBLIOTECARIO-56. Este acto no re-verifica esa cuenta caso por caso
(fuera de lo pedido: el encargo la cita como motivación, no como cifra a re-derivar), pero
confirma la condición estructural que la hace cierta: antes de este acto, cero tablas del
repo tenían una fila por reactivo sin filtro de demanda (§1, `grep -cE` → 2 de 1527 filas).
Con `data/inventario-reactivos-v1_0.tsv` esa consulta ahora es posible sin abrir un solo
payload a mano — 178,246 reactivos consultables por `variable_id`/`instrumento`, aunque
sin texto en el 97.9% de los casos (encabezados crudos).

## 7 · Qué NO hizo este acto (perímetro respetado)

Cero emparejamiento contra `milpa/` o contra ninguna tabla de variables existente. Cero
columna `necesidad` o filtro de demanda. Cero red/API (`grep -n "requests\.\|urllib\.\|http"
tools/inventario_reactivos.py` → sin resultados). Cero adquisición. Cero adjudicación de
casilla/letra/tier. Cero edición de `tools/curador_registro/**` (verificado contra el
origen real, no una rama local potencialmente vieja —
`git diff --stat origin/main -- tools/curador_registro/` vacío tras este acto; el diff
completo contra `origin/main` toca exactamente 5 archivos, todos nuevos, cero ediciones
a archivos preexistentes: `data/inventario-reactivos-v1_0.tsv`,
`data/inventario-reactivos-v1_0.tsv.meta`, el encargo archivado, la spec de COMMIT-1 y
`tools/inventario_reactivos.py`).

## 8 · Extensión de perímetro declarada

`data/inventario-reactivos-v1_0.tsv.meta` (archivo hermano nuevo, no listado por nombre
en el perímetro del encargo pero previsto por su texto — "líneas que empiecen con # ...
o un archivo .meta hermano si mezclar comentarios en el TSV complica el parseo", paso 4):
contiene el universo declarado (SHA del listado, fecha, denominador, conteo NO-EXTRAIDO
por formato) que el encargo pedía en la cabecera del TSV. Se optó por el archivo hermano
en vez de líneas `#` dentro del TSV para no romper la convención de este repo de que la
línea 1 de un TSV es la cabecera real (varias herramientas del repo asumen esto con
`awk -F'\t' 'NR==1{...}'`).
