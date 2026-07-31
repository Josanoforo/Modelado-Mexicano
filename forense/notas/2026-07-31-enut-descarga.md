# ENUT: bajada de las cinco ediciones · identificación de los cinco DescargaMasiva_*

Sesión ENCARGO E-H, rama `sesion/enut`, base `origin/main` = `d9f2954` (PR #24 dentro,
posterior a `134739b`).

## Parte 1 · ENUT

### Verificación de la premisa Tipo (3)

La nota de PR #24 declaraba, sin verificar: "el portal de ENUT expone las cinco ediciones
(2002, 2009, 2014, 2019, 2024), cada una con base, descriptor de archivos y diagrama
entidad-relación, desde la pestaña Microdatos". Se comprobó contra el portal.
**Resultado: coincide parcialmente.** El componente `descargaMasivaV2` que sirve la pestaña
Microdatos (`data-tipoinformacion=4`) publica, por edición:

| Edición | idBiinegi | Base de datos | Descriptor de archivos | Diagrama E-R | Diccionario de variables (vía RNM) |
|---|---|---|---|---|---|
| 2002 | 1721 | sí (DBF, .zip) | sí (PDF) | **no** | **no** (sin catálogo RNM enlazado) |
| 2009 | 1143 | sí (DBF, .zip) | sí (PDF) | **no** | sí (catálogo RNM 12) |
| 2014 | 1720 | sí (DBF, .zip) | sí (XLS) | **no** | sí (catálogo RNM 276) |
| 2019 | 2968 | sí (CSV, .zip) | sí (XLSX) | sí (.zip) | sí (catálogo RNM 618) |
| 2024 | 3381 | sí (CSV, .zip) | sí (XLSX) | sí (.zip) | sí (catálogo RNM 1127) |

El diagrama entidad-relación como archivo descargable en la pestaña Microdatos **solo existe
para 2019 y 2024**; 2002/2009/2014 no lo publican ahí (ni en ningún otro lugar detectado). El
"diccionario de variables" no aparece nunca en la pestaña Microdatos: vive en la Red Nacional
de Metadatos (RNM, catálogo tipo NADA/IHSN), enlazada desde la pestaña Documentación
(`arbolData.js` → "Metadatos (estándar DDI)"). 2002 no tiene entrada en RNM -- es la única
edición sin diccionario de variables localizado. **Esto es el hallazgo**: la premisa de
PR #24 describe correctamente 2019 y 2024, pero no las tres ediciones anteriores.

### Mecanismo de descubrimiento (sin navegador)

El precedente de la sesión anterior (`arbolData.js` + `archivoscompaginacion?...&tipodocto=4`,
ver `forense/hallazgos.md` líneas 33/35) **no sirvió tal cual** contra ENUT: con esos parámetros
el endpoint devolvía `204 No Content` para las cinco ediciones. Se determinó por qué: el
parámetro correcto no es `tipodocto` sino `tipoinformacion`, y el endpoint requiere además
`tema`, `subtema`, `areaGeografica`, `proyecto`, `anio` y `agrupacion` (base64 de "Todas"),
ninguno de los cuales aparece en la nota previa. Estos se recuperaron leyendo el JS fuente del
componente (`/componentes/descargaMasiva/js/descargaMasivaV2.min.js`) y el archivo de
configuración de pestañas específico de cada página
(`/programas/enut/{año}/data/pestana/pestanadata.js`, que expone `data-id` = idBiinegi y
`data-tipoinformacion` = 4 para Microdatos). Con esos valores, `archivoscompaginacion` sí
devuelve la lista de archivos (título, formato, `pathLogico`). La URL de descarga real se
construye como `https://www.inegi.org.mx/contenidos` + `pathLogico` + extensión (tomada de
`formato`, lógica de `generarTdsEnlaces_DescargarArchivos2` / `urlNas="/contenidos"` en el
mismo JS) -- **no se adivinó**: cada URL construida así se verificó con HEAD (Content-Length
byte-exacto) antes de bajarla.

Precedente corregido para la próxima sesión que toque un portal con este mismo componente:
el parámetro es `tipoinformacion`, no `tipodocto`, y sin `data-pestana/pestanadata.js` de la
página específica no hay forma de derivar `tema/subtema/proyecto/anio` sin ejecutar JS.

