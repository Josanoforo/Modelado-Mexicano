# CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001

## Pregunta y alcance

Mide si las brechas descriptivas de carga de cuidado por sexo y edad aparecen
en la participación, en la intensidad entre participantes o en ambas. La
unidad es persona de 12 a 96 años en `tvar_crea.csv`; el ponderador es
`FAC_PER`. No releva automáticamente a `CALC-ENUT-0001`, cuya unidad y
estimando son hogar y reparto de horas.

La familia principal de horas semanales suma, exactamente como el precedente,
`CUID_ESP_INT_HOG_CON_CP`, `CUID_INT_0A5_CON_CP`,
`CUID_INT_6A14_CON_CP` y `CUID_INT_60MAS_CON_CP`. No incluye
`CUID_INT_15A59`, que carece de pareja CON_CP/SIN_CP, ni cuidados a otros
hogares. Es un agregado de horas declaradas que puede contener simultaneidad;
no es tiempo exclusivo del reloj y no se capa en 168 horas.

La sensibilidad SIN_CP usa las cuatro parejas documentadas por el FD como
excluyendo cuidados pasivos e incluyendo cuidados emocionales. No se etiqueta
como «cuidado activo».

## Exposición previa y novedad

Antes de congelar se conocían `CALC-ENUT-0001` y las diez medias GEN1 por
sexo×edad publicadas en `milpa/tramite.yaml`. Esta corrida reestima esas medias
con incertidumbre de diseño; son nuevos la participación `P(h>0)`, la media
condicional `E(h|h>0)`, los contrastes mujeres–hombres con covarianza, la
sensibilidad pareada SIN_CP−CON_CP y sus intervalos. No se reclama ceguera.
No se encontró equivalente exacto en `main` ni en las ramas remotas activas al
19/sep/2026.

## Universo común, faltantes y cortes

`LLAVEMOD` es la llave primaria de persona según el FD. El marco documentado
es edad 12–96. Son válidas `SEXO` 1=hombre/2=mujer, edad 12–96, `FAC_PER`
finito y positivo, `EST_DIS`/`UPM_DIS` no vacíos y las ocho variables de
horas numéricas dentro de los rangos no negativos del FD. Una fila inválida
en cualquiera de esos campos queda fuera del universo común CON_CP/SIN_CP y
se cuenta por causa. Un cero dentro del rango es genuino; un blanco, no
numérico, negativo o valor sobre el máximo documental no se vuelve cero.

Cortes, reutilizados de la salida previa: 12–17, 18–29, 30–39, 40–59 y 60+.
Se publican nacional, sexo, edad y sexo×edad; ningún otro eje. Cada fila trae
`n` y masa del marco del grupo, `n` y masa válidos, cobertura y denominador de
participantes. Un denominador vacío produce `NO-ESTIMABLE`, nunca cero.

## Estimandos e incertidumbre

Con los mismos pesos y cobertura:

* `P(h>0) = Σw I(h>0) / Σw`;
* `E(h) = Σw h / Σw`, incluidos ceros válidos;
* `E(h|h>0) = Σw h / Σw I(h>0)`.

Se publican diferencias mujer menos hombre para total y cada tramo, y
diferencias pareadas SIN_CP menos CON_CP para todas las celdas. Un único plan
de 2 000 réplicas, `numpy.PCG64`, semilla 20260919, remuestrea UPM con
reemplazo dentro de cada `EST_DIS`, conserva el número de UPM por estrato y
recalcula todas las razones y diferencias dentro de la misma réplica. Un
estrato de una UPM se remuestrea a sí mismo y aporta varianza cero; su número
se informa. IC95 por percentiles 2.5/97.5. No hay bootstrap iid de personas.

La identidad `E(h)=P(h>0)×E(h|h>0)` se comprueba en cada celda. También se
reconcilian denominadores y se compara el cálculo directo con los suficientes
agregados por UPM. La identidad es contable, no causal: no se estiman efectos
del género, preferencias ni mecanismos familiares.

## Salidas y gobierno

Las tablas largas son `estimaciones.csv` y `contrastes.csv`; las incidencias
de incompatibilidad están en `incidencias.json`. Sus hashes son RESULT del
CALC y el sello liga esos RESULT con spec, medidor y ejecución. El primer
resultado producido por este procedimiento es el reportado. Contador y
adopción quedan `PENDIENTE-DE-MESA`; esta corrida no modifica `milpa/`.
