# Insuficiencias de la spec humana · CALC-ENADID-COLA-2018-0001

Los puntos (razón ponderada Σw·y/Σw) de las 100 llaves quedan fijados por la spec sin ambigüedad material. Las insuficiencias afectan sobre todo al **IC95**. La de `niv` = 99 (punto 5) podría mover puntos del marco MUJERES si se leyera de otra forma.

## Todas las llaves (IC95)

1. **Variante del bootstrap.** La spec dice «bootstrap de UPM dentro de estrato» y «UPM única del estrato = de certeza». No fija cuántas UPM se sortean por estrato (n_h o n_h−1), ni si se reescalan los pesos (Rao-Wu). Tampoco dice cómo trata un estrato de certeza. Se usó n_h de n_h, sin reescalar, y el estrato de UPM única queda fijo (D1). En este dato no hay estratos de UPM única.
2. **Orden de consumo del generador.** Están fijados `PCG64(20261001)`, 2000 réplicas y bloques de 50. No se fijan: el orden de estratos y UPM, la forma de cada sorteo, si hay un generador por marco o uno compartido, ni el orden entre marcos. Las funciones del motor (`motor_pisos.py`) no se describen en prosa. Los extremos del IC no son reproducibles bit a bit (D2).
3. **Tipo de intervalo.** No se dice si el IC95 es percentil, normal con EE bootstrap u otro. Se usó percentil 2.5/97.5 con interpolación lineal (D3).
4. **«Réplica degenerada».** La spec no la define. Se tomó como denominador ponderado del dominio igual a 0 en la réplica (D4). Esto afecta a 6 llaves `JEFATURA-FEMENINA-CON-MIGRANTE-VARON-2018-ENTIDAD-{03,09,15,19,23,31}`, que quedan `NO-IDENTIFICADA`. Con otra variante de bootstrap o de consumo del generador, el número de réplicas degeneradas y el conjunto de llaves afectadas pueden cambiar.

## Grupo ESCOLARIDAD (8 llaves)

5. **`niv` = 99.** Aparece en 29 filas y queda fuera del rango del FD (00…11) y de la agrupación de la spec. La spec no dice si esas filas se excluyen del eje o del marco. Se excluyeron solo del eje ESCOLARIDAD (D5). Si se excluyeran del marco entero, cambiarían los puntos de TOTAL, EDAD y TAMLOC del marco MUJERES, no los de ESCOLARIDAD.

## Grupo TOTAL-TODOS (4 llaves)

6. **Eje TOTAL.** El §3 de la spec no lo enumera. Se interpretó como el agregado de toda la subpoblación de la conducta (D9).
