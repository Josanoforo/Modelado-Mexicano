# Inserción lista · precisión del descriptivo WBES México 2023

## Qué precisión se agregó

El punto descriptivo propio no cambia: entre los establecimientos expuestos
con desenlace clasificable, 15.24% reportó al menos una solicitud o expectativa
de regalo/pago informal. La extensión reproduce, al grano publicado, el total y
los cuatro tamaños de `CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001`; la máxima
diferencia numérica antes de redondear es `4.57e-13`.

El diseño operativo disponible es de una etapa: establecimientos seleccionados
por muestreo aleatorio simple dentro de estratos de industria × región × tamaño
× condición panel/fresco. `strata` identifica el estrato y cada establecimiento
es una unidad de muestreo; `a6a` sólo define los tamaños publicados. La varianza
de la razón ponderada se linealizó con `wmedian` sobre la muestra completa de
1,322 establecimientos. Las unidades fuera de cada dominio aportan cero: no se
filtraron antes de construir la varianza.

| Dominio | n clasificable | Punto | EE / IC95 singleton=certeza | EE / IC95 singleton=average | Límites lógicos por faltantes |
|---|---:|---:|---:|---:|---:|
| Total | 242 | 15.24% | 4.95 pp / 7.82%–27.60% | 5.34 pp / 7.40%–28.79% | 14.89%–17.21% |
| Pequeña (5–19) | 102 | 15.38% | 6.45 pp / 6.43%–32.47% | 6.96 pp / 5.98%–34.17% | 15.30%–15.80% |
| Mediana (20–99) | 57 | 14.15% | 7.96 pp / 4.36%–37.34% | 8.58 pp / 3.96%–39.73% | 13.43%–18.50% |
| Grande (100–250) | 41 | 17.64% | 7.61 pp / 7.11%–37.45% | 8.21 pp / 6.60%–39.36% | 15.54%–27.44% |
| Extra grande (251+) | 42 | 14.54% | 7.90 pp / 4.66%–37.21% | 8.52 pp / 4.24%–39.53% | 13.26%–22.04% |

Los IC son `IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS`, no intervalos oficiales.
Usan linealización de Taylor con aproximación con reemplazo, 242 estratos, 34
estratos singleton y 1,080 grados de libertad; no aplican corrección finita.
El IC95 se construyó en escala logit con crítico t y el EE se reporta en escala
de proporción.

## Qué cuestan los supuestos

La documentación oficial acredita selección aleatoria simple dentro de celda,
pesos ajustados por elegibilidad y combinación de muestras panel/fresca. El
*Sampling Note* advierte además que un panel singleton puede ser selección de
certeza. Sin embargo, México 2023 no publica la probabilidad/FPC por celda
panel/fresca que permitiría reconocer cuáles de los 34 singleton observados
son realmente de certeza; 29 son panel y 5 frescos. Tampoco hay réplicas
oficiales.

Por ello se conservan dos escenarios fijados antes del IC: `certeza` asigna
aporte cero a todo singleton; `average` imputa a cada uno la contribución media
de los estratos no singleton. El segundo produce EE entre 7.9% y 8.0% mayores
que el primero en los cinco dominios. Ninguno es una cota garantizada y no se
elige el más estrecho. La aproximación tampoco propaga incertidumbre adicional
de los ajustes de elegibilidad/no respuesta del ponderador.

Los límites lógicos por faltantes permanecen separados. Condicionan qué pasaría
si los desenlaces desconocidos fueran todos negativos o todos positivos; no
tienen cobertura muestral. A su vez, los IC describen error muestral del punto
entre clasificables y no eliminan posible sesgo por no respuesta.

## Cómo cambia la interpretación

La sensibilidad a desenlaces faltantes del total es estrecha (14.89%–17.21%),
pero la incertidumbre muestral aproximada es mucho mayor (cerca de 7%–29%). En
los tamaños, los IC son todavía más amplios. Por tanto, 15% sigue siendo una
magnitud descriptiva útil, pero no una cifra precisa para ordenar tamaños: que
grandes tenga 17.64% y medianas 14.15% no acredita diferencia estadística.

Tampoco procede inferir significancia por traslape de IC marginales, comparar
numéricamente WBES con ENCRIGE, generalizar fuera del universo WBES, afirmar
que el pago ocurrió o presentar estos IC como productos oficiales del Banco
Mundial. La pieza faltante para pasar de aproximación condicional a una receta
de diseño plenamente acreditada es la probabilidad/FPC operativa por celda
panel/fresca —o réplicas oficiales— junto con el tratamiento oficial de sus
singleton.
