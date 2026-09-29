# Insuficiencias de la spec humana · CALC-ENSU-PISOS-0001

Ninguna llave quedó sin estimar por falta de método, acceso o dato: las 5445 llaves se reconstruyeron con IC calculado. Lo que sigue es lo que la spec no fija y que resolví con una decisión documentada (ver `diagnostico.json:decisiones`). Afecta a los IC y, en un caso, al punto.

## Todas las llaves (solo el IC95)

1. **Esquema de bootstrap.** La spec dice «bootstrap de UPM dentro de estrato» pero no fija cuántas UPM se sortean por estrato (n_h o n_h−1), ni si hay reescalamiento de pesos (Rao-Wu) o no. La «receta común por sha256» (`tools/dominios/salud/pisos_diseno.py`) no está en el paquete. Usé el bootstrap ingenuo: n_h con reemplazo y sin reescalar.
2. **Consumo del generador.** `PCG64(20260925)` fija la semilla, pero no fija:
   - el orden de los estratos y de las UPM;
   - la forma de los sorteos;
   - si se usa un generador por ola, por celda o uno global.

   Cualquier otra elección da réplicas distintas. Usé un generador por ola, con estratos y UPM en orden lexicográfico y `integers(0, n_h, size=(1000, n_h))` por estrato. Las réplicas se comparten entre celdas, conforme a «mismo marco, semilla y réplicas».
3. **Percentiles.** El método de interpolación no está fijado. Usé el lineal de numpy.
4. **«Réplica degenerada».** No está definida. La tomé como una réplica con denominador ponderado 0 en el dominio. Ninguna celda la presentó.
5. **«UPM única de certeza».** La interpreté como multiplicidad 1 fija. Solo afecta a 2024T1, que tiene 28 estratos con una sola UPM.

## Llaves EDAD `60-MAS` (2024T1, 2025T3, 2025T4; todas las conductas): punto e IC

La lista §4 define `60-MAS` = 60–96 y excluye solo 98/99. El dato trae EDAD = 97 («97 o más años» en el FD): 10, 7 y 4 personas por ola, respectivamente. Decidí incluirlas en `60-MAS`. La lectura literal (60–96) las dejaría fuera del eje.

## Menores (sin efecto numérico observado)

- En 2024T1, 2 pares de filas CB comparten la llave UPM/VIV_SEL/H_MUD/R_SEL. La regla `G-CS-DUPLICADA` es para el join CS, que no existe en E3. Las conservé.
