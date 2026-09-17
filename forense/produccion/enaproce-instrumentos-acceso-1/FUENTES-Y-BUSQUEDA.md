# Fuentes, adquisición y búsqueda negativa

## Estado de cada pieza

Los catálogos RNM 330/518 ya estaban descargados y acreditados en el
manifiesto. Se releyeron desde el corpus local antes de consultar la red. Sus
pestañas oficiales de materiales y diccionario permitieron descubrir los seis
cuestionarios siguientes. Todos fueron descargados, validados como PDF real,
leídos con extracción de texto y revisados visualmente en el módulo XII.

| ID nuevo | Ola/instrumento | URL oficial | Bytes | SHA-256 | Estado de lectura |
|---|---|---|---:|---|---|
| `inegi_rnm_330_download_19206_enaproce2015_pyme_comserv` | 2015 PyME comercio/servicios | https://www.inegi.org.mx/rnm/index.php/catalog/330/download/19206 | 204944 | `ba3c7a8f60378c17e0e72701024a0e49bbad1e1a821f46833ac91f647659b325` | PDF 40 pp.; módulo XII pp. 35–37 leído y visto |
| `inegi_rnm_330_download_19207_enaproce2015_pyme_manufac` | 2015 PyME manufactura | https://www.inegi.org.mx/rnm/index.php/catalog/330/download/19207 | 299948 | `b0223e7acc8f838a8db24571a754eb0b83ac18a34c7726aca4a4a043043272a3` | PDF 40 pp.; módulo XII pp. 35–37 leído; pp. 35/37 vistas y texto contrastado |
| `inegi_rnm_330_download_19208_enaproce2015_micro` | 2015 micro | https://www.inegi.org.mx/rnm/index.php/catalog/330/download/19208 | 287157 | `69892f70f3ebe398e3b8c12d85c7bfe566de2cb36c71dc9f3be8578532abe0ef` | PDF 32 pp.; módulo XII pp. 27–29 leído y visto |
| `inegi_rnm_518_download_19215_enaproce2018_pyme_comserv` | 2018 PyME comercio/servicios | https://www.inegi.org.mx/rnm/index.php/catalog/518/download/19215 | 297112 | `e365b7467cfd22b43dd131a7e9e5508cedc64bc51bcff73cdc6e882af538caa1` | PDF 44 pp.; módulo XII pp. 39–41 leído y visto |
| `inegi_rnm_518_download_19216_enaproce2018_pyme_manufac` | 2018 PyME manufactura | https://www.inegi.org.mx/rnm/index.php/catalog/518/download/19216 | 296370 | `7d9a1ebd44583e3c1c339dc76436b22ef146895bd1bb3939b68a757ea04c31a5` | PDF 44 pp.; módulo XII pp. 39–41 leído; pp. 39/41 vistas y texto contrastado |
| `inegi_rnm_518_download_19217_enaproce2018_micro` | 2018 micro | https://www.inegi.org.mx/rnm/index.php/catalog/518/download/19217 | 281506 | `f41e487030b814012038bb509ba192f566fd3c9da7d1264c6c37fe6c20b0679d` | PDF 34 pp.; módulo XII pp. 29–31 leído y visto |

Fecha de descarga: 2026-09-16 (America/Mexico_City). Ruta lógica común:
`data/raw/ENAPROCE_instrumentos/`. No se registra ninguna ruta física privada.

También se leyeron en línea las cuatro tablas de diccionario ya enlazadas por
los catálogos: 2015 `F19`/`F20` y 2018 `F1`/`F2`, y las páginas individuales de
las variables contratadas. Esas páginas se usaron como metadatos navegables;
no se incorporaron como nuevos payloads ni consumieron el cupo de seis PDF.

`inegi_rnm_518_download_19219` siguió identificado como informe final de
levantamiento; no se volvió a presentar como descriptor ni base y no fue
necesario abrirlo. No se abrieron los enlaces de indicadores de calidad,
tabulados, resultados, bases reales ni bases de ejemplo cegadas.

## Búsqueda negativa acotada

Universo examinado: seis cuestionarios completos por extracción textual, los
módulos XII por inspección visual y cuatro diccionarios RNM con sus variables
del módulo. Términos: `trámite`, `trámites gubernamentales`, `inspección`,
`corrupción`, `pago informal`, `mordida`, `soborno`, `solicitud de pago`,
`obstáculo`, `regulación`, `permiso`, `licencia` y las expresiones efectivamente
usadas `obligaciones fiscales federales`, `tiempo y recursos` y `horas`.

Resultado: se localizaron trámites, permisos, licencias, obstáculo, gasto
formal y horas. `Inspección` sólo aparece fuera del desenlace objetivo (por
ejemplo, aviso legal o definiciones ajenas). No se localizó en los módulos ni
diccionarios un reactivo de solicitud/insinuación/pago informal, mordida,
soborno o corrupción. El rótulo correcto es
**NO-ENCONTRADO-EN-LO-REVISADO**, no una afirmación de inexistencia mundial.

No hubo exposición incidental a distribuciones del objetivo: se leyeron
instrumentos y metadatos, no respuestas ni tabulados. Las cifras de muestra de
los catálogos describen diseño/campo, no resultados de las variables R03.
