# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-18. Entorno: CAJA/WSL2. Antes de caminar, `data/raw`
resolvió a `/home/pc0/mm-corpus/raw`, el clon productivo fue
`/home/pc0/mm-adq` y `https://www.inegi.org.mx/` respondió HTTP 200 desde
`200.23.8.5`. La selección canónica `python3 tools/adq_doctor.py --selecciona
--maximo 5 --json` entregó cero elegidos; no hubo fila inicial de adquisición.
Se ejecutaron en orden las tres investigaciones seleccionadas por el wrapper.

## DEM-AHORRO-STOCK-DURACION-01

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`. Modos:
CONSTRUCTO, HERMANAS y LATERAL.

Búsquedas web reales nuevas: `site:edu.mx (encuesta OR cuestionario) "ahorros"
"meses" México hogares`, `site:mx "¿Por cuánto tiempo" ahorros encuesta
hogar`, `site:condusef.gob.mx encuesta ahorro "meses" cuestionario` y
`site:cnbv.gob.mx encuesta ahorro "cuánto tiempo" cuestionario`.

Los resultados pertinentes fueron IIEG EIF 2022, ENIF 2024, ENSAFI 2023 y dos
tests divulgativos de CONDUSEF. Las tres encuestas ya estaban expresamente en
el universo agotado; los tests de CONDUSEF no tienen marco probabilístico ni
microdato y preguntan capacidad hipotética, no ausencia/tenencia y duración
del mismo stock en campos separados. No apareció candidata pública nueva que
reduzca la brecha. No se creó residual ni se intentó payload.

Estado: `continua`. Frontera no examinada: catálogos variable-por-variable de
encuestas financieras de universidades estatales fuera de Colmex/UNAM/IIEG y
archivos históricos no indexados de CNBV/CONDUSEF. Cursor: buscar un
instrumento probabilístico con una variable de tenencia/ausencia y otra de
meses o días cubiertos por ese mismo stock, no capacidad hipotética mezclada.
Tras seis ciclos sin avance material, alternativa concreta para mesa: relabel
de los tres consumidores al uso acotado autorizado por #772; esta corrida no
lo decide.

Suficiencia: identidad PARCIAL; concepto NO_ACREDITADA; población ACREDITADA;
selección/no respuesta ACREDITADA; unidad ACREDITADA; temporalidad PARCIAL;
diseño ACREDITADA; identificación NO_APLICA; uso INCOMPATIBLE; pregunta
ABIERTA.

## NC-0202

Versión: `2026-09-15-ennvih-diseno-publico-v1`. Modos: LATERAL y HERMANAS.

Búsquedas web reales: `ICPSR 118971 Mexican Family Life Survey weights
documentation`, `"118971" "MxFLS" sample design`,
`site:ennvih-mxfls.org weights wave 2 wave 3 PSU strata` y `Berumen 2007
Mexican Family Life Survey sample design PDF`.

La página oficial pública de ENNViH-3 expone por separado ponderadores
transversales 2009 y longitudinales a población 2002. A.8 acreditó que los
objetos exactos ya estaban en `data/manifiesto.yaml` como
`ennvih3_2009_ponderador_transversal` y
`ennvih3_2009_ponderador_longitudinal`, con sus ZIP presentes en
`data/raw/ennvih/`; no se repitió la descarga. La inspección de contenedor y
columnas produjo `testzip=None`: todos los archivos contienen sólo `folio`,
`ls` cuando aplica y un factor `fac_*`; no contienen UPM, estrato ni réplicas.
La guía de ola 2 remite a Berumen (2007), pero tampoco publica esos campos.

Estado: `evidencia_existente`; la pregunta sigue ABIERTA. Frontera no
examinada: metadatos/adjuntos públicos del depósito ICPSR 118971 y una copia
pública independiente del documento Berumen (2007). Cursor: inspeccionar esos
dos objetos sin repetir guías, IHSN ni ZIP de ponderadores; si tampoco aportan
PSU/estrato/réplicas, conservar la solicitud humana NC-0156.

Suficiencia: identidad ACREDITADA; concepto ACREDITADA; población ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad ACREDITADA;
diseño PARCIAL; identificación NO_APLICA; uso INCOMPATIBLE; pregunta ABIERTA.

## NC-0244

Versión: `AUTO-NC-v1-2fbd85423ec2`. Modos: CONSTRUCTO, HERMANAS y LATERAL.

Búsquedas externas reales: buscador web con
`site:github.com/Josanoforo/Modelado-Mexicano "RES-0047" "RES-0049"`, los dos
IDs de CALC por separado, y API pública de GitHub con búsqueda de código,
issues/PR y commits del archivo `data/corrida0/relevo-usos-v1_0.tsv`.
El buscador general no indexó el contenido. La API de GitHub devolvió cinco PR
pertinentes, incluidos #788 (`GEN2-RELEVO-USOS-1`) y #800
(`GEN2-CAJA-SUCESORES-1`), y los commits públicos `a7255e0...` y `292ac12...`.
La historia pública confirma la secuencia ya descrita: #788 adoptó ambos slots
citando `CALC-ENIF-0001`; #800 re-derivó después y detectó el segundo canal
`CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1`. No hay discrepancia numérica ni una
fuente pública externa capaz de adjudicar cuál procedencia interna debe mandar.

Estado: `barrera`. La reactivación es una decisión explícita de mesa que elija
el pin canónico de RES-0047/RES-0049; no corresponde fabricar una candidata de
adquisición ni tomar la decisión por clasificación. Frontera no examinada:
ninguna ruta pública científica pertinente; sólo queda la adjudicación interna
de mesa. Cursor: al recibir la firma, actualizar el escritor canónico y
re-derivar la vista sin cambiar los valores 0.458657 y 0.626870.

Suficiencia: identidad ACREDITADA; concepto ACREDITADA; población ACREDITADA;
selección/no respuesta ACREDITADA; unidad ACREDITADA; temporalidad ACREDITADA;
diseño ACREDITADA; identificación NO_APLICA; uso APTA_USO_DECLARADO; pregunta
ABIERTA (procedencia pendiente, no cifra pendiente).
