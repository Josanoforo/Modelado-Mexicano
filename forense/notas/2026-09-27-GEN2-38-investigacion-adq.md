# GEN2-38 · investigación ADQ · 2026-09-27

Entorno CAJA acreditado antes de caminar filas: WSL2, clon productivo
`/home/pc0/mm-adq`, `data/raw -> /home/pc0/mm-corpus/raw` y control real
`https://www.inegi.org.mx/` con HTTP 200. El selector canónico de adquisición
devolvió cero elegidos; se ejecutaron las tres investigaciones fijadas por el
wrapper.

## DEM-AHORRO-STOCK-DURACION-01

Versión `2026-09-15-stock-ausencia-y-duracion-separados-v1`; modos
CONSTRUCTO, HERMANAS y LATERAL.

- Búsqueda web: `site:edu.mx encuesta finanzas hogares ahorro "cuánto
  tiempo" ahorros cuestionario México` y `México encuesta ahorro duración
  ahorros meses cuestionario universidad`.
- Aparecieron ENSAFI 2023, ENIF, la encuesta de salud financiera de CONDUSEF
  y la EACF de Banxico. Son familias ya examinadas. La EACF 2024 reporta
  duración de ahorro a nivel hogar; no acredita el par separado requerido en
  unidad persona. ENSAFI condiciona monto/duración a quienes ya ahorran.
- No se descargó ni reencoló una familia repetida. No apareció instrumento
  público nuevo compatible con las ocho dimensiones.

Estado `continua`. Frontera no examinada: catálogos variable-por-variable de
encuestas financieras de universidades estatales distintas de IIEG y archivos
históricos no indexados de CNBV/CONDUSEF. Tras catorce ciclos sin avance, la
alternativa concreta sigue siendo decisión de mesa entre mantener el bloqueo,
relabel del uso acotado autorizado por #772 o aprobar un proxy explícito; esta
clasificación no decide.

## NC-0202

Versión `2026-09-15-ennvih-diseno-publico-v1`; modos LATERAL y HERMANAS.

- Búsqueda web: `site:ennvih-mxfls.org Berumen 2007 survey design pdf`,
  `"Berumen" "MxFLS" 2007 sample design`, `Berumen 2007 Mexican Family Life
  Survey sample design PDF` y `"Mexico Family Life Survey" "Sample Design"
  INEGI 2004 Berumen`.
- Los resultados llevan otra vez a `usersguidev2.pdf`, literatura secundaria
  e IHSN 7063. La guía cita el documento de trabajo Berumen (2007), pero no lo
  adjunta ni aporta identificadores ejecutables de UPM/estrato o réplicas.
- No se repitieron IHSN, UCLA ni las guías oficiales ya agotadas.

Estado `continua`. Frontera: copia pública independiente de Berumen (2007),
adjunto INEGI (2004) Sample Design o archivo oficial con UPM/estrato/réplicas.
La alternativa humana continúa siendo NC-0156; no se imputan conglomerados.

## NC-0260

Versión `AUTO-NC-v1-aac2d014bf36`; modos CONSTRUCTO, HERMANAS y LATERAL.

- Búsqueda web externa: `"EJE-TRANSPUESTO" datos descriptor` y `"reactivos
  ciegos" encuesta descriptor`. No devolvió documentación pública pertinente;
  los resultados homónimos no describen el censo ni sus 2 368 filas.
- La evidencia material sigue siendo interna y ya acreditada por el acto que
  originó la NC: categorías EJE-TRANSPUESTO, MIEMBRO-ES-EL-PROPIO-FD y
  NO-ES-TABLA-DE-DATOS. La pregunta no necesita una fuente externa nueva sino
  re-derivar el censo leyendo el crosswalk ya existente.
- No se abre candidata ni se toma una decisión científica por clasificación.

Estado `barrera`. Evento de reactivación: asignación de un acto con
`data/reactivos-ciegos-81-v1_0.tsv`, `tools/censa_reactivos_ciegos.py` y el
crosswalk residual en perímetro, o decisión explícita de mesa de conservar el
denominador. No queda una ruta pública plausible cuya repetición cambie este
resultado.
