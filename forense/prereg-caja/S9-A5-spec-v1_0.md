# S9 · Pre-registro del protocolo de adquisición PDN (R0–R7) — `ACTO MAESTRA38-A5`

### `prereg-caja-S9-A5` · **v1.0** · 6 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S9-A5-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S9-A5`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Congelamiento, ANTES de correr ninguna ruta sustantiva de este acto, de la Parte I del encargo (`forense/encargos/2026-09-06-MAESTRA38-A5-PDN-BULK-Y-PROXY.md`) — el protocolo de ocho rutas independientes (`R0`–`R7`) para adquirir/verificar la fila de cola `PDN_SESNA_S1_S2_S3_S6`, con su tabla de éxito por objeto y su regla de cierre. |
> | **QUÉ NO ES** | No es la ejecución (eso es `COMMIT-2`, `forense/notas/2026-09-06-MAESTRA38-A5-resultados.md`). No mide ninguna regla del canon (0 necesidades citan PDN hoy). No sustituye ni reabre lo que `ACTO MAESTRA38-A4` + `ADENDA-A4-rutas-PDN` ya dejaron depositado y registrado — este acto no toca esas salidas. |
> | **VERIFICAS ASÍ** | Compara cada ruta `R0`–`R7` de `COMMIT-2` contra el texto verbatim de abajo: cada una debe tener, en la nota de resultados, su comando y su salida cruda pegados, o una línea «no aplica porque …» con la evidencia de por qué no aplica (regla de cierre, §1). |