Aviso propio del portal, registrado en la nota de `enut2019_bd_csv`: "El 28 de agosto de 2025,
se reemplazaron los microdatos de la ENUT 2019, debido a que se actualizaron las estimaciones
de población" -- el archivo bajado es esa versión reemplazada, no la original de 2019.

### Conteo de archivos bajados por edición

- 2002: 2 archivos (base DBF + descriptor PDF)
- 2009: 3 archivos (base DBF + descriptor PDF + diccionario de variables HTML, RNM 12)
- 2014: 3 archivos (base DBF + descriptor XLS + diccionario de variables HTML, RNM 276)
- 2019: 4 archivos (base CSV + descriptor XLSX + DER zip + diccionario de variables HTML, RNM 618)
- 2024: 4 archivos (base CSV + descriptor XLSX + DER zip + diccionario de variables HTML, RNM 1127)
- **Total: 16 archivos**, 16 entradas nuevas en `data/manifiesto.yaml`, todas `raiz: data_raw`,
  `usado_para: "documentación / microdato — ENUT, constructo pendiente de asignar en el cruce
  de Hito E"`.

Lo que el portal publica y esta sesión NO bajó: los tabulados precalculados (pestaña
"Tabulados", `tipoinformacion=5`) y, para 2019/2024, "Datos abiertos" (`tipoinformacion=12`)
-- son presentaciones derivadas de la misma base de microdatos, fuera de lo pedido (base +
descriptor + diccionario + DER). Tampoco se bajaron los documentos de la pestaña
Documentación (nota técnica, diseño conceptual, diseño muestral, manuales, cuestionario,
informe operativo) -- son metodología de la encuesta, no del cruce de microdatos; quedan
listados en `arbolData.js` de cada edición si una sesión futura los necesita. Ningún payload
de microdato (los `.zip`/`.dbf`/`.csv` de "base de datos") fue abierto ni extraído -- solo
hasheado, por firewall vigente de esta sesión. Los descriptores (PDF/XLS/XLSX), diagramas E-R
(zip, no abiertos -- son binarios comprimidos, tratados igual que un payload) y páginas de
diccionario de variables (HTML, documentación publicada) sí fueron leídos para confirmar que
correspondían a la edición esperada.

## Parte 2 · Los cinco DescargaMasiva_3072026_*.zip

`unzip` no está instalado en este entorno; se usó el módulo `zipfile` de Python (misma
operación que `unzip -l`: lista nombres y tamaños, no extrae ni abre contenido). Resultado,
idéntico en estructura para los cinco archivos:

```
DescargaMasivaApp.exe   (850432 bytes)
leeme.txt                  (434 bytes)
DescargaMasivaOD.xml   (348–480 bytes, varía por archivo)
```

**No se identifican.** Los tres nombres internos son genéricos -- son el instalador/lanzador
de escritorio "Descarga Masiva" que INEGI distribuye desde *cualquier* pestaña Microdatos que
use el componente `descargaMasivaV2` (el mismo componente que sirvió los 16 archivos de ENUT
en la Parte 1), no un paquete específico de una encuesta. El nombre no lleva ningún token de
programa, año o idBiinegi -- a diferencia de los `pathLogico` reales (`enut_2019_bd_csv`,
`fd_enut14`, etc.), que sí lo llevan. El único lugar donde la encuesta/edición real quedaría
determinada es dentro de `DescargaMasivaOD.xml` (probablemente los mismos parámetros
`idBiinegi`/`tipoinformacion`/`anio` reconstruidos en la Parte 1) -- **fuera de perímetro**:
el encargo limita esta sesión a `unzip -l`/listar nombres, y abrir ese XML sería abrir
contenido del payload, no solo listarlo. No se hizo.

`usado_para` y `url_origen` de las cinco entradas `descargamasiva_3072026_*` **quedan sin
tocar** -- siguen exactamente como estaban (`sin uso asignado — registro de inventario`,
`url_origen: no determinada`). No se inventa procedencia sobre una coincidencia de nombre de
componente; la coincidencia con `descargaMasivaV2` es una pista de mecanismo, no una prueba de
qué encuesta contienen.

**Esta sesión queda inhabilitada para pre-registrar contra ENUT y contra los cinco ZIP**: leyó
los nombres internos de los cinco `DescargaMasiva_3072026_*.zip` (vía `zipfile`, sin extraer)
y leyó/hasheó los 16 archivos de ENUT descritos arriba. Por ADR-46, ambos quedan fuera de
alcance para pre-registro de esta sesión.
