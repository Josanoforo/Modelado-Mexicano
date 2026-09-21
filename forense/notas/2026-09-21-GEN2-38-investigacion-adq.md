# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-21. Entorno: CAJA/WSL2. Antes de caminar, `data/raw`
resolvió a `/home/pc0/mm-corpus/raw`, el clon fue `/home/pc0/mm-adq` y
`https://www.inegi.org.mx/` respondió HTTP 200. La selección canónica
`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` entregó cero
elegidos; no hubo fila inicial de adquisición.

## DEM-AHORRO-STOCK-DURACION-01

Versión `2026-09-15-stock-ausencia-y-duracion-separados-v1`; modos
CONSTRUCTO, HERMANAS y LATERAL. Búsqueda web real:
`site:edu.mx filetype:pdf cuestionario "ahorros" "cuántos meses" encuesta financiera México`,
`site:condusef.gob.mx filetype:pdf encuesta "ahorros" "meses" cuestionario`,
`site:cnbv.gob.mx filetype:pdf cuestionario "ahorros" "cuánto tiempo" encuesta`
y `site:repositorio.*.mx encuesta bienestar financiero "ahorros" "meses"`.

Los resultados pertinentes devolvieron ENSAFI 2023, ya examinada, y tests
editoriales de CONDUSEF que no son instrumentos probabilísticos. ENSAFI sí
separa tener ahorro y equivalencia del monto en quincenas/meses, pero pertenece
al universo previo y no añade una fuente nueva ni corrige por sí sola el rótulo
de horizonte puro. No se creó candidata ni se tomó decisión científica.

Estado `continua`. Frontera: catálogos variable-por-variable de encuestas
financieras de universidades estatales y archivos históricos no indexados de
CNBV/CONDUSEF. Cursor: buscar instrumento probabilístico con tenencia/ausencia
y meses o días del mismo stock. Tras nueve ciclos sin avance, la alternativa
concreta permanece: mesa elige entre mantener el bloqueo, relabel del uso
acotado autorizado por #772 o aprobar un proxy nuevo con alcance explícito.

Suficiencia: identidad PARCIAL; conceptual NO_ACREDITADA; poblacional
ACREDITADA; selección/no respuesta ACREDITADA; unidad ACREDITADA;
temporalidad PARCIAL; diseño ACREDITADA; identificación NO_APLICA; uso
INCOMPATIBLE; pregunta ABIERTA.

## NC-0202

Versión `2026-09-15-ennvih-diseno-publico-v1`; modos LATERAL y HERMANAS.
Búsqueda web real: `"Berumen (2007)" ENNViH PDF`, `"Berumen" "ENNViH-2"
diseño muestra`, `site:icpsr.umich.edu 118971 codebook variables strata PSU`
y `site:dataverse.harvard.edu MxFLS strata PSU weights`.

Los resultados devolvieron la guía ENNViH-2 ya examinada y falsos positivos
de otros estudios. No apareció copia pública de Berumen (2007), ni archivos
de ENNViH/MxFLS con UPM/estrato por observación o réplicas. No se repitieron
UCLA, IHSN, guías ni pesos.

Estado `continua`; pregunta ABIERTA. Frontera: copia pública de Berumen (2007)
o archivos que expongan identificadores ejecutables de UPM/estrato/réplicas.
Cursor: continuar sólo por Berumen o variables ejecutables. Tras el segundo
ciclo consecutivo sin avance material, alternativa concreta: mantener los IC
bloqueados o pedir a mesa/titular que active NC-0156; no imputar conglomerados.

Suficiencia: identidad ACREDITADA; conceptual ACREDITADA; poblacional
ACREDITADA; selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad
ACREDITADA; diseño PARCIAL; identificación NO_APLICA; uso
APTA_ALCANCE_MENOR; pregunta ABIERTA.

## NC-0162

Versión `AUTO-NC-v1-273b1bd2a16a`; modos CONSTRUCTO, HERMANAS y LATERAL.
Búsqueda web real: `site:inegi.org.mx/rnm 268 ENPOL 2016 DDI XML`,
`site:inegi.org.mx "ENPOL 2016" "descriptor de archivos" PDF`,
`site:inegi.org.mx/contenidos/programas/enpol/2016 doc FD ENPOL 2016` y
`"ENPOL 2016" diccionario de datos Ponderador`.

Se localizó el FD oficial, objeto exacto que la fila residual declaraba
pendiente. A.8 no halló `fd_enpol2016.pdf` en manifiesto ni corpus. Se creó
`ENPOL_2016_FD` con
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/ENPOL_2016_FD` y se adquirió.
Resultado verbatim de las dos descargas: `download1 http=200 bytes=2549127
exit=0`; `download2 http=200 bytes=2549127 exit=0`. Ambas dieron sha256
`5b2c780f29b991ada8f0ed8bb9c0f93ed98ce1e75edcb5c6c0b12aa7ae3f3b19`;
`file` reportó `PDF document, version 1.6 (zip deflate encoded)` y termina en
`%%EOF`. Manifiesto: `enpol2016_fd_pdf`; archivo:
`data/raw/fd_enpol2016.pdf`.

La lectura documental identifica `P8_7` («De los pagos antes mencionados,
¿usted denunció ante alguna autoridad?»), `FAC_PER`, `EST_DIS` y `FPC`. Esto
reduce la brecha de variable y diseño para 2016, pero no acredita por sí solo
comparabilidad con 2021, reserva suficiente ni aptitud confirmatoria. No se
creó relación científica en las tres tablas: `NC-0162` no existe como
`necesidad_id` en `necesidad-objeto-modelo.tsv` y asignarle un objeto de modelo
sería una decisión nueva; la cola y el manifiesto sí enlazan explícitamente el
objeto al mandato GEN2-38.

Estado `continua`. Frontera: comparar P8_7/codificación/universo con ENPOL 2021
y resolver por mesa si la familia entra al conjunto reservado. Cursor: usar el
FD adquirido y el FD 2021 ya presente; no repetir descarga ni adoptar.

Suficiencia: identidad ACREDITADA; conceptual PARCIAL; poblacional ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad PARCIAL;
diseño ACREDITADA; identificación NO_APLICA; uso APTA_ALCANCE_MENOR; pregunta
ABIERTA.
