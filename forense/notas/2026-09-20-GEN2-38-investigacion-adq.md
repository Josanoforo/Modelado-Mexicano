# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-20. Entorno: CAJA/WSL2. Antes de caminar, `data/raw`
resolvió a `/home/pc0/mm-corpus/raw`, el clon fue `/home/pc0/mm-adq` y
`https://www.inegi.org.mx/` respondió HTTP 200. La selección canónica
`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` entregó cero
elegidos; no hubo fila inicial de adquisición.

## DEM-AHORRO-STOCK-DURACION-01

Versión `2026-09-15-stock-ausencia-y-duracion-separados-v1`; modos
CONSTRUCTO, HERMANAS y LATERAL. Búsqueda web real (20/sep):
`site:mx encuesta ahorro duración ahorros meses cuestionario México universidad`,
`site:edu.mx encuesta finanzas personales ahorro duración fondo emergencia cuestionario`
y `México encuesta bienestar financiero meses ahorros disponibles duración stock ahorro`.

Los resultados pertinentes fueron EACF/Banxico, ENSAFI, ENIF, ENFIH y un
estudio académico de resiliencia financiera de dueños de MiPyME. Las cuatro
encuestas nacionales ya estaban en el universo examinado. El estudio MiPyME
pregunta cuánto tiempo podría mantenerse la persona con sus ahorros actuales,
pero su población son dueños de MiPyME en contexto de crisis y no acredita un
instrumento probabilístico de personas adultas en México ni el par separado
tenencia/ausencia + duración del mismo stock. No es candidata material para
los tres consumidores.

Estado `continua`. Frontera: catálogos variable-por-variable de encuestas
financieras de universidades estatales y archivos históricos no indexados de
CNBV/CONDUSEF. Cursor: buscar instrumento probabilístico con tenencia/ausencia
y meses o días del mismo stock. Alternativa concreta, obligatoria tras más de
dos ciclos sin avance: mesa elige entre mantener el bloqueo, relabel del uso
acotado autorizado por #772 o aprobar un proxy nuevo con alcance explícito;
esta corrida no decide.

Suficiencia: identidad PARCIAL; conceptual NO_ACREDITADA; poblacional
ACREDITADA; selección/no respuesta ACREDITADA; unidad ACREDITADA;
temporalidad PARCIAL; diseño ACREDITADA; identificación NO_APLICA; uso
INCOMPATIBLE; pregunta ABIERTA.

## NC-0202

Versión `2026-09-15-ennvih-diseno-publico-v1`; modos LATERAL y HERMANAS.
Búsqueda web real: `Berumen 2007 Mexican Family Life Survey sample design PDF`,
`"Berumen" "Mexican Family Life Survey" 2007` e
`ICPSR 118971 documentation sample design MxFLS`.

Los resultados devolvieron las guías oficiales ya examinadas, el portal MxFLS,
IHSN y un capítulo público de eScholarship que resume el diseño basal como
probabilístico, estratificado, multietápico y por conglomerados. Ninguno
publica la copia Berumen (2007), identificadores de UPM/estrato por observación,
réplicas o campos ejecutables para varianza. El capítulo es descripción
secundaria y no añade cobertura respecto del PDF UCLA ya registrado; no se
encola ni descarga otra copia.

Estado `continua`; pregunta ABIERTA. Frontera: copia pública de Berumen (2007)
o archivos que expongan identificadores ejecutables de UPM/estrato/réplicas.
Cursor: continuar sólo por Berumen o variables ejecutables, sin repetir
UCLA/IHSN/guías/pesos.

Suficiencia: identidad ACREDITADA; conceptual ACREDITADA; poblacional
ACREDITADA; selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad
ACREDITADA; diseño PARCIAL; identificación NO_APLICA; uso
APTA_ALCANCE_MENOR; pregunta ABIERTA.

## NC-0284

Versión `AUTO-NC-v1-1849e41a8cba`; modos CONSTRUCTO, HERMANAS y LATERAL.
Búsqueda web real: `site:inegi.org.mx ENCRIGE 2020 microdatos CSV cuestionario
descarga`, `site:inegi.org.mx/rnm ENCRIGE 2020 datos cuestionario` y `ENCRIGE
2020 microdatos CSV cuestionario`. Confirmó el programa y cuestionario
oficiales, pero la brecha vigente no era descubrir otra fuente: era resolver
las raíces locales de dos inputs ya sellados.

En esta CAJA, `python3 tools/corrida0.py verify
CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001` resolvió los tres inputs del
manifiesto, acreditó sus SHA-256 y terminó `VERIFY: REPRODUCE
(CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)`: 15/15 RESULT reprodujeron, con
delta 0 donde aplica. La premisa `RAIZ_NO_CONFIGURADA` quedó superada por
evidencia local existente; no hubo descarga ni decisión científica. La
publicación/estado de registro y cualquier firma de contador permanecen fuera
de esta clasificación.

Estado `evidencia_existente`; la pregunta original queda CUBIERTA en su brecha
de verificación. Frontera externa no examinada: ninguna material para este
objeto; la etapa restante es de registro/gobierno, no de fuente. Cursor: no
repetir búsqueda web; el acto autorizado consume el verify REPRODUCE y decide
la actualización registral sin alterar el estimando.

Suficiencia: identidad ACREDITADA; conceptual ACREDITADA; poblacional
ACREDITADA; selección/no respuesta ACREDITADA; unidad ACREDITADA;
temporalidad ACREDITADA; diseño ACREDITADA; identificación NO_APLICA; uso
APTA_USO_DECLARADO; pregunta CUBIERTA.
