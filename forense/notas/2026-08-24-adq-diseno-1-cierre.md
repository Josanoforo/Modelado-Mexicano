# Nota de acto · ADQ-DISENO-1 — «no está descargado, la descargamos y ya»

**Fecha:** 24/ago/2026 · **Entorno:** UBUNTU (corpus + red) · **SHA base:** `5bef289` (origin/main, SELLA-AGO24-D fusionado) · **Rama:** `adq-diseno-1`

## ARRANQUE

1. Repo: worktree existente reutilizado en `/home/pc0/mm-adq-diseno-1`.
2. SHA base verificado: `git log origin/main -1` → `5bef289 Merge pull request #319` (SELLA-AGO24-D fusionado en `0505b01`, confirmado por commit previo en la misma cadena).
3. `data/raw` symlinkeado a `/home/pc0/mm-corpus/raw` (no existía en el worktree nuevo).
4. Sonda entorno (A.2): `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `200`. `ls data/raw | head -1` → `2005trim1_csv.zip` (no vacío). Variable esperada `sin_variable` confirmada.
5. Espejo: no tocado.

## Tabla resumen

| Objeto | URL | Veredicto A.4 | id manifiesto |
|---|---|---|---|
| T1 · ENNViH/MxFLS calculo-de-factores | http://ennvih-mxfls.org/assets/calculo-de-factores-de-expansion.pdf | EXISTE-NO-SATISFACE (ya registrado desde 30/jul/2026, confirma FP-118) | `ennvih3_2009_factores_exp` (preexistente) |
| T1 · ENNViH/MxFLS nota de muestra | http://ennvih-mxfls.org/assets/ennvih-1_muestra.pdf | EXISTE-NO-SATISFACE (nuevo, misma limitación) | `ennvih1_muestra_diseno` |
| T2 · ENPOL 2021 diseño muestral | (sin URL real — sin barrer, ver detalle) | EXISTE-NO-SATISFACE | — |
| T3 · ENSAFI 2023 FD | https://www.inegi.org.mx/contenidos/programas/ensafi/2023/microdatos/ensafi_2023_fd.xlsx | NO-ENCONTRADO | — |
| T3 · ENSU 2025 FD | https://www.inegi.org.mx/contenidos/programas/ensu/2025/microdatos/ensu_2025_fd.xlsx | NO-ENCONTRADO | — |
| T4 · ENOE post-2019, 28 olas vía /microdatos/ | https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/... | EXISTE-SATISFACE (28/28) | `enoe_YYYYtrimN_microdatos` (ver detalle) |

## T1 · ENNViH/MxFLS — identificadores de diseño

Barrido: `https://ennvih-mxfls.org/sitemap.xml` (200, 314 URLs únicas) + `robots.txt` (200, no excluye nada relevante). El sitemap es el índice completo declarado por el propio sitio — no hay `/assets/` sin listar ahí (no se navegó por adivinanza).

Filtro por patrón `upm|conglomer|estrato|muestr|design|factor|weight|ponder|sample|codebook|manual` sobre las 314 URLs → 6 candidatas:
- `assets/calculo-de-factores-de-expansion.pdf` — **ya en corpus** desde 2026-07-30 (`ennvih3_2009_factores_exp`), registrado entonces para CAL-G3/Nota 7, no para FP-118. Contiene fórmulas completas con UPM, estrato, USM, región (`nrh`, `Vrhi`, factor de expansión corregido por no respuesta).
- `assets/ennvih-1_muestra.pdf` y `assets/ennvih-1_muestra2.pdf` — **byte-idénticos** (md5 `50bf8a9ec6e649975d341fbed43538fa`), ambos apuntan al mismo PDF servido dos veces. Descargado y registrado como `ennvih1_muestra_diseno`. Contiene el diseño muestral completo: "polietápico, estratificado y por conglomerados"; UPM's clasificadas en 3 estratos (alto/medio/bajo); fórmulas con UPM/estrato/entidad/región, tablas "UPM SELECCIONADAS".
- `ponderadores1.html`, `ponderadores2.html`, `ponderadores3.html` — páginas HTML descriptivas, no bajadas (no aportan campo nuevo sobre lo ya extraído de los dos PDF; declarado, no registrado).

