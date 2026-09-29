# Insuficiencias de la spec humana · CALC-LATINOBAROMETRO-COLA-2023-0001

Los puntos (razón ponderada Σw·y/Σw) de las 68 llaves quedan fijados por la spec sin ambigüedad material. Las insuficiencias afectan solo a los IC95 (las 68 llaves, todas las conductas y ejes):

1. **Esquema de remuestreo.** La spec dice «bootstrap ponderado de entrevistas… cada entrevista es su propia UPM, un solo estrato», pero no dice si se extraen n o n−1 entrevistas por réplica (Rao-Wu), ni si hay reescalado de pesos. Supuse n con reemplazo y sin reescalado (D1).
2. **Consumo del generador.** Fija `PCG64(20260928)`, 2000 réplicas y «bloques de 50», pero no dice qué llamada de numpy genera los índices o conteos (integers / choice / multinomial), en qué orden ni qué significan los bloques. Tampoco dice si las réplicas se comparten entre llaves o si se vuelve a sembrar por conducta o eje. Elegí `rng.integers(0, n, (50, n))` por bloque, con un solo flujo compartido por las 68 llaves (D2). Otra lectura da IC distintos a nivel de dígitos.
3. **Percentiles.** «percentiles 2.5/97.5» no fija el método de interpolación. Usé el lineal de numpy (D3).
4. **Réplica degenerada.** No define «degenerada». Tomé «denominador del dominio igual a 0 en la réplica» (D4). En esta corrida no ocurrió en ninguna llave.

La spec fija el control de ORO-CONFIA-GOBIERNO (debe reproducir el CONFIA-GOBIERNO del CALC de PISOS) contra un valor sellado que no está en el paquete. Esta sesión no puede verificarlo.
