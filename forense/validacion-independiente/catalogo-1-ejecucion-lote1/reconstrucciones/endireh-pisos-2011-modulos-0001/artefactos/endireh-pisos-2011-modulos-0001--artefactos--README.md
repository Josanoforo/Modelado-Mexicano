# Reconstrucción ENDIREH 2011

REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA. Se usa este rótulo conservador porque no se certificó el aislamiento completo del entorno respecto de otras reservas. Sólo se consultaron el paquete `/entrada`, los insumos `/raw` y dependencias genéricas del sistema; no se buscaron ni se leyeron resultados esperados, código del productor, clon o comparación. No se contactó al preparador y no se solicita revelación. No se afirma concordancia con resultados de referencia.

## Entrega

- `reconstruccion.tsv`: una fila por llave recibida, en su orden original; punto e IC en proporciones, con 17 dígitos significativos.
- `replicas.tsv`: 200 proporciones por llave publicable; sin identificadores de mujeres, hogares o UPM.
- `recibo.json`: SHA-256 del manifiesto, su lista completa de entradas, hashes comprobados y entradas originales de los cinco insumos. Los valores `estado_acceso` dentro de las entradas originales son metadatos recibidos, no conclusiones de esta reconstrucción.
- `entrada/`: copia byte por byte del encargo, especificación, llaves, tolerancia y manifiesto recibidos.
- `inventario_zip.json`: nombres, tamaños y SHA-256 de cada miembro del ZIP, incluida la documentación interna, sin copiar su contenido al repositorio.
- `ejecucion.json`, `resumen.json`, `ejecucion.log`: entorno, diseño, comprobaciones de uniones, conteos y registro del cálculo.
- `SHA256SUMS`: hashes del código, las entradas y las salidas congeladas. Excluye su propio archivo y metadatos Git para evitar circularidad.

El SHA-256 de `/entrada/manifiesto.json` recibido es:

`a78bf4a6fb8d215c3fc7932f062f752c06d5a3f590ab236eb6ed524b5196171d`

## Ejecución

Dependencias instaladas: Python, NumPy 2.3.5, pandas 2.3.3 y olefile. Pandas se usa para lectura y uniones; el estimador usa NumPy. No se descargó ninguna dependencia. La instalación intentada de xlrd no fue posible por ausencia de red; se implementó un lector de celdas BIFF8 con olefile para consultar el FD. `pdftotext -layout` permitió leer los tres cuestionarios en archivos temporales ajenos al repositorio.

Desde este directorio, hacia una carpeta de salida nueva:

```sh
OPENBLAS_NUM_THREADS=1 python3 reconstruir.py --entrada /entrada --raw /raw --salida /tmp/repeticion-endireh
python3 -m unittest -v test_reconstruir.py
sha256sum -c SHA256SUMS
```

El programa rehúsa sobrescribir `reconstruccion.tsv`: se conserva el primer cálculo de estimandos. Un primer arranque se detuvo antes de cualquier estimación al exigir erróneamente que `CVE_ENT` apareciera también en el FD; el registro se conserva en `intento_01_sin_estimaciones.log`. Se corrigió esa comprobación: `CVE_ENT` es una columna explícita del CSV, no una identidad deducida de números de fila. No se modificó el estimador a partir de resultados de referencia.

## Identidades, fuentes y reglas

Cada llave se interpreta exclusivamente por las columnas `conducta`, `eje` y `segmento` recibidas; `celda` no se utiliza para asignar identidades. Los módulos A/B/C corresponden exactamente a las tablas indicadas. Las partes se unen por `CONTROL,VIV_SEL,HOGAR,R_SEL_M` con comprobación uno a uno, igualdad de claves e igualdad de columnas compartidas. Se comprueba que no haya identidades compartidas entre módulos. Edad y escolaridad provienen de TSDem, cambiando el nombre de N_REN a R_SEL_M; no se imputan uniones ausentes. No se reconstruye ninguna identidad a partir de valores esperados.

El FD verifica los códigos y variables: DOMINIO U/R; EDAD 97 significa 97 o más, 98/99 son desconocidos y no entran en cortes de edad; NIV se agrupa exactamente como la especificación. `media_superior` es la etiqueta entregada para los códigos 04/06/07. Entidad usa CVE_ENT del CSV, conservada como cadena de dos posiciones.

