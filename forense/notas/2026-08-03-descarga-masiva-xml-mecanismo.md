# Descarga masiva CPV 2020 (XML) + ENADID 2023: mecanismo, y una identificación de payload corregida

Sesión Sonnet, Ubuntu, rama `sesion/descarga-dirigida`. Encargo: bajar y registrar 9 archivos
(7 CPV, 2 ENADID) más el propio XML de descarga masiva, y documentar el mecanismo que los
desbloqueó. No se abrió ningún microdato más allá de lo necesario para HEAD (Content-Type/tamaño)
y `unzip -l`/pestañas de descriptor para identificar el payload (ADR-46: identificar estructura,
no leer reactivo).

## CORRECCIÓN, primero: CAAS y CEU no son lo que esta sesión registró al principio

El registro inicial de `cpv2020_caas_eum_csv` y `cpv2020_ceu_eum_csv` los describía como la
muestra de personas/viviendas del Cuestionario Ampliado — **incorrecto**, heredado sin verificar
de la anotación con la que arrancó el encargo. Verificado después de que el autor señalara que
1.08 MB era un tamaño imposible para una tabla nacional de personas:

- **CAAS = Censo de Alojamientos de Asistencia Social**, no una muestra de personas en vivienda.
  `unzip -l` (vía `zipfile`, sin abrir filas) da tres tablas: `TI_TRA_CAAS_00.csv` (trabajadores),
  `TI_USU_CAAS_00.csv` (usuarios), `TR_ALO_CAAS_00.csv` (alojamientos) — confirmado además por las
  pestañas del descriptor `cpv2020_caas_descriptor_bd_xlsx`: `CAAS_Alojamientos` / `CAAS_Usuarios`
  / `CAAS_Trabajadores`. Es el censo de instituciones de asistencia social (albergues, asilos,
  orfanatos) — coherente con que la muestra de vivienda del Cuestionario Ampliado excluye
  justamente esa población (§4).
- **CEU = cartografía urbana**, no una muestra de viviendas. `unzip -l` da `TR_VIALIDAD_EU.csv`
  (vialidades) y `TI_MANZANA_EU.csv` (manzanas) — confirmado por las pestañas de su descriptor
  (`cpv2020_ceu_descriptor_bd_xlsx`): `TR_VIALIDAD_EU` / `TI_MANZANA_EU`.
- **La muestra real del Cuestionario Ampliado (VIVIENDAS / PERSONAS / MIGRANTES)** sí se identificó
  — son las pestañas de `cpv2020_diccionario_cuestionario_ampliado_xlsx`, que sí se bajó esta
  sesión — pero **sus archivos de datos NO están entre las 576 URLs del XML de descarga masiva**.
  Ninguna de las 5 familias del XML (`caas`/`cl`/`ceu`/`iter`/`ageb_manzana`) corresponde a esas
  tres tablas. **El bloqueo de proyecto/anio de `2026-07-31-cola-descarga-rederivada.md` §4 sigue
  sin resolverse para ese producto específico** — lo que sí se resolvió fue el acceso a otros 5
  productos del mismo portal, que no son el que el encargo original asumía.

Las tres entradas del manifiesto (`cpv2020_caas_eum_csv`, `cpv2020_ceu_eum_csv`,
`cpv2020_diccionario_cuestionario_ampliado_xlsx`) quedaron corregidas en el mismo commit que esta
nota, con la cadena `CORREGIDO 2026-08-03` al inicio de su `usado_para`. No se tocó `sha256` ni
`tamano_bytes` de ninguna — el archivo en disco siempre fue el correcto, solo la descripción de
qué es estaba mal.

**`CL` (la tercera familia, 99 URLs, no bajada) queda sin identificar** — mismo patrón de nombre
de tres letras que CAAS/CEU, así que no se asume qué es sin verificar su descriptor
(`Censo2020_CL_descriptor_bd.xlsx`, en el XML pero no bajado esta sesión). Cola para quien la
necesite.

## 0 · Qué bloqueo resuelve esto (y qué no)

