# PAQUETE-RECETAS-5 — 2026-09-04

Producido por `ACTO MAESTRA38-N4 · PROPAGA-Y-PAGA` (FP-286) sobre las 12 filas `MESA-DECIDE` de `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2. A diferencia de `PAQUETE-RECETAS-3` (las 6 `BAJAR` del mismo informe, receta directa y limpia), aquí van las recetas que el propio informe documentó **dentro** de una recomendación `MESA-DECIDE` — cada una es una de las dos opciones con costo que la fila trae, no un `BAJAR` puro: ejecutarla no cierra la necesidad de modelo que originó la fila, y en dos casos (17, 28) la fila ya está `OBTENIDO-PARCIAL`, así que la receta completa una parte, no el todo.

**Discrepancia declarada contra el encargo (D-13, re-derivar no heredar de prosa).** El encargo de este acto citaba «11 recetas → PENDIENTE-DE-MESA; PAQUETE-RECETAS-5 consolidado (11 + ICPSR + WB + PDN)». Releído el informe fila por fila (las 12 `MESA-DECIDE`: 5, 6, 7, 8, 9, 10, 11, 12, 17, 25, 27, 28), solo **6** traen una receta de navegador concreta y verificada dentro de su propio texto — filas 9, 12, 17, 25, 27 y 28. Las otras 6 `MESA-DECIDE` (5, 6, 7, 8, 10, 11) ofrecen únicamente vías institucionales (correo, formulario, convenio, cotización) sin URL de descarga: no calzan con el estándar «receta ≤1 minuto» y este acto no las fuerza a serlo. De las 6 con receta real, `WB` (fila 12, `ENAFIN`, hermana World Bank Enterprise Surveys) y `PDN` (fila 28, `PDN_SESNA_S1_S2_S3_S6`, nota lateral DeclaraNet) sí calzan con los rótulos que el encargo nombraba; `ICPSR` no — ninguna de las 28 filas del informe rindió un candidato ICPSR con receta verificable (aparece solo como universo de búsqueda sin resultado en varias filas: 1, 6, 7, 9, 12). Este documento consolida las 6 reales, no 11.

De las 6, solo 4 mueven `estado_A4A5` a `PENDIENTE-DE-MESA` (filas 9, 12, 25, 27 — hoy sin nada adquirido); las otras 2 (17, 28) quedan `OBTENIDO-PARCIAL` sin cambio de estado porque ya tienen un payload parcial en el corpus y la receta de abajo solo trae una pieza más, no el cierre de la fila — ver `data/curacion-registro/cola-adquisicion-registro.tsv` (nota de cada fila, columna `nota`, escrita vía `tsv_crudo.upsert_fila`).

Ninguna receta de abajo, ejecutada, cierra por sí sola la necesidad de modelo que originó la fila — eso lo dice el propio informe fila por fila; ver el detalle completo en `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2.

---

## Tablero

| # (=fila del informe) | fuente_canonica | estado_A4A5 tras este acto | qué trae |
|---:|---|---|---|
| 9 | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | PENDIENTE-DE-MESA | receta abajo (hermana MILK RCT) |
| 12 | `ENAFIN` | PENDIENTE-DE-MESA | receta abajo (hermana WB Enterprise Surveys) |
| 17 | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | OBTENIDO-PARCIAL (sin cambio) | receta abajo (CSV histórico CompraNet) |
| 25 | `IEEPCO_OAXACA_SERIE_MUNICIPAL` | PENDIENTE-DE-MESA | receta abajo (pata 2016) |
| 27 | `INEGI_CNGF` | PENDIENTE-DE-MESA | receta abajo (3 documentos verificados) |
| 28 | `PDN_SESNA_S1_S2_S3_S6` | OBTENIDO-PARCIAL (sin cambio) | receta abajo (DeclaraNet, solo S1 federal) |

---

## 9. `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` — Opción A de §2.9

Receta ejecutable en ≤1 minuto, verbatim (verificada hoy 3/sep/2026 por HEAD, sin reto Cloudflare en este host): abrir en el navegador `https://media.milliman.com/v1/media/edge/images/millimaninc5660-milliman6442-prod27d5-0001/media/Milliman/PDFs/Microinsurance/MILK-RCT--Study-of-Life-MI-Purchasing-Decisions-in-Mexico.pdf`, Ctrl+S / Guardar como `MILK-RCT--Study-of-Life-MI-Purchasing-Decisions-in-Mexico.pdf` (HTTP/2 200, `content-type: application/pdf`, `content-length: 1 111 333` B). Es la hermana MILK RCT (Zimmerman/Bauchet/Magnoni/Poulton 2014, mismos ~8,700 clientes de Compartamos Banco) del objeto exacto de la fila (Bauchet, SSRN 2474620, bloqueado por Cloudflare/403 hoy en `papers.ssrn.com`, reconfirmado). Nota para quien ejecute: NO satisface R1.4 (sin comparador de marca/sustituto) — es evidencia complementaria de elasticidad-precio y framing, no cierre de la necesidad; darla de alta como hermana en `aliases-fuentes.tsv` exige firma de mesa (A.7), fuera del perímetro de este acto.

---

## 12. `ENAFIN` — Opción A de §2.12

