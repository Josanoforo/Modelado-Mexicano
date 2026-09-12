# CALC-IMOR-CONTEXTO-0001 · especificación congelada

Fecha de congelamiento: 11/sep/2026. Acto:
`GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN`. Esta especificación se fija antes
de ejecutar el medidor sobre la serie completa.

## 1. Pregunta y objeto

Describir cómo varían el nivel, los cambios y la dispersión temporal del IMOR
publicado por Banco de México, por producto y dentro de cada régimen de
definición. El objeto es un porcentaje mensual de **saldos**, no una
probabilidad individual, una tasa de personas ni un error estándar de
encuesta.

Consumidor contextual: `dinero.credito.scoring_alternativo` (`R1.6`). Uso:
`DESCRIPTIVO-NO-CALIBRA`; no altera el motor ni sustituye una regla de
scoring.

## 2. Entrada congelada

- Archivo versionado:
  `data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv`.
- SHA-256: `772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9`.
- Corte esperado: 2016-01..2026-03, 123 meses, cinco productos, 615 filas.
- Universo institucional: banca comercial; incluye Sofomes ER subsidiarias
  de instituciones bancarias y grupos financieros; excluye CI Banco.
- `ABCD`: adquisición de bienes de consumo duradero, incluidos bienes muebles
  y automotriz.
- Fuente primaria de la tabla: publicación oficial equivalente de Banxico
  manifestada como
  `gen2_banxico_imor_consumo_producto_mensual_2026t1_html`; no es R16 CNBV.

El cierre de #723 y las notas incluidas en la publicación acreditan una sola
ruptura metodológica dentro del corte: enero de 2022. No se encontró otra
ruptura documentada en esos materiales. La foto CNBV R16 de 2021-12 queda
fuera de este cálculo.

## 3. Ventanas y estimandos

Regímenes, calculados siempre por separado:

1. `PRE_IFRS9_CARTERA_VENCIDA`: 2016-01..2021-12; numerador, saldo de cartera
   vencida.
2. `IFRS9_ETAPA_3`: 2022-01..2026-03; numerador, saldo clasificado en etapa 3.

Para cada producto y régimen se calcula:

- nivel mensual publicado, en porcentaje;
- cambio mensual, `valor[t] - valor[t-1]`, en puntos porcentuales, sólo si
  ambos meses pertenecen al mismo régimen y son consecutivos;
- cambio interanual, `valor[t] - valor[t-12]`, en puntos porcentuales, sólo si
  ambos extremos pertenecen al mismo régimen;
- los mismos cambios relativos, `100 * (valor[t] / valor[previo] - 1)`, en
  porcentaje relativo y en columnas distintas de los puntos porcentuales;
- media temporal uniforme entre meses, mediana, mínimo/máximo y todas sus
  fechas;
- desviación estándar **poblacional** (`ddof=0`) entre los meses observados
  para el nivel, los cambios mensuales y los cambios interanuales.

El primer mes de cada régimen conserva cambio mensual vacío. Los primeros
doce meses de cada régimen conservan cambio interanual vacío. No se calcula el
salto 2021-12→2022-01. No se promedian productos para fabricar un IMOR total:
se usa `Consumo total`, la serie agregada publicada.

Las medias temporales dan el mismo peso a cada mes y no reconstruyen un ratio
agregado de saldos, porque la tabla no incluye los denominadores monetarios.
Mínimos y máximos son extremos del periodo observado. La desviación temporal
no es incertidumbre de muestreo.

## 4. Salidas y aceptación

La corrida canónica devuelve guardias y dos resúmenes JSON, uno por régimen.
El mismo script, en modo de materialización, escribe bajo
`data/analisis-imor-contexto-temporal/`:

- niveles mensuales;
- cambios mensuales e interanuales en pp y porcentaje relativo;
- resumen por producto y régimen;
- dos figuras SVG exportables, una de niveles y otra de cambios mensuales.

Aceptación:

- llave `fecha×producto` única; cinco productos exactos;
- 123 meses continuos y cinco filas por mes;
- regímenes y numeradores coherentes con la fecha;
- cero valores ausentes, no numéricos o fuera de 0..100;
- 615 niveles, 605 cambios mensuales calculables y 495 interanuales;
- ningún cambio cruza la ruptura;
- referencias numéricas reconstruidas por una implementación independiente.

## 5. Límites y conteo

Es un CALC para aprovechar el contrato canónico de identidad, ejecución,
sello y replay. Se rotula `cuenta_gen2: NO-DERIVACION-CONTEXTUAL`: deriva
estadísticos de una serie ya adquirida/publicada y el encargo no firma una
nueva medición independiente para el contador. No calibra R1.6, no adopta
parámetros, no valida predicción, no estima causalidad y no cierra N34.
