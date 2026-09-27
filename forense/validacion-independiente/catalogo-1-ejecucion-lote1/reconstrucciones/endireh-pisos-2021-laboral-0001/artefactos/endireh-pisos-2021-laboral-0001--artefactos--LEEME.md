# Entrega congelada antes de revelación

Rótulo: **REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA**. No se certifica aislamiento del entorno; el permiso de lectura es amplio. No se buscaron ni consultaron clones, comparaciones, reservas o resultados esperados, y no se contactó al preparador. Las fuentes utilizadas fueron exclusivamente `/entrada` y `/raw`. Este rótulo conservador no afirma exposición a resultados. No se declara concordancia con resultados de referencia.

## Resultado y límite de identidad

`reconstruccion.tsv` contiene las 100 llaves recibidas, en su orden original, con estado `NO-RECALCULABLE-DESDE-SPEC`, campos numéricos vacíos y motivo. Cada eje/segmento tiene dos llaves; ni `estimandos.tsv` ni `metodo.md` identifican cuál corresponde a vida y cuál a reciente. Los ordinales de `celda` no son una definición temporal. No se asignaron identidades por ordinal, posición ni similitud numérica.

El método estadístico sí pudo ejecutarse. `resultados_semanticos.tsv` contiene los primeros 100 cálculos, etiquetados explícitamente por ventana, eje y segmento, **sin asignarlos a ninguna llave recibida**. Todos satisfacen los umbrales de publicación. `replicas_agregadas.tsv` conserva las 200 réplicas de cada cálculo publicable; no contiene microdatos ni identificadores individuales, de UPM o municipales. No hay cruces entre ejes.

## Decisiones de implementación

- Lectura Latin-1 de los CSV directamente desde el ZIP. Unión uno a uno mediante `ID_PER`; se comprueba identidad única y correspondencia completa con TSDem, y sexo femenino. Factor, estrato y UPM provienen de TB_SEC_VIII. Edad y NIV provienen de TSDem.
- Universo analítico: A1/A2/B1/B2/C1/C2, FAC_MUJ positivo y finito, edad 15–120. Las 110127 filas del módulo cumplen esos filtros.
- Vida: P8_1=1; unión positiva con cualquier sí, negativa solo con 19 no, desconocida en los demás casos. Reciente: además P8_4=1 y vida conocida; P8_9=2 implica código reciente 4, P8_9=1 permite leer P8_11, y otros códigos de vida dejan el acto reciente desconocido. Se aplican las uniones especificadas. El denominador ponderado incluye únicamente resultados conocidos en la ventana y dominio correspondientes.
- Ejes directos: localidad=DOMINIO, pareja=T_INSTRUM, entidad=CVE_ENT. Edad y NIV se agrupan exactamente según metodo.md. Ninguna variable se deriva de la posición de una llave.
- Marco de remuestreo: las 17744 UPM presentes en TB_SEC_VIII, agrupadas en los 617 EST_DIS, antes de restringir dominios y elegibilidad. Identificador de UPM: par (EST_DIS, UPM_DIS). En cada estrato se extrae con reemplazo su mismo número de UPM y se aplican sus multiplicidades a los totales ponderados. Se incluyen todas las UPM de aporte cero. Un singleton se extraería siempre a sí mismo; no hay singleton en estos insumos.
- Se usa un único conjunto de 200 remuestreos para todos los dominios y ventanas. Semilla 20260923, NumPy Generator PCG64; estratos y UPM ordenados lexicográficamente; por estrato, `integers(0,n,size=(200,n))`, recorrido de réplicas por filas. No se cambia la semilla ni se seleccionan resultados.
- Percentiles con interpolación lineal NumPy (tipo 7). CV=desviación estándar muestral de las réplicas (ddof=1) dividida entre estimación puntual cuando p>0. UPM con casos significa UPM con al menos una observación conocida del dominio. Se exigen n≥100, UPM≥5, ancho≤0.20 y CV≤0.30 si p>0. Si una réplica no tuviera denominador se suprimiría la celda; no ocurrió.
- La especificación no fija familia de RNG, versión, recorrido de sorteos, interpolación de percentiles ni convención ddof. Se documentan estas convenciones para reproducibilidad: **la misma semilla no garantiza IC idénticos entre implementaciones**, especialmente con tolerancia recibida 1e-10. No se consultó el RNG del productor ni se ajustaron IC.

## Evidencia documental

Documentos locales recibidos: FD, páginas PDF 134–135 (identificación del módulo y DOMINIO/T_INSTRUM), 140–143 (P8_9 y comienzo de P8_11), página 18 (NIV); cuestionario A, página PDF 13 (preguntar 8.11 solo con 8.4=1 y 8.9=1; frecuencias 1–3 y no ocurrió=4). Se consultaron extracciones de texto temporales fuera del repositorio. Los originales y sus extracciones no se incluyen en el commit.

`inventario_raw.json` conserva las siete entradas originales de insumos.json, rutas recibidas, tamaños y hashes recalculados. `entradas_zip.json` conserva nombres, tamaños, CRC32 y SHA-256 del contenido descomprimido de todas las entradas del ZIP. Las seis entradas del manifiesto fueron verificadas; los siete insumos raw también. `entrada/` conserva byte a byte toda la carpeta recibida, incluido el manifiesto original. `recibo.json` conserva su SHA-256, la lista de entradas y versiones de ejecución.

## Ejecución y verificación

Ejecutado: `OPENBLAS_NUM_THREADS=1 python3 reconstruir.py`. Dependencias: Python, NumPy y pandas genéricos, con versiones en recibo.json. No se utilizaron helpers del productor. Hubo un fallo inicial de decodificación UTF-8, antes de producir estimaciones; se corrigió a Latin-1. La ejecución posterior produjo los primeros resultados numéricos y no se repitió ni se sustituyó.

Verificación: `OPENBLAS_NUM_THREADS=1 python3 verificar.py`. Prueba uniones con desconocidos, saltos y exclusiones de elegibilidad; comprueba cobertura y orden de llaves, motivos, límites de publicación y percentiles calculados sobre las réplicas conservadas. No emplea valores esperados externos. `control.json` registra los conteos agregados de ejecución.

Para reproducir, copiar el código y `entrada/` a una carpeta limpia, con los mismos `/entrada` y `/raw` montados. El programa rechaza sobrescribir `resultados_semanticos.tsv`, para proteger el primer resultado. No se solicita revelación al terminar.

## Congelación

`SHA256SUMS` sella todos los archivos entregados salvo sí mismo y los metadatos de Git; el commit sella también ese listado. Git se inicializa en `/work/reconstruccion`, porque la raíz tiene `.git` protegido. No se versionan raw, ZIP, PDF ni registros individuales. El identificador del commit se entrega al usuario fuera del árbol para evitar una autorreferencia imposible.