Receta: registro gratuito en `https://www.enterprisesurveys.org/en/data` (World Bank Enterprise Surveys — México 2023, `microdata.worldbank.org/index.php/catalog/6453`), aceptar términos de citación, descargar el microdato. Costo real: minutos, no un solo clic (exige registro), pero sin trámite institucional ni viaje. Nota para quien ejecute: cobertura PARCIAL e incierta — el WebFetch a la ficha de estudio no confirmó si trae la pregunta puntual «motivo de rechazo = sin historial crediticio» que N19 pide; revisar el cuestionario/diccionario completo (`pdf-documentation` del catálogo 6453) antes de dar por cerrado nada. Los tabulados de ENAFIN ya en el corpus (`adq15_enafin_conjunto_de_datos_enafin_2024_csv`) NO traen el cruce tamaño×sector×motivo-de-rechazo que N19 exige — esta hermana es la única vía identificada hoy que podría traerlo, sin confirmar.

---

## 17. `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` — Opción 1 de §2.17

Receta ejecutable en ≤1 minuto: abrir `https://www.datos.gob.mx/dataset/contratos_expedientes_sistema_historico_compranet`, clic en el recurso listado con formato CSV («compranet_historico.csv»), botón de descarga (verificado hoy: `HEAD` con `Range 0-500` → HTTP 206, `Content-Range` total 951 619 345 B, `Last-Modified` 2025-07-03). Nota para quien ejecute: ~951 MB — amplía la ventana temporal de contrato/procedimiento/proveedor pero NO añade persona-con-id ni sanción, que es el hueco decisivo que la fila ya tiene identificado (veredicto `EXISTE-NO-SATISFACE` sobre `CompraNet5`, `forense/notas/2026-09-03-MAESTRA36-A2-P1-P3-compranet-llaves.md`) — solo `PDN` S1/S2 cerraría eso, y esos dos sistemas siguen sin URL de descarga masiva pública (ver fila 28 abajo).

---

## 25. `IEEPCO_OAXACA_SERIE_MUNICIPAL` — Opción A de §2.25

Receta YA escrita por `ACTO MAESTRA35-L3` (2026-09-02), re-verificada vigente hoy: abrir `https://www.ieepco.org.mx/archivos/elecciones-2016/ESTAD%C3%8DSTICA%20CONCEJALES%20%202016.xlsx` en el navegador (resuelve la cadena TLS incompleta sin intervención manual, a diferencia de `curl`/`requests`) y Guardar como `ESTADISTICA_CONCEJALES_2016_IEEPCO.xlsx` (968 301 B). Nota para quien ejecute: solo cubre 2016 (25 hojas D01..D25, régimen de partidos); 2018/2021/2024 solo existen por consulta-por-municipio en el portal (sin archivo bulk). `R7.1` ya está archivada con veredicto A (`ADR-145`) usando otra evidencia — esta receta es cobertura futura, no reabre nada.

---

## 27. `INEGI_CNGF` — Opción A de §2.27

Tres archivos, cada uno verificado hoy con `curl` (200, tamaño real, no soft-404 — el soft-404 de INEGI da 200/2263B, estos son sustancialmente mayores): (1) `https://www.inegi.org.mx/contenidos/programas/cngf/2025/doc/cngf_2025_m1s1.pdf` (2 014 714 B). (2) `https://www.inegi.org.mx/contenidos/programas/cngf/2025/doc/ec_cngf2025.xlsx` (marco conceptual, 195 845 B). (3) `https://www.inegi.org.mx/contenidos/programas/cngf/2025/doc/cngf_2025_resultados.pdf` (1 075 400 B). Abrir cada URL en el navegador y Guardar como. Alternativa (requiere JS, no verificable byte a byte desde esta caja): `https://www.inegi.org.mx/programas/cngf/2025/` → pestaña «Datos abiertos» → CSV/ZIP de Administración Pública Federal. Nota para quien ejecute: 0 necesidades de `relaciones.tsv` citan esta fuente hoy (confirmado con grep) — es cobertura de contexto (oferta institucional agregada de trámites), no cierre de una regla viva.

---

## 28. `PDN_SESNA_S1_S2_S3_S6` — nota lateral de §2.28 (no la Opción A del informe, que exige navegación manual de 3 secciones sin receta de 1 minuto)

Receta ejecutable en ≤1 minuto, verificada hoy por `HEAD`: descargar `.../11_datos_abiertos_declaranet_2018.csv` desde el catálogo CKAN de `datos.gob.mx`/`repodatos.atdt.gob.mx`, dataset «listado_declaraciones_situacion_patrimonial» (200, `content-type: text/csv`, `content-length: 45 284 941` B, `last-modified: 16/oct/2025`; seis recursos, uno por año 2013-2018). Nota para quien ejecute: cubre SOLO Poder Ejecutivo Federal y SOLO 2013-2018 — no sustituye a PDN-S1 (cobertura subnacional 2019+) ni toca S2/S3/S6. La vía completa (Opción A del informe: navegar `plataformadigitalnacional.org` con un navegador real, como mesa ya hizo para S3) sigue siendo la única que cerraría S1/S2/S6 de verdad, pero no calza con el estándar de receta ≤1 minuto de este paquete.

---

## Contador

Payloads `OBTENIDO` antes de este acto → después: **sin cambio** (0) — este acto no descarga (perímetro explícito del encargo: "cola + vista", no `data/raw`); las 6 recetas de arriba son candidatas para que mesa/un acto de adquisición ejecute. Recetas consolidadas: **6**, no las 11 que el encargo citaba (ver discrepancia declarada arriba). Filas promovidas a `PENDIENTE-DE-MESA`: **4** (9, 12, 25, 27).
