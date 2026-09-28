# Reconstrucción independiente ENDIREH 2016

Se recibieron únicamente `/entrada` y `/raw`. No se accedió a resultados esperados, no se solicitó revelación ni se contactó al preparador. El commit que contiene este archivo congela el código y los números anteriores a cualquier revelación.

`recibo.json` conserva el SHA-256 del manifiesto original, versiones de bibliotecas, convenciones de remuestreo y hashes de salidas. `inventario.json` conserva las rutas, entradas y hashes de todos los insumos y miembros del ZIP. `entrada/` preserva las siete entradas originales. No se versionan raw, PDFs ni textos extraídos de PDFs.

## Resultado y limitación de identidad

`reconstruccion.tsv` contiene las 92 llaves originales, todas con estado `NO-RECALCULABLE-DESDE-SPEC`, motivo explícito y cifras vacías. `estimandos.tsv` repite dos veces cada uno de los 46 dominios y no contiene ventana temporal. El método define P13_1 y P13_3, pero no establece correspondencia entre estas ventanas y las llaves/celdas. El índice y el orden no acreditan identidad. No se asignan los cálculos a ninguna llave.

Se implementó y ejecutó el método para ambas ventanas con nombres explícitos en `calculos_por_ventana.tsv`: 92 estimaciones agregadas y sus intervalos. Esos números no son reconstrucciones identificadas de las llaves solicitadas. `replicas_agregadas.tsv` conserva las 46 000 réplicas por ventana, eje y segmento, sin identificadores individuales ni UPM. Las 92 estimaciones pasan los filtros de publicación implementados. `auditoria.json` conserva los conteos de procesamiento.

## Implementación y decisiones reproducibles

Se leen directamente del ZIP TB_SEC_XIII.csv y TSDem.csv; se verifica unión uno a uno por ID_MUJ y correspondencia completa. Se restringe a T_INSTRUM A1/A2, factor positivo y edad 15–120. Para cada ventana se usa la razón entre suma de factores de respuestas positivas y suma de factores de respuestas conocidas. Los nueve actos se unen sin sumar prevalencias. Una respuesta positiva prevalece sobre otros actos desconocidos; solo nueve respuestas 4 producen cero. En P13_3, cada acto con P13_1=4 se recodifica a 4 y toda unión con P13_1 desconocida queda desconocida.

El marco de remuestreo comprende todas las UPM de A1/A2 antes de excluir por edad, factor, respuesta o dominio. Se identifican UPM por el par EST_DIS/UPM_DIS. Se ordenan ambos campos lexicográficamente. Con NumPy PCG64 y semilla 20260923 se generan, por estrato, 500 vectores multinomiales de multiplicidad, cada uno de tamaño igual al número de UPM y probabilidades iguales. Es equivalente a extraer ese número de UPM con reemplazo. Se usan las mismas multiplicidades en todas las celdas y ventanas, incluyendo contribuciones cero. El estrato singleton siempre tiene multiplicidad uno.

IC: percentiles lineales 2.5/97.5 de las razones replicadas; error estándar: desviación de las 500 razones con ddof=1; CV=error estándar/proporción para p>0. Se interpreta «UPM con casos» como UPM con respuesta conocida que contribuye al denominador. Se exige n≥100, UPM≥5, ancho≤0.20 y CV≤0.30 cuando p>0. Si una réplica carece de denominador se suprime la estimación; no se descartan réplicas silenciosamente. Las cifras principales de celdas suprimidas se dejarían vacías con motivo; se conservan las réplicas agregadas según lo pedido en el método.

El método no especifica generador pseudoaleatorio, orden de consumo, interpolación del percentil, ddof ni el sentido de «casos» para contar UPM. Las convenciones anteriores hacen reproducible esta implementación, pero la semilla por sí sola no garantiza identidad numérica a tolerancia absoluta 1e-10 con otra implementación. La tolerancia recibida está preservada; no puede evaluarse concordancia sin resultados esperados y sin identidad temporal explícita.

## Documentación consultada

- `metodo.md` y `estimandos.tsv` originales.
- FD Excel: hoja TB_SEC_XIII, filas 25 (A1/A2), 33–90 (ventana histórica y actos); P13_3_1 y siguientes (ventana reciente); hoja TSDem para EDAD/NIV y hoja TB_SEC_III para T_INSTRUM.
- Cuestionario A, sección XIII, página impresa 32: encabezados 13.1/13.3 y aplicación de 13.2/13.3 solo a actos con códigos 1, 2 o 3 en 13.1.
- FD PDF interno del ZIP, cuyo hash se verifica contra el preregistro. Los demás cuestionarios enumerados están disponibles y sus hashes fueron verificados; no se necesitan para la población A1/A2.

## Ejecución y verificación

Desde este directorio, con `/entrada` y `/raw` montados:

```sh
OPENBLAS_NUM_THREADS=1 python3 reconstruir.py
python3 verificar.py
```

Las versiones exactas usadas constan en el recibo. Las pruebas verifican desconocidos, positivos y saltos, cobertura intacta de llaves, ausencia de cifras asignadas sin identidad, cobertura de réplicas, umbrales y hashes. El historial Git identifica la congelación; no se incluye el hash del commit dentro del propio commit para evitar autorreferencia.
