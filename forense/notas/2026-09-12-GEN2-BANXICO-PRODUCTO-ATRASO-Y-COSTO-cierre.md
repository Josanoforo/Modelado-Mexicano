# ACTO GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO · cierre

Fecha de ejecución: 11–12/sep/2026. Entorno: CAJA, Ubuntu/WSL2, Python 3.14.4,
corpus compartido montado. Worktree:
`/home/pc0/mm-gen2-banxico-producto-atraso-costo`; rama:
`acto/gen2-banxico-producto-atraso-costo`; base efectiva:
`origin/main=e4c25385e218e7e30c4cc45ecdff65a6fcaa36a5` (#743), posterior a la
base `6e634aa` declarada en el encargo. El árbol propio arrancó limpio. El clon
principal ajeno estaba 116 commits detrás y tenía `error.log` no rastreado; no
se tocó.

Perímetro ejecutado: spec descriptiva, medición real, control independiente,
agregados, gráfico, registros de la relación Banxico de N34 y oferta para el
encargo 40. Cero adquisición, motor, adopción, causalidad, F5, cron o cambios a
los helpers excluidos.

## 1. Resultado

Se creó y selló `CALC-BANXICO-PRODUCTO-DANO-0001` sobre el XLSX oficial de
12,408 filas persona-ola y 142 columnas. Recorre cinco productos y seis cortes;
genera 270 estimandos principales, 1,320 celdas conjuntas costo×pago, 55 celdas
costo–daño 2024, un resumen de 30 filas y un gráfico. Los tres insumos
(microdato, manual e informe) coinciden byte a byte con el manifiesto.

| producto | 2024 n pago válido | atraso | imposibilidad/impago | unión |
|---|---:|---:|---:|---:|
| tarjeta de crédito | 554 | 4.236% | 0.015% | 4.251% |
| crédito hipotecario | 426 | 18.510% | 0.173% | 18.683% |
| crédito personal | 419 | 8.032% | 0.539% | 8.570% |
| crédito de nómina | 412 | 10.352% | 0.000% | 10.352% |
| crédito automotriz | 128 | 4.309% | 0.000% | 4.309% |

Los ceros de imposibilidad son respuestas válidas con masa positiva y cero
numerador; no se confunden con el no levantamiento. En 2019, las 422 personas
con hipotecario, 398 con nómina y 128 con automotriz tienen el reactivo de pago
en blanco: sus proporciones quedan nulas. Tarjeta y personal sí son estimables.

## 2. Contrato y denominadores

El manual fija para tarjeta `3=atraso`, `4=no ha pagado`; para los otros
créditos `2|3=atraso`, `4=no ha podido pagar`. Pago válido es `1..4`, costo
percibido conserva `0..10`, problemas y reclamación usan `1|2`. Reclamación se
estima únicamente entre quienes reportaron problema (`problemas=1`): por
ejemplo, en hipotecario 2024 son 40 elegibles/válidos, 20 reclamantes y 53.78%
ponderado, no 20 entre 428 tenedores.

Cada fila tabular declara el universo, conteos elegible/válido/positivo, masas,
faltantes por causa y cociente. Los 12,408 pesos son finitos y positivos. No se
calculan EE/IC porque no están acreditadas UPM, estratos ni una receta de
varianza; el ponderador sólo sustenta los puntos.

## 3. Lectura sustantiva

El daño de tarjeta alcanza 9.25% en 2021 y 4.25% en 2024. En los productos con
serie desde 2020, 2024 está por debajo de 2020: hipotecario 23.03→18.68%,
personal 26.44→8.57%, nómina 14.36→10.35% y automotriz 27.68→4.31%. Son
diferencias entre cortes transversales, sin EE/IC, no cambios individuales ni
efectos.

Las tasas 2024 por cada nivel original de costo no forman una relación
monotónica estable y tienen mucha granularidad: 37/55 celdas poseen `n<30`,
10/55 `n<10`, y las once celdas automotrices tienen `n<30`. Se publican todas,
incluidos ceros y tamaños pequeños. La calificación es percepción de intereses,
no CAT ni tasa; la asociación está sujeta a selección en tenencia, autorreporte
y confusión.

## 4. Verificación

- `corrida0 preflight`: VERDE; 35 RESULT únicos, tres inputs COINCIDE, spec
  commiteada y árbol limpio.
- Primera invocación de `run`: falló antes del sello porque el adaptador pasó el
  registro completo del input en vez de `ruta_absoluta`; se corrigió una línea,
  se commiteó y se repitió desde preflight.
- Segunda invocación: exit 0, sello válido; corrida
  `CALC-BANXICO-PRODUCTO-DANO-0001--20ff8eb70fc3`.
- `corrida0 verify`: `REPRODUCE`, contexto `IDENTICO`, 35/35 RESULT y 3/3
  inputs coincidentes.
- Control independiente con `openpyxl`: `COINCIDE`; reproduce TDC 2024,
  reclamación hipotecaria filtrada, no levantamiento hipotecario 2019, 5/5
  conteos/masas 2024 contra #734 y 5/5 hashes de artefactos contra RESULT.
- `spec-check`: 0 OK/27 FAIL sobre 317,718 filas porque los inventarios vigentes
  contienen cero filas de este XLSX nuevo. La existencia de columnas se
  comprueba físicamente contra el encabezado de 142 columnas y el manual; no se
  reetiquetó el negativo de inventario.

## 5. Producto para 40 y reserva

La ficha consumible es
`data/banxico-producto-dano-medicion/ficha-consumo-banxico.md`; el
resumen temporal está en `resumen-producto-ola.csv`, la auditoría completa en
`estimandos.csv`, la conjunta en `conjunta-costo-pago.csv` y los niveles 2024
en `costo-dano-2024.csv`. El encargo 40 puede citar esos puntos como descripción
o asociación mexicana urbana por categoría de producto.

No se adopta ninguna tasa al motor. `NC-0164` permanece abierta por producto o
lender mexicano exacto/BNPL, costo objetivo (CAT/tasa/fricción) e identificación
causal. La relación Banxico de N34 sí pasa de insumo preparado a medición
sellada disponible; las relaciones SHED/CFPB y el cierre global de NC-0164 no
se modifican.
