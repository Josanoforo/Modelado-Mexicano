# Insuficiencias de la spec humana · CALC-PEW-RELIGION-2024-0001

Ninguna impidió estimar: las 44 llaves tienen punto e IC calculados. Estos son los puntos que la spec no alcanzó a fijar y que resolví con una decisión propia (ver `diagnostico.json` → `decisiones`). Todos son de la inferencia, no del punto.

## Todas las llaves (IC95)

1. **Algoritmo exacto del bootstrap.** La spec dice «bootstrap ponderado de entrevistas», `PCG64(20261002)`, 2000 réplicas y «bloques de 50», pero la receta vive en `pisos_diseno.py`/`motor_pisos.py`, que no están en el paquete. No fija:
   - cómo se sacan los índices en cada bloque (usé `rng.integers(0, n, size=(50, n))`, o sea multiplicidades de un remuestreo n-de-n);
   - si hay reescalado de pesos (por ejemplo Rao-Wu con n-1) o multiplicadores de otro tipo;
   - si el generador se vuelve a sembrar por llave, eje o conducta, o si se consume en una sola secuencia (usé una misma matriz de réplicas para todas las llaves);
   - el método de percentil (usé el lineal de numpy).

   Cualquier otra lectura cambia los extremos del IC, pero no el punto.
2. **Qué es una «réplica degenerada».** La spec no la define. Tomé la réplica con denominador ponderado igual a 0. No hubo ninguna en las 44 llaves.
3. **Unidad de remuestreo frente al universo.** La spec dice que el universo «se aplica aparte, sobre el diseño ya válido». Lo leí así: se remuestrean las 1042 filas con peso válido y el universo 18–97 entra como indicador de dominio. Otra lectura, remuestrear solo las 1039 filas del universo, daría un IC distinto.

## Umbral de soporte

§5 menciona ramas «con soporte / sin soporte», pero no da ningún umbral numérico. No apliqué ninguno y no suprimí celdas.

## CATOLICO / SIN-RELIGION

El texto exacto de la pregunta en México es [TEXTO-DEL-MEDIDOR, NO-VERIFICADO-AQUÍ] según la propia spec. Eso no afecta el cálculo, porque los códigos sí están fijados. La advertencia de Pew «NOT FOR POINT ESTIMATES» se mantiene, como lo declara la spec.
