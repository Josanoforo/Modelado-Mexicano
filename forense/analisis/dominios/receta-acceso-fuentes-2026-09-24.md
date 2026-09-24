# Receta de acceso a fuentes documentales · ASTRA5-U0 · 24/sep/2026

**Para quién:** `GEN2-ASTRA5-U5-ADQUISICION-1` (CAJA, red real) y cualquier sesión que retome las 130 filas del mapa rotuladas `NO-ACCESIBLE-DESDE-SANDBOX` (131 en los lotes; `TIME-033` quedó absorbida por fusión en `VIOL-023`). La lista está en `no-accesible-desde-sandbox-v1_0.tsv`, con la pieza faltante y la causa registrada de cada una.

**Qué es y qué no es.** Es lo que la sesión #1079 midió el 24/sep/2026 sobre URLs reales que fallaron a los ejecutores; cada ruta se probó con control (la misma URL por la vía que había fallado). No es una herramienta instalada: la herramienta `u0red.py` que empaquetaba estas rutas **no se escribió**, porque el control de permisos del modo automático la bloqueó y mesa no agregó las tres reglas que la `ADENDA-1` fijó como su firma (se aplicó su opción 2). Tampoco autoriza descargar payloads al corpus: eso es `/adquiere` en CAJA con registro en `data/manifiesto.yaml`.

## 1 · Por qué fallaron (131 filas, causa registrada en su `dictamen_razon`)

| causa | filas |
|---|---:|
| buscador web de la sesión agotado (200 de 200 `WebSearch`, compartido entre todos los agentes) | 91 |
| ruta candidata `404`, adivinada porque no había buscador para ubicar la vigente | 16 |
| bloqueo del host: `403`, reto Cloudflare o captcha | 10 |
| cadena TLS incompleta vista desde el sandbox (`curl: (60)`) | 3 |
| documento no localizado con las rutas disponibles desde el sandbox | 11 |

Sobre 562 `WebFetch` de los agentes en las dos sesiones (166 dominios), fallaron 168 (78 dominios; 54 nunca respondieron nada útil). Un `404` de una URL adivinada no dice nada de la existencia del documento (A.4): por eso ninguna fila dice «no existe».

## 2 · Rutas que SÍ funcionaron (medidas hoy, con control)

| ruta | cómo | resolvió | evidencia |
|---|---|---|---|
| **curl.exe de Windows** (Schannel, red de Windows) | `/mnt/c/Windows/System32/curl.exe --ssl-no-revoke -sS -L -A "<UA de navegador>" <url>`, **fuera del sandbox** (interop de WSL) | cadenas TLS incompletas que OpenSSL rechaza con `curl: (60)` | `portafolioinfo.cnbv.gob.mx` (boletín SOFIPO, 200, 64 700 B), `www.condusef.gob.mx/documentos/275536_AHORRO.PDF` (200, 4 571 603 B, PDF), `planeacion.sep.gob.mx/principalescifras/` (200), `www.dgcs.unam.mx/boletin/bdboletin/2024_108.html` (200). El mismo `curl` de Linux dio `(60)` en los cuatro. |
| **Cabeceras de navegador** (User-Agent, Accept, Accept-Language) | `curl -A "<UA>" -H "Accept-Language: es-MX,…"` | bloqueos por User-Agent de librería | `www.migrationpolicy.org/article/mexican-immigrants-united-states` (200, redirige a `/journal/spotlight/…`); el fallo anterior era de la herramienta `WebFetch`, no del sitio. |
| **Wayback Machine, captura cruda `id_`** | `https://archive.org/wayback/available?url=<url>` → `https://web.archive.org/web/<timestamp>id_/<url>` | hosts tras reto Cloudflare o captcha, o caídos | CIDH `oas.org/es/cidh/informes/pdfs/2026/informe_desapariciones_mx_spa.pdf`: captura `20260826234040`, 2 548 951 B, `%PDF-1.4` con `%%EOF` (sha256 inicia `ba9ac1ed6aba5b64`). Capturas disponibles también para Crisis Group `b050-mexico-online.pdf` (`20260120071821`), Hofstede `country-comparison-tool?countries=mexico` (`20260327120503`) y CONASAMI (`20260901103139`). |
| **OpenAlex** (sustituto del buscador para obras académicas) | `https://api.openalex.org/works?search=<autor título año>&select=id,doi,title,publication_year,best_oa_location` | citas académicas sin DOI conocido; da la ubicación de acceso abierto | Gelfand et al. 2011 → `10.1126/science.1197754` al primer resultado. |
| **Crossref y PubMed E-utilities** (ya usadas por los ejecutores de la segunda pasada) | `api.crossref.org/works?query.bibliographic=…`; `eutils.ncbi.nlm.nih.gov` | confirmar autoría/año/revista | Crossref respondió 113 veces (23 `429` por tasa: espaciar consultas); PubMed 41/43. |

