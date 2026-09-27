# Reconstrucción independiente ENDIREH 2021

Implementación desde las entradas recibidas en `/entrada` y los insumos de
`/raw`, sin helpers del productor, resultados esperados, comparación ni contacto
con el preparador. No se buscaron ni consultaron reservas externas. Esta
declaración describe lo consultado; no certifica restricciones del entorno más
allá de los directorios entregados. Si existiera acceso a reservas del productor,
corresponde la etiqueta REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA.

El SHA-256 del manifiesto recibido es
`de73c528a563885a3b47c0ffa3a6e0c7792e10b6fce54609c5de00f59a5240d1`.
`recibo.json` conserva el manifiesto completo, todas sus entradas, los hashes
recalculados de los siete insumos y el inventario del ZIP. `entrada/` conserva
copias exactas de la especificación. Los hashes de los dos CSV utilizados se
calculan sobre sus bytes descomprimidos. No se incluyen microdatos, PDF ni sus
extracciones de texto.

## Método implementado

La sección XI define el marco de UPM por `(EST_DIS, UPM_DIS)`. Se enlaza TSDem
por `ID_PER`, comprobando unicidad y cobertura completa. Se seleccionan edades
15–120, factor positivo y los seis tipos de instrumento especificados; se
comprueba sexo femenino. La unión vale uno con cualquier respuesta 1–3, cero
solo con veinte respuestas 4; todas las demás combinaciones son desconocidas.
El cociente ponderado usa exclusivamente respuestas conocidas.

Identidades documentadas: FD, sección XI, páginas impresas 301–305, campos
`T_INSTRUM`, `DOMINIO`, `CVE_ENT` y batería `P11_1_1` a `P11_1_20`.
El cuestionario A, pregunta 11.1, confirma la ventana octubre 2020 a la fecha.
Localidad es `DOMINIO`: U urbano, C complemento urbano, R rural; condición es
directamente `T_INSTRUM`. Entidad conserva los códigos de dos dígitos de
`CVE_ENT`. Edad y escolaridad usan `EDAD` y `NIV` de TSDem, con las agrupaciones
explícitas del método. Las llaves se toman de `estimandos.tsv`: no se asignan
identidades por posición ni por similitud de cifras.

Se agregan numeradores y denominadores por UPM y celda. Cada réplica sortea,
con reemplazo, tantas UPM como existen en cada estrato, conservando todas las
mujeres de la UPM y sus factores originales. Las UPM sin casos del dominio
tienen contribución cero y permanecen en el sorteo. Los singleton se sortean
a sí mismos. Se comparten los sorteos entre todas las celdas, sin corrección
de población finita ni reescalamiento no indicado por el método.

Se usan 200 réplicas, semilla 20260923, NumPy Generator PCG64. Estratos y UPM
se ordenan lexicográficamente por sus códigos de texto; el bucle exterior es
réplica y el interior estrato. IC percentil 2.5/97.5 con interpolación lineal;
CV = desviación estándar muestral de las 200 estimaciones / estimación puntual.
“UPM con casos” se interpreta como UPM con mujeres de respuesta conocida en
el dominio, el mismo denominador del estimando. Se aplican n≥100, UPM≥5,
ancho≤0.20, CV≤0.30 cuando p>0.

La especificación no identifica RNG, orden de sorteos, interpolación de
percentiles ni convención de desviación estándar. Se fijan aquí para hacer
reproducible esta implementación. La misma semilla en otro RNG no garantiza
los mismos IC; no se ajustarán al resultado esperado ni a la tolerancia
absoluta 1e-10. El archivo de resultados corresponde a la primera ejecución
numérica completa; el programa impide sobrescribirlo.

## Archivos y reproducción

- `reconstruccion.tsv`: las 50 llaves, punto, IC, estado y motivo.
- `diagnosticos.tsv`: tamaños de muestra y UPM, ancho y CV.
- `replicas.tsv`: 200 réplicas de agregados, sin identificadores personales.
- `recibo.json`: procedencia, hashes, versiones y auditoría de población.
- `SHA256SUMS`: hashes de código, entradas y salidas antes del commit.

Ejecutar `python3 reconstruir.py` con NumPy y pandas, conservando los siete
insumos originales en `/raw`. Para reproducir, copiar código y `entrada/` a
un directorio nuevo sin salidas; no borrar ni sustituir la primera entrega.
Las versiones exactas constan en el recibo. `python3 verificar.py` comprueba
invariantes y consistencia de los agregados ya producidos sin remuestrear.
`sha256sum -c SHA256SUMS` verifica el contenido congelado.

La entrega termina con un commit local anterior a cualquier revelación.
No contiene evaluación de concordancia con resultados del preparador.
