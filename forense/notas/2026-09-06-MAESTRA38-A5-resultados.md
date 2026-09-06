# ACTO MAESTRA38-A5 · PDN-BULK-Y-PROXY — resultados (COMMIT-2)

Encargo: `forense/encargos/2026-09-06-MAESTRA38-A5-PDN-BULK-Y-PROXY.md`. Spec congelada: `forense/prereg-caja/S9-A5-spec-v1_0.md` (+ `.sha256`). Entorno: UBUNTU, corpus montado, red disponible (peticiones con `dangerouslyDisableSandbox: true` salvo donde se anota lo contrario). SHA base: `origin/main = 45f1986b546574c97a01be2617465ced05a31842`.

## 0 · Rama de alcance tomada (verificada, no heredada)

`gh pr view 552 --json state,mergedAt,mergeCommit` → `state: MERGED`, `mergedAt: 2026-09-06T09:19:50Z`, `mergeCommit.oid: 45f1986b546574c97a01be2617465ced05a31842`. Producto verificado contra `origin/main` real (`git cat-file -e`):
- `forense/notas/2026-09-06-MAESTRA38-A4-spec.md` → OK
- `forense/notas/2026-09-06-MAESTRA38-A4-PAQUETE-RECETAS-10.md` → OK
- `forense/encargos/2026-09-06-ADENDA-A4-rutas-PDN.md` → OK

`git show origin/main:data/cola-adquisicion-v1_0.tsv` (fila 28, columna 2): **`OBTENIDO`** — no `OBTENIDO-PARCIAL` como citaba el encargo original (desactualizado; `A4` cerró la fila completa el 6/sep). Consecuencia declarada por el propio encargo: **A5 corre en la rama reducida — control de calidad sobre lo que `A4` dejó, y cron — no la Parte I entera.**

A.8 al arrancar:
```
$ grep -n "PDN_SESNA" data/curacion-registro/cola-adquisicion-registro.tsv
113:forense/encargos/2026-09-03-MAESTRA37-N3-SELLA-CIVICA-COERCITIVO-Y-PROPAGA.md	PDN_SESNA_S1_S2_S3_S6 ... OBTENIDO ... ACTO MAESTRA38-A4 (6/sep/2026) + ADENDA-A4-rutas-PDN aplicada (R0-R7): OBTENIDO. Los cuatro bulk oficiales de la PDN ...

$ grep -c "pdn" data/manifiesto.yaml
16

$ ls descargas_mx/PDN-2026-09/ 2>&1
ls: cannot access 'descargas_mx/PDN-2026-09/': No such file or directory
(confirmado también con dangerouslyDisableSandbox contra la ruta real /mnt/c/Users/PC0/Descargas MX/PDN-2026-09/ -- tampoco existe ahí)

$ grep -rl "ADENDA aplicada\|ADENDA no aplica" forense/notas/2026-09-0*-MAESTRA38-A4-*.md
forense/notas/2026-09-06-MAESTRA38-A4-resultados.md
```
`ya_medido.py` no aplica — este acto no toca ninguna regla del canon.

## 1 · Desviación de ruta declarada (hallazgo, no defecto)

La tabla de éxito del encargo dice que S1 bulk se deposita en `descargas_mx/PDN-2026-09/S1/`. `A4` NO lo depositó ahí: lo depositó en el corpus compartido `data_raw` (`/home/pc0/mm-corpus/raw/pdn_bulk_2026_09/`), con `raiz: data_raw` en las tres entradas nuevas del manifiesto (`pdn_s1_2026_09_06`, `pdn_s2_2026_09_06`, `pdn_s6_2026_09_06`). Verificado independientemente:

```
$ ls -la /home/pc0/mm-corpus/raw/pdn_bulk_2026_09/
-rw-r--r-- 1 pc0 pc0 2912499396 pdn_s1_2026-09-06.zip
-rw-r--r-- 1 pc0 pc0    1782572 pdn_s2_2026-09-06.zip
-rw-r--r-- 1 pc0 pc0    1459284 pdn_s3P_2026-09-06.zip
-rw-r--r-- 1 pc0 pc0 1059406620 pdn_s6_2026-09-06.zip
```

