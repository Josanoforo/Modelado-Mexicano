# Insuficiencias de la spec humana · CALC-ENSU-SERIE-0001

El punto (Σw·y/Σw) queda fijado por la spec y la lista cerrada. Lo que no alcanzan a fijar:

## 1 · IC95 bootstrap: las 7189 llaves

La spec §3 dice «bootstrap de UPM dentro de estrato, `PCG64(20260925)`, 1 000 réplicas,
percentiles 2.5/97.5, UPM única de certeza, contrato conservador (réplica degenerada → sin IC),
receta común por sha256». La receta (`tools/dominios/salud/pisos_diseno.py`) no está en el paquete,
y la prosa no fija:

- el tamaño del remuestreo por estrato (n_h de n_h, n_h−1 de Rao-Wu con reescalado, u otro);
- el orden en que se consume el generador (por réplica o por estrato; orden de estratos y de UPM),
  y si se reinicia en cada ola o se usa un solo flujo para toda la serie;
- el método de interpolación del percentil;
- qué cuenta como «réplica degenerada».

Adopté la lectura D01–D04 y D11 de `diagnostico.json`. Los extremos del IC son, por tanto, los de
**mi** implementación del bootstrap descrito. Salvo por el ruido de Monte Carlo no deberían
diferir de los de la receta, pero no se puede asegurar que sean idénticos byte a byte. Además,
si la receta usa n_h−1 reescalado, los intervalos cambian de forma sistemática. En ninguna celda
hubo réplicas degeneradas (con denominador 0).

## 2 · EDAD `60-MAS` y el código 97 (eje EDAD, todas las olas E1/E2)

La lista §4 dice «`60-MAS` = 60–96; 98/99 no especificada fuera del eje». El código 97
(«97 o más años», FD 2016) no está ni incluido ni excluido de forma expresa. Lo incluí en `60-MAS`
(D05). Afecta a pocas personas por ola (p. ej., 5 en 2016T1 y 9 en 2020T3; ver `edad_97` en
`diagnostico.json/por_ola`).

## 3 · Llaves duplicadas en la CB (2020T3, 2020T4)

La spec §1 solo regula la llave duplicada **en CS** (`G-CS-DUPLICADA`). En 2020T3 hay 140 filas
de CB con llave `UPM+VIV_SEL+H_MUD+R_SEL` repetida y en 2020T4 hay 82 (la CB es «una por
vivienda»). La spec no dice qué hacer con ellas. Las dejé en el marco (TOTAL y CIUDAD). Para
SEXO/EDAD se aplicó la regla de la spec: casi todas coinciden con llaves CS duplicadas y salen
del eje (279 y 161 personas con `G-CS-DUPLICADA`).

## 4 · Normalización de la llave CB→CS (eje SEXO/EDAD, E1/E2)

La spec no dice cómo comparar los componentes de la llave (los anchos de R_SEL/N_REN difieren
entre tablas). Recorté espacios y comparé sin ceros a la izquierda (D07). En 2017T1 ninguna
persona une con CS (`G-JOIN-SIN-CS` = 14497). El esquema no pide SEXO/EDAD de 2017T1, así que no
afecta a ninguna llave.

## 5 · Fuente de sexo/edad en 2020T3/T4

La CB de 2020T3/T4 trae `SEX`/`EDAD`, pero la lista §2 asigna E2 (hasta 2020T4) a la unión con CS.
Usé la CS (D06). Como control, en las 21843 personas unidas de 2020T3 la CB y la CS coinciden
por completo en sexo y edad.
