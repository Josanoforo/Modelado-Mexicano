# GEN2-38 · investigación ADQ · 2026-09-26

Entorno CAJA confirmado antes de caminar filas: `/home/pc0/mm-adq`,
`data/raw -> /home/pc0/mm-corpus/raw`, WSL2 y `https://www.inegi.org.mx/`
respondió HTTP 200. El selector canónico devolvió cero objetos de adquisición.

## DEM-AHORRO-STOCK-DURACION-01

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`.

- Búsqueda web real, CONSTRUCTO/HERMANAS/LATERAL: `México encuesta ahorro
  duración meses ahorros emergencia cuestionario universidad`,
  `site:mx "cuánto tiempo" ahorros encuesta hogares México`,
  `site:edu.mx encuesta financiera ahorro duración stock ahorros cuestionario`
  y `México encuesta capacidades financieras ahorros cubrir gastos meses`.
- El buscador devolvió ENIF 2024, ENSAFI 2023, EACF/Banxico, ENFIH e IIEG.
  Son familias ya examinadas por la investigación previa. ENSAFI condiciona
  la duración a quienes declaran ahorro; ENIF/EACF mantiene la categoría
  mezclada que motivó la necesidad. No apareció un instrumento nuevo que
  observe en campos separados ausencia/tenencia y duración del mismo stock.
- No se descargó ni reencoló ninguna candidata repetida.

Estado: `continua`. Frontera: catálogos variable-por-variable de encuestas
financieras de universidades estatales distintas de IIEG y archivos históricos
no indexados de CNBV/CONDUSEF. Cursor: buscar sólo instrumentos probabilísticos
de personas adultas que separen ausencia/tenencia y meses o días del mismo
stock. Alternativa concreta para mesa, tras más de dos ciclos sin avance:
mantener el bloqueo, relabel del uso acotado ya autorizado por #772, o aprobar
un proxy nuevo con alcance explícito; esta caminata no decide entre ellas.

## NC-0202

Versión: `2026-09-15-ennvih-diseno-publico-v1`.

- Búsqueda web real, LATERAL/HERMANAS: `"Berumen" 2007 Mexican Family Life
  Survey sample design pdf`, `"Mexican Family Life Survey" "primary sampling
  unit" strata weights`, `site:icpsr.umich.edu 118971 "Mexican Family Life
  Survey" documentation` y `site:ennvih-mxfls.org "sample design"`.
- La búsqueda localizó `usersguidev2.pdf` y `usersguidemxfls-3.pdf`, que citan
  a Berumen (2007), además de IHSN 7063 y el resumen UCLA ya adquiridos. Las
  guías oficiales ya formaban parte del universo agotado y no publican campos
  ejecutables de UPM/estrato ni réplicas. Resultados académicos secundarios
  describen el diseño, pero tampoco entregan llaves por observación.
- No se repitieron las guías, IHSN ni el PDF UCLA.

Estado: `continua`. Frontera: copia pública independiente de Berumen (2007),
adjunto INEGI (2004) Sample Design o archivo oficial con UPM/estrato/réplicas.
Cursor: continuar sólo por documento o variables ejecutables; la alternativa
humana sigue siendo NC-0156, sin imputar conglomerados.

## NC-0258

Versión: `AUTO-NC-v1-11a62e37243a`.

- Búsqueda web real, CONSTRUCTO/HERMANAS/LATERAL: `site:inegi.org.mx/rnm
  ENAPROCE 2015 diccionario datos descriptor archivos`,
  `site:inegi.org.mx/rnm ENAPROCE 2018 diccionario datos`, `ENAPROCE 2015
  descriptor de archivos FD cuestionario variables` y `ENAPROCE 2018
  descriptor archivos microdatos`.
- La búsqueda oficial ubicó RNM catálogo 330 y la página del programa. A.8
  encontró que el corpus ya contiene `inegi_rnm_catalog_330_enaproce2015` y
  los tres cuestionarios oficiales 2015 con ids
  `inegi_rnm_330_download_19206_enaproce2015_pyme_comserv`,
  `inegi_rnm_330_download_19207_enaproce2015_pyme_manufac` e
  `inegi_rnm_330_download_19208_enaproce2015_micro`. Los archivos existen en
  `/home/pc0/mm-corpus/raw` y el HTML enlaza el diccionario de datos.
- No se descargó el objeto duplicado. Esta evidencia cubre una de las 55
  familias (`enaproce2015`) en la dimensión documental y permite un cableado
  posterior al extractor; no es microdato, no cubre ENAPROCE 2018 ni las otras
  54 familias, y la unidad es empresa, no persona.

Estado: `evidencia_existente`. Frontera: las restantes familias
`REQUIERE-FD-EN-CORPUS`, empezando por `enaproce2018`, y el cableado explícito
del cuestionario ENAPROCE 2015 a las variables de la base ciega. Cursor:
añadir los tres cuestionarios ya manifestados a la tabla de fuentes del
extractor sin volver a descargarlos; después buscar el descriptor 2018.
