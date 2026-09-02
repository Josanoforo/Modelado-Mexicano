# ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3 — P0-bis y evaluación A.4

Encargo: `forense/encargos/2026-09-02-MAESTRA35-A1-REGISTRA-Y-EVALUA-DESCARGAS-3.md`
(archivado por A.3 en este mismo commit; SHA de redacción `792b7ef`, ejecutado
contra `origin/main = 4d7bd1e`). Enmienda de dirección **firma e1** (2/sep/2026),
propagada verbatim en el archivo del encargo.

---

## §0 · La compuerta se abrió a mitad del acto — el «+0» ya no es cierto

El encargo estaba `GATED a que mesa deposite`, con verificación por producto.
**Se verificó tres veces, con resultados distintos**, y eso es el hecho central
de esta nota:

| hora (CST) | `command find "<descargas_mx>" -type f` | `… -newermt 2026-09-02` |
|---|---|---|
| 16:33 | 160 | **0** |
| 16:54 | 160 | **0** |
| 17:17 | **190** | **30** |

A las 16:33 y 16:54 la compuerta estaba **cerrada** y el acto cerró con cero
commits, como manda el paso 2 de `.claude/commands/acto.md`. Mesa depositó
**30 archivos entre las 16:56 y las 17:10**, es decir *después* de que se
levantara el primer veredicto y *mientras* se redactaba la enmienda e1. Por eso
el `CONSUMIDO` de este acto **no** dice «+0 descargas de mesa», que era el texto
dictado en el punto 4 de la firma: decirlo sería escribir un dato falso sobre el
árbol. Se propaga la *estructura* que mesa pidió (un PR de un commit para
(2)-(3), P1-P4 al relanzamiento) y se corrige el *hecho*.

Precedente de la clase: `feedback_encargo_premisa_se_verifica_contra_el_arbol` —
la premisa de un encargo se verifica contra el árbol, y sus autoadvertencias
pueden quedar obsoletas entre la redacción y la ejecución. Aquí quedaron
obsoletas en **23 minutos**.

**A.13 del negativo original** (para que quede el rastro de que fue un negativo
real y no un comando roto): universo 160 archivos, 2 directorios; controles
positivos del mismo comando `-newermt 2026-09-01` → 38 y `-newermt 2026-08-01`
→ 128, ambos coincidentes con el barrido de `MAESTRA34-A1`; `-newerct
2026-09-02` → 0, que descarta copias con `mtime` preservado; ninguna de las 14
subcarpetas que el PDF manda crear existía (control positivo `Descargas
Manuales` → 1).

---

## §1 · P0-bis — `ieeh_hidalgo_2016_ayuntamientos_zip`, por las tres capas

### El extractor: no hizo falta instalar nada

El paso 0 de la lista v2 pedía `sudo apt-get install -y unrar p7zip-full` +
`pip install rarfile`. **Ninguno de los tres era necesario, y el primero no lo
puede ejecutar un agente.** Salidas crudas:

```
$ sudo apt-get update                       # dentro del sandbox
sudo: The "no new privileges" flag is set, which prevents sudo from running as root.

$ sudo apt-get update                       # fuera del sandbox
sudo: A terminal is required to authenticate
```

Lo que sí funciona, sin privilegios y sin instalar:

```
$ /mnt/c/Windows/System32/tar.exe -xvf ieeh_hidalgo_2016_ayuntamientos.rar
x AYUNTAMIENTOS_MUNICIPIO.xlsx
x AYUNTAMIENTOS_MUNICIPIO_DETALLE.xlsx
x AYUNTAMIENTOS_CASILLAS.xlsx
exit=0
```

Windows 10 1803+ trae `bsdtar`/`libarchive` en `System32`, y libarchive lee
RAR. **Dentro del sandbox el mismo comando falla** con
`<3>WSL (10 - ) ERROR: UtilConnectUnix:526: socket failed 1` y `exit=1`: es el
socket del interop de WSL, **no la herramienta**. Confundir esas dos cosas es lo
que dejó la fila parada dos actos seguidos.

