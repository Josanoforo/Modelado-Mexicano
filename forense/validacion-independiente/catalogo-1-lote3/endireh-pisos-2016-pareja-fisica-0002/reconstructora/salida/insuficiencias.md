# Insuficiencias de la spec humana

Las 92 llaves se estimaron. Ninguna quedó bloqueada: todas las columnas que pide el método están en la lista autorizada. Hay puntos que `metodo.md` no fija de forma unívoca. Resolverlos de otra manera cambia los números. La decisión que tomé en cada caso está en `diagnostico.json` → `decisiones`.

## Todas las llaves: IC95 (puntos 1 a 5)

1. **Esquema de bootstrap.** La spec dice «Se remuestrean todas las UPM A1/A2 por estrato». No fija cuántas UPM se extraen por estrato (n_h o n_h−1). Tampoco dice si se aplica el reescalamiento Rao-Wu o una corrección de varianza. Usé extracción ingenua de n_h con reemplazo y multiplicador igual al número de veces que sale cada UPM. Es la lectura compatible con «Singleton autorremuestreado aporta varianza cero». Con Rao-Wu m=n_h−1 un singleton no estaría definido. El resultado real tiene 1 estrato singleton.
2. **Generador y orden de extracción.** La spec da la semilla 20260923. No dice el generador (`default_rng`/PCG64, `RandomState`/MT19937 u otro) ni el orden en que se recorren réplicas, estratos y UPM. Los extremos del IC dependen de esto. La combinación que usé está documentada. Otra implementación con la misma semilla no reproducirá los mismos extremos bit a bit.
3. **Definición del percentil.** La spec dice «IC percentil 2.5/97.5» sin indicar el método de interpolación. Usé tipo 7 (lineal).
4. **Conjunto de «UPM A1/A2».** Tomé las UPM_DIS con al menos una mujer del universo final (A1/A2, factor>0, edad 15–120): 17 174 UPM en 619 estratos. La spec no dice si cuentan las UPM que solo tienen mujeres B/C. Incluirlas no cambia nada, porque aportarían cero al numerador y al denominador.
5. **Réplicas con denominador cero en el dominio.** La spec no dice cómo tratarlas. Las descarté. En esta corrida no hubo ninguna.

## Llaves de edad (#1–#4 y #47–#50)

6. **EDAD=98.** El FD la define como «Edad no especificada en personas de 15 años o más». El filtro «edad 15–120» la admite numéricamente, pero no se puede asignar a ningún grupo de edad. Dejé esos 96 casos en el universo y en los demás ejes, y fuera de los cuatro grupos de edad. Los 6 casos con EDAD=97 («97 o más») van a 60+.

## Llaves de escolaridad (#5–#8 y #51–#54)

7. **NIV=99 y NIV=1.** NIV=99 (no especificado, 3 casos) no está en ninguna categoría de la spec, así que queda fuera del eje de escolaridad. NIV=1 (preescolar) va a «básica» según la lista literal «1–3/5–6».

## Llaves de ventana `desde_octubre_2015` (#46–#91)

8. **Consistencia 13.1/13.3.** Hay 1 166 pares de actos con 13.1=3 («una vez») y 13.3=2 («pocas veces»). La spec no pide ninguna depuración, así que 13.3 se usa tal cual (cualquier 1–3 cuenta como positivo). La recodificación por salto y la regla de desconocido se aplicaron como están escritas.
9. **Acto con 13.1∈{1,2,3} y 13.3 en blanco o 9.** El acto reciente queda desconocido. La unión reciente es 1 si algún otro acto reciente es positivo, y desconocida si no hay ninguno positivo y no todos valen 4. Es la aplicación literal de la regla de unión.

## Regla de publicabilidad (diagnóstico)

10. **«≥5 UPM con casos».** La spec no aclara si «casos» son mujeres del dominio con respuesta conocida o mujeres con resultado positivo. Para la regla usé las primeras. Las dos cifras se informan. El CV usa la desviación estándar de las réplicas con ddof=1, y la spec no fija el ddof. Las 92 celdas cumplen la regla.

## Comparación con 2021

11. El último párrafo de `metodo.md` habla de la comparación con 2021. Ninguna de las 92 llaves la pide, así que no se implementó nada al respecto.

## Identidad

12. `sha256_entrada` se copió del encargo tal como venía. El paquete no dice sobre qué bytes se calcula, así que no pude verificarlo. En `diagnostico.json` sí se verificaron los hashes de `manifiesto.json`.