`forense/notas/2026-07-31-cola-descarga-rederivada.md` §4 dejó declarado el bloqueo: el endpoint
AJAX de microdatos de CPV/ENADID (`.../descargamasiva/lista/archivoscompaginacion`) exige
`proyecto`/`anio` que no aparecen como atributo `data-*` en `pestanadata.js` de esos dos portales.
Esta sesión no resolvió ese endpoint — lo **rodeó** para 5 productos concretos del portal de CPV
(caas/cl/ceu/iter/ageb_manzana): el botón "Descarga masiva" entrega un XML con las URLs ya
resueltas, sin pasar por ese endpoint. **No rodeó el bloqueo para la muestra real del Cuestionario
Ampliado** (ver corrección arriba) — ese producto específico sigue bloqueado.

## 1 · Mecanismo A — XML de "Descarga masiva" (botón del portal)

El usuario descargó `DescargaMasiva_382026_131650.zip` desde el botón "Descarga masiva" de
`/programas/ccpv/2020/` en el navegador. Contiene tres archivos (`leeme.txt` es explícito):
- `DescargaMasivaApp.exe` — instalador genérico de escritorio de INEGI (el mismo que
  `forense/notas/2026-07-31-enut-descarga.md` Parte 2 ya documentó para otro programa: no trae
  payload de encuesta, solo orquesta la descarga real).
- `DescargaMasivaOD.xml` — **lo que importa**: `<Archivo>` por cada URL real,
  verificado en esta sesión con **576 URLs exactas** (570 bajo `microdatos/` + 6 bajo `doc/`),
  agrupadas en 5 familias: `caas` (99) · `cl` (99) · `ceu` (97) · `iter` (65) · `ageb_manzana`
  (64). El elemento raíz trae `<Descarga totalMb="8.23 GB" aut="57de16c5-…" />` — `aut` es un
  token de sesión/solicitud, no un parámetro a derivar ni reutilizar.

**Confirmado también para ENADID 2023**, corrigiendo §2 de la versión anterior de esta nota: existe
`DescargaMasiva_382026_13276.zip` (mismo directorio de Descargas, zip distinto), con
`DescargaMasivaOD.xml` propio: `<Descarga totalMb="138.55 MB" aut="09db0481-…" />`, 4 `<Archivo>`
— `base_datos_enadid23_csv.zip`, `base_datos_enadid23_dbf.zip`, `base_datos_enadid23_sav.zip`,
`fd_enadid23.xlsx`. Los 2 URLs de ENADID que esta sesión bajó (csv y xlsx) se localizaron
directos en el HTML del portal, sin pasar por este XML — pero el mecanismo A **sí existe** para
ENADID; simplemente no hizo falta usarlo para esos 2 archivos. `base_datos_enadid23_dbf.zip`
(23 475 875 bytes por HEAD) y `base_datos_enadid23_sav.zip` (71 962 794 bytes por HEAD) están
identificados y verificados por HEAD pero **no bajados ni registrados** — no estaban en la lista
de 9 del encargo; quedan como cola declarada, formatos alternos del mismo dato ya registrado en
CSV.

**Receta para reusar esto en otra fuente:**
1. En el navegador, abrir `/programas/{prog}/{año}/` y pulsar "Descarga masiva" (pestaña
   Microdatos). Requiere navegador — no se encontró forma de invocarlo por curl.
2. Descomprimir el `.zip`, extraer solo `DescargaMasivaOD.xml` (el `.exe` no se ejecuta ni se
   registra como payload).
3. `grep -oP '(?<=<Archivo>).*?(?=</Archivo>)'` sobre el XML da la lista plana de URLs reales.
4. **Antes de asumir que una URL es el producto que crees que es, revisa el nombre de familia
   contra su descriptor** (`unzip -l` + pestañas del `*_descriptor_bd.xlsx` si existe) — la
   corrección de arriba es la evidencia de que el nombre de tres/cuatro letras del portal
   (`CAAS`, `CEU`, `CL`) no es autoexplicativo y no coincide necesariamente con la premisa con la
   que se llegó a esa URL.
