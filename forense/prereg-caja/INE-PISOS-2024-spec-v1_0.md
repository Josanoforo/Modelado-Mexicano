# CALC-INE-PISOS-2024-0001 · Conteo censal de marcas de voto

El primer resultado que produzca este procedimiento es el que se reporta.
Objeto: elección federal 2024, cuadernillos de lista nominal de casillas
catalogadas por el INE, fuente administrativa de cierre Conteos Censales
DECEyEC 2024. Cada archivo del ZIP corresponde a una entidad; las filas son
sección electoral de la cartografía DERFE 2023 × sexo × edad × elección. La
sección no se une a personas de encuesta. Se exige exactamente 32 CSV.

Filtro: AELEC=2024. Para cada fila se leen EDOCVE, SEXO y los enteros no
negativos LN, SV, NV, NS. SEXO admite 0 hombres, 1 mujeres, 2 no binario.
Se cuenta cada fila con LN distinto de cero y cero. Se registra cada
descuadre LN != SV+NV+NS sin corregirlo ni ocultarlo. Se suma por entidad y
sexo; se produce también total de entidad, sexo nacional y total nacional.
La tasa principal es suma(SV)/suma(LN). Como diagnóstico de cobertura se
reporta NS; la tasa SV/(SV+NV) se rotula sólo entre marcas conocidas. No se
promedian tasas seccionales. Celdas con LN<30 se suprimen. No hay intervalo
de muestreo: es conteo administrativo, sujeto a NS, error de captura y
exclusiones de cobertura. No incluye casillas especiales ni voto en el
extranjero; tampoco equivale a votos válidos, PREP o cómputos definitivos.
La unidad mínima publicada aquí es entidad×sexo (y los marginales).

El parser lee CSV en orden lexicográfico, detecta coma, punto y coma o tabulador
en cabecera por frecuencia máxima, y exige las columnas declaradas. Cualquier
código de entidad/sexo fuera del contrato o conteo no entero detiene la
corrida. La salida textual es JSON canónico con filas ordenadas por geo/sexo.
Sin modelo predictivo ni calibración temporal: una sola elección en este CALC.
Comparación conceptual con ENCUP/LAPOP sólo con universo/fecha explícitos;
este registro no permite inferir motivos individuales o compra de voto.

## Auditoría de rigor extremo

La escala es proporción de registros de lista nominal con marca de voto,
no proporción de personas mexicanas ni voto válido. Geografía y sexo son
categorías administrativas; diferencias no prueban psicología, cultura ni
efecto causal de instituciones. La cobertura omite modalidades especiales,
por lo que comparaciones rurales, indígenas o populares requieren revisar
captura y acceso. No se mezcla cifra retrospectiva con prospección. Esta
especificación no mueve contadores antes de ejecutar el CALC.