Esto **corrige dos mediciones previas**, y ambas correcciones importan porque
las dos concluían «no se puede»:

- `MAESTRA34-L6`: «el `.rar` de 2016 no se pudo abrir en esta caja (no hay
  unrar/bsdtar accesible en el sandbox)» — cierto *dentro* del sandbox, falso
  fuera.
- `MAESTRA35-L3`: «rarfile y patoolib no instalados» — **`rarfile` 4.5 sí
  importa** (y `py7zr` también). Lo que faltaba era el **binario de respaldo**:
  con los 7 extractores nativos ausentes, `rarfile` falla con
  `RarCannotExec: Cannot find working tool`. El diagnóstico apuntaba al módulo
  cuando el hueco era el binario — y el binario estaba del lado de Windows todo
  el tiempo.

### Integridad del re-empaquetado

Los tres XLSX salieron con tamaños **idénticos** a los que `rarfile.infolist()`
declaró *antes* de extraer nada (control cruzado independiente del extractor), y
`zipfile.testzip()` da limpio en los tres:

| archivo interno | rarfile declaró | extraído | `testzip` | mtime original |
|---|---|---|---|---|
| `AYUNTAMIENTOS_MUNICIPIO.xlsx` | 50 607 | 50 607 | sin error | 2017-10-31 14:28 |
| `AYUNTAMIENTOS_MUNICIPIO_DETALLE.xlsx` | 40 853 | 40 853 | sin error | 2019-07-10 16:30 |
| `AYUNTAMIENTOS_CASILLAS.xlsx` | 436 321 | 436 321 | sin error | 2017-10-31 10:02 |

### A.7 · los dos hashes

Un re-empaquetado cambia el crudo, así que el crudo **no** es identidad de
contenido. Se registran los dos, como pidió la firma e1:

- **crudo del ZIP** (derivado por `tests/manifiesto.py`, no tecleado):
  `1de5e344fb87fbe68dfcfa426b2c6a2b8cb3d75535ac30f1088e9010089e80b2`, 447 674 B.
- **hash del SET de los tres XLSX internos** (identidad estable, independiente
  del empaquetado): `16bf5826d7717e195fa58923a42640c6074dd6f9c8bad77ea25272bc122e126d`.
  Receta reproducible: `sha256( concat de "<nombre>:<sha256>\n" , nombres
  ordenados asc )`, sobre
  `AYUNTAMIENTOS_CASILLAS.xlsx:b2c6d934…`,
  `AYUNTAMIENTOS_MUNICIPIO.xlsx:98e420b6…`,
  `AYUNTAMIENTOS_MUNICIPIO_DETALLE.xlsx:7945f79f…`.

### Las tres capas

**(i) payload + manifiesto.** Bytes en el **corpus compartido**
(`/home/pc0/mm-corpus/raw/electoral_local_municipal_serie/`), no solo en el
worktree — cierre anti-PR#77. Una invocación de `--registra` para el único id.
Entradas del manifiesto: 1039 → **1040**.

Cierre anti-PR#77, una invocación por id, salida cruda sin colapsar:

