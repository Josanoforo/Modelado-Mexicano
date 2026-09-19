# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-19. Entorno: CAJA/WSL2. Antes de caminar, `data/raw`
resolvió a `/home/pc0/mm-corpus/raw`, el clon fue `/home/pc0/mm-adq` y
`https://www.inegi.org.mx/` respondió HTTP 200. La selección canónica
`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` entregó cero
elegidos; no hubo fila inicial de adquisición.

## DEM-AHORRO-STOCK-DURACION-01

Versión `2026-09-15-stock-ausencia-y-duracion-separados-v1`; modos
CONSTRUCTO, HERMANAS y LATERAL. Búsquedas web reales:
`site:edu.mx encuesta financiera ahorro "meses" gastos ahorros México cuestionario`,
`site:mx "cuánto tiempo" "ahorros" encuesta México`,
`site:condusef.gob.mx encuesta ahorro cubrir gastos meses` y
`site:cnbv.gob.mx encuesta ahorro duración stock ahorros`.

Los resultados pertinentes fueron EACF/Banxico, IIEG EIF, ENSAFI y el test
de salud financiera de CONDUSEF. EACF, IIEG y ENSAFI ya pertenecían al
universo examinado; el test no tiene marco probabilístico ni microdato. ENSAFI
condiciona la duración a quienes declararon ahorro, pero no crea el par público
nuevo de ausencia/tenencia y duración del mismo stock que exige la versión.
No apareció candidata pública nueva. Estado `continua`. Frontera: catálogos
variable-por-variable de encuestas financieras de universidades estatales y
archivos históricos no indexados de CNBV/CONDUSEF. Cursor: buscar un
instrumento probabilístico con tenencia/ausencia y meses o días cubiertos por
el mismo stock. Alternativa concreta para mesa tras más de dos ciclos: relabel
del uso acotado autorizado por #772; esta corrida no lo decide.

Suficiencia: identidad PARCIAL; conceptual NO_ACREDITADA; poblacional
ACREDITADA; selección/no respuesta ACREDITADA; unidad ACREDITADA;
temporalidad PARCIAL; diseño ACREDITADA; identificación NO_APLICA; uso
INCOMPATIBLE; pregunta ABIERTA.

## NC-0202

Versión `2026-09-15-ennvih-diseno-publico-v1`; modos LATERAL y HERMANAS.
Búsquedas web reales: `"Description of MxFLS Baseline Sample" filetype:pdf`,
`"Berumen" "MxFLS" sample design`, `"Mexican Family Life Survey" "primary
sampling unit" strata` e `ICPSR 118971 documentation files`.

Hallazgo nuevo: un informe público alojado por UCLA reproduce una ficha MxFLS
de 2007 y describe muestra probabilística multietápica, 150 comunidades y tres
estratos construidos con 14 variables del marco ENEU. Se descargó dos veces;
ambas copias dieron SHA-256
`f6ae6b5f803885a03460a5cc88ca0de8173d3b489caf5deff861d4b300abc405` y el
PDF de 107 páginas termina en `%%EOF`. El payload quedó en
`data/raw/ennvih/ucla_mxfls_design_summary_2007_a.pdf`.

No se acredita como adquirido: `tests/manifiesto.py --registra` paró porque el
manifiesto vigente contiene la clave preexistente `estado_reserva` en
`enco_2025_junio_dbf_reservado`, desconocida para el validador. La fila
`UCLA_MXFLS_DESIGN_SUMMARY_2007` queda como
`NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)` y no se añadió relación a las tres
tablas porque la capa payload no obtuvo ID. Uso menor permitido una vez
registrado: descripción general del diseño; no aporta identificadores de
UPM/estrato, réplicas ni habilita intervalos.

Estado `candidata_publica`; pregunta ABIERTA. Frontera: copia pública del
documento Berumen (2007) o archivos que expongan identificadores ejecutables.
Cursor: reparar la incompatibilidad manifiesto/validador, registrar el PDF ya
descargado sin repetir red y continuar sólo por Berumen/variables ejecutables.

Suficiencia: identidad ACREDITADA; conceptual ACREDITADA; poblacional
ACREDITADA; selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad
ACREDITADA; diseño PARCIAL; identificación NO_APLICA; uso
APTA_ALCANCE_MENOR; pregunta ABIERTA.

## NC-0253

Versión `AUTO-NC-v1-ee3e3a37bf9d`; modos CONSTRUCTO, HERMANAS y LATERAL.
Búsquedas web reales sobre el repositorio público por
`GEN2-L8-LINAJE-HEREDADO-1`, `RESULT-L8CONV-A-P-MINIMO` y
`data/l8-resultados-tipo-boleta-v1_0.json` no devolvieron resultados indexados.
La comprobación directa del árbol actual sí encontró que la premisa de entrada
fue superada: `tools/corrida0.py` ya reconoce el JSON como fuente legacy,
`data/corrida0/corridas.tsv` clasifica el linaje como `HEREDADO`, y
`forense/evidencia-replay-aislado-2026-09-19.json` acredita reproducción
idéntica de los tres RESULT. No corresponde buscar otra fuente ni citar por
clasificación; queda una etapa de adopción/pin, no de adquisición.

Estado `evidencia_existente`; pregunta original CUBIERTA en su brecha de
linaje. Frontera no examinada: ninguna ruta externa material; la etapa restante
es que el acto autorizado cite los tres RESULT en `milpa/tramite.yaml` si la
mesa mantiene esa adopción. Cursor: no repetir búsqueda web; verificar el pin
de adopción en el acto sucesor.

Suficiencia: identidad ACREDITADA; conceptual ACREDITADA; poblacional
NO_APLICA; selección/no respuesta NO_APLICA; unidad ACREDITADA; temporalidad
ACREDITADA; diseño ACREDITADA; identificación NO_APLICA; uso
APTA_USO_DECLARADO; pregunta CUBIERTA.
