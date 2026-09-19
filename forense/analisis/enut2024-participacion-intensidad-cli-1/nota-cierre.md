# Cierre — participación e intensidad del cuidado, ENUT 2024

## Resultado

En el agregado CON_CP, 51.85% de las personas participa en al menos una de
las cuatro actividades delimitadas; la media es 11.12 horas semanales y 21.44
horas entre participantes. Frente a hombres, las mujeres presentan +8.19 pp
de participación, +8.37 horas de media y +12.97 horas entre participantes;
los tres IC95 de las diferencias excluyen cero.

| tramo | brecha participación (pp) | IC95 | brecha intensidad (h/sem) | IC95 |
|---|---:|---:|---:|---:|
| 12–17 | +2.93 | [+0.55, +5.45] | +3.44 | [+2.48, +4.41] |
| 18–29 | +17.12 | [+15.35, +19.02] | +22.15 | [+20.84, +23.39] |
| 30–39 | +14.71 | [+12.95, +16.52] | +18.30 | [+17.00, +19.65] |
| 40–59 | +6.00 | [+4.51, +7.40] | +8.52 | [+7.55, +9.52] |
| 60+ | −1.06 | [−3.01, +0.70] | +2.75 | [+1.65, +3.87] |

La respuesta descriptiva es **ambas**, con máxima separación en 18–39: ahí
las mujeres participan más y, cuando participan, dedican mucho más tiempo.
En 60+ no se distingue una brecha de participación, pero sí una de intensidad;
por eso la mayor media femenina en ese tramo se asocia descriptivamente con
tiempo condicional, no con más participantes. Esto no identifica efectos del
género ni mecanismos familiares.

La sensibilidad SIN_CP conserva el universo y baja el nacional a 48.90% de
participación, 5.67 horas de media y 11.59 horas entre participantes. Frente a
CON_CP, las diferencias pareadas son −2.95 pp, −5.45 h y −9.85 h,
respectivamente, con IC95 que excluyen cero. SIN_CP significa excluir cuidados
pasivos e incluir emocionales según el FD; no se lo llama cuidado activo.

## Cobertura, integridad y límites

El archivo contiene 74 053 personas; entran 73 891 y masa expandida
107 537 532. Las ocho variables de horas tienen cero faltantes/no numéricos,
cero negativos y cero valores sobre el máximo documental. Se excluyeron 162
filas únicamente porque `EDAD` vale 97 (33) o 98 (129), fuera del rango 12–96
que declara el FD y que se congeló. Esta decisión explica que el `n` 60+ no
iguale el descriptor histórico, que incluyó las 74 053 filas pese a describir
su universo como 12–96. Es una reserva documental material pero pequeña; no se
reescribe el intento sellado.

El agregado no incluye cuidado de personas de 15–59 porque esa variable no
tiene pareja CON_CP/SIN_CP. Las horas pueden superponerse por simultaneidad y
no representan tiempo exclusivo del reloj. No se caparon extremos.

## Validaciones

* `verify`: `REPRODUCE`, contexto `IDENTICO`, 22 RESULT idénticos.
* Identidad contable: error máximo `3.55e-15` horas.
* Las medias nacionales reconstruidas desde los cinco tramos difieren del
  cálculo directo en menos de `1.5e-13` horas.
* Control independiente representativo, mujeres 30–39: participación
  `0.7731949542`; Taylor WR estratificado IC95 `[0.758919, 0.787471]`,
  consistente con bootstrap `[0.758998, 0.787046]`.
* Cuatro pruebas sintéticas dirigidas pasan.
* Cero estratos contienen una sola UPM.
* Replay dirigido posterior a COMMIT-2: `REPRODUCE`, contexto `IDENTICO`.
* `corrida0 registro --verifica --escribe` terminó con `REPLAY-PISADO
  (NC-0094)` por seis corridas ajenas; no escribió ninguna vista. No se usó
  `--lote`, conforme al encargo. Evidencia en `replay-registro.txt`.

## CONSUMIDO

`enut2024_bd_csv` y `enut2024_fd_xlsx`, ambos con hash idéntico al manifiesto;
`CALC-ENUT-0001`, el medidor histórico, el preregistro anterior y las diez
medias por sexo×edad se usaron solo como precedente y control. No se consumió
ninguna reserva ciega ni se modificó `milpa/`.

## NO-CORRIDO / RESERVAS

No se corrieron ejes de ocupación, entidad ni otros instrumentos. No se
estimaron efectos causales ni una descomposición causal. Quedan a mesa la
adopción, el contador y si desea un sucesor que trate 97/98 como edades reales
frente al rango publicado por el FD. `CALC-ENUT-0001` permanece intacto y no
es reemplazado por esta unidad persona. La publicación en las vistas derivadas
queda pendiente de un lote autorizado que resuelva las seis transiciones
ajenas listadas en `replay-registro.txt`; no afecta el sello ni el replay
dirigido de este CALC.