```
ieeh_hidalgo_2016_ayuntamientos_zip [data_raw]: COINCIDE -- sha256 y tamaño (447674 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0

ieeh_hidalgo_2016_ayuntamientos_rar [data_raw]: COINCIDE -- sha256 y tamaño (444642 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

**(ii) cola del registro.** Fila `IEEH_HIDALGO_SERIE_MUNICIPAL` de
`data/curacion-registro/cola-adquisicion-registro.tsv`: enmienda **fechada**
añadida al final de `nota` (la nota anterior no se edita), `ids_manifiesto`
+1 (3 → 4). `estado_A4A5` **sin cambio**: sigue `OBTENIDO-SIN-DENOMINADOR`, por
lo que dice §2. Editada por línea, nunca con el módulo `csv`. Vista
`data/cola-adquisicion-v1_0.tsv` regenerada con
`python3 tools/vista_cola_adquisicion.py` (95 filas) — T26 en verde.

**(iii) relación.** Sin cambio, como declaró la firma. `via_capa2.py --root .`
corrido **en lectura**, sin `--escribe`.

---

## §2 · Evaluación A.4 de lo extraído (punto 3 de la firma e1)

**Veredicto: `EXISTE-NO-SATISFACE`.** El payload existe, es válido y queda
registrado; **no** trae el denominador.

**A.13 — hojas examinadas: 86 (1 + 1 + 84), 0 aciertos de `NOMINAL`.**

> **Corrección de una cifra propia.** La firma e1 pidió la A.13 sobre
> «2+2+168». Ese `168` salió de un conteo mío descuidado en el reporte previo:
> contaba entradas del `namelist()` del XLSX que casan `sheet`, lo que incluye
> los `xl/worksheets/_rels/…` además de los `xl/worksheets/sheetN.xml`. El
> número real de hojas, leído de `xl/workbook.xml`, es **84** en
> `AYUNTAMIENTOS_CASILLAS.xlsx` y **1** en cada uno de los otros dos. Total
> **86**, no 172.

Búsqueda en `sharedStrings.xml` **y** inline en las 86 hojas, insensible a
mayúsculas: **0**. Controles positivos con el mismo método sobre el mismo
archivo: `CASILLA` → 3, `MUNICIPIO` → 1 — el método sí encuentra cuando hay.

Encabezado de la primera hoja de `AYUNTAMIENTOS_CASILLAS.xlsx` (hoja
`'Acatlán_A'`, la primera de las 84):

```
Municipio | Sección | Casilla | Partido Acción Nacional | Partido Revolucionario Institucional |
Partido de la Revolución Democrática | Partido del Trabajo | Partido Verde Ecologista de México |
Partido Movimiento Ciudadano | Partido Nueva Alianza | Partido Morena | Partido Encuentro Social |
PRI-VERDE-NUEVA ALIANZA | PRI-VERDE | …
```

Son votos por partido y casilla. **No hay columna de lista nominal.** Hidalgo
2016 sigue `OBTENIDO-SIN-DENOMINADOR` por esta vía, y el denominador seguía
siendo SICEE — hasta §3.

---

## §3 · P1 · Inventario de lo que mesa depositó (lectura, sin registrar)

30 archivos, 558.7 MB, depositados 16:56–17:10 en la **raíz** de `descargas_mx`
(no en las subcarpetas que el PDF indicaba — se identifican por nombre y por
contenido, como manda P1, no por carpeta). Tipo real por byte 0: **28 ZIP + 2
PDF, ningún HTML** — no hay soft-404 en el lote. `zipfile.testzip()` **limpio en
los 28**.

| grupo | archivos | corresponde a |
|---|---|---|
| `AGS_PEL_{2016,2018,2019,2021,2024}` | 5 | v2 A2 · `IEE_AGUASCALIENTES_SERIE_MUNICIPAL` |
| `HGO_PEL_{2016,2018,2020,2021}` | 4 | v2 A1 · `IEEH_HIDALGO_SERIE_MUNICIPAL` |
| `VER_PEL_{2016,2017,2018,2021}` | 4 | v2 A3 · Veracruz (**sin fila propia** → alta de fuente nueva) |
| `DIPUTACIONES_FED_{MR,RP}_{2018,2021,2024}` | 6 | v2 A4 · federales por casilla |
| `SENADURIAS_{MR,RP}_{2018,2024}` + `MR_NAY_EXT_2021` + `MR_TAMPS_EXT_2023` | 6 | v2 A4 · federales |
| `PRESIDENCIA_{2018,2024}` | 2 | v2 A4 · federales |
| `ICPSR_35024-V1.zip` | 1 | `MEXICO_PANEL_STUDY_2012` |
| `ssrn-2589578.pdf`, `ssrn-2689238.pdf` | 2 | `PRICE_AND_INFORMATION_TYPE…` (ver abajo) |

### Tres hallazgos de contenido, verificados

**(a) El denominador aparece — y esto destraba el diseño.** Los paquetes `*_PEL_*`
son las bases SEE del INE. `HGO_PEL_2016/AYUNTAMIENTOS_csv/2016_SEE_AYUN_HGO_MUN.csv`
trae, en 63 columnas: `col 61 = LISTA_NOMINAL` y `col 62 = PARTICIPACION` (ya
calculada), en **84 filas de datos = los 84 municipios de Hidalgo**. La primera
fila es `13,HIDALGO,1,ACATLÁN,…,9675,280,9959,16086,0.6191`. El nivel casilla
(`…_CAS.csv`, 69 columnas) también trae `LISTA_NOMINAL` (col 64).

Es exactamente lo que `MAESTRA35-L3` declaró inalcanzable tras **cinco** rutas
probadas por programa. **No lo mido aquí** (este acto no mide, y P3 está fuera
de lo que la firma e1 autorizó), pero cambia la evaluación de las dos filas:
Hidalgo y Aguascalientes dejan de estar sin denominador en cuanto se registren.

**(b) `ICPSR_35024-V1.zip` es documentación otra vez, NO microdato.** Las 10
entradas son 6 PDF (cuestionarios y codebooks ES/EN de DS0001–DS0004), 2 `.txt`
(manifest, related_literature) y 2 `.html` (cita, términos de uso).
Extensiones: `{'.pdf': 6, '.txt': 2, '.html': 2}` — **cero** `.dta`, `.sav`,
`.por` o `.tsv` de datos. `MEXICO_PANEL_STUDY_2012` sigue **PARCIAL**, igual que
lo dejó `MAESTRA34-A1`: la receta hay que corregirla para seleccionar los
archivos de **datos** de cada `DS000n` (Stata o Delimited) en el carrito de
ICPSR, no el paquete de documentación.

**(c) Los dos PDF de SSRN son de Bauchet, pero NO son el paper pedido.** La fila
pide *«Price and Information Type in Life Microinsurance Demand»*
(`abstract_id=2474620`). Llegaron `ssrn-2589578` = *«Modalities matter:
Microinsurance take-up under different payment schemes»* y `ssrn-2689238` =
*«Asymmetric information in microinsurance markets: Experimental evidence from
Mexico»*. Mismo autor, mismo tema, misma familia experimental — **otro papel**.
`EXISTE-NO-SATISFACE` para la fila tal como está redactada; si a la dirección le
sirve la familia y no el título exacto, es una decisión de mesa, no del ejecutor.

---

## §4 · Qué sigue pendiente

- **P2/P3 sobre los 30 payloads**: registro por las tres capas y evaluación A.4
  fila por fila. Fuera de lo que la firma e1 autorizó para este PR; es el
  relanzamiento que mesa ya declaró («cuando yo deposite lo de SICEE, se
  relanza con la compuerta abierta»). La compuerta **ya está abierta**.
- **Veracruz** (`VER_PEL_*`, 4 payloads) **no tiene fila propia** en la cola →
  exige alta de fuente nueva en `aliases-fuentes.tsv` + fila en la cola, con la
  receta del PDF v2 como origen.
- **ICPSR**: receta corregida (seleccionar datos, no documentación).
- **Bauchet**: decidir si la familia sustituye al título exacto.
- **`descargas pendientes v3`** no se escribe aquí: se deriva del registro, y el
  registro de los 30 es justo lo que queda pendiente. La v2 (1/sep) sigue
  vigente: 6 cumplidas · 2 parciales · 3 no ejecutadas · 4 que nunca fueron
  descargas.

## CONTADOR

- payloads registrados con sha: **+1** (`ieeh_hidalgo_2016_ayuntamientos_zip`,
  crudo `1de5e344…`, set `16bf5826…`, `--verifica` COINCIDE)
- filas de la cola que cambian de estado: **+0** (la de Hidalgo se enmienda y
  suma un id, pero el estado sigue `OBTENIDO-SIN-DENOMINADOR` por §2)
- descargas de mesa: **+30 archivos, 558.7 MB**, inventariados y verificados,
  **0 registrados** (P2 al relanzamiento)
- descargas pendientes: **v2 → v3 no emitida** (depende del registro de los 30)
