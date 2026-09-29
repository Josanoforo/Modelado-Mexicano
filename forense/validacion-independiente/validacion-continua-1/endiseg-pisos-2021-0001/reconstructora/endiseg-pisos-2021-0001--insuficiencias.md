# Insuficiencias de la spec humana · CALC-ENDISEG-PISOS-2021-0001

Ninguna impidió estimar: las 424 llaves tienen punto e IC (`RECONSTRUIDO`/`CALCULADO`). Lo que sigue es lo que la spec no fija por completo; la lectura adoptada, con la frase que la motiva, está en `diagnostico.json` → `decisiones`.

## Todas las llaves (IC95)

1. **Secuencia exacta del generador.** La spec fija `PCG64(20260926)`, 2 000 réplicas y bloques de 50, pero no fija el orden de los sorteos (estratos, UPM, réplicas o bloques), la llamada (`integers`, `choice` o multinomial) ni el orden de las UPM dentro del estrato. Remite a `pisos_diseno.py` / `motor_pisos.py`, que no están en el paquete y no se describen en prosa. Sin eso, los extremos del IC sólo se pueden reproducir hasta el error de Monte Carlo, no bit a bit.
2. **Variante del bootstrap.** No dice si se sortean n_h o n_h−1 UPM por estrato, ni si hay reescalado de pesos (Rao-Wu). Se usó n_h sin reescalado.
3. **Base del recuento de estratos y UPM.** No dice si las UPM se cuentan sobre el universo filtrado o sobre cada dominio. Se usó el universo filtrado (44 178 personas, 513 estratos, 6 360 UPM, ningún estrato con UPM única).
4. **Definición de «réplica degenerada».** Se tomó como denominador replicado Σw* = 0 en el dominio. No hubo ninguna.
5. **Interpolación de percentiles.** No se fija; se usó `numpy.percentile` lineal.

## Grupo `lgbt` y eje `LGBT`

6. La derivada no dice qué hacer si una componente es UNO y la otra no está definida, ni si una es CERO y la otra no está definida. Se tomó UNO en el primer caso y fuera en el segundo.

## Grupo `identidad-no-cisgenero`

7. No se dice qué pasa si `P9_1` ∈ {1,2} y `P7_1` falta. No ocurre en el universo observado (`P7_1` siempre es 1 o 2).

## Correspondencia esquema ↔ spec

8. El esquema usa `SEXO`, `INDIGENA` y `AFRO` con segmentos `AL-NACER-*` y `AUTOADSCRITO-SI/NO`; la spec los llama `SEXO-AL-NACER`, `INDIGENA-AUTOADSCRITO` y `AFRO-AUTOADSCRITO` con códigos 1/2. Se tomaron como equivalentes (SI/HOMBRE = 1, NO/MUJER = 2).

## Identidad de entrada

9. El `sha256_entrada` indicado (`abb596fb…`) no es el sha256 de `paquete/datos/tmodulo.csv` (`2c387bb0…`). Se copió literalmente como ordena el encargo. El paquete no permite comprobar a qué objeto corresponde.