**Re-lectura de ambos PDF buscando específicamente NOMBRE DE CAMPO (no solo notación matemática, que FP-118 ya sabía que existía):** se buscó en el texto extraído de `ennvih-1_muestra.pdf` cualquier token con forma de nombre de columna (`upm[0-9_]`, `est_upm`, `id_upm`, `clave_upm`, `folio`) — cero aciertos. Las únicas ocurrencias de "NOMBRE" en el documento son de una tabla "DISTRIBUCIÓN DE LA MUESTRA POR DOMINIO Y REGIÓN" con nombres de región (SUR-SURESTE, etc.), no nombres de columna de microdato. Igual que `calculo-de-factores-de-expansion.pdf` (ya registrado desde el 30/jul), el documento define UPM/estrato/USM como símbolos matemáticos (`nrh`, `Vrhi`) para la fórmula del factor de expansión, sin mapearlos a un nombre de campo del `.dta`.

**Veredicto:** EXISTE-NO-SATISFACE (ambos documentos, el preexistente y el nuevo). Confirma exactamente lo que FP-118 ya tenía escrito: "el método está documentado ... en notación matemática, sin nombre de campo". El barrido completo del sitemap (314 URLs) no encontró un tercer documento que sí traiga el nombre de campo — no hay apéndice de datos, guía de usuario ni codebook adicional bajo `ennvih-mxfls.org`. Se registra el segundo PDF (`ennvih1_muestra_diseno`) porque documenta el diseño estadístico completo y es evidencia nueva sobre la fila, aun sin resolverla.

No se navegó el "repositorio académico espejo" (ICPSR/otro) — el sitemap propio (314 URLs, universo completo declarado por el sitio) ya se agotó y no lo tiene; declarado como universo no barrido si CAL-G3 quiere intentar una segunda fuente independiente (fuera de alcance de este acto, que solo agota `ennvih-mxfls.org`).

## T2 · ENPOL 2021 — documento de diseño muestral

- FD en corpus: `data/raw/enpol2021/fd_enpol2021.pdf` — sin UPM (confirmado previamente por dirección).
- Página del programa `https://www.inegi.org.mx/programas/enpol/2021/` → HTML de 4273 bytes, cascarón SPA sin enlaces navegables por curl (JS-driven, sin `<a href>` reales en el HTML servido).
- Intentos de rutas derivadas por patrón (control positivo: mismo patrón SÍ funciona para ENASIC 2022, confirmado — 266488 bytes, `.xlsx` real):
  - `.../enpol/2021/doc/enpol2021_diseno_muestral.pdf` → HTTP 200 pero 2263 bytes, `file` = HTML (cascarón "soft-404" de INEGI).
  - `.../enpol/2021/doc/enpol2021_nota_tecnica.pdf` → idéntico cascarón (byte-a-byte, `diff` vacío).
  - `.../enpol/2021/microdatos/documentacion/enpol2021_diseno_muestral.pdf` → mismo cascarón, 2263 bytes.
  - `.../enpol/2021/microdatos/enpol2021_fd.zip` → mismo cascarón, 2263 bytes.
  - RNM `catalog/670` (adivinado) → resolvió a un dataset distinto ("Censo Nacional de Poderes Legislativos Estatales 2020"), no ENPOL.
  - Buscador RNM (`catalog/search?q=ENPOL+2021`) → devolvió resultados no relacionados (boletines recientes de balanza comercial/confianza del consumidor), el buscador no parece indexar por texto libre como se esperaba.
  - Biblioteca INEGI (`app/biblioteca/buscador.html`, `app/api/biblioteca/busqueda`) → 404 en el endpoint API; la página de buscador HTML no trae resultados navegables por curl.
