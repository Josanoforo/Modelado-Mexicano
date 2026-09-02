# ACTO MAESTRA34-L3 · CORPUS-SANO-Y-CNGMD — nota de cierre

**Encargo:** `forense/encargos/2026-09-01-MAESTRA34-L3-CORPUS-SANO-Y-CNGMD.md`
(dirección/Fable, 1/sep/2026, SHA de redacción `3c3ab3a`).
**Entorno:** UBUNTU (caja). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`;
`https://www.inegi.org.mx/` → 200; `https://www.ine.mx/` → 200; `data/raw/` con 366
entradas al arrancar. **Base:** `origin/main = e4af4ed` (el encargo declaraba
`3c3ab3a`; main se movió un merge, y ese merge es el que archivó este encargo).

---

## 0 · COMPUERTA — no se cumplió, y el encargo lo previó

`GATED a MAESTRA34-N6 fusionado`, verificable por los dos productos que el propio
encargo declara. Medidos contra `origin/main = e4af4ed` el 1/sep/2026:

| producto declarado | comando | resultado | veredicto |
|---|---|---|---|
| `data/raw` dentro de T27 > 0 | `git show origin/main:tests/check.py` acotado a `t27_infraestructura` (l. 3805-3834) | **0** | **FALLA** |
| control positivo del comando anterior (A.13) | `grep -c 'T27'` sobre el mismo tramo | 3 | el comando sí examinó el cuerpo |
| `baseline.json` recongelado después de `c6a0d72` | `git log -1 origin/main -- tests/baseline.json` | `e597a94`, 31/ago 05:31 | literal SÍ, pero es `CI: --freeze … to unblock PR #398`, **anterior a N6** |

De `MAESTRA34-N6` solo está fusionado el **encolado de su encargo** (`PR #455`,
`[COLA] encola MAESTRA34-N6/L3 + enmienda N3`); su P1 no se ha ejecutado. Se
procedió por la cláusula explícita del encargo — *«si igual se lanza, reporta como
A1 (ROJO-solo-T27) y no PARA»* — y la cascada cierra en ROJO-solo-T27, igual que
hizo `MAESTRA34-A1`.

**Consecuencia colateral del gate ausente, no prevista por el encargo:** el
perímetro manda escribir las tres capas del curador *«por la vía de N6»*. Esa vía
—la sección «alta de fuente nueva en tres tablas» de `GUIA-CURADOR-REGISTRO.md`—
es P3 de N6 y **no existe**: `grep -i 'alta de fuente'` sobre la GUIA da 0 y su
único índice es `## via_capa2.py`. `FP-230` sigue viva. P3 escribió las tres capas
a mano contra el esquema vigente y cerró con el validador en verde; la vía sigue
sin documentar.

---

## 1 · P1 · SYMLINK — la verificación que el encargo propuso no podía moverse

`/home/pc0/mm-corpus/raw/raw -> /home/pc0/mm-corpus/raw` (12/ago/2026) eliminado
con `rm` del enlace, nunca `rm -r`, tras comprobar `[ -L ]`. Destino intacto:
366 → 365 entradas, y la diferencia es exactamente el enlace.

| medida | comando | antes | después |
|---|---|---|---|
| symlinks de nivel 1 en el corpus | `find /home/pc0/mm-corpus/raw -maxdepth 1 -type l` | 1 | **0** |
| symlinks a cualquier profundidad | `find /home/pc0/mm-corpus/raw -type l` | 1 | 0 |
| ficheros vistos por `find` | `find -L data/raw -type f` | 771 | **771 — sin cambio** |
| avisos de bucle por stderr | idem, stderr | 1 línea | 0 |
| entradas vistas por el glob de T27 | `glob.glob(data/**/*, recursive=True)` | 35 672 | **1 117** |
| · de ellas, ficheros | idem | 31 054 | 985 |
| · fantasmas bajo `data/raw/raw/…` | idem | **30 069** | 0 |

**Hallazgo.** La segunda verificación que el encargo pide («que `find data/raw -type f`
baje al conteo real») es **insensible al defecto que P1 repara**: GNU `find -L` ya
detectaba el ciclo y lo saltaba con `File system loop detected`, así que 771 → 771
es el resultado correcto de un comando que nunca vio el bucle. Aceptar ese 771→771
como prueba de que la reparación falló habría sido un falso negativo del arreglo.
Quien mide el daño es el patrón exacto de `t27_infraestructura`, que no tiene
guardia de bucle — Python 3.14.4 sigue recursando en symlinks de directorio con
`**`, así que la guardia tiene que ser del test, no del intérprete.

