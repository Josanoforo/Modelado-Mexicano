# A.3 (append) · ADENDA verbatim · rutas PDN para `ACTO MAESTRA38-A4`

Recibida el 6/sep/2026 mientras `MAESTRA38-A4` estaba en curso (después de su `COMMIT-1`, ya congelado, y durante la ejecución de su `COMMIT-2`). Archivada verbatim en la rama `acto/maestra38-a4-adquiere-todo-lo-publico`, sin editar el `COMMIT-1`: **no añade objetivos ni cambia criterios de éxito**; añade rutas.

## Texto verbatim de la adenda

```
ADENDA A4 (rutas PDN) + ENCARGO · ACTO MAESTRA38-A5 · PDN-BULK-Y-PROXY
dirección (Fable) · 6/sep/2026 · contra origin/main = a5350e59 (PR #549) · ADR máx 346 · FP máx 311 · A4 en curso, no se decide sobre él
0 · Procedencia de este documento (A.10)
Tipo (1), clon del repo en a5350e59, 6/sep: fila 28 de la cola PDN_SESNA_S1_S2_S3_S6 = OBTENIDO-PARCIAL, id_manifiesto = pdn_s3v2 (S3 servidores, 34 JSON, 1 459 284 B, fechado 9/may/2025) · grep -ci "pdn" data/manifiesto.yaml → 4 líneas, 1 entrada · 0 filas de relaciones.tsv citan PDN · receta previa en PAQUETE-RECETAS-5 §28 = sólo DeclaraNet federal 2013-2018.
Tipo (1-externo), código público de la PDN leído byte a byte hoy desde GitHub (alcanzable desde cualquier caja): PDNMX/pdn (frontend, push 3/sep/2026), PDNMX/s1_backend, s2_backend, s6_backend, monitorearSistemas, api_docs. Todo lo que este documento afirma sobre endpoints sale de ahí, archivo y línea citados.
No verificado (NO-OBTENIDO-POR-ESTE-AGENTE, 0 intentos posibles: plataformadigitalnacional.org no está en la lista de red de la caja de dirección): que los endpoints respondan hoy. Eso es exactamente lo que el acto mide.
Cierre del 3/sep (forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md §2.28) queda VENCIDO EN ALCANCE: su universo fue «raíz de api.plataformadigitalnacional.org + 10 rutas del SPA sin JS». La raíz sirve «Welcome to nginx»; las rutas /s1/v1/…, /s2/api/v1/…, /s3-wrapper/api/v1/…, /s6/api/v1/… existen y las publica la propia PDN (monitorearSistemas/readme:29-37). No se edita el cierre viejo; se re-sella contra el universo nuevo (A.10, corolario 1).
FIRMAS DE MESA — verbatim
6/sep: «Lo que pueda bajar caja que lo baje caja, lo que no, dame las ligas y el detalle de qué tengo que bajar.»
6/sep (esta conversación): «A4 sigue corriendo y seguirá corriendo, no decidamos sobre 1 solo commit de un trabajo que aún sigue avanzando.»
6/sep (esta conversación): «lo que nos ha pasado es que la sesión intenta un solo acceso y lo declara como inaccesible, necesito que la instrucción invite a sonnet ultracode a intentar por diferentes medios y opciones.»
6/sep (esta conversación): «creo que lo que sigue es el encargo para PDN o una adenda para A4 y que lo intente también.» → se entregan las dos, sobre un solo protocolo.
PARTE I · PROTOCOLO DE RUTAS PDN (común a la adenda y al encargo)

Regla de cierre, y es la que manda. La fila 28 (o cualquiera de sus cuatro sistemas) no puede rotularse NO-OBTENIDO-POR-ESTE-AGENTE hasta que las rutas R0–R7 tengan, cada una, su comando y su salida cruda pegados en la nota, o una línea «no aplica porque …» con la evidencia. Un 000, un 403, un 200 con shell vacío o un «Welcome to nginx» en una ruta es un dato sobre esa ruta, no un veredicto (A.5). Tres hallazgos distintos por ruta, nunca colapsados: RED (000/timeout) · SERVIDOR (4xx/5xx con cuerpo) · VACÍO (200 sin contenido útil: shell React, nginx default, []). Toda sonda declara bytes recibidos y Content-Type (A.13).

Disciplina de red. Todo curl fuera del sandbox de bash (A4 midió 000 dentro / 200 fuera). UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36". --max-time 60. Una petición por segundo, sin paralelismo. Sin credenciales, sin formularios, sin clickwrap (/adquiere §3). Términos del portal: https://plataformadigitalnacional.org/terminos — se abre, se cita una línea en la nota.

R0 · Control positivo, antes de nada
curl -sS -A "$UA" -o /dev/null -w "%{http_code} %{size_download}\n" --max-time 30 https://www.inegi.org.mx/

Reporta los dos valores. Sin 200 aquí ninguna ruta de abajo produce hallazgo: es RED del entorno.

R1 · Backends públicos de la PDN (proxy sin autenticación) — la ruta principal

Hechos leídos del código: el navegador llama a estos backends sin token; las credenciales OAuth de cada estado las guarda el servidor de la PDN (s1_backend/endpoints.json.example, s1_backend/routes/v1.js:213). Las credenciales del Mercado Digital Anticorrupción (SESAEMM etc.) no se necesitan — esta ruta las consume por nosotros. URLs de producción publicadas por la PDN en monitorearSistemas/readme:29-37 y numeralia/APIService_s6.js:16.

S1 · declaraciones

curl -sS -A "$UA" -H "Accept: application/json" https://api.plataformadigitalnacional.org/s1/v1/providers | tee s1-providers.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d)); print([p.get('supplier_id') for p in d])"
curl -sS -A "$UA" -H "Content-Type: application/json" -X POST -d '{"supplier_id":"EDOMEX","page":1,"pageSize":10}' https://api.plataformadigitalnacional.org/s1/v1/search | python3 -m json.tool | head -60

Del segundo comando: pega pagination completo (totalRows, pageSize, hasNextPage, lo que traiga). Luego escala pageSize 10 → 100 → 500 → 1000 con el mismo proveedor y reporta el tope real (el backend no lo fija — routes/v1.js:224 sólo pone 10 por defecto; el tope lo pone cada estado). Después: por cada supplier_id de providers, pagina con query vacío hasta hasNextPage=false o page*pageSize ≥ totalRows; guarda s1/<supplier_id>/p<NNNN>.json. Lista de control de ids: monitorearSistemas/utils/providers_catalog.json (66 entradas el 6/sep — reporta cuántas devuelve providers hoy, no heredes 66). Un proveedor que falla (error.status en el JSON) se anota por proveedor, no tumba S1.

S2 · servidores en contrataciones

curl -sS -A "$UA" -H "Content-Type: application/json" -X POST -d '{}' https://api.plataformadigitalnacional.org/s2/api/v1/suppliers | python3 -m json.tool | head
curl -sS -A "$UA" -H "Content-Type: application/json" -X POST -d '{}' https://api.plataformadigitalnacional.org/s2/api/v1/summary   | python3 -m json.tool | head -80
curl -sS -A "$UA" -H "Content-Type: application/json" -X POST -d '{"supplier_id":"<id>","page":1,"pageSize":100}' https://api.plataformadigitalnacional.org/s2/api/v1/search | python3 -m json.tool | head -40

summary trae totalRows por proveedor (s2_backend/routes/API/v1.js:84; es lo que el monitor oficial usa, numeralia/APIService_s2.js:126-146). Pagina igual que S1. Endpoints extra si search falla: /s2/api/v1/entities, /s2/api/v0/getTotalRows, /s2/api/v0/getInstituciones (s2_backend/routes/API/v0.js).

S6 · contratos (OCDS)

curl -sS -A "$UA" -H "Content-Type: application/json" -X POST -d '{}' "https://api.plataformadigitalnacional.org/s6/api/v1/search?supplier_id=SHCP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('pagination'))"
curl -sS -A "$UA" https://api.plataformadigitalnacional.org/s6/api/v1/summary | python3 -m json.tool | head -40
curl -sS -A "$UA" https://api.plataformadigitalnacional.org/s6/api/v1/buyers  | head -c 800

Tope de pageSize en código: 200 (s6_backend/routes/API/v1.js:193), default 10 (:161). Otros supplier_id de S6: los que liste summary. Registro individual: /s6/api/v1/releases/:ocid y /records/:ocid — sólo para muestreo de control, no para bajar uno por uno.

S3 · sancionados — control del método, no objetivo (ya en corpus como pdn_s3v2)

curl -sS -A "$UA" https://api.plataformadigitalnacional.org/s3-wrapper/api/v1/providers | head -c 1500

El frontend pide /s3-wrapper/api/v1/<endpoint>/<providerId> (pdn/src/components/Sistema3-v2/index.jsx, ${baseUrl}/api/v1/${endpoint}/${providerId}; el nombre de endpoint se lee del mismo archivo). Sirve para verificar que el barrido reproduce lo que mesa bajó a mano: compara conteo por entidad contra los 34 JSON de PDN_S3v2.zip. CONTROL-COINCIDE / CONTROL-DIFIERE (fecha) — se reporta, no se re-registra S3.

R2 · Botón «Descarga todos los datos { JSON }» — el bulk oficial

Existe en las cuatro páginas (pdn/src/components/Compartidos/Descarga.jsx; usado en Sistema1/Busqueda.jsx:600, Sistema2/BuscadorS2v2.jsx:571, Sistema3/*/Buscador*.jsx:103-104, Sistema6/index.jsx:137). Es un href estático inyectado en el bundle desde .env (REACT_APP_S1_BULK, REACT_APP_BULK_S2, _S3_SERVIDORES, _S3_PARTICULARES, _S6). Así llegó PDN_S3v2.zip. Extraer las cinco URLs del bundle:

curl -sS -A "$UA" -c jar.txt -b jar.txt --compressed --max-time 60 https://www.plataformadigitalnacional.org/declaraciones -o shell1.html -w "%{http_code} %{size_download}\n"
sleep 2; curl -sS -A "$UA" -c jar.txt -b jar.txt --compressed https://www.plataformadigitalnacional.org/declaraciones -o shell2.html -w "%{http_code} %{size_download}\n"   # segunda con cookie __zjc
grep -oE '<script[^>]+src="[^"]+"' shell2.html
curl -sS -A "$UA" -b jar.txt --compressed "https://www.plataformadigitalnacional.org/<ruta del main.*.js>" -o main.js -w "%{http_code} %{size_download}\n"
grep -oE 'https?://[^"'"'"' ]+\.(zip|json|gz|tgz|tar|7z|csv)' main.js | sort -u
grep -oE '[a-z0-9.-]*plataformadigitalnacional[a-z0-9./_-]*' main.js | sort -u

Si el shell pesa < 2 KB y no trae <script src= → VACÍO por Zenedge; se reintenta máximo tres variantes, con salida cruda cada una: (a) --http2 + Accept: text/html,application/xhtml+xml + Accept-Language: es-MX; (b) misma petición 5 s después con la cookie del intento anterior; (c) la ruta /static/js/ directa si el shell la nombra. Tres VACÍO → R2 cierra «bundle no accesible sin JS en N intentos» y se pasa a R6, no a NO-OBTENIDO. Con cada URL bulk: curl -sSI + Range: bytes=0-500 → Content-Type, Content-Length; descarga completa; A.7 doble descarga (los bulk pueden llevar marca de generación → hash crudo + hash de contenido); testzip. Control positivo obligatorio: el bulk de S3-servidores contra pdn_s3v2 (sha256 923d0dd0…): COINCIDE / DIFIERE-CON-FECHA.

R3 · Espejo temporal (Wayback) — para el bundle o los bulk si R2 da VACÍO
curl -sS -A "$UA" "https://web.archive.org/cdx/search/cdx?url=plataformadigitalnacional.org/*&filter=mimetype:application/javascript&limit=20&collapse=urlkey"
curl -sS -A "$UA" "https://web.archive.org/cdx/search/cdx?url=*.plataformadigitalnacional.org/*&filter=mimetype:application/zip&limit=20"

Un bundle archivado trae las mismas cinco URLs bulk (cambian rara vez). Reporta RED/SERVIDOR/VACÍO.

R4 · OpenAPI del portal

El frontend enlaza https://www.plataformadigitalnacional.org/oas/ui/ y /validapi/. curl -sS -A "$UA" -o oas.html -w "%{http_code} %{size_download}\n" + grep -oE '"(url|servers)"[^,]{0,120}' oas.html. Puede exponer el servers: real de los backends. Un VACÍO aquí no invalida R1.

R5 · GitHub — siempre alcanzable, para no inventar rutas

PDNMX/api_docs (OAS de S1/S2/S3/S6: nombres de campo y paginación para validar el JSON bajado) · PDNMX/monitorearSistemas (URLs de producción y providers_catalog.json) · PDNMX/pdn (grep -rn "process.env.REACT_APP_S" src descubre cualquier endpoint que este documento no listó). Cita commit leído.

R6 · Navegador en la caja — sólo si R2 y R3 dan VACÍO
which chromium chromium-browser google-chrome; python3 -c "import playwright" 2>&1

Si hay navegador: carga /declaraciones, espera red idle, vuelca document.querySelectorAll('a[href]') y performance.getEntriesByType('resource') → las URLs bulk y las de los backends. Si no hay: pip install playwright --break-system-packages && playwright install chromium cuesta minutos y disco — se declara y se hace, no se salta. Si tampoco: aquí sí nace la receta ≤1 min para mesa: en cada página, clic derecho sobre el ícono de nube bajo «Descarga todos los datos» → «Copiar dirección de enlace» × 5 (S1, S2, S3-servidores, S3-particulares, S6). Esa receta es entregable de R6, no sustituto de R1.

R7 · Hermanas en datos abiertos federales
curl -sS -A "$UA" "https://datos.gob.mx/api/3/action/package_search?q=plataforma+digital+nacional&rows=20" | python3 -c "import sys,json; [print(p['name'], [r.get('url') for r in p.get('resources',[])][:3]) for p in json.load(sys.stdin)['result']['results']]"

Mismo comando con q=declaraciones+patrimoniales y q=contrataciones+abiertas+OCDS. Si el bulk está espejado ahí, es ruta (iv) de /adquiere.

Qué es éxito, por objeto (declarado antes de correr)
Objeto EXISTE-SATISFACE si… Registro
S1 bulk: archivo > 1 MB, JSON/ZIP válido, testzip OK → descargas_mx/PDN-2026-09/S1/ · A.7
S1 barrido: registros bajados = Σ totalRows por proveedor (o lista de proveedores en error, con su error.status) → un .tar.gz por sistema con MANIFIESTO-interno.tsv (fecha, supplier_id, totalRows, bajados, páginas, tope pageSize)
S2 bulk / barrido: ídem → ídem
S6 bulk / barrido: ídem; pagination.total como denominador → ídem
S3: control: COINCIDE/DIFIERE contra pdn_s3v2 → sólo nota; no se re-registra
Resumen: data/pdn-adquisicion-resumen-v1_0.tsv (sistema · ruta que funcionó · objeto · bytes · sha256 crudo · sha256 contenido · fecha) → nuevo

Bulk y barrido son dos payloads distintos del mismo sistema (A.7: identidad = contenido): si ambos llegan, se registran ambos, con nota cruzada. Anti-PR#77: al cerrar, ls -la del corpus compartido, no del worktree.

PARTE II · ADENDA A4 — rutas adicionales para el objetivo PDN (fila 28)

Qué es: información nueva para el ejecutor de A4, archivo nuevo en forense/encargos/2026-09-06-ADENDA-A4-rutas-PDN.md (append, A.3). Qué no es: una edición del COMMIT-1 de A4. No añade objetivos, no cambia criterios de éxito ya congelados: añade rutas (R1–R7) a un objetivo que A4 ya tiene o no tiene.

Instrucción al ejecutor de A4, en una línea: grep -n "PDN\|pdn_s3v2\|fila 28" forense/notas/2026-09-06-MAESTRA38-A4-spec.md → si tu COMMIT-1 incluye la fila 28, aplica la Parte I completa a ese objetivo antes de rotularla, y declara en la nota «ADENDA aplicada»; si no la incluye, no la apliques — escribe «ADENDA no aplica: fila 28 fuera de mi COMMIT-1» y A5 la toma. Cualquiera de las dos es entregable. Nada más de A4 cambia.

Cómo llega a A4 (mesa): se pega este archivo en la sesión de A4 y se commitea en su rama. Si A4 ya cerró la fila 28 antes de recibir la adenda, no se reabre dentro de A4: queda para A5.
```

