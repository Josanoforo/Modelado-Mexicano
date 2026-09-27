# Reconstrucción independiente congelada antes de revelación

Se recibieron únicamente `/entrada` y `/raw`. Se implementó el método con Python,
NumPy y pandas, sin helpers del productor, sin consultar resultados esperados y
sin contactar al preparador. No se solicitó revelación ni se realizó comparación.
No se certifica aislamiento del sistema más allá de las rutas efectivamente usadas;
no se buscaron clones, comparaciones ni reservas.

## Entrega y límite de identidad

`reconstruccion.tsv` contiene las 96 llaves recibidas, en su orden original. Todas
están en estado `NO-RECALCULABLE-DESDE-SPEC`, con cifras vacías y motivo explícito:
no existe un campo ni una regla que asigne cada llave al periodo vida o reciente.
Por ejemplo, las celdas 0 y 50 tienen ambos eje nacional y segmento MX. No se
interpretó el número de celda ni la ausencia de algunas celdas como identidad.
La misma carencia afecta incluso a segmentos que aparecen una sola vez.
No falta acceso a los insumos recibidos.

`calculos_sin_asignar.tsv` conserva la primera ejecución estadística completa:
100 combinaciones identificadas explícitamente por periodo, eje y segmento, sin
llaves del productor. Son 96 publicables y 4 suprimidas. Las celdas suprimidas no
contienen punto ni IC y detallan el criterio incumplido. `replicas_publicables.tsv`
contiene únicamente las 200 estimaciones agregadas de cada celda publicable.
Estas tablas auxiliares no resuelven la identidad de las llaves solicitadas.

## Decisiones de implementación

Se consultaron FD y cuestionario A, sección VII, desde los PDF recibidos; sus
extracciones temporales permanecen fuera del repositorio. FD documenta DOMINIO
U/C/R, T_INSTRUM A1/A2/B1/B2/C1/C2, NIV y variables de diseño. El cuestionario
indica que 7.8 se pregunta solo cuando 7.2=1 y el acto de 7.6=1. Se aplica la
imputación a 4 de actos 7.6=2 según metodo.md. Los blancos permanecen desconocidos;
un positivo determina la unión. Se impide reciente conocido si vida es desconocida.

Se une TB_SEC_VII con TSDem por ID_PER, comprobando unicidad, correspondencia
completa y sexo femenino. Se filtra edad 15–120 y FAC_MUJ positivo. Denominador:
suma de factores de mujeres elegibles con unión conocida. Numerador: suma de
factores de esas mujeres con unión positiva. Se usan proporciones, no porcentajes.

El marco de remuestreo contiene todas las UPM presentes en TB_SEC_VII, antes de
filtrar dominios o elegibilidad. La identidad de UPM es (EST_DIS, UPM_DIS). En cada
réplica se extraen n_h UPM con reemplazo dentro del estrato de tamaño n_h y se
multiplican sus totales completos por su multiplicidad. Se comparte el sorteo entre
dominios y periodos. Los estratos singleton se autorremuestrean sin consumo RNG;
no se observaron singletons. No se aplicó reescalamiento ni corrección de población
finita, al no estar especificados. UPM con casos significa UPM con mujeres del
dominio y respuesta conocida, no solo respuestas positivas.

Se conserva semilla 20260923 y B=200. La spec no identifica motor RNG, orden de
sorteos, método de interpolación percentil ni convención del estimador de CV.
Se fijan PCG64 de NumPy; orden réplica→estrato→UPM lexicográfico; percentil lineal;
CV=desviación estándar muestral de las 200 réplicas / punto, cuando punto>0.
Estas decisiones están registradas en ejecucion.json. No es posible conocer una
diferencia efectiva respecto al RNG del productor sin revelación. La tolerancia
recibida 1e-10 no permite suponer equivalencia de IC entre motores o secuencias.
No se ajustó semilla ni cifras para obtener resultados ajenos.

## Reproducción e integridad

Desde este directorio:

```sh
OPENBLAS_NUM_THREADS=1 python3 reconstruir.py
python3 verificar.py
sha256sum -c SHA256SUMS
```

Las versiones exactas y conteos se registran en ejecucion.json. Las pruebas
cubren desconocidos, saltos, elegibilidad, cobertura de llaves, supresión y
coherencia de los intervalos con las réplicas conservadas. No usan valores del
productor. `validacion.txt` registra su ejecución.

`entrada/` conserva byte por byte los siete archivos recibidos. `recibo.json`
conserva SHA-256 del manifiesto recibido, su lista íntegra de entradas, las rutas
originales declaradas de los insumos, sus hashes observados y los hashes de las
28 entradas del ZIP. SHA-256 del manifiesto recibido:
`74b50525814ef0647880e161862d332826abe91304e8a17661035b8eadec1472`.
Los estados históricos de acceso dentro de insumos.json se preservan literalmente;
no constituyen una declaración de concordancia de resultados de esta reconstrucción.

SHA256SUMS congela código, entradas y resultados; excluye a sí mismo para evitar
autorreferencia. El commit Git fija también ese archivo. Raw y PDF no se copian
ni se incluyen en el commit. El identificador del commit se obtiene con
`git rev-parse HEAD`. El trabajo termina tras congelar, sin solicitar revelación.