**Acto:** `ACTO MAESTRA38-A5 · PDN-BULK-Y-PROXY`, 6/sep/2026, entorno **UBUNTU** (corpus + red, fuera del sandbox de bash para las peticiones — `dangerouslyDisableSandbox: true`), sobre `origin/main = 45f1986b546574c97a01be2617465ced05a31842` (SHA de fusión de `A4`, PR #552, verificado por `git log -1`/`git merge-base --is-ancestor` contra el clon de esta sesión).

---

## 0 · Consecuencia de la compuerta sobre el alcance (verificada, no heredada)

`COMPUERTA: A4 fusionado` — verificada por PRODUCTO en el paso 2 de `/acto`:
`gh pr view 552` → `MERGED`, `mergedAt 2026-09-06T09:19:50Z`, `mergeCommit 45f1986b…`; los tres archivos que `A4` debió producir existen en `origin/main` (`git cat-file -e`); la fila 28 de `data/cola-adquisicion-v1_0.tsv` en `origin/main` lee:

```
PDN_SESNA_S1_S2_S3_S6  OBTENIDO  sin-prioridad-asignada  https://www.plataformadigitalnacional.org/  pdn_s3v2  ...
```

Estado real = **`OBTENIDO`** (no `OBTENIDO-PARCIAL`, que es lo que citaba el encargo original — desactualizado; `A4` cerró la fila completa). Por la propia cláusula de la compuerta del encargo:

> «si `OBTENIDO` completo en S1+S2+S6, A5 se reduce a control de calidad y cron; si `NO-OBTENIDO` o parcial, A5 corre la Parte I entera»

→ **este acto corre en la rama reducida: control de calidad sobre lo que `A4` dejó, y cron, no la Parte I entera.** La Parte I completa (§1–§9 de abajo) se congela igual, verbatim, como spec de referencia — es el procedimiento que regiría si algún sistema resultara realmente parcial al verificar, y es el que un futuro re-uso de esta fila (regeneración de los bulk, ver §7 «Qué es éxito») deberá seguir.

El primer resultado que produzca este procedimiento es el que se reporta.

---

## 1 · Regla de cierre (verbatim, la que manda)

> La fila 28 (o cualquiera de sus cuatro sistemas) no puede rotularse `NO-OBTENIDO-POR-ESTE-AGENTE` hasta que las rutas `R0`–`R7` tengan, cada una, su comando y su salida cruda pegados en la nota, o una línea «no aplica porque …» con la evidencia. Un `000`, un `403`, un `200` con shell vacío o un «Welcome to nginx» en una ruta es un dato sobre esa ruta, no un veredicto (A.5). Tres hallazgos distintos por ruta, nunca colapsados: **RED** (`000`/timeout) · **SERVIDOR** (`4xx`/`5xx` con cuerpo) · **VACÍO** (`200` sin contenido útil: shell React, nginx default, `[]`). Toda sonda declara bytes recibidos y `Content-Type` (A.13).

## 2 · Disciplina de red (verbatim)

> Todo curl fuera del sandbox de bash (A4 midió `000` dentro / `200` fuera → usa `dangerouslyDisableSandbox: true` para las peticiones de red). `UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"`. `--max-time 60`. Una petición por segundo, sin paralelismo. Sin credenciales, sin formularios, sin clickwrap. Términos del portal: `https://plataformadigitalnacional.org/terminos` — se abre, se cita una línea en la nota.

**Hallazgo de este acto sobre §2:** en esta sesión, `curl` a `https://www.inegi.org.mx/`, `https://api.plataformadigitalnacional.org/s1/v1/providers` y `https://www.plataformadigitalnacional.org/declaraciones` respondieron `200` **dentro** del sandbox de bash (a diferencia de lo que `A4` midió — `000` dentro/`200` fuera). Declarado en `COMMIT-2`; no cambia el protocolo, que exige `dangerouslyDisableSandbox: true` para toda petición de red sin condicionarlo al resultado dentro del sandbox.

## 3 · R0 · Control positivo (verbatim)

> `curl -sS -A "$UA" -o /dev/null -w "%{http_code} %{size_download}\n" --max-time 30 https://www.inegi.org.mx/` — sin `200` aquí ninguna ruta produce hallazgo: es RED del entorno.

## 4 · R1 · Backends públicos de la PDN (proxy sin autenticación) (verbatim)

> A4 ya midió que responden `200` SIN token (S1 `totalRows` 153 011) — verifica que sigue siendo cierto y úsalo como control.
> **S1:** `curl -sS -A "$UA" -H "Accept: application/json" https://api.plataformadigitalnacional.org/s1/v1/providers` · POST a `/s1/v1/search` con `{"supplier_id":"EDOMEX","page":1,"pageSize":10}`, pega `pagination` completo, escala `pageSize` 10→100→500→1000 y reporta el tope real; pagina por cada `supplier_id` hasta `hasNextPage=false`. Lista de control: `monitorearSistemas/utils/providers_catalog.json` (66 el 6/sep — reporta cuántas devuelve hoy, no heredes 66).
> **S2:** POST `{}` a `/s2/api/v1/suppliers`, `/s2/api/v1/summary` (trae `totalRows` por proveedor), `/s2/api/v1/search`. Extra si `search` falla: `/s2/api/v1/entities`, `/s2/api/v0/getTotalRows`, `/s2/api/v0/getInstituciones`.
> **S6:** POST `{}` a `"/s6/api/v1/search?supplier_id=SHCP"` (lee `pagination`), `/s6/api/v1/summary`, `/s6/api/v1/buyers`. Tope de `pageSize` en código: 200, default 10.
> **S3** (control, no objetivo — ya en corpus como `pdn_s3v2`): `curl /s3-wrapper/api/v1/providers`. Compara conteo por entidad contra los 34 JSON de `PDN_S3v2.zip` → `CONTROL-COINCIDE` / `CONTROL-DIFIERE` (fecha).

## 5 · R2 · Botón «Descarga todos los datos { JSON }» (verbatim)

> El bulk oficial. Son `href` estáticos inyectados en el bundle React desde `.env` (`REACT_APP_S1_BULK`, `REACT_APP_BULK_S2`, `_S3_SERVIDORES`, `_S3_PARTICULARES`, `_S6`). A4 ya los encontró y reporta que apuntan a Google Drive. Extrae las cinco URLs del bundle: baja el shell de `https://www.plataformadigitalnacional.org/declaraciones` con cookie jar (dos veces, la segunda con la cookie `__zjc`), `grep '<script[^>]+src="[^"]+"'`, baja el `main.*.js` y `grep -oE 'https?://[^"'"'"' ]+\.(zip|json|gz|tgz|tar|7z|csv)'`. Si el shell pesa <2 KB y no trae `<script src=` → VACÍO por Zenedge; tres variantes máximo con salida cruda: (a) `--http2` + `Accept` de navegador + `Accept-Language es-MX`; (b) misma petición 5 s después con la cookie anterior; (c) la ruta `/static/js/` directa. Tres VACÍO → R2 cierra «bundle no accesible sin JS en N intentos» y pasa a R6. Con cada URL bulk: `curl -sSI` + `Range: bytes=0-500` → `Content-Type`, `Content-Length`; descarga completa; A.7 doble descarga (hash crudo + hash de contenido, los bulk pueden llevar marca de generación); `testzip`. Control positivo obligatorio: bulk de S3-servidores contra `pdn_s3v2` (sha256 `923d0dd0…`): COINCIDE / DIFIERE-CON-FECHA.

## 6 · R3–R7 (verbatim)

> **R3 · Espejo temporal (Wayback), si R2 da VACÍO:** `curl "https://web.archive.org/cdx/search/cdx?url=plataformadigitalnacional.org/*&filter=mimetype:application/javascript&limit=20&collapse=urlkey"` y la variante con `*.plataformadigitalnacional.org` y `mimetype:application/zip`. Reporta RED/SERVIDOR/VACÍO.
> **R4 · OpenAPI del portal:** `https://www.plataformadigitalnacional.org/oas/ui/` y `/validapi/` → `grep -oE '"(url|servers)"[^,]{0,120}'`. Un VACÍO aquí no invalida R1.
> **R5 · GitHub** — siempre alcanzable, para no inventar rutas: `PDNMX/api_docs` (OAS de S1/S2/S3/S6) · `PDNMX/monitorearSistemas` (URLs de producción y `providers_catalog.json`) · `PDNMX/pdn` (`grep -rn "process.env.REACT_APP_S" src`). Cita commit leído.
> **R6 · Navegador en la caja** — sólo si R2 y R3 dan VACÍO: `which chromium chromium-browser google-chrome`; `python3 -c "import playwright"`. Si hay navegador: carga `/declaraciones`, espera red idle, vuelca `document.querySelectorAll('a[href]')` y `performance.getEntriesByType('resource')`. Si no hay: `pip install playwright --break-system-packages && playwright install chromium` — se declara y se hace, no se salta. Si tampoco: nace la receta ≤1 min para mesa (clic derecho sobre el ícono de nube bajo «Descarga todos los datos» → «Copiar dirección de enlace» × 5). Esa receta es entregable de R6, no sustituto de R1.
> **R7 · Hermanas en datos abiertos federales:** `curl "https://datos.gob.mx/api/3/action/package_search?q=plataforma+digital+nacional&rows=20"` y lo mismo con `q=declaraciones+patrimoniales` y `q=contrataciones+abiertas+OCDS`.

## 7 · Qué es éxito, por objeto (verbatim — tabla de éxito)

| Objeto | Criterio de éxito |
|---|---|
| S1 bulk | archivo >1 MB, JSON/ZIP válido, `testzip` OK, depósito en `descargas_mx/PDN-2026-09/S1/` con A.7 |
| S1 barrido | registros bajados = Σ `totalRows` por proveedor (o lista de proveedores en error con su `error.status`), un `.tar.gz` por sistema con `MANIFIESTO-interno.tsv` (fecha, `supplier_id`, `totalRows`, bajados, páginas, tope `pageSize`) |
| S2 y S6 | ídem S1 barrido (S6 usa `pagination.total` como denominador) |
| S3 | control `COINCIDE`/`DIFIERE` contra `pdn_s3v2`, sólo nota, no se re-registra |
| Resumen | `data/pdn-adquisicion-resumen-v1_0.tsv` (sistema · ruta que funcionó · objeto · bytes · sha256 crudo · sha256 contenido · fecha), nuevo |

Bulk y barrido son dos payloads distintos del mismo sistema (A.7: identidad = contenido): si ambos llegan, se registran ambos, con nota cruzada. Anti-PR#77: al cerrar, `ls -la` del corpus compartido, no del worktree.

**Nota de este acto sobre la ruta de depósito de S1/S2/S6:** la tabla de arriba (heredada verbatim del encargo) declara `descargas_mx/PDN-2026-09/S1/` como destino de S1 bulk. `A4` NO depositó ahí — depositó en el corpus compartido `data_raw` (`/home/pc0/mm-corpus/raw/pdn_bulk_2026_09/`), con `raiz: data_raw` en el manifiesto. Es una **desviación de ruta declarada**, evaluada en `COMMIT-2` (§ hallazgos de `forense/notas/2026-09-06-MAESTRA38-A5-resultados.md`) — no una ruta faltante: el objeto llegó, con A.7, a una raíz igualmente compartida y ya registrada.

## 8 · El primer resultado que produzca este procedimiento es el que se reporta.

Ninguna ruta se reintenta buscando un resultado mejor una vez que produjo un hallazgo válido (RED/SERVIDOR/VACÍO/ÉXITO) con su evidencia cruda. Reintentos sólo dentro del límite que cada ruta ya declara (p. ej. las tres variantes de R2).

## 9 · Verificación al cerrar

`COMMIT-2` (`forense/notas/2026-09-06-MAESTRA38-A5-resultados.md`) debe traer, ruta por ruta, comando + salida cruda o «no aplica porque …» con evidencia — verificable línea por línea contra §3–§6 de este documento.
