# Recibo de reconstrucción independiente, previo a revelación

SHA-256 del `/entrada/manifiesto.json` recibido:
`011670fe1b4e2ceaff52c6dc4fd7f9814372d8dbe5aa457a24cd1d7b8ed68615`.

Se recibieron únicamente `/entrada` y `/raw`. Se conservaron sin modificación las siete entradas en `entradas/`, incluido el manifiesto original con su lista de seis archivos y hashes. Se verificaron todos esos hashes y los siete hashes declarados de insumos. `inventario_raw.json` conserva identificador, nombre de entrada declarado, ruta recibida, tamaño, URL declarada y SHA-256. `inventario_zip.json` conserva nombre, tamaño, CRC32 y SHA-256 de cada una de las 28 entradas del ZIP. Los archivos raw, CSV de microdatos, PDFs y sus transcripciones no forman parte del repositorio.

Etiqueta conservadora: **REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA**. La sesión dispone de herramientas generales de lectura; no se certifica aislamiento técnico respecto de eventuales reservas externas al paquete. No se buscó ni leyó ningún clon del productor, helper, resultado esperado, comparación o reserva. Solo se consultaron entradas, raw y utilidades/dependencias del sistema. No hubo solicitudes al preparador, revelación ni comparación con resultados esperados. No se afirma concordancia con resultados esperados. Los valores de estado de acceso en `entradas/insumos.json` son texto original recibido, no conclusiones de esta reconstrucción.

## Resultado congelado

`reconstruccion.tsv`: 138 llaves, todas con cifras y estado `RECONSTRUIDO`; incluye `motivo`, vacío cuando hay cifras. Ninguna celda requirió supresión. Se calculó el primer y único bootstrap de producción y se conservó su resultado. `replicas_publicables.tsv` contiene únicamente 500 proporciones agregadas por celda publicable, sin identificadores de personas, UPM ni estratos. `diagnostico_celdas.tsv` contiene únicamente n conocido y número de UPM con casos por celda.

Universo observado: 68 540 mujeres A1/A2, sin llaves vacías, duplicadas ni falta de enlace entre las tres tablas; factores positivos y edad dentro del filtro especificado. Todas se verificaron como mujeres mediante `SEXO=2` en TSDem. Marco de remuestreo: 16 846 UPM en 617 estratos, dos singleton. Los conteos y versiones se conservan en `auditoria.json`.

## Interpretación implementada y trazabilidad

- Identidad de mujer: unión exacta uno a uno por `ID_PER`, conservado como texto. No se asignaron identidades por posición, similitud o suposición. Las llaves de resultados se tomaron de `estimandos.tsv`; sus etiquetas conducta/eje/segmento determinan el cálculo, no el orden ni el número de celda.
- FD, tablas IV y XV: `T_INSTRUM=A1` es mujer casada/unida con pareja residente y `A2` con pareja ausente temporal. `DOMINIO=U/C/R` identifica urbano/complemento urbano/rural; entidad es `CVE_ENT`. Se tomaron de XV junto con factor y diseño. Escolaridad se toma de TSDem y se agrupa exactamente según el método.
- FD, IV `P4_11` y cuestionario A, pregunta 4.11: dinero que puede utilizar como quiera; 1 afirmativo y 2 negativo. FD, XV `P15_1AB_3` y `P15_1AB_7`, y cuestionario A, 15.1AB, incisos 3 y 7: decisiones sobre dinero propio/disponible y sobre gasto/economía, respectivamente. Se aplicaron exactamente 1/4/5 frente a 2/3; 6/7/blanco se excluyen del denominador. Las tres conductas son descriptivas y no equivalen a inferencias de dependencia, control o causalidad.
- Se aplicó **literalmente** el intervalo numérico de edad 15–120 de `metodo.md`. Existe una discrepancia semántica: el FD define EDAD=97 como 97 o más, 98 como edad no especificada en personas de 15 o más y 99 como no especificada. Hay 39 registros A1/A2 con 98 y ninguno con 99; el filtro literal los incluye y los asigna al intervalo numérico 60+. Esta es una consecuencia explícita del filtro recibido, no una afirmación de que su edad real sea 98 ni una imputación. Se deja registrada la limitación; no se cambió el método ni se calcularon variantes para seleccionar resultados.
- Proporción: suma de FAC_MUJ por respuesta positiva / suma de FAC_MUJ por respuesta conocida en la celda. El marco de UPM se forma antes de excluir factor, edad o respuestas. Las UPM sin casos válidos aportan cero al numerador y denominador del dominio.
- Bootstrap ordinario de conglomerados estratificado: para cada estrato con m UPM se extraen m UPM con reemplazo por réplica, con igual probabilidad. La multiplicidad multiplica las sumas ponderadas originales. No se añadieron corrección de población finita ni reescalado no especificados. Los singleton se incluyen una vez en todas las réplicas y no consumen números aleatorios.
- Semilla 20260923, 500 réplicas, un único flujo `numpy.random.Generator(PCG64)`. Estratos y UPM ordenados lexicográficamente como texto de anchura fija; por estrato, `integers(0,m,size=(500,m))`, con filas de réplica. Se comparte cada selección entre todas las celdas. El método no especifica RNG, algoritmo de extracción ni orden de consumo. Por ello no se garantiza identidad numérica de IC con otra implementación, especialmente a tolerancia absoluta 1e-10. No se ajustó el RNG ni se sustituyó ningún IC para aproximar valores externos.
- Percentiles 2.5/97.5 mediante interpolación lineal de NumPy (tipo 7). CV = desviación estándar de las 500 proporciones, divisor 499, dividida por el punto ponderado si p>0. Ambos detalles no están definidos en el método y se fijaron antes del primer cálculo. Filtros: n conocido ≥100, ≥5 UPM con casos, ancho ≤0.20, CV≤0.30 para p>0.

## Validación y reproducción

`verificar.py` comprueba las 138 llaves, recalcula cada punto con sumas directas de mujeres (sin agregación por UPM ni helpers de producción) y verifica los IC y filtros con las réplicas ya congeladas. No genera un segundo bootstrap. `verificacion.json` guarda el resultado. Se comprobaron además unicidad de uniones, factores, sexo, tamaño del remuestreo por estrato y rango de proporciones en el código de producción.

Dependencias: Python 3.14.4, NumPy 2.3.5 y pandas 2.3.3. Lectura CSV Latin-1; códigos como texto, sin perder ceros iniciales. Ejecución desde cualquier directorio:

```sh
OPENBLAS_NUM_THREADS=1 python3 /work/reconstruccion/reconstruir.py --raw /raw --salida /tmp/reproduccion-endireh
OPENBLAS_NUM_THREADS=1 python3 /work/reconstruccion/verificar.py
```

`SHA256SUMS` congela código, entradas, recibo, inventarios, auditorías y cifras; se excluye a sí mismo para evitar autorreferencia. El commit inicial congela también ese archivo. El identificador del commit se entrega al finalizar; no se inserta dentro de su propio contenido. No se solicitará revelación en esta sesión.