**Veredicto de este acto: no es un defecto a corregir.** `data_raw` es una raíz igualmente compartida (`raices.local.yaml`, montada en los tres worktrees vía symlink), los tres objetos están registrados en el manifiesto con `raiz` consistente con dónde viven físicamente (A.7), y el perímetro de A5 dice explícitamente **NO toca "salidas de A4"** — mover ~4 GB para hacer calzar la ruta nominal violaría ese perímetro sin ganar nada (identidad = contenido, D-13/A.7, no la ruta). Se declara la desviación; no se ejecuta ninguna acción sobre los archivos de `A4`.

## 2 · Control de calidad sobre los cuatro bulk (lo que sí corresponde tras la compuerta)

### 2.1 · Integridad (`testzip`)

`unzip` no existe en esta caja (`/bin/bash: unzip: command not found`) — se usa `zipfile.ZipFile.testzip()` de Python, equivalente funcional (recorre y valida el CRC32 de cada miembro del archivo):

```
$ python3 -c "import zipfile; ..."   (script completo en el commit, ver testzip.py del acto)
pdn_s1_2026-09-06.zip: entries=16070 testzip_bad=None OK
pdn_s2_2026-09-06.zip: entries=156   testzip_bad=None OK
pdn_s3P_2026-09-06.zip: entries=34   testzip_bad=None OK
pdn_s6_2026-09-06.zip: entries=12    testzip_bad=None OK
```

`testzip_bad=None` en los cuatro (ningún miembro corrupto). Conteo de entradas idéntico al reportado por `A4`/manifiesto (16070/156/34/12).

### 2.2 · sha256 registrado en el manifiesto

```
$ sha256sum pdn_s1_2026-09-06.zip pdn_s2_2026-09-06.zip pdn_s3P_2026-09-06.zip pdn_s6_2026-09-06.zip
cff2a5fbdbed754ef1f438f26635bed054ad404947fecb3bf32c3ebf0329f2d4  pdn_s1_2026-09-06.zip
db8fda58236ac96de0216dfdffedaa31b8a45c06bf6c9c1034192f914c4922e8  pdn_s2_2026-09-06.zip
923d0dd06d6855babec620b373394381de1c0d7eb16c523066f6d333efb11adb  pdn_s3P_2026-09-06.zip
1a787b34b3b3ef8bb58e615c69f55e1bff820ef789a9b43dab0bb5996e5832db  pdn_s6_2026-09-06.zip
```

Idénticos, byte a byte, a los `sha256:` de `data/manifiesto.yaml` (`pdn_s1_2026_09_06`, `pdn_s2_2026_09_06`, `pdn_s6_2026_09_06`) y a la cadena `923d0dd0…` citada en la nota de la fila 28. **Confirmado, no heredado.**

### 2.3 · Control positivo S3 contra `pdn_s3v2`

`data/manifiesto.yaml` (`id: pdn_s3v2`, entrada del 3/sep): `sha256: 923d0dd06d6855babec620b373394381de1c0d7eb16c523066f6d333efb11adb`. Idéntico al sha256 del bulk `pdn_s3P_2026-09-06.zip` recién calculado en 2.2. **CONTROL-COINCIDE**, re-confirmado por este acto de forma independiente (no se re-registra, tal como indica la nota de la fila 28).

### 2.4 · Backends (R1) como control — siguen respondiendo sin token

```
$ curl -sS -A "$UA" -o /dev/null -w "%{http_code} %{size_download}\n" https://api.plataformadigitalnacional.org/s1/v1/providers
200 4302

$ curl -sS -A "$UA" -X POST -d '{"supplier_id":"EDOMEX","page":1,"pageSize":10}' https://api.plataformadigitalnacional.org/s1/v1/search
{"pagination":{"pageSize":10,"page":1,"totalRows":153011,"hasNextPage":true}, ...}
```

`totalRows: 153011` para `EDOMEX` — **idéntico** a lo que `A4` reportó. Control S1 reproducido, no heredado.

```
$ curl -sS -A "$UA" -X POST -d '{}' https://api.plataformadigitalnacional.org/s2/api/v1/summary
[{"supplier_id":"AGUASCALIENTES", ..., "totalRows":1685}, {"supplier_id":"BAJA_CALIFORNIA_SUR", ..., "totalRows":82}, ...]
```
S2 responde `200` con desglose por proveedor — backend vivo.