Los indicadores binarios son 1/0/desconocido. Una unión de ítems es positiva con al menos un sí y negativa sólo si todos son no. Se excluyen los códigos no aplicables. El salto 6.1=4 aporta no al año. C exige CP4_1=1/2 en los indicadores de pareja y permisos. Permiso mide código 1 (debe pedir permiso), frente a 2/3. Despojo se calcula aparte, sin atribuirlo sólo a familiares.

Las instituciones se calculan entre afectadas de pareja; las razones entre afectadas sin ayuda institucional y con alguna razón válida. La razón i sólo es positiva si la casilla i contiene su código i, verificado en el FD; un blanco pasa a no sólo en ese conjunto, y 99 sigue siendo desconocido. Los resultados de denuncia usan códigos 01 en 6.8 (válidos 01–10) y 1 en 2.12 (válidos 1–8), según el FD. C queda excluida del resultado de denuncia de pareja. No se elige una institución por una fecha inferida: 6.8 ya pregunta el resultado de la última visita a cada institución.

En 2.7/2.8 la segunda respuesta es opcional: una casilla vacía acompañada de otra válida no implica un segundo agresor/lugar desconocido. Un código explícito inválido sí impide declarar negativo el hecho, salvo que otra respuesta ya establezca positividad. En el año se vincula 2.9 con la misma posición de agresor/lugar. La prevalencia de dominio exige los doce hechos conocidos para declarar no. Ayuda y resultado externos utilizan sólo los actos 1–9: las listas de respuestas múltiples son positivas si contienen el código buscado, negativas si hay algún código válido sin el buscado y desconocidas si no hay ninguno válido. No se convierten los blancos de mujeres no afectadas en no. El resultado de atención sólo usa casillas de instituciones con ayuda válida.

Estas convenciones de listas múltiples y casillas opcionales son decisiones explícitas de operacionalización desde cuestionario/FD. La especificación humana no detalla todas las combinaciones de respuestas parciales; no se ha probado que coincidan con convenciones del productor.

## Muestreo y publicación

Se usa la razón de sumas ponderadas por FAC_PER en el conjunto conocido. El marco es la totalidad de pares EST_DIS,UPM_DIS observados en TViviend, incluyendo las UPM que no contribuyen al estimando. Para cada estrato de m UPM se extraen m UPM con reemplazo por réplica y se pondera por multiplicidad. Un estrato de una UPM conservaría su única UPM. Se reutiliza el mismo conjunto de 200 réplicas para todos los estimandos y cortes.

Semilla 20260923, `Generator(PCG64)`, estratos y UPM ordenados lexicográficamente. En cada estrato se generan las 200 filas de extracciones con `rng.integers(0,m,size=(200,m))`. Los percentiles 2.5/97.5 usan interpolación lineal; el CV usa desviación estándar de las réplicas con ddof=1 dividida por el punto. Para p=0 no se aplica el límite del CV. Se exigen n conocido >=100, al menos 5 UPM contribuyentes, ancho <=0.20 y CV <=0.30 si p>0.

La especificación fija semilla y tamaño, pero no algoritmo RNG, orden de llamadas, interpolación de cuantiles ni ddof. Por ello los IC pueden diferir incluso con NumPy 2.3.5 y no se promete la tolerancia de 1e-10 respecto de un cálculo desconocido. Se conservan los primeros IC obtenidos: no se intentó escoger un RNG para ajustar resultados.

Las cifras presentes llevan `RECONSTRUIDO`. Las celdas que la especificación obliga a suprimir no publican punto ni réplicas. Como el vocabulario solicitado no incluye un estado SUPRIMIDO, se utiliza `NO-RECALCULABLE-DESDE-SPEC` con motivo explícito `SUPRIMIDO-POR-SPEC`; significa que no se puede entregar una cifra bajo sus reglas de publicación, no que no se haya intentado calcular. Si hay una insuficiencia del método o identidad, ese mismo estado debe explicarla. `BLOQUEADO-POR-ACCESO` se reserva a acceso faltante y `NO-EVALUADO` a trabajo no intentado; no se usan para supresión.

## Congelación

El commit incluye código, pruebas, entradas textuales, recibo, inventario y números; excluye todos los raw, XLS y PDF, así como las extracciones temporales. SHA256SUMS permite verificar los bytes y Git conserva la instantánea previa a cualquier revelación. El hash del commit se comunica al cerrar la entrega, fuera de los archivos que forman ese mismo commit.
