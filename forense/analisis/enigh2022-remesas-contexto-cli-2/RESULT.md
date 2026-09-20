# RESULT · ENIGH 2022 remesas por contexto

## Resultado útil

En ENIGH 2022 la recepción de remesas y su intensidad contable condicional se
concentran en los extremos de localidades pequeñas y estrato socioeconómico
bajo. Esto es una descripción transversal, no evidencia de que las remesas
causen el estrato observado, protejan al hogar o generen dependencia.

Entre localidades con menos de 2,500 habitantes, 10.26% de los hogares recibe
remesas (IC95% 9.60–10.93%), frente a 1.87% (1.70–2.03%) en localidades de
100,000 o más. Entre receptores con ingreso corriente positivo, la remesa
representa en promedio 34.90% del ingreso del hogar (33.59–36.31%) en las
localidades más pequeñas y 22.45% (20.35–24.60%) en las mayores. La proporción
con participación de al menos 50% es 29.26% (27.02–31.56%) y 14.55%
(11.49–17.64%), respectivamente.

En estrato socioeconómico bajo, 9.33% recibe remesas (8.58–10.11%), frente a
1.35% (1.05–1.65%) en estrato alto. Entre receptores, la participación media
es 35.23% (33.60–36.97%) en el estrato bajo y 16.67% (13.51–20.01%) en el
alto; la fracción con participación ≥50% es 30.07% (27.31–32.94%) frente a
5.59% (2.03–9.96%). `est_socio` es la clasificación nativa documentada: no es
un decil de ingreso ni se usa aquí para clasificar “hogares pobres”.

## Contrastes predefinidos

Los seis contrastes son positivos y sus IC de réplicas compartidas no incluyen
cero. Localidad 4 menos 1: prevalencia +8.39 pp (IC95% +7.72 a +9.08),
participación media +12.46 pp (+10.06 a +14.93) y proporción ≥50% +14.71 pp
(+10.93 a +18.56). Estrato 1 menos 4: +7.98 pp (+7.20 a +8.81), +18.55 pp
(+14.89 a +22.22) y +24.48 pp (+19.24 a +28.91), en el mismo orden. No se
hicieron comparaciones oportunistas con categorías intermedias.

La lectura conjunta es explícita: frecuencia e intensidad condicional son
estimandos distintos; un grupo podría tener menos hogares receptores y mayor
participación entre quienes reciben, aunque en estos dos contrastes los tres
estimandos se mueven en la misma dirección.

## Universo, cobertura y diseño

Unidad: hogar. Marco y universo elegible: 90,102 hogares, masa expandida
37,560,123. Remesas válidas: 90,102; receptores: 5,208, masa 1,716,276. Los
5,208 receptores tienen `ing_cor>0` válido. No hubo pesos inválidos, remesas
ausentes/no finitas/negativas, ingresos corrientes inválidos ni casos
`remesas>ing_cor+0.01`. Los residuos de clasificación de ambos ejes están
publicados y vacíos. Las categorías separadas reconstruyen exactamente n,
masas y prevalencia nacional desde numeradores y denominadores.

Precisión: 2,000 réplicas comunes de UPM dentro de 560 estratos, 10,211 UPM,
cero estratos singleton y cero réplicas degeneradas en los contrastes. Se
publican todas las celdas, incluidas las vacías, sin umbral de ocultamiento.

## Controles y reservas

El total reproduce los dos antecedentes en prevalencia, media/mediana de monto
y los tres cocientes (deltas numéricos de cero a 2.7e-11). El cálculo focal
independiente con `math.fsum` da media nacional 14,455.4298 pesos y el EE
linealizado independiente por UPM/estrato es 386.342 pesos. La media de razones
nacional es 0.304923 y la razón de sumas 0.274688: no se intercambian.

Los montos son pesos de 2022 por trimestre normalizado. No se anualizaron,
deflactaron, imputaron ni truncaron. Una sola ola no permite inferir quién
emigró, trayectorias, volatilidad, respuesta a choques, ingreso sin remesas o
causalidad entre remesas y contexto.

Tablas completas: `perfil.tsv` y `contrastes.tsv`. Fuente sellada:
`data/corrida0/CALC-ENIGH2022-REMESAS-CONTEXTO-0001/resultados.json`.