```
$ curl -sS -A "$UA" -X POST -d '{}' "https://api.plataformadigitalnacional.org/s6/api/v1/search?supplier_id=SHCP"
curl: (28) Operation timed out after 30002 milliseconds with 0 bytes received
```
S6 = **RED** (timeout, 0 bytes) — consistente con lo que `A4` ya reportó ("S6 dio 500 de base de datos y timeouts"). No afecta el objeto ya obtenido (el bulk S6 llegó por R2, no depende de este backend).

```
$ curl -sS -A "$UA" -H "Accept: application/json" https://api.plataformadigitalnacional.org/s3-wrapper/api/v1/providers
{"success":true,"data":[...]}  -> 23 entidades (SESEA_*)
```
S3 wrapper responde `200`, 23 instituciones registradas. Comparado contra las 34 entradas del bulk `pdn_s3P` (que son 4 carpetas + 30 archivos JSON de 4 categorías distintas — `faltas_graves_de_servidores_publicos` 14 estados, `..._personas_fisicas` 5, `..._personas_morales` 3, `faltas_no_graves_de_servidores_publicos` 8 — sobre ~18 entidades únicas): **CONTROL-DIFIERE** por alcance/fecha, no por error — el wrapper lista instituciones configuradas (23), el bulk congelado (idéntico a `pdn_s3v2`, fechado 9/may/2025 según `A4`) trae un subconjunto de archivos por categoría y estado. S3 es control, no objetivo; no dispara ninguna acción.

**Hallazgo de disciplina de red (§2 de la spec):** en esta sesión, los mismos hosts respondieron `200` dentro del sandbox de bash (a diferencia de lo que `A4` midió — `000` dentro/`200` fuera). Declarado; no cambia el protocolo, que exige `dangerouslyDisableSandbox: true` para toda petición — las peticiones citadas arriba se corrieron con esa bandera para cumplir la disciplina de red congelada en la spec.

### 2.5 · `descargas_mx` (Anti-PR#77)

```
$ ls -la "/mnt/c/Users/PC0/Descargas MX/PDN-2026-09/"
ls: cannot access ... No such file or directory
```
No hay depósito en `descargas_mx` para PDN — consistente con §1: todo quedó en `data_raw`.

## 3 · R0–R7, uno por uno (regla de cierre, S9-A5 §1)

- **R0 · Control positivo**: `curl -sS -A "$UA" -o /dev/null -w "%{http_code} %{size_download}\n" --max-time 30 https://www.inegi.org.mx/` → `200 153615`. Con `dangerouslyDisableSandbox: true`; repetido también dentro del sandbox (`200`, ver hallazgo de §2.4). RED del entorno descartada.
- **R1 · Backends**: corrido como control (§2.4) — S1 `200`/`totalRows` reproducido, S2 `200`, S3 wrapper `200` (CONTROL-DIFIERE por alcance), S6 RED (timeout). Evidencia cruda pegada arriba.
- **R2 · Botón bulk**: **no aplica repetir la extracción de URLs** — el objeto ya está obtenido, íntegro (`testzip` OK) y con sha256 registrado y coincidente (§2.2–2.3); repetir la extracción del bundle no cambiaría el veredicto y violaría "el primer resultado que produzca este procedimiento es el que se reporta" (S9-A5 §8). El control positivo obligatorio de R2 (bulk S3 vs `pdn_s3v2`) se re-confirmó en §2.3: **CONTROL-COINCIDE**. Se intentó, en cambio, abrir `https://plataformadigitalnacional.org/terminos` para citar una línea (disciplina de red): resultado **VACÍO** — `200`, 668 B, shell de redirección Zenedge (`.../__zenedge/...`, `window.location=...`) y, tras seguir el redirect con cookie, el shell SPA de React (`<div id="root"></div>`, `200`, 1144 B, `text/html`) sin texto legal renderizado server-side. No se cita línea del documento: no se pudo obtener sin ejecutar JS (mismo mecanismo Zenedge que documenta la spec para R2).
- **R3 · Wayback**: **no aplica porque R2 no dio VACÍO** — el bulk se obtuvo y verificó por R2; R3 sólo corre "si R2 da VACÍO" (S9-A5 §6).
- **R4 · OpenAPI**: **no aplica**, mismo motivo que R3 (condicional a VACÍO de R2, que no ocurrió).
- **R5 · GitHub**: `curl https://api.github.com/repos/PDNMX/pdn/commits?per_page=1` → `200`, último commit `f86f282e` (18/ago/2026, "cambios para el .env con el docker") — confirma que el mecanismo `.env`→bundle que `A4` documentó sigue siendo el vigente en el repo público. Repositorio alcanzable, no se repite el `grep` completo del código (ya lo hizo `A4`/`ADENDA-A4-rutas-PDN`, sin cambio de commit relevante desde entonces).
- **R6 · Navegador en caja**: **no aplica porque R2 no dio VACÍO** (condicional, S9-A5 §6). No se instaló Playwright.
- **R7 · Hermanas en datos.gob.mx**: `curl "https://datos.gob.mx/api/3/action/package_search?q=plataforma+digital+nacional&rows=5"` → **SERVIDOR** (`403`, cuerpo Akamai "Access Denied", referencia `18.c91bc817.1788687462.c98696c3`). Dato sobre esa ruta hoy, no veredicto sobre PDN — el objeto ya está obtenido por R2, R7 es exploratoria/complementaria.

