# Insuficiencias de la spec humana · CALC-ENASEM-ESCOLARIDAD-2021-0001

Punto (14 llaves): ninguna. La spec fija sin ambigüedad material el universo, el peso, las listas UNO/CERO sobre `YRSCHOOL`, los ejes y la razón ponderada Σw·y/Σw.

IC95 (las 14 llaves, mismo motor): la spec nombra el método (bootstrap de UPM dentro de estrato, `PCG64(20260930)`, 2000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato conservador), pero la prosa no alcanza a fijar lo siguiente. Por eso un IC que coincida bit a bit con el del motor original (`motor_pisos.py`, que no está en el paquete) depende de supuestos:

1. **Esquema de remuestreo.** No dice si en cada estrato se sortean n_h o n_h−1 UPM, ni si se aplica el reescalamiento Rao-Wu a los pesos. Usé n_h con reemplazo, sin reescalar.
2. **Consumo del generador.** No dice en qué orden se piden los números aleatorios (por bloque, estrato o réplica), ni cómo se ordenan las UPM, ni qué llamada de numpy se usa (`integers`, `choice`, multinomial). Tampoco dice cómo intervienen los «bloques de 50» en la secuencia aleatoria. Mi elección está en `diagnostico.json` → `decisiones`.
3. **Marco del bootstrap.** No dice si el juego de UPM que se remuestrea es el marco universo+diseño completo, compartido por todas las llaves, o si se arma por conducta o dominio después de excluir `YRSCHOOL` en blanco. Usé un marco común: universo con diseño válido, antes de quitar los blancos.
4. **Interpolación de percentiles.** No la fija. Usé la opción por defecto de `numpy.percentile` (lineal).
5. **«Réplica degenerada».** No la define. Usé: denominador de réplica igual a 0 o valor no finito. No se observó ninguna.
6. **UPM de certeza.** No dice cómo se trata una UPM única en su estrato. Usé multiplicador 1. No aplica al dato: los 4 estratos tienen más de una UPM.