- **Total de intentos:** 9 URLs/endpoints distintos probados, todos sin devolver documentación de diseño muestral nueva.

**Veredicto:** EXISTE-NO-SATISFACE. Cita exacta: el FD en corpus (`fd_enpol2021.pdf`) no trae UPM (confirmado); la página del programa es una SPA sin API pública descubierta desde este barrido, y las 6 rutas derivadas por patrón (que sí funcionan para ENASIC) devuelven el cascarón "soft-404" característico de INEGI (2263 bytes, HTML). No se descarta que exista bajo una ruta o nombre distinto no cubierto por este barrido — se declara como pendiente de un barrido con renderizado JS (fuera del alcance de curl), no como "no existe".

## T3 · FDs de ENSAFI 2023 y ENSU 2025

Ambas URLs candidatas (`ensafi_2023_fd.xlsx`, `ensu_2025_fd.xlsx`) devuelven el mismo cascarón "soft-404" (2263 bytes, HTML) que en T2. Control positivo: el mismo patrón de ruta (`.../<programa>/<año>/microdatos/<programa>_<año>_fd.xlsx`) SÍ resuelve para ENASIC 2022 y ENFIH 2019 (confirmado por dirección en la verificación de existencia).

Barrido de años vecinos para descartar error de año exacto: `ensafi` 2020-2024 y `ensu` 2020-2024 (10 URLs adicionales) → los 10 devuelven el mismo cascarón de 2263 bytes.

**Total de intentos:** 12 URLs (2 exactas del encargo + 10 de barrido de año).

**Veredicto:** NO-ENCONTRADO (ambos). Universo examinado: 12 URLs bajo el patrón que funciona para ENASIC/ENFIH, ningún año 2020-2024 resuelve para ninguno de los dos programas bajo ese nombre de archivo. No se navegaron las páginas de programa (mismo problema SPA que en T2).

**Receta A.5 (un minuto, para clic manual de mesa si hace falta):**
1. Ir a `https://www.inegi.org.mx/programas/ensafi/2023/` (o `ensu/2025/`) en un navegador con JS.
2. Click en pestaña "Microdatos".
3. Buscar el archivo con extensión `.xlsx` etiquetado "Descriptor de la base de datos" o "Diccionario de datos" (FD).
4. Si no aparece: el programa puede no tener aún microdatos publicados para ese año (ENSU 2025 podría estar en curso; ENSAFI es programa relativamente nuevo).

## T4 · ENOE post-2019 vía /microdatos/ (FP-110-b)

Se re-adquirieron las 28 olas trimestrales 2019T1–2026T1 (con el hueco real de 2020T2, ENOE suspendida por confinamiento COVID y sustituida por ENOEN telefónica ese trimestre — no es un error del barrido) desde `https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/...`, confirmando primero con un control positivo (`enoe_2023_trim1_csv.zip`, 37 487 716 bytes, zip real) que la ruta funciona, luego derivando la lista completa de 28 nombres reales desde `data/indice-descarga-masiva-2026-08-05.tsv` (que ya tenía las URLs correctas indexadas — no hubo que adivinar nombres) en vez de adivinar la convención (que cambia de `AAAAtrimN_csv.zip` a `enoe_AAAA_trimN_csv.zip` a `enoe_n_AAAA_trimN_csv.zip` según el año, sin patrón único).

IDs registrados con sufijo `_microdatos` (ver detalle abajo), sin sobreescribir las 20 entradas `enoe_AAAA_Nt_csv` preexistentes (vía `/datosabiertos/`) — ambas quedan en el manifiesto como historia paralela.

(Detalle de los 28 ids, tamaños y sha256: ver `data/manifiesto.yaml`, prefijo `enoe_` sufijo `_microdatos`, y el bloque de verificación más abajo en esta nota.)