`FP-229` queda **ABIERTA**: (c) divide el ruido de T27 por ~31 —no ~18, como
estimaba la fila— pero no lo hace satisfacible. Falta (a) citar los payloads en
`INFRAESTRUCTURA` o (b) exentar `data/raw/**`, que es P1 de N6.

**Anti-regresión.** Ningún archivo versionado dependía de la ruta borrada: los 11
aciertos de `raw/raw` en el árbol son documentación del defecto, y el único código
que la nombra (`enumerar_universo()`) ya la excluía.

---

## 2 · P2 · CNGMD 2023 — 87 de 87

**A.8 antes de la primera petición de red.** 6 entradas `cngmd` en el manifiesto,
las 6 documentación (esquema conceptual, 4 cuestionarios, la app de descarga
masiva); **0 payloads de datos**. El único acierto de `_cngmd2023_csv.zip` estaba
dentro de una `nota`, no en un campo `archivo`.

**Fuente de las URLs.** `DescargaMasivaOD.xml`, miembro de
`DescargaMasiva_192026_194559.zip` ya en el corpus — 87 URLs, `159.08 MB`
declarados, desglose **m1 2 · m2 31 · m3 23 · m4 9 · m5 6 · m6 10 · m7 6**,
idéntico al que declara el encargo. Orden de descarga del encargo: m1, m3, m2,
m4, m5, m6, m7. La orden **no tiene URL propia**: es un archivo dentro de un ZIP,
así que `url_origen` de cada payload es la URL que el XML declara para él.

**Resultado.** 87/87 `OBTENIDO`, 163.3 MB en 305.6 s, **0 soft-404, 0 fallos de
red**, y los 87 con `sha256` idéntico en la doble descarga (A.7).

