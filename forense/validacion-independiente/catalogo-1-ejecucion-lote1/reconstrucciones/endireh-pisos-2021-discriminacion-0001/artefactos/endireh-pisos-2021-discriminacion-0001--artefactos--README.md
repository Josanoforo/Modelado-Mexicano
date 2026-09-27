# Reconstrucción independiente congelada antes de revelación

Se leyeron exclusivamente /entrada y /raw como fuentes de reconstrucción. No se solicitaron resultados al preparador, no se consultó un clon del productor ni comparaciones, ni se usaron helpers del productor. Rótulo conservador: REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA, porque no se certifica que el entorno impida técnicamente leer otras reservas. No se inspeccionaron para comprobarlo.

La primera ejecución estadística se conserva: 286 llaves, 258 estimaciones publicables, 23 celdas educativas sin recodificación especificada y 5 estimaciones suprimidas por CV >0.30. No se declara concordancia con resultados esperados. Las menciones de concordancia en insumos.json son texto recibido sobre acceso, no una conclusión de esta reconstrucción.

## Ejecución

`OPENBLAS_NUM_THREADS=1 python3 reconstruir.py /raw`

Requiere Python 3 y numpy==2.3.5 (entorno usado: Python 3.14.4). El programa verifica los hashes originales antes del cálculo. Las copias de entrada son exactas. recibo.json conserva el SHA-256 del manifiesto recibido, su lista de entradas, los registros originales de insumos, hashes observados y hashes de cada entrada del ZIP. El ZIP, los microdatos y los PDF permanecen fuera del repositorio.

## Identidad y recodificación

La llave se conserva literalmente; no se usan los ordinales de `celda` para deducir categorías. Conducta, eje y segmento determinan cada cálculo. FD, páginas impresas 131–133: DOMINIO = U/C/R, CVE_ENT = 01–32, T_INSTRUM = A1/A2/B1/B2/C1/C2. El eje `pareja` usa estos códigos explícitos de instrumento: FD los identifica como situaciones conyugales; el método solicita el corte por esos mismos seis instrumentos. No se asignan identidades individuales ni se imputan códigos.

TSDem se une exactamente por ID_PER, verificando unicidad, presencia, sexo y edad válida de las elegibles. Se conservan identificadores solo en memoria. FD página 15 enumera NIV pero ni FD ni metodo.md determinan la agrupación de preescolar, estudios técnicos con diversos antecedentes y normal en los cuatro niveles pedidos. Se dejan las 23 llaves educativas sin cifras; tampoco se impone una definición independiente al grupo ninguno.

P8_2=1 es la elegibilidad. Se implementan los dos eventos de prueba y los tres de perjuicio tal como indican FD y sección 8.3 de cuestionarios A/B/C. Cada evento es conocido solo en 1/2; en las uniones cualquier 1 es positivo y solo todos 2 son negativo. Blanco, 9 y mezclas de 2/3 sin positivo quedan desconocidos. FAC_MUJ se usa sin normalizar.

## Remuestreo y límites de especificación

Se preservan 200 réplicas y semilla 20260923. La spec no fija generador, orden de consumo del RNG, variante exacta del bootstrap, convención de cuantiles ni divisor de varianza. Se implementa bootstrap ordinario de conglomerados: por cada estrato se sortean con reemplazo tantas UPM como contiene; estratos y pares (EST_DIS, UPM_DIS) ordenados lexicográficamente, PCG64 mediante Generator.integers, matriz de sorteos de forma (200, número de UPM). Las mismas réplicas sirven para todas las celdas. El marco es todo TB_SEC_VIII, antes de filtrar elegibilidad o dominio, incluyendo UPM sin casos del dominio. No se aplica corrección por población finita ni reescalamiento adicional. Estratos de una UPM conservarían esa UPM.

Cada réplica es la razón entre sumas ponderadas de positivos y conocidos, con multiplicidad de UPM. IC percentil con interpolación lineal, CV = desviación estándar de las 200 razones (ddof=1) / punto. No se ajusta el RNG a resultados externos. La tolerancia recibida 1e-10 no permite prometer igualdad exacta de IC con una implementación cuyo flujo aleatorio no fue especificado.

Se aplican n conocido >=100, al menos 5 UPM con conocidos, ancho <=0.20 y CV <=0.30 para p>0. Se guardan únicamente réplicas agregadas por celda, sin identificadores públicos. Cinco celdas no superan CV: el método prohíbe publicar su estimación. Entre los cuatro estados autorizados no existe SUPRIMIDO: se consignan sin cifras como NO-RECALCULABLE-DESDE-SPEC con motivo explícito de supresión; no es una falta de acceso ni una celda no intentada. Su decisión de publicación tampoco es exactamente reproducible desde la spec sin las convenciones RNG/varianza ausentes. soporte.tsv retiene n, UPM, denominador y CV; replicas.tsv retiene las réplicas agregadas. Esta distinción evita confundirlas con las 23 identidades educativas no determinadas.

## Integridad

SHA256SUMS cubre código, entradas y salidas, excepto sí mismo y .git. El commit congela también ese inventario. validacion.json registra verificaciones estructurales y casos de clasificación; no se volvió a ejecutar el estimador después de su primera ejecución. La entrega termina antes de revelación.
