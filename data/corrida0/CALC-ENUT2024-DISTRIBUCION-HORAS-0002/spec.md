# CALC-ENUT2024-DISTRIBUCION-HORAS-0002

Sucesor no numérico de `CALC-ENUT2024-DISTRIBUCION-HORAS-0001`. Conserva
íntegramente estimandos, universo, seed y resultados; corrige únicamente los
cuatro basenames genéricos que T02 detectó después del sello inicial. El
primer resultado, ejecución y sello permanecen inmutables en el CALC padre y
en el commit `2f0954cf4303ee58cdbf53eb426e5bfd4adfc2d5`.

## Pregunta y alcance

Describe qué ocultan las medias de cuidado de ENUT 2024: percentiles de horas
y fracción de las horas acumulada por el 10% superior de personas. La unidad
es persona de 12 a 96 años en `tvar_crea.csv`; el ponderador es `FAC_PER`.
Es una descripción de horas declaradas, no un diagnóstico de sobrecarga ni
tiempo exclusivo del reloj.

Las horas CON_CP y SIN_CP suman, respectivamente, las cuatro parejas
`CUID_ESP_INT_HOG`, `CUID_INT_0A5`, `CUID_INT_6A14` y
`CUID_INT_60MAS`. No se añade 15A59 ni cuidado de otro hogar. SIN_CP excluye
cuidados pasivos e incluye emocionales según el FD; no se denomina cuidado
activo. No se recorta a 168 horas ni se winsorizan observaciones.

## Exposición previa y novedad

Antes de congelar se conocían `CALC-ENUT-0001`, las medias históricas y el
resultado completo de `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001` (#879),
que se usa como control de universo, medias y participación. No se reclama
ceguera. No se encontró un equivalente por contenido en CALC, análisis,
encargos, ramas o PR al 19/sep/2026.

## Universo, dominios y diseño

Se conserva exactamente el universo común del padre: llave `LLAVEMOD` única,
`SEXO` 1/2, edad 12–96, `FAC_PER` finito y positivo, diseño `EST_DIS` y
`UPM_DIS` completo y las ocho horas numéricas, no negativas y dentro de los
máximos documentales. Edad 97/98 queda en reserva y fuera de los dominios. Un
cero válido permanece; un desconocido no se vuelve cero.

El plan de réplicas se construye desde todas las filas con peso y claves de
diseño válidos. El universo analítico y los subgrupos entran como dominios de
contribución cero, no reduciendo el marco a participantes. Se publican total,
hombres y mujeres para dos dominios: todas las personas válidas (ceros
incluidos) y participantes de cada variante (`h>0`). Cada fila informa `n`,
masa y cobertura respecto del universo inmediato: marco 12–96 para todas las
válidas y personas válidas para participantes.

## Estimandos congelados

Los percentiles ponderados p25, p50, p75 y p90 son la inversa izquierda de la
CDF empírica: el menor valor cuya masa acumulada alcanza `p * masa_total`.
No hay interpolación. La concentración es la fracción de horas ponderadas que
acumula exactamente el 10% superior de la masa de personas ordenadas por
horas. Si el umbral corta una observación o un empate, se usa la fracción de
peso necesaria; como todas las personas empatadas aportan las mismas horas,
el resultado es invariante al orden. Si las horas totales son cero, no es
estimable.

Se repite todo con SIN_CP sobre el mismo universo. Se estiman diferencias
pareadas SIN_CP−CON_CP de p50, p90 y concentración por sexo y dominio, y
diferencias mujer−hombre de p50 y p90 CON_CP por dominio. No hay cortes por
edad ni selección posterior de grupos.

## Incertidumbre y salidas

Un plan común de 2 000 réplicas, `numpy.PCG64` semilla 20260919, remuestrea
UPM con reemplazo dentro de `EST_DIS`, conservando el número de UPM. Un
estrato de UPM única se remuestrea a sí mismo. Cada réplica recalcula
percentiles, umbral fraccionado, concentración y contrastes; IC95 usa
percentiles 2.5/97.5. Se reportan réplicas válidas. Un intervalo colapsado por
masa en un valor se etiqueta como propiedad discreta del estimador, no como
ausencia demostrada de error.

Las tablas largas deterministas son `distribucion.csv` y `contrastes.csv`,
acompañadas por `incidencias.json`. Sus hashes son RESULT. Contador, consumo y
adopción quedan `PENDIENTE-DE-MESA`; no se modifica `milpa/`.