**El caso que un `testzip()` a secas habría tirado.** Dos payloads
(`m1/ayuntamientos_cngmd2023_csv.zip`, `m2/admon_archiv_gest_docum_cngmd2023_csv.zip`)
fallan `zipfile.testzip()`, y **no están corruptos**. La excepción exacta es
`BadZipFile: File name in directory 'metadatos/' and header b'metadatos\\' differ`:
el directorio central guarda el nombre con `/` y la cabecera local con `\`. Es la
entrada de **directorio**; los 64 y 60 ficheros reales descomprimen con tamaño
exacto, y el defecto se reproduce en las dos descargas — luego es empaquetado en
origen, no transporte. Control: 56 de los 85 restantes traen la misma entrada
`metadatos/` sin discrepancia, y todos los miembros de este corpus usan `\` como
separador. Cerrarlos como `NO-OBTENIDO` habría tirado dos payloads buenos;
aceptarlos por tamaño habría tapado el hecho.

**Layout.** Subcarpeta por módulo (`data/raw/cngmd2023/<mN>/`) porque **4 nombres
de tabla colisionan entre módulos** — `rec_huma` ×3, `transito_vialidad` ×2,
`rec_presup` ×2. Un layout plano habría sobrescrito 4 payloads en silencio.

**Título de módulo.** m4-m7 se citan de los cuestionarios que `MAESTRA34-A1` ya
registró (Protección civil · Justicia cívica · Agua potable y saneamiento ·
Residuos sólidos urbanos). m1-m3 **no** tienen título derivado por este acto: la
página de programa de INEGI es una SPA de 4 018 B y las hojas `M1`-`M7` del
esquema conceptual solo traen cabeceras genéricas. Se describen por sus tablas.

**Registro.** `data/manifiesto.yaml` 845 → 932 (+87, una invocación de
`tests/manifiesto.py --registra` por `--id`, A.1). Cola del registro: fila `CNGMD`
`NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)` → `OBTENIDO`, `ids_manifiesto` 7 → 94.
`OBTENIDO` en la cola 53 → 54. Vista regenerada con
`python3 tools/vista_cola_adquisicion.py` (T26).

**Anti-PR#77.** 87 zips visibles por `data/raw/cngmd2023/` (symlink al corpus
compartido) y 87 en `/home/pc0/mm-corpus/raw/cngmd2023/`; **0** fuera del corpus
en el worktree.

---

## 3 · P3 · CROSSWALK sección electoral → municipio — lo entrega la ruta (iv)

**A.8 verbatim del encargo.**
`grep -i "seccion\|crosswalk\|catalogo.*municip" data/manifiesto.yaml` → **62
líneas**, y las 62 son «secciones» de **cuestionario**, no electorales; el único
catálogo con municipio es de salud (CIE10/CIE9MC/CLUES). Confirma la
clasificación `NO-ENCONTRADO` de dirección al 1/sep. Control A.13: el comando
examinó `data/manifiesto.yaml`, 16 505 líneas, `usado_para` aparece 843 veces.

**Las cuatro rutas, con salida cruda por ruta.**

| ruta | qué se probó | resultado |
|---|---|---|
| **(i)** portal INE de cartografía/estadística | `cartografia.ife.org.mx/sige7/?inicio` — el enlace que la propia página del INE publica | **HTTP 502** |
| | `cartografia.ine.mx/` → SPA Nuxt `sige8` | 200; `GET /sige8/api/tokens` → 200, devuelve la config web de Firebase del proyecto `ine-carto-next` → datos tras Firebase + reCAPTCHA |
| | `www.ine.mx/credencial/estadisticas-lista-nominal-padron-electoral/` | 200; publica **un** fichero de datos, `PE-y-LN_Nacional-Extranjero_20-08-2026.xlsx`, nacional, sin desglose por sección |
| | | **NO.** No se intentó credencial ni formulario (`/adquiere` §3 lo prohíbe) |
| **(ii)** datos.gob.mx (CKAN) | `/busca/api/3/action/package_search?q=…` | **404** (HTML de 14 347 B) |
| | `api.datos.gob.mx/v1/` | **curl 35** `TLS connect error: unexpected eof while reading` |
| | `/dataset/?q=seccion+electoral` y `?q=marco+geografico+electoral` | 200; **0** enlaces `/dataset/<algo>` en la respuesta |
| | | **NO** |
| **(iii)** SICEE | `sicee.ine.mx/` | 200, **6 205 B**: cascarón Angular. Su CSP admite `tableau.ine.mx` y `sie.ine.mx` |
| | `sie.ine.mx/` | 200, **1 587 B**: es un **Tableau Server** (`vizportal`), visor BI, no catálogo |
| | `siceen.ine.mx/` | **403** |
| | | **NO** — y por `DS-a` es de mesa, por navegador |
| **(iv)** repositorio documental INE | `repositoriodocumental.ine.mx/open-search/?query=…` (DSpace) | 200, **2 855 resultados**; los primeros son literalmente «CATÁLOGOS DE MUNICIPIOS Y SECCIONES QUE CONFORMAN EL MARCO GEOGRÁFICO ELECTORAL» |
| | | **SÍ** |

**Lo que entrega la (iv).** Los catálogos de la DERFE se publican como **anexos**
de acuerdos del Consejo General / de la Comisión Nacional de Vigilancia, y algunos
anexos son **XLSX legibles por máquina**, no solo PDF:

- **Estado de México** (handle `123456789/128317`, acuerdo `CRFE_22032016_1aSO`):
  `CRFE_22032016_1aSO_P07_1_3.xlsx`, **6 461 filas** (1 título + 1 cabecera + 6 459
  de datos), columnas `ENTIDAD | NOMBRE_ENTIDAD | DISTRITO_LOCAL | MUNICIPIO |
  NOMBRE_MUNICIPIO | SECCION`, entidad **15 = MEXICO**. Su gemelo `_1_4.xlsx` da los
  **125 municipios**.
- **Coahuila** (handle `123456789/128291`, acuerdo `CRFE_17052016_5aSE`):
  `CRFE_17052016_5aSE_P07_2.zip` — que **no es un ZIP**: es un **7-zip** servido con
  extensión `.zip` (magic `377abcaf271c`; `zipfile.ZipFile` lo rechaza con *«File is
  not a zip file»*, se abre con `py7zr`, disponible en la caja en 1.1.3). Trae 16
  XLSX, 2 por cada uno de 8 estados. El de Coahuila,
  `5a-SE-2016-CRFE-P07_2_1_Anexo1_COAH.xlsx`, tiene **1 690 filas** (1 688 de datos),
  columnas `ENTIDAD | NOMBRE_ENTIDAD | DISTRITO_FEDERAL | MUNICIPIO |
  NOMBRE_MUNICIPIO | SECCION`, entidad **5 = COAHUILA**; su Anexo2 da **38
  municipios**.

⚠️ **El eje de distrito NO es la misma columna en las dos mitades**: Edomex trae
`DISTRITO_LOCAL` y Coahuila `DISTRITO_FEDERAL`. Cruzarlas por «distrito» sin mirar
sería un defecto silencioso.

⚠️ **VIGENCIA — la reserva que no se resuelve aquí.** Los dos catálogos son de
**2016** (insumo de la distritación 2016). No son de 2023 ni de 2024, y la
correspondencia sección→municipio cambia con cada redistritación y
reseccionamiento. El vintage más reciente que este repositorio expone para estos
catálogos es 2022 (`handle 130671` — CNV 2022-03-09 — y `handle 126959` — CNV
2022-02-11), y **ninguno de los dos cubre Coahuila ni Edomex**: el primero cubre
Aguascalientes, Durango, Hidalgo, Oaxaca, Quintana Roo y Tamaulipas; el segundo,
Guerrero, Nuevo León, Morelos, Sinaloa y Yucatán. Las fechas que DSpace muestra
(2024-12-09, 2026-08-07) son de **depósito**, no del acuerdo: la fecha real va en
el identificador del documento.

**Registro.** 5 payloads nuevos en `data/manifiesto.yaml` (932 → **937**), bajo
`data/raw/ine_marco_geografico_electoral/`, los 5 con `sha256` idéntico en la doble
descarga (A.7) y estructura verificada (`%PDF-` + `%%EOF` en los dos PDF, OOXML con
`testzip() = None` en los dos XLSX, magic 7z en el contenedor). `--verifica`:
`data_raw coincide=826`.

**Tres capas** (a mano, porque la vía de N6 no existe; validador en verde):
`relaciones.tsv` 199 → 200 · `evidencias.tsv` 200 → 201 · `utilidad-modelo.tsv`
199 → 200 · `candidatas` 141 → 142. El invariante
`len(evidencias) − len(relaciones) = len(fusiones)` se conserva en 1.
`python3 tools/curador_registro/baseline.py data/curacion-registro` → `"ok": true`,
`"errores": []`. `python3 tools/curador_registro/via_capa2.py --root .` →
**`Diffs propuestos (capa2_manifiesto): 0`** sobre 200 filas, así que el `SI` que la
fila nueva declara lo deriva la herramienta, no lo declara el ejecutor.

La fila nueva es **`CANDIDATA`, no `CONFIRMADA`**, con
`capa4_apertura_mapeo = EXISTE-NO-SATISFACE` y `reason_code =
APERTURA_NEGATIVA_EXPLICITA`. El motivo importa: el crosswalk es una **llave
instrumental** —permite agregar a municipio un dato publicado por sección, empezando
por el PREP 2024 ya en corpus (`REL-8b5abcdb9a618f64c2639477`)— y **no** una
medición de `N25`. Marcarlo `CONFIRMADA` habría dicho que satisface la necesidad, y
no la satisface.

**Qué NO se pudo relacionar y por qué.** El encargo pide relacionar también con «la
necesidad cívica». Esa necesidad **no existe**: `grep -ic 'concurrente'
data/curacion-registro/necesidad-objeto-modelo.tsv` → **0**, y crearla es P2/P3 de
`MAESTRA34-N6` — `necesidad-objeto-modelo.tsv` **no está en el perímetro de este
encargo**. Se deja nombrado, no escrito.

**Precisión sobre `R7.1`.** La ficha declara el hueco de granularidad municipal,
pero el **falsador de Hito D de `R7.1` ya corrió y está adjudicado en `A`**
(`ADR-145`, 24/ago/2026, firma de mesa D1), contra la base electoral por sección de
Calderón-Hernández et al. (`data/raw/zenodo_electoral_precinct_level_mexico_municipal.zip`).
Este crosswalk **no reabre ni mueve ese veredicto**: sirve a la pieza cívica que P4
evalúa.

---

## 4 · P4 · VEREDICTO A.4 — **EXISTE-NO-SATISFACE**. `MAESTRA34-L4` NO se redacta

**Pregunta del encargo:** *¿existe ya, para Coahuila o Edomex, elección local 2023
+ concurrente 2024 con lista nominal y votos por municipio?*

**Respuesta: no.** Dos de las tres mitades faltan enteras, y la que sí está tiene
un hueco medido.

| mitad del diseño | qué hay en corpus, medido | veredicto |
|---|---|---|
| **elección LOCAL 2023** (no concurrente) | **nada.** La única base municipal por sección del corpus (`zenodo_electoral_precinct_level_mexico_municipal.zip`, Calderón-Hernández et al.) cubre **Coahuila 1996, 1999, 2002, 2005, 2009, 2013, 2017, 2018** y **México 1996, 2000, 2003, 2006, 2009, 2012, 2015, 2018** — llega a **2018** en las dos entidades. Sus listas nominales van de **2012 a 2019**. | **FALTA ENTERA** |
| **concurrente 2024 · mitad FEDERAL** | `ine_prep2024_base_datos_20240603_2005_zip` = 3 concursos, los 3 federales (`PRES_2024.csv` 48 col / 171 417 líneas · `DIP_FED_2024.csv` 50 col / 172 413 · `SEN_2024.csv` 48 col / 172 445). Los tres traen `SECCION` **y** `LISTA_NOMINAL` por casilla, y **ninguno** trae `MUNICIPIO`. Con el crosswalk de P3 se agregan a municipio. | **CUBIERTA CON RESERVA** |
| **concurrente 2024 · mitad LOCAL** | **nada.** Ese PREP no contiene ni un concurso local. | **FALTA ENTERA** |

**La reserva, en números** (cruce por `(ID_ENTIDAD, SECCION)` del catálogo 2016 de
P3 contra las secciones distintas del PREP 2024 `PRES`; verificación de cobertura
del payload, **no** medición de ninguna regla):

| entidad | secciones en PREP 2024 | cubiertas por el catálogo 2016 | sin correspondencia | municipios alcanzables |
|---|---|---|---|---|
| 5 · COAHUILA | 1 779 | **1 640 = 92.19 %** | 139 | **38 de 38** |
| 15 · MÉXICO | 6 745 | **6 338 = 93.97 %** | 407 | **125 de 125** |

Es decir: el crosswalk de 2016 alcanza **todos** los municipios de las dos
entidades, pero deja **6-8 % de las secciones de 2024 sin asignar** — secciones
creadas o reseccionadas entre 2016 y 2024. Agregar a municipio sin resolver esas
546 secciones sesgaría los totales municipales por abajo, y el sesgo no es
uniforme entre municipios. Es una reserva cuantificada, no una estimación.

**Por qué NO se redacta `MAESTRA34-L4 · CIVICA-CONCURRENTE`.** El encargo lo
condiciona a `EXISTE-SATISFACE`, y el veredicto es `EXISTE-NO-SATISFACE`. Redactar
la spec sucesora con dos mitades ausentes sería escribir un encargo que cita datos
que no existen — exactamente lo que la convención de `forense/encargos/` prohíbe
(*«un encargo que cita un archivo inexistente está mal escrito — ocurrió tres
veces»*). Mismo criterio con el que `MAESTRA34-A1` cerró sus dos sucesores
condicionados.

**Qué mitad falta, nombrada para quien la busque.** Los **resultados de las
elecciones LOCALES** de Coahuila y Estado de México — 2023 (gubernatura, no
concurrente) y la mitad local de 2024 (concurrente) —, por sección o por
municipio, con su lista nominal. La vía designada es **SICEE** (`https://sicee.ine.mx/`),
que por `DS-a` baja mesa por navegador; al 1/sep/2026 **no está**: `find /home/pc0
/mnt/c/Users/PC0/Downloads -maxdepth 3 -iname '*sicee*'` → **0 aciertos**, y su
fila en `cola-adquisicion-registro.tsv` sigue en
`NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`. Los organismos locales (IEC en Coahuila,
IEEM en el Estado de México) son la otra vía posible y **este acto no los sondeó**:
no estaban en el encargo y habrían caído fuera del perímetro.

**Tensión de diseño que hay que resolver antes de L4** — no es un detalle de
redacción. La spec que el encargo manda usar (`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md`,
l. 502-508) pide *«resultados electorales de comicios locales concurrentes vs. no
concurrentes **del mismo año y estado**»*. La firma `DS-a` fija en cambio **local
2023 no concurrente vs 2024 concurrente**, que es una comparación **entre años**.
No son el mismo diseño y no exigen el mismo dato: el de la spec necesita variación
de concurrencia dentro de un mismo año, y el de `DS-a` compara dos años distintos y
carga con todo lo que cambia entre 2023 y 2024 (candidaturas, elección presidencial
de por medio, padrón). Se deja nombrado para mesa, sin resolverlo: adjudicarlo no
es de este acto.
