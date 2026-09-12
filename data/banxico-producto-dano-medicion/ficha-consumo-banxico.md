# Ficha de consumo · Banxico producto, atraso y costo percibido

## Oferta

`CALC-BANXICO-PRODUCTO-DANO-0001` mide puntos ponderados por producto y ola
con la Encuesta de Satisfacción de las Personas Usuarias de Productos y
Servicios Financieros de Banco de México, 2019–2024. Población: personas
mexicanas de 18–70 años con producto financiero en localidades de 50 mil
habitantes o más. Las olas son cortes transversales separados y los productos
no son excluyentes.

| producto | n válido 2024 | atraso % | imposibilidad/impago % | daño combinado % |
|---|---:|---:|---:|---:|
| tarjeta de crédito | 554 | 4.236 | 0.015 | 4.251 |
| crédito hipotecario | 426 | 18.510 | 0.173 | 18.683 |
| crédito personal | 419 | 8.032 | 0.539 | 8.570 |
| crédito de nómina | 412 | 10.352 | 0.000 | 10.352 |
| crédito automotriz | 128 | 4.309 | 0.000 | 4.309 |

El estimando de tarjeta usa atraso=`3`, impago=`4`; los otros productos usan
atraso=`2|3`, imposibilidad=`4`. Los denominadores excluyen `5`/NS-NC, saltos,
blancos y códigos inválidos, y las masas excluyen pesos no positivos. En 2019,
hipotecario, nómina y automotriz no levantan pago en los bytes: las salidas son
no estimables, no ceros.

## Archivos

- `estimandos.csv`: 270 filas; distribución completa de pago, atraso,
  imposibilidad, daño, problemas y reclamación condicionada a problema.
- `conjunta-costo-pago.csv`: 1,320 celdas (30 producto×ola × 11 costos × 4
  respuestas de pago), con denominadores y faltantes.
- `costo-dano-2024.csv`: 55 tasas de daño, una por nivel 0–10 y producto. Se
  preservan las 37 celdas con `n válido < 30` y las 10 con `n válido < 10`.
- `resumen-producto-ola.csv`: 30 filas compactas para lectura temporal.
- `atraso-por-producto-ola.svg`: gráfico de daño combinado; huecos indican
  reactivo no levantado.

Todos los CSV conservan `producto`, `ola`, variable/códigos, universo,
`n_elegible`, `n_valido`, `n_positivo`, masas correspondientes, faltantes por
causa, estimación, unidad y alcance. Sus hashes están sellados como RESULT del
CALC. `control-independiente.json` acredita los controles materiales con un
lector distinto.

## Lectura para N34/R1.7 y para el encargo 40

Entre cortes comparables, el daño combinado de tarjeta fue 5.98%, 7.38%,
9.25%, 5.97%, 8.08% y 4.25% entre 2019 y 2024. Hipotecario bajó de 23.03% en
2020 a 18.68% en 2024, personal de 26.44% a 8.57%, nómina de 14.36% a 10.35%
y automotriz de 27.68% a 4.31%; no se publica 2019 para los tres productos sin
reactivo. Son cambios entre cortes, no transiciones de las mismas personas, y
no tienen EE/IC porque el diseño necesario no quedó acreditado.

Las 55 celdas 2024 de costo–daño son irregulares y frecuentemente pequeñas;
no sostienen por sí solas una pendiente monotónica. La escala 0–10 es costo
percibido (0=bajo, 10=alto), no CAT, tasa contractual ni monto. El uso válido
es descripción/asociación mexicana por categoría de producto. No calibra la
probabilidad del motor, no identifica un efecto causal y no cierra `NC-0164`
(lender/producto mexicano exacto, costo objetivo e identificación causal).

## Reproducción

```bash
python3 tools/corrida0.py verify CALC-BANXICO-PRODUCTO-DANO-0001
PYTHONPATH=. python3 data/corrida0/CALC-BANXICO-PRODUCTO-DANO-0001/medidor.py \
  --out data/banxico-producto-dano-medicion
python3 data/corrida0/CALC-BANXICO-PRODUCTO-DANO-0001/control_independiente.py
```
