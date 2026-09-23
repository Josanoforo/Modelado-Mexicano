# ASTRA5-U2 · ENDIREH · Ámbito comunitario 2021

Estado: **procedimiento sellado**. Medición descriptiva retrospectiva, sin inferencia causal ni adopción.

- CALC: `CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001`; COMMIT-1 `7b5726c8eb2c4f2c70ebe34409836adb3ee865c0`.
- `preflight` verde; `run` selló; `verify` **REPRODUCE** (2/2 RESULT).
- `resultados.json` SHA256 `443417ff6f80128f80756919e62d53757001bc0be55a51f0e063306bd61044e7`; sello `5c7a47a33a1b717423f79fe2c5c46d311b84741e796781735e20f6577ddfb51c`.
- [endireh2021-comunitaria-tabla.tsv](endireh2021-comunitaria-tabla.tsv): 100 celdas, 100 publicables; RESULT `RESULT-ENDIREH2021-COM-TABLA` conserva réplicas agregadas.

| Ventana | Universo conocido | Prevalencia unión de actos | IC95 de diseño |
|---|---:|---:|---:|
| vida | 110,127 | 45.5779% | 45.1124–45.9419% |
| desde_octubre_2020 | 110,114 | 22.4214% | 21.9262–22.8842% |

Unidad mujer de 15+; factor `FAC_MUJ`; diseño `EST_DIS`/`UPM_DIS`. IC bootstrap por UPM completas dentro de estrato, con dominios de contribución cero. Elegibilidad y códigos de actos están congelados en `spec.md`/`medidor.py`. Un acto es unión de reactivos; salto, no aplica, NS y no respuesta quedan fuera del denominador conocido.

Supresión predefinida por soporte, UPM, CV y ancho de IC; las celdas no publicables figuran sin punto en la tabla. Cortes por edad, escolaridad, localidad, pareja y entidad son estimaciones de dominio. La ventana reciente depende de la redacción del instrumento. No se identifica subregistro ni causalidad. El agregado U0 de 70.1% no se contrasta directamente con este componente.

Origen numérico: microdatos primarios INEGI registrados en manifiesto; GEN1 sólo orientación. La tabla está sellada en disco, pendiente de registro de publicación.
