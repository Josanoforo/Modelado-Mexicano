# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-17. Entorno: CAJA/WSL2. Antes de caminar, `data/raw`
resolvió a `/home/pc0/mm-corpus/raw`, el clon productivo fue
`/home/pc0/mm-adq` y `https://www.inegi.org.mx/` respondió HTTP 200. La
selección canónica `python3 tools/adq_doctor.py --selecciona --maximo 5
--json` entregó cero elegidos; por ello no hubo fila inicial de adquisición.
Se ejecutaron en orden las tres investigaciones seleccionadas por el wrapper.

## DEM-AHORRO-STOCK-DURACION-01

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`.

Modos: CONSTRUCTO, HERMANAS y LATERAL. Consultas web reales nuevas, sin
repetir las familias agotadas: `site:*.edu.mx encuesta estatal México
cuestionario ahorro duración ahorros meses gastos`, `site:colmex.mx encuesta
ahorro cuestionario duración ahorros México` y
`site:repositorio.uanl.mx encuesta financiera ahorro duración cuestionario
México`.

El resultado pertinente fue el *Cuestionario Socioeconómico* de El Colegio de
México (`https://ogp.colmex.mx/encuestasbdogp/CuestionarioSocioeconomico_01jun.pdf`).
El contenido indexado separa una condición de ahorro en los últimos 12 meses
(9.1), las personas que ahorraron (9.2) y el monto ahorrado (9.4). No observa
duración/cobertura temporal del mismo stock, y su unidad inmediata es hogar
con desagregación por persona, no la persona adulta nacional exigida. Es una
candidata pública nueva respecto de la frontera previa pero
`EXISTE-NO-SATISFACE`; no justifica alta residual ni descarga. Se deja
vinculada a este ciclo bajo el mandato de investigación
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/COLMEX_CUESTIONARIO_SOCIOECONOMICO_AHORRO`;
el token no autoriza adopción científica.

Estado: `continua`. Frontera no examinada: repositorios académicos estatales
distintos de Colmex/UNAM/IIEG y archivos no indexados CNBV/CONDUSEF. Cursor:
examinar un catálogo variable-por-variable de una encuesta estatal que además
de tenencia/monto pregunte cuántos días o meses cubre ese mismo stock. Tras
más de dos ciclos sin avance material, la alternativa concreta para mesa se
mantiene: relabel de los tres consumidores al uso acotado autorizado por #772,
sin ejecutarlo por clasificación.

Suficiencia: identidad PARCIAL; concepto NO_ACREDITADA; población ACREDITADA;
selección/no respuesta ACREDITADA; unidad ACREDITADA; temporalidad PARCIAL;
diseño ACREDITADA; identificación NO_APLICA; uso INCOMPATIBLE; pregunta
ABIERTA.

## NC-0202

Versión: `2026-09-15-ennvih-diseno-publico-v1`.

Modos: LATERAL y HERMANAS. Consultas web reales: `"Sample Design. Description
of MxFLS Baseline Sample"`, `Berumen 2007 ENNViH MxFLS diseño muestra UPM
estrato PDF` y `site:repositorio.ibero.mx ENNViH diseño muestral Berumen
2007`.

La búsqueda ubicó la copia pública exacta de INEGI (2004), *Diseño muestral*,
en `https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf`. A.8 mostró que
ya estaba en `data/manifiesto.yaml` como `ennvih1_muestra_diseno`, archivo
`data/raw/ennvih_diseno/ennvih-1_muestra.pdf`, SHA-256
`9f90df10338c7749cf46f86edc0664fc300c913e4fc4b1eee5e360d2970e91f0`.
No se repitió la descarga. El documento acredita para la línea basal selección
independiente por región/estrato, UPM con probabilidad proporcional al tamaño,
USM y vivienda, pero no entrega identificadores públicos ejecutables de
UPM/estrato para olas 2/3 ni réplicas. Estado: `evidencia_existente`; la
pregunta permanece ABIERTA.

Frontera: tablas públicas de pesos de olas 2/3 y metadatos del depósito ICPSR
118971. Cursor: inspeccionar sólo nombres/columnas de archivos de pesos o
metadatos del depósito, sin repetir guías, IHSN ni este PDF; si sólo aparecen
factores, conservar la solicitud humana NC-0156.

Suficiencia: identidad ACREDITADA; concepto ACREDITADA; población ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad ACREDITADA;
diseño PARCIAL; identificación NO_APLICA; uso INCOMPATIBLE; pregunta ABIERTA.

## NC-0162

Versión: `AUTO-NC-v1-b998fe1ea1c5`.

Modos: CONSTRUCTO, HERMANAS y LATERAL. Consultas web reales:
`site:inegi.org.mx/contenidos/programas/enpol/2016 "descriptor de archivos"`,
`site:inegi.org.mx/contenidos/programas/enpol/2016 "FD" ENPOL 2016 xlsx` y
`site:inegi.org.mx/programas/enpol/2016 documentación microdatos descriptor
archivos`.

La búsqueda confirmó dos objetos públicos oficiales: la página de programa
ENPOL 2016 y el diccionario variable-por-variable de RNM, catálogo 268
(`https://www.inegi.org.mx/rnm/index.php/catalog/268/data_dictionary`). La
landing acredita población privada de la libertad de 18 años y más, muestra
de 64,150 personas, cobertura nacional/entidad/centros de interés y diseño
probabilístico estratificado. RNM enumera las seis tablas del microdato. Esto
mejora la frontera de búsqueda, pero no acredita todavía cuál variable mide la
denuncia/mordida requerida por R11 ni su comparabilidad con 2021. La ruta queda
vinculada al mandato
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/ENPOL_2016_RNM_DICCIONARIO`.
No hubo intento de payload: una landing/diccionario web no se registra como
microdato ni sustituye el FD.

Estado: `continua`. Frontera: exportación DDI/XML o JSON del catálogo RNM 268
y documento FD 2016, si su enlace directo público puede resolverse sin fuerza
bruta. Cursor: abrir la exportación oficial y buscar nombre, texto, universo,
codificación y ponderador del reactivo de corrupción/denuncia; si es un
payload público pertinente, crear residual y adquirirlo dentro de GEN2-38.
La alternativa sustantiva no cambia: ENPOL 2016 por sí sola es alcance menor y
no completa las 6 familias piloto + 12 confirmatorias requeridas; mesa tendría
que reducir explícitamente ese umbral o aportar nuevas familias retenidas.

Suficiencia: identidad ACREDITADA; concepto PARCIAL; población ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad PARCIAL;
diseño ACREDITADA; identificación NO_APLICA; uso APTA_ALCANCE_MENOR; pregunta
ABIERTA.