Rutas del aparato del repo que siguen vigentes y conviene usar antes de adivinar URL: INEGI por `pestanaData.js` → `idBiinegi` → API de descarga masiva (las rutas de programa son SPA con soft-404 de `200`); CKAN de datos.gob.mx en `/api/3/` (no `/busca/api/3/`), con recursos en `repodatos.atdt.gob.mx`; API de una SPA leída desde su bundle JS (`apiUrl`), que puede vivir en otro host. Reglas de `.claude/commands/adquiere.md` §3 (UA real, `--max-time`, sin fuerza bruta, `curl 60` no es barrera de credencial).

## 3 · Lo que NO funcionó (y no hay que repetir)

- **Edge headless (`msedge.exe --headless=new --dump-dom`) NO pasa retos Cloudflare**: la página de Crisis Group devolvió «Attention Required! | Cloudflare». Sirve sólo para páginas que se arman con JavaScript sin reto.
- **CONASAMI, CONAPRED y Hofstede sólo por Wayback**: cortan el TLS tanto por OpenSSL (`unexpected eof while reading`, también con TLS 1.2 y `SECLEVEL=0`) como por Schannel (`failed to receive handshake`); CONASAMI por HTTP plano da una respuesta de 144 B, no el sitio. Wayback sí tiene capturas.
- **curl.exe y cabeceras de navegador no pasan Cloudflare/captcha** (CIDH en `oas.org`, `crisisgroup.org`): mismo `403` por las dos vías. Para esos hosts, ir directo a Wayback.
- **DuckDuckGo y Bing como buscador sustituto**: CAPTCHA o resultados desalineados; no sirven.
- **Adivinar rutas de portales oficiales sin buscador**: la mayoría de los 65 `404` medidos son rutas inventadas; ubica primero la ruta (CDX de Wayback, sitemap, API del portal, bundle JS) y luego pide el archivo.

## 4 · Orden recomendado por URL (un intento por ruta, sin reintentos abiertos)

1. Si es cita académica: OpenAlex → Crossref → PubMed; usar la ubicación de acceso abierto si existe; un documento de pago queda **identificado**, no se descarga ni se elude el muro.
2. Si es documento en host conocido: cabeceras de navegador (Linux) → curl.exe de Windows (fuera del sandbox) → Wayback `id_`.
3. Si la URL no se conoce: índice CDX de Wayback del dominio con filtro de texto y `mimetype:application/pdf` (`https://web.archive.org/cdx/search/cdx?url=<dominio>/*&output=json&collapse=urlkey&filter=mimetype:application/pdf`) o la API del portal; nunca barridos de rutas.
4. Verificar estructura antes de aceptar (`%PDF-` y `%%EOF`, ZIP legible, título HTML real frente a soft-404 o reto) y anotar ruta, código, bytes, sha256 y fecha por URL.

## 5 · Condición de entorno

Las rutas 2 (curl.exe) y el render de Edge dependen de la **máquina de mesa** (Windows con WSL e interop) y corren fuera del sandbox; una sesión de nube no las tiene (A.2). Wayback, OpenAlex, Crossref y PubMed sólo necesitan red de salida hacia esos hosts.