## PASO 2 · Verificación de aplicabilidad — el comando que la propia adenda pide

```
grep -n "PDN\|pdn_s3v2\|fila 28" forense/notas/2026-09-06-MAESTRA38-A4-spec.md
```

Salida cruda en `forense/notas/2026-09-06-MAESTRA38-A4-resultados.md` §PDN. **Veredicto: SÍ aplica** — el objetivo **#27** del `COMMIT-1` de `A4` es `PDN S1/S2/S6 (bulk)`, fuente `PDN_SESNA_S1_S2_S3_S6`, y el objetivo **#21** es la receta lateral DeclaraNet de la misma fila. La fila 28 **no** estaba cerrada cuando llegó la adenda.

## PASO 3

`ADENDA aplicada`. Ejecución de `R0`–`R7` con comando y salida cruda en `forense/notas/2026-09-06-MAESTRA38-A4-resultados.md`, sección «Objetivo #27 · PDN — ADENDA aplicada (R0–R7)». Alcance respetado: **un objeto dentro del `COMMIT-1` de A4**, no el barrido paginado completo de los cuatro sistemas — eso es `MAESTRA38-A5 · PDN-BULK-Y-PROXY`, que corre en rama propia. Disciplina de red respetada: todo `curl` fuera del sandbox de bash, **una petición por segundo, sin paralelismo**.

## HISTÓRICO-GEN1 — sin marca al cierre de GEN1 (7/sep/2026, PR #597). No se reabre: GEN2 deriva su perímetro de consumidores activos (E.2), no de encargos. Registrado por GEN2-E7 pieza D.
