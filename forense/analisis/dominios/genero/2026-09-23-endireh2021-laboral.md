# ASTRA5-U2 · ENDIREH · Ámbito laboral interpersonal 2021

Estado: **procedimiento sellado**. Medición descriptiva retrospectiva, sin inferencia causal ni adopción.

- CALC: `CALC-ENDIREH-PISOS-2021-LABORAL-0001`; COMMIT-1 `9ab33a8c7ac5ac84694ec6d9866f861dd81544af`.
- `preflight` verde; `run` selló; `verify` **REPRODUCE** (2/2 RESULT).
- `resultados.json` SHA256 `16732c7b6c5cae762ba44d089a84d75745f6e3d4d17df6b1f8aae6a204bc435c`; sello `34f57f6e532cf4fb4ee507a6d0bde9775f19a709553b00e1044c29e01e0de7ca`.
- [endireh2021-laboral-tabla.tsv](endireh2021-laboral-tabla.tsv): 100 celdas, 100 publicables; RESULT `RESULT-ENDIREH2021-LAB-TABLA` conserva réplicas agregadas.

| Ventana | Universo conocido | Prevalencia unión de actos | IC95 de diseño |
|---|---:|---:|---:|
| vida | 88,418 | 19.7806% | 19.4060–20.1569% |
| desde_octubre_2020 | 54,896 | 10.1125% | 9.6802–10.4900% |

Unidad mujer de 15+; factor `FAC_MUJ`; diseño `EST_DIS`/`UPM_DIS`. IC bootstrap por UPM completas dentro de estrato, con dominios de contribución cero. Elegibilidad y códigos de actos están congelados en `spec.md`/`medidor.py`. Un acto es unión de reactivos; salto, no aplica, NS y no respuesta quedan fuera del denominador conocido.

Supresión predefinida por soporte, UPM, CV y ancho de IC; las celdas no publicables figuran sin punto en la tabla. Cortes por edad, escolaridad, localidad, pareja y entidad son estimaciones de dominio. La ventana reciente depende de la redacción del instrumento. No se identifica subregistro ni causalidad. El agregado U0 de 70.1% no se contrasta directamente con este componente.

Origen numérico: microdatos primarios INEGI registrados en manifiesto; GEN1 sólo orientación. La tabla está sellada en disco, pendiente de registro de publicación.