5. `curl -sI` cada URL antes de bajar (Content-Type, Content-Length) — no asumir que todas
   resuelven.
6. `curl` real, `tests/manifiesto.py --registra`, luego `--verifica`.
7. **Control de integridad agregado, `totalMb` del XML** (ver §8) — para una descarga completa
   de una familia o de todo el XML, sumar los `Content-Length` reales contra `totalMb` declarado
   detecta truncación grosera; no reemplaza el `--verifica` por archivo.

**No verificado esta sesión:** si el botón "Descarga masiva" existe en las páginas de las 27
fuentes SIN PAYLOAD de `cola-descarga-rederivada.md` §2 (ENASEM, ENDIREH, ENSU, ENCUP, etc.). Se
confirmó para CPV y ENADID. Razonable esperar que exista en otros programas del mismo portal, pero
es expectativa, no verificación.

## 2 · Dos rutas de acceso, no dos mecanismos exclusivos

La premisa con la que arrancó este encargo ("ENADID y cualquier otra fuente del portal usan el
mismo [mecanismo que CPV]") **queda corregida en sentido distinto al que la primera versión de
esta nota decía**: no son "dos mecanismos, uno por programa" — ambos programas exponen **el mismo
mecanismo A** (XML de descarga masiva vía botón), y además ENADID expone sus URLs directas en el
HTML crudo (mecanismo B), redundante con el XML. No se verificó si CPV también expone sus URLs
directas en HTML sin pasar por el XML — no hacía falta, ya se tenía el XML. La consecuencia
práctica para reuso: probar primero el HTML crudo de la página de microdatos (más barato, sin
navegador) y recurrir al botón+ZIP+XML si no aparece ahí — pero no asumir que la ausencia del
botón en un intento anterior significa que el mecanismo A no existe para ese portal.

## 3 · Cola declarada, no abierta hoy: los 5 `DescargaMasiva_*.zip` ya en manifiesto

`data/manifiesto.yaml` ya registra 5 entradas `descargamasiva_3072026_*` (`raiz: descargas_mx`,
`usado_para: sin uso asignado`), bajadas por el usuario el 30/jul vía navegador — instancias de
este mismo mecanismo A para el programa que el usuario navegaba ese día, sin identificar. Por el
§2 de `cola-descarga-rederivada.md`, se sabe que solo contienen el instalador genérico — pero eso
se concluyó **sin abrir el XML interno de cada uno**. **Se anota como cola, no se abre esta sesión**
(instrucción explícita del encargo): la próxima sesión debería extraer `DescargaMasivaOD.xml` de
esos 5 zips y correr la receta de §1 — y, dado el hallazgo de esta sesión, **verificar el nombre de
familia contra su descriptor antes de asumir qué producto es**, no solo contra el nombre del portal
que se navegaba ese día.

## 4 · Universo declarado por el portal — aplica al Cuestionario Ampliado real, no a CAAS/CEU

La declaración original de este encargo ("la muestra cubre solo viviendas particulares habitadas:
excluye colectivas, Servicio Exterior y población sin vivienda") es del producto **Cuestionario
Ampliado real** (VIVIENDAS/PERSONAS/MIGRANTES) — el que sigue sin bajarse (corrección arriba), no
de CAAS/CEU. No se verificó si esa misma exclusión aplica a CAAS (de hecho, dado que CAAS censa
instituciones de asistencia social, es razonable que exista precisamente para cubrir la población
que el Cuestionario Ampliado excluye — pero eso es una lectura razonada, no algo confirmado contra
el descriptor de CAAS esta sesión). Cualquier uso downstream de VIVIENDAS/PERSONAS/MIGRANTES
cuando se bajen debe declarar esta exclusión.

## 5 · Descarga y registro

| id | Archivo | Qué es en realidad | Bytes | `--verifica` |
|---|---|---|---|---|
| `cpv2020_caas_eum_csv` | `Censo2020_CAAS_eum_csv.zip` | Censo de Alojamientos de Asistencia Social, nacional (NO muestra de personas — corregido) | 1 076 224 | COINCIDE |
| `cpv2020_ceu_eum_csv` | `Censo2020_CEU_eum_csv.zip` | Cartografía urbana, vialidad+manzana, nacional (NO muestra de viviendas — corregido) | 135 163 712 | COINCIDE (re-registrado, ver §6) |
| `cpv2020_iter_nal_csv` | `ITER_NAL_2020_csv.zip` | Iter nacional (agregados por localidad) | 36 604 573 | COINCIDE |
| `cpv2020_diccionario_cuestionario_ampliado_xlsx` | `diccionario_cuestionario_ampliado_cpv2020.xlsx` | Diccionario VIVIENDAS/PERSONAS/MIGRANTES — de un producto aún sin bajar (corregido) | 95 642 | COINCIDE |
| `cpv2020_caas_descriptor_bd_xlsx` | `Censo2020_CAAS_descriptor_bd.xlsx` | Descriptor de BD, CAAS | 77 167 | COINCIDE |
| `cpv2020_ceu_descriptor_bd_xlsx` | `Censo2020_CEU_descriptor_bd.xlsx` | Descriptor de BD, CEU | 52 106 | COINCIDE |
| `cpv2020_fd_iter_pdf` | `fd_iter_cpv2020.pdf` | Ficha descriptiva, Iter | 921 352 | COINCIDE |
| `enadid2023_base_datos_csv` | `base_datos_enadid23_csv.zip` | ENADID 2023, base completa CSV | 44 922 433 | COINCIDE |
| `enadid2023_fd_xlsx` | `fd_enadid23.xlsx` | Ficha descriptiva ENADID 2023 | 2 085 302 | COINCIDE |
| `descargamasiva_382026_131650_xml` | `DescargaMasivaOD_382026_131650.xml` | El XML mismo, mecanismo | 69 763 | COINCIDE |

## 6 · Anomalía: hash inestable en la primera descarga de `cpv2020_ceu_eum_csv`

El primer `curl` de `Censo2020_CEU_eum_csv.zip` completó con `HTTP 200`, tamaño exacto
(135 163 712 bytes, igual al HEAD previo) y `--registra` computó `sha256=0f3a1baa…`. Corriendo
`--verifica` minutos después sobre el mismo path, el sha256 recomputado dio `49f2dd95…` — mismo
tamaño, hash distinto. Dos re-descargas frescas del mismo URL, inmediatas, dieron `49f2dd95…` de
forma estable y reproducible. Ningún proceso propio de esta sesión tocó el archivo entre el
registro y la verificación (`ps aux` sin curl/python concurrentes).

**No se puede concluir con certeza la causa:** (a) el servidor de INEGI sirvió contenido distinto
para la misma URL en dos momentos del mismo día, tamaño coincidente por construcción; o (b) otra
sesión, en otro worktree que comparte el mismo `data/raw` externo (`/home/pc0/mm-corpus/raw`,
symlink común a los tres worktrees vivos), sobrescribió el archivo entre `--registra` y
`--verifica`. `ps aux` no descarta (b): `forense/hallazgos.md` (31/jul) ya registró que ese
namespace de PID no ve procesos de otro worktree. (b) tiene precedente directo en este repositorio
(dos incidentes de sesiones concurrentes sobre `data/raw` compartido, mismo archivo), así que es
la hipótesis más verosímil, no la única posible.

**Corregido:** se retiró la entrada con el hash `0f3a1baa…` (nunca comiteada) y se re-registró
contra el contenido estable verificado dos veces (`49f2dd95…`). Registrado también en
`forense/hallazgos.md`.

## 7 · Nota de ruta: "Descargas" vs "Downloads"

El encargo nombró la ruta como `/mnt/c/Users/PC0/Descargas/...`; la carpeta real de Windows para
este usuario se llama `Downloads` (inglés) — el zip estaba en
`/mnt/c/Users/PC0/Downloads/DescargaMasiva_382026_131650.zip`. `downloads` ya está declarada en
`data/raices.local.yaml`, distinta de `descargas_mx` (`/mnt/c/Users/PC0/Descargas MX`, la carpeta
de los 5 zips de §3). Ningún cambio de configuración hizo falta.

## 8 · `totalMb` del XML como control de integridad agregado

El elemento `<Descarga totalMb="…" />` de cada `DescargaMasivaOD.xml` declara el tamaño total del
lote que describe — 8.23 GB para las 576 URLs de CPV, 138.55 MB para las 4 de ENADID. Verificado
esta sesión, dos formas:

- **Por archivo, contra `Content-Length` de `curl -sI`:** `Censo2020_CAAS_eum_csv.zip` —
  HEAD da `Content-Length: 1076224`, idéntico al tamaño en disco y al registrado
  (1 076 224 bytes exactos, sin truncar). Esta es la verificación que sostiene la corrección de
  arriba: el archivo no está corrupto ni truncado, solo estaba mal identificado.
- **Agregado, sumando los 4 `Content-Length` de ENADID contra `totalMb="138.55 MB"`:**
  44 922 433 + 23 475 875 + 71 962 794 + 2 085 302 = **142 446 404 bytes** = 142.45 MB (decimal,
  ÷1e6) o 135.84 MiB (binario, ÷1 048 576). Ninguna de las dos conversiones da 138.55 exacto —
  la más cercana (binaria) queda ~2% por debajo, la decimal ~2.8% por encima. **No es un error**:
  `data/manifiesto.yaml:44` ya documenta un caso previo de INEGI anunciando un tamaño de página
  que no coincide con el byte exacto (36.5 MB anunciados vs. 38 309 647 bytes reales) — el mismo
  patrón de imprecisión del lado del portal, no del lado de la descarga.

**Conclusión para reuso:** `totalMb` sirve como **control grosero** — detecta truncación de orden
de magnitud (una descarga que diera 13 MB en vez de 138 sería sospechosa; una que da 142 vs. 138.55
no lo es). No sirve como checksum exacto: no reemplaza `sha256`/`--verifica` por archivo, que es lo
que de hecho detectó la anomalía de §6 (una discrepancia de hash con tamaño idéntico, que un chequeo
de `totalMb` agregado nunca habría visto).

## 9 · Por qué no hay `verificacion_tamano` en las entradas de esta sesión

`verificacion_tamano` no es un campo del esquema que `tests/manifiesto.py` lea o escriba —
`--registra`/`--verifica` no lo tocan (verificado por `grep` sobre el script: cero referencias).
Aparece exactamente una vez en todo `data/manifiesto.yaml` (línea 44), como texto narrativo que un
humano añadió a mano para declarar el mismo patrón de imprecisión de §8 en un caso anterior — no es
un campo obligatorio ni derivado automáticamente. Las 10 entradas de esta sesión no lo traen porque
la verificación de tamaño que sí corre — `--verifica`, sha256 + `tamano_bytes` contra el archivo
real — ya cubre esa función y dio COINCIDE en las 10 (§5). Si se quiere que `verificacion_tamano`
sea un campo estándar en vez de una anotación ad hoc, es una decisión de esquema para otra sesión,
no algo que este encargo pidiera.

## Prohibiciones respetadas

`canon/` no se tocó. No se abrió microdato: los archivos de datos no se leyeron más allá de HEAD
(Content-Type/tamaño) y `unzip -l` (nombres y tamaños de entrada, no contenido de fila) — la
identificación de CAAS/CEU se hizo así, no leyendo filas. Las pestañas de los `*_descriptor_bd.xlsx`
y del diccionario del Cuestionario Ampliado se leyeron por nombre de hoja (estructura, no reactivo)
— mismo criterio que sesiones anteriores usaron para nombrar correctamente instrumentos sin leer
preguntas de fondo. El XML se leyó completo porque es el mecanismo mismo, no un payload de encuesta.
Los 5 `DescargaMasiva_*.zip` de §3 no se abrieron, por instrucción explícita del encargo. Ninguna
cifra de este documento se tecleó a mano: las 576/4 URLs, la partición por familia, los tamaños en
bytes y las sumas de `totalMb` salen de `grep`/`curl -sI`/`zipfile`/`tests/manifiesto.py --verifica`
corridos en esta sesión.