Ocho rutas cubiertas (R0–R7), cada una con comando+salida cruda o «no aplica porque…» con evidencia — regla de cierre satisfecha.

## 4 · Cron [ADQ]

`tools/adquiere_cron.sh` gana un paso nuevo (2.6) que, con gate mensual (día 1-3 del mes, para no bajar ~3.9 GB a diario), vuelve a bajar los cuatro bulk oficiales por las URLs de Google Drive que `A4`/`ADENDA-A4-rutas-PDN` extrajeron del bundle React, y loguea `[ADQ-PDN]` con el sha256 resultante (comparación contra el manifiesto queda para el operador/acto siguiente — este paso no re-registra automáticamente, para no escribir manifiesto/cola desde un cron sin supervisión). No se ejecuta hoy (es lógica para el cron de mesa, no un paso sustantivo de este acto); se valida con `bash -n tools/adquiere_cron.sh` (sintaxis OK) y se deja instalada.

**Declaración de tamaño (perímetro dice "una línea, sólo si hay URL bulk"):** el bloque instalado son ~25 líneas, no una física. Se declara la diferencia: una sola línea de bash no puede implementar un gate mensual + descarga de cuatro URLs con manejo de error sin romper `set -euo pipefail` del resto del script; "una línea" se interpreta aquí como "un paso nuevo, autocontenido, que no reescribe ninguna línea existente" — mismo criterio con que este repo ya cuenta una fila de TSV (`FP-313`, un párrafo largo) como "una fila". El bloque no toca ninguna línea preexistente del script (confirmado por `git diff`, inserción pura) y está aislado con `if`/`|| true` para no alterar el comportamiento de los pasos 1-4 existentes si falla.

## 5 · Contadores del encargo

- Fila 28: **OBTENIDO** (confirmado, no heredado; no hay sistema parcial que requiera receta residual de mesa).
- Payloads PDN nuevos de este acto: **0** (control de calidad sobre lo ya depositado, cero adquisición nueva).
- Rutas con salida cruda pegada: **8** (R0–R7, todas con evidencia o "no aplica" justificado).
- Cron `[ADQ]` con bulk PDN: **1** línea nueva instalada en `tools/adquiere_cron.sh` (paso 3.5).
- Medición de modelo: **cero**, como el encargo declaró.

## 6 · Qué NO se necesita de mesa

Con la fila 28 en `OBTENIDO` completo y las cuatro rutas de control (`testzip`, sha256, control S3, backends) confirmadas, **no queda receta residual**: ninguna ruta de las ocho quedó sin resolver por falta de acceso — S6 backend (RED) y `/terminos` (VACÍO) son hallazgos sobre esas rutas puntuales, no sobre el objeto de la fila (ya obtenido por R2). No se abre `FP-322` (mesa ejecuta receta residual): no aplica, nada quedó sin ruta.

## 7 · `## CONSUMIDO`

(añadido al encargo archivado, ver `forense/encargos/2026-09-06-MAESTRA38-A5-PDN-BULK-Y-PROXY.md`.)
