Contadores movidos: 0.

# Encargo D-2 (mesa #20) — Descarga quirúrgica: los dos diccionarios huérfanos y ENASEM

Sesión Sonnet, Ubuntu con red, worktree nuevo `/home/pc0/mm-d2-descargas`,
rama `sesion/d2-descargas-endutih-mociba-enasem` desde `origin/main` =
`1c09601` (sin diferencia — PR #104 fusionado, coincide exacto con lo que
el encargo declaraba). `data/raw` enlazada a `/home/pc0/mm-corpus/raw`
(ausente al crear el worktree, como espera Bloque D — no es PARO).

## 0 · Arranque (Bloque D) y concurrencia

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Firma correcta (Ubuntu con red). `git branch -r`: `origin/HEAD -> origin/main`,
`origin/claude/adjudicar-r3-1-adr-60-4as2g0` (PR #106, M-1 relanzado, vivo
en nube), `origin/main`, `origin/sesion/hitoD-r3-1-encig` (ya fusionada,
PR #104). W1-P no aparece en remoto (no ha hecho push) — verificado
directo en `/home/pc0/mm-encargo-w1-p-policial`, branch
`sesion/encargo-w1-p-policial`, HEAD `4dca34c`, vivo según mesa. Ningún
archivo de este acto se cruza con la lista de W1-P (`tests/`,
`forense/notas/` con nombre propio, `milpa/procedencia.yaml`) ni con la
de M-1 (`forense/hitoD-preregistro`, `canon/`, `README.md`).

## 1 · Mecanismo: reconstruido y validado contra un resultado ya documentado, no adivinado

El campo `descargado_por` de `endutih2024_bd_dbf_zip`/`mociba2024_bd_csv_zip`
(ya en el manifiesto) cita la API `archivoscompaginacion` con sonda `-r 0-0`.
La URL completa del endpoint y sus parámetros exactos NO estaban en esas
dos entradas — se localizaron en `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
§1 (`https://www.inegi.org.mx/app/api/descarga/componente/descargamasiva/lista/archivoscompaginacion`,
con `idBiinegi`, `tipodocto`, `tema=subtema=areaGeografica=proyecto=anio=0`,
`agrupacion=VG9kYXM=`, `desde=1&hasta=1000&ordenar=orden&orden=desc&ingles=0&datosAbiertos=0&textoBuscar=`)
y en `forense/notas/2026-08-04-cal-conf-faseb-pos4-endireh-paso1.md` §3
(regla de construcción de URL final: `contenidos` + `pathLogico` + `_` +
`extension` + `.zip` para formatos de dato; `pathLogico` + `.` + `extension`
sin `.zip` para `pdf`/`xlsx`).

**Antes de usarlo contra un objetivo real, se validó contra ENDIREH
(`idBiinegi=3117`, `tipodocto=0`)**, cuyo resultado ya está documentado
(42 archivos, incluido el FD en `.../endireh/2021/doc/endireh2021_fd.pdf`):
la reconstrucción dio exactamente 42 entradas, con el mismo FD en el mismo
`pathLogico`. No se adivinó ningún parámetro — se reconstruyó y se
verificó contra un resultado conocido antes de aplicarlo a ENDUTIH/MOCIBA/ENASEM.

## 2 · ENASEM — lista de olas derivada del portal, no del inventario

`data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md`
§12 declara 7 ediciones (2001/2003/2012/2015/2018/2021/2024) sin distinguir
cuáles viven en el portal INEGI (`/programas/enasem/{año}/`) y cuáles solo
en MHAS. Sondeadas las 7 contra el portal INEGI, `curl` real por año:

| Año | `http_code` | Tamaño | Resultado |
|---|---|---|---|
| 2001 | 200 | 13 370 B | soft-404 ("Página no encontrada") — **no lo encontré** bajo este patrón de URL ni en dos variantes de namespace alternas probadas (`/proyectos/investigacion/enasem/2001/`, `/proyectos/enasem/2001/`, mismas 13 370 B) |
| 2003 | 200 | 13 370 B | mismo soft-404 — **no lo encontré** |
| 2012 | 200 | 13 370 B | mismo soft-404 — **no lo encontré** |
| 2015 | 403 | 1 233 B | **hallazgo de vocabulario, cuarta clase**: `403 - Forbidden: Access is denied.` de IIS, reproducible en reintento — NO es el soft-404 (200, 13 370 B) ni "no alcanzable desde este entorno" (que sería bloqueo de red/sandbox antes de llegar al host, firma `000`/`403` al `CONNECT`, `forense/hallazgos.md` 4/ago). Aquí el host respondió con un 403 real, a nivel de aplicación. Se declara como su propia clase, no se colapsa en ninguna de las tres — no se insistió (no se probó `-k`, ni variantes de ruta: la instrucción del encargo es no usar MHAS si INEGI no alcanza para una ola, y aquí INEGI-2015 específicamente no alcanzó). |
| 2018 | 200 | 2 831 B | RESPONDE — `idm="2967"` |
| 2021 | 200 | 3 974 B | RESPONDE — `idm="3295"` (coincide con el ya documentado en el barrido del 4/ago) |
| 2024 | 200 | 3 175 B | RESPONDE — `idm="3504"` (formato de atributo con comillas dobles, no simples — el grep inicial lo perdió, corregido) |

`/programas/enasem/` (sin año) es un stub de redirección JS a `/2024/` — no
enumera ediciones. No se insistió con más variantes de namespace: dos
intentos con la misma firma de soft-404 exacta (13 370 B) es señal
suficiente sin cruzar a "adivinar URLs por analogía" (§3 del encargo, que
prohíbe esto para archivos, no para rutas de portal ya documentadas — pero
se aplicó el mismo criterio conservador).

**Decisión:** se bajan las tres olas que SÍ responden por la vía INEGI —
2018 y 2021 (prioridad del encargo, flanquean la reforma de feb/2019) y
2024 (barata por el mismo mecanismo — API ya resuelto, sin costo adicional
— "si hay más olas por esa vía y son baratas, tráelas"). No se intentó
MHAS para 2015 ni para 2001/2003/2012 — instrucción explícita del encargo.

## 3 · Resolución y sonda, por objetivo (antes de cualquier descarga)

API `archivoscompaginacion` (`tipodocto=0`) por `idBiinegi`, luego `-r 0-0`
sobre la URL resuelta. Ninguna URL de archivo se derivó por analogía de
sufijo — todas salen de `pathLogico`/`extension` que el propio API declaró.

| Objetivo | `idBiinegi` | Archivo (API) | `pathLogico` | URL final | `-r 0-0` |
|---|---|---|---|---|---|
| ENDUTIH 2024 FD | 3413 | "Descriptor de archivos (FD)" | `.../endutih/2024/microdatos/fd_endutih2024` | `.../fd_endutih2024.xlsx` | `206`, `Content-Range: bytes 0-0/155075` |
| MOCIBA 2024 FD | 3438 | "Descriptor de archivos (FD)" | `.../mociba/2024/doc/mociba2024_fd` | `.../mociba2024_fd.xlsx` | `206`, `bytes 0-0/139012` |
| ENASEM 2018 BD | 2967 | "Bases de datos" | `.../enasem/2018/microdatos/enasem_2018_bd` | `..._bd_csv.zip` | `206`, `bytes 0-0/8767343` |
| ENASEM 2018 FD | 2967 | "Descriptor de archivos" | `.../enasem/2018/microdatos/enasem_2018_fd` | `..._fd.xlsx` | `206`, `bytes 0-0/628677` |
| ENASEM 2021 BD | 3295 | "Bases de datos" | `.../enasem/2021/microdatos/enasem_2021_bd` | `..._bd_csv.zip` | `206`, `bytes 0-0/7438658` (coincide exacto con el ya verificado 4/ago) |
| ENASEM 2021 FD | 3295 | "Descriptor de archivos (FD)" | `.../enasem/2021/microdatos/enasem_2021_fd` | `..._fd.xlsx` | `206`, `bytes 0-0/633836` |
| ENASEM 2024 BD | 3504 | "Bases de datos" | `.../enasem/2024/microdatos/enasem_2024_bd` | `..._bd_csv.zip` | `206`, `bytes 0-0/11929796` |
| ENASEM 2024 FD | 3504 | "Descriptor de archivos" | `.../enasem/2024/microdatos/enasem_2024_fd` | `..._fd.xlsx` | `206`, `bytes 0-0/617009` |

