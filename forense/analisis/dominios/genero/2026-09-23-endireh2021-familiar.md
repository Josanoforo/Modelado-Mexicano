# ASTRA5-U2 · ENDIREH · Ámbito familiar 2021

Estado: **procedimiento sellado**. Medición descriptiva retrospectiva, sin inferencia causal ni adopción.

- CALC: `CALC-ENDIREH-PISOS-2021-FAMILIAR-0001`; COMMIT-1 `f78355a781452e33507e3b3cca287c5737bd6b0f`.
- `preflight` verde; `run` selló; `verify` **REPRODUCE** (2/2 RESULT).
- `resultados.json` SHA256 `6806febd86451de569944ee99a4e0a9f43278ab40bc56575e3057cfe562b60d7`; sello `5a463f9a679de60acfcee89bd669ac86041f460ad9553f62649d2993f45c4667`.
- [endireh2021-familiar-tabla.tsv](endireh2021-familiar-tabla.tsv): 50 celdas, 50 publicables; RESULT `RESULT-ENDIREH2021-FAM-TABLA` conserva réplicas agregadas.

| Ventana | Universo conocido | Prevalencia unión de actos | IC95 de diseño |
|---|---:|---:|---:|
| desde_octubre_2020 | 110,127 | 11.3861% | 11.0672–11.6583% |

Unidad mujer de 15+; factor `FAC_MUJ`; diseño `EST_DIS`/`UPM_DIS`. IC bootstrap por UPM completas dentro de estrato, con dominios de contribución cero. Elegibilidad y códigos de actos están congelados en `spec.md`/`medidor.py`. Un acto es unión de reactivos; salto, no aplica, NS y no respuesta quedan fuera del denominador conocido.

Supresión predefinida por soporte, UPM, CV y ancho de IC; las celdas no publicables figuran sin punto en la tabla. Cortes por edad, escolaridad, localidad, pareja y entidad son estimaciones de dominio. La ventana reciente depende de la redacción del instrumento. No se identifica subregistro ni causalidad. El agregado U0 de 70.1% no se contrasta directamente con este componente.

Origen numérico: microdatos primarios INEGI registrados en manifiesto; GEN1 sólo orientación. La tabla está sellada en disco, pendiente de registro de publicación.
