# Insuficiencias de la spec humana

La spec bastó para fijar el **punto** de las 138 llaves (conductas, códigos UNO/CERO, universo, ejes, peso y razón Σw·y/Σw están en prosa). Lo que no fija afecta a los **extremos del IC** de las 138 llaves (todas con `estado_ic: CALCULADO`); las decisiones tomadas están en `diagnostico.json` → `decisiones_implementacion`.

## IC95, las 138 llaves

1. **Orden de consumo del generador** (D3). La spec da `numpy.PCG64(20261003)`, 2000 réplicas y «bloques de 50», pero no dice cómo se sortea dentro de un bloque: el orden de los estratos y de las UPM, si hay una llamada por estrato o una global, ni qué método del generador se usa (`integers`, `choice`…). Con la misma semilla, otro orden da réplicas distintas. Por eso los extremos del IC no se pueden reproducir bit a bit desde la prosa.
2. **Variante del bootstrap** (D1). Dice «bootstrap de UPM dentro de estrato» sin fijar cuántas UPM se sortean (n_h o n_h−1) ni si hay reescalado (Rao-Wu). Usé n_h sin reescalar.
3. **Definición de «réplica degenerada»** (D5). No se define. La tomé como réplica con denominador cero en el dominio. En este dato ninguna llave tuvo réplicas degeneradas.
4. **Método de percentil** (D6). «percentiles 2.5/97.5» no fija la interpolación. Usé la lineal por defecto de numpy.
5. **Receta y motor referidos por sha256** (`pisos_diseno.py`, `motor_pisos.py`) no están en el paquete. Su comportamiento solo cuenta en la medida en que la spec lo describe en prosa, y los puntos 1–4 no están descritos.

## Menores, sin efecto observado en este dato

- Deduplicación de `tsdem` por `ID_PER` (D7): no se dice qué fila conservar. No hubo duplicados.
- Estratos de UPM única (D2): no se dice cómo se tratan en el orden del generador. No hubo ninguno.