**Ninguno de los dos diccionarios (ENDUTIH/MOCIBA) resultó ausente** —
el escenario "no existe FD separado publicado" (legítimo, distinto de "no
lo encontré") **no se activó**: ambos existen como archivo `xlsx`
independiente, resueltos por el API, no por sufijo adivinado.

Los 8 tamaños suman ≈ 30.3 MB — confirma que traer las tres olas de
ENASEM era "barato" en el sentido del encargo.

## 4 · Descarga y registro

Los 8 archivos se bajaron con `curl` real (no solo `-r 0-0`) a
`data/raw/{prog}{año}/`, verificados byte-exacto contra el `Content-Range`
de §3, y registrados con `tests/manifiesto.py --registra` (sha256/tamaño
derivados del archivo, no tecleados):

| id | Archivo | Bytes | `--verifica` |
|---|---|---|---|
| `endutih2024_fd_xlsx` | `endutih2024/fd_endutih2024.xlsx` | 155 075 | COINCIDE |
| `mociba2024_fd_xlsx` | `mociba2024/mociba2024_fd.xlsx` | 139 012 | COINCIDE |
| `enasem2018_bd_csv_zip` | `enasem2018/enasem_2018_bd_csv.zip` | 8 767 343 | COINCIDE |
| `enasem2018_fd_xlsx` | `enasem2018/enasem_2018_fd.xlsx` | 628 677 | COINCIDE |
| `enasem2021_bd_csv_zip` | `enasem2021/enasem_2021_bd_csv.zip` | 7 438 658 | COINCIDE |
| `enasem2021_fd_xlsx` | `enasem2021/enasem_2021_fd.xlsx` | 633 836 | COINCIDE |
| `enasem2024_bd_csv_zip` | `enasem2024/enasem_2024_bd_csv.zip` | 11 929 796 | COINCIDE |
| `enasem2024_fd_xlsx` | `enasem2024/enasem_2024_fd.xlsx` | 617 009 | COINCIDE |

`--verifica` corrido un `--id` por invocación (defecto conocido de
invocación múltiple, `hallazgos.md` 4/ago — no se tocó `tests/`, fuera de
perímetro de este acto). Los 8 dan `COINCIDE`.

**Verificado desde worktree hermano** (`/home/pc0/Modelado-Mexicano`,
mismo symlink `data/raw -> /home/pc0/mm-corpus/raw`): los 8 archivos son
visibles y sus sha256, recalculados de forma independiente con `sha256sum`
desde ese otro worktree, coinciden dígito por dígito con lo que
`--registra` escribió. El defecto de `PR #77` (payloads que se quedan solo
en el worktree local) no se reprodujo.

## 5 · Declaración de no-apertura (§5 del encargo)

**Cero apertura de contenido.** Ninguno de los 8 archivos se extrajo,
abrió ni leyó — los 2 ZIP de ENASEM (2018, 2021, 2024 — tres, no dos) no
se descomprimieron; los 6 XLSX (2 FD de ENDUTIH/MOCIBA + 4 de ENASEM, dos
por ola) no se abrieron con ninguna librería. Verificación por tamaño
exacto contra `Content-Range` y por `sha256` de archivo completo, nunca
por inspección de contenido.

## 6 · ADR-46 — corrección al propio encargo, declarada (terreno ≠ supuesto)

El encargo (§5, paso 3) afirma que "cero apertura de contenido... mantiene
esta sesión limpia y habilitada para pre-registrar contra ENDUTIH, MOCIBA
y ENASEM después (ADR-46)". Verificado el texto real de ADR-46
(`canon/gobernanza-v1_15.md:367` y su fila `1.14`) antes de obedecer esa
lectura: **ADR-46 declara dos niveles, no uno** — "(2) dos niveles —
descarga ciega (no contamina) vs. exploración de estructura (contamina
parcialmente, declarar hasta dónde); (3) condición verificable — una
sesión pre-registra contra una fuente si no leyó `data/raw/` de esa
fuente, ni la bitácora de su tanda, **ni ningún registro de exploración de
su estructura**". Esta sesión sí exploró estructura: consultó el API
`archivoscompaginacion` (parámetros, `pathLogico`, `extension`, tamaños
declarados) para ENDUTIH, MOCIBA, ENASEM 2018/2021/2024 — seis consultas
de estructura, no solo descarga ciega de una URL ya conocida. Por el
criterio explícito de ADR-46, **esta sesión queda parcialmente
contaminada para pre-registrar contra esas fuentes** — no "limpia y
habilitada" sin matiz, como decía el encargo. Declarado hasta dónde, "el
conservador declara más exploración, no menos" (ADR-46(3)):

- **Explorado (estructura, vía API):** ENDUTIH 2024, MOCIBA 2024, ENASEM
  2018/2021/2024 — nombres de archivo publicados (`titulo`,
  `tipoInformacion`), `pathLogico`, `extension`, tamaño declarado. Ningún
  contenido de archivo (ninguna fila, ninguna etiqueta de variable, ningún
  texto de pregunta).
- **También consultado, como validación del mecanismo (no como
  exploración nueva):** ENDIREH 2021 (`idBiinegi=3117`) — replay de un
  resultado ya publicado en `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`,
  sin descubrir nada que esa nota no dijera ya.
- **No explorado, no abierto:** contenido de ningún archivo de las 8
  fuentes — la contaminación de esta sesión es de estructura, no de
  contenido, y es más superficial que la de la sesión previa sobre ENASEM
  (`forense/notas/2026-08-04-enasem-paso1-descriptor.md`, "Encargo S"),
  que sí abrió el codebook DDI completo de 2018/2021 (nombres de variable,
  etiquetas, texto literal de preguntas, frecuencias marginales) y se
  declaró **permanentemente inhabilitada** para ENASEM por eso — una
  contaminación de contenido, no solo de estructura.

**No es PARO** — el encargo pedía la descarga, no el pre-registro; esta
nota corrige la lectura de ADR-46 que el encargo trae, para que quien
pre-registre después sepa que esta sesión no es la "sesión limpia" que
necesita (tendría que ser una que no haya corrido las consultas de
estructura de esta nota), igual que ya no lo era la de "Encargo S" por una
vía más profunda (contenido).

## 7 · Suite

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Sin cambio frente a la línea base pre-existente — este acto no introdujo
ningún FAIL/WARN nuevo.

## Prohibiciones respetadas

No se persiguieron las 26 fuentes sin payload restantes. No se construyó
ninguna URL de archivo por analogía de sufijo — las 8 URLs finales salen
de `pathLogico`/`extension` que el propio API `archivoscompaginacion`
declaró, verificado además por replay exacto contra el resultado ya
documentado de ENDIREH antes de aplicarse a un objetivo real. No se usó
el portal MHAS (`mhasweb.org`) — ni siquiera se sondeó, a diferencia de
"Encargo S", que sí lo sondeó (sin descargar) y lo dejó documentado como
alcanzable pero fuera de uso. No se abrió ningún ZIP/XLSX. No se tocó
`milpa/`, `canon/`, `tests/` ni `forense/hitoD-preregistro`. No se
adjudicó ni se propuso fila para `R1.3` ni `R5.1` — eso es trabajo de
quien pre-registre, con la contaminación de esta sesión ya declarada en
§6 para que lo tome en cuenta.
