# Reconstrucción independiente ENDIREH 2021

Trabajo realizado únicamente con `/entrada` y `/raw`, sin resultados esperados, helpers del productor, consultas al preparador ni solicitud de revelación. No se exploraron clones ni reservas. El recibo acredita lo efectivamente leído; no certifica el aislamiento de rutas ajenas a las entradas entregadas. No se declara coincidencia con resultados de referencia.

## Identidad y alcance

`reconstruccion.tsv` conserva todas las llaves entregadas y agrega `motivo`. Las 471 filas de prevalencias carecen de la dimensión de ventana: el método define tanto 14.1 (desde inicio de relación) como 14.3 (periodo reciente), mientras `estimandos.tsv` no indica cuál corresponde a cada llave. No se deduce la ventana de la posición, número de celda, duplicación, ausencia de otra fila o supresión aparente. Se implementaron las reglas de unión y salto, pero no se asignaron números a esas identidades incompletas.

El método tampoco define cómo agrupar los códigos NIV/GRA en los cuatro niveles educativos. El FD describe preescolar, técnicas con distintos antecedentes y normal, pero no proporciona la agrupación solicitada. Las ocho filas de ayuda/denuncia por escolaridad quedan sin cifras. No se supone una clasificación para ninguna de ellas, incluido `ninguno`, cuya frontera con preescolar no está fijada.

Se reconstruyen las identidades restantes de ayuda, denuncia, instituciones y razones. Cada variable usa sus respuestas conocidas: 1/2 en ayuda, denuncia e instituciones; 0/1 en razones. Blancos y 9 se excluyen del denominador de la variable. Instituciones: ayuda=1; razones: ayuda=2 y denuncia=2 en microdato. Siempre B1/B2/C1 y algún acto positivo 1–38 de 14.1. Actos exclusivos AB se excluyen para C. No se suman categorías.

EDAD 97 significa 97 o más; 98 acredita 15 o más sin edad especificada y entra al universo general pero no a grupos de edad; 99 no acredita edad y se excluye. Uniones por ID_PER verificadas como únicas y completas. Se usa FAC_MUJ sin normalizar; DOMINIO para localidad, CVE_ENT para entidad y T_INSTRUM para pareja.

## IC y decisiones de implementación

NumPy 2.3.5; Python y versión efectiva registrados en recibo. Semilla 20260923, 200 réplicas, Generator(PCG64), `default_rng`. Marco de UPM: todos los pares EST_DIS/UPM_DIS presentes en TB_SEC_XIV, antes de filtros, incluidos C2 y mujeres con contribución cero a la celda. No se limita el marco a UPM con casos ni a UPM del segmento. No se añaden UPM que no aparecen en la tabla de la unidad mujer. La inspección de TVIV detectó 19 pares adicionales; el método no especifica ampliar el marco a viviendas sin registro XIV.

Orden lexicográfico de estratos y UPM. Por estrato se sortean n UPM con reemplazo, con igual probabilidad, en una matriz de tamaño (200,n); se reutilizan los mismos sorteos en todas las celdas. Los pesos de réplica son FAC_MUJ por multiplicidad de UPM. Se calcula la razón de totales ponderados, sin normalizar pesos ni aplicar corrección de población finita. Percentiles con interpolación lineal; CV = desviación estándar muestral de las réplicas (ddof=1) / estimación puntual. Ningún estrato tiene una sola UPM. Un denominador de réplica cero se informaría sin sustituir su valor.

La spec no fija familia RNG, orden de sorteos, reutilización entre celdas, interpolación de percentiles ni ddof. Estas convenciones se fijaron antes del primer cálculo. No se garantiza igualdad de IC a 1e-10 con otra implementación, aun con igual semilla. Se conservan los primeros números y las réplicas agregadas publicables; no se ajusta el RNG frente a resultados ajenos.

Se aplican n conocido ≥100, ≥5 UPM con respuesta positiva, ancho ≤0.20 y CV ≤0.30 si p>0. Las supresiones, si las hubiera, no publican cifras ni réplicas; al no existir estado SUPRIMIDO en el vocabulario solicitado, su motivo explicita la regla de publicación. No se interpreta una supresión como falta de acceso.

## Archivos y reproducción

- `entrada/`: copia exacta de las siete entradas recibidas, incluido manifiesto original.
- `recibo.json`: SHA-256 del manifiesto, lista original de entradas, verificación de hashes de entradas e insumos, rutas y versiones.
- `entradas_zip.json`: nombres, tamaños y SHA-256 de cada entrada del archivo ZIP; no incluye contenido raw.
- `reconstruir.py`: implementación desde la especificación y documentación entregadas.
- `reconstruccion.tsv`: entrega por llave.
- `replicas.tsv`: únicamente réplicas agregadas por celda publicable, sin identificadores personales o de UPM.
- `diagnostico.tsv`: conteos agregados de denominador y UPM con casos de las celdas con identidad resuelta.
- `resumen.json`: cobertura y motivos.
- `SHA256SUMS`: hashes de todos los archivos congelados salvo el propio listado y `.git`.

Requiere biblioteca estándar y `numpy==2.3.5`. Para reproducir en una copia limpia, con `/raw` disponible, ejecutar `OPENBLAS_NUM_THREADS=1 python3 reconstruir.py`. El programa se niega a sobreescribir `reconstruccion.tsv`: el primer resultado se preserva. `python3 reconstruir.py --selftest` verifica positividad de unión, negativos completos, desconocidos, exclusiones C y propagación del salto 14.3. La validación final revisa cobertura exacta de llaves, estados, motivos, límites de proporciones y 200 réplicas por celda publicada, sin recalcular ni seleccionar resultados.

Los PDFs y los microdatos permanecen fuera del repositorio. El commit congela entradas, implementación, recibo, documentación de decisiones y cifras antes de cualquier revelación. Se termina sin pedir resultados al preparador.
