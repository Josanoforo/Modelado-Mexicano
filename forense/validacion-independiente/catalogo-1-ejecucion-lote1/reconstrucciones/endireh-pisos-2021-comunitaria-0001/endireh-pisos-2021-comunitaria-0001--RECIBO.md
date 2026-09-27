# Recibo de reconstrucción independiente, anterior a revelación

SHA-256 de `/entrada/manifiesto.json` recibido:
`e8a13d0d4e8658525cf9b88fc02f976b7fac8fe44b1ad88f247dff63a4cf3f2b`.

Se conserva el manifiesto íntegro y su lista de entradas en `entrada/manifiesto.json`; también se incorpora literalmente en `salida/ejecucion.json`. Se comprobaron todos sus hashes y los siete hashes de los insumos. Se incluyen copias completas de `/entrada` y `/raw` en el commit. `SHA256SUMS` congela todos los archivos de entrega salvo el propio listado y los metadatos de Git; el commit congela también ese listado.

Rótulo conservador: **REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA**. No se consultaron resultados esperados, código del productor, comparaciones ni reservas, ni se contactó al preparador. Solo se usaron las entradas recibidas, las bibliotecas genéricas y herramientas del sistema. El perfil del entorno permite lectura fuera de las entradas; no se certifica aislamiento técnico respecto de posibles reservas, ni se exploraron para comprobarlo. Este rótulo no afirma que se haya visto ningún resultado esperado. No se solicitó revelación.

## Entrega y faltante de identificación

`salida/reconstruccion.tsv` contiene las 100 llaves originales, en el orden recibido, con las cinco columnas solicitadas. Su estado es `FALTANTE_HORIZONTE_EN_LLAVE` y los tres valores están vacíos. `estimandos.tsv` no contiene columna de horizonte; cada par eje/segmento se repite en dos celdas. Por ejemplo, nacional/MX está en las celdas 0 y 50. Ni `metodo.md` ni los cuestionarios ni FD vinculan esos índices de salida con vida o reciente. Asignar 0–49 a vida y 50–99 a reciente sería una conjetura. No se hizo esa asignación.

La implementación estadística está ejecutada y sus primeros números se conservan en `salida/estimaciones_por_horizonte.tsv`: 50 dominios para vida y 50 para reciente. No son una sustitución de la identificación faltante. Las 100 celdas pasaron los filtros de publicación. `salida/replicas_publicables.tsv` conserva únicamente proporciones agregadas de esas celdas; `salida/supresion.tsv` documenta el estado. No se exportaron identificadores de mujeres ni de UPM como resultados. Los insumos crudos recibidos se archivan íntegros para reproducibilidad.

## Decisiones de implementación fijadas antes de revelación

- Se leen los CSV con Latin-1, preservando ceros iniciales. Se une `TB_SEC_IX` con edad, escolaridad y sexo de `TSDem` por `ID_PER`, validando unicidad y correspondencia completa. Se seleccionan instrumentos A1/A2/B1/B2/C1/C2, mujeres, edad 15–120 y factor positivo. El marco contiene 110127 mujeres, 17744 UPM y 617 estratos; no hay singleton.
- Las uniones siguen literalmente la especificación, incluido el salto de 9.3 y la propagación de vida desconocida. Hay 110127 respuestas conocidas de vida y 110114 recientes. El cuestionario A, sección IX, exige preguntar 9.3 solo ante sí en 9.1. FD sección IX confirma códigos comunes a A/B/C. `DOMINIO` determina localidad; `T_INSTRUM`, condición; `CVE_ENT`, entidad. La escolaridad sigue exactamente los grupos NIV del método.
- Se identifica cada UPM por el par `(EST_DIS, UPM_DIS)`. Se ordenan estratos y UPM lexicográficamente. Con un único flujo NumPy `Generator(PCG64(20260923))`, se recorre primero réplica y luego estrato, seleccionando con reemplazo tantas UPM como contiene el estrato. Se reutiliza el mismo remuestreo para todas las celdas y ventanas. UPM ajenas a cada dominio conservan contribución cero. Un singleton se seleccionaría a sí mismo.
- Punto: suma de pesos de mujeres positivas dividida por suma de pesos de mujeres con respuesta conocida del dominio. Cada réplica calcula de nuevo esa razón con las multiplicidades de las UPM. No se aplica corrección de población finita ni reescalamiento adicional, no especificados.
- IC: percentiles 2.5 y 97.5 con interpolación lineal (tipo 7). CV: desviación estándar muestral de las 200 proporciones (`ddof=1`) dividida por el punto si es positivo. «UPM con casos» se interpreta como UPM con al menos una mujer positiva. Se aplican todos los umbrales del método; una réplica sin denominador impide publicación. No ocurrió en las celdas publicadas.

La especificación no identifica RNG, versión, orden de extracciones, algoritmo de percentil ni convención de desviación estándar. Las decisiones anteriores están explícitas y congeladas, pero no se afirma identidad de los IC con otra implementación. La tolerancia entregada de 1e-10 no elimina las diferencias entre flujos aleatorios. No se ajustó la semilla, no se seleccionó otra ejecución y no se sustituyeron intervalos. Hubo un intento de lectura fallido por codificación UTF-8 antes de producir resultados estadísticos; se corrigió a Latin-1. También se configuró la ruta de BLAS/LAPACK para cargar las bibliotecas genéricas del sistema.

## Reproducción y comprobación

Código: `reconstruir.py`; ejecución: `./ejecutar.sh`. Dependencias usadas: Python 3.14.4, NumPy 2.3.5 y pandas 2.3.3. La ejecución rechaza sobrescribir una carpeta `salida` existente. Para reproducir, usar una copia separada de la entrega sin esa carpeta. El archivo `salida/ejecucion.json` registra versiones, semilla, marco y hashes.

Se ejecutó `verificar.py`: pruebas sintéticas de negativos estructurales, desconocidos y prioridad de positivos; integridad de las 100 llaves; límites y ancho de los intervalos; ausencia de cifras en celdas suprimidas; 200 réplicas por celda publicable. Resultado satisfactorio. No se efectuó comparación externa.

La reconstrucción numérica por horizonte queda congelada. La reconstrucción por llave queda incompleta por el faltante de identificación, documentado sin solicitar resultados ni aclaraciones al preparador. Se termina antes de revelación.
